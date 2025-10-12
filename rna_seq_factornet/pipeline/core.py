# rna_seq_factornet/pipeline/core.py
"""
Main pipeline for RNA-seq expression analysis with simple, clean API
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Union, List
from sklearn.model_selection import KFold

from ..data.loader import ExpressionDataLoader
from ..models.factornet import ExpressionFactorNet
from ..interpretation.methods import InterpretationMethods
from ..interpretation.visualizer import InterpretabilityVisualizer


def _regression_metrics(y_true, y_pred):
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 0.0 if ss_tot == 0 else 1 - ss_res / ss_tot
    mae = float(np.mean(np.abs(y_true - y_pred)))
    mse = float(np.mean((y_true - y_pred) ** 2))
    pr = (
        np.corrcoef(y_true, y_pred)[0, 1]
        if np.std(y_true) > 0 and np.std(y_pred) > 0
        else np.nan
    )
    return {"r2": float(r2), "mae": mae, "mse": mse, "pearson_r": float(pr)}


class ExpressionPipeline:
    """
    Simple, user-friendly pipeline for RNA-seq expression analysis
    """

    def __init__(self, cache_dir: str = "./cache"):
        """Initialize pipeline"""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

        self.loader = ExpressionDataLoader(str(self.cache_dir))
        self.model = None
        self.data = None
        self.interpreter = None
        self.visualizer = InterpretabilityVisualizer()

        print("🧬 RNA-seq FactorNet Pipeline initialized")

    def load_data(
        self,
        filepath: str,
        nan_strategy: str = "remove",
        min_expression: float = 0.5,
        feature_selection: str = "variance",
        **kwargs,
    ) -> Dict:
        """Load and preprocess expression data"""
        print(f"📊 Loading data from {filepath}...")

        # Load raw data
        raw_data = self.loader.load_expression_data(
            filepath, nan_strategy=nan_strategy, **kwargs
        )

        # Preprocess
        self.data = self.loader.preprocess_for_factornet(
            raw_data,
            min_expression=min_expression,
            feature_selection=feature_selection,
        )

        print(
            f"✅ Data loaded: {len(self.data['gene_names'])} genes, "
            f"{self.data['preprocessing_params']['n_features']} samples"
        )

        return self.data

    def train_model(
        self,
        use_cv: bool = True,
        k_folds: int = 5,
        epochs: int = 50,
        batch_size: int = 16,
        **model_params,
    ) -> Dict:
        """
        Train the FactorNet model (Option 2: Keras fit/predict style)
        Prints R², MAE, MSE, Pearson r; supports optional k-fold CV.
        """
        if self.data is None:
            raise ValueError("Load data first using load_data()")

        print("🤖 Training FactorNet model...")

        X = self.data["expression_features"]
        y = self.data["expression_targets"]
        n_features = X.shape[1]

        default_params = {
            "conv_filters": 32,
            "lstm_units": 32,
            "dense_units": 64,
            "dropout_rate": None,
        }
        default_params.update(model_params)

        def _build_model():
            return ExpressionFactorNet(input_dim=n_features, **default_params)

        # ---- No CV (single fit) ----
        if not use_cv:
            self.model = _build_model()
            hist = self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)
            yhat = self.model.predict(X)
            metrics = _regression_metrics(y, yhat)
            print(
                f"✅ Training completed | R²: {metrics['r2']:.4f} | "
                f"MAE: {metrics['mae']:.4f} | MSE: {metrics['mse']:.4f} | r: {metrics['pearson_r']:.4f}"
            )
            self.interpreter = InterpretationMethods(self.model)
            return {"history": hist.history, **metrics}

        # ---- With CV ----
        kf = KFold(n_splits=k_folds, shuffle=True, random_state=0)
        r2s, maes, mses, rs = [], [], [], []
        for tr, va in kf.split(X):
            m = _build_model()
            m.fit(X[tr], y[tr], epochs=epochs, batch_size=batch_size, verbose=0)
            yhat = m.predict(X[va])
            mtr = _regression_metrics(y[va], yhat)
            r2s.append(mtr["r2"])
            maes.append(mtr["mae"])
            mses.append(mtr["mse"])
            rs.append(mtr["pearson_r"])

        cv = {
            "cv_mean_r2": float(np.mean(r2s)),
            "cv_std_r2": float(np.std(r2s)),
            "cv_mean_mae": float(np.mean(maes)),
            "cv_std_mae": float(np.std(maes)),
            "cv_mean_mse": float(np.mean(mses)),
            "cv_std_mse": float(np.std(mses)),
            "cv_mean_r": float(np.nanmean(rs)),
            "cv_std_r": float(np.nanstd(rs)),
        }
        print(
            f"✅ CV completed | R²: {cv['cv_mean_r2']:.4f} ± {cv['cv_std_r2']:.4f} | "
            f"MAE: {cv['cv_mean_mae']:.4f} | MSE: {cv['cv_mean_mse']:.4f}"
        )

        # Optional refit on all data (for interpretation)
        self.model = _build_model()
        self.model.fit(
            X, y, epochs=max(1, epochs // 3), batch_size=batch_size, verbose=0
        )
        self.interpreter = InterpretationMethods(self.model)
        return cv

    def predict_and_report(self, save_dir: str = "./plots"):
        """
        Generate predictions, compute metrics, and save diagnostic plots.
        """
        import pandas as pd, numpy as np, matplotlib.pyplot as plt, json, os
        os.makedirs(save_dir, exist_ok=True)

        if self.model is None or self.data is None:
            raise ValueError("Train model first using train_model()")

        X = self.data["expression_features"]
        y_true = self.data["expression_targets"].ravel()
        y_pred = self.model.predict(X).ravel()
        genes  = np.array(self.data["gene_names"])

        pred_df = pd.DataFrame({
            "gene_id": genes,
            "true_expression": y_true,
            "predicted_expression": y_pred,
        })
        pred_df["residual"]  = pred_df["true_expression"] - pred_df["predicted_expression"]
        pred_df["abs_error"] = pred_df["residual"].abs()

        # metrics
        ss_res = np.sum((y_true - y_pred)**2)
        ss_tot = np.sum((y_true - np.mean(y_true))**2)
        r2  = 0.0 if ss_tot == 0 else 1 - ss_res/ss_tot
        mae = float(np.mean(np.abs(y_true - y_pred)))
        mse = float(np.mean((y_true - y_pred)**2))
        r   = float(np.corrcoef(y_true, y_pred)[0,1]) if np.std(y_true)>0 and np.std(y_pred)>0 else float("nan")
        metrics = {"r2": r2, "mae": mae, "mse": mse, "pearson_r": r}

        print("\n📈 Prediction Metrics:")
        for k, v in metrics.items():
            print(f"   {k:10s}: {v:.4f}")

        # save files
        pred_df.to_csv(f"{save_dir}/predictions.tsv", sep="\t", index=False)
        with open(f"{save_dir}/metrics.json", "w") as f: json.dump(metrics, f, indent=2)

        # scatter plot
        plt.figure(figsize=(5,5))
        plt.scatter(y_true, y_pred, s=8, alpha=0.6)
        lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
        plt.plot(lims, lims, 'k--', lw=1)
        plt.xlabel("True Expression")
        plt.ylabel("Predicted Expression")
        plt.title(f"Predictions (R²={r2:.3f}, r={r:.3f})")
        plt.tight_layout()
        plt.savefig(f"{save_dir}/pred_scatter.png", dpi=160)
        plt.close()

        # residuals histogram
        plt.figure(figsize=(5,4))
        plt.hist(pred_df["residual"], bins=40)
        plt.xlabel("Residual (True - Predicted)")
        plt.ylabel("Count")
        plt.title("Residual Distribution")
        plt.tight_layout()
        plt.savefig(f"{save_dir}/residuals_hist.png", dpi=160)
        plt.close()

        # Top mispredicted genes
        pred_df.sort_values("abs_error", ascending=False).head(50)\
               .to_csv(f"{save_dir}/top_miss_genes.tsv", sep="\t", index=False)

        print(f"\n✅ Saved prediction report and plots in: {save_dir}")
        return metrics

    def interpret(self, method: str = "bpnet", n_genes: int = 5, **kwargs) -> Dict:
        """Interpret model predictions"""
        if self.interpreter is None:
            raise ValueError("Train model first using train_model()")

        print(f"🔍 Running {method} interpretation on {n_genes} genes...")

        n_genes = min(n_genes, len(self.data["gene_names"]))
        features = self.data["expression_features"][:n_genes]

        if method == "bpnet":
            importance = self.interpreter.bpnet_contribution_scores(features)
        elif method == "saliency":
            importance = self.interpreter.saliency_gradients(features)
        elif method == "integrated_gradients":
            steps = kwargs.get("steps", 50)
            importance = self.interpreter.integrated_gradients_scores(
                features, steps=steps
            )
        else:
            importance = self.interpreter.standard_gradients(features)

        results = {
            "method": method,
            "feature_importance": importance,
            "gene_names": self.data["gene_names"][:n_genes],
            "sample_names": self.data["sample_names"],
            "predictions": self.model.predict(features),
        }

        print(f"✅ {method.title()} interpretation completed")
        return results

    def visualize(
        self, results: Dict, gene_idx: int = 0, save_dir: Optional[str] = None
    ):
        """Create visualizations for interpretation results"""
        print("📊 Creating visualizations...")

        self.visualizer.plot_contribution_profile(
            results["feature_importance"][gene_idx],
            results["gene_names"][gene_idx],
            results["sample_names"],
            results["method"].replace("_", " ").title(),
            save_path=f"{save_dir}/{results['gene_names'][gene_idx]}_{results['method']}.png"
            if save_dir
            else None,
        )

        self.visualizer.plot_contribution_heatmap(
            results["feature_importance"],
            results["gene_names"],
            results["sample_names"],
            results["method"].replace("_", " ").title(),
            save_path=f"{save_dir}/heatmap_{results['method']}.png"
            if save_dir
            else None,
        )

        print("✅ Visualizations created")

    def compare_methods(self, methods: List[str] = None, n_genes: int = 3) -> Dict:
        """Compare multiple interpretation methods"""
        if methods is None:
            methods = ["bpnet", "saliency", "integrated_gradients"]

        print(f"🔬 Comparing {len(methods)} interpretation methods...")

        results = {}
        for method in methods:
            results[method] = self.interpret(method, n_genes=n_genes)

        return results

    def predict(self, expression_features: Optional[np.ndarray] = None) -> np.ndarray:
        """Make predictions on expression data"""
        if self.model is None:
            raise ValueError("Train model first")

        if expression_features is None:
            expression_features = self.data["expression_features"]

        return self.model.predict(expression_features)

    def save_pipeline(self, filepath: str):
        """Save the complete pipeline"""
        if self.model is None:
            raise ValueError("No model to save")

        self.model.save_model(f"{filepath}_model")

        import pickle

        with open(f"{filepath}_data.pkl", "wb") as f:
            pickle.dump(self.data, f)

        print(f"💾 Pipeline saved to {filepath}")

    def load_pipeline(self, filepath: str):
        """Load a saved pipeline"""
        import pickle

        with open(f"{filepath}_data.pkl", "rb") as f:
            self.data = pickle.load(f)

        n_features = self.data["preprocessing_params"]["n_features"]
        self.model = ExpressionFactorNet(input_dim=n_features)
        self.model.load_model(f"{filepath}_model")

        self.interpreter = InterpretationMethods(self.model)
        print(f"📂 Pipeline loaded from {filepath}")
