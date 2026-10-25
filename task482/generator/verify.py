"""The independent verifier: reads only the shipped bundle (target/), the golden deliverables and figures.json, on its
own code path (pandas joins and group-bys, pdfplumber for the documents, no import of golden.py), and recomputes the
elections, every benchmark and threshold, the members in a stay running at the cut, the ask and the write-up's
figures.

    python3 task482/generator/verify.py
"""
import json
import os
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
CAP = 250000.0
EM = ["99211", "99212", "99213", "99214", "99215"]


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
    a = pd.DataFrame({"payer": "MLH", "member": m.MBR_ID, "typ": m.CLM_TYP.replace({"PHRM": "RX", "OUTP": "FAC"}),
                      "svc": pd.to_datetime(m.SVC_FROM_DT), "end": pd.to_datetime(m.SVC_THRU_DT), "fp": m.fp,
                      "paid": pd.to_datetime(m.PD_DT), "code": m.PROC_CD, "mod": m.PROC_MOD, "pos": m.POS_CD, "rev": m.REV_CD,
                      "npi": m.REND_NPI, "amt": m.ALLOWED_AMT.astype(float), "clm": "M" + m.CLM_ID})
    k = pd.read_csv(f("KBP_CLAIMS"), sep="|", dtype=str, keep_default_na=False)
    k["key"] = k.CLAIM_NO.str.split("-").str[0]
    k["pd"] = pd.to_datetime(k.PAID_DATE, format="%m/%d/%Y")
    k["fp"] = k.groupby("key").pd.transform("min")
    k = k[k.CLAIM_STATUS == "P"]
    typ = np.where(k.CLAIM_FORM == "1500", "PROF", np.where(k.CLAIM_FORM == "NCPDP", "RX",
                                                            np.where(k.BILL_TYPE.str[:3] == "011", "INPT", "FAC")))
    b = pd.DataFrame({"payer": "KBP", "member": k.MEMBER_NO, "typ": typ, "svc": pd.to_datetime(k.FIRST_DOS, format="%m/%d/%Y"),
                      "end": pd.to_datetime(k.LAST_DOS, format="%m/%d/%Y"), "fp": k.fp, "paid": k.pd, "code": k.PROCEDURE,
                      "mod": k.MODIFIER, "pos": k.PLACE_OF_SVC, "rev": k.REVENUE, "npi": k.RENDERING_PROV_NPI,
                      "amt": k.ALLOWED_CENTS.astype(float) / 100, "clm": "K" + k.CLAIM_NO})
    j = pd.DataFrame(json.load(open(f("pmh_partner_claims")))["records"])
    j["fp"] = pd.to_datetime(j.groupby("claimId").adjudicated.transform("min"))
    j = j.sort_values("version").drop_duplicates("claimId", keep="last")
    tmap = {"professional": "PROF", "pharmacy": "RX", "institutional_inpatient": "INPT", "institutional_outpatient": "FAC"}
    t = pd.DataFrame({"payer": "PMH", "member": j.memberId, "typ": j["type"].map(tmap), "svc": pd.to_datetime(j.serviceStart),
                      "end": pd.to_datetime(j.serviceEnd), "fp": j.fp, "paid": pd.to_datetime(j.adjudicated),
                      "code": j.cpt.fillna(""), "mod": j["modifier"].fillna("") if "modifier" in j else "",
                      "pos": j.pos.fillna(""), "rev": j.revenueCode.fillna(""), "npi": j.renderingNpi.fillna(""),
                      "amt": j.allowed.astype(float), "clm": "P" + j.claimId})
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
    r = ros[["npi", "practice", "start", "end"]].rename(columns={"start": "r_start", "end": "r_end"})
    x = lines.reset_index().merge(r, on="npi", how="inner")
    x = x[(x.svc >= x.r_start) & (x.svc <= x.r_end)]
    return x.set_index("index").practice


def rate(members, cl, mm, cap=CAP):
    """Per practice capped cost and member months for a {(payer, member): practice} frame."""
    tot = cl.groupby(["payer", "member"]).amt.sum()
    df = members.copy()
    df["cost"] = [min(cap, tot.get(k, 0.0)) for k in zip(df.payer, df.member)]
    df["mm"] = [mm.get(k, 0) for k in zip(df.payer, df.member)]
    return df.groupby("practice")[["cost", "mm"]].sum()


