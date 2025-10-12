# rna_seq_factornet/__init__.py

"""
RNA-seq FactorNet — simple entrypoint.

Usage:
    from rna_seq_factornet import ExpressionPipeline
"""

from .pipeline.core import ExpressionPipeline

__all__ = ["ExpressionPipeline"]
__version__ = "1.0.0"
__author__ = "Azan"