"""Simulate the members, eligibility, prices and claims behind the pack.

Every claim line is generated from the behaviour in world.py: a referral goes to the owner's sites
after a purchase only where the member's product places the owner at the preferred tier (or has no
tiers), at the capture rate, and destinations are assigned by quota so shares are stable over any
window of months.
"""
import hashlib
import math
import random
from collections import defaultdict
from datetime import date, timedelta

import orgs as O
import world as W

D = date


def h01(*parts):
    """A deterministic number in [0, 1) from the parts."""
    x = int(hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:13], 16)
    return x / float(16 ** 13)


# ------------------------------------------------------------------ prices
YEAR_FACTOR = {2021: 0.931, 2022: 0.957, 2023: 0.979, 2024: 1.000}
MEDICARE = {  # CY2025 Medicare amounts referenced by percent-of-Medicare agreements (OPPS for
    # outpatient services, CLFS for laboratory tests), Wisconsin wage-adjusted
    "70551": 254.37, "72148": 254.37, "73721": 254.37, "74177": 381.62, "71250": 123.48,
    "71046": 64.92, "73562": 64.92, "76700": 123.48, "77067": 98.71, "93306": 520.15,
    "45378": 1078.94, "45380": 1078.94, "43239": 942.37, "29881": 3186.40,
    "80053": 10.56, "85025": 7.77, "80061": 13.39, "83036": 9.71, "84443": 16.80,
    "82947": 3.93, "87086": 8.20,
}


def fac_idio(fkey, cpt):
    return 0.96 + 0.08 * h01("idio", fkey, cpt)


def facility_rate(fkey, carrier, cpt, year=2024):
    """Allowed amount per unit at a facility outside Ledgestone (other systems and independents)."""
    fam = W.CPT[cpt][1]
    sysk = W.FAC[fkey][2]
    base = W.CPT[cpt][2]
    mult = W.SITE_MULT[sysk].get(fam, 1.0)
    r = round(base * mult * W.CARRIER_FACTOR[carrier] * fac_idio(fkey, cpt), 2)
    return round(r * YEAR_FACTOR[min(year, 2024)], 2)


def ldg_facility_rate(carrier, cpt, year=2025):
    """Ledgestone's agreed rate, one chargemaster for its three outpatient sites. From 2025 the
    Bayfield agreement prices outpatient services as a percent of the Medicare amount."""
    fam = W.CPT[cpt][1]
    if year >= 2025 and carrier == "C2":
        return round(MEDICARE[cpt] * W.LDG_C2_PCT_2025[fam], 2)
    base = W.CPT[cpt][2]
    r = round(base * W.SITE_MULT["LDG"][fam] * W.CARRIER_FACTOR[carrier] * W.LDG_RATE_TWEAK.get(cpt, 1.0), 2)
    return r if year >= 2024 else round(r * YEAR_FACTOR[year], 2)


def rate(fkey, carrier, cpt, year=2024):
    if W.FAC[fkey][2] == "LDG":
        return ldg_facility_rate(carrier, cpt, year)
    return facility_rate(fkey, carrier, cpt, year)


def bmg_prof_rate(carrier, code):
    base = W.PROF[code][1]
    return round(base * W.CARRIER_FACTOR[carrier] * (0.985 + 0.03 * h01("bmgp", carrier, code)), 2)


def ldg_prof_rate(carrier, code):
    return round(bmg_prof_rate(carrier, code) * W.LDG_PROF_UPLIFT[carrier] * (0.99 + 0.02 * h01("ldgp", carrier, code)), 2)


def other_prof_rate(practice, carrier, code, year=2024):
    base = W.PROF[code][1]
    lvl = {"LMG": 1.21, "KPN": 1.16, "WRMG": 1.17}.get(practice, 0.97 + 0.08 * h01("op", practice))
    r = base * W.CARRIER_FACTOR[carrier] * lvl * (0.985 + 0.03 * h01("opr", practice, carrier, code))
    return round(r * YEAR_FACTOR[min(year, 2024)], 2)


