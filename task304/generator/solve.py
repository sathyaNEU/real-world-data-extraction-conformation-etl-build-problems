"""Every owed figure, computed from the shipped files under target/ only.

The funnel for each setting in 2027: arrivals (the yearly average of distinct people arriving in the two plan years
to 30 September 2026), tested (the pilot's share tested), antibody positive (the peer team's reactive share among the
setting's arrivals it tested in those two years), active infection (each of those positives' status at the test,
read from every record that holds it, averaged), started (the pilot's share started within twelve weeks).

The rungs differ only in how each positive's status at the test is read:
  R0  every positive counted as a start candidate (no viraemic share)
  R1  every positive at the validated viraemic share (the laboratory's first reactive antibody results)
  R2  each positive's status from the network's own records: the treatment register and the regional laboratory
  R3  the golden: R2 plus the prison health provider's course log (cures and courses given inside)"""
import datetime as dt
import json
import os
from collections import defaultdict

import pandas as pd

import params as P

D = dt.date
POOL_END_1 = D(2025, 9, 30)


def _date(s):
    if s is None or (isinstance(s, float) and pd.isna(s)) or s == "":
        return None
    if isinstance(s, (dt.datetime, pd.Timestamp)):
        return s.date()
    if isinstance(s, dt.date):
        return s
    s = str(s).strip()
    if "/" in s:
        d, m, y = s.split("/")
        return D(int(y), int(m), int(d))
    return D.fromisoformat(s[:10])


def plan_year(d):
    if P.POOL_START <= d <= POOL_END_1:
        return 1
    if POOL_END_1 < d <= P.AS_OF:
        return 2
    return None


def load(target):
    f = P.FILES
    T = {}
    T["arr"] = pd.read_csv(os.path.join(target, f["arrivals"]), dtype=str)
    T["peer"] = pd.read_csv(os.path.join(target, f["peer"]), dtype=str, keep_default_na=False)
    T["pilot"] = pd.read_csv(os.path.join(target, f["pilot"]), dtype=str, keep_default_na=False)
    T["lab"] = pd.read_csv(os.path.join(target, f["lab"]), dtype=str, keep_default_na=False)
    T["reg"] = pd.read_csv(os.path.join(target, f["register"]), dtype=str, keep_default_na=False)
    x = pd.read_excel(os.path.join(target, f["prison"]), sheet_name=None, dtype=str)
    old = x["Courses 2017-20"].fillna("")
    new = x["Courses 2021-26"].fillna("")
    old = pd.DataFrame({"pseudonym": old["Pseudo ID"].str.upper(), "start": old["Start"], "end": old["End"],
                        "released": old["Released in course"].map({"Y": True, "N": False}),
                        "release": "", "svr_date": old["SVR12 (date)"], "svr": old["SVR12"]})
    new = pd.DataFrame({"pseudonym": new["Pseudonym"].str.upper(), "start": new["Course start"],
                        "end": new["Course end"], "released": new["Released before end"].map({"Yes": True, "No": False}),
                        "release": new["Release date"], "svr_date": new["SVR12 date"], "svr": new["SVR12 result"]})
    T["prison"] = pd.concat([old, new], ignore_index=True)
    rc = x["Reception BBV positives"].fillna("")
    T["reception"] = pd.DataFrame({"pseudonym": rc["Pseudonym"].str.upper(), "d": rc["Reception test date"].map(_date),
                                   "rna": rc["HCV RNA"]})
    T["clinics"] = pd.read_csv(os.path.join(target, f["clinics"]), dtype=str)
    return T


