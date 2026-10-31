"""Write the Tamarack County pack's data files from the simulated world: the assessor's roll, the building
inspectors' certificates of occupancy, the demolition permits, the 2020 census block groups, the Center's census
history, the boundary register, the group quarters survey, the county address points and the state registrar's
births and deaths, with the Department of Transportation's road miles and the Census Bureau's county estimates."""
import csv
import datetime as dt
import functools
import zlib

import numpy as np

import sim as S
import world as W

ASSESSOR_NO = {"Town of Ashgrove": "002", "Town of Cedar Run": "006", "Town of Elk Prairie": "010",
               "Town of Glenmoor": "012", "Town of Harwick": "014", "Town of Ivydale": "015", "Town of Kessler": "016",
               "Town of Maple Ford": "018", "Town of Northfield": "020", "Village of Barrow": "106",
               "Village of Fallon": "116", "Village of Ivydale": "131", "Village of Lorne": "146",
               "City of Dunmore": "221", "City of Juniper": "241"}
ASSESSOR_NAME = {m: {"Town": "T", "Village": "V", "City": "C"}[m.split(" ")[0]] + " " + m.split(" of ", 1)[1].upper()
                 for m in ASSESSOR_NO}
LAND_USE = {"SF": ("1010", "SINGLE FAMILY"), "TH2": ("1020", "TWO FAMILY"), "THC": ("1030", "CONDOMINIUM UNIT"),
            "AP": ("1050", "APARTMENTS 4+ UNITS"), "MH": ("1080", "MANUFACTURED HOME"), "VAC": ("1000", "VACANT RESIDENTIAL")}
SUFFIX_LONG = {"ST": "STREET", "AVE": "AVENUE", "DR": "DRIVE", "LN": "LANE", "CT": "COURT", "RD": "ROAD", "CIR": "CIRCLE",
               "TRL": "TRAIL", "PL": "PLACE", "WAY": "WAY", "PKWY": "PARKWAY", "TER": "TERRACE"}


def write_csv(path, header, rows, crlf=True):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def d(x):
    return S.from_frac(x)


@functools.lru_cache(maxsize=None)
def parcels():
    """tax keys: each building's parcel, a two-family house one parcel, a townhouse row one condominium parcel per
    unit, an apartment building one parcel; annexed parcels renumbered into the gaining municipality"""
    w = S.world()
    seq = {}
    key_of_unit, key_of_bldg, prior = {}, {}, {}
    units_of = {}
    for u in w["units"]:
        units_of.setdefault(u["bid"], []).append(u)
    for b in sorted(w["buildings"], key=lambda b: (b["muni"], b["sub"], b["comp"], b["bid"])):
        rb = b.get("rebuild_of")
        us = units_of[b["bid"]]
        if rb is not None:
            key_of_bldg[b["bid"]] = key_of_bldg[rb]
            for u, u0 in zip(us, units_of[rb]):
                key_of_unit[u["uid"]] = key_of_unit[u0["uid"]]
            continue
        m0 = us[0]["annexed"][1] if us[0]["annexed"] else (W.IVY_TOWN[1] if us[0]["ivy_town"] else b["muni"])
        mno = ASSESSOR_NO[m0]
        blk = int(b["sub"].split("-")[1]) * 100 + int(b["sub"].split("-")[2]) + 1
        k = seq.get((mno, blk), 0) + 1
        seq[(mno, blk)] = k
        base = "%s-%04d-%04d" % (mno, blk, k)
        if us[0]["annexed"] or us[0]["ivy_town"]:
            to = b["muni"]
            k2 = seq.get((ASSESSOR_NO[to], 9000 + blk), 0) + 1
            seq[(ASSESSOR_NO[to], 9000 + blk)] = k2
            new = "%s-%04d-%04d" % (ASSESSOR_NO[to], 9000 + blk, k2)
            prior[new] = base
            base = new
        key_of_bldg[b["bid"]] = base
        for i, u in enumerate(us):
            key_of_unit[u["uid"]] = base + ("ABCDEF"[i] if b["type"] == "TH" and b["size"] > 2 else "")
    return key_of_unit, key_of_bldg, prior


