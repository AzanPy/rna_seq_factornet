# RNA-seq FactorNet API Reference

## Main Pipeline

- **ExpressionPipeline**
  - `load_data(filepath, ...)`
  - `train_model(...)`
  - `interpret(method, ...)`
  - `visualize(results, ...)`
  - `compare_methods(methods, ...)`
  - `save_pipeline(filepath)`
  - `load_pipeline(filepath)`

## Modules

- **rna_seq_factornet.data**
  - `ExpressionDataLoader`
  - `preprocess_for_factornet`

- **rna_seq_factornet.models**
  - `ExpressionFactorNet`

- **rna_seq_factornet.interpretation**
  - `InterpretationMethods`
  - `BPNetContributions`
  - `SaliencyMethods`
  - `IntegratedGradients`

## Utilities

- `quick_analysis(data_file, ...)`
- `load_example_data()`
- **metrics:** MSE, MAE, RMSE, R², Pearson correlation, etc.

---

Refer to code comments and docstrings for details on each method/class.
