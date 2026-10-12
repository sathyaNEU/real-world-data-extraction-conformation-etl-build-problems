"""Write the evidence pack: every file as the system or team that owns it would export it."""
import csv
import datetime as dt
import io
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import core as C
import supply as SU
import world as W

TD = dt.timedelta
FILES = {
    "listing": "lyrevo_line_listing_PSUR6_DLP20260930.csv",
    "dosage": "lyrevo_dosage_lines_PSUR6.csv",
    "feed": "psp_lab_feed_2023-2026.csv",
    "labreg": "psp_laboratory_register.xlsx",
    "dupreg": "duplicate_register_PSUR6.xlsx",
    "terms": "rmp_term_list_version_4.xlsx",
    "annex": "RVB-417_RMP_annex7_methods.pdf",
    "guide": "safety_export_field_guide.pdf",
    "sellin": "sellin_wholesaler_monthly_2023-2026.csv",
    "calloff": "tender_calloffs_FR_IT_ES_2025-2026.xlsx",
    "master": "product_master_national_codes.csv",
    "xevmpd": "xevmpd_presentations_RVB-417.xml",
    "channels": "market_supply_channels.xlsx",
    "section5": "PSUR6_section5_exposure_method.docx",
    "finance": "finance_net_sales_by_market_quarter.xlsx",
    "medinfo": "medinfo_enquiries_2023-2026.xlsx",
    "litscreen": "literature_screening_PSUR6.csv",
    "signals": "signal_tracker_2026.xlsx",
    "log": "PSUR6_data_package_log.txt",
}
DISTRACTORS = ["medinfo", "litscreen", "signals"]
REFEREE = "finance"
# workbook owner and last-saved stamp
WB = {
    "labreg": ("PSP Data Management", dt.datetime(2026, 9, 29, 11, 20)),
    "dupreg": ("PV Case Processing", dt.datetime(2026, 10, 5, 17, 41)),
    "terms": ("Lasse Christoffersen", dt.datetime(2026, 8, 21, 14, 6)),
    "calloff": ("Sundby Pharma Logistics", dt.datetime(2026, 10, 6, 6, 31)),
    "channels": ("Supply Chain Planning", dt.datetime(2026, 9, 14, 10, 2)),
    "finance": ("Finance Controlling", dt.datetime(2026, 10, 6, 9, 15)),
    "medinfo": ("Medical Information", dt.datetime(2026, 10, 2, 16, 48)),
    "signals": ("Signal Management", dt.datetime(2026, 9, 30, 18, 12)),
}
HDR_FONT = Font(bold=True)
HDR_FILL = PatternFill("solid", fgColor="DDE3EA")


def write_csv(path, df):
    df.to_csv(path, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def _sheet(ws, header, rows, widths=None, start_row=1):
    for j, h in enumerate(header):
        c = ws.cell(row=start_row, column=j + 1, value=h)
        c.font = HDR_FONT
        c.fill = HDR_FILL
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            ws.cell(row=start_row + 1 + i, column=j + 1, value=v)
    for j, w in enumerate(widths or []):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j + 1)].width = w
    ws.freeze_panes = ws.cell(row=start_row + 1, column=1)


def _wb(key, path, sheets):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, fn in sheets:
        ws = wb.create_sheet(title)
        fn(ws)
    owner, stamp = WB[key]
    wb.properties.creator = owner
    wb.properties.lastModifiedBy = owner
    wb.properties.created = stamp - TD(days=120)
    wb.properties.modified = stamp
    wb.save(path)


def saved_stamp(key):
    return WB[key][1].strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------ safety side

def write_labreg(path, df):
    def main(ws):
        _sheet(ws, list(df.columns), df.values.tolist(), [10, 40, 8, 8, 9, 7, 10, 10, 11])

    def notes(ws):
        lines = ["Reference limits as notified by each PSP partner laboratory with its result transfers.",
                 "Upper limits (uln_male, uln_female) and lower limit (lln) are in the laboratory's own unit.",
                 "Maintained by the PSP vendor's data management team; changes are notified to Drug Safety."]
        for i, t in enumerate(lines):
            ws.cell(row=i + 1, column=1, value=t)
        ws.column_dimensions["A"].width = 100
    _wb("labreg", path, [("register", main), ("notes", notes)])


def write_dupreg(path, df):
    def main(ws):
        rows = []
        for r in df.itertuples(index=False):
            rows.append([r.master_case_no, r.duplicate_case_no, dt.date.fromisoformat(r.linked_on), r.link_reason, r.linked_by])
        _sheet(ws, list(df.columns), rows, [16, 18, 12, 70, 20])
        for row in ws.iter_rows(min_row=2, min_col=3, max_col=3):
            for c in row:
                c.number_format = "yyyy-mm-dd"
    _wb("dupreg", path, [("Duplicate links", main)])