def street_of(b):
    return "%d %s %s" % (b["number"], b["street"][0], b["street"][1])


def roll_rows():
    """the roll of 1 January 2026: the residential parcels standing then with their living units and year built; a
    lot whose house came down and was not rebuilt, and a lot whose house was not finished by then, is vacant land"""
    w = S.world()
    ku, kb, _ = parcels()
    x = S.yfrac(W.ROLL)
    r = np.random.default_rng(W.SEED + 21)
    units_of = {}
    for u in w["units"]:
        units_of.setdefault(u["bid"], []).append(u)
    rows = []
    rebuilt = {b["rebuild_of"] for b in w["buildings"] if b.get("rebuild_of") is not None}
    for b in w["buildings"]:
        us = units_of[b["bid"]]
        muni = b["muni"]
        blocks = us[0]["geoid_block"]
        later = b["comp"] > x
        gone = b.get("demolished") is not None and b["demolished"] <= x
        if b.get("rebuild_of") is not None and later:
            continue                      # the old house's row stands for the lot until the new one is valued
        if gone and (b["bid"] in rebuilt):
            nb = [c for c in w["buildings"] if c.get("rebuild_of") == b["bid"]][0]
            if nb["comp"] <= x:
                continue                  # the new house's row carries the lot
        yb = int(b["comp"])
        if yb < 1910 and r.random() < 0.06:
            yb = 0                        # the assessor's placeholder where the year was never recorded
        lv = int(round(np.exp(r.normal(10.6, 0.35)) / 100) * 100)
        if b["type"] == "SF" or b["type"] == "MH" or (b["type"] == "TH" and b["size"] == 2):
            lu = LAND_USE["SF" if b["type"] == "SF" else ("MH" if b["type"] == "MH" else "TH2")]
            n = b["size"]
            keys = [kb[b["bid"]]]
            unit = [""]
        elif b["type"] == "TH":
            lu = LAND_USE["THC"]
            keys = [ku[u["uid"]] for u in us]
            unit = ["UNIT %s" % u["unit"] for u in us]
            n = 1
        else:
            lu = LAND_USE["AP"]
            keys = [kb[b["bid"]]]
            unit = [""]
            n = b["size"]
        for key, un in zip(keys, unit):
            if later or gone:
                rows.append([key, ASSESSOR_NO[muni], ASSESSOR_NAME[muni], "R", LAND_USE["VAC"][0], LAND_USE["VAC"][1],
                             b["number"], b["street"][0], b["street"][1], "", 0, "", lv, 0, blocks, 2026])
                continue
            age = x - b["comp"]
            imp = int(round(np.exp(r.normal(12.2, 0.3)) * (0.55 + 0.45 * np.exp(-age / 40)) * (n if n > 1 else 1) / 100) * 100)
            rows.append([key, ASSESSOR_NO[muni], ASSESSOR_NAME[muni], "R", lu[0], lu[1], b["number"], b["street"][0],
                         b["street"][1], un, n, yb, lv, imp, blocks, 2026])
    rows.sort(key=lambda r_: (r_[1], r_[0]))
    return rows


ROLL_COLS = ["TAXKEY", "MUNI_NO", "MUNI_NAME", "PROP_CLASS", "LAND_USE", "LAND_USE_DESC", "SITUS_NO", "SITUS_STREET",
             "SITUS_SUFFIX", "SITUS_UNIT", "LIVING_UNITS", "YEAR_BUILT", "LAND_VALUE", "IMPR_VALUE", "CENSUS_BLOCK_2020",
             "ROLL_YEAR"]

USE_WORDS = {"SF": "Single-family dwelling", "MH": "Manufactured home", "TH2": "Two-family dwelling",
             "THC": "Townhouse unit", "AP": "Multi-family dwelling"}


