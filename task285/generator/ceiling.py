"""task285 ask-layer ceiling, measured on the cut pack (target/ only, through verify.py's readers).

Routes scored figure by figure against figures.json:
  cracker        lands the call and runs the hygiene battery: UTC converted, barrier windows unioned, a police
                 closure with no opening run to the first barrier, the guidance's dwelling, flat and threshold rules
                 executed, cancelled cheques and the 31 October cut applied; reads every level as recorded and keys
                 every record by the reference it carries;
  full includer  the cracker plus the datum seen and every closure keyed by road and place (the route closure
                 kept as a closure of its own), keying ledger payments by payee because some references do not
                 name a 2026 award;
  mirror         files the envelope (off the call) and stops at each ask's most attractive wrong rung: each block's
                 threshold for every flat in it, barrier rows added up by reference, the police closure with no
                 opening left out, every ledger payment counted against the reference it carries.
Pair = ((38 + 7 + 55 Lc) + (5 + 7 + 55 Lm)) / 2, L the share of ask figures each keeps.
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta

import verify as V

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = json.load(open(os.path.join(HERE, "figures.json")))


def ask1(datum_fix, upper_flats_out):
    st, polys, net, pts, hosp, annex = V.load()
    peak = {sa: max(v.values()) for sa, v in st.items()}
    survey = V.xlsx_rows("pfr_property_survey_2022.xlsx")
    lev = {int(s["UPRN"]): float(s["Threshold level (mAOD)"]) for s in survey}
    units = {int(s["UPRN"]): {u.strip().upper() for u in (s["Ground floor units"] or "").split(",") if u.strip()} for s in survey}
    shift, low, _ = V.datum_shift()
    code_to_parish = {r["parish_code"]: r["parish_name"] for r in V.rows("council_tax_dwellings_by_parish_oct2026.csv")}
    code_to_parish["E04014119"] = "Hawkesbridge North"
    out = defaultdict(int)
    for r in V.rows("address_register_extract_oct2026.csv"):
        if not (r["CLASS"].startswith("RD") or r["CLASS"].startswith("RH")):
            continue
        x, y = float(r["EASTING"]), float(r["NORTHING"])
        sa = next((s for s, ring in polys.items() if V.in_poly(x, y, ring)), None)
        if sa is None:
            continue
        par = int(r["PARENT_UPRN"]) if r["PARENT_UPRN"] else None
        g = float(r["GROUND_LEVEL_M"]) + (shift if datum_fix and r["LEVEL_SOURCE"] in low else 0.0)
        if par is not None:
            if upper_flats_out and r["SAO_TEXT"].upper() not in units.get(par, set()):
                continue
            fl = lev.get(par, g + 0.15)
        else:
            fl = lev.get(int(r["UPRN"]), g + 0.15)
        if peak[sa] > fl:
            out[code_to_parish[r["PARISH_CODE"]]] += 1
    return out


def ask2(by_ref, union, blank_to_barrier, route_to_sections=False, utc_convert=True):
    hw = V.rows("highways_road_closures_jul2021.csv")
    if route_to_sections:
        route = [r for r in hw if " to " in r["location"]]
        hw = [r for r in hw if " to " not in r["location"]]
    place = lambda r: (r["road_number"], r["location"].split(",")[-1].strip())
    first = {}
    for r in sorted(hw, key=lambda r: datetime.strptime(r["closed_local"], "%d/%m/%Y %H:%M")):
        first.setdefault(place(r), r["closure_ref"])
    spans = defaultdict(list)
    for r in hw:
        a = datetime.strptime(r["closed_local"], "%d/%m/%Y %H:%M")
        b = datetime.strptime(r["reopened_local"], "%d/%m/%Y %H:%M")
        spans[r["closure_ref"] if by_ref else first[place(r)]].append((a, b))
    if route_to_sections:
        for r in route:
            a = datetime.strptime(r["closed_local"], "%d/%m/%Y %H:%M")
            b = datetime.strptime(r["reopened_local"], "%d/%m/%Y %H:%M")
            for k, ref in first.items():
                if k[0] == r["road_number"]:
                    spans[ref].append((a, b))
    for r in V.rows("police_road_closures_jul2021.csv"):
        road, pl = r["location_text"].split(" ", 1)
        key = first[(road, pl)]
        off = timedelta(hours=1 if utc_convert else 0)
        a = datetime.strptime(r["closed_utc"], "%Y-%m-%dT%H:%MZ") + off
        if r["opened_utc"]:
            b = datetime.strptime(r["opened_utc"], "%Y-%m-%dT%H:%MZ") + off
        elif blank_to_barrier:
            b = min(datetime.strptime(z["closed_local"], "%d/%m/%Y %H:%M") for z in hw
                    if place(z) == (road, pl))
        else:
            continue
        spans[key].append((a, b))
    out = {}
    for k, v in spans.items():
        v.sort()
        if union:
            m = []
            for a, b in v:
                if m and a <= m[-1][1]:
                    m[-1] = (m[-1][0], max(m[-1][1], b))
                else:
                    m.append((a, b))
            v = m
        out[k] = int(round(sum((b - a).total_seconds() for a, b in v) / 3600))
    return out


def ask3(cancel, key):
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(V.T, "flood_ready_ledger_2026.xlsx"), read_only=True)["Transactions"]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    led = [dict(zip(head, r)) for r in it]
    cancelled = {r["cheque_no"] for r in V.rows("bank_cancelled_cheques_2026.csv")} if cancel else set()
    owner, total, paid = {}, defaultdict(float), defaultdict(float)
    for r in led:
        base = r["Reference"].split("-V")[0]
        if r["Type"] == "AWARD":
            owner[base] = r["Payee"].replace(" Parish Council", "")
        if r["Type"] in ("AWARD", "VARIATION"):
            total[base] += r["Amount GBP"]
    award_of = {p: b for b, p in owner.items()}
    for r in led:
        if r["Type"] != "PAYMENT" or r["Posted"].strftime("%Y-%m-%d") > "2026-10-31":
            continue
        if r["Cheque no"] and str(r["Cheque no"]) in cancelled:
            continue
        base = r["Reference"].split("-V")[0]
        payee = r["Payee"].replace(" Parish Council", "")
        if key == "reference":
            b = base if base in owner else None
        elif key == "payee":
            b = award_of.get(payee)
        else:
            b = base if base in owner else award_of.get(payee)
        if b:
            paid[b] += r["Amount GBP"]
    return {owner[b]: int(round(total[b] - paid[b])) for b in owner}


def score(a1, a2, a3):
    g1, g2, g3 = FIG["ask1_dwellings_reached"], FIG["ask2_closure_hours"], FIG["ask3_unpaid"]
    h1 = sum(1 for k, v in g1.items() if a1.get(k, 0) == v)
    h2 = sum(1 for k, v in g2.items() if a2.get(k) == v)
    h3 = sum(1 for k, v in g3.items() if a3.get(k) == v)
    n = len(g1) + len(g2) + len(g3)
    return (h1, len(g1)), (h2, len(g2)), (h3, len(g3)), (h1 + h2 + h3) / n


def main():
    crack = score(ask1(False, True), ask2(True, True, True), ask3(True, "reference"))
    full = score(ask1(True, True), ask2(False, True, True), ask3(True, "payee"))
    mirror = score(ask1(False, False), ask2(True, False, False), ask3(False, "reference"))
    gold = score(ask1(True, True), ask2(False, True, True, True), ask3(True, "award"))
    C = 38 + 7 + 55 * crack[3]
    S = 5 + 7 + 55 * mirror[3]
    print("| route | ask 1 kept | ask 2 kept | ask 3 kept | share of ask weight |")
    print("|---|---|---|---|---|")
    for name, s in (("cracker (call landed)", crack), ("full includer (datum seen, closures by place, payments by payee)", full),
                    ("mirror (call missed)", mirror), ("golden handling", gold)):
        print("| %s | %d of %d | %d of %d | %d of %d | %.1f per cent |" % (name, s[0][0], s[0][1], s[1][0], s[1][1],
                                                                      s[2][0], s[2][1], 100 * s[3]))
    print("Pair ceiling: %.1f (cracker %.1f, mirror %.1f)" % ((C + S) / 2, C, S))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * mirror[3]))
    assert gold[3] == 1.0, gold
    sys.exit(0)


if __name__ == "__main__":
    main()
