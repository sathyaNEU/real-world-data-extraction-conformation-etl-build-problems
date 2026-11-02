"""task483 pack: the files under target/, each written the way its producing system writes it.

The pathology network's culture export spans its old laboratory system and the one that took every specimen from
7 September 2026 (each system's own accession numbers, date layout, result wording and organism codes; the
laboratory's code table is the current system's). The federation's issue extract comes from its EMIS and SystmOne
practices and the extended access hub. The register, the code lists, the organism and antimicrobial tables and the
three files nobody's calculation needs are written here too; the specification is docs.py's.
"""
import csv
import datetime as dt
import io

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import records as R
import world as W

FILES = {
    "cultures": "urine_culture_results_2024-2026.csv",
    "issues": "gp_uti_antibacterial_issues_2024-2026.csv",
    "register": "member_practice_register_2026.xlsx",
    "codelists": "uti_pathway_code_lists_2027-28.xlsx",
    "organisms": "laboratory_organism_codes.csv",
    "antimicrobials": "laboratory_antimicrobial_codes.csv",
    "spec": "uti_pathway_specification_2027-28.pdf",
    "icb": "icb_antimicrobial_prescribing_2025-26.xlsx",
    "cdiff": "c_difficile_community_cases_2024-2026.csv",
    "lists": "gp_registered_list_sizes_2026-10.csv",
}
DISTRACTORS = ("icb", "cdiff", "lists")

LAB_ABX = [("AMX", "AMOX"), ("AMC", "COAM"), ("CEX", "CEPH"), ("CPD", "CPOD"), ("CIP", "CIPR"), ("FOS", "FOSF"),
           ("GEN", "GENT"), ("MEC", "MECI"), ("NIT", "NITR"), ("TMP", "TRIM"), ("ETP", "ERTA")]
LAB_COLS = ["LabNo", "NHSNumberPseudo", "Sex", "AgeYears", "GPPracticeCode", "RequestingLocation", "SpecimenType",
            "DateCollected", "DateTimeReceived", "DateTimeAuthorised", "CultureResult", "OrganismCode"] + \
           [c for _, c in LAB_ABX]
OLD_CODE = {"EFAE": "ENTE", "ECLO": "ENTC"}
NEW_CODE = {"EFAE": "ENTC", "ECLO": "ECLO"}
RESULT_TEXT = {
    "old": {"POS": "Significant growth", "MIX": "Mixed growth", "NSG": "No significant growth"},
    "new": {"POS": "Significant growth", "MIX": "Mixed growth - doubtful significance", "NSG": "No significant growth"},
}
ISSUE_COLS = ["IssuingOrganisationCode", "RegisteredPracticeCode", "PatientPseudonym", "Sex", "AgeAtIssue",
              "IssueDate", "MedicationName", "Quantity", "Dosage", "IssueType", "LinkedProblem"]

ORGANISM_TABLE = [
    ("ABAU", "Acinetobacter baumannii complex"), ("CAND", "Candida species"), ("CFRE", "Citrobacter freundii complex"),
    ("CKOS", "Citrobacter koseri"), ("CNST", "Coagulase-negative Staphylococcus"), ("ECLO", "Enterobacter cloacae complex"),
    ("ECOL", "Escherichia coli"), ("ENTC", "Enterococcus species"), ("KAER", "Klebsiella aerogenes"),
    ("KOXY", "Klebsiella oxytoca"), ("KPNE", "Klebsiella pneumoniae"), ("MMOR", "Morganella morganii"),
    ("PAER", "Pseudomonas aeruginosa"), ("PMIR", "Proteus mirabilis"), ("PVUL", "Proteus vulgaris"),
    ("PRET", "Providencia rettgeri"), ("SAGA", "Streptococcus agalactiae (group B)"), ("SAUR", "Staphylococcus aureus"),
    ("SMAR", "Serratia marcescens"), ("SSAP", "Staphylococcus saprophyticus"),
]
ANTIMICROBIAL_TABLE = [("AMOX", "Amoxicillin"), ("COAM", "Amoxicillin-clavulanic acid"), ("CEPH", "Cefalexin"),
                       ("CPOD", "Cefpodoxime"), ("CIPR", "Ciprofloxacin"), ("ERTA", "Ertapenem"),
                       ("FOSF", "Fosfomycin"), ("GENT", "Gentamicin"), ("MECI", "Mecillinam"),
                       ("NITR", "Nitrofurantoin"), ("TRIM", "Trimethoprim")]


