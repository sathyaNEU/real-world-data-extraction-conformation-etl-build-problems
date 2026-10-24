"""Halvard County Air Quality Program's world: the Halvard Valley PM2.5 maintenance area's five burn zones, the
households on their parcels (main heating fuel, the wood-burning appliances registered there and the wood each burns),
three propane distributors' accounts with every delivery from July 2023 to June 2026, the 2024-25 household heating
survey, the airport station's daily temperatures, and the county's households outside the maintenance area. Propane
prices spiked from December 2025 to February 2026; households with a heating appliance moved part of their heat onto
it, households without one did not cut back. Everything else in the pack is written from these objects."""
import datetime as dt

import numpy as np

SEED = 4843
PROGRAM = "Halvard County Air Quality Program"
COUNTY = "Halvard"
STATE_DEQ = "Montana Department of Environmental Quality"
PEOPLE = dict(lead="Billy Davis", registry="Kimberly Rogers", inventory="Martin Booth")
SEASONS = {2023: (dt.date(2023, 10, 1), dt.date(2024, 4, 30)), 2024: (dt.date(2024, 10, 1), dt.date(2025, 4, 30)),
           2025: (dt.date(2025, 10, 1), dt.date(2026, 4, 30))}
WINDOW = (dt.date(2023, 7, 1), dt.date(2026, 6, 30))
REGISTRY_ASOF = dt.date(2026, 5, 15)
HDD_TARGET = {2023: 7904.0, 2024: 7391.0, 2025: 7395.0}
ALLOTMENT = dict(VFN=63.9, VFS=52.6, EB=89.9, WB=77.6, UV=58.6)     # Table 4-2, tons of PM2.5 a heating season
FUND = 465000                                                        # the 2026-27 changeout fund, USD
RESPONSE_RATE = 0.62
SURVEY_SEED = SEED + 238007          # the respondents drawn (seedsearch: every standing member mid-bin)
ACCOUNT_SEED = SEED + 8013          # asktune: every ask A figure mid-bin
REMAINDER_SEED = SEED + 243011      # asktune_b: every ask B figure mid-bin, the 2010 codes read as 2020 move all twelve

BTU_GAL = 91500.0              # propane, Btu per gallon (the state's fuel equivalents sheet)
AFUE = 0.85                    # an existing propane furnace or boiler
CORD_MMBTU = 18.5              # the state tool's cord of the valley's mixed softwoods
PELLET_MMBTU_TON = 16.4
TONS_PER_CORD = 1.163

# class: SCC, description, the county's device code, heating efficiency (None: not a heating appliance), the 2023
# factor in pounds of PM2.5 per ton, the median 2024-25 burning (cords; pellets in tons), the share of a home's heat
# demand moved onto it in 2025-26 by a propane home
CLASSES = {
    "UNC": ("2104008310", "Woodstove: freestanding, non-EPA certified", "STV-U", 0.54, 30.6, 2.3, 0.18),
    "CNC": ("2104008320", "Woodstove: freestanding, EPA certified, non-catalytic", "STV-C", 0.68, 14.6, 2.0, 0.18),
    "CAT": ("2104008330", "Woodstove: freestanding, EPA certified, catalytic", "STV-K", 0.72, 13.0, 1.9, 0.18),
    "PEL": ("2104008400", "Woodstove: pellet-fired, general (freestanding or FP insert)", "PLT", 0.78, 3.2, 1.4, 0.14),
    "FPL": ("2104008100", "Fireplace: general", "FPL", None, 23.6, 0.4, 0.0),
    "HYD": ("2104008610", "Hydronic heater: outdoor", "OHH", 0.45, 18.8, 6.5, 0.28),
}
CL = list(CLASSES)
HEATING = [c for c in CL if CLASSES[c][3] is not None]

