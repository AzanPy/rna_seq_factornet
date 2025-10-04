"""
Analysis Utilities for RNA-seq FactorNet

Provides functions for batch analysis, summary statistics, and report generation.
"""

import os
import pandas as pd
from rna_seq_factornet.pipeline.core import ExpressionPipeline

def batch_run(
    file_list,
    output_dir="./batch_results",
    use_cv=True,
    n_genes=5,
    interpret_method="bpnet"
):
    """
    Run complete pipeline (train + interpret) on a list of data files.
    Saves summary results for each file to output_dir.

    Args:
        file_list: list of file paths (CSV/TSV/Excel) for expression data.
        output_dir: directory to store results and summaries.
        use_cv: run training with cross-validation.
        n_genes: top genes to interpret.
        interpret_method: interpretability method to use.

    Returns:
        summary_table (pd.DataFrame): one row per file with key performance and output info.
    """
    os.makedirs(output_dir, exist_ok=True)
    records = []
    for i, file in enumerate(file_list):
        print(f"\n=== Processing file {i+1}/{len(file_list)}: {file} ===")
        try:
            pipeline = ExpressionPipeline()
            pipeline.load_data(file)
            stats = pipeline.train_model(use_cv=use_cv)
            results = pipeline.interpret(interpret_method, n_genes=n_genes)
            pipeline.visualize(results, save_dir=output_dir)
            # Save predictions for inspection
            pred_df = pd.DataFrame(
                results['predictions'],
                index=results['gene_names'],
                columns=["prediction"]
            )
            pred_fname = os.path.join(output_dir, f"predictions_{os.path.basename(file)}.csv")
            pred_df.to_csv(pred_fname)
            rec = dict(
                file=file,
                r2=stats.get("mean_r2", "NA"),
                n_genes=n_genes,
                interpret_method=interpret_method,
                pred_file=pred_fname
            )
            records.append(rec)
        except Exception as e:
            print(f"Error processing {file}: {e}")
            records.append(dict(file=file, r2="ERROR", n_genes=n_genes, interpret_method=interpret_method, pred_file=""))
    summary = pd.DataFrame(records)
    summary_name = os.path.join(output_dir, "batch_summary.csv")
    summary.to_csv(summary_name, index=False)
    print(f"\nBatch analysis completed. Summary written to: {summary_name}")
    return summary

def summarize_model_results(results, stats=None, n=5):
    """
    Print summary statistics and preview top model outputs.

    Args:
        results: interpretation results from pipeline.interpret()
        stats: dictionary from training (optional)
        n: genes to show
    """
    if stats:
        print("----- Model Training Performance -----")
        for k, v in stats.items():
            print(f"{k}: {v}")
    print("\n----- Predictions Preview -----")
    for gene, pred in zip(results["gene_names"][:n], results["predictions"][:n]):
        print(f"Gene: {gene} | Predicted: {pred}")

if __name__ == "__main__":
    # Demo: batch process multiple example datasets (modify for your own files)
    files = ["example_expression_data.csv"]  # or glob for multiple datasets
    batch_run(files, output_dir="./analysis_batch_demo")