# ------------------------------------------------------------------ members and eligibility
UNTIERED = [p for p, v in W.PRODUCTS.items() if not v[3]]


# residence ZIP weights for the two lakeshore counties (Manitowoc about three quarters)
LAKE_ZIP_WEIGHTS = {"54220": .32, "54241": .15, "54228": .07, "53042": .10, "54230": .10,
                    "54216": .10, "54201": .08, "54217": .08}


def weighted_pick(weights, u):
    keys = sorted(weights)
    tot = sum(weights[k] for k in keys)
    acc = 0.0
    for k in keys:
        acc += weights[k] / tot
        if u < acc:
            return k
    return keys[-1]


class Members:
    def __init__(self):
        self.by_pool = defaultdict(list)
        self.info = {}          # member -> dict(zips, birth, sex, spans, pool, renew, group)

    @staticmethod
    def new_id(pool, i):
        return "WM" + hashlib.sha256(("m|%s|%d" % (pool, i)).encode()).hexdigest()[:10].upper()

    def add_pool(self, pool, n, mix, zips, years, switch_rate=0.04, switch_before=None, mover_rate=0.0):
        """n members on the product mix. A member may move to another product at an employer
        renewal; moves happen only between products with no tiers, so a member's tier for any
        system never changes on a move. zips is a list (uniform) or a dict of weights. A share of
        the pool changes address once during the last year (mover_rate)."""
        prods = sorted(mix)
        cum, acc = [], 0.0
        for p in prods:
            acc += mix[p]
            cum.append(acc)
        for i in range(n):
            mid = self.new_id(pool, i)
            u = h01("prod", pool, i) * acc
            prod = prods[next(k for k, c in enumerate(cum) if u < c)]
            if isinstance(zips, dict):
                zp = weighted_pick(zips, h01("zip", pool, i))
            else:
                zp = zips[int(h01("zip", pool, i) * len(zips))]
            birth = 1961 + int(h01("birth", pool, i) * 46)
            sex = "F" if h01("sex", pool, i) < 0.53 else "M"
            renew = 7 if h01("renew", pool, i) < 0.28 else 1
            start, end = D(years[0], 1, 1), D(years[1], 12, 31)
            spans = [(prod, start, end)]
            if prod in UNTIERED and h01("sw", pool, i) < switch_rate:
                last = (switch_before or years[1] + 1) - 1
                yrs = list(range(years[0], last + 1))
                swyr = yrs[int(h01("swy", pool, i) * len(yrs))]
                cut = D(swyr, renew, 1)
                if start < cut <= end:
                    alt = [p for p in UNTIERED if p != prod]
                    p2 = alt[int(h01("swp", pool, i) * len(alt))]
                    spans = [(prod, start, cut - timedelta(days=1)), (p2, cut, end)]
            zl = [(zp, start, end)]
            if mover_rate and h01("mv", pool, i) < mover_rate:
                mvd = D(years[1], 2 + int(h01("mvm", pool, i) * 10), 1)
                county = W.ZIP_COUNTY[zp]
                if county == "Kewaunee":
                    dest = ["54220", "54241", "54311"]
                else:
                    dest = ["54216", "54217", "54201", "54304"]
                nz = dest[int(h01("mvz", pool, i) * len(dest))]
                zl = [(zp, start, mvd - timedelta(days=1)), (nz, mvd, end)]
            group = None
            # two self-funded employer groups on Lakefront's network PPO: Kewaunee County schools and the
            # City of Two Rivers
            if pool == "LKO" and prod == "LBA-PPO7":
                if W.ZIP_COUNTY[zp] == "Kewaunee":
                    group = "KCSD"
                elif zp == "54241":
                    group = "TRWC"
            self.info[mid] = {"zips": zl, "birth": birth, "sex": sex, "spans": spans, "pool": pool,
                              "renew": renew, "group": group}
            self.by_pool[pool].append(mid)

    def product_on(self, mid, d):
        for p, s, e in self.info[mid]["spans"]:
            if s <= d <= e:
                return p
        return None

    def zip_on(self, mid, d):
        for z, s, e in self.info[mid]["zips"]:
            if s <= d <= e:
                return z
        return None

    def plan_year(self, mid, d):
        return W.plan_year_of(d, self.info[mid]["renew"])


