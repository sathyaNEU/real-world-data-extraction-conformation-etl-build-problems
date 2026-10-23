"""The golden for task171, computed from the shipped files in target/ only, plus the rival routes checks.py
measures. Prices come from common.py here; verify.py reads them from the shipped rate schedules."""
from __future__ import annotations

import os
import warnings

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import statsmodels.api as sm

import common as C

warnings.filterwarnings("ignore")
OFFER = pd.Timestamp("2024-03-01")
ASOF = pd.Timestamp("2026-10-31")
LAUNCH = pd.Timestamp("2027-01-01")
PRE = ["%04d-%02d" % C.MONTHS[i] for i in C.PRE_A]
TEST = ["%04d-%02d" % C.MONTHS[i] for i in C.TEST]


def load(tdir):
    ami = pq.read_table(os.path.join(tdir, C.F_AMI)).to_pandas()
    sa = pd.read_csv(os.path.join(tdir, C.F_SVC), dtype=str, keep_default_na=False)
    rate = pd.read_csv(os.path.join(tdir, C.F_RATE), dtype=str, keep_default_na=False)
    sa["start"] = pd.to_datetime(sa.service_start, format="%m/%d/%Y")
    sa["end"] = pd.to_datetime(sa.service_end.replace("", None), format="%m/%d/%Y")
    rate["f"] = pd.to_datetime(rate.eff_from)
    rate["t"] = pd.to_datetime(rate.eff_to.replace("", None))
    return ami, sa, rate


def use_by(ami, months, keep_actual=False):
    """billed use per service and period over the billing months given; one row per meter-month unless a
    re-collected actual row stands beside an estimate (then the actual is kept, keep_actual)"""
    a = ami[ami.bill_month.isin(months)]
    if keep_actual:
        dup = a.duplicated(["meter_no", "service_acct", "bill_month", "read_from"], keep=False)
        a = a[~(dup & (a.read_type == "EST"))]
    g = a.groupby("service_acct")[C.PERIODS].sum()
    n = a.groupby("service_acct").bill_month.nunique()
    return g, n


def spells(rate, sa):
    """rate spells per service: contiguous rows of one code joined; an open R-TOU row on a closed service ends at the
    service's final read"""
    r = rate.sort_values(["service_acct", "f"]).copy()
    end = sa.set_index("service_acct").end
    r["t2"] = r.t
    miss = r.t2.isna()
    r.loc[miss, "t2"] = r.loc[miss, "service_acct"].map(end)
    prev_code = r.groupby("service_acct").rate_code.shift()
    prev_t = r.groupby("service_acct").t2.shift()
    new = ~((prev_code == r.rate_code) & (prev_t + pd.Timedelta(days=1) == r.f))
    r["sp"] = new.cumsum()
    s = r.groupby("sp").agg(service_acct=("service_acct", "first"), code=("rate_code", "first"), f=("f", "min"), t=("t2", "max"),
                            open_end=("t2", lambda x: x.isna().any()))
    s.loc[s.open_end, "t"] = pd.NaT
    return s.reset_index(drop=True)


def saving_A(u):
    return u.sum(1) * C.R1_2024["e"] - (u[C.PERIODS[2]] * C.RTOU_2024["peak"] + (u.sum(1) - u[C.PERIODS[2]]) * C.RTOU_2024["other"])


def saving_B(u):
    return u.sum(1) * C.R1_2027["e"] - (u[C.PERIODS[0]] * C.RON_2027["off"] + (u.sum(1) - u[C.PERIODS[0]]) * C.RON_2027["other"])


