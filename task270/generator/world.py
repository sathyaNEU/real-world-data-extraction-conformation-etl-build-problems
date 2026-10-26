"""The clean world for task270: Hallowmere's 72 stores and their refrigeration packs, each pack's refrigerant losing day
by day (a background weep, joints that start leaking and are found at a visit, the rare ruptured line), Kelbray's
routine rounds by region and its call-outs on Tarnley's low-level alarm, the charges weighed in and the receiver
levels read on arrival and departure, and Tarnley's daily mean receiver level. The truth the analysis has to recover
is each pack's refrigerant lost in 2026; nothing here is a defect, every record says what it says."""
import datetime as dt

import numpy as np
import pandas as pd

import common as K

DAYS = pd.date_range(K.START, K.END, freq="D")
ND = len(DAYS)
TOWNS = {
    "YOR": ["Skipton", "Keighley", "Ilkley", "Otley", "Harrogate", "Knaresborough", "Ripon", "Thirsk", "Northallerton",
            "Selby", "Tadcaster", "Wetherby", "Pontefract", "Castleford", "Goole", "Driffield", "Malton", "Pickering",
            "Whitby", "Settle", "Richmond", "Bedale"],
    "LAN": ["Clitheroe", "Garstang", "Kirkham", "Poulton", "Fleetwood", "Longridge", "Chorley", "Leyland", "Ormskirk",
            "Darwen", "Accrington", "Haslingden", "Rawtenstall", "Colne", "Nelson", "Barnoldswick", "Carnforth",
            "Morecambe", "Heysham", "Lytham"],
    "NE": ["Hexham", "Morpeth", "Alnwick", "Amble", "Blyth", "Cramlington", "Ponteland", "Prudhoe", "Consett",
           "Stanley", "Chester-le-Street", "Durham", "Spennymoor", "Crook", "Barnard Castle", "Seaham", "Peterlee",
           "Sedgefield"],
    "CUM": ["Kendal", "Windermere", "Ulverston", "Penrith", "Keswick", "Cockermouth", "Workington", "Whitehaven",
            "Wigton", "Brampton", "Appleby", "Sedbergh"],
}
# each region's routine rounds: (year, month) at which the round starts; a round runs over about three weeks
ROUNDS = {
    "YOR": [(2024, 3), (2024, 9), (2025, 4), (2025, 12), (2026, 3), (2026, 6)],
    "LAN": [(2024, 5), (2024, 11), (2025, 5), (2025, 11), (2026, 5)],          # the November 2026 round not run
    "NE": [(2024, 4), (2024, 10), (2025, 4), (2026, 1), (2026, 6), (2026, 11)],  # October 2025 run in January 2026
    "CUM": [(2024, 2), (2024, 8), (2025, 2), (2025, 8), (2026, 2), (2026, 8)],
}
LEAK_MEDIAN = {"YOR": 0.086, "LAN": 0.104, "NE": 0.068, "CUM": 0.076}   # background loss a year, share of charge
RECEIVER = {"YOR": (0.22, 0.30), "LAN": (0.65, 0.80), "NE": (0.38, 0.52), "CUM": (0.36, 0.5)}
ALARM = 25.0


