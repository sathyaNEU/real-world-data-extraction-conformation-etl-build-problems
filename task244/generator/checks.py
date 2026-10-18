"""task244 generator checks, run by make.py on the built pack: the three rules on the simulator's clean truth (R1 to
R3c), the call and its rungs, every row of the design note's semantic fork table (SF1 to SF16), the asks' devices and
stops, every graded figure's distance to its rounding edge, the realism sweep and the input gates."""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import build as B
import estim as E
import params as P
import sim
import solve

S = P.STATUS
GOLD = [("D03", "EU"), ("D04", "UE"), ("D05", "EU"), ("D05", "UE"), ("D06", "EU"), ("D06", "UE"), ("D07", "EU"),
        ("D07", "UE"), ("D08", "EU"), ("D08", "UE"), ("D09", "EU"), ("D10", "UE"), ("D12", "EU")]


class Count:
    n = 0


def ok(cond, what):
    assert cond, what
    Count.n += 1


def edge(v, u=0.1):
    """the distance from a printed figure's value to the nearer edge of its rounding cell"""
    return u / 2 - abs(v - round(v / u) * u)


def clean_truth(W):
    """the call on the simulator's clean truth: each district's true flows without sampling or reading error, the
    original interview's classification error as drawn, the counted flows they make"""
    gold, ppv, both, ppvd = {}, {}, {}, {}
    pooled = sum(sim.clean_flows(W, d) for d in P.DCODES) / len(P.DCODES)
    v = E.stocks_ppv(pooled, W.M)
    for d in P.DCODES:
        Ft = sim.clean_flows(W, d)
        Ot = W.M.T @ Ft @ W.M
        vd = E.stocks_ppv(Ft, W.M)
        for a, b in E.CELLS:
            i, j = S.index(a), S.index(b)
            gold[(d, a + b)] = E.not_real(Ot, W.M, a, b)
            ppv[(d, a + b)] = 1 - v[i] * v[j]
            ppvd[(d, a + b)] = 1 - vd[i] * vd[j]
            both[(d, a + b)] = E.not_real_both_right(W.M, a, b)
    return gold, ppv, both, ppvd


