"""task210's golden, computed from target/ alone (the generator's truth is never read here).

Main call: firm brakes are attached to the AVL passes of the car that logged them; each pass gets the sun's position
at its midpoint against its section direction's bearing, and the airport's sky cover for that clock hour; a Poisson
model of firm brakes per pass (section-direction, hour, weekend and holiday, darkness, and the glare term
1 + G * glare * sun) is fitted to the whole record and projected onto the January 2027 pick's weekday peak passes at
the station's normal sunshine. The four section-direction peaks with the highest expected rates take the slots.
Asks: emergency applications in revenue service per line and local month (A); overspeeds of the May and August 2026
classes in each operator's first 60 days of revenue service, their revenue hours and the rate per 100 hours (B).

    python3 task210/generator/golden.py      # writes generator/figures.json and golden/
"""
import json
import os
import re
import sys
import numpy as np
import pandas as pd
import pdfplumber
import statsmodels.api as sm
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)
from solar import sun_position  # noqa: E402  (NOAA General Solar Position; verify.py uses another algorithm)

TZ = "America/Denver"
M_LAT = 111320.0
CAP = 4
F = {"edr": "edr_event_export_2026-04-01_2026-10-31.csv", "avl": "avl_section_passes_2026.parquet",
     "survey": "streetcar_track_survey_2025.geojson", "metar": "ash_awos_hourly_obs_2026.csv",
     "yard": "yard_block_sheets_2026.csv", "runs": "run_sheets_2026.csv", "roster": "operator_roster_2026.csv",
     "cards": "badge_card_register.csv", "pick": "january_2027_pick_timetable.pdf", "srm": "SRM-07_seasonal_restricted_speed_orders.pdf",
     "normals": "ash_climate_normals_1991-2020.pdf"}


def path(k, target=TARGET):
    return os.path.join(target, F[k])


def to_local(utc_strings):
    t = pd.to_datetime(utc_strings, utc=True)
    return t.dt.tz_convert(TZ).dt.tz_localize(None).astype("datetime64[ns]")


def to_utc(local):
    return pd.DatetimeIndex(local).tz_localize(TZ, ambiguous=True, nonexistent="shift_forward").tz_convert("UTC").tz_localize(None)


# ---------------------------------------------------------------- the network and the pick
def survey(target=TARGET):
    g = json.load(open(path("survey", target)))
    rows, pts = [], []
    for f in g["features"]:
        if f["geometry"]["type"] != "LineString":
            continue
        p = f["properties"]
        (lo1, la1), (lo2, la2) = f["geometry"]["coordinates"][0], f["geometry"]["coordinates"][-1]
        rows.append(dict(section=p["section_id"], line=p["line"], lon1=lo1, lat1=la1, lon2=lo2, lat2=la2,
                         from_stop=p["from_stop"], to_stop=p["to_stop"]))
        pts += [(la1, lo1), (la2, lo2)]
    s = pd.DataFrame(rows)
    lat0 = float(np.mean([a for a, _ in pts]))
    dx = (s["lon2"] - s["lon1"]) * M_LAT * np.cos(np.radians(lat0))
    dy = (s["lat2"] - s["lat1"]) * M_LAT
    s["bearing_out"] = np.degrees(np.arctan2(dx, dy)) % 360
    return s, lat0, float(np.mean([b for _, b in pts]))


def pick(target=TARGET):
    with pdfplumber.open(path("pick", target)) as pdf:
        txt = "\n".join(pg.extract_text() for pg in pdf.pages)
    spans = []
    for a, b, h in re.findall(r"^Weekday (\d\d:\d\d) to (\d\d:\d\d) every ([\d.]+) min", txt, re.M):
        hm = lambda s: int(s[:2]) * 60 + int(s[3:])
        spans.append((hm(a), hm(b), float(h)))
    run = {}
    for sec, o, i in re.findall(r"\b([JF]\d) .*? (\d+) (\d+)$", txt, re.M):
        run[sec] = (int(o), int(i))
    m = re.search(r"Pick dates: \w+ (\d+) (\w+) to \w+ (\d+) (\w+) (\d{4})", txt)
    start = pd.Timestamp(f"{m.group(1)} {m.group(2)} {m.group(5)}")
    end = pd.Timestamp(f"{m.group(3)} {m.group(4)} {m.group(5)}")
    hol = [pd.Timestamp(f"{d} {mo} {m.group(5)}") for d, mo in re.findall(r"Monday (\d+) (\w+)", txt.split("Holidays in this pick")[1][:120])]
    return dict(spans=spans, run=run, start=start, end=end, holidays=hol)


