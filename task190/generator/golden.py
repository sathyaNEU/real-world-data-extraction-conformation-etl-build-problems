"""Everything the submission states, recomputed from the shipped bundle alone."""
import datetime as dt
import json
import os

import pandas as pd

import pack as PK
import world as W

Q_FROM, Q_TO = "2026-07", "2026-12"          # the two complete quarters before the extract date


def load(target):
    rd = lambda k: pd.read_csv(os.path.join(target, PK.FILES[k]), dtype=str, keep_default_na=False)
    cases = rd("cases")
    alerts = rd("alerts")
    lines = rd("lines")
    xw = rd("crosswalk")
    backlog = rd("backlog")
    ledger = rd("ledger")
    matches = rd("matches")
    lists = json.load(open(os.path.join(target, PK.FILES["lists"]), encoding="utf-8"))
    base = pd.read_excel(os.path.join(target, PK.FILES["base"]), sheet_name="Customers by line",
                         header=None, dtype=object)
    return cases, alerts, lines, xw, backlog, ledger, matches, lists, base


def line_now(lines):
    """code as recorded -> the business line in force at the review date"""
    cur = {r.line_code: r.line_name for r in lines.itertuples() if r.status == "current"}
    return {r.line_code: cur[r.current_line_code] for r in lines.itertuples()}


def months(a, b):
    return (int(b[:4]) - int(a[:4])) * 12 + (int(b[5:7]) - int(a[5:7])) + 1


def governing_cases(cases, lines):
    """clause 2.3 and the handbook: one confirmed case per customer and typology, latest version"""
    d = cases.copy()
    d["ver"] = pd.to_numeric(d["record_version"], errors="coerce")
    d = d.sort_values(["case_id", "ver"]).groupby("case_id", as_index=False).tail(1)
    d = d[d["disposition"] == "confirmed"]
    nm = line_now(lines)
    d["line"] = [nm.get(x, x) for x in d["line_code"]]
    d["delay"] = [months(o, f) - 1 for o, f in zip(d["onset_month"], d["first_seen_month"])]
    return d.drop_duplicates(subset=["customer_ref", "typology", "line"])


def assess(target):
    cases, alerts, lines, xw, backlog, ledger, matches, lists, base = load(target)
    d = governing_cases(cases, lines)
    cf, ct = W.CLOSED_FROM.strftime("%Y-%m"), W.CLOSED_TO.strftime("%Y-%m")
    nmonths = months(cf, ct)
    out = {}
    for name in [l[0] for l in W.LINES]:
        g = d[d["line"] == name]
        closed = g[(g["onset_month"] >= cf) & (g["onset_month"] <= ct)]
        lam_m = len(closed) / nmonths
        w_hat = float(closed["delay"].mean())
        cohort = sum(int((closed["delay"] > k).sum()) for k in range(0, 72)) / nmonths
        conf2q = len(g[(g["confirmed_month"] >= Q_FROM) & (g["confirmed_month"] <= Q_TO)])
        out[name] = {"closed_cases": len(closed), "arrivals_a_month": lam_m, "months_unseen": w_hat,
                     "expected_carrying": lam_m * w_hat, "cohort_estimate": cohort,
                     "confirmed_two_quarters": conf2q}
    return out, (cases, alerts, lines, xw, backlog, ledger, matches, lists, base)


def ladder(target):
    a, _ = assess(target)
    cust = {l[0]: l[3] for l in W.LINES}
    bl = {l[0]: l[5] for l in W.LINES}
    pick = lambda key: sorted(sorted(a, key=lambda n: -key(n))[:W.CAPACITY])
    return {
        "rung0_confirmed_two_quarters": pick(lambda n: a[n]["confirmed_two_quarters"]),
        "rung1_confirmed_per_thousand": pick(lambda n: a[n]["confirmed_two_quarters"] / cust[n]),
        "rung2_alert_backlog": pick(lambda n: bl[n]),
        "rung3_months_unseen": pick(lambda n: a[n]["months_unseen"]),
        "answer_expected_carrying": pick(lambda n: a[n]["expected_carrying"]),
        "answer_cohort_estimate": pick(lambda n: a[n]["cohort_estimate"]),
    }


