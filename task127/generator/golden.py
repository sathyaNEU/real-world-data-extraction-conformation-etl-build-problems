"""Golden deliverables for task127:  python3 task127/generator/golden.py

Reads only task127/target/. Builds each co-op's 2027 expected rebated installs from the Heat Survey's
qualifying households and the pilot's install rate for each heating system, caps each feeder at the heat pumps
its filed hosting capacity takes, works the year's meter orders through each co-op crew's spare meter sets, and
splits the 1,800 slots under section 5 of the programme rules. Then audits the 2026 pilot's installed cost and
the rebates paid through 30 November by co-op. Writes the three files the prompt names into task127/golden/:
  slot_split_board_note_2027.docx  (the trustees' note)
  coop_slot_split_2027.csv         (finance's load file)
  coop_slots_2027.svg              (the screen chart, rendered here)
Prints the critical components' figures at the end."""
import csv
import io
import json
import math
import re
import sys
from fractions import Fraction
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import openpyxl
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
TASK = HERE.parent
T = TASK / "target"
OUT = TASK / "golden"

COOPS = ["North Shore", "Valley", "Lakes", "Uplands", "Riverbend", "Pinewood"]   # the rules' own order
SYSTEMS = {"PF": "propane furnace (ducted)", "ER": "electric resistance", "PB": "propane boiler (hydronic)"}
CT = ZoneInfo("America/Chicago")
YEAR = 2027
HEAD_LINE = "multi-zone heat pump system, indoor head"


def rows_csv(name):
    with open(T / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def rows_xlsx(name, sheet, header_row=1):
    ws = openpyxl.load_workbook(T / name, read_only=True, data_only=True)[sheet]
    it = ws.iter_rows(values_only=True)
    for _ in range(header_row - 1):
        next(it)
    hdr = [str(h) for h in next(it)]
    return [dict(zip(hdr, r)) for r in it if r and any(v is not None for v in r)]


def pdf_text(name):
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(str(T / name)).pages))


def day(v):
    return v.date() if isinstance(v, datetime) else date.fromisoformat(str(v)[:10])


def tens(v):
    return int(math.floor(v / 10 + 0.5)) * 10


# ------------------------------------------------------------------ the filed rules

RULES = pdf_text("heat_pump_programme_rules_2027.pdf")
TERMS = pdf_text("cooperative_participation_terms.pdf")
TOTAL_SLOTS = int(re.search(r"The fund has ([\d,]+) rebate slots", RULES).group(1).replace(",", ""))
KW_PER_HP = int(re.search(r"assessed at (\d+) kW", TERMS).group(1))
INCOME = re.search(r"from \$([\d,]+) to \$([\d,]+)\. Homes", RULES).groups()
LOW_BAND = re.search(r"Income \$([\d,]+) to \$([\d,]+)", TERMS).groups()
SCHED = {lbl: int(re.search(re.escape(lbl) + r" \$([\d,]+)", TERMS, re.I).group(1).replace(",", ""))
         for lbl in ("Propane furnace (ducted)", "Electric resistance", "Propane boiler (hydronic)")}
SCHED = {k.lower(): v for k, v in SCHED.items()}
TOP_UP = int(re.search(r"plus \$([\d,]+)", TERMS).group(1).replace(",", ""))
assert TOTAL_SLOTS == 1800 and KW_PER_HP == 5


def in_band(label):
    if " to " not in label:          # "under 35,000", "150,000 and over"
        return False
    lo, hi = (int(x) for x in label.replace(",", "").split(" to "))
    return int(INCOME[0].replace(",", "")) <= lo and hi <= int(INCOME[1].replace(",", ""))


# ------------------------------------------------------------------ 1. expected installs (survey x pilot rates)

SURVEY = rows_csv("heat_survey_2025_households.csv")
PILOT = rows_xlsx("pilot_rebates_2026.xlsx", "rebates")
assert len(PILOT) == len({str(r["premises_id"]) for r in PILOT}), "one pilot install per premises"
PILOT_NB = {r["neighbourhood"] for r in PILOT}
QUAL = [r for r in SURVEY if r["tenure"] == "owner" and r["structure"] == "single-family detached"
        and in_band(r["income_band"]) and r["heating_system"] in SYSTEMS]