def pick_passes(sec, pk, lat, lon):
    days = [d for d in pd.date_range(pk["start"], pk["end"]) if d.weekday() < 5 and d not in pk["holidays"]]
    rows = []
    for line in ("J", "F"):
        secs = [s for s in sec["section"] if s.startswith(line)]
        for dirn, order in (("O", secs), ("I", secs[::-1])):
            for a, b, h in pk["spans"]:
                t = a * 60.0
                while t < b * 60 - 1e-9:
                    cum = t
                    for s in order:
                        rt = pk["run"][s][0 if dirn == "O" else 1]
                        rows.append((s, dirn, cum, cum + rt))
                        cum += rt
                    t += h * 60
    base = pd.DataFrame(rows, columns=["section", "dir", "a", "b"])
    out = []
    for d in days:
        x = base.copy()
        x["enter"] = d + pd.to_timedelta(x["a"], unit="s")
        x["exit"] = d + pd.to_timedelta(x["b"], unit="s")
        out.append(x)
    X = pd.concat(out, ignore_index=True)
    m = X["enter"].dt.hour * 60 + X["enter"].dt.minute
    X["peak"] = np.where((m >= 390) & (m < 540), "AM", np.where((m >= 960) & (m < 1110), "PM", "OFF"))
    X = X[X["peak"] != "OFF"].reset_index(drop=True)
    return _sun(X, sec, lat, lon)


def _sun(X, sec, lat, lon, at="mid"):
    brg = sec.set_index("section")["bearing_out"]
    X["sd"] = X["section"] + "-" + X["dir"]
    X["bearing"] = np.where(X["dir"] == "O", X["section"].map(brg), (X["section"].map(brg) + 180) % 360)
    t = X["enter"] + (X["exit"] - X["enter"]) / 2 if at == "mid" else X["enter"]
    el, az = sun_position(np.asarray(to_utc(t.dt.round("s")).values, dtype="datetime64[s]"), lat, lon)
    X["elev"], X["az"] = el, az
    X["hour"] = X["enter"].dt.hour
    return X


def glare(elev, az, bearing, cone=25.0, efull=12.0, ezero=25.0, shape="cos2"):
    off = np.abs(((az - bearing + 180.0) % 360.0) - 180.0)
    if shape == "cos2":
        a = np.where(off < cone, np.cos(np.pi / 2 * off / cone) ** 2, 0.0)
    elif shape == "lin":
        a = np.clip(1 - off / cone, 0, 1)
    else:
        a = (off < cone).astype(float)
    h = np.where(elev <= 0.0, 0.0, np.where(elev <= efull, 1.0, np.clip((ezero - elev) / max(ezero - efull, 1e-6), 0, 1)))
    return a * h


# ---------------------------------------------------------------- the observed record
def passes(target=TARGET, at="mid", sky="hour", assign="position"):
    sec, lat, lon = survey(target)
    A = pd.read_parquet(path("avl", target))
    A = A.rename(columns={"section_id": "section", "enter_local": "enter", "exit_local": "exit"})
    A["dir"] = A["direction"].astype(str).map({"OB": "O", "IB": "I"})
    A["vehicle"] = A["vehicle"].astype("int64")
    A["enter"], A["exit"] = A["enter"].astype("datetime64[ns]"), A["exit"].astype("datetime64[ns]")
    A["section"] = A["section"].astype(str)
    A["service_date"] = pd.to_datetime(A["service_date"])
    A = _sun(A, sec, lat, lon, at)
    # day type from the service actually run: the weekday timetable runs the most trips
    trips = A.groupby("service_date")["trip_id"].nunique()
    A["wkend"] = (A["service_date"].map(trips) < 0.9 * trips.max()).astype(float)
    A["pid"] = np.arange(len(A))
    # firm brakes onto the passes of the car that logged them
    E = pd.read_csv(path("edr", target))
    E = E[E["event_code"] == "FB"].copy()
    E["t"] = to_local(E["event_time_utc"]).astype("datetime64[ns]")
    E["car"] = E["car"].astype("int64")
    A["n_fb"] = _attach(A, E, sec, assign)
    # sky cover for the pass's clock hour (observations at :53 UTC each hour)
    M = pd.read_csv(path("metar", target))
    M["t"] = to_local(M["valid_utc"])
    M["sun"] = M["skyc"].astype(str).str[:3].isin(["CLR", "FEW", "SCT"]).astype(float)
    A["sun"] = _sky(A, M, sky)
    return A, sec, lat, lon


