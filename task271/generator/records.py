"""The pack's data files, written from the world and the system's records: the register's pedigree export, the
genetic test results, the variant register, the tumor registry's incidence and abstracts, the surgical extract, the
breast MRI exams, the EMPI identifiers and merge log, the death linkage, and two files the analysis does not need."""
import csv
import datetime as dt
import math

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import common as K
import core as C
import clinical as CL
import world as W

ROLE_ORDER = ["PROBAND", "MOTHER", "FATHER", "SISTER", "BROTHER", "HALF_SISTER_MAT", "HALF_SISTER_PAT",
              "HALF_BROTHER_MAT", "HALF_BROTHER_PAT", "DAUGHTER", "SON", "PARTNER", "MAT_GRANDMOTHER",
              "MAT_GRANDFATHER", "MAT_AUNT", "MAT_UNCLE", "PAT_GRANDMOTHER", "PAT_GRANDFATHER", "PAT_AUNT",
              "PAT_UNCLE", "NIECE", "NEPHEW", "GRANDDAUGHTER", "GRANDSON"]
SECOND = {"MAT_GRANDMOTHER", "MAT_GRANDFATHER", "PAT_GRANDMOTHER", "PAT_GRANDFATHER", "MAT_AUNT", "MAT_UNCLE",
          "PAT_AUNT", "PAT_UNCLE"}