# code, name, appliances in use, class mix (CL order), propane share of appliance homes, gas share, propane homes
# without an appliance, commercial propane accounts, distributor shares (D1, D2, D3) of the zone's residential accounts
ZONES = [
    ("VFN", "Valley Floor North", 3400, (.14, .37, .08, .14, .26, .01), 0.08, 0.84, 700, 150, (0.70, 0.30, 0.00)),
    ("VFS", "Valley Floor South", 3100, (.18, .35, .07, .13, .25, .02), 0.12, 0.80, 900, 140, (0.50, 0.00, 0.50)),
    ("EB", "East Bench", 2300, (.30, .33, .08, .12, .07, .10), 0.75, 0.05, 2600, 105, (0.55, 0.45, 0.00)),
    ("WB", "West Bench", 2000, (.28, .35, .08, .13, .07, .09), 0.68, 0.08, 2100, 95, (0.00, 0.60, 0.40)),
    ("UV", "Upper Valley", 1300, (.26, .34, .07, .12, .09, .12), 0.50, 0.00, 1100, 80, (0.00, 0.30, 0.70)),
]
ZC = [z[0] for z in ZONES]
ZNAME = {z[0]: z[1] for z in ZONES}
DIST = ["D1", "D2", "D3"]

STREETS = {
    "VFN": ["Airport", "Meridian", "Northgate", "Halvard", "Grange", "Cottonwood", "Depot", "Mill Creek", "Larch"],
    "VFS": ["Southgate", "Fairground", "Riverside", "Orchard", "Willow", "Granary", "Sheridan", "Lone Pine", "Mead"],
    "EB": ["East Bench", "Ponderosa", "Elk Ridge", "Coyote", "Sun Canyon", "Timberline", "Bunchgrass", "Quartz"],
    "WB": ["West Bench", "Juniper", "Pinecrest", "Sage Hen", "Antler", "Lookout", "Cutbank", "Saddle"],
    "UV": ["Upper Valley", "Beaver Creek", "Trapper", "Moose", "Hidden Lake", "Kinnick", "Snowshoe", "Fox Hollow"],
}
STYPE = {"VFN": ["St", "Ave", "Dr", "Ln"], "VFS": ["St", "Ave", "Dr", "Ln"], "EB": ["Rd", "Ln", "Trl", "Dr"],
         "WB": ["Rd", "Ln", "Trl", "Loop"], "UV": ["Rd", "Trl", "Ln", "Loop"]}
DIRS = {"VFN": "N", "VFS": "S"}


def address(z, num, street, stype):
    """A situs address in the assessor's form: the valley floor's grid carries its directional, the rural roads none."""
    return ("%d %s %s %s" % (num, DIRS[z], street, stype)) if z in DIRS else "%d %s %s" % (num, street, stype)


class Home:
    __slots__ = ("hid", "zone", "parcel", "address", "fuel", "devices", "D", "base", "s", "acct", "outside")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


class Device:
    __slots__ = ("did", "home", "cl", "installed", "registered", "removed", "reason", "replaces", "replaced_by",
                 "w24", "cert", "survey")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def energy_per_unit(cl):
    """Btu in a cord (pellets: a ton)."""
    return (PELLET_MMBTU_TON if cl == "PEL" else CORD_MMBTU) * 1e6


def tons_of(cl, units):
    return units if cl == "PEL" else units * TONS_PER_CORD


def in_use(d, season):
    a, b = SEASONS[season]
    return d.installed <= a and (d.removed is None or d.removed > b)


def _geocode(r, zi):
    return "17-%04d-%02d-%d-%02d-%02d-0000" % (2100 + 37 * zi + int(r.integers(0, 37)), int(r.integers(1, 37)),
                                               int(r.integers(1, 5)), int(r.integers(1, 20)), int(r.integers(1, 40)))


