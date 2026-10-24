"""The Quillmere Lake basin for task482: eight towns' residents and everyone else present in them month by month (the
lodges' and the platforms' paid guests, the owners in their cottages, the residents' guests and the day visitors), the
treatment plants that carry all of them, one joint plant's member meters, the lodging returns and the two booking
platforms' bookings. Every file downstream is cut from these records."""
import calendar
import datetime as dt

import numpy as np

SEED = 48212
OFFICE = "Office of the State Demographer"
PROGRAM = "Seasonal Communities Aid"
PEOPLE = dict(lead="Marvin Jordan", estimates="William Terry", steward="Bryce Williams")
BASIN = "Quillmere Lake"
COUNTY = "Quillmere County"
APPROPRIATION = 2_400_000
THRESHOLD = 3.0
MY = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))        # the statute's measurement year
LODGE_START = dt.date(2024, 7, 1)                         # lodging returns and platform bookings from fiscal 2025
LODGE_END = dt.date(2026, 9, 30)
MOR_MONTHS = [(2025, m) for m in range(1, 13)] + [(2026, m) for m in range(1, 10)]
RATE_CHANGE = dt.date(2026, 1, 1)                         # the Lake Protection Fee per guest-night
RATES = (1.25, 1.50)
PLAT = ("Lakeward Stays", "Kettle & Pine")

# calendar-month shapes (January first) of each part of the people present, as shares of its summer peak
SHAPE = dict(
    lodge=np.array([.0015, .002, .001, .001, .25, .68, 1.0, .89, .46, .28, .06, .09]),
    plat=np.array([.002, .0025, .0015, .001, .22, .70, 1.0, .90, .42, .22, .05, .11]),
    own7=np.array([0, 0, 0, 0, .12, .55, 1.0, .82, .26, .07, .05, .03]),
    own8=np.array([0, 0, 0, 0, .10, .42, .76, 1.0, .31, .07, .05, .03]),
    vfr=np.array([.002, 0, 0, 0, .12, .52, 1.0, .74, .16, .05, .09, .26]),
    day=np.array([0, 0, 0, 0, .14, .58, 1.0, .86, .33, .15, 0, 0]),
)

# name, residents 1 July 2024/2025/2026, plant, peaks of lodge guests, platform guests, owners, residents' guests and
# day visitors (persons a day in the peak month, a day visitor at the share of the day spent), the owners' peak month,
# the plant's flow and BOD per person a day (gallons, pounds)
TOWNS = [
    ("Birchwick",     (1822, 1838, 1851), "BIR",  640,  860, 2780,  520, 260, 7, 61.0, 0.170),
    ("Teskadel",      (3869, 3884, 3902), "TES", 2350, 1250,  760,  880, 610, 7, 62.2, 0.171),
    ("Ruddmere",      (1188, 1193, 1197), "RUD",  210,  620, 2760,  350, 150, 8, 60.4, 0.169),
    ("Sorrelton",     (3021, 3036, 3052), "SOR", 5100, 1900,  420,  640, 610, 7, 61.6, 0.170),
    ("Pinehold",      (2214, 2398, 2411), "PIN",  500, 1890,  490,  430, 240, 7, 60.8, 0.169),
    ("Tamsen Point",  (3071, 3086, 3094), "TAM",  480,  610, 4840,  870, 410, 8, 61.9, 0.170),
    ("Esker Narrows", (1584, 1592, 1603), "NAR", 3700, 1330,  270,  340, 560, 7, 61.5, 0.171),
    ("Hollin Bay",    (2683, 2694, 2706), "NAR",  860, 2280,  400,  330, 220, 7, 61.5, 0.170),
]
NAMES = [t[0] for t in TOWNS]
PLANTS = dict(
    BIR=dict(name="Birchwick Wastewater Treatment Facility", permit="MN0099127", towns=["Birchwick"], kind="mechanical",
             layout="edmr"),
    TES=dict(name="Teskadel Wastewater Treatment Plant", permit="MN0099146", towns=["Teskadel"], kind="mechanical",
             layout="edmr"),
    RUD=dict(name="Ruddmere Wastewater Stabilization Ponds", permit="MNG589913", towns=["Ruddmere"], kind="pond",
             layout="workbook"),
    SOR=dict(name="Sorrelton Wastewater Treatment Plant", permit="MN0099158", towns=["Sorrelton"], kind="mechanical",
             layout="edmr"),
    PIN=dict(name="Pinehold Wastewater Stabilization Ponds", permit="MNG589927", towns=["Pinehold"], kind="pond",
             layout="workbook"),
    TAM=dict(name="Tamsen Point Wastewater Treatment Facility", permit="MN0099173", towns=["Tamsen Point"],
             kind="mechanical", layout="edmr"),
    NAR=dict(name="Narrows Joint Wastewater Treatment Plant", permit="MN0099181", towns=["Esker Narrows", "Hollin Bay"],
             kind="mechanical", layout="edmr"),
)