def frames(tdir):
    ami, sa, rate = load(tdir)
    sp = spells(rate, sa)
    # the offer cohort: services open and on R-1 on 1 March 2024
    on_r1 = sp[(sp.code == "R-1") & (sp.f <= OFFER) & ((sp.t.isna()) | (sp.t >= OFFER))].service_acct
    coh = sa[sa.service_acct.isin(on_r1) & (sa.start < OFFER) & (sa.end.isna() | (sa.end > OFFER))].copy()
    tou = sp[sp.code == "R-TOU"].groupby("service_acct").f.min()
    coh["tou_f"] = coh.service_acct.map(tou)
    coh["k"] = (coh.tou_f.dt.year - 2024) * 12 + coh.tou_f.dt.month - 3
    coh.loc[coh.tou_f.isna(), "k"] = 999
    coh["k_end"] = np.where(coh.end.isna(), 99, (coh.end.dt.year - 2024) * 12 + coh.end.dt.month - 3)
    u0, n0 = use_by(ami, PRE)
    coh = coh.join(u0, on="service_acct").fillna({p: 0.0 for p in C.PERIODS})
    coh["savA"] = saving_A(coh[C.PERIODS])
    coh["kwhA"] = coh[C.PERIODS].sum(1)
    # the forecast population: services open and on R-1 at 31 October 2026
    on_r1b = sp[(sp.code == "R-1") & (sp.f <= ASOF) & (sp.t.isna() | (sp.t >= ASOF))].service_acct
    pop = sa[sa.service_acct.isin(on_r1b) & sa.end.isna()].copy()
    u1, n1 = use_by(ami, TEST)
    pop = pop[pop.service_acct.map(n1).fillna(0).values == 12].copy()      # billed for all twelve test-year months
    pop = pop.join(u1, on="service_acct").fillna({p: 0.0 for p in C.PERIODS})
    pop["savB"] = saving_B(pop[C.PERIODS])
    pop["kwhB"] = pop[C.PERIODS].sum(1)
    return dict(ami=ami, sa=sa, rate=rate, sp=sp, coh=coh, pop=pop)


def hazard_fit(coh, x):
    X, Y = [], []
    for k in range(12):
        risk = (coh.k.values >= k) & (coh.k_end.values >= k)
        d = np.zeros((risk.sum(), 12)); d[:, k] = 1
        X.append(np.column_stack([x[risk], d])); Y.append((coh.k.values[risk] == k).astype(float))
    return sm.Logit(np.concatenate(Y), np.vstack(X)).fit(disp=0)


def hazard_path(m, xB):
    surv = np.ones(len(xB)); out = []
    for k in range(12):
        d = np.zeros((len(xB), 12)); d[:, k] = 1
        surv = surv * (1 - m.predict(np.column_stack([xB, d])))
        out.append(1 - surv)
    return out


def golden(F):
    coh, pop = F["coh"], F["pop"]
    m = hazard_fit(coh, coh.savA.values)
    path = hazard_path(m, pop.savB.values)
    P12 = path[11]
    res = dict(members=float(P12.sum()), shortfall=float((P12 * pop.savB.values).sum()),
               quarters=[float(path[q].sum()) for q in (2, 5, 8, 11)],
               b=float(m.params[0]), cohort=int(len(coh)), pop=int(len(pop)),
               takers12=int((coh.k < 12).sum()))
    res["by_district"] = pop.assign(p=P12, s=P12 * pop.savB.values).groupby("district")[["p", "s"]].sum().to_dict()
    return res, P12


