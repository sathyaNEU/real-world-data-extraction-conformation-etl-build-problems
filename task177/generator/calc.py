"""task177 calc: every graded figure computed from the shipped files (the generator's own reading of the pack), with
the default path and the rival routes beside the golden. deliver.py writes the goldens from it; checks.py asserts on
it; verify.py recomputes the graded figures on its own code path."""
from __future__ import annotations

import os
import re
from collections import defaultdict

import numpy as np
import pandas as pd

import common as C

FIRST = C.mi(*C.HIST_FROM)
TEND = C.mi(*C.DATA_END)


def month_of(s):
    s = str(s)
    if re.fullmatch(r"\d{6}", s):
        return C.mi(int(s[:4]), int(s[4:]))
    return C.mi(int(s[:4]), int(s[5:7]))


def norm_id(x):
    return re.sub(r"\D", "", str(x))


# ------------------------------------------------------------------------------------------------- public side
def load_public(target):
    L = pd.read_csv(os.path.join(target, C.F_LOANS), dtype={"loan_no": str, "member_id": str})
    X = pd.read_csv(os.path.join(target, C.F_XWALK), dtype=str)
    R = pd.read_csv(os.path.join(target, C.F_RETURNS), dtype=str).drop_duplicates()
    D = pd.read_csv(os.path.join(target, C.F_DEFAULTS), dtype={"loan_reference": str, "member_id": str})
    canon = dict(zip(X["legacy_loan_no"], X["core_loan_no"]))
    R["loan"] = R["loan_reference"].map(lambda r: canon.get(r, r))
    R["t"] = R["period"].map(month_of)
    R["left"] = R["reason"].isin(["01", "SIN SALARIO"])
    D["loan"] = D["loan_reference"].map(lambda r: canon.get(r, r))
    D["t"] = D["default_date"].map(lambda s: C.mi(int(s[:4]), int(s[5:7])))
    leg = L["origin_system"] == "LEGACY"
    for col in ("net_pay_at_origination", "principal", "instalment"):
        L[col] = L[col].astype(float) * np.where(leg, 1000.0, 1.0)
    L["d"] = L["disbursement_date"].map(lambda s: C.mi(int(s[:4]), int(s[5:7])))
    L["temp"] = L["contract_type"].isin(["T", "TEMPORAL"])
    return L, R, D


def runs(R):
    """each SIN SALARIO run's first month, per loan: a month whose previous month was not a SIN SALARIO return"""
    S = R[R["left"]][["loan", "t"]].drop_duplicates().sort_values(["loan", "t"])
    prev = S.groupby("loan")["t"].shift(1)
    return S[(prev.isna()) | (S["t"] - prev > 1)].rename(columns={"t": "c"})


def conversion(L, R, D, last_start=C.mi(2025, 12)):
    """F[j]: of the loans whose borrower stopped being paid by the payroll with the loan open (the first month of a run
    of SIN SALARIO returns, runs starting January 2017 to December 2025), the share whose default date falls within j
    months of that first month"""
    S = runs(R)
    S = S[S["c"] <= last_start]
    first = S.groupby("loan")["c"].min().reset_index()
    dd = D.groupby("loan")["t"].min()
    first["dt"] = first["loan"].map(dd)
    lag = first["dt"] - first["c"]
    F = np.array([((lag >= 0) & (lag <= j)).mean() for j in range(13)])
    return F, len(first)


def residual(L, R, D):
    """the monthly chance of default on a loan that is still paid by the payroll: defaults with no SIN SALARIO run
    before them, per loan-month on payroll, January 2017 to December 2025"""
    S = runs(R)
    firstrun = S.groupby("loan")["c"].min()
    dd = D.groupby("loan")["t"].min()
    loans = L[["loan_no", "d", "term_months"]].copy()
    loans["fr"] = loans["loan_no"].map(firstrun)
    loans["dt"] = loans["loan_no"].map(dd)
    end = np.minimum(loans["d"] + loans["term_months"], C.mi(2025, 12))
    stop = loans["fr"].fillna(1e9)
    stop = np.minimum(stop, loans["dt"].fillna(1e9))
    expo = np.clip(np.minimum(end, stop) - loans["d"], 0, None)
    margin_def = loans["dt"].notna() & (loans["fr"].isna() | (loans["fr"] > loans["dt"])) & (loans["dt"] <= C.mi(2025, 12))
    return float(margin_def.sum() / expo.sum())


