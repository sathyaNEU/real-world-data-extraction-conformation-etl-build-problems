"""The golden from the shipped pack alone (the first solver), with the rungs and the licensed family beside it.

    python3 task484/generator/golden.py          (reads task484/target/)

Each zone's 2025-26 PM2.5 from residential wood combustion: its appliances in use (the registry) at the 2024-25
survey's wood burned by zone and class, plus the wood the propane homes with a heating appliance burned in place of
propane, read from how much further their 2025-26 deliveries fell than at the zone's propane homes with none (in
proportion, as the two groups moved alike from 2023-24 to 2024-25), at the furnace's and the appliance's
efficiencies. The asks: each zone's commercial and institutional propane by delivery date, and the county outside
the maintenance area on the state tool."""
import collections
import csv
import datetime as dt
import os
import re

import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
SEASON = {2023: (dt.date(2023, 10, 1), dt.date(2024, 4, 30)), 2024: (dt.date(2024, 10, 1), dt.date(2025, 4, 30)),
          2025: (dt.date(2025, 10, 1), dt.date(2026, 4, 30))}
LONG = {"NORTH": "N", "SOUTH": "S", "STREET": "ST", "AVENUE": "AVE", "DRIVE": "DR", "LANE": "LN", "ROAD": "RD",
        "TRAIL": "TRL", "LOOP": "LOOP"}
UNITS = {"cords": 1.0, "face cords": 1 / 3.0, "pickup loads": 0.5, "tons": 1.0, "bags (40 lb)": 40 / 2000.0}


def rows(T, name):
    with open(os.path.join(T, name), newline="") as f:
        return list(csv.DictReader(f))


def find(T, prefix):
    m = [n for n in os.listdir(T) if n.startswith(prefix)]
    assert len(m) == 1, (prefix, m)
    return m[0]


def pdf_text(T, prefix):
    return " ".join(p.extract_text() for p in PdfReader(os.path.join(T, find(T, prefix))).pages).replace("\n", " ")


def season_of(d):
    for t, (a, b) in SEASON.items():
        if a <= d <= b:
            return t
    return None


def norm_address(a):
    return " ".join(LONG.get(p, p) for p in a.upper().replace(".", "").split())


