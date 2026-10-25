"""The independent verifier: reads only the shipped bundle (target/), the golden deliverables and figures.json, on its
own code path (pandas joins and group-bys, pdfplumber for the documents, no import of golden.py), and recomputes the
elections, every benchmark and threshold, both asks and the write-up's figures.

    python3 task482/generator/verify.py
"""
import json
import os
import re
import sys

import numpy as np
import openpyxl
import pandas as pd
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GD = os.path.join(TASK, "golden")
OK, BAD = [0], []
TS = pd.Timestamp


def v(label, cond, detail=""):
    OK[0] += 1
    if not cond:
        BAD.append(label)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  (" + detail + ")") if detail else ""))


def f(prefix):
    m = [n for n in os.listdir(T) if n.startswith(prefix)]
    assert len(m) == 1, prefix
    return os.path.join(T, m[0])


def pdf(prefix):
    with pdfplumber.open(f(prefix)) as d:
        return " ".join(" ".join(p.extract_text() or "" for p in d.pages).split())


def claims():
    """Every claim line of the three feeds at its current version, with the date its claim was first paid."""
    m = pd.read_csv(f("mlh_tcoc_claims"), dtype=str, keep_default_na=False)
    voided = set(m.loc[m.ADJ_TYP == "VOID", "ORIG_CLM_ID"])
    m["key"] = np.where(m.ORIG_CLM_ID != "", m.ORIG_CLM_ID, m.CLM_ID)
    m["fp"] = pd.to_datetime(m.groupby("key").PD_DT.transform("min"))
    m = m[(m.ADJ_TYP != "VOID") & ~m.CLM_ID.isin(voided)]
    a = pd.DataFrame({"payer": "MLH", "member": m.MBR_ID, "typ": m.CLM_TYP.replace({"PHRM": "RX"}), "svc": pd.to_datetime(m.SVC_FROM_DT),
                      "fp": m.fp, "paid": pd.to_datetime(m.PD_DT), "code": m.PROC_CD, "mod": m.PROC_MOD, "pos": m.POS_CD,
                      "npi": m.REND_NPI, "amt": m.ALLOWED_AMT.astype(float)})
    k = pd.read_csv(f("KBP_CLAIMS"), sep="|", dtype=str, keep_default_na=False)
    k["key"] = k.CLAIM_NO.str.split("-").str[0]
    k["pd"] = pd.to_datetime(k.PAID_DATE, format="%m/%d/%Y")
    k["fp"] = k.groupby("key").pd.transform("min")
    k = k[k.CLAIM_STATUS == "P"]
    b = pd.DataFrame({"payer": "KBP", "member": k.MEMBER_NO, "typ": k.CLAIM_FORM.map({"1500": "PROF", "UB04": "FAC", "NCPDP": "RX"}),
                      "svc": pd.to_datetime(k.FIRST_DOS, format="%m/%d/%Y"), "fp": k.fp, "paid": k.pd, "code": k.PROCEDURE,
                      "mod": k.MODIFIER, "pos": k.PLACE_OF_SVC, "npi": k.RENDERING_PROV_NPI,
                      "amt": k.ALLOWED_CENTS.astype(float) / 100})
    j = pd.DataFrame(json.load(open(f("pmh_partner_claims")))["records"])
    j["fp"] = pd.to_datetime(j.groupby("claimId").adjudicated.transform("min"))
    j = j.sort_values("version").drop_duplicates("claimId", keep="last")
    t = pd.DataFrame({"payer": "PMH", "member": j.memberId, "typ": j["type"].map(lambda s: "PROF" if s == "professional" else (
        "RX" if s == "pharmacy" else "FAC")), "svc": pd.to_datetime(j.serviceStart), "fp": j.fp,
        "paid": pd.to_datetime(j.adjudicated), "code": j.cpt.fillna(""), "mod": j["modifier"].fillna("") if "modifier" in j else "",
        "pos": j.pos.fillna(""), "npi": j.renderingNpi.fillna(""), "amt": j.allowed.astype(float)})
    return pd.concat([a, b, t], ignore_index=True)


