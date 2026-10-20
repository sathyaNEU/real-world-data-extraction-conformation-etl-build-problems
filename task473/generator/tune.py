"""Tuning the knobs against the design note's ladder (run by hand; the generator reads only world.py).

    python3 tune.py            # report: every route's set, each county's completed deaths and rate under the family
    python3 tune.py --found    # search world.LOCAL_FOUND so each county's deaths sit inside one whole number

The search changes only how many of a county's impaired surviving drivers at the arrest-only agencies were arrested
at each band (within two of the drawn count) and keeps every route's set as the ladder names it."""
import sys

import methods as M
import truth as T
import world as W

LADDER = {"G": {"005", "011", "019", "027"}, "R6": {"005", "011", "019", "021"}, "R2": {"005", "011", "019"},
          "R8": {"003", "005", "011", "019"}, "R5": {"005", "011", "019", "021"}, "truth": {"005", "011", "019", "027"}}


def evaluate():
    crashes = T.build()
    obs = T.observe(crashes)
    vmt = {c["fips"]: T.knobs(c["fips"])["vmt3"] * 1e8 for c in W.COUNTIES}
    sets = {r: {f for f, v in M.rate(M.route(obs, r), vmt).items() if v >= W.THRESHOLD} for r in LADDER
            if r != "truth"}
    true = {}
    for cr in crashes:
        if T.ai(cr):
            true[cr.fips] = true.get(cr.fips, 0) + T.deaths(cr)
    sets["truth"] = {f for f in vmt if true.get(f, 0) / vmt[f] * 1e8 >= W.THRESHOLD}
    fam = M.g_family(obs)
    out = {}
    for c in W.COUNTIES:
        f = c["fips"]
        ds = [fam[k].get(f, 0.0) for k in fam]
        g = fam["pooled"].get(f, 0.0)
        n = round(g)
        margin = min(min(ds) - (n - 0.5), (n + 0.5) - max(ds))
        out[f] = dict(g=g, lo=min(ds), hi=max(ds), margin=margin, rate=g / vmt[f] * 1e8)
    return crashes, sets, out


def found_counts(crashes, f):
    res = []
    for b in (0, 1):
        rows = [p for cr in crashes if cr.fips == f and not T.protocol(cr) for p in cr.persons
                if p.is_driver and p.identified and not p.killed and p.band == b]
        res.append((sum(p.arrested for p in rows), len(rows)))
    return res


def report():
    crashes, sets, out = evaluate()
    for r, s in sets.items():
        print(r, sorted(W.NAMES[f] for f in s), "ok" if s == LADDER[r] else "OFF LADDER")
    for c in W.COUNTIES:
        o = out[c["fips"]]
        print("%-10s deaths %7.2f (family %.2f to %.2f, margin %.2f) rate %.4f" % (
            c["name"], o["g"], o["lo"], o["hi"], o["margin"], o["rate"]))


def search(min_margin=0.20):
    crashes, sets, out = evaluate()
    assert all(sets[r] == LADDER[r] for r in LADDER), sets
    for c in W.COUNTIES:
        f = c["fips"]
        if out[f]["margin"] >= min_margin:
            continue
        (lo, nlo), (hi, nhi) = found_counts(crashes, f)
        tried = []
        for a in range(max(0, lo - 2), min(nlo, lo + 2) + 1):
            for b in range(max(0, hi - 2), min(nhi, hi + 2) + 1):
                if (a, b) == (lo, hi):
                    continue
                W.LOCAL_FOUND[f] = (a, b)
                cr2, s2, o2 = evaluate()
                if all(s2[r] == LADDER[r] for r in LADDER):
                    tried.append((o2[f]["margin"], abs(a - lo) + abs(b - hi), (a, b)))
        good = sorted([t for t in tried if t[0] >= min_margin], key=lambda t: (t[1], -t[0]))
        pick = good[0] if good else max(tried)
        W.LOCAL_FOUND[f] = pick[2]
        print("%-10s found %s of %s -> %s, margin %.2f" % (c["name"], (lo, hi), (nlo, nhi), pick[2], pick[0]))
    print("LOCAL_FOUND =", dict(sorted(W.LOCAL_FOUND.items())))


if __name__ == "__main__":
    if "--found" in sys.argv:
        search()
    else:
        report()
