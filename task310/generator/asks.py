"""The supplementary asks' worlds and files, on populations the main call never reads:

A  eligible homes per region on 30 September 2026: Southmark's distributed energy resources register, its NMI
   standing data and the Battery Booster scheme's 2021 to 2023 claims;
B  the 2024 pilot batteries' energy delivered in each quarter of 2025: the battery maker's daily telemetry and the
   pilot site register;
C  2025 battery installations in each region by installers accredited for the programme through 2027: the
   accreditation register, the installation certificates and their amendments.

Each world is drawn on its own random stream, so the panel's physics never moves when an ask is edited."""
import datetime as dt

import numpy as np
import pandas as pd

import params as P

STREETS = ["Acacia", "Banksia", "Bottlebrush", "Wattle", "Ironbark", "Kurrajong", "Grevillea", "Jacaranda", "Waratah",
           "Melaleuca", "Callistemon", "Boronia", "Coolabah", "Brigalow", "Casuarina", "Lilly Pilly", "Myrtle",
           "Tallowwood", "Blackbutt", "Stringybark", "Kookaburra", "Rosella", "Lorikeet", "Currawong", "Magpie",
           "Pelican", "Heron", "Egret", "Ibis", "Brolga", "Jabiru", "Plover", "Curlew", "Kestrel", "Osprey",
           "Harbour View", "Ridgeline", "Hillcrest", "Valley View", "Riverside", "Parkland", "Seaview", "Sunrise",
           "Bellbird", "Wombat", "Echidna", "Possum", "Platypus", "Dingo", "Quokka", "Bilby", "Numbat"]
TYPES = [("Street", "ST"), ("Road", "RD"), ("Avenue", "AVE"), ("Crescent", "CRES"), ("Place", "PL"),
         ("Drive", "DR"), ("Court", "CT"), ("Parade", "PDE"), ("Close", "CL")]
# the network's suburbs by region (a postcode shared by two regions is told apart by suburb)
SUBURB_REGION = {
    "WEN": [("Coral Bay", "2587"), ("Pelican Heads", "2589"), ("Sandhaven", "2590"), ("Port Ellery", "2592"),
            ("Ellery Downs", "2592")],
    "BEL": [("Eastbrook", "2711"), ("Cedar Park", "2713"), ("Ashgrove", "2714"), ("Stonebridge South", "2716"),
            ("Eastbrook North", "2711")],
    "YAR": [("Yarrandale", "2804"), ("Mulga Flats", "2806"), ("Riverbend Estate", "2807"),
            ("Quarry Hill Estate", "2809"), ("Glenvale West", "2905")],
    "TAR": [("Tarrock", "2902"), ("Mount Ellis", "2904"), ("Glenvale", "2905"), ("Fernhill", "2907"),
            ("Stonebridge Hills", "2716")],
}
PREMISES = {"WEN": 8600, "BEL": 11200, "YAR": 6400, "TAR": 5800}
# Yarrandale Valley's homes are mostly in the two estates of its growth corridor
SUB_W = {"YAR": [0.06, 0.05, 0.45, 0.40, 0.04]}
CENSUS = dt.date(2026, 9, 30)
SOLAR_BY = dt.date(2025, 9, 30)          # solar connected by this date has run for the whole twelve months to the census
BOOSTER_NMI_FROM = dt.date(2022, 7, 1)
REG_MANDATORY = dt.date(2022, 7, 1)


def _d(rng, a, b):
    a, b = dt.date.fromisoformat(a), dt.date.fromisoformat(b)
    return a + dt.timedelta(days=int(rng.integers(0, (b - a).days + 1)))


