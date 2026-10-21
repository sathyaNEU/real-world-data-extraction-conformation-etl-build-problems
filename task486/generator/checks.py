"""task486 checks on the built pack, the golden and the generator's truth. Every row of the design note's fork table
has an assertion here (SF ids), the ladder is read back from the cut pack against the note's table, and the
three-rules block executes the analyst test on the clean truth."""
import collections
import datetime as dt
import json
import os
import re
import subprocess
import zipfile

import numpy as np

import asks as A
import census as C
import golden as G
import methods as M
import pack as P
import world as W

RESULTS = []
TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    return bool(cond)


def edge(v, unit):
    return unit / 2.0 - abs(v - round(v / unit) * unit)


def _text(path):
    if path.endswith(".docx"):
        import docx
        return "\n".join(p.text for p in docx.Document(path).paragraphs)
    if path.endswith(".pdf"):
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path)
        return "\n".join(" ".join(str(v) for v in r if v is not None) for ws in wb.worksheets
                         for r in ws.iter_rows(values_only=True))
    return open(path, encoding="utf-8").read()


def note_ladder():
    """The design note's ladder table: rung -> (twelve counts), 60 and over then 75 and over."""
    text = open(os.path.join(TASK, "DESIGN_NOTE.md"), encoding="utf-8").read()
    sec = text.split("## Ladder", 1)[1].split("\n## ", 1)[0]
    out = {}
    for line in sec.splitlines():
        m = re.match(r"^\| (R\d) \|[^|]*\| ([\d, ]+) \| ([\d, ]+) \|", line)
        if m:
            nums = lambda s: [int(x.replace(",", "")) for x in s.split()]
            out[m.group(1)] = nums(m.group(2)) + nums(m.group(3))
    return out


def twelve(route_counts):
    return [route_counts["60"][a] for a in W.AREAS] + [route_counts["75"][a] for a in W.AREAS]


def clean_truth(b, draws=40):
    """The release's expected published values over fresh draws of its noise on the same census-day residents: the
    block sum and the block-group route by area, and the truth."""
    acc = {r: {w: collections.Counter() for w in ("60", "75")} for r in ("block_sum", "bg_hu")}
    for k in range(draws):
        rng = np.random.default_rng(W.SEED * 1000 + k)
        rel = C.release(b.blocks, rng)
        for r in acc:
            for w in ("60", "75"):
                for a, v in M.area_counts(b.blocks, rel, r, w).items():
                    acc[r][w][a] += v / draws
    truth = {w: M.truth(b.blocks, w) for w in ("60", "75")}
    return acc, truth