def co_rows():
    """certificates of occupancy from 1 January 2020 to 30 June 2026: every new dwelling building's certificate,
    a temporary certificate first on about three in ten, the final weeks later; and the inspectors' certificates for
    commercial buildings, accessory buildings and additions"""
    w = S.world()
    ku, kb, _ = parcels()
    r = np.random.default_rng(W.SEED + 31)
    lo, hi = S.yfrac(W.CO_FROM), S.yfrac(W.CO_TO) + 1 / 365
    units_of = {}
    for u in w["units"]:
        units_of.setdefault(u["bid"], []).append(u)
    rows = []
    pseq = {}
    for b in sorted(w["buildings"], key=lambda b: (b["comp"], b["bid"])):
        if not lo <= b["comp"] < hi:
            continue
        us = units_of[b["bid"]]
        kind = "SF" if b["type"] == "SF" else ("MH" if b["type"] == "MH" else (
            "TH2" if (b["type"] == "TH" and b["size"] == 2) else ("THC" if b["type"] == "TH" else "AP")))
        if kind == "THC":
            items = [(ku[u["uid"]], street_of(b) + " UNIT " + u["unit"], 1) for u in us]
        else:
            items = [(kb[b["bid"]], street_of(b), b["size"])]
        pyear = int(b["comp"] - 0.6)
        pk = (ASSESSOR_NO[b["muni"]], pyear)
        pseq[pk] = pseq.get(pk, 0) + 1
        permit = "%s-%02d-%04d" % (pk[0], pyear % 100, pseq[pk])
        for key, addr, n in items:
            when = d(b["comp"])
            if r.random() < 0.3:
                rows.append([permit, b["muni"], key, addr, "Temporary", when.isoformat(), USE_WORDS[kind], n])
                fin = when + dt.timedelta(days=int(r.integers(18, 85)))
                if fin <= W.CO_TO:
                    rows.append([permit, b["muni"], key, addr, "Final", fin.isoformat(), USE_WORDS[kind], n])
            else:
                rows.append([permit, b["muni"], key, addr, "Final", when.isoformat(), USE_WORDS[kind], n])
    # other certificates the inspectors issue
    munis = [m[1] for m in W.MUNIS]
    for i in range(int(len(rows) * 0.32)):
        m = munis[int(r.integers(0, len(munis)))]
        when = W.CO_FROM + dt.timedelta(days=int(r.integers(0, (W.CO_TO - W.CO_FROM).days)))
        use = ["Commercial building", "Accessory building", "Addition", "Addition", "Accessory building",
               "Change of use"][int(r.integers(0, 6))]
        key = "%s-%04d-%04d" % (ASSESSOR_NO[m], int(r.integers(1, 400)), int(r.integers(1, 90)))
        addr = "%d %s %s" % (int(r.integers(1, 90)) * 10, ["MAIN", "COMMERCE", "INDUSTRIAL", "MARKET", "RAILROAD"][
            int(r.integers(0, 5))], ["ST", "AVE", "DR", "PKWY"][int(r.integers(0, 4))])
        rows.append(["%s-%02d-%04d" % (ASSESSOR_NO[m], when.year % 100, 6000 + i), m, key, addr, "Final",
                     when.isoformat(), use, 0])
    rows.sort(key=lambda r_: (r_[5], r_[0], r_[2]))
    out = []
    for i, row in enumerate(rows, 1):
        out.append(["CO%06d" % (200000 + i * 3)] + row)
    return out


CO_COLS = ["CO_NO", "PERMIT_NO", "JURISDICTION", "TAXKEY", "SITE_ADDRESS", "CO_TYPE", "ISSUED", "USE", "NEW_DWELLING_UNITS"]


