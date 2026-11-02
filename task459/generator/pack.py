"""Writes task459's evidence pack: the files Pinyon Valley Health Plan's systems and partners export.

Each file carries its own system's conventions (date layouts, identifiers, adjustment codes); nothing under
target/ describes the data or the task. Provenance goes to metadata.json (build.py).
"""
import csv
import datetime as dt
import io
import os
import re
import zipfile

import numpy as np

import world as W

ORG = "Pinyon Valley Health Plan"
PAID_THROUGH = dt.date(2026, 6, 30)

FILES = {
    "schedule": "SC_2027_IHS_Agreement_Schedule_B.pdf",
    "members": "sc_member_extract_20261009.csv",
    "addr": "sc_member_address_history_20261009.csv",
    "enroll": "sc_enrollment_spans_20261009.csv",
    "medical": "med_claims_svc2025_paid_thru_20260630.csv",
    "pbm": "pbm_claims_2025_PVHP.txt",
    "visits": "ihs_visit_claims_2025.csv",
    "directory": "provider_directory_20261001.xlsx",
    "moves": "provider_location_changes_2025.csv",
    "pharmacies": "pharmacy_network_2025.csv",
    "population": "az_pop_75plus_by_county_2025.csv",
    "adequacy": "network_adequacy_review_2025Q4.xlsx",
}
DISTRACTORS = ["population", "adequacy"]
STAMPS = {  # each file's in-fiction export time (also the file's mtime)
    "schedule": dt.datetime(2026, 9, 22, 15, 10), "members": dt.datetime(2026, 10, 9, 6, 2),
    "addr": dt.datetime(2026, 10, 9, 6, 4), "enroll": dt.datetime(2026, 10, 9, 6, 3),
    "medical": dt.datetime(2026, 7, 2, 4, 47), "pbm": dt.datetime(2026, 3, 4, 2, 15),
    "visits": dt.datetime(2026, 4, 6, 9, 31), "directory": dt.datetime(2026, 10, 1, 7, 55),
    "moves": dt.datetime(2026, 1, 12, 11, 20), "pharmacies": dt.datetime(2026, 1, 9, 8, 40),
    "population": dt.datetime(2026, 5, 18, 13, 5), "adequacy": dt.datetime(2026, 1, 27, 16, 12),
}


def fips(county):
    return W.COUNTY_FIPS[county]


def write_csv(path, header, rows, delimiter=",", lineterminator="\r\n"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delimiter, lineterminator=lineterminator)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def claim_no(rng, prefix, used, ndig=10):
    while True:
        v = prefix + "".join(str(x) for x in rng.integers(0, 10, ndig))
        if v not in used:
            used.add(v)
            return v


def money(x):
    return "%.2f" % x


FREQ_DESC = {"1": "ORIGINAL", "7": "REPLACEMENT OF PRIOR CLAIM", "8": "VOID OF PRIOR CLAIM"}


