"""task468 architecture 6: the golden review memo (PDF with its chart) and the figures workbook."""
import datetime as dt
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import wio  # noqa: E402

MEMO = "trade_waste_cod_review_2026.pdf"
BOOK = "trade_waste_figures_2026.xlsx"
SHORT = {"Coolabah Olives Pty Ltd": "Coolabah Olives", "Tallowood Tannery Pty Ltd": "Tallowood Tannery",
         "Mt Edwin Cheese Company": "Mt Edwin Cheese", "Glenbrae Meats Pty Ltd": "Glenbrae Meats",
         "Riverbend Poultry": "Riverbend Poultry", "Sunvale Dairy Ingredients": "Sunvale Dairy",
         "Hartley Street Brewing Co": "Hartley St Brewing", "Bellbird Beverages": "Bellbird Beverages",
         "Kingfisher Linen Services": "Kingfisher Linen", "Golden Crumb Bakeries": "Golden Crumb",
         "Paddock Fresh Vegetables": "Paddock Fresh", "Wattle Pet Foods": "Wattle Pet Foods"}


def chart(R, path):
    custs = sorted(R["D"]["custs"], key=lambda c: -R["cod"][c] / R["D"]["limit"][c])
    share = [100 * R["cod"][c] / R["D"]["limit"][c] for c in custs]
    fig, ax = plt.subplots(figsize=(7.2, 3.9), dpi=150)
    cols = ["#b5452f" if c in R["over"] else "#7d93a8" for c in custs]
    ax.barh(range(len(custs)), share, color=cols, height=0.62)
    ax.axvline(100, color="#222222", lw=1.0, ls="--")
    ax.text(100.8, len(custs) - 0.6, "agreement limit", fontsize=7.5, va="top")
    ax.set_yticks(range(len(custs)))
    ax.set_yticklabels([SHORT[c] for c in custs], fontsize=7.6)
    ax.invert_yaxis()
    ax.set_xlabel("2026 COD mass as a share of the agreement's annual limit (%)", fontsize=8)
    ax.tick_params(axis="x", labelsize=7.5)
    for i, v in enumerate(share):
        ax.text(v + 1, i, "%.0f%%" % v, va="center", fontsize=6.8)
    ax.set_xlim(0, max(share) * 1.13)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def write_memo(R, path, png):
    b = R["fit"]
    over = [SHORT[c] for c in R["over"]]
    rows = [["Customer", "2026 COD (t)", "Limit (t)", "Share of limit", "Exceeded"]]
    for c in sorted(R["D"]["custs"], key=lambda c: SHORT[c]):
        lim = R["D"]["limit"][c]
        rows.append([SHORT[c], "%.1f" % R["cod"][c], ("%.1f" % lim) if lim < 100 else "%.0f" % lim,
                     "%.0f%%" % (100 * R["cod"][c] / lim), "yes" if c in R["over"] else "no"])
    blocks = [
        ("s", "Glenbrae Water, Trade Waste Unit. Prepared 2 February 2027 for the 2026 annual return."),
        ("t", "2026 COD review: customers over their agreement limits"),
        ("p", "<b>%s exceeded their agreements' 2026 COD limits</b> and go on the annual return with a notice of "
              "agreement review. No other customer exceeded its limit." % (", ".join(over[:-1]) + " and " + over[-1])),
        ("p", "From 2 February the laboratory reported TOC instead of COD. Each TOC sample is converted to the "
              "dichromate COD it would have read through the %d samples tested both ways between October and "
              "December 2025, on the sample's own TOC and chloride: COD = %.1f + %.3f x TOC + %.4f x chloride "
              "(mg/L). The dichromate test also oxidises chloride, which TOC does not read, so the brine customers "
              "cannot share one COD to TOC factor, and their chloride changed after the parallel run: Mt Edwin "
              "Cheese's fell when its brine recovery started in May, Tallowood Tannery's rose from March." %
              (R["n_parallel"], b[0], b[1], b[2])),
        ("table", (rows, [52, 30, 26, 30, 22])),
        ("image", (png, 168, 91)),
        ("s", "Masses follow the policy: the year's metered volume (both meters where one was exchanged) times the "
              "volume-weighted mean concentration of the year's compliance samples, January on the measured COD."),
    ]
    wio.pdf(path, blocks, "2026 COD review", "Trade Waste Unit", "D:20270202101500+10'00'",
            "D:20270202143000+10'00'", "Glenbrae Water  |  Trade Waste Unit  |  2026 COD review")


def write_book(R, path):
    q = [["Customer", "Q1 2026 (kL)", "Q2 2026 (kL)", "Q3 2026 (kL)", "Q4 2026 (kL)", "2026 (kL)"]]
    s = [["Customer", "Suspended solids discharged in 2026 (t)"]]
    for c in R["D"]["custs"]:
        qs = [int(round(x)) for x in R["vol"][c]["q"]]
        q.append([c] + qs + [sum(qs)])
        s.append([c, round(R["ss"][c], 1)])
    wio.xlsx(path, [("Volumes", q, [1], {}), ("Suspended solids", s, [1], {"B": "0.0"})], "Trade Waste Unit",
             dt.datetime(2027, 1, 27, 9, 5), dt.datetime(2027, 2, 2, 4, 20), widths=[30, 14, 14, 14, 14, 14],
             company="Glenbrae Water")


def write_all(R, golden):
    os.makedirs(golden, exist_ok=True)
    png = os.path.join(golden, ".chart.png")
    chart(R, png)
    write_memo(R, os.path.join(golden, MEMO), png)
    os.remove(png)
    write_book(R, os.path.join(golden, BOOK))
