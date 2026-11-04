"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks). Shares no code
with the generator: every figure here is recomputed from target/ by its own route.

    python3 task210/generator/ceiling.py

Ask A is the streetcar's emergency brake applications in service by Mountain-time month (SRM-07 6.2: from a car's
pull-out onto a block until it pulls in, a running brake test on the depot loop after a release excepted, a two-car
train's two records one application); ask B is each line's operator defect cards for brakes, doors and all other
defects, each on the day it was written if the weekday timetable ran, April to October as a whole.

Rows. The cracker lands the call, runs the battery (UTC to Mountain time, exact repeats dropped) and executes every
filed rule against the register each one points at: in service is a pass in the AVL log, the agency's record of its
revenue trips, and a record no pass holds is set aside; it reads the MMS entered date as the keying and dates each card
to the day before it. The second cracker takes in service from the yard sheets, drops each depot running test by the
release log and pairs a two-car train's records within a minute, and dates each card to its car's last day out. The
mirror stops at the observed-rate rung on the call and handles the asks as the cracker does. The full includer reads
every file and acts on every stated fact, against one register per question: the yard sheets' pull-out car between
the block's pull-out and pull-in (the release log's tests dropped, the second car's records dropped or paired), or the
AVL log; each card dated to the day its car ran its block by the yard sheets, or by the AVL log. A car no register
names is an orphan and is set aside. The omniscient row is the golden's handling: the cars that ran each block are
the yard sheets' and the car the AVL log shows taking a block over. The blind row counts every EB record but the named
exceptions and dates each card on the business day before it was entered. The stress rows (not the gate) are the
reconstructions the golden makes: ask A's in-service map across the yard sheets and the AVL log, and ask B's cards the
yard sheets cannot date put on the business day before entry (the keying lag inferred).
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
TZ = "America/Denver"
MLAT = 111320.0
MONTHS = list(range(4, 11))


def _csv(n, target, **kw):
    return pd.read_csv(os.path.join(target, n), **kw)


def _local(s):
    return pd.to_datetime(s, utc=True).dt.tz_convert(TZ).dt.tz_localize(None).astype("datetime64[ns]")


def eb_events(target):
    e = _csv("edr_event_export_2026-04-01_2026-10-31.csv", target)
    e = e[e["event_code"] == "EB"].copy()
    e["t"] = _local(e["event_time_utc"])
    e["sday"] = (e["t"] - pd.Timedelta(hours=3)).dt.normalize()
    return e.reset_index(drop=True)


def yard(target):
    """One row per car on each block-day sheet line, with the block's pull-out and pull-in as times."""
    y = _csv("yard_block_sheets_2026.csv", target)
    y["sday"] = pd.to_datetime(y["sheet_date"], format="%m/%d/%Y")
    hm = lambda s: pd.to_timedelta(s.str[:2].astype(int) * 60 + s.str[3:].astype(int), unit="m")
    y["t_out"] = y["sday"] + hm(y["out_time"].astype(str))
    y["t_in"] = y["sday"] + hm(y["in_time"].astype(str))
    y.loc[y["t_in"] <= y["t_out"], "t_in"] += pd.Timedelta(days=1)
    rows = [(d, b, int(c), k, o, i) for d, b, cs, o, i in zip(y["sday"], y["block"], y["pullout_cars"].astype(str),
                                                              y["t_out"], y["t_in"]) for k, c in enumerate(cs.split("+"))]
    return pd.DataFrame(rows, columns=["sday", "block", "car", "pos", "t_out", "t_in"])


def avl(target, cols=("service_date", "block", "vehicle", "enter_local", "exit_local")):
    a = pd.read_parquet(os.path.join(target, "avl_section_passes_2026.parquet"), columns=list(cols))
    if "service_date" in a:
        a["sday"] = pd.to_datetime(a["service_date"])
    if "block" in a:
        a["block"] = a["block"].astype(str)
    if "vehicle" in a:
        a["vehicle"] = a["vehicle"].astype("int64")
    for c in ("enter_local", "exit_local"):
        if c in a:
            a[c] = a[c].astype("datetime64[ns]")
    return a


