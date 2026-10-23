"""The cracker and the mirror on the cut pack, and the pair ceiling on supplemental-stumping Part 0's weights
(call and components 38, instructions 7, asks 55 over the ask figures; a response off the call keeps 5).

The cracker lands the call (so it already filters services open at October 31, 2026 and reads closures from the
service accounts), runs the hygiene battery and executes every filed rule: it converts the CRM's UTC times to local
time, drops cases closed as duplicates, finds the duplicated meter-months of the load-research extract and drops
them with the usual keep-first, takes a service's time on R-TOU from the rate row in effect at October 31, 2026,
and places a request in the district of the service the case names. The mirror stops off the call and takes every
table at face value: UTC months, every case, every extract row, every R-TOU row in effect."""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import solve         # noqa: E402

T = os.path.join(C.TASK, "target")
ASOF = pd.Timestamp("2026-10-31")
CUT = pd.Timestamp("2025-11-01")


def ask_a(F, careful):
    sa, rate, ami = F["sa"], F["rate"], F["ami"]
    r = rate[(rate.rate_code == "R-TOU") & (rate.f <= ASOF) & (rate.t.isna() | (rate.t >= ASOF))]
    r = r.merge(sa[["service_acct", "district", "status"]], on="service_acct")
    if careful:
        r = r[r.status == "Active"]
    a = ami[ami.bill_month.isin(solve.TEST) & ami.service_acct.isin(r.service_acct)]
    if careful:
        a = a.drop_duplicates(["meter_no", "bill_month"])          # the battery's repair, pandas keep-first
    kwh = a.groupby("service_acct").kwh_1600_2100.sum()
    night = a.groupby("service_acct").kwh_2300_0600.sum()
    r = r.assign(k=r.service_acct.map(kwh).fillna(0.0), n=r.service_acct.map(night).fillna(0.0), long=r.f <= CUT)
    g = r.groupby("district").agg(twelve=("long", "sum"), kwh=("k", "sum"), night=("n", "sum"))
    return {d: dict(twelve=int(g.twelve.get(d, 0)), kwh=int(round(g.kwh.get(d, 0))), night=int(round(g.night.get(d, 0)))) for d in C.DISTRICTS}


def ask_b(F, careful):
    crm = pd.read_excel(os.path.join(T, C.F_CRM), dtype=str)
    if careful:
        crm["lm"] = solve.local_month(crm.received_utc)
        crm = crm[crm.status != "Closed - duplicate"]
    else:
        crm["lm"] = crm.received_utc.str[:7]
    r = crm[(crm.request == "Enrol R-TOU") & crm.lm.isin(solve.ASK_MONTHS)]
    r = r.merge(F["sa"][["service_acct", "district"]], on="service_acct")
    g = r.groupby("district").size(); w = r[r.channel == "Web form"].groupby("district").size()
    return {d: dict(requests=int(g.get(d, 0)), web=int(w.get(d, 0))) for d in C.DISTRICTS}


def score(fig, A, B):
    keys, hits = [], []
    for d in C.DISTRICTS:
        k = C.DCODE[d]
        for name, v in (("a_%s_twelve_months" % k, A[d]["twelve"]), ("a_%s_kwh_4to9pm" % k, A[d]["kwh"]),
                        ("a_%s_kwh_11pmto6am" % k, A[d]["night"]), ("b_%s_requests" % k, B[d]["requests"]), ("b_%s_web" % k, B[d]["web"])):
            keys.append(name); hits.append(abs(v - fig[name]) <= 0.5)
    return keys, hits


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    F = solve.frames(T)
    out = {}
    for who, careful in (("cracker", True), ("mirror", False)):
        keys, hits = score(fig, ask_a(F, careful), ask_b(F, careful))
        out[who] = (keys, hits)
    n = len(out["cracker"][0])
    kc, km = sum(out["cracker"][1]), sum(out["mirror"][1])
    c = 38 + 7 + 55 * kc / n
    s = 5 + 7 + 55 * km / n
    for who in ("cracker", "mirror"):
        keys, hits = out[who]
        for part in ("a_", "b_"):
            sel = [h for kk, h in zip(keys, hits) if kk.startswith(part)]
            print("%-8s ask %s keeps %d of %d" % (who, part[0].upper(), sum(sel), len(sel)))
    print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (c, s, (c + s) / 2, 100 * km / n))
    return (c + s) / 2, 100 * km / n, kc


if __name__ == "__main__":
    main()
