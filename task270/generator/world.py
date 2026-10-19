"""The world behind the pack: Fennacre Mutual's private car book from January 2023 to the September 2026 extract.

Every policy has a garaging district (and so a rating region), a driver age band, a vehicle, a cover and a step on the
no-claims scale. Policy terms renew yearly; a term may end early (a cancellation) and a policy may lapse at renewal,
new business taking its place. Mid-term adjustments move a vehicle to another district, change the vehicle or the
cover. Accidents (the policyholder at fault, split, or not at fault), windscreen damage and thefts happen through
each term. An at-fault or split claim, a theft and a fire move the policy three steps down at the next renewal, so a
claim costs the policyholder the premium difference over the climb back; a policyholder pays at-fault damage below
that cost themselves, and the claim never reaches the record. Step 0 (nothing to lose) and Step Protection (sold at
renewal on steps 6 to 9 from 2024) claim everything.

world(seed) returns the terms, segments, events and claims, and the truth the call is judged against."""
import datetime as dt
import math

import numpy as np

import common as K

SEED = 270203

# ------------------------------------------------------------------------------------------- the regions' worlds
# per region: share of the book, at-fault and split accident rate (per vehicle-year, before the age, step and
# frailty factors), not-at-fault rate, glass rate (comprehensive), theft rate, premium level, and the step mix's mean
REGION = {
    #        share  af      naf     glass   theft   prem   mean step
    "NEC": (0.105, 0.0680, 0.0200, 0.104, 0.0062, 0.93, 3.4),
    "NWE": (0.150, 0.0990, 0.0236, 0.118, 0.0105, 2.15, 2.9),
    "YHU": (0.130, 0.0880, 0.0252, 0.109, 0.0084, 0.98, 1.5),
    "EMI": (0.115, 0.0700, 0.0205, 0.101, 0.0070, 0.95, 4.9),
    "WMI": (0.140, 0.1060, 0.0278, 0.121, 0.0118, 1.30, 4.8),
    "EOE": (0.115, 0.0660, 0.0198, 0.098, 0.0061, 1.02, 5.9),
    "SEA": (0.145, 0.1130, 0.0262, 0.112, 0.0080, 1.05, 8.0),
    "SWW": (0.100, 0.0690, 0.0210, 0.099, 0.0055, 1.05, 7.7),
}
CONC = {"NWE": 30.0, "SEA": 18.0, "YHU": 9.0}       # a region's step mix concentration (default 11)
AGE_SPREAD = {"NWE": 0.4, "SEA": 0.5}                # how far a region's age bands spread its steps (default 1)
AGE_BANDS = ["17-24", "25-34", "35-49", "50-64", "65+"]
AGE_AF = [2.05, 1.25, 0.95, 0.85, 1.05]
AGE_PREM = [2.1, 1.3, 1.0, 0.9, 1.0]
BASE_PREMIUM = 760.0             # pounds before steps, region and age: the book's average risk
SEV_MU, SEV_SIG = math.log(1800.0), 1.00      # cost to the mutual of an accident claim above the excess
PREM_CAP = 2200.0                # the mutual's underwriting limit on a term's premium before steps
THR_LO, THR_HI = 0.70, 1.30      # a policyholder's threshold, times the cost of a claim on their step
PILOT_TAKE = 0.090               # Step Protection take-up at a renewal on steps 6 to 9 (from 2024)
PILOT_SEL = 1.40                 # buyers' frailty tilt: Step Protection holders have more accidents
BOOK = 92000                     # policies in force at the start of 2023
FIRE_RATE = 0.0009               # fires a vehicle-year (both covers)
REPEAT_THEFT = 0.07              # the chance a stolen or broken-into car is targeted again within the term


def cost_of_claim(step, base):
    """The extra premium a claim costs: three steps down at renewal, then one step up a year back to the step."""
    s2 = max(step - K.DROP, 0)
    extra, cur = 0.0, s2
    while cur < step:
        extra += K.REL[cur] - K.REL[step]
        cur += 1
    return extra * base


