"""An independent verifier: it reads only the shipped bundle (target/, golden/, submission.md) with the csv module and
its own arithmetic, rebuilds the dwelling stock, fits persons per dwelling by type and age on the 2020 block groups,
estimates every municipality on 1 July 2026, places the births and deaths by address, and compares the call and every
graded figure with the golden workbook and the write-up."""
import csv
import datetime as dt
import os
import re

import numpy as np
import openpyxl

LINE = 10000
NAMES = {"002": "Town of Ashgrove", "006": "Town of Cedar Run", "010": "Town of Elk Prairie", "012": "Town of Glenmoor",
         "014": "Town of Harwick", "016": "Town of Kessler", "018": "Town of Maple Ford", "020": "Town of Northfield",
         "106": "Village of Barrow", "116": "Village of Fallon", "131": "Village of Ivydale", "146": "Village of Lorne",
         "221": "City of Dunmore", "241": "City of Juniper"}
MCD = {"21400": "City of Dunmore", "39050": "City of Juniper", "13200": "Town of Cedar Run",
       "49875": "Town of Maple Ford", "03450": "Town of Ashgrove", "04875": "Village of Barrow",
       "23800": "Town of Elk Prairie", "25600": "Village of Fallon", "29975": "Town of Glenmoor",
       "33100": "Town of Harwick", "37600": "Village of Ivydale", "40150": "Town of Kessler",
       "46225": "Village of Lorne", "57650": "Town of Northfield"}
KIND = {"1010": 0, "1020": 1, "1030": 1, "1050": 2, "1080": 3}
USE = {"Single-family dwelling": 0, "Two-family dwelling": 1, "Townhouse unit": 1, "Multi-family dwelling": 2,
       "Manufactured home": 3}
BANDS = [0, 5, 10, 15, 20, 30, 40, 60]


def dec(s):
    d = dt.date.fromisoformat(s)
    y0 = dt.date(d.year, 1, 1)
    return d.year + (d - y0).days / (dt.date(d.year + 1, 1, 1) - y0).days


