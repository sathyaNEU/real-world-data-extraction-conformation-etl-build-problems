"""The two golden deliverables."""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import world as W


def table(path, g):
    """The schedule the committee paper carries: one row per work programme, the authority last.

    Sorted by the misstatement indicated, descending, then by programme name, which is the order
    the chart uses too. Recorded value to the cent as the ledger holds it, the misstatement whole
    because 9.1 states it to the nearest fifty thousand, the share to one decimal.
    """
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["work_programme", "programme_code", "misstatement_indicated_eur",
                    "misstatement_as_pct_of_recorded_value"])
        for c in sorted(W.PROG_CODES, key=lambda c: (-g["per"][c], W.PROG_NAME[c])):
            w.writerow([W.PROG_NAME[c], c, g["per"][c],
                        "%.2f" % (100.0 * g["per"][c] / g["recorded"][c])])
        w.writerow(["Authority", "", g["total"],
                    "%.2f" % (100.0 * g["total"] / g["recorded_total"])])
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
    ax.set_xlabel("Misstatement indicated, thousands of euro, to the nearest fifty", fontsize=9)
    ax.set_title("The capital programme payments population is referred for extended testing:\n"
                 "%s euro indicated for the year to 31 December 2026, %s of it in %s"
                 % (format(g["total"], ","), format(g["per"][g["largest"]], ","),
                    W.PROG_NAME[g["largest"]]), fontsize=10, loc="left")
    for i, (b, v) in enumerate(zip(bars, vals)):
        ax.text(b.get_width() + max(vals) * 0.012, b.get_y() + b.get_height() / 2,
                "%s" % format(int(v * 1000), ","), va="center", fontsize=8.5)
    ax.set_xlim(0, max(vals) * 1.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", labelsize=8.5)
    fig.text(0.012, 0.022, "Three programmes show no misstatement: none of the lines tested in "
             "them carried an exception.", ha="left", fontsize=8, color="#44546a")
    fig.text(0.988, 0.022, "Internal audit, testing completed %s" % W.TESTING_DONE,
             ha="right", fontsize=8, color="#44546a")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)
    return path
