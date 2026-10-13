"""The golden deliverables, computed from the shipped files only: restoration_slate_2027.docx (the water quality
program's memo to the technical committee: the three tributaries, each tributary's water-year 2026 load against its
allocation, a chart, how the loads were built) and tributary_loads_wy2026.csv (each tributary, whether it gets a 2027
project, its upstream permitted wastewater phosphorus and its 2026 cover crop acres); and figures.json, every figure
the write-up states."""
import collections
import io
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import calc as C        # noqa: E402
import pack as P        # noqa: E402
import world as W       # noqa: E402

DOCX = "restoration_slate_2027.docx"
CSV = "tributary_loads_wy2026.csv"
FULL = C.ROUTES[:4]       # corrected rating curves on the full record


def schedule(target):
    """Schedule 1 of the agreement: each tributary's allocation"""
    from pypdf import PdfReader
    txt = "\n".join(p.extract_text() for p in PdfReader(os.path.join(target, P.FILES["agreement"])).pages)
    A = {}
    for t in W.TRIBS:
        m = re.search(re.escape(t[1]) + r"\s+" + re.escape(t[2]) + r"\s+([\d,]+)", txt)
        A[t[1]] = float(m.group(1).replace(",", ""))
    return A


def k10(v):
    return int(round(v / 10.0)) * 10


def floor10(v):
    return int(np.floor(v / 10.0)) * 10


def ceil10(v):
    return int(np.ceil(v / 10.0)) * 10


def compute(target):
    L = C.load(target)
    A = schedule(target)
    R, info = C.route_loads(L)
    X = dict(L=L, A=A, R=R, info=info)
    X["slates"] = {nm: C.slate(R[nm], A)[0] for nm in C.ROUTES}
    X["call"], X["excess"] = C.slate(R[C.GOLD], A)
    X["ww"] = C.ask_wastewater(L)
    X["cover"] = C.ask_cover(L)
    return X


def figures(X):
    F = collections.OrderedDict()
    A, R = X["A"], X["R"]
    G = R[C.GOLD]
    F["call"] = list(X["call"])
    F["routes"] = collections.OrderedDict((nm, X["slates"][nm]) for nm in C.ROUTES)
    F["default_slate"] = X["slates"][C.DEFAULT]
    F["load_kg"] = collections.OrderedDict((n, k10(G[n])) for n in W.NAME.values())
    F["allocation_kg"] = collections.OrderedDict((n, int(A[n])) for n in W.NAME.values())
    F["excess_kg"] = collections.OrderedDict((n, k10(G[n] - A[n])) for n in W.NAME.values())
    F["excess_range_full_record_kg"] = collections.OrderedDict(
        (n, [floor10(min(R[k][n] for k in FULL) - A[n]), ceil10(max(R[k][n] for k in FULL) - A[n])]) for n in W.NAME.values())
    F["load_range_full_record_kg"] = collections.OrderedDict(
        (n, [floor10(min(R[k][n] for k in FULL)), ceil10(max(R[k][n] for k in FULL))]) for n in W.NAME.values())
    F["default_below_kg"] = collections.OrderedDict(
        (n, k10(A[n] - R[C.DEFAULT][n])) for n in W.NAME.values() if R[C.DEFAULT][n] < A[n] and n in X["call"])
    F["excess_by_route_kg"] = collections.OrderedDict((nm, collections.OrderedDict((n, k10(R[nm][n] - A[n])) for n in W.NAME.values()))
                                                      for nm in C.ROUTES)
    F["slope"] = collections.OrderedDict((n, round(float(X["info"][n]["beta"][1]), 2)) for n in W.NAME.values())
    F["n_samples"] = collections.OrderedDict((n, int(X["info"][n]["n"])) for n in W.NAME.values())
    F["smearing"] = collections.OrderedDict((n, round(float(X["info"][n]["smear"]), 3)) for n in W.NAME.values())
    F["wastewater_kg"] = collections.OrderedDict((n, round(X["ww"][n], 1)) for n in W.NAME.values())
    F["wastewater_stated"] = collections.OrderedDict((n, k10(X["ww"][n])) for n in W.NAME.values())
    F["cover_acres"] = collections.OrderedDict((n, round(X["cover"][n], 1)) for n in W.NAME.values())
    F["cover_stated"] = collections.OrderedDict((n, k10(X["cover"][n])) for n in W.NAME.values())
    tot_g = sum(G.values())
    F["basin_load_kg"] = k10(tot_g)
    F["default_vs_golden_pct"] = collections.OrderedDict(
        (n, round(100 * (R[C.DEFAULT][n] / G[n] - 1), 1)) for n in W.NAME.values())
    F["record"] = {"from": "1 October 2023", "first_water_year": 2024}
    F["clauses"] = ["1.4", "2.2", "3.1", "4.1"]
    s26 = C.tp_samples(X["L"])
    F["samples_wy2026_mean"] = int(round(np.mean([sum(W.WY26_START <= d <= W.WY_END for d, c in s26[n]) for n in W.NAME.values()])))
    # the forcing evidence: the top tenth of each station's water year 2026 days by discharge, their share of the
    # golden load and of the water year's samples
    L = X["L"]
    s, q = C.tp_samples(L), C.daily_q(L)
    tl, ts = collections.OrderedDict(), collections.OrderedDict()
    for n in W.NAME.values():
        qd = np.array([q[n][d] for d in C.WY26])
        b = X["info"][n]["beta"]
        a = np.array([2 * np.pi * d.timetuple().tm_yday / 365.25 for d in C.WY26])
        ld = np.exp(b[0] + b[1] * np.log(qd) + b[2] * np.sin(a) + b[3] * np.cos(a)) * qd
        top = qd > np.quantile(qd, 0.9)
        s26 = [d for d, c in s[n] if W.WY26_START <= d <= W.WY_END]
        tl[n] = round(100 * float(ld[top].sum() / ld.sum()))
        ts[n] = round(100 * float(np.mean([q[n][d] > np.quantile(qd, 0.9) for d in s26])))
    F["top_tenth_load_pct"] = tl
    F["top_tenth_samples_pct"] = ts
    return F


