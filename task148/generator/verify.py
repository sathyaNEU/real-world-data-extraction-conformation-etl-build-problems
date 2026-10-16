"""Independent verifier: reads only the bundle (target/) and the goldens, on its own code path (pandas readers, a
uniformized Erlang A, a winding-number boundary test, its own callback matching), and recomputes every graded figure.
It imports nothing from the generator."""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
import pandas as pd

LEG = "acd_call_detail_legacy_2025-01-01_2025-05-16.csv"
I3 = "i3_call_log_2025-05-13_2026-09-30.jsonl"
FC = "tri_county_911_hourly_forecast_fy2027_fy2028.xlsx"
CHE = "che_location_records_fy2026_northeast.csv"
GEOJ = "halvorsen_township_boundary.geojson"
DIRC = "esinet_psap_directory.csv"
CB = "callback_desk_tasks_2026-01_2026-06.csv"
TZ = "America/Chicago"


def load_calls(t):
    a = pd.read_csv(os.path.join(t, LEG), dtype=str, keep_default_na=False)
    a = a[a["CALL_STATUS"] != "TST"]

    def loc(s):
        x = pd.to_datetime(s.where(s != "", None), format="%m/%d/%Y %H:%M:%S")
        return x.dt.tz_localize(TZ).dt.tz_convert("UTC")
    leg = pd.DataFrame({"presented": loc(a["SEIZE_TIME"]), "answered": loc(a["ANS_TIME"]),
                        "ready": loc(a["RDY_TIME"]), "ended": loc(a["DISC_TIME"]),
                        "abandoned": a["CALL_STATUS"] == "ABN", "service": a["CLASS_OF_SVC"], "xfer_to": a["XFER_OUT_TO"],
                        "cbn": a["CBN_REF"].str.lower(), "id": a["CALL_ID"]})
    recs = [json.loads(x) for x in open(os.path.join(t, I3), encoding="utf-8")]
    b = pd.DataFrame(recs)
    b = b[b["serviceType"] != "test"]
    ts = lambda col: pd.to_datetime(b[col], format="%Y-%m-%dT%H:%M:%S.%fZ", utc=True)
    i3 = pd.DataFrame({"presented": ts("presented"), "answered": ts("answered"), "ready": ts("ready"), "ended": ts("ended"),
                       "abandoned": b["disposition"] == "abandoned", "service": b["serviceType"],
                       "xfer_to": b["transferTo"].fillna(""), "cbn": b["callbackRef"].str.replace("cb-", "", regex=False),
                       "id": b["callId"]})
    df = pd.concat([leg, i3], ignore_index=True)
    end = df["ended"].where(df["abandoned"], df["answered"])
    df["wait"] = (end - df["presented"]).dt.total_seconds()
    df["busy"] = (df["ready"] - df["answered"]).dt.total_seconds()
    return df


def tagged_uniform(c, mu, th, t, K=90):
    """P(answered within t | k ahead) and P(abandoned within t | k ahead), k = 0..K-1, by uniformization."""
    n = K + 2
    S, AB = K, K + 1
    Q = np.zeros((n, n))
    for k in range(K):
        if k:
            Q[k, k - 1] = c * mu + k * th
        else:
            Q[k, S] = c * mu
        Q[k, AB] = th
        Q[k, k] = -Q[k].sum()
    lam = -Q.diagonal().min()
    P = np.eye(n) + Q / lam
    x = lam * t
    acc = np.zeros((n, n))
    term = np.eye(n)
    w = math.exp(-x)
    j = 0
    while True:
        acc += w * term
        j += 1
        w *= x / j
        term = term @ P
        if j > x + 12 * math.sqrt(x + 1) + 20:
            break
    return acc[:K, S], acc[:K, AB]


_CACHE = {}


def share(lam, mu, th, c, t=15 / 3600, tex=5 / 3600):
    key = (c, mu, th)
    if key not in _CACHE:
        _CACHE[key] = (tagged_uniform(c, mu, th, t)[0], tagged_uniform(c, mu, th, tex)[1])
    s15, a5 = _CACHE[key]
    N = c + 90
    p = np.ones(N)
    for k in range(1, N):
        p[k] = p[k - 1] * lam / (min(k, c) * mu + max(k - c, 0) * th)
    p /= p.sum()
    q = p[c:]
    return p[:c].sum() + q @ s15, q @ a5


def fy2028(t, busy, pat):
    df = pd.read_excel(os.path.join(t, FC), sheet_name="FY2028", header=2)
    df = df[df["PSAP"] == "Tavish County ECA"]
    cell = {}
    for _, r in df.iterrows():
        mon = pd.Timestamp(pd.to_datetime(r["Month"], format="%b %Y"))
        cell[(mon.year, mon.month, r["Day"], int(str(r["Hour beginning"])[:2]))] = float(r["Forecast 911 calls per hour"])
    mu, th = 3600 / busy, 3600 / pat
    out = {}
    for y, m in [(2027, k) for k in range(7, 13)] + [(2028, k) for k in range(1, 7)]:
        num = den = 0.0
        d = pd.Timestamp(year=y, month=m, day=1)
        while d.month == m:
            if d.dayofweek in (4, 5):
                start = pd.Timestamp(year=d.year, month=d.month, day=d.day, hour=22).tz_localize(TZ).tz_convert("UTC")
                nxt = d + pd.Timedelta(days=1)
                stop = pd.Timestamp(year=nxt.year, month=nxt.month, day=nxt.day, hour=2).tz_localize(
                    TZ, nonexistent="shift_backward").tz_convert("UTC")
                h = start
                while h < stop:
                    lh = h.tz_convert(TZ)
                    lam = cell[(y, m, lh.day_name(), lh.hour)]
                    st, a5 = share(lam, mu, th, 4)
                    num += lam * st
                    den += lam * (1 - a5)
                    h += pd.Timedelta(hours=1)
            d += pd.Timedelta(days=1)
        out[(y, m)] = num / den
    return out


