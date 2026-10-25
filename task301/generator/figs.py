"""figures.json: every figure the write-up and the goldens state, computed once from the shipped bundle."""
import numpy as np
import pandas as pd

import params as P
import solve as S


def r(x, u):
    return int(round(x / float(u)) * u)


def compute(target):
    gold, cv, h, pr, L, log, ext = S.golden(target)
    order = sorted(S.CANDS, key=lambda g: -gold[g]["quits"])
    win = order[0]
    W = gold[win]
    old5 = {g: int(((pd.Timestamp(P.EXTRACT) - pd.to_datetime(L[L.sub_region == g].smoking_status_date)).dt.days
                    > 5 * 365.25).sum()) for g in S.CANDS}
    A = S.ask_referrals(target)
    B = S.ask_evening(target)
    C = S.ask_talk(target)
    calls, handed = S.dialler_calls(target)
    F = {
        "call_region": win,
        "call_quits": r(W["quits"], P.CALL_ROUND),
        "listed": {g: int(gold[g]["listed"]) for g in S.CANDS},
        "listed_over5y": old5,
        "quit_rate_pct": {g: int(round(100 * gold[g]["quit_rate"])) for g in S.CANDS},
        "relapse_pct": round(100 * float(np.mean([gold[g]["relapse"] for g in S.CANDS])), 1),
        "call_still_pct": r(100 * W["still"] / W["listed"], 5),
        "quits_per100_still": int(round(100 * cv["k"])),
        "pilot": {"listed": cv["listed"], "reached": cv["reached"], "stopped": cv["stopped"],
                  "smokers_reached": cv["reached"] - cv["stopped"], "quit_dates": cv["quit_dates"], "quits": cv["quits"]},
        "pilot_reach_pct": round(100 * cv["reach"], 1),
        "pilot_quit_per_smoker_reached_pct": round(100 * cv["per_smoker_reached"], 1),
        "ask_referrals": {g: {q: int(A.loc[g, q]) for q in A.columns} for g in S.CANDS},
        "ask_evening": {d: {"calls": int(B.loc[d, "calls"]), "reached": int(B.loc[d, "reached"])} for d in S.WEEKDAYS},
        "ask_talk_min": {m: round(float(v), 1) for m, v in C.items()},
        "handed_over_legs": int(handed),
        "dialler_legs": int(len(calls) + handed),
    }
    X = dict(gold=gold, cv=cv, order=order, A=A, B=B, C=C)
    return F, X
