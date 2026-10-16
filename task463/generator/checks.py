"""task463 checks: the three rules executed on the clean truth and the pack (R1 to R3c), every semantic fork row, the
ladder, the drift-free comparisons' agreement, each Layer 1 item's neutrality, the asks' stops and edges, the separation
of the call from the asks, the input gates and the realism sweep.

    python3 task463/generator/checks.py
"""
import csv
import datetime as dt
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bundle as B     # noqa: E402
import golden as G     # noqa: E402
import methods as M    # noqa: E402
import world as W      # noqa: E402

GOLD_STAY = ["1105", "1146", "1182"]
STORE = [c for c, n, dip, *_ in W.ITEMS if dip >= 0.25 and c not in GOLD_STAY]
FRESH = [c for c, n, dip, *_ in W.ITEMS if dip < 0.25 and c not in GOLD_STAY]
NEAREST_IN, NEAREST_OUT, UNIT_VALUE_MISS = "1103", "1105", "1211"
DEFAULT_MOVES = None    # set from figures.json: the fresh items, and Pasta and rice when its linked rate lands near the published


def pm_variant(target, keep_all=False, pad=True, gross=True, drop_returns=False, week_start=False):
    """The pack's product-months with one Layer 1 item mishandled at a time."""
    pm = defaultdict(lambda: [0, 0.0])
    off = 0 if not week_start else 6
    rows = list(csv.DictReader(open(B.path(target, "wrenfold"), encoding="utf-8")))
    if not keep_all:
        latest = {}
        for r in rows:
            k = (r["week_ending"], r["gtin"])
            if k not in latest or r["extract_date"] > latest[k]["extract_date"]:
                latest[k] = r
        rows = list(latest.values())
    for r in rows:
        d = dt.date.fromisoformat(r["week_ending"]) - dt.timedelta(days=off)
        m = B.month_key(d)
        if m in B.MONTH_KEYS:
            c = pm[(W.RNAME["W"], r["gtin"], m)]
            c[0] += int(r["units"])
            c[1] += float(r["sales_value"])
    cal = {(r["fiscal_year"], int(r["week"])): dt.date.fromisoformat(r["week_end"])
           for r in csv.DictReader(open(B.path(target, "calendar"), encoding="utf-8"))}
    for r in csv.DictReader(open(B.path(target, "gorsedale"), encoding="utf-8"), delimiter="|"):
        m = B.month_key(cal[(r["FISCAL_YEAR"], int(r["WEEK"]))] - dt.timedelta(days=off))
        if m in B.MONTH_KEYS:
            c = pm[(W.RNAME["G"], r["EAN"].zfill(13) if pad else r["EAN"], m)]
            c[0] += int(r["QTY"])
            c[1] += float(r["SALES"])
    con = sqlite3.connect(B.path(target, "calderby"))
    for d, g, u, v in con.execute("SELECT s.sale_date, k.gtin, s.units, s.net_value FROM daily_sales s JOIN sku_gtin k "
                                  "ON k.sku = s.sku"):
        if drop_returns and u < 0:
            continue
        if d[:7] in B.MONTH_KEYS:
            c = pm[(W.RNAME["C"], g, d[:7])]
            c[0] += int(u)
            c[1] += float(v) * ((1 + W.GST) if gross else 1.0)
    con.close()
    return {k: (u, v) for k, (u, v) in pm.items()}


def rates_of(arr, how="direct"):
    out = {}
    for it in W.ICODE:
        keys, P, Q, E = arr[it]
        if how == "direct":
            x = M.tornqvist(P, Q, E, 0, W.NM - 1)
        elif how == "chained":
            x = M.chained(M.tornqvist, P, Q, E)
        elif how == "chained_fisher":
            x = M.chained(M.fisher, P, Q, E)
        elif how == "jevons":
            x = M.jevons(P, Q, E, 0, W.NM - 1)
        elif how == "chained_jevons":
            x = M.chained(M.jevons, P, Q, E)
        elif how == "unit_value":
            x = M.unit_value(P, Q, E, 0, W.NM - 1)
        out[it] = G.r1(M.rate(x))
    return out


