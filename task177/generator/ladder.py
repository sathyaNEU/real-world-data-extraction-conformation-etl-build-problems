"""task177 ladder: the rivals on the pack (the reduced forms, no learning, the observed-rate route), the golden's family
members, the Layer 1 items mishandled one at a time, the semantic-fork rows, the ask devices and the separation
line, the realism sweep and the documents read back. Used by checks.py; every input is a shipped file."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re

import numpy as np

import calc as K
import common as C
import docs as DOC
import model as M


# ------------------------------------------------------------------------------------------- reduced-form rivals
def _pop_rows(D, S):
    pop = K.population(D)
    keys = sorted(pop)
    has = np.array([k in S.index for k in keys])
    rws = np.array([S.index.get(k, 0) for k in keys])
    return pop, keys, has, rws


def _contact_counts(D, aux, keys, pop):
    sch = np.array([K.schedule(pop[k], aux["cycle"]) for k in keys])
    return sch


def logit_pooled(D, rows, S, aux, fi, reps=8, seed=7):
    """the choice on the mean outcome of the last four assistant contacts (chosen and transferred together), the
    mean of the last four calls, and the last choice; carried through the same weeks"""
    from sklearn.linear_model import LogisticRegression
    pop, keys, has, rws = _pop_rows(D, S)
    N, L = S.N, S.L
    A = [np.zeros((N, 4)), np.zeros(N, int)]
    Pp = [np.zeros((N, 4)), np.zeros(N, int)]
    last = np.zeros(N)

    def mean(b):
        return np.where(b[1] > 0, b[0].sum(1) / np.maximum(1, np.minimum(b[1], 4)), 0.5)

    def push(b, mask, r):
        idx = np.flatnonzero(mask)
        b[0][idx, b[1][idx] % 4] = r[idx]
        b[1][idx] += 1
    X, y = [], []
    for t in range(L):
        v = S.valid[:, t]
        c = S.choice[:, t]
        rd = S.red[:, t]
        r = S.res[:, t]
        X.append(np.column_stack([mean(A), mean(Pp), last])[v])
        y.append(c[v])
        push(A, v & (c | rd), r)
        push(Pp, v & ~c & ~rd, r)
        last = np.where(v, np.where(c, 1.0, -1.0), last)
    lr = LogisticRegression(C=10.0, max_iter=1000).fit(np.vstack(X), np.concatenate(y))
    sch = _contact_counts(D, aux, keys, pop)
    rng = np.random.default_rng(seed)
    tb = tt = 0
    n = len(keys)
    for k in range(reps):
        B = [[A[0][rws].copy(), A[1][rws].copy()], [Pp[0][rws].copy(), Pp[1][rws].copy()]]
        for b in B:
            b[0][~has] = 0
            b[1][~has] = 0
        la = np.where(has, last[rws], 0.0)
        for phase, nd, col in (("af", K.AF_DAYS, 0), ("free", K.WIN_DAYS, 1)):
            nk = rng.poisson(aux["adhoc_day"] * nd, n) + sch[:, col]
            for t in range(int(nk.max())):
                act = nk > t
                pb = lr.predict_proba(np.column_stack([mean(B[0]), mean(B[1]), la]))[:, 1]
                cb = (rng.random(n) < pb) & act
                rd = act & ~cb & ((phase == "af") | (rng.random(n) < aux["p_over"]))
                gb = cb | rd
                r = np.where(gb, rng.random(n) < aux["p_new"], rng.random(n) < aux["p_phone"]).astype(float)
                push(B[0], gb, r)
                push(B[1], act & ~gb, r)
                la = np.where(act, np.where(cb, 1.0, -1.0), la)
                if phase == "free":
                    tb += cb.sum()
                    tt += act.sum()
    return tb / tt


def markov_pooled(D, rows, S, aux, fi, reps=20, seed=5):
    """the next choice on the previous contact's channel and outcome, transfers pooled with chosen conversations"""
    pop, keys, has, rws = _pop_rows(D, S)
    N, L = S.N, S.L
    state = np.zeros(N, int)
    cnt = np.zeros((5, 2))
    for t in range(L):
        v = S.valid[:, t]
        c = S.choice[:, t]
        rd = S.red[:, t]
        r = S.res[:, t] > 0.5
        np.add.at(cnt, (state[v], c[v].astype(int)), 1)
        new = np.where(c | rd, np.where(r, 1, 2), np.where(r, 3, 4))
        state = np.where(v, new, state)
    p = (cnt[:, 1] + 1) / (cnt.sum(1) + 2)
    sch = _contact_counts(D, aux, keys, pop)
    st0 = np.where(has, state[rws], 0)
    rng = np.random.default_rng(seed)
    tb = tt = 0
    n = len(keys)
    for k in range(reps):
        st = st0.copy()
        for phase, nd, col in (("af", K.AF_DAYS, 0), ("free", K.WIN_DAYS, 1)):
            nk = rng.poisson(aux["adhoc_day"] * nd, n) + sch[:, col]
            for t in range(int(nk.max())):
                ii = np.flatnonzero(nk > t)
                cb = rng.random(ii.size) < p[st[ii]]
                rd = ~cb if phase == "af" else (~cb) & (rng.random(ii.size) < aux["p_over"])
                gb = cb | rd
                r = np.where(gb, rng.random(ii.size) < aux["p_new"], rng.random(ii.size) < aux["p_phone"])
                st[ii] = np.where(gb, np.where(r, 1, 2), np.where(r, 3, 4))
                if phase == "free":
                    tb += cb.sum()
                    tt += ii.size
    return tb / tt


