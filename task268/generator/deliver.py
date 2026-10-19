"""The goldens: hf_programme_site_2027.xlsx (each hospital's two-year survival and how its patients left follow-up, the
2025 laboratory testing, the 2025 new diagnoses) and service_line_committee_hf_2027.pptx (the recommendation to the
service line committee with the chart of the five hospitals' two-year survival), plus generator/figures.json and
metadata.json. Every figure comes from analysis.py run on the shipped pack."""
import json
import os
import shutil

import analysis as A
import common as K
import postprocess as PP

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX, PPTX = "hf_programme_site_2027.xlsx", "service_line_committee_hf_2027.pptx"


def whole(x):
    """Round half up to the whole unit (percent, point, count)."""
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def results(target):
    D = A.load(target)
    L = A.ladder(D)
    C = L["_cohort"]
    S = L["golden"]
    order = sorted(K.CODES, key=lambda h: S[h])
    pick, runner = order[0], order[1]
    gap = 100 * (S[runner] - S[pick])
    G = A.by_h(C)
    counts = {}
    for h in K.CODES:
        g = G[h]
        counts[h] = dict(n=len(g), deaths=sum(p["E"] for p in g), north=sum(p["lost"] == "north" for p in g),
                         consent=sum(p["lost"] == "consent" for p in g))
    rates = {h: A.censor_rates(G[h]) for h in K.CODES}
    visits = {h: [sum(1 for p in G[h] for d, c in p["visits"] if d <= p["T"] and c == k) for k in range(4)] for h in K.CODES}
    moves = {h: [sum(1 for p in G[h] if p["lost"] == "north" and p["visits"] and p["visits"][-1][0] == p["T"]
                     and p["visits"][-1][1] == k) for k in range(4)] for h in K.CODES}
    return dict(D=D, L=L, S=S, order=order, pick=pick, runner=runner, gap=gap, counts=counts, rates=rates, visits=visits,
                moves=moves, surv={h: whole(100 * S[h]) for h in K.CODES}, gap_pts=whole(gap),
                km={h: whole(100 * L["km"][h]) for h in K.CODES}, ask_a=A.ask_a(D), ask_b=A.ask_b(D))


