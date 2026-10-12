"""task501 goldens: facility_election_2027.docx (the election paper with the 2026 distributions chart) and
distributions_received_2026.xlsx, written into task501/golden/ from generator/figures.json and the shipped files.
Every figure comes from figures.json or from the same computation in solve.py, and the totals are asserted to tie.
Run after build.py and checks.py."""
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import docx
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S
import world as W
import pack as PK

ROOT = os.path.dirname(HERE)
GOLD = os.path.join(ROOT, "golden")
REPO = os.path.dirname(ROOT)
SCRUB = os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
F = json.load(open(os.path.join(HERE, "figures.json")))
PAPER = "facility_election_2027.docx"
BOOK = "distributions_received_2026.xlsx"
CHART = "distributions_2026_chart.png"
STAMP = (2027, 1, 8, 16, 20, 0)
STRAT_ORDER = ("BO", "GR", "PC", "IN")
NAMES = W.STRATEGIES
COLOURS = {"BO": "#1f4e79", "GR": "#6f9fc9", "PC": "#b8860b", "IN": "#8c8c8c"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def k(x):
    return f"{x:,.0f}"


def m1(x):
    return f"{x:,.1f}"


def long_date(s):
    d = date.fromisoformat(s) if isinstance(s, str) else s
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def fund_names():
    pk = S.Pack()
    return {r["fund_code"]: r["fund_name"] for _, r in pk.reg.iterrows()}, {r["fund_code"]: NAMES[r["strategy"]] for _, r in pk.reg.iterrows()}


# ------------------------------------------------------------------ the chart
def chart(path):
    D = F["distributions_2026_chf_k"]
    top = F["top_strategy"]
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=200)
    xs = [1, 2, 3, 4]
    bottom = [0.0] * 4
    for s in STRAT_ORDER:
        vals = [D[f"{s}_Q{q}"] for q in xs]
        ax.bar(xs, vals, 0.58, bottom=bottom, color=COLOURS[s], edgecolor="white", linewidth=0.6, label=NAMES[s], zorder=3)
        bottom = [b + v for b, v in zip(bottom, vals)]
    for x in xs:
        t = D[f"total_Q{x}"]
        ax.text(x, t + 1800, k(t), ha="center", va="bottom", fontsize=9, fontweight="bold", color="#222222")
    ax.set_xticks(xs)
    ax.set_xticklabels(["Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026"], fontsize=9)
    ax.set_ylabel("CHF thousand", fontsize=9)
    ax.set_ylim(0, max(D[f"total_Q{q}"] for q in xs) * 1.16)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.tick_params(axis="y", labelsize=8.5)
    ax.grid(axis="y", color="#dddddd", linewidth=0.6, zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    tcode = next(s for s in STRAT_ORDER if NAMES[s] == top)
    ax.set_title(f"{top} returned the most cash from distributions in 2026: CHF {k(D[f'{tcode}_year'])} thousand",
                 fontsize=10.5, loc="left", fontweight="bold")
    h, l = ax.get_legend_handles_labels()
    ax.legend(h[::-1], l[::-1], fontsize=8.5, frameon=False, loc="upper right", ncol=1)
    fig.tight_layout()
    fig.savefig(path, dpi=200, metadata={"Software": None})
    plt.close(fig)


# ------------------------------------------------------------------ the paper
def cell_text(cell, text, bold=False, size=8.5, right=False, italic=False):
    cell.text = ""
    p = cell.paragraphs[0]
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(0)
    if right:
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hex_fill)
    tcPr.append(sh)


def table(doc, header, rows, widths, total=False):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    for i, h in enumerate(header):
        cell_text(t.rows[0].cells[i], h, bold=True, right=i > 0 and header[i] not in ("Strategy", "Period ends", "Period ended"))
        shade(t.rows[0].cells[i], "E8EDF3")
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cell_text(cells[i], str(v), bold=total and ri == len(rows) - 1, right=i > 0 and header[i] not in ("Strategy", "Period ends", "Period ended"))
    for i, w in enumerate(widths):
        t.columns[i].width = Cm(w)
        for row in t.rows:
            row.cells[i].width = Cm(w)
    return t


def source(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(7.5)
    r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)


def heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)


