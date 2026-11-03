"""The ask ceiling, measured on the cut pack with no code shared with the generator.

Two responses are scored figure by figure against figures.json at each figure's printed precision:
  the cracker lands the call and runs the hygiene battery: it drops the legacy rows the case system carried over,
    composes an order from its address rows, converts UTC, reads every sheet and executes every filed definition
    (the service standard's turnaround, the contract schedule's midnight rule on the incident log's absences);
  the mirror stops at the most attractive wrong rung (a judge on the custody list), gets the default path's figures
    right, and reads each ask at the files' face value.
Scores use the pair arithmetic of supplemental-stumping Part 0 (call 38, instructions 7, asks 55), with the
critical components the miss keeps counted from its own figures.

    python3 task399/generator/ceiling.py [target_dir]
"""
import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NZT = ZoneInfo("Pacific/Auckland")
UTC = dt.timezone.utc
P2 = (dt.date(2025, 10, 1), dt.date(2026, 9, 30))
MONTHS = [(2025, m) for m in range(10, 13)] + [(2026, m) for m in range(1, 10)]


def rcsv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def rxlsx(path, sheet):
    it = load_workbook(path, read_only=True, data_only=True)[sheet].iter_rows(values_only=True)
    h = list(next(it))
    return [dict(zip(h, r)) for r in it]


def day(v):
    if v in (None, ""):
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v)
    if "/" in s:
        d, m, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s[:10])


def nz(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC).astimezone(NZT)


# ------------------------------------------------------------------ ask 1, EM turnaround by month
def em_cracker(t):
    """Section 2 executed: the court's order day from the court's own record (the extract's order appearance, by CRN or
    else surname, first name and date of birth), the unit's own order date where the extract has no order appearance
    for the case, the first report filed (the upload log in New Zealand time), one order an assessment, the tracker's
    carried-over rows dropped for their case-system copies, every courthouse of the region kept."""
    app = rcsv(os.path.join(t, "cms_appearances_oct2024_sep2026.csv"))
    by_crn, by_person = {}, {}
    for r in app:
        if r["Outcome"] == "Remanded in custody, EM bail address assessment ordered":
            d = dt.date.fromisoformat(r["AppearanceDate"])
            by_crn.setdefault(r["CRN"], []).append(d)
            by_person.setdefault((r["Surname"].upper(), r["GivenNames"].upper(), r["DateOfBirth"]), []).append(d)

    def order_day(crn, pk, unit_day):
        c = [d for d in (by_crn.get(crn, []) if crn else by_person.get(pk, [])) if d <= unit_day]
        return max(c) if c else unit_day

    leg = rxlsx(os.path.join(t, "em_bail_tracker_2025-26.xlsx"), "Tracker")
    case = rcsv(os.path.join(t, "em_case_system_assessments.csv"))
    region = {"Kestrel Bay", "Dunmore", "Ashgrove", "Thornmere", "KBY", "DUN", "ASH", "THM"}
    orders, carried, addr = {}, {}, defaultdict(set)
    for r in leg:
        addr[r["Ref"].split("/")[0]].add(r["Address"])
    for r in leg:
        if r["Court"] not in region:
            continue
        pk = (str(r["Surname"]).upper(), str(r["First name"]).upper(), day(r["DOB"]).isoformat())
        od = order_day(r["CRN"], pk, day(r["Referral date"]))
        if r["Status"] == "Migrated":                  # carried into the case system: its copy is kept, with the
            carried[frozenset(addr[r["Ref"].split("/")[0]])] = od    # legacy record's order day
            continue
        orders.setdefault(r["Ref"].split("/")[0], (od, day(r["Report filed"])))
    first = {}
    for u in rcsv(os.path.join(t, "em_document_uploads.csv")):
        if u["DocumentType"] == "EM address assessment report":     # section 2: the first report filed
            dd = nz(u["UploadedAt"]).date()
            first[u["OrderRef"]] = min(dd, first.get(u["OrderRef"], dd))
    caddr = defaultdict(set)
    for r in case:
        caddr[r["OrderRef"]].add(r["Address"])
    for r in case:
        if r["Court"] not in region or r["OrderRef"] not in first:
            continue
        od = carried.get(frozenset(caddr[r["OrderRef"]])) or order_day(r["CRN"], None, day(r["OrderDate"]))
        orders.setdefault(r["OrderRef"], (od, first[r["OrderRef"]]))
    return _months(orders.values())


def em_mirror(t):
    leg = rxlsx(os.path.join(t, "em_bail_tracker_2025-26.xlsx"), "Tracker")
    case = rcsv(os.path.join(t, "em_case_system_assessments.csv"))
    rows = [(day(r["Referral date"]), day(r["Report filed"])) for r in leg if r["Report filed"]]
    rows += [(day(r["OrderDate"]), day(r["ReportFiledDate"])) for r in case]
    return _months(rows)


def _months(pairs):
    out = {}
    for ym in MONTHS:
        v = [(b - a).days for a, b in pairs if a and b and (a.year, a.month) == ym]
        out["em_%d_%02d" % ym] = sum(v) / len(v) if v else float("nan")
    return out


