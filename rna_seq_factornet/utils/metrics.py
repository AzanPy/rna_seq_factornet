"""
Metrics for RNA-seq FactorNet Expression Prediction

Includes regression, correlation, and error metrics to evaluate model performance.
"""

import numpy as np

def mean_squared_error(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean((y_true - y_pred) ** 2)

def root_mean_squared_error(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

def mean_absolute_error(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean(np.abs(y_true - y_pred))

def median_absolute_error(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.median(np.abs(y_true - y_pred))

def r_squared(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

def explained_variance(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return 1 - np.var(y_true - y_pred) / np.var(y_true) if np.var(y_true) != 0 else 0

def mean_absolute_percentage_error(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    mask = y_true != 0
    if np.sum(mask) == 0:
        return np.nan
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def pearson_correlation(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    if len(y_true) < 2:
        return np.nan
    return np.corrcoef(y_true, y_pred)[0,1]


# Optionally add a summary function that reports all metrics at once
def regression_summary(y_true, y_pred):
    return {
        "MSE": mean_squared_error(y_true, y_pred),
        "RMSE": root_mean_squared_error(y_true, y_pred),
        "MAE": mean_absolute_error(y_true, y_pred),
        "MedianAE": median_absolute_error(y_true, y_pred),
        "R^2": r_squared(y_true, y_pred),
        "ExplainedVariance": explained_variance(y_true, y_pred),
        "MAPE": mean_absolute_percentage_error(y_true, y_pred),
        "PearsonCorr": pearson_correlation(y_true, y_pred),
    }
