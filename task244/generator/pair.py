"""task244 pair measurement on the cut pack. The cracker lands the call and takes the asks the way the files document
them: the match rate with section 8.2's link (dwelling, household and line, or a new household's sex and month and year
of birth) over the records with identical rows taken once, and the reinterview's days to the call's date as the
fieldwork log records it, every other handling right (the districts as from 1 April 2027, each person's own
interview, the late reinterviews in). The
mirror stops at a wrong rung on the call and takes the asks by whichever path keeps it the most figures among the
cracker's and five lazier ones. Every ask figure is scored against the golden at its rounding. Prints the cracker sheet,
the mirror's leakage and the pair ceiling; --ladder prints the design note's ladder figures and the grid of routes,
--asks the ask sheet's stops, devices and hazards.

    python3 task244/generator/pair.py [target]
    python3 task244/generator/pair.py --ladder [target]
    python3 task244/generator/pair.py --asks [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import estim as E
import params as P
import solve

TARGET = os.path.join(os.path.dirname(HERE), "target")


def ask_paths(target):
    F = B.FILES
    exact = solve.persons(target, F, dedupe="exact")
    raw = solve.persons(target, F, dedupe="none")
    filed = solve.ask_match(target, F, exact)
    sync = solve.ask_days(target, F, exact, date="attempt_date")
    return {
        "cracker": (filed, sync),
        "rows as received": (solve.ask_match(target, F, raw), solve.ask_days(target, F, raw, date="attempt_date")),
        "recorded district codes": (solve.ask_match(target, F, exact, district="district"),
                                    solve.ask_days(target, F, exact, date="attempt_date", district="district")),
        "household's first interview": (filed, solve.ask_days(target, F, exact, date="attempt_date", anchor="household")),
        "late reinterviews left out": (filed, solve.ask_days(target, F, exact, date="attempt_date", late=False)),
        "line key alone": (solve.ask_match(target, F, exact, key="line"), sync),
    }


def score(target, paths):
    F = B.FILES
    df = solve.persons(target, F)
    gm, gd = solve.ask_match(target, F, df), solve.ask_days(target, F, df)
    n = 3 * len(P.DCODES)
    keep = {}
    for k, (m, d) in paths.items():
        hits = ["base " + c for c in P.DCODES if m[c][2] == gm[c][2]] + \
               ["rate " + c for c in P.DCODES if round(m[c][1], 1) == round(gm[c][1], 1)] + \
               ["days " + c for c in P.DCODES if round(d[c][1], 1) == round(gd[c][1], 1)]
        keep[k] = len(hits) / n
        print("%-28s keeps %2d of %d ask figures %s" % (k, len(hits), n, hits))
    return keep


def mirror_on_call(target):
    """the share of the call's per-rate criteria (the warning and the share at its rounding) a response stopping at each
    wrong rung keeps"""
    A = solve.answer(target, B.FILES)
    V, _ = solve.rungs(target, B.FILES, A)
    gold, sh = A["warned"], A["shares"]
    best = (None, 0.0)
    for k in ["R0 predictive values multiplied", "R1 correct readings multiplied", "R1 predictive values by district",
              "R2 rate overstatement (net)", "R2 flow excess (net)"]:
        w = E.warned(V[k])
        right = sum((x in w) == (x in gold) for x in sh)
        same = sum(round(100 * V[k][x], 1) == round(100 * sh[x], 1) for x in sh)
        share = (right + same) / 48.0
        print("mirror at %-34s warns %2d; %2d of 24 warnings right, %2d of 24 shares right" % (k, len(w), right, same))
        if share > best[1]:
            best = (k, share)
    return best


def ladder(target):
    A = solve.answer(target, B.FILES)
    V, _ = solve.rungs(target, B.FILES, A)
    gold = A["warned"]
    for k, v in V.items():
        w = E.warned(v)
        print("%-34s warns %2d, same as the golden: %-5s shares %.1f to %.1f per cent, nearest the line %.1f points" % (
            k, len(w), w == gold, 100 * min(v.values()), 100 * max(v.values()),
            100 * min(abs(x - P.WARN_SHARE) for x in v.values())))
    print("golden: warns %d, shares %.1f to %.1f, nearest the line %.1f points" % (
        len(gold), 100 * min(A["shares"].values()), 100 * max(A["shares"].values()),
        100 * min(abs(x - P.WARN_SHARE) for x in A["shares"].values())))


def grid(target):
    """the method by the error's truth by its scope by the reading, every cell's warned rates against the golden's and
    how many of the 24 printed shares it keeps"""
    import itertools
    F = B.FILES
    A = solve.answer(target, F)
    O, gold, gs = A["O"], A["warned"], A["shares"]
    _, X = solve.rungs(target, F, A)
    r, wt = X["r"], X["wt"]
    t = (r.reconciled - 1).values
    o = (r.orig_status - 1).values
    u = (r.reint_status - 1).values
    for (tn, tr), scope, method, reading in itertools.product(
            (("reconciled", t), ("supervisor's own", u)), ("state", "district"), ("predictive", "correct", "inversion"),
            ("gross", "net")):
        if method != "inversion" and reading == "net":
            continue
        sh = {}
        for d in P.DCODES:
            C = E.table(tr, o) if scope == "state" else E.table(tr[wt.d27.values == d], o[wt.d27.values == d])
            M = E.misread(C)
            for a, b in E.CELLS:
                if method == "predictive":
                    v = E.not_real_ppv(C, a, b)
                elif method == "correct":
                    v = E.not_real_both_right(M, a, b)
                elif reading == "gross":
                    v = E.not_real(O[d], M, a, b)
                else:
                    v = E.not_real_net(O[d], M, a, b)
                sh[(d, a + b)] = v
        w = E.warned(sh)
        same = sum(round(100 * sh[k], 1) == round(100 * gs[k], 1) for k in gs)
        print("%-17s %-8s %-10s %-5s warns %2d, %-16s largest share %.1f, %2d of 24 shares the golden's" % (
            tn, scope, method, reading, len(w), "the golden's" if w == gold else "%d differ" % len(set(w) ^ set(gold)),
            100 * max(sh.values()), same))


def asks(target):
    """the ask sheet's figures: each stop's deltas against the golden, the device and hazard counts"""
    import datetime as dt
    import pandas as pd
    F = B.FILES
    df = solve.persons(target, F)
    ex = solve.persons(target, F, dedupe="exact")
    raw = solve.persons(target, F, dedupe="none")
    g = solve.ask_match(target, F, df)
    copies = ex[ex.duplicated([c for c in ex.columns if c not in ("hh", "d27", "qi")])]
    due = copies[copies.visit <= 3].groupby("d27").size()
    print("A records taken in again: %d, due another visit %d to %d a district" % (len(copies), due.min(), due.max()))
    for name, x in (("filed link, identical rows once (cracker)", solve.ask_match(target, F, ex)),
                    ("rows as received", solve.ask_match(target, F, raw)),
                    ("line key alone", solve.ask_match(target, F, df, key="line")),
                    ("recorded district codes", solve.ask_match(target, F, df, district="district"))):
        db = [x[d][2] - g[d][2] for d in P.DCODES]
        dr = [x[d][1] - g[d][1] for d in P.DCODES]
        moved = sum(x[d][2] != g[d][2] or round(x[d][1], 1) != round(g[d][1], 1) for d in P.DCODES)
        print("A %-42s base %+d to %+d, rate %+.2f to %+.2f, %d districts moved" % (name, min(db), max(db), min(dr),
                                                                                  max(dr), moved))
    rr, cr = solve.ask_match(target, F, raw), solve.ask_match(target, F, ex)
    print("A the batch received twice kept, Market Towns base %+d" % (rr["D11"][2] - cr["D11"][2]))
    line = solve.ask_match(target, F, df, key="line")
    print("A members of split households the line key misses: %d" % sum(g[d][0] - line[d][0] for d in P.DCODES))
    print("A records under the Industrial Corridor's codes in the moved areas before 1 April 2027: %d" % int(
        ((raw.district == "D04") & raw.ea.isin([3, 7, 9, 12, 14, 15]) & raw.quarter.isin(P.QUARTERS[:2])).sum()))
    gd = solve.ask_days(target, F, df)
    for name, x in (("the call's date as recorded (cracker)", solve.ask_days(target, F, df, date="attempt_date")),
                    ("the household's first interview", solve.ask_days(target, F, df, anchor="household")),
                    ("late reinterviews left out", solve.ask_days(target, F, df, late=False)),
                    ("2026Q4 kept", solve.ask_days(target, F, df, quarters=P.QUARTERS))):
        dd = [x[d][1] - gd[d][1] for d in P.DCODES]
        moved = sum(round(x[d][1], 1) != round(gd[d][1], 1) for d in P.DCODES)
        print("B %-42s days %+.2f to %+.2f, %d districts moved" % (name, min(dd), max(dd), moved))
    log = pd.read_csv(os.path.join(target, F["reint_log"]), dtype={"dwelling": str})
    ad = log.attempt_date.map(dt.date.fromisoformat)
    vd = log.visit_start.str[:10].map(dt.date.fromisoformat)
    after = vd >= log.supervisor.map(P.APP_UPDATE)
    print("B calls %d: dates agree on %d of %d before each tablet's update, on %d of %d after" % (
        len(log), int((ad[~after] == vd[~after]).sum()), int((~after).sum()), int((ad[after] == vd[after]).sum()),
        int(after.sum())))
    r = pd.read_csv(os.path.join(target, F["reint_results"]), dtype={"dwelling": str})
    done = log[log.result == "completed"].assign(vd=vd, ad=ad)
    rr2 = r.merge(df[["quarter", "dwelling", "hh", "line", "int_date"]], on=["quarter", "dwelling", "hh", "line"])
    rr2 = rr2.merge(done[["quarter", "dwelling", "hh", "vd", "ad"]], on=["quarter", "dwelling", "hh"])
    iday = rr2.int_date.map(dt.date.fromisoformat)
    out_call = sum((a - i).days > P.REINT_WINDOW for a, i in zip(rr2.ad, iday))
    out_visit = sum((v - i).days > P.REINT_WINDOW for v, i in zip(rr2.vd, iday))
    print("B results outside the 14-day window: %d by the call's date as recorded, %d by visit_start" % (out_call,
                                                                                                         out_visit))


def main(target=TARGET):
    keep = score(target, ask_paths(target))
    rung, share = mirror_on_call(target)
    r_miss = round(38 * 0.75 * share, 1)
    print("the best wrong rung on the call: %s, keeping %.1f of the 38 recommendation points" % (rung, r_miss))
    lc = keep["cracker"]
    ls = max(keep.values())
    c, s = 38 + 7 + 55 * lc, r_miss + 7 + 55 * ls
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return (c + s) / 2, 100 * ls


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    t = args[0] if args else TARGET
    if "--ladder" in sys.argv:
        ladder(t)
        grid(t)
    elif "--asks" in sys.argv:
        asks(t)
    else:
        main(t)
