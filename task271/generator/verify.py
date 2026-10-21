"""Independent verifier: recomputes the call and both planning figures from target/ alone with code that shares
nothing with analysis.py or models.py (pandas joins, a hand-rolled life table, an EM fit of the Mendelian mixture),
and compares them with generator/figures.json."""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))


def life_table_risk(age, event, upto=70):
    """1 - prod(1 - d/n) over completed ages below upto; events counted before censorings at a tied age."""
    df = pd.DataFrame({"age": np.asarray(age, int), "ev": np.asarray(event, int)})
    s = 1.0
    for a in range(upto):
        n = (df["age"] >= a).sum()
        d = ((df["age"] == a) & (df["ev"] == 1)).sum()
        if n:
            s *= 1 - d / n
    return 1 - s


def em_mendel(age, event, genotype, rates, iters=400):
    """EM for the two-component mixture: E-step, each untested woman's posterior chance of carrying (prior one half);
    M-step, carrier hazards by band as weighted events over weighted exposure. Noncarrier hazard = population."""
    age = np.asarray(age, float)
    ev = np.asarray(event, int)
    ev = np.where(age < 70, ev, 0)
    t = np.minimum(age + 0.5, 70.0)
    edges = [0, 40, 50, 60, 70]
    expo = np.stack([np.clip(t - edges[k], 0, edges[k + 1] - edges[k]) for k in range(4)], 1)
    band = np.clip(np.searchsorted(edges, t, side="right") - 1, 0, 3)
    h_pop = np.asarray(rates, float) / 1e5
    full = np.minimum(np.maximum(t[:, None] - np.arange(0, 5 * len(h_pop), 5), 0), 5)
    Hn = (full * h_pop).sum(1)
    hn_ev = h_pop[np.minimum((t // 5).astype(int), len(h_pop) - 1)]
    g = np.asarray(genotype, float)          # 1 carrier, 0 noncarrier, nan untested
    hc = np.full(4, 0.005)
    for _ in range(iters):
        lc = -(expo @ hc) + np.where(ev == 1, np.log(hc[band]), 0.0)
        ln = -Hn + np.where(ev == 1, np.log(np.maximum(hn_ev, 1e-12)), 0.0)
        post = 1 / (1 + np.exp(ln - lc))
        w = np.where(np.isnan(g), post, g)
        new = np.array([(w * ev * (band == k)).sum() / max((w * expo[:, k]).sum(), 1e-12) for k in range(4)])
        new = np.maximum(new, 1e-9)
        if np.max(np.abs(new - hc)) < 1e-10:
            hc = new
            break
        hc = new
    return 1 - np.exp(-(hc * np.diff(edges)).sum())


def run(task):
    target = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    files = {f: os.path.join(target, f) for f in os.listdir(target)}
    find = lambda stem: next(v for k, v in files.items() if k.startswith(stem))
    ped = pd.read_csv(find("icrs_pedigree_export"), dtype=str, keep_default_na=False)
    lab = pd.read_csv(find("icrs_laboratory_reports"), dtype=str, keep_default_na=False)
    inc = pd.read_csv(find("ellisford_tumor_registry_breast_incidence"), dtype=str)
    rates = inc["rate_per_100000"].astype(float).values
    f_n = 1 - np.exp(-(rates[:14] * 5).sum() / 1e5)

    live = lab[~lab["report_id"].isin(set(lab["supersedes"]) - {""})]
    pos = set(live.loc[live["result"].isin(["Variant identified", "Detected", "Positive"]), "person_id"])
    tested = set(live["person_id"])

    def first_breast(r):
        a = [int(r["cancer_%d_age" % k]) for k in (1, 2, 3) if r["cancer_%d" % k] == "Breast" and r["cancer_%d_age" % k]]
        return min(a) if a else None
    fdr = ped[ped["relationship"].isin(["MOTHER", "SISTER", "DAUGHTER"])].copy()
    fb = fdr.apply(first_breast, axis=1)
    fdr["ev"] = fb.notna().astype(int)
    fdr["t"] = np.where(fb.notna(), fb.fillna(0).astype(int), fdr["age"].astype(int))
    fdr["g"] = [np.nan if p not in tested else (1.0 if p in pos else 0.0) for p in fdr["person_id"]]
    bad = 0
    out = {}
    for code, d in fdr.groupby("family_variant_group"):
        kin = 2 * life_table_risk(d["t"], d["ev"]) - f_n
        em = em_mendel(d["t"].values, d["ev"].values, d["g"].values, rates)
        out[code] = (kin, em)
        verdict = "Yes" if kin >= 0.30 else "No"
        ok = verdict == fig["verdict"][code] and (em >= 0.30) == (kin >= 0.30) and \
            abs(kin - fig["risk_kin"][code]) < 5e-4
        bad += not ok
        print("%-11s kin %.4f  EM %.4f  verdict %s  %s" % (code, kin, em, verdict, "ok" if ok else "MISMATCH"))

    # planning figures
    deaths = set(pd.read_csv(find("ellisford_death_linkage"), dtype=str)["enterprise_id"])
    ab = pd.read_csv(find("ellisford_tumor_registry_breast_abstracts"), dtype=str)
    sx = pd.read_csv(find("ellisford_surgical_procedures"), dtype=str, keep_default_na=False)
    mri = pd.read_csv(find("ellisford_breast_mri_exams"), dtype=str)
    empi = pd.read_csv(find("ellisford_empi_identifiers"), dtype=str)
    pos_pp = set(live.loc[live["result"].isin(["Variant identified", "Detected", "Positive"]) &
                          live["classification"].isin(["Pathogenic", "Likely pathogenic"]), "person_id"])
    w = ped[ped["person_id"].isin(pos_pp) & (ped["sex"] == "F") & (ped["enterprise_id"] != "") &
            (ped["vital_status"] == "Living") & ~ped["enterprise_id"].isin(deaths)].copy()
    dob = pd.to_datetime(w["birth_date"])
    age = 2027 - dob.dt.year - ((dob.dt.month > 4) | ((dob.dt.month == 4) & (dob.dt.day > 1))).astype(int)
    w = w[(age >= 30) & (age <= 74)]
    sides = {}
    for _, r in ab.iterrows():
        c = int(r["surgery_primary_site_code"])
        s = sides.setdefault(r["enterprise_id"], set())
        if c in (41, 42, 51, 56):
            s.add("L" if r["laterality"] == "Left" else "R")
        if c in (42, 56):
            s |= {"L", "R"}
    for _, r in sx.iterrows():
        if r["cpt_code"] in ("19303", "19305", "19306", "19307"):
            s = sides.setdefault(r["enterprise_id"], set())
            s |= {"L", "R"} if r["modifier"] == "50" else {r["modifier"][0]}
    w = w[[len(sides.get(e, set())) < 2 for e in w["enterprise_id"]]]
    m = mri[(mri["status"] == "COMPLETED") & (mri["indication"] == "SCREENING - HIGH RISK") &
            (mri["exam_date"] >= "2025-10-01") & (mri["exam_date"] <= "2026-09-30")]
    m = m.merge(empi, on=["hospital", "mrn"], suffixes=("_order", ""))
    seen = set(m["enterprise_id"])
    a = w.groupby("family_variant_group").size().to_dict()
    b = w[~w["enterprise_id"].isin(seen)].groupby("family_variant_group").size().to_dict()
    for code in fig["ask_a"]:
        ok = a.get(code, 0) == fig["ask_a"][code] and b.get(code, 0) == fig["ask_b"][code]
        bad += not ok
        print("%-11s A %4d (figures %4d)  B %4d (figures %4d)  %s" % (code, a.get(code, 0), fig["ask_a"][code],
                                                                     b.get(code, 0), fig["ask_b"][code],
                                                                     "ok" if ok else "MISMATCH"))
    print("verify:", "PASS" if bad == 0 else "FAIL %d" % bad)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(run(os.path.dirname(HERE)))
