"""Cut the shipped files from the clean truth: the two contractors' case exports, the area weights file keyed on the
pre-2024 numbering, the ministry's crosswalk, the region list, the code lists and the two distractors."""
import csv
import datetime as dt
import io

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font

import world as W

FILES = {
    "northmark": "northmark_phms_case_export_2023-2025.csv",
    "ostrander": "ostrander_phms2025_cases.json",
    "weights": "phms_area_weights_2023-2025.csv",
    "crosswalk": "moh_survey_area_concordance_2024.xlsx",
    "regions": "health_regions.csv",
    "nm_codes": "northmark_disposition_codes.txt",
    "os_codes": "ostrander_code_frame.txt",
    "report": "phms_2025_technical_report.pdf",
    "terms": "wexcombe_boost_terms_2027.pdf",
    "pharmacy": "community_pharmacy_register_2025.csv",
    "quotes": "phms2027_fieldwork_quotes.xlsx",
}
DISTRACTORS = ["community_pharmacy_register_2025.csv", "phms2027_fieldwork_quotes.xlsx"]

# Northmark's disposition codes (AAPOR-style numbering of its own case system)
NM_DISP = {W.COMPLETE: "1100", W.PROXY: "1120", W.PARTIAL: "1200", W.REFUSAL: "2110", W.NONCONTACT: "2200",
           W.VACANT: "4700", W.OTHER: "2350", W.WITHDRAWN: "3910"}
NM_ITEM = {"yes": "1", "no": "2", "noRx": "3", "dk": "7", "ref": "8", None: ""}
# Ostrander's code frame
OS_DISP = {W.COMPLETE: "CI", W.PROXY: "CP", W.PARTIAL: "PI", W.REFUSAL: "RF", W.NONCONTACT: "NC",
           W.VACANT: "VD", W.OTHER: "OT", W.WITHDRAWN: "WD"}
OS_ITEM = {"yes": "Y", "no": "N", "noRx": "NP", "dk": "DK", "ref": "RF", None: ""}


def code_at(c):
    """The area code a case carries: Northmark's 2023 cases and its 2024 cases assigned before its system took up
    the new numbering carry the pre-2024 code; everything later carries the new code."""
    a = c["area"]
    if c["wave"] == 2023:
        return a["old_code"]
    if c["wave"] == 2024 and c["assigned"] < W.NORTHMARK_SWITCH:
        return a["old_code"]
    return a["new_code"]


def _interviewers(world):
    """A stable interviewer per area and contractor, with a few areas changing hands between waves."""
    rng = W.rng_for(7)
    nm = ["NM%03d" % int(x) for x in rng.choice(np.arange(101, 489), size=64, replace=False)]
    os_ = ["OS-%04d" % int(x) for x in rng.choice(np.arange(1000, 9999), size=26, replace=False)]
    ids = {}
    for a in world["areas"]:
        base_nm = nm[int(rng.integers(0, len(nm)))]
        for wave in (2023, 2024, 2025):
            who = base_nm if rng.random() > 0.12 else nm[int(rng.integers(0, len(nm)))]
            ids[(id(a), wave, "A")] = who
        ids[(id(a), 2025, "B")] = os_[int(rng.integers(0, len(os_)))]
    return ids


def case_numbers(world):
    """Northmark numbers its cases per wave in issue order (N23-, N24-, N25-); Ostrander its own (OST25-)."""
    nums = {}
    for wave in (2023, 2024, 2025):
        rng = W.rng_for(8, wave)
        seq_a = int(rng.integers(10200, 10900))
        seq_b = int(rng.integers(40100, 40800))
        ordered = sorted(world["cases"][wave], key=lambda c: (c["assigned"], c["area"]["new_code"], c["line"],
                                                               c["reissue_of"] is not None))
        for c in ordered:
            if W.contractor(wave, c["area"]["new_region"]) == "A":
                seq_a += int(rng.integers(1, 3))
                nums[id(c)] = "N%02d-%06d" % (wave % 100, seq_a)
            else:
                seq_b += int(rng.choice([1, 1, 1, 1, 2, 3]))
                nums[id(c)] = "OST25-%05d" % seq_b
    return nums


