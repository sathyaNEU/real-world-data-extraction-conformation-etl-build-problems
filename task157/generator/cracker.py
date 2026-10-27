#!/usr/bin/env python3
"""task157 architecture 2, the stage 2 measurement harness.

Runs on the generator's clean truth (no pack exists yet; stage 3 re-runs every number against the cut
bundle). It answers four questions the design note owes, and it is deterministic: two runs print the
same bytes.

  1  the reflex sweep, every route a competent analyst takes on the deciding quantity, with the printed
     figure and the statutory band each files (the readability screen's test 3 and the ladder)
  2  the convergence block, the golden's OWN family and at least two families a solver builds INSTEAD,
     with the bucket each files (architecture 1's measured blind spot)
  3  the bin measurements (a), (b) and (c) in units of the graded figure's own bin
  4  the cracker sheet and the pair arithmetic for the ask sheet

    python3 task157/generator/cracker.py [--seeds 5]
"""
import argparse
import math
import random

# ---------------------------------------------------------------- the world

BIN = 5_000               # the asking sentence's rounding on the graded figure
REQUIRED = 384_924        # 15 per cent of the votes cast for Governor in 2026
BAND_LO = 365_678         # 95 per cent of required: below this the petition is insufficient
BAND_HI = 404_170         # 105 per cent of required: above this it is sufficient

SHEETS = 36_000           # petition sheets filed and receipted
LINES = 15                # signature lines a sheet carries
FILED = SHEETS * LINES    # 540,000 signature lines filed
SAMPLE = FILED // 20      # the statute's five per cent random sample of the signatures filed
P = SAMPLE / FILED        # 0.05

SINGLE_RATE = 0.2100      # signer is not registered, address does not match, signature does not match
DOUBLES = 60_000          # signers who signed the petition twice
TRIPLES = 150             # signers who signed it three times
# The county still filing on the pre-2024 code set folds "not registered" and "duplicate" into one code.
# Measured at a 9.2 per cent share of the sampled duplicate strikes it moves the golden by 0.61 bins while
# four of five seeds sit 0.03 to 0.19 bins from a cell edge, so unfolding it was load-bearing on the graded
# figure and therefore a fork. Closed by C1 in the world rather than by a sentence: that county's sampled
# lines were gathered by one firm in one week and carry no duplicate strike at all, so the fold is neutral
# on every route and the single-ground classes it also folds expand at the common factor.
FOLDED_COUNTY_SHARE = 0.0
# Sampled lines whose signer was cancelled in the list-maintenance run that ran during the circulation
# window and who signed after their own cancellation. The extract current when circulation opened still
# shows them registered, so a solver re-deriving registration from it does not strike them although they
# were not registered at signing; the counties, checking live at verification, did strike them. The slip
# therefore walks the figure AWAY from the golden, so every correction below the decisive one walks one
# way and only the decisive move reverses (stumping Part 3).
VINTAGE_SLIP = 400
COUNTY_STRUCK = 0.62      # share of sampled duplicate strikes the county recorder found inside its own batch
COUNTIES = 15
FIRMS = 4


def band(valid):
    """The statutory disposition the projection files."""
    if valid < BAND_LO:
        return "insufficient"
    if valid > BAND_HI:
        return "sufficient"
    return "full count"


def printed(valid):
    """The graded figure as the asking sentence rounds it."""
    return int(round(valid / BIN)) * BIN


def edge(valid):
    """Distance from the printed cell's nearest edge (determinism-check section 3)."""
    return BIN / 2 - abs(valid - printed(valid))


# ---------------------------------------------------------------- clean truth

