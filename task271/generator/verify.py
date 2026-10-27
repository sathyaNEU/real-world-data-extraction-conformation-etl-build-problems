"""task271 independent verifier: recomputes every graded figure from target/ with the standard library and openpyxl
only (no pandas, none of calc.py), then compares with generator/figures.json.

    python3 task271/generator/verify.py task271/target"""
from __future__ import annotations

import bisect
import collections
import csv
import datetime as dt
import json
import math
import os
import sys
from zoneinfo import ZoneInfo

import openpyxl

LON = ZoneInfo("Europe/London")
UTC = dt.timezone.utc
NAMES = {"XWEX": "Wexcombe Stock Exchange", "AWKL": "Ardenwick MTF lit book", "DLVL": "Delvenne MTF lit book",
         "AWKM": "Ardenwick MTF midpoint book", "DLVM": "Delvenne Midpoint", "THGD": "Thursgate MTF midpoint book",
         "BDSI": "Brindock Securities SI", "QTSI": "Quintrell Markets SI"}


def half_up(x, nd=0):
    q = x * 10 ** nd
    return math.floor(q + 0.5) / 10 ** nd


def call(t):
    busted = set()
    with open(os.path.join(t, "ashlowe_execution_report_2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["exec_type"] == "BUST":
                busted.add(r["ref_exec_id"])
    wb = openpyxl.load_workbook(os.path.join(t, "pemberwick_execution_report_2026.xlsx"), read_only=True)
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        head = list(next(it))
        si, oi = head.index("Status"), head.index("Orig Exec Ref")
        for r in it:
            if r[si] == "Busted":
                busted.add(r[oi])
    seen = set()
    rows = []
    with open(os.path.join(t, "hessenby_tca_executions_2026-01-02_to_2026-10-30.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["broker_exec_id"] in seen:
                continue
            seen.add(r["broker_exec_id"])
            ts = dt.datetime.strptime(r["exec_time_utc"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC).timestamp()
            rows.append((r["isin"], ts, r))
    by = collections.defaultdict(list)
    for isin, ts, r in rows:
        by[isin].append(ts)
    for k in by:
        by[k].sort()
    sums = collections.defaultdict(float)
    cnt = collections.Counter()
    n_read = 0
    for isin, ts, r in rows:
        if r["session"] != "CONT" or not r["mid_plus_60s"] or r["broker_exec_id"] in busted:
            continue
        n_read += 1
        L = by[isin]
        j = bisect.bisect_right(L, ts)
        if j < len(L) and L[j] <= ts + 60:
            continue
        m0, m1 = float(r["mid_at_exec"]), float(r["mid_plus_60s"])
        s = 1.0 if r["side"] == "BUY" else -1.0
        v = "THGD" if r["last_mkt"] in ("THGD", "THGM") else r["last_mkt"]
        sums[v] += -s * (m1 - m0) / m0 * 1e4
        cnt[v] += 1
    est = {v: sums[v] / cnt[v] for v in NAMES}
    return est, cnt, n_read


def notes(t):
    out = []
    with open(os.path.join(t, "gresmere_contract_notes_settling_2026-01-02_to_2026-11-03.csv"), encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["note_status"] != "CANCELLED"]
    key = collections.Counter((r["client_order_ref"], r["trade_date"], r["trade_time"], r["shares"], r["side"])
                              for r in rows)
    for r in rows:
        d = dt.datetime.strptime(r["trade_date"], "%d/%m/%Y").date()
        k = (r["client_order_ref"], r["trade_date"], r["trade_time"], r["shares"], r["side"])
        if key[k] > 1 and r["note_ref"].startswith("CN26-") and d < dt.date(2026, 7, 1):
            continue
        out.append((d, r))
    return out


def ask_b(t):
    tot = collections.defaultdict(int)          # pence, exact
    for d, r in notes(t):
        if dt.date(2026, 1, 1) <= d <= dt.date(2026, 10, 30):
            gross = round(int(r["shares"]) * float(r["price_gbx"]))   # pence to the penny
            tot[(d.month, r["side"])] += gross
    return {k: v / 100.0 / 1e6 for k, v in tot.items()}


def ask_a(t):
    closed = set()
    with open(os.path.join(t, "uk_trading_calendar_2025-12-01_to_2027-01-31.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["uk_market"] == "CLOSED":
                closed.add(dt.date.fromisoformat(r["date"]))
    sh = collections.defaultdict(int)
    in_2026 = set()
    for d, r in notes(t):
        sh[r["client_order_ref"]] += int(r["shares"])
        if dt.date(2026, 1, 1) <= d <= dt.date(2026, 10, 30):
            in_2026.add(r["client_order_ref"])
    adv = {}
    with open(os.path.join(t, "securities_master_2026-10-30.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            adv[r["isin"]] = float(r["adv_shares_2026"])
    ca = json.load(open(os.path.join(t, "corporate_actions_2026.json")))
    cons = [(e["new_isin"], dt.date.fromisoformat(e["ex_date"])) for e in ca["events"] if e["event_type"] == "CONSOLIDATION"]
    net = collections.defaultdict(int)
    cuts = [9 * 60 + 15, 11 * 60 + 45, 14 * 60 + 15]
    with open(os.path.join(t, "wealth_platform_client_orders_2025-12-29_to_2026-10-30.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["client_order_ref"] not in in_2026:
                continue
            loc = dt.datetime.strptime(r["placed_at"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC).astimezone(LON)
            d, mins = loc.date(), loc.hour * 60 + loc.minute + loc.second / 60.0
            point = None
            if d not in closed:
                for i, c in enumerate(cuts):
                    if mins < c:
                        point = i
                        break
            if point is None:
                d += dt.timedelta(days=1)
                while d in closed:
                    d += dt.timedelta(days=1)
                point = 0
            q = sh[r["client_order_ref"]]
            net[(d, point, r["isin"])] += q if r["side"] == "BUY" else -q
    counts = collections.Counter()
    sizes = collections.defaultdict(list)
    for (d, p, isin), q in net.items():
        if q == 0:
            continue
        counts[p] += 1
        pct = abs(q) / adv[isin] * 100.0
        for ni, eff in cons:
            if isin == ni and d < eff:
                pct /= 10.0
        sizes[p].append(pct)
    return counts, {k: sum(v) / len(v) for k, v in sizes.items()}


def main(t):
    fig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    ans = fig["answers"]
    diffs = []
    est, cnt, n_read = call(t)
    for v, nm in NAMES.items():
        w = int(half_up(est[v]))
        if ans["adverse_move_bp"][nm] != w:
            diffs.append(("adverse move %s" % nm, ans["adverse_move_bp"][nm], w))
        if ans["fills_read_by_venue"][nm] != format(cnt[v], ","):
            diffs.append(("fills read %s" % nm, ans["fills_read_by_venue"][nm], cnt[v]))
    off = [NAMES[v] for v in NAMES if est[v] > 1.5]
    if sorted(off) != sorted(fig["call"]["kept_off"]):
        diffs.append(("kept off", fig["call"]["kept_off"], off))
    if fig["steps"]["fills_read"] != format(n_read, ","):
        diffs.append(("fills read", fig["steps"]["fills_read"], n_read))
    counts, sizes = ask_a(t)
    pts = ["09:30", "12:00", "14:30"]
    for i, pn in enumerate(pts):
        if ans["market_orders"][pn] != format(counts[i], ","):
            diffs.append(("market orders %s" % pn, ans["market_orders"][pn], counts[i]))
        got = "%.3f" % half_up(sizes[i], 3)
        if ans["mean_size_pct_adv"][pn] != got:
            diffs.append(("size %s" % pn, ans["mean_size_pct_adv"][pn], got))
    b = ask_b(t)
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]
    for m in range(1, 11):
        got = "%.2f" % half_up((b.get((m, "BUY"), 0) - b.get((m, "SELL"), 0)), 2)
        if ans["net_bought_gbp_m"][months[m - 1]] != got:
            diffs.append(("net %s" % months[m - 1], ans["net_bought_gbp_m"][months[m - 1]], got))
    n = 8 * 2 + 2 + 3 + 3 + 10
    print("verify: %d figures, %d differ" % (n, len(diffs)))
    for d in diffs:
        print("  DIFF", d)
    print("PASS" if not diffs else "FAIL")
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")))