def _w(path, header, rows, delimiter=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, delimiter=delimiter, lineterminator="\r\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)
    return len(rows)


def iso(d):
    return d.isoformat() if d else ""


# ---------------------------------------------------------------------------------------------- the pedigree
def pedigree_rows(w, rec, seed):
    rng = np.random.default_rng([seed, 11])
    rows = []
    for i, f in enumerate(w["families"]):
        hist = W.ydate(f["history"])
        lid_pid = {p["lid"]: rec["pid"][(i, p["lid"])] for p in f["persons"]}
        for p in f["persons"]:
            key = (i, p["lid"])
            pat = rec["pat"].get(key)
            alive = p["alive_at_hist"]
            age = int(np.floor(p["last_age"]))
            unknown = p["role"] in SECOND and not pat and rng.random() < 0.06
            by = "" if (p["role"] in SECOND and not pat and rng.random() < 0.05) else str(int(np.floor(p["birth"])))
            cancers = []
            if np.isfinite(p["breast"]) and p["breast"] <= p["last_age"]:
                cancers.append(("Breast", p["breast"]))
            for site, a in p["other"]:
                if a <= p["last_age"]:
                    cancers.append((site, a))
            if p["role"] == "PROBAND" and rng.random() < 0.05:
                a2 = p["breast"] + rng.uniform(1.5, 8)
                if a2 <= p["last_age"]:
                    cancers.append(("Breast", a2))
            cancers.sort(key=lambda x: x[1])
            cancers = cancers[:3]
            exact = bool(pat) or p["degree"] == "proband"
            cells = []
            for site, a in cancers:
                aa = "" if (p["role"] in SECOND and not exact and rng.random() < 0.12) else str(int(np.floor(a)))
                cells += [site, aa]
            cells += [""] * (6 - len(cells))
            rows.append([
                rec["fid"][i], lid_pid[p["lid"]], p["role"], p["sex"],
                lid_pid.get(p["mother"], "") if p["mother"] is not None else "",
                lid_pid.get(p["father"], "") if p["father"] is not None else "",
                by, iso(pat["dob"]) if pat else "", pat["eid"] if pat else "",
                "Unknown" if unknown else ("Living" if alive else "Deceased"), "" if unknown else str(age),
                iso(hist), f["code"]] + cells + ["Exact" if exact else ("Approximate" if cancers else "")])
    rows.sort(key=lambda r: (r[0], ROLE_ORDER.index(r[2]), r[6] or "9999", r[1]))
    return rows


PEDIGREE_HEADER = ["family_id", "person_id", "relationship", "sex", "mother_id", "father_id", "birth_year",
                   "birth_date", "enterprise_id", "vital_status", "age", "history_date", "family_variant_group",
                   "cancer_1", "cancer_1_age", "cancer_2", "cancer_2_age", "cancer_3", "cancer_3_age",
                   "ages_reported"]


def write_pedigree(path, w, rec, seed):
    return _w(path, PEDIGREE_HEADER, pedigree_rows(w, rec, seed))


# ------------------------------------------------------------------------------------- genetic test results
CLASS_OF = {"protein-truncating": "Pathogenic", "missense": "Likely pathogenic"}


def lab_rows(w, rec, seed):
    rng = np.random.default_rng([seed, 12])
    switch = W.yfrac(K.LAB_SWITCH)
    panel23 = W.yfrac(K.PANEL_2023)
    rows = []
    tmp = [0]

    for i, f in enumerate(w["families"]):
        code = f["code"]
        var = w["variants"][code][f["variant"]]
        late = K.LATE[code]
        for p in f["persons"]:
            if not np.isfinite(p["test"]):
                continue
            key = (i, p["lid"])
            pat = rec["pat"][key]
            coll = p["test"]
            ref = coll < switch
            lab = K.REFLAB if ref else K.LAB
            rep = min(coll + rng.uniform(0.03, 0.08), W.EXPORT_Y - 1 / 365)
            car = bool(p["car"])
            base = [rec["pid"][key], pat["eid"], rec["fid"][i]]

            def line(rtype, sup, coll_y, rep_y, labname, test, gene, cls, result, refstyle):
                vc = var["c"] if gene and not refstyle else ""
                vp = var["p"] if gene and not refstyle else ""
                lg = var["legacy"] if gene and refstyle else ""
                tx = var["transcript"] if gene else ""
                cd = W.workday(W.ydate(coll_y))
                rd = max(W.workday(W.ydate(rep_y)), cd + dt.timedelta(days=5))
                rd = min(rd, K.EXPORT)
                tmp[0] += 1
                rows.append([tmp[0], labname, iso(cd), iso(rd), rtype, sup] + base +
                            [test, gene, tx, vc, vp, lg, cls, result])
                return tmp[0]

            if p["test_kind"] == "familial":
                res = ("Positive" if car else "Negative") if ref else ("Detected" if car else "Not detected")
                line("Original", "", coll, rep, lab, "Familial variant analysis", var["gene"],
                     CLASS_OF[K.KIND[code]] if car else "", res, ref)
                continue
            test = "Hereditary breast cancer panel" if coll < panel23 else "Hereditary breast cancer panel (v2)"
            if late == "panel 2023" and coll < panel23:
                first = line("Original", "", coll, rep, lab, test, "", "", "No reportable variants", ref)
                y = max(f["ident"], coll + 0.1) + rng.uniform(0.0, 0.1)
                line("Reanalysis", first, coll, y, K.LAB, test, var["gene"],
                     CLASS_OF[K.KIND[code]] if car else "", "Variant identified" if car else "No reportable variants",
                     False)
                continue
            if late == "reclassified 2024" and coll < W.yfrac(K.RECLASS_2024):
                if car:
                    first = line("Original", "", coll, rep, lab, test, var["gene"], "Uncertain significance",
                                 "Variant identified", ref)
                    y = max(f["ident"], coll + 0.1) + rng.uniform(0.0, 0.08)
                    line("Amended", first, coll, y, K.LAB, test, var["gene"], CLASS_OF[K.KIND[code]],
                         "Variant identified", False)
                else:
                    line("Original", "", coll, rep, lab, test, "", "", "No reportable variants", ref)
                continue
            if car:
                line("Original", "", coll, rep, lab, test, var["gene"], CLASS_OF[K.KIND[code]], "Variant identified",
                     ref)
            else:
                line("Original", "", coll, rep, lab, test, "", "", "No reportable variants", ref)
    # report numbers run with the date reported
    rows.sort(key=lambda r: (r[3], r[2], r[6], r[0]))
    num, n = {}, 700001
    for r in rows:
        n += int(rng.integers(1, 9))
        num[r[0]] = "GT%07d" % n
    for r in rows:
        r[0] = num[r[0]]
        if r[5]:
            r[5] = num[r[5]]
    return rows


LAB_HEADER = ["report_id", "laboratory", "collected", "reported", "report_type", "supersedes", "person_id",
              "enterprise_id", "family_id", "test", "gene", "transcript", "hgvs_c", "hgvs_p", "legacy_name",
              "classification", "result"]


def write_labs(path, w, rec, seed):
    return _w(path, LAB_HEADER, lab_rows(w, rec, seed))


def positives(w):
    """Keys of the people whose final result shows the family's variant."""
    return {(i, p["lid"]) for i, f in enumerate(w["families"]) for p in f["persons"]
            if np.isfinite(p["test"]) and p["car"]}


# ------------------------------------------------------------------------------------------ variant register
def _xl_header(ws, row, cols, widths):
    for j, (h, wd) in enumerate(zip(cols, widths), 1):
        c = ws.cell(row, j, h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="3B4A6B")
        c.alignment = Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(j)].width = wd
    ws.freeze_panes = ws.cell(row + 1, 1)


