"""The clean truth: every member hospital's daily census, staffed beds, respiratory census, respiratory admissions
and declared surge level from 1 July 2021, run on to 31 March 2027 so the forward window's realised draw exists in
the generator (it never ships). Nothing here carries mess; records.py writes the exports from it.

Each winter one respiratory wave crosses the state: it peaks in the Southeast first, in West and Central Michigan
anywhere from a few days to a month later, and in the North about a month after West and Central. The wave's
calendar timing and West and Central's gap behind the Southeast move from winter to winter; the North's lag behind
West and Central holds. A member declares Level 1 when its midnight census
has been at or above 95 per cent of staffed beds on two consecutive nights, Level 2 at or above 101 per cent, steps
down below 98 per cent and stands down below 93 per cent (the association's model surge plan). Surges come only
with the wave."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as C

D = dt.date
SIM_END = D(2027, 3, 31)


def rng(*k):
    return np.random.default_rng([C.SEED] + list(k))


MONTH_BASE = {1: 0.846, 2: 0.846, 3: 0.843, 4: 0.826, 5: 0.812, 6: 0.803, 7: 0.795, 8: 0.797, 9: 0.804,
              10: 0.818, 11: 0.842, 12: 0.846}
WEEKDAY = {0: 0.010, 1: 0.011, 2: 0.008, 3: 0.004, 4: -0.004, 5: -0.013, 6: -0.016}


def month_base(d):
    """Smooth seasonal base occupancy: the monthly level interpolated at mid-month."""
    m = d.month
    mid = D(d.year, m, 15)
    if d >= mid:
        nm = 1 if m == 12 else m + 1
        ny = d.year + 1 if m == 12 else d.year
        nxt = D(ny, nm, 15)
        f = (d - mid).days / (nxt - mid).days
        return MONTH_BASE[m] * (1 - f) + MONTH_BASE[nm] * f
    pm = 12 if m == 1 else m - 1
    py = d.year - 1 if m == 1 else d.year
    prv = D(py, pm, 15)
    f = (d - prv).days / (mid - prv).days
    return MONTH_BASE[pm] * (1 - f) + MONTH_BASE[m] * f


def holiday_effect(d):
    md = (d.month, d.day)
    if md == (12, 25):
        return -0.012
    if md in ((12, 24), (12, 26), (1, 1)):
        return -0.006
    if md in ((11, 26), (11, 27)) and d.weekday() in (3, 4):
        return -0.012
    return 0.0


# this winter's southern wave is an ordinary one: its amplitude puts its surge draw at the closed winters' mean
THIS_WINTER_AMP = {"SE": 1.008, "WC": 1.004, "NO": 1.0}


def wave_params(hs):
    """Each hospital's wave peak date and amplitude in each winter. The regional lag of a winter is drawn once per
    region; a hospital adds its own stable offset and a little noise."""
    r = rng(1)
    off = {h["facility_id"]: r.normal(0, 0.7) for h in hs}
    out = {}
    past = {k: [] for k in C.AMP}
    for w in C.WINTERS:
        lag_wc = C.WC_GAP[w] + r.normal(0, 1.0)
        lag = {"SE": 0.0, "WC": lag_wc, "NO": lag_wc + C.NO_LAG + r.normal(0, 1.0)}
        amp_w = {k: C.AMP[k] * (1 + r.normal(0, 0.022)) for k in C.AMP}
        if w == 2027:                                     # this winter's wave is an ordinary-sized one
            amp_w = {k: sum(v) / len(v) * THIS_WINTER_AMP[k] for k, v in past.items()}
        else:
            for k in C.AMP:
                past[k].append(amp_w[k])
        for h in hs:
            reg = h["region"]
            pk = lag[reg] + off[h["facility_id"]] + r.normal(0, 0.5)
            a = amp_w[reg] * (1 + r.normal(0, 0.015))
            out[(w, h["facility_id"])] = (C.SE_PEAK[w] + dt.timedelta(days=float(pk)), pk, a)
    return out


def summer_bumps():
    """Small summer and autumn COVID bumps that never come near a surge trigger."""
    r = rng(2)
    bumps = []
    for y in (2022, 2023, 2024, 2025, 2026):
        c = D(y, 8, 10) + dt.timedelta(days=int(r.integers(0, 30)))
        bumps.append((c, 0.025 + 0.012 * r.random(), 10.0))
    return bumps


def staffed_beds(h, d):
    b = h["beds"]
    # two members re-opened or closed units on file; staffing rounds
    if h["facility_id"] == "MI-0503" and d < D(2023, 3, 6):
        return b - 18
    if h["facility_id"] == "MI-0437" and d >= D(2025, 9, 15):
        return b + 12
    return b


def simulate():
    hs = C.hospitals()
    wp = wave_params(hs)
    bumps = summer_bumps()
    days = list(C.daterange(C.CENSUS_START - dt.timedelta(days=2), SIM_END))
    truth = {}
    for i, h in enumerate(hs):
        r = rng(10, i)
        hoff = r.normal(0, 0.012)
        ar = 0.0
        level = 0
        hist = []
        rows = []
        for d in days:
            ar = 0.7 * ar + r.normal(0, 0.0055)
            base = month_base(d) + hoff + WEEKDAY[d.weekday()] + holiday_effect(d) + ar
            resp = 0.0
            for w in C.WINTERS:
                pkd, _, a = wp[(w, h["facility_id"])]
                t = (dt.datetime.combine(d, dt.time(12)) - dt.datetime.combine(pkd, dt.time(12)) if isinstance(pkd, D)
                     else None)
                # pkd may carry a fractional day: rebuild from the float offset
            for w in C.WINTERS:
                _, pk, a = wp[(w, h["facility_id"])]
                t = (d - C.SE_PEAK[w]).days - pk
                if abs(t) < 45:
                    resp += a * math.exp(-t * t / (2 * C.SIG[h["region"]] ** 2))
            for c, a, s in bumps:
                t = (d - c).days
                if abs(t) < 40:
                    resp += a * math.exp(-t * t / (2 * s * s))
            beds = staffed_beds(h, d)
            census = int(round(beds * (base + resp)))
            occ = census / beds
            rows.append([d, beds, census, resp])
            hist.append(occ)
        # declared level for census night d is the level in force at that midnight, set at the 07:00 huddle on d from
        # the two previous census nights
        levels = []
        for k, (d, beds, census, resp) in enumerate(rows):
            if k < 2:
                levels.append(0)
                continue
            o1, o2 = hist[k - 1], hist[k - 2]
            prev = levels[-1]
            if prev == 0:
                lv = 2 if (o1 >= C.L2_UP and o2 >= C.L1_UP) else (1 if (o1 >= C.L1_UP and o2 >= C.L1_UP) else 0)
            elif prev == 1:
                lv = 2 if o1 >= C.L2_UP else (1 if o1 >= C.L1_DOWN else 0)
            else:
                lv = 2 if o1 >= C.L2_DOWN else (1 if o1 >= C.L1_DOWN else 0)
            levels.append(lv)
        # respiratory admissions in the 24 hours to midnight: the respiratory census turned over at a six-day stay,
        # led by three days
        r2 = rng(20, i)
        resp_by_day = {row[0]: row[3] for row in rows}
        out = []
        for k, (d, beds, census, resp) in enumerate(rows):
            if d < C.CENSUS_START:
                continue
            lead = resp_by_day.get(d + dt.timedelta(days=3), resp)
            lam = max(0.2, lead * beds / 6.0 + 0.015 * beds)
            adm = int(r2.poisson(lam))
            out.append({"date": d, "beds": beds, "census": census, "level": levels[k], "resp_admits": adm,
                        "resp_share": resp})
        truth[h["facility_id"]] = out
    return hs, wp, truth


def spells(series):
    """Runs of consecutive surge-active census nights: (first, last, days at Level 1, days at Level 2)."""
    out, cur = [], None
    for row in series:
        if row["level"] > 0:
            if cur is None:
                cur = [row["date"], row["date"], 0, 0]
            cur[1] = row["date"]
            cur[2 if row["level"] == 1 else 3] += 1
        elif cur is not None:
            out.append(tuple(cur))
            cur = None
    if cur is not None:
        out.append(tuple(cur))
    return out


if __name__ == "__main__":
    hs, wp, truth = simulate()
    for h in hs:
        sp = spells(truth[h["facility_id"]])
        print(h["facility_id"], h["region"], h["name"][:26].ljust(26), [(a.isoformat(), b.isoformat(), l1, l2) for a, b, l1, l2 in sp])


# ------------------------------------------------------------------------------------------------- declarations
TZ_OFFSET = {"EST": -5, "EDT": -4}


def us_eastern_offset(t):
    """UTC offset of Michigan's Eastern time for a naive local datetime (second Sunday of March to first Sunday of
    November is daylight time). The Upper Peninsula's four western counties keep Central time; no member sits there."""
    y = t.year
    m = dt.datetime(y, 3, 8)
    while m.weekday() != 6:
        m += dt.timedelta(days=1)
    start = m.replace(hour=2)
    n = dt.datetime(y, 11, 1)
    while n.weekday() != 6:
        n += dt.timedelta(days=1)
    end = n.replace(hour=2)
    return -4 if start <= t < end else -5