# ---------------------------------------------------------------- A: eligible homes
def premises_world(panel=()):
    """Southmark's solar premises. The panel's homes are among them, with nothing recorded but their solar."""
    rng = np.random.default_rng([P.SEED, 101])
    prem = []
    taken = {h["nmi"] for h in panel}
    nmis = [n for n in ("4402%06d" % x for x in rng.choice(np.arange(10 ** 5, 10 ** 6), sum(PREMISES.values()) + 3400,
                                                            replace=False)) if n not in taken]
    k = 0
    for r in P.REGION_ORDER:
        subs = SUBURB_REGION[r]
        used = set()

        def address(sub, pc):
            while True:
                st = STREETS[int(rng.integers(0, len(STREETS)))]
                tp = TYPES[int(rng.integers(0, len(TYPES)))]
                num = int(rng.integers(1, 180))
                unit = int(rng.integers(1, 9)) if rng.random() < 0.12 else 0
                key = (pc, sub, st, tp[1], num, unit)
                if key not in used:
                    used.add(key)
                    return st, tp, num, unit
        for h in [h for h in panel if h["region"] == r]:
            st, tp, num, unit = address(h["suburb"], h["postcode"])
            prem.append(dict(region=r, suburb=h["suburb"], postcode=h["postcode"], street=st, stype=tp, num=num,
                             unit=unit, nmi=h["nmi"], pv_from=h["installed"], cls="RES", pv_kw=h["ac"], replaced_pv=None,
                             old_nmi=None, reissue=None, batteries=[], booster=None, panel=True))
        for j in range(PREMISES[r]):
            if r in SUB_W:
                sub, pc = subs[int(rng.choice(len(subs), p=SUB_W[r]))]
            else:
                sub, pc = subs[int(rng.integers(0, len(subs)))]
            st, tp, num, unit = address(sub, pc)
            nmi = nmis[k]
            k += 1
            estate = sub in ("Riverbend Estate", "Quarry Hill Estate")
            pv_from = _d(rng, "2023-07-01", "2026-06-30") if estate else _d(rng, "2009-03-01", "2026-08-31")
            if dt.date(2025, 9, 26) <= pv_from <= dt.date(2025, 10, 4):
                pv_from += dt.timedelta(days=9)          # no connection within days of the twelve-month line
            cls = "BUS" if rng.random() < 0.04 else "RES"
            prem.append(dict(region=r, suburb=sub, postcode=pc, street=st, stype=tp, num=num, unit=unit, nmi=nmi,
                             pv_from=pv_from, cls=cls,
                             pv_kw=round(float(rng.choice([1.5, 2.0, 3.0, 4.0, 5.0, 5.0, 6.6, 6.6, 8.0, 10.0])), 1),
                             replaced_pv=None, old_nmi=None, reissue=None, batteries=[], booster=None, panel=False))
    others = [p for p in prem if not p["panel"]]
    # system replacements (an older PV record decommissioned when the new system was commissioned)
    for p in others:
        if p["pv_from"] > dt.date(2016, 1, 1) and rng.random() < 0.09:
            p["replaced_pv"] = (_d(rng, "2009-01-01", (p["pv_from"] - dt.timedelta(days=400)).isoformat())
                                if p["pv_from"] > dt.date(2011, 2, 1) else None)
    # NMIs reissued after a switchboard upgrade: the old NMI is made extinct and its records decommissioned
    for p in others:
        if rng.random() < 0.035:
            p["old_nmi"] = p["nmi"]
            p["nmi"] = nmis[k]
            k += 1
            p["reissue"] = _d(rng, "2021-03-01", "2026-07-31")
    # Battery Booster batteries, 2021 to 2023
    for p in others:
        if p["cls"] == "RES" and p["pv_from"] < dt.date(2023, 6, 1) and rng.random() < 0.075:
            inst = _d(rng, "2021-02-01", "2023-11-30")
            inst = max(inst, p["pv_from"] + dt.timedelta(days=30))
            if inst > dt.date(2023, 12, 20):
                continue
            notified = inst >= REG_MANDATORY or rng.random() < 0.30
            removed = _d(rng, "2024-03-01", "2026-06-30") if rng.random() < 0.07 else None
            p["batteries"].append(dict(inst=inst, kwh=float(rng.choice([6.5, 9.8, 10.0, 13.5])), registered=notified,
                                       removed=removed, booster=True))
            p["booster"] = inst
    # other batteries outside 2025, registered at commissioning (2025's come from the installation certificates)
    for p in others:
        if not p["batteries"] and rng.random() < 0.045:
            inst = _d(rng, "2022-07-15", "2025-09-20")
            if inst.year == 2025:
                inst = inst + dt.timedelta(days=365)
            if inst < p["pv_from"]:
                continue
            p["batteries"].append(dict(inst=inst, kwh=float(rng.choice([5.0, 10.0, 13.5, 16.0])), registered=True,
                                       removed=None, booster=False))
    return prem


def _std_addr(p):
    base = "%d %s %s" % (p["num"], p["street"].upper(), p["stype"][1])
    return ("%d/%s" % (p["unit"], base)) if p["unit"] else base


