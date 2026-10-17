"""task235 checks: the three rules executed on the simulator's clean truth (R1 to R3c), every semantic fork row (SF1 to
SF12), the golden against the truth with its margins, the rungs, the ask devices and their stops, the separation of the
call from the devices, the documents' pins, the input gates and the realism sweep."""
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

import estim as E
import params as P

N = [0]
GOLD = {("android", "7.41.0"), ("ios", "7.42.0")}
DEFAULT = {("android", "7.38.1"), ("android", "7.41.0"), ("ios", "7.38.2"), ("ios", "7.39.1"), ("ios", "7.40.0")}
ACCOUNT_FALSE = {("ios", "7.38.2"), ("ios", "7.39.1"), ("ios", "7.40.0")}
TESTED = {("ios", "7.41.0"), ("ios", "7.41.1"), ("ios", "7.42.0"), ("android", "7.41.0"), ("android", "7.41.3"),
          ("android", "7.42.0")}
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))


def ok(cond, label):
    assert cond, label
    N[0] += 1


def irish(t):
    return (t + pd.to_timedelta(np.where(t < pd.Timestamp(P.IST_END), 1, 0), unit="h")).dt.date


def clean_truth(W):
    """the world before any record is written: the game's purchases in the window with the fate of each event"""
    p = W.purchases.copy()
    p["day"] = irish(p.purchased_at)
    p = p[(p.day >= E.WIN0) & (p.day <= E.WIN1)].copy()
    p["build"] = list(zip(p.platform, p.version))
    p["matched"] = p.received.notna()
    p["due"] = p.next_start.notna() & (p.next_start < pd.Timestamp(P.RUN))
    p["held"] = p.matched & p.due & (p.received >= p.next_start)
    p["age_d"] = (pd.Timestamp(P.RUN) - p.purchased_at).dt.total_seconds() / 86400
    return p


def golden_on(p):
    out = {}
    for b, g in p.groupby("build"):
        lost = int((g.due & ~g.matched).sum()); held = int(g.held.sum()); pend = int((~g.due & ~g.matched).sum())
        q = lost / (lost + held) if lost + held else 0.0
        out[b] = (lost + pend * q) / len(g)
    return out


def call_on(D, p=None, clock="irish"):
    q = E.conform(D, clock, p)
    return E.alerted(E.loss(q)), E.loss(q)


