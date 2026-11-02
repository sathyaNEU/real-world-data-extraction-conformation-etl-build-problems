"""The golden deliverables: review_horizon_workbook_2027.xlsx (the settings, the members by setting, the unit's
reviews by town) and review_horizon_board_paper_2027.docx (the recommendation to the Board with the coverage chart),
plus generator/figures.json and metadata.json."""
import datetime as dt
import json
import os
import shutil
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
from openpyxl import Workbook            # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402

import analysis as A                     # noqa: E402
import common as K                       # noqa: E402
import postprocess as PP                 # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CHART = "share_by_years_after_first_exposure.png"


def r1(x):
    """A share as a per cent to one decimal, rounded half up on the exact value."""
    return float("%.1f" % (round(x * 1000 + 1e-9) / 10.0))


def results(target, T):
    sched = T["unit"]
    m = A.main_call(target)
    o = dict(main=m)
    o["share"] = {H: r1(m["golden"][H]) for H in K.SETTINGS}
    o["call"] = m["golden_setting"]
    o["runner_up"] = K.SETTINGS[K.SETTINGS.index(o["call"]) - 1]
    o["reviews"] = A.ask_reviews(target, sched)
    o["members"], o["members_seen"], o["members_list"] = A.ask_members(target, sched)
    o["natural_reviews"] = A.ask_reviews(target, sched, handle_swaps=False, handle_blanks=False)
    o["natural_members"], _, _ = A.ask_members(target, sched, handle_blanks=False)
    return o