def days_in(y, m):
    return calendar.monthrange(y, m)[1]


def month_iter(a, b):
    y, m = a.year, a.month
    while (y, m) <= (b.year, b.month):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def year_factor(y, m):
    """Summer 2026 ran a little above summer 2025, and the seasons before July 2025 a little below."""
    return 1.03 if y == 2026 else 1.00 if (y, m) >= (2025, 7) else 0.97


def residents(town, y, m):
    res = TOWNS[NAMES.index(town)][1]
    return float(res[2] if y == 2026 else res[1] if y == 2025 else res[0])


# ------------------------------------------------------------------------------------------- the paid stays
LODGE_KINDS = (("Resort", 10, 34, 3.1), ("Lodge", 14, 48, 2.4), ("Motel", 12, 30, 2.0), ("Inn", 5, 14, 2.1),
               ("Campground", 24, 90, 3.4), ("Bed and breakfast", 3, 7, 1.9))


def lodges():
    """Each town's lodging properties: kind, rooms (or sites), persons per occupied unit, a peak occupancy, and a
    filing frequency (eight units or more file monthly)."""
    r = rng(201)
    out = []
    n_acct = 40118
    for t in TOWNS:
        n, H = t[0], t[3]
        props, cap = [], 0.0
        while cap < H:
            kind, lo, hi, ppr = LODGE_KINDS[int(r.choice(6, p=[.2, .16, .2, .14, .12, .18]))]
            units = int(r.integers(lo, hi + 1))
            occ = float(r.uniform(0.84, 0.95))
            props.append(dict(town=n, kind=kind, units=units, ppr=ppr * float(r.uniform(0.93, 1.07)), occ=occ))
            cap += units * occ * props[-1]["ppr"]
        scale = H / cap
        for p_ in props:
            p_["occ"] = min(0.99, p_["occ"] * scale) if scale < 1 else p_["occ"]
            n_acct += int(r.integers(3, 40))
            p_["account"] = "QL-%06d" % n_acct
            p_["freq"] = "monthly" if p_["units"] >= 8 else "quarterly"
        # rescale the units so the town's peak paid guests are H exactly
        tot = sum(p_["units"] * p_["occ"] * p_["ppr"] for p_ in props)
        for p_ in props:
            p_["ppr"] *= H / tot
        out.extend(props)
    return out


def lodge_nights(props):
    """Guest-nights by property and month, January 2025 to September 2026, with a share of stays of 30 nights or more
    (summer staff housed by the resorts and campgrounds) the fee exempts."""
    r = rng(211)
    out = {}
    for i, p_ in enumerate(props):
        for (y, m) in MOR_MONTHS:
            k = m - 1
            g = p_["units"] * p_["occ"] * p_["ppr"] * SHAPE["lodge"][k] * year_factor(y, m) * days_in(y, m)
            g *= 1 + r.normal(0, 0.035)
            exempt = 0.0
            if p_["kind"] in ("Resort", "Campground") and m in (6, 7, 8):
                exempt = g * float(r.uniform(0.02, 0.06))
            out[(i, y, m)] = (int(round(g)), int(round(exempt)))
    return out


def listings():
    """Each town's whole-home listings on the two platforms (about three in five on Lakeward Stays)."""
    r = rng(221)
    out = []
    lid = {0: 5810233, 1: 77120}
    for t in TOWNS:
        n, S = t[0], t[4]
        k = int(round(S / (0.86 * 4.3)))
        for _ in range(k):
            pl = 0 if r.random() < 0.6 else 1
            lid[pl] += int(r.integers(7, 400))
            out.append(dict(town=n, platform=pl, id=("LW%d" % lid[pl]) if pl == 0 else ("KP-%06d" % lid[pl]),
                            size=int(r.choice([2, 4, 4, 6, 6, 8, 10]))))
    return out


