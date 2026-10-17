"""The independent verifier: recompute the call, the conformed file and the grade 7 figures from target/ alone, with its
own reading of the files and its own equipercentile and linear linking (no generator module), and compare them with the
goldens.

    python3 task464/generator/verify.py
"""
import csv
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def read(target, name):
    with open(os.path.join(target, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def equipercentile_k(old, new, cut):
    """Highest retiring score whose equipercentile equivalent (mid-percentile ranks, uniform kernel) is below cut - 0.5;
    and the same by linear linking."""
    vo = np.arange(150, 451)
    fo = np.array([np.sum(old == v) for v in vo], float) / len(old)
    Fo = np.cumsum(fo)
    pr = Fo - fo / 2
    vn = np.arange(2100, 2901)
    fn = np.array([np.sum(new == v) for v in vn], float) / len(new)
    Fn = np.cumsum(fn)
    eq = np.interp(pr, np.concatenate([[0.0], Fn]), np.concatenate([[2099.5], vn + 0.5]))
    present = np.array([np.any(old == v) for v in vo])
    k_eq = int(vo[(eq < cut - 0.5) & present].max())
    lin = new.mean() + (vo - old.mean()) * new.std() / old.std()
    k_lin = int(vo[(lin < cut - 0.5) & present].max())
    return k_eq, k_lin


def main(target, golden):
    files = sorted(os.listdir(target))
    rules = pdf_text(os.path.join(target, "alp_2027_grant_rules.pdf"))
    att = rules.split("Attachment A")[-1]
    applicants = sorted(set(re.findall(r"\b(1\d{3})\b", att)))
    res = pdf_text(os.path.join(target, "sbe_resolution_2026_22_slm_cut_scores.pdf"))
    g7cut = int(re.search(r"\b7 (\d{4}) \d{4} \d{4}", res.split("Attachment A")[-1]).group(1))
    summ = pdf_text(os.path.join(target, "slm_2026_grade8_technical_summary.pdf"))
    cuts = [int(v) for v in re.search(r"Level 2 begins at (\d{4}), Level 3 at (\d{4}) and Level 4 at (\d{4})",
                                      summ).groups()]
    roll = {}
    for r in read(target, "enrollment_october_2026_grades_9_12.csv"):
        if r["grade"] in ("9", "10") and r["district_code"] in applicants and r["entry_date"] <= "2026-10-01" and \
                (r["exit_date"] == "" or r["exit_date"] >= "2026-10-01"):
            roll[r["state_student_id"]] = (r["district_code"], int(r["grade"]))
    xw = {r["TEST_TAKER_ID"]: r["STATE_STUDENT_ID"] for r in read(target, "calderwood_examinee_id_crosswalk_2025.csv")}
    latest = {}
    for r in read(target, "glra_2025_student_results.csv"):
        if r["GRADE"] == "8" and r["SCORE_STATUS"] == "SCR":
            sid = r["STATE_STUDENT_ID"] or xw[r["TEST_TAKER_ID"]]
            if sid not in latest:
                latest[sid] = ("GLRA", int(r["SCALE_SCORE"]))
    for r in read(target, "slm_2026_student_results.csv"):
        if r["grade"] == "8" and r["status"] == "Scored":
            latest[r["state_student_id"]] = ("SLM", int(r["scale_score"]))
    br = read(target, "glra_slm_bridge_study_2026.csv")
    old = np.array([int(r["glra_scale_score"]) for r in br])
    new = np.array([int(r["slm_scale_score"]) for r in br])
    ks = []
    for c in cuts:
        k_eq, k_lin = equipercentile_k(old, new, c)
        assert k_eq == k_lin, (c, k_eq, k_lin)
        ks.append(k_eq)

    def level(test, sc):
        return 1 + sum(sc >= c for c in cuts) if test == "SLM" else 1 + sum(sc > k for k in ks)
    counts = {d: 0 for d in applicants}
    lev = {}
    for sid, (d, g) in roll.items():
        if sid in latest:
            lev[sid] = level(*latest[sid])
            counts[d] += lev[sid] == 1
    order = sorted(applicants, key=lambda d: (-counts[d], d))
    funded, first = order[:6], order[6]
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(golden, "alp_grants_2027.xlsx"), data_only=True)
    grows = {r[0]: r for r in wb["Applicants"].iter_rows(min_row=5, values_only=True) if r[0]}
    funded_g = [r[1] for r in wb["Grants 2027"].iter_rows(min_row=5, max_row=10, values_only=True)]
    ok = [("the six funded", sorted(funded) == sorted(funded_g)),
          ("every applicant's students at Level 1", all(grows[d][4] == counts[d] for d in applicants)),
          ("the first left out and the gap", grows[first][5] == "No" and
           counts[funded[-1]] - counts[first] == next(r[5] for r in wb["Grants 2027"].iter_rows(min_row=1, values_only=True)
                                                      if r[0] and str(r[0]).startswith("Gap")))]
    sch = {str(r[0]): str(r[2]) for r in wb_dir(target)}
    g7 = {d: [0, 0] for d in applicants}
    for r in read(target, "slm_2026_student_results.csv"):
        if r["grade"] == "7" and r["status"] == "Scored" and sch.get(r["school_code"]) in g7:
            d = sch[r["school_code"]]
            g7[d][1] += 1
            g7[d][0] += int(r["scale_score"]) < g7cut
    ok.append(("each applicant's grade 7 students at Level 1 and their share",
               all(grows[d][7] == g7[d][0] and grows[d][8] == round(100.0 * g7[d][0] / g7[d][1], 1) for d in applicants)))
    with open(os.path.join(golden, "alp_conformed_grade8_reading_2026.csv"), encoding="utf-8") as fh:
        conf = {r["state_student_id"]: int(r["slm_level"]) for r in csv.DictReader(fh)}
    ok.append(("the conformed file: one row per counted student, each level", conf == lev))
    for label, good in ok:
        print("%s  verify: %s" % ("PASS" if good else "FAIL", label))
    print("verify: %d files read; boundaries %s; funded %s" % (len(files), ks, ", ".join(funded)))
    if not all(g for _, g in ok):
        raise SystemExit("verify failed")


def wb_dir(target):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, "district_directory_2026.xlsx"), read_only=True)
    return [r for r in wb["Schools"].iter_rows(min_row=5, values_only=True) if r[0]]


if __name__ == "__main__":
    main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