# ------------------------------------------------------------------------------------------------ private side
def load_registers(target):
    G = pd.read_csv(os.path.join(target, C.F_REGISTERS), dtype=str).drop_duplicates()
    G["emp"] = G["employee_id"].map(norm_id)
    G["t"] = G["period_start"].map(lambda s: C.mi(int(s[:4]), int(s[5:7])))
    G["hire_t"] = G["hire_date"].map(lambda s: C.mi(int(s[:4]), int(s[5:7])))
    return G


def hazards(G, min_tenure=12, upto=TEND):
    """each employer's monthly chance that an employee with min_tenure months of service works their last month:
    leavers (the month of their final settlement) over employee-months, from the employer's first register"""
    W = G[G["payment_type"].isin(["NOMINA", "LIQUIDACION"])]
    P = W[["employer_nit", "emp", "t", "hire_t"]].drop_duplicates()
    leave = W[W["payment_type"] == "LIQUIDACION"][["employer_nit", "emp", "t"]].drop_duplicates()
    P = P[(P["t"] - P["hire_t"] >= min_tenure) & (P["t"] <= upto)]
    expo = P.groupby("employer_nit").size()
    lv = leave.merge(P, on=["employer_nit", "emp", "t"])
    nl = lv.groupby("employer_nit").size()
    h = (nl.reindex(expo.index).fillna(0) / expo)
    return h.to_dict(), expo.to_dict(), nl.reindex(expo.index).fillna(0).to_dict()


def load_launch(target):
    B = pd.read_csv(os.path.join(target, C.F_LAUNCH), dtype={"member_id": str, "employer_nit": str})
    A = pd.read_excel(os.path.join(target, C.F_AGREE), dtype=str)
    sec = dict(zip(A["employer_nit"], A["sector"]))
    B["sector"] = B["employer_nit"].map(sec)
    return B, A


def golden_probs(B, h, F, r):
    """each launch loan's chance of default by 31 January 2028: leaving at the end of month m (February 2027 is 1)
    misses month m + 1 first; default within the window when the lag fits in the months left; plus the on-payroll
    route at the residual monthly rate, three months from its start"""
    out = []
    for nit in B["employer_nit"]:
        hh = h[nit]
        surv = 1.0
        p = 0.0
        for m in range(1, 13):
            c = m + 1
            j = 12 - c
            p += surv * hh * (F[j] if j >= 0 else 0.0)
            if m + 3 <= 12:
                p += surv * (1 - hh) * r
            surv *= (1 - hh) * (1 - r)
        out.append(p)
    return np.array(out)


def call_figures(target):
    L, R, D = load_public(target)
    F, nruns = conversion(L, R, D)
    r = residual(L, R, D)
    G = load_registers(target)
    h, expo, nl = hazards(G)
    B, A = load_launch(target)
    p = golden_probs(B, h, F, r)
    B = B.assign(p=p)
    sec = B.groupby("sector")["p"].sum().reindex(list(C.SECTORS))
    out = dict(total=float(p.sum()), sectors={k: float(v) for k, v in sec.items()}, F=F, n_runs=nruns, resid=r,
               h=h, expo=expo, leavers=nl, n_launch=len(B))
    return out


