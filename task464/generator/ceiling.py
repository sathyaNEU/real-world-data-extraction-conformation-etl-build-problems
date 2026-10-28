"""task464 architecture 9: the ask layer's ceiling, measured on the cut pack.

The cracker (supplemental-stumping Part 1.1) is the route the portal's responses showed: it lands the call, drops
the cancelled items, keeps the duplicate requests that were dispensed, carries supply forward within the drug, reads
every dose in the directions right (a dose written in milligrams against the product's strength), and rebuilds the
directions on each issue by walking the change log back from the directions each repeat list gives, matching each
change to the repeat its row names. On R2 it takes each start from the discharge summaries' coded entries, pairs it
with the infarction coded within three days, counts it at the practice registered that day and its 90mg issues at
any practice, and reads a term naming a myocardial infarction as the infarction.

  C = 38 + 7 + 55 * Lc     the landed call's score
  S = 5  + 7 + 55 * Ls     the best response off the call
  pair = (C + S) / 2       the ceiling precut.py reads

The asks read no row the call reads (checks.py, the separation block), so a response off the call takes the same
ask path as the cracker and Ls equals Lc by construction. The variants below are the other uniform readings a
careful response could take; the worst of them is reported beside the cracker's, and the gated figure is the worse.
"""
import json, os, hashlib
import world as W
import answers as A

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "generator", "ceiling.json")


def digest():
    h = hashlib.sha256()
    t = os.path.join(BASE, "target")
    for n in sorted(os.listdir(t)):
        h.update(n.encode()); h.update(open(os.path.join(t, n), "rb").read())
    return h.hexdigest()[:16]


VARIANTS = {
    "cracker: walk back by repeat reference, infarction by term": (dict(join="ref", walk="back"), dict(mi="term")),
    "walk forward through the log by repeat reference": (dict(join="ref", walk="log"), dict(mi="term")),
    "walk back, the patient's changes pooled by product": (dict(join="line", walk="back"), dict(mi="term")),
    "walk back by reference, infarction as the one concept": (dict(join="ref", walk="back"), dict(mi="code")),
    "the listed directions, no log": (dict(use_history=False), dict(mi="term")),
    "doses read as tablets a day, walk back": (dict(join="ref", walk="back", parse="words"), dict(mi="term")),
}
CRACKER = "cracker: walk back by repeat reference, infarction by term"


def cracker(D, variant=CRACKER):
    ka, kb = VARIANTS[variant]
    return A.ask_a(D, **ka), A.ask_b(D, **kb)


def rows(D=None, wide=False, variant=CRACKER):
    D = D or A.Data()
    F = A.figures(D, write=False)
    a, b = cracker(D, variant)
    out = []
    for c in sorted(F["ask_a"]):
        k = W.BY_CODE[c]["name"]
        out.append(("R1 percent, %s" % k, F["ask_a"][c]["pct"], A.pct(a[c][1], a[c][0], 1), 0.05))
        if wide:
            out.append(("R1 denominator, %s" % k, F["ask_a"][c]["patients"], a[c][0], 0.5))
            out.append(("R1 numerator, %s" % k, F["ask_a"][c]["at_80"], a[c][1], 0.5))
    for c in sorted(F["ask_b"]):
        k = W.BY_CODE[c]["name"]
        cb = b.get(c, (0, 0))
        out.append(("R2 percent, %s" % k, F["ask_b"][c]["pct"], A.pct(cb[1], cb[0], 0) if cb[0] else None, 0.5))
        if wide:
            out.append(("R2 denominator, %s" % k, F["ask_b"][c]["started"], cb[0], 0.5))
            out.append(("R2 numerator, %s" % k, F["ask_b"][c]["overrun"], cb[1], 0.5))
    return [(n, g, v, v is not None and abs(g - v) < tol) for n, g, v, tol in out]


