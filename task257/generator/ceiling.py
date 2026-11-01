"""The ask layer's honest ceiling, measured on the cut pack (task257/target.zip) by a cracker written from the files
alone. It shares no code with the generator: it reads the zip and the golden figures (generator/figures.json) and
nothing else.

The cracker landed the call and runs the hygiene battery (supplemental-stumping 1.1c) and every filed rule it points
at: Kestrava's test tokens out; the last submission of a personal link (standard 3.2); a kiosk session joined to the
employee number it was signed in with (re-padded to seven digits); the close at 23:59 local time at the employee's
site (3.1), the site held in HR on the opening day (3.4) and its time zone from the site directory; a printed form's
answers dated by its envelope's sealed date (the paper returns log says the export records them when keyed); then
each store employee's department on the opening day by the HR report's row in force that day (3.4), the response
rate on the employees assigned that day (4.3) and the stores where a department team has 10 or more respondents
(4.1). It reads the department as the report names it, the way every as-of join reads a dimension column.

Stress rows (not the gate) are printed beside it: each employee's latest row, each employee's own 1 October row, and
the full includer who reads every September code through the 1 October reorganisation rows.

    python3 task257/generator/ceiling.py [path/to/target.zip]"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import sys
import zipfile

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
OFF = {"America/Toronto": -4, "America/Winnipeg": -5, "America/Moncton": -3}
OPEN, SEP30, OCT1 = "2026-09-14", "2026-09-30", "2026-10-01"


def load(zp):
    z = zipfile.ZipFile(zp)
    raw = {n: z.read(n) for n in z.namelist()}
    csv = lambda n, **kw: pd.read_csv(io.BytesIO(raw[n]), **kw)
    T = {
        "resp": csv("kestrava_brackenmere_2026_responses.csv", comment="#", dtype=str),
        "subs": csv("kestrava_brackenmere_2026_submissions.csv", dtype=str),
        "dist": csv("kestrava_brackenmere_2026_distribution_list.csv", dtype=str),
        "hr": csv("hris_assignment_history_2026.csv", comment="#", dtype=str, keep_default_na=False),
        "sites": csv("site_directory_2026-10.csv", dtype=str, keep_default_na=False),
        "kiosk": pd.read_json(io.BytesIO(raw["kiosk_sessions_2026-09.jsonl"]), lines=True, dtype=False),
        "paper": pd.read_excel(io.BytesIO(raw["paper_returns_engagement_2026.xlsx"]), header=4),
    }
    return T, raw


def in_force(hr, day):
    h = hr[hr["action"] != "termination"]
    end = hr[hr["action"] == "termination"].groupby("employee_id")["effective_from"].min().to_dict()
    h = h[(h["effective_from"] <= day) & ((h["effective_to"] == "") | (h["effective_to"] >= day))]
    return h[[not (e in end and end[e] <= day) for e in h["employee_id"]]]


def respondents(T):
    """The cracker's respondents: employees with an answer to one of the 30 items before their site's close."""
    resp, subs = T["resp"], T["subs"]
    resp = resp[~resp["token"].isin(set(subs.loc[subs["status"] == "test", "token"]))].copy()
    resp["submission"] = resp["submission"].astype(int)
    resp = resp[resp["submission"] == resp.groupby("token")["submission"].transform("max")]
    resp = resp[resp["item"] != "ENPS"]
    emp = dict(zip(T["dist"]["token"], T["dist"]["employee_id"]))
    emp.update({s: "%07d" % int(e) for s, e in zip(T["kiosk"]["session"], T["kiosk"]["employee"])})
    resp["emp"] = resp["token"].map(emp)
    op = in_force(T["hr"], OPEN)
    site = dict(zip(op["employee_id"], op["site_no"]))
    tz = dict(zip(T["sites"]["site_no"], T["sites"]["time_zone"]))
    close = {z: (dt.datetime(2026, 9, 27, 23, 59, 59) - dt.timedelta(hours=o)).strftime("%Y-%m-%dT%H:%M:%SZ")
             for z, o in OFF.items()}
    lim = resp["emp"].map(lambda e: close[tz.get(site.get(e), "America/Toronto")])
    ok = resp["answered_at"] <= lim
    ch = subs.drop_duplicates("token").set_index("token")["channel"]
    pap = resp["token"].map(ch) == "paper"
    dsite = dict(zip(T["dist"]["token"], T["dist"]["site_no"]))
    env = T["paper"]
    sealed = {(str(int(s)), pd.Timestamp(k).date().isoformat()): pd.Timestamp(x).date().isoformat()
              for s, k, x in zip(env["Site"], env["Keyed"], env["Sealed"])}
    ok[pap] = [sealed.get((dsite[t], a[:10]), "9999") <= "2026-09-27"
               for t, a in zip(resp.loc[pap, "token"], resp.loc[pap, "answered_at"])]
    return set(resp.loc[ok, "emp"])


def departments(T, mode):
    """employee -> (store site, department) on the opening day under one reading of the HR report."""
    hr, sites = T["hr"], T["sites"]
    stores = set(sites.loc[sites["site_type"] == "store", "site_no"])
    h = in_force(hr, OPEN)
    h = h[h["site_no"].isin(stores)]
    if mode == "cracker":
        dep = list(h["department"])
    elif mode == "latest":
        live = hr[hr["action"] != "termination"].sort_values(["employee_id", "effective_from"])
        last = live.groupby("employee_id")["department"].last().to_dict()
        dep = [last[e] for e in h["employee_id"]]
    elif mode == "own_1_october":
        o = hr[(hr["effective_from"] == OCT1) & (hr["action"] == "reorganisation")]
        nxt = dict(zip(o["employee_id"], o["department"]))
        dep = [nxt.get(e, d) for e, d in zip(h["employee_id"], h["department"])]
    else:   # the full includer
        b = in_force(hr, SEP30)
        b = b[b["site_no"].isin(stores)]
        o = hr[(hr["effective_from"] == OCT1) & (hr["action"] == "reorganisation")]
        m = b.merge(o, on=["employee_id", "site_no"], suffixes=("_b", "_a"))
        votes = m.groupby(["department_code_b", "department_a"]).size()
        code = {}
        for (c, d), n in votes.items():
            if c not in code or n > votes[(c, code[c])]:
                code[c] = d
        dep = [code[c] for c in h["department_code"]]
    return {e: (s, d) for e, s, d in zip(h["employee_id"], h["site_no"], dep)}


def figures(od, rs):
    resp, head, team = {}, {}, {}
    for e, (s, d) in od.items():
        head[d] = head.get(d, 0) + 1
        if e in rs:
            resp[d] = resp.get(d, 0) + 1
            team[(s, d)] = team.get((s, d), 0) + 1
    rate = {d: round(100.0 * resp.get(d, 0) / head[d], 1) for d in head}
    shown = {d: sum(1 for (s, dd), n in team.items() if dd == d and n >= 10) for d in head}
    return resp, rate, shown


def score(fig, got):
    resp, rate, shown = got
    cells = []
    for d in fig["dept_respondents"]:
        cells.append(("respondents", d, resp.get(d), fig["dept_respondents"][d]))
        cells.append(("response rate", d, rate.get(d), fig["dept_rate"][d]))
        cells.append(("stores shown", d, shown.get(d), fig["dept_stores_shown"][d]))
    hits = [c for c in cells if c[2] is not None and abs(c[2] - c[3]) < (0.05 if c[0] == "response rate" else 0.5)]
    return hits, cells


def main(zp=None):
    zp = zp or os.path.join(TASK, "target.zip")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    T, _ = load(zp)
    rs = respondents(T)
    if not rs:
        raise SystemExit("ceiling.py: the cracker found no respondent in %s; nothing to score, no verdict" % zp)
    if len(fig.get("dept_respondents", {})) != 8:
        raise SystemExit("ceiling.py: figures.json holds %d store departments, not 8; no verdict" %
                         len(fig.get("dept_respondents", {})))
    digest = hashlib.sha256(open(zp, "rb").read()).hexdigest()[:8]
    print("pack target.zip %s; cracker's respondents %d (figures.json %d)" % (digest, len(rs), fig["respondents"]))
    rows = {}
    for mode in ("cracker", "latest", "own_1_october", "full_includer"):
        hits, cells = score(fig, figures(departments(T, mode), rs))
        if len(cells) != 24 or not any(c[2] is not None for c in cells):
            raise SystemExit("ceiling.py: %s scored %d cells with values; no verdict" % (mode, len(cells)))
        rows[mode] = len(hits)
        print("%-14s keeps %2d of %d department cells%s" % (mode, len(hits), len(cells),
                                                            "  (the gate)" if mode == "cracker" else "  (stress)"))
        if mode == "cracker":
            for c in cells:
                print("    %-14s %-17s cracker %8s  golden %8s  %s" % (c[0], c[1], c[2], c[3],
                                                                    "hit" if c in hits else "miss"))
    # pair arithmetic on 38 / 7 / 55; ask criteria: 24 department cells and the chart's three parts (the
    # construction layer: the cracker has the latent eigenvalues, the mirror on the Pearson rung keeps the axes)
    n_ask = 24 + 3
    kc = (rows["cracker"] + 3) / n_ask
    km = (rows["cracker"] + 1) / n_ask
    C = 38 + 7 + 55 * kc
    M = 5 + 7 + 55 * km
    print("cracker %.1f (ask weight kept %.1f%%), mirror %.1f (%.1f%%): pair ceiling %.1f" % (
        C, 100 * kc, M, 100 * km, (C + M) / 2))
    F = 38 + 7 + 55 * (rows["full_includer"] + 3) / n_ask
    print("stress: the full includer with the call landed %.1f; pair with the mirror on its path %.1f" % (
        F, (F + 5 + 7 + 55 * (rows["full_includer"] + 1) / n_ask) / 2))
    return rows


if __name__ == "__main__":
    main(*(sys.argv[1:2]))
