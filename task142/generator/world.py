"""The world before any file is written: the members' HITH episodes from April 2024, the daily census, the stays
pool, the 2026-27 operating plans (revised in October 2026), the in-house capacity return, and on the asks' side
Bellbird's July to September 2026 overflow (referrals, acceptances, visits, re-entered records), the intake register
and the referral portal. Every random draw comes from its own named stream (common.rng)."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import model as MD

# ---------------------------------------------------------------------------------------------------- parameters
# non-bone-and-joint admissions a day at the July 2025 level, and each stream's share of them
BASE = {"NGH": 2.36, "RBH": 2.02, "WMH": 1.58, "KDH": 1.31, "HCH": 1.09}
SHARE = {
    "NGH": {"H01": 0.335, "H02": 0.158, "H03": 0.171, "H06": 0.128, "H07": 0.112, "H08": 0.096},
    "WMH": {"H01": 0.322, "H02": 0.166, "H03": 0.165, "H06": 0.139, "H07": 0.104, "H08": 0.104},
    "RBH": {"H01": 0.296, "H02": 0.139, "H03": 0.154, "H05": 0.041, "H06": 0.131, "H07": 0.101, "H08": 0.091},
    "KDH": {"H01": 0.305, "H02": 0.146, "H03": 0.142, "H05": 0.037, "H06": 0.127, "H07": 0.097, "H08": 0.094},
    "HCH": {"H01": 0.301, "H02": 0.137, "H03": 0.151, "H05": 0.044, "H06": 0.134, "H07": 0.099, "H08": 0.087},
}
BJI_HIST = {"NGH": 0.0, "RBH": 0.142, "WMH": 0.0, "KDH": 0.098, "HCH": 0.052}    # admissions a day before October 2026
BJI_FWD = {"NGH": 0.204, "RBH": 0.142, "WMH": 0.161, "KDH": 0.098, "HCH": 0.052}  # from 1 October 2026
# the October 2026 plan revision: stream multipliers from 1 October 2026
FWD = {("RBH", "H08"): 1.55, ("KDH", "H03"): 1.45, ("HCH", "H05"): 2.1, ("NGH", "H01"): 1.04, ("WMH", "H02"): 1.08}
PLAN_ADJ = {"NGH": 1.008, "RBH": 0.982, "WMH": 1.002, "KDH": 0.986, "HCH": 1.0}   # members' own planning assumption
GROWTH = 0.04                                     # a year, linear from July 2025
LOS = {"H01": ("gamma", 5.0, 1.22, 2, 16), "H02": ("gamma", 4.6, 1.18, 2, 13), "H03": ("gamma", 3.6, 1.45, 2, 13),
       "H04": ("normal", 44.0, 12.5, 14, 92), "H05": ("normal", 29.0, 8.0, 10, 49), "H06": ("gamma", 2.6, 4.8, 3, 46),
       "H07": ("gamma", 3.6, 1.08, 1, 9), "H08": ("gamma", 4.1, 1.65, 2, 15)}
AMP = {"H01": 0.14, "H02": 0.03, "H03": -0.18, "H04": 0.0, "H05": 0.0, "H06": 0.0, "H07": 0.0, "H08": -0.07}
P_INTERRUPT = {"H01": 0.022, "H02": 0.02, "H03": 0.024, "H04": 0.06, "H05": 0.055}   # course resumed after a ward stay
P_WARD = 0.031            # returned to the ward, course not resumed in HITH
P_TRANSFER = 0.004
P_DIED = 0.0018
P_RETURNING = 0.11        # an episode for a patient the member has treated before

CAMPUS = {"NGH": [("4103", 1.0)], "RBH": [("4211", 0.71), ("4218", 0.29)], "KDH": [("5212", 1.0)],
          "HCH": [("5307", 1.0)]}
WM_CAMPUS_OLD = {"W": "5121", "A": "5133"}
WM_CAMPUS_NEW = {"W": "5140", "A": "5141"}
DX = {"H01": [("L03.11", .55), ("L03.10", .12), ("L03.2", .06), ("L02.4", .12), ("L03.3", .08), ("L08.9", .07)],
      "H02": [("N10", .45), ("N39.0", .45), ("N30.0", .10)],
      "H03": [("J18.9", .45), ("J15.9", .15), ("J44.0", .25), ("J22", .15)],
      "H04": [("M86.16", .2), ("M86.67", .2), ("M00.96", .2), ("T84.5", .3), ("M46.26", .1)],
      "H05": [("I33.0", .45), ("J86.9", .25), ("K75.0", .2), ("G06.0", .1)],
      "H06": [("T81.4", .35), ("L89.3", .1), ("L97", .35), ("T81.3", .2)],
      "H07": [("I80.2", .6), ("I26.9", .4)],
      "H08": [("I50.0", .7), ("I50.9", .3)]}
OLD_CODE = {"H01": "AB", "H02": "AB", "H03": "AB", "H04": "AB", "H05": "AB", "H06": "WC", "H07": "AC", "H08": "HF"}
CROSSWALK = [("AB", "L02", "H01"), ("AB", "L03", "H01"), ("AB", "L08", "H01"), ("AB", "N10", "H02"),
             ("AB", "N30", "H02"), ("AB", "N39", "H02"), ("AB", "J15", "H03"), ("AB", "J18", "H03"),
             ("AB", "J22", "H03"), ("AB", "J44", "H03"), ("AB", "M00", "H04"), ("AB", "M46", "H04"),
             ("AB", "M86", "H04"), ("AB", "T84", "H04"), ("AB", "G06", "H05"), ("AB", "I33", "H05"),
             ("AB", "J86", "H05"), ("AB", "K75", "H05"), ("WC", "", "H06"), ("AC", "", "H07"), ("HF", "", "H08")]


def seas(dates, amp):
    doy = np.array([d.timetuple().tm_yday for d in dates])
    return 1 + amp * np.cos(2 * np.pi * (doy - 15) / 365.25)


def growth(dates):
    return np.array([1 + GROWTH * (d - K.CENSUS0).days / 365.25 for d in dates])


def rate(m, s, dates, forward):
    """Primary admissions a day (before interrupted courses resume as second episodes)."""
    dates = list(dates)
    g = growth(dates) * seas(dates, AMP[s])
    after = np.array([d >= K.PATH for d in dates])
    if s == "H04":
        hist = np.full(len(dates), BJI_HIST[m])
        if forward:
            hist = np.where(after, BJI_FWD[m] * PLAN_ADJ[m], hist)
        return hist * g
    sh = SHARE[m].get(s, 0.0)
    base = np.full(len(dates), BASE[m] * sh) * g
    if forward:
        base = np.where(after, base * FWD.get((m, s), 1.0) * PLAN_ADJ[m], base)
    return base


def draw_los(r, s, n):
    sp = LOS[s]
    x = r.gamma(sp[1], sp[2], n) if sp[0] == "gamma" else r.normal(sp[1], sp[2], n)
    return np.clip(np.round(x), sp[3], sp[4]).astype(int)


def pick(r, table):
    vals = [v for v, _ in table]
    p = np.array([w for _, w in table], dtype=float)
    return vals[r.choice(len(vals), p=p / p.sum())]


class World:
    pass


# ---------------------------------------------------------------------------------------------------- episodes

def _patient_no(m, n, campus_letter="W"):
    if m == "NGH":
        return "%07d" % n
    if m == "RBH":
        return "RB%06d" % n
    if m == "WMH":
        return ("51%06d" if campus_letter == "W" else "57%06d") % n
    if m == "KDH":
        return "K%06d" % n
    return "%06dH" % n


def episodes():
    """Every HITH episode admitted from 1 April 2024 to 30 September 2026, with its stay drawn in full (the extract
    shows the separation only where it falls on or before 30 September 2026)."""
    dates = K.days(K.D0, K.D1)
    out = []
    for m in K.MEMBERS:
        r = rng_m = K.rng("episodes", m)
        courses = []
        for s in K.STREAMS:
            lam = rate(m, s, dates, forward=False)
            if lam.sum() == 0:
                continue
            rs = K.rng("adm", m, s)
            n = rs.poisson(lam)
            idx = np.repeat(np.arange(len(dates)), n)
            L = draw_los(rs, s, len(idx))
            for i, LL in zip(idx, L):
                courses.append((dates[i], s, int(LL)))
        courses.sort(key=lambda c: (c[0], c[1], c[2]))
        seen = []
        seq = 0
        nxt_patient = {"NGH": 391000, "RBH": 207000, "WMH": 104000, "KDH": 318000, "HCH": 296000}[m]
        for a, s, L in courses:
            # the patient
            if m == "WMH":
                letter = "A" if r.random() < 0.26 else "W"
            else:
                letter = "W"
            if seen and r.random() < P_RETURNING:
                pat = seen[r.integers(len(seen))]
            else:
                nxt_patient += int(r.integers(1, 9))
                pat = (_patient_no(m, nxt_patient, letter), letter)
                seen.append(pat)
            pno, letter = pat
            dx = pick(r, DX[s])
            # how the course ends
            u = r.random()
            pieces = []
            if s in P_INTERRUPT and L >= 6 and u < P_INTERRUPT[s]:
                j = int(r.integers(2, L - 2))
                gap = int(r.integers(1, 4))
                pieces = [(a, j, "2"), (a + dt.timedelta(days=j + gap), L - j, "1")]
            elif u < P_INTERRUPT.get(s, 0) + P_WARD and L >= 3:
                pieces = [(a, int(r.integers(1, L)), "2")]
            elif u < P_INTERRUPT.get(s, 0) + P_WARD + P_TRANSFER and L >= 3:
                pieces = [(a, int(r.integers(1, L)), "3")]
            elif u < P_INTERRUPT.get(s, 0) + P_WARD + P_TRANSFER + P_DIED and L >= 3:
                pieces = [(a, int(r.integers(1, L)), "4")]
            else:
                pieces = [(a, L, "1")]
            for (pa, pl, mode) in pieces:
                if pa > K.D1:
                    continue
                seq += 1
                if m == "WMH":
                    campus = (WM_CAMPUS_OLD if pa < K.MERGER else WM_CAMPUS_NEW)[letter]
                else:
                    cs = CAMPUS[m]
                    campus = cs[0][0] if len(cs) == 1 else (cs[0][0] if r.random() < cs[0][1] else cs[1][0])
                out.append(dict(member=m, campus=campus, patient=pno, seq=seq, adm=pa, stay=pl, mode=mode, stream=s,
                                dx=dx, letter=letter))
    # episode numbers in admission order within each member
    for m in K.MEMBERS:
        eps = sorted((e for e in out if e["member"] == m), key=lambda e: (e["adm"], e["seq"]))
        start = {"NGH": 6100000, "RBH": 2240000, "WMH": 8810000, "KDH": 4470000, "HCH": 3320000}[m]
        for i, e in enumerate(eps):
            e["episode"] = "%s%07d" % (m[:2], start + 3 * i + int(K.rng("epno", m, i).integers(0, 3)))
    out.sort(key=lambda e: (e["adm"], e["member"], e["episode"]))
    for e in out:
        e["last"] = e["adm"] + dt.timedelta(days=e["stay"] - 1)
        e["open"] = e["last"] > K.D1
    return out


def pools(eps, last_admission=K.POOL_LAST_ADMISSION, first_admission=K.D0, member=None, include_open=False,
          include_late_completed=False):
    """Stays (home days) of the alliance's episodes by stream: completed episodes admitted from first_admission to
    last_admission (all complete by 30 September 2026), optionally one member's only."""
    out = {s: [] for s in K.STREAMS}
    for e in eps:
        if member and e["member"] != member:
            continue
        if e["adm"] < first_admission:
            continue
        if e["open"]:
            if include_open:
                out[e["stream"]].append((K.D1 - e["adm"]).days + 1)
            continue
        if e["adm"] > last_admission and not include_late_completed:
            continue
        out[e["stream"]].append(e["stay"])
    return {s: np.array(v, dtype=int) for s, v in out.items()}


