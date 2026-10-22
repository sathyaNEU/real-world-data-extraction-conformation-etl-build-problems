"""The analyst's side: reads task478's cut pack (never world.py) and computes the call and the asks by every route the
design names. Used by golden.py, checks.py and ceiling.py."""
import csv
import datetime as dt
import os

import numpy as np
import openpyxl
import pandas as pd

LIMIT = 80000
KG = 0.45359237
# the program's section table (section 1): code, name, milepost from, milepost to
SECTIONS = [("01", "Ashford Gap", 0.0, 21.6), ("02", "Brannock", 21.6, 44.9), ("03", "Cole Hollow", 44.9, 63.2),
            ("04", "Dunmere", 63.2, 88.7), ("05", "Elk Ferry", 88.7, 109.4), ("06", "Foxbriar", 109.4, 131.0),
            ("07", "Garnet Ridge", 131.0, 152.8), ("08", "Halbrook", 152.8, 178.3),
            ("09", "Ingram Mill", 178.3, 203.5), ("10", "Jessup Fork", 203.5, 229.0),
            ("11", "Kettle Run", 229.0, 256.2), ("12", "Lowfield", 256.2, 284.0)]
CODES = [s[0] for s in SECTIONS]
NAMES = {s[0]: s[1] for s in SECTIONS}
WEEKDAYS_2026 = 261


def section_at(mp):
    for c, n, a, b in SECTIONS:
        if a <= mp < b:
            return c
    raise ValueError(mp)


def files(folder):
    import pack as P
    return {k: os.path.join(folder, v) for k, v in P.FILES.items()}


def read_piezo(path):
    """Fixed-width records: station 1-4, direction 5, lane 6, date 7-14, time 15-22 (hundredths), speed 23-26 (tenths of
    mph), class 27-28, axles 29-30, gross 31-35 (tens of lb), nine axle weights of four (tens of lb), eight spacings of
    three (tenths of ft), flag 96."""
    rows = []
    with open(path, encoding="ascii") as fh:
        for ln in fh:
            n = int(ln[28:30])
            rows.append((ln[0:4].strip(), ln[4], int(ln[5]), ln[6:14] + ln[14:20], int(ln[22:26]) / 10.0,
                         int(ln[26:28]), n, int(ln[30:35]) * 10, int(ln[35:39]) * 10, int(ln[95])))
    df = pd.DataFrame(rows, columns=["station", "dir", "lane", "stamp", "speed_mph", "cls", "axles", "gross",
                                     "steer", "rejected"])
    df["local"] = pd.to_datetime(df.pop("stamp"), format="%Y%m%d%H%M%S")
    return df


def read_bending(path):
    df = pd.read_csv(path, dtype={"site": str})
    out = pd.DataFrame({"station": df["site"], "dir": df["dir"].str[0], "lane": df["lane"],
                        "local": pd.to_datetime(df["local_time"]), "speed_mph": df["speed_kph"] / 1.609344,
                        "cls": df["fhwa_class"], "axles": df["axles"], "gross": df["gvw_kg"] / KG,
                        "steer": df["ax1_kg"] / KG, "rejected": (df["status"] == "REJ").astype(int)})
    return out


def read_wim(folder):
    f = files(folder)
    pz = read_piezo(f["piezo"])
    bp = read_bending(f["bending"])
    st = pd.read_csv(f["stations"], dtype={"station_id": str})
    sec = {r.station_id: section_at(float(r.milepost)) for r in st.itertuples()}
    df = pd.concat([pz, bp], ignore_index=True)
    df["section"] = df["station"].map(sec)
    return df


