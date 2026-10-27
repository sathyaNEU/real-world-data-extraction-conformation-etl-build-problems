"""The goldens, from the cut pack only: statin_service_tiers_2027-28.docx (the board paper: the networks in the
enhanced tier, each network's population and 2026 share fallen behind, the closest network left out, the chart) and
statin_adherence_2026_by_network.xlsx (the networks' figures and the 2025-26 pilot's), with generator/figures.json
and submission.md, every figure in them emitted from the objects that computed it."""
from __future__ import annotations

import io
import json
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import asks as A
import calc as C
import common as K
import pilot as PL
import postprocess as PP
import records as R

DOCX = "statin_service_tiers_2027-28.docx"
XLSX = "statin_adherence_2026_by_network.xlsx"
QNAME = {1: "October to December 2025", 2: "January to March 2026", 3: "April to June 2026",
         4: "July to September 2026"}
WORDS = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}
INK = "#1d2229"
INK2 = "#4b525c"
GRID = "#e3e6ea"
ENH = "#005eb8"
STD = "#aeb7c2"
PAPER_STAMP = "2027-01-27T15:42:00Z"


class Out:
    pass


def compute(target):
    T = C.patient_table(target)
    X = Out()
    X.T = T
    X.mask = C.route_mask(T, "G", "cyc1")
    X.sh = C.shares(T, X.mask)
    X.tier = C.tier(X.sh)
    X.pct = {k: K.round_half_up(100 * v["share"], 1) for k, v in X.sh.items()}
    X.order = sorted(K.NETWORK_NAME, key=lambda c: -X.sh[c]["share"])
    X.first_below = [c for c in X.order if c not in X.tier][0]
    X.gap = K.round_half_up(100 * (K.TIER_LINE - X.sh[X.first_below]["share"]), 1)
    X.lowest_in = min(X.tier, key=lambda c: X.sh[c]["share"])
    base = T["eligible_base"]
    X.n_base = int(base.sum())
    X.n_care = int((base & T["care_home"]).sum())
    cyc = base & ~T["care_home"] & (T["cyc1"] | T["coded_aid"])
    X.n_cycle = int(cyc.sum())
    X.n_cycle_coded = int((cyc & T["coded_aid"]).sum())
    X.n_pop = int(X.mask.sum())
    X.n_low = int(sum(v["low"] for v in X.sh.values()))
    X.C1, X.C2 = A.pilot_figures(target)
    return X


def names(codes):
    s = [K.NETWORK_NAME[c] for c in codes]
    return ", ".join(s[:-1]) + " and " + s[-1] if len(s) > 1 else s[0]


def fmt(n):
    return format(n, ",")