def write_register(path, w):
    wb = Workbook()
    ws = wb.active
    ws.title = "Groups"
    cols = ["group", "gene", "variant type", "on the system's panel from", "variants on the register", "note"]
    _xl_header(ws, 1, cols, [14, 9, 20, 16, 12, 70])
    for r, code in enumerate(K.CODES, 2):
        late = K.LATE[code]
        since = K.PANEL_2023 if late == "panel 2023" else K.UNIVERSAL_START
        note = {"panel 2023": "Added to the hereditary breast cancer panel (v2) on %s; panels run from January 2016 "
                              "re-analysed for the gene, reports issued from August 2023." % K.PANEL_2023.strftime("%-d %B %Y"),
                "reclassified 2024": "Variants classified pathogenic or likely pathogenic, most of them reclassified "
                                     "from uncertain significance on %s (amended reports)."
                                     % K.RECLASS_2024.strftime("%-d %B %Y"),
                "": ""}[late]
        vals = [code, K.GENE[code], K.KIND[code], since, len(w["variants"][code]), note or None]
        for j, v in enumerate(vals, 1):
            c = ws.cell(r, j, v)
            if isinstance(v, dt.date):
                c.number_format = "yyyy-mm-dd"
    v2 = wb.create_sheet("Variants")
    cols = ["group", "gene", "transcript", "HGVS c.", "HGVS p.", "reference laboratory name (to Feb 2021)",
            "classification", "classified on"]
    _xl_header(v2, 1, cols, [14, 9, 14, 20, 24, 22, 18, 14])
    r = 2
    for code in K.CODES:
        late = K.LATE[code]
        for var in sorted(w["variants"][code], key=lambda v: v["c"]):
            when = K.RECLASS_2024 if late == "reclassified 2024" else (K.PANEL_2023 if late == "panel 2023"
                                                                       else K.UNIVERSAL_START)
            vals = [code, var["gene"], var["transcript"], var["c"], var["p"], var["legacy"], CLASS_OF[K.KIND[code]],
                    when]
            for j, v in enumerate(vals, 1):
                c = v2.cell(r, j, v)
                if isinstance(v, dt.date):
                    c.number_format = "yyyy-mm-dd"
            r += 1
    wb.save(path)
    return r - 2


# --------------------------------------------------------------------------------------- tumor registry
AGE_SHARE = np.array([5.8, 6.0, 6.2, 6.3, 6.4, 6.9, 7.1, 6.9, 6.5, 6.1, 6.2, 6.3, 6.4, 6.1, 5.2, 4.1, 2.9, 1.9,
                      1.0, 0.5])


def incidence_rows(seed):
    rng = np.random.default_rng([seed, 13])
    py = 2.34e7 * AGE_SHARE / AGE_SHARE.sum()
    rows = []
    for b in range(20):
        label = "%02d-%02d" % (5 * b, 5 * b + 4) if b < 17 else ("85+" if b == 17 else None)
        if label is None:
            continue
        pyb = py[b] if b < 17 else py[17:].sum()
        rate = C.POP[b] if b < 17 else C.POP[17]
        cases = int(rng.poisson(pyb * rate))
        rows.append([label, cases, int(round(pyb)), "%.1f" % (cases / pyb * 1e5)])
    return rows


