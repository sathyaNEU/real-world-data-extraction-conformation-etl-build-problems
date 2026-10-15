"""Writers for the bundle's data files, each in the layout and idiom of the system that exports it."""
import csv
import datetime as dt

import numpy as np

import claims as CL
import providers as PV
import world as W

D = dt.date
FILES = {
    "claims": "bh_claims_encounters_dos_2025-07-01_2026-06-30.csv",
    "spans": "enrollment_spans_2025-07-01_2026-06-30.csv",
    "nppes": "npidata_pfile_wa_20050523-20261011.csv",
    "week1": "npidata_pfile_wa_20261012-20261018.csv",
    "week2": "npidata_pfile_wa_20261019-20261025.csv",
    "week3": "npidata_pfile_wa_20261026-20261101.csv",
    "week4": "npidata_pfile_wa_20261102-20261108.csv",
    "deact": "NPPES_Deactivated_NPI_Report_20261110.xlsx",
    "zipcty": "ZIP_COUNTY_062026.xlsx",
    "nucc": "nucc_taxonomy_261.csv",
    "fees": "bh_professional_fee_schedule_fy2026.csv",
    "policy": "np31_prescriber_service_area_designation.pdf",
    "dict": "network_analytics_data_dictionary.xlsx",
    "adequacy": "network_adequacy_time_distance_2026q2.xlsx",
    "ofm": "ofm_april1_population_2026.csv",
    "manifest": "extract_manifest_2026-11-12.csv",
}
WEEK_KEYS = ["week1", "week2", "week3", "week4"]

NPPES_COLUMNS = [
    "NPI", "Entity Type Code", "Replacement NPI", "Employer Identification Number (EIN)",
    "Provider Organization Name (Legal Business Name)", "Provider Last Name (Legal Name)", "Provider First Name",
    "Provider Middle Name", "Provider Name Prefix Text", "Provider Name Suffix Text", "Provider Credential Text",
    "Provider Other Organization Name", "Provider Other Organization Name Type Code", "Provider Other Last Name",
    "Provider Other First Name", "Provider Other Middle Name", "Provider Other Name Prefix Text",
    "Provider Other Name Suffix Text", "Provider Other Credential Text", "Provider Other Last Name Type Code",
    "Provider First Line Business Mailing Address", "Provider Second Line Business Mailing Address",
    "Provider Business Mailing Address City Name", "Provider Business Mailing Address State Name",
    "Provider Business Mailing Address Postal Code", "Provider Business Mailing Address Country Code (If outside U.S.)",
    "Provider Business Mailing Address Telephone Number", "Provider Business Mailing Address Fax Number",
    "Provider First Line Business Practice Location Address", "Provider Second Line Business Practice Location Address",
    "Provider Business Practice Location Address City Name", "Provider Business Practice Location Address State Name",
    "Provider Business Practice Location Address Postal Code",
    "Provider Business Practice Location Address Country Code (If outside U.S.)",
    "Provider Business Practice Location Address Telephone Number", "Provider Business Practice Location Address Fax Number",
    "Provider Enumeration Date", "Last Update Date", "NPI Deactivation Reason Code", "NPI Deactivation Date",
    "NPI Reactivation Date", "Provider Sex Code", "Authorized Official Last Name", "Authorized Official First Name",
    "Authorized Official Middle Name", "Authorized Official Title or Position", "Authorized Official Telephone Number",
]
for _k in range(1, 5):
    NPPES_COLUMNS += ["Healthcare Provider Taxonomy Code_%d" % _k, "Provider License Number_%d" % _k,
                      "Provider License Number State Code_%d" % _k, "Healthcare Provider Primary Taxonomy Switch_%d" % _k]
NPPES_COLUMNS += ["Is Sole Proprietor", "Is Organization Subpart", "Parent Organization LBN", "Parent Organization TIN",
                  "Certification Date"]

CLAIM_COLUMNS = ["clm_icn", "clm_line_num", "clm_freq_cd", "orig_icn", "mbr_id", "fin_arrangement_cd", "billing_npi",
                 "rendering_npi", "pos_cd", "proc_cd", "proc_mod1", "svc_units", "svc_from_dt", "svc_thru_dt", "dx_cd_1",
                 "dx_cd_2", "dx_cd_3", "dx_cd_4", "billed_amt", "paid_amt", "clm_rcvd_dt", "clm_paid_dt"]
SPAN_COLUMNS = ["span_id", "mbr_id", "client_id", "birth_dt", "sex_cd", "elig_group_cd", "span_start_dt", "span_end_dt",
                "res_county_fips", "res_zip", "span_reason_cd"]
GROUP_CODE = {"DSB": "SSI-DIS", "EXP": "ADULT-EXP", "PCR": "PARENT-CR", "AGD": "AGED-65"}