def _head(ws, row, head, widths):
    for j, h in enumerate(head, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2E4A62")
        c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[c.column_letter].width = widths[j - 1]


def workbook(path, o):
    wb = Workbook()
    ws = wb.active
    ws.title = "Horizon"
    ws["A1"] = "Review horizon for the 2027-2031 term: share of the workforce's mesotheliomas by setting"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Fund register as closed for 2025-26 (diagnoses 1 July 2004 to 30 June 2026), workers first exposed "
                "before 1 January 1986; each case weighted for the years its own exposure date let the register see it.")
    _head(ws, 4, ["Setting (years after first exposure)", "Share diagnosed within the setting (%)",
                  "Nine in ten reached", "Recommended"], [22, 22, 14, 13])
    for i, H in enumerate(K.SETTINGS):
        vals = [H, o["share"][H], "Yes" if o["share"][H] >= 90.0 else "No", "Recommended" if H == o["call"] else None]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=5 + i, column=j, value=v)
            if j == 2:
                c.number_format = "0.0"
    ws.cell(row=13, column=1, value="Register cases in the estimate").font = Font(italic=True)
    ws.cell(row=13, column=2, value=o["main"]["n"])
    b = wb.create_sheet("Members by setting")
    b["A1"] = "Members reviewed in 2025-26 who would still be inside each setting on 1 July 2027"
    b["A1"].font = Font(bold=True, size=12)
    _head(b, 3, ["Setting (years after first exposure)", "Members still inside the setting"], [22, 20])
    for i, H in enumerate(K.ASK_SETTINGS):
        b.cell(row=4 + i, column=1, value=H)
        b.cell(row=4 + i, column=2, value=o["members"][H]).number_format = "#,##0"
    b.cell(row=11, column=1, value="Members reviewed in 2025-26").font = Font(italic=True)
    b.cell(row=11, column=2, value=o["members_seen"]).number_format = "#,##0"
    b.freeze_panes = "A4"
    ws.freeze_panes = "A5"
    c = wb.create_sheet("Unit reviews 2025-26")
    c["A1"] = "Mobile Review Unit: reviews held in each circuit town, 1 July 2025 to 30 June 2026"
    c["A1"].font = Font(bold=True, size=12)
    _head(c, 3, ["Town", "Reviews held"], [18, 14])
    for i, t in enumerate(sorted(K.CIRCUIT)):
        c.cell(row=4 + i, column=1, value=t)
        c.cell(row=4 + i, column=2, value=o["reviews"][t])
    c.cell(row=4 + len(K.CIRCUIT), column=1, value="All towns").font = Font(bold=True)
    tot = c.cell(row=4 + len(K.CIRCUIT), column=2, value=sum(o["reviews"][t] for t in K.CIRCUIT))
    tot.font = Font(bold=True)
    tot.number_format = "#,##0"
    c.freeze_panes = "A4"
    n = wb.create_sheet("Notes")
    n.column_dimensions["A"].width = 110
    notes = ["Prepared 12 February 2027 for the Board meeting of 25 February 2027 (item 6).",
             "Horizon: program terms 2027-2031, clause 4. Shares are of every mesothelioma among workers first exposed to "
             "asbestos at work before 1 January 1986, whenever diagnosed (4.2), years at 365.25 days (4.3), no curve "
             "shape assumed (4.4). The setting is read from the unrounded shares; shares shown to one decimal.",
             "Register as closed for 2025-26 (diagnoses 1 July 2004 to 30 June 2026), both case systems. Household, "
             "environmental and unexposed cases, and workers first exposed in 1986 or later, are outside the workforce (2.1).",
             "Members by setting: members with a review in 2025-26, counted once, inside a setting when fewer years than "
             "the setting have passed since first exposure on 1 July 2027 (3.2).",
             "Unit reviews: each booking reviewed on a Mobile Review Unit day, placed in the town the unit worked that "
             "day. Blank attendance rows count as reviews only on the days the unit's X-ray exposure counter shows "
             "them reviewed (the tablet's offline weeks in September 2025 and April 2026)."]
    for i, t in enumerate(notes, 1):
        cell = n.cell(row=i, column=1, value=t)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def chart(path, o):
    x, f = o["main"]["curve"]
    import numpy as np
    xs = np.concatenate([[20 * K.YEAR], x, [86 * K.YEAR]]) / K.YEAR
    ys = np.concatenate([[0.0], np.cumsum(f), [1.0]]) * 100
    fig, ax = plt.subplots(figsize=(7.0, 3.5), dpi=150)
    ax.step(xs, ys, where="post", color="#1f5a7a", lw=1.7)
    ax.axhline(90, color="#7a2e1f", lw=.9, ls=":")
    ax.text(21, 91.3, "Nine in ten (program terms 4.2)", fontsize=7, color="#7a2e1f")
    for H in K.SETTINGS:
        ax.plot([H, H], [0, o["share"][H]], color="#9aa5ad", lw=.6, ls="--")
        ax.plot(H, o["share"][H], "o", ms=3.6, color="#1f5a7a" if H != o["call"] else "#7a2e1f")
        ax.text(H + .5, o["share"][H] - 5.5 if H < 60 else o["share"][H] - 7.5, "%.1f%%" % o["share"][H], fontsize=6.6,
                color="#1d2326", fontweight="bold" if H == o["call"] else "normal")
    ax.set_xlim(20, 80)
    ax.set_ylim(0, 102)
    ax.set_xticks(range(20, 81, 5))
    ax.set_xlabel("Years after first exposure to asbestos at work", fontsize=8)
    ax.set_ylabel("Mesotheliomas diagnosed (cumulative %)", fontsize=8)
    ax.tick_params(labelsize=7.5)
    ax.set_title("Nine in ten of the workforce's mesotheliomas are diagnosed by %d years" % o["call"], fontsize=8.8,
                 loc="left")
    ax.grid(color="#e8ecee", lw=.6)
    ax.set_axisbelow(True)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(left=.08, right=.97, top=.9, bottom=.14)
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def paper(path, o, png):
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Mm, Pt, RGBColor
    GREY = RGBColor(0x5B, 0x64, 0x6B)
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(9.5)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(18)
    sec.top_margin, sec.bottom_margin = Mm(13), Mm(12)
    fp = sec.footer.paragraphs[0]
    fp.text = "Board paper 2027/06  |  Prepared by the Review Program  |  Page "
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    run = fp.add_run()
    for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = txt
        run._r.append(el)
    for r_ in fp.runs:
        r_.font.size = Pt(7.5)
        r_.font.color.rgb = GREY
    hp = sec.header.paragraphs[0]
    hp.text = "%s | Board meeting of 25 February 2027 | Item 6 (for decision)" % K.FUND
    hp.runs[0].font.size = Pt(7.5)
    hp.runs[0].font.color.rgb = GREY

    def para(text="", size=None, bold=False, color=None, after=3, before=0):
        p = doc.add_paragraph()
        if text:
            r = p.add_run(text)
            r.bold = bold
            if size:
                r.font.size = Pt(size)
            if color:
                r.font.color.rgb = color
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.space_before = Pt(before)
        return p

    for k, v in (("To", "The Board"), ("From", "%s, Manager, Review Program" % K.PEOPLE["manager"]),
                 ("Date", "12 February 2027"),
                 ("Subject", "Review Program horizon for the term from 1 July 2027 (program terms, clause 4)")):
        p = para(after=0)
        r = p.add_run("%s:\t" % k)
        r.bold = True
        p.add_run(v)
    sh = o["share"]
    para("Set the horizon at %d years after first exposure" % o["call"], 13, bold=True, before=8, after=4)
    p = para(after=4)
    p.add_run("Recommendation: that the Board set the Program's horizon for 2027-2031 at %d years after first "
              "exposure. On the register, %.1f%% of the workforce's mesotheliomas are diagnosed within %d years, "
              "against %.1f%% within %d years, so %d is the shortest five-year step that reaches the nine in ten "
              "that clause 4.2 asks for." % (o["call"], sh[o["call"]], o["call"], sh[o["runner_up"]],
                                             o["runner_up"], o["call"])).bold = True
    tb = doc.add_table(rows=1, cols=3)
    tb.style = "Light List"
    for i, t in enumerate(["Setting (years after first exposure)", "Mesotheliomas diagnosed within it",
                           "Members reviewed in 2025-26 still inside it on 1 July 2027"]):
        tb.rows[0].cells[i].text = t
    for H in K.SETTINGS:
        cells = tb.add_row().cells
        cells[0].text = "%d%s" % (H, "  (recommended)" if H == o["call"] else "")
        cells[1].text = "%.1f%%" % sh[H]
        cells[2].text = "{:,}".format(o["members"][H]) if H in o["members"] else "-"
        for i in (1, 2):
            cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for row in tb.rows:
        for i, w in enumerate((58, 52, 64)):
            row.cells[i].width = Mm(w)
    para("Source: Fund mesothelioma register as closed for 2025-26, %s cases among workers first exposed before "
         "1 January 1986; members and bookings from the Program's booking system." % "{:,}".format(o["main"]["n"]),
         7.5, color=GREY, before=2, after=0)
    para("Household, environmental and unexposed cases on the register, and workers first exposed in 1986 or later, "
         "are outside the workforce (clause 2.1). The setting is read from the unrounded shares.", 7.5, color=GREY,
         after=6)
    para("How the shares were read", 10.5, bold=True, before=2, after=2)
    para("The register only holds a mesothelioma diagnosed between 1 July 2004 and 30 June 2026. So each worker's "
         "latency can only reach it inside a window that their first exposure fixes: a worker first exposed in "
         "1950 appears only if diagnosed 54 to 76 years later, one first exposed in 1980 only at 24 to 46 years. "
         "Taken as they stand, the register's latencies miss the short latencies of the early workforce (diagnosed "
         "before the Fund began) and the long latencies of the 1970s and 1980s workforce, which are still to come; "
         "most of the workforce started in the 1970s, so the second gap is the bigger one. Read straight off the "
         "register, %.1f%% of cases fall within 55 years; admitting cases only from the Fund's start gives %.1f%%. Both put the horizon at 55 years." % (r1(o["main"]["empirical"][55]),
                                                                               r1(o["main"]["delayed"][55])), after=3)
    para("The shares above weight every case by the chance that its own window catches a latency, estimating the "
         "latency curve and those chances together (the nonparametric maximum likelihood estimate for data seen "
         "between two dates; no curve shape is assumed, per clause 4.4). Years after first exposure run from the "
         "first day of the earliest period of work the exposure assessment marks as exposed to the day of "
         "diagnosis, at 365.25 days a year (clause 4.3).", after=4)
    doc.add_picture(png, width=Mm(170))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    para("For the term's costing", 10.5, bold=True, before=4, after=2)
    rv = o["reviews"]
    top = sorted(K.CIRCUIT, key=lambda t: -rv[t])
    para("Of the members reviewed in 2025-26, %s would still be inside a %d-year horizon on 1 July 2027 (%s inside "
         "%d years). The Mobile Review Unit held {:,} reviews across its fourteen circuit towns in 2025-26, from %d "
         "at %s to %d at %s; the workbook has every town.".format(sum(rv[t] for t in K.CIRCUIT))
         % ("{:,}".format(o["members"][o["call"]]), o["call"], "{:,}".format(o["members"][o["runner_up"]]),
            o["runner_up"], rv[top[0]], top[0], rv[top[-1]], top[-1]), after=3)
    para("Attachments: review_horizon_workbook_2027.xlsx (settings, members by setting, unit reviews by town).", 7.5,
         color=GREY, after=0)
    doc.save(path)


