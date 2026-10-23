"""task176 the remaining pack tables: the grant award workbook, the star ratings, the market rate survey, the data
dictionary and the export manifest."""
from __future__ import annotations

import datetime as dt

import common as C


def write_grants(path, rows):
    import xlsxwriter
    wb = xlsxwriter.Workbook(path)
    hf = wb.add_format({"bold": True, "bg_color": "#DDEBF7", "border": 1, "text_wrap": True, "valign": "top"})
    df = wb.add_format({"num_format": "m/d/yyyy"})
    mf = wb.add_format({"num_format": "#,##0"})
    ws = wb.add_worksheet("Awards")
    ws.write(0, 0, "%s, 2023 round: awards and payments" % C.GRANT)
    ws.write(1, 0, "Grants management export, 6 January 2027. One row per award. The second payment is made after six "
                   "months of licensed operation; a home whose licence ends within twelve months of first issue repays "
                   "under the award terms.")
    for j, h in enumerate(("Award no.", "Licence no.", "County", "Award date", "Award amount", "First payment date",
                           "First payment", "Second payment date", "Second payment", "Recovery date", "Recovered")):
        ws.write(3, j, h, hf)
    for i, r in enumerate(rows, start=4):
        ws.write(i, 0, r[0])
        ws.write(i, 1, r[1])
        ws.write(i, 2, r[2])
        for j, v in ((3, r[3]), (5, r[5]), (7, r[7]), (9, r[9])):
            if v:
                d = dt.date.fromisoformat(v)
                ws.write_datetime(i, j, dt.datetime(d.year, d.month, d.day), df)
        for j, v in ((4, r[4]), (6, r[6]), (8, r[8]), (10, r[10])):
            if v != "":
                ws.write_number(i, j, v, mf)
    for j, w in enumerate((12, 11, 11, 11, 10, 12, 10, 12, 10, 11, 10)):
        ws.set_column(j, j, w)
    ws.freeze_panes(4, 0)
    n = wb.add_worksheet("Notes")
    for i, t in enumerate((
            "Round 2023 was funded from the federal child care relief supplement and closed to applications on 30 November 2023.",
            "Awards of USD 6,000 were made to homes licensed for the first time from 1 February to 30 November 2023 whose "
            "provider applied within 30 days of first issue.",
            "Recoveries are recorded when the repayment is received.")):
        n.write(i, 0, t)
    n.set_column(0, 0, 110)
    wb.close()
    return len(rows)


def qris_rows(homes, ident):
    r = C.stream("qris")
    rows = []
    for h in sorted(homes, key=lambda x: x.hid):
        if h.close is not None and h.close < dt.date(2025, 1, 1):
            continue
        if h.lic > dt.date(2026, 6, 30) or r.random() > 0.57:
            continue
        stars = int(r.choice([1, 2, 3, 4, 5], p=[0.12, 0.31, 0.32, 0.17, 0.08]))
        d = max(h.lic, dt.date(2024, 1, 1)) + dt.timedelta(days=int(r.integers(30, 700)))
        if d > C.RECORD_END:
            d = C.RECORD_END - dt.timedelta(days=int(r.integers(5, 90)))
        rows.append((ident.cur[h.hid], stars, d.isoformat(), (d + dt.timedelta(days=3 * 365)).isoformat(),
                     "Y" if r.random() < 0.18 else "N"))
    rows.sort()
    return rows


def write_qris(path, homes, ident):
    return C.write_csv(path, ("licence_no", "star_rating", "rating_date", "rating_expires", "in_improvement_plan"),
                       qris_rows(homes, ident))


