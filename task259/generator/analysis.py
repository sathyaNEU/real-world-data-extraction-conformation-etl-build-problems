"""Every rung, the golden and the asks, computed from target/ alone (no import of world.py or pack.py).

The golden: each workforce area's share of employed residents holding more than one job, counted as each resident
would report it themselves, over 2025Q4 to 2026Q3 on the final weights. A household member answering for an absent
adult reports a held second job only some of the time; that sensitivity is read within person, from residents who
answered for themselves in one quarter and were answered for in an adjacent one, and every answered-for report is
corrected by it.
"""
import os
import zipfile

import numpy as np
import openpyxl
import pandas as pd

QUARTERS = ["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3"]
REF = ["2025Q4", "2026Q1", "2026Q2", "2026Q3"]
AREAS = ["01", "02", "03", "04", "05", "06", "07", "08"]
THRESHOLD = 7.0


# ----------------------------------------------------------------------------------------------------- loading
def load(tdir):
    P = pd.read_csv(os.path.join(tdir, "HES_PERSON_2025Q1_2026Q3.csv"),
                    dtype={"CASEID": str, "HES_AREA": str, "OCCMAJ": str})
    P["qi"] = P["SURVEY_QTR"].map({q: i for i, q in enumerate(QUARTERS)})
    X = pd.read_csv(os.path.join(tdir, "HES_CASEID_CROSSWALK_CAPI2026.csv"), dtype=str)
    wb = openpyxl.load_workbook(os.path.join(tdir, "HES_FINAL_WEIGHTS_2025Q4_2026Q3.xlsx"), read_only=True)
    wsheets = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        df = pd.DataFrame(rows[1:], columns=rows[0])
        df["CASEID"] = df["CASEID"].astype(str)
        df["LINENO"] = df["LINENO"].astype(int)
        wsheets[ws.title] = df
    wb.close()
    D = pd.read_csv(os.path.join(tdir, "HES_HOUSEHOLD_DISPOSITIONS_2025Q1_2026Q3.csv"),
                    dtype={"CASEID": str, "FRAMEID": str, "CTY": str, "ZIP": str, "MODE": str, "START_UTC": str})
    F = pd.read_csv(os.path.join(tdir, "HES_FRAME_MAINTENANCE_2024-07_2026-09.csv"), dtype=str)
    C = pd.read_csv(os.path.join(tdir, "HES_DISPOSITION_CODES.csv"), dtype=str)
    wb = openpyxl.load_workbook(os.path.join(tdir, "TDLI_WORKFORCE_AREAS_2026.xlsx"), read_only=True)
    areas = [r for r in wb["Areas"].iter_rows(values_only=True)][1:]
    zips = [r for r in wb["County 59041"].iter_rows(values_only=True)][1:]
    wb.close()
    return dict(P=P, X=X, W=wsheets, D=D, F=F, C=C, areas=areas, zips=zips)


def attach_weights(L, q3_sheet="2026Q3 rev"):
    P = L["P"]
    parts = []
    for q in REF:
        sheet = q3_sheet if q == "2026Q3" else q
        w = L["W"][sheet][["CASEID", "LINENO", "FWGT"]].copy()
        w["SURVEY_QTR"] = q
        parts.append(w)
    Wt = pd.concat(parts)
    out = P[P["SURVEY_QTR"].isin(REF)].merge(Wt, on=["SURVEY_QTR", "CASEID", "LINENO"], how="left")
    return out


def employed(df):
    e = df[df["LFSTAT"].isin([1, 2])].copy()
    e["mjh"] = (e["MJH"] == 1).astype(float)
    e["self"] = e["RESPLINE"] == e["LINENO"]
    return e


