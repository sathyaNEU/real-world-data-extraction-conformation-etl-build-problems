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


def weighted_km_quantile(rows, p=0.8):
    """Kaplan-Meier with case weights: (time, event, weight) rows"""
    rows = sorted(rows)
    tot = sum(r[2] for r in rows)
    at_risk, S, i, n = tot, 1.0, 0, len(rows)
    while i < n:
        t, d, wsum, j = rows[i][0], 0.0, 0.0, i
        while j < n and rows[j][0] == t:
            d += rows[j][2] * rows[j][1]
            wsum += rows[j][2]
            j += 1
        if d:
            S *= 1 - d / at_risk
            if S <= 1 - p + 1e-12:
                return t
        at_risk -= wsum
        i = j
    return float("nan")


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
    # the same shift at the quarter's own appointment share: a percentile moved by a mean, landing by coincidence
    pA_q = sum(Q["mix"][c] * comp["pA_cat"][c] for c in C.CATS)
    out["_pA_quarter"] = pA_q
    out["record since the rule plus the new delay times the quarter's appointment share"] = recent + pA_q * dL / M
    out["record, all receipts, plus the new delay times the quarter's appointment share"] = (
        K.km_quantile(rec_all) / M + pA_q * dL / M)
    # the default path reweighted to the quarter's categories: the post-rule rows (all (c)(26)) weighted so the
    # appointment route carries the quarter's share
    pA_post = float(np.mean([r["route"] == "appointment" for r in rens if r["route"] and not r["withdrawn"] and
                             OLD[0] <= r["received"] <= OLD[1]]))
    wrows = []
    for r in rens:
        if r["withdrawn"] or r["received"] is None or not (OLD[0] <= r["received"] <= OLD[1]) or not r["route"]:
            continue
        end = min(x for x in (C.EXPORT, r["stop"]) if x)
        ap = r["route"] == "appointment"
        add = dL if ap else 0.0
        wt = pA_q / pA_post if ap else (1 - pA_q) / (1 - pA_post)
        if r["decided"] and r["decided"] <= end:
            wrows.append(((r["decided"] - r["received"]).days + add, 1, wt))
        else:
            wrows.append(((end - r["received"]).days + add, 0, wt))
    out["default path reweighted to the quarter's categories"] = weighted_km_quantile(wrows) / M
    w, _ = K.simulate(comp, cap=False)
    out["stage model, uncapped"] = float(np.quantile(w, 0.8)) / M
    w, _ = K.simulate(comp, cap=False, mix=Q["mix"])
    out["stage model, uncapped, the quarter's categories"] = float(np.quantile(w, 0.8)) / M
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
    for lo in (42, 56, 70, 84, 98):
        for lab, since in (("", None), (", filed since the rule", C.IFR)):
            sub = [((r["decided"] - r["received"]).days, 1) for r in dec if r["route"] == "appointment" and r["appt"]
                   and (r["appt"] - r["received"]).days >= lo and (since is None or r["received"] >= since)]
            out["decided renewals with an appointment %d days or more out%s" % (lo, lab)] = (
                float(np.quantile([s[0] for s in sub], 0.8)) / M if len(sub) >= 10 else float("nan"))
            out["_n_lead_%d%s" % (lo, "_post" if since else "")] = len(sub)
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


def _q(comp, **kw):
    return float(np.quantile(K.simulate(comp, **kw)[0], .8)) / M


def ask_a_mix(Q):
    """the category shares of ask A's own window (July to September 2027), a mix a solver may borrow for the quarter"""
    A = K.ask_a(Q["T"], Q["cases"], Q["ref"])
    tot = {cat: sum(A[(y, m, cat)] for (y, m) in C.ASK_A_MONTHS) for cat in C.CATS}
    return {cat: tot[cat] / sum(tot.values()) for cat in C.CATS}


def variants(Q):
    """the golden under every defensible construction the record supports (the family the margin rule reads)"""
    rens, mix = Q["rens"], Q["mix"]
    out = {}
    base = K.components(rens)
    out["golden (the quarter's category mix, Oct to Nov leads, Q by Kaplan-Meier, D and the response since the rule)"] = \
        _q(base, mix=mix)
    out["requests taken at the card's expiry (no offsets)"] = _q(base, mix=mix, offsets=False)
    out["the mix of ask A's window (July to September expiries)"] = _q(base, mix=ask_a_mix(Q))
    out["the record's own route share (no category mix)"] = _q(base)
    post = K.components([r for r in rens if r["received"] >= C.IFR])
    out["the route share of the renewals filed since the rule (no category mix)"] = _q(dict(base, pA=post["pA"]))
    out["leads from 14 September"] = _q(K.components(rens, regime=(dt.date(2026, 9, 14), dt.date(2026, 11, 30))), mix=mix)
    out["leads, November only"] = _q(K.components(rens, regime=(dt.date(2026, 11, 1), dt.date(2026, 11, 30))), mix=mix)
    out["leads, October only"] = _q(K.components(rens, regime=(dt.date(2026, 10, 1), dt.date(2026, 10, 31))), mix=mix)
    out["review from decided renewals only"] = _q(K.components(rens, q_mode="decided"), mix=mix)
    out["card gap from the whole record"] = _q(K.components(rens, d_from=C.RECORD_START), mix=mix)
    c2 = dict(base)
    c2["E"] = np.full(len(base["E"]), float(np.median(base["E"])))
    out["expedite response at its median"] = _q(c2, mix=mix)
    logL = np.log(base["L"])
    c3_lead = (lambda r, n, mu=logL.mean(), sd=logL.std(): np.exp(r.normal(mu, sd, n)))
    out["lead as a fitted lognormal"] = _q(base, mix=mix, lead_add=c3_lead)
    out["month of 365.25/12 days"] = _q(base, mix=mix) * M / (365.25 / 12)
    for s in (1, 2, 3):
        out["simulation seed %d" % s] = _q(base, mix=mix, seed=s)
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


