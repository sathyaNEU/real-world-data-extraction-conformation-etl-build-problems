"""Simulate task452's world: each gage's daily discharge over water years 2024 to 2026 (regional storms, snowmelt,
base flow), each station's daily mean total phosphorus (rising with discharge, seasonal, with day-to-day scatter),
and the samples: the commission's fixed monthly visits and the college laboratory's storm samples."""
import datetime as dt

import numpy as np

import world as W

DAYS = [W.WY_START + dt.timedelta(days=i) for i in range((W.WY_END - W.WY_START).days + 1)]
N = len(DAYS)
DOY = np.array([d.timetuple().tm_yday for d in DAYS])
WYR = np.array([d.year + (1 if d.month >= 10 else 0) for d in DAYS])


def regional_storms(rng):
    """the basin's storms: dates and regional size (rain events and rain on snow)"""
    out = []
    t = 0
    while t < N:
        m = DAYS[t].month
        rate = 1 / 9.0 if m in (3, 4, 5, 10, 11) else (1 / 13.0 if m in (6, 7, 8, 9) else 1 / 18.0)
        t += int(rng.exponential(1 / rate)) + 2
        if t >= N:
            break
        out.append((t, float(rng.lognormal(0.0, 0.75))))
    return out


def flows(rng, storms):
    """daily mean discharge (cfs) at each gage"""
    Q = {}
    for code, name, st, lab, gage, da_s, da_g, qmed, flash, lc0, b, sig, amp, reach, role in W.TRIBS:
        seas = (1 + 1.6 * np.exp(-((DOY - 102) / 22.0) ** 2) - 0.55 * np.exp(-((DOY - 240) / 38.0) ** 2)
                + 0.25 * np.exp(-((DOY - 320) / 30.0) ** 2))
        base = qmed * 0.62 * seas * np.exp(np.cumsum(rng.normal(0, 0.035, N)) * 0.0 + rng.normal(0, 0.06, N))
        ev = np.zeros(N)
        k = rng.uniform(0.32, 0.55) * (1.25 if flash > 1.2 else 1.0)
        for t, size in storms:
            mag = qmed * flash * 1.7 * size * float(rng.lognormal(0.0, 0.35))
            span = min(N, t + 30)
            ev[t:span] += mag * np.exp(-k * np.arange(span - t))
        Q[code] = base + ev
    return Q


def concentrations(rng, Q):
    """daily mean total phosphorus (mg/L) at each compliance station; discharge carried to an off-gage station by
    drainage-area ratio"""
    C, Qs = {}, {}
    for code, name, st, lab, gage, da_s, da_g, qmed, flash, lc0, b, sig, amp, reach, role in W.TRIBS:
        q = Q[code] * (da_s / da_g)
        Qs[code] = q
        med = float(np.median(q))
        lnc = lc0 + b * np.log(q / med) + amp * np.sin(2 * np.pi * (DOY - 80) / 365.25) + rng.normal(0, sig, N)
        C[code] = np.exp(lnc)
    return C, Qs


def visit_days(y, m):
    """the commission's round: the first and third Tuesdays of the month"""
    d = W.D(y, m, 1)
    while d.weekday() != 1:
        d += dt.timedelta(days=1)
    return [d, d + dt.timedelta(days=14)]


def samples(rng, Q, C):
    """sample days and grab concentrations per station: the commission's round (first and third Tuesdays) and the laboratory's
    storm samples, taken on weekdays on a high and rising discharge; in water years 2024 and 2025 across the storms,
    in water year 2026 on whichever storms the crews reached (modest ones at some stations, the spring peaks at
    others)"""
    idx = {d: i for i, d in enumerate(DAYS)}
    out = {}
    months = sorted({(d.year, d.month) for d in DAYS})
    for code, name, st, lab, gage, da_s, da_g, qmed, flash, lc0, b, sig, amp, reach, role in W.TRIBS:
        rows = []
        for y, m in months:
            for d in visit_days(y, m):
                if d in idx:
                    rows.append((idx[d], "monthly"))
        q = Q[code]
        q80, q92 = np.quantile(q, 0.80), np.quantile(q, 0.92)
        rising = [i for i in range(1, N) if q[i] > q[i - 1] and DAYS[i].weekday() < 5]
        for wy in (2024, 2025, 2026):
            if wy < 2026:
                # the laboratory's first seasons: storms across the range, the largest included
                n = W.PRIOR_STORMS.get(code, 3)
                big = sorted([i for i in rising if WYR[i] == wy and q[i] > q92], key=lambda i: -q[i])[:6]
                rest = [i for i in rising if WYR[i] == wy and q80 < q[i] <= q92]
                rng.shuffle(big)
                rng.shuffle(rest)
                cand = big[:2] + rest
            elif reach == "low":
                cand = [i for i in rising if WYR[i] == wy and q80 < q[i] < q92]
                n = 2
            elif reach == "high":
                cand = sorted([i for i in rising if WYR[i] == wy and DAYS[i].month in (3, 4, 5) and q[i] > q92],
                              key=lambda i: -q[i])
                n = 3
            else:
                cand = [i for i in rising if WYR[i] == wy and q[i] > q80]
                n = 2
            if reach != "high" and wy == 2026:
                rng.shuffle(cand)
            pick = []
            for i in cand:
                if all(abs(i - j) > 12 for j in pick):
                    pick.append(i)
                if len(pick) == n:
                    break
            rows += [(i, "storm") for i in sorted(pick)]
        rows.sort()
        grab = [(i, kind, float(C[code][i] * np.exp(rng.normal(0, 0.05)))) for i, kind in rows]
        out[code] = grab
    return out


