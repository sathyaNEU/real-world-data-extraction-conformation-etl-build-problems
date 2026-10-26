"""Writing the pack: the ledger extract as a SQLite database, the exception register and the reference files.

The ledger extract carries FY26 P1 to P9 at the entry, which is what the question is about, plus the line
detail of a stratified sample of vouchers, which is what an auditor pulls to see how a voucher is made up.
FY25 ships as a period summary, which is how a comparative year reaches an extract.
"""
import csv
import datetime as dt
import os
import sqlite3
import zlib

import numpy as np

import ledger as L
import world as W

GL_DB = "drumcondra_gl_fy26.sqlite"
EXCEPTIONS = "monitoring_exceptions_fy26.csv"
FY25_SUMMARY = "gl_period_summary_fy25.csv"
UNIT_REGISTER = "trading_unit_register.csv"
CALENDAR = "period_calendar.csv"
ACCOUNTS = "chart_of_accounts.csv"
MANIFEST = "extract_manifest.txt"

# a stratified voucher sample: how many vouchers of each posting-count band carry their full line detail
LINE_SAMPLE = ((1, 1, 500), (2, 9, 400), (10, 99, 300), (100, 999, 60), (1000, 10 ** 9, 12))


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)
    return len(rows)


def write_gl(path, table, lines_period=9):
    """The extract: journal_entries for FY26 P1 to P9, journal_lines for the sampled vouchers."""
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    con.execute("""CREATE TABLE journal_entries (
        entry_no INTEGER PRIMARY KEY, voucher_ref TEXT NOT NULL, unit_code TEXT NOT NULL,
        fiscal_year TEXT NOT NULL, fiscal_period INTEGER NOT NULL, posting_date TEXT NOT NULL,
        source_interface TEXT NOT NULL, item_count INTEGER NOT NULL, line_count INTEGER NOT NULL,
        debit_total REAL NOT NULL, credit_total REAL NOT NULL,
        entered_by TEXT NOT NULL, released_by TEXT NOT NULL)""")
    con.execute("""CREATE TABLE journal_lines (
        entry_no INTEGER NOT NULL, line_no INTEGER NOT NULL, account_code TEXT NOT NULL,
        source_doc_ref TEXT NOT NULL, debit REAL NOT NULL, credit REAL NOT NULL,
        PRIMARY KEY (entry_no, line_no))""")
    con.executemany("INSERT INTO journal_entries VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    [(r["entry_no"], r["voucher_ref"], r["unit_code"], "FY26", r["period"],
                      r["day"].isoformat(), r["source_interface"] if "source_interface" in r
                      else r["interface"], r["items"], r["lines"], r["amount"], r["amount"],
                      r["entered_by"], r["released_by"]) for r in table])
    con.executemany("INSERT INTO journal_lines VALUES (?,?,?,?,?,?)",
                    line_rows(table, lines_period))
    con.execute("CREATE INDEX ix_entries_unit ON journal_entries (unit_code, fiscal_period)")
    con.execute("CREATE INDEX ix_lines_entry ON journal_lines (entry_no)")
    con.commit()
    n_e = con.execute("SELECT count(*) FROM journal_entries").fetchone()[0]
    n_l = con.execute("SELECT count(*) FROM journal_lines").fetchone()[0]
    con.close()
    return n_e, n_l


def sampled_entries(table, period):
    """The stratified voucher sample whose line detail ships, drawn inside one closed period."""
    rng = np.random.default_rng(L.SEED + 409)
    pool = [r for r in table if r["period"] == period]
    picked = []
    for lo, hi, want in LINE_SAMPLE:
        band = [r for r in pool if lo <= r["items"] <= hi]
        if not band:
            continue
        take = min(want, len(band))
        idx = rng.choice(len(band), size=take, replace=False)
        picked += [band[int(i)] for i in sorted(idx)]
    picked.sort(key=lambda r: r["entry_no"])
    return picked


