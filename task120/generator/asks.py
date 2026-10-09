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
    n_employers=9_400, paper_only_share=0.15, both_share=0.085, both_paper_p=0.34,
    w2_mis_resolved=0.0155, w2_mis_open=0.0030, resolve_p=0.83, nonfiler_statements=13_850,
    # estimated payments
    es_p=[(0, 0.012), (50_000, 0.02), (100_000, 0.05), (200_000, 0.25), (260_000, 0.33), (300_000, 0.47), (742_000, 0.62), (3_000_000, 0.72)],
    due_day_p=0.24, evening_due_p=0.27, evening_other_p=0.11, late_p=0.04,
    credit_scale=(0.6, 1.7), credit_early=0.136, credit_late=0.021,
    cell_misapplied=0.021, cell_notpaid=0.031, cell_repaid=0.0105, cell_mis_resolved=0.0152, cell_mis_open=0.0028,
    # capital gains (tier targets are shares of the tier's golden gain)
    schd_p=[(0, 0.07), (50_000, 0.13), (100_000, 0.22), (214_000, 0.52), (742_000, 0.86), (5_000_000, 0.93)],
    gain_share=[(0, 0.04), (100_000, 0.05), (214_000, 0.075), (318_000, 0.13), (742_000, 0.30), (5_000_000, 0.42)],
    # tier 2 tilted so its share of AGI sits off the round one-decimal value (determinism-check A.6)
    gain_tilt={0: 1.0, 1: 1.0, 2: 1.0023, 3: 1.0},
    loss_p=[(0, 0.24), (214_000, 0.15), (742_000, 0.11)],
    h3_target={0: 0.030, 1: 0.026, 2: 0.029, 3: 0.044},
    d2_target={0: 0.050, 1: 0.056, 2: 0.058, 3: 0.063},
    acc_target={0: 0.030, 1: 0.032, 2: 0.032, 3: 0.034},
    acc_up=(0.22, 0.65), unacc_cut=(0.40, 0.95), amend_other=0.011,
)

EXTRACT = pd.Timestamp("2026-10-22")
OPEN_SEASON = pd.Timestamp("2026-01-21")       # TY2025 e-filing opened


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

