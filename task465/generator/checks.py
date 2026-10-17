"""task465 checks: the three rules executed on the clean truth and on the pack (R1 to R3c), the convergence the literal
reader relies on (C1), every semantic fork row, the ladder and its margins, each Layer 1 item's neutrality, the asks'
stops and bins, the separation of the call from the asks, the input gates and the realism sweep.

    python3 task465/generator/checks.py
"""
import csv
import json
import os
import re
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bundle as B     # noqa: E402
import methods as M    # noqa: E402
import sim as S        # noqa: E402
import world as W      # noqa: E402

GOLD = ["Ardley", "Elster", "Pallard"]
SANDY = ["Ardley", "Elster", "Pallard", "Tresham"]


def calls(el, q):
    return [c for c in W.MEMBERS if q[c] <= W.BUY_MULTIPLE * el[c] + 1e-12]


def _pdf_text(p):
    import pypdf
    return " ".join(pg.extract_text() for pg in pypdf.PdfReader(p).pages).replace("\n", " ")


def _mid(v, step):
    k = v / step
    return abs((k - np.floor(k)) - 0.5) / 0.5


def run(target, golden, x=None, meta_path=None, fig_path=None):
    results = []

    def check(label, cond, detail=""):
        results.append(bool(cond))
        print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [" + str(detail) + "]") if detail != "" else ""))

    F = json.load(open(fig_path or os.path.join(HERE, "figures.json")))
    ts = B.terms(target)
    q = B.quotes(target)
    route = {m: B.expected_loss(B.yields(target, m), ts) for m in
             ("drop", "district", "ratio", "regress", "worst", "zero", "golden", "golden_unrounded")}
    gold = route["golden"]
    gset = calls(gold, q)

    # ------------------------------------------------------------------ R1 to R3c, the three rules executed
    heads = [open(B.path(target, k), encoding="utf-8").readline() for k in ("pull24", "pull26", "enrol", "tickets",
                                                                             "transfers", "drought")]
    check("R1 the field's raw material ships: county and district acres and production by year; no expected-loss, "
          "burn or recovered-yield column in any file", all(not re.search(r"loss|burn|recover|indemn", h, re.I)
                                                             for h in heads))
    rec = B.recovered(target)
    check("R1 the golden's decisive computation reads the district and county harvested acres and production",
          len(rec) == 10 and all(v["harvested"] > 0 and v["production"] > 0 for v in rec.values()), len(rec))
    if x is not None:
        cty, dist = S.current(x)
        R = M.routes(cty, dist, x["pub"], x["terms"])
        t = {m: M.expected_loss(s, x["terms"]) for m, s in R.items()}
        check("R3a the easy route on the clean truth (the published years, every filed rule applied) buys none of "
              "the five covers", calls(t["drop"], W.QUOTES) == [], calls(t["drop"], W.QUOTES))
        check("R3b the easy route with only the decisive step changed (each withheld year recovered from its "
              "district) buys Ardley, Elster and Pallard on the clean truth", calls(t["golden"], W.QUOTES) == GOLD)
        check("R3b each lower rung's single correction leaves the truth on a wrong answer (district, peers, ratio, "
              "regression and worst-year fills buy none; a total failure buys four)",
              all(calls(t[m], W.QUOTES) == [] for m in ("district", "peers", "ratio", "regress", "worst"))
              and calls(t["zero"], W.QUOTES) == SANDY)
        check("R3b the clean truth's expected losses equal the pack's, every cover", all(
            abs(t["golden"][c] - gold[c]) < 1e-9 for c in W.MEMBERS))
    check("R3a on the pack the default path buys none of the five covers", calls(route["drop"], q) == [],
          {c: round(v, 2) for c, v in route["drop"].items()})
    check("R3b on the pack only recovery buys Ardley, Elster and Pallard", gset == GOLD and all(
        calls(route[m], q) != GOLD for m in ("drop", "district", "ratio", "regress", "worst", "zero")), gset)
    texts = {k: _pdf_text(B.path(target, k)) for k in ("methods", "terms", "policy")}
    texts["notice"] = open(B.path(target, "notice"), encoding="utf-8").read()
    alltext = " ".join(texts.values())
    check("R3c no plant: no document ties a withheld estimate to a drought, says a county can be had by subtraction, or "
          "names an other-counties row", not re.search(r"other counties|subtract|less the (?:published|other|count)|residual|withheld.{0,80}"
                                                        r"drought|drought.{0,80}withheld", alltext, re.I))
    check("R3c no plant: no document ranks the covers or states an expected loss",
          not re.search(r"expected loss (?:of|is) \d|burn cost|loss cost", alltext, re.I))
    cty_p, dist_p = B.sorghum(target)
    series = {c: tuple(round(v["yield"], 1) for y, v in sorted(cty_p[c].items()) if v["yield"] is not None)
              for c in cty_p}
    check("R3c no plant: no county's published dryland yield series repeats another's", len(set(series.values()))
          == len(series))

    # ------------------------------------------------------------------ C1, what the literal reader relies on
    cd = B.county_district(target)
    foot, resid_ok = True, True
    for d in W.COUNTY_DISTRICTS:
        cs = [c for c, v in cd.items() if v == d]
        for y in range(1991, 2026):
            withheld = [c for c in cs if cty_p[c][y]["yield"] is None]
            for f in ("harvested", "production"):
                s = sum(cty_p[c][y][f] for c in cs if c not in withheld)
                if not withheld:
                    foot &= abs(s - dist_p[d][y][f]) < 1e-6
                else:
                    resid_ok &= len(withheld) == 1 and dist_p[d][y][f] - s > 0
    check("C1 the counties foot to their district to the acre and the bushel in every year none is withheld", foot)
    check("C1 in every withheld year exactly one county of the district is withheld and the residual is positive",
          resid_ok)
    if x is not None:
        tr = M.recovered(*S.current(x), x["pub"], "Ardley")
        truth_ok = True
        for c in SANDY:
            for y, v in M.recovered(*S.current(x), x["pub"], c).items():
                truth_ok &= rec[(c, y)]["production"] == v["production"] and rec[(c, y)]["harvested"] == v["harvested"]
        check("C1 each recovered county-year equals the service's own estimate in the generator", truth_ok and len(tr) == 3)
    cty_a, dist_a = B.sorghum(target, practice="ALL")
    all_ok = True
    for (c, y), v in rec.items():
        d = cd[c]
        peers = [k for k, dd in cd.items() if dd == d and k != c]
        h = dist_a[d][y]["harvested"] - sum(cty_a[k][y]["harvested"] for k in peers)
        p = dist_a[d][y]["production"] - sum(cty_a[k][y]["production"] for k in peers)
        all_ok &= h == v["harvested"] and p == v["production"]
    check("C1 the all-practices tables give the same recovered acres and bushels for every withheld county-year", all_ok)
    check("C1 every recovered yield is exact to one decimal (rounded and unrounded recoveries give the same expected "
          "losses)", all(abs(route["golden"][c] - route["golden_unrounded"][c]) < 1e-9 for c in W.MEMBERS))

    # ------------------------------------------------------------------ the semantic fork table
    ap = B.expected_loss(B.yields(target, "golden", practice="ALL"), ts)
    check("SF1 the all-practices yield gives the same call", calls(ap, q) == GOLD, {c: round(v, 2) for c, v in ap.items()})
    cty_g = B.yields(target, "golden")
    unr = {}
    for c in W.MEMBERS:
        unr[c] = {y: (cty_p[c][y]["production"] / cty_p[c][y]["harvested"] if cty_p[c][y]["yield"] is not None
                      else cty_g[c][y]) for y in range(1991, 2026)}
    el_unr = B.expected_loss(unr, ts)
    check("SF2 published yields recomputed unrounded from production and acres give the same call", calls(el_unr, q) == GOLD)
    check("SF3 the golden runs 35 crop years for every cover", all(len(cty_g[c]) == 35 for c in W.MEMBERS))
    check("SF4 the district's yield in withheld years buys none; a zero buys four",
          calls(route["district"], q) == [] and calls(route["zero"], q) == SANDY)
    rt = B.expected_loss(cty_g, ts, ratio_trend=True)
    check("SF5 the term sheet brings a year to 2027 by adding the trend (the ratio reading would add Corvin's cover)",
          "by adding the county's trend" in texts["terms"].replace("  ", " ") and calls(rt, q) != GOLD, calls(rt, q))
    check("SF6 the trigger is 90 per cent of the expected yield", "90 per cent of the expected yield" in texts["terms"])
    shares = [B.share(c, y, v, ts) for c in W.MEMBERS for y, v in cty_g[c].items()]
    check("SF7 every share lies in [0, 1] and the payment is capped at the liability",
          0 <= min(shares) and max(shares) <= 1 and "never more than the liability" in texts["terms"])
    check("SF8 the policy averages over the crop years 1991 to 2025", re.search(r"average,\s*over the crop years 1991 to "
                                                                                 r"2025", texts["policy"]) is not None)
    import openpyxl
    hdr = [c.value for c in openpyxl.load_workbook(B.path(target, "quotes"))["Dryland grain sorghum"][4]]
    check("SF9 the quote schedule states rates per cent of liability", any("per cent of liability" in str(h) for h in hdr))
    marg = min(max(q[c], W.BUY_MULTIPLE * gold[c]) / min(q[c], W.BUY_MULTIPLE * gold[c]) for c in W.MEMBERS)
    check("SF10 no cover's quoted rate within 1.2 of its line either way", marg >= 1.2, round(marg, 3))
    early = B.expected_loss(B.yields(target, "golden", vintage="early"), ts)
    check("SF11 the March 2024 download's estimates give the same call, expected losses within 0.1",
          calls(early, q) == GOLD and max(abs(early[c] - gold[c]) for c in W.MEMBERS) < 0.1,
          max(abs(early[c] - gold[c]) for c in W.MEMBERS))
    no25 = {c: {y: v for y, v in s.items() if y != 2025} for c, s in cty_g.items()}
    same = all(calls(B.expected_loss(B.yields(target, m, vintage="early"), ts), q) == calls(route[m], q)
               for m in ("drop", "district", "ratio", "regress", "worst", "zero"))
    check("SF11 grid: on every rung the March 2024 download's estimates file the same call as the October 2026 one", same)
    check("SF12 leaving out the preliminary 2025 estimates gives the same call", calls(B.expected_loss(no25, ts), q) == GOLD)
    raw_ok = True
    for r in B.read_export(target, "pull24"):
        if r["Geo Level"] == "COUNTY" and r["County"].title() in cd:
            raw_ok &= B.district_code(r["Ag District Code"], int(r["Year"])) == cd[r["County"].title()]
    check("SF13 no county changed district; one-digit codes read as their two-digit codes", raw_ok)
    ansi24 = {r["County"]: r["County ANSI"] for r in B.read_export(target, "pull24") if r["Geo Level"] == "COUNTY"}
    ansi26 = {r["County"]: r["County ANSI"] for r in B.read_export(target, "pull26") if r["Geo Level"] == "COUNTY"}
    check("SF14 every county carries one name and one code (leading zeros apart) in both downloads",
          set(ansi24) == set(ansi26) and all(ansi24[c].zfill(3) == ansi26[c] for c in ansi26))
    check("SF15 the reported figures are the same rounded or not at the recovery step",
          all(abs(route["golden"][c] - route["golden_unrounded"][c]) < 1e-9 for c in W.MEMBERS))

    # ------------------------------------------------------------------ the ladder and margins
    check("ladder R0 the published years only: buys none", calls(route["drop"], q) == [])
    check("ladder R1 the district fill: buys none", calls(route["district"], q) == [])
    check("ladder R2 ratio, regression and worst-year fills: buy none",
          all(calls(route[m], q) == [] for m in ("ratio", "regress", "worst")))
    check("ladder R2x a total failure: buys Ardley, Elster, Pallard and Tresham", calls(route["zero"], q) == SANDY)
    check("ladder R3 recovery: buys Ardley, Elster and Pallard", gset == GOLD)
    for c in GOLD:
        best = max(route[m][c] for m in ("drop", "district", "ratio", "regress", "worst"))
        lo, hi = W.BUY_MULTIPLE * best, W.BUY_MULTIPLE * gold[c]
        check("margin %s: its quoted rate sits 1.2 or more inside its line and outside the best fill's" % c,
              hi / q[c] >= 1.2 and q[c] / lo >= 1.2, (round(hi / q[c], 3), round(q[c] / lo, 3)))
    lo, hi = W.BUY_MULTIPLE * gold["Tresham"], W.BUY_MULTIPLE * route["zero"]["Tresham"]
    check("margin Tresham: dear by 1.2 or more on recovery, cheap by 1.2 or more on a total failure",
          q["Tresham"] / lo >= 1.2 and hi / q["Tresham"] >= 1.2, (round(q["Tresham"] / lo, 3), round(hi / q["Tresham"], 3)))
    check("margin Corvin: dear by 1.2 or more on every rung", all(q["Corvin"] / (W.BUY_MULTIPLE * route[m]["Corvin"]) >= 1.2
                                                                  for m in route))
    worth = min(gold[c] - max(route[m][c] for m in ("drop", "district", "ratio", "regress", "worst")) for c in GOLD)
    check("worth: recovery moves each bought cover's expected loss 1.9 points or more over the best fill", worth >= 1.9,
          round(worth, 2))
    mids = []
    for c in W.MEMBERS:
        mids += [_mid(gold[c], 0.01), _mid(q[c] / gold[c], 0.01), _mid(W.BUY_MULTIPLE * gold[c], 0.01)]
    check("bins: every main figure sits 0.1 or more of a half-bin from its rounding edge", min(mids) >= 0.1,
          round(min(mids), 2))

    # ------------------------------------------------------------------ figures.json and the goldens
    check("figures.json carries the call and every cover's figures as recomputed", F["call"]["buy"] == GOLD and all(
        F["covers"][c]["expected_loss"] == float("%.2f" % gold[c]) and F["covers"][c]["multiple"] ==
        float("%.2f" % (q[c] / gold[c])) and F["covers"][c]["change_rate"] == float("%.2f" % (1.4 * gold[c]))
        for c in W.MEMBERS))
    with open(os.path.join(golden, W.GOLDEN["record"]), encoding="utf-8") as fh:
        rr = list(csv.DictReader(fh))
    st = F["stated"]
    check("figures.json's stated constants are the pack's: the policy's 1.4, the term sheet's 90 per cent, the methods "
          "note's 14 per cent moisture", re.search(r"at most %.1f times\s+the cover's expected loss" % st["policy_multiple"],
                                                    texts["policy"]) is not None
          and "Trigger %d per cent of the expected yield" % st["trigger_pct"] in texts["terms"]
          and "56 pounds at %d per cent moisture" % st["standard_moisture_pct"] in texts["methods"]
          and "$%.2f per hundredweight" % st["price_cwt"] in texts["terms"]
          and "weighs %d pounds" % st["bushel_lb"] in texts["terms"])
    check("the conformed record holds 175 county-years, ten recovered", len(rr) == 175 and sum(
        r["source"].startswith("recovered") for r in rr) == 10)
    wb = openpyxl.load_workbook(os.path.join(golden, W.GOLDEN["workbook"]))
    check("the workbook carries Covers, Burn, Liability and premium, Receipts 2016-2020 and Notes, with a chart",
          wb.sheetnames == ["Covers", "Burn", "Liability and premium", "Receipts 2016-2020", "Notes"]
          and len(wb["Covers"]._charts) == 1)
    cov = {wb["Covers"].cell(row=i, column=1).value: [wb["Covers"].cell(row=i, column=j).value for j in range(4, 9)]
           for i in range(5, 10)}
    check("the workbook's cover figures agree with figures.json", all(
        abs(cov[c][0] * 100 - F["covers"][c]["expected_loss"]) < 1e-9 and cov[c][4] == F["covers"][c]["call"]
        for c in W.MEMBERS))

    # ------------------------------------------------------------------ Ask A: liability and premium
    acres, lia, prem = B.liability(target)
    check("Ask A golden figures as in figures.json", all(F["liability"][c] == int(round(lia[c], -2)) and
                                                         F["premium"][c] == int(round(prem[c], -2)) for c in W.MEMBERS))
    check("Ask A bins: every liability and premium 0.6 or more of a half-bin from its edge",
          min(min(_mid(lia[c], 100), _mid(prem[c], 100)) for c in W.MEMBERS) >= 0.6)
    _, l_utc, p_utc = B.liability(target, local_close=False)
    check("Ask A primary D8: the UTC date filter (the cracker) moves every county's liability and premium out of its bin",
          all(round(p_utc[c], -2) != round(prem[c], -2) and round(l_utc[c], -2) != round(lia[c], -2) for c in W.MEMBERS),
          {c: int(round(p_utc[c], -2)) for c in W.MEMBERS})
    _, _, p_irr = B.liability(target, keep_irrigated=True)
    check("Ask A H1: irrigated fields kept move Corvin's premium", round(p_irr["Corvin"], -2) != round(prem["Corvin"], -2))
    _, _, p_first = B.liability(target, latest=False)
    check("Ask A H2: each field's first submission kept moves the premium of every county with an amended field",
          sum(round(p_first[c], -2) != round(prem[c], -2) for c in W.MEMBERS) >= 4)
    _, _, p_bu = B.liability(target, price_per_bu=W.PRICE_CWT)
    check("Ask A H3: the price read per bushel moves every premium", all(round(p_bu[c], -2) != round(prem[c], -2)
                                                                         for c in W.MEMBERS))
    enr = B.enrolment(target)
    late = [r for r in enr if "2026-10-30T22:00:00Z" <= r["submitted_at"] < "2026-10-31T00:00:00Z"]
    check("Ask A device rows: late submissions dated 30 October in UTC in every county, nothing marks them",
          {r["field_county"] for r in late} == set(W.MEMBERS) and set(enr[0]) == {
              "submission_id", "submitted_at", "member_no", "field_id", "field_county", "crop", "practice", "acres",
              "action"}, len(late))

    # ------------------------------------------------------------------ Ask B: receipts share
    sh = B.receipts_share(target)
    check("Ask B golden figures as in figures.json", all(F["receipts_share"][c] == float("%.1f" % sh[c])
                                                         for c in W.MEMBERS))
    check("Ask B bins: every share 0.6 or more of a half-bin from its edge", min(_mid(sh[c], 0.1) for c in W.MEMBERS)
          >= 0.6)
    for label, kw in (("primary D1: every ticket counted (the cracker)", dict(drop_transfers=False)),
                      ("H4: pounds at delivery moisture", dict(shrink=False)),
                      ("H7: the March 2024 download's production", dict(vintage="early")),
                      ("H6: wheat and corn kept", dict(sorghum_only=False))):
        v = B.receipts_share(target, **kw)
        check("Ask B %s moves every county's share out of its bin" % label,
              all(round(v[c], 1) != round(sh[c], 1) for c in W.MEMBERS), {c: round(v[c], 1) for c in W.MEMBERS})
    with open(B.path(target, "dict"), encoding="utf-8") as fh:
        dtext = fh.read()
    ni_c, _ = B.sorghum(target, practice="NI")
    al_c, _ = B.sorghum(target, practice="ALL")
    irr = [c for c in W.MEMBERS if any(al_c[c][y]["production"] != ni_c[c][y]["production"] for y in range(2016, 2021))]
    check("Ask B reading: the dictionary says the tickets hold irrigated and dryland grain alike, so the share runs on "
          "the county's grain sorghum production, all practices; only Corvin grows irrigated sorghum",
          "irrigated and dryland alike" in dtext and irr == ["Corvin"], irr)
    check("Ask A reading: the premium from the rounded liability lands in the same hundred for every cover",
          all(round(q[c] / 100.0 * round(lia[c], -2), -2) == round(prem[c], -2) for c in W.MEMBERS))
    tr = {t["transfer_no"] for t in B.transfers(target)}
    tk = B.tickets(target)
    refs = [t["reference"] for t in tk]
    check("Ask B device rows: the terminal's transfer tickets carry the member's account and a reference like any "
          "other ticket's", all(re.fullmatch(r"\d{7}", r) for r in refs) and sum(r in tr for r in refs) == len(tr))
    check("Ask B: ticket and transfer numbers unique", len(set(t["ticket_no"] for t in tk)) == len(tk)
          and len(tr) == len(B.transfers(target)))

    # ------------------------------------------------------------------ separation of the call and the asks
    tmp = tempfile.mkdtemp()
    try:
        for k in W.FILES:
            if k not in ("enrol", "notice", "tickets", "transfers", "roster", "drought", "prior"):
                shutil.copy(B.path(target, k), os.path.join(tmp, W.FILES[k]))
        g2 = B.expected_loss(B.yields(tmp, "golden"), B.terms(tmp))
        check("separation: the call and every rung computed with the cooperative's and the distractor files deleted "
              "are identical", all(abs(g2[c] - gold[c]) < 1e-12 for c in W.MEMBERS))
    finally:
        shutil.rmtree(tmp)
    tmp = tempfile.mkdtemp()
    try:
        for k in W.FILES:
            if k not in ("drought", "prior"):
                shutil.copy(B.path(target, k), os.path.join(tmp, W.FILES[k]))
        a2, l2, p2 = B.liability(tmp)
        s2 = B.receipts_share(tmp)
        check("separation: the distractors deleted, every ask figure is unchanged", all(
            p2[c] == prem[c] and s2[c] == sh[c] for c in W.MEMBERS))
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------ Layer 1 neutrality (R2)
    check("R2 two downloads: the earlier one's revised years leave the call where it is", calls(early, q) == GOLD)
    check("R2 practice rows: the all-practices yield leaves the call where it is", calls(ap, q) == GOLD)
    check("R2 symbols: the golden method never reads a withheld cell's value", all(
        cty_g[c][y] == rec[(c, y)]["yld"] for (c, y) in rec))
    check("R2 district recode: recovery is within a year and the codes map one to one", raw_ok)

    # ------------------------------------------------------------------ input gates and realism
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("gates: 10 or more files, 3 or more formats, a file of 25,000 rows or more",
          len(files) >= 10 and len(fmts) >= 3 and big >= 25000, (len(files), sorted(fmts), big))
    meta = json.load(open(meta_path)) if meta_path else {}
    check("gates: two or more distractors named in metadata.json, each a shipped file",
          len(meta.get("distractor_files", [])) >= 2 and all(d in files for d in meta.get("distractor_files", [])))
    check("realism: no 'distractor' in any file name", not any("distract" in f.lower() for f in files))
    check("realism: the risk manager named in the policy and the notice", W.PEOPLE["risk"] in texts["policy"]
          and W.PEOPLE["risk"] in texts["notice"])
    check("realism: no library banner in any PDF", all(b"ReportLab" not in open(B.path(target, k), "rb").read()
                                                       for k in ("methods", "terms", "policy")))
    check("realism: every file stamped with the folder's date", len({int(os.path.getmtime(os.path.join(target, f)))
                                                                    for f in files}) == 1)
    dash = [f for f in files if f.endswith((".csv", ".txt")) and ("—" in open(os.path.join(target, f),
                                                                                   encoding="utf-8").read())]
    check("realism: no em dash in any text file", not dash, dash)
    check("realism: the withheld marks are common across crops (sorghum's dryland marks are not singled out)",
          sum(1 for r in B.read_export(target, "pull24") if r["Value"] == "(S)") > 2000)
    ok = all(results)
    print("%s  task465 checks: %d of %d pass" % ("PASS" if ok else "FAIL", sum(results), len(results)))
    return ok


if __name__ == "__main__":
    import build as BLD
    x = BLD.world()
    TASK = os.path.dirname(HERE)
    sys.exit(0 if run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), x=x,
                      meta_path=os.path.join(TASK, "metadata.json"),
                      fig_path=os.path.join(HERE, "figures.json")) else 1)
