"""Every rung, the golden and the asks, computed from the files under target/ alone (no import of the
world or the generator's truth)."""
import json
import os
import re
import numpy as np
import pandas as pd

APPX_A = {"V253", "V254", "V255", "V256", "V331", "V332", "V337"}
REVISION = {"V264", "V347"}
ELECTIVE = {"11", "12", "13"}
EMERGENCY = {"21", "22", "23", "24", "28", "2A", "2B", "2C", "2D"}
COEF = None
FLOOR = 14.5
VOLUME = 1250
CALL_FROM, CALL_TO = pd.Timestamp("2023-04-01"), pd.Timestamp("2025-03-31")
FY26_FROM, FY26_TO = pd.Timestamp("2025-04-01"), pd.Timestamp("2026-03-31")
SNAP = pd.Timestamp("2026-03-31")
DUR = {"Less than 3 months": 1, "3 to 12 months": 2, "1 to 2 years": 3, "More than 2 years": 4}


def coef_from_policy(target):
    """Appendix B as the board files it (read from the PDF text)."""
    from io_util import pdf_text
    t = pdf_text(os.path.join(target, "spinal_contracting_policy_2027-28.pdf"))
    def grab(label):
        m = re.search(re.escape(label) + r"\s+([+-]?[0-9.]+)", t)
        return float(m.group(1))
    return dict(intercept=grab("Constant"), pre=grab("Per point of pre-operative ODI score, measured from 45"),
                age=grab("Per year of age on admission, measured from 55"), female=grab("Female"),
                smoker=grab("Current smoker"), prev=grab("Previous lumbar spinal surgery"),
                symp=grab("Symptoms for more than 12 months"),
                disc=grab("Disc herniation (primary diagnosis M51.1 or M51.2)"))


def load(target):
    P = lambda f: os.path.join(target, f)
    s = pd.read_csv(P("apc_spells_lumbar_cohort_2022-26.csv"), dtype=str, keep_default_na=False)
    for c in ("admission_date", "discharge_date", "procedure_date"):
        s[c] = pd.to_datetime(s[c], format="%d/%m/%Y", errors="coerce")
    s["sus_submitted"] = pd.to_datetime(s.sus_submitted)
    s["age_on_admission"] = s.age_on_admission.astype(int)
    prov = pd.read_csv(P("provider_reference_2026-09.csv"), dtype=str, keep_default_na=False)
    # one provider per hospital: a successor code reports under its predecessor's site
    site = dict(zip(prov.provider_code, prov.provider_code))
    for r in prov.itertuples():
        if r.predecessor_provider_code:
            site[r.provider_code] = r.predecessor_provider_code
    s["unit"] = s.provider_code.map(site)
    old = pd.read_excel(P("mossgill_spinal_proms_2022-04_to_2025-03.xlsx"), skiprows=3, dtype=object)
    odi = ["ODI%d" % i for i in range(1, 11)]
    o = pd.DataFrame({"ref": old.PatientRef.astype(str), "site": old.Site.astype(str),
                      "sup_op": pd.to_datetime(old.OperationDate), "completed": pd.to_datetime(old.Completed),
                      "qtype": np.where(old.Questionnaire == "Pre-operative", "pre", "m12"),
                      "yob": old.BirthYear.astype(int), "sex": np.where(old.Sex == "F", 2, 1),
                      "smoker": old.Smoker.map({"Yes": 1, "No": 0}), "prev": old.PreviousSpinalSurgery.map({"Yes": 1, "No": 0}),
                      "dur": old.SymptomDuration.map(DUR),
                      "n": old[odi].notna().sum(axis=1).astype(int),
                      "tot": old[odi].apply(pd.to_numeric).sum(axis=1).astype(float)})
    new = pd.read_csv(P("mossgill_spinal_proms_2025-04_to_2026-09.csv"), dtype=str, keep_default_na=False)
    n = pd.DataFrame({"ref": new.patient_ref, "site": new.site_code,
                      "sup_op": pd.to_datetime(new.operation_date, format="%d/%m/%Y"),
                      "completed": pd.to_datetime(new.completed_date), "qtype": np.where(new.questionnaire == "PREOP", "pre", "m12"),
                      "yob": new.birth_year.astype(int), "sex": new.sex.astype(int),
                      "smoker": new.smoker.map({"Y": 1, "N": 0}), "prev": new.previous_spinal_surgery.map({"Y": 1, "N": 0}),
                      "dur": pd.to_numeric(new.symptom_duration, errors="coerce"),
                      "n": new.odi_sections_answered.astype(int), "tot": new.odi_raw_score.astype(float)})
    q = pd.concat([o, n], ignore_index=True)
    q["score"] = np.where(q.n >= 8, q.tot / (5.0 * q.n) * 100.0, np.nan)
    link = pd.read_csv(P("mossgill_nhs_number_link_2026-09.csv"), dtype=str, keep_default_na=False)
    q = q.merge(link[["patient_ref", "pseudo_nhs_number"]].rename(columns={"patient_ref": "ref", "pseudo_nhs_number": "pseudo"}),
                on="ref", how="left")
    q["pseudo"] = q.pseudo.fillna("")
    deaths = pd.read_csv(P("cohort_deaths_linked_2026-09.csv"), dtype=str)
    deaths["date_of_death"] = pd.to_datetime(deaths.date_of_death)
    cap = pd.read_excel(P("spinal_capacity_returns_2027-28.xlsx"), skiprows=4)
    return dict(s=s, prov=prov, site=site, q=q, link=link, deaths=deaths, cap=cap)