def running(cl, year):
    """The members in a long stay still running at the year's cut, by this verifier's own reading: inpatient hospital
    visits (place of service 21, the neonatal, critical and hospital care codes) on consecutive days to within ten days
    of 31 August, paid by 30 September, with no inpatient facility claim paid by then covering them; past the cap where
    the days to the cut, at the lowest per-day allowed of the closed stays of 30 days or more of the same kind, reach it."""
    cut, paid = TS(year, 8, 31), TS(year, 9, 30)
    inpt = cl[cl.typ == "INPT"].copy()
    inpt["los"] = (inpt.end - inpt.svc).dt.days
    long_ = inpt[inpt.los >= 30]
    kind_of = {"0174": "NICU", "0200": "ICU"}
    low = {}
    for r in long_.itertuples():
        kd = kind_of.get(r.rev)
        if kd:
            low[kd] = min(low.get(kd, 1e12), r.amt / r.los)
    codes = {"99468": "NICU", "99469": "NICU", "99291": "ICU", "99223": "MED", "99232": "MED", "99238": "MED", "99239": "ICU"}
    pr = cl[(cl.typ == "PROF") & (cl.pos == "21") & cl.code.isin(list(codes)) & (cl.svc.dt.year == year) & (cl.svc <= cut)
            & (cl.fp <= paid)]
    fac = inpt[(inpt.svc.dt.year == year) & (inpt.fp <= paid)]
    out = {}
    for key, g in pr.groupby(["payer", "member"]):
        days = sorted(set(g.svc))
        if (cut - days[-1]).days > 10:
            continue
        first = days[-1]
        for d in reversed(days[:-1]):
            if (first - d).days > 2:
                break
            first = d
        ff = fac[(fac.payer == key[0]) & (fac.member == key[1])]
        if ((ff.svc <= first + pd.Timedelta(days=1)) & (ff.end >= days[-1])).any():
            continue
        kinds = set(g[g.svc >= first].code.map(codes))
        kd = "NICU" if "NICU" in kinds else ("ICU" if "ICU" in kinds else "MED")
        n = (cut - first).days + 1
        if kd in low and n * low[kd] >= CAP:
            out[key] = (kd, first, n)
    return out, low


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    par = figs["parameters"]
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
    std = pdf("lpn_performance_standard")
    v("the standard states the cap and the factors' large-claim rule", "USD 250,000" in std and
      "over USD 100,000 are left out of the lag study" in std)

    # the members in a long stay running at each cut
    h26, low = running(cl, 2026)
    h25, _ = running(cl, 2025)
    v("the lowest per-day amounts of the closed long stays are USD 4,580 (neonatal) and 6,380 (intensive)",
      {k: round(x, 2) for k, x in low.items()} == {"NICU": 4580.0, "ICU": 6380.0}, str(low))
    r26 = rn[rn.run == "R26"][["payer", "member", "practice"]]
    rmap = {(a_, b_): c_ for a_, b_, c_ in zip(r26.payer, r26.member, r26.practice)}
    held = {}
    for key in h26:
        held[rmap[key]] = held.get(rmap[key], 0) + 1
    v("seven members in a long stay running at the 2026 cut, past the cap: %s" % held,
      held == dict(par["steps"]["held"]), str(h26))
    v("no long stay runs at the 2025 cut", not h25, str(h25))

    # 2025 measure on the final runs, benchmark and threshold
    f25 = rn[rn.run == "F25"][["payer", "member", "practice"]]
    c25 = cl[(cl.svc.dt.year == 2025) & (cl.fp <= TS(2026, 3, 31))]
    mm25 = months(cov, 2025, 12)
    F0 = rate(f25, c25, mm25)
    F0["pm"] = F0.cost / F0.mm
    bench = F0.pm.map(lambda x: round(round(x, 2) * 1.052, 2))     # the standard's section 3.4
    thr = bench * 0.98
    cents = [int(round(round(x, 2) * 100)) for x in F0.pm]
    v("no benchmark on a half cent: no 2025 measure's cents times 1052 end in 500", all((c_ * 1052) % 1000 != 500 for c_ in cents))
    v("no threshold on a half cent: no benchmark's cents times 98 end in 50",
      all((int(round(b_ * 100)) * 98) % 100 != 50 for b_ in bench))
    keep = lambda df, h: df[[k not in h for k in zip(df.payer, df.member)]]
    F = rate(keep(f25, h25), c25, mm25)
    # the October runs' interim measure, the held members out
    c26 = cl[(cl.svc.dt.year == 2026) & (cl.svc <= TS(2026, 8, 31)) & (cl.fp <= TS(2026, 9, 30))].copy()
    c26["amt"] = c26.amt / [cfd[(p, m)] for p, m in zip(c26.payer, c26.svc.dt.month)]
    mm26 = months(cov, 2026, 8)
    I = rate(r26, c26, mm26)
    I["pm"] = I.cost / I.mm
    Ir = rate(keep(r26, h26), c26, mm26)
    # the 2025 attribution re-run at the October run's cut, from the 2025 professional claims
    q = cl[(cl.typ == "PROF") & cl.code.isin(qual) & (cl.svc.dt.year == 2025) & (cl.svc <= TS(2025, 8, 31))
           & (cl.fp <= TS(2025, 9, 30))].copy()
    q["practice"] = at_practice(q, ros)
    q = q.dropna(subset=["practice"])
    days = q.groupby(["payer", "member", "practice"]).svc.agg(["nunique", "max"]).reset_index()
    days = days.sort_values(["payer", "member", "nunique", "max", "practice"], ascending=[True, True, False, False, True])
    aug = days.drop_duplicates(["payer", "member"])[["payer", "member", "practice"]]
    c25a = cl[(cl.svc.dt.year == 2025) & (cl.svc <= TS(2025, 8, 31)) & (cl.fp <= TS(2026, 3, 31))]
    A = rate(keep(aug, h25), c25a, months(cov, 2025, 8))
    R = (F.cost / F.mm) / (A.cost / A.mm)
    mm_year = months(cov, 2026, 12)
    proj, runout_only = {}, {}
    for k in thr.index:
        n_held = held.get(k, 0)
        mrest = Ir.mm[k] * F.mm[k] / A.mm[k]
        add = sum(mm_year.get(key, 0) for key in h26 if rmap[key] == k)
        proj[k] = ((Ir.cost[k] / Ir.mm[k]) * R[k] * mrest + CAP * n_held) / (mrest + add)
        runout_only[k] = I.pm[k] * R[k]
    enter = sorted(k for k in thr.index if proj[k] <= thr[k])
    v("the elections recompute: %d practices enter" % len(enter), enter == sorted(figs["call"]["enter"]), str(enter))
    v("every benchmark and threshold recomputes to the cent",
      all(abs(round(bench[k], 2) - par["benchmark"][k]) < 0.006 and abs(round(thr[k], 2) - par["threshold"][k]) < 0.006
          for k in thr.index))
    v("every projected position recomputes to a tenth of a per cent",
      all(abs(100 * (proj[k] / thr[k] - 1) - par["position_pct"][k]) < 0.051 for k in thr.index))
    gap = min(abs(proj[k] / thr[k] - 1) for k in thr.index)
    v("no practice within 4.5 per cent of its threshold", gap >= 0.045, "%.4f" % gap)
    dflt = sorted(k for k in thr.index if I.pm[k] <= thr[k])
    v("the interim measure as it stands enters %s" % ", ".join(x.split()[0] for x in dflt),
      dflt == sorted(par["steps"]["default_enter"]))
    ro = sorted(k for k in thr.index if runout_only[k] <= thr[k])
    v("the run-out alone enters %d, the held members' practices among them" % len(ro),
      ro == sorted(par["steps"]["runout_enter"]) and all(k in ro for k in held))

    # ask A: the level each payer paid, read from the allowed amount against its schedule for the visit's setting
    wb = openpyxl.load_workbook(f("payer_em_fee_schedules"), read_only=True)
    sched = {}
    for ws, py in zip(wb.worksheets, ("MLH", "KBP", "PMH")):
        for x in ws.iter_rows(min_row=5, values_only=True):
            if x[0] and str(x[0]).startswith("992"):
                sched[(py, str(x[0]))] = (float(x[2]), float(x[3]) if x[3] is not None else None)
    prof26 = cl[(cl.typ == "PROF") & (cl.svc.dt.year == 2026) & (cl.svc <= TS(2026, 8, 31))]
    em = prof26[prof26.code.isin(EM)].copy()
    em["practice"] = at_practice(em, ros)
    em = em.dropna(subset=["practice"])
    side = prof26[~prof26.code.isin(EM) & ~prof26.code.isin(qual) & (prof26.code != "")]
    beside = set(zip(side.payer, side.member, side.npi, side.svc))
    claim_amt = prof26.groupby("clm").amt.sum()          # a claim's allowed amount: every line, adjustments included
    em["camt"] = em.clm.map(claim_amt)
    fac = em.pos.isin(["19", "22"]) | ((em.payer == "PMH") & em.pos.isin(["02", "10"]))
    lv = []
    for r, fa in zip(em.itertuples(), fac):
        amt = r.camt * (2 if (r.payer == "MLH" and r.mod == "25" and (r.payer, r.member, r.npi, r.svc) in beside) else 1)
        hit = [i for i, c_ in enumerate(EM) if abs(sched[(r.payer, c_)][1 if fa else 0] - amt) < 0.005]
        lv.append(hit[0] + 1 if hit else EM.index(r.code) + 1)
    em["lvl"] = lv
    share = (100 * (em.lvl == 5).groupby(em.practice).mean()).round(1)
    v("ask A: all 13 level 5 shares recompute", all(abs(share[k] - figs["ask_a"][k]) < 1e-9 for k in share.index),
      str(share.to_dict()))
    v("ask A: every E&M claim's allowed amount matches a level's rate for its setting, after Merrinlake's halving",
      all(any(abs(sched[(p_, c_)][1 if fa else 0] - a_ * (2 if (p_ == "MLH" and m_ == "25" and k_ in beside) else 1)) < 0.005
              for c_ in EM) for p_, m_, a_, fa, k_ in zip(em.payer, em["mod"], em.camt, fac,
                                                          zip(em.payer, em.member, em.npi, em.svc))))
    kb = em[em.payer == "KBP"]
    v("ask A: every Kesselcrest E&M line carries its code's rate, and %d of its 99215 claims total its 99214 rate" % int(
        ((kb.code == "99215") & (kb.lvl == 4)).sum()),
      all(abs(sched[("KBP", c_)][1 if fa else 0] - a_) < 0.005 for c_, a_, fa in zip(kb.code, kb.amt, fac[kb.index]))
      and ((kb.code == "99215") & (kb.lvl == 4)).sum() > 300)
    v("ask A: one established-patient visit a member a day with the practices' clinicians",
      not em.groupby(["payer", "member", "svc"]).size().gt(1).any())
    # the golden workbook carries the same figures
    wb = openpyxl.load_workbook(os.path.join(GD, "two_sided_track_elections_2027.xlsx"), data_only=True)
    ws = wb["Elections 2027"]
    rows = [x for x in ws.iter_rows(min_row=5, values_only=True) if x[0]]
    v("workbook: the elections sheet carries every benchmark, threshold, held count and election",
      len(rows) == 13 and all(abs(x[3] - round(bench[x[0]], 2)) < 0.006 and abs(x[4] - round(thr[x[0]], 2)) < 0.006
                              and (x[7] or 0) == held.get(x[0], 0) and (x[10] == "Two-sided") == (x[0] in enter) for x in rows))
    la = [x for x in wb["Level 5 visits"].iter_rows(min_row=5, values_only=True) if x[0] and x[0] != "Network"]
    v("workbook: the level 5 sheet carries the 13 shares", all(abs(round(100 * x[3], 1) - share[x[0]]) < 1e-6 for x in la))
    v("workbook: three sheets and the notes, no fees sheet", wb.sheetnames == ["Elections 2027", "Level 5 visits", "Notes"],
      str(wb.sheetnames))
    sub = open(os.path.join(TASK, "submission.md")).read()
    b4 = sub.split("## 4.")[1]
    v("submission: every election in block 4 as recomputed",
      all(("- %s: %s" % (k, "two-sided" if k in enter else "one-sided")) in b4 for k in thr.index))
    v("submission: the eight named in block 1", all(k.split()[0] in sub.split("## 2.")[0] for k in enter))
    v("submission: the two held practices' thresholds in block 2", all("USD {:,.2f}".format(thr[k]) in sub.split("## 3.")[0]
                                                                         for k in held))
    print("\n%d checks, %d failed" % (OK[0], len(BAD)))
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