def stores(rng):
    out, n = [], 0
    for reg in K.REGIONS:
        for town in TOWNS[reg]:
            n += 1
            opened = int(rng.choice([1988, 1993, 1997, 2001, 2004, 2008, 2011, 2014, 2017, 2020]))
            out.append(dict(store=n, town=town, region=reg, opened=opened, sqm=int(rng.integers(1400, 4200) // 10 * 10)))
    return pd.DataFrame(out)


def packs(rng, st):
    rows = []
    for s in st.itertuples(index=False):
        kinds = ["LT1", "MT1"] if s.sqm < 2600 else ["LT1", "MT1", "MT2"]
        if s.sqm < 1800 and rng.random() < 0.5:
            kinds = ["MT1"]
        for kind in kinds:
            lt = kind.startswith("LT")
            installed = max(s.opened, int(rng.choice([2006, 2009, 2012, 2015, 2018, 2021])))
            if installed < 2016:
                gas = "R404A" if rng.random() < 0.45 else str(rng.choice(["R448A", "R449A", "R407F"]))
            else:
                gas = str(rng.choice(["R448A", "R449A"]))
            charge = round(float(rng.choice([95, 110, 130, 150, 170, 190, 220, 250]) * (0.8 if lt else 1.0)
                                 * rng.uniform(0.94, 1.06)), 1)
            lo, hi = RECEIVER[s.region]
            rec = charge * rng.uniform(lo, hi)                     # kg the receiver's level span holds
            rows.append(dict(store=s.store, region=s.region, kind=kind, code="%03d/%s" % (s.store, kind), gas=gas,
                             charge=charge, installed=installed, k=100.0 / rec, full=float(rng.uniform(62, 76)),
                             rate=rng.lognormal(np.log(K_LEAK(s.region)), 0.55) * charge / 365.0))
    return pd.DataFrame(rows)


def K_LEAK(reg):
    return LEAK_MEDIAN[reg]


def round_days(rng, reg, n_packs):
    """each pack's routine visit day in each round of its region, spread over three weeks of working days"""
    out = []
    for (y, m) in ROUNDS[reg]:
        start = dt.date(y, m, 2)
        days = [start + dt.timedelta(days=i) for i in range(26)]
        days = [d for d in days if d.weekday() < 5 and not (d.month == 12 and d.day >= 22) and not
                (d.month == 1 and d.day <= 3)]
        out.append([days[int(rng.integers(0, len(days)))] for _ in range(n_packs)])
    return out


def simulate(seed=K.SEED):
    rng = np.random.default_rng(seed)
    st = stores(rng)
    pk = packs(rng, st)
    idx = {d.date(): i for i, d in enumerate(DAYS)}
    routine = {}
    for reg in K.REGIONS:
        sub = pk.index[pk.region == reg].tolist()
        for rnd in round_days(rng, reg, len(sub)):
            for p, d in zip(sub, rnd):
                routine.setdefault(p, set()).add(idx[d])
    retro, dec = schedules(seed, st, pk)
    jobs, levels, deficit = [], np.zeros((len(pk), ND)), np.zeros((len(pk), ND))
    jn = 41000
    for p, row in pk.iterrows():
        prng = np.random.default_rng([seed, 11, p])
        d = float(prng.uniform(0.0, 0.06)) * row.charge
        ev = 0.0
        alarm_since = None
        for t in range(ND):
            day = DAYS[t].date()
            if ev == 0.0 and prng.random() < 1 / 1300:
                ev = float(prng.lognormal(np.log(0.0014), 0.5)) * row.charge
            if prng.random() < 1 / 15000:
                d += float(prng.uniform(0.08, 0.18)) * row.charge
            d = min(d + float(prng.gamma(2.0, row.rate / 2.0)) + ev, 0.9 * row.charge)
            lev = row.full - row.k * d
            if lev < ALARM and alarm_since is None:
                alarm_since = t
            visit, jtype = None, None
            holiday = (day.month == 12 and day.day >= 24) or (day.month == 1 and day.day <= 2)
            if alarm_since is not None and ((not holiday and prng.random() < 0.35) or (lev < 14 and prng.random() < 0.6)):
                visit, jtype = True, "BREAKDOWN"
            elif t in routine.get(p, ()):
                visit, jtype = True, "ROUTINE"
            hour = float(prng.uniform(8.5, 16.5))
            if p in dec and day >= dec[p][0]:
                if day == dec[p][0]:
                    arr = float(np.clip(lev + prng.normal(0, 0.25), 0, 100))
                    jobs.append(dict(job=jn, pack=p, date=day, hour=hour, type="DECOMMISSIONING", charged=0.0,
                                     recovered=round(row.charge - d, 1), arr=round(arr, 1), dep=None, leak="N",
                                     d_before=d, d_after=row.charge, gas=retro.get(p, (0, row.gas))[1]))
                    jn += int(prng.integers(1, 4))
                levels[p, t] = np.nan
                deficit[p, t] = np.nan
                continue
            if p in retro and day == retro[p][0]:
                arr = float(np.clip(lev + prng.normal(0, 0.25), 0, 100))
                dep = float(np.clip(row.full + prng.normal(0, 0.25), 0, 100))
                jobs.append(dict(job=jn, pack=p, date=day, hour=hour, type="RETROFIT", charged=row.charge,
                                 recovered=round(row.charge - d, 1), arr=round(arr, 1), dep=round(dep, 1),
                                 leak="N", d_before=d, d_after=0.0, gas=retro[p][1]))
                jn += int(prng.integers(1, 4))
                frac = hour / 24.0
                levels[p, t] = frac * lev + (1 - frac) * row.full
                deficit[p, t] = 0.0
                d, ev, alarm_since = 0.0, 0.0, None
                continue
            if visit:
                found = ev > 0 or jtype == "BREAKDOWN"
                rec_kg = 0.0
                if found and prng.random() < 0.12:
                    rec_kg = round(float(prng.uniform(4, 18)), 1)    # a section recovered to change a component
                need = d if (d > 0.025 * row.charge or jtype == "BREAKDOWN") else 0.0
                charged = 0.0
                if need > 0 or rec_kg > 0:
                    charged = round(max(0.0, need * float(prng.uniform(0.985, 1.015)) + rec_kg
                                        + float(prng.normal(0, 0.15))), 1)
                arr = float(np.clip(lev + prng.normal(0, 0.25), 0, 100))
                d_after = max(0.0, d - (charged - rec_kg))
                dep = float(np.clip(row.full - row.k * d_after + prng.normal(0, 0.25), 0, 100))
                jobs.append(dict(job=jn, pack=p, date=day, hour=hour, type=jtype, charged=charged, recovered=rec_kg,
                                 arr=round(arr, 1), dep=round(dep, 1), leak="Y" if found else "N",
                                 d_before=d, d_after=d_after,
                                 gas=retro[p][1] if p in retro and day > retro[p][0] else row.gas))
                jn += int(prng.integers(1, 4))
                if ev > 0 and prng.random() < 0.88:
                    ev = 0.0
                frac = (hour - 0.0) / 24.0
                levels[p, t] = frac * lev + (1 - frac) * (row.full - row.k * d_after)
                deficit[p, t] = d_after
                d = d_after
                alarm_since = None
            else:
                levels[p, t] = lev
                deficit[p, t] = d
    noise = np.random.default_rng([seed, 23]).normal(0, 0.3, levels.shape)
    levels = np.clip(levels + noise, 0, 100)
    return dict(stores=st, packs=pk, jobs=pd.DataFrame(jobs), levels=levels, deficit=deficit, retro=retro, dec=dec)


def schedules(seed, st, pk):
    """the R404A packs retrofitted to a lower-GWP blend in 2024 and 2025 (day, new gas, register left stale) and the
    packs decommissioned in 2026 (day, why)"""
    rng = np.random.default_rng([seed, 29])
    town = dict(zip(st.town, st.store))
    dec = {}
    for reg, tn, kind, day, why in DECOMMISSIONS:
        for p in pk.index[(pk.store == town[tn]) & ((pk.kind == kind) | (kind == "*"))]:
            dec[p] = (day, why)
    retro = {}
    for p in pk.index[(pk.gas == "R404A")]:
        if p in dec or rng.random() > 0.45:
            continue
        day = dt.date(int(rng.choice([2024, 2025])), int(rng.integers(2, 11)), int(rng.integers(3, 26)))
        retro[p] = [day, str(rng.choice(["R448A", "R449A"])), bool(rng.random() < 0.3)]
    for reg in K.REGIONS:                      # the register left unchanged for at least one retrofit in each region
        mine = [p for p in retro if pk.loc[p, "region"] == reg]
        if mine and not any(retro[p][2] for p in mine):
            retro[mine[int(rng.integers(0, len(mine)))]][2] = True
    return {p: tuple(v) for p, v in retro.items()}, dec


def truth(w, year=K.YEAR):
    """each pack's refrigerant lost in the year: what was charged less what was recovered, plus what it was short at
    the year's end less what it was short at its start (end of the day before)"""
    pk, jb, de = w["packs"], w["jobs"], w["deficit"]
    pk = pk[~pk.index.isin(list(w.get("dec", {})))]
    jb = jb[jb.type.isin(["ROUTINE", "BREAKDOWN"])]
    j0 = DAYS.get_loc(pd.Timestamp(year - 1, 12, 31))
    j1 = DAYS.get_loc(pd.Timestamp(year, 12, 31))
    yr = jb[pd.to_datetime(jb.date).dt.year == year]
    net = (yr.charged - yr.recovered).groupby(yr.pack).sum().reindex(pk.index).fillna(0.0)
    loss = net + de[pk.index, j1] - de[pk.index, j0]
    return pd.DataFrame({"pack": pk.index, "region": pk.region, "charge": pk.charge, "net": net.values,
                         "loss": loss.values}).set_index("pack")


DECOMMISSIONS = [("CUM", "Cockermouth", "LT1", dt.date(2026, 4, 21), "CO2"), ("YOR", "Ripon", "MT1", dt.date(2026, 9, 8), "CO2"),
                 ("NE", "Seaham", "*", dt.date(2026, 10, 12), "CLOSED")]
CLOSED = {"Seaham": dt.date(2026, 10, 3)}


def extras(w, seed=K.SEED):
    """what sits beside the packs in the same records: the packs decommissioned in 2026 and the CO2 packs that replaced
    two of them, the R404A packs retrofitted to a lower-GWP blend in 2024 and 2025 (the register not updated for some),
    each store's integral cabinets and cold rooms with Kelbray's charges on them and the cylinders each charge came from"""
    rng = np.random.default_rng([seed, 31])
    st, pk, dec = w["stores"], w["packs"], w["dec"]
    co2 = []
    for p, (day, why) in dec.items():
        if why == "CO2":
            co2.append(dict(store=int(pk.loc[p, "store"]), kind=pk.loc[p, "kind"], since=day + dt.timedelta(days=2),
                            charge=round(float(rng.uniform(280, 420)), 1), full=float(rng.uniform(42, 52))))
    # integral cabinets and cold rooms
    eq, n = [], 0
    for s in st.itertuples(index=False):
        for i in range(max(10, s.sqm // 110)):
            n += 1
            yr = int(rng.integers(2008, 2026))
            gas = "R290" if yr >= 2018 else str(rng.choice(["R404A", "R134a"]))
            ch = round(float(rng.uniform(0.11, 0.15) if gas == "R290" else rng.uniform(0.35, 1.2)), 2)
            eq.append(dict(asset="C%04d" % n, store=s.store, region=s.region, type="Integral cabinet", gas=gas,
                           charge=ch, installed=yr))
        for i in range(int(rng.integers(2, 5))):
            n += 1
            yr = int(rng.integers(2006, 2025))
            gas = "R404A" if yr < 2015 else str(rng.choice(["R448A", "R449A"]))
            eq.append(dict(asset="R%04d" % n, store=s.store, region=s.region, type="Cold room", gas=gas,
                           charge=round(float(rng.uniform(2.5, 7.5)), 1), installed=yr))
    eq = pd.DataFrame(eq)
    # Kelbray's visits to cabinets and cold rooms: one visit may charge several assets of one store on one day
    vis, vno = [], 0
    for y in (2024, 2025, 2026):
        for s in st.itertuples(index=False):
            if s.town in CLOSED and y == 2026 and False:
                pass
            sub = eq[(eq.store == s.store) & (eq.gas != "R290")]
            nvis = int(rng.poisson(1.6 if y < 2026 else 1.8))
            for _ in range(nvis):
                day = dt.date(y, int(rng.integers(1, 13)), int(rng.integers(1, 28)))
                if s.town in CLOSED and day >= CLOSED[s.town]:
                    continue
                cold = sub[sub.type == "Cold room"]
                cab = sub[sub.type == "Integral cabinet"]
                gasv = str(rng.choice(sorted(set(sub.gas))))
                pick = []
                c1 = cold[cold.gas == gasv]
                if len(c1) and rng.random() < 0.7:
                    nn = min(len(c1), 2 if rng.random() < 0.45 else 1)
                    for _, a in c1.sample(nn, random_state=int(rng.integers(1e9))).iterrows():
                        pick.append(a)
                c2 = cab[cab.gas == gasv]
                for _ in range(int(rng.integers(0, 3))):
                    if len(c2):
                        pick.append(c2.sample(1, random_state=int(rng.integers(1e9))).iloc[0])
                if not pick:
                    continue
                vno += 1
                amounts = [round(float(a.charge * rng.uniform(0.15, 0.6)), 1) or 0.1 for a in pick]
                fits = len(pick) > 1 and round(sum(amounts), 1) <= min(a.charge for a in pick)
                vis.append(dict(visit=vno, store=s.store, region=s.region, date=day, gas=gasv,
                                assets=[a.asset for a in pick], kg=amounts, stamp_total=bool(fits and rng.random() < 0.7)))
    w.update(co2=co2, eq=eq, visits=vis)
    return w