def write_terms(path, terms, changes):
    def main(ws):
        _sheet(ws, list(terms.columns), terms.values.tolist(), [44, 58, 46, 28])

    def chg(ws):
        _sheet(ws, list(changes.columns), changes.values.tolist(), [10, 40, 46, 9, 13, 90])
    _wb("terms", path, [("Term list v4", main), ("Changes v3 to v4", chg)])


# ------------------------------------------------------------------ supply side

MATERIAL = {}


def _material(c, p):
    k = (c, p)
    if k not in MATERIAL:
        MATERIAL[k] = str(100480000 + 37 * (W.MARKET_ORDER.index(c) * 4 + int(p)) + (W.MARKET_ORDER.index(c) * 13) % 11)
    return MATERIAL[k]


CUSTNO = {}


def write_sellin(path, sellin):
    rows = []
    for r in sellin:
        c = r["market"]
        ctype, codes = SU.CODES[c]
        code = codes[r["pres"]]
        if c == "DE" and r["wholesaler"] == SU.STRIPPED_PZN_WHOLESALER:
            code = code.lstrip("0")
        if r["wholesaler"] not in CUSTNO:
            CUSTNO[r["wholesaler"]] = str(2100000 + 1301 * (len(CUSTNO) + 1))
        rows.append([r["period"], "%s01" % c, c, CUSTNO[r["wholesaler"]], r["wholesaler"], _material(c, r["pres"]), code,
                     r["doc"], r["reason"], str(r["qty"]), "%.2f" % r["value"]])
    rows.sort(key=lambda x: (x[0], x[2], x[3], x[5], {"F2": 0, "FOC": 1, "RE": 2}[x[7]]))
    import pandas as pd
    df = pd.DataFrame(rows, columns=["posting_period", "sales_org", "country", "customer_no", "customer_name", "material",
                                     "national_code", "billing_type", "reason", "quantity", "net_value_eur"])
    write_csv(path, df)
    return df


def write_calloffs(path, calloff):
    rows = []
    n = 0
    for r in sorted(calloff, key=lambda r: (r["date"], r["market"], r["region"], r["pres"])):
        n += 1
        tender = {"FR": "FR-AO-%d-%03d", "IT": "IT-GARA-%d-%04d", "ES": "ES-EXP-%d-%03d"}[r["market"]] % (
            2024 if r["market"] == "FR" else 2025, 100 + (sum(map(ord, r["region"])) % 600))
        rows.append(["CO%07d" % (2500000 + n * 3), r["date"], r["market"], r["region"], r["hosp"], tender,
                     SU.HOSP_GTIN[r["market"]][r["pres"]], r["cases"]])

    def main(ws):
        head = ["Hospital call-off deliveries, client Ravnsborg Pharma A/S, product Lyrevo",
                "Sundby Pharma Logistics ApS, client report CR-114 (tender call-offs, FR / IT / ES)",
                "Deliveries 03.02.2025 to 06.10.2026, report run 06.10.2026 06:30",
                "Quantities in shipper cases (1 case = 10 packs)"]
        for i, t in enumerate(head):
            ws.cell(row=i + 1, column=1, value=t)
        ws.cell(row=1, column=1).font = HDR_FONT
        _sheet(ws, ["call_off_no", "delivery_date", "country", "region", "hospital", "tender_ref", "gtin", "qty"],
               rows, [12, 13, 8, 28, 11, 15, 16, 6], start_row=6)
        for row in ws.iter_rows(min_row=7, min_col=2, max_col=2):
            for c in row:
                c.number_format = "dd.mm.yyyy"
        for row in ws.iter_rows(min_row=7, min_col=7, max_col=7):
            for c in row:
                c.number_format = "@"
    _wb("calloff", path, [("call-offs", main)])
    return rows


