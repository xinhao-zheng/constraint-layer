# -*- coding: utf-8 -*-
"""
plot_figures.py - manuscript figures for "The Constraint Layer"
===============================================================

Publication-grade schematic figures, cold editorial style, English-only
labels. Both figures are explicitly schematic: no empirical series is
plotted; they illustrate the structural argument of the text. Labels sit
in clear regions; nothing crosses a line or a panel boundary.

Figures
    fig1  The complementarity (two panels)
          a  Generativity vs. bindability - where systems sit
          b  The agent action lifecycle - where the ledger attaches
    fig2  Bounded delegation and the determinism gap (two panels)
          a  Machine principal: authority compiled to a policy predicate
          b  Checked vs. settled under non-deterministic / deterministic rails

Usage
    python scripts/plot_figures.py
Outputs
    paper/figures/fig{1,2}_*.png (300 dpi) + .svg,
    copied into paper/en/ and paper/zh/
"""

from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parent.parent
PAPER_DIR = ROOT / "paper"
FIG_DIR = PAPER_DIR / "figures"

PAPER = "#FFFFFF"
INK = "#1B2128"
SLATE = "#4A545F"
MUTE = "#8A95A1"
FAINT = "#E7ECF1"
TRACK = "#EEF2F7"
RULE = "#D8DFE6"

GEN_C = "#A8503A"     # generativity / AI side
BIND_C = "#2F7D72"    # bindability / ledger side
PROOF_C = "#3C63A8"   # proof / policy
LEDGER_C = "#22384E"

TITLE_KW = dict(loc="left", fontsize=11.0, fontweight="bold", color=INK, pad=11)


def setup_style() -> None:
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "axes.edgecolor": "#2A2F36",
        "axes.linewidth": 0.8,
        "xtick.color": SLATE,
        "ytick.color": SLATE,
        "text.color": INK,
        "svg.fonttype": "none",
        "mathtext.fontset": "dejavusans",
    })


def panel_letter(fig: plt.Figure, ax: plt.Axes, letter: str) -> None:
    pos = ax.get_position()
    fig.text(pos.x0 - 0.050, pos.y1 + 0.028, letter, fontsize=13,
             fontweight="bold", color=INK, ha="left", va="baseline")


def _box(ax, x, y, w, h, label, *, fc="white", ec=INK, lw=1.0,
         fontsize=8.4, fontcolor=INK, bold=False) -> None:
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0,rounding_size=0.018",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3,
        mutation_aspect=0.6))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=fontsize, color=fontcolor,
            fontweight="bold" if bold else "normal", zorder=4,
            linespacing=1.05)


