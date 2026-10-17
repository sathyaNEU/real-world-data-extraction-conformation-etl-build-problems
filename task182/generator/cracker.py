"""Score the ask layer against the cracker and the mirror, on the cut pack.

The cracker is `supplemental-stumping` Part 1.1's: it landed the call, ran the hygiene battery (key
uniqueness, exact duplicates, unmatched joins, fan-out, count ties), executed the filed rules that battery
points at, and matched every control. It reads the clauses its own quantities name (3.1 and 3.2 for the
level, 4.1 and 4.2 for validity, 4.3 for tonality) and otherwise takes the records at face value, which for
the plant's figures means the process channel the historian writes.

The mirror stops at the most attractive wrong rung, the statistical background of the position's own record,
so it loses the construction layer and answers the rest exactly as the cracker does.

A second, pessimistic cracker is scored beside it: one that reads every clause of the plan, including
section 5, and so executes the counter and run conventions as well. Both numbers are reported, because the
difference between them is the whole of the process records' device mass.

Run: python3 cracker.py            (after build.py, from the generator directory)
"""
import csv
import datetime as dt
import json
import os

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(TASK, "target")
FIG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json"),
                     encoding="utf-8"))

WEEKS = [dt.date(2026, 8, 31) + dt.timedelta(days=7 * i) for i in range(6)]
DAY_START, DAY_END = 7, 19
ASK_WEIGHT = 55.0          # the generated rubric's ask share, points
REC_LANDED = 38.0          # recommendation and critical components, a landed call
REC_MISSED = 5.0           # what a wrong call keeps of them
INSTRUCTION = 7.0