def build():
    r = np.random.default_rng(SEED)
    homes, devices = [], []
    used_parcel, used_addr = set(), set()
    nxt = [24000]

    def new_did():
        nxt[0] += int(r.integers(1, 6))
        return "SFD-%06d" % nxt[0]

    def parcel_and_address(zi, z):
        while True:
            p = _geocode(r, zi)
            if p not in used_parcel:
                used_parcel.add(p)
                break
        while True:
            num = int(r.integers(100, 9999)) if z in ("VFN", "VFS") else int(r.integers(1000, 39999))
            a = address(z, num, STREETS[z][int(r.integers(len(STREETS[z])))], STYPE[z][int(r.integers(len(STYPE[z])))])
            if a.upper() not in used_addr:
                used_addr.add(a.upper())
                return p, a

    hid = [0]
    for zi, (z, name, n_dev, mix, p_prop, p_gas, n_noapp, n_com, dshare) in enumerate(ZONES):
        cls = r.choice(CL, size=n_dev, p=np.array(mix) / sum(mix))
        k = 0
        while k < n_dev:
            u = r.random()
            fuel = "propane" if u < p_prop else "gas" if u < p_prop + p_gas else \
                str(r.choice(["electric", "wood"], p=[0.55, 0.45]))
            hid[0] += 1
            p, a = parcel_and_address(zi, z)
            h = Home(hid=hid[0], zone=z, parcel=p, address=a, fuel=fuel, devices=[], outside=False)
            take = 2 if (fuel != "propane" and k + 1 < n_dev and r.random() < 0.05 and cls[k] != "FPL") else 1
            for j in range(take):
                cl = str(cls[k]) if j == 0 else "FPL"
                k += 1
                med = CLASSES[cl][5] * (1.12 if z in ("EB", "WB", "UV") else 1.0) * (1.25 if fuel == "wood" else 1.0)
                d = Device(did=new_did(), home=h, cl=cl, w24=float(med * r.lognormal(0, 0.45)), survey=False)
                d.installed = _install_date(r, fuel)
                d.registered = max(d.installed, dt.date(2008, 3, 1)) + dt.timedelta(days=int(r.integers(5, 140)))
                if d.registered > REGISTRY_ASOF:
                    d.registered = d.installed + dt.timedelta(days=3)
                d.cert = _cert(r, cl)
                h.devices.append(d)
                devices.append(d)
            homes.append(h)
        for i in range(n_noapp):
            hid[0] += 1
            p, a = parcel_and_address(zi, z)
            homes.append(Home(hid=hid[0], zone=z, parcel=p, address=a, fuel="propane", devices=[], outside=False))
    # history: devices removed, replaced by the changeout programme (2016 to 2022 summers) or by owners, and
    # appliances installed since; nothing changes at a propane home after 2022, nothing inside a heating season
    for d in list(devices):
        h = d.home
        if d.cl in ("UNC", "HYD") and r.random() < (0.10 if h.fuel != "propane" else 0.07):
            yr = int(r.integers(2016, 2023)) if h.fuel == "propane" else int(r.integers(2016, 2026))
            when = dt.date(yr, int(r.integers(5, 9)), int(r.integers(1, 29)))
            old = Device(did=new_did(), home=h, cl=d.cl, survey=False, cert="",
                         w24=float(CLASSES[d.cl][5] * (1.12 if h.zone in ("EB", "WB", "UV") else 1.0) * r.lognormal(0, 0.45)))
            old.installed = _install_date(r, h.fuel, before=when.year - 3)
            old.registered = max(old.installed, dt.date(2008, 3, 1)) + dt.timedelta(days=int(r.integers(5, 140)))
            old.removed, old.reason, old.replaced_by = when, "Changeout", d
            d.cl = "CNC" if d.cl == "UNC" or r.random() < 0.6 else "PEL"
            d.cert = _cert(r, d.cl)
            d.w24 = float(CLASSES[d.cl][5] * (1.12 if h.zone in ("EB", "WB", "UV") else 1.0) * r.lognormal(0, 0.45))
            d.installed = when + dt.timedelta(days=int(r.integers(1, 20)))
            d.registered = d.installed + dt.timedelta(days=int(r.integers(2, 30)))
            d.replaces = old
            devices.append(old)
        elif h.fuel != "propane" and r.random() < 0.035:      # removed by the owner, nothing replacing it
            yr = int(r.integers(2016, 2026))
            when = dt.date(yr, int(r.integers(5, 10)), int(r.integers(1, 29)))
            gone = Device(did=new_did(), home=h, cl=d.cl, survey=False, cert=d.cert,
                          w24=float(CLASSES[d.cl][5] * (1.12 if h.zone in ("EB", "WB", "UV") else 1.0) * r.lognormal(0, 0.45)),
                          installed=_install_date(r, h.fuel, before=when.year - 2), reason=str(
                              r.choice(["Owner removed", "Home sale removal", "Demolition", "Converted to gas"])))
            gone.registered = max(gone.installed, dt.date(2008, 3, 1)) + dt.timedelta(days=int(r.integers(5, 140)))
            gone.removed = when
            devices.append(gone)
    for d in devices:
        if d.registered > REGISTRY_ASOF:
            d.registered = REGISTRY_ASOF - dt.timedelta(days=int(r.integers(10, 60)))
    # heat demand (gallons of propane at 2024-25 weather), each appliance's 2024-25 heat, and the 2025-26 switch
    for h in homes:
        if h.fuel != "propane":
            continue
        h.D = float(r.lognormal(np.log(820 if h.devices else 880), 0.28))
        h.base = float(r.uniform(0, 30))
        h.s = 0.0
        if h.devices:
            c = h.devices[0].cl
            h.s = float(CLASSES[c][6] * r.uniform(0.6, 1.4))
    devices.sort(key=lambda d: d.did)
    return homes, devices