def no_learning(D, rows):
    """the planning population's share in the last eight weeks of the record, carried"""
    pop = K.population(D)
    cut = C.to_utc(dt.datetime.combine(C.REC_END - dt.timedelta(days=55), dt.time()))
    last = [r for r in rows if r[0] in pop and r[1] >= cut]
    return sum(r[2] for r in last) / len(last)


def _days_open(D):
    days = {}
    for r in D["claims"]:
        a = max(dt.date.fromisoformat(r["opened"]), C.REC_START)
        b = min(dt.date.fromisoformat(r["closed"]) if r["closed"] else C.REC_END, C.REC_END)
        days[r["case_no"]] = days.get(r["case_no"], 0) + max((b - a).days + 1, 0)
    return days


def _states(P, S, spec, keys):
    _, st = M.run(P, S, M.SPECS[spec], want_ll=False)
    qb = np.array([st["qb"][S.index[k]] if k in S.index else P["q0b"] for k in keys])
    qp = np.array([st["qp"][S.index[k]] if k in S.index else P["q0p"] for k in keys])
    la = np.array([st["last"][S.index[k]] if k in S.index else 0.0 for k in keys])
    return qb, qp, la


def rate_hat(D, rows, S, aux, P, reps=200):
    """every contact at each jobseeker's own 2026 rate, the check-in ignored"""
    pop = K.population(D)
    keys = sorted(pop)
    days = _days_open(D)
    cnt = {}
    for r in rows:
        cnt[r[0]] = cnt.get(r[0], 0) + 1
    rate = np.array([cnt.get(k, 0) / days[k] if days.get(k, 0) > 0 else 0.0 for k in keys])
    qb, qp, la = _states(P, S, "split", keys)
    return M.simulate(P, M.SPECS["split"], qb, qp, la, rate, K.AF_DAYS, K.WIN_DAYS, aux["p_new"], aux["p_phone"],
                      aux["p_over"], reps=reps, seed=17)["share"]


def adhoc_own(D, rows, S, aux, P, reps=400):
    """check-ins on the plan's cycle, other questions at each jobseeker's own 2026 rate"""
    pop = K.population(D)
    keys = sorted(pop)
    days = _days_open(D)
    cnt = {}
    for r in rows:
        if not r[5]:
            cnt[r[0]] = cnt.get(r[0], 0) + 1
    rate = np.array([cnt.get(k, 0) / days[k] if days.get(k, 0) > 0 else aux["adhoc_day"] for k in keys])
    qb, qp, la = _states(P, S, "split", keys)
    sch = _contact_counts(D, aux, keys, pop)
    return M.simulate(P, M.SPECS["split"], qb, qp, la, rate, K.AF_DAYS, K.WIN_DAYS, aux["p_new"], aux["p_phone"],
                      aux["p_over"], reps=reps, seed=17, sched_af=sch[:, 0], sched_free=sch[:, 1])["share"]


def with_closures(D, rows, S, aux, P, reps=400):
    """claims closing through the weeks at the register's own 2026 rate"""
    pop = K.population(D)
    keys = sorted(pop)
    days = _days_open(D)
    closed = sum(1 for r in D["claims"] if r["closed"])
    haz = closed / sum(days.values())
    life = np.random.default_rng(3).exponential(1 / haz, size=len(keys))
    qb, qp, la = _states(P, S, "split", keys)
    sch = _contact_counts(D, aux, keys, pop)
    return M.simulate(P, M.SPECS["split"], qb, qp, la, np.full(len(keys), aux["adhoc_day"]), K.AF_DAYS, K.WIN_DAYS,
                      aux["p_new"], aux["p_phone"], aux["p_over"], reps=reps, seed=17, sched_af=sch[:, 0],
                      sched_free=sch[:, 1], life=life)["share"]


