"""The generator's own oracle. Every number the build rests on is asserted here against the clean
truth and against the shipped bundle, including the client's three rules, every semantic-fork row and
the neutrality of every Layer 1 item.

    python3 task202/generator/checks.py          (on the pack already in target/)
"""
import csv
import io
import os
import re
import sys
import zipfile

import numpy as np
from openpyxl import load_workbook

import build as B
import params as P
import records as RC
import sim
import solve
import writeup as WU

N = 0
FAIL = []


def ok(label, cond, note=""):
    global N
    N += 1
    if not cond:
        FAIL.append("%s %s" % (label, note))
        print("  FAIL %s %s" % (label, note))
    return cond


def eq(label, a, b, tol=0.0, note=""):
    return ok(label, abs(float(a) - float(b)) <= tol, "%s: %r vs %r %s" % (note, a, b, note))


# ------------------------------------------------------------------ readers for the shipped pack
def text_of(path, flat=True):
    """Every shipped format read back through one helper, so the pack is read one way only.
    Whitespace is collapsed, because a sentence filed in a PDF is laid out across lines."""
    if path.endswith(".pdf"):
        from pypdf import PdfReader
        raw = "\n".join((pg.extract_text() or "") for pg in PdfReader(path).pages)
        return re.sub(r"\s+", " ", raw) if flat else raw
    if path.endswith(".xlsx"):
        out = []
        wb = load_workbook(path, read_only=True, data_only=True)
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                out.append(" ".join("" if c is None else str(c) for c in row))
        return re.sub(r"[ \t]+", " ", "\n".join(out))
    return open(path, encoding="utf-8", errors="replace").read()


def pack_text(target):
    return {f: text_of(os.path.join(target, f)) for f in sorted(os.listdir(target))}


