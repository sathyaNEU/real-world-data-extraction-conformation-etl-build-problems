"""The filter's 2025/26 runs (on the 2023/24 screen's cells), the batches sent to Fernhollow, their
acknowledgements and examination, Fernhollow's invoices, and the golden answers to the three 2025/26
tables. Every figure here is computed from the payment records and the run mechanics."""
import datetime as dt
import random
from collections import Counter, defaultdict

import params as PR
import screen as S
from world import DEPT_ORDER

FY0, FY1 = PR.FY["2025/26"]
LATE_FILE_PAYDATE = dt.date(2026, 2, 3)          # the creditor file submitted after January's scheduled run
RERUN_MONTH = (2025, 10)


def run_month_of(payday):
    f = PR.wd_before(payday, 2)
    return (f.year, f.month), f


def build_runs(world, cells):
    """Run log rows and the batches. cells: the department-cells the runs applied."""
    rng = random.Random(PR.SEED * 11 + 3)
    inrange = defaultdict(Counter)     # (run_key) -> dept -> screened
    routed = defaultdict(Counter)      # (run_key) -> (dept, cell) -> routed
    for p in world.pay:
        g = p[6] + p[7]
        if not 100000 <= g <= 99999999:
            continue
        (y, m), f = run_month_of(p[5])
        if not (FY0 <= f <= FY1):
            continue
        key = ((y, m), "S1" if p[5] == LATE_FILE_PAYDATE else "01")
        inrange[key][p[0]] += 1
        c = S.cell_p(g)
        if (p[0], c) in cells:
            routed[key][(p[0], c)] += 1
    runs = []
    for (y, m) in PR.months(FY0, FY1):
        last = PR.last_wd(y, m)
        runs.append(dict(key=((y, m), "01"), ref="DF-%02d%02d-01" % (y % 100, m), month="%d-%02d" % (y, m),
                         type="Scheduled", done=dt.datetime(last.year, last.month, last.day, 17, rng.randint(36, 58))))
        if (y, m) == RERUN_MONTH:
            nd = dt.date(2025, 11, 3)
            runs.append(dict(key=((y, m), "01"), ref="DF-2510-02", month="2025-10", type="Re-run",
                             done=dt.datetime(nd.year, nd.month, nd.day, 10, 42)))
        if (y, m) == (2026, 1):
            runs.append(dict(key=((y, m), "S1"), ref="DF-2601-S1", month="2026-01", type="Supplementary",
                             done=dt.datetime(2026, 2, 2, 9, 18)))
    rows, batches = [], []
    for r in runs:
        tag = r["ref"][3:]
        for d in DEPT_ORDER:
            dc = sorted(c for (dd, c) in cells if dd == d)
            n_in = inrange[r["key"]][d]
            tot = sum(routed[r["key"]][(d, c)] for c in dc)
            bref = ("WCC-%s-%s" % (tag, d)) if tot else ""
            if dc:
                for c in dc:
                    rows.append(dict(run_ref=r["ref"], run_month=r["month"], run_type=r["type"],
                                     run_completed=r["done"].strftime("%Y-%m-%d %H:%M"), department=d,
                                     payments_in_range=n_in, flagged_cell=c,
                                     payments_routed=routed[r["key"]][(d, c)], batch_ref=bref))
            else:
                rows.append(dict(run_ref=r["ref"], run_month=r["month"], run_type=r["type"],
                                 run_completed=r["done"].strftime("%Y-%m-%d %H:%M"), department=d,
                                 payments_in_range=n_in, flagged_cell="", payments_routed=0, batch_ref=""))
            if tot:
                batches.append(dict(batch_ref=bref, run_ref=r["ref"], run_month=r["month"], run_type=r["type"],
                                    sent=r["done"] + dt.timedelta(minutes=rng.randint(9, 31)), dept=d, n=tot))
    return runs, rows, batches


def wd_after(d, k):
    while k:
        d += dt.timedelta(days=1)
        if PR.is_wd(d):
            k -= 1
    return d