# ------------------------------------------------------------------------------------------- the gage records
def unit_values(rng, Q):
    """water year 2026 at 15 minutes: each local day's values (96, or 92 and 100 on the days the clocks change), shaped
    within the day (a rising limb on a storm's first day, a slow fall after), averaging to the day's mean; timestamps
    in UTC, running without a gap or a repeat"""
    out = {}
    i26 = [i for i in range(N) if WYR[i] == 2026]
    for code, name, st, lab, gage, *_ in W.TRIBS:
        q = Q[code]
        vals = []
        for i in i26:
            d = DAYS[i]
            prev = q[i - 1] if i > 0 else q[i]
            nxt = q[i + 1] if i + 1 < N else q[i]
            x = np.linspace(0, 1, 96, endpoint=False)
            if q[i] > 1.25 * prev:              # a storm arrives during the day
                onset = rng.uniform(0.15, 0.7)
                shape = np.where(x < onset, prev / q[i], 1.0 + (x - onset) * 0.9)
            else:
                shape = 1.0 + (nxt - prev) / max(q[i], 1e-9) * (x - 0.5) * 0.5
            shape = np.maximum(shape, 0.2) * np.exp(rng.normal(0, 0.004, 96))
            # local midnight keeps the previous day's clock until 2am, so the day runs from there to the next midnight
            t0 = dt.datetime(d.year, d.month, d.day) + dt.timedelta(hours=W.utc_offset(d - dt.timedelta(days=1)))
            t1 = dt.datetime(d.year, d.month, d.day) + dt.timedelta(days=1, hours=W.utc_offset(d))
            n = int((t1 - t0).total_seconds() // 900)
            if n != 96:
                shape = np.interp(np.linspace(0, 95, n), np.arange(96), shape)
            v = q[i] * shape / shape.mean()
            for j in range(n):
                vals.append((t0 + dt.timedelta(minutes=15 * j), float(v[j])))
        out[code] = vals
    return out


def ice_days(rng):
    """gages whose winter record is estimated under ice, and the spans"""
    out = {}
    for code in ("KES", "TAM", "COR", "HES"):
        a = W.D(2026, 1, int(rng.integers(5, 20)))
        out[code] = (a, a + dt.timedelta(days=int(rng.integers(12, 30))))
    return out


# ------------------------------------------------------------------------------------- the laboratory results
def lab_rows(rng, Qs, C, S):
    """every result the two organisations report: total and dissolved phosphorus, suspended solids, chloride,
    nitrate and the field readings, with quality-control replicates and blanks, rejected results and the contract
    laboratory's change of units and name on 1 July 2025"""
    rows = []
    act = [0]
    trib = {t[0]: t for t in W.TRIBS}
    for code in W.CODES:
        t = trib[code]
        for i, kind, cgrab in S[code]:
            d = DAYS[i]
            org = "BLC" if kind == "monthly" else "ACWL"
            sid = t[2] if org == "BLC" else t[3]
            if org == "BLC":
                hh = 8 + W.CODES.index(code) * 0.6 + rng.uniform(-0.1, 0.1)
            else:
                hh = rng.uniform(7.0, 18.5)
            tm = "%02d:%02d" % (int(hh), int((hh % 1) * 60))
            tz = "EDT" if W.utc_offset(d) == 4 else "EST"
            act[0] += 1
            aid = "%s-%s-%s-%03d" % (org, d.strftime("%Y%m%d"), sid.split("-")[-1], act[0] % 1000)
            q = Qs[code][i]
            tp = cgrab
            tdp = tp * float(np.clip(rng.normal(0.32 - 0.06 * np.log(max(q, 1) / 30), 0.08), 0.08, 0.7))
            tss = float(np.exp(np.log(tp * 210) + rng.normal(0, 0.35)))
            cl = float(np.exp(np.log(18) - 0.35 * np.log(max(q, 1) / 30) + rng.normal(0, 0.15)))
            no3 = float(np.exp(np.log(0.45) + rng.normal(0, 0.3)))
            temp = float(np.clip(12 - 10 * np.cos(2 * np.pi * (d.timetuple().tm_yday - 20) / 365.25) + rng.normal(0, 1), 0, 27))
            status = "Accepted"
            note = ""
            if rng.random() < 0.012:
                status, note = "Rejected", "Holding time exceeded; sample not reanalysed."
                tp = tp * float(rng.uniform(1.4, 2.6))
            rows.append(dict(org=org, aid=aid, atype="Sample-Routine", date=d, time=tm, tz=tz, station=sid, code=code,
                             tp=tp, tdp=tdp, tss=tss, cl=cl, no3=no3, temp=temp, status=status, note=note, kind=kind))
            if org == "BLC" and rng.random() < 1 / 12:
                act[0] += 1
                rows.append(dict(rows[-1], aid=aid + "R", atype="Quality Control Sample-Field Replicate",
                                 tp=tp * float(np.exp(rng.normal(0, 0.06))), tdp=tdp * float(np.exp(rng.normal(0, 0.08))),
                                 tss=tss * float(np.exp(rng.normal(0, 0.12))), status="Accepted", note=""))
            if org == "BLC" and rng.random() < 1 / 20:
                act[0] += 1
                rows.append(dict(rows[-1], aid=aid + "B", atype="Quality Control Sample-Field Blank", tp=0.0, tdp=0.0,
                                 tss=0.0, cl=0.0, no3=0.0, status="Accepted", note=""))
    return rows


# ---------------------------------------------------------------------------- discharge monitoring reports
def dmrs(rng):
    """each facility's reports for water year 2026 (October 2025 to September 2026), monthly or, at the smaller
    dischargers, by calendar quarter: phosphorus as a monthly average and a daily maximum over the reporting period,
    concentration with flow or mass per day, some reports resubmitted"""
    rows = []
    months = [(2025, m) for m in (10, 11, 12)] + [(2026, m) for m in range(1, 10)]
    last = lambda y, m: W.D(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
    for pid, fname, rw, rkm, mgd, tp, mode, resub, reloc in W.FACILITIES:
        if pid in W.QUARTERLY:
            periods = [(W.D(months[3 * k][0], months[3 * k][1], 1), last(*months[3 * k + 2]), months[3 * k + 1][1],
                        {3 * k, 3 * k + 1, 3 * k + 2}) for k in range(4)]
        else:
            periods = [(W.D(y, m, 1), last(y, m), m, {k}) for k, (y, m) in enumerate(months)]
        for start, end, mid, ks in periods:
            flow = mgd * float(np.clip(rng.normal(1.0 + 0.18 * np.cos(2 * np.pi * (mid - 4) / 12), 0.07), 0.55, 1.6))
            conc = tp * float(np.exp(rng.normal(0, 0.18)))
            dmax = conc * float(rng.uniform(1.3, 2.2))
            recv = end + dt.timedelta(days=int(rng.integers(12, 27)))
            outfall = "001"
            def put(sub, rcv, c, f):
                tpd = "Phosphorus, total [as P]"
                fl = "Flow, in conduit or thru treatment plant"
                if mode == "conc":
                    rows.append([pid, fname, outfall, start, end, tpd, "MO AVG", round(c, 3), "mg/L", rcv, sub])
                    rows.append([pid, fname, outfall, start, end, tpd, "DAILY MX", round(c * dmax / conc, 3), "mg/L", rcv, sub])
                else:
                    lbd = c * f * W.GAL_L / W.LB_KG
                    rows.append([pid, fname, outfall, start, end, tpd, "MO AVG", round(lbd, 2), "lb/d", rcv, sub])
                    rows.append([pid, fname, outfall, start, end, tpd, "DAILY MX", round(lbd * dmax / conc, 2), "lb/d", rcv, sub])
                rows.append([pid, fname, outfall, start, end, fl, "MO AVG", round(f, 3), "MGD", rcv, sub])
            if ks & set(resub):
                # the original, later corrected: a laboratory or flow-meter error found at the facility's review
                bad_c = conc * float(rng.choice([0.62, 1.55, 1.8]))
                put("Original", recv, bad_c, flow)
                put("Resubmission", recv + dt.timedelta(days=int(rng.integers(20, 60))), conc, flow)
            else:
                put("Original", recv, conc, flow)
    return rows


# ------------------------------------------------------------------------------------- cover crop contracts
def practices(rng):
    """the farm practice program's cover crop contracts (crop years 2024 to 2027): each enrols one to three whole fields
    of one farm, near one another; some are amended to withdraw or add a field; and the program's overlay of each
    enrolled field on the watersheds, fields near a divide straddling two"""
    contracts, fields = [], {}
    fid = [0]
    cid = [0]
    neighbours = {"FAL": "KES", "KES": "ORR", "ORR": "TAM", "TAM": "VAR", "VAR": "AMB", "AMB": "HES", "HES": "PEL",
                  "PEL": "DUN", "DUN": "COR", "COR": "FAL"}
    weight = {"FAL": 6, "KES": 15, "ORR": 9, "TAM": 11, "VAR": 10, "HES": 13, "PEL": 5, "AMB": 12, "DUN": 7, "COR": 9}

    def new_field(code):
        fid[0] += 1
        f = "F%05d" % (10000 + fid[0] * 7)
        acres = float(np.round(rng.uniform(12, 95), 1))
        if rng.random() < 0.34:
            other = neighbours[code] if rng.random() < 0.7 else neighbours[neighbours[code]]
            sh = float(np.round(rng.uniform(0.18, 0.45), 2))
            split = [(code, round(1 - sh, 2)), (other, sh)]
        else:
            split = [(code, 1.0)]
        fields[f] = dict(acres=acres, split=split, code=code)
        return f

    for code in W.CODES:
        for _ in range(weight[code]):
            cid[0] += 1
            k = int(rng.choice([1, 1, 1, 2, 2, 3]))
            fl = [new_field(code if j == 0 or rng.random() < 0.6 else neighbours[code]) for j in range(k)]
            start = int(rng.choice([2024, 2025, 2026]))
            end = start + int(rng.choice([2, 3]))
            farm = "FM%04d" % (300 + int(rng.integers(0, 220)))
            versions = [list(fl)]
            if rng.random() < 0.22:
                if len(fl) > 1 and rng.random() < 0.5:
                    versions.append(fl[:-1])                    # a field withdrawn
                else:
                    versions.append(fl + [new_field(code)])     # a field added
            contracts.append(dict(cid="CC-%04d" % cid[0], farm=farm, start=start, end=end, versions=versions))
    return contracts, fields


# ---------------------------------------------------------------------------------------------- distractors
def precipitation(rng, storms):
    out = []
    rain = np.zeros(N)
    for t, size in storms:
        rain[t] += 14 * size
    for sid, nm in W.WEATHER:
        r = np.maximum(0, rain * float(rng.uniform(0.8, 1.2)) * np.exp(rng.normal(0, 0.25, N))
                       + np.where(rng.random(N) < 0.18, rng.exponential(3.0, N), 0))
        out += [(sid, DAYS[i], float(round(r[i], 1))) for i in range(N)]
    return out


def lake(rng):
    out = []
    for sid, nm in W.LAKE_STATIONS:
        base = float(rng.uniform(11, 24))
        for y in (2024, 2025, 2026):
            for m in (5, 6, 7, 8, 9, 10):
                d = W.D(y, m, int(rng.integers(5, 25)))
                tp = base * float(np.exp(rng.normal(0.05 * (m - 7), 0.2)))
                chl = tp * 0.28 * float(np.exp(rng.normal(0, 0.3)))
                secchi = float(np.clip(6.5 - 0.15 * tp + rng.normal(0, 0.4), 1.2, 8))
                out.append((sid, nm, d, round(tp, 1), round(chl, 1), round(secchi, 1)))
    return out


def simulate(seed=W.SEED):
    rng = np.random.default_rng(seed)
    storms = regional_storms(rng)
    Q = flows(rng, storms)
    C, Qs = concentrations(rng, Q)
    S = samples(rng, Qs, C)
    r2 = np.random.default_rng(seed + 101)
    return dict(storms=storms, Q=Q, Qs=Qs, C=C, S=S, UV=unit_values(r2, Q), ice=ice_days(r2), lab=lab_rows(r2, Qs, C, S),
                dmr=dmrs(r2), practices=practices(r2), precip=precipitation(r2, storms), lake=lake(r2))