# ------------------------------------------------------------------ the checks
def run(target, world, fig, golden_dir):
    global N, FAIL
    N, FAIL = 0, []
    W = world["W"] if "W" in world else world
    R = world["R"]
    mean, cnt, shape = W["mean"], W["cnt"], W["shape"]
    files = sorted(os.listdir(target))
    txt = pack_text(target)

    # ---------------------------------------------------------- input gates
    ok("gate.files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("gate.formats", len(fmts) >= 3, sorted(fmts))
    rows = {}
    for f in files:
        if f.endswith(".csv"):
            rows[f] = sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1
    ok("gate.big_file", max(rows.values()) >= 25000, "largest %d rows" % max(rows.values()))
    ok("gate.big_is_portal", max(rows, key=rows.get) == B.FILES["portal"], max(rows, key=rows.get))
    ok("gate.distractors", len(B.DISTRACTORS) >= 2, B.DISTRACTORS)
    for k in B.DISTRACTORS:
        ok("gate.distractor_name_clean", "distract" not in B.FILES[k].lower(), B.FILES[k])
    ok("gate.no_answer_key", not any(re.search(r"is_correct|should_exclude|ceiling_php|referred_share",
                                               t, re.I) for t in txt.values()))
    ok("gate.manifest_licence", all("Foundation record" in l for l in
                                    [r["licence"] for r in csv.DictReader(
                                        open(os.path.join(target, B.FILES["manifest"]), encoding="utf-8"))]))

    # ---------------------------------------------------------- R1: the field's raw material ships
    por = WU.read_portal(os.path.join(target, B.FILES["portal"]),
                         WU.read_crosswalk(os.path.join(target, B.FILES["xwalk"])))
    ok("R1.award_level_rows_ship", len(por) > 10000, "%d portal award rows in the window" % len(por))
    ok("R1.cell_averages_ship", len(cnt) == 528, len(cnt))
    hdr = open(os.path.join(target, B.FILES["portal"]), encoding="utf-8").readline()
    ok("R1.no_deciding_quantity_column",
       not any(c in hdr for c in ("ceiling", "referred", "share", "shape", "ratio")), hdr.strip())
    ok("R1.no_shipped_ceiling", not any(re.search(r"referral ceiling (of|is|at) PHP", t) for t in txt.values()))
    ok("R1.decisive_reads_both",
       len({(c, b) for c, b, a in por}) < len(cnt), "portal covers only its own cells")

    # ---------------------------------------------------------- R3a/R3b: the analyst test
    L = solve.ladder(W)
    G = L["R6"]
    eq("R3a.default_path_files_the_named_wrong_answer", L["R1"], 5800)
    eq("R3b.decisive_step_alone_files_the_golden", G, 7800)
    ok("R3b.default_is_wrong_by", abs(G - L["R1"]) >= 1000, "%d pesos" % (G - L["R1"]))
    for r, lo in (("R2", 500), ("R3", 500), ("R4", 500), ("R5a", 500), ("R5b", 500)):
        ok("R3b.rung_%s_separated" % r, abs(L[r] - G) >= lo,
           "%s at %d, %+d pu" % (r, L[r], (L[r] - G) // 100))
    ok("R3b.every_rung_distinct", len({L[r] for r in solve.ROUTES + ["R6"]}) == len(solve.ROUTES) + 1,
       sorted(L[r] for r in solve.ROUTES + ["R6"]))
    eq("R3b.correct_family_converges", L["Rmix"], G, 0, "a correctly specified two-component fit")

    # ---------------------------------------------------------- R3c: no plant
    amt = np.array([a["amount"] for a in W["win"]], float)
    ok("R3c.amounts_mostly_distinct", len(set(amt.tolist())) > 0.90 * len(amt),
       "%d distinct of %d" % (len(set(amt.tolist())), len(amt)))
    seq = [a["amount"] for a in sorted(W["por"], key=lambda a: (a["paid"], a["partner"], a["amount"]))]
    runs = {}
    for i in range(len(seq) - 2):
        runs[(seq[i], seq[i + 1], seq[i + 2])] = runs.get((seq[i], seq[i + 1], seq[i + 2]), 0) + 1
    ok("R3c.no_repeated_run_of_amounts", max(runs.values()) == 1,
       "a run of three amounts occurs %d times" % max(runs.values()))
    sets = {}
    for a in W["win"]:
        sets.setdefault(a["partner"], []).append(a["amount"])
    sig = [tuple(sorted(v)) for v in sets.values()]
    ok("R3c.no_partner_shares_an_amount_set", len(set(sig)) == len(sig),
       "%d distinct of %d partners" % (len(set(sig)), len(sig)))
    mc = {}
    for a in W["awards"]:
        mc[a["month"]] = mc.get(a["month"], 0) + 1
    ok("R3c.no_identical_period_counts", len(set(mc.values())) >= len(mc) - 1, len(set(mc.values())))
    ok("R3c.no_memo_arguing_a_figure",
       not any(re.search(r"we (recommend|propose|suggest)|should be set at", t, re.I) for t in txt.values()))

    # ---------------------------------------------------------- the goodness of fit that closes the family
    from scipy.stats import norm as _n, gamma as _g
    xs = np.sort(shape)
    n = len(xs)
    ecdf = np.arange(1, n + 1) / n
    crit = 1.36 / np.sqrt(n)
    cv = float(shape.std(ddof=1) / shape.mean())
    v = np.log(1 + cv ** 2)
    kk = 1.0 / cv ** 2
    ks_ln = float(np.abs(_n.cdf((np.log(xs) + 0.5 * v) / np.sqrt(v)) - ecdf).max()) / crit
    ks_ga = float(np.abs(_g.cdf(xs * kk, kk) - ecdf).max()) / crit
    pi, mu, sd = L["_mix_params"]
    ks_mix = float(np.abs(sum(pi[k] * _n.cdf((np.log(xs) - mu[k]) / sd[k]) for k in range(2)) - ecdf).max()) / crit
    ok("fit.lognormal_refused", ks_ln > 5, "%.1f x critical" % ks_ln)
    ok("fit.gamma_refused", ks_ga > 5, "%.1f x critical" % ks_ga)
    ok("fit.two_component_accepted", ks_mix < 1.5, "%.2f x critical" % ks_mix)
    pl, ps = [], []
    part = np.array([a["partner"] for a in W["porwin"]])
    pam = np.array([a["amount"] for a in W["porwin"]], float)
    for p in sorted(set(part.tolist())):
        sel = part == p
        pl.append(float(np.mean([mean[(p, bb)] for bb in P.BANDS if (p, bb) in mean])))
        ps.append(float(pam[sel].std(ddof=1)))
    ok("fit.spread_scales_with_level", np.corrcoef(pl, ps)[0, 1] > 0.9,
       "corr %.3f" % np.corrcoef(pl, ps)[0, 1])

    # ---------------------------------------------------------- clause 9's own margin
    s0 = solve.share_cells(G, mean, cnt, shape)
    s1 = solve.share_cells(G - 100, mean, cnt, shape)
    ok("clause9.at_or_below", s0 <= P.COMMITTED_SHARE, "%.6f" % s0)
    ok("clause9.one_step_down_above", s1 > P.COMMITTED_SHARE, "%.6f" % s1)
    ok("clause9.clearance", (P.COMMITTED_SHARE - s0) / (s1 - s0) > 0.15, "%.2f of the step" % ((P.COMMITTED_SHARE - s0) / (s1 - s0)))
    ok("clause9.excess", (s1 - P.COMMITTED_SHARE) / (s1 - s0) > 0.15, "%.2f of the step" % ((s1 - P.COMMITTED_SHARE) / (s1 - s0)))
    mono = [solve.share_cells(c, mean, cnt, shape) for c in range(5000, 11001, 100)]
    ok("clause9.monotone", all(mono[i] >= mono[i + 1] - 1e-12 for i in range(len(mono) - 1)))
    ok("clause9.lowest_is_unique", all(solve.share_cells(c, mean, cnt, shape) > P.COMMITTED_SHARE
                                       for c in range(G - 500, G, 100)))

    # ---------------------------------------------------------- the semantic fork table
    # SF1 the scheme's awards: all accredited partners, or only the portal partners
    pc = {k: v for k, v in cnt.items() if W["parts"][k[0]]["portal"]}
    pm = {k: mean[k] for k in pc}
    sf1 = solve.lowest(lambda c: solve.share_cells(c, pm, pc, shape))
    ok("SF1.portal_only_population_differs", abs(sf1 - G) >= 500, "%d" % sf1)
    ok("SF1.closed_by_clause", "awards of all accredited partners" in txt[B.FILES["policy"]])
    # SF2 the window
    ok("SF2.window_filed", "twelve months to 31 March 2027" in txt[B.FILES["policy"]])
    ok("SF2.award_month_is_payment_month",
       all(a["month"] == (a["paid"].year, a["paid"].month) for a in W["awards"]))
    # SF3 which claims measure the shape: the window, or the portal's whole 27 months
    sh27 = np.array([a["amount"] / mean[(a["partner"], a["band"])] for a in W["por"]
                     if (a["partner"], a["band"]) in mean], float)
    sf3 = solve.lowest(lambda c: solve.share_cells(c, mean, cnt, sh27 / sh27.mean()))
    ok("SF3.pre_window_claims_differ_by_record",
       all(a["component"] not in ("SHL", "EQP") for a in W["por"] if a["month"] < P.CAPITAL_FROM),
       "no capital component before the amendment")
    ok("SF3.amendment_shipped", "1 July 2025" in txt[B.FILES["policy"]]
       and "SHL" in txt[B.FILES["policy"]])
    ok("SF3.alternative_moves_so_the_record_decides", abs(sf3 - G) >= 100, "%d" % sf3)
    # SF4 the shape pooled or per band
    def grouped(c, gmap, arrs):
        above = tot = 0.0
        for k in sorted(cnt):
            s = arrs[gmap(k)]
            above += cnt[k] * (1.0 - np.searchsorted(s, solve.band_ceiling(c, k[1]) / mean[k], side="right") / len(s))
            tot += cnt[k]
        return above / tot
    band = np.array([a["band"] for a in W["porwin"]])
    arrs = {b: np.sort(shape[band == b]) for b in P.BANDS}
    sf4 = solve.lowest(lambda c: grouped(c, (lambda k: k[1]), arrs))
    eq("SF4.per_band_shape_same_call", sf4, G, 0)
    lv = {p: float(np.mean([mean[(p, bb)] for bb in P.BANDS if (p, bb) in mean])) for p in sorted({k[0] for k in cnt})}
    ter = np.quantile([lv[p] for p in sorted(set(part.tolist()))], [1 / 3, 2 / 3])
    tof = lambda x: 0 if x <= ter[0] else (1 if x <= ter[1] else 2)
    tarr = {t: np.sort(shape[np.isin(part, [p for p in sorted(set(part.tolist())) if tof(lv[p]) == t])])
            for t in (0, 1, 2)}
    sf4b = solve.lowest(lambda c: grouped(c, (lambda k: tof(lv[k[0]])), tarr))
    eq("SF4.per_level_tercile_shape_same_call", sf4b, G, 0)
    for b in P.BANDS:
        sub = shape[band == b]
        ok("SF4.band_%d_shape_homogeneous" % b,
           abs(float(np.quantile(sub, 0.94)) / float(np.quantile(shape, 0.94)) - 1) < 0.12,
           "%.3f" % (float(np.quantile(sub, 0.94)) / float(np.quantile(shape, 0.94))))
    # SF5 rounding up
    ok("SF5.rounded_up_filed", "rounded up to the nearest one hundred pesos" in txt[B.FILES["policy"]])
    eq("SF5.band2_ceiling_is_rounded_up", solve.band_ceiling(G, 2), 5600)
    ok("SF5.round_down_would_differ", 100 * int(G * P.SCALE3[2] / 100000) != solve.band_ceiling(G, 2))
    # SF6 the lowest qualifying ceiling
    ok("SF6.lowest_filed", "the lowest amount" in txt[B.FILES["policy"]])
    # SF7 share of awards, not of value
    ok("SF7.share_of_awards_filed", "share of the scheme's awards" in txt[B.FILES["policy"]])
    fv = solve.figures_for(G, W)
    ok("SF7.value_share_differs", abs(fv["referred_value_share"] - fv["referred_share"]) > 5,
       "%.1f vs %.1f" % (fv["referred_value_share"], fv["referred_share"]))
    # SF8 band 6 is six or more
    ok("SF8.open_band_filed", "6 or more persons" in txt[B.FILES["policy"]])
    eq("SF8.band6_factor_at_six", P.SCALE3[6] / 1000.0, round((6 / 4) ** 0.5, 3), 1e-9)
    ok("SF8.sizes_above_six_exist", max(a["size"] for a in W["win"]) > 6,
       max(a["size"] for a in W["win"]))
    # SF9 the normalisation of the shape is a no-op
    raw = np.array([a["amount"] / mean[(a["partner"], a["band"])] for a in W["porwin"]], float)
    eq("SF9.raw_ratios_average_one", raw.mean(), 1.0, 1e-12)
    eq("SF9.normalisation_is_a_no_op", solve.lowest(lambda c: solve.share_cells(c, mean, cnt, raw)), G, 0)
    # SF10 the superseded months
    ok("SF10.rule_filed", "supersedes the preliminary return in full" in txt[B.FILES["policy"]])
    recon = _portal_reconciliation(target, W, R)
    ok("SF10.portal_matches_revised", recon["revised_matches"], recon)
    ok("SF10.portal_refuses_prelim", recon["prelim_mismatches"] > 0, recon)
    # SF11 the partner accredited mid-window and the one that withdrew
    ok("SF11.lifecycle_filed", "accredited or withdrawn during them" in txt[B.FILES["policy"]])
    newp = [pt for pt in W["parts"] if pt["first_month"] != P.RETURNS_FROM]
    exitp = [pt for pt in W["parts"] if pt["last_month"] != (2027, 3)]
    ok("SF11.one_accredited_mid_window", len(newp) == 1 and newp[0]["first_month"] == (2026, 8))
    ok("SF11.one_withdrew_mid_window", len(exitp) == 1 and exitp[0]["last_month"] == (2026, 10))
    ok("SF11.both_inside_the_window",
       all((P.WINDOW_FROM <= a["month"] <= P.WINDOW_TO) or not (P.WINDOW_FROM <= a["month"] <= P.WINDOW_TO)
           for a in W["win"]))
    ok("SF11.new_partner_has_window_awards", any(a["partner"] == newp[0]["idx"] for a in W["win"]))
    ok("SF11.exited_partner_has_window_awards", any(a["partner"] == exitp[0]["idx"] for a in W["win"]))
    # SF12 the published summary is in thousands
    ok("SF12.units_stated", "thousands of pesos" in txt[B.FILES["summary"]])
    ok("SF12.summary_not_in_the_solve_path", B.FILES["summary"] in [B.FILES[k] for k in B.DISTRACTORS])
    return _rest(target, world, fig, golden_dir, txt, L, G, mean, cnt, shape, fv)


def _portal_reconciliation(target, W, R):
    """For the reopened months the portal's own awards match the revised return and not the
    preliminary one, which is what refuses counting both."""
    ws = load_workbook(os.path.join(target, B.FILES["ret2627"]), read_only=True, data_only=True).active
    grid = [[c for c in r] for r in ws.iter_rows(values_only=True)]
    h = next(i for i, r in enumerate(grid) if r and any(str(c).strip() == "claim_month" for c in r if c))
    cols = {str(c).strip(): j for j, c in enumerate(grid[h]) if c}
    pid = {R.ledger[pt["idx"]]: pt["idx"] for pt in R.parts}
    pw = {}
    for a in W["por"]:
        k = (a["month"], a["partner"], a["band"])
        c = pw.setdefault(k, [0, 0.0])
        c[0] += 1
        c[1] = round(c[1] + a["amount"], 2)
    rev_ok, pre_bad = True, 0
    for r in grid[h + 1:]:
        if not r or r[cols["claim_month"]] is None:
            continue
        mo = WU._month(r[cols["claim_month"]])
        if mo not in P.REVISED_MONTHS:
            continue
        code = str(r[cols["partner_code"]]).strip()
        if code not in pid or not W["parts"][pid[code]]["portal"]:
            continue
        k = (mo, pid[code], WU._band(r[cols["household_size_band"]]))
        if k not in pw:
            continue
        n, tot = int(r[cols["awards"]]), float(r[cols["total_claimed_php"]])
        st = str(r[cols["return_status"]]).strip()
        same = (n == pw[k][0] and abs(tot - pw[k][1]) < 0.01)
        if st == "REVISED":
            rev_ok = rev_ok and same
        elif not same:
            pre_bad += 1
    return {"revised_matches": rev_ok, "prelim_mismatches": pre_bad}


def _rest(target, world, fig, golden_dir, txt, L, G, mean, cnt, shape, fv):
    W = world["W"]
    R = world["R"]
    # ---------------------------------------------------------- closure axes that need a number
    eq("axis10.rounding_once", solve.band_ceiling(G, 5), 8800)
    import math
    for b in P.BANDS:
        exact = 100 * math.ceil(G * math.sqrt(b / 4.0) / 100 - 1e-9)
        eq("axis13.three_decimal_factor_agrees_with_the_root_band_%d" % b,
           solve.band_ceiling(G, b), exact, 0)
    perms = []
    rng = np.random.default_rng(7)
    for _ in range(6):
        idx = rng.permutation(len(shape))
        perms.append(solve.lowest(lambda c: solve.share_cells(c, mean, cnt, shape[idx])))
    ok("axis14.row_order_invariant", len(set(perms)) == 1 and perms[0] == G, perms)
    ok("axis20.ceilings_are_whole_hundreds",
       all(solve.band_ceiling(G, b) % 100 == 0 for b in P.BANDS))
    srt = np.sort(shape)
    thr = np.array([solve.band_ceiling(G, k[1]) / mean[k] for k in sorted(cnt)])
    j = np.clip(np.searchsorted(srt, thr), 1, len(srt) - 1)
    gap = float(np.minimum(np.abs(srt[j] - thr), np.abs(srt[j - 1] - thr)).min())
    ok("axis9.no_ratio_sits_on_a_threshold", gap > 1e-9, "nearest ratio %.3e away" % gap)
    strict = solve.share_cells(G, mean, cnt, shape)
    nonstrict = float(sum(cnt[k] * (1.0 - np.searchsorted(np.sort(shape), solve.band_ceiling(G, k[1]) / mean[k], side="left") / len(shape))
                          for k in sorted(cnt)) / sum(cnt.values()))
    eq("axis9.strict_and_nonstrict_agree", strict, nonstrict, 1e-12)
    ddof0 = float(shape.std(ddof=0) / shape.mean())
    eq("axis19.cv_reading_invariant", round(ddof0, 2), fig["cv"], 1e-9)

    # ---------------------------------------------------------- mess neutrality, item by item
    import mess_check as MC
    neu = MC.all_items(target)
    for k, v in sorted(neu.items()):
        eq("mess.%s_call_unchanged" % k, v["call"], G, 0)
        eq("mess.%s_overall_share_unchanged" % k, round(v["share"], 2), fig["share_pct"], 1e-9)
        if k != "both_counted":
            eq("mess.%s_band_figures_unchanged" % k, round(v["b4"], 1),
               fig["bands"]["4"]["referred_share"], 1e-9)
    # counting a superseded return as well as its revision breaks clause 4.2 rather than mishandling
    # the mess, and the asks are meant to turn on it: it must move an ask figure and nothing else
    ok("ask.device_superseded_return_moves_a_band_figure",
       round(neu["both_counted"]["b4"], 1) != fig["bands"]["4"]["referred_share"],
       "band 4 share %.4f against %.1f" % (neu["both_counted"]["b4"], fig["bands"]["4"]["referred_share"]))
    eq("ask.device_superseded_return_leaves_the_call", neu["both_counted"]["call"], G, 0)

    # ---------------------------------------------------------- distractor deletion
    for k in B.DISTRACTORS:
        ok("distractor.%s_unused" % k, True, B.FILES[k])
    f2 = WU.figures(target, B.FILES)
    eq("distractor.deletion_leaves_the_call", f2["call"], fig["call"], 0)
    for b in P.BANDS:
        eq("distractor.deletion_leaves_band_%d" % b, f2["bands"][str(b)]["referred_share"],
           fig["bands"][str(b)]["referred_share"], 1e-9)

    # ---------------------------------------------------------- the pack reproduces the golden
    eq("pack.call_from_bundle", f2["call"], G, 0)
    eq("pack.default_from_bundle", f2["default_call"], L["R1"], 0)
    eq("pack.awards_from_bundle", f2["awards"], len(W["win"]), 0)
    eq("pack.cells_from_bundle", f2["cells"], len(cnt), 0)
    eq("pack.shape_rows_from_bundle", f2["portal_window_rows"], len(shape), 0)
    for b in P.BANDS:
        eq("pack.band_%d_ceiling" % b, f2["bands"][str(b)]["ceiling"], solve.band_ceiling(G, b), 0)
        eq("pack.band_%d_factor" % b, f2["bands"][str(b)]["factor"], P.SCALE3[b] / 1000.0, 1e-9)

    # ---------------------------------------------------------- every graded figure is mid-cell
    tight = (None, 9e9)
    for b in P.BANDS:
        for key, unit in (("referred_share", 0.1), ("referred_value_share", 0.1)):
            v = fv["bands"][b][key]
            e = unit / 2 - abs(v - round(v / unit) * unit)
            ok("bin.band_%d_%s" % (b, key), e > 0.15 * (unit / 2),
               "%.4f, edge %.4f = %.2f of the half-cell" % (v, e, e / (unit / 2)))
            if e / (unit / 2) < tight[1]:
                tight = ("band %d %s" % (b, key), e / (unit / 2))
    print("  tightest graded figure: %s at %.2f of its half-cell" % tight)

    # ---------------------------------------------------------- realism sweep
    amt = [a["amount"] for a in W["win"]]
    ok("real.no_round_total", abs(sum(amt) - round(sum(amt), -3)) > 1, "%.2f" % sum(amt))
    ok("real.amounts_not_round", sum(1 for x in amt if abs(x - round(x, -2)) < 0.005) < 0.02 * len(amt))
    ok("real.no_uniform_partner_counts", len({sum(1 for a in W["win"] if a["partner"] == p)
                                              for p in range(len(W["parts"]))}) > 60)
    names = [pt["name"] for pt in W["parts"]]
    ok("real.no_placeholder_names", not any(re.search(r"\b(Acme|Company [A-Z]|Partner [A-Z]|John Doe|Test|Sample)\b", n) for n in names))
    ok("real.personas_from_guard", {v[0] for v in P.PEOPLE.values()} <=
       {"Kathryn Newman", "Robert Gonzalez", "Erica Costa", "Ronald Rosales", "Barry Rose",
        "James Snyder", "Cheryl Chase", "Alexandra Melton", "Steven Espinoza", "John King"})
    ok("real.no_em_dash", not any("—" in t for t in txt.values()))
    ok("real.distinct_partner_names", len(set(names)) == len(names))
    # document control dates against the events they describe
    pol = txt[B.FILES["policy"]]
    ok("doc.policy_dates_coherent", "12 February 2027" in pol and "1 April 2027" in pol)
    ok("doc.amendment_before_approval", pol.index("1 July 2025") < len(pol))
    ok("doc.extract_after_last_record",
       max(a["paid"] for a in W["awards"]).isoformat() <= P.EXTRACT_DATE.isoformat())
    ok("doc.no_date_after_extract",
       not re.search(r"\b(2027-0[5-9]|2027-1[0-2]|2028)-\d\d\b", txt[B.FILES["portal"]]))

    # ---------------------------------------------------------- the positive controls
    ok("control.policy_text_readable", "Household Relief Grant" in pol and len(pol) > 2000,
       "%d characters extracted" % len(pol))
    ok("control.summary_text_readable", "Annual Report 2025/26" in txt[B.FILES["summary"]],
       "%d characters" % len(txt[B.FILES["summary"]]))
    ok("control.returns_readable", "partner_code" in txt[B.FILES["ret2627"]])
    ok("control.clause9_present", "9.1 For each scheme year" in pol)
    ok("control.scheduleB_present", "B.2 The factor for a band" in pol)
    ok("control.scheduleB_tabulates_no_factor",
       not re.search(r"0\.500|0\.707|0\.866|1\.118|1\.225", pol),
       "a tabulated factor is a graded answer printed in the pack")
    for b in P.BANDS:
        ok("leak.factor_band_%d_absent_from_the_pack" % b,
           not any(("%.3f" % (P.SCALE3[b] / 1000.0)) in t for t in txt.values()),
           "%.3f" % (P.SCALE3[b] / 1000.0))

    # ---------------------------------------------------------- no leak of the decisive step
    for f, t in txt.items():
        ok("leak.%s_no_within_partner" % f,
           not re.search(r"within[- ]partner|award shape|spread about|coefficient of variation", t, re.I), f)
    ok("leak.no_method_in_the_pack",
       not re.search(r"rebuild|reconstruct the distribution|per[- ]award distribution", pol, re.I))

    # ---------------------------------------------------------- H9: the registers know every file
    man = [r["file_name"] for r in csv.DictReader(
        open(os.path.join(target, B.FILES["manifest"]), encoding="utf-8"))]
    shipped = set(os.listdir(target))
    ok("register.manifest_is_the_shipped_set", set(man) == shipped,
       "manifest %d vs shipped %d: %s" % (len(man), len(shipped),
                                          sorted(shipped.symmetric_difference(man))))
    dct = txt[B.FILES["dict"]]
    for k in B.PACK:
        if k in ("dict", "policy", "summary", "request"):
            continue
        ok("register.dictionary_names_%s" % k, B.FILES[k] in dct, B.FILES[k])
    # H4: the golden folder is exactly the deliverables
    import golden as _G
    ok("ship.golden_is_the_deliverables", sorted(os.listdir(golden_dir)) == sorted([_G.XLSX, _G.PDF]),
       sorted(os.listdir(golden_dir)))
    # the archive is cut after these checks run, so its freshness is asserted in make.py where it
    # is cut (H7: a freshness assertion rather than build order)

    # ---------------------------------------------------------- the goldens
    import golden as GD
    for f in (GD.XLSX, GD.PDF):
        ok("golden.%s_exists" % f, os.path.exists(os.path.join(golden_dir, f)))
    gx = text_of(os.path.join(golden_dir, GD.XLSX))
    gp = text_of(os.path.join(golden_dir, GD.PDF))
    ok("golden.call_in_workbook", "7800" in gx.replace(",", "") or "7,800" in gx)
    ok("golden.call_in_paper", "PHP 7,800" in gp, gp[:0])
    for b in P.BANDS:
        c = "{:,}".format(solve.band_ceiling(G, b))
        ok("golden.band_%d_ceiling_in_paper" % b, c in gp, c)
    ok("golden.chart_embedded", os.path.getsize(os.path.join(golden_dir, GD.PDF)) > 60000)
    ok("golden.no_working_png", not any(f.endswith(".png") for f in os.listdir(golden_dir)))

    if FAIL:
        print("\n%d FAILED:" % len(FAIL))
        for f in FAIL:
            print("   " + f)
        raise AssertionError("%d checks failed" % len(FAIL))
    return N


if __name__ == "__main__":
    import make
    TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    w = B.run(os.path.join(TASK, "target"), documents=False) if "--rebuild" in sys.argv else None
    import json
    fig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    world = {"W": sim.make()}
    world["R"] = RC.Records(world["W"])
    print("checks: %d assertions passed" % run(os.path.join(TASK, "target"), world, fig,
                                               os.path.join(TASK, "golden")))
