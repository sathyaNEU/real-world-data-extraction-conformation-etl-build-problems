"""Write the bundle's data files: the register extract, the quarterly reports, the wage records, the county codes
and the three files the bureau keeps beside them (population estimates, the Secretary of State's entity filings, the
program's grant disbursements)."""
import csv
import datetime as dt
import io

import numpy as np

import econ as E
import names as N
import world as W

QS = W.QUARTERS


def account_numbers(world):
    """Legacy accounts keep the numbers the old system gave them; accounts opened since the 2025 replacement are
    numbered in registration order (other employers across the state register in between)."""
    rng = np.random.default_rng(W.SEED + 11)
    used = set()
    nums = {}
    legacy = [a for a in world.accts if a.reg < W.LEGACY_CUTOVER]
    for a in sorted(legacy, key=lambda a: (a.reg, a.idx)):
        while True:
            n = "%d%08d" % (int(rng.integers(1, 8)), int(rng.integers(0, 10 ** 8)))
            if n not in used:
                used.add(n)
                nums[a.idx] = n
                break
    seq = 214_337
    for a in sorted((a for a in world.accts if a.reg >= W.LEGACY_CUTOVER), key=lambda a: (a.reg, a.idx)):
        seq += 1 + int(rng.geometric(1 / 41.0))
        n = "8%08d" % seq
        used.add(n)
        nums[a.idx] = n
    return nums


def address_text(a):
    ad = a.addr
    if a.reg < W.LEGACY_CUTOVER:
        return N.fmt_legacy(ad["num"], ad["dirn"], ad["street"], ad["stype"], ad["suite"]), ad["town"]
    return N.fmt_usps(ad["num"], ad["dirn"], ad["street"], ad["stype"], ad["suite"]), ad["town"].upper()


def register_rows(world, nums):
    rows = []
    for a in world.accts:
        street, city = address_text(a)
        legacy = a.reg < W.LEGACY_CUTOVER
        inact = a.inact if (a.inact is not None and a.inact <= W.EXTRACT) else None
        pred = ""
        tdate = ""
        if a.kind == "succ" and a.succ_type == "filed":
            pred = nums[a.source]
            tdate = a.first.isoformat()
        rows.append({
            "account_no": nums[a.idx], "legal_name": a.legal, "trade_name": a.trade, "fein": a.fein,
            "worksite_address": street, "worksite_city": city, "worksite_zip": a.zip,
            "county_code": W.CODE[a.county], "naics_code": a.naics17 if legacy else a.naics22,
            "naics_vintage": "2017" if legacy else "2022", "ownership_code": "5",
            "registration_date": a.reg.isoformat(), "liability_date": a.liab.isoformat() if a.liab else "",
            "status": "INACTIVE" if inact else "ACTIVE", "inactivation_date": inact.isoformat() if inact else "",
            "predecessor_account": pred, "transfer_date": tdate,
        })
    rows.sort(key=lambda r: r["account_no"])
    return rows


REGISTER_COLS = ["account_no", "legal_name", "trade_name", "fein", "worksite_address", "worksite_city", "worksite_zip",
                 "county_code", "naics_code", "naics_vintage", "ownership_code", "registration_date", "liability_date",
                 "status", "inactivation_date", "predecessor_account", "transfer_date"]
QCEW_COLS = ["account_no", "year", "qtr", "county_code", "naics_code", "own_code", "month1_emplvl", "month2_emplvl",
             "month3_emplvl", "total_qtrly_wages", "taxable_qtrly_wages"]


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\r\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return len(rows)


def qcew_rows(world, d, nums):
    A = world.accts
    rows = []
    for r in d["qrows"]:
        a = A[r["acct"]]
        y, q = QS[r["qi"]]
        rows.append({"account_no": nums[a.idx], "year": y, "qtr": q, "county_code": r["county"], "naics_code": a.naics22,
                     "own_code": "5", "month1_emplvl": r["m1"], "month2_emplvl": r["m2"], "month3_emplvl": r["m3"],
                     "total_qtrly_wages": "%.2f" % r["wages"], "taxable_qtrly_wages": "%.2f" % r["taxable"]})
    rows.sort(key=lambda r: (r["year"], r["qtr"], r["account_no"]))
    return rows


def write_wages(path, world, S, d, nums):
    keys = {}
    out = io.StringIO()
    out.write("worker_key|account_no|year|qtr|wages\r\n")
    rows = []
    for wk, ac, qi, v in d["wage_rows"]:
        if wk not in keys:
            keys[wk] = N.worker_key(wk)
        y, q = QS[qi]
        rows.append((y, q, nums[ac], keys[wk], v))
    rows.sort()
    for y, q, ac, k, v in rows:
        out.write("%s|%s|%d|%d|%.2f\r\n" % (k, ac, y, q, v))
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(out.getvalue())
    return len(rows)


def write_counties(path):
    rows = [{"county_code": c, "county_name": n, "region": "Lornock Valley Development Region", "county_seat": s}
            for c, n, s, _ in W.COUNTIES]
    return write_csv(path, ["county_code", "county_name", "region", "county_seat"], rows)


POP = {"Brennock": 41_873, "Caldmere": 17_914, "Dunrath": 33_406, "Eskwell": 18_652, "Fennamore": 29_731,
       "Quarrin": 21_288, "Tolbeck": 15_207}
GROWTH = {"Brennock": 0.0041, "Caldmere": -0.0022, "Dunrath": 0.0063, "Eskwell": 0.0087, "Fennamore": -0.0011,
          "Quarrin": 0.0024, "Tolbeck": 0.0102}


