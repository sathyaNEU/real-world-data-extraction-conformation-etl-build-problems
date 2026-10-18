"""The exports, each in its producer's own layout: the regional commuting extract (main and auxiliary parts), the
survey's public-use file, the census population table, the gazetteer, the delineation list, the planning map and
the distractors. Each writer returns the rows it wrote."""
import csv
import math

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font

import common as K
import world as W

CREATEDATE = "20250303"
SA = {"SI01": (.19, .57, .24), "SI02": (.31, .49, .20), "SI03": (.21, .58, .21)}
SE = {"SI01": (.12, .31, .57), "SI02": (.24, .39, .37), "SI03": (.16, .26, .58)}


def tract_name(code):
    whole, part = int(code[:4]), int(code[4:])
    return "Census Tract %d" % whole + (".%02d" % part if part else "")


def county_names():
    out = {}
    for m in K.METROS:
        st = K.STATES[m["st"]][0]
        out[st + m["central"][1]] = m["central"][0]
        for nm, c in m["outlying"]:
            out[st + c] = nm
        for nm, c, _ in m["outside"]:
            out[st + c] = nm
    return out


def od_rows(Wd):
    """Every flow as the agency writes it: total, three age bands, three earnings bands, three industry groups."""
    out = []
    for i, M in enumerate(Wd["metros"]):
        r = np.random.default_rng([W.SEED, i, 7])
        for (h, w), gs in sorted(M["flows"].items(), key=lambda kv: (kv[0][1], kv[0][0])):
            n = sum(gs.values())
            sa, se = np.zeros(3, int), np.zeros(3, int)
            for g, c in gs.items():
                if c:
                    sa += r.multinomial(c, SA[g])
                    se += r.multinomial(c, SE[g])
            out.append([w, h, n] + list(map(int, sa)) + list(map(int, se)) + [gs["SI01"], gs["SI02"], gs["SI03"],
                                                                                CREATEDATE])
    out.sort(key=lambda x: (x[0], x[1]))
    return out


def write_od(path_main, path_aux, Wd):
    head = ["w_tract", "h_tract", "S000", "SA01", "SA02", "SA03", "SE01", "SE02", "SE03", "SI01", "SI02", "SI03",
            "createdate"]
    rows = od_rows(Wd)
    main = [x for x in rows if x[0][:2] == x[1][:2]]
    aux = [x for x in rows if x[0][:2] != x[1][:2]]
    for path, part in ((path_main, main), (path_aux, aux)):
        with open(path, "w", newline="") as f:
            wr = csv.writer(f, lineterminator="\n")
            wr.writerow(head)
            wr.writerows(part)
    return len(main), len(aux)


def write_survey(path, Wd):
    age = {b: i + 1 for i, b in enumerate(W.AGE_BANDS)}
    edu = {b: i + 1 for i, b in enumerate(W.EDUC)}
    rows = sorted(Wd["survey"], key=lambda x: (x["wave"], x["rid"]))
    with open(path, "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["WAVE", "RESPID", "FINALWT", "AGEGRP", "SEX", "EDUC", "NAICS_SECTOR", "HOMEREL", "DAYS_PREM",
                     "DAYS_HOME", "DAYS_NOTWORK"])
        for x in rows:
            wr.writerow([x["wave"].replace("-", ""), x["rid"], "%.2f" % x["weight"], age[x["age"]], x["sex"],
                         edu[x["edu"]], x["sector"], x["rel"], x["prem"], x["home"], x["off"]])
    return len(rows)


def cbsa_tracts(Wd):
    """Every tract of the six metropolitan areas' counties (the central county and its outlying counties)."""
    out = []
    for M in Wd["metros"]:
        for t in M["tracts"]:
            if t["county"] == M["central"] or t["county"] in M["outlying"]:
                out.append(t)
    return sorted(out, key=lambda t: t["geoid"])


