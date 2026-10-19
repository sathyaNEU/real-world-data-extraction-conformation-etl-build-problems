"""The goldens and figures.json, every figure computed from the shipped pack: the site selection workbook
(arv1102_site_selection.xlsx) and the chart of the eight clinics (arv1102_clinic_decline.png)."""
import os
from decimal import ROUND_HALF_UP, Decimal

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import analysis as A
import common as K
import pack as PK

WB = "arv1102_site_selection.xlsx"
CHART = "arv1102_clinic_decline.png"


def half_up(x, nd=0):
    q = Decimal(1).scaleb(-nd)
    return float(Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP))


def half_point(x):
    """To the nearest half point, halves of a half rounding up."""
    return half_up(2.0 * float(x)) / 2.0


def compute(target):
    P = PK.load(target)
    res = A.main(P)
    a, a_rows = A.ask_a(P)
    b, b_rows = A.ask_b(P)
    dec = res["decline"]
    fig = dict(
        call=dict(sites=res["sites"], below=res["below"], order=res["order"]),
        decline={c: half_point(dec[c]) for c in K.NAMES},
        gain=half_point(res["gain"]),
        ask_a=dict(under_follow_up={c: a[c]["under"] for c in K.NAMES},
                   aged_85_or_under={c: a[c]["age_ok"] for c in K.NAMES}),
        ask_b=dict(within_42_days_pct={c: half_up(b[c]["share"], 1) for c in K.NAMES},
                   average_days={c: half_up(b[c]["mean"], 1) for c in K.NAMES}),
        terms=dict(six_weeks_days=K.SIX_WEEKS, age_limit=K.AGE_LIMIT),
        counts=dict(patients_compared=int(res["n"].sum()),
                    patients_by_clinic={c: int(res["n"].get(c, 0)) for c in K.NAMES},
                    diagnosed_by_clinic={c: b[c]["n"] for c in K.NAMES}),
    )
    res.update(ask_a=a, ask_b=b, a_rows=a_rows, b_rows=b_rows, P=P)
    return fig, res


THIN = Side(style="thin", color="B9C3CA")
HEAD = PatternFill("solid", fgColor="DCE6EE")
PICK = PatternFill("solid", fgColor="E3EEF6")


def _head(ws, row):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")


def _print(ws, titles):
    """Landscape, one page wide, the header row repeated: the committee pack is printed."""
    ws.print_title_rows = titles
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0


