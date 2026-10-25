"""task485 world: eighteen permitted coal boilers in the Northern Priority Area over calendar 2026, day by day.

Each boiler fires coal from its site's yard; its wet limestone scrubber removes a share of the sulphur dioxide
while it runs and doses limestone at its operating ratio per mole removed; some scrubbers stand on bypass for
spells while their boilers fire, which no record carries. Deliveries, stocks, returns and tests are cut from
these daily flows, so every file the pack ships is a view of one world."""
import datetime as dt

import numpy as np

SEED = 485
YEAR = 2026
DAYS = 365
D0 = dt.date(YEAR, 1, 1)
MS, MSO2, MCACO3, MCO2, MC = 32.065, 64.066, 100.087, 44.010, 12.011
LINE = 250.0

SUPPLIERS = {
    # mean sulphur % as received, lot sd, ash %, total moisture %, carbon % ar, gross CV MJ/kg ar, lot tonnes
    "Ormthwaite Colliery": dict(s=1.08, sd=0.07, ash=13.6, tm=9.2, c=61.2, gcv=25.3, lot=(27.5, 31.5)),
    "Brisgarth Main Colliery": dict(s=2.14, sd=0.11, ash=16.1, tm=8.1, c=59.0, gcv=24.5, lot=(27.5, 31.5)),
    "Ostmouth Coal Imports": dict(s=0.71, sd=0.05, ash=11.2, tm=12.6, c=60.4, gcv=25.0, lot=(54.0, 60.0)),
    "Zellfold Fuels": dict(s=1.33, sd=0.09, ash=14.2, tm=10.1, c=60.1, gcv=24.8, lot=(27.5, 31.5)),
}
SUP_CODE = {"Ormthwaite Colliery": "OTC", "Brisgarth Main Colliery": "BGC", "Ostmouth Coal Imports": "OCI",
            "Zellfold Fuels": "ZFF"}

# site, firm, industry
SITES = [
    ("S01", "Quarholt Board Mills", "paper and board"),
    ("S02", "Eskfold Sugar", "sugar"),
    ("S03", "Dremstead Chemicals", "chemicals"),
    ("S04", "Ulvdale Dyeworks", "textiles"),
    ("S05", "Kirlgate Maltings", "malting"),
    ("S06", "Vornfield Brewery", "brewing"),
    ("S07", "Yeldholt General Hospital Energy Centre", "hospital campus"),
    ("S08", "Haskmouth Paper", "paper"),
    ("S09", "Nethstead Tissue", "tissue"),
    ("S10", "Pridwold Starch", "starch"),
    ("S11", "Lathgarth Fibres", "textiles"),
    ("S12", "Candrigg Soda Works", "chemicals"),
    ("S13", "Thalwold Foods", "food"),
    ("S14", "Sellhope Rubber", "rubber"),
    ("S15", "Umbgarth District Heating", "district heating"),
    ("S16", "Wendscar Tannery", "leather"),
]

