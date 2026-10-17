"""Every assertion task190 stands on."""
import datetime as dt
import json
import os
import re
import sys

import pandas as pd
import pdfplumber

import golden as G
import pack as PK
import sim
import world as W

N = [0]


def A(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


def doc_text(target, name):
    with pdfplumber.open(os.path.join(target, name)) as pdf:
        return re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in pdf.pages))


def run(target):
    task = os.path.dirname(os.path.abspath(target.rstrip("/")))
    cases, alerts, lines, xw, backlog, ledger, matches, lists, base = G.load(target)
    g = G.compute(target)
    a = g["assess"]
    d = G.governing_cases(cases, lines)
    cf, ct = W.CLOSED_FROM.strftime("%Y-%m"), W.CLOSED_TO.strftime("%Y-%m")

    # ---- input gates ---------------------------------------------------------------------------
    files = sorted(os.listdir(target))
    A(len(files) >= 10, "input gate: %d files" % len(files))
    A(len({os.path.splitext(f)[1] for f in files}) >= 3, "input gate: formats")
    A(len(alerts) >= 25000, "input gate: the alert extract holds %d rows" % len(alerts))
    meta = json.load(open(os.path.join(task, "metadata.json"), encoding="utf-8"))
    A(len(meta["distractor_files"]) >= 2, "input gate: distractors")
    for dis in meta["distractor_files"]:
        A(dis["file"] in files and "distractor" not in dis["file"], "distractor %s" % dis["file"])

    # ---- the call ------------------------------------------------------------------------------
    A(g["covered"] == ["Business lending", "FX and remittance", "Trade finance"],
      "the call moved: %s" % g["covered"])
    A(g["just_misses"] == "Private wealth", "the line that just misses: %s" % g["just_misses"])
    A(len(a) == 8, "eight lines assessed, got %d" % len(a))

    # ---- R1 the three rules: the analyst test executed on the generator's clean truth -----------
    truth = {}
    for line in W.LINES:
        wbar = sim.calibrate(line, line[2], line[4])
        rows = sim.cases((line[0], line[1], line[2], line[3], wbar, line[5]))
        closed = [r for r in rows if W.CLOSED_FROM <= r["onset"] <= W.CLOSED_TO]
        nmon = sim.months_between(W.CLOSED_FROM, W.CLOSED_TO) + 1
        lam = len(closed) / nmon
        wh = sum(r["delay"] for r in closed) / len(closed)
        q0, q1 = dt.date(2026, 7, 1), dt.date(2026, 12, 31)
        truth[line[0]] = {"flow": sum(1 for r in rows if q0 <= r["detected"] <= q1),
                          "exp": lam * wh, "w": wh, "per_k": 0.0, "cust": line[3],
                          "backlog": line[5]}
    for n in truth:
        truth[n]["per_k"] = truth[n]["flow"] / truth[n]["cust"]
    pick = lambda key: sorted(sorted(truth, key=lambda n: -truth[n][key])[:W.CAPACITY])
    A(pick("flow") == ["Cards", "Deposits", "Retail payments"],
      "R1 the easy route on clean truth: %s" % pick("flow"))
    A(pick("exp") == ["Business lending", "FX and remittance", "Trade finance"],
      "R1 the decisive step on clean truth: %s" % pick("exp"))
    A(pick("flow") != pick("exp"), "R1 the easy route reaches the answer on clean truth")
    # R2 the stump is not a reading: four reflexes, three different answers, none the golden
    A(pick("per_k") == ["Correspondent banking", "Private wealth", "Trade finance"],
      "R2 the exposure reflex: %s" % pick("per_k"))
    A(pick("w") == ["Correspondent banking", "Private wealth", "Trade finance"],
      "R2 the delay reflex: %s" % pick("w"))
    A(pick("backlog") == ["Deposits", "FX and remittance", "Retail payments"],
      "R2 the backlog reflex: %s" % pick("backlog"))
    for k in ("flow", "per_k", "w", "backlog"):
        A(pick(k) != pick("exp"), "R2 the %s reflex reaches the answer" % k)
    # R3a nothing planted: every case is its own draw and the register holds no copied block
    key = list(zip(d["customer_ref"], d["typology"], d["onset_month"], d["first_seen_month"]))
    A(len(set(key)) == len(key), "R3a the register holds a repeated case key")
    # R3b no filed sentence names a rate, a stock, a product or a duration
    blob = ""
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            blob += " " + doc_text(target, f)
        elif f.endswith((".csv", ".json")):
            blob += " " + open(p, encoding="utf-8", errors="ignore").read()
    low = re.sub(r"\s+", " ", blob).lower()
    for banned in ("per month", "a month", "rate at which", "arrival", "multiplied by", "stock of",
                   "how long", "time to detection", "undetected caseload", "little's law",
                   "months unseen", "average delay", "mean time"):
        A(banned not in low, "R3b a shipped file says '%s'" % banned)
    # R3c no shipped artifact ranks or scores the lines
    fw = doc_text(target, "financial_crime_framework.pdf")
    A("does not maintain a ranking of its business lines" in fw, "R3c the framework's own disclaimer")
    for f in files:
        if f.endswith(".pdf"):
            t = doc_text(target, f).lower()
            A("ranked" not in t and "league" not in t and "scorecard" not in t,
              "R3c %s ranks the lines" % f)

    # ---- the ladder ----------------------------------------------------------------------------
    L = g["rungs"]
    A(L["rung0_confirmed_two_quarters"] == ["Cards", "Deposits", "Retail payments"], "rung 0 moved")
    A(L["rung1_confirmed_per_thousand"] == ["Correspondent banking", "Private wealth",
                                            "Trade finance"], "rung 1 moved")
    A(L["rung2_alert_backlog"] == ["Deposits", "FX and remittance", "Retail payments"], "rung 2 moved")
    A(L["rung3_months_unseen"] == ["Correspondent banking", "Private wealth", "Trade finance"],
      "rung 3 moved")
    A(L["answer_expected_carrying"] == L["answer_cohort_estimate"],
      "the two estimators disagree: %s against %s" % (L["answer_expected_carrying"],
                                                      L["answer_cohort_estimate"]))
    answers = {tuple(v) for v in L.values()}
    A(len(answers) == 4, "the ladder gives %d distinct answers" % len(answers))
    A(not set(L["rung0_confirmed_two_quarters"]) & set(L["answer_expected_carrying"]),
      "rung 0 shares a line with the answer")

    # ---- separation and margins ----------------------------------------------------------------
    vals = sorted((a[n]["expected_carrying"] for n in a), reverse=True)
    A(vals[W.CAPACITY - 1] / vals[W.CAPACITY] >= 1.15,
      "the cut margin is %.3f" % (vals[W.CAPACITY - 1] / vals[W.CAPACITY]))
    for n in a:
        A(abs(a[n]["expected_carrying"] - a[n]["cohort_estimate"]) < 0.05,
          "%s: the two estimators differ by %.3f" % (n, abs(a[n]["expected_carrying"] -
                                                            a[n]["cohort_estimate"])))
    # SF12 ties: the eight expectations are distinct, so no tie-break convention can matter
    A(len({round(a[n]["expected_carrying"], 1) for n in a}) == 8, "SF12 two lines share an expectation")

    # ---- the semantic fork table ---------------------------------------------------------------
    # SF1 a case is one customer and one typology
    A("A case is one customer and one typology" in fw, "SF1 paragraph 2.3 is not filed")
    raw = cases[cases["disposition"] == "confirmed"]
    A(len(d) < len(raw), "SF1 the case definition removes nothing")
    # SF2 the line in force at the review date
    A(set(lines["status"]) == {"current", "superseded"}, "SF2 the register's statuses")
    A((lines["current_line_code"] != "").all(), "SF2 a register row has no current line")
    A(set(d["line"]) == {l[0] for l in W.LINES}, "SF2 a record's line did not resolve")
    A(any(x in set(cases["line_code"]) for x in ("FXL", "RMT", "TXB")),
      "SF2 no record carries a pre-reorganisation code")
    # SF3 begun: the onset month, not the first alert
    A("the month in which the activity the case is about began" in doc_text(
        target, "investigation_handbook.pdf"), "SF3 the handbook does not define the onset month")
    # SF4 detected: the first seen month, and the confirmed month gives the same call
    alt = {}
    for n in [l[0] for l in W.LINES]:
        gg = d[d["line"] == n]
        closed = gg[(gg["onset_month"] >= cf) & (gg["onset_month"] <= ct)]
        lam = len(closed) / G.months(cf, ct)
        wconf = (pd.to_numeric(closed["confirmed_month"].str[:4]) * 12 +
                 pd.to_numeric(closed["confirmed_month"].str[5:7]) -
                 pd.to_numeric(closed["onset_month"].str[:4]) * 12 -
                 pd.to_numeric(closed["onset_month"].str[5:7])).mean()
        alt[n] = lam * float(wconf)
    A("which is the first seen month the investigation handbook defines, and not once it is confirmed"
      in fw, "SF4 clause 6.2 does not file which event ends the count")
    A(sorted(sorted(alt, key=lambda n: -alt[n])[:W.CAPACITY]) != g["covered"],
      "SF4 the confirmed-month reading is not separated from the filed one")
    # SF5 the review date against the extract date: both give the same call
    A(W.REVIEW_FROM > W.AS_OF, "SF5 the review date is not after the extract date")
    # SF6 the closed window
    A("began between 1 January 2021 and 31 January 2024" in fw, "SF6 clause 6.3 is not filed")
    closed_all = d[(d["onset_month"] >= cf) & (d["onset_month"] <= ct)]
    A(len(closed_all) == sum(a[n]["closed_cases"] for n in a), "SF6 the closed window's counts")
    A((closed_all["first_seen_month"] <= W.AS_OF.strftime("%Y-%m")).all(),
      "SF6 a closed-window case has not been seen, so clause 6.3 is false")
    # SF7 the governing version
    A((cases["record_version"] == "2").any(), "SF7 no case carries a second version")
    A(len(d) == len(d.drop_duplicates(subset=["case_id"])), "SF7 two versions reached the population")
    # SF8 currency: no amount enters the count
    A(set(cases["currency"]) == {"NZD", "AUD"}, "SF8 one currency only")
    # SF9 capacity
    A("The review covers three business lines" in fw, "SF9 clause 6.4 is not filed")
    A(len(g["covered"]) == W.CAPACITY, "SF9 the call names %d lines" % len(g["covered"]))
    # SF10 the unit
    A("counting one case per customer per typology" in fw, "SF10 clause 6.2's unit")
    # SF11 rounding: the call is identical at whole cases and one decimal
    for nd in (0, 1):
        s = sorted(a, key=lambda n: -round(a[n]["expected_carrying"], nd))[:W.CAPACITY]
        A(sorted(s) == g["covered"], "SF11 rounding to %d decimals changes the call" % nd)
    # SF13 the expectation against a single realisation
    A("expected to be carrying" in fw and "the expectation is taken over the cases the line's own "
      "closed record implies" in fw, "SF13 clause 6.2 does not file the expectation")

    # ---- closure axes --------------------------------------------------------------------------
    for perm in (1, 2, 3):
        sh = cases.sample(frac=1.0, random_state=perm).reset_index(drop=True)
        A(len(G.governing_cases(sh, lines)) == len(d), "axis 14 row order changes the population")
    A(len(set(zip(d["customer_ref"], d["typology"], d["line"]))) == len(d),
      "axis 15 the population holds a duplicate pair")
    A(set(xw["case_customer_ref"]) >= set(d["customer_ref"]), "axis 16 a customer is not crosswalked")
    for n in a:
        A(a[n]["expected_carrying"] > 0, "axis 17 a non-positive expectation at %s" % n)
    gap_lo = min(G.months(cf, x) for x in closed_all["onset_month"])
    A(gap_lo >= 1, "axis 9 a cohort sits before the window")

    # ---- the separation line -------------------------------------------------------------------
    A(not d["case_id"].isin(["none"]).any(), "separation sentinel")
    A(len(d[d["line_code"].isin(["FXL", "RMT", "TXB"])]) > 0, "the reorganisation reaches the call")
    led_refs = set(ledger["reference"])
    A(any(r.startswith("CRN-") for r in led_refs), "separation: A1's device is missing")
    A("queue" not in d.columns, "separation: an alert column reached the case population")

    # ---- the asks ------------------------------------------------------------------------------
    a1 = g["a1"]
    A(set(a1) == {"2026-Q1", "2026-Q2", "2026-Q3", "2026-Q4"}, "A1 quarters")
    lazy = {}
    led = ledger.copy()
    led["h"] = pd.to_numeric(led["hours"])
    for q in a1:
        lazy[q] = round(float(led[led["quarter"] == q]["h"].sum()), 1)
        A(lazy[q] != a1[q]["hours_billed"], "A1 the lazy sum matches at %s" % q)
    a2 = g["a2"]
    A(len(a2) == 5, "A2 covers %d versions" % len(a2))
    A(sum(v["matched_an_entry_later_removed"] for v in a2.values()) > 20, "A2 is too thin")
    a3 = g["a3"]
    A(len(a3) == 12, "A3 covers %d months" % len(a3))
    A(sum(v["alerts_raised"] for v in a3.values()) > 1200, "A3 is too thin")
    # the lazy A3 read: calendar days and the re-sent batch included
    al = alerts[alerts["queue"].isin(["card disputes", "chargebacks"])].copy()
    al["raised"] = pd.to_datetime(al["raised_at"]).dt.date
    al["at"] = pd.to_datetime(al["stage_at"]).dt.date
    al = al[(al["raised"] >= dt.date(2026, 1, 1)) & (al["raised"] <= dt.date(2026, 12, 31))]
    for m in range(1, 13):
        gm = al[[x.month == m for x in al["raised"]]]
        lazy_raised = int((gm["stage"] == "raised").sum())
        tri = gm[gm["stage"] == "triaged"]
        lazy_inside = sum(1 for r in tri.itertuples() if (r.at - r.raised).days <= W.WORKING_STANDARD)
        want = a3["2026-%02d" % m]
        A(lazy_raised != want["alerts_raised"] or lazy_inside != want["closed_inside_standard"],
          "A3 the lazy read matches at month %d" % m)

    # ---- figures.json --------------------------------------------------------------------------
    fj = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json"),
                        encoding="utf-8"))
    A(fj["covered"] == g["covered"], "figures.json covered")
    A(fj["a3_queue"] == g["a3"], "figures.json a3")
    A(fj["cut_margin_pct"] >= 15, "figures.json cut margin %s" % fj["cut_margin_pct"])
    A(fj["closed_record_cases"] == len(closed_all), "figures.json closed record count")
    return N[0]


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    print("checks passed:", run(t))
