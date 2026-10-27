"""task307 records: the subarea network extract, trip tables, model outputs, count stations, probe travel times."""
import datetime as dt

import numpy as np
import pandas as pd

import net
import params as P
import solve
import world

ZONE_OFFSET = {"W1": (-2600, 0), "W2": (-2500, 300), "W3": (-2700, -200), "W4": (-2400, 200), "W5": (-1800, -2500),
               "W6": (-2100, -800), "Z_DT1": (600, 900), "Z_DT2": (900, -700), "Z_E": (2500, 1200), "Z_P": (1500, -2200)}


def node_number(name):
    return P.NODE_ID.get(name) or int(name)


def ftype(l):
    if l["ftype"] == "freeway" and l["bottleneck"]:
        return P.FTYPE["freeway_lanedrop"]
    return P.FTYPE[l["ftype"]]


def link_records(links):
    """one record per two-way link, in the extract's order (pairs come out of the network builder together)"""
    recs = []
    for k in range(0, len(links), 2):
        ab, ba = links[k], links[k + 1]
        assert ab["a"] == ba["b"] and ab["b"] == ba["a"]
        recs.append(dict(LINK_ID=len(recs) + 1, A_NODE=node_number(ab["a"]), B_NODE=node_number(ab["b"]),
                         STREET=ab["name"] if ab["name"] != "connector" else "", FTYPE=ftype(ab),
                         AB_LANES=ab["lanes"], BA_LANES=ba["lanes"], LENGTH_MI=ab["length_mi"],
                         FF_SPD_MPH=ab["speed_mph"], _k=k))
    return recs


def nodes_table(links):
    zm = world.zones()
    rows = []
    for name, nid in P.NODE_ID.items():
        x, y = P.NODE_XY[name]
        rows.append(dict(N=nid, X=x, Y=y, CENTROID=0))
    rng = np.random.default_rng(P.SEED + 11)
    for z in sorted(zm):
        m = zm[z]
        ax, ay = P.NODE_XY[world.ATTACH[m]]
        ox, oy = ZONE_OFFSET[m]
        rows.append(dict(N=z, X=int(ax + ox + rng.integers(-900, 900)), Y=int(ay + oy + rng.integers(-900, 900)), CENTROID=1))
    return pd.DataFrame(rows).sort_values("N")


def trips_table(tabs):
    rows = []
    for per in ("AM", "PM"):
        for (o, d), q in sorted(tabs[per].items(), key=lambda kv: (int(kv[0][0]), int(kv[0][1]))):
            rows.append(dict(PERIOD=per, I=int(o), J=int(d), TRIPS=q))
    return pd.DataFrame(rows)


def loaded_table(o):
    links = o["links"]
    recs = link_records(links)
    rows = []
    # the corridor assignment loads trips at the zones' attachment nodes; a connector carries its zone's trip ends
    ends = {}
    for per in ("AM", "PM"):
        for (i, j), q in o["tabs"][per].items():
            ends[(per, "out", int(i))] = ends.get((per, "out", int(i)), 0) + q
            ends[(per, "in", int(j))] = ends.get((per, "in", int(j)), 0) + q
    for r in recs:
        k = r["_k"]
        row = dict(LINK_ID=r["LINK_ID"], A_NODE=r["A_NODE"], B_NODE=r["B_NODE"])
        for per in ("AM", "PM"):
            v, t = o["nobuild"][per]["v"].copy(), o["nobuild"][per]["t"]
            if links[k]["ftype"] == "connector":
                v[k] = ends.get((per, "out", r["A_NODE"]), 0)
                v[k + 1] = ends.get((per, "in", r["A_NODE"]), 0)
            row["AB_VOL_" + per] = round(float(v[k]), 1); row["BA_VOL_" + per] = round(float(v[k + 1]), 1)
            row["AB_TIME_" + per] = round(float(t[k]), 3); row["BA_TIME_" + per] = round(float(t[k + 1]), 3)
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- count stations
STATIONS = [  # station, location, link (a, b) in the AB sense, AB direction label, BA direction label
    ("S-0101", "Route 9, Ashkettle Bridge", ("F4", "BN"), "EB", "WB"),
    ("S-0102", "Center Street Bridge", ("A3", "C3"), "EB", "WB"),
    ("S-0103", "Southport Bridge", ("A1", "C1"), "EB", "WB"),
    ("S-0104", "Route 9 at Millbrook", ("F2", "F3"), "NB", "SB"),
    ("S-0105", "Route 9 south of Lakeview Road", ("F1", "F2"), "NB", "SB"),
    ("S-0106", "Millbrook Road at Quarry Lane", ("A2", "A3"), "NB", "SB"),
    ("S-0107", "Harbor Avenue at Dock Street", ("C2", "C3"), "NB", "SB"),
    ("S-0108", "Lakeview Parkway east of Harbor Avenue", ("C4", "EF"), "EB", "WB"),
]
REPLACED = ("S-0103", "S-0103R", dt.date(2025, 7, 15))


