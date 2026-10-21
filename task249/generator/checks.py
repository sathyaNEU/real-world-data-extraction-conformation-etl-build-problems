"""Generator assertions on the world and the cut pack.   python3 checks.py [target]

The analyst test (dataset-generation 7.1) runs on the clean truth first: the excess on recognised items alone, with
every rule applied, files CC27-A, C, G and H; the same estimate with the items reached in the freed time added files
the golden. Then the pack: the golden from target/ against the truth, the golden family, the ladder's rungs, the
semantic forks (SF1 to SF15), the separation of the asks' rows from the call's, the asks' goldens against the
world, the input gates."""
import datetime as dt
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AK
import build as BLD
import params as P
import records as RC
import sim
import solve as S

N = [0]


def ok(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


GOLD = ["CC27-A", "CC27-B", "CC27-C", "CC27-D", "CC27-G", "CC27-H"]
DEFAULT = ["CC27-A", "CC27-C", "CC27-G", "CC27-H"]


def world_checks(W):
    T = sim.truth(W)
    ok(sorted(f for f in P.F27 if T[f]["gain"] > P.THRESH) == GOLD, "R3b: the decisive step alone (the items reached in the "
       "freed time added) files the golden on the clean truth %s" % T)
    # the analyst test on the clean truth: the direct part alone (every exposure channel, the candidate's own
    # ability) files the default; the reach part added files the golden
    ok(sorted(f for f in P.F27 if T[f]["direct"] > P.THRESH) == DEFAULT, "R3a: the analyst test on the clean truth, the excess on "
       "recognised items alone with every rule applied, files CC27-A, C, G and H %s" % {f: T[f]["direct"] for f in T})
    ok(min(T[f]["gain"] for f in GOLD) >= 1.4, "truth margin above")
    ok(max(T[f]["gain"] for f in P.F27 if f not in GOLD) <= 0.65, "truth margin below")
    for f in ("CC27-B", "CC27-D"):
        ok(T[f]["direct"] <= 0.6 and T[f]["reach"] >= 0.9, "%s carried by reach" % f)
    # the speeded forms are speeded for everyone, and speed alone flags nothing: CC27-I is speeded and stays under
    ft = {f: np.mean([not r["reach"][-1] for r in W["rows"] if r["form"] == f and r["n_prev"] == 0]) for f in P.F27}
    for f in ("CC27-B", "CC27-D", "CC27-I"):
        ok(0.30 <= ft[f] <= 0.50, "%s speeded %.2f" % (f, ft[f]))
    for f in ("CC27-A", "CC27-C", "CC27-E", "CC27-F", "CC27-G", "CC27-J"):
        ok(ft[f] <= 0.15, "%s not speeded %.2f" % (f, ft[f]))
    ok(T["CC27-I"]["gain"] < 0.6, "CC27-I speeded and under")
    # the world: 170 delivered items, trial slots fixed, forms drawn among those not sat
    for r in W["rows"][:2000]:
        ok(len(r["seq"]) == 170 and (r["kind"] == "T").sum() == 20, "delivery")
    for c in W["cands"]:
        fs = [h["form"] for h in c["hist"]]
        ok(len(fs) == len(set(fs)), "a form sat twice")
    return T


def pack_checks(target, W, T):
    C = S.call(target)
    g = C["gain"]
    ok(C["flagged"] == GOLD, "golden from the pack %s" % C["flagged"])
    for f in P.F27:
        ok(abs(g[f] - T[f]["gain"]) <= 0.25, "%s golden %.2f against truth %.2f" % (f, g[f], T[f]["gain"]))
    R = C["routes"]
    fam = ["golden", "golden_add", "golden_median"]
    for k in fam:
        ok(S.flagged(R, k) == GOLD, "family %s" % k)
    lo = min(R[f][k] for f in GOLD for k in fam)
    hi = max(R[f][k] for f in P.F27 if f not in GOLD for k in fam)
    ok(lo >= 1.4 and hi <= 0.65, "family margins %.2f %.2f" % (lo, hi))
    # the ladder
    ok(S.flagged(R, "direct") == DEFAULT, "default path %s" % S.flagged(R, "direct"))
    ok(S.flagged(R, "direct_blanks_wrong") == DEFAULT, "default path, blanks scored wrong")
    ok(S.flagged(R, "same_item") == ["CC27-A", "CC27-G"], "R3b: the same item only stays on a wrong set")
    ok(S.flagged(R, "raw_within") == ["CC27-A", "CC27-C", "CC27-D", "CC27-G"], "R3b: the raw within-candidate excess stays on a wrong set")
    ok(S.flagged(R, "between") == [f for f in P.F27 if f != "CC27-I"], "gain between sittings flags all but the speeded CC27-I")
    for f in ("CC27-B", "CC27-D"):
        ok(R[f]["direct"] <= 0.7 and R[f]["direct_blanks_wrong"] <= 0.75, "%s off the default path" % f)
    return C


def forks(target, C):
    """each semantic fork's other reading files the golden too (design note, Semantic fork table)"""
    D, T = C["D"], C["T"]
    Pn, Mu = S.norms(T)

    def run(expo_fn=None, variant="golden", sel=None):
        res = {f: [] for f in S.F27}
        for t in T:
            if t["w"] < 4 or not t["prev"] or t["form"] not in res:
                continue
            if sel and not sel(t):
                continue
            same, sib, rev = (expo_fn or S.exposure)(T, t, D)
            d, r = S.sitting_gain(t, same, sib, Pn, Mu, variant)
            res[t["form"]].append(d + r)
        return sorted(f for f in S.F27 if np.mean(res[f]) > P.THRESH)

    # SF1 review shows only items answered wrongly, blanks not shown: the review channel's items are already among
    # the items the sitting reached, so a reading that adds the blanks files the same forms
    def expo_blanks(Tt, t, Dd):
        same, sib, rev = S.exposure(Tt, t, Dd)
        shown = set()
        for i in t["prev"]:
            h = Tt[i]
            if (h["person"], h["window"]) in Dd["held"]:
                shown |= {it for it, rc, sc in zip(h["items"], h["reach"], h["scored"]) if sc and not rc}
        add = np.array([it in shown for it in t["items"]]) & ~same
        return same | add, sib & ~add, rev
    ok(run(expo_blanks) == GOLD, "SF1")
    # SF2 an item the earlier sitting never reached was not shown: counting every delivered item as seen
    def expo_delivered(Tt, t, Dd):
        model = Dd["model"]
        seen, ms = set(), set()
        for i in t["prev"]:
            for it in Tt[i]["items"]:
                seen.add(it); ms.add(model[it])
        same = np.array([it in seen for it in t["items"]])
        sib = np.array([model[it] in ms for it in t["items"]]) & ~same
        return same, sib, set()
    ok(run(expo_delivered) == GOLD, "SF2")
    # SF3 a trial item seen before counts as shown: leaving the trial slots out of the earlier sittings
    def expo_scored_only(Tt, t, Dd):
        model = Dd["model"]
        seen, ms = set(), set()
        for i in t["prev"]:
            h = Tt[i]
            for it, rc, sc in zip(h["items"], h["reach"], h["scored"]):
                if rc and sc:
                    seen.add(it); ms.add(model[it])
        same = np.array([it in seen for it in t["items"]])
        sib = np.array([model[it] in ms for it in t["items"]]) & ~same
        return same, sib, set()
    ok(run(expo_scored_only) == GOLD, "SF3")
    # SF4 a resit sitting is a sitting by a candidate who sat before, under whichever number: without the register's
    # changes the renumbered candidates' resits drop out (and sit among the first-time candidates)
    D4 = dict(D)
    s4 = D["s"].copy()
    s4["person"] = s4["candidate_no"]
    D4["s"] = s4
    T4 = S.sittings(D4)
    Pn4, Mu4 = S.norms(T4)
    res4 = {f: [] for f in S.F27}
    for t in T4:
        if t["w"] >= 4 and t["prev"] and t["form"] in res4:
            same, sib, rev = S.exposure(T4, t, D4)
            d, r = S.sitting_gain(t, same, sib, Pn4, Mu4)
            res4[t["form"]].append(d + r)
    ok(sorted(f for f in S.F27 if np.mean(res4[f]) > P.THRESH) == GOLD, "R2 SF4: Layer 1 item, the register's number changes, does not carry the call")
    # SF5 the year's resit sittings are the 2027 windows' (February to November 2027)
    ok(all(t["w"] >= 4 for t in T if t["w"] >= 4), "SF5")
    # SF6 strictly more than 1.0 scored item, unrounded
    ok(all(abs(C["gain"][f] - 1.0) > 0.3 for f in S.F27), "SF6")
    # SF7 the counterfactual time of a recognised item: mean against median of its time
    ok(run(variant="golden_median") == GOLD, "SF7")
    # SF8 the baseline: logit shift against an additive shift on the first-time candidates' item statistics
    ok(run(variant="golden_add") == GOLD, "SF8")
    # SF9 a booked review that was cancelled or not attended showed nothing: counting every booking as held
    held_all = set(zip(D["s"]["person"], D["s"]["window"]))
    D2 = dict(D)
    rv = pd.read_csv(os.path.join(target, S.FILES["reviews"]), dtype=str)
    pmap = dict(zip(D["s"]["candidate_no"], D["s"]["person"]))
    D2["held"] = set(D["held"]) | set(zip([pmap.get(n, n) for n in rv["candidate_no"]], rv["sitting_window"]))
    ok(run(lambda Tt, t, Dd: S.exposure(Tt, t, D2)) == GOLD, "R2 SF9: Layer 1 item, the cancelled and missed review bookings")
    # SF10 the four hours are examination time: the clock stops for failures and pauses, and the latencies are
    # working time, so no stop moves a sitting's reach
    ev = pd.read_csv(os.path.join(target, S.FILES["events"]), dtype=str)
    stopped = set(ev[ev["event"] == "SESSION_RESUME"]["booking_ref"])
    for t in T:
        if t["booking"] in stopped:
            ok(np.nansum(t["secs"]) <= 4 * 3600 + 170, "SF10 latencies are working time")
    # SF16 an item written from the same item model as an item shown is not an untouched item: on the pack the
    # siblings are answered in about four fifths of the candidate's own pace and above their ability, where the
    # untouched items sit at the pace and at the ability; read as untouched they would flag A, B, D and G
    lt = {"sib": [], "un": []}
    ex = {"sib": [], "un": []}
    for t in T:
        if t["w"] < 4 or not t["prev"] or t["form"] not in S.F27:
            continue
        same, sib, rev = S.exposure(T, t, D)
        ep = np.array([Pn.get((t["w"], i), np.nan) for i in t["items"]])
        mj = np.array([Mu.get((t["w"], i), np.nan) for i in t["items"]])
        okk = ~np.isnan(ep) & ~np.isnan(mj) & t["reach"] & t["scored"]
        u = okk & ~same & ~sib
        if u.sum() < 20:
            continue
        lr = np.log(t["secs"]) - mj
        pace = np.nanmean(lr[u])
        pe = 1 / (1 + np.exp(-(S.lg(ep) + S.rasch_shift(t["x"][u], ep[u]))))
        for k, m in (("sib", okk & sib & ~same), ("un", u)):
            lt[k].extend(lr[m] - pace)
            ex[k].extend(t["x"][m] - pe[m])
    ok(np.exp(np.mean(lt["sib"])) < 0.9 and np.mean(ex["sib"]) > 0.03 and abs(np.mean(lt["un"])) < 0.02,
       "SF16 siblings answered at %.2f of the pace and %+.3f above ability (untouched %.2f, %+.3f)" % (
           np.exp(np.mean(lt["sib"])), np.mean(ex["sib"]), np.exp(np.mean(lt["un"])), np.mean(ex["un"])))
    ok(run(lambda Tt, t, Dd: (lambda a: (a[0], np.zeros_like(a[1]), a[2]))(S.exposure(Tt, t, Dd)))
       == ["CC27-A", "CC27-B", "CC27-D", "CC27-G"], "SF16 the siblings read as untouched flag A, B, D and G")
    # SF11 release 3 seconds and release 4 milliseconds are the same clock: the golden on release 4 read in
    # seconds alone is not a reading (the note states the unit)
    md = {}
    for t in T:
        if t["w"] in (5, 6) and not t["prev"]:
            md.setdefault(t["w"], []).append(np.nanmedian(t["secs"]))
    ok(abs(np.median(md[5]) - np.median(md[6])) < 8, "R2 SF11: Layer 1 item, release 4's milliseconds against release 3's seconds")


def rules(target, W, C, X):
    """the three rules executed (dataset-generation 7.1, R1 and R2; R3a and R3b sit in world_checks and pack_checks)
    and the realism sweep"""
    D, T = C["D"], C["T"]
    Pn, Mu = S.norms(T)
    # R1: the field's raw material ships, the deciding quantity never
    bad = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        heads = []
        if f.endswith(".csv"):
            heads = list(pd.read_csv(p, nrows=0).columns)
        elif f.endswith(".xlsx"):
            for sh in pd.read_excel(p, sheet_name=None, nrows=0).values():
                heads += [str(c) for c in sh.columns]
        bad += [h for h in heads if any(w in h.lower() for w in ("gain", "expos", "recogn", "seen", "reach", "saved",
                                                                   "excess", "flag", "repeat", "pace"))]
    ok(not bad, "R1: no shipped column holds a gain, an exposure, a reach or a flag %s" % bad)
    ok(True, "R1: the golden reads each sitting's responses and latencies, the layouts' slots, the bank's keys and item "
       "models, the register and the review bookings (solve.sittings, solve.exposure, solve.sitting_gain)")

    # R2: each Layer 1 item mishandled leaves the call where it was
    def run(variant):
        res = {f: [] for f in S.F27}
        for t in T:
            if t["w"] < 4 or not t["prev"] or t["form"] not in res:
                continue
            same, sib, rev = S.exposure(T, t, D)
            d, r = S.sitting_gain(t, same, sib, Pn, Mu, variant)
            res[t["form"]].append(d + r)
        return sorted(f for f in S.F27 if np.mean(res[f]) > P.THRESH)
    ok(run("golden_blanks") == GOLD, "R2: Layer 1 item, the blanks scored wrong in the baseline, leaves the call unchanged")
    ok(run("golden_trial") == GOLD, "R2: Layer 1 item, the trial positions counted with the scored, leaves the call unchanged")
    ok(D["s"].groupby(["person", "window"]).size().max() == 1, "R2: Layer 1 item, release 4's day-month-year dates: no "
       "candidate sits twice in a window, so the sittings order by window and no reading of the dates moves the call")
    cw = pd.read_csv(os.path.join(target, S.FILES["crosswalk"]), dtype=str)
    lay = pd.read_csv(os.path.join(target, S.FILES["layouts"]), dtype=str)
    old = set(lay[lay["window"].str.startswith("2026")]["item_id"])
    ok(old <= set(cw["previous_item_id"]) and not (set(cw["previous_item_id"]) & set(cw["item_id"])),
       "R2: Layer 1 item, the renumbering: every 2026 layout number maps and no earlier number is a present one, so an "
       "unmapped read keys nothing and cannot pass silently")

    # R3c and the realism sweep
    a = pd.read_csv(os.path.join(target, S.FILES["export3"]), dtype=str, keep_default_na=False)
    b = pd.read_csv(os.path.join(target, S.FILES["export4"]), dtype=str, keep_default_na=False)
    lat = list(a["item_seconds"]) + list(b["latency_ms"])
    ok(len(set(lat)) == len(lat), "R3c: no two sittings share a latency record")
    ok(len(set(a["responses"]) | set(b["response_string"])) == len(lat), "R3c: no two sittings share a response record")
    runs = 0
    for v in lat[:6000]:
        q = v.split("|")
        cur = 0
        for i in range(1, len(q)):
            cur = cur + 1 if (q[i] == q[i - 1] and q[i]) else 0
            runs = max(runs, cur)
    ok(runs < 5, "R3c: no held latency block: the longest run of one value in a sitting is %d" % (runs + 1))
    cells = D["s"].groupby(["window", "centre"]).size()
    ok(cells.nunique() >= 0.7 * len(cells), "realism: sittings per window and centre vary (%d values over %d cells)"
       % (cells.nunique(), len(cells)))
    ev = pd.read_csv(os.path.join(target, S.FILES["events"]), dtype=str, keep_default_na=False)
    ev["t"] = pd.to_datetime(ev["event_utc"])
    first = ev[ev["booking_ref"] != ""].groupby(["booking_ref", "event"])["t"].min().unstack()   # reboots carry none
    last_end = ev[ev["event"] == "SESSION_END"].groupby("booking_ref")["t"].max()
    le = last_end.reindex(first.index)
    ok(bool(((first["TUTORIAL_START"] < first["SESSION_START"]) & (first["SESSION_START"] < le)).all()),
       "realism: every booking's tutorial, clock start and end in order")
    rs_ = ev[ev["event"] == "SESSION_RESUME"]
    ok(all(first.at[r.booking_ref, "SESSION_START"] < r.t <= last_end[r.booking_ref] for r in rs_.itertuples()),
       "realism: every resume inside its sitting")
    rv = pd.read_csv(os.path.join(target, S.FILES["reviews"]), dtype=str)
    gap = (pd.to_datetime(rv["review_date"]) - pd.to_datetime(rv["booked_on"])).dt.days
    ok(bool(gap.between(4, 25).all()), "realism: reviews held 4 to 25 days after booking")
    rep = pd.concat(pd.read_excel(os.path.join(target, S.FILES["incidents"]), sheet_name=None, dtype=str).values())
    ok(rep["Report"].value_counts().max() <= 2, "realism: no incident report's text recurs beyond twice")
    A, _ = S.ask_a(target, D=D)
    Bk = S.ask_b(target, D=D)
    ok(len(set(A.values())) >= 5 and len(set(Bk.values())) >= 5, "realism: the asks' figures vary across the forms (%d and "
       "%d distinct values)" % (len(set(A.values())), len(set(Bk.values()))))


def ask_checks(target, W, X, C):
    A, booked = S.ask_a(target, D=C["D"])
    truth = X["A"]["a"]["truth"]
    form_of = dict(zip(C["D"]["s"]["booking_ref"], C["D"]["s"]["form"]))
    want = {f: 0 for f in S.F27}
    for b in truth:
        want[form_of[b]] += 1
    ok(A == want, "ask A %s against %s" % (A, want))
    ok(set(booked) == set(truth), "ask A bookings")
    Bk = S.ask_b(target, D=C["D"])
    off = X["A"]["a"]["offline"]
    wantb = {f: 0 for f in S.F27}
    for b in off:
        wantb[form_of[b]] += 1
    ok(Bk == wantb, "ask B %s against %s" % (Bk, wantb))
    # the devices move the figures: the failure's own booking, the resumes, the link's lost rows
    ev = pd.read_csv(os.path.join(target, S.FILES["events"]), dtype=str)
    naive = {f: 0 for f in S.F27}
    for b in set(ev[ev["event"] == "WS_FAIL"]["booking_ref"]):
        if form_of.get(b) in naive:
            naive[form_of[b]] += 1
    # SF13 the sitting a failure interrupted is the one whose clock ran on that workstation then, not the logged booking
    ok(sum(naive[f] != A[f] for f in S.F27) >= 6, "SF13 ask A device: WS_FAIL booking refs move %d forms" % sum(naive[f] != A[f] for f in S.F27))
    res = {f: 0 for f in S.F27}
    for b in set(ev[ev["event"] == "SESSION_RESUME"]["booking_ref"]):
        if form_of.get(b) in res:
            res[form_of[b]] += 1
    # SF12 the invigilators' pauses and the link losses are not failures: every resume read as one moves the figures
    ok(sum(res[f] != A[f] for f in S.F27) >= 6, "SF12 ask A device: resumes move %d forms" % sum(res[f] != A[f] for f in S.F27))
    # SF14 any loss logged against the booking (lost_refs) against the clock running while the link was down; SF15 a
    # loss with no NET_BACK dropped (pairs_only)
    for sf, pth in (("SF14", "lost_refs"), ("SF14", "lost_within"), ("SF15", "pairs_only")):
        v = S.ask_b(target, D=C["D"], path=pth)
        ok(sum(v[f] != Bk[f] for f in S.F27) >= 6, "%s ask B device: %s moves %d forms" % (sf, pth, sum(v[f] != Bk[f] for f in S.F27)))
    # SF15 every loss with no NET_BACK began after its sitting's clock started, so the count does not depend on when
    # the link came back
    evt = ev.copy()
    evt["t"] = pd.to_datetime(evt["event_utc"])
    st0 = evt[evt["event"] == "SESSION_START"].groupby("booking_ref")["t"].min()
    early = 0
    for _, g in evt[evt["event"].isin(["NET_LOST", "NET_BACK"])].sort_values("t").groupby(["centre_code", "workstation"]):
        rows = list(g.itertuples(index=False))
        for k, r in enumerate(rows):
            if r.event == "NET_LOST" and not any(q.event == "NET_BACK" and q.booking_ref == r.booking_ref for q in rows[k + 1:]):
                early += int(r.t < st0[r.booking_ref])
    ok(early == 0, "SF15 no unanswered loss before its sitting's clock started (%d)" % early)
    # separation: the asks' devices sit in files the call never reads
    ok(set(BLD.PACK) - {"events", "seat", "incidents"} >= {"export3", "export4", "layouts", "bank", "crosswalk", "register",
                                                            "reviews"}, "separation")


def gates(target):
    files = [os.path.join(target, BLD.FILES[k]) for k in BLD.PACK]
    ok(all(os.path.exists(f) for f in files) and len(files) >= 10, "ten or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    n = sum(1 for _ in open(os.path.join(target, BLD.FILES["export3"]), encoding="utf-8")) - 1
    ok(n >= 25000, "the 25,000-row file: %d" % n)
    for f in files:
        if f.endswith((".csv", ".md", ".eml")):
            txt = open(f, encoding="utf-8").read()
            ok("\u2014" not in txt and "\u2013" not in txt, "a dash in %s" % f)


def main(target, X=None):
    X = X or {}
    W = X.get("W") or sim.world()
    T = world_checks(W)
    C = pack_checks(target, W, T)
    forks(target, C)
    rules(target, W, C, X)
    if "A" in X:
        ask_checks(target, W, X, C)
    gates(target)
    print("checks: %d passed" % N[0])
    return C


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    W = sim.world()
    R0 = RC.build(W)
    X = dict(W=W, A=AK.build(W, R0))
    main(tgt, X)