def write_market_rates(path):
    import xlsxwriter
    r = C.stream("market")
    wb = xlsxwriter.Workbook(path)
    hf = wb.add_format({"bold": True, "bg_color": "#FCE4D6", "border": 1, "text_wrap": True})
    mf = wb.add_format({"num_format": "#,##0"})
    ws = wb.add_worksheet("Weekly full-time rates")
    ws.write(0, 0, "2025 Child Care Market Rate Survey: weekly full-time prices charged to private-paying families")
    ws.write(1, 0, "Survey fielded March to May 2025; responses weighted to licensed capacity by county and provider type.")
    head = ("County", "Provider type", "Age group", "Responses", "25th percentile", "Median", "75th percentile")
    for j, h in enumerate(head):
        ws.write(3, j, h, hf)
    i = 4
    for c in C.COUNTIES:
        lvl = 1.0 + (0.22 if c[2] == 2 else 0.0) + r.uniform(-0.08, 0.08)
        for pt, base in (("Family child care", 205), ("Large family child care", 222), ("Centre", 268)):
            for ag, f in (("Infant", 1.26), ("Toddler", 1.15), ("Preschool", 1.0), ("School-age", 0.72)):
                med = base * f * lvl
                n = int(r.integers(6, 60))
                ws.write(i, 0, c[1])
                ws.write(i, 1, pt)
                ws.write(i, 2, ag)
                ws.write_number(i, 3, n)
                ws.write_number(i, 4, round(med * r.uniform(0.84, 0.92)), mf)
                ws.write_number(i, 5, round(med), mf)
                ws.write_number(i, 6, round(med * r.uniform(1.08, 1.18)), mf)
                i += 1
    for j, w in enumerate((11, 22, 11, 10, 12, 9, 12)):
        ws.set_column(j, j, w)
    ws.freeze_panes(4, 0)
    wb.close()
    return i - 4


DICT = [
    (C.F_LIC, "Licensing system extract of every family child care home (small and large) whose licence "
              "was in force on or after 1 January 2016, pulled 8 January 2027 with status as at 31 December 2026. One row "
              "per licence.", [
        ("licence_no", "current licence number (FC and six digits); homes licensed before 1 July 2019 also carry a former "
                       "number, see licence_number_crosswalk_2019.csv"),
        ("licence_type", "SFCC small family child care home (up to eight children); LFCC large family child care home (up to twelve)"),
        ("status", "ACTIVE or CLOSED at the end of 31 December 2026"),
        ("county", "county of the licensed residence"),
        ("zip", "ZIP code of the licensed residence"),
        ("licensed_capacity", "children the licence permits at one time"),
        ("first_licensed_date", "date the licence was first issued"),
        ("closure_effective_date", "date the licence ended; blank while ACTIVE"),
        ("closure_reason", "reason recorded at closure"),
        ("provider_id", "the licensed provider"),
        ("provider_birth_year", "year of birth of the provider; blank where the legacy system did not hold it"),
        ("last_renewal_date", "date of the most recent annual renewal (the first issue date if none)")]),
    (C.F_XW, "Former and current licence numbers of homes licensed before the 1 July 2019 system replacement.", [
        ("legacy_licence_no", "former licence number (F, county code, five digits)"),
        ("licence_no", "current licence number"),
        ("migrated", "2019-07-01 for homes open at the replacement; archived for homes closed before it")]),
    (C.F_WS, "Children listed on capacity worksheets filed from 1 January 2016 to 31 December 2026 (applications, annual "
             "renewals and capacity amendments). One row per child per worksheet. Worksheets filed before 1 July 2019 carry "
             "the former licence number, birth dates as month/day/year and the former relationship codes.", [
        ("licence_ref", "licence number on the worksheet"),
        ("worksheet_date", "date the worksheet was filed"),
        ("worksheet_type", "INITIAL, RENEWAL or AMENDMENT"),
        ("line", "line on the worksheet"),
        ("child_initials", "child's initials"),
        ("child_birth_date", "child's date of birth"),
        ("relationship", "to the provider; from 1 July 2019 C own child, GC grandchild, FC foster child, R other relative; "
                         "before it OWN CHILD, GRANDCHILD, FOSTER, OTHER REL"),
        ("lives_in_home", "Y if the child lives in the licensed residence")]),
    (C.F_GRANT, "Start-up grant awards of the 2023 round, with payments and recoveries. Sheet Awards, one row per award; "
                "sheet Notes.", []),
    (C.F_CCAP, "Child Care Assistance Program remittance lines from the payment runs of 5 January 2026 to 4 January 2027, "
               "every provider type. One row per child per remittance.", [
        ("remittance_no", "remittance number"),
        ("pay_run_date", "date of the payment run"),
        ("county_fips", "county office that issued the remittance"),
        ("provider_no", "licence number for family child care homes; CC centre number; LE license-exempt carer number"),
        ("provider_type", "SFCC small and LFCC large family child care home, CTR centre, EXEMPT license-exempt relative carer"),
        ("case_no", "family's assistance case"),
        ("child_no", "child authorised for care"),
        ("service_from", "first day the line covers"),
        ("service_to", "last day the line covers"),
        ("care_days", "Monday to Friday days from service_from to service_to, both included"),
        ("remittance_amount", "USD, the amount of the remittance"),
        ("remittance_status", "PAID or VOID")]),
    (C.F_CACFP, "Child and Adult Care Food Program claims received for 2026 for sponsored family child care homes, and the "
                "claims centres filed directly. One row per claim received.", [
        ("claim_no", "claim as numbered on receipt"),
        ("sponsor_id", "sponsoring organisation that filed the claim (S01 Allerton Family Day Care Food Program, S02 "
                       "Lakeshore Child Nutrition Services, S03 Valley Home Providers Food Program, S04 Tri-County Child "
                       "Care Food Program); blank for a centre"),
        ("site_licence_no", "licence or centre number of the site"),
        ("county_fips", "county of the site, by name"),
        ("claim_month", "month of service the claim covers"),
        ("received_date", "date the department received the claim"),
        ("operating_days", "days the site served meals in the period claimed"),
        ("enrolled_children", "children enrolled at the site for the period claimed"),
        ("breakfasts", "breakfasts claimed"), ("lunches", "lunches claimed"), ("suppers", "suppers claimed"),
        ("snacks", "snacks claimed")]),
    (C.F_VIS, "Licensing visits recorded for 2026, homes and centres. One row per visit record.", [
        ("visit_no", "visit record"),
        ("licence_no", "licence or centre number"),
        ("facility_type", "SFCC or LFCC family child care home, CTR centre"),
        ("county", "county of the facility"),
        ("visit_date", "date of the visit"),
        ("visit_type", "MONITORING (unannounced annual), COMPLAINT, FOLLOW-UP, RENEWAL (centres)"),
        ("inspector_id", "inspector"),
        ("arrived", "time the inspector arrived, 24-hour clock"),
        ("departed", "time the inspector left"),
        ("status", "COMPLETED or CANCELLED")]),
    (C.F_CTY, "Counties and the department's five regions.", []),
    (C.F_QRIS, "Quality rating and improvement system ratings current in 2025 or 2026 for family child care homes.", []),
]


