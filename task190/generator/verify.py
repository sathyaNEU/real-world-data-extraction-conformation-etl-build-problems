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


def excess(amounts, lo=5000, hi=16000, bw=250):
    n = (hi - lo) // bw
    bins = [0] * n
    for a in amounts:
        if lo <= a < hi:
            bins[int((a - lo) // bw)] += 1
    band = [k for k in range(n) if BAND_LO <= lo + k * bw < BAND_HI]
    keep = [k for k in range(n) if k not in band and bins[k] > 0]
    xs = [float(k) for k in keep]
    ys = [math.log(bins[k]) for k in keep]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sl = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    ic = my - sl * mx
    pred = sum(math.exp(ic + sl * k) for k in band)
    return sum(bins[k] for k in band) - pred


def r10(x):
    return int(math.floor(x / 10.0 + 0.5) * 10)


def main(target, figpath):
    fig = json.load(open(figpath, encoding="utf-8"))
    dep, seg, cross = load(target)
    win = [d for d in dep if YEAR_LO <= d[2] <= YEAR_HI]

    by_seg = {}
    for s, a, day in win:
        by_seg.setdefault(s, []).append(a)

    # the figure
    per = {s: r10(excess(v)) for s, v in by_seg.items()}
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
        if len(a) >= 2 and all(x < THRESHOLD for x in a) and sum(a) >= THRESHOLD:
            screen += sum(1 for x in a if BAND_LO <= x < BAND_HI)
    chk("the same-day screen", screen, fig["steps"]["same_day_screen"])
    chk("one profile for the book", r10(excess([a for s, a, d in win])),
        fig["steps"]["one_profile_for_the_book"])

    # convergence: every accepted estimator gives the same segment figures
    for lo, hi, bw in ((5000, 16000, 250), (5000, 16000, 500), (6000, 14000, 250),
                       (5500, 15000, 250), (5000, 15000, 250), (5000, 14000, 500)):
        for s, v in by_seg.items():
            chk("convergence %s %d-%d/%d" % (s, lo, hi, bw), r10(excess(v, lo, hi, bw)), per[s])

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
