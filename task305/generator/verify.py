"""Independent verifier: unzip target.zip into a scratch folder and recompute every graded figure from the bundle with
code that shares nothing with solve.py, then compare with figures.json and the write-up.

    python3 task305/generator/verify.py [target.zip]
"""
import datetime as dt
import io
import json
import math
import os
import re
import sys
import tempfile
import zipfile
import zoneinfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def ll(E, N):
    """OSGB36 grid to WGS84, Ordnance Survey's own formulas (Helmert shift), written afresh here"""
    a, b, F0 = 6377563.396, 6356256.909, 0.9996012717
    phi0, lam0, N0, E0 = math.radians(49), math.radians(-2), -100000, 400000
    e2 = 1 - b * b / (a * a)
    n = (a - b) / (a + b)
    phi, M = phi0, 0.0
    while True:
        phi = (N - N0 - M) / (a * F0) + phi
        M = b * F0 * ((1 + n + 1.25 * n * n + 1.25 * n ** 3) * (phi - phi0)
                      - (3 * n + 3 * n * n + 2.625 * n ** 3) * math.sin(phi - phi0) * math.cos(phi + phi0)
                      + (1.875 * n * n + 1.875 * n ** 3) * math.sin(2 * (phi - phi0)) * math.cos(2 * (phi + phi0))
                      - (35 / 24) * n ** 3 * math.sin(3 * (phi - phi0)) * math.cos(3 * (phi + phi0)))
        if abs(N - N0 - M) < 1e-5:
            break
    s, c, t = math.sin(phi), math.cos(phi), math.tan(phi)
    nu = a * F0 / math.sqrt(1 - e2 * s * s)
    rho = a * F0 * (1 - e2) / (1 - e2 * s * s) ** 1.5
    eta2 = nu / rho - 1
    d = E - E0
    lat = phi - t / (2 * rho * nu) * d ** 2 + t / (24 * rho * nu ** 3) * (5 + 3 * t * t + eta2 - 9 * t * t * eta2) * d ** 4 \
        - t / (720 * rho * nu ** 5) * (61 + 90 * t * t + 45 * t ** 4) * d ** 6
    lon = lam0 + d / (c * nu) - (nu / rho + 2 * t * t) / (6 * c * nu ** 3) * d ** 3 \
        + (5 + 28 * t * t + 24 * t ** 4) / (120 * c * nu ** 5) * d ** 5 \
        - (61 + 662 * t * t + 1320 * t ** 4 + 720 * t ** 6) / (5040 * c * nu ** 7) * d ** 7
    sl, cl = math.sin(lat), math.cos(lat)
    nu0 = a / math.sqrt(1 - e2 * sl * sl)
    x, y, z = nu0 * cl * math.cos(lon), nu0 * cl * math.sin(lon), (1 - e2) * nu0 * sl
    sc = -20.4894e-6
    rx, ry, rz = (math.radians(v / 3600) for v in (0.1502, 0.2470, 0.8421))
    X = 446.448 + (1 + sc) * x - rz * y + ry * z
    Y = -125.157 + rz * x + (1 + sc) * y - rx * z
    Z = 542.060 - ry * x + rx * y + (1 + sc) * z
    A, B = 6378137.0, 6356752.3142
    E2 = 1 - B * B / (A * A)
    p = math.hypot(X, Y)
    la = math.atan2(Z, p * (1 - E2))
    for _ in range(12):
        la = math.atan2(Z + E2 * A / math.sqrt(1 - E2 * math.sin(la) ** 2) * math.sin(la), p)
    return math.degrees(la), math.degrees(math.atan2(Y, X))


def dist(a, b):
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b[1] - a[1]) / 2) ** 2
    return 2 * 6371008.8 * math.asin(math.sqrt(h))