def family(F):
    """the golden family: constructions of the same quantity a competent analyst could choose"""
    coh, pop = F["coh"], F["pop"]
    xA, xB, sB = coh.savA.values, pop.savB.values, pop.savB.values
    out = {}
    g, _ = golden(F)
    out["hazard"] = (g["members"], g["shortfall"])
    surv = coh.k_end.values >= 11
    y = (coh.k.values < 12).astype(float)
    for name, mdl in (("logit12", sm.Logit), ("probit12", sm.Probit)):
        mm = mdl(y[surv], sm.add_constant(xA[surv])).fit(disp=0)
        p = mm.predict(sm.add_constant(xB)); out[name] = (p.sum(), (p * sB).sum())
    mm = sm.Logit(y, sm.add_constant(xA)).fit(disp=0)          # closed services counted as not taking it
    p = mm.predict(sm.add_constant(xB)); out["logit12_all"] = (p.sum(), (p * sB).sum())
    Xc = sm.add_constant(np.column_stack([xA, coh.kwhA.values / 1000]))
    mm = sm.Logit(y[surv], Xc[surv]).fit(disp=0)
    p = mm.predict(sm.add_constant(np.column_stack([xB, pop.kwhB.values / 1000]))); out["logit12_kwh"] = (p.sum(), (p * sB).sum())
    for nb in (20, 40):
        bins = np.quantile(xA[surv], np.linspace(0, 1, nb + 1)); bins[0] = -1e9; bins[-1] = 1e9
        ia = np.digitize(xA, bins) - 1
        r = np.array([y[surv & (ia == j)].mean() for j in range(nb)])
        p = r[np.clip(np.digitize(xB, bins) - 1, 0, nb - 1)]
        out["bins%d" % nb] = (p.sum(), (p * sB).sum())
    dmy = pd.get_dummies(coh.district).values.astype(float)[:, 1:]
    dmyB = pd.get_dummies(pop.district).values.astype(float)[:, 1:]
    mm = sm.Logit(y[surv], sm.add_constant(np.column_stack([xA, dmy]))[surv]).fit(disp=0)
    p = mm.predict(sm.add_constant(np.column_stack([xB, dmyB]))); out["logit12_district"] = (p.sum(), (p * sB).sum())
    return out


def rivals(F):
    """the routes that skip or misplace the decisive step"""
    coh, pop, ami = F["coh"], F["pop"], F["ami"]
    sB = pop.savB.values
    surv = coh.k_end.values >= 11
    y = (coh.k.values < 12).astype(float)
    out = {}
    rate = y[surv].mean()
    out["rate_x_average"] = (rate * len(pop), rate * sB.sum())                      # rung 0
    yc = (coh.k.values < 99).astype(float)
    out["cumulative_rate"] = (yc.mean() * len(pop), yc.mean() * sB.sum())
    tk = coh[(coh.k < 12)]
    sB_of = pop.set_index("service_acct").savB
    u1, _ = use_by(ami, TEST)
    tk_B = saving_B(u1.reindex(tk.service_acct).fillna(0.0))
    out["takers_profile"] = (rate * len(pop), rate * len(pop) * tk_B.mean())
    pos = sB > 0
    out["savers_only"] = (rate * len(pop), rate * len(pop) * sB[pos].mean())
    # the textbook route: take-up on own saving, the saving read on the latest twelve billing months
    uL, _ = use_by(ami, TEST)
    xL = saving_A(uL.reindex(coh.service_acct).fillna(0.0)).values
    ok = surv & (uL.reindex(coh.service_acct)[C.PERIODS[0]].notna().values)
    mm = sm.Logit(y[ok], sm.add_constant(xL[ok])).fit(disp=0)
    p = mm.predict(sm.add_constant(sB)); out["saving_on_latest_use"] = (p.sum(), (p * sB).sum())
    m2 = hazard_fit(coh.assign(k_end=np.where(ok, coh.k_end, -1)), xL)
    p2 = hazard_path(m2, sB)[11]; out["saving_on_latest_use_hazard"] = (p2.sum(), (p2 * sB).sum())
    allm = sorted(ami.bill_month.unique())
    uA, nA = use_by(ami, allm)
    xa = (saving_A(uA) * 12 / nA).reindex(coh.service_acct).fillna(0.0).values
    mm = sm.Logit(y[surv], sm.add_constant(xa[surv])).fit(disp=0)
    p = mm.predict(sm.add_constant(sB)); out["saving_on_all_years"] = (p.sum(), (p * sB).sum())
    pctA = coh.savA.values / np.maximum(coh.kwhA.values * C.R1_2024["e"], 1)
    pctB = sB / np.maximum(pop.kwhB.values * C.R1_2027["e"], 1)
    mm = sm.Logit(y[surv], sm.add_constant(pctA[surv])).fit(disp=0)
    p = mm.predict(sm.add_constant(pctB)); out["saving_in_per_cent"] = (p.sum(), (p * sB).sum())
    shA = coh[C.PERIODS[2]].values / np.maximum(coh.kwhA.values, 1)
    shB = pop[C.PERIODS[2]].values / np.maximum(pop.kwhB.values, 1)
    Xa = sm.add_constant(np.column_stack([coh.kwhA.values / 1000, shA]))
    mm = sm.Logit(y[surv], Xa[surv]).fit(disp=0)
    p = mm.predict(sm.add_constant(np.column_stack([pop.kwhB.values / 1000, shB]))); out["load_shape_covariates"] = (p.sum(), (p * sB).sum())
    return out


