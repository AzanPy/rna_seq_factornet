from setuptools import setup, find_packages

# --- Basic project metadata ---
NAME = "rna_seq_factornet"
DESCRIPTION = "Deep Learning Framework for RNA-seq Expression Analysis with Interpretability"
URL = "https://github.com/AzanPy/rna_seq_factornet"  # update with your actual GitHub URL
AUTHOR = "Azan"
AUTHOR_EMAIL = "your.email@example.com"
LICENSE = "MIT"
VERSION = "1.0.0"
PYTHON_REQUIRES = ">=3.8"

# --- Long description from README.md ---
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# --- Requirements from requirements.txt ---
try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        install_requires = [
            line.strip() for line in fh
            if line.strip() and not line.startswith("#")
        ]
except FileNotFoundError:
    install_requires = []

# --- Setup configuration ---
setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    project_urls={
        "Bug Tracker": f"{URL}/issues",
        "Documentation": f"{URL}/tree/main/docs",
        "Source Code": URL,
    },
    license=LICENSE,
    packages=find_packages(include=["rna_seq_factornet", "rna_seq_factornet.*"]),
    include_package_data=True,
    python_requires=PYTHON_REQUIRES,
    install_requires=install_requires,
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
    keywords="rna-seq deep-learning bioinformatics interpretability factornet machine-learning",
)
