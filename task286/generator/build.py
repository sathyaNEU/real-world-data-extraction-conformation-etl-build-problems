"""task286 pack builder: writes target/, golden/, generator/figures.json and metadata.json. Deterministic."""
import csv
import json
import os
import re
import shutil
import zipfile
from datetime import date, datetime, timedelta

import numpy as np

import world as W
import records as R
import docs as D
import golden as G

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
EXPORT_TIME = (2026, 10, 19, 8, 47, 22)
EXPORT_TS = datetime(*EXPORT_TIME).timestamp()

F_METER = "meter_reads_daily_2025-26.parquet"
F_MATCH = "pw_property_uprn_match_2026-10.csv"
F_GAZ = "county_gazetteer_extract_2026-10.csv"
F_TDC_L = "teversby_ctax_legacy_archive_to_2026-05-04.csv"
F_TDC_N = "teversby_ctax_extract_2026-10-05.xlsx"
F_SBC = "swanholt_ctax_extract_2026-10-06.csv"
F_NDR = "ndr_self_catering_entries_2026-10.csv"
F_CEN = "census2021_household_spaces_oa.csv"
F_LKP = "oa21_to_community_area_bestfit.csv"
F_TOR = "homes_in_use_pilot_terms_of_reference_v1-2.pdf"
F_DSA = "pennimouth_water_data_sharing_agreement_PW-DSA-2026-014.pdf"
F_CTB = "council_taxbase_returns_october_2025.pdf"
F_HNA = "housing_needs_assessment_2024_summary.pdf"


def ds(d):
    return "" if d is None else d.isoformat()


def uk(d):
    return "" if d is None else d.strftime("%d/%m/%Y")


