"""
Data Preprocessing Utilities for RNA-seq Expression Analysis
Handles normalization, feature selection, and conversion for model training.
"""

import numpy as np

def preprocess_for_factornet(df, min_expression=0.5, feature_selection='variance', top_n=None):
    # Remove genes with very low mean expression
    gene_means = df.mean(axis=1)
    filtered_df = df[gene_means >= min_expression]

    # Optionally select most variable/top genes
    if feature_selection == 'variance':
        gene_vars = filtered_df.var(axis=1)
        ordered = gene_vars.sort_values(ascending=False)
        if top_n:
            filtered_df = filtered_df.loc[ordered.index[:top_n]]
    elif feature_selection == 'mean':
        ordered = filtered_df.mean(axis=1).sort_values(ascending=False)
        if top_n:
            filtered_df = filtered_df.loc[ordered.index[:top_n]]

    # Normalize per sample (z-score)
    norm_data = (filtered_df - filtered_df.mean(axis=1, keepdims=True)) / filtered_df.std(axis=1, keepdims=True)
    norm_data = norm_data.fillna(0)

    # Package output for model
    output = {
        'expression_features': norm_data.values,
        'expression_targets': filtered_df.mean(axis=1).values,
        'gene_names': list(filtered_df.index),
        'sample_names': list(filtered_df.columns),
        'normalized_data': norm_data,
        'preprocessing_params': {
            'min_expression': min_expression,
            'feature_selection': feature_selection,
            'n_features': norm_data.shape[1],
            'n_genes': norm_data.shape[0]
        }
    }
    return output