def hazards(D, F):
    """Each hazard's move on the network's figures, the one handling changed and everything else golden."""
    def net_a(x):
        return A.pct(sum(v[1] for v in x.values()), sum(v[0] for v in x.values()), 1)

    def net_b(x):
        return A.pct(sum(v[1] for v in x.values()), sum(v[0] for v in x.values()), 0)
    g_a, g_b = F["ask_a_network"]["pct"], F["ask_b_network"]["pct"]
    out = {
        "R1 the repeat lists' directions, no log": net_a(A.ask_a(D, use_history=False)) - g_a,
        "R1 log rows matched by the reference they name": net_a(A.ask_a(D, join="ref")) - g_a,
        "R1 walked back from the listed directions": net_a(A.ask_a(D, walk="back")) - g_a,
        "R1 milligram doses read as tablets a day": net_a(A.ask_a(D, parse="words")) - g_a,
        "R2 infarction as the one concept 22298006": net_b(A.ask_b(D, mi="code")) - g_b,
        "R2 infarction as any term naming one": net_b(A.ask_b(D, mi="term")) - g_b,
        "R1 cancelled items kept": net_a(A.ask_a(D, drop_cancelled=False)) - g_a,
        "R1 second issue within 7 days dropped": net_a(A.ask_a(D, dedup_days=7)) - g_a,
        "R1 every issue read as 28 days": net_a(A.ask_a(D, fixed_days=28)) - g_a,
        "R2 first GP issue as the start (the device)": net_b(A.ask_b(D, anchor="gp")) - g_b,
        "R2 ticagrelor 60mg counted": net_b(A.ask_b(D, any_strength=True)) - g_b,
    }
    return {k: round(v, 1) for k, v in out.items()}


def pair_of(rs):
    kept = sum(1 for r in rs if r[3])
    Lc = kept / len(rs)
    Ls = Lc
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Ls
    return kept, Lc, Ls, (C + S) / 2


def main(write=True):
    D = A.Data()
    rs = rows(D)
    kept, Lc, Ls, pair = pair_of(rs)
    wide = rows(D, wide=True)
    kw, Lw, _, pw = pair_of(wide)
    var = {}
    for v in VARIANTS:
        rv = rows(D, variant=v)
        k2, L2, _, p2 = pair_of(rv)
        var[v] = dict(kept=k2, L=round(L2, 4), pair=round(p2, 1), keeps=[r[0] for r in rv if r[3]])
    worst = max(var, key=lambda v: var[v]["pair"])
    res = dict(pack=digest(), asked_figures=len(rs), kept=kept, Lc=round(Lc, 4), Ls=round(Ls, 4), pair=round(pair, 1),
               variants=var, worst_variant=worst, gated_pair=max(round(pair, 1), var[worst]["pair"]),
               mirror_leakage_pct=round(100 * Ls, 1),
               every_return_column=dict(figures=len(wide), kept=kw, L=round(Lw, 4), pair=round(pw, 1)),
               rows=[dict(figure=n, golden=g, cracker=v, kept=h) for n, g, v, h in rs],
               hazards=hazards(D, A.figures(D, write=False)))
    if write:
        json.dump(res, open(OUT, "w"), indent=1)
    return res


if __name__ == "__main__":
    r = main()
    for x in r["rows"]:
        print("%-44s %8s %8s %s" % (x["figure"], x["golden"], x["cracker"], "KEEP" if x["kept"] else "miss"))
    print("pack %s: cracker keeps %d of %d asked figures, Lc %.3f, pair ceiling %.1f, mirror leakage %.1f%%"
          % (r["pack"], r["kept"], r["asked_figures"], r["Lc"], r["pair"], r["mirror_leakage_pct"]))
    for k, v in r["variants"].items():
        print("  variant %-58s keeps %2d, pair %.1f %s" % (k, v["kept"], v["pair"], ("(" + ", ".join(v["keeps"]) + ")") if v["keeps"] else ""))
    print("gated pair ceiling %.1f (worst: %s)" % (r["gated_pair"], r["worst_variant"]))
    for k, v in r["hazards"].items():
        print("  hazard %-48s network move %+.1f points" % (k, v))
    w = r["every_return_column"]
    print("every return column graded: keeps %d of %d, pair %.1f" % (w["kept"], w["figures"], w["pair"]))
