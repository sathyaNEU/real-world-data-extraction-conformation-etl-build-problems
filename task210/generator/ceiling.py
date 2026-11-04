"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored against the golden handling on the same files, and the pair priced on the
planning weights (38 for the call and its components, 7 for instruction-following, 55 for the asks). Shares no code
with the generator: every figure here is recomputed from target/ by its own route.

    python3 task210/generator/ceiling.py

Rows. The cracker lands the call, runs the battery (UTC to Mountain time, exact repeats dropped, every badge through
the card register) and takes "in revenue service" to the AVL log, the agency's record of revenue trips, and each
operator's first run-sheet row as the start of revenue service. The second cracker takes revenue service from the yard
sheets, drops each depot running test by the release log and pairs a two-car train's records within a minute, and
starts each window at the class's qualification date. The mirror stops at the observed-rate rung on the call and
handles the asks as the crackers do. The full includer notices every device: the trailing car's copies (paired within
a minute on the same block), the depot tests (dropped by their walking-pace signature in Foundry Loop, or by the
release log), the AVL drop-outs (revenue taken from the yard sheets) and the route-training rows (each window opened
at the first run the operator holds alone).
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


def ask_b(target, start, badges="register"):
    r = _csv("run_sheets_2026.csv", target)
    r["service_date"] = pd.to_datetime(r["service_date"])
    ro = _csv("operator_roster_2026.csv", target)
    ro["qualified"] = pd.to_datetime(ro["qualified"])
    alone = r[r["duty"] == "operator"]
    cards = _csv("badge_card_register.csv", target, dtype={"badge": str})
    if badges != "register":
        cards = cards[cards["withdrawn"].isna()]
    b2o = dict(zip(cards["badge"], cards["operator_no"]))
    e = _csv("edr_event_export_2026-04-01_2026-10-31.csv", target, dtype={"operator_badge": str})
    e = e[e["event_code"] == "OS"].copy()
    e["op"] = e["operator_badge"].map(b2o)
    e["sday"] = (_local(e["event_time_utc"]) - pd.Timedelta(hours=3)).dt.normalize()
    figs = []
    for cls in ("26-2", "26-3"):
        n, h = 0, 0.0
        for o in ro.loc[ro["training_class"] == cls, "operator_no"]:
            src = alone if start == "solo" else r
            w0 = (alone if start == "solo" else r).loc[lambda d: d["operator_no"] == o, "service_date"].min() \
                if start in ("solo", "first_row") else ro.loc[ro["operator_no"] == o, "qualified"].iloc[0]
            w1 = w0 + pd.Timedelta(days=30)
            n += int(((e["op"] == o) & (e["sday"] >= w0) & (e["sday"] < w1)).sum())
            h += float(src.loc[(src["operator_no"] == o) & (src["service_date"] >= w0) & (src["service_date"] < w1), "revenue_hours"].sum())
        figs += [n, round(h, 1), round(100 * n / h, 1)]
    return figs


def kept(resp, gold):
    return sum(int(x == y) for x, y in zip(resp, gold))


def main(target=TARGET):
    gold = ask_a(target, "operating", window=360, metres=80) + ask_b(target, "solo")
    fj = json.load(open(os.path.join(HERE, "figures.json")))
    want = [fj["ask_a"][k] for k in sorted(fj["ask_a"], key=lambda k: (k.split()[0] != "Juniper", k))]
    want += [v for c in ("May", "August") for v in (fj["ask_b"][c]["overspeeds"], fj["ask_b"][c]["revenue_hours"],
                                                    fj["ask_b"][c]["per_100h"])]
    assert gold == want, ("ceiling's own golden handling disagrees with figures.json", gold, want)
    n = len(gold)
    rows = {
        "cracker (AVL revenue log; first operator duty on the run sheets)": ask_a(target, "avl", window=0) + ask_b(target, "solo"),
        "second cracker (yard sheets, release log, pairs in a minute; class date)":
            ask_a(target, "yard", tests="release", window=60) + ask_b(target, "qualified"),
        "naive (every EB record, UTC month; class date, current cards)": ask_a(target, "all", window=0, utc_month=True)
            + ask_b(target, "qualified", badges="current"),
        "full includer, signature (yard, Loop signature, pairs in a minute; first solo run)":
            ask_a(target, "yard", tests="signature", window=60) + ask_b(target, "solo"),
        "full includer, release log (yard, release log, pairs in a minute; first solo run)":
            ask_a(target, "yard", tests="release", window=60) + ask_b(target, "solo"),
        "full includer, AVL (AVL revenue log; first solo run)": ask_a(target, "avl", window=0) + ask_b(target, "solo"),
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
    print("pair ceiling %.1f (one on the call, one off); both on the call %.1f; mirror leakage %.1f per cent of the ask "
          "weight; full includer keeps %.1f per cent" % ((c + s) / 2, c, 100 * lc, 100 * full / n))
    return dict(pair=(c + s) / 2, both_on=c, leak=100 * lc, full=100 * full / n, keep=keep, n=n)


if __name__ == "__main__":
    main()
