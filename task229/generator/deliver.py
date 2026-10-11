"""Write the golden deliverables into task229/golden/ from the shipped bundle alone."""
import json
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G

TASK = os.path.dirname(HERE)


def ordered(sc):
    return sorted(sc, key=lambda r: sc[r]["rh"] - sc[r]["lcl"])


def payload(g):
    sc = g["scorecard"]
    order = ordered(sc)
    fire = [r for r in order if sc[r]["fire"]]
    hold = [r for r in order if not sc[r]["fire"]]
    return {
        "alert_id": "RHG-2026-W41",
        "alert": "read-health gate (MDS-STD-114 r3)",
        "assessment_week": {"from": "2026-10-05", "to": "2026-10-11", "clock": "market time (AEST)"},
        "for_wave": "Wave 8, nights of 13 and 14 October 2026",
        "fire": fire,
        "hold": hold,
        "reference_read_health_pct": 99.50,
        "builds": [{"release": r,
                    "assessed_installations": int(sc[r]["n"]),
                    "read_health_pct": round(float(sc[r]["rh"]), 2),
                    "lower_limit_pct": round(float(sc[r]["lcl"]), 2),
                    "alert": "FIRE" if sc[r]["fire"] else "HOLD"} for r in order],
        "wave8_schedule_moves_if_it_goes_ahead": {k: int(v) for k, v in sorted(g["wave8"].items())},
        "wave7_moves_this_week": [{"onto": k, "installations_moved": int(v["installations"]),
                                   "interval_reads_missing_at_cutoff_on_move_day": int(v["missing"])}
                                  for k, v in sorted(g["wave7"].items())],
        "notes": ["assessed installations ran the build from 00:00 Mon 5 Oct to 24:00 Sun 11 Oct AEST with no meter change (MDS-STD-114 3.7)",
                  "reads counted as actual in the latest MDM delivery received before 06:00 AEST the day after each read date (3.5)",
                  "wave 8 counts follow the schedule as cut on 1 Oct, net of meters already on the target image or no longer in service"],
        "raised_by": "Metering Data Services",
        "raised_local": "2026-10-12T17:05:00+11:00",
    }


INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
HOLD_C, FIRE_C = "#2a78d6", "#d03b3b"


def chart(g, path):
    sc = g["scorecard"]
    order = ordered(sc)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": MUTED,
                         "xtick.color": INK2, "ytick.color": INK, "axes.labelcolor": INK2})
    fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    ys = list(range(len(order)))[::-1]
    for y, r in zip(ys, order):
        v = sc[r]
        col = FIRE_C if v["fire"] else HOLD_C
        ax.plot([v["lcl"], v["rh"]], [y, y], color=col, lw=2, alpha=0.45, solid_capstyle="round", zorder=1)
        ax.plot([v["lcl"]], [y], marker="|", markersize=15, mew=2.4, color=INK2, zorder=2)
        ax.plot([v["rh"]], [y], marker="o", markersize=8.5, color=col, markeredgecolor=SURFACE, mew=2, zorder=3)
        ax.annotate("%.2f%%" % v["rh"], (v["rh"], y), xytext=(7, 6), textcoords="offset points", fontsize=8.5, color=INK)
        ax.annotate("limit %.2f" % v["lcl"], (v["lcl"], y), xytext=(-5, -13), textcoords="offset points",
                    fontsize=7.5, color=INK2, ha="right")
        if v["fire"]:
            ax.plot([100.05], [y], marker="o", markersize=7, color=FIRE_C, zorder=3, clip_on=False)
            ax.annotate("FIRE", (100.05, y), xytext=(8, 0), textcoords="offset points", fontsize=8.5,
                        fontweight="bold", color=INK, va="center", annotation_clip=False)
    ax.axvline(99.50, color=INK, ls=(0, (4, 3)), lw=1)
    ax.annotate("reference 99.50%", (99.50, len(order) - 0.45), xytext=(5, 0), textcoords="offset points",
                fontsize=8, color=INK)
    ax.set_yticks(ys)
    ax.set_yticklabels(["%s  (%s inst.)" % (r, format(sc[r]["n"], ",")) for r in order])
    ax.set_xlim(96.4, 100.25)
    ax.set_ylim(-0.8, len(order) - 0.2)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: "%.1f%%" % x))
    ax.set_xlabel("read health of the average assessed installation (expected interval reads held as actual at the 06:00 AEST cut-off)",
                  fontsize=8)
    fig.suptitle("Read-health alert fires on EM3.10.9, EM3.12.1 and PX5.2.7; the other five builds hold for Wave 8",
                 fontsize=11, x=0.015, ha="left", fontweight="bold", color=INK)
    ax.set_title("Week of 5 to 11 Oct 2026 (AEST). Dot: read health. Tick: lower limit (reference less three "
                 "standard errors). Furthest below the limit at the top.", fontsize=7.5, color=INK2, loc="left")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None}, facecolor=SURFACE)
    plt.close(fig)


def main(target=None, out=None):
    target = target or os.path.join(TASK, "target")
    out = out or os.path.join(TASK, "golden")
    os.makedirs(out, exist_ok=True)
    D, g = G.solve(target)
    text = json.dumps(payload(g), indent=2)
    # percentages carry two decimals in the payload the router reads
    text = re.sub(r'("[a-z_]*_pct": )(\d+\.\d+)', lambda m: m.group(1) + "%.2f" % float(m.group(2)), text)
    with open(os.path.join(out, "wave8_read_health_alerts.json"), "w") as fh:
        fh.write(text + "\n")
    chart(g, os.path.join(out, "read_health_by_build_wk41.png"))
    return g


if __name__ == "__main__":
    main()