def load(T=TARGET):
    p = {}
    # the registry, the device codes and the zones
    p["scc"] = {x["device_code"]: x for x in rows(T, find(T, "device_code_scc"))}
    code_cls = {"STV-U": "UNC", "STV-C": "CNC", "STV-K": "CAT", "PLT": "PEL", "FPL": "FPL", "OHH": "HYD"}
    p["scc_of"] = {c: p["scc"][k]["scc"] for k, c in code_cls.items()}
    p["desc_of"] = {c: p["scc"][k]["scc_description"] for k, c in code_cls.items()}
    reg = []
    for x in rows(T, find(T, "solid_fuel_device_registry")):
        inst = x["installed"]
        inst = dt.date(int(inst), 1, 1) if len(inst) == 4 else dt.date.fromisoformat(inst)
        rem = dt.date.fromisoformat(x["status_date"]) if x["status"] == "Removed" else None
        reg.append(dict(id=x["device_id"], geo=x["geocode"], zone=x["burn_zone"], cls=code_cls[x["device_code"]],
                        installed=inst, removed=rem))
    p["registry"] = reg
    zones = rows(T, find(T, "burn_zone_parcels"))
    p["zone_of"] = {x["geocode"]: x["burn_zone"] for x in zones}
    p["geo_of_addr"] = {x["situs_address"]: x["geocode"] for x in zones}
    p["zones"] = sorted(set(p["zone_of"].values()), key=["Valley Floor North", "Valley Floor South", "East Bench",
                                                          "West Bench", "Upper Valley"].index)
    # constants: the plan's allotments, the 2023 factors, the tool's appliance table and the fuel sheet
    plan = pdf_text(T, "maintenance_plan")
    p["allot"] = {z: float(re.search(re.escape(z) + r" (\d+\.\d)", plan).group(1)) for z in p["zones"]}
    p["fund"] = int(re.search(r"2026-27 changeout season is USD ([\d,]+)", plan).group(1).replace(",", ""))
    ef = rows(T, find(T, "emission_factors_2023"))
    p["ef"] = {x["scc"]: float(x["factor"]) for x in ef if x["pollutant"] == "PM2.5" and x["unit"].startswith("lb/ton")}
    p["ef_lp"] = {(x["category"], x["pollutant"]): float(x["factor"]) for x in ef if x["unit"] == "lb/MMBtu heat input"}
    tool = pdf_text(T, "montana_rwc_tool")
    p["cord_btu"] = float(re.search(r"holds ([\d.]+) million Btu and weighs", tool).group(1)) * 1e6
    p["tpc"] = float(re.search(r"weighs ([\d.]+) tons", tool).group(1))
    p["pellet_btu"] = float(re.search(r"a ton of pellets holds ([\d.]+) million Btu", tool).group(1)) * 1e6
    p["eff"], p["tshare"], p["tuse"] = {}, {}, {}
    for c, scc in p["scc_of"].items():
        m = re.search(scc + r" (not a heating appliance|\d+%) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)", tool)
        p["eff"][c] = None if m.group(1).startswith("not") else int(m.group(1)[:-1]) / 100.0
        p["tshare"][c] = (float(m.group(2)), float(m.group(3)))
        p["tuse"][c] = (float(m.group(4)), float(m.group(5)))
    p["secondary"] = float(re.search(r"secondary heat source are ([\d.]+) times", tool).group(1))
    fuel = rows(T, find(T, "heating_fuel_equivalents"))
    lp = [x for x in fuel if x["fuel"] == "Propane" and x["appliance"] == "Furnace or boiler, existing"][0]
    p["btu_gal"], p["afue"] = float(lp["btu_per_unit"]), float(lp["seasonal_efficiency_pct"]) / 100.0
    # the survey
    resp = []
    for x in rows(T, find(T, "heating_survey_2024_25_responses")):
        resp.append(dict(zone=x["burn_zone"], dev=x["device_id"], units=float(x["amount_burned_2024_25"]) * UNITS[x["unit"]],
                         w=float(x["weight"]), fuel=x["main_heating_fuel"]))
    byid = {d["id"]: d for d in reg}
    for x in resp:
        x["cls"] = byid[x["dev"]]["cls"]
    p["survey"] = resp
    # the three distributors' accounts and deliveries, one shape: account key, class, geocode, deliveries by date
    acct, deliv = {}, collections.defaultdict(list)
    for x in rows(T, find(T, "wapiti_propane_accounts")):
        acct["L" + x["account_no"]] = dict(cls="COM" if x["account_class"] == "Commercial" else "RES", geo=x["geocode"])
    for x in rows(T, find(T, "wapiti_propane_tickets")):
        m, d, y = x["delivery_date"].split("/")
        deliv["L" + x["account_no"]].append((dt.date(int(y), int(m), int(d)), float(x["gallons"]), None))
    with open(os.path.join(T, find(T, "coldwater_activity_export"))) as f:
        for line in f:
            line = line.rstrip("\r\n")
            if line[0] == "A":
                g = line[58:75]
                geo = "%s-%s-%s-%s-%s-%s-%s" % (g[0:2], g[2:6], g[6:8], g[8], g[9:11], g[11:13], g[13:17])
                acct["C" + line[1:9].strip()] = dict(cls="COM" if line[9] == "C" else "RES", geo=geo)
            else:
                ref = line[9:21]
                d = dt.datetime.strptime(ref[1:7], "%y%m%d").date()
                post = dt.datetime.strptime(line[21:29], "%Y%m%d").date()
                deliv["C" + line[1:9].strip()].append((d, int(line[29:36]) / 10.0, post))
    wb = openpyxl.load_workbook(os.path.join(T, find(T, "halvard_coop_propane")), read_only=True)
    mnum = dict(Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12, Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6)
    for ws in wb.worksheets:
        fy = int(ws.title[2:6])
        head = None
        for row in ws.iter_rows(values_only=True):
            if row and row[0] == "Member account":
                head = list(row)
                continue
            if head is None or not row or row[0] is None:
                continue
            k = "H" + str(row[0])
            geo = p["geo_of_addr"].get(norm_address(row[2]))
            acct[k] = dict(cls="COM" if row[1] == "Commercial" else "RES", geo=geo)
            for j, mn in enumerate(head[4:], 4):
                if row[j]:
                    m = mnum[mn]
                    y = fy if m >= 7 else fy + 1
                    deliv[k].append((dt.date(y, m, 15), float(row[j]), None))
    for k, a in acct.items():
        a["zone"] = p["zone_of"].get(a["geo"]) if a["geo"] else None
    p["acct"], p["deliv"] = acct, deliv
    return p


