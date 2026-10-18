"""The asks, computed on the cut pack: bottles CMS delivered to each region's ART facilities in C4 and C5 by the date
each delivery was signed for, and bottles those facilities reported dispensing in their reports for the months of
C4 and C5, each facility counted in its current region; the chart's national months. Every handling a solver might
take is a named route, so checks.py and cracker.py score the same constructions.

Routes for the facility's region:
  "registry_dated"   the registry record valid for the code on the event's date (the golden): a reissued code's
                     closed site before its closure, its new site from its opening
  "registry_current" the registry's operational record for the code
  "label"            the region the source row carries (CMS's customer master for a delivery, the requisition
                     group's region at submission for a report)
Routes for a delivery's date: "signed" (the proof of delivery, the golden) or "posted".
Routes for a report: "approved" (the golden) or "all" (every submission summed) or "latest" (the latest submission)."""
from __future__ import annotations

import csv
import datetime as dt
import json
import os

D = dt.date
REGIONS = ["Capital", "Central", "Northern", "Eastern", "Southern", "Western"]
CYCLES = {"C4": (D(2025, 7, 1), D(2025, 12, 31)), "C5": (D(2026, 1, 1), D(2026, 6, 30))}
TLD = "ARV0412"
TLD_ALL = ("ARV0412", "ARV0412D")


def _rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


class Pack:
    def __init__(self, pack):
        self.reg = _rows(os.path.join(pack, "facility_registry_extract_2026-09-01.csv"))
        self.acc = {r["account"]: r for r in _rows(os.path.join(pack, "cms_customer_accounts_2026-09-02.csv"))}
        self.lines = _rows(os.path.join(pack, "cms_deliveries_tld_2025-07_2026-08.csv"))
        self.pod = {r["delivery_no"]: r for r in _rows(os.path.join(pack, "cms_pod_2025-07_2026-08.csv"))}
        self.lmis = json.load(open(os.path.join(pack, "lmis_monthly_reports_2025-07_2026-08.json"), encoding="utf-8"))
        self.by_code = {}
        for r in self.reg:
            self.by_code.setdefault(r["mfl_code"], []).append(r)

    def region(self, code, d, route, label=None):
        recs = self.by_code.get(code, [])
        if route == "label":
            return label
        if not recs:
            return None
        if route == "registry_current":
            op = [r for r in recs if r["status"] == "Operational"]
            return (op or recs)[0]["region"]
        # the record operating in the event's month: a reissued code's closed site to its closure month, its new site
        # from its opening month (no month holds both)
        mo = (d.year, d.month)
        hit = []
        for r in recs:
            o = D.fromisoformat(r["opened_on"])
            c = D.fromisoformat(r["closed_on"]) if r["closed_on"] else D(2100, 1, 1)
            if (o.year, o.month) <= mo <= (c.year, c.month):
                hit.append(r)
        assert len(hit) == 1, (code, d, len(hit))
        return hit[0]["region"]


def deliveries(P, region_route="registry_dated", date_route="signed", depot=False, refusals="exclude"):
    """Bottles by (region, cycle) and national by month. A delivery refused at the gate (its proof of delivery
    records the refusal, and a return line brings the goods back) was not delivered."""
    out = {(r, c): 0 for r in REGIONS for c in CYCLES}
    month = {}
    for ln in P.lines:
        if ln["delivery_type"] == "LR":
            continue
        if ln["delivery_type"] != "LF" and not depot:
            continue
        pod = P.pod.get(ln["delivery_no"])
        if refusals == "exclude" and pod is not None and pod["signed_by"].startswith("Refused"):
            continue
        if date_route == "signed":
            if pod is None:
                continue
            d = D.fromisoformat(pod["signed_on"])
        else:
            d = D.fromisoformat(ln["posting_date"])
        q = int(ln["qty"])
        a = P.acc[ln["customer"]]
        reg = P.region(a["mfl_code"], d, region_route, ln["delivery_region"]) if a["mfl_code"] else ln["delivery_region"]
        if region_route == "label":
            reg = ln["delivery_region"]
        for c, (lo, hi) in CYCLES.items():
            if lo <= d <= hi and reg in REGIONS:
                out[(reg, c)] += q
        month[(d.year, d.month)] = month.get((d.year, d.month), 0) + q
    return out, month


def dispensing(P, region_route="registry_dated", report_route="approved", products="tld_all"):
    out = {(r, c): 0 for r in REGIONS for c in CYCLES}
    month = {}
    reqs = P.lmis["requisitions"]
    if report_route == "latest":
        last = {}
        for q in reqs:
            k = (q["facilityCode"], q["period"])
            if k not in last or q["submittedAt"] > last[k]["submittedAt"]:
                last[k] = q
        use = list(last.values())
    elif report_route == "approved":
        use = [q for q in reqs if q["status"] == "Approved"]
    else:
        use = list(reqs)
    for q in use:
        y, m = int(q["period"][:4]), int(q["period"][5:])
        d = D(y, m, 15)
        codes = TLD_ALL if products == "tld_all" else (TLD,)
        disp = sum(li["quantityDispensed"] for li in q["lineItems"] if li["productCode"] in codes)
        reg = q["region"] if region_route == "label" else P.region(q["facilityCode"], d, region_route)
        for c, (lo, hi) in CYCLES.items():
            if lo <= d <= hi and reg in REGIONS:
                out[(reg, c)] += disp
        month[(y, m)] = month.get((y, m), 0) + disp
    return out, month


def chart(P, **kw):
    """The chart's bars: each region's deliveries and dispensing in C4 and C5 (the table's figures)."""
    dl, _ = deliveries(P, **{k: v for k, v in kw.items() if k in ("region_route", "date_route", "depot", "refusals")})
    sp, _ = dispensing(P, **{k: v for k, v in kw.items() if k in ("region_route", "report_route", "products")})
    return dict(delivered=dl, dispensed=sp)


def golden(P):
    a, _ = deliveries(P)
    b, _ = dispensing(P)
    ch = chart(P)
    return dict(A=a, B=b, chart=ch)