def _claim_addr(p, rng):
    st = "%d %s %s" % (p["num"], p["street"], p["stype"][0])
    if p["unit"]:
        return ("Unit %d, %s" % (p["unit"], st)) if rng.random() < 0.7 else ("%d/%s" % (p["unit"], st))
    return st


def der_register(prem):
    rows = []
    for p in prem:
        cur, old = p["nmi"], p["old_nmi"]
        if p["replaced_pv"]:
            n0 = old if (old and p["reissue"] > p["pv_from"]) else cur
            rows.append([n0, p["region"], p["postcode"], "PV", round(p["pv_kw"] * 0.6, 1), p["replaced_pv"].isoformat(),
                         "Decommissioned", p["pv_from"].isoformat(), p["cls"]])
        if old:
            if p["reissue"] > p["pv_from"]:
                rows.append([old, p["region"], p["postcode"], "PV", p["pv_kw"], p["pv_from"].isoformat(), "Decommissioned",
                             p["reissue"].isoformat(), p["cls"]])
                rows.append([cur, p["region"], p["postcode"], "PV", p["pv_kw"], p["reissue"].isoformat(), "Active", "",
                             p["cls"]])
            else:
                rows.append([cur, p["region"], p["postcode"], "PV", p["pv_kw"], p["pv_from"].isoformat(), "Active", "",
                             p["cls"]])
        else:
            rows.append([cur, p["region"], p["postcode"], "PV", p["pv_kw"], p["pv_from"].isoformat(), "Active", "", p["cls"]])
        for b in p["batteries"]:
            if not b["registered"]:
                continue
            n = old if (old and p["reissue"] > b["inst"]) else cur
            if b["removed"]:
                rows.append([n, p["region"], p["postcode"], "BESS", b["kwh"], b["inst"].isoformat(), "Decommissioned",
                             b["removed"].isoformat(), p["cls"]])
            else:
                if old and p["reissue"] > b["inst"]:
                    rows.append([old, p["region"], p["postcode"], "BESS", b["kwh"], b["inst"].isoformat(),
                                 "Decommissioned", p["reissue"].isoformat(), p["cls"]])
                    rows.append([cur, p["region"], p["postcode"], "BESS", b["kwh"], p["reissue"].isoformat(), "Active", "",
                                 p["cls"]])
                else:
                    rows.append([n, p["region"], p["postcode"], "BESS", b["kwh"], b["inst"].isoformat(), "Active", "",
                                 p["cls"]])
    df = pd.DataFrame(rows, columns=["nmi", "network_region", "postcode", "der_type", "capacity", "commissioned",
                                     "status", "status_date", "customer_class"])
    df["network_region"] = df.network_region.map(P.REGIONS)
    df["capacity_unit"] = np.where(df.der_type == "PV", "kW", "kWh")
    df = df[["nmi", "network_region", "postcode", "customer_class", "der_type", "capacity", "capacity_unit",
             "commissioned", "status", "status_date"]]
    return df.sort_values(["nmi", "der_type", "commissioned"], kind="mergesort").reset_index(drop=True)


def standing_data(prem):
    rows = []
    for p in prem:
        a = _std_addr(p)
        rows.append([p["nmi"], a, p["suburb"].upper(), p["postcode"], "Active", p["old_nmi"] or ""])
        if p["old_nmi"]:
            rows.append([p["old_nmi"], a, p["suburb"].upper(), p["postcode"], "Extinct", ""])
    df = pd.DataFrame(rows, columns=["nmi", "address", "suburb", "postcode", "nmi_status", "previous_nmi"])
    return df.sort_values("nmi").reset_index(drop=True)