def truth(seed):
    """One draw of the world, at the signer level. Sampling is modelled as independent inclusion of each
    signature line at P; the hypergeometric correction is P*(n-1)/(F-1), carried in the family below and
    measured there at under a thousandth of a bin."""
    rng = random.Random(seed)

    # Registration validity is a property of the SIGNER, so both lines of a double signer share it, and
    # the office strikes on the first ground that applies: not registered before duplicate.
    reg_doubles = sum(1 for _ in range(DOUBLES) if rng.random() >= SINGLE_RATE)
    reg_triples = sum(1 for _ in range(TRIPLES) if rng.random() >= SINGLE_RATE)

    # Full count: a signer who signed k times and is registered loses k-1 lines as duplicates.
    dup_full = reg_doubles + 2 * reg_triples

    # The sample. A double signer's pair is seen only when both its lines are drawn.
    seen2 = sum(1 for _ in range(reg_doubles) if rng.random() < P and rng.random() < P)
    seen3 = 0
    for _ in range(reg_triples):
        s = sum(1 for _ in range(3) if rng.random() < P)
        seen3 += max(0, s - 1)
    dup_seen = seen2 + seen3

    # Single-ground strikes among the sampled lines.
    single_seen = 0
    for _ in range(SAMPLE):
        if rng.random() < SINGLE_RATE:
            single_seen += 1

    folded = int(round(dup_seen * FOLDED_COUNTY_SHARE))   # filed under the old county's merged code

    return {
        "seed": seed,
        "dup_full": dup_full,
        "dup_seen": dup_seen,
        "single_seen": single_seen,
        "folded": folded,
        "reg_doubles": reg_doubles,
        "reg_triples": reg_triples,
    }


def valid_from(single_seen, dup_estimate):
    """The projection: filed less the single-ground grounds expanded at the sample's own factor, less the
    estimated duplicate burden."""
    return FILED - single_seen * (FILED / SAMPLE) - dup_estimate


# ---------------------------------------------------------------- the routes

def routes(t):
    """Every route a competent analyst takes on the deciding quantity.

    Returns a list of (key, label, valid, note). The reflex row is enumerated from election
    administration's and sampling's own vocabulary for a sample projection, not from the rungs beneath it.
    """
    s, d, folded = t["single_seen"], t["dup_seen"], t["folded"]
    out = []

    # R1 the default path: every disposition class expanded at the sample's factor, registration re-derived
    #    from the extract current at FILING rather than at signing.
    out.append(("R1", "every class at N/n, registration re-derived off the pre-run extract",
                valid_from(s - VINTAGE_SLIP, d * (FILED / SAMPLE)), "rung 0"))

    # R2 the same, vintage fixed. Note the folded county is NEUTRAL here: both classes carry one factor.
    out.append(("R2", "every class at N/n, vintage fixed", valid_from(s, d * (FILED / SAMPLE)), "rung 1"))

    # R3 a duplicate pair read as two invalid lines rather than one.
    out.append(("R3", "every class at N/n, both lines of a pair struck",
                valid_from(s, 2 * d * (FILED / SAMPLE)), "reflex"))

    # R4 expanded county by county and summed (the factor is common, so this is R2 exactly).
    out.append(("R4", "expanded per county and summed", valid_from(s, d * (FILED / SAMPLE)), "reflex"))

    # R5 the duplicate class expanded on the SIGNER base rather than the signature base.
    signers = FILED - DOUBLES - 2 * TRIPLES
    out.append(("R5", "duplicates expanded at the signer factor S/s",
                valid_from(s, d * (signers / (SAMPLE * (signers / FILED)))), "reflex"))

    # R6 "either line of the pair drawn", a half-seen pair correction at 2p.
    out.append(("R6", "duplicates at 2p, either line drawn", valid_from(s, d / (2 * P)), "reflex"))

    # R7 Chao1 on the sampled signers' frequency distribution, the capture-recapture reflex.
    f2 = d                                   # signers seen twice in the sample
    f1 = SAMPLE - 2 * d                      # signers seen once
    chao = (f1 * f1) / (2 * f2) if f2 else float("inf")
    out.append(("R7", "Chao1 unseen pairs off the sample's singletons and doubletons",
                valid_from(s, chao), "rival family"))

    # R8 the decisive step applied without unfolding the old county's merged code.
    # rung 2: the pair logic applied to the cross-county strikes only, on the view that a county recorder
    # checked its whole batch while the state could only cross-check the sample. Refuted by one shipped
    # fact: no county keyed a line outside its own sampled sections, so no full-batch check was possible.
    cs = int(round(d * COUNTY_STRUCK))
    out.append(("R10", "pair inclusion on the cross-county strikes only, county strikes at N/n",
                valid_from(s, cs * (FILED / SAMPLE) + (d - cs) / (P * P)), "rung 2"))
    out.append(("R8", "pair inclusion with the folded county's duplicates left folded",
                valid_from(s + folded, (d - folded) / (P * P)), "SF closure, C1"))

    # R9 the golden: single grounds at N/n, duplicate strikes at the pair's own inclusion probability.
    # SF5: the filed total read off the counties' reported sheet counts rather than the office receipt log,
    # which carries the 240 sheets two firms filed twice and the office struck at receipt.
    f2 = FILED + 240 * LINES
    p2 = SAMPLE / f2
    out.append(("R11", "golden on the counties' reported filed total, not the receipt log",
                f2 - s * (f2 / SAMPLE) - d / (p2 * p2), "SF5"))

    out.append(("R9", "pair inclusion P squared, vintage fixed, folded county unfolded",
                valid_from(s, d / (P * P)), "GOLDEN"))

    return out


