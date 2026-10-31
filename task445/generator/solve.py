"""The golden, computed from target/ alone: each place's residents' deaths from 1 June to 31 August 2026 (the
register's entries plus the medical examiner offices' deaths that are not on it, linked on surname, forenames,
date of birth and date of death), the excess over Table 1 and the qualifying places; the two asks; and every rung
the checks price, each a parameter here."""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict

from openpyxl import load_workbook
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as PK  # noqa: E402
import world as W  # noqa: E402


def pdate(s):
    s = s.strip()
    if "/" in s:
        d, m, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s)


class Pack:
    def __init__(self, target=W.TARGET):
        self.target = target
        self.places = {}
        with open(os.path.join(target, PK.LOOKUP), encoding="utf-8") as fh:
            self.lookup = {r["postcode"]: r["place_name"] for r in csv.DictReader(fh)}
            fh.seek(0)
            self.code_place = {r["place_code"]: r["place_name"] for r in csv.DictReader(fh)}
        with open(os.path.join(target, PK.REG), encoding="utf-8") as fh:
            self.reg = list(csv.DictReader(fh))
        for r in self.reg:
            r["_reg"] = pdate(r["date_of_registration"])
            r["_dod"] = pdate(r["date_of_death"])
            r["_dob"] = pdate(r["date_of_birth"])
            r["_place"] = self.code_place[r["usual_residence_code"]]
        self.expected = self._table1()
        self.north = self._north()
        self.south = self._south()

    def _table1(self):
        txt = "\n".join(p.extract_text() for p in PdfReader(os.path.join(self.target, PK.TERMS)).pages)
        out = {}
        for p in W.NAMES:
            m = re.search(re.escape(p) + r"\s+E\d{8}\s+([\d,]+)", txt)
            out[p] = int(m.group(1).replace(",", ""))
        return out

    def _north(self):
        ws = load_workbook(os.path.join(self.target, PK.NORTH), read_only=True)["Scrutiny log"]
        rows = []
        it = ws.iter_rows(values_only=True)
        hdr = next(it)
        for v in it:
            r = dict(zip(hdr, v))
            sur, fn = [s.strip() for s in r["Deceased"].split(",", 1)]
            rows.append(dict(office="North", ref=r["Case ref"], surname=sur, forenames=fn,
                             dob=r["Date of birth"].date(), dod=r["Date of death"].date(), pc=r["Usual postcode"],
                             completed=r["Scrutiny completed"].date(), outcome=r["Outcome"],
                             cref=r["Coroner ref"] or "", decision=r["Coroner decision"] or ""))
        return rows

    def _south(self):
        doc = json.load(open(os.path.join(self.target, PK.SOUTH), encoding="utf-8"))
        rows = []
        for c in doc["cases"]:
            ts = dt.datetime.strptime(c["scrutiny"]["completed_at"], "%Y-%m-%dT%H:%M:%SZ")
            local = ts + dt.timedelta(hours=1 if bst(ts.date()) else 0)
            co = c["coroner"] or {}
            rows.append(dict(office="South", ref=c["case_id"], surname=c["deceased"]["family_name"],
                             forenames=c["deceased"]["given_names"],
                             dob=dt.date.fromisoformat(c["deceased"]["date_of_birth"]),
                             dod=dt.date.fromisoformat(c["death"]["date"]), pc=c["death"]["usual_postcode"],
                             completed=local.date(), outcome=c["scrutiny"]["outcome"],
                             cref=co.get("reference") or "", decision=co.get("decision") or ""))
        return rows


def bst(d):
    a = dt.date(d.year, 3, 31) - dt.timedelta(days=(dt.date(d.year, 3, 31).weekday() + 1) % 7)
    b = dt.date(d.year, 10, 31) - dt.timedelta(days=(dt.date(d.year, 10, 31).weekday() + 1) % 7)
    return a <= d < b


def key(sur, fn, dob, dod):
    return (sur.strip().lower(), fn.strip().lower(), dob, dod)


def entries(P, latest=False):
    """one row per register entry: the Registration row, or with latest=True the last row recorded for it"""
    out = {}
    for r in P.reg:
        k = (r["registration_district"], int(r["entry_number"]))
        if k not in out:
            out[k] = r
        elif latest and int(r["version"]) > int(out[k]["version"]):
            out[k] = r
        elif not latest and r["version"] == "1":
            out[k] = r
    return out


