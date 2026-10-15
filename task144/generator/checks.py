"""task144's assertions, run on every build: the three-rules block on the clean truth (R1 to R3c), every semantic
fork row (SF1 to SF16), the ladder (winners, margins, positions, dominance, the twin pair, the back-test), the bins
and the readings' spreads, the asks and their device profiles, the separation of the asks from the call, the input
gates, the distractors and the realism sweep."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import tempfile

import numpy as np

import calc as C
import common as K

N = {"pass": 0}


def ok(cond, label, detail=""):
    if not cond:
        raise AssertionError("%s FAILED %s" % (label, detail))
    N["pass"] += 1
    print("  ok  %-58s %s" % (label, detail))


def k(x):
    return K.round_to(x, 1000)


def edge(x, step=1000):
    """Distance from x to the nearest rounding edge of its bin."""
    r = (x / step) % 1
    return min(abs(r - 0.5), 1.5 - r if r > 0.5 else r + 0.5) * step


def same_figures(G0, G1):
    a = {r["name"]: (k(r["total"])) for r in G0["rows"]}
    b = {r["name"]: (k(r["total"])) for r in G1["rows"]}
    return G0["pick"]["name"] == G1["pick"]["name"] and a == b and k(G0["pick"]["lift"]) == k(G1["pick"]["lift"])


# ---------------------------------------------------------------------------------------------------- clean truth

def clean_truth(W):
    """The rungs on the world before any export is written (no file, no mess): the generator's own stars."""
    acc = W.accounts.by_id
    cut = K.CUT

    def ext(r):
        mem = set(W.members[r.id])
        return [s for s in r.stars if s.first and acc[s.account].type != "bot" and s.account not in mem
                and K.day_index(r.public, s.t) <= 100 and s.t <= cut]

    def daily(r):
        d = np.zeros(102)
        for s in ext(r):
            kk = K.day_index(r.public, s.t)
            if 1 <= kk <= 100:
                d[kk] += 1
        return d
    spot = [r for r in W.lottery if r.drawn]
    runners = [r for r in W.lottery if not r.drawn and r.public.date() + dt.timedelta(days=89) <= cut.date()]
    dd = {r.id: daily(r) for r in runners}

    def G(a):
        return sum(dd[r.id][a + 1:91].sum() for r in runners) / sum(dd[r.id][a - 6:a + 1].mean() for r in runners)
    nl = [s for r in spot for s in r.stars if s.first and s.surface == "newsletter" and K.day_index(r.public, s.t) <= 100]
    fR = float(np.mean([acc[s.account].followers for s in nl]))
    fd = [s for r in W.repos if r.shipped_events for s in r.stars if s.first and s.surface == "feed"
          and K.day_index(r.public, s.t) <= 100 and s.t <= cut]
    f2 = float(np.mean([acc[s.account].followers for s in fd]))
    D_by = {r.issue: sum(1 for s in ext(r) if s.surface == "newsletter") for r in spot}
    rate = sum(D_by.values()) / sum(W.list[ym] for ym in D_by)
    D = rate * W.list[K.OCT]
    lifts, bases, L = [], [], []
    for r in spot:
        if r.public.date() + dt.timedelta(days=89) > cut.date():
            continue
        a = K.day_index(r.public, K.ISSUE_SEND[r.issue]) - 1
        d = daily(r)
        base = d[1:a + 1].sum() + d[a - 6:a + 1].mean() * G(a)
        lifts.append(d[1:91].sum() - base)
        bases.append(base)
        L.append(W.list[r.issue])
    Lbar = np.mean(lifts) * W.list[K.OCT] / np.mean(L)
    pbar = sum(lifts) / sum(bases)
    out = {}
    for r in W.october:
        a = K.day_index(r.public, cut)
        d = daily(r)
        base = d[1:a + 1].sum() + d[a - 6:a + 1].mean() * G(a)
        st = [s for s in r.stars if s.first and s.t <= cut]
        c = sum(1 for s in st if s.surface == "feed") / sum(acc[s.account].followers for s in st)
        e = ext(r)
        Kf = sum(1 for s in e if s.surface == "feed") / len(e)
        out[r.name] = dict(R0=base + Lbar, R1=base * (1 + pbar), R2=base + D / (1 - Kf),
                           R3=base + D * (1 + c * fR / (1 - c * f2)), base=base, c=c, K=Kf)
    win = {rung: max(out, key=lambda n: out[n][rung]) for rung in ("R0", "R1", "R2", "R3")}
    return out, win, dict(fR=fR, f2=f2, rate=rate, D=D, Lbar=Lbar)