# boiler roles fix the ladder; secondary parameters are drawn.  bypass: share of the year's sulphur fired that went
# to the stack on bypass; mix: supplier shares (by half-year where two are given); eff_on: mean removal while running
BOILERS = [
    dict(site="S01", unit=1, type="PF", mwth=97.4, cf=0.80, mix={"Brisgarth Main Colliery": 1.0},
         design=0.925, ratio=1.05, eff_on=0.962, bypass=0.0, role="beats"),
    dict(site="S01", unit=2, type="PF", mwth=58.9, cf=0.69, mix=None, design=0.95, ratio=1.05, eff_on=0.944,
         bypass=0.14, role="bypassed"),
    dict(site="S02", unit=1, type="stoker", mwth=52.4, cf=0.66, mix={"Zellfold Fuels": 1.0}, design=0.94, ratio=1.07,
         eff_on=0.936, bypass=0.0, role="plain"),
    dict(site="S03", unit=1, type="stoker", mwth=71.8, cf=0.71, mix={"Ormthwaite Colliery": 0.6, "Zellfold Fuels": 0.4},
         design=0.95, ratio=1.03, eff_on=0.943, bypass=0.205, role="bypassed"),
    dict(site="S04", unit=1, type="stoker", mwth=36.6, cf=0.64, mix={"Zellfold Fuels": 1.0}, design=0.94, ratio=1.07,
         eff_on=0.932, bypass=0.055, role="bypassed_under"),
    dict(site="S05", unit=1, type="stoker", mwth=28.4, cf=0.58, mix={"Ostmouth Coal Imports": 1.0}, design=0.93,
         ratio=1.05, eff_on=0.927, bypass=0.0, role="plain"),
    dict(site="S06", unit=1, type="PF", mwth=58.3, cf=0.62, mix={"Ormthwaite Colliery": 1.0}, design=0.95, ratio=1.05,
         eff_on=0.947, bypass=0.0, role="plain"),
    dict(site="S07", unit=1, type="PF", mwth=69.2, cf=0.62, mix={"Zellfold Fuels": 0.6, "Ormthwaite Colliery": 0.4},
         design=0.95, ratio=1.05, eff_on=0.945, bypass=0.0, role="plain"),
    dict(site="S08", unit=1, type="stoker", mwth=29.8, cf=0.67, mix={"Zellfold Fuels": 0.5, "Ormthwaite Colliery": 0.5},
         design=0.94, ratio=1.07, eff_on=0.934, bypass=0.0, role="plain"),
    dict(site="S09", unit=1, type="stoker", mwth=35.6, cf=0.68, mix={"Ormthwaite Colliery": 1.0}, design=0.94,
         ratio=1.03, eff_on=0.935, bypass=0.045, role="bypassed_under"),
    dict(site="S09", unit=2, type="PF", mwth=66.7, cf=0.66, mix=None, design=0.95, ratio=1.03, eff_on=0.946,
         bypass=0.0, role="plain"),
    dict(site="S10", unit=1, type="stoker", mwth=88.4, cf=0.78,
         mix=[(0, {"Ostmouth Coal Imports": 1.0}), (98, {"Brisgarth Main Colliery": 1.0}),
              (152, {"Ostmouth Coal Imports": 1.0})], design=0.94, ratio=1.05, eff_on=0.910, bypass=0.0,
         role="conc"),
    dict(site="S11", unit=1, type="stoker", mwth=38.6, cf=0.63, mix={"Ormthwaite Colliery": 1.0}, design=0.94,
         ratio=1.07, eff_on=0.936, bypass=0.0, role="plain"),
    dict(site="S12", unit=1, type="PF", mwth=98.2, cf=0.83, mix={"Brisgarth Main Colliery": 1.0}, design=0.93,
         ratio=1.05, eff_on=0.921, bypass=0.0, role="big"),
    dict(site="S13", unit=1, type="stoker", mwth=56.9, cf=0.69, mix={"Zellfold Fuels": 0.7, "Brisgarth Main Colliery": 0.3},
         design=0.94, ratio=1.03, eff_on=0.933, bypass=0.175, role="bypassed"),
    dict(site="S14", unit=1, type="stoker", mwth=40.2, cf=0.72, mix={"Zellfold Fuels": 1.0}, design=0.94, ratio=1.07,
         eff_on=0.934, bypass=0.35, role="bypassed"),
    dict(site="S15", unit=1, type="stoker", mwth=64.0, cf=0.61, mix={"Ormthwaite Colliery": 0.5, "Zellfold Fuels": 0.5},
         design=0.95, ratio=1.05, eff_on=0.944, bypass=0.28, role="bypassed"),
    dict(site="S16", unit=1, type="stoker", mwth=61.2, cf=0.73, mix={"Brisgarth Main Colliery": 0.5, "Zellfold Fuels": 0.5},
         design=0.94, ratio=1.03, eff_on=0.935, bypass=0.0, role="plain"),
]

QUARRIES = {"Bromscar Quarry": dict(caco3=96.1, sd=0.6), "Molhope Lime and Stone": dict(caco3=94.2, sd=0.8)}


class World:
    pass


def day(d):
    return D0 + dt.timedelta(days=int(d))


def stream(tag, *keys):
    """an independent random stream per module and entity, so a change to one boiler moves only its own draws"""
    return np.random.default_rng([SEED, tag] + [int(k) for k in keys])


def key(b):
    return int(b["site"][1:]), b["unit"]


