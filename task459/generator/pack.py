"""Writes task459's evidence pack: the files Pinyon Valley Health Plan's systems and its partners export.

Each file carries its own system's conventions (date layouts, identifiers, adjustment codes); nothing under
target/ describes the data or the task. Provenance goes to metadata.json (build.py).
"""
import csv
import datetime as dt
import io
import os
import zipfile

import numpy as np

import world as W

FICTION_STAMP = dt.datetime(2026, 10, 14, 16, 42, 0)
ORG = "Pinyon Valley Health Plan"
PLAN = "Senior Choice"


def fips(county):
    return W.COUNTY_FIPS[county]


def write_csv(path, header, rows, delimiter=",", lineterminator="\r\n"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delimiter, lineterminator=lineterminator)
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def claim_no(rng, prefix, used):
    while True:
        v = prefix + "".join(str(x) for x in rng.integers(0, 10, 10))
        if v not in used:
            used.add(v)
            return v


def money(x):
    return "%.2f" % x


# ---------------------------------------------------------------------------------------------------------
def build_medical(wd, svcs):
    """Medical claims as the claims system extracts them: one row per claim line, service dates in 2025,
    paid through 30 June 2026. Replacements (frequency 7) and voids (frequency 8) point at the claim they
    adjust; denied lines stay in the extract with nothing paid."""
    rng = W.stream("medical_claims")
    provs = wd["provs"]
    used = set()
    rows = []
    for s in svcs:
        p = provs[s.npi]
        cid = claim_no(rng, "25", used)
        lag = int(rng.choice([12, 16, 21, 28, 35, 49, 75, 120], p=[0.2, 0.22, 0.2, 0.15, 0.1, 0.07, 0.04, 0.02]))
        paid = s.date + dt.timedelta(days=lag + int(rng.integers(0, 6)))
        if paid > dt.date(2026, 6, 30):
            continue
        billing = s.npi
        lines = []
        for li, (code, units, allowed) in enumerate(s.lines, 1):
            allowed_amt = round(allowed * units * (1 + float(rng.normal(0, 0.015))), 2)
            billed = round(allowed_amt * float(rng.uniform(1.6, 2.6)), 2)
            denied = rng.random() < 0.035
            if denied:
                paid_amt, allowed_amt2 = 0.0, 0.0
            else:
                paid_amt = round(allowed_amt * (0.80 if s.pos not in ("81",) else 1.0) - (0 if rng.random() < 0.7 else 20.0), 2)
                paid_amt = max(paid_amt, 0.0)
                allowed_amt2 = allowed_amt
            mod = "95" if s.pos == "10" else ("GP" if code.startswith("97") else "")
            lines.append([cid, li, s.mid, s.date.strftime("%Y%m%d"), s.date.strftime("%Y%m%d"), s.npi, billing,
                          s.pos, code, mod, units, money(billed), money(allowed_amt2), money(paid_amt),
                          "D" if denied else "P", "1", "", paid.strftime("%Y%m%d")])
        rows.extend(lines)
        r = rng.random()
        if r < 0.024:
            # corrected claim: same service, corrected units or amounts, new claim number, paid later
            cid2 = claim_no(rng, "25", used)
            paid2 = paid + dt.timedelta(days=int(rng.integers(14, 60)))
            if paid2 <= dt.date(2026, 6, 30):
                for ln in lines:
                    n = list(ln)
                    n[0] = cid2
                    factor = float(rng.choice([0.85, 0.9, 1.1, 1.15]))
                    n[12] = money(float(ln[12]) * factor) if ln[14] == "P" else ln[12]
                    n[13] = money(float(ln[13]) * factor) if ln[14] == "P" else ln[13]
                    n[11] = money(float(ln[11]))
                    n[15] = "7"
                    n[16] = cid
                    n[17] = paid2.strftime("%Y%m%d")
                    rows.append(n)
        elif r < 0.032:
            # void: the claim was billed twice; the second submission is voided
            cid2 = claim_no(rng, "25", used)
            cid3 = claim_no(rng, "25", used)
            paid2 = paid + dt.timedelta(days=int(rng.integers(5, 25)))
            paid3 = paid2 + dt.timedelta(days=int(rng.integers(10, 45)))
            if paid3 <= dt.date(2026, 6, 30):
                for ln in lines:
                    n = list(ln)
                    n[0] = cid2
                    n[17] = paid2.strftime("%Y%m%d")
                    rows.append(n)
                for ln in lines:
                    n = list(ln)
                    n[0] = cid3
                    n[12] = money(-float(ln[12]))
                    n[13] = money(-float(ln[13]))
                    n[11] = money(-float(ln[11]))
                    n[15] = "8"
                    n[16] = cid2
                    n[17] = paid3.strftime("%Y%m%d")
                    rows.append(n)
    rows.sort(key=lambda x: (x[17], x[0], x[1]))
    header = ["CLAIM_ID", "LINE_NO", "MEMBER_ID", "SVC_FROM_DT", "SVC_TO_DT", "RENDERING_NPI", "BILLING_NPI",
              "PLACE_OF_SVC", "PROC_CD", "MODIFIER", "UNITS", "BILLED_AMT", "ALLOWED_AMT", "PAID_AMT", "LINE_STATUS",
              "CLAIM_FREQ_CD", "ORIG_CLAIM_ID", "PAID_DT"]
    return header, rows