ASK_MONTHS = ["2024-03", "2024-04", "2024-05"]


def ask_A(F):
    """by district of the service location: services on R-TOU at 31 October 2026, of which on it since 1 November
    2025 or earlier, and their 4 p.m. to 9 p.m. kWh in billing months November 2025 to October 2026"""
    sa, sp, ami = F["sa"], F["sp"], F["ami"]
    t = sp[(sp.code == "R-TOU") & (sp.f <= ASOF) & (sp.t.isna() | (sp.t >= ASOF))]
    act = sa[sa.end.isna()].set_index("service_acct")
    t = t[t.service_acct.isin(act.index)].copy()
    t["district"] = t.service_acct.map(act.district)
    t["long"] = t.f <= pd.Timestamp("2025-11-01")
    u, _ = use_by(ami, TEST, keep_actual=True)
    t["peak"] = t.service_acct.map(u[C.PERIODS[2]]).fillna(0.0)
    t["night"] = t.service_acct.map(u[C.PERIODS[0]]).fillna(0.0)
    g = t.groupby("district").agg(on=("service_acct", "size"), long=("long", "sum"), kwh=("peak", "sum"), night=("night", "sum"))
    return {d: dict(on=int(g.on[d]), twelve=int(g.long[d]), kwh=int(round(g.kwh[d])), night=int(round(g.night[d]))) for d in C.DISTRICTS}


def local_month(utc_str):
    ts = pd.to_datetime(utc_str, utc=True).dt.tz_convert("America/Chicago")
    return ts.dt.strftime("%Y-%m")


def ask_B(tdir, F):
    """R-TOU enrolment requests received in March, April and May 2024 (local time), a duplicate submission counted
    once, by the district of the service whose rate the request asked to change"""
    crm = pd.read_excel(os.path.join(tdir, C.F_CRM), dtype=str)
    sa, sp = F["sa"], F["sp"]
    crm["lm"] = local_month(crm.received_utc)
    r = crm[(crm.request == "Enrol R-TOU") & crm.lm.isin(ASK_MONTHS) & (crm.status != "Closed - duplicate")].copy()
    mem = sa.set_index("service_acct").membership_no
    by_mem = sa.groupby("membership_no").service_acct.apply(list)
    tou = sp[sp.code == "R-TOU"].groupby("service_acct").f.min()
    dist = sa.set_index("service_acct").district

    def target(row):
        if row.status != "Completed":
            return row.service_acct
        done = pd.Timestamp(row.completed_on)
        cands = [row.service_acct] + [s for s in by_mem.get(mem.get(row.service_acct), []) if s != row.service_acct]
        for s in cands:
            f = tou.get(s)
            if f is not None and 0 <= (f - done).days <= 45:
                return s
        return row.service_acct
    r["target"] = r.apply(target, axis=1)
    r["district"] = r.target.map(dist)
    g = r.groupby("district").size()
    w = r[r.channel == "Web form"].groupby("district").size()
    return {d: dict(requests=int(g.get(d, 0)), web=int(w.get(d, 0))) for d in C.DISTRICTS}