# ---------------------------------------------------------------------------------------------------- the run

def run(target, golden, W=None, meta_path=None):
    print("checks: task144")
    B = C.load(target)
    R = C.rungs(B)
    G = R["G"]
    X = G["X"]
    rows = {r["name"]: r for r in G["rows"]}
    out = R["out"]
    rk = R["ranks"]
    A = C.load_asks(target)
    AA = C.ask_a(B, A)
    AB = C.ask_b(B, A)

    # ---------------------------------------------------------------- the three rules (R1 to R3c)
    print("three rules")
    heads = []
    for f in os.listdir(target):
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            heads += open(p, encoding="utf-8-sig").readline().strip().lower().replace(";", ",").split(",")
    banned = [h for h in heads if re.search(r"rate|lift|forecast|expected|reach|multiplier|cascade|viral|per_view", h)]
    ok(not banned, "R1 no shipped column holds a rate, reach, lift or forecast", "headers checked: %d" % len(heads))
    ok(len(B["events"]) > 150_000 and B["unmapped_codes"] == 0,
       "R1 raw material: star events at the account grain", "%d events, every v5 code mapped" % len(B["events"]))
    ok(all(r["expo"] > 0 and r["feed"] > 0 for r in G["rows"]),
       "R1 the decisive rate reads feed stars and every starrer's followers",
       ", ".join("%s %d/%d" % (r["name"], r["feed"], r["expo"]) for r in G["rows"]))
    # R2: each mess item mishandled leaves the call and its figures where they were
    variants = {
        "R2 v5 surface codes left unmapped": None,
        "R2 restars and every star event counted": {"all_events": True},
        "R2 stars net of later unstars": {"net_unstars": True},
        "R2 bots kept": {"keep_bots": True},
        "R2 members by the current snapshot": {"members_now": True},
        "R2 Amsterdam days for the window": {"amsterdam_days": True},
        "R2 lottery 2026 sheet only": {"rate_issues": "2026", "fR": "2026"},
    }
    for label, opts in variants.items():
        if opts is None:
            B2 = C.load(target)
            ev = B2["events"]
            ev.loc[ev.t < K.SCHEMA_V6, "surface"] = None
            G1 = C.golden(B2, {"rate_issues": "v6"})
            ok(same_figures(G, G1), label, "pick %s, %s" % (G1["pick"]["name"], ", ".join(
                "%s %d" % (r["name"][:5], r["total"]) for r in G1["rows"][:3])))
            continue
        G1 = C.golden(B, opts)
        ok(same_figures(G, G1), label, "pick %s, %s" % (G1["pick"]["name"],
                                                         ", ".join("%s %d" % (r["name"][:5], r["total"]) for r in G1["rows"][:3])))
    roll_eq = all(np.array_equal(C.daily_from_rollup(B, r["rid"])[1:r["a"] + 1], r["daily"][1:r["a"] + 1]) for r in G["rows"])
    ok(roll_eq, "R2 rollup and events agree for the shortlist", "daily external stars equal day by day")
    # R3a, R3b on the clean truth and on the pack
    truth, twin, tk = clean_truth(W) if W is not None else (None, None, None)
    if truth is not None:
        ok(twin["R0"] == "tracewire", "R3a analyst test on the clean truth files tracewire",
           "R0 %s %.0f" % (twin["R0"], truth["tracewire"]["R0"]))
        ok(twin["R3"] == "slidewell" and twin["R1"] != "slidewell" and twin["R2"] != "slidewell",
           "R3b only the decisive step files slidewell", "R1 %s, R2 %s, R3 %s" % (twin["R1"], twin["R2"], twin["R3"]))
        ok(all(abs(truth[n]["R3"] - out[n]["R3"]) < 1e-6 for n in truth),
           "R3 clean truth and pack agree to zero drift", "seven expected totals equal")
    ok(rk["R0"]["winner"] == "tracewire", "R3a default path on the pack files tracewire",
       "%.0f, the spotlight adding %.0f" % (out["tracewire"]["R0"], R["Lbar"]))
    ok(rk["R3"]["winner"] == "slidewell", "R3b decisive step on the pack files slidewell",
       "%.0f, adding %.0f" % (rows["slidewell"]["total"], rows["slidewell"]["lift"]))
    memo = pdf_text(os.path.join(target, K.MEMO))
    words = [w for w in ("average", "lift", "follower", "feed", "cascade", "lottery's effect", "per view", "multiplier",
                         "pace", "trajectory", "forecast") if w in memo.lower()]
    nums = [n for n in re.findall(r"\b\d[\d,.]*\b", memo) if n not in ("1.1", "1.2", "2.1", "2.2", "2.3", "2.4", "3.1",
                                                                      "3.2", "3.3", "4.1", "4.2", "5.1", "5.2", "1",
                                                                      "2", "3", "4", "5", "90", "90th", "6", "2026",
                                                                      "2025", "20", "23", "27", "30", "09:00", "15",
                                                                      "09", "00", "7")]
    ok(not words and not nums, "R3c no decoy: the memo names no method and no figure", "method words %s, numbers %s" % (words, nums))
    ok(not repeated_blocks(B), "R3c no copied block in the star stream", "no repeated 50-event run across repositories")

    # ---------------------------------------------------------------- the semantic fork table
    print("semantic forks")
    for sf, opts in (("SF1", {"all_events": True}), ("SF1", {"net_unstars": True}), ("SF1", {"members_now": True})):
        G1 = C.golden(B, opts)
        moved = max(abs(G1_r["total"] - rows[G1_r["name"]]["total"]) / rows[G1_r["name"]]["total"] for G1_r in G1["rows"])
        ok(same_figures(G, G1) and moved < 0.02, "%s external stars, reading %s" % (sf, list(opts)[0]),
           "largest move %.2f per cent" % (100 * moved))
    for opts in ({"hour_window": True}, {"amsterdam_days": True}):
        ok(same_figures(G, C.golden(B, opts)), "SF2 window from the %s" % ("public hour" if "hour_window" in opts else
                                                                             "Amsterdam day"), "same pick and bins")
    ok(rk["direct"]["winner"] == "tracewire", "SF3 the newsletter's own stars only file tracewire",
       "%.0f against slidewell %.0f" % (out["tracewire"]["direct"], out["slidewell"]["direct"]))
    lifts = np.array([l["lift"] for l in R["L"]])
    med = float(np.median(lifts)) * X["subs_oct"] / np.mean([l["subs"] for l in R["L"]])
    r0med = max(rows, key=lambda n: rows[n]["base"] + med)
    ok(r0med == "tracewire", "SF4 expected: a median lift keeps the default on tracewire; the golden is a mean",
       "median lift %.0f" % med)
    octrow = X["octrow"]
    pubs = [B["public"][rid] for rid in octrow["shortlist"]]
    ok(len(octrow["shortlist"]) == 7 and min(pubs) >= dt.datetime(2026, 8, 24) and max(pubs) <= dt.datetime(2026, 9, 8),
       "SF5 the shortlist: the lottery log's October row", "seven ids, public 24 Aug to 7 Sep")
    ok(B["events"].t.max() <= K.CUT, "SF6 no event after the extract's last second", str(B["events"].t.max()))
    ok(same_figures(G, C.golden(B, {"all_events": True})), "SF7 a restar counted again", "same pick and bins")
    ok(same_figures(G, C.golden(B, {"keep_bots": True})), "SF8 bots kept", "same pick and bins")
    ok(same_figures(G, C.golden(B, {"members_now": True})), "SF9 members by the current snapshot", "same pick and bins")
    ok(same_figures(G, C.golden(B, {"list_september": True})), "SF10 the September issue's list instead",
       "same pick and bins")
    merged = set(B["accounts"].account_id[B["accounts"].merged_into.notna()])
    cand_starrers = set(B["events"][B["events"].repo.isin(octrow["shortlist"])].account)
    ok(not (merged & cand_starrers), "SF11 no merged account starred a candidate", "%d merged accounts" % len(merged))
    sep = [x for x in X["past"] if x["issue"] == dt.date(2026, 9, 1)][0]
    ev = B["events"]
    gap = K.CUT - C.send_utc(sep["issue"])
    late = tot = 0
    for x in X["past"]:
        if x["issue"] >= dt.date(2026, 9, 1):
            continue
        nl_x = ev[(ev.repo == x["drawn"]) & (ev.surface == "newsletter") & (ev.action == "star")]
        late += int((nl_x.t > C.send_utc(x["issue"]) + gap).sum())
        tot += len(nl_x)
    ok(late <= 0.002 * tot, "SF12 the September spotlight's newsletter stars are complete by the extract",
       "earlier issues: %d of %d newsletter stars came later than %d days after the send" % (late, tot, gap.days))
    for opts in ({"rate_issues": "2026"}, {"rate_issues": "last6"}):
        ok(same_figures(G, C.golden(B, opts)), "SF13 direct rate from %s issues" % opts["rate_issues"], "same pick and bins")
    for opts in ({"fR": "2026"}, {"fR": "issue_mean"}):
        ok(same_figures(G, C.golden(B, opts)), "SF14 readers' reach, %s" % opts["fR"], "same pick and bins")
    for opts in ({"f2": "candidates"}, {"f2": "spotlights"}):
        ok(same_figures(G, C.golden(B, opts)), "SF15 feed starrers' reach, %s" % opts["f2"], "same pick and bins")
    comp = all(k(k(r["base"]) + k(r["lift"])) == k(r["total"]) for r in G["rows"])
    ok(comp, "SF16 rounding once or per component gives the same figures", "seven candidates")

    # ---------------------------------------------------------------- the ladder
    print("ladder")
    for rung, name, floor in (("R0", "tracewire", 1.15), ("R1", "tracewire", 1.15), ("R2", "tracewire", 1.15),
                              ("R3", "slidewell", 1.2)):
        ok(rk[rung]["winner"] == name and rk[rung]["margin"] >= floor, "rung %s files %s" % (rung, name),
           "margin %.3f, slidewell %d" % (rk[rung]["margin"], rk[rung]["slidewell"]))
    ok(rk["R0"]["slidewell"] in (4, 5), "position: slidewell 4th or 5th on rung 0", "%d" % rk["R0"]["slidewell"])
    ok(rk["R1"]["slidewell"] > 2 and rk["R2"]["slidewell"] > 2, "position: slidewell off the top two on R1 and R2",
       "%d, %d" % (rk["R1"]["slidewell"], rk["R2"]["slidewell"]))
    for rival in ("pace", "direct", "platform", "analogs", "regression"):
        ok(rk[rival]["winner"] != "slidewell", "rival %s files another pick" % rival,
           "%s (margin %.3f)" % (rk[rival]["winner"], rk[rival]["margin"]))
    fg = out["slidewell"]["first"]
    ok(rk["first"]["winner"] == "slidewell" and k(fg) != k(rows["slidewell"]["total"]) and
       k(fg - rows["slidewell"]["base"]) != k(rows["slidewell"]["lift"]),
       "rival first generation: right pick, both figures a bin off", "%.0f, adding %.0f" % (fg, fg - rows["slidewell"]["base"]))
    sw, tw = rows["slidewell"], rows["tracewire"]
    ok(sw["c"] / tw["c"] >= 1.2 * max(tw["base"] / sw["base"], tw["K"] / sw["K"]), "dominance: per-view rate against base and feed share",
       "%.1f against 1.2 x %.2f" % (sw["c"] / tw["c"], max(tw["base"] / sw["base"], tw["K"] / sw["K"])))
    L = {l["issue"]: l for l in R["L"]}
    t1, t2 = L[dt.date(2026, 3, 3)], L[dt.date(2026, 4, 7)]
    close = lambda a, b, tol: abs(a - b) / max(a, b) <= tol
    ok(t1["a"] == t2["a"] and close(t1["S"], t2["S"], 0.05) and close(t1["pace"], t2["pace"], 0.05) and close(t1["K"], t2["K"], 0.05),
       "twin pair: March and April 2026 spotlights alike before the issue",
       "age %d/%d, stars %d/%d, pace %.1f/%.1f, feed share %.3f/%.3f" % (t1["a"], t2["a"], t1["S"], t2["S"], t1["pace"],
                                                                        t2["pace"], t1["K"], t2["K"]))
    ok(t2["lift"] / t1["lift"] >= 1.8 and t2["c"] / t1["c"] >= 5, "twin pair: lifts apart on the per-view rate",
       "lifts %.0f/%.0f, rates %.4f/%.4f" % (t1["lift"], t2["lift"], t1["c"], t2["c"]))
    pred = np.array([X["rate"] * l["subs"] * (1 + l["c"] * X["fR"] / (1 - l["c"] * X["f2"])) for l in R["L"]])
    act = np.array([l["lift"] for l in R["L"]])
    rm_c = float(np.sqrt(np.mean((pred - act) ** 2)))
    rm_m = float(np.sqrt(np.mean((act * 0 + act.mean() - act) ** 2)))
    ok(np.corrcoef(pred, act)[0, 1] >= 0.9 and rm_c < 0.5 * rm_m, "back-test: the cascade explains the lottery's lifts",
       "corr %.3f, RMSE %.0f against %.0f for the average" % (np.corrcoef(pred, act)[0, 1], rm_c, rm_m))
    ok(all(C.day_index(B["public"][r["rid"]], K.OCT_SEND + dt.timedelta(days=21)) <= 90 for r in G["rows"]),
       "axis 22: the cascade runs inside every window", "three weeks after the send is before every day 90")

    # ---------------------------------------------------------------- bins and spreads
    print("bins")
    figs = [("pick total", sw["total"]), ("pick added", sw["lift"])] + [(r["name"], r["total"]) for r in G["rows"]]
    for name, v in figs:
        ok(edge(v) >= 150, "bin: %s" % name, "%.0f, %.0f from the edge" % (v, edge(v)))
    spreads = [{"pace_window": 10}, {"pace_window": 14}, {"drop_last_days": 2}, {"fR": "issue_mean"},
               {"f2": "spotlights"}, {"rate_issues": "last6"}, {"rate_issues": "2026", "fR": "2026"}]
    for opts in spreads:
        G1 = C.golden(B, opts)
        ok(same_figures(G, G1), "spread: %s" % opts, "slidewell %.0f adding %.0f" % (G1["rows"][0]["total"], G1["rows"][0]["lift"]))
    for ym, v in AA.items():
        pos = (v["share"] * 100) % 1
        ok(pos <= 0.2 or pos >= 0.8, "bin: click-through %d-%02d" % ym, "%.4f" % v["share"])
    for name, v in AB.items():
        if v["org"]:
            pos = (v["share"] * 100) % 1
            ok(abs(pos - 0.5) >= 0.2, "bin: share outside %s" % name, "%.4f" % v["share"])

    # ---------------------------------------------------------------- the asks
    print("asks")
    profiles_a = {"cracker": dict(sum_all=1, by_label=1, sum_per_campaign=1), "sum_all": dict(sum_all=1),
                  "first_send": dict(first_send=1, clicks_counted_only=1), "one_per_campaign": dict(one_per_campaign=1),
                  "issue_day_counted_clicks": dict(clicks_counted_only=1), "issue_day_label": dict(by_label=1),
                  "issue_day_per_campaign": dict(sum_per_campaign=1), "issue_day_per_link": dict(sum_per_link=1)}
    hits_a = {}
    for name, h in profiles_a.items():
        v = C.ask_a(B, A, h)
        hits_a[name] = sum((v[ym]["delivered"] == AA[ym]["delivered"]) + (v[ym]["share2"] == AA[ym]["share2"]) for ym in AA)
    profiles_b = {"cracker": dict(no_hash_map=1, no_merge_map=1), "hash_only": dict(no_merge_map=1, no_renames=1),
                  "hash_merge_one_hop_renames": dict(single_hop=1), "hash_merge": dict(no_renames=1),
                  "hash_renames": dict(no_merge_map=1)}
    hits_b = {}
    for name, h in profiles_b.items():
        v = C.ask_b(B, A, h)
        hits_b[name] = sum((v[n]["people"] == AB[n]["people"]) + (bool(AB[n]["org"]) and v[n].get("share2") == AB[n]["share2"])
                           for n in AB)
    ok(hits_a["cracker"] == 0 and hits_b["cracker"] == 0, "cracker misses every ask figure", "A %d/12, B %d/12" % (hits_a["cracker"], hits_b["cracker"]))
    ok(max(hits_a.values()) < 12 and max(hits_b.values()) < 12, "no ask whole on fewer than all its devices",
       "A %s; B %s" % (hits_a, hits_b))
    single_b = hits_b["hash_only"]
    one = max(hits_a["issue_day_counted_clicks"], single_b)
    ok(one / 24 < 0.35, "mirror leakage under 35 per cent with one device handled",
       "%d of 24 (Ask A's batches against the Thursday send; Ask B's hashes alone %d)" % (one, hits_b["hash_only"]))
    pair = (38 + 7 + 55 * one / 24 + 5 + 7 + 55 * min(hits_a["cracker"], hits_b["cracker"]) / 24) / 2
    ok(abs(pair - 35.4) < 0.05 and pair <= 40, "pair ceiling at or under 40, as the ask sheet states", "%.1f" % pair)
    n_dev = sum(1 for ym in AA)
    ok(all(AA[ym]["delivered"] < sum_all_delivered(B, A, ym) for ym in AA), "A2 every issue has a Thursday resend",
       "%d issues" % n_dev)
    with tempfile.TemporaryDirectory(dir=os.path.dirname(target)) as tmp:
        for f in os.listdir(target):
            if f not in K.ASK_FILES and f not in K.DISTRACTORS:
                shutil.copy(os.path.join(target, f), tmp)
        Bn = C.load(tmp)
        ok(same_figures(G, C.golden(Bn)) and abs(C.golden(Bn)["pick"]["total"] - sw["total"]) < 1e-6,
           "separation: the call unchanged with every ask file and distractor deleted", "zero drift")
    for f in K.DISTRACTORS:
        with tempfile.TemporaryDirectory(dir=os.path.dirname(target)) as tmp:
            for g in os.listdir(target):
                if g != f:
                    shutil.copy(os.path.join(target, g), tmp)
            Bd = C.load(tmp)
            Ad = C.load_asks(tmp)
            ok(same_figures(G, C.golden(Bd)) and C.ask_a(Bd, Ad) == AA and C.ask_b(Bd, Ad) == AB,
               "distractor deleted: %s" % f[:40], "golden and asks unchanged")

    # ---------------------------------------------------------------- registers and grains (house fixes)
    man = [r["file"] for r in csv_rows(os.path.join(target, K.MANIFEST))]
    ok(set(man) == set(os.listdir(target)) - {K.MANIFEST} and len(man) == len(set(man)),
       "H9 the manifest lists every shipped file once", "%d files" % len(man))
    dic = open(os.path.join(target, K.DICTIONARY), encoding="utf-8").read()
    data_files = [f for f in os.listdir(target) if f.endswith((".csv", ".json", ".parquet", ".xlsx")) and f != K.MANIFEST]
    ok(all(f in dic for f in data_files), "H9 the dictionary names every data file", "%d data files" % len(data_files))
    comp, dd = X["complete"], X["dd"]
    for how in ("mean_of_ratios", "median"):
        moved = True
        for r in G["rows"]:
            vals = [dd[q][r["a"] + 1:91].sum() / dd[q][r["a"] - 6:r["a"] + 1].mean() for q in comp
                    if dd[q][r["a"] - 6:r["a"] + 1].mean() > 0]
            g = float(np.mean(vals)) if how == "mean_of_ratios" else float(np.median(vals))
            moved = moved and k(r["S"] + r["pace"] * g + r["lift"]) == k(r["total"])
        ok(moved, "H14 runners-up ratio pooled or as the %s" % how.replace("_", " "), "every figure in its bin")

    # ---------------------------------------------------------------- input gates and metadata
    print("input gates")
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(files) >= 10 and len(fmts) >= 3, "input gates: files and formats", "%d files, %s" % (len(files), sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8-sig")) for f in files if f.endswith(".csv"))
    ok(big >= 25_000, "input gates: a file of 25,000 rows or more", "%d rows" % big)
    if meta_path:
        meta = json.load(open(meta_path))
        ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]),
           "metadata: two distractors named by bundle path", ", ".join(meta["distractor_files"]))
        ok(all("distractor" not in f for f in files), "no file named after its role", "")

    # ---------------------------------------------------------------- realism sweep
    print("realism")
    totals = [r["total"] for r in G["rows"]]
    ok(len({round(x) for x in totals}) == 7 and all(round(x) % 100 for x in totals), "no round or repeated totals",
       ", ".join("%.0f" % x for x in totals))
    delivered = [v["delivered"] for v in AA.values()]
    ok(len(set(delivered)) == 6 and all(d % 100 for d in delivered), "no round or repeated delivered counts", "")
    people = [v["people"] for v in AB.values()]
    ok(len(set(people)) == 7, "no repeated nominator counts", str(people))
    text = " ".join(open(os.path.join(target, f), encoding="utf-8-sig", errors="ignore").read()
                    for f in files if f.endswith((".md", ".csv", ".json")) and os.path.getsize(os.path.join(target, f)) < 2_000_000)
    text += memo
    ok("—" not in text and "–" not in text, "no em or en dash in the pack", "")
    tells = [w for w in ("leverage", "robust", "comprehensive", "seamless", "delve", "stakeholder", "John Doe", "Acme",
                         "Company A", "lorem") if w.lower() in text.lower()]
    ok(not tells, "no placeholder or generated-text tells", str(tells))
    stamps = {os.path.getmtime(os.path.join(target, f)) for f in files}
    ok(stamps == {K.PACK_STAMP.timestamp()}, "every file stamped at the export", K.PACK_STAMP.isoformat())
    import pandas as pd
    v5max = pd.to_datetime(pd.read_csv(os.path.join(target, K.EV25), usecols=["event_ts_ms"]).event_ts_ms.max(), unit="ms")
    ok(v5max < K.SCHEMA_V6 and B["events"].t.min() >= dt.datetime(2024, 11, 24), "schema vintages split at 2 March 2026",
       "v5 to %s" % v5max)
    people_names = set(K.PEOPLE.values())
    ok(all(n in memo or n in text for n in (K.PEOPLE["editor"], K.PEOPLE["data"])), "personas from guard.py names",
       ", ".join(sorted(people_names)))
    ok(text.count("433812") + text.count("433,812") == 0, "the October list sits in the lottery log only", "")
    print("checks: %d passed" % N["pass"])
    return N["pass"]


def csv_rows(path):
    import csv
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def sum_all_delivered(B, A, ym):
    s, _ = C.issue_sends(A, ym)
    return int(s.delivered.sum())


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(p.extract_text() for p in PdfReader(path).pages)


def repeated_blocks(B, n=50):
    """A run of n consecutive (account, surface) events repeated in another repository's stream."""
    ev = B["events"][B["events"].action == "star"]
    seen = {}
    for rid, g in ev.groupby("repo"):
        acc = list(g.account)
        for i in range(0, max(0, len(acc) - n), n):
            key = tuple(acc[i:i + n])
            if key in seen and seen[key] != rid:
                return True
            seen[key] = rid
    return False
