"""The ask sheet's cracker and mirror for task281, run on the cut pack (supplemental-stumping Part 1.1).

The cracker lands the call, runs the hygiene battery and executes every filed rule it points at; on the asks it takes
the path a careful solver takes: the energy from the installer's log row (the sodium fixture it took down and the LED
catalog it put up), the tariff's input watts and burning hours, the node records for the dimmed hours with an
unrecorded month at full input, the poles' removals dated from their orders; the repairs from every outage order
completed in 2026, each timed from the earliest report on its own pole (portal stamps converted from UTC) or, for a
crew's find, from the order's creation. The mirror stops at the most attractive wrong rung, the lifecycle model's
Weibull over every conversion driver, and does the asks as the cracker does.

    python3 task281/generator/cracker.py            the sheet for <task>/target
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import params as P     # noqa: E402

W_CALL, W_IF, W_ASK = 38.0, 7.0, 55.0
R_MISS = 5.0             # the recommendation weight a wrong call keeps


def r5(v):
    return int(round(v * 100 / 5) * 5)


def digest(folder):
    h = hashlib.sha256()
    for f in sorted(os.listdir(folder)):
        h.update(f.encode())
        h.update(open(os.path.join(folder, f), "rb").read())
    return h.hexdigest()[:12]


def sheet(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    D = A.load(target)
    G = A.golden_call(D)
    rows = G["rows"]
    towns = sorted(fig["towns"])
    gold_sh = {pc: fig["phases"][pc]["share5"] for pc in P.PHASE_CODES}
    gold_e = {t: fig["towns"][t]["energy"] for t in towns}
    gold_r = {t: fig["towns"][t]["late"] for t in towns}

    # the cracker's asks
    e_cr = A.energy_saving(dict(D, wos=[x for x in D["wos"] if x["kind"] != "glare"]))[0]
    r_cr = A.repairs(D, circuits=False, lookback_days=10)[0]
    e_hit = {t: int(round(e_cr[t])) == gold_e[t] for t in towns}
    r_hit = {t: r_cr[t] == gold_r[t] for t in towns}
    # the mirror's call and construction
    pooled = A.rung_pooled(rows)[0]
    m_sh = {pc: r5(pooled[pc]["share"]) for pc in P.PHASE_CODES}
    m_hit = {pc: m_sh[pc] == gold_sh[pc] for pc in P.PHASE_CODES}

    n_chart = 4    # one bar per phase, the 45 per cent line, the designated phases set apart, each bar's share labelled
    n_ask = len(P.PHASE_CODES) + n_chart + 2 * len(towns)
    crack = len(P.PHASE_CODES) + n_chart + sum(e_hit.values()) + sum(r_hit.values())
    mirror = sum(m_hit.values()) + (n_chart - 1) + sum(e_hit.values()) + sum(r_hit.values())
    Lc, Ls = crack / n_ask, mirror / n_ask
    C = W_CALL + W_IF + W_ASK * Lc
    S = R_MISS + W_IF + W_ASK * Ls
    return dict(digest=digest(target), towns=towns, e_cr=e_cr, r_cr=r_cr, e_hit=e_hit, r_hit=r_hit, m_sh=m_sh,
                m_hit=m_hit, gold_e=gold_e, gold_r=gold_r, gold_sh=gold_sh, Lc=Lc, Ls=Ls, C=C, S=S,
                pair=(C + S) / 2, n_ask=n_ask, crack=crack, mirror=mirror)


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    s = sheet(target)
    print("pack digest %s" % s["digest"])
    print("A2 energy, cracker (installer catalog all year): %s" % ", ".join(
        "%s %d (golden %d)" % (t, round(s["e_cr"][t]), s["gold_e"][t]) for t in s["towns"]))
    print("   hits %d of %d" % (sum(s["e_hit"].values()), len(s["towns"])))
    print("A3 repairs, cracker (earliest report on the order's own pole in the ten days before it): %s" % ", ".join(
        "%s %d (golden %d)" % (t, s["r_cr"][t], s["gold_r"][t]) for t in s["towns"]))
    print("   hits %d of %d" % (sum(s["r_hit"].values()), len(s["towns"])))
    print("A1 shares, mirror (one Weibull over every driver): %s" % ", ".join(
        "%s %d (golden %d)" % (pc, s["m_sh"][pc], s["gold_sh"][pc]) for pc in P.PHASE_CODES))
    print("   hits %d of %d" % (sum(s["m_hit"].values()), len(P.PHASE_CODES)))
    print("cracker keeps %d of %d ask criteria (%.1f per cent): %.1f" % (s["crack"], s["n_ask"], 100 * s["Lc"], s["C"]))
    print("mirror keeps %d of %d ask criteria (%.1f per cent): %.1f" % (s["mirror"], s["n_ask"], 100 * s["Ls"], s["S"]))
    print("pair ceiling %.1f" % s["pair"])


if __name__ == "__main__":
    main()
