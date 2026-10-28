"""The golden's analysis and every rival route, computed from the shipped tables only.

checks.py asserts on these figures; writeup.py states them; verify.py recomputes the graded ones from the files on
disk without importing this module."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import params as P

TXN = {"SELF": "OWN", "GS": "GRP_SUPP", "NIL": "NOT_PAID"}
CALL_INPUTS = ("pool_tape", "kshetra", "collectpro", "migmap")     # every table the main call reads


def unify(s):
    """One ledger across both platforms, on Kshetra ids where the migration map gives them."""
    mm = s["migmap"]
    mmap = dict(zip(mm.collectpro_id[mm.entity == "MEMBER"], mm.kshetra_id[mm.entity == "MEMBER"]))
    lmap = dict(zip(mm.collectpro_id[mm.entity == "LOAN"], mm.kshetra_id[mm.entity == "LOAN"]))
    gmap = dict(zip(mm.collectpro_id[mm.entity == "GROUP"], mm.kshetra_id[mm.entity == "GROUP"]))
    cp = s["collectpro"]
    gkey = cp.CENTRE + "-" + cp.GRP.astype(str)
    old = pd.DataFrame({
        "date": pd.to_datetime(cp.MTG_DT, format="%d/%m/%Y"),
        "group": gkey.map(gmap).fillna(gkey),
        "member": cp.MEM_CODE.map(mmap).fillna(cp.MEM_CODE),
        "loan": cp.LOAN_AC.map(lmap).fillna(cp.LOAN_AC),
        "inst": cp.INST.astype(int),
        "txn": cp.MODE.map(TXN),
    })
    ks = s["kshetra"]
    new = pd.DataFrame({"date": pd.to_datetime(ks.meeting_date), "group": ks.group_id, "member": ks.member_id,
                        "loan": ks.loan_id, "inst": ks.instalment_no.astype(int), "txn": ks.txn_type})
    return pd.concat([old, new], ignore_index=True)


def facts(led):
    lf = led.groupby("loan").agg(first_date=("date", "min"), last_date=("date", "max"), min_inst=("inst", "min"),
                                 max_inst=("inst", "max"), group=("group", "last"))
    fu = led[led.txn == "NOT_PAID"].groupby("loan").date.min()
    lf["first_unpaid"] = fu
    # disbursement: fourteen days before instalment 1, read back from the earliest instalment the ledger holds
    lf["disbursed"] = lf.first_date - pd.to_timedelta(14 * lf.min_inst, unit="D")
    gm = led.groupby(["group", "date"]).txn.apply(lambda s: int((s == "GRP_SUPP").sum())).rename("k").reset_index()
    return lf, gm


def asof_frame(led, lf, gm, E, mhp=True):
    """Loans current at as-of E (a Timestamp): rows on or before E, no unpaid instalment due on or before E, the
    schedule not finished; with the group's carried count at its last meeting on or before E (k) and the larger of
    its last two meetings (k2)."""
    upto = led[led.date <= E]
    lastrow = upto.groupby("loan").agg(d=("date", "max"), inst=("inst", "max"), group=("group", "last"))
    lastrow = lastrow.join(lf[["first_unpaid", "disbursed"]])
    cur = lastrow[(lastrow.first_unpaid.isna() | (lastrow.first_unpaid > E)) & (lastrow.inst < P.INSTALMENTS)]
    if mhp:
        cur = cur[cur.disbursed <= E - pd.Timedelta(days=P.MHP_DAYS)]
    g = gm[gm.date <= E].sort_values("date").groupby("group").tail(2)
    last = g.groupby("group").tail(1).set_index("group")
    k2 = g.groupby("group").k.max().rename("k2")
    cur = cur.join(last.rename(columns={"date": "gdate"}), on="group").join(k2, on="group")
    return cur


def history(led, lf, gm, step="month", mhp=True, start=None):
    ends = []
    last = led.date.max()
    d = pd.Timestamp(P.HIST_START)
    if step == "month":
        e = (d + pd.offsets.MonthEnd(0))
        while e + pd.Timedelta(days=P.HORIZON_DAYS) <= last:
            ends.append(e)
            e = e + pd.offsets.MonthEnd(1)
    else:
        meets = np.sort(led.date.unique())
        ends = [pd.Timestamp(x) for x in meets if pd.Timestamp(x) + pd.Timedelta(days=P.HORIZON_DAYS) <= last]
    if start is not None:
        ends = [e for e in ends if e >= start]
    frames = []
    for E in ends:
        f = asof_frame(led, lf, gm, E, mhp=mhp)
        f = f.assign(E=E, out=(f.first_unpaid <= E + pd.Timedelta(days=P.HORIZON_DAYS - P.DPD_LINE)).fillna(False))
        frames.append(f[["E", "k", "k2", "out", "group"]].assign(loan=f.index))
    return pd.concat(frames, ignore_index=True)


def rates(h, key="k3"):
    h = h.assign(k3=h.k.clip(upper=3))
    return h.groupby(key).out.agg(["mean", "size", "sum"])


def pool_states(s, led, gm):
    E = pd.Timestamp(P.CUTOFF)
    pt = s["pool_tape"]
    g = gm[gm.date <= E].sort_values("date").groupby("group").tail(2)
    gl = g.groupby("group").tail(1).set_index("group")
    k2 = g.groupby("group").k.max().rename("k2")
    st = pt[["loan_id", "member_id", "group_id", "district", "branch_code"]].join(gl, on="group_id").join(k2, on="group_id")
    st["k3"] = st.k.clip(upper=3)
    # each member's own posting at her last meeting
    lastm = led[(led.date <= E)].sort_values("date").groupby("loan").tail(1).set_index("loan")
    st["own_carried"] = st.loan_id.map(lastm.txn).eq("GRP_SUPP").astype(int)
    return st


def forecast(r, st, col="k3"):
    return float(sum(r.loc[k, "mean"] * (st[col] == k).sum() for k in r.index))


def main_call(s):
    led = unify(s)
    lf, gm = facts(led)
    h = history(led, lf, gm, "month")
    r = rates(h)
    st = pool_states(s, led, gm)
    gold = forecast(r, st)
    by_d = {d: float(sum(r.loc[k, "mean"] * ((st.k3 == k) & (st.district == d)).sum() for k in r.index))
            for d in P.DISTRICTS}
    return dict(led=led, lf=lf, gm=gm, hist=h, rates=r, states=st, gold=gold, by_district=by_d)


def rivals(s, mc):
    """The ladder's rungs and the golden family's members."""
    led, lf, gm, h, st = mc["led"], mc["lf"], mc["gm"], mc["hist"], mc["states"]
    out = {}
    # rung 0: the loan-level six-month roll rate from the current bucket
    out["roll_rate"] = float(h.out.mean() * len(st))
    # rung 1: each member's own posting at her last meeting before the as-of
    led_last = led.sort_values("date")
    hh = h.copy()
    own = []
    for E, g in hh.groupby("E"):
        lm = led_last[led_last.date <= E].groupby("loan").tail(1).set_index("loan").txn
        own.append(g.loan.map(lm).eq("GRP_SUPP").astype(int))
    hh["own"] = pd.concat(own).reindex(hh.index).values
    ro = hh.groupby("own").out.mean()
    out["own_posting"] = float(sum(ro.loc[k] * (st.own_carried == k).sum() for k in ro.index))
    # the group flagged when it carried anyone at its last meeting
    hh["anyk"] = (hh.k > 0).astype(int)
    ra = hh.groupby("anyk").out.mean()
    st_any = (st.k > 0).astype(int)
    out["group_any"] = float(sum(ra.loc[k] * (st_any == k).sum() for k in ra.index))
    # every member carried at the cut-off defaults, the rest at the history's rate for members paying themselves
    out["carried_all"] = float(st.own_carried.sum() + ro.loc[0] * (st.own_carried == 0).sum())
    # the group read on the distinct members it carried over its last six meetings
    sup = led[led.txn == "GRP_SUPP"][["group", "date", "member"]]
    meet = gm[["group", "date"]].sort_values(["group", "date"])
    meet["rank"] = meet.groupby("group").cumcount()
    sup = sup.merge(meet, on=["group", "date"])

    def window_k(frame, E_col=None, E=None):
        ks = []
        for EE, g in (frame.groupby(E_col) if E_col else [(E, frame)]):
            lm = meet[meet.date <= EE].groupby("group").tail(1).set_index("group")["rank"]
            s2 = sup[sup.date <= EE]
            s2 = s2.join(lm.rename("lr"), on="group")
            s2 = s2[s2["rank"] > s2.lr - 6]
            kw = s2.groupby("group").member.nunique()
            ks.append(g.group.map(kw).fillna(0).clip(upper=3).astype(int))
        return pd.concat(ks).reindex(frame.index)
    hh["kw"] = window_k(hh, "E").values
    rw = hh.groupby("kw").out.mean()
    st_kw = window_k(st.assign(group=st.group_id), E=pd.Timestamp(P.CUTOFF))
    out["group_window"] = float(sum(rw.loc[k] * (st_kw == k).sum() for k in rw.index))
    # golden family members
    h_meet = history(led, lf, gm, "meeting")
    out["fam_every_meeting"] = forecast(rates(h_meet), st)
    h_nomhp = history(led, lf, gm, "month", mhp=False)
    out["fam_no_mhp"] = forecast(rates(h_nomhp), st)
    out["fam_kshetra_only"] = forecast(rates(h[h.E >= pd.Timestamp(P.MIGRATION)]), st)
    # the group's state as the larger of its last two meetings
    gm2 = gm.sort_values(["group", "date"]).copy()
    gm2["k2"] = gm2.groupby("group").k.transform(lambda x: x.rolling(2, min_periods=1).max()).astype(int)
    h2 = h.drop(columns=["k"]).copy()
    ks = []
    for E, g in h2.groupby("E"):
        gl = gm2[gm2.date <= E].groupby("group").tail(1).set_index("group").k2
        ks.append(g.group.map(gl))
    h2["k"] = pd.concat(ks).reindex(h2.index).values
    gl2 = gm2[gm2.date <= pd.Timestamp(P.CUTOFF)].groupby("group").tail(1).set_index("group").k2
    st2 = st.assign(k3=st.group_id.map(gl2).clip(upper=3))
    out["fam_last_two"] = forecast(rates(h2), st2)
    out["fam_two_plus"] = forecast(rates(h.assign(k=h.k.clip(upper=2))), st.assign(k3=st.k.clip(upper=2)))
    return out


# ---- the asks -------------------------------------------------------------------------------------------------

def ask_bureau(s):
    """Pool borrowers in breach of the bank's microfinance guardrails on the bureau at the cut-off, by branch, and the
    pool principal outstanding on their loans (INR lakh); with the rivals' figures."""
    cic, d = s["cic"], s["cic_directory"]
    inst = dict(zip(d.member_code, d.institution))
    parent = {r.member_code: (r.parent_code or r.member_code) for r in d.itertuples()}
    succ = {r.member_code: (r.successor_code or r.member_code) for r in d.itertuples()}

    def institution(code):
        return inst[succ[parent[code]]]
    mf = cic[cic.account_type.isin(["JLG", "MFI-IND"]) & (cic.account_status == "ACTIVE")].copy()
    mf["dt_rep"] = pd.to_datetime(mf.date_reported)
    mf = mf.sort_values(["inquiry_ref", "dt_rep"])
    # a loan reported under two account numbers is one loan, taken at its latest report
    once = mf.drop_duplicates(["inquiry_ref", "member_code", "date_opened", "sanctioned_amount"], keep="last")
    once = once.assign(entity=once.member_code.map(institution))
    kyc = s["kyc"][["member_id", "cic_ref"]]
    pt = s["pool_tape"][["member_id", "branch_code", "principal_outstanding_inr"]].merge(kyc, on="member_id")

    def score(frame, ent_col):
        g = frame.groupby("inquiry_ref").agg(lenders=(ent_col, "nunique"), debt=("current_balance", "sum"))
        b = pt.join(g, on="cic_ref")
        b["breach"] = (b.lenders >= 4) | (b.debt > 200000)
        n = b.groupby("branch_code").breach.sum().astype(int)
        lakh = b[b.breach].groupby("branch_code").principal_outstanding_inr.sum().reindex(n.index).fillna(0) / 1e5
        return n, lakh.round(1), b
    gold_n, gold_l, borrower = score(once, "entity")
    out = dict(gold_n=gold_n, gold_l=gold_l, borrower=borrower)
    # rivals: the bureau's own summary columns; member codes counted as lenders; stale rows kept; institutions by
    # the directory's successor only (its parent link ignored, the correspondent's code counted apart)
    summ = cic.groupby("inquiry_ref")[["summary_active_mfi_lenders", "summary_mfi_outstanding"]].first()
    b2 = pt.join(summ, on="cic_ref")
    b2["breach"] = (b2.summary_active_mfi_lenders >= 4) | (b2.summary_mfi_outstanding > 200000)
    out["summary_n"] = b2.groupby("branch_code").breach.sum().astype(int)
    out["codes_n"], out["codes_l"], _ = score(once.assign(code=once.member_code), "code")
    out["stale_n"], out["stale_l"], _ = score(mf.assign(entity=mf.member_code.map(institution)), "entity")
    out["succ_only_n"], out["succ_only_l"], _ = score(once.assign(e2=once.member_code.map(succ)), "e2")
    return out


