"""figures.json: every figure the write-up and the goldens state, computed once from the shipped bundle."""
import numpy as np

import params as P
import solve as S


def r(x, u):
    return int(round(x / float(u)) * u)


def compute(target):
    D, est, add, oos = S.golden(target)
    order = sorted(S.CATS, key=lambda c: -add[c])
    win = order[0]
    k = D["cat"] == win
    whole = int((D["O"][:, k, S.BASE:].all(axis=1)).sum())
    A = S.ask_trial(target)
    Bst = S.ask_stops(target)
    C = S.ask_pallets(target)
    st = D["st"]
    F = {
        "call_category": win,
        "call_add": r(add[win], 10000),
        "add_nzd": {c: int(round(add[c])) for c in S.CATS},
        "oos_line_days": oos,
        "win_lines": int(k.sum()),
        "win_whole_shelf_store_days": whole,
        "cut_pct": int(round(100 * P.CUT)),
        "ask_trial": {str(s): {"after": int(A[s]["after"]), "change_pct": round(-A[s]["down_pct"], 1)} for s in A},
        "ask_late_stops": {g: int(sum(int(Bst.get(s, 0)) for s in st.store_no[st.island == g]))
                           for g in st.island.drop_duplicates()},
        "ask_pallets": {c: {m: int(C.loc[c, m]) for m in S.MONTHS} for c in S.DC_CATS},
        "store_names": {str(int(a)): b for a, b in zip(st.store_no, st.store_name)},
    }
    X = dict(D=D, est=est, add=add, order=order, A=A, B=Bst, C=C)
    return F, X
