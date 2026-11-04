"""checks.py: the generator's assertions on the cut pack and the clean truth. Labels: I input gates, R the three
rules (R1 raw material, R2 per mess item, R3a analyst test, R3b decisive step alone, R3c no plant), L the stem-map
linkage, G the ladder, SF the semantic fork table, A the asks and their devices, X the realism sweep."""
import json
import math
import os
import re
import shutil
import sqlite3
import tempfile

import pdfplumber
from openpyxl import load_workbook

import bundle as B
import golden as G
import world as W

FAILS = []


def chk(label, ok, detail=""):
    print("%s  %s %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)


def truth_sets(x):
    """The clean truth: each stand's share under the tag join and under the golden reading."""
    b, tag, gold = {}, {}, {}
    for t in x["trees"]:
        if not t.get("alive21"):
            continue
        s = t["cst"]
        v = G.ba(t["hist"][2021])
        b[s] = b.get(s, 0) + v
        if t["cut"]:
            continue
        if t["dies"] or t["tagloss"] == "retag":
            tag[s] = tag.get(s, 0) + v
        if t["dies"]:
            gold[s] = gold.get(s, 0) + v
    return (sorted(s for s in b if tag.get(s, 0) / b[s] >= W.LINE), sorted(s for s in b if gold.get(s, 0) / b[s] >= W.LINE))


def fia_route(d, g):
    """Added records too large for ingrowth and standing on no 2021 tree read as trees passed over in 2021 (taken into
    2021 at their 2026 DBH less a typical five-year growth), the tag join otherwise."""
    tag = G.fates(d, g["res"], "TAG")
    missed = {}
    for r in g["res"]["new"]:
        if r["dbh"] >= 7.5:
            st = B.cond_stand(d["reg"], r["plot"], r["cond"])
            missed[st] = missed.get(st, 0) + G.ba(r["dbh"] - 1.2)
    for tg, n in g["res"]["retag"].items():
        st = B.cond_stand(d["reg"], n["plot"], n["cond"])
        missed[st] = missed.get(st, 0) + G.ba(n["dbh"] - 1.2)
    return G.shares(d, tag, missed=missed)


def cnt_route(d, g):
    """Plot netting: on each plot the missing trees' basal area is offset by the added records of 7.5 inches and
    more (at their 2026 DBH less a typical growth), never below zero; no tree is linked."""
    tagf = G.fates(d, g["res"], "TAG")
    big = {}
    for r in g["res"]["added"]:
        if r["dbh"] >= 7.5:
            big[r["plot"]] = big.get(r["plot"], 0) + G.ba(r["dbh"] - 1.2)
    bsum, lost = {}, {}
    per_plot = {}
    for tg, t in d["live21"].items():
        st = B.cond_stand(d["reg"], t["plot"], t["cond"])
        v = G.ba(t["dbh21"])
        bsum[st] = bsum.get(st, 0) + v
        f = tagf[tg][0]
        if f == "dead":
            lost[st] = lost.get(st, 0) + v
        elif f == "missing":
            per_plot.setdefault((t["plot"], st), []).append(v)
    for (p, st), vs in per_plot.items():
        lost[st] = lost.get(st, 0) + max(0.0, sum(vs) - big.get(p, 0) * sum(vs) / max(1e-9, sum(
            sum(v2) for (p2, s2), v2 in per_plot.items() if p2 == p)))
    return {s: dict(share=lost.get(s, 0) / bsum[s]) for s in bsum}


def text_of(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join((pg.extract_text() or "") for pg in pdf.pages)


def main(target, gdir, x):
    del FAILS[:]
    d = B.load(target)
    g = G.compute(d)
    gold = ["CF-112", "CF-138", "CF-152"]
    burned = sorted(W.BURN_DATES)
    tag_set = sorted(gold + burned)

    # ---- I: input gates
    files = []
    for root, _, fs in os.walk(target):
        files += [os.path.relpath(os.path.join(root, f), target) for f in fs]
    chk("I1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    chk("I2 three or more formats", len(fmts) >= 3, ",".join(fmts))
    chk("I3 a table of 25,000 or more rows", d["nmeas"] >= 25000, "tree_meas %d rows" % d["nmeas"])
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    chk("I4 two or more distractors in metadata.json", len(meta["distractor_files"]) >= 2, str(meta["distractor_files"]))
    bad = [f for f in files if re.search(r"readme|dictionar|notes|manifest|codebook|schema", f, re.I)]
    wb = load_workbook(os.path.join(target, W.FILES["register"]), read_only=True)
    bad += [s for s in wb.sheetnames if re.search(r"readme|dictionar|notes|about|key", s, re.I)]
    chk("I5 no file or sheet describing the data", not bad, str(bad))
    tmp = tempfile.mkdtemp()
    t2 = os.path.join(tmp, "target")
    shutil.copytree(target, t2)
    for f in meta["distractor_files"]:
        os.remove(os.path.join(t2, f))
    g2 = G.compute(B.load(t2))
    chk("I6 golden unchanged with every distractor deleted", g2["marked"] == g["marked"] and
        all(abs(g2["pa"][s]["vol"] - g["pa"][s]["vol"]) < 1e-9 for s in g["pa"]))
    shutil.rmtree(tmp)

    # ---- R: the three rules on the clean truth and the pack
    chk("R1a the decisive step reads tree rows (2021 stem map and 2026 added records)",
        len(d["live21"]) > 5000 and len(g["res"]["added"]) > 500,
        "%d 2021 live trees, %d added records" % (len(d["live21"]), len(g["res"]["added"])))
    cols = []
    for f in files:
        if f.endswith(".csv"):
            cols += open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",")
    con = sqlite3.connect(os.path.join(target, W.FILES["db"]))
    for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        cols += [r[1] for r in con.execute("PRAGMA table_info(%s)" % t)]
    cols += [str(c.value) for c in next(load_workbook(os.path.join(target, W.FILES["register"])).active.iter_rows(max_row=1))]
    hit = [c for c in cols if re.search(r"share_lost|mortal|loss|retag|prev|old_tag|former|link|match|same|dup", c, re.I)]
    chk("R1b no shipped column holds the deciding quantity or the link", not hit, str(hit))
    tag_truth, gold_truth = truth_sets(x)
    chk("R3a analyst test: the tag join on the clean truth files the eight stands", tag_truth == tag_set, str(tag_truth))
    chk("R3a the golden reading on the clean truth files the three stands", gold_truth == gold, str(gold_truth))
    tagc = G.compute(d, route="TAG")
    chk("R3b only the decisive step changed: the tag join on the pack files the eight", tagc["marked"] == tag_set)
    chk("R3b the tag join with the added records linked back files the golden", g["marked"] == gold, str(g["marked"]))
    ex = G.compute(d, route="EXCL")
    chk("R3b setting not-found trees aside instead stays wrong (misses the fire stand)", ex["marked"] == ["CF-112", "CF-152"],
        str(ex["marked"]))
    fia = fia_route(d, g)
    chk("R3b the passed-over-tree reading stays wrong", G.marked(fia) == tag_set, str(G.marked(fia)))
    # R2: each mess item mishandled leaves the call and the shares, or moves only its ledgered asks
    r2a = G.compute(d, species_check=False)
    chk("R2 species codes (FIA against company codes) not crosswalked: linkage and shares unchanged",
        r2a["marked"] == gold and {k: v["tag"] for k, v in r2a["res"]["retag"].items()} ==
        {k: v["tag"] for k, v in g["res"]["retag"].items()})
    r2b = G.compute(d, assign="plot", area="plot")
    mv = max(abs(r2b["shares"][s]["share"] - g["shares"][s]["share"]) for s in g["shares"] if s in r2b["shares"])
    chk("R2 conditions ignored (whole plots to their register stand): same call", r2b["marked"] == gold,
        "largest share move %.2f points" % (100 * mv))
    r2c = G.compute(d, heights=False)
    chk("R2 September height revisit ignored: call and shares unchanged", r2c["marked"] == gold and
        all(r2c["shares"][s]["share"] == g["shares"][s]["share"] for s in g["shares"]))
    r2d = G.compute(d, dedupe=False)
    chk("R2 found-tag entries not merged: call and shares unchanged", r2d["marked"] == gold and
        all(r2d["shares"][s]["share"] == g["shares"][s]["share"] for s in g["shares"]))
    cutf = {k: (("dead",) + v[1:] if v[0] == "cut" else v) for k, v in g["fate"].items()}
    chk("R2 cut trees read as lost: same call", G.marked(G.shares(d, cutf)) == gold)
    tags = {}
    for r in d["t26"]:
        tags.setdefault(r["tag"], set()).add(r["plot"])
    chk("R2 padded keys: every 2026 tag sits on one plot, so tag alone and plot with tag join alike",
        all(len(v) == 1 for v in tags.values()))
    con2 = sqlite3.connect(os.path.join(target, W.FILES["db"]))
    orphan = con2.execute("""SELECT COUNT(*) FROM tree_meas a WHERE a.cycle_yr = 2016 AND a.status = 'L' AND NOT EXISTS
                            (SELECT 1 FROM tree_meas b WHERE b.tag = a.tag AND b.cycle_yr = 2021)""").fetchone()[0]
    chk("R2 earlier cycles: every tree live in 2016 has a 2021 record, so the 2021 cycle is the whole population",
        orphan == 0, "%d orphans" % orphan)
    plots_rows = {}
    for r in d["t26"]:
        plots_rows.setdefault(r["plot"], []).append(r["dbh"])
    sig = [tuple(v) for v in plots_rows.values()]
    chk("R3c no copied block: no two plots share a 2026 diameter list", len(set(sig)) == len(sig))

    # ---- L: the stem-map linkage
    res = g["res"]
    chk("L1 no added record has two candidate trees, none stands on a dead or cut tree", not res["amb"] and not res["odd"],
        "%d ambiguous, %d on dead or cut" % (len(res["amb"]), len(res["odd"])))
    base = {k: v["tag"] for k, v in res["retag"].items()}
    conv = []
    for tol in (2.0, 2.5, 3.0, 4.0, 5.0, 6.0):
        for grow in ((-0.4, 3.2), (0.0, 2.6), (-1.0, 4.0), (-5.0, 10.0)):
            for sc in (True, False):
                v = G.resolve(d, tol=tol, grow=grow, species_check=sc)
                conv.append({k: r["tag"] for k, r in v["retag"].items()} == base and v["dup"] == res["dup"] and not v["amb"])
    chk("L2 every tolerance from 2 to 6 feet, every growth window, species on or off: one linkage", all(conv),
        "%d of %d settings" % (sum(conv), len(conv)))
    vm = G.resolve(d, centric="M")
    chk("L2 linking from the trees not found gives the same links", {k: r["tag"] for k, r in vm["retag"].items()} == base)
    alpha = {k: v["company_code"] for k, v in d["spp"].items()}
    on_plot = {}
    for t in d["live21"].values():
        on_plot.setdefault(t["plot"], []).append(t)
    part, other, polar = [], [], True
    dup_partners = set()
    linked_keys = {(v["plot"], v["tag"]) for v in res["retag"].values()}
    for r in res["added"]:
        x1, y1 = G.xy(r["az"], r["dist"])
        ds = sorted((math.hypot(G.xy(t["az"], t["dist"])[0] - x1, G.xy(t["az"], t["dist"])[1] - y1), t["tag"], t)
                    for t in on_plot.get(r["plot"], []))
        key = (r["plot"], r["tag"])
        if key in linked_keys or key in res["dup"]:
            part.append(ds[0][0])
            other.append(ds[1][0])
            t0 = ds[0][2]
            if key in res["dup"]:
                dup_partners.add(t0["tag"])
            daz = abs((r["az"] - t0["az"] + 180) % 360 - 180)
            polar = polar and (daz <= 6 or t0["dist"] < 8) and abs(r["dist"] - t0["dist"]) <= 1.2
        elif ds:
            other.append(ds[0][0])
    chk("L3 partners sit within 2.0 feet; every other tree is 6.0 feet or more away", max(part) <= 2.0 and min(other) >= 6.0,
        "partners up to %.2f ft, nearest other %.2f ft" % (max(part), min(other)))
    chk("L3 an azimuth-and-distance match (6 degrees, 1.2 feet) finds the same partners", polar)
    big_unlinked = [r for r in res["new"] if r["dbh"] >= 7.5]
    far = all(min([math.hypot(G.xy(t["az"], t["dist"])[0] - G.xy(r["az"], r["dist"])[0],
                              G.xy(t["az"], t["dist"])[1] - G.xy(r["az"], r["dist"])[1]) for t in on_plot.get(r["plot"], [])]
                  or [99]) >= 8.0 for r in big_unlinked)
    chk("L4 every linked record is 9.0 inches or more; every unlinked record over 7.5 inches stands 8 feet from any tree",
        min(v["dbh"] for v in res["retag"].values()) >= 9.0 and far,
        "smallest linked %.1f in., %d large unlinked" % (min(v["dbh"] for v in res["retag"].values()), len(big_unlinked)))
    small = max(r["dbh"] for r in res["new"] if r["dbh"] < 7.5)
    chk("L4 every added record under 7.5 inches is new ingrowth size (5.0 to 7.3)", small <= 7.3, "largest %.1f" % small)
    tr = {t["tag"]: t["new_tag"] for t in x["trees"] if t.get("tagloss") == "retag" and t.get("alive21")}
    trd = {t["new_tag"] for t in x["trees"] if t.get("tagloss") == "dup" and t.get("alive21")}
    chk("L5 the linkage recovers the truth exactly (every re-tallied tree, every found-tag entry)",
        base == tr and {k[1] for k in res["dup"]} == trd, "%d links, %d entries" % (len(base), len(res["dup"])))

    # ---- G: the ladder
    sh = {s: 100 * v["share"] for s, v in g["shares"].items()}
    chk("G1 golden marks CF-112, CF-138 and CF-152", g["marked"] == gold, str(g["marked"]))
    chk("G2 the tag join marks the eight", tagc["marked"] == tag_set)
    chk("G3 setting not-found trees aside marks two", ex["marked"] == ["CF-112", "CF-152"])
    gap = min(abs(v - 15) for v in sh.values())
    chk("G4 every stand sits 4 points or more from the line under the golden", gap >= 4.0, "closest %.1f points" % gap)
    tsh = {s: 100 * v["share"] for s, v in tagc["shares"].items()}
    chk("G5 under the tag join every burned stand is 19 per cent or more", min(tsh[s] for s in burned) >= 19.0,
        "lowest %.1f" % min(tsh[s] for s in burned))
    chk("G5 every stand neither burned, beetle-killed nor fire-killed stays under 11 per cent on every route",
        all(max(sh[s], tsh[s], 100 * ex["shares"].get(s, {"share": 0})["share"]) < 11 for s in sh if s not in tag_set))
    chk("G6 setting not-found trees aside leaves the fire stand under 11 per cent",
        100 * ex["shares"]["CF-138"]["share"] < 11.0, "%.1f" % (100 * ex["shares"]["CF-138"]["share"]))
    worth = min(tsh[s] - sh[s] for s in burned)
    chk("G7 the decisive step moves every burned stand 12 points or more", worth >= 12.0, "smallest %.1f" % worth)
    cnt = cnt_route(d, g)
    cheap = [n for n, s in (("tag join", tagc["marked"]), ("not-found aside", ex["marked"]), ("passed-over", G.marked(fia)))
             if s == gold]
    chk("G8 no cheap route (tag join, not-found aside, passed-over) lands the call", not cheap, str(cheap))
    print("      note: plot netting marks %s" % G.marked(cnt))

    # ---- SF: semantic fork table
    chk("SF1 '15 per cent or more' read as more than 15: same call", sorted(s for s, v in sh.items() if v > 15) == gold)
    missed = {}
    for r in big_unlinked:
        st = B.cond_stand(d["reg"], r["plot"], r["cond"])
        missed[st] = missed.get(st, 0) + G.ba(r["dbh"] - 1.2)
    chk("SF2 trees passed over in 2021 taken into the 2021 population: same call",
        G.marked(G.shares(d, g["fate"], missed=missed)) == gold, "%d trees" % len(big_unlinked))
    chk("SF3 trees not found counted as not tallied live is the literal reading and the golden; set aside it moves the call",
        ex["marked"] != gold and g["marked"] == gold)
    cutout = {k: v for k, v in g["fate"].items()}
    sh_cut = G.shares(d, {k: (("unknown",) + v[1:] if v[0] == "cut" else v) for k, v in cutout.items()})
    chk("SF4 cut trees out of both sides: same call", G.marked(sh_cut) == gold)
    k0 = W.BA_K
    W.BA_K = math.pi / 576
    sh_pi = G.shares(d, g["fate"])
    W.BA_K = k0
    chk("SF5 basal area at pi over 576 instead of 0.005454: same call, same shares to the tenth",
        G.marked(sh_pi) == gold and all(G.r1(100 * sh_pi[s]["share"]) == G.r1(sh[s]) for s in sh))
    con3 = sqlite3.connect(os.path.join(target, W.FILES["db"]))
    latest = con3.execute("""SELECT COUNT(*) FROM tree_meas m WHERE m.status = 'L' AND m.cycle_yr = (SELECT MAX(cycle_yr)
                             FROM tree_meas n WHERE n.tag = m.tag AND n.cycle_yr <= 2021) AND m.cycle_yr = 2021""").fetchone()[0]
    chk("SF6 the previous measurement as each tree's latest record to 2021: the same population", latest == len(d["live21"]),
        "%d trees" % latest)
    chk("SF7 conditions ignored: same call", r2b["marked"] == gold)
    mean_plot = {}
    for tg, t in d["live21"].items():
        st = B.cond_stand(d["reg"], t["plot"], t["cond"])
        k = (st, t["plot"])
        a = mean_plot.setdefault(k, [0.0, 0.0])
        a[0] += G.ba(t["dbh21"])
        if g["fate"][tg][0] in ("dead", "missing"):
            a[1] += G.ba(t["dbh21"])
    mp = {}
    for (st, p), (bb, ll) in mean_plot.items():
        mp.setdefault(st, []).append(ll / bb)
    chk("SF8 share as a mean of plot shares: same call", sorted(s for s, v in mp.items() if sum(v) / len(v) >= W.LINE) == gold)
    chk("SF9 stand ids: the register's and the stand table's are one set",
        sorted({r["Stand"] for r in d["reg"].values()}) == sorted(r["stand_id"] for r in d["stands"]))
    chk("SF10 the revisit carries heights only: no status in it", all(isinstance(v, int) for v in d["rev"].values()))
    chk("SF11 rounding the share before the comparison: same call",
        sorted(s for s, v in sh.items() if round(v, 1) >= 15.0) == gold)
    chk("SF12 a tree entered under its found tag and an added tag is live either way",
        dup_partners and all(g["fate"][tg][0] == "live" and tagc["fate"][tg][0] == "live" for tg in dup_partners),
        "%d trees" % len(dup_partners))

    # ---- A: the asks and their devices
    nd = G.per_acre(d, G.live26(d, res, dedupe=False))
    ba_mv = min(abs(round(nd[s]["ba"], 1) - round(g["pa"][s]["ba"], 1)) for s in g["pa"])
    vol_mv = min(abs(G.r10(nd[s]["vol"]) - G.r10(g["pa"][s]["vol"])) for s in g["pa"])
    chk("A1 found-tag entries kept: every stand's live basal area moves 2 bins or more", ba_mv >= 0.2, "smallest %.1f" % ba_mv)
    chk("A1 found-tag entries kept: every stand's net volume moves 2 bins or more", vol_mv >= 20, "smallest %d" % vol_mv)
    wp = G.per_acre(d, G.live26(d, res), area="plot")
    split_st = {r["Stand"] for r in d["reg"].values() if r["Cond 2 stand"]} | \
        {r["Cond 2 stand"] for r in d["reg"].values() if r["Cond 2 stand"]}
    moved = [s for s in g["pa"] if round(wp[s]["ba"], 1) != round(g["pa"][s]["ba"], 1)]
    chk("A2 whole plots per stand: basal area moves on every stand a mapped condition touches",
        set(moved) >= split_st, "%d stands" % len(moved))
    nh = G.per_acre(d, G.live26(d, res), heights=False)
    smoke_st = {B.cond_stand(d["reg"], p, 1) for (p, _) in d["rev"]}
    mv3 = [s for s in g["pa"] if G.r10(nh[s]["vol"]) != G.r10(g["pa"][s]["vol"])]
    chk("A3 revisit heights ignored: volume moves on every stand with a smoke-week plot", set(mv3) >= smoke_st,
        "%d stands" % len(mv3))
    variants = dict(tens=G.per_acre(d, G.live26(d, res), tens=False), cull=G.per_acre(d, G.live26(d, res), cull=False),
                    near=G.per_acre(d, G.live26(d, res), logs_rule="near"))
    for k, v in variants.items():
        n_mv = sum(1 for s in g["pa"] if G.r10(v[s]["vol"]) != G.r10(g["pa"][s]["vol"]))
        chk("A4 volume rule mishandled (%s): moves every stand" % k, n_mv == len(g["pa"]), "%d stands" % n_mv)
    chk("A5 separation: found-tag entries and revisit rows never touch a 2021 tree's fate",
        r2c["fate"] == g["fate"] and r2d["fate"] == g["fate"])
    # rounding paths: per-tree basal area to the thousandth, per-tree net volume to the board foot
    def edge(v, u):
        return u / 2 - abs(v - round(v / u) * u)
    e_sh = min(edge(v, 0.1) for v in sh.values())
    e_ba = min(edge(g["pa"][s]["ba"], 0.1) for s in g["pa"])
    e_vol = min(edge(g["pa"][s]["vol"], 10) for s in g["pa"])
    k0 = W.BA_K
    ba0 = G.ba
    G.ba = lambda dd: round(k0 * dd * dd, 3)
    gr = G.compute(d)
    G.ba = ba0
    same_r = all(G.r1(100 * gr["shares"][s]["share"]) == G.r1(sh[s]) and G.r1(gr["pa"][s]["ba"]) == G.r1(g["pa"][s]["ba"])
                 for s in sh)
    nets = []
    for r in G.live26(d, res):
        if r["dbh"] >= 11.0 and r["fia"] != 818 and (r["merch"] or d["rev"].get((r["plot"], r["tag"]))):
            nets.append(r["cull"] or 0)
    chk("A6 rounding paths: per-tree basal area to the thousandth moves no share and no basal area", same_r,
        "nearest edges: shares %.4f, BA %.4f, volume %.2f" % (e_sh, e_ba, e_vol))
    chk("A6 rounding paths: every tree's net volume is a whole number of board feet (cull in tens of per cent)",
        all(c % 10 == 0 for c in nets), "%d sawtimber records" % len(nets))
    # ---- X: realism sweep
    con4 = sqlite3.connect(os.path.join(target, W.FILES["db"]))
    tg_all = [r[0] for r in con4.execute("SELECT tag FROM tree ORDER BY tag")]
    steps = {b - a for a, b in zip(tg_all, tg_all[1:])}
    pl_all = sorted(d["reg"])
    chk("X1 tag and plot series are not one constant step", len(steps) > 1 and len({b - a for a, b in zip(pl_all, pl_all[1:])}) > 1)
    cnt_pl = {}
    for r in d["reg"].values():
        cnt_pl[r["Stand"]] = cnt_pl.get(r["Stand"], 0) + 1
    chk("X2 plots per stand vary", len(set(cnt_pl.values())) >= 6, str(sorted(set(cnt_pl.values()))))
    notes = [r["Notes"] for r in d["reg"].values() if r["Notes"] and r["Notes"] != "boundary mapped 2021"]
    chk("X3 no free-text note recurs beyond a real rate", max([notes.count(n) for n in set(notes)] or [0]) <= 8)
    pdfs = [f for f in files if f.endswith(".pdf")]
    stump = re.compile(r"re-?tag|lost tag|tags? (?:fell|lost|missing)|duplicat|linked|same tree|stem map|"
                       r"tallied again|found tag", re.I)
    texts = {f: text_of(os.path.join(target, f)) for f in pdfs}
    ctl = "15 per cent" in texts[W.FILES["policy"]] and "aluminium tags" in texts[W.FILES["manual"]]
    chk("X4 positive control: the PDF reader finds known sentences", ctl and all(len(t) > 200 for t in texts.values()))
    from pypdf import PdfReader
    strict = {}
    for f in pdfs:
        try:
            rd = PdfReader(os.path.join(target, f), strict=True)
            strict[f] = " ".join((pg.extract_text() or "") for pg in rd.pages)
        except Exception as e:   # noqa: BLE001
            strict[f] = "ERROR %s" % e
    pol_s = re.sub(r"\s+", " ", strict[W.FILES["policy"]])
    chk("X4 a strict PDF reader opens every shipped PDF and finds the policy's rule",
        all(not v.startswith("ERROR") and len(v) > 200 for v in strict.values()) and "15 per cent or more" in pol_s)
    hits = {f: stump.findall(t) for f, t in texts.items() if stump.findall(t)}
    for f in files:
        if f.endswith(".csv"):
            h = stump.findall(open(os.path.join(target, f), encoding="utf-8").read())
            if h:
                hits[f] = h
    chk("X4 no shipped document or table carries the decisive step's vocabulary", not hits, str(hits)[:200])
    mtxt = json.dumps(meta)
    chk("X5 metadata.json names no mechanism", not stump.search(mtxt) and "link" not in mtxt.lower())
    dates = [r["date"] for r in d["t26"]]
    chk("X6 2026 field dates inside the season, revisit in September, nothing after the pack date",
        min(dates) >= "2026-06-08" and max(dates) <= "2026-08-28")
    fire = texts[W.FILES["fire"]]
    chk("X6 the October 2025 fire report states nothing after its own date", "2026" not in fire)
    chk("X6 the December 2024 burn reports state nothing after their own date", not re.search(r"202[5-9]", texts[W.FILES["burns"]]))
    people = {W.MANAGER, W.FORESTER, W.CHAIR}
    named = set(re.findall(r"\b[A-Z][a-z]+ [A-Z][a-z]+son\b|\b[A-Z][a-z]+ Freeman\b|\b[A-Z][a-z]+ Wolf\b", " ".join(texts.values())))
    chk("X7 every person named in the pack is a drawn persona", named <= people, str(named))
    print("checks: %d failures" % len(FAILS))
    return not FAILS