def to_utc(t):
    return t - dt.timedelta(hours=us_eastern_offset(t))


def declarations(hs, truth):
    """The surge declaration log: one row for each change of declared level, timed at the 06:45 bed huddle or the
    14:45 bed meeting of the day whose census night carries the new level. Activations carry the surge request number
    the hospital sends both agencies."""
    out = []
    seq = {}
    for i, h in enumerate(hs):
        r = rng(30, i)
        fid = h["facility_id"]
        prev = 0
        for row in truth[fid]:
            lv = row["level"]
            if lv != prev:
                d = row["date"]
                if prev == 0:
                    pm = r.random() < 0.18
                elif lv == 0:
                    pm = r.random() < 0.16
                else:
                    pm = r.random() < 0.10
                t = dt.datetime.combine(d, dt.time(14, 45) if pm else dt.time(6, 45))
                req = ""
                if prev == 0:
                    y = d.year if d.month >= 7 else d.year - 1
                    seq[(fid, y)] = seq.get((fid, y), 0) + 1
                    req = "SR-%s-%s-%02d" % (h["member_no"], str(y)[2:] + str(y + 1)[2:], seq[(fid, y)])
                out.append({"facility_id": fid, "declared_at": t, "level_from": prev, "level_to": lv, "request_no": req})
                prev = lv
    out.sort(key=lambda x: (x["declared_at"], x["facility_id"]))
    return out


