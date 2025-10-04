"""
Data Loader for RNA-seq Expression Analysis
Supports CSV, TSV, TXT, and Excel formats with flexible NaN and formatting options.
"""

import pandas as pd
from pathlib import Path

class ExpressionDataLoader:
    def __init__(self, cache_dir="./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def load_expression_data(self, filepath, delimiter=None, sheet_name=0, nan_strategy='remove', **kwargs):
        ext = str(filepath).lower()
        
        # Auto-select delimiter if not provided
        if delimiter is None:
            if ext.endswith('.tsv'):
                delimiter = '\t'
            elif ext.endswith('.csv'):
                delimiter = ','
            elif ext.endswith('.txt'):
                delimiter = '\t'
            else:
                delimiter = ','

        # Read file
        if ext.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(filepath, sheet_name=sheet_name)
        else:
            df = pd.read_csv(filepath, delimiter=delimiter, **kwargs)
        
        # Clean column/row names if needed
        df.columns = [str(c).strip() for c in df.columns]
        df.index = df.index.map(str)
        
        # NaN cleaning strategy
        if nan_strategy == 'remove':
            df = df.dropna()
        elif nan_strategy == 'fill_zero':
            df = df.fillna(0)
        elif nan_strategy == 'fill_mean':
            df = df.fillna(df.mean())
        elif nan_strategy == 'fill_median':
            df = df.fillna(df.median())
        
        return df