def write_workbook(path, fig, res):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Recruiting sites"
    s1, s2 = fig["call"]["sites"]
    ws.append(["Recruiting sites for ARV-1102: %s and %s" % (s1, s2)])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Decline in cognition, 1 January 2022 to 30 September 2026, as paper RC/26/11 section 3 defines it. "
               "First clinic below the two sites: %s." % fig["call"]["below"]])
    ws.append([])
    ws.append(["Clinic", "Decline, ACE-III points a year", "Rank", "Recruiting site"])
    _head(ws, 4)
    for i, c in enumerate(fig["call"]["order"]):
        ws.append([c, fig["decline"][c], i + 1, "Yes" if c in fig["call"]["sites"] else None])
        r = ws.max_row
        ws.cell(r, 2).number_format = "0.0"
        ws.cell(r, 2).alignment = Alignment(horizontal="right")
        if c in fig["call"]["sites"]:
            for cell in ws[r]:
                cell.fill = PICK
        if i == 1:
            for cell in ws[r]:
                cell.border = Border(bottom=Side(style="medium", color="005EB8"))
    ws.append([])
    ws.append(["Gain at the second completed assessment, ACE-III points", fig["gain"]])
    ws.cell(ws.max_row, 2).number_format = "0.0"
    for col, w in zip("ABCD", (52, 16, 8, 15)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    _print(ws, "4:4")

    f = wb.create_sheet("Questionnaire B")
    f.append(["Clinic", "B1 Alzheimer's disease or MCI under follow-up, 30 September 2026",
              "B2 Of whom 85 or under on 1 January 2027"])
    _head(f, 1)
    for c in K.NAMES:
        f.append([c, fig["ask_a"]["under_follow_up"][c], fig["ask_a"]["aged_85_or_under"][c]])
        for k in (2, 3):
            f.cell(f.max_row, k).number_format = "#,##0"
    f.append(["All clinics", sum(fig["ask_a"]["under_follow_up"].values()),
              sum(fig["ask_a"]["aged_85_or_under"].values())])
    for cell in f[f.max_row]:
        cell.font = Font(bold=True)
    for k in (2, 3):
        f.cell(f.max_row, k).number_format = "#,##0"
    for col, w in zip("ABC", (16, 30, 26)):
        f.column_dimensions[col].width = w
    f.freeze_panes = "B2"
    _print(f, "1:1")

    g = wb.create_sheet("Questionnaire C")
    g.append(["Clinic", "Patients given a diagnosis, 1 October 2025 to 30 September 2026",
              "C1 Diagnosed within 42 days of referral (%)", "C2 Average days, referral to diagnosis"])
    _head(g, 1)
    for c in K.NAMES:
        g.append([c, fig["counts"]["diagnosed_by_clinic"][c], fig["ask_b"]["within_42_days_pct"][c],
                  fig["ask_b"]["average_days"][c]])
        g.cell(g.max_row, 2).number_format = "#,##0"
        g.cell(g.max_row, 3).number_format = "0.0"
        g.cell(g.max_row, 4).number_format = "0.0"
    for col, w in zip("ABCD", (16, 24, 22, 22)):
        g.column_dimensions[col].width = w
    g.freeze_panes = "B2"
    _print(g, "1:1")

    n = wb.create_sheet("Notes")
    notes = [
        "Decline: each patient's ACE-III totals in the period, net of the gain a patient's second completed "
        "assessment carries from having sat the test before, fitted as a straight line in time; the clinic's figure "
        "is the average of its patients' slopes. The gain, %.1f points, is estimated within patients from everyone "
        "with three or more completed assessments in the period: each patient's own intercept and slope, one step "
        "from the second completed assessment of their life on. It comes once, so a slope drawn through a patient's "
        "first two or three assessments understates their decline, most at clinics whose patients are new to the "
        "test." % fig["gain"],
        "Patients: Alzheimer's disease (F00, G30) or mild cognitive impairment (F06.7) as the latest diagnosis on the "
        "record on 30 September 2026, two or more completed assessments in the period, counted at the clinic of the "
        "last (%s patients). CIS forms are joined to the EPR through the master patient index, merged numbers "
        "included; abandoned forms, incomplete sets and sets entered in error are left out." %
        format(fig["counts"]["patients_compared"], ","),
        "B1 and B2: episodes open on 30 September 2026, less the patients the appointments show discharged at a "
        "review, or handed to the care home liaison team, between the start of their episode and that day (the EPR "
        "ends an episode when the letter goes, so some were still open in the extract of 2 October), and less deaths "
        "on the NHS Spine. Age on 1 January 2027 from the master patient index.",
        "C1 and C2: the pathway tracker's referral date to the appointment at which the patient was given their "
        "diagnosis (the EPR outcome 'diagnosis given'). The tracker's diagnosis date is the day the diagnosis went on "
        "the problem list, often some days later.",
        "Prepared by %s, Lead for Dementia Research, for the Research Committee of 21 October 2026. EPR extracts of 2 "
        "October 2026." % K.PEOPLE["lead"],
    ]
    for line in notes:
        n.append([line])
    n.column_dimensions["A"].width = 120
    for row in n.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def write_chart(path, fig, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    order = fig["call"]["order"]
    sites = fig["call"]["sites"]
    v = [float(res["decline"][c]) for c in order]
    fg, ax = plt.subplots(figsize=(8.6, 4.8), dpi=150)
    y = np.arange(len(order))[::-1]
    ax.barh(y, v, height=0.62, color=["#005eb8" if c in sites else "#a9bccb" for c in order])
    ax.set_yticks(y)
    ax.set_yticklabels(["%s  %.1f" % (c, fig["decline"][c]) for c in order])
    ax.axhline(y[1] - 0.5, color="#2b3a67", lw=1.0, ls="--")
    ax.text(5.9, y[1] - 0.42, "recruiting sites", ha="right", va="bottom", fontsize=8.6, color="#2b3a67")
    ax.set_xlim(0, 6)
    ax.set_xlabel("Decline in ACE-III points a year, 2022 to September 2026 (to the nearest half point)")
    ax.spines[["top", "right"]].set_visible(False)
    fg.suptitle("%s and %s: the fastest decline once the second assessment's gain is taken out" % (sites[0], sites[1]),
                x=0.012, ha="left", fontsize=11.2, fontweight="bold", color="#1f2428")
    fg.text(0.01, 0.01, "Average of each patient's own decline, Alzheimer's disease or MCI, two or more completed "
                        "ACE-III assessments in the period (paper RC/26/11, section 3).", fontsize=7.4, color="#5d646a")
    fg.tight_layout(rect=(0, 0.04, 1, 0.95))
    fg.savefig(path, metadata={"Software": None})
    plt.close(fg)


def write(target, golden):
    fig, res = compute(target)
    if os.path.exists(golden):
        for f in os.listdir(golden):
            os.remove(os.path.join(golden, f))
    os.makedirs(golden, exist_ok=True)
    write_workbook(os.path.join(golden, WB), fig, res)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(golden, WB), K.PEOPLE["lead"], K.PEOPLE["lead"], "2026-10-12T09:10:00Z",
                       "2026-10-14T16:35:00Z", title="ARV-1102 recruiting sites", excel=True)
    write_chart(os.path.join(golden, CHART), fig, res)
    return fig, res
