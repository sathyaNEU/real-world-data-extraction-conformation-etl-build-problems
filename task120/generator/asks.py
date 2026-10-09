"""The TY2025 files the supplementary asks run through, all off the main call's path.

  wage statements: the platform's e-file extract (parquet) and the capture vendor's paper keying
      file (fixed width), plus the employers' annual reconciliation summary (the referee)
  estimated payments: the prepayment ledger (UTC timestamps, transfers between periods), the
      returned-items file and the TIN-resolution register (shared with wage statements)
  capital gains: the Schedule D extract (latest version received) and the amended-return log
  the employer withholding-deposit ledger (dated by receipt; nothing graded runs through it)

Devices (ledger in DESIGN_NOTE.md): D8 the clock, H1 transfers, H2 returned items and H4 the
register on the receipts; D2 versions and H3 the loss limit on gains; D4 the paper channel and H4
on withholding. Every rate below is a parameter the build asserts against, never a label in a file.
"""
import math

import numpy as np
import pandas as pd

from common import stream, make_eins
import world as Wm

FLOORS = (214_000, 318_000, 742_000)          # adopted floors: tier 3, tier 2, tier 1 lower bounds
DUE = {1: "2025-04-15", 2: "2025-06-16", 3: "2025-09-15", 4: "2026-01-15"}
NOMINAL = {1: "2025-04-15", 2: "2025-06-15", 3: "2025-09-15", 4: "2026-01-15"}

CFG = dict(
    # wage statements
    n_employers=9_400, paper_only_share=0.085, both_share=0.026, both_paper_p=0.30,
    mis_w2=0.0175, resolve_p=0.83, nonfiler_statements=13_850,
    # estimated payments
    es_p=[(0, 0.012), (50_000, 0.02), (100_000, 0.05), (200_000, 0.27), (318_000, 0.43), (742_000, 0.62), (3_000_000, 0.72)],
    due_day_p=0.24, evening_due_p=0.27, evening_other_p=0.11, late_p=0.04,
    credit_p=0.30, credit_scale=(0.9, 2.6), misapplied_p=0.026,
    dishonour_p=0.050, represent_p=0.36, mis_es=0.019,
    # capital gains
    schd_p=[(0, 0.07), (50_000, 0.13), (100_000, 0.22), (214_000, 0.52), (742_000, 0.86), (5_000_000, 0.93)],
    gain_share=[(0, 0.04), (100_000, 0.05), (214_000, 0.075), (318_000, 0.13), (742_000, 0.30), (5_000_000, 0.42)],
    loss_p=[(0, 0.26), (214_000, 0.17), (742_000, 0.12)], loss_scale=0.11,
    amend_p=0.024, amend_big_p=0.118, big_gain=150_000, unacc_share=0.47, acc_up=(0.22, 0.65),
    unacc_cut=(0.40, 0.95), accepted_then_unacc=0.18,
)

EXTRACT = pd.Timestamp("2026-10-22")


def interp_steps(x, table):
    return np.interp(x, [a for a, _ in table], [b for _, b in table])


def household_tiers(W):
    """Tier of every TY2025 household (generator side, from the world): 1, 2, 3 or 0."""
    y = 2025
    act = Wm.active_mask(W, y)
    att = np.bincount(W.dep_owner, weights=W.kid_agi[y], minlength=W.n).astype(np.int64)
    tot = W.own[y] + att
    tier = np.zeros(W.n, np.int8)
    tier[act & (tot >= FLOORS[0])] = 3
    tier[act & (tot >= FLOORS[1])] = 2
    tier[act & (tot >= FLOORS[2])] = 1
    return tier, tot


