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
    """Link each adult across quarters: the unit's case id carried back through the CAPI crosswalk, plus the line
    number, kept only where sex matches and age moves by 0 or 1 (a new household reuses line numbers)."""
    P = L["P"].copy()
    new2old = dict(zip(L["X"]["NEW_CASEID"], L["X"]["OLD_CASEID"]))
    P["unit"] = P["CASEID"].map(lambda c: new2old.get(c, c))
    P = P.sort_values(["unit", "LINENO", "qi"]).reset_index(drop=True)
    prev = P.groupby(["unit", "LINENO"]).shift(1)
    P["prev_qi"] = prev["qi"]
    P["prev_idx"] = P.index.to_series().groupby([P["unit"], P["LINENO"]]).shift(1)
    ok = (P["prev_qi"] == P["qi"] - 1)
    if check_identity:
        ok &= (prev["SEX"] == P["SEX"]) & ((P["AGE"] - prev["AGE"]).isin([0, 1]))
    P["linked"] = ok
    return P


def pairs(PK):
    """Adjacent-quarter pairs of the same adult, employed in both quarters."""
    cur = PK[PK["linked"]].copy()
    prv = PK.loc[cur["prev_idx"].astype(int).values].reset_index(drop=True)
    cur = cur.reset_index(drop=True)
    out = pd.DataFrame({
        "unit": cur["unit"], "line": cur["LINENO"], "area": cur["HES_AREA"], "q0": prv["SURVEY_QTR"],
        "q1": cur["SURVEY_QTR"],
        "emp0": prv["LFSTAT"].isin([1, 2]).values, "emp1": cur["LFSTAT"].isin([1, 2]).values,
        "m0": (prv["MJH"] == 1).values, "m1": (cur["MJH"] == 1).values,
        "s0": (prv["RESPLINE"] == prv["LINENO"]).values, "s1": (cur["RESPLINE"] == cur["LINENO"]).values})
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
    """Sensitivity from adults answered for in a quarter flanked by two quarters in which they reported a second job
    themselves (no persistence correction needed on either side)."""
    lk = PK.set_index(PK.index)
    rows = []
    cur = PK[PK["linked"]]
    nxt = {}
    for i, r in cur[["prev_idx"]].iterrows():
        nxt[int(r["prev_idx"])] = i
    for mid, r in PK.iterrows():
        if not r["linked"] or mid not in nxt:
            continue
        a, b = int(r["prev_idx"]), nxt[mid]
        A, B = PK.loc[a], PK.loc[b]
        if not (A["LFSTAT"] in (1, 2) and r["LFSTAT"] in (1, 2) and B["LFSTAT"] in (1, 2)):
            continue
        if A["RESPLINE"] == A["LINENO"] and B["RESPLINE"] == B["LINENO"] and r["RESPLINE"] != r["LINENO"]:
            if A["MJH"] == 1 and B["MJH"] == 1:
                rows.append(r["MJH"] == 1)
    return float(np.mean(rows)), len(rows)


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


def carry(e, PK, fallback="face", s=None, mar=None):
    """Answered-for adults given their own second-job report from the nearest quarter in which they answered for
    themselves (employed then); adults never self-reporting get the fallback."""
    lk = PK[["unit", "LINENO", "qi", "SURVEY_QTR", "LFSTAT", "MJH", "RESPLINE", "SEX", "AGE", "linked"]].copy()
    # chains: consecutive linked rows of one adult share a chain id
    lk["start"] = ~lk["linked"]
    lk["chain"] = lk["start"].cumsum()
    lk["selfemp"] = (lk["RESPLINE"] == lk["LINENO"]) & lk["LFSTAT"].isin([1, 2])
    chain_self = lk[lk["selfemp"]][["chain", "qi", "MJH"]]
    e = e.copy()
    key = lk.set_index(["SURVEY_QTR", "unit", "LINENO"])["chain"]
    new2old = {}
    e = e.merge(lk[["SURVEY_QTR", "LINENO", "unit", "chain"]].assign(CASEID=None).drop(columns="CASEID"),
                how="left", left_on=["SURVEY_QTR", "LINENO", "unit"], right_on=["SURVEY_QTR", "LINENO", "unit"]) \
        if "unit" in e.columns else e
    return e


def golden_family(L, e, PK, pr):
    s_adj = sensitivity(pr, "adj")
    fp = false_report(pr)
    fam = {}
    fam["golden"] = corrected(e, s_adj, fp)
    fam["s_raw"] = corrected(e, sensitivity(pr, "raw"), fp)
    fam["s_fwd"] = corrected(e, sensitivity(pr, "fwd"), fp)
    fam["s_bwd"] = corrected(e, sensitivity(pr, "bwd"), fp)
    fam["no_fp"] = corrected(e, s_adj, 0.0)
    fam["s_by_area"] = corrected(e, s_adj, fp, {a: sensitivity(pr, "adj", a) for a in AREAS})
    fam["unweighted"] = corrected_unweighted(e, s_adj, fp)
    fam["by_quarter_mean"] = corrected_by_quarter(e, s_adj, fp)
    return fam, dict(s_adj=s_adj, s_raw=sensitivity(pr, "raw"), s_fwd=sensitivity(pr, "fwd"),
                     s_bwd=sensitivity(pr, "bwd"), fp=fp)


def designate(sh):
    return sorted(a for a, v in sh.items() if v >= THRESHOLD)


def main_call(L):
    E = employed(attach_weights(L))
    PK = person_keys(L)
    pr = pairs(PK)
    fam, par = golden_family(L, E, PK, pr)
    rungs = {}
    rungs["R0_face"] = shares_from(E, "mjh")
    sf = E[E["self"]]
    rungs["R1_self_only"] = shares_from(sf, "mjh")
    rungs["R2_mar"] = mar_impute(E)
    rungs["R2_mar_coarse"] = mar_impute(E, coarse=True)
    return dict(E=E, PK=PK, pr=pr, fam=fam, par=par, rungs=rungs)
