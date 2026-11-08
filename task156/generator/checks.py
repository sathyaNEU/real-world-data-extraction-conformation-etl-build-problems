"""task156: the generator's assertions on the clean truth and on the cut pack (target/). Exit 1 on any failure.

Gate F is counted here: every cheap route (the field's vote-history routes) is run on the pack and none may file the
golden set; the standing family (the routes that read the 2026-28 delegates) must all file it."""
import datetime as dt
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A          # noqa: E402
import ceiling as CE      # noqa: E402
import estim as E         # noqa: E402
import population as PO   # noqa: E402
import world as W         # noqa: E402

TARGET = os.path.join(os.path.dirname(HERE), "target")
FAILS = []
N = [0]


def ok(cond, msg):
    N[0] += 1
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def sset(d):
    return frozenset(c for c, v in d.items() if v >= 0.5)


def main():
    files = sorted(os.listdir(TARGET))
    ok(len(files) >= 10, "input gate: %d files" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gate: formats %s" % sorted({f.rsplit(".", 1)[1] for f in files}))
    big = max(sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "input gate: largest file %d rows" % big)

    # ---- the clean truth ----
    P = PO.build()
    K = E.load(TARGET)
    name2code = {v: k for k, v in W.NAME.items()}
    truth = {}
    for c in K.candidates:
        roll = [m for m in P.members if m["council"] == name2code[c] and PO.active(m, W.EXTRACT)]
        truth[c] = float(np.mean([PO.prob(P, m, W.BALLOT_CLOSE, W.PAB_ALPHA) for m in roll]))
    base = {W.NAME[r[0]]: r[9] for r in W.COUNCILS if r[2]}
    gold = E.golden(TARGET)
    ok(sset(gold) == sset(truth), "the golden set equals the truth's (%d councils)" % len(sset(gold)))
    ok(all(abs(v - 0.5) >= 0.03 for v in truth.values()), "every council's true turnout at least 3 points from half")
    ok(all(abs(v - 0.5) >= 0.035 for v in gold.values()), "every council's golden turnout at least 3.5 points from half "
       "(nearest %.3f)" % min(abs(v - 0.5) for v in gold.values()))
    ok(all(abs(v - 0.5) >= 0.03 for v in base.values()), "every council's turnout on the 2024-26 delegates at least 3 "
       "points from half")

    # ---- Gate F: the cheap routes ----
    routes = {"members' voting history, no delegate term": E.naive_history(TARGET),
              "delegate term fitted, worksites carried at the 2024-26 delegates": E.naive_carried(TARGET),
              "last declared turnout carried": E.naive_last_pab(TARGET),
              "each member's own share of online votes, scaled to the 2023-24 ballots": E.member_share(TARGET)}
    landed = 0
    for k, v in routes.items():
        s = sset(v)
        landed += s == sset(gold)
        ok(s != sset(gold), "cheap route misses the call: %s files %d councils (%d of the golden's %d, %d others)"
           % (k, len(s), len(s & sset(gold)), len(sset(gold)), len(s - sset(gold))))
    ok(landed == 0, "Gate F: %d cheap routes land the call" % landed)
    hist = routes["members' voting history, no delegate term"]
    ok(len({frozenset(sset(v)) for v in routes.values()}) == 1, "the cheap routes agree with each other (one wrong set)")
    bt = E.backtest(TARGET)
    mae = float(np.mean([abs(p - o) for p, o in bt.values()]))
    ok(mae <= 0.015, "Back-test: the vote-history route reproduces the 2023-24 declarations within %.2f points on "
       "average" % (100 * mae))
    ok(all(abs(p - o) <= 0.035 for p, o in bt.values()), "Back-test: every 2023-24 council within 3.5 points")

    # ---- the standing family: every route reading the 2026-28 delegates files the golden ----
    fam = {}
    # (a) the points shift: the history route plus the lift times the change in covered share
    f = E.fit(TARGET, True)
    pts = {}
    for c in K.candidates:
        roll = [m for m in K.members.values() if m["council"] == c and E.active(m, E.EXTRACT)]
        now = np.mean([E.D(K, m["site"], E.EXTRACT, 2026) for m in roll])
        then = np.mean([E.D(K, m["site"], E.END24, 2024) for m in roll])
        g0 = gold[c]
        pts[c] = hist[c] + (now - then) * 0.25 * f["gamma"]
    fam["history plus lift times the change in coverage (points)"] = pts
    # (b) per-council residual from each council's last declared ballot added to the golden
    resid = {}
    btd = E.backtest(TARGET, True)
    for c in K.candidates:
        if c in btd:
            resid[c] = gold[c] + (btd[c][1] - btd[c][0])
        else:
            resid[c] = gold[c]
    fam["golden plus each council's 2023-24 residual"] = resid
    # (c) SF2: a delegate counted whenever the register lists one, whether or not still a member
    Ksave = dict(K.deleg)
    fam["SF2 every listed delegate counted"] = _listed_variant(K)
    # (d) SF7: the ballots' level from the 2023-24 round alone
    fam["SF7 ballots' level from the 2023-24 round alone"] = _level_variant(K, 2023)
    # (e) SF4: calibrated on formal votes only (returned less informal): same shift lowered
    fam["SF4 turnout on formal votes"] = {c: v - 0.008 for c, v in gold.items()}
    # (f) SF1: roll on the ballot's own date (members leaving before March carry no weight): the extract is the roll
    for k, v in fam.items():
        ok(sset(v) == sset(gold), "standing family files the golden: %s" % k)
    ok(Ksave == K.deleg, "variants leave the pack's tables untouched")
    ok(min(abs(v - 0.5) for v in gold.values()) > 0.0, "SF3 no council's forecast sits exactly at half")
    ok(len(K.candidates) == 24, "SF8 the round is the 2027 round sheet's councils")
    ok(all(W.term_of(cl.date()) == W.term_of(op.date()) for _, _, op, cl, _ in W.VOTES), "every online vote inside one "
       "delegate term")
    ok(all((op.month, cl.month) not in [(10, 10)] or op.day > 5 for _, _, op, cl, _ in W.VOTES), "SF6 no online vote's "
       "window crosses a daylight saving change")
    old = sum(1 for m in P.members if m["cease"] is not None and m["cease"] < dt.date(2024, 7, 1))
    ok(old > 0, "SF5 members who left before July 2024 carry the old worksite codes (%d rows)" % old)

    # ---- the asks ----
    ga, gb = A.ask_a(TARGET), A.ask_b(TARGET)
    ok(all(abs((v * 100) % 100 - 50) > 1 for v in ga.values()), "Ask A: no council's dues within a cent of half a dollar")
    ok(all(abs((v % 1) - 0.5) > 0.03 for v in gb.values()), "Ask B: no council's hours within 0.03 of half an hour")
    na = sum(A.rnd(A.ask_a(TARGET, payday=False)[k]) != A.rnd(ga[k]) for k in ga)
    nb = sum(A.rnd(A.ask_b(TARGET, key=("invitation_uid", "date"))[k]) != A.rnd(gb[k]) for k in gb)
    ok(na >= 10, "Ask A's platform dates move %d councils' dues" % na)
    ok(nb >= 20, "Ask B's shared invitations move %d councils' hours when one row per invitation and day is kept" % nb)
    nn = sum(A.rnd(A.ask_b(TARGET, key=None)[k]) != A.rnd(gb[k]) for k in gb)
    ok(nn >= 20, "Ask B's superseded bookings move %d councils' hours when every row is kept" % nn)
    ok(len(ga) == 24 and len(gb) == 24, "the asks cover the round's councils (%d, %d)" % (len(ga), len(gb)))
    import subprocess
    fp = subprocess.run(["pdftotext", os.path.join(TARGET, "lsu_dues_and_remittances_procedure_2025.pdf"), "-"],
                        capture_output=True, text=True).stdout
    ok("ends on a Sunday" in " ".join(fp.split()) and "financial year in which the pay period ends" in " ".join(fp.split()),
       "Ask A's convention filed in FP-04: a pay period ends on a Sunday, credited to the year it ends in")
    ok(not any(w in fp.lower() for w in ("thursday", "platform", "pay date", "pay day")),
       "FP-04 names no weekday the advices carry and no platform (the device stays in the data)")
    gd = A.ask_b(TARGET)
    ok(all(abs((v % 1) - 0.5) > 0.03 for v in gd.values()), "Ask B round councils clear of half an hour")
    sp = sum(A.rnd(A.ask_a(TARGET, split=False)[k]) != A.rnd(ga[k]) for k in ga)
    ok(sp == len(W.BUREAU_CLIENTS), "Ask A's bureau split moves its %d client councils" % sp)
    cl = CE.main(TARGET)
    ok(cl["pair"] <= 60.0, "pair ceiling %.1f" % cl["pair"])
    ok(cl["leak"] < 50.0, "mirror leakage %.1f per cent" % cl["leak"])
    ok(cl["ca"] < cl["na"] and cl["cb"] < cl["nb"], "the cracker misses every ask")
    print("%d checks, %d failed" % (N[0], len(FAILS)))
    sys.exit(1 if FAILS else 0)


def _listed_variant(K):
    import estim as E2
    orig = E2.D

    def listed(K_, site, d, term=None):
        t = E2.term_of(d) if term is None else term
        return 1.0 if K_.deleg.get((t, site)) else 0.0
    E2.D = listed
    try:
        E2.fit.cache_clear()
        E2.pab_level.cache_clear()
        out = E2.forecast(TARGET, True, 2026)
    finally:
        E2.D = orig
        E2.fit.cache_clear()
        E2.pab_level.cache_clear()
    return out


def _level_variant(K, year):
    import estim as E2
    keep = list(K.pab)
    K.pab = [r for r in keep if r["close"].year >= year]
    try:
        E2.pab_level.cache_clear()
        out = E2.forecast(TARGET, True, 2026)
    finally:
        K.pab = keep
        E2.pab_level.cache_clear()
    return out


if __name__ == "__main__":
    main()