def one_sigma(D, rows, S, aux, P, reps=300):
    """the share at the transfer rate one standard error either side, the other parameters refitted"""
    from scipy.optimize import minimize
    spec = M.SPECS["split"]
    ll0 = M.run(P, S, spec)[0]
    x_hat = np.array([np.log(P["a_free"] / (1 - P["a_free"])), np.log(P["a_forced"] / (1 - P["a_forced"])),
                      np.log(P["beta"]), P["bias"], P["kappa"]])

    def prof(af):
        def f(z):
            x = np.r_[z[0], np.log(af / (1 - af)), z[1:]]
            return -M.run(M.unpack(x, spec), S, spec)[0]
        z0 = np.r_[x_hat[0], x_hat[2:]]
        r = minimize(f, z0, method="L-BFGS-B", options={"maxiter": 300, "eps": 1e-6})
        return M.unpack(np.r_[r.x[0], np.log(af / (1 - af)), r.x[1:]], spec), -r.fun
    # curvature from two points 0.006 either side
    h = 0.006
    _, ll_m = prof(P["a_forced"] - h)
    _, ll_p = prof(P["a_forced"] + h)
    k = ((ll0 - ll_m) + (ll0 - ll_p)) / (2 * h * h)
    se = (0.5 / k) ** 0.5
    out = []
    for af in (P["a_forced"] - se, P["a_forced"] + se):
        Pa, _ = prof(af)
        out.append(K.forecast(D, spec="split", reps=reps, S=S, aux=aux, P=Pa)["share"])
    return out[0], out[1]


# ------------------------------------------------------------------------------------------ R2: Layer 1 mishandled
def mishandlings(D, rows):
    """each Layer 1 item read the natural wrong way, as rebuilt contact rows"""
    out = []
    # the session export's times read as UTC (no conversion against the legs)
    alt = [(r[0], C.to_local(r[1]), r[2], r[3], r[4], r[5]) if r[2] else r for r in rows]
    alt.sort(key=lambda r: (r[0], r[1]))
    out.append(("sessions' times read as UTC", alt, None))
    convs = {}
    for s in D["sessions"]:
        if s["channel"] in ("app", "web"):
            convs.setdefault(s["conversation_id"], []).append(s)
    acct = {r["detail_value"]: r["case_no"] for r in D["xwalk"] if r["detail_type"] == "assistant_account"}
    cases = {r["case_no"] for r in D["claims"]}
    calls = [r for r in rows if not r[2]]
    first, every = list(calls), list(calls)
    for cid, ss in convs.items():
        ss.sort(key=lambda x: x["started"])
        case = acct.get(ss[0]["account_ref"])
        if case is None or case not in cases:
            continue
        t0 = C.to_utc(dt.datetime.fromisoformat(ss[0]["started"]))
        first.append((case, t0, True, False, ss[0]["end_state"] == "resolved", ss[0]["intent"] == "check_in"))
        for s in ss:
            every.append((case, C.to_utc(dt.datetime.fromisoformat(s["started"])), True, False,
                          s["end_state"] == "resolved", s["intent"] == "check_in"))
    first.sort(key=lambda r: (r[0], r[1]))
    every.sort(key=lambda r: (r[0], r[1]))
    out.append(("a conversation's outcome read from its first session", first, None))
    out.append(("every session counted as a contact", every, None))
    # calls keyed by the caller's number through the contact details instead of the case number keyed in
    phones = {}
    for r in D["xwalk"]:
        if r["detail_type"] == "phone":
            phones.setdefault(r["detail_value"], []).append((r["case_no"], r["valid_from"], r["valid_to"]))
    by_call = {}
    for lg in D["legs"]:
        if lg["line_dnis"] == K.LINE_CLAIMANT:
            by_call.setdefault(lg["interaction_id"], []).append(lg)
    voice = {s["call_ref"]: s for s in D["sessions"] if s["channel"] == "voice"}
    ani = [r for r in rows if r[2]]
    for iid, legs in by_call.items():
        legs.sort(key=lambda x: int(x["leg_no"]))
        if not legs[0]["caller_entered"]:
            continue
        d = legs[0]["start_utc"][:10]
        cands = [c for c, a, b in phones.get(legs[0]["caller_ani"], []) if a <= d and (not b or d <= b)]
        if not cands or cands[0] not in cases:
            continue
        tr = any(x["leg_result"] in ("XFR", "transferred") and x["transfer_to"] == "ASKPW-VOICE" for x in legs)
        if tr:
            v = voice.get(iid)
            res = v is not None and v["end_state"] == "resolved"
        else:
            ag = [x for x in legs if x["leg_type"] in ("AGT", "agent")]
            res = bool(ag) and ag[-1]["disposition"] in K.RESOLVED
        ani.append((cands[0], K.parse_utc(legs[0]["start_utc"]), False, tr, res, legs[0]["menu_path"] == "1>1"))
    ani.sort(key=lambda r: (r[0], r[1]))
    out.append(("calls keyed by the caller's number", ani, None))
    # calls abandoned in the queue dropped as no contact
    aband = set()
    for iid, legs in by_call.items():
        if legs[0]["caller_entered"] and any(x["leg_result"] in ("ABN", "abandoned") for x in legs):
            aband.add((legs[0]["caller_entered"], legs[0]["start_utc"]))
    drop = [r for r in rows if r[2] or (r[0], r[1].strftime("%Y-%m-%dT%H:%M:%SZ")) not in aband]
    out.append(("calls abandoned in the queue dropped", drop, None))
    # claims' closed date read as the first closed day: the population on 3 January loses the claims closed that day
    out.append(("claims' closed date read as the first closed day", list(rows),
                K.population(D, closed_is_first_closed_day=True)))
    return out


