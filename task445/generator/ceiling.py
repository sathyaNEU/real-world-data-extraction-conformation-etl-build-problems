"""task445 architecture 3: the ask layer's pair ceiling on the cut pack (supplemental-stumping Parts 0 and 1.1).

The cracker lands the call and executes every filed rule (code 2.1 to 2.3, 3.1, 6.1 to 6.3): it maps the merged
centres through the register, sets the absent candidates aside, lets the senior re-mark stand, counts every essay a
candidate wrote, places each review in its centre's local month and drops withdrawn requests. The mirror stops at the
chooser comparison (no scaling) and reads the asks off the files as they stand: a centre's region from its code's
letters, every row a marking, every review in its UTC month. Each figure is scored against the golden.

    python3 task445/generator/ceiling.py
"""
import hashlib
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import golden as G  # noqa: E402


def mirror_entries(D):
    sat = Counter()
    ans = {q: Counter() for q in G.QS}
    for r in D["marks"]:
        reg = r["centre_code"][:2]
        if r["question"]:
            ans[r["question"][1:]][reg] += 1
    seen = set()
    for r in D["marks"]:
        if r["candidate_no"] not in seen:
            seen.add(r["candidate_no"])
            sat[r["centre_code"][:2]] += 1
    return {g: dict(sat=sat[g], **{"q" + q: ans[q][g] for q in G.QS}) for g in G.REGIONS}


def mirror_reviews(D):
    rows = G._read(D["target"], "post_results_reviews_2025.csv")
    out = {"%d-%02d" % m: {g: dict(requests=0, grade_changes=0) for g in G.REGIONS} for m in G.MONTHS}
    for r in rows:
        if r["component"] != "P2":
            continue
        m = r["requested_utc"][:7]
        g = r["centre_code"][:2]
        if m in out and g in out[m]:
            out[m][g]["requests"] += 1
            out[m][g]["grade_changes"] += r["outcome"] == "GC"
    return out


def kept(gold, other):
    k = n = 0
    for a in gold:
        for b in gold[a]:
            n += 1
            k += gold[a][b] == other.get(a, {}).get(b)
    return k, n


def main():
    S = G.solve(T)
    D = S["D"]
    ka, na = kept(S["entries"], mirror_entries(D))
    kb, nb = kept(S["reviews"], mirror_reviews(D))
    n = na + nb
    crack = n
    mirror = ka + kb
    c = 38 + 7 + 55.0 * crack / n
    s = 5 + 7 + 55.0 * mirror / n
    zp = os.path.join(TASK, "target.zip")
    print("measured on target.zip %s" % hashlib.sha256(open(zp, "rb").read()).hexdigest()[:8])
    print("ask A: mirror keeps %d of %d; ask B: mirror keeps %d of %d" % (ka, na, kb, nb))
    print("cracker keeps %d of %d ask figures, scores %.1f with the call" % (crack, n, c))
    print("mirror keeps %d of %d, scores %.1f off it" % (mirror, n, s))
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * mirror / n))


if __name__ == "__main__":
    main()