def moved(rates, pub):
    return sorted(it for it in W.ICODE if abs(rates[it] - pub[it]) <= W.LINE + 1e-9)


def components(rates, pub):
    mv = moved(rates, pub)
    st = [it for it in W.ICODE if it not in mv]
    d = {it: G.r1(rates[it] - pub[it]) for it in W.ICODE}
    near_in = max(mv, key=lambda it: (abs(d[it]), it))
    near_out = min(st, key=lambda it: (abs(d[it]), it))
    return (tuple(mv), near_in, d[near_in], near_out, d[near_out])


def truth_arrays(x):
    """The lines' monthly truth (before the feeds cut it), as product-month arrays per item over the panel."""
    out = {}
    for it in W.ICODE:
        Ls = [L for L in x["lines"] if L["item"] == it and L["start"] == 0 and L["end"] == W.NM]
        P = np.full((len(Ls), W.NM), np.nan)
        Q = np.zeros((len(Ls), W.NM))
        for i, L in enumerate(Ls):
            for m in range(W.NM):
                if L["units"][m] > 0:
                    mu = L["member_share"][m] if L["member_price"][m] is not None else 0.0
                    P[i, m] = L["shelf"][m] * (1 - mu) + (L["member_price"][m] or 0) * mu
                    Q[i, m] = L["units"][m]
        ok = ~np.isnan(P).any(1)
        out[it] = (None, P[ok], Q[ok], P[ok] * Q[ok])
    return out


