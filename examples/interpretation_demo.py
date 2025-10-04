"""
Interpretation Demo for RNA-seq FactorNet

Demonstrates how to use all key interpretability methods (BPNet, Saliency Maps, Integrated Gradients, Standard Gradients)
on real or synthetic RNA-seq data. Results are compared and visualized for easy understanding.
"""

from rna_seq_factornet import ExpressionPipeline, quick_analysis, load_example_data

def run_demo(expression_file=None):
    print("=== RNA-seq FactorNet Interpretation Demo ===")
    # Use synthetic data if none provided
    if expression_file is None:
        expression_file = load_example_data()
        print(f"Using synthetic example dataset: {expression_file}")

    # Build pipeline and train
    pipeline = ExpressionPipeline()
    pipeline.load_data(expression_file)
    pipeline.train_model()

    # Interpret with all main methods
    methods = ['bpnet', 'saliency', 'integrated_gradients', 'gradients']
    num_genes = 5

    print("\n--- Feature Attribution Methods ---")
    for method in methods:
        print(f"\nInterpreting with {method}...")
        results = pipeline.interpret(method, n_genes=num_genes)
        print(f"Feature importance shape: {results['feature_importance'].shape}")
        pipeline.visualize(results)

    # Compare all methods
    print("\n--- Method Comparison ---")
    comparison = pipeline.compare_methods(methods, n_genes=num_genes)
    for method, results in comparison.items():
        print(f"\nMethod: {method}")
        print(f"  Feature importance: {results['feature_importance'].shape}")

if __name__ == "__main__":
    # Run with no arguments for a complete demo with synthetic data
    run_demo()