def rates(T):
    pl = T["pilot"]
    arrived = len(pl)
    tested = (pl["tested_by_van"] == "Y").sum()
    reactive = ((pl["tested_by_van"] == "Y") & (pl["antibody"] == "Reactive")).sum()
    det = pl[(pl["rna"] == "Detected")]
    started12 = 0
    for _, r in det.iterrows():
        if r["treatment_started"] == "Y" and (_date(r["start_date"]) - _date(r["test_date"])).days <= 84:
            started12 += 1
    out = dict(pilot_arrived=int(arrived), pilot_tested=int(tested), pilot_reactive=int(reactive),
               pilot_detected=int(len(det)), pilot_started12=int(started12),
               test_share=tested / arrived, start_share=started12 / len(det),
               pilot_ratio=len(det) / reactive)
    # the laboratory's first reactive antibody results and the RNA result on the same occasion
    lab = lab_frame(T)
    ab = lab[lab["test"] == "AB"]
    first = ab[ab["result"] == "Reactive"].sort_values(["sample_taken", "lab_number"]).drop_duplicates("pseudonym")
    rna = lab[lab["test"] == "RNA"]
    rna_by = defaultdict(list)
    for p, d, res in zip(rna["pseudonym"], rna["sample_taken"], rna["result"]):
        rna_by[p].append((d, res))
    n = k = 0
    for p, d in zip(first["pseudonym"], first["sample_taken"]):
        hits = sorted([x for x in rna_by.get(p, []) if 0 <= (x[0] - d).days <= 30])
        if hits:
            n += 1
            k += hits[0][1] != "Not detected"
    out.update(lab_first_positives=int(n), lab_first_detected=int(k), lab_ratio=k / n)
    return out


def lab_frame(T):
    if "_labf" in T:
        return T["_labf"]
    lab = T["lab"].drop_duplicates(["lab_number"]).copy()
    lab["sample_taken"] = lab["sample_taken"].map(_date)
    lab["test"] = lab["test_code"].map({"HCVAB": "AB", "HCV-AB-EIA": "AB", "HCVPCR": "RNA", "HCV-RNA-VL": "RNA"})
    lab["result"] = lab["result"].map(lambda s: "Not detected" if s == "Not detected" else
                                      ("Detected" if s.startswith("Detected") else s))
    T["_labf"] = lab
    return lab


def pool(T, window=60):
    """distinct arrivals per plan year, and the reactive tests of each setting's arrivals in the two years"""
    arr = T["arr"].copy()
    arr["d"] = arr["arrival_date"].map(_date)
    arr["py"] = arr["d"].map(plan_year)
    A = {}
    for s in P.SETTINGS:
        a = arr[(arr["setting"] == s) & arr["py"].notna()]
        A[s] = (a[a["py"] == 1]["pseudonym"].nunique() + a[a["py"] == 2]["pseudonym"].nunique()) / 2
    peer = T["peer"]
    peer = peer[peer["result"].isin(["Reactive", "Non-reactive"])].copy()
    peer["d"] = peer["test_date"].map(_date)
    arr_by = defaultdict(list)
    for p, s, d, py in zip(arr["pseudonym"], arr["setting"], arr["d"], arr["py"]):
        if py:
            arr_by[p].append((d, s))
    tests = []
    for _, r in peer.iterrows():
        if not r["pseudonym"]:
            continue
        hits = [(d, s) for (d, s) in arr_by.get(r["pseudonym"], []) if 0 <= (r["d"] - d).days <= window]
        if hits:
            d, s = max(hits)
            tests.append(dict(pid=r["pseudonym"], setting=s, test_date=r["d"], reactive=r["result"] == "Reactive",
                              written=r["setting_or_venue"]))
    return A, pd.DataFrame(tests)


def histories(T):
    """per person: cure dates and course spans from each record, and the laboratory's RNA results"""
    lab = lab_frame(T)
    rna = defaultdict(list)
    for p, d, res in zip(lab["pseudonym"], lab["sample_taken"], lab["result"]):
        if res in ("Detected", "Not detected"):
            rna[p].append((d, res))
    reg = T["reg"]
    net_cure, net_span = defaultdict(list), defaultdict(list)
    for _, r in reg.iterrows():
        st = _date(r["start_date"])
        last = _date(r["stopped_on"]) if r["outcome"] == "Stopped" else _date(r["planned_end"])
        net_span[r["pseudonym"]].append((st, last))
        if r["svr12_result"] == "Not detected":
            net_cure[r["pseudonym"]].append(_date(r["svr12_date"]))
    pr = T["prison"]
    pr_cure, pr_span = defaultdict(list), defaultdict(list)
    for _, r in pr.iterrows():
        st, en = _date(r["start"]), _date(r["end"])
        rel = _date(r["release"]) if r["release"] else None
        pr_span[r["pseudonym"]].append((st, en))
        if r["svr"] == "Not detected":
            pr_cure[r["pseudonym"]].append(_date(r["svr_date"]))
    pr_rna = defaultdict(list)
    for p, d, res in zip(T["reception"]["pseudonym"], T["reception"]["d"], T["reception"]["rna"]):
        pr_rna[p].append((d, res))
    return dict(rna=rna, net_cure=net_cure, net_span=net_span, pr_cure=pr_cure, pr_span=pr_span, pr_rna=pr_rna)