# ---------------------------------------------------------------------------------------------------- the plan

def plan_admissions(eps):
    """Admissions by member, stream and month: July to September 2026 as recorded, October 2026 to June 2027 the
    revised plan (expected episodes, interrupted courses resuming included, rounded to whole admissions)."""
    out = {m: {s: {} for s in K.STREAMS} for m in K.MEMBERS}
    for e in eps:
        if K.FY0 <= e["adm"] <= K.D1:
            mo = e["adm"].replace(day=1)
            out[e["member"]][e["stream"]][mo] = out[e["member"]][e["stream"]].get(mo, 0) + 1
    for m in K.MEMBERS:
        for s in K.STREAMS:
            for mo in K.MONTHS_FY:
                if mo < K.PATH:
                    out[m][s].setdefault(mo, 0)
                    continue
                dd = K.days(mo, K.month_end(mo))
                lam = rate(m, s, dd, forward=True).sum() * (1 + P_INTERRUPT.get(s, 0.0))
                out[m][s][mo] = int(K.round_to(lam, 1))
    return out


def plan_visits(eps, adm, pool):
    """Visits on each month's days by member and stream: July to September 2026 as recorded in the census, October
    2026 to June 2027 expected from the patients at home on 30 September 2026 and the planned admissions, every stay
    drawn from the alliance's stays pool."""
    out = {m: {s: {} for s in K.STREAMS} for m in K.MEMBERS}
    for e in eps:
        for k in range(e["stay"]):
            d = e["adm"] + dt.timedelta(days=k)
            if K.FY0 <= d <= K.D1:
                mo = d.replace(day=1)
                v = K.visits_on_day(e["stream"], k)
                out[e["member"]][e["stream"]][mo] = out[e["member"]][e["stream"]].get(mo, 0) + v
    fdays = K.days(K.PATH, K.FY1)
    t_index = {d: i for i, d in enumerate(fdays)}
    for s in K.STREAMS:
        Ls = pool[s]
        if len(Ls) == 0:
            continue
        maxL = int(Ls.max())
        surv = np.array([(Ls > k).mean() for k in range(maxL + 2)])
        vis = np.array([K.visits_on_day(s, k) for k in range(maxL + 2)], dtype=float)
        for m in K.MEMBERS:
            exp_day = np.zeros(len(fdays))
            # patients at home on 30 September 2026
            for e in eps:
                if e["member"] != m or e["stream"] != s or not e["open"]:
                    continue
                k0 = (K.D1 - e["adm"]).days
                if k0 + 1 >= len(surv) or surv[k0] == 0:
                    continue
                for j, d in enumerate(fdays):
                    k = k0 + 1 + j
                    if k > maxL:
                        break
                    exp_day[j] += vis[k] * surv[k] / surv[k0]
            # planned admissions from 1 October 2026
            rates = MD.daily_rates(adm[m][s], K.PATH, K.FY1)
            for j in range(len(fdays)):
                if rates[j] == 0:
                    continue
                kk = np.arange(0, min(maxL, len(fdays) - j))
                exp_day[j + kk] += rates[j] * vis[kk] * surv[kk]
            for mo in K.MONTHS_FY:
                if mo < K.PATH:
                    out[m][s].setdefault(mo, 0)
                    continue
                a, b = t_index[mo], t_index[K.month_end(mo)]
                out[m][s][mo] = exp_day[a:b + 1].sum()
    # rounded to whole visits for the plan
    rounded = {m: {s: {mo: (int(K.round_to(v, 1)) if mo >= K.PATH else int(v)) for mo, v in out[m][s].items()}
                   for s in K.STREAMS} for m in K.MEMBERS}
    return rounded, out