def line_rows(table, period):
    """Every ledger line of each sampled voucher. One source document posts its own balanced set of lines,
    so counting distinct source_doc_ref on an entry reproduces its item_count."""
    rng = np.random.default_rng(L.SEED + 503)
    cost = [a for a, _n, k in W.ACCOUNTS if k in ("cost", "revenue")]
    ctrl = [a for a, _n, k in W.ACCOUNTS if k == "control"]
    out = []
    for r in sampled_entries(table, period):
        per_doc = max(r["lines"] // r["items"], 2)
        line_no = 0
        for d in range(r["items"]):
            doc = "%s/%06d/%04d" % (r["source_interface"][:3] if "source_interface" in r
                                    else r["interface"][:3], r["entry_no"], d + 1)
            val = round(float(r["amount"]) / r["items"], 2)
            split = max(per_doc - 1, 1)
            part = round(val / split, 2)
            for j in range(split):
                line_no += 1
                amt = part if j < split - 1 else round(val - part * (split - 1), 2)
                out.append((r["entry_no"], line_no, cost[int(rng.integers(0, len(cost)))], doc, amt, 0.0))
            line_no += 1
            out.append((r["entry_no"], line_no, ctrl[int(rng.integers(0, len(ctrl)))], doc, 0.0, val))
    return out


def write_exceptions(path, reg):
    """The platform's output: one row per flagged journal entry, with the rules that fired on it."""
    return _w(path, ["exception_id", "entry_no", "voucher_ref", "unit_code", "raised_at_utc",
                     "rules_fired", "rule_count"],
              [(r["exception_id"], r["entry_no"], r["voucher_ref"], r["unit_code"],
                dt.datetime.combine(r["day"], dt.time(2, 15)).isoformat(timespec="seconds") + "Z",
                r["rules"], r["n_rules"]) for r in reg])


def write_unit_register(path):
    rows = []
    for code, old, name, kind, county in W.UNITS:
        rows.append((code, name, kind, county, old, W.RENUMBER_DATE.isoformat(),
                     "code_to in force from this date; code_from in force before it"))
    return _w(path, ["unit_code", "unit_name", "unit_kind", "county", "former_unit_code",
                     "code_effective_from", "note"], rows)


def write_calendar(path):
    rows = []
    for label, pers in (("FY25", W.FY25_PERIODS), ("FY26", W.FY26_PERIODS)):
        for n, a, b in pers:
            rows.append((label, n, a.isoformat(), b.isoformat(), (b - a).days + 1,
                         W.PERIOD_WEEKS[n - 1]))
    return _w(path, ["fiscal_year", "fiscal_period", "period_start", "period_end", "days", "weeks"], rows)


def write_accounts(path):
    return _w(path, ["account_code", "account_name", "account_type"],
              [(a, n, k) for a, n, k in W.ACCOUNTS])


def write_fy25_summary(path, table25):
    """FY25 as a period summary: how a comparative year reaches an extract."""
    agg = {}
    for r in table25:
        key = (r["unit_code"], r["period"], r["stream"])
        a = agg.setdefault(key, [0, 0, 0.0])
        a[0] += 1
        a[1] += r["items"]
        a[2] += r["amount"]
    rows = [(u, p, i, n, items, round(val, 2)) for (u, p, i), (n, items, val) in sorted(agg.items())]
    return _w(path, ["unit_code", "fiscal_period", "posting_stream", "entries", "postings",
                     "value_eur"], rows)


def write_manifest(path, counts):
    lines = [
        "DRUMCONDRA PROVISIONS GROUP",
        "General ledger and continuous monitoring extract",
        "",
        "Extract date          : %s" % W.EXTRACT_DATE.isoformat(),
        "Financial year        : FY26, which runs %s to %s" % (
            W.FY26_START.isoformat(), (W.FY26_PERIODS[-1][2]).isoformat()),
        "Periods closed        : P1 to P%d, P%d closed %s" % (
            W.GRADED_PERIODS, W.GRADED_PERIODS, W.FY26_PERIODS[W.GRADED_PERIODS - 1][2].isoformat()),
        "Periods still to run  : P%d to P12" % (W.GRADED_PERIODS + 1),
        "Currency              : %s" % W.CURRENCY,
        "",
        "Scope of this extract",
        "  Journal entries for FY26 P1 to P%d, every trading unit, every posting interface." % W.GRADED_PERIODS,
        "  Entries posted after the extract date are not included.",
        "  Ledger line detail for a stratified sample of P%d vouchers, drawn across posting-count" % W.GRADED_PERIODS,
        "  bands so that each band is represented. Line detail for every voucher is held in the",
        "  ledger and is not extracted; its volume is some five and a half million lines a year.",
        "  FY25 is summarised by unit, period and interface. FY25 line and entry detail is archived.",
        "",
        "Row counts",
    ]
    for k, v in counts.items():
        lines.append("  %-34s %12s" % (k, "{:,}".format(v)))
    lines += ["", "Prepared by Group Finance Systems for Group Internal Audit."]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return len(lines)


FUEL = "fleet_fuel_card_transactions_fy26.csv"
STOCK = "branch_stock_count_variances_fy26.csv"


def write_fuel(path):
    """A distractor: fuel card spend by vehicle. Relevant to the group's expense controls and to the audit
    plan's scoping, and read by nothing in the solution."""
    rng = np.random.default_rng(L.SEED + 701)
    rows = []
    for code in W.BRANCHES + ("DPG-510",):
        for v in range(1, int(rng.integers(9, 22))):
            reg = "%02d-%s-%d" % (int(rng.integers(21, 27)),
                                  ("D", "C", "G", "L", "W", "MO")[int(rng.integers(0, 6))],
                                  int(rng.integers(1000, 99999)))
            for p in range(1, W.GRADED_PERIODS + 1):
                litres = round(float(rng.uniform(380.0, 1_650.0)), 1)
                rows.append((code, reg, p, int(rng.integers(4, 19)), litres,
                             "%.2f" % round(litres * float(rng.uniform(1.52, 1.79)), 2)))
    return _w(path, ["unit_code", "vehicle_reg", "fiscal_period", "fills", "litres", "spend_eur"], rows)


def write_stock(path):
    """A distractor: branch stock count variances. Relevant to where the audit plan puts effort, and read
    by nothing in the solution."""
    rng = np.random.default_rng(L.SEED + 709)
    rows = []
    for code in W.BRANCHES:
        for p in range(1, W.GRADED_PERIODS + 1):
            for cat in ("ambient", "chilled", "frozen", "non-food"):
                counted = int(rng.integers(1_200, 9_400))
                var = round(float(rng.normal(0.0, counted * 0.004)), 2)
                rows.append((code, p, cat, counted, "%.2f" % var,
                             "%.3f" % round(100.0 * var / counted, 3)))
    return _w(path, ["unit_code", "fiscal_period", "stock_category", "lines_counted",
                     "variance_eur", "variance_pct"], rows)
