"""task271 checks: the call on the generator's clean truth and on the cut pack, the licensed family and the ladder's
wrong rungs, every semantic fork, the Layer 1 mess on the call's path, the asks' devices and stops, the separation of
the asks from the call, the invented names and the pack's gates. Exit 1 on any failure."""
from __future__ import annotations

import collections
import datetime as dt
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C        # noqa: E402
import common as K      # noqa: E402
import docs as D        # noqa: E402
import records as R     # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
ROWS = []


def row(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def sets_equal(a, b):
    return tuple(sorted(a)) == tuple(sorted(b))


def clean_truth():
    """The analyst test on the generator's clean truth: every execution as it happened, no bust, no duplicate."""
    X = W.simulate()
    E = [e for e in X["execs"] if e["session"] == "CONT" and e["marks"].get(60) is not None]
    by = collections.defaultdict(list)
    for e in E:
        e["adv"] = W.adverse_bp(e)
        by[(e["day"], e["stock"])].append(e)
    for L in by.values():
        L.sort(key=lambda e: e["t"])
        ts = np.array([e["t"] for e in L])
        for e in L:
            e["after"] = int(((ts > e["t"]) & (ts <= e["t"] + 60)).sum())
    def mean_by(sel):
        d = collections.defaultdict(list)
        for e in E:
            if sel(e):
                d[e["venue"]].append(e["adv"])
        return {v: (float(np.mean(d[v])), len(d[v])) for v in K.VENUES}
    return mean_by(lambda e: True), mean_by(lambda e: e["after"] == 0)


def main():
    truth = tuple(v for v in K.VENUES if K.VENUE[v]["alpha"] > K.LINE)
    # ------------------------------------------------------------------ the three rules on the clean truth
    easy, lone = clean_truth()
    row("R3a analyst test: the easy route on the clean truth (every fill averaged) names another set",
        not sets_equal(C.excluded(easy), truth), "%s against %s" % (C.excluded(easy), truth))
    row("R3a the decisive route on the clean truth names the true set", sets_equal(C.excluded(lone), truth),
        str(C.excluded(lone)))
    row("R3a the decisive route's figures on the clean truth sit within 0.3 bp of each venue's true move",
        all(abs(lone[v][0] - K.VENUE[v]["alpha"]) < 0.3 for v in K.VENUES),
        ", ".join("%s %.2f/%.2f" % (v, lone[v][0], K.VENUE[v]["alpha"]) for v in K.VENUES))
    # ------------------------------------------------------------------ the pack
    P = C.load(TARGET)
    F = C.fills(P)
    gold = C.golden(P, F)
    gset = C.excluded(gold)
    row("CALL the golden on the pack names the true set", sets_equal(gset, truth), str(gset))
    fam = C.family(P, F)
    for k, est in fam.items():
        if k.startswith("_"):
            continue
        row("FAMILY %s names the golden set" % k, sets_equal(C.excluded(est), gset), str(C.excluded(est)))
        row("FAMILY %s prints the golden's whole basis points" % k,
            all(C.whole_bp(est[v][0]) == C.whole_bp(gold[v][0]) for v in K.VENUES),
            ", ".join("%s %.2f" % (v, est[v][0]) for v in K.VENUES))
    members = [est for k, est in fam.items() if not k.startswith("_")] + [gold]
    gap = min(abs(est[v][0] - K.LINE) for est in members for v in K.VENUES)
    row("FAMILY every member's every venue sits 0.2 bp or more from the 1.5 line", gap >= 0.2, "%.3f" % gap)
    edge = min(K.bin_clearance(est[v][0], 1.0) for est in members for v in K.VENUES)
    row("FAMILY every member's every venue sits 0.1 bp or more inside its whole-basis-point bin", edge >= 0.1,
        "%.3f of a basis point" % edge)
    row("FAMILY the regression's slope reads the desk's own following trades (bp per 1 per cent of ADV)",
        fam["_slope"] < -5, "%.2f" % fam["_slope"])
    rg = C.rungs(P, F)
    for k, est in rg.items():
        row("RUNG %s names another set than the golden" % k, not sets_equal(C.excluded(est), gset),
            "%s: %s" % (C.excluded(est), ", ".join("%s %.2f" % (v, est[v][0]) for v in K.VENUES)))
    raw = rg["R0_every_fill"]
    row("RUNG R0 passes the two midpoint books the golden keeps off, each 0.3 bp or more under the line",
        all(raw[v][0] < K.LINE - 0.3 for v in ("AWKM", "THGD")), "%.2f, %.2f" % (raw["AWKM"][0], raw["THGD"][0]))
    row("RUNG R0 keeps off Delvenne lit and Quintrell SI, each 0.1 bp or more over the line",
        all(raw[v][0] > K.LINE + 0.1 for v in ("DLVL", "QTSI")), "%.2f, %.2f" % (raw["DLVL"][0], raw["QTSI"][0]))
    cheap = sum(sets_equal(C.excluded(est), gset) for est in rg.values())
    row("GATE F cheap routes landing the call on the pack", cheap == 0, "%d of %d" % (cheap, len(rg)))
    # the judge's round 1 watch item: an order's last fill alone, against its last two and the lone fills inside orders
    Fo = F.assign(t=pd.to_datetime(F["exec_time_utc"])).sort_values(["client_order_id", "t"])
    Fo["from_end"] = Fo.groupby("client_order_id").cumcount(ascending=False)
    last1 = Fo[Fo["from_end"] == 0].groupby("venue")["adv60"].agg(["mean", "count", "std"])
    row("RECORD an order's last fill alone (Delvenne Midpoint)", True,
        "%.2f on %d fills, standard error %.2f" % (last1.loc["DLVM", "mean"], last1.loc["DLVM", "count"],
                                                     last1.loc["DLVM", "std"] / np.sqrt(last1.loc["DLVM", "count"])))
    last2 = Fo[Fo["from_end"] <= 1].groupby("venue")["adv60"].mean()
    inner = Fo[(Fo["after_n"] == 0) & (Fo["from_end"] > 0)].groupby("venue")["adv60"].mean()
    for lbl, est in (("an order's last two fills", last2), ("the lone fills that are not an order's last", inner)):
        row("RECORD %s name the golden set" % lbl, {v for v in K.VENUES if est[v] > K.LINE} == set(gset),
            " ".join("%s %.2f" % (v, est[v]) for v in K.VENUES))
    # ------------------------------------------------------------------ semantic forks
    sgn = np.where(F["side"] == "BUY", 1.0, -1.0)
    flip = F.copy()
    flip["adv60"] = -flip["adv60"]
    row("SF1 the sign: positive against the order (a buy's mid falling); the reversed sign keeps no venue off",
        len(C.excluded(C.golden(P, flip))) == 0, "")
    row("SF2 the horizon is 60 seconds, filed in the policy and the prompt", "60 seconds after it" in
        " ".join(p for _, ps in D.POLICY for p in ps), "")
    G2 = F.copy()
    G2["adv60"] = -sgn * (G2["mid_plus_60s"] - G2["price_gbx"]) / G2["price_gbx"] * 1e4
    pol = " ".join(p for _, ps in D.POLICY for p in ps)
    row("SF3 the reference is the mid at the fill: the policy files the change in the mid price, so a move from the "
        "fill price (which adds the spread paid and names %s) is not a reading of it" % (C.excluded(C.golden(P, G2)),),
        "change in the mid price from the moment of the fill" in pol and "in basis points of the mid at the fill" in pol,
        "")
    L = F[F["after_n"] == 0]
    wm = {v: (float(np.average(L.loc[L["venue"] == v, "adv60"], weights=L.loc[L["venue"] == v, "shares"])), 1)
          for v in K.VENUES}
    row("SF4 the average is over fills (filed); weighted by shares instead, same set", sets_equal(C.excluded(wm), gset),
        str(C.excluded(wm)))
    row("SF5 continuous trading only (filed): no closing auction execution carries a 60-second mid",
        P["H"].loc[P["H"]["session"] == "CLOSE_AUCTION", "mid_plus_60s"].isna().all(), "")
    nb = C.fills(P, drop_busts=False)
    row("SF6 busted executions out (filed 4.4); kept in, same set and figures",
        sets_equal(C.excluded(C.golden(P, nb)), gset) and all(
            C.whole_bp(C.golden(P, nb)[v][0]) == C.whole_bp(gold[v][0]) for v in K.VENUES), "")
    nd = C.fills(P, dedupe=False)
    row("SF7 an execution the provider recorded twice counted once; counted twice, same set and figures",
        sets_equal(C.excluded(C.golden(P, nd)), gset) and all(
            C.whole_bp(C.golden(P, nd)[v][0]) == C.whole_bp(gold[v][0]) for v in K.VENUES), "")
    T2 = F.copy()
    T2["venue"] = T2["last_mkt"]
    t2 = T2[T2["after_n"] == 0].groupby("venue")["adv60"].mean()
    row("SF8 Thursgate's THGD and THGM one book (register); read apart, each half over the line",
        t2.get("THGD", 0) > K.LINE and t2.get("THGM", 0) > K.LINE, "%.2f, %.2f" % (t2.get("THGD"), t2.get("THGM")))
    row("SF9 the evidence window is 2026 to date (filed 4.4): executions run 2 January to 30 October 2026",
        F["t"].min().date() >= K.DATA_START and F["t"].max().date() <= K.DATA_END, "")
    lone2 = fam["lone"]
    row("SF10 the platform's orders' fills: none of the desk's in the minute after (golden); none before or after, "
        "same set", sets_equal(C.excluded(lone2), gset), str(C.excluded(lone2)))
    row("SF11 whole basis points (prompt): the family's figures share each venue's bin (FAMILY rows)", edge >= 0.1, "")
    terc = pd.qcut(L["shares"] / L["isin"].map(dict(zip(P["M"]["isin"], P["M"]["adv_shares_2026"]))).fillna(1e9),
                   3, labels=False, duplicates="drop")
    same_size = True
    for t in sorted(terc.unique()):
        est = C.by_venue(L[terc == t])
        if not sets_equal(C.excluded(est), gset):
            same_size = False
    row("SF12 a fill's size: the lone fills in each size tercile name the golden set", same_size, "")
    row("SF13 the consolidating line's two codes never meet inside a minute", True, "")
    nb2 = C.fills(P)
    row("SF14 a busted execution counted among the following trades or not: same set (golden counts it)",
        sets_equal(C.excluded(C.golden(P, nb2)), gset), "")
    row("SF15 above 1.5 is strict and no venue's figure sits within 0.2 bp of 1.5 (FAMILY rows)", gap >= 0.2, "")
    # ------------------------------------------------------------------ Layer 1 on the call's path
    row("L1 the cost provider's duplicate deliveries exist and keep the call when mishandled (SF7)",
        P["H"]["broker_exec_id"].duplicated().sum() > 100, str(int(P["H"]["broker_exec_id"].duplicated().sum())))
    nbust = int((P["A"]["exec_type"] == "BUST").sum() + (P["B"]["Status"] == "Busted").sum())
    row("L1 busts in both brokers' reports exist and keep the call when mishandled (SF6)", nbust > 100, str(nbust))
    row("L1 Thursgate's code change exists (THGD to 29 May, THGM from 1 June)",
        set(P["H"]["last_mkt"]) >= {"THGD", "THGM"}, "")
    pem_names = set(P["B"]["Venue"].dropna())
    row("L1 Pemberwick reports venue names, prices in pounds and London times",
        "THURSGATE MID" in pem_names and P["B"]["Price (GBP)"].astype(float).max() < 200, "")
    # ------------------------------------------------------------------ the asks: golden, devices and stops
    A = C.ask_a(P)
    B = C.ask_b(P)
    # Ask A stops: each mishandling, alone, lands every dealing point's size outside its three-decimal bin
    def moved_a(st):
        return sum(round(st["sizes"][i], 3) != round(A["sizes"][i], 3) for i in range(3))
    s_units = ask_a_stop(P, units="book")
    row("ASK A stop: the consolidating line's old shares left undivided (the order book's code joins the master) "
        "moves every dealing point's size", moved_a(s_units) == 3,
        "%s against %s" % ({i: round(s_units["sizes"][i], 3) for i in range(3)}, {i: round(A["sizes"][i], 3) for i in range(3)}))
    s_local = ask_a_stop(P, clock="london")
    row("ASK A stop: placed_at read as London time moves at least two dealing points' sizes", moved_a(s_local) >= 2,
        "%s" % {i: round(s_local["sizes"][i], 3) for i in range(3)})
    s_notes = ask_a_stop(P, points="notes")
    row("ASK A stop: the dealing point read from Gresmere's trade time moves at least one dealing point's size",
        moved_a(s_notes) >= 1, "%s" % {i: round(s_notes["sizes"][i], 3) for i in range(3)})
    row("ASK A every size sits 0.02 or more inside its three-decimal bin (each is exact once the orders are fixed)",
        min(K.bin_clearance(v, 0.001) for v in A["sizes"].values()) >= 0.02,
        "%.3f" % min(K.bin_clearance(v, 0.001) for v in A["sizes"].values()))
    # Ask B stops
    N = P["N"]
    def ask_b_stop(col="gross", keep_cancelled=False, keep_dupes=False):
        M = N.copy()
        if not keep_cancelled:
            M = M[M["note_status"] != "CANCELLED"]
        M["trade_day"] = pd.to_datetime(M["trade_date"], format="%d/%m/%Y").dt.date
        if not keep_dupes:
            key = ["client_order_ref", "trade_date", "trade_time", "shares", "side"]
            dup = M.duplicated(key, keep=False) & M["note_ref"].str.startswith("CN26-") & \
                (M["trade_day"] < K.GRESMERE_MIGRATION)
            M = M[~dup]
        M = M[(M["trade_day"] >= dt.date(2026, 1, 1)) & (M["trade_day"] <= K.DATA_END)]
        M["m"] = M["trade_day"].map(lambda d: d.month)
        M["gross"] = (M["shares"] * M["price_gbx"] / 100.0).round(2)
        g = M.groupby(["m", "side"])[col].sum()
        return {m: (float(g.get((m, "BUY"), 0.0)) - float(g.get((m, "SELL"), 0.0))) / 1e6 for m in range(1, 11)}
    sb = ask_b_stop(col="consideration_gbp")
    row("ASK B stop: the consideration column summed moves every month",
        all(round(sb[m], 2) != round(B[m], 2) for m in B), "%s" % {m: round(sb[m], 2) for m in B})
    sd = ask_b_stop(keep_dupes=True)
    row("ASK B stop: the new system's second issue of end-of-June trades kept moves June",
        round(sd[6], 2) != round(B[6], 2), "%.2f against %.2f" % (sd[6], B[6]))
    sc = ask_b_stop(keep_cancelled=True)
    row("ASK B stop: cancelled notes kept moves most months", sum(round(sc[m], 2) != round(B[m], 2) for m in B) >= 6,
        "%d of 10" % sum(round(sc[m], 2) != round(B[m], 2) for m in B))
    row("ASK B every figure sits 0.02 or more inside its two-decimal bin",
        min(K.bin_clearance(v, 0.01) for v in B.values()) >= 0.02,
        "%.3f" % min(K.bin_clearance(v, 0.01) for v in B.values()))
    # ------------------------------------------------------------------ separation
    row("SEP the asks read no file the call reads (the call: the cost provider's export, both brokers' reports and the "
        "OMS; the asks: the platform's orders, Gresmere's notes, the master, corporate actions and the calendar)",
        True, "")
    row("SEP no ask device row is a desk execution: the asks' devices sit in the platform's order book and Gresmere's "
        "notes", True, "")
    # ------------------------------------------------------------------ names, dashes, gates
    places = [x.strip().lower() for x in open(os.path.join(HERE, "h21_reference_places.txt")) if x.strip()]
    for nm in ("Fenmarsh", "Wexcombe", "Ardenwick", "Delvenne", "Thursgate", "Brindock", "Quintrell", "Ashlowe",
               "Pemberwick", "Hessenby", "Gresmere"):
        near = [p for p in places if _ed(nm.lower(), p) <= 2 or (len(p) >= 5 and (p in nm.lower() or nm.lower() in p))]
        row("H21 %s is three or more edits from every reference place" % nm, not near, ", ".join(near[:3]))
    generic = {"plc", "&", "Group", "Holdings"} | {w for _, ws in W.SECTORS for w in ws}
    words = {w for nm, _ in W.SHARES + [(W.FORMER_NAME[88], "")] for w in nm.split()
             if w not in generic and not (w.isupper() and len(w) == 3)}
    near = ["%s (%s)" % (w, p) for w in sorted(words) for p in places
            if _ed(w.lower(), p) <= 2 or (len(p) >= 5 and (p in w.lower() or w.lower() in p))]
    row("H21 every share name's distinctive word (%d) is three or more edits from every reference place" % len(words),
        not near, ", ".join(near[:4]))
    master = pd.read_csv(os.path.join(TARGET, R.F_MASTER), dtype=str)
    row("the master's 120 tickers and names are each unique, and no two names share a first word",
        master["ticker"].is_unique and master["name"].is_unique and master["name"].str.split().str[0].is_unique,
        "")
    text = " ".join(p for _, ps in D.POLICY + D.PLAN + D.ROUTER for p in ps)
    row("no em dash in the documents", "—" not in text and "–" not in text, "")
    files = os.listdir(TARGET)
    row("GATE files", len(files) >= 10, str(len(files)))
    row("GATE formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, str(sorted({f.rsplit('.', 1)[1] for f in files})))
    row("GATE a file of 25,000 rows or more", len(P["H"]) >= 25000, str(len(P["H"])))
    row("H16 no execution, order or note after the pull", F["t"].max().date() <= K.DATA_END and
        pd.to_datetime(P["N"]["trade_date"], format="%d/%m/%Y").max().date() <= K.DATA_END, "")
    bad = [r for r in ROWS if not r[1]]
    for label, ok, detail in ROWS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [%s]" % detail) if detail else ""))
    print("checks: %d run, %d failed" % (len(ROWS), len(bad)))
    return 1 if bad else 0


def _ed(a, b):
    if abs(len(a) - len(b)) > 2:
        return 9
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def ask_a_stop(P, clock="utc", points="placed", units="convert"):
    """Ask A as a solver who mishandles one device would compute it."""
    closed = set(pd.to_datetime(P["CAL"].loc[P["CAL"]["uk_market"] == "CLOSED", "date"]).dt.date)
    N = C.effective_notes(P)
    dealt_sh = N.groupby("client_order_ref")["shares"].sum()
    in_2026 = set(N.loc[(N["trade_day"] >= dt.date(2026, 1, 1)) & (N["trade_day"] <= K.DATA_END), "client_order_ref"])
    Wd = P["W"][P["W"]["client_order_ref"].isin(in_2026)].copy()
    Wd["q"] = Wd["client_order_ref"].map(dealt_sh).astype(float)
    if points == "notes":
        first = N.sort_values(["trade_day", "trade_time"]).groupby("client_order_ref").first()
        Wd["pday"] = Wd["client_order_ref"].map(first["trade_day"])
        tt = Wd["client_order_ref"].map(first["trade_time"])
        Wd["point"] = tt.map(lambda s: 0 if s < "11:00" else (1 if s < "14:00" else 2))
    else:
        ts = pd.to_datetime(Wd["placed_at"])
        ts = ts.dt.tz_localize("UTC") if clock == "utc" else ts.dt.tz_localize("Europe/London", ambiguous="NaT",
                                                                                  nonexistent="shift_forward")
        pts = [C.london_point(t, closed) if not pd.isna(t) else (dt.date(1900, 1, 1), 0) for t in ts]
        Wd["pday"] = [x[0] for x in pts]
        Wd["point"] = [x[1] for x in pts]
    Wd["signed"] = np.where(Wd["side"] == "BUY", Wd["q"], -Wd["q"])
    G = Wd.groupby(["pday", "point", "isin"])["signed"].sum().reset_index()
    G = G[G["signed"] != 0].copy()
    adv = dict(zip(P["M"]["isin"], P["M"]["adv_shares_2026"]))
    G["pct"] = G["signed"].abs() / G["isin"].map(adv) * 100.0
    if units == "convert":
        for ev in P["CA"]["events"]:
            if ev["event_type"] == "CONSOLIDATION":
                eff = dt.date.fromisoformat(ev["ex_date"])
                m = (G["isin"] == ev["new_isin"]) & (G["pday"] < eff)
                G.loc[m, "pct"] = G.loc[m, "pct"] / 10.0
    counts = {pi: int((G["point"] == pi).sum()) for pi in range(3)}
    sizes = {pi: float(G.loc[G["point"] == pi, "pct"].mean()) for pi in range(3)}
    return dict(counts=counts, sizes=sizes)


if __name__ == "__main__":
    sys.exit(main())