def booster_claims(prem):
    rng = np.random.default_rng([P.SEED, 103])
    rows = []
    n = 0
    for p in prem:
        if not p["booster"]:
            continue
        b = [x for x in p["batteries"] if x["booster"]][0]
        lodged = b["inst"] + dt.timedelta(days=int(rng.integers(3, 40)))
        nmi_at = ""
        if lodged >= BOOSTER_NMI_FROM:
            nmi_at = p["old_nmi"] if (p["old_nmi"] and p["reissue"] > lodged) else p["nmi"]
        n += 1
        rows.append(["", lodged, b["inst"], _claim_addr(p, rng),
                     p["suburb"], p["postcode"], nmi_at, b["kwh"], "Paid", lodged + dt.timedelta(days=int(rng.integers(20, 75)))])
    # rejected and withdrawn claims at premises that never received a rebate
    pool = [p for p in prem if not p["booster"] and p["cls"] == "RES"]
    for i in rng.choice(len(pool), 230, replace=False):
        p = pool[i]
        lodged = _d(rng, "2021-02-10", "2023-12-15")
        nmi_at = p["nmi"] if lodged >= BOOSTER_NMI_FROM and not (p["old_nmi"] and p["reissue"] > lodged) else \
            (p["old_nmi"] if lodged >= BOOSTER_NMI_FROM else "")
        n += 1
        st = "Rejected" if rng.random() < 0.7 else "Withdrawn"
        rows.append(["", lodged, lodged - dt.timedelta(days=9),
                     _claim_addr(p, rng), p["suburb"], p["postcode"], nmi_at,
                     float(rng.choice([6.5, 9.8, 10.0, 13.5])), st, None])
    df = pd.DataFrame(rows, columns=["claim_ref", "lodged", "battery_installed", "premises_address", "suburb", "postcode",
                                     "nmi", "battery_kwh", "status", "paid"])
    df = df.sort_values("lodged", kind="mergesort").reset_index(drop=True)
    # claim references run in lodgement order, shared with the scheme's other rebate streams
    df["claim_ref"] = ["BB-%05d" % x for x in 10213 + np.cumsum(rng.integers(1, 7, len(df)))]
    return df


def solar_start(p):
    """When solar was first connected at the premises: a replaced system ran until its successor was commissioned."""
    return p["replaced_pv"] or p["pv_from"]


def eligible_truth(prem):
    out = {r: 0 for r in P.REGION_ORDER}
    for p in prem:
        if p["cls"] != "RES" or solar_start(p) > SOLAR_BY:
            continue
        has_bat = any(b["inst"] <= CENSUS and not (b["removed"] and b["removed"] <= CENSUS) for b in p["batteries"]
                      if b["registered"])
        if has_bat or p["booster"]:
            continue
        out[p["region"]] += 1
    return out


# ---------------------------------------------------------------- B: the pilot batteries' telemetry
QUARTERS = [(dt.date(2025, 1, 1), dt.date(2025, 3, 31)), (dt.date(2025, 4, 1), dt.date(2025, 6, 30)),
            (dt.date(2025, 7, 1), dt.date(2025, 9, 30)), (dt.date(2025, 10, 1), dt.date(2025, 12, 31))]


