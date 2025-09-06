# rna_seq_factornet/__init__.py
"""
RNA-seq FactorNet: A Deep Learning Framework for Expression Analysis with Interpretability

A comprehensive toolkit for RNA-seq expression data analysis using modified FactorNet architecture
with advanced interpretability methods including Integrated Gradients, Saliency Maps, and 
BPNet-style contribution scores.

Simple Usage:
    ```python
    from rna_seq_factornet import ExpressionPipeline
    
    # Create pipeline and run analysis
    pipeline = ExpressionPipeline()
    pipeline.load_data('expression_data.csv')
    pipeline.train_model()
    
    # Interpret predictions
    results = pipeline.interpret('bpnet', n_genes=5)
    pipeline.visualize(results)
    ```

Advanced Usage:
    ```python
    from rna_seq_factornet.models import ExpressionFactorNet
    from rna_seq_factornet.data import ExpressionDataLoader
    from rna_seq_factornet.interpretation import SaliencyMethods
    
    # Manual control over components
    loader = ExpressionDataLoader()
    model = ExpressionFactorNet(n_features=50)
    interpreter = SaliencyMethods(model)
    ```
"""

from .pipeline.core import ExpressionPipeline
from .models.factornet import ExpressionFactorNet
from .data.loader import ExpressionDataLoader
from .interpretation.methods import (
    IntegratedGradients,
    SaliencyMethods, 
    BPNetContributions
)
from .interpretation.visualizer import InterpretabilityVisualizer

# Simple high-level API
__all__ = [
    # Main pipeline (recommended for most users)
    'ExpressionPipeline',
    
    # Core components (for advanced users)
    'ExpressionFactorNet',
    'ExpressionDataLoader',
    
    # Interpretation methods
    'IntegratedGradients',
    'SaliencyMethods',
    'BPNetContributions',
    'InterpretabilityVisualizer',
    
    # Convenience functions
    'quick_analysis',
    'load_example_data'
]

# Version information
__version__ = "1.0.0"
__author__ = "ML Utility Generator"
__email__ = "your.email@example.com"
__description__ = "RNA-seq expression analysis with deep learning and interpretability"

def quick_analysis(data_file, method='bpnet', n_genes=5, save_plots=True):
    """
    Quick analysis function for immediate results
    
    Args:
        data_file: Path to expression data file
        method: Interpretation method ('bpnet', 'saliency', 'integrated_gradients')
        n_genes: Number of genes to analyze
        save_plots: Whether to save visualization plots
        
    Returns:
        Tuple of (pipeline, interpretation_results)
    """
    pipeline = ExpressionPipeline()
    pipeline.load_data(data_file)
    pipeline.train_model()
    results = pipeline.interpret(method, n_genes=n_genes)
    
    if save_plots:
        pipeline.visualize(results)
    
    return pipeline, results

def load_example_data():
    """
    Load example synthetic data for testing
    
    Returns:
        Path to example data file
    """
    import numpy as np
    import pandas as pd
    
    # Generate example data
    np.random.seed(42)
    n_genes, n_samples = 100, 20
    
    gene_names = [f"Gene_{i:03d}" for i in range(n_genes)]
    sample_names = [f"Sample_{i:02d}" for i in range(n_samples)]
    
    # Log-normal expression data
    data = np.random.lognormal(2, 1, (n_genes, n_samples))
    df = pd.DataFrame(data, index=gene_names, columns=sample_names)
    
    example_file = "example_expression_data.csv"
    df.to_csv(example_file)
    
    return example_file