def run(target, W, R, fig, golden):
    F = B.FILES
    A = solve.answer(target, F)
    gold = A["warned"]
    ok(gold == GOLD, ("the call", gold))
    names = {(c["district"], c["key"]): c for c in fig["cells"]}
    ok(len(gold) == fig["call"]["count"] and all(names[k]["warning"] for k in gold), "the call matches figures.json")

    # ---------------------------------------------------------------- R1: the field's raw material ships
    wb = load_workbook(os.path.join(target, F["flows"]), read_only=True)
    ok(wb.sheetnames == ["F1 flows", "F2 rates"], "R1 the flows tables ship as published, two sheets")
    ok(all(A["O"][d].shape == (3, 3) and (A["O"][d] > 0).all() for d in P.DCODES),
       "R1 every district's nine flows between the three statuses ship")
    r = pd.read_csv(os.path.join(target, F["reint_results"]), dtype={"dwelling": str})
    ok({"orig_status", "reint_status", "reconciled"} <= set(r.columns), "R1 the reinterview ships person by person")
    cols = " ".join(pd.read_csv(os.path.join(target, f), nrows=1).columns.str.lower().str.cat(sep=" ")
                    for f in [F[k] for k in F if F[k].endswith(".csv")])
    ok(not re.search(r"share|warn|real|true|flag", cols), "R1 no shipped column holds the deciding quantity")

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    tg, tp, tb, tpd = clean_truth(W)
    ok(E.warned(tp) == [], "R3a the default path (predictive values multiplied) on the clean truth warns none")
    ok(E.warned(tb) == [], "R3a the correct readings multiplied on the clean truth warns none")
    ok(E.warned(tpd) == [], "R3a the predictive values of each district's own stocks on the clean truth warn none")
    ok(E.warned(tg) == gold, "R3b the decisive step alone (the error out at both quarters) on the clean truth gives the "
                             "golden's rates")
    ok(min(abs(v - P.WARN_SHARE) for v in tg.values()) >= 0.08, "R3b the clean truth clears the line by 8 points")

    # ---------------------------------------------------------------- the call, its margins and its rungs
    sh = A["shares"]
    ok(min(abs(v - P.WARN_SHARE) for v in sh.values()) >= 0.08, "the call: every rate 8 points or more from the line")
    Fd = {d: E.true_flows(A["O"][d], A["M"]) for d in P.DCODES}
    ok(all((Fd[d] > 0).all() for d in P.DCODES), "the true flows are positive in every district (the inversion is the "
                                                 "maximum likelihood)")
    V, X = solve.rungs(target, F, A)
    rungs = {k: E.warned(v) for k, v in V.items()}
    ok(rungs["R0 predictive values multiplied"] == [], "R0 warns none")
    ok(rungs["R1 correct readings multiplied"] == [], "R1 warns none")
    ok(rungs["R1 predictive values by district"] == [], "R1 by district warns none")
    p0 = V["R0 predictive values multiplied"]
    ok(len({round(v, 12) for v in p0.values()}) == 1, "R0 puts every rate at one share")
    ok(abs(round(100 * list(p0.values())[0], 1) - fig["rungs"]["ppv_statewide"]) < 1e-9, "R0's figure in figures.json")
    p1 = V["R1 correct readings multiplied"]
    ok(abs(round(100 * list(p1.values())[0], 1) - fig["rungs"]["both_right"]) < 1e-9, "R1's figure in figures.json")
    # the clean data test: the easy route and the answer stay apart on the pack and on the truth
    ok(max(p0.values()) < P.WARN_SHARE - 0.1 and max(tp.values()) < P.WARN_SHARE - 0.1,
       "the default path stays 10 points under the line on the pack and on the truth")

    # ---------------------------------------------------------------- the semantic fork table
    net = rungs["R2 rate overstatement (net)"]
    ok(sorted(set(net) ^ set(gold)) == [("D06", "UE")], "SF1 the rate's overstatement (net) drops Cocoa Belt West's "
                                                        "job-finding rate (ruled out by section 8.1's persons counted)")
    ok(rungs["R2 flow excess (net)"] == gold, "SF1 the counted flow's excess over the true flow gives the same rates")
    mu = V["M unreconciled"]
    ok(sorted(set(rungs["M unreconciled"]) ^ set(gold)) == [("D10", "EU")] and max(mu.values()) > 1.0,
       "SF2 the supervisor's own reading as the truth adds the Creeks' job-loss rate and a share above one (ruled out by "
       "section 8.1's reconciled status)")
    ok(rungs["M 2027Q1 to 2027Q4"] == gold, "SF3 the 2027 quarters' reinterviews alone give the same rates")
    ok(rungs["M weighted"] == gold, "SF4 the reinterview weighted gives the same rates")
    ok(sorted(set(rungs["M by district"]) ^ set(gold)) == [("D12", "EU")],
       "SF5 the error by district drops the University Towns' job-loss rate (ruled out by protocol section 7)")
    ok(rungs["flows rebuilt, bureau key"] == gold, "SF6 the flows rebuilt from the person files on the cross-sectional "
                                                    "weights give the same rates")
    ok(rungs["flows rebuilt, every person"] == gold, "SF7 the flows rebuilt on every person interviewed again give the "
                                                      "same rates")
    f2 = pd.read_excel(os.path.join(target, F["flows"]), sheet_name="F2 rates", header=2)
    for row in f2.itertuples():
        d = row.Code
        ok(abs(round(100 * A["published"][(d, "UE")], 1) - row._3) < 1e-9 and
           abs(round(100 * A["published"][(d, "EU")], 1) - row._4) < 1e-9,
           "SF8 Table F2's rates are Table F1's flows over the first status (%s)" % d)
    ok(len(sh) == 24 and {k[1] for k in sh} == {"UE", "EU"}, "SF9 the 24 rates: each district's job-finding and job-loss")
    ok(all((v >= P.WARN_SHARE) == (round(100 * v, 1) >= 33.3) for v in sh.values()),
       "SF10 a third or more: the unrounded share and the printed share give the same warnings")
    ok(len(gold) == len(E.warned({k: v - 0.05 for k, v in sh.items()})) == len(E.warned({k: v + 0.05 for k, v in sh.items()})),
       "SF10 a line five points either side warns the same rates")
    rs = X["wt"]
    ok((rs.lfs_status.values == rs.orig_status.values).all(), "SF11 the reinterview's original status is the person "
                                                              "file's status")
    gz = pd.read_csv(os.path.join(target, F["gazetteer"]))
    ok(int((gz.effective.fillna("") == P.BOUNDARY_DATE.isoformat()).sum()) == len(P.MOVED_EAS),
       "SF12 the gazetteer lists the six areas moved on 1 April 2027")
    ok(set(f2.Code) == set(P.DCODES), "SF12 the tables are on the twelve districts as from 1 April 2027")
    ok(int(A["C"].sum()) == len(r) == fig["reinterview"]["persons"], "SF13 each person reinterviewed counts once")
    ok(r.drop_duplicates(["quarter", "dwelling", "hh", "line"]).shape[0] == len(r), "SF13 no person twice in a quarter")
    O1 = {d: np.round(R.flows()[d]) for d in P.DCODES}
    ok(all((O1[d] == A["O"][d]).all() for d in P.DCODES), "SF14 Table F1 as read is the bureau's rounded flows")
    raw = {(d, a + b): E.not_real(R.flows()[d], A["M"], a, b) for d in P.DCODES for a, b in E.CELLS}
    ok(E.warned(raw) == gold and max(abs(raw[k] - sh[k]) for k in sh) < 0.002,
       "SF14 the unrounded flows give the same rates, every share within 0.2 points")
    ok(fig["constants"]["pairs"] == 4, "SF15 the average of the four quarter pairs")
    per_pair = {}
    df = X["df"]
    for qi in range(4):
        a_ = df[(df.qi == qi) & (df.visit <= 3)]
        b_ = df[df.qi == qi + 1]
        m_ = a_.merge(b_[["dwelling", "hh", "line", "lfs_status"]], on=["dwelling", "hh", "line"], suffixes=("", "_b"))
        for d in P.DCODES:
            x = m_[m_.d27 == d]
            o = np.zeros((3, 3))
            np.add.at(o, (x.lfs_status.values - 1, x.lfs_status_b.values - 1), x.wt.values)
            for a, b in E.CELLS:
                per_pair.setdefault((d, a + b), []).append(E.not_real(o, A["M"], a, b))
    ok(E.warned({k: float(np.mean(v)) for k, v in per_pair.items()}) == gold,
       "SF15 the mean of the four pairs' own shares gives the same rates")
    q = A["M"]
    ok(abs(q.sum(1) - 1).max() < 1e-12 and (np.diag(q) > 0.8).all(), "SF16 each status's readings sum to one")

    # ---------------------------------------------------------------- ask A: the match rate
    df = solve.persons(target, F)
    mA = solve.ask_match(target, F, df)
    for x in fig["match"]:
        g = mA[x["district"]]
        ok(g[0] == x["persons"] and abs(round(g[1], 1) - x["rate"]) < 1e-9 and g[2] == x["due"], "A golden %s" % x["district"])
        ok(edge(g[1]) >= 0.007, "A %s 7 per cent of a bin from the edge (%.4f)" % (x["district"], g[1]))
    pid = pd.DataFrame([(h["dw"], h["hh"], p["line"], h["q"], p["pid"]) for h in W.hhq for p in h["people"]],
                       columns=["dwelling", "hh", "line", "qi", "pid"])
    at = {}
    for h in W.hhq:
        for p in h["people"]:
            at.setdefault((h["dw"], h["q"]), set()).add(p["pid"])
    m = solve.match(df).merge(pid, on=["dwelling", "hh", "line", "qi"], how="left")
    truth = [p_ in at.get((w, q_ + 1), set()) for p_, w, q_ in zip(m.pid, m.dwelling, m.qi)]
    ok(int((m.matched.values != np.array(truth)).sum()) == 0, "A the golden link is the truth for every person")
    birth = ["dwelling", "sex", "birth_year", "birth_month"]
    for qi in range(4):
        b_ = df[df.qi == qi + 1]
        ok(not b_.duplicated(birth).any(), "A sex and month and year of birth identify a person in a dwelling (%d)" % qi)
    raw = pd.concat([pd.read_csv(os.path.join(target, F["persons_" + q.lower()]), dtype={"dwelling": str})
                     for q in P.QUARTERS], ignore_index=True)
    dup = raw[raw.duplicated(keep=False)]
    ok(len(dup) > 0 and set(dup.quarter) == {"2027Q2"} and set(dup.district) == {"D11"},
       "A the one batch received twice: Market Towns, second quarter")
    # the primary: the server's restore of 17 May re-ingested the uploads of 14 May under the dwelling's next household
    # numbers, so every field but the household number repeats; each person once is the filed count
    exact = solve.persons(target, F, dedupe="exact")
    copies = exact[exact.duplicated([c for c in exact.columns if c not in ("hh", "d27", "qi")], keep="first")]
    ok(len(copies) > 0 and set(copies.int_date) == {P.REPLAY_DAY.isoformat()} and set(copies.quarter) == {"2027Q2"},
       "A the records received again are the uploads of 14 May only (%d)" % len(copies))
    gen = R.persons()
    top = gen.groupby("dwelling")["hh"].max()
    ok(all(h > top[d] for d, h in zip(copies.dwelling, copies.hh)), "A each copy under a number no household of its "
                                                                     "dwelling ever had")
    ok(len(exact) - len(copies) == len(df) and len(df) == len(gen), "A each person once gives the simulated records")
    cd = copies[copies.visit <= 3].groupby(copies.d27).size()
    ok(set(cd.index) == set(P.DCODES) and cd.min() >= 15, "A copies due another visit in every district (%d to %d)"
       % (cd.min(), cd.max()))
    keys = exact[["quarter", "dwelling", "hh", "line"]]
    ok(not keys.duplicated().any(), "A the copies pass the key check (dwelling, household and line unique)")
    crack = solve.ask_match(target, F, exact)
    ok(all(crack[d][2] != mA[d][2] and round(crack[d][1], 1) != round(mA[d][1], 1) for d in P.DCODES),
       "A the cracker (every filed rule, identical rows once) misses every district's base and rate")
    line = solve.ask_match(target, F, df, key="line")
    ok(all(round(line[d][1], 1) != round(mA[d][1], 1) for d in P.DCODES), "A the line key alone misses every rate")
    keep = solve.persons(target, F, dedupe="none")
    kd = solve.ask_match(target, F, keep)
    ok(all(kd[d][2] != mA[d][2] for d in P.DCODES), "A the rows as received move every district's base")
    old = solve.ask_match(target, F, df, district="district")
    ok(old["D02"] != mA["D02"] and old["D04"] != mA["D04"], "A the recorded codes move the Fringe and the Corridor")
    ok(all(old[d] == mA[d] for d in P.DCODES if d not in ("D02", "D04")), "A the recorded codes move those two only")

    # ---------------------------------------------------------------- ask B: reinterview timing
    dB = solve.ask_days(target, F, df)
    for x in fig["days"]:
        g = dB[x["district"]]
        ok(g[0] == x["persons"] and abs(round(g[1], 1) - x["mean"]) < 1e-9, "B golden %s" % x["district"])
        ok(edge(g[1]) >= 0.007, "B %s 7 per cent of a bin from the edge (%.4f)" % (x["district"], g[1]))
    stops = {"the call's date as recorded": solve.ask_days(target, F, df, date="attempt_date"),
             "the household's first interview": solve.ask_days(target, F, df, anchor="household")}
    for k, v in stops.items():
        ok(all(round(v[d][1], 1) != round(dB[d][1], 1) for d in P.DCODES), "B the stop '%s' misses every district" % k)
    log = pd.read_csv(os.path.join(target, F["reint_log"]), dtype={"dwelling": str})
    ad = log.attempt_date.map(dt.date.fromisoformat)
    vd = log.visit_start.map(lambda s: dt.date.fromisoformat(s[:10]))
    upd = log.supervisor.map(P.APP_UPDATE)
    after = vd >= upd
    ok(((ad == vd) == ~after).all(), "B the two dates agree before each tablet's update and only before it")
    ok(set(d.weekday() for d in ad[after]) == {4}, "B from the update the call's date is always a Friday")
    ok(log.groupby("supervisor").apply(lambda g: (vd[g.index] >= upd[g.index]).sum() > 0).all(),
       "B every supervisor's tablet took the update")
    hours = log.visit_start.str[11:13].astype(int)
    ok(hours.min() >= 9 and hours.max() <= 20 and (hours[vd.map(lambda d: d.weekday() == 4)] >= 16).all(),
       "B visits between 9:00 and 21:00, Friday's in the evening")
    ok(len(set(d.weekday() for d in vd)) == 7, "B the visits fall on every day of the week")
    # the window: under visit_start every person in the results file was reinterviewed within 14 days of their own
    # interview; under the call's date as recorded some were not, which the protocol rules out (sections 5 and 6)
    done = log[log.result == "completed"].assign(vd=vd, ad=ad)
    rr = r.merge(df[["quarter", "dwelling", "hh", "line", "int_date"]].drop_duplicates(), on=["quarter", "dwelling", "hh",
                                                                                              "line"])
    rr = rr.merge(done[["quarter", "dwelling", "hh", "vd", "ad"]], on=["quarter", "dwelling", "hh"])
    iday = rr.int_date.map(dt.date.fromisoformat)
    by_visit = np.array([(v - i).days for v, i in zip(rr.vd, iday)])
    by_call = np.array([(v - i).days for v, i in zip(rr.ad, iday)])
    ok(len(rr) == len(r), "B every person in the results file has a completing visit in the log")
    ok(by_visit.max() <= P.REINT_WINDOW and by_visit.min() >= 1, "B visit_start: every result within the window")
    ok((by_call > P.REINT_WINDOW).sum() >= 100, "B the call's date as recorded puts %d results outside the window"
       % (by_call > P.REINT_WINDOW).sum())
    late = solve.ask_days(target, F, df, late=False)
    ok(sum(round(late[d][1], 1) != round(dB[d][1], 1) for d in P.DCODES) >= 10, "B the late reinterviews left out move "
                                                                               "ten districts or more")
    q4 = solve.ask_days(target, F, df, quarters=P.QUARTERS)
    ok(sum(round(q4[d][1], 1) != round(dB[d][1], 1) for d in P.DCODES) >= 6, "B 2026Q4 kept in moves six districts or "
                                                                             "more")

    # ---------------------------------------------------------------- the critical components' rounding
    for k, v in fig["reinterview"]["misread"].items():
        x = 100 * A["M"][S.index(k[0]), S.index(k[1])]
        ok(edge(x, 0.01) >= 0.0007, "M %s 7 per cent of a bin from the edge (%.5f)" % (k, x))
    for s, v in fig["reinterview"]["correct"].items():
        x = 100 * A["M"][S.index(s), S.index(s)]
        ok(edge(x, 0.01) >= 0.0007, "M %s%s 7 per cent of a bin from the edge (%.5f)" % (s, s, x))
    for k, v in sh.items():
        ok(edge(100 * v) >= 0.007, "share %s%s 7 per cent of a bin from the edge (%.4f)" % (k[0], k[1], 100 * v))
    ok(edge(100 * list(p0.values())[0]) >= 0.007 and edge(100 * list(p1.values())[0]) >= 0.007,
       "the rungs' figures off the edge")

    # ---------------------------------------------------------------- the realism sweep
    ok(len({x["persons"] for x in fig["match"]}) == 12 and len({x["due"] for x in fig["match"]}) == 12,
       "realism: no identical counts across districts")
    ok(len({x["persons"] for x in fig["days"]}) == 12, "realism: no identical reinterview counts across districts")
    ok(all(x["persons"] % 100 for x in fig["match"]), "realism: no round counts")
    flows = [A["O"][d][i, j] for d in P.DCODES for i in range(3) for j in range(3)]
    ok(len(set(flows)) == len(flows), "realism: no two published flows equal")
    sizes = raw.groupby(["quarter", "district"]).size()
    ok(sizes.value_counts().max() <= 4 and raw.groupby("quarter").size().nunique() == len(P.QUARTERS),
       "realism: no quarter's file the size of another's, no district sample size five times (60 cells of about "
       "3,700 persons)")
    ok(log.groupby("supervisor").size().nunique() == len(P.SUPERVISORS), "realism: supervisors' workloads differ")

    # ---------------------------------------------------------------- the input gates and the dates
    files = [B.FILES[k] for k in B.PACK]
    ok(len(files) >= 10 and all(os.path.exists(os.path.join(target, f)) for f in files), "gate: 10 or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "gate: 3 or more formats")
    big = max(sum(1 for _ in open(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "gate: a file of 25,000 rows or more (%d)" % big)
    ok(len(B.DISTRACTORS) >= 2, "gate: two or more distractors")
    for f in files:
        if f.endswith((".csv", ".md", ".eml")):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            ok("—" not in txt and "–" not in txt, "no dashes: %s" % f)
    last = max(dt.date.fromisoformat(x) for x in df.int_date)
    ok(last < dt.date(2028, 1, 1) and vd.max() < dt.date(2028, 2, 2), "dates: every record before the request")
    return Count.n