def families(t):
    """Convergence. The golden's own family first, then the families a competent solver builds INSTEAD."""
    s, d = t["single_seen"], t["dup_seen"]
    own, rival = [], []

    own.append(("P squared", valid_from(s, d / (P * P))))
    hyper = P * ((SAMPLE - 1) / (FILED - 1))
    own.append(("hypergeometric pair inclusion", valid_from(s, d / hyper)))
    # per county and per firm: the estimator is a count over a constant, so every grouping collapses.
    for name, groups in (("grouped per county", COUNTIES), ("grouped per firm", FIRMS)):
        parts, rem = [], d
        for i in range(groups):
            take = rem // (groups - i)
            parts.append(take)
            rem -= take
        own.append((name, valid_from(s, sum(x / (P * P) for x in parts))))
    own.append(("two-step: partner seen at P, then expanded at N/n",
                valid_from(s, (d / P) * (FILED / SAMPLE))))

    rival.append(("Chao1 unseen pairs", valid_from(s, ((SAMPLE - 2 * d) ** 2) / (2 * d))))
    # a bootstrap over the sampled lines: resample the sample, recompute the golden, take the mean.
    rng = random.Random(90_000 + t["seed"])
    draws = []
    for _ in range(200):
        boot = sum(1 for _ in range(d) if True) if d == 0 else 0
        boot = 0
        for _ in range(SAMPLE):
            if rng.random() < d / SAMPLE:
                boot += 1
        draws.append(valid_from(s, boot / (P * P)))
    rival.append(("bootstrap over sampled lines, mean", sum(draws) / len(draws)))
    rival.append(("linear expansion of every class", valid_from(s, d * (FILED / SAMPLE))))
    return own, rival


def bins(t):
    """(a) the decisive step's worth, (b) the defensible family spread, (c) the golden estimator's own
    95 per cent sampling interval, each in units of the graded figure's bin."""
    s, d = t["single_seen"], t["dup_seen"]
    gold = valid_from(s, d / (P * P))
    naive = valid_from(s, d * (FILED / SAMPLE))
    a = abs(gold - naive)

    own, _ = families(t)
    spread = max(v for _, v in own) - min(v for _, v in own)

    sd_dup = math.sqrt(d) / (P * P)
    sd_single = math.sqrt(SINGLE_RATE * (1 - SINGLE_RATE) / SAMPLE) * FILED
    c = 1.96 * math.sqrt(sd_dup ** 2 + sd_single ** 2)

    # the triple-signer bias the all-doubles estimator carries, which (b) is only small if the world's
    # multiplicity is near binary
    exp_seen = t["reg_doubles"] * P * P + t["reg_triples"] * (3 * P * P - P ** 3)
    tri_bias = abs(exp_seen / (P * P) - t["dup_full"])

    cs = int(round(d * COUNTY_STRUCK))
    rung2 = valid_from(s, cs * (FILED / SAMPLE) + (d - cs) / (P * P))
    rung0 = valid_from(s - VINTAGE_SLIP, d * (FILED / SAMPLE))
    return {"gold": gold, "naive": naive, "a": a, "b": spread, "c": c, "tri": tri_bias,
            "g0": (rung0 - naive), "g1": (naive - rung2), "g2": (rung2 - gold),
            "clear_hi": BAND_HI - gold, "clear_lo": gold - BAND_LO, "edge": edge(gold)}


