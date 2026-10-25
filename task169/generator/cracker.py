"""task169 cracker: the pair ceiling and the mirror leakage measured on the cut pack, on Part 0's weights (the
recommendation and its components 38, instructions 7, the asks 55 shared over the 26 ask figures).

The cracker is portal round 4's responses, which reproduced all three tables of the round 3 pack, executed on this
pack along the round 3 golden's own path: every convention the asking sentences state (one recommitment per parolee
per hearing date, not rescinded by 30 June 2026, the first day counted and the last not, halves by the day, county
jails to districts by the methodology's Table 1, a writ trip ended at the WRI or the release), the legacy entries
dated after the legacy system's close dropped as the parallel run's, every order on a case with a RESCIND row out,
one detainer per case with a carried-over case taken from the new system, a legacy detainer with no lift date ended
at the next admission, each parolee's overlapping detainers merged. The mirror stopped on the record's
new-commitment rate and trusted each file as written: both systems added, rescissions kept, detainers without a lift
date left out, unpaired writs dropped.

    python3 task169/generator/cracker.py [target]"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import calc          # noqa: E402
import pandas as pd  # noqa: E402

W_CALL, W_INSTR, W_ASK, R_WRONG = 38.0, 7.0, 55.0, 5.0


def figures(D, a_kw, b_kw, c_kw):
    A = calc.ask_a(D, **a_kw)
    B = calc.ask_b(D, **b_kw)
    W = calc.ask_c(D, **c_kw)
    out = {}
    for o in calc.OFFICES:
        for k in ("arrest", "conditions"):
            out["a1_%s.%s" % (o, k)] = A[o][k]
    for d in C.DISTRICTS:
        for q in B[d]:
            out["b_%s.%s" % (d, q)] = B[d][q]
    for i in calc.INSTITUTIONS:
        for h in W[i]:
            out["c_%s.%s" % (i, h)] = W[i][h]
    return out


def reader_a_table(D):
    """reader A, Table 1 literally: both systems, deduplicated on DOC number, report date and arrest number, minus
    any case rescinded at any date"""
    leg, new = calc._board(D)
    FY = calc.FY
    L = leg[(leg.action == "REVOKE") & (leg.ad >= FY[0]) & (leg.ad <= FY[1])]
    L = L[~L.case_no.isin(set(leg[leg.action == "RESCIND"].case_no))]
    N = new[(new.decision == "REVOKED") & (new.dd >= FY[0]) & (new.dd <= FY[1])]
    N = N[N.rescinded_date.fillna("") == ""]
    out = pd.concat([pd.DataFrame({"doc": L.doc_number, "rep": L.rep, "otn": L.arrest_otn, "office": L.office}),
                     pd.DataFrame({"doc": N.doc_number, "rep": N.rep, "otn": N.arrest_otn, "office": N.office})])
    out = out.drop_duplicates(["doc", "rep", "otn"])
    return {o: {"arrest": int(((out.office == o) & (out.otn != "")).sum()),
                "conditions": int(((out.office == o) & (out.otn == "")).sum())} for o in calc.OFFICES}


def reader_b_table(D):
    """reader B, Table 1 literally: legacy REVOKE rows from 1 July 2025 to the close, cases carried into the new system
    and cases with a RESCIND row left out, plus the new system's REVOKED rows to 30 June 2026 with no rescinded date"""
    leg, new = calc._board(D)
    FY = calc.FY
    close = pd.Timestamp(C.BOARD_MIGRATE_CUT)
    L = leg[(leg.action == "REVOKE") & (leg.ad >= FY[0]) & (leg.ad <= close)]
    moved = set(new[new.opened_in == "LEGACY"].doc_number + "|" + new[new.opened_in == "LEGACY"].report_date)
    L = L[~(L.doc_number + "|" + L.rep.dt.strftime("%Y-%m-%d")).isin(moved)]
    L = L[~L.case_no.isin(set(leg[leg.action == "RESCIND"].case_no))]
    N = new[(new.decision == "REVOKED") & (new.dd >= FY[0]) & (new.dd <= FY[1])]
    N = N[N.rescinded_date.fillna("") == ""]
    out = pd.concat([pd.DataFrame({"otn": L.arrest_otn, "office": L.office}),
                     pd.DataFrame({"otn": N.arrest_otn, "office": N.office})])
    return {o: {"arrest": int(((out.office == o) & (out.otn != "")).sum()),
                "conditions": int(((out.office == o) & (out.otn == "")).sum())} for o in calc.OFFICES}


def flat(A=None, B=None, W=None):
    out = {}
    for o in (A or {}):
        for k in ("arrest", "conditions"):
            out["a1_%s.%s" % (o, k)] = A[o][k]
    for d in (B or {}):
        for q in B[d]:
            out["b_%s.%s" % (d, q)] = B[d][q]
    for i in (W or {}):
        for h in W[i]:
            out["c_%s.%s" % (i, h)] = W[i][h]
    return out


def kept(golden, resp):
    return sum(1 for k, v in golden.items() if resp.get(k) == v)


def main(target):
    D = calc.load(target)
    gold = figures(D, {}, {}, {})
    n = len(gold)
    # the cracker is the round 3 golden's path, which portal round 4's two responses reproduced cell for cell
    crack_a = dict(level="case", parallel="date")
    crack_b = dict(carry="new")
    crack_c = dict()
    cr = figures(D, crack_a, crack_b, crack_c)
    mi = figures(D, dict(orders=False, dedupe=False, rescind=False), dict(union=False, dedupe=False, blank="drop"),
                 dict(ended_by_release=False))
    kc, km = kept(gold, cr), kept(gold, mi)
    C_ = W_CALL + W_INSTR + W_ASK * kc / n
    S_ = R_WRONG + W_INSTR + W_ASK * km / n
    print("ask figures %d" % n)
    print("cracker (call landed): keeps %d of %d ask figures, scores %.1f" % (kc, n, C_))
    print("mirror (call missed):  keeps %d of %d ask figures, scores %.1f" % (km, n, S_))
    print("pair ceiling %.1f   mirror leakage %.1f per cent of ask weight" % ((C_ + S_) / 2, 100 * km / n))
    Bq, Wq = calc.ask_b(D, **crack_b), calc.ask_c(D, **crack_c)
    for name, tab in (("stage 4 reader A's quoted path", reader_a_table(D)), ("stage 4 reader B's quoted path", reader_b_table(D))):
        k = kept(gold, flat(tab, Bq, Wq))
        c1 = W_CALL + W_INSTR + W_ASK * k / n
        print("%s: keeps %d of %d ask figures (Table 1 %d of 8), scores %.1f, pair %.1f"
              % (name, k, n, kept(gold, flat(tab)), c1, (c1 + S_) / 2))
    print("\none crack at a time (the cracker repairs one device and keeps its other stops):")
    singles = (("A: a rescission sets aside the order before it", dict(crack_a, level="event"), crack_b, crack_c),
               ("B: a carried-over detainer from its legacy lodge", crack_a, dict(carry="legacy"), crack_c))
    for name, ak, bk, ck in singles:
        k = kept(gold, figures(D, ak, bk, ck))
        c1 = W_CALL + W_INSTR + W_ASK * k / n
        print("  %-48s keeps %2d of %d, cracker %.1f, pair %.1f" % (name, k, n, c1, (c1 + S_) / 2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
