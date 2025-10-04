# test_data_loader.py
"""
Test suite for ExpressionDataLoader and data preprocessing.
"""

import os
import pandas as pd
from rna_seq_factornet.data.loader import ExpressionDataLoader
from rna_seq_factornet.data.preprocessor import preprocess_for_factornet

def test_loader_and_preprocessor():
    example_file = "example_expression_data.csv"
    loader = ExpressionDataLoader()
    df = loader.load_expression_data(example_file)
    assert isinstance(df, pd.DataFrame)
    output = preprocess_for_factornet(df)
    assert "expression_features" in output and "gene_names" in output
    print("Data loader and preprocessor passed basic test.")

if __name__ == "__main__":
    test_loader_and_preprocessor()