# ---------------------------------------------------------------------------------------------------------
def build_medical(wd, svcs):
    """Medical claims as the claims system extracts them: one row per claim line, service dates in 2025, paid
    through 30 June 2026. A replacement (frequency 7) carries the whole corrected claim and names the claim it
    replaces; a void (frequency 8) cancels the claim it names; denied lines stay in the extract with nothing paid."""
    rng = W.stream("medical_claims")
    used = set()
    rows = []
    for s in svcs:
        cid = claim_no(rng, "25", used)
        lag = int(rng.choice([12, 16, 21, 28, 35, 49, 75, 120], p=[0.2, 0.22, 0.2, 0.15, 0.1, 0.07, 0.04, 0.02]))
        paid = s.date + dt.timedelta(days=lag + int(rng.integers(0, 6)))
        if paid > PAID_THROUGH:
            paid = PAID_THROUGH - dt.timedelta(days=int(rng.integers(0, 20)))
        lines = []
        for li, (code, units, allowed) in enumerate(s.lines, 1):
            allowed_amt = round(allowed * units * (1 + float(rng.normal(0, 0.015))), 2)
            billed = round(allowed_amt * float(rng.uniform(1.6, 2.6)), 2)
            denied = rng.random() < 0.035
            if denied:
                paid_amt, allowed_amt2 = 0.0, 0.0
            else:
                paid_amt = round(allowed_amt * (0.80 if s.pos != "81" else 1.0) - (0 if rng.random() < 0.7 else 20.0), 2)
                paid_amt = max(paid_amt, 0.0)
                allowed_amt2 = allowed_amt
            mod = "95" if s.pos == "10" else ("GP" if code.startswith("97") else "")
            lines.append([cid, li, s.mid, s.date.strftime("%Y%m%d"), s.date.strftime("%Y%m%d"), s.npi, s.pos, code, mod,
                          units, money(billed), money(allowed_amt2), money(paid_amt), "D" if denied else "P",
                          "DENIED" if denied else "PAID", "1", FREQ_DESC["1"], "", paid.strftime("%Y%m%d")])
        rows.extend(lines)
        r = rng.random()
        if r < 0.024:
            # corrected claim: the same service with corrected units or amounts, a new claim number, paid later
            cid2 = claim_no(rng, "25", used)
            paid2 = paid + dt.timedelta(days=int(rng.integers(14, 60)))
            if paid2 <= PAID_THROUGH:
                factor = float(rng.choice([0.85, 0.9, 1.1, 1.15]))
                for ln in lines:
                    n = list(ln)
                    n[0] = cid2
                    if ln[13] == "P":
                        n[11] = money(float(ln[11]) * factor)
                        n[12] = money(float(ln[12]) * factor)
                    n[15], n[16], n[17] = "7", FREQ_DESC["7"], cid
                    n[18] = paid2.strftime("%Y%m%d")
                    rows.append(n)
        elif r < 0.032:
            # billed twice: the second submission is paid, then voided
            cid2 = claim_no(rng, "25", used)
            cid3 = claim_no(rng, "25", used)
            paid2 = paid + dt.timedelta(days=int(rng.integers(5, 25)))
            paid3 = paid2 + dt.timedelta(days=int(rng.integers(10, 45)))
            if paid3 <= PAID_THROUGH:
                for ln in lines:
                    n = list(ln)
                    n[0] = cid2
                    n[18] = paid2.strftime("%Y%m%d")
                    rows.append(n)
                for ln in lines:
                    n = list(ln)
                    n[0] = cid3
                    n[10] = money(-float(ln[10]))
                    n[11] = money(-float(ln[11]))
                    n[12] = money(-float(ln[12]))
                    n[15], n[16], n[17] = "8", FREQ_DESC["8"], cid2
                    n[18] = paid3.strftime("%Y%m%d")
                    rows.append(n)
    rows.sort(key=lambda x: (x[18], x[0], x[1]))
    header = ["CLAIM_ID", "LINE_NO", "MEMBER_ID", "SVC_FROM_DT", "SVC_TO_DT", "RENDERING_NPI", "PLACE_OF_SVC", "PROC_CD",
              "MODIFIER", "UNITS", "BILLED_AMT", "ALLOWED_AMT", "PAID_AMT", "LINE_STATUS", "LINE_STATUS_DESC",
              "CLAIM_FREQ_CD", "CLAIM_FREQ_DESC", "ORIG_CLAIM_ID", "PAID_DT"]
    return header, rows