def mix_of(mean, conc=11.0):
    a = conc * mean / 9.0
    b = conc - a
    def lb(x, y):
        return math.lgamma(x) + math.lgamma(y) - math.lgamma(x + y)
    p = np.array([math.comb(9, k) * math.exp(lb(k + a, 9 - k + b) - lb(a, b)) for k in range(10)])
    return p / p.sum()


def days(a, b):
    return (b - a).days


def add_year(d):
    try:
        return d.replace(year=d.year + 1)
    except ValueError:
        return d.replace(year=d.year + 1, day=28)


# ------------------------------------------------------------------------------------------- the book
class Policy:
    __slots__ = ("pid", "region", "district", "age", "veh_group", "veh_year", "camera", "cover", "step", "frail",
                 "anniv", "start", "legacy_no", "platform_no", "reg", "protected", "prem_noise", "channel")


def district_region(district, day):
    for code, _, ds in K.REGIONS:
        if district in ds:
            base = code
            break
    if district in K.REMAP and day >= K.REMAP_DATE:
        return K.REMAP[district][1]
    return base


REG_LETTERS = "ABCDEFGHJKLMNOPRSTUVWXY"


def registration(rng, year):
    # a current-format plate: two letters, the age identifier, three letters
    age = (year % 100) if rng.random() < 0.5 else (year % 100) + 50
    if age >= 100:
        age -= 50
    return "%s%s%02d %s" % (rng.choice(list(REG_LETTERS)), rng.choice(list(REG_LETTERS)), age,
                            "".join(rng.choice(list(REG_LETTERS), 3)))


def new_policy(rng, pid, start, region=None, fresh=False):
    p = Policy()
    p.pid = pid
    if region is None:
        shares = np.array([REGION[c][0] for c in K.CODES])
        region = K.CODES[rng.choice(8, p=shares / shares.sum())]
    p.region = region
    ds = [r[2] for r in K.REGIONS if r[0] == region][0]
    p.district = ds[rng.integers(len(ds))]
    mean = REGION[region][6]
    # age band, then a step drawn around the region's mean and moved by age (young drivers low on the scale)
    age_p = np.array([0.10, 0.20, 0.30, 0.24, 0.16])
    tilt = (mean - 4.5) / 6.0
    age_p = age_p * np.exp(tilt * np.array([-1.5, -0.6, 0.0, 0.5, 0.9]))
    p.age = int(rng.choice(5, p=age_p / age_p.sum()))
    m = min(max(mean + [-2.8, -1.2, 0.0, 0.8, 1.4][p.age] * AGE_SPREAD.get(region, 1.0), 0.4), 8.6)
    p.step = int(rng.choice(10, p=mix_of(m, CONC.get(region, 11.0))))
    if fresh and rng.random() < 0.35:
        p.step = int(rng.choice(4, p=[0.55, 0.2, 0.15, 0.1]))
    p.frail = rng.gamma(5.0, 0.2)
    p.veh_group = int(rng.integers(5, 45))
    p.veh_year = int(min(start.year, 2026) - rng.choice(np.arange(0, 16), p=_vage()))
    p.camera = p.veh_year >= 2017 and rng.random() < (0.35 + 0.06 * (p.veh_year - 2017))
    p.cover = "TPFT" if rng.random() < [0.42, 0.18, 0.08, 0.06, 0.07][p.age] else "COMP"
    p.anniv = start
    p.start = start
    p.legacy_no = None
    p.platform_no = None
    p.reg = registration(rng, p.veh_year)
    p.protected = False
    p.prem_noise = rng.lognormal(0.0, 0.18)
    p.channel = rng.choice(["Direct web", "Direct phone", "Broker"], p=[0.58, 0.17, 0.25])
    return p


_VAGE = None


def _vage():
    global _VAGE
    if _VAGE is None:
        w = np.array([0.04, 0.07, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.03, 0.03])
        _VAGE = w / w.sum()
    return _VAGE


