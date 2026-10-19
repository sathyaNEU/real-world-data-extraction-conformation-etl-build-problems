"""The cracker and the mirror on the cut pack, scored against figures.json.

The cracker lands the call and runs the hygiene battery (record numbers unique in each file, exact duplicates, every
hospital ID and NPI found in the directory, every void and replacement naming a claim in the extract), executes every
filed handling (the revised release in place of the preliminary, Appendix A's codes in any procedure slot, a voided
claim and its void left out, a replaced claim giving way to the claim that names it, a stay's interim claims added
together) and takes each ask from the file that carries it: Ask A counts the revised release's resections at each
hospital, Ask B averages the members' stays' allowed amounts. The mirror stops off the call (the risk model on the
operation's own record) and takes the same reads on the asks: the asks consume nothing the call's construction
produces, so the two rows agree by construction (the separation is asserted in checks.py).

Weights are the skill's: 38 for the call and its components, 7 for instruction-following, 55 for the asks, a figure a
hit at its stated rounding (Ask A whole operations, Ask B whole dollars)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A    # noqa: E402
import common as K      # noqa: E402
import pack as PK       # noqa: E402
from deliver import dollars   # noqa: E402


def battery(P):
    """The hygiene battery on the ask files: what it finds is a work order, and on this pack it finds nothing."""
    out = {}
    for k in ("prelim", "revised"):
        ids = [r["rec_id"] for r in P[k]]
        out[k + " record numbers unique"] = len(ids) == len(set(ids))
        rows = [tuple(sorted((kk, str(v)) for kk, v in r.items() if kk != "rec_id")) for r in P[k]]
        out[k + " exact duplicates (all but the record number)"] = len(rows) - len(set(rows))
        out[k + " hospital IDs unmatched"] = sum(1 for r in P[k] if r["hosp"] is None)
    cl = P["claims"]
    out["claim ids unique"] = cl.claim_id.is_unique
    out["claims exact duplicates (all but the claim id)"] = int(cl.drop(columns=["claim_id"]).duplicated().sum())
    out["claims NPIs unmatched"] = int(cl.hosp.isna().sum())
    refs = set(cl.original_claim_id[cl.original_claim_id != ""])
    out["claims naming a claim not in the extract"] = len(refs - set(cl.claim_id))
    return out


def ask_a(P):
    cnt = {h: 0 for h in K.ELIGIBLE}
    for rec in P["revised"]:
        if rec["hosp"] in cnt and A._res_date(rec) is not None and K.H1_2026[0] <= rec["discharge"] <= K.H1_2026[1]:
            cnt[rec["hosp"]] += 1
    return cnt


def ask_b(P):
    cl = P["claims"]
    voided = set(cl.original_claim_id[cl.bill_type == "0118"])
    replaced = set(cl.original_claim_id[cl.bill_type == "0117"])
    keep = cl[(cl.bill_type != "0118") & ~cl.claim_id.isin(voided) & ~cl.claim_id.isin(replaced)]
    stays = keep.groupby(["hosp", "member_id", "admit_date"]).allowed.sum().reset_index()
    return {h: dollars(stays[stays.hosp == h].allowed.mean()) for h in K.ELIGIBLE}


def score(fig, a, b):
    rows, hits = [], 0
    for h in K.ELIGIBLE:
        n = K.NAME[h]
        x = [a[h] == fig["ask_a"][n], b[h] == fig["ask_b"][n]]
        hits += sum(x)
        rows.append((n, a[h], fig["ask_a"][n], b[h], fig["ask_b"][n], "".join("x" if v else "." for v in x)))
    return hits, rows


def run(task, quiet=False):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    P = PK.load(os.path.join(task, "target"))
    bat = battery(P)
    total = 2 * len(K.ELIGIBLE)
    ca, rows = score(fig, ask_a(P), ask_b(P))
    ma = ca      # the mirror takes the same reads on the asks
    cracker = 38 + 7 + 55.0 * ca / total
    mirror = 5 + 7 + 55.0 * ma / total
    pair = (cracker + mirror) / 2
    if not quiet:
        print("battery:", bat)
        print("cracker (hospital, A got/golden, B got/golden, hits)")
        for r in rows:
            print("   %-36s A %3d/%3d  B %6d/%6d  %s" % r)
        print("cracker keeps %d of %d ask figures; the mirror, on the same reads, %d of %d" % (ca, total, ma, total))
        print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of the ask weight"
              % (cracker, mirror, pair, 100.0 * ma / total))
    return dict(cracker_hits=ca, mirror_hits=ma, total=total, pair=pair, cracker=cracker, mirror=mirror, battery=bat)


if __name__ == "__main__":
    r = run(os.path.dirname(HERE))
    sys.exit(0 if r["cracker_hits"] == 0 else 1)