def base_assignment():
    """the 2025 base-year assignment: 2028 tables scaled back to 2025 and assigned to equilibrium"""
    links = world.network()
    cap, t0, al, be = net.link_arrays(links)
    tabs = world.trip_tables()
    out = {}
    for per, od in tabs.items():
        od25 = {k: q * P.BASE_GROWTH for k, q in od.items()}
        v, t = solve.equilibrium(links, od25, cap, t0, al, be)
        out[per] = v
    return links, out


def directed_index(links, a, b):
    for k, l in enumerate(links):
        if l["a"] == a and l["b"] == b:
            return k
    raise KeyError((a, b))


# the truck model's share of heavy vehicles moves by direction and peak (freight runs against the commute)
HV_ADJ = {(s, d, p): f for s, ds, fs in [("S-0101", ("EB", "WB"), (0.88, 1.21, 1.17, 0.86)),
                                         ("S-0102", ("EB", "WB"), (0.74, 1.32, 1.28, 0.70)),
                                         ("S-0103", ("EB", "WB"), (0.81, 1.44, 1.36, 0.78)),
                                         ("S-0104", ("NB", "SB"), (0.92, 1.12, 1.09, 0.95)),
                                         ("S-0105", ("NB", "SB"), (0.95, 1.07, 1.10, 0.93))]
          for (d, p), f in zip([(ds[0], "AM"), (ds[1], "AM"), (ds[0], "PM"), (ds[1], "PM")], fs)}


def validation_table(links, base):
    rows = []
    for st, loc, (a, b), dab, dba in STATIONS[:5]:
        rec_id = None
        for r in link_records(links):
            if {r["A_NODE"], r["B_NODE"]} == {node_number(a), node_number(b)}:
                rec_id = r["LINK_ID"]
        for (x, y), dlab in (((a, b), dab), ((b, a), dba)):
            k = directed_index(links, x, y)
            for per in ("AM", "PM"):
                hv = round(P.HV_SHARE[ftype(links[k])] * HV_ADJ[(st, dlab, per)], 3)
                veh = int(round(base[per][k]))
                rows.append(dict(STATION=st, LINK_ID=rec_id, DIR=dlab, PERIOD=per,
                                 VOL_PCE=round(veh * (1 + hv), 2), HV_PCT=round(100 * hv, 1)))
    return pd.DataFrame(rows)


HOLIDAYS_2025 = [dt.date(2025, 1, 1), dt.date(2025, 1, 20), dt.date(2025, 2, 17), dt.date(2025, 5, 26),
                 dt.date(2025, 6, 19), dt.date(2025, 7, 4), dt.date(2025, 9, 1), dt.date(2025, 10, 13),
                 dt.date(2025, 11, 11), dt.date(2025, 11, 27), dt.date(2025, 12, 25)]
DST_ON, DST_OFF = dt.date(2025, 3, 9), dt.date(2025, 11, 2)


