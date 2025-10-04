# rna_seq_factornet/pipeline/core.py
"""
Main pipeline for RNA-seq expression analysis with simple, clean API
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, Union, List

from ..data.loader import ExpressionDataLoader
from ..models.factornet import ExpressionFactorNet
from ..interpretation.methods import InterpretationMethods
from ..interpretation.visualizer import InterpretabilityVisualizer

class ExpressionPipeline:
    """
    Simple, user-friendly pipeline for RNA-seq expression analysis
    
    Example:
        ```python
        pipeline = ExpressionPipeline()
        pipeline.load_data('expression.csv')
        pipeline.train_model()
        results = pipeline.interpret('bpnet', n_genes=5)
        pipeline.visualize(results)
        ```
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
    
    def load_data(self, filepath: str, 
                  nan_strategy: str = 'remove',
                  min_expression: float = 0.5,
                  feature_selection: str = 'variance',
                  **kwargs) -> Dict:
        """
        Load and preprocess expression data
        
        Args:
            filepath: Path to expression data file
            nan_strategy: How to handle NaN values ('remove', 'fill_zero', 'fill_mean', 'fill_median')
            min_expression: Minimum expression threshold
            feature_selection: Feature selection method ('variance', 'mean', 'all')
            **kwargs: Additional arguments for data loading
            
        Returns:
            Processed data dictionary
        """
        print(f"📊 Loading data from {filepath}...")
        
        # Load raw data
        raw_data = self.loader.load_expression_data(
            filepath, 
            nan_strategy=nan_strategy,
            **kwargs
        )
        
        # Preprocess
        self.data = self.loader.preprocess_for_factornet(
            raw_data,
            min_expression=min_expression,
            feature_selection=feature_selection
        )
        
        print(f"✅ Data loaded: {len(self.data['gene_names'])} genes, "
              f"{self.data['preprocessing_params']['n_features']} samples")
        
        return self.data
    
    def train_model(self, 
                   use_cv: bool = True,
                   k_folds: int = 5,
                   epochs: int = 50,
                   **model_params) -> Dict:
        """
        Train the FactorNet model
        
        Args:
            use_cv: Whether to use cross-validation
            k_folds: Number of CV folds
            epochs: Number of training epochs
            **model_params: Model architecture parameters
            
        Returns:
            Training results
        """
        if self.data is None:
            raise ValueError("Load data first using load_data()")
        
        print("🤖 Training FactorNet model...")
        
        # Initialize model
        n_features = self.data['preprocessing_params']['n_features']
        
        # Set default small model for speed
        default_params = {
            'conv_filters': 32,
            'lstm_units': 32,
            'dense_units': 64,
            'batch_size': 16
        }
        default_params.update(model_params)
        
        self.model = ExpressionFactorNet(n_features=n_features, **{
            k: v for k, v in default_params.items() 
            if k in ['conv_filters', 'conv_kernel_size', 'lstm_units', 'dense_units', 'dropout_rate']
        })
        
        # Train
        X = self.data['expression_features']
        y = self.data['expression_targets']
        
        if use_cv:
            results = self.model.train_with_cv(
                X, y, k_folds=k_folds, epochs=epochs,
                batch_size=default_params.get('batch_size', 16)
            )
            print(f"✅ CV completed: R² = {results['mean_r2']:.3f} ± {results['std_r2']:.3f}")
        else:
            results = self.model.train(
                X, y, epochs=epochs, 
                batch_size=default_params.get('batch_size', 16)
            )
            print("✅ Training completed")
        
        # Initialize interpreter
        self.interpreter = InterpretationMethods(self.model)
        
        return results
    
    def interpret(self, method: str = 'bpnet', n_genes: int = 5, **kwargs) -> Dict:
        """
        Interpret model predictions
        
        Args:
            method: Interpretation method ('bpnet', 'saliency', 'integrated_gradients', 'gradients')
            n_genes: Number of genes to analyze
            **kwargs: Method-specific parameters
            
        Returns:
            Interpretation results
        """
        if self.interpreter is None:
            raise ValueError("Train model first using train_model()")
        
        print(f"🔍 Running {method} interpretation on {n_genes} genes...")
        
        # Select genes
        n_genes = min(n_genes, len(self.data['gene_names']))
        features = self.data['expression_features'][:n_genes]
        
        # Run interpretation
        if method == 'bpnet':
            importance = self.interpreter.bpnet_contribution_scores(features)
        elif method == 'saliency':
            importance = self.interpreter.saliency_gradients(features)
        elif method == 'integrated_gradients':
            steps = kwargs.get('steps', 50)
            importance = self.interpreter.integrated_gradients_scores(features, steps=steps)
        else:  # gradients
            importance = self.interpreter.standard_gradients(features)
        
        results = {
            'method': method,
            'feature_importance': importance,
            'gene_names': self.data['gene_names'][:n_genes],
            'sample_names': self.data['sample_names'],
            'predictions': self.model.predict(features)
        }
        
        print(f"✅ {method.title()} interpretation completed")
        return results
    
    def visualize(self, results: Dict, gene_idx: int = 0, save_dir: Optional[str] = None):
        """
        Create visualizations for interpretation results
        
        Args:
            results: Results from interpret()
            gene_idx: Index of gene to visualize
            save_dir: Directory to save plots
        """
        print("📊 Creating visualizations...")
        
        # Individual gene plot
        self.visualizer.plot_contribution_profile(
            results['feature_importance'][gene_idx],
            results['gene_names'][gene_idx],
            results['sample_names'],
            results['method'].replace('_', ' ').title(),
            save_path=f"{save_dir}/{results['gene_names'][gene_idx]}_{results['method']}.png" if save_dir else None
        )
        
        # Heatmap for all genes
        self.visualizer.plot_contribution_heatmap(
            results['feature_importance'],
            results['gene_names'],
            results['sample_names'],
            results['method'].replace('_', ' ').title(),
            save_path=f"{save_dir}/heatmap_{results['method']}.png" if save_dir else None
        )
        
        print("✅ Visualizations created")
    
    def compare_methods(self, methods: List[str] = None, n_genes: int = 3) -> Dict:
        """
        Compare multiple interpretation methods
        
        Args:
            methods: List of methods to compare
            n_genes: Number of genes to analyze
            
        Returns:
            Dictionary with results for each method
        """
        if methods is None:
            methods = ['bpnet', 'saliency', 'integrated_gradients']
        
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
            expression_features = self.data['expression_features']
        
        return self.model.predict(expression_features)
    
    def save_pipeline(self, filepath: str):
        """Save the complete pipeline"""
        if self.model is None:
            raise ValueError("No model to save")
        
        # Save model
        self.model.save_model(f"{filepath}_model")
        
        # Save data
        import pickle
        with open(f"{filepath}_data.pkl", 'wb') as f:
            pickle.dump(self.data, f)
        
        print(f"💾 Pipeline saved to {filepath}")
    
    def load_pipeline(self, filepath: str):
        """Load a saved pipeline"""
        # Load data
        import pickle
        with open(f"{filepath}_data.pkl", 'rb') as f:
            self.data = pickle.load(f)
        
        # Load model
        n_features = self.data['preprocessing_params']['n_features']
        self.model = ExpressionFactorNet(n_features=n_features)
        self.model.load_model(f"{filepath}_model")
        
        # Initialize interpreter
        self.interpreter = InterpretationMethods(self.model)
        
        print(f"📂 Pipeline loaded from {filepath}")