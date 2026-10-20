"""The pack's records: every county's wells with their addresses and parcels, the permit database (the active domestic
wells and the permits that are not), the assessors' residential parcels (private well or public water), the survey's
draw manifest, the three laboratories' results, the retest requests and the reference files; written as the systems
that hold them write them."""
import csv
import datetime as dt

import numpy as np

import sim as S
import world as W

FILES = {
    "permits": "DOH_well_construction_permits_extract_2026-08-03.csv",
    "parcels": "county_assessor_residential_parcels_2025_roll.xlsx",
    "manifest": "PWNS_2025-26_draw_manifest.csv",
    "hal": "Halvorsen_PWNS_results_2025-26.csv",
    "ced": "Cedarline_PWNS_results_2025-26.xlsx",
    "kin": "Kinsale_PWNS_results_2025-26.csv",
    "retests": "PWNS_retest_kit_requests_2026.csv",
    "counties": "PWP_county_codes.csv",
    "design": "PWNS_2025-26_survey_design_report.pdf",
    "standard": "WWA_2027_county_allocation_standard.pdf",
    "factsheet": "PWP_nitrate_and_your_well_fact_sheet.pdf",
    "labs": "certified_drinking_water_labs_2025.csv",
}
DISTRACTORS = ("factsheet", "labs")

STREETS = ["Oak Ridge", "Mill Pond", "Cedar Hollow", "Fox Run", "Quarry", "Old Farm", "Birch Hill", "Stony Brook",
           "Maple Grove", "Pine Knob", "Hidden Valley", "Orchard", "Spring Creek", "Sawmill", "Ridgeview", "Elm Bend",
           "Cranberry", "Beaver Dam", "Turkey Hill", "Chestnut", "Long Meadow", "Pheasant", "Shady", "Granite",
           "Willow Brook", "Hemlock", "Bluebird", "Red Barn", "Clover Hill", "Deer Path", "Sugarbush", "Indian Creek",
           "Tamarack", "Lost Lake", "Prairie View", "Windmill", "Hickory", "Kettle Pond", "Saddleback", "Thornapple",
           "Wolf Creek", "Gravel Pit", "Schoolhouse", "Church", "Creamery", "Depot", "Ferry", "Grange", "Hayfield",
           "Juniper", "Larkspur", "Meadowlark", "Nettle", "Plum Creek", "Quail Run", "Ravine", "Silo", "Timber",
           "Upper Valley", "Vista", "Wheatfield", "Yarrow", "Alder Creek", "Bramble", "Cobble Hill", "Dogwood",
           "Evergreen", "Fieldstone", "Goose Pond", "Heron", "Ironwood", "Juneberry", "Kingfisher", "Lilac",
           "Mossy Rock", "Northfield", "Owl Hollow", "Partridge", "Rabbit Run", "Sandhill", "Tanager", "Valley View"]
SUFFIX = [("Road", "RD"), ("Lane", "LN"), ("Drive", "DR"), ("Trail", "TRL"), ("Highway", "HWY"), ("Court", "CT"),
          ("Avenue", "AVE"), ("Street", "ST")]
SUFFIX_P = [0.46, 0.18, 0.12, 0.08, 0.05, 0.04, 0.04, 0.03]
DIRS = [("North", "N"), ("South", "S"), ("East", "E"), ("West", "W")]
TOWNS = ["Ashby", "Bellmont", "Carrick", "Dalton", "Easton", "Fairhope", "Garland", "Hilton", "Iona", "Jasper",
         "Kirkby", "Linton", "Milford", "Norland", "Orrin", "Pelham", "Rowan", "Selby", "Tilden", "Upton", "Vernon",
         "Weldon", "Yardley", "Alston", "Briar", "Colby", "Dover", "Elgin", "Fenton", "Gilman", "Hadley", "Ingram",
         "Kendall", "Larue", "Mapleton", "Newcomb", "Oxbow", "Prescott", "Quincy", "Redfield", "Stanwood", "Thayer",
         "Ulster", "Vail", "Whitby", "Arden", "Bixby", "Cullen", "Darrow", "Ellery", "Fulton", "Grafton"]