# ---------------------------------------------------------------- the inventory


def in_use(d, t):
    a, b = SEASON[t]
    return d["installed"] <= a and (d["removed"] is None or d["removed"] > b)


def tons(p, c, units):
    return units if c == "PEL" else units * p["tpc"]


def survey_means(p, small=10, pooled=False, weighted=True):
    area = {}
    for c in p["scc_of"]:
        xs = [(x["w"] if weighted else 1.0, x["units"]) for x in p["survey"] if x["cls"] == c]
        area[c] = sum(w * u for w, u in xs) / sum(w for w, u in xs)
    out = {}
    for z in p["zones"]:
        for c in p["scc_of"]:
            xs = [(x["w"] if weighted else 1.0, x["units"]) for x in p["survey"] if x["cls"] == c and x["zone"] == z]
            out[z, c] = area[c] if pooled or len(xs) < small else sum(w * u for w, u in xs) / sum(w for w, u in xs)
    return out


def counts(p, t=2025):
    n = collections.Counter()
    for d in p["registry"]:
        if in_use(d, t):
            n[d["zone"], d["cls"]] += 1
    return n


def season_gallons(p, k, t, by="delivery"):
    a, b = SEASON[t]
    tot = 0.0
    for d, g, post in p["deliv"][k]:
        x = post if (by == "posted" and post is not None) else d
        if a <= x <= b:
            tot += g
    return tot


def propane_homes(p):
    """Residential accounts in the zones with the heating appliance in use at their parcel (None if none)."""
    heat = {}
    for d in p["registry"]:
        if in_use(d, 2025) and in_use(d, 2024) and p["eff"][d["cls"]] is not None:
            heat[d["geo"]] = d["cls"]
    fpl = {d["geo"] for d in p["registry"] if in_use(d, 2025) and d["cls"] == "FPL"}
    out = []
    for k, a in p["acct"].items():
        if a["cls"] != "RES" or a["zone"] is None:
            continue
        g = {t: season_gallons(p, k, t) for t in SEASON}
        out.append(dict(k=k, zone=a["zone"], cls=heat.get(a["geo"]), fpl=a["geo"] in fpl, g=g))
    return out


def switch(p, homes, R="zone", form="ratio", fpl_comp=True):
    """Gallons each zone's propane homes with a heating appliance did not take in 2025-26, by appliance class."""
    out = {}
    for z in p["zones"]:
        comp = [h for h in homes if h["zone"] == z and h["cls"] is None and (fpl_comp or not h["fpl"])]
        if R == "zone":
            Rv = sum(h["g"][2025] for h in comp) / sum(h["g"][2024] for h in comp)
        elif R == "pool":
            cp = [h for h in homes if h["cls"] is None and (fpl_comp or not h["fpl"])]
            Rv = sum(h["g"][2025] for h in cp) / sum(h["g"][2024] for h in cp)
        else:
            Rv = float(R)
        dl = sum(h["g"][2025] - h["g"][2024] for h in comp) / len(comp)
        for c in p["scc_of"]:
            trt = [h for h in homes if h["zone"] == z and h["cls"] == c]
            if form == "level":
                out[z, c] = sum(h["g"][2024] + dl - h["g"][2025] for h in trt)
            else:
                out[z, c] = sum(h["g"][2024] * Rv - h["g"][2025] for h in trt)
        out[z, "R"] = Rv
    return out


def extra_units(p, c, gal):
    """Cords (pellets: tons) carrying the heat of gal gallons of propane burned in the furnace."""
    e = p["eff"][c]
    if e is None or gal == 0:
        return 0.0
    return gal * p["btu_gal"] * p["afue"] / ((p["pellet_btu"] if c == "PEL" else p["cord_btu"]) * e)