def _attach(A, E, sec, assign):
    S = sec.set_index("section")
    P = A[["pid", "vehicle", "section", "dir", "enter", "exit"]].sort_values("enter")
    E = E.sort_values("t")
    b = pd.merge_asof(E, P, left_on="t", right_on="enter", left_by="car", right_by="vehicle", direction="backward",
                      tolerance=pd.Timedelta(minutes=30))
    f = pd.merge_asof(E, P, left_on="t", right_on="enter", left_by="car", right_by="vehicle", direction="forward",
                      tolerance=pd.Timedelta(seconds=20))
    if assign == "time":
        ok = b["exit"] >= b["t"]
        pid = np.where(ok, b["pid"], f["pid"])
    else:
        def dist(df):
            s = df["section"].map(lambda v: v if isinstance(v, str) else None)
            out = np.full(len(df), np.inf)
            m = s.notna().values
            g = S.loc[s[m].values]
            x1 = (g["lon1"].values - df["lon"].values[m]) * np.cos(np.radians(df["lat"].values[m]))
            y1 = g["lat1"].values - df["lat"].values[m]
            x2 = (g["lon2"].values - df["lon"].values[m]) * np.cos(np.radians(df["lat"].values[m]))
            y2 = g["lat2"].values - df["lat"].values[m]
            dx, dy = x2 - x1, y2 - y1
            u = np.clip(-(x1 * dx + y1 * dy) / (dx * dx + dy * dy), 0, 1)
            out[m] = np.hypot(x1 + u * dx, y1 + u * dy) * M_LAT
            return out
        db = np.where((b["exit"] + pd.Timedelta(seconds=20) >= b["t"]).fillna(False).values, dist(b), np.inf)
        df_ = dist(f)
        pid = np.where(db <= df_, b["pid"], f["pid"])
        pid = np.where(np.minimum(db, df_) < 60, pid, np.nan)
    cnt = pd.Series(pid).dropna().astype(int).value_counts()
    return A["pid"].map(cnt).fillna(0).astype(int).values


def _sky(A, M, how):
    """Sun visible on each pass from the airport's hourly observation: the observation in the pass's clock hour
    (golden), the nearest observation, or the :53 observation read as the next hour's."""
    M = M.sort_values("t")
    near = pd.merge_asof(pd.DataFrame({"t": A["enter"].values, "i": np.arange(len(A))}).sort_values("t"), M[["t", "sun"]],
                         on="t", direction="nearest", tolerance=pd.Timedelta(minutes=120)).sort_values("i")["sun"].values
    if how == "nearest":
        s = pd.Series(near)
    else:
        k = M["t"].dt.floor("h") if how == "hour" else M["t"].dt.ceil("h")
        h = M.assign(k=k).drop_duplicates("k").set_index("k")["sun"]
        s = pd.Series(A["enter"].dt.floor("h").map(h).values)
        s = s.fillna(pd.Series(near))      # an hour whose observation is missing takes the nearest one
    return s.fillna(0.0).values


