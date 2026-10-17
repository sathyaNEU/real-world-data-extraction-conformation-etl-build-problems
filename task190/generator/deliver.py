"""The two golden deliverables."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import world as W


def table(path, g):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["work_programme", "payments_recorded_eur", "misstatement_indicated_eur",
                    "share_of_recorded_value_certain_of_selection_pct"])
        for c in sorted(W.PROG_CODES, key=lambda c: (-g["per"][c], W.PROG_NAME[c])):
            w.writerow([W.PROG_NAME[c], "%.2f" % g["recorded"][c], g["per"][c],
                        "%.1f" % g["certain_share"][c]])
        w.writerow(["Authority", "%.2f" % g["recorded_total"], g["total"], ""])
    return path


def chart(path, g):
    order = sorted(W.PROG_CODES, key=lambda c: (-g["per"][c], W.PROG_NAME[c]))
    vals = [g["per"][c] / 1000.0 for c in order]
    names = [W.PROG_NAME[c] for c in order]
    fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=150)
    cols = ["#1f3b63" if c == g["largest"] else "#9fb3c8" for c in order]
    bars = ax.barh(range(len(order))[::-1], vals, color=cols, height=0.64)
    ax.set_yticks(range(len(order))[::-1])
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel("Misstatement indicated, thousands of euro", fontsize=9)
    ax.set_title("Capital programme payments 2026: misstatement indicated by work programme,\n"
                 "authority total %s euro against tolerable misstatement of %s euro"
                 % (format(g["total"], ","), format(int(W.TOLERABLE), ",")), fontsize=10,
                 loc="left")
    for i, (b, v) in enumerate(zip(bars, vals)):
        ax.text(b.get_width() + max(vals) * 0.012, b.get_y() + b.get_height() / 2,
                "%s" % format(int(v * 1000), ","), va="center", fontsize=8.5)
    ax.set_xlim(0, max(vals) * 1.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", labelsize=8.5)
    fig.text(0.985, 0.022, "%s marked: the programme carrying most of the misstatement"
             % W.PROG_NAME[g["largest"]], ha="right", fontsize=8, color="#44546a")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)
    return path
