# test_model.py
"""
Test suite for core model training and prediction.
"""

import numpy as np
from rna_seq_factornet.models.factornet import ExpressionFactorNet

def test_model_training_and_prediction():
    X = np.random.normal(size=(20,10))
    y = np.random.normal(size=20)
    model = ExpressionFactorNet(n_features=10)
    model.train(X, y, epochs=2)
    preds = model.predict(X)
    assert preds.shape == y.shape
    print("Model training and prediction passed basic test.")

if __name__ == "__main__":
    test_model_training_and_prediction()
