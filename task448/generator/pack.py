"""Write the pack's data files: the HMDA loan-level file and reporter panel, the recorder vendor's three deliveries
and its delivery register, the mortgagee alias register, the lender register, the board's shortlist, the two
neighbouring files, and the export manifest."""
import csv
import datetime as dt

import numpy as np
import pandas as pd

import sim as S
import world as W

FILES = {
    "lar": "hmda_lar_kansas_2024_2025.csv",
    "panel": "hmda_reporter_panel_2024_2025.csv",
    "feed24": "venridge_pmm_ks8_2024.txt",
    "feed25": "venridge_pmm_ks8_2025.txt",
    "feed26": "venridge_pmm_ks8_2026ytd.txt",
    "deliveries": "venridge_delivery_register.csv",
    "alias": "mortgagee_alias_register.csv",
    "register": "lender_register_2026-09.csv",
    "shortlist": "rural_lender_shortlist_2027.xlsx",
    "agg2023": "hmda_2023_county_summary_ks.csv",
    "education": "homebuyer_education_completions_2024_2026.csv",
    "manifest": "export_manifest.csv",
}
DISTRACTORS = ["agg2023", "education"]
V3 = ["REC_KEY", "STATE", "CNTY_FIPS", "CNTY_NAME", "MTG_DOC_NO", "MTG_REC_DATE", "MTG_INSTR_DATE", "MTG_AMT",
      "MORTGAGEE_NAME", "MORTGAGOR_NAME", "DEED_DOC_NO", "DEED_REC_DATE", "DEED_TYPE", "DEED_CONSIDERATION",
      "GRANTOR_NAME", "GRANTEE_NAME", "APN", "SITUS_ADDR", "SITUS_CITY", "SITUS_ZIP", "LEGAL_BRIEF", "DOC_REMARKS",
      "LOAD_DATE"]
V4 = ["REC_KEY", "CNTY_FIPS", "CNTY_NAME", "APN", "SITUS_ADDR", "SITUS_CITY", "SITUS_ZIP", "MTG_DOC_NO", "RECORDING_DT",
      "DOC_DT", "LOAN_AMT", "LENDER_NAME", "BORROWER_NAME", "LOAN_TYPE_HINT", "DEED_DOC_NO", "DEED_RECORDING_DT",
      "DEED_TYPE", "SALE_AMT", "SELLER_NAME", "BUYER_NAME", "LEGAL_BRIEF", "REMARKS", "LOAD_TS"]
AGENCY = {"NB": 7, "CU": 5}


def write_lar(out, path):
    out.to_csv(path, index=False, lineterminator="\n")
    return len(out)


def write_panel(LX, path):
    rng = np.random.default_rng(W.SEED + 51)
    rows = []
    for y in (2024, 2025):
        for x in LX:
            if x["kind"] != "R":
                continue
            if x["ch"] == "NB":
                agency, assets, olc = 7, "", 0
            elif x["ch"] == "CU":
                agency, assets, olc = 5, int(x["rows"] * rng.uniform(1900, 2600) * (1.04 if y == 2025 else 1)), 0
            else:
                agency = 1 if x["name"].endswith("N.A.") else 3
                assets = int(x["rows"] * rng.uniform(1500, 2600) * (1.05 if y == 2025 else 1))
                olc = 0
            parent = ""
            if x["id"] == "REG1":
                parent = "ARKHAVEN BANCSHARES, INC."
            elif x["id"] == "REG2":
                parent = "SHUNGA VALLEY FINANCIAL CORPORATION"
            rows.append(dict(activity_year=y, lei=x["lei"], agency_code=agency, id_rssd=x["rssd"] if x["rssd"] else -1,
                             respondent_name=x["name"].upper(), respondent_city=x["hq"][0].upper(),
                             respondent_state=x["hq"][1], parent_name=parent, assets=assets, other_lender_code=olc))
    P = pd.DataFrame(rows).sort_values(["activity_year", "respondent_name"], kind="mergesort")
    P.to_csv(path, index=False, lineterminator="\n")
    return len(P)


def _d3(d):
    return d.strftime("%m/%d/%Y")


