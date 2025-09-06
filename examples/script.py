# Create a modular package structure for RNA-seq FactorNet
import os
from pathlib import Path

print("🏗️ CREATING MODULAR RNA-SEQ FACTORNET PACKAGE")
print("=" * 60)

# Create the package structure
package_structure = {
    'rna_seq_factornet/': {
        '__init__.py': '',
        'data/': {
            '__init__.py': '',
            'loader.py': 'ExpressionDataLoader class',
            'preprocessor.py': 'Data preprocessing utilities'
        },
        'models/': {
            '__init__.py': '',
            'factornet.py': 'ExpressionFactorNet model class',
            'training.py': 'Training utilities and cross-validation'
        },
        'interpretation/': {
            '__init__.py': '',
            'methods.py': 'All interpretation methods (saliency, bpnet, etc.)',
            'visualizer.py': 'Visualization utilities'
        },
        'pipeline/': {
            '__init__.py': '',
            'core.py': 'Main pipeline class',
            'analysis.py': 'Analysis workflows'
        },
        'utils/': {
            '__init__.py': '',
            'validation.py': 'Data validation utilities',
            'metrics.py': 'Evaluation metrics'
        }
    },
    'examples/': {
        'basic_usage.py': 'Simple usage examples',
        'advanced_analysis.py': 'Advanced analysis workflows',
        'interpretation_demo.py': 'Interpretation methods demo'
    },
    'tests/': {
        '__init__.py': '',
        'test_data_loader.py': 'Data loader tests',
        'test_model.py': 'Model tests',
        'test_interpretation.py': 'Interpretation tests'
    },
    'docs/': {
        'README.md': 'Detailed documentation',
        'API.md': 'API reference',
        'tutorials/': {
            'getting_started.md': 'Getting started guide',
            'interpretation_guide.md': 'Interpretation methods guide'
        }
    }
}

def create_directory_structure(structure, base_path='.'):
    """Create directory structure recursively"""
    for name, content in structure.items():
        path = Path(base_path) / name
        
        if isinstance(content, dict):
            # It's a directory
            path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created directory: {path}")
            create_directory_structure(content, path)
        else:
            # It's a file
            if not path.exists():
                path.touch()
                print(f"📄 Created file: {path}")

# Create the structure
create_directory_structure(package_structure)
print("\n✅ Package structure created!")