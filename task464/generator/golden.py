"""task464 architecture 12: the golden deliverables, written from figures.json and the pack.

    restart_series_2027.xlsx   the sizing, the pilot sends' restart funnel, the loss by mailbox group and send, basis
    restart_series_2027.docx   the leadership team note with one chart of each send's restarts
"""
import io
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Mm, Pt, RGBColor  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import answers as A  # noqa: E402
import world as W  # noqa: E402

GOLD = os.path.join(BASE, "golden")
GROUP_LABEL = {"gmail": "Google (gmail)", "microsoft": "Microsoft (hotmail, outlook, live)", "yahoo_aol": "Yahoo and AOL"}
INK = "1F3A5F"


def detail(tgt):
    wh = A.Warehouse(tgt)
    days = A.pilot_days()
    nm = sum(wh.n(A.SENDS[0], g, "restart_pilot_mailed") for g in A.GROUPS)
    nh = sum(wh.n(A.SENDS[0], g, "restart_pilot_holdout") for g in A.GROUPS)
    cm = sum(wh.total(d, g, "restart_pilot_mailed") for d in days for g in A.GROUPS)
    ch = sum(wh.total(d, g, "restart_pilot_holdout") for d in days for g in A.GROUPS)
    per, aff, ctl = A.damage(wh, "event")
    logged = A.restarts_by_send(tgt, "plain")
    return {"nm": nm, "nh": nh, "cm": int(cm), "ch": int(ch), "per": per, "aff": aff, "ctl": ctl,
            "logged": [len(s) for s in logged]}