def _take_until(keys, amounts, target):
    """Indices, in key order, whose amounts first reach target (stratified device selection)."""
    order = np.argsort(keys, kind="stable")
    cum = np.cumsum(amounts[order])
    k = int(np.searchsorted(cum, target)) + 1
    return order[:min(k, len(order))]


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
    tier = np.where(ent >= 0, tier_e[np.maximum(ent, 0)], 0).astype(np.int8)
    bset = set()
    for F in Wm.ANSWER_PINS:
        bset.update(W.boundary[F])
    boundary_ret = np.isin(ent, list(bset)) & (role != "N")
    special_hh = np.where(ent >= 0, W.special[2025][np.maximum(ent, 0)] != "", False)
    taken = set(r.filer_tin.tolist()) | set(r.spouse_tin[r.spouse_tin > 0].tolist())
    # a misreported TIN never lands on anyone in the files: every filer, spouse and listed dependent
    # of any year (a nonfiling dependent included), so no reported number joins a schedule by accident
    every = [W.tin_p, W.tin_s[W.tin_s > 0], W.dep_tin, W.nonres_dep_pool]
    for yy in sorted(W.nonres):
        every += [W.nonres[yy]["tin"], W.nonres[yy]["spouse"][W.nonres[yy]["spouse"] > 0]]
    taken.update(np.concatenate(every).astype(np.int64).tolist())
    A["tier_ret"] = tier
    A["boundary_ret"] = boundary_ret

    # ---------------- Schedule D on each return (the version of record), then wages
    schd_p = interp_steps(np.maximum(agi, 0), CFG["schd_p"])
    is_kid = role == "D"
    kid_special = is_kid & special_hh
    schd_p = np.where(is_kid, np.where(kid_special, 0.92, 0.03), schd_p)
    has_schd = (rng.random(n) < schd_p) & ~boundary_ret
    tilt = np.array([CFG["gain_tilt"][int(t)] for t in range(4)])[tier]
    gshare = interp_steps(np.maximum(agi, 0), CFG["gain_share"]) * rng.lognormal(0, 0.55, n) * tilt
    gshare = np.where(kid_special, rng.uniform(0.25, 0.55, n), gshare)
    gshare = np.clip(gshare, 0.0, 0.88)
    is_loss = has_schd & (rng.random(n) < interp_steps(np.maximum(agi, 0), CFG["loss_p"])) & ~kid_special
    gain = np.where(has_schd & ~is_loss, np.round(np.maximum(agi, 0) * gshare), 0).astype(np.int64)
    cap = np.where(status == 3, 1_500, 3_000)
    base_loss = np.exp(rng.normal(0.0, 0.9, n)) * np.maximum(agi, 25_000) * 0.03
    net = gain.copy()
    in_agi = gain.copy()
    floor_loss = rng.integers(140, 2_400, n)
    loss_in_agi = -np.minimum(cap, np.maximum(floor_loss, np.round(base_loss * 0.2)).astype(np.int64))
    # the loss limit: each tier's excess of net loss over the amount entering AGI is a set share of
    # that tier's gain (H3); a multiplier on the loss sizes per tier
    for t in (0, 1, 2, 3):
        sel = is_loss & (tier == t)
        G = gain[tier == t].sum() + loss_in_agi[sel].sum()
        tgt = CFG["h3_target"][t] * G

        def excess(mult):
            lo = np.maximum(floor_loss[sel], np.round(base_loss[sel] * mult)).astype(np.int64)
            return float((lo - np.minimum(cap[sel], lo)).sum())
        a, b = 0.01, 400.0
        for _ in range(80):
            mid = math.sqrt(a * b)
            if excess(mid) < tgt:
                a = mid
            else:
                b = mid
        lo = np.maximum(floor_loss[sel], np.round(base_loss[sel] * b)).astype(np.int64)
        net[sel] = -lo
        in_agi[sel] = -np.minimum(cap[sel], lo)
    net = np.where(has_schd, net, 0).astype(np.int64)
    in_agi = np.where(has_schd, in_agi, 0).astype(np.int64)
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

    A.update(_wage_statements(W, r, wages, status, taken, tier))
    A.update(_estimated_payments(W, r, tier_e, tot_e, tier, role, ent, agi, wages, boundary_ret, special_hh, taken, R24))
    A.update(_versions(r, tier, has_schd, net, in_agi, status, agi))
    A.update(_register(A))
    A.update(_deposits(A))
    return A


# ------------------------------------------------------------------ wage statements