def build_pbm(wd, fills):
    """The pharmacy benefit manager's claim file: pipe-delimited, MM/DD/YYYY dates, cardholder IDs in the PBM's
    own layout. Reversals (B2) carry the claim they reverse; most reversed fills are re-billed the same day."""
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
        base = [cno, card, "01", f.date.strftime("%m/%d/%Y"), f.ncpdp, f.ndc, f.name, f.strength, f.qty, f.days,
                money(cost), money(fee), money(plan_paid), money(copay), "B1", ""]
        rows.append(base)
        if rng.random() < 0.028:
            rv = claim_no(rng, "6", used)
            rows.append([rv, card, "01", f.date.strftime("%m/%d/%Y"), f.ncpdp, f.ndc, f.name, f.strength, f.qty, f.days,
                         money(-cost), money(-fee), money(-plan_paid), money(-copay), "B2", cno])
            # re-billed the same day with the corrected quantity
            rb = claim_no(rng, "6", used)
            rows.append([rb, card, "01", f.date.strftime("%m/%d/%Y"), f.ncpdp, f.ndc, f.name, f.strength, f.qty, f.days,
                         money(cost), money(fee), money(plan_paid), money(copay), "B1", ""])
    rows.sort(key=lambda x: (dt.datetime.strptime(x[3], "%m/%d/%Y"), x[0]))
    header = ["RX_CLAIM_NBR", "CARDHOLDER_ID", "PERSON_CD", "DATE_FILLED", "SVC_PROV_ID", "PRODUCT_ID", "DRUG_NAME",
              "STRENGTH", "QTY_DISPENSED", "DAYS_SUPPLY", "INGRED_COST", "DISP_FEE", "PLAN_PAID", "PATIENT_PAY",
              "TRANS_TYPE", "ORIG_RX_CLAIM_NBR"]
    return header, rows


def build_visits(wd, visits):
    """In-home support agencies' claims: 15-minute units, a visit longer than four hours billed on a second
    claim, corrected and voided claims pointing at the claim they adjust."""
    rng = W.stream("visit_claims")
    used = set()
    rows = []
    rate = {"T1019": 6.85, "S5130": 6.10, "S5150": 5.90}
    for v in visits:
        parts = [v.units] if v.units <= 16 else [16, v.units - 16]
        for u in parts:
            cno = claim_no(rng, "H", used)
            rows.append([cno, v.mid, v.npi, v.npi, v.date.strftime("%Y-%m-%d"), v.start, v.code, u, "1", "",
                         money(u * rate[v.code])])
            x = rng.random()
            if x < 0.03:
                c2 = claim_no(rng, "H", used)
                u2 = max(1, u + int(rng.choice([-2, -1, 1, 2])))
                rows.append([c2, v.mid, v.npi, v.npi, v.date.strftime("%Y-%m-%d"), v.start, v.code, u2, "7", cno,
                             money(u2 * rate[v.code])])
            elif x < 0.04:
                c2 = claim_no(rng, "H", used)
                c3 = claim_no(rng, "H", used)
                rows.append([c2, v.mid, v.npi, v.npi, v.date.strftime("%Y-%m-%d"), v.start, v.code, u, "1", "",
                             money(u * rate[v.code])])
                rows.append([c3, v.mid, v.npi, v.npi, v.date.strftime("%Y-%m-%d"), v.start, v.code, u, "8", c2,
                             money(-u * rate[v.code])])
    rows.sort(key=lambda x: (x[4], x[0]))
    header = ["CLAIM_NO", "MEMBER_ID", "BILLING_NPI", "RENDERING_NPI", "DATE_OF_SERVICE", "VISIT_START", "HCPCS",
              "UNITS", "FREQ_CD", "ORIG_CLAIM_NO", "PAID_AMT"]
    return header, rows