# ------------------------------------------------------------------------------------------- panel linking
def person_keys(L, check_identity=True):
    """Each adult across quarters: the unit's case id carried back through the CAPI crosswalk, plus the line number.
    A new household at the address reuses line numbers, so a chain breaks where sex changes or age does not move by
    0 or 1 between the quarters (with identity checking off, unit and line alone)."""
    P = L["P"].copy()
    new2old = dict(zip(L["X"]["NEW_CASEID"], L["X"]["OLD_CASEID"]))
    P["unit"] = P["CASEID"].map(lambda c: new2old.get(c, c))
    P = P.sort_values(["unit", "LINENO", "qi"]).reset_index(drop=True)
    g = P.groupby(["unit", "LINENO"])
    prev_sex, prev_age, prev_qi = g["SEX"].shift(1), g["AGE"].shift(1), g["qi"].shift(1)
    new_chain = prev_qi.isna()
    if check_identity:
        new_chain |= (prev_sex != P["SEX"]) | ~((P["AGE"] - prev_age).isin([0, 1]))
    P["pid"] = new_chain.cumsum()
    P["linked"] = (~new_chain) & (prev_qi == P["qi"] - 1)
    return P


def pairs(PK, lag=1):
    """Pairs of quarters of the same adult `lag` quarters apart, employed in both."""
    A = PK[["pid", "qi", "HES_AREA", "SURVEY_QTR", "LFSTAT", "MJH", "RESPLINE", "LINENO"]]
    B = A.copy()
    B["qi"] = B["qi"] - lag
    m = A.merge(B, on=["pid", "qi"], suffixes=("0", "1"))
    out = pd.DataFrame({
        "pid": m["pid"], "area": m["HES_AREA0"], "q0": m["SURVEY_QTR0"], "q1": m["SURVEY_QTR1"],
        "emp0": m["LFSTAT0"].isin([1, 2]), "emp1": m["LFSTAT1"].isin([1, 2]),
        "m0": m["MJH0"] == 1, "m1": m["MJH1"] == 1,
        "s0": m["RESPLINE0"] == m["LINENO0"], "s1": m["RESPLINE1"] == m["LINENO1"]})
    return out[out["emp0"] & out["emp1"]].reset_index(drop=True)


def sensitivity(pr, how="adj", area=None):
    """The answering member's chance of reporting a second job the adult holds, read within person.

    raw: among adults who reported a second job themselves one quarter and were answered for the next (or the
    reverse), the share whose answered-for report has the second job.  adj: that share divided by the chance a second
    job reported by the adult themselves is still reported by them the next quarter (both quarters self-reported),
    so jobs that really ended between quarters are not charged to the answering member."""
    if area is not None:
        pr = pr[pr["area"] == area]
    f_sp = pr[pr["s0"] & ~pr["s1"] & pr["m0"]]           # self then proxy
    b_ps = pr[~pr["s0"] & pr["s1"] & pr["m1"]]           # proxy then self
    ss = pr[pr["s0"] & pr["s1"]]
    keep_f = ss[ss["m0"]]["m1"].mean()
    keep_b = ss[ss["m1"]]["m0"].mean()
    if how == "fwd":
        raw = f_sp["m1"].mean()
        return raw / keep_f
    if how == "bwd":
        raw = b_ps["m0"].mean()
        return raw / keep_b
    n = len(f_sp) + len(b_ps)
    raw = (f_sp["m1"].sum() + b_ps["m0"].sum()) / n
    if how == "raw":
        return raw
    keep = (ss["m0"].sum() * keep_f + ss["m1"].sum() * keep_b) / (ss["m0"].sum() + ss["m1"].sum())
    return raw / keep


def false_report(pr):
    """The answering member's chance of reporting a second job the adult does not hold, net of second jobs that
    really began between quarters (read off the adults self-reporting in both quarters)."""
    f_sp = pr[pr["s0"] & ~pr["s1"] & ~pr["m0"]]
    b_ps = pr[~pr["s0"] & pr["s1"] & ~pr["m1"]]
    ss = pr[pr["s0"] & pr["s1"]]
    gain = (ss[~ss["m0"]]["m1"].sum() + ss[~ss["m1"]]["m0"].sum()) / ((~ss["m0"]).sum() + (~ss["m1"]).sum())
    raw = (f_sp["m1"].sum() + b_ps["m0"].sum()) / (len(f_sp) + len(b_ps))
    return max(0.0, raw - gain)


