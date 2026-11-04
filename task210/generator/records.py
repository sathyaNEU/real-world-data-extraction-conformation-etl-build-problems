"""The organisation's own records, built from the clean truth: what each ART system would have exported.

records(T) returns DataFrames for every shipped data file plus the truth the asks' goldens need:
  edr       event data recorder export (UTC, per car), FB/EB/OS rows
  avl       AVL section-pass log (local time, lead vehicle), with the onboard units' drop-outs
  consist   the yard's daily block sheet (cars per block)
  releases  Foundry depot maintenance releases (local time)
  dispatch  daily run sheets (run, block, operator, revenue hours), route-training ride-alongs included
  operators the roster with training class, qualification date and first solo revenue run
Ask devices: a two-car train's emergency application is logged by both cars' recorders, the trailing car's under a
free-running clock (A1); running brake tests on the day's spare Foundry cars after depot releases (A2); AVL onboard
unit drop-outs leave revenue trips unlogged (A3). Ask B's records (the maintenance system's defect reports, operator
cards keyed on the next business morning) are drawn in defects.py on their own random stream, after every record here.
Badges follow each operator's card (old format until the card was reissued after the July migration), and new operators
ride along on regular runs during route training before their first run alone: both are the run sheets' and the
recorder's own content, read by the main call's careful readers when they net new operators.
"""
import math
import numpy as np
import pandas as pd
import world as W
import simulate as S

FT = 3.28084
DROP_P = 0.2             # share of block-days whose AVL unit drops out for a stretch


def _point_on(geo_row, frac, outbound):
    x1, y1, x2, y2 = geo_row["x1"], geo_row["y1"], geo_row["x2"], geo_row["y2"]
    if not outbound:
        x1, y1, x2, y2 = x2, y2, x1, y1
    return x1 + (x2 - x1) * frac, y1 + (y2 - y1) * frac


def _latlon_noisy(x, y, rng, sd=6.0):
    return S.to_latlon(x + rng.normal(0, sd), y + rng.normal(0, sd))


def utc(local_ts):
    return pd.DatetimeIndex(local_ts).tz_localize(W.TZ, ambiguous=True, nonexistent="shift_forward").tz_convert("UTC").tz_localize(None)


def realised(P, seed):
    """The actual running against the schedule, on its own random stream: each trip leaves its outer stop late (never
    early; a gamma lateness with a mean near 45 seconds and now and then a disruption of several minutes) and each
    section's run varies around its scheduled time (street sections more, with a stop at a signal on some passes;
    reserved track less). The AVL log, the recorder's event times and the run sheets follow the actual running; the
    hazard truth stays on the schedule, a minute or two from it."""
    r = np.random.default_rng(seed + 41)
    Q = P[["trip", "entry_local", "exit_local", "track"]].sort_values(["trip", "entry_local"], kind="mergesort")
    tr = np.sort(Q["trip"].unique())
    late = r.gamma(1.4, 32.0, len(tr))
    late = np.round(late + np.where(r.random(len(tr)) < 0.015, r.uniform(180.0, 540.0, len(tr)), 0.0))
    street = Q["track"].values == "street"
    sched = (Q["exit_local"] - Q["entry_local"]).dt.total_seconds().values
    fac = np.exp(r.normal(0.0, 1.0, len(Q)) * np.where(street, 0.07, 0.035))
    sig = np.where(street & (r.random(len(Q)) < 0.16), r.uniform(12.0, 50.0, len(Q)), 0.0)
    rt = np.round(sched * fac + sig)
    cs = pd.Series(rt, index=Q.index).groupby(Q["trip"].values).cumsum().values - rt
    t0 = Q.groupby("trip")["entry_local"].transform("min")
    enter = t0 + pd.to_timedelta(late[np.searchsorted(tr, Q["trip"].values)] + cs, unit="s")
    out = P.copy()
    out.loc[Q.index, "entry_local"] = enter.values
    out.loc[Q.index, "exit_local"] = (enter + pd.to_timedelta(rt, unit="s")).values
    return out


