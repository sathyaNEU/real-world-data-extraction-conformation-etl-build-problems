"""The Complemento Familiar's administrative register from its October 2022 launch to October 2026: every claim,
review and decision, and the 2025 incident log (suspensions, lifts, extinctions, births, eighteenth birthdays and
moves). The register's families are an administrative population sized from the survey's weighted counts; they are
not the survey's households.

Export conventions (how the benefits system writes a family's history):
- a renewal that takes effect normally is written as a new resolution starting in the review month, and the earlier
  resolution's last month paid is that same review month (one family, two resolutions open in that month, one
  payment);
- a renewal held up by missing documents suspends payment from the review month: the earlier resolution ends the
  month before; the renewal, once the documents arrive (within three months), is decided on that day and starts in
  the review month (the suspended months are paid with the next payment); otherwise it is written as extinguished;
- an appeal against a refusal is a second resolution on the same case number."""
import datetime as dt

import numpy as np

import params as P

# share of eventual claimants who have claimed by month k after a claim window opens (k = 1, 2, ...)
PACE_LAUNCH = [0.12, 0.20, 0.27, 0.325, 0.375, 0.43, 0.47, 0.505, 0.54, 0.57, 0.595, 0.62,
               0.645, 0.67, 0.695, 0.72, 0.745, 0.77, 0.79, 0.81, 0.83, 0.85, 0.87, 0.89,
               0.905, 0.92, 0.935, 0.945, 0.955, 0.965, 0.972, 0.979, 0.986, 0.991, 0.996, 1.0]
PACE_WIDENING = [0.04, 0.075, 0.11, 0.145, 0.18, 0.21, 0.24, 0.27, 0.30, 0.33, 0.36, 0.385,
                 0.41, 0.435, 0.46, 0.49, 0.52, 0.55, 0.58, 0.61, 0.64, 0.67, 0.70, 0.73,
                 0.76, 0.79, 0.82, 0.85, 0.88, 0.905, 0.93, 0.95, 0.965, 0.98, 0.99, 1.0]
EVENTUAL = 0.82
SUSPEND_P = 0.075

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
T25A, T25B = t_of(2025, 1), t_of(2025, 12)
YEAR_END = dt.date(2025, 12, 31)


def draw_pace_month(rng, pace):
    u = float(rng.random())
    for k, f in enumerate(pace, start=1):
        if u <= f:
            return k
    return len(pace)


def tax_year(d):
    return d.year - (1 if d.month >= 7 else 2)


def rate_at(t):
    return [r for (yy, mm), r in P.CFV_RATES if t_of(yy, mm) <= t][-1]


