"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks). Shares no code
with the generator: every figure here is recomputed from target/ by its own route.

    python3 task210/generator/ceiling.py

Rows. The cracker lands the call, runs the battery (UTC to Mountain time, exact repeats dropped, every badge through
the card register) and takes "in revenue service" to the AVL log, the agency's record of revenue trips; it sees that the
MMS keys operators' cards on business mornings and dates each card to the service day before it was keyed. The second
cracker takes revenue service from the yard sheets, drops each depot running test by the release log and pairs a
two-car train's records within a minute, and dates each card to the last day its car pulled out before the card was
keyed. The mirror stops at the observed-rate rung on the call and handles the asks as the crackers do. The full
includer notices every device: the trailing car's copies (paired within a minute on the same block), the depot tests
(dropped by their walking-pace signature in Foundry Loop, or by the release log), the AVL drop-outs (revenue taken from
the yard sheets), and the cards' keying lag (each card dated to its car's last day out, or to the day its car ran the
card's block, with weekdays read off the calendar).
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
    y = _csv("yard_block_sheets_2026.csv", target)
    y["sday"] = pd.to_datetime(y["sheet_date"], format="%m/%d/%Y")
    rows = [(d, b, int(c)) for d, b, cs in zip(y["sday"], y["block"], y["pullout_cars"].astype(str)) for c in cs.split("+")]
    return pd.DataFrame(rows, columns=["sday", "block", "car"])


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


def ask_a(target, route, tests=None, window=60, metres=None, utc_month=False):
    e = eb_events(target)
    if route == "all":
        pass
    elif route == "avl":
        a = pd.read_parquet(os.path.join(target, "avl_section_passes_2026.parquet"),
                            columns=["vehicle", "block", "enter_local", "exit_local"])
        a = a.astype({"vehicle": "int64", "enter_local": "datetime64[ns]", "exit_local": "datetime64[ns]"}).sort_values("enter_local")
        x = pd.merge_asof(e.astype({"car": "int64"}).sort_values("t"), a, left_on="t", right_on="enter_local",
                          left_by="car", right_by="vehicle", direction="backward")
        e = x[(x["t"] <= x["exit_local"] + pd.Timedelta(seconds=20)).fillna(False)].copy()
        e["block"] = e["block"].astype(str)
    elif route in ("yard", "operating"):
        y = yard(target)
        e = e.merge(y, on=["sday", "car"], how="inner")
        if route == "operating":
            a = pd.read_parquet(os.path.join(target, "avl_section_passes_2026.parquet"),
                                columns=["service_date", "block", "vehicle", "enter_local"])
            a["sday"] = pd.to_datetime(a["service_date"])
            a["block"] = a["block"].astype(str)
            a["vehicle"] = a["vehicle"].astype(int)
            lead = y.groupby(["sday", "block"])["car"].first().rename("lead").reset_index()
            a = a.merge(lead, on=["sday", "block"])
            sw = a[a["vehicle"] != a["lead"]].groupby(["sday", "block"], as_index=False).agg(
                vehicle=("vehicle", "first"), t_sw=("enter_local", "min"))
            e = e.merge(sw[["sday", "block", "t_sw"]], on=["sday", "block"], how="left")
            e = e[e["t_sw"].isna() | (e["t"] < e["t_sw"])].drop(columns="t_sw")
            # the car that took over a block after a swap runs it to the end of the day
            ee = eb_events(target).merge(sw.rename(columns={"vehicle": "car"}), on=["sday", "car"], how="inner")
            ee = ee[ee["t"] >= ee["t_sw"]].drop(columns="t_sw")
            e = pd.concat([e, ee], ignore_index=True)
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
    if window and "block" in e.columns:
        e = pair_drop(e, window, metres)
    month = pd.to_datetime(e["event_time_utc"]).dt.month if utc_month else e["t"].dt.month
    line = np.where(e["car"] < 120, "Juniper", "Foundry")
    out = pd.Series(1, index=e.index).groupby([line, month.values]).sum()
    return [int(out.get((ln, m), 0)) for ln in ("Juniper", "Foundry") for m in range(4, 11)]


