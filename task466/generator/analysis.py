"""Computes every rung of the ladder, the golden and every ask answer from the shipped files in target/ alone.

    python3 analysis.py <target dir>
"""
import csv
import datetime as dt
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C  # noqa: E402

RHO_N = 0.7168
CE = 0.90
OX = 0.10
DE = 0.99
TIERS = ((375.0, 0, "Tier 1"), (450.0, 118000, "Tier 2"), (1e12, 312000, "Tier 3"))


def tier_of(released):
    for lim, charge, name in TIERS:
        if released < lim:
            return name, charge
    return TIERS[-1][2], TIERS[-1][1]


# ------------------------------------------------------------------------------------------------ readers
def read_scada(target):
    path = os.path.join(target, "BH_gas_plant_hourly_2024-2026.csv")
    rows = []
    with open(path, encoding="utf-8") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    rd = csv.reader(lines)
    head = next(rd)
    for r in rd:
        rows.append(r)
    ts = np.array([dt.datetime.strptime(r[0], "%Y-%m-%d %H:%M").replace(tzinfo=C.UTC) for r in rows])

    def col(i):
        return np.array([float(r[i]) if r[i] != "" else np.nan for r in rows])
    d = dict(ts=ts, blwa=col(1), blwb=col(2), flow=col(3), ch4=col(4), o2=col(5), co2=col(6), vac=col(7),
             g1=col(8), g2=col(9), flare=col(10), ftemp=col(11), head=head)
    d["run"] = d["blwa"] + d["blwb"]
    d["ch4kg"] = np.where(d["flow"] > 0, d["flow"] * np.nan_to_num(d["ch4"]) / 100.0 * RHO_N, 0.0)
    return d


def parse_local(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=C.TZ).astimezone(C.UTC)


def read_outages(target):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, "BH_gas_plant_outage_log_2024-2026.xlsx"), read_only=True)
    ws = wb["Outages"]
    out = []
    for r in ws.iter_rows(min_row=4, values_only=True):
        if r[0] is None:
            continue
        a, b = parse_local(r[1]), parse_local(r[2])
        out.append(dict(no=int(r[0]), start=a, end=b, cause=r[4]))
    return out


def year_bounds(year):
    a = dt.datetime(year, 1, 1, tzinfo=C.TZ).astimezone(C.UTC)
    b = dt.datetime(year + 1, 1, 1, tzinfo=C.TZ).astimezone(C.UTC)
    return a, b


def year_mask(ts, year, basis="local"):
    if basis == "local":
        a, b = year_bounds(year)
    else:
        a, b = C.utc(year, 1, 1), C.utc(year + 1, 1, 1)
    return np.array([(t >= a) and (t < b) for t in ts])


def released(gen, cap):
    return (gen - cap) * (1 - OX) + cap * (1 - DE)


