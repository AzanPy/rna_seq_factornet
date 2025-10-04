"""
Validation metrics for RNA-seq FactorNet

Includes functions for evaluating model performance on regression tasks.
"""

import numpy as np

def mean_squared_error(y_true, y_pred):
    """Compute Mean Squared Error (MSE)."""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean((y_true - y_pred) ** 2)

def mean_absolute_error(y_true, y_pred):
    """Compute Mean Absolute Error (MAE)."""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean(np.abs(y_true - y_pred))

def r_squared(y_true, y_pred):
    """Compute Coefficient of Determination (R²)."""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)

def explained_variance(y_true, y_pred):
    """Compute explained variance score"""
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return 1 - np.var(y_true - y_pred) / np.var(y_true)

# Additional custom validation metrics can be added here as needed

if __name__ == "__main__":
    # Simple test example
    y_true = [3.0, -0.5, 2.0, 7.0]
    y_pred = [2.5, 0.0, 2.1, 7.8]

    print("MSE:", mean_squared_error(y_true, y_pred))
    print("MAE:", mean_absolute_error(y_true, y_pred))
    print("R²:", r_squared(y_true, y_pred))
    print("Explained Variance:", explained_variance(y_true, y_pred))