def misreads(Q):
    """constructions that contradict a shipped record or the estimand; each still lands the bin, none is in the family"""
    base, mix, rens = Q["comp"], Q["mix"], Q["rens"]
    out = {"every expedite accepted (the log records denials)": _q(base, mix=mix, use_accept=False)}
    # the response read from USCIS's reply to the service request (outcome_date), not the decision notice (4.2)
    reply = np.array([(r["exp_reply"] - r["exp_req"]).days for r in rens if r["exp_req"] and r["received"] >= C.IFR
                      and r["exp_out"] == "Accepted" and r["exp_reply"]], float)
    out["the expedite response read from USCIS's reply date, not the decision notice"] = _q(dict(base, E=reply), mix=mix)
    # the quarter's mix keeping the (c)(9) cards of holders whose adjustment is approved (they will not renew)
    mix_all, _ = K.forward_mix(Q["T"], Q["cases"], Q["ref"], Q["d_median"], keep_approved=True)
    out["the quarter's mix keeping holders whose adjustment is approved"] = _q(base, mix=mix_all)
    return out


def one_sigma(Q):
    """each component of the golden construction moved by one standard error, the quote recomputed"""
    comp, mix = Q["comp"], Q["mix"]
    out = {}
    for name, key in (("lead", "L"), ("card gap", "D"), ("expedite response", "E"), ("request offset", "R")):
        arr = comp[key]
        se = float(arr.std() / np.sqrt(len(arr)))
        for sgn in (-1, 1):
            c = dict(comp)
            c[key] = arr + sgn * se
            out["%s %+d se" % (name, sgn)] = _q(c, mix=mix)
    for sgn in (-1, 1):
        c = dict(comp)
        c["pA_cat"] = {cat: comp["pA_cat"][cat] + sgn * float(np.sqrt(comp["pA_cat"][cat] * (1 - comp["pA_cat"][cat]) /
                                                                      comp["n_cat"][cat])) for cat in C.CATS}
        out["appointment share by category %+d se" % sgn] = _q(c, mix=mix)
        se_acc = float(np.sqrt(comp["accept"] * (1 - comp["accept"]) / max(1, len(comp["E"]))))
        out["expedite acceptance %+d se" % sgn] = _q(dict(comp, accept=comp["accept"] + sgn * se_acc), mix=mix)
        n9 = Q["n_mix"]["(c)(9)"] + Q["n_mix"]["(c)(26)"]
        f9 = mix["(c)(9)"] + sgn * float(np.sqrt(mix["(c)(9)"] * (1 - mix["(c)(9)"]) / n9))
        out["the quarter's (c)(9) share %+d se" % sgn] = _q(comp, mix={"(c)(9)": f9, "(c)(26)": 1 - f9})
    qs = np.array([q[0] for q in comp["qrows"] if q[1] == 1], float)
    se = float(qs.std() / np.sqrt(len(qs)))
    for sgn in (-1, 1):
        c = dict(comp)
        c["qrows"] = [(q[0] + sgn * se, q[1]) for q in comp["qrows"]]
        out["review %+d se" % sgn] = _q(c, mix=mix)
    return out


def margin(Q):
    """the margin rule: every construction in the family, moved by the largest one-sigma move of the golden, a
    quarter-bin clear of both edges of its half-month cell"""
    var = variants(Q)
    sig = one_sigma(Q)
    g = Q["months"]
    up = max(0.0, max(sig.values()) - g)
    dn = max(0.0, g - min(sig.values()))
    lo = min(var.values()) - dn
    hi = max(var.values()) + up
    cell = C.half_month(g)
    return dict(lo=lo, hi=hi, edge_lo=lo - (cell - 0.25), edge_hi=(cell + 0.25) - hi, var=var, sig=sig,
                ok=C.half_month(lo) == cell == C.half_month(hi) and lo - (cell - 0.25) >= 0.125 - 1e-9 and
                (cell + 0.25) - hi >= 0.125 - 1e-9)


if __name__ == "__main__":
    Q = K.quote(sys.argv[1])
    for k, v in routes(Q).items():
        print("%-75s %8.3f%s" % (k, v, "" if k.startswith("_") or np.isnan(v) else "  -> %.1f" % C.half_month(v)))
    print(backtest(Q))
    mg = margin(Q)
    for k, v in mg["var"].items():
        print("variant %-100s %.3f -> %.1f" % (k, v, C.half_month(v)))
    for k, v in misreads(Q).items():
        print("misread %-100s %.3f -> %.1f" % (k, v, C.half_month(v)))
    for k, v in mg["sig"].items():
        print("one sigma %-45s %.3f -> %.1f" % (k, v, C.half_month(v)))
    print("margin: family with one sigma %.3f to %.3f, edges %.3f and %.3f, %s" % (
        mg["lo"], mg["hi"], mg["edge_lo"], mg["edge_hi"], "PASS" if mg["ok"] else "FAIL"))
