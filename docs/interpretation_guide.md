# RNA-seq FactorNet Interpretation Guide

## Overview

RNA-seq FactorNet provides several feature attribution/interpretability methods:
- **BPNet Contribution Scores (Gradient × Input):** Highlights regulatory features.
- **Saliency Maps:** Shows direct sensitivity of genes.
- **Integrated Gradients:** Robust importance using gradient integration.

## How to Use

After training, call:

results = pipeline.interpret('bpnet', n_genes=10)
pipeline.visualize(results)

## Choosing a Method

- **BPNet:** Best for regulatory landscape analysis.
- **Saliency:** Direct, fast for exploratory work.
- **Integrated Gradients:** Best for robust, high-confidence attribution.

## Visualization

- Individual gene profiles and heatmaps are produced for deeper biological insights.

## Advanced Tips

- Use `compare_methods` to see differences across interpretability styles.
- Adjust `n_genes` and attribution parameters for more/fewer genes.

---

Explore examples in `examples/interpretation_demo.py` or `getting_started.md`.
