"""The golden solve: reads only ../target/ and computes every graded figure.

    python3 golden.py           prints the slate and the ask figures
    python3 golden.py --write   also writes ../golden/inspection_slate_2027-28.docx and dga_fleet_review.csv

Everything is parameterised so checks.py can run each rung, grid cell and ask stop on the same bytes.
"""
import csv
import datetime as dt
import math
import os
import re
import sys
from functools import lru_cache
from zoneinfo import ZoneInfo

import numpy as np
import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W        # noqa: E402
import standard as S     # noqa: E402

TARGET = os.path.join(HERE, "..", "target")
GOLDEN = os.path.join(HERE, "..", "golden")
NZ = ZoneInfo("Pacific/Auckland")


def tp(prefix):
    return os.path.join(TARGET, next(f for f in sorted(os.listdir(TARGET)) if f.startswith(prefix)))


# ---------------------------------------------------------------------------------------------
# loaders
@lru_cache(None)
def main_rows():
    out = []
    with open(tp("dga_main_tank_results")) as fh:
        for r in csv.DictReader(fh):
            r = dict(r)
            r["sampled"] = dt.datetime.strptime(r["sampled"], "%Y-%m-%d %H:%M")
            r["date"] = dt.date.fromisoformat(r["date"])
            out.append(r)
    return tuple(out)


@lru_cache(None)
def register():
    wb = openpyxl.load_workbook(tp("asset_register"), read_only=True, data_only=True)
    rows = list(wb["Transformers"].iter_rows(values_only=True))
    hdr = rows[0]
    return {r[0]: dict(zip(hdr, r)) for r in rows[1:] if r[0]}


@lru_cache(None)
def counters():
    df = pd.read_csv(tp("scada_tap_counters"), dtype={"transformer_id": str})
    out = {}
    for tid, g in df.groupby("transformer_id", sort=True):
        days = [dt.date.fromisoformat(x) for x in g["date"]]
        out[tid] = (days, g["tap_ops_counter"].to_numpy(dtype=np.int64))
    return out


@lru_cache(None)
def maintenance_log():
    wb = openpyxl.load_workbook(tp("maintenance_log"), read_only=True, data_only=True)
    rows = list(wb.worksheets[0].iter_rows(values_only=True))
    hdr = rows[0]
    out = []
    for r in rows[1:]:
        if not r[0]:
            continue
        d = dict(zip(hdr, r))
        d["completed"] = d["completed"].date() if isinstance(d["completed"], dt.datetime) else d["completed"]
        out.append(d)
    return tuple(out)


REPLACED = re.compile(r"counter replaced|new counter|replaced the operations counter|op counter replaced",
                      re.I)


@lru_cache(None)
def _services_log():
    return services_raw("log")


def services(source="log"):
    if source == "log":
        return _services_log()
    return services_raw(source)


def services_raw(source="log"):
    """Last tap-changer service per unit, and the dates on which a counter was replaced."""
    last, repl = {}, {}
    for e in maintenance_log():
        if e["work_type"] not in ("OLTC SERVICE", "OLTC INSPECTION"):
            continue
        tid = e["asset"]
        d = e["completed"]
        if tid not in last or d > last[tid]:
            last[tid] = d
        if REPLACED.search(e["description"]) and "not replaced" not in e["description"].lower():
            repl.setdefault(tid, set()).add(d)
    if source == "register":
        reg = register()
        last = {tid: (reg[tid]["oltc_last_service"].date() if isinstance(reg[tid]["oltc_last_service"], dt.datetime)
                      else reg[tid]["oltc_last_service"]) for tid in reg}
    return last, repl


def log_counter_reading(tid, d):
    for e in maintenance_log():
        if e["asset"] == tid and e["completed"] == d and e["work_type"] == "OLTC SERVICE":
            m = re.search(r"Op counter ([\d,]+), not replaced", e["description"])
            if m:
                return int(m.group(1).replace(",", ""))
    return None


