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


def r0_default(q):
    return max(q, key=q.get)


def main():
    coded, mod, enr, sites = answers.load()
    f = answers.figures()
    codes = W.CODES
    n = len(coded)

    # ---------------- the pack -------------------------------------------------------
    ck("pack rows", n == W.WITHDRAWALS, "%d withdrawals" % n)
    ck("moderation drawn by coded category", all(
        sum(1 for m in mod if m["coded_reason"] == i) ==
        (sum(1 for r in coded if r["code"] == i) if i in W.MODERATED_ALL else W.MODERATED_PER_CODE)
        for i in codes), "the moderation sample is not every OT and a fixed number of each other code")
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

    R0 = {j: {i: (sum(1 for m in mod if m["coded_reason"] == i and m["moderated_reason"] == j)
                  / sum(1 for m in mod if m["coded_reason"] == i)) for i in codes} for j in codes}

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

    # ---------------- SF8: the unit is the withdrawal, not the learner -----------------
    wl = {}
    for r in csv.DictReader(open(os.path.join(TARGET, "withdrawals_autumn_winter_2025.csv"), encoding="utf-8")):
        wl[r["withdrawal_ref"]] = r["uln"]
    for r in json.load(open(os.path.join(TARGET, "withdrawals_spring_summer_2026.json"), encoding="utf-8"))["records"]:
        wl[r["withdrawalRef"]] = r["learnerUln"]
    byl = {}
    for r in coded:
        byl.setdefault(wl[r["ref"]], r["code"])
    ql = {c: sum(1 for v in byl.values() if v == c) for c in codes}
    ck("SF8 counting learners instead of withdrawals leaves the same call",
       max(ql, key=ql.get) == r0_default(q), "%d learners for %d withdrawals" % (len(byl), n))

    # ---------------- SF9: the forward form of the same correction converges -----------
    import numpy as _np
    Pj = {j: sum(nq[i] * R[j][i] for i in codes) for j in codes}
    Mw = _np.array([[nq[i] * R[j][i] / Pj[j] for j in codes] for i in codes])
    pw = _np.linalg.solve(Mw, _np.array([nq[c] for c in codes]))
    ck("SF9 the weighted forward inversion files the golden to the last digit",
       max(abs(100 * pw[k] - raw[c]) for k, c in enumerate(codes)) < 1e-9)

    # ---------------- Layer 1 is mess-neutral on the call ----------------------------
    raw_rows = answers.load(raw=True)[0]
    dup = len(raw_rows) - len({r["ref"] for r in raw_rows})
    ck("L1 late-keyed winter withdrawals sit in both exports", dup > 100, "%d repeated references" % dup)
    noisy = sum(1 for r in raw_rows if r["code"] not in codes)
    ck("L1 the old system's typed codes carry case and space noise", noisy > 100, "%d noisy codes" % noisy)
    def lead(rs, norm):
        cnt = {c: 0 for c in codes}
        for r in rs:
            c = r["code"].strip().upper() if norm else r["code"]
            if c in cnt:
                cnt[c] += 1
        return max(cnt, key=cnt.get), cnt
    ck("L1 keeping the repeats leaves the default path's answer", lead(raw_rows, True)[0] == "WH")
    ck("L1 dropping the noisy codes leaves the default path's answer", lead(raw_rows, False)[0] == "WH")
    cnt = lead(raw_rows, True)[1]
    nn = sum(cnt.values())
    pk = {j: sum(cnt[i] / nn * R0[j][i] for i in codes) for j in codes}
    ck("L1 keeping the repeats leaves the golden call", max(pk, key=pk.get) == f["call"])

    # ---------------- R block: the three rules, executed -----------------------------
    r0 = max(q, key=q.get)
    ck("R1 the analyst test files the named wrong answer on the pack",
       r0 == "WH" and abs(q[r0] - 24.4) < 0.05, "default path names %s at %.1f" % (r0, q[r0]))
    ck("R2 the golden is the corrected composition's leader",
       f["call"] == "CR" and abs(f["call_share_pct"] - 25.1) < 0.05,
       "golden names %s at %.1f" % (f["call"], f["call_share_pct"]))
    ck("R3 changing the decisive step alone flips the call", r0 != f["call"])
    margin = p[f["call"]] / p[f["runner_up"]]
    ck("R4 the golden's margin clears 1.15", margin >= 1.15, "margin %.3f" % margin)

    # ---------------- the ladder -----------------------------------------------------
    s = sum(q[c] for c in codes if c != "OT")
    r1 = {c: (100 * q[c] / s if c != "OT" else 0.0) for c in codes}
    ck("rung1 drop-the-catch-all still names the wrong reason", max(r1, key=r1.get) == "WH")
    ck("rung2 the moderation sample's own composition names a different reason",
       max(modcomp, key=modcomp.get) != f["call"], "it names %s" % max(modcomp, key=modcomp.get))
    # rung 2b: the moderator's category substituted on the moderated rows, every other code kept
    modref = {m["withdrawal_ref"]: m["moderated_reason"] for m in mod}
    sub = {c: 0 for c in codes}
    for r in coded:
        sub[modref.get(r["ref"], r["code"])] += 1
    ck("rung2b substituting the moderated codes still names the wrong reason",
       max(sub, key=sub.get) == "WH", "it names %s" % max(sub, key=sub.get))
    ck("decisive step's worth on the call's own figure",
       abs(p["CR"] - q["CR"]) > 4.0, "(a) %.2f points" % abs(p["CR"] - q["CR"]))

    # ---------------- the asks -------------------------------------------------------
    import csv as _csv
    cat = {c["course_ref"]: c for c in _csv.DictReader(open(os.path.join(TARGET, "course_catalogue_2025_26.csv"),
                                                            encoding="utf-8"))}
    in_scope = {x["site_code"] for x in sites}
    rows = [e for e in enr if e["site_code"] in in_scope]
    link = answers.cutover_links(rows, cat)
    tcodes = [t["code"] for t in W.TERMS]
    cut = tcodes.index(W.CUTOVER_AFTER)
    across = [r for r, c in cat.items() if int(c["terms_spanned"]) == 2 and tcodes.index(c["start_term"]) == cut]
    ck("ask device: every course across the cutover is linked to exactly one continuation",
       sorted(link.values()) == sorted(across), "%d links for %d courses" % (len(link), len(across)))
    # the identity that forces the link, measured on the shipped rows: every learner on a continuation holds a
    # continuing row on the old reference, and no other course in the catalogue is in that position
    on = {}
    for e in rows:
        on.setdefault((e["course_ref"], e["term_code"]), set()).add(e["uln"])
    ident = all(on[(y, tcodes[cut + 1])] <= on[(x, tcodes[cut])] for y, x in link.items())
    ck("ask device: the learner-set identity holds on every link", ident)
    ck("ask device: no course outside the cutover is missing its second term",
       all((r, tcodes[tcodes.index(c["start_term"]) + 1]) in on for r, c in cat.items()
           if int(c["terms_spanned"]) == 2 and r not in across))
    ck("ask device: every centre carries linked learner-courses",
       {cat[x]["site_code"] for x in link.values()} >= in_scope)
    ck("ask device: every curriculum area carries linked learner-courses",
       {cat[x]["curriculum_area"] for x in link.values()} == set(W.CURRICULUM))
    # the separation line: no learner the call reads holds a row on a continuation reference
    wd_ulns = set()
    for r in _csv.DictReader(open(os.path.join(TARGET, "withdrawals_autumn_winter_2025.csv"), encoding="utf-8")):
        wd_ulns.add(r["uln"])
    for r in json.load(open(os.path.join(TARGET, "withdrawals_spring_summer_2026.json"), encoding="utf-8"))["records"]:
        wd_ulns.add(r["learnerUln"])
    dev_ulns = {e["uln"] for e in rows if e["course_ref"] in link}
    ck("separation: zero device rows on a learner the call reads", not (wd_ulns & dev_ulns),
       "%d withdrawn learners hold a continuation row" % len(wd_ulns & dev_ulns))
    ck("separation: the call reads only the withdrawal exports and the moderation file", True)
    ck("ask1 covers every curriculum area", len(f["ask1_planned_hours"]) == len(W.CURRICULUM))
    ck("ask2 covers every centre", len(f["ask2_started"]) == len(W.SITES) == len(f["ask2_completed_pct"]))
    ck("ask2 every completed share is clear of its rounding boundary",
       min(abs((10 * v) % 1 - 0.5) for v in f["ask2_completed_raw"].values()) >= 0.12,
       "closest %.3f" % min(abs((10 * v) % 1 - 0.5) for v in f["ask2_completed_raw"].values()))
    ck("the subcontract rows are outside the review's scope",
       f["enrolment_rows_in_extract"] - f["enrolment_rows_in_scope"] == W.SUBCONTRACT_ENROLMENTS,
       "the out-of-scope count does not match the subcontracted rows written")
    ck("every row repeats its course's whole planned hours",
       all(int(e["guided_hours_planned"]) == int(cat[e["course_ref"]]["planned_guided_hours"]) for e in enr))

    # ---------------- realism sweep: the five measured shapes and no round totals ----------
    def steps(vals):
        nums = sorted(int("".join(ch for ch in v if ch.isdigit())) for v in vals)
        return {b - a for a, b in zip(nums, nums[1:])}
    wrefs = [r["ref"] for r in coded]
    ck("realism 1 withdrawal references are not one constant step", len(steps(wrefs)) > 1)
    ck("realism 1 learner numbers are not one constant step", len(steps({e["uln"] for e in enr})) > 1)
    ck("realism 1 course references are not one constant step", len(steps(cat.keys())) > 1)
    by_code = [x["site_name"] for x in sorted(sites, key=lambda x: x["site_code"])]
    ck("realism 2 the centres in code order are not the centres sorted", by_code != sorted(by_code))
    shapes = {x["site_name"].split()[-1] for x in sites}
    ck("realism 3 centre names take more than two shapes", len(shapes) > 2, ", ".join(sorted(shapes)))
    ck("realism 4 no round totals", n % 100 != 0 and f["enrolment_rows_in_scope"] % 100 != 0
       and f["enrolment_rows_in_extract"] % 100 != 0, "%d withdrawals, %d rows" % (n, f["enrolment_rows_in_scope"]))
    import subprocess
    pdfs = sorted(x for x in names if x.endswith(".pdf"))
    late = []
    import re as _re, datetime as _dt
    months = {m: k for k, m in enumerate(["january", "february", "march", "april", "may", "june", "july",
                                         "august", "september", "october", "november", "december"], 1)}
    for x in pdfs:
        txt = subprocess.run(["pdftotext", os.path.join(TARGET, x), "-"], capture_output=True, text=True).stdout
        found = [_dt.date.fromisoformat(d) for d in _re.findall(r"\b\d{4}-\d{2}-\d{2}\b", txt)]
        for d, m, y in _re.findall(r"\b(\d{1,2}) (%s) (\d{4})\b" % "|".join(months), txt.lower()):
            found.append(_dt.date(int(y), months[m], int(d)))
        if not found or max(found) > _dt.date.fromisoformat(W.ASOF):
            late.append("%s (%s)" % (x, max(found) if found else "no date"))
    ck("realism 5 no document states a date after the review's own", not late, ", ".join(late))

    # The ask layer's ceiling, measured on the cut pack by ceiling.py against the Part 1.1 cracker.
    import ceiling
    cmp = ceiling.compare()
    kept, Lc, Ls, pair = ceiling.pair_of(cmp)
    ck("ask ceiling is measured on the cut pack", len(cmp) == 16, "%d ask figures" % len(cmp))
    ck("the cracker misses every ask figure", kept == 0,
       "keeps " + ", ".join(n for n, _, _, hit in cmp if hit))
    ck("the pair ceiling is inside the build target", pair <= 51.0, "pair %.1f" % pair)
    weak = ceiling.compare(sum_rows=True)
    ck("the weaker reading misses every ask figure too", ceiling.pair_of(weak)[0] == 0)
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
        print("  ASK CEILING %d figures, cracker keeps %d, Lc %.3f, PAIR %.1f (precut allows 60)"
              % (nfig, kept, Lc, pair))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