def sandwich(PK):
    """Sensitivity from adults answered for in a quarter flanked by quarters in which they reported a second job
    themselves (no persistence correction on either side)."""
    A = PK[["pid", "qi", "LFSTAT", "MJH", "RESPLINE", "LINENO"]].copy()
    A["self"] = A["RESPLINE"] == A["LINENO"]
    A["emp"] = A["LFSTAT"].isin([1, 2])
    L_ = A.assign(qi=A["qi"] + 1)
    R_ = A.assign(qi=A["qi"] - 1)
    m = A.merge(L_, on=["pid", "qi"], suffixes=("", "_l")).merge(R_, on=["pid", "qi"], suffixes=("", "_r"))
    m = m[m["emp"] & m["emp_l"] & m["emp_r"] & ~m["self"] & m["self_l"] & m["self_r"] & (m["MJH_l"] == 1) &
          (m["MJH_r"] == 1)]
    return float((m["MJH"] == 1).mean()), int(len(m))


# ------------------------------------------------------------------------------------------------ estimators
def shares_from(e, value_col, weight_col="FWGT", by_quarter=False):
    out = {}
    for a in AREAS:
        g = e[e["HES_AREA"] == a]
        if by_quarter:
            qs = []
            for q in REF:
                h = g[g["SURVEY_QTR"] == q]
                qs.append(100 * (h[weight_col] * h[value_col]).sum() / h[weight_col].sum())
            out[a] = float(np.mean(qs))
        else:
            out[a] = float(100 * (g[weight_col] * g[value_col]).sum() / g[weight_col].sum())
    return out


def corrected(e, s, fp=0.0, s_by_area=None):
    """Answered-for reports corrected for the answering member's sensitivity and false reports, area by area."""
    e = e.copy()
    out = {}
    for a in AREAS:
        g = e[e["HES_AREA"] == a]
        sa = s_by_area[a] if s_by_area else s
        sf = g[g["self"]]
        pf = g[~g["self"]]
        rp = (pf["FWGT"] * pf["mjh"]).sum() / pf["FWGT"].sum()
        tp = min(1.0, max(0.0, (rp - fp) / (sa - fp)))
        num = (sf["FWGT"] * sf["mjh"]).sum() + tp * pf["FWGT"].sum()
        out[a] = float(100 * num / g["FWGT"].sum())
    return out


def corrected_unweighted(e, s, fp=0.0):
    e = e.copy()
    e["one"] = 1.0
    out = {}
    for a in AREAS:
        g = e[e["HES_AREA"] == a]
        sf, pf = g[g["self"]], g[~g["self"]]
        tp = (pf["mjh"].mean() - fp) / (s - fp)
        out[a] = float(100 * (sf["mjh"].sum() + tp * len(pf)) / len(g))
    return out


def corrected_by_quarter(e, s, fp=0.0):
    out = {}
    for a in AREAS:
        vals = []
        for q in REF:
            g = e[(e["HES_AREA"] == a) & (e["SURVEY_QTR"] == q)]
            sf, pf = g[g["self"]], g[~g["self"]]
            rp = (pf["FWGT"] * pf["mjh"]).sum() / pf["FWGT"].sum()
            tp = (rp - fp) / (s - fp)
            vals.append(100 * ((sf["FWGT"] * sf["mjh"]).sum() + tp * pf["FWGT"].sum()) / g["FWGT"].sum())
        out[a] = float(np.mean(vals))
    return out


