"""Readers of the shipped bundle (target/) and the golden's own path through them, used by checks.py, verify.py and
ceiling.py. Nothing here imports the generator's state."""
import csv
import datetime as dt
import os
import statistics

from openpyxl import load_workbook

import methods as M

Z = 1.645


def find(target, prefix):
    for f in sorted(os.listdir(target)):
        if f.startswith(prefix):
            return os.path.join(target, f)
    raise FileNotFoundError(prefix)


def read_acs(path):
    """{geoid without prefix: Est-like (u, mu, x, mx)} from a Bureau download (two header rows)."""
    with open(path, encoding="utf-8") as fh:
        r = csv.reader(fh)
        head = next(r)
        next(r)
        out = {}
        for row in r:
            d = dict(zip(head, row))
            gid = d["GEO_ID"].split("US")[1]
            k = [h for h in head if h.endswith("_001E")][0][:-5]
            out[gid] = Est(int(d[k + "_001E"]), int(d[k + "_001M"]), int(d[k + "_002E"]), int(d[k + "_002M"]))
        return out


class Est:
    def __init__(self, u, mu, x, mx):
        self.u, self.mu, self.x, self.mx = u, mu, x, mx


def candidates(target):
    wb = load_workbook(find(target, "carrow_nsf_2027_candidate"), read_only=True)
    ws = wb["2027 candidates"]
    out = []
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0 or not row[0]:
            continue
        out.append((row[0], str(row[3])))
    return out


def blockrel(target):
    with open(find(target, "tab2010_tab2020"), encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="|"))


def tractrel(target):
    with open(find(target, "tab20_tract20_tract10"), encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="|"))


def tract_table(target, golden=True, ratio=False, route="golden"):
    """Each candidate 2020 tract with both periods' rate and margin, z and the verdicts.
    route: golden (a split tract's 2014-18 from the 2010 block groups that tile it), parent (the parent's rate
    through the relationship file, by area share), drop (no 2014-18 row, no verdict), whole (the parent tested
    whole, every child taking its verdict)."""
    t18 = read_acs(find(target, "ACSDT5Y2018.B17001"))
    t23 = read_acs(find(target, "ACSDT5Y2023.B17001"))
    b18 = read_acs(find(target, "ACSDT5Y2018.B17021"))
    br = blockrel(target)
    tr = tractrel(target)
    pre = None
    # 2010 block groups making up each 2020 tract, and whether whole
    bgs_of, land_in = {}, {}
    land_bg = {}
    for r in br:
        g10 = r["STATE_2010"] + r["COUNTY_2010"] + r["TRACT_2010"] + r["BLK_2010"][0]
        t20 = r["STATE_2020"] + r["COUNTY_2020"] + r["TRACT_2020"]
        land_bg[g10] = land_bg.get(g10, 0) + int(r["AREALAND_INT"])
        k = (t20, g10)
        land_in[k] = land_in.get(k, 0) + int(r["AREALAND_INT"])
    for (t20, g10), l in land_in.items():
        bgs_of.setdefault(t20, []).append((g10, l / land_bg[g10]))
    parents = {}
    for r in tr:
        parents.setdefault(r["GEOID_TRACT_20"], []).append(
            (r["GEOID_TRACT_10"], int(r["AREALAND_PART"]) / int(r["AREALAND_TRACT_10"])))
    rows = []
    for nb, gid in candidates(target):
        cur = t23[gid]
        c = M.proportion(cur.x, cur.mx, cur.u, cur.mu, ratio=ratio)
        same = gid in t18          # a 2020 tract keeping its 2010 code keeps its ground (a touch-up moves no one)
        if same:
            p = t18[gid]
            e = M.proportion(p.x, p.mx, p.u, p.mu, ratio=ratio)
        elif route == "golden":
            whole = [g for g, s in bgs_of[gid] if s > 0.999]
            e = M.proportion(*M.summed([b18[g] for g in whole]), ratio=ratio)
        elif route == "parent":
            ps = [(p, s) for p, s in parents[gid] if s > 0.001]
            x = sum(t18[p].x * s for p, s in ps)
            u = sum(t18[p].u * s for p, s in ps)
            e = M.proportion(x, M.rss([t18[p].mx * s for p, s in ps]), u, M.rss([t18[p].mu * s for p, s in ps]),
                             ratio=ratio)
        elif route == "drop":
            e = None
        elif route == "whole":
            par = max(parents[gid], key=lambda t: t[1])[0]
            kids = [g for g, ps in parents.items() if any(p == par and s > 0.5 for p, s in ps)]
            pe = t18[par]
            e1 = M.proportion(pe.x, pe.mx, pe.u, pe.mu, ratio=ratio)
            e2 = M.proportion(*M.summed([t23[k] for k in kids]), ratio=ratio)
            zz = M.z(*e1, *e2)
            rows.append(dict(nbhd=nb, geoid=gid, r18=e1[0], m18=e1[1], r23=c[0], m23=c[1], z=zz,
                             qual=zz > Z and c[0] >= 0.2, split=True))
            continue
        if e is None:
            rows.append(dict(nbhd=nb, geoid=gid, r18=None, m18=None, r23=c[0], m23=c[1], z=None, qual=False,
                             split=True))
            continue
        zz = M.z(*e, *c)
        rows.append(dict(nbhd=nb, geoid=gid, r18=e[0], m18=e[1], r23=c[0], m23=c[1], z=zz,
                         qual=zz > Z and c[0] >= 0.2, split=not same))
    return rows