def window_register(P, w0=W.W0, w1=W.W1):
    return [r for r in entries(P).values() if w0 <= r["_dod"] <= w1]


def me_deaths(P, w0=W.W0, w1=W.W1):
    """the residents' deaths in the logs, one per person"""
    out = {}
    for r in P.north + P.south:
        if not (w0 <= r["dod"] <= w1):
            continue
        place = P.lookup.get(r["pc"])
        if place is None:
            continue
        out.setdefault(key(r["surname"], r["forenames"], r["dob"], r["dod"]), (place, r))
    return out


def golden_counts(P, w0=W.W0, w1=W.W1):
    reg = window_register(P, w0, w1)
    keys = {key(r["deceased_surname"], r["deceased_forenames"], r["_dob"], r["_dod"]): r for r in reg}
    counts = defaultdict(int)
    months = defaultdict(int)
    for r in reg:
        counts[r["_place"]] += 1
        months[(r["_place"], r["_dod"].month)] += 1
    added = defaultdict(int)
    for k, (place, r) in me_deaths(P, w0, w1).items():
        if k in keys:
            continue
        counts[place] += 1
        months[(place, r["dod"].month)] += 1
        added[place] += 1
    return dict(counts), dict(months), dict(added), len(reg)


def completeness(P, by_place=False, by_month=False, years=range(2021, 2026)):
    """the earlier summers' share of deaths on the register by 9 October of the same year, against the entries made
    by the extract; pooled, by place or by month of death"""
    ent = list(entries(P).values())
    num, den = defaultdict(int), defaultdict(int)
    shares = defaultdict(list)
    for y in years:
        a, b = W.summer(y)
        cut = dt.date(y, 10, 9)
        n2, d2 = defaultdict(int), defaultdict(int)
        for r in ent:
            if a <= r["_dod"] <= b:
                g = (r["_place"] if by_place else "all", r["_dod"].month if by_month else 0)
                d2[g] += 1
                if r["_reg"] <= cut:
                    n2[g] += 1
        for g in d2:
            shares[g].append(n2[g] / d2[g])
            num[g] += n2[g]
            den[g] += d2[g]
    mean = {g: sum(v) / len(v) for g, v in shares.items()}
    return mean


def completed_counts(P, by_place=False, by_month=False, years=range(2021, 2026)):
    sh = completeness(P, by_place, by_month, years)
    reg = window_register(P)
    out = defaultdict(float)
    for r in reg:
        g = (r["_place"] if by_place else "all", r["_dod"].month if by_month else 0)
        out[r["_place"]] += 1.0 / sh[g]
    return dict(out)


def registered_counts(P):
    out = defaultdict(int)
    for r in window_register(P):
        out[r["_place"]] += 1
    return dict(out)


def excess(counts, expected):
    return {p: 100.0 * (counts[p] - expected[p]) / expected[p] for p in W.NAMES}


def qualifying(ex):
    return [p for p in W.NAMES if ex[p] >= 100 * W.LINE]