def cell_key(e):
    hrs = e["HRSMAIN"]
    pt = np.where(hrs == -9, "u", np.where(hrs < 35, "p", "f"))
    ag = pd.cut(e["AGE"], [15, 24, 34, 44, 54, 64, 200], labels=False)
    return e["HES_AREA"] + "|" + ag.astype(str) + "|" + e["SEX"].astype(str) + "|" + pt + "|" + e["OCCMAJ"].str[:2]


def mar_impute(e, coarse=False):
    """Answered-for adults given the self-reporters' rate in their cell (area, age group, sex, hours band, and
    occupation unless coarse)."""
    e = e.copy()
    k = cell_key(e)
    if coarse:
        k = k.str.rsplit("|", n=1).str[0]
    e["cell"] = k
    sf = e[e["self"]]
    rate = (sf["FWGT"] * sf["mjh"]).groupby(sf["cell"]).sum() / sf["FWGT"].groupby(sf["cell"]).sum()
    # cells with no self-reporter fall back to the area, age group and sex rate
    k2 = e["HES_AREA"] + "|" + pd.cut(e["AGE"], [15, 24, 34, 44, 54, 64, 200], labels=False).astype(str) + "|" + \
        e["SEX"].astype(str)
    e["cell2"] = k2
    rate2 = (sf["FWGT"] * sf["mjh"]).groupby(k2[sf.index]).sum() / sf["FWGT"].groupby(k2[sf.index]).sum()
    imp = e["cell"].map(rate)
    imp = imp.fillna(e["cell2"].map(rate2))
    e["v"] = np.where(e["self"], e["mjh"], imp)
    return shares_from(e, "v")

def carry(e, PK, fallback="face", s=None, fp=0.0, how="nearest"):
    """Answered-for adults given their own second-job report from the nearest quarter in which they answered for
    themselves while employed (any quarter on file); adults never answering for themselves get the fallback:
    their answered-for report as it stands (face), their cell's self-reported rate (mar), or the answered-for report
    corrected by the sensitivity s (corrected)."""
    keys = PK[["SURVEY_QTR", "CASEID", "LINENO", "pid"]]
    e = e.merge(keys, on=["SURVEY_QTR", "CASEID", "LINENO"], how="left")
    own = PK[(PK["RESPLINE"] == PK["LINENO"]) & PK["LFSTAT"].isin([1, 2])][["pid", "qi", "MJH"]]
    own = own.rename(columns={"qi": "qo", "MJH": "mo"})
    px = e[~e["self"]][["pid", "qi"]].reset_index()
    m = px.merge(own, on="pid", how="inner")
    m["d"] = (m["qo"] - m["qi"]).abs()
    if how == "nearest":
        m = m.sort_values(["index", "d", "qo"]).drop_duplicates("index")
        val = (m.set_index("index")["mo"] == 1).astype(float)
    else:
        val = m.assign(v=(m["mo"] == 1).astype(float)).groupby("index")["v"].mean()
    e["carried"] = val
    e["has"] = e["carried"].notna()
    if fallback == "face":
        e["v"] = np.where(e["self"], e["mjh"], np.where(e["has"], e["carried"], e["mjh"]))
        return shares_from(e, "v"), e
    if fallback == "mar":
        e2 = e.copy()
        k = cell_key(e2)
        sf = e2[e2["self"]]
        rate = (sf["FWGT"] * sf["mjh"]).groupby(k[sf.index]).sum() / sf["FWGT"].groupby(k[sf.index]).sum()
        k2 = e2["HES_AREA"] + "|" + pd.cut(e2["AGE"], [15, 24, 34, 44, 54, 64, 200], labels=False).astype(str)
        rate2 = (sf["FWGT"] * sf["mjh"]).groupby(k2[sf.index]).sum() / sf["FWGT"].groupby(k2[sf.index]).sum()
        imp = k.map(rate).fillna(k2.map(rate2))
        e2["v"] = np.where(e2["self"], e2["mjh"], np.where(e2["has"], e2["carried"], imp))
        return shares_from(e2, "v"), e
    out = {}
    for a in AREAS:
        g = e[e["HES_AREA"] == a]
        sf, pc, pn = g[g["self"]], g[~g["self"] & g["has"]], g[~g["self"] & ~g["has"]]
        rp = (pn["FWGT"] * pn["mjh"]).sum() / pn["FWGT"].sum()
        tp = (rp - fp) / (s - fp)
        num = (sf["FWGT"] * sf["mjh"]).sum() + (pc["FWGT"] * pc["carried"]).sum() + tp * pn["FWGT"].sum()
        out[a] = float(100 * num / g["FWGT"].sum())
    return out, e


