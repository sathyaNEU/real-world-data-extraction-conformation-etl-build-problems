"""The three supplemental asks, all on FY25, which is outside the call's window.

Each carries one primary device plus shared hazards, and no device row falls inside FY26 P1 to P9, which
`checks.py` asserts by count. The devices are silent: the hygiene battery reconciles past all three, and
only a cross-file or cross-grain cut nothing invites exposes them.

Ask 1  the payables accrual reconciliation. A restatement is posted in a later period without reversing the
       first, so one source document carries an accrual under two refs and a naive sum double counts it.
Ask 2  the till takings reconciliation. The EPOS interface uploads a branch's trading day to the ledger on
       the next working day, and two days after a public holiday, so the voucher's posting date is not the
       trading date and a join on date moves the last trading day of each quarter into the next one.
Ask 3  the monitoring coverage. Evaluation drains down over three periods before a re-platforming, the run
       log's completion flag is true for partial runs, and one unit's first period was extracted partially.
"""
import csv
import datetime as dt

import numpy as np

import ledger as L
import world as W

ACCRUALS = "payables_accruals_fy25.csv"
AP_CONTROL = "payables_control_account_fy25.csv"
SUPPLIERS = "supplier_register.csv"
TILLS = "epos_till_takings_fy25.csv"
SALES_CONTROL = "sales_control_account_fy25.csv"
RUN_LOG = "monitoring_run_log_fy25.csv"

# Ask 3: the posting streams the ruleset covers. Single supplier invoices below the authorisation
# threshold are not monitored, and neither is payroll, so the in-scope population is not every entry.
MONITORED = ("EPOS", "ROUTE_DOCKET", "ROUTE_VAN", "AP_BATCH", "MANUAL")
REPLATFORM = (8, 9, 10)          # periods over which evaluation drains before the platform change
PARTIAL_UNIT = "DPG-320"         # the unit whose first period came through partially

IE_HOLIDAYS_FY25 = tuple(dt.date(*d) for d in (
    (2024, 10, 28), (2024, 12, 25), (2024, 12, 26), (2025, 1, 1), (2025, 2, 3),
    (2025, 3, 17), (2025, 4, 21), (2025, 5, 5), (2025, 6, 2), (2025, 8, 4)))


def _former(code):
    """FY25 artifacts carry the unit code in force before the FY26 half-year renumbering. Idempotent, so
    it is safe wherever a code may already be in its former form."""
    cur = W.resolve_unit(code)
    return next(u[1] for u in W.UNITS if u[0] == cur)


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)
    return len(rows)


# ---------------------------------------------------------------- ask 1

def accruals(sim):
    """The purchase ledger's open supplier accruals at the FY25 close.

    A restatement supersedes an earlier accrual without reversing it, so the superseded row is still in the
    listing and a naive sum counts the same obligation twice. Some chains are three long, so matching one
    restatement to one original over-corrects.
    """
    rng = np.random.default_rng(L.SEED + 601)
    sup = suppliers()
    rows = []
    n = 0
    for code, _o, _nm, kind, _c in W.UNITS:
        base = {"branch": 300, "contracts": 240, "bakery": 180, "services": 140}[kind]
        for _ in range(int(rng.integers(base - 25, base + 25))):
            n += 1
            pno = int(rng.integers(1, 13))
            pstart, pend = next((a, b) for p, a, b in W.FY25_PERIODS if p == pno)
            rows.append(dict(ref="AC25-%06d" % n, unit_code=code, period=pno,
                             day=pstart + dt.timedelta(days=int(rng.integers(0, (pend - pstart).days + 1))),
                             supplier=sup[int(rng.integers(0, len(sup)))][0],
                             amount=round(float(rng.uniform(140.0, 24_000.0)), 2),
                             restates="", posted_to=code))
    # the device: restatement chains, the superseded row left in the listing
    base_rows = list(rows)
    idx = rng.choice(len(base_rows), size=int(len(base_rows) * 0.085), replace=False)
    for i in sorted(idx):
        prev = base_rows[int(i)]
        for _step in range(2 if rng.random() < 0.26 else 1):
            n += 1
            later = min(prev["period"] + int(rng.integers(1, 3)), 12)
            pstart, pend = next((a, b) for p, a, b in W.FY25_PERIODS if p == later)
            rows.append(dict(ref="AC25-%06d" % n, unit_code=prev["unit_code"], period=later,
                             day=pstart + dt.timedelta(days=int(rng.integers(0, (pend - pstart).days + 1))),
                             supplier=prev["supplier"],
                             amount=round(prev["amount"] * float(rng.uniform(0.55, 1.45)), 2),
                             restates=prev["ref"], posted_to=prev["unit_code"]))
            prev = rows[-1]
    # a hazard: a few accruals the ledger posted to another unit, which nets to zero at group level
    for r in rng.choice(len(rows), size=46, replace=False):
        row = rows[int(r)]
        other = [u[0] for u in W.UNITS if u[0] != row["unit_code"]]
        row["posted_to"] = other[int(rng.integers(0, len(other)))]
    rows.sort(key=lambda r: (r["unit_code"], r["ref"]))
    return rows