def typo(tins, rng, taken):
    """A misreported TIN: two adjacent digits transposed or one digit keyed wrong; never a TIN
    that belongs to anyone in the files."""
    out = np.empty(len(tins), np.int64)
    for i, t in enumerate(tins):
        s = f"{int(t):09d}"
        for _ in range(80):
            if rng.random() < 0.55:
                j = int(rng.integers(0, 8))
                if s[j] == s[j + 1]:
                    continue
                c = s[:j] + s[j + 1] + s[j] + s[j + 2:]
            else:
                j = int(rng.integers(0, 9))
                c = s[:j] + str((int(s[j]) + int(rng.integers(1, 10))) % 10) + s[j + 1:]
            v = int(c)
            if c[0] != "0" and v not in taken:
                taken.add(v)
                out[i] = v
                break
        else:
            raise AssertionError("no typo")
    return out


def business_days_after(ts, k):
    d = ts.normalize()
    while k > 0:
        d = d + pd.Timedelta(days=1)
        if d.weekday() < 5:
            k -= 1
    return d


def to_utc(local):
    s = pd.Series(pd.to_datetime(local))
    s = s.dt.tz_localize("America/Chicago", nonexistent="shift_forward", ambiguous=False)
    return s.dt.tz_convert("UTC").dt.tz_localize(None)


def instalment_of_local(local):
    """The filed rule: the first instalment whose due date (11:59:59 pm Central, rolled) the
    payment is received by; the fourth takes everything after the third due date."""
    t = pd.Series(pd.to_datetime(local))
    out = np.full(len(t), 4, np.int8)
    for k in (3, 2, 1):
        cut = pd.Timestamp(DUE[k]) + pd.Timedelta(hours=23, minutes=59, seconds=59)
        out[(t <= cut).to_numpy()] = k
    return out


# ------------------------------------------------------------------ build

def build(W, R25, R24):
    A = {}
    rng = stream("asks")
    tier_e, tot_e = household_tiers(W)
    r = R25
    role = r._role.to_numpy()
    ent = r._ent.to_numpy()
    agi = r.federal_agi.to_numpy()
    status = r.filing_status.to_numpy()
    n = len(r)
    tier = np.where(ent >= 0, tier_e[np.maximum(ent, 0)], 0)
    bset = set()
    for F in Wm.ANSWER_PINS:
        bset.update(W.boundary[F])
    boundary_ret = np.isin(ent, list(bset)) & (role != "N")
    special_hh = np.where(ent >= 0, W.special[2025][np.maximum(ent, 0)] != "", False)
    taken = set(r.filer_tin.tolist()) | set(r.spouse_tin[r.spouse_tin > 0].tolist())
    A["tier_ret"] = tier
    A["boundary_ret"] = boundary_ret

    # ---------------- Schedule D on each return (the version of record), then wages
    schd_p = interp_steps(np.maximum(agi, 0), CFG["schd_p"])
    is_kid = role == "D"
    kid_special = is_kid & special_hh
    schd_p = np.where(is_kid, np.where(kid_special, 0.92, 0.03), schd_p)
    has_schd = (rng.random(n) < schd_p) & ~boundary_ret
    gshare = interp_steps(np.maximum(agi, 0), CFG["gain_share"]) * rng.lognormal(0, 0.55, n)
    gshare = np.where(kid_special, rng.uniform(0.25, 0.55, n), gshare)
    gshare = np.clip(gshare, 0.0, 0.88)
    is_loss = has_schd & (rng.random(n) < interp_steps(np.maximum(agi, 0), CFG["loss_p"])) & ~kid_special
    net = np.where(has_schd, np.round(np.maximum(agi, 0) * gshare), 0).astype(np.int64)
    loss_amt = np.round(np.exp(rng.normal(np.log(np.maximum(agi, 20_000) * CFG["loss_scale"]), 1.05, n))).astype(np.int64)
    net = np.where(is_loss, -np.maximum(loss_amt, 600), net)
    in_agi = np.where(net < 0, np.maximum(net, -np.where(status == 3, 1_500, 3_000)), net)
    in_agi = np.where(has_schd, in_agi, 0).astype(np.int64)
    net = np.where(has_schd, net, 0).astype(np.int64)
    wshare = np.interp(np.maximum(agi, 0), [0, 30_000, 100_000, 300_000, 1_000_000, 5_000_000, 50_000_000],
                       [0.80, 0.86, 0.84, 0.70, 0.42, 0.20, 0.07]) * rng.uniform(0.72, 1.12, n)
    room = np.clip(1.0 - np.where(in_agi > 0, in_agi / np.maximum(agi, 1), 0) - 0.04, 0, 1)
    wshare = np.minimum(wshare, room)
    no_wage_p = np.interp(np.maximum(agi, 0), [0, 20_000, 60_000, 200_000, 1_000_000], [0.42, 0.24, 0.14, 0.10, 0.12])
    no_wage = rng.random(n) < no_wage_p
    wages = np.where(no_wage | (agi <= 0), 0, np.round(np.maximum(agi, 0) * wshare)).astype(np.int64)
    wages = np.where(is_kid, np.where(kid_special, 0, np.round(agi * rng.uniform(0.86, 1.0, n))), wages).astype(np.int64)
    wages = np.where(boundary_ret, 0, wages)
    A["ret_wages"], A["ret_net"], A["ret_in_agi"], A["ret_has_schd"] = wages, net, in_agi, has_schd

    A.update(_wage_statements(W, r, wages, status, taken))
    A.update(_estimated_payments(W, r, tier_e, tot_e, role, ent, agi, wages, boundary_ret, special_hh, taken, R24))
    A.update(_versions(r, has_schd, net, in_agi, status, agi))
    A.update(_register(A))
    A.update(_deposits(A))
    return A