def run(target, gdir, b, meta_path, fig_path):
    RESULTS.clear()
    fig = json.load(open(fig_path))
    f = lambda k: os.path.join(target, P.FILES[k])
    d = G.load(target)
    files = sorted(os.listdir(target))
    gx = {w: G.census(d, "bg_hu", w) for w in ("60", "75")}
    same = lambda dd, **kw: all(abs(G.census(dd, "bg_hu", w, **kw)[a] - gx[w][a]) < 1e-6
                                for w in ("60", "75") for a in W.AREAS)

    # ---------------------------------------------------------------- input gates
    meta = json.load(open(meta_path))
    ok("gate: 10 or more files", len(files) >= 10, "%d" % len(files))
    fmts = {os.path.splitext(n)[1] for n in files}
    ok("gate: 3 or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    nlog = sum(1 for _ in open(f("log"), encoding="utf-8")) - 1
    nblk = sum(1 for _ in open(f("blocks"), encoding="utf-8")) - 1
    ok("gate: a file of 25,000 rows", max(nlog, nblk) >= 25000, "log %d, block table %d" % (nlog, nblk))
    ok("gate: 2 or more distractors", len(meta["distractor_files"]) >= 2, ", ".join(meta["distractor_files"]))
    ok("gate: distractors shipped", all(x in files for x in meta["distractor_files"]))
    ok("gate: no distractor named as such", not any("distract" in n.lower() for n in files))
    ok("H9 metadata lists every shipped file", sorted(x["file"] for x in meta["files"]) == files)
    inv = [r[0] for r in G._rows(f("inventory"))[1]]
    ok("H9 the data inventory lists every shipped file but itself", sorted(inv) == sorted(set(files) - {P.FILES["inventory"]}))
    guide = _text(f("guide"))
    named = [n for n in files if n.endswith(".csv") and not n.startswith(("dhc2020_", "acs2022_"))
             and n != P.FILES["inventory"]]
    ok("H9 the field guide names every agency, county and state file", all(n in guide for n in named),
       ", ".join(n for n in named if n not in guide))
    ok("gate: the large files are the release's block table and the delivery log", nblk == 2839 * 46,
       "%d blocks x 46 cells" % (nblk // 46))

    # ---------------------------------------------------------------- the ladder, read from the cut pack
    lad = note_ladder()
    routes = {"R0": "block_sum", "R1": "bg_points", "R2": "bg_pop", "R3": "tract_hu", "R4": "bg_hu"}
    gold = twelve(fig["counts"])
    for rung, route in routes.items():
        got = twelve(fig["routes"][route])
        ok("ladder: %s (%s) on the pack equals the design note's row" % (rung, route), got == lad.get(rung),
           "%s against %s" % (got, lad.get(rung)))
    off = {rung: sum(1 for x, y in zip(twelve(fig["routes"][route]), gold) if x != y) for rung, route in routes.items()}
    ok("ladder: R0, R1 and R2 miss all twelve counts", off["R0"] == off["R1"] == off["R2"] == 12, str(off))
    ok("ladder: R3 misses six of twelve", off["R3"] == 6, str(off["R3"]))
    ok("ladder: R4 is the golden", off["R4"] == 0)
    mem = {w: M.area_counts(b.blocks, b.rel, "bg_hu", w) for w in ("60", "75")}
    ok("ladder: the pack's golden equals the generator's route in memory",
       all(abs(mem[w][a] - fig["exact"][w][a]) < 1e-3 for w in mem for a in W.AREAS))
    dist = [abs(x - y) // 10 for x, y in zip(twelve(fig["routes"]["block_sum"]), gold)]
    ok("ladder: the block sum sits two tens or more from the golden on every count", min(dist) >= 2, str(dist))
    ok("default path: the block sum files North Kelvane at 850 aged 60 and over",
       fig["routes"]["block_sum"]["60"]["North Kelvane"] == 850 and fig["counts"]["60"]["North Kelvane"] == 700)
    rural_up = all(fig["routes"]["block_sum"][w][a] > fig["counts"][w][a] for w in ("60", "75") for a in W.RURAL_AREAS)
    towns_dn = all(fig["routes"]["block_sum"][w][a] < fig["counts"][w][a] for w in ("60", "75") for a in W.TOWN_AREAS)
    ok("default path: every rural count above the golden, both towns' below", rural_up and towns_dn)
    pct = {a: 100.0 * (fig["routes"]["block_sum"]["60"][a] / float(fig["counts"]["60"][a]) - 1) for a in W.AREAS}
    ok("stump sentence: rural areas 4 to 21 per cent high, towns 1 to 3 per cent low (60 and over, as filed)",
       all(3.5 <= pct[a] < 21.5 for a in W.RURAL_AREAS) and all(-3.5 < pct[a] <= -0.5 for a in W.TOWN_AREAS),
       ", ".join("%s %+.1f" % (a, v) for a, v in pct.items()))
    mn = min(min(fig["edge"][w].values()) for w in fig["edge"])
    ok("bins: every golden count at least 2 persons from the edge of its ten", mn >= 2.0, "nearest %.2f" % mn)
    ok("bins: the nearest edge is 2.3 persons, as the note states (SF5)", round(mn, 1) == 2.3, "%.3f" % mn)

    # ---------------------------------------------------------------- the semantic fork table
    gq_blocks = {P.geoid_block(bl) for bl in b.blocks if bl["gq"]}
    hh = {w: dict(fig["exact"][w]) for w in ("60", "75")}
    for g in gq_blocks:
        hh["60"][d["area"][g]] -= d["block"][g][0]
        hh["75"][d["area"][g]] -= d["block"][g][1]
    ok("SF1 household population only moves both towns' counts (another population)",
       all(M.r10(hh[w][a]) != fig["counts"][w][a] for w in ("60", "75") for a in W.TOWN_AREAS))
    a75_84 = ["P12_%03dN" % k for k in (23, 24, 47, 48)]
    G_AGE75 = G.AGE75
    try:
        G.AGE75 = a75_84
        alt = G.census(d, "bg_hu", "75")
    finally:
        G.AGE75 = G_AGE75
    ok("SF2 75 to 84 moves the 75-and-over counts (another population)",
       sum(1 for a in W.AREAS if M.r10(alt[a]) != fig["counts"]["75"][a]) >= 5)
    old = {w: G.census(d, "block_sum", w, areas=d["area_2016"]) for w in ("60", "75")}
    oldbg = {w: G.census(d, "bg_hu", w, areas=d["area_2016"]) for w in ("60", "75")}
    ok("SF3 the rows before the redraw give another population (North Kelvane 560 by the block sum)",
       M.r10(old["60"]["North Kelvane"]) == 560 and M.r10(old["60"]["North Kelvane"]) != fig["counts"]["60"]["North Kelvane"])
    acs = _acs_counts(f("acs"), d)
    ok("SF4 the ACS five-year table gives other counts (another concept and period)",
       sum(1 for w in ("60", "75") for a in W.AREAS if M.r10(acs[w][a]) != fig["counts"][w][a]) >= 8,
       "%d of 12 differ" % sum(1 for w in ("60", "75") for a in W.AREAS if M.r10(acs[w][a]) != fig["counts"][w][a]))
    parts = _rounded_parts(d)
    ok("SF5 each cut group's parts rounded to whole persons first: every count in the same ten",
       all(M.r10(parts[w][a]) == fig["counts"][w][a] for w in ("60", "75") for a in W.AREAS))
    ok("SF6 the 2026 address points split the cut groups to other counts (R1)", off["R1"] == 12)
    empty = [g for g, h in d["hu"].items() if h == 0 and g not in gq_blocks]
    ok("SF7 every block with no housing units and no group quarters facility is empty in the release",
       all(sum(d["block"][g][2:]) == 0 for g in empty), "%d blocks" % len(empty))
    fac = _facility_blocks(f("facilities"))
    cut = G.cut_groups(d)
    ok("SF8 every facility on the licensing list lies in a block group no boundary cuts",
       fac and all(g[:12] not in cut for g in fac), "%d facilities" % len(fac))
    ok("SF8 the facility blocks have no housing units and publish residents",
       all(d["hu"][g] == 0 and sum(d["block"][g][2:]) > 0 for g in fac))
    tb = {"57041" + r[0].zfill(10) for r in d["assign_rows"]}
    ok("SF9 every assignment row, zero-filled to ten digits, is a block of the release, and every block has a row",
       tb == set(d["hu"]) == set(d["block"]), "%d blocks" % len(tb))
    ties = all(abs(sum(G.census(d, r, w).values()) - fig["county"][w]) < 1e-6
               for r in ("block_sum", "bg_hu", "tract_hu", "bg_pop", "bg_points") for w in ("60", "75"))
    ok("SF10 every route adds to the county's published counts", ties,
       "%d and %d" % (fig["county"]["60"], fig["county"]["75"]))
    ok("SF10 the six rounded counts add to the county's count rounded",
       all(sum(fig["counts"][w].values()) == fig["county_rounded"][w] for w in ("60", "75")))

    # ---------------------------------------------------------------- evidence the release carries (the note's ratios)
    pubs, trues, rur = _ratios(b)
    ok("evidence: inside the cut groups, blocks of one to four housing units publish 1.94 aged 60 and over per unit "
       "against 0.57 for blocks of twenty or more (true 0.59 and 0.65)",
       (round(pubs[0], 2), round(pubs[1], 2), round(trues[0], 2), round(trues[1], 2)) == (1.94, 0.57, 0.59, 0.65),
       "%.3f %.3f true %.3f %.3f" % (pubs[0], pubs[1], trues[0], trues[1]))
    ok("evidence: the whole rural block groups publish 0.80 per unit against a true 0.79",
       (round(rur[0], 2), round(rur[1], 2)) == (0.80, 0.79), "%.3f %.3f" % rur)
    tr_rates = []
    for u in cut:
        tr = u[:11]
        for v in d["bg"]:
            if v[:11] == tr:
                hu = sum(h for g, h in d["hu"].items() if g[:12] == v)
                tr_rates.append(G._ages(d["bg"][v], G.AGE60) / float(hu))
    ok("evidence: the block groups of the cut tracts publish 0.48 to 0.97 aged 60 and over per housing unit",
       (round(min(tr_rates), 2), round(max(tr_rates), 2)) == (0.48, 0.97),
       "%.3f to %.3f" % (min(tr_rates), max(tr_rates)))

    # ---------------------------------------------------------------- the three rules, executed (R1 to R3)
    ok("R1 the release ships at the field's grain: blocks by sex and age, block groups, tracts, housing units",
       len(d["block"]) == 2839 and len(d["bg"]) == fig["n_bg"] and len(d["tract"]) == 25 and len(d["hu"]) == 2839)
    heads = []
    for n in files:
        if n.endswith(".csv"):
            heads += [h.lower() for h in open(os.path.join(target, n), encoding="utf-8").readline().strip().split(",")]
    bad = [h for h in heads if any(w in h for w in ("area_pop", "estimate_60", "aged_60", "provider_count", "bias"))]
    ok("R1 no shipped column holds a provider area's count", not bad, ", ".join(bad))
    area_files = [n for n in files if n.endswith((".csv", ".xlsx", ".txt", ".pdf", ".docx"))
                  and any(a in _text(os.path.join(target, n)) for a in W.RURAL_AREAS)]
    gold_text = {"{:,}".format(v) for w in ("60", "75") for v in fig["counts"][w].values()} | \
                {"{:,}".format(v) for w in ("60", "75") for v in fig["routes"]["block_sum"][w].values()}
    hits = [n for n in area_files if n.endswith((".pdf", ".docx", ".txt"))
            and any(re.search(r"(?<![\d,])%s(?![\d,])" % re.escape(t), _text(os.path.join(target, n))) for t in gold_text)]
    ok("R1 no document states a provider area's count", not hits, ", ".join(hits))
    blanked = dict(d, block={g: [0, 0] + [0] * 46 for g in d["block"]})
    ok("R2 the block table's long layout: the golden never reads it (blanked, the counts stand)", same(blanked))
    as_int = {}
    for tbk, area, code, frm, to in d["assign_rows"]:
        if not to:
            as_int[int(tbk)] = area
    ok("R2 the assignment's numeric block codes read as numbers on both sides give the same areas",
       all(as_int[int(g[5:])] == a for g, a in d["area"].items()))
    ok("R2 the 2023 redraw: under the rows before it no block group is cut, and the block sum and the block-group "
       "route agree to the person (the redraw moves the population, filed in instructions 3, never the estimator)",
       all(abs(old[w][a] - oldbg[w][a]) < 1e-6 for w in ("60", "75") for a in W.AREAS))
    nopts = dict(d, points=collections.Counter())
    ok("R2 the 2026 address points: blanked, the golden stands (they enter only the R1 route)", same(nopts))
    housed = {g: a for g, a in d["area"].items() if d["hu"][g] > 0}
    ok("R2 group quarters blocks dropped with every block of no housing units: the golden unchanged (they lie in "
       "whole groups)", same(d, areas=housed) and all(g[:12] not in cut for g in gq_blocks))
    second = G._rows(f("bgs"))[1][0]
    ok("R2 the downloads' second header row is a label row no reader takes for counts",
       second[0] == "Geography" and not any(x.strip().isdigit() for x in second))
    svc = dict(d, roster={}, episodes=[], log=[], deaths=[], links=[])
    ok("R2 the service records' mess (replays, packs, the route loan, late closures, earlier registry numbers) "
       "touches no row of the census counts", same(svc))
    acc, truth = clean_truth(b)
    diff = {w: {a: acc["block_sum"][w][a] - acc["bg_hu"][w][a] for a in W.AREAS} for w in ("60", "75")}
    ok("R3a analyst test: on the clean truth (40 draws of the release's noise) the block sum puts every rural area "
       "above the block-group route and both towns below it",
       all(diff[w][a] > 0 for w in diff for a in W.RURAL_AREAS) and all(diff[w][a] < 0 for w in diff for a in W.TOWN_AREAS),
       "; ".join("%s %s" % (w, ", ".join("%s %+.0f" % (a.split()[0], diff[w][a]) for a in W.AREAS)) for w in diff))
    ratio = min(abs(acc["block_sum"][w][a] - truth[w][a]) / max(abs(acc["bg_hu"][w][a] - truth[w][a]), 1e-9)
                for w in ("60", "75") for a in W.AREAS)
    ok("R3b on the clean truth the block-group route sits closer to the truth than the block sum on all twelve counts, "
       "three times closer or more", ratio >= 3.0, "smallest ratio %.1f" % ratio)
    ok("R3b the decisive step alone (the block sum's level and split changed) files the golden", off["R4"] == 0)
    ok("R3b each lower rung's single correction files a wrong count", all(off[r] > 0 for r in ("R1", "R2", "R3")))
    rows_bg = [tuple(r.values())[2:] for r in d["bg"].values()]
    ok("R3c no block group's table repeats another's", len(set(rows_bg)) == len(rows_bg))
    big = [tuple(v[2:]) for g, v in d["block"].items() if sum(v[2:]) >= 20]
    ok("R3c no block of 20 or more residents repeats another's 46 cells", len(set(big)) == len(big), "%d blocks" % len(big))
    memo = [n for n in files if n.endswith((".pdf", ".docx", ".txt"))
            and re.search(r"sum(ming)? (the )?blocks|custom area|block groups? (are|is) (more )?accurate|aggregate (the )?blocks"
                          r"|bias|overstat|understat|inflat|drift", _text(os.path.join(target, n)), re.I)]
    ok("R3c no document advises a route or names the drift", not memo, ", ".join(memo))

    # ---------------------------------------------------------------- the asks
    gm, ga = G.meals(d), G.active(d)
    ok("ask A: the golden's meals per provider equal the generator's", gm == A.meals(b.deliveries, b.clients), str(gm))
    ok("ask B: the golden's active clients per provider equal the generator's",
       ga == A.active(b.clients, b.episodes, b.links, b.deaths), str(ga))
    for lab, kw in (("every row counted", dict(cap="none")), ("every repeated client-day item collapsed", dict(cap="all"))):
        m = G.meals(d, **kw)
        ok("ask A device D1: %s misses every provider" % lab, all(m[a] != gm[a] for a in W.AREAS), str(m))
    m = G.meals(d, by="route")
    ok("ask A hazard: by the route's provider moves Wickmoor and North Kelvane (the spring loan)",
       m["Wickmoor City"] > gm["Wickmoor City"] and m["North Kelvane"] < gm["North Kelvane"])
    one = dict(d, meals_per_item={k: 1 for k in d["meals_per_item"]})
    m = G.meals(one)
    ok("ask A hazard: packs counted as one meal move every provider", all(m[a] != gm[a] for a in W.AREAS))
    i = {c: k for k, c in enumerate(d["log_head"])}
    grp = collections.defaultdict(list)
    for r in d["log"]:
        grp[(r[i["client_id"]], r[i["delivery_date"]], r[i["item_code"]])].append(r)
    plan2 = {c for c, r in d["roster"].items() if r["meals_per_day"] == "2"}
    home = G.provider_of_client(d)
    rep, gen = collections.Counter(), collections.Counter()
    gaps_rep, gaps_gen = [], []
    for (c, day, item), rs in grp.items():
        cap = 2 if (item == "HOT" and c in plan2) else 1
        ts = sorted(dt.datetime.strptime(r[i["uploaded_at"]], "%Y-%m-%d %H:%M:%S") for r in rs)
        if len(rs) > cap:
            rep[home[c]] += 1
            gaps_rep.append((ts[cap] - ts[cap - 1]).total_seconds() / 60.0)
        if item == "HOT" and c in plan2:
            gen[home[c]] += 1
            gaps_gen.append((ts[1] - ts[0]).total_seconds() / 60.0)
    ok("ask A device D1: every provider has re-sent rows and genuine two-meal pairs",
       all(rep[a] > 0 and gen[a] > 0 for a in W.AREAS), "re-sent %s; pairs %s" % (dict(rep), dict(gen)))
    lo, hi = 5.0, 70.0
    ok("ask A device D1 fair: upload gaps do not separate a re-sent day from a second meal",
       sum(1 for g in gaps_rep if lo <= g <= hi) >= 20 and sum(1 for g in gaps_gen if lo <= g <= hi) >= 20,
       "re-sent in 5 to 70 minutes %d; second meals %d" % (sum(1 for g in gaps_rep if lo <= g <= hi),
                                                           sum(1 for g in gaps_gen if lo <= g <= hi)))
    a2 = G.active(d, chain=False)
    ok("ask B device D7: the death match joined on the roster's number misses every provider",
       all(a2[a] != ga[a] for a in W.AREAS), str(a2))
    a3 = G.active(d, by="roster")
    ok("ask B hazard: the episode's enrolling provider moves at least one provider (the 2023 redraw)",
       any(a3[a] != ga[a] for a in W.AREAS), str(a3))
    a4 = G.active(d, cutoff=False)
    ok("ask B hazard: deaths after 30 September dropped too moves at least one provider",
       any(a4[a] != ga[a] for a in W.AREAS), str(a4))
    ok("ask B: no Kelvane death, closure or enrolment falls on 30 September 2026 (no reading of 'that day' moves a "
       "figure)", not any(x["date_of_death"] == G.AS_OF for x in d["deaths"]
                          if x["state_participant_id"] in {r["state_participant_id"] for r in d["roster"].values()}
                          | {l["prior_participant_id"] for l in d["links"]})
       and not any(e["closed"] == G.AS_OF or e["enrolled"] == G.AS_OF for e in d["episodes"]))
    ids = {r["state_participant_id"] for r in d["roster"].values()} | {l["prior_participant_id"] for l in d["links"]}
    share = sum(1 for x in d["deaths"] if x["state_participant_id"] not in ids) / float(len(d["deaths"]))
    ok("ask B device D7 fair: most of the statewide death match matches no Kelvane number", share > 0.9, "%.3f" % share)

    # ---------------------------------------------------------------- the pair ceiling, on the cut pack
    import ceiling as CE
    keep = lambda m, a_: sum(m[x] == gm[x] for x in W.AREAS) + sum(a_[x] == ga[x] for x in W.AREAS)
    base = keep(G.meals(d, cap="all"), G.active(d, chain=False))
    mirror_call = sum(1 for x, y in zip(twelve(fig["routes"]["block_sum"]), gold) if x == y)
    cracker = 38.0 + CE.W_INSTR + CE.W_ASK * base
    mirror = CE.W_CALL * mirror_call + CE.W_INSTR + CE.W_ASK * base
    pair = (cracker + mirror) / 2
    ok("ceiling: the pair on the cut pack is 40 or under", pair <= 40.0, "cracker %.1f, mirror %.1f, pair %.1f" % (
        cracker, mirror, pair))
    ok("ceiling: the cut pack's pair equals the generator's", abs(pair - CE.main(quiet=True)) < 1e-9)
    ok("ceiling: the design note's pair ceiling line matches", "Pair ceiling: %.1f" % pair in open(
        os.path.join(TASK, "DESIGN_NOTE.md"), encoding="utf-8").read())

    # ---------------------------------------------------------------- realism sweep
    ok("realism: no round county total", fig["county"]["60"] % 10 and fig["county"]["75"] % 10)
    ok("realism: no round service total", fig["meals_total"] % 10 and fig["active_total"] % 10)
    ok("realism: no large file with a round thousand of rows", nlog % 1000 and nblk % 1000, "%d %d" % (nlog, nblk))
    tells = []
    for n in files + [os.path.join("..", "golden", x) for x in os.listdir(gdir)]:
        p = os.path.join(target, n)
        if p.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as z:
                raw = b"".join(z.read(x) for x in z.namelist())
        else:
            raw = open(p, "rb").read()
        tells += [n for t in (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab", b"matplotlib") if t in raw]
    ok("realism: containers scrubbed (no writing library named in any file, golden included)", not tells,
       ", ".join(tells))
    stamps = []
    for n in files:
        p = os.path.join(target, n)
        if n.endswith((".xlsx", ".docx")):
            core = zipfile.ZipFile(p).read("docProps/core.xml").decode()
            stamps += [(n, s[:10]) for s in re.findall(r"W3CDTF\">([^<]+)<", core)]
        if n.endswith(".pdf"):
            stamps += [(n, "%s-%s-%s" % (s[:4], s[4:6], s[6:8])) for s in re.findall(r"D:(\d{14})", open(p, "rb").read().decode("latin-1"))]
    ok("realism: every document stamp falls between June 2023 and the pull",
       stamps and all("2023-06-01" <= s <= "2026-10-09" for _, s in stamps), str(sorted(set(s for _, s in stamps))))
    late = [n for n in files if dt.date.fromtimestamp(os.path.getmtime(os.path.join(target, n))) > W.PULL]
    ok("realism: every file saved on or before the pull (9 October 2026)", not late, ", ".join(late))
    caps = (("log", "delivery_date", "2026-09-30"), ("log", "uploaded_at", "2026-10-01"), ("deaths", "run_date", "2026-10-05"),
            ("episodes", "closed", "2026-10-09"), ("episodes", "enrolled", "2026-10-09"), ("links", "linked_on", "2026-10-05"),
            ("points", "ADDED", "2026-10-02"), ("assign", "EFFECTIVE_FROM", "2023-07-01"))
    for k, col, cap in caps:
        head, rows = G._rows(f(k))
        j = head.index(col)
        top = max(r[j] for r in rows if r[j])
        ok("realism: %s's %s runs no later than %s (%s)" % (P.FILES[k], col, cap, top[:10]), top[:10] <= cap)
    people = [n for n in files if n.endswith((".pdf", ".txt", ".csv")) and any(
        p in _text(os.path.join(target, n)) for p in W.PEOPLE.values())]
    ok("realism: personas only in document properties", not people, ", ".join(people))
    for n in files:
        p = os.path.join(target, n)
        t = _text(p) if n.endswith((".pdf", ".docx", ".xlsx", ".txt")) else open(p, encoding="utf-8").read()
        ok("no long dashes in %s" % n, "—" not in t and "–" not in t)
    sub = open(os.path.join(os.path.dirname(target), "submission.md"), encoding="utf-8").read()
    ok("no long dashes in submission.md", "—" not in sub and "–" not in sub)
    gx = os.path.join(gdir, G.XLSX)
    ok("no long dashes in the golden", "—" not in _text(gx) and "–" not in _text(gx))
    rpt = _readback(gx)
    ok("golden: the workbook's table carries every graded figure as the write-up states it",
       rpt == {a: (fig["counts"]["60"][a], fig["counts"]["75"][a], fig["meals"][a], fig["active"][a]) for a in W.AREAS},
       str(rpt))
    blocks_md = re.findall(r"^## (.+)$", sub, re.M)
    ok("write-up: exactly the five blocks", blocks_md == ["Tags", "1. Final Recommendation", "2. Critical Components",
                                                          "3. Step-by-Step Solution", "4. Deliverable Answers"],
       str(blocks_md))
    steps = re.findall(r"^\d+\. ", sub.split("## 3.", 1)[1].split("## 4.", 1)[0], re.M)
    ok("write-up: at most eight steps", len(steps) <= 8, "%d" % len(steps))
    fc = subprocess.run(["python3", os.path.join(TASK, "..", ".claude", "skills", "determinism-check", "figures_check.py"),
                         os.path.basename(TASK), "--quiet"], capture_output=True, text=True, cwd=os.path.join(TASK, ".."))
    ok("write-up: figures_check.py passes", fc.returncode == 0, fc.stdout.strip().splitlines()[-1] if fc.stdout else "")
    for key in ("cut_rural_60", "cut_rural_75"):
        v = fig["exact_parts"][key]
        ok("bins: component %s at least one person from the edge of its ten" % key, edge(v, 10.0) >= 1.0,
           "%.3f" % edge(v, 10.0))
    sp = _rounded_parts(d, split_sum=True)
    ok("bins: the cut groups' rural parts rounded group by group first give the same component figures",
       (M.r10(sp["60"]), M.r10(sp["75"])) == (fig["cut_rural_60"], fig["cut_rural_75"]), "%s %s" % (sp["60"], sp["75"]))

    good = all(c for _, c, _ in RESULTS)
    bad = [(n, x) for n, c, x in RESULTS if not c]
    print("checks: %d of %d passed" % (sum(1 for _, c, _ in RESULTS if c), len(RESULTS)))
    for n, x in bad:
        print("  FAIL", n, x)
    return good


# ---------------------------------------------------------------- helpers
def _acs_counts(path, d):
    head, rows = G._rows(path, skip=1)
    est = {}
    for r in rows:
        rec = dict(zip(head, r))
        est[rec["GEO_ID"].replace("1500000US", "")] = rec
    out = {}
    for w in ("60", "75"):
        dd = dict(d, bg={u: {c.replace("B01001_", "P12_")[:-1] + "N": v for c, v in est[u].items()
                             if c.endswith("E") and c.startswith("B01001_")} for u in est})
        out[w] = G.census(dd, "bg_hu", w)
    return out


def _rounded_parts(d, split_sum=False):
    """Each cut group's parts rounded to whole persons before the areas are added."""
    cut = G.cut_groups(d)
    out = {}
    for w, codes in (("60", G.AGE60), ("75", G.AGE75)):
        tot = collections.Counter()
        rural = 0
        for u, rec in d["bg"].items():
            c = G._ages(rec, codes)
            if u not in cut:
                tot[d["area"][[g for g in d["area"] if g[:12] == u][0]]] += c
                continue
            blocks = cut[u]
            areas = sorted({d["area"][g] for g in blocks}, key=W.AREAS.index)
            hu = {a: sum(d["hu"][g] for g in blocks if d["area"][g] == a) for a in areas}
            r_part = int(np.floor(c * hu[areas[-1]] / float(sum(hu.values())) + 0.5))
            tot[areas[-1]] += r_part
            tot[areas[0]] += c - r_part
            rural += r_part
        out[w] = rural if split_sum else tot
    return out


def _facility_blocks(path):
    import openpyxl
    ws = openpyxl.load_workbook(path).worksheets[0]
    return [str(r[5]) for r in ws.iter_rows(min_row=4, values_only=True) if r[0]]


def _ratios(b):
    pub = b.rel["block"]
    cut_small, cut_large, rural = [0, 0, 0], [0, 0, 0], [0, 0, 0]
    for i, bl in enumerate(b.blocks):
        p60, t60 = M.ages(pub[i], "60"), M.ages(bl["cells"], "60")
        if bl["cut"] and 1 <= bl["hu"] <= 4:
            acc = cut_small
        elif bl["cut"] and bl["hu"] >= 20:
            acc = cut_large
        elif bl["kind"] == "rural" and bl["hu"] > 0:
            acc = rural
        else:
            continue
        acc[0] += p60
        acc[1] += t60
        acc[2] += bl["hu"]
    small = (cut_small[0] / float(cut_small[2]), cut_small[1] / float(cut_small[2]))
    large = (cut_large[0] / float(cut_large[2]), cut_large[1] / float(cut_large[2]))
    return (small[0], large[0]), (small[1], large[1]), (rural[0] / float(rural[2]), rural[1] / float(rural[2]))


def _readback(path):
    import openpyxl
    ws = openpyxl.load_workbook(path).worksheets[0]
    out = {}
    for r in ws.iter_rows(min_row=6, max_row=11, values_only=True):
        out[r[0]] = tuple(r[2:6])
    return out
