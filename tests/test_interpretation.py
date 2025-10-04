# test_interpretation.py
"""
Test suite for interpretation methods (BPNet, Saliency, Integrated Gradients).
"""

import numpy as np
from rna_seq_factornet.models.factornet import ExpressionFactorNet
from rna_seq_factornet.interpretation.methods import InterpretationMethods

def test_interpretation():
    # Synthetic input and model for testing
    model = ExpressionFactorNet(n_features=10)
    X = np.random.normal(size=(5,10))
    interpreter = InterpretationMethods(model)
    # Check method outputs
    assert interpreter.bpnet_contribution_scores(X).shape == X.shape
    assert interpreter.saliency_gradients(X).shape == X.shape
    assert interpreter.integrated_gradients_scores(X).shape == X.shape
    print("Interpretation methods passed basic test.")

if __name__ == "__main__":
    test_interpretation()