def ask_cyclone(s, reorg, declared):
    """The pool's principal outstanding in the GPs declared severely affected, by coastal district, INR lakh."""
    moved = {}
    renamed = {}
    for r in reorg:
        if r["kind"] == "split":
            for v in r["moved"]:
                moved[(r["block"], v)] = r["new"]
        else:
            renamed[(r["block"], r["old"])] = r["new"]
    k = s["kyc"]
    pt = s["pool_tape"][["member_id", "principal_outstanding_inr"]].merge(k, on="member_id")

    def now(row):
        if (row.block, row.village) in moved:
            return moved[(row.block, row.village)]
        return renamed.get((row.block, row.gram_panchayat), row.gram_panchayat)
    pt["gp_now"] = [now(r) for r in pt.itertuples()]
    coastal = ["Kendrapara", "Jagatsinghpur", "Bhadrak", "Balasore"]
    gold = {d: round(pt[(pt.district == d) & pt.gp_now.isin(declared)].principal_outstanding_inr.sum() / 1e5, 1)
            for d in coastal}
    naive = {d: round(pt[(pt.district == d) & pt.gram_panchayat.isin(declared)].principal_outstanding_inr.sum() / 1e5, 1)
             for d in coastal}
    ren_only = pt.assign(g2=[renamed.get((b, g), g) for b, g in zip(pt.block, pt.gram_panchayat)])
    renamed_fix = {d: round(ren_only[(ren_only.district == d) & ren_only.g2.isin(declared)].principal_outstanding_inr.sum() / 1e5, 1)
                   for d in coastal}
    return dict(gold=gold, naive=naive, renamed_only=renamed_fix, frame=pt)