# ------------------------------------------------------------------ claims
def months(y0, y1):
    return [(y, m) for y in range(y0, y1 + 1) for m in range(1, 13)]


def day_in(y, m, frac):
    nd = (D(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)).day
    d = D(y, m, 1 + int(frac * nd) % nd)
    # outpatient services and office visits run Monday to Friday
    while d.weekday() >= 5:
        d = d - timedelta(days=d.weekday() - 4)
    return d


REF_MIX = {
    "FM": {"80053": 70, "85025": 64, "80061": 56, "83036": 40, "84443": 46, "71046": 18, "76700": 9,
           "77067": 28, "70551": 4, "72148": 7, "74177": 5, "71250": 3, "93306": 3, "95810": 3, "78452": 2},
    "IM": {"80053": 82, "85025": 70, "80061": 60, "83036": 52, "84443": 50, "71046": 20, "76700": 12,
           "70551": 6, "72148": 6, "74177": 7, "71250": 5, "93306": 8, "95810": 4, "78452": 4},
    "PED": {"85025": 40, "80053": 12, "71046": 10, "84443": 8},
    "GI": {"45378": 105, "45380": 150, "43239": 165, "80053": 30, "85025": 30, "74177": 16, "76700": 15},
    "ORTH": {"73721": 58, "72148": 30, "73562": 140, "29881": 66, "80053": 6, "85025": 5},
    "CARD": {"93306": 175, "78452": 58, "80061": 50, "80053": 40, "85025": 30, "71250": 10},
}
REF_MIX["NP"] = {k: v * 0.55 for k, v in REF_MIX["FM"].items()}
REF_MIX["PA"] = REF_MIX["NP"]
PROF_MIX = {
    "FM": {"99213": 450, "99214": 400, "99212": 90, "99215": 70, "99203": 40, "99204": 40, "99396": 85,
           "99395": 55, "99386": 22, "99385": 14, "36415": 90, "96372": 45, "93000": 30, "69210": 14, "11102": 8},
    "IM": {"99213": 360, "99214": 470, "99215": 120, "99212": 40, "99204": 40, "99203": 20, "99396": 70,
           "99386": 24, "36415": 110, "93000": 55, "96372": 40},
    "GI": {"99243": 120, "99244": 90, "99213": 140, "99214": 150, "45378-P": 105, "45380-P": 150, "43239-P": 165},
    "ORTH": {"99203": 80, "99204": 75, "99213": 220, "99214": 160, "99212": 90, "20610": 240, "29881-P": 66},
    "CARD": {"99214": 290, "99215": 130, "99204": 70, "99203": 30, "93000": 260, "93306-26": 175},
    "PED": {"99213": 400, "99214": 180, "99212": 120},
}
PROF_MIX["NP"] = {k: v * 0.6 for k, v in PROF_MIX["FM"].items()}
PROF_MIX["PA"] = PROF_MIX["NP"]