# ------------------------------------------------------------------------------------- the default path and rivals
def default_path(target):
    """a PD model on the public book's borrower attributes (default within twelve months of disbursement, loans
    disbursed 2017 to 2025) scored on the launch loans"""
    from sklearn.linear_model import LogisticRegression
    L, R, D = load_public(target)
    dd = D.groupby("loan")["t"].min()
    L["dt"] = L["loan_no"].map(dd)
    H = L[L["d"] <= C.mi(2025, 12)].copy()
    H["y"] = (H["dt"].notna() & (H["dt"] <= H["d"] + 12)).astype(int)
    H["tenure"] = H["d"] - H["hire_date"].map(lambda s: C.mi(int(s[:4]), int(s[5:7])))
    H["age"] = H["disbursement_date"].str[:4].astype(int) - H["birth_year"]
    H["ratio"] = H["instalment"] / H["net_pay_at_origination"]

    def X(df):
        return np.column_stack([df["age"], np.log(df["net_pay_at_origination"]), np.log1p(df["tenure"].clip(lower=0)),
                                df["temp"].astype(float), df["ratio"], df["term_months"]])
    lr = LogisticRegression(max_iter=4000).fit(X(H), H["y"])
    B, A = load_launch(target)
    B["tenure"] = C.mi(2027, 2) - B["hire_date"].map(lambda s: C.mi(int(s[:4]), int(s[5:7])))
    B["age"] = 2027 - 40   # the launch file carries no birth year; the public mean age stands in
    B["temp"] = False
    B["net_pay_at_origination"] = B["certified_net_pay"].astype(float)
    B["ratio"] = B["instalment"].astype(float) / B["net_pay_at_origination"]
    B["age"] = 40
    pr = lr.predict_proba(X(B))[:, 1]
    sec = pd.Series(pr).groupby(B["sector"].values).sum().reindex(list(C.SECTORS))
    return dict(total=float(pr.sum()), sectors={k: float(v) for k, v in sec.items()}, pooled=float(H["y"].mean()),
                pooled_total=float(H["y"].mean() * len(B)), temp_rate=float(H[H["temp"]]["y"].mean()))


def ratio_route(target, cf=None):
    """the public 12-month default share scaled by the private employers' leaving rate over the public borrowers'
    rate of stopping being paid by the payroll"""
    L, R, D = load_public(target)
    dd = D.groupby("loan")["t"].min()
    L["dt"] = L["loan_no"].map(dd)
    H = L[L["d"] <= C.mi(2025, 12)]
    pd12 = float((H["dt"].notna() & (H["dt"] <= H["d"] + 12)).mean())
    S = runs(R)
    S = S[S["c"] <= C.mi(2025, 12)]
    end = np.minimum(L["d"] + L["term_months"], C.mi(2025, 12))
    expo = float(np.clip(end - L["d"], 0, None).sum())
    hpub = len(S.groupby("loan")["c"].min()) / expo
    cf = cf or call_figures(target)
    B, A = load_launch(target)
    hp = np.array([cf["h"][n] for n in B["employer_nit"]])
    return dict(total=float((pd12 * hp / hpub).sum()), hpub=hpub, pd12=pd12)