def write_population(path, Wd):
    names = county_names()
    r = np.random.default_rng([W.SEED, 31])
    rows = []
    for t in cbsa_tracts(Wd):
        st = [v for v in K.STATES.values() if v[0] == t["geoid"][:2]][0][1]
        est = int(round(t["R"]))
        moe = 13 if est == 0 else int(round(est * float(r.uniform(.07, .19)) + float(r.uniform(40, 160))))
        rows.append(["1400000US" + t["geoid"], "%s; %s County; %s" % (tract_name(t["geoid"][5:]), names[t["county"]], st),
                     est, moe])
    with open(path, "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["GEO_ID", "NAME", "B01003_001E", "B01003_001M"])
        wr.writerow(["Geography", "Geographic Area Name", "Estimate!!Total", "Margin of Error!!Total"])
        wr.writerows(rows)
    return len(rows)


def write_gazetteer(path, Wd):
    usps = {v[0]: k for k, v in K.STATES.items()}
    r = np.random.default_rng([W.SEED, 32])
    lines = ["USPS\tGEOID\tALAND\tAWATER\tALAND_SQMI\tAWATER_SQMI\tINTPTLAT\tINTPTLONG" + " " * 117]
    n = 0
    for t in cbsa_tracts(Wd):
        aland = int(round(t["area"] * 1e6))
        if t["kind"] == "water":
            awater = int(round(t["water"] * 1e6))
        else:
            awater = 0 if r.random() < .62 else int(round(aland * float(r.uniform(.001, .06))))
        lines.append("%s\t%s\t%d\t%d\t%.3f\t%.3f\t%.6f\t%.6f" % (usps[t["geoid"][:2]], t["geoid"], aland, awater,
                                                                  aland / 2589988.110336, awater / 2589988.110336,
                                                                  t["lat"], t["lon"]))
        n += 1
    with open(path, "w", newline="") as f:
        f.write("\n".join(lines) + "\n")
    return n


def delineation_rows(Wd):
    rows = []
    for m in K.METROS:
        st, stname = K.STATES[m["st"]]
        title = "%s, %s" % (m["name"], m["st"])
        rows.append([m["cbsa"], "", "", title, "Metropolitan Statistical Area", "", "", m["central"][0] + " County",
                     stname, st, m["central"][1], "Central"])
        for nm, c in m["outlying"]:
            rows.append([m["cbsa"], "", "", title, "Metropolitan Statistical Area", "", "", nm + " County", stname, st,
                         c, "Outlying"])
        for nm, c, other in m["outside"]:
            if other:
                rows.append([other[0], "", "", "%s, %s" % (other[1], m["st"]), "Micropolitan Statistical Area", "", "",
                             nm + " County", stname, st, c, "Central"])
    rows.sort(key=lambda x: (x[0], x[11] != "Central", x[7]))
    return rows


def write_delineation(path, Wd):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "List 1"
    ws["A1"] = ("List 1. CORE BASED STATISTICAL AREAS (CBSAs), METROPOLITAN DIVISIONS, AND COMBINED STATISTICAL "
                "AREAS (CSAs)")
    ws["A2"] = "July 2023"
    head = ["CBSA Code", "Metropolitan Division Code", "CSA Code", "CBSA Title", "Metropolitan/Micropolitan Statistical Area",
            "Metropolitan Division Title", "CSA Title", "County/County Equivalent", "State Name", "FIPS State Code",
            "FIPS County Code", "Central/Outlying County"]
    ws.append(head)
    rows = delineation_rows(Wd)
    for x in rows:
        ws.append([v if v != "" else None for v in x])
    ws.append([])
    ws.append(["Note: The 2020 Standards for Delineating Core Based Statistical Areas appear in the Federal Register "
               "(86 FR 37770-37778) on July 16, 2021."])
    ws.append(["Source: File prepared by U.S. Census Bureau, Population Division, based on Office of Management and "
               "Budget, July 2023 delineations <https://www.whitehouse.gov/wp-content/uploads/2023/07/OMB-Bulletin-23-01.pdf>."])
    ws.append(["Internet Release Date: July 2023"])
    ws.append(["Rows kept: the candidate metropolitan areas and the areas next to them, Location Analytics, "
               "September 2026."])
    for c, wdt in zip("ABCDEFGHIJKL", [11, 14, 9, 26, 34, 22, 14, 26, 16, 9, 9, 13]):
        ws.column_dimensions[c].width = wdt
    for cell in ws[3]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for row in ws.iter_rows(min_row=4, max_row=3 + len(rows)):
        for cell in row:
            cell.number_format = "@"
    wb.save(path)
    return len(rows)


ZONES = ["Downtown", "Market Quarter", "Riverside", "Old Town", "North End", "Westgate", "Eastside", "Southbank",
         "Mill District", "Union Square", "Hillcrest", "Parkview"]


def write_cores(path, Wd):
    names = county_names()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Core tracts"
    ws.append(["Metro", "State", "County", "Tract", "Tract name", "Planning zone"])
    n = 0
    for M in Wd["metros"]:
        r = np.random.default_rng([W.SEED, 41, K.METRO_NAMES.index(M["metro"]["name"])])
        core = sorted((t for t in M["tracts"] if t["core"]), key=lambda t: t["geoid"])
        zones = ZONES[:]
        r.shuffle(zones)
        for t in core:
            if t["kind"] == "cbd":
                zone = "Downtown"
            else:
                ang = math.atan2(t["y"], t["x"])
                zone = zones[1 + int(((ang + math.pi) / (2 * math.pi)) * 5) % 5]
                if zone == "Downtown":
                    zone = zones[7]
            ws.append([M["metro"]["name"], M["metro"]["st"], names[t["county"]] + " County", t["geoid"],
                       tract_name(t["geoid"][5:]), zone])
            n += 1
    for row in ws.iter_rows(min_row=2):
        row[3].number_format = "@"
    for c, wdt in zip("ABCDEF", [13, 7, 19, 14, 20, 16]):
        ws.column_dimensions[c].width = wdt
    for cell in ws[1]:
        cell.font = Font(bold=True)
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("About")
    for line in ["Planning map: the cores of the six candidate metros for the 2027 weekday pilot, as the board paper "
                 "of 17 September 2026 refers to them.",
                 "A core is the set of 2020 census tracts listed here for its metro; the planning zones are the "
                 "network team's own labels and carry no weight.",
                 "Prepared by Location Analytics, September 2026."]:
        ws2.append([line])
    ws2.column_dimensions["A"].width = 110
    wb.save(path)
    return n


# ------------------------------------------------------------------------------------------------- distractors
def county_people(Wd):
    """Residents of every county the extract's flows reach in the six states, from the world's tracts."""
    out, kind = {}, {}
    for M in Wd["metros"]:
        for t in M["tracts"]:
            out[t["county"]] = out.get(t["county"], 0.0) + t["R"]
            kind[t["county"]] = t["kind"] if t["kind"] in ("outlying", "outside") else "central"
    return out, kind


def write_acs_commute(path, Wd):
    """ACS 2018-2022 five-year B08301, means of transportation to work, by county of residence."""
    names = county_names()
    people, kind = county_people(Wd)
    r = np.random.default_rng([W.SEED, 51])
    wfh_mean = {"central": .078, "outlying": .101, "outside": .066}
    rows = []
    for c in sorted(people):
        stname = [v[1] for v in K.STATES.values() if v[0] == c[:2]][0]
        tot = int(round(people[c] * W.EMP * float(r.uniform(.96, 1.03))))
        wfh = int(round(tot * wfh_mean[kind[c]] * float(r.uniform(.85, 1.15))))
        transit = int(round(tot * {"central": .046, "outlying": .012, "outside": .004}[kind[c]] * float(r.uniform(.7, 1.3))))
        walk = int(round(tot * float(r.uniform(.012, .03))))
        bike = int(round(tot * float(r.uniform(.002, .007))))
        other = int(round(tot * float(r.uniform(.008, .015))))
        car = tot - wfh - transit - walk - bike - other
        vals = [tot, car, transit, bike, walk, wfh]
        moes = [int(round(v * float(r.uniform(.006, .02)) + 40)) for v in vals]
        rows.append(["0500000US" + c, "%s County, %s" % (names[c], stname)] + [x for pair in zip(vals, moes) for x in pair])
    head = ["GEO_ID", "NAME"]
    lab = ["Geography", "Geographic Area Name"]
    for code, l in (("001", "Total:"), ("002", "Total:!!Car, truck, or van:"), ("010", "Total:!!Public transportation (excluding taxicab):"),
                    ("018", "Total:!!Bicycle"), ("019", "Total:!!Walked"), ("021", "Total:!!Worked from home")):
        head += ["B08301_%sE" % code, "B08301_%sM" % code]
        lab += ["Estimate!!" + l, "Margin of Error!!" + l]
    with open(path, "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(head)
        wr.writerow(lab)
        wr.writerows(rows)
    return len(rows)


def write_cbp(path, Wd):
    """County Business Patterns 2022: establishments and employment by county and two-digit sector."""
    names = county_names()
    people, kind = county_people(Wd)
    r = np.random.default_rng([W.SEED, 52])
    rows = []
    for c in sorted(people):
        if kind[c] == "outside":
            continue
        stname = [v[1] for v in K.STATES.values() if v[0] == c[:2]][0]
        jobs = people[c] * (.62 if kind[c] == "central" else .31)
        for code, title, g in K.SECTORS:
            if code in ("92",):
                continue
            share = {"SI01": .17, "SI02": .21, "SI03": .62}[g] / sum(1 for s in K.SECTORS if s[2] == g and s[0] != "92")
            emp = int(round(jobs * share * float(r.lognormal(0, .35))))
            if emp < 20:
                continue
            est = max(3, int(round(emp / float(r.uniform(9, 24)))))
            rows.append(["%s County, %s" % (names[c], stname), code, title, est, emp,
                         int(round(emp * float(r.uniform(38, 96)))), c[:2], c[2:]])
    with open(path, "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["NAME", "NAICS2017", "NAICS2017_LABEL", "ESTAB", "EMP", "PAYANN", "state", "county"])
        wr.writerows(rows)
    return len(rows)


def write_expansion(path):
    """The home metro's dark-store launch log, kept by Network Expansion."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Launches"
    head = ["Store", "Neighbourhood", "Opened", "Service hours", "Floor area (sq ft)", "Couriers at opening",
            "Weekday orders per day, weeks 1-4", "Weeks 5-8", "Weeks 9-12", "Share of weekday orders to workplaces, weeks 9-12",
            "Notes"]
    ws.append(head)
    r = np.random.default_rng([W.SEED, 53])
    hoods = ["Canal Ward", "Fenmarket", "Old Quay", "Hollins Park", "St Anselm", "Brewery Row", "Westmoor", "Kiln Street",
             "Gallows Green", "Upper Dock", "Tanner's Yard", "Northfield", "Lantern Hill"]
    d = [2023, 3, 6]
    notes = ["", "", "Opened in a former bank branch", "", "Courier shortfall in week 3", "", "Shares a loading bay",
             "", "Weekend hours added in month 4", "", "", "Moved from Kiln St unit 4 to unit 9 in week 7", ""]
    for i, h in enumerate(hoods):
        o1 = int(r.integers(120, 240))
        o2 = int(o1 * float(r.uniform(1.25, 1.6)))
        o3 = int(o2 * float(r.uniform(1.08, 1.3)))
        opened = "%04d-%02d-%02d" % (d[0], d[1], d[2])
        ws.append(["TR-%02d" % (i + 1), h, opened, "Mon-Fri 9:00-18:00" if i < 9 else "Mon-Sun 8:00-22:00",
                   int(r.integers(32, 46)) * 100, int(r.integers(9, 19)), o1, o2, o3, round(float(r.uniform(.18, .44)), 2),
                   notes[i] or None])
        d[1] += int(r.integers(2, 4))
        if d[1] > 12:
            d[0], d[1] = d[0] + 1, d[1] - 12
    for c, wdt in zip("ABCDEFGHIJK", [8, 16, 11, 18, 10, 10, 13, 10, 10, 14, 40]):
        ws.column_dimensions[c].width = wdt
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    wb.save(path)
    return len(hoods)


# ------------------------------------------------------------------------------------------------- the asks' files
def write_listings(path, L):
    head = ["listing_id", "address", "suite", "city", "state", "zip", "census_tract", "property_type", "floor", "space_sf",
            "asking_rent", "rent_basis", "lease_type", "status", "status_date", "date_listed", "broker"]
    with open(path, "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(head)
        for x in L:
            rent = x["asking_rent"]
            wr.writerow([x["listing_id"], x["address"], x["suite"], x["city"], x["state"], x["zip"], x["census_tract"],
                         x["property_type"], x["floor"], x["space_sf"], ("%.0f" % rent) if x["rent_basis"] == "/MO" else "%.2f" % rent,
                         x["rent_basis"], x["lease_type"], x["status"], x["status_date"], x["date_listed"], x["broker"]])
    return len(L)


def write_locators(path, rows):
    head = ["scrape_date", "brand", "store_code", "store_name", "address", "unit", "city", "state", "zip", "latitude",
            "longitude", "census_tract", "services", "hours"]
    with open(path, "w", newline="") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(head)
        for x in rows:
            wr.writerow([x[h] for h in head])
    return len(rows)