def figures(o):
    m = o["main"]
    return dict(
        call=o["call"], runner_up=o["runner_up"], cover=90.0, settings=K.SETTINGS,
        share={str(H): o["share"][H] for H in K.SETTINGS},
        rungs={k: {str(H): r1(m[k][H]) for H in K.SETTINGS} for k in ("empirical", "delayed", "reverse", "golden")},
        rung_settings={k: m[k + "_setting"] for k in ("empirical", "delayed", "reverse", "golden")},
        cases_in_estimate=m["n"], register_cases=len(A.load_cases(os.path.join(os.path.dirname(HERE), "target"))),
        clauses=["2.1", "2.2", "3.2", "4.1", "4.2", "4.3", "4.4"], midday_window=[t.replace(":", ".") for t in A.MIDDAY],
        members={str(H): o["members"][H] for H in K.ASK_SETTINGS}, members_reviewed=o["members_seen"],
        reviews={t: o["reviews"][t] for t in sorted(K.CIRCUIT)}, reviews_total=sum(o["reviews"][t] for t in K.CIRCUIT),
        natural=dict(reviews={t: o["natural_reviews"][t] for t in sorted(K.CIRCUIT)},
                     members={str(H): o["natural_members"][H] for H in K.ASK_SETTINGS}),
        register_window=["2004-07-01", "2026-06-30"], cohort_before="1986-01-01", year_days=365.25,
        term_start="2027-07-01", fy=["2025-07-01", "2026-06-30"])


