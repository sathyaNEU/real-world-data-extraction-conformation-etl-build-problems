"""task258's generator checks: the input gates, the ladder (winners, margins, position), the three rules executed on
the clean truth (R1 to R3c), every semantic fork row (SF1 to SF16), the estimator corridor behind every graded
count, both asks' ladders and the separation line, the goldens against figures.json, and the realism sweep."""
from __future__ import annotations

import csv
import json
import os
import re

import numpy as np
import pandas as pd

import analysis as AN
import common as K
import load as L
import world as W

GOOD = K.GOOD_MS


class Checks:
    def __init__(self):
        self.n = 0

    def __call__(self, label, cond, detail=""):
        if not cond:
            raise AssertionError("%s: %s" % (label, detail))
        self.n += 1


def edge_m(x):
    """distance (millions) from a count of page loads to the nearest 100,000 rounding edge"""
    v = x / 1e5
    return abs((v % 1) - 0.5) * 0.1


def rounded(R):
    return {n: AN.round_to(R.loc[n, "golden"], 1e5) for n in AN.NAMES}


def clean_truth():
    """The world before any mess: the Sydney month's beacons once each, true weights, own images from the page
    catalogue, and the engagements' beacons in their windows by Sydney date."""
    W._CATALOGUES.clear()
    nov = W.november_beacons(edges=False)
    nov = nov[nov.lcp_ms.notna()].copy()
    for c in L.PARTS:
        nov[c] = nov[c].astype(float)
    code = nov.origin.str.split(".").str[0]
    nov["prop"] = code.map({p["code"]: p["name"] for p in K.PROPERTIES})
    nov["weight"] = [1.0 / K.rate_at(c, t.to_pydatetime()) for c, t in zip(code, nov.fired_at_utc)]
    own_urls = set()
    for p in K.PROPERTIES:
        cat = W.catalogue(p)
        own_urls |= set(cat["hero_url"][cat["hero"] == "own"])
    nov["own"] = nov.lcp_url.isin(own_urls).to_numpy() & (nov.lcp_element == "IMG").to_numpy()
    eng = W.engagement_beacons()
    win = {w[0]: w[1:] for w in W.engagement_windows()}
    day = AN.sydney_dates(eng.fired_at_utc)
    tag = []
    for eid, d in zip(eng.engagement, day):
        b0, b1, ship, a0, a1 = win[eid]
        tag.append("before" if b0 <= d <= b1 else "after" if a0 <= d <= a1 else "")
    eng["window"] = tag
    return nov, eng[eng.window != ""]