def rows(name):
    with open(os.path.join(T, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def windows():
    """Per position, its weekday assessment windows in local time."""
    out = {}
    for d in rows("meter_deployments_2026.csv"):
        a = dt.datetime.strptime(d["deployed_at"], "%Y-%m-%d %H:%M")
        b = dt.datetime.strptime(d["collected_at"], "%Y-%m-%d %H:%M")
        for k in range((b.date() - a.date()).days + 1):
            day = a.date() + dt.timedelta(days=k)
            if day.weekday() > 4:
                continue
            lo = dt.datetime(day.year, day.month, day.day, DAY_START)
            hi = dt.datetime(day.year, day.month, day.day, DAY_END)
            if lo >= a and hi <= b:
                out.setdefault(d["position_code"], []).append((lo, hi))
    return out


def channel_plant_state():
    """The cracker's per-position figures: the process channel read at face value."""
    feed = [(dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M"), float(r["centrifuge_feed_m3_h"]))
            for r in rows("scada_15min_2026.csv")]
    wins = windows()
    mins, runs = {}, {}
    for code, w in wins.items():
        mins[code] = sum(15 for t, f in feed if f > 0 and any(lo <= t < hi for lo, hi in w))
        n, prev = 0, 0.0
        for t, f in feed:
            if f > 0 and prev == 0 and any(lo <= t < hi for lo, hi in w):
                n += 1
            prev = f
        runs[code] = n
    return mins, runs


def channel_weekly():
    """The cracker's weekly figures: the counter differenced row by row inside the week, the blower's rate
    column summed, a run counted as a block of feed, the engine's hours counted off its export rows."""
    sc = rows("scada_15min_2026.csv")
    out = {}
    prev_c = prev_f = None
    for r in sc:
        t = dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")
        wk = next((i for i, w in enumerate(WEEKS) if w <= t.date() < w + dt.timedelta(days=7)), None)
        c, f = float(r["biogas_meter_m3"]), float(r["centrifuge_feed_m3_h"])
        if wk is not None:
            d = out.setdefault(wk, {"biogas_m3": 0.0, "blower_air_knm3": 0.0, "centrifuge_runs": 0,
                                    "engine_hours": 0.0})
            if prev_c is not None:
                step = c - prev_c
                if step < -50000:
                    step += 100000.0
                if step >= 0:
                    d["biogas_m3"] += step
            d["blower_air_knm3"] += float(r["blower_air_nm3_h"]) * 0.25 / 1000.0
            if f > 0 and (prev_f == 0 or prev_f is None):
                d["centrifuge_runs"] += 1
            if float(r["engine_export_kw"]) > 0:
                d["engine_hours"] += 0.25
        prev_c, prev_f = c, f
    return {k: {"biogas_m3": int(round(v["biogas_m3"])),
                "blower_air_knm3": int(round(v["blower_air_knm3"])),
                "centrifuge_runs": v["centrifuge_runs"],
                "engine_hours": round(v["engine_hours"], 1)} for k, v in out.items()}


def log_runs():
    """Plan 5.2 executed on the shipped log: a start, and the first stop the log records for the same
    machine after it; a start the log does not stop before that machine starts again is not a run."""
    opens, runs = {}, []
    for r in sorted(rows("plant_equipment_events_2026.csv"), key=lambda x: x["logged_at"]):
        if not r["equipment"].startswith("CF-"):
            continue
        t = dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M")
        if r["event"] == "START":
            opens[r["equipment"]] = t
        elif r["equipment"] in opens:
            runs.append((opens.pop(r["equipment"]), t))
    return sorted(runs)


def valid_minutes():
    """The validity mask behind the levels, as plan 4.1 and 4.2 give it: the solver that landed the call
    already holds this, so the clause-reading cracker is given exactly it."""
    import pyarrow.parquet as pq
    met, wind, rained = rows("weather_10min_2026.csv"), {}, {}
    prev_tips, prev_day = None, None
    for r in met:
        t = dt.datetime.strptime(r["measured_at_utc"], "%Y-%m-%d %H:%M")
        v = float(r["wind_speed"])
        wind[t] = round(v / 3.6, 6) if t.date() >= dt.date(2026, 9, 20) else v
        tips = int(r["rain_tips_today"])
        step = tips if (prev_day is None or t.date() != prev_day) else tips - prev_tips
        rained[t] = max(step, 0) > 0
        prev_tips, prev_day = tips, t.date()
    spans = {}
    for d in rows("meter_deployments_2026.csv"):
        spans.setdefault(d["meter_serial"], []).append(
            (dt.datetime.strptime(d["deployed_at"], "%Y-%m-%d %H:%M"),
             dt.datetime.strptime(d["collected_at"], "%Y-%m-%d %H:%M"), d["position_code"]))
    tbl = pq.read_table(os.path.join(T, "sound_levels_1min_2026.parquet")).to_pydict()
    out, seen = {}, set()
    for i in range(len(tbl["meter_serial"])):
        serial, stamp = tbl["meter_serial"][i], tbl["measured_at_utc"][i]
        if (serial, stamp) in seen:
            continue
        seen.add((serial, stamp))
        local = stamp + dt.timedelta(hours=1)
        if local.weekday() > 4 or not (DAY_START <= local.hour < DAY_END):
            continue
        code = None
        for a, b, c in spans.get(serial, []):
            if a <= local <= b:
                code = c
                break
        if code is None:
            continue
        if float(tbl["laeq_db"][i]) <= -120.0:
            continue
        k = stamp - dt.timedelta(minutes=stamp.minute % 10)
        if k in wind and (rained.get(k, False) or wind[k] > 5.0):
            continue
        out.setdefault(code, set()).add(local)
    return out


def clause_plant_state():
    """What a solver who reads plan 5.2 and the ask's own wording files: the log's runs against the valid
    minutes of each position's assessment period, and the runs that overlap any minute of that period."""
    runs = log_runs()
    wins = windows()
    valid = valid_minutes()
    mins, nruns = {}, {}
    for code, w in wins.items():
        n = 0
        for t in sorted(valid.get(code, ())):
            if any(a <= t < b for a, b in runs):
                n += 1
        mins[code] = n
        nruns[code] = sum(1 for a, b in runs if any(a < hi and b > lo for lo, hi in w))
    return mins, nruns


def clause_weekly():
    """What that solver files for the week: plan 5.1's two counter readings, the log's runs that start in
    the week, and the engine's own hour counter with its replacement taken account of."""
    sc = {dt.datetime.strptime(r["logged_at"], "%Y-%m-%d %H:%M"): r
          for r in rows("scada_15min_2026.csv")}
    runs = log_runs()
    out = {}
    for i, wk in enumerate(WEEKS):
        a = dt.datetime(wk.year, wk.month, wk.day)
        b = a + dt.timedelta(days=7)
        air = float(sc[b]["blower_air_total_knm3"]) - float(sc[a]["blower_air_total_knm3"])
        inside = sorted((t, float(r["engine_hours_run"])) for t, r in sc.items() if a <= t <= b)
        eng = 0.0
        for j in range(1, len(inside)):
            step = inside[j][1] - inside[j - 1][1]
            eng += inside[j][1] if step < 0 else step
        out[i] = {"blower_air_knm3": int(round(air)),
                  "centrifuge_runs": sum(1 for s, _ in runs if a <= s < b),
                  "engine_hours": round(eng, 1)}
    return out


def score():
    gold_min = FIG["centrifuge_minutes"]
    gold_run = FIG["centrifuge_runs_position"]
    gold_wk = {int(k): v for k, v in FIG["weekly_plant"].items()}
    ch_min, ch_run = channel_plant_state()
    ch_wk = channel_weekly()
    cl_min, cl_run = clause_plant_state()
    cl_wk = clause_weekly()

    asks = []           # (ask, figure group, criteria, cracker hits, clause-reading cracker hits)
    asks.append(("A1 the fourteen specific levels", 14, 14, 14))
    asks.append(("A1 the five, the sixth and the margin", 3, 3, 3))
    asks.append(("A1 the ranked chart", 4, 4, 4))
    asks.append(("A2 centrifuge minutes per position", 14,
                 sum(1 for c in gold_min if ch_min[c] == gold_min[c]),
                 sum(1 for c in gold_min if cl_min[c] == gold_min[c])))
    asks.append(("A2 centrifuge runs per position", 14,
                 sum(1 for c in gold_run if ch_run[c] == gold_run[c]),
                 sum(1 for c in gold_run if cl_run[c] == gold_run[c])))
    for key, label in (("blower_air_knm3", "blower air delivered"),
                       ("centrifuge_runs", "centrifuge runs"), ("engine_hours", "engine hours run")):
        asks.append(("A3 %s, six weeks" % label, 6,
                     sum(1 for i in range(6) if ch_wk[i][key] == gold_wk[i][key]),
                     sum(1 for i in range(6) if cl_wk[i][key] == gold_wk[i][key])))
    asks.append(("A4 the tone summary", 3, 3, 3))

    n = sum(a[1] for a in asks)
    per = ASK_WEIGHT / n
    construction = {"A1 the fourteen specific levels", "A1 the five, the sixth and the margin",
                    "A1 the ranked chart"}
    ck = sum(a[2] for a in asks)
    ck_clause = sum(a[3] for a in asks)
    mr = sum(a[2] for a in asks if a[0] not in construction)
    mr_clause = sum(a[3] for a in asks if a[0] not in construction)

    print("%-42s %9s %9s %9s" % ("ask figure group", "criteria", "cracker", "clause-reader"))
    for name, crit, h, hc in asks:
        print("%-42s %9d %9s %9s" % (name, crit, "%d hit" % h if h else "all miss",
                                     "%d hit" % hc if hc else "all miss"))
    print("%-42s %9d %9d %9d" % ("total", n, ck, ck_clause))
    out = {}
    for label, c_keep, m_keep in (("cracker (the sheet's)", ck, mr), ("clause-reading cracker", ck_clause,
                                                                     mr_clause)):
        lc, ls = c_keep / float(n), m_keep / float(n)
        C = REC_LANDED + INSTRUCTION + lc * ASK_WEIGHT
        S = REC_MISSED + INSTRUCTION + ls * ASK_WEIGHT
        print("\n%s: keeps %d of %d ask criteria (%.3f of ask weight) -> %.1f" % (label, c_keep, n, lc, C))
        print("   mirror keeps %d (%.3f) -> %.1f;  pair %.1f;  mirror leakage %.1f per cent"
              % (m_keep, ls, S, (C + S) / 2.0, 100.0 * ls))
        out[label] = {"pair": round((C + S) / 2.0, 1), "leakage": round(100.0 * ls, 1),
                      "criteria": n, "cracker_keeps": c_keep, "mirror_keeps": m_keep}
    return out


if __name__ == "__main__":
    score()
