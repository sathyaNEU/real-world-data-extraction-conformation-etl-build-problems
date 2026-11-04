"""The world as it happened, in UTC: the retail fleet's and the contract carrier's trips, every compartment load at
the terminal and at the partner's, every drop, the ships' receipts, the diesel header's line-up, the transfers, the
vapour recovery unit and the tanks. Nothing here is a pack file; pack.py writes the systems' own views of it."""
import datetime as dt
import math

import numpy as np

import world as W

D = dt.timedelta
DENSITY = {"ULP": 735.0, "P95": 741.0, "P98": 746.0, "DSL": 836.0}
K54B = {"ULP": (346.4228, 0.4388), "P95": (346.4228, 0.4388), "P98": (346.4228, 0.4388), "DSL": (186.9696, 0.4862)}


def vcf(product, temp_c, rho=None):
    """ASTM Table 54B form, the old TAS's volume correction factor to 15 C, printed to four decimals."""
    k0, k1 = K54B[product]
    rho = rho or DENSITY[product]
    a = k0 / rho ** 2 + k1 / rho
    t = temp_c - 15.0
    return round(math.exp(-a * t * (1 + 0.8 * a * t)), 4)


def product_temp(utc, rng_day):
    loc = W.to_local(utc)
    doy = loc.timetuple().tm_yday + (loc.year - 2026) * 365
    return 19.6 + 5.4 * math.cos(2 * math.pi * (doy - 27) / 365.0) + rng_day


class Unit:
    def __init__(self, uid, operator, config, comps, cap, plates, tas_id):
        self.uid, self.operator, self.config, self.comps, self.cap = uid, operator, config, comps, cap
        self.plates, self.tas_id = plates, tas_id
        self.last = {c: ("ULP" if operator == "BRN" else "DSL") for c in range(1, comps + 1)}   # last delivered product
        self.vapour = {c: ("PET" if operator == "BRN" else "LEAN") for c in range(1, comps + 1)}
        self.last_tas = dict(self.last)      # last product this terminal's TAS saw it load
        self.free_at = None


def make_fleet(rng):
    units = []
    semis = ["BF-%02d" % n for n in (3, 5, 6, 9, 12)]
    bdbl = ["BF-%02d" % n for n in (14, 17, 21)]
    oak = ["OH-%03d" % n for n in (104, 117, 121, 126, 133)]
    letters = "ABCDEFGHJKLMNPRSTUVWXYZ"

    def plate():
        return "X%s%02d%s%s" % (letters[rng.integers(0, len(letters))], rng.integers(10, 99),
                                letters[rng.integers(0, len(letters))], letters[rng.integers(0, len(letters))])
    tas_ids = rng.choice(np.arange(312, 980), size=len(semis) + len(bdbl) + len(oak), replace=False)
    k = 0
    for u in semis:
        units.append(Unit(u, "BRN", "Semi-trailer", 5, [7600, 7600, 7600, 7600, 7600], [plate()], "T-%04d" % tas_ids[k]))
        k += 1
    for u in bdbl:
        units.append(Unit(u, "BRN", "B-double", 9, [6900] * 5 + [6700] * 4, [plate(), plate()], "T-%04d" % tas_ids[k]))
        k += 1
    for u in oak:
        units.append(Unit(u, "OAK", "Semi-trailer", 4, [9600, 9600, 9400, 9400], [plate()], "T-%04d" % tas_ids[k]))
        k += 1
    return units