def build_pbm(wd, fills):
    """The pharmacy benefit manager's claim file: pipe-delimited, MM/DD/YYYY dates, cardholder IDs in the PBM's
    own layout. A reversal (B2) carries the claim it reverses; some reversed fills are re-billed the same day."""
    rng = W.stream("pbm_claims")
    used = set()
    rows = []
    for f in fills:
        card = "PV" + f.mid[3:]
        cno = claim_no(rng, "6", used)
        fee = 0.0 if wd["pharm"][f.ncpdp].kind != "retail" else float(rng.choice([1.75, 2.10, 2.50]))
        cost = f.cost
        total = cost + fee
        copay = round(min(total, float(rng.choice([0.0, 5.0, 10.0, 15.0], p=[0.35, 0.3, 0.25, 0.1]))), 2)
        plan_paid = round(total - copay, 2)
        dfill = f.date.strftime("%m/%d/%Y")
        rows.append([cno, card, "01", dfill, f.ncpdp, f.ndc, f.name, f.strength, f.qty, f.days,
                     money(cost), money(fee), money(plan_paid), money(copay), "B1", "PAID", ""])
        if rng.random() < 0.028:
            rv = claim_no(rng, "6", used)
            rows.append([rv, card, "01", dfill, f.ncpdp, f.ndc, f.name, f.strength, f.qty, f.days,
                         money(-cost), money(-fee), money(-plan_paid), money(-copay), "B2", "REVERSAL", cno])
            if rng.random() < 0.6:
                rb = claim_no(rng, "6", used)
                rows.append([rb, card, "01", dfill, f.ncpdp, f.ndc, f.name, f.strength, f.qty, f.days,
                             money(cost), money(fee), money(plan_paid), money(copay), "B1", "PAID", ""])
    rows.sort(key=lambda x: (dt.datetime.strptime(x[3], "%m/%d/%Y"), x[0]))
    header = ["RX_CLAIM_NBR", "CARDHOLDER_ID", "PERSON_CD", "DATE_FILLED", "SVC_PROV_ID", "PRODUCT_ID", "DRUG_NAME",
              "STRENGTH", "QTY_DISPENSED", "DAYS_SUPPLY", "INGRED_COST", "DISP_FEE", "PLAN_PAID", "PATIENT_PAY",
              "TRANS_TYPE", "CLAIM_STATUS", "ORIG_RX_CLAIM_NBR"]
    return header, rows


RATE = {"T1019": 6.85, "S5130": 6.10, "S5150": 5.90}


