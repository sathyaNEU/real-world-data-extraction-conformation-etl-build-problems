"""Every figure the write-up, the goldens and the checks use, computed once from the shipped tables (solve.py) and
written to figures.json. Nothing is typed downstream."""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd

import params as P
import solve as S

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_NAMES = {0: "none", 1: "one", 2: "two", 3: "three or more"}
BRANCH_ORDER = [b[0] for b in P.BRANCHES]
BRANCH_NAME = {b[0]: b[1] for b in P.BRANCHES}


def nearest(v, u):
    return int(round(v / u) * u)


def compute(shipped, aux, with_family=True):
    mc = S.main_call(shipped)
    rv = S.rivals(shipped, mc)
    fam = S.family(shipped, mc) if with_family else {}
    ab = S.ask_bureau(shipped)
    st = mc["states"]
    r = mc["rates"]
    F = {}
    F["pool_loans"] = int(len(shipped["pool_tape"]))
    F["mhp_days"] = int(P.MHP_DAYS)
    F["horizon_days"] = int(P.HORIZON_DAYS)
    F["dpd_line"] = int(P.DPD_LINE)
    F["pool_principal_lakh"] = round(shipped["pool_tape"].principal_outstanding_inr.sum() / 1e5, 2)
    F["call_unrounded"] = round(mc["gold"], 1)
    F["call"] = nearest(mc["gold"], 100)
    F["call_share_pct"] = round(100 * mc["gold"] / len(st), 1)
    for k in range(4):
        F["state_loans_%d" % k] = int((st.k3 == k).sum())
        F["state_rate_pct_%d" % k] = round(100 * float(r.loc[k, "mean"]), 2)
        F["state_hist_loanmonths_%d" % k] = int(r.loc[k, "size"])
        F["state_hist_events_%d" % k] = int(round(float(r.loc[k, "mean"]) * int(r.loc[k, "size"])))
        F["state_expected_%d" % k] = round(float(r.loc[k, "mean"]) * int((st.k3 == k).sum()), 1)
    F["state_loans_2plus"] = F["state_loans_2"] + F["state_loans_3"]
    F["state_groups_2plus"] = int(st[st.k3 >= 2].group_id.nunique())
    F["hist_first_asof"] = str(mc["hist"].E.min().date())
    F["hist_last_asof"] = str(mc["hist"].E.max().date())
    F["hist_loanmonths"] = int(len(mc["hist"]))
    F["ledger_rows"] = int(len(mc["led"]))
    for k, v in mc["by_district"].items():
        F["district_expected_%s" % k] = round(v, 1)
    for k, v in rv.items():
        F["rival_%s" % k] = round(v, 1)
        F["rival_%s_printed" % k] = nearest(v, 100)
    for key, v in fam.items():
        F["family_%s" % "_".join(str(x) for x in key)] = round(v, 1)
    if fam:
        F["family_min"] = round(min(fam.values()), 1)
        F["family_max"] = round(max(fam.values()), 1)
    # the record's own contrast: groups that carried two distinct members over six meetings, split by whether the two
    # were carried at the same meeting
    F.update(contrast(mc))
    F.update(edges(shipped, mc))
    # SF15 and SF16: the forecast months' repayment conditions (term sheet clause 12) and its strict reading
    land = pd.Timestamp(P.CYCLONE)
    for key, lo, hi in (("pre", pd.Timestamp(P.HIST_START), land - pd.Timedelta(days=1)),
                        ("pre_kshetra", pd.Timestamp(P.MIGRATION), land - pd.Timedelta(days=1)),
                        ("dec", pd.Timestamp(2026, 12, 1), pd.Timestamp(P.CUTOFF)),
                        ("novdec", pd.Timestamp(2026, 11, 1), pd.Timestamp(P.CUTOFF)),
                        ("post", land, pd.Timestamp(P.CUTOFF))):
        v, n, _ = S.regime_chain(shipped, mc, lo, hi)
        F["sf_chain_%s" % key] = round(v, 1)
        F["sf_chain_%s_printed" % key] = nearest(v, 100)
        F["sf_chain_%s_transitions" % key] = n
    v, n = S.windows_before_landfall(mc)
    F["sf_windows_before_landfall"] = round(v, 1)
    F["sf_windows_before_landfall_asofs"] = n
    # the ask
    for b in BRANCH_ORDER:
        F["ask_breach_%s" % b] = int(ab["gold_n"].get(b, 0))
        F["ask_lakh_%s" % b] = round(float(ab["gold_l"].get(b, 0.0)), 1)
        for rv_name in ("summary_n", "codes_n", "stale_n", "succ_only_n"):
            F["askriv_%s_%s" % (rv_name, b)] = int(ab[rv_name].get(b, 0))
        for rv_name in ("codes_l", "stale_l", "succ_only_l"):
            F["askriv_%s_%s" % (rv_name, b)] = round(float(ab[rv_name].get(b, 0.0)), 1)
    F["ask_breach_total"] = int(sum(F["ask_breach_%s" % b] for b in BRANCH_ORDER))
    F["ask_lakh_total"] = round(sum(F["ask_lakh_%s" % b] for b in BRANCH_ORDER), 1)
    cic = shipped["cic"]
    mf = cic[cic.account_type.isin(["JLG", "MFI-IND"]) & (cic.account_status == "ACTIVE")]
    pairs = mf.groupby(["inquiry_ref", "member_code", "date_opened", "sanctioned_amount"]).size()
    F["ask_same_loan_pairs"] = int((pairs > 1).sum())
    F["ask_stale_report_date"] = str(mf[mf.member_code == "SFB0014"].date_reported.min())
    return F, dict(mc=mc, rv=rv, fam=fam, ab=ab)