def bookings(lst):
    """Stays night by night, 1 December 2024 to 30 September 2026: a free listing is booked on a day with a hazard set
    by the month's occupancy, for a length and party drawn for the season; the platforms' records cut from these."""
    r = rng(231)
    start, end = dt.date(2024, 12, 1), dt.date(2026, 9, 30)
    out = []
    bid = 30000000
    for j, L in enumerate(lst):
        d = start
        while d <= end:
            k = d.month - 1
            o = 0.86 * SHAPE["plat"][k] * year_factor(d.year, d.month)
            summer = d.month in (6, 7, 8)
            mean_len = 6.4 if summer else 3.1
            h = min(0.98, o / (mean_len * max(0.03, 1 - o)))
            if r.random() < h:
                ln = max(1, int(round(r.normal(7 if summer else 3, 1.6 if summer else 1.3))))
                if not summer and r.random() < 0.012:
                    ln = int(r.integers(30, 92))          # a winter let of a month or more, which the fee exempts
                party = int(max(1, min(L["size"] + 2, round(r.normal(L["size"] * 0.78, 1.1)))))
                bid += int(r.integers(1, 90))
                out.append(dict(listing=j, id=bid, checkin=d, nights=ln, guests=party,
                                booked=d - dt.timedelta(days=int(r.integers(3, 160)))))
                d = d + dt.timedelta(days=ln + int(r.integers(0, 2)))
            else:
                d = d + dt.timedelta(days=1)
    return out


def platform_nights(lst, bk):
    """Guest-nights by town and month from the stays."""
    out = {}
    for b in bk:
        town = lst[b["listing"]]["town"]
        for i in range(b["nights"]):
            d = b["checkin"] + dt.timedelta(days=i)
            key = (town, d.year, d.month)
            out[key] = out.get(key, 0) + b["guests"]
    return out


_CACHE = {}


def build():
    if not _CACHE:
        props = lodges()
        ln = lodge_nights(props)
        lst = listings()
        bk = bookings(lst)
        pn = platform_nights(lst, bk)
        lodge_town = {}
        for (i, y, m), (g, ex) in ln.items():
            k = (props[i]["town"], y, m)
            lodge_town[k] = lodge_town.get(k, 0) + g
        _CACHE.update(props=props, lodge_nights=ln, listings=lst, bookings=bk, plat_nights=pn, lodge_town=lodge_town)
    return _CACHE


def parts(town, y, m):
    """The people present on an average day of the month, by part, for one town: the residents, the paid guests the
    lodges and the platforms recorded, and the owners, the residents' guests and the day visitors no record holds."""
    W = build()
    t = TOWNS[NAMES.index(town)]
    _, res, _, H, S, O, V, D, own_peak, _, _ = t
    k = m - 1
    f = year_factor(y, m)
    own = SHAPE["own7" if own_peak == 7 else "own8"]
    dd = days_in(y, m)
    return dict(residents=residents(town, y, m), lodge=W["lodge_town"].get((town, y, m), 0) / dd,
                plat=W["plat_nights"].get((town, y, m), 0) / dd, owners=O * own[k] * f, guests=V * SHAPE["vfr"][k] * f,
                day=D * SHAPE["day"][k] * f)


def present(town, y, m):
    return sum(parts(town, y, m).values())


def truth():
    """Each town's true average population present by month of the measurement year, its busiest month and ratio."""
    out = {}
    for t in TOWNS:
        n = t[0]
        months = list(month_iter(*MY))
        pres = {ym: present(n, *ym) for ym in months}
        best = max(months, key=lambda ym: pres[ym])
        res = t[1][2]
        paid = {ym: parts(n, *ym)["residents"] + parts(n, *ym)["lodge"] + parts(n, *ym)["plat"] for ym in months}
        out[n] = dict(present=pres, busiest=best, peak=pres[best], residents=res, ratio=pres[best] / res,
                      paid_peak=max(paid.values()))
    return out


def rng(k):
    return np.random.default_rng(SEED + k)


# ---------------------------------------------------------------------------------------------------- the plants
# monthly operating report noise: winter months are steadier than summer ones
def _noise(r, y, m, winter, summer):
    return r.normal(0, winter if m in (1, 2, 3, 4, 11, 12) else summer)


