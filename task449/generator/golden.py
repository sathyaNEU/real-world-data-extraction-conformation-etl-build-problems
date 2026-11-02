"""The golden deliverables, computed from target/ alone: the Minister's briefing note (docx, with its chart) and the
certification tables (xlsx); and the figures the write-up states."""
import datetime as dt
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import analysis as A    # noqa: E402
import asks as K        # noqa: E402
import common as C      # noqa: E402

ISSUED = dt.datetime(2026, 11, 16, 15, 20)
THRESHOLD = 1.5


def r1(x):
    """One decimal, half away from zero (the Bureau's rounding of a ratio)."""
    import decimal
    return float(decimal.Decimal(repr(x)).quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_HALF_UP))


def titles(tgt):
    import pandas as pd
    c = pd.read_csv(os.path.join(tgt, "noc_2016_v1.3_to_noc_2021_v1.0.csv"), dtype=str)
    return dict(zip(c["noc_2021"], c["noc_2021_title"]))


def compute(tgt):
    main = A.compute(tgt)
    ask = K.golden(tgt)
    t = titles(tgt)
    rows = []
    for o in main["J"]:
        rows.append({"noc": o, "title": t[o], "J": main["J"][o], "V": main["V"][o], "R": main["R"][o],
                     "listed": o in main["listed"]})
    rows.sort(key=lambda r: r["noc"])
    return {"rows": rows, "listed": main["listed"], "ask": ask}


