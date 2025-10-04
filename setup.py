from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rna-seq-factornet",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Deep Learning Framework for RNA-seq Expression Analysis with Interpretability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/rna-seq-factornet",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/rna-seq-factornet/issues",
        "Documentation": "https://github.com/yourusername/rna-seq-factornet/docs",
        "Source Code": "https://github.com/yourusername/rna-seq-factornet",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    include_package_data=True,
    keywords="rna-seq, deep-learning, bioinformatics, interpretability, factornet, machine-learning",
)