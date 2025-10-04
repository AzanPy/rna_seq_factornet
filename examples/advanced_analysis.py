"""
Advanced RNA-seq FactorNet Analysis Example

Demonstrates custom data loading, hyperparameter tuning, robust NaN handling,
cross-validation, and multiple interpretation methods on real or synthetic data.
"""

from rna_seq_factornet import ExpressionPipeline, load_example_data

def run_advanced_analysis(expression_file=None):
    print("\n=== Advanced RNA-seq FactorNet Analysis ===")

    # Use user data if available, else fallback to synthetic test data
    if expression_file is None:
        expression_file = load_example_data()
        print(f"Using synthetic example data: {expression_file}")

    # --- Step 1: Load data with custom preprocessing options ---
    pipeline = ExpressionPipeline()
    pipeline.load_data(
        expression_file,
        nan_strategy='fill_mean',           # Fill NaNs with gene mean
        min_expression=1.0,                 # Only keep genes with mean expression > 1
        feature_selection='variance'        # Top variable genes for analysis
    )

    # --- Step 2: Train model with custom settings and cross-validation ---
    pipeline.train_model(
        use_cv=True,
        k_folds=5,                         # 5-fold cross-validation
        epochs=40,                         # Fewer epochs for quicker runs
        conv_filters=64,                   # Larger convolution filters
        lstm_units=64,                     # More LSTM units
        dense_units=128,                   # Wide dense layer
        batch_size=32,                     # Larger batches
        dropout_rate=0.4                   # Increased dropout for regularization
    )

    # --- Step 3: Interpret with Integrated Gradients and more steps ---
    print("\n--- Integrated Gradients Interpretation ---")
    ig_results = pipeline.interpret(
        'integrated_gradients',
        n_genes=8,
        steps=100                          # More steps for attribution
    )
    pipeline.visualize(ig_results, save_dir="./advanced_results")

    # --- Step 4: Interpret with BPNet and Saliency ---
    print("\n--- BPNet Interpretation ---")
    bpnet_results = pipeline.interpret('bpnet', n_genes=8)
    pipeline.visualize(bpnet_results, save_dir="./advanced_results")

    print("\n--- Saliency Maps Interpretation ---")
    saliency_results = pipeline.interpret('saliency', n_genes=8)
    pipeline.visualize(saliency_results, save_dir="./advanced_results")

    # --- Step 5: Compare all methods ---
    print("\n--- Comparing Multiple Methods ---")
    comparison = pipeline.compare_methods(
        methods=['bpnet', 'saliency', 'integrated_gradients'],
        n_genes=8
    )
    pipeline.visualizer.plot_method_comparison(comparison, gene_idx=0, save_dir="./advanced_results")

    print("\n--- Advanced analysis complete! ---")

if __name__ == "__main__":
    # Run analysis (leave expression_file=None to use synthetic data)
    run_advanced_analysis()
