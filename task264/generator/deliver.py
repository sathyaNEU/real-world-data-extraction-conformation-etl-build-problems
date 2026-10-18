"""The goldens: levy_apportionment_2027-28.xlsx (the 2027-28 levy schedule, the charging parks' 2025-26 parking
income and vehicles, the 2025-26 levy collection at 31 March 2026) and levy_report_2027-28.docx (the report to
members, with the chart of each council's share on the old and new bases), both from golden.py on the shipped pack;
generator/figures.json, the figures the write-up states; and metadata.json."""
from __future__ import annotations

import json
import os
import shutil
import tempfile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                          # noqa: E402
from openpyxl import Workbook                             # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402

import common as K                                        # noqa: E402
import golden as G                                        # noqa: E402
import postprocess as PP                                  # noqa: E402
import world as W                                         # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVERABLES = ["levy_apportionment_2027-28.xlsx", "levy_report_2027-28.docx"]
DISTRACTORS = ["permits", "population", "payments"]
CHART = "levy_shares_chart.png"


def hundred(x):
    return int(round(x / 100.0)) * 100


def pounds(x):
    return int(G.np.floor(x + .5))


def results(target):
    o = G.compute(target)
    N = o["N"]
    tot = sum(N.values())
    o["share"] = {c: N[c] / tot for c in K.CODES}
    o["old"] = W.apportion(K.LEVY_2026, {c: W.POP[c][1] for c in K.CODES})
    o["old_valley"] = 100 * sum(o["old"][c] for c in K.VALLEY) / K.LEVY_2026
    o["valley_levy"] = sum(o["levy_r"][c] for c in K.VALLEY)
    o["valley_N"] = sum(N[c] for c in K.VALLEY)
    d = o["survey"]
    o["n"] = dict(interviews=len(d), wave1=int((d["case"].str[0] == "1").sum()),
                  wave2=int((d["case"].str[0] == "2").sum()), members=int(d["code"].isin(K.CODES).sum()),
                  out=int((d["code"] == "OUT").sum()), nk=int((d["code"] == "NK").sum()))
    return o


# ---------------------------------------------------------------------------------------------- workbook
HEAD = PatternFill("solid", fgColor="E4E9E1")
THIN = Side(style="thin", color="8C968A")


def _head(ws, head, widths):
    ws.append(head)
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    ws.row_dimensions[ws.max_row].height = 44


def _total(ws):
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
        c.border = Border(top=THIN)


def _fmt(ws, cols, f):
    for col in cols:
        for cell in ws[col][1:]:
            if isinstance(cell.value, (int, float)):
                cell.number_format = f