# ---------------------------------------------------------------------------------------------- the workbook
def workbook(path, o):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    ink, accent = "1C2428", "0E5A6E"
    thin = Side(style="thin", color="B4BDC3")
    head_fill = PatternFill("solid", fgColor="E3EEF1")
    pick_fill = PatternFill("solid", fgColor="FBE7D6")
    pick, runner = o["pick"], o["runner"]

    def header(ws, row, cols, height=42):
        for j, v in enumerate(cols, 1):
            cell = ws.cell(row=row, column=j, value=v)
            cell.font = Font(bold=True, color=ink)
            cell.fill = head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left" if j == 1 else "right")
            cell.border = Border(bottom=thin)
        ws.row_dimensions[row].height = height

    def landscape(ws):
        ws.page_setup.orientation = "landscape"
        ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_title_rows = "4:4"

    def title(ws, text, sub):
        ws["A1"] = text
        ws["A1"].font = Font(bold=True, size=13, color=accent)
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, size=9, color="5A646B")

    def widths(ws, ws_w):
        for j, w in enumerate(ws_w, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w

    # Survival
    ws = wb.active
    ws.title = "Survival"
    title(ws, "Host the 2027 programme at %s: the lowest two-year survival from diagnosis" % K.NAME[pick],
          "Patients newly diagnosed with heart failure in 2022 and 2023, %s. Two-year survival with each patient who moved "
          "beyond the registry's death linkage carried by the NYHA class recorded at the visit where the move was "
          "reported." % K.REGISTRY)
    header(ws, 4, ["Hospital", "Patients diagnosed 2022-23", "Deaths within two years on file",
                   "Moved beyond the death linkage before two years", "Left at the re-consent before two years",
                   "Two-year survival (%)"])
    r = 5
    for h in o["order"]:
        c = o["counts"][h]
        vals = [K.NAME[h], c["n"], c["deaths"], c["north"], c["consent"], o["surv"][h]]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(row=r, column=j, value=v)
            if j >= 2:
                cell.alignment = Alignment(horizontal="right")
                cell.number_format = "#,##0"
            if h == pick:
                cell.fill = pick_fill
                cell.font = Font(bold=True, color=ink)
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Recommendation: host the programme at %s from April 2027. Its patients' two-year "
            "survival is %d%%, %d points below %s's %d%%, the next lowest." % (
                K.NAME[pick], o["surv"][pick], o["gap_pts"], K.NAME[runner], o["surv"][runner])).font = Font(bold=True)
    ws.cell(row=r + 1, column=1, value="Survival is the product-limit estimate at two years, each patient still followed "
            "weighted, visit by visit, by the inverse of the hospital's chance that a patient of the class recorded at "
            "that visit stays within the death linkage's reach. The gap is worked from the unrounded figures.").font = \
        Font(size=9, color="5A646B")
    widths(ws, [34, 14, 14, 18, 16, 14])
    ws.freeze_panes = "B5"
    landscape(ws)

    # Moves by class
    ws = wb.create_sheet("Moves by class")
    title(ws, "How the patients left follow-up: moves beyond the death linkage by the NYHA class at the visit",
          "Clinic visits within each patient's first two years, while followed; a move is counted at the visit where it "
          "was reported.")
    header(ws, 4, ["Hospital", "Visits in class I", "II", "III", "IV", "Moves in class I", "II", "III", "IV",
                   "Chance of moving at a class III visit (%)", "At a class IV visit (%)"])
    r = 5
    for h in K.CODES:
        v, m, rt = o["visits"][h], o["moves"][h], o["rates"][h]
        vals = [K.NAME[h]] + v + m + [round(100 * rt.get(2, 0.0), 1), round(100 * rt.get(3, 0.0), 1)]
        for j, x in enumerate(vals, 1):
            cell = ws.cell(row=r, column=j, value=x)
            if j >= 2:
                cell.alignment = Alignment(horizontal="right")
                cell.number_format = "#,##0" if j <= 9 else "0.0"
            if h == pick:
                cell.fill = pick_fill
        r += 1
    widths(ws, [34] + [10] * 8 + [16, 14])
    landscape(ws)

    # Laboratory
    ws = wb.create_sheet("Laboratory")
    title(ws, "NT-proBNP tests reported in 2025, by hospital laboratory",
          "Each specimen once, at its final result; the referral level is %d pg/mL (charter, 2.3)." % K.REFERRAL)
    header(ws, 4, ["Hospital", "NT-proBNP tests reported in 2025", "At or above %d pg/mL" % K.REFERRAL], 32)
    r = 5
    for h in K.CODES:
        a = o["ask_a"][h]
        for j, x in enumerate([K.NAME[h], a[0], a[1]], 1):
            cell = ws.cell(row=r, column=j, value=x)
            if j >= 2:
                cell.alignment = Alignment(horizontal="right")
                cell.number_format = "#,##0"
        r += 1
    widths(ws, [34, 18, 18])

    # New diagnoses
    ws = wb.create_sheet("New diagnoses 2025")
    title(ws, "Patients newly diagnosed with heart failure in 2025, by hospital",
          "By diagnosis date (a record showing its diagnosis after its enrolment is dated at the enrolment); a patient "
          "enrolled again after the 2024 record-number migration is not a new diagnosis.")
    header(ws, 4, ["Hospital", "Newly diagnosed in 2025", "Of whom during an inpatient stay"], 32)
    r = 5
    for h in K.CODES:
        b = o["ask_b"][h]
        for j, x in enumerate([K.NAME[h], b[0], b[1]], 1):
            cell = ws.cell(row=r, column=j, value=x)
            if j >= 2:
                cell.alignment = Alignment(horizontal="right")
                cell.number_format = "#,##0"
        r += 1
    widths(ws, [34, 18, 22])

    # Notes
    ws = wb.create_sheet("Notes")
    notes = [
        "Cohort: every enrolment in %s with a diagnosis date from 1 January 2022 to 31 December 2023; the hospital "
        "is the hospital of diagnosis (Brenmoor's North Campus is Brenmoor Regional)." % K.FILES["patients"],
        "Deaths: the Florida certificate linkage (by current record number, legacy numbers through the crosswalk) and "
        "the Tri-State exchange (by registry identifier); a patient alive on the second anniversary of diagnosis "
        "survived two years.",
        "Follow-up ends at a relocation to a state outside Georgia, Alabama and South Carolina and at Wrenhaven's 1 "
        "April 2024 re-consent; patients who moved to those three states stay in vital status follow-up.",
        "At %s most patients who moved beyond the linkage were in NYHA class III or IV at the visit where the move was "
        "reported, so the product-limit estimate with the moves as ordinary censoring credits them with the survival "
        "of the patients who stayed (%d%% against %d%% weighted). The chance of a move by class is measured hospital "
        "by hospital." % (K.NAME[pick], o["km"][pick], o["surv"][pick]),
        "Laboratory: results released in 2025; a corrected result released again under a new accession (same patient "
        "and collection time) counts once, at its final value.",
        "New diagnoses: by diagnosis date; the registry module's update of November 2024 overwrote some diagnosis "
        "dates with a later problem-list date, so a record showing its diagnosis after its enrolment is dated at the "
        "enrolment (the diagnosis came first). A 2025 enrolment whose record number maps through the crosswalk to a "
        "patient enrolled earlier is not counted; the inpatient stays are those the setting records as Inpatient or INPT.",
    ]
    ws["A1"] = "Notes on the figures"
    ws["A1"].font = Font(bold=True, size=12, color=accent)
    for k, t in enumerate(notes, 3):
        ws.cell(row=k, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 120
    wb.save(path)


# ---------------------------------------------------------------------------------------------- the deck
def deck(path, o):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Emu, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]
    INK, GREY, ACC = RGBColor(0x1C, 0x24, 0x28), RGBColor(0x5A, 0x64, 0x6B), RGBColor(0xB2, 0x4A, 0x16)
    TEAL = RGBColor(0x0E, 0x5A, 0x6E)
    pick, runner = o["pick"], o["runner"]

    def text(slide, x, y, w, h, s, size=14, bold=False, color=INK, align=None):
        tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = s
        p.font.size, p.font.bold, p.font.color.rgb = Pt(size), bold, color
        p.font.name = "Calibri"
        if align:
            p.alignment = align
        return tf

    def footer(slide, n, source):
        text(slide, 457200, 6400800, 10300000, 300000, "Heart and vascular outcomes | Service line committee, May 2026 | "
             "Source: " + source, 9, color=GREY)
        text(slide, 11000000, 6400800, 800000, 300000, str(n), 9, color=GREY, align=PP_ALIGN.RIGHT)

    HEAD, BAND, PICK = RGBColor(0x1F, 0x4E, 0x5C), RGBColor(0xF2, 0xF5, 0xF6), RGBColor(0xFB, 0xE7, 0xD6)

    def table(slide, rows, x, y, w, h, bold_row=None, size=13, cw=None):
        shape = slide.shapes.add_table(len(rows), len(rows[0]), Emu(x), Emu(y), Emu(w), Emu(h))
        tb = shape.table
        tb.first_row = True
        tb.horz_banding = False
        if cw:
            for j, f in enumerate(cw):
                tb.columns[j].width = Emu(int(w * f))
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                cell = tb.cell(i, j)
                cell.text = v
                cell.fill.solid()
                cell.fill.fore_color.rgb = HEAD if i == 0 else (PICK if bold_row is not None and r[0] == bold_row
                                                                 else (BAND if i % 2 == 0 else RGBColor(0xFF, 0xFF, 0xFF)))
                para = cell.text_frame.paragraphs[0]
                para.font.size = Pt(size if i else size - 1)
                para.font.name = "Calibri"
                para.font.bold = i == 0 or (bold_row is not None and r[0] == bold_row)
                para.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i == 0 else INK
                if j:
                    para.alignment = PP_ALIGN.RIGHT
        return tb

    S = o["surv"]
    # 1. the call
    s = prs.slides.add_slide(blank)
    text(s, 457200, 1250000, 11200000, 900000, "Host the 2027 programme at %s" % K.NAME[pick], 34, True, ACC)
    tf = text(s, 457200, 2350000, 11000000, 1500000,
              "Its patients newly diagnosed with heart failure in 2022 and 2023 had a two-year survival of %d%%, the "
              "lowest of our five hospitals and %d points below %s's %d%%." % (S[pick], o["gap_pts"], K.NAME[runner],
                                                                             S[runner]), 20)
    p = tf.add_paragraph()
    p.text = ("Charter, section 3: the programme goes to the hospital whose newly diagnosed patients had the lowest "
              "two-year survival from diagnosis, every patient counted, those the registry no longer follows included.")
    p.font.size, p.font.color.rgb = Pt(14), GREY
    rows = [["Hospital"] + [K.SHORT[h] for h in o["order"]],
            ["Two-year survival, 2022-23 diagnoses"] + ["%d%%" % S[h] for h in o["order"]]]
    table(s, rows, 457200, 4250000, 11200000, 900000, size=13, cw=[0.30] + [0.14] * 5)
    footer(s, 1, K.REGISTRY + ", extract of 31 March 2026")
    # 2. the chart
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 700000, "%s's patients have the lowest two-year survival" % K.SHORT[pick], 26, True)
    text(s, 457200, 900000, 11200000, 400000, "Two-year survival from diagnosis, patients newly diagnosed with heart "
         "failure in 2022 and 2023, per cent", 13, color=GREY)
    cd = CategoryChartData()
    cd.categories = [K.SHORT[h] for h in o["order"]]
    cd.add_series("Two-year survival (%)", [S[h] for h in o["order"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(457200), Emu(1400000), Emu(11200000), Emu(4800000), cd)
    ch = gf.chart
    ch.has_title = False
    ch.has_legend = False
    plot = ch.plots[0]
    plot.gap_width = 70
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format, dl.number_format_is_linked = '0"%"', False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(14)
    ser = plot.series[0]
    for k, h in enumerate(o["order"]):
        pt = ser.points[k]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = ACC if h == pick else TEAL
    va = ch.value_axis
    va.minimum_scale, va.maximum_scale, va.major_unit = 0, 100, 20
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor(0xDD, 0xE2, 0xE5)
    va.tick_labels.font.size = Pt(12)
    ch.category_axis.tick_labels.font.size = Pt(14)
    footer(s, 2, K.REGISTRY + "; Florida death certificate linkage; Tri-State exchange")
    # 3. why the plain estimate misleads at the pick
    s = prs.slides.add_slide(blank)
    v, m = o["visits"][pick], o["moves"][pick]
    tot = sum(m)
    hi = m[2] + m[3]
    text(s, 457200, 300000, 11200000, 700000, "At %s the patients who moved north had worsened" % K.SHORT[pick], 26, True)
    lines = [
        "{:,} of {}'s {:,} patients moved beyond the registry's death linkage within two years of diagnosis; {:,} of them "
        "were in NYHA class III or IV at the visit where they told the clinic.".format(tot, K.SHORT[pick],
                                                                                        o["counts"][pick]["n"], hi),
        "Counting those moves as ordinary losses puts %s's survival at %d%%, as if the movers fared like the patients "
        "who stayed. Weighted by the class at each visit it is %d%%." % (K.SHORT[pick], o["km"][pick], S[pick]),
    ]
    tf = text(s, 457200, 1250000, 11200000, 1900000, lines[0], 16)
    p = tf.add_paragraph()
    p.text = lines[1]
    p.font.size = Pt(16)
    p.space_before = Pt(10)
    rt = o["rates"][pick]
    rows = [["NYHA class at the visit", "Visits", "Moves beyond the linkage", "Chance of moving at the visit"]]
    for k in range(4):
        rows.append([K.CLASSES[k], "{:,}".format(v[k]), "{:,}".format(m[k]), "%.1f%%" % (100 * rt.get(k, 0.0))])
    table(s, rows, 457200, 3450000, 11200000, 2000000, size=14, cw=[0.31, 0.2, 0.25, 0.24])
    footer(s, 3, K.REGISTRY + ", clinic visits and follow-up events")
    # 4. the testing and the diagnoses the programme builds on
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 700000, "Testing and new diagnoses, 2025", 26, True)
    rows = [["Hospital", "NT-proBNP tests reported", "At or above %d pg/mL" % K.REFERRAL, "Newly diagnosed",
             "Diagnosed as inpatients"]]
    for h in K.CODES:
        a, b = o["ask_a"][h], o["ask_b"][h]
        rows.append([K.NAME[h], "{:,}".format(a[0]), "{:,}".format(a[1]), "{:,}".format(b[0]), "{:,}".format(b[1])])
    table(s, rows, 457200, 1300000, 11200000, 2600000, bold_row=K.NAME[pick], size=14, cw=[0.32, 0.17, 0.17, 0.17, 0.17])
    text(s, 457200, 4300000, 11200000, 1100000, "Tests: each specimen once at its final result. New diagnoses: by "
         "diagnosis date, a record dated after its own enrolment taken at the enrolment; a patient enrolled again after "
         "the 2024 record-number migration is not counted.", 13, color=GREY)
    footer(s, 4, "laboratory results 2025; " + K.REGISTRY)
    prs.save(path)


def figures(o):
    L = o["L"]
    return {
        "call": dict(hospital=K.NAME[o["pick"]], runner_up=K.NAME[o["runner"]], gap=o["gap_pts"], survival=o["surv"][o["pick"]],
                     runner_survival=o["surv"][o["runner"]]),
        "survival": {K.NAME[h]: o["surv"][h] for h in K.CODES},
        "rungs": {r: dict(pick=K.NAME[A.pick(L[r])[0]], survival={K.NAME[h]: round(100 * L[r][h], 1) for h in K.CODES})
                  for r in A.WRONG + A.FAMILY},
        "counts": {K.NAME[h]: o["counts"][h] for h in K.CODES},
        "ask_a": {K.NAME[h]: dict(tests=o["ask_a"][h][0], referral=o["ask_a"][h][1]) for h in K.CODES},
        "ask_b": {K.NAME[h]: dict(new=o["ask_b"][h][0], inpatient=o["ask_b"][h][1]) for h in K.CODES},
        "km": {K.NAME[h]: o["km"][h] for h in K.CODES},
        "cohort_total": sum(o["counts"][h]["n"] for h in K.CODES),
        "moves_class_3_4": {K.NAME[h]: o["moves"][h][2] + o["moves"][h][3] for h in K.CODES},
        "move_rate": {K.NAME[h]: {"class_3": round(100 * o["rates"][h].get(2, 0.0), 1),
                                  "class_4": round(100 * o["rates"][h].get(3, 0.0), 1)} for h in K.CODES},
        "params": dict(cohort_years=[2022, 2023], years=2, referral=K.REFERRAL, results_year=2025, diagnoses_year=2025,
                       charter_clauses=sorted(float(v) for v in K.CHARTER_CLAUSES.values()),
                       manual_sections=sorted(float(v) for v in K.MANUAL_SECTIONS.values()), chart_max=100),
    }


def write(target, golden, W=None):
    o = results(target)
    if os.path.exists(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    workbook(os.path.join(golden, XLSX), o)
    deck(os.path.join(golden, PPTX), o)
    PP.COMPANY = K.ORG_INC
    PP.normalize_ooxml(os.path.join(golden, XLSX), K.PEOPLE["epi"], K.PEOPLE["epi"], "2026-04-16T13:05:41Z",
                       "2026-04-29T21:12:08Z", excel=True)
    PP.normalize_ooxml(os.path.join(golden, PPTX), K.PEOPLE["epi"], K.PEOPLE["director"], "2026-04-30T14:22:19Z",
                       "2026-05-06T22:47:55Z", title="HF early diagnosis programme: host hospital")
    json.dump(figures(o), open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    meta = {"distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS], "deliverables": [XLSX, PPTX],
            "stated_inputs": []}
    json.dump(meta, open(os.path.join(os.path.dirname(HERE), "metadata.json"), "w"), indent=2)
    return o
