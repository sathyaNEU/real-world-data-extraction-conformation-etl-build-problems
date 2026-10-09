#!/usr/bin/env python3
"""TY2025 income tax tier schedule: the workbook and the chart for the finance secretary.

    python3 task120/generator/golden.py [target_dir] [out_dir]

Reads only the research extracts and the Conference tables in target_dir, writes tier_schedule.xlsx and
tier_floors.png to out_dir, and prints the schedule, the reproduction count and the tier base.
"""
import datetime as dt
import io
import math
import os
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import duckdb
import numpy as np
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.page import PageMargins

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter, NullLocator  # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent / "target"
OUT = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else HERE.parent / "golden"

TY = 2025
PUBLISHED_YEARS = (2022, 2023, 2024)          # the three most recent Household Income Tables
MARKS = (10, 5, 1)                             # methodology s.2
OFFICE = "Office of Revenue Research"
PREPARED = dt.datetime(2026, 11, 9, 9, 0)      # date the schedule goes to the secretary
SCRUB = REPO / ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py"

# The build record's figures; the golden must land on them exactly.
RECORD = {
    "floors": (214_000, 318_000, 742_000), "units": 582_544, "hits": 69,
    "receipts": {1: (57_100_430, 60_982_470, 59_690_330, 62_279_690),
                 2: (27_130_950, 28_344_190, 28_273_480, 29_413_200),
                 3: (12_597_420, 13_026_520, 13_083_940, 13_625_350)},
    "withholding": {1: 135_364_253, 2: 229_035_640, 3: 184_720_391},
    "gain": {1: 3_147_270_635, 2: 995_783_766, 3: 339_052_645},
    "share": {1: 30.4, 2: 10.1, 3: 4.5},
}


def nearest_thousand(x):
    return int(math.floor(x / 1000.0 + 0.5)) * 1000


def thousands_half_up(x):
    q, r = divmod(int(x), 1000)
    return q + (1 if r >= 500 else 0)


# --------------------------------------------------------------------------------------------- loading
def load(con):
    for y in PUBLISHED_YEARS + (TY,):
        con.execute(f"create table r{y} as select * from read_parquet('{TARGET}/returns_processed_ty{y}.parquet')")
        con.execute(f"create table s{y} as select * from read_parquet('{TARGET}/dependents_schedule_ty{y}.parquet')")
    con.execute(f"create table ledger as select * from read_parquet('{TARGET}/estimated_payments_ledger_2025.parquet')")
    con.execute(f"create table returned as select * from read_csv('{TARGET}/returned_items_2025.csv', header=true)")
    con.execute(f"create table reg as select * from read_csv('{TARGET}/tin_match_cases.csv', header=true)")
    con.execute(f"create table schd as select * from read_csv('{TARGET}/schedule_d_extract_ty2025.csv', header=true)")
    con.execute(f"create table amended as select * from read_csv('{TARGET}/amended_returns_log_ty2025.csv', header=true)")
    con.execute(f"create table efile as select * from read_parquet('{TARGET}/wage_statements_efile_ty2025.parquet')")
    # paper statements, capture vendor fixed-width layout (record layouts s.8b)
    rows = [(int(l[10:19]), int(l[19:28]), int(l[43:53]))
            for l in open(TARGET / "w2_paper_keyed_ty2025.txt", encoding="ascii")]
    con.execute("create table paper (employer_ein bigint, employee_tin bigint, state_tax_withheld bigint)")
    con.executemany("insert into paper values (?, ?, ?)", rows)


def households_sql(y):
    """Full-year resident household units: each federal filing unit (a spouse's separate state return joins its
    partner's on the federal primary TIN) plus the own returns of the dependents its returns claim."""
    return f"""
      with r as (select * from r{y} where residency_code = 1),
      d as (select r.return_id, c.federal_primary_tin as claimant_fpt
            from r join s{y} s on r.filer_tin = s.dependent_tin
                   join r c on c.return_id = s.claimant_return_id)
      select coalesce(d.claimant_fpt, r.federal_primary_tin) as hkey, sum(r.federal_agi)::bigint as agi
      from r left join d on r.return_id = d.return_id group by 1"""


