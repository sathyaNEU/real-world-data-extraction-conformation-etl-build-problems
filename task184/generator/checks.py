"""Assertions on the built pack and goldens: the input gates, every rung of the ladder at its named wrong answer with
its margin, the variants a solver might run, dominance, the flip, the semantic forks (SF1 to SF9), the rounding bins,
the separation line between the call and the asks, each ask's stops outside its bin at every airport, the documents'
silence on the stand-down, the realism sweep, and the goldens agreeing with figures.json."""
import collections
import csv
import json
import os
import re

import numpy as np
import openpyxl

import analysis as AN
import asks as A
import build as B
import docs as D
import models as M
import profiles as PR
import records as R
import sim as S
import world as W

N = [0]
PEOPLE = {v[0] for v in W.PEOPLE.values()}


def ok(cond, what):
    N[0] += 1
    if not cond:
        raise AssertionError(what)


def _pdf_text(path):
    from pypdf import PdfReader
    return " ".join(pg.extract_text() for pg in PdfReader(path).pages).replace("\n", " ")


def standard_2023(a, lanes):
    c = np.asarray(lanes, float) * W.LANE_RATE_2023
    q, over = 0.0, 0.0
    for i in range(W.T):
        q = max(0.0, q + a[i] - c[i])
        if 15.0 * q / c[i] > W.STANDARD_MIN:
            over += a[i]
    return over