def in_service(target):
    """The golden's map of which car was in service on each block when: the yard sheet's car or cars from the block's
    pull-out until the AVL log first shows another vehicle on the block that day, which is in service from then until
    the block's pull-in."""
    y = yard(target)
    a = avl(target, ("service_date", "block", "vehicle", "enter_local"))
    lead = y[y["pos"] == 0][["sday", "block", "car"]].rename(columns={"car": "lead"})
    a = a.merge(lead, on=["sday", "block"])
    sw = a[a["vehicle"] != a["lead"]].groupby(["sday", "block"], as_index=False).agg(spare=("vehicle", "first"),
                                                                                      t_sw=("enter_local", "min"))
    y = y.merge(sw, on=["sday", "block"], how="left")
    y["t_end"] = np.where(y["t_sw"].notna(), y["t_sw"], y["t_in"])
    m = y[["sday", "block", "car", "t_out", "t_end"]].rename(columns={"t_out": "t0", "t_end": "t1"})
    s = y[y["t_sw"].notna() & (y["pos"] == 0)][["sday", "block", "spare", "t_sw", "t_in"]]
    s = s.rename(columns={"spare": "car", "t_sw": "t0", "t_in": "t1"})
    s["car"] = s["car"].astype(int)
    return pd.concat([m, s], ignore_index=True)


def pair_drop(e, window, metres=None):
    """Drop the second record of a pair on the same block and service day within the window (and distance)."""
    e = e.sort_values("t").reset_index(drop=True)
    drop = set()
    for _, g in e.groupby(["sday", "block"]):
        rows = list(g.itertuples())
        for a in range(len(rows)):
            if rows[a].Index in drop:
                continue
            for b in range(a + 1, len(rows)):
                ra, rb = rows[a], rows[b]
                if rb.Index in drop or ra.car == rb.car:
                    continue
                if (rb.t - ra.t).total_seconds() > window:
                    break
                d = np.hypot((rb.lat - ra.lat) * MLAT, (rb.lon - ra.lon) * MLAT * np.cos(np.radians(ra.lat)))
                if metres is None or d <= metres:
                    drop.add(rb.Index)
                    break
    return e[~e.index.isin(drop)]


def ask_a(target, route, tests=None, copies="pair", window=360, metres=80, span=True, utc_month=False):
    """The streetcar's applications by month. route: "avl" (a logged pass of the car), "yard" (the yard sheet's cars,
    between the block's pull-out and pull-in with span, else all service day), "operating" (the golden's in-service
    map), "all" (every record). tests: None, "release" (the release log, the hour after), "signature" (walking pace
    within 300 m of Foundry Loop). copies: "pair" (on one block within the window and distance), "drop" (the yard
    sheet's second car's records), None."""
    e = eb_events(target)
    if tests == "signature":
        g = json.load(open(os.path.join(target, "streetcar_track_survey_2025.geojson")))
        lo, la = [f["geometry"]["coordinates"] for f in g["features"] if f["properties"].get("stop_name") == "Foundry Loop"][0]
        d = np.hypot((e["lat"] - la) * MLAT, (e["lon"] - lo) * MLAT * np.cos(np.radians(la)))
        e = e[~((e["speed_mph"] < 8) & (d < 300))]
    elif tests == "release":
        r = _csv("foundry_depot_releases_2026.csv", target)
        r["released"] = pd.to_datetime(r["released"])
        x = e.reset_index().merge(r[["car", "released"]], on="car", how="left")
        hit = (x["t"] >= x["released"]) & (x["t"] <= x["released"] + pd.Timedelta(minutes=60))
        e = e[~e.index.isin(x.loc[hit, "index"])]
    if route == "all" and copies == "drop":
        y = yard(target)
        second = set(zip(y.loc[y["pos"] == 1, "sday"], y.loc[y["pos"] == 1, "car"]))
        e = e[[(d, int(c)) not in second for d, c in zip(e["sday"], e["car"])]]
        copies = None
    if route == "avl":
        a = avl(target).sort_values("enter_local")
        x = pd.merge_asof(e.astype({"car": "int64"}).sort_values("t"), a[["vehicle", "block", "enter_local", "exit_local"]],
                          left_on="t", right_on="enter_local", left_by="car", right_by="vehicle", direction="backward")
        e = x[(x["t"] <= x["exit_local"] + pd.Timedelta(seconds=20)).fillna(False)].copy()
    elif route == "yard":
        y = yard(target)
        x = e.reset_index().merge(y, on=["sday", "car"], how="inner")
        if span:
            x = x[(x["t"] >= x["t_out"]) & (x["t"] < x["t_in"])]
        e = x.drop_duplicates("index").set_index("index")
    elif route == "operating":
        m = in_service(target)
        x = e.reset_index().merge(m, on=["sday", "car"], how="inner")
        x = x[(x["t"] >= x["t0"]) & (x["t"] < x["t1"])]
        e = x.drop_duplicates("index").set_index("index")
    if copies == "drop" and route != "avl":
        y = yard(target)
        second = set(zip(y.loc[y["pos"] == 1, "sday"], y.loc[y["pos"] == 1, "car"]))
        e = e[[(d, int(c)) not in second for d, c in zip(e["sday"], e["car"])]]
    elif copies == "pair" and window and "block" in e.columns:
        e = pair_drop(e, window, metres)
    month = pd.to_datetime(e["event_time_utc"]).dt.month if utc_month else e["t"].dt.month
    out = pd.Series(1, index=e.index).groupby(month.values).sum()
    return [int(out.get(m, 0)) for m in MONTHS]