def page_field(par):
    def fld(instr):
        r = par.add_run()
        b = OxmlElement("w:fldChar")
        b.set(qn("w:fldCharType"), "begin")
        it = OxmlElement("w:instrText")
        it.set(qn("xml:space"), "preserve")
        it.text = instr
        e = OxmlElement("w:fldChar")
        e.set(qn("w:fldCharType"), "end")
        r._r.append(b)
        r._r.append(it)
        r._r.append(e)
        r.font.size = Pt(7.5)
    r = par.add_run("Page ")
    r.font.size = Pt(7.5)
    fld("PAGE")
    r = par.add_run(" of ")
    r.font.size = Pt(7.5)
    fld("NUMPAGES")


def paper(chart_path):
    names, strat = fund_names()
    fu, six, slow = F["four_funds"], F["six_detail"], F["slow_starters"]
    amt, down = F["call_amount_chf_m"], F["next_amount_down_chf_m"]
    D = F["distributions_2026_chf_k"]
    four = sorted(fu, key=lambda c: fu[c]["ip_end"])
    lo4, hi4 = F["four_drawn_range_pct"]
    lo6, hi6 = F["six_drawn_range_pct"]

    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(9.5)
    st.paragraph_format.space_after = Pt(6)
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Cm(2.2)
        sec.top_margin = Cm(1.8)
        sec.bottom_margin = Cm(1.6)
        fp = sec.footer.paragraphs[0]
        r = fp.add_run(f"{W.ORG} · Treasury & Liquidität · Standby facility 2027 · intern        ")
        r.font.size = Pt(7.5)
        page_field(fp)

    p = doc.add_paragraph()
    r = p.add_run(W.ORG)
    r.bold = True
    r.font.size = Pt(11)
    p.add_run("\nTreasury & Liquidität").font.size = Pt(9)
    p = doc.add_paragraph()
    p.paragraph_format.tab_stops.add_tab_stop(Cm(1.9))
    for label, val in [("To", f"{W.PEOPLE['president']}, President of the Stiftungsrat"),
                       ("From", f"{W.PEOPLE['treasury']}, Head of Treasury & Liquidität"),
                       ("Date", "8 January 2027"),
                       ("Subject", "Standby facility 2027: election of the facility amount (RL-PM-05 sections 4 and 5.3)")]:
        r = p.add_run(f"{label}:\t")
        r.bold = True
        r.font.size = Pt(9)
        r2 = p.add_run(val + ("\n" if label != "Subject" else ""))
        r2.font.size = Pt(9)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    r = p.add_run(f"Elect CHF {amt} million for 2027")
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    doc.add_paragraph(
        f"We propose to elect the 2027 standby facility at CHF {amt} million and to confirm it to {W.BANK} by 15 January. The plan "
        f"under RL-PM-05 puts the programme's expected capital calls for 2027 at CHF {m1(F['expected_calls_chf_m'])} million: the calls "
        f"with a value date in 2027 on the {F['funds_in_register']} commitments in the register at 31 December 2026, translated at the "
        f"plan-date reference rates (USD {F['plan_date_rates']['USD']:.4f}, EUR {F['plan_date_rates']['EUR']:.4f}). One tenth on top makes "
        f"CHF {m1(F['expected_calls_plus_tenth_chf_m'])} million, and with the CHF {F['reserve_chf_m']} million reserve set against it the "
        f"facility has to cover CHF {m1(F['requirement_chf_m'])} million. CHF {down} million would leave CHF "
        f"{m1(F['shortfall_next_down_chf_m'])} million of that open; CHF {amt} million is the smallest amount on the lender's menu that "
        f"covers it.")
    doc.add_paragraph(
        f"Under the term sheet of 9 December the fees for the year come to CHF {F['fees_at_amount_chf']:,} at CHF {amt} million "
        f"(commitment fee CHF {F['commitment_fee_at_amount']:,}, arrangement fee CHF {F['arrangement_fee_at_amount']:,}) and "
        f"CHF {F['fees_at_next_down_chf']:,} at CHF {down} million (CHF {F['commitment_fee_next_down']:,} and "
        f"CHF {F['arrangement_fee_next_down']:,}).")

    heading(doc, "Why the calls rise in 2027")
    nm = [names[c] for c in four]
    doc.add_paragraph(
        f"Half of the expected calls come from four funds that fell behind in the 2023-24 deal drought: {nm[0]}, {nm[1]}, {nm[2]} and "
        f"{nm[3]}. At the end of December they were between {lo4:.1f} and {hi4:.1f} per cent drawn, with CHF "
        f"{m1(F['four_undrawn_chf_m'])} million undrawn between them, and their investment periods end between "
        f"{long_date(fu[four[0]]['ip_end'])} and {long_date(fu[four[-1]]['ip_end'])}. After that a fund may call only for follow-on "
        f"investments in companies it already holds and for partnership expenses, so whatever they still mean to invest has to be "
        f"called before the date.")
    doc.add_paragraph(
        f"Our own record shows how such funds finish. All {F['closed_funds']} funds whose investment period has ended had drawn between "
        f"{F['closed_share_min_pct']:.1f} and {F['closed_share_max_pct']:.1f} per cent of their commitment by its last day, "
        f"{F['closed_share_mean_pct']:.1f} per cent on average, and that includes the five that were as far behind a year out as these four "
        f"are now (table 2). We have planned the four to reach {F['closed_share_mean_pct']:.1f} per cent by their deadlines and to call at "
        f"the programme's post-period rate after them: CHF {m1(F['four_2027_chf_m'])} million in 2027. The programme's call rates by fund "
        f"age, which forecast the 2025 and 2026 calls within {F['backtests_pct']['2025']:.1f} and {F['backtests_pct']['2026']:.1f} per "
        f"cent, would give the same four funds CHF {m1(F['four_default_chf_m'])} million: the funds those rates are measured on were at "
        f"that age with years of investment period still ahead of them. On those rates alone the plan would come to "
        f"CHF {m1(F['default_expected_calls_chf_m'])} million and the facility to CHF {F['default_amount_chf_m']} million.")
    doc.add_paragraph(
        f"The six other funds whose periods end in 2027 are already {lo6:.1f} to {hi6:.1f} per cent drawn and add CHF "
        f"{m1(F['six_2027_chf_m'])} million. The remaining {F['rest_count']} commitments are planned on the programme's call rates on "
        f"unfunded commitment by year of age since each fund's first call, summed calls over summed unfunded commitment across the "
        f"record from 2015: CHF {m1(F['rest_2027_chf_m'])} million.")

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.add_run("Table 1. Funds whose investment periods end in 2027").bold = True
    rows = []
    allten = [(c, fu[c]["ip_end"], fu[c]["drawn_share"], fu[c]["undrawn_chf_k"], fu[c]["calls_2027_chf_k"]) for c in fu] + \
             [(c, six[c]["ip_end"], six[c]["drawn_share"], six[c]["undrawn_chf_k"], six[c]["calls_2027_chf_k"]) for c in six]
    for c, ipe, ds, und, cl in sorted(allten, key=lambda x: x[1]):
        rows.append([names[c], strat[c], long_date(ipe), f"{ds:.1f}%", k(und), k(cl)])
    table(doc, ["Fund", "Strategy", "Period ends", "Drawn 31.12.2026", "Undrawn, CHF thousand", "Planned calls 2027, CHF thousand"], rows,
          [4.9, 2.3, 3.2, 1.9, 2.1, 2.2])
    source(doc, "Source: notice ledger and fund register as at 31 December 2026. Drawn: capital calls with a value date to 31 December 2026 "
                "over commitment. Francs at the plan-date reference rates. Planned calls: the balance to 92.6 per cent of commitment by the "
                "end of the period, then the programme's post-period call rate.")

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.add_run("Table 2. Funds that reached the end of their investment period behind schedule").bold = True
    rows = [[names[c], strat[c], long_date(v["ip_end"]), f"{v['year_before_pct']:.1f}%", f"{v['at_end_pct']:.1f}%"]
            for c, v in sorted(slow.items(), key=lambda kv: kv[1]["ip_end"])]
    table(doc, ["Fund", "Strategy", "Period ended", "Drawn a year before", "Drawn at the end"], rows, [4.9, 2.3, 3.2, 2.9, 2.9])
    source(doc, f"Source: notice ledger, calls by value date over commitment in the fund currency. The other "
                f"{F['closed_funds'] - len(slow)} funds whose periods have ended were at least {F['closed_others_year_before_min_pct']:.1f} "
                f"per cent drawn a year before the end.")

    heading(doc, "Cash received from distributions in 2026")
    doc.add_paragraph(
        f"For the annual liquidity report (RL-PM-05 section 6): the programme account received CHF {k(F['distributions_2026_total_chf_k'])} "
        f"thousand from fund distributions in 2026. {F['top_strategy']} returned the most, CHF "
        f"{k(D[next(s for s in STRAT_ORDER if NAMES[s] == F['top_strategy']) + '_year'])} thousand; the first "
        f"quarter was the strongest, at CHF {k(D['total_Q1'])} thousand. None of it reduces the facility: distributions are swept to "
        f"the general portfolio on the day they arrive and are not credited against calls.")
    doc.add_picture(chart_path, width=Cm(15.6))
    source(doc, "Figure 1. Distributions received on the programme account by quarter of arrival, CHF thousand at the reference rate of "
                "the day the cash arrived. Source: custodian statement of the programme account and notice ledger.")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.add_run("Table 3. Distributions received in 2026, CHF thousand").bold = True
    rows = [[NAMES[s]] + [k(D[f"{s}_Q{q}"]) for q in (1, 2, 3, 4)] + [k(D[f"{s}_year"])] for s in STRAT_ORDER]
    rows.append(["Total"] + [k(D[f"total_Q{q}"]) for q in (1, 2, 3, 4)] + [k(F["distributions_2026_total_chf_k"])])
    table(doc, ["Strategy", "Q1", "Q2", "Q3", "Q4", "Year"], rows, [3.6, 2.5, 2.5, 2.5, 2.5, 2.6], total=True)
    insp = F["in_specie_2026"][0].split(" ")[0]
    wd = F["withdrawn_distributions_2026"][0]
    source(doc, f"Each credit of a distribution on the programme account dated in 2026, at the notice's amount in the fund currency and the "
                f"reference rate of the credit's value date, by the quarter the cash arrived. Notices of the managers on the custodian's portal "
                f"appear in the ledger twice from January to September 2026 (the custodian's advice and the notice as keyed); each credit is "
                f"counted once. The {names[insp]} distribution in listed shares and notice {wd}, which its manager withdrew and reissued, "
                f"brought no cash of their own. Detail by credit in {BOOK}.")
    doc.core_properties.author = W.PEOPLE["treasury"]
    doc.core_properties.title = "Standby facility 2027: election of the facility amount"
    doc.core_properties.subject = ""
    doc.core_properties.keywords = ""
    doc.core_properties.comments = ""
    doc.core_properties.last_modified_by = W.PEOPLE["treasury"]
    doc.save(os.path.join(GOLD, PAPER))


