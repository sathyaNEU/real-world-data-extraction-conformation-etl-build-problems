#!/usr/bin/env python3
"""Independent verifier for task128. Reads only <task>/target and <task>/metadata.json and
recomputes the answer split, every graded figure, the ladder ordering, and the two calibration
back-tests, sharing no code path with the generator.

    python3 -I verify.py /path/to/task128 [--json out.json]
"""
import argparse
import collections
import csv
import datetime as dt
import json
import math
import os
import sys

import openpyxl
import pyarrow.parquet as pq

ESTATES = ["payments", "checkout", "search", "media", "tools", "pipeline"]
COLO = ["payments", "checkout"]
CLOUD = ["search", "media", "tools", "pipeline"]
RANK = {e: i for i, e in enumerate(ESTATES)}
LABEL2E = {"Payments": "payments", "Checkout": "checkout", "Search": "search", "Media": "media",
           "Internal tools": "tools", "Data pipeline": "pipeline"}
RACK = 40
THRESH = 0.10


def rd(path, name):
    with open(os.path.join(path, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def latest_scores(path):
    t = pq.read_table(os.path.join(path, "epss_score_history_2026.parquet")).to_pydict()
    last = {}
    for cve, d, s in zip(t["cve"], t["score_date"], t["epss"]):
        if cve not in last or d > last[cve][0]:
            last[cve] = (d, s)
    return {c: v[1] for c, v in last.items()}


def score_on(path, cutmap):
    """Score of each cve on a given date (max over dates <= cut)."""
    t = pq.read_table(os.path.join(path, "epss_score_history_2026.parquet")).to_pydict()
    out = collections.defaultdict(lambda: None)
    rowsby = collections.defaultdict(list)
    for cve, d, s in zip(t["cve"], t["score_date"], t["epss"]):
        rowsby[cve].append((d, s))
    return rowsby


def verify(path):
    res = {}
    target = os.path.join(path, "target")
    meta = json.load(open(os.path.join(path, "metadata.json")))

    # ---- cloud candidate values: exploitable-now open findings per (estate, package)
    latest = latest_scores(target)
    cloudv = collections.defaultdict(int)
    with open(os.path.join(target, "vuln_findings_2026-10-23.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            s = latest.get(r["cve"])
            if s is not None and s >= THRESH:
                cloudv[(r["estate"], r["package"])] += 1

    # ---- colocated whole-host exposure from the feed
    whole = collections.defaultdict(int)
    est_of = {}
    with open(os.path.join(target, "colocation_managed_host_findings_2026-10-23.jsonl"),
              encoding="utf-8") as f:
        for line in f:
            o = json.loads(line)
            whole[o["host_id"]] += 1
            est_of[o["host_id"]] = o["estate"]
    colo_hosts = collections.defaultdict(list)
    for h, e in est_of.items():
        colo_hosts[e].append(h)

    # ---- November drains from the calendar + forecast + capacity register
    cap = {}
    wb = openpyxl.load_workbook(os.path.join(target, "colocation_capacity_register_2026-10.xlsx"))
    ws = wb["Capacity"]
    hdr = [c.value for c in ws[1]]
    for row in ws.iter_rows(min_row=2, values_only=True):
        d = dict(zip(hdr, row))
        if d["month"] == "2026-11":
            cap[d["estate"]] = (int(d["hosts_in_service"]), float(d["per_host_tps"]),
                                int(d["failure_domain_hosts"]))
    # forecast: max tps over each window's hours
    fc = collections.defaultdict(dict)
    with open(os.path.join(target, "estate_transaction_forecast_2026.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            fc[(r["estate"], r["date"])][int(r["hour"])] = float(r["tps"])
    drains = {e: 0 for e in COLO}
    per_window = collections.defaultdict(list)
    for r in rd(target, "november_window_calendar.csv"):
        e = r["estate"]
        n, per, rack = cap[e]
        hh = r["window_hours_local"]
        sh = int(hh[:2]); eh = int(hh[6:8])
        hours = [(sh + k) % 24 for k in range((eh - sh) % 24 or 24)]
        peak = max(fc[(e, r["window_date"])][h] for h in hours)
        needed = math.ceil(peak / per)
        concurrent = n - needed - rack
        drains[e] += concurrent * int(r["drain_cycles"])
        per_window[e].append((r["window_date"], concurrent * int(r["drain_cycles"])))

    # ---- the answer: one colocated ticket per window (each its share of the top hosts), then the
    # cloud tickets that take out the most
    split = {e: 0 for e in ESTATES}
    figs = {}
    total = 0
    for e in COLO:
        ranked = sorted(colo_hosts[e], key=lambda h: (-whole[h], h))
        dr = ranked[:drains[e]]
        figs[e] = sum(whole[h] for h in dr)
        split[e] = sum(1 for _, c in per_window[e] if c > 0)
        total += figs[e]
    n_cloud = 300 - split["payments"] - split["checkout"]
    cs = sorted(((v, RANK[e], e, p) for (e, p), v in cloudv.items() if v > 0),
                key=lambda x: (-x[0], x[1], x[3]))
    chosen = cs[:n_cloud]
    cloud_fig = collections.defaultdict(int)
    for v, _, e, p in chosen:
        split[e] += 1
        cloud_fig[e] += v
        total += v
    for e in CLOUD:
        figs[e] = cloud_fig[e]
    res["split"] = split
    res["figs"] = figs
    res["total"] = total
    res["last_in"] = chosen[-1][0]
    res["first_below"] = cs[n_cloud][0] if len(cs) > n_cloud else None
    res["drains"] = drains

    # ---- close-out back-test from the fixed findings
    res["closeout"] = closeout(target)
    res["crewlog"] = crewlog(target)
    # ---- acknowledgements back-test
    res["acks"] = acks(target)
    res["one_request"] = one_request(target)
    return res, meta


def one_request(target):
    """Every colocated ticket in the crew log rode exactly one office change request, ran only on
    that request's window dates, on exactly the hosts the provider accepted."""
    wb = openpyxl.load_workbook(os.path.join(target,
                               "colocation_change_acknowledgements_may_oct_2026.xlsx"))
    ws = wb["Acknowledgements"]
    hdr = [c.value for c in ws[1]]
    acks_ = {r[0]: dict(zip(hdr, r)) for r in ws.iter_rows(min_row=2, values_only=True)}
    tk = collections.defaultdict(list)
    for r in rd(target, "crew_deployment_log_2026.csv"):
        if r["estate"] in COLO:
            tk[r["ticket_id"]].append(r)
    bad, part = 0, 0
    for t, rs in tk.items():
        crs = {r["change_request"] for r in rs}
        if len(crs) != 1:
            bad += 1
            continue
        a = acks_[next(iter(crs))]
        wd = dt.date.fromisoformat(str(a["window_date"])[:10])
        days = {r["run_date"] for r in rs}
        ok = [r for r in rs if r["outcome"] == "succeeded"]
        if not days <= {wd.isoformat(), (wd + dt.timedelta(days=1)).isoformat()} or \
                len(ok) != int(a["hosts_accepted"]):
            bad += 1
        if int(a["hosts_accepted"]) < int(a["hosts_requested"]):
            part += 1
    return {"tickets": len(tk), "violations": bad, "part_accepted": part}


def closeout(target):
    """Back-test the Q3 close-out: every closed finding counted on its CVE's score on the ticket's
    cut day exactly, against the 12 estate-month cells printed in the close-out PDF."""
    import re
    import pypdf
    day = {}
    t = pq.read_table(os.path.join(target, "epss_score_history_2026.parquet")).to_pydict()
    for cve, d, s in zip(t["cve"], t["score_date"], t["epss"]):
        day[(cve, str(d)[:10])] = s
    rows = rd(target, "cloud_q3_closed_findings.csv")
    truth = collections.defaultdict(int)
    latest = latest_scores(target)
    rivals = {"score_at_export": collections.defaultdict(int)}
    missing = 0
    for r in rows:
        cut = r["cut_date"]
        cell = (r["estate"], int(cut[5:7]))
        s = day.get((r["cve"], cut))
        if s is None:
            missing += 1
            continue
        if s >= THRESH:
            truth[cell] += 1
        if latest.get(r["cve"], 0.0) >= THRESH:
            rivals["score_at_export"][cell] += 1
    text = " ".join(pg.extract_text() for pg in
                    pypdf.PdfReader(os.path.join(target, "q3_2026_remediation_closeout.pdf")).pages)
    printed = {}
    for lab, e in LABEL2E.items():
        if e not in CLOUD:
            continue
        m = re.search(re.escape(lab) + r"\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", text)
        assert m, f"close-out row {lab} not found"
        vals = [int(x.replace(",", "")) for x in m.groups()]
        for mo, v in zip((7, 8, 9), vals[:3]):
            printed[(e, mo)] = v
    match = sum(1 for c in printed if printed[c] == truth.get(c, 0))
    rows_ = len(rows)
    cves = len({r["cve"] for r in rows})
    out = {"truth_total": sum(truth.values()), "printed_total": sum(printed.values()),
           "cells": match, "missing_cut_scores": missing, "rows": rows_, "distinct_cves": cves}
    for nm, fig in rivals.items():
        out[nm + "_misses"] = sum(1 for c in printed if fig.get(c, 0) != printed[c])
    return out


def crewlog(target):
    """No host run precedes its ticket's vendor release; every ticket's vendor_first_release is the
    first_published of one advisory of its package in the feed, and none equals a republish date."""
    feed = json.load(open(os.path.join(target, "vendor_advisory_feed.json"), encoding="utf-8"))
    firsts = collections.defaultdict(set)
    revs = collections.defaultdict(set)
    for a in feed:
        firsts[a["package"]].add(a["first_published"])
        if a["latest_revision"] != a["first_published"]:
            revs[a["package"]].add(a["latest_revision"])
    early, unmatched, on_rev = 0, set(), set()
    for r in rd(target, "crew_deployment_log_2026.csv"):
        if r["run_date"] < r["vendor_first_release"]:
            early += 1
        if r["vendor_first_release"] not in firsts[r["package"]]:
            unmatched.add(r["ticket_id"])
        if r["vendor_first_release"] in revs[r["package"]]:
            on_rev.add(r["ticket_id"])
    return {"runs_before_release": early, "unmatched": len(unmatched), "on_revision": len(on_rev)}


def acks(target):
    wb = openpyxl.load_workbook(os.path.join(target,
                               "colocation_change_acknowledgements_may_oct_2026.xlsx"))
    ws = wb["Acknowledgements"]
    hdr = [c.value for c in ws[1]]
    rows = [dict(zip(hdr, r)) for r in ws.iter_rows(min_row=2, values_only=True)]
    tot = sum(int(r["hosts_accepted"]) for r in rows)
    return {"requests": len(rows), "accepted_total": tot}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task")
    ap.add_argument("--json")
    a = ap.parse_args()
    res, meta = verify(a.task)
    # checks against metadata
    assert res["total"] == meta["answer"]["total_exposures"], \
        f'total {res["total"]} vs meta {meta["answer"]["total_exposures"]}'
    for e in ESTATES:
        assert res["split"][e] == meta["answer"]["split"][e], f"split {e}"
        assert res["figs"][e] == meta["answer"]["exposures_taken_out"][e], f"fig {e}"
    assert res["drains"]["payments"] == 96 and res["drains"]["checkout"] == 120, res["drains"]
    assert res["closeout"]["cells"] == 12 and res["closeout"]["missing_cut_scores"] == 0, \
        res["closeout"]
    assert res["closeout"]["truth_total"] == res["closeout"]["printed_total"], res["closeout"]
    assert res["closeout"]["score_at_export_misses"] >= 3, res["closeout"]
    assert res["closeout"]["distinct_cves"] < res["closeout"]["rows"] * 0.6, res["closeout"]
    assert res["crewlog"] == {"runs_before_release": 0, "unmatched": 0, "on_revision": 0}, \
        res["crewlog"]
    assert res["acks"]["requests"] >= 400, res["acks"]
    assert res["one_request"]["violations"] == 0 and res["one_request"]["part_accepted"] >= 6, \
        res["one_request"]
    assert (res["split"]["payments"], res["split"]["checkout"]) == (4, 5), res["split"]
    print(f"verifier: answer total {res['total']:,}, split "
          f"{'/'.join(str(res['split'][e]) for e in ESTATES)}, drains {res['drains']}, "
          f"close-out {res['closeout']['cells']} of 12 cells at {res['closeout']['truth_total']:,}, {res['acks']['requests']} acknowledgements "
          "- all match metadata")
    if a.json:
        json.dump(res, open(a.json, "w"), indent=2, default=str)


if __name__ == "__main__":
    main()