def write_feed(F, year, path):
    if year < 2026:
        G = F[F.mtg_rec.map(lambda d: d.year) == year]
        cols = V3
    else:
        G = F[F.mtg_rec.map(lambda d: d.year) == 2026]
        cols = V4
    G = G.sort_values(["county", "mtg_rec", "mtg_doc"], kind="mergesort")
    hint = {"CONV": "CONV", "FHA": "FHA", "VA": "VA", "USDA": "USDA-RD"}
    rng = np.random.default_rng(W.SEED + 52 + year)
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, delimiter="|", lineterminator="\r\n", quoting=csv.QUOTE_NONE, escapechar="\\")
        wr.writerow(cols)
        for r in G.itertuples():
            if year < 2026:
                wr.writerow([r.rec_key, "KS", W.FIPS[r.county], r.county.upper(), r.mtg_doc, _d3(r.mtg_rec), _d3(r.instr),
                             "%.2f" % r.amount, r.mortgagee, r.mortgagor, r.deed_doc, _d3(r.deed_rec), r.deed_type,
                             r.consideration, r.grantor, r.grantee, r.apn, r.addr, r.city.upper(), r.zip, r.legal,
                             r.remarks, _d3(r.load)])
            else:
                h = hint.get(r.ltype, "") if (r.ltype and rng.random() < 0.83) else ""
                wr.writerow([r.rec_key, W.FIPS[r.county], r.county.upper(), r.apn, r.addr, r.city.upper(), r.zip,
                             r.mtg_doc, r.mtg_rec.isoformat(), r.instr.isoformat(), "%d" % r.amount, r.mortgagee,
                             r.mortgagor, h, r.deed_doc, r.deed_rec.isoformat(), r.deed_type, r.consideration,
                             r.grantor, r.grantee, r.legal, r.remarks,
                             "%sT0%d:%02d:00" % (r.load.isoformat(), int(rng.integers(2, 6)), int(rng.integers(0, 60)))])
    return len(G)


def write_deliveries(F, counts, path):
    rows = [dict(delivery_id="VPD-KS8-2024-A", file_name=FILES["feed24"], layout="PMM v3", counties="8",
                 recordings_from="2024-01-01", recordings_to="2024-12-31", rows=counts["feed24"],
                 delivered="2025-01-17", note="annual file"),
            dict(delivery_id="VPD-KS8-2025-A", file_name=FILES["feed25"], layout="PMM v3", counties="8",
                 recordings_from="2025-01-01", recordings_to="2025-12-31", rows=counts["feed25"],
                 delivered="2026-01-16", note="annual file"),
            dict(delivery_id="VPD-KS8-2026-YTD08", file_name=FILES["feed26"], layout="PMM v4", counties="8",
                 recordings_from="2026-01-01", recordings_to="2026-08-31", rows=counts["feed26"],
                 delivered="2026-09-15", note="year to date; first delivery in layout v4")]
    pd.DataFrame(rows).to_csv(path, index=False, lineterminator="\n")
    return len(rows)


def write_alias(F, LX, path):
    import recorder as RC
    by = {x["id"]: x for x in LX}
    seen = F[F.lender != ""].groupby(["mortgagee", "lender"]).mtg_rec.agg(["min", "max"]).reset_index()
    rng = np.random.default_rng(W.SEED + 53)
    rows = []
    for r in seen.itertuples():
        x = by[r.lender]
        note = "MERS as nominee" if r.mortgagee.startswith(("MERS", "MORTGAGE ELECTRONIC")) else (
            "exact" if r.mortgagee == x["name"].upper() else "variant")
        rev = S.next_bday(r.min + dt.timedelta(days=int(rng.integers(20, 90))))
        if rev >= W.PULL:
            rev = dt.date(2026, 10, 7) - dt.timedelta(days=int(rng.integers(0, 4)))
        # matches first seen in the 2026 delivery wait for the desk's quarterly review
        seen26 = r.min >= dt.date(2026, 6, 1) and rng.random() < 0.7
        rows.append(dict(mortgagee_as_indexed=r.mortgagee, nmls_id=x["nmls"], lender_name=x["name"], match=note,
                         first_seen=r.min.isoformat(), reviewed="" if seen26 else rev.isoformat()))
    A = pd.DataFrame(rows).sort_values(["lender_name", "mortgagee_as_indexed"], kind="mergesort")
    A.to_csv(path, index=False, lineterminator="\n")
    return len(A)


