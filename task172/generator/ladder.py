"""task172 ladder: every natural route to the quote, computed on the cut pack, and the out-of-sample test that rejects
the uncapped stage model. Never shipped; checks.py asserts each route's distance from the golden."""
from __future__ import annotations

import datetime as dt
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K     # noqa: E402
import common as C   # noqa: E402

M = C.MONTH_DAYS
OLD = (dt.date(2025, 10, 30), dt.date(2026, 8, 23))      # post-IFR receipts on the old appointment lead
RAMP_START = dt.date(2026, 9, 1)                          # "before September 2026" in the write-up


def wait_rows(rens, lo=None, hi=None, route=None):
    rows = []
    for r in rens:
        if r["withdrawn"] or r["received"] is None:
            continue
        if lo and r["received"] < lo or hi and r["received"] > hi:
            continue
        if route and r["route"] != route:
            continue
        end = min(x for x in (C.EXPORT, r["stop"]) if x)
        if r["decided"] and r["decided"] <= end:
            rows.append(((r["decided"] - r["received"]).days, 1))
        else:
            rows.append(((end - r["received"]).days, 0))
    return rows


def routes(Q):
    rens, comp, T = Q["rens"], Q["comp"], Q["T"]
    out = {}
    # the government's posted time, latest capture
    last = max(p["captured_on"] for p in T["posted"])
    cur = {(p["form_line"], p["office"]): float(p["posted_months"]) for p in T["posted"] if p["captured_on"] == last}
    for (line, office), v in sorted(cur.items()):
        out["posted, %s, %s" % (line, office)] = v
    rec_all = wait_rows(rens, hi=dt.date(2026, 11, 30))
    out["record KM, all receipts"] = K.km_quantile(rec_all) / M
    out["record KM, since 30 Oct 2025"] = K.km_quantile(wait_rows(rens, lo=C.IFR)) / M
    out["record KM, last 12 months"] = K.km_quantile(wait_rows(rens, lo=dt.date(2025, 12, 1))) / M
    dec = [r for r in rens if r["decided"] and not r["withdrawn"]]
    lastq = [(r["decided"] - r["received"]).days for r in dec if dt.date(2026, 9, 1) <= r["decided"] <= C.EXPORT]
    out["decided Sep to Nov 2026, q80"] = float(np.quantile(lastq, 0.8)) / M
    allw = np.array([(r["decided"] - r["received"]).days for r in dec], float)
    out["decided only, q80"] = float(np.quantile(allw, 0.8)) / M
    last12 = np.array([(r["decided"] - r["received"]).days for r in dec if r["decided"] >= dt.date(2025, 12, 1)], float)
    out["mean plus one sd, decided last 12 months"] = (last12.mean() + last12.std()) / M
    old_lead = np.array([(r["appt"] - r["received"]).days for r in rens if r["route"] == "appointment" and r["appt"] and
                         OLD[0] <= r["received"] <= OLD[1]], float)
    dL = float(np.median(comp["L"]) - np.median(old_lead))
    out["_dL_days"] = dL
    # the default path: the appointment delay now being set laid on the record's appointment-route waits
    shifted = []
    for r in rens:
        if r["withdrawn"] or r["received"] is None or not (OLD[0] <= r["received"] <= OLD[1]) or not r["route"]:
            continue
        end = min(x for x in (C.EXPORT, r["stop"]) if x)
        add = dL if r["route"] == "appointment" else 0.0
        if r["decided"] and r["decided"] <= end:
            shifted.append(((r["decided"] - r["received"]).days + add, 1))
        else:
            shifted.append(((end - r["received"]).days + add, 0))
    out["default: post-rule record, appointment waits plus the new delay"] = K.km_quantile(shifted) / M
    recent = K.km_quantile(wait_rows(rens, lo=OLD[0], hi=OLD[1])) / M
    out["record since the rule plus the new delay, flat"] = recent + dL / M
    out["record since the rule plus the new delay times the appointment share"] = recent + comp["pA"] * dL / M
    w, _ = K.simulate(comp, cap=False)
    out["stage model, uncapped"] = float(np.quantile(w, 0.8)) / M
    rng = np.random.default_rng(7)
    n = K.N_SIM
    appt = rng.random(n) < comp["pA"]
    vals, ps = K.km_points(comp["qrows"])
    Qd = rng.choice(vals, n, p=ps)
    L = rng.choice(comp["L"], n)
    Dd = rng.choice(comp["D"], n)
    E = rng.choice(comp["E"], n)
    wn = np.where(appt, L, 0.0) + Qd
    out["cut at the card's expiry, no expedite response"] = float(np.quantile(np.minimum(wn, Dd), 0.8)) / M
    out["every renewal cut: q80 of expiry plus response"] = float(np.quantile(Dd + E, 0.8)) / M
    naive = out["record KM, all receipts"]
    for b in (0.5, 1.0, 1.5, 2.0):
        out["record plus %.1f months" % b] = naive + b
    for k in (1.25, 1.5):
        out["record times %.2f" % k] = naive * k
    out["post-rule record, 97.5th percentile"] = K.km_quantile(wait_rows(rens, lo=C.IFR), 0.975) / M
    for lo in (42, 56):
        sub = [((r["decided"] - r["received"]).days, 1) for r in dec if r["route"] == "appointment" and r["appt"] and
               (r["appt"] - r["received"]).days >= lo]
        out["decided renewals with an appointment %d days or more out" % lo] = (
            float(np.quantile([s[0] for s in sub], 0.8)) / M if len(sub) >= 5 else float("nan"))
        out["_n_lead_%d" % lo] = len(sub)
    ex = [(r["decided"] - r["received"]).days for r in dec if r["exp_req"] and r["exp_out"] == "Accepted"]
    out["renewals decided after an expedite request, q80"] = float(np.quantile(ex, 0.8)) / M
    out["_longest_decided_post_rule_lead"] = float(max((r["appt"] - r["received"]).days for r in dec
                                                       if r["route"] == "appointment" and r["appt"] and
                                                       r["received"] >= C.IFR))
    return out


