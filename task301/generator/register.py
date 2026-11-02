"""The Complemento Familiar's administrative register from its October 2022 launch to October 2026: every claim,
review and decision, and the 2025 incident log (suspensions, births, eighteenth birthdays, moves). The register's
families are an administrative population sized from the survey's weighted counts; they are not the survey's
households."""
import datetime as dt

import numpy as np

import params as P

# share of eventual claimants who have claimed by month k after a claim window opens (k = 1, 2, ...)
PACE_LAUNCH = [0.12, 0.20, 0.27, 0.325, 0.375, 0.43, 0.47, 0.505, 0.54, 0.57, 0.595, 0.62,
               0.645, 0.67, 0.695, 0.72, 0.745, 0.77, 0.79, 0.81, 0.83, 0.85, 0.87, 0.89,
               0.905, 0.92, 0.935, 0.945, 0.955, 0.965, 0.972, 0.979, 0.986, 0.991, 0.996, 1.0]
PACE_WIDENING = [0.07, 0.13, 0.19, 0.245, 0.295, 0.34, 0.385, 0.425, 0.46, 0.495, 0.53, 0.56,
                 0.59, 0.62, 0.65, 0.68, 0.705, 0.73, 0.755, 0.78, 0.805, 0.83, 0.855, 0.88,
                 0.90, 0.92, 0.935, 0.95, 0.962, 0.973, 0.982, 0.989, 0.994, 0.997, 0.999, 1.0]
EVENTUAL = 0.82

T0 = (2022, 10)


def t_of(y, m):
    return (y - T0[0]) * 12 + (m - T0[1])


def ym_of(t):
    y = T0[0] + (T0[1] - 1 + t) // 12
    m = (T0[1] - 1 + t) % 12 + 1
    return y, m


def month_start(t):
    y, m = ym_of(t)
    return dt.date(y, m, 1)