def dedup(s):
    """A spell submitted more than once: its latest submission stands."""
    s = s.sort_values(["sus_submitted", "spell_id"])
    return s.drop_duplicates(["pseudo_nhs_number", "provider_code", "admission_date"], keep="last")


def index_ops(s):
    s = dedup(s)
    a = s[s.admission_method.isin(ELECTIVE) & s.primary_procedure.isin(APPX_A)].copy()
    allA = s[s.primary_procedure.isin(APPX_A)][["pseudo_nhs_number", "procedure_date"]]
    prior = a[["spell_id", "pseudo_nhs_number", "procedure_date"]].merge(allA, on="pseudo_nhs_number", suffixes=("", "_o"))
    gap = (prior.procedure_date - prior.procedure_date_o).dt.days
    bad = set(prior[(gap > 0) & (gap <= 365)].spell_id)
    return a[~a.spell_id.isin(bad)].copy(), s


def eligible(L, frm=CALL_FROM, to=CALL_TO):
    global COEF
    ops, s = index_ops(L["s"])
    m = ops[(ops.procedure_date >= frm) & (ops.procedure_date <= to)].copy()
    q = L["q"]
    pre = q[(q.qtype == "pre") & q.score.notna() & (q.pseudo != "")]
    x = m[["spell_id", "pseudo_nhs_number", "procedure_date"]].merge(pre, left_on="pseudo_nhs_number", right_on="pseudo")
    gap = (x.procedure_date - x.completed).dt.days
    x = x[(gap >= 0) & (gap <= 89)].sort_values(["spell_id", "completed"]).drop_duplicates("spell_id", keep="last")
    m = m.merge(x[["spell_id", "score", "smoker", "prev", "dur"]].rename(columns={"score": "pre"}), on="spell_id")
    dd = L["deaths"].groupby("pseudo_nhs_number").date_of_death.min()
    dod = m.pseudo_nhs_number.map(dd)
    m = m[~(dod.notna() & (dod <= m.procedure_date + pd.Timedelta(days=365)))].copy()
    m12 = q[(q.qtype == "m12") & q.score.notna() & (q.pseudo != "")]
    y = m[["spell_id", "pseudo_nhs_number", "procedure_date"]].merge(m12, left_on="pseudo_nhs_number", right_on="pseudo")
    g2 = (y.completed - y.procedure_date).dt.days
    y = y[(g2 >= 336) & (g2 <= 448)].sort_values(["spell_id", "completed"]).drop_duplicates("spell_id", keep="first")
    m = m.merge(y[["spell_id", "score"]].rename(columns={"score": "post"}), on="spell_id", how="left")
    m["resp"] = m.post.notna()
    m["chg"] = m.pre - m.post
    C = COEF
    m["E"] = (C["intercept"] + C["pre"] * (m.pre - 45) + C["age"] * (m.age_on_admission - 55) + C["female"] * (m.sex == "2")
              + C["smoker"] * m.smoker + C["prev"] * m.prev + C["symp"] * (m.dur >= 3)
              + C["disc"] * m.primary_diagnosis.isin(["M511", "M512"]))
    m["d"] = m.chg - m.E
    return m, s


