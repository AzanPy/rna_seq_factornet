# Getting Started with RNA-seq FactorNet

## 1. Installation

- Install dependencies using `pip install -r requirements.txt`
- Clone/download the repository
- Ensure your data files are accessible

## 2. Example Usage

from rna_seq_factornet import ExpressionPipeline

pipeline = ExpressionPipeline()
pipeline.load_data("your_data.csv")
pipeline.train_model()
results = pipeline.interpret('bpnet', n_genes=5)
pipeline.visualize(results)


## 3. Running Demos

- See `examples/interpretation_demo.py` for a full pipeline example
- For advanced analysis, use `examples/advanced_analysis.py`

## 4. Data Format

- Input: Genes as rows, samples as columns (CSV, TSV, Excel)

## 5. Support

- For issues, visit the GitHub repository page.