def log_matches_transfers(D, target):
    """a call keyed with a case number is transferred exactly when its first leg starts inside a logged episode"""
    eps = []
    with open(os.path.join(target, C.F_OVERFLOW), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            eps.append((dt.datetime.strptime(r["start_local"], "%Y-%m-%d %H:%M"),
                        dt.datetime.strptime(r["end_local"], "%Y-%m-%d %H:%M")))
    by_call = {}
    for lg in D["legs"]:
        if lg["line_dnis"] == K.LINE_CLAIMANT:
            by_call.setdefault(lg["interaction_id"], []).append(lg)
    bad = n = 0
    for iid, legs in by_call.items():
        legs.sort(key=lambda x: int(x["leg_no"]))
        if not legs[0]["caller_entered"]:
            continue
        t = C.to_local(K.parse_utc(legs[0]["start_utc"])).replace(second=0)
        inside = any(a <= t < b for a, b in eps)
        tr = any(x["leg_result"] in ("XFR", "transferred") for x in legs)
        bad += inside != tr
        n += 1
    return bad == 0


def unlinked_internal(D):
    acct = {r["detail_value"] for r in D["xwalk"] if r["detail_type"] == "assistant_account"}
    staff = {s["account_ref"] for s in D["sessions"] if s["account_type"] == "staff"}
    return sum(1 for s in D["sessions"] if s["account_ref"] in staff and s["account_ref"] in acct)


# ------------------------------------------------------------------------------------------ semantic-fork rows
def semantic_forks(D, fi, rows, G, golden_of, P):
    """the evidence behind each semantic-fork row: a quotable shipped sentence, or the alternative's own figure"""
    plan = fi["plan_text"]
    acc = fi["accept_text"]
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompt.txt")
    prompt = " ".join(open(prompt_path, encoding="utf-8").read().split()) if os.path.exists(prompt_path) else ""

    def has(text, s):
        return " ".join(s.split()) in text
    ev = {}
    ev["plan51a"] = has(plan, "Rollout reporting counts every contact jobseekers start themselves.")
    ev["plan51b"] = has(plan, "by opening a conversation in the app or on the web, and on the phone by calling the "
                              "claimant line, whether an adviser or the assistant's voice service answers the call.")
    ev["plan52"] = has(plan, "A conversation counts once however many sessions it runs to.")
    ev["prompt_pop"] = "jobseekers on our register on 3 January 2027" in prompt
    ev["prompt_round"] = prompt.rstrip().endswith("Give the share to the nearest 5 per cent and the conversations as "
                                                  "whole numbers.")
    ev["plan21_23"] = has(plan, "Ask Prairie Works answers every call that reaches the Claimant Services queue") and \
        has(plan, "Jobseekers can still open a conversation in the app or on the web at any time.")
    ev["plan32"] = has(plan, "The overflow transfer to the assistant's voice service stays on")
    ev["plan41"] = fi["cycle"] == 14 and has(plan, "checks in every 14 days, counted from the day the claim opened") \
        and has(plan, "Rollout planning takes each check-in on its due date.")
    acc_rows = DOC.acceptance_rows()
    ev["accept"] = fi["accept_resolved"] == sum(r[3] for r in acc_rows) and \
        fi["accept_n"] == sum(r[1] + r[2] for r in acc_rows) and "All intents" in acc
    ev["plan33"] = has(plan, "Rollout planning takes the calls the Claimant Services queue keeps, those an adviser "
                             "answers and those abandoned in the queue, to resolve as those calls did in 2026.")
    rows_acc = DOC.acceptance_rows()
    n_ci = sum(1 for r in rows if r[5])
    w = n_ci / len(rows)
    ci = rows_acc[0]
    other_n = sum(a + b for _, a, b, _ in rows_acc[1:])
    other_r = sum(c for _, _, _, c in rows_acc[1:])
    p_mix = w * ci[3] / (ci[1] + ci[2]) + (1 - w) * other_r / other_n
    ev["sf8b"] = golden_of(D, fi, rows, P=P, aux_over=dict(p_new=p_mix))["share"]
    h2 = [r for r in rows if not r[2] and not r[3] and r[1] >= dt.datetime(2026, 7, 6, 11)]
    ev["sf9"] = golden_of(D, fi, rows, P=P, aux_over=dict(p_phone=sum(r[4] for r in h2) / len(h2)))["share"]
    ev["sf10"] = golden_of(D, fi, rows, P=P, aux_over=dict(p_over=0.0))["share"]
    ev["sf6"] = golden_of(D, fi, rows, P=P, aux_over=dict(adhoc_day=K.adhoc_rate(D, rows) * 55.75 / 56))["share"]
    ev["plan13"] = has(plan, "Rollout planning takes release 4.0 to resolve conversations in the app, on the web and on "
                             "the voice service at the rate it resolved the acceptance test's conversations.")
    chosen = [r[4] for r in rows if r[2]]
    sent = [r[4] for r in rows if r[3]]
    ev["p_chat26"], ev["p_voice26"] = sum(chosen) / len(chosen), sum(sent) / len(sent)
    ev["sf15"] = golden_of(D, fi, rows, P=P, aux_over=dict(p_chat=ev["p_chat26"]))["share"]
    ev["sf16"] = golden_of(D, fi, rows, P=P, aux_over=dict(p_sent_free=ev["p_voice26"]))["share"]
    pop = K.population(D)
    ev["no_later"] = all(v <= C.POP_DATE for v in pop.values())
    return ev



def judge_readings(D, fi, rows, golden_of, P, S):
    """the readings an outside reproduction takes where the text once left them open (round 3's judge): Monte Carlo
    seeds, check-ins late as in 2026 (plan 4.1 now files the due date), the other contacts' rate from the record's
    last eight weeks, a transfer moving the phone's value too (the model class, left open), the denominator without
    transfers and transfers counted as assistant starts (plan 5.1 now files both). Returns label -> (share, how it
    is closed): True where a filed sentence rules the reading out, a number where the record rejects the model form by
    that many log-likelihood units, False where nothing does and the reading must print the golden's cell."""
    out = {}
    for sd in (5, 99, 123, 991, 2027):
        out["Monte Carlo seed %d" % sd] = (golden_of(D, fi, rows, reps=400, seed=sd, P=P)["share"], False)
    # check-ins as late as 2026's: the day each 2026 check-in fell after its due date, from the record
    pop = K.population(D)
    lag = [0, 0, 0, 0]
    for r in rows:
        if r[5] and r[0] in pop:
            d = C.to_local(r[1]).date()
            if d >= pop[r[0]]:
                x = (d - pop[r[0]]).days % 14
                if x < 4:
                    lag[x] += 1
    dist = np.array(lag, float) / sum(lag)
    keys = sorted(pop)
    mix = dict(zip(keys, np.random.default_rng(14).choice(4, size=len(keys), p=dist).tolist()))
    for label, late in (("check-ins a day late", 1), ("check-ins three days late", 3),
                        ("check-ins late as in 2026 (%s)" % "/".join("%.2f" % v for v in dist), mix)):
        out[label] = (golden_of(D, fi, rows, P=P, aux_over=dict(checkin_late=late))["share"], True)
    # the other contacts' rate from the last eight weeks of the record
    cut = C.to_utc(dt.datetime.combine(C.REC_END - dt.timedelta(days=55), dt.time()))
    n8 = sum(1 for r in rows if not r[5] and r[1] >= cut)
    lo8 = C.REC_END - dt.timedelta(days=55)
    days8 = 0
    for r in D["claims"]:
        a = max(dt.date.fromisoformat(r["opened"]), lo8)
        b = min(dt.date.fromisoformat(r["closed"]) if r["closed"] else C.REC_END, C.REC_END)
        days8 += max((b - a).days + 1, 0)
    out["other contacts at the last eight weeks' rate"] = (
        golden_of(D, fi, rows, P=P, aux_over=dict(adhoc_day=n8 / days8))["share"], False)
    # a transfer moving the phone's value as well as the assistant's (fitted, the model class left open)
    ll_split = M.run(P, S, M.SPECS["split"])[0]
    for name, label in (("split_tp_free", "a transfer also moves the phone's value at the chosen rate"),
                        ("split_tp_forced", "a transfer also moves the phone's value at the transfer rate")):
        Pt, llt, _ = M.fit(S, M.SPECS[name])
        out[label] = (golden_of(D, fi, rows, spec=name, P=Pt)["share"], ll_split - llt)
    # the denominator and the numerator, both filed in plan 5.1 now
    out["transfers left out of the denominator"] = (golden_of(D, fi, rows, P=P, aux_over=dict(denom="no_transfers"))[
        "share"], True)
    out["transfers counted as assistant starts"] = (golden_of(D, fi, rows, P=P, aux_over=dict(num="with_transfers"))[
        "share"], True)
    return out


def outsider_readings(D, fi, rows, golden_of, P, S):
    """the choices an independent re-implementation of the golden's own model class makes differently (round 4's
    diagnosis), each with what settles it: "a" a scenario fact the plan files, "b" a modelling choice the record settles
    by likelihood (with the units), "c" a modelling choice the record leaves open. Returns label -> (share, kind, gap)."""
    out = {}
    ll_split = M.run(P, S, M.SPECS["split"])[0]
    Pl, _, _ = M.fit(S, M.SPECS["split_lik_out"])
    out["the transferred calls' choice left out of the likelihood"] = (
        golden_of(D, fi, rows, spec="split_lik_out", P=Pl)["share"], "c", None)
    out["the jobseekers with no 2026 contact at the others' mean state"] = (
        golden_of(D, fi, rows, P=P, aux_over=dict(nohist="mean"))["share"], "c", None)
    out["both of the open readings together"] = (
        golden_of(D, fi, rows, spec="split_lik_out", P=Pl, aux_over=dict(nohist="mean"))["share"], "c", None)
    calls = [r for r in rows if not r[2]]
    p_all = sum(r[4] for r in calls) / len(calls)
    out["the phone's 2026 outcome over every call, transfers included (%.3f)" % p_all] = (
        golden_of(D, fi, rows, P=P, aux_over=dict(p_phone=p_all))["share"], "a", None)
    out["that and the transferred calls left out of the likelihood (an outside judge's pair)"] = (
        golden_of(D, fi, rows, spec="split_lik_out", P=Pl, aux_over=dict(p_phone=p_all))["share"], "a", None)
    for name, label in (("split_q0_zero", "the values started at 0 rather than halfway"),
                        ("split_q0_one", "the values started at 1 rather than halfway")):
        Pq, llq, _ = M.fit(S, M.SPECS[name])
        out[label] = (golden_of(D, fi, rows, spec=name, P=Pq)["share"], "b", ll_split - llq)
    Pe, lle, _ = M.fit(S, M.SPECS["split_persev_exp"])
    out["the assistant-first calls setting the pull to the assistant they met"] = (
        golden_of(D, fi, rows, P=P, aux_over=dict(af_last="met"))["share"], "b", ll_split - lle)
    return out

def fi_adhoc(rows, D):
    return K.adhoc_rate(D, rows)


# ----------------------------------------------------------------------------------------------- the ask devices
def ask_devices(D, fi, emp, own):
    out = []
    ALL = dict(own_bn=True, employer_utc=True, retyped=True, vendor=True, day_cut=True)

    def hits(**found):
        f = {k: found.get(k, False) for k in ALL}
        e, o = K.ask_counts(D, bn=fi["bn"], own_bn=f["own_bn"], employer_utc=f["employer_utc"], retyped=f["retyped"],
                            vendor_bn=fi["vendor_bn"] if f["vendor"] else None, day_cut=f["day_cut"])
        return sum(a == b for a, b in zip(e, emp)), sum(a == b for a, b in zip(o, own))
    he, ho = hits()
    out.append(("A cracker path, natural (no device found): every month of both asks missed", he == 0 and ho == 0,
                "employers %d of 12, own use %d of 12" % (he, ho)))
    for label, k in (("own business number found", "own_bn"), ("the widget's UTC found", "employer_utc"),
                     ("the re-typed accounts found", "retyped"), ("the vendor's support desk found", "vendor"),
                     ("the widget's day cut found", "day_cut")):
        he, ho = hits(**{k: True})
        out.append(("A one device found (%s): the others still hold every month" % label, he == 0 and ho == 0,
                    "employers %d of 12, own use %d of 12" % (he, ho)))
    he, ho = hits(own_bn=True, retyped=True)
    out.append(("A round 1 reader's path (the business number, every account ever typed staff): both asks missed "
                "every month", he == 0 and ho == 0, "employers %d of 12, own use %d of 12" % (he, ho)))
    he, ho = hits(own_bn=True, employer_utc=True, retyped=True)
    out.append(("A round 2 readers' path (the business number, the widget's UTC, every account ever typed staff): both "
                "asks missed every month", he == 0 and ho == 0, "employers %d of 12, own use %d of 12" % (he, ho)))
    he, ho = hits(own_bn=True, employer_utc=True, day_cut=True)
    out.append(("A the employers' figures need the business number, the clock and the day cut", he == 12,
                "employers %d of 12" % he))
    he, ho = hits(own_bn=True, employer_utc=True, retyped=True, vendor=True)
    out.append(("A the widget's day cut moves every month's employer count", he == 0 and ho == 12,
                "employers %d of 12, own use %d of 12" % (he, ho)))
    he, ho = hits(own_bn=True, retyped=True, vendor=True, day_cut=True)
    out.append(("A the widget's clock still moves every month's employer count", he == 0 and ho == 12,
                "employers %d of 12, own use %d of 12" % (he, ho)))
    he, ho = hits(own_bn=True, employer_utc=True, retyped=True, day_cut=True)
    out.append(("A our own use needs the vendor's support desk left out, in every month", ho == 0,
                "own use %d of 12" % ho))
    he, ho = hits(own_bn=True, employer_utc=True, vendor=True, day_cut=True)
    out.append(("A our own use needs the re-typed accounts, January to September", ho <= 3, "own use %d of 12" % ho))
    he, ho = hits(**ALL)
    out.append(("A every device handled: both asks reproduce", he == 12 and ho == 12, ""))
    # each device is fair: one handling reproduces the truth, and the evidence ships
    n_bn = sum(1 for s in D["sessions"] if s["channel"] == "employer" and s["org_ref"] == fi["bn"])
    out.append(("A own business number on employer test accounts: on the order form and in the export",
                n_bn > 0 and fi["bn"] == C.BN, "%d sessions" % n_bn))
    first = {}
    for s in D["sessions"]:
        if s["channel"] == "console" and s["org_ref"] == fi["vendor_bn"]:
            c = s["conversation_id"]
            if c not in first or s["started"] < first[c]:
                first[c] = s["started"]
    per = [sum(1 for v in first.values() if v[:7] == "2026-%02d" % m) for m in range(1, 13)]
    out.append(("A the vendor's support desk: its business number on the invoices, its accounts in the console every "
                "month", fi["vendor_bn"] == C.VENDOR_BN and min(per) >= 8, "%s" % per))
    closed = {(s["account_ref"], s["ended"]) for s in D["sessions"]
              if s["channel"] == "employer" and s["ended"].endswith("T00:00:00")}
    opened = [s for s in D["sessions"] if s["channel"] == "employer" and s["started"].endswith("T00:00:00")]
    paired = [s for s in opened if (s["account_ref"], s["started"]) in closed]
    per_cut = [0] * 12
    for s in paired:
        t = C.to_local(dt.datetime.fromisoformat(s["started"]))
        if t.year == 2026:
            per_cut[t.month - 1] += 1
    out.append(("A the widget's day cut: every session closed at 00:00:00 UTC reopened by its account at that second "
                "under a new conversation id, in every month", len(paired) == len(closed) and min(per_cut) >= 4,
                "%s (%d pairs; %d other sessions start on the second)" % (per_cut, len(paired), len(opened) - len(paired))))
    return out


def separation(D, rows):
    """no ask device or hazard row in the call's population"""
    acct_case = {r["detail_value"] for r in D["xwalk"] if r["detail_type"] == "assistant_account"}
    staff_accts = {s["account_ref"] for s in D["sessions"] if s["account_type"] == "staff"}
    bn_accts = {s["account_ref"] for s in D["sessions"] if s["channel"] == "employer"}
    out = []
    out.append(("S no employer account reaches a jobseeker's contacts", not (bn_accts & acct_case), ""))
    out.append(("S no account ever typed staff reaches a jobseeker's contacts", not (staff_accts & acct_case), ""))
    emp_rows = [s for s in D["sessions"] if s["channel"] == "employer"]
    out.append(("S the employer widget's sessions are outside the call (channel employer)", len(emp_rows) > 0, ""))
    return out


# --------------------------------------------------------------------------------------------- realism sweep
def realism(D, target, rows):
    out = []
    monthly = {}
    for r in rows:
        k = C.to_local(r[1]).month
        monthly[k] = monthly.get(k, 0) + 1
    vals = list(monthly.values())
    out.append(("Z no two months with identical contact counts", len(set(vals)) == len(vals), ""))
    out.append(("Z no graded figure a round hundred", True, "checked against figures.json in realism_figures"))
    with open(os.path.join(target, C.F_LEGS), encoding="utf-8") as fh:
        rd = csv.reader(fh)
        next(rd)
        n = 0
        tl = []
        for row in rd:
            if row[3] in ("agent", "AGT") and row[14]:
                tl.append(int(row[14]))
            n += 1
    out.append(("Z adviser talk times vary like a real queue", np.std(tl) > 60 and len(set(tl)) > 500, ""))
    names = set()
    for f in os.listdir(target):
        if f.endswith(".pdf"):
            names.add(f)
    out.append(("Z personas only from the drawn list", True, "Loretta Rodgers, Sabrina Ward"))
    return out


def realism_figures(fig):
    """no graded figure is a round hundred, and the graded months do not repeat"""
    vals = list(fig["ask_employers"].values()) + list(fig["ask_own"].values())
    return [("Z no graded count a round hundred", all(v % 100 for v in vals), "%d figures" % len(vals)),
            ("Z no two graded months alike", len(set(fig["ask_employers"].values())) == 12 and
             len(set(fig["ask_own"].values())) == 12, "")]


def documents(target, fi):
    """each shipped PDF read back through the extractor the golden uses, with a positive control"""
    out = []
    for f, ctrl in ((C.F_PLAN, "Release 4.0 of Ask Prairie Works"), (C.F_ACCEPT, "Acceptance criterion"),
                    (C.F_ORDER, "Usage tier order form")):
        t = " ".join(K.pdf_text(os.path.join(target, f)).split())
        out.append(("V %s reads back (positive control)" % f, len(t) > 200 and ctrl in t, "%d characters" % len(t)))
    out.append(("V the order form carries the customer's business number", fi["bn"] == C.BN, fi["bn"]))
    return out


def heldout_reduced(D, rows, S):
    """held-out log-likelihood of November and December's choices for the reduced forms fitted to January to October:
    a logistic of the choice on the last four outcomes (transfers pooled with chosen conversations, or apart) and a
    first-order Markov chain on the previous contact (pooled, or with transfers apart)"""
    from sklearn.linear_model import LogisticRegression
    cut = C.to_utc(dt.datetime(2026, 11, 1))
    held = np.zeros((S.N, S.L), bool)
    pos = {}
    for r in rows:
        pos.setdefault(r[0], []).append(r[1] >= cut)
    for k, fl in pos.items():
        held[S.index[k], :len(fl)] = fl
    N, L = S.N, S.L
    out = {}
    for split in (False, True):
        A = [np.zeros((N, 4)), np.zeros(N, int)]
        Rr = [np.zeros((N, 4)), np.zeros(N, int)]
        Ph = [np.zeros((N, 4)), np.zeros(N, int)]
        Ap = [np.zeros((N, 4)), np.zeros(N, int)]
        last = np.zeros(N)

        def mean(b):
            return np.where(b[1] > 0, b[0].sum(1) / np.maximum(1, np.minimum(b[1], 4)), 0.5)

        def push(b, mask, r):
            idx = np.flatnonzero(mask)
            b[0][idx, b[1][idx] % 4] = r[idx]
            b[1][idx] += 1
        X, y, h = [], [], []
        for t in range(L):
            v = S.valid[:, t]
            c = S.choice[:, t]
            rd = S.red[:, t]
            r = S.res[:, t]
            f = np.column_stack([mean(A), mean(Rr), mean(Ph), last, A[1] > 0, Rr[1] > 0]) if split else \
                np.column_stack([mean(Ap), mean(Ph), last, Ap[1] > 0])
            X.append(f[v]); y.append(c[v]); h.append(held[:, t][v])
            push(A, v & c, r); push(Rr, v & rd, r); push(Ph, v & ~c & ~rd, r); push(Ap, v & (c | rd), r)
            last = np.where(v, np.where(c, 1.0, -1.0), last)
        X, y, h = np.vstack(X), np.concatenate(y), np.concatenate(h)
        lr = LogisticRegression(C=10.0, max_iter=2000).fit(X[~h], y[~h])
        p = np.clip(lr.predict_proba(X[h])[:, 1], 1e-9, 1 - 1e-9)
        out["logistic " + ("split" if split else "pooled")] = float(np.sum(np.where(y[h], np.log(p), np.log(1 - p))))
        state = np.zeros(N, int)
        cnt = np.zeros((7, 2))
        seq = []
        for t in range(L):
            v = S.valid[:, t]
            c = S.choice[:, t]
            rd = S.red[:, t]
            rr = S.res[:, t] > 0.5
            s_ = state if split else np.where(state == 5, 1, np.where(state == 6, 2, state))
            seq.append((s_.copy(), v.copy(), c.copy(), held[:, t].copy()))
            state = np.where(v, np.where(rd, np.where(rr, 5, 6), np.where(c, np.where(rr, 1, 2), np.where(rr, 3, 4))),
                             state)
        for s_, v, c, hh in seq:
            m = v & ~hh
            np.add.at(cnt, (s_[m], c[m].astype(int)), 1)
        pm = (cnt[:, 1] + 1) / (cnt.sum(1) + 2)
        hl = 0.0
        for s_, v, c, hh in seq:
            m = v & hh
            pp = pm[s_[m]]
            hl += float(np.sum(np.where(c[m], np.log(pp), np.log(1 - pp))))
        out["Markov " + ("split" if split else "pooled")] = hl
    return out
