"""The records the company and its laboratory keep: the stations' 15-minute logger record, the field team's sample
sheet, the laboratory's results, the maintenance log, the laboratory's 2027 batch export, the station register and
the two neighbouring series (precipitation, reservoir levels). Everything the published loads and the review read is
built here; the documents are in docs.py."""
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import params as P
import sim

OSLO = ZoneInfo("Europe/Oslo")
UTC = dt.timezone.utc
STEP = pd.date_range("2025-01-01 00:00", periods=sim.N, freq="15min", tz="UTC")
Y26_END = sim.Y27.start          # first step of 2027
GUARD = 12                        # three hours either side of a calibration sample stay clean
CODE_SWITCH = pd.Timestamp("2026-04-14 06:00", tz="UTC")   # the data team's database migration: new flag letters


def _t(k):
    return STEP[int(k)].to_pydatetime()


def _local(ts_utc):
    return ts_utc.astimezone(OSLO)


# ------------------------------------------------------------------ the 15-minute record and its history
def _free(mask, idx, a, b):
    """is the step range [a, b) clear of every calibration sample by GUARD steps and of anything already placed"""
    if a < 0 or b > Y26_END or mask[a:b].any():
        return False
    near = idx[(idx >= a - GUARD) & (idx < b + GUARD)]
    return len(near) == 0


def sample_steps(key, d):
    """the 15-minute steps of the bottles the programme brought back (the same draw samples() makes)"""
    return np.array(sorted(r[0] for r in _program(d, np.random.default_rng(P.SEED[key] + 31))))


