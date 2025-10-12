"""
Data Loader for RNA-seq Expression Analysis
Supports CSV, TSV, TXT, and Excel formats with flexible NaN and formatting options.
Adds:
- gene_col/header_row support
- numeric-only coercion
- 'gene_id' index auto-detection
- bridge to preprocessor for pipeline compatibility
"""

import pandas as pd
from pathlib import Path
from .preprocessor import preprocess_for_factornet as _preprocess


class ExpressionDataLoader:
    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def load_expression_data(
        self,
        filepath,
        delimiter: str | None = None,
        sheet_name: int | str = 0,
        nan_strategy: str = "remove",
        gene_col: int | str | None = None,
        header_row: int = 0,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Load an expression matrix from CSV/TSV/TXT/Excel.

        Parameters
        ----------
        filepath : str | Path
            Path to the data file.
        delimiter : str | None
            Field delimiter for CSV/TSV/TXT (auto-detected if None).
        sheet_name : int | str
            Excel sheet name or index (only used for Excel files).
        nan_strategy : {'remove','fill_zero','fill_mean','fill_median'}
            How to handle NaNs.
        gene_col : int | str | None
            Column (index or name) containing gene IDs. If None and a 'gene_id'
            column exists, that column is used. Otherwise the first column is used.
        header_row : int
            Header row index for the input file.
        **kwargs :
            Extra kwargs passed to pandas readers (e.g., dtype, encoding, etc.).

        Returns
        -------
        pd.DataFrame
            DataFrame indexed by gene IDs with numeric sample columns.
        """
        path_str = str(filepath)
        lower = path_str.lower()

        # Auto-select delimiter for text formats
        if delimiter is None:
            if lower.endswith(".tsv") or lower.endswith(".txt"):
                delimiter = "\t"
            elif lower.endswith(".csv"):
                delimiter = ","
            else:
                delimiter = ","  # sensible default

        # Read file
        if lower.endswith((".xls", ".xlsx", ".xlsm", ".xlsb")):
            df = pd.read_excel(filepath, sheet_name=sheet_name, header=header_row)
        else:
            df = pd.read_csv(filepath, delimiter=delimiter, header=header_row, **kwargs)

        # Decide index column for gene IDs
        # Priority: explicit gene_col > 'gene_id' column > first column
        if gene_col is not None:
            df = df.set_index(gene_col)
        elif "gene_id" in df.columns:
            df = df.set_index("gene_id")
        else:
            df = df.set_index(df.columns[0])

        # Clean names and coerce to numeric
        df.index = df.index.astype(str).str.strip()
        df.columns = [str(c).strip() for c in df.columns]
        df = df.apply(pd.to_numeric, errors="coerce")

        # NaN handling
        if nan_strategy == "remove":
            df = df.dropna(axis=0, how="any")
        elif nan_strategy == "fill_zero":
            df = df.fillna(0)
        elif nan_strategy == "fill_mean":
            df = df.fillna(df.mean(numeric_only=True))
        elif nan_strategy == "fill_median":
            df = df.fillna(df.median(numeric_only=True))
        else:
            raise ValueError(f"Unsupported nan_strategy: {nan_strategy}")

        return df

    # Bridge so pipeline can call loader.preprocess_for_factornet(...)
    # and keep all preprocessing logic in the preprocessor module.
    def preprocess_for_factornet(self, df: pd.DataFrame, **kwargs):
        return _preprocess(df, **kwargs)
