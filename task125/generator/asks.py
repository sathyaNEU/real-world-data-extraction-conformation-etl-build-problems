"""The three regional asks, computed the way the golden does and the way each wrong path does, from the rows the
pack ships (never from the simulation's hidden state)."""
from collections import defaultdict

import world as W

Q2, Q3 = "2026Q2", "2026Q3"


def strip(serial):
    return serial[:9]


def visits(call_rows, register):
    """Ask 1: first-interview visits made to the July to September 2026 intake, by region. Golden: one visit per
    address and visit number. Wrong paths: every row; one visit per address and day."""
    region = {r["serial"]: r["region"] for r in register}
    gold, rows, by_day = defaultdict(set), defaultdict(int), defaultdict(set)
    for r in call_rows:
        if r["intake"] != Q3:
            continue
        g = region[strip(r["serial"])]
        gold[g].add((r["serial"], r["visit_no"]))
        rows[g] += 1
        by_day[g].add((r["serial"], r["visit_start"].date()))
    f = lambda d: {g: len(d[g]) if isinstance(d[g], set) else d[g] for g in W.RCODES}
    return {"golden": f(gold), "rows": f(rows), "serial_day": f(by_day)}


def _status_by(rows, quarter, key):
    out = {}
    for r in rows:
        if r["quarter"] == quarter:
            out.setdefault(key(r), []).append(r)
    return out


def flows(person_rows):
    """Ask 2: of the respondents unemployed in April to June 2026, the share employed in July to September 2026, by
    region (percent). Golden: the same person matched on serial, sex and date of birth. Wrong paths: serial and
    person number (the cracker); serial alone (fan-out)."""
    k_gold = lambda r: (strip(r["serial"]), r["sex"], r["date_of_birth"])
    k_pno = lambda r: (strip(r["serial"]), r["person_no"])
    out = {}
    for name, key in (("golden", k_gold), ("person_no", k_pno)):
        q2 = _status_by(person_rows, Q2, key)
        q3 = _status_by(person_rows, Q3, key)
        num, den = defaultdict(int), defaultdict(int)
        for k, a in q2.items():
            assert len(a) == 1, (name, k)
            if a[0]["ilo_status"] != 2 or k not in q3:
                continue
            assert len(q3[k]) == 1
            den[a[0]["region"]] += 1
            num[a[0]["region"]] += q3[k][0]["ilo_status"] == 1
        out[name] = {g: 100 * num[g] / den[g] for g in W.RCODES}
        out[name + "_n"] = {g: (num[g], den[g]) for g in W.RCODES}
    # serial alone: every April to June unemployed person against every July to September person in the household
    q2 = _status_by(person_rows, Q2, lambda r: strip(r["serial"]))
    q3 = _status_by(person_rows, Q3, lambda r: strip(r["serial"]))
    num, den = defaultdict(int), defaultdict(int)
    for k, a in q2.items():
        for p in a:
            if p["ilo_status"] != 2 or k not in q3:
                continue
            for b in q3[k]:
                den[p["region"]] += 1
                num[p["region"]] += b["ilo_status"] == 1
    out["serial_only"] = {g: 100 * num[g] / den[g] for g in W.RCODES}
    return out


def to_decimal(h):
    whole = int(h)
    return whole + round((h - whole) * 100) / 60


def hours(person_rows):
    """Ask 3: total weekly hours actually worked by the employed, July to September 2026, by region, thousands of
    hours (final weights). Golden: telephone h.mm converted to decimal hours. Wrong paths: raw values (the cracker);
    every value converted as h.mm, face-to-face decimals included."""
    acc = {n: defaultdict(float) for n in ("golden", "raw", "all_converted")}
    for r in person_rows:
        if r["quarter"] != Q3 or r["ilo_status"] != 1:
            continue
        h, wt = r["actual_hours"], r["weight"]
        acc["golden"][r["region"]] += wt * (to_decimal(h) if r["mode"] == "CATI" else h)
        acc["raw"][r["region"]] += wt * h
        acc["all_converted"][r["region"]] += wt * to_decimal(h)
    return {n: {g: v[g] / 1000 for g in W.RCODES} for n, v in acc.items()}