def status(pid, when, H, ratio, use_prison=True, use_lab=True, reinf=True):
    """a positive's chance of an active infection at a test on `when`, from the records the route reads"""
    spans = list(H["net_span"].get(pid, []))
    cures = [d for d in H["net_cure"].get(pid, []) if d and d < when]
    if use_prison:
        spans += H["pr_span"].get(pid, [])
        cures += [d for d in H["pr_cure"].get(pid, []) if d and d < when]
    if any(st is not None and st <= when and (en is None or en >= when) for st, en in spans):
        return 0.0                                   # on a course when the van meets them: not a start
    rna = sorted(x for x in H["rna"].get(pid, []) if x[0] < when) if use_lab else []
    if use_prison:
        rna = sorted(rna + [x for x in H["pr_rna"].get(pid, []) if x[0] < when])
    if cures:
        last = max(cures)
        if reinf and any(d > last and res == "Detected" for d, res in rna):
            return 1.0
        return 0.0
    if rna:
        return 1.0 if rna[-1][1] == "Detected" else 0.0
    return ratio


def funnel(T, R=None):
    R = R or rates(T)
    A, tests = pool(T)
    H = histories(T)
    out = {}
    for s in P.SETTINGS:
        t = tests[tests["setting"] == s]
        pos = t[t["reactive"]]
        ab = len(pos) / len(t)
        arrivals = A[s]
        tested = arrivals * R["test_share"]
        positives = tested * ab
        st = {}
        for key, kw in {"R3": dict(), "R2": dict(use_prison=False), "R3_pilot_ratio": dict(),
                        "R3_no_reinfection": dict(reinf=False), "R3_no_lab_for_never": dict(use_lab=False)}.items():
            ratio = R["pilot_ratio"] if key == "R3_pilot_ratio" else R["lab_ratio"]
            vals = [status(p, d, H, ratio, **kw) for p, d in zip(pos["pid"], pos["test_date"])]
            st[key] = sum(vals) / len(vals)
        rec = dict(arrivals=arrivals, tested=tested, ab_share=ab, positives=positives, n_tests=len(t),
                   n_positive=len(pos))
        for key, v in st.items():
            rec["active_" + key] = positives * v
            rec["starts_" + key] = positives * v * R["start_share"]
        rec["active_R1"] = positives * R["lab_ratio"]
        rec["starts_R1"] = rec["active_R1"] * R["start_share"]
        rec["starts_R1_pilot"] = positives * R["pilot_ratio"] * R["start_share"]
        rec["starts_R0"] = positives * R["start_share"]
        rec["active"] = rec["active_R3"]
        rec["starts"] = rec["starts_R3"]
        # the prison log read with no cures but its courses running at the test (a half-handled route)
        out[s] = rec
    return out, R


def aliases(T):
    """for each pseudonym, every pseudonym Fenwold Pathology holds for the same patient (its lims_patient_id)"""
    if "_alias" in T:
        return T["_alias"]
    lab = T["lab"]
    by = defaultdict(set)
    for l, p in zip(lab["lims_patient_id"], lab["pseudonym"]):
        by[l].add(p)
    out = {}
    for ps in by.values():
        for p in ps:
            out[p] = sorted(ps)
    T["_alias"] = out
    return out


def ask_a(T):
    """courses the network's clinics finished between 1 October 2024 and 30 September 2025, and how many are
    confirmed as cures: an RNA test taken twelve weeks or more after the last dose, not detected"""
    lab = lab_frame(T)
    rna = defaultdict(list)
    for p, d, res in zip(lab["pseudonym"], lab["sample_taken"], lab["result"]):
        if res in ("Detected", "Not detected"):
            rna[p].append((d, res))
    AL = aliases(T)
    out = {}
    reg = T["reg"]
    for c in P.CLINICS:
        out[c] = dict(finished=0, confirmed=0)
    for _, r in reg.iterrows():
        if r["outcome"] == "Stopped":
            last = _date(r["stopped_on"])
        elif r["outcome"] == "Completed":
            last = _date(r["planned_end"])
        else:
            continue
        if not (P.POOL_START <= last <= POOL_END_1):
            continue
        out[r["clinic_code"]]["finished"] += 1
        ids = AL.get(r["pseudonym"], [r["pseudonym"]])
        after = sorted(x for i in ids for x in rna.get(i, []) if (x[0] - last).days >= 84 and x[0] <= P.AS_OF)
        ok = (after and after[0][1] == "Not detected")
        if r["svr12_result"] == "Not detected" and _date(r["svr12_date"]) and (_date(r["svr12_date"]) - last).days >= 84:
            ok = True
        out[r["clinic_code"]]["confirmed"] += int(bool(ok))
    return out


