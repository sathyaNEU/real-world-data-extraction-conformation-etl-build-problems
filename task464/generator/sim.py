"""task464 architecture 8: the generating process.

Each withdrawal has a reason the learner actually had, and a category a coder placed their comment in. The two
differ at a rate that depends on the category, because some reasons are described obliquely.

The moderation sample is drawn by CODED category (every OT, a fixed number of each other code), so what it
measures is P(true category | coded category), and the corrected composition is the coded composition
reweighted by it:

    p[j] = sum over coded i of q[i] * R[j|i]

That is one formula with no free parameter. The moderation sample's own composition is NOT an estimate of the
service's composition, because every OT is in it and only a fixed number of each other code, so it is
dominated by the comments coded OT.
"""
import numpy as np
import world as W

# Clause pools. A comment carries the clause of the reason the learner had, and where the coder read it as
# something else it also carries the clause that supports that reading, because that is why they read it so.
# Slots in braces are filled per comment, so the year's comments are as varied as people's own words.
FILL = {
    "kin": ["mum", "dad", "my gran", "my mother", "my dad", "my husband", "my wife", "my partner", "my son",
            "my daughter", "my brother", "my sister", "my grandson", "my granddaughter", "my mother in law",
            "my neighbour"],
    "kids": ["the kids", "the little ones", "my youngest", "the twins", "my two", "my boy", "my girl",
             "my grandkids"],
    "day": ["monday", "tuesday", "wednesday", "thursday", "tuesdays", "wednesdays", "thursday nights",
            "monday evenings", "the evening"],
    "shift": ["lates", "earlies", "nights", "a 2 till 10", "a 6 till 2", "12 hour shifts", "a split shift",
              "weekends"],
    "work": ["the shop", "the depot", "the warehouse", "the care home", "work", "the hospital", "the factory",
             "the call centre", "the school kitchen", "my new job", "the hotel"],
    "bus": ["the 47", "the 12", "the X5", "the 31", "the 8a", "the last bus", "the evening bus"],
    "subj": ["the maths", "the english", "the course", "the computer side", "the written work",
             "the assessments", "the units", "the essays", "the coursework"],
    "ill": ["my back", "my knee", "my anxiety", "my depression", "my chest", "my heart", "my diabetes",
            "long covid", "my migraines", "my hip", "my nerves"],
}
TRUE_CLAUSE = {
    "CR": ["{kin} came out of hospital and i look after them now", "no one else can collect {kids} from school",
           "the childminder gave up at half term", "im caring for {kin} since the fall",
           "had to take over looking after {kin}", "{kin} needs me there most of the day now",
           "i have {kids} on my own now", "nobody to sit with {kin} on {day}",
           "{kin} has gone downhill and i do the caring", "lost the after school club place for {kids}",
           "i am now a full time carer for {kin}", "{kin} cant be left any more"],
    "WH": ["my shifts changed to {shift} so i cant make the class", "{work} put me on {shift}",
           "{work} moved me to {day}", "i got more hours at {work} and they clash",
           "my manager at {work} wont swap {day}", "started {shift} at {work}",
           "new rota at {work} means i am never free on {day}", "took on extra shifts at {work}",
           "{work} changed my contract hours", "cant get the time off from {work}"],
    "TR": ["{bus} stopped running that early", "it was two buses each way and i couldnt keep paying it",
           "roadworks on the bypass made me late every week", "my lift fell through when {kin} moved",
           "parking at the centre was impossible after six", "{bus} was cancelled most weeks",
           "the car failed its mot and i cant get there", "moved house and its too far now",
           "the train fares went up again", "no way of getting there after {bus} got cut"],
    "CD": ["{subj} was way above what i did at school", "i couldnt keep up with the pace of {subj}",
           "{subj} was harder than i expected", "felt lost after the first few weeks",
           "the level was wrong for me, should have done entry 3", "{subj} went too fast for me",
           "i didnt understand {subj} and was too embarrassed to say", "{subj} was not what i signed up for",
           "the tutor went too quick with {subj}", "i failed the first assessment and gave up"],
    "HL": ["ive been signed off with {ill}", "{ill} got worse and i couldnt come in",
           "waiting on an operation for {ill}", "chest infection and then it just dragged on",
           "my medication changed and im not right yet", "in and out of hospital with {ill}",
           "{ill} flared up again", "doctor told me to rest because of {ill}",
           "had a fall and broke my wrist", "pregnancy has been hard on me"],
    "OT": ["just wasnt for me in the end", "changed my mind about the course", "didnt get on with it",
           "sorted something else out instead", "no particular reason really", "not going to say",
           "personal reasons", "lost interest", "i will try again another year", "", "n/a", "na",
           "other", "moving on"],
}
# The clause that makes a comment readable as the coded category when the coder read it that way.
BRIDGE = {
    "CR": ["and i cant get cover in the evenings", "so the evenings are not possible for me now",
           "and theres nobody else to do it", "so i cant leave the house at night"],
    "WH": ["so the {day} slot doesnt work with my hours", "and the timing just clashes now",
           "the hours dont fit any more", "so i cant be there for the start", "and {day} is out for me now"],
    "TR": ["and getting across town after that is hard", "so getting there got difficult",
           "and i cant get there in time"],
    "CD": ["and i was falling behind on the work", "i wasnt keeping up either", "and i got behind"],
    "HL": ["and im not been well with it", "it took it out of me health wise", "and its got me down"],
    "OT": ["", "it just stopped working out", "so thats that"],
}
OPENER = ["", "", "", "", "sorry but ", "hi, ", "unfortunately ", "to be honest ", "basically ", "really sorry, "]
CLOSER = ["", "", "", "", ". thanks for everything", ". sorry", ". hope to come back", ". thank you",
          ". will try again next year", ". the tutor was lovely"]