# where referrals go when they do not go to the referring group's owner, by region and service family
OUTSIDE = {
    "lakeshore": {"IMG": [("KLH", .35), ("MOI", .57), ("LMN", .08)], "ECHO": [("KLH", .62), ("CIC", .30), ("LMN", .08)],
                  "ENDO": [("KLH", .30), ("TRE", .62), ("LMN", .08)], "ARTH": [("KLH", .27), ("MOS", .65), ("LMN", .08)],
                  "LAB": [("NCL", .66), ("KLH", .26), ("LMN", .08)], "SLEEP": [("MSD", 1.0)],
                  "NUC": [("KLH", .80), ("CIC", .20)]},
    "sheboygan": {"IMG": [("KSM", .45), ("EDI", .55)], "ECHO": [("KSM", .85), ("CIC", .15)],
                  "ENDO": [("KSM", .55), ("TRE", .45)], "ARTH": [("KSM", .50), ("MOS", .50)],
                  "LAB": [("NCL", .60), ("KSM", .40)], "SLEEP": [("MSD", 1.0)], "NUC": [("KSM", .70), ("CIC", .30)]},
    "kewaunee": {"IMG": [("MOI", .34), ("KLH", .28), ("FCI", .24), ("LMN", .06), ("LMC", .08)],
                 "ECHO": [("CIC", .42), ("KLH", .44), ("LMC", .14)], "ENDO": [("TRE", .38), ("BAE", .30), ("KLH", .18), ("LMC", .14)],
                 "ARTH": [("MOS", .40), ("TSC", .32), ("KLH", .16), ("LMC", .12)],
                 "LAB": [("NCL", .70), ("KLH", .20), ("LMC", .10)], "SLEEP": [("GBS", .50), ("MSD", .50)],
                 "NUC": [("CIC", .60), ("KLH", .40)]},
    "metro": {"IMG": [("FCI", .52), ("WRO", .10), ("OIA", .22), ("LMC", .08), ("EDI", .08)],
              "ECHO": [("CIC", .70), ("WRO", .22), ("LMC", .08)], "ENDO": [("BAE", .74), ("WRO", .18), ("LMC", .08)],
              "ARTH": [("TSC", .78), ("WRO", .14), ("LFC", .08)], "LAB": [("NCL", .84), ("WRO", .08), ("LMC", .08)],
              "SLEEP": [("GBS", 1.0)], "NUC": [("CIC", .75), ("WRO", .25)]},
    "oshkosh": {"IMG": [("OIA", .62), ("FCI", .22), ("LFC", .08), ("WRO", .08)],
                "ECHO": [("OHL", .76), ("LFC", .16), ("WRO", .08)], "ENDO": [("BAE", .50), ("LFC", .42), ("WRF", .08)],
                "ARTH": [("TSC", .66), ("LFC", .26), ("WRO", .08)], "LAB": [("NCL", .84), ("LFC", .08), ("WRO", .08)],
                "SLEEP": [("GBS", 1.0)], "NUC": [("OHL", 1.0)]},
}
T2_WEIGHT = 0.25        # cost sharing pulls a patient away from a second-tier facility


HISTORY_PRACTICES = ("P1", "P2", "P3", "P4", "P5", "W1", "W2")


class Quota:
    """Assigns a stream of items to 'owner' with a target share, spread evenly in time order."""

    def __init__(self):
        self.count = defaultdict(int)
        self.hits = defaultdict(int)

    def take(self, key, share, offset=0.0):
        i = self.count[key]
        self.count[key] += 1
        want = math.floor((i + 1) * share + offset) - math.floor(i * share + offset)
        if want > 0:
            self.hits[key] += 1
            return True
        return False


def site_offers(fkey, cpt):
    return cpt in W.FAC[fkey][6]


def acquirer_offers(sysk, cpt):
    return any(f[2] == sysk and cpt in f[6] for f in W.FACILITIES)


def fac_tier(fkey, product, plan_year):
    sysk = W.FAC[fkey][2]
    return 1 if sysk is None else W.tier_for(product, sysk, plan_year)


def choose_outside(region, fam, cpt, product, plan_year, exclude_sys, u):
    opts = [(f, s) for f, s in OUTSIDE[region][fam]
            if (exclude_sys is None or W.FAC[f][2] != exclude_sys) and site_offers(f, cpt)]
    if not opts:   # nothing local outside the owner: the nearest independent offering the service
        opts = [(f[0], 1.0) for f in W.FACILITIES if f[2] is None and cpt in f[6]][:1]
    wts = [(f, s * (T2_WEIGHT if fac_tier(f, product, plan_year) == 2 else 1.0)) for f, s in opts]
    tot = sum(w for _, w in wts)
    acc = 0.0
    for f, w in wts:
        acc += w / tot
        if u < acc:
            return f
    return wts[-1][0]


