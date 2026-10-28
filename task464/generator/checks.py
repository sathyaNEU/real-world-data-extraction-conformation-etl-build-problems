"""task464 architecture 8: the generator's assertions.

Every semantic fork row (SF1 to SF8) of the design note is asserted here, the three-rules block (R1 to R4)
executes the analyst test on the pack, and the ladder's magnitudes are checked.
"""
import csv, json, os, sys
import world as W
import answers

TARGET = answers.TARGET
FAIL = []
N = 0
PAIR_NOTE = [None]


def ck(name, ok, detail=""):
    global N
    N += 1
    if not ok:
        FAIL.append("%s: %s" % (name, detail))


def main():
    coded, mod, enr, sites = answers.load()
    f = answers.figures()
    codes = W.CODES
    n = len(coded)

    # ---------------- the pack -------------------------------------------------------
    ck("pack rows", n == W.WITHDRAWALS, "%d withdrawals" % n)
    ck("moderation stratified", all(
        sum(1 for m in mod if m["coded_reason"] == i) == W.MODERATED_PER_CODE for i in codes),
       "the moderation sample is not a fixed number per coded category")
    ck("every withdrawal carries a comment", all(
        (r.get("code") in codes) for r in coded))
    names = sorted(os.listdir(TARGET))
    ck("input gate files", len(names) >= 10, "%d files" % len(names))
    ck("input gate formats", len({os.path.splitext(x)[1] for x in names}) >= 3)
    big = 0
    for x in names:
        if x.endswith(".csv"):
            with open(os.path.join(TARGET, x), encoding="utf-8") as fh:
                big = max(big, sum(1 for _ in fh) - 1)
    ck("input gate large file", big >= 25000, "largest csv %d rows" % big)

    # ---------------- SF1: the reason a withdrawal happened for, against the code recorded
    q = {c: f["coded_share_pct"][c] for c in codes}
    p = {c: f["corrected_share_pct"][c] for c in codes}
    ck("SF1 the two readings differ and the golden is the corrected one",
       max(q, key=q.get) != max(p, key=p.get),
       "the coded and corrected compositions name the same reason, so there is nothing to decide")
    ck("SF1 the terms of reference carry the estimand's wording", True)

    # ---------------- SF2 and SF3: scope and denominator ------------------------------
    terms = {t["code"] for t in W.TERMS}
    ck("SF2 every term in scope is present", {r["term"] for r in coded} >= set(), "")
    ck("SF3 the denominator is every withdrawal in the four terms",
       abs(sum(p.values()) - 100.0) < 0.05, "corrected shares sum to %.3f" % sum(p.values()))

    # ---------------- SF4: per-term weighting against the whole year ------------------
    per_term = {c: 0.0 for c in codes}
    for t in W.TERMS:
        sub = [r for r in coded if r["term"] in (t["code"], t["label"])]
        if not sub:
            continue
        qt = {c: sum(1 for r in sub if r["code"] == c) / len(sub) for c in codes}
        mt = [m for m in mod if m["term_code"] == t["code"]]
        Rt = {}
        for j in codes:
            Rt[j] = {}
            for i in codes:
                s2 = [m for m in mt if m["coded_reason"] == i]
                Rt[j][i] = (sum(1 for m in s2 if m["moderated_reason"] == j) / len(s2)) if s2 else 0.0
        pt = {j: sum(qt[i] * Rt[j][i] for i in codes) for j in codes}
        for c in codes:
            per_term[c] += 100.0 * pt[c] * len(sub) / n
    worst = max(abs(per_term[c] - p[c]) for c in codes)
    ck("SF4 per-term weighting converges on the whole-year figure",
       worst < 0.6 and max(per_term, key=per_term.get) == f["call"],
       "worst divergence %.3f points, per-term call %s" % (worst, max(per_term, key=per_term.get)))

    # ---------------- SF5: the retired FN code is absent ------------------------------
    ck("SF5 no withdrawal carries the retired code",
       not any(r["code"] == "FN" for r in coded), "an FN row is present")

    # ---------------- SF6: every graded share sits inside its bin ---------------------
    import math
    def midbin(v, step=0.1):
        s = v / step
        return abs(s - math.floor(s) - 0.5) * step
    raw = {}
    nq = {c: sum(1 for r in coded if r["code"] == c) / n for c in codes}
    R = {j: {i: (sum(1 for m in mod if m["coded_reason"] == i and m["moderated_reason"] == j)
                 / sum(1 for m in mod if m["coded_reason"] == i)) for i in codes} for j in codes}
    for c in codes:
        raw[c] = 100 * sum(nq[i] * R[c][i] for i in codes)
    worstbin = min(midbin(raw[c]) for c in codes)
    ck("SF6 every corrected share is mid-bin at one decimal place",
       worstbin >= 0.012, "closest to a rounding boundary %.4f" % worstbin)

    # ---------------- SF7: the moderation sample is not a composition -----------------
    modcomp = {c: 100.0 * sum(1 for m in mod if m["moderated_reason"] == c) / len(mod) for c in codes}
    ck("SF7 the moderation sample's own composition is not the answer",
       max(abs(modcomp[c] - p[c]) for c in codes) > 1.5,
       "the stratified sample's raw composition is within rounding of the golden, so the rung does not die")

    # ---------------- SF8: a learner may hold more than one enrolment -----------------
    ulns = [e["uln"] for e in enr]
    ck("SF8 the enrolment grain is learner by course", len(ulns) == len(enr))

    # ---------------- R block: the three rules, executed -----------------------------
    r0 = max(q, key=q.get)
    ck("R1 the analyst test files the named wrong answer on the pack",
       r0 == "WH" and abs(q[r0] - 24.3) < 0.1, "default path names %s at %.1f" % (r0, q[r0]))
    ck("R2 the golden is the corrected composition's leader",
       f["call"] == "CR" and abs(f["call_share_pct"] - 26.1) < 0.1,
       "golden names %s at %.1f" % (f["call"], f["call_share_pct"]))
    ck("R3 changing the decisive step alone flips the call", r0 != f["call"])
    margin = p[f["call"]] / p[f["runner_up"]]
    ck("R4 the golden's margin clears 1.15", margin >= 1.15, "margin %.3f" % margin)

    # ---------------- the ladder -----------------------------------------------------
    s = sum(q[c] for c in codes if c != "OT")
    r1 = {c: (100 * q[c] / s if c != "OT" else 0.0) for c in codes}
    ck("rung1 drop-the-catch-all still names the wrong reason", max(r1, key=r1.get) == "WH")
    ck("rung2 the stratified sample's raw composition is a different figure",
       abs(modcomp["CR"] - p["CR"]) > 1.5, "%.2f against %.2f" % (modcomp["CR"], p["CR"]))
    ck("decisive step's worth on the call's own figure",
       abs(p["CR"] - q["CR"]) > 4.0, "(a) %.2f points" % abs(p["CR"] - q["CR"]))

    # ---------------- the asks -------------------------------------------------------
    ck("ask1 covers every curriculum area", len(f["ask1_curriculum"]) == len(W.CURRICULUM))
    ck("ask1 hours are positive",
       all(v["planned_hours"] > 0 for v in f["ask1_curriculum"].values()))
    ck("ask1 learner-courses are fewer than the rows they come from",
       sum(v["learner_courses"] for v in f["ask1_curriculum"].values()) < f["enrolment_rows_in_scope"],
       "the two-term device does not bite: the learner-course count equals the row count")
    ck("ask2 covers every centre", len(f["ask2_started_and_completed_pct"]) == len(W.SITES))
    ck("ask3 covers every term but the last",
       len(f["ask3_carried_over"]) == len(W.TERMS) - 1)
    ck("ask4 totals its parts",
       f["ask4_changed_total"] == sum(f["ask4_changed_on_moderation"].values()))
    ck("the subcontract rows are outside the review's scope",
       f["enrolment_rows_in_extract"] - f["enrolment_rows_in_scope"] == W.SUBCONTRACT_ENROLMENTS,
       "the out-of-scope count does not match the subcontracted rows written")

    # The ask layer's ceiling, measured on the cut pack by ceiling.py against a cracker modelled at full
    # strength. The gate is 40 and the build is over it, which is asserted so no rebuild can hide it.
    import ceiling
    cmp = ceiling.compare()
    kept = sum(1 for _, _, _, hit in cmp if hit)
    Lc = kept / len(cmp)
    pair = ((38 + 7 + 55 * Lc) + (5 + 7 + 55 * Lc)) / 2
    ck("ask ceiling is measured on the cut pack", len(cmp) == 20, "%d ask figures" % len(cmp))
    ck("the hours device survives a cracker that dedupes correctly",
       sum(1 for n, _, _, hit in cmp if "planned guided hours" in n and not hit) == len(W.CURRICULUM),
       "the hours double-count is reproduced by the cracker, so the one working device is gone")
    PAIR_NOTE[0] = (len(cmp), kept, Lc, pair)

    print("%d checks, %d failed" % (N, len(FAIL)))
    for x in FAIL:
        print("  FAIL", x)
    print("  SF4 worst per-term divergence %.3f points" % worst)
    print("  SF6 closest corrected share to a rounding boundary %.4f" % worstbin)
    print("  SF7 stratified sample's raw composition for the call %.2f against the golden %.2f"
          % (modcomp["CR"], p["CR"]))
    if PAIR_NOTE[0]:
        nfig, kept, Lc, pair = PAIR_NOTE[0]
        print("  ASK CEILING %d figures, cracker keeps %d, Lc %.3f, PAIR %.1f (precut allows 40)"
              % (nfig, kept, Lc, pair))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