def days_in(t):
    y, m = ym_of(t)
    n = dt.date(y + (m // 12), m % 12 + 1, 1)
    return (n - dt.date(y, m, 1)).days


LAST_T = t_of(*P.REGISTER_LAST_MONTH)          # October 2026
RISE_T = t_of(2024, 4)


def office_code(muni_by_code, code):
    return {"VAL": "81", "CUE": "82", "SIE": "83"}[muni_by_code[code]["office"]]


def draw_pace_month(rng, pace):
    u = float(rng.random())
    for k, f in enumerate(pace, start=1):
        if u <= f:
            return k
    return len(pace)


def build(rng, W):
    hh = W["hh"]
    munis = W["munis"]
    muni_by_code = {m["code"]: m for m in munis}
    by_prov = {}
    for m in munis:
        by_prov.setdefault(m["prov"], []).append(m)
    # the survey's weighted entitled families, by band, as the population the register draws from
    kids = [h for h in hh if h["kids"] > 0]
    w = np.array([h["w"] for h in kids])
    assessed = np.array([h["assessed"] for h in kids])
    low = [i for i, h in enumerate(kids) if h["assessed"] < P.CFV_LIMIT_OLD]
    band = [i for i, h in enumerate(kids) if P.CFV_LIMIT_OLD <= h["assessed"] < P.CFV_LIMIT]
    above = [i for i, h in enumerate(kids) if P.CFV_LIMIT <= h["assessed"] < 11500]
    n_low = int(round(w[low].sum()))
    n_band = int(round(w[band].sum()))

    def sample(idx, n):
        p = w[idx] / w[idx].sum()
        return [kids[i] for i in rng.choice(idx, size=n, p=p)]

    def place(h):
        ms = by_prov[h["prov"]]
        sh = np.array([m["share"] for m in ms])
        return ms[int(rng.choice(len(ms), p=sh / sh.sum()))]["code"]

    fams = []
    fid = 0

    def new_family(h, entitled_t, cohort, inc):
        nonlocal fid
        fid += 1
        k = h["kids"]
        youngest = min(a for a in h["ages"] if a <= 17)
        fams.append({"fid": fid, "kids": k, "youngest_age27": youngest, "inc": inc, "muni": place(h),
                     "entitled_t": entitled_t, "cohort": cohort})
        return fams[-1]

    # launch stock: entitled when the claim window opened
    for h in sample(low, n_low):
        new_family(h, 0, "launch", h["assessed"] * float(np.exp(rng.normal(0, 0.04))))
    # widening stock: entitled from 1 April 2024
    for h in sample(band, n_band):
        inc = min(P.CFV_LIMIT - 1, max(P.CFV_LIMIT_OLD, h["assessed"] * float(np.exp(rng.normal(0, 0.02)))))
        new_family(h, RISE_T, "widening", inc)
    # inflow: families newly entitled month by month (a birth, a fall in income)
    for t in range(1, LAST_T + 1):
        limit = P.CFV_LIMIT_OLD if t < RISE_T else P.CFV_LIMIT
        n_in = int(rng.poisson(0.0062 * (n_low + (n_band if t >= RISE_T else 0))))
        pool = low if t < RISE_T else low + band
        for h in sample(pool, n_in):
            inc = min(limit - 1, h["assessed"] * float(np.exp(rng.normal(0, 0.05))))
            new_family(h, t, "inflow", inc)

    awards = []
    incidents = []
    seq = {}

    def expediente(year):
        seq[year] = seq.get(year, 0) + 1
        return "CFV-%d-%06d" % (year, seq[year])

    def claim_day(t):
        return month_start(t) + dt.timedelta(days=int(rng.integers(0, days_in(t))))

    def decide(claim_date):
        lag = int(np.clip(np.exp(rng.normal(np.log(24.0), 0.50)), 4, 95))
        return claim_date + dt.timedelta(days=lag)

    def tm(d):
        return t_of(d.year, d.month)

    rate_at = lambda t: [r for (yy, mm), r in P.CFV_RATES if t_of(yy, mm) <= t][-1]

    for f in fams:
        if rng.random() >= EVENTUAL:
            continue
        if f["cohort"] == "launch":
            ct = draw_pace_month(rng, PACE_LAUNCH) - 1
        elif f["cohort"] == "widening":
            ct = RISE_T + draw_pace_month(rng, PACE_WIDENING) - 1
        else:
            ct = f["entitled_t"] + int(rng.exponential(4.0))
        if ct > LAST_T:
            continue
        cd = claim_day(ct)
        dd = decide(cd)
        if dd > P.REGISTER_PULL:
            awards.append(dict(ex=expediente(cd.year), fid=f["fid"], tipo="I", claim=cd, dec=None, res="P",
                               ejercicio=cd.year - (1 if cd.month >= 7 else 2), inc=f["inc"], kids=f["kids"],
                               muni=f["muni"], first=None, last=None, rate=None))
            continue
        year = cd.year
        first = tm(dd) + 1
        f["claimed"] = True
        # the life of the award: reviews every twelve months, exits
        exit_hazard = 0.0034
        end_t = None
        start = first
        tipo = "I"
        ex = expediente(year)
        claim_date, dec_date = cd, dd
        ejercicio = cd.year - (1 if cd.month >= 7 else 2)
        inc = f["inc"]
        while True:
            review = start + 12
            # exits between reviews (left the region, youngest child no longer counted)
            end_t = None
            for t in range(start, min(review, LAST_T + 1)):
                if rng.random() < exit_hazard:
                    end_t = t
                    break
            if end_t is not None:
                awards.append(dict(ex=ex, fid=f["fid"], tipo=tipo, claim=claim_date, dec=dec_date, res="C",
                                   ejercicio=ejercicio, inc=inc, kids=f["kids"], muni=f["muni"], first=start,
                                   last=end_t, rate=rate_at(start)))
                break
            if review > LAST_T:
                awards.append(dict(ex=ex, fid=f["fid"], tipo=tipo, claim=claim_date, dec=dec_date, res="C",
                                   ejercicio=ejercicio, inc=inc, kids=f["kids"], muni=f["muni"], first=start,
                                   last=None, rate=rate_at(start)))
                break
            # annual review: notice early in the month before, decision in the review month
            inc = inc * float(np.exp(rng.normal(0.0, 0.06)))
            limit = P.CFV_LIMIT_OLD if review < RISE_T else P.CFV_LIMIT
            rclaim = month_start(review - 1) + dt.timedelta(days=int(rng.integers(0, 10)))
            rdec = month_start(review) + dt.timedelta(days=int(rng.integers(0, min(25, days_in(review)))))
            rex = expediente(rclaim.year)
            if inc >= limit:
                awards.append(dict(ex=ex, fid=f["fid"], tipo=tipo, claim=claim_date, dec=dec_date, res="C",
                                   ejercicio=ejercicio, inc=inc if tipo == "I" else inc, kids=f["kids"],
                                   muni=f["muni"], first=start, last=review - 1, rate=rate_at(start)))
                awards.append(dict(ex=rex, fid=f["fid"], tipo="R", claim=rclaim, dec=rdec, res="D",
                                   ejercicio=rclaim.year - (1 if rclaim.month >= 7 else 2), inc=inc,
                                   kids=f["kids"], muni=f["muni"], first=None, last=None, rate=None))
                break
            # the export closes the earlier resolution in the month the renewal takes effect
            awards.append(dict(ex=ex, fid=f["fid"], tipo=tipo, claim=claim_date, dec=dec_date, res="C",
                               ejercicio=ejercicio, inc=f["inc"] if tipo == "I" else inc, kids=f["kids"],
                               muni=f["muni"], first=start, last=review, rate=rate_at(start)))
            tipo = "T" if rng.random() < 0.012 else "R"
            ex, claim_date, dec_date = rex, rclaim, rdec
            ejercicio = rclaim.year - (1 if rclaim.month >= 7 else 2)
            start = review
    # refused first claims (income above the limit) and archived withdrawals
    n_ref = int(0.13 * sum(1 for a in awards if a["tipo"] == "I"))
    for _ in range(n_ref):
        h = kids[int(rng.choice(above))] if above else kids[0]
        ct = int(rng.integers(0, LAST_T + 1))
        cd = claim_day(ct)
        dd = decide(cd)
        if tm(dd) > LAST_T:
            continue
        fid += 1
        limit = P.CFV_LIMIT_OLD if ct < RISE_T else P.CFV_LIMIT
        inc = max(limit + 15.0, h["assessed"] * float(np.exp(rng.normal(0.05, 0.05))))
        awards.append(dict(ex=expediente(cd.year), fid=fid, tipo="I", claim=cd, dec=dd, res="D",
                           ejercicio=cd.year - (1 if cd.month >= 7 else 2), inc=inc, kids=h["kids"],
                           muni=place(h), first=None, last=None, rate=None))
    n_arch = int(0.022 * sum(1 for a in awards if a["tipo"] == "I"))
    for _ in range(n_arch):
        h = kids[int(rng.integers(0, len(kids)))]
        ct = int(rng.integers(0, LAST_T + 1))
        cd = claim_day(ct)
        fid += 1
        awards.append(dict(ex=expediente(cd.year), fid=fid, tipo="I", claim=cd,
                           dec=cd + dt.timedelta(days=int(rng.integers(20, 80))), res="A",
                           ejercicio=cd.year - (1 if cd.month >= 7 else 2), inc=None, kids=h["kids"],
                           muni=place(h), first=None, last=None, rate=None))
    return {"fams": fams, "awards": awards, "incidents": incidents}


def add_appeals_and_incidents(rng, R, W):
    """Appeals against 2025 refusals (a second decision on the same claim), and the 2025 incident log: suspensions
    at the year's reviews (lifted with the suspended months paid, or the award extinguished), births, children
    reaching eighteen, and changes of address."""
    aw = R["awards"]
    munis = W["munis"]
    by_prov = {}
    for m in munis:
        by_prov.setdefault(m["prov"], []).append(m)
    y25 = (dt.date(2025, 1, 1), dt.date(2025, 12, 31))
    extra = []
    for a in aw:
        if a["res"] == "D" and a["dec"] is not None and y25[0] <= a["dec"] <= dt.date(2025, 10, 20):
            if rng.random() < 0.13:
                adec = a["dec"] + dt.timedelta(days=int(rng.integers(32, 72)))
                granted = rng.random() < 0.56
                b = dict(a)
                b["dec"] = adec
                b["res"] = "C" if granted else "D"
                b["appeal"] = True
                if granted:
                    b["first"] = t_of(adec.year, adec.month) + 1
                    b["last"] = None
                    b["rate"] = [r for (yy, mm), r in P.CFV_RATES if t_of(yy, mm) <= b["first"]][-1]
                extra.append(b)
    aw.extend(extra)
    inc_rows = []
    # suspensions at 2025 reviews: renewals (R or T) whose first month falls in 2025
    t25a, t25b = t_of(2025, 1), t_of(2025, 12)
    for a in aw:
        if a["tipo"] in ("R", "T") and a["res"] == "C" and a.get("first") is not None and t25a <= a["first"] <= t25b \
                and not a.get("appeal"):
            if rng.random() < 0.075:
                sus_day = month_start(a["first"])
                inc_rows.append({"fid": a["fid"], "ex": a["ex"], "date": sus_day, "type": "SUS", "dato": ""})
                gap = int(rng.choice([1, 2, 3, 4], p=[0.40, 0.30, 0.18, 0.12]))
                lift_t = a["first"] + gap
                if gap <= 3:
                    lift_day = month_start(lift_t) + dt.timedelta(days=int(rng.integers(0, 20)))
                    a["dec"] = lift_day             # the renewal is decided once the documents arrive
                    a["suspended_to"] = lift_t
                    if lift_day <= dt.date(2025, 12, 31):
                        inc_rows.append({"fid": a["fid"], "ex": a["ex"], "date": lift_day, "type": "LEV",
                                         "dato": str(gap)})
                else:
                    ext_day = month_start(a["first"] + 3) + dt.timedelta(days=int(rng.integers(0, 15)))
                    a["res"] = "X"                  # extinguished: never paid
                    a["ext_day"] = ext_day
                    if ext_day <= dt.date(2025, 12, 31):
                        inc_rows.append({"fid": a["fid"], "ex": a["ex"], "date": ext_day, "type": "EXT", "dato": ""})
    # births, eighteenth birthdays and moves among families with an award open in 2025
    open25 = {}
    for a in aw:
        if a["res"] == "C" and a.get("first") is not None and a["first"] <= t25b and (a["last"] is None or a["last"] >= t25a):
            open25[a["fid"]] = a
    for fid in sorted(open25):
        a = open25[fid]
        day = lambda: dt.date(2025, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
        if rng.random() < 0.045:
            inc_rows.append({"fid": fid, "ex": a["ex"], "date": day(), "type": "NAC", "dato": "+1"})
        if rng.random() < 0.055:
            inc_rows.append({"fid": fid, "ex": a["ex"], "date": day(), "type": "MAY", "dato": "-1"})
        if rng.random() < 0.034:
            prov = a["muni"][:2]
            if rng.random() < 0.30:
                prov = str(rng.choice([p for p, _ in P.PROVINCES if p != prov]))
            ms = by_prov[prov]
            sh = np.array([m["share"] for m in ms])
            new = ms[int(rng.choice(len(ms), p=sh / sh.sum()))]["code"]
            if new != a["muni"]:
                inc_rows.append({"fid": fid, "ex": a["ex"], "date": day(), "type": "DOM", "dato": new})
    inc_rows.sort(key=lambda r: (r["date"], r["fid"], r["type"]))
    R["incidents"] = inc_rows
    return R
