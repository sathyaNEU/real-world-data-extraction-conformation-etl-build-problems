#!/usr/bin/env python3
"""task464: the independent verifier. Reads the shipped bundle and nothing else.

    python3 generator/verify.py [--target <dir>] [--figures <path>]

It shares no code with the generator: the positions come from a sweep over the two encounter tables, the
sessions from the roster, the category figure and the standard from the agreement's own text, and every
graded figure is compared with generator/figures.json. Exit 0 all agree, 1 any disagreement.
"""
import argparse
import collections
import csv
import datetime as dt
import json
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def norm(t):
    return re.sub(r"\s+", " ", t or "")


def read_pdf(path):
    import pdfplumber
    with pdfplumber.open(path) as d:
        return norm(" ".join((p.extract_text() or "") for p in d.pages))


def read_xlsx(path, sheet):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    return [[c for c in row] for row in wb[sheet].iter_rows(values_only=True)]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=os.path.join(TASK, "target"))
    ap.add_argument("--figures", default=os.path.join(HERE, "figures.json"))
    a = ap.parse_args(argv)
    T = a.target
    want = json.load(open(a.figures, encoding="utf-8"))
    bad = []

    def same(tag, got, exp):
        if got != exp:
            bad.append("%s: verifier %r, figures.json %r" % (tag, got, exp))

    # the agreement's own words give the standard, the window and the category figure
    ag = read_pdf(os.path.join(T, "network_agreement_2027_capacity_terms.pdf"))
    cushion = float(re.search(r"at or above ([\d.]+) times", ag).group(1))
    assert "a week is one fifty-second of a contract year" in ag
    assert "The 2026 contract year is the calendar year 2026" in ag
    turns = {"in-centre haemodialysis": 1, "ambulatory infusion": 2}
    assert "one for in-centre haemodialysis and two for ambulatory infusion" in ag
    same("constants.cushion", cushion, want["constants"]["cushion"])

    # the population and each site's area and category
    rows = list(csv.DictReader(open(os.path.join(T, "provider_directory_2027.csv"), encoding="utf-8")))
    cur = max(int(r["attestation_cycle"]) for r in rows)
    pop = {r["plan_site_id"]: r for r in rows
           if int(r["attestation_cycle"]) == cur and r["contract_intent_2027"] == "contract"}
    same("constants.sites_in_scope", len(pop), want["constants"]["sites_in_scope"])

    # the roster's sessions a week
    ses = {r["plan_site_id"]: int(r["treatment_sessions_week"]) for r in
           csv.DictReader(open(os.path.join(T, "staffing_roster_2026q4.csv"), encoding="utf-8"))}

    # the greatest number of each site's treatments running at one time, from both layouts
    con = sqlite3.connect(os.path.join(T, "treatment_encounters.db"))
    iv = collections.defaultdict(list)
    y26 = collections.Counter()
    half26 = collections.Counter()
    for sid, sdate, start, stop in con.execute(
            "SELECT service_facility_id, service_date, service_start, service_stop"
            " FROM encounters_2023_2024 WHERE encounter_status='completed'"):
        t0 = dt.datetime.fromisoformat(start.replace(" ", "T"))
        t1 = dt.datetime.fromisoformat(stop.replace(" ", "T"))
        iv[sid].append((int(t0.timestamp()) // 60, int((t1 - t0).total_seconds()) // 60))
    for sid, sdate, start, mins in con.execute(
            "SELECT service_facility_id, service_date, service_start, service_minutes"
            " FROM encounters_2025_2026 WHERE encounter_status='completed'"):
        t0 = dt.datetime.fromisoformat(start)
        iv[sid].append((int(t0.timestamp()) // 60, int(mins)))
        d = dt.date.fromisoformat(sdate)
        if d.year == 2026:
            y26[sid] += 1
            half26[(sid, "H1" if d.month <= 6 else "H2")] += 1
    con.close()

    def sweep(lst):
        ev = sorted([(t, 1) for t, _ in lst] + [(t + d, -1) for t, d in lst])
        cur_n, mx = 0, 0
        for _, k in ev:
            cur_n += k
            mx = max(mx, cur_n)
        return mx

    slots, areas = {}, collections.defaultdict(int)
    for sid, r in sorted(pop.items()):
        pos = sweep(iv[sid])
        s = pos * ses[sid] * turns[r["service_category"]]
        slots[sid] = s
        areas[r["service_area_code"]] += s
        same("site.%s.slots" % sid, s, want["site"][sid]["slots"])
    same("call.network_weekly_slots", sum(slots.values()), want["call"]["network_weekly_slots"])

    # the demand side
    growth = {r["service_area_code"]: float(r["projected_growth_factor"]) for r in
              csv.DictReader(open(os.path.join(T, "enrolment_projection_2027.csv"), encoding="utf-8"))}
    area_vol = collections.Counter()
    for sid, r in pop.items():
        area_vol[r["service_area_code"]] += y26[sid]
    req, short = {}, []
    for c in sorted(areas):
        req[c] = int(round(cushion * growth[c] * area_vol[c] / 52.0))
        same("area.%s.slots" % c, areas[c], want["area"][c]["slots"])
        same("area.%s.required" % c, req[c], want["area"][c]["required"])
        same("area.%s.meets" % c, "yes" if areas[c] >= req[c] else "no", want["area"][c]["meets"])
        if areas[c] < req[c]:
            short.append((req[c] - areas[c], c))
    same("call.areas_short", len(short), want["call"]["areas_short"])
    same("call.nearest_short_shortfall", min(short)[0], want["call"]["nearest_short_shortfall"])
    same("call.required_weekly_slots_network", sum(req.values()),
         want["call"]["required_weekly_slots_network"])
    same("cc1", sum(sweep(iv[sid]) for sid in pop), want["cc1"])
    same("cc2", sum(int(r["attested_stations"]) for r in pop.values()), want["cc2"])
    same("cc4", sum(req.values()), want["cc4"])

    # ask A: the area of the site treated, the service date, the run-out supplement included
    dropped = {r["site_name"]: r["service_area_code"] for r in rows
               if int(r["attestation_cycle"]) == cur and r["contract_intent_2027"] == "none"}
    oon = collections.Counter()
    for fn in ("out_of_network_payments_2026.csv", "out_of_network_payments_runout_2027q1.csv"):
        for r in csv.DictReader(open(os.path.join(T, fn), encoding="utf-8")):
            d = dt.date.fromisoformat(r["service_date"])
            if d.year != 2026:
                continue
            oon[(dropped[r["service_facility_name"]], "H1" if d.month <= 6 else "H2")] += \
                int(r["treatment_units"])
    for c in sorted(areas):
        for h in ("H1", "H2"):
            inn = sum(half26[(sid, h)] for sid, r in pop.items() if r["service_area_code"] == c)
            n = oon[(c, h)]
            tot = n + inn
            same("ask_a.%s.%s.treatments" % (c, h), n, want["ask_a"][c][h]["treatments"])
            same("ask_a.%s.%s.share" % (c, h), round(n * 100.0 / tot, 1) if tot else 0.0,
                 want["ask_a"][c][h]["share"])

    # ask B: the facility row covering the as-of date, per licence number
    asof = dt.date.fromisoformat(json.load(open(os.path.join(TASK, "metadata.json"),
                                                encoding="utf-8"))["as_of"])
    lic = read_xlsx(os.path.join(T, "state_licence_register.xlsx"), "Licences")
    head = [str(h) for h in lic[0]]
    cover = {}
    for r in lic[1:]:
        d = dict(zip(head, r))
        if d["holder_type"] != "facility":
            continue
        f = dt.date.fromisoformat(str(d["effective_from"])[:10])
        t = dt.date.fromisoformat(str(d["effective_to"])[:10]) if d["effective_to"] else None
        if f > asof or (t is not None and t <= asof):
            continue
        cover[d["licence_no"]] = (d["county_or_area"], int(d["licensed_stations"]))
    agg = collections.defaultdict(lambda: [0, 0])
    for k, (c, st) in cover.items():
        agg[c][0] += 1
        agg[c][1] += st
    for c in sorted(areas):
        same("ask_b.%s.sites" % c, agg[c][0], want["ask_b"][c]["sites"])
        same("ask_b.%s.stations" % c, agg[c][1], want["ask_b"][c]["stations"])

    # ask C: the row covering the filing's own position date, distinct sites, the current area
    fil = read_xlsx(os.path.join(T, "state_adequacy_filing_2026.xlsx"), "Contracted Sites")
    fh = [str(h) for h in fil[0]]
    summ = read_xlsx(os.path.join(T, "state_adequacy_filing_2026.xlsx"), "Area Summary")
    pos_date = None
    for r in summ:
        if r and str(r[0]) == "position as at":
            pos_date = dt.date.fromisoformat(str(r[1])[:10])
    at_pos = {}
    for r in lic[1:]:
        d = dict(zip(head, r))
        if d["holder_type"] != "facility":
            continue
        f = dt.date.fromisoformat(str(d["effective_from"])[:10])
        t = dt.date.fromisoformat(str(d["effective_to"])[:10]) if d["effective_to"] else None
        if f > pos_date or (t is not None and t <= pos_date):
            continue
        at_pos[d["licence_no"]] = d["service_address"]
    byaddr = {r["service_address"]: (r["service_area_code"], r["contract_intent_2027"])
              for r in rows if int(r["attestation_cycle"]) == cur}
    best = {}
    for r in fil[1:]:
        d = dict(zip(fh, r))
        rank = 0 if d["licence_no"] in at_pos else 1
        if d["service_address"] not in best or rank < best[d["service_address"]][0]:
            best[d["service_address"]] = (rank, d)
    agg2 = collections.defaultdict(lambda: [0, 0])
    for addr, (rank, d) in sorted(best.items()):
        hit = byaddr.get(at_pos.get(d["licence_no"], addr))
        if hit is None or hit[1] != "none":
            continue
        agg2[hit[0]][0] += 1
        agg2[hit[0]][1] += int(d["licensed_stations"])
    for c in sorted(areas):
        same("ask_c.%s.sites" % c, agg2[c][0], want["ask_c"][c]["sites"])
        same("ask_c.%s.stations" % c, agg2[c][1], want["ask_c"][c]["stations"])

    # the deliverables carry the same figures
    gold = list(csv.DictReader(open(os.path.join(TASK, "golden", "outpatient_capacity_2027.csv"),
                                    encoding="utf-8")))
    for r in gold:
        same("golden csv %s" % r["plan_site_id"], int(r["weekly_treatment_slots"]),
             slots[r["plan_site_id"]])
    ac = read_xlsx(os.path.join(TASK, "golden", "area_capacity_2027.xlsx"), "Area Capacity")
    for r in ac[1:13]:
        same("golden xlsx %s slots" % r[0], r[2], areas[r[0]])
        same("golden xlsx %s required" % r[0], r[3], req[r[0]])
    if bad:
        for b in bad:
            print("DISAGREE  %s" % b)
        print("FAIL  %d disagreements" % len(bad))
        return 1
    print("PASS  verify.py: %d sites, %d areas, %d ask figures, every graded figure recomputed from the"
          " bundle" % (len(pop), len(areas), 48 + 24 + 24))
    return 0


if __name__ == "__main__":
    sys.exit(main())
