"""Independent verification: reads only the shipped bundle and figures.json, by its own code path."""
import datetime as dt
import json
import os
import re
import sys

import pandas as pd
import pdfplumber

CAP = 3
CLOSED = ("2021-01", "2024-01")
TWO_Q = ("2026-07", "2026-12")
STANDARD = 5
HOLIDAYS = {dt.date(2026, 1, 1), dt.date(2026, 1, 2), dt.date(2026, 2, 6), dt.date(2026, 4, 3),
            dt.date(2026, 4, 6), dt.date(2026, 4, 27), dt.date(2026, 6, 1), dt.date(2026, 10, 26),
            dt.date(2026, 12, 25), dt.date(2026, 12, 28), dt.date(2027, 1, 1), dt.date(2027, 1, 4)}
K = [0]


def ok(cond, msg):
    K[0] += 1
    if not cond:
        raise AssertionError("verify: " + msg)


def mon(a, b):
    return (int(b[:4]) - int(a[:4])) * 12 + int(b[5:7]) - int(a[5:7])


def wdays(a, b):
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in HOLIDAYS:
            n += 1
    return n


def run(target, figures):
    fig = json.load(open(figures, encoding="utf-8"))
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "fewer than ten files")
    ok(len({os.path.splitext(f)[1] for f in files}) >= 3, "fewer than three formats")
    rd = lambda n: pd.read_csv(os.path.join(target, n), dtype=str, keep_default_na=False)
    cases = rd("confirmed_case_register.csv")
    alerts = rd("alert_adjudication_extract.csv")
    lines = rd("line_structure_register.csv")
    xw = rd("customer_id_crosswalk.csv")
    ledger = rd("contractor_hours_ledger.csv")
    matches = rd("screening_match_log.csv")
    lists = json.load(open(os.path.join(target, "screening_list_versions.json"), encoding="utf-8"))
    man = rd("extract_manifest.csv")
    ok(len(alerts) >= 25000, "the alert extract holds %d rows" % len(alerts))
    ok(int(man.loc[man["file_name"] == "alert_adjudication_extract.csv", "row_count"].iloc[0])
       == len(alerts), "the manifest disagrees on the alert extract")

    # the business line in force now, for every code the records carry
    cur = {r.line_code: r.line_name for r in lines.itertuples() if r.status == "current"}
    now = {r.line_code: cur[r.current_line_code] for r in lines.itertuples()}

    c = cases.copy()
    c["v"] = pd.to_numeric(c["record_version"])
    c = c.sort_values(["case_id", "v"]).groupby("case_id", as_index=False).tail(1)
    c = c[c["disposition"] == "confirmed"]
    c["line"] = [now[x] for x in c["line_code"]]
    c = c.drop_duplicates(subset=["customer_ref", "typology", "line"])
    c["delay"] = [mon(o, f) for o, f in zip(c["onset_month"], c["first_seen_month"])]

    nmon = mon(CLOSED[0], CLOSED[1]) + 1
    exp, flow, coh, wbar, closedn = {}, {}, {}, {}, {}
    for name, g in c.groupby("line"):
        cl = g[(g["onset_month"] >= CLOSED[0]) & (g["onset_month"] <= CLOSED[1])]
        lam = len(cl) / nmon
        w = float(cl["delay"].mean())
        exp[name] = lam * w
        coh[name] = sum(int((cl["delay"] > k).sum()) for k in range(0, 72)) / nmon
        wbar[name] = w
        closedn[name] = len(cl)
        flow[name] = len(g[(g["confirmed_month"] >= TWO_Q[0]) & (g["confirmed_month"] <= TWO_Q[1])])
    ok(len(exp) == fig["lines_assessed"], "assessed %d lines" % len(exp))
    covered = sorted(sorted(exp, key=lambda n: -exp[n])[:CAP])
    ok(covered == fig["covered"], "the call is %s" % covered)
    rest = sorted(((exp[n], n) for n in exp if n not in covered), reverse=True)
    ok(rest[0][1] == fig["just_misses"], "the line that just misses is %s" % rest[0][1])
    ok(sorted(sorted(coh, key=lambda n: -coh[n])[:CAP]) == covered,
       "the cohort estimator disagrees with the product")
    ok(sorted(sorted(flow, key=lambda n: -flow[n])[:CAP]) == fig["rungs"]["rung0_confirmed_two_quarters"],
       "rung 0 does not reproduce")
    for n in exp:
        ok(flow[n] == fig["confirmed_two_quarters"][n], "confirmed cases at %s" % n)
        ok(abs(round(exp[n], 1) - fig["expected_carrying"][n]) < 1e-9, "expectation at %s" % n)
        ok(abs(round(wbar[n], 1) - fig["months_unseen"][n]) < 1e-9, "months unseen at %s" % n)
        ok(closedn[n] == fig["closed_cases"][n], "closed cases at %s" % n)
    v = sorted(exp.values(), reverse=True)
    ok(int(round(100 * (v[CAP - 1] / v[CAP] - 1))) == fig["cut_margin_pct"], "the cut margin")

    # A1: the reissued credit notes are owed once
    allowed = {"2026-Q1": 420.0, "2026-Q2": 420.0, "2026-Q3": 480.0, "2026-Q4": 480.0}
    l = ledger.copy()
    l["h"] = pd.to_numeric(l["hours"])
    l["rate"] = pd.to_numeric(l["hourly_rate"])
    l = l.sort_values(["ticket", "reference"]).groupby("ticket", as_index=False).head(1)
    for q, want in fig["a1_contract"].items():
        gq = l[l["quarter"] == q]
        ok(round(float(gq["h"].sum()), 1) == want["hours_billed"], "A1 hours at %s" % q)
        ok(allowed[q] == want["hours_allowed"], "A1 allowed at %s" % q)
        ok(int((gq["rate"] != 285.0).sum()) == want["tickets_outside_rate_card"], "A1 rate card at %s" % q)

    # A2: the list version in force at the screening date
    vers = lists["versions"]
    later = {}
    for i, vv in enumerate(vers):
        s = set()
        for w in vers[i + 1:]:
            s |= set(w["entries_removed"])
        later[vv["version"]] = s
    inforce = sorted((vv["in_force_from"], vv["version"]) for vv in vers)
    got = {vv["version"]: [0, 0] for vv in vers}
    for r in matches.itertuples():
        v = None
        for frm, nm in inforce:
            if frm <= r.screened_on:
                v = nm
        if v and r.list_entry in later[v]:
            got[v][0] += 1
            if r.outcome == "cleared":
                got[v][1] += 1
    for v, want in fig["a2_screening"].items():
        ok(got[v][0] == want["matched_an_entry_later_removed"], "A2 matches at %s" % v)
        ok(got[v][1] == want["of_those_cleared"], "A2 cleared at %s" % v)

    # A3: working days, and the re-sent batch counted once
    al = alerts[alerts["queue"].isin(["card disputes", "chargebacks"])].copy()
    al = al[~al["batch_id"].str.endswith("R")]
    al["raised"] = pd.to_datetime(al["raised_at"]).dt.date
    al["at"] = pd.to_datetime(al["stage_at"]).dt.date
    al = al[(al["raised"] >= dt.date(2026, 1, 1)) & (al["raised"] <= dt.date(2026, 12, 31))]
    for m in range(1, 13):
        gm = al[[x.month == m for x in al["raised"]]]
        want = fig["a3_queue"]["2026-%02d" % m]
        ok(int((gm["stage"] == "raised").sum()) == want["alerts_raised"], "A3 raised in month %d" % m)
        tri = gm[gm["stage"] == "triaged"]
        ok(sum(1 for r in tri.itertuples() if wdays(r.raised, r.at) <= STANDARD)
           == want["closed_inside_standard"], "A3 inside the standard in month %d" % m)
        ok(int((gm["stage"] == "escalated").sum()) == want["escalated"], "A3 escalated in month %d" % m)

    # no shipped document names the decisive step, and the clauses the call rests on are present
    blob = ""
    for f in files:
        if f.endswith(".pdf"):
            with pdfplumber.open(os.path.join(target, f)) as pdf:
                blob += " " + " ".join(p.extract_text() or "" for p in pdf.pages)
        elif f.endswith((".csv", ".json")):
            blob += " " + open(os.path.join(target, f), encoding="utf-8", errors="ignore").read()
    low = re.sub(r"\s+", " ", blob).lower()
    for banned in ("multiplied by", "arrival", "per month", "stock of", "little's law", "mean time"):
        ok(banned not in low, "a shipped file says '%s'" % banned)
    for needed in ("a case is one customer and one typology", "the review covers three business lines",
                   "expected to be carrying", "began between 1 january 2021 and 31 january 2024",
                   "which is the first seen month the investigation handbook defines"):
        ok(needed in low, "a shipped file no longer says '%s'" % needed)

    # the deliverables agree with figures.json
    task = os.path.dirname(os.path.abspath(target.rstrip("/")))
    xl = os.path.join(task, "golden", "review_placement_2027.xlsx")
    if os.path.exists(xl):
        rows = pd.read_excel(xl, sheet_name="Placement 2027", header=4, dtype=object)
        rows = rows[rows["Business line"].notna()]
        cov = [str(r[1]) for r in rows.itertuples() if str(r[3]) == "yes"]
        ok(sorted(cov) == fig["covered"], "the workbook covers %s" % sorted(cov))
    return K[0]


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    figs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")
    print("independent checks passed:", run(tgt, figs))
