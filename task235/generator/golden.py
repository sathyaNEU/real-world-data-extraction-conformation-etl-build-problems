"""The golden deliverables: tracking_loss_alerts_2026-11-09.csv and tracking_loss_by_build_2026-11-09.png."""
import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = "tracking_loss_alerts_2026-11-09.csv"
PNG = "tracking_loss_by_build_2026-11-09.png"
RED = "#B03A2E"
GREY = "#8EA3B9"
FIELDS = ["platform", "version", "build_number", "alert", "paying_players", "gross_bookings_per_paying_player_eur"]


def alert_list(path, A):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(FIELDS)
        for r in A["builds"]:
            w.writerow([r["platform"], r["version"], r["build_number"], "yes" if r["alert"] else "no", r["players"],
                        "%.2f" % r["per_player"]])


def chart(path, A):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(figsize=(9.0, 6.4), dpi=150)
    rows = A["builds"][::-1]
    y, ypos, prev = [], 0.0, None
    for r in rows:
        if prev is not None and r["platform"] != prev:
            ypos += 0.7
        y.append(ypos); ypos += 1
        prev = r["platform"]
    vals = [r["loss_pct_raw"] for r in rows]
    ax.barh(y, vals, color=[RED if r["alert"] else GREY for r in rows], height=0.7, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(["%s %s  (%s)" % ("iOS" if r["platform"] == "ios" else "Android", r["version"], r["build_number"])
                        for r in rows])
    ax.axvline(2.0, color=RED, linestyle="--", linewidth=1.2, zorder=4)
    ax.text(2.07, y[-1] + 0.75, "alert line 2%", color=RED, fontsize=8.5, va="bottom")
    for yy, r, v in zip(y, rows, vals):
        if not r["alert"]:
            continue
        note = ("%d of %s purchases lost, none still on a phone" % (r["lost"], format(r["n"], ","))
                if not r["pending"] else
                "%d of %d lost, %d still on phones: %.2f%% even if all %d arrive"
                % (r["lost"], r["n"], r["pending"], r["lo_pct"], r["pending"]))
        ax.text(v + 0.08, yy, note, va="center", ha="left", fontsize=8, color=RED, fontweight="bold")
    top = max(vals)
    ax.set_xlim(0, top * 1.9)
    ticks = [t for t in range(0, int(top) + 2)]
    ax.set_xticks(ticks)
    ax.set_xticklabels(["%d%%" % t for t in ticks])
    ax.set_ylim(-0.8, y[-1] + 1.6)
    ax.grid(axis="x", color="#E5E5E5", zorder=0)
    ax.set_xlabel("Tracking loss, per cent of the build's purchases whose purchase_completed event never reaches the warehouse")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_bounds(0, ticks[-1])
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.text(0.015, 0.985, "Alert Android 7.41.0 and iOS 7.42.0; the other ten builds stay well under the 2% line",
             fontsize=12, fontweight="bold", va="top")
    fig.text(0.015, 0.948, "Purchases made 12 October to 8 November 2026 (Irish dates), run of Monday 9 November, KC-DQ-04. "
                           "A missing event is lost once the\nphone that made the purchase has opened the game again; one still on a phone "
                           "counts at the share of the build's events, still on a phone at its next opening, that never arrived.",
             fontsize=8.2, va="top", color="#333333", linespacing=1.4)
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write(golden_dir, A):
    os.makedirs(golden_dir, exist_ok=True)
    alert_list(os.path.join(golden_dir, CSV), A)
    chart(os.path.join(golden_dir, PNG), A)