# ------------------------------------------------------------------------------------------------ the call
def recovery_windows(d, outages, end_rule="return", tol=0.03, base_h=48, fixed_h=None):
    """For each outage, the hours after the restart while the capture runs above its pre-outage level.

    end_rule 'return': until three consecutive hours sit within tol of the baseline; 'fixed': fixed_h hours.
    Returns a list of (outage index, first hour index, last hour index exclusive, baseline kg/h)."""
    ts = d["ts"]
    t0 = ts[0]
    idx_of = lambda t: int((t - t0).total_seconds() // 3600)  # noqa: E731
    out = []
    for k, o in enumerate(outages):
        s, e = idx_of(o["start"]), idx_of(o["end"])
        lo = max(0, s - base_h)
        pre = d["ch4kg"][lo:s]
        prer = d["run"][lo:s]
        good = pre[prer >= 0.999]
        base = float(np.median(good)) if len(good) else np.nan
        first = e + 1 if (o["end"].minute > 0) else e
        # the partial restart hour is part of the outage-affected span
        start_h = e
        if end_rule == "fixed":
            last = min(len(ts), first + fixed_h)
        else:
            j = first
            while j + 3 < len(ts) and not np.all(np.abs(d["ch4kg"][j:j + 3] - base) <= tol * base):
                j += 1
            last = j
        out.append((k, start_h, last, base))
    return out


def golden_call(d, outages, year=2026, **kw):
    ts = d["ts"]
    m = year_mask(ts, year)
    cap = float(d["ch4kg"][m].sum()) / 1000.0
    yo = [o for o in outages if o["start"] >= year_bounds(year)[0] and o["start"] < year_bounds(year)[1]]
    hours_year = (year_bounds(year)[1] - year_bounds(year)[0]).total_seconds() / 3600.0
    down = sum((o["end"] - o["start"]).total_seconds() / 3600.0 for o in yo)
    f_rec = 1 - down / hours_year
    naive_gen = cap / CE
    hh8_gen = cap / (CE * f_rec)
    # steady hours: full running hours outside every outage and every recovery span
    wins = recovery_windows(d, outages, **kw)
    steady = (d["run"] >= 0.999)
    t0 = ts[0]
    for o in outages:
        s = int((o["start"] - t0).total_seconds() // 3600)
        e = int((o["end"] - t0).total_seconds() // 3600)
        steady[s:e + 1] = False
    excess = 0.0
    for k, a, b, base in wins:
        steady[a:b] = False
        o = outages[k]
        if year_bounds(year)[0] <= o["start"] < year_bounds(year)[1]:
            # the restart hour carries the running part's steady capture plus held gas
            e_frac = 1.0 - (o["end"].minute / 60.0)
            seg = d["ch4kg"][a:b].copy()
            basev = np.full(len(seg), base)
            basev[0] = base * e_frac
            excess += float((seg - basev).sum())
    excess /= 1000.0
    # generation from the steady hours, month by month (local months)
    gen = 0.0
    months = []
    for mo in range(1, 13):
        a = dt.datetime(year, mo, 1, tzinfo=C.TZ).astimezone(C.UTC)
        b = (dt.datetime(year, mo + 1, 1, tzinfo=C.TZ) if mo < 12 else dt.datetime(year + 1, 1, 1, tzinfo=C.TZ)).astimezone(C.UTC)
        mm = np.array([(t >= a) and (t < b) for t in ts])
        hrs = (b - a).total_seconds() / 3600.0
        rate = float(d["ch4kg"][mm & steady].mean())
        months.append(dict(month=mo, steady_rate=rate, hours=hrs))
        gen += rate / CE * hrs / 1000.0
    excess_gen = (cap - excess) / (CE * f_rec)
    return dict(captured=cap, down_hours=down, f_rec=f_rec, n_outages=len(yo), hours_year=hours_year,
                naive_gen=naive_gen, hh8_gen=hh8_gen, steady_gen=gen, excess_gen=excess_gen, recovered=excess,
                naive_rel=released(naive_gen, cap), hh8_rel=released(hh8_gen, cap), golden_rel=released(gen, cap),
                excess_rel=released(excess_gen, cap), months=months)


def variants(d, outages, year=2026):
    """Every construction of the golden family and of the rivals, for the convergence assertions."""
    out = {}
    for rule, extra in (("return", dict(tol=0.02)), ("return", dict(tol=0.03)), ("return", dict(tol=0.05)),
                        ("fixed", dict(fixed_h=24)), ("fixed", dict(fixed_h=36)), ("fixed", dict(fixed_h=48)),
                        ("fixed", dict(fixed_h=72))):
        for bh in (24, 48, 168):
            g = golden_call(d, outages, year, end_rule=rule, base_h=bh, **extra)
            key = "%s_%s_b%d" % (rule, "_".join("%s%s" % kv for kv in extra.items()), bh)
            out["steady_" + key] = g["golden_rel"]
            out["excess_" + key] = g["excess_rel"]
    g = golden_call(d, outages, year)
    ts = d["ts"]
    m = year_mask(ts, year)
    runh = (d["run"] >= 0.999) & m
    # one-group-by routes a solver might take
    out["median_running"] = released(float(np.median(d["ch4kg"][runh])) / CE * g["hours_year"] / 1000.0, g["captured"])
    out["mean_running_x_year"] = released(float(d["ch4kg"][runh].mean()) / CE * g["hours_year"] / 1000.0, g["captured"])
    # UTC year instead of local year for the golden
    mu = year_mask(ts, year, "utc")
    out["utc_year_capture_shift"] = float(d["ch4kg"][mu].sum()) / 1000.0 - g["captured"]
    return out


# ------------------------------------------------------------------------------------------------ asks
def read_events(target):
    rows = []
    with open(os.path.join(target, "BH_engine_plant_events_2026.txt"), encoding="utf-8") as f:
        for ln in f:
            mm = re.match(r"^(\d{4}-\d\d-\d\d)\s+(\d\d:\d\d:\d\d)\s+(\S+)\s+(.+?)\s{2,}(.*)$", ln.rstrip("\r\n"))
            if not mm:
                continue
            day, tm, unit, code, text = mm.groups()
            rows.append(dict(local=day + " " + tm, unit=unit, code=code.strip(), text=text.strip()))
    # local to UTC; a repeated hour at the autumn change is taken in order (first CDT, then CST)
    out = []
    seen_fold = False
    for r in rows:
        naive = dt.datetime.strptime(r["local"], "%Y-%m-%d %H:%M:%S")
        t = naive.replace(tzinfo=C.TZ)
        if naive.date() == dt.date(2026, 11, 1) and naive.hour == 1:
            t = naive.replace(tzinfo=C.TZ, fold=1 if seen_fold else 0)
        out.append(dict(r, t=t.astimezone(C.UTC)))
        if naive.date() == dt.date(2026, 11, 1) and naive.hour >= 1:
            seen_fold = seen_fold or naive.hour >= 2
    return out


def quarter_bounds(year, q):
    m0 = (1, 4, 7, 10)[q - 1]
    a = dt.datetime(year, m0, 1, tzinfo=C.TZ).astimezone(C.UTC)
    b = (dt.datetime(year, m0 + 3, 1, tzinfo=C.TZ) if q < 4 else dt.datetime(year + 1, 1, 1, tzinfo=C.TZ)).astimezone(C.UTC)
    return a, b


def engine_answers(target, outages, use_outage_log=True, count_resync=False):
    """Each engine's operating hours (synchronised) and starts from standstill, per local quarter of 2026."""
    ev = read_events(target)
    res = {}
    pf = [o for o in outages if o["cause"] == "Utility power failure"]
    for unit, e in (("GEN1", 1), ("GEN2", 2)):
        intervals = []
        starts = []
        state = "running"            # the year opens with both engines on the grid (first line decides otherwise)
        on_since = year_bounds(2026)[0]
        lines = [x for x in ev if x["unit"] == unit]
        for x in lines:
            c = x["code"]
            if c in ("STOP", "TRIP"):
                if state == "running":
                    intervals.append((on_since, x["t"]))
                state = "stopped"
            elif c == "BREAKER OPEN":
                if state == "running":
                    intervals.append((on_since, x["t"]))
                state = "breaker"
            elif c == "CONTROLLER POWER UP":
                if state == "running":
                    # the controller lost power with the plant: the engine stopped when the supply failed
                    stop_t = x["t"]
                    if use_outage_log:
                        cands = [o for o in pf if o["start"] <= x["t"] <= o["end"] + dt.timedelta(minutes=10)]
                        if cands:
                            stop_t = cands[-1]["start"]
                    intervals.append((on_since, stop_t))
                state = "stopped"
            elif c == "RUNNING":
                if state == "stopped":
                    starts.append(x["t"])
                elif state == "breaker" and count_resync:
                    starts.append(x["t"])
                if state != "running":
                    on_since = x["t"]
                state = "running"
        if state == "running":
            intervals.append((on_since, year_bounds(2026)[1]))
        for q in (1, 2, 3, 4):
            a, b = quarter_bounds(2026, q)
            hrs = sum(max(0.0, (min(y, b) - max(x0, a)).total_seconds()) for x0, y in intervals) / 3600.0
            n = sum(1 for s in starts if a <= s < b)
            res[(e, q)] = dict(hours=hrs, starts=n)
    return res


def flare_answers(target, d, outages):
    """The methane destroyed in the flare per local quarter (routed by difference at the plant: inlet less engines),
    and the flare's operating hours (lit at or above 1,400 F) per quarter from the event log."""
    out = {}
    ts = d["ts"]
    routed_diff = np.where(d["flow"] > 0, (d["flow"] - d["g1"] - d["g2"]) * np.nan_to_num(d["ch4"]) / 100.0 * RHO_N, 0.0)
    routed_diff = np.clip(routed_diff, 0, None)
    routed_meter_n = d["flare"] * np.nan_to_num(d["ch4"]) / 100.0 * RHO_N
    ev = [x for x in read_events(target) if x["unit"] == "FLR"]
    for q in (1, 2, 3, 4):
        a, b = quarter_bounds(2026, q)
        mq = np.array([(t >= a) and (t < b) for t in ts])
        out[q] = dict(destroyed=float(routed_diff[mq].sum()) * DE / 1000.0,
                      destroyed_meter_normal=float(routed_meter_n[mq].sum()) * DE / 1000.0)
    # operating hours from the event log
    first = ev[0]["code"] if ev else "FLARE START"
    opening_lit = first in ("LOW TEMP", "FLARE STOP", "TEMP NORMAL")
    opening_perm = first in ("LOW TEMP", "FLARE STOP")
    y0 = year_bounds(2026)[0]
    for q in (1, 2, 3, 4):
        a, b = quarter_bounds(2026, q)
        op = 0.0
        lit_only = 0.0
        state_on, perm = opening_lit, opening_perm
        t_perm = y0 if opening_perm else None
        t_lit = y0 if opening_lit else None
        for x in ev:
            c = x["code"]
            t = x["t"]
            if c == "FLARE START":
                state_on, perm, t_lit = True, False, t
            elif c in ("TEMP PERMISSIVE", "TEMP NORMAL"):
                if state_on and not perm:
                    perm, t_perm = True, t
            elif c == "LOW TEMP":
                if perm:
                    op += max(0.0, (min(t, b) - max(t_perm, a)).total_seconds())
                perm = False
            elif c == "FLARE STOP":
                if perm:
                    op += max(0.0, (min(t, b) - max(t_perm, a)).total_seconds())
                if state_on and t_lit is not None:
                    lit_only += max(0.0, (min(t, b) - max(t_lit, a)).total_seconds())
                state_on, perm = False, False
        out[q]["hours"] = op / 3600.0
        out[q]["hours_lit"] = lit_only / 3600.0
    return out


def read_sem(target):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, "BH_surface_emissions_monitoring_2026.xlsx"), read_only=True)
    walks = {}
    for q in (1, 2, 3, 4):
        ws = wb["Q%d walkover" % q]
        rows = []
        for r in ws.iter_rows(min_row=3, values_only=True):
            if r[0] is None:
                continue
            t = dt.datetime.strptime(r[0] + " " + r[1], "%Y-%m-%d %H:%M:%S").replace(tzinfo=C.TZ)
            rows.append(dict(t=t, label=r[2], x=float(r[3]), y=float(r[4]), ppm=float(r[5]), bg=float(r[6])))
        walks[q] = rows
    rm = []
    ws = wb["Re-monitoring"]
    for r in ws.iter_rows(min_row=3, values_only=True):
        if r[0] is None:
            continue
        t = dt.datetime.strptime(r[1] + " " + r[2], "%Y-%m-%d %H:%M").replace(tzinfo=C.TZ)
        rm.append(dict(q=int(r[0][1]), t=t, label=r[3], x=float(r[4]), y=float(r[5]), ppm=float(r[6])))
    checks = []
    with open(os.path.join(target, "SEM_analyser_checks_2026.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t = dt.datetime.strptime(r["date"] + " " + r["time"], "%Y-%m-%d %H:%M").replace(tzinfo=C.TZ)
            checks.append(dict(t=t, result=r["result"]))
    return walks, rm, checks


def sem_answers(target, void_rule=True, match="gps", radius=25.0):
    walks, rm, checks = read_sem(target)
    out = {}
    for q in (1, 2, 3, 4):
        rows = walks[q]
        if void_rule:
            # readings after the last passing check and before a failed check are void
            fails = [c["t"] for c in checks if c["result"] == "FAIL"]
            void = []
            for ft in fails:
                passes = [c["t"] for c in checks if c["result"] == "PASS" and c["t"] < ft and c["t"].date() == ft.date()]
                if passes:
                    lo = max(passes)
                    void.append((lo, ft))
            rows = [r for r in rows if not any(lo <= r["t"] < hi for lo, hi in void)]
        exc = [r for r in rows if r["ppm"] - r["bg"] > 500]
        # one location per point label (a re-walked point counts once)
        locs = {}
        for r in exc:
            locs.setdefault(r["label"], r)
        locs = list(locs.values())
        still = 0
        for loc in locs:
            cands = [x for x in rm if x["q"] == q]
            if match == "gps":
                best = min(cands, key=lambda x: (x["x"] - loc["x"]) ** 2 + (x["y"] - loc["y"]) ** 2) if cands else None
                if best is not None and ((best["x"] - loc["x"]) ** 2 + (best["y"] - loc["y"]) ** 2) ** 0.5 <= radius:
                    if best["ppm"] - 3 > 500:
                        still += 1
                else:
                    still += 1        # not re-monitored counts as not cleared
            else:
                hit = [x for x in cands if x["label"] == loc["label"]]
                if not hit or hit[0]["ppm"] - 3 > 500:
                    still += 1
        out[q] = dict(exceed=len(locs), still=still)
    return out


def compute(target):
    d = read_scada(target)
    outages = read_outages(target)
    g = golden_call(d, outages)
    res = dict(call=g, variants=variants(d, outages))
    res["tier"], res["charge"] = tier_of(g["golden_rel"])
    res["tier_hh8"], _ = tier_of(g["hh8_rel"])
    res["tier_naive"], _ = tier_of(g["naive_rel"])
    res["engines"] = engine_answers(target, outages)
    res["flare"] = flare_answers(target, d, outages)
    res["sem"] = sem_answers(target)
    # back years for the back-test line
    res["back"] = {y: golden_call(d, outages, y) for y in (2024, 2025)}
    return res


if __name__ == "__main__":
    import json
    r = compute(sys.argv[1] if len(sys.argv) > 1 else os.path.join(C.TASK, "target"))
    g = r["call"]
    print(json.dumps({k: v for k, v in g.items() if k != "months"}, indent=1, default=str))
    print(r["tier"], r["charge"], "hh8:", r["tier_hh8"], "naive:", r["tier_naive"])
    print({k: round(v, 1) for k, v in r["variants"].items()})