def write_population(path):
    """The state demographer's July 1 estimates (vintage 2026) for the seven counties."""
    rng = np.random.default_rng(W.SEED + 21)
    rows = []
    for code, name, _, _ in W.COUNTIES:
        p = POP[name]
        for y in range(2020, 2027):
            pop = int(round(p * (1 + GROWTH[name]) ** (y - 2020) + rng.normal(0, 40)))
            wa = int(round(pop * (0.603 - 0.0021 * (y - 2020)) + rng.normal(0, 25)))
            rows.append({"county_code": code, "county_name": name, "estimate_date": "%d-07-01" % y,
                         "vintage": "V2026", "total_population": pop, "population_16_to_64": wa})
    return write_csv(path, ["county_code", "county_name", "estimate_date", "vintage", "total_population",
                            "population_16_to_64"], rows)


def write_sos(path, world, nums):
    """New business entity filings with the Secretary of State, 2025 and 2026, principal office in the valley: the
    entities of the region's new employer accounts and many entities that never hire."""
    rng = np.random.default_rng(W.SEED + 31)
    rows = []
    seen = set()
    for a in world.accts:
        if a.reg < W.LEGACY_CUTOVER or a.legal in seen:
            continue
        if rng.random() < 0.08:
            continue
        seen.add(a.legal)
        date = a.reg - dt.timedelta(days=int(rng.integers(6, 120)))
        county = a.county if rng.random() < 0.86 else W.ORDER[int(rng.integers(len(W.ORDER)))]
        if date.year >= 2025:
            rows.append((date, a.legal, county))
    namer = N.Namer(np.random.default_rng(W.SEED + 32))
    namer.legal |= seen
    for k in range(1240):
        county = W.ORDER[int(rng.choice(7, p=np.array([0.26, 0.09, 0.19, 0.11, 0.15, 0.12, 0.08])))]
        style = ["Holdings", "Properties", "Investments", "Ventures", "Rentals", "Farms", "Consulting", "Trust"]
        base = "%s %s" % (N.SURNAMES[int(rng.integers(len(N.SURNAMES)))] if rng.random() < 0.6
                          else W.PLACE_WORDS[int(rng.integers(len(W.PLACE_WORDS)))],
                          style[int(rng.integers(len(style)))])
        legal = "%s LLC" % base
        if legal in namer.legal:
            legal = "%s %s LLC" % (base, ["II", "Group", "of the Valley", "Partners"][int(rng.integers(4))])
        if legal in namer.legal:
            continue
        namer.legal.add(legal)
        date = dt.date(2025, 1, 2) + dt.timedelta(days=int(rng.integers(0, 728)))
        rows.append((date, legal, county))
    rows.sort(key=lambda r: (r[0], r[1]))
    out = []
    for i, (date, legal, county) in enumerate(rows):
        et = "Limited Liability Company" if legal.endswith("LLC") else (
            "Professional Corporation" if legal.endswith((" PC", " PLLC")) else
            "Limited Liability Partnership" if legal.endswith("LLP") else "Business Corporation")
        town = next(c for c in W.COUNTIES if c[1] == county)[2]
        status = "Active" if rng.random() > 0.0398 else "Administratively Dissolved"
        out.append({"filing_number": "%s%07d" % ("L" if et.startswith("Limited") else "C", 4_210_000 + 37 * i + int(rng.integers(0, 30))),
                    "filing_date": date.isoformat(), "entity_name": legal, "entity_type": et,
                    "principal_office_city": town, "principal_office_county": county, "status": status})
    return write_csv(path, ["filing_number", "filing_date", "entity_name", "entity_type", "principal_office_city",
                            "principal_office_county", "status"], out)


def write_grants(path):
    """Payments in fiscal year 2026 to the development authorities of the 2025 to 2027 cycle's Formation Counties."""
    import openpyxl
    from openpyxl.styles import Font
    rng = np.random.default_rng(W.SEED + 41)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Disbursements FY2026"
    ws.append(["Formation Counties Program: grant disbursements, fiscal year 2026 (1 July 2025 to 30 June 2026)"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Department of Commerce, Office of Business Development. Grant period 2025 to 2027."])
    ws.append([])
    ws.append(["Payment date", "Grantee", "County", "Grant number", "Purpose", "Amount (USD)"])
    for c in ws[4]:
        c.font = Font(bold=True)
    grantees = [("Brennock County Economic Development Authority", "Brennock", "FC-2025-011"),
                ("Fennamore County Development Corporation", "Fennamore", "FC-2025-053"),
                ("Eskwell Area Development Partnership", "Eskwell", "FC-2025-041")]
    purposes = ["Small business development center staffing", "Microloan fund capitalisation",
                "Incubator space lease", "Entrepreneur training cohort", "Storefront improvement matching grants"]
    for m in range(12):
        d0 = dt.date(2025 + (m + 6) // 12, (m + 6) % 12 + 1, 1)
        for g, county, num in grantees:
            if m % 3 != 0 and rng.random() < 0.55:
                continue
            d = d0 + dt.timedelta(days=int(rng.integers(3, 27)))
            while d.weekday() >= 5:
                d += dt.timedelta(days=1)
            amt = round(float(rng.uniform(21_000, 74_000)), 2)
            ws.append([d, g, county, num, purposes[int(rng.integers(len(purposes)))], amt])
            ws.cell(ws.max_row, 1).number_format = "yyyy-mm-dd"
            ws.cell(ws.max_row, 6).number_format = "#,##0.00"
    ws.column_dimensions["A"].width = 13
    ws.column_dimensions["B"].width = 46
    ws.column_dimensions["E"].width = 44
    ws.column_dimensions["F"].width = 14
    wb.save(path)
    return ws.max_row - 4