def write_csv(path, cols, rows, lineterminator="\r\n"):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator=lineterminator)
        w.writerow(cols)
        for r in rows:
            w.writerow(r)
    return len(rows)


def _d_old(d):
    return d.strftime("%d/%m/%Y")


def _dt_old(t):
    return t.strftime("%d/%m/%Y %H:%M")


def culture_rows(specs):
    """One row per organism a specimen grew (one row for a specimen that grew none), accession numbers as each system
    issues them: the old system's by year of receipt, the new system's from its go-live."""
    rows = []
    seq_old, seq_new = {}, 1000
    rng = W.rng_for("lab-render")
    for s in specs:
        new = s["received"].date() >= W.LIMS_GO_LIVE
        if new:
            seq_new += 1 + int(rng.random() < 0.07)
            lab = "%02dU%07d" % (s["received"].year % 100, seq_new)
            fd, fdt, codes, txt = (lambda d: d.isoformat()), (lambda t: t.strftime("%Y-%m-%d %H:%M")), NEW_CODE, RESULT_TEXT["new"]
        else:
            y = s["received"].year
            seq_old[y] = seq_old.get(y, 0) + 1 + int(rng.random() < 0.05)
            lab = "H%02dU%06d" % (y % 100, seq_old[y])
            fd, fdt, codes, txt = _d_old, _dt_old, OLD_CODE, RESULT_TEXT["old"]
        s["lab_no"] = lab
        base = [lab, R.pseudo(s["pid"]), s["sex"], s["age"], s["gp"], s["requester"], s["type"], fd(s["collected"]),
                fdt(s["received"]), fdt(s["authorised"]), txt[s["result"]]]
        if s["result"] != "POS" or not s["orgs"]:
            rows.append(base + [""] + [""] * len(LAB_ABX))
            continue
        for org, res in s["orgs"]:
            vals = []
            for d, _ in LAB_ABX:
                v = res.get(d)
                if org == "EFAE" and d in ("CPD", "GEN", "CIP", "ETP"):
                    # the old system printed its whole automated panel; the new one's reporting rules suppress
                    # agents an enterococcus is not treated with
                    v = None if new else ("R" if d in ("CPD", "ETP") else (v or ("S" if rng.random() < 0.7 else "R")))
                if v is None:
                    vals.append("")
                elif v == "S" and d in ("CIP", "CPD") and rng.random() < 0.03:
                    vals.append("I")
                else:
                    vals.append(v)
            rows.append(base + [codes.get(org, org)] + vals)
    return rows


def issue_rows(issues):
    rows = []
    for i in issues:
        rows.append([i["issuer"], i["gp"], R.pseudo(i["pid"]), i["sex"], W.age_on(i["birth"], i["day"]),
                     i["day"].isoformat(), i["product"], i["qty"], i["dosage"], i["type"], i["problem"]])
    return rows


def _style_header(ws, ncol):
    for c in range(1, ncol + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="DCE6F1")
        cell.alignment = Alignment(vertical="top", wrap_text=True)