def coverage():
    rows = []
    e = pd.read_csv(f("mlh_eligibility"), dtype=str)
    rows.append(pd.DataFrame({"payer": "MLH", "member": e.MBR_ID, "s": pd.to_datetime(e.COV_EFF_DT),
                              "e": pd.to_datetime(e.COV_TERM_DT.str.replace("9999-12-31", "2099-12-31"))}))
    e = pd.read_csv(f("KBP_ELIG"), sep="|", dtype=str, keep_default_na=False)
    rows.append(pd.DataFrame({"payer": "KBP", "member": e.MEMBER_NO, "s": pd.to_datetime(e.EFF_DATE, format="%m/%d/%Y"),
                              "e": pd.to_datetime(e.TERM_DATE.replace("", "12/31/2099"), format="%m/%d/%Y")}))
    e = pd.read_csv(f("pmh_members"), dtype=str, keep_default_na=False)
    rows.append(pd.DataFrame({"payer": "PMH", "member": e.memberId, "s": pd.to_datetime(e.coverageStart),
                              "e": pd.to_datetime(e.coverageEnd.replace("", "2099-12-31"))}))
    return pd.concat(rows, ignore_index=True)


def months(cov, year, upto):
    """Member months by payer and member: each calendar month a span touches, January to month upto."""
    out = {}
    for mo in range(1, upto + 1):
        first = TS(year, mo, 1)
        last = first + pd.offsets.MonthEnd(0)
        hit = cov[(cov.s <= last) & (cov.e >= first)][["payer", "member"]].drop_duplicates()
        for key in zip(hit.payer, hit.member):
            out[key] = out.get(key, 0) + 1
    return pd.Series(out)


def runs():
    tin = lambda x: str(x).replace("-", "")
    r = []
    a = pd.read_csv(f("mlh_attribution"), dtype=str)
    r.append(pd.DataFrame({"payer": "MLH", "member": a.MBR_ID, "run": np.where(a.RUN_ID == "PY2025-F", "F25", "R26"),
                           "tin": a.PRACTICE_TIN.map(tin)}))
    wb = openpyxl.load_workbook(f("KBP_ATTRIBUTION"), read_only=True)
    for sheet, tag in (("PY2025 Final", "F25"), ("PY2026 Run 10", "R26")):
        rows = [x for x in wb[sheet].iter_rows(min_row=5, values_only=True) if x[0]]
        r.append(pd.DataFrame({"payer": "KBP", "member": [str(x[0]) for x in rows], "run": tag, "tin": [tin(x[1]) for x in rows]}))
    a = pd.read_csv(f("pmh_attribution"), dtype=str)
    r.append(pd.DataFrame({"payer": "PMH", "member": a.memberId, "run": np.where(a.run == "FINAL", "F25", "R26"), "tin": a.tin.map(tin)}))
    return pd.concat(r, ignore_index=True)


def roster():
    wb = openpyxl.load_workbook(f("lpn_primary_care_roster"), read_only=True)
    rows = [x for x in wb.active.iter_rows(min_row=2, values_only=True) if x[0]]
    return pd.DataFrame({"npi": [str(x[0]) for x in rows], "practice": [x[3] for x in rows],
                         "tin": [str(x[4]).replace("-", "") for x in rows], "start": pd.to_datetime([x[5] for x in rows]),
                         "end": pd.to_datetime([x[6] if x[6] else "2099-12-31" for x in rows])})


def at_practice(lines, ros):
    """Each line's practice: the roster row for its rendering NPI in force on its date of service."""
    x = lines.reset_index().merge(ros[["npi", "practice", "start", "end"]], on="npi", how="inner")
    x = x[(x.svc >= x.start) & (x.svc <= x.end)]
    return x.set_index("index").practice