def run(target, golden, o, X):
    N[0] = 0
    W, R = o["W"], o["R"]
    D, p = X["D"], X["p"]
    G, C = X["gold"], X["counts"]
    files = {k: os.path.join(target, f) for k, f in __import__("build").FILES.items()}
    cat = _pdf_text(files["cat"])
    sdk = open(files["sdk"]).read()
    dic = open(files["dict"]).read()

    # ------------------------------------------------------------ R1: the field's raw material ships, no deciding column
    cols = []
    for k in ("val", "evt", "ses", "links", "rates"):
        cols += list(pd.read_csv(files[k], nrows=1).columns)
    ok(not any(re.search(r"loss|lost|alert|due|late|held|lag|delay|pending|settle|matched|missing", c, re.I) for c in cols),
       "R1 no shipped column holds a loss, an alert, a due or late flag, a lag or a match")
    ok(len(D["ses"]) >= 300_000 and D["ses"].device_id.nunique() >= 12_000,
       "R1 the session service's starts ship row by row for every phone (%d starts)" % len(D["ses"]))
    ok(p.device_id.isin(set(D["ses"].device_id)).all(), "R1 every purchase's phone has its session starts in the log")
    ok(len(p) == sum(c["n"] for c in C.values()) and p.store_transaction_id.is_unique,
       "R1 the golden reads every purchase of the window at its own grain (%d)" % len(p))
    for phrase in ("uploaded in batches when the game starts and every 30 seconds", "The queue is kept when the game is closed",
                   "sent as soon as StoreKit reports the transaction", "WorkManager"):
        ok(phrase in sdk, "R1 the SDK notes carry the delivery facts: %s" % phrase)

    # ------------------------------------------------------------ the golden against the clean truth
    T = clean_truth(W)
    tb = {b: g for b, g in T.groupby("build")}
    ok(set(tb) == set(E.ORDER) and len(T) == len(p), "C1 the window holds the same %d purchases in the world and the pack" % len(T))
    for b in E.ORDER:
        g = tb[b]
        c = C[b]
        same = (len(g) == c["n"] and int(g.due.sum()) == c["due"] and int((g.due & ~g.matched).sum()) == c["lost"]
                and int(g.held.sum()) == c["held"] and int((~g.due & ~g.matched).sum()) == c["pending"])
        ok(same, "C1 %s: purchases, due, lost, held and open events in the pack equal the clean truth's" % (b,))
    drop = {b: float((g.route == "dropped").mean()) for b, g in tb.items()}
    ok(E.alerted(drop) == GOLD, "truth: the builds that drop more than 2 per cent of their events are the golden pair")
    ok(min(drop[b] for b in GOLD) >= 0.045 and max(drop[b] for b in drop if b not in GOLD) <= 0.01,
       "truth: the golden pair drop %.1f and %.1f per cent, every other build 1 per cent or less"
       % (100 * drop[("android", "7.41.0")], 100 * drop[("ios", "7.42.0")]))
    ok(all(abs(G[b] - drop[b]) <= 0.01 for b in E.ORDER), "truth: every build's golden within 1 point of its drop share")
    ok(X["esc"] == GOLD, "golden: alert Android 7.41.0 and iOS 7.42.0")

    # ------------------------------------------------------------ R3a: the analyst test on the clean truth
    s7 = {}
    for b, g in tb.items():
        x = g[g.age_d >= 7]
        s7[b] = 1 - x.matched.mean() if len(x) else float("nan")
    ok(E.alerted(s7) == DEFAULT and E.alerted(X["routes"]["settle7"]) == DEFAULT,
       "R3a the seven-day window on the clean truth alerts Android 7.38.1, 7.41.0, iOS 7.38.2, 7.39.1, 7.40.0, as on the pack")
    ok(all(s7[b] != s7[b] for b in E.NEW), "R3a the 7.42.0 builds have no purchase seven days old")
    ok(len(E.alerted(s7) ^ GOLD) == 5, "R3a the default path files 5 of the 12 builds wrong")
    s7b = {b: float(((g.age_d >= 7) & ~g.matched).sum()) / len(g) for b, g in tb.items()}
    ok(E.alerted(s7b) == DEFAULT and E.alerted(X["routes"]["settle7_all"]) == DEFAULT,
       "R3a the seven-day window with the younger purchases kept as not yet lost: the same five builds (truth and pack)")
    ok(min(s7[b] for b in DEFAULT - GOLD) - E.LINE >= 0.007,
       "R3a every false alert of the default path is 0.7 points or more above the line")
    # ------------------------------------------------------------ R3b: the decisive step alone
    ok(E.alerted(golden_on(T)) == GOLD, "R3b only the phone's next session: the golden on the clean truth")
    ok(all(abs(golden_on(T)[b] - G[b]) < 1e-12 for b in E.ORDER), "R3b the clean truth's figures equal the pack's")
    for days in (11, 14, 21):
        s = {}
        for b, g in tb.items():
            x = g[g.age_d >= days]
            s[b] = 1 - x.matched.mean() if len(x) else float("nan")
        ok(E.alerted(s) == {("android", "7.41.0")}, "R3b a %d-day window alone: Android 7.41.0, iOS 7.42.0 missed" % days)
    # the account's next session on the clean truth
    S = W.sessions.sort_values("start")
    acc_starts = {a: g.start.values for a, g in S.groupby("account")}
    na = E.next_start(acc_starts, T.account, T.purchased_at.values)
    Ta = T.assign(due=np.asarray(na.notna()), next_start=np.asarray(na))
    Ta["held"] = Ta.matched & Ta.due & (Ta.received >= Ta.next_start)
    ok(E.alerted(golden_on(Ta)) == GOLD | ACCOUNT_FALSE and E.alerted(X["routes"]["account"]) == GOLD | ACCOUNT_FALSE,
       "R3b the account's next session instead of the phone's: false alerts on iOS 7.38.2, 7.39.1, 7.40.0 (truth and pack)")

    # ------------------------------------------------------------ the rungs on the pack
    rt = X["routes"]
    ok(E.alerted(rt["settle11"]) == {("android", "7.41.0")} and E.alerted(rt["settle14"]) == {("android", "7.41.0")},
       "rung 1: windows of 11 and 14 days alert Android 7.41.0 alone")
    ok(len(E.alerted(rt["settle0"])) == 8 and E.alerted(rt["settle0"]) >= GOLD, "rung 1: every missing event lost alerts 8")
    ok(all(abs(rt["settle0"][b] - rt["upper"][b]) < 1e-12 for b in E.ORDER),
       "rung 1: every missing event lost is every open event lost")
    cu = E.alerted(rt["curve"])
    ok(len(cu ^ GOLD) == 6 and ("ios", "7.42.0") not in cu, "rung 1: the pooled arrival curve files 6 wrong, iOS 7.42.0 missed")
    for w, v in X["short"].items():
        a, i = v[("android", "7.42.0")], v[("ios", "7.42.0")]
        if w <= 2.5:
            ok(a[0] > E.LINE, "rung 1: at a %.2f-day window Android 7.42.0 reads %.2f, above the line" % (w, 100 * a[0]))
        ok(not (i[0] > E.LINE) or a[0] > E.LINE, "rung 1: no window alerts iOS 7.42.0 without Android 7.42.0 (%.2f days)" % w)
    ma = X["matched_age"]
    ok(ma[("android", "7.42.0")][0] - ma[("android", "7.42.0")][1] >= 0.015 and
       ma[("ios", "7.42.0")][1] - ma[("ios", "7.42.0")][0] >= 0.03,
       "rung 1: against same-age purchases Android 7.42.0 reads %.2f over %.2f and iOS 7.42.0 %.2f under %.2f"
       % tuple(100 * x for x in (ma[("android", "7.42.0")] + ma[("ios", "7.42.0")])))
    ok(E.alerted(rt["due"]) == GOLD and E.alerted(rt["lower"]) == GOLD,
       "SF6 the loss over the purchases whose phone came back, and every open event delivered: the golden pair")
    cor = X["corridor"]
    for name, v in cor.items():
        ok(E.alerted(v) == GOLD, "C3 SF6 the open purchases at the %s rate: the golden pair" % name)
    ok(abs(X["plat_q"]["ios"] - 0.0372) < 0.0005 and abs(X["plat_q"]["android"] - 0.1816) < 0.0005
       and abs(X["pooled_q"] - 0.1129) < 0.0005, "C3 the platform and pooled resolved shares (3.72, 18.16, 11.29 per cent)")
    worst = max(v[b] for v in list(cor.values()) + [rt["lower"]] for b in E.ORDER if b not in GOLD)
    ok(worst <= 0.0168 + 1e-9, "C3 every other build at %.2f per cent or less under every rate" % (100 * worst))
    ok(all(abs(cor["own"][b] - G[b]) < 1e-12 for b in E.ORDER), "C3 the build's own rate is the chart's figure")

    # ------------------------------------------------------------ margins
    for b in GOLD:
        ok(X["lo"][b] - E.LINE >= 0.01, "margin: %s above the line by a point or more however its open events end (%.2f)"
           % (b, 100 * X["lo"][b]))
    ok(C[("android", "7.41.0")]["pending"] == 0, "margin: Android 7.41.0 has no open event (its share known outright)")
    for b in set(E.ORDER) - GOLD:
        c = C[b]
        ok(G[b] <= 0.006, "margin: %s at %.2f per cent" % (b, 100 * G[b]))
        ok(E.flip_share(c) >= 0.2 and E.flip_share(c) >= 5 * E.resolved_share(c),
           "margin: %s crosses the line only if %.0f per cent of its open events were lost, where %.0f per cent of its "
           "resolved gaps were" % (b, 100 * min(E.flip_share(c), 9.99), 100 * E.resolved_share(c)))
    for b in E.ORDER:
        x = 100 * X["per_player_raw"][b]
        ok(abs((x - np.floor(x)) - 0.5) >= 0.05,
           "bin: %s's gross bookings per paying player %.5f sits 0.05 cent or more from a rounding edge"
           % (b, X["per_player_raw"][b]))

    # ------------------------------------------------------------ semantic fork table
    v = D["val"]
    reg = D["builds"]
    ok(set(v[v.transaction_kind == "purchase"].app_build) <= set(reg.build_number.astype(str)) and len(reg) == 12,
       "SF1 every purchase's build number is one of the register's twelve")
    ok((v[v.transaction_kind == "renewal"].app_build == "").all(), "SF2 renewals carry no build")
    pt = E.purchases(D, testers=True)
    ok(call_on(D, pt)[0] == GOLD and len(pt) > len(p), "R2 SF2 testers' purchases kept: same call")
    pr = E.purchases(D, renewals=True)
    ok(call_on(D, pr)[0] == GOLD and len(pr) > len(p), "R2 SF2 renewals kept: same call")
    refunded = set(v[v.transaction_kind == "refund"].store_transaction_id)
    pf = E.purchases(D)
    pf = pf[~pf.store_transaction_id.isin(refunded)]
    ok(call_on(D, pf)[0] == GOLD and len(pf) < len(p), "SF2 refunded purchases dropped: same call")
    e = D["evt"]
    ok(len(e) > e.event_id.nunique() > e.store_transaction_id.nunique(),
       "SF3 duplicate uploads (one event id twice) and restored events (a new id, the same transaction) exist")
    el = e.assign(recv=E.utc(e.received_at)).sort_values(["store_transaction_id", "recv"])
    el = el.drop_duplicates("store_transaction_id", keep="last").set_index("store_transaction_id")
    q = p.copy(); q["recv"] = q.store_transaction_id.map(el.recv); q["held"] = q.matched & q.due & (q.recv >= q.next)
    ok(E.alerted(E.loss(q)) == GOLD, "R2 SF3 each transaction's latest event copy instead of its first: same call")
    ev = E.events(D)
    m = p.store_transaction_id.isin(ev.index)
    ok((p.loc[m, "store_transaction_id"].map(ev.app_version).values == p.loc[m, "build"].map(lambda b: b[1]).values).all(),
       "R2 SF4 every matched event names the validation's build version")
    ok(call_on(D, clock="utc")[0] == GOLD, "R2 SF5 UTC dates: same call")
    v2 = v.copy(); v2["purchased_at"] = v2["validated_at"]
    ok(call_on(dict(D, val=v2))[0] == GOLD, "SF5 the validation time for the purchase time: same call")
    ok("lost only if it never will" in cat and E.alerted(rt["settle0"]) != GOLD,
       "SF6 every missing event counted lost alerts 8; KC-DQ-04 s.4's 'lost only if it never will' rules it out")
    ok(min(X["lo"][b] for b in GOLD) - E.LINE >= 0.01 and E.LINE - worst >= 0.003,
       "SF7 no build on the line: the alerted pair a point or more above it however their open events end, every other "
       "build 0.3 points or more below it under every rate")
    W_ = W.purchases
    edge = W_[(W_.route == "waiting") & W_.next_start.notna() & (W_.next_start < pd.Timestamp(P.RUN))]
    ok(len(edge) == 0, "SF8 no event of a purchase whose phone opened the game before the run arrives after it")
    pv = v[(v.transaction_kind == "purchase") & (v.environment == "Production") & (v.purchase_type == "standard")]
    ok(pv.store_transaction_id.is_unique, "SF9 no purchase validated twice")
    ok((p.loc[m, "store_transaction_id"].map(ev.device_id).values == p.loc[m, "device_id"].values).all(),
       "SF10 every matched event names the validation's device")
    ok((reg.status == "production").all(), "SF11 the register lists all twelve builds as in production")
    ok(E.alerted({b: round(G[b], 4) for b in G}) == GOLD and all(E.alerted(v) == GOLD for v in cor.values()),
       "SF12 the chart's loss at any rate for the open purchases, or rounded first: the same two builds above the line")
    # device clocks: the event's client_ts in place of the purchase time
    ct = e.assign(ct=pd.to_datetime(e.client_ts.astype("int64"), unit="ms")).sort_values(["store_transaction_id", "ct"])
    ct = ct.drop_duplicates("store_transaction_id").set_index("store_transaction_id")
    pc = E.purchases(D)
    mc = pc.store_transaction_id.isin(ct.index)
    pc.loc[mc, "t"] = pc.loc[mc, "store_transaction_id"].map(ct.ct).values
    ok(call_on(D, pc)[0] == GOLD, "R2 device clocks taken for the purchase time: same call")
    skew = (pc.loc[mc, "t"] - E.purchases(D).loc[mc, "t"]).dt.total_seconds().abs()
    ok((skew > 86400).sum() >= 100, "R2 the device clocks run days out on %d events" % (skew > 86400).sum())

    # ------------------------------------------------------------ separation: the asks' columns move no alert
    rng = np.random.default_rng(11)
    va = v.assign(account_id=rng.permutation(v.account_id.values), price_minor=rng.permutation(v.price_minor.values),
                  currency=rng.permutation(v.currency.values))
    sa = D["ses"].assign(account_id=rng.permutation(D["ses"].account_id.values))
    D2 = dict(D, val=va, ses=sa, links=D["links"].iloc[:0], rates=D["rates"].iloc[:0])
    l2 = E.loss(E.conform(D2))
    ok(all(abs(l2[b] - G[b]) < 1e-12 for b in E.ORDER),
       "separation: accounts, prices and currencies scrambled, the links and the rates dropped: every build's loss unchanged")

    # ------------------------------------------------------------ ask A: paying players and its stops
    pl = X["players"]
    truth = {b: g.player.nunique() for b, g in tb.items()}
    ok(all(pl["golden"][b] == truth[b] for b in E.ORDER), "ask A fair: the golden equals each build's players in the world")
    for how, lo in (("chain", 3), ("one_hop", 3), ("account", 6)):
        ok(all(pl[how][b] - pl["golden"][b] >= lo for b in E.ORDER),
           "ask A stop: %s reads every build %d or more high" % (how, lo))
    ok(sum(pl["chain"][b] != pl["one_hop"][b] for b in E.ORDER) >= 8, "ask A: one hop and the whole chain differ on most builds")
    with_ev = E.players(D, with_events=True)
    ok(all(p[p.build == b].account_id.map(with_ev).nunique() == pl["golden"][b] for b in E.ORDER),
       "ask A: the warehouse's events beside the validations and the sessions join the same guests")
    st = E.signed_in_to(D)
    linked = set(D["links"][D["links"].link_type == "guest_upgrade"].from_account_id)
    ok(sum(1 for g in st if g not in linked) >= 300, "ask A device: %d guest sign-ins with no link" % sum(1 for g in st if g not in linked))
    ok(all((pl["testers_in"][b] - pl["golden"][b] >= 5) == (b in TESTED) for b in E.ORDER),
       "ask A hazard: testers kept move exactly the six builds they bought on")
    ok(sum(pl["refunded_out"][b] < pl["golden"][b] for b in E.ORDER) >= 10, "ask A hazard: refunded purchases dropped move 10 or more builds")

    # ------------------------------------------------------------ ask B: gross bookings per paying player and its stops
    bk = X["bookings"]
    pp = X["per_player"]
    rates = D["rates"].assign(date=pd.to_datetime(D["rates"].date).dt.date)
    days = sorted(rates.date.unique())
    tab = rates.pivot(index="date", columns="currency", values="rate")
    true_eur = {}
    for b, g in tb.items():
        tot = 0.0
        for r in g.itertuples():
            local, cur = R._price(r.product, R.country[r.account])
            x = local if cur == "EUR" else local / tab.loc[[d for d in days if d <= r.day][-1], cur]
            tot += round(x + 1e-9, 2)
        true_eur[b] = round(tot, 2)
    ok(all(abs(true_eur[b] - bk["golden"][b]) < 0.005 for b in E.ORDER),
       "ask B fair: each price at its currency's exponent reproduces the bookings from the world's own prices")
    tp = E.per_player({b: true_eur[b] for b in E.ORDER}, truth)
    ok(all(tp[b] == pp["golden"][b] for b in E.ORDER), "ask B fair: the world's bookings over its players give the golden")
    ok(all(pp["golden"][b] - pp["all2"][b] >= 0.5 for b in E.ORDER), "ask B stop: every price over 100 reads every build 0.50 euro or more low")
    for how in ("chain", "one_hop", "account"):
        ok(all(pp["golden"][b] - pp[how][b] >= 0.05 for b in E.ORDER),
           "ask B stop: the paying players of A's %s route read every build 0.05 euro or more low" % how)
    ok(all((pp["testers_in"][b] != pp["golden"][b]) == (b in TESTED) for b in E.ORDER),
       "ask B hazard: testers kept move exactly the six builds they bought on")
    ok(sum(pp["refunds_netted"][b] < pp["golden"][b] for b in E.ORDER) >= 10, "ask B hazard: refunds netted move 10 or more builds")
    ok(all(pp["next"][b] == pp["golden"][b] and pp["unrounded"][b] == pp["golden"][b] for b in E.ORDER),
       "ask B: the next rate at weekends and the total summed before rounding cancel at a player's cent")
    jk = v[v.currency.isin(["JPY", "KRW"]) & (v.transaction_kind == "purchase")]
    ok((jk.price_minor.astype(int) >= 100).all() and (jk.price_minor.astype(int) % 10 == 0).all(),
       "ask B: yen and won prices are whole store price points")

    # ------------------------------------------------------------ the documents
    for phrase, sf in (("purchase type standard", "SF2"), ("A refunded purchase remains a purchase", "SF2"),
                       ("the validation's app_build", "SF4"), ("Irish date (Europe/Dublin) of its purchased_at", "SF5"),
                       ("the rows are one event", "SF3"), ("lost only if it never will", "SF6"),
                       ("above 2 per cent, compared unrounded", "SF7"), ("every build in production in the build register", "SF11"),
                       ("a guest account is the same player as the account it signs in to", "ask A"),
                       ("divided by its paying players, to the cent", "ask B"), ("and so on through any chain", "ask A")):
        ok(phrase in cat, "%s pinned in KC-DQ-04: %s" % (sf, phrase))
    ok(not re.search(r"session|settle|seven days|matur|lag|next time|queue|phone", cat, re.I),
       "KC-DQ-04 names no way of telling a lost event from a late one")
    ok("next session" not in sdk and not re.search(r"lost|missing|loss", sdk, re.I),
       "the SDK notes link no missing event to a session and say nothing of loss")
    ok("history moved to the account it signed in to" in dic and "gst_" in dic,
       "the dictionary describes guest_upgrade as history that moved, and guest accounts by prefix")
    ok("not a register of every account a player has used" in dic and "until the player signs in on it" in dic,
       "the links file says it is no full register, and the session log's account changes when the player signs in")
    ok(not re.search(r"older account|account made before|no link|not linked", dic + cat, re.I),
       "no document says a sign-in to an older account leaves no link")

    # ------------------------------------------------------------ R3c, input gates, dates
    names = os.listdir(target)
    ok(len(names) >= 10 and len({f.rsplit(".", 1)[1] for f in names}) >= 3, "input gates: %d files, formats %s"
       % (len(names), sorted({f.rsplit(".", 1)[1] for f in names})))
    ok(max(sum(1 for _ in open(os.path.join(target, f))) for f in names if f.endswith(".csv")) >= 25_001,
       "input gate: a file of 25,000 rows or more")
    run_iso = "2026-11-09T07:00:00.000Z"
    ok(v.purchased_at.max() < run_iso and v.validated_at.max() < run_iso, "no validation after the run")
    ok(e.received_at.max() < run_iso and D["ses"].started_at.max() < run_iso, "no event or session after the run")
    ok(D["links"].linked_at.max() < run_iso, "no link after the run")
    ok(str(D["rates"].date.max()) == "2026-11-06" and pd.to_datetime(D["rates"].date).dt.weekday.max() < 5,
       "ECB rates on working days to Friday 6 November")
    for f in ("crash", "ratings", "push"):
        ok(os.path.exists(files[f]), "distractor %s ships; the golden and both asks read none of it" % f)
    sub = os.path.join(os.path.dirname(target), "submission.md")
    for path in (sub, os.path.join(os.path.dirname(target), "DESIGN_NOTE.md"), os.path.join(os.path.dirname(target), "prompt.txt")):
        if os.path.exists(path):
            ok("—" not in open(path).read(), "no em dash in %s" % os.path.basename(path))
    for f in names:
        if f.endswith((".md", ".csv")):
            ok("—" not in open(os.path.join(target, f)).read(), "no em dash in %s" % f)

    # ------------------------------------------------------------ realism sweep
    for k in ("val", "evt", "ses", "links", "rates"):
        df = D[k]
        const = [c for c in df.columns if df[c].nunique() == 1 and c != "event_name"]
        ok(not const, "realism: no constant column in %s" % os.path.basename(files[k]))
    daily = E.utc(D["ses"].started_at).dt.date.value_counts().sort_index().values
    ok(len(set(daily)) == len(daily), "realism: no two days with the same number of session starts")
    pdays = p.groupby(["build", "day"]).size()
    runs = sum(1 for _, s in pdays.groupby(level=0) for i in range(len(s) - 2) if s.iloc[i] == s.iloc[i + 1] == s.iloc[i + 2])
    ok(runs <= 3, "realism: a build's daily purchases repeat three days running %d times" % runs)
    ok(len(p) % 100 and sum(pl["golden"].values()) % 100 and round(sum(bk["golden"].values())) % 100,
       "realism: no round headline total (%d purchases, %d paying players, %.2f euro)"
       % (len(p), sum(pl["golden"].values()), sum(bk["golden"].values())))
    ok(D["ses"].session_id.is_unique and e.event_id.nunique() > 19_000, "realism: session ids unique; event ids by the thousand")
    card = json.load(open(os.path.join(REPO, ".claude", "skills", "fingerprint", "cards", "task235.json")))
    ok(set(P.PEOPLE.values()) == set(card["world"]["people"]), "realism: every persona drawn by guard.py names")
    scrub = os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
    for folder in (target, golden):
        out = subprocess.run([sys.executable, scrub, folder], capture_output=True, text=True).stdout
        ok("clean, no producer signature" in out, "realism: containers scrubbed in %s" % os.path.basename(folder))
    return N[0]


def _pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path).pages)
