"""task172 cracker and mirror sheets, run on the cut pack (target/).

The cracker landed the call, ran the hygiene battery (key uniqueness, exact duplicates, unmatched joins, fan-out),
executed every filed sentence and pin, and links a spouse to her sponsoring employee through every record that carries
the link (it is credited with the most obvious device on each ask). The mirror stops at the most attractive wrong rung
of the call and works the asks the natural way. Each ask figure is scored a hit within half a unit of its rounding;
the pair ceiling is the strongest response with any one more device cracked, at the build's rubric weights."""
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


def ask_a_by(T, cases, ref, **kw):
    """ask A executed on the pack with one handling changed (calc.latest_cards' options): sources, links, merge"""
    return K.ask_a(T, cases, ref, **kw)


def ask_b_counsel(T, cases, ref, with_forwarded=False, with_register=False):
    """counsel's rejection notices by notice date; refiled when the case's next receipt notice falls within 30 days"""
    rej = {}
    for n in T["notices"]:
        if n["notice_type"] == "Rejection notice":
            rej[(ref.get(n["client_ref"]), K._d(n["notice_date"]))] = 1
    if with_forwarded:
        for a in T["actions"]:
            if a["action"] == "Notice forwarded by applicant" and a["detail"] == "Rejection notice":
                rej.setdefault((ref.get(a["case_id"]), K._d(a["notice_date"])), 1)
    rec = defaultdict(list)
    for n in T["notices"]:
        if n["notice_type"] == "Receipt notice":
            rec[ref.get(n["client_ref"])].append(K._d(n["received_date"]))
    if with_register:
        for c in cases.values():
            if c["received"]:
                rec[c["id"]].append(c["received"])
    out = {}
    for label, a, b in C.ASK_B_QUARTERS:
        nr = nf = 0
        for (k, nd) in rej:
            if a <= nd <= b:
                nr += 1
                later = sorted(x for x in rec.get(k, []) if x > nd)
                nf += bool(later and (later[0] - nd).days <= C.REFILE_DAYS)
        out[label] = (nr, nf)
    return out


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
    # the cracker executes GM-07 1.3, 1.4, 2.3 and 2.4 and runs the battery on the joins they make: 1.4's category
    # sends it from HR's roster to counsel's approval notices, so it adds the approvals the roster lacks and takes each
    # approval's category; it links every spouse through every record (credited); it keys persons by the ID each
    # record carries. Its two ask A devices: cards only the register's filings and the tracker hold (A1), and a
    # spouse's two IDs (A6)
    crack_a = dict(sources=("roster", "counsel"), merge=False)
    rows = {}
    rows["cracker"] = (score(A, B, ask_a_by(T, cases, ref, **crack_a), ask_b_counsel(T, cases, ref)),
                       "the roster with counsel's approvals and their categories, every spouse link, persons by ID; "
                       "counsel's rejection and receipt notices")
    rows["cracker, most obvious device cracked"] = (
        score(A, B, ask_a_by(T, cases, ref, **crack_a), ask_b_counsel(T, cases, ref, True, False)),
        "as the cracker, with the rejection notices applicants forwarded")
    rows["cracker, the other device cracked"] = (
        score(A, B, ask_a_by(T, cases, ref, **crack_a), ask_b_counsel(T, cases, ref, False, True)),
        "as the cracker, with every receipt the register holds")
    rows["cracker, ask A's roster gap cracked"] = (
        score(A, B, ask_a_by(T, cases, ref, merge=False), ask_b_counsel(T, cases, ref)),
        "as the cracker, with the register's filings and the tracker's cards")
    rows["cracker, ask A's two IDs cracked"] = (
        score(A, B, ask_a_by(T, cases, ref, sources=("roster", "counsel")), ask_b_counsel(T, cases, ref)),
        "as the cracker, a spouse's two IDs taken as one person")
    rows["mirror"] = (score(A, B, ask_a_by(T, cases, ref, sources=("roster",), links="benefits", merge=False),
                            ask_b_dispatch(T, cases, ref)),
                      "the roster's cards and categories, spouses linked through Benefits; the mailroom's returned packets")
    rows["mirror, counsel's notices"] = (
        score(A, B, ask_a_by(T, cases, ref, sources=("roster", "counsel"), links="benefits", merge=False),
              ask_b_counsel(T, cases, ref)),
        "the roster with counsel's approvals, spouses linked through Benefits; counsel's rejection notices")
    base = rows["cracker"][0]["total"]
    cr_rows = ("cracker, most obvious device cracked", "cracker, the other device cracked",
               "cracker, ask A's roster gap cracked", "cracker, ask A's two IDs cracked")
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