def run(target, golden, x=None, meta_path=None, fig_path=None):
    results = []

    def check(label, cond, detail=""):
        results.append(bool(cond))
        print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [" + str(detail) + "]") if detail != "" else ""))

    F = json.load(open(fig_path or os.path.join(HERE, "figures.json")))
    global DEFAULT_MOVES
    DEFAULT_MOVES = sorted(F["default_moved"])
    pub = B.published_rates(target)
    pm = B.product_months(target)
    cl = B.read_classes(target)
    arr = B.item_arrays(target, pm, cl)
    gold = rates_of(arr, "direct")
    gm = moved(gold, pub)
    base = components(gold, pub)

    # ------------------------------------------------------------------ R1 to R3c, the three rules executed
    feeds_cols = (open(B.path(target, "wrenfold"), encoding="utf-8").readline().strip(),
                  open(B.path(target, "gorsedale"), encoding="utf-8").readline().strip())
    check("R1 the field's raw material ships: product-level sales by week and day, no index, rate or price-change column",
          all(not re.search(r"index|rate|change|relative", h, re.I) for h in feeds_cols)
          and sum(len(arr[it][0]) for it in W.ICODE) > 900, "%d lines compared" % sum(len(arr[it][0]) for it in W.ICODE))
    check("R1 the golden's decisive computation reads the product-month unit values of the lines compared",
          F["lines"] == {it: len(arr[it][0]) for it in W.ICODE})
    if x is not None:
        ta = truth_arrays(x)
        t_default = rates_of(ta, "chained")
        t_gold = rates_of(ta, "direct")
        check("R3a the easy route on the clean truth (linked month-on-month Tornqvist, every filed rule applied) files "
              "the default path's answer", moved(t_default, pub) == DEFAULT_MOVES, moved(t_default, pub))
        check("R3b the easy route with only the decisive step changed (a direct comparison of the two Septembers) "
              "files the golden on the clean truth", moved(t_gold, pub) == gm, len(moved(t_gold, pub)))
        check("R3b each lower rung's single correction leaves the truth on a wrong answer (unweighted 14, unit value "
              "or linked Fisher)", len(moved(rates_of(ta, "jevons"), pub)) == 14
              and moved(rates_of(ta, "unit_value"), pub) != gm and moved(rates_of(ta, "chained_fisher"), pub) != gm)
    d_pack = rates_of(arr, "chained")
    check("R3a the easy route on the pack files the default path's answer, holding all nine items whose goods keep",
          moved(d_pack, pub) == DEFAULT_MOVES and not set(STORE) & set(DEFAULT_MOVES), moved(d_pack, pub))
    check("R3b on the pack only the drift-free comparison files the thirteen", gm == F["moved"] and len(gm) == 13,
          len(gm))
    plan_text = _pdf_text(B.path(target, "plan"))
    check("R3c no plant: no document names a move list, a transaction-data rate, a link, a drift or a multilateral index",
          not re.search(r"chain|link|drift|multilateral|GEKS|direct comparison|offer|promotion|stockpil", plan_text, re.I))
    check("R3c no plant: no copied block (no two lines share a 13-month series of units and unit values in any item)",
          _no_copied_series(arr))
    check("R3c no plant: no offer flag or promotion column in any feed",
          all(not re.search(r"promo|offer|deal", h, re.I) for h in feeds_cols))

    # ------------------------------------------------------------------ the drift-free comparisons agree (C1)
    agree, edge_ok = True, True
    for it in W.ICODE:
        keys, P, Q, E = arr[it]
        vals = list(M.drift_free(P, Q, E).values())
        agree &= len({G.r1(v) for v in vals}) == 1
        edge_ok &= all(abs((abs(v) * 10) % 1 - 0.5) >= 0.15 for v in vals)
    check("C1 direct Tornqvist and Fisher, GEKS on Tornqvist and Fisher, and CCDI give every item the same rate to the "
          "tenth", agree)
    check("C1 every drift-free rate sits 0.015 or more from its tenth's edge", edge_ok)
    below = []
    for it in STORE:
        keys, P, Q, E = arr[it]
        rel = (P[:, -1] / P[:, 0] - 1) * 100
        below.append(M.rate(M.chained(M.tornqvist, P, Q, E)) < rel.min())
    check("C1 in the nine items whose goods keep the linked index ends below every line's own change", all(below))

    # ------------------------------------------------------------------ the ladder
    uv = rates_of(arr, "unit_value")
    jv = rates_of(arr, "jevons")
    cf = rates_of(arr, "chained_fisher")
    cj = rates_of(arr, "chained_jevons")
    check("ladder R0 each item's unit value moves twelve, holding Coffee",
          moved(uv, pub) == sorted(set(gm) - {UNIT_VALUE_MISS}), moved(uv, pub))
    check("ladder R1 unweighted relatives move fourteen, adding Pasta and rice",
          moved(jv, pub) == sorted(gm + ["1105"]), moved(jv, pub))
    check("ladder R2 linked Tornqvist moves the four fresh items, and Pasta and rice",
          DEFAULT_MOVES == sorted(FRESH + ["1105"]))
    check("ladder R2a linked Fisher also holds all nine items whose goods keep", not set(STORE) & set(moved(cf, pub)),
          moved(cf, pub))
    check("ladder R3 the golden moves thirteen; Pasta and rice, Cheese and Chocolate and sweets stay",
          sorted(set(W.ICODE) - set(gm)) == sorted(GOLD_STAY))
    dg = {it: G.r1(gold[it] - pub[it]) for it in W.ICODE}
    check("margins: every moved item within 0.9 of its published rate, every stay 2.1 or more away",
          all(abs(dg[it]) <= 0.9 for it in gm) and all(abs(dg[it]) >= 2.1 for it in GOLD_STAY),
          {W.INAME[it]: dg[it] for it in W.ICODE})
    check("margins: Breakfast cereals the moving item nearest the line, 0.3 or more beyond every other move; Pasta and "
          "rice the staying item nearest it, 0.4 or more inside the other two",
          base[1] == NEAREST_IN and 0.8 <= abs(base[2]) <= 0.9 and all(abs(dg[it]) <= 0.5 for it in gm if it != NEAREST_IN)
          and base[3] == NEAREST_OUT and 2.1 <= abs(base[4]) <= 2.4
          and all(abs(dg[it]) >= 2.8 for it in GOLD_STAY if it != NEAREST_OUT), base)
    dd = {it: G.r1(d_pack[it] - pub[it]) for it in STORE}
    check("margins: the default path's nine wrongly held sit 3.5 to 11 points under their published rates",
          all(-11 <= v <= -3.5 for v in dd.values()), dd)
    check("dominance: the linked index drifts 4.5 or more below the golden in every storable item and 0.4 or less in "
          "the fresh items", all(gold[it] - d_pack[it] >= 4.5 for it in STORE)
          and all(abs(gold[it] - d_pack[it]) <= 0.4 for it in FRESH))
    check("grid: linked weighted 5, linked unweighted 14, drift-free weighted 13, drift-free unweighted 14",
          (len(moved(d_pack, pub)), len(moved(cj, pub)), len(gm), len(moved(jv, pub))) == (5, 14, 13, 14))
    check("worth: every storable item's rate moves 4.5 to 10.5 points between the default path and the golden",
          all(4.5 <= gold[it] - d_pack[it] <= 10.5 for it in STORE))

    # ------------------------------------------------------------------ the design note's figures, recomputed
    r1 = G.r1
    dd_all = [dd[it] for it in STORE]
    drift = [F["linked_drift"][it] for it in STORE]
    check("note: the default path's nine wrongly held sit 4.7 to 8.4 points under (Bottled water nearest, Laundry "
          "furthest)", (min(dd_all), max(dd_all)) == (-8.4, -4.7) and dd["1222"] == -4.7 and dd["5611"] == -8.4,
          (min(dd_all), max(dd_all)))
    check("note: the linked index ends 4.6 to 8.4 points below the golden in the nine items whose goods keep",
          (min(drift), max(drift)) == (4.6, 8.4), (min(drift), max(drift)))
    check("note: the stays sit 2.3 to 2.9 from their published rates, Pasta and rice alone under 2.8; every move but "
          "Breakfast cereals within 0.5", sorted(abs(dg[it]) for it in GOLD_STAY) == [2.3, 2.8, 2.9]
          and max(abs(dg[it]) for it in gm if it != NEAREST_IN) == 0.5)
    check("note: ladder rows (unit value holds Coffee at 1.8 against 5.8; unweighted relatives move Pasta and rice at 2.9; "
          "linked Törnqvist Bread +0.5 and Pasta and rice 2.9; linked Fisher Pasta and rice 3.1, Coffee -5.5)",
          (uv["1211"], r1(uv["1211"] - pub["1211"]), jv["1105"], r1(d_pack["1101"] - pub["1101"]), d_pack["1105"],
           cf["1105"], r1(cf["1211"] - pub["1211"])) == (1.8, -4.0, 2.9, 0.5, 2.9, 3.1, -5.5))
    lo_rel, hi_rel, lo_lnk, hi_lnk = [], [], [], []
    for it in STORE:
        keys, P, Q, E = arr[it]
        rel = (P[:, -1] / P[:, 0] - 1) * 100
        lo_rel.append(rel.min())
        hi_rel.append(rel.max())
        lo_lnk.append(M.rate(M.chained(M.tornqvist, P, Q, E)))
    keys, P, Q, E = arr["5611"]
    laundry = (P[:, -1] / P[:, 0] - 1) * 100
    check("note: the nine items' lines' own changes run -0.8 to +9.3 per cent and their linked indices -0.9 to -5.8; "
          "Laundry products' lines -0.8 to +5.5 against its linked -5.8",
          (r1(min(lo_rel)), r1(max(hi_rel)), r1(max(lo_lnk)), r1(min(lo_lnk)), r1(laundry.min()), r1(laundry.max()),
           r1(M.rate(M.chained(M.tornqvist, P, Q, E)))) == (-0.8, 9.3, -0.9, -5.8, -0.8, 5.5, -5.8))

    # ------------------------------------------------------------------ the semantic fork table
    pooled = _pooled_rates(pm, cl)
    check("SF1 item: the classification's item for each line and month (every in-scope line classified)",
          all(B.item_of(cl, r, g, m) is not None for (r, g, m) in pm if B.item_of(cl, r, g, B.MONTH_KEYS[0]) is not None))
    check("SF2 a GTIN pooled across supermarkets gives the same call", moved(pooled, pub) == gm)
    for label, kw in (("SF3 a week by the month it starts in", dict(week_start=True)),
                      ("SF4 Calderby left net of GST", dict(gross=False)),
                      ("SF4 returns dropped", dict(drop_returns=True)),
                      ("SF10 both extracts of a resent week kept", dict(keep_all=True)),
                      ("SF11 Gorsedale's EANs joined unpadded", dict(pad=False))):
        a2 = B.item_arrays(target, pm_variant(target, **kw), cl)
        check(label + " gives the same call and critical components (R2)", components(rates_of(a2), pub) == base)
    allines = B.item_arrays(target, pm, cl, panel=False)
    r_all = {}
    for it in W.ICODE:
        keys, P, Q, E = allines[it]
        r_all[it] = G.r1(M.rate(M.tornqvist(P, Q, E, 0, W.NM - 1)))
    check("SF5 the lines sold in both Septembers (every line, direct) give the same call and rates (R2)",
          moved(r_all, pub) == gm and r_all == gold)
    check("SF5 every line linked month on month still files the default path's four", moved(rates_of(allines, "chained"),
                                                                                         pub) == DEFAULT_MOVES)
    fish = {it: G.r1(M.rate(M.fisher(*arr[it][1:], 0, W.NM - 1))) for it in W.ICODE}
    lasp = {it: G.r1(M.rate(M.laspeyres(*arr[it][1:], 0, W.NM - 1))) for it in W.ICODE}
    check("SF6 Fisher for Tornqvist: the same sixteen rates; Laspeyres: the same call and critical components",
          fish == gold and components(lasp, pub) == base)
    check("SF7 the 12-month rate runs September 2025 to September 2026, the records starting in September 2025",
          min(m for (_, _, m) in pm) == "2025-09" and max(m for (_, _, m) in pm) == "2026-09")
    unr = {it: M.rate(M.tornqvist(*arr[it][1:], 0, W.NM - 1)) for it in W.ICODE}
    check("SF8 unrounded rates give the same call; no item within 0.6 of the line",
          moved({it: unr[it] for it in W.ICODE}, pub) == gm
          and all(abs(abs(gold[it] - pub[it]) - W.LINE) >= 0.6 for it in W.ICODE))
    pub_from_levels = _published_from_levels(target)
    check("SF9 published rates recomputed from the rounded indices give the same call", moved(gold, pub_from_levels) == gm)
    check("SF12 rates to two decimals give the same call", moved({it: round(unr[it], 2) for it in W.ICODE}, pub) == gm)
    check("SF13 each line's share taken within its supermarket, the supermarkets combined by their spending, gives the "
          "same sixteen rates", _two_stage_rates(arr) == gold)

    # ------------------------------------------------------------------ the asks
    dl = B.delivery_figures(target)
    dl_utc = B.delivery_figures(target, local=False)
    dl_ov = B.delivery_figures(target, week_rule=False)
    dl_first = B.delivery_figures(target, resends=False)
    gA = {r: G.r1(v["average"]) for r, v in dl.items()}
    check("Ask A golden: each supermarket's average days", gA == F["delivery"], gA)
    check("Ask A the cracker (UTC dates) misses every supermarket", all(G.r1(dl_utc[r]["average"]) != gA[r] for r in gA),
          {r: G.r1(v["average"]) for r, v in dl_utc.items()})
    check("Ask A weeks by calendar overlap miss Wrenfold and Gorsedale", all(G.r1(dl_ov[W.RNAME[k]]["average"]) !=
                                                                          gA[W.RNAME[k]] for k in ("W", "G")))
    check("Ask A Wrenfold's resent weeks and Calderby's second extract ignored miss Wrenfold and Calderby's",
          all(G.r1(dl_first[W.RNAME[k]]["average"]) != gA[W.RNAME[k]] for k in ("W", "C")))
    check("Ask A stops as the note states them: UTC 1.8, 7.4, 8.3; calendar overlap 7.9, 20.6; first files 1.7, 8.0, 7.4",
          [G.r1(dl_utc[W.RNAME[k]]["average"]) for k in "WGC"] == [1.8, 7.4, 8.3]
          and [G.r1(dl_ov[W.RNAME[k]]["average"]) for k in "WG"] == [7.9, 20.6]
          and [G.r1(dl_first[W.RNAME[k]]["average"]) for k in "WGC"] == [1.7, 8.0, 7.4])
    check("Ask A each average 0.03 or more from its tenth's edge",
          all(abs((v["average"] * 10) % 1 - 0.5) >= 0.3 for v in dl.values()))
    cov = B.coverage_figures(target)
    cov_code = B.coverage_figures(target, by_name=False)
    cov_trade = B.coverage_figures(target, retail_only=False)
    cov_net = B.coverage_figures(target, gross_up=False)
    gB = {it: int(np.floor(cov[it] + 0.5)) for it in W.ICODE}
    check("Ask B golden: each item's coverage", gB == {k: v for k, v in F["coverage"].items()})
    check("Ask B the cracker (code join) misses every item by 3 points or more",
          all(abs(cov_code[it] - cov[it]) >= 3.0 for it in W.ICODE), min(abs(cov_code[it] - cov[it]) for it in W.ICODE))
    dB = [abs(cov_code[it] - cov[it]) for it in W.ICODE]
    check("Ask B stops as the note states them: the code join moves every item 3.1 to 39.8 points (Bread 47 against 68, "
          "Toiletries 33 against 73); the golden 55 to 77",
          (round(min(dB), 1), round(max(dB), 1)) == (3.1, 39.8) and (int(np.floor(cov_code["1101"] + 0.5)), gB["1101"]) ==
          (47, 68) and (int(np.floor(cov_code["6213"] + 0.5)), gB["6213"]) == (33, 73) and
          (min(gB.values()), max(gB.values())) == (55, 77))
    check("Ask B the code join stays plausible (every coverage between 30 and 95 per cent)",
          all(30 < cov_code[it] < 95 for it in W.ICODE))
    check("Ask B trade rows kept move the nine items with trade sales; Calderby left net moves every item",
          sum(1 for it in W.ICODE if int(np.floor(cov_trade[it] + 0.5)) != gB[it]) == 9
          and all(cov_net[it] < cov[it] for it in W.ICODE))
    check("Ask B each coverage 0.1 or more from its whole-per-cent edge", all(abs(cov[it] % 1 - 0.5) >= 0.1
                                                                             for it in W.ICODE))

    # ------------------------------------------------------------------ separation and distractors
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            shutil.copy(os.path.join(target, f), tmp)
        for k in ("deliveries", "returns", "catmap", "spending", "quotes", "rsi"):
            os.remove(os.path.join(tmp, W.FILES[k]))
        a3 = B.item_arrays(tmp)
        check("separation: the call and every rung computed with the ask files and distractors deleted are identical",
              rates_of(a3) == gold and rates_of(a3, "chained") == d_pack)
    finally:
        shutil.rmtree(tmp)
    tmp = tempfile.mkdtemp()
    try:
        for k in ("deliveries", "returns", "catmap", "spending", "dict", "plan"):
            shutil.copy(B.path(target, k), tmp)
        check("separation: the asks computed with the feeds, classification, published indices and distractors deleted "
              "are identical", B.coverage_figures(tmp) == cov and
              {r: v["average"] for r, v in B.delivery_figures(tmp).items()} == {r: v["average"] for r, v in dl.items()})
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------ input gates and realism
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("input gates: 10 or more files, 3 or more formats", len(files) >= 10 and len(fmts) >= 3, "%d files, %s" %
          (len(files), sorted(fmts)))
    con = sqlite3.connect(B.path(target, "calderby"))
    n_daily = con.execute("SELECT COUNT(*) FROM daily_sales").fetchone()[0]
    con.close()
    check("input gates: a table of 25,000 rows or more (Calderby's daily sales)", n_daily >= 25000, n_daily)
    if meta_path and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        check("input gates: two or more distractors declared in metadata.json", len(meta["distractor_files"]) >= 2
              and all(d in files for d in meta["distractor_files"]))
    check("realism: no 'distractor' in any file name", not any("distract" in f.lower() for f in files))
    counts = [len(arr[it][0]) for it in W.ICODE]
    check("realism: the items' lines compared are not uniform", len(set(counts)) >= 12, counts)
    tot = {r: 0.0 for r in W.RNAME.values()}
    for (r, g, m), (u, v) in pm.items():
        tot[r] += v
    check("realism: no round retailer totals", all(abs(v - round(v, -3)) > 1 for v in tot.values()))
    check("realism: personas from guard.py names, each once in the plan", plan_text.count(W.PEOPLE["prices"]) == 1)
    check("realism: the plan has no library banner", b"ReportLab" not in open(B.path(target, "plan"), "rb").read())
    check("realism: every file stamped with the folder's date", len({int(os.path.getmtime(os.path.join(target, f)))
                                                                 for f in files}) == 1)
    wk_units = defaultdict(list)
    for r in csv.DictReader(open(B.path(target, "wrenfold"), encoding="utf-8")):
        wk_units[r["week_ending"]].append(int(r["units"]))
    sums = [sum(v) for v in wk_units.values()]
    check("realism: Wrenfold's weekly unit totals all differ", len(set(sums)) == len(sums))
    check("golden: the workbook, the product-month file and the chart exist",
          all(os.path.exists(os.path.join(golden, W.GOLDEN[k])) for k in W.GOLDEN))
    rows = list(csv.reader(open(os.path.join(golden, W.GOLDEN["products"]), encoding="utf-8")))[1:]
    check("golden: the product-month file holds every product-month of the sixteen items",
          len(rows) == F["csv_rows"] and sum(1 for r in rows if r[7] == "Y") == sum(counts) * W.NM)
    good = all(results)
    print("%d checks, %d failed" % (len(results), results.count(False)))
    return good


