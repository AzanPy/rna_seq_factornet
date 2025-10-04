# RNA-seq FactorNet 🧬

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![TensorFlow 2.0+](https://img.shields.io/badge/tensorflow-2.0+-orange.svg)](https://tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](docs/)

A comprehensive deep learning framework for RNA-seq expression data analysis with advanced interpretability methods. Built on a modified FactorNet architecture with integrated gradient-based attribution techniques.

## ✨ Features

- **🔬 Deep Learning**: Modified FactorNet architecture optimized for expression data
- **🧠 Interpretability**: Multiple attribution methods (Integrated Gradients, Saliency Maps, BPNet-style)
- **📊 Robust Data Handling**: Comprehensive NaN handling and preprocessing
- **📈 Visualization**: Publication-ready plots and heatmaps
- **⚡ Easy to Use**: Simple 3-line API for quick analysis
- **📁 Multiple Formats**: Support for CSV, TSV, TXT, and Excel files

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/yourusername/rna-seq-factornet.git
cd rna-seq-factornet
pip install -r requirements.txt
```

### Simple 3-Line Analysis

```python
from rna_seq_factornet import ExpressionPipeline

pipeline = ExpressionPipeline()
pipeline.load_data('expression_data.csv')
pipeline.train_model()

# Interpret with BPNet-style contribution scores
results = pipeline.interpret('bpnet', n_genes=5)
pipeline.visualize(results)
```

### One-Line Analysis

```python
from rna_seq_factornet import quick_analysis

pipeline, results = quick_analysis('expression_data.csv', method='bpnet')
```

## 📖 Documentation

- **[Getting Started Guide](docs/tutorials/getting_started.md)** - Complete tutorial
- **[API Reference](docs/API.md)** - Detailed API documentation  
- **[Interpretation Guide](docs/tutorials/interpretation_guide.md)** - Understanding results
- **[Examples](examples/)** - Usage examples and demos

## 🔬 Interpretation Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| **BPNet** | Gradient × input contribution scores | Similar to genomic BPNet analysis |
| **Saliency Maps** | Direct gradient-based importance | Fast, interpretable attribution |
| **Integrated Gradients** | Baseline-to-input attribution | Gold standard for attribution |
| **Standard Gradients** | Traditional gradient attribution | Baseline comparison method |

## 📊 Supported Data Formats

- **CSV/TSV/TXT**: Delimiter auto-detection
- **Excel**: Multi-sheet support (.xls, .xlsx)
- **Data Layout**: Genes as rows, samples as columns
- **Missing Data**: Multiple NaN handling strategies

## 🛠️ Advanced Usage

### Custom Model Training

```python
from rna_seq_factornet import ExpressionPipeline

pipeline = ExpressionPipeline()
pipeline.load_data('data.csv', nan_strategy='fill_mean')

pipeline.train_model(
    use_cv=True,
    k_folds=5,
    epochs=50,
    conv_filters=64,
    lstm_units=64
)
```

### Method Comparison

```python
# Compare multiple interpretation methods
comparison = pipeline.compare_methods(['bpnet', 'saliency', 'integrated_gradients'])

# Visualize comparison
pipeline.visualizer.plot_method_comparison(comparison, gene_idx=0)
```

### Modular Components

```python
from rna_seq_factornet.models import ExpressionFactorNet
from rna_seq_factornet.data import ExpressionDataLoader
from rna_seq_factornet.interpretation import SaliencyMethods

# Manual control over components
loader = ExpressionDataLoader()
model = ExpressionFactorNet(n_features=50)
interpreter = SaliencyMethods(model)
```

## 📈 Example Results

### Contribution Profiles
Individual gene contribution patterns across samples showing which samples contribute most to predictions.

### Heatmaps  
Multi-gene visualization matrices revealing expression patterns and sample relationships.

### Method Comparisons
Side-by-side attribution comparisons to understand different interpretability perspectives.

## 🔧 Requirements

- Python 3.8+
- TensorFlow 2.0+
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- Openpyxl (for Excel support)

## 📦 Installation Options

### From Source
```bash
git clone https://github.com/yourusername/rna-seq-factornet.git
cd rna-seq-factornet
pip install -e .
```

### Development Installation  
```bash
git clone https://github.com/yourusername/rna-seq-factornet.git
cd rna-seq-factornet
pip install -e ".[dev]"
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_model.py

# Run with coverage
pytest --cov=rna_seq_factornet tests/
```

## 📚 Examples

- **[Basic Usage](examples/basic_usage.py)** - Simple API examples
- **[Advanced Analysis](examples/advanced_analysis.py)** - Complex workflows
- **[Interpretation Demo](examples/interpretation_demo.py)** - Method comparisons

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/rna-seq-factornet/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/rna-seq-factornet/discussions)
- **Email**: your.email@example.com

## 📊 Citation

If you use this software in your research, please cite:

```bibtex
@software{rna_seq_factornet,
  author = {Your Name},
  title = {RNA-seq FactorNet: Deep Learning Framework for Expression Analysis},
  url = {https://github.com/yourusername/rna-seq-factornet},
  version = {1.0.0},
  year = {2025}
}
```

## 🙏 Acknowledgments

- FactorNet architecture inspiration
- TensorFlow and Keras teams
- Scikit-learn contributors
- Open source community

---

<div align="center">
  Made with ❤️ for the bioinformatics community
</div>