def active_intervals(decl, fid):
    """(start, end, level) intervals during which the hospital's surge plan was active, from the declaration log."""
    rows = [x for x in decl if x["facility_id"] == fid]
    out, cur = [], None
    for x in rows:
        if cur is not None:
            out.append((cur[0], x["declared_at"], cur[1]))
            cur = None
        if x["level_to"] > 0:
            cur = (x["declared_at"], x["level_to"])
    if cur is not None:
        out.append((cur[0], dt.datetime(2099, 1, 1), cur[1]))
    return out


def level_at(intervals, t):
    for a, b, lv in intervals:
        if a <= t < b:
            return lv
    return 0


# ------------------------------------------------------------------------------------------------- agency shifts
AGENCY_SEASONS = [(D(2025, 11, 1), D(2026, 3, 31)), (D(2026, 11, 1), C.CENSUS_END)]
REG_UNITS = {
    "SE": ["Med-Surg 3 West", "Med-Surg 4 East", "Telemetry 5", "Ortho/Neuro 6", "ICU", "Step-Down 2"],
    "WC": ["Med-Surg 2 North", "Med-Surg 3 South", "Telemetry", "Surgical 4", "ICU", "Oncology 5"],
    "NO": ["Med-Surg 2", "Med-Surg 3", "ICU/CCU", "Surgical"],
}
# per active surge shift, the expected nurses booked on the surge request for another unit, at Level 1 and Level 2;
# three in four go to the emergency department
XTRA = (0.16, 0.30)
XTRA_UNITS = {"SE": ["Emergency Dept", "Med-Surg 4 East"], "WC": ["Emergency", "Med-Surg 3 South"],
              "NO": ["Emergency", "Med-Surg 3"]}