def _fill(rng, text):
    out = text
    while "{" in out:
        a = out.index("{")
        b = out.index("}", a)
        pool = FILL[out[a + 1:b]]
        out = out[:a] + pool[int(rng.integers(0, len(pool)))] + out[b + 1:]
    return out


def _noise(rng, text):
    """The way people type into a free-text box: casing, doubled spaces, a slipped key, no full stop."""
    if not text:
        return text
    if rng.random() < 0.55:
        text = text[0].upper() + text[1:]
    if rng.random() < 0.05:
        text = text.upper()
    if rng.random() < 0.06:
        words = text.split(" ")
        k = int(rng.integers(0, len(words)))
        w = words[k]
        if len(w) > 3:
            j = int(rng.integers(1, len(w) - 1))
            words[k] = w[:j] + w[j + 1] + w[j] + w[j + 2:]
        text = " ".join(words)
    if rng.random() < 0.08:
        text = text.replace(" ", "  ", 1)
    if rng.random() < 0.3:
        text = text + "."
    return text


def comment(rng, tr, cd):
    core = TRUE_CLAUSE[tr][int(rng.integers(0, len(TRUE_CLAUSE[tr])))]
    if not core:                                   # a blank or near-blank box is only ever left as it is
        return core
    txt = _fill(rng, core)
    if cd != tr:
        br = BRIDGE[cd][int(rng.integers(0, len(BRIDGE[cd])))]
        if br:
            txt = txt + " " + _fill(rng, br)
    if len(core) > 12:
        txt = OPENER[int(rng.integers(0, len(OPENER)))] + txt + CLOSER[int(rng.integers(0, len(CLOSER)))]
    return _noise(rng, txt)


def simulate(seed=None):
    seed = W.SEED if seed is None else seed
    rng = np.random.default_rng(seed)
    trng = np.random.default_rng(seed + 101)       # the words people wrote, drawn apart from the reasons
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
            txt = comment(trng, tr, cd)
            rows.append({"wid": wid, "term": t["code"], "true": tr, "coded": cd, "comment": txt})
    # the moderation sample, drawn by CODED category: every OT, and a fixed number of each other code
    mod = []
    for i in codes:
        pool = [r for r in rows if r["coded"] == i]
        take = len(pool) if i in W.MODERATED_ALL else min(W.MODERATED_PER_CODE, len(pool))
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