def make_sites(rng):
    suburbs_metro = ["Ashgrove Heights", "Bellmere", "Calloway", "Dunmore Park", "Eastwick", "Fernlea", "Glenaven",
                     "Harbour Flat", "Iluka Rise", "Jarrah Hill", "Kellyville South", "Lindfield Bay", "Marsden Point",
                     "Northcote Vale", "Oyster Creek", "Parkhurst", "Quarry Hill", "Redbank", "Seaforth North",
                     "Tallow Beach", "Upper Warrenby", "Valley View", "Wattle Grove", "Yarramundi", "Warrenby Central",
                     "Port Warrenby", "Kingsholme", "Brookvale West", "Carrington", "Deepwater"]
    brands = ["Brennock", "Brennock", "Brennock", "Coastline Fuel", "Kwik Fuels", "Harbourside Service Centre",
              "Shoreway", "Northgate Motors", "Bayside Auto"]
    sites = []
    n = 0
    for s in suburbs_metro:
        for j in range(int(rng.integers(2, 6))):
            n += 1
            b = brands[int(rng.integers(0, len(brands)))]
            kind = "Service station"
            name = "%s %s" % (b, s) if j == 0 else "%s %s %s" % (b, s, ["North", "South", "Rd", "Hwy", "Plaza"][j % 5])
            sites.append(dict(code="S%04d" % (1000 + 37 * n + int(rng.integers(0, 30))), name=name, kind=kind, area=s,
                              metro=True, vr=True))
    rural = ["Gindabar", "Moorlands", "Tullamore Flats", "Kurrajong Creek", "Barwon Downs", "Coolac", "Ellerslie",
             "Mount Hope", "Narrabri West", "Spring Ridge", "Tilbuster", "Wollun", "Yetholme", "Bundella", "Garah"]
    kinds = [("Farm", "%s Pastoral"), ("Farm", "%s Grain Co"), ("Mine", "%s Quarry"), ("Depot", "%s Council Depot"),
             ("Farm", "%s Station"), ("Contractor", "%s Earthmoving")]
    for s in rural:
        for j in range(int(rng.integers(2, 5))):
            n += 1
            kind, fmt = kinds[int(rng.integers(0, len(kinds)))]
            sites.append(dict(code="R%04d" % (2000 + 41 * n + int(rng.integers(0, 35))), name=fmt % s, kind=kind,
                              area=s, metro=False, vr=False))
    codes = [x["code"] for x in sites]
    assert len(set(codes)) == len(codes)
    return sites