# ------------------------------------------------------------------------------------------------------- chart
def chart_png(X, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "DejaVu Sans"
    A, G = X["A"], X["R"][C.GOLD]
    order = sorted(W.NAME.values(), key=lambda n: G[n] - A[n])
    fund = set(X["call"])
    fig, ax = plt.subplots(figsize=(7.4, 4.6), dpi=150)
    y = np.arange(len(order))
    ax.barh(y, [G[n] / 1000 for n in order], height=0.6, color=["#1f5f7a" if n in fund else "#9fb6c3" for n in order],
            label="Water year 2026 load")
    ax.scatter([A[n] / 1000 for n in order], y, marker="|", s=420, color="#b23b1e", linewidths=2.2, zorder=3,
               label="Allocation (Schedule 1)")
    for i, n in enumerate(order):
        ex = G[n] - A[n]
        ax.text(max(G[n], A[n]) / 1000 + 0.25, i, ("+%s kg" % "{:,}".format(k10(ex))) if ex > 0 else ("%s kg" % "{:,}".format(k10(ex))),
                va="center", fontsize=7.6, color="#202326")
    ax.set_yticks(y)
    ax.set_yticklabels(order, fontsize=8.2)
    ax.set_xlabel("Total phosphorus, thousand kilograms", fontsize=8.6)
    ax.set_xlim(0, max(max(G.values()), max(A.values())) / 1000 * 1.18)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(fontsize=7.6, frameon=False, loc="lower right")
    c3 = X["call"]
    ax.set_title("%s, %s and %s carried the most phosphorus above allocation" % (c3[0], c3[1], c3[2]),
                 fontsize=9.2, loc="left", color="#202326")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


# -------------------------------------------------------------------------------------------------------- memo

def set_widths(table, inches):
    """fix a table's column widths in both the grid and every cell, so every reader lays it out the same"""
    from docx.shared import Inches
    from docx.oxml.ns import qn
    grid = table._tbl.tblGrid
    for gc, w in zip(grid.findall(qn("w:gridCol")), inches):
        gc.set(qn("w:w"), str(int(w * 1440)))
    for row in table.rows:
        for c, w in zip(row.cells, inches):
            c.width = Inches(w)
    table.autofit = False

def write_docx(X, F, path):
    import docx
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches, Pt
    A, G = X["A"], X["R"][C.GOLD]
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = Inches(1.0)
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import RGBColor
    h2 = d.styles["Heading 2"]
    h2.font.name = "Calibri"
    h2.font.size = Pt(11.5)
    h2.font.color.rgb = RGBColor(0x1F, 0x5F, 0x7A)
    foot = sec.footer.paragraphs[0]
    foot.text = "Brannoch Lake Commission  |  Water quality program  |  Water year 2026 tributary loads  |  Page "
    foot.runs[0].font.size = Pt(8)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    fr = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "16")
    rpr.append(sz)
    fr.append(rpr)
    ft = OxmlElement("w:t")
    ft.text = "1"
    fr.append(ft)
    fld.append(fr)
    foot._p.append(fld)
    t = d.add_paragraph()
    r = t.add_run("MEMORANDUM")
    r.bold = True
    r.font.size = Pt(13)
    hdr = d.add_table(rows=4, cols=2)
    for i, (k, v) in enumerate((("To", "Technical Committee, Brannoch Lake Commission"),
                                ("From", "%s, %s" % W.PEOPLE["manager"]),
                                ("Date", "12 January 2027"),
                                ("Subject", "Water year 2026 tributary loads and the 2027 Tributary Restoration Fund"))):
        hdr.cell(i, 0).text = k
        hdr.cell(i, 1).text = v
        hdr.cell(i, 0).paragraphs[0].runs[0].bold = True
    set_widths(hdr, (0.9, 5.6))
    d.add_paragraph()
    call = X["call"]
    ex = {n: G[n] - A[n] for n in G}
    rest_over = sorted((n for n in ex if n not in call and ex[n] > 0), key=lambda n: -ex[n])
    n_under = sum(1 for n in ex if ex[n] <= 0)
    p = d.add_paragraph()
    r = p.add_run("Fund the 2027 projects in the %s, the %s and %s." % (call[0], call[1], call[2]))
    r.bold = True
    d.add_paragraph(
        "Under section 3.1 of the agreement the Fund takes the three tributaries whose water year 2026 load exceeded its "
        "allocation by the most kilograms. On the approved record those are the %s (%s kg above its allocation), the "
        "%s (%s kg) and %s (%s kg). %s; the other %s tributaries were under their allocations."
        % (call[0], "{:,}".format(F["excess_kg"][call[0]]), call[1], "{:,}".format(F["excess_kg"][call[1]]), call[2],
           "{:,}".format(F["excess_kg"][call[2]]),
           " and ".join("%s (%s kg)" % (n, "{:,}".format(F["excess_kg"][n])) for n in rest_over) +
           (" were also above, by less" if len(rest_over) > 1 else " was also above, by less"),
           {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}[n_under]))
    d.add_paragraph("Table 1. Water year 2026 loads against Schedule 1 allocations (kilograms of total phosphorus).")
    tb = d.add_table(rows=1, cols=6)
    tb.style = "Table Grid"
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths = (1.55, 0.75, 1.35, 0.85, 0.9, 0.85)
    for j, h in enumerate(("Tributary", "Load", "Range, full record", "Allocation", "Above allocation", "2027 project")):
        tb.rows[0].cells[j].text = h
        tb.rows[0].cells[j].paragraphs[0].runs[0].bold = True
    for n in sorted(G, key=lambda n: -ex[n]):
        row = tb.add_row().cells
        lo, hi = F["load_range_full_record_kg"][n]
        vals = [n, "{:,}".format(F["load_kg"][n]), "{:,} to {:,}".format(lo, hi) if lo != hi else "{:,}".format(lo), "{:,}".format(F["allocation_kg"][n]),
                "{:,}".format(F["excess_kg"][n]), "Yes" if n in call else "No"]
        for j, v in enumerate(vals):
            row[j].text = v
            if j in (1, 2, 3, 4):
                row[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    d.add_paragraph("Loads to the nearest 10 kg; the ranking is made on unrounded loads (agreement 2.2). The load is the "
                    "seasonal rating curve with the smearing correction; the range covers the same curve without the seasonal "
                    "cycle, with a quadratic term in discharge, and with the normal-theory correction, each fitted to the "
                    "full record, rounded outward to 10 kg.").runs[0].font.size = Pt(8.5)
    set_widths(tb, widths)
    d.add_picture(io.BytesIO(chart_png(X, F)), width=Inches(5.5))
    d.add_paragraph("Figure 1. Each tributary's water year 2026 load (bars) against its allocation (red marks).").runs[0].font.size = Pt(8.5)
    d.add_heading("How the loads were built", level=2)
    sl = F["slope"]
    d.add_paragraph(
        "A load is the year's daily discharge times the day's concentration, summed. Discharge comes from the approved "
        "15-minute record, averaged over local days (Dunmarsh Brook's carried from its gage by the ratio of drainage "
        "areas). Concentration was sampled on about %d days of the year at each station: the Commission's rounds on the "
        "first and third Tuesdays and the college's storm samples. In every tributary concentration rises with discharge "
        "(slopes of %.2f to %.2f on the log scale), and few samples fall on the high flows that carry the load: on the "
        "Kestle River the tenth of days with the highest discharge carried %d per cent of the year's phosphorus and held "
        "%d per cent of its samples. Carrying the samples across the days between them prices those days at the "
        "readings of the days around them. Each day's concentration is therefore taken from a rating curve fitted to "
        "every accepted routine sample from water years 2024 to 2026: log concentration on log discharge with a "
        "seasonal cycle, retransformed to the mean with the smearing factor."
        % (F["samples_wy2026_mean"], min(sl.values()), max(sl.values()), F["top_tenth_load_pct"]["Kestle River"],
           F["top_tenth_samples_pct"]["Kestle River"]))
    d.add_paragraph(
        "Interpolating the samples between visit days instead puts the Kestle and Hessick rivers below their allocations "
        "and funds Ambrey River, Orrinwood Brook and Varrow Brook; the selection above holds on every rating curve we "
        "fitted (with or without the seasonal cycle, a quadratic term, the normal-theory correction, or a shorter "
        "calibration record).")
    d.add_heading("Data notes", level=2)
    for note in ("Results from both organisations are used: the Commission's (BLC stations) and the college's storm "
                 "samples (ACWL stations), joined through the station register. Field replicates, field blanks and "
                 "rejected results are left out; results reported in micrograms per litre since July 2025 are converted.",
                 "The approved discharge delivered on 14 December 2026 replaces the provisional values for July to "
                 "September; two gages' ratings were shifted from 1 August 2026.",
                 "The upstream wastewater phosphorus and cover crop acres the agreement's section 4.1 asks for are in "
                 "tributary_loads_wy2026.csv."):
        d.add_paragraph(note, style="List Bullet")
    d.save(path)


def write_csv(X, F, path):
    import csv
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["tributary", "compliance_station", "project_2027", "upstream_permitted_wastewater_p_kg_wy2026",
                    "cover_crop_acres_2026"])
        for t in W.TRIBS:
            n = t[1]
            w.writerow([n, t[2], "Yes" if n in X["call"] else "No", F["wastewater_stated"][n], F["cover_stated"][n]])


def main(target, golden, figures_path):
    os.makedirs(golden, exist_ok=True)
    X = compute(target)
    F = figures(X)
    write_docx(X, F, os.path.join(golden, DOCX))
    write_csv(X, F, os.path.join(golden, CSV))
    import postprocess as PP
    by = W.PEOPLE["manager"][0]
    PP.normalize_ooxml(os.path.join(golden, DOCX), by, by, "2027-01-11T15:02:00Z", "2027-01-12T14:31:27Z",
                       title="Water year 2026 tributary loads", company=W.COMMISSION)
    with open(figures_path, "w") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
    return X