def workbook(fig, det):
    wb = Workbook()
    thin = Side(style="thin", color="B7C3D0")
    head_fill = PatternFill("solid", fgColor="DCE6F0")
    bold = Font(bold=True)
    ws = wb.active
    ws.title = "Sizing"
    ws["A1"] = "Restart series: the pilot's sends cost more sponsored clicks than they brought back"
    ws["A1"].font = Font(bold=True, size=13, color=INK)
    ws["A2"] = "Quaywork CRM, 24 November 2026. Sponsored clicks as the click system records them for billing."
    ws["A2"].font = Font(italic=True, size=9)
    rows = [
        ("Paused jobseekers in the pilot pool on 1 April 2026, mailed arm", det["nm"], "#,##0", "jobseekers"),
        ("Paused jobseekers in the pilot pool on 1 April 2026, held out", det["nh"], "#,##0", "jobseekers"),
        ("Sponsored clicks over the six 28-day windows, mailed arm", det["cm"], "#,##0", "clicks"),
        ("Sponsored clicks over the six 28-day windows, held out", det["ch"], "#,##0", "clicks"),
        ("Clicks per jobseeker, mailed arm", det["cm"] / det["nm"], "0.0000", "per jobseeker"),
        ("Clicks per jobseeker, held out", det["ch"] / det["nh"], "0.0000", "per jobseeker"),
        ("Gain among the paused pool (mailed arm against the holdout)", fig["pilot_uplift_exact"], "#,##0", "clicks"),
        ("Loss among jobseekers with alerts on, Google, Microsoft and Yahoo addresses", -fig["pilot_loss_exact"], "#,##0", "clicks"),
        ("Net effect of the pilot on Quaywork's sponsored clicks", fig["pilot_net_exact"], "#,##0", "clicks"),
        ("Net effect per send (six sends)", fig["pilot_net_exact"] / 6.0, "#,##0", "clicks"),
        ("2027 sizing: thirteen sends at the average pilot send", fig["series_2027_clicks_exact"], "#,##0", "clicks a year"),
    ]
    ws.append([])
    ws.append(["Step", "Value", "Unit", "At the plan's rounding"])
    for c in ws[4]:
        c.font = bold
        c.fill = head_fill
    rounded = {6: fig["pilot_uplift_clicks"], 7: -fig["pilot_loss_clicks"], 8: fig["pilot_net_clicks"],
               10: fig["series_2027_clicks"]}
    for i, (lab, val, fmt, unit) in enumerate(rows):
        ws.append([lab, round(val, 4) if fmt == "0.0000" else round(val), unit, rounded.get(i, None)])
        r = ws.max_row
        ws.cell(r, 2).number_format = fmt
        ws.cell(r, 4).number_format = "#,##0;-#,##0"
        for c in range(1, 5):
            ws.cell(r, c).border = Border(bottom=thin)
    last = ws.max_row
    for c in range(1, 5):
        ws.cell(last, c).font = Font(bold=True, color=INK)
    ws.append([])
    ws.append(["Recommendation: drop the restart series from the 2027 plan; it does not add sponsored clicks."])
    ws.cell(ws.max_row, 1).font = Font(bold=True)
    ws.column_dimensions["A"].width = 74
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 16
    ws.column_dimensions["D"].width = 22
    ws.freeze_panes = "A5"

    s2 = wb.create_sheet("Pilot sends")
    s2.append(["Send", "Date", "Restarts logged from the send's link", "Gateway passes removed",
               "Restarted by people", "Of whom clicked a sponsored job, send date to 27 days after"])
    for c in s2[1]:
        c.font = bold
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for k in range(6):
        s2.append([A.RS[k], A.SENDS[k], det["logged"][k], det["logged"][k] - fig["restarted_by_people"][k],
                   fig["restarted_by_people"][k], fig["clicked_within_28_days"][k]])
        s2.cell(s2.max_row, 2).number_format = "dd mmm yyyy"
        for c in (3, 4, 5, 6):
            s2.cell(s2.max_row, c).number_format = "#,##0"
    s2.append(["Total", None, sum(det["logged"]), sum(det["logged"]) - sum(fig["restarted_by_people"]),
               sum(fig["restarted_by_people"]), sum(fig["clicked_within_28_days"])])
    for c in s2[s2.max_row]:
        c.font = bold
    for c in (3, 4, 5, 6):
        s2.cell(s2.max_row, c).number_format = "#,##0"
    for col, w in zip("ABCDEF", [10, 13, 20, 16, 14, 26]):
        s2.column_dimensions[col].width = w
    s2.row_dimensions[1].height = 45
    s2.freeze_panes = "A2"

    s3 = wb.create_sheet("Loss by group and send")
    s3.append(["Mailbox group"] + A.RS + ["Total"])
    for c in s3[1]:
        c.font = bold
        c.fill = head_fill
    for g in det["aff"]:
        v = det["per"][g]
        s3.append([GROUP_LABEL.get(g, g)] + [round(x) for x in v] + [round(sum(v))])
        for c in range(2, 9):
            s3.cell(s3.max_row, c).number_format = "#,##0"
    s3.append(["All three"] + [round(sum(det["per"][g][k] for g in det["aff"])) for k in range(6)] +
              [round(fig["pilot_loss_exact"])])
    for c in s3[s3.max_row]:
        c.font = bold
    for c in range(2, 9):
        s3.cell(s3.max_row, c).number_format = "#,##0"
    s3.append([])
    s3.append(["Days 0 to 13 after each send, every channel, against the pooled rate of %s at each group's ratio "
               "on days 14 to 27 of the same window." % ", ".join(det["ctl"])])
    s3.cell(s3.max_row, 1).font = Font(italic=True, size=9)
    s3.column_dimensions["A"].width = 34
    for col in "BCDEFGH":
        s3.column_dimensions[col].width = 11

    s4 = wb.create_sheet("Basis")
    notes = [
        ("As of", "Warehouse extract to 8 November 2026; the pilot's six 28-day windows run 14 April to 28 September 2026."),
        ("Measure", "Sponsored clicks as the click system records them for billing, every channel (the alert email, "
                    "the website, the app), per jobseeker per day from sponsored_clicks_by_mailbox_daily.csv."),
        ("Judged on", "Jobseeker email plan 2027, section 5: the clicks Quaywork takes with a programme against "
                      "without it, each send over the 28 days from it, the 2027 series at the average pilot send times thirteen."),
        ("Counted once", "The warehouse reload sent 20, 21 and 22 October 2026 twice; each day is counted once. From 1 "
                         "October 2026 the app channel arrives as app_ios and app_android and is summed."),
        ("Restarts", "A restart counts as a person's when the send's email was not opened link by link by a "
                     "gateway (four or more links from one subscriber inside ten seconds in Postvane's click events)."),
        ("Clicked", "A restarter counts once if the CRM pull shows a sponsored click dated from the send's date to 27 "
                    "days after it, before or after the restart; the pull and the restart log are on the UK clock, "
                    "Postvane's events in UTC."),
        ("Rounding", "Exact counts in the tables; the plan's figures to the nearest 50,000 (the pilot) and 100,000 (2027)."),
    ]
    s4.append(["Item", "Note"])
    for c in s4[1]:
        c.font = bold
        c.fill = head_fill
    for k, v in notes:
        s4.append([k, v])
        s4.cell(s4.max_row, 2).alignment = Alignment(wrap_text=True, vertical="top")
    s4.column_dimensions["A"].width = 14
    s4.column_dimensions["B"].width = 110
    wb.save(os.path.join(GOLD, "restart_series_2027.xlsx"))


def chart(fig):
    x = list(range(6))
    a1 = fig["restarted_by_people"]
    a2 = fig["clicked_within_28_days"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    f, ax = plt.subplots(figsize=(6.4, 3.3), dpi=200)
    w = 0.38
    b1 = ax.bar([i - w / 2 for i in x], a1, w, color="#1F3A5F", label="Restarted their alerts themselves")
    b2 = ax.bar([i + w / 2 for i in x], a2, w, color="#7FA7C9", label="Of whom clicked a sponsored job, send date to 27 days after")
    for b, v in list(zip(b1, a1)) + list(zip(b2, a2)):
        ax.text(b.get_x() + b.get_width() / 2, v + 120, "{:,}".format(v), ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels(["%s\n%s" % (A.RS[k], A.SENDS[k].strftime("%d %b")) for k in x], fontsize=8)
    ax.set_ylabel("Jobseekers")
    ax.set_title("Restarts by people fell from {:,} at the first send to {:,} at the sixth".format(a1[0], a1[-1]),
                 fontsize=10, loc="left", color="#1F3A5F")
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: "{:,.0f}".format(v)))
    ax.set_ylim(0, max(a1) * 1.15)
    ax.legend(frameon=False, fontsize=7.5, loc="upper right")
    f.tight_layout()
    buf = io.BytesIO()
    f.savefig(buf, format="png", metadata={"Software": None})
    plt.close(f)
    buf.seek(0)
    return buf