def suppliers():
    rng = np.random.default_rng(L.SEED + 607)
    stems = ("Ardkeen", "Ballyroan", "Carrowmore", "Dromahair", "Emlagh", "Fintra", "Glasheen",
             "Headford", "Inchicore", "Kilbarry", "Lisnagry", "Moyvane", "Newtown", "Oughterard",
             "Portumna", "Rathduff", "Skenakilla", "Tullyvin", "Urlingford", "Whitegate")
    tails = ("Dairies", "Produce", "Meats", "Bakery Supplies", "Packaging", "Beverages",
             "Chilled Foods", "Dry Goods", "Frozen", "Cleaning Supplies")
    out = []
    for i in range(96):
        out.append(("SUP-%04d" % (1000 + i), "%s %s" % (stems[i % len(stems)],
                                                        tails[(i // len(stems) + i) % len(tails)]),
                    ("30 days", "45 days", "60 days", "on receipt")[int(rng.integers(0, 4))]))
    return out


def superseded(rows):
    """The refs a later accrual restates. Those rows are superseded and must not be summed."""
    return {r["restates"] for r in rows if r["restates"]}


def accrual_balance(rows, by="unit_code"):
    """The correct closing balance: chain-latest amounts only, grouped by `by`.

    `unit_code` is the unit the accrual belongs to, which is what the subledger listing is by.
    `posted_to` is the unit the ledger posted it to, which is what the control account is by. The two
    differ on the mispostings, which is the second reconciling item and nets to zero at group level.
    """
    dead = superseded(rows)
    out = {}
    for r in rows:
        if r["ref"] in dead:
            continue
        out[r[by]] = out.get(r[by], 0.0) + r["amount"]
    return {k: round(v, 2) for k, v in out.items()}


def ap_control(rows):
    """The ledger's purchase-ledger control account per unit: the accrual the ledger carries, plus goods
    received not yet invoiced, which the subledger does not hold and which is the reconciling item."""
    bal = accrual_balance(rows, by="posted_to")
    rng = np.random.default_rng(L.SEED + 613)
    out = []
    for code, _o, _nm, _k, _c in W.UNITS:
        grni = round(float(rng.uniform(14_000.0, 96_000.0)), 2)
        a = bal.get(code, 0.0)
        out.append((code, round(a, 2), grni, round(a + grni, 2)))
    return out


def write_accruals(path, rows):
    return _w(path, ["accrual_ref", "unit_code", "fiscal_period", "accrual_date", "supplier_code",
                     "accrual_eur", "restates_ref", "posted_to_unit"],
              [(r["ref"], _former(r["unit_code"]), r["period"], r["day"].isoformat(), r["supplier"],
                "%.2f" % r["amount"], r["restates"], _former(r["posted_to"])) for r in rows])


def write_ap_control(path, rows):
    return _w(path, ["unit_code", "accrual_per_ledger_eur", "goods_received_not_invoiced_eur",
                     "control_account_eur"],
              [(_former(u), "%.2f" % a, "%.2f" % g, "%.2f" % t) for u, a, g, t in rows])


def write_suppliers(path):
    return _w(path, ["supplier_code", "supplier_name", "payment_terms"], suppliers())


# ---------------------------------------------------------------- ask 2

def _upload_date(trading_day):
    """The EPOS interface uploads a trading day on the next working day, two days after a holiday."""
    d = trading_day + dt.timedelta(days=1)
    while d.weekday() == 6 or d in IE_HOLIDAYS_FY25:
        d += dt.timedelta(days=1)
    if trading_day in IE_HOLIDAYS_FY25 or (trading_day + dt.timedelta(days=1)) in IE_HOLIDAYS_FY25:
        d += dt.timedelta(days=1)
        while d.weekday() == 6:
            d += dt.timedelta(days=1)
    return d


def tills(sim):
    """Branch till takings for FY25, by branch, till and trading day."""
    rng = np.random.default_rng(L.SEED + 619)
    rows = []
    for code in W.BRANCHES:
        n_tills = int(rng.integers(3, 7))
        for pno, pstart, pend in W.FY25_PERIODS:
            days = [pstart + dt.timedelta(days=d) for d in range((pend - pstart).days + 1)]
            for day in [d for d in days if d.weekday() < 6]:
                for t in range(1, n_tills + 1):
                    txns = int(rng.integers(90, 420))
                    val = round(txns * float(rng.uniform(21.0, 58.0)), 2)
                    rows.append((code, "T%d" % t, day.isoformat(), _upload_date(day).isoformat(),
                                 txns, "%.2f" % val))
    return rows


def write_tills(path, rows):
    return _w(path, ["unit_code", "till_id", "business_date", "transactions", "takings_eur"],
              [(_former(u), t, b, n, v) for u, t, b, _up, n, v in rows])


def sales_control(till_rows):
    """The ledger's sales control account by unit and FY25 period, which the EPOS interface posts by its
    own upload date, not by the trading date."""
    agg = {}
    for u, _t, _b, up, _n, v in till_rows:
        d = dt.date.fromisoformat(up)
        p = W.period_of(d, W.FY25_PERIODS)
        if p is None:
            continue
        agg[(u, p)] = agg.get((u, p), 0.0) + float(v)
    return [(_former(u), p, "%.2f" % round(val, 2)) for (u, p), val in sorted(agg.items())]


def write_sales_control(path, rows):
    return _w(path, ["unit_code", "fiscal_period", "epos_sales_posted_eur"], rows)


# ---------------------------------------------------------------- ask 3

def run_log(table25):
    """The platform's nightly run log for FY25: what each run presented and what it evaluated."""
    rng = np.random.default_rng(L.SEED + 631)
    in_scope = {}
    for r in table25:
        if r["stream"] in MONITORED:
            key = (r["unit_code"], r["period"])
            in_scope[key] = in_scope.get(key, 0) + 1
    rows = []
    for (u, p), n in sorted(in_scope.items()):
        # every period leaves a residue: entries posted after the nightly cut-off are picked up by the
        # next run only if they are still in the window, and some never are
        share = 1.0 - float(rng.uniform(0.006, 0.028))
        if p in REPLATFORM:
            share = {8: 0.82, 9: 0.61, 10: 0.44}[p]
        if u == PARTIAL_UNIT and p == 1:
            share = min(share, 0.68)
        evaluated = int(round(n * share))
        runs = 28 if p in (3, 6, 9, 12) else 24
        # the device: the run completed every night, partial or not, so the flag never shows the shortfall
        rows.append((u, p, runs, evaluated, "Y",
                     int(rng.integers(140, 420)), round(float(rng.uniform(0.4, 3.1)), 2)))
    return rows


def write_run_log(path, rows):
    """What the platform ran and what it evaluated. The in-scope population is not in this file: it comes
    from the ledger, filtered to the interfaces the ruleset covers."""
    return _w(path, ["unit_code", "fiscal_period", "runs_completed", "entries_evaluated",
                     "run_completed_all_nights", "rules_version_changes", "mean_run_hours"],
              [(_former(u), p, r, e, c, v, h) for u, p, r, e, c, v, h in rows])