# ---------------------------------------------------------------- the ask sheet

# Each row: the ask, its figures, its weight share of the ask block, and whether the careful solver that
# takes the call's default path also takes this ask's easy route (the cracker). A row is MISS when the
# ask's own silent device defeats that route.
ASKS = [
    ("A", "sampled and projected figure for each disposition the counties used", 22, 0.26, 0.35,
     "the pre-2024 merged code has to be unfolded before any class is projected, and the grounds apply in "
     "order, so a sampled line sits in exactly one class", "miss"),
    ("B", "each county's sheets, sampled signatures and invalid rate other than duplication", 45, 0.28, 0.30,
     "two counties filed their register twice and the correction supersedes row by row, so a wholesale "
     "replacement loses the rows the correction does not carry", "miss"),
    ("C", "each circulator firm's sheets, sampled signatures and invalid rate other than duplication", 12,
     0.30, 0.28,
     "240 sheets were filed twice by two firms and struck at receipt, so a firm's sheets filed is the "
     "receipt log's count and not the counties' reported count", "miss"),
    ("D", "per month of circulation, sampled signatures and those the later extract has cancelled", 12, 0.16,
     0.30,
     "the extract timestamps are UTC against local signing dates, so a month boundary moves 17 hours of "
     "signatures", "miss"),
]

CALL_WEIGHT = 0.40      # recommendation and critical components
INSTRUCTION = 0.05
ASK_WEIGHT = 0.55


ON_CALL = 45.0          # what a response that files the golden's call and components banks before any ask
OFF_CALL = 12.0         # what a response on rung 0 or rung 1 banks


def pair_arithmetic():
    """The two cold responses the ladder is built against, on the rubric's own weights.

    The ladder is built so one of the top two lands the call and one does not (`stumping` Part 0), and the
    ask layer holds each of them under two fifths of the ask weight. The share each ask's own device leaves
    on the table is the fifth field of ASKS, measured per ask rather than assumed to be all or nothing.
    """
    base = sum(w * keep for _, _, _, w, keep, _, _ in ASKS)
    lander = base + 0.06          # the response that lands the call also reads two asks more carefully
    misser = base
    r1 = ON_CALL + 100 * ASK_WEIGHT * lander + 100 * INSTRUCTION * 0.80
    r2 = OFF_CALL + 100 * ASK_WEIGHT * misser + 100 * INSTRUCTION * 0.60
    return r1, r2, (r1 + r2) / 2, lander, misser


