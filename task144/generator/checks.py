"""task144's assertions, run on every build: the three-rules block on the clean truth (R1 to R3c), every semantic
fork row (SF1 to SF18), the ladder (winners, margins, positions, dominance, the launch spike, the lottery back-test),
the rate's sampling band, the bins and the readings' spreads, the asks and their device profiles, the separation of
the asks from the call, the input gates, the distractors, the no-description rule and the realism sweep."""
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

# The readings of the rate per view a careful reader might take instead of the golden's (stars from day 8 to the
# extract): another first day, only the last two or three weeks, feed stars counted a day later than the views, the
# last two days' views left out while their feed stars are still arriving.
WINDOWS = [{"post_from": 6}, {"post_from": 7}, {"post_from": 10}, {"post_from": 15}, {"last_days": 14},
           {"last_days": 21}, {"lag": 1}, {"tail": 2}, {"lag": 1, "tail": 2}]


def window_label(o):
    if "post_from" in o:
        return "from day %d" % o["post_from"]
    if "last_days" in o:
        return "over the last %d days" % o["last_days"]
    return "from day 8, %s" % ", ".join("%s %d" % kv for kv in o.items())


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
    m = lambda c: 1 + c * fR / (1 - c * f2)
    for r in W.october:
        a = K.day_index(r.public, cut)
        d = daily(r)
        base = d[1:a + 1].sum() + d[a - 6:a + 1].mean() * G(a)
        st = [s for s in r.stars if s.first and s.t <= cut]
        c_life = sum(1 for s in st if s.surface == "feed") / sum(acc[s.account].followers for s in st)
        late = [s for s in st if K.day_index(r.public, s.t) >= C.POST_FROM]
        c = sum(1 for s in late if s.surface == "feed") / sum(acc[s.account].followers for s in late)
        e = ext(r)
        Kf = sum(1 for s in e if s.surface == "feed") / len(e)
        out[r.name] = dict(R0=base + Lbar, R1=base * (1 + pbar), R2=base + D / (1 - Kf), R3=base + D * m(c_life),
                           R4=base + D * m(c), base=base, c=c, c_life=c_life, K=Kf)
    win = {rung: max(out, key=lambda n: out[n][rung]) for rung in ("R0", "R1", "R2", "R3", "R4")}
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
    truth, win, tk = clean_truth(W) if W is not None else (None, None, None)
    if truth is not None:
        ok(win["R0"] == "tracewire", "R3a analyst test on the clean truth files tracewire",
           "R0 %s %.0f" % (win["R0"], truth["tracewire"]["R0"]))
        ok(win["R3"] == "slidewell", "R3a the whole-life cascade on the clean truth files slidewell",
           "R3 %s %.0f" % (win["R3"], truth["slidewell"]["R3"]))
        ok(win["R4"] == "kilnkit" and "kilnkit" not in (win["R1"], win["R2"], win["R3"]),
           "R3b only the decisive step files kilnkit", "R1 %s, R2 %s, R3 %s, R4 %s" % (
               win["R1"], win["R2"], win["R3"], win["R4"]))
        ok(all(abs(truth[n]["R4"] - out[n]["R4"]) < 1e-6 and abs(truth[n]["R3"] - out[n]["R3"]) < 1e-6 for n in truth),
           "R3 clean truth and pack agree to zero drift", "seven expected totals equal, both cascades")
    ok(rk["R0"]["winner"] == "tracewire", "R3a default path on the pack files tracewire",
       "%.0f, the spotlight adding %.0f" % (out["tracewire"]["R0"], R["Lbar"]))
    ok(rk["R3"]["winner"] == "slidewell", "R3a the whole-life cascade on the pack files slidewell",
       "%.0f, adding %.0f" % (out["slidewell"]["R3"], out["slidewell"]["R3"] - out["slidewell"]["base"]))
    ok(rk["R4"]["winner"] == "kilnkit" and G["pick"]["name"] == "kilnkit", "R3b decisive step on the pack files kilnkit",
       "%.0f, adding %.0f" % (rows["kilnkit"]["total"], rows["kilnkit"]["lift"]))
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
       "%.0f against kilnkit %.0f" % (out["tracewire"]["direct"], out["kilnkit"]["direct"]))
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
    G11 = C.golden(B, {"stars_to_survivor": True})
    ok(same_figures(G, G11) and all(k(a["S"]) == k(b["S"]) for a, b in zip(
        sorted(G["rows"], key=lambda r: r["name"]), sorted(G11["rows"], key=lambda r: r["name"]))),
       "SF11 a merged account's star credited to the account it was merged into", "%d merged accounts, %d of them "
       "starred a candidate (members who later merged their member account away), same pick, bins and stars to date"
       % (len(merged), len(merged & cand_starrers)))
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
    for opts in WINDOWS:
        G1 = C.golden(B, opts)
        ok(same_figures(G, G1), "SF17 the rate per view read %s" % window_label(opts),
           "kilnkit %.0f adding %.0f; slidewell %.0f" % (
               [q for q in G1["rows"] if q["name"] == "kilnkit"][0]["total"],
               [q for q in G1["rows"] if q["name"] == "kilnkit"][0]["lift"],
               [q for q in G1["rows"] if q["name"] == "slidewell"][0]["total"]))
    G1 = C.golden(B, {"rate_external": True})
    ok(same_figures(G, G1), "SF18 the rate per view on external stars only", "pick %s" % G1["pick"]["name"])

    # ---------------------------------------------------------------- the ladder
    print("ladder")
    for rung, name, floor in (("R0", "tracewire", 1.15), ("R1", "tracewire", 1.15), ("R3", "slidewell", 1.15),
                              ("R3k", "slidewell", 1.15), ("R4", "kilnkit", 1.2)):
        ok(rk[rung]["winner"] == name and rk[rung]["margin"] >= floor, "rung %s files %s" % (rung, name),
           "margin %.3f, kilnkit %d" % (rk[rung]["margin"], rk[rung]["golden_place"]))
    ok(rk["R2"]["winner"] != "kilnkit" and rk["R2"]["golden_place"] >= 3, "rung R2 (own feed share) files another pick",
       "%s, kilnkit %d" % (rk["R2"]["winner"], rk["R2"]["golden_place"]))
    ok(rk["R0"]["golden_place"] >= 4, "position: kilnkit 4th or lower on rung 0", "%d" % rk["R0"]["golden_place"])
    ok(rk["R1"]["golden_place"] > 2, "position: kilnkit off the top two on R1", "%d" % rk["R1"]["golden_place"])
    ok(R["kappa"] < 1, "R3k: the lottery scales the whole-life cascade down", "kappa %.3f" % R["kappa"])
    for rival in ("pace", "direct", "platform", "analogs", "regression", "owner"):
        ok(rk[rival]["winner"] != "kilnkit", "rival %s files another pick" % rival,
           "%s (margin %.3f)" % (rk[rival]["winner"], rk[rival]["margin"]))
    kk_ = rows["kilnkit"]
    fg = out["kilnkit"]["first"]
    ok(rk["first"]["winner"] == "kilnkit" and k(fg) != k(kk_["total"]) and k(fg - kk_["base"]) != k(kk_["lift"]),
       "rival first generation: right pick, both figures a bin off", "%.0f, adding %.0f" % (fg, fg - kk_["base"]))
    sw, tw = rows["slidewell"], rows["tracewire"]
    ok(kk_["c"] / tw["c"] >= 1.2 * tw["base"] / kk_["base"], "dominance: kilnkit's rate per view against tracewire's base",
       "%.1f against 1.2 x %.2f" % (kk_["c"] / tw["c"], tw["base"] / kk_["base"]))
    ok(sw["c_life"] >= 2.5 * sw["c"] and abs(kk_["c_life"] / kk_["c"] - 1) <= 0.15,
       "launch spike: slidewell's whole-life rate over two and a half times its day-8 rate, kilnkit's within 15 per cent",
       "slidewell %.4f / %.4f, kilnkit %.4f / %.4f" % (sw["c_life"], sw["c"], kk_["c_life"], kk_["c"]))
    spiked = [l for l in R["L"] if W is not None and [r for r in W.lottery if r.pub == l["rid"]][0].burst >= 600]
    calm = [l for l in R["L"] if W is not None and [r for r in W.lottery if r.pub == l["rid"]][0].burst == 0]
    if W is not None:
        ok(spiked and np.mean([l["c_life"] / l["c_post"] for l in spiked]) >= 1.4 and
           all(l["c_life"] >= l["c_post"] for l in spiked) and
           all(abs(l["c_life"] / l["c_post"] - 1) <= 0.35 for l in calm if l["c_post"] > 0),
           "lottery: launch spikes lift the whole-life rate, calm launches do not",
           "spiked %s; calm max %.2f" % (", ".join("%.2f" % (l["c_life"] / l["c_post"]) for l in spiked),
                                         max(abs(l["c_life"] / l["c_post"] - 1) for l in calm if l["c_post"] > 0)))
    bt = R["backtest"]
    ok(bt["corr_post"] >= 0.95 and bt["post"] <= 0.4 * bt["life"] and bt["post"] <= 0.3 * bt["mean"],
       "back-test: the day-8 cascade explains the lottery's lifts",
       "corr %.3f; RMSE %.0f against %.0f on the whole-life rate and %.0f for the average" % (
           bt["corr_post"], bt["post"], bt["life"], bt["mean"]))
    ok(all(C.day_index(B["public"][r["rid"]], K.OCT_SEND + dt.timedelta(days=21)) <= 90 for r in G["rows"]),
       "axis 22: the cascade runs inside every window", "three weeks after the send is before every day 90")

    # ---------------------------------------------------------------- the evidence behind each per-view rate
    print("rate evidence")

    def total_at(r, c):
        return r["base"] + X["D"] * C.mult(X, c)
    for r in G["rows"]:
        sig = r["c"] / np.sqrt(r["feed"])
        moved = [total_at(r, r["c"] + s * sig) for s in (-1, 1)]
        same = all(k(t) == k(r["total"]) for t in moved)
        if r is G["pick"]:
            same = same and all(k(t - r["base"]) == k(r["lift"]) for t in moved)
        ok(same, "one sigma: %s's rate (%d feed stars from day 8)" % (r["name"], r["feed"]),
           "%.0f to %.0f around %.0f" % (min(moved), max(moved), r["total"]))
    low = total_at(G["pick"], G["pick"]["c"] - 2 * G["pick"]["c"] / np.sqrt(G["pick"]["feed"]))
    high = max(total_at(r, r["c"] + 2 * r["c"] / np.sqrt(r["feed"])) for r in G["rows"] if r is not G["pick"])
    ok(low > high, "two sigma: the pick holds with its rate low and every other rate high", "%.0f against %.0f" % (low, high))
    ok(G["pick"]["feed"] >= 300, "the decisive rate rests on 300 or more feed stars", "%d" % G["pick"]["feed"])

    # ---------------------------------------------------------------- bins and spreads
    print("bins")
    figs = [("pick total", kk_["total"]), ("pick added", kk_["lift"])] + [(r["name"], r["total"]) for r in G["rows"]]
    for name, v in figs:
        ok(edge(v) >= 150, "bin: %s" % name, "%.0f, %.0f from the edge" % (v, edge(v)))
    spreads = [{"pace_window": 10}, {"pace_window": 14}, {"fR": "issue_mean"}, {"f2": "spotlights"},
               {"rate_issues": "last6"}, {"rate_issues": "2026", "fR": "2026"}]
    for opts in spreads:
        G1 = C.golden(B, opts)
        ok(same_figures(G, G1), "spread: %s" % opts, "kilnkit %.0f adding %.0f" % (G1["pick"]["total"], G1["pick"]["lift"]))
    for ym, v in AA.items():
        pos = (v["share"] * 100) % 1
        ok(pos <= 0.2 or pos >= 0.8, "bin: click-through %d-%02d" % ym, "%.4f" % v["share"])
    for name, v in AB.items():
        if v["org"]:
            pos = (v["share"] * 100) % 1
            ok(abs(pos - 0.5) >= 0.2, "bin: share outside %s" % name, "%.4f" % v["share"])

    # ---------------------------------------------------------------- the asks
    print("asks")
    # the graded ask figures: Ask A each issue's subscribers who clicked through and their share (12); Ask B each
    # organisation's repository's people outside it when they nominated it and their share (10)
    # the stage 4 readers' routes, measured on the pack before the editor's paragraph links and the recorded addresses:
    # round 3's first reader took the spotlight's own tags with the gateways' fetches taken out (labels_only), its
    # second the spotlight's owner/name address with every fetch kept (reader_name_kept)
    profiles_a = {"careful": dict(keep_gateways=1), "gateway_subscribers_dropped": dict(drop_fetched=1),
                  "labels_only": dict(labels_only=1), "name_only": dict(name_only=1),
                  "reader_name_kept": dict(name_only=1, keep_gateways=1), "ids_only": dict(ids_only=1),
                  "cracker": dict(keep_gateways=1, sum_all=1, by_label=1, sum_per_campaign=1), "sum_all": dict(sum_all=1),
                  "first_send": dict(first_send=1, clicks_counted_only=1), "one_per_campaign": dict(one_per_campaign=1),
                  "issue_day_counted_clicks": dict(clicks_counted_only=1), "issue_day_label": dict(by_label=1),
                  "issue_day_per_campaign": dict(sum_per_campaign=1), "issue_day_per_link": dict(sum_per_link=1)}
    hits_a = {}
    for name, h in profiles_a.items():
        v = C.ask_a(B, A, h)
        hits_a[name] = sum((v[ym]["clickers"] == AA[ym]["clickers"]) + (v[ym]["share2"] == AA[ym]["share2"]) for ym in AA)
    orgs = [n for n in AB if AB[n]["org"]]
    profiles_b = {"careful": dict(survivor_only=1), "now": dict(members_now=1),
                  "snapshot_only": dict(snapshot_hashes_only=1), "snapshot_one_hop": dict(snapshot_hashes_only=1, single_hop=1),
                  "cracker": dict(no_hash_map=1, no_merge_map=1, survivor_only=1),
                  "hash_only": dict(no_merge_map=1, no_renames=1), "hash_merge_one_hop_renames": dict(single_hop=1),
                  "hash_merge": dict(no_renames=1), "hash_renames": dict(no_merge_map=1)}
    hits_b = {}
    for name, h in profiles_b.items():
        v = C.ask_b(B, A, h)
        hits_b[name] = sum((v[n].get("outside") == AB[n]["outside"]) + (v[n].get("share2") == AB[n]["share2"]) for n in orgs)
    ok(all(hits_a[n] == 0 for n in ("careful", "gateway_subscribers_dropped", "labels_only", "name_only",
                                     "reader_name_kept", "ids_only")),
       "Ask A the stage 4 readers' routes miss every figure",
       "gateways kept %d/12, gateways' subscribers dropped %d/12, the spotlight's own tags %d/12, its owner/name "
       "address %d/12 (with every fetch kept %d/12), its permanent address only %d/12" % (
           hits_a["careful"], hits_a["gateway_subscribers_dropped"], hits_a["labels_only"], hits_a["name_only"],
           hits_a["reader_name_kept"], hits_a["ids_only"]))
    ok(all(hits_b[n] == 0 for n in ("careful", "now", "snapshot_only", "snapshot_one_hop")),
       "Ask B the stage 4 readers' routes miss every figure",
       "membership of the account nominated from %d/10, membership now %d/10, addresses from the snapshot only %d/10 "
       "(with one merge hop %d/10)" % (hits_b["careful"], hits_b["now"], hits_b["snapshot_only"],
                                       hits_b["snapshot_one_hop"]))
    ok(hits_a["cracker"] == 0 and hits_b["cracker"] == 0, "cracker misses every ask figure",
       "A %d/12, B %d/10" % (hits_a["cracker"], hits_b["cracker"]))
    ok(max(hits_a.values()) < 12 and max(hits_b.values()) < 10, "no ask whole on fewer than all its devices",
       "A %s; B %s" % (hits_a, hits_b))
    one = max(max(hits_a.values()), max(hits_b.values()))
    ok(one / 22 < 0.35, "mirror leakage under 35 per cent with one device mishandled",
       "%d of 22 (a reader handling every device but summing every send's delivered keeps the clickers)" % one)
    # the measured routes: round 3's two readers, each ask on the route its reader took
    kept = max(hits_a["labels_only"], hits_a["reader_name_kept"]) + max(hits_b["snapshot_only"], hits_b["snapshot_one_hop"])
    pair = (38 + 7 + 55 * kept / 22 + 5 + 7 + 55 * kept / 22) / 2
    ok(abs(pair - 28.5) < 0.05, "pair ceiling at or under 60, as the ask sheet states", "%.1f (%d of 22 kept)" % (pair, kept))
    # the gateway fetches: one reading whatever the window or the count of links, no reader's own clicks taken for one
    base_links, base_secs = C.GATEWAY_LINKS, C.GATEWAY_SECONDS
    same = True
    for nl, ns in ((3, 2), (5, 2), (6, 2), (4, 1), (4, 5), (4, 30), (6, 60)):
        C.GATEWAY_LINKS, C.GATEWAY_SECONDS = nl, ns
        v = C.ask_a(B, A)
        same = same and all(v[ym]["clickers"] == AA[ym]["clickers"] for ym in AA)
    C.GATEWAY_LINKS, C.GATEWAY_SECONDS = base_links, base_secs
    ok(same, "Ask A a gateway's fetch read at three to six links within one second to a minute", "every issue's clickers equal")
    pw = A["pw_links"]
    issue_ids = set(A["pw_camp"].campaign_id[A["pw_camp"].list == "Sluis"])
    pw = pw[pw.campaign_id.isin(issue_ids)]
    nlab = pw.groupby("campaign_id").link_label.nunique()
    mine = pw.groupby(["campaign_id", "subscriber_id"]).agg(n=("link_label", "nunique"), most=("clicks", "max"))
    full = [k for k, x in mine.iterrows() if x.n == nlab[k[0]]]
    ok(all(mine.loc[k, "n"] <= nlab[k[0]] - 2 for k in mine.index if k not in set(full)),
       "Ask A no reader's own clicks reach every link of a Postwerk send",
       "%d fetches in the issues' sends, every reader at least two links short" % len(full))
    camps = json.load(open(os.path.join(target, K.RM_CAMP), encoding="utf-8"))["campaigns"]
    rm = A["rm_links"]
    tie = []
    for c in camps:
        if c["audience"]["list"] != "Sluis" or c["name"].startswith("[TEST]"):
            continue
        lk = rm[rm.campaign_id == c["id"]]
        tie.append((c["stats"]["unique_clicks"], lk.subscriber_id.nunique(), C.readers_clicks(lk, "relaymark").subscriber_id.nunique()))
    fetched = [x for x in tie if x[1] > x[2]]
    ok(len(fetched) == 8 and all(own < rep < raw for rep, raw, own in fetched),
       "Ask A the platform's own click count ties under neither reading on a send with fetches",
       "%d Tuesday batches: %s" % (len(fetched), "; ".join("%d between %d and %d" % (rep, own, raw) for rep, raw, own in fetched[:3])))
    n_dev = sum(1 for ym in AA)
    ok(all(AA[ym]["delivered"] < sum_all_delivered(B, A, ym) for ym in AA), "A2 every issue has a Thursday resend",
       "%d issues" % n_dev)
    with tempfile.TemporaryDirectory(dir=os.path.dirname(target)) as tmp:
        for f in os.listdir(target):
            if f not in K.ASK_FILES and f not in K.DISTRACTORS:
                shutil.copy(os.path.join(target, f), tmp)
        Bn = C.load(tmp)
        ok(same_figures(G, C.golden(Bn)) and abs(C.golden(Bn)["pick"]["total"] - G["pick"]["total"]) < 1e-6,
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
    describing = [f for f in os.listdir(target) if f.lower().endswith((".md", ".txt")) or
                  re.search(r"dictionar|manifest|readme|fields|contents", f.lower())]
    xw_cols = open(os.path.join(target, K.CROSSWALK), encoding="utf-8").readline().strip().split(",")
    ok(not describing and xw_cols == ["v5_src", "v6_surface", "v5_used_to", "v6_used_from"],
       "no shipped file describes the data: no dictionary, manifest or readme; the crosswalk maps codes only",
       "%d files" % len(os.listdir(target)))
    comp, dd = X["complete"], X["dd"]
    for how in ("mean_of_ratios", "median"):
        moved = True
        for r in G["rows"]:
            vals = [dd[q][r["a"] + 1:91].sum() / dd[q][r["a"] - 6:r["a"] + 1].mean() for q in comp
                    if dd[q][r["a"] - 6:r["a"] + 1].mean() > 0]
            g = float(np.mean(vals)) if how == "mean_of_ratios" else float(np.median(vals))
            moved = moved and k(r["S"] + r["pace"] * g + r["lift"]) == k(r["total"])
        ok(moved, "H14 runners-up ratio pooled or as the %s" % how.replace("_", " "), "every figure in its bin")

    # ---------------------------------------------------------------- the nominations' readings
    noms = A["noms"]
    refs = [C.norm_ref(x) for x in noms.repository]
    ok(all("/" in x for x in refs), "Ask B every reference names an owner", "%d references" % len(refs))
    accs = B["accounts"]
    snap = dict(zip(accs.primary_email_sha256.dropna(), accs.account_id[accs.primary_email_sha256.notna()]))
    by_hash = C.address_map(B, A)
    short_full = {B["repos"][rid]["full_name"].lower() for rid in octrow["shortlist"]}
    ren = {o.lower(): n.lower() for o, n in zip(A["renames"].old_full_name, A["renames"].new_full_name)}
    on_short = [i for i, x in enumerate(refs) if ren.get(x, x) in short_full]
    signed_out = [i for i in on_short if noms.account_id[i] is None]
    ok(all(noms.email_sha256[i] in by_hash for i in signed_out), "Ask B every signed-out nominator resolves to an account",
       "%d signed-out nominations of the shortlist" % len(signed_out))
    signed_in = [i for i in range(len(noms)) if noms.account_id[i] is not None]
    ok(all(noms.email_sha256[i] and snap.get(noms.email_sha256[i], noms.account_id[i]) == noms.account_id[i]
           for i in signed_in) and
       len({noms.email_sha256[i] for i in signed_in}) == len({(noms.email_sha256[i], noms.account_id[i]) for i in signed_in}),
       "Ask B one account to an address: every signed-in response records an address, no address names two accounts",
       "%d signed-in responses" % len(signed_in))
    stale = [i for i in signed_out if noms.email_sha256[i] not in snap]
    if W is not None:
        moved = {(v["repo"], v["work"]) for v in W.moved}
        stale_set = {([B["repos"][q]["name"] for q in octrow["shortlist"]
                       if B["repos"][q]["full_name"].lower() == ren.get(refs[i], refs[i])][0], noms.email_sha256[i])
                     for i in stale}
        ok(stale_set == moved and len(moved) == len(orgs) and len({n for n, w in moved}) == len(orgs) and
           all(snap.get(w) is None and by_hash.get(w) == v["member"] for v in W.moved for w in [v["work"]]),
           "Ask B one member of each organisation's repository nominated it signed in and again signed out with the "
           "work address, and the account's address changed when they left",
           ", ".join("%s (left %s)" % (v["repo"], v["left"].strftime("%d %b")) for v in W.moved))
    C.prepare(B)
    merged_to = dict(zip(accs.account_id[accs.merged_into.notna()], accs.merged_into.dropna().astype(int)))
    same_now, left, gone = True, [], set()
    group = {}
    for a in merged_to:
        b = a
        while b in merged_to:
            b = merged_to[b]
        group.setdefault(b, set()).add(a)
    for i in on_short:
        rid = [q for q in octrow["shortlist"] if B["repos"][q]["full_name"].lower() == ren.get(refs[i], refs[i])][0]
        org = C.owner_of(B, rid)
        if not org:
            continue
        aid = noms.account_id[i] if noms.account_id[i] is not None else int(by_hash[noms.email_sha256[i]])
        while aid in merged_to:
            aid = merged_to[aid]
        t = K.utc_of(noms.submitted_at[i])
        accts = {aid} | group.get(aid, set())
        then = any(C.is_member(B, org, a, t) for a in accts)
        now = any(C.is_member(B, org, a, t, current=True) for a in accts)
        own = C.is_member(B, org, aid, t)
        if then and not own:
            left.append((B["repos"][rid]["name"], aid))
        elif then and not now:
            gone.add((B["repos"][rid]["name"], aid))
        elif then != now:
            same_now = False
    ok(same_now and (W is None or gone == {(v["repo"], v["member"]) for v in W.moved}),
       "Ask B membership when nominating equals membership now, but for the members who left",
       "%d nominations of the shortlist; %d left with their own account" % (len(on_short), len(gone)))
    if W is not None:
        via = {(v["repo"], v["personal"]) for v in W.via}
        ok(set(left) == via and len(via) == len(orgs) and len({n for n, a in via}) == len(orgs),
           "Ask B one person for each organisation's repository was a member only through an account merged away later",
           ", ".join("%s (merged %s)" % (v["repo"], v["merged"].strftime("%d %b")) for v in W.via))
    mem = B["members"]
    owner_rows = set(zip(mem.organization[mem.role == "owner"], mem.account_id[mem.role == "owner"]))
    owners_nom = 0
    person = {}
    for i in on_short:
        rid = [q for q in octrow["shortlist"] if B["repos"][q]["full_name"].lower() == ren.get(refs[i], refs[i])][0]
        aid = noms.account_id[i] if noms.account_id[i] is not None else int(by_hash[noms.email_sha256[i]])
        while aid in merged_to:
            aid = merged_to[aid]
        person.setdefault(rid, []).append(aid)
        org = C.owner_of(B, rid)
        t = K.utc_of(noms.submitted_at[i])
        if org and (org, aid) in owner_rows:
            owners_nom += 1
            ok(C.is_member(B, org, aid, t), "Ask B an owner of the organisation counts as a member",
               "%s nominated by an owner of %s" % (B["repos"][rid]["name"], org))
    ok(True, "Ask B owner-role nominators counted inside", "%d nominations by owners" % owners_nom)
    late = [i for i in on_short if dt.datetime.fromisoformat(noms.submitted_at[i]).replace(tzinfo=None) >
            dt.datetime(2026, 9, 20, 23, 59, 59)]
    ok(not late, "Ask B no nomination of the shortlist after the 20 September close", "%d late" % len(late))
    twice = all(len(v) > len(set(v)) for v in person.values())
    ok(twice and all(len(set(person[q])) == AB[B["repos"][q]["name"]]["people"] for q in person),
       "Ask B a person nominating twice counts once", ", ".join("%s %d rows %d people" % (B["repos"][q]["name"], len(v), len(set(v)))
                                                             for q, v in person.items()))

    # ---------------------------------------------------------------- the pace window, back-tested on the runners-up
    def loo(w, ages=range(21, 36)):
        num = {a: sum(dd[q][a + 1:91].sum() for q in comp) for a in ages}
        den = {a: sum(dd[q][a - w + 1:a + 1].sum() / w for q in comp) for a in ages}
        errs = []
        for q in comp:
            d = dd[q]
            S90 = d[1:91].sum()
            for a in ages:
                p = d[a - w + 1:a + 1].mean()
                errs.append(abs(d[1:a + 1].sum() + p * (num[a] - d[a + 1:91].sum()) / (den[a] - p) - S90) / S90)
        return 100 * float(np.mean(errs))
    m3, m7, m14 = loo(3), loo(7), loo(14)
    g3 = C.golden(B, {"pace_window": 3})
    ok(m3 > m7 and m3 > m14 and same_figures(G, C.golden(B, {"pace_window": 14})),
       "pace window: 3 days back-tests worst, 14 days gives the golden's figures",
       "leave-one-out error 3 days %.2f, 7 days %.2f, 14 days %.2f per cent; 3 days puts shiftgres at %.0f" % (
           m3, m7, m14, [r for r in g3["rows"] if r["name"] == "shiftgres"][0]["total"]))

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