def northmark_rows(world):
    nums = case_numbers(world)
    ivw = _interviewers(world)
    rows = []
    for wave in (2023, 2024, 2025):
        for c in world["cases"][wave]:
            a = c["area"]
            if W.contractor(wave, a["new_region"]) != "A":
                continue
            done = c["cls"] in (W.COMPLETE, W.PROXY, W.PARTIAL)
            rows.append({
                "wave": wave,
                "case_no": nums[id(c)],
                "area_at_assignment": code_at(c),
                "listing_line": c["line"],
                "assigned": c["assigned"].isoformat(),
                "disposition": NM_DISP[c["cls"]],
                "disposition_date": c["outcome_date"].isoformat(),
                "reissue_of": nums[id(c["reissue_of"])] if c["reissue_of"] is not None else "",
                "interviewer": ivw[(id(a), wave, "A")],
                "hh_size": c.get("hh_size", "") if done else "",
                "q_rx_cost": NM_ITEM[c.get("item")] if done else "",
            })
    rows.sort(key=lambda r: (r["wave"], r["case_no"]))
    return rows


NM_COLS = ["wave", "case_no", "area_at_assignment", "listing_line", "assigned", "disposition", "disposition_date",
           "reissue_of", "interviewer", "hh_size", "q_rx_cost"]


def ostrander_rows(world):
    nums = case_numbers(world)
    ivw = _interviewers(world)
    rows = []
    for c in world["cases"][2025]:
        a = c["area"]
        if W.contractor(2025, a["new_region"]) != "B":
            continue
        done = c["cls"] in (W.COMPLETE, W.PROXY, W.PARTIAL)
        r = a["new_region"]
        num = int(a["new_code"][1:])
        rows.append([
            nums[id(c)],
            "%s-%03d" % (W.RABBR[r], num),
            c["line"],
            c["assigned"].strftime("%d/%m/%Y"),
            OS_DISP[c["cls"]],
            c["outcome_date"].strftime("%d/%m/%Y"),
            nums[id(c["reissue_of"])] if c["reissue_of"] is not None else None,
            ivw[(id(a), 2025, "B")],
            c.get("hh_size") if done else None,
            OS_ITEM[c.get("item")] if (done and c.get("item") is not None) else None,
        ])
    rows.sort(key=lambda r: r[0])
    return rows


OS_COLS = ["Case ID", "Survey area", "Listing line", "Date issued", "Final disposition", "Disposition date",
           "Reissue of", "Interviewer", "Household size", "RX_COST"]


def weights_rows(world):
    """The weighting system's area table, one row per wave and area, keyed on the pre-2024 numbering."""
    rows = []
    for wave in (2023, 2024, 2025):
        for a in sorted(world["areas"], key=lambda a: a["old_code"]):
            rows.append({
                "wave": wave,
                "area_pre2024": a["old_code"],
                "stratum": "CVS" if a["supplement"] else "%02d" % a["old_region"],
                "design_weight": "%.2f" % a["design_weight"],
                "occupied_dwellings": a["occupied"][wave],
            })
    return rows


W_COLS = ["wave", "area_pre2024", "stratum", "design_weight", "occupied_dwellings"]

OLD_RNAME = {1: "North", 2: "Central Valley", 3: "Lakeshore", 4: "Southern Uplands", 5: "Metro"}


def write_csv(path, cols, rows, delimiter=","):
    buf = io.StringIO()
    wr = csv.DictWriter(buf, fieldnames=cols, delimiter=delimiter, lineterminator="\r\n")
    wr.writeheader()
    for r in rows:
        wr.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())
    return len(rows)


def write_ostrander(path, rows):
    """Ostrander's case system exports the wave as one JSON document: a header and one object per case."""
    import json
    keys = ["case_id", "survey_area", "listing_line", "date_issued", "final_disposition", "disposition_date",
            "reissue_of", "interviewer", "household_size", "rx_cost"]
    doc = {"export": "PHMS 2025 case file", "exported": "2025-06-17T14:02:11-06:00", "system": "Ostrander CaseTrack 4.2",
           "cases": [dict(zip(keys, r)) for r in rows]}
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)
        f.write("\n")
    return len(rows)


def write_crosswalk(path, world):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Concordance"
    ws["A1"] = "Health region reorganisation: survey area concordance, effective 1 April 2024"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Ministry of Health, Health System Planning Branch. Issued 14 March 2024."
    ws.append([])
    hdr = ["Survey area (to 31 March 2024)", "Health region (to 31 March 2024)", "Survey area (from 1 April 2024)",
           "Health region (from 1 April 2024)"]
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for a in sorted(world["areas"], key=lambda a: a["old_code"]):
        ws.append([a["old_code"], OLD_RNAME[a["old_region"]], a["new_code"], W.RNAME[a["new_region"]]])
    for col, wdt in zip("ABCD", (18, 20, 18, 20)):
        ws.column_dimensions[col].width = wdt
    wb.save(path)
    return len(world["areas"])