def hhmm_plus(start, units):
    h, m = map(int, start.split(":"))
    t = h * 60 + m + 15 * units
    return "%02d:%02d" % (t // 60, t % 60)


def build_visits(wd, visits):
    """In-home support agencies' claims: one claim per period of attendance in 15-minute units, a claim holding at
    most 16 units, so an attendance longer than four hours is billed as consecutive claims, the second starting
    when the first ends. Replacements (7) carry corrected units for the claim they name; voids (8) cancel it."""
    rng = W.stream("visit_claims")
    used = set()
    rows = []
    for v in visits:
        parts = [(v.start, v.units)] if v.units <= 16 else [(v.start, 16), (hhmm_plus(v.start, 16), v.units - 16)]
        split = len(parts) > 1
        for st, u in parts:
            cno = claim_no(rng, "H", used, 9)
            d = v.date.strftime("%Y-%m-%d")
            rows.append([cno, v.mid, v.npi, d, st, v.code, u, "1", FREQ_DESC["1"], "", money(u * RATE[v.code])])
            x = rng.random()
            if x < 0.03 and not split:
                c2 = claim_no(rng, "H", used, 9)
                u2 = int(min(16, max(1, u + int(rng.choice([-2, -1, 1, 2])))))
                if u2 == u:
                    u2 = u - 1
                rows.append([c2, v.mid, v.npi, d, st, v.code, u2, "7", FREQ_DESC["7"], cno, money(u2 * RATE[v.code])])
            elif x < 0.04:
                c2 = claim_no(rng, "H", used, 9)
                c3 = claim_no(rng, "H", used, 9)
                rows.append([c2, v.mid, v.npi, d, st, v.code, u, "1", FREQ_DESC["1"], "", money(u * RATE[v.code])])
                rows.append([c3, v.mid, v.npi, d, st, v.code, -u, "8", FREQ_DESC["8"], c2, money(-u * RATE[v.code])])
    rows.sort(key=lambda x: (x[3], x[0]))
    header = ["CLAIM_NO", "MEMBER_ID", "AGENCY_NPI", "DATE_OF_SERVICE", "PERIOD_START", "HCPCS", "UNITS", "FREQ_CD",
              "FREQ_DESC", "ORIG_CLAIM_NO", "PAID_AMT"]
    return header, rows


def build_members(wd):
    """The member extract as of 9 October 2026, the address history and the enrollment spans."""
    rng = W.stream("member_extract")
    mrows, arows, erows = [], [], []
    srcs = ["MEMBER CALL", "CMS TRANSACTION", "RETURNED MAIL UPDATE", "ONLINE PORTAL"]
    for m in wd["members"]:
        hist = sorted(m.addr_hist)
        cur_when, cur_zip, _ = hist[-1]
        city, county = W.ZIP_INFO[cur_zip]
        status = "ACTIVE"
        if m.dod is not None:
            status = "DECEASED"
        elif m.enroll[-1][1] is not None:
            status = "TERMINATED"
        pcp_when, pcp_npi = sorted(m.pcp_hist)[-1]
        mrows.append([m.mid, m.dob.strftime("%Y-%m-%d"), m.sex, cur_zip, city.upper(), fips(county),
                      cur_when.strftime("%Y-%m-%d"), pcp_npi, pcp_when.strftime("%Y-%m-%d"), "H0417-012", status])
        for i, (when, z, src) in enumerate(hist):
            c, k = W.ZIP_INFO[z]
            s = "ENROLLMENT FORM" if i == 0 else srcs[int(rng.integers(0, len(srcs)))]
            arows.append([m.mid, when.strftime("%Y-%m-%d"), z, c.upper(), fips(k), s])
        for j, (s0, e0) in enumerate(m.enroll):
            reason = ""
            if e0 is not None:
                if m.dod is not None and e0 == m.dod:
                    reason = "DECEASED"
                elif j < len(m.enroll) - 1:
                    reason = "NONPAYMENT OF PREMIUM"
                else:
                    reason = ["VOLUNTARY DISENROLLMENT", "ENROLLED IN OTHER PLAN", "MOVED OUT OF SERVICE AREA"][int(rng.integers(0, 3))]
            erows.append([m.mid, s0.strftime("%Y-%m-%d"), e0.strftime("%Y-%m-%d") if e0 else "", "SC-HMO-POS", reason])
    mrows.sort(key=lambda r: r[0])
    arows.sort(key=lambda r: (r[0], r[1]))
    erows.sort(key=lambda r: (r[0], r[1]))
    mh = ["MEMBER_ID", "DATE_OF_BIRTH", "SEX", "ADDR_OF_RECORD_ZIP", "ADDR_OF_RECORD_CITY", "ADDR_OF_RECORD_COUNTY_FIPS",
          "ADDR_EFF_DATE", "PCP_NPI", "PCP_EFF_DATE", "CONTRACT_PBP", "MEMBER_STATUS"]
    ah = ["MEMBER_ID", "EFFECTIVE_DATE", "ZIP", "CITY", "COUNTY_FIPS", "SOURCE"]
    eh = ["MEMBER_ID", "SPAN_START", "SPAN_END", "PRODUCT", "TERM_REASON"]
    return (mh, mrows), (ah, arows), (eh, erows)


TYPE_NAME = {"pcp": "PRIMARY CARE", "spec": "SPECIALIST", "uc": "URGENT CARE", "hosp": "HOSPITAL OUTPATIENT",
             "pt": "PHYSICAL THERAPY", "img": "IMAGING CENTER", "home": "IN-HOME SUPPORT AGENCY",
             "lab": "INDEPENDENT LABORATORY"}


def location_changes(wd):
    """The provider data team's change log for 2025: practice moves, each with the date it took effect. Moves
    within a region are logged the same way as the five that crossed a region line."""
    rng = W.stream("location_changes")
    provs = wd["provs"]
    rows = []
    for p in sorted(provs.values(), key=lambda q: q.npi):
        for when, nz in p.moves:
            rows.append([p.npi, when.strftime("%Y-%m-%d"), p.zip, fips(W.ZIP_INFO[p.zip][1]), nz, fips(W.ZIP_INFO[nz][1]),
                         "PRACTITIONER ATTESTATION"])
    pool = sorted([p for p in provs.values() if p.kind in ("pcp", "spec", "pt") and not p.moves], key=lambda q: q.npi)
    for i in range(14):
        p = pool[int(rng.integers(0, len(pool)))]
        if p.moves:
            continue
        same = [z for z, c, k, w in W.ZIPS if W.COUNTY_REGION[k] == p.region and z != p.zip]
        nz = same[int(rng.integers(0, len(same)))]
        when = dt.date(2025, 1, 6) + dt.timedelta(days=int(rng.integers(0, 340)))
        p.moves.append((when, nz))
        rows.append([p.npi, when.strftime("%Y-%m-%d"), p.zip, fips(W.ZIP_INFO[p.zip][1]), nz, fips(W.ZIP_INFO[nz][1]),
                     ["PRACTITIONER ATTESTATION", "CREDENTIALING UPDATE", "CAQH ROSTER"][int(rng.integers(0, 3))]])
    rows.sort(key=lambda r: (r[1], r[0]))
    return ["NPI", "EFFECTIVE_DATE", "PRIOR_ZIP", "PRIOR_COUNTY_FIPS", "NEW_ZIP", "NEW_COUNTY_FIPS", "SOURCE"], rows


def directory_rows(wd):
    provs = wd["provs"]
    rows = []
    agency_name = dict(W.AGENCIES)
    for p in sorted(provs.values(), key=lambda q: q.npi):
        z = p.zip_on(W.EXTRACT_DATE)
        city, county = W.ZIP_INFO[z]
        rows.append([p.npi, p.name, TYPE_NAME[p.kind], city.upper(), z, fips(county), "IN NETWORK",
                     agency_name[p.agency] if p.kind == "home" else ""])
    return ["NPI", "PROVIDER_NAME", "PROVIDER_TYPE", "PRACTICE_CITY", "PRACTICE_ZIP", "PRACTICE_COUNTY_FIPS",
            "NETWORK_STATUS", "AGENCY_NAME"], rows


def pharmacy_rows(wd):
    rows = []
    tname = {"retail": "RETAIL", "mail": "MAIL ORDER", "specialty": "SPECIALTY"}
    for ph in sorted(wd["pharm"].values(), key=lambda q: q.ncpdp):
        cf = fips(W.ZIP_INFO[ph.zip][1]) if ph.state == "AZ" else ""
        rows.append([ph.ncpdp, ph.name, ph.city.upper(), ph.state, ph.zip, cf, tname[ph.kind]])
    return ["NCPDP_ID", "PHARMACY_NAME", "CITY", "STATE", "ZIP", "COUNTY_FIPS", "PHARMACY_TYPE"], rows


def county_population_rows():
    # Arizona residents aged 75 and over by county, 1 July 2025 (county population estimates by age).
    est = {"Apache": 5980, "Cochise": 15240, "Coconino": 10870, "Gila": 7960, "Graham": 2810, "Greenlee": 610,
           "La Paz": 3420, "Maricopa": 329460, "Mohave": 31720, "Navajo": 9410, "Pima": 98730, "Pinal": 37150,
           "Santa Cruz": 4180, "Yavapai": 41320, "Yuma": 16890}
    fa = dict(W.COUNTY_FIPS)
    fa.update({"Graham": "04009", "Greenlee": "04011"})
    rows = [[k + " County", fa[k], "%d" % v] for k, v in sorted(est.items())]
    rows.append(["Arizona", "04000", "%d" % sum(est.values())])
    return ["GEOGRAPHY", "FIPS", "POP_75_PLUS_JUL2025"], rows


# ---------------------------------------------------------------------------------------------------------
# OOXML with the organisation's own document properties.
APP_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           '<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
           '<Company>%s</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
           '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')


