"""Write the golden deliverables into task229/golden/ from the shipped bundle alone."""
import json
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
        "raised_by": "Metering Data Services",
        "raised_local": "2026-10-12T17:05:00+11:00",
    }


def chart(g, path):
    sc = g["scorecard"]
    order = ordered(sc)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "229"})
    fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=150)
    ys = list(range(len(order)))[::-1]
    for y, r in zip(ys, order):
        v = sc[r]
        col = "#c0392b" if v["fire"] else "#2c6e91"
        ax.plot([v["lcl"], v["rh"]], [y, y], color=col, lw=1.2, alpha=0.6, zorder=1)
        ax.plot([v["lcl"]], [y], marker="|", markersize=14, mew=2.2, color="#555555", zorder=2)
        ax.plot([v["rh"]], [y], marker="o", markersize=7, color=col, zorder=3)
        lab = "%.2f%%" % v["rh"]
        ax.annotate(lab, (v["rh"], y), xytext=(6, 6), textcoords="offset points", fontsize=8, color=col)
        ax.annotate("limit %.2f" % v["lcl"], (v["lcl"], y), xytext=(-4, -12), textcoords="offset points",
                    fontsize=7, color="#555555", ha="right")
        if v["fire"]:
            ax.annotate("FIRE", (99.98, y), fontsize=8.5, fontweight="bold", color="#c0392b", va="center")
    ax.axvline(99.50, color="#333333", ls="--", lw=1)
    ax.annotate("reference 99.50%", (99.50, len(order) - 0.45), xytext=(4, 0), textcoords="offset points", fontsize=8)
    ax.set_yticks(ys)
    ax.set_yticklabels(["%s  (n=%d)" % (r, sc[r]["n"]) for r in order])
    ax.set_xlim(96.4, 100.3)
    ax.set_ylim(-0.8, len(order) - 0.2)
    ax.set_xlabel("read health of the average assessed installation, % of expected interval reads held at the 06:00 cut-off")
    fig.suptitle("Read-health alert fires on EM3.10.9, EM3.12.1 and PX5.2.7; the other five builds hold for Wave 8",
                 fontsize=11, x=0.015, ha="left", fontweight="bold")
    ax.set_title("Week of 5 to 11 Oct 2026 (AEST). Dot: read health. Tick: lower limit (reference less three "
                 "standard errors). Furthest below the limit at the top.", fontsize=7.5, color="#444444", loc="left")
    ax.grid(axis="x", color="#e5e5e5")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
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