def register_workbook(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Member practices"
    ws.append(["Hollinbrook Health Federation member practice register, as at 31 December 2026. Networks are those "
               "agreed with the ICB for 2027-28. Owner: Federation business office. Version 2026.4, refreshed "
               "08/01/2027."])
    ws.append([])
    cols = ["Practice code", "Practice name", "PCN code", "Primary care network", "Clinical system",
            "Registered patients (Oct 2026)", "Status"]
    ws.append(cols)
    lists = list_sizes()
    for pr in W.practices():
        status = "Active"
        if pr["code"] == W.MERGE_FROM:
            status = "Merged into J83102 Hollin Lane Medical Practice on 01/07/2026"
        elif pr["code"] == W.MERGE_INTO:
            status = "Active (absorbed J83386 Stanbridge Road Surgery on 01/07/2026)"
        n = 0 if pr["code"] == W.MERGE_FROM else sum(v for (c, _, _), v in lists.items() if c == pr["code"])
        ws.append([pr["code"], pr["name"], pr["pcn"], pr["network"], "SystmOne" if pr["system"] == "SystmOne" else "EMIS Web",
                   n if n else None, status])
    ws.append([W.HUB, "Hollinbrook Extended Access Hub", None, "Federation-wide", "EMIS Web", None,
               "Active (evening and weekend appointments for patients of every member practice)"])
    for c, w in zip("ABCDEFG", (14, 34, 10, 20, 14, 16, 62)):
        ws.column_dimensions[c].width = w
    ws.freeze_panes = "A4"
    for c in range(1, 8):
        ws.cell(row=3, column=c).font = Font(bold=True)
    ws2 = wb.create_sheet("Networks")
    ws2.append(["PCN code", "Primary care network", "Member practices from 1 July 2026"])
    for net, pcn, prs in W.NETWORKS:
        k = len([p for p in prs if p[0] != W.MERGE_FROM])
        ws2.append([pcn, net, k])
    for c, w in zip("ABC", (10, 22, 30)):
        ws2.column_dimensions[c].width = w
    _style_header(ws2, 3)
    wb.save(path)


def codelist_workbook(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pathway antibacterials"
    ws.append(["Medication name (as issued)", "Pathway antibacterial"])
    names = {"NIT": "Nitrofurantoin", "TMP": "Trimethoprim", "MEC": "Pivmecillinam", "CEX": "Cefalexin",
             "AMC": "Co-amoxiclav", "FOS": "Fosfomycin", "AMX": "Amoxicillin"}
    seen = set()
    for drug in ("NIT", "TMP", "MEC", "CEX", "AMC", "FOS", "AMX"):
        for emis_name, s1_name, _, _ in R.PRODUCTS[drug]:
            for nm in (emis_name, s1_name):
                if nm not in seen:
                    seen.add(nm)
                    ws.append([nm, names[drug]])
        if drug in R.CHILD_PRODUCTS:
            ws.append([R.CHILD_PRODUCTS[drug][0], names[drug]])
    ws.append(["Trimethoprim 100mg tablets", "Trimethoprim"])
    ws.append(["Amoxicillin 250mg/5ml oral suspension", "Amoxicillin"])
    ws.column_dimensions["A"].width = 58
    ws.column_dimensions["B"].width = 22
    _style_header(ws, 2)
    ws2 = wb.create_sheet("Lower UTI problems")
    ws2.append(["Linked problem (SNOMED CT preferred term)", "Lower UTI for the pathway"])
    for t in ("Urinary tract infection", "Lower urinary tract infection", "Cystitis", "Acute cystitis",
              "Recurrent urinary tract infection"):
        ws2.append([t, "Yes"])
    for t in ("Urinary tract infection in pregnancy", "Asymptomatic bacteriuria in pregnancy", "Pyelonephritis",
              "Prostatitis", "Catheter-associated urinary tract infection"):
        ws2.append([t, "No"])
    ws2.column_dimensions["A"].width = 48
    ws2.column_dimensions["B"].width = 26
    _style_header(ws2, 2)
    wb.save(path)


def list_sizes():
    """NHS Digital style registered list, October 2026: practice, sex, five-year band (women 16 to 64 as in world.py)."""
    rng = W.rng_for("lists")
    out = {}
    bands = ["0_4", "5_9", "10_14", "15_19", "20_24", "25_29", "30_34", "35_39", "40_44", "45_49", "50_54", "55_59",
             "60_64", "65_69", "70_74", "75_79", "80_84", "85_89", "90_94", "95+"]
    shape = np.array([5.1, 5.6, 5.9, 5.8, 5.9, 6.4, 6.9, 6.8, 6.5, 6.3, 6.9, 6.8, 6.1, 5.4, 5.2, 4.1, 2.8, 1.6, 0.7, 0.2])
    for pr in W.practices():
        if pr["code"] == W.MERGE_FROM:
            continue
        women = pr["women"] + (dict((p["code"], p["women"]) for p in W.practices())[W.MERGE_FROM]
                               if pr["code"] == W.MERGE_INTO else 0)
        w1664 = shape[3:13].sum() - shape[3] * 0.8
        scale = women / w1664
        for sex in ("FEMALE", "MALE"):
            for b, s in zip(bands, shape):
                adj = 1.0 if sex == "FEMALE" else (1.02 if b in ("0_4", "5_9", "10_14", "15_19") else
                                                    (0.97 if s > 3 else 0.78))
                out[(pr["code"], sex, b)] = int(round(s * scale * adj * float(rng.lognormal(0, 0.035))))
    return out


def list_rows():
    rows = []
    for (code, sex, band), n in sorted(list_sizes().items(), key=lambda kv: (kv[0][0], kv[0][1], _band_key(kv[0][2]))):
        rows.append(["GP_PRAC_PAT_LIST", "01OCT2026", "GP", "QHB", code, sex, band, n])
    return rows


def _band_key(b):
    return int(b.split("_")[0].rstrip("+"))


def cdiff_rows():
    rng = W.rng_for("cdiff")
    rows = []
    month = dt.date(2024, 1, 1)
    while month <= dt.date(2026, 12, 1):
        for pr in W.practices():
            if pr["code"] == W.MERGE_FROM and month >= W.MERGE_DAY:
                continue
            n = rng.poisson(pr["women"] * 0.00042)
            for _ in range(n):
                age = int(rng.choice([int(rng.integers(18, 65)), int(rng.integers(65, 96))], p=[0.3, 0.7]))
                band = "65+" if age >= 65 else ("45-64" if age >= 45 else "18-44")
                rows.append([month.strftime("%Y-%m"), pr["code"], "F" if rng.random() < 0.61 else "M", band,
                             "COCA" if rng.random() < 0.58 else "COIA"])
        month = dt.date(month.year + (month.month == 12), month.month % 12 + 1, 1)
    return rows


def icb_workbook(path):
    """The ICB's quarterly prescribing indicators for 2025-26 by practice (all antibacterials, every indication)."""
    rng = W.rng_for("icb")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Practice indicators"
    ws.append(["Hollinbrook ICB antimicrobial prescribing indicators, 2025-26, by practice and quarter. Source: ePACT2 "
               "dispensed items; STAR-PU weighted list. Medicines Optimisation team, published 14/05/2026."])
    ws.append([])
    hdr = ["Practice code", "Quarter", "Antibacterial items per STAR-PU (12 months to quarter end)",
           "Co-amoxiclav, cephalosporin and quinolone items (% of antibacterial items)",
           "Nitrofurantoin items", "Trimethoprim items"]
    ws.append(hdr)
    for pr in W.practices():
        base = float(rng.uniform(0.72, 0.98))
        broad = float(rng.uniform(6.8, 10.9))
        for q in ("2025-26 Q1", "2025-26 Q2", "2025-26 Q3", "2025-26 Q4"):
            nit = int(pr["women"] * float(rng.uniform(0.024, 0.034)))
            tmp = int(pr["women"] * float(rng.uniform(0.006, 0.019)))
            ws.append([pr["code"], q, round(base * float(rng.lognormal(0, 0.03)), 3),
                       round(broad * float(rng.lognormal(0, 0.05)), 1), nit, tmp])
    for c, w in zip("ABCDEF", (14, 12, 30, 34, 16, 16)):
        ws.column_dimensions[c].width = w
    for c in range(1, 7):
        ws.cell(row=3, column=c).font = Font(bold=True)
        ws.cell(row=3, column=c).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)


def write_all(out, x):
    import os
    f = lambda k: os.path.join(out, FILES[k])
    n = {}
    n["cultures"] = write_csv(f("cultures"), LAB_COLS, culture_rows(x["specimens"]))
    n["issues"] = write_csv(f("issues"), ISSUE_COLS, issue_rows(x["issues"]), lineterminator="\n")
    register_workbook(f("register"))
    codelist_workbook(f("codelists"))
    n["organisms"] = write_csv(f("organisms"), ["OrganismCode", "OrganismName"], ORGANISM_TABLE)
    n["antimicrobials"] = write_csv(f("antimicrobials"), ["AntimicrobialCode", "Antimicrobial"], ANTIMICROBIAL_TABLE)
    icb_workbook(f("icb"))
    n["cdiff"] = write_csv(f("cdiff"), ["Month", "PracticeCode", "Sex", "AgeBand", "OnsetCategory"], cdiff_rows())
    n["lists"] = write_csv(f("lists"), ["PUBLICATION", "EXTRACT_DATE", "TYPE", "SUB_ICB_LOCATION_CODE", "ORG_CODE",
                                        "SEX", "AGE_GROUP_5", "NUMBER_OF_PATIENTS"], list_rows())
    return n
