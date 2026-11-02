"""The golden deliverable (kwikstaart_leerlingenprognose_2027-2029.docx) and generator/figures.json, from analysis.py's
figures on the cut pack."""
import datetime as dt
import io
import json
import os

import analysis as A
import params as P

BOOK = "kwikstaart_leerlingenprognose_2027-2029.docx"
STAMP = (2026, 10, 19, 16, 40, 0)
WD = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def owed(F, M):
    f = dict(F)
    r = M["routes"]
    f["pooled_2029"] = round(r["pooled"][2029], 1)
    f["by_wijk_2029"] = round(r["by_wijk"][2029], 1)
    f["trend_2029"] = round(r["trend"][2029], 1)
    f["everyone_2028"] = round(r["everyone"][2028], 1)
    f["intake_total"] = M["tot"][True][0] + M["tot"][False][0]
    f["intake_entered_total"] = M["tot"][True][1] + M["tot"][False][1]
    f["future_total"] = sum(F["future_children"].values())
    f["future_sibling_total"] = sum(F["future_sibling"].values())
    f["excess_2029_whole"] = int(round(F["excess_2029_exact"]))
    f["under_2028_whole"] = int(round(M["C"] - r["golden"][2028]))
    f["rounding_units"] = [10, 1000]
    f["sections"] = "2.3 3.1 3.2 3.3 3.4 3.5"
    f["bso_total"] = sum(F["bso"].values())
    return f


def chart_png(F, M):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    years = ["2027-28", "2028-29", "2029-30"]
    vals = [M["routes"]["golden"][y] for y in A.FORE]
    fig, ax = plt.subplots(figsize=(6.0, 3.0), dpi=150)
    bars = ax.bar(years, vals, color="#2a78d6", width=0.55, label="Forecast pupils")
    ax.axhline(M["C"], color="#eb6834", linewidth=2, label="Capacity, %d pupils" % M["C"])
    for b_, v in zip(bars, vals):
        ax.text(b_.get_x() + b_.get_width() / 2, v - 28, "%d" % A.rnd(v, 10), ha="center", va="top", color="white",
                fontsize=9, fontweight="bold")
    ax.set_ylim(0, 700)
    ax.set_ylabel("Pupils on 1 October")
    ax.set_title("De Kwikstaart exceeds its capacity at the 2029-30 count", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color="#e3e2de")
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def memo(F, M, path):
    from docx import Document
    from docx.shared import Pt, Cm
    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(10.5)
    C = M["C"]
    g = M["routes"]["golden"]
    doc.add_heading("De Kwikstaart exceeds its capacity at the 1 October 2029 count", level=1)
    doc.add_paragraph("To: the supervisory council, %s. From: %s, bureau Huisvesting. 19 October 2026. "
                      "Subject: pupil forecast for the accommodation request 2028 (PV-2)." % (P.BOARD, P.PEOPLE["planner"]))
    doc.add_paragraph("On the board's procedure PV-2 the school's roll reaches %d pupils at the count of 1 October 2029, "
                      "%d above the %d places in the accommodation plan; it stays within them in 2027 (%d) and 2028 (%d). "
                      "The request should ask for extra accommodation from the 2029-30 school year." %
                      (A.rnd(g[2029], 10), F["excess_2029_whole"], C, A.rnd(g[2027], 10), A.rnd(g[2028], 10)))
    t = doc.add_table(rows=1, cols=4)
    t.style = "Light Grid Accent 1"
    for c, h in zip(t.rows[0].cells, ["1 October count", "Forecast pupils", "Capacity", "Result"]):
        c.text = h
    for y, lab in zip(A.FORE, ["2027-28", "2028-29", "2029-30"]):
        r = t.add_row().cells
        r[0].text, r[1].text, r[2].text = lab, "%d" % A.rnd(g[y], 10), "%d" % C
        r[3].text = "short" if g[y] > C else "within"
    doc.add_paragraph("Pupils to the nearest 10; the test compares the unrounded forecast (%.1f, %.1f and %.1f) with the "
                      "capacity." % (g[2027], g[2028], g[2029]))
    doc.add_picture(io.BytesIO(chart_png(F, M)), width=Cm(15))
    doc.add_heading("What the forecast rests on", level=2)
    doc.add_paragraph("Of the last five intakes' catchment children, %d had a brother or sister from the same household on "
                      "the roll at their first count and %d of them entered (%d per cent); of the %d without one, %d entered "
                      "(%d per cent). The coming counts' children are counted at their own circumstance's share:" %
                      (M["tot"][True][0], M["tot"][True][1], F["rate_sibling_pct"], M["tot"][False][0],
                       M["tot"][False][1], F["rate_other_pct"]))
    t2 = doc.add_table(rows=1, cols=3)
    t2.style = "Light Grid Accent 1"
    for c, h in zip(t2.rows[0].cells, ["First count", "Catchment children", "With a brother or sister on the roll"]):
        c.text = h
    for y, lab in zip(A.FORE, ["1 October 2027", "1 October 2028", "1 October 2029"]):
        r = t2.add_row().cells
        r[0].text, r[1].text, r[2].text = lab, str(F["future_children"][str(y)]), str(F["future_sibling"][str(y)])
    doc.add_paragraph("At the pooled share of the last five intakes (%d per cent) the roll would stay within the capacity "
                      "(%.0f at 2029-30); the coming cohorts hold far more children with a brother or sister on the roll "
                      "than the last five intakes did." % (F["rate_pooled_pct"], M["routes"]["pooled"][2029]))
    doc.add_heading("Use of the buildings", level=2)
    doc.add_paragraph("Gas, hoofdgebouw and dependance together, school years from 1 August (m3, nearest 1,000): "
                      "2023-24 %s; 2024-25 %s; 2025-26 %s." % tuple("{:,}".format(F["gas_m3"][str(s)]) for s in (2023, 2024, 2025)))
    doc.add_paragraph("After-school care in the dependance, attendances of De Kwikstaart pupils in October 2026: " +
                      "; ".join("%s %d" % (WD[k], F["bso"][str(k)]) for k in range(5)) + ".")
    cp = doc.core_properties
    cp.author = cp.last_modified_by = P.PEOPLE["planner"]
    cp.title = "Leerlingenprognose De Kwikstaart 2027-2029"
    cp.created = cp.modified = dt.datetime(2026, 10, 19, 16, 40)
    cp.revision = 2
    cp.comments = ""
    doc.save(path)
    from pack import normalise_zip
    normalise_zip(path, "2026-10-19T14:40:00Z", app="Microsoft Office Word")


def write_all(target, golden_dir, gen_dir):
    os.makedirs(golden_dir, exist_ok=True)
    os.makedirs(gen_dir, exist_ok=True)
    F, M = A.figures(target)
    memo(F, M, os.path.join(golden_dir, BOOK))
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(owed(F, M), fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
    return F, M
