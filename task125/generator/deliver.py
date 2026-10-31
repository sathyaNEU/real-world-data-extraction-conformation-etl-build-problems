"""figures.json, the two golden deliverables, submission.md and metadata.json, all from the cut pack."""
import datetime as dt
import io
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import docs as DC  # noqa: E402
import figs as F  # noqa: E402
import pack as P  # noqa: E402
import world as W  # noqa: E402

PDF = "sulfate_load_directives_2027.pdf"
XLSX = "umzimela_sulfate_loads_2025_26.xlsx"
NAMES = {r[0]: r[2] for r in W.RU}
ALLOC = {r[0]: r[5] for r in W.RU}


def compute(target):
    D = F.load(target)
    g = F.season_loads(D, "golden")
    p = F.season_loads(D, "point")
    a = F.ask_a(target)
    b = F.ask_b(target)
    return {
        "call": {"over": F.over_set(g), "within": sorted(c for c in g if c not in F.over_set(g))},
        "loads_t_per_day": {c: round(g[c], 3) for c in g},
        "loads_whole": {c: int(round(g[c])) for c in g},
        "point_loads_t_per_day": {c: round(p[c], 3) for c in p},
        "default_over": F.over_set(p),
        "dry_runs": [d.isoformat() for d in F.dry_runs(D)],
        "ask_a_tonnes": {"%s %s" % k: int(round(v, -1)) for k, v in sorted(a.items())},
        "ask_b_hours": {"%s %s" % k: v for k, v in sorted(b.items())},
        "allocations_t_per_day": {r[0]: r[5] for r in W.RU},
        "triggers_uS_cm": dict(P.TRIGGERS),
        "constants": {"mg_l_m3s_to_t_per_day": 0.0864, "so4_per_s": 2.996, "dry_runs": len(F.dry_runs(D))},
    }


def _chart(fig):
    codes = [r[0] for r in W.RU]
    loads = [fig["loads_t_per_day"][c] for c in codes]
    over = set(fig["call"]["over"])
    fg, ax = plt.subplots(figsize=(7.2, 3.6), dpi=150)
    xs = range(len(codes))
    ax.bar(xs, loads, color=["#b03a2e" if c in over else "#5b7c99" for c in codes], width=0.62, zorder=2)
    ax.scatter(xs, [ALLOC[c] for c in codes], marker="_", s=420, color="#1b1b1b", linewidths=2.2, zorder=3,
               label="allocation (Table 2)")
    ax.set_xticks(list(xs))
    ax.set_xticklabels(codes, fontsize=8)
    ax.set_ylabel("t/d of sulfate (as SO4)", fontsize=8.5)
    ax.tick_params(axis="y", labelsize=8)
    ax.set_title("Dry season 2026 (May to September runs): load past each unit's lower boundary", fontsize=9)
    ax.grid(axis="y", color="#dddddd", linewidth=0.6, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(fontsize=7.5, frameon=False, loc="upper left")
    buf = io.BytesIO()
    fg.tight_layout()
    fg.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fg)
    buf.seek(0)
    return buf