def write_incidence(path, seed):
    return _w(path, ["age_band", "first_primary_breast_cancers", "female_patient_years", "rate_per_100000"],
              incidence_rows(seed))


HIST = [("8500/3", "Infiltrating duct carcinoma"), ("8520/3", "Lobular carcinoma"),
        ("8522/3", "Infiltrating duct and lobular carcinoma"), ("8500/2", "Intraductal carcinoma, noninfiltrating")]


def write_abstracts(path, w, rec, seed):
    rng = np.random.default_rng([seed, 14])
    rows = []
    acc = 2016000100
    for a in sorted(rec["abstracts"], key=lambda a: (a["dx"], rec["pat"][a["key"]]["eid"])):
        acc += int(rng.integers(3, 40))
        insitu = a["behavior"] == "In situ"
        h = HIST[3] if insitu else HIST[0 if rng.random() < 0.75 else (1 if rng.random() < 0.6 else 2)]
        sub = "C50.%d" % int(rng.choice([1, 2, 3, 4, 5, 8, 9], p=[.08, .14, .07, .4, .1, .16, .05]))
        stage = "0" if insitu else str(rng.choice(["I", "IA", "IIA", "IIB", "IIIA", "IIIC", "IV"],
                                                  p=[.05, .37, .24, .14, .1, .05, .05]))
        rows.append([str(acc), rec["pat"][a["key"]]["eid"], a["hosp"], iso(a["dx"]), a["age"], sub, a["lat"],
                     "Invasive" if not insitu else "In situ", h[0], h[1], stage, a["surg"], CL.SURG[a["surg"]],
                     iso(a["surg_date"])])
    return _w(path, ["accession_no", "enterprise_id", "reporting_hospital", "date_of_diagnosis", "age_at_diagnosis",
                     "primary_site", "laterality", "behavior", "histology_code", "histology", "stage_group",
                     "surgery_primary_site_code", "surgery_primary_site", "surgery_date"], rows)


CPT_DESC = {"19301": "MASTECTOMY, PARTIAL (EG, LUMPECTOMY, TYLECTOMY, QUADRANTECTOMY, SEGMENTECTOMY)",
            "19303": "MASTECTOMY, SIMPLE, COMPLETE", "19307": "MASTECTOMY, MODIFIED RADICAL",
            "19120": "EXCISION OF CYST, FIBROADENOMA, OR OTHER BENIGN OR MALIGNANT TUMOR, BREAST",
            "19318": "BREAST REDUCTION"}


def write_procedures(path, w, rec, seed):
    rng = np.random.default_rng([seed, 15])
    rows = []
    case = 5100000
    for q in sorted(rec["procedures"], key=lambda q: (q["date"], rec["pat"][q["key"]]["eid"], q["cpt"], q["mod"])):
        case += int(rng.integers(1, 30))
        pat = rec["pat"][q["key"]]
        rows.append(["OR%d" % case, pat["eid"], pat["hosp"], iso(q["date"]), q["cpt"], q["mod"], CPT_DESC[q["cpt"]]])
    return _w(path, ["surgical_case", "enterprise_id", "hospital", "procedure_date", "cpt_code", "modifier",
                     "description"], rows)