def quarter_plan(pv, m):
    return sum(pv[m][s][mo] for s in K.STREAMS for mo in (dt.date(2027, 1, 1), dt.date(2027, 2, 1),
                                                          dt.date(2027, 3, 1)))


# ---------------------------------------------------------------------------------------------------- capacity
VISITS_PER_SHIFT = {"NGH": 8, "RBH": 7, "WMH": 7, "KDH": 7, "HCH": 6}
LEAVE_SHARE = {"NGH": 0.118, "RBH": 0.124, "WMH": 0.109, "KDH": 0.131, "HCH": 0.127}
GOLD_RESIDUE = 10.5     # where the golden excess sits inside its lot (visits past the last full lot)


def place_capacity(W):
    """The members' in-house capacity for January to March 2027, as rostered: net visiting shifts times the member's
    visits a shift. The roster is the members'; the build checks where each member's excess falls inside its lot."""
    from scipy import stats
    W.capacity, W.shifts = {}, {}
    for m in K.MEMBERS:
        req = MD.requirement(W.adm[m], W.pool, W.plan_q[m])[0]
        plan = W.plan_q[m]
        pois_a = float(stats.poisson.ppf(0.9, plan))
        pois_b = plan + 1.2816 * math.sqrt(plan)
        target = {"NGH": 12, "RBH": 10, "WMH": 9, "KDH": 7, "HCH": 7}[m]
        vps = VISITS_PER_SHIFT[m]
        best = None
        c0 = int((req - target * K.LOT) / vps)
        for net in range(c0 - 8, c0 + 9):
            cap = net * vps
            e = req - cap
            if K.lots_for(e) != target:
                continue
            res = e - (K.lots_for(e) - 1) * K.LOT
            same_default = K.lots_for(pois_a - cap) == K.lots_for(pois_b - cap) and K.lots_for(pois_a - cap) > 0
            score = abs(res - GOLD_RESIDUE) + (100 if not same_default else 0)
            if best is None or score < best[0]:
                best = (score, net, cap)
        _, net, cap = best
        rostered = int(round(net / (1 - LEAVE_SHARE[m])))
        W.shifts[m] = dict(rostered=rostered, leave=rostered - net, net=net, per_shift=vps)
        W.capacity[m] = cap


# ---------------------------------------------------------------------------------------------------- Bellbird
CLIENT = {"NGH": "C4471", "RBH": "C4472", "WMH": "C4475", "KDH": "C4478", "HCH": "C4480"}
CLIENT_ALTONA = "C3920"
CLIENT_OFFICE = "C4466"                # the Alliance program office's billing account
P_REF = {"NGH": 0.19, "RBH": 0.20, "WMH": 0.25, "KDH": 0.27, "HCH": 0.30}
P_DECLINE = 0.07
P_ATTEMPT = 0.045
P_CANCEL = 0.02
P_CALLOUT = 0.035         # an unscheduled return the same day to an IV patient (pump alarm, line or dressing problem)
P_LATE_POST = 0.12
P_REPLAY = {"NGH": 0.035, "RBH": 0.03, "WMH": 0.055, "KDH": 0.035, "HCH": 0.06}
NURSES = {"NGH": ["RN0412", "RN0437", "RN0455", "RN0461", "RN0478", "RN0503"],
          "RBH": ["RN0318", "RN0326", "RN0349", "RN0461", "RN0512", "RN0530"],
          "WMH": ["RN0207", "RN0219", "RN0244", "RN0251", "RN0268", "RN0286"],
          "KDH": ["RN0603", "RN0611", "RN0629", "RN0642", "RN0657"],
          "HCH": ["RN0702", "RN0715", "RN0723", "RN0739", "RN0748"]}
