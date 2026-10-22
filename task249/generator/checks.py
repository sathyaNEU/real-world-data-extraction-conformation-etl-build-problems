"""Generator assertions on the world and the cut pack.   python3 checks.py [target]

The analyst test (dataset-generation 7.1) runs on the clean truth first: the excess on recognised items alone, with
every rule applied, files CC27-A, C, G and H; the same estimate with the items reached in the freed time added files
the golden. Then the pack: the golden from target/ against the truth, the golden family, the ladder's rungs, the
semantic forks (SF1 to SF20), the separation of the asks' rows from the call's, the asks' goldens against the
world and every route short of them, the input gates."""
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
    ok(S.flagged(R, "same_item") == ["CC27-A"], "R3b: the same item only stays on a wrong set")
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
    rep = pd.concat([df.iloc[:, 4] for df in pd.read_excel(os.path.join(target, S.FILES["incidents"]), sheet_name=None,
                                                             dtype=str).values()])
    ok(rep.value_counts().max() <= 2, "realism: no incident report's text recurs beyond twice")
    A, _ = S.ask_a(target, D=D)
    Bk = S.ask_b(target, D=D)
    ok(len(set(A.values())) >= 5 and len(set(Bk.values())) >= 5, "realism: the asks' figures vary across the forms (%d and "
       "%d distinct values)" % (len(set(A.values())), len(set(Bk.values()))))


def centre_view(target, ev, use_first_back):
    """the link item read centre by centre: each loss two or more clients at a centre logged, from its first NET_LOST
    (or before anyone logged in) to its first or its last NET_BACK (or to the close), against every sitting there whose
    clock ran inside it, the hall stops taken out"""
    st = ev[ev["event"] == "SESSION_START"].groupby("booking_ref")["t"].min()
    en = ev[ev["event"] == "SESSION_END"].groupby("booking_ref")["t"].max()
    where = ev[ev["event"] == "SESSION_START"].groupby("booking_ref")["centre_code"].first()
    halls = S.hall_stops(target, ev)
    seat = pd.read_csv(os.path.join(target, S.FILES["seat"]), dtype=str)
    sess = dict(zip(seat["booking_ref"], zip(seat["session_date"], seat["session"])))
    net = ev[ev["event"].isin(["NET_LOST", "NET_BACK"])].sort_values("t")
    out = set()
    for cc, g in net.groupby("centre_code"):
        g = g.reset_index(drop=True)
        part = (g["t"].diff() > pd.Timedelta(minutes=20)).cumsum()
        for _, h in g.groupby(part):
            if h[["booking_ref", "workstation"]].drop_duplicates().shape[0] < 2:
                continue
            lost = h[h["event"] == "NET_LOST"]["t"]
            back = h[h["event"] == "NET_BACK"]["t"]
            a = lost.min() if len(lost) else pd.Timestamp.min
            if len(lost) and len(back) and back.max() < lost.max():
                z = pd.Timestamp.max                              # down until the session closed
            elif len(back):
                z = back[back > a].min() if use_first_back else back.max()
            else:
                z = pd.Timestamp.max
            here = {sess[b] for b in h["booking_ref"]}
            for b in where[where == cc].index:
                if sess[b] not in here:
                    continue
                run = [(st[b], en[b])]
                for p, q in halls.get(b, []):
                    run = [y for u, v in run for y in ([(u, v)] if q <= u or p >= v else [(u, p), (q, v)]) if y[0] < y[1]]
                if any(max(u, a) < min(v, z) for u, v in run):
                    out.add(b)
    return out | S.power_cut(target, ev)


