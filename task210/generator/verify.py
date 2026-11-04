"""task210's independent verifier: reads only the shipped bundle (target/, prompt.txt) and figures.json, and recomputes
every graded answer by its own route, sharing no code with the generator's golden.

    python3 task210/generator/verify.py          # exit 1 on any mismatch

Main call: the sun's position from the Astronomical Almanac's low-precision formulae (golden.py uses NOAA's General
Solar Position), firm brakes attached to the logging car's pass by time alone, the hourly sky report floored to its
clock hour, the pick timetable read with pypdf (golden.py uses pdfplumber), the glare multiplier profiled by a grid
and Brent's method, and the four highest expected rates on the pick's weekday-peak passes at the normals' sunshine.
Asks: recomputed by ceiling.py's own routes, which read target/ and share no code with the generator.
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from pypdf import PdfReader
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
TZ = "America/Denver"
BAD = []


def say(name, ok, detail=""):
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail), flush=True)
    if not ok:
        BAD.append(name)


def sun(t_utc, lat, lon):
    """Elevation and azimuth (degrees, azimuth clockwise from north): Astronomical Almanac low-precision formulae."""
    t = pd.DatetimeIndex(t_utc)
    jd = t.to_julian_date().values
    n = jd - 2451545.0
    L = np.radians((280.460 + 0.9856474 * n) % 360)
    g = np.radians((357.528 + 0.9856003 * n) % 360)
    lam = L + np.radians(1.915) * np.sin(g) + np.radians(0.020) * np.sin(2 * g)
    eps = np.radians(23.439 - 0.0000004 * n)
    ra = np.arctan2(np.cos(eps) * np.sin(lam), np.cos(lam))
    dec = np.arcsin(np.sin(eps) * np.sin(lam))
    gmst = (18.697374558 + 24.06570982441908 * n) % 24
    ha = np.radians(((gmst + lon / 15.0) * 15.0) % 360) - ra
    phi = np.radians(lat)
    el = np.arcsin(np.sin(phi) * np.sin(dec) + np.cos(phi) * np.cos(dec) * np.cos(ha))
    az = np.arctan2(-np.sin(ha), np.tan(dec) * np.cos(phi) - np.sin(phi) * np.cos(ha))
    return np.degrees(el), np.degrees(az) % 360


def to_utc(local):
    return pd.DatetimeIndex(local).tz_localize(TZ, ambiguous=True, nonexistent="shift_forward").tz_convert("UTC").tz_localize(None)


def glare(el, az, brg):
    off = np.abs(((az - brg + 180.0) % 360.0) - 180.0)
    a = np.where(off < 25.0, np.cos(np.pi / 2 * off / 25.0) ** 2, 0.0)
    h = np.where(el <= 0, 0.0, np.where(el <= 12.0, 1.0, np.clip((25.0 - el) / 13.0, 0, 1)))
    return a * h


def network():
    g = json.load(open(os.path.join(T, "streetcar_track_survey_2025.geojson")))
    rows = []
    for f in g["features"]:
        if f["geometry"]["type"] == "LineString":
            (x1, y1), (x2, y2) = f["geometry"]["coordinates"][0], f["geometry"]["coordinates"][-1]
            rows.append((f["properties"]["section_id"], x1, y1, x2, y2))
    s = pd.DataFrame(rows, columns=["section", "lon1", "lat1", "lon2", "lat2"])
    lat0, lon0 = s[["lat1", "lat2"]].values.mean(), s[["lon1", "lon2"]].values.mean()
    s["brg"] = np.degrees(np.arctan2((s["lon2"] - s["lon1"]) * np.cos(np.radians(lat0)), s["lat2"] - s["lat1"])) % 360
    return s.set_index("section")["brg"], lat0, lon0


def weekday_days(A):
    first = A.groupby("service_date")["enter_local"].min()
    return {d for d, t in first.items() if pd.Timestamp(d).weekday() < 5 and t.hour < 7}


def record(brg, lat, lon):
    A = pd.read_parquet(os.path.join(T, "avl_section_passes_2026.parquet"))
    A["section_id"] = A["section_id"].astype(str)
    A["d"] = np.where(A["direction"].astype(str) == "OB", "O", "I")
    A["sd"] = A["section_id"] + "-" + A["d"]
    A["brg"] = A["section_id"].map(brg) + np.where(A["d"] == "O", 0.0, 180.0)
    A["brg"] = A["brg"] % 360
    mid = A["enter_local"] + (A["exit_local"] - A["enter_local"]) / 2
    A["el"], A["az"] = sun(to_utc(mid.dt.round("s")), lat, lon)
    A["hour"] = A["enter_local"].dt.hour
    wk = weekday_days(A)
    A["wkend"] = (~A["service_date"].isin(wk)).astype(float)
    A["vehicle"] = A["vehicle"].astype("int64")
    A = A.sort_values("enter_local").reset_index(drop=True)
    E = pd.read_csv(os.path.join(T, "edr_event_export_2026-04-01_2026-10-31.csv"))
    E = E[E["event_code"] == "FB"].copy()
    E["t"] = pd.to_datetime(E["event_time_utc"], utc=True).dt.tz_convert(TZ).dt.tz_localize(None).astype("datetime64[ns]")
    E["car"] = E["car"].astype("int64")
    A["enter_ns"] = A["enter_local"].astype("datetime64[ns]")
    A["exit_ns"] = A["exit_local"].astype("datetime64[ns]")
    x = pd.merge_asof(E.sort_values("t"), A[["enter_ns", "exit_ns", "vehicle"]].reset_index(), left_on="t",
                      right_on="enter_ns", left_by="car", right_by="vehicle", direction="backward")
    x = x[x["t"] <= x["exit_ns"] + pd.Timedelta(seconds=20)]
    A["fb"] = A.index.map(x["index"].value_counts()).fillna(0).astype(int)
    M = pd.read_csv(os.path.join(T, "ash_awos_hourly_obs_2026.csv"))
    M["t"] = pd.to_datetime(M["valid_utc"], utc=True).dt.tz_convert(TZ).dt.tz_localize(None).dt.floor("h")
    M["s"] = M["skyc"].astype(str).str[:3].isin(["CLR", "FEW", "SCT"]).astype(float)
    hs = M.drop_duplicates("t").set_index("t")["s"]
    A["sun"] = A["enter_ns"].dt.floor("h").map(hs)
    near = pd.merge_asof(A[["enter_ns"]].reset_index(), M[["t", "s"]].sort_values("t").astype({"t": "datetime64[ns]"}),
                         left_on="enter_ns", right_on="t", direction="nearest").set_index("index")["s"]
    A["sun"] = A["sun"].fillna(near).fillna(0.0)
    return A


def fit(A):
    d = pd.DataFrame({"sd": A["sd"], "hour": A["hour"], "wkend": A["wkend"], "dark": (A["el"] < 0).astype(float),
                      "y": A["fb"], "gs": glare(A["el"].values, A["az"].values, A["brg"].values) * A["sun"].values})
    c = d.groupby(["sd", "hour", "wkend", "dark"], as_index=False).agg(y=("y", "sum"), n=("y", "size"), s=("gs", "sum"))
    X = pd.concat([pd.get_dummies(c["sd"], prefix="sd").astype(float),
                   pd.get_dummies(c["hour"].astype(str), prefix="h", drop_first=True).astype(float), c[["wkend", "dark"]]], axis=1)

    def nll(G):
        return -sm.GLM(c["y"].values, X.values, family=sm.families.Poisson(), offset=np.log(c["n"].values + G * c["s"].values)).fit().llf

    grid = np.arange(0.0, 5.01, 0.25)
    g0 = grid[int(np.argmin([nll(g) for g in grid]))]
    G = minimize_scalar(nll, bracket=(max(g0 - 0.25, 0.0), g0, g0 + 0.25), method="brent", tol=1e-4).x
    m = sm.GLM(c["y"].values, X.values, family=sm.families.Poisson(), offset=np.log(c["n"].values + G * c["s"].values)).fit()
    return dict(zip(X.columns, m.params)), G


def pick(brg, lat, lon):
    txt = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "january_2027_pick_timetable.pdf")).pages)
    txt = re.sub(r"\s+", " ", txt)
    spans = [(int(a[:2]) * 60 + int(a[3:]), int(b[:2]) * 60 + int(b[3:]), float(h))
             for a, b, h in re.findall(r"Weekday (\d\d:\d\d) to (\d\d:\d\d) every ([\d.]+) min", txt)]
    run = {s: (int(o), int(i)) for s, o, i in
           re.findall(r"(?:Juniper|Foundry) Line ([JF]\d) .*? (\d+) (\d+)(?= (?:Juniper|Foundry) Line| ?$)", txt)}
    m = re.search(r"Monday (\d+) January to Friday (\d+) February (\d{4})", txt)
    days = pd.date_range("%s-01-%02d" % (m.group(3), int(m.group(1))), "%s-02-%02d" % (m.group(3), int(m.group(2))))
    hol = re.findall(r"Monday (\d+) (January|February) 2027", txt.split("Holidays in this pick")[1][:160])
    hol = {pd.Timestamp("%s %s 2027" % (a, b)) for a, b in hol}
    days = [d for d in days if d.weekday() < 5 and d not in hol]
    rows = []
    for line in ("J", "F"):
        secs = sorted([s for s in run if s[0] == line], key=lambda s: int(s[1:]))
        for dn, order in (("O", secs), ("I", secs[::-1])):
            for a, b, h in spans:
                t = a * 60.0
                while t < b * 60 - 1e-9:
                    cum = t
                    for s in order:
                        rt = run[s][0 if dn == "O" else 1]
                        rows.append((s, dn, cum, cum + rt))
                        cum += rt
                    t += h * 60
    base = pd.DataFrame(rows, columns=["s", "d", "a", "b"])
    X = pd.concat([base.assign(day=d) for d in days], ignore_index=True)
    X["enter"] = X["day"] + pd.to_timedelta(X["a"], unit="s")
    mm = X["enter"].dt.hour * 60 + X["enter"].dt.minute
    X["peak"] = np.where((mm >= 390) & (mm < 540), "AM", np.where((mm >= 960) & (mm < 1110), "PM", ""))
    X = X[X["peak"] != ""].reset_index(drop=True)
    mid = X["day"] + pd.to_timedelta((X["a"] + X["b"]) / 2, unit="s")
    X["el"], X["az"] = sun(to_utc(mid.dt.round("s")), lat, lon)
    X["sd"] = X["s"] + "-" + X["d"]
    X["brg"] = (X["s"].map(brg) + np.where(X["d"] == "O", 0.0, 180.0)) % 360
    X["hour"] = X["enter"].dt.hour
    return X


def main():
    fj = json.load(open(os.path.join(HERE, "figures.json")))
    brg, lat, lon = network()
    A = record(brg, lat, lon)
    coef, G = fit(A)
    X = pick(brg, lat, lon)
    txt = PdfReader(os.path.join(T, "ash_climate_normals_1991-2020.pdf")).pages[0].extract_text()
    ps = [int(v) / 100 for v in re.search(r"Possible sunshine, %\s*((?:\d+\s*){12})", txt).group(1).split()]
    psun = X["enter"].dt.month.map(lambda m: ps[m - 1]).values
    lin = np.array([coef["sd_" + s] for s in X["sd"]]) + np.array([coef.get("h_%d" % h, 0.0) for h in X["hour"]])
    lin = lin + coef["dark"] * (X["el"].values < 0)
    r = pd.Series(np.exp(lin) * (1 + G * glare(X["el"].values, X["az"].values, X["brg"].values) * psun) * 1000)
    r = r.groupby([X["sd"].values, X["peak"].values]).mean().sort_values(ascending=False)
    sl = sorted("%s %s" % k for k in r.index[:4])
    say("main call: the four slots recompute", sl == fj["slate"], str(sl))
    sep = 100 * (r.iloc[3] / r.iloc[4] - 1)
    say("main call: the fourth slot clears the fifth by 10 per cent or more", sep >= 10, "%.1f per cent, G %.3f" % (sep, G))
    csv = pd.read_csv(os.path.join(TASK, "golden", "slot_plan_jan_feb_2027.csv"))
    on = {"%s-%s %s" % (a, "O" if b == "outbound" else "I", c)
          for a, b, c, v in zip(csv["section_id"], csv["direction"], csv["peak"], csv["restricted_speed_slot"]) if v == "yes"}
    say("slot_plan_jan_feb_2027.csv marks exactly the slate (52 rows)", on == set(sl) and len(csv) == 52)
    sys.path.insert(0, HERE)
    import ceiling
    a = ceiling.ask_a(T, "operating", window=360, metres=80)
    want_a = [fj["ask_a"][k] for k in sorted(fj["ask_a"], key=lambda k: (k.split()[0] != "Juniper", k))]
    say("ask A recomputes (14 figures)", a == want_a, str(a))
    b = ceiling.ask_b(T, "block")
    want_b = [fj["ask_b"][ln][g] for ln in ("Juniper", "Foundry") for g in ("Brakes", "Doors", "All other")]
    say("ask B recomputes (6 figures)", b == want_b, str(b))
    files = sorted(os.listdir(T))
    say("input gates: 10 or more files, 3 or more formats", len(files) >= 10 and len({os.path.splitext(f)[1] for f in files}) >= 3,
        "%d files" % len(files))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    say("distractors named in metadata.json exist", all(d in files for d in meta["distractors"]) and len(meta["distractors"]) >= 2)
    p = open(os.path.join(TASK, "prompt.txt")).read()
    say("the prompt names both deliverables", "slot_plan_jan_feb_2027.csv" in p and "braking_shift.png" in p)
    print("VERIFY %s (%d failed)" % ("PASS" if not BAD else "FAIL", len(BAD)))
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
