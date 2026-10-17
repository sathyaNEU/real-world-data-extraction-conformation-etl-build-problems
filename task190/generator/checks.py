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
    # R3c no shipped artifact ranks or scores the lines, and none says the bank does not
    fw = doc_text(target, "financial_crime_framework.pdf")
    for f in files:
        if f.endswith(".pdf"):
            t = doc_text(target, f).lower()
            for w in ("ranked", "ranking", "league", "scorecard", "highest risk line",
                      "most exposed"):
                A(w not in t, "R3c %s says '%s'" % (f, w))

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
    A(sorted(sorted(alt, key=lambda n: -alt[n])[:W.CAPACITY]) == g["covered"],
      "SF4 the confirmed-month reading moves the call")
    A(sorted(((alt[n], n) for n in alt), reverse=True)[W.CAPACITY][1] == g["just_misses"],
      "SF4 the confirmed-month reading moves the line that just misses")
    cut = sorted(((alt[n], n) for n in alt), reverse=True)[W.CAPACITY][0]
    for n in alt:
        if n in g["covered"] or n == g["just_misses"]:
            continue
        A(alt[n] < cut, "SF4 %s reaches the cut under the confirmed-month reading" % n)
    # SF5 the review date against the extract date: both give the same call
    A(W.REVIEW_FROM > W.AS_OF, "SF5 the review date is not after the extract date")
    # SF6 the closed window
    A("between 1 January 2021 and 31 January 2024 is complete" in fw,
      "SF6 clause 6.3 does not file the look-back span")
    closed_all = d[(d["onset_month"] >= cf) & (d["onset_month"] <= ct)]
    A(len(closed_all) == sum(a[n]["closed_cases"] for n in a), "SF6 the closed window's counts")
    A((closed_all["first_seen_month"] <= W.AS_OF.strftime("%Y-%m")).all(),
      "SF6 a look-back case has not been seen, so clause 6.3 is false")
    # SF6b every window the longest observed delay resolves, and the register as a whole, name the
    # same three lines, so no choice of estimation window can move the call
    longest = int(d["delay"].max())
    A(longest == W.DELAY_CAP, "SF6b the longest observed delay is not the record's cap")
    wins = [(lo, hi) for lo in ("2020-07", "2020-10", "2021-01", "2021-04", "2021-07", "2021-10",
                                "2022-01")
            for hi in ("2023-06", "2023-09", "2023-12", "2024-01", "2024-02")
            if G.months(lo, hi) >= 24] + [("2020-07", W.AS_OF.strftime("%Y-%m"))]
    for lo, hi in wins:
        e = {}
        for n in [l[0] for l in W.LINES]:
            gg = d[(d["line"] == n) & (d["onset_month"] >= lo) & (d["onset_month"] <= hi)]
            e[n] = len(gg) / G.months(lo, hi) * float(gg["delay"].mean())
        A(sorted(sorted(e, key=lambda n: -e[n])[:W.CAPACITY]) == g["covered"],
          "SF6b window %s..%s moves the call" % (lo, hi))
    A(len(wins) >= 30, "SF6b too few windows swept")
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
    # SF13 the expectation, and nothing in the pack saying how it is formed
    A("expected to be carrying" in fw, "SF13 clause 6.2 does not file the expectation")
    A("closed record" not in fw, "SF13 clause 6.2 still points at a record to estimate from")
    A("whether or not the bank yet holds a record of it" in fw,
      "SF13 clause 6.2 does not say the unobserved cases are in the population")
    A(len(d[(d["onset_month"] <= W.REVIEW_FROM.strftime("%Y-%m")) &
            (d["first_seen_month"] > W.REVIEW_FROM.strftime("%Y-%m"))]) == 0,
      "SF13 the register can be read as holding the unseen cases, so no construction is forced")
    # SF15 the count at a month end: a case seen in the month it began was never carried
    hb = doc_text(target, "investigation_handbook.pdf")
    A("A case seen in the month it began was never carried unseen past any month end" in hb,
      "SF15 the handbook does not close the count at a month end")
    inc = {}
    for n in [l[0] for l in W.LINES]:
        gg = d[(d["line"] == n) & (d["onset_month"] >= cf) & (d["onset_month"] <= ct)]
        inc[n] = len(gg) / G.months(cf, ct) * (float(gg["delay"].mean()) + 1.0)
    inc_top = sorted(sorted(inc, key=lambda n: -inc[n])[:W.CAPACITY])
    A(inc_top != g["covered"],
      "SF15 the inclusive month count gives the same call, so nothing turns on the sentence")
    third = sorted(((inc[n], n) for n in inc), reverse=True)[W.CAPACITY - 1][0]
    fourth = sorted(((inc[n], n) for n in inc), reverse=True)[W.CAPACITY][0]
    A(third / fourth >= 1.06,
      "SF15 the inclusive month count is a coin flip, not a named wrong answer")

    # SF14 the disposition: counting the cases that were put forward and not accepted gives the
    # same three lines, so no reading of the register's disposition field can move the call
    A(set(cases["disposition"]) == {"confirmed", "withdrawn"}, "SF14 the register's dispositions")
    A((cases.loc[cases["disposition"] == "withdrawn", "confirmed_month"] == "").all(),
      "SF14 a withdrawn case carries a confirmed month")
    A((cases.loc[cases["disposition"] == "confirmed", "confirmed_month"] != "").all(),
      "SF14 a confirmed case carries no confirmed month")
    A("withdrawn for one that was put to them and not accepted" in doc_text(
        target, "extract_dictionary.pdf"), "SF14 the dictionary does not define the disposition")
    wide = cases.copy()
    wide["ver"] = pd.to_numeric(wide["record_version"], errors="coerce")
    wide = wide.sort_values(["case_id", "ver"]).groupby("case_id", as_index=False).tail(1)
    nmw = G.line_now(lines)
    wide["line"] = [nmw.get(x, x) for x in wide["line_code"]]
    wide["delay"] = [G.months(o, f) - 1 for o, f in zip(wide["onset_month"], wide["first_seen_month"])]
    wide = wide.drop_duplicates(subset=["customer_ref", "typology", "line"])
    A(len(wide) > len(d), "SF14 the wider reading adds no case")
    ew = {}
    for n in [l[0] for l in W.LINES]:
        gw = wide[(wide["line"] == n) & (wide["onset_month"] >= cf) & (wide["onset_month"] <= ct)]
        ew[n] = len(gw) / G.months(cf, ct) * float(gw["delay"].mean())
    A(sorted(sorted(ew, key=lambda n: -ew[n])[:W.CAPACITY]) == g["covered"],
      "SF14 counting the withdrawn cases moves the call")
    # A2 the screening ask: an entry is removed once, so "an entry a later version removed" and
    # "an entry on the list at screening that a later version removed" select the same matches
    seen_removed = []
    for v in lists["versions"]:
        seen_removed += list(v["entries_removed"])
    A(len(seen_removed) == len(set(seen_removed)), "A2 an entry is removed by two versions")
    added_at = {}
    for v in lists["versions"]:
        for e in v["entries_added"]:
            added_at[e] = v["in_force_from"]
    A(all(r.list_entry in added_at for r in matches.itertuples()),
      "A2 a match names an entry no version ever added")
    A(all(added_at[r.list_entry] <= r.screened_on for r in matches.itertuples()),
      "A2 a match was recorded before its entry was on the list")
    # A1 the reissued reversal moves the quarter it sits in by more than the stated rounding
    led = ledger.copy()
    led["h"] = pd.to_numeric(led["hours"])
    for q, want in g["a1"].items():
        gq = led[led["quarter"] == q]
        A(abs(round(float(gq["h"].sum()), 1) - want["hours_billed"]) >= 0.1 * 30 or
          q != "2026-Q1", "A1 the reissued reversal does not move %s" % q)

    # A1 the quarter a ticket is billed to is the quarter it is dated in, so no reading forks
    led = ledger.copy()
    for r in led.itertuples():
        y, q = r.quarter.split("-Q")
        mo = int(r.ticket_date[5:7])
        A((mo - 1) // 3 + 1 == int(q) and r.ticket_date[:4] == y,
          "A1 ticket %s is dated outside the quarter it is billed to" % r.ticket)
    A("the contract quarter the ticket is billed to" in doc_text(target, "extract_dictionary.pdf"),
      "A1 the dictionary does not say what the quarter field is")
    A("a rate the card does not carry for its work type" in doc_text(target, "contract_register.pdf"),
      "A1 the contract does not say what is outside the rate card")

    # A3 every triage lands on a working day, and clause 7.2 pins the count exactly
    shut = {dt.date.fromisoformat(x) for x in
            pd.read_csv(os.path.join(target, "bank_closed_days.csv"), dtype=str)["closed_on"]}
    A(len(shut) >= 12, "A3 the pack ships too few closed days")
    tri = alerts[alerts["stage"].isin(["triaged", "escalated", "reopened"])]
    for x in set(tri["stage_at"]):
        day = dt.date.fromisoformat(x)
        A(day.weekday() < 5 and day not in shut, "A3 an adjudication fell on %s, a closed day" % x)
    A("A working day is a day from Monday to Friday that is not a day the bank is closed" in fw,
      "A3 clause 7.2 does not pin the working day")
    A("from the day after the alert was raised up to and including the day the triage recorded it"
      in fw, "A3 clause 7.2 does not pin how the days are counted")

    # A2 no match is recorded against an entry the list had already removed
    removed_on = {}
    for v in lists["versions"]:
        for e in v["entries_removed"]:
            removed_on[e] = v["in_force_from"]
    for r in matches.itertuples():
        A(removed_on.get(r.list_entry, "9999") > r.screened_on,
          "A2 match %s is against an entry already removed" % r.match_id)

    # the register as a record: amended cases past a second version, and identifiers with gaps
    A(set(cases["record_version"]) >= {"1", "2", "3"}, "the register holds no third version")
    ids = sorted({int(x[4:]) for x in cases["case_id"]})
    steps = [b - a for a, b in zip(ids, ids[1:])]
    A(max(ids) - min(ids) + 1 > len(ids), "the register's identifiers run without gaps")
    A(steps.count(1) / len(steps) > 0.75, "the register's identifiers do not mostly run consecutively")
    A(max(steps) > 4, "the register's identifiers never jump")

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