def county_sql(y):
    # the household's county is its federal primary filer's county of residence
    return f"select filer_tin as hkey, county_code from r{y} where residency_code = 1 and filer_tin = federal_primary_tin"


# --------------------------------------------------------------------------------------------- the corpus
def read_tables():
    cells = []   # (year, label, measure, published, key)
    for y in PUBLISHED_YEARS:
        wb = openpyxl.load_workbook(TARGET / f"household_income_tables_ty{y}.xlsx", data_only=True)
        for row in wb["Table 1"].iter_rows(values_only=True):
            if isinstance(row[0], str) and row[0].startswith("$") and isinstance(row[1], (int, float)):
                lo, hi = class_bounds(row[0])
                cells.append((y, row[0], "Household units", int(row[1]), ("units", lo, hi)))
                cells.append((y, row[0], "Federal AGI ($ thousands)", int(row[2]), ("agi_k", lo, hi)))
            elif isinstance(row[0], str) and row[0].startswith("All full-year resident"):
                cells.append((y, "All full-year resident household units", "Federal AGI ($ thousands)",
                              int(row[2]), ("total",)))
        if "Appendix A" in wb.sheetnames:
            for row in wb["Appendix A"].iter_rows(values_only=True):
                if row[1] and str(row[1]).isdigit() and isinstance(row[2], (int, float)):
                    cells.append((y, f"{row[0]} ({row[1]}), $500,000 or more", "Household units", int(row[2]),
                                  ("county", str(row[1]))))
    return cells


def class_bounds(label):
    nums = [int(x.replace(",", "")) for x in re.findall(r"\$([\d,]+)", label)]
    return nums[0], (nums[1] if len(nums) > 1 else None)


def rebuild(con, y, key):
    sql = households_sql(y)
    if key[0] == "total":
        return thousands_half_up(con.execute(f"select sum(agi) from ({sql})").fetchone()[0])
    if key[0] == "county":
        return con.execute(f"select count(*) from ({sql}) u join ({county_sql(y)}) k using (hkey) "
                           f"where u.agi >= 500000 and k.county_code = '{key[1]}'").fetchone()[0]
    _, lo, hi = key
    cond = f"agi >= {lo}" + (f" and agi < {hi}" if hi else "")
    n, s = con.execute(f"select count(*), coalesce(sum(agi), 0) from ({sql}) where {cond}").fetchone()
    return int(n) if key[0] == "units" else thousands_half_up(s)


# --------------------------------------------------------------------------------------------- the schedule
def schedule(con):
    con.execute(f"create table hh as {households_sql(TY)}")
    n = con.execute("select count(*) from hh").fetchone()[0]
    out = []
    for p in MARKS:
        k = (n * p + 99) // 100          # the k-th largest household AGI marks the top p per cent
        agi = con.execute(f"select agi from hh order by agi desc limit 1 offset {k - 1}").fetchone()[0]
        out.append((p, k, int(agi), nearest_thousand(agi)))
    return n, out


def tiers(con, floors):
    f10, f5, f1 = floors
    con.execute(f"""create table t_ret as
        with r as (select * from r{TY} where residency_code = 1),
        d as (select r.return_id, c.federal_primary_tin as claimant_fpt
              from r join s{TY} s on r.filer_tin = s.dependent_tin join r c on c.return_id = s.claimant_return_id)
        select r.return_id, r.filer_tin, r.spouse_tin, r.filing_status,
               coalesce(d.claimant_fpt, r.federal_primary_tin) as hkey
        from r left join d on r.return_id = d.return_id""")
    con.execute(f"""create table t_hh as select hkey, agi,
        case when agi >= {f1} then 1 when agi >= {f5} then 2 when agi >= {f10} then 3 else 0 end as t from hh""")
    # every TIN that belongs to a household: its filers and the spouses on its joint returns
    con.execute("""create table t_member as
        select r.filer_tin as tin, h.t from t_ret r join t_hh h using (hkey)
        union all select r.spouse_tin, h.t from t_ret r join t_hh h using (hkey)
        where r.filing_status = 2 and r.spouse_tin is not null""")
    con.execute("create table t_rid as select r.return_id, h.t from t_ret r join t_hh h using (hkey)")
    rows = con.execute("select t, count(*), sum(agi)::bigint from t_hh where t > 0 group by t order by t").fetchall()
    return {int(t): (int(c), int(a)) for t, c, a in rows}


