"""
Interpretation Methods for RNA-seq FactorNet

Implements BPNet-style contributions, Saliency Maps, Integrated Gradients, and basic gradients
for attribution analysis on neural network models.
"""

import numpy as np

class InterpretationMethods:
    def __init__(self, model):
        self.model = model

    def bpnet_contribution_scores(self, X):
        """
        Gradient × Input scores (BPNet-style contribution).
        Returns the elementwise product of model gradients and the input.
        """
        gradients = self._get_gradients(X)
        importance = gradients * X
        return importance

    def saliency_gradients(self, X):
        """
        Returns absolute model gradients as feature importance.
        """
        gradients = self._get_gradients(X)
        importance = np.abs(gradients)
        return importance

    def standard_gradients(self, X):
        """
        Returns raw model gradients (signed attribution).
        """
        return self._get_gradients(X)

    def integrated_gradients_scores(self, X, baseline=None, steps=50):
        """
        Integrated Gradients: Attribute by integrating gradients from baseline to input.
        Ideal for high-confidence feature attribution.
        """
        if baseline is None:
            baseline = np.zeros_like(X)
        scaled_inputs = [baseline + (float(i)/steps) * (X - baseline) for i in range(steps+1)]
        grads = np.array([self._get_gradients(si) for si in scaled_inputs])
        avg_grads = np.mean(grads, axis=0)
        ig = (X - baseline) * avg_grads
        return ig

    def _get_gradients(self, X):
        """
        Utility: Compute gradients of model's output with respect to input X.
        This should work for Keras/TensorFlow, PyTorch, or a custom backend;
        here it is abstracted, you should adapt to your model's framework.
        """
        # Example stub for Keras/TensorFlow models
        if hasattr(self.model, "compute_gradients"):
            return self.model.compute_gradients(X)
        else:
            # You must implement this for your backend!
            raise NotImplementedError("Gradient computation not implemented for this model.")

# High-level function interface (optional convenience)
def BPNetContributions(model, X):
    return InterpretationMethods(model).bpnet_contribution_scores(X)

def SaliencyMethods(model, X):
    return InterpretationMethods(model).saliency_gradients(X)

def IntegratedGradients(model, X, baseline=None, steps=50):
    return InterpretationMethods(model).integrated_gradients_scores(X, baseline=baseline, steps=steps)
