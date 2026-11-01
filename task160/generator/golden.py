"""The golden deliverables: the forecast workbook and the go-live memo with its chart, written from target/ through
analysis.py, plus figures.json for figures_check.py."""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import docx  # noqa: E402
from docx.shared import Inches, Pt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402

import analysis as A  # noqa: E402
import io_util as IO  # noqa: E402

BOOK = "msp26_review_forecast_q1_2027.xlsx"
MEMO = "msp26_go_live_review_memo.docx"
NAMES = {"4N": "4 North Medicine", "4S": "4 South Medicine", "9E": "9 East Medicine", "9W": "9 West Medicine",
         "2N": "2 North Medicine", "12N": "12 North Medicine", "11N": "11 North Geriatrics",
         "11S": "11 South Pulmonary", "3E": "3 East Stroke and Spine", "3W": "3 West Renal", "6E": "6 East Orthopaedics",
         "6W": "6 West General Surgery", "10N": "10 North Surgery", "10S": "10 South Surgery",
         "5W": "5 West Vascular Surgery"}
MONTH_NAME = {"2026-07": "July 2026", "2026-08": "August 2026", "2026-09": "September 2026"}
HEAD = Font(bold=True)
FILL = PatternFill("solid", fgColor="DCE6EE")


def chart(b, path):
    fig, ax = plt.subplots(figsize=(6.4, 3.3), dpi=150)
    x = np.arange(3)
    wdt = 0.26
    cols = {"Day": "#2f5d7c", "Evening": "#7fa7c4", "Night": "#c9a24a"}
    for i, s in enumerate(A.SHIFTS):
        vals = [b[(m, s)] for m in A.MONTHS]
        bars = ax.bar(x + (i - 1) * wdt, vals, wdt, label=s, color=cols[s])
        for rect, v in zip(bars, vals):
            ax.text(rect.get_x() + rect.get_width() / 2, v + 4, str(v), ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels([MONTH_NAME[m] for m in A.MONTHS], fontsize=8)
    ax.set_ylabel("Reviews signed off", fontsize=8)
    ax.tick_params(axis="y", labelsize=7)
    tot = sum(b.values())
    day = sum(b[(m, "Day")] for m in A.MONTHS)
    ax.set_title("Day shift signed off %d%% of Quillfield's reviews, July to September 2026" % round(100.0 * day / tot),
                 fontsize=9)
    ax.legend(fontsize=7, frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, max(b.values()) * 1.15)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def workbook(P, g, a, b, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Forecast"
    ws.append(["MSP26 go-live: about %d more override reviews from Quillfield's adult wards in the first 13 weeks"
               % A.r100(g["net"])])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Thirteen weeks from Monday 4 January 2027 to Sunday 4 April 2027, against the same weeks without "
               "the go-live (Schedule B 4.3)"])
    ws.append([])
    ws.append(["", "Reviews, 13 weeks", "Rounded"])
    for c in ws[4]:
        c.font = HEAD
    ws.append(["Reviews the QT combination alert adds", round(g["qt_add"], 1), A.r100(g["qt_add"])])
    ws.append(["Current reviews that no longer reach the desk", -round(g["pre"], 1), -A.r100(g["pre"])])
    ws.append(["Net change in override reviews", round(g["net"], 1), A.r100(g["net"])])
    for c in ws[7]:
        c.font = HEAD
        c.fill = FILL
    ws.append([])
    ws.append(["Working"])
    ws["A9"].font = HEAD
    rows = [
        ("Pilot units (7W, 5E, 8N), duplicate PRN opioid alerts answered by removing the order", "%.0f%%" % (100 * g["c"])),
        ("Pilot units, QT combination alerts overridden", "%.0f%%" % (100 * g["p"])),
        ("Base period", "6 July to 25 October 2026 (background log, 16 weeks)"),
        ("QT combination alerts in the background log, orders not removed", g["qt_rows_B"]),
        ("Overridden high-severity alerts on the wards going live", g["reviews_B"]),
        ("Expected reviews lost, base period", round(g["pre_B"], 1)),
        ("Net change, base period", round(g["net_B"], 1)),
        ("Admissions to the wards going live, base period", g["adm_B"]),
        ("Planned admissions, 13 weeks from 4 January 2027", g["plan_adm"]),
        ("Scale (planned over base admissions)", round(g["scale"], 4)),
    ]
    for r in rows:
        ws.append(list(r))
    ws.append([])
    ws.append(["A current review is lost when its own order, or the active order it fired against, would be removed "
               "at a package alert: removal at the duplicate PRN opioid alert at the pilot units' rate, and at a QT "
               "combination alert at one minus the pilot override share."])
    ws.column_dimensions["A"].width = 78
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 10
    h = wb.create_sheet("Desk hours Q3 2026")
    h.append(["Department", "Ward", "Desk hours, July to September 2026"])
    for c in h[1]:
        c.font = HEAD
    for u in P.going_live:
        h.append([u, NAMES[u], int(np.floor(a[u] + 0.5))])
    h.append([])
    h.append(["Desk time from claim to sign-off or return, every session; ward is the department the alert fired "
              "in, from the alert history."])
    for col, wdt in zip("ABC", (12, 28, 34)):
        h.column_dimensions[col].width = wdt
    h.freeze_panes = "A2"
    s = wb.create_sheet("Signed off by shift")
    s.append(["Month", "Day (07:00 to 15:00)", "Evening (15:00 to 23:00)", "Night (23:00 to 07:00)", "Total"])
    for c in s[1]:
        c.font = HEAD
    for m in A.MONTHS:
        vals = [b[(m, x)] for x in A.SHIFTS]
        s.append([MONTH_NAME[m]] + vals + [sum(vals)])
    s.append([])
    s.append(["One review per overridden alert; month and shift of sign-off, Eastern time."])
    for col, wdt in zip("ABCDE", (18, 20, 24, 22, 10)):
        s.column_dimensions[col].width = wdt
    s.freeze_panes = "B2"
    nt = wb.create_sheet("Notes")
    for line in ["Basis: Schedule B 4.3, the reviews the adult wards will send with MSP26 live against the same weeks "
                 "without it; one overridden alert is one review (2.1).",
                 "Extracts through Sunday 25 October 2026; prepared 28 October 2026.",
                 "7W, 5E and 8N have run MSP26 live since 9 September 2024 and are unchanged by the go-live.",
                 "Volumes on Quillfield's FY2027 inpatient volume plan (Schedule B 4.1)."]:
        nt.append([line])
    nt.column_dimensions["A"].width = 110
    for row in ws.iter_rows(min_row=10, max_row=19):
        row[0].alignment = Alignment(wrap_text=False)
    wb.save(path)
    IO.repack_ooxml(path, "Desk Planning", "Desk Planning", "2026-10-28T13:40:00Z", "2026-10-28T19:05:00Z",
                    "MSP26 review forecast Q1 2027", "Corvane Remote Pharmacy")


