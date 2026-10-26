"""The generator's assertions on the cut pack and the clean truth: the input gates, the realism sweep, the three rules
(R1 to R3), the Layer 1 items, the ladder, both families, the semantic fork rows (SF1 to SF10), the separation of the
ask from the call, the fairness of the ask's devices and the context table's recomputation.

    python3 task485/generator/checks.py
"""
import collections
import csv
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import ceiling as C   # noqa: E402
import golden as G    # noqa: E402
import metadata as M  # noqa: E402
import world as W     # noqa: E402

D = dt.date
RESULTS = []
GOLD_SET = ["DIG", "FIN", "HOS"]
DEFAULT_SET = ["CON", "DIG", "FIN", "HOS", "HSC", "RET"]


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %-58s %s" % ("PASS" if ok else "FAIL", label, detail))


def clean_truth(w):
    """the world's own stays with every departure to the cut known (no late notice, no system move), cut into rows the
    golden's functions read"""
    rows = []
    for s in w.stays:
        rows.append(dict(reg=str(s.pid), ref="w%d" % id(s), origin="ARRIVAL", arrive=s.arrive, registered=s.registered,
                         code=s.code, sector=s.sector, parish=s.parish, sex=w.people[s.pid]["sex"], yob=1990,
                         nat=w.people[s.pid]["nat"], leave=s.leave if s.leave <= W.CUT else None, notice=None))
    return rows


class RowsPack(G.Pack):
    def __init__(self, base, rows):
        self.__dict__.update({k: v for k, v in base.__dict__.items() if k not in ("cur", "by_reg")})
        self.cur = rows
        self.by_reg = collections.defaultdict(list)
        for r in rows:
            self.by_reg[r["reg"]].append(r)