def run(target, golden, st, meta_path):
    ck = Checks()
    fig = st["fig"]["figures"]
    files = sorted(os.listdir(target))

    # ---------------------------------------------------------------- input gates
    ck("gate: 10 or more files", len(files) >= 10, files)
    ck("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ck("gate: a file of 25,000 rows or more", big >= 25000, big)
    meta = json.load(open(meta_path))
    ck("gate: two distractors named in metadata.json", len(meta["distractor_files"]) >= 2 and
       all(f in files for f in meta["distractor_files"]))
    ck("gate: no file named as a distractor", not any("distract" in f.lower() for f in files))
    ck("gate: deliverables present", sorted(os.listdir(golden)) == sorted(K.DELIVERABLES), os.listdir(golden))
    logged = {r["file"] for r in csv.DictReader(open(os.path.join(target, K.EXTRACT_LOG), encoding="utf-8"))}
    ck("H9: the extract log lists every data extract", logged == {f for f in files if f.endswith(".csv")} -
       {K.EXTRACT_LOG}, logged)
    rows = {r["file"]: int(r["rows"]) for r in csv.DictReader(open(os.path.join(target, K.EXTRACT_LOG),
                                                                  encoding="utf-8"))}
    for f, n in rows.items():
        ck("H9: extract log row count for %s" % f,
           n == sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1)

    # ---------------------------------------------------------------- the ladder on the pack
    nov = AN.page_loads(target)
    e = AN.engagement_frame(target)
    eff = AN.effect(e)
    R = AN.rungs(nov, eff)
    want = {"slow_all": "Tideline", "R1_reach": "Hearth", "R2_parts": "Ledger", "R2_whole": "Ledger",
            "R3_zero": "Ledger", "shift": "Ledger", "R4_held": "Pantry", "golden": "Matchday"}
    for col, who in want.items():
        w, v, second, margin = AN.winner(R[col])
        ck("ladder: %s files %s" % (col, who), w == who, (w, v))
        ck("ladder: %s margin 1.15x or more" % col, margin >= 1.15, margin)
    ck("ladder: the golden's margin 1.2x or more", AN.winner(R.golden)[3] >= 1.2)
    for col in ("R2_floor", "R3_floor", "shift_floor"):
        ck("grid: the floor without the level (%s) files Ledger" % col, AN.winner(R[col])[0] == "Ledger",
           AN.winner(R[col]))
    rank = {c: list(R[c].sort_values(ascending=False).index).index("Matchday") + 1 for c in want}
    ck("position: Matchday 4th or 5th on every slow load and on the default path",
       rank["slow_all"] in (4, 5) and rank["R2_parts"] in (4, 5), rank)
    ck("position: Matchday never 1st on an intermediate rung, 2nd on at most one, and there 1.20x behind",
       all(rank[c] > 1 for c in want if c != "golden") and sum(rank[c] == 2 for c in want if c != "golden") <= 1
       and all(AN.winner(R[c])[3] >= 1.2 for c in want if c != "golden" and rank[c] == 2), rank)
    coincide = {c: [n for n in AN.NAMES if AN.round_to(R.loc[n, c], 1e5) == AN.round_to(R.loc[n, "golden"], 1e5)]
                for c in want if c != "golden"}
    ck("mirror: no wrong rung shares more than two of the six rounded counts with the golden (the held rung only "
       "Hearth's and Ledger's)", all(len(v) <= 2 for v in coincide.values()) and
       set(coincide["R4_held"]) == {"Hearth", "Ledger"}, coincide)
    ck("figures: the call", fig["call_property"] == "Matchday" and fig["call_loads_moved_m"] ==
       round(AN.round_to(R.loc["Matchday", "golden"], 1e5) / 1e6, 1))
    ck("engagements: the level the delay settled at is 240 ms", eff["level"] == 240.0, eff["level"])
    afters = [v["after"]["load_delay_ms"] for v in eff["by"].values()]
    befores = [v["before"]["load_delay_ms"] for v in eff["by"].values()]
    ck("engagements: every after-delay within 10 ms of the level, before-delays from under it to over 2,500 ms",
       max(abs(a - 240) for a in afters) <= 10 and min(befores) < 200 and max(befores) > 2500, (afters, befores))
    ratios = [v["after"]["load_time_ms"] / v["before"]["load_time_ms"] for v in eff["by"].values()]
    ck("engagements: the load time scales (every ratio within 0.44 to 0.52)", 0.44 <= min(ratios) and
       max(ratios) <= 0.52, ratios)
    for part in ("ttfb_ms", "fcp_ms"):
        rr = [v["after"][part] / v["before"][part] for v in eff["by"].values()]
        ck("SF10: engagements: %s unchanged (every ratio within 0.95 to 1.05)" % part, 0.95 <= min(rr) and max(rr) <= 1.05,
           rr)
    held_eng = set(K.GATED_ENGAGEMENTS)
    rr = {k: v["after"]["render_delay_ms"] / v["before"]["render_delay_ms"] for k, v in eff["by"].items()}
    ck("SF15: engagements: the render delay held where the pages first painted soon after their first byte",
       all(0.95 <= rr[k] <= 1.05 for k in rr if k not in held_eng), rr)
    ck("SF15: engagements: the render delay rose more than threefold on the two sites whose pages first painted "
       "about three seconds after their first byte", all(rr[k] > 3 for k in held_eng), rr)
    late = {k: float((g.fcp_ms - g.ttfb_ms).median()) for k, g in e.groupby("engagement")}
    ck("SF15: first paint about three seconds after the first byte on those two sites, under 300 ms on the rest",
       all(3000 <= late[k] <= 3250 for k in held_eng) and all(late[k] < 300 for k in late if k not in held_eng), late)
    ck("SF15: no load's LCP before its first contentful paint (November and the engagements)",
       bool((nov.lcp_ms >= nov.fcp_ms).all()) and bool((e.lcp_ms >= e.fcp_ms).all()))
    # the engagements' own loads choose the paint's model: each before window carried through the playbook,
    # floored at its own first paint, lands on the after window's median paint; held, it misses the two sites
    for eid, g in e.groupby("engagement"):
        b, a = g[g.window == "before"], g[g.window == "after"]
        hb = b.ttfb_ms + eff["level"] + eff["r_load"] * b.load_time_ms + b.render_delay_ms
        obs = float(a.lcp_ms.median())
        fl, hd = float(np.maximum(hb, b.fcp_ms).median()), float(hb.median())
        ck("SF15: %s: the floored rebuild of the before window within 5 per cent of the after window's paint" % eid,
           abs(fl / obs - 1) < 0.05, (fl, obs))
        if eid in held_eng:
            ck("SF15: %s: the rebuild with the render delay held misses the after window by over 25 per cent" % eid,
               abs(hd / obs - 1) > 0.25, (hd, obs))
    delay_ratios = [a / b for a, b in zip(afters, befores)]
    ck("engagements: the delay's ratio ranges from under 0.1 to over 1.5 (it is no ratio)",
       min(delay_ratios) < 0.1 and max(delay_ratios) > 1.5, delay_ratios)

    # ---------------------------------------------------------------- the three rules, on the clean truth
    tn, te = clean_truth()
    teff = AN.effect(te)
    TR = AN.rungs(tn, teff)
    ck("R1: the beacons carry each load's four parts and its LCP element", all(c in nov.columns for c in L.PARTS))
    head = open(os.path.join(target, K.BEACONS), encoding="utf-8").readline().strip().split(",")
    ck("R1: no shipped column holds a load's paint after the playbook or a moved flag",
       not any(re.search(r"after|moved|playbook|good", h) for h in head), head)
    ck("R3a: the analyst test, ratios of medians part by part on the clean truth, files Ledger",
       AN.winner(TR.R2_parts)[0] == "Ledger", AN.winner(TR.R2_parts))
    ck("R3a: the preload rule of thumb (no delay) on the clean truth files Ledger", AN.winner(TR.R3_zero)[0] == "Ledger")
    ck("R3a: the delay at the engagements' level with the render delay held files Pantry on the clean truth",
       AN.winner(TR.R4_held)[0] == "Pantry", AN.winner(TR.R4_held))
    ck("R3b: the decisive step (the level, each paint floored at the load's own first paint) files Matchday on the "
       "clean truth", AN.winner(TR.golden)[0] == "Matchday", AN.winner(TR.golden))
    ck("R3b: the floor without the level (a ratio, no delay or a fixed cut) files Ledger on the clean truth",
       all(AN.winner(TR[c])[0] == "Ledger" for c in ("R2_floor", "R3_floor", "shift_floor")))
    ck("R3b: the reach correction alone (every slow own-image load) files Hearth", AN.winner(TR.R1_reach)[0] == "Hearth")
    ck("R3b: clean truth and pack agree on every rounded count", rounded(TR) == rounded(R), (rounded(TR), rounded(R)))
    # R2: every Layer 1 item mishandled leaves the call and the rounded counts where they were
    nd = AN.page_loads(target, dedupe=False)
    ck("R2 SF14: beacons received twice kept: the same call and rounded counts", rounded(AN.rungs(nd, eff)) == rounded(R))
    for clock in ("utc", "ship"):
        ce = AN.effect(AN.engagement_frame(target, clock))
        ck("R2 SF13: review windows read on %s dates: the same rounded counts" % clock,
           rounded(AN.rungs(nov, ce)) == rounded(R))
    utc = AN.page_loads(target, month=(np.datetime64("2026-11-01"), np.datetime64("2026-12-01")))
    RU = AN.rungs(utc, eff)
    ck("R2 SF2: November in UTC: the same call", AN.winner(RU.golden)[0] == "Matchday")
    rates = L.sampling(target)

    def rate_at(origin, t):
        r = None
        for since, rate in rates[origin]:
            if np.datetime64(since) <= t:
                r = rate
        return r
    for which, t in (("first", np.datetime64(K.MONTH_START_UTC)), ("last", np.datetime64(K.MONTH_END_UTC) - 1)):
        pick = {o: rate_at(o, t) for o in rates}
        R1r = AN.rungs(AN.page_loads(target, weights=lambda df, pick=pick: 1.0 / df.origin.map(pick).to_numpy()), eff)
        ck("R2 SF4: one sampling rate a property (the month's %s): the same call" % which,
           AN.winner(R1r.golden)[0] == "Matchday")
        ck("R2 SF4: one rate (the %s) moves a count" % which, rounded(R1r) != rounded(R))
    unw = AN.rungs(AN.page_loads(target, weights=lambda df: np.ones(len(df))), eff)
    for col in ("slow_all", "R1_reach", "R2_parts", "R2_whole", "R3_zero", "shift", "R4_held", "R2_floor", "R3_floor",
                "shift_floor"):
        ck("R2: sampling weights ignored: %s still files a wrong property" % col, AN.winner(unw[col])[0] != "Matchday",
           AN.winner(unw[col]))
    no_pre = nov[nov.navigation_type != "prerender"]
    ck("R2 SF1: prerendered loads left out: the same rounded counts", rounded(AN.rungs(no_pre, eff)) == rounded(R))
    pre = nov[nov.navigation_type == "prerender"]
    ck("R2 SF1: no prerendered load is slower than 2,500 ms", float((pre.lcp_ms > GOOD).sum()) == 0)
    restores = L.beacons(target)
    restores = restores[restores.navigation_type == "back_forward"]
    ck("R2 SF1: back-forward restores report no LCP", restores.lcp_ms.isna().all() and len(restores) > 0)
    hosts = L.hosts(target)
    own_only = nov.copy()
    own_only["own"] = AN.own_image(nov, {n: ({h for h in hs if h.startswith("images.")}, "/nowhere/")
                                         for n, (hs, _) in hosts.items()})
    RO = AN.rungs(own_only, eff)
    ck("R2 SF6: own image host only: the same call", AN.winner(RO.golden)[0] == "Matchday")
    ck("R2 SF6: the alias and CDN paths move counts (the runbook decides)", rounded(RO) != rounded(R))
    ck("R2: the distractors and the ask files are never read by the call",
       not {K.CRUX, K.ANALYTICS, K.IMG_LOGS, K.LEGACY_LOGS, K.AVIF_TABLE, K.CONTRACT, K.DAM} &
       set(meta["call_files"]))
    # R3c: no plant
    b = open(os.path.join(target, K.BEACONS), encoding="utf-8").read().splitlines()[1:]
    body = [ln.split(",", 1)[1] for ln in b]
    ck("R3c: no copied block of beacons (no run of 3 identical consecutive rows past the first column)",
       not any(body[i] == body[i + 1] == body[i + 2] for i in range(len(body) - 2)))
    shipped_text = " ".join(open(os.path.join(target, f), encoding="utf-8").read() for f in files if f.endswith(".md"))
    shipped_text += " ".join(p.extract_text() for f in files if f.endswith(".pdf")
                             for p in __import__("pypdf").PdfReader(os.path.join(target, f)).pages)
    ck("R3c: no shipped document names the experimentation tool, its snippet, consent or a page held from showing",
       not re.search(r"flicker|experiment|consent|snippet|held from|first paint", shipped_text, re.I))
    for doc in (K.RUNBOOK, K.NOTES):
        txt = open(os.path.join(target, doc), encoding="utf-8").read()
        ck("R3c: %s states no load delay, level, ratio or moved count" % doc,
           not re.search(r"\b240\b|\b0\.48\b|\blevel\b|settle|moved into|loads moved", txt))

    # ---------------------------------------------------------------- semantic forks
    ck("SF3: no load on 2,500 ms now", float((nov.lcp_ms == GOOD).sum()) == 0)
    cf = nov.ttfb_ms + eff["level"] + eff["r_load"] * nov.load_time_ms + nov.render_delay_ms
    strict = (nov.lcp_ms > GOOD) & nov.own & (np.maximum(cf, nov.fcp_ms) < GOOD)
    RS = (strict * nov.weight).groupby(nov.prop).sum().reindex(AN.NAMES)
    ck("SF3: under 2,500 ms in place of 2,500 ms or less after the playbook: the same rounded counts",
       {n: AN.round_to(RS[n], 1e5) for n in AN.NAMES} == rounded(R))
    net = {n: AN.round_to(R.loc[n, "golden"] - R.loc[n, "pushed_out"], 1e5) for n in AN.NAMES}
    ck("SF5: net of loads pushed out: the same call and rounded counts", net == rounded(R), (net, rounded(R)))
    ck("SF5: the playbook pushes some loads out (the charter's gross count decides)", R.pushed_out.sum() > 0)
    ck("SF7: every slow load (no reach) files Tideline", AN.winner(R.slow_all)[0] == "Tideline")
    phones = nov[nov.device == "mobile"]
    ck("SF11: phones only: another count", rounded(AN.rungs(phones, eff)) != rounded(R))
    ck("SF12: the extract holds the six www origins only",
       set(L.beacons(target).origin.unique()) == {p["origin"] for p in K.PROPERTIES})
    # SF8 and SF9: the corridor of estimators for the level and the load time's ratio
    A = e[e.window == "after"]
    B = e[e.window == "before"]
    levels = {"median": eff["level"], "mean": float(A.load_delay_ms.mean()),
              "median of medians": float(np.median(afters)), "mean of medians": float(np.mean(afters))}
    rl = {"ratio of medians": eff["r_load"], "mean ratio": float(np.mean(ratios)),
          "median ratio": float(np.median(ratios)),
          "ratio of means": float(A.load_time_ms.mean() / B.load_time_ms.mean())}
    worst = 1.0
    for ln, lv in levels.items():
        for rn, rv in rl.items():
            RV = AN.rungs(nov, eff, level=lv, r_load=rv)
            ck("SF8/SF9: level by %s, load time by %s: the same rounded counts" % (ln, rn), rounded(RV) == rounded(R))
            worst = min(worst, min(edge_m(RV.loc[n, "golden"]) for n in AN.NAMES))
    dev_lv = {d: float(g.load_delay_ms.median()) for d, g in A.groupby("device")}
    dev_rl = {d: float(A[A.device == d].load_time_ms.median() / B[B.device == d].load_time_ms.median())
              for d in ("mobile", "desktop", "tablet")}
    t, u, q, dv = nov.ttfb_ms, nov.load_time_ms, nov.render_delay_ms, nov.device
    reach = (nov.lcp_ms > GOOD) & nov.own
    by_dev = reach & (np.maximum(t + dv.map(dev_lv) + dv.map(dev_rl) * u + q, nov.fcp_ms) <= GOOD)
    RDV = (by_dev * nov.weight).groupby(nov.prop).sum().reindex(AN.NAMES)
    ck("SF8/SF9: level and ratio by device: the same rounded counts",
       {n: AN.round_to(RDV[n], 1e5) for n in AN.NAMES} == rounded(R))
    ecdf = np.sort(A.load_delay_ms.to_numpy())
    slack = GOOD - (t + eff["r_load"] * u + q)
    pr = np.searchsorted(ecdf, slack.to_numpy(), side="right") / len(ecdf)
    REC = pd.Series(reach.to_numpy() * (nov.fcp_ms <= GOOD).to_numpy() * pr * nov.weight.to_numpy(),
                    index=nov.index).groupby(nov.prop).sum()
    ck("SF8: the after-delay's whole distribution in place of its median: the same rounded counts",
       {n: AN.round_to(REC[n], 1e5) for n in AN.NAMES} == rounded(R))
    # SF16: the render work after the first paint counted after the later of the image and the first paint
    ready0 = t + nov.load_delay_ms + u
    ready1 = t + eff["level"] + eff["r_load"] * u
    alt = np.maximum(ready1, nov.fcp_ms) + (nov.lcp_ms - np.maximum(ready0, nov.fcp_ms))
    RA = ((reach & (alt <= GOOD)) * nov.weight).groupby(nov.prop).sum().reindex(AN.NAMES)
    ck("SF16: the paint's own work counted after the later of the image and the first paint: the same rounded counts",
       {n: AN.round_to(RA[n], 1e5) for n in AN.NAMES} == rounded(R))
    worst = min(worst, min(edge_m(RA[n]) for n in AN.NAMES))
    # a partial floor, only where the hero painted in the first paint, keeps the held render delay on the held pages
    # whose hero arrived after the page showed: it files Pantry, and the two held engagements refute it
    held_now = t + eff["level"] + eff["r_load"] * u + q
    partial = np.where(nov.lcp_ms == nov.fcp_ms, np.maximum(held_now, nov.fcp_ms), held_now)
    RP = ((reach & (partial <= GOOD)) * nov.weight).groupby(nov.prop).sum().reindex(AN.NAMES)
    ck("SF15: the floor only where LCP equals the first paint files Pantry", AN.winner(RP)[0] == "Pantry", AN.winner(RP))
    for eid in K.GATED_ENGAGEMENTS:
        b, a = e[(e.engagement == eid) & (e.window == "before")], e[(e.engagement == eid) & (e.window == "after")]
        hb = b.ttfb_ms + eff["level"] + eff["r_load"] * b.load_time_ms + b.render_delay_ms
        pb = np.where(b.lcp_ms == b.fcp_ms, np.maximum(hb, b.fcp_ms), hb)
        ck("SF15: %s: the partial floor misses the after window's paint by over 25 per cent" % eid,
           abs(float(np.median(pb)) / float(a.lcp_ms.median()) - 1) > 0.25)
    worst = min(worst, min(edge_m(R.loc[n, "golden"]) for n in AN.NAMES))
    ck("bins: every graded count at least 25,000 loads from a rounding edge under every estimator", worst >= 0.025,
       worst)

    # ---------------------------------------------------------------- Ask A
    eg = AN.egress(target)
    for n in AN.NAMES:
        gb, aud = eg[n]["gb"], eg[n]["aud"]
        ck("A bins: %s GB at least 0.1 from a rounding edge" % n, abs(gb % 1 - 0.5) >= 0.1, gb)
        ck("A bins: %s AUD at least 0.05 from a rounding edge, and the same from rounded GB" % n,
           abs(aud % 1 - 0.5) >= 0.05 and AN.round_to(round(gb) * L.cdn_rate(target), 1) == AN.round_to(aud, 1), aud)
        ck("A figures: %s" % n, fig["egress_gb"][n] == AN.round_to(gb, 1) and fig["egress_aud"][n] == AN.round_to(aud, 1))
    paths = {"every slot": AN.egress(target, hero_only=False), "304s kept": AN.egress(target, statuses=(200, 304)),
             "UTC month": AN.egress(target, month_utc=False), "no legacy log": AN.egress(target, with_legacy=False)}
    for name, pth in paths.items():
        miss = [n for n in AN.NAMES if AN.round_to(pth[n]["gb"], 1) != fig["egress_gb"][n]]
        if name == "no legacy log":
            ck("A ladder: the no legacy log path misses Hearth and Trailhead", {"Hearth", "Trailhead"} <= set(miss), miss)
        elif name == "UTC month":
            ck("A ladder: the UTC month path misses four properties or more (a hazard)", len(miss) >= 4, miss)
        else:
            ck("A ladder: the %s path misses every property" % name, len(miss) == 6, miss)
    cracker = AN.egress(target, statuses=(200, 304), with_legacy=False)
    ck("A cracker sheet: hero slot read right, 304s and the legacy log missed: every property off",
       all(AN.round_to(cracker[n]["gb"], 1) != fig["egress_gb"][n] for n in AN.NAMES))

    # ---------------------------------------------------------------- Ask B
    gold_b = AN.hero_images(target)
    truth_b = {p["name"]: st["dam_live"][p["code"]] for p in K.PROPERTIES}
    ck("B figures: the pack's count is the world's live hero images", gold_b == fig["hero_images"] and gold_b == truth_b,
       (gold_b, truth_b))
    for how in ("ids", "rows", "content", "all", "property"):
        alt = AN.hero_images(target, how)
        ck("B ladder: counting by %s misses every property" % how, all(alt[n] != gold_b[n] for n in AN.NAMES), alt)
    d = L.dam(target)
    nov_used = d[d.last_used_on >= "2026-11-01"]
    ck("B C1: live read as used in November or later selects the latest crawl's assets",
       set(nov_used.asset_id) == set(d[d.last_used_on == d.last_used_on.max()].asset_id))
    ck("B: every legacy_id names a record in the export", set(d.legacy_id.dropna()) <= set(d.asset_id))
    ck("B: last use is the latest crawl or before October",
       set(d.last_used_on[d.last_used_on > "2026-09-30"]) == {K.LATEST_CRAWL.isoformat()})

    # ---------------------------------------------------------------- separation and documents
    call_text = " ".join(open(os.path.join(target, f), encoding="utf-8").read() for f in (K.RUNBOOK, K.NOTES))
    ck("separation: the call's documents carry no ask device (304, rendition, legacy_id, its own log)",
       not re.search(r"304|rendition|legacy_id|own logs?\b", call_text))
    from pypdf import PdfReader
    charter = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, K.CHARTER)).pages)
    ck("charter: the estimand is filed (2.1 to 2.4)", all(s in charter for s in ("2.1", "2.2", "2.3", "2.4")) and
       "2,500 ms or less" in charter and "Sydney" in charter)
    ck("charter: no model of the playbook's effect", not re.search(r"\b240\b|\b0\.48\b|ratio|level|connection",
                                                                    charter), charter[:200])

    # ---------------------------------------------------------------- goldens
    note = open(os.path.join(golden, K.DELIVERABLES[0]), encoding="utf-8").read()
    for n in AN.NAMES:
        ck("golden note: %s's figures" % n, ("%.1f million" % fig["loads_moved_m"][n]) in note and
           "{:,}".format(fig["egress_gb"][n]) in note and "${:,}".format(fig["egress_aud"][n]) in note and
           "{:,}".format(fig["hero_images"][n]) in note)
    ck("golden note: the call leads", note.splitlines()[0].endswith(fig["call_property"]) and
       "**Send the squad to %s.**" % fig["call_property"] in note)
    png = open(os.path.join(golden, K.DELIVERABLES[1]), "rb").read()
    ck("golden chart: a PNG without the plotting library's name", png[:8] == b"\x89PNG\r\n\x1a\n" and
       b"atplotlib" not in png)

    # ---------------------------------------------------------------- realism sweep
    for f in files + [os.path.join("..", "golden", g) for g in K.DELIVERABLES if g.endswith(".md")]:
        if f.endswith((".csv", ".md")):
            ck("realism: no em dash in %s" % f, "\u2014" not in open(os.path.join(target, f), encoding="utf-8").read())
    for f in files:
        if f.endswith(".pdf"):
            raw = open(os.path.join(target, f), "rb").read()
            ck("H1: %s carries no writer name" % f, b"ReportLab" not in raw and b"reportlab" not in raw)
    vals = [fig[k][n] for k in ("egress_gb", "egress_aud", "hero_images") for n in AN.NAMES]
    ck("realism: no two properties share a graded figure",
       all(len({fig[k][n] for n in AN.NAMES}) == 6 for k in ("loads_moved_m", "egress_gb", "egress_aud",
                                                             "hero_images")))
    ck("realism: no round graded figure", not any(v % 100 == 0 for v in vals if v > 100), vals)
    people = set(K.PEOPLE.values())
    text = " ".join(open(os.path.join(target, f), encoding="utf-8").read() for f in files if f.endswith(".md"))
    named = set(re.findall(r"\b[A-Z][a-z]+ [A-Z][a-z]+(?= \(|,)", text)) - {"Brolga Kids", "Brolga Media"}
    ck("realism: every person named is a drawn persona", named <= people, named)
    dates = L.beacons(target).fired_at_utc
    ck("H16: no beacon after the extract window", dates.max() < np.datetime64(K.EXTRACT_END_UTC))
    ck("H16: no DAM upload after the export", d.uploaded_utc.max() <= "2026-12-03")
    print("checks: %d assertions green" % ck.n)
    return ck.n