def run(target, golden, world, meta_path):
    F = world["F"]
    d, p = F["design"], F["plans"]
    fig = json.load(open(os.path.join(os.path.dirname(golden), "generator", "figures.json")))
    tot, rank = F["tot"], F["rank"]
    lead = lambda h: tot[h][rank[h][0]] / tot[h][rank[h][1]]

    # ---- input gates
    meta = json.load(open(meta_path))
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    ok(meta["input_gates"]["largest_file_rows"] >= 25000, "a file of 25,000 rows or more")
    ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]), "two distractors")
    for f in meta["distractor_files"]:
        ok("distract" not in f, "distractor not named as such")
    src = "".join(open(os.path.join(os.path.dirname(__file__), m)).read()
                  for m in ("analysis.py", "asks.py", "verify.py", "models.py"))
    for f in meta["distractor_files"]:
        ok(f not in src, "the solution never reads " + f)
    main_src = open(os.path.join(os.path.dirname(__file__), "verify.py")).read().split("def passengers_2026")[0]
    for f in (R.HOTELS, R.CLAIMS, R.RETURNS, R.REGISTER, R.QUEUE_TIME, R.FAULTS, R.FEEDBACK):
        ok(f not in main_src, "the main call's path never reads " + f)

    # ---- the ladder: rung 0 (the pattern plus three), rung 1 (the posted day's whole gap averaged over the unit's
    # hours), rung 2 (that gap interval by interval, the pattern as the baseline), the golden (both arms on the lanes
    # the checkpoint actually opens)
    ok(rank["gross"][0] == "CUL" and lead("gross") >= 1.15, "rung 0 names Cullinvale by 1.15x")
    ok(rank["gross"].index("ESK") in (3, 4), "Eskerford 4th or 5th on rung 0")
    ok(rank["average"][0] == "HAL" and lead("average") >= 1.15, "rung 1 names Halloran Bay by 1.15x")
    ok(rank["interval"][0] == "HAL" and lead("interval") >= 1.15, "rung 2 names Halloran Bay by 1.15x")
    ok(round(tot["average"]["HAL"], -2) != round(tot["interval"]["HAL"], -2),
       "rung 1 and rung 2 name Halloran Bay at different figures")
    ok(rank["interval"].index("ESK") == 1 and tot["interval"]["HAL"] / tot["interval"]["ESK"] >= 1.20,
       "Eskerford second on rung 2, by 1.20x")
    ok(rank["average"].index("ESK") >= 1 and rank["gross"].index("ESK") >= 1,
       "Eskerford never first on an intermediate rung")
    ok(rank["actual"][0] == "ESK" and lead("actual") >= 1.2, "golden Eskerford by 1.2x or more")
    ok(len({rank["gross"][0], rank["interval"][0], rank["actual"][0]}) == 3, "each rung names its own airport")
    for h in ("double", "standonly", "shift", "average18", "uniform"):
        ok(rank[h][0] != "ESK" and tot[h][rank[h][0]] >= 1.10 * tot[h]["ESK"],
           "the %s basis names %s and leaves Eskerford 1.10x behind" % (h, W.NAME[rank[h][0]]))
    ok(tot["actual"][rank["actual"][1]] / tot["actual"][rank["actual"][2]] >= 1.10,
       "the golden runner-up clear of the third by 1.10x")
    # the grain the lane feed and the pattern share is 15 minutes; averaging both arms by the hour keeps the call
    hourly = {}
    for c in W.CODES:
        hs = 0.0
        for n in W.DAYS:
            pl = p[c][n]
            b, g = M.baseline(c, pl).copy(), M.gap_seen(c, pl).copy()
            for h in range(W.OPEN_H, W.CLOSE_H):
                m = (M.HOUR >= h) & (M.HOUR < h + 1)
                b[m] = M.baseline(c, pl)[m].mean()
                g[m] = M.gap_seen(c, pl)[m].mean()
            hs += (M.queue(d[c][n], b)[0] - M.queue(d[c][n], pl + M.team() - g)[0]) * W.DAYS[n]
        hourly[c] = hs
    ok(max(hourly, key=hourly.get) == "ESK" and hourly["ESK"] / sorted(hourly.values())[-2] >= 1.15,
       "both arms averaged by the hour instead of by 15 minutes still names Eskerford")
    real = F["realised"]
    rr = sorted(real, key=lambda c: -real[c])
    ok(rr[0] == "CUL" and real[rr[0]] / real[rr[1]] >= 1.15, "last summer's realised effect names Cullinvale")
    ok(rr.index("ESK") >= 2, "Eskerford neither 1st nor 2nd on last summer's realised effect")
    swing = (tot["interval"]["ESK"] / tot["actual"]["ESK"]) / (tot["interval"]["HAL"] / tot["actual"]["HAL"])
    carried = tot["interval"]["HAL"] / tot["interval"]["ESK"]
    ok(1 / swing >= 1.2 * carried, "dominance: the baseline's swing %.2f against Halloran Bay's carried lead %.2f" %
       (1 / swing, carried))
    leaks_g = sum(1 for c in W.CODES if round(tot["gross"][c], -2) == round(tot["actual"][c], -2))
    leaks_a = sum(1 for c in W.CODES if round(tot["average"][c], -2) == round(tot["actual"][c], -2))
    leaks_i = sum(1 for c in W.CODES if round(tot["interval"][c], -2) == round(tot["actual"][c], -2))
    ok(leaks_g == 0, "rung 0 matches no summer figure (%d)" % leaks_g)
    ok(leaks_a == 0, "rung 1 matches no summer figure (%d)" % leaks_a)
    ok(leaks_i <= 1 and round(tot["interval"]["HAL"], -2) == round(tot["actual"]["HAL"], -2),
       "rung 2 matches only Halloran Bay's summer figure, the one checkpoint that opens its pattern (%d)" % leaks_i)
    t23 = {}
    for c in W.CODES:
        t23[c] = sum((standard_2023(d[c][n], M.baseline(c, p[c][n])) -
                      standard_2023(d[c][n], p[c][n] + M.team() - M.gap_seen(c, p[c][n]))) * W.DAYS[n]
                     for n in W.DAYS)
    ok(any(round(t23[c], -2) != round(tot["actual"][c], -2) for c in W.CODES),
       "the superseded 2023 basis moves the figures")

    # ---- the three rules, executed (CLAUDE.md, first section)
    # R1 the analyst test: the easy route on the generator's own clean truth, every rule read correctly, files
    # Cullinvale; R2 changing the decisive step alone gives the golden
    easy = M.ranking(M.scenario(d, p, "gross"))
    ok(easy[0] == "CUL" and easy[0] != rank["actual"][0], "R1 the easy route files Cullinvale, not the golden")
    one_step = M.ranking(M.scenario(d, p, "interval"))
    ok(one_step[0] == "HAL" and one_step[0] != rank["actual"][0],
       "R1 correcting the posted day's gap alone still files a wrong airport")
    ok(M.ranking(M.scenario(d, p, "actual"))[0] == "ESK",
       "R2 taking both arms on the lanes the checkpoint opens, and nothing else, gives the golden")
    # R3a not a plant: every shipped lane count is the checkpoint's own record and nothing is wrong with it
    for c in W.CODES:
        sfl = F["shortfall_seen"][c]
        gp = F["gap_seen"][c]
        ok(np.allclose(sfl, M.shortfall(c, PR.plan(c))), "R3a %s unopened lanes recoverable from its own days" % c)
        ok(np.all(gp["min"] >= sfl - 1e-9), "R3a %s posted days never open more than its own days" % c)
    # R3b not semantics: the decisive step survives every reading in the fork table (asserted below, SF1 to SF9)
    # R3c not rule application: no shipped sentence names the step, swept below over every document
    # ---- the flip
    ok(len(set(F["flips"].values())) == 1, "SF8 the flip is the same whether scaled arrivals are rounded or not")
    ok("smallest whole per cent shortfall" in open(os.path.join(os.path.dirname(target), "prompt.txt")).read(),
       "SF8 the prompt asks the smallest whole per cent shortfall at which another posting moves more")
    k, ru = F["flip"], F["runner"]
    best = max(v for c, v in tot["actual"].items() if c != F["pick"])
    for mode in ("none", "round", "floor"):
        ok(M.summer(d, p, "ESK", 1 - (k - 1) / 100.0, mode) >= 1.02 * best, "at %d%% Eskerford still ahead" % (k - 1))
        ok(M.summer(d, p, "ESK", 1 - k / 100.0, mode) <= 0.98 * best, "at %d%% Eskerford behind" % k)

    # ---- memo claims
    for n in W.DAYS:
        ok(all(F["gold"]["ESK"][n] > F["gold"][c][n] for c in W.CODES if c != "ESK"), "Eskerford first in " + n)
    ok(W.SHORT["ESK"][0] == 2 and W.SHORT["HAL"][0] == 0 and
       all(W.SHORT[c][0] == 1 for c in W.CODES if c not in ("ESK", "HAL")),
       "two bank lanes unopened at Eskerford, one at six others, none at Halloran Bay")
    ok(all(PR.plan("HAL") == W.LANES["HAL"]), "Halloran Bay's pattern staffs its five lanes right through the day")
    ok(sum(1 for c in W.CODES if W.RELEASE[c][0] == 2) == 6 and all(W.RELEASE[c][1] == 2 for c in W.CODES),
       "two own lanes down through the evening bank at all eight and through the morning bank at six")
    ok(fig["pick_total"] - fig["runner_total"] == AN.rnd100(tot["actual"]["ESK"] - tot["actual"][ru]),
       "the gap reads the same from rounded and unrounded totals")
    for c in W.CODES:
        resid = sum(M.queue(d[c][n], M.arms(c, p[c][n], "actual")[1])[0] for n in W.DAYS)
        base = sum(M.queue(d[c][n], M.arms(c, p[c][n], "actual")[0])[0] for n in W.DAYS)
        ok(0 < resid < base, "the posting at %s leaves some passengers outside the standard and fewer than before" % c)

    # ---- semantic forks
    ok("those outside it on the lanes open with it" in _pdf_text(os.path.join(target, D.STANDARD_26)),
       "SF1 the standard defines the passengers moved")
    for c in W.CODES:
        rs = F["gap_seen"][c]
        ok(np.array_equal(rs["min"], rs["max"]), "SF2 %s showed the same gap on every posted day" % c)
        ok(np.allclose(rs["min"], M.gap_seen(c, PR.plan(c))), "SF2 %s gap as filed" % c)
        ok(rs["min"].sum() > 0, "SF2 %s opened fewer lanes than the pattern while the unit was there" % c)
        ok(np.array_equal(rs["min"], np.round(rs["min"])), "SF7 %s whole lanes" % c)
        sfl = F["shortfall_seen"][c]
        ok(np.array_equal(sfl, np.round(sfl)), "SF7 %s whole lanes unopened" % c)
        ok((sfl.sum() > 0) == (W.SHORT[c][0] > 0), "SF10 %s unopened lanes show on its own days" % c)
    l26 = sorted((r["airport"], r["interval_start"], int(r["lanes_planned"]))
                 for r in csv.DictReader(open(os.path.join(target, R.ROSTER_26), encoding="utf-8")))
    ws27 = openpyxl.load_workbook(os.path.join(target, R.ROSTER_27), read_only=True).worksheets[0]
    rows27 = [r for r in ws27.iter_rows(values_only=True)]
    hdr = next(i for i, r in enumerate(rows27) if r and r[0] == "Start")
    cols = rows27[hdr]
    l27 = sorted((cols[j], r[0], int(r[j])) for r in rows27[hdr + 1: hdr + 73] for j in range(1, len(cols)))
    ok(l26 == l27, "SF2 the 2026 and 2027 roster patterns plan the same lanes")
    posted_weeks = collections.Counter(W.POSTINGS_2026)
    ok(posted_weeks["ARD"] == 3 and W.POSTINGS_2026[9] == W.POSTINGS_2026[10] == "ARD",
       "SF2 a two-week posting shows the gap held")
    for c in W.CODES:
        days = [x for x in world["airports"][c]["daily"] if not x["posted"]]
        clean = [x for x in days if np.allclose(np.array(x["open"], float), M.baseline(c, PR.plan(c)))]
        ok(len(clean) >= 40, "SF10 %s opens the same lanes on at least forty of its own days (%d)" % (c, len(clean)))
    ok([W.DAYS[n] for n, _, _ in W.PERIODS] == [16, 31, 31], "SF4 the periods' days")
    sheets = [f for f in files if f.endswith(".xlsx")]
    with_design = [f for f in sheets if "Design day" in str(openpyxl.load_workbook(os.path.join(target, f),
                                                                                    read_only=True).worksheets[0]["A1"].value)]
    ok(with_design == [R.PLANNING], "SF3 the planning sheet is the only design-day source in the pack")
    ok(int(M.team().sum()) == 3 * 64, "SF5 three lanes from 05:00 to 21:00")
    for c in W.CODES:
        for n in W.DAYS:
            g, w = PR.margins(c, d[c][n], p[c][n])
            ok(g >= 0.3 and w >= 0.1, "SF6 no wait within half a minute of 20 (%s %s)" % (c, n))
    for c in W.CODES:
        nm = W.NAME[c]
        ok(sum(fig["moved"][nm].values()) == fig["moved_total"][nm], "SF9 %s summer equals its rounded periods" % nm)

    # ---- rounding bins
    for c in W.CODES:
        for n in W.DAYS:
            v = F["gold"][c][n]
            ok(abs((v % 100) - 50) >= 1, "no period figure on a half-hundred tie (%s %s)" % (c, n))
        ok(abs((tot["interval"][c] % 100) - 50) >= 2, "bin total " + c)
        ok(abs((F["asks"]["passengers"][c] % 100) - 50) >= 2, "bin passengers " + c)
        for key in ("hotel", "claims"):
            v = F["asks"][key][c] * 100
            ok(abs((v % 1) - 0.5) >= 0.01, "bin %s %s" % (key, c))
        for nm in (W.NAME[c],):
            ok(fig["moved_total"][nm] % 1000 != 0 and all(x % 1000 for x in fig["moved"][nm].values()),
               "no whole-thousand figure for " + nm)

    # ---- asks: every stop outside its bin at every airport (the cracker sheet)
    for c in W.CODES:
        g1 = round(F["asks"]["passengers"][c], -2)
        for h, v in F["stops"]["passengers"].items():
            ok(round(v[c], -2) != g1, "ask 1 %s misses at %s" % (h, c))
        g2 = round(F["asks"]["hotel"][c], 2)
        ok(round(F["stops"]["hotel"]["every line"][c], 2) != g2, "ask 2 every line misses at " + c)
        g3 = round(F["asks"]["claims"][c], 2)
        for h, v in F["stops"]["claims"].items():
            ok(round(v[c], 2) != g3, "ask 3 %s misses at %s" % (h, c))
    ok(round(F["stops"]["hotel"]["no credit"]["HAL"], 2) != round(F["asks"]["hotel"]["HAL"], 2),
       "ask 2 dropping the credit note misses at Halloran Bay")
    # ask 1's evidence: the operators' returns reconcile with the passenger lanes and not with every lane
    pm = R.passenger_lanes_by_month(world)
    rets = {(r["airport"], r["month"]): int(r["departing_passengers"])
            for r in csv.DictReader(open(os.path.join(target, R.RETURNS), encoding="utf-8"))}
    for c in W.CODES:
        staff = set(S.staff_ids(c))
        alls = collections.Counter()
        for (_, lane, dd, i, n) in world["airports"][c]["lanes"]:
            alls[dd.month] += n
            if lane in staff:
                ok(i < 4 or i >= 68, "staff lanes only before 05:00 and after 21:00")
        for m in (7, 8):
            rep = rets[(c, "2026-%02d" % m)]
            ok(abs(rep / pm[c][m] - 1) < 0.008, "returns reconcile with passenger lanes %s %d" % (c, m))
            ok(rep / alls[m] - 1 < -0.012, "returns do not reconcile with every lane %s %d" % (c, m))
    # ask 2: invoiced stays equal the postings' officer-nights; ask 3: the replay copies only the August batch
    stays = collections.defaultdict(int)
    po_air = {x["po"]: x["airport"] for x in F["posts"]}
    for x in F["lines"]:
        if x["line"] == 1:
            stays[po_air[x["po"]]] += x["nights"]
    logged = collections.Counter()
    for x in F["posts"]:
        logged[x["airport"]] += x["officer_nights"]
    ok(dict(stays) == dict(logged), "invoiced officer-nights equal the postings' at every airport")
    keys = collections.Counter((x["claim_ref"], x["line"]) for x in F["export"])
    dup = [k for k, v in keys.items() if v > 1]
    ok(all(v <= 2 for v in keys.values()) and dup, "claim lines appear once or twice")
    by_key = collections.defaultdict(list)
    for x in F["export"]:
        by_key[(x["claim_ref"], x["line"])].append(x)
    for k_ in dup:
        a_, b_ = by_key[k_]
        ok(a_["approved"].month == 8 and {kk: v for kk, v in a_.items() if kk != "row_id"} ==
           {kk: v for kk, v in b_.items() if kk != "row_id"}, "only the August batch repeats, row id aside")
    claims_by = collections.defaultdict(list)
    for x in F["export"]:
        claims_by[x["claim_ref"]].append(x)
    for ref, rows in claims_by.items():
        subs = {A.week_airport(F["posts"], x["date"]) for x in rows if x["category"] == "SUBS-DAY"}
        ok(len(subs) == 1, "each claim's subsistence days fall in one posting week")
    # separation line: no ask device row inside the main call's rows (05:00 to 21:00 lane presence, plans, sheet)
    ok(all(W.clock(i) < "05:00" or W.clock(i) >= "21:00" for c in W.CODES for (_, lane, dd, i, n) in
           world["airports"][c]["lanes"] if lane in set(S.staff_ids(c))), "separation: staff lanes outside 05:00-21:00")

    # ---- documents silent on the stand-down; no dash anywhere
    texts = {f: _pdf_text(os.path.join(target, f)) for f in files if f.endswith(".pdf")}
    texts.update({f: open(os.path.join(target, f), encoding="utf-8").read() for f in files
                  if f.endswith((".md", ".json"))})
    for f, t in texts.items():
        low = t.lower()
        for word in ("stood down", "stand down", "stands down", "stand-down", "released", "release", "training",
                     "own lanes", "host's lanes", "host lanes", "unopened", "not opened", "never opens",
                     "unfilled", "vacant", "overtime", "uncovered", "shortfall", "short of the pattern",
                     "fewer lanes", "actually open"):
            ok(word not in low, "%s silent on %r" % (f, word))
        ok("—" not in t and "–" not in t, "no dash in " + f)
    for f in files:
        if f.endswith(".csv"):
            t = open(os.path.join(target, f), encoding="utf-8").read()
            ok("—" not in t and "–" not in t, "no dash in " + f)

    # ---- the extract notes register every shipped file but themselves (H9)
    notes = open(os.path.join(target, D.NOTES), encoding="utf-8").read()
    ok({f for f in files if "`%s`" % f in notes} == set(files) - {D.NOTES}, "the extract notes name every shipped file")

    # ---- dates: only forward-looking records run past the extract date (H16 allow-list)
    late = []
    for f in files:
        if f.endswith((".csv", ".md", ".json")):
            t = open(os.path.join(target, f), encoding="utf-8").read()
            if any(x > "2027-04-23" for x in set(re.findall(r"\b20\d\d-\d\d-\d\d\b", t))):
                late.append(f)
    ok(late == [], "no shipped record runs past the extract date (%s)" % late)

    # ---- realism sweep
    sums = [fig["passengers_2026"][W.NAME[c]] for c in W.CODES]
    ok(len(set(sums)) == len(sums), "no two airports with the same 2026 passengers")
    daily = collections.defaultdict(set)
    for c in W.CODES:
        for x in world["airports"][c]["daily"]:
            daily[c].add(x["screened"])
    ok(all(len(v) > 70 for v in daily.values()), "daily throughput varies at every airport")
    allt = " ".join(texts.values())
    for who in PEOPLE:
        ok(who in allt or who == W.PEOPLE["team"][0], "persona %s from the card" % who)
    ok(W.PEOPLE["team"][0] in open(os.path.join(target, R.POSTINGS)).read(), "team leader in the postings")
    flags = json.load(open(os.path.join(target, D.FLAGS)))
    fl = [x["airport"] for x in flags["airports"] if x["flagged"]]
    ok(sorted(fl) == sorted(W.CODES), "the detector flagged the eight airports")
    byb = sorted(flags["airports"], key=lambda x: -x["breach_intervals"])
    ok([x["airport"] for x in byb] != rank["actual"], "the detector's order is not the posting order")
    ok(byb[0]["airport"] != F["pick"], "the detector's worst checkpoint is not the posting")

    # ---- goldens agree with figures.json
    memo = _pdf_text(os.path.join(golden, "mobile_team_posting_summer_2027.pdf"))
    from pypdf import PdfReader
    ok(len(PdfReader(os.path.join(golden, "mobile_team_posting_summer_2027.pdf")).pages) == 2, "a two-page memo")
    for nm in fig["moved_total"]:
        ok("{:,}".format(fig["moved_total"][nm]) in memo, "memo carries %s summer" % nm)
        ok("{:,}".format(fig["passengers_2026"][nm]) in memo, "memo carries %s 2026 passengers" % nm)
        ok("{:,.2f}".format(fig["hotel_per_night"][nm]) in memo, "memo carries %s hotel" % nm)
        ok("{:,.2f}".format(fig["claims_per_week"][nm]) in memo, "memo carries %s claims" % nm)
    ok("%d per cent" % fig["flip_pct"] in memo, "memo carries the flip")
    ok("—" not in memo and "–" not in memo, "no dash in the memo")
    wx = openpyxl.load_workbook(os.path.join(golden, "mobile_team_effect_2027.xlsx"), data_only=True)
    pe = {r[1]: r for r in wx["Posting effect"].iter_rows(min_row=5, max_row=12, values_only=True)}
    for c in W.CODES:
        nm = W.NAME[c]
        ok(pe[c][5] == fig["moved_total"][nm] and pe[c][2] == W.SHORT[c][0] and pe[c][3] == W.RELEASE[c][0] and
           pe[c][4] == W.RELEASE[c][1], "workbook posting effect " + nm)
    s26 = {r[1]: r for r in wx["Summer 2026"].iter_rows(min_row=4, max_row=11, values_only=True)}
    for c in W.CODES:
        nm = W.NAME[c]
        ok(s26[c][2] == fig["passengers_2026"][nm] and s26[c][3] == fig["hotel_per_night"][nm] and
           s26[c][5] == fig["claims_per_week"][nm], "workbook summer 2026 " + nm)
    print("checks: %d assertions passed (call %s %s; rung 0 %s %.2fx; rung 1 %s %.2fx; rung 2 %s %.2fx; golden lead "
          "%.2fx over %s; flip %d%%; realised 2026 %s; leaks rung 0 %d, rung 1 %d, rung 2 %d)" % (
              N[0], W.NAME[F["pick"]], "{:,}".format(fig["pick_total"]), rank["gross"][0], lead("gross"),
              rank["average"][0], lead("average"), rank["interval"][0], lead("interval"), lead("actual"),
              W.NAME[ru], k, rr[0], leaks_g, leaks_a, leaks_i))