def rate(members, cl, mm, cap=250000.0):
    """Per practice capped cost and member months for a {(payer, member): practice} frame."""
    tot = cl.groupby(["payer", "member"]).amt.sum()
    df = members.copy()
    df["cost"] = [min(cap, tot.get(k, 0.0)) for k in zip(df.payer, df.member)]
    df["mm"] = [mm.get(k, 0) for k in zip(df.payer, df.member)]
    return df.groupby("practice")[["cost", "mm"]].sum()


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    cl = claims()
    cov = coverage()
    rn = runs()
    ros = roster()
    tin2 = dict(zip(ros.tin, ros.practice))
    rn["practice"] = rn.tin.map(tin2)
    v("every attribution TIN maps to a roster practice", rn.practice.notna().all())
    qual = set(pd.read_csv(f("qualifying_primary_care"), dtype=str).code)
    cf = pd.read_csv(f("payer_completion_factors"), dtype=str)
    cfd = {(r.payer, int(r.incurred_month[5:7])): float(r.completion_factor) for r in cf.itertuples()}

    # 2025 measure on the final runs, benchmark and threshold
    f25 = rn[rn.run == "F25"][["payer", "member", "practice"]]
    c25 = cl[(cl.svc.dt.year == 2025) & (cl.fp <= TS(2026, 3, 31))]
    F = rate(f25, c25, months(cov, 2025, 12))
    F["pm"] = F.cost / F.mm
    bench = F.pm.map(lambda x: round(round(x, 2) * 1.052, 2))     # the standard's section 3.4
    thr = bench * 0.98
    cents = [int(round(round(x, 2) * 100)) for x in F.pm]
    v("no benchmark on a half cent: no 2025 measure's cents times 1052 end in 500",
      all((c_ * 1052) % 1000 != 500 for c_ in cents))
    v("no threshold on a half cent: no benchmark's cents times 98 end in 50",
      all((int(round(b_ * 100)) * 98) % 100 != 50 for b_ in bench))
    # the October runs' interim measure
    r26 = rn[rn.run == "R26"][["payer", "member", "practice"]]
    c26 = cl[(cl.svc.dt.year == 2026) & (cl.svc <= TS(2026, 8, 31)) & (cl.fp <= TS(2026, 9, 30))].copy()
    c26["amt"] = c26.amt / [cfd[(p, m)] for p, m in zip(c26.payer, c26.svc.dt.month)]
    I = rate(r26, c26, months(cov, 2026, 8))
    I["pm"] = I.cost / I.mm
    # the 2025 attribution re-run at the October run's cut, from the 2025 professional claims
    q = cl[(cl.typ == "PROF") & cl.code.isin(qual) & (cl.svc.dt.year == 2025) & (cl.svc <= TS(2025, 8, 31))
           & (cl.fp <= TS(2025, 9, 30))].copy()
    q["practice"] = at_practice(q, ros)
    q = q.dropna(subset=["practice"])
    days = q.groupby(["payer", "member", "practice"]).svc.agg(["nunique", "max"]).reset_index()
    days = days.sort_values(["payer", "member", "nunique", "max", "practice"], ascending=[True, True, False, False, True])
    aug = days.drop_duplicates(["payer", "member"])[["payer", "member", "practice"]]
    c25a = cl[(cl.svc.dt.year == 2025) & (cl.svc <= TS(2025, 8, 31)) & (cl.fp <= TS(2026, 3, 31))]
    A = rate(aug, c25a, months(cov, 2025, 8))
    A["pm"] = A.cost / A.mm
    R = F.pm / A.pm
    proj = I.pm * R
    enter = sorted(k for k in proj.index if proj[k] <= thr[k])
    v("the elections recompute: %d practices enter" % len(enter), enter == sorted(figs["call"]["enter"]), str(enter))
    v("every benchmark and threshold recomputes to the cent",
      all(abs(round(bench[k], 2) - figs["practices"][k]["benchmark"]) < 0.006 and
          abs(round(thr[k], 2) - figs["practices"][k]["threshold"]) < 0.006 for k in proj.index))
    v("every 2025 measure recomputes to the cent", all(abs(round(F.pm[k], 2) - figs["practices"][k]["f2025"]) < 0.006 for k in proj.index))
    v("every run-out and projection recomputes", all(abs(R[k] - figs["practices"][k]["runout"]) < 6e-5 and
                                                   abs(round(proj[k], 2) - figs["practices"][k]["projected"]) < 0.006 for k in proj.index))
    gap = (proj / thr - 1).abs().min()
    v("no practice within 4.5 per cent of its threshold", gap >= 0.045, "%.4f" % gap)
    dflt = sorted(k for k in proj.index if I.pm[k] <= thr[k])
    v("the default path (the interim measure as it stands) enters %s" % ", ".join(x.split()[0] for x in dflt),
      dflt == sorted(figs["steps"]["default_enter"]))
    pooled = (F.cost.sum() / F.mm.sum()) / (A.cost.sum() / A.mm.sum())
    v("the pooled run-out recomputes", abs(pooled - figs["steps"]["pooled_runout"]) < 0.0006, "%.4f" % pooled)

    # ask A: the level each payer paid, read from the allowed amount against its schedule for the visit's setting
    wb = openpyxl.load_workbook(f("payer_em_fee_schedules"), read_only=True)
    sched = {}
    for ws, py in zip(wb.worksheets, ("MLH", "KBP", "PMH")):
        for x in ws.iter_rows(min_row=5, values_only=True):
            if x[0] and str(x[0]).startswith("992"):
                sched[(py, str(x[0]))] = (float(x[2]), float(x[3]) if x[3] is not None else None)
    em = cl[(cl.typ == "PROF") & cl.code.isin(["99211", "99212", "99213", "99214", "99215"]) & (cl.svc.dt.year == 2026)
            & (cl.svc <= TS(2026, 8, 31))].copy()
    em["practice"] = at_practice(em, ros)
    em = em.dropna(subset=["practice"])
    fac = em.pos.isin(["19", "22"]) | ((em.payer == "PMH") & em.pos.isin(["02", "10"]))
    r5 = np.array([sched[(p, "99215")][1 if fa else 0] for p, fa in zip(em.payer, fac)])
    paid5 = (em.code == "99215") & ((np.abs(em.amt - r5) < 0.005) | (np.abs(2 * em.amt - r5) < 0.01))
    share = (100 * paid5.groupby(em.practice).mean()).round(1)
    v("ask A: all 13 level 5 shares recompute", all(abs(share[k] - figs["ask_a"][k]) < 1e-9 for k in share.index),
      str(share.to_dict()))
    # ask B: the remittances by the month each line covers, the standard's fees only
    rem = []
    m = pd.read_csv(f("mlh_care_coordination"), dtype=str)
    rem.append(pd.DataFrame({"payer": "MLH", "tin": m.PRACTICE_TIN, "cov": m.COV_MO.str[4:6].astype(int),
                             "n": m.MBR_CNT.astype(int), "amt": m.PMT_AMT.astype(float)}))
    wb = openpyxl.load_workbook(f("KBP_CCF_REMIT"), read_only=True)
    rows = [x for x in wb.active.iter_rows(min_row=2, values_only=True) if x[0]]
    rem.append(pd.DataFrame({"payer": "KBP", "tin": [str(x[2]).replace("-", "") for x in rows],
                             "cov": [int(str(x[3])[5:7]) for x in rows], "n": [int(x[4]) for x in rows],
                             "amt": [float(x[5]) for x in rows]}))
    pm = pd.read_csv(f("pmh_ccf_payments"), dtype=str)
    rem.append(pd.DataFrame({"payer": "PMH", "tin": pm.tin.str.replace("-", ""),
                             "cov": pm.paymentRef.str.extract(r"-2026(\d\d)-")[0].astype(int),
                             "n": pm.memberCount.astype(int), "amt": pm.amount.astype(float)}))
    rem = pd.concat(rem, ignore_index=True)
    std = pdf("lpn_performance_standard")
    fee = {}
    for py, name in (("MLH", "Merrinlake Health Plan"), ("KBP", "Kesselcrest Benefit Partners"), ("PMH", "Pemberglen Mutual Health")):
        fee[py] = float(re.search(re.escape(name) + r" USD (\d+\.\d\d)", std).group(1))
    rem = rem[np.abs(rem.n * rem.payer.map(fee) - rem.amt) < 0.005]
    rem = rem[rem["cov"] <= 9]
    rem["practice"] = rem.tin.map(tin2)
    rem["q"] = (rem["cov"] - 1) // 3 + 1
    fees = rem.groupby(["practice", "q"]).amt.sum().round(2)
    v("ask B: all 39 fees recompute to the cent", len(fees) == 39 and all(abs(fees[(k, q_)] - figs["ask_b"]["%s|Q%d" % (k, q_)]) < 0.005
                                                                         for k, q_ in fees.index))

    # the golden workbook carries the same figures
    wb = openpyxl.load_workbook(os.path.join(GD, "two_sided_track_elections_2027.xlsx"), data_only=True)
    ws = wb["Elections 2027"]
    rows = [x for x in ws.iter_rows(min_row=5, values_only=True) if x[0]]
    v("workbook: the elections sheet carries every benchmark, threshold and election",
      len(rows) == 13 and all(abs(x[3] - round(bench[x[0]], 2)) < 0.006 and abs(x[4] - round(thr[x[0]], 2)) < 0.006
                              and (x[9] == "Two-sided") == (x[0] in enter) for x in rows))
    la = [x for x in wb["Level 5 visits"].iter_rows(min_row=5, values_only=True) if x[0] and x[0] != "Network"]
    v("workbook: the level 5 sheet carries the 13 shares", all(abs(100 * x[3] - share[x[0]]) < 1e-6 for x in la))
    fb = [x for x in wb["Care coordination fees"].iter_rows(min_row=5, values_only=True) if x[0] and x[0] != "Network"]
    v("workbook: the fees sheet carries the 39 fees", all(abs(x[q_] - fees[(x[0], q_)]) < 0.005 for x in fb for q_ in (1, 2, 3)))
    sub = open(os.path.join(TASK, "submission.md")).read()
    v("submission: every benchmark and threshold in block 4 as recomputed",
      all(("benchmark USD {:,.2f}, threshold USD {:,.2f}".format(bench[k], thr[k])) in sub for k in proj.index))
    v("submission: the nine named in block 1", all(k.split()[0] in sub.split("## 2.")[0] for k in enter))
    print("\n%d checks, %d failed" % (OK[0], len(BAD)))
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