den = defaultdict(int)
for r in QUAL:
    if r["neighbourhood"] in PILOT_NB:
        den[SYSTEMS[r["heating_system"]]] += int(r["weight"])
num = defaultdict(int)
for r in PILOT:
    num[r["heating_system_replaced"]] += 1
RATE = {s: num[s] / den[s] for s in SYSTEMS.values()}
RATE_FR = {s: Fraction(num[s], den[s]) for s in SYSTEMS.values()}

# back-test: the system rates against each pilot neighbourhood's own installs
bt = defaultdict(float)
for r in QUAL:
    if r["neighbourhood"] in PILOT_NB:
        bt[r["neighbourhood"]] += int(r["weight"]) * RATE[SYSTEMS[r["heating_system"]]]
for nb in PILOT_NB:
    act = sum(1 for p in PILOT if p["neighbourhood"] == nb)
    assert abs(bt[nb] / act - 1) < 0.01, ("system rates reproduce the pilot", nb, bt[nb], act)

# 2027 territory: every qualifying home outside the six pilot neighbourhoods (rules section 2)
BUY_NB = defaultdict(float)
QUAL_HH = defaultdict(int)
for r in QUAL:
    if r["neighbourhood"] in PILOT_NB:
        continue
    BUY_NB[(r["coop"], r["neighbourhood"])] += int(r["weight"]) * RATE[SYSTEMS[r["heating_system"]]]
    QUAL_HH[r["coop"]] += int(r["weight"])
EXPECTED = {c: sum(v for (cc, _), v in BUY_NB.items() if cc == c) for c in COOPS}

# ------------------------------------------------------------------ 2. the feeder cap