def _wage_statements(W, r, wages, status, taken, tier):
    rng = stream("w2")
    n = len(r)
    rng_e = stream("employers")
    E = CFG["n_employers"]
    eins = make_eins(rng_e, E)
    size = rng_e.pareto(1.05, E) + 0.2
    order = np.argsort(size)
    chan = np.full(E, "E", dtype="<U1")
    # small and mid-sized employers file on paper through the capture vendor; some mid-sized
    # employers file most statements on the platform and a share on paper
    po = rng_e.choice(order[int(E * 0.25): int(E * 0.92)], int(E * CFG["paper_only_share"]), replace=False)
    chan[po] = "P"
    mid = np.setdiff1d(order[int(E * 0.50): int(E * 0.99)], po)
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
    # H4: a set share of each tier's withholding sits on statements whose TIN was keyed wrong
    st_tier = np.where(st_ret >= 0, tier[np.maximum(st_ret, 0)], 0)
    mis = np.zeros(m, bool)
    openc = np.zeros(m, bool)
    keys = stream("w2_mis_keys").random(m)
    for t in (0, 1, 2, 3):
        idx = np.where((st_tier == t) & (st_ret >= 0))[0]
        tot = st_wh[idx].sum()
        pick_r = idx[_take_until(keys[idx], st_wh[idx], CFG["w2_mis_resolved"] * tot)]
        rest = np.setdiff1d(idx, pick_r)
        pick_o = rest[_take_until(keys[rest] * 7.31 % 1, st_wh[rest], CFG["w2_mis_open"] * tot)]
        mis[pick_r] = True
        mis[pick_o] = True
        openc[pick_o] = True
    rep = st_tin.copy()
    rep[mis] = typo(st_tin[mis], stream("typo_w2"), taken)
    w2 = pd.DataFrame({"true_tin": st_tin, "reported_tin": rep, "wages": st_wage, "withheld": st_wh,
                       "ein": eins[emp], "paper": paper, "mis": mis, "open": openc, "ret": st_ret, "emp": emp, "tier": st_tier})
    ef = w2[~w2.paper].copy()
    ef["sub_day"] = stream("w2_days").integers(0, 31, len(ef))
    ef = ef.sort_values(["sub_day", "ein", "true_tin"], kind="stable").reset_index(drop=True)
    key = ef.ein.to_numpy() * 100 + ef.sub_day.to_numpy()
    uniq, first = np.unique(key, return_index=True)
    order_first = np.argsort(first)
    sub_ids = np.empty(len(uniq), np.int64)
    sub_ids[order_first] = 26_400_000 + np.cumsum(stream("w2_sub").integers(1, 9, len(uniq)))
    ef["submission_id"] = sub_ids[np.searchsorted(uniq, key)]
    ef["received_date"] = (pd.Timestamp("2026-01-05") + pd.to_timedelta(ef.sub_day, unit="D")).dt.date
    ef["statement_id"] = 410_000_000 + np.cumsum(stream("w2_sid").integers(1, 4, len(ef)))
    pp = w2[w2.paper].copy()
    rk = stream("w2_paper")
    pp = pp.sort_values(["ein", "true_tin"], kind="stable").reset_index(drop=True)
    batch = np.zeros(len(pp), np.int64)
    seq = np.zeros(len(pp), np.int64)
    bno, cnt = 512, 0
    for i in range(len(pp)):
        if cnt == 0 or cnt >= 250 or rk.random() < 0.004:
            bno += int(rk.integers(1, 3))
            cnt = 0
        cnt += 1
        batch[i] = bno
        seq[i] = cnt
    pp["batch"] = batch
    pp["seq"] = seq
    pp["keyed_date"] = pd.Timestamp("2026-02-02") + pd.to_timedelta((batch - batch.min()) // 6, unit="D")
    emp_tab = pd.DataFrame({"ein": eins, "chan": chan, "size": size})
    return {"w2": w2, "w2_efile": ef, "w2_paper": pp, "employers": emp_tab}


# ------------------------------------------------------------------ estimated payments

def _estimated_payments(W, r, tier_e, tot_e, tier, role, ent, agi, wages, boundary_ret, special_hh, taken, R24):
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
    pay = []
    credits = []
    for i in idx:
        tin = int(filer[i])
        qi = int(q[i])
        inst = [1, 2, 3, 4]
        if rng.random() < 0.06:
            inst.remove(int(rng.integers(1, 5)))
        amount = {k: qi for k in inst}
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
            pay.append((tin, 2025, a, day + pd.Timedelta(seconds=secs), chn, int(tier[i])))
    pay = pd.DataFrame(pay, columns=["tin", "tax_year", "amount", "local", "channel", "tier"])
    pay["inst"] = instalment_of_local(pay.local)
    # overpayments credited from TY2024 returns: per tier, those posted by the April due date come
    # to a set share of April's receipts and those posted later to a set share of June's
    rc = stream("credits")
    cand = [(int(i), int(filer[i]), int(tier[i])) for i in idx if int(filer[i]) in r24.index]
    ckeys = rc.random(len(cand))
    for t in (0, 1, 2, 3):
        cell1 = pay.amount[(pay.tier == t) & (pay.inst == 1)].sum()
        cell2 = pay.amount[(pay.tier == t) & (pay.inst == 2)].sum()
        early, late = [], []
        for (i, tin, tt_), kk in zip(cand, ckeys):
            if tt_ != t:
                continue
            rr = r24.loc[tin]
            pdt = pd.Timestamp(rr.processed_date)
            c = int(round(q[i] * (0.6 + 1.1 * kk) / 10.0) * 10)
            post = pdt + pd.Timedelta(hours=1, minutes=int(5 + 44 * ((kk * 13.7) % 1)), seconds=int(60 * ((kk * 31.3) % 1)))
            (early if pdt <= pd.Timestamp("2025-04-15") else late).append((kk, int(rr.return_id), c, tin, post))
        for lst, tgt in ((early, CFG["credit_early"] * cell1), (late, CFG["credit_late"] * cell2)):
            lst.sort()
            acc = 0
            for kk, rid, c, tin, post in lst:
                if acc >= tgt:
                    break
                credits.append((rid, c, tin, post))
                acc += c
    pay["misapplied"] = False
    pay["ret_code"] = ""
    pay["mis"] = False
    pay["open"] = False
    lead = (pay.local.dt.normalize() <= pay.inst.map(lambda k: due[k]) - pd.Timedelta(days=12)).to_numpy() | (pay.inst == 4).to_numpy()
    keys = stream("es_keys").random(len(pay))
    amt = pay.amount.to_numpy().astype(float)
    chn = pay.channel.to_numpy()
    used = np.zeros(len(pay), bool)
    rep_pick = {}
    for t in (0, 1, 2, 3):
        for k in (1, 2, 3, 4):
            cell = np.where((pay.tier == t).to_numpy() & (pay.inst == k).to_numpy())[0]
            tot = amt[cell].sum()
            # payments keyed to tax year 2024 by mistake, moved back by transfer
            c = cell[lead[cell] & (chn[cell] != "ACH_CREDIT") & ~used[cell]]
            s = c[_take_until(keys[c], amt[c], CFG["cell_misapplied"] * tot)]
            pay.loc[s, "misapplied"] = True
            pay.loc[s, "tax_year"] = 2024
            used[s] = True
            # returned items: early NSF items re-presented and paid; the rest not paid
            c = cell[lead[cell] & (chn[cell] == "EPAY_ACH_DEBIT") & ~used[cell]]
            s = c[_take_until((keys[c] * 3.7) % 1, amt[c], CFG["cell_repaid"] * tot)]
            pay.loc[s, "ret_code"] = "R01"
            for i in s:
                rep_pick[int(i)] = "PAID"
            used[s] = True
            c = cell[(chn[cell] != "ACH_CREDIT") & ~used[cell]]
            s = c[_take_until((keys[c] * 5.3) % 1, amt[c], CFG["cell_notpaid"] * tot)]
            used[s] = True
            rr = stream(f"ret_codes{t}{k}")
            for i in s:
                if chn[i] == "CARD":
                    code = "CB"
                else:
                    code = rr.choice(["R01", "R02", "R03", "R08", "R16", "R29"], p=[0.5, 0.17, 0.11, 0.09, 0.05, 0.08])
                pay.loc[i, "ret_code"] = code
                if code == "R01" and lead[i] and rr.random() < 0.3:
                    rep_pick[int(i)] = "RETURNED"
            # TINs keyed wrong on the voucher or card form: resolved, and open cases
            c = cell[~used[cell]]
            s = c[_take_until((keys[c] * 7.9) % 1, amt[c], CFG["cell_mis_resolved"] * tot)]
            pay.loc[s, "mis"] = True
            used[s] = True
            c = cell[~used[cell]]
            s = c[_take_until((keys[c] * 9.1) % 1, amt[c], CFG["cell_mis_open"] * tot)]
            pay.loc[s, "mis"] = True
            pay.loc[s, "open"] = True
            used[s] = True
    # transfer postings: an April payment's transfer posts in May or June; every other one inside
    # its own instalment window
    rm = stream("misapplied")
    xfer_post = []
    for i in np.where(pay.misapplied.to_numpy())[0]:
        k = int(pay.inst[i])
        loc = pay.local[i]
        if k == 1:
            post = pd.Timestamp("2025-05-05") + pd.Timedelta(days=int(rm.integers(0, 38)))
        elif k == 4:
            post = loc.normalize() + pd.Timedelta(days=int(rm.integers(4, 40)))
            post = min(post, pd.Timestamp("2026-01-28"))
        else:
            lo = loc.normalize() + pd.Timedelta(days=3)
            hi = due[k] - pd.Timedelta(days=2)
            post = lo + pd.Timedelta(days=int(rm.integers(0, max(1, (hi - lo).days))))
        post = post + pd.Timedelta(hours=1, minutes=int(rm.integers(5, 50)), seconds=int(rm.integers(0, 60)))
        xfer_post.append((int(i), post))
    rd = stream("returned")
    ret = []
    for i in np.where(pay.ret_code.to_numpy() != "")[0]:
        loc = pay.local[i]
        k = int(pay.inst[i])
        rdate = business_days_after(loc, int(rd.integers(2, 5)))
        rep_date, rep_res = None, rep_pick.get(int(i))
        if rep_res:
            rep_date = business_days_after(rdate, int(rd.integers(1, 3)))
            assert k == 4 or rep_date <= due[k], (k, loc, rep_date)
        ret.append((int(i), pay.ret_code[i], rdate, rep_date, rep_res))
    # TY2024 fourth-instalment payments received in January 2025 (another tax year in the file)
    r2 = stream("es_ty2024")
    old = []
    for i in idx[r2.random(len(idx)) < 0.86]:
        day = pd.Timestamp("2025-01-15") - pd.Timedelta(days=int(min(14, r2.gamma(1.3, 4.0))))
        if r2.random() < 0.05:
            day = day + pd.Timedelta(days=int(r2.integers(18, 40)))
        old.append((int(filer[i]), 2024, int(q[i] * r2.uniform(0.8, 1.15) // 10 * 10),
                    day + pd.Timedelta(seconds=int(r2.integers(6 * 3600, 23 * 3600))),
                    r2.choice(["EPAY_ACH_DEBIT", "CARD", "ACH_CREDIT"], p=[0.6, 0.2, 0.2])))
    mis = pay.mis.to_numpy()
    pay["reported_tin"] = pay.tin.to_numpy()
    pay.loc[mis, "reported_tin"] = typo(pay.tin.to_numpy()[mis], stream("typo_es"), taken)
    return {"es_pay": pay, "es_credits": credits, "es_xfer": xfer_post, "es_old": old, "es_returned": ret}


# ------------------------------------------------------------------ versions

def _versions(r, tier, has_schd, net, in_agi, status, agi):
    """Every version of an amended return. The returns file carries the version of record (latest
    accepted); the Schedule D extract carries the latest version received. Per tier, unaccepted
    latest versions cut a set share of the tier's gain (D2) and accepted amendments raised it by a
    set share over the originals."""
    rng = stream("versions")
    n = len(r)
    pdate = pd.to_datetime(r.processed_date.to_numpy())
    rid = r.return_id.to_numpy()
    cap = np.where(status == 3, 1_500, 3_000)
    keys = stream("version_keys").random(n)
    cut = rng.uniform(*CFG["unacc_cut"], n)
    up = rng.uniform(*CFG["acc_up"], n)
    unacc = np.zeros(n, bool)
    acc = np.zeros(n, bool)
    for t in (0, 1, 2, 3):
        gsel = has_schd & (tier == t) & (net > 0)
        G = float(in_agi[(tier == t) & has_schd].sum())
        c = np.where(gsel)[0]
        drop = np.round(net[c] * cut[c])
        s = c[_take_until(keys[c], drop.astype(float), CFG["d2_target"][t] * G)]
        unacc[s] = True
        rise = np.round(net[c] - net[c] / (1 + up[c]))
        s2 = c[_take_until((keys[c] * 4.7) % 1, rise.astype(float), CFG["acc_target"][t] * G)]
        acc[s2] = True
    # amendments to returns without a schedule (other items): texture
    other = (~has_schd) & (agi > 0) & (rng.random(n) < CFG["amend_other"])
    vers = []
    latest = {}
    for i in np.where(unacc | acc | other)[0]:
        rec_net, rec_in, rec_agi = int(net[i]), int(in_agi[i]), int(agi[i])
        sch = bool(has_schd[i])
        t0 = max(pdate[i] - pd.Timedelta(days=int(rng.integers(6, 30))), OPEN_SEASON)
        seqs = []
        if acc[i] or (other[i] and rng.random() < 0.55):
            o_net = int(round(rec_net / (1 + up[i]))) if sch else 0
            o_in = (max(o_net, -int(cap[i])) if o_net < 0 else o_net) if sch else 0
            d_other = 0 if sch else int(rng.integers(-9_000, 9_000))
            o_agi = rec_agi - (rec_in - o_in) - d_other
            a1 = min(pdate[i] + pd.Timedelta(days=int(rng.integers(25, 200))), pd.Timestamp("2026-08-15"))
            seqs.append((0, t0, "ACCEPTED", pdate[i], o_agi, o_net, o_in))
            seqs.append((1, a1, "ACCEPTED", a1 + pd.Timedelta(days=int(rng.integers(12, 60))), rec_agi, rec_net, rec_in))
        else:
            seqs.append((0, t0, "ACCEPTED", pdate[i], rec_agi, rec_net, rec_in))
        if unacc[i] or (other[i] and len(seqs) == 1):
            c_net = int(round(rec_net * (1 - cut[i]))) if sch else 0
            c_in = (max(c_net, -int(cap[i])) if c_net < 0 else c_net) if sch else 0
            d_other = 0 if sch else int(rng.integers(-12_000, 2_000))
            c_agi = rec_agi - (rec_in - c_in) + d_other
            last = seqs[-1][1]
            recv = max(last, pdate[i]) + pd.Timedelta(days=int(rng.integers(20, 160)))
            if recv > pd.Timestamp("2026-10-19"):
                recv = pd.Timestamp("2026-10-19") - pd.Timedelta(days=int(rng.integers(0, 30)))
            if recv <= last:
                recv = last + pd.Timedelta(days=5)
            pending = recv > pd.Timestamp("2026-08-20") or rng.random() < 0.3
            if pending:
                disp, ddate = "PENDING", None
            else:
                disp, ddate = "REJECTED", min(recv + pd.Timedelta(days=int(rng.integers(14, 70))), EXTRACT - pd.Timedelta(days=2))
            seqs.append((len(seqs), recv, disp, ddate, c_agi, c_net, c_in))
        for s in seqs:
            vers.append((int(rid[i]), s[0], s[1], s[2], s[3], s[4], s[5], s[6], sch))
        latest[int(i)] = seqs[-1]
    log = pd.DataFrame(vers, columns=["return_id", "amendment_seq", "received_date", "disposition", "disposition_date",
                                      "federal_agi", "net_gain_loss", "amount_in_agi", "has_schd"])
    sidx = np.where(has_schd)[0]
    seq = np.zeros(len(sidx), np.int64)
    rcv = (pdate[sidx] - pd.to_timedelta(stream("schd_rcv").integers(6, 30, len(sidx)), unit="D")).to_numpy().copy()
    rcv = np.maximum(rcv, np.datetime64(OPEN_SEASON))
    xn = net[sidx].copy()
    xi = in_agi[sidx].copy()
    for j, i in enumerate(sidx):
        s = latest.get(int(i))
        if s is not None:
            seq[j], rcv[j], xn[j], xi[j] = s[0], np.datetime64(s[1]), s[5], s[6]
    ext = pd.DataFrame({"return_id": rid[sidx], "amendment_seq": seq, "received_date": rcv,
                        "net_gain_loss": xn, "amount_in_agi": xi})
    return {"versions": log, "schd_extract": ext, "amended": unacc | acc | other}


def _register(A):
    """TIN-resolution register: every reported TIN that matched no filer, from wage statements
    and payments; resolved rows carry the filer's TIN."""
    rng = stream("register")
    w2 = A["w2"]
    pay = A["es_pay"]
    rows = []
    for rep, true, op in zip(w2.reported_tin[w2.mis].to_numpy(), w2.true_tin[w2.mis].to_numpy(), w2.open[w2.mis].to_numpy()):
        rows.append((int(rep), int(true), "W2", bool(op)))
    for rep, true, op in zip(pay.reported_tin[pay.mis].to_numpy(), pay.tin[pay.mis].to_numpy(), pay.open[pay.mis].to_numpy()):
        rows.append((int(rep), int(true), "ES", bool(op)))
    reg = pd.DataFrame(rows, columns=["reported_tin", "true_tin", "source", "open"]).drop_duplicates("reported_tin")
    resolved = ~reg.open.to_numpy()
    reg["status"] = np.where(resolved, "RESOLVED", "OPEN")
    reg["resolved_tin"] = np.where(resolved, reg.true_tin, 0)
    first_pay = pay[pay.mis].groupby("reported_tin").local.min().dt.normalize()
    base = np.where(reg.source == "W2", pd.Timestamp("2026-02-16").value,
                    first_pay.reindex(reg.reported_tin).fillna(pd.Timestamp("2025-04-01")).astype("int64").to_numpy())
    opened = pd.to_datetime(base) + pd.to_timedelta(np.where(reg.source == "W2", rng.integers(0, 70, len(reg)), rng.integers(9, 45, len(reg))), unit="D")
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
            while rec.weekday() >= 5:
                rec = rec + pd.Timedelta(days=1)
            if rec.year != 2025:
                continue
            dep_id += int(rng.integers(1, 6))
            rows.append((dep_id, int(ein), sched, pe.date(), rec.date(), int(a)))
    dep = pd.DataFrame(rows, columns=["deposit_id", "employer_ein", "deposit_schedule", "period_end", "received_date", "amount"])
    return {"deposits": dep.sort_values(["received_date", "deposit_id"], kind="stable").reset_index(drop=True)}
