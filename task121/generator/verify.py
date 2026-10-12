"""The independent verifier. It reads only the files under target/ and imports nothing from the generator: the
complaint export cleaned to the district's complaints and odor events, the station's 5-minute records averaged to
hours without the maintenance log's held-vane periods, the upwind check from each household's geocode, each
facility's events against the same clock hour on the season's other days, the complaints by month and the
station's usable and calm hours.

    python3 task121/generator/verify.py [target_dir]
"""
import datetime as dt
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from openpyxl import load_workbook

LA = ZoneInfo("America/Los_Angeles")
S0, S1 = dt.date(2026, 5, 1), dt.date(2026, 9, 30)


def find(target, prefix):
    return os.path.join(target, next(f for f in sorted(os.listdir(target)) if f.startswith(prefix)))


def key(addr):
    a = re.sub(r"\s+", " ", addr.upper().strip())
    a = re.sub(r"\b(?:APT|UNIT)\b\s*|#\s*", "#", a)
    a = re.sub(r"\bSTREET\b", "ST", a)
    a = re.sub(r"\bAVENUE\b", "AVE", a)
    a = re.sub(r"\bDRIVE\b", "DR", a)
    a = re.sub(r"\bROAD\b", "RD", a)
    a = re.sub(r"\s*#", " #", a)
    return a


def inside(lat, lon, ring):
    xs, ys = np.array([p[0] for p in ring]), np.array([p[1] for p in ring])
    c = False
    j = len(ring) - 1
    for i in range(len(ring)):
        if (ys[i] > lat) != (ys[j] > lat):
            if lon < (xs[j] - xs[i]) * (lat - ys[i]) / (ys[j] - ys[i]) + xs[i]:
                c = not c
        j = i
    return c


def complaints(target):
    df = pd.read_csv(find(target, "odor_complaints_export"), dtype=str, keep_default_na=False)
    df["rec"] = pd.to_datetime(df.received)
    df["notc"] = pd.to_datetime(df.noticed)
    ring = json.load(open(find(target, "ukvaqmd_boundary")))["features"][0]["geometry"]["coordinates"][0]
    df["inside"] = [inside(float(a), float(b), ring) for a, b in zip(df.latitude, df.longitude)]
    df = df[df.inside].copy()
    # the app wrote UTC with no offset until its 30 April release: the noticed time falls after the received time
    utc = (df.channel == "App") & (df.notc > df.rec)
    local = [pd.Timestamp(t).tz_localize("UTC").tz_convert(LA).tz_localize(None) if u else t
             for t, u in zip(df.notc, utc)]
    df["local"] = local
    # carried over from the retired system on 6 January: noticed in 2025
    ocs = pd.read_csv(find(target, "ocs_open_complaints"), dtype=str)
    carried = {(key(a), t.strip().lower()) for a, t in zip(ocs.location, ocs.complaint_text)}
    df["hh"] = df.address.map(key)
    imp = [(h, d.strip().lower()) in carried and r.date() == dt.date(2026, 1, 6)
           for h, d, r in zip(df.hh, df.description, df.rec)]
    df.loc[imp, "local"] = pd.NaT
    # one person's report once: the app's resend repeats the household and time noticed with its saved draft
    df = df.sort_values(["rec", "complaint_no"])
    keep = []
    texts = {}
    for i, r in df.iterrows():
        k = (r.hh, r.noticed)
        t = r.description.strip().lower()
        if k in texts and any(t in x for x in texts[k]):
            continue
        texts.setdefault(k, []).append(t)
        keep.append(i)
    return df.loc[keep].copy()


def events(df):
    s = df[df.local.notna()].copy()
    s = s[(s.local.dt.date >= S0) & (s.local.dt.date <= S1)].sort_values(["hh", "local"])
    out = []
    for hh, g in s.groupby("hh", sort=False):
        first = None
        for _, r in g.iterrows():
            if first is None or (r.local - first) > pd.Timedelta(hours=2):
                first = r.local
                out.append(dict(hh=hh, t=r.local, lat=float(r.latitude), lon=float(r.longitude)))
    return out


def held_periods(target):
    m = pd.read_csv(find(target, "hfs_station_maintenance_log"), dtype=str, keep_default_na=False)
    spans, start = [], None
    for _, r in m.iterrows():
        w = r.work.lower()
        if "held" in w and r.start_pst and r.end_pst:
            spans.append((pd.Timestamp(r.date + " " + r.start_pst), pd.Timestamp(r.date + " " + r.end_pst)))
        elif "unplugged" in w:
            start = pd.Timestamp(r.date + " " + r.start_pst)
        elif "connected" in w and start is not None:
            spans.append((start, pd.Timestamp(r.date + " " + r.end_pst)))
            start = None
    return spans