def demo_rows():
    """demolition permits since 2000: every house the county lost, with garages, barns and commercial buildings, and
    permits that expired with the building standing"""
    w = S.world()
    ku, kb, _ = parcels()
    r = np.random.default_rng(W.SEED + 41)
    units_of = {}
    for u in w["units"]:
        units_of.setdefault(u["bid"], []).append(u)
    rows = []
    for b in w["buildings"]:
        if b.get("demolished") is None:
            continue
        done = d(b["demolished"])
        issued = done - dt.timedelta(days=int(r.integers(10, 120)))
        u0 = units_of[b["bid"]][0]
        muni = S.muni_on(u0, done)
        rows.append([muni, kb[b["bid"]], street_of(b), USE_WORDS["SF" if b["type"] == "SF" else "MH"], b["size"],
                     int(b["comp"]), "Completed", issued.isoformat(), done.isoformat()])
    n = len(rows)
    standing = [b for b in w["buildings"] if b.get("demolished") is None and b["type"] in ("SF", "MH") and b["comp"] < 1990]
    for i in range(int(n * 0.12)):
        b = standing[int(r.integers(0, len(standing)))]
        issued = dt.date(2000, 1, 1) + dt.timedelta(days=int(r.integers(0, 9600)))
        rows.append([S.muni_on(units_of[b["bid"]][0], issued), kb[b["bid"]], street_of(b),
                     USE_WORDS["SF" if b["type"] == "SF" else "MH"], b["size"], int(b["comp"]), "Expired",
                     issued.isoformat(), ""])
    for i in range(int(n * 1.6)):
        b = standing[int(r.integers(0, len(standing)))]
        issued = dt.date(2000, 1, 1) + dt.timedelta(days=int(r.integers(0, 9600)))
        rows.append([S.muni_on(units_of[b["bid"]][0], issued), kb[b["bid"]], street_of(b),
                     ["Detached garage", "Barn", "Shed", "Commercial building"][int(r.integers(0, 4))], 0, "",
                     "Completed", issued.isoformat(), (issued + dt.timedelta(days=int(r.integers(5, 90)))).isoformat()])
    rows = [rw for rw in rows if rw[7] <= W.CO_TO.isoformat()]
    for rw in rows:
        if rw[8] and rw[8] > W.CO_TO.isoformat():
            rw[6], rw[8] = "Issued", ""
    rows.sort(key=lambda r_: (r_[7], r_[1]))
    return [["DM%02d-%05d" % (int(rw[7][2:4]), 101 + i)] + rw for i, rw in enumerate(rows)]


DEMO_COLS = ["PERMIT_NO", "MUNICIPALITY", "TAXKEY", "ADDRESS", "STRUCTURE", "DWELLING_UNITS", "YEAR_BUILT", "STATUS",
             "ISSUED", "COMPLETED"]


def gq_by_bg(date):
    """each facility's residents at a census, in the block group of the street its era is built on"""
    w = S.world()
    out = {}
    for f, t, m, e, v in S.gq_on(date):
        b = facility_building(f)
        bg = W.STATE_FIPS + W.COUNTY_FIPS + b["tract"] + b["bg"]
        out[bg] = out.get(bg, 0) + v
    return out


