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
    # the take was made in FY2025/26: invert it on the stores and parks of then, from the historic entries (each
    # version's current-from and current-to dates), joined to their measures by assessment reference
    hl = pd.read_csv(os.path.join(T, "archive", "voa_historic_list_entries_lq_20261002.txt"), sep="*", header=None,
                     dtype=str, keep_default_na=False)
    hs = pd.read_csv(os.path.join(T, "archive", "voa_historic_summary_valuations_lq_20261002.csv"), dtype=str)
    hl = hl.merge(hs, left_on=19, right_on="assessment_reference", how="inner")
    hl["frm"] = pd.to_datetime(hl[26], format="%d-%b-%Y")
    hl["to"] = pd.to_datetime(hl[27], format="%d-%b-%Y")
    then = hl[(hl["frm"] <= "2025-04-01") & (hl["to"] >= "2026-03-31")].copy()
    then["mm"] = pd.to_numeric(then["main_measure"], errors="coerce")
    g25 = then[then[5].isin(["SUPERMARKET AND PREMISES", "SUPERSTORE AND PREMISES", "FOOD STORE AND PREMISES"]) &
               (then["unit_of_measurement"] == "m2") & (then["mm"] >= 280)]
    stores25 = [(ownpc.get(r[14]), xy(r[14]), r["mm"]) for _, r in g25.iterrows()]
    parks25 = [(xy(r[14]), r["mm"]) for _, r in then[then["unit_of_measurement"] == "pitches"].iterrows()]
    own25 = [i for i, (sid, _, _) in enumerate(stores25) if sid]
    den = sum(n * sum(sh(p, stores25)[i] for i in own25) for p, n in parks25)
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
    # B: the report lists a night shift against both dates it covers; the shifts a colleague starts on a date are the
    # clock-ins that date (a clock-out with no clock-in before it is a shift whose clock-in was forgotten, dated by the
    # clock-out), and each takes one of that date's lines, at the store of the terminal it was punched at
    _wl = open(os.path.join(T, "wfm_paid_hours_20251006_20260329.csv"), encoding="utf-8").read().split("\n")
    w = pd.read_csv(io.StringIO("\n".join(_wl[next(i for i, ln in enumerate(_wl) if ln.startswith("employee_no,")):])), dtype=str)
    p = pd.read_csv(os.path.join(T, "ta_punches_20251006_20260329.csv"), dtype=str)
    term = dict(zip(*[pd.read_csv(os.path.join(T, "ta_terminals.csv"), dtype=str)[c] for c in ("terminal_id", "store_no")]))
    p["t"] = pd.to_datetime(p["punch_time_local"])
    p["store"] = p["terminal_id"].map(term)
    p = p.sort_values(["employee_no", "t"])
    begin = {}
    for emp, g in p.groupby("employee_no"):
        prev = None
        for t, kind, store in zip(g["t"], g["punch"], g["store"]):
            if kind == "IN":
                begin.setdefault((emp, t.date().isoformat()), []).append(store)
            elif prev != "IN":
                begin.setdefault((emp, t.date().isoformat()), []).append(store)
            prev = kind
    Bh = {}
    for (emp, d), g in w.groupby(["employee_no", "date"], sort=False):
        for paid, store in zip(g["paid_hours"].astype(float), begin.get((emp, d), [])):
            Bh[store] = Bh.get(store, 0.0) + paid
    Bh = {s: x / 25.0 for s, x in Bh.items()}
    # C: departures by the clock on Friday 15 January 2027
    pcs = pd.read_csv(os.path.join(T, "onspd_may2026_lq.csv"), dtype=str).set_index("pcds")
    sites = pd.read_excel(os.path.join(T, "site_shortlist_2027.xlsx"), sheet_name="Shortlist")
    pos = {r["site"]: ll(float(pcs.loc[r["postcode"], "oseast1m"]), float(pcs.loc[r["postcode"], "osnrth1m"]))
           for _, r in sites.iterrows()}
    seen = set()
    for f in ("gtfs_sallowmere_motor_services_20261002.zip", "gtfs_wrentoft_district_coaches_20261002.zip"):
        z = zipfile.ZipFile(os.path.join(T, f))
        rd = lambda n: pd.read_csv(io.BytesIO(z.read(n)), dtype=str)
        cal, cd = rd("calendar.txt"), rd("calendar_dates.txt")
        trips = rd("trips.txt")
        stops = rd("stops.txt")
        near = {k: set(stops[[dist((float(a), float(b)), q) <= 400 for a, b in zip(stops["stop_lat"], stops["stop_lon"])]]["stop_id"])
                for k, q in pos.items()}
        st = rd("stop_times.txt")
        st = st[st["pickup_type"] != "1"]
        for ymd, wd, late in (("20270115", "friday", False), ("20270114", "thursday", True)):
            on = set(cal[(cal[wd] == "1") & (cal["start_date"] <= ymd) & (cal["end_date"] >= ymd)]["service_id"])
            on |= set(cd[(cd["date"] == ymd) & (cd["exception_type"] == "1")]["service_id"])
            on -= set(cd[(cd["date"] == ymd) & (cd["exception_type"] == "2")]["service_id"])
            tr = trips[trips["service_id"].isin(on)][["trip_id", "block_id"]]
            x = st.merge(tr, on="trip_id")
            x = x[(x["departure_time"] >= "24:00:00") == late]
            # a bus is its block: the same block at the same stop and time is one departure, whichever feed or
            # timetable lists it
            for blk, sid, tm in zip(x["block_id"], x["stop_id"], x["departure_time"]):
                for k in pos:
                    if sid in near[k]:
                        seen.add((k, ymd, blk, sid, tm))
    C = {k: 0 for k in pos}
    for key in seen:
        C[key[0]] += 1
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