def designated(rows):
    n = {}
    for r in rows:
        n[r["nbhd"]] = n.get(r["nbhd"], 0) + (1 if r["qual"] else 0)
    return sorted(k for k, v in n.items() if v >= 3), n


# ------------------------------------------------------------------------------------------------- the asks
RES = {"R1", "R2", "R3", "RM", "RC"}


def parcels(target):
    with open(find(target, "carrow_parcels"), encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    by = {}
    for r in rows:
        by[r["parcel_id"]] = r
        by[r["prior_parcel_id"]] = r
    return by


def nbhd_of(target):
    """{2020 tract GEOID: neighbourhood}"""
    return {gid: nb for nb, gid in candidates(target)}


def ask_a(target, history=True):
    """Each neighbourhood's residential properties with a housing case open on 31 December 2026 and the average days
    open. history=False reads the export's status and dates as of that day (the cracker)."""
    ps = parcels(target)
    nb = nbhd_of(target)
    end = dt.date(2026, 12, 31)
    with open(find(target, "carrow_code_cases"), encoding="utf-8") as fh:
        cases = list(csv.DictReader(fh))
    evs = {}
    with open(find(target, "carrow_code_case_events"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            evs.setdefault(r["case_number"], []).append((dt.date.fromisoformat(r["event_date"]), r["event"]))
    out = {}
    for c in cases:
        if c["case_type"] != "HOUSING":
            continue
        p = ps.get(c["parcel_number"])
        if p is None or p["land_use_code"] not in RES:
            continue
        n = nb.get(p["census_block_2020"][:11])
        if n is None:
            continue
        opened = dt.datetime.strptime(c["opened_date"], "%m/%d/%Y").date()
        if history:
            state = False
            for d, e in sorted(evs[c["case_number"]]):
                if d > end:
                    break
                if e in ("CASE OPENED", "CASE REOPENED"):
                    state = True
                elif e.startswith("CASE CLOSED"):
                    state = False
            is_open = state
        else:
            closed = dt.datetime.strptime(c["closed_date"], "%m/%d/%Y").date() if c["closed_date"] else None
            is_open = opened <= end and (closed is None or closed > end)
        if is_open:
            props, ages = out.setdefault(n, (set(), []))
            props.add(p["parcel_id"])
            ages.append((end - opened).days)
    return {n: (len(v[0]), sum(v[1]) / float(len(v[1]))) for n, v in out.items()}


def journal(target):
    wb = load_workbook(find(target, "nsf_rehab_payment_register"), read_only=True)
    rows = []
    for ws in wb.worksheets:
        for i, r in enumerate(ws.iter_rows(values_only=True)):
            if i == 0 or r[0] is None:
                continue
            d = r[1].date() if hasattr(r[1], "date") else r[1]
            rows.append(dict(entry=int(r[0]), date=d, grant=r[2], parcel=str(r[3]), amount=float(r[6]),
                             ref=r[7] or ""))
    return rows


def ask_b(target, by_void=True):
    """Each neighbourhood's grant dollars paid in calendar 2026 and properties paid. by_void=False sums the 2026
    entries as they stand (the cracker: dated 2026, netted within the year)."""
    ps = parcels(target)
    nb = nbhd_of(target)
    rows = journal(target)
    voided = {int(r["ref"].split()[1]) for r in rows if r["ref"].startswith("REV")}
    out = {}
    for r in rows:
        if r["date"].year != 2026:
            continue
        p = ps.get(r["parcel"])
        n = nb.get(p["census_block_2020"][:11]) if p else None
        if n is None:
            continue
        if by_void and (r["amount"] < 0 or r["entry"] in voided):
            continue
        amt, props = out.setdefault(n, [0.0, {}])
        out[n][0] = amt + r["amount"]
        props[p["parcel_id"]] = props.get(p["parcel_id"], 0.0) + r["amount"]
    return {n: (round(v[0], 2), sum(1 for a in v[1].values() if a > 0.005)) for n, v in out.items()}


def golden_csv(path):
    raise NotImplementedError