def backtest(Q):
    """out of sample: the renewals filed since the rule change that were still pending on their card's expiry. The
    uncapped stage model, fitted on the renewals filed before the change, predicts how much longer each would wait
    given the days it had already waited; the record shows what happened"""
    rens, comp = Q["rens"], Q["comp"]
    pre = [r for r in rens if r["received"] < C.IFR]
    prows = []
    for r in pre:
        st = r["appt"] if r["route"] == "appointment" else r["received"]
        if st is None or r["withdrawn"]:
            continue
        end = min(x for x in (C.EXPORT, r["stop"]) if x)
        if r["decided"] and r["decided"] <= end:
            prows.append(((r["decided"] - st).days, 1))
        else:
            prows.append(((end - st).days, 0))
    vals, ps = K.km_points([p for p in prows if p[0] >= 0])
    hold = [r for r in rens if r["received"] >= C.IFR and r["exp_req"] and r["exp_out"] == "Accepted" and r["decided"]]
    pred, obs = [], []
    for r in hold:
        st = r["appt"] if r["route"] == "appointment" else r["received"]
        if st is None:
            continue
        elapsed = (r["exp_req"] - st).days
        mask = vals > elapsed
        if not mask.any():
            continue
        cond_v, cond_p = vals[mask], ps[mask] / ps[mask].sum()
        pred.append(float(np.sum(cond_v * cond_p)) - elapsed)
        obs.append((r["decided"] - r["exp_req"]).days)
    pred, obs = np.array(pred), np.array(obs)
    e_med = float(np.median(comp["E"]))
    return dict(n=len(obs), obs_median=float(np.median(obs)), obs_mean=float(obs.mean()),
                uncapped_pred_median=float(np.median(pred)), uncapped_pred_mean=float(pred.mean()),
                uncapped_mae=float(np.mean(np.abs(pred - obs))), capped_mae=float(np.mean(np.abs(e_med - obs))),
                share_within_14=float(np.mean(obs <= 14)))