def chart_png(X):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for f in ("/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
              "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"):
        font_manager.fontManager.addfont(f)
    plt.rcParams["font.family"] = "Carlito"
    vals = [100 * X.sh[c]["share"] for c in X.order]
    fig = plt.figure(figsize=(8.6, 4.3), dpi=170)
    ax = fig.add_axes([0.075, 0.25, 0.905, 0.6])
    xs = np.arange(len(X.order))
    ax.bar(xs, vals, width=0.62, color=[ENH if c in X.tier else STD for c in X.order], zorder=3)
    ax.axhline(30, color=INK, lw=1.1, ls=(0, (5, 3)), zorder=4)
    ax.text(len(X.order) - 0.4, 30.5, "Enhanced tier at 30%", ha="right", va="bottom", fontsize=9.4, color=INK)
    for x, c, v in zip(xs, X.order, vals):
        ax.text(x, v + 0.4, "%.1f" % X.pct[c], ha="center", va="bottom", fontsize=8.8, color=INK)
    ax.set_xticks(xs)
    ax.set_xticklabels([K.NETWORK_NAME[c] for c in X.order], fontsize=9, color=INK2, rotation=35, ha="right")
    ax.set_ylabel("Fallen behind in 2026 (%)", fontsize=9.4, color=INK2)
    ax.set_ylim(0, 40)
    ax.set_yticks([0, 10, 20, 30, 40])
    ax.grid(axis="y", color=GRID, lw=0.7, zorder=1)
    ax.tick_params(axis="y", labelsize=9.2, colors=INK2, length=0)
    ax.tick_params(axis="x", length=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#9aa1aa")
    fig.text(0.075, 0.965, "%s networks have 30%% or more of the service's population behind on their statin"
             % WORDS[len(X.tier)], fontsize=12, color=INK, fontweight="bold", va="top")
    fig.text(0.075, 0.905, "Share of each network's population under 80% of days covered in 2026; blue, the enhanced "
             "tier", fontsize=9, color=INK2, va="top")
    fig.text(0.075, 0.025, "Source: community pharmacy statin dispensing 2026 and the practices' lipid cohort lists at "
             "31 December 2026, Iversford Vale Health Data Service.", fontsize=8, color=INK2)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=170, metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_docx(path, X, png):
    import docx
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
    d = docx.Document()
    sec = d.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.8)
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(6)
    grey = RGBColor(0x5d, 0x65, 0x70)
    blue = RGBColor(0x00, 0x5e, 0xb8)
    foot = sec.footer.paragraphs[0]
    foot.text = "%s board, %s. Page " % (K.FEDERATION, K.uk_date(K.MEETING))
    for r in foot.runs:
        r.font.size = Pt(8)
        r.font.color.rgb = grey
    run = foot.add_run()
    for tag, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)
    run.font.size = Pt(8)
    p = d.add_paragraph()
    r = p.add_run("%s\nBoard of directors, %s, item 6" % (K.FEDERATION, K.uk_date(K.MEETING)))
    r.font.size = Pt(9)
    r.font.color.rgb = grey
    h = d.add_paragraph()
    r = h.add_run("Statin Adherence Support Service 2027-28: %s networks for the enhanced tier"
                  % WORDS[len(X.tier)].lower())
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = blue
    meta = d.add_table(rows=3, cols=2)
    meta.autofit = False
    meta.columns[0].width, meta.columns[1].width = Cm(2.6), Cm(14)
    for i, (a, b) in enumerate((("From", "%s, Head of Medicines Optimisation" % K.PEOPLE["head"]),
                                ("Date", K.uk_date(K.PAPER_DATE)),
                                ("Purpose", "Decision: the tier schedule for the service that starts on "
                                            "1 April 2027"))):
        meta.cell(i, 0).text = a
        meta.cell(i, 1).text = b
        meta.cell(i, 0).paragraphs[0].runs[0].bold = True
        meta.cell(i, 0).width = Cm(2.6)
        meta.cell(i, 1).width = Cm(14)
    d.add_paragraph()
    d.add_paragraph().add_run("1. Recommendation").bold = True
    d.add_paragraph(
        "The board is asked to put %s primary care networks in the enhanced tier of the Statin Adherence Support "
        "Service for 2027-28. In each of them 30 per cent or more of the patients the service is for had fallen "
        "behind on their statin in 2026, from %.1f per cent in %s to %.1f per cent in %s; the other %s networks "
        "go in the standard tier. The closest network left out, %s, sits %.1f percentage points under the line."
        % (names(X.tier), X.pct[X.lowest_in], K.NETWORK_NAME[X.lowest_in], X.pct[X.order[0]],
           K.NETWORK_NAME[X.order[0]], WORDS.get(12 - len(X.tier), str(12 - len(X.tier))).lower(),
           K.NETWORK_NAME[X.first_below], X.gap))
    d.add_paragraph().add_run("2. How the 2026 measure was read").bold = True
    d.add_paragraph(
        "The measure follows the service specification: the patients registered with our practices on 31 December "
        "2026, born in 1961 or earlier, with two or more statin items dispensed in 2026, who collect and take their "
        "own statins (2.1); each patient's proportion of days covered from their first 2026 item to the year end "
        "(2.2); fallen behind under 80 per cent (2.3). Each network is read as its practices stood on 31 December "
        "2026, so the two practices that moved network on 1 April 2026 count in their new networks.")
    d.add_paragraph(
        "Care home residents are recorded on both practice systems' lists and are out. Patients whose statins a "
        "pharmacy packs into a compliance aid are out too, and here the lists do not reach them: Quarvis's list "
        "records the aid for about two thirds of its practices' aid patients and Synaris's list has no field for it. "
        "A pharmacy supplies a compliance aid on its own cycle, every pack on the patient's set weekday 7 or 28 days "
        "after the last, whatever the patient takes, so an aid patient's dispensing reads as covered all year and "
        "would hold a network's share down. Every patient whose 2026 statin items ran on that cycle is therefore out "
        "of the count whether or not the list records the aid; every patient Quarvis's list records shows the cycle, "
        "and no other patient's collections keep to it.")
    d.add_paragraph().add_run("3. Each network's 2026 share").bold = True
    t = d.add_table(rows=1, cols=5)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    trpr = t.rows[0]._tr.get_or_add_trPr()
    rep = OxmlElement("w:tblHeader")
    rep.set(qn("w:val"), "true")
    trpr.append(rep)
    for j, hh in enumerate(("Primary care network", "Patients in the population", "Fallen behind",
                            "Fallen behind (%)", "Tier 2027-28")):
        c = t.rows[0].cells[j]
        c.text = hh
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.size = Pt(9.5)
    for c in X.order:
        cells = t.add_row().cells
        vals = (K.NETWORK_NAME[c], fmt(X.sh[c]["n"]), fmt(X.sh[c]["low"]), "%.1f" % X.pct[c],
                "Enhanced" if c in X.tier else "Standard")
        for j, v in enumerate(vals):
            cells[j].text = v
            para = cells[j].paragraphs[0]
            para.runs[0].font.size = Pt(9.5)
            para.runs[0].bold = c in X.tier and j in (0, 4)
            if j in (1, 2, 3):
                para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    src = d.add_paragraph("Source: community pharmacy statin dispensing to 31 December 2026 and the practices' lipid "
                          "cohort lists at 31 December 2026 (Iversford Vale Health Data Service).")
    src.runs[0].font.size = Pt(8)
    src.runs[0].font.color.rgb = grey
    d.add_picture(io.BytesIO(png), width=Cm(16.4))
    d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    d.add_paragraph().add_run("4. The pilot").bold = True
    d.add_paragraph(
        "The workbook statin_adherence_2026_by_network.xlsx sets out, quarter by quarter, the patients the pilot "
        "pharmacies in Krathwold and Lathcombe saw for a first consultation from October 2025 to September 2026 and "
        "those followed up within six weeks, counted from the services portal and the payment statements to January "
        "2027.")
    note = d.add_paragraph(
        "Note: a patient whose statins were dispensed by a distance-selling pharmacy is in the population on the "
        "same terms (specification 2.1).")
    note.runs[0].font.size = Pt(8.5)
    note.runs[0].font.color.rgb = grey
    d.core_properties.title = "Statin Adherence Support Service 2027-28: tier schedule"
    d.save(path)