FMAP = {(r["coop"], r["neighbourhood"]): r["feeder"] for r in rows_csv("area_feeder_map.csv")}
HOST = {}
for r in rows_xlsx("hosting_capacity_nov2026.xlsx", "feeders", header_row=5):
    kw = int(r["hosting_capacity_remaining_kw"])
    assert kw % KW_PER_HP == 0
    HOST[r["feeder"]] = (r["coop"], kw // KW_PER_HP)
per_feeder = defaultdict(float)
for k, v in BUY_NB.items():
    per_feeder[(k[0], FMAP[k])] += v
HOSTABLE = {c: sum(min(v, HOST[f][1]) for (cc, f), v in per_feeder.items() if cc == c) for c in COOPS}
FULL_FEEDERS = {c: sorted(f for (cc, f), v in per_feeder.items() if cc == c and v > HOST[f][1]) for c in COOPS}

# ------------------------------------------------------------------ 3. the meter crews

def holidays(y):
    """The days the co-op crews were off in 2025 and 2026 (asserted against the record below)."""
    def nth(m, wd, n):
        d = date(y, m, 1)
        return d + timedelta(days=(wd - d.weekday()) % 7) + timedelta(weeks=n - 1)

    def observed(d):
        return d + timedelta(days={5: -1, 6: 1}.get(d.weekday(), 0))
    memorial = date(y, 5, 31) - timedelta(days=date(y, 5, 31).weekday())
    thanks = nth(11, 3, 4)
    return {observed(date(y, 1, 1)), memorial, observed(date(y, 7, 4)), nth(9, 0, 1), thanks,
            thanks + timedelta(days=1), observed(date(y, 12, 25))}


FO = rows_csv("field_orders_2025_2026.csv")
assert len(FO) >= 25000
PULL = max(r["completed_date"] for r in FO if r["completed_date"])
AS_OF_YEAR_START = (date.fromisoformat(PULL) - timedelta(days=363)).isoformat()   # the 52 weeks to the pull
HP_ORDER = "HPRM"
EXCH = "MXCH"


def crew(coop):
    rows = [r for r in FO if r["coop"] == coop]
    tot, std = defaultdict(int), defaultdict(int)
    exch_req = defaultdict(int)
    for r in rows:
        if r["order_type"] == EXCH:
            exch_req[r["requested_date"]] += 1
    bday, bsize = max(exch_req.items(), key=lambda kv: kv[1])
    batch = bsize >= 50     # a one-day bulk exchange request, not a crew's ordinary exchange flow
    bdone = []
    for r in rows:
        d = r["completed_date"]
        if not d:
            continue
        tot[d] += 1
        if batch and r["order_type"] == EXCH and r["requested_date"] == bday:
            bdone.append(d)
        elif r["order_type"] != HP_ORDER:
            std[d] += 1
    days = sorted(d for d in tot if d >= "2025-01-01")
    weekdays = {date.fromisoformat(d).weekday() for d in days}
    week = sorted(weekdays)
    # the crew's working days off are exactly the holiday list, in both closed years
    for y in (2025, 2026):
        d, off = date(y, 1, 1), set()
        while d.year == y and d.isoformat() <= PULL:
            if d.weekday() in weekdays and d.isoformat() not in tot:
                off.add(d)
            d += timedelta(days=1)
        assert off == {h for h in holidays(y) if h.weekday() in weekdays and h.isoformat() <= PULL}, (coop, y, off)
    win = [d for d in days if d >= AS_OF_YEAR_START]
    standing = sum(std[d] for d in win) / len(win)
    if batch:
        plateau = [d for d in days if min(bdone) <= d < max(bdone)]
        ceiling = sum(tot[d] for d in plateau) / len(plateau)
        basis = "ceiling held while the July 2025 exchange batch was worked off"
    else:
        # no closed stretch at capacity: best 15 working days on record, a floor under the ceiling
        best = max(sum(tot[d] for d in days[i:i + 15]) / 15 for i in range(len(days) - 14))
        ceiling, plateau = best, []
        basis = "best 15 working days on record"
    return dict(week=week, standing=standing, ceiling=ceiling, spare=ceiling - standing, plateau=len(plateau),
                batch=(bday, bsize) if batch else None, basis=basis)


CREW = {c: crew(c) for c in COOPS}
FOUR_DAY = [c for c in COOPS if CREW[c]["week"] == [0, 1, 2, 3]]
assert FOUR_DAY == ["Lakes", "Uplands"] and all(CREW[c]["batch"] for c in FOUR_DAY)
assert all(CREW[c]["week"] == [0, 1, 2, 3, 4] for c in COOPS if c not in FOUR_DAY)
# standing work held its level through the batch: 2025 outside the plateau agrees with the 52 weeks to the pull
for c in FOUR_DAY:
    assert CREW[c]["plateau"] >= 40

# 2027 meter orders arrive on the pilot's calendar: one order per install, raised on the install date
for r in [r for r in FO if r["order_type"] == HP_ORDER]:
    p = next(p for p in PILOT if str(p["premises_id"]) == r["premises_id"])
    assert r["requested_date"] == day(p["install_date"]).isoformat()
ARRIVE = defaultdict(float)
for p in PILOT:
    d = day(p["install_date"])
    ARRIVE[date(YEAR, d.month, d.day)] += 1 / len(PILOT)
SPRING = sum(v for d, v in ARRIVE.items() if d.month <= 6)
FIRST_AUTUMN = min(d for d in ARRIVE if d.month >= 7)


def meter_sets(coop):
    """Day by day through 2027: an order raised on a day is worked from the crew's next working day, after the
    crew's standing work; what is set by 31 December is the co-op's useful slots."""
    k = CREW[coop]
    hol = holidays(YEAR)
    waiting, done, d = 0.0, 0.0, date(YEAR, 1, 1)
    last = None
    while d.year == YEAR:
        if d.weekday() in k["week"] and d not in hol:
            s = min(waiting, k["spare"])
            waiting -= s
            done += s
            if s > 0:
                last = d
        waiting += HOSTABLE[coop] * ARRIVE.get(d, 0.0)
        d += timedelta(days=1)
    return done, waiting, last


SETS, UNSET, LAST_SET = {}, {}, {}
for c in COOPS:
    SETS[c], UNSET[c], LAST_SET[c] = meter_sets(c)

# ------------------------------------------------------------------ 4. the split (rules section 5)

SLOTS = {c: tens(SETS[c]) for c in COOPS}
assert sum(SLOTS.values()) <= TOTAL_SLOTS        # the sharing branch does not fire
PLACED = sum(SLOTS.values())
UNALLOC = TOTAL_SLOTS - PLACED
RANK = sorted(COOPS, key=lambda c: -SLOTS[c])
LEADER, SECOND = RANK[0], RANK[1]
LEAD_BY = SLOTS[LEADER] - SLOTS[SECOND]
assert SLOTS[RANK[0]] > SLOTS[RANK[1]] and len(set(SLOTS.values())) == 6
for c in COOPS:
    r = (SETS[c] - 5) % 10
    assert min(r, 10 - r) >= 1.0, (c, SETS[c])
PILOT_N = {c: sum(1 for p in PILOT if p["coop"] == c) for c in COOPS}
MAX_LAG = max((day(p["meter_set_date"]) - day(p["install_date"])).days for p in PILOT)

# ------------------------------------------------------------------ 5. the pilot's installed cost (finance procedures 2)

BY_PREM = {str(p["premises_id"]): p for p in PILOT}
BY_REB = {str(p["rebate_id"]): p for p in PILOT}
jobs = defaultdict(list)
for r in rows_csv("installer_invoices_2026.csv"):
    jobs[r["invoice_no"]].append(r)
COST, N_JOBS, REBATE = defaultdict(float), defaultdict(int), defaultdict(float)
for no, lines in sorted(jobs.items()):
    accepted = [int(r["version"]) for r in lines if r["accepted_at"]]
    v = max(accepted)                              # the latest version the fund accepted
    rec = [r for r in lines if int(r["version"]) == v]
    heads = [r for r in rec if r["description"].startswith(HEAD_LINE)]
    # a multi-zone system is one install at the system price (price guide); the export repeats it per head
    assert len({r["amount_usd"] for r in heads}) <= 1
    cost = sum(float(r["amount_usd"]) for r in rec if r not in heads) + (float(heads[0]["amount_usd"]) if heads else 0)
    p = BY_PREM[rec[0]["premises_id"]]
    COST[p["coop"]] += cost
    N_JOBS[p["coop"]] += 1
    low = p["income_band"] == f"{LOW_BAND[0]} to {LOW_BAND[1]}"
    REBATE[p["coop"]] += SCHED[p["heating_system_replaced"]] + (TOP_UP if low else 0)
assert N_JOBS == PILOT_N, "one invoice of record per pilot install"
AVG_COST = {c: COST[c] / N_JOBS[c] for c in COOPS}
SHARE = {c: 100 * REBATE[c] / COST[c] for c in COOPS}
AVG_COST_ALL = sum(COST.values()) / sum(N_JOBS.values())
SHARE_ALL = 100 * sum(REBATE.values()) / sum(COST.values())

# ------------------------------------------------------------------ 6. rebates paid through 30 November (finance procedures 4, 5)

MONTH_END = date(2026, 11, 30)
returned = {n["original_payment_reference"] for n in json.loads((T / "bank_returns_2026.json").read_text())["notices"]}
PAID, COVERED = defaultdict(float), defaultdict(set)
for r in rows_csv("rebate_payments_2026.csv"):
    if not r["cleared_at"] or r["payment_id"] in returned:
        continue
    cleared = datetime.strptime(r["cleared_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if cleared.astimezone(CT).date() > MONTH_END:
        continue
    c = BY_REB[r["rebate_id"]]["coop"]
    PAID[c] += float(r["amount_usd"])
    COVERED[c].add(r["rebate_id"])
N_COVERED = {c: len(COVERED[c]) for c in COOPS}
for c in COOPS:
    assert N_COVERED[c] <= PILOT_N[c] and abs(PAID[c] - round(PAID[c])) < 1e-9
    ra = (AVG_COST[c] - 0.5) % 1
    rs = (SHARE[c] - 0.05) % 0.1
    assert min(ra, 1 - ra) >= 0.2 and min(rs, 0.1 - rs) >= 0.02, (c, AVG_COST[c], SHARE[c])


def money(v):
    return f"${v:,.0f}"


# ------------------------------------------------------------------ deliverable: coop_slot_split_2027.csv

def write_csv(path):
    hdr = ["coop", "slots_2027", "pilot_avg_installed_cost_usd", "pilot_rebate_share_of_cost_pct",
           "pilot_rebates_paid_thru_2026_11_30_usd", "pilot_installs_covered_by_payments"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(hdr)
        for c in COOPS:
            w.writerow([c, SLOTS[c], round(AVG_COST[c]), f"{SHARE[c]:.1f}", round(PAID[c]), N_COVERED[c]])
        w.writerow(["Total", PLACED, round(AVG_COST_ALL), f"{SHARE_ALL:.1f}", round(sum(PAID.values())),
                    sum(N_COVERED.values())])


# ------------------------------------------------------------------ deliverable: coop_slots_2027.svg

INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#fcfcfb"
C_2027, C_2026, C_HELD = "#2a78d6", "#eb6834", "#b9b8b2"


def write_svg(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams.update({"svg.hashsalt": "chf-2027-split", "svg.fonttype": "none",
                                "font.family": "DejaVu Sans", "font.size": 10})
    order = RANK                                     # largest 2027 allocation first
    fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=100)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    w, gap = 0.36, 0.04
    xs = list(range(len(order)))
    for i, c in enumerate(order):
        for dx, val, col in ((-(w + gap) / 2, SLOTS[c], C_2027), ((w + gap) / 2, PILOT_N[c], C_2026)):
            ax.bar(i + dx, val, width=w, color=col, edgecolor=SURFACE, linewidth=1)
            ax.text(i + dx, val + 6, f"{val:,}", ha="center", va="bottom", fontsize=9, color=INK)
    xh = len(order) + 0.35
    ax.bar(xh, UNALLOC, width=w, color=C_HELD, edgecolor=SURFACE, linewidth=1, hatch="//")
    ax.text(xh, UNALLOC + 6, f"{UNALLOC:,}", ha="center", va="bottom", fontsize=9, color=INK)
    ax.axvline(len(order) - 0.35, color=GRID, linewidth=1)
    ax.set_xticks(xs + [xh])
    ax.set_xticklabels(order + ["Unallocated\n(held by the fund)"], color=INK2)
    ax.set_ylabel("Rebate slots (2027) / rebated installs (2026)", color=INK2)
    ax.set_ylim(0, 700)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(axis="both", length=0, colors=INK2)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=C_2027, label="2027 slots"), Patch(color=C_2026, label="2026 pilot installs"),
                       Patch(facecolor=C_HELD, hatch="//", edgecolor=SURFACE, label="Slots not allocated")],
              loc="upper left", frameon=False, fontsize=9, ncol=3, bbox_to_anchor=(0, 1.02))
    fig.suptitle(f"2027 rebate slots: {PLACED:,} of {TOTAL_SLOTS:,} placed, {LEADER} takes the most",
                 x=0.06, ha="left", fontsize=13, fontweight="bold", color=INK, y=0.97)
    fig.text(0.06, 0.02, "Slots per co-operative under section 5 of the programme rules, in tens. "
             f"2026 pilot installs from the pilot rebate log, {len(PILOT):,} in all.", fontsize=8, color=MUTED)
    fig.subplots_adjust(left=0.08, right=0.98, top=0.86, bottom=0.16)
    fig.savefig(path, format="svg", facecolor=SURFACE, metadata={"Date": None, "Creator": None})
    plt.close(fig)


# ------------------------------------------------------------------ deliverable: slot_split_board_note_2027.docx

def write_docx(path):
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt, RGBColor, Cm

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
    sec.left_margin = sec.right_margin = Cm(2.3)
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
    st = doc.styles["Normal"]
    st.font.name, st.font.size = "Calibri", Pt(10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    st.paragraph_format.space_after = Pt(6)
    for name, size in (("Heading 1", 15), ("Heading 2", 12)):
        h = doc.styles[name]
        h.font.name, h.font.size, h.font.bold = "Calibri", Pt(size), True
        h.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            h.element.rPr.rFonts.attrib.pop(qn(a), None)

    def field(par, instr):
        for kind, text in (("begin", None), (None, instr), ("separate", None), (None, "1"), ("end", None)):
            r = par.add_run()
            if kind:
                e = OxmlElement("w:fldChar")
                e.set(qn("w:fldCharType"), kind)
                r._r.append(e)
            elif text == instr:
                e = OxmlElement("w:instrText")
                e.set(qn("xml:space"), "preserve")
                e.text = f" {instr} "
                r._r.append(e)
            else:
                r.text = text
        return par

    hp = sec.header.paragraphs[0]
    hp.text = "Minnesota Clean Heat Fund  |  Board of Trustees, 17 December 2026  |  Item 4"
    hp.runs[0].font.size, hp.runs[0].font.color.rgb = Pt(8.5), RGBColor(0x52, 0x51, 0x4E)
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = fp.add_run("Internal: trustees and staff only.   Page ")
    field(fp, "PAGE")
    fp.add_run(" of ")
    field(fp, "NUMPAGES")
    for r in fp.runs:
        r.font.size, r.font.color.rgb = Pt(8.5), RGBColor(0x52, 0x51, 0x4E)

    def shade(cell, hexfill):
        tcPr = cell._tc.get_or_add_tcPr()
        s = OxmlElement("w:shd")
        s.set(qn("w:val"), "clear")
        s.set(qn("w:color"), "auto")
        s.set(qn("w:fill"), hexfill)
        tcPr.append(s)

    def table(header, rows, widths, bold_rows=(), note=None):
        t = doc.add_table(rows=1, cols=len(header))
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        for j, h in enumerate(header):
            c = t.rows[0].cells[j]
            c.text = ""
            run = c.paragraphs[0].add_run(h)
            run.bold, run.font.size = True, Pt(9.5)
            shade(c, "E8EEF5")
            if j:
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for i, row in enumerate(rows):
            cells = t.add_row().cells
            for j, v in enumerate(row):
                cells[j].text = ""
                run = cells[j].paragraphs[0].add_run(str(v))
                run.font.size = Pt(9.5)
                run.bold = i in bold_rows
                if j:
                    cells[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        t.autofit = False
        tblPr = t._tbl.tblPr
        lay = OxmlElement("w:tblLayout")
        lay.set(qn("w:type"), "fixed")
        tblPr.append(lay)
        for j, wcm in enumerate(widths):
            t.columns[j].width = Cm(wcm)
        for row in t.rows:
            for j, wcm in enumerate(widths):
                row.cells[j].width = Cm(wcm)
        if note:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(3)
            run = p.add_run(note)
            run.italic, run.font.size, run.font.color.rgb = True, Pt(8.5), RGBColor(0x52, 0x51, 0x4E)
        return t

    def para(text, size=None, bold=False, italic=False, after=None):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold, run.italic = bold, italic
        if size:
            run.font.size = Pt(size)
        if after is not None:
            p.paragraph_format.space_after = Pt(after)
        return p

    def fr(k):
        f = RATE_FR[k]
        return f"{f.numerator} in {f.denominator}"
    lk, up = CREW["Lakes"], CREW["Uplands"]
    # the prose's own claims, checked against the figures they describe
    assert abs(SPRING - 0.25) < 1e-9 and FULL_FEEDERS["North Shore"] == ["NS-411", "NS-414"]
    assert FULL_FEEDERS["Valley"] == ["VA-205", "VA-206"]
    for c in ("North Shore", "Valley"):
        assert sum(v for (cc, f), v in per_feeder.items() if cc == c and f in FULL_FEEDERS[c]) > 0.5 * EXPECTED[c]
        assert all(HOST[f][1] <= 0.5 * per_feeder[(c, f)] for f in FULL_FEEDERS[c])
    up_low = sum(int(r["weight"]) for r in QUAL if r["coop"] == "Uplands" and r["neighbourhood"] not in PILOT_NB
                 and r["heating_system"] in ("PB", "ER")) / QUAL_HH["Uplands"]
    assert 0.65 <= up_low < 0.75 and max(QUAL_HH, key=QUAL_HH.get) == "Uplands"
    assert sorted(COOPS, key=lambda c: -EXPECTED[c]).index("Uplands") == 3
    assert all(CREW[c]["week"] == [0, 1, 2, 3] for c in ("Lakes", "Uplands"))
    others = [c for c in COOPS if c not in FOUR_DAY]
    last_other = max(LAST_SET[c] for c in others)

    doc.add_heading(f"Programme year 2: place {PLACED:,} of the {TOTAL_SLOTS:,} rebate slots, "
                    f"with {LEADER} taking the most", level=1)
    para("Paper from Stephanie O'Connor, programme director. 11 December 2026. For decision.",
         size=9.5, italic=True, after=10)
    para(f"I recommend the trustees adopt this split of the fund's {TOTAL_SLOTS:,} heat-pump rebate slots for 2027 "
         f"under section 5 of the programme rules, and hold the other {UNALLOC:,} unallocated.")
    table(["Co-operative", "2027 slots"],
          [[c, f"{SLOTS[c]:,}"] for c in COOPS] + [["Allocated", f"{PLACED:,}"],
                                                   ["Not allocated, held by the fund", f"{UNALLOC:,}"],
                                                   ["Fund total", f"{TOTAL_SLOTS:,}"]],
          [6.5, 2.5], bold_rows=(6, 8))
    para(f"{LEADER} takes the most slots, {SLOTS[LEADER]:,}, which is {LEAD_BY:,} more than {SECOND} "
         f"at {SLOTS[SECOND]:,}.", bold=True)

    doc.add_heading("Why the split places fewer than the 1,800", level=2)
    para("Section 5 gives each co-operative the rebated installs we expect in its territory in 2027, to the nearest "
         "ten, and section 4 only counts an install once the co-operative has set the heat-pump rate meter. Slots "
         "a co-operative cannot turn into a set meter by 31 December lapse, so they are not allocated. Three things "
         "decide each line of the split.")
    para("Demand. The Heat Survey 2025 sample records give the eligible homes in each territory directly (owner-"
         "occupied detached homes on propane or electric resistance heat, income $35,000 to $149,999), leaving out "
         "the six pilot neighbourhoods, which are not in programme year 2. The pilot converted eligible homes at a "
         "rate that depends on the heating system it replaced: "
         f"{fr('propane furnace (ducted)')} homes with a propane furnace, {fr('electric resistance')} on electric "
         f"resistance and {fr('propane boiler (hydronic)')} with a propane boiler. Those three rates reproduce the installs "
         "in every pilot neighbourhood; one pooled rate does not.")
    para(f"Feeder room. Under section 3 of the participation terms each heat pump takes {KW_PER_HP} kW of the "
         "hosting capacity filed for its feeder, and an install cannot proceed without it. Most of North Shore's and "
         "Valley's demand sits on feeders filed with room for far fewer heat pumps than their homes would buy ("
         + "; ".join(f"{f} takes {HOST[f][1]}" for c in ("North Shore", "Valley") for f in FULL_FEEDERS[c])
         + f"), so their feeders take {HOSTABLE['North Shore']:,.0f} and {HOSTABLE['Valley']:,.0f} of the installs we "
         "would otherwise expect there.")
    para("Meter sets before year-end. Every rebated install raises a field order for the co-operative's meter crew, "
         "and the crew works it after its standing work (exchanges, new services, tests, disconnects and "
         f"reconnects). The pilot never tested this: every pilot meter was set within {MAX_LAG} days of the install. "
         "Lakes and Uplands run three-person crews on four ten-hour days. While they worked off the July 2025 "
         f"meter-exchange batch their completions held flat at {lk['ceiling']:.2f} and {up['ceiling']:.2f} orders a working day "
         f"and their standing work carried on at its usual level, which over the year to the {date.fromisoformat(PULL):%-d %B} pull was "
         f"{lk['standing']:.2f} and {up['standing']:.2f} a day. That leaves room for {lk['spare']:.2f} and "
         f"{up['spare']:.2f} heat-pump meter sets a working day. Both windows open on the pilot's dates, and three "
         "quarters of the pilot's installs came out of the autumn window, so from late September both crews have "
         f"more orders than they can set. By 31 December Lakes sets {SETS['Lakes']:,.0f} meters and Uplands "
         f"{SETS['Uplands']:,.0f}; the rest would still be waiting on 31 December and their slots would lapse. The "
         f"other four crews work five days and set every programme meter by {last_other:%-d %B}.")
    table(["Co-operative", "Expected installs", "Feeders can take", "Meters set by 31 Dec", "2027 slots",
           "2026 pilot installs"],
          [[c, f"{EXPECTED[c]:,.0f}", f"{HOSTABLE[c]:,.0f}", f"{SETS[c]:,.0f}", f"{SLOTS[c]:,}", f"{PILOT_N[c]:,}"]
           for c in COOPS] + [["Total", "", "", "", f"{PLACED:,}", f"{sum(PILOT_N.values()):,}"]],
          [3.2, 2.6, 2.6, 2.8, 2.2, 2.6], bold_rows=(6,),
          note="Sources: Heat Survey 2025 sample records (weighted); 2026 pilot rebate log; hosting capacity filings "
               "as at 30 November 2026; meter-shop field orders to the " f"{date.fromisoformat(PULL):%-d %B} pull. Expected installs, feeder "
               "room and meter sets are whole installs; slots are each co-operative's meter sets to the nearest ten, "
               "per section 5, and the total is the sum of the co-operatives' slots.")

    doc.add_heading("On the comments received", level=2)
    para(f"Sara Duncan is right that Uplands has more qualifying homes than any other co-operative "
         f"({QUAL_HH['Uplands']:,} outside the pilot neighbourhood on the survey's weights). Seven in ten of them heat "
         "with a propane boiler or electric resistance, the two systems the pilot converted least often, so Uplands "
         "expects fewer installs than North Shore, Valley or Lakes before its crew is counted. The spring outreach "
         "booked there still has a use: spring orders reach the crew while it has room.")
    para("Larry Woodward's firms can install what we fund, and nothing here says otherwise. The limit at Lakes and "
         "Uplands is the co-operative's own meter set, which follows the install. The state energy office's match "
         "apportionment on Table H1 is its own basis for its own money and does not set our slots.")

    doc.add_heading("What the pilot cost and what we have paid, by co-operative", level=2)
    table(["Co-operative", "Average installed cost", "Rebate as share of cost", "Rebates paid to 30 Nov",
           "Pilot installs covered"],
          [[c, money(AVG_COST[c]), f"{SHARE[c]:.1f}%", money(PAID[c]), f"{N_COVERED[c]:,}"] for c in COOPS]
          + [["All six", money(AVG_COST_ALL), f"{SHARE_ALL:.1f}%", money(sum(PAID.values())),
              f"{sum(N_COVERED.values()):,}"]],
          [3.2, 3.2, 3.2, 3.2, 3.0], bold_rows=(6,),
          note="Installed cost is the invoice of record for each pilot install, the latest version the fund accepted "
               "(finance procedures, section 2); a multi-zone ductless system is one install at its system price, "
               "as the installers' price guide sets it, however many indoor-head lines the invoice carries. The "
               "rebate is the Schedule B amount for the heating system replaced, with the income addition where it "
               "applies. Payments count on the date they cleared, in Central time, through the 30 November month "
               "end; returned payments are left out and reissued payments counted when they cleared (finance "
               "procedures, sections 4 and 5).")

    cp = doc.core_properties
    cp.author = cp.last_modified_by = "Stephanie O'Connor"
    cp.title = "Programme year 2 slot split"
    cp.subject = cp.comments = cp.keywords = cp.category = ""
    cp.created = cp.modified = datetime(2026, 12, 11, 9, 40)
    cp.revision = 3
    doc.save(path)
    sys.path.insert(0, str(HERE))
    sys.dont_write_bytecode = True
    import writers as W      # deterministic container only; no data
    W.normalise_zip(path, when=(2026, 12, 11, 9, 40, 0))


def main():
    OUT.mkdir(exist_ok=True)
    write_csv(OUT / "coop_slot_split_2027.csv")
    write_svg(OUT / "coop_slots_2027.svg")
    write_docx(OUT / "slot_split_board_note_2027.docx")
    print("Install rates by heating system replaced (pilot installs over eligible pilot-neighbourhood homes):")
    for s, v in RATE.items():
        print(f"  {s:<28} {RATE_FR[s].numerator} in {RATE_FR[s].denominator}  ({100 * v:.4f}%)")
    print("Meter crews (orders a working day):")
    for c in FOUR_DAY:
        k = CREW[c]
        print(f"  {c:<12} ceiling {k['ceiling']:6.2f}  standing {k['standing']:6.2f}  spare {k['spare']:5.2f}")
    print(f"{'co-op':<12}{'expected':>10}{'feeders':>10}{'set 31 Dec':>12}{'slots':>8}")
    for c in COOPS:
        print(f"{c:<12}{EXPECTED[c]:10.2f}{HOSTABLE[c]:10.2f}{SETS[c]:12.2f}{SLOTS[c]:8,}")
    print(f"Placed {PLACED:,} of {TOTAL_SLOTS:,}; unallocated {UNALLOC:,}; {LEADER} leads {SECOND} by {LEAD_BY:,}")
    print("Pilot: avg installed cost, rebate share, paid to 30 Nov, installs covered")
    for c in COOPS:
        print(f"  {c:<12}{money(AVG_COST[c]):>9}{SHARE[c]:7.1f}%{money(PAID[c]):>11}{N_COVERED[c]:5}")


if __name__ == "__main__":
    main()