def workbook(path, o):
    wb = Workbook()
    ws = wb.active
    ws.title = "Levy 2027-28"
    _head(ws, ["Member council", "Residents aged 16 and over who visited in 2025-26 (estimate)", "Share of the levy",
               "Levy 2027-28 (GBP)", "Levy 2026-27 (GBP), by population", "Change (GBP)"], [30, 20, 11, 15, 17, 13])
    for c in K.CODES:
        ws.append([K.NAME[c], hundred(o["N"][c]), round(o["share"][c], 6), o["levy_r"][c], o["old"][c],
                   o["levy_r"][c] - o["old"][c]])
    ws.append(["Total", hundred(sum(o["N"].values())), 1.0, sum(o["levy_r"].values()), sum(o["old"].values()),
               sum(o["levy_r"].values()) - sum(o["old"].values())])
    _total(ws)
    ws.append([])
    ws.append(["Keldmere, Ravenwick and Snelgarth", hundred(o["valley_N"]), round(o["valley"]["golden"] / 100, 6),
               o["valley_levy"], sum(o["old"][c] for c in K.VALLEY), o["valley_levy"] - sum(o["old"][c] for c in K.VALLEY)])
    _fmt(ws, "BDEF", "#,##0;-#,##0")
    _fmt(ws, "C", "0.0%")
    ws.freeze_panes = "B2"

    ws = wb.create_sheet("Car parks 2025-26")
    _head(ws, ["Park", "Paid at the pay machines, net of VAT (GBP)", "Paid through the parking app, net of VAT (GBP)",
               "Paid in all, net of VAT (GBP)", "Vehicles that entered its car parks"], [26, 17, 17, 15, 15])
    for p in K.CHARGING:
        m, a = o["parts"][p]
        ws.append([K.PARK_NAME[p], round(m, 2), round(a, 2), pounds(m + a), int(o["vehicles"][p])])
    ws.append(["Total", round(sum(v[0] for v in o["parts"].values()), 2), round(sum(v[1] for v in o["parts"].values()), 2),
               pounds(sum(o["income"].values())), int(sum(o["vehicles"].values()))])
    _total(ws)
    _fmt(ws, "BC", "#,##0.00")
    _fmt(ws, "DE", "#,##0")
    ws.freeze_panes = "B2"

    ws = wb.create_sheet("Levy 2025-26 collection")
    _head(ws, ["Member council", "Levy 2025-26 invoiced (GBP)", "Paid by the instalments' due dates (GBP)",
               "Paid after the due date, by 31 March 2026 (GBP)", "Unpaid on 31 March 2026 (GBP)"], [30, 16, 18, 18, 16])
    B = o["collection"]
    for c in K.CODES:
        ws.append([K.NAME[c], pounds(B[c]["levy"]), pounds(B[c]["on_time"]), pounds(B[c]["late"]),
                   pounds(B[c]["unpaid"])])
    ws.append(["Total", pounds(sum(B[c]["levy"] for c in K.CODES)), pounds(sum(B[c]["on_time"] for c in K.CODES)),
               pounds(sum(B[c]["late"] for c in K.CODES)), pounds(sum(B[c]["unpaid"] for c in K.CODES))])
    _total(ws)
    _fmt(ws, "BCDE", "#,##0;-#,##0")
    ws.freeze_panes = "B2"

    ws = wb.create_sheet("Notes")
    ws.column_dimensions["A"].width = 118
    n = o["n"]
    for line in [
        "Prepared by Finance for the Authority's meeting of 21 January 2027 (item 7). Figures from the 2025-26 visitor "
        "survey (both waves and the contractor's weights), the car-park systems and the finance system as exported on "
        "6 January 2027.",
        "Residents. Resolution 14/2026 counts each member council's residents aged 16 and over who visited at least once "
        "between 1 April 2025 and 31 March 2026, each once. The survey interviewed adults leaving the parks, every eighth "
        "adult crossing the survey line, so each adult's chance of being interviewed rises with how often they came. Each "
        "interview is counted as its expansion weight (its stratum's estimated adult visits over the stratum's interviews) "
        "divided by the respondent's visits to the six parks in the last 12 months including that day (Q9, the six "
        "parks' answers added, since a resident can be met at any park they visit), which counts each resident once; summed by the home area the contractor coded. %s of the %s interviews were with residents "
        "of the member councils; %s lived outside them and %s gave no home that could be placed, and neither is counted "
        "(paragraphs 4 and 6)." % ("{:,}".format(n["members"]), "{:,}".format(n["interviews"]), "{:,}".format(n["out"]),
                                   n["nk"]),
        "Levy. Each council's share of the 7,416,300 pound requirement is its estimated residents over the nine "
        "councils' total, unrounded; each levy is rounded to the pound (paragraph 5). Residents are shown to the "
        "nearest hundred, and totals are the unrounded estimates added and then rounded, so the rounded figures may not "
        "add to them.",
        "Car parks. Pay-machine takings are each ticket once (three machines re-sent several days' tickets with a "
        "later upload), placed at the park where the machine stood when it took them (PM-2103 stood in Gorthfield's main car "
        "park until it replaced PM-2203 at the Water Park on 1 September 2025; its takings to then are at Gorthfield's "
        "charges), and divided by 1.2 to take out VAT. The app provider's parking income is stated without VAT and is "
        "taken as stated (sessions times charge over 1.2). Vehicles are entries at the car-park counters over the survey "
        "year: C-09, the Water Park's loop from 18 August 2025, counts every vehicle in and out, so its counts are "
        "halved; C-05 and C-10 both reported Gorthfield's lakeside entrance from 3 to 24 February 2026 and the entrance "
        "is counted once; C-07 stood at Thruscote Hall until 14 October 2025, when it moved to Lockshaw Moor's valley car "
        "park and C-11 took its place.",
        "Levy collection. Each receipt counts once against the invoices the cash book allocates it to, each at its own "
        "amount where a council's payment run paid a sundry invoice with an instalment (the receipts listing prints "
        "the receipt's amount on each of its lines), and is dated by the day the bank credited it (the bank's report, "
        "matched on the reference and amount), not the day the finance system posted it: a payment credited on its "
        "due date is on time. The fourth instalments credited on 31 March were posted on 1 April, after the cash "
        "book's year, and are taken from the bank's report against each payer's open invoice: the shared finance "
        "service's transfer pays Hornmere's and Wendstow's, and Ferncote's quoted Grinbury's invoice and is "
        "Ferncote's. Chaldale paid its third instalment at its 2024-25 amount; Grinbury's fourth instalment reached the "
        "bank on 8 April 2026.",
    ]:
        ws.append([line])
        ws.cell(ws.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


# ---------------------------------------------------------------------------------------------- chart
def chart(path, o):
    names = [K.SHORT[c] for c in K.CODES][::-1]
    new = [100 * o["share"][c] for c in K.CODES][::-1]
    old = [100 * o["old"][c] / K.LEVY_2026 for c in K.CODES][::-1]
    fig, ax = plt.subplots(figsize=(7.2, 4.1), dpi=150)
    y = list(range(len(names)))
    ax.barh([v + .19 for v in y], new, height=.36, color="#2f5d50", label="2027-28, residents who visited (resolution 14/2026)")
    ax.barh([v - .19 for v in y], old, height=.36, color="#b9c4b6", label="2026-27, population (resolution 6/1998)")
    for v, a in zip(y, new):
        ax.text(a + .25, v + .19, "%.1f%%" % a, va="center", fontsize=7.2, color="#1d2326")
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8.5)
    for lab in ax.get_yticklabels():
        if lab.get_text() in {K.SHORT[c] for c in K.VALLEY}:
            lab.set_fontweight("bold")
    ax.set_xlabel("Share of the levy (per cent)", fontsize=8.5)
    ax.set_xlim(0, 24)
    ax.tick_params(axis="x", labelsize=8)
    ax.set_title("Keldmere, Ravenwick and Snelgarth pay %.1f per cent of the 2027-28 levy,\nagainst %.1f per cent of "
                 "2026-27's levy on population" % (o["valley"]["golden"], o["old_valley"]), fontsize=9.2, loc="left")
    ax.legend(loc="lower right", fontsize=7.4, frameon=False)
    ax.grid(axis="x", color="#e7ebe6", lw=.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


# ---------------------------------------------------------------------------------------------- report
def report(path, o, png):
    import docx
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Mm, Pt, RGBColor
    GREY = RGBColor(0x5B, 0x64, 0x6B)
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Mm(22)
    hp = sec.header.paragraphs[0]
    hp.text = "%s | Meeting of the Authority, 21 January 2027 | Item 7, annex" % K.AUTH
    hp.runs[0].font.size = Pt(7.5)
    hp.runs[0].font.color.rgb = GREY
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = fp.add_run("Page ")
    run.font.size = Pt(7.5)
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        el = OxmlElement("w:fldChar" if kind else "w:instrText")
        if kind:
            el.set(qn("w:fldCharType"), kind)
        else:
            el.set(qn("xml:space"), "preserve")
            el.text = text
        r2 = fp.add_run()
        r2.font.size = Pt(7.5)
        r2._r.append(el)

    def para(text, size=None, bold=False, color=None, after=5):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color
        p.paragraph_format.space_after = Pt(after)
        return p

    def h(text):
        p = para(text, size=10.5, bold=True, after=3)
        p.paragraph_format.space_before = Pt(9)

    def table(head, rows, right, widths):
        tb = doc.add_table(rows=1, cols=len(head))
        tb.style = "Light List"
        tb.alignment = WD_TABLE_ALIGNMENT.LEFT
        for i, txt in enumerate(head):
            tb.rows[0].cells[i].text = txt
        for r in rows:
            cells = tb.add_row().cells
            for i, v in enumerate(r):
                cells[i].text = v
                if i in right:
                    cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for row in tb.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Mm(w)
                for p in row.cells[i].paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(8.5)
        return tb

    def note(text):
        para(text, size=7.8, color=GREY, after=6)

    m = lambda x: "{:,}".format(int(x))
    N, L = o["N"], o["levy_r"]
    para("The 2027-28 levy of £7,416,300 falls %.1f per cent on Keldmere, Ravenwick and Snelgarth, whose residents use "
         "the parks most" % o["valley"]["golden"], size=13.5, bold=True, color=RGBColor(0x2F, 0x5D, 0x50), after=2)
    para("Apportionment under resolution 14/2026. Report of the Head of Finance. For decision.", size=8.5, color=GREY,
         after=8)

    h("Recommendation")
    para("That the Authority approves the levy on the member councils for 2027-28 as set out in the table below, a total "
         "of £7,416,300, and notifies each council of its levy by 15 February 2027.")
    rows = []
    for c in K.CODES:
        rows.append([K.NAME[c], m(hundred(N[c])), "%.1f%%" % (100 * o["share"][c]), m(L[c]), m(o["old"][c]),
                     ("+" if L[c] >= o["old"][c] else "-") + m(abs(L[c] - o["old"][c]))])
    rows.append(["Total", m(hundred(sum(N.values()))), "100.0%", m(sum(L.values())), m(sum(o["old"].values())),
                 "+" + m(sum(L.values()) - sum(o["old"].values()))])
    table(["Member council", "Residents 16+ who visited, 2025-26", "Share", "Levy 2027-28 (£)", "Levy 2026-27 (£)",
           "Change (£)"], rows, (1, 2, 3, 4, 5), [50, 27, 15, 24, 24, 22])
    note("Residents are estimates from the 2025-26 visitor survey, shown to the nearest hundred; shares, levies and "
         "totals are worked from the unrounded estimates, so the rounded residents may not add to the total, and each "
         "levy is rounded to the pound (resolution 14/2026, paragraph 5). The 2026-27 levy was apportioned by mid-2024 "
         "population (Appendix B to the item 7 papers).")

    h("How each council's residents were counted")
    d = o["n"]
    para("Resolution 14/2026 apportions the levy by the number of each council's residents aged 16 and over who visited "
         "at least one of the six parks between 1 April 2025 and 31 March 2026, each counted once however often they "
         "came, as estimated from the visitor survey. The survey did not set out to count people. Its interviewers "
         "stood at each park's main exit on sampled days and approached every eighth adult leaving, so it is a sample "
         "of visits: a Keldmere resident who walks a dog in Brathden Woods most mornings passes the survey line two "
         "hundred times a year and is two hundred times as likely to be interviewed as a Larkstead family who come once. "
         "The contractor's weights expand each of the %s interviews to the adult visits it stands for in its park, "
         "season and day type." % m(d["interviews"]))
    para("To count people, each interview is weighted by its expansion weight divided by the number of visits the "
         "respondent said they had made to the six parks in the last 12 months, including the day of the interview, "
         "every park counted because the survey could have met them leaving any of them. A respondent who came twice "
         "then stands for half as many people as their weight stands for visits, and one who came two hundred times for "
         "a two-hundredth: across everyone the visit sample can reach, each resident is counted once. "
         "On that basis %s of the nine councils' residents aged 16 and over visited in 2025-26, %s of them from "
         "Keldmere, Ravenwick and Snelgarth." % (m(hundred(sum(N.values()))), m(hundred(o["valley_N"]))))
    para("Two shortcuts give a different split and are not used. Summing the weights by council counts visits, not "
         "residents, and would put %.1f per cent of the levy on the three valley councils. Dividing each council's "
         "visits by its respondents' average visit count looks like a count of people, but in an exit survey that "
         "average is weighted towards the people who come most, because they are the ones most often interviewed; it "
         "overstates how often residents come, most where everyday walkers and occasional visitors mix, and would put "
         "only %.1f per cent on the valley councils. Dividing by the visits to the park where the interview took place "
         "alone counts a resident who walks in two parks once at each, %.1f per cent on the valley councils." % (
             o["valley"]["visits"], o["valley"]["mean"], o["valley"]["here"]))
    doc.add_picture(png, width=Mm(150))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.LEFT
    note("Interviews by home area: %s with residents of the member councils, %s with visitors from elsewhere (not counted, "
         "paragraph 6) and %s whose home could not be placed (not counted, paragraph 4)." % (
             m(d["members"]), m(d["out"]), d["nk"]))

    h("Car parks, 2025-26")
    para("Parking income offsets the levy requirement, and the car-park counts are the base from which the survey's "
         "visits are expanded. For the four charging parks:")
    rows = []
    for p in K.CHARGING:
        mm, aa = o["parts"][p]
        rows.append([K.PARK_NAME[p], m(pounds(mm)), m(pounds(aa)), m(pounds(mm + aa)), m(o["vehicles"][p])])
    rows.append(["Total", m(pounds(sum(v[0] for v in o["parts"].values()))),
                 m(pounds(sum(v[1] for v in o["parts"].values()))), m(pounds(sum(o["income"].values()))),
                 m(sum(o["vehicles"].values()))])
    table(["Park", "Pay machines, net of VAT (£)", "Parking app, net of VAT (£)", "Paid in all, net of VAT (£)",
           "Vehicles entered"], rows, (1, 2, 3, 4), [48, 30, 30, 30, 24])
    note("Machine takings are each ticket once (three machines re-sent several days' tickets with a later upload), at "
         "the park where the machine then stood (PM-2103 was in Gorthfield's main car park until 1 September 2025), less "
         "VAT at 20 per cent. The app provider states parking income without VAT. Vehicles are counter entries: the Water Park's "
         "loop installed on 18 August 2025 counts vehicles in and out and is halved; Gorthfield's lakeside entrance is "
         "counted once while its old and new counters ran side by side in February 2026; counter C-07 counted at "
         "Thruscote Hall until it moved to Lockshaw Moor on 14 October 2025. Rows may not add to the total by a pound.")

    h("The 2025-26 levy at 31 March 2026")
    B = o["collection"]
    rows = [[K.NAME[c], m(B[c]["levy"]), m(B[c]["on_time"]), m(B[c]["late"])] for c in K.CODES]
    rows.append(["Total", m(sum(B[c]["levy"] for c in K.CODES)), m(sum(B[c]["on_time"] for c in K.CODES)),
                 m(sum(B[c]["late"] for c in K.CODES))])
    table(["Member council", "Levy 2025-26 (£)", "Paid by the due dates (£)", "Paid late, by 31 March 2026 (£)"], rows,
          (1, 2, 3), [56, 34, 36, 36])
    late = [c for c in K.CODES if B[c]["late"] > 0]
    clean = [K.NAME[c].split()[0] for c in K.CODES if B[c]["late"] == 0 and B[c]["unpaid"] == 0]
    words = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}
    para("%s councils paid at least one instalment after its due date by 31 March. %s paid every instalment on time; "
         "Grinbury's fourth instalment reached us on 8 April 2026, and Chaldale paid its third instalment at its 2024-25 "
         "amount, leaving £%s unpaid. Payments are dated by the day the bank credited them: the cash book posts each "
         "receipt from the bank's statement the next working day, so a payment made on its due date shows there a day "
         "late, and the fourth instalments paid on 31 March fall in April's postings, outside the finance system's "
         "2025-26 receipts, and are taken from the bank's report. Where a council's payment run paid a sundry invoice "
         "with an instalment, the receipt counts once and the instalment at its own amount." % (
             words[len(late)], " and ".join(clean), m(B["CHD"]["unpaid"])))
    for p in doc.paragraphs:
        p.paragraph_format.line_spacing = 1.08
    doc.core_properties.author = "Finance"
    doc.core_properties.title = "Levy 2027-28: apportionment"
    doc.save(path)