def write_dictionary(path):
    out = ["Allerton Department of Early Learning, Office of Child Care",
           "Data dictionary for the January 2027 supply folder",
           "Prepared 12 January 2027", ""]
    for f, desc, cols in DICT:
        out.append(f)
        out.append("  " + desc)
        for c, d in cols:
            out.append("  %-24s %s" % (c, d))
        out.append("")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\r\n".join(out) + "\r\n")


def write_manifest(path, counts):
    rows = []
    src = {C.F_LIC: "Licensing system", C.F_XW: "Licensing system", C.F_WS: "Licensing system",
           C.F_GRANT: "Grants management", C.F_CCAP: "CCAP payment system", C.F_CACFP: "CACFP claims system",
           C.F_VIS: "Licensing system", C.F_CTY: "Office of Child Care", C.F_RULES: "Office of Child Care Licensing",
           C.F_POL: "Subsidy Operations", C.F_SUP: "Supply and planning", C.F_QRIS: "Quality ratings office",
           C.F_MRS: "Supply and planning", C.F_DICT: "Supply and planning"}
    pulled = {C.F_RULES: "2025-07-01", C.F_POL: "2025-12-09", C.F_SUP: "2026-10-21", C.F_MRS: "2025-08-14",
              C.F_GRANT: "2027-01-06", C.F_DICT: "2027-01-12", C.F_CTY: "2026-03-02"}
    for f in C.ALL_FILES:
        if f == C.F_MAN:
            continue
        kind = "document" if f.endswith((".pdf", ".txt")) else ("workbook" if f.endswith(".xlsx") else "extract")
        rows.append((f, kind, src[f], pulled.get(f, C.PULL.isoformat()), counts.get(f, "")))
    return C.write_csv(path, ("file_name", "item_type", "system_of_record", "as_of", "record_count"), rows)