# ---------------------------------------------------------------- the model and the projection
def fit(A, cone=25.0, efull=12.0, ezero=25.0, shape="cos2", dark_at=0.0, controls=("wkend", "dark"), hourfe=True,
        school=None):
    d = pd.DataFrame({"sd": A["sd"].values, "hour": A["hour"].values, "wkend": A["wkend"].values,
                      "dark": (A["elev"].values < dark_at).astype(float), "y": A["n_fb"].values})
    if school is not None:
        d["school_am"] = school
    d["gs"] = glare(A["elev"].values, A["az"].values, A["bearing"].values, cone, efull, ezero, shape) * A["sun"].values
    keys = ["sd", "hour"] + list(controls)
    c = d.groupby(keys, as_index=False).agg(y=("y", "sum"), n=("y", "size"), sgs=("gs", "sum"))
    X = pd.get_dummies(c["sd"], prefix="sd").astype(float)
    if hourfe:
        X = pd.concat([X, pd.get_dummies(c["hour"].astype(str), prefix="h", drop_first=True).astype(float)], axis=1)
    for k in controls:
        X[k] = c[k].astype(float).values
    y, n, Xv = c["y"].values, c["n"].values.astype(float), X.values
    nll = lambda G: -sm.GLM(y, Xv, family=sm.families.Poisson(), offset=np.log(n + G * c["sgs"].values)).fit().llf
    G = minimize_scalar(nll, bounds=(0.0, 10.0), method="bounded", options={"xatol": 0.002}).x
    m = sm.GLM(y, Xv, family=sm.families.Poisson(), offset=np.log(n + G * c["sgs"].values)).fit()
    return dict(zip(X.columns, m.params)), float(G)


def normals_sunshine(target=TARGET):
    with pdfplumber.open(path("normals", target)) as pdf:
        txt = pdf.pages[0].extract_text()
    vals = re.search(r"Possible sunshine, %((?: \d+){12})", txt).group(1).split()
    return {i + 1: int(v) / 100 for i, v in enumerate(vals)}


def project(coef, G, X, psun, cone=25.0, efull=12.0, ezero=25.0, shape="cos2", dark_at=0.0, school=None):
    g = glare(X["elev"].values, X["az"].values, X["bearing"].values, cone, efull, ezero, shape)
    ps = X["enter"].dt.month.map(psun).values
    lin = np.array([coef[f"sd_{s}"] for s in X["sd"].values]) + np.array([coef.get(f"h_{h}", 0.0) for h in X["hour"].values])
    lin = lin + coef.get("dark", 0.0) * (X["elev"].values < dark_at)
    if school is not None:
        lin = lin + coef.get("school_am", 0.0) * school
    r = np.exp(lin) * (1 + G * g * ps) * 1000
    return pd.Series(r).groupby([X["sd"].values, X["peak"].values]).mean()


def slate(r, cap=CAP):
    return set(r.sort_values(ascending=False).index[:cap])


def main_call(target=TARGET, at="mid", sky="hour", assign="position", **kw):
    A, sec, lat, lon = passes(target, at, sky, assign)
    X = pick_passes(sec, pick(target), lat, lon)
    fk = {k: v for k, v in kw.items() if k in ("cone", "efull", "ezero", "shape", "dark_at", "controls", "hourfe")}
    pk = {k: v for k, v in kw.items() if k in ("cone", "efull", "ezero", "shape", "dark_at")}
    coef, G = fit(A, **fk)
    r = project(coef, G, X, normals_sunshine(target), **pk)
    return r, G, A


def observed_sepoct(A):
    m = A["enter"].dt.hour * 60 + A["enter"].dt.minute
    pk = np.where((m >= 390) & (m < 540), "AM", np.where((m >= 960) & (m < 1110), "PM", "OFF"))
    d = A[(A["wkend"] == 0) & (pk != "OFF") & A["service_date"].dt.month.isin([9, 10])].assign(peak=pk[(A["wkend"] == 0) & (pk != "OFF") & A["service_date"].dt.month.isin([9, 10])])
    t = d.groupby(["sd", "peak"])["n_fb"].agg(["sum", "size"])
    return t["sum"] / t["size"] * 1000