def working_days(a, b):
    n, d = 0, a
    while d < b:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in W.HOLIDAYS:
            n += 1
    return n


def ask_contract(target):
    """A1: the contractor's quarters, with the reissued credit notes counted once"""
    _, (cases, alerts, lines, xw, backlog, ledger, matches, lists, base) = assess(target)
    allowed = {"2026-Q1": 420.0, "2026-Q2": 420.0, "2026-Q3": 480.0, "2026-Q4": 480.0}
    d = ledger.copy()
    d["h"] = pd.to_numeric(d["hours"])
    d["rate"] = pd.to_numeric(d["hourly_rate"])
    d = d.sort_values(["ticket", "reference"]).groupby(["ticket"], as_index=False).head(1)
    out = {}
    for q in sorted(allowed):
        g = d[d["quarter"] == q]
        out[q] = {"hours_billed": round(float(g["h"].sum()), 1), "hours_allowed": allowed[q],
                  "tickets_outside_rate_card": int((g["rate"] != 285.0).sum())}
    return out


def ask_screening(target):
    """A2: per list version, the customers who matched an entry a later version removed"""
    _, (cases, alerts, lines, xw, backlog, ledger, matches, lists, base) = assess(target)
    vers = lists["versions"]
    removed_later = {}
    for i, v in enumerate(vers):
        later = set()
        for w in vers[i + 1:]:
            later |= set(w["entries_removed"])
        removed_later[v["version"]] = later
    inforce = []
    for v in vers:
        inforce.append((v["in_force_from"], v["version"]))
    inforce.sort()

    def version_at(day):
        cur = None
        for frm, name in inforce:
            if frm <= day:
                cur = name
        return cur

    out = {v["version"]: {"matched_an_entry_later_removed": 0, "of_those_cleared": 0} for v in vers}
    for r in matches.itertuples():
        v = version_at(r.screened_on)
        if v is None:
            continue
        if r.list_entry in removed_later[v]:
            out[v]["matched_an_entry_later_removed"] += 1
            if r.outcome == "cleared":
                out[v]["of_those_cleared"] += 1
    return out


def ask_queue(target):
    """A3: the card disputes queue by month of 2026, on working days and without the re-sent batch"""
    _, (cases, alerts, lines, xw, backlog, ledger, matches, lists, base) = assess(target)
    d = alerts.copy()
    d = d[d["queue"].isin(["card disputes", "chargebacks"])]
    d = d[~d["batch_id"].str.endswith("R")]
    d["raised"] = pd.to_datetime(d["raised_at"]).dt.date
    d["at"] = pd.to_datetime(d["stage_at"]).dt.date
    d = d[(d["raised"] >= dt.date(2026, 1, 1)) & (d["raised"] <= dt.date(2026, 12, 31))]
    out = {}
    for m in range(1, 13):
        g = d[[x.month == m for x in d["raised"]]]
        raised = g[g["stage"] == "raised"]
        tri = g[g["stage"] == "triaged"]
        inside = sum(1 for r in tri.itertuples() if working_days(r.raised, r.at) <= W.WORKING_STANDARD)
        esc = int((g["stage"] == "escalated").sum())
        out["2026-%02d" % m] = {"alerts_raised": len(raised), "closed_inside_standard": inside,
                                "escalated": esc}
    return out


def compute(target):
    a, _ = assess(target)
    L = ladder(target)
    picked = L["answer_expected_carrying"]
    rest = sorted(((a[n]["expected_carrying"], n) for n in a if n not in picked), reverse=True)
    return {"covered": picked, "just_misses": rest[0][1], "assess": a, "rungs": L,
            "a1": ask_contract(target), "a2": ask_screening(target), "a3": ask_queue(target)}