REF_FROM = dt.date(2026, 6, 15)       # referrals generated from here (late June runs carry into July)
ASK_SALT = 0                          # the referral stream's draw (asks only; nothing the call reads depends on it)


def bellbird_ref(e):
    digits = "".join(ch for ch in e["patient"] if ch.isdigit()).lstrip("0")
    code = CLIENT_ALTONA if (e["member"] == "WMH" and e["letter"] == "A") else CLIENT[e["member"]]
    return code, "%s/%s" % (code, digits)


def _t(d, minutes):
    return dt.datetime.combine(d, dt.time(0, 0)) + dt.timedelta(minutes=float(minutes))


def in_outage(t):
    return K.OUTAGE[0] <= t < K.OUTAGE[1]


def referrals(W):
    """The members' referrals to Bellbird, sent from mid-June to 30 September 2026 (Melbourne time), with Bellbird's
    response and the run of visits Bellbird made for each accepted one."""
    out = []
    for m in K.MEMBERS:
        r = K.rng("referrals", m) if ASK_SALT == 0 else K.rng("referrals", ASK_SALT, m)
        cands = [e for e in W.eps if e["member"] == m and e["last"] >= REF_FROM and e["adm"] <= dt.date(2026, 9, 28)]
        chosen = []
        for e in cands:
            if r.random() >= P_REF[m]:
                continue
            chosen.append(e)
        # each member phones at least one referral during the portal outage
        outage_days = K.days(K.OUTAGE[0].date(), K.OUTAGE[1].date())
        for e in chosen:
            e["_ref"] = None
        for e in chosen:
            lo = max(e["adm"], REF_FROM)
            hi = min(e["last"], dt.date(2026, 9, 28))
            if hi < lo:
                continue
            if e["adm"] >= REF_FROM and r.random() < 0.5:
                rd = e["adm"]
                mins = r.uniform(8 * 60, 11 * 60)
            else:
                rd = lo + dt.timedelta(days=int(r.integers(0, (hi - lo).days + 1)))
                mins = r.uniform(8 * 60, 11.5 * 60) if r.random() < 0.6 else r.uniform(11.5 * 60, 17.5 * 60)
            e["_ref"] = (rd, mins)
        n_out = sum(1 for e in chosen if e["_ref"] and in_outage(_t(*e["_ref"])))
        if n_out == 0:
            pool_out = [e for e in cands if e not in chosen and e["adm"] <= outage_days[1]
                        and e["last"] >= outage_days[2]]
            e = pool_out[int(r.integers(len(pool_out)))]
            rd = outage_days[1 + int(r.integers(0, 2))]
            e["_ref"] = (rd, r.uniform(8.5 * 60, 12 * 60))
            chosen.append(e)
        for e in chosen:
            if not e["_ref"]:
                continue
            rd, mins = e["_ref"]
            sent = _t(rd, round(mins))
            start = rd if mins < 11 * 60 else rd + dt.timedelta(days=1)
            if start > e["last"] or start > dt.date(2026, 9, 30):
                start = rd
            phone = in_outage(sent)
            declined = r.random() < P_DECLINE
            lag = float(np.clip(r.lognormal(math.log(36 if phone else 52), 0.85), 4, 240 if phone else 600))
            if abs(lag - 120) < 2.5:          # whole minutes: keep clear of an exact two-hour tie
                lag += 5
            resp = sent + dt.timedelta(minutes=round(lag))
            if resp.hour >= 20:
                resp = _t(resp.date() + dt.timedelta(days=1), r.uniform(7 * 60 + 40, 8 * 60 + 30))
            resp = resp.replace(second=0, microsecond=0)
            ref = dict(member=m, ep=e, sent=sent, start=start, phone=phone, declined=declined, resp=resp)
            if not declined:
                run = _run(W, e, ref, r)
                if not run:
                    ref["declined"] = True
                ref["run"] = run
            out.append(ref)
        for e in chosen:
            e.pop("_ref", None)
    out.sort(key=lambda x: (x["sent"], x["member"]))
    return out