def note(fig, det):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    meta = d.add_paragraph()
    meta.add_run("To: ").bold = True
    meta.add_run("Leadership team, meeting of 7 December 2026\n")
    meta.add_run("From: ").bold = True
    meta.add_run("%s, CRM Analyst, for %s\n" % (W.PEOPLE["analyst"], W.PEOPLE["head"]))
    meta.add_run("Date: ").bold = True
    meta.add_run("24 November 2026\n")
    meta.add_run("Subject: ").bold = True
    meta.add_run("The restart series in the 2027 jobseeker email plan")
    t = d.add_paragraph()
    r = t.add_run("Drop the restart series from the 2027 plan: its thirteen sends would cost about 300,000 "
                  "sponsored clicks a year.")
    r.bold = True
    r.font.size = Pt(12.5)
    r.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
    d.add_paragraph(
        "The pilot did bring paused jobseekers back. Over its six 28-day windows the mailed arm made {:.3f} sponsored "
        "clicks per jobseeker against {:.3f} for the held-out tenth, a gain of about 100,000 clicks among the paused "
        "pool. But every "
        "send went out from the same domain as the daily alerts, to addresses that had gone unread for months, and in "
        "the fortnight after each one the alerts of jobseekers with Google, Microsoft and Yahoo addresses drew "
        "markedly fewer sponsored clicks, even after the clicks those jobseekers made on the site and app instead. "
        "Read against the six mailbox groups that never moved, that loss comes to about 250,000 clicks over the pilot."
        .format(fig["mailed_clicks_per_jobseeker"], fig["holdout_clicks_per_jobseeker"]))
    d.add_paragraph(
        "Netting the two, the pilot cost Quaywork about 150,000 sponsored clicks. Sized as the plan asks, at the "
        "average pilot send thirteen times, the 2027 series would cost about 300,000 clicks a year. The plan keeps a "
        "programme only if it adds sponsored clicks, so the restart series should not stay. Paused jobseekers keep "
        "the site and app routes to restart.")
    tb = d.add_table(rows=1, cols=2)
    tb.style = "Light List Accent 1"
    tb.rows[0].cells[0].text = "Sizing (sponsored clicks)"
    tb.rows[0].cells[1].text = "Figure"
    for lab, v in [("Gain among the paused pool, six sends", "{:,}".format(fig["pilot_uplift_clicks"])),
                   ("Loss among jobseekers with alerts on", "{:,}".format(-fig["pilot_loss_clicks"])),
                   ("Net effect of the pilot", "{:,}".format(fig["pilot_net_clicks"])),
                   ("2027, thirteen sends", "{:,}".format(fig["series_2027_clicks"]))]:
        c = tb.add_row().cells
        c[0].text = lab
        c[1].text = v
        c[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    src = d.add_paragraph("Source: sponsored_clicks_by_mailbox_daily.csv; the pilot's figures to the nearest 50,000, "
                          "2027 to the nearest 100,000.")
    src.runs[0].font.size = Pt(8)
    src.runs[0].italic = True
    d.add_paragraph(
        "Of the restarts the alert system logged from each send's link, {:,} in all, {:,} were gateways at university "
        "and business addresses opening every link of the email in one pass; they are left out of the restart counts "
        "below.".format(sum(det["logged"]), sum(det["logged"]) - sum(fig["restarted_by_people"])))
    d.add_picture(chart(fig), width=Mm(160))
    cap = d.add_paragraph("Each pilot send's restarts by people and, of them, those who clicked a sponsored job on the "
                          "send's date or in the 27 days after it, before or after restarting (app clicks made logged "
                          "out included where the device is theirs).")
    cap.runs[0].font.size = Pt(8)
    cap.runs[0].italic = True
    cp = d.core_properties
    cp.author = W.PEOPLE["analyst"]
    cp.last_modified_by = W.PEOPLE["analyst"]
    cp.title = "The restart series in the 2027 jobseeker email plan"
    import datetime as dt
    cp.created = dt.datetime(2026, 11, 24, 10, 5, 0)
    cp.modified = dt.datetime(2026, 11, 24, 17, 35, 0)
    cp.revision = 4
    d.save(os.path.join(GOLD, "restart_series_2027.docx"))


def main(fig):
    os.makedirs(GOLD, exist_ok=True)
    tgt = os.path.join(BASE, "target")
    det = detail(tgt)
    workbook(fig, det)
    note(fig, det)


if __name__ == "__main__":
    import json
    main(json.load(open(os.path.join(HERE, "figures.json"))))
