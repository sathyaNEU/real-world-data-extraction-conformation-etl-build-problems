"""The independent verifier: reads only the shipped bundle (target/ and golden/), on its own code path (its own PDF and
workbook readers, its own matching of DSS's town names, its own handling of the grants data system's exports), and
recomputes every graded figure: the nine allocations, the nine averages and 27 region-years, the default path's
allocation, the transition figures, and each figure's distance to its rounding edge, against figures.json and the
golden deliverables.

    python3 verify.py [target] [golden] [figures.json]
"""
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
import zipfile

import openpyxl

FILES = dict(
    rel2021="sdc_poverty_estimates_dec2021.pdf", rel2022="sdc_poverty_estimates_dec2022.pdf",
    rel2023="sdc_poverty_estimates_dec2023.pdf", rel2024="sdc_poverty_estimates_dec2024_transition.pdf",
    rel2025="sdc_poverty_estimates_2024_planning_regions.xlsx", acs="acs5_2020_2024_b17001_towns_regions.csv",
    snap="dss_snap_participation_by_town_2019_2026.txt", codes="town_county_region_codes.csv",
    rule="obp_rof_fy2027_allocation_rule.pdf", closeout="rof_fy2026_closeout.xlsx",
    extract="rof_client_services_extract_20260930.csv", audit="rof_gds_profile_audit_fy2026.csv",
    conversion="cca_client_number_conversion_20260101.csv", layout="rof_gds_export_layout.txt")
OK = []


def ok(label, cond, detail=""):
    OK.append(bool(cond))
    print("%s  verify: %s%s" % ("ok  " if cond else "FAIL", label, ("  [%s]" % detail) if (detail and not cond) else ""))


def raw_pdf(path):
    return subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True, check=True).stdout


def release(path):
    """Table 1 and Table 2 from a release read in raw mode: a row is a code, a name and the counts after it."""
    tabs, cur, years = {}, None, {}
    for line in raw_pdf(path).splitlines():
        m = re.search(r"Table ([12])\. Residents in poverty, (\d{4})", line)
        if m:
            cur = int(m.group(1))
            years[cur] = int(m.group(2))
            tabs[cur] = {}
            continue
        m = re.match(r"^(52\d{3}) ([A-Za-z .]+?) ([\d,]+)\b", line.strip())
        if cur and m:
            tabs[cur][m.group(2).strip()] = int(m.group(3).replace(",", ""))
    return tabs, years