# ------------------------------------------------------------------ Ask B: the offices' deaths scrutinised
def ask_b(P, mode="golden"):
    """distinct deaths each office completed in each 2025-26 quarter. golden merges rows that share a coroner
    reference or the person (surname, forenames, birth date, death date); 'rows' counts cases; 'person' merges on
    the person only"""
    out = {}
    for office, rows in (("North", P.north), ("South", P.south)):
        rows = [r for r in rows if W.quarter_fy(r["completed"])]
        parent = list(range(len(rows)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        def union(i, j):
            a, b = find(i), find(j)
            if a != b:
                parent[max(a, b)] = min(a, b)
        if mode != "rows":
            by = defaultdict(list)
            for i, r in enumerate(rows):
                by[("p",) + key(r["surname"], r["forenames"], r["dob"], r["dod"])].append(i)
                if mode == "golden" and r["cref"]:
                    by[("c", r["cref"])].append(i)
            for v in by.values():
                for j in v[1:]:
                    union(v[0], j)
        groups = defaultdict(list)
        for i in range(len(rows)):
            groups[find(i)].append(rows[i])
        for q in (1, 2, 3, 4):
            out[(office, q)] = sum(1 for g in groups.values() if W.quarter_fy(min(r["completed"] for r in g)) == q)
    return out


# ------------------------------------------------------------------ Ask C: registered within five days
def fieldwise(P):
    """each entry as it now stands: the latest version's fields, with the registration's own date (version 1)"""
    first, last = entries(P), entries(P, latest=True)
    out = {}
    for k, r in last.items():
        row = dict(r)
        row["_reg"] = first[k]["_reg"]
        out[k] = row
    return out


def ask_c(P, mode="golden"):
    """each place's share of its 2025 deaths with a medical certificate whose registration came no more than five
    days after the death, by calendar quarter of death. golden reads each entry as it now stands (the latest fields,
    the registration's own date); latest reads every field off the last version; first reads version 1 only; rows
    reads every row as an entry"""
    rows = {"golden": lambda: list(fieldwise(P).values()), "latest": lambda: list(entries(P, latest=True).values()),
            "first": lambda: list(entries(P).values()), "rows": lambda: P.reg}[mode]()
    num, den = defaultdict(int), defaultdict(int)
    for r in rows:
        if r["_dod"].year != 2025 or not r["certification"].startswith("Medical certificate"):
            continue
        g = (r["_place"], (r["_dod"].month - 1) // 3 + 1)
        den[g] += 1
        if (r["_reg"] - r["_dod"]).days <= 5:
            num[g] += 1
    return {g: 100.0 * num[g] / den[g] for g in den}, dict(num), dict(den)


def solve(target=W.TARGET):
    P = Pack(target)
    counts, months, added, nreg = golden_counts(P)
    ex = excess(counts, P.expected)
    reg = registered_counts(P)
    comp = completed_counts(P)
    comp_place = completed_counts(P, by_place=True)
    comp_month = completed_counts(P, by_month=True)
    rungs = {"registered": reg, "pooled": comp, "by_place": comp_place, "by_month": comp_month,
             "pooled_last3": completed_counts(P, years=range(2023, 2026)),
             "place_last3": completed_counts(P, by_place=True, years=range(2023, 2026))}
    rung_sets = {k: qualifying(excess(v, P.expected)) for k, v in rungs.items()}
    b = ask_b(P)
    c, cn, cd = ask_c(P)
    return dict(P=P, counts=counts, months=months, added=added, excess=ex, qualifying=qualifying(ex),
                expected=P.expected, rungs=rungs, rung_sets=rung_sets,
                rung_excess={k: excess(v, P.expected) for k, v in rungs.items()},
                ask_b=b, ask_b_rows=ask_b(P, "rows"), ask_b_person=ask_b(P, "person"),
                ask_c=c, ask_c_num=cn, ask_c_den=cd, ask_c_latest=ask_c(P, "latest")[0],
                ask_c_first=ask_c(P, "first")[0], ask_c_rows=ask_c(P, "rows")[0],
                completeness=completeness(P), completeness_place=completeness(P, by_place=True))


def r1(x):
    return "%.1f" % (round(x * 10 + 1e-9) / 10.0)


if __name__ == "__main__":
    S = solve()
    for p in W.NAMES:
        print("%-14s deaths %4d expected %4d excess %5.1f  registered %4d (%+.1f)  pooled %+.1f  by place %+.1f"
              % (p, S["counts"][p], S["expected"][p], S["excess"][p], S["rungs"]["registered"][p],
                 S["rung_excess"]["registered"][p], S["rung_excess"]["pooled"][p], S["rung_excess"]["by_place"][p]))
    print("golden", S["qualifying"])
    for k, v in S["rung_sets"].items():
        print("  rung", k, v)
    print("ask B golden", S["ask_b"])
    print("ask B rows  ", S["ask_b_rows"])
    print("ask B person", S["ask_b_person"])
    print("ask C", {k: r1(v) for k, v in sorted(S["ask_c"].items())})
    print("ask C latest", {k: r1(v) for k, v in sorted(S["ask_c_latest"].items())})
    print("ask C first", {k: r1(v) for k, v in sorted(S["ask_c_first"].items())})