def golden_family(L, e, PK, pr):
    s_adj = sensitivity(pr, "adj")
    fp = false_report(pr)
    fam = {}
    fam["golden"] = corrected(e, s_adj, fp)
    fam["s_raw"] = corrected(e, sensitivity(pr, "raw"), fp)
    fam["s_fwd"] = corrected(e, sensitivity(pr, "fwd"), fp)
    fam["s_bwd"] = corrected(e, sensitivity(pr, "bwd"), fp)
    fam["no_fp"] = corrected(e, s_adj, 0.0)
    for how in ("adj", "raw", "fwd", "bwd"):
        fam["area_s_" + how] = corrected(e, s_adj, fp, {a: sensitivity(pr, how, a) for a in AREAS})
    fam["unweighted"] = corrected_unweighted(e, s_adj, fp)
    fam["by_quarter_mean"] = corrected_by_quarter(e, s_adj, fp)
    sw, nsw = sandwich(PK)
    fam["sandwich"] = corrected(e, sw, fp)
    pr2 = pairs(PK, lag=2)
    s2 = sensitivity(pd.concat([pr, pr2]), "adj")
    fam["lags_1_2"] = corrected(e, s2, fp)
    fam["carry_then_correct"] = carry(e, PK, "corrected", s=s_adj, fp=fp)[0]
    PKn = person_keys(L, check_identity=False)
    prn = pairs(PKn)
    fam["no_identity_check"] = corrected(e, sensitivity(prn, "adj"), false_report(prn))
    e_pre = employed(attach_weights(L, "2026Q3"))
    fam["q3_first_issue"] = corrected(e_pre, s_adj, fp)
    par = dict(s_adj=s_adj, s_raw=sensitivity(pr, "raw"), s_fwd=sensitivity(pr, "fwd"), s_bwd=sensitivity(pr, "bwd"),
               fp=fp, s_sandwich=sw, n_sandwich=nsw, s_lags=s2,
               n_sp=int((pr["s0"] & ~pr["s1"] & pr["m0"]).sum()), n_ps=int((~pr["s0"] & pr["s1"] & pr["m1"]).sum()))
    return fam, par


def designate(sh):
    return sorted(a for a, v in sh.items() if v >= THRESHOLD)


def statewide(e, s=None, fp=0.0):
    """The state's share on the self-report basis (s given) or as reported (s None)."""
    if s is None:
        return float(100 * (e["FWGT"] * e["mjh"]).sum() / e["FWGT"].sum())
    sf, pf = e[e["self"]], e[~e["self"]]
    num = (sf["FWGT"] * sf["mjh"]).sum()
    for a in AREAS:
        g = pf[pf["HES_AREA"] == a]
        rp = (g["FWGT"] * g["mjh"]).sum() / g["FWGT"].sum()
        num += (rp - fp) / (s - fp) * g["FWGT"].sum()
    return float(100 * num / e["FWGT"].sum())