def later_flags(m, s):
    """What happened to each patient after the operation, from the later spells in the same extract."""
    later = s[["pseudo_nhs_number", "unit", "admission_date", "admission_method", "primary_procedure"]].rename(
        columns={"unit": "unit_l", "admission_date": "admission_date_l", "admission_method": "admission_method_l",
                 "primary_procedure": "primary_procedure_l"})
    x = m[["spell_id", "pseudo_nhs_number", "unit", "admission_date", "discharge_date", "procedure_date"]].merge(
        later, on="pseudo_nhs_number")
    x = x[x.admission_date_l > x.admission_date]
    em = x.admission_method_l.isin(EMERGENCY)
    since_dis = (x.admission_date_l - x.discharge_date).dt.days
    since_op = (x.admission_date_l - x.procedure_date).dt.days
    f = {}
    f["f30"] = set(x[em & (since_dis > 0) & (since_dis <= 30)].spell_id)
    f["f90"] = set(x[em & (since_dis > 0) & (since_dis <= 90)].spell_id)
    f["f90op"] = set(x[em & (since_op > 0) & (since_op <= 90)].spell_id)
    f["f365"] = set(x[em & (since_op > 0) & (since_op <= 365)].spell_id)
    f["same"] = set(x[em & (since_dis > 0) & (since_dis <= 90) & (x.unit_l == x.unit)].spell_id)
    f["reop"] = set(x[x.primary_procedure_l.isin(REVISION) & (since_op > 0) & (since_op <= 365)].spell_id)
    f["nonel"] = set(x[(em | (x.admission_method_l == "81")) & (since_op >= 0) & (since_op <= 90)].spell_id)
    f["any"] = set(x[(since_op > 0) & (since_op <= 365)].spell_id)
    for k, v in f.items():
        m[k] = m.spell_id.isin(v)
    return m


def cell(m, flag, netE):
    out = {}
    for u, g in m.groupby("unit"):
        tot = 0.0
        for c in (False, True):
            cc = g[g[flag] == c]
            if (~cc.resp).sum() and cc.resp.sum():
                tot += cc[cc.resp].d.sum() + cc[cc.resp].d.mean() * (~cc.resp).sum()
            else:
                tot += cc[cc.resp].d.sum() + (g[g.resp].d.mean() * (~cc.resp).sum() if (~cc.resp).sum() else 0)
        out[u] = netE + tot / len(g)
    return out


XCOLS = ["pre", "age_on_admission", "fem", "smoker", "prev", "symp", "disc"]


def reg_imp(m, extra, netE):
    out = {}
    m = m.assign(fem=(m.sex == "2").astype(float), symp=(m.dur >= 3).astype(float),
                 disc=m.primary_diagnosis.isin(["M511", "M512"]).astype(float))
    for u, g in m.groupby("unit"):
        cols = list(extra) + XCOLS
        r = g[g.resp]
        A = np.column_stack([np.ones(len(r))] + [r[c].astype(float) for c in cols])
        b, *_ = np.linalg.lstsq(A, r.d.values, rcond=None)
        n = g[~g.resp]
        B = np.column_stack([np.ones(len(n))] + [n[c].astype(float) for c in cols])
        out[u] = netE + (r.d.sum() + (B @ b).sum()) / len(g)
    return out