def regions_rows():
    return [{"region": r, "region_name": n, "abbreviation": ab} for r, n, ab in W.REGIONS]


NM_CODES_TXT = """Northmark Field Research - PHMS case system - disposition and item codes
Case system release 7.4

DISPOSITION
1100  Complete interview, household health contact
1120  Complete interview, another adult household member
1200  Partial interview, ended before the end of section D
2110  Refusal
2200  No contact after the full call pattern
2350  Other non-interview (language, illness, away for the period)
3910  Withdrawn, not worked
4700  Not a dwelling or vacant

Q_RX_COST  In the past 12 months, did anyone in this household not fill a prescription because of the cost?
1  Yes
2  No
3  No prescription to fill in the past 12 months
7  Don't know
8  Refused
blank  Not asked
"""

OS_CODES_TXT = """OSTRANDER DATA COLLECTION INC.
CODE FRAME  PHMS 2025  (v2.1, 27 January 2025)

Final disposition
CI   Complete interview
CP   Complete interview by another adult member of the household
PI   Partial interview (did not reach the end of section D)
RF   Refusal
NC   Non-contact
OT   Other non-response
WD   Withdrawn from the workload, not attempted
VD   Vacant or not a private dwelling

RX_COST   Prescription not filled because of cost, past 12 months (household)
Y    Yes
N    No
NP   No prescription in the past 12 months
DK   Don't know
RF   Refused
(empty)   Item not reached
"""


def pharmacy_rows(world):
    """A distractor: the College of Pharmacists' 2025 register of community pharmacies by health region."""
    rng = W.rng_for(9)
    chains = ["Rexall", "Shoppers Drug Mart", "Pharmasave", "Guardian", "IDA", "London Drugs", "Medicine Shoppe",
              "Co-op Pharmacy", "Remedy'sRx"]
    per_region = {1: 21, 2: 74, 3: 46, 4: 33, 5: 188}
    rows = []
    reg = 2101
    for r in (1, 2, 3, 4, 5):
        for i in range(per_region[r]):
            reg += int(rng.integers(3, 29))
            if rng.random() < 0.3:
                name = "Independent pharmacy"
            else:
                name = "%s #%d" % (chains[int(rng.integers(0, len(chains)))], int(rng.integers(100, 9900)))
            rows.append({
                "licence_no": "CP-%05d" % reg,
                "pharmacy_name": name,
                "health_region": W.RNAME[r],
                "setting": ("remote" if r == 1 else str(rng.choice(["urban", "urban", "town", "rural"]))),
                "dispensing_fee_cad": "%.2f" % float(rng.choice([11.99, 12.15, 12.50, 12.99, 13.25, 14.20])),
                "hours_per_week": int(rng.choice([40, 44, 50, 55, 60, 72, 84])),
            })
    rows.sort(key=lambda r: r["licence_no"])
    return rows


P_COLS = ["licence_no", "pharmacy_name", "health_region", "setting", "dispensing_fee_cad", "hours_per_week"]


def write_quotes(path):
    """A distractor: the two contractors' 2027 quotes per completed interview, by region."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Quotes"
    ws["A1"] = "PHMS 2027 fieldwork: rates quoted per completed interview (CAD, before tax)"
    ws["A1"].font = Font(bold=True)
    ws.append([])
    ws.append(["Health region", "Northmark Field Research", "Ostrander Data Collection", "Notes"])
    for c in ws[3]:
        c.font = Font(bold=True)
    data = [("North", 212.40, 239.00, "Fly-in communities priced per trip; boost interviews at the same rate"),
            ("Central Valley", 96.75, 88.50, ""),
            ("Lakeshore", 104.20, 97.25, ""),
            ("Southern Uplands", 118.60, 124.00, ""),
            ("Metro", 84.10, 91.75, "Evening and weekend calls included")]
    for d in data:
        ws.append([v if v != "" else None for v in d])
    ws.append([])
    ws.append(["Quotes received 30 September 2026 (Northmark) and 2 October 2026 (Ostrander); valid to 31 January 2027."])
    for col, wdt in zip("ABCD", (18, 24, 25, 62)):
        ws.column_dimensions[col].width = wdt
    wb.save(path)