def record_history(key, d, rng):
    """the swap date, the maintenance visits (sensor out of the water), the fouled spans, the logger outages and
    the re-sent rows, all inside 2025 and 2026 and clear of every calibration sample"""
    idx = sample_steps(key, d)
    order = P.KEYS.index(key)
    used = np.zeros(sim.N, bool)
    swap_day = dt.date(2026, 9, 7) + dt.timedelta(days=int(order * 5 + rng.integers(0, 4)))
    gap_len = int(rng.integers(3, 7))
    for _ in range(30):
        swap_local = dt.datetime.combine(swap_day, dt.time(10 + int(rng.integers(0, 4)), int(rng.integers(0, 4)) * 15 + 7),
                                         tzinfo=OSLO)
        swap_k = int((swap_local.astimezone(UTC) - P.T0).total_seconds() // 900) + 1
        if _free(used, idx, swap_k - 1, swap_k + gap_len):
            break
        swap_day += dt.timedelta(days=1)
    else:
        raise AssertionError("no free swap time at " + key)
    used[swap_k - 1:swap_k + gap_len] = True
    visits, fouled, outages = [], [], []
    # cleaning visits roughly every four weeks from April to November, every eight in winter
    day = dt.date(2025, 1, 6) + dt.timedelta(days=int(rng.integers(0, 20)))
    last_clean = None
    while day < swap_day - dt.timedelta(days=10):
        gap = 28 if 4 <= day.month <= 11 else 56
        for _ in range(12):
            minute = int(rng.integers(0, 60))
            minute += 1 if minute % 15 == 0 else 0           # field watches are not set to the quarter hour
            start_local = dt.datetime.combine(day, dt.time(int(rng.integers(8, 15)), minute), tzinfo=OSLO)
            minutes = int(rng.integers(25, 111))
            minutes += 1 if (minute + minutes) % 15 == 0 else 0
            a = int((start_local.astimezone(UTC) - P.T0).total_seconds() // 900) + 1
            b = int(((start_local + dt.timedelta(minutes=minutes)).astimezone(UTC) - P.T0).total_seconds() // 900) + 1
            if b > a and _free(used, idx, a, b):
                break
            day += dt.timedelta(days=1)
        else:
            day += dt.timedelta(days=gap)
            continue
        found_fouled = (last_clean is not None and 6 <= day.month <= 9 and rng.uniform() < 0.4)
        visit = {"start": start_local, "minutes": minutes, "a": a, "b": b, "fouled": False,
                 "check": bool(rng.uniform() < 0.35)}
        if found_fouled:
            # the data team flags back from the visit to the day the optics were last known clean
            span = int(rng.integers(2, 8)) * 96
            fa = max(a - span, last_clean)
            if _free(used, idx, fa, a):
                fouled.append((fa, a))
                used[fa:a] = True
                visit["fouled"] = True
        used[a:b] = True
        visits.append(visit)
        last_clean = b
        day += dt.timedelta(days=gap + int(rng.integers(-5, 6)))
    # logger outages: no rows at all
    for _ in range(int(rng.integers(2, 6))):
        for _ in range(40):
            length = int(rng.integers(6 * 4, 4 * 96))
            a = int(rng.integers(96, Y26_END - length - 96))
            if _free(used, idx, a, a + length):
                outages.append((a, a + length))
                used[a:a + length] = True
                break
    gap = (swap_k - 1, swap_k + gap_len)                        # the old logger off until the new one starts
    late = []
    for _ in range(int(rng.integers(1, 3))):
        for _ in range(40):
            k = int(rng.integers(gap[1] + 96, Y26_END - 96))
            if _free(used, idx, k, k + 1):
                late.append(k); used[k] = True
                break
    return {"swap_local": swap_local, "swap_k": swap_k, "swap_gap": gap, "visits": visits, "fouled": fouled,
            "outages": outages, "late_checks": late}


def logger_record(key, d, hist, rng):
    """one station's 15-minute rows as the logger network delivered them"""
    T = d["T"].copy()
    rec_T = T.copy()
    sk = hist["swap_k"]
    flag = np.full(sim.N, "", dtype=object)
    new_codes = STEP >= CODE_SWITCH
    for fa, fb in hist["fouled"]:
        drift = np.linspace(0.02, rng.uniform(0.25, 0.6), fb - fa)
        rec_T[fa:fb] = T[fa:fb] * (1 + drift)
        flag[fa:fb] = np.where(new_codes[fa:fb], "F", "G")
    for v in hist["visits"]:
        if v["check"] and v["a"] - 1 >= 0:
            flag[v["a"] - 1] = "C" if new_codes[v["a"] - 1] else "K"     # checked against the handheld meter first
        rec_T[v["a"]:v["b"]] = rng.uniform(0.1, 1.5, v["b"] - v["a"])     # the sonde in the air or the bucket
        flag[v["a"]:v["b"]] = np.where(new_codes[v["a"]:v["b"]], "M", "O")
    for k in hist.get("late_checks", []):
        flag[k] = "C"
    old = np.arange(sim.N) < sk
    rec_T = np.where(old, np.minimum(rec_T, P.OLD_LIMIT), np.minimum(rec_T, P.NEW_LIMIT))
    rec_T = np.round(rec_T, 1)
    doy = sim.DOY
    base_t = {"glacier": 0.6, "rain": 2.5, "lake": 3.0}[d["kind"]]
    amp_t = {"glacier": 4.5, "rain": 10.5, "lake": 13.0}[d["kind"]]
    wt = base_t + amp_t * np.clip(np.sin(np.pi * (doy - 110) / 200), 0, None) + 0.6 * np.sin(2 * np.pi * (sim.HOD - 15) / 24)
    wt = np.round(np.clip(wt + rng.normal(0, 0.15, sim.N), 0.0, None), 1)
    keep = np.ones(sim.N, bool)
    for a, b in hist["outages"] + [hist["swap_gap"]]:
        keep[a:b] = False
    df = pd.DataFrame({"station": P.CODE[key], "time_utc": STEP, "discharge_m3s": d["qp"], "turbidity_fnu": rec_T,
                       "water_temp_c": wt, "flag": flag})
    df = df[keep]
    # after each outage the logger re-sent its last hours before the gap
    extra = []
    for a, b in hist["outages"]:
        n = int(rng.integers(8, 49))
        lo = max(0, a - n)
        extra.append(df[(df["time_utc"] >= STEP[lo]) & (df["time_utc"] < STEP[a])])
    if extra:
        df = pd.concat([df] + extra)
        df = df.sort_values("time_utc", kind="mergesort")
    return df.reset_index(drop=True)


def unusable_intervals(df, hist):
    """intervals of 2025 and 2026 with no row, a fouling or sonde-out flag (either letter set), or a TS-10 reading at
    its limit: the count the spring review's turbidity line reports"""
    pre = df[df["time_utc"] < pd.Timestamp("2027-01-01", tz="UTC")].drop_duplicates(["station", "time_utc"])
    missing = Y26_END - len(pre)
    flagged = pre["flag"].isin(["F", "M", "G", "O"])
    ceil = (pre["time_utc"] < STEP[hist["swap_k"]]) & (pre["turbidity_fnu"] >= P.OLD_LIMIT) & ~flagged
    return int(missing + flagged.sum() + ceil.sum())


def settle_quarter_hours(key, d, hist, make_df):
    """the review reports whole hours: lengthen the station's last cleaning visit of 2025 by a quarter of an hour
    until the count of intervals does not fall on a half hour"""
    idx = sample_steps(key, d)
    for _ in range(3):
        df = make_df(hist)
        if unusable_intervals(df, hist) % 4 != 2:
            return hist, df
        v = [x for x in hist["visits"] if x["b"] < 35040][-1]
        assert len(idx[(idx >= v["b"] - GUARD) & (idx < v["b"] + 1 + GUARD)]) == 0
        v["b"] += 1
        v["minutes"] += 15
    raise AssertionError("no settled count at " + key)


# ------------------------------------------------------------------ samples: the field sheet and the laboratory
def _program(d, rng):
    """the bottles the programme actually brought back: some rounds were missed (weather, illness, a closed road),
    some callouts took a third bottle as the flood went on, a few came back with one"""
    idx, src, trip, s = list(d["idx"]), list(d["src"]), list(d["trip"]), list(d["s"])
    keep = [not (sr == "routine" and rng.uniform() < 0.07) for sr in src]
    out = [(k, sr, tr, v) for k, sr, tr, v, kp in zip(idx, src, trip, s, keep) if kp]
    by_trip = {}
    for row in out:
        if row[1] == "callout":
            by_trip.setdefault(row[2], []).append(row)
    extra, drop = [], set()
    for tr, rows in sorted(by_trip.items()):
        u = rng.uniform()
        if u < 0.22 and len(rows) == 2:
            k3 = rows[-1][0] + int(rng.uniform(1.0, 2.5) / sim.DT)
            if k3 < sim.N:
                extra.append((k3, "callout", tr, float(d["ssc"][k3] * rng.lognormal(0, 0.06))))
        elif u > 0.92 and len(rows) == 2:
            drop.add((rows[-1][0], tr))
    out = [r for r in out if (r[0], r[2]) not in drop] + extra
    out.sort(key=lambda r: (r[0], r[1]))
    return out


def samples(W, rng):
    """every calibration bottle: its station, its UTC time to the minute, the trip it came from, its result"""
    rows = []
    for key in P.KEYS:
        d = W[key]
        for k, src, trip, s in _program(d, np.random.default_rng(P.SEED[key] + 31)):
            t = _t(k) + dt.timedelta(minutes=int(rng.integers(-7, 8)))
            loc = _local(t)
            # nobody samples inside the hour the clocks go back twice
            if loc.fold == 1 or (loc.month == 10 and loc.day >= 25 and loc.hour == 2):
                t += dt.timedelta(hours=1)
            rows.append({"key": key, "k": int(k), "utc": t, "src": src, "trip": int(trip), "ssc": float(s)})
    S = pd.DataFrame(rows).sort_values(["utc", "key"], kind="mergesort").reset_index(drop=True)
    S["year"] = [_local(t).year for t in S["utc"]]
    S["bottle"] = S.groupby("year").cumcount() + 1
    # callouts numbered by the year of the flood, in order
    co = S[S["src"] == "callout"].drop_duplicates(["key", "trip"])[["key", "trip", "utc"]]
    co = co.sort_values("utc", kind="mergesort")
    co["year"] = [_local(t).year for t in co["utc"]]
    co["ref"] = ["U-%d-%02d" % (y, i + 1) for y, i in zip(co["year"], co.groupby("year").cumcount())]
    S = S.merge(co[["key", "trip", "ref"]], on=["key", "trip"], how="left")
    S["ref"] = S["ref"].fillna("")
    S["ssc_lab"] = np.round(S["ssc"], 1)
    return S


def field_sheet(S, rng):
    crews = ["LP/HB", "LP/KS", "HB/KS", "KS/OR", "LP/OR"]
    remarks_r = ["", "", "", "", "", "ice along the banks", "low water", "light rain", "wind, sampled from the bridge"]
    remarks_c = ["", "", "high water", "brown water", "debris on the cable", "heavy rain", ""]
    out = []
    for r in S.itertuples():
        loc = _local(r.utc)
        out.append({"bottle_no": r.bottle, "station": P.CODE[r.key], "sampled": loc.isoformat(timespec="minutes"),
                    "trip": "flood callout" if r.src == "callout" else "routine round",
                    "callout_ref": r.ref, "sampler": "depth-integrating (US DH-48 type)",
                    "crew": crews[int(rng.integers(0, len(crews)))],
                    "remarks": (remarks_c if r.src == "callout" else remarks_r)[int(rng.integers(0, 7))]})
    return pd.DataFrame(out)


def lims(S, rng):
    """the laboratory's results: 2025 from the old LIMS (Norwegian layout), 2026 and 2027 from the new one, where a
    corrected result keeps the replaced one beside it"""
    old, new = [], []
    for r in S.itertuples():
        loc = _local(r.utc)
        rec = loc.date() + dt.timedelta(days=int(rng.integers(1, 5)))
        ana = rec + dt.timedelta(days=int(rng.integers(2, 12)))
        if r.year == 2025:
            old.append({"Prøvenr": "%02d-%04d" % (r.year % 100, r.bottle), "Stasjon": P.CODE[r.key],
                        "Prøvetatt": loc.strftime("%d.%m.%Y"), "Mottatt": rec.strftime("%d.%m.%Y"),
                        "Analysert": ana.strftime("%d.%m.%Y"), "SS mg/l": r.ssc_lab, "Merknad": ""})
        else:
            sid = "%d-%04d" % (r.year, r.bottle)
            lab_no = "SMA-%d-%05d" % (r.year, 1000 + int(r.bottle) * 3 + int(rng.integers(0, 3)))
            base = {"sample_id": sid, "station": P.CODE[r.key], "collected": loc.strftime("%Y-%m-%d"),
                    "received": rec.isoformat(), "analysed": ana.isoformat(), "lab_no": lab_no}
            if rng.uniform() < 0.025:
                wrong = round(r.ssc_lab * rng.choice([0.86, 0.9, 1.12, 1.17]), 1)
                new.append(dict(base, ssc_mg_l=wrong, status="replaced", comment="re-weighed, see corrected result"))
                new.append(dict(base, ssc_mg_l=r.ssc_lab, status="final", comment="corrected after re-weighing",
                                analysed=(ana + dt.timedelta(days=int(rng.integers(3, 9)))).isoformat()))
            else:
                new.append(dict(base, ssc_mg_l=r.ssc_lab, status="final", comment=""))
    cols = ["sample_id", "station", "collected", "received", "analysed", "lab_no", "ssc_mg_l", "status", "comment"]
    return pd.DataFrame(old), pd.DataFrame(new)[cols]


# ------------------------------------------------------------------ the laboratory's 2027 batches (Ask B)
LOTS = [("KS-26-11", 50.0, dt.date(2027, 1, 1), dt.date(2027, 6, 30)),
        ("KS-27-06", 54.0, dt.date(2027, 7, 1), dt.date(2028, 3, 31))]


def batches(S, rng):
    """2027's samples gathered into weighing batches; each batch carries a filter blank and two aliquots of the
    control suspension, and the export repeats the batch's control results on every sample line"""
    s27 = S[S["year"] == 2027].copy()
    s27["recv"] = [(_local(t).date() + dt.timedelta(days=2)) for t in s27["utc"]]
    s27 = s27.sort_values(["recv", "bottle"], kind="mergesort")
    groups, cur, start = [], [], None
    for r in s27.itertuples():
        width = 7 if 5 <= r.recv.month <= 10 else 14
        if cur and (r.recv - start).days >= width:
            groups.append(cur); cur = []
        if not cur:
            start = r.recv
        cur.append(r)
    if cur:
        groups.append(cur)
    out, truth = [], []
    for i, g in enumerate(groups):
        weighed = max(r.recv for r in g) + dt.timedelta(days=int(rng.integers(3, 7)))
        while weighed.weekday() >= 5:
            weighed += dt.timedelta(days=1)
        lot, cert = [(l, c) for l, c, a, b in LOTS if a <= weighed <= b][0]
        vol = 200 if rng.uniform() < 0.2 else 250
        blank = round(float(rng.normal(0.0, 0.18)), 2)
        rec1, rec2 = rng.normal(1.0, 0.025, 2)
        truth.append({"batch": i, "weighed": weighed, "lot": lot, "cert": cert, "vol": vol, "blank": blank,
                      "rec1": rec1, "rec2": rec2})
        out.append(g)
    return out, truth


def plant_failures(truth, rng):
    """the year's real deviations: blanks over 0.5 mg, an aliquot outside 90 to 110 per cent, two aliquots more than
    10 per cent apart; spread so most months hold one or two"""
    n = len(truth)
    months = np.array([t["weighed"].month for t in truth])
    picks = []
    for m in range(1, 13):
        cand = [i for i in range(n) if months[i] == m]
        if not cand:
            continue
        k = int(rng.choice([0, 1, 1, 1, 2, 2])) if len(cand) > 1 else int(rng.choice([0, 1]))
        picks += list(rng.choice(cand, min(k, len(cand)), replace=False))
    # every batch's controls sit well inside the limits unless a deviation is set below
    for t in truth:
        while not (0.93 <= t["rec1"] <= 1.07 and 0.93 <= t["rec2"] <= 1.07
                   and abs(t["rec1"] - t["rec2"]) / ((t["rec1"] + t["rec2"]) / 2) < 0.08):
            t["rec1"], t["rec2"] = rng.normal(1.0, 0.025, 2)
        if abs(t["blank"]) > 0.4:
            t["blank"] = round(float(np.sign(t["blank"]) * rng.uniform(0.05, 0.4)), 2)
    kinds = ["blank", "low", "high", "apart"]
    for j, i in enumerate(sorted(picks)):
        t = truth[i]
        kind = kinds[j % 4]
        if kind == "blank":
            t["blank"] = round(float(rng.choice([-1, 1]) * rng.uniform(0.62, 1.1)), 2)
        elif kind == "low":
            t["rec1"] = rng.uniform(0.84, 0.885)
        elif kind == "high":
            t["rec2"] = rng.uniform(1.115, 1.15)
        else:
            t["rec1"], t["rec2"] = rng.uniform(0.94, 0.96), rng.uniform(1.07, 1.085)
    return truth


def batch_export(groups, truth):
    rows = []
    for g, t in zip(groups, truth):
        m1 = round(t["cert"] * t["rec1"] * t["vol"] / 1000, 2)
        m2 = round(t["cert"] * t["rec2"] * t["vol"] / 1000, 2)
        bno = "SS-27-%03d" % (t["batch"] + 1)
        for r in g:
            rows.append({"batch": bno, "weighed": t["weighed"].strftime("%d.%m.%Y"),
                         "sample_id": "2027-%04d" % r.bottle, "blank_change_mg": t["blank"],
                         "control_lot": t["lot"], "control_nominal_mg_l": 50.0,
                         "control_1_mass_mg": m1, "control_1_volume_ml": t["vol"],
                         "control_2_mass_mg": m2, "control_2_volume_ml": t["vol"]})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ register, maintenance log, neighbours
def register(H):
    rows = []
    for key, code, name, river, res, area, glac, _ in P.STATIONS:
        kind = P.SPEC[key][0]
        rows.append({"station": code, "name": name, "river": river, "reservoir": res,
                     "regime": P.KIND_LABEL[kind], "catchment_km2": area, "glacier_cover_pct": glac,
                     "turbidity_sensor": P.NEW_SENSOR, "sensor_installed": H[key]["swap_local"].date().isoformat(),
                     "discharge": "pressure transducer, station rating",
                     "sampling_point": "bridge" if P.KEYS.index(key) % 3 else "cableway"})
    return pd.DataFrame(rows)


def maintenance_log(H, rng):
    techs = ["OR", "KS", "HB", "AV"]
    rows = []
    for key in P.KEYS:
        h = H[key]
        for v in h["visits"]:
            out_ = v["start"]
            in_ = out_ + dt.timedelta(minutes=v["minutes"])
            rows.append({"date": out_.strftime("%d.%m.%Y"), "station": P.CODE[key], "visit": "cleaning",
                         "sonde_out": out_.strftime("%H:%M"), "sonde_in": in_.strftime("%H:%M"),
                         "technician": techs[int(rng.integers(0, 4))],
                         "remarks": ("handheld turbidimeter before removal; " if v["check"] else "")
                         + ("heavy growth on the optical window, readings flagged back to last clean"
                            if v["fouled"] else ["optics wiped", "optics wiped, logger battery changed",
                                                 "optics wiped, cable checked", "optics wiped"][int(rng.integers(0, 4))])})
        s = h["swap_local"]
        rows.append({"date": s.strftime("%d.%m.%Y"), "station": P.CODE[key], "visit": "sensor replaced",
                     "sonde_out": s.strftime("%H:%M"), "sonde_in": (s + dt.timedelta(minutes=50)).strftime("%H:%M"),
                     "technician": techs[int(rng.integers(0, 4))],
                     "remarks": "%s removed; %s with wiper installed, logger replaced" % (P.OLD_SENSOR, P.NEW_SENSOR)})
        for k in h["late_checks"]:
            t = _local(_t(k))
            rows.append({"date": t.strftime("%d.%m.%Y"), "station": P.CODE[key], "visit": "handheld check",
                         "sonde_out": "", "sonde_in": "", "technician": techs[int(rng.integers(0, 4))],
                         "remarks": "handheld turbidimeter at %s, sonde left in place" % t.strftime("%H:%M")})
        day = dt.date(2027, 2, 1) + dt.timedelta(days=int(rng.integers(0, 20)))
        while day.year == 2027:
            rows.append({"date": day.strftime("%d.%m.%Y"), "station": P.CODE[key], "visit": "wiper check",
                         "sonde_out": "", "sonde_in": "", "technician": techs[int(rng.integers(0, 4))],
                         "remarks": "serviced in place, sonde not removed"})
            day += dt.timedelta(days=int(rng.integers(50, 80)))
    L = pd.DataFrame(rows)
    L["_d"] = pd.to_datetime(L["date"], format="%d.%m.%Y")
    return L.sort_values(["_d", "station"], kind="mergesort").drop(columns="_d").reset_index(drop=True)


def precipitation(cal, rng):
    days = pd.date_range("2025-01-01", "2027-12-31", freq="D")
    rows = []
    storm_days = set(int(k * sim.DT // 24) for k in cal)
    for name, scale in (("Fjellbrekke kraftstasjon", 1.0), ("Juvstøl", 1.35)):
        for i, d in enumerate(days):
            wet = rng.uniform() < 0.48
            mm = rng.gamma(0.9, 6.0) * scale if wet else 0.0
            if i in storm_days or (i - 1) in storm_days:
                mm += rng.uniform(25, 70) * scale
            doy = d.dayofyear
            tair = -3.5 + 15.5 * np.sin(np.pi * (doy - 95) / 230) * (doy > 95) * (doy < 325) + rng.normal(0, 2.2)
            rows.append({"station": name, "date": d.date().isoformat(), "precip_mm": round(float(mm), 1),
                         "air_temp_c": round(float(tair), 1)})
    return pd.DataFrame(rows)


def reservoir_levels(rng):
    days = pd.date_range("2025-01-01", "2027-12-31", freq="D")
    rows = []
    for name, hrv, lrv, area_km2 in (("Breiavatn", 1062.0, 1021.0, 6.4), ("Kvitstølvatn", 948.0, 915.0, 3.9),
                                     ("Djupevatn", 811.0, 776.0, 5.1)):
        lvl = lrv + 6
        for d in days:
            doy = d.dayofyear
            inflow = 0.9 if 150 < doy < 280 else -0.25
            lvl = float(np.clip(lvl + inflow * rng.uniform(0.1, 0.5) + rng.normal(0, 0.05), lrv, hrv))
            rows.append({"reservoir": name, "date": d.date().isoformat(), "level_masl": round(lvl, 2),
                         "volume_mm3": round((lvl - lrv) * area_km2, 1)})
    return pd.DataFrame(rows)
