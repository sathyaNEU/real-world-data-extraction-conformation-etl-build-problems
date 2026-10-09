#!/usr/bin/env python3
"""Steady Ground Fund, September 2026 round: the in-house screen, the replay and the offers.

    python3 golden.py [target_dir] [out_dir]

Reads the round folder (target_dir) and writes the trustees' paper, the conformed screen and the
offers chart to out_dir:
    steady_ground_sep2026_offers.docx
    steady_ground_sep2026_screen.csv
    steady_ground_sep2026_offers.png
Prints the figures the paper rests on.
"""
import csv
import io
import os
import re
import sys
import zipfile
from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import openpyxl
from pypdf import PdfReader

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "target"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE.parent / "golden"

CENSUS = date(2026, 9, 30)
PAPER_DATE = datetime(2026, 10, 28, 9, 0, 0)
BALANCE = {"31 March": 3, "30 June": 6, "31 December": 12}
DOCX = "steady_ground_sep2026_offers.docx"
CSV_OUT = "steady_ground_sep2026_screen.csv"
PNG = "steady_ground_sep2026_offers.png"


# --------------------------------------------------------------------------- quarters
# A quarter is (year, month of its last day). fy_q is its position in the organisation's financial year.

def q_shift(q, k):
    t = q[0] * 12 + q[1] - 1 + 3 * k
    return (t // 12, t % 12 + 1)


def q_of(d):
    return (d.year, (d.month - 1) // 3 * 3 + 3)


def fy_q(q, bal):
    return (q[1] - bal - 1) % 12 // 3 + 1


def iso(s):
    return date(int(s[:4]), int(s[5:7]), int(s[8:10]))


def pct1(fall, prior):
    return (Decimal(fall) * 100 / Decimal(prior)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def money(x):
    return f"-${-x:,}" if x < 0 else f"${x:,}"


# --------------------------------------------------------------------------- the round folder
def pdf_text(name):
    return "\n".join(p.extract_text() for p in PdfReader(TARGET / name).pages)


rules = pdf_text("SGF_round_rules_rev2026-06.pdf")
LINE = int(re.search(r"fall is (\d+) per cent or more", rules).group(1))
FLOOR = int(re.search(r"raised to \$([\d,]+)", rules).group(1).replace(",", ""))
CAP = int(re.search(r"held to \$([\d,]+)", rules).group(1).replace(",", ""))
minute = pdf_text("trustees_budget_minute_2026-27_extract.pdf")
POT = int(re.search(r"September 2026 round\s*\$([\d,]+)", minute).group(1).replace(",", ""))

wb = openpyxl.load_workbook(TARGET / "grants_register_20261007.xlsx", read_only=True)
grants = [dict(zip(r[0], x)) for r in [list(wb["Grants"].iter_rows(values_only=True))] for x in r[1:]]
ORG_OF = {g["grant_ref"]: g["charity_no"] for g in grants}
NAME = {g["charity_no"]: g["organisation"] for g in grants}
BAL = {g["charity_no"]: BALANCE[g["balance_date"]] for g in grants}
OPERATING = {g["charity_no"]: (g["start_date"].date(), g["end_date"].date())
             for g in grants if g["programme"] == "Operating grant"}
assert len(OPERATING) == len(NAME), "every organisation holds one operating grant"

# Portal: accepted versions only (field guide), pooled across an organisation's grant references.
accepted = defaultdict(list)          # (charity_no, quarter) -> [(accepted_at, lines)]
versions = {}
with open(TARGET / "portal_return_lines_2018q3_2026q2.csv", newline="") as fh:
    for r in csv.DictReader(fh):
        key = (r["return_id"], r["version_no"])
        v = versions.get(key)
        if v is None:
            pe = iso(r["period_end"])
            v = versions[key] = dict(cc=ORG_OF[r["grant_ref"]], q=(pe.year, pe.month), status=r["version_status"],
                                     acc=r["accepted_at"], form=r["form"], ytd={}, py={})
        (v["ytd"] if r["column"] == "YTD" else v["py"])[r["line_code"]] = int(r["amount"])
for v in versions.values():
    if v["status"] == "accepted":
        accepted[(v["cc"], v["q"])].append(v)
for lst in accepted.values():
    lst.sort(key=lambda v: v["acc"])

register = {}
with open(TARGET / "charities_register_returns_extract_20261007.csv", newline="") as fh:
    for r in csv.DictReader(fh):
        cc = r["charity_no"].strip().upper()
        ye = iso(r["year_end"])
        assert (cc, (ye.year, ye.month)) not in register, "one annual return per organisation and year"
        register[(cc, (ye.year, ye.month))] = dict(received=iso(r["date_received"]),
                                                   total=int(r["total_gross_income"]),
                                                   govt=int(r["govt_grants_contracts"]))
assert all(cc in NAME for cc, _ in register), "every register row joins after trimming and upper-casing"

run_paid = defaultdict(int)           # (charity_no, quarter the money reached the account) -> dollars
with open(TARGET / "trust_payment_run_2018-07_to_2026-09.csv", newline="") as fh:
    for r in csv.DictReader(fh):
        if r["payment_status"] == "paid":          # a returned line is reissued under its own row
            run_paid[(r["charity_no"], q_of(iso(r["value_date"])))] += int(r["amount"])


def rule7_pay_day(y, m):
    """Rule 7: paid on the 20th of the month before the month the instalment is for, or the Friday before."""
    y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    d = date(y, m, 20)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


# Steady Ground instalments are not in the payment run; they are rebuilt from the offers sheet.
sgf_paid = defaultdict(int)
offer_rows = list(wb["Steady Ground offers"].iter_rows(values_only=True))
for x in (dict(zip(offer_rows[0], r)) for r in offer_rows[1:]):
    y0, m0 = int(x["first_instalment_for"][:4]), int(x["first_instalment_for"][5:7])
    n, each = int(x["instalments"]), int(x["instalment"])
    for k in range(n):
        t = y0 * 12 + m0 - 1 + k
        amt = each if k < n - 1 else int(x["offer_amount"]) - (n - 1) * each
        sgf_paid[(x["charity_no"], q_of(rule7_pay_day(t // 12, t % 12 + 1)))] += amt
trust_paid = defaultdict(int)
for d_ in (run_paid, sgf_paid):
    for k, v in d_.items():
        trust_paid[k] += v

packs = {}
for y in range(2021, 2027):
    pw = openpyxl.load_workbook(TARGET / f"SGF_screen_run_{y}-03.xlsx", read_only=True)
    rows = list(pw["Screen"].iter_rows(values_only=True))
    h = next(i for i, r in enumerate(rows) if r and r[0] == "Charity no.")
    rnd = {r[0]: r[1] for r in pw["Round"].iter_rows(values_only=True)}
    packs[y] = dict(rows={r[0]: (r[2], r[3], r[4], Decimal(str(r[5])), r[6] or 0) for r in rows[h + 1:] if r and r[0]},
                    pot=int(rnd["Pot ($)"]), rate=Decimal(str(rnd["Rate (cents per dollar of fall)"])))


# --------------------------------------------------------------------------- the screen
def held(cc, q, census):
    """The organisation's return for quarter q as the Trust held it at the end of the census day."""
    cut = census.isoformat() + " 23:59"
    lst = [v for v in accepted.get((cc, q), []) if v["acc"] <= cut]
    return lst[-1] if lst else None


def received(cc, q, census):
    r = register.get((cc, q))
    return r is not None and r["received"] <= census


def total_line(v):
    return v["ytd"].get("TOT_INC", v["ytd"].get("TOT_REV"))


def quarter_amount(cc, q, census, ytd_of, year_total):
    """Discrete quarter from year-to-date figures. The final quarter of a financial year exists only as
    the filed annual return less the nine-month year to date, and only once the return is received."""
    bal = BAL[cc]
    k = fy_q(q, bal)
    if k == 4:
        if not received(cc, q, census):
            return None
        before = ytd_of(cc, q_shift(q, -1), census)
        return None if before is None else year_total(cc, q) - before
    now = ytd_of(cc, q, census)
    if now is None:
        return None
    if k == 1:
        return now
    before = ytd_of(cc, q_shift(q, -1), census)
    return None if before is None else now - before


def ytd_total(cc, q, census):
    v = held(cc, q, census)
    return None if v is None else total_line(v)


def ytd_govt(cc, q, census):
    v = held(cc, q, census)
    if v is None or "GOV_GRT" not in v["ytd"]:
        return None                                      # short form: not reported
    y = v["ytd"]
    if v["form"] == "QFR-24":                            # GOV_GRT: grants and contracts
        return y["GOV_GRT"]
    return y["GOV_GRT"] + y["FEE_SVC_GOV"]               # QFR-16: grants only; contracts sat in fees, on the memo


def admissible(cc, q, census):
    return fy_q(q, BAL[cc]) != 4 or received(cc, q, census)


def census_before(census):
    """Rule 2: 31 March each year and, from 2026, 30 September."""
    days = [date(y, 3, 31) for y in range(2015, census.year + 1)]
    days += [date(y, 9, 30) for y in range(2026, census.year + 1)]
    return max(d for d in days if d < census)


def quarter_end(q):
    return date(q[0] + (q[1] == 12), q[1] % 12 + 1, 1) - timedelta(days=1)


def windows(cc, census):
    """Latest eight consecutive admissible quarters before the census quarter: (current four, prior four).
    Rule 4.1: the twelve months must end on or after the census before this one."""
    end = q_shift(q_of(census), -1)
    while quarter_end(end) >= census_before(census):
        if all(admissible(cc, q_shift(end, -k), census) for k in range(8)):
            return [q_shift(end, -k) for k in range(4)], [q_shift(end, -k) for k in range(4, 8)], end
        end = q_shift(end, -1)
    return None


def offer_at(rate_hc, fall):
    raw = (Decimal(rate_hc) * fall / 10000).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return min(max(int(raw), FLOOR), CAP)


def strike(falls, pot):
    lo, hi = 0, 10000                                    # hundredths of a cent
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if sum(offer_at(mid, f) for f in falls) <= pot:
            lo = mid
        else:
            hi = mid
    return lo


def screen(census, pot):
    rows = []
    for cc, (start, end) in OPERATING.items():
        if not start <= census <= end:
            continue
        w = windows(cc, census)
        if w is None:
            continue
        cur, pri, wend = w
        a =[quarter_amount(cc, q, census, ytd_total, lambda c, q: register[(c, q)]["total"]) for q in cur + pri]
        if any(x is None for x in a):
            continue                                     # returns do not cover both periods (rule 3.2)
        income, before = sum(a[:4]), sum(a[4:])
        rows.append(dict(cc=cc, cur=cur, pri=pri, end=wend, income=income, before=before,
                         fall=before - income, pct=pct1(before - income, before),
                         eligible=100 * (before - income) >= LINE * before))
    elig = [r for r in rows if r["eligible"]]
    rate = strike([r["fall"] for r in elig], pot)
    for r in rows:
        r["offer"] = offer_at(rate, r["fall"]) if r["eligible"] else 0
    in_scope = sum(1 for s, e in OPERATING.values() if s <= census <= e)
    return dict(rows=rows, rate=rate, total=sum(r["offer"] for r in rows), in_scope=in_scope)


# --------------------------------------------------------------------------- the replay (cutover standard 4)
replay = {}
for y, pk in packs.items():
    s = screen(date(y, 3, 31), pk["pot"])
    mine = {r["cc"]: (r["income"], r["before"], r["fall"], r["pct"], r["offer"]) for r in s["rows"]}
    back = sum(1 for cc, v in pk["rows"].items() if mine.get(cc) == v)
    replay[y] = dict(published=len(pk["rows"]), back=back,
                     offers=sum(1 for v in pk["rows"].values() if v[4]),
                     offers_back=sum(1 for cc, v in pk["rows"].items() if v[4] and mine.get(cc, (0,) * 5)[4] == v[4]),
                     rate_back=Decimal(s["rate"]) / 100 == pk["rate"], extra=len(mine) - len(pk["rows"]))
    assert back == len(pk["rows"]) and replay[y]["extra"] == 0 and replay[y]["rate_back"], f"replay {y} fails"
    assert replay[y]["offers_back"] == replay[y]["offers"], f"replay {y} offers"

# --------------------------------------------------------------------------- September 2026
S = screen(CENSUS, POT)
rows = sorted(S["rows"], key=lambda r: -r["fall"])
offered = [r for r in rows if r["offer"]]
outside = max((r for r in rows if not r["eligible"]), key=lambda r: (r["fall"] / r["before"]))
stepped = [r for r in rows if r["end"] != q_shift(q_of(CENSUS), -1)]
# The rule the paper states, checked row by row: a stepped-back window ends at the quarter before the year-end
# whose return was not on the register, December 2025 for 31 March and March 2026 for 30 June.
assert all(r["end"] == {3: (2025, 12), 6: (2026, 3)}[BAL[r["cc"]]] for r in stepped)
assert all(not received(r["cc"], {3: (2026, 3), 6: (2026, 6)}[BAL[r["cc"]]], CENSUS) for r in stepped)
unscored = S["in_scope"] - len(rows)
scored_cc = {r["cc"] for r in rows}
not_scored = [cc for cc, (s, e) in OPERATING.items() if s <= CENSUS <= e and cc not in scored_cc]
# Rule 4.1: a 31 March organisation without its 2025-26 return on the register would be scored on twelve months
# to December 2025, which end before the census before (31 March 2026), so it is not scored this round.
late31 = sorted(cc for cc in not_scored if BAL[cc] == 3 and not received(cc, (2026, 3), CENSUS))
newer = [cc for cc in not_scored if cc not in late31]
assert all(OPERATING[cc][0] >= date(2024, 7, 1) for cc in newer), "the rest are grantees from mid-2024 or later"
assert census_before(CENSUS) == date(2026, 3, 31) and not any(BAL[r["cc"]] == 3 for r in stepped)
for cc in late31:                                        # ... on the same twelve months as in March 2026
    qs = [q_shift((2025, 12), -k) for k in range(8)]
    a = [quarter_amount(cc, q, CENSUS, ytd_total, lambda c, q: register[(c, q)]["total"]) for q in qs]
    assert None not in a and (sum(a[:4]), sum(a[4:])) == packs[2026]["rows"][cc][:2], cc
assert S["total"] <= POT < sum(offer_at(S["rate"] + 1, r["fall"]) for r in offered)
assert len({r["fall"] for r in rows}) == len(rows), "no two falls equal, so the sort is stable"

# The parts of each fall: government grants and contracts, and the Trust's own money, over the same windows.
for r in rows:
    cc = r["cc"]
    g = [quarter_amount(cc, q, CENSUS, ytd_govt, lambda c, q: register[(c, q)]["govt"]) for q in r["cur"] + r["pri"]]
    r["govt"] = None if any(x is None for x in g) else sum(g[4:]) - sum(g[:4])
    r["trust"] = sum(trust_paid[(cc, q)] for q in r["pri"]) - sum(trust_paid[(cc, q)] for q in r["cur"])

# Control: on every QFR-24 return held at the census, the Trust memo agrees with the payment run.
memo_checked = 0
for (cc, q), lst in accepted.items():
    v = held(cc, q, CENSUS)
    if v is None or "GRT_NGO_APT" not in v["ytd"]:
        continue
    k = fy_q(q, BAL[cc])
    assert v["ytd"]["GRT_NGO_APT"] == sum(run_paid[(cc, q_shift(q, -j))] for j in range(k)), (cc, q)
    memo_checked += 1
assert memo_checked > 800
assert all(r["govt"] is not None for r in offered), "every offered grantee files the full form"

# --------------------------------------------------------------------------- outputs
OUT.mkdir(parents=True, exist_ok=True)
for stale in (DOCX, CSV_OUT, PNG):
    if (OUT / stale).exists():
        (OUT / stale).unlink()

with open(OUT / CSV_OUT, "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["charity_no", "organisation", "twelve_month_income", "twelve_months_before", "fall",
                "fall_pct", "offer", "fall_govt_grants_contracts", "fall_trust_money"])
    for r in rows:
        w.writerow([r["cc"], NAME[r["cc"]], r["income"], r["before"], r["fall"], f"{r['pct']:.1f}", r["offer"],
                    "" if r["govt"] is None else r["govt"], r["trust"]])

rate_txt = f"{Decimal(S['rate']) / 100:.2f}"
COUNT_WORD = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
              8: "eight", 9: "nine"}
in_words = lambda n: COUNT_WORD[n] if 0 < n < 10 else str(n)    # the Trust's house style in prose
n_cap = sum(1 for r in offered if r["offer"] == CAP)
n_floor = sum(1 for r in offered if r["offer"] == FLOOR)
assert n_cap in COUNT_WORD and n_floor in COUNT_WORD and n_cap >= 1

# Chart: one series, bars in order of offer, floor and cap as labelled reference lines.
INK, INK2, GRID, SURFACE, BAR = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb", "#2a78d6"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "sgf"})
fig, ax = plt.subplots(figsize=(8.6, 6.0), dpi=150)
fig.patch.set_facecolor(SURFACE)
ax.set_facecolor(SURFACE)
names = [NAME[r["cc"]] for r in offered]
vals = [r["offer"] for r in offered]
ypos = list(range(len(offered)))[::-1]
ax.barh(ypos, vals, height=0.55, color=BAR, zorder=2)
for y_, v in zip(ypos, vals):
    ax.text(v + 1800, y_, f"${v:,}", va="center", ha="left", color=INK, fontsize=8.5, zorder=3)
for x, label in ((FLOOR, f"Floor ${FLOOR:,}"), (CAP, f"Cap ${CAP:,}")):
    ax.axvline(x, color=INK2, lw=1.1, ls=(0, (4, 3)), zorder=3)
    ax.text(x + 1500, len(offered) - 0.3, label, ha="left", va="bottom", color=INK2, fontsize=8.5)
ax.set_yticks(ypos)
ax.set_yticklabels(names, color=INK)
ax.set_xlim(0, 182000)
ax.set_ylim(-0.7, len(offered) + 0.2)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x / 1000:,.0f}k" if x else "$0"))
ax.set_xlabel("Offer (NZ$, paid in twelve monthly instalments from December 2026)", color=INK2)
ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", colors=INK2)
fig.text(0.015, 0.965, f"September 2026 offers at {rate_txt} cents per dollar of fall", ha="left", va="top",
         fontsize=12.5, fontweight="bold", color=INK)
fig.text(0.015, 0.925, f"{len(offered)} grantees, {money(S['total'])} of the {money(POT)} pot".replace("$", r"\$"),
         ha="left", va="top", fontsize=9.5, color=INK2)
fig.text(0.02, 0.012, "Source: in-house screen at the 30 September 2026 census, round rules as amended 16 June 2026.",
         fontsize=7.5, color=INK2)
fig.tight_layout(rect=(0, 0.03, 1, 0.9))
fig.savefig(OUT / PNG, facecolor=SURFACE, metadata={"Software": None})
plt.close(fig)


# Trustees' paper.
def shade(cell, hex_):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hex_)
    tcPr.append(sh)


def para(doc, text="", bold=False, size=None, after=6, italic=False, align=None, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    if align:
        p.alignment = align
    if bold and size and size >= 11:
        p.paragraph_format.keep_with_next = True
    if text:
        run = p.add_run(text)
        run.bold, run.italic = bold, italic
        if size:
            run.font.size = Pt(size)
        if color:
            run.font.color.rgb = RGBColor.from_string(color)
    return p


def note_ref(p, n):
    run = p.add_run(str(n))
    run.font.superscript = True


def table(doc, header, body, widths, right_from=1, total=None):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]
        c.text = ""
        run = c.paragraphs[0].add_run(h)
        run.bold = True
        run.font.size = Pt(9)
        shade(c, "E8EEF5")
        if i >= right_from:
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for line in body + ([total] if total else []):
        cells = t.add_row().cells
        for i, x in enumerate(line):
            cells[i].text = ""
            run = cells[i].paragraphs[0].add_run(x)
            run.font.size = Pt(9)
            if total and line is total:
                run.bold = True
            if i >= right_from:
                cells[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    t.autofit = False
    for i, wdt in enumerate(widths):
        t.columns[i].width = Cm(wdt)
    for row in t.rows:
        for i, wdt in enumerate(widths):
            row.cells[i].width = Cm(wdt)
    return t


def page_number_footer(section, left):
    p = section.footer.paragraphs[0]
    p.text = ""
    r = p.add_run(left + "\tPage ")
    r.font.size = Pt(8)
    for kind, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        run = p.add_run()
        run.font.size = Pt(8)
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = txt
        run._r.append(el)


doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(10.5)
sec = doc.sections[0]
sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(1.8)
hp = sec.header.paragraphs[0]
hr = hp.add_run("Ashworth Pascoe Trust  |  Trustees' meeting, 11 November 2026  |  Steady Ground Fund")
hr.font.size = Pt(8)
hr.font.color.rgb = RGBColor(0x52, 0x51, 0x4E)
page_number_footer(sec, "Paper for decision. Draft for the chair, 28 October 2026.")

para(doc, "Ashworth Pascoe Trust", bold=True, size=9, after=0, color="52514E")
para(doc, f"Steady Ground Fund, September 2026 round: offers at {rate_txt} cents per dollar of fall",
     bold=True, size=15, after=8)
for k, v in (("To", "Wiremu Roberts (chair) and trustees"),
             ("From", "Marie Griffin, head of grants"),
             ("Date", "28 October 2026, for the meeting of 11 November 2026"),
             ("Decision", "Approve the round's rate and its offers (round rules, rule 8)")):
    p = para(doc, after=1)
    p.paragraph_format.tab_stops.add_tab_stop(Cm(2.6))
    p.add_run(k).bold = True
    p.add_run("\t" + v)
para(doc, after=2)

para(doc, "Recommendation", bold=True, size=11.5, after=4)
p = para(doc, f"That the trustees set the rate for the September 2026 round at {rate_txt} cents per dollar of "
              f"fall and approve the {in_words(len(offered))} offers below, together {money(S['total'])} against the "
              f"{money(POT)} pot in the 2026-27 budget, with {money(POT - S['total'])} left in the Fund. "
              "Each offer is paid in twelve monthly instalments, the first for December 2026.")

para(doc, "The rate", bold=True, size=11.5, after=4)
para(doc, f"This is the first round the Trust has screened itself. Of the {S['in_scope']} organisations holding an "
          f"operating grant at the 30 September census, the screen scored {len(rows)}. Of these, {in_words(len(offered))} had a "
          f"fall in twelve-month income of {LINE} per cent or more of the twelve months before, and the rate is the "
          "highest, to the hundredth of a cent, at which their offers fit inside the pot (rule 5.3). "
          f"{COUNT_WORD[n_cap].capitalize()} offer{'s' if n_cap > 1 else ''} {'is' if n_cap == 1 else 'are'} held at "
          + ("the cap; none needed raising to the floor." if n_floor == 0 else
             f"the cap and {COUNT_WORD[n_floor]} {'is' if n_floor == 1 else 'are'} raised to the floor."))
p = para(doc, "A September census falls on the filing deadline for organisations with a 31 March balance date, "
              "and three months before the deadline for those balancing at 30 June, so a good number had no "
              "2025-26 annual return on the register at the census. The screen takes a year's last quarter only "
              "from the filed annual return (its total gross income less the nine-month year to date), so for "
              "those organisations the twelve months end at the quarter before that year-end, with the twelve "
              f"months before stepping back with them. For the {len(stepped)} balancing at 30 June that is March "
              "2026, and they are scored on it. For the "
              f"{len(late31)} balancing at 31 March it is December 2025, which ends before 31 March 2026, the census "
              "before this one, so under rule 4.1 they cannot be scored this round; each was scored on those same "
              "twelve months in the March 2026 round. This is the method that gives back Ledgerwood's six March "
              "packs, below. Rule 4.1 never bound in a March round, where the census before was a year earlier.")
note_ref(p, 1)

para(doc, "Offers", bold=True, size=11.5, after=4)
p = para(doc, "Each offer, with the part of the fall it is struck on that was government grants and contracts "
              "and the part that was money from the Trust itself (operating and project grants, and Steady "
              "Ground instalments from earlier rounds). A negative part means that income rose over the year "
              "while total income fell.", after=4)
note_ref(p, 2)
body = [[NAME[r["cc"]], money(r["offer"]) + (" (cap)" if r["offer"] == CAP else " (floor)" if r["offer"] == FLOOR else ""),
         money(r["govt"]), money(r["trust"])] for r in offered]
table(doc, ["Organisation", "Offer", "Government part of fall", "Trust part of fall"], body,
      [7.4, 3.2, 3.3, 2.7], total=["Total", money(S["total"]), "", ""])
para(doc, "Source: in-house screen at 30 September 2026 (steady_ground_sep2026_screen.csv); portal returns, "
          "register match, grants register and payment run as at 7 October 2026.", italic=True, size=8, after=8,
     color="52514E")

para(doc, "Just outside the line", bold=True, size=11.5, after=4)
para(doc, f"The first organisation outside the line is {NAME[outside['cc']]}, with a fall of {outside['pct']:.1f} "
          "per cent. No scored organisation sits close enough to the line for a rounding question to arise.")

para(doc, "The replay", bold=True, size=11.5, after=4)
para(doc, "The cutover standard lets the in-house screen be used only once it gives back every grantee row, every "
          "offer and each round's rate in Ledgerwood's six published March runs (clause 4). Re-run at each March "
          "census with that round's pot, it does:", after=4)
rbody = [[f"March {y}", str(v["published"]), str(v["back"]), f"{v['offers_back']} of {v['offers']}",
          f"{packs[y]['rate']:.2f}"] for y, v in replay.items()]
table(doc, ["Round", "Rows published", "Rows given back exactly", "Offers given back", "Rate (cents)"], rbody,
      [3.0, 3.0, 3.8, 3.4, 2.6])
para(doc, "Rows are compared on twelve-month income, the twelve months before, the fall in dollars and per cent, "
          "and the offer. The replay record is filed with the round papers (clause 5).",
     italic=True, size=8, after=8, color="52514E")

para(doc, "Purpose of the round", bold=True, size=11.5, after=4)
para(doc, "It has been put to me that the round is for the groups hit by the March government funding cut. The "
          "rules score every organisation on its own fall, whatever the cause (rules 1 and 4), and the "
          "government part of each fall is shown above so trustees can see where public money is behind it.")

para(doc, "Notes", bold=True, size=9.5, after=2)
for n, txt in ((1, "Annual returns are read from the register match as received by the end of the census day. "
                   f"Of the {unscored} organisations in scope and not scored, {len(late31)} are the 31 March "
                   f"organisations above and {COUNT_WORD[len(newer)]} are newer grantees whose returns do not yet "
                   "cover both twelve-month periods (rule 3.2)."),
               (2, "Government grants and contracts: on QFR-24 returns the 'Government grants and contracts' line; "
                   "on QFR-16 returns (to September 2024) 'Government grants' plus the memo 'of which government "
                   "service contracts', as the line kept its code when contracts moved onto it. Trust money is "
                   "counted in the quarter it reached the organisation's account: operating and project grant "
                   "payments from the payment run (paid lines, so a returned payment counts once, through its "
                   "reissue), and Steady Ground instalments, which are not in the payment run, from the offers "
                   "sheet on the pay day rule 7 sets. Whole dollars throughout; fall percentages to one decimal.")):
    p = para(doc, after=2, size=8)
    r1 = p.add_run(f"{n}  ")
    r1.font.size = Pt(8)
    r2 = p.add_run(txt)
    r2.font.size = Pt(8)

cp = doc.core_properties
cp.author = cp.last_modified_by = "Marie Griffin"
cp.title = "Steady Ground Fund, September 2026 round"
cp.comments = cp.subject = cp.keywords = cp.category = ""
cp.created = cp.modified = PAPER_DATE
cp.last_printed = PAPER_DATE
cp.revision = 3
buf = io.BytesIO()
doc.save(buf)
# Repack at a fixed entry time so the paper rebuilds byte for byte; the entries themselves are untouched.
src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
with zipfile.ZipFile(OUT / DOCX, "w", zipfile.ZIP_DEFLATED) as z:
    for info in src.infolist():
        data = src.read(info.filename)
        zi = zipfile.ZipInfo(info.filename, date_time=PAPER_DATE.timetuple()[:6])
        zi.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(zi, data)
fixed = PAPER_DATE.timestamp()
for f in (DOCX, CSV_OUT, PNG):
    os.utime(OUT / f, (fixed, fixed))

# --------------------------------------------------------------------------- what the paper rests on
print(f"Rate: {rate_txt} cents per dollar of fall ({len(offered)} offers, {money(S['total'])} of {money(POT)}, "
      f"{money(POT - S['total'])} left in the Fund)")
print(f"In scope {S['in_scope']}, scored {len(rows)}; twelve months to March 2026 for {len(stepped)} at 30 June; "
      f"{len(late31)} at 31 March not scored under rule 4.1; {len(newer)} newer grantees not scored")
print("Replay: " + "; ".join(f"{y} {v['back']} of {v['published']} rows, {v['offers_back']} of {v['offers']} offers, "
                             f"rate {'given back' if v['rate_back'] else 'MISSED'}" for y, v in replay.items()))
print(f"Replay totals: {sum(v['back'] for v in replay.values())} of {sum(v['published'] for v in replay.values())} "
      f"rows, {sum(v['offers_back'] for v in replay.values())} offers, {sum(v['rate_back'] for v in replay.values())} rates")
print(f"First outside the line: {NAME[outside['cc']]} at {outside['pct']:.1f} per cent")
print(f"Trust memo agrees with the payment run on {memo_checked} QFR-24 returns held at the census; "
      f"Steady Ground instalments rebuilt: {sum(sgf_paid.values()):,} dollars")
for r in offered:
    print(f"  {NAME[r['cc']]:<42} offer {money(r['offer']):>9}  govt {money(r['govt']):>9}  trust {money(r['trust']):>8}")
