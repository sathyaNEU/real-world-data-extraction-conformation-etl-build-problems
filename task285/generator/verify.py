"""task285 independent verifier: reads only target/ (and figures.json to compare), recomputes every graded figure.

Usage: python3 verify.py [path/to/target]   exit 0 when every figure reproduces.
"""
import csv
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
LIMIT = 0.25


def rows(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pdf_text(name):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, name)).pages)


def xlsx_rows(name):
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(T, name), read_only=True).active
    it = ws.iter_rows(values_only=True)
    head = next(it)
    return [dict(zip(head, r)) for r in it]


def in_poly(x, y, ring):
    inside = False
    for i in range(len(ring) - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        if (y1 > y) != (y2 > y) and x1 + (y - y1) * (x2 - x1) / (y2 - y1) > x:
            inside = not inside
    return inside


def load():
    st = defaultdict(dict)
    for r in rows("storage_area_stages_QRN25_D100CC.csv"):
        st[r["storage_area"]][int(r["hour_from_storm_start"])] = float(r["stage_mAOD"])
    polys = {f["properties"]["SA_ID"]: f["geometry"]["coordinates"][0]
             for f in json.load(open(os.path.join(T, "storage_areas_QRN25.geojson")))["features"]}
    net = {f["properties"]["LINK_ID"]: (f["properties"]["START_NODE"], f["properties"]["END_NODE"])
           for f in json.load(open(os.path.join(T, "highways_network_2025.geojson")))["features"]}
    cw = defaultdict(list)
    for r in rows("link_reference_crosswalk_2019_2025.csv"):
        cw[r["link_ref_2019"]].append((float(r["from_chainage_m"]), float(r["to_chainage_m"]), r["link_id_2025"]))
    pts = defaultdict(list)   # link_id_2025 -> [(sa, level)]
    for r in rows("highways_levels_survey_2019.csv"):
        ch = float(r["chainage_m"])
        lid = [c[2] for c in cw[r["link_ref_2019"]] if c[0] - 0.05 <= ch <= c[1] + 0.05]
        lid = lid[0]
        x, y = float(r["easting"]), float(r["northing"])
        sa = next((s for s, ring in polys.items() if in_poly(x, y, ring)), None)
        pts[lid].append((sa, float(r["level_mAOD"])))
    txt = pdf_text("flood_ready_fund_guidance_2027.pdf")
    hosp = re.search(r"network node (HBN-\d{4})", txt).group(1)
    annex = {}
    for m in re.finditer(r"([A-Z][A-Za-z' ]+?)\s*\n\s*(E0401\d{4})\s*\n\s*(HBN-\d{4})", txt):
        annex[m.group(1).strip()] = m.group(3)
    return st, polys, net, pts, hosp, annex


def impassable(pts, st, h, limit=LIMIT):
    return {lid for lid, ps in pts.items() if any(sa and st[sa][h] - lev > limit + 1e-9 for sa, lev in ps)}


def reach(net, closed, hosp):
    adj = defaultdict(set)
    for lid, (a, b) in net.items():
        if lid not in closed:
            adj[a].add(b)
            adj[b].add(a)
    seen, stack = {hosp}, [hosp]
    while stack:
        n = stack.pop()
        for m in adj[n]:
            if m not in seen:
                seen.add(m)
                stack.append(m)
    return seen


def main_call():
    st, polys, net, pts, hosp, annex = load()
    hours = sorted(next(iter(st.values())))
    cut = defaultdict(list)
    counts = {}
    for h in hours:
        closed = impassable(pts, st, h)
        counts[h] = len(closed)
        r = reach(net, closed, hosp)
        for p, node in annex.items():
            if node not in r:
                cut[p].append(h)
    peak_closed = {lid for lid, ps in pts.items() if any(sa and max(st[sa].values()) - lev > LIMIT for sa, lev in ps)}
    wet = {lid for lid, ps in pts.items() if any(sa and max(st[sa].values()) - lev > 0 for sa, lev in ps)}
    env = sorted(p for p, n in annex.items() if n not in reach(net, peak_closed, hosp))
    env0 = sorted(p for p, n in annex.items() if n not in reach(net, wet, hosp))
    wh = max(hours, key=lambda h: (counts[h], -h))
    whs = sorted(p for p, n in annex.items() if n not in reach(net, impassable(pts, st, wh), hosp))
    return sorted(cut), env, env0, (wh, whs), {p: (min(v), max(v)) for p, v in cut.items()}


def households():
    return {r["parish_name"]: int(r["all_dwellings"]) for r in rows("council_tax_dwellings_by_parish_oct2026.csv")}


def datum_shift():
    """the Quarnell Navigation Datum offset the model report gives, and the register sources it applies to: the
    sources whose levels sit that far below the 2022 surveyors' own ground levels at the same UPRNs."""
    m = re.search(r"Quarnell Navigation Datum, which lies (\d\.\d+) m below", pdf_text("quarnell_flood_model_report_2025.pdf"))
    shift = float(m.group(1))
    sv = {int(s["UPRN"]): float(s["Ground level (mAOD)"]) for s in xlsx_rows("pfr_property_survey_2022.xlsx")}
    diff = defaultdict(list)
    for r in rows("address_register_extract_oct2026.csv"):
        u = int(r["UPRN"])
        if u in sv:
            diff[r["LEVEL_SOURCE"]].append(float(r["GROUND_LEVEL_M"]) - sv[u])
    low = {src for src, d in diff.items() if sum(d) / len(d) < -shift / 2}
    return shift, low, {src: (len(d), round(sum(d) / len(d), 3), round(min(d), 2), round(max(d), 2)) for src, d in diff.items()}


def ask1():
    st, polys, net, pts, hosp, annex = load()
    peak = {sa: max(v.values()) for sa, v in st.items()}
    survey = xlsx_rows("pfr_property_survey_2022.xlsx")
    lev = {int(s["UPRN"]): float(s["Threshold level (mAOD)"]) for s in survey}
    units = {int(s["UPRN"]): {u.strip().upper() for u in (s["Ground floor units"] or "").split(",") if u.strip()} for s in survey}
    shift, low, _ = datum_shift()
    reg = rows("address_register_extract_oct2026.csv")
    code_to_parish = {r["parish_code"]: r["parish_name"] for r in rows("council_tax_dwellings_by_parish_oct2026.csv")}
    code_to_parish["E04014119"] = "Hawkesbridge North"
    out = defaultdict(int)
    for r in reg:
        if not (r["CLASS"].startswith("RD") or r["CLASS"].startswith("RH")):
            continue
        x, y = float(r["EASTING"]), float(r["NORTHING"])
        sa = next((s for s, ring in polys.items() if in_poly(x, y, ring)), None)
        if sa is None:
            continue
        u = int(r["UPRN"])
        par = int(r["PARENT_UPRN"]) if r["PARENT_UPRN"] else None
        if par is not None:
            if r["SAO_TEXT"].upper() not in units.get(par, set()):
                continue
            fl = lev[par]
        elif u in lev:
            fl = lev[u]
        else:
            g = float(r["GROUND_LEVEL_M"]) + (shift if r["LEVEL_SOURCE"] in low else 0.0)
            fl = g + 0.15
        if peak[sa] > fl:
            out[code_to_parish[r["PARISH_CODE"]]] += 1
    return dict(out)


def ask2():
    spans = defaultdict(list)
    routes = []
    for r in rows("highways_road_closures_jul2021.csv"):
        a = datetime.strptime(r["closed_local"], "%d/%m/%Y %H:%M")
        b = datetime.strptime(r["reopened_local"], "%d/%m/%Y %H:%M")
        if " to " in r["location"]:
            routes.append((r["road_number"], r["location"], a, b))
            continue
        spans[(r["road_number"], r["location"].split(",")[-1].strip())].append((a, b, r["closure_ref"]))
    # a route closure closes every section of its road between its two ends (the B5131 sections all lie
    # between Hollinside and Lunnerby on the network)
    for road, loc, a, b in routes:
        ends = [x.strip() for x in loc.split(" to ")]
        for k in list(spans):
            if k[0] == road:
                spans[k].append((a, b, "route"))
        assert all(any(k == (road, e) for k in spans) for e in ends), (road, ends)
    # a section is a road at a place; it is labelled with the reference its first barrier row carries
    ref = {k: min(z for z in v if z[2] != "route")[2] for k, v in spans.items()}
    for r in rows("police_road_closures_jul2021.csv"):
        road, place = r["location_text"].split(" ", 1)
        a = datetime.strptime(r["closed_utc"], "%Y-%m-%dT%H:%MZ") + timedelta(hours=1)
        if r["opened_utc"]:
            b = datetime.strptime(r["opened_utc"], "%Y-%m-%dT%H:%MZ") + timedelta(hours=1)
        else:
            # handed to highways: closed until the first highways barrier at the section went up
            b = min(z[0] for z in spans[(road, place)] if z[2] != "route")
        spans[(road, place)].append((a, b, None))
    out = {}
    for k, v in spans.items():
        v = sorted((a, b) for a, b, _ in v)
        merged = []
        for a, b in v:
            if merged and a <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        out[ref[k]] = sum((b - a).total_seconds() for a, b in merged) / 3600.0
    return out


def ask3():
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(T, "flood_ready_ledger_2026.xlsx"), read_only=True)["Transactions"]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    led = [dict(zip(head, r)) for r in it]
    cancelled = {r["cheque_no"] for r in rows("bank_cancelled_cheques_2026.csv")}
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
        if base not in owner:
            # a payment under a reference that is no 2026 award belongs to its payee's 2026 award
            base = award_of[r["Payee"].replace(" Parish Council", "")]
        paid[base] += r["Amount GBP"]
    return {owner[b]: int(round(total[b] - paid[b])) for b in owner}


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    ok = True
    gold, env, env0, wh, hours = main_call()
    hh = households()
    checks = [
        ("golden set", gold == sorted(figs["call"]["parishes"]), gold),
        ("households total", sum(hh[p] for p in gold) == figs["call"]["households_total"], sum(hh[p] for p in gold)),
        ("households each", all(hh[p] == figs["households"][p] for p in gold), {p: hh[p] for p in gold}),
        ("default path envelope", env == sorted(figs["default_path"]["parishes"]), env),
        ("rung 0 any water", env0 == sorted(figs["rungs"]["R0_any_water"]), env0),
        ("rung 2 worst hour", [wh[0], wh[1]] == [figs["rungs"]["R2_worst_hour"][0], sorted(figs["rungs"]["R2_worst_hour"][1])], wh),
        ("cut-off hours", all(list(hours[p]) == figs["cut_off_hours"][p] for p in gold), hours),
    ]
    txt = pdf_text("flood_ready_fund_guidance_2027.pdf").replace("\n", " ")
    budget = int(re.search(r"set aside GBP ([\d,]+) for the 2027 round", txt).group(1).replace(",", ""))
    base = int(re.search(r"base grant of GBP ([\d,]+)", txt).group(1).replace(",", ""))
    rest = budget - base * len(gold)
    tot = sum(hh[p] for p in gold)
    grants = {p: int(round(base + rest * hh[p] / tot)) for p in gold}
    checks.append(("grants", grants == figs["grant_amounts"] and sum(grants.values()) == budget, grants))
    a1 = ask1()
    checks.append(("ask 1 dwellings", all(a1.get(p, 0) == v for p, v in figs["ask1_dwellings_reached"].items()), a1))
    a2 = ask2()
    checks.append(("ask 2 hours", all(int(round(a2[k])) == v for k, v in figs["ask2_closure_hours"].items()), a2))
    a3 = ask3()
    checks.append(("ask 3 unpaid", all(a3[p] == v for p, v in figs["ask3_unpaid"].items()), a3))
    for name, good, detail in checks:
        print("%-24s %s %s" % (name, "PASS" if good else "FAIL", "" if good else detail))
        ok &= bool(good)
    print("verify:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