def call(T):
    hh = pd.read_csv(os.path.join(T, "census2021_ts041_households_oa.csv"))
    pw = pd.read_csv(os.path.join(T, "oa21_population_weighted_centroids.csv"))
    sp = pd.read_csv(os.path.join(T, "grocery_spend_estimates_2026_oa21.csv"))
    oa = hh.merge(pw, left_on="geography code", right_on="OA21CD").merge(sp, on="OA21CD")
    oa["d"] = oa["Number of households"] * oa["AvgWeeklyGrocerySpendPerHousehold_GBP_2026"] * 52 * 0.88
    pcs = pd.read_csv(os.path.join(T, "onspd_may2026_lq.csv"), dtype=str).set_index("pcds")
    lst = pd.read_csv(os.path.join(T, "voa_list_entries_2026_lq.txt"), sep="*", header=None, dtype=str, keep_default_na=False)
    smv = pd.read_csv(os.path.join(T, "voa_summary_valuations_2026_lq.csv"), dtype=str)
    lst = lst.merge(smv, left_on=6, right_on="uarn", how="left")
    lst["mm"] = pd.to_numeric(lst["main_measure"], errors="coerce")
    groc = lst[lst[5].isin(["SUPERMARKET AND PREMISES", "SUPERSTORE AND PREMISES", "FOOD STORE AND PREMISES"]) &
               (lst["unit_of_measurement"] == "m2") & (lst["mm"] >= 280)]
    est = pd.read_excel(os.path.join(T, "store_estate_2026.xlsx"), sheet_name="Stores", dtype={"store_no": str})
    ownpc = dict(zip(est["postcode"], est["store_no"]))
    xy = lambda pc: (float(pcs.loc[pc, "oseast1m"]), float(pcs.loc[pc, "osnrth1m"]))
    stores = [(ownpc.get(r[14]), xy(r[14]), r["mm"]) for _, r in groc.iterrows()]
    parks = [(xy(r[14]), r["mm"]) for _, r in lst[lst["unit_of_measurement"] == "pitches"].iterrows()]

    def sh(o, S):
        w = np.array([a * math.exp(-0.22 * 1.25 * math.hypot(o[0] - p[0], o[1] - p[1]) / 1000.0) for _, p, a in S])
        return w / w.sum()
    cards = pd.read_csv(os.path.join(T, "card_spend_by_home_sector_fy2025_26.csv"), dtype={"store_no": str})
    nl = cards[~cards["cardholder_home_sector"].str.startswith("LQ")].groupby(["store_no", "month"])["spend_gbp"].sum().unstack(fill_value=0.0)
    off = nl[["2025-11", "2025-12", "2026-01", "2026-02"]].mean(axis=1)
    season = [m for m in nl.columns if int(m[5:]) in (3, 4, 5, 6, 7, 8, 9, 10)]
    share = dict(zip(est["store_no"], est["card_share_of_sales"]))
    guests = {s: float((nl.loc[s, season] - off[s]).sum()) / float(share[s]) for s in nl.index}
    own_idx = [i for i, (sid, _, _) in enumerate(stores) if sid]
    den = sum(n * sum(sh(p, stores)[i] for i in own_idx) for p, n in parks)
    V = sum(guests.values()) / den
    origins = [((r["x"], r["y"]), r["d"]) for _, r in oa.iterrows()] + [(p, n * V) for p, n in parks]
    res_only = [((r["x"], r["y"]), r["d"]) for _, r in oa.iterrows()]
    sites = pd.read_excel(os.path.join(T, "site_shortlist_2027.xlsx"), sheet_name="Shortlist")
    out = {}
    for label, org in (("golden", origins), ("resident", res_only)):
        base = sum(d * sh(o, stores) for o, d in org)
        add = {}
        for _, r in sites.iterrows():
            S2 = stores + [(r["site"], xy(r["postcode"]), float(r["proposed_floor_area_m2"]))]
            b2 = sum(d * sh(o, S2) for o, d in org)
            took = sum(base[i] - b2[i] for i in own_idx)
            add[r["site"]] = 0.26 * (b2[-1] - took) - float(r["rent_gbp"] + r["business_rates_gbp"] + r["staffing_gbp"] + r["other_running_gbp"])
        out[label] = add
    return out, V