def brief(fig, path):
    st = DC._styles()
    over = fig["call"]["over"]
    rows = [("Unit", "Reach ends at", "Dry-season load, t/d", "Allocation, t/d", "Assessment")]
    for code, river, name, inflows, weir, alloc in W.RU:
        rows.append((code, "%s (%s)" % (name, weir), "%d" % fig["loads_whole"][code], "%.0f" % alloc,
                     "over: direct" if code in over else "within"))
    text = [
        Paragraph("Umzimela Catchment Management Agency, Water Resource Protection", st["s"]),
        Paragraph("Sulfate load directives for 2027", st["t"]),
        Paragraph("For the Chief Executive Officer. Assessment of the 2025/26 dry season under Schedule 3, section 3.",
                  st["s"]),
        Spacer(1, 4),
        Paragraph("Recommendation", st["h"]),
        Paragraph("Issue 2027 directives for the Khambule, Mzimela at Ngwelezane Drift, Ntsheketshe and Nyathi at "
                  "Mabhokweni resource units (KH1, MZ4, NT1 and NY2), and for no other unit. The Mzimela at "
                  "Esikhotheni and Nyathi at Siphethu units (MZ2, NY3) are within their allocations although their "
                  "boundary samples read high.", st["p"]),
        Paragraph("Why the boundary samples are not the loads", st["h"]),
        Paragraph("Four boundary weirs stand two to three kilometres below a mine stream's confluence, inside the "
                  "reach where the stream's water still runs along the bank it entered on. Esikhotheni and Siphethu "
                  "are on the mine stream's bank and sample its plume; Ngwelezane Drift and Mabhokweni are on the far "
                  "bank and sample the main river's water. On every dry-season run the loads those four samples give "
                  "fail to balance with what the inflows carry in and with what the next mixed weir downstream "
                  "carries out. Sulfate is conserved over these reaches, so each unit's load is the sum its inflows "
                  "carry in, each measured at its own weir where its water is mixed; the downstream weirs at "
                  "Mzimela Middle, Lower Mzimela and Lower Nyathi confirm it within one per cent.", st["p"]),
        Spacer(1, 3),
        Image(_chart(fig), width=168 * mm, height=84 * mm),
        Spacer(1, 3),
        DC._table(rows, [14, 70, 32, 26, 26], st),
    ]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm,
                            bottomMargin=16 * mm, title="Sulfate load directives for 2027", author="Umzimela CMA",
                            creator="Umzimela CMA", producer="Umzimela CMA", invariant=1)
    doc.build(text)
    DC.fix_dates(path, "D:20261012091500+02'00'", "D:20261013154000+02'00'")


def workbook(fig, path):
    pts = sorted({k.split()[0] for k in fig["ask_a_tonnes"]})
    a = [("Discharge point", "Q1 Oct-Dec 2025", "Q2 Jan-Mar 2026", "Q3 Apr-Jun 2026", "Q4 Jul-Sep 2026")]
    for pt in pts:
        a.append(tuple([pt] + [fig["ask_a_tonnes"]["%s %s" % (pt, q)] for q in ("Q1", "Q2", "Q3", "Q4")]))
    a += [(), ("Tonnes of sulfate as SO4 to the nearest ten; each month's metered volume at that month's composite.",)]
    months = ["2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04"]
    b = [tuple(["Logger", "Site", "Trigger uS/cm"] + months)]
    for lid, site in P.LOGGERS:
        b.append(tuple([lid, site, P.TRIGGERS[lid]] + [fig["ask_b_hours"]["%s %s" % (lid, m)] for m in months]))
    b += [(), ("Hours of the river's EC above the trigger in SAST months; fouling drift taken off linearly between "
               "service visits and telemetry gaps filled from the loggers' memory downloads.",)]
    c = [("Resource unit", "Dry-season load t/d", "Allocation t/d", "Assessment")]
    for code in [r[0] for r in W.RU]:
        c.append((code, fig["loads_whole"][code], ALLOC[code], "over" if code in fig["call"]["over"] else "within"))
    P._xlsx(path, [("Unit loads", c, [16, 20, 16, 14]), ("Discharges by quarter", a, [16, 16, 16, 16, 16]),
                   ("EC logger hours", b, [10, 8, 14, 10, 10, 10, 10, 10, 10])],
            "Umzimela CMA Water Resource Protection", dt.datetime(2026, 10, 12, 8, 55), dt.datetime(2026, 10, 13, 15, 32))


def write_all(target, golden, task):
    os.makedirs(golden, exist_ok=True)
    fig = compute(target)
    json.dump(fig, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json"), "w"), indent=1,
              sort_keys=True)
    brief(fig, os.path.join(golden, PDF))
    workbook(fig, os.path.join(golden, XLSX))
    return fig