TOWN_SHARE = [0.52, 0.33, 0.15]       # the third town of each county is the smallest, on its border
WATER_CODES = {"A": ("W", "P"), "B": ("WELL", "PUBLIC"), "C": ("2", "1")}   # private well code, public water code
LAYOUT_OF = {"C01": "A", "C02": "B", "C03": "C", "C04": "A", "C05": "B", "C06": "A", "C07": "C", "C08": "B",
             "C09": "A", "C10": "C", "C11": "B", "C12": "A", "C13": "C", "C14": "B", "C15": "A", "C16": "C"}
ASSESSOR_STYLE = {"A": "dash", "B": "plain", "C": "space"}
# the sixteen counties sit four by four, C01 to C04 across the north; a county's neighbours share an edge
GRID = {"C%02d" % (i + 1): (i // 4, i % 4) for i in range(16)}
FRAME_DATE = dt.date(2025, 8, 31)


def rng(seed, *parts):
    return np.random.default_rng([seed, *parts])


def neighbours(code):
    r0, c0 = GRID[code]
    return [k for k, (r1, c1) in GRID.items() if abs(r0 - r1) + abs(c0 - c1) == 1]


def fmt_parcel(cc, book, lot, style):
    if style == "dash":
        return "%02d-%03d-%04d" % (cc, book, lot)
    if style == "plain":
        return "%02d%03d%04d" % (cc, book, lot)
    if style == "space":
        return "%02d %03d %04d" % (cc, book, lot)
    if style == "short":
        return "%02d%03d-%04d" % (cc, book, lot)
    raise ValueError(style)


def everything(seed=W.SEED):
    x = dict(seed=seed, counties=[])
    order = list(rng(seed, 19).permutation(len(TOWNS)))
    for k, ((name, code), p) in enumerate(zip(W.COUNTIES, W.PLACED)):
        c = S.county(seed, k, p)
        c.update(name=name, code=code, cc=k + 1, lab=W.LAB_OF[code], layout=LAYOUT_OF[code])
        c["towns"] = [TOWNS[int(i)] for i in order[3 * k:3 * k + 3]]
        c["zips"] = ["%05d" % (58100 + 37 * k + 11 * j + (k * 7 + j * 3) % 9) for j in range(3)]
        attributes(seed, c)
        x["counties"].append(c)
    kits(seed, x)
    route(seed, x)
    return x


def attributes(seed, c):
    """addresses, parcels, permits and the extra parcels and permits the files hold beside the frames"""
    r = rng(seed, 20, c["k"])
    N = c["N"]
    extra_pub = int(N * r.uniform(0.55, 0.9))           # residential parcels on public water
    n_new = int(c["NP"] * r.uniform(0.012, 0.022))      # domestic wells drilled after the frame date
    total = N + extra_pub + n_new
    used, addr = set(), []
    while len(addr) < total:
        num = int(r.integers(10, 9990)) if r.random() < 0.7 else int(r.integers(10000, 29999))
        st = STREETS[int(r.integers(len(STREETS)))]
        if (num, st) in used:
            continue
        used.add((num, st))
        sf = int(r.choice(len(SUFFIX), p=SUFFIX_P))
        d = int(r.integers(4)) if r.random() < 0.28 else -1
        addr.append(dict(num=num, street=st, suf=sf, dir=d, town=int(r.choice(3, p=TOWN_SHARE))))
    lots, parcels = set(), []
    while len(parcels) < N + extra_pub:
        b, l = int(r.integers(1, 420)), int(r.integers(1, 9999))
        if (b, l) in lots:
            continue
        lots.add((b, l))
        parcels.append((b, l))
    c["addr"] = addr[:N]
    c["parcel"] = parcels[:N]
    c["pub_addr"] = addr[N:N + extra_pub]
    c["pub_parcel"] = parcels[N:]
    c["new_addr"] = addr[N + extra_pub:]
    c["year_built"] = np.where(c["grp"] == 1, r.integers(1890, 1986, N), r.integers(1950, 2025, N))
    # the assessor codes a permit-only well's parcel as public water or leaves the field blank
    c["po_code"] = np.where(r.random(N) < 0.7, "PUBLIC", "BLANK")
    onP = c["onP"]
    d0 = np.datetime64("1986-01-02")
    span = (np.datetime64(FRAME_DATE.isoformat()) - d0).astype(int)
    drilled = np.full(N, np.datetime64("NaT"), dtype="datetime64[D]")
    drilled[onP] = d0 + r.integers(0, span, int(onP.sum())).astype("timedelta64[D]")
    c["drilled"] = drilled
    c["permit_no"], c["permit_parcel_style"] = {}, {}
    seen = set()

    def permit_no(yr):
        while True:
            v = "W-%d-%05d" % (yr, int(r.integers(10000, 99999)))
            if v not in seen:
                seen.add(v)
                return v
    for i in np.flatnonzero(onP):
        yr = int(str(drilled[i])[:4])
        c["permit_no"][int(i)] = permit_no(yr)
        # a permit carries the parcel number more often the newer it is
        has = r.random() < (0.45 if yr < 2000 else 0.75 if yr < 2012 else 0.93)
        c["permit_parcel_style"][int(i)] = (["dash", "short", "plain"][int(r.choice(3, p=[0.7, 0.2, 0.1]))]
                                            if has else None)
    c["depth"] = np.where(c["grp"] == 1, r.integers(18, 140, N), r.integers(80, 640, N))
    c["casing"] = (c["depth"] * r.uniform(0.3, 0.8, N)).astype(int)
    # permits outside the frame: wells for irrigation, livestock or monitoring, the earlier permits of replaced wells,
    # abandoned domestic wells on parcels now on public water, and domestic wells drilled after the frame date
    noise = []
    for _ in range(int(onP.sum() * r.uniform(0.10, 0.16))):
        use = ["IRRIGATION", "LIVESTOCK", "MONITORING", "INDUSTRIAL"][int(r.choice(4, p=[0.45, 0.3, 0.2, 0.05]))]
        a = dict(num=int(r.integers(30000, 49999)), street=STREETS[int(r.integers(len(STREETS)))],
                 suf=int(r.choice(len(SUFFIX), p=SUFFIX_P)), dir=-1, town=int(r.choice(3, p=TOWN_SHARE)))
        yr = int(r.integers(1986, 2026))
        noise.append(dict(permit=permit_no(yr), addr=a, use=use, status="ACTIVE",
                          drilled=dt.date(yr, int(r.integers(1, 13)), int(r.integers(1, 28))), parcel=None,
                          depth=int(r.integers(40, 900))))
    for i in r.choice(np.flatnonzero(onP), int(onP.sum() * r.uniform(0.04, 0.07)), replace=False):
        yr = int(str(drilled[i])[:4])
        old = max(1986, yr - int(r.integers(6, 25)))
        noise.append(dict(permit=permit_no(old), addr=c["addr"][i], use="DOMESTIC", status="REPLACED",
                          drilled=dt.date(old, int(r.integers(1, 13)), int(r.integers(1, 28))), parcel=None,
                          depth=int(r.integers(40, 300))))
    for j in range(int(onP.sum() * r.uniform(0.03, 0.06))):
        yr = int(r.integers(1986, 2010))
        noise.append(dict(permit=permit_no(yr), addr=c["pub_addr"][j], use="DOMESTIC", status="ABANDONED",
                          drilled=dt.date(yr, int(r.integers(1, 13)), int(r.integers(1, 28))),
                          parcel=c["pub_parcel"][j], depth=int(r.integers(40, 300))))
    for a in c["new_addr"]:
        d = FRAME_DATE + dt.timedelta(days=int(r.integers(2, 330)))
        noise.append(dict(permit=permit_no(d.year), addr=a, use="DOMESTIC", status="ACTIVE", drilled=d, parcel=None,
                          depth=int(r.integers(80, 640))))
    c["noise_permits"] = noise


def kits(seed, x):
    """kit numbers, collection dates, reruns, and the retest kits households asked for"""
    r = rng(seed, 30)
    kit_used = set()

    def new_kit(prefix):
        while True:
            v = "%s%06d" % (prefix, int(r.integers(100000, 999999)))
            if v not in kit_used:
                kit_used.add(v)
                return v
    start = np.datetime64(W.SURVEY_START.isoformat())
    for c in x["counties"]:
        c["kit"], c["collected"], c["rerun"] = {}, {}, {}
        for i in np.flatnonzero(c["tested"]):
            i = int(i)
            c["kit"][i] = new_kit("PW25-")
            c["collected"][i] = start + np.timedelta64(int(r.integers(6, 225)), "D")
            if r.random() < 0.035:
                c["rerun"][i] = float(c["measured"][i] * np.exp(r.normal(0, 0.06)))
        # requests: every household whose first test was above the standard and that asked for a retest, a few
        # households below it that asked anyway, and households outside the survey whose own test was high
        req = []
        for i in np.flatnonzero(c["retested"]):
            i = int(i)
            first = c["collected"][i]
            d = max(np.datetime64("2026-01-12"),
                    min(np.datetime64("2026-06-28"), first + np.timedelta64(int(r.integers(35, 170)), "D")))
            req.append(dict(well=i, via="PHONE" if c["phone"][i] else "PORTAL", collected=d,
                            value=float(c["remeasured"][i]), kind="above"))
        above = np.flatnonzero(c["tested"] & (c["measured"] > W.STANDARD_N) & ~c["retested"])
        for i in (r.choice(above, min(len(above), int(r.integers(1, 4))), replace=False) if len(above) else []):
            req.append(dict(well=int(i), via="PORTAL" if r.random() < 0.6 else "PHONE",
                            collected=np.datetime64("2026-07-01") + np.timedelta64(int(r.integers(0, 24)), "D"),
                            value=float(c["nitrate"][i] * r.uniform(0.82, 1.02)), kind="late"))
        below = np.flatnonzero(c["tested"] & (c["measured"] > 6.5) & (c["measured"] < 9.6))
        for i in (r.choice(below, min(len(below), int(r.integers(1, 4))), replace=False) if len(below) else []):
            req.append(dict(well=int(i), via="PORTAL" if r.random() < 0.5 else "PHONE",
                            collected=np.datetime64("2026-02-02") + np.timedelta64(int(r.integers(0, 140)), "D"),
                            value=float(c["nitrate"][i] * np.exp(r.normal(0, 0.05))), kind="below"))
        untested = np.flatnonzero(~c["tested"] & (c["nitrate"] > 9.0))
        for i in r.choice(untested, min(len(untested), int(r.integers(1, 4))), replace=False):
            req.append(dict(well=int(i), via="PHONE",
                            collected=np.datetime64("2026-02-01") + np.timedelta64(int(r.integers(0, 140)), "D"),
                            value=float(c["nitrate"][i] * np.exp(r.normal(0, 0.04))), kind="outside"))
        for q in req:
            q["kit"] = new_kit("PW26-R")
            q["requested"] = q["collected"] - np.timedelta64(int(r.integers(9, 32)), "D")
            q["mailed"] = q["requested"] + np.timedelta64(int(r.integers(1, 4)), "D")
            q["rerun"] = float(q["value"] * np.exp(r.normal(0, 0.05))) if r.random() < 0.03 else None
        c["requests"] = req
    # keep every printed result clear of the standard, so that no rounding and no conversion factor (4.427, or the
    # fact sheet's 4.4 against its 44 mg/L) puts a result on the other side of it
    def clear(v):
        if 9.90 < v <= W.STANDARD_N:
            return float(r.uniform(9.55, 9.90))
        if W.STANDARD_N < v < 10.05:
            return float(r.uniform(10.05, 10.40))
        return v
    for c in x["counties"]:
        for i in list(c["kit"]):
            c["measured"][i] = clear(c["measured"][i])
        for q in c["requests"]:
            q["value"] = clear(q["value"])


def route(seed, x):
    """The kit vendor routes a portal request to a county by the ZIP code the household types. In most counties one
    of the two smaller towns has a ZIP code whose post office sits over the county line, so its portal requests go to
    that neighbour, whose laboratory analyses the retest. Phone requests are routed by the county the caller gives."""
    r = rng(seed, 31)
    codes = [c["code"] for c in x["counties"]]
    by = {c["code"]: c for c in x["counties"]}
    close = np.datetime64(W.RETESTS_CLOSE.isoformat())
    flows, gold, portal = {}, {}, {}
    for k in codes:
        c = by[k]
        counted = [q for q in c["requests"] if q["kind"] == "above" and q["collected"] <= close]
        gold[k] = (len(counted), sum(1 for q in counted if q["value"] > W.STANDARD_N))
        port = [q for q in counted if q["via"] == "PORTAL"]
        portal[k] = (len(port), sum(1 for q in port if q["value"] > W.STANDARD_N))
        for town in (1, 2):
            qs = [q for q in port if c["addr"][q["well"]]["town"] == town]
            flows[(k, town)] = (len(qs), sum(1 for q in qs if q["value"] > W.STANDARD_N))
    for _ in range(400000):
        pick = {k: (int(r.integers(1, 3)), neighbours(k)[int(r.integers(len(neighbours(k))))]) for k in codes}
        net = {k: [0, 0] for k in codes}
        for k, (town, nb) in pick.items():
            for j in (0, 1):
                net[k][j] -= flows[(k, town)][j]
                net[nb][j] += flows[(k, town)][j]
        # every county's two figures move when requests are counted in the county on the request, and again when
        # only the portal's requests are
        if all(net[k][j] != 0 and portal[k][j] + net[k][j] != gold[k][j] for k in codes for j in (0, 1)):
            break
    else:
        raise SystemExit("no routing moves every county's retest figures")
    x["border"] = pick
    for c in x["counties"]:
        town, nb = pick[c["code"]]
        for q in c["requests"]:
            q["route"] = nb if (q["via"] == "PORTAL" and c["addr"][q["well"]]["town"] == town) else c["code"]


# ----------------------------------------------------------------------------------------------------- formatting
def addr_permit(a, r):
    st = a["street"]
    suf_long, suf_short = SUFFIX[a["suf"]]
    style = r.random()
    if a["dir"] >= 0:
        dl, ds = DIRS[a["dir"]]
    if style < 0.6:
        return "%d %s%s %s" % (a["num"], (ds + " ") if a["dir"] >= 0 else "", st, suf_short.title())
    if style < 0.85:
        return "%d %s%s %s" % (a["num"], (dl + " ") if a["dir"] >= 0 else "", st, suf_long)
    return "%d %s%s %s." % (a["num"], (ds + ". ") if a["dir"] >= 0 else "", st, suf_short.title())


def addr_parcel(a, layout):
    st = a["street"].upper()
    suf_long, suf_short = SUFFIX[a["suf"]]
    if layout == "A":
        return "%d %s%s %s" % (a["num"], (DIRS[a["dir"]][1] + " ") if a["dir"] >= 0 else "", st, suf_short)
    if layout == "C":
        return "%d %s%s %s" % (a["num"], (DIRS[a["dir"]][1] + " ") if a["dir"] >= 0 else "", st, suf_long.upper())
    raise ValueError(layout)


def addr_request(a, r):
    st = a["street"]
    suf_long, suf_short = SUFFIX[a["suf"]]
    d = ""
    if a["dir"] >= 0:
        d = (DIRS[a["dir"]][0] if r.random() < 0.5 else DIRS[a["dir"]][1]) + " "
    s = "%d %s%s %s" % (a["num"], d, st, suf_long if r.random() < 0.5 else suf_short.title())
    return s.upper() if r.random() < 0.3 else s


# --------------------------------------------------------------------------------------------------- the writers
PERMIT_COLS = ["PERMIT_NO", "COUNTY", "SITE_ADDRESS", "SITE_CITY", "PARCEL_NO", "DATE_DRILLED", "WELL_USE",
               "WELL_STATUS", "TOTAL_DEPTH_FT", "CASING_DEPTH_FT"]


def permit_rows(x):
    r = rng(x["seed"], 40)
    out = []
    for c in x["counties"]:
        for i, pno in c["permit_no"].items():
            a = c["addr"][i]
            style = c["permit_parcel_style"][i]
            b, l = c["parcel"][i]
            out.append([pno, c["name"].upper(), addr_permit(a, r), c["towns"][a["town"]],
                        fmt_parcel(c["cc"], b, l, style) if style else "", str(c["drilled"][i]), "DOMESTIC", "ACTIVE",
                        int(c["depth"][i]), int(c["casing"][i])])
        for n in c["noise_permits"]:
            par = fmt_parcel(c["cc"], *n["parcel"], "dash") if n["parcel"] else ""
            out.append([n["permit"], c["name"].upper(), addr_permit(n["addr"], r), c["towns"][n["addr"]["town"]], par,
                        n["drilled"].isoformat(), n["use"], n["status"], n["depth"], int(n["depth"] * 0.5)])
    out.sort(key=lambda v: (v[0][2:6], v[0]))
    return out


PARCEL_LAYOUTS = {
    "A": ["PARCEL_ID", "SITUS_ADDRESS", "SITUS_CITY", "USE_CODE", "YEAR_BUILT", "WATER"],
    "B": ["PIN", "HOUSE_NO", "DIR", "STREET", "SUFFIX", "CITY", "CLASS", "YR_BLT", "WATER_SOURCE"],
    "C": ["Parcel Number", "Property Address", "Municipality", "Property Type", "Year Built", "Water Service"],
}


def parcel_sheets(x):
    """each county assessor's residential parcels, in that assessor's layout"""
    r = rng(x["seed"], 41)
    sheets = {}
    for c in x["counties"]:
        lay = c["layout"]
        pw, pub = WATER_CODES[lay]
        rows = []
        for i in range(c["N"]):
            b, l = c["parcel"][i]
            code = (pub if c["po_code"][i] == "PUBLIC" else "") if c["grp"][i] == 0 else pw
            rows.append((b, l, c["addr"][i], int(c["year_built"][i]), code))
        for j, a in enumerate(c["pub_addr"]):
            b, l = c["pub_parcel"][j]
            rows.append((b, l, a, int(r.integers(1900, 2025)), pub))
        out = []
        for o in r.permutation(len(rows)):
            b, l, a, yb, code = rows[o]
            town = c["towns"][a["town"]]
            if lay == "A":
                out.append([fmt_parcel(c["cc"], b, l, "dash"), addr_parcel(a, "A"), town.upper(), "R1", yb, code])
            elif lay == "B":
                out.append([fmt_parcel(c["cc"], b, l, "plain"), a["num"], (DIRS[a["dir"]][1] if a["dir"] >= 0 else ""),
                            a["street"].upper(), SUFFIX[a["suf"]][1], town.upper(), "RES", yb, code])
            else:
                out.append([fmt_parcel(c["cc"], b, l, "space"), addr_parcel(a, "C"), town, "Single family", yb, code])
        sheets[c["code"]] = (lay, out)
    return sheets


MANIFEST_COLS = ["DRAW_ID", "COUNTY_CODE", "FRAME", "FRAME_RECORD", "DRAW_SEQ", "MAILED", "OUTCOME", "KIT_ID"]


def manifest_rows(x):
    out = []
    n = 0
    for c in x["counties"]:
        seq = {"P": 0, "Q": 0}
        day = np.datetime64(W.SURVEY_START.isoformat())
        for lst, i, outcome in c["draws"]:
            i = int(i)
            seq[lst] += 1
            n += 1
            b, l = c["parcel"][i]
            rec = c["permit_no"][i] if lst == "P" else fmt_parcel(c["cc"], b, l, ASSESSOR_STYLE[c["layout"]])
            mailed = day + np.timedelta64(int(seq[lst] // 9), "D")
            kit = c["kit"].get(i, "") if outcome in ("TESTED", "TESTED_EARLIER") else ""
            out.append(["D%06d" % (100000 + n), c["code"], "PERMIT" if lst == "P" else "PARCEL", rec, seq[lst],
                        str(mailed), outcome, kit])
    return out


def lab_records(x):
    """every result row the three laboratories report, before formatting; a retest goes to the laboratory of the
    county the request was routed to"""
    r = rng(x["seed"], 43)
    by = {c["code"]: c for c in x["counties"]}
    items = []
    for c in x["counties"]:
        for i, kit in c["kit"].items():
            items.append((c["code"], "FIRST", kit, c["collected"][i], float(c["measured"][i]), c["rerun"].get(i)))
        for q in c["requests"]:
            items.append((q["route"], "RETEST", q["kit"], q["collected"], q["value"], q["rerun"]))
    items.sort(key=lambda v: (str(v[3]), v[2]))
    recs = {"HAL": [], "CED": [], "KIN": []}
    sid = {"HAL": 30000, "CED": 50000, "KIN": 700000}
    for code, typ, kit, d, v, rerun in items:
        lab = by[code]["lab"]
        sid[lab] += int(r.integers(1, 7))
        arsenic = float(np.exp(r.normal(0.6, 1.0)))
        tc = r.random() < 0.18
        ec = tc and r.random() < 0.12
        recs[lab].append(dict(county=code, kit=kit, sample=sid[lab], collected=d, nitrate=v, rerun=rerun,
                              arsenic=arsenic, tc=tc, ec=ec, type=typ,
                              received=d + np.timedelta64(int(r.integers(1, 4)), "D"),
                              reported=d + np.timedelta64(int(r.integers(6, 15)), "D")))
    return recs


def nitrate_text(v, lab):
    if v < 0.4:
        return "<0.4" if lab == "HAL" else "0.4" if lab == "CED" else "1.8"
    return "%.2f" % v if lab != "KIN" else "%.1f" % (v * W.NO3_PER_N)


HAL_COLS = ["SAMPLE_ID", "KIT_ID", "COUNTY_CODE", "COLLECTED", "RECEIVED", "REPORTED", "SAMPLE_TYPE", "NO3N_MG_L",
            "AS_UG_L", "TOTAL_COLIFORM", "E_COLI", "RESULT_STATUS"]


def hal_rows(recs):
    out = []
    for q in recs:
        base = ["H25-%05d" % q["sample"], q["kit"], q["county"], str(q["collected"]), str(q["received"])]
        typ = "ROUTINE" if q["type"] == "FIRST" else "CONFIRMATION"
        if q["rerun"] is not None:
            out.append(base + [str(q["reported"] - np.timedelta64(3, "D")), typ, nitrate_text(q["rerun"], "HAL"),
                               "%.1f" % q["arsenic"], "A", "A", "SUPERSEDED"])
        out.append(base + [str(q["reported"]), typ, nitrate_text(q["nitrate"], "HAL"), "%.1f" % q["arsenic"],
                           "P" if q["tc"] else "A", "P" if q["ec"] else "A", "FINAL"])
    return out


CED_COLS = ["Lab Sample", "Client Kit", "County", "Date Sampled", "Analyte", "Result", "Unit", "Qualifier", "Method",
            "Report Date", "Comment"]


def _d(v):
    return dt.date.fromisoformat(str(v))


def ced_rows(recs):
    out = []
    for q in recs:
        base = ["CED-25-%05d" % q["sample"], q["kit"], q["county"], _d(q["collected"])]
        rep = _d(q["reported"])
        com = "Confirmation sample" if q["type"] == "RETEST" else ""
        if q["rerun"] is not None:
            out.append(base + ["Nitrate as N", nitrate_text(q["rerun"], "CED"), "mg/L", "", "EPA 300.0",
                               _d(q["reported"] - np.timedelta64(4, "D")), com])
            com2 = "Reanalysis; replaces earlier result" + ("; " + com if com else "")
        else:
            com2 = com
        out.append(base + ["Nitrate as N", nitrate_text(q["nitrate"], "CED"), "mg/L", "U" if q["nitrate"] < 0.4 else "",
                           "EPA 300.0", rep, com2])
        out.append(base + ["Arsenic", "%.1f" % q["arsenic"], "ug/L", "U" if q["arsenic"] < 1 else "", "EPA 200.8", rep,
                           com])
        out.append(base + ["Total Coliform", "Present" if q["tc"] else "Absent", "", "", "SM 9223B", rep, com])
        out.append(base + ["E. coli", "Present" if q["ec"] else "Absent", "", "", "SM 9223B", rep, com])
    return out


KIN_COLS = ["SAMPLEID", "CLIENTID", "CNTY", "SAMPLED", "PARAMETER", "VALUE", "UNITS", "FLAG", "VERSION", "REPORTED"]


def kin_rows(recs):
    out = []
    for q in recs:
        base = ["K%06d" % q["sample"], q["kit"], q["county"], str(q["collected"]).replace("-", "")]
        rep = str(q["reported"]).replace("-", "")
        ver = 1
        if q["rerun"] is not None:
            out.append(base + ["NITRATE", nitrate_text(q["rerun"], "KIN"), "mg/L NO3", "", 1,
                               str(q["reported"] - np.timedelta64(3, "D")).replace("-", "")])
            ver = 2
        out.append(base + ["NITRATE", nitrate_text(q["nitrate"], "KIN"), "mg/L NO3", "<" if q["nitrate"] < 0.4 else "",
                           ver, rep])
        out.append(base + ["ARSENIC", "%.1f" % q["arsenic"], "ug/L", "<" if q["arsenic"] < 1 else "", ver, rep])
        out.append(base + ["TC", "POS" if q["tc"] else "NEG", "", "", ver, rep])
        out.append(base + ["EC", "POS" if q["ec"] else "NEG", "", "", ver, rep])
    return out


REQUEST_COLS = ["REQUEST_ID", "COUNTY_CODE", "REQUESTED", "CHANNEL", "ORIGINAL_KIT", "SHIP_TO_ADDRESS", "SHIP_TO_CITY",
                "SHIP_TO_ZIP", "RETEST_KIT", "KIT_MAILED"]


def request_rows(x):
    r = rng(x["seed"], 44)
    out = []
    for c in x["counties"]:
        for q in c["requests"]:
            a = c["addr"][q["well"]]
            orig = c["kit"].get(q["well"], "") if q["via"] == "PORTAL" else ""
            out.append([None, q["route"], str(q["requested"]), q["via"], orig, addr_request(a, r),
                        c["towns"][a["town"]].upper() if q["via"] == "PHONE" else c["towns"][a["town"]],
                        c["zips"][a["town"]], q["kit"], str(q["mailed"])])
    out.sort(key=lambda v: (v[2], v[8]))
    for n, v in enumerate(out):
        v[0] = "RQ%05d" % (20001 + n)
    return out


COUNTY_COLS = ["COUNTY_CODE", "COUNTY", "PERMIT_DB_COUNTY", "ASSESSOR_SHEET", "SURVEY_LAB"]


def county_rows(x):
    return [[c["code"], c["name"], c["name"].upper(), c["code"] + " " + c["name"], W.LABS[c["lab"]]]
            for c in x["counties"]]


LAB_ROSTER_COLS = ["LAB_ID", "LABORATORY", "CITY", "CERTIFIED_FOR", "CERT_EXPIRES"]


def lab_roster_rows():
    return [["NE0112", "Halvorsen Analytical", "Garland", "Nitrate, Nitrite, Arsenic, Coliform/E. coli", "2026-12-31"],
            ["NE0187", "Cedarline Environmental Laboratories", "Pelham", "Inorganics, Metals, Microbiology", "2027-06-30"],
            ["NE0203", "Kinsale Water Testing", "Selby", "Nitrate, Arsenic, Coliform/E. coli", "2026-09-30"],
            ["NE0215", "Upton Municipal Water Laboratory", "Upton", "Microbiology", "2026-03-31"],
            ["NE0221", "Briar Valley Labs", "Briar", "Inorganics, Microbiology, Radionuclides", "2027-01-31"],
            ["NE0230", "Fenton Regional Health Laboratory", "Fenton", "Microbiology", "2025-12-31"],
            ["NE0238", "Tri-County Analytical Services", "Colby", "Nitrate, Nitrite, Fluoride", "2026-11-30"]]


def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        w.writerows(rows)
    return len(rows)