# ------------------------------------------------------------------ wage statements

def _wage_statements(W, r, wages, status, taken):
    rng = stream("w2")
    n = len(r)
    rng_e = stream("employers")
    E = CFG["n_employers"]
    eins = make_eins(rng_e, E)
    size = rng_e.pareto(1.05, E) + 0.2
    order = np.argsort(size)
    chan = np.full(E, "E", dtype="<U1")
    po = rng_e.choice(order[: int(E * 0.55)], int(E * CFG["paper_only_share"]), replace=False)
    chan[po] = "P"
    mid = np.setdiff1d(order[int(E * 0.35): int(E * 0.97)], po)
    bo = rng_e.choice(mid, int(E * CFG["both_share"]), replace=False)
    chan[bo] = "B"
    p_emp = size / size.sum()
    spouse = r.spouse_tin.to_numpy()
    filer = r.filer_tin.to_numpy()
    sp_share = np.where(rng.random(n) < 0.32, 1.0, rng.uniform(0.5, 0.95, n))
    joint2 = (status == 2) & (spouse > 0) & (sp_share < 1.0) & (wages > 0)
    one = (wages > 0) & ~joint2
    a = np.round(wages * sp_share).astype(np.int64)
    et = np.concatenate([filer[one], filer[joint2], spouse[joint2]])
    ew = np.concatenate([wages[one], a[joint2], wages[joint2] - a[joint2]])
    er = np.concatenate([np.where(one)[0], np.where(joint2)[0], np.where(joint2)[0]])
    keep = ew > 0
    et, ew, er = et[keep], ew[keep], er[keep]
    nst = rng.choice([1, 2, 3], len(et), p=[0.76, 0.19, 0.05])
    st_tin = np.repeat(et, nst)
    st_ret = np.repeat(er, nst)
    parts = np.concatenate([rng.dirichlet(np.ones(k) * 2.5) for k in nst])
    st_wage = np.maximum(np.round(np.repeat(ew, nst) * parts).astype(np.int64), 1)
    nf_tins = W.spare_tins[: CFG["nonfiler_statements"]]
    nf_tins = nf_tins[~np.isin(nf_tins, np.fromiter(taken, np.int64))]
    taken.update(nf_tins.tolist())
    st_tin = np.concatenate([st_tin, nf_tins])
    st_wage = np.concatenate([st_wage, np.round(np.exp(rng.normal(math.log(4_200), 0.8, len(nf_tins)))).astype(np.int64)])
    st_ret = np.concatenate([st_ret, np.full(len(nf_tins), -1)])
    m = len(st_tin)
    rate = np.interp(st_wage, [0, 20_000, 60_000, 150_000, 500_000, 5_000_000], [0.011, 0.026, 0.036, 0.045, 0.051, 0.054])
    st_wh = np.round(st_wage * rate * rng.uniform(0.86, 1.12, m)).astype(np.int64)
    emp = rng.choice(E, m, p=p_emp)
    ch = chan[emp]
    paper = (ch == "P") | ((ch == "B") & (rng.random(m) < CFG["both_paper_p"]))
    mis = (rng.random(m) < CFG["mis_w2"]) & (st_ret >= 0)
    rep = st_tin.copy()
    rep[mis] = typo(st_tin[mis], stream("typo_w2"), taken)
    w2 = pd.DataFrame({"true_tin": st_tin, "reported_tin": rep, "wages": st_wage, "withheld": st_wh,
                       "ein": eins[emp], "paper": paper, "mis": mis, "ret": st_ret, "emp": emp})
    # e-file: submissions per employer, statement ids in submission order
    ef = w2[~w2.paper].copy()
    ef["sub_day"] = stream("w2_days").integers(0, 31, len(ef))
    ef = ef.sort_values(["sub_day", "ein", "true_tin"], kind="stable").reset_index(drop=True)
    sub_of = {}
    sid = []
    rs = stream("w2_sub")
    base = 26_400_000
    for e, d in zip(ef.ein.to_numpy(), ef.sub_day.to_numpy()):
        key = (int(e), int(d))
        if key not in sub_of:
            base += int(rs.integers(1, 9))
            sub_of[key] = base
        sid.append(sub_of[key])
    ef["submission_id"] = sid
    ef["received_date"] = (pd.Timestamp("2026-01-05") + pd.to_timedelta(ef.sub_day * 1, unit="D")).dt.date
    ef["statement_id"] = 410_000_000 + np.cumsum(stream("w2_sid").integers(1, 4, len(ef)))
    pp = w2[w2.paper].copy()
    rk = stream("w2_paper")
    pp = pp.sort_values(["ein", "true_tin"], kind="stable").reset_index(drop=True)
    batch = np.zeros(len(pp), np.int64)
    seq = np.zeros(len(pp), np.int64)
    bno, cnt = 512, 0
    for i in range(len(pp)):
        if cnt == 0 or cnt >= 250 or (i > 0 and rk.random() < 0.004):
            bno += int(rk.integers(1, 3))
            cnt = 0
        cnt += 1
        batch[i] = bno
        seq[i] = cnt
    pp["batch"] = batch
    pp["seq"] = seq
    keyed = pd.Timestamp("2026-02-02") + pd.to_timedelta((batch - batch.min()) // 6, unit="D")
    pp["keyed_date"] = keyed
    emp_tab = pd.DataFrame({"ein": eins, "chan": chan, "size": size})
    return {"w2": w2, "w2_efile": ef, "w2_paper": pp, "employers": emp_tab}


# ------------------------------------------------------------------ estimated payments

def _estimated_payments(W, r, tier_e, tot_e, role, ent, agi, wages, boundary_ret, special_hh, taken, R24):
    rng = stream("es")
    n = len(r)
    filer = r.filer_tin.to_numpy()
    hh_tot = np.where(ent >= 0, tot_e[np.maximum(ent, 0)], agi)
    p = interp_steps(np.maximum(hh_tot, 0), CFG["es_p"])
    p = np.where(role == "D", np.where(special_hh, 0.45, 0.004), p)
    p = np.where(role == "N", 0.035, p)
    payer = (rng.random(n) < p) & ~boundary_ret & (agi > 0)
    nonwage = np.maximum(agi - wages, 0)
    annual = 0.049 * nonwage * rng.uniform(0.55, 1.35, n) + np.where(wages > 0, 0.004 * wages, 0)
    q = np.round(annual / 4.0 / 10.0) * 10
    q = np.where(q >= 2_000, np.round(q / 100.0) * 100, q)
    q = np.maximum(q, 50).astype(np.int64)
    idx = np.where(payer)[0]
    r24 = R24[(R24.residency_code == 1) & (R24.processed_date <= np.datetime64("2025-05-29"))]
    r24 = r24.drop_duplicates("filer_tin").set_index("filer_tin")
    due = {k: pd.Timestamp(v) for k, v in DUE.items()}
    pay = []          # tin, tax_year, amount, local, channel, instalment_intended, misapplied
    credits = []      # TY2024 return_id, amount, tin, posted local
    for i in idx:
        tin = int(filer[i])
        qi = int(q[i])
        inst = [1, 2, 3, 4]
        if rng.random() < 0.06:
            inst.remove(int(rng.integers(1, 5)))
        amount = {k: qi for k in inst}
        if tin in r24.index and rng.random() < CFG["credit_p"]:
            rr = r24.loc[tin]
            c = int(round(qi * rng.uniform(*CFG["credit_scale"]) / 10.0) * 10)
            post = pd.Timestamp(rr.processed_date) + pd.Timedelta(hours=1, minutes=int(rng.integers(5, 50)), seconds=int(rng.integers(0, 60)))
            credits.append((int(rr.return_id), c, tin, post))
            left = c
            for k in (1, 2):
                if k in amount and left > 0:
                    take = min(left, amount[k])
                    amount[k] -= take
                    left -= take
        for k, a in amount.items():
            if a <= 0:
                continue
            d = due[k]
            u = rng.random()
            if u < CFG["due_day_p"]:
                day, ev = d, CFG["evening_due_p"]
            elif u < CFG["due_day_p"] + CFG["late_p"] and k < 4:
                day, ev = d + pd.Timedelta(days=int(rng.integers(1, 11))), CFG["evening_other_p"]
            else:
                day = d - pd.Timedelta(days=int(min(60, max(1, rng.gamma(1.4, 7.0)))))
                ev = CFG["evening_other_p"]
            chn = rng.choice(["EPAY_ACH_DEBIT", "CARD", "ACH_CREDIT"], p=[0.6, 0.2, 0.2])
            if chn == "ACH_CREDIT":
                while day.weekday() >= 5:
                    day = day - pd.Timedelta(days=1)
                secs = int(rng.integers(7 * 3600, 16 * 3600))
            elif rng.random() < ev:
                secs = int(rng.integers(19 * 3600, 24 * 3600 - 1))
            else:
                secs = int(rng.integers(6 * 3600, 19 * 3600))
            pay.append((tin, 2025, a, day + pd.Timedelta(seconds=secs), chn, k, False))
    pay = pd.DataFrame(pay, columns=["tin", "tax_year", "amount", "local", "channel", "inst_intended", "misapplied"])
    pay["inst"] = instalment_of_local(pay.local)
    # payments keyed to tax year 2024 by mistake, moved to 2025 by transfer; an April payment's
    # transfer posts in May or June, every other one inside its own instalment window
    rm = stream("misapplied")
    lead = (pay.local.dt.normalize() <= pay.inst.map(lambda k: due[k]) - pd.Timedelta(days=12)).to_numpy()
    cand = np.where(lead & (pay.channel != "ACH_CREDIT").to_numpy())[0]
    mis_i = cand[rm.random(len(cand)) < CFG["misapplied_p"] * len(pay) / max(len(cand), 1)]
    pay.loc[mis_i, "misapplied"] = True
    pay.loc[mis_i, "tax_year"] = 2024
    xfer_post = []
    for i in mis_i:
        k = int(pay.inst[i])
        loc = pay.local[i]
        if k == 1:
            post = pd.Timestamp("2025-05-05") + pd.Timedelta(days=int(rm.integers(0, 38)))
        else:
            hi = due[k] - pd.Timedelta(days=2)
            lo = loc.normalize() + pd.Timedelta(days=3)
            span = max(1, (hi - lo).days)
            post = lo + pd.Timedelta(days=int(rm.integers(0, span)))
        post = post + pd.Timedelta(hours=1, minutes=int(rm.integers(5, 50)), seconds=int(rm.integers(0, 60)))
        xfer_post.append((int(i), post))
    # TY2024 fourth-instalment payments received in January 2025 (another tax year in the file)
    r2 = stream("es_ty2024")
    old = []
    for i in idx[r2.random(len(idx)) < 0.86]:
        day = pd.Timestamp("2025-01-15") - pd.Timedelta(days=int(min(25, r2.gamma(1.3, 4.0))))
        if r2.random() < 0.05:
            day = day + pd.Timedelta(days=int(r2.integers(18, 40)))
        old.append((int(filer[i]), 2024, int(q[i] * r2.uniform(0.8, 1.15) // 10 * 10),
                    day + pd.Timedelta(seconds=int(r2.integers(6 * 3600, 23 * 3600))),
                    r2.choice(["EPAY_ACH_DEBIT", "CARD", "ACH_CREDIT"], p=[0.6, 0.2, 0.2])))
    # returned items: ACH debits and card payments of TY2025; NSF items may be re-presented
    rd = stream("returned")
    elig = np.where((pay.channel != "ACH_CREDIT").to_numpy() & ~pay.misapplied.to_numpy())[0]
    ret_i = elig[rd.random(len(elig)) < CFG["dishonour_p"]]
    ret = []
    for i in ret_i:
        loc = pay.local[i]
        code = rd.choice(["R01", "R02", "R03", "R08", "R16", "R29"], p=[0.62, 0.12, 0.08, 0.07, 0.04, 0.07])
        if pay.channel[i] == "CARD":
            code = "CB"
        rdate = business_days_after(loc, int(rd.integers(2, 5)))
        k = int(pay.inst[i])
        early = k == 4 or loc.normalize() <= due[k] - pd.Timedelta(days=12)
        rep_date, rep_res = None, None
        if code == "R01" and early and rd.random() < CFG["represent_p"] / 0.62:
            rep_date = business_days_after(rdate, int(rd.integers(1, 3)))
            assert k == 4 or rep_date <= due[k]
            rep_res = "PAID" if rd.random() < 0.86 else "RETURNED"
        ret.append((int(i), code, rdate, rep_date, rep_res))
    # ES misreports (TIN keyed wrong on the voucher or the card form)
    rt = stream("typo_es")
    mis = (rt.random(len(pay)) < CFG["mis_es"]) & ~pay.misapplied.to_numpy()
    pay["reported_tin"] = pay.tin.to_numpy()
    pay.loc[mis, "reported_tin"] = typo(pay.tin.to_numpy()[mis], rt, taken)
    pay["mis"] = mis
    return {"es_pay": pay, "es_credits": credits, "es_xfer": xfer_post, "es_old": old, "es_returned": ret}


# ------------------------------------------------------------------ versions

def _versions(r, has_schd, net, in_agi, status, agi):
    """Every version of an amended return. The returns file carries the version of record (latest
    accepted); the Schedule D extract carries the latest version received."""
    rng = stream("versions")
    n = len(r)
    big = has_schd & (net > CFG["big_gain"])
    p = np.where(big, CFG["amend_big_p"], np.where(has_schd, CFG["amend_p"], 0.011))
    amended = (rng.random(n) < p) & (agi > 0)
    pdate = pd.to_datetime(r.processed_date.to_numpy())
    rid = r.return_id.to_numpy()
    cap = np.where(status == 3, 1_500, 3_000)
    vers = []        # return_id, seq, received, disposition, disp_date, agi, net, in_agi, has_schd
    latest = {}      # return index -> (seq, received, net, in_agi)
    for i in np.where(amended)[0]:
        rec_net, rec_in, rec_agi = int(net[i]), int(in_agi[i]), int(agi[i])
        sch = bool(has_schd[i])
        u = rng.random()
        unacc = u < CFG["unacc_share"]
        acc_then = unacc and rng.random() < CFG["accepted_then_unacc"]
        seqs = []
        t0 = pdate[i] - pd.Timedelta(days=int(rng.integers(6, 30)))
        if not unacc or acc_then:
            # an accepted amendment is the version of record; the original differs from it
            if sch and rec_net > 0:
                up = rng.uniform(*CFG["acc_up"])
                o_net = int(round(rec_net / (1 + up)))
            elif sch:
                o_net = int(round(rec_net * rng.uniform(0.55, 0.95)))
            else:
                o_net = 0
            o_in = (max(o_net, -int(cap[i])) if o_net < 0 else o_net) if sch else 0
            d_other = 0 if sch else int(rng.integers(-9_000, 9_000))
            o_agi = rec_agi - (rec_in - o_in) - d_other
            a1 = pdate[i] + pd.Timedelta(days=int(rng.integers(25, 200)))
            a1 = min(a1, pd.Timestamp("2026-09-30"))
            seqs.append((0, t0, "ACCEPTED", pdate[i], o_agi, o_net, o_in))
            seqs.append((1, a1, "ACCEPTED", a1 + pd.Timedelta(days=int(rng.integers(12, 60))), rec_agi, rec_net, rec_in))
        else:
            seqs.append((0, t0, "ACCEPTED", pdate[i], rec_agi, rec_net, rec_in))
        if unacc:
            if sch and rec_net > 0:
                c_net = int(round(rec_net * (1 - rng.uniform(*CFG["unacc_cut"]))))
            elif sch:
                c_net = int(round(rec_net * rng.uniform(1.4, 3.0)))
            else:
                c_net = 0
            c_in = (max(c_net, -int(cap[i])) if c_net < 0 else c_net) if sch else 0
            d_other = 0 if sch else int(rng.integers(-12_000, 2_000))
            c_agi = rec_agi - (rec_in - c_in) + d_other
            last = seqs[-1][1]
            recv = max(last, pdate[i]) + pd.Timedelta(days=int(rng.integers(20, 160)))
            if recv > pd.Timestamp("2026-10-19"):
                recv = pd.Timestamp("2026-10-19") - pd.Timedelta(days=int(rng.integers(0, 30)))
            pending = recv > pd.Timestamp("2026-08-20") or rng.random() < 0.3
            if pending:
                disp, ddate = "PENDING", None
                if recv <= last:
                    recv = last + pd.Timedelta(days=5)
            else:
                disp, ddate = "REJECTED", recv + pd.Timedelta(days=int(rng.integers(14, 70)))
                if ddate > EXTRACT - pd.Timedelta(days=1):
                    ddate = EXTRACT - pd.Timedelta(days=2)
            seqs.append((len(seqs), recv, disp, ddate, c_agi, c_net, c_in))
        for s in seqs:
            vers.append((int(rid[i]), s[0], s[1], s[2], s[3], s[4], s[5], s[6], sch))
        latest[int(i)] = seqs[-1]
    log = pd.DataFrame(vers, columns=["return_id", "amendment_seq", "received_date", "disposition", "disposition_date",
                                      "federal_agi", "net_gain_loss", "amount_in_agi", "has_schd"])
    # the Schedule D extract: every return with a schedule, its latest version received
    sidx = np.where(has_schd)[0]
    seq = np.zeros(len(sidx), np.int64)
    rcv = (pdate[sidx] - pd.to_timedelta(stream("schd_rcv").integers(6, 30, len(sidx)), unit="D")).to_numpy().copy()
    xn = net[sidx].copy()
    xi = in_agi[sidx].copy()
    for j, i in enumerate(sidx):
        s = latest.get(int(i))
        if s is not None:
            seq[j], rcv[j], xn[j], xi[j] = s[0], np.datetime64(s[1]), s[5], s[6]
    ext = pd.DataFrame({"return_id": rid[sidx], "amendment_seq": seq, "received_date": rcv,
                        "net_gain_loss": xn, "amount_in_agi": xi})
    return {"versions": log, "schd_extract": ext, "amended": amended}


def _register(A):
    """TIN-resolution register: every reported TIN that matched no filer, from wage statements
    and payments; resolved rows carry the filer's TIN."""
    rng = stream("register")
    w2 = A["w2"]
    pay = A["es_pay"]
    rows = []
    for rep, true in zip(w2.reported_tin[w2.mis].to_numpy(), w2.true_tin[w2.mis].to_numpy()):
        rows.append((int(rep), int(true), "W2"))
    for rep, true in zip(pay.reported_tin[pay.mis].to_numpy(), pay.tin[pay.mis].to_numpy()):
        rows.append((int(rep), int(true), "ES"))
    reg = pd.DataFrame(rows, columns=["reported_tin", "true_tin", "source"]).drop_duplicates("reported_tin")
    resolved = rng.random(len(reg)) < CFG["resolve_p"]
    reg["status"] = np.where(resolved, "RESOLVED", "OPEN")
    reg["resolved_tin"] = np.where(resolved, reg.true_tin, 0)
    opened = np.where(reg.source == "W2", pd.Timestamp("2026-03-02").value, pd.Timestamp("2025-05-12").value)
    opened = pd.to_datetime(opened) + pd.to_timedelta(rng.integers(0, 150, len(reg)), unit="D")
    reg["opened_date"] = opened
    reg["closed_date"] = np.where(resolved, opened + pd.to_timedelta(rng.integers(8, 120, len(reg)), unit="D"), pd.NaT)
    reg["closed_date"] = pd.to_datetime(reg["closed_date"])
    late = reg.closed_date > pd.Timestamp("2026-10-20")
    reg.loc[late, "closed_date"] = pd.Timestamp("2026-10-20") - pd.to_timedelta(rng.integers(0, 20, int(late.sum())), unit="D")
    return {"register": reg.reset_index(drop=True)}


def _deposits(A):
    """Employer withholding deposits received in calendar 2025: monthly, semi-weekly and quarterly
    depositors; each deposit dated by receipt and by the payroll period it covers."""
    rng = stream("deposits")
    emp = A["employers"]
    w2 = A["w2"]
    annual = w2.groupby("ein").withheld.sum()
    rows = []
    dep_id = 7_310_000
    for ein, tot in annual.items():
        tot = int(tot)
        if tot >= 900_000:
            sched = "SEMIWEEKLY"
            periods = pd.date_range("2024-12-27", "2025-12-26", freq="7D")
        elif tot >= 18_000:
            sched = "MONTHLY"
            periods = pd.date_range("2024-12-31", "2025-11-30", freq="ME")
        else:
            sched = "QUARTERLY"
            periods = pd.to_datetime(["2024-12-31", "2025-03-31", "2025-06-30", "2025-09-30"])
        k = len(periods)
        w = rng.uniform(0.86, 1.14, k)
        amt = np.round(tot / (k if sched != "SEMIWEEKLY" else 52.0) * w).astype(np.int64)
        for pe, a in zip(periods, amt):
            if sched == "SEMIWEEKLY":
                rec = pe + pd.Timedelta(days=int(rng.integers(2, 5)))
            elif sched == "MONTHLY":
                rec = pe + pd.Timedelta(days=int(rng.integers(8, 16)))
            else:
                rec = pe + pd.Timedelta(days=int(rng.integers(20, 31)))
            if rec.year != 2025:
                continue
            dep_id += int(rng.integers(1, 6))
            rows.append((dep_id, int(ein), sched, pe.date(), rec.date(), int(a)))
    dep = pd.DataFrame(rows, columns=["deposit_id", "employer_ein", "deposit_schedule", "period_end", "received_date", "amount"])
    return {"deposits": dep.sort_values(["received_date", "deposit_id"], kind="stable").reset_index(drop=True)}