def asks(T):
    LON = zoneinfo.ZoneInfo("Europe/London")
    # A: delivered cases; a stop closed sooner than its cases could come off (4 min + 0.02 min a case) was turned away
    tms = pd.read_csv(os.path.join(T, "tms_stop_export_20251006_20260329.csv"), dtype={"store_no": str})
    d = tms[tms["stop_type"] == "DEL"].copy()
    arr, dep = pd.to_datetime(d["arrive_utc"]), pd.to_datetime(d["depart_utc"])
    d = d[(dep - arr).dt.total_seconds() / 60.0 >= 4 + 0.02 * d["cases"]]
    d["local"] = pd.to_datetime(d["arrive_utc"]).dt.tz_localize("UTC").dt.tz_convert(LON).dt.date
    d = d[(d["local"] >= dt.date(2025, 10, 6)) & (d["local"] <= dt.date(2026, 3, 29))]
    A = (d.groupby("store_no")["cases"].sum() / 25.0).to_dict()
    # B: one row per shift worked (two rows of a colleague's day whose times overlap are one shift, the one standing
    # being the row the clock-out follows), its paid hours at the store of the terminal clocked in at (or out at)
    w = pd.read_csv(os.path.join(T, "wfm_paid_hours_20251006_20260329.csv"), dtype=str).reset_index()
    w["a"] = pd.to_datetime(w["shift_date"] + " " + w["shift_start"])
    w["b"] = pd.to_datetime(w["shift_date"] + " " + w["shift_end"])
    w.loc[w["b"] <= w["a"], "b"] += pd.Timedelta(days=1)
    p = pd.read_csv(os.path.join(T, "ta_punches_20251006_20260329.csv"), dtype=str)
    term = dict(zip(*[pd.read_csv(os.path.join(T, "ta_terminals.csv"), dtype=str)[c] for c in ("terminal_id", "store_no")]))
    p["t"] = pd.to_datetime(p["punch_time"])
    p["store"] = p["terminal_id"].map(term)
    pin = {k: list(zip(g["t"], g["store"])) for k, g in p[p["punch"] == "IN"].groupby("employee_no")}
    pout = {k: list(zip(g["t"], g["store"])) for k, g in p[p["punch"] == "OUT"].groupby("employee_no")}
    Bh = {}
    for (emp, d), g in w.groupby(["employee_no", "shift_date"]):
        rows = g.sort_values("index").to_dict("records")
        left = list(rows)
        while left:
            r = left.pop(0)
            same = [r] + [q for q in left if q["a"] < r["b"] and r["a"] < q["b"]]
            left = [q for q in left if q not in same]
            if len(same) > 1:
                fol = [q for q in same if any(pd.Timedelta(0) <= t - q["b"] <= pd.Timedelta(minutes=15) for t, _ in pout.get(emp, []))]
                r = fol[-1]
            st = [s for t, s in pin.get(emp, []) if pd.Timedelta(0) <= r["a"] - t <= pd.Timedelta(minutes=15)] or \
                 [s for t, s in pout.get(emp, []) if pd.Timedelta(0) <= t - r["b"] <= pd.Timedelta(minutes=15)]
            Bh[st[0]] = Bh.get(st[0], 0.0) + float(r["paid_hours"])
    Bh = {s: x / 25.0 for s, x in Bh.items()}
    # C: departures by the clock on Friday 15 January 2027
    pcs = pd.read_csv(os.path.join(T, "onspd_may2026_lq.csv"), dtype=str).set_index("pcds")
    sites = pd.read_excel(os.path.join(T, "site_shortlist_2027.xlsx"), sheet_name="Shortlist")
    pos = {r["site"]: ll(float(pcs.loc[r["postcode"], "oseast1m"]), float(pcs.loc[r["postcode"], "osnrth1m"]))
           for _, r in sites.iterrows()}
    cnt = []
    for f in ("gtfs_sallowmere_motor_services_20261002.zip", "gtfs_wrentoft_district_coaches_20261002.zip"):
        z = zipfile.ZipFile(os.path.join(T, f))
        rd = lambda n: pd.read_csv(io.BytesIO(z.read(n)), dtype=str)
        cal, cd = rd("calendar.txt"), rd("calendar_dates.txt")
        trips = rd("trips.txt").merge(rd("routes.txt"), on="route_id")
        stops = rd("stops.txt")
        near = {k: set(stops[[dist((float(a), float(b)), q) <= 400 for a, b in zip(stops["stop_lat"], stops["stop_lon"])]]["stop_id"])
                for k, q in pos.items()}
        st = rd("stop_times.txt")
        st = st[st["pickup_type"] != "1"]
        c = {}
        for ymd, wd, late in (("20270115", "friday", False), ("20270114", "thursday", True)):
            on = set(cal[(cal[wd] == "1") & (cal["start_date"] <= ymd) & (cal["end_date"] >= ymd)]["service_id"])
            on |= set(cd[(cd["date"] == ymd) & (cd["exception_type"] == "1")]["service_id"])
            on -= set(cd[(cd["date"] == ymd) & (cd["exception_type"] == "2")]["service_id"])
            tr = trips[trips["service_id"].isin(on)][["trip_id", "route_short_name", "direction_id"]]
            x = st.merge(tr, on="trip_id")
            x = x[(x["departure_time"] >= "24:00:00") == late]
            for _, r in x.iterrows():
                for k in pos:
                    if r["stop_id"] in near[k]:
                        key = (k, r["route_short_name"], r["direction_id"], r["stop_id"], r["departure_time"], ymd)
                        c[key] = c.get(key, 0) + 1
        cnt.append(c)
    C = {k: 0 for k in pos}
    # a journey both feeds list is one bus; a second bus one feed lists on the same timetable is another
    for key in set(cnt[0]) | set(cnt[1]):
        C[key[0]] += max(cnt[0].get(key, 0), cnt[1].get(key, 0))
    return A, Bh, C