def main_call(L):
    E = employed(attach_weights(L))
    PK = person_keys(L)
    pr = pairs(PK)
    fam, par = golden_family(L, E, PK, pr)
    rungs = {}
    rungs["R0_face"] = shares_from(E, "mjh")
    rungs["R1_self_only"] = shares_from(E[E["self"]], "mjh")
    rungs["R2_mar"] = mar_impute(E)
    rungs["R2_mar_coarse"] = mar_impute(E, coarse=True)
    rungs["R3_carry_face"], Ec = carry(E, PK, "face")
    rungs["R3_carry_mean"] = carry(E, PK, "face", how="mean")[0]
    rungs["R3b_carry_mar"] = carry(E, PK, "mar")[0]
    k = cell_key(E)
    sf = E[E["self"]]
    rate = (sf["FWGT"] * sf["mjh"]).groupby(k[sf.index]).sum() / sf["FWGT"].groupby(k[sf.index]).sum()
    pf = E[~E["self"]]
    expct = k[pf.index].map(rate)
    ok = expct.notna()
    cs_ratio = float((pf["FWGT"][ok] * pf["mjh"][ok]).sum() / (pf["FWGT"][ok] * expct[ok]).sum())
    raw_ratio = float(((pf["FWGT"] * pf["mjh"]).sum() / pf["FWGT"].sum()) /
                      ((sf["FWGT"] * sf["mjh"]).sum() / sf["FWGT"].sum()))
    par.update(cs_ratio_cells=cs_ratio, cs_ratio_raw=raw_ratio, carried_share=float(Ec[~Ec["self"]]["has"].mean()),
               proxy_share=float(1 - E["self"].mean()))
    state = dict(face=statewide(E), golden=statewide(E, par["s_adj"], par["fp"]),
                 s_raw=statewide(E, par["s_raw"], par["fp"]), s_fwd=statewide(E, par["s_fwd"], par["fp"]),
                 s_bwd=statewide(E, par["s_bwd"], par["fp"]), sandwich=statewide(E, par["s_sandwich"], par["fp"]))
    return dict(E=E, PK=PK, pr=pr, fam=fam, par=par, rungs=rungs, state=state)


# ------------------------------------------------------------------------------------------------------- asks
INTERVIEW = {"1", "201"}
NOT_ELIGIBLE = {"5", "6", "223", "224", "225"}
NO_ONE_HOME = {"3", "216"}


def area_of(L):
    """County to workforce area from the areas workbook; county 59041 by ZIP."""
    cty = {}
    for wda, name, counties, board in L["areas"]:
        for c in str(counties).split(","):
            cty.setdefault(c.strip(), []).append(str(wda))
    z = {str(r[0]): str(r[1]) for r in L["zips"]}
    return cty, z


def unit_quarters(L, quarters=REF, dedup=True, split041="zip"):
    D = L["D"]
    D = D[D["SURVEY_QTR"].isin(quarters)].copy()
    cty, z = area_of(L)
    if split041 == "zip":
        D["area"] = [z[zp] if c == "59041" else cty[c][0] for c, zp in zip(D["CTY"], D["ZIP"])]
    else:
        D["area"] = [split041 if c == "59041" else cty[c][0] for c, zp in zip(D["CTY"], D["ZIP"])]
    D["code"] = D["DISPO"].astype(str)
    if not dedup:
        D["interviewed"] = D["code"].isin(INTERVIEW)
        D["visit"] = D["DISPO_DATE"]
        return D
    g = D.groupby(["FRAMEID", "SURVEY_QTR"])
    first = g.first()[["area"]]
    first["interviewed"] = g["code"].agg(lambda s: bool(set(s) & INTERVIEW))
    nonint = D[~D["code"].isin(INTERVIEW)].sort_values("DISPO_DATE").groupby(["FRAMEID", "SURVEY_QTR"]).last()
    first["code"] = nonint["code"]
    first["visit"] = nonint["DISPO_DATE"]
    first.loc[first["interviewed"], "code"] = "I"
    return first.reset_index()