def read_tickets(folder):
    ws = openpyxl.load_workbook(files(folder)["tickets"], read_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df


def class9(df, line=None):
    return df[(df["cls"] == 9) & (df["rejected"] == 0)]


def shares(df, factors=None):
    out = {}
    for c in CODES:
        d = df[df["section"] == c]
        f = 1.0 if factors is None else factors[c]
        out[c] = 100.0 * float(np.mean(d["gross"].to_numpy() / f > LIMIT))
    return out


def factors(df, tk, how="loaded", line=50000, agg="median", ragg="median"):
    """Each station's calibration against the scale houses' tickets, read on the steer axle (or the gross peaks)."""
    a = {"median": np.median, "mean": np.mean}[agg]
    ra = {"median": np.median, "mean": np.mean}[ragg]
    tsteer = tk["Axle 1 (lb)"].astype(float).to_numpy()
    tgross = (tk[["Axle %d (lb)" % i for i in range(1, 6)]].astype(float).sum(axis=1)).to_numpy()
    out = {}
    for c in CODES:
        d = df[df["section"] == c]
        g = d["gross"].to_numpy()
        s = d["steer"].to_numpy()
        if how == "loaded":
            out[c] = a(s[g > line]) / ra(tsteer[tgross > line])
        elif how == "pooled":
            out[c] = a(s) / ra(tsteer)
        elif how == "empty":
            out[c] = a(s[g <= line]) / ra(tsteer[tgross <= line])
        elif how == "gross":
            out[c] = a(g) / ra(tgross)
        elif how == "empty_peak":
            out[c] = _mode(g, 20000, 45000) / _mode(tgross, 20000, 45000)
    return out


def _mode(x, lo, hi):
    h, ed = np.histogram(x[(x > lo) & (x < hi)], bins=np.arange(lo, hi + 1, 1000))
    return ed[int(np.argmax(h))] + 500


def five(sh):
    return sorted(sorted(sh, key=lambda c: -sh[c])[:5])


def hround(x):
    return int(np.floor(x + 0.5))


# ------------------------------------------------------------------ the asks
def read_entries(folder):
    df = pd.read_csv(files(folder)["entries"], dtype={"txn_id": str, "tag_id": str})
    df["stamp"] = pd.to_datetime(df["entry_utc"], format="mixed")
    df["old"] = ~df["txn_id"].str.startswith("T26")
    return df


def eastern_offset(d):
    m3 = dt.date(d.year, 3, 8)
    start = m3 + dt.timedelta(days=(6 - m3.weekday()) % 7)
    n1 = dt.date(d.year, 11, 1)
    end = n1 + dt.timedelta(days=(6 - n1.weekday()) % 7)
    return 4 if start <= d < end else 5


def to_local(utc):
    off = utc.dt.date.map(eastern_offset)
    loc = utc - pd.to_timedelta(off, unit="h")
    # a UTC date's offset can differ from its local date's only in the hours of a change night; recheck there
    off2 = loc.dt.date.map(eastern_offset)
    return utc - pd.to_timedelta(off2, unit="h")


def _twins(old, new, lo, hi):
    """New-host rows with an old-host row of the same tag and plaza stamped between lo and hi seconds after them."""
    o = old[["tag_id", "plaza", "stamp"]].rename(columns={"stamp": "s_old"})
    m = new[["tag_id", "plaza", "stamp"]].reset_index().merge(o, on=["tag_id", "plaza"])
    d = (m["s_old"] - m["stamp"]).dt.total_seconds()
    return set(m.loc[(d >= lo) & (d <= hi), "index"])


def entries_clean(folder, dedup="golden", clock="golden"):
    """The year's entries once each, on local time. Golden: an old-host row is the old host's local receipt stamp; a
    new-host row stamped up to 16 minutes before (or within the minute after) an old-host row of the same tag and plaza
    is the new host's backfill
    of it and goes; every other new-host row is a UTC stamp of the new host's own."""
    df = read_entries(folder)
    old, new = df[df["old"]], df[~df["old"]]
    if dedup == "golden":
        drop = _twins(old, new, -60, 16 * 60)
    elif dedup == "pair60":
        drop = _twins(old, new, -60, 60)
    elif dedup == "exact":
        drop = set(new.index[new.set_index(["tag_id", "plaza", "stamp"]).index.isin(
            old.set_index(["tag_id", "plaza", "stamp"]).index)])
    elif dedup == "cut_first":
        first = new["stamp"].min()
        drop = set(old.index[old["stamp"] >= first]) | set(new.index[new["stamp"] < first])
    elif dedup == "cut_last":
        last = old["stamp"].max()
        drop = set(new.index[new["stamp"] <= last])
    else:
        drop = set()
    df = df.drop(index=sorted(drop))
    if clock == "golden":
        df["local"] = df["stamp"].where(df["old"], to_local(df["stamp"]))
    elif clock == "utc":
        df["local"] = to_local(df["stamp"])
    else:
        df["local"] = df["stamp"]
    df["date"] = df["local"].dt.date
    if dedup == "sameday":
        df = df.drop_duplicates(["tag_id", "plaza", "date"])
    return df


def plaza_section(folder, how="dated"):
    """plaza code and local date -> section; 'dated' honours the plaza list's in-service dates and reads a code before
    its date from the 2025 toll schedule; 'current' maps every row by the list as it stands."""
    pl = pd.read_csv(files(folder)["plazas"])
    cur = {r.plaza: (section_at(float(r.milepost)), r.in_service_from) for r in pl.itertuples()}
    old = {"P23": "02"}          # the 2025 toll schedule: P23 is Brannock Road, milepost 38.1

    def f(code, d):
        sec, since = cur[code]
        if how == "dated" and isinstance(since, str) and since and d < dt.date.fromisoformat(since):
            return old.get(code)
        return sec
    return f


def weekday_entries(folder, dedup="golden", clock="golden", plazas="dated"):
    df = entries_clean(folder, dedup, clock)
    ps = plaza_section(folder, plazas)
    df["section"] = [ps(p, d) for p, d in zip(df["plaza"], df["date"])]
    wk = df[np.array([d.weekday() < 5 for d in df["date"]]) & (df["local"].dt.year == 2026).to_numpy()]
    cnt = wk.groupby("section").size()
    return {c: float(cnt.get(c, 0)) / WEEKDAYS_2026 for c in CODES}


def read_citations(folder):
    df = pd.read_csv(files(folder)["citations"], dtype={"tag_id": str})
    df["issued_local"] = pd.to_datetime(df["issued"], format="%m/%d/%Y %H:%M")
    return df


def citations_by_section(folder, how="trip", plazas="dated", dedup="golden", clock="golden"):
    """Gross-overweight citations by the section where the truck entered: 'logged' takes the log's entry plaza, 'trip'
    the tag's last entry before the stop."""
    ci = read_citations(folder)
    g = ci[ci["violation"] == "G"].copy()
    ps = plaza_section(folder, plazas)
    if how == "logged":
        secs = [ps(p, d.date()) for p, d in zip(g["entry_plaza"], g["issued_local"])]
    else:
        en = entries_clean(folder, dedup, clock)
        en = en.sort_values("local")
        by_tag = {t: v for t, v in en.groupby("tag_id")}
        secs = []
        for tag, when in zip(g["tag_id"], g["issued_local"]):
            v = by_tag[tag]
            before = v[v["local"] <= when]
            if not len(before):
                secs.append(None)
                continue
            row = before.iloc[-1]
            secs.append(ps(row["plaza"], row["date"]))
    g["section"] = secs
    cnt = g.groupby("section").size()
    return {c: int(cnt.get(c, 0)) for c in CODES}