def ask_b(target, dating, weekdays="timetable"):
    """Operator cards per line for brakes, doors and the rest, April to October, in weekday service: each card dated
    by the route's own rule (the card's car on its block, the car's last day out, the day before keying, or the
    MMS reported date); weekday service from the AVL log (a Monday to Friday with trips before 07:00, the weekday
    timetable's start), or the calendar's Monday to Friday."""
    m = _csv("mms_defect_reports_2026.csv", target, dtype={"block": str})
    m = m[m["source"] == "Operator card"].reset_index(drop=True)
    keyed = pd.to_datetime(m["created"]).dt.normalize()
    y = yard(target)
    day = pd.Series(pd.NaT, index=m.index)
    if dating in ("block", "car"):
        for k in m.index:
            c = y[(y["car"] == m.at[k, "car"]) & (y["sday"] < keyed[k]) & (y["sday"] >= keyed[k] - pd.Timedelta(days=7))]
            if dating == "block":
                c = c[c["block"] == m.at[k, "block"]]
            if len(c):
                day[k] = c["sday"].max()
    elif dating == "previous":
        day = keyed - pd.Timedelta(days=1)
    else:
        day = pd.to_datetime(m["reported"])
    if weekdays == "timetable":
        a = pd.read_parquet(os.path.join(target, "avl_section_passes_2026.parquet"), columns=["service_date", "enter_local"])
        a["service_date"] = pd.to_datetime(a["service_date"])
        early = a[a["enter_local"].dt.hour < 7].groupby("service_date").size()
        wk = {d for d in early.index if d.weekday() < 5}
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


def main(target=TARGET):
    gold = ask_a(target, "operating", window=360, metres=80) + ask_b(target, "block")
    fj = json.load(open(os.path.join(HERE, "figures.json")))
    want = [fj["ask_a"][k] for k in sorted(fj["ask_a"], key=lambda k: (k.split()[0] != "Juniper", k))]
    want += [fj["ask_b"][ln][g] for ln in ("Juniper", "Foundry") for g in ("Brakes", "Doors", "All other")]
    assert gold == want, ("ceiling's own golden handling disagrees with figures.json", gold, want)
    n = len(gold)
    rows = {
        "cracker (AVL revenue log; each card on the day before it was keyed)": ask_a(target, "avl", window=0)
            + ask_b(target, "previous"),
        "second cracker (yard sheets, release log, pairs in a minute; each card on its car's last day out)":
            ask_a(target, "yard", tests="release", window=60) + ask_b(target, "car"),
        "naive (every EB record, UTC month; cards on the MMS reported date, calendar weekdays)":
            ask_a(target, "all", window=0, utc_month=True) + ask_b(target, "reported", weekdays="calendar"),
        "full includer, signature (yard, Loop signature, pairs in a minute; each card on its car's last day out)":
            ask_a(target, "yard", tests="signature", window=60) + ask_b(target, "car"),
        "full includer, release log (yard, release log, pairs in a minute; card on its block's day, calendar weekdays)":
            ask_a(target, "yard", tests="release", window=60) + ask_b(target, "block", weekdays="calendar"),
        "full includer, AVL (AVL revenue log; card on its block's day, calendar weekdays)": ask_a(target, "avl", window=0)
            + ask_b(target, "block", weekdays="calendar"),
        "omniscient (the golden's handling; stress row, not the gate)": gold,
    }
    keep = {k: kept(v, gold) for k, v in rows.items()}
    crack = max(keep[k] for k in keep if "cracker" in k)
    full = max(keep[k] for k in keep if k.startswith("full includer"))
    lc = crack / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lc
    for k, v in keep.items():
        print("%-88s keeps %2d of %d ask figures (%4.1f per cent)" % (k, v, n, 100 * v / n))
    na = 14
    ka = {k: kept(v[:na], gold[:na]) for k, v in rows.items()}
    kb = {k: kept(v[na:], gold[na:]) for k, v in rows.items()}
    lf = full / n
    print("pair ceiling %.1f (one on the call, one off); both on the call %.1f; mirror leakage %.1f per cent of the ask "
          "weight; full includer keeps %.1f per cent" % ((c + s) / 2, c, 100 * lc, 100 * lf))
    print("at the full includer's keep: pair %.1f, both on the call %.1f" % ((45 + 55 * lf + 12 + 55 * lf) / 2, 45 + 55 * lf))
    return dict(pair=(c + s) / 2, both_on=c, leak=100 * lc, full=100 * lf, keep=keep, n=n, keep_a=ka, keep_b=kb,
                pair_full=(57 + 110 * lf) / 2, both_full=45 + 55 * lf)


if __name__ == "__main__":
    main()