# ---------------------------------------------------------------- ask A: emergency applications in revenue service
def operating(target=TARGET):
    """Which car was running each block when: the yard sheet's pull-out car until the AVL log first shows another
    vehicle on the block that day, then that vehicle to the end of the day; a two-car block's trailing car rides with
    its lead. Returns rows (day, block, car, start, end)."""
    Y = pd.read_csv(path("yard", target))
    Y["day"] = pd.to_datetime(Y["sheet_date"], format="%m/%d/%Y")
    A = pd.read_parquet(path("avl", target), columns=["service_date", "block", "vehicle", "enter_local"])
    A["day"] = pd.to_datetime(A["service_date"])
    A["block"] = A["block"].astype(str)
    A["vehicle"] = A["vehicle"].astype(int)
    A = A.sort_values("enter_local")
    first = A.groupby(["day", "block", "vehicle"], as_index=False)["enter_local"].min()
    out = []
    lo, hi = pd.Timedelta(hours=0), pd.Timedelta(hours=27)
    fmap = {k: g for k, g in first.groupby(["day", "block"])}
    for r in Y.itertuples():
        cars = [int(c) for c in str(r.pullout_cars).split("+")]
        g = fmap.get((r.day, r.block))
        start, end = r.day + lo, r.day + hi
        if g is not None:
            other = g[g["vehicle"] != cars[0]].sort_values("enter_local")
            if len(other):
                sw = other.iloc[0]
                end = pd.Timestamp(sw["enter_local"])
                out.append((r.day, r.block, int(sw["vehicle"]), end, r.day + hi))
        for c in cars:
            out.append((r.day, r.block, c, start, end))
    return pd.DataFrame(out, columns=["day", "block", "car", "start", "end"])


def ask_a(target=TARGET, revenue="operating", dedupe="pair", window_s=360, month="local"):
    E = pd.read_csv(path("edr", target))
    E = E[E["event_code"] == "EB"].copy()
    E["t"] = to_local(E["event_time_utc"])
    E["day"] = (E["t"] - pd.Timedelta(hours=3)).dt.normalize()     # service day: the last trips run past midnight
    if revenue == "operating":
        O = operating(target)
        x = E.reset_index().merge(O, on=["day", "car"], how="inner")
        x = x[(x["t"] >= x["start"]) & (x["t"] < x["end"])].drop_duplicates("index")
        E = x.set_index("index")
    elif revenue == "yard":
        Y = pd.read_csv(path("yard", target))
        Y["day"] = pd.to_datetime(Y["sheet_date"], format="%m/%d/%Y")
        on = pd.DataFrame([(d, int(c), b) for d, cs, b in zip(Y["day"], Y["pullout_cars"].astype(str).str.split("+"), Y["block"]) for c in cs],
                          columns=["day", "car", "block"])
        E = E.merge(on, on=["day", "car"], how="inner")
    elif revenue == "avl":
        A = pd.read_parquet(path("avl", target))
        P = A[["vehicle", "block", "enter_local", "exit_local"]].astype({"vehicle": "int64", "enter_local": "datetime64[ns]",
                                                                         "exit_local": "datetime64[ns]"}).sort_values("enter_local")
        x = pd.merge_asof(E.astype({"car": "int64"}).sort_values("t"), P, left_on="t", right_on="enter_local", left_by="car",
                          right_by="vehicle", direction="backward")
        E = x[(x["exit_local"] + pd.Timedelta(seconds=20) >= x["t"]).fillna(False)]
        E["block"] = E["block"].astype(str)
    if dedupe in ("pair", "window"):
        E = E.sort_values("t").reset_index(drop=True)
        keep = np.ones(len(E), dtype=bool)
        for _, g in E.groupby(["day", "block"]):
            idx = list(g.index)
            used = set()
            for i in idx:
                if i in used:
                    continue
                for j in idx:
                    if j <= i or j in used or E.at[j, "car"] == E.at[i, "car"]:
                        continue
                    dt = abs((E.at[j, "t"] - E.at[i, "t"]).total_seconds())
                    dd = np.hypot((E.at[j, "lat"] - E.at[i, "lat"]) * M_LAT,
                                  (E.at[j, "lon"] - E.at[i, "lon"]) * M_LAT * np.cos(np.radians(E.at[i, "lat"])))
                    if dt <= window_s and (dedupe == "window" or dd <= 80):
                        keep[j] = False
                        used.update((i, j))
                        break
        E = E[keep]
    E = E.assign(line=np.where(E["car"] < 120, "Juniper", "Foundry"))
    mon = E["t"].dt.month if month == "local" else pd.to_datetime(E["event_time_utc"]).dt.month
    out = E.groupby(["line", mon.values]).size()
    return {f"{ln} {m:02d}": int(out.get((ln, m), 0)) for ln in ("Juniper", "Foundry") for m in range(4, 11)}