def build_members(wd):
    """The member extract as of 9 October 2026, the address history and the enrollment spans."""
    rng = W.stream("member_extract")
    provs = wd["provs"]
    mrows, arows, erows = [], [], []
    srcs = ["ENROLLMENT FORM", "MEMBER CALL", "CMS TRANSACTION", "RETURNED MAIL UPDATE", "ONLINE PORTAL"]
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
            s = "ENROLLMENT FORM" if i == 0 else srcs[1 + int(rng.integers(0, len(srcs) - 1))]
            arows.append([m.mid, when.strftime("%Y-%m-%d"), z, c.upper(), fips(k), s])
        for (s0, e0) in m.enroll:
            reason = ""
            if m.dod is not None:
                reason = "DECEASED"
            elif e0 is not None:
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


def directory_rows(wd):
    provs = wd["provs"]
    rows = []
    type_name = {"pcp": "PRIMARY CARE", "spec": "SPECIALIST", "uc": "URGENT CARE", "hosp": "HOSPITAL OUTPATIENT",
                 "pt": "PHYSICAL THERAPY", "img": "IMAGING CENTER", "home": "IN-HOME SUPPORT AGENCY", "lab": "LABORATORY"}
    for p in sorted(provs.values(), key=lambda q: q.npi):
        z = p.zip_on(W.EXTRACT_DATE)
        city, county = W.ZIP_INFO[z]
        agency = ""
        if p.kind == "home":
            agency = [a for r, a in W.AGENCIES if r == p.agency][0]
        rows.append([p.npi, p.name, type_name[p.kind], city.upper(), z, fips(county), "IN NETWORK", agency])
    return ["NPI", "PROVIDER_NAME", "PROVIDER_TYPE", "PRACTICE_CITY", "PRACTICE_ZIP", "PRACTICE_COUNTY_FIPS",
            "NETWORK_STATUS", "AGENCY_NAME"], rows


def location_changes(wd):
    rng = W.stream("location_changes")
    provs = wd["provs"]
    rows = []
    for p in provs.values():
        for when, nz in p.moves:
            oz = p.zip
            rows.append([p.npi, when.strftime("%Y-%m-%d"), oz, fips(W.ZIP_INFO[oz][1]), nz, fips(W.ZIP_INFO[nz][1]),
                         "PRACTITIONER ATTESTATION"])
    # moves inside a county or within a region, recorded the same way
    pool = [p for p in provs.values() if p.kind in ("pcp", "spec", "pt") and not p.moves]
    for i in range(14):
        p = pool[int(rng.integers(0, len(pool)))]
        same = [z for z, c, k, w in W.ZIPS if W.COUNTY_REGION[k] == p.region and z != p.zip]
        nz = same[int(rng.integers(0, len(same)))]
        when = dt.date(2025, 1, 6) + dt.timedelta(days=int(rng.integers(0, 340)))
        p.moves.append((when, nz))
        rows.append([p.npi, when.strftime("%Y-%m-%d"), p.zip, fips(W.ZIP_INFO[p.zip][1]), nz, fips(W.ZIP_INFO[nz][1]),
                     ["PRACTITIONER ATTESTATION", "CREDENTIALING UPDATE", "CAQH ROSTER"][int(rng.integers(0, 3))]])
    rows.sort(key=lambda r: (r[1], r[0]))
    return ["NPI", "EFFECTIVE_DATE", "PRIOR_ZIP", "PRIOR_COUNTY_FIPS", "NEW_ZIP", "NEW_COUNTY_FIPS", "SOURCE"], rows