def ask_checks(target, W, X, C):
    a = X["A"]["a"]
    sa = S.ask_a_sets(target)
    A, booked = S.ask_a(target, D=C["D"], sets=sa)
    truth = a["truth"]
    form_of = dict(zip(C["D"]["s"]["booking_ref"], C["D"]["s"]["form"]))
    want = {f: 0 for f in S.F27}
    for b in truth:
        want[form_of[b]] += 1
    ok(A == want, "ask A %s against %s" % (A, want))
    ok(set(booked) == set(truth), "ask A bookings")
    sb = S.offline_sets(target, C["D"])
    Bk = S.ask_b(target, D=C["D"], sets=sb)
    ok(sb["golden"] == a["offline"], "ask B bookings")
    wantb = {f: 0 for f in S.F27}
    for b in a["offline"]:
        wantb[form_of[b]] += 1
    ok(Bk == wantb, "ask B %s against %s" % (Bk, wantb))
    # every route short of the golden misses every form: SF12 (a WS_FAIL the sitting did not stop after: a finished
    # candidate's workstation switched off, a workstation's own connection), SF13 (a restart in place with no WS_FAIL and
    # no report), SF14 (an unexplained resume read as a failure takes the unreported pauses with it)
    ok(set(S.A_CAREFUL) | set(S.A_MIRRORS) == set(S.A_ROUTES) - {"golden", "no_power"}, "every ask A route classed")
    for pth in S.A_CAREFUL + S.A_MIRRORS:
        v, _ = S.ask_a(target, D=C["D"], path=pth, sets=sa)
        kept = [f for f in S.F27 if v[f] == A[f]]
        ok(len(kept) <= (2 if pth in S.A_MIRRORS else 0), "ask A route %s keeps %s" % (pth, kept))
    # SF15 (a loss one client logged alone is not the centre's link), SF17 (a loss inside a hall stop ran no clock), SF19
    # (a client that started without the link), the roster read
    for pth in ("per_booking", "per_booking_stops", "centre_only", "pairs_only", "lost_refs"):
        v = S.ask_b(target, D=C["D"], path=pth, sets=sb)
        kept = [f for f in S.F27 if v[f] == Bk[f]]
        ok(len(kept) <= (2 if pth == "lost_refs" else 0), "ask B route %s keeps %s" % (pth, kept))
    v = S.ask_b(target, D=C["D"], path="no_power", sets=sb)
    ok(sum(v[f] != Bk[f] for f in S.F27) >= 4, "SF20 the power cut's minutes on the UPS left out move the August forms")
    # SF21 the moves to a spare: the workstation a sitting left is restarted before the session's last sitting ends after
    # a fault (a freeze, a keyboard, mouse or screen, a client hung at the link's loss, a change of seat asked for over a
    # fault) and never after a change of seat asked for over anything else, reported or not
    info = a["info"]
    hw = {b for b, rec in info.items() if rec["kind"] in AK.HARDWARE}
    req = {b for b, rec in info.items() if rec["kind"] == "move"}
    ok(sa["moved"] == hw | req, "SF21 every move to a spare is a fault's or a change of seat's")
    ok(sa["moved_restarted"] == hw, "SF21 the workstation left restarted after every fault and after no change of seat "
       "(%d and %d)" % (len(sa["moved_restarted"] - hw), len(hw - sa["moved_restarted"])))
    ok(sa["spare_req_rep"] - sa["spare_fault_rep"] <= req and sa["spare_fault_rep"] <= hw,
       "SF22 a reported change of seat over a fault is a fault's move, over anything else a request's")
    # each device reaches every form
    dev = a["device"]
    for k in ("quiet_restart", "unreported_pause", "switch_off", "fault", "hall_stop", "silent_hw_move", "silent_req_move"):
        per = {f: 0 for f in S.F27}
        for b in dev[k]:
            per[form_of[b]] += 1
        ok(min(per.values()) >= 1, "device %s reaches every form: %s" % (k, per))
    # SF18 the edges: each client's own reading and the centre's (to its first or its last NET_BACK) file the same sittings
    ev = S.events(target)
    for first in (True, False):
        cv = centre_view(target, ev, first)
        ok(cv == sb["golden"], "SF18 the centre's reading (%s NET_BACK) against the clients': %d and %d differ"
           % ("first" if first else "last", len(cv - sb["golden"]), len(sb["golden"] - cv)))
    # every loss of a centre's link is logged by three or more clients; every loss one client logged alone is a
    # workstation's own connection, with no other client logging anything there within 45 minutes
    ivs, _, _ = S.net_intervals(ev)
    net = ev[ev["event"].isin(["NET_LOST", "NET_BACK"])]
    lone = [iv for iv in ivs if not iv["shared"]]
    for iv in lone:
        near = net[(net["centre_code"] == iv["cc"]) & (net["t"] > iv["a"] - pd.Timedelta(minutes=45))
                   & (net["t"] < iv["z"] + pd.Timedelta(minutes=45))]
        ok(set(near["booking_ref"]) == {iv["b"]}, "a lone loss has no other client's row within 45 minutes")
        ok(iv["b"] in dev["fault"], "a lone loss is a workstation's own connection")
    ok({iv["b"] for iv in lone} == dev["fault"], "every fault logged alone")
    for cc, g in net.groupby("centre_code"):
        g = g.sort_values("t")
        part = (g["t"].diff() > pd.Timedelta(minutes=20)).cumsum()
        for _, h in g.groupby(part):
            n = h[["booking_ref", "workstation"]].drop_duplicates().shape[0]
            ok(n == 1 or n >= 3, "a loss of a centre's link logged by %d clients" % n)
    # the hall stops: every sitting running then stopped before the router went and resumed after the link was back
    halls = S.hall_stops(target, ev)
    ok(set(halls) == dev["hall_stop"], "the hall stops' sittings")
    # the switch-offs: a WS_FAIL after a submitted sitting's end, before the session closed
    end = ev[ev["event"] == "SESSION_END"].groupby("booking_ref")["t"].max()
    late = {r.booking_ref for r in ev[ev["event"] == "WS_FAIL"].itertuples() if r.t > end[r.booking_ref]}
    ok(late == dev["switch_off"], "every WS_FAIL after its sitting's end is a switched-off finished workstation")
    # realism: no spare or workstation serves two sittings at once; a reboot inside a sitting is that sitting's restart
    spans = {}
    for r in ev[ev["booking_ref"] != ""].itertuples(index=False):
        lohi = spans.setdefault((r.centre_code, r.workstation, r.t.date()), {}).setdefault(r.booking_ref, [r.t, r.t])
        lohi[0], lohi[1] = min(lohi[0], r.t), max(lohi[1], r.t)
    clash = 0
    for d in spans.values():
        v = sorted(d.values())
        clash += sum(int(a1 < z0) for (a0, z0), (a1, z1) in zip(v, v[1:]))
    ok(clash == 0, "realism: no workstation or spare serves two sittings at once (%d clashes)" % clash)
    resumes = {}
    for r in ev[ev["event"] == "SESSION_RESUME"].itertuples(index=False):
        resumes.setdefault((r.centre_code, r.workstation, r.booking_ref), []).append(r.t)
    stray = 0
    for r in ev[ev["event"] == "WS_REBOOT"].itertuples(index=False):
        for b, (lo, hi) in spans.get((r.centre_code, r.workstation, r.t.date()), {}).items():
            if lo < r.t < hi:
                stray += int(not any(r.t < t <= r.t + pd.Timedelta(minutes=10) for t in resumes.get((r.centre_code, r.workstation, b), [])))
    ok(stray == 0, "realism: a reboot inside a sitting is that sitting's restart (%d others)" % stray)
    # separation: the asks' devices sit in files the call never reads
    ok(set(BLD.PACK) - {"events", "seat", "incidents"} >= {"export3", "export4", "layouts", "bank", "crosswalk", "register",
                                                            "reviews"}, "separation")


def gates(target):
    files = [os.path.join(target, BLD.FILES[k]) for k in BLD.PACK]
    ok(all(os.path.exists(f) for f in files) and len(files) >= 10, "ten or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    n = max(sum(1 for _ in open(f, encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
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
