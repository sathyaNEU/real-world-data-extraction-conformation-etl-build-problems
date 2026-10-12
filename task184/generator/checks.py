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

    # ---- the ladder: rung 0 (roster plus three), rung 1 (stand-down averaged over the unit's day), golden
    ok(rank["gross"][0] == "CUL" and lead("gross") >= 1.15, "rung 0 names Cullinvale by 1.15x")
    ok(rank["gross"].index("HAL") in (3, 4), "Halloran Bay 4th or 5th on rung 0")
    ok(rank["average"][0] == "ESK" and lead("average") >= 1.15, "rung 1 names Eskerford by 1.15x")
    ok(rank["average"].index("HAL") >= 1 and tot["average"]["ESK"] / tot["average"]["HAL"] >= 1.20,
       "Halloran Bay 2nd at most on rung 1, by 1.20x")
    ok(rank["interval"][0] == "HAL" and lead("interval") >= 1.2, "golden Halloran Bay by 1.2x or more")
    ok(len({rank["gross"][0], rank["average"][0], rank["interval"][0]}) == 3, "each rung names its own airport")
    for h in ("average18", "shift"):
        ok(rank[h][0] == "ESK", "the stand-down averaged another way (%s) still names Eskerford" % h)
    ok(rank["uniform2"][0] != "HAL", "Cullinvale's stand-down applied at every host does not name Halloran Bay")
    ok(tot["interval"][rank["interval"][1]] / tot["interval"][rank["interval"][2]] >= 1.10,
       "the golden runner-up clear of the third by 1.10x")
    for c in W.CODES:
        for n in W.DAYS:
            ok(F["sc"]["allday"][c][n] == F["gold"][c][n], "the after-bank windows never bite (%s %s)" % (c, n))
    hourly = {}
    for c in W.CODES:
        hs = 0.0
        for n in W.DAYS:
            r = M.release(c, p[c][n])
            for h in range(4, 22):
                m = (M.HOUR >= h) & (M.HOUR < h + 1)
                r[m] = r[m].mean()
            hs += M.moved(d[c][n], p[c][n], r) * W.DAYS[n]
        hourly[c] = hs
    ok(max(hourly, key=hourly.get) == "HAL" and all(abs(hourly[c] - tot["interval"][c]) < 1e-6 for c in W.CODES),
       "the stand-down by the hour gives the golden")
    real = F["realised"]
    rr = sorted(real, key=lambda c: -real[c])
    ok(rr[0] == "CUL" and real[rr[0]] / real[rr[1]] >= 1.15, "last summer's realised effect names Cullinvale")
    ok(rr.index("HAL") >= 2, "Halloran Bay neither 1st nor 2nd on last summer's realised effect")
    swing = (tot["gross"]["CUL"] / tot["interval"]["CUL"]) / (tot["gross"]["HAL"] / tot["interval"]["HAL"])
    carried = tot["gross"]["CUL"] / tot["gross"]["HAL"]
    ok(swing >= 1.2 * carried, "dominance: the stand-down's swing %.2f against Cullinvale's carried lead %.2f" %
       (swing, carried))
    leaks_g = sum(1 for c in W.CODES if round(tot["gross"][c], -2) == round(tot["interval"][c], -2))
    leaks_a = sum(1 for c in W.CODES if round(tot["average"][c], -2) == round(tot["interval"][c], -2))
    ok(leaks_g <= 1, "rung 0 matches only Halloran Bay's summer figure (%d)" % leaks_g)
    ok(leaks_a == 0, "rung 1 matches no summer figure (%d)" % leaks_a)
    t23 = {}
    for c in W.CODES:
        t23[c] = sum((standard_2023(d[c][n], p[c][n]) - standard_2023(d[c][n], p[c][n] + M.team() -
                                                                        M.release(c, p[c][n]))) * W.DAYS[n]
                     for n in W.DAYS)
    ok(any(round(t23[c], -2) != round(tot["interval"][c], -2) for c in W.CODES),
       "the superseded 2023 basis moves the figures")

    # ---- the flip
    ok(len(set(F["flips"].values())) == 1, "SF8 the flip is the same whether scaled arrivals are rounded or not")
    ok("smallest whole per cent shortfall" in open(os.path.join(os.path.dirname(target), "prompt.txt")).read(),
       "SF8 the prompt asks the smallest whole per cent shortfall at which another posting moves more")
    k, ru = F["flip"], F["runner"]
    best = tot["interval"][ru]
    for mode in ("none", "round", "floor"):
        ok(M.summer(d, p, "HAL", 1 - (k - 1) / 100.0, mode) >= 1.02 * best, "at %d%% Halloran Bay still ahead" % (k - 1))
        ok(M.summer(d, p, "HAL", 1 - k / 100.0, mode) <= 0.98 * best, "at %d%% Halloran Bay behind" % k)

    # ---- memo claims
    for n in W.DAYS:
        a, pl = d["HAL"][n], p["HAL"][n]
        ok(M.queue(a, pl + M.team() - M.release("HAL", pl))[0] == 0, "Halloran Bay within the standard with the unit")
        ok(all(F["gold"]["HAL"][n] > F["gold"][c][n] for c in W.CODES if c != "HAL"), "Halloran Bay first in " + n)
    peak = {c: (W.LANES[c] + W.DEMAND27[c][1]) / W.LANES[c] for c in W.CODES}
    ok(max(peak, key=peak.get) == "HAL", "Halloran Bay's banks the heaviest against its lanes")
    hr = M.release("HAL", p["HAL"]["July"])
    ok(2.0 < hr[M.TEAM_ON].mean() < 2.5 and abs((hr == 4).sum() / 4.0 - 8.75) < 1e-9,
       "Halloran Bay stands down four lanes for 8.75 hours, a little over two lanes averaged")
    ok(all(W.RELEASE[c][0] == 2 for c in W.CODES if c != "HAL") and W.RELEASE["HAL"][0] == 0,
       "two lanes all day at seven hosts, none through Halloran Bay's banks")
    ok(fig["pick_total"] - fig["runner_total"] == AN.rnd100(tot["interval"]["HAL"] - tot["interval"][ru]),
       "the gap reads the same from rounded and unrounded totals")

    # ---- semantic forks
    ok("those outside it on the lanes open with it" in _pdf_text(os.path.join(target, D.STANDARD_26)),
       "SF1 the standard defines the passengers moved")
    for c in W.CODES:
        rs = F["release_seen"][c]
        ok(np.array_equal(rs["min"], rs["max"]), "SF2 %s stood down the same lanes every posted day" % c)
        ok(np.allclose(rs["min"], M.release(c, PR.plan(c))), "SF2 %s stand-down as filed" % c)
        ok(rs["min"].sum() > 0, "SF2 %s stood lanes down" % c)
        ok(np.array_equal(rs["min"], np.round(rs["min"])), "SF7 %s whole lanes" % c)
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
       "SF2 a two-week posting shows the stand-down held")
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
                     "own lanes", "host's lanes", "host lanes"):
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
        ok(pe[c][4] == fig["moved_total"][nm] and pe[c][2] == W.RELEASE[c][0], "workbook posting effect " + nm)
    s26 = {r[1]: r for r in wx["Summer 2026"].iter_rows(min_row=4, max_row=11, values_only=True)}
    for c in W.CODES:
        nm = W.NAME[c]
        ok(s26[c][2] == fig["passengers_2026"][nm] and s26[c][3] == fig["hotel_per_night"][nm] and
           s26[c][5] == fig["claims_per_week"][nm], "workbook summer 2026 " + nm)
    print("checks: %d assertions passed (call %s %s; rung 0 %s %.2fx; rung 1 %s %.2fx; golden lead %.2fx over %s; "
          "flip %d%%; realised 2026 %s; leaks rung 0 %d, rung 1 %d)" % (
              N[0], W.NAME[F["pick"]], "{:,}".format(fig["pick_total"]), rank["gross"][0], lead("gross"),
              rank["average"][0], lead("average"), lead("interval"), W.NAME[ru], k, rr[0], leaks_g, leaks_a))
