"""Recompute every figure from the shipped bundle alone, on its own code path.

Reads target/ and generator/figures.json. Imports nothing from the generator.
    python3 verify.py [target_dir] [figures.json]
"""
import csv
import datetime as dt
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
MIRROR_HI = 11000
GRAIN = 50
BAND_LO, BAND_HI = 9000.0, 10000.0
THRESHOLD = 10000.0
YEAR_LO, YEAR_HI = dt.date(2026, 7, 1), dt.date(2027, 6, 30)
DST_LO, DST_HI = dt.date(2026, 9, 27), dt.date(2027, 4, 4)
FAILS = []
N = [0]


def chk(label, got, want, tol=0):
    N[0] += 1
    good = (abs(got - want) <= tol) if isinstance(want, (int, float)) and \
        isinstance(got, (int, float)) else got == want
    if not good:
        FAILS.append("%s: got %r want %r" % (label, got, want))
    return good


def rows(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def xlsx_rows(path, sheet=0):
    from openpyxl import load_workbook
    wb = load_workbook(path, data_only=True)
    ws = wb[wb.sheetnames[sheet]]
    return [[c.value for c in r] for r in ws.iter_rows()]


def local_date(ts):
    u = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    off = 13 if DST_LO <= u.date() < DST_HI else 12
    return (u + dt.timedelta(hours=off)).date()


def load(target):
    """Every physical cash deposit of the reporting year, with its customer's segment."""
    # the register: master number to segment
    reg = xlsx_rows(os.path.join(target, "business_customer_register.xlsx"))
    head = None
    seg = {}
    for r in reg:
        if r and r[0] == "master_customer_no":
            head = {v: i for i, v in enumerate(r) if v}
            continue
        if head and r and r[0]:
            seg[r[head["master_customer_no"]]] = r[head["segment_name"]]
    cross = {r["acct_customer_no"]: r["master_customer_no"]
             for r in rows(target, "customer_number_crosswalk.csv")}
    out = []
    reversed_refs = set()
    for r in rows(target, "cash_deposit_counter_2026_2027.csv"):
        if r["reversal_of"]:
            reversed_refs.add(r["reversal_of"])
            reversed_refs.add(r["deposit_ref"])
    for r in rows(target, "cash_deposit_counter_2026_2027.csv"):
        if r["instrument"] != "cash" or r["deposit_ref"] in reversed_refs:
            continue
        day = dt.date(*[int(v) for v in r["deposit_date"].split("-")])
        out.append((seg[cross[r["acct_customer_no"]]], float(r["amount_nzd"]), day))
    seen = set()
    for r in rows(target, "cash_deposit_machine_2026_2027.csv"):
        if r["machine_deposit_ref"] in seen:
            continue
        seen.add(r["machine_deposit_ref"])
        out.append((seg[cross[r["acct_customer_no"]]], float(r["amount_nzd"]),
                    local_date(r["deposit_ts_utc"])))
    return out, seg, cross


def _bins(amounts, lo, hi, step):
    n = int((hi - lo) // step)
    out = [0] * n
    for a in amounts:
        if lo <= a < hi:
            out[int((a - lo) // step)] += 1
    return out


def _line(xs, ys, w=None):
    w = w or [1.0] * len(xs)
    sw = sum(w)
    mx = sum(wi * x for wi, x in zip(w, xs)) / sw
    my = sum(wi * y for wi, y in zip(w, ys)) / sw
    sxy = sum(wi * (x - mx) * (y - my) for wi, x, y in zip(w, xs, ys))
    sxx = sum(wi * (x - mx) ** 2 for wi, x in zip(w, xs))
    k = sxy / sxx
    return k, my - k * mx


def _poly(xs, ys, w, order):
    m = order + 1
    A = [[sum(w[i] * xs[i] ** (r + c) for i in range(len(xs))) for c in range(m)]
         for r in range(m)]
    bb = [sum(w[i] * ys[i] * xs[i] ** r for i in range(len(xs))) for r in range(m)]
    for c in range(m):
        piv = max(range(c, m), key=lambda r: abs(A[r][c]))
        A[c], A[piv] = A[piv], A[c]
        bb[c], bb[piv] = bb[piv], bb[c]
        if abs(A[c][c]) < 1e-14:
            return None
        for r in range(c + 1, m):
            f = A[r][c] / A[c][c]
            for cc in range(c, m):
                A[r][cc] -= f * A[c][cc]
            bb[r] -= f * bb[c]
    q = [0.0] * m
    for r in range(m - 1, -1, -1):
        q[r] = (bb[r] - sum(A[r][c] * q[c] for c in range(r + 1, m))) / A[r][r]
    return q


def _fit(xs, ys, family, order):
    if family == "ols":
        p = _poly(xs, ys, [1.0] * len(xs), order)
        return (lambda x: sum(p[j] * x ** j for j in range(order + 1))) if p else None
    if family == "log_ols":
        p = _poly(xs, [math.log(max(y, 0.5)) for y in ys], [1.0] * len(xs), order)
        return (lambda x: math.exp(sum(p[j] * x ** j for j in range(order + 1)))) if p else None
    p = [0.0] * (order + 1)
    p[0] = math.log(max(sum(ys) / float(len(ys)), 1e-9))
    for _ in range(60):
        mu = [math.exp(min(30.0, sum(p[j] * x ** j for j in range(order + 1)))) for x in xs]
        z = [sum(p[j] * x ** j for j in range(order + 1)) + (y - m) / max(m, 1e-9)
             for x, y, m in zip(xs, ys, mu)]
        q = _poly(xs, z, mu, order)
        if q is None:
            return None
        done = max(abs(q[j] - p[j]) for j in range(order + 1)) < 1e-11
        p = q
        if done:
            break
    return lambda x: math.exp(min(30.0, sum(p[j] * x ** j for j in range(order + 1))))


def sides(amounts, lo=5000, hi=16000, step=250, family="poisson", order=1):
    """The band's surplus and the deficit 10,000 to 11,000 carries, from one fit."""
    b = _bins(amounts, lo, hi, step)
    n = len(b)
    out = [k for k in range(n) if BAND_LO <= lo + k * step < MIRROR_HI]
    rest = [k for k in range(n) if k not in out]
    if any(b[k] == 0 for k in rest):
        return None
    keep = [k for k in rest if b[k] > 0]
    if len(keep) < order + 3:
        return None
    low = [k for k in range(n) if BAND_LO <= lo + k * step < BAND_HI]
    mir = [k for k in range(n) if BAND_HI <= lo + k * step < MIRROR_HI]
    if not low or not mir:
        return None
    f = _fit([(lo + k * step) / 1000.0 for k in keep], [float(b[k]) for k in keep], family, order)
    if f is None:
        return None
    pl = sum(f((lo + k * step) / 1000.0) for k in low)
    pm = sum(f((lo + k * step) / 1000.0) for k in mir)
    if not (0 < pl < 1e7 and 0 < pm < 1e7):
        return None
    return (sum(b[k] for k in low) - pl, pm - sum(b[k] for k in mir))


def figure(amounts, lo=5000, hi=16000, step=250, family="poisson", order=1):
    s = sides(amounts, lo, hi, step, family, order)
    return None if s is None else (s[0] + s[1]) / 2.0


def r50(x):
    return int(math.floor(x / float(GRAIN) + 0.5) * GRAIN)


def main(target, figpath):
    fig = json.load(open(figpath, encoding="utf-8"))
    dep, seg, cross = load(target)
    win = [d for d in dep if YEAR_LO <= d[2] <= YEAR_HI]

    by_seg = {}
    for s, a, day in win:
        by_seg.setdefault(s, []).append(a)

    # the figure
    per = {s: r50(figure(v)) for s, v in by_seg.items()}
    want = fig["critical_components"]["segment_deposits_split"]
    for s in sorted(want):
        chk("segment %s" % s, per.get(s), want[s])
    chk("the bank's figure", sum(per.values()), fig["call"]["deposits_split"])
    chk("the largest segment", max(per, key=lambda s: (per[s], s)),
        fig["call"]["largest_segment"])
    chk("the largest segment's figure", per[fig["call"]["largest_segment"]],
        fig["call"]["largest_segment_deposits_split"])

    # the deposits paid in
    paid = {s: len(v) for s, v in by_seg.items()}
    for s, v in fig["critical_components"]["segment_cash_deposits_paid_in"].items():
        chk("deposits paid in %s" % s, paid.get(s), v)
    chk("deposits paid in total", sum(paid.values()),
        fig["critical_components"]["cash_deposits_paid_in_total"])

    # the band as observed
    band = {s: sum(1 for a in v if BAND_LO <= a < BAND_HI) for s, v in by_seg.items()}
    chk("band deposits observed", sum(band.values()),
        fig["critical_components"]["band_deposits_observed"])
    for s, v in fig["critical_components"]["band_deposits_observed_by_segment"].items():
        chk("band observed %s" % s, band.get(s), v)

    # the steps on the ladder, rebuilt from the bundle
    days = {}
    for r in rows(target, "cash_deposit_counter_2026_2027.csv"):
        if r["instrument"] != "cash" or r["reversal_of"]:
            continue
        day = dt.date(*[int(v) for v in r["deposit_date"].split("-")])
        if not (YEAR_LO <= day <= YEAR_HI):
            continue
        days.setdefault((cross[r["acct_customer_no"]], day), []).append(float(r["amount_nzd"]))
    seen = set()
    for r in rows(target, "cash_deposit_machine_2026_2027.csv"):
        if r["machine_deposit_ref"] in seen:
            continue
        seen.add(r["machine_deposit_ref"])
        day = local_date(r["deposit_ts_utc"])
        if not (YEAR_LO <= day <= YEAR_HI):
            continue
        days.setdefault((cross[r["acct_customer_no"]], day), []).append(float(r["amount_nzd"]))
    screen = 0
    for (cust, day), a in days.items():
        if len(a) >= 2 and sum(a) >= THRESHOLD and any(x < THRESHOLD for x in a):
            screen += sum(1 for x in a if BAND_LO <= x < BAND_HI)
    chk("the same-day screen", screen, fig["steps"]["same_day_screen"])
    chk("the near-threshold band counted", sum(band.values()),
        fig["steps"]["near_threshold_band_counted"])
    chk("the band read on its own",
        sum(r50(sides(v)[0]) for s, v in by_seg.items()),
        fig["steps"]["band_read_on_its_own"])
    mirror = {s: sum(1 for a in v if BAND_HI <= a < MIRROR_HI) for s, v in by_seg.items()}
    chk("deposits in 10,000 to 11,000", sum(mirror.values()),
        fig["steps"]["mirror_deposits_observed"])

    # convergence over the determinism judge's own candidate set, with the record's balance
    # deciding which specifications stand: the dollars moved, so the surplus below and the
    # deficit above are the same number, and a specification whose two sides disagree is out
    seen, kept, grid = set(), 0, 0
    for lo, hi in ((5000, 16000), (6000, 14000), (7000, 13000), (8000, 12000), (5000, 20000)):
        for step in (50, 100, 200, 250, 500):
            for fam in ("poisson", "ols", "log_ols"):
                for order in (1, 2, 3):
                    grid += 1
                    ss = [sides(v, lo, hi, step, fam, order) for s, v in sorted(by_seg.items())]
                    if any(x is None for x in ss):
                        continue
                    below = sum(x[0] for x in ss)
                    above = sum(x[1] for x in ss)
                    if abs(below - above) > 0.20 * max(abs(below), abs(above), 1.0):
                        continue
                    kept += 1
                    got = tuple(r50((x[0] + x[1]) / 2.0) for x in ss)
                    seen.add(got)
                    chk("convergence %d-%d/%d/%s/o%d" % (lo, hi, step, fam, order), sum(got),
                        fig["call"]["deposits_split"])
    chk("the judge's grid is the candidate set", grid, fig["steps"]["specifications_in_the_grid"])
    chk("the specifications the record leaves standing", kept,
        fig["steps"]["specifications_the_record_leaves"])
    chk("one set of segment figures across every one of them", len(seen), 1)

    # the deliverables
    wb = xlsx_rows(os.path.join(TASK, "golden", "structured_cash_deposits_2027.xlsx"))
    flat = [r for r in wb if r and r[0]]
    gotrows = {r[0]: [r[1], r[2]] for r in flat if r[0] in per}
    for s, v in fig["deliverables"]["structured_cash_deposits_2027.xlsx"]["rows"].items():
        chk("workbook row %s" % s, gotrows.get(s), v)
    tot = [r for r in flat if r[0] == "Total"]
    chk("workbook total", tot[0][2] if tot else None,
        fig["deliverables"]["structured_cash_deposits_2027.xlsx"]["deposits_split_total"])

    # the asks
    tol = {}
    for r in xlsx_rows(os.path.join(target, "cash_tolerance_register.xlsx")):
        if r and r[0] and r[0] not in ("effective_from",) and isinstance(r[2], (int, float)):
            tol[r[0]] = float(r[2])
    quarters = [("2026Q3", dt.date(2026, 7, 1), dt.date(2026, 9, 30)),
                ("2026Q4", dt.date(2026, 10, 1), dt.date(2026, 12, 31)),
                ("2027Q1", dt.date(2027, 1, 1), dt.date(2027, 3, 31)),
                ("2027Q2", dt.date(2027, 4, 1), dt.date(2027, 6, 30))]
    agg = {q: [0, 0, 0.0] for q, _, _ in quarters}
    for r in rows(target, "till_balance_log_2026_2027.csv"):
        ts = r["session_opened_ts"]
        day = local_date(ts) if ts.endswith("Z") else dt.date(*[int(v) for v in ts[:10].split("-")])
        v = float(r["variance_nzd"])
        for q, lo, hi in quarters:
            if lo <= day <= hi:
                t = 25.0 if day < dt.date(2027, 1, 1) else 15.0
                agg[q][0] += 1
                agg[q][1] += 1 if abs(v) > t else 0
                agg[q][2] += v
    for q, v in fig["asks"]["till_sessions_by_quarter"].items():
        chk("A1 %s sessions" % q, agg[q][0], v[0])
        chk("A1 %s over tolerance" % q, agg[q][1], v[1])
        chk("A1 %s net variance" % q, round(agg[q][2], 2), v[2], tol=0.005)

    svc = rows(target, "machine_service_log_2027.csv")
    per_month = {}
    for r in svc:
        mo = r["reported_ts"][:7]
        per_month[mo] = per_month.get(mo, 0) + int(r["out_of_service_minutes"])
    for mo, v in fig["asks"]["machine_hours_by_month"].items():
        chk("A3 %s hours" % mo, round(per_month.get(mo, 0) / 60.0, 1), v, tol=0.051)

    print("verify: %d checks, %d failed" % (N[0], len(FAILS)))
    for f in FAILS[:30]:
        print("  FAIL", f)
    return 1 if FAILS else 0


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    f = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "figures.json")
    sys.exit(main(t, f))