def plant_people(code, y, m):
    """People present on an average day of the month in the towns a plant serves, by town."""
    return {n: present(n, y, m) for n in PLANTS[code]["towns"]}


def mor():
    """Each plant's monthly operating report values, January 2025 to September 2026: the influent's average daily
    flow (MGD) and its BOD and TSS (mg/L, monthly composites), and the effluent's flow, BOD, TSS and total phosphorus,
    with the pond systems' controlled discharges (days discharged, or none). The joint plant's member meters read each
    town's monthly gallons."""
    out, meters = {}, {}
    r = rng(101)
    for code, pl in PLANTS.items():
        rows = []
        for (y, m) in MOR_MONTHS:
            pp = plant_people(code, y, m)
            flow_gpd, bod_lb, tss_lb = 0.0, 0.0, 0.0
            for n, ppl in pp.items():
                t = TOWNS[NAMES.index(n)]
                q, b = t[9], t[10]
                fq = 1 + _noise(r, y, m, 0.004, 0.007)
                gal = ppl * q * fq
                flow_gpd += gal
                bod_lb += ppl * b * (1 + _noise(r, y, m, 0.004, 0.006))
                tss_lb += ppl * b * 1.176 * (1 + _noise(r, y, m, 0.005, 0.007))
                if len(pp) > 1:
                    meters[(n, y, m)] = gal * days_in(y, m) * (1 + r.normal(0, 0.004))
            mgd = flow_gpd / 1e6
            conc = lambda lb: lb / (mgd * 8.34)
            rows.append(dict(y=y, m=m, inf_flow=mgd, inf_bod=conc(bod_lb), inf_tss=conc(tss_lb)))
        out[code] = rows
    eff = effluent(out)
    for code in out:
        for row, e in zip(out[code], eff[code]):
            row.update(e)
    return out, meters


def effluent(inf):
    """Effluent quality. Mechanical plants discharge every day; the stabilization ponds hold the year's wastewater and
    discharge only in spring and autumn drawdowns, so their reports carry no discharge in the other months. Every
    plant's effluent flow is the month's average daily flow over the days of the month."""
    r = rng(131)
    out = {}
    for code, rows in inf.items():
        kind = PLANTS[code]["kind"]
        e = []
        tp_base = dict(BIR=0.62, TES=0.71, SOR=0.55, TAM=0.83, NAR=0.66, RUD=1.9, PIN=2.2)[code]
        for row in rows:
            y, m = row["y"], row["m"]
            if kind == "mechanical":
                e.append(dict(eff_flow=row["inf_flow"] * (0.985 + r.normal(0, 0.004)),
                              eff_bod=max(3.0, 9.0 + r.normal(0, 2.2)), eff_tss=max(3.0, 10.5 + r.normal(0, 2.6)),
                              eff_tp=max(0.12, tp_base * (1 + r.normal(0, 0.12))), days=days_in(y, m)))
            else:
                if m in (4, 5, 6, 10, 11):
                    span = {4: (8, 14), 5: (10, 18), 6: (4, 9), 10: (9, 16), 11: (3, 8)}[m]
                    d = int(r.integers(span[0], span[1] + 1))
                    # the outlet's rate on the days it is open, reported as the month's average daily flow
                    rate = 0.79 + 0.16 * r.random() if code == "RUD" else 1.14 + 0.22 * r.random()
                    e.append(dict(eff_flow=rate * d / days_in(y, m),
                                  eff_bod=max(4.0, 14.0 + r.normal(0, 3)), eff_tss=max(5.0, 21.0 + r.normal(0, 5)),
                                  eff_tp=max(0.5, tp_base * (1 + r.normal(0, 0.15))), days=d))
                else:
                    e.append(dict(eff_flow=None, eff_bod=None, eff_tss=None, eff_tp=None, days=0))
        out[code] = e
    return out


if __name__ == "__main__":
    tr = truth()
    for n, v in tr.items():
        ms = sorted(v["present"], key=lambda ym: -v["present"][ym])
        second = v["present"][ms[1]]
        print("%-14s R %5d busiest %d-%02d peak %7.0f ratio %4.2f (2nd %d-%02d, margin %4.1f%%) paid-only ratio %4.2f"
              % (n, v["residents"], v["busiest"][0], v["busiest"][1], v["peak"], v["ratio"], ms[1][0], ms[1][1],
                 100 * (v["peak"] / second - 1), v["paid_peak"] / v["residents"]))