def base_premium(p):
    return min(PREM_CAP, BASE_PREMIUM * REGION[p.region][5] * AGE_PREM[p.age] * (0.75 + p.veh_group / 60.0)
               * p.prem_noise)


# ------------------------------------------------------------------------------------------- simulation
def world(seed=SEED):
    rng = np.random.default_rng([seed, 1])
    erng = np.random.default_rng([seed, 2])       # events
    grng = np.random.default_rng([seed, 3])       # glass and theft
    pid = 0
    pols = []
    # the book on 1 January 2023: anniversaries spread over 2022, so every term in force then is found
    for _ in range(BOOK):
        anniv = dt.date(2022, 1, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
        p = new_policy(rng, pid, anniv)
        pols.append(p)
        pid += 1
    terms, segs, events = [], [], []
    queue = list(pols)
    lapse = 0.105
    nb_rate = None
    while queue:
        p = queue.pop()
        t0 = p.anniv
        while t0 <= K.EXTRACT:
            t1 = add_year(t0) - dt.timedelta(days=1)
            base = base_premium(p)
            # Step Protection at renewal (from 2024) on steps 6 to 9, adversely selected on frailty
            if t0 >= K.PILOT_START and p.step in K.PILOT_STEPS:
                if p.protected:
                    p.protected = rng.random() < 0.86
                else:
                    pr = PILOT_TAKE * min(3.0, (p.frail / 1.0) ** 1.6)
                    p.protected = rng.random() < pr
            elif p.step not in K.PILOT_STEPS:
                p.protected = False
            cancelled = None
            if rng.random() < 0.035:
                cancelled = t0 + dt.timedelta(days=int(rng.integers(20, 360)))
                if cancelled > t1:
                    cancelled = None
            end = min(cancelled or t1, t1)
            thr_u = rng.uniform(K_LO(), K_HI())
            term = dict(pid=p.pid, start=t0, end=t1, cancelled=cancelled, step=p.step, protected=p.protected,
                        cover=p.cover, age=p.age, veh_group=p.veh_group, veh_year=p.veh_year, camera=p.camera,
                        reg=p.reg, district=p.district, base=base, thr=cost_of_claim(p.step, base) * thr_u,
                        channel=p.channel, frail=p.frail, mtas=[])
            # mid-term adjustments: a move (district), a vehicle change, a cover change
            cur_d, cur_cover = p.district, p.cover
            mta_days = []
            if rng.random() < 0.028:
                mta_days.append(("ADDR", t0 + dt.timedelta(days=int(rng.integers(15, 350)))))
            if rng.random() < 0.075:
                mta_days.append(("VEH", t0 + dt.timedelta(days=int(rng.integers(15, 350)))))
            if rng.random() < 0.012:
                mta_days.append(("COVER", t0 + dt.timedelta(days=int(rng.integers(15, 350)))))
            mta_days.sort(key=lambda x: x[1])
            bounds = [t0]
            states = [(cur_d, cur_cover)]
            for kind, d in mta_days:
                if d > end:
                    continue
                if kind == "ADDR":
                    if rng.random() < 0.6:
                        same = [r[2] for r in K.REGIONS if r[0] == district_region(cur_d, d) or cur_d in r[2]][0]
                        nd = same[rng.integers(len(same))]
                    else:
                        reg = K.CODES[rng.integers(8)]
                        ds = [r[2] for r in K.REGIONS if r[0] == reg][0]
                        nd = ds[rng.integers(len(ds))]
                    if nd == cur_d:
                        continue
                    cur_d = nd
                    term["mtas"].append(dict(kind="Change of address", day=d, district=nd, cover=cur_cover))
                elif kind == "COVER":
                    cur_cover = "TPFT" if cur_cover == "COMP" else "COMP"
                    term["mtas"].append(dict(kind="Change of cover", day=d, district=cur_d, cover=cur_cover))
                else:
                    term["mtas"].append(dict(kind="Change of vehicle", day=d, district=cur_d, cover=cur_cover))
                    continue
                bounds.append(d)
                states.append((cur_d, cur_cover))
            bounds.append(end + dt.timedelta(days=1))
            term["segments"] = []
            for i in range(len(states)):
                a, b = bounds[i], bounds[i + 1]
                if days(a, b) <= 0:
                    continue
                term["segments"].append((a, b, states[i][0], states[i][1]))
            p.district, p.cover = cur_d, cur_cover
            terms.append(term)
            # events through the term
            made_fault = 0
            for (a, b, dist, cover) in term["segments"]:
                for y in (a.year, b.year):
                    pass
                span = days(a, b)
                # region on the day changes only at the remap for S40 and MK40: split the segment there
                cuts = [a]
                if dist in K.REMAP and a < K.REMAP_DATE < b:
                    cuts.append(K.REMAP_DATE)
                cuts.append(b)
                for j in range(len(cuts) - 1):
                    s0, s1 = cuts[j], cuts[j + 1]
                    nd = days(s0, s1)
                    reg = district_region(dist, s0)
                    segs.append(dict(pid=p.pid, term=len(terms) - 1, a=s0, b=s1, region=reg, district=dist,
                                     cover=cover, step=term["step"], protected=term["protected"]))
                    lam = REGION[reg][1] * AGE_AF[p.age] * p.frail * (1.20 - 0.04 * term["step"])
                    n_af = erng.poisson(lam * nd / 365.0)
                    n_naf = erng.poisson(REGION[reg][2] * nd / 365.0)
                    for kind, n in (("AF", n_af), ("NAF", n_naf)):
                        for _ in range(n):
                            day = s0 + dt.timedelta(days=int(erng.integers(0, nd)))
                            cost = float(np.exp(SEV_MU + SEV_SIG * erng.standard_normal()))
                            split = kind == "AF" and erng.random() < 0.16
                            claimed = True
                            if kind == "AF" and not (term["step"] == 0 or term["protected"]):
                                claimed = cost > term["thr"]
                            events.append(dict(pid=p.pid, term=len(terms) - 1, kind=kind, split=split, day=day,
                                               region=reg, district=dist, cost=cost, claimed=claimed,
                                               step=term["step"], protected=term["protected"], cover=cover))
                            if claimed and kind == "AF":
                                made_fault += 1
                    if cover == "COMP":
                        for _ in range(grng.poisson(REGION[reg][3] * nd / 365.0)):
                            day = s0 + dt.timedelta(days=int(grng.integers(0, nd)))
                            events.append(dict(pid=p.pid, term=len(terms) - 1, kind="GLASS", day=day, region=reg,
                                               district=dist, camera=term["camera"], veh_group=term["veh_group"],
                                               cover=cover))
                    else:
                        # third party, fire and theft: the partner fits the screen and recharges the customer
                        for _ in range(grng.poisson(0.55 * REGION[reg][3] * nd / 365.0)):
                            day = s0 + dt.timedelta(days=int(grng.integers(0, nd)))
                            events.append(dict(pid=p.pid, term=len(terms) - 1, kind="GLASS_TPFT", day=day,
                                               region=reg, district=dist, camera=term["camera"],
                                               veh_group=term["veh_group"], cover=cover))
                    vf = 1.0 + 0.8 * (p.veh_group > 30)
                    for _ in range(grng.poisson(REGION[reg][4] * vf * nd / 365.0)):
                        day = s0 + dt.timedelta(days=int(grng.integers(0, nd)))
                        events.append(dict(pid=p.pid, term=len(terms) - 1, kind="THEFT", day=day, region=reg,
                                           district=dist, veh_group=term["veh_group"]))
                        made_fault += 1
                        # a car taken once is taken again more often than chance (keyless entry, a known address)
                        if grng.random() < REPEAT_THEFT:
                            again = day + dt.timedelta(days=int(grng.integers(20, 200)))
                            if again < s1:
                                events.append(dict(pid=p.pid, term=len(terms) - 1, kind="THEFT", day=again,
                                                   region=reg, district=dist, veh_group=term["veh_group"]))
                                made_fault += 1
                    for _ in range(grng.poisson(FIRE_RATE * nd / 365.0)):
                        day = s0 + dt.timedelta(days=int(grng.integers(0, nd)))
                        events.append(dict(pid=p.pid, term=len(terms) - 1, kind="FIRE", day=day, region=reg,
                                           district=dist, veh_group=term["veh_group"]))
                        made_fault += 1
            # renewal
            if cancelled is not None or rng.random() < lapse:
                # the policy ends; new business replaces it in the same region
                if t1 < K.EXTRACT:
                    nb_start = (cancelled or t1) + dt.timedelta(days=int(rng.integers(1, 60)))
                    if nb_start <= K.EXTRACT:
                        q = new_policy(rng, pid, nb_start, region=p.region, fresh=True)
                        pid += 1
                        queue.append(q)
                break
            if term["protected"] and made_fault:
                pass
            elif made_fault:
                p.step = max(0, p.step - K.DROP * made_fault)
            else:
                p.step = min(9, p.step + 1)
            if rng.random() < 0.06:
                p.veh_year = min(t1.year, p.veh_year + int(rng.integers(2, 8)))
                p.camera = p.veh_year >= 2017 and rng.random() < (0.35 + 0.06 * (p.veh_year - 2017))
                p.reg = registration(rng, p.veh_year)
            p.anniv = t1 + dt.timedelta(days=1)
            t0 = p.anniv
    return dict(terms=terms, segs=segs, events=events, n_policies=pid)


def K_LO():
    return THR_LO


def K_HI():
    return THR_HI


# ------------------------------------------------------------------------------------------- the truth
def exposure(segs, years=K.ACC_YEARS, cover=None):
    """Vehicle-years by region within the accident years (days over 365), optionally one cover only."""
    out = {c: 0.0 for c in K.CODES}
    for s in segs:
        if cover and s["cover"] != cover:
            continue
        for y in years:
            a = max(s["a"], dt.date(y, 1, 1))
            b = min(s["b"], dt.date(y + 1, 1, 1))
            if b > a:
                out[s["region"]] += days(a, b) / 365.0
    return out


def costs_mutual(e):
    """An accident the mutual pays for: at fault or split on any cover; not at fault on comprehensive (the
    other driver's insurer pays a third party, fire and theft policyholder direct, the mutual records a nil
    notification)."""
    return e["kind"] == "AF" or (e["kind"] == "NAF" and e["cover"] == "COMP")


def truth(w):
    E = exposure(w["segs"])
    acc = {c: 0 for c in K.CODES}
    rep = {c: 0 for c in K.CODES}
    for e in w["events"]:
        if e["kind"] in ("AF", "NAF") and e["day"].year in K.ACC_YEARS and costs_mutual(e):
            acc[e["region"]] += 1
            if e["claimed"]:
                rep[e["region"]] += 1
    return dict(exposure=E, protected={c: 100.0 * acc[c] / E[c] for c in K.CODES},
                reported={c: 100.0 * rep[c] / E[c] for c in K.CODES}, accidents=acc, claims=rep)


if __name__ == "__main__":
    import sys
    import time
    t = time.time()
    w = world(int(sys.argv[1]) if len(sys.argv) > 1 else SEED)
    tr = truth(w)
    print("policies", w["n_policies"], "terms", len(w["terms"]), "segments", len(w["segs"]), "events",
          len(w["events"]), "%.0fs" % (time.time() - t))
    for c in K.CODES:
        print(c, round(tr["exposure"][c]), round(tr["protected"][c], 2), round(tr["reported"][c], 2),
              round(1 - tr["reported"][c] / tr["protected"][c], 3))
    order = sorted(K.CODES, key=lambda c: -tr["protected"][c])
    print("protected order", order)
    print("reported order ", sorted(K.CODES, key=lambda c: -tr["reported"][c]))
