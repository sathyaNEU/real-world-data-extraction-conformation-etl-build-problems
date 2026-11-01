"""The golden, computed from target/ alone: the price paid record with the January 2027 update applied, each
dwelling's consecutive standard sales paired by address, the pairs whose dwelling had building work completed between
its two sales set aside, each ward's repeat-sales index, the pressured wards and their shares, and the three asks.
Every route the checks price is a parameter here."""
import csv
import datetime as dt
import os
import re
import sys
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "target")
F = {"hist": "pp-harrowmere-2015-2025.csv", "y26": "pp-harrowmere-2026.csv", "upd": "pp-monthly-update-2027-01.csv",
     "pcs": "harrowmere_postcode_directory_2026-11.csv", "wards": "ward_codes_names_2019_2023.csv",
     "reg": "hcc_building_control_completions_2015-2026.xlsx", "pipe": "hvha_affordable_pipeline_2027-28.xlsx",
     "claims": "hvha_start_on_site_claims_2025-2027.csv"}
COLS = ["id", "price", "date", "postcode", "ptype", "new", "duration", "paon", "saon", "street", "locality", "town",
        "district", "county", "cat", "status"]
YEARS = list(range(2015, 2027))
LINE = 5.0
POT = 12_000_000
PY0, PY1 = dt.date(2027, 4, 1), dt.date(2028, 3, 31)
SUFFIX = {"RD": "ROAD", "ST": "STREET", "AVE": "AVENUE", "GR": "GROVE", "TER": "TERRACE", "CL": "CLOSE",
          "CRES": "CRESCENT", "DR": "DRIVE", "LN": "LANE", "PL": "PLACE", "GDNS": "GARDENS", "CT": "COURT"}


def p(target, k):
    return os.path.join(target, F[k])


# ------------------------------------------------------------------------------------------------ loading