def write_master(path):
    import pandas as pd
    names = {"DK": "Lyrevo filmovertrukne tabletter %d mg", "SE": "Lyrevo filmdragerade tabletter %d mg",
             "NO": "Lyrevo tabletter, filmdrasjerte %d mg", "FI": "Lyrevo tabletti, kalvopäällysteinen %d mg",
             "DE": "Lyrevo %d mg Filmtabletten", "AT": "Lyrevo %d mg Filmtabletten", "NL": "Lyrevo %d mg filmomhulde tabletten",
             "BE": "Lyrevo %d mg filmomhulde tabletten", "FR": "LYREVO %d mg, comprimé pelliculé",
             "IT": "LYREVO %d MG COMPRESSE RIVESTITE CON FILM", "ES": "LYREVO %d MG COMPRIMIDOS RECUBIERTOS CON PELICULA",
             "PL": "Lyrevo %d mg tabletki powlekane", "PT": "Lyrevo %d mg comprimidos revestidos por película"}
    rows = []
    for c in W.MARKET_ORDER:
        ctype, codes = SU.CODES[c]
        for p in ("001", "002", "003", "004"):
            st = SU.PRES[p][0]
            rows.append([codes[p], ctype, c, SU.EU + p, names[c] % st, str(st), "15", W.MARKETS[c][0].isoformat()])
    for c in W.HOSPITAL_MARKETS:
        for p in ("001", "002", "003", "004"):
            st = SU.PRES[p][0]
            rows.append([SU.HOSP_GTIN[c][p], "GTIN", c, SU.EU + p, names[c] % st, str(st), "15", W.MARKETS[c][0].isoformat()])
    df = pd.DataFrame(rows, columns=["national_code", "code_type", "market", "eu_presentation", "product_name",
                                     "strength_mg", "who_ddd_mg", "valid_from"])
    write_csv(path, df)
    return df


def write_xevmpd(path):
    ev = {"001": "PRD5872013", "002": "PRD5872014", "003": "PRD5872015", "004": "PRD5872016"}
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<evprmExport xmlns="urn:ravnsborg:xevmpd:export:1" exportDate="2026-09-28" sender="Ravnsborg Pharma A/S" '
             'mahCode="ORG-100047751" source="Article 57 database, own submissions">']
    for p in ("001", "002", "003", "004"):
        st, ps = SU.PRES[p]
        lines += ['  <authorisedProduct>',
                  '    <evCode>%s</evCode>' % ev[p],
                  '    <productName>Lyrevo %d mg film-coated tablets</productName>' % st,
                  '    <authorisationNumber>%s%s</authorisationNumber>' % (SU.EU, p),
                  '    <authorisationProcedure>Centralised</authorisationProcedure>',
                  '    <authorisationDate>2023-02-14</authorisationDate>',
                  '    <activeSubstance code="SUB212487">RVB-417</activeSubstance>',
                  '    <strength numerator="%d" numeratorUnit="mg" denominator="1" denominatorUnit="tablet"/>' % st,
                  '    <pharmaceuticalForm>Film-coated tablet</pharmaceuticalForm>',
                  '    <routeOfAdministration>Oral use</routeOfAdministration>',
                  '    <package>',
                  '      <description>Blister (PVC/PCTFE/Aluminium), calendar blister</description>',
                  '      <packSize unit="tablet">%d</packSize>' % ps,
                  '    </package>',
                  '    <lastUpdate>2025-11-03</lastUpdate>',
                  '  </authorisedProduct>']
    lines.append('</evprmExport>')
    open(path, "w").write("\n".join(lines) + "\n")


def write_channels(path):
    rows = []
    sellin_src = "SAP SD billing, BW query ZSD_SELLIN_M (monthly, by customer and national code)"
    for c in W.MARKET_ORDER:
        frm = W.MARKETS[c][0]
        if c in W.HOSPITAL_MARKETS:
            rows.append([c, "Retail pharmacy", frm, "Wholesaler", sellin_src, "Community pharmacies, minority of patients"])
            rows.append([c, "Hospital pharmacy", frm, "3PL against regional tender call-offs",
                         "Sundby Pharma Logistics client report CR-114",
                         "Hospital-only dispensing for most patients; prices under regional tenders"])
        else:
            rows.append([c, "Retail pharmacy", frm, "Wholesaler", sellin_src, ""])
        if c in ("DE", "NL", "DK", "SE", "NO", "FI", "AT"):
            rows.append([c, "PSP bridging supply", frm, "Wholesaler, free of charge",
                         sellin_src, "Free packs for programme patients while reimbursement is arranged"])

    def main(ws):
        _sheet(ws, ["market", "channel", "supplied_from", "supply_route", "data_source", "comment"], rows,
               [8, 18, 13, 34, 66, 60])
        for row in ws.iter_rows(min_row=2, min_col=3, max_col=3):
            for cc in row:
                cc.number_format = "yyyy-mm-dd"
    _wb("channels", path, [("channels", main)])