# ------------------------------------------------------------------ ask 2, bail house occupied nights by month
def bh_cracker(t):
    """Clause 4 executed on a state rebuilt from the incident log in New Zealand time: a placement runs from its
    arrival to the night before the resident leaves; each departure (police custody, hospital, not back by curfew)
    closed by its return is an absence, tested at midnight, and a departure never closed is the resident leaving;
    every absence on the app's Away sheet is joined to the log's (a union, never a sum)."""
    reg = rxlsx(os.path.join(t, "bail_house_register_2025-26.xlsx"), "Placements")
    away = rxlsx(os.path.join(t, "bail_house_register_2025-26.xlsx"), "Away")
    inc = rcsv(os.path.join(t, "bail_house_incidents.csv"))
    ev = defaultdict(list)
    for e in inc:
        ev[e["Placement"]].append((nz(e["ReportedAt"]), e["Type"]))
    closes = {"Taken into police custody": "Returned from police custody", "Admitted to hospital": "Returned from hospital",
              "Resident did not return": "Resident returned"}
    gone, span = defaultdict(set), {}
    for pid, es in ev.items():
        es.sort()
        arr = [x for x, k in es if k == "Resident arrived"]
        leave = [x for x, k in es if k == "Resident moved out"]
        for i, (o, k) in enumerate(es):
            if k not in closes:
                continue
            back = [x for x, kb in es[i + 1:] if kb == closes[k]]
            if not back:
                leave.append(o)                        # never back: the resident left
                continue
            b = min(back)
            d = o.date()
            while True:
                mid = dt.datetime(d.year, d.month, d.day, tzinfo=NZT) + dt.timedelta(days=1)
                if o < mid < b:
                    gone[pid].add(d)
                if mid >= b:
                    break
                d += dt.timedelta(days=1)
        span[pid] = (min(arr).date() if arr else None, min(leave).date() if leave else None)
    for a in away:                                     # every sheet read: the app's absences joined to the log's
        d, last = day(a["Away from"]), day(a["Away to (last night away)"])
        while d <= last:
            gone[a["Placement"]].add(d)
            d += dt.timedelta(days=1)
    reg2 = []
    for p in reg:
        a0, e0 = span.get(p["Placement"], (None, None))
        q = dict(p)
        if a0:
            q["First night"] = a0
        q["Left"] = e0 if e0 else None
        reg2.append(q)
    return _nights(reg2, gone)


def bh_mirror(t):
    reg = rxlsx(os.path.join(t, "bail_house_register_2025-26.xlsx"), "Placements")
    return _nights(reg, defaultdict(set))


def _nights(reg, gone):
    n = {ym: 0 for ym in MONTHS}
    for p in reg:
        first, left = day(p["First night"]), day(p["Left"])
        end = left if left else P2[1] + dt.timedelta(days=1)
        d = first
        while d < end:
            if P2[0] <= d <= P2[1] and d not in gone[p["Placement"]]:
                n[(d.year, d.month)] += 1
            d += dt.timedelta(days=1)
    return {"bh_%d_%02d" % ym: n[ym] for ym in MONTHS}


def main(argv):
    t = argv[1] if len(argv) > 1 else os.path.join(TASK, "target")
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    units = figs["_units"]
    ask_keys = [k for k in units if k.startswith(("em_", "bh_"))]
    rows = {"cracker": {}, "mirror": {}}
    rows["cracker"].update(em_cracker(t))
    rows["cracker"].update(bh_cracker(t))
    rows["mirror"].update(em_mirror(t))
    rows["mirror"].update(bh_mirror(t))
    kept = {}
    print("| Ask | Figures | Cracker kept | Mirror kept | Cracker |")
    print("|---|---|---|---|---|")
    for ask, pre in (("Ask 1, EM turnaround by month", "em_"), ("Ask 2, bail house nights by month", "bh_")):
        ks = [k for k in ask_keys if k.startswith(pre)]
        res = {}
        for who in ("cracker", "mirror"):
            res[who] = sum(1 for k in ks if round(rows[who][k] / units[k]) == round(figs[k] / units[k]))
            kept.setdefault(who, 0)
            kept[who] += res[who]
        print("| %s | %d | %d | %d | %s |" % (ask, len(ks), res["cracker"], res["mirror"],
                                              "miss" if res["cracker"] < len(ks) else "KEEPS"))
    n = len(ask_keys)
    lc, ls = kept["cracker"] / n, kept["mirror"] / n
    cc = figs["_critical"]
    miss_cc = sum(1 for k in cc if k in figs["_default_path_same"]) / len(cc)
    c_score = 38 + 7 + 55 * lc
    s_score = 18 * miss_cc + 7 + 55 * ls
    pair = (c_score + s_score) / 2
    print("Cracker ask keep %.1f per cent (%d of %d); mirror ask keep %.1f per cent; critical components the miss "
          "keeps %.1f per cent" % (100 * lc, kept["cracker"], n, 100 * ls, 100 * miss_cc))
    print("Cracker %.1f, mirror %.1f, pair ceiling %.1f" % (c_score, s_score, pair))
    print("Mirror leakage %.1f per cent of ask weight" % (100 * ls))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