def ipw(m, cols, netE):
    """Inverse probability of answering, the probability taken within cells of the given columns."""
    out = {}
    for u, g in m.groupby("unit"):
        pr = g.groupby(cols).resp.transform("mean") if cols else pd.Series(g.resp.mean(), index=g.index)
        r = g.resp
        wts = 1.0 / pr[r]
        out[u] = netE + float((g.d[r] * wts).sum() / wts.sum())
    return out


def pooled_flag(m, flag, netE):
    r = m[m.resp]
    units = sorted(m.unit.unique())
    A = np.column_stack([(r.unit == u).astype(float) for u in units] + [r[flag].astype(float)])
    b, *_ = np.linalg.lstsq(A, r.d.values, rcond=None)
    out = {}
    for i, u in enumerate(units):
        g = m[m.unit == u]
        n = g[~g.resp]
        out[u] = netE + (g[g.resp].d.sum() + (b[i] + b[-1] * n[flag].astype(float)).sum()) / len(g)
    return out


def capacity(L):
    cap = L["cap"]
    prov = L["prov"]
    ods_to = dict(zip(prov.ods_site_code, prov.provider_code))
    out = {}
    for r in cap.itertuples():
        code = ods_to[str(r[2])]
        out[L["site"][code]] = int(r[7])
    return out


def place(score, cap):
    order = sorted([u for u in score if score[u] >= FLOOR], key=lambda u: -score[u])
    left, aw = VOLUME, {}
    for u in order:
        a = min(cap[u], left)
        aw[u] = a
        left -= a
        if left <= 0:
            break
    return {u: aw.get(u, 0) for u in score}


def main_call(L):
    m, s = eligible(L)
    m = later_flags(m, s)
    netE = m.E.mean()
    R = {}
    R["R0_raw_answerers"] = {u: g[g.resp].chg.mean() for u, g in m.groupby("unit")}
    nEr = m[m.resp].E.mean()
    R["R1_answerers_adjusted"] = {u: nEr + g[g.resp].d.mean() for u, g in m.groupby("unit")}
    R["R2_casemix_imputation"] = reg_imp(m, [], netE)
    R["R2b_casemix_ipw"] = ipw(m.assign(pre_band=pd.cut(m.pre, [0, 30, 40, 50, 60, 101]), old=m.age_on_admission >= 65),
                               ["pre_band", "old"], netE)
    R["R3_at_expected"] = {u: netE + np.where(g.resp, g.d, 0).mean() for u, g in m.groupby("unit")}
    R["R3b_no_change"] = {u: netE + (np.where(g.resp, g.chg, 0) - g.E).mean() for u, g in m.groupby("unit")}
    R["R4_same_provider_only"] = cell(m, "same", netE)
    R["R4b_reoperation_only"] = cell(m, "reop", netE)
    R["R4c_any_later_spell"] = cell(m, "any", netE)
    R["GOLD"] = cell(m, "f90", netE)
    fam = {}
    for f in ("f30", "f90", "f90op", "f365", "nonel"):
        fam["cell_" + f] = cell(m, f, netE)
        fam["reg_" + f] = reg_imp(m, [f], netE)
        fam["ipw_" + f] = ipw(m, [f], netE)
        fam["pooled_" + f] = pooled_flag(m, f, netE)
    return m, netE, R, fam


