"""task172 cracker and mirror sheets, run on the cut pack (target/).

The cracker is the stage 4 reader's measured path, not a guess at it: it landed the call, ran the hygiene battery,
executed GM-07 1.3, 1.4, 2.3 and 2.4, linked every spouse through every record that carries the link and took a
spouse's two household IDs as one person (round 3's settled cell), took each person's card approved most recently
from HR's roster, counsel's approval notices and the register's approvals, counted counsel's rejection notices with the
ones applicants forwarded (one per case and notice date) and looked for each case's next receipt. Each ask figure is
scored a hit only when it equals the golden (whole numbers); the pair ceiling is the cracker with any one more device
found, at the build's rubric weights. The mirror stops at the most attractive wrong rung of the call and works the
asks the natural way."""
from __future__ import annotations

import datetime as dt
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K     # noqa: E402
import common as C   # noqa: E402

W_CALL, W_COMP, W_IF, W_ASK = 25.0, 12.0, 7.0, 56.0     # per cent of the rubric
N_ASK = 6 + 6 + 8                                          # ask A cells, the chart's labelled bars, ask B cells
ALL = ("roster", "register", "counsel", "tracker")
CAREFUL_A = dict(sources=("roster", "counsel", "register"), dual=False, moves=False)
CAREFUL_B = dict(by_renewal=False, scope=False)


def ask_a_by(T, cases, ref, **kw):
    """ask A executed on the pack with one handling changed (calc.persons' options)"""
    return K.ask_a(T, cases, ref, **kw)


def ask_b_by(T, cases, ref, **kw):
    """ask B executed on the pack with one handling changed (calc.ask_b's options)"""
    return K.ask_b(T, cases, ref, **kw)


def ask_b_dispatch(T, cases, ref):
    """the mailroom's returned renewal packets, dated by counsel's notice where one matches, refiled when the person's
    next packet left within 30 days"""
    notice_by_case = defaultdict(list)
    for n in T["notices"]:
        if n["notice_type"] == "Rejection notice":
            notice_by_case[ref.get(n["client_ref"])].append(K._d(n["notice_date"]))
    sends = defaultdict(list)
    for r in T["dispatch"]:
        if "renewal" in r["contents"]:
            sends[r["person_id"]].append(K._d(r["sent_on"]))
    out = {lab: [0, 0] for lab, _, _ in C.ASK_B_QUARTERS}
    for r in T["dispatch"]:
        if "renewal" not in r["contents"] or r["status"] != "Returned":
            continue
        ret = K._d(r["returned_on"])
        k = ref.get(r["case_id"])
        cand = [d for d in notice_by_case.get(k, []) if d <= ret]
        nd = max(cand) if cand else ret
        for lab, a, b in C.ASK_B_QUARTERS:
            if a <= nd <= b:
                out[lab][0] += 1
                later = sorted(d for d in sends[r["person_id"]] if d > K._d(r["sent_on"]))
                out[lab][1] += bool(later and (later[0] - nd).days <= C.REFILE_DAYS)
    return {k: tuple(v) for k, v in out.items()}


def score(truth_a, truth_b, got_a, got_b):
    """hits on the ask cells and the chart's labelled bars (the chart carries ask A's figures)"""
    ha = sum(1 for k in truth_a if got_a.get(k) == truth_a[k])
    hb = sum(1 for k in truth_b for j in (0, 1) if got_b.get(k, (None, None))[j] == truth_b[k][j])
    return dict(ask_a=ha, chart=ha, ask_b=hb, total=2 * ha + hb)


def sheets(target):
    Q = K.quote(target)
    T, cases, ref = Q["T"], Q["cases"], Q["ref"]
    A = K.ask_a(T, cases, ref)
    B = K.ask_b(T, cases, ref)
    a_care = ask_a_by(T, cases, ref, **CAREFUL_A)
    b_care = ask_b_by(T, cases, ref, **CAREFUL_B)
    rows = {}
    rows["cracker"] = (score(A, B, a_care, b_care),
                       "the reader's path: the roster with counsel's and the register's approvals, every spouse link, a "
                       "spouse's two household IDs one person; counsel's and the forwarded rejections, receipts by case")
    one = (("cracker, the tracker's approvals found", dict(CAREFUL_A, sources=ALL), None),
           ("cracker, one card under two IDs found", dict(CAREFUL_A, dual=True), None),
           ("cracker, an employee's two IDs found", dict(CAREFUL_A, moves=True), None),
           ("cracker, the applicant's own filing found", None, dict(CAREFUL_B, by_renewal=True)),
           ("cracker, the other filings' rejections found", None, dict(CAREFUL_B, scope=True)))
    for name, ka, kb in one:
        rows[name] = (score(A, B, ask_a_by(T, cases, ref, **ka) if ka else a_care,
                            ask_b_by(T, cases, ref, **kb) if kb else b_care), name.split(", ", 1)[1])
    rows["mirror"] = (score(A, B, ask_a_by(T, cases, ref, sources=("roster",), links="benefits", merge=False,
                                            dual=False, moves=False), ask_b_dispatch(T, cases, ref)),
                      "the roster's cards and categories, spouses linked through Benefits; the mailroom's returned packets")
    rows["mirror, counsel's notices"] = (
        score(A, B, ask_a_by(T, cases, ref, sources=("roster", "counsel"), links="benefits", merge=False, dual=False,
                             moves=False), ask_b_by(T, cases, ref, forwarded=False, **CAREFUL_B)),
        "the roster with counsel's approvals, spouses linked through Benefits; counsel's rejection notices")
    base = rows["cracker"][0]["total"]
    cr_rows = tuple(name for name, _, _ in one)
    cr = max(rows[k][0]["total"] for k in cr_rows)
    mi = max(rows["mirror"][0]["total"], rows["mirror, counsel's notices"][0]["total"])
    lc = cr / N_ASK
    ls = mi / N_ASK
    on_call = W_CALL + W_COMP + W_IF + W_ASK * lc
    off_call = 4.0 + W_IF + W_ASK * ls          # the mirror keeps the lead, a component the easy route also reads
    both = W_CALL + W_COMP + W_IF + W_ASK * base / N_ASK
    return dict(rows=rows, lc=lc, ls=ls, pair=(on_call + off_call) / 2, both_on_call=both, mirror_leak=ls * 100,
                base=base, truth_a=A, truth_b=B,
                pair_by_row={k: (W_CALL + W_COMP + W_IF + W_ASK * rows[k][0]["total"] / N_ASK + off_call) / 2
                             for k in cr_rows})


if __name__ == "__main__":
    S = sheets(sys.argv[1])
    for k, (sc, how) in S["rows"].items():
        print("%-55s ask A %d/6  chart %d/6  ask B %d/8  (%s)" % (k, sc["ask_a"], sc["chart"], sc["ask_b"], how))
    print("cracker keeps %d of %d ask cells; with one device cracked at most %.1f%% of ask weight; mirror %.1f%%; "
          "pair ceiling %.1f (%s); both top responses on the call with no device cracked %.1f" % (
              S["base"], N_ASK, S["lc"] * 100, S["ls"] * 100, S["pair"],
              ", ".join("%s %.1f" % (k.replace("cracker, ", ""), v) for k, v in S["pair_by_row"].items()),
              S["both_on_call"]))
