"""The generator's assertions on the world and on the cut pack: the golden is the world's truth and every estimator
of a single factor agrees on it, every named wrong route files another list, the easy route fails on the clean truth
(dataset-generation 7.1), every semantic fork of the call is closed (SF1 to SF11, SF17), the asks' figures are the world's
and do not move with any convention the pack leaves open, and the pack gates hold.

    python3 checks.py [target]      exit 0 when every check passes"""
import datetime as dt
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import params as P
import records as RC
import sim
import solve as S

TASK = os.path.dirname(HERE)
N = {"pass": 0}
FAILS = []


def ok(cond, what):
    if cond:
        N["pass"] += 1
    else:
        FAILS.append(what)


def main(T=None):
    T = T or os.path.join(TASK, "target")
    W = sim.world(P.SEED)
    ser = RC.serials(W, P.SEED)
    sid = {i: ser[i][0] for i in range(len(W["meters"]))}
    D = S.load(T, B.FILES)
    Pf = S.pairs_frame(D)
    e, G = S.call(D, P=Pf)

    # the golden is the world's truth
    truth = sorted(sid[i] for i, m in enumerate(W["meters"]) if abs(m["b"]) > 0.05)
    ok(G == truth, "golden list is the world's truth: %s against %s" % (G, truth))
    ok(len(G) == 8, "eight meters listed")

    # SF2: every estimator of a single factor gives the same list, 1 point clear of the line
    for kw in S.FAMILY:
        ek, Lk = S.call(D, P=Pf, **kw)
        ok(Lk == G, "SF2 family %s gives the golden list" % kw)
        ok(min(abs(abs(v) - S.TOL) for v in ek.values()) >= 1.0, "SF2/SF6 family %s at least 1 point clear" % kw)

    # every named wrong route files another list
    for name, kw in S.VARIANTS.items():
        if name == "golden":
            continue
        ek, Lk = S.call(D, P=Pf, **kw)
        ok(Lk != G, "route '%s' files another list" % name)
    e1, L1 = S.call(D, P=Pf, population="all")
    ok(len(set(L1) - set(G)) >= 1 and len(set(G) - set(L1)) >= 1, "the pooled route both drops and adds a meter")

    # the scheduled set read from the pack is exactly the world's scheduled pairings
    acc_cp = set()
    Pw = sorted(W["pairs"], key=lambda p: p["draw"])
    pr = D["pairs"]
    ok(len(pr) == len(Pw), "one pairing row per world pairing")
    kinds = [p["kind"] for p in Pw]
    ok(list(Pf["sched"]) == [k == "CP" for k in kinds], "the plan and the morning round recover the scheduled pairings")

    # dataset-generation 7.1: the easy route on the clean truth files the wrong list; the decisive step alone fixes it
    by = {}
    for p in W["pairs"]:
        t = W["tests"][p["test"]]
        L = p["L"] / (1 + sim.LAB_A) if p["civil_date"] < sim.SWITCH else p["L"]
        if p["civil_date"] > W["meters"][t["m"]]["svc"] and sim.LO <= t["M"] <= sim.HI:
            by.setdefault(t["m"], []).append((t["M"] / L - 1, p["kind"]))
    easy = sorted(sid[m] for m, v in by.items() if abs(np.mean([r for r, k in v])) > 0.05)
    right = sorted(sid[m] for m, v in by.items() if abs(np.mean([r for r, k in v if k == "CP"])) > 0.05)
    ok(easy != truth, "analyst test: every pairing on the clean truth files a wrong list")
    ok(right == truth, "analyst test: the scheduled pairings alone file the truth")

    # SF1: every meter in the register has its scheduled pairings
    sel = Pf["sched"] & Pf["since"] & Pf["num"].notna()
    n = Pf[sel].groupby("matricola").size()
    ok(set(n.index) == set(D["reg"]["matricola"]) and n.min() >= 90, "SF1 every register meter has 90 or more pairings")
    # SF3, SF10: one filed factor; the raw laboratory files another list (asserted among the routes)
    ok(abs(S.A_OVER_B - 1.035) < 1e-12, "SF3/SF10 the note's factor")
    # SF4: since the calibration, asserted among the routes (since July 2026 files another list)
    # SF5: no scheduled pairing on its meter's calibration day
    cal = {r.matricola: r.ultima_taratura.date() for r in D["reg"].itertuples(index=False)}
    on_cal = sum(1 for m, d, s in zip(Pf["matricola"], Pf["dd"], Pf["sched"]) if s and d == cal[m])
    ok(on_cal == 0, "SF5 no scheduled pairing on a calibration day (%d)" % on_cal)
    # SF7: a LO or HI reading carries no number; set at the range's ends instead, the list does not move
    Pi = Pf.copy()
    Pi.loc[Pi["glucometro_mg_dl"] == "LO", "num"] = 20.0
    Pi.loc[Pi["glucometro_mg_dl"] == "HI", "num"] = 600.0
    ok(S.call(D, P=Pi)[1] == G, "SF7 LO and HI at the range's ends give the same list")
    ok(int((Pf["sched"] & Pf["since"] & Pf["num"].isna()).sum()) <= 10, "SF7 few LO or HI among the pairings used")
    proc = open(os.path.join(HERE, "docs.py"), encoding="utf-8").read()
    ok("le letture LO e HI, che non" in proc and "non entrano nella stima" in proc,
       "SF7 section 7 files that LO and HI readings stay out of the estimate")
    # SF8: the plan's holiday rule does not move the list
    Ph = S.pairs_frame(D, holiday_rule=False)
    ok(S.call(D, P=Ph)[1] == G, "SF8 the list without the holiday rule")
    # SF9: no other pairing within ten minutes of the round's edges on a planned day
    pl = S.planned(D)
    edge = sum(1 for m, d, mm, s in zip(Pf["matricola"], Pf["dd"], Pf["mm"], Pf["sched"])
               if not s and d in pl.get(m, ()) and S.ROUND[0] - 10 <= mm <= S.ROUND[1] + 10)
    ok(edge == 0, "SF9 the round's edges are clear (%d)" % edge)
    # SF10: the note's factor read as a multiplier of 0.965 instead of a division by 1.035
    P965 = Pf.copy()
    P965["lab_b"] = np.where(P965["dd"] < S.SWITCH, P965["lab"] * 0.965, P965["lab"])
    ok(S.call(D, P=P965)[1] == G, "SF10 the list with the C600 multiplied by 0.965")
    # SF11: the meter's date and the laboratory's date give the same scheduled and since sets
    md = [dt.datetime.strptime(x, "%d/%m/%Y %H:%M:%S").date() for x in pr["data_ora_test"]]
    ok(all((d == m) or not s for d, m, s in zip(Pf["dd"], md, Pf["sched"])), "SF11 scheduled pairings dated alike")

    # the asks: the world's figures, and no open convention moves them
    a1, a2 = S.asks(D)
    E2 = S.results(D)
    y = E2[[d.year == 2027 for d in E2["day"]]].copy()
    y["q"] = [(d.month - 1) // 3 + 1 for d in y["day"]]
    y["late2"] = (y["rec"] - y["utc"]).dt.total_seconds() >= 7200
    ge = {(h, int(q)): 100.0 * g["late2"].mean() for (h, q), g in y.groupby(["hosp", "q"])}
    ok(all(round(ge[k], 1) == round(v, 1) for k, v in a1.items()), "SF16 two hours or more gives the same shares")
    for kw in (dict(date="utc"), dict(date="meter")):
        b1, b2 = S.asks(D, **kw)
        ok(all(round(b1[k], 1) == round(v, 1) for k, v in a1.items()) and b2 == a2, "SF15 asks unmoved by %s" % kw)
    X = RC.build(W, P.SEED)
    first = {}
    for i, rec, cp in X["receptions"]:
        first[i] = min(first.get(i, rec), rec)
    late, cnt = {}, {}
    for i, t in enumerate(W["tests"]):
        if t["kind"] != "P":
            continue
        civ = sim.utc_to_civil(t["utc"])
        if civ.year != 2027:
            continue
        w = t["ward"]
        h = RC.hosp_of(w)
        q = (civ.month - 1) // 3 + 1
        late.setdefault((h, q), []).append(first[i] - (t["utc"] * 60 + t["sec"]) > 7200)
        cnt[w] = cnt.get(w, 0) + 1
    ok(all(round(100 * np.mean(v), 1) == round(a1[k], 1) for k, v in late.items()), "SF12/SF13 ask 1 is the world's (first reception, solar clock)")
    ok(cnt == a2, "SF14 ask 2 is the world's (the ward where the meter stood)")

    # the devices are present: copies, the solar clock, the moved meters' current assignment
    E = D["export"]
    ok(E.duplicated(["matricola", "n_memoria"]).sum() > 1000, "SF12 re-sent copies present")
    moved = [m for m in set(D["hist"]["matricola"]) if (D["hist"]["matricola"] == m).sum() > 1]
    ok(len(moved) == 7, "SF14 seven meters moved")
    # SF17: a listed meter's ward and hospital, the register's current assignment or where it stood when paired
    ok(not set(moved) & set(G), "SF17 no listed meter moved, so its ward and hospital read alike")
    summer = [(dt.datetime.strptime(b, "%d/%m/%Y %H:%M") - dt.datetime.strptime(a[:16], "%d/%m/%Y %H:%M")
               ).total_seconds() / 60 for a, b, s, d in zip(pr["data_ora_test"], pr["data_ora_prelievo"], Pf["sched"],
                                                            Pf["dd"]) if s and dt.date(2027, 4, 1) <= d <= dt.date(2027, 9, 30)]
    winter = [(dt.datetime.strptime(b, "%d/%m/%Y %H:%M") - dt.datetime.strptime(a[:16], "%d/%m/%Y %H:%M")
               ).total_seconds() / 60 for a, b, s, d in zip(pr["data_ora_test"], pr["data_ora_prelievo"], Pf["sched"],
                                                            Pf["dd"]) if s and dt.date(2027, 11, 1) <= d]
    ok(abs(np.median(summer) - 60) <= 6 and abs(np.median(winter)) <= 6, "SF13 the meters' clocks keep solar time")

    # Gate G and the separation line: the pairing report carries no summary and no copy
    ok(list(pr.columns) == ["id_risultato", "matricola", "data_ora_test", "glucometro_mg_dl", "n_accettazione",
                            "data_ora_prelievo", "laboratorio_mg_dl", "presidio", "reparto"], "pairing report columns")
    ok(pr["n_accettazione"].is_unique and pr["id_risultato"].is_unique, "one row per tube and per meter result")

    # pack gates
    files = [B.FILES[k] for k in B.PACK]
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "10 or more files, 3 or more formats")
    ok(len(E) >= 25000, "spine of 25,000 rows or more")
    ok(len(B.DISTRACTORS) >= 2, "two distractors")
    for k in ("dictionary", "mail"):
        txt = open(os.path.join(T, B.FILES[k]), encoding="utf-8").read()
        ok("—" not in txt and "–" not in txt, "no em or en dash in %s" % B.FILES[k])
    import docs
    src = open(os.path.join(HERE, "docs.py"), encoding="utf-8").read()
    ok("—" not in src and "–" not in src, "no em or en dash in the documents' source")
    for w in ("selezion", "distors", "regressione verso", "programmat"):
        ok(not re.search(w, src, re.I), "the documents never say '%s'" % w)
    print("checks: %d passed, %d failed" % (N["pass"], len(FAILS)))
    for f in FAILS:
        print("   FAIL", f)
    return FAILS


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 0)