def _w(path, header, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        for row in rows:
            w.writerow(row)
    return len(rows)


def _mdy(d):
    return d.strftime("%m/%d/%Y") if d else ""


def _phone(r):
    return "509%07d" % int(r.integers(2000000, 9999999))


# ------------------------------------------------------------------ NPPES

def _license(r, tax):
    pre = {"2084P0800X": "MD", "2084P0804X": "MD", "2084P0802X": "MD", "2084P0805X": "MD", "2084A0401X": "OP",
           "207QA0401X": "MD", "207RA0401X": "MD", "363LP0808X": "AP", "364SP0808X": "AP", "363LF0000X": "AP",
           "363LA2200X": "AP", "207Q00000X": "MD", "207R00000X": "MD", "363A00000X": "PA", "103T00000X": "PY",
           "101YM0800X": "LH", "1041C0700X": "LW", "101YA0400X": "CO", "207P00000X": "MD", "208D00000X": "OP"}.get(tax, "")
    return (pre + "%08d" % int(r.integers(60000000, 61400000))) if pre else ""


def _zip9(r, z):
    return z + ("%04d" % int(r.integers(1000, 9999)) if r.random() < 0.7 else "")


def nppes_row(r, rec, state):
    """One NPPES record as a file shows it. state: 'active' or 'blank' (a deactivated NPI: only the NPI and the
    deactivation date)."""
    row = {k: "" for k in NPPES_COLUMNS}
    row["NPI"] = rec["npi"]
    if state == "blank":
        row["NPI Deactivation Date"] = _mdy(rec["deactivated"])
        return [row[k] for k in NPPES_COLUMNS]
    org = rec.get("entity") == 2
    row["Entity Type Code"] = "2" if org else "1"
    if org:
        row["Provider Organization Name (Legal Business Name)"] = rec["name"]
        row["Employer Identification Number (EIN)"] = "<UNAVAIL>"
        row["Authorized Official Last Name"] = rec.get("ao_last", "")
        row["Authorized Official First Name"] = rec.get("ao_first", "")
        row["Authorized Official Title or Position"] = rec.get("ao_title", "")
        row["Authorized Official Telephone Number"] = rec.get("phone", "")
        row["Is Organization Subpart"] = rec.get("subpart", "N")
        row["Parent Organization LBN"] = rec.get("parent", "")
    else:
        row["Provider Last Name (Legal Name)"] = rec["last"].upper()
        row["Provider First Name"] = rec["first"].upper()
        row["Provider Middle Name"] = rec.get("middle", "")
        row["Provider Credential Text"] = rec.get("cred", "")
        row["Provider Sex Code"] = rec.get("sex", "")
        row["Is Sole Proprietor"] = rec.get("sole", "N")
    mail, prac = rec["mailing"], rec["practice"]
    row["Provider First Line Business Mailing Address"] = mail["line1"].upper()
    row["Provider Second Line Business Mailing Address"] = mail.get("line2", "").upper()
    row["Provider Business Mailing Address City Name"] = mail["city"].upper()
    row["Provider Business Mailing Address State Name"] = mail["state"]
    row["Provider Business Mailing Address Postal Code"] = mail.get("zip9") or mail["zip"]
    row["Provider Business Mailing Address Country Code (If outside U.S.)"] = "US"
    row["Provider Business Mailing Address Telephone Number"] = rec.get("phone", "")
    row["Provider First Line Business Practice Location Address"] = prac["line1"].upper()
    row["Provider Second Line Business Practice Location Address"] = prac.get("line2", "").upper()
    row["Provider Business Practice Location Address City Name"] = prac["city"].upper()
    row["Provider Business Practice Location Address State Name"] = prac["state"]
    row["Provider Business Practice Location Address Postal Code"] = prac.get("zip9") or prac["zip"]
    row["Provider Business Practice Location Address Country Code (If outside U.S.)"] = "US"
    row["Provider Business Practice Location Address Telephone Number"] = rec.get("phone", "")
    row["Provider Enumeration Date"] = _mdy(rec["enumerated"])
    row["Last Update Date"] = _mdy(rec["last_update"])
    row["NPI Reactivation Date"] = _mdy(rec.get("reactivated_shown"))
    row["Certification Date"] = _mdy(rec.get("certified"))
    for k, (tax, lic, prim) in enumerate(rec["taxonomies"][:4], start=1):
        row["Healthcare Provider Taxonomy Code_%d" % k] = tax
        row["Provider License Number_%d" % k] = lic
        row["Provider License Number State Code_%d" % k] = "WA" if lic else ""
        row["Healthcare Provider Primary Taxonomy Switch_%d" % k] = prim
    return [row[k] for k in NPPES_COLUMNS]


BACKGROUND_TAX = [("1223G0001X", 9, "DDS"), ("183500000X", 8, "PHARMD"), ("163W00000X", 10, "RN"),
                  ("225100000X", 6, "DPT"), ("111N00000X", 3, "DC"), ("152W00000X", 3, "OD"), ("207Q00000X", 6, "MD"),
                  ("207R00000X", 5, "MD"), ("208600000X", 2, "MD"), ("207V00000X", 2, "MD"), ("208000000X", 3, "MD"),
                  ("363LF0000X", 4, "ARNP"), ("363A00000X", 3, "PA-C"), ("235Z00000X", 2, "CCC-SLP"),
                  ("1041C0700X", 4, "LICSW"), ("101YM0800X", 5, "LMHC"), ("103T00000X", 2, "PHD"),
                  ("2084P0800X", 2, "MD"), ("363LP0808X", 2, "ARNP")]
BACKGROUND_ORG = [("333600000X", "PHARMACY"), ("251E00000X", "HOME HEALTH"), ("261QR1300X", "RURAL HEALTH CLINIC"),
                  ("311500000X", "ALZHEIMER CENTER"), ("332B00000X", "MEDICAL SUPPLY")]


def nppes_records(clins, orgs):
    """Every NPPES record the files carry: the world's clinicians and organisations, and the other Washington providers
    around them (dentists, pharmacists, nurses, therapists, other physicians, pharmacies), including behavioral-health
    prescribers practising in Spokane, Seattle and elsewhere outside the plan's counties. Returns {npi: record}."""
    r = np.random.default_rng([W.SEED, 30])
    recs = {}
    ff, fm, ll = W.first_last_pools()
    used = {(c["first"], c["last"]) for c in clins}
    for c in clins:
        rec = dict(c)
        rec["entity"] = 1
        rec["phone"] = _phone(r)
        rec["sole"] = "Y" if r.random() < 0.18 else "N"
        rec["middle"] = (ll[int(r.integers(len(ll)))][0] if r.random() < 0.4 else "")
        if rec["practice"] is not None:
            rec["practice"] = dict(rec["practice"], zip9=_zip9(r, rec["practice"]["zip"]))
        rec["mailing"] = dict(rec["mailing"] or rec["practice"])
        if "zip9" not in rec["mailing"]:
            rec["mailing"]["zip9"] = _zip9(r, rec["mailing"]["zip"])
        taxes = [(c["tax"], _license(r, c["tax"]), "Y")]
        if c.get("secondary"):
            taxes.append((c["secondary"], _license(r, c["secondary"]), "N"))
        if c["kind"] in ("prescriber", "dark", "mover", "react", "tele") and c["tax"] == "2084P0800X" and r.random() < 0.15:
            taxes.append(("2084P0804X", taxes[0][1], "N"))
        rec["taxonomies"] = taxes
        recs[c["npi"]] = rec
    for o in orgs:
        rec = dict(o)
        rec["entity"] = 2
        rec["phone"] = _phone(r) if o["kind"] != "tele" else "206%07d" % int(r.integers(2000000, 9999999))
        first, last = ff[int(r.integers(len(ff)))], ll[int(r.integers(len(ll)))]
        rec.update(ao_first=first.upper(), ao_last=last.upper(),
                   ao_title=["CHIEF EXECUTIVE OFFICER", "EXECUTIVE DIRECTOR", "CLINICAL DIRECTOR", "PRACTICE MANAGER",
                             "CHIEF FINANCIAL OFFICER"][int(r.integers(5))])
        rec["practice"] = dict(rec["practice"], zip9=_zip9(r, rec["practice"]["zip"]))
        rec["mailing"] = dict(rec["practice"])
        rec["taxonomies"] = [(o["tax"], "", "Y")]
        recs[o["npi"]] = rec
    # the other Washington providers
    places = [(c, z) for c, zs in sorted(W.ZIPS.items()) for z in zs if W.county_of_zip(z) == c]
    elsewhere = [("Spokane", "99201"), ("Spokane", "99204"), ("Spokane", "99208"), ("Spokane Valley", "99216"),
                 ("Seattle", "98104"), ("Seattle", "98122"), ("Tacoma", "98405"), ("Everett", "98201"),
                 ("Olympia", "98501"), ("Vancouver", "98664"), ("Bellevue", "98004"), ("Pullman", "99163"),
                 ("Clarkston", "99403"), ("Moscow", "83843")]
    taken = set(recs)
    for k in range(2400):
        while True:
            npi = W.npi(r)
            if npi not in taken:
                taken.add(npi)
                break
        if k < 2000:
            c, z = places[int(r.integers(len(places)))] if r.random() < 0.72 else (None, None)
            if c is None:
                city, z = elsewhere[int(r.integers(len(elsewhere)))]
                state = "ID" if z.startswith("83") else "WA"
            else:
                city, state = W.CITY[z], "WA"
            tax, _, cred = BACKGROUND_TAX[int(r.choice(len(BACKGROUND_TAX), p=np.array([w for _, w, _ in BACKGROUND_TAX]) / sum(w for _, w, _ in BACKGROUND_TAX)))]
            if tax in W.BH_TAXONOMY and c is not None:
                c, city, z, state = None, "Spokane", "99204", "WA"
            while True:
                fem = r.random() < 0.55
                first = (ff if fem else fm)[int(r.integers(len(ff if fem else fm)))]
                last = ll[int(r.integers(len(ll)))]
                if (first, last) not in used:
                    used.add((first, last))
                    break
            addr = {"line1": "%d %s" % (int(r.integers(100, 9800)), W.STREETS[int(r.integers(len(W.STREETS)))]),
                    "line2": W.SUITES[int(r.integers(len(W.SUITES)))], "city": city, "state": state, "zip": z}
            addr["zip9"] = _zip9(r, z)
            en = D(int(r.integers(2005, 2026)), int(r.integers(1, 13)), int(r.integers(1, 29)))
            recs[npi] = {"npi": npi, "entity": 1, "first": first, "last": last, "sex": "F" if fem else "M",
                         "cred": cred, "practice": addr, "mailing": dict(addr), "phone": _phone(r),
                         "enumerated": en, "last_update": max(en, D(int(r.integers(2012, 2027)), int(r.integers(1, 10)), int(r.integers(1, 29)))),
                         "taxonomies": [(tax, _license(r, tax), "Y")], "kind": "background",
                         "sole": "Y" if r.random() < 0.2 else "N", "middle": ""}
        else:
            c, z = places[int(r.integers(len(places)))]
            tax, word = BACKGROUND_ORG[int(r.integers(len(BACKGROUND_ORG)))]
            nm = "%s %s" % (W.CITY[z].upper(), word) if r.random() < 0.6 else "%s %s %s" % (
                ll[int(r.integers(len(ll)))].upper(), ["FAMILY", "VALLEY", "COMMUNITY", "NORTHWEST"][int(r.integers(4))], word)
            addr = {"line1": "%d %s" % (int(r.integers(100, 9800)), W.STREETS[int(r.integers(len(W.STREETS)))]),
                    "line2": "", "city": W.CITY[z], "state": "WA", "zip": z}
            addr["zip9"] = _zip9(r, z)
            en = D(int(r.integers(2005, 2026)), int(r.integers(1, 13)), int(r.integers(1, 29)))
            recs[npi] = {"npi": npi, "entity": 2, "name": nm, "practice": addr, "mailing": dict(addr), "phone": _phone(r),
                         "enumerated": en, "last_update": max(en, D(int(r.integers(2014, 2027)), int(r.integers(1, 10)), int(r.integers(1, 29)))),
                         "taxonomies": [(tax, "", "Y")], "kind": "background_org",
                         "ao_first": ff[int(r.integers(len(ff)))].upper(), "ao_last": ll[int(r.integers(len(ll)))].upper(),
                         "ao_title": "ADMINISTRATOR"}
    return recs


def monthly_and_weeks(recs):
    """The October monthly file (through 11 October) and the four weekly incremental files: the rows each carries."""
    r = np.random.default_rng([W.SEED, 31])
    monthly = []
    weeks = [[] for _ in W.WEEKS]

    def week_of(day):
        for k, (a, b) in enumerate(W.WEEKS):
            if a <= day <= b:
                return k
        return None

    for npi in sorted(recs):
        rec = recs[npi]
        kind = rec.get("kind")
        if kind == "new":
            weeks[week_of(rec["enumerated"])].append(nppes_row(r, rec, "active"))
            continue
        if kind == "deact":
            monthly.append(nppes_row(r, rec, "blank"))
            continue
        if kind == "react":
            monthly.append(nppes_row(r, rec, "blank"))
            back = dict(rec, last_update=rec["reactivated"], reactivated_shown=rec["reactivated"])
            weeks[week_of(rec["reactivated"])].append(nppes_row(r, back, "active"))
            continue
        if kind == "mover":
            monthly.append(nppes_row(r, rec, "active"))
            to = rec["moved_to"]
            if to in W.COUNTIES:
                z = [z for z in W.ZIPS[to] if W.county_of_zip(z) == to][int(r.integers(3))]
                city, state = W.CITY[z], "WA"
            else:
                city, z, state = {"Spokane": ("SPOKANE", "99204", "WA"), "Seattle": ("SEATTLE", "98122", "WA")}[to]
            addr = {"line1": "%d %s" % (int(r.integers(100, 4800)), W.STREETS[int(r.integers(len(W.STREETS)))]),
                    "line2": "Suite %d" % int(r.integers(100, 400)), "city": city, "state": state, "zip": z}
            addr["zip9"] = _zip9(r, z)
            moved = dict(rec, practice=addr, mailing=dict(addr), last_update=rec["moved_on"])
            weeks[week_of(rec["moved_on"])].append(nppes_row(r, moved, "active"))
            continue
        if kind == "switch":
            monthly.append(nppes_row(r, rec, "active"))
            t0 = rec["taxonomies"][0]
            sw = dict(rec, taxonomies=[(t0[0], t0[1], "N"), (rec["switched_to"], _license(r, rec["switched_to"]), "Y")],
                      cred="ARNP, PMHNP-BC", last_update=rec["switched_on"])
            weeks[week_of(rec["switched_on"])].append(nppes_row(r, sw, "active"))
            continue
        if kind in ("deact_late_before", "deact_late_after"):
            monthly.append(nppes_row(r, rec, "active"))
            weeks[week_of(rec["deactivated"])].append(nppes_row(r, rec, "blank"))
            continue
        monthly.append(nppes_row(r, rec, "active"))
    # the routine updates each week carries: phone numbers, suites, a renewed license, a corrected name
    pool = [n for n in sorted(recs) if recs[n].get("kind") in ("background", "background_org", "prescriber", "therapist",
                                                                  "pcp", "dark", "tele", "ed")]
    for k, (a, b) in enumerate(W.WEEKS):
        for npi in r.choice(pool, size=int(r.integers(55, 80)), replace=False):
            rec = dict(recs[str(npi)])
            rec["phone"] = _phone(r) if r.random() < 0.5 else rec.get("phone", "")
            rec["last_update"] = a + dt.timedelta(days=int(r.integers(0, 7)))
            if r.random() < 0.3 and rec["practice"]:
                rec["practice"] = dict(rec["practice"], line2=W.SUITES[int(r.integers(len(W.SUITES)))])
                rec["mailing"] = dict(rec["mailing"], line2=rec["practice"]["line2"])
            weeks[k].append(nppes_row(r, rec, "active"))
    for w in weeks:
        w.sort(key=lambda x: x[0])
    monthly.sort(key=lambda x: x[0])
    return monthly, weeks


def write_nppes(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_ALL, lineterminator="\r\n")
        w.writerow(NPPES_COLUMNS)
        for row in rows:
            w.writerow(row)
    return len(rows)


def write_deactivations(recs, path):
    """CMS's deactivated NPI report: every NPI deactivated, with the date (the plan's copy of the 10 November file)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    r = np.random.default_rng([W.SEED, 32])
    rows = [(rec["npi"], rec["deactivated"]) for rec in recs.values() if rec.get("deactivated") and
            rec.get("kind") in ("deact", "react", "deact_late_before", "deact_late_after")]
    taken = set(recs)
    start, end = D(2019, 1, 2), D(2026, 11, 6)
    span = (end - start).days
    for _ in range(2600):
        npi = W.npi(r)
        if npi in taken:
            continue
        taken.add(npi)
        # deactivations run every business day, more of them in recent years
        while True:
            d = start + dt.timedelta(days=int(span * (1 - r.random() ** 1.6)))
            if d.weekday() < 5:
                break
        rows.append((npi, d))
    rows.sort(key=lambda x: (x[1], x[0]))
    wb = Workbook()
    ws = wb.active
    ws.title = "Deactivated NPIs"
    ws.append(["NPPES Deactivated NPI Report"])
    ws.append(["Run date: 11/10/2026"])
    ws.append([])
    ws.append(["NPI", "NPPES Deactivation Date"])
    for npi, d in rows:
        ws.append([npi, _mdy(d)])
    ws["A1"].font = Font(bold=True, size=12)
    for c in ws[4]:
        c.font = Font(bold=True)
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 26
    wb.save(path)
    return len(rows)


# ------------------------------------------------------------------ enrollment and claims

def span_rows(persons):
    """The enrollment system's spans for every member number with coverage on a day of the contract year."""
    r = np.random.default_rng([W.SEED, 40])
    rows = []
    sid = 7_300_000
    for p in persons:
        client = "%09dWA" % (100_000_000 + int(p.pid[1:]) * 3 % 899_999_999)
        for s in sorted(p.spells, key=lambda s: (s["start"], s["source"] != "RETRO")):
            sid += int(r.integers(1, 9))
            county = s["county"]
            zs = [z for z in W.ZIPS[county] if W.county_of_zip(z, basis="residential") == county]
            if county in ("Grant", "Franklin") and r.random() < 0.03:
                z = "99344"
            elif county == "Okanogan" and r.random() < 0.04:
                z = "98813"
            else:
                z = zs[int(r.integers(len(zs)))]
            rows.append(["S%08d" % sid, s["member_id"], client, p.dob.isoformat(), p.sex, GROUP_CODE[p.group],
                         s["start"].isoformat(), s["end"].isoformat() if s["end"] and s["end"] <= W.EXTRACT else "",
                         W.COUNTIES[county]["fips"], z,
                         {"NEW": "NEW", "RENEWAL": "RENEW", "RETRO": "RETRO", "TRANSFER": "MOVE"}[s["source"]]])
    rows.sort(key=lambda x: (x[1], x[6]))
    return rows


def write_spans(rows, path):
    return _w(path, SPAN_COLUMNS, rows)


def _money(x):
    return "%.2f" % x


def claim_rows(lines):
    out = []
    for ln in lines:
        out.append([ln["icn"], ln["line"], ln["freq"], ln["orig"], ln["member_id"], ln["arr"], ln["bill"], ln["render"],
                    ln["pos"], ln["proc"], ln["mod"], ln["units"], ln["from"].isoformat(), ln["thru"].isoformat()] +
                   list(ln["dx"]) + [_money(ln["billed"]), _money(ln["paid"]), ln["received"].isoformat(),
                                     ln["paid_date"].isoformat()])
    return out


def write_claims(rows, path):
    return _w(path, CLAIM_COLUMNS, rows)


# ------------------------------------------------------------------ reference files

OTHER_COUNTIES = {"Spokane": "53063", "King": "53033", "Pierce": "53053", "Snohomish": "53061", "Thurston": "53067",
                  "Clark": "53011", "Whitman": "53075", "Asotin": "53003", "Columbia": "53013"}
OTHER_ZIPS = [("99201", "Spokane", "SPOKANE"), ("99204", "Spokane", "SPOKANE"), ("99208", "Spokane", "SPOKANE"),
              ("99216", "Spokane", "SPOKANE VALLEY"), ("98101", "King", "SEATTLE"), ("98104", "King", "SEATTLE"),
              ("98122", "King", "SEATTLE"), ("98004", "King", "BELLEVUE"), ("98405", "Pierce", "TACOMA"),
              ("98201", "Snohomish", "EVERETT"), ("98501", "Thurston", "OLYMPIA"), ("98664", "Clark", "VANCOUVER"),
              ("99163", "Whitman", "PULLMAN"), ("99403", "Asotin", "CLARKSTON")]


def write_zip_county(path):
    """The HUD-USPS ZIP-county crosswalk, second quarter 2026, for the ZIP codes of the plan's providers and members."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    rows = []
    seen = set()
    for c, zs in sorted(W.ZIPS.items()):
        for z in zs:
            if z in seen:
                continue
            seen.add(z)
            if z in W.SPLIT:
                for cc, res, bus in W.SPLIT[z]:
                    oth = round((res + bus) / 2, 6)
                    rows.append([z, W.COUNTIES[cc]["fips"], W.CITY[z].upper(), "WA", res, bus, oth, round((3 * res + bus) / 4, 6)])
            elif z in W.SLIVER:
                oc, res, bus = W.SLIVER[z]
                oth = round((res + bus) / 2, 6)
                tot = round((3 * res + bus) / 4, 6)
                ofips = W.COUNTIES[oc]["fips"] if oc in W.COUNTIES else OTHER_COUNTIES[oc]
                rows.append([z, W.COUNTIES[c]["fips"], W.CITY[z].upper(), "WA", round(1 - res, 6), round(1 - bus, 6),
                             round(1 - oth, 6), round(1 - tot, 6)])
                rows.append([z, ofips, W.CITY[z].upper(), "WA", res, bus, oth, tot])
            else:
                rows.append([z, W.COUNTIES[c]["fips"], W.CITY[z].upper(), "WA", 1, 1, 1, 1])
    for z, cname, city in OTHER_ZIPS:
        rows.append([z, OTHER_COUNTIES[cname], city, "WA", 1, 1, 1, 1])
    rows.sort(key=lambda x: (x[0], -x[7]))
    wb = Workbook()
    ws = wb.active
    ws.title = "ZIP_COUNTY_062026"
    ws.append(["ZIP", "COUNTY", "USPS_ZIP_PREF_CITY", "USPS_ZIP_PREF_STATE", "RES_RATIO", "BUS_RATIO", "OTH_RATIO", "TOT_RATIO"])
    for row in rows:
        ws.append(row)
    for c in ws[1]:
        c.font = Font(bold=True)
    for k, wdt in enumerate([8, 9, 22, 22, 11, 11, 11, 11]):
        ws.column_dimensions[chr(65 + k)].width = wdt
    wb.save(path)
    return len(rows)


NUCC_ROWS = [
    ("101YA0400X", "Behavioral Health & Social Service Providers", "Counselor", "Addiction (Substance Use Disorder)", "Addiction (Substance Use Disorder) Counselor"),
    ("101YM0800X", "Behavioral Health & Social Service Providers", "Counselor", "Mental Health", "Mental Health Counselor"),
    ("103T00000X", "Behavioral Health & Social Service Providers", "Psychologist", "", "Psychologist"),
    ("1041C0700X", "Behavioral Health & Social Service Providers", "Social Worker", "Clinical", "Clinical Social Worker"),
    ("111N00000X", "Chiropractic Providers", "Chiropractor", "", "Chiropractor"),
    ("1223G0001X", "Dental Providers", "Dentist", "General Practice", "General Practice Dentistry"),
    ("193200000X", "Group", "Multi-Specialty", "", "Multi-Specialty Group"),
    ("193400000X", "Group", "Single Specialty", "", "Single Specialty Group"),
    ("152W00000X", "Eye and Vision Services Providers", "Optometrist", "", "Optometrist"),
    ("163W00000X", "Nursing Service Providers", "Registered Nurse", "", "Registered Nurse"),
    ("183500000X", "Pharmacy Service Providers", "Pharmacist", "", "Pharmacist"),
    ("207P00000X", "Allopathic & Osteopathic Physicians", "Emergency Medicine", "", "Emergency Medicine Physician"),
    ("207Q00000X", "Allopathic & Osteopathic Physicians", "Family Medicine", "", "Family Medicine Physician"),
    ("207QA0401X", "Allopathic & Osteopathic Physicians", "Family Medicine", "Addiction Medicine", "Addiction Medicine (Family Medicine) Physician"),
    ("207R00000X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "", "Internal Medicine Physician"),
    ("207RA0401X", "Allopathic & Osteopathic Physicians", "Internal Medicine", "Addiction Medicine", "Addiction Medicine (Internal Medicine) Physician"),
    ("207V00000X", "Allopathic & Osteopathic Physicians", "Obstetrics & Gynecology", "", "Obstetrics & Gynecology Physician"),
    ("208000000X", "Allopathic & Osteopathic Physicians", "Pediatrics", "", "Pediatrics Physician"),
    ("2084A0401X", "Allopathic & Osteopathic Physicians", "Psychiatry & Neurology", "Addiction Medicine", "Addiction Medicine (Psychiatry & Neurology) Physician"),
    ("2084P0800X", "Allopathic & Osteopathic Physicians", "Psychiatry & Neurology", "Psychiatry", "Psychiatry Physician"),
    ("2084P0802X", "Allopathic & Osteopathic Physicians", "Psychiatry & Neurology", "Addiction Psychiatry", "Addiction Psychiatry Physician"),
    ("2084P0804X", "Allopathic & Osteopathic Physicians", "Psychiatry & Neurology", "Child & Adolescent Psychiatry", "Child & Adolescent Psychiatry Physician"),
    ("2084P0805X", "Allopathic & Osteopathic Physicians", "Psychiatry & Neurology", "Geriatric Psychiatry", "Geriatric Psychiatry Physician"),
    ("208600000X", "Allopathic & Osteopathic Physicians", "Surgery", "", "Surgery Physician"),
    ("208D00000X", "Allopathic & Osteopathic Physicians", "General Practice", "", "General Practice Physician"),
    ("225100000X", "Respiratory, Developmental, Rehabilitative and Restorative Service Providers", "Physical Therapist", "", "Physical Therapist"),
    ("235Z00000X", "Speech, Language and Hearing Service Providers", "Speech-Language Pathologist", "", "Speech-Language Pathologist"),
    ("251E00000X", "Agencies", "Home Health", "", "Home Health Agency"),
    ("261QF0400X", "Ambulatory Health Care Facilities", "Clinic/Center", "Federally Qualified Health Center (FQHC)", "Federally Qualified Health Center (FQHC)"),
    ("261QM0801X", "Ambulatory Health Care Facilities", "Clinic/Center", "Mental Health (Including Community Mental Health Center)", "Mental Health Clinic/Center (Including Community Mental Health Center)"),
    ("261QM2800X", "Ambulatory Health Care Facilities", "Clinic/Center", "Methadone", "Methadone Clinic"),
    ("261QR1300X", "Ambulatory Health Care Facilities", "Clinic/Center", "Rural Health", "Rural Health Clinic/Center"),
    ("311500000X", "Nursing & Custodial Care Facilities", "Alzheimer Center (Dementia Center)", "", "Alzheimer Center (Dementia Center)"),
    ("332B00000X", "Suppliers", "Durable Medical Equipment & Medical Supplies", "", "Durable Medical Equipment & Medical Supplies Supplier"),
    ("333600000X", "Suppliers", "Pharmacy", "", "Pharmacy"),
    ("363A00000X", "Physician Assistants & Advanced Practice Nursing Providers", "Physician Assistant", "", "Physician Assistant"),
    ("363LA2200X", "Physician Assistants & Advanced Practice Nursing Providers", "Nurse Practitioner", "Adult Health", "Adult Health Nurse Practitioner"),
    ("363LF0000X", "Physician Assistants & Advanced Practice Nursing Providers", "Nurse Practitioner", "Family", "Family Nurse Practitioner"),
    ("363LP0808X", "Physician Assistants & Advanced Practice Nursing Providers", "Nurse Practitioner", "Psych/Mental Health", "Psychiatric/Mental Health Nurse Practitioner"),
    ("364SP0808X", "Physician Assistants & Advanced Practice Nursing Providers", "Clinical Nurse Specialist", "Psych/Mental Health", "Psychiatric/Mental Health Clinical Nurse Specialist"),
]


def write_nucc(path):
    rows = [list(x[:4]) + [x[4], "Individual" if not x[0].startswith(("19", "25", "26", "28", "31", "33")) else "Non-Individual"]
            for x in NUCC_ROWS]
    return _w(path, ["Code", "Grouping", "Classification", "Specialization", "Display Name", "Section"], rows, crlf=True)


FEE_DESC = {"99213": "Office/outpatient visit, established patient, low MDM", "99214": "Office/outpatient visit, established patient, moderate MDM",
            "99215": "Office/outpatient visit, established patient, high MDM", "90792": "Psychiatric diagnostic evaluation with medical services",
            "90833": "Psychotherapy, 30 minutes, with E/M (add-on)", "90834": "Psychotherapy, 45 minutes",
            "90837": "Psychotherapy, 60 minutes", "90832": "Psychotherapy, 30 minutes", "90847": "Family psychotherapy with patient",
            "99283": "Emergency department visit, moderate MDM", "99284": "Emergency department visit, moderate-high MDM",
            "99285": "Emergency department visit, high MDM", "90791": "Psychiatric diagnostic evaluation",
            "H0036": "Community psychiatric supportive treatment, per 15 minutes", "H0039": "Assertive community treatment, per 15 minutes",
            "H2015": "Comprehensive community support services, per 15 minutes", "T1017": "Targeted case management, per 15 minutes",
            "H0004": "Behavioral health counseling and therapy, per 15 minutes", "H0005": "Alcohol and/or drug services, group counseling",
            "H0020": "Alcohol and/or drug services, methadone administration and/or service", "H0001": "Alcohol and/or drug assessment",
            "H0031": "Mental health assessment, by non-physician"}


def write_fees(path):
    rows = []
    for code in sorted(FEE_DESC):
        rows.append([code, FEE_DESC[code], "2025-07-01", "2025-12-31", "%.2f" % W.FEE[code]])
        rows.append([code, FEE_DESC[code], "2026-01-01", "2026-06-30", "%.2f" % CL.fee(code, D(2026, 1, 1))])
    return _w(path, ["proc_cd", "description", "effective_from", "effective_thru", "max_allowable_per_unit_usd"], rows)


# ------------------------------------------------------------------ distractors

P60 = {"Adams": 0.931, "Benton": 0.996, "Chelan": 0.984, "Douglas": 0.957, "Franklin": 0.989, "Grant": 0.948,
       "Kittitas": 0.972, "Okanogan": 0.923, "Walla Walla": 0.991, "Yakima": 0.979}


def june_members(persons):
    """Members enrolled on 30 June 2026, by the county of the span covering that day."""
    out = {c: 0 for c in W.COUNTIES}
    day = W.WINDOW_END
    for p in persons:
        for s in p.spells:
            if s["start"] <= day and (s["end"] is None or s["end"] >= day):
                out[s["county"]] += 1
                break
    return out


def write_adequacy(path, persons):
    """The plan's time and distance report to the state for the second quarter of 2026 (behavioral health prescribers):
    the share of each county's members living within 30 and 60 minutes' drive of a contracted prescriber."""
    from openpyxl import Workbook
    from openpyxl.styles import Font
    r = np.random.default_rng([W.SEED, 50])
    june = june_members(persons)
    wb = Workbook()
    ws = wb.active
    ws.title = "BH Prescriber T&D Q2 2026"
    ws.append(["%s - Network Adequacy Time and Distance, Behavioral Health Prescribers, Q2 2026" % W.ORG])
    ws.append(["Standard: 90% of members within 60 minutes (rural) of a contracted behavioral health prescriber"])
    ws.append([])
    ws.append(["County", "Members (June 2026)", "Within 30 min", "Within 60 min", "Pct within 60 min", "Meets standard"])
    for c in sorted(W.COUNTIES):
        n = june[c]
        n60 = int(round(n * min(0.999, P60[c] + 0.004 * (r.random() - 0.5))))
        n30 = int(round(n60 * (0.64 + 0.3 * r.random())))
        ws.append([c, n, n30, n60, n60 / n, "Y" if n60 / n >= 0.90 else "N"])
    ws["A1"].font = Font(bold=True)
    for cell in ws[4]:
        cell.font = Font(bold=True)
    for k, wdt in enumerate([14, 20, 15, 15, 18, 15]):
        ws.column_dimensions[chr(65 + k)].width = wdt
    for row in ws.iter_rows(min_row=5, min_col=5, max_col=5):
        for c in row:
            c.number_format = "0.0%"
    wb.save(path)
    return len(W.COUNTIES)


OFM_POP = {"Adams": (21330, 14420), "Benton": (215700, 160300), "Chelan": (80500, 63600), "Douglas": (45230, 34700),
           "Franklin": (101300, 68900), "Grant": (104100, 75400), "Kittitas": (46300, 38500), "Okanogan": (43750, 35100),
           "Walla Walla": (63400, 50300), "Yakima": (259800, 186600)}


def write_ofm(path):
    rows = [[W.COUNTIES[c]["fips"], c, tot, adult, "2026-04-01"] for c, (tot, adult) in sorted(OFM_POP.items())]
    return _w(path, ["county_fips", "county", "total_population", "population_18_and_over", "estimate_date"], rows)


# ------------------------------------------------------------------ the data dictionary and the manifest

DICT_FILES = [
    (FILES["claims"], "The claims system's extract of behavioral-health claims and encounters: every claim and encounter "
     "line with a service date from 1 July 2025 to 30 June 2026 that carries a behavioral-health diagnosis or procedure code "
     "or a behavioral-health rendering or billing provider, paid or accepted through 31 October 2026. Every version of a "
     "claim is included. Sorted by paid or accepted date."),
    (FILES["spans"], "The enrollment system's spans for every member number with coverage on at least one day from 1 July "
     "2025 to 30 June 2026. A span is a continuous period under one member number, eligibility group and county of "
     "residence; dates are inclusive."),
    (FILES["nppes"], "NPPES full replacement monthly file of October 2026 (data through 11 October 2026), the records with "
     "a Washington practice location or mailing address and the records of NPIs on the plan's provider file."),
    (FILES["week1"], "NPPES weekly incremental file, 12 to 18 October 2026: records created or updated that week, same "
     "selection and layout as the monthly file."),
    (FILES["week2"], "NPPES weekly incremental file, 19 to 25 October 2026."),
    (FILES["week3"], "NPPES weekly incremental file, 26 October to 1 November 2026."),
    (FILES["week4"], "NPPES weekly incremental file, 2 to 8 November 2026."),
    (FILES["deact"], "CMS's NPPES Deactivated NPI Report of 10 November 2026, the rows for NPIs that had a Washington "
     "address in NPPES before deactivation or are on the plan's provider file (CMS publishes the national list)."),
    (FILES["zipcty"], "HUD-USPS ZIP code to county crosswalk, second quarter 2026, for the ZIP codes of the plan's members "
     "and providers."),
    (FILES["nucc"], "The NUCC health care provider taxonomy code set, version 26.1, for the codes in the NPPES records."),
    (FILES["fees"], "The plan's fee schedule for behavioral-health professional services in the contract year. A "
     "fee-for-service line is allowed the lesser of its billed charge and the maximum allowable for its units."),
    (FILES["policy"], "Network Policy NP-31, Prescriber Service Area Designation."),
    (FILES["adequacy"], "The plan's network adequacy report to the Health Care Authority for the second quarter of 2026: "
     "time and distance to a contracted behavioral-health prescriber."),
    (FILES["ofm"], "Office of Financial Management April 1, 2026 population estimates for the ten counties."),
    (FILES["manifest"], "The list of the files Network Analytics pulled on 12 November 2026."),
]
DICT_FIELDS = [
    (FILES["claims"], "clm_icn", "Internal control number of the claim or encounter (one per version)."),
    (FILES["claims"], "clm_line_num", "Line number within the claim."),
    (FILES["claims"], "clm_freq_cd", "Claim frequency code: 1 original; 7 replacement of the claim in orig_icn; 8 void of "
     "the claim in orig_icn."),
    (FILES["claims"], "orig_icn", "For a replacement or void, the claim it replaces or voids."),
    (FILES["claims"], "mbr_id", "The plan's member number on the date of service."),
    (FILES["claims"], "fin_arrangement_cd", "FFS: fee-for-service claim. SUBCAP: encounter reported by a sub-capitated "
     "behavioral health agency or opioid treatment program, paid through its monthly capitation."),
    (FILES["claims"], "billing_npi", "NPI of the billing provider."),
    (FILES["claims"], "rendering_npi", "NPI of the clinician who rendered the service; blank where the agency reports none."),
    (FILES["claims"], "pos_cd", "CMS place of service code (02 and 10 telehealth; 11 office; 23 emergency department; 53 "
     "community mental health center; 57 non-residential substance use disorder treatment facility)."),
    (FILES["claims"], "proc_cd", "CPT or HCPCS procedure code."),
    (FILES["claims"], "proc_mod1", "First procedure modifier (95: synchronous telemedicine)."),
    (FILES["claims"], "svc_units", "Units of service."),
    (FILES["claims"], "svc_from_dt", "First date of service of the line."),
    (FILES["claims"], "svc_thru_dt", "Last date of service of the line."),
    (FILES["claims"], "dx_cd_1", "ICD-10-CM diagnosis code in the first position, as billed (no decimal point)."),
    (FILES["claims"], "dx_cd_2", "Second diagnosis code."),
    (FILES["claims"], "dx_cd_3", "Third diagnosis code."),
    (FILES["claims"], "dx_cd_4", "Fourth diagnosis code."),
    (FILES["claims"], "billed_amt", "Billed charge (USD)."),
    (FILES["claims"], "paid_amt", "Amount paid (USD); 0.00 on SUBCAP encounters."),
    (FILES["claims"], "clm_rcvd_dt", "Date the claim system received the claim or encounter."),
    (FILES["claims"], "clm_paid_dt", "Date the claim was paid or the encounter accepted."),
    (FILES["spans"], "span_id", "Identifier of the span."),
    (FILES["spans"], "mbr_id", "The plan's member number. A person enrolling again after more than 90 days without "
     "coverage is issued a new member number."),
    (FILES["spans"], "client_id", "The Health Care Authority's client identifier; a person keeps it across member numbers."),
    (FILES["spans"], "birth_dt", "Date of birth."),
    (FILES["spans"], "sex_cd", "Sex as the Health Care Authority reports it."),
    (FILES["spans"], "elig_group_cd", "Eligibility group: SSI-DIS disabled adults (SSI-related); ADULT-EXP adults 19 to 64 "
     "eligible under the Medicaid expansion; PARENT-CR parents and caretaker relatives; AGED-65 adults 65 and over."),
    (FILES["spans"], "span_start_dt", "First day of coverage in the span."),
    (FILES["spans"], "span_end_dt", "Last day of coverage in the span; blank while the span is open."),
    (FILES["spans"], "res_county_fips", "County of residence (FIPS) for the span."),
    (FILES["spans"], "res_zip", "Residence ZIP code for the span."),
    (FILES["spans"], "span_reason_cd", "NEW: new enrollment; RENEW: renewal or return after a short gap; RETRO: coverage the "
     "Health Care Authority backdated to before the application month; MOVE: the member moved to another county."),
    (FILES["deact"], "NPI", "Deactivated NPI."),
    (FILES["deact"], "NPPES Deactivation Date", "Date NPPES deactivated the NPI."),
    (FILES["zipcty"], "RES_RATIO", "Share of the ZIP code's residential addresses in the county."),
    (FILES["zipcty"], "BUS_RATIO", "Share of the ZIP code's business addresses in the county."),
    (FILES["zipcty"], "OTH_RATIO", "Share of the ZIP code's other addresses in the county."),
    (FILES["zipcty"], "TOT_RATIO", "Share of all the ZIP code's addresses in the county."),
    (FILES["fees"], "max_allowable_per_unit_usd", "The plan's maximum allowable amount per unit for services in the "
     "effective period."),
]


def write_dictionary(path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Files"
    ws.append(["File name", "What it holds"])
    for row in DICT_FILES:
        ws.append(list(row))
    ws2 = wb.create_sheet("Columns")
    ws2.append(["File name", "Column", "Definition"])
    for row in DICT_FIELDS:
        ws2.append(list(row))
    for s, widths in ((ws, [48, 120]), (ws2, [46, 28, 110])):
        for c in s[1]:
            c.font = Font(bold=True)
        s.freeze_panes = "A2"
        for k, wdt in enumerate(widths):
            s.column_dimensions[chr(65 + k)].width = wdt
        for row in s.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    return len(DICT_FIELDS)


def write_manifest(path, n):
    src = {"claims": "Claims system (paid claims and accepted encounters)", "spans": "Enrollment system",
           "nppes": "CMS NPPES downloadable file", "week1": "CMS NPPES downloadable file",
           "week2": "CMS NPPES downloadable file", "week3": "CMS NPPES downloadable file",
           "week4": "CMS NPPES downloadable file", "deact": "CMS NPPES downloadable file",
           "zipcty": "HUD USER", "nucc": "National Uniform Claim Committee", "fees": "Provider reimbursement",
           "policy": "Network Development", "dict": "Network Analytics", "adequacy": "Network Development",
           "ofm": "Washington State Office of Financial Management"}
    when = {"claims": "2026-11-12", "spans": "2026-11-12", "nppes": "2026-10-13", "week1": "2026-10-20",
            "week2": "2026-10-27", "week3": "2026-11-03", "week4": "2026-11-10", "deact": "2026-11-10",
            "zipcty": "2026-09-18", "nucc": "2026-07-01", "fees": "2026-01-14", "policy": "2026-05-21",
            "dict": "2026-11-12", "adequacy": "2026-08-14", "ofm": "2026-06-30"}
    rows = []
    for k, name in FILES.items():
        if k == "manifest":
            continue
        cnt = n.get(k)
        rows.append([name, "" if cnt is None else str(cnt), src[k], when[k]])
    return _w(path, ["file_name", "record_count", "system_of_record", "as_of_date"], rows)