def pilot_world(skies):
    """The 2024 pilot: 600 batteries in Sandhaven Coast and Eastbrook Metro. Most homes have one battery; some have two,
    either a Duo (two units behind one battery meter, every unit's daily report carrying that meter's energy) or two
    units each metered on its own. Every battery delivers energy every day of 2025 whether or not the maker's cloud
    heard from it."""
    rng = np.random.default_rng([P.SEED, 221])
    sites = []
    serials = list(rng.choice(np.arange(10 ** 6, 10 ** 7), 700, replace=False))
    for r in ("WEN", "BEL"):
        kd = skies[r]["k"].reshape(365, 48).mean(axis=1)
        clear = np.clip((kd - 0.12) / 0.55, 0, 1.25)
        kinds = list(rng.permutation(["single"] * 266 + ["duo"] * 12 + ["pair"] * 5))
        for kind in kinds:
            fitted = _d(rng, "2024-03-04", "2024-11-29")
            a = float(rng.uniform(0.55, 1.0))
            if kind == "single":
                need = float(rng.uniform(5.5, 11.0))
                d = np.minimum(9.5 * a * clear * rng.normal(1.0, 0.08, 365), need * rng.normal(1.0, 0.07, 365))
                meters = [np.clip(d, 0, 9.5)]
            else:
                need = float(rng.uniform(7.5, 12.5))
                tot = np.minimum(19.0 * a * clear * rng.normal(1.0, 0.08, 365), need * rng.normal(1.0, 0.07, 365))
                if kind == "duo":
                    meters = [np.clip(tot, 0, 19.0)]
                else:
                    sh = float(rng.uniform(0.42, 0.58))
                    meters = [np.clip(tot * sh * rng.normal(1.0, 0.04, 365), 0, 9.5),
                              np.clip(tot * (1 - sh) * rng.normal(1.0, 0.04, 365), 0, 9.5)]
            meters = [np.round(np.clip(m, 0, None) * 1000).astype(int) for m in meters]      # Wh a day
            units = ["NV10-%07d" % serials.pop(0) for _ in range(1 if kind == "single" else 2)]
            sites.append(dict(site=None, region=r, fitted=fitted, kind=kind, units=units, meters=meters,
                              counter0=[int(rng.integers(900_000, 2_400_000)) for _ in meters], swap=None, outages=[]))
    ids = rng.choice(np.arange(1000, 9999), len(sites), replace=False)
    for s_, i in zip(sites, ids):
        s_["site"] = "PLT-%04d" % i
    # warranty swaps during 2025 on single-battery homes: the new battery reports under its own serial, counter from zero
    singles = [i for i, s_ in enumerate(sites) if s_["kind"] == "single"]
    for i in rng.choice(singles, 6, replace=False):
        sites[i]["swap"] = (int(rng.integers(50, 300)), "NV10-%07d" % serials.pop(0))
    # cloud outages: no daily rows for the home's batteries; they keep working and their counters carry the energy
    bounds = [0, 89, 90, 180, 181, 272, 273, 364]
    for s_ in sites:
        for _ in range(int(rng.choice([0, 0, 1, 1, 2, 3]))):
            ln = int(rng.integers(2, 11))
            st = int(rng.integers(3, 360 - ln))
            if any(st - 2 <= b <= st + ln + 1 for b in bounds):
                continue
            if s_["swap"] and st - 3 <= s_["swap"][0] <= st + ln + 3:
                continue
            if any(not (st + ln + 2 < a or a + l2 + 2 < st) for a, l2 in s_["outages"]):
                continue
            s_["outages"].append((st, ln))
    return sites


def telemetry(sites):
    rng = np.random.default_rng([P.SEED, 203])
    rows = []
    upload = 50211
    for s_ in sites:
        off = set()
        for st, ln in s_["outages"]:
            off.update(range(st, st + ln))
        # the reporting streams: one per unit, each fed by its meter (a Duo's two units by the one meter)
        streams = []
        for j, u in enumerate(s_["units"]):
            m = 0 if len(s_["meters"]) == 1 else j
            streams.append(dict(serial=u, meter=m, buffer=[]))
        counters = list(s_["counter0"])
        for d in range(365):
            date = dt.date(2025, 1, 1) + dt.timedelta(days=d)
            if s_["swap"] and d == s_["swap"][0]:
                streams[0]["serial"], counters[0] = s_["swap"][1], 0
            for m in range(len(counters)):
                counters[m] += int(s_["meters"][m][d])
            if d in off:
                continue
            resend = (d - 1) in off
            if resend:
                upload += 1
            for st_ in streams:
                if resend and st_["buffer"]:
                    for b in st_["buffer"][-int(rng.integers(2, 4)):]:
                        rows.append(b[:6] + [upload])
                e = int(s_["meters"][st_["meter"]][d])
                soc = int(np.clip(rng.normal(22 if e > (12000 if s_["kind"] == "duo" else 6000) else 40, 12), 0, 100))
                row = [st_["serial"], date.isoformat(), e, int(round(e / (P.BAT_CHARGE_EFF * P.BAT_DISCHARGE_EFF))),
                       counters[st_["meter"]], soc, upload]
                rows.append(row)
                st_["buffer"].append(list(row))
                st_["buffer"] = st_["buffer"][-4:]
            upload += 1 if d % 29 == 0 else 0
    df = pd.DataFrame(rows, columns=["battery_serial", "date", "discharged_wh", "charged_wh", "lifetime_discharged_wh",
                                     "soc_end_pct", "upload_batch"])
    return df


def pilot_register(sites):
    rows = []
    for s_ in sites:
        for j, u in enumerate(s_["units"]):
            if j == 0 and s_["swap"]:
                d = (dt.date(2025, 1, 1) + dt.timedelta(days=s_["swap"][0])).isoformat()
                rows.append([s_["site"], P.REGIONS[s_["region"]], s_["fitted"].isoformat(), u, d, "warranty replacement"])
                rows.append([s_["site"], P.REGIONS[s_["region"]], d, s_["swap"][1], "", "replacement unit"])
            else:
                rows.append([s_["site"], P.REGIONS[s_["region"]], s_["fitted"].isoformat(), u, "", ""])
    df = pd.DataFrame(rows, columns=["site_id", "region", "fitted", "battery_serial", "removed", "note"])
    return df.sort_values(["region", "site_id", "fitted"], kind="mergesort").reset_index(drop=True)