def _run(W, e, ref, r):
    """Bellbird's visits for an accepted referral: from the first visit day for a run of days or to the end of the
    stay, each day's visits by the visit schedule."""
    s = e["stream"]
    resp = ref["resp"]
    f = max(ref["start"], resp.date())
    if resp.hour >= 15 and f == resp.date():
        f = f + dt.timedelta(days=1)
    if r.random() < 0.07:
        f = f + dt.timedelta(days=1)
    # move to the stay's next visit day (wound care every second day)
    while f <= e["last"] and K.visits_on_day(s, (f - e["adm"]).days) == 0:
        f += dt.timedelta(days=1)
    if f > e["last"] or f > dt.date(2026, 9, 30):
        return []
    R = 1 + int(r.geometric(0.2))
    end = min(e["last"], f + dt.timedelta(days=R - 1 + (R if s == "H06" else 0)))
    base = r.normal(10.5 * 60, 110) if r.random() > 0.09 else r.uniform(18 * 60, 20.25 * 60)
    if r.random() < 0.025:
        base = r.uniform(6.2 * 60, 6.9 * 60)
    base = float(np.clip(base, 6 * 60 + 10, 20.5 * 60))
    if s == "H08":
        base = float(np.clip(r.normal(9.5 * 60, 50), 7 * 60, 12 * 60))
    nurses = NURSES[e["member"]]
    primary = nurses[int(r.integers(len(nurses)))]
    dur_lo, dur_hi = {"IVT": (35, 70), "WND": (30, 60), "CLN": (25, 50)}[K.VISIT_TYPE[s]]
    visits = []
    d = f
    first = True
    while d <= end:
        k = (d - e["adm"]).days
        n = K.visits_on_day(s, k)
        for j in range(n):
            if j == 0:
                mins = base + r.normal(0, 22)
                if first and d == resp.date():
                    mins = max(mins, resp.hour * 60 + resp.minute + r.uniform(50, 150))
            else:
                mins = r.uniform(17.5 * 60, 20.5 * 60)
            mins = float(np.clip(mins, 6 * 60 + 5, 21 * 60))
            nurse = primary if r.random() < 0.7 else nurses[int(r.integers(len(nurses)))]
            st = _t(d, round(mins))
            if first and j == 0 and abs((st - resp).total_seconds() / 60 - 1440) < 4:
                st += dt.timedelta(minutes=9)     # whole minutes: keep clear of an exact 24-hour tie
            du = int(r.integers(dur_lo, dur_hi + 1))
            visits.append(dict(day=d, start=st, end=st + dt.timedelta(minutes=du), nurse=nurse, status="done",
                               first=first))
            first = False
        d += dt.timedelta(days=1)
    if not visits:
        return []
    # unscheduled returns later the same day to intravenous patients, ordered by the treating team
    extra = []
    for v in visits:
        if K.VISIT_TYPE[s] == "IVT" and not v["first"] and r.random() < P_CALLOUT:
            st = v["start"] + dt.timedelta(minutes=int(r.integers(4 * 60, 9 * 60)))
            if st.date() != v["start"].date() or st.hour * 60 + st.minute > 21 * 60 + 30:
                st = v["start"].replace(hour=21, minute=int(r.integers(0, 30)))
            if st <= v["end"]:
                continue
            extra.append(dict(day=v["day"], start=st, end=st + dt.timedelta(minutes=int(r.integers(20, 46))),
                              nurse=nurses[int(r.integers(len(nurses)))], status="done", first=False))
    visits = sorted(visits + extra, key=lambda v: v["start"])
    # attempts (patient not at home, revisited the same day) and cancellations (the member's nurse went instead)
    out = []
    for v in visits:
        u = r.random()
        if u < P_ATTEMPT and v["start"].hour < 18:
            a = dict(v)
            a["status"] = "attempt"
            a["end"] = a["start"] + dt.timedelta(minutes=int(r.integers(5, 12)))
            out.append(a)
            back = v["start"] + dt.timedelta(minutes=int(r.integers(95, 240)))
            if back.hour >= 21:
                back = v["start"] + dt.timedelta(minutes=70)
            dur = v["end"] - v["start"]
            out.append(dict(v, start=back, end=back + dur, first=False))
        elif u < P_ATTEMPT + P_CANCEL and not v["first"]:
            out.append(dict(v, status="cancel", end=None))
        else:
            out.append(v)
    return out


def bellbird_records(W):
    """Every record Bellbird's platform holds for the alliance's patients from 1 July to 30 September 2026
    (Melbourne), re-entered duplicates included, with the posting time."""
    recs = []
    for ref in W.refs:
        if ref["declined"]:
            continue
        e = ref["ep"]
        code, pref = bellbird_ref(e)
        for v in ref["run"]:
            if not (K.Q3S <= v["start"].date() <= K.Q3E):
                continue
            recs.append(dict(member=e["member"], client=code, pref=pref, stream=e["stream"], type=K.VISIT_TYPE[e["stream"]],
                             nurse=v["nurse"], start=v["start"], end=v["end"], status=v["status"], replay=False,
                             ref=ref))
    r = K.rng("posting")
    for x in recs:
        base = x["end"] if x["end"] else x["start"]
        if r.random() < P_LATE_POST:
            x["posted"] = base + dt.timedelta(minutes=int(r.integers(35, 420)))
        else:
            x["posted"] = base + dt.timedelta(minutes=int(r.integers(2, 15)))
    # re-entered visits: the nurse keys a visit again when the app shows it unsent
    rr = K.rng("replays")
    reps = []
    for x in recs:
        if x["status"] == "cancel":
            continue
        if rr.random() < P_REPLAY[x["member"]]:
            reps.append(_replay(x, rr))
    have = {(x["member"], x["start"].month) for x in reps}
    for m in K.MEMBERS:
        for mo in (7, 8, 9):
            if (m, mo) not in have:
                cand = [x for x in recs if x["member"] == m and x["start"].month == mo and x["status"] == "done"]
                reps.append(_replay(cand[int(rr.integers(len(cand)))], rr))
    recs.extend(reps)
    recs.sort(key=lambda x: (x["posted"], x["pref"], x["start"]))
    rn = K.rng("visit_no")
    n = 6104000
    for x in recs:
        n += int(rn.integers(3, 26))
        x["visit_no"] = "BV%07d" % n
    return recs


def lines(t, x):
    """Where a start time sits against every line a record's figures turn on: its Melbourne day (the weekend and
    public holiday loadings, the month, the pay week, the quarter), 7.00 am and 6.00 pm (the weekday loading) and, for
    the referral the record serves, the acceptance and 24 hours after it (the first-visit clock)."""
    resp = x["ref"]["resp"]
    return (t.date(), t.hour < 7, t.hour >= 18, t >= resp, t <= resp + dt.timedelta(hours=K.FIRST_VISIT_HOURS))


def _keyed_again(x, r, same_side):
    """The times a nurse keys for a visit the second time: start and end each up to 12 minutes off the first record,
    the two overlapping; with same_side, at least 2 minutes off at the start and on the first record's side of every
    line in lines()."""
    dur = (x["end"] - x["start"]).total_seconds() / 60
    while True:
        ds = int(r.integers(-12, 13))
        de = int(r.integers(-12, 13))
        st = x["start"] + dt.timedelta(minutes=ds)
        en = x["end"] + dt.timedelta(minutes=de)
        ov = (min(en, x["end"]) - max(st, x["start"])).total_seconds() / 60
        if (en - st).total_seconds() / 60 >= min(10, dur) and ov >= min(5, dur - 1) and \
                (not same_side or (abs(ds) >= 2 and lines(st, x) == lines(x["start"], x))):
            return st, en


def _replay(x, rr):
    """A record the app posts again under a fresh number. The re-keyed times never cross a line the record's fee,
    day or clocks turn on, so either record of the pair carries the same figures; a draw that would cross one is
    redrawn from the record's own stream, leaving the shared stream (and every other pair) as it was."""
    st, en = _keyed_again(x, rr, False)
    if lines(st, x) != lines(x["start"], x):
        st, en = _keyed_again(x, K.rng("replay_side", x["nurse"], x["pref"], x["start"].isoformat()), True)
    y = dict(x, start=st, end=en, replay=True, orig=x)
    y["posted"] = x["posted"] + dt.timedelta(minutes=int(rr.integers(120, 1800)))
    return y