def build(rng, W):
    hh = W["hh"]
    munis = W["munis"]
    by_prov = {}
    for m in munis:
        by_prov.setdefault(m["prov"], []).append(m)
    kids = [h for h in hh if h["kids"] > 0]
    w = np.array([h["w"] for h in kids])
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

    def new_family(h, entitled_t, cohort, inc):
        fams.append({"fid": len(fams) + 1, "kids": h["kids"], "inc": inc, "muni": place(h),
                     "entitled_t": entitled_t, "cohort": cohort})

    for h in sample(low, n_low):
        new_family(h, 0, "launch", h["assessed"] * float(np.exp(rng.normal(0, 0.04))))
    for h in sample(band, n_band):
        inc = min(P.CFV_LIMIT - 1, max(P.CFV_LIMIT_OLD, h["assessed"] * float(np.exp(rng.normal(0, 0.02)))))
        new_family(h, RISE_T, "widening", inc)
    for t in range(1, LAST_T + 1):
        limit = P.CFV_LIMIT_OLD if t < RISE_T else P.CFV_LIMIT
        n_in = int(rng.poisson(0.0062 * (n_low + (n_band if t >= RISE_T else 0))))
        pool = low if t < RISE_T else low + band
        for h in sample(pool, n_in):
            new_family(h, t, "inflow", min(limit - 1, h["assessed"] * float(np.exp(rng.normal(0, 0.05)))))

    awards = []
    incidents = []
    seq = {}

    def case_no(year):
        seq[year] = seq.get(year, 0) + 1
        return "CFV-%d-%06d" % (year, seq[year])

    def claim_day(t):
        return month_start(t) + dt.timedelta(days=int(rng.integers(0, days_in(t))))

    def decide(claim_date):
        lag = int(np.clip(np.exp(rng.normal(np.log(24.0), 0.50)), 4, 95))
        return claim_date + dt.timedelta(days=lag)

    def tm(d):
        return t_of(d.year, d.month)

    def row(**k):
        base = dict(appeal=False, first=None, last=None, rate=None)
        base.update(k)
        awards.append(base)
        return base

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
            row(ex=case_no(cd.year), fid=f["fid"], tipo="I", claim=cd, dec=None, res="P", ejercicio=tax_year(cd),
                inc=f["inc"], kids=f["kids"], muni=f["muni"])
            continue
        cur = dict(ex=case_no(cd.year), fid=f["fid"], tipo="I", claim=cd, dec=dd, res="C", ejercicio=tax_year(cd),
                   inc=f["inc"], kids=f["kids"], muni=f["muni"], first=tm(dd) + 1)
        inc = f["inc"]
        while True:
            review = cur["first"] + 12
            end_t = None
            for t in range(cur["first"], min(review, LAST_T + 1)):
                if rng.random() < 0.0034:
                    end_t = t
                    break
            if end_t is not None:
                row(**dict(cur, last=end_t, rate=rate_at(cur["first"])))
                break
            if review > LAST_T:
                row(**dict(cur, last=None, rate=rate_at(cur["first"])))
                break
            inc = inc * float(np.exp(rng.normal(0.0, 0.06)))
            limit = P.CFV_LIMIT_OLD if review < RISE_T else P.CFV_LIMIT
            rclaim = month_start(review - 1) + dt.timedelta(days=int(rng.integers(0, 10)))
            rdec = month_start(review) + dt.timedelta(days=int(rng.integers(0, min(25, days_in(review)))))
            rtipo = "T" if rng.random() < 0.012 else "R"
            rcase = case_no(rclaim.year)
            if inc >= limit:
                row(**dict(cur, last=review - 1, rate=rate_at(cur["first"])))
                row(ex=rcase, fid=f["fid"], tipo=rtipo, claim=rclaim, dec=rdec, res="D", ejercicio=tax_year(rclaim),
                    inc=inc, kids=f["kids"], muni=f["muni"])
                break
            suspended = T25A <= review <= T25B and rng.random() < SUSPEND_P
            if suspended:
                incidents.append({"fid": f["fid"], "ex": rcase, "date": month_start(review), "type": "SUS", "dato": ""})
                gap = int(rng.choice([1, 2, 3, 4], p=[0.40, 0.30, 0.18, 0.12]))
                row(**dict(cur, last=review - 1, rate=rate_at(cur["first"])))
                if gap <= 3:
                    lift = month_start(review + gap) + dt.timedelta(days=int(rng.integers(0, 20)))
                    if lift <= YEAR_END:
                        incidents.append({"fid": f["fid"], "ex": rcase, "date": lift, "type": "LEV", "dato": str(gap)})
                    rdec = lift
                else:
                    ext = month_start(review + 3) + dt.timedelta(days=int(rng.integers(0, 15)))
                    if ext <= YEAR_END:
                        incidents.append({"fid": f["fid"], "ex": rcase, "date": ext, "type": "EXT", "dato": ""})
                    row(ex=rcase, fid=f["fid"], tipo=rtipo, claim=rclaim, dec=ext, res="X", ejercicio=tax_year(rclaim),
                        inc=inc, kids=f["kids"], muni=f["muni"])
                    break
            else:
                row(**dict(cur, last=review, rate=rate_at(cur["first"])))
            cur = dict(ex=rcase, fid=f["fid"], tipo=rtipo, claim=rclaim, dec=rdec, res="C", ejercicio=tax_year(rclaim),
                       inc=inc, kids=f["kids"], muni=f["muni"], first=review)
    n_init = sum(1 for a in awards if a["tipo"] == "I")
    for _ in range(int(0.13 * n_init)):
        h = kids[int(rng.choice(above))]
        ct = int(rng.integers(0, LAST_T + 1))
        cd = claim_day(ct)
        dd = decide(cd)
        fams.append({"fid": len(fams) + 1, "kids": h["kids"], "inc": None, "muni": place(h), "entitled_t": None,
                     "cohort": "refused"})
        limit = P.CFV_LIMIT_OLD if ct < RISE_T else P.CFV_LIMIT
        inc = max(limit + 15.0, h["assessed"] * float(np.exp(rng.normal(0.05, 0.05))))
        if dd > P.REGISTER_PULL:
            row(ex=case_no(cd.year), fid=fams[-1]["fid"], tipo="I", claim=cd, dec=None, res="P", ejercicio=tax_year(cd),
                inc=inc, kids=h["kids"], muni=fams[-1]["muni"])
        else:
            row(ex=case_no(cd.year), fid=fams[-1]["fid"], tipo="I", claim=cd, dec=dd, res="D", ejercicio=tax_year(cd),
                inc=inc, kids=h["kids"], muni=fams[-1]["muni"])
    for _ in range(int(0.022 * n_init)):
        h = kids[int(rng.integers(0, len(kids)))]
        ct = int(rng.integers(0, LAST_T - 2))
        cd = claim_day(ct)
        fams.append({"fid": len(fams) + 1, "kids": h["kids"], "inc": None, "muni": place(h), "entitled_t": None,
                     "cohort": "withdrawn"})
        row(ex=case_no(cd.year), fid=fams[-1]["fid"], tipo="I", claim=cd,
            dec=cd + dt.timedelta(days=int(rng.integers(20, 80))), res="A", ejercicio=tax_year(cd), inc=None,
            kids=h["kids"], muni=fams[-1]["muni"])
    # appeals against refusals decided in 2025: a second resolution on the same case number
    for a in list(awards):
        if a["res"] == "D" and a["dec"] is not None and dt.date(2025, 1, 1) <= a["dec"] <= dt.date(2025, 10, 20) \
                and rng.random() < 0.13:
            adec = a["dec"] + dt.timedelta(days=int(rng.integers(32, 72)))
            granted = rng.random() < 0.56
            b = dict(a, dec=adec, res="C" if granted else "D", appeal=True)
            if granted:
                b["first"] = tm(adec) + 1
                b["last"] = None
                b["rate"] = rate_at(b["first"])
                if a["tipo"] == "I" and a.get("inc") is not None:
                    b["inc"] = min(a["inc"], (P.CFV_LIMIT if a["claim"] >= P.CFV_LIMIT_RISE else P.CFV_LIMIT_OLD) - 1)
            awards.append(b)
    # births, eighteenth birthdays and moves among families with a resolution paid in 2025
    open25 = {}
    for a in awards:
        if a["res"] == "C" and a["first"] is not None and a["first"] <= T25B and (a["last"] is None or a["last"] >= T25A):
            open25[a["fid"]] = a
    for fid in sorted(open25):
        a = open25[fid]

        def day():
            return dt.date(2025, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
        if rng.random() < 0.045:
            incidents.append({"fid": fid, "ex": a["ex"], "date": day(), "type": "NAC", "dato": "+1"})
        if rng.random() < 0.055:
            incidents.append({"fid": fid, "ex": a["ex"], "date": day(), "type": "MAY", "dato": "-1"})
        if rng.random() < 0.034:
            prov = a["muni"][:2]
            if rng.random() < 0.30:
                prov = str(rng.choice([p for p, _ in P.PROVINCES if p != prov]))
            ms = by_prov[prov]
            sh = np.array([m["share"] for m in ms])
            new = ms[int(rng.choice(len(ms), p=sh / sh.sum()))]["code"]
            if new != a["muni"]:
                incidents.append({"fid": fid, "ex": a["ex"], "date": day(), "type": "DOM", "dato": new})
    incidents.sort(key=lambda r: (r["date"], r["fid"], r["type"]))
    # a move takes effect from the month after it is recorded; resolutions starting from then carry the new address
    for r in incidents:
        if r["type"] != "DOM":
            continue
        eff = t_of(r["date"].year, r["date"].month) + 1
        for a in awards:
            if a["fid"] == r["fid"] and ((a["first"] is not None and a["first"] >= eff)
                                         or (a["first"] is None and a["claim"] > r["date"])):
                a["muni"] = r["dato"]
    # case numbers run in registration order within each year; an appeal keeps its claim's number
    firsts = [a for a in awards if not a["appeal"]]
    order = sorted(range(len(firsts)), key=lambda i: (firsts[i]["claim"], i))
    new_no, count = {}, {}
    for i in order:
        a = firsts[i]
        y = a["claim"].year
        count[y] = count.get(y, 0) + 1
        new_no[a["ex"]] = "CFV-%d-%06d" % (y, count[y])
    for a in awards:
        a["ex"] = new_no[a["ex"]]
    for r in incidents:
        r["ex"] = new_no[r["ex"]]
    return {"fams": fams, "awards": awards, "incidents": incidents}