def tier_of(col):
    """Tier of a TIN as reported, read through the resolved TIN match cases."""
    return ("coalesce(m.t, m2.t, 0)",
            f"left join t_member m on {col} = m.tin "
            f"left join (select * from reg where case_status = 'RESOLVED') g on {col} = g.reported_tin "
            f"left join t_member m2 on g.resolved_tin = m2.tin")


def due_dates():
    """Instalment due dates for TY2025, a weekend date moving to the next business day (record layouts s.3)."""
    out = []
    for y, m in ((TY, 4), (TY, 6), (TY, 9), (TY + 1, 1)):
        d = dt.date(y, m, 15)
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        out.append(d)
    return out


def receipts(con, due):
    # Cash received toward TY2025: ES payments not returned unpaid (a re-presented item that paid stays), plus
    # transfers into 2025 of a payment misapplied to another year, dated by that payment. Transfers citing a
    # TY2024 return are credit elections, which methodology s.4 excludes.
    d1, d2, d3, _ = (f"timestamp '{d.isoformat()} 23:59:59'" for d in due)
    expr, joins = tier_of("p.tin")
    sql = f"""
      with p as (
        select account_tin as tin, amount, cast(txn_utc as timestamptz) as ts from ledger
        where tax_year = {TY} and txn_type = 'ES'
          and txn_id not in (select txn_id from returned where coalesce(represented_result, '') <> 'PAID')
        union all
        select l.account_tin, l.amount, cast(o.txn_utc as timestamptz) from ledger l
        join ledger o on l.source_ref = cast(o.txn_id as varchar)
        where l.tax_year = {TY} and l.txn_type = 'TRF'),
      q as (select p.amount, timezone('America/Chicago', p.ts) as local_ts, {expr} as t from p {joins})
      select t, case when local_ts <= {d1} then 1 when local_ts <= {d2} then 2
                     when local_ts <= {d3} then 3 else 4 end as k, sum(amount)::bigint
      from q where t > 0 group by all"""
    out = {(t, k): 0 for t in (1, 2, 3) for k in (1, 2, 3, 4)}
    for t, k, s in con.execute(sql).fetchall():
        out[(int(t), int(k))] = int(s)
    return out


def capital_gain(con):
    # amount entering AGI, on each return's version of record (latest accepted version in the amended log)
    sql = """
      with a as (select return_id, amount_in_agi as v from (
                   select *, row_number() over (partition by return_id order by amendment_seq desc) rn
                   from amended where disposition = 'ACCEPTED' and amount_in_agi is not null) where rn = 1),
      x as (select e.return_id, coalesce(a.v, e.amount_in_agi) as g from schd e left join a using (return_id))
      select t.t, sum(x.g)::bigint from x join t_rid t using (return_id) where t.t > 0 group by 1"""
    return {int(t): int(s) for t, s in con.execute(sql).fetchall()}


def withholding(con):
    expr, joins = tier_of("p.tin")
    sql = f"""
      with p as (select employee_tin as tin, state_tax_withheld as w from efile
                 union all select employee_tin, state_tax_withheld from paper),
      q as (select p.w, {expr} as t from p {joins})
      select t, sum(w)::bigint from q where t > 0 group by 1"""
    return {int(t): int(s) for t, s in con.execute(sql).fetchall()}


def survival(con):
    """Household AGI of every unit at $100,000 or more, descending, for the at-or-above curve."""
    return np.array([r[0] for r in con.execute("select agi from hh where agi >= 100000 order by agi desc").fetchall()],
                    dtype=float)