# -------------------------------------------------------------------------------------------------------- ask A
def ask_a(target):
    """for each sector: the savings contributions in the effective schedules of the 2026 months, and the part of it
    with no transfer received by 31 December 2026"""
    S = pd.read_csv(os.path.join(target, C.F_SCHED), dtype={"member_id": str, "employer_nit": str})
    T = pd.read_csv(os.path.join(target, C.F_STMT), dtype={"payer_id": str})
    A = pd.read_excel(os.path.join(target, C.F_AGREE), dtype=str)
    sec = dict(zip(A["employer_nit"], A["sector"]))
    S["contribution"] = S["contribution"].astype(float)
    tot = S.groupby(["schedule_no", "employer_nit", "period", "filed_on"])["contribution"].sum().reset_index()
    mem = S.groupby("schedule_no")["member_id"].apply(frozenset).to_dict()
    # a later schedule for the same employer and month whose members overlap the earlier one's replaces it
    eff = []
    for (nit, per), g in tot.sort_values(["filed_on", "schedule_no"]).groupby(["employer_nit", "period"]):
        keep = []
        for _, row in g.iterrows():
            ms = mem[row["schedule_no"]]
            for k in list(keep):
                if len(ms & mem[k["schedule_no"]]) >= 0.5 * len(mem[k["schedule_no"]]):
                    keep.remove(k)
            keep.append(row)
        eff.extend(keep)
    E = pd.DataFrame(eff)
    E26 = E[E["period"].str.startswith("2026")]
    # transfers: credits referencing a period, net of returned transfers
    tr = T[T["description"] == "TRANSFERENCIA RECIBIDA"].copy()
    rv = T[T["description"] == "DEVOLUCION TRANSFERENCIA"]
    for _, x in rv.iterrows():
        m = tr[(tr["payer_id"] == x["payer_id"]) & (tr["reference"] == x["reference"]) &
               (tr["credit"].astype(float) == float(x["debit"])) & (tr["posting_date"] <= x["posting_date"])]
        if len(m):
            tr = tr.drop(m.index[-1])
    tr["amt"] = tr["credit"].astype(float)
    tr["per"] = tr["reference"].str.extract(r"(\d\d)/(\d{4})").apply(lambda r: "%s-%s" % (r[1], r[0]), axis=1)
    # match each transfer to the effective schedules it pays: same payer and month, or the payer's month together
    # with another employer's schedule for the same month whose sum it equals; otherwise the payer's open months in
    # order
    open_ = {r["schedule_no"]: r for _, r in E.iterrows()}
    paid = set()
    for _, x in tr.sort_values("posting_date").iterrows():
        own = [s for s in open_.values() if s["employer_nit"] == x["payer_id"] and s["schedule_no"] not in paid]
        same = [s for s in own if s["period"] == x["per"]]
        amt = x["amt"]
        hit = None
        for s in same:
            if abs(s["contribution"] - amt) < 0.5:
                hit = [s]
                break
        others = [o for o in open_.values() if o["period"] == x["per"] and o["employer_nit"] != x["payer_id"]
                  and o["schedule_no"] not in paid]
        if hit is None:
            single = [o for o in others if abs(o["contribution"] - amt) < 0.5]
            if len(single) == 1:
                hit = single
        if hit is None and same:
            for s in same:
                for o in others:
                    if abs(s["contribution"] + o["contribution"] - amt) < 0.5:
                        hit = [s, o]
                        break
                if hit:
                    break
        if hit is None:
            cand = sorted(own, key=lambda s: s["period"])
            acc, pick = 0.0, []
            for s in cand:
                if acc + s["contribution"] <= amt + 0.5:
                    pick.append(s)
                    acc += s["contribution"]
                if abs(acc - amt) < 0.5:
                    break
            hit = pick if abs(acc - amt) < 0.5 else []
        for s in hit:
            paid.add(s["schedule_no"])
    E26 = E26.assign(sector=E26["employer_nit"].map(sec), paid=E26["schedule_no"].isin(paid))
    ded = E26.groupby("sector")["contribution"].sum().reindex(list(C.SECTORS))
    out = E26[~E26["paid"]].groupby("sector")["contribution"].sum().reindex(list(C.SECTORS)).fillna(0)
    return dict(deducted={k: float(v) for k, v in ded.items()}, outstanding={k: float(v) for k, v in out.items()})


# -------------------------------------------------------------------------------------------------------- ask B
def ask_b(target):
    """for the public loans that entered default in 2023 and in 2024, by unit type: receipts by 31 December 2026 net
    of reversals, other than transfers from the borrowing member's own savings account"""
    L, R, D = load_public(target)
    X = pd.read_csv(os.path.join(target, C.F_XWALK), dtype=str)
    canon = dict(zip(X["legacy_loan_no"], X["core_loan_no"]))
    Rc = pd.read_csv(os.path.join(target, C.F_RECEIPTS), dtype={"member_id": str, "loan_reference": str, "originating_account": str})
    Sv = pd.read_csv(os.path.join(target, C.F_SAVINGS), dtype={"member_id": str})
    own = dict(Sv.groupby("savings_account")["member_id"].first())
    Rc["loan"] = Rc["loan_reference"].map(lambda r: canon.get(r, r))
    Rc["amount"] = Rc["amount"].astype(float)
    Rc["own"] = Rc["originating_account"].map(own) == Rc["member_id"]
    # a reversal undoes its receipt (same receipt number with R)
    rev = set(Rc[Rc["channel"] == "REVERSO"]["receipt_id"].str[:-1])
    ok = Rc[(Rc["channel"] != "REVERSO") & (~Rc["receipt_id"].isin(rev))]
    typ = dict(zip(L["loan_no"], L["unit_type"]))
    D["year"] = D["default_date"].str[:4].astype(int)
    out = {}
    for y in (2023, 2024):
        loans = set(D[D["year"] == y]["loan"])
        g = ok[ok["loan"].isin(loans) & (~ok["own"])]
        s = g.groupby(g["loan"].map(typ))["amount"].sum().reindex(list(C.AGENCY_TYPES)).fillna(0)
        out[y] = {k: float(v) for k, v in s.items()}
    return out