def records(T, seed=W.SEED):
    rng = np.random.default_rng(seed + 7)
    P = realised(T["passes"], seed)
    geo = T["geo"].set_index("section")
    O = T["operators"].copy()
    C = T["consists"]
    days = sorted(P["date"].unique())

    # recorder clocks: the active cab's recorder is GPS-disciplined to a few seconds; a trailing car's recorder
    # free-runs while it trails, so its clock is off by up to a few minutes on those days
    cars = W.CARS["J"] + W.CARS["F"]
    lead_off = {(c, d): float(np.clip(rng.normal(0, 3), -8, 8)) for c in cars for d in days}
    trail_off = {(int(r.trail_car), r.date): float(rng.uniform(-210, 210)) for r in C[C["trail_car"].notna()].itertuples()}

    # in-service swaps: on some Foundry weekdays a car is bad-ordered in service, runs in to the depot and the day's
    # spare takes over its block for the rest of the day; the yard sheet keeps the pull-out car (A2)
    P = P.copy()
    swaps = []
    for d in days:
        if pd.Timestamp(d).weekday() >= 5 or rng.random() >= W.SWAP_P:
            continue
        fb = C[(C["date"] == d) & C["block"].str.startswith("F")]
        spares = [c for c in W.CARS["F"] if c not in set(fb["lead_car"].astype(int))]
        r = fb.iloc[int(rng.integers(0, len(fb)))]
        t_sw = pd.Timestamp(d) + pd.Timedelta(minutes=int(rng.integers(9 * 60, 13 * 60 + 30)))
        spare = int(rng.choice(spares))
        m = (P["date"] == d) & (P["block"] == r["block"]) & (P["entry_local"] >= t_sw)
        P.loc[m, "lead_car"] = spare
        swaps.append((pd.Timestamp(d), r["block"], int(r["lead_car"]), spare, P.loc[m, "entry_local"].min()))
    SW = pd.DataFrame(swaps, columns=["date", "block", "bad_car", "spare", "t_first"])

    ev = []
    for code, ncol in (("FB", "n_fb"), ("EB", "n_eb"), ("OS", "n_os")):
        sub = P[P[ncol] > 0]
        rep = sub.loc[sub.index.repeat(sub[ncol].values)].reset_index(drop=True)
        frac = rng.random(len(rep))
        dur = (rep["exit_local"] - rep["entry_local"]).dt.total_seconds().values
        t_local = rep["entry_local"] + pd.to_timedelta(np.round(frac * dur).astype(int), unit="s")
        xs, ys = zip(*[_point_on(geo.loc[s], f, d == "O") for s, f, d in zip(rep["section"], frac, rep["dir"])])
        e = pd.DataFrame({"code": code, "car": rep["lead_car"].values, "t_local": t_local.values, "x": xs, "y": ys,
                          "section": rep["section"].values, "dir": rep["dir"].values, "line": rep["line"].values,
                          "date": rep["date"].values, "emp": rep["emp"].values, "track": rep["track"].values,
                          "block": rep["block"].values, "cars": rep["cars"].values, "trail_car": rep["trail_car"].values,
                          "copy": False, "test": False})
        if code == "EB":
            # the Foundry Loop terminal crossing: some outbound F7 applications are made at walking pace in the loop
            loop = (e["section"] == "F7") & (e["dir"] == "O") & (rng.random(len(e)) < W.LOOP_SLOW_P)
            e["slow"] = loop.values
            fr = 1.0 - rng.random(int(loop.sum())) * 0.15
            pts = [_point_on(geo.loc["F7"], f, True) for f in fr]
            e.loc[loop, "x"] = [p[0] for p in pts]
            e.loc[loop, "y"] = [p[1] for p in pts]
        ev.append(e)
        if code == "EB":
            two = e[(e["cars"] == 2) & e["trail_car"].notna()].copy()
            # the trailing car's recorder logs the same loop opening about one car length behind
            ang = np.array([math.radians(geo.loc[s, "bearing_out"] + (0 if d == "O" else 180)) for s, d in zip(two["section"], two["dir"])])
            two["x"] = two["x"].values - 27.0 * np.sin(ang)
            two["y"] = two["y"].values - 27.0 * np.cos(ang)
            two["car"] = two["trail_car"].astype(int).values
            two["copy"] = True
            ev.append(two)
    E = pd.concat(ev, ignore_index=True)

    # Foundry depot releases: each bad-ordered car is repaired, released and run on the depot loop before it goes back
    # to the ready line, with an emergency application in the running brake test (A2)
    rel = []
    fgeo = geo.loc["F7"]
    hostlers = O[(O["cls"] == "") & (O["qualified"] < pd.Timestamp("2024-01-01"))]["emp"].values[:6]
    wtypes = ["door system repair", "pantograph inspection", "wheel flat", "HVAC repair", "brake cylinder", "coupler repair",
              "propulsion fault", "destination sign"]
    tests = []
    for sw in SW.itertuples():
        t_rel = sw.t_first + pd.Timedelta(minutes=int(rng.integers(70, 200)))
        rel.append((t_rel, sw.bad_car, f"WO-{int(rng.integers(40000, 69999))}", str(rng.choice(wtypes))))
        t_test = t_rel + pd.Timedelta(minutes=int(rng.integers(12, 46)))
        x, y = _point_on(fgeo, 1.0 - rng.random() * 0.18, True)
        tests.append(dict(code="EB", car=sw.bad_car, t_local=t_test, x=x, y=y, section="F7", dir="O", line="F",
                          date=sw.date, emp=int(rng.choice(hostlers)), track="reserved", block="", cars=1,
                          trail_car=np.nan, copy=False, test=True, slow=True))
    E = pd.concat([E, pd.DataFrame(tests)], ignore_index=True)
    R = pd.DataFrame(rel, columns=["released_local", "car", "work_order", "work_type"])

    # UTC stamps on each recorder's own clock, positions with GPS scatter, speeds and decelerations
    off = [trail_off[(int(c), pd.Timestamp(d))] if cp else lead_off[(int(c), pd.Timestamp(d))]
           for c, d, cp in zip(E["car"], E["date"], E["copy"])]
    E["t_utc"] = utc(E["t_local"]) + pd.to_timedelta(np.round(off).astype(int), unit="s")
    lat, lon = _latlon_noisy(E["x"].values, E["y"].values, rng)
    E["lat"], E["lon"] = np.round(lat, 6), np.round(lon, 6)
    street = E["track"].values == "street"
    E["speed_mph"] = np.where(E["code"] == "OS", np.where(street, 25 + rng.uniform(3.2, 9, len(E)), 45 + rng.uniform(3.2, 9, len(E))),
                              np.where(street, rng.uniform(8, 27, len(E)), rng.uniform(14, 42, len(E))))
    E["slow"] = E["slow"].fillna(False).astype(bool)
    E.loc[E["slow"], "speed_mph"] = rng.uniform(3, 7, int(E["slow"].sum()))
    # decelerations: a firm brake clears the 1.3 m/s2 trigger and thins out above it (a truncated exponential, most
    # just over the trigger); an emergency application centres near 2.75 m/s2 with the rail's adhesion. The same two
    # uniform draws as before, mapped through each shape, so the stream and every later draw are unchanged
    q_fb = (rng.uniform(1.3, 2.15, len(E)) - 1.3) / 0.85
    q_eb = (rng.uniform(2.35, 3.05, len(E)) - 2.35) / 0.70
    from scipy.stats import norm
    fb_dec = 1.3 - 0.18 * np.log(1 - q_fb * (1 - np.exp(-0.9 / 0.18)))
    eb_dec = np.clip(2.75 + 0.15 * norm.ppf(np.clip(q_eb, 1e-6, 1 - 1e-6)), 2.3, 3.2)
    E["decel_mps2"] = np.where(E["code"] == "FB", fb_dec, np.where(E["code"] == "EB", eb_dec, np.nan))
    E["speed_mph"] = E["speed_mph"].round(1)
    E["decel_mps2"] = E["decel_mps2"].round(2)
    # a copy is logged at the trailing car's own speed reading, a few tenths away from the lead's
    E.loc[E["copy"], "speed_mph"] = (E.loc[E["copy"], "speed_mph"] + rng.normal(0, 0.4, int(E["copy"].sum()))).round(1)

    # badges: old 4-digit until the card was reissued after the migration, 6-digit after (B1)
    O["card_reissued"] = pd.to_datetime(O["card_reissued"])
    bmap = O.set_index("emp")
    eo = E["emp"].astype(int).values
    born_new = bmap.loc[eo, "qualified"].values >= np.datetime64(W.BADGE_MIGRATION)
    E["badge"] = np.where(born_new | (E["date"].values >= bmap.loc[eo, "card_reissued"].values),
                          bmap.loc[eo, "badge_new"].values, bmap.loc[eo, "badge_old"].values)

    # each recorder numbers every event it logs (door interlocks, track brake, gong and the rest, the March
    # commissioning runs included); the export carries the FB, EB and OS rows only, so its numbers run with gaps
    E = E.sort_values(["t_utc", "car"]).reset_index(drop=True)
    rq = np.random.default_rng(seed + 43)
    start = {c: int(rq.integers(140, 960)) for c in cars}
    stepn = 1 + rq.poisson(2.6, len(E))
    E["seq"] = E["car"].astype(int).map(start).values + pd.Series(stepn).groupby(E["car"].astype(int).values).cumsum().values
    E["event_id"] = [f"{c}-{s:06d}" for c, s in zip(E["car"].astype(int), E["seq"])]

    # AVL section-pass log (lead vehicle, local time). Onboard units drop out for a stretch on some block-days (A3), and
    # a detector outage at Arsenal Road 8 to 14 June left F3 and F4 passes unlogged
    avl = P[["date", "line", "dir", "trip", "block", "lead_car", "section", "entry_local", "exit_local"]].copy()
    bd = avl[["date", "block"]].drop_duplicates().sort_values(["date", "block"]).reset_index(drop=True)
    hit = rng.random(len(bd)) < DROP_P
    st = rng.integers(6 * 60, 21 * 60, len(bd))
    ln = rng.integers(120, 480, len(bd))
    bd = bd.assign(d0=st, d1=st + ln)[hit]
    bd = bd[~bd.set_index(["date", "block"]).index.isin(SW.set_index(["date", "block"]).index)]
    mins = avl["entry_local"].dt.hour * 60 + avl["entry_local"].dt.minute
    avl = avl.assign(_m=mins.values).merge(bd, on=["date", "block"], how="left")
    lost = avl["d0"].notna() & (avl["_m"] >= avl["d0"]) & (avl["_m"] < avl["d1"])
    outage = (avl["section"].isin(["F3", "F4"])) & (avl["date"] >= pd.Timestamp("2026-06-08")) & (avl["date"] <= pd.Timestamp("2026-06-14"))
    avl = avl[~lost & ~outage].drop(columns=["_m", "d0", "d1"]).reset_index(drop=True)

    # run sheets: each run's operator and scheduled revenue hours; a 2026-class operator rides along on a regular run
    # each weekday of route training before the first solo run (B2)
    P2 = P.assign(sec=(P["exit_local"] - P["entry_local"]).dt.total_seconds())
    hours = P2.groupby(["date", "run"], as_index=False).agg(block=("block", "first"), emp=("emp", "first"), rh=("sec", "sum"))
    hours["rh"] = (hours["rh"] / 3600).round(2)
    ride = []
    hosts = set(O[(O["cls"] == "") & (O["qualified"] < pd.Timestamp("2025-01-01"))]["emp"].astype(int))   # line instructors are experienced operators
    for o in O[O["cls"] != ""].itertuples():
        for d in pd.date_range(o.qualified, o.first_revenue - pd.Timedelta(days=1), freq="D"):
            if d.weekday() >= 5 or d < pd.Timestamp(W.OBS_START):
                continue
            pool = hours[(hours["date"] == d) & hours["emp"].isin(hosts)]
            r = pool.iloc[int(rng.integers(0, len(pool)))]
            ride.append((d, r["run"], r["block"], int(o.emp), r["rh"]))
    disp = pd.concat([hours.rename(columns={"rh": "revenue_hours"}).assign(duty="operator"),
                      pd.DataFrame(ride, columns=["date", "run", "block", "emp", "revenue_hours"]).assign(duty="route training")],
                     ignore_index=True)
    disp = disp.sort_values(["date", "run", "emp"]).reset_index(drop=True)

    # truth for the asks
    E["t_local_true"] = E["t_local"]
    rev = E[(E["code"] == "EB") & (~E["copy"]) & (~E["test"])]
    eb_truth = rev.groupby(["line", rev["t_local"].dt.month]).size()
    import defects
    mms, cards_truth, rel_wo = defects.defect_reports(T, dict(swaps=SW), seed)
    R["work_order"] = rel_wo          # the repairs' numbers in the agency's work-order series (the draw above is spent)
    defect_truth = defects.ask_b_truth(cards_truth)
    return dict(edr=E, avl=avl, releases=R, dispatch=disp, consist=C, operators=O, eb_truth=eb_truth, mms=mms, cards_truth=cards_truth,
                defect_truth=defect_truth,
                metar=T["weather"], swaps=SW)


if __name__ == "__main__":
    T = S.simulate()
    Rr = records(T)
    E = Rr["edr"]
    print(E["code"].value_counts().to_dict(), "copies", int(E["copy"].sum()), "tests", int(E["test"].sum()))
    print("eb truth", Rr["eb_truth"].to_dict())
    print("defect truth", Rr["defect_truth"], "mms rows", len(Rr["mms"]))
    print("avl rows", len(Rr["avl"]), "of", len(T["passes"]), "releases", len(Rr["releases"]), "run rows", len(Rr["dispatch"]))