def chart_png(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = sorted(res["rows"], key=lambda r: r["R"])
    fig, ax = plt.subplots(figsize=(6.6, 7.4), dpi=150)
    y = list(range(len(rows)))
    cols = ["#1f4e79" if r["listed"] else "#a6b8c8" for r in rows]
    ax.barh(y, [r["R"] for r in rows], color=cols, height=0.7)
    ax.set_yticks(y)
    ax.set_yticklabels(["%s %s" % (r["noc"], _short(r["title"])) for r in rows], fontsize=6.5)
    ax.axvline(THRESHOLD, color="#c00000", lw=1.2)
    ax.text(THRESHOLD + 0.03, len(rows) - 0.6, "1.5", color="#c00000", fontsize=7.5, va="top")
    ax.set_xlabel("Registered jobseekers per vacancy, four reference dates combined", fontsize=7.5)
    ax.tick_params(axis="x", labelsize=7)
    ax.set_xlim(0, max(r["R"] for r in rows) * 1.08)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_title("Schedule A occupations, 2027 test (dark bars meet the test)", fontsize=8.5, loc="left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _short(t):
    t = t.replace(" (except industrial and power system)", "").replace(" and related occupations", "")
    t = t.replace(", truck and bus mechanics and mechanical repairers", " and mechanics")
    t = t.replace(" and related support occupations", "").replace(", poultry preparers and related workers", "")
    return t if len(t) <= 46 else t[:44].rstrip(" ,") + "..."


def write_briefing(res, path):
    import docx
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.shared import Pt, Inches, RGBColor
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = Inches(0.9)
    sec.top_margin = sec.bottom_margin = Inches(0.8)

    def para(text, bold=False, size=None, space=4, italic=False, color=None):
        p = d.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        p.paragraph_format.space_after = Pt(space)
        return p

    para("Provincial Statistics Bureau | Labour Market Statistics", size=9, color="555555", space=2)
    para("BRIEFING NOTE FOR THE MINISTER OF LABOUR, SKILLS AND IMMIGRATION", bold=True, size=12.5, space=6)
    meta = d.add_table(rows=4, cols=2)
    meta.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, (k, v) in enumerate([("Subject", "Certification of the In-Demand Occupations Order, 2027"),
                                ("Date", "16 November 2026"),
                                ("Prepared by", "Cody Riddle, Senior Analyst, Labour Market Statistics"),
                                ("Approved by", "Sherri Underwood, Manager, Labour Market Statistics")]):
        meta.cell(i, 0).text = k
        meta.cell(i, 1).text = v
        meta.cell(i, 0).paragraphs[0].runs[0].bold = True
        meta.cell(i, 0).width = Inches(1.3)
        meta.cell(i, 1).width = Inches(5.2)
    para("", space=2)
    listed = [r for r in res["rows"] if r["listed"]]
    others = [r for r in res["rows"] if not r["listed"]]
    para("Certification", bold=True, size=11, space=3)
    para("%s of the %d Schedule A occupations meet the 2027 test of no more than 1.5 registered jobseekers per "
         "vacancy over the four reference dates (31 December 2025, 31 March, 30 June and 30 September 2026). The "
         "Bureau certifies them for the order:" % (_word(len(listed)).capitalize(), len(res["rows"])))
    t = d.add_table(rows=1, cols=3)
    t.style = "Light Grid Accent 1"
    hdr = t.rows[0].cells
    for c, h in zip(hdr, ["NOC 2021", "Occupation", "Jobseekers per vacancy"]):
        c.text = h
        c.paragraphs[0].runs[0].bold = True
    for r in listed:
        cells = t.add_row().cells
        cells[0].text = r["noc"]
        cells[1].text = r["title"]
        cells[2].text = "%.1f" % r1(r["R"])
    for row in t.rows:
        row.cells[0].width = Inches(0.9)
        row.cells[1].width = Inches(4.3)
        row.cells[2].width = Inches(1.4)
    para("", space=2)
    para("The other %s occupations do not meet the test: %s." % (_word(len(others)),
                                                                ", ".join(r["noc"] for r in others)))
    para("How the vacancies were counted", bold=True, size=11, space=3)
    para("The survey's estimate for each industry sector on each reference date is shared among occupations by the "
         "positions in the Workshore Job Board postings live that day, each posting placed in a sector by its "
         "employer's NAICS code. A posting Employer Services manages comes down on the day the employer reports the "
         "outcome, so it counts in full. A self-service posting stays up until the employer takes it down or its "
         "42-day term runs out, and most employers leave a filled job's posting up: a posting that was renewed, or "
         "taken down after the reference date, counts in full, and one that ran to the end of its term counts by the "
         "chance its job was still open at its age, read from how long Employer Services vacancies in the same "
         "occupation stayed open before they closed.")
    para("Counting every live self-service posting as an open job lists %s and leaves out %s, because filled jobs "
         "in the fast-filling occupations stay on the board until their terms end."
         % (_join(res["default_extra"]), _join(res["default_missing"])))
    d.add_picture(io.BytesIO(chart_png(res)), width=Inches(5.6))
    para("Figure 1. Registered jobseekers per vacancy, Schedule A occupations. Source: Provincial Statistics Bureau "
         "from the Quarterly Employer Vacancy Survey and Workshore records.", italic=True, size=8.5, space=8)
    para("Employer Services referrals in Schedule A occupations", bold=True, size=11, space=3)
    para("Workshore clients who started a job Employer Services referred them to, by quarter of the start:")
    a = res["ask"]
    t2 = d.add_table(rows=1, cols=4)
    t2.style = "Light Grid Accent 1"
    for c, h in zip(t2.rows[0].cells, ["Quarter", "Clients who started", "Still with the employer at 90 days",
                                       "Average days, referral to start"]):
        c.text = h
        c.paragraphs[0].runs[0].bold = True
    for k, q in enumerate(K.QLABEL):
        cells = t2.add_row().cells
        cells[0].text = q
        cells[1].text = C.fmt_int(a["starts"][k])
        cells[2].text = C.fmt_int(a["retained"][k])
        cells[3].text = "%.1f" % r1(a["avg_days"][k])
    para("", space=2)
    para("A start is dated from the client's job report, not the start date given at hire; a job counts as ended "
         "before 90 days on a client or consultant report or a Record of Employment from the employer.", size=9)
    para("Next step", bold=True, size=11, space=3)
    para("The Minister makes the order by 1 December 2026. The Bureau's tables are in in_demand_2027_tables.xlsx.")
    C.save_docx(d, path, ISSUED, "Provincial Statistics Bureau")


def _word(n):
    w = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
         17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty", 21: "twenty-one", 22: "twenty-two"}
    return w.get(n, str(n))


def _join(codes):
    codes = list(codes)
    if len(codes) <= 1:
        return "".join(codes)
    return ", ".join(codes[:-1]) + " and " + codes[-1]


def write_tables(res, path):
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Schedule A"
    ws.append(["In-Demand Occupations Order, 2027: test results by Schedule A occupation"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Registered jobseekers and vacancies summed over 31 Dec 2025, 31 Mar 2026, 30 Jun 2026 and 30 Sep 2026"])
    ws.append([])
    ws.append(["NOC 2021", "Occupation", "Registered jobseekers", "Vacancies", "Jobseekers per vacancy",
               "Meets the test"])
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    fill = PatternFill("solid", fgColor="DDEBF7")
    for r in res["rows"]:
        ws.append([r["noc"], r["title"], r["J"], round(r["V"]), r1(r["R"]), "Yes" if r["listed"] else "No"])
        row = ws.max_row
        ws.cell(row=row, column=3).number_format = "#,##0"
        ws.cell(row=row, column=4).number_format = "#,##0"
        ws.cell(row=row, column=5).number_format = "0.0"
        if r["listed"]:
            for col in range(1, 7):
                ws.cell(row=row, column=col).fill = fill
    ws.append([])
    ws.append(["Source: Provincial Statistics Bureau, from the Quarterly Employer Vacancy Survey (Q3 2026 release) and "
               "Workshore records extracted 14 November 2026."])
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 62
    for col in "CDEF":
        ws.column_dimensions[col].width = 14
    ws2 = wb.create_sheet("Referrals")
    ws2.append(["Employer Services referrals in Schedule A occupations, by quarter of the client's start"])
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append([])
    ws2.append(["Quarter", "Clients who started", "Still with the employer 90 days after starting",
                "Average days from referral to start"])
    for c in ws2[3]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    a = res["ask"]
    for k, q in enumerate(K.QLABEL):
        ws2.append([q, a["starts"][k], a["retained"][k], r1(a["avg_days"][k])])
        ws2.cell(row=ws2.max_row, column=4).number_format = "0.0"
    ws2.append([])
    ws2.append(["Source: Workshore referral records (both platforms), client job reports and Records of Employment "
                "received to 14 November 2026."])
    ws2.column_dimensions["A"].width = 16
    for col in "BCD":
        ws2.column_dimensions[col].width = 20
    C.save_workbook(wb, path, ISSUED, "Provincial Statistics Bureau")


def write_golden(tgt, gld):
    os.makedirs(gld, exist_ok=True)
    res = compute(tgt)
    live = A.compute(tgt, mode="live")
    res["default_extra"] = sorted(set(live["listed"]) - set(res["listed"]))
    res["default_missing"] = sorted(set(res["listed"]) - set(live["listed"]))
    write_briefing(res, os.path.join(gld, "in_demand_2027_briefing.docx"))
    write_tables(res, os.path.join(gld, "in_demand_2027_tables.xlsx"))
    return res


def figures(res, tgt):
    live = A.compute(tgt, mode="live")
    f = {
        "listed": res["listed"],
        "listed_count": len(res["listed"]),
        "not_listed": [r["noc"] for r in res["rows"] if not r["listed"]],
        "schedule_a_count": len(res["rows"]),
        "threshold": THRESHOLD,
        "term_days": 42,
        "retain_days": 90,
        "default_listed": live["listed"],
        "default_extra": sorted(set(live["listed"]) - set(res["listed"])),
        "default_missing": sorted(set(res["listed"]) - set(live["listed"])),
        "default_count": len(live["listed"]),
    }
    for r in res["rows"]:
        if r["listed"]:
            f["ratio_%s" % r["noc"]] = "%.1f" % r1(r["R"])
    for o in live["listed"]:
        f["default_ratio_%s" % o] = "%.1f" % r1(live["R"][o])
    a = res["ask"]
    for k in range(4):
        f["starts_q%d" % (k + 1)] = a["starts"][k]
        f["retained_q%d" % (k + 1)] = a["retained"][k]
        f["avg_days_q%d" % (k + 1)] = "%.1f" % r1(a["avg_days"][k])
    return f