def pharmacy_rows(wd):
    rows = []
    tname = {"retail": "RETAIL", "mail": "MAIL ORDER", "specialty": "SPECIALTY"}
    for ph in sorted(wd["pharm"].values(), key=lambda q: q.ncpdp):
        county = W.ZIP_INFO[ph.zip][1].upper() if ph.state == "AZ" else ""
        rows.append([ph.ncpdp, ph.name, ph.city.upper(), ph.state, ph.zip, county, tname[ph.kind]])
    return ["NCPDP_ID", "PHARMACY_NAME", "CITY", "STATE", "ZIP", "COUNTY", "PHARMACY_TYPE"], rows


def county_population_rows():
    # Arizona residents aged 75 and over by county, 1 July 2025 (state demographer's county estimates series).
    est = {"Apache": 5980, "Cochise": 15240, "Coconino": 10870, "Gila": 7960, "Graham": 2810, "Greenlee": 610,
           "La Paz": 3420, "Maricopa": 329460, "Mohave": 31720, "Navajo": 9410, "Pima": 98730, "Pinal": 37150,
           "Santa Cruz": 4180, "Yavapai": 41320, "Yuma": 16890}
    fips_all = dict(W.COUNTY_FIPS)
    fips_all.update({"Graham": "04009", "Greenlee": "04011"})
    rows = [[k, fips_all[k], v] for k, v in sorted(est.items())]
    rows.append(["Arizona", "04000", sum(est.values())])
    return ["COUNTY", "FIPS", "POP_75_PLUS_JUL2025"], rows


# ---------------------------------------------------------------------------------------------------------
# XLSX and PDF writers with the fiction's metadata (no writer signature, the export's own dates).
def save_xlsx(wb, path, title):
    wb.properties.creator = ORG
    wb.properties.lastModifiedBy = "Provider Data Management"
    wb.properties.title = title
    wb.properties.created = FICTION_STAMP - dt.timedelta(days=3)
    wb.properties.modified = FICTION_STAMP
    bio = io.BytesIO()
    wb.save(bio)
    repack_ooxml(bio.getvalue(), path, title, "Provider Data Management")


APP_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
           'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           '<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
           '<Company>%s</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
           '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')


def repack_ooxml(blob, path, title, modby):
    zin = zipfile.ZipFile(io.BytesIO(blob))
    out = io.BytesIO()
    created = (FICTION_STAMP - dt.timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    modified = FICTION_STAMP.strftime("%Y-%m-%dT%H:%M:%SZ")
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>%s</dc:title><dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
            '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
            % (title, ORG, modby, created, modified))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in zin.namelist():
            data = zin.read(name)
            if name == "docProps/core.xml":
                data = core.encode("utf-8")
            elif name == "docProps/app.xml":
                data = (APP_XML % ORG).encode("utf-8")
            zi = zipfile.ZipInfo(name, date_time=(2026, 10, 14, 16, 42, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zout.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(out.getvalue())


def finish_pdf(path, created, modified):
    """reportlab in invariant mode stamps 2000-01-01; put the document's own dates in at equal length."""
    b = open(path, "rb").read()
    import re
    def sub_date(blob, key, when):
        pat = re.compile(rb"/" + key + rb" \(D:\d{14}[^)]*\)")
        m = pat.search(blob)
        if not m:
            return blob
        old = m.group(0)
        new = b"/" + key + b" (D:" + when.strftime("%Y%m%d%H%M%S").encode() + b"-07'00')"
        if len(new) <= len(old):
            new = new + b" " * (len(old) - len(new))
        else:
            return blob
        return blob[:m.start()] + new + blob[m.end():]
    b = sub_date(b, b"CreationDate", created)
    b = sub_date(b, b"ModDate", modified)
    open(path, "wb").write(b)
