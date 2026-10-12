"""Write the two deliverables from the golden figures: the client flag file and the September bridge."""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

LAYOUT_COLS = ["report_period", "cusip", "ticker", "inst_own_pct", "crowded", "prior_inst_own_pct"]


def r1(x):
    """one decimal, half away from zero, on the unrounded value"""
    from decimal import Decimal, ROUND_HALF_UP
    return str(Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def flag_file(g, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(LAYOUT_COLS)
        for c, t in zip(g["cusips"], g["tickers"]):
            w.writerow(["2022-12-31", c, t, r1(g["dec_io"][c]), "Y" if g["flag"][c] else "N", r1(g["sep_io"][c])])


def bridge_png(g, path):
    b = g["bridge"]
    steps = [("Information-table lines\nas filed", b["raw"], "total"),
             ("Put and call lines\n(put/call field or title)", -b["options"], "down"),
             ("Other lines in reports replaced\nby a later amendment", -b["superseded"], "down"),
             ("Lines matched back\nto their CUSIPs", b["cusip_repaired"], "up"),
             ("September institutional\nshares, twelve names", b["conformed"], "total")]
    fig, ax = plt.subplots(figsize=(10.5, 5.6), dpi=110)
    run = 0
    colors = {"total": "#4a5568", "down": "#c05621", "up": "#2b6cb0"}
    lo_all = []
    for k, (lab, v, kind) in enumerate(steps):
        if kind == "total":
            bottom, height = 0, v
            run = v
        else:
            bottom = run if v >= 0 else run + v
            height = abs(v)
            run += v
        ax.bar(k, height, bottom=bottom, width=0.56, color=colors[kind], edgecolor="white", linewidth=1.5)
        top = bottom + height
        lo_all.append(bottom)
        txt = f"{v:,.0f}" if kind == "total" else f"{v:+,.0f}"
        ax.text(k, top + 0.004 * b["raw"], txt, ha="center", va="bottom", fontsize=9, color="#1a202c")
        if k < len(steps) - 1:
            ax.plot([k + 0.28, k + 0.72], [run, run], color="#a0aec0", linewidth=0.8)
    ymin = min(b["raw"], b["conformed"]) - 3.2 * max(b["options"], b["superseded"], b["cusip_repaired"])
    ax.set_ylim(ymin, max(b["raw"], b["conformed"]) * 1.012)
    ax.set_xticks(range(len(steps)))
    ax.set_xticklabels([s[0] for s in steps], fontsize=8.5)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1e6:,.0f}m"))
    ax.set_ylabel("Shares (axis truncated)", fontsize=9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#edf2f7", linewidth=0.8)
    ax.set_axisbelow(True)
    net = b["conformed"] - b["raw"]
    ax.set_title(f"Our September institutional shares sit {abs(net) / 1e6:,.1f}m {'below' if net < 0 else 'above'} a straight sum of the SEC lines",
                 fontsize=11.5, loc="left", pad=38, fontweight="bold")
    ax.text(0, 1.02, "Put and call lines come out first, then the other lines in reports replaced by a later amendment;\nlines matched "
            "back to their CUSIPs come back in. Twelve watchlist names, period ended 30 Sep 2022.", transform=ax.transAxes, fontsize=9,
            color="#4a5568", ha="left", va="bottom")
    fig.text(0.01, 0.01, "Source: Form 13F reports for the period ended 30 Sep 2022, filed through 3 Feb 2023. "
             "Quillfield Research ownership desk.", fontsize=7.5, color="#4a5568")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write(g, golden_dir):
    os.makedirs(golden_dir, exist_ok=True)
    flag_file(g, os.path.join(golden_dir, "crowded_flags_2022q4.csv"))
    bridge_png(g, os.path.join(golden_dir, "sep_quarter_bridge.png"))