def family(s, mc):
    """The golden's construction under every combination of the choices it leaves to the analyst: as-of at each
    month-end or at each meeting; the minimum holding period applied to the history or not; the whole ledger or the
    Kshetra months only; the group's state at its last meeting or the larger of its last two; states 0, 1, 2, 3+ or
    0, 1, 2+."""
    led, lf, gm, st = mc["led"], mc["lf"], mc["gm"], mc["states"]
    hs = {("month", True): mc["hist"]}
    for step in ("month", "meeting"):
        for mhp in (True, False):
            if (step, mhp) not in hs:
                hs[(step, mhp)] = history(led, lf, gm, step, mhp=mhp)
    out = {}
    for (step, mhp), h in hs.items():
        for span in ("all", "kshetra"):
            hh = h if span == "all" else h[h.E >= pd.Timestamp(P.MIGRATION)]
            for state in ("last", "last_two"):
                for cap in (3, 2):
                    col = "k" if state == "last" else "k2"
                    r = hh.assign(kk=hh[col].clip(upper=cap)).groupby("kk").out.mean()
                    pk = st[col].clip(upper=cap)
                    out[(step, mhp, span, state, cap)] = float(sum(r.loc[k] * (pk == k).sum() for k in r.index))
    return out


def regime_chain(s, mc, lo, hi):
    """A group-level transition chain: a group's carried count at one meeting (0, 1, 2, 3 or more) to its count at the
    next, or to stopped (the next meeting's rows all unpaid), estimated on meetings from lo to hi whose next meeting also
    falls by hi; then run forward from each pool group's count at its last meeting on or before the cut-off over its
    meetings due on or before the day 90 days ahead of 30 June 2027. Calibrated on the experience before the cyclone it is
    another construction of the golden; calibrated on the cyclone's own months it carries them into 2027."""
    if "chain_g" not in mc:
        led = mc["led"]
        t = led.assign(sup=(led.txn == "GRP_SUPP").astype(int), unp=(led.txn == "NOT_PAID").astype(int), one=1)
        g = t.groupby(["group", "date"])[["sup", "unp", "one"]].sum().reset_index().sort_values(["group", "date"])
        g["k3"] = g.sup.clip(upper=3)
        g["stopped"] = g.unp == g.one
        nxt = g.groupby("group")
        g["to"] = np.where(nxt.stopped.shift(-1) == True, 4, nxt.k3.shift(-1))
        g["next_date"] = nxt.date.shift(-1)
        mc["chain_g"] = g
    g = mc["chain_g"]
    a = g[~g.stopped & g.next_date.notna() & (g.date >= lo) & (g.date <= hi) & (g.next_date <= hi)]
    M = np.zeros((5, 5))
    for k in range(4):
        sub = a[a.k3 == k]
        if len(sub):
            for j in range(5):
                M[k, j] = float((sub.to == j).mean())
        else:
            M[k, k] = 1.0
    M[4, 4] = 1.0
    pt = s["pool_tape"]
    st = mc["states"].set_index("loan_id")
    nd = pd.to_datetime(pt.next_due_on, dayfirst=True)
    line = pd.Timestamp(P.OUTCOME) - pd.Timedelta(days=P.DPD_LINE)
    steps = ((line - nd).dt.days // 14 + 1).clip(lower=0)
    frame = pd.DataFrame({"k3": st.loc[pt.loan_id, "k3"].values, "steps": steps.values})
    tot = 0.0
    for (k, n), sub in frame.groupby(["k3", "steps"]):
        v = np.zeros(5)
        v[int(k)] = 1.0
        for _ in range(int(n)):
            v = v @ M
        tot += v[4] * len(sub)
    return tot, int(len(a)), M


def windows_before_landfall(mc):
    """The golden's rates read only from as-ofs whose 181-day windows closed before the cyclone's landfall."""
    h = mc["hist"]
    hh = h[h.E + pd.Timedelta(days=P.HORIZON_DAYS) < pd.Timestamp(P.CYCLONE)]
    return forecast(rates(hh), mc["states"]), int(hh.E.nunique())