def main(target, golden, fig_path):
    del OK[:]
    p = lambda k: os.path.join(target, FILES[k])
    F = json.load(open(fig_path, encoding="utf-8"))
    rule = re.sub(r"\s+", " ", raw_pdf(p("rule")))
    fund = int(re.search(r"appropriation, \$([\d,]+)", rule).group(1).replace(",", ""))
    ok("the rule's fund is $%s" % "{:,}".format(fund), fund == F["fund"])
    # codes
    with open(p("codes"), encoding="utf-8") as fh:
        codes = list(csv.DictReader(fh))
    county = {r["town"]: r["former_county"] for r in codes}
    region = {r["town"]: r["planning_region"] for r in codes}
    by_geo = {"0600000US" + r["town_geoid_region_basis"]: r["town"] for r in codes}
    # the SDC's estimates, the latest publication of each year wins
    est = {}
    for k in ("rel2021", "rel2022", "rel2023", "rel2024"):
        tabs, years = release(p(k))
        for t in (1, 2):
            for area, v in tabs[t].items():
                if area != "State":
                    est[(area, years[t])] = v
    wb = openpyxl.load_workbook(p("rel2025"), data_only=True)
    for sheet, year in (("Table 1", 2024), ("Table 2", 2023)):
        for row in wb[sheet].iter_rows(values_only=True):
            if row and isinstance(row[0], str) and re.fullmatch(r"52\d{3}", row[0]):
                est[(row[1], year)] = int(row[2])
    counties = sorted({r["former_county"] for r in codes})
    regions = [r["planning_region"] for r in sorted(codes, key=lambda r: r["region_fips"])]
    regions = list(dict.fromkeys(regions))
    ok("every former county has 2020 to 2022 and every region 2023 and 2024",
       all((c, y) in est for c in counties for y in (2020, 2021, 2022)) and
       all((g, y) in est for g in regions for y in (2023, 2024)))
    # the survey's town counts
    below = {}
    with open(p("acs"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["table_line"] == "B17001_002" and r["geo_id"] in by_geo:
                below[by_geo[r["geo_id"]]] = int(r["estimate"])
    ok("the survey's below-poverty count for all %d towns" % len(below), len(below) == len(codes))
    # DSS's names, expanded back to the codes file's
    exp = [(r"^E ", "EAST "), (r"^N ", "NORTH "), (r"^W ", "WEST "), (r"^LWR ", "LOWER "), (r"^UPR ", "UPPER "),
           (r" CTR$", " CENTER"), (r"-", " ")]
    upper = {t.upper(): t for t in county}
    snap = {}
    with open(p("snap"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter="|"):
            n = r["TOWN"]
            for a, b in exp:
                n = re.sub(a, b, n)
            if n in upper:
                ym = r["BENEFIT_MONTH"]
                snap[(upper[n], int(ym[:4]), int(ym[4:]))] = int(r["RECIPIENTS"])
    ok("DSS's names expanded match all %d towns" % len({k[0] for k in snap}), len({k[0] for k in snap}) == len(codes))
    yearly = {(t, y): sum(snap[(t, y, m)] for m in range(1, 13)) / 12.0 for t in county for y in range(2020, 2025)}

    def build(town_year):
        ser = {g: {} for g in regions}
        for y in (2020, 2021, 2022):
            for g in regions:
                ser[g][y] = 0.0
            for c in counties:
                ts = [t for t in county if county[t] == c]
                w = {t: town_year(t, y) for t in ts}
                s = sum(w.values())
                for t in ts:
                    ser[region[t]][y] += est[(c, y)] * w[t] / s
        for y in (2023, 2024):
            for g in regions:
                ser[g][y] = float(est[(g, y)])
        avg = {g: sum(ser[g].values()) / 5.0 for g in regions}
        tot = sum(avg.values())
        return ser, avg, {g: fund * avg[g] / tot for g in regions}
    five = {t: sum(yearly[(t, y)] for y in range(2020, 2025)) / 5.0 for t in county}
    ser, avg, amt = build(lambda t, y: yearly[(t, y)] * below[t] / five[t])
    r10k = lambda v: int(round(v / 10000.0)) * 10000
    r100 = lambda v: int(round(v / 100.0)) * 100
    ok("the nine allocations recompute from the bundle", all(r10k(amt[g]) == F["amounts"][g] for g in regions),
       {g: r10k(amt[g]) for g in regions})
    ok("the nine averages and 27 region-years recompute", all(r100(avg[g]) == F["average"][g] for g in regions) and
       all(r100(ser[g][y]) == F["cells"][g][str(y)] for g in regions for y in (2020, 2021, 2022)))
    ok("the averages sum to %s" % "{:,}".format(r100(sum(avg.values()))), r100(sum(avg.values())) == F["average_sum"])
    e = lambda v, u: u / 2.0 - abs(v - round(v / u) * u)
    ea = min(e(amt[g], 10000) for g in regions)
    ev = min(e(avg[g], 100) for g in regions)
    ec = min(e(ser[g][y], 100) for g in regions for y in (2020, 2021, 2022))
    ok("every graded main figure clear of its rounding edge (amounts %.0f, averages %.1f, cells %.1f)" % (ea, ev, ec),
       ea > 500 and ev > 5 and ec > 3)
    _, _, amt0 = build(lambda t, y: float(below[t]))
    ok("the default path (the release's shares) files the rival amounts the write-up names",
       all(r10k(amt0[g]) == F["rivals"]["release_shares"][g] for g in regions))
    ratios = [below[t] / five[t] for t in county]
    ok("the towns' ratio runs %.2f to %.2f" % (min(ratios), max(ratios)),
       [round(min(ratios), 2), round(max(ratios), 2)] == F["ratio_range"])
    # the transition figures, by this verifier's own handling of the exports
    def rows(k):
        with open(p(k), encoding="utf-8", newline="") as fh:
            rd = csv.reader(fh)
            next(rd)
            return [tuple(r) for r in rd]
    ext = list(dict.fromkeys(rows("extract")))               # a repeated upload counts once
    ext = [r for r in ext if "2025-07-01" <= r[4] <= "2026-06-30"]
    newno = {a: b for a, b, _ in rows("conversion")}
    person = lambda c: newno.get(c, c)
    moves = {}
    for a in rows("audit"):
        if a[2] == "town":
            moves.setdefault(person(a[1]), []).append((a[5], a[3], a[4]))

    def lived(r):
        h = sorted(moves.get(person(r[1]), []))
        town = h[0][1] if h else r[6]
        for eff, old, new in h:
            if eff <= r[4]:
                town = new
        return town
    layout = open(p("layout"), encoding="utf-8").read()
    agency_name = dict(re.findall(r"\b(HCCAA|CCA|WOC|AGCS|LCAP|MCA|SACA|PCAC) ([A-Z][A-Za-z ]+?)(?:;|\n)",
                                  layout.replace("\n                  ", " ")))
    wbc = openpyxl.load_workbook(p("closeout"), data_only=True)["FY2026 closeout"]
    unexp, county_of_agency = {}, {}
    for row in wbc.iter_rows(values_only=True):
        if row and isinstance(row[0], str) and row[0].startswith("ROF-"):
            unexp[row[2]] = int(row[5])
            county_of_agency[row[1]] = row[2]
    code_county = {c: county_of_agency[n.strip()] for c, n in agency_name.items()}
    ok("the layout's eight agency codes map to the closeout's eight agencies", len(code_county) == 8)
    served = {}
    for r in ext:
        served.setdefault((code_county[r[0]], region[lived(r)]), set()).add(person(r[1]))
    carry = {g: 0.0 for g in regions}
    people = {g: 0 for g in regions}
    for c in counties:
        n = {g: len(v) for (cc, g), v in served.items() if cc == c}
        for g, k in n.items():
            carry[g] += unexp[c] * k / sum(n.values())
            people[g] += k
    paid, energy = set(), {g: 0.0 for g in regions}
    for r in ext:
        if r[3] == "EA" and (r[2], r[4]) not in paid:
            paid.add((r[2], r[4]))
            energy[region[lived(r)]] += float(r[7])
    ok("each council's share of the unexpended balances recomputes",
       all(int(round(carry[g] / 100.0)) * 100 == F["asks"]["carry"][g] for g in regions))
    ok("the people each share is counted on recompute", all(people[g] == F["asks"]["people"][g] for g in regions))
    ok("the energy assistance paid in each council's towns recomputes",
       all(int(round(energy[g] / 100.0)) * 100 == F["asks"]["energy"][g] for g in regions))
    ok("every transition figure clear of its $100 edge", min(e(v, 100) for v in list(carry.values()) +
                                                            list(energy.values())) > 5)
    # the golden deliverables against figures.json
    with open(os.path.join(golden, "rof_fy2027_region_poverty.csv"), encoding="utf-8") as fh:
        g_rows = list(csv.DictReader(fh))
    ok("the golden CSV carries every region-year and average", all(
        int(r["residents_in_poverty_%d" % y]) == F["cells"][r["planning_region"]][str(y)] and
        int(r["average_2020_2024"]) == F["average"][r["planning_region"]] for r in g_rows for y in (2020, 2021, 2022)))
    with zipfile.ZipFile(os.path.join(golden, "rof_fy2027_allocation_memo.docx")) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    body = re.sub(r"<[^>]+>", "", xml)
    fm = lambda v: "{:,}".format(v)
    ok("the memo states the nine allocations and the transition figures",
       all(("$" + fm(F["amounts"][g])) in body and ("$" + fm(F["asks"]["carry"][g])) in body and
           ("$" + fm(F["asks"]["energy"][g])) in body for g in regions))
    good = all(OK)
    print("verify: %d checks, %s" % (len(OK), "all pass" if good else "%d failed" % OK.count(False)))
    return good


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    a = sys.argv[1:]
    main(a[0] if a else os.path.join(task, "target"), a[1] if len(a) > 1 else os.path.join(task, "golden"),
         a[2] if len(a) > 2 else os.path.join(here, "figures.json"))
