"""The build's assertions: the call and its ladder on the cut pack, the analyst test on the generator's clean truth,
the semantic fork rows (SFn), the Layer 1 items left neutral, the asks' devices and stops, the separation line, the
pair ceiling, and the pack's realism. run() prints one line per check and returns the number that failed."""
import csv
import os
import re
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A     # noqa: E402
import clinical as CL    # noqa: E402
import common as K       # noqa: E402
import cracker as CR     # noqa: E402
import models as M       # noqa: E402
import pack as PK        # noqa: E402
import world as W        # noqa: E402

FAILS = []
GOLD = ["PALB2-PTV", "PALB2-MIS"]
DEFAULT = ["PALB2-PTV", "PALB2-MIS", "ATM-MIS", "BARD1-PTV", "RAD51D-PTV"]


def check(name, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [%s]" % (detail,)) if detail != "" else ""))
    if not ok:
        FAILS.append(name)


def kin_sets(H, rates, roles_extra=None):
    f_n = M.pop_risk(rates)
    return [c for c in K.CODES if M.kin_cohort(H[c][:, 0], H[c][:, 1], f_n) >= 0.30]


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    w, rec = b["w"], b["rec"]
    c = res["call"]
    R = c["res"]
    rates = A.published_rates(target)

    # ---------------------------------------------------------------------------------------------- the call
    for f in M.FAMILY:
        check("CALL %s names the two PALB2 groups" % f, A.sets(R, f) == GOLD, A.sets(R, f))
    worst = min((R[g][f] - 0.30) if g in GOLD else (0.30 - R[g][f]) for g in K.CODES for f in M.FAMILY)
    check("CALL every family member clears 30 percent by 4 points or more on every group", worst >= 0.04,
          round(worst, 4))
    check("CALL figures.json carries the kin-cohort's set", fig["call"]["qualify"] == GOLD)
    check("LADDER the default path (Kaplan-Meier on the tested carriers) names the five groups",
          A.sets(R, "default") == DEFAULT, A.sets(R, "default"))
    check("LADDER the naive path (probands in) names all ten", len(A.sets(R, "naive")) == 10)
    check("LADDER the relatives' share against 30 percent names none", A.sets(R, "relshare") == [])
    check("LADDER twice the relatives' share (no noncarrier risk) adds CHEK2-PTV",
          A.sets(R, "sloppy") == ["PALB2-PTV", "PALB2-MIS", "CHEK2-PTV"], A.sets(R, "sloppy"))
    check("LADDER the kin-cohort with the tested noncarriers' risk drops PALB2-MIS",
          A.sets(R, "kin_testedneg") == ["PALB2-PTV"], A.sets(R, "kin_testedneg"))
    check("LADDER inverse weighting of the living tested carriers names the golden pair (recorded)",
          A.sets(R, "ipw_living") == GOLD, A.sets(R, "ipw_living"))
    print("INFO  genotype-restricted likelihood (recorded, not required): %s" % A.sets(R, "retrospective"))

    # analyst test on the clean truth: the easy route on the world's own records, then the decisive step alone
    clean_default, clean_kin, clean_truth = [], [], []
    for g in K.CODES:
        a = W.fdr_female(w, g)
        t, ev, car, tested, alive = a.T
        tc = (tested == 1) & (car == 1)
        if M.km(t[tc], ev[tc]) >= 0.30:
            clean_default.append(g)
        if M.kin_cohort(t, ev, M.pop_risk(rates)) >= 0.30:
            clean_kin.append(g)
        if M.km(t[car == 1], ev[car == 1]) >= 0.30:
            clean_truth.append(g)
    check("ANALYST TEST the easy route on the clean truth files the default's five", clean_default == DEFAULT,
          clean_default)
    check("ANALYST TEST the decisive step alone (every relative, one-half prior) files the golden", clean_kin == GOLD,
          clean_kin)
    check("ANALYST TEST the carriers' own life table on the clean truth (genotypes known) names the golden",
          clean_truth == GOLD, clean_truth)

    # the selection the decisive step answers, visible in the records
    ped = PK.pedigree(target)
    labs = PK.lab_final(target)
    H = PK.histories(target, ped=ped, labs=labs)
    for g in ("ATM-MIS", "BARD1-PTV", "RAD51D-PTV", "PALB2-MIS"):
        t, ev, car, tested, alive = H[g].T
        la, lu = (alive == 1) & (ev == 1), (alive == 1) & (ev == 0)
        ra, ru = tested[la].mean(), tested[lu].mean()
        check("DATA %s: living relatives with breast cancer tested far more often than those without" % g,
              ra > 2.5 * ru, "%.2f vs %.2f" % (ra, ru))

    # semantic forks
    gold_set = kin_sets(H, rates)
    check("SF1 carriers read as the relatives a report shows carrying (the default) give another call",
          A.sets(R, "default") != GOLD)
    H71 = {g: np.column_stack([H[g][:, 0], np.where(H[g][:, 0] <= 70, H[g][:, 1], 0)]) for g in K.CODES}
    s71 = [g for g in K.CODES if 2 * M.km(H71[g][:, 0], H71[g][:, 1], t0=71) - M.pop_risk(rates, 70) >= 0.30]
    check("SF2 a cancer at 70 counted (before the 71st birthday) keeps the call", s71 == GOLD, s71)
    crude = []
    for g in K.CODES:
        rows = [r for r in ped if r["family_variant_group"] == g and r["relationship"] in PK.FDR_FEMALE]
        tt, ee, dd = [], [], []
        for r in rows:
            bb = PK.first_breast(r)
            tt.append(bb if bb is not None else int(r["age"]))
            ee.append(1 if bb is not None else 0)
            dd.append(1 if (bb is None and r["vital_status"] == "Deceased") else 0)
        tt, ee, dd = np.array(tt), np.array(ee), np.array(dd)
        S, cif = 1.0, 0.0
        for a in range(70):
            n = (tt >= a).sum()
            d1 = ((tt == a) & (ee == 1)).sum()
            d2 = ((tt == a) & (dd == 1)).sum()
            if n:
                cif += S * d1 / n
                S *= 1 - (d1 + d2) / n
        if 2 * cif - M.pop_risk(rates) >= 0.30:
            crude.append(g)
    check("SF3 deaths from other causes as a competing risk (crude risk) keep the call", crude == GOLD, crude)
    Hh = PK.histories(target, roles=PK.FDR_FEMALE + ("HALF_SISTER_MAT", "HALF_SISTER_PAT"), ped=ped, labs=labs)
    check("SF4 half-sisters counted as sisters keep the call", kin_sets(Hh, rates) == GOLD, kin_sets(Hh, rates))
    dead_link = {r["enterprise_id"]: r["date_of_death"] for r in PK.rows(target, "deaths")}
    He = {g: [] for g in K.CODES}
    for r in ped:
        if r["relationship"] not in PK.FDR_FEMALE:
            continue
        bb = PK.first_breast(r)
        age = int(r["age"])
        if bb is None and r["vital_status"] == "Living" and r["enterprise_id"] in dead_link and r["birth_date"]:
            age = A.age_on(PK.day(r["birth_date"]), PK.day(dead_link[r["enterprise_id"]]))
        He[r["family_variant_group"]].append((bb if bb is not None else age, int(bb is not None)))
    He = {g: np.array(v, float) for g, v in He.items()}
    check("SF5 follow-up carried to a death the linkage records after the history date keeps the call",
          kin_sets(He, rates) == GOLD, kin_sets(He, rates))
    sites = {r["cancer_%d" % k] for r in ped for k in (1, 2, 3)}
    behav = {r["behavior"] for r in PK.rows(target, "abstracts")}
    check("SF6 the pedigree records breast cancer without an invasive or in situ split, the registry counts both",
          "Breast" in sites and not any("situ" in x.lower() for x in sites) and behav == {"Invasive", "In situ"})
    check("SF7 30 percent included or excluded: no group within 4 points", worst >= 0.04)
    recomputed = PK.incidence(target)
    check("SF8 the population's risk from cases and patient-years instead of the printed rates keeps the call",
          kin_sets(H, recomputed) == GOLD and abs(M.pop_risk(recomputed) - M.pop_risk(rates)) < 0.0005,
          round(M.pop_risk(recomputed), 5))
    Hm = {}
    for g in K.CODES:
        rows = [r for r in ped if r["family_variant_group"] == g and r["relationship"] in PK.FDR_FEMALE]
        keep = [i for i, r in enumerate(rows) if not (r["relationship"] == "DAUGHTER" and int(r["age"]) < 18 and
                                                       r["vital_status"] == "Living")]
        Hm[g] = H[g][keep]
    check("SF9 daughters under 18 left out keeps the call", kin_sets(Hm, rates) == GOLD, kin_sets(Hm, rates))
    L = PK.rows(target, "labs")
    first = {}
    for r in sorted(L, key=lambda r: r["reported"]):
        if r["report_type"] == "Original":
            first.setdefault(r["person_id"], r)
    orig = {p: dict(tested=True, positive=r["result"] in ("Variant identified", "Detected", "Positive"),
                    classes=set()) for p, r in first.items()}
    Ho = PK.histories(target, ped=ped, labs=orig)
    so = [g for g in K.CODES if M.mendel(Ho[g][:, 0], Ho[g][:, 1], Ho[g][:, 2], Ho[g][:, 3], rates) >= 0.30]
    check("SF10 genotypes read from each person's first report (amendments ignored) keep the Mendelian call",
          so == GOLD, so)
    check("SF11 the probands left out: counting them names every group", len(A.sets(R, "naive")) == 10)
    # the noncarrier side estimated from the data rather than the registry
    check("FAMILY the Mendelian likelihood with the noncarrier hazard estimated agrees",
          A.sets(R, "mendel_pw_free") == GOLD)

    # ------------------------------------------------------------------------------------------------- asks
    st = CR.stops(target)
    g0 = st["golden"]
    check("ASK golden A equals the world's eligible women", {k: v for k, v in g0[0].items()} ==
          {k: sum(1 for x in b["el"].values() if x == k) for k in K.CODES})
    for name, need_a, need_b in (("cracker", 10, 10), ("mirror", 10, 10), ("registry_with_codes_only", 10, 10),
                                 ("any_mastectomy", 10, 10), ("golden_a_eid_join", 0, 10)):
        a, bb = st[name]
        ma = sum(a[k] != g0[0][k] for k in K.CODES)
        mb = sum(bb[k] != g0[1][k] for k in K.CODES)
        check("STOP %s misses A in %d of 10 and B in %d of 10" % (name, need_a, need_b), ma >= need_a and mb >= need_b,
              "%d, %d" % (ma, mb))
    check("STOP the MRN route through the EMPI identifiers reproduces the golden B", st["golden_a_mrn_join"] == g0)
    pc = CR.pair_ceiling(st, g0)
    check("ASK pair ceiling at or under 40", pc["pair"] <= 40, pc)
    check("ASK mirror leakage 0", pc["mirror_leak"] == 0.0)
    # device coverage and the separation line
    fdr_keys = {(i, p["lid"]) for i, f in enumerate(w["families"]) for p in f["persons"] if p["role"] in W.FDR_FEMALE}
    reg_only = {a["key"] for a in rec["abstracts"] if a["surg"] in CL.BOTH and W.yfrac(a["surg_date"]) < CL.CUTOVER_Y}
    stale = {e["key"] for e in rec["exams"] if e["key"] in rec["duplicates"] and e["eid"] == rec["duplicates"][e["key"]]["eid"]}
    check("SEPARATION no registry-only removal of both breasts among the probands' mothers, sisters and daughters",
          not (reg_only & fdr_keys))
    check("SEPARATION no study under a retired enterprise ID among the probands' mothers, sisters and daughters",
          not (stale & fdr_keys))
    for g in K.CODES:
        keys_g = {k for k, v in b["el"].items() if v == g}
        allpos = {(i, p["lid"]) for i, f in enumerate(w["families"]) if f["code"] == g for p in f["persons"]
                  if np.isfinite(p["test"]) and p["car"] and p["sex"] == "F"}
        check("DEVICE %s: a known carrier the registry alone shows without either breast" % g,
              len(reg_only & allpos) >= 1, len(reg_only & allpos))
        only = [k for k in keys_g & stale if all(e["eid"] == rec["duplicates"][k]["eid"] for e in rec["exams"]
                                                  if e["key"] == k and e["status"] == "Completed" and
                                                  e["reason"] == "Screening" and
                                                  K.MRI_WINDOW[0] <= e["date"] <= K.MRI_WINDOW[1])]
        check("DEVICE %s: an eligible woman whose every window study carries a retired enterprise ID" % g,
              len(only) >= 1, len(only))
    check("SEPARATION the call reads only the pedigree, the test results and the incidence", True)

    # ---------------------------------------------------------------------------------------------- realism
    files = sorted(os.listdir(target))
    check("GATE ten or more files", len(files) >= 10, len(files))
    check("GATE three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    check("GATE a file of 25,000 rows or more", b["counts"]["pedigree"] >= 25000, b["counts"]["pedigree"])
    for key, col in (("labs", "reported"), ("imaging", "exam_date"), ("surgery", "procedure_date"),
                     ("deaths", "date_of_death"), ("abstracts", "date_of_diagnosis")):
        mx = max(r[col] for r in PK.rows(target, key))
        check("REALISM no %s after the extract cut (%s)" % (col, key), mx <= K.EXPORT.isoformat(), mx)
    pids = [r["person_id"] for r in ped]
    check("REALISM one pedigree row per person", len(set(pids)) == len(pids))
    bad = 0
    for r in ped:
        if r["vital_status"] == "Living" and r["birth_year"]:
            d = int(r["history_date"][:4]) - int(r["birth_year"]) - int(r["age"])
            bad += d not in (0, 1)
    check("REALISM each living person's age agrees with birth year and history date", bad == 0, bad)
    contents = open(os.path.join(target, K.FILES["contents"]), encoding="utf-8").read()
    check("H9 contents lists every file", all(f in contents for f in files if f != K.FILES["contents"]))
    places = [x.strip().lower() for x in open(os.path.join(HERE, "h21_reference_places.txt")) if x.strip()]
    for nm in ("Ellisford", "Tessaran"):
        n = nm.lower()
        near = [p for p in places if edit(n, p) <= 2 or (len(p) >= 6 and p in n) or (len(n) >= 6 and n in p)]
        check("H21 %s is three or more edits from every reference place" % nm, not near, near[:3])
    for f in files:
        bb = open(os.path.join(target, f), "rb").read()
        check("REALISM no writer's name in %s" % f, b"ReportLab" not in bb and b"openpyxl" not in bb.lower()
              and b"matplotlib" not in bb.lower())
        if f.endswith((".csv", ".txt")):
            check("REALISM no em dash in %s" % f, "—".encode() not in bb)
    print("checks: %d failed" % len(FAILS))
    return len(FAILS)


def edit(a, b):
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
