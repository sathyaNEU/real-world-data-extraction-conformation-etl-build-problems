"""task402 generator checks: the clean truth (world + harness), the cut pack (target/) and the goldens.

    python3 task402/generator/checks.py
"""
import json
import os
import re
import sys
import zipfile
from collections import Counter
from datetime import date

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
import harness as H  # noqa: E402
import verify as V  # noqa: E402
import world as W  # noqa: E402

RES = []


def check(label, ok, detail=""):
    RES.append((label, bool(ok), detail))


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    w = W.simulate()
    m = H.measure(w)
    r = H.price(m, w)
    refs, users, c, bk = V.load(T)
    res, mm, cover = V.main_call(refs, users, c, bk, f)
    s3 = m[(m.fy == 25) & (m.step == 3) & (m.n_treat_att >= 1)]
    br = s3[(s3.broken == True) & (s3.broken_kind == "agency")]
    est = {k: r[k] for k in ("A_landmark", "A_landmark_band", "A_pooled", "A_all_handovers", "A_lm_emp", "A_pooled_emp",
                             "A_cover_coarse", "A_cover_coarse_lm")}
    wide = {k: r[k] for k in ("A_agency_unbroken", "A_agency_unbroken_lm", "A_longwait_unbroken",
                              "A_longwait_unbroken_lm", "A_vs_fy24_lm")}
    rivals = {"B": r["B"], "B_vs24": r["B_vs24"], "D": r["D"], "E": r["E"], "C_golden": r["C_golden"],
              "C_left": r["C_left"]}
    plan = "\n".join(p.text for p in __import__("docx").Document(os.path.join(T, "improvement_plan_2026-27.docx")).paragraphs)
    check("control: the plan text was read", "national measure" in plan and len(plan) > 1500)

    # ---- the semantic fork table
    check("SF1 recovery on the national measure is filed in the plan's annex",
          "PHQ-9 total of 10 or more" in plan and "two or more attended treatment appointments" in plan)
    check("SF1 the bundle's national measure equals the clean truth (both years)",
          res["recoveries_2024-25"] == f["recoveries_2024-25"] and res["recoveries_2025-26"] == f["recoveries_2025-26"])
    check("SF2 the year by discharge date on the refreshed extract is filed",
          "by discharge date" in plan and "refreshed extract of 6 May 2026" in plan)
    near = int(((pd.to_datetime(br.end).dt.date - W.FY25[0]).map(lambda x: abs(x.days)) <= 1).sum() +
               ((pd.to_datetime(br.end).dt.date - W.FY25[1]).map(lambda x: abs(x.days)) <= 1).sum())
    check("SF2 no broken course ends within a day of either year boundary", near == 0, str(near))
    check("SF3 the cost clause is filed (would have had, less those they had)",
          "would have had without the change, less the number they had" in plan)
    check("SF4 the comparison is filed as the year's other referrals at the same step",
          "read from the year's other referrals at the same step" in plan)
    bins = {k: int(round(v / 50.0) * 50) for k, v in est.items()}
    check("SF4 every estimator inside the filed comparison grades to the golden's bin",
          set(bins.values()) == {f["a_cost"]}, str({k: round(v, 1) for k, v in est.items()}))
    check("SF4 every such estimator sits at least 7 per cent of a bin from its edge",
          min(edge(v, 50) for v in est.values()) >= 3.5, str(round(min(edge(v, 50) for v in est.values()), 1)))
    check("SF5 the register files an extension as an additional line under the original reference",
          "booked as an additional line under the original booking reference" in
          " ".join(str(x) for x in pd.read_excel(os.path.join(T, "agency_bookings_psychological_therapies_2025-26.xlsx"), header=None, nrows=3)[0]))
    contiguous = all((pd.to_datetime(g["Line start (UTC)"].iloc[1:].values) - pd.to_datetime(g["Line end (UTC)"].iloc[:-1].values)
                      ).total_seconds().min() <= 3600 * 2 for _, g in bk.sort_values(["Booking ref", "Line"]).groupby("Booking ref") if len(g) > 1)
    check("SF5 each booking's lines run on without a gap (an assignment is its booking and extensions)", contiguous)
    # SF6: under the directory map no course spanning the migration changes therapist at the migration
    span = c[c.type == "treatment"].sort_values(["ref", "date", "time"])
    pre = span[span.date < W.MIGRATION].groupby("ref").user.last()
    post = span[span.date >= W.MIGRATION].groupby("ref").user.first()
    both = pre.index.intersection(post.index)
    changed = [x for x in both if pre[x] != post[x]]
    back = {v: k for k, v in __import__("pack").Pack(w).rid.items()}
    tr = w.truth.set_index("ref")
    false_change = [x for x in changed if not bool(tr.at[back[x], "broken"])]
    check("SF6 under the directory map, every course spanning 13 October 2025 that changes practitioner across the "
          "cutover is a true handover", not false_change, "%d changed, %d not handovers" % (len(changed), len(false_change)))
    old = pd.read_csv(os.path.join(T, "care_contacts_2023-10-02_to_2025-10-12.csv"), dtype=str)
    newp = pd.read_parquet(os.path.join(T, "appointments_2025-10-13_to_2026-05-06.parquet"))
    check("SF6 unmapped, legacy codes and user IDs never coincide (every spanning course would read as a handover)",
          not (set(old.TherapistCode) & set(newp.clinician_user_id)))
    check("SF7 the step clause is filed and the HI-therapist rule equals the CareStep field (asserted in verify)",
          "high-intensity therapist" in plan)
    allmin = min(list(est.values()) + list(wide.values()))
    check("SF8 change A's cost exceeds every rival's under every estimator, by at least 2 times",
          allmin >= 2 * max(rivals.values()), "A min %.1f, largest rival %.1f" % (allmin, max(rivals.values())))
    check("SF8 the fund rule is filed (largest cost in recoveries, not per patient)",
          "largest cost in recoveries" in plan and "Cost per patient reached is not used" in plan)

    # ---- the call's construction
    check("every broken course is discharged by an employed therapist", set(br.disch_kind) == {"employed"})
    check("every broken course's counterfactual end falls inside 2025-26", br.cf_end.max() <= W.FY25[1], str(br.cf_end.max()))
    check("the bundle's broken courses equal the clean truth's", res["broken_courses"] == len(br) == f["broken_courses"])
    check("the graded cost of A recomputes from the bundle", res["a_cost"] == f["a_cost"] and res["a_cost_exact"] == f["a_cost_exact"])
    check("A's graded figure sits mid-bin (at least 7 per cent of a bin from its edge)", edge(f["a_cost_exact"], 50) >= 3.5,
          str(round(edge(f["a_cost_exact"], 50), 1)))
    check("the last agency lapse breaks under 60 courses", r["breaks_last_date"][1] < 60, str(r["breaks_last_date"]))
    cells = r["cells"]
    n, k = cells["long_employed"][0], round(cells["long_employed"][0] * cells["long_employed"][2] / 100)
    from scipy.stats import binomtest
    ci = binomtest(int(k), int(n)).proportion_ci(0.95, method="wilson") if n else None
    check("risk 2: the long-wait employed cell is under 15 courses", n < 15, str(cells))
    check("risk 2: its 95 per cent interval covers both the long-wait agency rate and the short-wait rate",
          ci is not None and ci.low <= cells["long_agency"][2] / 100 <= ci.high and ci.low <= cells["short_employed"][2] / 100 <= ci.high,
          "%s %s" % (ci, cells))

    # ---- the three rules, executed on the clean truth
    check("R1 the field's raw material ships: session-by-session scores and every appointment's practitioner",
          {"PHQ9_Q1", "GAD7_Q7"} <= set(pd.read_csv(os.path.join(T, "outcome_measures_items_2023-10-02_to_2025-10-12.csv"), nrows=2).columns)
          and "clinician_user_id" in newp.columns)
    cols = " ".join(old.columns) + " " + " ".join(newp.columns) + " " + " ".join(bk.columns) + " " + " ".join(refs.columns)
    check("R1 no shipped column holds the deciding quantity (no broken, handover, lapse or continuity field)",
          not re.search(r"broken|handover|hand_over|lapse|continu|realloc", cols, re.I))
    check("R2 migration mishandled (codes left unmapped): the call stays A", allmin >= 2 * max(rivals.values()))
    check("R2 booking lines read as separate assignments: no extra course breaks (therapist unchanged at renewals)",
          res["broken_courses"] == f["broken_courses"])
    check("R2 provisional report used for the year: the call stays A (the report prints no change's cost)", True)
    dflt = {"C": r["C_default"], "A": r["A_default"], "B": r["B"], "D": r["D"], "E": r["E"]}
    check("R3a the analyst test: the default path on the clean truth files C", max(dflt, key=dflt.get) == "C", str(dflt))
    coarse = {"C": r["C_default"], "A": r["A_first_kind"], "B": r["B"], "D": r["D"], "E": r["E"]}
    check("R3a the lower rung (A by the first practitioner) still files C beside the wait band with leavers",
          max(coarse, key=coarse.get) == "C" and r["C_default"] / r["A_first_kind"] >= 1.15, str(round(r["C_default"] / r["A_first_kind"], 2)))
    dec = {"A": r["A_landmark"], "C": r["C_golden"], "B": r["B"], "D": r["D"], "E": r["E"]}
    check("R3b the decisive step alone files A", max(dec, key=dec.get) == "A", str({k: round(v, 1) for k, v in dec.items()}))
    check("R3c no plant: no memo, draft or stakeholder figure ranks the changes",
          not any(x in " ".join(os.listdir(T)).lower() for x in ("memo", "draft", "briefing", "note")))

    # ---- careful comparisons agree in direction with the truth
    check("direction: agency therapists' discharged-course rate is not below employed (they are sound)",
          r["A_kpi_rates"][0] >= r["A_kpi_rates"][1] - 3, str(r["A_kpi_rates"]))
    check("direction: the locum's short-wait courses recover like employed short-wait courses",
          abs(cells["short_agency"][2] - cells["short_employed"][2]) <= 5, str(cells))
    check("direction: broken courses recover far below unbroken", br.rec.mean() < 0.6 * s3[s3.broken != True].rec.mean())

    # ---- asks
    for kk, v in f["ask_hours_exact"].items():
        check("ask 3 hours %s mid-bin" % kk, edge(v, 1) >= 0.07, str(round(edge(v, 1), 3)))
    for kk, v in f["ask_cost_exact"].items():
        check("ask 3 cost %s mid-bin" % kk, edge(v, 100) >= 7, str(round(edge(v, 100), 1)))
    check("asks recompute from the bundle (verify)", V.main([T]) == 0)
    # zero device rows in the main call's files: the ask builders write only their own files
    check("zero device rows in the main call's files among step 3 referrals ending in 2025-26",
          set(os.listdir(T)) >= {"agency_timesheets_2025-04_to_2026-03.csv", "steadyway_activity_export_2025-07_to_2026-05.json"}
          and res["broken_courses"] == f["broken_courses"])

    # ---- input gates, realism, containers
    files = sorted(os.listdir(T))
    check("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    check("input gate: 3 or more formats", len({x.rsplit(".", 1)[1] for x in files}) >= 3)
    check("input gate: one file of 25,000 or more rows", len(old) >= 25000, str(len(old)))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("input gate: two or more distractors, named only in metadata.json", len(meta["distractor_files"]) >= 2
          and not any("distract" in x for x in files))
    check("no describing file ships", not any(re.search(r"readme|dictionar|manifest|field.?notes|codebook", x, re.I) for x in files))
    for col, s in (("ContactID", old.ContactID.astype(int)), ("ReferralID", pd.to_numeric(refs.referral_id, errors="coerce").dropna())):
        d = np.diff(np.sort(s.values))
        check("realism: %s is not an arithmetic sequence" % col, len(set(d)) > 1)
    check("realism: job titles take more than two shapes", users["Job title"].nunique() > 2)
    waits = list(f["ask_waiting"].values())
    check("realism: no identical month-end counts", len(set(waits)) == len(waits))
    for fn in ("improvement_plan_2026-27.docx", "clinical_system_users_2026-05-06.xlsx",
               "agency_bookings_psychological_therapies_2025-26.xlsx"):
        z = zipfile.ZipFile(os.path.join(T, fn))
        core = z.read("docProps/core.xml").decode()
        app = z.read("docProps/app.xml").decode()
        check("H1 %s: no library stamp, application named" % fn,
              "python-docx" not in core and "openpyxl" not in core and "Microsoft" in app and "2026-" in core)
    pdf = open(os.path.join(T, "monthly_performance_report_2026-03_provisional.pdf"), "rb").read()
    check("H1 pdf: no library banner, no empty subject or keywords, no trapped flag",
          b"ReportLab" not in pdf and b"/Subject ()" not in pdf and b"/Trapped" not in pdf and b"(unspecified)" not in pdf)
    check("H1 pdf: the font is an embedded TrueType subset, not base-14 Helvetica",
          b"/FontFile2" in pdf and b"Helvetica" not in pdf)
    paras = [p.strip() for p in plan.split("\n") if len(p.strip()) > 30]
    check("no free-text value repeats more than three times (plan)", max(Counter(paras).values()) <= 3)
    for fn in os.listdir(os.path.join(TASK, "golden")):
        if fn.endswith((".docx", ".xlsx", ".pptx")):
            core = zipfile.ZipFile(os.path.join(TASK, "golden", fn)).read("docProps/core.xml").decode()
            check("H1 golden %s scrubbed" % fn, "python-docx" not in core and "openpyxl" not in core)
    sub = open(os.path.join(TASK, "submission.md")).read()
    check("no em dash in the submission", "—" not in sub)

    bad = [x for x in RES if not x[1]]
    for lab, ok, det in RES:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", lab, ("  [" + det + "]") if det and not ok else ""))
    print("%d checks, %d failed" % (len(RES), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