# ------------------------------------------------------------------ the simulation
T2_TARGET = {"P1": 0.62, "P2": 0.45, "P3": 0.55, "P4": 0.58, "P5": 0.48, "W1": 0.40, "W2": 0.34}
REF_VOLUME = {"BMG": 1.33, "P1": 1.0, "P2": 1.0, "P3": 1.0, "P4": 1.0, "P5": 1.0, "W1": 1.0, "W2": 1.0, "LMG": 0.70,
              "MFP": 0.9, "KPN": 0.85, "RRF": 0.9, "AFH": 0.85, "KAC": 0.85, "MDC": 0.9, "SOA": 0.9}
OWN_SITE = {"P1": "LFC", "P2": "LMC", "P3": "LMC", "P4": "LMC", "P5": "LFC", "W1": "WRO", "W2": "WRF", "LMG": "LMC",
            "MFP": "LMN", "BMG": "LMN"}
LAKESHORE_INDEP = ("RRF", "AFH", "KAC", "MDC", "SOA")
# extra referrals by county and line: (to other sites, to Ledgestone)
TOPUP = {("Kewaunee", "ARTH"): (3, 0), ("Kewaunee", "ENDO"): (0, 1), ("Kewaunee", "IMG"): (1, 0),
         ("Manitowoc", "ARTH"): (3, 0)}
TOPUP_SOURCE = {("Kewaunee", "ARTH"): ("SOA", ["29881"], "MOS", "LMC"),
                ("Kewaunee", "ENDO"): ("AFH", ["45378"], "BAE", "LMC"),
                ("Kewaunee", "IMG"): ("KAC", ["76700"], "FCI", "LMC"),
                ("Manitowoc", "ARTH"): ("SOA", ["29881"], "MOS", "LMN")}


def mix_with_t2(base_mix, sysk, t2_target, plan_year=2021):
    t2 = {p: w for p, w in base_mix.items() if W.tier_for(p, sysk, plan_year) == 2}
    t1 = {p: w for p, w in base_mix.items() if W.tier_for(p, sysk, plan_year) == 1}
    s2, s1 = sum(t2.values()), sum(t1.values())
    out = {p: w / s2 * t2_target for p, w in t2.items()}
    out.update({p: w / s1 * (1 - t2_target) for p, w in t1.items()})
    return out