def _install_date(r, fuel, before=None):
    hi = 2022 if fuel == "propane" else 2025
    if before is not None:
        hi = min(hi, before)
    yr = int(r.integers(1979, hi + 1))
    return dt.date(yr, int(r.integers(5, 10)), int(r.integers(1, 29)))


def _cert(r, cl):
    if cl in ("CNC", "CAT", "PEL", "HYD") and r.random() < 0.9:
        return "%s-%04d" % ({"CNC": "N", "CAT": "C", "PEL": "P", "HYD": "H"}[cl], int(r.integers(100, 2400)))
    return ""


def heating_propane(h):
    """2024-25 heating propane: the heat demand less what its appliance delivered, never below a quarter of demand."""
    if not h.devices:
        return h.D
    d = h.devices[0]
    eff = CLASSES[d.cl][3]
    if eff is None:
        return h.D
    wood_heat = d.w24 * energy_per_unit(d.cl) * eff / (BTU_GAL * AFUE)
    return max(h.D - wood_heat, 0.25 * h.D)


def hdd_ratio(season, temps):
    return temps["hdd"][season] / temps["hdd"][2024]


def season_propane(homes, temps):
    """Each propane home's in-season deliveries by season (gallons): heating at the season's degree days, less the
    2025-26 switch, plus the base load, with the season's delivery noise."""
    r = np.random.default_rng(SEED + 3)
    out = {}
    for h in homes:
        if h.fuel != "propane":
            continue
        hp = heating_propane(h)
        rec = {}
        for t in (2023, 2024, 2025):
            f = hdd_ratio(t, temps)
            shift = h.s * h.D * f if t == 2025 else 0.0
            rec[t] = max(30.0, (hp * f - shift + h.base) * float(r.lognormal(0, 0.06)))
        out[h.hid] = rec
    return out


def wood_2025(d, h, temps):
    """The world's 2025-26 burning (cords; pellets in tons)."""
    f = hdd_ratio(2025, temps)
    units = d.w24 * f
    if h.fuel == "propane" and h.devices and d is h.devices[0] and CLASSES[d.cl][3] is not None:
        units += h.s * h.D * f * BTU_GAL * AFUE / (energy_per_unit(d.cl) * CLASSES[d.cl][3])
    return units


def temperatures():
    """Daily maximum and minimum (deg F) at the airport, 1 July 2023 to 30 June 2026, with each season's heating
    degree days (base 65, daily mean of maximum and minimum) brought to its target by a uniform offset."""
    r = np.random.default_rng(SEED + 5)
    days = [WINDOW[0] + dt.timedelta(days=i) for i in range((WINDOW[1] - WINDOW[0]).days + 1)]
    doy = np.array([d.timetuple().tm_yday for d in days])
    clim = 42.0 - 25.0 * np.cos(2 * np.pi * (doy - 18) / 365.25)
    anom = np.zeros(len(days))
    for i in range(1, len(days)):
        anom[i] = 0.78 * anom[i - 1] + r.normal(0, 4.2)
    mean = clim + anom
    for t, (a, b) in SEASONS.items():
        idx = np.array([a <= d <= b for d in days])
        lo, hi = -15.0, 15.0
        for _ in range(80):
            mid = (lo + hi) / 2
            h = np.maximum(0, 65 - np.round(mean[idx] + mid, 1)).sum()
            if h > HDD_TARGET[t]:
                lo = mid
            else:
                hi = mid
        mean[idx] = mean[idx] + (lo + hi) / 2
    rng = np.clip(r.normal(22, 5, len(days)), 8, 40)
    tmax = np.round(mean + rng / 2)
    tmin = np.round(mean - rng / 2)
    # whole-degree readings: settle each season's degree days on the readings themselves
    hdd = {}
    for t, (a, b) in SEASONS.items():
        hdd[t] = float(sum(max(0.0, 65 - (tmax[i] + tmin[i]) / 2) for i, d in enumerate(days) if a <= d <= b))
    return dict(days=days, tmax=tmax, tmin=tmin, hdd=hdd)