def _verified(x):
    """The desk re-checked the board's shortlist before the September meeting; every other lender keeps the date
    it was last looked up, from the register's set-up in March 2025 on."""
    if x["id"] in W.OFFICES:
        return "2026-09-08"
    return ("2025-03-14", "2025-06-02", "2025-11-20", "2026-01-29", "2026-04-07", "2026-06-23")[int(x["nmls"]) % 6]


def write_register(LX, path):
    kinds = {"NB": "Mortgage company", "CU": "Credit union", "CB": "Bank", "RB": "Bank"}
    rows = []
    for x in sorted(LX, key=lambda x: x["name"]):
        if x["ch"] == "CU":
            charter = "Federal credit union" if "Federal" in x["name"] else "State credit union"
        elif x["ch"] == "NB":
            charter = "Licensed mortgage company"
        else:
            charter = "National bank" if x["name"].endswith("N.A.") or "National" in x["name"] else "State bank"
        rows.append(dict(nmls_id=x["nmls"], legal_name=x["name"], institution_type=kinds[x["ch"]], charter=charter,
                         hq_city=x["hq"][0], hq_state=x["hq"][1], lei=x["lei"], rssd_id=x["rssd"],
                         service_area_offices=W.OFFICES.get(x["id"], ""), last_verified=_verified(x)))
    pd.DataFrame(rows).to_csv(path, index=False, lineterminator="\n")
    return len(rows)