def build(seed=SEED):
    w = World()
    sites = {s: dict(site=s, firm=f, industry=i) for s, f, i in SITES}
    B = [dict(b) for b in BOILERS]
    for b in B:
        b.update(sites[b["site"]])
        b["ash_ret"] = 0.02 if b["type"] == "PF" else 0.05
        b["id"] = "%s-%d" % (b["site"], b["unit"])
    # a second boiler on a site shares its unit 1's yard and supplier mix
    for b in B:
        if b["mix"] is None:
            b["mix"] = next(x["mix"] for x in B if x["site"] == b["site"] and x["unit"] == 1)
        if isinstance(b["mix"], dict):
            b["mix"] = [(0, b["mix"])]
    w.B, w.sites = B, sites
    t = np.arange(DAYS)
    # daily coal fired, t: rating MW x 86.4 GJ per MW-day x load / GCV MJ per kg
    for b in B:
        rng = stream(1, *key(b))
        mix = b["mix"][0][1]
        gcv = sum(sh * SUPPLIERS[s]["gcv"] for s, sh in mix.items())
        if b["industry"] in ("hospital campus", "district heating"):
            season = 1 + 0.22 * np.cos(2 * np.pi * (t - 18) / 365)
        elif b["industry"] == "sugar":
            season = np.where((t >= 268) | (t < 32), 1.42, 0.82)
        else:
            season = 1 + 0.05 * np.cos(2 * np.pi * (t - 30) / 365)
            season = season * np.where((t % 7) == 6, 0.86, 1.0)
        load = b["cf"] * season * rng.lognormal(0, 0.06, DAYS)
        stops = []
        for _ in range(int(rng.integers(1, 3))):
            s0 = int(rng.integers(20, DAYS - 20))
            stops.append((s0, int(rng.integers(4, 11))))
        for s0, n in stops:
            load[s0:s0 + n] = 0.0
        b["load"] = np.clip(load, 0, 1.0)
        b["stops"] = stops
        b["coal_day"] = b["mwth"] * 86.4 * b["load"] / gcv
    return w


def flows(w):
    """the scrubber's day: bypass hours while firing, removal while running, limestone dosed"""
    for b in w.B:
        rng = stream(11, *key(b))
        firing = b["coal_day"] > 0
        off = np.zeros(DAYS)
        spells = []
        if b["bypass"] > 0:
            # spells of 5 to 64 hours, never notified (the guidance asks only for planned outages in the return)
            s_gas = b["coal_day"] * b["s_day"] * (1 - b["ash_ret"])
            target = b["bypass"] * s_gas.sum()
            got = 0.0
            while got < target:
                hrs = float(rng.uniform(5, 64))
                start = float(rng.uniform(0, (DAYS - 3) * 24))
                h0, h1 = start, start + hrs
                add = 0.0
                trial = off.copy()
                for d in range(int(h0 // 24), int(h1 // 24) + 1):
                    a, z = max(h0, d * 24), min(h1, (d + 1) * 24)
                    if z > a and firing[d]:
                        new = min(1.0, trial[d] + (z - a) / 24)
                        add += (new - trial[d]) * s_gas[d]
                        trial[d] = new
                if add <= 0:
                    continue
                off = trial
                got += add
                spells.append((round(h0, 1), round(hrs, 1)))
        else:
            for _ in range(int(rng.integers(0, 3))):
                start = float(rng.uniform(0, (DAYS - 3) * 24))
                hrs = float(rng.uniform(1.5, 7))
                d = int(start // 24)
                if firing[d]:
                    off[d] = min(1.0, off[d] + hrs / 24)
                    spells.append((round(start, 1), round(hrs, 1)))
        b["off"], b["bypass_spells"] = off, sorted(spells)
        b["eff_day"] = np.clip(b["eff_on"] + rng.normal(0, 0.0035, DAYS), 0.88, 0.99)
        s_fired = b["coal_day"] * b["s_day"]
        s_gas = s_fired * (1 - b["ash_ret"])
        s_rem = s_gas * (1 - off) * b["eff_day"]
        b["S_fired_true"], b["S_gas_true"], b["S_rem_true"] = s_fired, s_gas, s_rem
        b["SO2_true"] = float((s_gas - s_rem).sum() * MSO2 / MS)
        b["caco3_day"] = s_rem / MS * b["ratio"] * MCACO3
        b["bypass_share_true"] = float(((s_gas * off).sum()) / s_gas.sum())


if __name__ == "__main__":
    import coal
    w = build()
    coal.deliveries(w)
    flows(w)
    for b in w.B:
        print("%-5s %-6s %5.1f coal %7.0f S %.2f%% byp %.3f SO2 %6.0f %s" % (
            b["id"], b["type"], b["mwth"], b["coal_day"].sum(), 100 * b["S_fired_true"].sum() / b["coal_day"].sum(),
            b["bypass_share_true"], b["SO2_true"], b["role"]))