# local traffic the corridor model does not carry, on the count-only arterial stations (vehicles an hour, each way)
LOCAL_BG = {"S-0106": 380, "S-0107": 520, "S-0108": 430}
_H = np.arange(24) + 0.5                     # index i is hour ending i+1, centred on its half hour
_NIGHT = np.array([0.30, 0.18, 0.13, 0.12, 0.22, 0.55] + [1.0] * 15 + [0.85, 0.65, 0.45])
_PLATEAU = (0.75 + 0.25 * np.exp(-0.5 * ((_H - 13) / 3.5) ** 2)) * _NIGHT
_BAM = np.exp(-0.5 * ((_H - 7.6) / 1.1) ** 2)
_BPM = np.exp(-0.5 * ((_H - 17.4) / 1.3) ** 2)


def day_shape(am, pm, weekend=False):
    """a weekday's hourly volumes in one direction whose 7-8 a.m. and 5-6 p.m. hours are the model's peak hours: a
    midday plateau below the lesser peak and an AM and a PM bump sized to meet the two peaks"""
    if weekend:
        return 0.55 * am * _PLATEAU / _PLATEAU[12] + 0.25 * am * np.exp(-0.5 * ((_H - 13.5) / 2.5) ** 2)
    m = min(0.55 * (am + pm) / 2, 0.85 * min(am, pm)) / _PLATEAU[12]
    M = np.array([[_BAM[7], _BPM[7]], [_BAM[17], _BPM[17]]])
    A, B = np.linalg.solve(M, [am - m * _PLATEAU[7], pm - m * _PLATEAU[17]])
    return m * _PLATEAU + max(A, 0) * _BAM + max(B, 0) * _BPM


# one loop fault per station in 2025: the direction, when the fault began and when the crew's repair put it right
# (local time), and what the fault did to that direction's count (a dead lane loop undercounts by roughly that
# lane's share; a crosstalking detector card counts some vehicles twice)
FAULTS = {
    "S-0101": ("EB", dt.datetime(2025, 4, 8, 13), dt.datetime(2025, 4, 22, 10), 0.62, 3, "open"),
    "S-0102": ("WB", dt.datetime(2025, 9, 16, 7), dt.datetime(2025, 9, 30, 11), 1.45, 1, "crosstalk"),
    "S-0103": ("EB", dt.datetime(2025, 5, 6, 15), dt.datetime(2025, 5, 16, 9), 0.52, 1, "open"),
    "S-0104": ("SB", dt.datetime(2025, 1, 28, 4), dt.datetime(2025, 2, 10, 13), 0.52, 2, "open"),
    "S-0105": ("NB", dt.datetime(2025, 6, 3, 19), dt.datetime(2025, 6, 16, 10), 0.62, 3, "open"),
    "S-0106": ("SB", dt.datetime(2025, 8, 5, 11), dt.datetime(2025, 8, 19, 14), 0.52, 2, "open"),
    "S-0107": ("NB", dt.datetime(2025, 11, 4, 2), dt.datetime(2025, 11, 17, 9), 0.52, 1, "open"),
    "S-0108": ("WB", dt.datetime(2025, 3, 3, 16), dt.datetime(2025, 3, 14, 10), 0.52, 2, "open"),
}
MISSED_RATE = 14          # missed polls per station-year (the station's counter carries them into the next poll)


def _day_hours(day):
    hours = list(range(1, 25))
    if day == DST_ON:
        hours = [h for h in hours if h != 3]
    elif day == DST_OFF:
        hours = hours[:2] + [2] + hours[2:]
    return hours


STATION_SEED = {'S-0101': 87, 'S-0102': 27, 'S-0103': 16, 'S-0104': 4, 'S-0105': 0, 'S-0106': 0, 'S-0107': 3, 'S-0108': 0}