SURVEY_RATE = dict(VFN=0.085, VFS=0.09, EB=0.10, WB=0.10, UV=0.11)
SURVEY_FRAME, SURVEY_SAMPLED, SURVEY_RESP = {}, {}, {}
SMALL_CELL = 10


def survey(devices):
    """The 2024-25 household heating survey (fielded May to June 2025): a sample of each zone's appliances in use that
    season, each respondent's weight its zone's frame over its respondents. Reported use carries the respondent's
    recall and the unit they chose."""
    r = np.random.default_rng(SURVEY_SEED)
    out = []
    for z in ZC:
        frame = [d for d in devices if d.home.zone == z and in_use(d, 2024)]
        k = int(round(SURVEY_RATE[z] * len(frame)))
        SURVEY_FRAME[z], SURVEY_RESP[z] = len(frame), k
        SURVEY_SAMPLED[z] = int(round(k / RESPONSE_RATE)) + int(r.integers(0, 9))
        pick = sorted(r.choice(len(frame), k, replace=False))
        for j in pick:
            d = frame[j]
            d.survey = True
            use = d.w24 * float(r.lognormal(0, 0.10))
            if d.cl == "PEL":
                unit = "bags (40 lb)" if r.random() < 0.6 else "tons"
                amt = float(round(use * 2000 / 40)) if unit.startswith("bags") else round(use * 4) / 4
                conv = amt * 40 / 2000 if unit.startswith("bags") else amt
            else:
                u = r.random()
                unit = "face cords" if u < 0.25 else "pickup loads" if u < 0.40 else "cords"
                amt = float(round(use * 3)) if unit == "face cords" else round(use * 2) / 1.0 if unit == "pickup loads" \
                    else round(use * 4) / 4
                conv = amt / 3 if unit == "face cords" else amt / 2 if unit == "pickup loads" else amt
            out.append(dict(dev=d, weight=len(frame) / k, amount=amt, unit=unit, units=float(conv)))
    return out


def survey_means(resp):
    """The vendor's estimates: a zone's appliances of a class burned the weighted mean of the zone's respondents with
    that class (cords; pellets in tons); a class with fewer than ten respondents in a zone takes the maintenance
    area's weighted mean for the class."""
    area = {}
    for c in CL:
        xs = [(x["weight"], x["units"]) for x in resp if x["dev"].cl == c]
        area[c] = sum(w * u for w, u in xs) / sum(w for w, u in xs)
    out = {}
    for z in ZC:
        for c in CL:
            xs = [(x["weight"], x["units"]) for x in resp if x["dev"].cl == c and x["dev"].home.zone == z]
            out[z, c] = (sum(w * u for w, u in xs) / sum(w for w, u in xs)) if len(xs) >= SMALL_CELL else area[c]
    return out


TOWNS_OUT = ["Brennan", "Kessler Flat", "Dunmore"]
STREETS_OUT = ["Brennan", "Old Stage", "Kessler", "Dunmore", "Ranch", "Prairie View"]