def memo(P, g, b, png, path):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("MSP26 go-live: about %d more override reviews in the first 13 weeks" % A.r100(g["net"]), level=1)
    p = d.add_paragraph()
    p.add_run("To: ").bold = True
    p.add_run("Override Review Service Manager    ")
    p.add_run("From: ").bold = True
    p.add_run("Desk Planning    ")
    p.add_run("Date: ").bold = True
    p.add_run("28 October 2026    ")
    p.add_run("Ref: ").bold = True
    p.add_run("CR-2291")
    d.add_paragraph(
        "When both MSP26 rules go live on every adult ward on 4 January 2027, the desk should plan for about %d more "
        "override reviews from Quillfield over the thirteen weeks to 4 April 2027 than it would get without the "
        "go-live (Schedule B 4.3)." % A.r100(g["net"]))
    d.add_paragraph(
        "The background log's QT combination alerts, overridden at the pilot units' %.0f per cent, add about %d "
        "reviews. Against that, the duplicate PRN opioid alert is answered on the pilot units by removing the new "
        "order %.0f per cent of the time, and a removed order no longer carries its own alerts or has severe "
        "interaction alerts fire against it later in the stay. Tying each background duplicate-opioid alert to the "
        "overridden alerts today on that order, or naming it as the interacting order, takes about %d current "
        "reviews off the desk. The base period is 6 July to 25 October 2026, scaled to the volume plan's admissions "
        "for the thirteen weeks." % (100 * g["p"], A.r100(g["qt_add"]), 100 * g["c"], A.r100(g["pre"])))
    t = d.add_table(rows=1, cols=2)
    t.style = "Light Grid Accent 1"
    t.rows[0].cells[0].text, t.rows[0].cells[1].text = "Thirteen weeks from 4 January 2027", "Reviews"
    for k, v in (("Added by the QT combination alert", "+%d" % A.r100(g["qt_add"])),
                 ("Current reviews no longer reaching the desk", "-%d" % A.r100(g["pre"])),
                 ("Net change", "+%d" % A.r100(g["net"]))):
        c = t.add_row().cells
        c[0].text, c[1].text = k, v
    d.add_paragraph("Source: Quillfield medication alert history and MSP26 background log to 25 October 2026; FY2027 "
                    "inpatient volume plan. Reviews from 7W, 5E and 8N do not change: the package has run live there "
                    "since September 2024.")
    d.add_paragraph("For the shift mix, the desk signed off these Quillfield reviews last quarter:")
    d.add_picture(png, width=Inches(6.0))
    tot = sum(b.values())
    d.add_paragraph("%d reviews in all from July to September 2026, one per overridden alert, by the shift and month "
                    "of sign-off (Eastern time). Source: Corvane queue export, matched to the alert history." % tot)
    d.core_properties.author = "Desk Planning"
    d.save(path)
    IO.repack_ooxml(path, "Desk Planning", "Desk Planning", "2026-10-28T15:02:00Z", "2026-10-28T19:12:00Z",
                    "MSP26 go-live review forecast", "Corvane Remote Pharmacy")


def write_all(target, golden, gen):
    os.makedirs(golden, exist_ok=True)
    os.makedirs(gen, exist_ok=True)
    P = A.Pack(target)
    g = P.golden()
    a = P.ask_a()
    b = P.ask_b()
    png = os.path.join(gen, "signed_off_by_shift.png")
    chart(b, png)
    workbook(P, g, a, b, os.path.join(golden, BOOK))
    memo(P, g, b, png, os.path.join(golden, MEMO))
    figs = A.figures(P)
    working = {"pilot_duplicate_removal_pct": round(100 * g["c"]), "pilot_qt_override_pct": round(100 * g["p"]),
               "pilot_qt_removal_pct": 100 - round(100 * g["p"]), "base_qt_alerts": g["qt_rows_B"],
               "base_qt_reviews_added": round(g["qt_add_B"]), "base_reviews": g["reviews_B"],
               "base_reviews_lost": round(g["pre_B"]), "plan_admissions": g["plan_adm"], "base_admissions": g["adm_B"],
               "qt_added_unrounded": round(g["qt_add"]), "lost_unrounded": round(g["pre"]),
               "net_unrounded": round(g["net"]), "rounding_unit": 100,
               "signed_off_total": sum(b.values())}
    json.dump({"task": "task160", "figures": figs, "working": working}, open(os.path.join(gen, "figures.json"), "w"),
              indent=1, sort_keys=True)
    return figs