def pilot_truth(sites):
    out = []
    for a, b in QUARTERS:
        i, j = (a - dt.date(2025, 1, 1)).days, (b - dt.date(2025, 1, 1)).days
        out.append(sum(int(m[i:j + 1].sum()) for s_ in sites for m in s_["meters"]) / 1e6)       # MWh
    return out


# ---------------------------------------------------------------- C: installers and their 2025 certificates
RENUMBER = dt.date(2025, 8, 1)
ROUND_END = dt.date(2027, 12, 31)


# installers whose trading name places them work from that region
LOCAL = {"Coastline Solar & Storage": "WEN", "Harbour Electrical Services": "WEN", "Valley Energy Solutions": "YAR",
         "Highland Electrics": "TAR", "Tarrock Solar Centre": "TAR", "Metro Battery Installers": "BEL"}


def installer_world(prem):
    rng = np.random.default_rng([P.SEED, 301])
    firms = []
    names = ["Coastline Solar & Storage", "Brightside Electrical", "Southside Solar & Electrical", "Greenway Power",
             "Sunridge Installations", "Harbour Electrical Services", "Ridgeline Solar", "Outback Battery Co",
             "Valley Energy Solutions", "Highland Electrics", "Tarrock Solar Centre", "Metro Battery Installers",
             "Eastwind Electrical", "Bluegum Energy", "Firetail Solar", "Mallee Power Systems", "Kestrel Electrical",
             "Banksia Energy", "Pelican Solar", "Wattle Electrical Group", "Bright Spark Electrical",
             "Clearsky Solar", "Ironbark Energy", "Jacaranda Electrical", "Lighthouse Solar", "Northgate Power",
             "Oakbridge Energy", "Paddock Solar", "Quandong Electrical", "Redgum Solar & Batteries", "Saltbush Energy",
             "Tasman Electrical", "Upland Solar", "Verandah Energy", "Windmill Electrical", "Yellowbox Solar",
             "Zircon Power", "Acorn Electrical", "Bayside Batteries", "Copperhead Electrical", "Dunes Solar",
             "Eucalypt Energy", "Fernleaf Electrical", "Granite Solar", "Hearth Energy", "Island Electrical",
             "Junction Solar", "Kiln Power"]
    a_nums = rng.choice(np.arange(10000, 99999), len(names), replace=False)
    s_nums = rng.choice(np.arange(500000, 599999), len(names) + 10, replace=False)
    for i, nm in enumerate(names):
        since = _d(rng, "2012-01-01", "2025-11-30")
        old = ("A%05d" % a_nums[i]) if since < RENUMBER else ""
        new = "S%06d" % s_nums[i]
        u = rng.random()
        if u < 0.62:
            expires, status = _d(rng, "2028-01-31", "2029-12-31"), "Current"
        elif u < 0.80:
            expires, status = _d(rng, "2026-12-01", "2027-11-30"), "Current"
        elif u < 0.90:
            expires, status = _d(rng, "2028-02-01", "2029-06-30"), "Suspended"
        else:
            expires, status = _d(rng, "2025-10-01", "2026-08-31"), "Lapsed"
        home = P.REGION_ORDER[int(rng.choice(4, p=[0.29, 0.31, 0.19, 0.21]))]
        home = LOCAL.get(nm, home)
        firms.append(dict(name=nm, old=old, new=new, since=since, expires=expires, status=status, home=home,
                          rate=float(rng.uniform(12, 80))))
    return firms


def _num(f, when):
    """The accreditation number an installer quoted on a form dated `when`."""
    return f["old"] if (f["old"] and when < RENUMBER) else f["new"]


NEIGHBOURS = {"WEN": 5, "BEL": 5, "YAR": 4, "TAR": 5}
RELODGED = {"WEN": 14, "BEL": 16, "YAR": 12, "TAR": 10}
PROCESSED = {"WEN": 4, "BEL": 4, "YAR": 4, "TAR": 3}
MAKERS = [("Norvane NV%d", 5.0, (1, 3)), ("Corvessa CV %.1f", 3.2, (2, 4)), ("Halvexa HX %.1f", 2.4, (3, 5))]


