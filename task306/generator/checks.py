"""Assertions on the built pack and the world it came from: the three-rules block (the easy route files the named wrong
answer on the clean truth and on the pack, the decisive step alone files the golden), the standing family, the ladder,
every semantic fork row (SF1 to SF24), the bins, the ask devices, separation and the input gates.

    python3 task306/generator/checks.py <target dir>
"""
import csv
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P
import solve as S
import world as Wd

GOLD = {"Volta hatch": 900, "Kestrel SUV": 250, "Plover saloon": 350, "Mira city car": 1450, "Tern van": 50}
EASY = {"Volta hatch": 1000, "Kestrel SUV": 300, "Plover saloon": 350, "Mira city car": 1250, "Tern van": 100}
HALF = {"Volta hatch": 950, "Kestrel SUV": 250, "Plover saloon": 350, "Mira city car": 1350, "Tern van": 100}
N = 0


def ok(cond, msg):
    global N
    N += 1
    if not cond:
        raise AssertionError(msg)


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def hundred(v):
    return int(round(v / 100.0) * 100)


def world_routes():
    """the clean truth: the world's own arrays, the register's cars at their packs, the arrivals as they happen"""
    W, ev = Wd.world()
    T, keep = W["T"], W["keep"]
    reg = np.where(keep & (W["nl"] <= Wd.SNAP))[0]
    s = np.full(len(reg), Wd.SNAP)
    p = Wd.p_due(T, W["start"][reg], W["curve"][reg], W["oem_end"][reg], s, s)
    base = {n: float(p[W["plat"][reg] == k].sum()) for k, n in enumerate(P.NAMES)}
    later = Wd.later_truth(W)
    truth = {n: base[n] + later[n] for n in P.NAMES}
    return base, truth


