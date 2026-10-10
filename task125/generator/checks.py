"""Every assertion of the build (dataset-generation 11.7, determinism-check B, supplemental-stumping Part 8,
reduce-house-fixes H1/H4/H9/H16). Run by build.py after the pack is written. Prints one line per assertion
and a JSON record of the figures to stdout's tail."""
import collections
import datetime as dt
import itertools
import json
import re
import zipfile
from collections import Counter
from pathlib import Path

import params as PR
import screen as S
import fernhollow as FHM
from world import DEPT_ORDER, FLAGGED_2526

RESULTS = []
REC = {}


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print("%s  %s%s" % ("PASS" if cond else "FAIL", name, ("  [" + str(detail) + "]") if detail else ""))
    return cond


def hundred(x):
    return int(round(x / 100.0)) * 100


def bin_margin(x):
    r = x % 100
    return min(r + 50, 50 - r) if r < 50 else min(r - 50, 150 - r)


# ---------------------------------------------------------------------------------------- plan-year model
def plan_components(W, D, cells, sl="b2dec", hs="runoff", runs=13, hs_term=30, tiers=("SDs", "SDe", "SDc"),
                    lag=False, joint="household"):
    """The routed count for 2027/28 under a forward model, built from the shipped records (the generator's
    path): flat streams carried at their 2025/26 count, Housing Support's instalments per household on a term,
    Shared Lives carers' plan-year amounts under a reading of the closure. joint: how the halves paid to the two
    carers of a joint household are carried ("held" at their current amounts, "household": the household's fee
    re-summed, the step-down placements dropped and halved again, "one": re-summed and paid as one payment,
    "every": every joint household with a step-down guest moved into cell 14)."""
    pays = D["pays"]
    _, by = S.routed_in(pays, cells, S.CORRECT)
    comp = dict(by)
    if ("HS", 14) in cells:
        if hs == "runoff":
            n = 0
            a, b = PR.FY[PR.PLAN]
            for case, ven, label, appr, amt, (y, m) in W.households:
                for i in range(hs_term):
                    if a <= PR.tsp_date(y, m) <= b:
                        n += 1
                    m += 1
                    if m == 13:
                        y, m = y + 1, 1
            comp[("HS", 14)] = 12 * PR.STREAMS["HS_FS14"]["n"] + n
        elif hs == "drop":
            comp[("HS", 14)] = 0
    if ("ASC", 14) in cells:
        k = 0

        def after(combo):
            if sl == "carried":
                return 4 * sum(PR.RATES[g] for g in combo)
            if sl == "b2dec":
                return 4 * sum(PR.RATES[g] for g in combo if g not in tiers)
            if sl == "every":
                return 1464 if any(g.startswith("SD") for g in combo) and len(combo) > 1 else PR.carer_amount(combo)

        for ven, combo in W.carers:
            amt = after(combo)
            if amt and PR.cell_of(amt) == 14:
                # a one-period arrears lag pays the first plan-year run at the pre-closure amount
                k += (runs - 1) if (lag and amt != PR.carer_amount(combo)) else runs
        for va, vb, combo in W.joint:
            if joint == "held" or sl == "carried":
                halves = [PR.joint_half(combo)] * 2
            elif joint == "household":
                halves = [after(combo) // 2] * 2
            elif joint == "one":
                halves = [after(combo)]
            elif joint == "every":
                halves = [1464] * 2 if any(g.startswith("SD") for g in combo) else [PR.joint_half(combo)] * 2
            for h in halves:
                if h and PR.cell_of(h) == 14:
                    k += (runs - 1) if (lag and h != PR.joint_half(combo)) else runs
        comp[("ASC", 14)] = 12 * PR.STREAMS["ASC_DP14"]["n"] + k
    return sum(comp.values()), comp


def grid(W, D):
    out = {}
    for amt, rng in (("net", "pub"), ("net", "dec"), ("gross", "dec")):
        basis = (amt, rng, "excl")
        cnt = D["counts"][basis]
        for cs in ("2526", "2324"):
            cells = S.flagged_cells(cnt, "2025/26" if cs == "2526" else "2023/24", DEPT_ORDER)
            base, by = S.routed_in(D["pays"], cells, basis)
            for hs in ("carried", "runoff"):
                for sl in ("carried", "b2dec", "every"):
                    for jt in ("held", "household"):
                        if sl == "carried" and jt == "household":
                            continue
                        v = base
                        if ("HS", 14) in cells and hs == "runoff":
                            v += plan_components(W, D, {("HS", 14)}, hs="runoff")[1][("HS", 14)] - by[("HS", 14)]
                        if ("ASC", 14) in cells:
                            j = "every" if (sl == "every" and jt == "household") else jt
                            v += plan_components(W, D, {("ASC", 14)}, sl=sl, joint=j)[1][("ASC", 14)] - \
                                by[("ASC", 14)]
                        out[(amt + "-" + rng, cs, hs, sl, jt)] = v
    return out


def check_main(W, D, F):
    pays = D["pays"]
    corr = D["counts"][S.CORRECT]
    # ---- the corpus: survivor and rivals
    st = D["st"]
    misses = {}
    for b in S.BASES:
        stb = S.statements(D["counts"][b], DEPT_ORDER)
        misses[b] = sum(1 for k in st if stb[k] != st[k])
    ok("corpus: gross complete decades, credit notes excluded, reproduces 63 of 63", misses[S.CORRECT] == 0
       and len(st) == 63, "%d figures" % len(st))
    worst = min(v for b, v in misses.items() if b != S.CORRECT)
    ok("corpus: every one of the 11 rival constructions misses at least 6 figures", worst >= 6,
       {"/".join(b): v for b, v in misses.items()})
    REC["corpus_misses"] = {"/".join(b): v for b, v in misses.items()}
    ok("corpus: rung 1 (net complete decades) reproduces exactly the 30 VAT-free figures",
       63 - misses[("net", "dec", "excl")] == 30, 63 - misses[("net", "dec", "excl")])
    ok("corpus: rung 0 (published range) reproduces none of the 63", misses[("net", "pub", "excl")] == 63)
    for b in S.BASES:
        if b == S.CORRECT:
            continue
        tot = [sum(sum(D["counts"][b][(fy, d)].values()) for d in DEPT_ORDER) for fy in PR.SCREEN_YEARS]
        tot0 = [sum(sum(corr[(fy, d)].values()) for d in DEPT_ORDER) for fy in PR.SCREEN_YEARS]
        if any(x == y for x, y in zip(tot, tot0)):
            ok("corpus aggregate: council-wide payments tested differ under rival %s in every year" % "/".join(b),
               False, (tot, tot0))
            break
    else:
        ok("corpus aggregate: council-wide payments tested differ under every rival in every year", True)
    # MAD rounding safety
    edge = min(abs(S.mad(corr[(fy, d)]) * 1e5 % 1 - 0.5) for fy in PR.SCREEN_YEARS for d in DEPT_ORDER)
    ok("statement MADs sit clear of the fifth-decimal rounding edge (1e-8)", edge > 0.001, round(edge, 4))
    # ---- flags
    ok("2025/26 gross screen flags exactly ASC 14, HS 14, HT 49, HT 99, PF 12", D["cells2526"] == FLAGGED_2526,
       sorted(D["cells2526"]))
    ok("2023/24 gross screen flags the same cells plus WE 11 (the run log's cells)",
       D["cells2324"] == FLAGGED_2526 | {("WE", 11)}, sorted(D["cells2324"]))
    lo_f, hi_u = 99.0, 0.0
    for fy in PR.SCREEN_YEARS:
        for d in DEPT_ORDER:
            for c, (f, r) in S.flags(corr[(fy, d)]).items():
                if f:
                    lo_f = min(lo_f, r)
                else:
                    hi_u = max(hi_u, r)
    ok("every flagged cell at least 1.20 of its threshold, every unflagged cell at most 0.86", lo_f >= 1.20 and
       hi_u <= 0.86, "lowest flagged %.3f, highest unflagged %.3f" % (lo_f, hi_u))
    REC["flag_margins"] = (round(lo_f, 3), round(hi_u, 3))
    # ---- rungs
    r2, by2 = S.routed_in(pays, D["cells2526"], S.CORRECT)
    ok("rung 2: 2025/26 flagged-cell payments carried forward = 7,608", r2 == 7608, dict(by2))
    ok("twin pair: ASC 14 and HS 14 each 2,706 in 2025/26", by2[("ASC", 14)] == 2706 and by2[("HS", 14)] == 2706)
    r3, c3 = plan_components(W, D, D["cells2526"], sl="carried")
    r4s, c4s = plan_components(W, D, D["cells2526"], sl="b2dec", joint="held")
    r4, c4 = plan_components(W, D, D["cells2526"], sl="b2dec", joint="household")
    ok("rung 3 (HS run off on 30 instalments, Shared Lives carried) = 5,718", r3 == 5718, r3)
    ok("rung 4 (each carer row decomposed, the joint halves held) = 6,498", r4s == 6498, r4s)
    ok("answer (rung 5, joint households re-summed and halved again) = 6,706 from the shipped records",
       r4 == 6706, {"%s %d" % k: v for k, v in c4.items()})
    sim = W.plan_year()
    routed_sim = Counter()
    for dept, g, d, kind in sim:
        if g >= 100000 and (dept, S.cell_p(g)) in D["cells2526"]:
            routed_sim[(dept, S.cell_p(g))] += 1
    ok("answer equals the world's own forward simulation of 2027/28", sum(routed_sim.values()) == r4 and
       routed_sim == Counter(c4), sum(routed_sim.values()))
    ok("components: ASC 3,694, HS 816, HT 49 792, HT 99 432, PF 12 972",
       c4 == {("ASC", 14): 3694, ("HS", 14): 816, ("HT", 49): 792, ("HT", 99): 432, ("PF", 12): 972})
    ok("answer bin: 6,706 files 6,700, 56 above and 44 below the edges", hundred(r4) == 6700 and
       r4 - 6650 == 56 and 6750 - r4 == 44)
    ok("rung 4 bin: 6,498 files 6,500, a different hundred from the answer", hundred(r4s) == 6500)
    r1, _ = S.routed_in(pays, S.flagged_cells(D["counts"][("net", "dec", "excl")], "2025/26", DEPT_ORDER),
                        ("net", "dec", "excl"))
    r0, _ = S.routed_in(pays, S.flagged_cells(D["counts"][("net", "pub", "excl")], "2025/26", DEPT_ORDER),
                        ("net", "pub", "excl"))
    side = sum(D["b1"].values())
    REC.update(r0=r0, r1=r1, r2=r2, r3=r3, r4=r4s, r5=r4, side=side)
    hund = {"r0": hundred(r0), "r1": hundred(r1), "r2": hundred(r2), "r3": hundred(r3), "r4": hundred(r4s),
            "r5": hundred(r4), "side": hundred(side)}
    ok("every rung and the side cell file a different hundred", len(set(hund.values())) == 7, hund)
    ok("rung 0 and rung 1 sit at least 25 per cent above the answer", r0 > 1.25 * r4 and r1 > 1.25 * r4,
       (r0, r1))
    ok("bracket: rung 3 is 14.7 per cent low, rung 4 3.1 per cent low and rung 2 13.5 per cent high",
       round(100 * (r3 / r4 - 1), 1) == -14.7 and round(100 * (r4s / r4 - 1), 1) == -3.1 and
       round(100 * (r2 / r4 - 1), 1) == 13.5)
    ok("cohort drop worth more than a sixth of the closed-year figure (L4)", (r2 - r3) / r2 > 1 / 6,
       round((r2 - r3) / r2, 3))
    return dict(r0=r0, r1=r1, r2=r2, r3=r3, r4=r4, r4s=r4s, side=side, c4=c4)


def check_grid(W, D, M):
    r4 = M["r4"]
    G = grid(W, D)
    ans = ("gross-dec", "2526", "runoff", "b2dec", "household")
    stop4 = ("gross-dec", "2526", "runoff", "b2dec", "held")
    ok("grid: 60 cells computed, the answer cell is 6,706", len(G) == 60 and G[ans] == r4)
    same = [k for k, v in G.items() if hundred(v) == hundred(r4)]
    ok("grid: only the answer cell files 6,700", same == [ans], same)
    single = {k: v for k, v in G.items() if sum(1 for x, y in zip(k, ans) if x != y) == 1}
    near = sorted((abs(v / r4 - 1), k, v) for k, v in single.items() if k != stop4)
    ok("grid: every single-violation cell but rung 4 sits at least 6 per cent from the answer", near[0][0] >= 0.06,
       [(k, v, round(100 * d, 1)) for d, k, v in near[:3]])
    ok("grid: rung 4 (the joint halves held) files 6,500, 208 below the answer", G[stop4] == M["r4s"] and
       r4 - G[stop4] == 208 and hundred(G[stop4]) == 6500)
    multi = sorted((abs(v / r4 - 1), k, v) for k, v in G.items() if k != ans and k not in single)
    close = [(k, v, round(100 * (v / r4 - 1), 1)) for d, k, v in multi if d < 0.06]
    ok("grid: multi-violation cells within 6 per cent file another hundred",
       all(hundred(v) != hundred(r4) for k, v, _ in close), close)
    REC["grid_close_multi"] = [(list(k), v) for k, v, _ in close]
    net_far = min(v for k, v in G.items() if k[0] != "gross-dec")
    ok("grid: every net-basis and published-range cell sits at least 5 per cent high, in another hundred",
       net_far >= 1.05 * r4 and all(hundred(v) != hundred(r4) for k, v in G.items() if k[0] != "gross-dec"),
       net_far)
    REC["grid_nearest_single"] = [(list(k), v) for d, k, v in near[:4]]
    # separation table
    cells = D["cells2526"]
    sep = {
        "lag12": plan_components(W, D, cells, lag=True)[0],
        "run14": plan_components(W, D, cells, runs=14)[0],
        "std_only": plan_components(W, D, cells, tiers=("SDs",))[0],
        "every": plan_components(W, D, cells, sl="every", joint="every")[0],
        "term24": plan_components(W, D, cells, hs_term=24)[0],
        "term36": plan_components(W, D, cells, hs_term=36)[0],
        "hs_drop": plan_components(W, D, cells, hs="drop")[0],
        "no_runoff": plan_components(W, D, cells, hs="carried")[0],
        "cells2324": G[("gross-dec", "2324", "runoff", "b2dec", "household")],
        "joint_held": plan_components(W, D, cells, joint="held")[0],
        "joint_one": plan_components(W, D, cells, joint="one")[0],
        "joint_every": plan_components(W, D, cells, joint="every")[0],
    }
    for t in (("SDs", "SDe"), ("SDs", "SDc"), ("SDe", "SDc")):
        sep["two_tier_" + "_".join(t)] = plan_components(W, D, cells, tiers=t)[0]
    want = SEP_WANT
    ok("separation table figures as designed", all(sep[k] == v for k, v in want.items()),
       {k: sep[k] for k in sep})
    ok("one-period arrears lag (12 runs) files 6,600, against the rate schedule's four weeks ending on the "
       "payment date", hundred(sep["lag12"]) == 6600)
    ok("every separation cell lands outside the answer's hundred",
       all(hundred(v) != 6700 for k, v in sep.items()), {k: v for k, v in sep.items()})
    REC["separation"] = sep
    return G, sep


SEP_WANT = dict(lag12=6630, run14=6884, std_only=6082, every=7317, term24=6112, term36=7840, hs_drop=5890,
                no_runoff=8596, cells2324=7198, joint_held=6498, joint_one=6524, joint_every=6784,
                two_tier_SDs_SDe=6420, two_tier_SDs_SDc=6368, two_tier_SDe_SDc=6342)


def check_world(W, D, M):
    # term back-test on the completed 2021 round
    per = Counter(c for (c, v, r, a, d, amt) in W.tsp if r == "2021")
    ok("term back-test: every one of the 288 households in the 2021 round received exactly 30 payments",
       len(per) == 288 and set(per.values()) == {30})
    for t in (24, 27, 33, 36):
        if any(v == t for v in per.values()):
            ok("term rival %d reproduces no household" % t, False)
            break
    else:
        ok("term rivals 24, 27, 33 and 36 each reproduce none of the 288", True)
    # TSP spine rows equal the ledger from April 2023
    sp = sorted((p[4], p[5], p[6]) for p in W.pay if p[8] == "TSP")
    lg = sorted((v, d, amt) for (c, v, r, a, d, amt) in W.tsp if d >= PR.SPINE_FROM)
    ok("Tenancy Sustainment rows in the spending file equal the case extract from April 2023", sp == lg, len(sp))
    # decomposition uniqueness
    amts = collections.defaultdict(list)
    for k in (1, 2, 3):
        for ms in itertools.combinations_with_replacement(sorted(PR.RATES), k):
            amts[4 * sum(PR.RATES[g] for g in ms)].append(ms)
    carer_amts = {PR.carer_amount(c) for c, n in PR.COMBOS}
    ok("each of the 19 carer amounts is four times a unique multiset of weekly rates",
       len(carer_amts) == 19 and all(len(amts[a]) == 1 for a in carer_amts))
    alt = 0
    for a in carer_amts:
        for mult in (4.33, 52 / 12):
            for k in (1, 2, 3):
                for ms in itertools.combinations_with_replacement(sorted(PR.RATES), k):
                    if abs(round(mult * sum(PR.RATES[g] for g in ms), 2) - a) < 0.005:
                        alt += 1
    ok("no calendar-month multiplier (weekly x 4.33 or x 52/12) reproduces any carer amount", alt == 0, alt)
    moved = [v for v, c in W.carers if PR.cell_of(PR.carer_amount(c)) != 14 and
             PR.cell_of(PR.carer_amount(c, dt.date(2027, 4, 28)) or 1) == 14]
    ok("lens swap: 60 carers outside cell 14 in every closed period enter it after the closure", len(moved) == 60)
    sl_cells = {PR.cell_of(PR.carer_amount(c)) for v, c in W.carers if v in set(moved)}
    ok("the 60 carers sit in cells 30, 32 and 35 throughout the extract", sl_cells == {30, 32, 35}, sl_cells)
    sdonly = {PR.cell_of(PR.carer_amount(c)) for v, c in W.carers if all(g.startswith("SD") for g in c)}
    ok("first-order closure check finds no step-down payment in a flagged cell (step-down-only carers in 15, 18, 20)",
       sdonly == {15, 18, 20})
    # joint households: the halves are the record, nothing states them
    halves = {PR.joint_half(c) for a, b, c in W.joint}
    ok("no joint half is four times a multiset of up to three weekly rates (no single-carer reading exists)",
       not any(amts.get(h) for h in halves), sorted(halves))
    ok("twice every joint half decomposes uniquely into four weeks of placement rates",
       all(len(amts.get(2 * h, [])) == 1 for h in halves))
    ok("every carer amount is either a single carer's fee or a joint half, never both",
       not halves & carer_amts)
    jv = {}
    for p in W.pay:
        if p[8] == "SLJ":
            jv.setdefault(p[4], set()).add((p[5], p[6]))
    pairs_ok = all(jv[a] == jv[b] and int(b) == int(a) + 1 for a, b, c in W.joint)
    ok("each joint household's two vendors are consecutive numbers paid the identical amount on every run",
       pairs_ok and len(jv) == 2 * len(W.joint))
    single_guest = [c for a, b, c in W.joint if len(c) == 1]
    ok("the split holds with one guest: joint households with a single long-term guest are paid in halves",
       single_guest and all(PR.cell_of(PR.joint_half(c)) == 73 for c in single_guest))
    entr = [(a, b, c) for a, b, c in W.joint if PR.cell_of(PR.joint_half(c, dt.date(2027, 4, 28)) or 1) == 14]
    ok("8 joint households (16 vendors) outside cell 14 in every closed period enter it after the closure",
       len(entr) == 8 and all(PR.cell_of(PR.joint_half(c)) != 14 for a, b, c in entr))
    ok("the entrants are the band 1 plus band 3 households with a step-down guest, halves 2,274, 2,388, 2,514",
       {PR.joint_half(c) for a, b, c in entr} == {2274, 2388, 2514} and
       all(set(c[:2]) == {"B1", "B3"} for a, b, c in entr))
    look = [(a, b, c) for a, b, c in W.joint if any(g.startswith("SD") for g in c) and (a, b, c) not in entr]
    ok("the other joint households with a step-down guest land in cell 13 after the closure",
       look and {PR.cell_of(PR.joint_half(c, dt.date(2027, 4, 28))) for a, b, c in look} == {13})
    held = sum(1 for a, b, c in W.joint if PR.cell_of(PR.joint_half(c)) in (14,))
    ok("no joint half sits in cell 14 in any closed period", held == 0)
    nohalf = [h for h in (PR.joint_half(c) for a, b, c in entr) if amts.get(h - 1464) or amts.get(h - 1484)]
    ok("subtracting a band 2 fee (1,464) or the post-closure half (1,484) from an entrant's half leaves no "
       "four-week rate multiset", not nohalf, nohalf)
    # flatness and one payment per run
    sl = Counter((p[4], p[5]) for p in W.pay if p[8] in ("SL", "SLJ"))
    runs = PR.sl_runs(PR.SPINE_FROM, PR.SPINE_TO)
    nv = 333 + 2 * len(W.joint)
    ok("every Shared Lives carer vendor has exactly one payment in every four-weekly run of the extract",
       len(sl) == nv * len(runs) and set(sl.values()) == {1}, nv)
    amt_by = collections.defaultdict(set)
    for p in W.pay:
        if p[8] in ("SL", "SLJ", "DP14", "TSP"):
            amt_by[p[4]].add(p[6] + p[7])
    ok("every carer, direct payment recipient and household is paid one constant amount throughout the extract",
       all(len(v) == 1 for v in amt_by.values()))
    con = Counter((p[4], p[6] + p[7], p[5].year, p[5].month) for p in W.pay
                  if p[8] in ("HS_FS14", "HT_V49", "HT_S99", "PF_C12"))
    ok("every contract line is paid once a month at a constant amount", set(con.values()) == {1} and
       len({(k[0], k[1]) for k in con}) * 47 == len(con))
    flat = {}
    for key in ("DP14", "HS_FS14", "HT_V49", "HT_S99", "PF_C12"):
        m = Counter((p[5].year, p[5].month) for p in W.pay if p[8] == key)
        flat[key] = set(m.values())
    ok("each flat stream has the same count in every month of the extract",
       all(len(v) == 1 for v in flat.values()), flat)
    # no background in flagged cells; short breaks out of cell 14
    bg = sum(1 for p in W.pay if p[8] not in ("SL", "SLJ", "DP14", "TSP", "HS_FS14", "HT_V49", "HT_S99", "PF_C12")
             and p[6] + p[7] >= 100000 and (p[0], S.cell_p(p[6] + p[7])) in FLAGGED_2526)
    ok("no payment outside the recurring streams falls in a 2025/26 flagged cell", bg == 0, bg)
    sb14 = sum(1 for p in W.pay if p[8] == "SB" and S.cell_p(p[6] + p[7]) == 14)
    ok("short-break claims never fall in cell 14", sb14 == 0)
    edge = sum(1 for p in W.pay if p[6] + p[7] in (100000, 99999999) or p[6] in (100000, 99999999))
    ok("no payment at exactly 1,000.00 or 999,999.99 on either amount", edge == 0)
    big_flag = sum(1 for p in W.pay if p[8] == "BIG" and (p[0], S.cell_p(p[6] + p[7])) in FLAGGED_2526)
    ok("no payment of a million pounds or more sits in a flagged department-cell", big_flag == 0)
    ok("2026/27 carries 14 Shared Lives runs and 2027/28 carries 13",
       len(PR.sl_runs(*PR.FY["2026/27"])) == 14 and len(PR.sl_runs(*PR.FY["2027/28"])) == 13)
    # clean-data repairs
    pays_g = [(p[0], p[1], p[2] + p[3], 0) for p in D["pays"]]
    cg = S.screen_counts(pays_g, ("net", "dec", "excl"))
    r1g, _ = S.routed_in(pays_g, S.flagged_cells(cg, "2025/26", DEPT_ORDER), ("net", "dec", "excl"))
    ok("repair 1: a gross-amount file collapses rung 1 onto rung 2 and leaves rungs 2 to 4 unchanged",
       r1g == M["r2"] and S.flagged_cells(cg, "2025/26", DEPT_ORDER) == D["cells2526"])
    _, rows2526, _ = FHM.build_runs(W, D["cells2526"])
    ok("repair 2: a run log on the 2025/26 cells gives the provider rung 2's 7,632; the answer does not move",
       sum(FHM.b1_routed(rows2526).values()) == M["r2"])


PLAN_MONTHS = ["%d-%02d" % ym for ym in PR.months(*PR.FY[PR.PLAN])]
FY_MONTHS = ["%d-%02d" % ym for ym in PR.months(*PR.FY["2025/26"])]


def monthly(sim, cells, by="file"):
    out = Counter()
    for dept, g, d, kind in sim:
        if g >= 100000 and (dept, S.cell_p(g)) in cells:
            k = PR.wd_before(d, 2) if by == "file" else d
            out["%d-%02d" % (k.year, k.month)] += 1
    return [out[m] for m in PLAN_MONTHS]


def diff_months(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


def check_asks(W, D, M):
    cells = D["cells2526"]
    sim = W.plan_year()
    A = monthly(sim, cells)
    ok("ask A: plan-year routed by run month sums to the answer", sum(A) == M["r4"], A)
    pay = monthly(sim, cells, by="payment")
    ok("ask A stop: payment-date months move December and March", diff_months(A, pay) == 2, pay)
    r3m = monthly(W.plan_year(sl_rule="carried"), cells)
    ok("ask A stop: rung 3 misses every month", diff_months(A, r3m) == 12)
    r4m = monthly(W.plan_year(sl_rule="carer"), cells)
    ok("ask A stop: rung 4 (joint halves held) misses every month", diff_months(A, r4m) == 12, r4m)
    ok("ask A: the busiest plan-year month is unique (December 2027)", A.count(max(A)) == 1 and
       PLAN_MONTHS[A.index(max(A))] == "2027-12", max(A))
    REC["A"] = dict(zip(PLAN_MONTHS, A))
    # ---- B1
    rows = D["runrows"]
    B1 = [D["b1"][m] for m in FY_MONTHS]
    allrows = Counter()
    for r in rows:
        allrows[r["run_month"]] += int(r["payments_routed"])
    latest = {}
    for r in rows:
        latest.setdefault(r["run_month"], set()).add((r["run_completed"], r["run_ref"]))
    keep = {m: max(v)[1] for m, v in latest.items()}
    lat = Counter()
    for r in rows:
        if keep[r["run_month"]] == r["run_ref"]:
            lat[r["run_month"]] += int(r["payments_routed"])
    pdm = Counter()
    for p in D["pays"]:
        g = p[2] + p[3]
        if PR.fy_of(p[1]) == "2025/26" and 100000 <= g <= 99999999 and (p[0], S.cell_p(g)) in D["cells2324"]:
            pdm["%d-%02d" % (p[1].year, p[1].month)] += 1
    no_we = Counter()
    for r in rows:
        if not (r["run_type"] == "Scheduled" and r["run_month"] == "2025-10") and r["department"] != "WE":
            no_we[r["run_month"]] += int(r["payments_routed"])
    stops = {"all_rows": [allrows[m] for m in FY_MONTHS], "latest_only": [lat[m] for m in FY_MONTHS],
             "payment_month": [pdm[m] for m in FY_MONTHS], "cells_2526": [no_we[m] for m in FY_MONTHS]}
    ok("ask B1: routed by run month, re-run replacing and supplementary adding", sum(B1) == M["side"], B1)
    ok("ask B1 stops each miss at least one month",
       all(diff_months(B1, v) >= 1 for v in stops.values()), {k: diff_months(B1, v) for k, v in stops.items()})
    REC["B1"] = dict(zip(FY_MONTHS, B1))
    REC["B1_stops"] = stops
    # ---- B2
    acks, inv = D["acks"], D["inv"]
    B2 = [D["b2"][m] for m in FY_MONTHS]
    rm = {a["batch_ref"]: a["_run_month"] for a in acks}
    inv_issue, inv_route, inv_pos = Counter(), Counter(), Counter()
    for r in inv:
        inv_issue[r["issue_date"][:7]] += r["quantity"]
        inv_route[rm[r["batch_ref"]]] += r["quantity"]
        if r["quantity"] > 0:
            inv_pos[rm[r["batch_ref"]]] += r["quantity"]
    recv, ackm = Counter(), Counter()
    for a in acks:
        if a["status"] == "examined":
            recv[a["_run_month"]] += a["payments_received"]
        ackm[a["acknowledged"][:7]] += a["payments_examined"]
    b2stops = {"invoice_issue_month": [inv_issue[m] for m in FY_MONTHS],
               "invoice_qty_by_run": [inv_route[m] for m in FY_MONTHS],
               "invoices_without_credits": [inv_pos[m] for m in FY_MONTHS],
               "received": [recv[m] for m in FY_MONTHS],
               "ack_month": [ackm[m] for m in FY_MONTHS],
               "routed_copy": B1}
    ok("ask B2: examined by routing month", sum(B2) == sum(a["payments_examined"] for a in acks), B2)
    ok("ask B2 stops each miss at least one month",
       all(diff_months(B2, v) >= 1 for v in b2stops.values()), {k: diff_months(B2, v) for k, v in b2stops.items()})
    ok("ask B2: examined differs from routed in at least ten months", diff_months(B2, B1) >= 10)
    ok("referee: the Q2 service report's examined total equals July to September of ask B2",
       D["q2"]["examined"] == sum(B2[3:6]) and D["q2"]["charged"] == D["q2"]["examined"])
    REC["B2"] = dict(zip(FY_MONTHS, B2))
    # ---- C
    ch, prem, unused, charge = D["c"]
    gold = [prem[q] for q in (1, 2, 3, 4)] + [int(round(charge[q])) for q in (1, 2, 3, 4)]
    ok("ask C: premium examinations in Q1 and Q2, unused-volume charges in Q3 and Q4",
       prem[1] > 0 and prem[2] > 0 and unused[3] > 0 and unused[4] > 0 and prem[3] == prem[4] == 0, gold)
    margin = min(abs((charge[q] % 1) - 0.5) for q in (3, 4))
    ok("ask C: unused-volume charges sit clear of the half-pound rounding edge", margin >= 0.05, round(margin, 2))

    def cfig(res):
        ch_, p_, u_, c_ = res
        return [p_[q] for q in (1, 2, 3, 4)] + [int(round(c_[q])) for q in (1, 2, 3, 4)]
    inv_q = {}
    for r in inv:
        inv_q.setdefault(r["batch_ref"], dt.date.fromisoformat(r["issue_date"]))
    cstops = {
        "original_allocation": cfig(FHM.c_quarters(acks, alloc={q: PR.ALLOC_ORIG for q in (1, 2, 3, 4)})),
        "rate_2026_27": cfig(FHM.c_quarters(acks, rate=PR.BASE_2627)),
        "examined_not_charged": cfig(FHM.c_quarters(acks, qty=lambda a: a["payments_examined"])),
        "invoice_quarter": cfig(FHM.c_quarters([a for a in acks if a["status"] == "examined"], qmap=lambda a: (
            {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[inv_q[a["batch_ref"]].month]
            if inv_q[a["batch_ref"]] <= dt.date(2026, 3, 31) else None))),
    }
    ok("ask C stops each move at least one of the eight figures",
       all(sum(1 for x, y in zip(gold, v) if x != y) >= 1 for v in cstops.values()),
       {k: sum(1 for x, y in zip(gold, v) if x != y) for k, v in cstops.items()})
    REC["C"] = gold
    REC["C_stops"] = cstops
    # ---- call furniture
    fh = M["side"]
    gap_u, gap_h = hundred(fh - M["r4"]), hundred(fh) - hundred(M["r4"])
    ok("Fernhollow's figure (the run log's 2025/26 routed total) and the gap converge on unrounded and rounded "
       "figures", gap_u == gap_h, (fh, gap_u, gap_h))
    ok("graded hundreds sit at least 20 from a bin edge (order, ASC count, Fernhollow figure, gap)",
       min(bin_margin(M["r4"]), bin_margin(M["c4"][("ASC", 14)]), bin_margin(fh), bin_margin(fh - M["r4"])) >= 20,
       (bin_margin(M["r4"]), bin_margin(M["c4"][("ASC", 14)]), bin_margin(fh), bin_margin(fh - M["r4"])))
    ok("Adult Social Care carries the largest share (3,694 of 6,706, no near tie)",
       M["c4"][("ASC", 14)] > 4 * M["c4"][("HS", 14)])
    REC.update(fernhollow=fh, gap=fh - M["r4"], asc=M["c4"][("ASC", 14)])


MAIN_FILES = ("spine", "tsp", "statements", "method", "rates", "closure", "scheme")
DEVICE_FILES = ("runlog", "runbook", "calendar", "invoices", "acks", "terms", "ratecards", "order", "q2report")


def doc_text(p):
    suf = p.suffix.lower()
    if suf in (".csv", ".txt", ".eml", ".json"):
        return p.read_text(encoding="utf-8")
    if suf in (".docx", ".xlsx"):
        with zipfile.ZipFile(p) as z:
            return "\n".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist() if n.endswith(".xml"))
    if suf == ".pdf":
        from pypdf import PdfReader
        return "\n".join(pg.extract_text() for pg in PdfReader(str(p)).pages)
    return ""


def check_pack(W, D, target, meta_path, F, distractors):
    import writers as WR
    files = sorted(p for p in target.iterdir() if p.is_file())
    meta = json.loads(Path(meta_path).read_text())
    ok("input gate: 10 or more files", len(files) >= 10, len(files))
    fmts = {p.suffix.lower() for p in files}
    ok("input gate: 3 or more formats", len(fmts) >= 3, sorted(fmts))
    with open(target / F["spine"], encoding="utf-8") as fh:
        nrows = sum(1 for _ in fh) - 1
    ok("input gate: the spending file carries 25,000 or more rows", nrows >= 25000, nrows)
    ok("input gate: two distractors named in metadata.json and present in target/",
       len(meta["distractor_files"]) >= 2 and all((target / f).exists() for f in meta["distractor_files"]))
    texts = {p.name: doc_text(p) for p in files}
    ok("no file name or file content under target/ says 'distractor'",
       not any("distractor" in n.lower() or "distractor" in t.lower() for n, t in texts.items()))
    ok("the shipped set equals the declared asset list (H4)", sorted(p.name for p in files) == sorted(F.values()))
    idx = texts[F["index"]]
    ok("the working papers index names every other shipped file (H9)",
       all(F[k] in idx for k in F if k != "index"))
    ok("no em dash anywhere under target/", not any("\u2014" in t for t in texts.values()))
    leak = ["1,464", "1464.00", "3,044", "3044.00", "6,522", "6,500", "5,742", "3,486", "per carer", "re-sum",
            "6,706", "6,700", "6,498", "5,718", "3,694", "1,484", "1484.00", "2,274", "2274.00", "jointly",
            "joint carer", "joint household", "halves", "half of the", "split between", "each carer"]
    hits = [(n, w) for n, t in texts.items() for w in leak if w in t and n != F["spine"]]
    ok("no document states a carer's amount, the answer or a rung figure", not hits, hits)
    closure = texts[F["closure"]].split("\n\n", 1)[1]
    ok("the closure notice body names no carer, amount or count",
       not re.search(r"\d{3,}", re.sub(r"20\d\d(/\d\d)?", "", closure)), "")
    ok("main-call files and ask-device files are disjoint (zero device rows in the main population)",
       not set(MAIN_FILES) & set(DEVICE_FILES) and not set(distractors) & (set(MAIN_FILES) | set(DEVICE_FILES)))
    # producer metadata and timestamps (H1), dates inside extracts (H16)
    bad = []
    for p in files:
        res = WR.SCRUB.audit(str(p), WR.FLOOR, WR.CEILING)
        if res and (res[0] or res[1]):
            bad.append((p.name, res))
    ok("no writer signature and no out-of-band timestamp in any shipped binary (H1)", not bad, bad)
    mt = max(p.stat().st_mtime for p in files)
    ok("file times run no later than the as-of date", dt.datetime.fromtimestamp(mt).date() <= PR.AS_OF)
    ack_max = max(a["examination_completed"] or "" for a in D["acks"])
    inv_max = max(r["issue_date"] for r in D["inv"])
    ok("acknowledgement and invoice extracts end before their extract dates (H16)",
       ack_max <= "2026-06-03" and inv_max <= "2026-06-04", (ack_max, inv_max))
    ok("the run log's entries end before it was closed (H16)",
       max(r["run_completed"] for r in D["runrows"]) <= "2026-04-07")
    sp_max = max(p[5] for p in W.pay)
    ok("spending file runs to the 25 February 2027 creditor run", sp_max == PR.SPINE_TO)
    names = set(re.findall(r"\b(?:Tina|Julia|Pauline|Wendy|Abigail|Douglas|Adam|Lynda|Bethan|Shaun|Anne) [A-Z]\w+",
                           "\n".join(t for n, t in texts.items() if n != F["spine"])))
    ok("every persona named in the pack is drawn from guard.py names", names <= set(PR.PEOPLE.values()), names)


def run_all(W, D, target, meta_path, F, distractors):
    M = check_main(W, D, F)
    check_grid(W, D, M)
    check_world(W, D, M)
    check_asks(W, D, M)
    check_pack(W, D, target, meta_path, F, distractors)
    n_ok = sum(1 for _, c, _ in RESULTS if c)
    print("\n%d of %d assertions pass" % (n_ok, len(RESULTS)))
    REC["assertions"] = [n_ok, len(RESULTS)]
    print("RECORD " + json.dumps(REC, default=str))
    return n_ok == len(RESULTS)