def certificates(firms, prem):
    """2025 installations and their certificates. A job is one battery fitted at one home; its certificate lists each
    module. Some jobs were lodged a second time (a portal error or a resubmission) and most second lodgements were
    never audited, so both certificates stand; where the scheme did process one, the first certificate was withdrawn.
    Neighbouring jobs fitted by one installer on one day in one suburb are separate installations. Every job that
    stands puts its battery on Southmark's register at commissioning."""
    rng = np.random.default_rng([P.SEED, 303])
    pool = {r: [p for p in prem if p["region"] == r and not p["panel"] and not p["batteries"]] for r in P.REGION_ORDER}
    chosen = set()
    seen_mods = set()

    def modules(n):
        out = []
        while len(out) < n:
            m = "M%09d" % rng.integers(10 ** 8, 10 ** 9)
            if m not in seen_mods:
                seen_mods.add(m)
                out.append(m)
        return out

    def home(r, inst, sub=None):
        cand = pool[r] if sub is None else [p for p in pool[r] if (p["suburb"], p["postcode"]) == sub]
        for _ in range(400):
            p = cand[int(rng.integers(0, len(cand)))]
            if id(p) not in chosen and p["pv_from"] <= inst:
                chosen.add(id(p))
                return p
        return None
    jobs = []
    for f in firms:
        if f["since"] > dt.date(2025, 12, 31):
            continue
        k = int(rng.poisson(f["rate"]))
        for _ in range(k):
            inst = _d(rng, max(f["since"], dt.date(2025, 1, 1)).isoformat(), "2025-12-31")
            if f["status"] == "Lapsed" and inst > f["expires"]:
                continue
            r = f["home"] if rng.random() < 0.85 else P.REGION_ORDER[int(rng.integers(0, 4))]
            p = home(r, inst)
            if p is None:
                continue
            mk = MAKERS[int(rng.choice([0, 0, 1, 2]))]
            mods = int(rng.integers(mk[2][0], mk[2][1] + 1))
            lodged = inst + dt.timedelta(days=int(rng.integers(1, 21)))
            jobs.append(dict(firm=f, region=r, prem=p, suburb=p["suburb"], postcode=p["postcode"], inst=inst,
                             model=mk[0] % (mk[1] * mods), mkwh=mk[1],
                             mods=modules(mods), neighbour=False,
                             certs=[dict(lodged=lodged, inst=inst, withdrawn=False, moved_to=None)]))
    base = len(jobs)
    # neighbours: the same installer fitting a second home in the same suburb on the same day
    near = [int(i) for r in P.REGION_ORDER
            for i in rng.choice([k for k in range(base) if jobs[k]["region"] == r], NEIGHBOURS[r], replace=False)]
    for i in near:
        j = jobs[i]
        p = home(j["region"], j["inst"], (j["suburb"], j["postcode"]))
        if p is None:
            continue
        lodged = j["certs"][0]["lodged"] + dt.timedelta(days=int(rng.integers(0, 2)))
        jobs.append(dict(j, prem=p, mods=modules(len(j["mods"])), neighbour=True,
                         certs=[dict(lodged=lodged, inst=j["inst"], withdrawn=False, moved_to=None)]))
    # second lodgements of the same job; fifteen were processed and their first certificate withdrawn
    pick, proper = [], set()
    for r in P.REGION_ORDER:
        sel = [int(i) for i in rng.choice([k for k in range(base) if jobs[k]["region"] == r], RELODGED[r], replace=False)]
        pick += sel
        proper |= set(sel[RELODGED[r] - PROCESSED[r]:])
    for i in pick:
        c0 = jobs[i]["certs"][0]
        inst2 = c0["inst"]
        if rng.random() < 0.4:
            inst2 = min(max(inst2 + dt.timedelta(days=int(rng.choice([-2, -1, 1, 2]))), dt.date(2025, 1, 1)),
                        dt.date(2025, 12, 31))
        c1 = dict(lodged=c0["lodged"] + dt.timedelta(days=int(rng.integers(25, 71))), inst=inst2, withdrawn=False,
                  moved_to=None)
        jobs[i]["certs"].append(c1)
        if i in proper:
            c0["withdrawn"] = True
            c0["withdrawn_on"] = c1["lodged"] + dt.timedelta(days=int(rng.integers(0, 6)))
    # certificate numbers run in lodgement order, shared with the scheme's other certificate types
    order = sorted((c["lodged"], ji, ci) for ji, j in enumerate(jobs) for ci, c in enumerate(j["certs"]))
    no = 418207
    for _, ji, ci in order:
        no += int(rng.integers(1, 9))
        jobs[ji]["certs"][ci]["no"] = "BIC-%07d" % no
    # amendments on singly lodged certificates: withdrawals, and certificates corrected to the installer who did the work
    single = [ji for ji, j in enumerate(jobs) if len(j["certs"]) == 1]
    am = []
    for ji in rng.choice(single, 64, replace=False):
        c = jobs[ji]["certs"][0]
        when = c["lodged"] + dt.timedelta(days=int(rng.integers(20, 90)))
        if rng.random() < 0.6:
            c["withdrawn"] = True
            am.append([c["no"], when.isoformat(), "withdrawn", ""])
        else:
            f2 = firms[int(rng.integers(0, len(firms)))]
            if f2["since"] > c["inst"] or f2 is jobs[ji]["firm"]:
                continue
            c["moved_to"] = f2
            am.append([c["no"], when.isoformat(), "installer corrected", _num(f2, when)])
    for ji in sorted(proper):
        c0 = jobs[ji]["certs"][0]
        am.append([c0["no"], c0["withdrawn_on"].isoformat(), "withdrawn", ""])
    rows = []
    for j in jobs:
        for c in j["certs"]:
            for m in j["mods"]:
                rows.append([c["no"], c["inst"].isoformat(), c["lodged"].isoformat(), j["suburb"], j["postcode"],
                             _num(j["firm"], c["lodged"]), j["model"], m, j["mkwh"]])
        # the battery of a job that stands is commissioned on Southmark's network once the installer notifies it,
        # days to weeks after the installation; a few installers never notify
        if any(not c["withdrawn"] for c in j["certs"]):
            j["prem"]["batteries"].append(dict(inst=j["inst"] + dt.timedelta(days=int(rng.integers(0, 22))),
                                               kwh=round(j["mkwh"] * len(j["mods"]), 1),
                                               registered=bool(rng.random() < 0.93), removed=None, booster=False))
    df = pd.DataFrame(rows, columns=["certificate_no", "installed", "lodged", "suburb", "postcode",
                                     "installer_accreditation", "battery_model", "module_serial", "module_kwh"])
    df = df.sort_values(["certificate_no", "module_serial"], kind="mergesort").reset_index(drop=True)
    am = pd.DataFrame(am, columns=["certificate_no", "amended_on", "amendment", "new_value"])
    am = am.sort_values(["amended_on", "certificate_no"], kind="mergesort").reset_index(drop=True)
    return df, am, jobs