def simulate(seed=W.SEED):
    rng = np.random.default_rng(seed)
    units = make_fleet(rng)
    sites = make_sites(rng)
    metro = [s for s in sites if s["metro"]]
    rural = [s for s in sites if not s["metro"]]
    day_temp_noise = {}
    days = int((W.SIM_END_UTC - W.SIM_START_UTC).total_seconds() // 86400)
    walk = 0.0
    for d in range(days + 2):
        walk = 0.85 * walk + rng.normal(0, 0.55)
        day_temp_noise[d] = walk
    # Planned VRU stops (loading of petrol interlocked): local start, hours.
    vru_off = []
    for (y, m, dd, hh, hrs) in [(2026, 2, 24, 22, 4), (2026, 5, 12, 21, 5), (2026, 8, 19, 22, 4), (2026, 11, 10, 23, 3)]:
        s = W.local_to_utc(dt.datetime(y, m, dd, hh, 15))
        vru_off.append((s, s + D(hours=hrs, minutes=20)))

    def in_off(t):
        for a, b in vru_off:
            if a <= t < b:
                return b
        return None
    loads, drops = [], []
    trip_no = 0
    bol_seq = [404100]
    tarrant_seq = [880200]
    meter_err = {}
    for b in (1, 2, 3, 4, 5):
        for q in range(6):
            meter_err[(b, q)] = rng.normal(0, 0.0011)

    def qidx(t):
        loc = W.to_local(t)
        return 0 if loc.year < 2026 else (5 if loc.year > 2026 else (loc.month - 1) // 3 + 1)

    def temp_at(t):
        dd = int((t - W.SIM_START_UTC).total_seconds() // 86400)
        return product_temp(t, day_temp_noise[dd])
    # ---------------------------------------------------------------- trips, day by day, unit by unit
    for d in range(days):
        day0 = W.SIM_START_UTC + D(days=d)            # local midnight-ish (AEDT basis)
        for u in units:
            if u.operator == "BRN":
                if rng.random() < 0.09:
                    continue
                n_trips = int(rng.choice([1, 2, 3], p=[0.26, 0.56, 0.18]))
                t = day0 + D(hours=float(rng.uniform(3.0, 6.5)))
            else:
                if rng.random() < 0.13:
                    continue
                n_trips = int(rng.choice([1, 2], p=[0.5, 0.5]))
                t = day0 + D(hours=float(rng.uniform(4.0, 8.0)))
            if u.free_at is not None and t < u.free_at:
                t = u.free_at + D(minutes=float(rng.uniform(30, 120)))
            for k in range(n_trips):
                trip_no += 1
                exch = u.operator == "BRN" and rng.random() < 0.235
                comps = list(range(1, u.comps + 1))
                if u.operator == "BRN":
                    spare = int(rng.binomial(2, 0.22)) if u.comps == 9 else int(rng.binomial(1, 0.14))
                    used = sorted(int(x) for x in rng.choice(comps, size=u.comps - spare, replace=False))
                    nd = 0 if exch else int(min(len(used), max(0, rng.binomial(len(used), 0.385))))
                    pref = [c for c in used if u.last[c] == "DSL"]
                    rng.shuffle(pref)
                    chosen = [c for c in pref if rng.random() < 0.57][:nd]
                    pool = [c for c in used if c not in chosen]
                    rng.shuffle(pool)
                    while len(chosen) < nd:
                        chosen.append(pool.pop())
                    prods = {}
                    for c in used:
                        prods[c] = "DSL" if c in chosen else str(rng.choice(W.PETROL, p=[0.53, 0.32, 0.15]))
                else:
                    used = comps
                    prods = {c: "DSL" for c in used}
                # ------------- loading
                pet = [c for c in used if prods[c] != "DSL"]
                dsl = [c for c in used if prods[c] == "DSL"]
                t_load = t
                if pet and not exch:
                    end = in_off(t_load)
                    while end is None and any(in_off(t_load + D(minutes=4 * i)) for i in range(len(pet) + 2)):
                        t_load = t_load + D(minutes=15)
                        end = in_off(t_load)
                    if end is not None:
                        t_load = end + D(minutes=float(rng.uniform(4, 25)))
                term = "SELWYN" if exch else "WARRENBY"
                seq = []
                if u.operator == "BRN":
                    pbay = int(rng.integers(1, 4))
                    dbay = 4 if rng.random() < 0.885 else 5
                    order = (pet, dsl) if rng.random() < 0.6 else (dsl, pet)
                    tt = t_load + D(minutes=float(rng.uniform(6, 18)))
                    for grp in order:
                        for c in grp:
                            seq.append((c, pbay if prods[c] != "DSL" else dbay, tt))
                            tt = tt + D(minutes=float(rng.uniform(2.6, 4.4)))
                        tt = tt + D(minutes=float(rng.uniform(5, 14)))
                else:
                    tt = t_load + D(minutes=float(rng.uniform(5, 15)))
                    for c in used:
                        seq.append((c, 5, tt))
                        tt = tt + D(minutes=float(rng.uniform(3.4, 5.2)))
                bol_by_bay = {}
                trip_loads = {}
                for c, bay, tb in seq:
                    p = prods[c]
                    gross = int(round(u.cap[c - 1] * float(rng.uniform(0.84, 0.995)) / 10.0) * 10)
                    temp = round(temp_at(tb) + float(rng.normal(0, 0.55)), 1)
                    v = vcf(p, temp)
                    net = int(round(gross * v))
                    if term == "WARRENBY":
                        if bay not in bol_by_bay:
                            bol_seq[0] += int(rng.integers(1, 3))
                            bol_by_bay[bay] = "W26-%06d" % bol_seq[0]
                        bol = bol_by_bay[bay]
                    else:
                        if "T" not in bol_by_bay:
                            tarrant_seq[0] += int(rng.integers(2, 9))
                            bol_by_bay["T"] = "SP%07d" % tarrant_seq[0]
                        bol = bol_by_bay["T"]
                    actual = gross * (1 + meter_err[(bay if term == "WARRENBY" else 1, qidx(tb))])
                    loads.append(dict(trip=trip_no, unit=u.uid, operator=u.operator, comp=c, product=p,
                                      gross=gross, temp=temp, vcf=v, net=net, utc=tb, terminal=term,
                                      bay=bay if term == "WARRENBY" else None, bol=bol,
                                      arrive_vapour=u.vapour[c], prev=u.last[c], prev_tas=u.last_tas[c],
                                      actual_net=actual * v, cap=u.cap[c - 1]))
                    trip_loads[c] = loads[-1]
                    if term == "WARRENBY":
                        u.last_tas[c] = p
                # ------------- deliveries
                t_dep = max(x[2] for x in seq) + D(minutes=float(rng.uniform(8, 20)))
                if u.operator == "BRN":
                    n_sites = int(rng.choice([1, 2, 3], p=[0.30, 0.48, 0.22]))
                    stops = [metro[int(i)] for i in rng.choice(len(metro), size=n_sites, replace=False)]
                else:
                    n_sites = int(rng.choice([1, 2, 3, 4], p=[0.18, 0.40, 0.30, 0.12]))
                    stops = [rural[int(i)] for i in rng.choice(len(rural), size=n_sites, replace=False)]
                assign = {c: int(rng.integers(0, n_sites)) for c in used}
                split = None
                if n_sites > 1 and rng.random() < 0.18:
                    split = used[int(rng.integers(0, len(used)))]
                tcur = t_dep + D(minutes=float(rng.uniform(25, 70)))
                for si, st in enumerate(stops):
                    cs = [c for c in used if assign[c] == si or (split == c and si == (assign[c] + 1) % n_sites)]
                    for c in cs:
                        ld = trip_loads[c]
                        share = 1.0
                        if split == c:
                            share = 0.55 if assign[c] == si else 0.45
                        dtemp = ld["temp"] + float(rng.normal(1.2, 1.1))
                        delivered = int(round(ld["gross"] * share * (1 + 0.00095 * (dtemp - ld["temp"]))))
                        arr = tcur
                        done = tcur + D(minutes=float(rng.uniform(9, 19)))
                        drops.append(dict(trip=trip_no, unit=u.uid, comp=c, product=ld["product"], site=st["code"],
                                          litres=delivered, vr=(st["vr"] and ld["product"] != "DSL"),
                                          arr=arr, done=done, terminal=term, ref=ld["bol"],
                                          driver=None, loaded=ld["net"], load_utc=ld["utc"], bay=ld["bay"]))
                        tcur = done + D(minutes=float(rng.uniform(1, 4)))
                    tcur = tcur + D(minutes=float(rng.uniform(18, 55)))
                # after the trip every used compartment carries what its last drop left
                for c in used:
                    p = prods[c]
                    u.last[c] = p
                    u.vapour[c] = "PET" if p != "DSL" else "LEAN"
                t = tcur + D(minutes=float(rng.uniform(20, 75)))
                u.free_at = t
    # drivers: a roster of ids per unit and period
    drv_ids = {}
    for u in units:
        drv_ids[u.uid] = ["D%04d" % int(x) for x in rng.choice(np.arange(1100, 9800), size=3, replace=False)]
    for x in drops:
        x["driver"] = drv_ids[x["unit"]][int(rng.integers(0, 3))]
    loads.sort(key=lambda r: (r["utc"], r["unit"], r["comp"]))
    drops.sort(key=lambda r: (r["arr"], r["unit"], r["comp"]))
    return dict(rng=rng, units=units, sites=sites, loads=loads, drops=drops, vru_off=vru_off, temp_at=temp_at,
                meter_err=meter_err)


# ----------------------------------------------------------------------------------- the vapour at each load
def load_vapour(ld):
    """kg of VOC each load pushed out of its compartment, and where it went: the petrol bays to the VRU, the
    distillate bays to air. A compartment that last delivered petrol through a station's vapour balance holds
    saturated petrol vapour; one that last delivered diesel holds next to none."""
    m = W.to_local(ld["utc"]).month
    if ld["product"] != "DSL":
        sat = 1.0 if ld["arrive_vapour"] == "PET" else 0.5
        return sat * ld["gross"] / 1000.0 * W.vapour_kg_per_kl(W.grade_season(m), ld["temp"], 1.0)
    own = ld["gross"] / 1000.0 * W.vapour_kg_per_kl("diesel", ld["temp"], 0.6)
    if ld["arrive_vapour"] == "PET":
        return own + ld["gross"] / 1000.0 * W.vapour_kg_per_kl(W.grade_season(m), ld["temp"], 1.0)
    return own
