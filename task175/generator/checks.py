"""task175 generator checks: input gates, the three-rules block (R1, R2, R3a to R3c), every semantic fork row, the
ladder, the bins, the asks' devices and their separation from the call, documents and realism.

    python3 checks.py <target>"""
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C       # noqa: E402
import calc              # noqa: E402
import docs as D         # noqa: E402

FAILS = []
N_OK = [0]


def check(label, ok, detail=""):
    if ok:
        N_OK[0] += 1
        print("  ok   %s %s" % (label, detail))
    else:
        FAILS.append(label)
        print("  FAIL %s %s" % (label, detail))


def r5(x):
    return int(5 * round(x / 5.0))


def r10(x):
    return int(10 * round(x / 10.0))


def r50(x):
    return int(50 * round(x / 50.0))


def printed(g):
    return (r50(g["total"]),)


def edge(v, u):
    return u / 2.0 - abs(v - round(v / u) * u)


def main(target):
    task = os.path.dirname(os.path.abspath(target))
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    files = sorted(os.listdir(target))

    print("input gates")
    check("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = set(f.rsplit(".", 1)[1] for f in files)
    check("G2 three or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    with open(os.path.join(target, C.F_ROLL)) as fh:
        nroll = sum(1 for _ in fh) - 1
    check("G3 a file of 25,000 rows or more", nroll >= 25000, "%s %d rows" % (C.F_ROLL, nroll))
    dis = meta["distractor_files"]
    check("G4 two or more distractors declared", len(dis) >= 2 and all(os.path.exists(os.path.join(task, d)) for d in dis), ", ".join(dis))
    check("G5 no file named for a distractor or the stump", not any(re.search(r"distract|street|neighbo|build.?out|decoy", f, re.I) for f in files))

    P = calc.Pack(target)
    season = calc.season_shares(P)
    res, info = calc.routes(P, season)
    g = res["golden (homes on the street, count bins)"]
    gp = printed(g)
    print("figures.json")
    check("F1 the call in figures.json is the golden", (fig["call_total_permits_2027"],) == gp and
          not any(k.startswith("call_") and k != "call_total_permits_2027" for k in fig), str(gp))

    print("R1 the field's raw material ships")
    roll_head = open(os.path.join(target, C.F_ROLL)).readline().strip().split(",")
    check("R1a the roll is lot by lot with legal description, site address and year built",
          {"STRAP", "SITE_ADDR", "LEGAL_DESC", "YR_BUILT", "WATERFRONT"} <= set(roll_head) and nroll == P.N)
    check("R1b no shipped column holds a street's build-out or a lot's chance",
          not any(re.search(r"street|segment|block_?(built|share)|neighbo|hazard|chance|prob", h, re.I) for h in roll_head))
    check("R1c the golden reads served lot-years built from the roll and both permit files",
          len(P.sf_permits) > 15000 and info["fl"].size == fig["cc1_vacant_lots_total"])

    print("R3 the analyst test on the clean truth and on the pack")
    from world import World
    w = World()
    truth = w.truth()
    # the analog on the clean truth: first twelve months after acceptance, per vacant lot, on the forward vacant lots
    num = den = 0
    for ai in range(1, 16):
        acc = np.datetime64(w.area_acc[ai].isoformat()); end = acc + np.timedelta64(365, "D")
        sel = w.L["area"] == ai
        vac = sel & (w.yb0 == 0) & ~(w.issued < acc)
        num += int((sel & (w.issued >= acc) & (w.issued < end)).sum()); den += int(vac.sum())
    fwv = int((np.isin(w.L["area"], [w.area_names.index(n) for n in calc.FORWARD]) & w.vac27).sum())
    an_truth = num / den * fwv * 0.94
    check("R3a the analog on the clean truth files a wrong answer (30 per cent or more above the 2027 expectation)",
          an_truth > 1.30 * truth["total"], "analog %.0f against truth %.0f" % (an_truth, truth["total"]))
    d0 = res["default: first-year analog, raw"]
    check("R3a the default path on the pack ends two bins or more from the golden", abs(d0["total"] - g["total"]) >= 100,
          "%.1f printed %s" % (d0["total"], printed(d0)))
    check("R3b the decisive step alone (the street) lands the golden", gp[0] == fig["call_total_permits_2027"] and gp[0] != printed(d0)[0], str(gp))
    lo, hi = gp[0] - 25, gp[0] + 25
    for k in ("default: first-year analog, market-scaled", "rival: analog regressed on built share at service",
              "rival: served lot model without the street", "rival: homes on the plat block"):
        t = res[k]["total"]
        check("R3b single correction short of the street stays out of the golden's bin by half a bin or more: %s" % k,
              t >= hi + 25 or t < lo - 25, "%.1f against the bin %d to %d" % (t, lo, hi))
    for t, who in ((430, "reader A, round 1"), (550, "reader B, round 1")):
        check("R3b the round 1 readers' totals stay outside the golden's bin: %s" % who, t >= hi or t < lo, str(t))
    check("R3b the golden is within 10 per cent of the generator's 2027 expectation (estimation from the record)",
          abs(g["total"] / truth["total"] - 1) < 0.10, "%.1f against %.1f" % (g["total"], truth["total"]))

    print("the honest family and the bin (nearest 50)")
    fam, _ = calc.family(P, season)
    for k, v in fam.items():
        m = min(v["total"] - lo, hi - v["total"])
        check("B1 family member inside the golden's bin with 5 or more to spare: %s" % k, m >= 5,
              "%.1f, margin %.1f" % (v["total"], m))
    check("B2 the golden centred: both edges 8 or more away", edge(g["total"], 50) >= 8, "edge %.1f" % edge(g["total"], 50))
    span = [min(v[n] for v in fam.values()) for n in calc.FORWARD], [max(v[n] for v in fam.values()) for n in calc.FORWARD]
    rd = lambda x, u_: int(u_ * round(x / u_))
    split = {u_: [n for n, a, b in zip(calc.FORWARD, *span) if rd(a, u_) != rd(b, u_)] for u_ in (5, 10, 25)}
    check("B3 at the nearest 5, 10 and 25 some area's family straddles a line, so no area figure is graded",
          all(split[u_] for u_ in split), "; ".join("%s %.1f to %.1f" % (n, a, b) for n, a, b in zip(calc.FORWARD, *span))
          + " | " + "; ".join("%d: %s" % (u_, ", ".join(v)) for u_, v in split.items()))
    check("SF9 the rate-times-exposure form files the same call", printed(fam["count bins, rate times exposure"]) == gp)

    print("refutations, as log-likelihood on the record")
    LY = calc.lot_years(P, season, "street")
    grp = np.digitize(LY["n"], calc.COUNT_BINS)
    ll_street = calc.fit_poisson(LY, grp, len(calc.COUNT_BINS) + 1)[3]
    LB = calc.lot_years(P, season, "block")
    ll_block = calc.fit_poisson(LB, np.digitize(LB["n"], calc.COUNT_BINS), len(calc.COUNT_BINS) + 1)[3]
    LYc = dict(LY, canal=np.zeros(len(LY["y"]), dtype=int))
    ll_nocanal = calc.fit_poisson(LYc, grp, len(calc.COUNT_BINS) + 1)[3]
    check("L1 the street beats the plat block by 300 log-likelihood units or more", ll_street - ll_block > 300, "%.1f" % (ll_street - ll_block))
    check("L2 the canal term is required (100 units or more)", ll_street - ll_nocanal > 100, "%.1f" % (ll_street - ll_nocanal))
    # homes permitted rather than completed by 1 January
    issue_by = {}
    Pp = calc.Pack.__new__(calc.Pack)
    Pp.__dict__.update(P.__dict__)
    Pp.co = {i: (d if d is not None else None) for i, d in P.issue.items()}
    Pp.yb = P.yb.copy()
    LYp = calc.lot_years(Pp, season, "street")
    ll_perm = calc.fit_poisson(LYp, np.digitize(LYp["n"], calc.COUNT_BINS), len(calc.COUNT_BINS) + 1)[3]
    check("L3 homes completed beat homes permitted by 30 units or more", ll_street - ll_perm > 30, "%.1f" % (ll_street - ll_perm))
    gperm, _ = calc.forecast(Pp, season)
    check("SF11 a permit issued counted as a home standing: same call, 4 or more inside the bin's edge",
          printed(gperm) == gp and edge(gperm["total"], 50) >= 4, "%.1f, %.1f from the edge" % (gperm["total"], edge(gperm["total"], 50)))

    print("semantic fork table")
    pools = sum(1 for r in csv.DictReader(open(os.path.join(target, C.F_PLEG))) if r["PERMIT_TYPE"] != "RES NEW SFR")
    check("SF1 other residential permits are thousands of rows, ruled out by the work class pin",
          pools > 3000 and "Residential New Single Family" in calc.pdf_text(os.path.join(target, C.F_CONV)), "%d legacy rows" % pools)
    conv = calc.pdf_text(os.path.join(target, C.F_CONV)).replace("\n", " ")
    conv = re.sub(r"\s+", " ", conv)
    check("SF2 issue date pinned (by issue date)", "by issue date" in conv)
    check("SF3 calendar year pinned", "in the calendar year forecast" in conv)
    check("SF4 areas by the schedule's plat units, and every forward lot maps to one", "plat units the program schedule lists" in conv
          and all(len(P.areas[n]["units"]) == 3 for n in calc.FORWARD))
    lvl = printed(res["golden family: level of 2024 to 2026"])
    check("SF10 the estimand is filed as expected distinct lots", "a lot being permitted at most once" in conv)
    check("SF5 the 2024 to 2026 level files the same call, and the conventions pin 2026", lvl == gp and
          "its calendar 2026 level" in conv, str(lvl))
    sched = re.sub(r"\s+", " ", calc.pdf_text(os.path.join(target, C.F_SCHED)))
    check("SF7 service from the acceptance day is filed", "may connect from that date" in sched)
    # SF6: carried-over permits kept twice; SF8: unserved months left out
    P6 = calc.Pack.__new__(calc.Pack); P6.__dict__.update(P.__dict__)
    leg = list(csv.DictReader(open(os.path.join(target, C.F_PLEG))))
    extra = [(P.ix_addr[calc.norm_addr(r["SITE_ADDR"])], calc._mdy(r["ISSUE_DT"]), None, r["PERMIT_NBR"]) for r in leg
             if r["STATUS"] == "MIGRATED" and r["PERMIT_TYPE"] == "RES NEW SFR"]
    P6.sf_permits = P.sf_permits + extra
    g6, _ = calc.forecast(P6, calc.season_shares(P6))
    check("SF6 carried-over permits counted twice: same call", printed(g6) == gp, "%s (%d duplicates)" % (printed(g6), len(extra)))
    P8 = calc.Pack.__new__(calc.Pack); P8.__dict__.update(P.__dict__)
    orig_u = calc.unserved_rate
    calc.unserved_rate = lambda _P: 0.0
    g8, _ = calc.forecast(P8, season)
    calc.unserved_rate = orig_u
    check("SF8 permits before service left out: same call", printed(g8) == gp, str(printed(g8)))

    print("R2 every mess item neutral on the call")
    P2 = calc.Pack.__new__(calc.Pack); P2.__dict__.update(P.__dict__)
    P2.co = {i: c for i, c in P.co.items() if c is None or c < dt.date(2026, 1, 1)}
    g2, _ = calc.forecast(P2, season)
    check("R2a the 2026 certificates of occupancy ignored (roll only): same call", printed(g2) == gp, str(printed(g2)))
    spelled = set(i for r in leg if r["PERMIT_TYPE"] == "RES NEW SFR" and r["SITE_ADDR"].rsplit(" ", 1)[1] in calc.SUFFIX_ABBR
                  for i in [P.ix_addr[calc.norm_addr(r["SITE_ADDR"])]])
    P3 = calc.Pack.__new__(calc.Pack); P3.__dict__.update(P.__dict__)
    P3.sf_permits = [p for p in P.sf_permits if not (p[3].startswith("B") and p[0] in spelled)]
    P3.issue = {i: d for i, d in P.issue.items() if i not in spelled}
    P3.co = {i: d for i, d in P.co.items() if i not in spelled}
    g3, _ = calc.forecast(P3, calc.season_shares(P3))
    check("R2b legacy addresses with a spelled-out suffix left unmatched: same call", printed(g3) == gp,
          "%s (%d lots)" % (printed(g3), len(spelled)))
    check("R2c the schedule table parses to 22 areas with acceptance dates", len(P.areas) == 22 and
          all(P.areas[n]["accepted"] is not None for n in calc.FORWARD))
    check("R3c no repeated block: yearly single-family permit counts all differ", len(set(
        sum(1 for p in P.sf_permits if p[1].year == y) for y in range(2008, 2027))) == 19)

    print("asks: devices, fairness, separation")
    from utility import Utility
    u = Utility(w)
    routes = calc.connections_fy26(target, P)
    grid = routes["golden"]
    new, q = u.connections_fy26()
    PH = ["Core", "1", "2", "3", "4"]
    tot = lambda rt, ph: sum(routes[rt][(ph, k)] for k in (1, 2, 3, 4))
    exact = all(grid[(ph, k)] == int(((u.phase_now == ph) & new & (q == k - 1)).sum()) for ph in PH for k in (1, 2, 3, 4))
    check("A1 law 6: the golden handling reproduces the clean truth in every phase and quarter", exact)
    for rname in ("cracker", "reader_a", "reader_b", "reader_d", "reader_e", "reader_f", "stored_phase"):
        check("A2 every phase total missed on the %s route" % rname, all(tot(rname, ph) != tot("golden", ph) for ph in PH[1:]))
    check("A3 the second-premise device is in every phase total", all(tot("reader_d", ph) > tot("golden", ph) for ph in PH[1:]))
    roll_addr = set(r["SITE_ADDR"] for r in csv.DictReader(open(os.path.join(target, C.F_ROLL))))
    stale = [r for r in csv.DictReader(open(os.path.join(target, C.F_PREM)))
             if r["PARCEL_ID"] and int(r["PARCEL_ID"].split("-")[3][1:]) in u.renum_units]
    check("A7 the renumbered units' stubs carry house numbers the roll no longer has, and keep their parcel numbers",
          len(stale) > 1000 and not any(r["SVC_ADDR"] in roll_addr for r in stale), "%d stubs" % len(stale))
    prem_rows = list(csv.DictReader(open(os.path.join(target, C.F_PREM))))
    by_addr_raw = defaultdict(int)
    for r in prem_rows:
        by_addr_raw[r["SVC_ADDR"]] += 1
    parcels = [r["PARCEL_ID"] for r in prem_rows if r["PARCEL_ID"]]
    check("A5 silent: no parcel number repeats in the premise extract and fewer than one counter premise in five repeats "
          "its stub's address string", len(parcels) == len(set(parcels)) and
          sum(1 for v in by_addr_raw.values() if v > 1) < 0.2 * len(u.prem2), "%d repeated strings of %d" %
          (sum(1 for v in by_addr_raw.values() if v > 1), len(u.prem2)))
    check("A6 no field names the device: the premise and install headers are unchanged",
          list(prem_rows[0].keys()) == ["PREMISE_ID", "SVC_ADDR", "PARCEL_ID", "UEP_PHASE", "CREATED_DT", "PREMISE_TYPE", "STATUS"])
    check("SF12 fork closed: the conventions count a connection once per lot at its first meter (the second install reading "
          "moves totals)", D.CONN_PIN in conv)
    check("Z1 frozen: the call total equals the round 1 fix figure", abs(g["total"] - 293.225) < 0.0006)
    check("A4 the connection figures in figures.json are the golden",
          all(fig["ask_connections_fy2026_phase%s" % ph] == tot("golden", ph) for ph in PH[1:]) and
          not any(k.startswith("ask_connections") and k.endswith(("_q1", "_q2", "_q3", "_q4")) for k in fig))
    fees, lines, by_no, fx = calc.fees_fy26(target, P, extra=True)
    cells = [(ph, k) for ph in PH for k in (1, 2, 3, 4)]
    check("B4 summing receipt lines misses every phase and quarter", all(abs(lines[c] - fees[c]) > 1000 for c in cells))
    check("B5 one amount per receipt number misses every phase and quarter (first line kept)",
          all(abs(by_no[c] - fees[c]) > 1000 for c in cells))
    for nm in ("number_last", "number_amount", "number_date"):
        check("B5 the %s dedupe misses every phase and quarter" % nm, all(abs(fx[nm][c] - fees[c]) > 1000 for c in cells))
    tru = {}
    for (rno, rdate, lot, amt, total, nl, drawer) in u.receipts:
        d = C.to_date(rdate); fy, qq = C.fq(d)
        if fy == 2026:
            tru[(rno, drawer)] = ((u.phase_now[lot], qq), total)
    tq = defaultdict(float)
    for c_, v in tru.values():
        tq[c_] += v
    check("B6 law 6: one amount per payment (receipt number and payer) reproduces the cash received in every cell",
          all(abs(tq[c] - fees[c]) < 0.5 for c in cells) and len(tq) == 20)
    ph_of = defaultdict(set)
    for (rno, rdate, lot, amt, total, nl, drawer) in u.receipts:
        ph_of[(rno, drawer)].add(u.phase_now[lot])
    check("B8 every payment's permits lie in one phase", all(len(v) == 1 for v in ph_of.values()))
    check("B7 figures.json fees are the golden",
          all(fig["ask_capacity_fees_fy2026_%s_q%d" % (ph.lower() if ph == "Core" else "phase" + ph, k)] == round(fees[(ph, k)])
              for ph, k in cells))
    from pack import Identity
    to_p = np.array([P.ix[s] for s in Identity(w).strap])
    exch_lots = set(int(to_p[i]) for i in u.changeouts[0])
    check("S1 separation: no exchange sits on a lot the call forecasts", not (exch_lots & set(info["fl"].tolist())))
    prem_p = set(int(to_p[i]) for i in np.where(u.has_premise)[0])
    rec_p = set(int(to_p[r[2]]) for r in u.receipts)
    check("S2 separation: no lot the call forecasts has a premise or a capacity fee receipt",
          not (prem_p & set(info["fl"].tolist())) and not (rec_p & set(info["fl"].tolist())))

    print("documents and realism")
    check("D1 positive control: the conventions read back", D.MARKET_PIN in conv and len(conv) > 1000)
    words = re.compile(r"street|neighbo|build.?out|first home|empty|homes standing", re.I)
    check("D2 no document names the decisive relation (conventions, schedule, dictionary)",
          not words.search(conv) and not words.search(sched) and not words.search(open(os.path.join(target, C.F_DICT)).read()))
    pm = max(p[1] for p in P.sf_permits)
    check("D3 no permit after the records' end", pm <= C.RECORDS_END, str(pm))
    ami_max = max(r["INSTALL_DATE"] for r in csv.DictReader(open(os.path.join(target, C.F_AMI))))
    check("D4 the AMI log ends inside fiscal 2026", ami_max <= "2026-09-30", ami_max)
    names = set(re.findall(r"(Melissa Payne|Steven Burke)", conv + sched))
    check("D5 personas from guard.py names only", names == {"Melissa Payne", "Steven Burke"}, str(names))
    lots = [P.areas[n]["lots"] for n in P.areas]
    check("D6 realism: no two areas share a lot count", len(set(lots)) == len(lots))

    print("distractors deleted: the golden and every ask unchanged")
    tmp = tempfile.mkdtemp(prefix="t175_dis_")
    try:
        for f in files:
            if f not in [d.split("/", 1)[1] for d in dis]:
                shutil.copy(os.path.join(target, f), tmp)
        Pd = calc.Pack(tmp)
        gd, _ = calc.forecast(Pd)
        gr2 = calc.connections_fy26(tmp, Pd)["golden"]
        fd = calc.fees_fy26(tmp, Pd)[0]
        check("X1 the call unchanged without the distractors", printed(gd) == gp)
        check("X2 the asks unchanged without the distractors", gr2 == grid and fd == fees)
    finally:
        shutil.rmtree(tmp)

    print("\n%d checks passed, %d failed" % (N_OK[0], len(FAILS)))
    if FAILS:
        print("FAILED: " + "; ".join(FAILS))
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