def agency_rosters():
    r = rng(40)
    ros = {"C": [], "I": []}
    used = set()
    for ag, pre in (("C", "CMS-"), ("I", "ISN")):
        n = 0
        while n < 420:
            v = int(r.integers(1000, 99999)) if ag == "C" else int(r.integers(1000, 9999))
            code = pre + ("%05d" % v if ag == "C" else "%04d" % v)
            if code in used:
                continue
            used.add(code)
            ros[ag].append(code)
            n += 1
    return ros


def agency_shifts(hs, truth, decl):
    """Every agency RN shift at the pool's members in the agency seasons: surge-unit shifts (with each slot's agency,
    booking code and bill-to), the skeleton openings before a morning declaration, the teams that report after a
    stand-down, the nurses booked on an open surge request for other units, and regular agency shifts on the members'
    other units. Times are local."""
    ros = agency_rosters()
    out = []
    for i, h in enumerate(hs):
        fid = h["facility_id"]
        r = rng(50, i)
        rx = rng(52, i)
        iv = active_intervals(decl, fid)
        hdecl = [x for x in decl if x["facility_id"] == fid]
        prim = h["agency"]
        other = "I" if prim == "C" else "C"
        # each hospital draws its agency nurses from a slice of each agency's roster
        base_c = (i * 13) % 300
        base_i = (i * 11) % 300
        pool_c = ros["C"][base_c:base_c + 60]
        pool_i = ros["I"][base_i:base_i + 60]
        for s0, s1 in AGENCY_SEASONS:
            if h["region"] == "NO" and s0 < C.NORTH_JOIN:
                continue
            req_of = {}
            for x in hdecl:
                if x["request_no"]:
                    req_of[x["declared_at"]] = x["request_no"]
            for d in C.daterange(s0, s1):
                for shift, hh in (("D", 7), ("N", 19)):
                    t = dt.datetime.combine(d, dt.time(hh))
                    lv = level_at(iv, t)
                    kind = None
                    n = 0
                    if lv > 0:
                        n = h["grid"][lv - 1] // 2
                        kind = "active"
                    else:
                        # skeleton opening the night before a morning declaration
                        nxt = [x for x in hdecl if x["level_from"] == 0 and x["level_to"] > 0
                               and x["declared_at"] == dt.datetime.combine(d + dt.timedelta(days=1), dt.time(6, 45))]
                        if shift == "N" and nxt:
                            n, kind = 1, "skeleton"
                        # the team booked for the shift after a stand-down
                        sd = [x for x in hdecl if x["level_to"] == 0 and x["level_from"] > 0]
                        for x in sd:
                            if shift == "D" and x["declared_at"] == dt.datetime.combine(d, dt.time(6, 45)):
                                if r.random() < 0.6:
                                    n, kind = h["grid"][x["level_from"] - 1] // 2, "after"
                            if shift == "N" and x["declared_at"] == dt.datetime.combine(d, dt.time(14, 45)):
                                if r.random() < 0.5:
                                    n, kind = h["grid"][x["level_from"] - 1] // 2, "after"
                    if not n:
                        continue
                    # the request this run of surge shifts was booked against
                    act = [x for x in hdecl if x["level_from"] == 0 and x["level_to"] > 0 and x["declared_at"] <= t
                           + dt.timedelta(hours=12)]
                    req = act[-1]["request_no"] if act else ""
                    first_act = act[-1]["declared_at"] if act else None
                    for k in range(n):
                        if r.random() < 0.006:
                            continue                                      # a slot the agencies could not fill
                        # Crestfield's rapid-open roster staffs every skeleton opening
                        ag = "C" if kind == "skeleton" else (prim if k % 2 == 0 else other)
                        # booking code: the morning-activation day shift was booked the evening before as staffing
                        code, bill = "SURGE", "POOL"
                        if kind == "skeleton":
                            code, bill = "STAFF", "FACILITY"
                        elif kind == "active" and first_act is not None and first_act.time() == dt.time(6, 45) \
                                and first_act.date() == d and shift == "D":
                            code, bill = "STAFF", "FACILITY"
                        pool = pool_c if ag == "C" else pool_i
                        nurse = pool[(k * 7 + d.toordinal()) % len(pool)]
                        out.append({"facility_id": fid, "agency": ag, "start": t, "shift": shift,
                                    "unit": h["surge_unit"], "surge_unit": True, "kind": kind, "level": lv,
                                    "code": code, "bill": bill, "request_no": req if code == "SURGE" else "",
                                    "nurse": nurse})
                    # nurses the staffing office books on the open surge request for its other units (the emergency
                    # department's holds, mostly); the agencies bill them to the pool like the surge unit's own
                    if kind == "active" and not (first_act is not None and first_act.date() == d and shift == "D"
                                                 and first_act.time() == dt.time(6, 45)):
                        for _ in range(int(rx.poisson(XTRA[lv - 1]))):
                            ag = prim if rx.random() < 0.65 else other
                            pool = pool_c if ag == "C" else pool_i
                            out.append({"facility_id": fid, "agency": ag, "start": t, "shift": shift,
                                        "unit": XTRA_UNITS[h["region"]][int(rx.integers(0, 4)) // 3],
                                        "surge_unit": False, "kind": "extra", "level": lv, "code": "SURGE",
                                        "bill": "POOL", "request_no": req, "nurse": pool[int(rx.integers(0, len(pool)))]})
                    # regular agency shifts on the member's other units
                lam = 0.0045 * h["beds"]
                for shift, hh in (("D", 7), ("N", 19)):
                    t = dt.datetime.combine(d, dt.time(hh))
                    m = int(r.poisson(lam))
                    for k in range(m):
                        ag = prim if r.random() < 0.7 else other
                        pool = pool_c if ag == "C" else pool_i
                        out.append({"facility_id": fid, "agency": ag, "start": t, "shift": shift,
                                    "unit": REG_UNITS[h["region"]][int(r.integers(0, len(REG_UNITS[h["region"]])))],
                                    "surge_unit": False, "kind": "regular", "level": level_at(iv, t),
                                    "code": "STAFF", "bill": "FACILITY", "request_no": "",
                                    "nurse": pool[int(r.integers(0, len(pool)))]})
    out.sort(key=lambda x: (x["start"], x["facility_id"], x["agency"], x["unit"], x["nurse"]))
    return out


def funded(s, iv_of):
    """The pool funds an agency RN shift that staffs a member's surge unit and starts while its plan is active."""
    return s["surge_unit"] and level_at(iv_of[s["facility_id"]], s["start"]) > 0


# ------------------------------------------------------------------------------------------------- wastewater
# sewersheds sampled by the association's surveillance programme: the members' cities, grouped where one plant
# serves several members
SEWERSHEDS = [
    ("WW-SE-01", "Detroit", "SE", ["MI-0412", "MI-0418", "MI-0446"], 1.00),
    ("WW-SE-02", "Pontiac", "SE", ["MI-0431", "MI-0451"], 0.62),
    ("WW-SE-03", "Mount Clemens", "SE", ["MI-0425", "MI-0455"], 0.55),
    ("WW-SE-04", "Ypsilanti", "SE", ["MI-0437"], 0.31),
    ("WW-SE-05", "Monroe", "SE", ["MI-0442"], 0.18),
    ("WW-WC-01", "Grand Rapids", "WC", ["MI-0503"], 0.66),
    ("WW-WC-02", "Kalamazoo", "WC", ["MI-0508"], 0.34),
    ("WW-WC-03", "Lansing", "WC", ["MI-0514"], 0.41),
    ("WW-WC-04", "Flint", "WC", ["MI-0519"], 0.36),
    ("WW-WC-05", "Saginaw", "WC", ["MI-0523"], 0.27),
    ("WW-WC-06", "Muskegon", "WC", ["MI-0528"], 0.19),
    ("WW-WC-07", "Battle Creek", "WC", ["MI-0532"], 0.15),
    ("WW-NO-01", "Traverse City", "NO", ["MI-0604"], 0.16),
    ("WW-NO-02", "Petoskey", "NO", ["MI-0609"], 0.07),
    ("WW-NO-03", "Alpena", "NO", ["MI-0613"], 0.07),
    ("WW-NO-04", "Gaylord", "NO", ["MI-0617"], 0.05),
    ("WW-NO-05", "Cadillac", "NO", ["MI-0622"], 0.05),
    ("WW-NO-06", "Marquette", "NO", ["MI-0626"], 0.10),
    ("WW-NO-07", "Escanaba", "NO", ["MI-0631"], 0.06),
    ("WW-NO-08", "Sault Ste. Marie", "NO", ["MI-0635"], 0.06),
]
WW_START = D(2021, 9, 6)


def wastewater(hs, wp):
    """Influenza A and SARS-CoV-2 concentrations at each sewershed: the wave in its members' communities, about nine
    days ahead of their respiratory census, sampled twice a week in the south (Monday and Thursday) and weekly in
    the North (Tuesday); results posted three days after sampling, about one in nine re-run and revised a week later."""
    r = rng(60)
    H = {h["facility_id"]: h for h in hs}
    out = []
    for code, city, reg, fids, scale in SEWERSHEDS:
        days = (0, 3) if reg != "NO" else (1,)
        d = WW_START
        while d <= C.CENSUS_END - dt.timedelta(days=3):
            if d.weekday() in days:
                inf = 0.0
                for w in C.WINTERS:
                    pks = [wp[(w, f)][1] for f in fids]
                    pk = sum(pks) / len(pks) - 9.0
                    t = (d - C.SE_PEAK[w]).days - pk
                    s = C.SIG[reg] + 1.0
                    if abs(t) < 50:
                        inf += math.exp(-t * t / (2 * s * s))
                flu = 220000.0 * (0.012 + inf) * (1 + 0.08 * r.normal()) * math.exp(r.normal(0, 0.33))
                cov = 90000.0 * (0.20 + 0.10 * math.sin(d.toordinal() / 41.0) ** 2 + 0.35 * inf) * math.exp(r.normal(0, 0.30))
                pmmov = 3.1e9 * math.exp(r.normal(0, 0.22))
                posted = d + dt.timedelta(days=3)
                for target, v in (("Influenza A", flu), ("SARS-CoV-2", cov)):
                    rev = r.random() < 0.11 and posted + dt.timedelta(days=7) <= C.CENSUS_END
                    v2 = v * math.exp(r.normal(0, 0.18)) if rev else None
                    out.append({"sewershed": code, "city": city, "sample_date": d, "target": target,
                                "conc": v, "pmmov": pmmov, "posted": posted, "revised": v2,
                                "revised_posted": posted + dt.timedelta(days=7) if rev else None})
            d += dt.timedelta(days=1)
    return out


def outlook(hs, wp, truth, issued=D(2026, 12, 18), horizon=14):
    """The surveillance unit's regional admissions outlook issued on Friday 18 December 2026: expected daily
    respiratory admissions in each region for the 14 days from 19 December, with an 80 per cent range. It is built
    from the regions' own recent admissions and wastewater and is close to the truth over its horizon."""
    r = rng(70)
    out = []
    for reg in ("SE", "WC", "NO"):
        hreg = [h for h in hs if h["region"] == reg]
        for k in range(1, horizon + 1):
            d = issued + dt.timedelta(days=k)
            mu = 0.0
            for h in hreg:
                fid = h["facility_id"]
                resp = 0.0
                for w in C.WINTERS:
                    _, pk, a = wp[(w, fid)]
                    t = (d + dt.timedelta(days=3) - C.SE_PEAK[w]).days - pk
                    if abs(t) < 45:
                        resp += a * math.exp(-t * t / (2 * C.SIG[h["region"]] ** 2))
                mu += resp * h["beds"] / 6.0 + 0.015 * h["beds"]
            mu *= 1 + r.normal(0, 0.04) * (k / horizon)
            lo, hi = mu * (1 - 0.06 - 0.012 * k), mu * (1 + 0.06 + 0.012 * k)
            out.append({"region": reg, "date": d, "expected": mu, "low": lo, "high": hi})
    return out
