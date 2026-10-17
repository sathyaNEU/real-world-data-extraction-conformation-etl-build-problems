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
SCREEN, HABIT, PRIOR, BAND, GOLD = 1287, 1088, 1406, 2196, 400


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        raise AssertionError("%s FAILED %s" % (label, detail))


def _rows(target, name):
    with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


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
    base = {k: G.r10(E.excess(dep[k])) for k in W.SEG_KEYS}
    ok("R2 baseline matches the golden", base == g["per_seg"], str(base))

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

    ok("R3a the same-day screen files the named wrong answer", g["rung0"] == SCREEN, str(g["rung0"]))
    ok("R3a the band count alone is not the golden", g["band_all"] == BAND and BAND != GOLD)
    ok("R3b the decisive step files the golden", g["total"] == GOLD, str(g["total"]))
    ok("R3b the habit filter alone stays wrong", g["rung1"] == HABIT and HABIT != GOLD)
    ok("R3b the prior-year control alone stays wrong", g["rung2"] == PRIOR and PRIOR != GOLD)

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
    out, tots, labels = G.convergence(g)
    sets = G.rounded_sets(out)
    want = tuple(g["per_seg"][k] for k in W.SEG_KEYS)
    ok("C1 the sweep runs every candidate", len(labels) >= 190, str(len(labels)))
    ok("C1 every estimator gives the same eight segment figures",
       set(sets) == {want}, str(sorted(set(sets) - {want})[:3]))
    ok("C1 every estimator's segment figures sum to the golden",
       {sum(s) for s in sets} == {GOLD})
    for i, k in enumerate(W.SEG_KEYS):
        vals = [out[k][j][1] for j in range(len(labels))]
        edge = min(min(vals) - (g["per_seg"][k] - 5), (g["per_seg"][k] + 5) - max(vals))
        ok("C1 %s sits clear of its rounding edge" % k, edge >= 2.0, "%.2f" % edge)
    ok("C1 the pooled book profile converges too", g["pooled_total"] == GOLD,
       "%.1f" % g["pooled"])
    ok("C1 the unrounded book sweep is reported, not asserted away",
       max(tots) - min(tots) < 20, "%.1f..%.1f" % (min(tots), max(tots)))
    ok("C1 the rounding path the prompt pins gives the golden",
       sum(g["per_seg"].values()) == GOLD)
    # the fit quality of the family the record supports, against the one it does not
    q_log = max(E.fit_quality(g["amt_by_seg"][k], family="poisson_log") for k in W.SEG_KEYS)
    ok("C1 the log family fits the record", q_log < 1.2, "%.3f" % q_log)

    # placebo: at twelve positions where there is no excess the estimator reads nought
    clean = {}
    for r in win:
        if not r["planted"]:
            clean.setdefault(seg_of[r["cust"]], []).append(r["amount"])
    res = []
    for lo in (5500, 6000, 6500, 7000, 7500, 8000, 9000, 10500, 11000, 11500, 12000, 13000):
        for k in W.SEG_KEYS:
            res.append(E.excess(clean[k], 5000, 16000, 250, "poisson_log", "both",
                                band_lo=lo, band_hi=lo + 1000))
    rms = math.sqrt(sum(x * x for x in res) / len(res))
    ok("placebo scatter is small", rms < 6.0, "%.2f" % rms)
    ok("placebo bias is near nought", abs(sum(res) / len(res)) < 2.0,
       "%.2f" % (sum(res) / len(res)))

    # ---------------------------------------------------------------- the ladder
    ok("ladder is ordered away from the golden",
       g["band_all"] > g["rung2"] > g["rung0"] > g["rung1"] > g["total"])
    ok("ladder margin rung0 over golden", g["rung0"] / float(g["total"]) > 3.0,
       "%.2f" % (g["rung0"] / float(g["total"])))
    ok("decisive move is the largest on the ladder",
       abs(g["rung1"] - g["total"]) > abs(g["rung0"] - g["rung1"]))
    ok("the golden is the extreme of the ladder",
       g["total"] < min(g["rung0"], g["rung1"], g["rung2"], g["band_all"]))
    r0 = sorted(W.SEG_KEYS, key=lambda k: -g["rung0_seg"][k])
    ok("rung 0 names a different largest segment", r0[0] != g["largest"], r0[0])
    ok("the golden's largest sits mid-table on rung 0", 3 <= r0.index(g["largest"]) + 1 <= 6,
       str(r0.index(g["largest"]) + 1))
    ok("the golden's largest leads the runner up",
       g["per_seg"][g["largest"]] >= 1.2 * sorted(g["per_seg"].values())[-2])
    ok("the band ranking is not the answer ranking",
       sorted(W.SEG_KEYS, key=lambda k: -g["band_obs"][k])[0] != g["largest"])
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
       sum(g["per_seg"].values()) == GOLD == sum(G.r10(v) for v in g["per_seg_raw"].values()))
    ok("SF13 the three constructions differ from each other and from the golden",
       len({g["band_all"], g["rung0"], g["rung1"], g["total"]}) == 4)
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
    ok("A1 the raw stamp stop misses", stops["raw_stamps"] != a1)
    ok("A1 the single tolerance stops miss",
       stops["tolerance_25_only"] != a1 and stops["tolerance_15_only"] != a1)

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
    ok("A3 no month sits on a rounding boundary",
       all(v % 6 == 0 for v in svc_month.values()), str(sorted(svc_month.values())[:3]))

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
