"""task122 generator: the golden deliverables and generator/figures.json.

VMK-4410_phase3_dose_recommendation.pdf carries the call, each dose's eGFR difference from placebo at month 36 and a
chart of each dose's difference by month to month 36; VMK-4410_phase2b_tables.xlsx carries the asks. Every figure
comes from the analysis of the shipped pack, never typed."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402
from openpyxl import Workbook      # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill   # noqa: E402
from openpyxl.utils import get_column_letter               # noqa: E402
from reportlab.lib import colors   # noqa: E402
from reportlab.lib.pagesizes import A4   # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet   # noqa: E402
from reportlab.lib.units import mm   # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import numpy as np          # noqa: E402
import params as P          # noqa: E402
import postprocess          # noqa: E402

DOSES = ["VMK-4410 5 mg", "VMK-4410 10 mg", "VMK-4410 20 mg", "VMK-4410 40 mg"]
ARMS = ["Placebo"] + DOSES
SHORT = {a: a.replace("VMK-4410 ", "") for a in ARMS}
COL = {"VMK-4410 5 mg": "#8c8c8c", "VMK-4410 10 mg": "#5b7fa6", "VMK-4410 20 mg": "#1f6f4a", "VMK-4410 40 mg": "#b4433b"}


def whole(x):
    return int(np.floor(x + 0.5)) if x >= 0 else -int(np.floor(-x + 0.5))


def _r(x, n=3):
    if isinstance(x, dict):
        return {str(k): _r(v, n) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_r(v, n) for v in x]
    if isinstance(x, (float, np.floating)):
        return round(float(x), n)
    if isinstance(x, np.integer):
        return int(x)
    return x


def figures(rec):
    g = rec["gold"]
    a = rec["asks"]
    f = {
        "call": rec["call"],
        "call_sentence": "Take VMK-4410 20 mg into the phase 3: on it eGFR would be %d mL/min/1.73 m2 higher than on placebo after 36 months' treatment, %d more than on 40 mg." % (whole(g["VMK-4410 20 mg"]), whole(g["VMK-4410 20 mg"]) - whole(g["VMK-4410 40 mg"])),
        "diff36": {SHORT[d]: whole(g[d]) for d in DOSES},
        "runner_up": rec["runner"],
        "gap36": whole(g[rec["call"]]) - whole(g[rec["runner"]]),
        "flip_slope_per_year": round(rec["flip_slope"], 1),
        "slope_per_year": {SHORT[d]: round(rec["slope24"][d], 1) for d in DOSES},
        "settled_week24_to_52": {SHORT[d]: round(rec["settled"][d], 1) for d in DOSES},
        "observed_diff": {SHORT[d]: {str(w): round(float(rec["diff"][d].loc[w]), 2) for w in rec["diff"][d].index} for d in DOSES},
        "default_month3": {SHORT[d]: whole(rec["routes"][d]["k12"]) for d in DOSES},
        "week52": {SHORT[d]: round(rec["routes"][d]["w52"], 1) for d in DOSES},
        "rise_12_24": {SHORT[d]: round(rec["rise_12_24"][d], 1) for d in DOSES},
        "eased": {SHORT[x]: rec["eased"][x] for x in ARMS},
        "loop": {SHORT[x]: rec["loop"][x] for x in ARMS},
        "randomised": {SHORT[x]: rec["n_arm"][x] for x in ARMS},
        "stopped_for_good_eGFR": {SHORT[x]: rec["n_stop"][x] for x in ARMS},
        "asks": {"potassium_above_5_5_patients": {SHORT[x]: a["A_k"][x] for x in ARMS},
                 "hyperkalaemia_events_began_on_treatment": {SHORT[x]: a["A_ae"][x] for x in ARMS},
                 "stopped_for_good_before_week52": {SHORT[x]: a["B_stop"][x] for x in ARMS},
                 "years_on_drug_before_week52": {SHORT[x]: round(a["B_years"][x], 1) for x in ARMS}},
        "conventions": {"trial_weeks": 52, "months": 36, "month36_week": 156, "fit_weeks": [24, 32, 40, 52],
                        "easing_visit_weeks": [12, 16, 20], "potassium_threshold_mmol_l": 5.5},
        "note": _r(rec.get("note", {})),
    }
    return f


def chart(rec, path_png):
    fig, ax = plt.subplots(figsize=(7.4, 3.9), dpi=200)
    for d in DOSES:
        s = rec["diff"][d]
        wk = np.array(s.index, float)
        ax.plot(wk * 12 / 52.0, s.to_numpy(float), "o-", color=COL[d], ms=2.8, lw=1.1)
        a, b = rec["int24"][d], rec["slope24"][d]
        xm = np.linspace(24, 156, 60)
        ax.plot(xm * 12 / 52.0, a + b * xm / 52.0, "--", color=COL[d], lw=1.2)
        v36 = a + b * 3.0
        lab = ("%+d" % whole(v36)) if whole(v36) else "0"
        ax.text(36.4, v36, "%s  %s" % (SHORT[d], lab), color=COL[d], fontsize=7.6, va="center", fontweight="bold")
    ax.axhline(0, color="#333333", lw=0.8)
    ax.axvline(24 * 12 / 52.0, color="#999999", lw=0.6, ls=":")
    ax.text(24 * 12 / 52.0 + 0.3, ax.get_ylim()[0] + 0.3, "week 24", fontsize=6.8, color="#666666")
    ax.set_xlim(0, 41)
    ax.set_xticks([0, 3, 6, 12, 18, 24, 30, 36])
    ax.set_xlabel("Months of treatment (points: VMK-4410-202 visits; dashed: chronic phase from week 24 carried forward)", fontsize=7.4)
    ax.set_ylabel("eGFR difference from placebo\n(mL/min/1.73 m2)", fontsize=7.6)
    ax.tick_params(labelsize=7.4)
    ax.set_title("eGFR difference from placebo by month, each VMK-4410 dose", fontsize=9.4, loc="left", fontweight="bold")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(path_png, dpi=200, metadata={"Software": None})
    plt.close(fig)


def recommendation_pdf(rec, f, path):
    tmp_png = path + ".chart.png"
    chart(rec, tmp_png)
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13.0, spaceAfter=5)
    head = ParagraphStyle("h", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, spaceBefore=7, spaceAfter=3)
    title = ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=13.2, alignment=0, leading=17, spaceAfter=6)
    small = ParagraphStyle("s", parent=body, fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", parent=body, fontSize=8.6, leading=10.6, spaceAfter=0)
    cellb = ParagraphStyle("cb", parent=cell, fontName="Helvetica-Bold")
    dd = f["diff36"]
    rows = [[Paragraph(x, cellb) for x in ("Dose", "eGFR difference from placebo after 36 months' treatment (mL/min/1.73 m2)",
                                           "Chronic phase, weeks 24 to 52 (difference from placebo, mL/min/1.73 m2 a year)")]]
    for d in ["VMK-4410 20 mg", "VMK-4410 40 mg", "VMK-4410 10 mg", "VMK-4410 5 mg"]:
        rows.append([Paragraph(x, cell) for x in (d, "%+d" % dd[SHORT[d]] if dd[SHORT[d]] else "0", "%+.1f" % f["slope_per_year"][SHORT[d]])])
    tb = Table(rows, colWidths=[34 * mm, 68 * mm, 68 * mm])
    tb.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#9a9a9a")),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6eaef")),
                            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#e7f2ec"))]))
    e, lp = f["eased"], f["loop"]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=17 * mm,
                            bottomMargin=17 * mm, title="VMK-4410 phase 3 dose", author="Biostatistics",
                            creator="Biostatistics", invariant=1)
    flow = [
        Paragraph("Varnmark Therapeutics A/S, Biostatistics, for the VMK-4410 end-of-phase-2 meeting package. 12 October "
                  "2026. Prepared by Nicolaj Lassen for Benedicte Laursen.", small),
        Spacer(1, 4),
        Paragraph("Take VMK-4410 20 mg into VMK-4410-301: after 36 months' treatment eGFR would be %d mL/min/1.73 m2 higher "
                  "than on placebo, against %d on 40 mg" % (dd["20 mg"], dd["40 mg"]), title),
        Paragraph("On the phase 3 synopsis's primary estimand (every randomised patient as randomised, as if each stayed on "
                  "the assigned dose, central CKD-EPI 2021 eGFR, change from baseline to the month-36 visit), 20 mg leaves "
                  "eGFR %d mL/min/1.73 m2 above placebo at month 36, 40 mg %d, 10 mg %d and 5 mg %d. The runner-up is 40 mg, "
                  "%d mL/min/1.73 m2 behind." % (dd["20 mg"], dd["40 mg"], dd["10 mg"], dd["5 mg"], f["gap36"]), body),
        tb,
        Spacer(1, 6),
        Image(tmp_png, width=170 * mm, height=89 * mm),
        Paragraph("Why the chronic phase starts at week 24", head),
        Paragraph("Every dose lowers eGFR in the first weeks, and more so on 20 and 40 mg in patients already on a loop "
                  "diuretic. The protocol kept background diuretics unchanged until the week-12 visit; on the day of the "
                  "week-12, 16 or 20 visit investigators reduced or stopped the loop diuretic of %d of the %d patients on "
                  "one on 40 mg and %d of %d on 20 mg (%d of %d on placebo). Those patients recovered part of the fall over the "
                  "following weeks, so the 40 mg arm's difference from placebo rose by %.1f mL/min/1.73 m2 between weeks 12 "
                  "and 24 and by %.1f a year after that. The rise is a one-off recovery of level, not the drug's long-run "
                  "effect, and the phase 3 repeats the same twelve-week rule, so its patients recover the same way. The "
                  "chronic phase is fitted from week 24, when the recovery is complete, to week 52, and carried to month 36 "
                  "from the level each arm settled at."
                  % (e["40 mg"], lp["40 mg"], e["20 mg"], lp["20 mg"], e["Placebo"], lp["Placebo"],
                     f["rise_12_24"]["40 mg"], f["slope_per_year"]["40 mg"]), body),
        Paragraph("Read with the chronic phase starting at month 3, the usual split, the recovery is counted as a slope and "
                  "carried for three years: 40 mg would read %d and 20 mg %d. The week-52 difference alone, before any "
                  "projection, ranks 10 mg first because it still carries the full early fall of the higher doses."
                  % (f["default_month3"]["40 mg"], f["default_month3"]["20 mg"]), body),
        Paragraph("How the figures were worked out", head),
        Paragraph("Central laboratory eGFR at the scheduled visits (the first sample of a visit), baseline the mean of the "
                  "screening and day-1 values, each patient's change from baseline; values from samples taken after a "
                  "patient's last dose set aside for the patients who stopped study drug for good, read from the dosing "
                  "record. Each arm's mean change at each visit less placebo's; a straight line through each dose's "
                  "differences at weeks 24, 32, 40 and 52, read at week 156. Differences are to the nearest whole "
                  "mL/min/1.73 m2.", body),
        Paragraph("40 mg would overtake 20 mg only if its chronic benefit over placebo were larger than 20 mg's by more than "
                  "%.1f mL/min/1.73 m2 a year." % f["flip_slope_per_year"], small),
    ]

    def footer(canvas, d_):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 9 * mm, "Varnmark Therapeutics A/S: VMK-4410 phase 3 dose, from VMK-4410-202")
        canvas.drawRightString(190 * mm, 9 * mm, "Page %d" % d_.page)
        canvas.restoreState()
    doc.build(flow, onFirstPage=footer, onLaterPages=footer)
    os.remove(tmp_png)
    postprocess.scrub(path, P.ORG, "2026-10-12")


def tables_xlsx(f, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Hyperkalaemia"
    _hdr(ws, ["Arm", "Patients with a serum potassium above 5.5 mmol/L on treatment",
              "Hyperkalaemia adverse events that began on treatment"])
    a = f["asks"]
    for r, x in enumerate(ARMS, start=2):
        for j, v in enumerate([x, a["potassium_above_5_5_patients"][SHORT[x]], a["hyperkalaemia_events_began_on_treatment"][SHORT[x]]], start=1):
            ws.cell(row=r, column=j, value=v)
    _w(ws, [18, 30, 30])
    ws.freeze_panes = "A2"
    ws = wb.create_sheet("Exposure")
    _hdr(ws, ["Arm", "Patients who stopped study drug for good before their week-52 visit",
              "Years on study drug before the week-52 visit"])
    for r, x in enumerate(ARMS, start=2):
        for j, v in enumerate([x, a["stopped_for_good_before_week52"][SHORT[x]], a["years_on_drug_before_week52"][SHORT[x]]], start=1):
            c = ws.cell(row=r, column=j, value=v)
            if j == 3:
                c.number_format = "0.0"
    _w(ws, [18, 30, 26])
    ws.freeze_panes = "A2"
    ws = wb.create_sheet("Notes")
    notes = ["VMK-4410-202: hyperkalaemia and exposure by arm (database locked 14 April 2026)",
             "Arms as randomised; every randomised patient took study drug as randomised.",
             "Serum potassium: every reported value from the central laboratory and the sites' local laboratories (mEq/L is the same as mmol/L), "
             "from samples taken after the first dose up to and including the day of the last dose.",
             "Hyperkalaemia events: the preferred terms Hyperkalaemia and Blood potassium increased, counted once per event (the records an event's group "
             "identifier ties together), when the event began between the first dose and the last dose; partial onset dates imputed as the SAP sets out.",
             "Stopped for good: no study drug taken after the last dose, by the dosing record, and that last dose before the week-52 visit "
             "(patients who left the study before week 52 included).",
             "Years on study drug: the days on which study drug was taken, each day once, before the week-52 visit date (all days for patients without "
             "one), divided by 365.25."]
    for r, t in enumerate(notes, start=1):
        c = ws.cell(row=r, column=1, value=t)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if r == 1:
            c.font = Font(bold=True)
    _w(ws, [130])
    wb.save(path)
    postprocess.scrub(path, "Nicolaj Lassen", "2026-10-12")
    postprocess.finish_office(path, "2026-10-09T07:40:00Z", "2026-10-12T12:18:00Z", P.ORG)


def _hdr(ws, cols):
    for j, c in enumerate(cols, start=1):
        cell = ws.cell(row=1, column=j, value=c)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="DDE4EE")
        cell.alignment = Alignment(wrap_text=True, vertical="top")


def _w(ws, widths):
    for j, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(j)].width = w


def write(rec, golden_dir, figures_path):
    os.makedirs(golden_dir, exist_ok=True)
    f = figures(rec)
    recommendation_pdf(rec, f, os.path.join(golden_dir, "VMK-4410_phase3_dose_recommendation.pdf"))
    tables_xlsx(f, os.path.join(golden_dir, "VMK-4410_phase2b_tables.xlsx"))
    with open(figures_path, "w") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
    return golden_dir, f