def write_xlsx(path, X):
    wb = Workbook()
    thin = Side(style="thin", color="C9CED4")
    head_fill = PatternFill("solid", fgColor="E8EDF2")
    bold = Font(name="Calibri", bold=True)

    def header(ws, row, cols):
        for j, c in enumerate(cols, 1):
            cell = ws.cell(row=row, column=j, value=c)
            cell.font = bold
            cell.fill = head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(bottom=thin)

    ws = wb.active
    ws.title = "Networks"
    ws["A1"] = "Statin Adherence Support Service 2027-28: the 2026 measure by primary care network"
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws["A2"] = ("Population (specification 2.1): registered on 31 December 2026, born in 1961 or earlier, two or more "
                "statin items dispensed in 2026, collecting and taking their own statins. Fallen behind: under 80 "
                "per cent of days covered from the first 2026 item to 31 December 2026 (2.2, 2.3).")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:E2")
    ws.row_dimensions[2].height = 46
    header(ws, 4, ["Primary care network", "Patients in the population", "Fallen behind",
                   "Share fallen behind (%)", "Tier 2027-28"])
    ws.row_dimensions[4].height = 30
    r = 5
    for c in sorted(K.NETWORK_NAME, key=lambda x: K.NETWORK_NAME[x]):
        ws.cell(row=r, column=1, value=K.NETWORK_NAME[c] + " PCN")
        ws.cell(row=r, column=2, value=X.sh[c]["n"]).number_format = "#,##0"
        ws.cell(row=r, column=3, value=X.sh[c]["low"]).number_format = "#,##0"
        ws.cell(row=r, column=4, value=X.pct[c]).number_format = "0.0"
        ws.cell(row=r, column=5, value="Enhanced" if c in X.tier else "Standard")
        if c in X.tier:
            for j in (1, 5):
                ws.cell(row=r, column=j).font = Font(name="Calibri", bold=True, color="00468C")
        r += 1
    ws.cell(row=r, column=1, value="All networks").font = bold
    ws.cell(row=r, column=2, value=X.n_pop).number_format = "#,##0"
    ws.cell(row=r, column=3, value=X.n_low).number_format = "#,##0"
    for j in range(1, 6):
        ws.cell(row=r, column=j).border = Border(top=thin)
    ws.cell(row=r + 2, column=1, value="Closest network left out: %s PCN, %.1f percentage points under the 30 per cent "
            "line." % (K.NETWORK_NAME[X.first_below], X.gap))
    for col, w in zip("ABCDE", (24, 15, 12, 14, 13)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    ws.print_title_rows = "4:4"

    ws2 = wb.create_sheet("Pilot Oct 2025 to Sep 2026")
    ws2["A1"] = ("The pilot, October 2025 to September 2026: patients seen for a first consultation and followed up "
                 "within six weeks")
    ws2["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws2["A2"] = ("Each patient's first consultation once, in the quarter it was held and the network its pharmacy was "
                 "in that day; followed up: a follow-up consultation within six weeks of it. Every consultation held "
                 "counts, whether or not the federation paid for it.")
    ws2["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws2.merge_cells("A2:E2")
    ws2.row_dimensions[2].height = 46
    header(ws2, 4, ["Quarter of the pilot", "Krathwold: first consultations", "Krathwold: followed up within six weeks",
                    "Lathcombe: first consultations", "Lathcombe: followed up within six weeks"])
    ws2.row_dimensions[4].height = 30
    for q in (1, 2, 3, 4):
        ws2.cell(row=4 + q, column=1, value=QNAME[q])
        ws2.cell(row=4 + q, column=2, value=X.C1[("KRT", q)])
        ws2.cell(row=4 + q, column=3, value=X.C2[("KRT", q)])
        ws2.cell(row=4 + q, column=4, value=X.C1[("LTH", q)])
        ws2.cell(row=4 + q, column=5, value=X.C2[("LTH", q)])
    for col, w in zip("ABCDE", (26, 16, 20, 16, 20)):
        ws2.column_dimensions[col].width = w
    ws2.freeze_panes = "B5"

    ws3 = wb.create_sheet("Notes")
    notes = [
        "Sources: %s for the member practices (dispensing 1 December 2025 to 31 December 2026; the practices' lipid cohort lists at 31 December "
        "2026; the pseudonym crosswalk of 1 July 2026; the practice network list); the services portal's pilot export "
        "of 2 October 2026; the pilot payment statements, November 2025 to January 2027; the community pharmacy list, "
        "December 2026." % K.DATA_SERVICE,
        "Patients whose statins a pharmacy dispensed on a compliance-aid cycle (every 2026 item on the same weekday, 7 "
        "or 28 days after the last, a bank holiday's pack on the next opening day) are outside the population whether "
        "or not their practice's list records the aid.",
        "Networks as their practices stood on 31 December 2026. Pseudonyms before 1 July 2026 carried to the new keys "
        "through the crosswalk.",
        "Pilot: a first consultation keyed twice counts once, at the record the federation did not recover; consultations "
        "recorded after the portal export was pulled are taken from the statements.",
        "Prepared on %s for the board meeting of %s." % (K.uk_date(K.PAPER_DATE), K.uk_date(K.MEETING)),
    ]
    for i, t in enumerate(notes, 1):
        ws3.cell(row=i, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
        ws3.row_dimensions[i].height = 46
    ws3.column_dimensions["A"].width = 110
    wb.save(path)


def figures(X):
    F = {"tier": [K.NETWORK_NAME[c] for c in X.tier], "closest_left_out": K.NETWORK_NAME[X.first_below],
         "gap_points": "%.1f" % X.gap, "lowest_in": "%.1f" % X.pct[X.lowest_in],
         "n_base": fmt(X.n_base), "n_care": fmt(X.n_care), "n_cycle": fmt(X.n_cycle),
         "n_cycle_coded": fmt(X.n_cycle_coded), "n_pop": fmt(X.n_pop), "tier_count": len(X.tier),
         "parameters": {"tier_line_pct": 30, "fallen_behind_pct": 80, "cycle_steps_days": [7, 28],
                        "specification_sections": ["2.2", "2.3", "3.1"], "follow_up_days": [1, 41]}}
    for c in K.NETWORK_NAME:
        F["share_" + c] = "%.1f" % X.pct[c]
        F["population_" + c] = fmt(X.sh[c]["n"])
    for (n, q), v in X.C1.items():
        F["pilot_first_%s_q%d" % (n, q)] = v
    for (n, q), v in X.C2.items():
        F["pilot_followed_%s_q%d" % (n, q)] = v
    return F


def writeup(X):
    """submission.md: the five blocks, every figure from X."""
    analyst = ["COR", "FEL", "KRT", "NVG"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Pharmacology, Pharmacoepidemiology & Safety (medication adherence and persistence: each "
             "primary care network's share of its older self-managing statin patients under 80 per cent of days "
             "covered in 2026).")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**The board should put %s in the enhanced tier of the 2027-28 Statin Adherence Support Service.**"
             % names(X.tier))
    L.append("In each, 30 per cent or more of the service's population fell under 80 per cent of days covered in 2026 "
             "(lowest %s at %.1f per cent), and the closest network left out, %s, sits %.1f points under the line. Not "
             "the four networks the practice lists' codes alone give (%s), which keep the patients whose statins a "
             "pharmacy dispensed on a compliance-aid cycle, uncoded, in the count at full cover and hold %s under the "
             "line." % (K.NETWORK_NAME[X.lowest_in], X.pct[X.lowest_in], K.NETWORK_NAME[X.first_below], X.gap,
                        names(analyst), names([c for c in X.tier if c not in analyst])))
    L.append("")
    L.append("## 2. Critical Components\n")
    L.append("1. Patients in the service's population across the twelve networks: **%s**." % fmt(X.n_pop))
    L.append("2. Patients out because their 2026 statin items ran on a compliance-aid cycle, recorded on a list or "
             "not: **%s**." % fmt(X.n_cycle))
    L.append("3. Briskdale's share fallen behind is **%.1f per cent**." % X.pct["BRK"])
    L.append("4. Grevmoor's share fallen behind is **%.1f per cent**." % X.pct["GRV"])
    L.append("5. %s, the closest network left out, is at **%.1f per cent**." % (K.NETWORK_NAME[X.first_below],
                                                                               X.pct[X.first_below]))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Carried every pre-July pseudonym in %s through %s and kept the patients on %s and %s born in 1961 or "
             "earlier with two or more 2026 statin items, each in the network its practice was in on 31 December 2026 "
             "(%s): %s patients." % (R.F_DISP, R.F_XWALK, R.F_QUARVIS, R.F_SYNARIS, R.F_PRACTICES, fmt(X.n_base)))
    L.append("2. Took out the care home residents both lists record (care_home_since; Residence Care home): %s patients."
             % fmt(X.n_care))
    L.append("3. Took out every patient whose 2026 items all fall on one weekday at steps of 7 or 28 days, a pack due "
             "on a Sunday or bank holiday supplied the next opening day (%s), which every patient %s records with "
             "mds_since shows and no other patient's collections keep to: %s patients, %s of them recorded."
             % ("compliance_aids_prescribing_and_supply_guidance_2025.pdf", R.F_QUARVIS, fmt(X.n_cycle),
                fmt(X.n_cycle_coded)))
    L.append("4. Computed each remaining patient's proportion of days covered as "
             "statin_adherence_support_service_specification_2027-28.pdf 2.2 defines it and took each network's share "
             "under 80 per cent (2.3, 3.1): %s networks at 30 per cent or more." % WORDS[len(X.tier)].lower())
    L.append("5. For the pilot, added to %s the payment lines in %s it lacks (consultations recorded after the pull), "
             "dropped a recovered first consultation only where the same patient, through the crosswalk, has another "
             "first consultation the federation did not recover (a hand-keyed second record), kept every other recovered "
             "record (a consultation held and claimed late), placed each consultation in the network its pharmacy was "
             "in that day (%s relocated_on and previous_locality), and counted each patient's first consultation once "
             "by quarter, followed up if a follow-up came 1 to 41 days after it."
             % (PL.F_PORTAL, PL.F_STATEMENTS, PL.F_PHARMACIES))
    L.append("6. The board puts %s in the enhanced tier." % names(X.tier))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % DOCX)
    L.append("1. Networks in the enhanced tier: %s." % names(X.tier))
    L.append("2. Each network's patients in the service's population and share fallen behind in 2026, per cent to one "
             "decimal:")
    for c in X.order:
        L.append("   - %s: %s patients, %.1f, %s" % (K.NETWORK_NAME[c], fmt(X.sh[c]["n"]), X.pct[c],
                                                   "enhanced" if c in X.tier else "standard"))
    L.append("3. The closest network left out, %s, sits %.1f percentage points under the line."
             % (K.NETWORK_NAME[X.first_below], X.gap))
    L.append("4. Bar chart of the twelve networks' shares against the 30 per cent line, the enhanced tier in blue.\n")
    L.append("### %s\n" % XLSX)
    L.append("5. Patients with a first consultation in the pilot, October 2025 to September 2026, by quarter:")
    for n in ("KRT", "LTH"):
        for q in (1, 2, 3, 4):
            L.append("   - %s, %s: %d" % (K.NETWORK_NAME[n], QNAME[q], X.C1[(n, q)]))
    L.append("6. Of them, followed up within six weeks:")
    for n in ("KRT", "LTH"):
        for q in (1, 2, 3, 4):
            L.append("   - %s, %s: %d" % (K.NETWORK_NAME[n], QNAME[q], X.C2[(n, q)]))
    return "\n".join(L) + "\n"


def main(target=K.TARGET, golden=K.GOLDEN, figs=os.path.join(K.HERE, "figures.json"),
         sub=os.path.join(K.TASK, "submission.md")):
    os.makedirs(golden, exist_ok=True)
    X = compute(target)
    png = chart_png(X)
    write_docx(os.path.join(golden, DOCX), X, png)
    write_xlsx(os.path.join(golden, XLSX), X)
    PP.normalize_docx(os.path.join(golden, DOCX), K.PEOPLE["head"], K.PEOPLE["head"], "2027-01-22T10:05:00Z",
                      PAPER_STAMP, 4, 96, "task270", title="Statin Adherence Support Service 2027-28: tier schedule",
                      company=K.FEDERATION)
    PP.normalize_ooxml(os.path.join(golden, XLSX), K.PEOPLE["head"], K.PEOPLE["head"], "2027-01-21T09:12:00Z",
                       "2027-01-27T15:20:00Z", excel=True, company=K.FEDERATION)
    with open(figs, "w") as fh:
        json.dump(figures(X), fh, indent=1, sort_keys=True)
    with open(sub, "w", encoding="utf-8") as fh:
        fh.write(writeup(X))
    return X


if __name__ == "__main__":
    main()