def simulate():
    people, assign, roster = O.make_people()
    mem = Members()
    lake_zips = W.ZIPS["Manitowoc"] + W.ZIPS["Kewaunee"]
    metro_zips = W.ZIPS["Brown"] + W.ZIPS["Outagamie"]
    osh_zips = W.ZIPS["Winnebago"] + W.ZIPS["Fond du Lac"]
    mem.add_pool("BMG", 9000, W.MIX_BRIGHTWATER, LAKE_ZIP_WEIGHTS, (2023, 2024), switch_before=2024)
    for p in ("P1", "P2", "P4", "P5"):
        mem.add_pool(p, 1900, mix_with_t2(W.MIX_METRO, "LDG", T2_TARGET[p]), metro_zips, (2021, 2024))
    mem.add_pool("P3", 1500, mix_with_t2(W.MIX_METRO, "LDG", T2_TARGET["P3"]), metro_zips, (2021, 2024))
    for p in ("W1", "W2"):
        mem.add_pool(p, 1700, mix_with_t2(W.MIX_OSHKOSH, "WRH", T2_TARGET[p]), osh_zips, (2021, 2024))
    mem.add_pool("LMG", 6400, W.MIX_METRO, metro_zips, (2024, 2024))
    mem.add_pool("LKO", 9800, W.MIX_LAKESHORE_OTHER, LAKE_ZIP_WEIGHTS, (2024, 2024), mover_rate=0.04)
    mem.add_pool("OTM", 3200, W.MIX_METRO, metro_zips + W.ZIPS["Calumet"], (2024, 2024))
    mem.add_pool("OTO", 2600, W.MIX_OSHKOSH, osh_zips, (2024, 2024))
    mem.add_pool("OTS", 3000, W.MIX_LAKESHORE_OTHER, W.ZIPS["Sheboygan"], (2024, 2024))

    quota = Quota()
    lines = []

    subsets = {}

    def draw_member(pool, key):
        if ":" in pool:   # pool restricted to residents of one county on 1 January
            if pool not in subsets:
                base, county = pool.split(":")
                subsets[pool] = [m for m in mem.by_pool[base]
                                 if W.ZIP_COUNTY[mem.info[m]["zips"][0][0]] == county]
            ids = subsets[pool]
        else:
            ids = mem.by_pool[pool]
        return ids[int(h01("mem", key) * len(ids))]

    def referrals(practice, npi, spec, years, pool, owner, event, volume, tag, own_site, region, phase=None):
        """phase None: before/after the event date; 'steady': an owned group; 'pre': not yet bought."""
        mix = REF_MIX[spec]
        for (y, m) in months(*years):
            for cpt, per_year in mix.items():
                lam = per_year * volume / 12.0
                n = int(lam) + (1 if h01("cnt", npi, cpt, y, m) < lam - int(lam) else 0)
                for k in range(n):
                    d = day_in(y, m, h01("day", npi, cpt, y, m, k))
                    mid = draw_member(pool, (npi, cpt, y, m, k))
                    prod = mem.product_on(mid, d)
                    if prod is None:
                        continue
                    py = mem.plan_year(mid, d)
                    fam = W.CPT[cpt][1]
                    dest = None
                    if owner is not None and own_site and site_offers(own_site, cpt):
                        t = W.tier_for(prod, owner, py)
                        if phase == "steady":
                            s0, ph = W.STEADY, "steady"
                            share = s0 + W.CAPTURE * (1 - s0) if t == 1 else s0
                        elif phase == "pre" or (event is not None and d < event):
                            s0, ph = W.PRE_SHARE[practice], "pre"
                            share = s0
                        else:
                            s0, ph = W.PRE_SHARE[practice], "post"
                            share = s0 + W.CAPTURE * (1 - s0) if t == 1 else s0
                        qkey = (practice, ph, t, fam)
                        if practice in HISTORY_PRACTICES:
                            # the acquired practices' shares hold product by product as well
                            qkey = qkey + (prod,)
                        if quota.take(qkey, share, offset=h01("off", qkey)):
                            dest = own_site
                    if dest is None:
                        dest = choose_outside(region, fam, cpt, prod, py, owner,
                                              h01("dest", npi, cpt, y, m, k))
                    lines.append(dict(kind="fac", tag=tag, practice=practice, member=mid, product=prod,
                                      carrier=W.PRODUCTS[prod][0], date=d, cpt=cpt, fac=dest, ref_npi=npi,
                                      units=1, event=event))

    # Brightwater's 2024 referrals: the baseline
    for npi in roster["BMG"]:
        referrals("BMG", npi, people[npi]["spec"], (2024, 2024), "BMG", "LDG", None, REF_VOLUME["BMG"],
                  "bmg_ref", "LMN", "lakeshore", phase="pre")
    # the earlier purchases, 2021-2024
    for p in ("P1", "P2", "P4", "P5", "W1", "W2"):
        owner = O.ACQUIRER[p]
        region = "oshkosh" if owner == "WRH" else "metro"
        for npi in roster[p]:
            referrals(p, npi, people[npi]["spec"], (2021, 2024), p, owner, O.EVENT_DATE[p], REF_VOLUME[p],
                      "hist_ref", OWN_SITE[p], region)
    # Northpoint Orthopedics: its orthopedists were reassigned to Ledgestone Medical Group one at a time
    for npi in roster["P3"]:
        mv = [a[2] for a in assign if a[0] == npi and a[1] == "LMG"][0]
        referrals("P3", npi, "ORTH", (2021, 2024), "P3", "LDG", mv, REF_VOLUME["P3"], "hist_ref",
                  OWN_SITE["P3"], "metro")
    # Ledgestone Medical Group's other physicians in 2024 (long-standing staff and later hires)
    on_2024 = [a[0] for a in assign if a[1] == "LMG" and a[2] <= D(2024, 1, 1)
               and (a[3] is None or a[3] >= D(2024, 12, 31))]
    lmg_now = sorted(set(on_2024) - set(roster["P1"]) - set(roster["P3"]) - set(roster["P4"]))
    for npi in lmg_now:
        referrals("LMG", npi, people[npi]["spec"], (2024, 2024), "LMG", "LDG", None, REF_VOLUME["LMG"],
                  "lmg_ref", "LMC", "metro", phase="steady")
    # the lakeshore groups, 2024
    for npi in roster["MFP"]:
        referrals("MFP", npi, people[npi]["spec"], (2024, 2024), "LKO:Manitowoc", "LDG", None, REF_VOLUME["MFP"],
                  "lake_ref", "LMN", "lakeshore", phase="steady")
    for i, npi in enumerate(roster["KPN"]):
        shb = i >= 13
        referrals("KPN", npi, people[npi]["spec"], (2024, 2024), "OTS" if shb else "LKO:Manitowoc", "KNK", None,
                  REF_VOLUME["KPN"], "lake_ref", "KSM" if shb else "KLH", "sheboygan" if shb else "lakeshore",
                  phase="steady")
    for p in LAKESHORE_INDEP:
        kew = p in ("KAC", "AFH")
        for npi in roster[p]:
            referrals(p, npi, people[npi]["spec"], (2024, 2024), "LKO:Kewaunee" if kew else "LKO:Manitowoc",
                      None, None, REF_VOLUME[p], "lake_ref", None, "kewaunee" if kew else "lakeshore")
    # other referrers in the region, 2024
    for i in range(150):
        npi = W.npi_from("other|%d" % i)
        spec = ["FM", "IM", "FM", "IM", "PED", "GI", "ORTH", "CARD"][i % 8]
        reg = ["metro", "metro", "oshkosh", "sheboygan", "metro", "oshkosh"][i % 6]
        pool = {"metro": "OTM", "oshkosh": "OTO", "sheboygan": "OTS"}[reg]
        vol = 0.22 + 0.25 * h01("ovol", npi)
        referrals("OTHER", npi, spec, (2024, 2024), pool, None, None, vol, "other_ref", None, reg)
    # basket laboratory codes that some laboratories bill in units (glucose series, urine cultures)
    for i in range(1300):
        reg = ["metro", "oshkosh", "sheboygan"][i % 3]
        pool = {"metro": "OTM", "oshkosh": "OTO", "sheboygan": "OTS"}[reg]
        cpt = "82947" if i % 2 == 0 else "87086"
        cands = sorted(f[0] for f in W.FACILITIES if cpt in f[6])
        dest = cands[int(h01("ldest", i) * len(cands))]
        d = day_in(2024, 1 + i % 12, h01("lday", i))
        mid = draw_member(pool, ("lab", i))
        prod = mem.product_on(mid, d)
        if prod is None:
            continue
        units = 1 if h01("lunits", i) < 0.62 else (2 if h01("lunits2", i) < 0.7 else 3)
        lines.append(dict(kind="fac", tag="lab_units", practice="OTHER", member=mid, product=prod,
                          carrier=W.PRODUCTS[prod][0], date=d, cpt=cpt, fac=dest,
                          ref_npi=W.npi_from("other|%d" % (i % 150)), units=units))

    # ---- professional claims rendered in Manitowoc and Kewaunee counties, 2024
    def professional(practice, npi, spec, volume, pool, tag, zips, billing_practice=None, pos_tele=0.0):
        mix = PROF_MIX[spec]
        for (y, m) in months(2024, 2024):
            for code, per_year in mix.items():
                lam = per_year * volume / 12.0
                n = int(lam) + (1 if h01("pcnt", npi, code, m) < lam - int(lam) else 0)
                for k in range(n):
                    d = day_in(y, m, h01("pday", npi, code, m, k))
                    mid = draw_member(pool, ("p", npi, code, m, k))
                    prod = mem.product_on(mid, d)
                    if prod is None:
                        continue
                    pos = W.PROF[code][2]
                    if pos == "24":
                        pos = "24" if h01("asc", npi, code, m, k) < 0.7 else "22"
                    tele = None
                    if pos == "11" and code.startswith("992") and h01("tele", npi, code, m, k) < pos_tele:
                        tele = "10" if h01("tpos", npi, code, m, k) < 0.5 else "95"
                    zp = zips[int(h01("pz", npi, code, m, k) * len(zips))]
                    lines.append(dict(kind="prof", tag=tag, practice=billing_practice or practice, member=mid,
                                      product=prod, carrier=W.PRODUCTS[prod][0], date=d, code=code,
                                      rnd_npi=npi, site_zip=zp, pos=pos, tele=tele, units=1))

    bmg_sites = {"FM": ["54220", "54220", "54241", "54216"], "IM": ["54220", "54241", "54216"],
                 "GI": ["54220"] * 6 + ["54216"], "ORTH": ["54220"] * 4 + ["54216"],
                 "CARD": ["54220"] * 5 + ["54216"]}
    for npi in roster["BMG"]:
        professional("BMG", npi, people[npi]["spec"], 1.06, "BMG", "bmg_prof", bmg_sites[people[npi]["spec"]])
    # one Brightwater gastroenterologist also holds a Thursday clinic for Kinnickinnic, billed under its TIN
    gi_split = [n for n in roster["BMG"] if people[n]["spec"] == "GI"][1]
    professional("KPN", gi_split, "GI", 0.16, "LKO:Manitowoc", "kpn_split", ["54220"], billing_practice="KPN")
    sites = {"MFP": ["54228", "54228", "54241"], "RRF": ["54220"], "AFH": ["54201"], "KAC": ["54216", "54217"],
             "MDC": ["54220"] * 5 + ["54217"], "SOA": ["54220"] * 6 + ["54241", "54216"]}
    for p, vol, tele in (("MFP", 0.95, 0.04), ("RRF", 1.0, 0.05), ("AFH", 0.9, 0.04), ("KAC", 0.9, 0.03),
                         ("MDC", 1.0, 0.02), ("SOA", 1.0, 0.02)):
        for npi in roster[p]:
            professional(p, npi, people[npi]["spec"], vol, "LKO:Kewaunee" if p in ("KAC", "AFH") else "LKO:Manitowoc",
                         "lake_prof", sites[p], pos_tele=tele)
    for npi in roster["KPN"][:13]:
        professional("KPN", npi, people[npi]["spec"], 0.95, "LKO:Manitowoc", "kpn_prof", ["54220", "54220", "54241"],
                     pos_tele=0.05)
    # Ledgestone's gastroenterology and orthopedic clinic days at its Manitowoc outpatient center
    lmg_gi = [n for n in lmg_now if people[n]["spec"] == "GI"][:1]
    lmg_or = [n for n in lmg_now if people[n]["spec"] == "ORTH"][:1]
    for npi in lmg_gi + lmg_or:
        professional("LMG", npi, people[npi]["spec"], 0.22, "LKO:Manitowoc", "lmg_prof_lake", ["54220"])

    # a few further lakeshore referrals from the independent groups' outreach clinics
    for (county, fam), (n_other, n_ldg) in sorted(TOPUP.items()):
        prac, cpts, other, ldg = TOPUP_SOURCE[(county, fam)]
        npi = roster[prac][0]
        cands = [m for m in mem.by_pool["LKO"] if W.ZIP_COUNTY[mem.info[m]["zips"][0][0]] == county
                 and len(mem.info[m]["zips"]) == 1 and mem.info[m]["group"] is None]
        for j in range(n_other + n_ldg):
            d = day_in(2024, 2 + (j * 5) % 8, h01("tu_d", county, fam, j))
            mid = cands[int(h01("tu_m", county, fam, j) * len(cands))]
            prod = mem.product_on(mid, d)
            cpt = cpts[j % len(cpts)]
            lines.append(dict(kind="fac", tag="lake_ref", practice=prac, member=mid, product=prod,
                              carrier=W.PRODUCTS[prod][0], date=d, cpt=cpt, fac=other if j < n_other else ldg,
                              ref_npi=npi, units=1, event=None))
    return mem, people, assign, roster, lines


def build():
    mem, people, assign, roster, lines = simulate()
    return {"mem": mem, "people": people, "assign": assign, "roster": roster, "lines": lines}