# --------------------------------------------------------------------------------------------- workbook
INK = "1F2933"
MUTED = "5F6B76"
RULE = Side(style="thin", color="B8C2CC")
HEAD_FILL = PatternFill("solid", fgColor="E8EEF5")
USD = '"$"#,##0'
COUNT = "#,##0"


def head_row(ws, r, labels, widths=None, text_cols=(1,)):
    for c, lab in enumerate(labels, 1):
        cell = ws.cell(r, c, lab)
        cell.font = Font(name="Arial", bold=True, size=9, color=INK)
        cell.fill = HEAD_FILL
        cell.border = Border(bottom=RULE)
        cell.alignment = Alignment(horizontal="left" if c in text_cols else "right", vertical="bottom", wrap_text=True)
    if widths:
        for c, w in enumerate(widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(c)].width = w


def put(ws, r, c, v, fmt=None, bold=False, color=INK, align=None, size=10):
    cell = ws.cell(r, c, v)
    cell.font = Font(name="Arial", size=size, bold=bold, color=color)
    if fmt:
        cell.number_format = fmt
    if align:
        cell.alignment = Alignment(horizontal=align, vertical="top", wrap_text=(align == "wrap"))
    return cell


def note(ws, r, text, size=9, color=MUTED, italic=False):
    cell = ws.cell(r, 1, text)
    cell.font = Font(name="Arial", size=size, color=color, italic=italic)
    return cell


