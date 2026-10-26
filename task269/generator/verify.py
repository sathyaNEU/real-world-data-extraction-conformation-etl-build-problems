"""The independent verifier: reads only the shipped bundle (target/ and figures.json) and recomputes the call, the
critical components and every ask figure with its own code, then compares with figures.json."""
import json
import os
import sys

import numpy as np
import pandas as pd

WARDS = ["AMU", "ESSU", "4A", "7A", "5A", "6A", "6B", "7B", "8A", "9A", "9B", "PCU", "CCU", "ICU"]


def _hm(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def _r1(x):
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(float(x))).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def run(task):
    T = os.path.join(task, "target")
    fig = json.load(open(os.path.join(task, "generator", "figures.json")))
    out = []

    def ok(label, a, b):
        out.append((label, a == b, "%s | %s" % (a, b)))

    ref = pd.read_excel(os.path.join(T, "ward_and_area_reference.xlsx"), sheet_name=None, dtype=str)
    w = ref["Wards"]
    canon = {c: ("6A" if c == "S1A" else c) for c in w["code"]}
    dept = dict(zip(w["audit_application_department"], w["code"].map(canon)))
    lab = dict(zip(w["laboratory_location"], w["code"].map(canon)))
    cc = dict(zip(w["cost_centre"], w["code"].map(canon)))
    disp = dict(zip(ref["Dispensers"]["dispenser_id"], ref["Dispensers"]["ward_or_area"].map(lambda u: canon.get(u, u))))

    # ---- the ward-shifts: required care hours and worked nursing hours
    ac = pd.read_csv(os.path.join(T, "acuity_patient_shifts_2025_26.csv"), dtype={"ward": str})
    ac["ward"] = ac["ward"].map(canon)
    req = ac.groupby(["ward", "shift_date", "shift"])["required_care_hours"].sum()
    ro = pd.read_csv(os.path.join(T, "nursing_roster_actuals_2025_26.csv"), dtype=str)
    ro = ro[(ro["shift_category"] == "Rostered") & ro["shift_code"].isin(["AM", "PM"])]
    ro["ward"] = ro["ward"].map(canon)
    ro["shift_date"] = pd.to_datetime(ro["roster_date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    wk = ro.assign(h=ro["worked_hours"].astype(float)).groupby(["ward", "shift_date", "shift_code"])["h"].sum()
    wk.index.names = ["ward", "shift_date", "shift"]
    sh = pd.concat([req.rename("req"), wk.rename("worked")], axis=1).reset_index()
    sh["v"] = sh["req"] / sh["worked"]
    # ---- the audited day moments
    au = pd.read_csv(os.path.join(T, "hand_hygiene_audit_moments_2025_26.csv"), dtype=str)
    au["ward"] = au["department"].map(dept)
    au = au[au["ward"].isin(WARDS)]
    t = au["session_start"].map(_hm)
    au["shift"] = np.where((t >= 420) & (t < 780), "AM", np.where((t >= 930) & (t < 1260), "PM", "other"))
    au = au[au["shift"] != "other"]
    au["shift_date"] = pd.to_datetime(au["session_date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    au["y"] = au["action"].isin(["Hand rub", "Hand wash"]).astype(int)
    se = au.groupby(["session_id", "ward", "shift_date", "shift"])["y"].agg(["sum", "size"]).reset_index()
    se = se.merge(sh, on=["ward", "shift_date", "shift"])
    # ---- the golden: logistic fit of ward and shortfall band by IRLS on the session totals
    edges = [1.05, 1.15, 1.25, 1.35]
    band = lambda v: np.digitize(v, edges)
    X = np.zeros((len(se), len(WARDS) + len(edges)))
    X[np.arange(len(se)), se["ward"].map(WARDS.index).to_numpy()] = 1
    bb = band(se["v"].to_numpy())
    for j in range(1, len(edges) + 1):
        X[bb == j, len(WARDS) + j - 1] = 1
    y, n = se["sum"].to_numpy(float), se["size"].to_numpy(float)
    beta = np.zeros(X.shape[1])
    for _ in range(60):
        p = 1 / (1 + np.exp(-X @ beta))
        Wt = n * p * (1 - p)
        beta = beta + np.linalg.solve(X.T @ (X * Wt[:, None]) + 1e-9 * np.eye(X.shape[1]), X.T @ (y - n * p))
    est = {}
    for i, c in enumerate(WARDS):
        x = sh[sh["ward"] == c]
        b2 = band(x["v"].to_numpy())
        z = beta[i] + np.where(b2 > 0, beta[len(WARDS) + np.maximum(b2, 1) - 1], 0.0)
        est[c] = float((x["req"].to_numpy() / (1 + np.exp(-z))).sum() / x["req"].sum())
    funded = [c for c in WARDS if est[c] < 0.80]
    ok("call: funded wards", funded, fig["call"]["funded"])
    # ---- components
    s10, a10 = sh["req"] > 1.1 * sh["worked"], se["req"] > 1.1 * se["worked"]
    comp = fig["components"]
    ok("component care hours on shifts over 10 per cent short", _r1(100 * sh.loc[s10, "req"].sum() / sh["req"].sum()),
       comp["care_hours_on_shifts_over_10_per_cent_short"])
    ok("component audited moments there", _r1(100 * se.loc[a10, "size"].sum() / se["size"].sum()),
       comp["audited_moments_on_shifts_over_10_per_cent_short"])
    ok("component compliance there", _r1(100 * se.loc[a10, "sum"].sum() / se.loc[a10, "size"].sum()),
       comp["compliance_on_those_shifts"])
    ok("component compliance elsewhere", _r1(100 * se.loc[~a10, "sum"].sum() / se.loc[~a10, "size"].sum()),
       comp["compliance_on_other_audited_shifts"])
    raw = au.groupby("ward")["y"].mean()
    ok("component audits as they stand, 9B", _r1(100 * raw["9B"]), comp["audits_as_they_stand"]["9B"])
    ok("component audits as they stand, lowest other ward", _r1(100 * raw.drop("9B").min()), comp["audits_lowest_other_ward"])

    # ---- Ask A: hospital-onset bloodstream infections
    ce = pd.read_csv(os.path.join(T, "midnight_census_2025_26.csv"), dtype={"ward": str})
    obd = ce.assign(ward=ce["ward"].map(canon)).groupby("ward")["occupied_beds"].sum()
    iso = pd.read_csv(os.path.join(T, "blood_culture_isolates_2025_26.csv"), dtype=str)
    iso["t"] = pd.to_datetime(iso["collected"], format="%d/%m/%Y %H:%M")
    ad = pd.read_csv(os.path.join(T, "blood_culture_patient_admissions_2025_26.csv"), dtype=str)
    ad["a"] = pd.to_datetime(ad["admitted"], format="%d/%m/%Y %H:%M")
    ad["s"] = pd.to_datetime(ad["separated"], format="%d/%m/%Y %H:%M")
    tr = pd.read_csv(os.path.join(T, "ward_transfers_2025_26.csv"), dtype=str)
    tr["t"] = pd.to_datetime(tr["transferred"], format="%d/%m/%Y %H:%M")
    known = set(ad["mrn"])
    link = []
    for _, r in iso.iterrows():
        if r["mrn"] in known:
            c = ad[(ad["mrn"] == r["mrn"]) & (ad["a"] <= r["t"]) & (ad["s"] >= r["t"])]
        else:
            c = ad[(ad["date_of_birth"] == r["date_of_birth"]) & (ad["sex"] == r["sex"]) & (ad["a"] <= r["t"]) &
                   (ad["s"] >= r["t"])]
        link.append(c["admission_no"].iloc[0] if len(c) == 1 else None)
    iso["adm"] = link
    iso = iso[iso["adm"].notna()]
    commensal = iso["organism"].str.contains("epidermidis|hominis|Micrococcus|Corynebacterium|Cutibacterium|Bacillus|viridans")
    # a stay in the hospital runs on through an admission that opened at the minute the patient's previous one closed
    adm_at, prev = {}, {}
    for _, r in ad.sort_values(["mrn", "a"]).iterrows():
        q = prev.get(r["mrn"])
        adm_at[r["admission_no"]] = adm_at[q[0]] if q is not None and q[1] == r["a"] else r["a"]
        prev[r["mrn"]] = (r["admission_no"], r["s"])
    first_ward = dict(zip(ad["admission_no"], ad["admitting_ward"].map(lambda x: canon.get(x, x))))
    moves = {k: list(zip(g["t"], g["to_ward"].map(lambda x: canon.get(x, x)))) for k, g in tr.sort_values("t").groupby("admission_no")}
    count = {c: 0 for c in WARDS}
    mrn_of = dict(zip(ad["admission_no"], ad["mrn"]))
    iso["who"] = iso["adm"].map(mrn_of)
    for (who, org), g in iso.assign(cm=commensal).sort_values("t").groupby(["who", "organism"]):
        ts = list(g["t"])
        adms = list(g["adm"])
        if g["cm"].iloc[0]:
            starts = [ts[i] for i in range(len(ts) - 1) if ts[i + 1] - ts[i] <= pd.Timedelta(hours=48)][:1]
        else:
            starts = ts
        anchor = None
        for t0 in starts:
            if anchor is not None and t0 - anchor < pd.Timedelta(days=14):
                continue
            anchor = t0
            a_no = adms[ts.index(t0)]
            if t0 - adm_at[a_no] <= pd.Timedelta(hours=48):
                continue
            ward = first_ward[a_no]
            for tt, wv in moves.get(a_no, []):
                if tt <= t0:
                    ward = wv
            if ward in count:
                count[ward] += 1
    for c in WARDS:
        ok("Ask A HOBSI %s" % c, count[c], fig["asks"]["A"]["hobsi"][c])
        ok("Ask A rate %s" % c, _r1(count[c] / obd[c] * 10000), fig["asks"]["A"]["rate_per_10000_obd"][c])

    # ---- Ask B: hand rub put out
    iss0 = pd.read_csv(os.path.join(T, "store_issues_hand_hygiene_2025_26.csv"), dtype=str)
    iss = iss0[iss0["cost_centre"].isin(cc) & iss0["item_code"].isin(["114502", "114519"])]
    iss["L"] = iss["quantity"].astype(int) * iss["item_code"].map({"114502": 0.5, "114519": 2.4})
    bottles = iss.groupby(iss["cost_centre"].map(cc))["L"].sum()
    rd = pd.read_csv(os.path.join(T, "dispenser_rounds_2025_26.csv"), dtype=str)
    rd["t"] = pd.to_datetime(rd["fitted"], format="%d/%m/%Y %H:%M")
    rd = rd.sort_values(["t", "record_id"])
    last = {}
    keep = []
    for _, r in rd.iterrows():
        k = (r["dispenser_id"], r["t"].strftime("%H:%M"))
        prev = last.get(k)
        if prev is not None and 0 < (r["t"].normalize() - prev).days <= 20:
            keep.append(False)
            continue
        last[k] = r["t"].normalize()
        keep.append(True)
    rd = rd[keep]
    kind = dict(zip(ref["Dispensers"]["dispenser_id"], ref["Dispensers"]["type"]))
    wall = rd[rd["dispenser_id"].map(kind) == "Hand rub"]["dispenser_id"].map(disp).value_counts()
    for c in WARDS:
        L = float(bottles.get(c, 0.0)) + float(wall.get(c, 0))
        ok("Ask B litres %s" % c, _r1(L), fig["asks"]["B"]["litres"][c])
        ok("Ask B rate %s" % c, _r1(L / obd[c] * 1000), fig["asks"]["B"]["litres_per_1000_obd"][c])
    # ---- Ask C: hand soap put out
    sp = iss0[iss0["cost_centre"].isin(cc) & (iss0["item_code"] == "114541")]
    soap_b = sp.groupby(sp["cost_centre"].map(cc))["quantity"].apply(lambda q: q.astype(int).sum() * 0.5)
    dtype = dict(zip(ref["Dispensers"]["dispenser_id"], ref["Dispensers"]["type"]))
    soap = rd[rd["dispenser_id"].map(dtype) == "Hand soap"]
    sw = soap["dispenser_id"].map(disp).value_counts()
    for c in WARDS:
        L = float(soap_b.get(c, 0.0)) + 0.8 * float(sw.get(c, 0))
        ok("Ask C litres %s" % c, _r1(L), fig["asks"]["C"]["litres"][c])
        ok("Ask C rate %s" % c, _r1(L / obd[c] * 1000), fig["asks"]["C"]["litres_per_1000_obd"][c])
    bad = [o for o in out if not o[1]]
    for label, good, detail in out:
        if not good:
            print("FAIL  %s  %s" % (label, detail))
    print("verify: %d figures, %d differ: %s" % (len(out), len(bad), "PASS" if not bad else "FAIL"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
