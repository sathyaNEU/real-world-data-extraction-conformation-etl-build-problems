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
                    "read_health_pct": round(float(sc[r]["rh"]), 2),
                    "standard_error_pct": round(float(sc[r]["se"]), 2),
                    "lower_limit_pct": round(float(sc[r]["lcl"]), 2),
                    "vs_limit_pct": round(float(sc[r]["rh"] - sc[r]["lcl"]), 2),
                    "alert": "FIRE" if sc[r]["fire"] else "HOLD"} for r in order],
        "wave8_moves_under_this_call": {k: int(v) for k, v in sorted(g["wave8"].items())},
        "settlement_substitution_load_installations": int(g["load"]),
        "notes": ["assessed installations ran the build from 00:00 Mon 5 Oct to 24:00 Sun 11 Oct AEST with no meter change (MDS-STD-114 3.7)",
                  "reads counted as actual in the latest MDM delivery received before 06:00 AEST the day after each read date (3.5)",
                  "standard errors taken over the comms nodes (collectors, access points) the assessed installations report "
                  "through, since a node that misses a night's collection takes that day from the installations behind it together",
                  "wave 8 counts take each meter once across the schedule's two batches (cut 1 Oct, batch B rebuilt 9 Oct), net of meters already on the target image or no longer in service",
                  "substitution load: installations whose in-service meter runs a build the alert fires on (6.1)"],
        "raised_by": "Metering Data Services",
        "raised_local": "2026-10-12T17:05:00+11:00",
    }


INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
HOLD_C, FIRE_C = "#2a78d6", "#d03b3b"


def chart(g, path):
    sc = g["scorecard"]
    order = ordered(sc)
    fire = [r for r in order if sc[r]["fire"]]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": MUTED,
                         "xtick.color": INK2, "ytick.color": INK, "axes.labelcolor": INK2})
    fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    lo = 96.0
    ys = list(range(len(order)))[::-1]
    for y, r in zip(ys, order):
        v = sc[r]
        col = FIRE_C if v["fire"] else HOLD_C
        tick = max(v["lcl"], lo + 0.06)
        ax.plot([tick, v["rh"]], [y, y], color=col, lw=2, alpha=0.45, solid_capstyle="round", zorder=1)
        if v["lcl"] >= lo + 0.06:
            ax.plot([v["lcl"]], [y], marker="|", markersize=15, mew=2.4, color=INK2, zorder=2)
            ax.annotate("limit %.2f" % v["lcl"], (v["lcl"], y), xytext=(-5, -13), textcoords="offset points",
                        fontsize=7.5, color=INK2, ha="right" if v["lcl"] > lo + 0.9 else "left")
        else:
            ax.plot([lo + 0.06], [y], marker="<", markersize=7, color=INK2, zorder=2)
            ax.annotate("limit %.2f (off scale)" % v["lcl"], (lo + 0.06, y), xytext=(6, -13), textcoords="offset points",
                        fontsize=7.5, color=INK2, ha="left")
        ax.plot([v["rh"]], [y], marker="o", markersize=8.5, color=col, markeredgecolor=SURFACE, mew=2, zorder=3)
        tight = v["lcl"] > v["rh"] and v["lcl"] - v["rh"] < 0.45
        ax.annotate("%.2f%%" % v["rh"], (v["rh"], y), xytext=(-7, 6) if tight else (7, 6), textcoords="offset points",
                    fontsize=8.5, color=INK, ha="right" if tight else "left")
        if v["fire"]:
            ax.plot([100.05], [y], marker="o", markersize=7, color=FIRE_C, zorder=3, clip_on=False)
            ax.annotate("FIRE", (100.05, y), xytext=(8, 0), textcoords="offset points", fontsize=8.5,
                        fontweight="bold", color=INK, va="center", annotation_clip=False)
    ax.axvline(99.50, color=INK, ls=(0, (4, 3)), lw=1)
    ax.annotate("reference 99.50%", (99.50, len(order) - 0.45), xytext=(5, 0), textcoords="offset points",
                fontsize=8, color=INK)
    ax.set_yticks(ys)
    ax.set_yticklabels(order)
    ax.set_xlim(lo, 100.25)
    ax.set_ylim(-0.8, len(order) - 0.2)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: "%.1f%%" % x))
    ax.set_xlabel("read health: mean over assessed installations of expected interval reads held as actual at the 06:00 AEST cut-off",
                  fontsize=8)
    names = ", ".join(fire[:-1]) + " and " + fire[-1] if len(fire) > 1 else fire[0]
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
    fig.suptitle("Read-health alert fires on %s; the other %s builds hold for Wave 8" % (names, words[len(order) - len(fire)]),
                 fontsize=11, x=0.015, ha="left", fontweight="bold", color=INK)
    ax.set_title("Week of 5 to 11 Oct 2026 (AEST). Dot: read health. Tick: lower limit, the reference less three standard "
                 "errors. Furthest below its limit at the top.", fontsize=7.5, color=INK2, loc="left")
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
    text = re.sub(r'("[a-z_]*_pct": )(-?\d+\.\d+)', lambda m: m.group(1) + "%.2f" % float(m.group(2)), text)
    with open(os.path.join(out, "wave8_read_health_alerts.json"), "w") as fh:
        fh.write(text + "\n")
    chart(g, os.path.join(out, "read_health_by_build_wk41.png"))
    return g


if __name__ == "__main__":
    main()