# ---------------------------------------------------------------- report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    args = ap.parse_args()
    seeds = list(range(157, 157 + args.seeds))

    print("task157 architecture 2, stage 2 harness")
    print("filed %d lines on %d sheets, statutory sample %d (%.4f), required %d, bands %d and %d, bin %d"
          % (FILED, SHEETS, SAMPLE, P, REQUIRED, BAND_LO, BAND_HI, BIN))
    print()

    print("1  reflex sweep and ladder (seed 157)")
    t0 = truth(seeds[0])
    gold0 = valid_from(t0["single_seen"], t0["dup_seen"] / (P * P))
    print("   %-4s %-62s %10s %10s %6s  %s" % ("", "route", "valid", "printed", "bins", "band"))
    for key, label, v, note in routes(t0):
        print("   %-4s %-62s %10.0f %10d %6.2f  %s%s"
              % (key, label[:62], v, printed(v), (v - gold0) / BIN, band(v),
                 "" if note in ("reflex", "") else "   <- " + note))
    print()

    print("2  convergence, the golden's own family then the families a solver builds instead (seed 157)")
    own, rival = families(t0)
    for name, v in own:
        print("   own    %-52s %10.0f  prints %7d  %s" % (name[:52], v, printed(v), band(v)))
    for name, v in rival:
        print("   RIVAL  %-52s %10.0f  prints %7d  %s" % (name[:52], v, printed(v), band(v)))
    print()

    print("3  bins over %d seeds (bin %d valid signatures)" % (len(seeds), BIN))
    print("   %-6s %10s %10s %8s %8s %8s %8s %8s %8s %6s %6s %6s"
          % ("seed", "golden", "rung1", "(a)", "(b)", "(c)", "hi clr", "lo clr", "edge",
             "gap01", "gap12", "gap2g"))
    agg = []
    for sd in seeds:
        m = bins(truth(sd))
        agg.append(m)
        print("   %-6d %10.0f %10.0f %8.2f %8.3f %8.2f %8.2f %8.2f %8.0f %6.2f %6.2f %6.2f"
              % (sd, m["gold"], m["naive"], m["a"] / BIN, m["b"] / BIN, m["c"] / BIN,
                 m["clear_hi"] / BIN, m["clear_lo"] / BIN, m["edge"],
                 m["g0"] / BIN, m["g1"] / BIN, m["g2"] / BIN))
    n = len(agg)
    print("   mean   %10.0f %10.0f %8.2f %8.3f %8.2f %8.2f %8.2f %8s %6.2f %6.2f %6.2f"
          % (sum(m["gold"] for m in agg) / n, sum(m["naive"] for m in agg) / n,
             sum(m["a"] for m in agg) / n / BIN, sum(m["b"] for m in agg) / n / BIN,
             sum(m["c"] for m in agg) / n / BIN, sum(m["clear_hi"] for m in agg) / n / BIN,
             sum(m["clear_lo"] for m in agg) / n / BIN, "",
             sum(m["g0"] for m in agg) / n / BIN, sum(m["g1"] for m in agg) / n / BIN,
             sum(m["g2"] for m in agg) / n / BIN))
    worst = min(m["g2"] for m in agg) / BIN
    print("   smallest rung gap over the seeds: %.2f bins (gap01 %.2f, gap12 %.2f, gap2g %.2f at the mean)"
          % (min(min(m["g0"], m["g1"], m["g2"]) for m in agg) / BIN,
             sum(m["g0"] for m in agg) / n / BIN, sum(m["g1"] for m in agg) / n / BIN,
             sum(m["g2"] for m in agg) / n / BIN))
    print("   decisive gap is the largest at every seed: %s; its worst value %.2f bins against (b)+(c) %.2f"
          % (all(m["g2"] > max(m["g0"], m["g1"]) for m in agg), worst,
             max((m["b"] + m["c"]) / BIN for m in agg)))
    print("   bands filed by the golden: %s" % sorted({band(m["gold"]) for m in agg}))
    print("   bands filed by the default: %s" % sorted({band(m["naive"]) for m in agg}))
    print("   all-doubles triple bias, mean %.0f signatures (%.4f bins)"
          % (sum(m["tri"] for m in agg) / n, sum(m["tri"] for m in agg) / n / BIN))
    print()

    print("4  cracker sheet and pair arithmetic")
    r1, r2, pair, lander, misser = pair_arithmetic()
    for key, label, figs, w, keep, device, verdict in ASKS:
        print("   %-3s %-58s %3d figs  weight %.2f  keeps %.2f  %s"
              % (key, label[:58], figs, w, keep, verdict))
    print("   ask weight kept: lander %.3f, best off-call response %.3f (bar 0.40)" % (lander, misser))
    print("   response 1 (lands the call) %.1f, response 2 (rung 1) %.1f" % (r1, r2))
    print("   pair ceiling %.1f (build target 60, bar 70); mirror leakage %.1f per cent of ask weight"
          % (pair, 100 * misser))


if __name__ == "__main__":
    main()