def atr_records(links, base, stations=None, seeds=None):
    """hourly two-direction volumes for every station through 2025, as the count program's server exports them"""
    seeds = STATION_SEED if seeds is None else seeds
    month_f = np.array([0.90, 0.93, 0.97, 1.00, 1.03, 1.05, 1.06, 1.06, 1.03, 1.02, 0.98, 0.95])
    dow_f = np.array([1.00, 1.02, 1.03, 1.03, 1.05, 0.80, 0.68])        # Monday .. Sunday
    out = []
    outages, missed = {}, {}
    days = [dt.date(2025, 1, 1) + dt.timedelta(days=i) for i in range(365)]
    for idx, (st, loc, (a, b), dab, dba) in enumerate(STATIONS):
        if stations is not None and st not in stations:
            continue
        rng = np.random.default_rng([P.SEED, 25, idx, seeds.get(st, 0)])
        # outage spells: logger dark for a run of days (zeros, status NR) and vendor-estimated stretches (EST)
        spells = []
        for _ in range(int(rng.integers(1, 4))):
            d0 = dt.date(2025, 1, 1) + dt.timedelta(days=int(rng.integers(5, 350)))
            spells.append((d0, d0 + dt.timedelta(days=int(rng.integers(1, 6))), "NR"))
        for _ in range(int(rng.integers(1, 3))):
            d0 = dt.date(2025, 1, 1) + dt.timedelta(days=int(rng.integers(5, 350)))
            spells.append((d0, d0 + dt.timedelta(days=int(rng.integers(0, 3))), "EST"))
        outages[st] = spells
        keys = [(day, h) for day in days for h in _day_hours(day)]
        n = len(keys)
        status = np.array(["OK"] * n, dtype=object)
        for i, (day, h) in enumerate(keys):
            for s0, s1, code in spells:
                if s0 <= day <= s1:
                    status[i] = code
        vols = {}
        for (x, y), dlab in (((a, b), dab), ((b, a), dba)):
            k = directed_index(links, x, y)
            bg = LOCAL_BG.get(st, 0)
            prof_d = day_shape(base["AM"][k] + bg, base["PM"][k] + bg) * rng.normal(1.0, 0.06)
            prof = day_shape(0.7 * (base["AM"][k] + base["PM"][k]) / 2 + bg, 0.7 * (base["AM"][k] + base["PM"][k]) / 2 + bg,
                             weekend=True)
            v = np.zeros(n, int)
            i = 0
            for day in days:
                dow = day.weekday()
                f = month_f[day.month - 1] * dow_f[dow] * rng.normal(1.0, 0.035)
                if day in HOLIDAYS_2025:
                    f *= 0.62
                p = prof_d if dow < 5 and day not in HOLIDAYS_2025 else prof
                dv = rng.poisson(np.maximum(f * p * (1 + rng.normal(0, 0.03, 24)), 0))
                if day == DST_ON:
                    dv = np.delete(dv, 2)
                elif day == DST_OFF:
                    dv = np.insert(dv, 2, int(dv[1] * 0.93))
                v[i:i + len(dv)] = dv
                i += len(dv)
            # the loop fault on its direction
            fd, f0, f1, fac, _, _ = FAULTS[st]
            if dlab == fd:
                for j, (day, h) in enumerate(keys):
                    t = dt.datetime(day.year, day.month, day.day) + dt.timedelta(hours=h - 1)
                    if f0 <= t < f1:
                        v[j] = int(rng.binomial(v[j], fac)) if fac < 1 else v[j] + int(rng.binomial(v[j], fac - 1))
            vols[dlab] = v
        st_est = status == "EST"
        for dlab in vols:
            vols[dlab] = np.where(st_est, (vols[dlab] * 0.97).astype(int), vols[dlab])
            vols[dlab] = np.where(status == "NR", 0, vols[dlab])
        # missed polls: the station does not answer (NR, zero written) and its counters carry the missed hours'
        # vehicles into the next answered poll
        runs = []
        taken = np.zeros(n, bool)
        for _ in range(int(rng.poisson(MISSED_RATE))):
            for _try in range(50):
                L = 1 if rng.random() < 0.8 else 2
                p0 = int(rng.integers(0, n - L - 1))
                seg = slice(p0, p0 + L + 1)
                if (status[seg] == "OK").all() and not taken[max(p0 - 1, 0):p0 + L + 2].any() \
                        and keys[p0][0] not in (DST_ON, DST_OFF) and keys[p0 + L][0] not in (DST_ON, DST_OFF):
                    taken[seg] = True
                    runs.append((p0, L))
                    break
        for p0, L in runs:
            for dlab in vols:
                vols[dlab][p0 + L] += int(vols[dlab][p0:p0 + L].sum())
                vols[dlab][p0:p0 + L] = 0
            status[p0:p0 + L] = "NR"
        missed[st] = [(keys[p0], L) for p0, L in runs]
        for (x, y), dlab in (((a, b), dab), ((b, a), dba)):
            v = vols[dlab]
            for j, (day, h) in enumerate(keys):
                sid = st
                if st == REPLACED[0] and day >= REPLACED[2]:
                    sid = REPLACED[1]
                out.append((sid, dlab, day.strftime("%m/%d/%Y"), h, int(v[j]), status[j]))
    df = pd.DataFrame(out, columns=["STATION", "DIR", "DATE", "HR_END", "VOLUME", "STATUS"])
    df = df.iloc[np.lexsort((np.arange(len(df)), df.DIR.values, df.STATION.values))].reset_index(drop=True)
    return df, dict(outages=outages, missed=missed)