# ------------------------------------------------------------------ the workbook
def workbook(rows):
    names, strat = fund_names()
    D = F["distributions_2026_chf_k"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Distributions 2026"
    thin = Side(style="thin", color="999999")
    ws["A1"] = f"{W.ORG}, private-markets programme: distributions received on the programme account, 2026"
    ws["A1"].font = Font(bold=True, size=11)
    ws["A2"] = "CHF thousand, at the reference rate of the day the cash arrived; quarter of arrival"
    ws["A2"].font = Font(italic=True, size=9, color="444444")
    hdr = ["Strategy", "Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026", "Year 2026"]
    for i, h in enumerate(hdr, 1):
        c = ws.cell(row=4, column=i, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E8EDF3")
        c.border = Border(bottom=thin)
        c.alignment = Alignment(horizontal="left" if i == 1 else "right")
    r = 5
    for s in STRAT_ORDER:
        ws.cell(row=r, column=1, value=NAMES[s])
        for q in (1, 2, 3, 4):
            ws.cell(row=r, column=1 + q, value=D[f"{s}_Q{q}"]).number_format = "#,##0"
        ws.cell(row=r, column=6, value=D[f"{s}_year"]).number_format = "#,##0"
        r += 1
    ws.cell(row=r, column=1, value="Total").font = Font(bold=True)
    for q in (1, 2, 3, 4):
        c = ws.cell(row=r, column=1 + q, value=D[f"total_Q{q}"])
        c.number_format = "#,##0"
        c.font = Font(bold=True)
    c = ws.cell(row=r, column=6, value=F["distributions_2026_total_chf_k"])
    c.number_format = "#,##0"
    c.font = Font(bold=True)
    for col in range(1, 7):
        ws.cell(row=r, column=col).border = Border(top=thin)
    ws.cell(row=r + 2, column=1, value=f"Top strategy for the year: {F['top_strategy']}.").font = Font(size=9)
    ws.cell(row=r + 3, column=1, value="Totals are summed from unrounded amounts; they agree with the sums of the rounded cells.").font = Font(size=9, italic=True, color="444444")
    ws.column_dimensions["A"].width = 18
    for col in "BCDEF":
        ws.column_dimensions[col].width = 13
    ws.freeze_panes = "B5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    wc = wb.create_sheet("Credits")
    hdr = ["Value date", "Custodian reference", "Fund", "Strategy", "Notice", "Currency", "Amount in fund currency", "Reference rate",
           "CHF", "Quarter"]
    wc.append(hdr)
    for i in range(1, len(hdr) + 1):
        c = wc.cell(row=1, column=i)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E8EDF3")
        c.alignment = Alignment(horizontal="left" if i in (1, 2, 3, 4, 5, 6) else "right", wrap_text=True)
    code_of = {fid: r_["fund_code"] for fid, r_ in S.Pack().reg.iterrows()}
    for (vd, fid, nid, tref, amt, ccy, chf, n) in sorted(rows, key=lambda x: (x[0], x[3])):
        code = code_of[fid]
        rate = chf / amt if amt else 1.0
        wc.append([vd, tref, names[code], strat[code], nid, ccy, round(amt, 2), round(rate, 4), round(chf, 2), f"Q{S.quarter(vd)}"])
    for row in wc.iter_rows(min_row=2):
        row[0].number_format = "yyyy-mm-dd"
        row[6].number_format = "#,##0.00"
        row[7].number_format = "0.0000"
        row[8].number_format = "#,##0.00"
        for c in row[6:9]:
            c.alignment = Alignment(horizontal="right")
    for col, w in zip("ABCDEFGHIJ", [11, 14, 30, 14, 18, 9, 16, 10, 15, 8]):
        wc.column_dimensions[col].width = w
    wc.freeze_panes = "A2"
    wc.auto_filter.ref = f"A1:J{wc.max_row}"

    wn = wb.create_sheet("Notes")
    notes = [
        "Distributions received on the programme account in 2026",
        "",
        "Source: custodian statement of the programme account (programmkonto_lindenhof_2025-2026.csv), postings 'Gutschrift Ausschuettung' with a value date in 2026; notice ledger (kapitalabrufe_ausschuettungen_2015-2026.csv) for the notice behind each credit; fund register for the strategy; custodian 16:00 reference rates.",
        "Amount: the cash lines of the notice the credit settles, in the fund currency, at the reference rate of the credit's value date (the day the cash arrived). The custodian's own franc amounts are at its dealing rate and are not used.",
        "Quarter: the quarter of the credit's value date. Several cross-border credits arrived a few business days after the payment date the notice states; they are counted when the cash arrived.",
        "From January to September 2026 the notices of the managers on the custodian's portal are in the ledger twice: the custodian's advice (custodian reference as notice number) and the notice keyed by Rechnungswesen. Each credit is counted once.",
        "Not cash: the distribution in listed shares of the third quarter and the notice its manager withdrew and reissued in the second quarter; the reissued notice is counted when its cash arrived.",
        "Prepared by Treasury & Liquidität, 8 January 2027, from the year-end extract PKW-PM-2026-12-31.",
    ]
    for i, t in enumerate(notes, 1):
        c = wn.cell(row=i, column=1, value=t)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if i == 1:
            c.font = Font(bold=True)
    wn.column_dimensions["A"].width = 120
    wb.properties.creator = W.PEOPLE["treasury"]
    wb.properties.title = "Distributions received 2026"
    wb.save(os.path.join(GOLD, BOOK))


def main():
    if os.path.isdir(GOLD):
        shutil.rmtree(GOLD)
    os.makedirs(GOLD)
    pk = S.Pack()
    g, rows = S.ask_golden(pk, detail=True)
    G = S.grid_figures(g)
    D = F["distributions_2026_chf_k"]
    for key in D:
        assert round(G[key]) == D[key], (key, G[key], D[key])
    assert abs(sum(r[6] for r in rows if r[0].year == 2026) / 1000.0 - sum(G[f"total_Q{q}"] for q in (1, 2, 3, 4))) < 1e-6
    tmp = os.path.join(HERE, "_chart")
    os.makedirs(tmp, exist_ok=True)
    cp = os.path.join(tmp, CHART)
    chart(cp)
    paper(cp)
    workbook([r for r in rows if r[0].year == 2026])
    shutil.rmtree(tmp)
    subprocess.run([sys.executable, SCRUB, GOLD, "--apply", "--producer", W.ORG, "--stamp", "2027-01-08", "--floor", "2026-12-01",
                    "--ceiling", "2027-01-08"], check=True, capture_output=True)
    core = {PAPER: ("2027-01-07T14:02:00Z", "2027-01-08T15:12:00Z"), BOOK: ("2027-01-07T10:40:00Z", "2027-01-08T15:05:00Z")}
    for f in (PAPER, BOOK):
        PK.fix_zip_times(os.path.join(GOLD, f), STAMP, core=core[f])
    stamp = time.mktime(STAMP + (0, 0, -1))
    for f in os.listdir(GOLD):
        os.utime(os.path.join(GOLD, f), (stamp, stamp))
    print("goldens:", sorted(os.listdir(GOLD)))


if __name__ == "__main__":
    main()
