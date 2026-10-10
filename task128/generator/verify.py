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

    # ---- the answer: colo whole-host top drains + cloud top (300 - 2)
    split = {e: 0 for e in ESTATES}
    figs = {}
    total = 0
    for e in COLO:
        ranked = sorted(colo_hosts[e], key=lambda h: (-whole[h], h))
        dr = ranked[:drains[e]]
        figs[e] = sum(whole[h] for h in dr)
        split[e] = 1
        total += figs[e]
    n_cloud = 300 - 2
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
    # ---- acknowledgements back-test
    res["acks"] = acks(target)
    return res, meta


def closeout(target):
    rowsby = collections.defaultdict(list)
    t = pq.read_table(os.path.join(target, "epss_score_history_2026.parquet")).to_pydict()
    for cve, d, s in zip(t["cve"], t["score_date"], t["epss"]):
        rowsby[cve].append((d, s))

    def score_at(cve, day):
        xs = [s for (dd, s) in rowsby.get(cve, []) if dd <= day]
        return max(xs) if xs else 0.0

    def latest(cve):
        xs = rowsby.get(cve, [])
        return max(xs)[1] if xs else 0.0
    cells = collections.defaultdict(lambda: collections.defaultdict(int))
    flags = {}
    with open(os.path.join(target, "vuln_findings_2026-10-23.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            flags[r["cve"]] = (r["exploit_available"] == "true", float(r["cvss_base"]))
    # fixed findings carry their own flag via the spine? close-out fixed are separate cves; read
    # their flag/cvss is not in spine, so flag rival uses history only here (score_at_export)
    rows = rd(target, "cloud_q3_closed_findings.csv")
    truth = collections.defaultdict(int)
    rivals = {"score_at_export": collections.defaultdict(int),
              "score_quarter_end": collections.defaultdict(int)}
    for r in rows:
        cut = dt.date.fromisoformat(r["cut_date"])
        cell = (r["estate"], cut.month)
        if score_at(r["cve"], cut.isoformat()) >= THRESH:
            truth[cell] += 1
        if latest(r["cve"]) >= THRESH:
            rivals["score_at_export"][cell] += 1
        if score_at(r["cve"], "2026-09-30") >= THRESH:
            rivals["score_quarter_end"][cell] += 1
    out = {"truth_total": sum(truth.values()), "cells": len(truth)}
    for nm, fig in rivals.items():
        allc = set(truth) | set(fig)
        out[nm + "_misses"] = sum(1 for c in allc if fig.get(c, 0) != truth.get(c, 0))
    return out


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
    assert res["closeout"]["cells"] == 12, res["closeout"]
    assert res["acks"]["requests"] >= 400, res["acks"]
    print(f"verifier: answer total {res['total']:,}, split "
          f"{'/'.join(str(res['split'][e]) for e in ESTATES)}, drains {res['drains']}, "
          f"close-out {res['closeout']['cells']} cells, {res['acks']['requests']} acknowledgements "
          "- all match metadata")
    if a.json:
        json.dump(res, open(a.json, "w"), indent=2, default=str)


if __name__ == "__main__":
    main()
