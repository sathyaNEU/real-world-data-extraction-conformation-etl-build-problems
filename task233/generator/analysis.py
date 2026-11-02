"""Every rung, the golden and the ask figures, computed from target/ alone."""
import csv
import datetime as dt
import math
import os
import re
from collections import defaultdict

from openpyxl import load_workbook

from io_util import pdf_text

QUARTER = ["2026-07", "2026-08", "2026-09"]


def d_parse(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return dt.datetime.strptime(str(v).strip(), "%d/%m/%Y").date()


class Pack:
    def __init__(self, target):
        self.t = target
        self.read()

    def f(self, name):
        return os.path.join(self.t, name)

    def csv(self, name):
        with open(self.f(name), encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))

    def read(self):
        # outlet register
        wb = load_workbook(self.f("cpi_outlet_register_2026-10.xlsx"))
        ws = wb["Outlets"]
        rows = list(ws.iter_rows(values_only=True))
        hdr = rows[0]
        self.outlets = [dict(zip(hdr, r)) for r in rows[1:]]
        self.by_code = {o["Outlet code"]: o for o in self.outlets}
        self.by_tnum = {o["Contractor outlet no."]: o for o in self.outlets}
        reg = list(wb["Regions"].iter_rows(values_only=True))
        self.regions = [r[0] for r in reg[1:]]
        self.region_name = {r[0]: r[1] for r in reg[1:]}
        self.area_region = {r[2]: r[0] for r in reg[1:]}
        # item list and status codes
        self.item_class = {r["item_code"]: r["coicop_class"] for r in self.csv("cpi_item_list_2026.csv")}
        self.status = {r["status"]: r["meaning"] for r in self.csv("handheld_status_codes.csv")}
        # price database, one row per quote and month (a re-sent upload is the same row again)
        seen = {}
        for r in self.csv("cpi_field_quotes_2025-10_2026-09.csv"):
            k = (r["ref_month"], r["quote_id"])
            if k in seen:
                continue
            seen[k] = r
        self.quotes = seen
        self.months = sorted({k[0] for k in seen})
        # back-check register
        wb = load_workbook(self.f("fqt_backcheck_register_2026q3.xlsx"))
        bc, raw = [], 0
        for ws in wb.worksheets:
            rows = list(ws.iter_rows(values_only=True))
            hi = [i for i, r in enumerate(rows) if r and r[0] == "Region"][0]
            hdr = rows[hi]
            month = dt.datetime.strptime(rows[1][0].split(": ")[1], "%B %Y").strftime("%Y-%m")
            keep = []
            for r in rows[hi + 1:]:
                if not r or r[0] is None:
                    continue
                raw += 1
                d = dict(zip(hdr, r))
                rec = (month, d["Region"], d["Outlet"], str(d["Quote"]), d["Item"], d["Collector price"],
                       d_parse(d["Re-collected on"]), d["FQT price"], d["Found"], d["Officer"])
                if rec in keep:
                    continue
                keep.append(rec)
            bc += keep
        self.bc_raw = raw
        self.backchecks = [dict(month=r[0], region=r[1], outlet=r[2], quote=r[3], item=r[4], rec=float(r[5]),
                                when=r[6], fqt=None if r[7] in (None, "") else float(r[7]), found=r[8] == "Y")
                           for r in bc]
        # visit log
        self.visits = self.csv("tallis_visit_log_2026-07_2026-09.csv")
        self.visit_days = defaultdict(list)
        for v in self.visits:
            if int(v["prices_entered"]) == 0:
                continue
            d = dt.date.fromisoformat(v["started"][:10])
            self.visit_days[(v["outlet_no"], v["started"][:7])].append(d)
        # calendar, schedule, reviews
        cal = self.csv("nso_collection_calendar_2026.csv")
        self.index_days = {r["date"][:7]: dt.date.fromisoformat(r["date"]) for r in cal if r["event"] == "Index day"}
        self.holidays = {dt.date.fromisoformat(r["date"]) for r in cal if r["event"] == "Public holiday"}
        self.schedule = self.csv("tallis_collection_schedule_2026q3.csv")
        wb = load_workbook(self.f("commodity_replacement_decisions_2026.xlsx"))
        rows = list(wb["Decisions"].iter_rows(values_only=True))
        self.reviews = [dict(zip(rows[0], r)) for r in rows[1:]]
        # governing documents
        self.pcqs_text = pdf_text(self.f("pcqs_price_collection_quality_standard_v3.pdf"))
        fee_text = pdf_text(self.f("pcsa_schedule4_collection_fees.pdf"))
        self.fees = {m.group(1): int(m.group(2).replace(",", ""))
                     for m in re.finditer(r"(CR\d\d)\s.*?\s([\d,]{5,})", fee_text)}
        self.band_compliant = float(re.search(r"(\d\d\.\d) per cent or more", self.pcqs_text).group(1))
        self.band_credit = float(re.search(r"Below (\d\d\.\d) per cent\b(?! and)", self.pcqs_text).group(1))
        self.credit_rate = float(re.search(r"credit of (\d+) per cent", self.pcqs_text).group(1)) / 100

    # helpers ------------------------------------------------------------------------------------
    def stratum(self, code):
        return "M" if self.by_code[code]["Outlet type"] == "Multiple" else "I"

    def is_workday(self, d):
        return d.weekday() < 5 and d not in self.holidays

    def window(self, month):
        d, out = self.index_days[month], []
        while len(out) < 5:
            if self.is_workday(d):
                out.append(d)
            d += dt.timedelta(days=1)
        return out

    def outcome(self, a):
        return "Compliant" if a >= self.band_compliant else ("Corrective action" if a >= self.band_credit else "Service credit")

    # monthly frequency of a recorded price change ---------------------------------------------
    def change_frequency(self, key="class", months=None):
        months = months or self.months
        cmp_, chg = defaultdict(int), defaultdict(int)
        pos = {m: i for i, m in enumerate(self.months)}
        byq = defaultdict(dict)
        for (m, q), r in self.quotes.items():
            byq[q][m] = r
        priced = {"P", "R", "10", "30"}
        same = {"P", "10"}
        for q, d in byq.items():
            for m in d:
                i = pos[m]
                if i == 0 or m not in months:
                    continue
                a, b = d.get(self.months[i - 1]), d[m]
                if a is None or a["status"] not in priced or b["status"] not in same:
                    continue
                k = self.fkey(dict(item=b["item_code"], outlet=b["outlet_code"]), key)
                cmp_[k] += 1
                chg[k] += abs(float(a["price"]) - float(b["price"])) > 0.004
        return {k: chg[k] / cmp_[k] for k in cmp_}

    def fkey(self, b, key):
        if key == "class":
            return (self.item_class[b["item"]], self.stratum(b["outlet"]))
        if key == "item":
            return (b["item"], self.stratum(b["outlet"]))
        if key == "stratum":
            return self.stratum(b["outlet"])
        region = self.by_code[b["outlet"]]["Region"]
        if key == "region":
            return (region, self.item_class[b["item"]], self.stratum(b["outlet"]))
        if key == "region_class":
            return (region, self.item_class[b["item"]])
        if key == "region_only":
            return region
        return "all"

    def visit_date(self, b):
        tnum = self.by_code[b["outlet"]]["Contractor outlet no."]
        days = self.visit_days[(tnum, b["month"])]
        assert len(days) == 1, (b["outlet"], b["month"], days)
        return days[0]

    def lag(self, b, basis="visit", workdays=False):
        start = self.visit_date(b) if basis == "visit" else self.index_days[b["month"]]
        if not workdays:
            return (b["when"] - start).days
        n, d = 0, start
        while d < b["when"]:
            d += dt.timedelta(days=1)
            if self.is_workday(d):
                n += 1
        return n

    # the call ------------------------------------------------------------------------------------
    def counted(self):
        return [b for b in self.backchecks if b["found"]]

    def agreement(self, exclude_class=None):
        out = {}
        for r in self.regions:
            v = [b for b in self.counted() if b["region"] == r and (exclude_class is None or not self.item_class[b["item"]].startswith(exclude_class))]
            out[r] = 100.0 * sum(abs(b["rec"] - b["fqt"]) < 0.005 for b in v) / len(v)
        return out

    def netted(self, key="class", form="exp", basis="visit", workdays=False, f=None, months=None):
        f = f or self.change_frequency(key, months)
        out = {}
        for r in self.regions:
            v = [b for b in self.counted() if b["region"] == r]
            agree = sum(abs(b["rec"] - b["fqt"]) < 0.005 for b in v)
            s = 0.0
            for b in v:
                ff = f[self.fkey(b, key)]
                L = self.lag(b, basis, workdays)
                s += (1 - ff) ** (L / 30.4) if form == "exp" else 1 - ff * L / 30.4
            out[r] = 100.0 * agree / s
        return out

    def persistence(self):
        """a disagreement counts as a genuine change when the collector's price is the previous month's and
        the officer's is the next month's"""
        out = {}
        nxt = {"2026-07": "2026-08", "2026-08": "2026-09"}
        prv = {"2026-07": "2026-06", "2026-08": "2026-07", "2026-09": "2026-08"}
        for r in self.regions:
            v = [b for b in self.counted() if b["region"] == r]
            err = 0
            for b in v:
                if abs(b["rec"] - b["fqt"]) < 0.005:
                    continue
                n = self.quotes.get((nxt.get(b["month"], ""), b["quote"]))
                p = self.quotes.get((prv[b["month"]], b["quote"]))
                ok = (n is not None and n["price"] and abs(float(n["price"]) - b["fqt"]) < 0.005 and
                      p is not None and p["price"] and abs(float(p["price"]) - b["rec"]) < 0.005)
                err += not ok
            out[r] = 100.0 * (1 - err / len(v))
        return out

    def golden(self):
        return self.netted()

    def outcomes(self, acc):
        return {r: self.outcome(a) for r, a in acc.items()}

    def credit(self, outs):
        return sum(round(self.credit_rate * self.fees[r], 2) for r, o in outs.items() if o == "Service credit")

    # ask 1: timeliness and missed visits ----------------------------------------------------------
    def successor(self, o):
        """the outlet that took over a sold branch: the same address, in the sample from the day after"""
        if o["In sample to"] is None:
            return None
        end = d_parse(o["In sample to"])
        for x in self.outlets:
            if x["Address"] == o["Address"] and x["In sample from"] is not None and d_parse(x["In sample from"]) == end + dt.timedelta(days=1):
                return x
        return None

    def timeliness(self, follow_takeover=True, holidays=True, last_visit=True):
        done, total, missed = defaultdict(int), defaultdict(int), defaultdict(int)
        for s in self.schedule:
            o = self.by_tnum[s["outlet_no"]]
            region = self.area_region[s["area"]]
            month = s["month"]
            tnum = s["outlet_no"]
            first = dt.date.fromisoformat(month + "-01")
            if follow_takeover and o["In sample to"] is not None and d_parse(o["In sample to"]) < first:
                succ = self.successor(o)
                if succ is not None:
                    tnum = succ["Contractor outlet no."]
            days = sorted(self.visit_days.get((tnum, month), []))
            total[region] += 1
            if not days:
                missed[region] += 1
                continue
            if holidays:
                win = self.window(month)
            else:
                d0 = self.index_days[month]
                win = [d0 + dt.timedelta(days=k) for k in range(7) if (d0 + dt.timedelta(days=k)).weekday() < 5][:5]
            check = days if last_visit else days[:1]
            if all(win[0] <= d <= win[-1] for d in check):
                done[region] += 1
        return ({r: 100.0 * done[r] / total[r] for r in self.regions}, {r: missed[r] for r in self.regions})

    # ask 2: replacement acceptance ------------------------------------------------------------------
    def replacement_events(self):
        ev = []
        for (m, q), r in self.quotes.items():
            if r["status"] in ("R", "30") and m >= "2026-06":
                tnum = self.by_code[r["outlet_code"]]["Contractor outlet no."]
                days = sorted(self.visit_days.get((tnum, m), []))
                region = self.by_code[r["outlet_code"]]["Region"]
                ev.append(dict(month=m, quote=q, region=region, day=days[0] if days else dt.date.fromisoformat(m + "-01")))
        return ev

    def acceptance(self, assign="asof", date_filter=False):
        ev = self.replacement_events()
        byq = defaultdict(list)
        for e in ev:
            byq[e["quote"]].append(e)
        for q in byq:
            byq[q].sort(key=lambda e: e["day"])
        latest = {}
        for rv in sorted(self.reviews, key=lambda x: (d_parse(x["Decided on"]), x["Review no."])):
            when = d_parse(rv["Decided on"])
            if date_filter and not (dt.date(2026, 7, 1) <= when <= dt.date(2026, 9, 30)):
                continue
            q = str(rv["Quote"])
            cands = [e for e in byq.get(q, []) if e["day"] < when]
            if not cands:
                continue
            if assign == "asof":
                targets = [cands[-1]]
            else:
                targets = byq[q]
            if rv["Decision"] == "Query to contractor":
                continue
            for e in targets:
                latest[(e["quote"], e["month"])] = rv["Decision"]
        acc, tot = defaultdict(int), defaultdict(int)
        for e in ev:
            if e["month"] not in QUARTER:
                continue
            tot[e["region"]] += 1
            acc[e["region"]] += latest.get((e["quote"], e["month"])) == "Comparable"
        return {r: 100.0 * acc[r] / tot[r] for r in self.regions}, dict(tot)


def run(target):
    p = Pack(target)
    gold = p.golden()
    outs = p.outcomes(gold)
    tim, missed = p.timeliness()
    accp, ntot = p.acceptance()
    return dict(pack=p, golden=gold, outcomes=outs, credit=p.credit(outs), timeliness=tim, missed=missed,
                acceptance=accp, replacements=ntot)


if __name__ == "__main__":
    import sys
    res = run(sys.argv[1] if len(sys.argv) > 1 else "../target")
    p = res["pack"]
    ag = p.agreement()
    for r in p.regions:
        print(r, "%.2f" % ag[r], p.outcome(ag[r])[:4], "%.2f" % res["golden"][r], res["outcomes"][r][:4],
              "%.1f" % res["timeliness"][r], res["missed"][r], "%.1f" % res["acceptance"][r], res["replacements"].get(r))
    print("credit", res["credit"], "default credit", p.credit(p.outcomes(ag)))
