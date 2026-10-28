"""task464 architecture 8: the generating process.

Each withdrawal has a reason the learner actually had, and a category a coder placed their comment in. The two
differ at a rate that depends on the category, because some reasons are described obliquely.

The moderation sample is drawn as a fixed number PER CODED CATEGORY, so what it measures is
P(true category | coded category), and the corrected composition is the coded composition reweighted by it:

    p[j] = sum over coded i of q[i] * R[j|i]

That is one formula with no free parameter. The moderation sample's own composition is NOT an estimate of the
service's composition, because the stratification over-represents whichever categories are coded rarely.
"""
import numpy as np
import world as W

# Clause pools. A comment carries the clause of the reason the learner had, and where the coder read it as
# something else it also carries the clause that supports that reading, because that is why they read it so.
TRUE_CLAUSE = {
    "CR": ["my mum came out of hospital and i look after her now",
           "no one else can collect the little ones from school",
           "my daughter's childminder gave up at half term",
           "im caring for my husband since his fall",
           "had to take over looking after my grandson"],
    "WH": ["my shifts changed to lates so i cant make the class",
           "the depot put me on a 2 till 10 rota",
           "work moved me to saturdays",
           "i got more hours at the shop and they clash",
           "my manager wont swap the tuesday shift"],
    "TR": ["the 47 bus stopped running that early",
           "it was two buses each way and i couldnt keep paying it",
           "roadworks on the bypass made me late every week",
           "my lift fell through when my neighbour moved",
           "parking at the centre was impossible after six"],
    "CD": ["the maths was way above what i did at school",
           "i couldnt keep up with the pace of the units",
           "the assignments were harder than i expected",
           "felt lost after the first few weeks",
           "the level was wrong for me, should have done entry 3"],
    "HL": ["ive been signed off with my back",
           "my anxiety got worse and i couldnt come in",
           "waiting on an operation in march",
           "chest infection and then it just dragged on",
           "my medication changed and im not right yet"],
    "OT": ["just wasnt for me in the end",
           "changed my mind about the course",
           "didnt get on with it",
           "sorted something else out instead",
           "no particular reason really"],
}
# The clause that makes a comment readable as the coded category when the coder read it that way.
BRIDGE = {
    "CR": ["and i cant get cover in the evenings", "so the evenings are not possible for me now"],
    "WH": ["so the tuesday evening slot doesnt work with my hours",
           "and the timing just clashes now", "the hours dont fit any more"],
    "TR": ["and getting across town after that is hard", "so getting there got difficult"],
    "CD": ["and i was falling behind on the work", "i wasnt keeping up either"],
    "HL": ["and im not been well with it", "it took it out of me health wise"],
    "OT": ["", "it just stopped working out"],
}


def simulate(seed=None):
    seed = W.SEED if seed is None else seed
    rng = np.random.default_rng(seed)
    codes = W.CODES
    true_p = np.array([W.TRUE_SHARE[c] for c in codes])
    rows = []
    wid = 0
    for t in W.TERMS:
        n = W.withdrawals_for(t["code"])
        for _ in range(n):
            wid += 1
            tr = codes[int(rng.choice(len(codes), p=true_p))]
            col = np.array([W.CODED_GIVEN_TRUE[i][tr] for i in codes])
            cd = codes[int(rng.choice(len(codes), p=col / col.sum()))]
            txt = TRUE_CLAUSE[tr][int(rng.integers(0, len(TRUE_CLAUSE[tr])))]
            if cd != tr:
                br = BRIDGE[cd][int(rng.integers(0, len(BRIDGE[cd])))]
                txt = (txt + " " + br).strip()
            rows.append({"wid": wid, "term": t["code"], "true": tr, "coded": cd, "comment": txt})
    # the moderation sample: a fixed number PER CODED CATEGORY, spread across the terms
    mod = []
    for i in codes:
        pool = [r for r in rows if r["coded"] == i]
        take = min(W.MODERATED_PER_CODE, len(pool))
        pick = rng.choice(len(pool), size=take, replace=False)
        for j in pick:
            mod.append(pool[int(j)])
    modset = {r["wid"] for r in mod}
    for r in rows:
        r["moderated"] = r["wid"] in modset
    return {"seed": seed, "rows": rows, "codes": codes}


def composition(rows, key):
    codes = W.CODES
    n = len(rows)
    return {c: sum(1 for r in rows if r[key] == c) / n for c in codes}


def reverse_matrix(rows):
    """R[j][i] = P(true j | coded i), from the moderation sample alone."""
    codes = W.CODES
    R = {j: {} for j in codes}
    for i in codes:
        sub = [r for r in rows if r["moderated"] and r["coded"] == i]
        m = len(sub)
        for j in codes:
            R[j][i] = (sum(1 for r in sub if r["true"] == j) / m) if m else 0.0
    return R


def corrected(rows):
    q = composition(rows, "coded")
    R = reverse_matrix(rows)
    return {j: sum(q[i] * R[j][i] for i in W.CODES) for j in W.CODES}, q, R


def ladder(rows):
    codes = W.CODES
    q = composition(rows, "coded")
    p, _, R = corrected(rows)
    # rung 1: drop the catch-all and renormalise, a common tidy-up
    s = sum(q[c] for c in codes if c != "OT")
    r1 = {c: (q[c] / s if c != "OT" else 0.0) for c in codes}
    # rung 2: the moderation sample's own composition, ignoring that it is stratified by coded category
    mod = [r for r in rows if r["moderated"]]
    r2 = {c: sum(1 for r in mod if r["true"] == c) / len(mod) for c in codes}
    return {"rung0_raw_coded": q, "rung1_drop_other": r1, "rung2_moderated_raw": r2, "golden_corrected": p,
            "reverse_matrix": R}


if __name__ == "__main__":
    s = simulate()
    lad = ladder(s["rows"])
    print("seed", s["seed"], " withdrawals", len(s["rows"]),
          " moderated", sum(1 for r in s["rows"] if r["moderated"]))
    print()
    print("%-26s %9s %9s %9s %9s" % ("reason", "rung0", "rung1", "rung2", "GOLDEN"))
    for c in W.CODES:
        print("%-26s %8.2f%% %8.2f%% %8.2f%% %8.2f%%" % (
            W.LABEL[c], 100 * lad["rung0_raw_coded"][c], 100 * lad["rung1_drop_other"][c],
            100 * lad["rung2_moderated_raw"][c], 100 * lad["golden_corrected"][c]))
    print()
    for k in ("rung0_raw_coded", "rung1_drop_other", "rung2_moderated_raw", "golden_corrected"):
        r = sorted(W.CODES, key=lambda c: -lad[k][c])
        print("%-22s names %-26s margin %.3fx" % (
            k, W.LABEL[r[0]], lad[k][r[0]] / lad[k][r[1]]))
    g = sorted(W.CODES, key=lambda c: -lad["golden_corrected"][c])
    print()
    print("recall of each category (P(coded as itself | true)) from the moderation sample:")
    for c in W.CODES:
        print("   %-26s %.3f" % (W.LABEL[c], lad["reverse_matrix"][c][c]))