def ran(target, source):
    """(service day, block, car) for every car a register shows on a block: "yard", "avl" or both ("operating")."""
    out = []
    if source in ("yard", "operating"):
        out.append(yard(target)[["sday", "block", "car"]])
    if source in ("avl", "operating"):
        a = avl(target, ("service_date", "block", "vehicle")).drop_duplicates()
        out.append(a.rename(columns={"vehicle": "car"})[["sday", "block", "car"]])
    return pd.concat(out, ignore_index=True).drop_duplicates()


def ask_b(target, dating, weekdays="timetable", entry_day=False, fallback=None):
    """Operator cards per line for brakes, doors and the rest, April to October, in weekday service: each card dated by
    the route's own rule (the day its car ran its block, by the yard sheets, the AVL log or both; its car's last day out
    on the yard sheets; the day before it was entered; the MMS entered date); weekday service from the run sheets'
    schedule ("timetable") or the calendar's Monday to Friday."""
    m = _csv("mms_defect_reports_2026.csv", target, dtype={"block": str})
    m = m[m["source"] == "Operator card"].reset_index(drop=True)
    entered = pd.to_datetime(m["entered_at"]).dt.normalize()
    day = pd.Series(pd.NaT, index=m.index)
    if dating in ("operating", "yard", "avl", "car"):
        y = ran(target, "yard" if dating == "car" else dating)
        on = ["car"] if dating == "car" else ["car", "block"]
        x = m[on].assign(kd=entered.values).reset_index().merge(y, on=on)
        hi = (x["sday"] <= x["kd"]) if entry_day else (x["sday"] < x["kd"])
        x = x[hi & (x["sday"] >= x["kd"] - pd.Timedelta(days=7))]
        day = x.groupby("index")["sday"].max().reindex(m.index)
    elif dating == "previous":
        day = entered - pd.Timedelta(days=1)
    elif dating == "business":
        day = entered.map(lambda d: d - pd.offsets.BDay(1))
    else:
        day = pd.to_datetime(m["entered_date"])
    if fallback == "business":
        day = day.fillna(entered.map(lambda d: d - pd.offsets.BDay(1)))
    if weekdays == "timetable":
        r = _csv("run_sheets_2026.csv", target, usecols=["service_date", "schedule"])
        wk = set(pd.to_datetime(r.loc[r["schedule"] == "Weekday", "service_date"].unique()))
        isw = day.map(lambda d: d in wk)
    else:
        isw = day.map(lambda d: (not pd.isna(d)) and d.weekday() < 5)
    ok = isw.astype(bool) & (day >= pd.Timestamp("2026-04-01")) & (day <= pd.Timestamp("2026-10-31"))
    figs = []
    for ln, lo, hi in (("Juniper", 100, 120), ("Foundry", 120, 140)):
        on = ok & (m["car"] >= lo) & (m["car"] < hi)
        figs += [int((on & (m["defect_group"] == "Brakes")).sum()), int((on & (m["defect_group"] == "Doors")).sum()),
                 int((on & ~m["defect_group"].isin(["Brakes", "Doors"])).sum())]
    return figs


def kept(resp, gold):
    return sum(int(x == y) for x, y in zip(resp, gold))


def golden(target=TARGET):
    return ask_a(target, "operating", tests="release", copies="pair", window=360, metres=80) + ask_b(target, "operating")


