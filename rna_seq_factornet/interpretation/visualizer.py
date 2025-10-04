# rna_seq_factornet/interpretation/visualizer.py
"""
Interpretability Visualization Utilities for RNA-seq FactorNet

This module renders:
  1) BPNet-style *profile contribution* tracks (gradient × input)
  2) Saliency maps (|gradient|) across samples/features
  3) Heatmaps for multi-gene attribution matrices

It is designed to be called by the pipeline:
    ExpressionPipeline.visualize(...)
        -> plot_contribution_profile(...)  # single gene vector
        -> plot_contribution_heatmap(...)  # multi-gene matrix

Expected inputs (consistent with pipeline.interpret results):
    - feature_importance: np.ndarray with shape (n_genes, n_features) or (n_features,)
    - gene_names: List[str] length n_genes
    - sample_names: List[str] length n_features

No plotting backends beyond matplotlib are required.

Author: Geo Project
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple, Union

import numpy as np
import matplotlib.pyplot as plt


ArrayLike = Union[np.ndarray, Sequence[float]]


@dataclass
class _Style:
    """Small style container for figure sizes and dpi."""
    figsize_profile: Tuple[float, float] = (10.0, 4.0)
    figsize_heatmap: Tuple[float, float] = (10.0, 6.0)
    dpi: int = 120
    font_size: int = 10
    tick_font_size: int = 8
    grid_alpha: float = 0.25


class InterpretabilityVisualizer:
    """
    Visualization class used by the pipeline.

    Public methods used by the pipeline:
        - plot_contribution_profile(...)
        - plot_contribution_heatmap(...)

    Additional helpers:
        - plot_saliency_profile(...)      # saliency for one gene
        - plot_saliency_heatmap(...)      # saliency heatmap (abs values)
        - to_dataframe(...)               # convert attributions to a tidy DataFrame
    """

    def __init__(self, style: Optional[_Style] = None):
        self.style = style or _Style()
        # Set some readable defaults without forcing a global style
        plt.rcParams.update({
            "figure.dpi": self.style.dpi,
            "font.size": self.style.font_size,
            "axes.titlesize": self.style.font_size + 1,
            "axes.labelsize": self.style.font_size,
            "xtick.labelsize": self.style.tick_font_size,
            "ytick.labelsize": self.style.tick_font_size,
        })

    # ------------------------------------------------------------------
    # Core API (used by ExpressionPipeline.visualize)
    # ------------------------------------------------------------------
    def plot_contribution_profile(
        self,
        contrib_vector: ArrayLike,
        gene_name: str,
        sample_names: Sequence[str],
        method_name: str,
        save_path: Optional[str] = None,
        *,
        kind: str = "bar",
        zero_line: bool = True,
        center_zero: bool = True,
        annotate_top_k: Optional[int] = None,
    ):
        """
        Plot a single-gene attribution profile across samples/features.

        Parameters
        ----------
        contrib_vector : array-like, shape (n_features,)
            Attribution values (e.g., BPNet gradient×input OR saliency values).
        gene_name : str
            Gene identifier for title/filename.
        sample_names : list[str]
            Feature/sample labels for the x-axis.
        method_name : str
            Label shown in the title (e.g., 'BPNet', 'Saliency', 'Integrated Gradients').
        save_path : str or None
            If provided, saves the figure to this path (directories created if missing).
        kind : {'bar', 'line'}, default 'bar'
            Visualization mode for the profile.
        zero_line : bool, default True
            Draw a horizontal line at y=0 (useful for signed attributions).
        center_zero : bool, default True
            Force symmetric y-limits around zero for diverging visuals (if signed).
        annotate_top_k : int or None
            If set, annotate the top-k absolute contribution positions.

        Returns
        -------
        fig, ax : matplotlib Figure and Axes
        """
        v = np.asarray(contrib_vector).astype(float)
        if v.ndim != 1:
            raise ValueError(f"contrib_vector must be 1D, got shape {v.shape}")
        if len(sample_names) != v.shape[0]:
            raise ValueError(
                f"len(sample_names) ({len(sample_names)}) != contrib_vector length ({v.shape[0]})"
            )

        fig, ax = plt.subplots(figsize=self.style.figsize_profile)

        # Choose colors for signed data (positive/negative) or single color for >=0
        signed = np.any(v < 0) and np.any(v > 0)
        if kind == "bar":
            if signed:
                colors = np.where(v >= 0, "#2E7D32", "#C62828")  # green/red
            else:
                colors = "#1E88E5"  # blue
            ax.bar(np.arange(len(v)), v, color=colors, width=0.8, edgecolor="none")
        elif kind == "line":
            ax.plot(np.arange(len(v)), v, linewidth=1.5)
        else:
            raise ValueError("kind must be 'bar' or 'line'")

        if zero_line:
            ax.axhline(0.0, color="black", linewidth=0.8, alpha=0.6)

        # Symmetric y-range for signed attributions for fair visual comparison
        if center_zero and signed:
            m = np.nanmax(np.abs(v)) if v.size else 1.0
            ax.set_ylim(-m * 1.05, m * 1.05)

        # Axes labels & ticks
        ax.set_title(f"{method_name} Profile — {gene_name}")
        ax.set_xlabel("Samples / Features")
        ax.set_ylabel("Contribution" if signed else "Importance")

        ax.set_xticks(np.arange(len(sample_names)))
        ax.set_xticklabels(sample_names, rotation=60, ha="right")

        ax.grid(axis="y", alpha=self.style.grid_alpha, linestyle="--")

        # Optional annotations for top-k contributors (by absolute value)
        if annotate_top_k is not None and annotate_top_k > 0:
            k = min(annotate_top_k, v.size)
            top_idx = np.argsort(np.abs(v))[-k:][::-1]
            for i in top_idx:
                ax.annotate(
                    sample_names[i],
                    (i, v[i]),
                    xytext=(0, 6 if v[i] >= 0 else -10),
                    textcoords="offset points",
                    ha="center",
                    va="bottom" if v[i] >= 0 else "top",
                    fontsize=self.style.tick_font_size,
                    rotation=60,
                )

        self._save_or_show(fig, save_path)
        return fig, ax

    def plot_contribution_heatmap(
        self,
        matrix: ArrayLike,
        gene_names: Sequence[str],
        sample_names: Sequence[str],
        method_name: str,
        save_path: Optional[str] = None,
        *,
        symmetric: bool = True,
        colorbar: bool = True,
        cmap_signed: str = "RdBu_r",
        cmap_positive: str = "viridis",
    ):
        """
        Heatmap of attributions for multiple genes (genes × features).

        Parameters
        ----------
        matrix : array-like, shape (n_genes, n_features)
            Attribution/importance matrix.
        gene_names : list[str]
            Row labels.
        sample_names : list[str]
            Column labels.
        method_name : str
            Label in the title (e.g., 'BPNet', 'Saliency', ...).
        save_path : str or None
            If provided, saves the figure.
        symmetric : bool, default True
            If True and matrix contains negative values, use symmetric color limits.
        colorbar : bool, default True
            Show a colorbar.
        cmap_signed : str
            Colormap for signed data.
        cmap_positive : str
            Colormap for nonnegative data.

        Returns
        -------
        fig, ax : matplotlib Figure and Axes
        """
        M = np.asarray(matrix).astype(float)
        if M.ndim != 2:
            raise ValueError(f"matrix must be 2D, got shape {M.shape}")
        if len(gene_names) != M.shape[0]:
            raise ValueError("len(gene_names) must match matrix rows")
        if len(sample_names) != M.shape[1]:
            raise ValueError("len(sample_names) must match matrix cols")

        fig, ax = plt.subplots(figsize=self.style.figsize_heatmap)

        has_neg = np.nanmin(M) < 0
        if has_neg and symmetric:
            vmax = np.nanmax(np.abs(M)) or 1.0
            vmin = -vmax
            cmap = cmap_signed
        else:
            vmin = np.nanmin(M)
            vmax = np.nanmax(M)
            cmap = cmap_positive

        im = ax.imshow(M, aspect="auto", interpolation="nearest",
                       cmap=cmap, vmin=vmin, vmax=vmax)

        ax.set_title(f"{method_name} — Feature Importance Heatmap")
        ax.set_xlabel("Samples / Features")
        ax.set_ylabel("Genes")

        ax.set_xticks(np.arange(len(sample_names)))
        ax.set_xticklabels(sample_names, rotation=60, ha="right")
        ax.set_yticks(np.arange(len(gene_names)))
        ax.set_yticklabels(gene_names)

        # Light gridlines to aid reading
        ax.set_xticks(np.arange(-0.5, M.shape[1], 1), minor=True)
        ax.set_yticks(np.arange(-0.5, M.shape[0], 1), minor=True)
        ax.grid(which="minor", color="white", linewidth=0.5, alpha=0.5)
        ax.tick_params(which="minor", bottom=False, left=False)

        if colorbar:
            cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            cbar.set_label("Contribution" if has_neg else "Importance")

        fig.tight_layout()
        self._save_or_show(fig, save_path)
        return fig, ax

    # ------------------------------------------------------------------
    # Convenience additions (optional but handy)
    # ------------------------------------------------------------------
    def plot_saliency_profile(
        self,
        saliency_vector: ArrayLike,
        gene_name: str,
        sample_names: Sequence[str],
        save_path: Optional[str] = None,
        **kwargs,
    ):
        """
        Thin wrapper around plot_contribution_profile for saliency vectors.
        Saliency is typically nonnegative, so diverging settings aren't needed.
        """
        return self.plot_contribution_profile(
            saliency_vector,
            gene_name,
            sample_names,
            method_name="Saliency",
            save_path=save_path,
            kind=kwargs.get("kind", "bar"),
            zero_line=kwargs.get("zero_line", False),
            center_zero=kwargs.get("center_zero", False),
            annotate_top_k=kwargs.get("annotate_top_k", None),
        )

    def plot_saliency_heatmap(
        self,
        saliency_matrix: ArrayLike,
        gene_names: Sequence[str],
        sample_names: Sequence[str],
        save_path: Optional[str] = None,
        **kwargs,
    ):
        """
        Heatmap for saliency (absolute gradients). Uses a non-diverging colormap.
        """
        return self.plot_contribution_heatmap(
            saliency_matrix,
            gene_names,
            sample_names,
            method_name="Saliency",
            save_path=save_path,
            symmetric=False,
            colorbar=kwargs.get("colorbar", True),
            cmap_positive=kwargs.get("cmap_positive", "viridis"),
        )

    @staticmethod
    def to_dataframe(
        matrix: ArrayLike,
        gene_names: Sequence[str],
        sample_names: Sequence[str],
    ):
        """
        Convert an attribution matrix to a pandas DataFrame (genes × samples).
        """
        try:
            import pandas as pd
        except ImportError as e:
            raise ImportError("pandas is required for to_dataframe(...)") from e

        M = np.asarray(matrix)
        if M.ndim == 1:
            M = M[None, :]
        return pd.DataFrame(M, index=list(gene_names), columns=list(sample_names))

    # ------------------------------------------------------------------
    # Internal utilities
    # ------------------------------------------------------------------
    @staticmethod
    def _ensure_dir(path: str):
        p = Path(path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        return str(p)

    def _save_or_show(self, fig: plt.Figure, save_path: Optional[str]):
        if save_path:
            path = self._ensure_dir(save_path)
            fig.savefig(path, bbox_inches="tight")
            plt.close(fig)
        else:
            # Return but keep the figure open for interactive sessions
            fig.tight_layout()
