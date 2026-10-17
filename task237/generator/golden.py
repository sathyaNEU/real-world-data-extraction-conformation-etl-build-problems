"""The golden deliverables: bcs12_wave6_release_decisions.csv and bcs12_wave6_release_chart.png."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

CSV = "bcs12_wave6_release_decisions.csv"
PNG = "bcs12_wave6_release_chart.png"
INK = "#2F3B45"
COLOUR = {"release": "#2E7D4F", "hold": "#C27C0E", "rework": "#B03A2E"}
BAND = {"release": "#E3F1E7", "hold": "#FBF0DC", "rework": "#F6E1DE"}
HEAD = ["version", "language", "vendor", "mode", "decision", "valid_pilot_completes", "pilot_mean_score"]


def table(path, A):
    lines = [",".join(HEAD)]
    for r in A["versions"]:
        lang = '"%s"' % r["language"] if "," in r["language"] else r["language"]
        lines.append(",".join([r["code"], lang, r["vendor"], r["mode"], r["decision"], str(r["completes"]),
                               "%.2f" % r["mean"]]))
    with open(path, "w", newline="") as fh:
        fh.write("\n".join(lines) + "\n")


def chart(path, A):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    rows = A["versions"][::-1]
    fig, ax = plt.subplots(figsize=(10.4, 6.4), dpi=150)
    lo, hi = 0.45, 0.95
    ax.axvspan(lo, 0.70, color=BAND["rework"], zorder=0)
    ax.axvspan(0.70, 0.80, color=BAND["hold"], zorder=0)
    ax.axvspan(0.80, hi, color=BAND["release"], zorder=0)
    for x in (0.70, 0.80):
        ax.axvline(x, color=INK, linewidth=0.9, linestyle="--", zorder=1)
    for i, r in enumerate(rows):
        a, t = r["alpha"], r["share"]
        if abs(a - t) > 0.012:
            ax.annotate("", xy=(t, i), xytext=(a, i), zorder=2,
                        arrowprops=dict(arrowstyle="-|>", color="#7A8793", linewidth=1.1, shrinkA=4, shrinkB=5))
        ax.scatter([a], [i], s=46, facecolors="white", edgecolors="#55616C", linewidths=1.3, zorder=3)
        ax.scatter([t], [i], s=62, color=COLOUR[r["decision"]], zorder=4)
        ax.text(hi - 0.004, i, r["decision"].upper(), ha="right", va="center", fontsize=8.6, fontweight="bold",
                color=COLOUR[r["decision"]])
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(["%s (%s)%s" % (r["short"], r["code"], "\nwording factor" if r["wording"] else "") for r in rows],
                       fontsize=8.8, linespacing=1.15)
    ax.set_xlim(lo, hi)
    ax.set_ylim(-0.7, len(rows) - 0.3)
    ax.set_xlabel("reliability of the total score", fontsize=9)
    ax.text(0.575, len(rows) - 0.45, "rework, under 0.70", ha="center", va="top", fontsize=8, color=COLOUR["rework"])
    ax.text(0.75, len(rows) - 0.45, "hold, 0.70 to under 0.80", ha="center", va="top", fontsize=8, color=COLOUR["hold"])
    ax.text(0.86, len(rows) - 0.45, "release, 0.80 or more", ha="center", va="top", fontsize=8, color=COLOUR["release"])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    handles = [Line2D([], [], marker="o", linestyle="", markerfacecolor="white", markeredgecolor="#55616C",
                      markersize=7, label="Cronbach's alpha (counts the wording factor as connectedness)"),
               Line2D([], [], marker="o", linestyle="", color=INK, markersize=7,
                      label="trait's share of score variance, wording factor separated (decides)")]
    ax.legend(handles=handles, loc="lower left", fontsize=8, frameon=True, framealpha=0.95)
    fig.subplots_adjust(left=0.17, right=0.97, top=0.84, bottom=0.10)
    c = A["counts"]
    fig.text(0.012, 0.975, "Release %d versions, hold %d and send %d back: alpha would release %d" %
             (c["release"], c["hold"], c["rework"], A["alpha_release"]), fontsize=12.5, fontweight="bold", va="top",
             color=INK)
    fig.text(0.012, 0.925, "BCS-12 wave 6 language versions, pilot valid completes who answered all twelve items. In six "
                           "translations the six negatively worded items share a wording factor;\nalpha counts it as "
                           "connectedness, the trait's share (omega hierarchical, bifactor model) does not. Bands: TAS-4 "
                           "section 6.", fontsize=8.3, va="top", color="#333333", linespacing=1.4)
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write(golden_dir, A):
    os.makedirs(golden_dir, exist_ok=True)
    table(os.path.join(golden_dir, CSV), A)
    chart(os.path.join(golden_dir, PNG), A)
