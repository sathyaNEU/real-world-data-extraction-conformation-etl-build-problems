"""braking_shift.png: each section direction's weekday-peak firm-braking rate in September and October 2026 beside its
expected rate in the January 2027 pick, AM and PM side by side, the four slot rows shaded. Network order, never
sorted on either rate."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

OBS, EXP = "#2a78d6", "#eb6834"
INK, INK2, GRID, BAND = "#0b0b0b", "#52514e", "#e4e3df", "#efeeea"


def draw(path, expected, observed, slate, sec):
    order = [(s, d) for s in sec["section"] for d in ("O", "I")]
    labels = ["%s %s" % (s, "outbound" if d == "O" else "inbound") for s, d in order]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "t210"})
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 8.2), sharey=True, dpi=150)
    y = np.arange(len(order))[::-1]
    hi = max(max(expected.values), max(observed.values)) * 1.08
    for ax, pk in zip(axes, ("AM", "PM")):
        ob = np.array([observed.get((f"{s}-{d}", pk), np.nan) for s, d in order])
        ex = np.array([expected.get((f"{s}-{d}", pk), np.nan) for s, d in order])
        for yi, (s, d) in zip(y, order):
            if (f"{s}-{d}", pk) in slate:
                ax.axhspan(yi - 0.5, yi + 0.5, color=BAND, zorder=0, lw=0)
                ax.text(hi * 0.995, yi, "slot", ha="right", va="center", fontsize=8, color=INK, fontweight="bold")
        ax.barh(y + 0.19, ob, height=0.34, color=OBS, label="Sep to Oct 2026, observed", zorder=2, edgecolor="white", linewidth=0.6)
        ax.barh(y - 0.19, ex, height=0.34, color=EXP, label="Jan to Feb 2027, expected", zorder=2, edgecolor="white", linewidth=0.6)
        ax.set_xlim(0, hi)
        ax.set_title("%s peak (%s)" % (pk, "06:30 to 08:59" if pk == "AM" else "16:00 to 18:29"), loc="left", fontsize=10,
                     color=INK, pad=6)
        ax.xaxis.grid(True, color=GRID, lw=0.7, zorder=1)
        ax.set_axisbelow(True)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color("#9b9a95")
        ax.tick_params(axis="both", colors=INK2, length=0)
        ax.set_xlabel("Firm brakes per 1,000 passes", color=INK2)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(labels)
    axes[0].set_ylim(-0.7, len(order) - 0.3)
    h, lab = axes[0].get_legend_handles_labels()
    fig.legend(h, lab, loc="upper right", ncol=2, frameon=False, fontsize=8.5, bbox_to_anchor=(0.985, 0.925))
    fig.suptitle("January's four slots are not this autumn's highest rows: J4 and J5 outbound (AM), F5 and F6 outbound (PM)",
                 x=0.012, y=0.985, ha="left", fontsize=11.5, color=INK, fontweight="bold")
    fig.text(0.012, 0.952, "Firm brakes per 1,000 passes by section direction and weekday peak. Observed: 1 Sep to 31 Oct 2026. "
             "Expected: the January 2027 pick (4 Jan to 26 Feb)\nat its scheduled passes in normal weather. Shaded rows take the "
             "four restricted-speed slots.", fontsize=8.2, color=INK2, va="top", linespacing=1.35)
    fig.text(0.012, 0.012, "Source: ART event data recorder export and AVL section-pass log (observed); January 2027 pick "
             "timetable and ASH 1991 to 2020 normals (expected). Peaks by section entry time, Mountain local time.",
             fontsize=7.4, color=INK2)
    fig.subplots_adjust(left=0.12, right=0.985, top=0.87, bottom=0.085, wspace=0.06)
    fig.savefig(path, dpi=150, metadata={"Software": None}, facecolor="white")
    plt.close(fig)