def rows(t, name):
    with open(os.path.join(t, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def stock(t):
    roll = rows(t, "tamarack_real_property_roll_2026.csv")
    cos = rows(t, "certificates_of_occupancy_2020-01_2026-06.csv")
    demo = rows(t, "demolition_permits_2000-2026.csv")
    first = {}
    for c in cos:
        if c["USE"] in USE and int(c["NEW_DWELLING_UNITS"]) > 0:
            w = dec(c["ISSUED"])
            if c["TAXKEY"] not in first or w < first[c["TAXKEY"]][0]:
                first[c["TAXKEY"]] = (w, c)
    roll_date = dec("2026-01-01")
    units = []   # (muni, kind, completed, demolished, block group)
    vacant = {}
    for r in roll:
        n = int(r["LIVING_UNITS"])
        if n == 0:
            vacant[r["TAXKEY"]] = r
            continue
        y = int(r["YEAR_BUILT"]) or 1900
        comp = first[r["TAXKEY"]][0] if r["TAXKEY"] in first else y + 0.5
        units += [[NAMES[r["MUNI_NO"]], KIND[r["LAND_USE"]], comp, 9999.0, r["CENSUS_BLOCK_2020"][:12], r["TAXKEY"]]] * n
    for k, (w, c) in first.items():
        if w >= roll_date and k in vacant:
            units += [[NAMES[k[:3]], USE[c["USE"]], w, 9999.0, vacant[k]["CENSUS_BLOCK_2020"][:12], k]] * int(c["NEW_DWELLING_UNITS"])
    blocks = {r["TAXKEY"]: r["CENSUS_BLOCK_2020"][:12] for r in roll}
    by_key = {}
    for i, u in enumerate(units):
        by_key.setdefault(u[5], []).append(i)
    for d in demo:
        if d["STATUS"] != "Completed" or int(d["DWELLING_UNITS"] or 0) == 0:
            continue
        w = dec(d["COMPLETED"])
        if w >= roll_date:
            for i in by_key.get(d["TAXKEY"], []):
                units[i] = units[i][:3] + [w] + units[i][4:]
        else:
            units += [[NAMES[d["TAXKEY"][:3]], USE[d["STRUCTURE"]], int(d["YEAR_BUILT"]) + 0.5, w,
                       blocks.get(d["TAXKEY"], ""), d["TAXKEY"]]] * int(d["DWELLING_UNITS"])
    return units


def band(a):
    j = 0
    for k, lo in enumerate(BANDS):
        if a >= lo:
            j = k
    return j


def estimates(t):
    units = stock(t)
    bg = rows(t, "census2020_dhc_tamarack_block_groups.csv")[1:]
    ids = [b["GEO_ID"][-12:] for b in bg]
    pos = {g: i for i, g in enumerate(ids)}
    y = np.array([float(b["P15_001N"]) for b in bg])
    X = np.zeros((len(ids), 4 + len(BANDS) - 1))
    c20 = dec("2020-04-01")
    for m, k, comp, gone, g, key in units:
        if comp <= c20 < gone:
            X[pos[g], k] += 1
            j = band(c20 - comp)
            if j < len(BANDS) - 1:
                X[pos[g], 4 + j] += 1
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    c26 = dec("2026-07-01")
    est = {}
    for m, k, comp, gone, g, key in units:
        if comp <= c26 < gone:
            j = band(c26 - comp)
            est[m] = est.get(m, 0.0) + beta[k] + (beta[4 + j] if j < len(BANDS) - 1 else 0.0)
    wb = openpyxl.load_workbook(os.path.join(t, "group_quarters_survey_2026.xlsx"), data_only=True)
    ws = wb.active
    for r in range(5, ws.max_row + 1):
        if ws.cell(row=r, column=3).value:
            est[ws.cell(row=r, column=3).value] += ws.cell(row=r, column=6).value
    return est


SUF = {"STREET": "ST", "AVENUE": "AVE", "DRIVE": "DR", "LANE": "LN", "COURT": "CT", "ROAD": "RD", "CIRCLE": "CIR",
       "TRAIL": "TRL", "PLACE": "PL", "PARKWAY": "PKWY", "TERRACE": "TER"}


def key(addr):
    words = addr.upper().split()
    while words and (words[-1].startswith("#") or (len(words) >= 2 and words[-2] in ("APT", "UNIT"))):
        words = words[:-2] if not words[-1].startswith("#") else words[:-1]
    words[-1] = SUF.get(words[-1], words[-1])
    return words[0], " ".join(words[1:-1]), words[-1]


def vital(t):
    pts = {}
    for p in sorted(rows(t, "tamarack_address_points_2026-07.csv"), key=lambda p: p["STATUS"]):
        pts.setdefault((p["ADD_NUM"], p["ST_NAME"], p["ST_TYPE"]), p["MCD"])
    out = {}
    for name, col in (("births_tamarack_residents_2025-2026.csv", "CHILD_DOB"),
                      ("deaths_tamarack_residents_2025-2026.csv", "DATE_OF_DEATH")):
        cnt = {}
        for r in rows(t, name):
            if "2025-07-01" <= r[col] <= "2026-06-30":
                m = MCD[pts[key(r["RES_STREET"])]]
                cnt[m] = cnt.get(m, 0) + 1
        out[name[:6]] = cnt
    return out


def main(t, gdir):
    ok = True
    est = estimates(t)
    call = sorted(m for m, v in est.items() if v >= LINE)
    v = vital(t)
    ws = openpyxl.load_workbook(os.path.join(gdir, "tamarack_municipal_estimates_2026.xlsx"), data_only=True).active
    reg = {}
    for r in range(5, ws.max_row + 1):
        m = ws.cell(row=r, column=2).value
        if m in MCD.values():
            reg[m] = (ws.cell(row=r, column=6).value, ws.cell(row=r, column=7).value, ws.cell(row=r, column=8).value)
    for m in MCD.values():
        want = ("Yes" if m in call else "No", v["births"].get(m, 0), v["deaths"].get(m, 0))
        if reg.get(m) != want:
            ok = False
            print("verify: register row %s %s, verifier %s" % (m, reg.get(m), want))
    sub = open(os.path.join(os.path.dirname(gdir), "submission.md"), encoding="utf-8").read()
    for m in call:
        if m not in sub.split("## 2.")[0]:
            ok = False
            print("verify: %s not in the recommendation" % m)
    for kind in ("births", "deaths"):
        for m, n in v[kind].items():
            if not re.search(r"- %s: %s\b" % (re.escape(m), "{:,}".format(n)), sub):
                ok = False
                print("verify: %s %s for %s not in the write-up" % (kind, n, m))
    print("verify: call %s; Cedar Run %.0f, Maple Ford %.0f; births %d, deaths %d; %s" % (
        ", ".join(call), est["Town of Cedar Run"], est["Town of Maple Ford"], sum(v["births"].values()),
        sum(v["deaths"].values()), "agrees" if ok else "DISAGREES"))
    return ok


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    raise SystemExit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