def write_workbook(path, n_units, sched, corpus, hits, tier_rows, rec, gain, wh, share, due):
    floors = [s[3] for s in sched]
    wb = Workbook()

    # ---- Schedule
    ws = wb.active
    ws.title = "Schedule"
    ws.sheet_view.showGridLines = False
    put(ws, 1, 1, OFFICE, bold=True, size=9, color=MUTED)
    put(ws, 2, 1, "Income tax tier schedule, tax year 2025", bold=True, size=14)
    put(ws, 3, 1, "For adoption by the finance secretary ahead of the Conference's certification of the "
                  "income tax estimate. 9 November 2026.", size=9, color=MUTED)
    put(ws, 5, 1, f"Adopt TY2025 tier floors of ${floors[0]:,} for the top 10 per cent, ${floors[1]:,} for the top "
                  f"5 per cent and ${floors[2]:,} for the top 1 per cent of full-year resident household units by "
                  f"household federal AGI.", bold=True, size=11)
    ws.merge_cells("A5:F6")
    ws["A5"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[5].height = 18
    ws.row_dimensions[6].height = 18
    head_row(ws, 8, ["Tier", "Mark", "Floor (household federal AGI)", "Household units in tier",
                     "Household units at or above floor", "Tier runs"], [25, 16, 20, 16, 18, 30], text_cols=(1, 2, 6))
    tier_for_mark = {10: 3, 5: 2, 1: 1}
    upper = {3: f"to ${floors[1] - 1:,}", 2: f"to ${floors[2] - 1:,}", 1: "and above"}
    for i, (p, k, _agi, f) in enumerate(sched):
        r = 9 + i
        t = tier_for_mark[p]
        put(ws, r, 1, f"Tier {t}")
        put(ws, r, 2, f"Top {p} per cent")
        put(ws, r, 3, f, USD, bold=True)
        put(ws, r, 4, tier_rows[t][0], COUNT)
        put(ws, r, 5, k, COUNT)
        put(ws, r, 6, f"  ${f:,} {upper[t]}")
    r = 13
    put(ws, r, 1, "Basis", bold=True, size=10)
    basis = [
        ("Population", f"{n_units:,} full-year resident household units, tax year 2025 (methodology s.2)", COUNT),
        ("Unit", "Federal filing unit (a spouse's separate state return joined to its partner's on the federal "
                 "primary TIN), plus the own returns of the dependents its returns claim on the dependents schedule", None),
        ("Published cells reproduced", f"{hits} of {len(corpus)} (Household Income Tables TY2022 to TY2024, Appendix A "
                                       f"included; see Reproduction)", None),
        ("Floor convention", "AGI of the k-th largest household, k = units x mark rounded up, stated to the nearest "
                             "$1,000", None),
    ]
    for i, (lab, txt, _) in enumerate(basis):
        put(ws, r + 1 + i, 1, lab, size=9, color=MUTED).alignment = Alignment(vertical="top")
        c = put(ws, r + 1 + i, 2, txt, size=9)
        ws.merge_cells(start_row=r + 1 + i, start_column=2, end_row=r + 1 + i, end_column=6)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r + 1 + i].height = 26
    ws.freeze_panes = "A9"
    ws.print_area = "A1:F17"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    # ---- Reproduction
    ws = wb.create_sheet("Reproduction")
    ws.sheet_view.showGridLines = False
    put(ws, 1, 1, "Household Income Tables TY2022 to TY2024: published cells and the household rebuild",
        bold=True, size=12)
    put(ws, 2, 1, f"Cells matched: {hits} of {len(corpus)}", bold=True, size=10)
    head_row(ws, 4, ["Tax year", "Cell", "Measure", "Published", "Rebuilt", "Match"], [9, 44, 24, 14, 14, 8],
             text_cols=(1, 2, 3))
    for i, (y, label, measure, pub, _key, reb) in enumerate(corpus):
        r = 5 + i
        put(ws, r, 1, y, "0")
        put(ws, r, 2, label)
        put(ws, r, 3, measure)
        put(ws, r, 4, pub, COUNT)
        put(ws, r, 5, reb, COUNT)
        put(ws, r, 6, "yes" if pub == reb else "no", align="right")
    last = 4 + len(corpus)
    note(ws, last + 2, "Rebuilt in the published units: whole household counts, AGI in $ thousands rounded half up "
                       "from whole-dollar household totals. County cells place each household in its primary "
                       "filer's county of residence.")
    note(ws, last + 3, "Sources: household_income_tables_ty2022.xlsx to _ty2024.xlsx; returns_processed_ty2022 to "
                       "_ty2024 and dependents_schedule_ty2022 to _ty2024 (research extracts, as of record).")
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:F{last}"
    ws.print_title_rows = "4:4"
    ws.print_area = f"A1:F{last + 3}"

    # ---- Tier base 2025
    ws = wb.create_sheet("Tier base 2025")
    ws.sheet_view.showGridLines = False
    put(ws, 1, 1, "Tier base, tax year 2025, on the adopted floors (whole dollars)", bold=True, size=12)
    labels = ["Tier", "Household units", "Household federal AGI"] + \
             [f"Estimated-tax receipts, instalment {i} (due {d.day} {d:%b %Y})" for i, d in enumerate(due, 1)] + \
             ["Withholding", "Net capital gain", "Net capital gain, share of tier AGI (%)"]
    head_row(ws, 3, labels, [9, 12, 18, 17, 17, 17, 17, 16, 17, 14])
    ws.row_dimensions[3].height = 54
    for i, t in enumerate((1, 2, 3)):
        r = 4 + i
        put(ws, r, 1, f"Tier {t}")
        put(ws, r, 2, tier_rows[t][0], COUNT)
        put(ws, r, 3, tier_rows[t][1], USD)
        for k in (1, 2, 3, 4):
            put(ws, r, 3 + k, rec[(t, k)], USD)
        put(ws, r, 8, wh[t], USD)
        put(ws, r, 9, gain[t], USD)
        put(ws, r, 10, share[t], "0.0")
    r = 7
    put(ws, r, 1, "Tiers 1-3", bold=True)
    put(ws, r, 2, sum(tier_rows[t][0] for t in (1, 2, 3)), COUNT, bold=True)
    put(ws, r, 3, sum(tier_rows[t][1] for t in (1, 2, 3)), USD, bold=True)
    for k in (1, 2, 3, 4):
        put(ws, r, 3 + k, sum(rec[(t, k)] for t in (1, 2, 3)), USD, bold=True)
    put(ws, r, 8, sum(wh.values()), USD, bold=True)
    put(ws, r, 9, sum(gain.values()), USD, bold=True)
    for c in range(1, 11):
        ws.cell(r, c).border = Border(top=RULE)
    notes = [
        "Receipts are cash received toward TY2025 (methodology s.4): estimated payments less items returned unpaid "
        "(a re-presented item that paid is kept), plus payments misapplied to another year and transferred in, at the "
        "time the original payment arrived. Overpayments credited from TY2024 returns are not receipts.",
        "Each receipt counts at the first instalment whose due date (11:59:59 pm Central) it arrives by; ledger times are "
        "UTC. The June instalment fell due on Monday 16 June 2025. Instalment 4 also takes later receipts through January.",
        "Withholding is state income tax withheld on employers' wage statements, electronic and paper (capture "
        "vendor) channels together.",
        "Net capital gain is the amount carried to federal AGI, on each return's version of record (its latest "
        "accepted version in the amended-returns log).",
        "Payments and wage statements are placed by the TIN as reported, or through a resolved TIN match case; "
        "open cases stay unplaced. A household's records are those of its filers, joint spouses and filing "
        "dependents.",
        "Share of tier AGI is net capital gain over the tier's household federal AGI, rounded once to one decimal.",
    ]
    for i, txt in enumerate(notes):
        c = note(ws, 9 + i, txt)
        ws.merge_cells(start_row=9 + i, start_column=1, end_row=9 + i, end_column=10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[9 + i].height = 26
    ws.freeze_panes = "B4"
    ws.page_setup.orientation = "landscape"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_area = "A1:J14"

    # ---- Notes
    ws = wb.create_sheet("Notes")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 96
    put(ws, 1, 1, "Notes", bold=True, size=12)
    rows = [
        ("Prepared by", f"{OFFICE}, 9 November 2026"),
        ("Data", "Department of Revenue TY2025 research extract delivered 23 October 2026; TY2022 to TY2024 extracts "
                 "in the same layout."),
        ("Household unit", "Methodology s.2 draws tiers on full-year resident household units. The unit used here "
                           "joins a spouse's separate state return to its partner's on the federal primary TIN and "
                           "attaches each filing dependent's own return to the household whose return claims it; it is "
                           "the construction that reproduces every published cell (methodology s.3)."),
        ("Not used", "Returns Processed by AGI Class (all filers, return grain) and the federal-filing-unit basis "
                     "the Legislative Fiscal Office tiers on; neither reproduces the published tables."),
        ("Residency", "Full-year residents only (residency code 1); part-year residents and nonresidents are outside "
                      "the base."),
        ("Base", "Every household unit counts whatever its AGI, zero and negative AGI included (methodology s.2)."),
        ("Rounding", "Floors to the nearest $1,000; dollar amounts whole; share to one decimal place."),
    ]
    for i, (a, b) in enumerate(rows):
        put(ws, 3 + i, 1, a, bold=True, size=9)
        c = put(ws, 3 + i, 2, b, size=9)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[3 + i].height = 40 if len(b) > 110 else 14

    for s in wb.worksheets:
        s.sheet_properties.pageSetUpPr.fitToPage = True
        s.page_setup.fitToWidth = 1
        s.page_setup.fitToHeight = 0
        s.page_margins = PageMargins(left=0.5, right=0.5, top=0.6, bottom=0.6)
        s.oddFooter.left.text = OFFICE
        s.oddFooter.right.text = "Page &P of &N"
    wb.properties.creator = OFFICE
    wb.properties.lastModifiedBy = "Stephanie Reid"
    wb.properties.title = "Income tax tier schedule, tax year 2025"
    wb.properties.created = PREPARED
    wb.properties.modified = PREPARED
    wb.save(path)


# --------------------------------------------------------------------------------------------- chart
SURF = "#fcfcfb"
TXT = "#0b0b0b"
TXT2 = "#52514e"
GRID = "#e4e2dc"
CURVE = "#2a78d6"
BANDS = {3: "#86b6ef", 2: "#3987e5", 1: "#1c5cab"}   # ordinal ramp, validated light


def money_tick(x, _pos=None):
    if x >= 1e6:
        v = x / 1e6
        return f"${v:,.0f}M" if v == int(v) else f"${v:,.1f}M"
    return f"${x / 1e3:,.0f}K"


def write_chart(path, agi_desc, floors, share, n_units):
    plt.rcParams.update({"font.family": "Liberation Sans", "font.size": 9})
    count = np.arange(1, len(agi_desc) + 1)
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=150)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    top = agi_desc[0] * 1.15
    edges = {3: (floors[0], floors[1]), 2: (floors[1], floors[2]), 1: (floors[2], top)}
    for t, (lo, hi) in edges.items():
        ax.axvspan(lo, hi, color=BANDS[t], alpha=0.16, lw=0, zorder=0)
    ax.step(agi_desc, count, where="post", color=CURVE, lw=2, zorder=3)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(100_000, top)
    ax.set_ylim(0.8, count[-1] * 1.6)
    ax.xaxis.set_major_locator(FixedLocator([1e5, 2e5, 5e5, 1e6, 2e6, 5e6, 1e7, 2e7, 5e7]))
    ax.xaxis.set_major_formatter(FuncFormatter(money_tick))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_major_locator(FixedLocator([1, 10, 100, 1_000, 10_000, 100_000]))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _p: f"{y:,.0f}"))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, which="major", color=GRID, lw=0.6, zorder=1)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#9a988f")
    ax.tick_params(colors=TXT2, length=3)
    ax.set_xlabel("Household federal AGI, tax year 2025 (log scale)", color=TXT2)
    ax.set_ylabel("Household units with AGI at or above this level (log scale)", color=TXT2)

    # floor values sit above the plot, off their lines, so no label crosses the curve or a neighbour
    xa = ax.get_xaxis_transform()
    marks = ((floors[0], "Top 10%", "right", 1 / 1.03), (floors[1], "Top 5%", "left", 1.03),
             (floors[2], "Top 1%", "left", 1.03))
    for f, lab, ha, nudge in marks:
        ax.axvline(f, color=TXT, lw=1.1, ls=(0, (4, 3)), zorder=4)
        ax.text(f * nudge, 1.015, f"{lab}  ${f:,}", transform=xa, ha=ha, va="bottom", color=TXT,
                fontsize=9.5, fontweight="bold", clip_on=False)
    # each tier's band carries its capital-gain share of tier AGI
    for t, (lo, hi) in edges.items():
        xc = math.sqrt(lo * (floors[2] * 4 if t == 1 else hi))
        ax.text(xc, 1.6, f"Tier {t}\ngain {share[t]:.1f}%", ha="center", va="bottom",
                color=TXT, fontsize=8.5, zorder=5, linespacing=1.25)
    fig.suptitle(f"TY2025 tier floors: ${floors[0]:,} / ${floors[1]:,} / ${floors[2]:,}",
                 x=0.07, ha="left", y=0.965, fontsize=14, fontweight="bold", color=TXT)
    fig.text(0.07, 0.885, f"Household units at or above each AGI, {n_units:,} full-year resident household units. Band "
                          "labels: net capital gain as a share of the tier's household federal AGI.",
             color=TXT2, fontsize=9.5, ha="left")
    fig.text(0.07, 0.018, "Source: Department of Revenue research extract TY2025 (processed returns, dependents "
                           "schedule, Schedule D, amended-returns log). Office of Revenue Research, 9 November 2026.",
             color=TXT2, fontsize=7.5, ha="left")
    fig.subplots_adjust(left=0.075, right=0.975, top=0.81, bottom=0.115)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=SURF, metadata={"Software": None})
    plt.close(fig)
    path.write_bytes(buf.getvalue())