def write_csv(name, header, rows, crlf=False):
    path = os.path.join(TARGET, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return path


def normalise_zip(path, modified, member_time):
    """rewrite an OOXML zip with fixed member times and order, so rebuilds are byte-identical."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    for name, data in items:
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                          b"\\g<1>" + modified.encode() + b"\\g<2>", data)
        out.append((name, data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=member_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def wb_new(creator, title, created, modified):
    from openpyxl import Workbook
    wb = Workbook()
    p = wb.properties
    p.creator = creator
    p.lastModifiedBy = creator
    p.title = title
    p.created = created
    p.modified = modified
    return wb


def wb_save(wb, path, modified, member_time):
    wb.save(path)
    normalise_zip(path, modified, member_time)


# --------------------------------------------------------------------------------------------- water files
def write_meter(homes):
    import pyarrow as pa
    import pyarrow.parquet as pq
    refs, serials, dates, litres, types = [], [], [], [], []
    for h in sorted(homes, key=lambda x: x.prop_ref):
        for serial, i, l, t in R.meter_rows(h):
            refs.append(h.prop_ref)
            serials.append(serial)
            dates.append(W.DAYS[i])
            litres.append(l)
            types.append(t)
    table = pa.table({"PROPERTY_REF": pa.array(refs, pa.string()),
                      "METER_SERIAL": pa.array(serials, pa.string()),
                      "READ_DATE_UTC": pa.array(dates, pa.date32()),
                      "CONSUMPTION_L": pa.array(litres, pa.int32()),
                      "READ_TYPE": pa.array(types, pa.string())})
    pq.write_table(table, os.path.join(TARGET, F_METER), compression="zstd", row_group_size=250000,
                   write_statistics=True, use_dictionary=["METER_SERIAL", "READ_TYPE"])
    return len(refs)


def write_match(homes):
    rows = []
    for h in sorted(homes, key=lambda x: x.prop_ref):
        uprn = "" if h.match == "UNMATCHED" else str(h.uprn)
        meth = "" if h.match == "UNMATCHED" else h.match
        rows.append([h.prop_ref, uprn, meth, R.billing_address(h) + " " + R.town(h).upper(), h.postcode,
                     "HOUSEHOLD"])
    write_csv(F_MATCH, ["PROPERTY_REF", "UPRN", "MATCH_METHOD", "BILLING_ADDRESS", "POSTCODE", "PROPERTY_CLASS"],
              rows, crlf=True)


def write_gazetteer(homes, parents, entries):
    xref = {}
    for e in entries:
        if e["site"]:
            xref[e["site"]["uprn"]] = e["ba_ref"]
        else:
            xref[e["homes"][0].uprn] = e["ba_ref"]
    rows = []
    first_built = {}
    for h in homes:
        if h.parent_uprn:
            first_built[h.parent_uprn] = min(first_built.get(h.parent_uprn, h.built), h.built)
    for p in parents:
        cls, desc = ("PP", "Property Shell")
        if first_built.get(p["uprn"], date(2014, 4, 1)) > date(2014, 4, 1):
            p_start = first_built[p["uprn"]] - timedelta(days=160 + p["uprn"] % 90)
        else:
            p_start = date(2001, 3, 19) + timedelta(days=int(p["uprn"] % 3300))
        rows.append({"UPRN": p["uprn"], "PARENT_UPRN": "", "CLASS": cls, "CLASS_DESC": desc, "SAO_TEXT": "",
                     "PAO_START_NUMBER": p["number"] or "", "PAO_TEXT": p["name"] or "",
                     "STREET_DESCRIPTION": p["street"] if p["kind"] != "site" else "",
                     "TOWN_NAME": W.AREA_NAME[p["area"]], "POSTCODE_LOCATOR": p["postcode"],
                     "COMMUNITY_AREA_CODE": p["area"], "COMMUNITY_AREA": W.AREA_NAME[p["area"]],
                     "BLPU_STATE": 2, "START_DATE": ds(p_start),
                     "NDR_XREF": xref.get(p["uprn"], "")})
    for h in homes:
        cls = h.ptype
        desc = {"RD02": "Detached", "RD03": "Semi-Detached", "RD04": "Terraced",
                "RD06": "Self Contained Flat (Includes Maisonette / Apartment)"}[cls]
        start = h.built if h.kind == "flats_new" else date(2002, 6, 14) + timedelta(days=int(h.uprn % 2400))
        rows.append({"UPRN": h.uprn, "PARENT_UPRN": h.parent_uprn or "", "CLASS": cls, "CLASS_DESC": desc,
                     "SAO_TEXT": h.flat or "", "PAO_START_NUMBER": h.number if h.kind != "flats_old" else h.number,
                     "PAO_TEXT": h.building or "", "STREET_DESCRIPTION": h.street if h.kind != "site" else "",
                     "TOWN_NAME": W.AREA_NAME[h.area], "POSTCODE_LOCATOR": h.postcode,
                     "COMMUNITY_AREA_CODE": h.area, "COMMUNITY_AREA": W.AREA_NAME[h.area], "BLPU_STATE": 2,
                     "START_DATE": ds(start), "NDR_XREF": xref.get(h.uprn, "")})
    for h in homes:
        if h.kind == "site":
            pass
    rows.sort(key=lambda r: int(r["UPRN"]))
    # a site's cottages carry the site's name as their building name on its own lane
    hdr = list(rows[0].keys())
    write_csv(F_GAZ, hdr, [[r[k] for k in hdr] for r in rows])
    return len(rows)


# ------------------------------------------------------------------------------------- council tax and NDR
def write_ctax(homes):
    leg, new, sbc = R.ctax_tables(homes)
    hdr = ["PROP_REF", "VO_REF", "ADDR_1", "ADDR_2", "ADDR_3", "POSTCODE", "BAND", "ACC_NO", "FROM_DATE",
           "TO_DATE", "STATUS", "EXEMPT_CLASS", "CLOSE_REASON"]
    write_csv(F_TDC_L, hdr, [[uk(r[k]) if isinstance(r[k], date) else r[k] for k in hdr] for r in leg], crlf=True)
    # the new system's export: one sheet of liabilities and the system's own field list
    wb = wb_new("Revenues and Benefits", "Council tax liabilities extract", datetime(2026, 10, 5, 7, 2, 41),
                datetime(2026, 10, 5, 7, 2, 41))
    ws = wb.active
    ws.title = "Liabilities"
    cols = ["Property ID", "UPRN", "Valuation List Ref", "Address", "Postcode", "Band", "Account", "Legacy Account",
            "Liability From", "Liability To", "Occupation", "Furnished", "Exemption Class"]
    ws.append(cols)
    for r in new:
        ws.append([r[c] if not isinstance(r[c], date) else datetime(r[c].year, r[c].month, r[c].day) for c in cols])
    for row in ws.iter_rows(min_row=2, min_col=9, max_col=10):
        for c in row:
            c.number_format = "dd/mm/yyyy"
    widths = [12, 14, 20, 52, 10, 6, 12, 15, 14, 14, 13, 10, 15]
    for i, wdt in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = wdt
    ws.freeze_panes = "A2"
    wb_save(wb, os.path.join(TARGET, F_TDC_N), "2026-10-05T07:02:41Z", (2026, 10, 5, 7, 2, 42))
    hdr = ["PROPERTY_REF", "UPRN", "VOA_REF", "ADDRESS", "POSTCODE", "BAND", "ACCOUNT_REF", "LIAB_START",
           "LIAB_END", "OCC_STATUS", "EX_CLASS", "ENTERED_ON"]
    write_csv(F_SBC, hdr, [[ds(r[k]) if isinstance(r[k], date) or (k == "LIAB_END" and r[k] is None) else r[k]
                            for k in hdr] for r in sbc])
    return leg, new, sbc


def write_ndr(entries):
    rows = []
    for e in entries:
        h0 = e["homes"][0]
        if e["site"]:
            addr = "%s, %s" % (e["site"]["name"].upper(), R.town(h0).upper())
            pc = e["site"]["postcode"]
            desc = "SELF CATERING HOLIDAY UNITS AND PREMISES"
        else:
            addr = R.billing_address(h0) + ", " + R.town(h0).upper()
            pc = h0.postcode
            desc = "SELF CATERING HOLIDAY UNIT AND PREMISES"
        rows.append([e["ba_ref"], desc, addr, pc, e["rv"], ds(e["from"]), ds(e["to"])])
    write_csv(F_NDR, ["BA_REFERENCE", "PRIMARY_DESCRIPTION", "FULL_PROPERTY_ADDRESS", "POSTCODE", "RATEABLE_VALUE",
                      "EFFECTIVE_FROM", "EFFECTIVE_TO"], rows)


def write_census(oas):
    rows = []
    for o in sorted(oas, key=lambda x: x["code"]):
        rows.append([o["code"], o["spaces"], o["spaces"] - o["nur"], o["nur"]])
    write_csv(F_CEN, ["geography code", "Household spaces: All household spaces",
                      "Household spaces: At least one usual resident", "Household spaces: No usual residents"], rows)
    rows = [[o["code"], o["bestfit"], W.AREA_NAME[o["bestfit"]]] for o in sorted(oas, key=lambda x: x["code"])]
    write_csv(F_LKP, ["OA21CD", "CA_CODE", "CA_NAME"], rows)


# ----------------------------------------------------------------------------------------------- metadata
def write_metadata():
    files = {
        F_METER: ("Pennimouth Water smart meter head end, daily consumption extract (PW-DSA-2026-014)", "2026-10-12"),
        F_MATCH: ("Pennimouth Water property to gazetteer UPRN match (PW-DSA-2026-014)", "2026-10-12"),
        F_GAZ: ("county address gazetteer extract, shortlisted community areas", "2026-10-07"),
        F_TDC_L: ("Teversby District Council legacy revenues system archive, liabilities to go-live", "2026-05-04"),
        F_TDC_N: ("Teversby District Council revenues system, council tax liabilities extract", "2026-10-05"),
        F_SBC: ("Swanholt Borough Council revenues system, council tax liabilities extract", "2026-10-06"),
        F_NDR: ("business rates list, self-catering entries for the shortlisted areas, as at the extract", "2026-10-08"),
        F_CEN: ("Census 2021 household spaces by output area for the shortlisted areas", "2023-01-05"),
        F_LKP: ("county research team best-fit lookup, 2021 output areas to community areas", "2024-02-19"),
        F_TOR: ("National Homes Agency, Homes in Use pilot terms of reference, version 1.2", "2026-09-08"),
        F_DSA: ("Pennimouth Water data sharing agreement PW-DSA-2026-014", "2026-09-01"),
        F_CTB: ("the two councils' published Council Taxbase returns, October 2025", "2025-10-20"),
        F_HNA: ("Teversby and Swanholt Housing Needs Assessment 2024, summary report", "2024-11-28"),
    }
    meta = {
        "task": "task286",
        "decision": "which shortlisted community area the 2027 Homes in Use pilot runs in",
        "deliverables": ["homes_in_use_pilot_2027.xlsx", "empty_homes_by_area_2026.png"],
        "distractor_files": ["target/" + F_CEN, "target/" + F_LKP, "target/" + F_HNA],
        "wrong_basis_distractor": {
            "file": "target/" + F_HNA,
            "basis": "household spaces with no usual residents on census day, 21 March 2021, by community area, "
                     "which ranks Tarnhithe and Kittlesea first; it counts homes nobody was living in on one day five "
                     "years before the pilot's weeks, second homes and holiday lets in use that season included",
            "ruled_out_by": "terms of reference 4.1 and 4.3 (" + F_TOR + "): the pilot goes to the area with the most "
                            "homes nobody used for at least 26 of the 52 weeks from 29 September 2025 to 27 September "
                            "2026, a week counting as a week of use if anybody lived in, stayed at or used the home on "
                            "any day of it",
        },
        "files": {("target/" + k): {"source": "constructed for this task (an invented county, its councils, its "
                                              "water company and a fictional national housing agency)",
                                    "covers": v[0], "date": v[1], "licence": "CC BY 4.0 (constructed for this task)"}
                  for k, v in sorted(files.items())},
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=1, sort_keys=True)
    return sorted(files)


def cut_zip():
    path = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo("target/" + fn, date_time=EXPORT_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, fn), "rb").read())
    os.utime(path, (EXPORT_TS, EXPORT_TS))


def main():
    for folder in (TARGET, GOLDEN):
        if os.path.isdir(folder):
            shutil.rmtree(folder)
    os.makedirs(TARGET)
    os.makedirs(GOLDEN)
    homes, parents, entries, oas = R.build_all()
    n_rows = write_meter(homes)
    write_match(homes)
    n_gaz = write_gazetteer(homes, parents, entries)
    write_ctax(homes)
    write_ndr(entries)
    write_census(oas)
    D.write_all(TARGET, homes, oas, F_TOR, F_DSA, F_CTB, F_HNA)
    figs = G.figures(homes, entries, oas, n_rows)
    G.write_golden(GOLDEN, figs)
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    names = write_metadata()
    for folder in (TARGET, GOLDEN):
        for fn in os.listdir(folder):
            os.utime(os.path.join(folder, fn), (EXPORT_TS, EXPORT_TS))
    assert sorted(os.listdir(TARGET)) == names, (sorted(os.listdir(TARGET)), names)
    cut_zip()
    print("built %d files, %d meter rows, %d gazetteer rows; call %s" % (len(names), n_rows, n_gaz, figs["call"]))


if __name__ == "__main__":
    main()