def _arrow(ax, x0, y0, x1, y1, *, color=SLATE, lw=1.3, mut=9.0,
           ls="-") -> None:
    ax.add_patch(FancyArrowPatch(
        (x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=mut,
        linewidth=lw, color=color, zorder=2, shrinkA=0, shrinkB=0,
        linestyle=ls))


# ----------------------------------------------------------------------
# Figure 1 - the complementarity
# ----------------------------------------------------------------------

def fig1() -> plt.Figure:
    fig = plt.figure(figsize=(12.8, 4.05))
    ax_a = fig.add_axes([0.066, 0.165, 0.372, 0.715])
    ax_b = fig.add_axes([0.560, 0.165, 0.420, 0.715])

    # -- panel a: generativity vs bindability -------------------------
    ax_a.add_patch(Rectangle((0.5, 0.5), 0.5, 0.5, facecolor=TRACK,
                             zorder=0))
    ax_a.text(0.97, 0.96, "trustworthy\nautonomy", fontsize=7.6,
              color=SLATE, ha="right", va="top", style="italic",
              linespacing=1.05, zorder=1)

    pts = [
        ("LLM agents", 0.86, 0.13, GEN_C, "below"),
        ("classical software", 0.17, 0.50, MUTE, "right"),
        ("value-only ledger", 0.13, 0.74, LEDGER_C, "right"),
        ("account-model contracts", 0.46, 0.40, PROOF_C, "below"),
    ]
    for label, x, y, c, where in pts:
        ax_a.scatter([x], [y], s=58, color=c, edgecolor="white",
                     linewidth=1.1, zorder=4)
        if where == "below":
            ax_a.text(x, y - 0.075, label, fontsize=8.0, color=c,
                      ha="center", va="top", fontweight="bold")
        elif where == "above":
            ax_a.text(x, y + 0.07, label, fontsize=8.0, color=c,
                      ha="center", va="bottom", fontweight="bold")
        else:
            ax_a.text(x + 0.035, y, label, fontsize=8.0, color=c,
                      ha="left", va="center", fontweight="bold")

    # target = agent paired with the constraint layer (star + inline label)
    ax_a.scatter([0.875], [0.84], s=165, marker="*", color=BIND_C,
                 edgecolor="white", linewidth=1.0, zorder=5)
    ax_a.text(0.825, 0.84, "agent +\nconstraint layer", fontsize=8.2,
              color=BIND_C, ha="right", va="center", fontweight="bold",
              linespacing=1.1)
    ax_a.add_patch(FancyArrowPatch(
        (0.875, 0.205), (0.875, 0.775), connectionstyle="arc3,rad=-0.17",
        arrowstyle="-|>", mutation_scale=11, lw=1.3, color=SLATE,
        zorder=3))
    ax_a.text(0.80, 0.45, "+ deterministic,\nproof-bearing\nsubstrate",
              fontsize=7.4, color=SLATE, ha="right", va="center",
              style="italic", linespacing=1.12, zorder=4)

    ax_a.set_xlim(0, 1.02)
    ax_a.set_ylim(0, 1.04)
    ax_a.set_xticks([])
    ax_a.set_yticks([])
    ax_a.set_xlabel("generativity  (open-ended decision)  \u2192",
                    fontsize=8.6, color=SLATE)
    ax_a.set_ylabel("bindability  (provable, settleable consequence)  \u2192",
                    fontsize=8.6, color=SLATE)
    for side in ("top", "right"):
        ax_a.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax_a.spines[side].set_color("#B9C2CC")
    ax_a.set_title("Generativity vs. bindability", **TITLE_KW)

    # -- panel b: agent action lifecycle ------------------------------
    ax_b.set_xlim(-0.02, 1.02)
    ax_b.set_ylim(0, 1)
    ax_b.axis("off")

    stages = [
        ("perceive", MUTE, "white"),
        ("decide", GEN_C, "#F6ECE8"),
        (r"prove $a \models \varphi$", PROOF_C, "#EAF0F8"),
        ("settle", BIND_C, "#E7F1EF"),
        ("audit", LEDGER_C, "#EAEEF3"),
    ]
    n = len(stages)
    w, gap = 0.156, 0.055
    total = n * w + (n - 1) * gap
    x0 = (1.0 - total) / 2
    yc, h = 0.395, 0.215
    centers = []
    for i, (label, ec, fc) in enumerate(stages):
        x = x0 + i * (w + gap)
        _box(ax_b, x, yc, w, h, label, fc=fc, ec=ec, fontsize=9.0,
             fontcolor=INK, bold=True)
        centers.append(x + w / 2)
        if i > 0:
            _arrow(ax_b, x - gap, yc + h / 2, x, yc + h / 2)

    # brackets over the AI side and the ledger side
    def bracket(x_lo, x_hi, y, label, color):
        ax_b.plot([x_lo, x_lo, x_hi, x_hi], [y - 0.025, y, y, y - 0.025],
                  color=color, lw=1.2, zorder=2)
        ax_b.text((x_lo + x_hi) / 2, y + 0.022, label, fontsize=8.2,
                  color=color, ha="center", va="bottom", fontweight="bold")

    dx = w / 2 + 0.012
    bracket(centers[1] - dx, centers[1] + dx, 0.760,
            "AI : generative, non-deterministic", GEN_C)
    bracket(centers[2] - dx, centers[4] + dx, 0.760,
            "ledger : rule-bound, deterministic", BIND_C)

    ax_b.text(centers[2], 0.195,
              "policy $\\varphi$ compiled by the principal",
              fontsize=8.0, color=SLATE, ha="center", va="center")
    ax_b.annotate("", xy=(centers[2], yc - 0.012),
                  xytext=(centers[2], 0.235),
                  arrowprops=dict(arrowstyle="-", lw=0.9, color=MUTE,
                                  ls=(0, (2, 2))))
    ax_b.set_title("Where the constraint layer attaches", **TITLE_KW)

    panel_letter(fig, ax_a, "a")
    panel_letter(fig, ax_b, "b")
    return fig


# ----------------------------------------------------------------------
# Figure 2 - bounded delegation and the determinism gap
# ----------------------------------------------------------------------

def fig2() -> plt.Figure:
    fig = plt.figure(figsize=(12.6, 4.5))
    ax_a = fig.add_axes([0.020, 0.070, 0.470, 0.820])
    ax_b = fig.add_axes([0.545, 0.070, 0.440, 0.820])
    for ax in (ax_a, ax_b):
        ax.set_xlim(-0.04, 1.04)
        ax.set_ylim(-0.06, 1.04)
        ax.axis("off")

    # -- a: bounded delegation ----------------------------------------
    ax = ax_a
    top, h = 0.72, 0.150
    _box(ax, 0.03, top, 0.26, h, "principal\n(human)", fontsize=8.2,
         bold=True)
    _box(ax, 0.40, top, 0.21, h, r"policy $\varphi$", fc="#F1F5FA",
         ec=SLATE, fontsize=8.8, fontcolor=SLATE)
    _box(ax, 0.72, top, 0.22, h, "agent", bold=True)
    _arrow(ax, 0.29, top + h / 2, 0.40, top + h / 2)
    _arrow(ax, 0.61, top + h / 2, 0.72, top + h / 2)
    ax.text(0.345, top + h + 0.045, "compile", fontsize=7.2, color=MUTE,
            ha="center")

    mid = 0.40
    _box(ax, 0.27, mid, 0.40, h, r"action $a \,\Vert\, \pi(a \models \varphi)$",
         fc="#EAF0F8", ec=PROOF_C, fontsize=8.8, fontcolor=LEDGER_C)
    _box(ax, 0.74, mid, 0.21, h, "counter-\nparty", fontsize=8.0)
    _arrow(ax, 0.78, top, 0.60, mid + h, lw=1.2)
    _arrow(ax, 0.67, mid + h / 2, 0.74, mid + h / 2)
    ax.text(0.705, mid + h + 0.03, "verify $\\pi$", fontsize=7.2, color=MUTE,
            ha="center", va="bottom")

    ax.add_patch(Rectangle((0.03, 0.105), 0.92, 0.105,
                           facecolor=LEDGER_C, edgecolor=LEDGER_C, zorder=3))
    ax.text(0.49, 0.1575, "L : public ledger - settlement and audit trail",
            ha="center", va="center", fontsize=8.0, color="white", zorder=4)
    for xd in (0.47, 0.845):
        ax.plot([xd, xd], [0.210, mid - 0.01], color=MUTE, lw=1.0,
                ls=(0, (2, 2)), zorder=1)
    ax.text(0.49, 0.028,
            "authority bounded ex ante - audit = replay the proofs",
            ha="center", fontsize=8.0, color=INK, fontweight="bold")
    ax.set_title("Bounded delegation", **TITLE_KW)

    # -- b: checked vs settled ----------------------------------------
    ax = ax_b
    bh = 0.135

    def rail(y, fc, ec, mid_label, mid_fc, result, result_color, ok):
        _box(ax, 0.02, y, 0.27, bh, "agent checks\naction @ $s_0$",
             fc="white", ec=SLATE, fontsize=7.8)
        _box(ax, 0.37, y, 0.26, bh, mid_label, fc=mid_fc, ec=ec,
             fontsize=7.6, fontcolor=ec)
        _box(ax, 0.71, y, 0.27, bh, result, fc=fc, ec=ec, fontsize=7.8,
             fontcolor=LEDGER_C)
        _arrow(ax, 0.29, y + bh / 2, 0.37, y + bh / 2, color=ec)
        _arrow(ax, 0.63, y + bh / 2, 0.71, y + bh / 2, color=ec)
        mark = "=" if ok else "\u2260"
        ax.text(0.50, y - 0.052, f"checked {mark} settled", fontsize=8.0,
                color=result_color, ha="center", va="center",
                fontweight="bold")

    rail(0.66, "#F6ECE8", GEN_C,
         "others reorder /\ninsert at inclusion", "#FBF3EF",
         "settles @ $s' \\neq s_0$", GEN_C, ok=False)
    ax.text(0.50, 0.875, "non-deterministic rail", fontsize=8.4,
            color=GEN_C, ha="center", fontweight="bold")

    rail(0.20, "#E7F1EF", BIND_C,
         "inputs fixed by\nthe action itself", "#EEF6F4",
         "settles @ $s_0$", BIND_C, ok=True)
    ax.text(0.50, 0.415, "deterministic rail (local = global)",
            fontsize=8.4, color=BIND_C, ha="center", fontweight="bold")

    ax.set_title("Checked vs. settled", **TITLE_KW)

    panel_letter(fig, ax_a, "a")
    panel_letter(fig, ax_b, "b")
    return fig


def main() -> None:
    setup_style()
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    jobs = [(fig1(), "fig1_complementarity"), (fig2(), "fig2_delegation")]
    outputs: list[Path] = []
    for fig, stem in jobs:
        png = FIG_DIR / f"{stem}.png"
        fig.savefig(png, dpi=300, bbox_inches="tight", pad_inches=0.08)
        try:
            fig.savefig(FIG_DIR / f"{stem}.svg",
                        bbox_inches="tight", pad_inches=0.08)
        except Exception as exc:  # pragma: no cover
            print(f"[warn] svg export skipped: {exc}")
        plt.close(fig)
        outputs.append(png)
        print(f"[ok] {png}")

    for sub in ("en", "zh"):
        dest = PAPER_DIR / sub
        dest.mkdir(parents=True, exist_ok=True)
        for png in outputs:
            shutil.copy2(png, dest / png.name)
            print(f"[ok] {dest / png.name}")


if __name__ == "__main__":
    main()
