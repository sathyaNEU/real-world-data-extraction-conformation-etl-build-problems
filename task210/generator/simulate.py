"""Clean truth for task210 architecture 2.

simulate(seed, **overrides) returns a dict of DataFrames at full truth (hidden columns included):
  geometry  section directions with bearings and coordinates
  passes    one row per train pass of a section in one direction (local and UTC times, sun, glare, operator, cars)
  fb, eb, os  recorder events (firm brake, emergency loop, overspeed) with the truth flags the asks need
  weather   hourly sky cover
  operators, consists, releases, cards  the roster, the yard's consist log, depot releases, badge card reissues
Overrides switch world drivers off for the competing-cause checks (new_op, school, dark) or move G and the bases.
"""
import heapq
import math
import numpy as np
import pandas as pd
import world as W
from solar import sun_position

M_PER_DEG_LAT = 111320.0


def to_latlon(x, y):
    lat = W.LAT0 + y / M_PER_DEG_LAT
    lon = W.LON0 + x / (M_PER_DEG_LAT * math.cos(math.radians(W.LAT0)))
    return lat, lon


def geometry():
    rows = []
    for line in ("J", "F"):
        x, y = W.LINE_START[line]
        for sec, ln, a, b, brg, length, typ in [s for s in W.SECTIONS if s[1] == line]:
            x2 = x + length * math.sin(math.radians(brg))
            y2 = y + length * math.cos(math.radians(brg))
            la1, lo1 = to_latlon(x, y)
            la2, lo2 = to_latlon(x2, y2)
            rows.append(dict(section=sec, line=line, from_stop=a, to_stop=b, bearing_out=brg, length_m=length, track=typ,
                             x1=x, y1=y, x2=x2, y2=y2, lat1=la1, lon1=lo1, lat2=la2, lon2=lo2))
            x, y = x2, y2
    return pd.DataFrame(rows)


def glare(elev, az, heading, cone=W.CONE, efull=W.E_FULL, ezero=W.E_ZERO, shape="cos2"):
    off = np.abs(((az - heading + 180.0) % 360.0) - 180.0)
    if shape == "cos2":
        a = np.where(off < cone, np.cos(np.pi / 2 * off / cone) ** 2, 0.0)
    elif shape == "lin":
        a = np.clip(1 - off / cone, 0, 1)
    else:
        a = (off < cone).astype(float)
    h = np.where(elev <= 0.5, 0.0, np.where(elev <= efull, 1.0, np.clip((ezero - elev) / max(ezero - efull, 1e-6), 0, 1)))
    return a * h


def day_type(d, holidays):
    if d.strftime("%Y-%m-%d") in holidays or d.weekday() == 6:
        return "sunday"
    return "saturday" if d.weekday() == 5 else "weekday"


def in_ranges(dates, ranges):
    out = np.zeros(len(dates), dtype=bool)
    for a, b in ranges:
        out |= (dates >= pd.Timestamp(a)) & (dates <= pd.Timestamp(b))
    return out


def trips_for(days, holidays):
    """Departures from each line's first stop (outbound O) and last stop (inbound I), local minutes."""
    rows = []
    for d in days:
        dt = day_type(d, holidays)
        for (a, b, h) in W.HEADWAY[dt]:
            t = a
            while t < b - 1e-9:
                for line in ("J", "F"):
                    for dirn in ("O", "I"):
                        rows.append((d, dt, line, dirn, t))
                t += h
    return pd.DataFrame(rows, columns=["date", "daytype", "line", "dir", "dep_min"])


def section_runs(geo, adj=None):
    """Scheduled stop-to-stop running times (dwell included) by direction; adj adds whole seconds per section and
    direction (the January pick's revised running times)."""
    out = {}
    adj = adj or {}
    for line in ("J", "F"):
        g = geo[geo["line"] == line]
        secs = list(g["section"])
        run = {s: g.set_index("section").loc[s, "length_m"] / (W.SPEED_KMH[g.set_index("section").loc[s, "track"]] / 3.6) + W.DWELL_S
               for s in secs}
        out[(line, "O")] = [(s, run[s] + adj.get(s, (0, 0))[0]) for s in secs]
        out[(line, "I")] = [(s, run[s] + adj.get(s, (0, 0))[1]) for s in reversed(secs)]
    return out