def ask_a_halves(T):
    """the same as ask_a, split into the two half-years: October 2024 to March 2025 and April to September 2025"""
    lab = lab_frame(T)
    rna = defaultdict(list)
    for p, d, res in zip(lab["pseudonym"], lab["sample_taken"], lab["result"]):
        if res in ("Detected", "Not detected"):
            rna[p].append((d, res))
    AL = aliases(T)
    out = {(c, h): dict(finished=0, confirmed=0) for c in P.CLINICS for h in (1, 2)}
    for _, r in T["reg"].iterrows():
        if r["outcome"] == "Stopped":
            last = _date(r["stopped_on"])
        elif r["outcome"] == "Completed":
            last = _date(r["planned_end"])
        else:
            continue
        if not (P.POOL_START <= last <= POOL_END_1):
            continue
        h = 1 if last <= D(2025, 3, 31) else 2
        out[(r["clinic_code"], h)]["finished"] += 1
        ids = AL.get(r["pseudonym"], [r["pseudonym"]])
        after = sorted(x for i in ids for x in rna.get(i, []) if (x[0] - last).days >= 84 and x[0] <= P.AS_OF)
        ok = bool(after) and after[0][1] == "Not detected"
        if r["svr12_result"] == "Not detected" and _date(r["svr12_date"]) and (_date(r["svr12_date"]) - last).days >= 84:
            ok = True
        out[(r["clinic_code"], h)]["confirmed"] += int(ok)
    return out


def capacity(T, F, R):
    """courses running at once: the starts (eight or twelve weeks) and the people arriving part-way through a course"""
    pr = T["prison"]
    arr = T["arr"].copy()
    arr["d"] = arr["arrival_date"].map(_date)
    arr["py"] = arr["d"].map(plan_year)
    by = defaultdict(list)
    for p, s, d, py in zip(arr["pseudonym"], arr["setting"], arr["d"], arr["py"]):
        if py:
            by[p].append((d, s))
    cont = defaultdict(float)
    for _, r in pr.iterrows():
        if r["released"] and r["release"]:
            rel = _date(r["release"])
            for (d, s) in by.get(r["pseudonym"], []):
                if 0 <= (d - rel).days <= 14:
                    cont[s] += 0.5
    out = {}
    for s in P.SETTINGS:
        out[s] = dict(continuity_per_year=cont[s], running=F[s]["starts"] * 10.2 / 52 + cont[s] * 6 / 52)
    return out


def solve(target):
    T = load(target)
    F, R = funnel(T)
    order = sorted(P.SETTINGS, key=lambda s: -F[s]["starts"])
    A = ask_a(T)
    AH = ask_a_halves(T)
    C = capacity(T, F, R)
    return dict(F=F, R=R, order=order, A=A, AH=AH, C=C, T=T)


def r10(x):
    return int(10 * round(x / 10.0))


def cured_shares(T):
    """among each setting's reactive arrivals, the share cured before arriving, by the record that holds the cure"""
    A, tests = pool(T)
    H = histories(T)
    out = {}
    for s in P.SETTINGS:
        pos = tests[(tests["setting"] == s) & tests["reactive"]]
        n = len(pos)
        net = sum(1 for p, d in zip(pos["pid"], pos["test_date"]) if any(x and x < d for x in H["net_cure"].get(p, [])))
        allc = sum(1 for p, d in zip(pos["pid"], pos["test_date"])
                   if any(x and x < d for x in H["net_cure"].get(p, []) + H["pr_cure"].get(p, [])))
        out[s] = dict(n=n, net=net, any=allc, prison_only=allc - net)
    return out


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    S = solve(os.path.join(os.path.dirname(here), "target"))
    for s in P.SETTINGS:
        f = S["F"][s]
        print(s, " ".join("%s=%.2f" % (k, v) for k, v in f.items() if isinstance(v, float)))
    print(S["order"], S["R"])
    print(S["A"])
    print(S["C"])