def contrast(mc):
    led, gm, h = mc["led"], mc["gm"], mc["hist"]
    sup = led[led.txn == "GRP_SUPP"][["group", "date", "member"]]
    meet = gm[["group", "date"]].sort_values(["group", "date"]).copy()
    meet["rank"] = meet.groupby("group").cumcount()
    sup = sup.merge(meet, on=["group", "date"])
    rows = []
    for E, g in h.groupby("E"):
        lm = meet[meet.date <= E].groupby("group").tail(1).set_index("group")["rank"]
        s2 = sup[sup.date <= E].join(lm.rename("lr"), on="group")
        s2 = s2[s2["rank"] > s2.lr - 6]
        kw = s2.groupby("group").member.nunique()
        rows.append(g.assign(kw=g.group.map(kw).fillna(0).astype(int)))
    hh = pd.concat(rows)
    two = hh[hh.kw >= 2]
    same = two[two.k >= 2]
    apart = two[two.k <= 1]
    return {"contrast_same_pct": round(100 * same.out.mean(), 1), "contrast_same_n": int(len(same)),
            "contrast_apart_pct": round(100 * apart.out.mean(), 1), "contrast_apart_n": int(len(apart))}


def edges(shipped, mc):
    """The forecast under readings the fork table closes as the same call (the cut-off meeting left out; the
    history's rates by district, by branch, by the loan's cycle counted in the ledger) and the estimate's own
    sampling interval, a bootstrap over groups."""
    gm, st, h, led = mc["gm"], mc["states"], mc["hist"], mc["led"]
    E = pd.Timestamp(P.CUTOFF)
    hh = h.assign(k3=h.k.clip(upper=3))
    pooled = hh.groupby("k3").out.mean()
    out = {}
    last = gm[gm.date < E].sort_values("date").groupby("group").tail(1).set_index("group").k.clip(upper=3)
    sk = st.group_id.map(last).fillna(0).astype(int)
    out["sf_cutoff_strict"] = round(float(sum(pooled.get(k, 0.0) * n for k, n in sk.value_counts().items())), 1)
    out["sf_cutoff_meetings"] = int((gm.date == E).sum())
    dist = {b[0]: b[2] for b in P.BRANCHES}
    hh = hh.assign(branch=hh.group.str[1:4])
    hh = hh.assign(district=hh.branch.map(dist))
    first = led.groupby("loan").agg(member=("member", "first"), start=("date", "min")).reset_index()
    first["cycle"] = first.sort_values("start").groupby("member").cumcount() + 1
    hh = hh.assign(cycle=hh.loan.map(first.set_index("loan").cycle.clip(upper=3)).fillna(1).astype(int))
    pc = shipped["pool_tape"].set_index("loan_id").loan_cycle.clip(upper=3)
    sp = st.assign(branch=st.branch_code, cycle=st.loan_id.map(pc).astype(int))

    def grain(col):
        rr = hh.groupby([col, "k3"]).out.mean()
        tot = 0.0
        for key, n in sp.groupby([col, "k3"]).size().items():
            tot += (rr[key] if key in rr.index else pooled[key[1]]) * n
        return round(float(tot), 1)
    for col in ("district", "branch", "cycle"):
        out["sf_grain_%s" % col] = grain(col)
    cnt = {k: int((st.k3 == k).sum()) for k in range(4)}
    g = hh.groupby(["group", "k3"]).out.agg(["sum", "size"]).reset_index()
    groups = g.group.unique()
    g["gi"] = g.group.map({x: i for i, x in enumerate(groups)})
    Sm = np.zeros((len(groups), 4))
    Nm = np.zeros((len(groups), 4))
    np.add.at(Sm, (g.gi.values, g.k3.values), g["sum"].values)
    np.add.at(Nm, (g.gi.values, g.k3.values), g["size"].values)
    rng = np.random.default_rng(7)
    vals = []
    for _ in range(400):
        w = np.bincount(rng.integers(0, len(groups), len(groups)), minlength=len(groups))
        s_ = (Sm * w[:, None]).sum(0)
        n_ = (Nm * w[:, None]).sum(0)
        r_ = np.where(n_ > 0, s_ / np.maximum(n_, 1), 0)
        vals.append(sum(r_[k] * cnt[k] for k in range(4)))
    out["boot_p025"] = round(float(np.percentile(vals, 2.5)), 1)
    out["boot_p975"] = round(float(np.percentile(vals, 97.5)), 1)
    return out


def write(F, path=os.path.join(HERE, "figures.json")):
    with open(path, "w") as f:
        json.dump(F, f, indent=1, sort_keys=True)
        f.write("\n")