def main():
    P = G.Pack()
    R = G.routes(P)
    gold = R["golden"]
    files = sorted(os.listdir(TARGET))

    # ---------------------------------------------------------------- input gates
    check("gate: 10 or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {os.path.splitext(f)[1] for f in files}
    check("gate: 3 or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(TARGET, f), "rb")) - 1 for f in files if f.endswith(".csv"))
    check("gate: a file of 25,000 rows or more", big >= 25000, "%d rows" % big)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("gate: two or more distractors named", len(meta["distractor_files"]) >= 2, ", ".join(meta["distractor_files"]))
    check("gate: every file has a source, date and licence", set(M.SOURCES) == set(files))
    check("gate: no file name names the step", not any(re.search(r"return|circular|history|duplicate|transfer", f)
                                                       for f in files))

    # ---------------------------------------------------------------- the call, the ladder and both families
    check("call: golden designates the three", G.designated(gold) == GOLD_SET, ",".join(G.designated(gold)))
    check("ladder L0 every arrival counted: all eight", len(G.designated(R["every_arrival"])) == 8)
    check("ladder L1 resolved stays only: none", G.designated(R["resolved_only"]) == [])
    check("ladder L2 every open stay counted long: seven", G.designated(R["open_counted_long"]) ==
          ["AGR", "CON", "DIG", "FIN", "HOS", "HSC", "RET"])
    check("ladder L3 default path: the six", G.designated(R["sector_months"]) == DEFAULT_SET)
    check("ladder L2b the sector's share of all arrivals: four", G.designated(R["flat_sector"]) ==
          ["CON", "DIG", "FIN", "HSC"])
    check("ladder L2c the share of all arrivals by sector and history: two", G.designated(R["flat_sector_history"]) ==
          ["DIG", "FIN"])
    for k in G.EASY:
        check("easy family %s files the default set" % k, G.designated(R[k]) == DEFAULT_SET)
    for k in G.STANDING:
        check("standing family %s files the golden set" % k, G.designated(R[k]) == GOLD_SET)
    sm = min(abs(R[k][s] - G.ALLOWANCE[s]) for k in G.STANDING for s in P.sectors)
    check("standing family at least 12 persons from every allowance", sm >= 12.0, "%.1f" % sm)
    em = min(R[k][s] - G.ALLOWANCE[s] for k in G.EASY for s in ("CON", "HSC", "RET"))
    check("easy family at least 11 persons over on the three flipped sectors", em >= 11.0, "%.1f" % em)
    spread = max(max(R[k][s] for k in G.STANDING) - min(R[k][s] for k in G.STANDING) for s in P.sectors)
    check("standing family spread on any sector", spread <= 16.0, "%.1f persons" % spread)
    for s in ("CON", "HSC", "RET"):
        check("decisive gap %s: default over golden by 25 or more" % s, R["sector_months"][s] - gold[s] >= 25,
              "%.1f" % (R["sector_months"][s] - gold[s]))

    # ---------------------------------------------------------------- R1, R2 and R3
    multi = sum(1 for v in P.by_reg.values() if len(v) > 1)
    check("R1 the register ships person by stay, with repeat stays", multi > 1000, "%d people with two or more stays" % multi)
    heads = open(os.path.join(TARGET, "population_register_extract_20260930.csv")).readline()
    check("R1 no shipped column holds the history or the outcome",
          not re.search(r"return|previous|history|long_term|outcome|months", heads), heads.strip())
    late = [dict(r, leave=None, notice=None) if (r["notice"] and r["notice"] > G.CUT) else r for r in P.cur]
    Pl = RowsPack(P, late)
    check("R2 notices received after the cut dropped: same call", G.designated(G.golden(Pl)) == GOLD_SET)
    regd = [dict(r, arrive=r["registered"]) if r["origin"] == "ARRIVAL" else r for r in P.cur]
    Pr = RowsPack(P, regd)
    check("R2 SF1 year by registration date: same call", G.designated(G.golden(Pr)) == GOLD_SET)
    arcdate = {}
    for a in P.arc:
        if a["closure"] == "TRANSFERRED":
            arcdate[P.xw[a["legacy"]]] = a["arrive"]
    tr = [dict(r, arrive=arcdate[r["reg"]]) if r["origin"] == "TRANSFER" else r for r in P.cur]
    check("R2 TRANSFER arrival dates from the archive: same call", G.designated(G.golden(RowsPack(P, tr))) == GOLD_SET)
    check("R2 every code resolves to one 2026 sector (SF5)", all(r["sector"] in P.sectors for r in P.cur))
    w = W.build()
    truth_rows = clean_truth(w)
    Pt = RowsPack(P, truth_rows)
    check("R3a analyst test on the clean truth files the default set",
          G.designated(G.completion(Pt, lambda r, m: (r["sector"], m))) == DEFAULT_SET)
    check("R3b the decisive step alone on the clean truth files the golden",
          G.designated(G.completion(Pt, lambda r, m: (r["sector"], Pt.history(r), m))) == GOLD_SET)
    for k in ("every_arrival", "resolved_only", "open_counted_long", "sector"):
        check("R3b lower rung %s stays wrong" % k, G.designated(R[k]) != GOLD_SET)
    true_long = collections.Counter(s.sector for s in w.stays if G.in_year(s.arrive, G.Y25) and s.long())
    check("truth: the world's own outcomes designate the golden set",
          sorted(s for s in P.sectors if true_long[s] > G.ALLOWANCE[s]) == GOLD_SET,
          " ".join("%s %d" % (s, true_long[s]) for s in P.sectors))

    # ---------------------------------------------------------------- semantic forks
    yr = [r for r in P.cur]
    a365 = G.completion(P, lambda r, m: (r["sector"], P.history(r), m))
    check("SF2 365 days for twelve months: same call", _days365(P) == GOLD_SET)
    check("SF3 notices by 31 August only: same call", G.designated(G.golden(Pl)) == GOLD_SET)
    chains = _chains(P)
    check("SF4 stays joined across breaks: another set", chains != GOLD_SET, ",".join(chains))
    check("SF6 the 2023-25 arrivals as the year before: same call",
          G.designated(G.completion(P, lambda r, m: (r["sector"], P.history(r), m),
                                    ref=P.cohort(G.Y23) + P.cohort(G.Y24))) == GOLD_SET)
    pub = {s: 50 * int(gold[s] / 50.0 + 0.5) for s in P.sectors}
    check("SF7 the published figures compared: same call",
          sorted(s for s in P.sectors if pub[s] > G.ALLOWANCE[s]) == GOLD_SET)
    check("SF8 no sector at its allowance", all(abs(a365[s] - G.ALLOWANCE[s]) > 1 for s in P.sectors))
    check("SF9 every record registered for work carries an activity", all(r["code"] for r in yr))
    c2426 = P.cohort(G.Y24) + P.cohort(G.Y25)
    check("SF10 no TRANSFER record among the 2024-26 arrivals",
          not any(r["origin"] == "TRANSFER" and (G.in_year(r["arrive"], G.Y24) or G.in_year(r["arrive"], G.Y25))
                  for r in P.cur))
    check("SF1 the year by arrival date: every cohort record dated", all(r["arrive"] for r in c2426))

    # ---------------------------------------------------------------- the ask: separation, fairness, devices
    check("separation: every history stay for 2024-26 ends after the move",
          all(o["leave"] is None or o["leave"] > W.MOVE or (r["arrive"] - o["leave"]).days > 365
              for r in c2426 for o in P.by_reg[r["reg"]] if o is not r))
    check("separation: no archive record is a 2024-26 arrival", not any(a["arrive"] >= G.Y24[0] for a in P.arc))
    A, B = G.back_series(P)
    truthA, truthB = {}, {}
    for y in G.BACK_YEARS:
        win = (D(y, 7, 1), D(y + 1, 6, 30))
        truthA[y] = collections.Counter(s.sector for s in w.stays if G.in_year(s.arrive, win))
        truthB[y] = collections.Counter(s.sector for s in w.stays if G.in_year(s.arrive, win) and
                                        (s.leave > W.CUT or s.leave >= G.anniversary(s.arrive)))
    check("ask fair: the golden arrivals are the world's own count",
          all(A[y][s] == truthA[y][s] for y in G.BACK_YEARS for s in P.sectors))
    check("ask fair: the golden long-term figures are the world's own count",
          all(B[y][s] == truthB[y][s] for y in G.BACK_YEARS for s in P.sectors))
    gold_b, keeps = C.measure(P)
    check("ask: the cracker keeps 2 or fewer of 80", keeps["cracker"] <= 2, "%d" % keeps["cracker"])
    check("ask: no handling but the golden keeps more than 12 of 80", max(keeps.values()) <= 12, json.dumps(keeps))
    twins = sum(1 for s in w.stays if s.dup_registered)
    stays = G.back_stays(P)
    recs = G.back_stays(P, "archive_stitched")
    check("ask device: twin records the golden counts once", twins > 600, "%d stays registered twice" % twins)
    tr_twins = sum(1 for s in w.stays if s.dup_registered and s.transferred())
    check("ask device: twins on both sides of the move", tr_twins > 150 and twins - tr_twins > 300,
          "%d carried across the move" % tr_twins)
    check("ask device: one current number for each legacy number", len(set(P.xw.values())) == len(P.xw))
    key = collections.Counter()
    for s in w.stays:
        if s.registered < W.MOVE and s.leave <= W.CUT and s.notice <= W.EXTRACT:
            p = w.people[s.pid]
            key[(s.arrive, p["sex"], p["nat"], s.code, s.leave, s.notice, s.pid)] += 1
    by_twin = collections.Counter((k[0], k[1], k[2], k[3], k[4], k[5]) for k in key)
    check("ask fair: no two people share a stay's declared particulars, leaving date and notice date",
          all(v == 1 for v in by_twin.values()), "%d keys" % len(by_twin))
    still = collections.Counter()
    trn = {r["reg"]: r for r in P.cur if r["origin"] == "TRANSFER"}
    for a in P.arc:
        t = None if a["closure"] == "LEFT" else trn.get(P.xw[a["legacy"]])
        if t is not None and t["leave"] is None:
            still[(a["arrive"], a["sex"], a["yob"], a["nat"], a["code"])] += 1
    check("ask fair: no two legacy records still open at the extract share every declared particular",
          all(v == 1 for v in still.values()), "%d open records" % sum(still.values()))
    for how in ("open_pairs_once", "leave_only"):
        check("ask fair: counting once the records alike %s files the golden back series" %
              ("in their particulars and open together" if how == "open_pairs_once" else
               "in their particulars and leaving date, whatever the notice"),
              G.back_series(P, how) == G.back_series(P))
    same_day = collections.Counter()
    for s in w.stays:
        if s.registered < W.MOVE:
            p = w.people[s.pid]
            same_day[(s.arrive, p["sex"], p["nat"], s.code, int(p["age"]))] += 1
    check("ask device: genuine people alike in every declared particular (the over-cleaning half)",
          sum(v - 1 for v in same_day.values() if v > 1) > 150, "%d" % sum(v - 1 for v in same_day.values() if v > 1))
    tdiff = sum(1 for r in P.cur if r["origin"] == "TRANSFER" and r["reg"] in arcdate and r["arrive"] != arcdate[r["reg"]])
    check("ask hazard: TRANSFER arrival dates are the legacy registration dates", tdiff > 5000, "%d" % tdiff)
    for y in G.BACK_YEARS:
        vals = [B[y][s] for s in P.sectors]
        check("realism: back series %d has eight distinct counts" % y, len(set(vals)) == 8, str(vals))
    del stays, recs

    # ---------------------------------------------------------------- the filed back-test (methods note 3.3)
    bt = G.backtests(P)
    sets = {k: G.designated(R[k]) for k in bt}
    same = [k for k in bt if sets[k] == GOLD_SET]
    other = [k for k in bt if sets[k] != GOLD_SET]
    best_same = min(bt[k][0] for k in same)
    best_other = min(bt[k][0] for k in other)
    check("SF11 the filed test's best candidate designates the golden set, 0.01 ahead of any other set",
          best_other - best_same >= 0.01, "%.4f against %.4f (%s)" % (best_same, best_other,
                                                                     min(other, key=lambda k: bt[k][0])))
    check("SF11 the golden scores within 0.001 of the best candidate", bt["golden"][0] - best_same <= 0.001,
          "%.4f" % bt["golden"][0])
    win = {}
    for w in (61, 122, 183, 274, 335, 365, 396, 456, 548, 730, 99999):
        win[w] = (G.backtest(P, lambda r, m, w=w: (r["sector"], P.history(r, w), m))[0],
                  G.designated(G.completion(P, lambda r, m, w=w: (r["sector"], P.history(r, w), m))))
    check("SF11 every history window from 61 days to any earlier stay files the golden set",
          all(v[1] == GOLD_SET for v in win.values()))
    check("SF11 the 335 to 396 day windows tie at the test's optimum over the windows",
          max(win[w][0] for w in (335, 365, 396)) - min(v[0] for v in win.values()) < 1e-12,
          "%.5f" % win[365][0])

    # ---------------------------------------------------------------- the context table and the realism sweep
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TARGET, "long_term_immigration_by_sector_2023_24.xlsx"))
    ws = wb["Table 1"]
    pubt = {r[0].value: (r[2].value, r[3].value) for r in ws.iter_rows(min_row=5, max_row=12)}
    mine = {}
    for r in P.cohort(G.Y23):
        if r["registered"] > D(2025, 9, 30):
            continue
        known = r["leave"] is not None and r["notice"] <= D(2025, 9, 30)
        lg = (not known) or r["leave"] >= G.anniversary(r["arrive"])
        a, b = mine.get(r["sector"], (0, 0))
        mine[r["sector"]] = (a + 1, b + lg)
    check("context: the published 2023-24 table recomputes at its own cut", all(pubt[s] == mine[s] for s in P.sectors),
          json.dumps(pubt))
    refs = [r["ref"] for r in P.cur]
    check("realism: one row per stay in the current extract", len(refs) == len(set(refs)))
    check("realism: no arrival after the cut", all(r["arrive"] <= G.CUT for r in P.cur))
    check("realism: no leaving date after the cut", all(r["leave"] is None or r["leave"] <= G.CUT for r in P.cur))
    check("realism: no notice after the extract", all(r["notice"] is None or r["notice"] <= W.EXTRACT for r in P.cur))
    check("realism: ARRIVAL registrations on or after arrival and the move",
          all(r["registered"] >= r["arrive"] and r["registered"] >= W.MOVE for r in P.cur if r["origin"] == "ARRIVAL"))
    check("realism: TRANSFER records registered on the move", all(r["registered"] == W.MOVE for r in P.cur
                                                                   if r["origin"] == "TRANSFER"))
    check("realism: no registration after the extract", all(r["registered"] <= W.EXTRACT for r in P.cur))
    check("realism: nobody registered after the stay ended",
          all(r["leave"] is None or r["registered"] < r["leave"] for r in P.cur if r["origin"] == "ARRIVAL") and
          all(a["registered"] < a["leave"] for a in P.arc if a["closure"] == "LEFT"))
    check("realism: the legacy register holds nothing registered after it closed", all(a["registered"] < W.MOVE
                                                                                       for a in P.arc))
    check("realism: TRANSFER arrival dates fall before the move", all(r["arrive"] < W.MOVE for r in P.cur
                                                                       if r["origin"] == "TRANSFER"))
    by_sector_year = collections.Counter((r["sector"], r["arrive"].year) for r in P.cur if r["origin"] == "ARRIVAL")
    vals = list(by_sector_year.values())
    check("realism: no repeated sector-year arrival count block", len(vals) - len(set(vals)) <= len(vals) // 3)
    from pypdf import PdfReader
    texts = " ".join(p.extract_text() for f in files if f.endswith(".pdf")
                     for p in PdfReader(os.path.join(TARGET, f)).pages)
    texts = " ".join(texts.split())
    check("realism: personas from the guard draw in the documents",
          all(n in texts for n in ("Jean Grant", "Gordon Hope", "Melanie Hilton")), "Jean Grant, Gordon Hope, Melanie Hilton")
    check("leak: no document names returns or circular work", not re.search(r"circular|returner|re-plac|agenc",
                                                                            texts, re.I))
    lag = [(r["registered"] - r["arrive"]).days for r in P.cur if r["origin"] == "ARRIVAL"]
    check("realism: registration lags vary", len(set(lag)) > 30, "%d distinct lags" % len(set(lag)))
    del texts
    n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
    print("%d checks, %d FAIL" % (len(RESULTS), n_fail))
    return n_fail


def _days365(P):
    """the golden with a stay long-term when it lasts 365 days or more"""
    save = G.anniversary
    G.anniversary = lambda a: a + dt.timedelta(days=365)
    try:
        return G.designated(G.golden(P))
    finally:
        G.anniversary = save


def _chains(P):
    """the reading that joins a person's stays across breaks of under a year: a return is no new arrival, and a
    chain's length runs from its first arrival to its last departure"""
    rows = []
    for reg, v in P.by_reg.items():
        v = sorted(v, key=lambda r: r["arrive"])
        cur = None
        for r in v:
            if cur is not None and cur["leave"] is not None and (r["arrive"] - cur["leave"]).days <= 365:
                cur["leave"] = r["leave"]
                continue
            if cur is not None:
                rows.append(cur)
            cur = dict(r)
        rows.append(cur)
    Pc = RowsPack(P, rows)
    return G.designated(G.completion(Pc, lambda r, m: (r["sector"], m)))


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