def accounts(homes, temps):
    """Every propane account in the three distributors' books for the valley: one per propane home in the zones, the
    commercial and institutional accounts, and residential accounts just outside the maintenance area. Each carries
    its distributor, number, class, parcel, address and in-season gallons by season."""
    r = np.random.default_rng(ACCOUNT_SEED)
    season = season_propane(homes, temps)
    acc = []
    for z, name, n_dev, mix, p_prop, p_gas, n_noapp, n_com, dshare in ZONES:
        for h in homes:
            if h.zone != z or h.fuel != "propane":
                continue
            dist = str(r.choice(DIST, p=dshare))
            a = dict(dist=dist, cls="RES", zone=z, parcel=h.parcel, address=h.address, home=h, gal=season[h.hid],
                     tank=500 if r.random() < 0.8 else 1000, statement=False, outside=False)
            h.acct = a
            acc.append(a)
    used = {a["address"].upper() for a in acc}
    zi_of = {z[0]: i for i, z in enumerate(ZONES)}
    taken = {h.parcel for h in homes}
    r_geo = np.random.default_rng(ACCOUNT_SEED + 1)        # a fresh parcel where a draw lands on one already taken
    for z, name, n_dev, mix, p_prop, p_gas, n_noapp, n_com, dshare in ZONES:
        for i in range(n_com):
            dist = str(r.choice(DIST, p=[0.35, 0.45, 0.20] if z not in ("VFS", "UV") else [0.30, 0.45, 0.25]))
            if dist == "D1" and z in ("WB", "UV"):
                dist = "D2"
            if dist == "D3" and z in ("VFN", "EB"):
                dist = "D2"
            base = float(r.lognormal(np.log(2300), 0.75))
            gal = {t: max(60.0, base * hdd_ratio(t, temps) * float(r.lognormal(0, 0.07))) for t in (2023, 2024, 2025)}
            p = _geocode(r, zi_of[z])
            while p in taken:
                p = _geocode(r_geo, zi_of[z])
            taken.add(p)
            while True:
                ad = address(z, int(r.integers(100, 9999)), STREETS[z][int(r.integers(len(STREETS[z])))],
                             STYPE[z][int(r.integers(len(STYPE[z])))])
                if ad.upper() not in used:
                    used.add(ad.upper())
                    break
            acc.append(dict(dist=dist, cls="COM", zone=z, parcel=p, address=ad, home=None, gal=gal,
                            tank=int(r.choice([1000, 1000, 2000, 3000])), statement=(dist == "D2" and r.random() < 0.7),
                            outside=False))
    for i in range(330):
        dist = str(r.choice(DIST, p=[0.4, 0.35, 0.25]))
        base = float(r.lognormal(np.log(860), 0.3))
        gal = {t: max(30.0, base * hdd_ratio(t, temps) * float(r.lognormal(0, 0.06))) for t in (2023, 2024, 2025)}
        town = TOWNS_OUT[int(r.integers(len(TOWNS_OUT)))]
        while True:
            ad = "%d %s %s" % (int(r.integers(1000, 49999)), STREETS_OUT[int(r.integers(len(STREETS_OUT)))],
                               str(r.choice(["Rd", "Ln", "Trl"])))
            if ad.upper() not in used:
                used.add(ad.upper())
                break
        acc.append(dict(dist=dist, cls="RES", zone=None, parcel="17-%04d-%02d-%d-%02d-%02d-0000" % (
            2400 + int(r.integers(0, 300)), int(r.integers(1, 37)), int(r.integers(1, 5)), int(r.integers(1, 20)),
            int(r.integers(1, 40))), address=ad, town=town, home=None, gal=gal, tank=500, statement=False,
                        outside=True))
    # account numbers in each distributor's own series
    order = r.permutation(len(acc))
    seq = dict(D1=[104000, 51000], D2=[30000], D3=[7000])
    for j in order:
        a = acc[j]
        if a["dist"] == "D1":
            k = 0 if a["cls"] == "RES" else 1
            seq["D1"][k] += int(r.integers(1, 7))
            a["no"] = str(seq["D1"][k])
        elif a["dist"] == "D2":
            seq["D2"][0] += int(r.integers(1, 9))
            a["no"] = "%02d-%05d" % (int(r.integers(10, 99)), seq["D2"][0])
        else:
            seq["D3"][0] += int(r.integers(1, 4))
            a["no"] = "M%05d" % seq["D3"][0]
        a["opened"] = dt.date(int(r.integers(1996, 2023)), int(r.integers(1, 13)), int(r.integers(1, 28)))
    return acc