def write_finance(path, fin):
    rows = []
    for c in W.MARKET_ORDER:
        for (y, q) in sorted({(y, q) for (cc, y, q) in fin if cc == c}):
            if (y, q) > (2026, 3):
                continue
            rows.append([c, "%d-Q%d" % (y, q), round(fin[(c, y, q)])])

    def main(ws):
        head = ["Net sales by market, EUR, management accounts (SAP CO-PA, product Lyrevo)",
                "Closed quarters only; extracted 06.10.2026"]
        for i, t in enumerate(head):
            ws.cell(row=i + 1, column=1, value=t)
        ws.cell(row=1, column=1).font = HDR_FONT
        _sheet(ws, ["market", "quarter", "net_sales_eur"], rows, [8, 10, 16], start_row=4)
        for row in ws.iter_rows(min_row=5, min_col=3, max_col=3):
            for cc in row:
                cc.number_format = "#,##0"
    _wb("finance", path, [("net sales", main)])
    return rows


# ------------------------------------------------------------------ the log

def write_log(path, counts):
    L = []
    L.append("PSUR 6 DATA PACKAGE  -  LYREVO (RVB-417)")
    L.append("Data lock point 30-SEP-2026        Package assembled 06-OCT-2026        Owner: Drug Safety, Ravnsborg Pharma A/S")
    L.append("Prepared by Lasse Christoffersen (Safety Data Lead)")
    L.append("")
    L.append("RUN  SYSTEM / SOURCE                    QUERY OR REPORT                 RUN (CET)          ROWS   FILE")
    runs = [
        ("01", "Argus Safety 8.4", "RVB_PSUR_LL_ALLVERS v3", "06-OCT-2026 07:42", counts["listing"], FILES["listing"]),
        ("02", "Argus Safety 8.4", "RVB_DOSAGE_LINES v2", "06-OCT-2026 07:49", counts["dosage"], FILES["dosage"]),
        ("03", "Argus Safety 8.4", "DUP_REGISTER_LYREVO", "06-OCT-2026 07:51", counts["dupreg"], FILES["dupreg"]),
        ("04", "PSP vendor SFTP", "LAB_TRANSFER_SAFETY_LINKED", "06-OCT-2026 06:05", counts["feed"], FILES["feed"]),
        ("05", "PSP vendor SFTP", "LAB_REGISTER", "29-SEP-2026 11:20", counts["labreg"], FILES["labreg"]),
        ("06", "SAP BW", "ZSD_SELLIN_M", "06-OCT-2026 05:10", counts["sellin"], FILES["sellin"]),
        ("07", "Sundby Pharma Logistics", "CR-114", "06-OCT-2026 06:30", counts["calloff"], FILES["calloff"]),
        ("08", "Regulatory Information Mgmt", "National code mapping", "02-OCT-2026 13:12", counts["master"], FILES["master"]),
        ("09", "xEVMPD (Article 57)", "Presentations export", "28-SEP-2026 09:40", 4, FILES["xevmpd"]),
        ("10", "SAP CO-PA", "Net sales by market", "06-OCT-2026 09:15", counts["finance"], FILES["finance"]),
        ("11", "Medical Information (IRMS)", "Enquiry log export", "02-OCT-2026 16:48", counts["medinfo"], FILES["medinfo"]),
        ("12", "Literature screening", "Weekly search log", "05-OCT-2026 10:05", counts["litscreen"], FILES["litscreen"]),
        ("13", "Signal Management", "Signal tracker 2026", "30-SEP-2026 18:12", counts["signals"], FILES["signals"]),
    ]
    for r in runs:
        L.append("%-4s %-34s %-31s %-18s %6s   %s" % (r[0], r[1], r[2], r[3], "{:,}".format(r[4]), r[5]))
    L.append("")
    L.append("DOCUMENTS")
    L.append("  %s   RMP annex 7, version 3.0, effective 24-AUG-2026" % FILES["annex"])
    L.append("  %s   Field guide DS-FG-021 version 4" % FILES["guide"])
    L.append("  %s   PSUR 6 section 5 method note, draft of 05-OCT-2026" % FILES["section5"])
    L.append("  %s   RMP term list version 4, in force from 14-NOV-2025" % FILES["terms"])
    L.append("  %s   Market supply channel overview, Supply Chain Planning" % FILES["channels"])
    L.append("")
    L.append("NOTES")
    L.append("  Run 01 returns every version of every Lyrevo case received up to the run, whatever the receipt date.")
    L.append("  Runs 06 and 07 return supply up to the run; posting period 2026-10 and deliveries in October are part months.")
    L.append("  MedDRA version 29.0 is used under the company's MSSO subscription. xEVMPD data are the company's own")
    L.append("  Article 57 submissions. Laboratory data are transferred under the PSP data processing agreement.")
    L.append("")
    open(path, "w").write("\n".join(L) + "\n")