def save_xlsx(wb, path, title, author, stamp):
    bio = io.BytesIO()
    wb.save(bio)
    zin = zipfile.ZipFile(io.BytesIO(bio.getvalue()))
    created = (stamp - dt.timedelta(days=2, hours=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    modified = stamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>%s</dc:title><dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
            '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
            % (title, author, author, created, modified))
    out = io.BytesIO()
    zt = (stamp.year, stamp.month, stamp.day, stamp.hour, stamp.minute, 0)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in zin.namelist():
            data = zin.read(name)
            if name == "docProps/core.xml":
                data = core.encode("utf-8")
            elif name == "docProps/app.xml":
                data = (APP_XML % ORG).encode("utf-8")
            zi = zipfile.ZipInfo(name, date_time=zt)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zout.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(out.getvalue())


def write_directory(wd, path):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Directory"
    h, rows = directory_rows(wd)
    ws.append(h)
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append(r)
    for col, wdt in zip("ABCDEFGH", (13, 46, 24, 18, 12, 22, 15, 44)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A2"
    save_xlsx(wb, path, "Senior Choice provider directory extract", "Provider Data Management", STAMPS["directory"])
    return len(rows)


def write_adequacy(path):
    """The plan's quarterly network adequacy review against the time and distance standards (county type)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    rng = W.stream("adequacy")
    wb = Workbook()
    ws = wb.active
    ws.title = "Standards"
    ws.append(["Specialty", "County type", "Max time (minutes)", "Max distance (miles)"])
    std = {"Primary Care": [(10, 5), (15, 10), (30, 20), (40, 30), (70, 60)],
           "Cardiology": [(20, 10), (30, 20), (50, 35), (75, 60), (95, 85)],
           "Outpatient Infusion": [(20, 10), (45, 30), (80, 60), (75, 60), (110, 100)],
           "Physical Therapy": [(20, 10), (30, 20), (50, 35), (75, 60), (95, 85)],
           "Pharmacy (retail)": [(None, 2), (None, 5), (None, 15), (None, 15), (None, 15)]}
    ctypes = ["Large Metro", "Metro", "Micro", "Rural", "CEAC"]
    for sp, vals in std.items():
        for ct, (t, d) in zip(ctypes, vals):
            ws.append([sp, ct, t if t is not None else "n/a", d])
    for c in ws[1]:
        c.font = Font(bold=True)
    for col, wdt in zip("ABCD", (22, 14, 20, 22)):
        ws.column_dimensions[col].width = wdt
    ws2 = wb.create_sheet("Results Q4 2025")
    ws2.append(["County", "County type", "Specialty", "Contracted providers", "Members within standard (%)", "Meets 90% standard"])
    ctype_of = {"Maricopa": "Large Metro", "Pima": "Metro", "Pinal": "Metro", "Yavapai": "Micro", "Coconino": "Micro",
                "Mohave": "Micro", "Yuma": "Metro", "Gila": "Rural", "Navajo": "Rural", "Cochise": "Micro",
                "Santa Cruz": "Rural", "Apache": "CEAC", "La Paz": "CEAC"}
    for county in sorted(W.COUNTY_FIPS):
        for sp in ("Primary Care", "Cardiology", "Outpatient Infusion", "Physical Therapy", "Pharmacy (retail)"):
            n = int(rng.integers(12, 160)) if county == "Maricopa" else int(rng.integers(1, 24))
            pct = round(float(min(100.0, rng.normal(97.0 if ctype_of[county] in ("Large Metro", "Metro") else 93.0, 3.0))), 1)
            ws2.append([county, ctype_of[county], sp, n, pct, "Yes" if pct >= 90.0 else "No"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for col, wdt in zip("ABCDEF", (14, 14, 22, 20, 28, 20)):
        ws2.column_dimensions[col].width = wdt
    save_xlsx(wb, path, "Network adequacy review Q4 2025", "Network Management", STAMPS["adequacy"])


# ---------------------------------------------------------------------------------------------------------
# The governing document.
def finish_pdf(path, created, modified):
    """Put the document's own dates into reportlab's invariant stamps at equal length, and replace the library's
    header comment with the organisation's at equal length, so no offset moves."""
    b = open(path, "rb").read()

    def sub_date(blob, key, when):
        pat = re.compile(rb"/" + key + rb" \(D:\d{14}[^)]*\)")
        m = pat.search(blob)
        if not m:
            return blob
        old = m.group(0)
        new = b"/" + key + b" (D:" + when.strftime("%Y%m%d%H%M%S").encode() + b"-07'00')"
        assert len(new) <= len(old), (old, new)
        new = new + b" " * (len(old) - len(new))
        return blob[:m.start()] + new + blob[m.end():]
    b = sub_date(b, b"CreationDate", created)
    b = sub_date(b, b"ModDate", modified)
    for m in list(re.finditer(rb"%[^\n%]*[Rr]eport[Ll]ab[^\n]*", b)):
        old = m.group(0)
        new = (b"% " + ORG.encode() + b" document services")[:len(old)]
        new = new + b" " * (len(old) - len(new))
        b = b[:m.start()] + new + b[m.end():]
    assert b"reportlab" not in b.lower()
    open(path, "wb").write(b)


def write_schedule_b(path):
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    base = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=14, alignment=TA_LEFT, spaceAfter=6)
    head = ParagraphStyle("h", parent=base, fontName="Times-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
    title = ParagraphStyle("t", parent=base, fontName="Times-Bold", fontSize=13.5, leading=17, spaceAfter=2)
    small = ParagraphStyle("s", parent=base, fontSize=9, leading=11.5)
    story = [
        Paragraph("PINYON VALLEY HEALTH PLAN", small),
        Paragraph("Senior Choice (HMO-POS) 2027 In-Home Support Agreement", title),
        Paragraph("Schedule B. Regional allocation of the 2027 in-home support budget", title),
        Spacer(1, 6),
        Paragraph("Approved by the Board of Directors on 22 September 2026. This Schedule forms part of each Agency's "
                  "2027 In-Home Support Agreement with Pinyon Valley Health Plan (the Plan) and governs the amount the "
                  "Plan pays each Agency for 2027.", base),
        Paragraph("B.1 Regions and Agencies", head),
        Paragraph("The Plan's Senior Choice service area is divided into Regions, each served by one Agency:", base),
    ]
    tab = [["Region", "Counties (county code)", "Agency"]]
    for code, name, counties in W.REGIONS:
        tab.append([name, Paragraph(", ".join("%s (%s)" % (c, W.COUNTY_FIPS[c]) for c in counties), small),
                    Paragraph(dict(W.AGENCIES)[code], small)])
    t = Table(tab, colWidths=[1.3 * inch, 2.6 * inch, 2.6 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Times-Bold", 9.5), ("FONT", (0, 1), (0, -1), "Times-Roman", 9.5),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.grey), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story += [t, Spacer(1, 4)]
    story += [
        Paragraph("B.2 The 2027 Budget", head),
        Paragraph("The Plan's 2027 budget for in-home support to Covered Members is USD 14,630,000 (the 2027 Budget).", base),
        Paragraph("B.3 Covered Members", head),
        Paragraph("A Covered Member is a Senior Choice member who was enrolled in Senior Choice on every day of the 2025 "
                  "calendar year and was aged 75 or over on 31 December 2025.", base),
        Paragraph("B.4 Region of a Covered Member", head),
        Paragraph("Agencies serve members where they live, and the 2027 Budget follows where Covered Members lived in "
                  "2025. Each Covered Member is counted once, in the Region where the member lived for the greater part "
                  "of 2025: the Region in which the member was physically present on more days of 2025 than in any other "
                  "Region. The Plan determines each Covered Member's Region from its own records of the member's 2025 "
                  "enrollment and services.", base),
        Paragraph("B.5 Allocation", head),
        Paragraph("Each Agency's 2027 Allocation is the 2027 Budget multiplied by the number of Covered Members counted "
                  "in its Region and divided by the number of all Covered Members, rounded to the nearest dollar.", base),
        Paragraph("B.6 Payment", head),
        Paragraph("The Plan pays each Allocation in twelve equal monthly installments in arrears, the first in February "
                  "2027. The Allocation is fixed for 2027 and is not adjusted for Covered Members who move, disenroll or "
                  "die during 2027.", base),
        Paragraph("B.7 Visits", head),
        Paragraph("A Visit is one continuous attendance by Agency staff at a member's home. Its length runs from the "
                  "staff member's arrival to departure. Agencies bill the Plan for Visits in units of 15 minutes and "
                  "report them by calendar quarter of the date of service.", base),
        Paragraph("B.8 Review", head),
        Paragraph("The Plan's Director of Provider Contracting and Payment presents the Allocations to the Board before "
                  "the 2027 agreements are signed. An Agency may ask the Plan to review its Allocation within 30 days of "
                  "receiving it.", base),
        Spacer(1, 14),
        Paragraph("Lisa Howell, Chair of the Board &nbsp;&nbsp;&nbsp;&nbsp; Willie Flores, Corporate Secretary", small),
    ]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Roman", 8)
        canvas.drawString(inch, 0.6 * inch, "Senior Choice 2027 In-Home Support Agreement, Schedule B")
        canvas.drawRightString(7.5 * inch, 0.6 * inch, "Page %d" % doc.page)
        canvas.restoreState()

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=0.9 * inch,
                            bottomMargin=0.9 * inch, title="2027 In-Home Support Agreement, Schedule B",
                            author="Pinyon Valley Health Plan, Office of the Corporate Secretary",
                            subject="Regional allocation of the 2027 in-home support budget",
                            creator=ORG, producer=ORG + " document services", invariant=1)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    finish_pdf(path, dt.datetime(2026, 9, 22, 15, 4), STAMPS["schedule"])


# ---------------------------------------------------------------------------------------------------------
def write_pack(out, wd, svcs, fills, visits):
    """Write every file of the pack into `out` (which must exist and be empty). Returns row counts."""
    counts = {}
    write_schedule_b(os.path.join(out, FILES["schedule"]))
    (mh, mr), (ah, ar), (eh, er) = build_members(wd)
    write_csv(os.path.join(out, FILES["members"]), mh, mr)
    write_csv(os.path.join(out, FILES["addr"]), ah, ar)
    write_csv(os.path.join(out, FILES["enroll"]), eh, er)
    counts.update(members=len(mr), addr=len(ar), enroll=len(er))
    h, rows = build_medical(wd, svcs)
    write_csv(os.path.join(out, FILES["medical"]), h, rows)
    counts["medical"] = len(rows)
    h, rows = build_pbm(wd, fills)
    write_csv(os.path.join(out, FILES["pbm"]), h, rows, delimiter="|", lineterminator="\n")
    counts["pbm"] = len(rows)
    h, rows = build_visits(wd, visits)
    write_csv(os.path.join(out, FILES["visits"]), h, rows)
    counts["visits"] = len(rows)
    mvh, mvr = MOVES_LOG
    write_csv(os.path.join(out, FILES["moves"]), mvh, mvr)
    counts["moves"] = len(mvr)
    counts["directory"] = write_directory(wd, os.path.join(out, FILES["directory"]))
    h, rows = pharmacy_rows(wd)
    write_csv(os.path.join(out, FILES["pharmacies"]), h, rows)
    counts["pharmacies"] = len(rows)
    h, rows = county_population_rows()
    write_csv(os.path.join(out, FILES["population"]), h, rows)
    counts["population"] = len(rows)
    write_adequacy(os.path.join(out, FILES["adequacy"]))
    for k, name in FILES.items():
        ts = STAMPS[k].replace(tzinfo=dt.timezone(dt.timedelta(hours=-7))).timestamp()
        os.utime(os.path.join(out, name), (ts, ts))
    return counts


MOVES_LOG = None


def prepare(wd):
    """Within-region practice moves join the providers before services are simulated, so each claim's provider
    location on its date is the logged one. Call once, after build_world and before simulate."""
    global MOVES_LOG
    MOVES_LOG = location_changes(wd)