# ---------------------------------------------------------------- probe travel times (CMP corridors)
CORRIDORS = [  # code, name, inbound direction label, node path inbound (AM peak direction)
    ("R9", "Route 9, Lakeview Road to Ferry Street", "NB", ["F1", "F2", "F3", "F4", "BN", "FX"]),
    ("CS", "Center Street, Millbrook Road to downtown", "EB", ["A3", "C3", "DT1"]),
    ("SP", "Southport Avenue, Millbrook Road to downtown", "EB", ["A1", "C1", "C2", "DT2"]),
    ("HA", "Harbor Avenue, Southport Bridge to Lakeview Parkway", "NB", ["C1", "C2", "C3", "C4"]),
]
OUTBOUND = {"NB": "SB", "EB": "WB"}


def segments(links):
    rows = []
    rng = np.random.default_rng(P.SEED + 31)
    n = 0
    for code, name, din, path in CORRIDORS:
        for d, seq in ((din, path), (OUTBOUND[din], list(reversed(path)))):
            for i, (a, b) in enumerate(zip(seq[:-1], seq[1:])):
                k = directed_index(links, a, b)
                l = links[k]
                n += 1
                ref = l["speed_mph"] * float(rng.uniform(0.90, 0.97))
                rows.append(dict(SEGMENT=f"112{'+' if d in ('NB', 'EB') else '-'}{4500 + n:05d}", CORRIDOR=code,
                                 CORRIDOR_NAME=name, DIR=d, SEQ=i + 1, LENGTH_MI=l["length_mi"],
                                 REF_SPEED_MPH=round(ref, 1), _k=k))
    return pd.DataFrame(rows)


def _utc(day, minute_local):
    off = 5 if DST_ON <= day < DST_OFF else 6
    t = dt.datetime(day.year, day.month, day.day) + dt.timedelta(minutes=minute_local + off * 60)
    return t


CORRIDOR_SEED = {'R9': 5, 'CS': 0, 'SP': 6, 'HA': 1}