def variants(Q):
    """the golden under every standard construction the record supports"""
    rens = Q["rens"]
    out = {}
    base = K.components(rens)
    out["golden (Oct to Nov leads, Q by Kaplan-Meier, D since the rule)"] = float(np.quantile(K.simulate(base)[0], .8)) / M
    out["leads from 14 September"] = float(np.quantile(K.simulate(K.components(
        rens, regime=(dt.date(2026, 9, 14), dt.date(2026, 11, 30))))[0], .8)) / M
    out["leads, November only"] = float(np.quantile(K.simulate(K.components(
        rens, regime=(dt.date(2026, 11, 1), dt.date(2026, 11, 30))))[0], .8)) / M
    out["leads, October only"] = float(np.quantile(K.simulate(K.components(
        rens, regime=(dt.date(2026, 10, 1), dt.date(2026, 10, 31))))[0], .8)) / M
    out["review from decided renewals only"] = float(np.quantile(K.simulate(K.components(rens, q_mode="decided"))[0], .8)) / M
    out["card gap from the whole record"] = float(np.quantile(K.simulate(K.components(rens, d_from=C.RECORD_START))[0], .8)) / M
    out["every expedite accepted"] = float(np.quantile(K.simulate(base, use_accept=False)[0], .8)) / M
    c2 = dict(base)
    c2["E"] = np.full(len(base["E"]), float(np.median(base["E"])))
    out["expedite response at its median"] = float(np.quantile(K.simulate(c2)[0], .8)) / M
    c3 = dict(base)
    rng = np.random.default_rng(3)
    logL = np.log(base["L"])
    c3_lead = (lambda r, n, mu=logL.mean(), sd=logL.std(): np.exp(r.normal(mu, sd, n)))
    out["lead as a fitted lognormal"] = float(np.quantile(K.simulate(base, lead_add=c3_lead)[0], .8)) / M
    out["month of 365.25/12 days"] = float(np.quantile(K.simulate(base)[0], .8)) / (365.25 / 12)
    for s in (1, 2, 3):
        out["simulation seed %d" % s] = float(np.quantile(K.simulate(base, seed=s)[0], .8)) / M
    # analog: the post-rule record re-run with the new appointment delay, each renewal cut at its own card's expiry
    rng = np.random.default_rng(11)
    ws = []
    E = base["E"]
    for r in rens:
        if r["withdrawn"] or r["received"] is None or not (OLD[0] <= r["received"] <= OLD[1]) or not r["route"]:
            continue
        if not r["card_exp"]:
            continue
        st = r["appt"] if r["route"] == "appointment" else r["received"]
        end = min(x for x in (C.EXPORT, r["stop"]) if x)
        if r["exp_req"] or not (r["decided"] and r["decided"] <= end):
            continue
        q = (r["decided"] - st).days
        D = (r["card_exp"] - r["received"]).days
        for _ in range(20):
            L = rng.choice(base["L"]) if r["route"] == "appointment" else 0.0
            wn = L + q
            ws.append(min(wn, D + rng.choice(E)) if wn > D else wn)
    out["analog: post-rule decided renewals re-run on the new delay"] = float(np.quantile(ws, 0.8)) / M
    return out


def one_sigma(Q):
    """each component moved by one standard error, the quote recomputed"""
    comp = Q["comp"]
    out = {}
    for name, key in (("lead", "L"), ("card gap", "D"), ("expedite response", "E")):
        arr = comp[key]
        se = float(arr.std() / np.sqrt(len(arr)))
        for sgn in (-1, 1):
            c = dict(comp)
            c[key] = arr + sgn * se
            out["%s %+d se" % (name, sgn)] = float(np.quantile(K.simulate(c)[0], .8)) / M
    c = dict(comp)
    pA_se = float(np.sqrt(comp["pA"] * (1 - comp["pA"]) / comp["n_rec"]))
    for sgn in (-1, 1):
        c = dict(comp)
        c["pA"] = comp["pA"] + sgn * pA_se
        out["appointment share %+d se" % sgn] = float(np.quantile(K.simulate(c)[0], .8)) / M
    vals, ps = K.km_points(comp["qrows"])
    qs = np.array([q[0] for q in comp["qrows"] if q[1] == 1], float)
    se = float(qs.std() / np.sqrt(len(qs)))
    for sgn in (-1, 1):
        c = dict(comp)
        c["qrows"] = [(q[0] + sgn * se, q[1]) for q in comp["qrows"]]
        out["review %+d se" % sgn] = float(np.quantile(K.simulate(c)[0], .8)) / M
    return out


if __name__ == "__main__":
    Q = K.quote(sys.argv[1])
    for k, v in routes(Q).items():
        print("%-75s %8.3f%s" % (k, v, "" if k.startswith("_") else "  -> %.1f" % C.half_month(v)))
    print(backtest(Q))
    for k, v in variants(Q).items():
        print("variant %-62s %.3f -> %.1f" % (k, v, C.half_month(v)))
    for k, v in one_sigma(Q).items():
        print("one sigma %-40s %.3f -> %.1f" % (k, v, C.half_month(v)))