# ---------------------------------------------------------------------------------------------------- the register
REG_STAFF = ["JW", "AN", "PK", "SL", "RD", "MB", "TQ"]
# Bellbird's intake desk opened a file under the intake log number for each patient referred by telephone while the
# portal was down, and linked those files to the Members' patient numbers once the portal was back (Melbourne time)
INTAKE_LINKED = dt.datetime(2026, 8, 14, 16, 40)
SUBURBS = ["Coburg", "Brunswick West", "Preston", "Reservoir", "Thornbury", "Glenroy", "Broadmeadows", "Craigieburn",
           "Epping", "Lalor", "Sunshine", "St Albans", "Deer Park", "Footscray", "Altona", "Altona Meadows", "Werribee",
           "Point Cook", "Hoppers Crossing", "Essendon", "Pascoe Vale", "Keilor East", "Sydenham", "Tarneit", "Melton",
           "Bundoora", "Mill Park", "Greensborough", "Fawkner", "Laverton", "Williamstown", "Maribyrnong", "Taylors Lakes",
           "Roxburgh Park", "Gladstone Park", "Kings Park", "Caroline Springs", "Wollert", "Mernda", "Thomastown"]
FAMILY = ["Daughter", "Son", "Wife", "Husband", "Patient", "Carer", "Neighbour", "Granddaughter", "Partner"]
OTHER_ORGS = [("Private client", ["Patient", "Daughter", "Son", "Wife", "Husband", "Carer"], 0.34),
              ("GP practice", ["Practice nurse", "GP", "Practice manager"], 0.24),
              ("Residential aged care", ["Facility nurse", "Care manager", "Clinical nurse consultant"], 0.14),
              ("Transition care program", ["Case manager", "Care coordinator"], 0.10),
              ("Community pharmacy", ["Pharmacist"], 0.06),
              ("NDIS support coordinator", ["Support coordinator"], 0.06),
              ("Home care package provider", ["Care manager", "Case manager"], 0.06)]
SERVICES = ["wound care", "catheter care", "medication prompting", "post-op wound review", "palliative support",
            "diabetes support", "stoma care", "compression bandaging", "PICC line flush", "insulin administration",
            "pressure injury care", "drain care", "suture removal", "eye drops", "bowel care", "blood glucose checks"]