def main(target=TARGET, verbose=True):
    gold = golden(target)
    fj = json.load(open(os.path.join(HERE, "figures.json")))
    want = [fj["ask_a"]["%02d" % m] for m in MONTHS]
    want += [fj["ask_b"][ln][g] for ln in ("Juniper", "Foundry") for g in ("Brakes", "Doors", "All other")]
    assert gold == want, ("ceiling's own golden handling disagrees with figures.json", gold, want)
    n, na = len(gold), len(MONTHS)
    crack = ask_a(target, "avl", copies=None) + ask_b(target, "previous")
    rows = {
        "cracker (AVL passes; each card on the day before it was entered)": crack,
        "second cracker (yard sheets, release log, pairs in a minute; each card on its car's last day out)":
            ask_a(target, "yard", tests="release", copies="pair", window=60, metres=None) + ask_b(target, "car"),
        "no-repair (every EB record, UTC month; cards on the MMS entered date, calendar weekdays)":
            ask_a(target, "all", copies=None, utc_month=True) + ask_b(target, "entered", weekdays="calendar"),
        "mirror (observed-rate rung on the call; the cracker's ask handling)": crack,
        "full includer, yard (the yard sheet's car from pull-out to pull-in, release log, second car dropped; cards by the yard sheets)":
            ask_a(target, "yard", tests="release", copies="drop") + ask_b(target, "yard"),
        "full includer, AVL (AVL passes; cards by the AVL log)":
            ask_a(target, "avl", copies=None) + ask_b(target, "avl"),
        "full includer, yard paired (yard sheet's car from pull-out to pull-in, release log, pairs in a minute; cards by the yard sheets)":
            ask_a(target, "yard", tests="release", copies="pair", window=60, metres=None) + ask_b(target, "yard"),
        "full includer, signature (yard sheet span, Loop signature, pairs in a minute; each card on its car's last day out)":
            ask_a(target, "yard", tests="signature", copies="pair", window=60, metres=None) + ask_b(target, "car"),
        "blind (every EB record but the release log's tests and the second car's; each card on the business day before entry)":
            ask_a(target, "all", tests="release", copies="drop") + ask_b(target, "business"),
        "stress, A reconstructed (the in-service map across the yard sheets and the AVL; cards by the yard sheets)":
            gold[:na] + ask_b(target, "yard"),
        "stress, B fallback (the yard sheets' span for A; cards by the yard sheets, an undated card on the business day before entry)":
            ask_a(target, "yard", tests="release", copies="drop") + ask_b(target, "yard", fallback="business"),
        "omniscient (the golden's handling; stress row, not the gate)": gold,
    }
    keep = {k: kept(v, gold) for k, v in rows.items()}
    ka = {k: kept(v[:na], gold[:na]) for k, v in rows.items()}
    kb = {k: kept(v[na:], gold[na:]) for k, v in rows.items()}
    crk = max(keep[k] for k in keep if "cracker" in k)
    full = max(keep[k] for k in keep if k.startswith("full includer"))
    lc, lf = crk / n, full / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    if verbose:
        print("golden ask figures", gold)
        for k, v in rows.items():
            print("%-100s A %d of %d, B %d of %d: keeps %2d of %d (%4.1f per cent)  %s" % (
                k, ka[k], na, kb[k], n - na, keep[k], n, 100 * keep[k] / n, v))
        print("pair ceiling %.1f (one on the call, one off); both on the call %.1f; mirror leakage %.1f per cent of the ask "
              "weight; full includer keeps %.1f per cent" % ((c + s) / 2, c, 100 * keep[[k for k in rows if k.startswith("mirror")][0]] / n, 100 * lf))
        print("at the full includer's keep: pair %.1f, both on the call %.1f" % ((45 + 55 * lf + 12 + 55 * lf) / 2, 45 + 55 * lf))
    return dict(pair=(c + s) / 2, both_on=c, leak=100 * lc, full=100 * lf, keep=keep, n=n, na=na, keep_a=ka, keep_b=kb,
                mirror=100 * keep[[k for k in rows if k.startswith("mirror")][0]] / n, rows=rows, gold=gold,
                pair_full=(57 + 110 * lf) / 2, both_full=45 + 55 * lf)


if __name__ == "__main__":
    main()