def inventory(p, rung="golden", homes=None, **kw):
    """rung: 'golden'; 'default' (the survey carried as reported); 'hdd' (carried at the two seasons' degree days);
    'golden' with kw for the family (R='pool' or a number, form='level', fpl_comp=False)."""
    n = counts(p)
    mean = survey_means(p)
    f = kw.pop("scale", 1.0)
    sw = switch(p, homes or propane_homes(p), **kw) if rung == "golden" else None
    cells, zone = {}, {}
    for z in p["zones"]:
        zt = 0.0
        for c, scc in p["scc_of"].items():
            units = mean[z, c] * n[z, c] * f
            if sw is not None:
                units += extra_units(p, c, sw[z, c])
            w = tons(p, c, units)
            pm = w * p["ef"][scc] / 2000.0
            cells[z, c] = dict(n=n[z, c], wood=w, pm=pm, extra=extra_units(p, c, sw[z, c]) if sw else 0.0,
                               gal=sw[z, c] if sw else 0.0)
            zt += pm
        zone[z] = dict(pm=zt, allot=p["allot"][z], over=zt > p["allot"][z], R=sw[z, "R"] if sw else None)
    return dict(cells=cells, zone=zone, over=[z for z in p["zones"] if zone[z]["over"]])


# ---------------------------------------------------------------- the asks


def ask_a(p, by="delivery"):
    """Each zone's commercial and institutional propane delivered in the 2025-26 season: gallons and tons of NOx."""
    gal = collections.Counter()
    for k, a in p["acct"].items():
        if a["cls"] == "COM" and a["zone"]:
            gal[a["zone"]] += season_gallons(p, k, 2025, by=by)
    nox = p["ef_lp"]["Commercial/institutional propane combustion", "NOx"]
    return {z: dict(gal=gal[z], nox=gal[z] * p["btu_gal"] / 1e6 * nox / 2000.0) for z in p["zones"]}


def main_households(p, T=TARGET, release="acs5_2019_2023", split="relationship"):
    return ask_b(p, T, release, split)["_main"]


def ask_b(p, T=TARGET, release="acs5_2019_2023", split="relationship"):
    """The county outside the maintenance area on the state tool: appliances and tons of PM2.5 by SCC."""
    acs = rows(T, find(T, release))
    asr = rows(T, find(T, "assessor_housing_units"))
    rel = rows(T, find(T, "tab2020_tab2010"))
    hu10 = collections.defaultdict(lambda: [0, 0])
    for x in asr:
        hu10[x["block_group"]][0 if x["maintenance_area"] else 1] += int(x["housing_units"])
    share = {}
    if split == "relationship":
        o20, t20 = collections.Counter(), collections.Counter()
        for x in rel:
            i, o = hu10[x["GEOID_BG_10"]]
            o20[x["GEOID_BG_20"]] += int(x["HU_20_OVERLAP"]) * o / (i + o)
            t20[x["GEOID_BG_20"]] += int(x["HU_20_OVERLAP"])
        share = {g: o20[g] / t20[g] for g in t20}
    else:
        share = {g: o / (i + o) for g, (i, o) in hu10.items()}
    main = 0.0
    for x in acs:
        g = x["GEO_ID"][-12:]
        main += int(x["B25040_008E"]) * share.get(g, 0.0)
    sec = main * p["secondary"]
    out = {}
    for c, scc in p["scc_of"].items():
        sm, ss = p["tshare"][c]
        um, us = p["tuse"][c]
        app = main * sm + sec * ss
        units = main * sm * um + sec * ss * us
        w = tons(p, c, units)
        out[c] = dict(app=app, wood=w, pm=w * p["ef"][scc] / 2000.0)
    out["_main"] = main
    return out


if __name__ == "__main__":
    p = load()
    homes = propane_homes(p)
    g = inventory(p, homes=homes)
    d = inventory(p, "default")
    print("zone                  allot | default | golden   R")
    for z in p["zones"]:
        print("%-20s %6.1f | %6.2f %s | %6.2f %s %.4f" % (z, p["allot"][z], d["zone"][z]["pm"],
                                                       "OVER" if d["zone"][z]["over"] else "    ", g["zone"][z]["pm"],
                                                       "OVER" if g["zone"][z]["over"] else "    ", g["zone"][z]["R"]))
    print("default:", d["over"], "\ngolden:", g["over"])
    for kw in (dict(R="pool"), dict(R=1.0), dict(form="level"), dict(fpl_comp=False)):
        x = inventory(p, homes=homes, **kw)
        print(kw, " ".join("%.2f" % x["zone"][z]["pm"] for z in p["zones"]), x["over"])
    print("ask A", {z: (round(v["gal"]), round(v["nox"], 3)) for z, v in ask_a(p).items()})
    print("ask A posted", {z: (round(v["gal"]), round(v["nox"], 3)) for z, v in ask_a(p, "posted").items()})
    print("ask B", {c: (round(v["app"], 1), round(v["pm"], 2)) for c, v in ask_b(p).items() if c != "_main"})