FREQ = ["", ", daily", ", twice weekly", ", three times a week", ", weekly", ", alternate days", ", twice daily"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _dm(d):
    return "%d/%02d" % (d.day, d.month)


def _hm12(minutes):
    h, m = divmod(int(minutes), 60)
    suf = "am" if h < 12 else "pm"
    h12 = h if 1 <= h <= 12 else (h - 12 if h > 12 else 12)
    return ("%d%s" % (h12, suf)) if m == 0 else ("%d.%02d%s" % (h12, m, suf))


def _choice(r, seq):
    return seq[int(r.integers(len(seq)))]


def _enquiry_note(r, d, who, alliance):
    sub = _choice(r, SUBURBS)
    day = _choice(r, ["today's", "tomorrow's", "this afternoon's", "the morning", "Saturday's", "Sunday's",
                      "%s's" % WEEKDAYS[(d.weekday() + 1) % 7]])
    opts = [
        lambda: "%s asking ETA for %s visit" % (who, day),
        lambda: "%s asked to move visit to after %s" % (who, _hm12(60 * int(r.integers(9, 15)) + 30 * int(r.integers(2)))),
        lambda: "%s asked if same nurse can come %s" % (who, _choice(r, ["tomorrow", "next week", "on the weekend",
                                                                          "for the rest of the course"])),
        lambda: "Asked nurse to ring ahead, %s" % _choice(r, ["dog in the yard", "gate code changed", "intercom broken",
                                                               "works nights", "hard of hearing", "new address in %s"
                                                               % sub, "unit at the back"]),
        lambda: "%s asked whether visits continue over %s" % (who, _choice(r, ["the weekend", "the long weekend",
                                                                                "Easter", "the public holiday"])),
        lambda: "%s reports %s, advised to call the HITH team" % (who, _choice(r, ["the pump alarming overnight",
                                                                                   "the line site red",
                                                                                   "the dressing lifting",
                                                                                   "patient feeling unwell",
                                                                                   "a missed dose"])),
        lambda: "%s wants a morning visit before %s" % (who, _choice(r, ["dialysis", "work", "an appointment",
                                                                         "school drop-off", "a specialist review"])),
        lambda: "%s asking what time nurse finished %s" % (who, _choice(r, ["yesterday", "on Saturday", "this morning"])),
        lambda: "%s rang to say patient back in hospital" % who if alliance else "%s asking about private rates" % who,
        lambda: "%s asking whether Bellbird covers %s" % (who, _choice(r, SUBURBS)),
        lambda: "%s gave a new contact number for %s" % (who, _choice(r, ["visits", "the nurse", "the family"])),
    ]
    if not alliance:
        opts += [lambda: "Invoice query, private visits in %s" % K.MONTH_NAME[max(1, d.month - 1)],
                 lambda: "Asked about weekend visits in %s" % sub,
                 lambda: "Asked whether Bellbird can take a new client for %s in %s" % (_choice(r, SERVICES), sub)]
    return opts[int(r.integers(len(opts)))]()


HOLIDAYS_2026 = [(dt.date(2026, 1, 26), "Australia Day"), (dt.date(2026, 3, 9), "Labour Day"),
                 (dt.date(2026, 4, 3), "Easter"), (dt.date(2026, 4, 25), "Anzac Day"),
                 (dt.date(2026, 6, 8), "the King's Birthday weekend"), (dt.date(2026, 9, 25), "the Grand Final holiday"),
                 (dt.date(2026, 11, 3), "Melbourne Cup")]


def _next_break(r, d):
    for h, name in HOLIDAYS_2026:
        if 0 <= (h - d).days <= 16:
            return name
    return _choice(r, ["the weekend", "the school holidays", "Saturday", "next week"])


def _roster_note(r, d):
    n = int(r.choice([1, 1, 2, 2, 3, 4]))
    when = _choice(r, ["tomorrow", "Saturday", "Sunday", "this weekend", "next week", "%s" % WEEKDAYS[(d.weekday() + 2) % 7],
                       "from %s" % _dm(d + dt.timedelta(days=int(r.integers(1, 6))))])
    opts = [
        lambda: "Asked capacity for %d patient%s %s" % (n, "" if n == 1 else "s", when),
        lambda: "Checking evening capacity %s" % when,
        lambda: "Asked if Bellbird can hold a nurse for the %s run %s" % (_choice(r, SUBURBS), when),
        lambda: "Asked whether %d IV patient%s can go to Bellbird %s" % (n, "" if n == 1 else "s", when),
        lambda: "Roster check before %s" % _next_break(r, d),
        lambda: "Own nurses short %s, %d patient%s may come over" % (when, n, "" if n == 1 else "s"),
        lambda: "Asked for early start capacity %s" % when,
        lambda: "Handing %d patient%s back to own nurses %s" % (n, "" if n == 1 else "s", when),
    ]
    return opts[int(r.integers(len(opts)))]()


def _referral_note(r, d, org):
    svc = _choice(r, SERVICES) + _choice(r, FREQ)
    sub = _choice(r, SUBURBS)
    start = d + dt.timedelta(days=int(r.choice([0, 1, 1, 2, 3, 7])))
    opts = [
        lambda: "New client, %s" % svc,
        lambda: "%s, %s, start %s" % (svc[0].upper() + svc[1:], sub, _dm(start)),
        lambda: "Discharge %s, %s" % (_dm(start), svc),
        lambda: "%s referral, %s" % (org.split()[0], svc),
        lambda: "New client in %s, %s" % (sub, svc),
        lambda: "Referral for %s from %s" % (svc, _dm(start)),
    ]
    return opts[int(r.integers(len(opts)))]()


def _feedback_note(r, who):
    opts = [
        lambda: "Compliment for the %s nurse" % _choice(r, ["morning", "evening", "weekend", "Sunday", "regular"]),
        lambda: "%s unhappy, visit %d minutes late" % (who, int(r.integers(4, 15)) * 5),
        lambda: "Asked for a female nurse",
        lambda: "Parking problem at %s address" % _choice(r, SUBURBS),
        lambda: "%s thanked the team for weekend visits" % who,
        lambda: "%s asked for the same nurse each visit" % who,
        lambda: "Complaint, nurse did not ring ahead",
        lambda: "%s says nurse was very thorough" % who,
    ]
    return opts[int(r.integers(len(opts)))]()


def _followup_note(r, ref):
    sent = ref["sent"]
    st = K.SNAME[ref["ep"]["stream"]].lower()
    opts = [
        lambda: "Chasing portal referral sent %s" % _hm12(sent.hour * 60 + sent.minute),
        lambda: "Portal referral not acknowledged yet, %s" % st,
        lambda: "Checking referral received, start %s" % _dm(ref["start"]),
        lambda: "Following up referral, %s, start %s" % (st, _dm(ref["start"])),
        lambda: "Rang to check portal referral had come through",
        lambda: "Asked for an answer on the %s referral" % _hm12(sent.hour * 60 + sent.minute),
    ]
    return opts[int(r.integers(len(opts)))]()


def _phone_note(r, ref):
    st = K.SNAME[ref["ep"]["stream"]].lower()
    s = _dm(ref["start"])
    opts = [
        lambda: "Portal down, referral by phone. %s, start %s" % (st[0].upper() + st[1:], s),
        lambda: "Phoned through, portal unavailable. Start %s" % s,
        lambda: "%s, start %s" % (st[0].upper() + st[1:], s),
        lambda: "Referral by phone, %s. Requested start %s" % (st, s),
        lambda: "New referral, %s, from %s" % (st, s),
        lambda: "Coordinator rang the referral through, start %s" % s,
    ]
    return opts[int(r.integers(len(opts)))]()


def register(W):
    """Bellbird's intake line log for 2026 (2 January to 30 October): enquiries, roster calls, other clients' referrals,
    feedback, follow-ups of portal referrals, and the Alliance referrals taken by telephone while the portal was down."""
    r = K.rng("register")
    rt = K.rng("register_text")
    rows = []
    org_names = [o for o, _, _ in OTHER_ORGS]
    org_w = np.array([w for _, _, w in OTHER_ORGS])
    for d in K.days(dt.date(2026, 1, 2), dt.date(2026, 10, 30)):
        wk = d.weekday()
        n = r.poisson(3.1 if wk < 5 else 0.9)
        for _ in range(n):
            t = _t(d, round(r.uniform(7.5 * 60, 19.5 * 60)))
            u = r.random()
            row = dict(t=t, patient=None, out_t=None, member=None, ref=None)
            if u < 0.43:
                alliance = r.random() < 0.45
                if alliance:
                    m = K.MEMBERS[int(r.integers(5))]
                    org, caller = K.NAME[m], _choice(rt, FAMILY)
                else:
                    k = int(r.choice(len(org_names), p=org_w / org_w.sum()))
                    org, caller = org_names[k], _choice(rt, OTHER_ORGS[k][1])
                who = caller if caller in FAMILY else ("Patient's family" if rt.random() < 0.3 else caller)
                row.update(kind="Enquiry", org=org, caller=caller, note=_enquiry_note(rt, d, who, alliance),
                           outcome=_choice(rt, ["Advised"] * 6 + ["Passed to nurse", "Passed to roster", "Rang back"]))
            elif u < 0.62:
                m = K.MEMBERS[int(r.integers(5))]
                row.update(kind="Roster", org=K.NAME[m], caller=_choice(rt, ["HITH coordinator", "Nurse in charge, HITH",
                                                                            "HITH manager", "Associate nurse unit manager"]),
                           note=_roster_note(rt, d), outcome=_choice(rt, ["Passed to roster"] * 3 + ["Confirmed", "Advised"]))
            elif u < 0.88:
                k = int(r.choice(len(org_names), p=org_w / org_w.sum()))
                org = org_names[k]
                row.update(kind="Referral", org=org, caller=_choice(rt, OTHER_ORGS[k][1]),
                           note=_referral_note(rt, d, org), patient="P%06d" % int(r.integers(410000, 489999)))
                v = r.random()
                row["outcome"] = "Accepted" if v < 0.8 else ("Declined" if v < 0.92 else "Waitlisted")
                if row["outcome"] == "Accepted":
                    row["out_t"] = t + dt.timedelta(minutes=int(r.integers(10, 150)))
            else:
                alliance = r.random() < 0.3
                if alliance:
                    org, caller = K.NAME[K.MEMBERS[int(r.integers(5))]], _choice(rt, FAMILY)
                else:
                    k = int(r.choice(len(org_names), p=org_w / org_w.sum()))
                    org, caller = org_names[k], _choice(rt, OTHER_ORGS[k][1])
                who = caller if caller in FAMILY else "Family"
                row.update(kind="Feedback", org=org, caller=caller, note=_feedback_note(rt, who),
                           outcome=_choice(rt, ["Logged", "Logged", "Passed to clinical lead"]))
            rows.append(row)
    # follow-up calls about portal referrals Bellbird had not answered
    for ref in W.refs:
        if ref["phone"]:
            continue
        lag = (ref["resp"] - ref["sent"]).total_seconds() / 60
        if lag > 50 and r.random() < 0.38:
            t = ref["sent"] + dt.timedelta(minutes=int(r.integers(40, int(min(lag, 240)))))
            rows.append(dict(t=t, kind="Referral follow-up", org=_org(ref["ep"]), patient=ref["ep"]["patient"],
                             caller=_choice(rt, ["HITH coordinator", "Nurse in charge, HITH"]),
                             note=_followup_note(rt, ref), outcome=_choice(rt, ["Advised", "Passed to intake nurse"]),
                             out_t=None, member=ref["member"], ref=ref))
    # the Alliance referrals telephoned while the portal was down
    for ref in W.refs:
        if ref["phone"]:
            rows.append(dict(t=ref["sent"], kind="Referral", org=_org(ref["ep"]), patient=_spoken(ref["ep"], r),
                             caller=_choice(rt, ["HITH coordinator", "Nurse in charge, HITH",
                                                 "Associate nurse unit manager"]),
                             note=_phone_note(rt, ref), outcome="Declined" if ref["declined"] else "Accepted",
                             out_t=ref["resp"], member=ref["member"], ref=ref))
    for ep_m in K.MEMBERS[:3]:
        t = _t(K.OUTAGE_MAR[0].date(), round(r.uniform(9 * 60, 15 * 60)))
        st = K.SNAME[["H01", "H02", "H06"][K.MEMBERS.index(ep_m)]].lower()
        rows.append(dict(t=t, kind="Referral", org=K.NAME[ep_m], patient=_patient_like(ep_m, r),
                         caller=_choice(rt, ["HITH coordinator", "Nurse in charge, HITH"]),
                         note=_choice(rt, ["Portal down, phoned through. %s" % (st[0].upper() + st[1:]),
                                           "Referral by phone, %s, start %s" % (st, _dm(t.date())),
                                           "Portal unavailable this morning, %s" % st]),
                         outcome="Accepted", out_t=t + dt.timedelta(minutes=int(r.integers(15, 80))), member=ep_m,
                         ref=None))
    for x in rows:
        x["by"] = REG_STAFF[int(r.integers(len(REG_STAFF)))]
    rows.sort(key=lambda x: x["t"])
    for i, x in enumerate(rows):
        x["log"] = "IL26-%04d" % (i + 1)
        if x["ref"] is not None and x["kind"] == "Referral":
            x["ref"]["log"] = x["log"]
    return rows


def intake_files(W):
    """Bellbird's records for patients referred by telephone during the August outage: without a portal referral the
    desk could not open the patient under the Member's account, so it opened a file under the Alliance's billing account
    with the intake log number as the reference; records posted after the desk linked the files (INTAKE_LINKED) carry
    the Member's account and patient number. A record the app re-posts keeps what it was first posted with."""
    for x in W.bb:
        x["pref_member"] = x["pref"]
        x["client_member"] = x["client"]
        ref = x["ref"]
        if not ref["phone"]:
            continue
        first_post = x["orig"]["posted"] if x["replay"] else x["posted"]
        if first_post < INTAKE_LINKED:
            x["client"] = CLIENT_OFFICE
            x["pref"] = "%s/%s" % (CLIENT_OFFICE, ref["log"])


def _org(e):
    if e["member"] == "WMH" and e["letter"] == "A":
        return "Westmere Health (Altona Park)"
    return K.NAME[e["member"]]


def _spoken(e, r):
    """The patient number as the caller gave it."""
    p = e["patient"]
    if e["member"] == "NGH" and r.random() < 0.5:
        return p.lstrip("0")
    if e["member"] == "HCH" and r.random() < 0.5:
        return p[:-1] + " H"
    return p


def _patient_like(m, r):
    return _patient_no(m, int(r.integers(300000, 399999)), "W")


def simulate():
    W = World()
    W.eps = episodes()
    W.pool = pools(W.eps)
    W.adm = plan_admissions(W.eps)
    W.visits, W.visits_exact = plan_visits(W.eps, W.adm, W.pool)
    W.plan_q = {m: quarter_plan(W.visits, m) for m in K.MEMBERS}
    place_capacity(W)
    W.refs = referrals(W)
    W.bb = bellbird_records(W)
    W.reg = register(W)
    intake_files(W)
    return W


if __name__ == "__main__":
    W = simulate()
    print("episodes", len(W.eps), "open", sum(e["open"] for e in W.eps))
    for m in K.MEMBERS:
        req, p90, mean, sd = MD.requirement(W.adm[m], W.pool, W.plan_q[m])
        print(m, "plan", W.plan_q[m], "req", round(req, 1), "cap", W.capacity[m], "excess", round(req - W.capacity[m], 1),
              "lots", K.lots_for(req - W.capacity[m]))
    refs = W.refs
    for m in K.MEMBERS:
        q3 = [x for x in refs if x["member"] == m and K.Q3S <= x["sent"].date() <= K.Q3E]
        print(m, "refs Q3", len(q3), "phone", sum(x["phone"] for x in q3), "declined", sum(x["declined"] for x in q3),
              "bb records", sum(1 for x in W.bb if x["member"] == m), "replays", sum(1 for x in W.bb if x["member"] == m and x["replay"]))
    print("register rows", len(W.reg))