def winds(target, honour_log=True):
    df = pd.read_csv(find(target, "hfs_met_5min"))
    df["t"] = pd.to_datetime(df.datetime_pst)
    ok = df.qc == "V"
    if honour_log:
        for a, b in held_periods(target):
            ok &= ~((df.t >= a) & (df.t < b))
    d = df[ok].copy()
    d["hour"] = d.t.dt.floor("h")
    rad = np.deg2rad(d.wd_deg)
    d["u"] = -d.ws_ms * np.sin(rad)
    d["v"] = -d.ws_ms * np.cos(rad)
    g = d.groupby("hour").agg(u=("u", "mean"), v=("v", "mean"), n=("u", "size"))
    g = g[g.n >= 9]
    g["sp"] = np.hypot(g.u, g.v)
    g["dir"] = (np.rad2deg(np.arctan2(-g.u, -g.v)) + 360) % 360
    allh = pd.date_range(df.t.min().floor("h"), df.t.max().floor("h"), freq="h")
    return {h: ((r.sp, r.dir) if not np.isnan(r.sp) else None) for h, r in g.reindex(allh).iterrows()}


def bearing(lat1, lon1, lat2, lon2):
    f1, f2, dl = np.radians(lat1), np.radians(lat2), np.radians(lon2 - lon1)
    y = np.sin(dl) * np.cos(f2)
    x = np.cos(f1) * np.sin(f2) - np.sin(f1) * np.cos(f2) * np.cos(dl)
    return (np.degrees(np.arctan2(y, x)) + 360) % 360


def facilities(target):
    wb = load_workbook(find(target, "odor_source_list"), read_only=True, data_only=True)
    rows = list(wb["Odor sources"].iter_rows(values_only=True))
    h = list(rows[0])
    return {r[h.index("Facility")]: (float(r[h.index("Latitude")]), float(r[h.index("Longitude")])) for r in rows[1:]}


def up(w, b):
    if w is None or w[0] < 0.5:
        return 0
    return int(abs((w[1] - b + 180) % 360 - 180) <= 30)


def to_station(t):
    return pd.Timestamp(t).tz_localize(LA).tz_convert("Etc/GMT+8").tz_localize(None)


def compare(evs, W, fac):
    """Each event against the same local clock hour on the season's other local days, read at the station's hour."""
    days = pd.date_range(str(S0), str(S1), freq="D")
    O = {f: 0 for f in fac}
    E = {f: 0.0 for f in fac}
    at = {h: [to_station(d + pd.Timedelta(hours=h)) for d in days] for h in range(24)}
    for e in evs:
        t = pd.Timestamp(e["t"])
        pst = to_station(t.floor("h"))
        ref = [W.get(s) for d, s in zip(days, at[t.hour]) if d.date() != t.date()]
        ref = [x for x in ref if x is not None]
        for f, (la, lo) in fac.items():
            b = bearing(e["lat"], e["lon"], la, lo)
            O[f] += up(W.get(pst), b)
            E[f] += sum(up(x, b) for x in ref) / len(ref)
    return O, E


def months(df):
    s = df[df.local.notna()]
    s = s[(s.local >= "2026-01-01") & (s.local < "2026-10-01")]
    return [int((s.local.dt.month == m).sum()) for m in range(1, 10)]


def station_hours(W):
    use = {m: 0 for m in range(5, 10)}
    calm = {m: 0 for m in range(5, 10)}
    for h, w in W.items():
        loc = h.tz_localize("Etc/GMT+8").tz_convert(LA)
        if loc.year == 2026 and 5 <= loc.month <= 9 and w is not None:
            use[loc.month] += 1
            calm[loc.month] += int(w[0] < 0.5)
    return [use[m] for m in range(5, 10)], [calm[m] for m in range(5, 10)]


def run(target):
    df = complaints(target)
    evs = events(df)
    W = winds(target)
    fac = facilities(target)
    O, E = compare(evs, W, fac)
    X = {f: O[f] - E[f] for f in fac}
    order = sorted(fac, key=lambda f: -X[f])
    u, c = station_hours(W)
    return dict(n=len(evs), O=O, E=E, X=X, call=order[0], rival=order[1], months=months(df), usable=u, calm=c)


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                            "target")
    v = run(tgt)
    print("odor events May to September 2026: %d" % v["n"])
    for f in v["O"]:
        print("  %-48s upwind %4d  expected %6.1f  beyond %6.1f" % (f, v["O"][f], v["E"][f], v["X"][f]))
    print("behind the surge: %s; closest: %s" % (v["call"], v["rival"]))
    print("complaints by month (January to September):", v["months"])
    print("usable hours (May to September):", v["usable"], "calm hours:", v["calm"])