PROV = ("constructed for this task by a seeded generator; the Dust Diseases Compensation Fund, its act, register, "
        "program, people, places and workplaces are fictional; the records follow the forms of an Australian state "
        "dust-diseases scheme's case register, interview records, booking system and fleet and equipment logs")


def metadata(target, n):
    cover = {
        "register": ("Mesothelioma register, cases notified from 1 January 2013, as closed for 2025-26", "Registrar",
                     "2026-09-30", "%d rows" % n["register"]),
        "legacy": ("Mesothelioma register, cases notified 1 July 2004 to 31 December 2012 (first case system)",
                   "Registrar", "2013-02-15", "%d rows" % n["legacy"]),
        "histories": ("Occupational histories of every register case as interviewed and assessed", "Exposure assessment unit",
                      "2026-09-30", "%d rows" % n["histories"]),
        "terms": ("Former Asbestos Workers Review Program terms 2027-2031", "Board", "2026-11-27", "2 pages"),
        "report": ("Annual Report 2025-26", "The Fund", "2026-10-21", "2 pages"),
        "members": ("Review Program members at 30 June 2026", "Review Program", "2026-06-30", "%d rows" % n["members"]),
        "appointments": ("Review bookings, 1 July 2023 to 30 June 2026", "Review Program", "2026-07-03",
                         "%d rows" % n["appointments"]),
        "schedule": ("Mobile Review Unit visit schedule 2025-26 as published", "Review Program", "2025-06-16", "1 page"),
        "card": ("Fleet card statement for the Mobile Review Unit, 2025-26", "Fleet Services", "2026-07-06",
                 "%d rows" % n["card"]),
        "qa": ("Mobile Review Unit X-ray daily QA and exposure counter log, 2025-26", "Medical imaging (unit)", "2026-06-30",
               "%d rows, 2 sheets" % n["qa"]),
        "roads": ("Review sites and road distance table from the travel policy", "Finance", "2025-05-26",
                  "%d places" % n["roads"]),
        "registry": ("State Cancer Registry, mesothelioma new cases by year and sex, 1982-2024", "State Cancer Registry",
                     "2025-11-04", "%d years" % n["registry"]),
        "workplaces": ("Register of workplaces where asbestos was used", "Exposure assessment unit", "2024-08-12",
                       "%d rows" % n["workplaces"]),
    }
    prov = {}
    for k, (cov, by, date, size) in cover.items():
        prov["target/" + K.FILES[k]] = dict(covers=cov, prepared_by=by, date=date, size=size, source=PROV,
                                             licence="CC0 1.0 (constructed for this task)")
    return {"distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS], "deliverables": K.DELIVERABLES,
            "as_of": K.ASOF.isoformat(), "stated_inputs": ["2027", "2025-26", "40", "70"], "provenance": prov}


def write(target, golden, T):
    os.makedirs(golden, exist_ok=True)
    for f in os.listdir(golden):
        os.remove(os.path.join(golden, f))
    o = results(target, T)
    xp = os.path.join(golden, K.DELIVERABLES[1])
    workbook(xp, o)
    tmp = tempfile.mkdtemp()
    png = os.path.join(tmp, CHART)
    chart(png, o)
    dp = os.path.join(golden, K.DELIVERABLES[0])
    paper(dp, o, png)
    shutil.rmtree(tmp)
    PP.COMPANY = K.FUND
    PP.normalize_ooxml(xp, K.PEOPLE["manager"], K.PEOPLE["manager"], "2027-02-08T22:14:37Z", "2027-02-12T03:41:15Z",
                       excel=True)
    PP.normalize_ooxml(dp, K.PEOPLE["manager"], K.PEOPLE["manager"], "2027-02-09T23:11:05Z", "2027-02-12T04:02:44Z",
                       title="Review Program horizon for the term from 1 July 2027")
    Fj = figures(o)
    json.dump(Fj, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(metadata(target, T["n"]), open(os.path.join(os.path.dirname(target), "metadata.json"), "w"), indent=2)
    T["o"] = o
    return o, Fj