# ------------------------------------------------------------------------------------------- Ask B
def participation(L, use_booked=False, match_unlinked=True):
    ops, s = index_ops(L["s"])
    q = L["q"]
    pre = q[(q.qtype == "pre") & q.score.notna()].copy()
    yr = ops[(ops.procedure_date >= FY26_FROM) & (ops.procedure_date <= FY26_TO)].copy()
    linked_pseudo = set(L["link"][L["link"].pseudo_nhs_number != ""].pseudo_nhs_number)
    lk = pre[pre.pseudo != ""]
    x = yr[["spell_id", "pseudo_nhs_number", "procedure_date"]].merge(lk, left_on="pseudo_nhs_number", right_on="pseudo")
    pairs = [x[["spell_id", "procedure_date", "sup_op", "completed"]]]
    if match_unlinked:
        prov = L["prov"]
        site_unit = {}
        for r in prov.itertuples():
            if r.mossgill_site_code:
                site_unit[r.mossgill_site_code] = L["site"][r.provider_code]
        free = ops[~ops.pseudo_nhs_number.isin(linked_pseudo)].copy()
        free["yob_lo"] = free.admission_date.dt.year - free.age_on_admission - 1
        free["yob_hi"] = free.admission_date.dt.year - free.age_on_admission
        un = pre[pre.pseudo == ""]
        got = []
        for r in un.itertuples():
            c = free[(free.unit == site_unit[r.site]) & (free.sex.astype(int) == r.sex) & (free.yob_lo <= r.yob) &
                     (free.yob_hi >= r.yob)]
            dd = (c.procedure_date - r.sup_op).dt.days
            c = c[(dd >= -30) & (dd <= 120)]
            if len(c):
                gap = (c.procedure_date - r.sup_op).dt.days.abs()
                c = c.assign(gap=gap).sort_values(["gap", "spell_id"])
                got.append((c.iloc[0].spell_id, c.iloc[0].procedure_date, r.sup_op, r.completed))
        if got:
            pairs.append(pd.DataFrame(got, columns=["spell_id", "procedure_date", "sup_op", "completed"]))
    pr = pd.concat(pairs, ignore_index=True)
    day = pr.sup_op if use_booked else pr.procedure_date
    gap = (day - pr.completed).dt.days
    ok = set(pr[(gap >= 0) & (gap <= 89)].spell_id)
    yr["ok"] = yr.spell_id.isin(ok)
    return {u: 100.0 * g.ok.mean() for u, g in yr.groupby("unit")}, yr


# ------------------------------------------------------------------------------------------- Ask A
def waits(target, site, prov, triage_match=True, chain=True, dedupe=True):
    P = lambda f: os.path.join(target, f)
    ptl = pd.read_csv(P("ptl_spinal_month_end_2026-01_to_2026-03.csv"), dtype=str, keep_default_na=False)
    rem = pd.read_csv(P("ptl_spinal_removals_2025-11_to_2026-04.csv"), dtype=str, keep_default_na=False)
    doc = json.load(open(P("msk_triage_referrals_2023-06_to_2026-03.json")))
    tri = pd.DataFrame(doc["referrals"])
    for c in ("referral_received", "rtt_clock_start"):
        ptl[c] = pd.to_datetime(ptl[c], format="%d/%m/%Y")
        rem[c] = pd.to_datetime(rem[c], format="%d/%m/%Y")
    rem["removal_date"] = pd.to_datetime(rem.removal_date, format="%d/%m/%Y")
    tri["received"] = pd.to_datetime(tri.received)
    tri["outcome_date"] = pd.to_datetime(tri.outcome_date)
    ods_unit = {r.ods_site_code: site[r.provider_code] for r in prov.itertuples()}
    tri["unit"] = tri.routed_to.map(ods_unit)
    tri["sexn"] = np.where(tri.sex == "F", 2, 1)
    sur = tri[tri.outcome == "Surgical opinion - spinal"]
    key = ["birth_year", "sexn", "postcode_district", "gp_practice", "unit"]
    sur = sur.assign(birth_year=sur.birth_year.astype(int))
    idx = {}
    for r in sur.itertuples():
        idx.setdefault((r.birth_year, r.sexn, r.postcode_district, r.gp_practice, r.unit), []).append((r.outcome_date, r.received))

    def triage_clock(unit, by, sx, dist, gp, receipt):
        c = [rec for od, rec in idx.get((by, sx, dist, gp, unit), []) if od <= receipt <= od + pd.Timedelta(days=10)]
        return c

    s = ptl[ptl.snapshot_date == "2026-03-31"].copy()
    s["unit"] = s.provider_code.map(site)
    ambiguous = 0
    clocks = []
    moved = rem[rem.removal_reason == "Transferred to another provider"]
    for r in s.itertuples():
        clock = r.rtt_clock_start
        if r.referral_route == "MSK triage" and triage_match:
            c = triage_clock(r.unit, int(r.birth_year), int(r.sex), r.postcode_district, r.gp_practice, r.referral_received)
            if len(c) == 1:
                clock = c[0]
            elif len(c) > 1:
                ambiguous += 1
        if r.referral_route == "Transfer" and chain:
            o = moved[(moved.pseudo_nhs_number == r.pseudo_nhs_number) & (moved.removal_date == r.referral_received)]
            if len(o) == 1:
                o = o.iloc[0]
                clock = o.rtt_clock_start
                if o.referral_route == "MSK triage" and triage_match:
                    c = triage_clock(site[o.provider_code], int(r.birth_year), int(r.sex), r.postcode_district,
                                     r.gp_practice, o.referral_received)
                    if len(c) == 1:
                        clock = c[0]
                    elif len(c) > 1:
                        ambiguous += 1
        clocks.append(clock)
    s["clock"] = clocks
    if dedupe:
        gone = moved[moved.removal_date <= SNAP][["provider_code", "pathway_id"]]
        s = s.merge(gone.assign(g=1), on=["provider_code", "pathway_id"], how="left")
        s = s[s.g.isna()].drop(columns="g")
    s["days"] = (SNAP - s.clock).dt.days
    out = {}
    for u, g in s.groupby("unit"):
        out[u] = dict(waiting=len(g), over52=int((g.days > 364).sum()), within18=100.0 * (g.days <= 126).mean())
    return out, ambiguous, s