def _pdf_text(path):
    import subprocess
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    except FileNotFoundError:
        return open(path, "rb").read().decode("latin-1")


def _no_copied_series(arr):
    for it in W.ICODE:
        keys, P, Q, E = arr[it]
        seen = set()
        for p, q in zip(np.round(P, 4), Q):
            t = tuple(p) + tuple(q)
            if t in seen:
                return False
            seen.add(t)
    return True


def _pooled_rates(pm, cl):
    pool = defaultdict(lambda: [0, 0.0])
    for (r, g, m), (u, v) in pm.items():
        it = B.item_of(cl, r, g, m)
        if it in W.INAME:
            c = pool[(it, g, m)]
            c[0] += u
            c[1] += v
    out = {}
    for it in W.ICODE:
        lines = defaultdict(dict)
        for (i2, g, m), (u, v) in pool.items():
            if i2 == it:
                lines[g][m] = (u, v)
        keys = [g for g, ms in lines.items() if all(m in ms and ms[m][0] > 0 for m in B.MONTH_KEYS)]
        P = np.array([[lines[g][m][1] / lines[g][m][0] for m in B.MONTH_KEYS] for g in keys])
        Q = np.array([[lines[g][m][0] for m in B.MONTH_KEYS] for g in keys], dtype=float)
        out[it] = G.r1(M.rate(M.tornqvist(P, Q, P * Q, 0, W.NM - 1)))
    return out