def departures(dtype):
    """Departure minutes from each line's outer stops for a day type (the same clock at both ends, as trips_for)."""
    out = []
    for a, b, h in W.HEADWAY[dtype]:
        t = a
        while t < b - 1e-9:
            out.append(t)
            t += h
    return out


def _fifo_slot(waiting, fut, ready):
    """For a car arriving at a terminal: the index into the coming departures fut of the one it takes behind the cars
    already waiting there (each takes the first departure its layover allows, in arrival order), and the index of the
    first departure its own layover allows."""
    i = 0
    for r in sorted(w[2] for w in waiting):
        while i < len(fut) and fut[i] < r - 1e-9:
            i += 1
        i += 1
    j = 0
    while j < len(fut) and fut[j] < ready - 1e-9:
        j += 1
    while i < len(fut) and fut[i] < ready - 1e-9:
        i += 1
    return i, j


def blocking(geo, line, dtype):
    """The scheduling department's blocks for one line on one day type: {(direction, departure minute): (block, run)}.

    Trips leave both outer stops on the same clock. A block pulls out of the line's yard at the outer end (Union Yard on
    the Juniper, the Foundry depot at Foundry Loop), straight onto an inbound trip or by deadhead to the inner end for an
    outbound one, and runs out and back: each departure takes the car that has laid over longest among those whose
    scheduled layover (W.LAYOVER) has run, and a pull-out covers a departure no car is ready for. A car arriving where the
    cars ahead of it already cover the first departure it could take is not needed and pulls in (from the inner end after
    a deadhead), as do the last arrivals. On weekdays the Juniper's J01 and J02 are the two blocks that come into Union
    Yard just before each strengthening window and leave it again after (each window's first trip inbound out of Union
    Yard, its last outbound into it), so the trailing car couples and uncouples in the yard; the other blocks are
    numbered in pull-out order. The early run hands the block to the late run at the outer end, in the layover nearest
    the middle of the block's day."""
    runs = section_runs(geo)
    R = {d: sum(rt for _, rt in runs[(line, d)]) / 60.0 for d in ("O", "I")}
    lay = dict(zip(("A", "B"), W.LAYOVER[line]))          # A the inner end (outbound leaves), B the outer end (inbound)
    deps = departures(dtype)
    ev = []
    for t in deps:
        heapq.heappush(ev, (t, 1, "B", -1))
        heapq.heappush(ev, (t, 2, "A", -1))
    q = {"A": [], "B": []}
    trips, nb = [], 0
    while ev:
        t, k, term, blk = heapq.heappop(ev)
        if k == 0:                                            # blk arrives at term
            fut = [d for d in deps if d > t - 1e-9]
            i, j = _fifo_slot(q[term], fut, t + lay[term])
            if i < len(fut) and i == j:
                q[term].append((blk, t, t + lay[term]))
            continue                                          # otherwise not needed: pulls in
        ready = [x for x in q[term] if x[2] <= t + 1e-9]
        if ready:
            x = min(ready, key=lambda x: x[1])
            q[term].remove(x)
            b = x[0]
        else:
            b, nb = nb, nb + 1                                # a pull-out
        d = "I" if term == "B" else "O"
        trips.append((b, d, t))
        heapq.heappush(ev, (t + R[d], 0, "A" if term == "B" else "B", b))
    by = {}
    for b, d, t in trips:
        by.setdefault(b, []).append((t, d))
    order = sorted(by, key=lambda b: (by[b][0][0], by[b][0][1] == "O"))
    if line in W.TWO_CAR and dtype == "weekday":
        two = [b for b in order if all(w and w[0][1] == "I" and w[-1][1] == "O" for w in
                                       ([(t, d) for t, d in by[b] if a <= t < z] for a, z in W.TWO_CAR[line]))]
        assert len(two) == len(W.TWO_CAR_BLOCKS), two
        order = two + [b for b in order if b not in two]
    out = {}
    for n, b in enumerate(order):
        tl = by[b]
        mid = (tl[0][0] + tl[-1][0] + R[tl[-1][1]]) / 2
        cand = [i for i in range(len(tl) - 1) if tl[i][1] == "O" and tl[i + 1][1] == "I"]
        rel = min(cand, key=lambda i: abs(tl[i][0] + R["O"] - mid))
        name = "%s%02d" % (line, n + 1)
        for i, (t, d) in enumerate(tl):
            out[(d, round(t, 4))] = (name, name + ("E" if i <= rel else "L"))
    return out