def frame_deleted_at(L, U, void_in_error=True):
    """Whether each unit-quarter's housing unit stood deleted from the frame (vacant or demolished) on the visit date.
    void_in_error: a deletion later restored as entered in error never took effect."""
    F = L["F"]
    dels = F[(F["ACTION"] == "DELETE") & F["REASON"].isin(["VACANT", "DEMOLISHED"])][["FRAMEID", "EFFECTIVE"]]
    rst = F[(F["ACTION"] == "RESTORE")][["FRAMEID", "EFFECTIVE"]].rename(columns={"EFFECTIVE": "R"})
    m = U[["FRAMEID", "SURVEY_QTR", "visit"]].merge(dels, on="FRAMEID", how="inner")
    m = m[m["EFFECTIVE"] <= m["visit"]]
    if void_in_error:
        r = m.merge(rst, on="FRAMEID", how="left")
        r["voided"] = r["R"].notna() & (r["R"] >= r["EFFECTIVE"])
        void = r.groupby(["FRAMEID", "SURVEY_QTR", "EFFECTIVE"])["voided"].any().reset_index()
        m = void[~void["voided"]]
    else:
        r = m.merge(rst, on="FRAMEID", how="left")
        r["restored_before"] = r["R"].notna() & (r["R"] >= r["EFFECTIVE"]) & (r["R"] <= r["visit"])
        void = r.groupby(["FRAMEID", "SURVEY_QTR", "EFFECTIVE"])["restored_before"].any().reset_index()
        m = void[~void["restored_before"]]
    keys = set(zip(m["FRAMEID"], m["SURVEY_QTR"]))
    return np.array([(f, q) in keys for f, q in zip(U["FRAMEID"], U["SURVEY_QTR"])])


def ask_rates(L, frame="golden", dedup=True, split041="zip", interview_proves=True):
    """Household response rate and noncontact rate by area over the four quarters, per cent.
    frame: golden (frame state at the visit, deletions restored as in error void), asof (state at the visit as the
    log then stood), none (disposition codes only)."""
    U = unit_quarters(L, dedup=dedup, split041=split041)
    if not dedup:
        U = U.rename(columns={"interviewed": "interviewed"})
        U["code"] = np.where(U["interviewed"], "I", U["code"])
    ne = U["code"].isin(NOT_ELIGIBLE).values
    if frame != "none":
        dz = frame_deleted_at(L, U, void_in_error=(frame == "golden"))
        if interview_proves:
            dz = dz & ~U["interviewed"].values
        ne = ne | dz
    U["eligible"] = ~ne
    U["nc"] = U["eligible"] & U["code"].isin(NO_ONE_HOME)
    out = {}
    for a in AREAS:
        g = U[U["area"] == a]
        el = g["eligible"].sum()
        out[a] = dict(rr=float(100 * (g["interviewed"] & g["eligible"]).sum() / el),
                      nc=float(100 * g["nc"].sum() / el), eligible=int(el),
                      interviewed=int((g["interviewed"] & g["eligible"]).sum()))
    return out


# ---------------------------------------------------------------------------------------------- the figures
def area_names(L):
    return {str(r[0]): str(r[1]) for r in L["areas"]}


def figures(L):
    """Every graded figure and every rung, from target/ alone."""
    M = main_call(L)
    names = area_names(L)
    gold = M["fam"]["golden"]
    asks = ask_rates(L)
    out = dict(
        certified=designate(gold),
        certified_names=[names[a] for a in designate(gold)],
        share=gold,
        statewide=M["state"]["golden"],
        statewide_face=M["state"]["face"],
        sensitivity=float(M["par"]["s_adj"]),
        false_report=float(M["par"]["fp"]),
        rr={a: asks[a]["rr"] for a in AREAS},
        nc={a: asks[a]["nc"] for a in AREAS},
        eligible={a: asks[a]["eligible"] for a in AREAS},
        interviewed={a: asks[a]["interviewed"] for a in AREAS},
        names=names)
    return out, M