# ---------------------------------------------------------------------------------------------- figures.json
def figures(o):
    N, L = o["N"], o["levy_r"]
    B = o["collection"]
    return dict(
        call=dict(requirement=K.LEVY_2027, levy={K.NAME[c]: L[c] for c in K.CODES},
                  residents={K.NAME[c]: hundred(N[c]) for c in K.CODES}, total_residents=hundred(sum(N.values())),
                  share_pct={K.NAME[c]: round(100 * o["share"][c], 1) for c in K.CODES},
                  valley_share=round(o["valley"]["golden"], 1), valley_levy=o["valley_levy"],
                  valley_residents=hundred(o["valley_N"]), levy_total=sum(L.values())),
        rungs={k: round(v, 1) for k, v in o["valley"].items()},
        old=dict(levy={K.NAME[c]: o["old"][c] for c in K.CODES}, valley_share=round(o["old_valley"], 1),
                 change={K.NAME[c]: L[c] - o["old"][c] for c in K.CODES}),
        counts=o["n"], rate=dict(every=W.EVERY, vat=1.2, strata=len(K.STRATA), q9_months=12),
        ask_a={K.PARK_NAME[p]: dict(machines=pounds(o["parts"][p][0]), app=pounds(o["parts"][p][1]),
                                    total=pounds(o["income"][p])) for p in K.CHARGING},
        ask_a_total=pounds(sum(o["income"].values())),
        ask_b={K.NAME[c]: dict(levy=pounds(B[c]["levy"]), on_time=pounds(B[c]["on_time"]), late=pounds(B[c]["late"]),
                               unpaid=pounds(B[c]["unpaid"])) for c in K.CODES},
        ask_c={K.PARK_NAME[p]: int(o["vehicles"][p]) for p in K.CHARGING},
        ask_c_total=int(sum(o["vehicles"].values())))


def write(target, golden, T=None):
    os.makedirs(golden, exist_ok=True)
    o = results(target)
    xp = os.path.join(golden, DELIVERABLES[0])
    workbook(xp, o)
    tmp = tempfile.mkdtemp()
    png = os.path.join(tmp, CHART)
    chart(png, o)
    dp = os.path.join(golden, DELIVERABLES[1])
    report(dp, o, png)
    shutil.rmtree(tmp)
    PP.COMPANY = K.AUTH
    PP.normalize_ooxml(xp, "Finance", "Finance", "2027-01-11T10:04:37Z", "2027-01-13T16:41:52Z", excel=True)
    PP.normalize_ooxml(dp, "Finance", "Finance", "2027-01-11T10:11:05Z", "2027-01-13T16:52:19Z",
                       title="Levy 2027-28: apportionment")
    F = figures(o)
    json.dump(F, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    meta = {"distractor_files": ["target/" + K.FILES[k] for k in DISTRACTORS],
            "stated_inputs": ["{:,}".format(K.LEVY_2027)]}
    json.dump(meta, open(os.path.join(os.path.dirname(target), "metadata.json"), "w"), indent=2)
    return o, F