def simulate(seed=W.SEED, start=W.OBS_START, end=W.OBS_END, holidays=None, G=None, base=None, new_op=None, school=None,
             dark=None, forward=False, runs_adj=None):
    rng = np.random.default_rng(seed)
    G = W.G_TRUE if G is None else G
    base = dict(W.BASE) if base is None else base
    new_op = W.NEW_OP if new_op is None else new_op
    school = W.SCHOOL if school is None else school
    dark = dict(W.DARK) if dark is None else dark
    holidays = W.OBS_HOLIDAYS if holidays is None else holidays
    geo = geometry()
    days = pd.date_range(start, end, freq="D")
    trips = trips_for(days, holidays)
    trips["trip"] = np.arange(len(trips))
    # blocks and runs from the scheduling department's blocking for each day type (out and back, layovers at the
    # terminals, pull-outs and pull-ins at the outer end, reliefs there); J01 and J02 run coupled in the peak windows
    sched = {(dt, l): blocking(geo, l, dt) for dt in sorted(trips["daytype"].unique()) for l in ("J", "F")}
    lab = [sched[(dt, l)][(d, round(m, 4))] for dt, l, d, m in zip(trips["daytype"], trips["line"], trips["dir"], trips["dep_min"])]
    trips["block"] = [x[0] for x in lab]
    trips["run"] = [x[1] for x in lab]
    runs = section_runs(geo, runs_adj)
    rows = []
    for (line, dirn), seq in runs.items():
        sub = trips[(trips["line"] == line) & (trips["dir"] == dirn)]
        t0 = sub["dep_min"].values * 60.0
        cum = 0.0
        for sec, rt in seq:
            rows.append(pd.DataFrame({"trip": sub["trip"].values, "section": sec,
                                      "entry_s": t0 + cum, "exit_s": t0 + cum + rt}))
            cum += rt
    P = pd.concat(rows, ignore_index=True).merge(trips, on="trip")
    P = P.merge(geo[["section", "bearing_out", "track", "length_m"]], on="section")
    P["bearing"] = np.where(P["dir"] == "O", P["bearing_out"], (P["bearing_out"] + 180) % 360)
    P["sd"] = P["section"] + "-" + P["dir"]
    P["entry_local"] = P["date"] + pd.to_timedelta(P["entry_s"].round().astype(int), unit="s")
    P["exit_local"] = P["date"] + pd.to_timedelta(P["exit_s"].round().astype(int), unit="s")
    mid = P["date"] + pd.to_timedelta(((P["entry_s"] + P["exit_s"]) / 2).round().astype(int), unit="s")
    mid_utc = pd.DatetimeIndex(mid).tz_localize(W.TZ, ambiguous=True, nonexistent="shift_forward").tz_convert("UTC").tz_localize(None)
    P["mid_utc"] = mid_utc
    el, az = sun_position(np.asarray(mid_utc.values, dtype="datetime64[s]"), W.LAT0, W.LON0)
    P["elev"], P["az"] = el, az
    P["glare"] = glare(el, az, P["bearing"].values)
    P["dark"] = (el < -3).astype(float)
    mins = P["entry_local"].dt.hour * 60 + P["entry_local"].dt.minute
    P["peak"] = "OFF"
    wk = P["daytype"].values == "weekday"
    for pk, (a, b) in W.PEAKS.items():
        P.loc[wk & (mins >= a).values & (mins < b).values, "peak"] = pk
    P["hour"] = P["entry_local"].dt.hour
    P["month"] = P["entry_local"].dt.month
    two = np.zeros(len(P), dtype=bool)
    if "J" in W.TWO_CAR:
        dep = P["dep_min"].values
        for a, b in W.TWO_CAR["J"]:
            two |= (P["line"].values == "J") & wk & (dep >= a) & (dep < b) & np.isin(P["block"].values, W.TWO_CAR_BLOCKS)
    P["cars"] = np.where(two, 2, 1)
    P = P.sort_values(["entry_local", "sd"]).reset_index(drop=True)

    # weather: hourly sky cover from a daily regime with persistence; sunshine fraction from the cover
    hours = pd.date_range(days[0], days[-1] + pd.Timedelta(hours=47), freq="h")
    st = 0.6
    regime = {}
    for d in pd.date_range(days[0], days[-1] + pd.Timedelta(days=1), freq="D"):
        p = W.SUN_NORM[d.month] / 100.0
        st = 0.45 * st + 0.55 * (1.0 if rng.random() < p else 0.0)
        regime[d] = st
    reg = np.array([regime[h.normalize()] for h in hours])
    pm = np.array([W.SUN_NORM[h.month] / 100.0 for h in hours])
    # an hour has the sun out with probability set by the day's regime, centred on the month's normal
    psun = np.clip(pm + 0.55 * (reg - pm), 0.02, 0.98)
    out_ = rng.random(len(hours)) < psun
    v = rng.random(len(hours))
    cover = np.where(out_, np.select([v < 0.45, v < 0.75], ["CLR", "FEW"], "SCT"), np.where(v < 0.55, "BKN", "OVC"))
    wx = pd.DataFrame({"hour_local": hours, "cover": cover})
    wx["sun"] = wx["cover"].map(W.SKY_SUN)
    P["hour_local"] = P["entry_local"].dt.floor("h")
    P = P.merge(wx[["hour_local", "cover", "sun"]], on="hour_local", how="left")

    # operators, training classes, runs: each block has an early and a late run each day
    ops = []
    emp = 4100
    hire0 = pd.Timestamp("2015-03-02")
    for i in range(W.OPERATORS_N):
        emp += int(rng.integers(3, 17))
        q = hire0 + pd.Timedelta(days=int(rng.integers(0, 3600)))
        ops.append(dict(emp=emp, cls="", qualified=q))
    for cls, qd, n in W.TRAINING_CLASSES:
        for k in range(n):
            emp += int(rng.integers(3, 17))
            ops.append(dict(emp=emp, cls=cls, qualified=pd.Timestamp(qd)))
    O = pd.DataFrame(ops)
    # employee numbers run in the order operators qualified (the draws above are kept, only reassigned), so the day's
    # rotation over the eligible operators carries no visible order in the numbers
    O.loc[O.sort_values("qualified", kind="mergesort").index, "emp"] = np.sort(O["emp"].values)
    O["badge_old"] = [f"{b:04d}" for b in rng.choice(np.arange(1200, 9800), len(O), replace=False)]
    O["badge_new"] = [f"{b:06d}" for b in rng.choice(np.arange(210000, 289999), len(O), replace=False)]
    O["card_reissued"] = pd.Timestamp(W.BADGE_MIGRATION) + pd.to_timedelta(rng.integers(0, 42, len(O)), unit="D")
    # the 2026 classes route-train for 5 to 20 days before their first revenue run
    O["first_revenue"] = O["qualified"]
    newc = (O["cls"] != "").values
    O.loc[newc, "first_revenue"] = O.loc[newc, "qualified"] + pd.to_timedelta(rng.integers(5, 21, int(newc.sum())), unit="D")
    # run assignment: operators in revenue service by the date rotate over the day's runs (each block's early and late
    # run from the blocking, the relief at the outer end)
    runkeys = P[["date", "run"]].drop_duplicates().sort_values(["date", "run"]).reset_index(drop=True)
    assign = []
    for d, grp in runkeys.groupby("date"):
        elig = O[O["first_revenue"] <= d].reset_index(drop=True)
        off = int((d - pd.Timestamp("2026-01-05")).days * 7) % len(elig)
        for j, r in enumerate(grp["run"].values):
            assign.append((d, r, int(elig.loc[(off + j * 3) % len(elig), "emp"])))
    A = pd.DataFrame(assign, columns=["date", "run", "emp"])
    P = P.merge(A, on=["date", "run"], how="left")
    P = P.merge(O[["emp", "qualified", "first_revenue", "cls"]], on="emp", how="left")
    P["days_in"] = (P["date"] - P["first_revenue"]).dt.days
    P["newop"] = (P["days_in"] < 60).astype(float)
    sch = in_ranges(P["date"], W.SCHOOL_TERMS) & ~in_ranges(P["date"], W.SCHOOL_BREAKS)
    P["school_am"] = (sch & (P["daytype"] == "weekday").values & (P["peak"] == "AM").values).astype(float)

    # fleet: daily car assignment per block from the line's cars (one or two cars)
    cons = []
    twoday = set(zip(P.loc[P["cars"] == 2, "date"], P.loc[P["cars"] == 2, "block"]))
    for (d, line), grp in P[["date", "line", "block"]].drop_duplicates().groupby(["date", "line"]):
        cars = list(rng.permutation(W.CARS[line]))
        for k, b in enumerate(sorted(grp["block"].unique())):
            lead = cars[k % len(cars)]
            # on a day they run coupled, the two strengthened blocks take the line's two cars left after every block
            # has its lead car
            trail = cars[len(grp["block"].unique()) + k] if (d, b) in twoday else None
            cons.append((d, b, lead, trail))
    C = pd.DataFrame(cons, columns=["date", "block", "lead_car", "trail_car"])
    P = P.merge(C, on=["date", "block"], how="left")

    # firm-brake truth per pass
    noise = {sd: float(np.exp(rng.normal(0, W.SECTION_SD))) for sd in sorted(P["sd"].unique())}
    hf = P["hour"].map(lambda h: W.HOUR_F.get(h, 0.9)).values * np.where(P["daytype"].values == "weekday", 1.0, W.WEEKEND_F)
    typ = P["track"].values
    b = np.where(typ == "street", base["street"], base["reserved"])
    dk = np.where(typ == "street", dark["street"], dark["reserved"])
    sch_f = 1 + np.where(typ == "street", school, 0.0) * P["school_am"].values
    P["p_fb"] = (b / 1000.0 * P["sd"].map(noise).values * hf * (1 + dk * P["dark"].values) * (1 + new_op * P["newop"].values)
                 * sch_f * (1 + G * P["glare"].values * P["sun"].values))
    P["n_fb"] = rng.poisson(P["p_fb"].values)
    P["n_eb"] = rng.poisson(np.where(typ == "street", W.EB_RATE["street"], W.EB_RATE["reserved"]) / 1000.0, len(P))
    osf = np.where(P["days_in"].values < 90, W.OS_NEW_F, 1.0)
    P["n_os"] = rng.poisson(np.where(typ == "street", W.OS_RATE["street"], W.OS_RATE["reserved"]) / 1000.0 * osf)
    return dict(geo=geo, passes=P, weather=wx, operators=O, consists=C, noise=noise, rng=rng)


if __name__ == "__main__":
    import time
    t = time.time()
    T = simulate()
    P = T["passes"]
    print("passes", len(P), "fb", int(P["n_fb"].sum()), "eb", int(P["n_eb"].sum()), "os", int(P["n_os"].sum()),
          "secs", round(time.time() - t, 1))
    print(P.groupby(["sd"]).size().head())
    print(T["geo"][["section", "bearing_out", "lat1", "lon1", "lat2", "lon2"]].round(5).to_string())