def run(target):
    global COEF
    COEF = coef_from_policy(target)
    L = load(target)
    m, netE, R, fam = main_call(L)
    cap = capacity(L)
    res = dict(netE=netE, eligible=len(m), answered=int(m.resp.sum()), R=R, fam=fam, cap=cap,
               place={k: place(v, cap) for k, v in list(R.items()) + list(fam.items())})
    res["askB"] = {"golden": participation(L)[0], "natural": participation(L, use_booked=True, match_unlinked=False)[0],
                   "cracker": participation(L, use_booked=False, match_unlinked=False)[0],
                   "half": participation(L, use_booked=True, match_unlinked=True)[0]}
    A = {}
    A["golden"], amb, _ = waits(target, L["site"], L["prov"])
    A["natural"], _, _ = waits(target, L["site"], L["prov"], triage_match=False, chain=False, dedupe=False)
    A["cracker"], _, _ = waits(target, L["site"], L["prov"], triage_match=False, chain=True, dedupe=True)
    A["half"], _, _ = waits(target, L["site"], L["prov"], triage_match=True, chain=False, dedupe=False)
    A["no_dedupe"], _, _ = waits(target, L["site"], L["prov"], triage_match=True, chain=True, dedupe=False)
    A["no_chain"], _, _ = waits(target, L["site"], L["prov"], triage_match=True, chain=False, dedupe=True)
    res["askA"] = A
    res["askA_ambiguous"] = amb
    res["m"] = m
    res["L"] = L
    return res


if __name__ == "__main__":
    import sys
    res = run(sys.argv[1])
    names = dict(zip(res["L"]["prov"].provider_code, res["L"]["prov"].provider_name))
    units = sorted(res["R"]["GOLD"])
    print("eligible", res["eligible"], "answered", res["answered"], "netE", round(res["netE"], 3))
    for k, v in list(res["R"].items()) + list(res["fam"].items()):
        pl = res["place"][k]
        print("%-24s" % k, " ".join("%5.2f" % v[u] for u in units), "|", " ".join("%s%d" % (names[u][:4], pl[u]) for u in units if pl[u]))
    for k, v in res["askB"].items():
        print("B", "%-8s" % k, " ".join("%5.1f" % v[u] for u in units))
    for k, v in res["askA"].items():
        print("A", "%-9s" % k, " ".join("%4d/%4.1f" % (v[u]["over52"], v[u]["within18"]) for u in units))
    print("ambiguous triage matches", res["askA_ambiguous"])