def write_shortlist(LX, path):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    by = {x["id"]: x for x in LX}
    notes = {"BIG1": "Wichita program participant since 2019; loan officers cover Salina", "BIG2": "",
             "BIG3": "Asked about a rural expansion at the June lender breakfast", "REG1": "Wichita program participant",
             "REG2": "Topeka program; Abilene branch opened 2023", "CUR2": "Wichita program; Salina branch only",
             "CBR1": "Raised by a director at the September meeting", "N1": "Proposed at the September meeting; three Salina offices",
             "N2": "Met at the McPherson housing fair (May 2026)", "N3": "Marion County commission suggested",
             "N4": "", "N5": "Called the office in August asking about the program"}
    order = ["N2", "BIG2", "REG1", "N5", "CBR1", "N4", "BIG1", "N3", "REG2", "BIG3", "N1", "CUR2"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Shortlist"
    ws.append(["No.", "Lender", "Type", "Headquarters", "NMLS ID", "Offices in the service area", "Notes"])
    for k, i in enumerate(order, 1):
        x = by[i]
        ws.append([k, x["name"], x["label"], "%s, %s" % x["hq"], x["nmls"], W.OFFICES[i], notes[i] or None])
    head = Font(bold=True, color="FFFFFF")
    for c in ws[1]:
        c.font = head
        c.fill = PatternFill("solid", fgColor="3B5B3A")
        c.alignment = Alignment(vertical="center", wrap_text=True)
    widths = [5, 32, 24, 18, 11, 30, 52]
    for col, wd in zip("ABCDEFG", widths):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("Board request")
    lines = ["2027 rural down-payment program: participating lender recruitment",
             "Shortlist agreed at the board meeting of 24 September 2026, twelve lenders proposed by board members "
             "and staff.",
             "Staff to bring the recruitment order to the December meeting.",
             "Prepared by the research desk; contacts to be assigned after the December meeting."]
    for ln in lines:
        ws2.append([ln])
    ws2["A1"].font = Font(bold=True)
    ws2.column_dimensions["A"].width = 110
    wb.save(path)
    return len(order)


def write_agg2023(path):
    """The FFIEC 2023 aggregate view the desk kept from last year's work: originations by county, purpose and
    loan type."""
    rng = np.random.default_rng(W.SEED + 54)
    import lar as LR
    cw = LR.county_weights()
    rows = []
    for c in W.KS_COUNTIES:
        base = (W.COUNTY_W[c] * 5.2 if c in W.REGION else cw[c]) * 440
        for purpose, pname, share in ((1, "Home purchase", 0.56), (31, "Refinancing", 0.12),
                                      (32, "Cash-out refinancing", 0.18), (2, "Home improvement", 0.09),
                                      (4, "Other purpose", 0.05)):
            for lt, lname, ls in ((1, "Conventional", 0.71), (2, "FHA", 0.15), (3, "VA", 0.08), (4, "FSA/RHS", 0.06)):
                n = int(rng.poisson(max(0.2, base * share * ls)))
                if n == 0 and rng.random() < 0.5:
                    continue
                rows.append(dict(activity_year=2023, county_code=W.FIPS[c], county_name=c + " County",
                                 loan_purpose=purpose, loan_purpose_desc=pname, loan_type=lt, loan_type_desc=lname,
                                 originations=n, loan_amount_000=int(n * rng.uniform(140, 260))))
    pd.DataFrame(rows).to_csv(path, index=False, lineterminator="\n")
    return len(rows)


def write_education(path):
    rng = np.random.default_rng(W.SEED + 55)
    rows = []
    d = dt.date(2024, 1, 1)
    while d <= dt.date(2026, 8, 1):
        for c in W.REGION:
            for fmt in ("In person", "Online"):
                lam = W.COUNTY_W[c] * 46 * (0.6 if fmt == "In person" else 0.4) * (1.25 if d.month in (2, 3, 4) else 1)
                n = int(rng.poisson(lam))
                if n == 0 and fmt == "In person":
                    continue
                ft = int(rng.binomial(n, 0.81))
                rows.append(dict(month=d.strftime("%Y-%m"), county=c, class_format=fmt, completions=n,
                                 first_time_buyers=ft))
        d = (d.replace(day=28) + dt.timedelta(days=5)).replace(day=1)
    pd.DataFrame(rows).to_csv(path, index=False, lineterminator="\n")
    return len(rows)


MANIFEST = [
    ("lar", "HMDA loan-level records, Kansas, activity years 2024 and 2025, every action and purpose",
     "FFIEC HMDA Data Browser, state = KS, years 2024 and 2025; fields kept as listed in the field dictionary",
     "2026-10-06", "Public data (FFIEC HMDA), no restrictions"),
    ("panel", "HMDA reporter panel rows for the institutions with records in the eight counties",
     "FFIEC HMDA reporter panel, 2024 and 2025", "2026-10-06", "Public data (FFIEC HMDA), no restrictions"),
    ("feed24", "Purchase-money mortgage file, eight counties, recordings of 2024", "Venridge Property Data, LLC",
     "2025-01-17", "Subscription; internal use under the Venridge data agreement"),
    ("feed25", "Purchase-money mortgage file, eight counties, recordings of 2025", "Venridge Property Data, LLC",
     "2026-01-16", "Subscription; internal use under the Venridge data agreement"),
    ("feed26", "Purchase-money mortgage file, eight counties, recordings of January to August 2026",
     "Venridge Property Data, LLC", "2026-09-15", "Subscription; internal use under the Venridge data agreement"),
    ("deliveries", "Venridge deliveries received for the eight counties", "Research desk", "2026-10-09", "Internal"),
    ("alias", "Mortgagee names as indexed by the recorders, matched to lenders by NMLS ID", "Research desk",
     "2026-10-08", "Internal"),
    ("register", "Lenders known to the fund, with identifiers", "Research desk (NMLS Consumer Access, NCUA, FFIEC NIC)",
     "2026-09-08", "Internal"),
    ("shortlist", "The board's twelve-lender shortlist for the 2027 rural program", "Board of directors",
     "2026-09-24", "Internal"),
    ("agg2023", "HMDA 2023 originations by county, purpose and loan type, Kansas", "FFIEC HMDA aggregate data, 2023",
     "2025-10-14", "Public data (FFIEC HMDA), no restrictions"),
    ("education", "Homebuyer education completions by month, county and class format", "Program operations",
     "2026-10-02", "Internal"),
    ("guidelines", "Rural Down-Payment Assistance Program guidelines, 2027", "Board of directors, approved 2026-06-18",
     "2026-06-18", "Internal"),
    ("layout", "Venridge purchase-money mortgage file: layout guide, v3 and v4", "Venridge Property Data, LLC",
     "2026-08-20", "Subscription documentation"),
    ("dictionary", "Field dictionary for the files in this folder", "Research desk", "2026-10-09", "Internal"),
]


def write_manifest(path, counts, names):
    rows = []
    for key, what, src, date, lic in MANIFEST:
        name = names[key]
        rows.append(dict(file=name, contents=what, source=src, received_or_pulled=date, terms=lic,
                         rows=counts.get(key, "")))
    pd.DataFrame(rows).to_csv(path, index=False, lineterminator="\n")
    return len(rows)