# ---------------------------------------------------------------- ask B: the 2026 classes' first 30 days
def ask_b(target=TARGET, start="solo", badges="register", date="service", days=30):
    R = pd.read_csv(path("runs", target))
    R["service_date"] = pd.to_datetime(R["service_date"])
    ro = pd.read_csv(path("roster", target))
    ro["qualified"] = pd.to_datetime(ro["qualified"])
    solo = R[R["duty"] == "operator"]
    cards = pd.read_csv(path("cards", target), dtype={"badge": str})
    E = pd.read_csv(path("edr", target), dtype={"operator_badge": str})
    E = E[E["event_code"] == "OS"].copy()
    E["t"] = to_local(E["event_time_utc"])
    if badges == "register":
        bm = cards.drop_duplicates("badge").set_index("badge")["operator_no"]
    else:   # the register's current cards only
        bm = cards[cards["withdrawn"].isna()].drop_duplicates("badge").set_index("badge")["operator_no"]
    E["op"] = E["operator_badge"].map(bm)
    out = {}
    for cls, name in (("26-2", "May"), ("26-3", "August")):
        ops = ro[ro["training_class"] == cls]["operator_no"].astype(int)
        n, h = 0, 0.0
        for o in ops:
            if start == "solo":
                w0 = solo[solo["operator_no"] == o]["service_date"].min()
            elif start == "first_row":
                w0 = R[R["operator_no"] == o]["service_date"].min()
            else:
                w0 = ro.set_index("operator_no").loc[o, "qualified"]
            w1 = w0 + pd.Timedelta(days=days)
            ev = E[E["op"] == o]
            dd = ev["t"].dt.normalize() if date == "calendar" else (ev["t"] - pd.Timedelta(hours=3)).dt.normalize()
            n += int(((dd >= w0) & (dd < w1)).sum())
            rr = solo if start == "solo" else R
            h += float(rr[(rr["operator_no"] == o) & (rr["service_date"] >= w0) & (rr["service_date"] < w1)]["revenue_hours"].sum())
        out[name] = dict(overspeeds=n, revenue_hours=round(h, 1), per_100h=round(100 * n / h, 1), hours_exact=round(h, 2),
                         rate_exact=round(100 * n / h, 4))
    return out


# ---------------------------------------------------------------- deliverables
def write_golden(r, obs, G, a, b, target=TARGET):
    os.makedirs(GOLDEN, exist_ok=True)
    sec, _, _ = survey(target)
    S = sec.set_index("section")
    sl = slate(r)
    rows = []
    for s in sec["section"]:
        for dname, dk in (("outbound", "O"), ("inbound", "I")):
            fs, ts = (S.loc[s, "from_stop"], S.loc[s, "to_stop"]) if dk == "O" else (S.loc[s, "to_stop"], S.loc[s, "from_stop"])
            for pk in ("AM", "PM"):
                rows.append((s, dname, pk, fs, ts, "yes" if (f"{s}-{dk}", pk) in sl else "no"))
    pd.DataFrame(rows, columns=["section_id", "direction", "peak", "from_stop", "to_stop", "restricted_speed_slot"]).to_csv(
        os.path.join(GOLDEN, "slot_plan_jan_feb_2027.csv"), index=False, lineterminator="\n")
    import chart
    chart.draw(os.path.join(GOLDEN, "braking_shift.png"), r, obs, sl, sec)


def compute(target=TARGET):
    r, G, A = main_call(target)
    obs = observed_sepoct(A)
    a = ask_a(target)
    b = ask_b(target)
    sl = sorted(f"{sd} {pk}" for sd, pk in slate(r))
    rs = r.sort_values(ascending=False)
    fig = {"slate": sl, "G_hat": round(G, 3), "fourth_rate": round(float(rs.iloc[3]), 2), "fifth_rate": round(float(rs.iloc[4]), 2),
           "fifth_cell": " ".join(rs.index[4]), "separation_pct": round(100 * (rs.iloc[3] / rs.iloc[4] - 1), 1),
           "expected_rates": {f"{k[0]} {k[1]}": round(float(v), 2) for k, v in r.items()},
           "observed_sepoct": {f"{k[0]} {k[1]}": round(float(v), 2) for k, v in obs.items()},
           "ask_a": a, "ask_b": b}
    return fig, r, obs, G


if __name__ == "__main__":
    fig, r, obs, G = compute()
    write_golden(r, obs, G, fig["ask_a"], fig["ask_b"])
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in fig.items() if k not in ("expected_rates", "observed_sepoct")}, indent=1))