@functools.lru_cache(maxsize=None)
def facility_building(f):
    """the building whose street a facility sits on: the first building of its municipality's era"""
    w = S.world()
    for (f_, t, m, e, v) in W.GQ:
        if f_ == f:
            cand = sorted((b for b in w["buildings"] if b["muni"] == m and b["era"] == e and b["type"] == "SF"
                           and b.get("demolished") is None and not b.get("rebuild_of")), key=lambda b: (b["comp"], b["bid"]))
            same = [x[0] for x in W.GQ if x[2] == m and x[3] == e]
            k = same.index(f)
            return cand[len(cand) * (2 * k + 1) // (2 * len(same))]     # each facility on its own street


def bg2020_rows():
    w = S.world()
    occ, size = S.households(W.C2020)
    x = S.yfrac(W.C2020)
    agg = {}
    for u in w["units"]:
        if not S.standing(u, x):
            continue
        a = agg.setdefault(u["geoid_bg"], [0, 0, 0])
        a[0] += int(size[u["uid"]])
        a[1] += 1
        a[2] += int(occ[u["uid"]])
    gq = gq_by_bg(W.C2020)
    for bg in set(u["geoid_bg"] for u in w["units"]):
        agg.setdefault(bg, [0, 0, 0])
    rows = []
    for bg in sorted(agg):
        hp, hu, oc = agg[bg]
        g = gq.get(bg, 0)
        tr = bg[5:11]
        name = "Block Group %s; Census Tract %s; %s" % (bg[11], "%d" % (int(tr) // 100) if int(tr) % 100 == 0
                                                                 else "%.2f" % (int(tr) / 100), W.COUNTY)
        rows.append(["1500000US" + bg, name, hp + g, hp, g, hu, oc, hu - oc])
    return rows


BG_COLS = ["GEO_ID", "NAME", "P1_001N", "P15_001N", "P18_001N", "H1_001N", "H1_002N", "H1_003N"]
BG_LABELS = ["Geography", "Geographic Area Name", " !!Total", " !!Total:!!Population in households",
             " !!Total:!!Population in group quarters", " !!Total", " !!Total:!!Occupied", " !!Total:!!Vacant"]


def history():
    """each census's municipalities on that census's boundaries"""
    w = S.world()
    out = {}
    for date in (W.C2000, W.C2010, W.C2020):
        occ, size = S.households(date)
        x = S.yfrac(date)
        agg = {}
        for u in w["units"]:
            if not S.standing(u, x):
                continue
            m = S.muni_on(u, date)
            a = agg.setdefault(m, [0, 0, 0])
            a[0] += int(size[u["uid"]])
            a[1] += 1
            a[2] += int(occ[u["uid"]])
        gq = {}
        for f, t, m, e, v in S.gq_on(date):
            gq[m] = gq.get(m, 0) + v
        out[date.year] = {m: (a[0] + gq.get(m, 0), a[0], gq.get(m, 0), a[1], a[2]) for m, a in agg.items()}
    return out


def boundary_rows():
    w = S.world()
    ku, kb, prior = parcels()
    rows = []
    for when, frm, to, era, n in W.ANNEX:
        keys = sorted({kb[u["bid"]] for u in w["units"] if u["annexed"] and u["annexed"][0] == when})
        filing = "A-%d-%03d" % (when.year, 11 + era + len(rows) % 7)
        for k in keys:
            rows.append([filing, "Annexation", when.isoformat(), frm, to, k, prior.get(k, ""),
                         "Ord. %d-%02d" % (when.year, 3 + len(rows) % 9)])
    rows.append(["C-2023-001", "Consolidation", W.CONSOLIDATION.isoformat(), W.IVY_TOWN[1], "Village of Ivydale",
                 "", "", "Joint Res. 2023-4"])
    return rows


BOUNDARY_COLS = ["FILING_NO", "CHANGE_TYPE", "EFFECTIVE", "FROM_MUNICIPALITY", "TO_MUNICIPALITY", "TAXKEY",
                 "PRIOR_TAXKEY", "ENACTMENT"]


def unit_address(b, u):
    if b["type"] == "AP":
        return "APT %s" % u["unit"]
    if b["type"] == "TH" and b["size"] > 2:
        return "UNIT %s" % u["unit"]
    if b["type"] == "TH":
        return "UNIT %s" % u["unit"]
    return ""


def points_rows():
    """address points: one for each dwelling unit and group quarters facility, retired when the dwelling came down,
    and the county's commercial and other points"""
    w = S.world()
    r = np.random.default_rng(W.SEED + 51)
    x26 = S.yfrac(W.EST)
    rows = []
    centre = {m[1]: (1520000 + 26000 * (i % 4), 352000 + 31000 * (i // 4)) for i, m in enumerate(W.MUNIS)}
    units_of = {}
    for u in w["units"]:
        units_of.setdefault(u["bid"], []).append(u)
    for b in w["buildings"]:
        if b["comp"] > x26:
            continue
        cx, cy = centre[b["muni"]]
        bx = cx + (zlib.crc32(b["sub"].encode()) % 9000) - 4500 + r.normal(0, 600)
        by = cy + (zlib.crc32(b["sub"][::-1].encode()) % 9000) - 4500 + r.normal(0, 600)
        created = d(b["comp"]) if b["comp"] > 2008 else dt.date(2008, 6, 2)
        retired = d(b["demolished"]) if b.get("demolished") else None
        units = units_of[b["bid"]] if b["size"] > 1 else [None]
        for u in units:
            unit = unit_address(b, u) if u else ""
            rows.append([b["number"], "", b["street"][0], b["street"][1], unit, W.CODE[b["muni"]], b["zip"], b["postal"],
                         "Residential", "Retired" if retired else "Active", created.isoformat(),
                         retired.isoformat() if retired else "", int(bx), int(by)])
    for f, t, m, e, v in W.GQ:
        b = facility_building(f)
        rows.append([b["number"] + 1, "", b["street"][0], b["street"][1], "", W.CODE[m], b["zip"], b["postal"],
                     "Institutional", "Active", "2008-06-02", "", int(centre[m][0]), int(centre[m][1])])
    for i in range(3600):
        m = W.MUNIS[int(r.integers(0, len(W.MUNIS)))][1]
        b = w["buildings"][int(r.integers(0, len(w["buildings"])))]
        if b["muni"] != m:
            continue
        rows.append([b["number"] + 1 + int(r.integers(0, 3)) * 2, "", b["street"][0], b["street"][1], "", W.CODE[m],
                     b["zip"], b["postal"], ["Commercial", "Commercial", "Utility", "Other"][int(r.integers(0, 4))],
                     "Active", "2008-06-02", "", int(centre[m][0]), int(centre[m][1])])
    # a point is unique on number, street and unit
    seen, out = set(), []
    for row in rows:
        k = (row[0], row[2], row[3], row[4], row[9])
        if k in seen:
            continue
        seen.add(k)
        out.append(row)
    out.sort(key=lambda r_: (r_[5], r_[2], r_[0], r_[4]))
    return [["%07d" % (1000000 + 7 * i)] + row for i, row in enumerate(out)]


POINT_COLS = ["ADDRPT_ID", "ADD_NUM", "PRE_DIR", "ST_NAME", "ST_TYPE", "UNIT", "MCD", "ZIP", "POSTAL_CITY", "PT_TYPE",
              "STATUS", "CREATED", "RETIRED", "X_SP", "Y_SP"]


def written_address(b, u, r):
    """how an address reaches a vital record: the suffix spelled out or abbreviated, the unit written in its forms"""
    suf = b["street"][1]
    if r.random() < 0.45:
        suf = SUFFIX_LONG[suf]
    s = "%d %s %s" % (b["number"], b["street"][0], suf)
    un = unit_address(b, u) if u is not None else ""
    if un:
        lab, val = un.split(" ")
        form = r.random()
        s += (" %s %s" % (lab, val)) if form < 0.5 else ((" #%s" % val) if form < 0.8 else (" %s%s" % (lab.title(), " " + val)))
    if r.random() < 0.55:
        s = s.title()
    return s


def births_rows():
    w = S.world()
    births, _ = S.vital()
    r = np.random.default_rng(W.SEED + 61)
    rows = []
    seq = {}
    hosp = ["TAMARACK REGIONAL MEDICAL CENTER", "TAMARACK REGIONAL MEDICAL CENTER", "ST. ANSGAR HOSPITAL - LAKEPORT",
            "JUNIPER COMMUNITY HOSPITAL"]
    for e in births:
        u = w["units"][e["uid"]]
        b = w["buildings"][u["bid"]]
        when = d(e["when"])
        filed = when + dt.timedelta(days=int(r.integers(2, 21)))
        if filed < dt.date(2025, 7, 1) or filed > dt.date(2026, 8, 15):
            continue
        city = S.written_city(u["muni"], b["postal"], r)
        addr = written_address(b, u, r)
        fac = hosp[int(r.integers(0, len(hosp)))]
        for k in range(2 if e["twin"] else 1):
            yr = filed.year
            seq[yr] = seq.get(yr, 0) + 1
            rows.append(["%d-%06d" % (yr, 40000 + seq[yr] * 3), when.isoformat(), e["sex"] if k == 0 else "MF"[int(r.integers(0, 2))],
                         2 if e["twin"] else 1, e["mage"], addr, city, b["zip"], "TAMARACK", fac, filed.isoformat()])
    rows.sort(key=lambda r_: (r_[10], r_[0]))
    return rows


BIRTH_COLS = ["CERT_NO", "CHILD_DOB", "CHILD_SEX", "PLURALITY", "MOTHER_AGE", "RES_STREET", "RES_CITY", "RES_ZIP", "RES_COUNTY", "BIRTH_FACILITY", "DATE_FILED"]


def deaths_rows():
    w = S.world()
    _, deaths = S.vital()
    r = np.random.default_rng(W.SEED + 71)
    rows = []
    seq = {}
    for e in deaths:
        when = d(e["when"])
        filed = when + dt.timedelta(days=int(r.integers(3, 30)))
        if filed < dt.date(2025, 7, 1) or filed > dt.date(2026, 8, 15):
            continue
        if e["uid"] is not None:
            u = w["units"][e["uid"]]
            b = w["buildings"][u["bid"]]
            muni = u["muni"]
            addr = written_address(b, u, r)
            place = ["Hospital inpatient", "Decedent's home", "Decedent's home", "Hospice facility", "Other"][int(r.integers(0, 5))]
            fac = "" if place in ("Decedent's home", "Other") else "TAMARACK REGIONAL MEDICAL CENTER"
        else:
            f = [x for x in W.GQ if x[0] == e["gq"]][0]
            b = facility_building(f[0])
            muni = f[2]
            addr = "%d %s %s" % (b["number"] + 1, b["street"][0], b["street"][1] if r.random() < 0.5 else SUFFIX_LONG[b["street"][1]])
            if r.random() < 0.55:
                addr = addr.title()
            place, fac = "Nursing facility", f[0].upper()
        city = S.written_city(muni, b["postal"], r, share=0.30)    # a funeral director writes the mailing city
        if when < W.EDRS_SWITCH:
            # the funeral director's city, coded to the municipality of that name
            cu = city.upper().replace("TOWN OF ", "").replace("VILLAGE OF ", "").replace("CITY OF ", "")
            cu = cu.replace(" TWP", "").replace(" VLG", "").replace(" CITY", "")
            mcd = [m[0] for m in W.MUNIS if m[1].split(" of ", 1)[1].upper() == cu][0]
        else:
            mcd = W.CODE[muni]
        yr = filed.year
        seq[yr] = seq.get(yr, 0) + 1
        rows.append(["%d%06d" % (yr, 21000 + seq[yr] * 7), when.isoformat(), e["age"], e["sex"], addr, city, b["zip"],
                     "TAMARACK", W.STATE_FIPS + W.COUNTY_FIPS + mcd, place, fac, filed.isoformat()])
    rows.sort(key=lambda r_: (r_[11], r_[0]))
    return rows


DEATH_COLS = ["STATE_FILE_NO", "DATE_OF_DEATH", "AGE_YEARS", "SEX", "RES_STREET", "RES_CITY", "RES_ZIP",
              "RES_COUNTY", "RES_MCD_CODE", "PLACE_OF_DEATH", "FACILITY", "DATE_FILED"]


def vintage_rows():
    """the Census Bureau's Vintage 2025 county estimates for the state's counties"""
    r = np.random.default_rng(W.SEED + 81)
    t = S.truth()
    tam26 = sum(t.values())
    rows = []
    for fips, name, base in (("001", "Abbott County", 41822), ("013", "Corliss County", 18730), ("027", "Elmore County", 66105),
                             ("041", W.COUNTY, None), ("053", "Lakeport County", 152344), ("069", "Pruett County", 23910)):
        if base is None:
            c20 = sum(v[0] for v in history()[2020].values())
            vals = [c20]
            for k in range(1, 6):
                vals.append(int(round(c20 + (tam26 - c20) * (k + 0.25) / 6.25 * (1 + r.normal(0, 0.002)))))
        else:
            g_ = r.normal(0.004, 0.004)
            vals = [base] + [int(round(base * (1 + g_) ** (k + 0.25))) for k in range(1, 6)]
        rows.append(["0500000US57%s" % fips, name, vals[0]] + vals)
    return rows


VINTAGE_COLS = ["GEO_ID", "NAME", "ESTIMATESBASE2020", "POPESTIMATE2020", "POPESTIMATE2021", "POPESTIMATE2022",
                "POPESTIMATE2023", "POPESTIMATE2024", "POPESTIMATE2025"]