def winding(lon, lat, ring):
    wn = 0
    for (x1, y1), (x2, y2) in zip(ring[:-1], ring[1:]):
        cross = (x2 - x1) * (lat - y1) - (lon - x1) * (y2 - y1)
        if y1 <= lat < y2 and cross > 0:
            wn += 1
        elif y2 <= lat < y1 and cross < 0:
            wn -= 1
    return wn != 0


def ask_a(t, df):
    gj = json.load(open(os.path.join(t, GEOJ)))
    polys = gj["features"][0]["geometry"]["coordinates"]
    inside = lambda lon, lat: any(winding(lon, lat, p[0]) and not any(winding(lon, lat, h) for h in p[1:]) for p in polys)
    che = pd.read_csv(os.path.join(t, CHE))
    hand = che[che["method"] != "cell"].sort_values(["call_id", "seq"]).groupby("call_id").last()
    uris = pd.read_csv(os.path.join(t, DIRC))
    wex = set(uris[uris["agency"] == "Wexley County Emergency Communications"]["uri"])
    w = df[(df["service"] == "wireless") & df["id"].isin(hand.index)].copy()
    w["local"] = w["presented"].dt.tz_convert(TZ)
    w = w[(w["local"] >= pd.Timestamp("2025-07-01", tz=TZ)) & (w["local"] < pd.Timestamp("2026-07-01", tz=TZ))]
    w["in"] = [inside(hand.loc[i, "longitude"], hand.loc[i, "latitude"]) for i in w["id"]]
    w = w[w["in"]]
    q = ((w["local"].dt.month - 7) % 12) // 3 + 1
    out = {}
    for k in (1, 2, 3, 4):
        s = w[q == k]
        out["Q%d" % k] = (len(s), int(s["xfer_to"].isin(wex).sum()))
    return out


def ask_b(t, df):
    cb = pd.read_csv(os.path.join(t, CB), dtype=str, keep_default_na=False)
    cb = cb[cb["line"] == "911"].copy()
    cb["num"] = cb["callback_number"].str.lower()
    cb["created_t"] = pd.to_datetime(cb["created"]).dt.tz_localize(TZ).dt.tz_convert("UTC")
    cb["first_t"] = pd.to_datetime(cb["first_dial"].where(cb["first_dial"] != "", None)).dt.tz_localize(TZ).dt.tz_convert("UTC")
    groups = {k: g for k, g in cb.groupby("num")}
    ab = df[df["abandoned"]].copy()
    ab["hl"] = ab["ended"].dt.tz_convert(TZ)
    ab = ab[(ab["hl"] >= pd.Timestamp("2026-01-01", tz=TZ)) & (ab["hl"] < pd.Timestamp("2026-07-01", tz=TZ))]
    res = {}
    for _, r in ab.iterrows():
        key = (r["hl"].year, r["hl"].month)
        g = groups.get(r["cbn"])
        ok = False
        if g is not None:
            c = g[(g["created_t"] <= r["ended"] + pd.Timedelta(seconds=30)) & (g["first_t"] >= r["ended"])]
            if len(c):
                ok = (c["first_t"].min() - r["ended"]).total_seconds() <= 120.0
        n, d = res.get(key, (0, 0))
        res[key] = (n + ok, d + 1)
    return {"%d-%02d" % k: round(100 * n / d, 1) for k, (n, d) in sorted(res.items())}


def main(target, golden):
    df = load_calls(target)
    ans = ~df["abandoned"]
    busy = df.loc[ans, "busy"].mean()
    pat = df["wait"].sum() / df["abandoned"].sum()
    g = fy2028(target, busy, pat)
    gold = {k: int(math.floor(100 * v + 0.5)) for k, v in g.items()}
    short = [k for k, v in sorted(g.items()) if v < 0.90]
    A = ask_a(target, df)
    Bv = ask_b(target, df)
    # the goldens
    book = pd.read_excel(os.path.join(golden, "late_shift_staffing_fy2028.xlsx"), sheet_name=None)
    m = book["FY2028 late shift"].iloc[:12]
    gm = dict(zip(m["Month"], m["Expected compliance (%)"]))
    names = {7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December", 1: "January",
             2: "February", 3: "March", 4: "April", 5: "May", 6: "June"}
    ok_main = all(int(gm["%s %d" % (names[mm], yy)]) == gold[(yy, mm)] for yy, mm in gold)
    h = book["Halvorsen FY2026"].iloc[:4]
    ok_a = [tuple(int(x) for x in h.iloc[k, 1:3]) for k in range(4)] == [A["Q%d" % q] for q in (1, 2, 3, 4)]
    cbk = book["Callbacks Jan-Jun 2026"].iloc[:6]
    ok_b = [round(float(x), 1) for x in cbk["Share (%)"]] == list(Bv.values())
    print("verify: busy %.2f s, patience %.2f s; fiscal 2028 %s; below 90: %s" % (
        busy, pat, " ".join("%d" % gold[k] for k in sorted(gold, key=lambda k: (k[0], k[1]))),
        ", ".join("%d-%02d" % k for k in short)))
    print("verify: Halvorsen %s; callbacks %s" % (A, Bv))
    if not (ok_main and ok_a and ok_b and short == [(2027, 7), (2027, 8), (2028, 6)]):
        raise SystemExit("verify failed: main %s, ask A %s, ask B %s, short %s" % (ok_main, ok_a, ok_b, short))
    print("verify: every graded figure recomputes from the bundle and matches the goldens")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target"),
         sys.argv[2] if len(sys.argv) > 2 else os.path.join(task, "golden"))