def _two_stage_rates(arr):
    """Each supermarket's Tornqvist over its own lines, combined by the supermarkets' spending shares averaged over the
    two Septembers."""
    import math
    out = {}
    for it in W.ICODE:
        keys, P, Q, E = arr[it]
        ln = 0.0
        for r in sorted({k[0] for k in keys}):
            rows = [i for i, k in enumerate(keys) if k[0] == r]
            w = (E[rows, 0].sum() / E[:, 0].sum() + E[rows, -1].sum() / E[:, -1].sum()) / 2
            ln += w * math.log(M.tornqvist(P[rows], Q[rows], E[rows], 0, W.NM - 1))
        out[it] = G.r1(M.rate(math.exp(ln)))
    return out


def _published_from_levels(target):
    import openpyxl
    ws = openpyxl.load_workbook(B.path(target, "published"), read_only=True)["Item indices"]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[3]
    a, b = head.index("Sep 2025"), head.index("Sep 2026")
    return {str(r[0]): G.r1((r[b] / r[a] - 1) * 100) for r in rows[4:] if r[0]}


if __name__ == "__main__":
    T = os.path.dirname(HERE)
    ok = run(os.path.join(T, "target"), os.path.join(T, "golden"), meta_path=os.path.join(T, "metadata.json"))
    sys.exit(0 if ok else 1)