def read_ppd(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if rows and rows[0][0].strip().lower().startswith("transaction unique identifier"):
        rows = rows[1:]
    return [dict(zip(COLS, row)) for row in rows]


def load_ppd(target, apply_update=True):
    recs = {}
    for k in ("hist", "y26"):
        for x in read_ppd(p(target, k)):
            recs[x["id"]] = x
    if apply_update:
        for x in read_ppd(p(target, "upd")):
            if x["status"] in ("A", "C"):
                recs[x["id"]] = x
            elif x["status"] == "D":
                recs.pop(x["id"], None)
    out = []
    for x in recs.values():
        x = dict(x)
        x["price"] = int(x["price"])
        x["date"] = dt.date.fromisoformat(x["date"][:10])
        out.append(x)
    return out


def load_wards(target, year="23"):
    names = {}
    with open(p(target, "wards"), newline="") as f:
        for r in csv.DictReader(f):
            names[r["WD23CD"]] = r["WD23NM"]
            names[r["WD19CD"]] = r["WD19NM"]
    ward = {}
    with open(p(target, "pcs"), newline="") as f:
        for r in csv.DictReader(f):
            ward[r["pcds"]] = names[r["wd23cd"] if year == "23" else r["wd19cd"]]
    return ward


def norm_pc(s):
    s = re.sub(r"\s+", "", (s or "").upper())
    return s[:-3] + " " + s[-3:] if len(s) >= 5 else s


def norm_street(s):
    w = re.sub(r"[^A-Z0-9 ]", " ", (s or "").upper()).split()
    if w and w[-1] in SUFFIX:
        w[-1] = SUFFIX[w[-1]]
    return " ".join(w)


def addr_key(paon, saon, postcode):
    return (re.sub(r"\s+", " ", (paon or "").upper().strip()), re.sub(r"\s+", " ", (saon or "").upper().strip()),
            norm_pc(postcode))


PC_RE = re.compile(r"(HW\d)\s*(\d[A-Z]{2})\s*$", re.I)


def parse_legacy(addr):
    """'Flat A, 14 Calder Rd, Harrowmere HW3 4QT' -> (paon, saon, street, postcode)"""
    a = addr.strip()
    m = PC_RE.search(a)
    pc = norm_pc(m.group(1) + m.group(2)) if m else ""
    a = a[:m.start()].strip(" ,") if m else a
    a = re.sub(r",?\s*Harrowmere\s*$", "", a, flags=re.I).strip(" ,")
    saon = ""
    m = re.match(r"(Flat\s+\w+)\s*,\s*(.*)$", a, re.I)
    if m:
        saon, a = m.group(1), m.group(2)
    parts = [x.strip() for x in a.split(",") if x.strip()]
    if len(parts) >= 2:
        paon, street = parts[0], parts[1]
    else:
        m = re.match(r"^(\d+[A-Z]?)\s+(.*)$", parts[0] if parts else "", re.I)
        if m:
            paon, street = m.group(1), m.group(2)
        else:   # a house name with the street run on: take the known street suffix as the end of the street
            toks = (parts[0] if parts else "").split()
            cut = max([i for i, t in enumerate(toks) if t.upper() in SUFFIX or t.upper() in SUFFIX.values()] or [len(toks) - 1])
            k = cut - 1
            paon, street = " ".join(toks[:k]), " ".join(toks[k:cut + 1])
    return paon, saon, street, pc


def load_register(target):
    wb = load_workbook(p(target, "reg"), read_only=True, data_only=True)
    out = []
    for row in list(wb["Legacy 2015-2020"].iter_rows(values_only=True))[1:]:
        ref, rec, addr, desc, comp, ward, plus, minus = row[:8]
        paon, saon, street, pc = parse_legacy(addr)
        out.append(dict(system="legacy", ref=ref, received=dt.datetime.strptime(rec, "%d/%m/%Y").date(),
                        completed=dt.datetime.strptime(comp, "%d/%m/%Y").date(), paon=paon, saon=saon, street=street,
                        postcode=pc, wtype=desc, desc=desc, cert="", created=int(plus or 0), lost=int(minus or 0),
                        lost_blank=False, ward=ward))
    for row in list(wb["Uniform 2021-2026"].iter_rows(values_only=True))[1:]:
        (app, rec, num, street, pc, wtype, desc, cert, cdate, body, plus, minus, ward) = row[:13]
        saon = ""
        num = str(num)
        m = re.match(r"(Flat\s+\w+)\s*,\s*(.*)$", num, re.I)
        if m:
            saon, num = m.group(1), m.group(2)
        out.append(dict(system="uniform", ref=app, received=dt.date.fromisoformat(rec),
                        completed=dt.date.fromisoformat(cdate), paon=num, saon=saon, street=street, postcode=norm_pc(pc),
                        wtype=wtype, desc=desc, cert=cert, created=int(plus or 0), lost=int(minus or 0),
                        lost_blank=minus is None and wtype == "Conversion", ward=ward))
    return out


# ------------------------------------------------------------------------------------------------ the index

def standard(recs, cats=("A",), types="DSTF"):
    return [x for x in recs if x["cat"] in cats and x["ptype"] in types]


def pairs_of(recs, key=lambda x: addr_key(x["paon"], x["saon"], x["postcode"]) + (x["street"],)):
    by = defaultdict(list)
    for x in recs:
        by[key(x)].append(x)
    out = []
    for k, ss in by.items():
        ss.sort(key=lambda x: (x["date"], x["id"]))
        for a, b in zip(ss, ss[1:]):
            out.append((k, a, b))
    return out


def works_index(reg, kinds=None, use="completed"):
    idx = defaultdict(list)
    for w in reg:
        if kinds and not kinds(w):
            continue
        idx[addr_key(w["paon"], w["saon"], w["postcode"])].append(w[use])
    return idx


def clean(pairs, widx):
    out = []
    for k, a, b in pairs:
        ds = widx.get(k[:3], [])
        if any(a["date"] < d < b["date"] for d in ds):
            continue
        out.append((k, a, b))
    return out


def bmn(rows, weights=None):
    """rows: (year1, year2, log ratio). Ordinary least squares on year indicators, 2015 the base."""
    idx = {y: k for k, y in enumerate(YEARS[1:])}
    rows = [r for r in rows if r[0] != r[1]]
    X = np.zeros((len(rows), len(idx)))
    yv = np.zeros(len(rows))
    for k, (y1, y2, lr) in enumerate(rows):
        if y2 in idx:
            X[k, idx[y2]] += 1
        if y1 in idx:
            X[k, idx[y1]] -= 1
        yv[k] = lr
    if weights is not None:
        w = np.sqrt(np.asarray([weights[k] for k in range(len(rows))]))
        X, yv = X * w[:, None], yv * w
    b, *_ = np.linalg.lstsq(X, yv, rcond=None)
    lev = {YEARS[0]: 0.0}
    lev.update({y: float(b[k]) for y, k in idx.items()})
    return lev


def change(lev, y=2026):
    return 100.0 * (np.exp(lev[y] - lev[y - 1]) - 1.0)


def ward_index(pairs, ward_of, min_hold=0, wrs=False):
    rows = defaultdict(list)
    for k, a, b in pairs:
        w = ward_of.get(norm_pc(b["postcode"])) or ward_of.get(norm_pc(a["postcode"]))
        if w is None:
            continue
        if (b["date"] - a["date"]).days < min_hold:
            continue
        rows[w].append((a["date"].year, b["date"].year, float(np.log(b["price"] / a["price"])), (b["date"] - a["date"]).days))
    out = {}
    for w, rr in rows.items():
        base = [(y1, y2, lr) for y1, y2, lr, _ in rr]
        if wrs:
            lev0 = bmn(base)
            res = [lr - (lev0[y2] - lev0[y1]) for y1, y2, lr in base]
            days = [d for y1, y2, lr, d in rr]
            # Case-Shiller second stage: squared residuals on the interval, weights the inverse of the fit
            A = np.vstack([np.ones(len(days)), np.asarray(days, float)]).T
            keep = [k for k, (y1, y2, lr) in enumerate(base) if y1 != y2]
            c, *_ = np.linalg.lstsq(A[keep], np.asarray(res)[keep] ** 2, rcond=None)
            fit = A @ c
            fit = np.clip(fit, 1e-4, None)
            wts = [1.0 / fit[k] for k in keep]
            lev = bmn([base[k] for k in keep], weights=wts)
        else:
            lev = bmn(base)
        out[w] = lev
    return out


def solve(target=TARGET, apply_update=True, wards="23", drop_works=True, works_kinds=None, works_use="completed",
          min_hold=0, wrs=False, cats=("A",), types="DSTF"):
    recs = load_ppd(target, apply_update)
    ward_of = load_wards(target, wards)
    reg = load_register(target)
    st = standard(recs, cats, types)
    prs = pairs_of(st)
    if drop_works:
        prs = clean(prs, works_index(reg, works_kinds, works_use))
    idx = ward_index(prs, ward_of, min_hold, wrs)
    ch = {w: change(lev) for w, lev in idx.items()}
    return dict(recs=recs, ward_of=ward_of, reg=reg, pairs=prs, index=idx, change=ch)


def pressured(ch):
    return sorted(w for w, v in ch.items() if round(v, 1) > LINE)


def pipeline_homes(target):
    wb = load_workbook(p(target, "pipe"), read_only=True, data_only=True)
    homes = defaultdict(int)
    for row in list(wb["Pipeline"].iter_rows(values_only=True))[1:]:
        sid, name, prov, ward, pc, h, sr, ar, so, start, comp, status, grant = row[:13]
        d = start.date() if hasattr(start, "date") else start
        if status in ("Approved", "In contract") and PY0 <= d <= PY1:
            homes[ward] += int(h)
    return dict(homes)


def shares(press, homes):
    tot = sum(homes.get(w, 0) for w in press)
    return {w: int(round(POT * homes.get(w, 0) / tot)) for w in press}, {
        w: POT * homes.get(w, 0) / tot for w in press}


# ------------------------------------------------------------------------------------------------ the asks

def dwelling_addresses(recs):
    """addresses the price paid record shows as a dwelling (an entry for a house or flat), with the entry dates"""
    out = defaultdict(list)
    for x in recs:
        if x["ptype"] in "DSTF":
            out[addr_key(x["paon"], x["saon"], x["postcode"])].append(x["date"])
    return out


def ask_supply(target, reg=None, ward_of=None, recs=None, dedupe=True, infer_lost=True, blank_lost=0):
    """net additional dwellings certified complete in 2026: created less lost, each application once; where an
    approver's certificate leaves the dwellings lost blank, a converted building the price paid record shows as a
    dwelling lost one"""
    reg = reg or load_register(target)
    ward_of = ward_of or load_wards(target)
    recs = recs if recs is not None else load_ppd(target)
    dwell = dwelling_addresses(recs) if infer_lost else {}
    seen = {}
    for w in reg:
        if w["completed"].year != 2026 or (w["created"] == 0 and not w["lost"]):
            continue
        key = w["ref"] if dedupe else (w["ref"], w["cert"], w["completed"])
        seen[key] = w
    out = defaultdict(int)
    for w in seen.values():
        lost = w["lost"]
        if w["lost_blank"]:
            if infer_lost:
                k = addr_key(w["paon"], w["saon"], w["postcode"])
                lost = 1 if any(d < w["completed"] for d in dwell.get(k, [])) else 0
            else:
                lost = blank_lost
        out[ward_of.get(norm_pc(w["postcode"]))] += w["created"] - lost
    return dict(out)


def ask_company(target, recs=None, ward_of=None, group=True, rule="plausible"):
    """money paid in 2026 additional entries for dwellings: a price standing on several entries of one day that is
    several times a single dwelling's price in the ward is one portfolio transfer's, counted once"""
    recs = recs if recs is not None else load_ppd(target)
    ward_of = ward_of or load_wards(target)
    med = defaultdict(list)
    for x in standard(recs):
        if x["date"].year == 2026:
            med[ward_of.get(norm_pc(x["postcode"]))].append(x["price"])
    med = {w: float(np.median(v)) for w, v in med.items()}
    b = [x for x in recs if x["cat"] == "B" and x["ptype"] in "DSTF" and x["date"].year == 2026]
    n = defaultdict(int)
    money = defaultdict(int)
    groups = defaultdict(list)
    for x in b:
        groups[(x["date"], x["price"])].append(x)
    for (d, pr), xs in groups.items():
        wards = [ward_of.get(norm_pc(x["postcode"])) for x in xs]
        for wd in wards:
            n[wd] += 1
        one = False
        if group and len(xs) >= 2:
            one = pr > 3 * med.get(wards[0], 1e18) if rule == "plausible" else len(xs) >= int(rule)
        if one:
            money[wards[0]] += pr
        else:
            for wd in wards:
                money[wd] += pr
    return dict(n), dict(money)


def ask_starts(target, ward_of=None, dedupe=True, statuses=("Paid", "Approved"), exact_only=False):
    """affordable homes started on site in 2026: each start once. A claim that restates, for the whole site, the
    homes other claims at the same postcode already started (the same total, from the first start) is not a start"""
    ward_of = ward_of or load_wards(target)
    with open(p(target, "claims"), newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["start"] = dt.datetime.strptime(r["Start on site"], "%d/%m/%Y").date()
        r["homes"] = int(r["Homes"])
        r["pc"] = norm_pc(r["Site postcode"])
    live = [r for r in rows if r["Claim status"] in statuses]
    keep = []
    for r in live:
        if r["start"].year != 2026:
            continue
        if dedupe:
            others = [o for o in live if o is not r and o["pc"] == r["pc"] and o["Provider"] != r["Provider"]
                      and o["start"] >= r["start"] and o["start"].year == 2026]
            if others and (sum(o["homes"] for o in others) == r["homes"] if not exact_only else
                           any(o["homes"] == r["homes"] and o["start"] == r["start"] for o in others)):
                # the later claim restates starts already claimed: keep the first claims
                first_sub = min(dt.datetime.strptime(o["Claim submitted"], "%d/%m/%Y").date() for o in others)
                if dt.datetime.strptime(r["Claim submitted"], "%d/%m/%Y").date() > first_sub:
                    continue
        keep.append(r)
    out = defaultdict(int)
    for r in keep:
        out[ward_of.get(r["pc"])] += r["homes"]
    return dict(out)


def golden(target=TARGET):
    S = solve(target)
    press = pressured(S["change"])
    homes = pipeline_homes(target)
    sh, exact = shares(press, homes)
    n, money = ask_company(target, S["recs"], S["ward_of"])
    return dict(S=S, change=S["change"], pressured=press, homes=homes, shares=sh, exact_shares=exact,
                supply=ask_supply(target, S["reg"], S["ward_of"], S["recs"]), company_n=n, company_money=money,
                starts=ask_starts(target, S["ward_of"]))


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else TARGET
    G = golden(t)
    D = solve(t, drop_works=False)
    for w in sorted(G["change"]):
        print("%-14s golden %6.2f  all-pairs %6.2f" % (w, G["change"][w], D["change"][w]))
    print("pressured", G["pressured"], "default", pressured(D["change"]))
    print("homes", G["homes"])
    print("shares", G["shares"])
    print("supply", G["supply"])
    print("company", G["company_n"], G["company_money"])
    print("starts", G["starts"])
