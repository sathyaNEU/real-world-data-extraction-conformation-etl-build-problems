"""task464 architecture 9: the ask layer's ceiling, measured on the cut pack.

The cracker (supplemental-stumping Part 1.1) lands the call, runs the hygiene battery and executes every filed
rule the return specification points at. On R1 it drops the cancelled items, keeps the duplicate requests that
were dispensed, carries supply forward within the drug, and reads each issue's days at the dose in the repeat's
directions, which the authorisation extract gives as they stand at the searches. On R2 it takes the day a
patient started ticagrelor 90mg from the issue records, the practice's first issue of it. That is the strongest
reading of the asks a response can take without rebuilding the directions in force on each issue from the change
log, or finding the start in the discharge summaries' coded entries.

  C = 38 + 7 + 55 * Lc     the landed call's score
  S = 5  + 7 + 55 * Ls     the best response off the call
  pair = (C + S) / 2       the ceiling precut.py reads

The asks read no row the call reads (checks.py, the separation block), so a response off the call takes the same
ask path as the cracker and Ls equals Lc by construction.
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


def cracker(D):
    a = A.ask_a(D, use_history=False, drop_cancelled=True)
    b = A.ask_b(D, anchor="gp")
    return a, b


def rows(D=None, wide=False):
    D = D or A.Data()
    F = A.figures(D, write=False)
    a, b = cracker(D)
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
        "R1 current dosage (the device)": net_a(A.ask_a(D, use_history=False)) - g_a,
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
    res = dict(pack=digest(), asked_figures=len(rs), kept=kept, Lc=round(Lc, 4), Ls=round(Ls, 4), pair=round(pair, 1),
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
    for k, v in r["hazards"].items():
        print("  hazard %-48s network move %+.1f points" % (k, v))
    w = r["every_return_column"]
    print("every return column graded: keeps %d of %d, pair %.1f" % (w["kept"], w["figures"], w["pair"]))