def tickets(acc, temps):
    """Every delivery, 1 July 2023 to 30 June 2026: each season's gallons in fills dated in proportion to the day's
    heating degree days, summer top-offs and spring fills outside the seasons. A delivery's gallons are to the tenth."""
    r = np.random.default_rng(SEED + 17)
    days = temps["days"]
    hdd_day = np.maximum(0.0, 65 - (temps["tmax"] + temps["tmin"]) / 2)
    idx = {d: i for i, d in enumerate(days)}
    out = []
    for a in acc:
        com = a["cls"] == "COM"
        fill = (0.55 if a["tank"] == 500 else 0.6) * a["tank"]
        # each account's habits outside the season: a summer top-off on a pre-buy plan, a spring fill
        topoff = float(r.uniform(40, 0.5 * a["tank"])) if r.random() < (0.55 if not com else 0.3) else 0.0
        spring = float(r.uniform(30, 0.4 * a["tank"])) if r.random() < 0.45 else 0.0
        for t in (2023, 2024, 2025):
            s0, s1 = SEASONS[t]
            lo, hi = idx[s0], idx[s1]
            g = a["gal"][t]
            n = max(1, int(round(g / (fill * float(r.uniform(0.85, 1.15))))))
            w = hdd_day[lo:hi + 1] + 2.0
            pick = np.sort(r.choice(np.arange(lo, hi + 1), size=n, replace=False, p=w / w.sum()))
            share = r.dirichlet(np.full(n, 8.0))
            tenths = np.floor(share * g * 10).astype(int)
            tenths[-1] += int(round(g * 10)) - int(tenths.sum())
            for i, k in zip(pick, tenths):
                out.append(dict(acct=a, date=days[i], gal=k / 10.0))
            # outside the season: the summer top-off before it, the spring fill after it
            y = s0.year
            if topoff:
                d = dt.date(y, int(r.integers(7, 10)), int(r.integers(1, 29)))
                out.append(dict(acct=a, date=d, gal=round(topoff * float(r.lognormal(0, 0.05)), 1)))
            if spring:
                d = dt.date(y + 1, int(r.integers(5, 7)), int(r.integers(1, 29)))
                if d <= WINDOW[1]:
                    out.append(dict(acct=a, date=d, gal=round(spring * float(r.lognormal(0, 0.05)), 1)))
    out.sort(key=lambda x: (x["date"], x["acct"]["dist"], x["acct"]["no"]))
    return out


def remainder():
    """Halvard County outside the maintenance area. The ACS tabulates 2020 block groups; the county assessor's GIS
    still carries the 2010 block groups, whose codes are the same where a tract kept its number but whose lines were
    redrawn in some tracts as the edge of the valley built out. Housing units sit in the overlaps of a 2010 and a 2020
    block group; a 2010 block group's units inside the maintenance area are a fixed share of each of its overlaps (the
    plan drew the area on 2010 lines). Wood is the main heat in the rural units far more often than in the valley's."""
    r = np.random.default_rng(REMAINDER_SEED)
    bg20, bg10, ov = [], [], []
    fips = "30059"
    for t in range(16):
        tract = fips + "%06d" % (960100 + 100 * t)
        redrawn = r.random() < 0.55
        f_in = []
        for b in (1, 2, 3):
            u = r.random()
            f_in.append(1.0 if u < 0.40 else float(np.round(r.uniform(0.15, 0.85), 2)) if u < 0.62 else 0.0)
        f_in.sort(reverse=True)
        hu = np.zeros((3, 3))
        for i10 in range(3):
            hu[i10, i10] = int(r.integers(280, 1050))
        if redrawn:
            hu[2, 0] = int(r.integers(220, 700))          # the outer block group's rural units into the first
            if r.random() < 0.6:
                hu[0, 1] = int(r.integers(80, 400))
            if r.random() < 0.4:
                hu[1, 2] = int(r.integers(80, 300))
        for i10 in range(3):
            tot = hu[i10].sum()
            inside = int(round(tot * f_in[i10]))
            bg10.append(dict(geoid=tract + str(i10 + 1), hu=int(tot), inside=inside))
            for j20 in range(3):
                if hu[i10, j20]:
                    ov.append(dict(g10=tract + str(i10 + 1), g20=tract + str(j20 + 1), hu=int(hu[i10, j20])))
        for j20 in range(3):
            tot = int(hu[:, j20].sum())
            out = sum(hu[i10, j20] * (1 - f_in[i10]) for i10 in range(3))
            wood = int(round(out * r.uniform(0.15, 0.24) + (tot - out) * r.uniform(0.02, 0.05)))
            drift = r.normal(1.04, 0.05)
            bg20.append(dict(geoid=tract + str(j20 + 1), hu=tot, outside=float(out / tot),
                             acs1923=wood, moe1923=int(round(wood * r.uniform(0.25, 0.6))) + 9,
                             acs2024=int(round(wood * drift)), moe2024=int(round(wood * r.uniform(0.25, 0.6))) + 9))
    return dict(bg20=bg20, bg10=bg10, ov=ov)
