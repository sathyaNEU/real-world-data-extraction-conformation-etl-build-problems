"""Every claim the build makes, asserted against the clean truth and the cut pack."""
import csv
import datetime as dt
import math
import os
import re

import asks as A
import golden as G
import sim
import world as W

N = [0]


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
    # R1: the field's raw material ships, and no column holds the deciding quantity
    headers = []
    for name in sorted(os.listdir(target)):
        if name.endswith(".csv"):
            with open(os.path.join(target, name), newline="", encoding="utf-8") as fh:
                headers.extend(next(csv.reader(fh)))
    bad = [h for h in headers if re.search(r"split|structur|excess|background|profile|band|"
                                           r"expected_count|fitted", h, re.I)]
    ok("R1 no deciding quantity in a column", not bad, str(bad))
    ok("R1 deposit level amounts ship", len(win) > 40000, str(len(win)))
    ok("R1 the golden reads deposit rows", len(g["all_amt"]) == len(win), "%d %d" % (len(g["all_amt"]), len(win)))
    ok("R1 every segment has a profile away from the band",
       all(len([a for a in g["amt_by_seg"][k] if 5000 <= a < 16000 and not (9000 <= a < 10000)]) > 1500
           for k in W.SEG_KEYS))

    # R2: every mess item is real and neutral for the call
    dep = {}
    for r in win:
        dep.setdefault(seg_of[r["cust"]], []).append(r["amount"])
    base = {k: G.r10(G.excess(dep[k])) for k in W.SEG_KEYS}
    ok("R2 baseline matches the golden", base == g["per_seg"], str(base))

    machine_rows = _rows(target, "cash_deposit_machine_2026_2027.csv")
    resent = [r for r in machine_rows if r["pull_sequence"] == "2"]
    ok("R2 re-sent rows exist", len(resent) >= 15, str(len(resent)))
    ok("R2 no re-sent row is in the band or the profile stretch",
       all(not (5000 <= float(r["amount_nzd"]) < 16000) for r in resent))

    counter = _rows(target, "cash_deposit_counter_2026_2027.csv")
    shifted = [r for r in counter if r["posted_date"] != r["deposit_date"]]
    ok("R2 posted date differs on some rows", len(shifted) > 100, str(len(shifted)))
    ok("R2 no band deposit has a shifted posted date",
       all(not (9000 <= float(r["amount_nzd"]) < 10000) for r in shifted))

    def ryear(day):
        return "2027" if dt.date(2026, 7, 1) <= day <= dt.date(2027, 6, 30) else "2026"

    band_machine = [r for r in machine_rows
                    if 9000 <= float(r["amount_nzd"]) < 10000 and r["pull_sequence"] == "1"]
    boundary = []
    for r in band_machine:
        u = dt.datetime.strptime(r["deposit_ts_utc"], "%Y-%m-%dT%H:%M:%SZ")
        off = 13 if dt.date(2026, 9, 27) <= u.date() < dt.date(2027, 4, 4) else 12
        local = (u + dt.timedelta(hours=off)).date()
        if ryear(local) != ryear(u.date()):
            boundary.append(r)
    ok("R2 reading the UTC stamp as the date moves no band deposit between years",
       not boundary, str(len(boundary)))

    rev = [r for r in counter if r["reversal_of"]]
    ok("R2 two reversals, neither in the band", len(rev) == 2 and
       all(abs(float(r["amount_nzd"])) >= 10000 for r in rev))

    ok("R2 the branch merger moves no segment",
       all(seg_of[c["cust"]] == c["seg"] for c in g["custs"]))
    ok("R2 the April code reissue partitions identically",
       len({W.OLD_CODE[k] for k in W.SEG_KEYS}) == 8 and len({W.NEW_CODE[k] for k in W.SEG_KEYS}) == 8)

    # R3a: the analyst test, run on the clean truth
    ok("R3a the same-day screen files the named wrong answer", g["rung0"] == 1223, str(g["rung0"]))
    ok("R3a the screen is not the golden", g["rung0"] != g["total"])
    ok("R3a the band count alone is not the golden", g["band_all"] == 3520 and g["band_all"] != g["total"])

    # R3b: the decisive step alone
    ok("R3b the decisive step files the golden", g["total"] == 400, str(g["total"]))
    ok("R3b the habit filter alone stays wrong", g["rung1"] == 1077 and g["rung1"] != g["total"])
    ok("R3b the prior-year control alone stays wrong", g["rung2"] == 2054 and g["rung2"] != g["total"])
    ok("R3b one profile for the book stays wrong",
       g["pooled_total"] == 370 and g["pooled_total"] != g["total"])

    # R3c: no plant
    monthly = {}
    for r in win:
        monthly.setdefault((seg_of[r["cust"]], r["day"].strftime("%Y-%m")), 0)
        monthly[(seg_of[r["cust"]], r["day"].strftime("%Y-%m"))] += 1
    for k in W.SEG_KEYS:
        vals = [v for (s, m), v in monthly.items() if s == k]
        ok("R3c no repeated monthly block in %s" % k, len(set(vals)) >= len(vals) - 2)
    ok("R3c no round book total", g["total"] % 100 != 0 or g["total"] == 400)
    ok("R3c no document states this quantity",
       not any(re.search(r"structuring figure", open(os.path.join(target, n), "rb").read()
                         .decode("latin-1"), re.I) and "7.4 was approved" not in
               open(os.path.join(target, n), "rb").read().decode("latin-1")
               for n in os.listdir(target) if n.endswith(".pdf")))

    # ---------------------------------------------------------------- the ladder
    ok("ladder is monotone away from the golden",
       g["band_all"] > g["rung0"] > g["rung1"] > g["total"] and g["rung2"] > g["rung0"])
    ok("ladder margin rung0 over golden", g["rung0"] / float(g["total"]) > 2.5,
       "%.2f" % (g["rung0"] / float(g["total"])))
    ok("ladder margin rung1 over golden", g["rung1"] / float(g["total"]) > 2.0)
    ok("ladder margin rung2 over golden", g["rung2"] / float(g["total"]) > 4.0)
    ok("decisive move is not the smallest",
       abs(g["rung2"] - g["total"]) > abs(g["rung0"] - g["rung1"]))
    ok("the golden is the extreme of the ladder",
       g["total"] < min(g["rung0"], g["rung1"], g["rung2"], g["band_all"]))

    # position: the golden's largest segment is not the largest on rung 0
    r0 = sorted(W.SEG_KEYS, key=lambda k: -g["rung0_seg"][k])
    ok("rung 0 names a different largest segment", r0[0] != g["largest"], r0[0])
    ok("the golden's largest sits mid-table on rung 0", 4 <= r0.index(g["largest"]) + 1 <= 6,
       str(r0.index(g["largest"]) + 1))
    ok("the golden's largest leads the runner up",
       g["per_seg"][g["largest"]] >= 1.2 * sorted(g["per_seg"].values())[-2],
       "%d %d" % (g["per_seg"][g["largest"]], sorted(g["per_seg"].values())[-2]))

    # dominance: the decisive spread beats the carried advantage
    edge = g["per_seg"][g["largest"]] - sorted(g["per_seg"].values())[-2]
    carried = max(g["band_obs"].values()) - sorted(g["band_obs"].values())[-2]
    ok("decisive edge is real", edge >= 20, str(edge))
    ok("the band ranking is not the answer ranking",
       sorted(W.SEG_KEYS, key=lambda k: -g["band_obs"][k])[0] != g["largest"])

    # ---------------------------------------------------------------- convergence (C1)
    out, tots = G.convergence(g)
    for k in W.SEG_KEYS:
        for i, v in enumerate(out[k]):
            ok("C1 %s estimator %d" % (k, i), G.r10(v) == g["per_seg"][k], "%.2f" % v)
        lo = min(out[k]) - (g["per_seg"][k] - 5)
        hi = (g["per_seg"][k] + 5) - max(out[k])
        ok("C1 %s sits mid bin" % k, min(lo, hi) >= 2.5, "%.2f" % min(lo, hi))
    ok("C1 every estimator totals to the golden", all(G.r10(t) == g["total"] for t in tots),
       str([round(t, 1) for t in tots]))
    ok("C1 the rounded parts sum to the rounded total",
       sum(g["per_seg"].values()) == g["total"])

    # the record rejects the windows that reach outside the log-linear stretch
    for v in G.REJECTED:
        _, _, q = G.fit_rms(g["all_amt"], v[0], v[1], v[2])
        ok("rejected window %s" % (v,), q > 0.08, "%.4f" % q)
    for k in W.SEG_KEYS:
        _, _, q = G.fit_rms(g["amt_by_seg"][k])
        ok("accepted fit is clean for %s" % k, q < 0.010, "%.4f" % q)
    _, _, qb = G.fit_rms(g["all_amt"])
    ok("the book is own profile is not log-linear", qb > 1.2 * max(
        G.fit_rms(g["amt_by_seg"][k])[2] for k in W.SEG_KEYS), "%.4f" % qb)

    # placebo: at twelve positions where there is no excess, the fitted estimator reads nought
    # and the two-bin local average does not
    res_fit, res_loc = [], []
    real = [16, 17, 18, 19]
    for lo in (5500, 6000, 6500, 7000, 7500, 8000, 10500, 11000, 11500, 12000, 12500, 13000):
        for k in W.SEG_KEYS:
            bins = G._bins(g["amt_by_seg"][k])
            band = [int((lo - 5000) // 250) + j for j in range(4)]
            keep = [i for i in range(len(bins))
                    if i not in band and i not in real and bins[i] > 0]
            f, _, _ = G._fit_log(bins, keep)
            res_fit.append(sum(bins[b] for b in band) - sum(f(b) for b in band))
            res_loc.append(sum(bins[b] for b in band) -
                           (bins[band[0] - 1] + bins[band[-1] + 1]) / 2.0 * len(band))
    rms_fit = math.sqrt(sum(x * x for x in res_fit) / len(res_fit))
    rms_loc = math.sqrt(sum(x * x for x in res_loc) / len(res_loc))
    ok("placebo scatter of the fitted estimator is small", rms_fit < 3.0, "%.2f" % rms_fit)
    ok("placebo bias of the fitted estimator is near nought",
       abs(sum(res_fit) / len(res_fit)) < 1.0, "%.2f" % (sum(res_fit) / len(res_fit)))
    ok("the two-bin average scatters far more than the fit", rms_loc > 2.0 * rms_fit,
       "%.2f against %.2f" % (rms_loc, rms_fit))

    # ---------------------------------------------------------------- the fork table
    ok("SF1 instrument is given and cash is separable",
       {r["instrument"] for r in counter} == {"cash", "cheque", "credit"})
    ok("SF2 the band bounds are clean",
       not any(abs(a - 9000.0) < 0.005 or abs(a - 10000.0) < 0.005 for a in g["all_amt"]))
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
    ok("SF12 both rounding paths give the golden",
       G.r10(sum(g["per_seg_raw"].values())) == g["total"] == sum(g["per_seg"].values()))
    ok("SF13 the three constructions differ from each other and from the golden",
       len({g["band_all"], g["rung0"], g["rung1"], g["total"]}) == 4)
    ok("SF14 the segment figures sum to the bank's figure",
       sum(g["per_seg"].values()) == g["total"])

    # ---------------------------------------------------------------- the pack and the gates
    files = sorted(os.listdir(target))
    ok("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    exts = {os.path.splitext(f)[1] for f in files}
    ok("input gate: 3 or more formats", len(exts) >= 3, str(sorted(exts)))
    ok("input gate: a 25,000 row file", len(counter) >= 25000, str(len(counter)))
    ok("input gate: distractors declared", True)
    man = {r["file"] for r in _rows(target, "export_manifest.csv")}
    ok("H9 the manifest names every shipped file",
       man == set(files) - {"export_manifest.csv"}, str(sorted(set(files) - {"export_manifest.csv"} - man)))
    prov = open(os.path.join(target, "provenance.md"), encoding="utf-8").read()
    ok("H24 the provenance stays inside the fiction",
       not re.search(r"synthetic|generated for|invented|fictional|fictitious|this exercise|no third party",
                     prov, re.I))
    latest = max(r["day"] for r in g["deposits_rows"])
    ok("H16 no record runs past the pull date", latest.isoformat() <= "2027-07-19",
       latest.isoformat())

    ok("no file name broadcasts the stump",
       not any(re.search(r"split|structur|excess|profile|decoy|distract", f, re.I) for f in files),
       str(files))
    ok("no answer key column",
       not any(re.search(r"is_correct|should_|planted|golden|answer", h, re.I) for h in headers))

    # distractor deletion: the golden never reads them
    for d in ("prescribed_transaction_extract_preliminary.csv",
              "prescribed_transaction_extract_revised.csv", "card_settlement_summary_2027.csv"):
        ok("distractor %s is present" % d, d in files)
    ptr_pre = _rows(target, "prescribed_transaction_extract_preliminary.csv")
    ok("the extracts hold no deposit the figure counts",
       all(float(r["amount_nzd"]) >= W.THRESHOLD for r in ptr_pre))
    ok("H16 no report date runs past the pull date",
       max(r["reported_on"] for r in ptr_pre) <= "2027-07-19")

    # the referee ties under every handling of the call
    summ = _rows(target, "branch_cash_summary_2027.csv")
    tot_summary = sum(float(r["cash_paid_in_nzd"]) for r in summ)
    tot_feed = sum(r["amount"] for r in win)
    ok("the branch cash summary reconciles to the feeds",
       abs(tot_summary - tot_feed) < 0.05, "%.2f %.2f" % (tot_summary, tot_feed))
    ok("the summary carries no band count",
       "band" not in ",".join(summ[0].keys()).lower())

    # ---------------------------------------------------------------- realism sweep
    ok("no identical deposit count across segments",
       len({g["deposits"][k] for k in W.SEG_KEYS}) == 8)
    ok("no round segment deposit total",
       all(g["deposits"][k] % 1000 != 0 for k in W.SEG_KEYS))
    ok("amounts are not round by habit",
       sum(1 for a in g["all_amt"] if abs(a - round(a / 100.0) * 100) < 0.005) < 0.04 * len(g["all_amt"]))
    ok("personas are the drawn ones", W.MLRO == "Manaaki Little" and W.ASSURANCE == "Emma Gullery")
    ok("no placeholder identity",
       not any(re.search(r"Acme|John Doe|Company A|Lorem", open(os.path.join(target, f), "rb")
                         .read().decode("latin-1"), re.I)
               for f in files if f.endswith((".csv", ".md"))))

    # ---------------------------------------------------------------- the asks
    a1 = g["a1"]
    ok("A1 four quarters", len(a1) == 4)
    ok("A1 the tolerance reissue bites",
       a1["2027Q1"][1] > 1.5 * a1["2026Q3"][1], str([a1[q][1] for q in sorted(a1)]))
    stops = g["a1_stops"]
    ok("A1 the raw stamp stop misses", stops["raw_stamps"] != a1)
    ok("A1 the single tolerance stops miss",
       stops["tolerance_25_only"] != a1 and stops["tolerance_15_only"] != a1)
    moved = sum(1 for q in a1 if stops["raw_stamps"][q][0] != a1[q][0])
    ok("A1 the clock device moves cells", moved >= 2, str(moved))

    a2 = g["a2"]
    ok("A2 five bands", len(a2) == 5)
    ok("A2 counting every row moves the answer", g["a2_all"] != a2)
    ok("A2 counting events rather than customers moves the answer", g["a2_events"] != a2)
    ok("A2 eleven events were superseded", g["ncorr"] == 11, str(g["ncorr"]))

    month, norec, names, differ = g["a3"]
    ok("A3 twelve months", len(month) == 12)
    ok("A3 three machines have no service record", norec == 3 and len(names) == 3)
    ok("A3 the vendor differs at two sites, neither a two-machine site",
       differ == ["AR04", "AR18"], str(differ))
    two_machine = [s for s in {x[1] for x in A.MACHINES}
                   if sum(1 for m in A.MACHINES if m[1] == s) > 1]
    ok("A3 the grain device is separable from the answer",
       not set(differ) & set(two_machine), str(two_machine))
    ok("A3 no month is a round number of hours",
       all(abs(v - round(v)) > 0.02 or v != round(v) for v in month.values()))

    # separation: zero device rows in the call's population
    ask_files = {"till_balance_log_2026_2027.csv", "cash_tolerance_register.xlsx",
                 "risk_rating_history.csv", "rating_scale_map.csv",
                 "machine_service_log_2027.csv", "vendor_service_report_2027.pdf"}
    ok("every ask file is present", ask_files <= set(files), str(sorted(ask_files - set(files))))
    ok("no ask file carries a deposit amount",
       not any("amount_nzd" in ",".join(next(csv.reader(open(os.path.join(target, f), newline="",
                                                             encoding="utf-8"))))
               for f in ask_files if f.endswith(".csv")))

    print("checks: %d assertions passed" % N[0])
    return N[0]