@lru_cache(None)
def top_oil():
    df = pd.read_parquet(tp("scada_top_oil"))
    ts = df["timestamp"].to_numpy(dtype="datetime64[s]")
    t0 = ts.min()
    out = {}
    for tid, g in df.groupby("transformer_id", sort=True):
        h = ((g["timestamp"].to_numpy(dtype="datetime64[s]") - t0) // np.timedelta64(1, "h")).astype(int)
        arr = np.full(h.max() + 1, np.nan)
        arr[h] = g["top_oil_c"].to_numpy()
        out[tid] = arr
    return t0.astype(dt.datetime), out


# ---------------------------------------------------------------------------------------------
# main call
def ops_between(tid, d1, d2):
    """Operations between 00:00 on d1 and 00:00 on d2: a drop is a rollover unless the log says the
    counter was replaced that day."""
    days, c = counters()[tid]
    i, j = days.index(d1), days.index(d2)
    repl = services("log")[1].get(tid, set())
    total = 0
    for k in range(i, j):
        a, b = int(c[k]), int(c[k + 1])
        total += (b - a) if b >= a else (b if days[k] in repl else b + W.COUNTER_MODULUS - a)
    return total


def signatures(rows=None, bdl="half", window="first_detectable", gap=W.BASE_GAP_DAYS):
    """Per unit with any detectable main-tank acetylene: tap-changer type, tracking r (raw and per
    day) of acetylene increments on tap operations, and the twelve-month C2H2/H2 increase ratio."""
    rows = rows or main_rows()
    units = S.by_unit(S.record_of_issue(rows))
    reg = register()
    out = {}
    for tid in W.IDS:
        ss = units[tid]
        det = [k for k, r in enumerate(ss) if not str(r["C2H2"]).startswith("<")]
        inc12, _, _ = S.increases(ss, bdl, gap)
        cls = S.preservation(ss)
        if len(det) < 4 or inc12["C2H2"] <= W.A3[cls]["C2H2"]:
            continue          # acetylene not rising: nothing to attribute
        first = det[0]
        a = first if window == "first_detectable" else max(0, first - 1)
        seg = ss[a:]
        days = [r["sampled"].date() for r in seg]
        lv = np.array([S.value(r["C2H2"], bdl) for r in seg])
        o = np.array([ops_between(tid, x, y) for x, y in zip(days[:-1], days[1:])], float)
        dd = np.array([(y - x).days for x, y in zip(days[:-1], days[1:])], float)
        inc = np.diff(lv)
        r_raw = float(np.corrcoef(inc, o)[0, 1]) if inc.std() > 0 else 0.0
        r_day = float(np.corrcoef(inc / dd, o / dd)[0, 1]) if inc.std() > 0 else 0.0
        # cumulative growth: level since onset against cumulative operations and against elapsed days
        cum_o = np.concatenate([[0], np.cumsum(o)])
        el = np.array([(x - days[0]).days for x in days], float)
        res_o = np.polyfit(cum_o, lv, 1, full=True)[1]
        res_t = np.polyfit(el, lv, 1, full=True)[1]
        res_o = float(res_o[0]) if len(res_o) else 0.0
        res_t = float(res_t[0]) if len(res_t) else 0.0
        h2 = inc12["H2"]
        ratio = inc12["C2H2"] / h2 if h2 > 0 else float("inf")
        out[tid] = {"type": reg[tid]["oltc_type"], "r": r_raw, "r_day": r_day, "ratio": ratio,
                    "cum_ops_better": res_o < 0.5 * res_t, "n": len(inc)}
    return out


def attribute(sig, rule=("type", "tracking", "ratio"), r_min=0.9, ratio_min=3.0, need=None, tracking="raw"):
    """Units whose main-tank acetylene is attributed to the tap changer under a rule. need: how many of
    the named signatures must hold (default all of them)."""
    out = []
    for tid, s in sig.items():
        checks = []
        for k in rule:
            if k == "type":
                checks.append(s["type"] == "In-oil arcing")
            elif k == "tracking":
                if tracking == "raw":
                    checks.append(s["r"] >= r_min)
                elif tracking == "day":
                    checks.append(s["r_day"] >= r_min)
                else:
                    checks.append(s["cum_ops_better"])
            elif k == "ratio":
                checks.append(s["ratio"] >= ratio_min)
        n = len(checks) if need is None else need
        if sum(checks) >= n:
            out.append(tid)
    return sorted(out)


def solve_main(excl_units=None, **kw):
    excl = {t: ("C2H2",) for t in (excl_units or [])}
    coded = S.fleet(list(main_rows()), excl=excl, **kw)
    top, c3 = S.slate(coded)
    return top, coded


def answer():
    sig = signatures()
    att = attribute(sig)
    top, coded = solve_main(att)
    return top, coded, att, sig


# ---------------------------------------------------------------------------------------------
# ask A: tap operations since the last service, in-oil tap changers
def ops_since(tid, d0, repl_dates, drops="log", start="service_day"):
    days, c = counters()[tid]
    i0 = days.index(d0) if start == "service_day" else days.index(d0 + dt.timedelta(1))
    total = 0
    for k in range(i0, len(days) - 1):
        a, b = int(c[k]), int(c[k + 1])
        if b >= a:
            total += b - a
            continue
        replaced_that_day = days[k] in repl_dates
        if drops == "all_rollover":
            replaced_that_day = False
        elif drops == "all_reset":
            replaced_that_day = True
        total += b if replaced_that_day else b + W.COUNTER_MODULUS - a
    return total


def ask_a(source="log", drops="log", start="service_day"):
    reg = register()
    last, repl = services("log")
    if source == "register":
        last, _ = services("register")
    out = {}
    latest_day = counters()[W.IDS[0]][0][-1]
    for tid in sorted(reg):
        if reg[tid]["oltc_type"] != "In-oil arcing":
            continue
        d0 = last[tid]
        days, c = counters()[tid]
        if d0 < days[0]:
            base = log_counter_reading(tid, d0)
            n = (int(c[0]) - base) % W.COUNTER_MODULUS + ops_since(tid, days[0], repl.get(tid, set()), drops,
                                                                   "service_day")
        else:
            n = ops_since(tid, d0, repl.get(tid, set()), drops, start)
        seven = dt.date(d0.year + 7, d0.month, d0.day)
        past = n > 60_000 or latest_day > seven
        out[tid] = {"last_service": d0, "ops": n, "past": past}
    return out


# ---------------------------------------------------------------------------------------------
# ask B: relative saturation at the latest sample
def ws(T):
    return 10 ** (7.42 - 1670.0 / (T + 273.0))


def scada_temp(tid, local_dt, tz="nz"):
    t0, arr = top_oil()
    hour = local_dt.replace(minute=0, second=0, microsecond=0)
    if tz == "nz":
        u = hour.replace(tzinfo=NZ).astimezone(dt.timezone.utc).replace(tzinfo=None)
    elif tz == "none":
        u = hour
    elif tz == "fixed12":
        u = hour - dt.timedelta(hours=12)
    elif tz == "fixed13":
        u = hour - dt.timedelta(hours=13)
    k = int((u - t0).total_seconds() // 3600)
    return float(arr[tid][k])


def ask_b(tz="nz", when="sampled", reissue="latest"):
    rows = list(main_rows())
    if reissue == "latest":
        rows = S.record_of_issue(rows)
    else:
        first = {}
        for r in rows:
            if r["sample_id"] not in first or int(r["issue"]) < int(first[r["sample_id"]]["issue"]):
                first[r["sample_id"]] = r
        rows = list(first.values())
    units = S.by_unit(rows)
    out = {}
    for tid in W.IDS:
        r = units[tid][-1]
        if r["oil_temp_c"] not in ("", None):
            T, basis = float(r["oil_temp_c"]), "label"
        else:
            t = r["sampled"]
            if when == "analysis":
                t = dt.datetime.combine(r["date"], t.time())
            T, basis = scada_temp(tid, t, tz), "scada"
        rs = float(r["moisture_ppm"]) / ws(T) * 100
        out[tid] = {"rs": rs, "T": T, "basis": basis, "sampled": r["sampled"], "moisture": float(r["moisture_ppm"])}
    return out


# ---------------------------------------------------------------------------------------------
def latest_c2h2():
    units = S.by_unit(S.record_of_issue(list(main_rows())))
    return {tid: S.value(units[tid][-1]["C2H2"]) for tid in W.IDS}


def solve():
    top, coded, att, sig = answer()
    naive_top, naive = solve_main([])
    a = ask_a()
    b = ask_b()
    return {"slate": top, "coded": coded, "attributed": att, "signatures": sig, "ask_a": a, "ask_b": b,
            "naive": naive, "naive_slate": naive_top, "latest_c2h2": latest_c2h2()}


def main():
    g = solve()
    print("slate", g["slate"])
    print("attributed", g["attributed"])
    for tid in W.IDS:
        c, s, gas, _ = g["coded"][tid]
        a = g["ask_a"].get(tid)
        print(f"{tid} code {c} sev {s:.4f} {gas:5s} ops {a['ops'] if a else '':>6} past {a['past'] if a else '':5} "
              f"rs {g['ask_b'][tid]['rs']:.3f} ({g['ask_b'][tid]['basis']})")
    if "--write" in sys.argv:
        import deliver
        deliver.write(g, GOLDEN)


if __name__ == "__main__":
    main()