def write_exams(path, w, rec, seed):
    rng = np.random.default_rng([seed, 16])
    rows = []
    acc = 88000000
    removed = {}
    for e in sorted(rec["exams"], key=lambda e: (e["date"], e["hosp"], e["mrn"])):
        acc += int(rng.integers(1, 60))
        key = e["key"]
        if key not in removed:
            removed[key] = CL.removed_both(rec, key)
        one = any(q["key"] == key and q["cpt"] in ("19303", "19307") for q in rec["procedures"]) or \
            any(a["key"] == key and a["surg"] in (41, 51) for a in rec["abstracts"])
        proc = ("77048", "MRI BREAST UNILATERAL W WO CONTRAST") if one else ("77049", "MRI BREAST BILATERAL W WO CONTRAST")
        ind = "SCREENING - HIGH RISK" if e["reason"] == "Screening" else ("DIAGNOSTIC" if rng.random() < 0.7 else
                                                                         "PROBLEM SOLVING")
        rows.append(["A%d" % acc, e["hosp"], e["mrn"], e["eid"], iso(e["date"]), proc[0], proc[1], ind,
                     e["status"].upper()])
    return _w(path, ["accession", "hospital", "mrn", "enterprise_id", "exam_date", "cpt_code", "procedure",
                     "indication", "status"], rows)


def write_empi(path, w, rec, seed):
    rng = np.random.default_rng([seed, 17])
    rows = []
    for key in sorted(rec["pat"]):
        pat = rec["pat"][key]
        p_first = None
        for k, (h, m) in enumerate(pat["mrns"]):
            reg = W.ydate(max(1995.0, W.yfrac(pat["dob"]) + 18) + rng.uniform(0, 20)) if k == 0 else \
                W.ydate(rng.uniform(2016.0, 2026.0))
            reg = min(reg, K.EXPORT)
            rows.append([h, m, pat["eid"], iso(reg), pat["dob"].isoformat()])
    rows.sort(key=lambda r: (r[0], r[1]))
    return _w(path, ["hospital", "mrn", "enterprise_id", "registered", "birth_date"], rows)


def write_merges(path, w, rec, seed):
    rows = [[m["retired"], m["surviving"], iso(m["date"]), "Duplicate registration"] for m in rec["merges"]]
    return _w(path, ["retired_enterprise_id", "surviving_enterprise_id", "merge_date", "reason"], rows)


def write_deaths(path, w, rec, seed):
    rows = sorted([[rec["pat"][d["key"]]["eid"], iso(d["date"]), d["source"]] for d in rec["deaths"]],
                  key=lambda r: (r[1], r[0]))
    return _w(path, ["enterprise_id", "date_of_death", "source"], rows)


# ---------------------------------------------------------------------------------------------- distractors
def write_capacity(path, seed):
    rng = np.random.default_rng([seed, 18])
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 plan"
    cols = ["hospital", "city", "state", "breast MRI scanners", "breast MRI slots per week (2026)",
            "screening studies 2025-26", "slots per week planned for 2027"]
    _xl_header(ws, 1, cols, [10, 18, 7, 12, 16, 16, 18])
    for r, (code, city, st) in enumerate(K.HOSPITALS, 2):
        sc = 1 if rng.random() < 0.7 else 2
        slots = int(sc * rng.integers(18, 30))
        vals = [code, city, st, sc, slots, int(slots * 52 * rng.uniform(0.35, 0.6)), slots + int(rng.integers(0, 8))]
        for j, v in enumerate(vals, 1):
            ws.cell(r, j, v)
    wb.save(path)
    return len(K.HOSPITALS)


def write_prs(path, w, rec, seed):
    rng = np.random.default_rng([seed, 19])
    rows = []
    for i, f in enumerate(w["families"]):
        for p in f["persons"]:
            key = (i, p["lid"])
            if p["sex"] != "F" or not (np.isfinite(p["test"]) and p["car"]) or not p["alive_at_hist"]:
                continue
            if rng.random() < 0.17:
                d = W.workday(W.ydate(rng.uniform(2025.1, 2025.9)))
                z = float(rng.normal(0, 1))
                pct = int(np.clip(round(100 * 0.5 * (1 + math.erf(z / math.sqrt(2)))), 1, 99))
                rows.append([rec["pid"][key], rec["pat"][key]["eid"], f["code"], iso(d), "PRS313", pct, "%.2f" % z])
    rows.sort(key=lambda r: (r[3], r[0]))
    return _w(path, ["person_id", "enterprise_id", "family_variant_group", "reported", "score", "percentile",
                     "standardized_score"], rows)