def probe_records(links, base_t, t0, corridors=None, seeds=None):
    """15-minute segment travel times (seconds) through 2025, stamped in UTC as the probe vendor delivers them"""
    seeds = CORRIDOR_SEED if seeds is None else seeds
    seg = segments(links)
    codes = [c[0] for c in CORRIDORS]
    rngs = {c: np.random.default_rng([P.SEED, 37, i, seeds.get(c, 0)]) for i, c in enumerate(codes)}
    rows_seg, rows_ts, rows_tt = [], [], []
    mins = np.arange(0, 1440, 15)
    am_shape = np.exp(-0.5 * ((mins + 7.5 - 478) / 42.0) ** 2)
    pm_shape = np.exp(-0.5 * ((mins + 7.5 - 1072) / 50.0) ** 2)
    for _, s in seg.iterrows():
        if corridors is not None and s.CORRIDOR not in corridors:
            continue
        rng = rngs[s.CORRIDOR]
        k = int(s["_k"])
        ff = 3600 * s.LENGTH_MI / s.REF_SPEED_MPH
        sig = 0.28 if links[k]["ftype"] in ("arterial", "collector") else 0.0     # signal delay at the peak
        c_am = max(base_t["AM"][k] / t0[k] - 1, 0.02) + sig
        c_pm = max(base_t["PM"][k] / t0[k] - 1, 0.02) + sig
        day = dt.date(2025, 1, 1)
        while day.year == 2025:
            wk = day.weekday() < 5 and day not in HOLIDAYS_2025
            sev = float(rng.lognormal(0, 0.35))
            inc = rng.random() < 0.035
            prof = (c_am * am_shape + c_pm * pm_shape) * (sev if wk else 0.15)
            if inc:
                h0 = int(rng.integers(0, 96))
                prof[h0:h0 + int(rng.integers(2, 8))] += float(rng.uniform(1.0, 3.5))
            tt = ff * (1.04 + prof) * (1 + rng.normal(0, 0.02, 96))
            miss = rng.random(96) < 0.012
            for i, m in enumerate(mins):
                if miss[i]:
                    continue
                rows_seg.append(s.SEGMENT)
                rows_ts.append(_utc(day, int(m) + 15).strftime("%Y-%m-%dT%H:%M:%SZ"))
                rows_tt.append(round(float(tt[i]), 1))
            day += dt.timedelta(days=1)
    df = pd.DataFrame({"segment_id": rows_seg, "measurement_tstamp": rows_ts, "travel_time_seconds": rows_tt})
    return seg, df


# ---------------------------------------------------------------- distractors
def crash_table():
    rng = np.random.default_rng(P.SEED + 41)
    rows = []
    for _, loc, (a, b), _, _ in STATIONS:
        for y in range(2021, 2026):
            k = int(rng.poisson(14 if "Route 9" in loc else 9))
            inj = int(rng.binomial(k, 0.28))
            rows.append(dict(Segment=loc, Year=y, Crashes=k, Injury=inj, Fatal=int(rng.binomial(inj, 0.03)),
                             PDO=k - inj))
    return pd.DataFrame(rows)


def transit_table():
    rng = np.random.default_rng(P.SEED + 43)
    routes = [("4", "Center Street Crosstown", 1850, 760, 2240), ("7", "Southport - Harbor", 1320, 610, 1980),
              ("12", "Millbrook Express", 940, 0, 1160), ("15", "Lakeview Parkway", 1110, 520, 1720),
              ("22", "Downtown Circulator", 2630, 1480, 2050), ("31", "Quarry Lane Flex", 210, 95, 640)]
    season = {7: 0.91, 8: 0.94, 9: 1.04, 10: 1.05, 11: 1.01, 12: 0.93, 1: 0.96, 2: 1.0, 3: 1.03, 4: 1.04, 5: 1.02, 6: 0.95}
    rows = []
    for r, nm, wk, sat, hrs in routes:
        trend = 1.0
        for m in range(7, 19):
            yr, mo = (2024, m) if m <= 12 else (2025, m - 12)
            trend *= rng.normal(1.003, 0.006)
            f = season[mo] * trend
            rows.append(dict(route=r, route_name=nm, service_month=f"{yr}-{mo:02d}",
                             weekday_avg_boardings=int(round(wk * f * rng.normal(1, 0.025))),
                             saturday_avg_boardings=int(round(sat * f * rng.normal(1, 0.04))) if sat else 0,
                             revenue_hours=int(round(hrs * (1.0 if mo not in (12, 7) else 0.97) + rng.integers(-15, 16)))))
    return pd.DataFrame(rows)
