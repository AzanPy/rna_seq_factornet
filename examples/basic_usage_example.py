# examples/basic_usage.py
"""
Basic Usage Examples for RNA-seq FactorNet

This example shows the simplest way to use the RNA-seq FactorNet package
for expression analysis and interpretation.
"""

# =============================================================================
# EXAMPLE 1: Simple 3-line analysis
# =============================================================================

from rna_seq_factornet import ExpressionPipeline

# Create pipeline and analyze
pipeline = ExpressionPipeline()
pipeline.load_data('your_expression_data.csv')
pipeline.train_model()

# Interpret with BPNet method
results = pipeline.interpret('bpnet', n_genes=5)
pipeline.visualize(results)


# =============================================================================
# EXAMPLE 2: Quick one-liner analysis
# =============================================================================

from rna_seq_factornet import quick_analysis

# Everything in one function call
pipeline, results = quick_analysis(
    'your_expression_data.csv', 
    method='bpnet', 
    n_genes=5
)


# =============================================================================
# EXAMPLE 3: Working with example data
# =============================================================================

from rna_seq_factornet import load_example_data, ExpressionPipeline

# Load synthetic example data
example_file = load_example_data()
print(f"Example data created: {example_file}")

# Run analysis
pipeline = ExpressionPipeline()
pipeline.load_data(example_file)
pipeline.train_model()

# Try different interpretation methods
bpnet_results = pipeline.interpret('bpnet', n_genes=3)
saliency_results = pipeline.interpret('saliency', n_genes=3)

# Compare methods
comparison = pipeline.compare_methods(['bpnet', 'saliency'], n_genes=3)


# =============================================================================
# EXAMPLE 4: Custom parameters
# =============================================================================

from rna_seq_factornet import ExpressionPipeline

pipeline = ExpressionPipeline()

# Load data with custom preprocessing
pipeline.load_data(
    'expression_data.csv',
    nan_strategy='fill_mean',          # Handle missing values
    min_expression=1.0,                # Higher expression threshold
    feature_selection='variance'       # Select most variable genes
)

# Train with custom model parameters
pipeline.train_model(
    use_cv=True,                      # Use cross-validation
    k_folds=5,                        # 5-fold CV
    epochs=30,                        # Fewer epochs for speed
    conv_filters=64,                  # Larger model
    lstm_units=64,
    batch_size=32
)

# Interpret with custom parameters
results = pipeline.interpret(
    'integrated_gradients', 
    n_genes=10,
    steps=100                         # More integration steps
)

# Visualize and save plots
pipeline.visualize(results, save_dir='./my_plots')


# =============================================================================
# EXAMPLE 5: Different data formats
# =============================================================================

from rna_seq_factornet import ExpressionPipeline

pipeline = ExpressionPipeline()

# CSV file
pipeline.load_data('data.csv')

# TSV file  
pipeline.load_data('data.tsv', delimiter='\t')

# Excel file
pipeline.load_data('data.xlsx', sheet_name='Expression')

# Custom column/row setup
pipeline.load_data(
    'data.csv',
    gene_col=0,                       # First column has gene names
    header_row=0                      # First row has sample names
)


# =============================================================================
# EXAMPLE 6: Save and load pipeline
# =============================================================================

from rna_seq_factornet import ExpressionPipeline

# Train and save
pipeline = ExpressionPipeline()
pipeline.load_data('expression_data.csv')
pipeline.train_model()
pipeline.save_pipeline('my_trained_model')

# Load later
new_pipeline = ExpressionPipeline()
new_pipeline.load_pipeline('my_trained_model')

# Use loaded model
results = new_pipeline.interpret('bpnet', n_genes=5)


# =============================================================================
# EXAMPLE 7: Error handling
# =============================================================================

from rna_seq_factornet import ExpressionPipeline
from pathlib import Path

pipeline = ExpressionPipeline()

# Check if file exists
data_file = 'my_expression_data.csv'
if Path(data_file).exists():
    try:
        pipeline.load_data(data_file)
        pipeline.train_model()
        results = pipeline.interpret('bpnet', n_genes=5)
        print("✅ Analysis completed successfully!")
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
else:
    print(f"❌ File {data_file} not found!")


if __name__ == "__main__":
    print("🧬 RNA-seq FactorNet Basic Usage Examples")
    print("=" * 50)
    print("Run individual examples by uncommenting the code sections above")
    print("\n📚 Available methods:")
    print("- ExpressionPipeline(): Main pipeline class")
    print("- quick_analysis(): One-function analysis")  
    print("- load_example_data(): Get synthetic test data")
    print("\n🔬 Interpretation methods:")
    print("- 'bpnet': BPNet-style contribution scores")
    print("- 'saliency': Gradient-based saliency maps")
    print("- 'integrated_gradients': Integrated gradients attribution")
    print("- 'gradients': Standard gradient attribution")