# --------------------------------------------------------------------------------------------- container
def repack(path, when):
    """Pin the OOXML zip entry times and core dates so a rebuild is byte-identical."""
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = {i.filename: z.read(i.filename) for i in infos}
    iso = when.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    data["docProps/core.xml"] = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*", rb"\g<1>" + iso,
                                       data["docProps/core.xml"])
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=when.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data[i.filename])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    load(con)

    corpus = []
    for y, label, measure, pub, key in read_tables():
        corpus.append((y, label, measure, pub, key, rebuild(con, y, key)))
    hits = sum(1 for c in corpus if c[3] == c[5])

    n_units, sched = schedule(con)
    floors = tuple(s[3] for s in sched)
    tier_rows = tiers(con, floors)
    due = due_dates()
    rec = receipts(con, due)
    gain = capital_gain(con)
    wh = withholding(con)
    share = {t: round(100.0 * gain[t] / tier_rows[t][1], 1) for t in (1, 2, 3)}

    # control totals against the build record
    assert floors == RECORD["floors"], floors
    assert n_units == RECORD["units"] and hits == RECORD["hits"] == len(corpus), (n_units, hits, len(corpus))
    for t in (1, 2, 3):
        assert tuple(rec[(t, k)] for k in (1, 2, 3, 4)) == RECORD["receipts"][t], (t, rec)
        assert wh[t] == RECORD["withholding"][t] and gain[t] == RECORD["gain"][t], t
        assert share[t] == RECORD["share"][t], share
        assert tier_rows[t][0] == {1: sched[2][1], 2: sched[1][1] - sched[2][1], 3: sched[0][1] - sched[1][1]}[t]

    xlsx = OUT / "tier_schedule.xlsx"
    png = OUT / "tier_floors.png"
    write_workbook(xlsx, n_units, sched, corpus, hits, tier_rows, rec, gain, wh, share, due)
    write_chart(png, survival(con), floors, share, n_units)

    # the writing libraries' names out of docProps, the Office's own in
    subprocess.run([sys.executable, str(SCRUB), str(OUT), "--apply", "--producer", OFFICE, "--stamp", "2026-11-09"],
                   capture_output=True, text=True)
    repack(xlsx, PREPARED)
    audit = subprocess.run([sys.executable, str(SCRUB), str(OUT), "--floor", "2026-10-23", "--ceiling", "2026-11-09"],
                           capture_output=True, text=True)
    assert audit.returncode == 0, audit.stdout + audit.stderr
    ts = PREPARED.timestamp()
    for p in (xlsx, png):
        os.utime(p, (ts, ts))

    # read the workbook back: every graded cell as written
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    assert [wb["Schedule"].cell(9 + i, 3).value for i in range(3)] == list(floors)
    tb = wb["Tier base 2025"]
    for i, t in enumerate((1, 2, 3)):
        assert [tb.cell(4 + i, c).value for c in range(4, 11)] == \
            [rec[(t, 1)], rec[(t, 2)], rec[(t, 3)], rec[(t, 4)], wh[t], gain[t], share[t]]

    print(f"SCHEDULE  ${floors[0]:,} / ${floors[1]:,} / ${floors[2]:,}  (top 10 / 5 / 1 per cent)")
    for p, k, agi, f in sched:
        print(f"  top {p:>2}%  k = {k:>6,}  k-th household AGI ${agi:,}  floor ${f:,}")
    print(f"HOUSEHOLD UNITS  {n_units:,}")
    print(f"REPRODUCTION  {hits} of {len(corpus)} published cells")
    print("TIER BASE (whole dollars)")
    for t in (1, 2, 3):
        print(f"  tier {t}: units {tier_rows[t][0]:,}  AGI ${tier_rows[t][1]:,}")
        print("    receipts " + "  ".join(f"i{k} ${rec[(t, k)]:,}" for k in (1, 2, 3, 4)))
        print(f"    withholding ${wh[t]:,}  net capital gain ${gain[t]:,}  share {share[t]:.1f}%")
    print("due dates " + ", ".join(d.isoformat() for d in due))
    print(f"wrote {xlsx.name}, {png.name} to {OUT}")


if __name__ == "__main__":
    main()