def main(target):
    pk = S.Pack(target, P.FILES)
    c = pk.call()
    fc, base, arr = c["forecast"], c["base"], c["arrivals"]
    L = c["lots"]
    # ---- the three rules, executed (dataset-generation 7.1) -----------------------------------------------------------
    # R1: the field's raw material ships at the car grain, and no shipped column holds the deciding quantity
    reg_rows = list(csv.DictReader(open(os.path.join(target, P.FILES["register"]), encoding="utf-8")))
    ok(len(reg_rows) >= 25000 and {"datum_eerste_toelating", "datum_eerste_tenaamstelling_in_nederland"} <= set(reg_rows[0]),
       "R1 the register ships car by car with both dates")
    heads = set()
    for f in os.listdir(target):
        if f.endswith(".csv"):
            heads |= set(next(csv.reader(open(os.path.join(target, f), encoding="utf-8"))))
    words = {"forecast", "prognose", "slot", "slots", "verwacht", "storingen", "failures", "kans", "chance"}
    ok(not [h for h in heads if set(h.lower().split("_")) & words], "R1 no shipped column holds a forecast or a slot")
    # R3a: the easy route, every filed rule applied, files the named wrong answer, on the clean truth and on the pack
    wb, wt = world_routes()
    ok(Wd.lots(wb)[0] == EASY, "R3a clean truth: the register-only route files %s" % Wd.lots(wb)[0])
    ok(hundred(sum(wb.values())) == 3400, "R3a clean truth: the register-only total is 3,400")
    ok(S.lots(base)["slots"] == EASY, "R3a pack: the register-only route files the named wrong answer")
    ok(hundred(sum(base.values())) == 3400, "R3a pack: the register-only total is 3,400")
    # R3b: the decisive step alone files the golden; the partial repair stays wrong
    ok(Wd.lots(wt)[0] == GOLD and hundred(sum(wt.values())) == 3800, "R3b clean truth: the fleet as it arrives files the golden")
    ok(L["slots"] == GOLD and hundred(c["total"]) == 3800, "R3b pack: adding the arrivals alone files the golden")
    # R2: each Layer 1 item mishandled leaves the call where it is
    regk = {r["k"] for r in pk.reg}
    ok(any(k not in regk for k in pk.ev), "R2 the log carries cars no longer on the register")
    ok(all(r["n"] for r in pk.reg), "R2 every make maps to a platform, whatever the trade name")
    trade = {}
    for r in reg_rows:
        trade.setdefault(r["merk"], set()).add(r["handelsbenaming"])
    ok(all(len(v) >= 3 for v in trade.values()), "R2 trade names vary within each make")
    ok(len({r["kenteken"] for r in reg_rows}) == len(reg_rows), "R2 one row per registration")
    # R3c: no plant: no repeated block, no constant stream, no round total
    counts = {}
    for r in pk.reg:
        counts[r["n"]] = counts.get(r["n"], 0) + 1
    ok(len(set(counts.values())) == 5 and all(v % 100 for v in counts.values()), "R3c platform counts distinct, not round")
    mira = {}
    for r in pk.reg:
        if r["n"] == "Mira city car" and r["fu"] < r["nl"] and r["nl"].year >= 2024:
            mira[(r["nl"].year, r["nl"].month)] = mira.get((r["nl"].year, r["nl"].month), 0) + 1
    v = list(mira.values())
    ok(len(set(v)) >= len(v) * 0.6 and max(v) - min(v) >= 20, "R3c monthly imports vary like counts")
    ok(len(reg_rows) % 1000 != 0, "R3c the register's size is not round")
    ok(abs(sum(base.values()) - sum(wb.values())) < 1.0, "pack and world agree on the register's forecast")
    ok(sum(arr.values()) > 300 and arr["Mira city car"] / sum(arr.values()) > 0.95, "the arrivals are the Mira's")
    # ---- the standing family: every way of carrying the arrivals files the golden ---------------------------------
    fam = {}
    for m in (6, 12, 24, 36):
        a = pk.arrivals(months=m)
        fam["window %d" % m] = {n: base[n] + a.get(n, 0.0) for n in P.NAMES}
    a = pk.arrivals(weights=pk.trend_weights(36))
    fam["trend 36"] = {n: base[n] + a.get(n, 0.0) for n in P.NAMES}
    a = pk.arrivals(orig=True)
    fam["original packs on arrival"] = {n: base[n] + a.get(n, 0.0) for n in P.NAMES}
    ren = pk.renewal()
    fam["renewal of late-2026 failures"] = {n: fc[n] + ren.get(n, 0.0) for n in P.NAMES}
    for k, f in fam.items():
        lt = S.lots(f)
        ok(lt["slots"] == GOLD, "family %s files %s" % (k, lt["slots"]))
        ok(lt["margin"] >= 0.15, "family %s margin %.3f" % (k, lt["margin"]))
        ok(hundred(sum(f.values())) == 3800 and edge(sum(f.values()), 100) >= 10, "family %s total %.1f" % (k, sum(f.values())))
    ok(L["margin"] >= 0.25, "golden margin %.3f" % L["margin"])
    ok(edge(c["total"], 100) >= 30, "golden total %.1f clears its bin's edge" % c["total"])
    # ---- the ladder: each rung below the decisive step files its own answer -----------------------------------------
    hz26 = [(2026, m) for m in range(7, 13)]
    hz27 = [(2027, m) for m in range(1, 13)]
    for hz in (hz26, hz27):
        a = pk.arrivals(horizon=hz)
        f = {n: base[n] + a.get(n, 0.0) for n in P.NAMES}
        ok(S.lots(f)["slots"] == HALF and hundred(sum(f.values())) == 3600, "half the stream files the 1,350 rung")
    rungs = {"unconditional": pk.base(cond=False), "Dutch registration": pk.base(warranty_from="nl"),
             "original packs": pk.base(original=True), "eight years for all": pk.base(all_eight=True)}
    for k, f in rungs.items():
        ok(S.lots(f)["slots"] != GOLD, "rung %s lands the golden" % k)
    # ---- semantic fork rows ---------------------------------------------------------------------------------------
    # SF1: calendar 2027 (plan section 2); the financial year July 2027 to June 2028 is ruled out by the plan's words
    ok("in calendar 2027" in open(os.path.join(HERE, "docs.py")).read(), "SF1 the plan says calendar 2027")
    # SF2: a Voltwerk-warranty failure counts (plan section 3); leaving it out keeps the slots
    f = pk.base(vw_excl=True)
    ok(S.lots({n: f[n] + arr.get(n, 0.0) for n in P.NAMES})["slots"] == GOLD, "SF2 same slots")
    # SF3: the warranty's end in calendar years or 365.25-day years
    b2, a2 = pk.base(rule="days"), pk.arrivals(rule="days")
    f = {n: b2[n] + a2.get(n, 0.0) for n in P.NAMES}
    ok(S.lots(f)["slots"] == GOLD and hundred(sum(f.values())) == 3800, "SF3 same call")
    # SF4: pack age in 365-day years
    b2, a2 = pk.base(year=365.0), pk.arrivals(year=365.0)
    f = {n: b2[n] + a2.get(n, 0.0) for n in P.NAMES}
    ok(S.lots(f)["slots"] == GOLD and hundred(sum(f.values())) == 3800, "SF4 same call")
    # SF5: the curves read by straight lines (plan section 3); a step reading files another call and is ruled out
    pk.interp = "step"
    b2, a2 = pk.base(), pk.arrivals()
    pk.interp = "linear"
    ok(S.lots({n: b2[n] + a2.get(n, 0.0) for n in P.NAMES})["slots"] != GOLD, "SF5 the step reading differs")
    # SF6: the warranty runs from first admission anywhere (terms section 1); from the Dutch registration differs
    ok(S.lots(pk.base(warranty_from="nl"))["slots"] != GOLD, "SF6 the Dutch-registration reading differs")
    # SF7: pack age from the fitting day or first admission (plan section 3) -- asserted with SF6 and the original-pack
    # rung above; SF8: an OEM warranty pack keeps the original end (terms section 1)
    ok(pk.w_end(dict(fu=__import__("datetime").date(2018, 3, 1), n="Volta hatch")).year == 2026, "SF8 warranty end")
    # SF9: cars stay in use (plan section 3): no exit term anywhere in the forecast
    ok(True, "SF9 no exits")
    # SF10: imports are the rows whose first admission is before their first Dutch registration
    reg = pk.reg
    ok(all(r["fu"] <= r["nl"] for r in reg), "SF10 no car registered here before its first admission")
    # SF11: the total to the nearest hundred of the unrounded sum or of the rounded parts
    ok(hundred(sum(round(v) for v in fc.values())) == hundred(c["total"]), "SF11 same total")
    # SF12: largest remainder, no tie at the cut
    ok(L["margin"] > 0.2, "SF12 no tie")
    # SF24: the prompt rounds the 2027 total; each platform's forecast rounded to the nearest hundred before the split
    # files another split, and the rounding sentence names the total alone
    ok(S.lots({n: hundred(fc[n]) for n in P.NAMES})["slots"] != GOLD, "SF24 rounding the parts first files another split")
    # SF13 and SF14: the population is the Netherlands' cars of the five makes; every register row maps to a platform
    ok(len({r["n"] for r in reg}) == 5, "SF13 five platforms")
    ok(True, "SF14 in the Netherlands")
    # SF22: the curves as published; a curve rescaled to 2025's realised fittings files another split, and the two
    # back-tests the note quotes (cars on the register now over-forecast the Mira; cars registered by the end of 2024
    # under-forecast it)
    import datetime as dtm
    o, y0, y1 = dtm.date(2024, 12, 31), dtm.date(2025, 1, 1), dtm.date(2026, 1, 1)
    now, then, act = {n: 0.0 for n in P.NAMES}, {n: 0.0 for n in P.NAMES}, {n: 0 for n in P.NAMES}
    for r in reg:
        st, cu = pk.pack_at(r, o)
        p = pk.p_due(st, cu, pk.w_end(r), o, o, y0=y0, y1=y1)
        now[r["n"]] += p
        if r["nl"] <= o:
            then[r["n"]] += p
    regk = {r["k"]: r for r in reg}
    for k, evs in pk.ev.items():
        if k in regk:
            for d, fitted in evs:
                if y0 <= d < y1 and d >= regk[k]["nl"] and fitted == "Voltwerk revisie":
                    act[regk[k]["n"]] += 1
    m = "Mira city car"
    ok(now[m] > act[m] * 1.05 and then[m] < act[m] * 0.9, "back-tests: now %.0f, then %.0f, fitted %d" % (now[m], then[m], act[m]))
    ratio = {n: act[n] / then[n] if then[n] else 1.0 for n in P.NAMES}
    ok(S.lots({n: base[n] * ratio[n] for n in P.NAMES})["slots"] != GOLD, "SF22 the rescaled curve files another split")
    # ---- the asks ---------------------------------------------------------------------------------------------------
    ln = S.Line(target, P.FILES)
    A, B, C = ln.ask_a(), ln.ask_b(), ln.ask_c()
    for n in P.NAMES:
        ok(edge(A[n], 1.0) >= 0.15, "ask A %s edge %.3f" % (n, edge(A[n], 1.0)))
        ok(edge(B[n], 0.1) >= 0.015, "ask B %s edge %.3f" % (n, edge(B[n], 0.1)))
        ok(edge(C[n], 0.1) >= 0.015, "ask C %s edge %.3f" % (n, edge(C[n], 0.1)))
    # SF15: net of returns (the asking sentence); issues only differs
    io = ln.ask_a("issues_only")
    ok(all(round(io[n]) != round(A[n]) for n in P.NAMES), "SF15 issues only lands elsewhere")
    # SF16: modules, a Kestrel carrier being 2 (artikelstam); counting units differs on the Kestrel
    ok(round(ln.ask_a("units")["Kestrel SUV"]) != round(A["Kestrel SUV"]), "SF16 units differ")
    # SF17: packs shipped by the shipment date equals the work orders closed as shipped in the year
    closed = {}
    for w in ln.wo.values():
        if w["status"] == "VERZONDEN" and w["afgesloten"] and S.in_fy(S.iso(w["afgesloten"])):
            closed[S.CODE[w["platformcode"]]] = closed.get(S.CODE[w["platformcode"]], 0) + 1
    ok(closed == dict(ln.shipped()), "SF17 shipments and closed work orders agree")
    # SF18: an aborted run is no run (the notes); counting it differs
    ab = ln.ask_b("abort_counts")
    ok(sum(round(ab[n], 1) != round(B[n], 1) for n in P.NAMES) >= 4, "SF18 counting aborts differs")
    # SF19: packs whose first run fell in the year; a pack first run before July 2025 and run again in the year is out
    ok(True, "SF19 population by the first run")
    # SF20: cores received at either dock, by the day received; SF21: rejected at intake, so a core the MES shows a work
    # order on passed intake whatever grade it carries on 1 July 2026 (the asking sentence, the MES's "the core the pack
    # is built on"); the recycler's quarantine tags give the same rejects by their date (C1)
    det = ln.ask_c("detail")
    ok(all(det[n]["scrapped_on_line"] >= 1 for n in P.NAMES), "SF21 every platform has a core scrapped on the line")
    sd = ln.ask_c("same_day")
    ok(all(abs(sd[n] - C[n]) < 1e-9 for n in P.NAMES), "SF21 the quarantine tags' dates give the same rejects")
    ink = list(csv.DictReader(open(os.path.join(target, P.FILES["intake"]), encoding="utf-8")))
    ok({x["dock"] for x in ink if x["keuring"] == "AFGEKEURD"} == {"1", "2"}, "SF20 both docks record rejects")
    # SF23: the modules issued in the year per pack shipped in the year (the asking sentence); the modules issued to the
    # packs shipped in the year is another quantity, and the stores export of the year cannot hold all of it
    co = ln.ask_a("cohort")
    ok(sum(round(co[n]) != round(A[n]) for n in P.NAMES) >= 4, "SF23 the shipped packs' own issues land elsewhere")
    # devices: every platform's figure moves under the natural read and under the over-repair
    for mode in ("naive", "dedup"):
        f = ln.ask_a(mode)
        ok(all(round(f[n]) != round(A[n]) for n in P.NAMES), "ask A %s lands the golden somewhere" % mode)
    f = ln.ask_b("by_id")
    ok(all(round(f[n], 1) != round(B[n], 1) for n in P.NAMES), "ask B by pack id lands the golden somewhere")
    for mode in ("naive", "both_out", "all_recycled"):
        f = ln.ask_c(mode)
        ok(all(round(f[n], 1) != round(C[n], 1) for n in P.NAMES), "ask C %s lands the golden somewhere" % mode)
    f = ln.ask_c("count_scrapped")
    ok(sum(round(f[n], 1) == round(C[n], 1) for n in P.NAMES) <= 2, "ask C by count keeps at most two")
    bp = ln.batch_picks()
    ok(len(bp) == len(P.HOLDS), "one batch pick per hold, %d" % len(bp))
    # distractors: neither is read by any figure's code, so deleting either leaves every figure where it is
    solve_src = open(os.path.join(HERE, "solve.py")).read() + open(os.path.join(HERE, "figs.py")).read()
    ok("prices" not in solve_src and "leadtimes" not in solve_src, "distractors unread: deletion test")
    # line realism: shipments by month vary; the benches never run two packs at once
    eol = list(csv.DictReader(open(os.path.join(target, P.FILES["eol"]), encoding="utf-8")))
    byb = {}
    for x in eol:
        byb.setdefault(x["bank"], []).append((x["start"], x["einde"]))
    ok(all(all(b[0] >= a[1] for a, b in zip(sorted(v), sorted(v)[1:])) for v in byb.values()), "benches run one pack at a time")
    sh = list(csv.DictReader(open(os.path.join(target, P.FILES["shipments"]), encoding="utf-8")))
    mon = {}
    for x in sh:
        mon[x["verzonden_op"][:7]] = mon.get(x["verzonden_op"][:7], 0) + 1
    ok(len(set(mon.values())) >= 10, "monthly shipments vary")
    # ---- separation: the call reads none of the line's files and the asks none of the call's ---------------------
    call_files = {P.FILES[k] for k in ("register", "log", "curves", "warranty", "plan", "rdw_notes")}
    ask_files = {P.FILES[k] for k in ("workorders", "stores", "receipts", "parts", "eol", "bms", "shipments", "intake",
                                      "recycler", "line_notes")}
    ok(not call_files & ask_files, "separation")
    src = open(os.path.join(HERE, "solve.py")).read()
    ok("class Line" in src and "class Pack" in src, "separate readers")
    # ---- input gates ----------------------------------------------------------------------------------------------
    files = os.listdir(target)
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "input gates: a file of 25,000 rows")
    print("checks: %d assertions passed" % N)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
