"""
Data Preprocessing Utilities for RNA-seq Expression Analysis
Handles normalization, feature selection, and conversion for model training.
"""

import numpy as np
import pandas as pd

def preprocess_for_factornet(
    df: "pd.DataFrame",
    min_expression: float = 0.5,
    feature_selection: str = "variance",  # {'variance','mean','all'}
    top_n: int | None = None,
):
    # 1) Filter low-expression genes (numeric-only to avoid string issues)
    gene_means = df.mean(axis=1, numeric_only=True)
    filtered_df = df.loc[gene_means >= min_expression]

    # 2) Optional feature selection
    if feature_selection == "variance":
        ordered = filtered_df.var(axis=1, numeric_only=True).sort_values(ascending=False)
        if top_n is not None:
            filtered_df = filtered_df.loc[ordered.index[:top_n]]
    elif feature_selection == "mean":
        ordered = filtered_df.mean(axis=1, numeric_only=True).sort_values(ascending=False)
        if top_n is not None:
            filtered_df = filtered_df.loc[ordered.index[:top_n]]
    elif feature_selection == "all":
        # Keep all genes; if top_n is set, pick top_n by variance
        if top_n is not None:
            ordered = filtered_df.var(axis=1, numeric_only=True).sort_values(ascending=False)
            filtered_df = filtered_df.loc[ordered.index[:top_n]]
    else:
        raise ValueError(f"Unsupported feature_selection: {feature_selection}")

    # 3) Row-wise (gene-wise) z-score with zero-variance guard (no keepdims)
    row_mean = filtered_df.mean(axis=1, numeric_only=True)
    row_std  = filtered_df.std(axis=1, numeric_only=True).replace(0, np.nan)
    norm_data = filtered_df.sub(row_mean, axis=0).div(row_std, axis=0).fillna(0.0)

    # 4) Package output for model
    output = {
        "expression_features": norm_data.values,
        "expression_targets": filtered_df.mean(axis=1, numeric_only=True).values,
        "gene_names": list(filtered_df.index),
        "sample_names": list(filtered_df.columns),
        "normalized_data": norm_data,
        "preprocessing_params": {
            "min_expression": min_expression,
            "feature_selection": feature_selection,
            "n_features": int(norm_data.shape[1]),
            "n_genes": int(norm_data.shape[0]),
        },
    }
    return output