def ask_worlds(w):
    """Every ask's world, drawn in the order the files depend on: the premises (with the panel's homes), the installers
    and their 2025 jobs (whose batteries reach the premises before the register is written), and the pilot."""
    panel = [dict(nmi=h["nmi"], region=h["region"], suburb=h["suburb"], postcode=h["postcode"],
                  installed=dt.date.fromisoformat(h["installed"]), ac=h["ac"]) for h in w["homes"]]
    prem = premises_world(panel)
    firms = installer_world(prem)
    certs, am, jobs = certificates(firms, prem)
    sites = pilot_world(w["skies"])
    return dict(prem=prem, firms=firms, certs=certs, am=am, jobs=jobs, sites=sites)


def accreditation_register(firms):
    rows = []
    for f in firms:
        rows.append([f["new"], f["old"], f["name"], f["since"].isoformat(), f["expires"].isoformat(), f["status"]])
    return pd.DataFrame(rows, columns=["accreditation_no", "previous_no", "business_name", "accredited_from", "expires",
                                       "status"]).sort_values("accreditation_no").reset_index(drop=True)


def installs_truth(jobs):
    out = {r: 0 for r in P.REGION_ORDER}
    for j in jobs:
        live = [c for c in j["certs"] if not c["withdrawn"]]
        if not live:
            continue
        f = live[-1]["moved_to"] or j["firm"]
        if f["status"] == "Current" and f["expires"] >= ROUND_END:
            out[j["region"]] += 1
    return out
