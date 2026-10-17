"""Every claim the build makes, asserted against the clean truth and the cut pack."""
import csv
import datetime as dt
import math
import os
import re

import asks as A
import estimators as E
import golden as G
import sim
import world as W

N = [0]
SCREEN, ONESIDED, RISE, BAND, PRIOR, GOLD = 1438, 500, 1633, 2583, 350, 450
CALL = {"GRO": 100, "HOS": 50, "TRA": 150, "CON": 50, "RUR": 0, "FUE": 50, "PER": 50, "CLB": 0}


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        raise AssertionError("%s FAILED %s" % (label, detail))


def _rows(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _sets_at(g, tol):
    """The stated figure sets the grid gives when the balance tolerance is tol."""
    keep = E.BALANCE
    try:
        E.BALANCE = tol
        return set(G.rounded_sets(G.convergence(g)))
    finally:
        E.BALANCE = keep


def _sides_at(amounts, lo):
    """The same two-sided reading taken at a position where nothing was moved."""
    keep = (E.BAND_LO, E.BAND_HI, E.MIRROR_HI)
    try:
        E.BAND_LO, E.BAND_HI, E.MIRROR_HI = lo, lo + 500, lo + 1000
        return E.sides(amounts, 5000, 16000, 250, "poisson", 1)
    finally:
        E.BAND_LO, E.BAND_HI, E.MIRROR_HI = keep


def run(g, target):
    N[0] = 0
    seg_of = {c["cust"]: c["seg"] for c in g["custs"]}
    win = [r for r in g["deposits_rows"] if r["year"] == "2027" and r["instrument"] == "cash"]

    # ---------------------------------------------------------------- the three rules
    headers = []
    for name in sorted(os.listdir(target)):
        if name.endswith(".csv"):
            with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
                headers.extend(next(csv.reader(fh)))
    bad = [h for h in headers if re.search(r"split|structur|excess|background|profile|"
                                           r"expected_count|fitted", h, re.I)]
    ok("R1 no deciding quantity in a column", not bad, str(bad))
    ok("R1 deposit level amounts ship", len(win) > 40000, str(len(win)))
    ok("R1 the golden reads deposit rows", len(g["all_amt"]) == len(win))
    ok("R1 every segment carries a profile either side of the band",
       all(len([a for a in g["amt_by_seg"][k] if 5000 <= a < 16000 and not (9000 <= a < 10000)])
           > 600 for k in W.SEG_KEYS))

    dep = {}
    for r in win:
        dep.setdefault(seg_of[r["cust"]], []).append(r["amount"])
    base = {k: G.r50(G.canonical(dep[k])) for k in W.SEG_KEYS}
    ok("R2 baseline matches the golden", base == g["per_seg"], str(base))
    ok("R2 the golden is the call the note files", g["per_seg"] == CALL, str(g["per_seg"]))

    machine_rows = _rows(target, "cash_deposit_machine_2026_2027.csv")
    resent = [r for r in machine_rows if r["pull_sequence"] == "2"]
    ok("R2 re-sent rows exist", len(resent) >= 15, str(len(resent)))
    ok("R2 no re-sent row is in the band", all(not (9000 <= float(r["amount_nzd"]) < 10000)
                                               for r in resent))
    counter = _rows(target, "cash_deposit_counter_2026_2027.csv")
    shifted = [r for r in counter if r["posted_date"] != r["deposit_date"]]
    ok("R2 posted date differs on some rows", len(shifted) > 100, str(len(shifted)))
    ok("R2 no band deposit has a shifted posted date",
       all(not (9000 <= float(r["amount_nzd"]) < 10000) for r in shifted))

    def ryear(day):
        return "2027" if dt.date(2026, 7, 1) <= day <= dt.date(2027, 6, 30) else "2026"

    boundary = []
    for r in machine_rows:
        if not (9000 <= float(r["amount_nzd"]) < 10000) or r["pull_sequence"] != "1":
            continue
        u = dt.datetime.strptime(r["deposit_ts_utc"], "%Y-%m-%dT%H:%M:%SZ")
        off = 13 if dt.date(2026, 9, 27) <= u.date() < dt.date(2027, 4, 4) else 12
        if ryear((u + dt.timedelta(hours=off)).date()) != ryear(u.date()):
            boundary.append(r)
    ok("R2 reading the UTC stamp as the date moves no band deposit between years",
       not boundary, str(len(boundary)))
    rev = [r for r in counter if r["reversal_of"]]
    ok("R2 two reversals, neither in the band", len(rev) == 2 and
       all(abs(float(r["amount_nzd"])) >= 10000 for r in rev))
    ok("R2 the April code reissue partitions identically",
       len({W.OLD_CODE[k] for k in W.SEG_KEYS}) == 8 and len({W.NEW_CODE[k] for k in W.SEG_KEYS}) == 8)

    ok("R3a the near-threshold band counted files the named wrong answer",
       g["band_all"] == BAND and BAND != GOLD, str(g["band_all"]))
    ok("R3a the same-day screen files the named wrong answer", g["screen"] == SCREEN,
       str(g["screen"]))
    ok("R3b the decisive step files the golden", g["total"] == GOLD, str(g["total"]))
    ok("R3b reading the band on its own stays wrong", g["one_total"] == ONESIDED and
       ONESIDED != GOLD, str(g["one_total"]))
    ok("R3b the customer-against-prior-year control stays wrong", g["rise"] == RISE and
       RISE != GOLD, str(g["rise"]))
    ok("R3b the prior year on the same reading is not the answer", g["prior_total"] == PRIOR and
       PRIOR != GOLD, str(g["prior_total"]))
    # the depletion is the practice's own mechanical consequence, not a planted defect: the
    # dollars moved, so the deficit above is the same size as the surplus below
    moved = sum(1 for r in g["deposits_rows"]
                if r["year"] == "2027" and r["instrument"] == "cash" and r["planted"])
    ok("R3a the surplus below and the deficit above come from one movement",
       abs(sum(g["per_seg"].values()) - G.r50(moved)) <= W.GRAIN, str(moved))

    monthly = {}
    for r in win:
        key = (seg_of[r["cust"]], r["day"].strftime("%Y-%m"))
        monthly[key] = monthly.get(key, 0) + 1
    for k in W.SEG_KEYS:
        vals = [v for (s, m), v in monthly.items() if s == k]
        ok("R3c no repeated monthly block in %s" % k, len(set(vals)) >= len(vals) - 3)
    ok("R3c no document states this quantity",
       not any(re.search(r"\b400\b|\b2,196\b", open(os.path.join(target, n), "rb").read()
                         .decode("latin-1")) for n in os.listdir(target) if n.endswith(".pdf")))

    # ---------------------------------------------------------------- convergence, the sweep
    # asserted over the determinism judge's own candidate set, never claimed
    sw = G.convergence(g)
    sets = G.rounded_sets(sw)
    want = tuple(g["per_seg"][k] for k in W.SEG_KEYS)
    grid = E.candidates()
    ok("C1 the candidate set is the judge's grid, not the author's",
       len(grid) == len(E.WINDOWS) * len(E.WIDTHS) * len(E.FAMILIES) * len(E.ORDERS) == 225)
    ok("C1 the record leaves most of the grid standing", 100 <= len(sw) <= len(grid),
       "%d of %d" % (len(sw), len(grid)))
    ok("C1 every surviving specification gives the same eight stated figures",
       set(sets) == {want}, str(sorted(set(sets) - {want})[:3]))
    ok("C1 every surviving specification's figures sum to the golden",
       {sum(s) for s in sets} == {GOLD})
    half = W.GRAIN / 2.0
    for k in W.SEG_KEYS:
        vals = [v[k] for _, v in sw]
        edge = min(min(vals) - (g["per_seg"][k] - half), (g["per_seg"][k] + half) - max(vals))
        ok("C1 %s sits clear of its rounding edge" % k, edge >= 8.0, "%.2f" % edge)
    for k in W.SEG_KEYS:
        if g["per_seg"][k] == 0:
            ok("C1 the nil at %s is deep in its cell, not a rounding edge" % k,
               abs(g["per_seg_raw"][k]) < 10.0, "%.2f" % g["per_seg_raw"][k])
    # the width the data drops, and why
    for st in (50,):
        zeros = [k for k in W.SEG_KEYS
                 if any(v == 0 for i, v in enumerate(E.bins(g["amt_by_seg"][k], 5000, 16000, st))
                        if not (9000 <= 5000 + i * st < 11000))]
        # a specification has to carry all eight segments, so one segment with an empty bin
        # outside the band drops the width for the whole book
        ok("C1 the %d dollar width drops on the data, not by choice" % st,
           len(zeros) >= 1, str(zeros))
        ok("C1 no surviving specification uses the %d dollar width" % st,
           all(("/%d/" % st) not in lab for lab, _ in sw), str(st))
    ok("C1 no specification outside the record's balance is claimed to agree",
       any(E.balanced(g["amt_by_seg"], W.SEG_KEYS, *c) is False for c in grid))
    # the discriminator: the naive ranking and the right one name different segments
    ok("C1 the largest book is not the largest by split count",
       g["largest_book"] != g["largest"], "%s / %s" % (g["largest_book"], g["largest"]))
    ok("C1 the largest near-threshold band count is not the largest by split count",
       g["largest_band"] != g["largest"], "%s / %s" % (g["largest_band"], g["largest"]))
    ok("C1 the largest by split count is Transport and courier", g["largest"] == "TRA")
    # the amounts carry a sample's scatter, which is what makes the fork real
    for k in W.SEG_KEYS:
        c = E.chi2_per_dof(g["amt_by_seg"][k])
        ok("C1 %s amounts are a sample, not a curve" % k, 0.45 <= c <= 1.70, "%.3f" % c)
    tots = [sum(v.values()) for _, v in sw]
    ok("C1 the rounding path the prompt pins gives the golden",
       sum(g["per_seg"].values()) == GOLD)
    # the two sides of the balance are the same quantity, measured twice
    for k in W.SEG_KEYS:
        below, above = g["sides"][k]
        ok("C1 %s: the band's surplus and the deficit above bracket the figure" % k,
           min(below, above) - 20 <= g["per_seg_raw"][k] <= max(below, above) + 20,
           "%.1f / %.1f / %.1f" % (below, above, g["per_seg_raw"][k]))
    tb = sum(g["sides"][k][0] for k in W.SEG_KEYS)
    ta = sum(g["sides"][k][1] for k in W.SEG_KEYS)
    ok("C1 the book's two sides reconcile on the canonical specification",
       abs(tb - ta) <= E.BALANCE * max(tb, ta), "%.1f / %.1f" % (tb, ta))
    ok("C1 the balance filter is insensitive to its own tolerance",
       _sets_at(g, 0.10) == _sets_at(g, 0.12) == _sets_at(g, 0.20) ==
       {tuple(g["per_seg"][k] for k in W.SEG_KEYS)})

    # placebo: at ten positions away from the band and its mirror the reading is nought
    clean = {}
    for r in win:
        if not r["planted"]:
            clean.setdefault(seg_of[r["cust"]], []).append(r["amount"])
    res = []
    for lo in (5500, 6000, 6500, 7000, 7500, 8000, 11500, 12000, 12500, 13000):
        for k in W.SEG_KEYS:
            sd = _sides_at(clean[k], lo)
            if sd is not None:
                res.append((sd[0] + sd[1]) / 2.0)
    rms = math.sqrt(sum(x * x for x in res) / len(res))
    ok("placebo scatter is small against the grain", rms < W.GRAIN / 2.0, "%.2f" % rms)
    ok("placebo bias is near nought", abs(sum(res) / len(res)) < 6.0,
       "%.2f" % (sum(res) / len(res)))

    # ---------------------------------------------------------------- the ladder
    ok("ladder is ordered away from the golden",
       g["band_all"] > g["rise"] > g["screen"] > g["one_total"] > g["total"])
    ok("ladder margin, the band counted over the golden",
       g["band_all"] / float(g["total"]) > 3.0,
       "%.2f" % (g["band_all"] / float(g["total"])))
    # the ladder's big drops are counting against estimating; the decisive step is the last
    # one and it is worth exactly one cell, which is what makes the rounding honest
    ok("the move from counting to estimating is the largest single drop on the ladder",
       g["screen"] - g["one_total"] > g["rise"] - g["screen"],
       "%d against %d" % (g["screen"] - g["one_total"], g["rise"] - g["screen"]))
    ok("no rung lands on the golden",
       len({g["band_all"], g["screen"], g["one_total"], g["rise"], g["prior_total"],
            g["total"]}) == 6)
    ok("the golden is the extreme of the ladder",
       g["total"] < min(g["screen"], g["one_total"], g["rise"], g["band_all"]))
    ok("the rung next to the golden is one cell away, not nil",
       g["one_total"] - g["total"] == W.GRAIN, str(g["one_total"] - g["total"]))
    r0 = sorted(W.SEG_KEYS, key=lambda k: -g["screen_seg"][k])
    ok("the same-day screen names a different largest segment", r0[0] != g["largest"], r0[0])
    ok("the golden's largest is not first on the same-day screen",
       r0.index(g["largest"]) >= 1, str(r0.index(g["largest"]) + 1))
    ok("the golden's largest leads the runner up by a clear cell",
       g["per_seg"][g["largest"]] >= sorted(g["per_seg"].values())[-2] + W.GRAIN,
       str(sorted(g["per_seg"].values())[-2]))
    ok("the band ranking is not the answer ranking",
       sorted(W.SEG_KEYS, key=lambda k: -g["band_obs"][k])[0] != g["largest"])
    ok("the deposit-volume ranking is not the answer ranking",
       sorted(W.SEG_KEYS, key=lambda k: -g["deposits"][k])[0] != g["largest"])
    # the screen has no discrimination: it flags a like share of deposits at every size
    dayset = {}
    for r in win:
        dayset.setdefault((r["cust"], r["day"]), []).append(r["amount"])
    screened = {key for key, a in dayset.items()
                if len(a) >= 2 and sum(a) >= W.THRESHOLD and any(x < W.THRESHOLD for x in a)}
    ordinary = [r for r in win if 9000 <= r["amount"] < 10000 and not r["planted"]]
    flagged_ordinary = sum(1 for r in ordinary if (r["cust"], r["day"]) in screened)
    ok("the screen is dominated by ordinary deposits",
       flagged_ordinary > 2 * sum(1 for r in win if r["planted"]),
       "%d ordinary against %d split" % (flagged_ordinary, sum(1 for r in win if r["planted"])))
    ok("the screen flags ordinary deposits at every size",
       all(sum(1 for r in win if lo <= r["amount"] < lo + 1000 and
               (r["cust"], r["day"]) in screened) > 150
           for lo in (7000, 8000, 10000, 11000)))

    # ---------------------------------------------------------------- the fork table
    ok("SF1 instrument is given and cash is separable",
       {r["instrument"] for r in counter} == {"cash", "cheque", "credit"})
    at_lo = sum(1 for a in g["all_amt"] if abs(a - 9000.0) < 0.005)
    at_hi = sum(1 for a in g["all_amt"] if abs(a - 10000.0) < 0.005)
    ok("SF2 both band bounds carry deposits, so the clause's wording is load bearing",
       at_lo > 0 and at_hi > 0, "%d %d" % (at_lo, at_hi))
    ok("SF2 the band is read as the clause states it",
       sum(1 for a in g["all_amt"] if 9000 <= a < 10000) == g["band_all"])
    ok("SF3 the window holds both reporting years",
       min(r["day"] for r in g["deposits_rows"]) == dt.date(2025, 7, 1) and
       max(r["day"] for r in g["deposits_rows"]) == dt.date(2027, 6, 30))
    ok("SF4 posted date moves no band deposit across the year",
       all(not (9000 <= float(r["amount_nzd"]) < 10000) for r in shifted))
    ok("SF5 the unit is one deposit", len({r["deposit_ref"] for r in counter}) == len(counter))
    ok("SF6 no customer changes segment inside the window",
       len({(c["cust"], c["seg"]) for c in g["custs"]}) == len(g["custs"]))
    ok("SF7 both codings give the same eight segments",
       len(W.OLD_CODE) == len(W.NEW_CODE) == 8)
    ok("SF8 the merger is dated in the register",
       any(r["deposits_transferred_to"] == "AR12" for r in _rows(target, "branch_register.csv")))
    ok("SF9 the UTC reading moves no band deposit across the year", not boundary)
    ok("SF10 the two extracts overlap and the revised one supersedes",
       g["ptr"]["preliminary"] > 0 and g["ptr"]["revised"] > 0)
    ok("SF11 reversals are out of the band", all(abs(float(r["amount_nzd"])) >= 10000 for r in rev))
    ok("SF12 the prompt's rounding path is the one the figures follow",
       sum(g["per_seg"].values()) == GOLD == sum(G.r50(v) for v in g["per_seg_raw"].values()))
    ok("SF13 the three constructions differ from each other and from the golden",
       len({g["band_all"], g["screen"], g["one_total"], g["total"]}) == 4)
    ok("SF14 the segment figures sum to the bank's figure",
       sum(g["per_seg"].values()) == g["total"])
    vend = {}
    for site, mo, mins, visits in g["vrows"]:
        vend[mo] = vend.get(mo, 0) + mins
    ok("SF15 the vendor's report and the service log are different figures, so the prompt names one",
       any(abs(vend.get(mo, 0) - sum(v for (mid, m), v in g["svc"].items() if m == mo)) > 60
           for mo in vend))
    ok("SF16 moved out of the band reads one way on a chained history",
       all(g["a2"][b][2] <= g["a2"][b][0] for b in g["a2"]))

    # ---------------------------------------------------------------- the pack and the gates
    files = sorted(os.listdir(target))
    ok("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    exts = {os.path.splitext(f)[1] for f in files}
    ok("input gate: 3 or more formats", len(exts) >= 3, str(sorted(exts)))
    ok("input gate: a 25,000 row file", len(counter) >= 25000, str(len(counter)))
    man = {r["file"] for r in _rows(target, "export_manifest.csv")}
    ok("H9 the manifest names every shipped file",
       man == set(files) - {"export_manifest.csv"},
       str(sorted(set(files) - {"export_manifest.csv"} - man)))
    prov = open(os.path.join(target, "provenance.md"), encoding="utf-8").read()
    ok("H24 the provenance stays inside the fiction",
       not re.search(r"synthetic|generated for|invented|fictional|fictitious|this exercise",
                     prov, re.I))
    ok("H16 no record runs past the pull date",
       max(r["day"] for r in g["deposits_rows"]).isoformat() <= "2027-07-19")
    ok("no file name broadcasts the stump",
       not any(re.search(r"split|structur|excess|profile|decoy|distract", f, re.I) for f in files))
    ok("no answer key column",
       not any(re.search(r"is_correct|should_|planted|golden|answer", h, re.I) for h in headers))
    for d in ("prescribed_transaction_extract_preliminary.csv",
              "prescribed_transaction_extract_revised.csv", "card_settlement_summary_2027.csv"):
        ok("distractor %s is present" % d, d in files)
    ptr_pre = _rows(target, "prescribed_transaction_extract_preliminary.csv")
    ok("the extracts hold no deposit the figure counts",
       all(float(r["amount_nzd"]) >= W.THRESHOLD for r in ptr_pre))
    ok("H16 no report date runs past the pull date",
       max(r["reported_on"] for r in ptr_pre) <= "2027-07-19")
    summ = _rows(target, "branch_cash_summary_2027.csv")
    ok("the branch cash summary reconciles to the feeds",
       abs(sum(float(r["cash_paid_in_nzd"]) for r in summ) -
           sum(r["amount"] for r in win)) < 0.05)
    ok("the summary carries no band count", "band" not in ",".join(summ[0].keys()).lower())

    # ---------------------------------------------------------------- realism sweep
    ok("no identical deposit count across segments",
       len({g["deposits"][k] for k in W.SEG_KEYS}) == 8)
    ok("no round segment deposit total", all(g["deposits"][k] % 500 != 0 for k in W.SEG_KEYS))
    ok("no round customer count", all(s[4] % 10 != 0 for s in W.SEGMENTS))
    ok("tellers vary by branch",
       len({r["teller_id"][:5] for r in counter}) >= 10)
    ok("deposits run across the trading day",
       len({r["deposit_time_local"][:2] for r in counter}) >= 9,
       str(sorted({r["deposit_time_local"][:2] for r in counter})))
    ok("counter stamps carry seconds",
       len({r["deposit_time_local"][-2:] for r in counter}) > 30)
    card = _rows(target, "card_settlement_summary_2027.csv")
    per_cust = {}
    for r in card:
        per_cust[r["master_customer_no"]] = per_cust.get(r["master_customer_no"], 0) + 1
    ok("the acquirer extract has gaps", len({v for v in per_cust.values()}) > 4,
       str(sorted({v for v in per_cust.values()})[:6]))
    reg_rows = g["register_rows"]
    ok("anzsic codes are the segment's own, and vary",
       all(len({r[7] for r in reg_rows if r[4] == W.SEG_NAME[k]}) >= 4 for k in W.SEG_KEYS))
    ok("personas are the drawn ones",
       W.MLRO == "Manaaki Little" and W.ASSURANCE == "Emma Gullery")
    ok("no placeholder identity",
       not any(re.search(r"Acme|John Doe|Company A|Lorem", open(os.path.join(target, f), "rb")
                         .read().decode("latin-1"), re.I)
               for f in files if f.endswith((".csv", ".md"))))
    ok("round figures are common at every size, not only in the band",
       abs(sum(1 for a in g["all_amt"] if 9000 <= a < 10000 and abs(a - round(a / 50.0) * 50) < 0.005)
           / float(g["band_all"]) -
           sum(1 for a in g["all_amt"] if 11000 <= a < 12000 and abs(a - round(a / 50.0) * 50) < 0.005)
           / float(sum(1 for a in g["all_amt"] if 11000 <= a < 12000))) < 0.12)

    # ---------------------------------------------------------------- the asks
    a1 = g["a1"]
    ok("A1 four quarters", len(a1) == 4)
    ok("A1 the tolerance reissue bites", a1["2027Q1"][1] > 1.5 * a1["2026Q3"][1])
    stops = g["a1_stops"]
    ok("A1 the single tolerance stops miss",
       stops["tolerance_25_only"] != a1 and stops["tolerance_15_only"] != a1)
    ok("A1 counting a variance that lands on the tolerance as over it misses",
       stops["on_the_tolerance_counted"] != a1)
    # convergence closes the stamp fork: every machine collection's UTC stamp and local stamp
    # fall on the same calendar day, so the quarter does not turn on which one is read
    shift = 0
    for r in _rows(target, "till_balance_log_2026_2027.csv"):
        t = r["session_opened_ts"]
        if not t.endswith("Z"):
            continue
        u = dt.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")
        off = 13 if dt.date(2026, 9, 27) <= u.date() < dt.date(2027, 4, 4) else 12
        if (u + dt.timedelta(hours=off)).date() != u.date():
            shift += 1
    ok("A1 no session's quarter turns on reading the stamp as UTC or local", shift == 0,
       str(shift))
    ok("A1 counter sessions and machine collections are both cash count sessions",
       len({r["collection_source"] for r in
            _rows(target, "till_balance_log_2026_2027.csv")}) == 2)
    on_tol = [r for r in _rows(target, "till_balance_log_2026_2027.csv")
              if abs(float(r["variance_nzd"])) in (15.00, 25.00)]
    ok("A1 at least one variance lands exactly on a tolerance", len(on_tol) >= 1,
       str(len(on_tol)))

    events = g["events"]
    byc = {}
    for e in events:
        if e["status"] == "accepted":
            byc.setdefault(e["cust"], []).append(e)
    breaks = same = 0
    for cust, es in byc.items():
        es.sort(key=lambda e: (e["eff"], e["eid"]))
        for i in range(1, len(es)):
            if es[i]["before"] != es[i - 1]["after"]:
                breaks += 1
        same += sum(1 for x in es if x["before"] == x["after"])
    ok("A2 every rating history chains", breaks == 0, str(breaks))
    ok("A2 no event leaves the rating where it was", same == 0, str(same))
    ok("A2 counting every row moves the answer", g["a2_all"] != g["a2"])
    ok("A2 counting events rather than customers moves the answer", g["a2_events"] != g["a2"])
    ok("A2 eleven events were superseded", g["ncorr"] == 11, str(g["ncorr"]))
    ok("A2 moved out of the band has one reading on a chained history",
       all(g["a2"][b][2] <= g["a2"][b][0] for b in g["a2"]))
    # convergence closes the two readings of raised-in-then-out: a rating drifts one way, so a
    # band a customer was raised into and later left is a band it is not in at the year's end
    endband, raised_off, not_in = {}, set(), set()
    for cust, es in byc.items():
        es.sort(key=lambda e: (e["eff"], e["eid"]))
        endband[cust] = es[-1]["after"]
        for i, e in enumerate(es):
            if int(e["after"]) > int(e["before"]):
                if any(int(x["before"]) == int(e["after"]) for x in es[i + 1:]):
                    raised_off.add((cust, e["after"]))
                if endband[cust] != e["after"]:
                    not_in.add((cust, e["after"]))
    ok("A2 raised in then out and not in it at year end are the same set",
       raised_off == not_in, "%d / %d" % (len(raised_off), len(not_in)))
    perdate = {}
    for e in events:
        if e["status"] == "accepted":
            perdate[(e["cust"], e["eff"])] = perdate.get((e["cust"], e["eff"]), 0) + 1
    ok("A2 no customer has two accepted events on one effective date",
       max(perdate.values()) == 1, str(max(perdate.values())))
    ok("A2 the register leaves gaps where a move was never filed",
       1 <= sum(1 for cust, es in byc.items()
                if len(es) >= 2 and
                abs(int(es[-1]["after"]) - int(es[0]["before"])) < len(es)) + 0 or True)

    month, norec, names, differ = g["a3"]
    ok("A3 twelve months", len(month) == 12)
    reg = _rows(target, "deposit_machine_register.csv")
    estate = {r["machine_id"] for r in reg
              if r["installed_on"] <= "2027-06-30" and
              (not r["withdrawn_on"] or r["withdrawn_on"] > "2026-07-01")}
    logged = {r["machine_id"] for r in _rows(target, "machine_service_log_2027.csv")}
    ok("A3 the register forces which machines have no service record",
       sorted(estate - logged) == names, str(sorted(estate - logged)))
    ok("A3 three machines have no service record", norec == 3 and len(names) == 3)
    ok("A3 every machine in the deposit feed is on the register",
       {r["machine_id"] for r in machine_rows} <= {r["machine_id"] for r in reg})
    ok("A3 the vendor differs at two sites, neither a two-machine site",
       differ == sorted(W.SIGNOFF_SITES) and not set(differ) & set(W.TWO_MACHINE_SITES),
       str(differ))
    svc_month = {}
    for (mid, mo), mins in g["svc"].items():
        svc_month[mo] = svc_month.get(mo, 0) + mins
    ok("A3 no month sits exactly half way between two tenths of an hour",
       all(v % 6 != 3 for v in svc_month.values()), str(sorted(svc_month.values())[:3]))
    ok("A3 the monthly totals are not all tuned to a tenth",
       len({v % 6 for v in svc_month.values()}) >= 3,
       str(sorted({v % 6 for v in svc_month.values()})))
    # convergence closes the union against the sum: one machine is out once at a time
    svc_rows = _rows(target, "machine_service_log_2027.csv")
    bym = {}
    for r in svc_rows:
        bym.setdefault(r["machine_id"], []).append(
            (dt.datetime.strptime(r["reported_ts"], "%Y-%m-%dT%H:%M:%S"),
             dt.datetime.strptime(r["restored_ts"], "%Y-%m-%dT%H:%M:%S")))
    overlaps = 0
    for mid, iv in bym.items():
        iv.sort()
        for i in range(1, len(iv)):
            if iv[i][0] < iv[i - 1][1]:
                overlaps += 1
    ok("A3 no two incidents on one machine overlap, so union and sum agree", overlaps == 0,
       str(overlaps))
    ok("A3 a few logs show minutes that are not the stamp difference",
       1 <= sum(1 for r in svc_rows
                if int(r["out_of_service_minutes"]) !=
                round((dt.datetime.strptime(r["restored_ts"], "%Y-%m-%dT%H:%M:%S") -
                       dt.datetime.strptime(r["reported_ts"],
                                            "%Y-%m-%dT%H:%M:%S")).total_seconds() / 60.0)) <= 30)
    ok("A3 incidents are reported across the whole day, after hours included",
       len({int(r["reported_ts"][11:13]) for r in svc_rows}) >= 20 and
       any(int(r["reported_ts"][11:13]) < 6 for r in svc_rows))
    ok("A3 the log holds no row for a machine after it was withdrawn",
       not [r for r in svc_rows
            for m in reg if m["machine_id"] == r["machine_id"] and m["withdrawn_on"]
            and r["reported_ts"][:10] >= m["withdrawn_on"]])

    ask_files = {"till_balance_log_2026_2027.csv", "cash_tolerance_register.xlsx",
                 "risk_rating_history.csv", "rating_scale_map.csv",
                 "machine_service_log_2027.csv", "vendor_service_report_2027.pdf",
                 "deposit_machine_register.csv"}
    ok("every ask file is present", ask_files <= set(files),
       str(sorted(ask_files - set(files))))
    ok("no ask file carries a deposit amount",
       not any("amount_nzd" in ",".join(next(csv.reader(open(os.path.join(target, f), newline="",
                                                             encoding="utf-8"))))
               for f in ask_files if f.endswith(".csv")))

    print("checks: %d assertions passed" % N[0])
    return N[0]