def main(zpath=None):
    zpath = zpath or os.path.join(TASK, "target.zip")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(zpath) as z:
            z.extractall(tmp)
        T = os.path.join(tmp, "target") if os.path.isdir(os.path.join(tmp, "target")) else tmp
        out, V = call(T)
        A, B, C = asks(T)
    bad = []
    g = out["golden"]
    site = max(g, key=g.get)
    if site != fig["site"] or round(g[site] / 1e5) / 10 != fig["add"]:
        bad.append("call %s %.0f" % (site, g[site]))
    if int(round(V / 10.0) * 10) != fig["V"]:
        bad.append("V %.1f" % V)
    r = out["resident"]
    if max(r, key=r.get) != fig["resident_site"] or round(r[fig["resident_site"]] / 1e5) / 10 != fig["resident_add"]:
        bad.append("resident route")
    for k, v in A.items():
        if int(round(v)) != fig["ask_a"][k]:
            bad.append("ask A %s %.2f" % (k, v))
    for k, v in B.items():
        if int(round(v)) != fig["ask_b"][k]:
            bad.append("ask B %s %.2f" % (k, v))
    for k, v in C.items():
        if v != fig["ask_c"][k]:
            bad.append("ask C %s %d" % (k, v))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    for k, v in fig["ask_a"].items():
        if "Store %s: %s cases" % (k, "{:,}".format(v)) not in sub:
            bad.append("write-up lacks store %s's cases" % k)
    for k, v in fig["ask_b"].items():
        if "Store %s: %s hours" % (k, "{:,}".format(v)) not in sub:
            bad.append("write-up lacks store %s's hours" % k)
    if "GBP %.1f million" % fig["add"] not in sub:
        bad.append("write-up lacks the addition")
    if bad:
        print("VERIFY FAIL: " + "; ".join(bad))
        return 1
    print("verify: the bundle recomputes the call (%s, %.1f million, %d a pitch), the resident route and all 26 ask "
          "figures" % (site, fig["add"], fig["V"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
