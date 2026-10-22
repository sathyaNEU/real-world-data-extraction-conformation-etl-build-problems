"""An independent recomputation of task482's golden from target/ alone, in code that shares nothing with bundle.py:
pandas for the files, a joint maximum likelihood Rasch fit with a position term written here, and the placements by
the policy's words. Exit 1 when any figure in figures.json does not recompute."""
import json
import math
import os
import sys

import numpy as np
import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")


def f(name):
    return os.path.join(T, name)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    fails = []
    pool = pd.read_csv(f("itemstore_assembly_pool_2027-02-03.csv"), dtype=str)
    pool["logit"] = (pool["difficulty_bu"].astype(float) - 500) / 100
    m = pd.read_csv(f("qpi_form_27A_assembly.csv"), dtype=str)
    anchors = m[m.section == "anchor"].item_id.tolist()
    unique = m[m.section == "unique"].item_id.tolist()
    d = dict(zip(pool.item_id, pool.logit))

    # responses: old platform by version map, new platform by seq
    lay = pd.read_csv(f("qpi_forms_26A_26B_layout.csv"), dtype=str)
    key = dict(zip(lay.item_id, lay.key))
    at = {}
    for _, r in lay.iterrows():
        fm = r.form if r.form in ("26A", "26B") else "FT" + r.form.split("-")[1]
        at[(fm, "A", int(r.kts_position_version_A))] = r.item_id
        at[(fm, "B", int(r.kts_position_version_B))] = r.item_id
    old = pd.read_csv(f("kts_qpi_attempts_2026-03-01_to_2026-06-30.csv"), dtype=str)
    rows = []
    for _, r in old.iterrows():
        for p in range(1, 71):
            fm = r.form if p <= 60 else "FT" + r.ft_set
            iid = at[(fm, r.version, p)]
            rows.append((r.attempt_id, iid, p, int(r.responses[p - 1] == key[iid])))
    resp = pd.concat([pd.DataFrame(rows, columns=["att", "item", "pos", "y"]),
                      pd.read_csv(f("northgate_item_responses_2026-07-01_to_2027-01-31.csv"),
                                  usecols=["attempt_ref", "item_id", "seq", "score"]).rename(
                          columns={"attempt_ref": "att", "item_id": "item", "seq": "pos", "score": "y"})])
    anchor = set(pool[pool.status == "anchor"].item_id)
    A = pd.factorize(resp.att)[0]
    items, I = np.unique(resp.item.values, return_inverse=True)
    X = resp.pos.values.astype(float)
    Y = resp.y.values.astype(float)
    isA = np.array([i in anchor for i in items])
    fixed = np.array([d.get(i, 0.0) for i in items])
    Xc = np.where(isA[I], 0.0, X)
    nI, nP = len(items), A.max() + 1
    th = np.zeros(nP)
    bb = fixed.copy()
    g = 0.0

    def sig(z):
        return 1 / (1 + np.exp(-z))
    for _ in range(500):
        pr = sig(th[A] - bb[I] - g * Xc)
        w = pr * (1 - pr)
        th += np.clip(np.bincount(A, Y - pr, nP) / np.maximum(np.bincount(A, w, nP), 1e-9), -1, 1)
        pr = sig(th[A] - bb[I] - g * Xc)
        w = pr * (1 - pr)
        step = np.bincount(I, pr - Y, nI) / np.maximum(np.bincount(I, w, nI), 1e-9)
        step[isA] = 0
        bb += np.clip(step, -1, 1)
        pr = sig(th[A] - bb[I] - g * Xc)
        w = pr * (1 - pr)
        free = ~isA[I]
        xm = np.bincount(I, w * Xc, nI) / np.maximum(np.bincount(I, w, nI), 1e-9)
        xc = Xc - xm[I]
        g += np.clip(np.sum((pr - Y)[free] * xc[free]) / np.sum((w * xc * xc)[free]), -0.005, 0.005)
    pos = np.arange(21, 71)

    def expected(t, gam):
        e = sum(sig(t - d[i]) for i in anchors)
        return e + sum(float(sig(t - (d[i] - gam * (65.5 - pos))).mean()) for i in unique)
    for lv, t, k_e, k_s in (("CA", 0.20, "expected_raw_ca", "college_algebra_score"),
                            ("CCA", -0.70, "expected_raw_cca", "corequisite_score")):
        e = expected(t, g)
        if "%.1f" % e != "%.1f" % F["components"][k_e]:
            fails.append("%s expected %.3f against %s" % (lv, e, F["components"][k_e]))
        if math.ceil(e) != F["call"][k_s]:
            fails.append("%s placement score %d against %s" % (lv, math.ceil(e), F["call"][k_s]))
        e0 = expected(t, 0.0)
        if math.ceil(e0) != F["rivals"]["filed_%s_score" % lv.lower()]:
            fails.append("%s filed score" % lv)
    if "%.2f" % (20 * g) != "%.2f" % F["components"]["carry_logits"]:
        fails.append("carry %.4f against %s" % (20 * g, F["components"]["carry_logits"]))
    print("verify: position term %.5f (JML), expected %.3f / %.3f" % (g, expected(0.2, g), expected(-0.7, g)))

    # the asks
    new = pd.read_csv(f("northgate_attempts_2026-07-01_to_2027-01-31.csv"), dtype=str)
    old["dob"] = pd.to_datetime(old.birth_date, format="%m/%d/%Y").dt.strftime("%Y-%m-%d")
    old["reg"] = pd.to_datetime(old.registered, format="%m/%d/%Y").dt.strftime("%Y-%m-%d")
    old["when"] = pd.to_datetime(old.test_date + " " + old.start, format="%m/%d/%Y %H:%M")
    old["level"] = old.placement.map({"131": "CA", "131C": "CCA", "091": "DM"})
    cen = pd.read_csv(f("qpi_testing_centres.csv"), dtype=str)
    site = dict(zip(cen.kts_site, cen.centre))
    old["centre"] = old.site.map(site)
    old["sess_date"] = pd.to_datetime(old.test_date, format="%m/%d/%Y").dt.strftime("%Y-%m-%d")
    hh = old.start.str.slice(0, 2).astype(int)
    old["sess_start"] = np.where(hh >= 17, "17:30", np.where(hh >= 12, "13:00", "09:00"))
    utc = pd.to_datetime(new.started_at, format="%Y-%m-%dT%H:%M:%SZ")
    dst = (utc >= pd.Timestamp("2026-03-08 08:00")) & (utc < pd.Timestamp("2026-11-01 07:00"))
    new["when"] = utc - pd.to_timedelta(np.where(dst, 5, 6), unit="h")
    new["dob"], new["reg"], new["level"] = new.birth_date, new.registered, new.placement
    parts = new.session_ref.str.split("-", expand=True)
    new["centre"] = "TC" + parts[0].str.slice(1)
    new["sess_date"] = pd.to_datetime(parts[1], format="%Y%m%d").dt.strftime("%Y-%m-%d")
    new["sess_start"] = parts[2].str.slice(0, 2) + ":" + parts[2].str.slice(2)
    cols = ["att", "dob", "sex", "hs_code", "reg", "when", "level", "centre", "sess_date", "sess_start"]
    old2 = old.rename(columns={"attempt_id": "att"})[cols]
    new2 = new.rename(columns={"attempt_ref": "att"})[cols]
    allat = pd.concat([old2, new2], ignore_index=True)
    ws = openpyxl.load_workbook(f("qpi_session_review_log_2026.xlsx"), read_only=True).active
    log = [r for r in ws.iter_rows(min_row=5, values_only=True) if r and r[0]]
    log.sort(key=lambda r: r[0])
    state = {}
    for logged, centre, sdate, sstart, plat, ref, decision, n, note in log:
        k = (centre, pd.Timestamp(sdate).strftime("%Y-%m-%d"), str(sstart))
        state[k] = decision == "Attempts invalidated"
    bad = {k for k, v in state.items() if v}
    allat["invalid"] = [(c, dd, s) in bad for c, dd, s in zip(allat.centre, allat.sess_date, allat.sess_start)]
    allat = allat[~allat.invalid].copy()
    rep = pd.read_csv(f("qpi_score_reports_2026-03-01_to_2027-01-31.csv"), dtype=str)
    auto = rep[rep.report == "automatic"].set_index("attempt").sent_to
    allat["college"] = allat.att.map(auto)
    allat["person"] = allat.dob + "|" + allat.sex + "|" + allat.hs_code + "|" + allat.reg
    allat["rank"] = allat.level.map({"DM": 0, "CCA": 1, "CA": 2})
    allat = allat.sort_values(["person", "rank", "when"])
    best = allat.groupby("person").tail(1)
    n_sit = allat.groupby("person").size()
    best = best.assign(twice=best.person.map(n_sit) >= 2)
    for code in sorted(F["colleges"]):
        sub = best[best.college == code]
        got = dict(placed=len(sub), CA=int((sub.level == "CA").sum()), CCA=int((sub.level == "CCA").sum()),
                   twice=int(sub.twice.sum()))
        for k, v in got.items():
            if v != F["colleges"][code][k]:
                fails.append("college %s %s %d against %d" % (code, k, v, F["colleges"][code][k]))
    for k in ("placed", "CA", "CCA", "twice"):
        if sum(F["colleges"][c][k] for c in F["colleges"]) != F["system"][k]:
            fails.append("system %s" % k)
    conv = F["conversion"]
    for r in range(61):
        want = "CA" if r >= F["call"]["college_algebra_score"] else ("CCA" if r >= F["call"]["corequisite_score"]
                                                                     else "DM")
        if conv[str(r)] != want:
            fails.append("conversion %d" % r)
    g_csv = pd.read_csv(os.path.join(TASK, "golden", "qpi_form27a_score_conversion.csv"), dtype=str)
    if list(g_csv.placement) != [conv[str(r)] for r in range(61)]:
        fails.append("golden conversion file")
    wb = openpyxl.load_workbook(os.path.join(TASK, "golden", "qpi_placement_review_2027.xlsx"), data_only=True)
    s1 = wb["Form 27A"]
    if (s1["D5"].value, s1["D6"].value) != (F["call"]["college_algebra_score"], F["call"]["corequisite_score"]):
        fails.append("workbook placement scores")
    s2 = wb["Colleges 2026"]
    for row in s2.iter_rows(min_row=5, max_row=18, values_only=True):
        c = row[0]
        if [row[2], row[3], row[4], row[5]] != [F["colleges"][c][k] for k in ("placed", "CA", "CCA", "twice")]:
            fails.append("workbook college %s" % c)
    for x in fails:
        print("FAIL  " + x)
    print("%s  verify: %d figures and files recomputed independently, %d failures" % ("PASS" if not fails else "FAIL",
                                                                                   4 + 56 + 61 + 4, len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