def examine(batches):
    """Acknowledgement and examination of each batch. A batch from a run that was re-run is withdrawn."""
    rng = random.Random(PR.SEED * 13 + 5)
    acks = []
    for b in batches:
        sent = b["sent"]
        ackd = wd_after(sent.date(), 1)
        withdrawn = b["run_ref"] == "DF-2510-01"
        ret = 0 if withdrawn else sum(1 for _ in range(b["n"]) if rng.random() < 0.012)
        ex = 0 if withdrawn else b["n"] - ret
        span = 4 + int(b["n"] / 14) + rng.randint(0, 3)
        done = None if withdrawn else wd_after(ackd, span)
        acks.append(dict(batch_ref=b["batch_ref"], received=sent.strftime("%Y-%m-%dT%H:%M:00"),
                         acknowledged=ackd.isoformat(), payments_received=b["n"],
                         returned_unexamined=ret, payments_examined=ex,
                         examination_completed=done.isoformat() if done else None,
                         status="withdrawn" if withdrawn else "examined",
                         _run_month=b["run_month"], _dept=b["dept"]))
    return acks


def charged_qty(a):
    return 0 if a["payments_examined"] == 0 else max(a["payments_examined"], PR.MIN_BATCH)


def invoices(acks):
    """Monthly invoices for batches whose examination completed in the month; one invoice credited and
    reissued. Returns rows in issue order."""
    by_month = defaultdict(list)
    for a in acks:
        if a["status"] != "examined":
            continue
        d = dt.date.fromisoformat(a["examination_completed"])
        by_month[(d.year, d.month)].append(a)
    rows = []
    seq = 40117
    for (y, m) in sorted(by_month):
        issue = PR.last_wd(y, m)
        lines = sorted(by_month[(y, m)], key=lambda a: a["batch_ref"])
        rate = PR.BASE_2526      # the card in force when each batch was received (all 2025/26 batches)
        seq += 1
        no = "FA%06d" % seq
        if (y, m) == (2025, 12):
            # issued with one line duplicated, credited in full and reissued
            bad = lines + [lines[1]]
            for a in bad:
                rows.append(_line(no, issue, "Invoice", a, rate, 1))
            seq += 1
            cn = "FC%06d" % seq
            cdate = PR.wd_before(dt.date(2026, 1, 16), 0) if PR.is_wd(dt.date(2026, 1, 16)) else issue
            for a in bad:
                rows.append(_line(cn, cdate, "Credit note", a, rate, -1, credits=no))
            seq += 1
            no2 = "FA%06d" % seq
            for a in lines:
                rows.append(_line(no2, cdate, "Invoice", a, rate, 1, replaces=no))
        else:
            for a in lines:
                rows.append(_line(no, issue, "Invoice", a, rate, 1))
    return rows


def _line(no, issue, kind, a, rate, sign, credits="", replaces=""):
    q = sign * charged_qty(a)
    net = round(q * rate, 2)
    vat = round(net * 0.2, 2)
    return dict(document_no=no, document_type=kind, issue_date=issue.isoformat(), batch_ref=a["batch_ref"],
                description="Post-payment examination", quantity=q, unit_rate="%.2f" % rate,
                net_amount="%.2f" % net, vat_amount="%.2f" % vat, related_document=credits or replaces)


# ---------------------------------------------------------------------------------------- golden asks
def b1_routed(rows):
    """Routed payments by run month: a re-run replaces the run it repeats; a supplementary run adds."""
    out = Counter()
    reran = {r["run_month"] for r in rows if r["run_type"] == "Re-run"}
    for r in rows:
        if r["run_type"] == "Scheduled" and r["run_month"] in reran:
            continue
        out[r["run_month"]] += int(r["payments_routed"])
    return out


def b2_examined(acks):
    out = Counter()
    for a in acks:
        out[a["_run_month"]] += a["payments_examined"]
    return out


def quarter_of(month):
    y, m = map(int, month.split("-"))
    return {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[m]


def c_quarters(acks, alloc=None, rate=PR.BASE_2526, qty=charged_qty, qmap=None):
    alloc = alloc or {1: PR.ALLOC_ORIG, 2: PR.ALLOC_ORIG, 3: PR.ALLOC_VARIED, 4: PR.ALLOC_VARIED}
    ch = Counter()
    for a in acks:
        q = qmap(a) if qmap else quarter_of(a["_run_month"])
        if q:
            ch[q] += qty(a)
    prem = {q: max(0, ch[q] - alloc[q]) for q in (1, 2, 3, 4)}
    unused = {q: max(0, alloc[q] - ch[q]) for q in (1, 2, 3, 4)}
    charge = {q: unused[q] * PR.UNUSED_SHARE * rate for q in (1, 2, 3, 4)}
    return ch, prem, unused, charge
