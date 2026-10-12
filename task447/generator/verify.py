"""Independent verifier: reads only the shipped bundle (target/) with the csv, json and openpyxl
modules and pypdf, shares no code with the generator or golden.py, and recomputes every graded figure.

    python3 verify.py <target> [<figures.json>]
"""
import csv
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, timedelta

import openpyxl
from pypdf import PdfReader

FAR = date(2099, 12, 31)


def d(s):
    s = s.strip()
    if len(s) == 8 and s.isdigit():
        return date(int(s[:4]), int(s[4:6]), int(s[6:]))
    return date(int(s[:4]), int(s[5:7]), int(s[8:10]))


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def line_of(cpt):
    c = int(cpt) if cpt.isdigit() else -1
    if 70010 <= c <= 76999 or 77046 <= c <= 77067:
        return "IMG"
    if 93303 <= c <= 93356:
        return "ECHO"
    if 43235 <= c <= 43270 or 45378 <= c <= 45398:
        return "ENDO"
    if 29805 <= c <= 29999:
        return "ARTH"
    if 80047 <= c <= 89398:
        return "LAB"
    return None


def run(target):
    P = lambda f: os.path.join(target, f)
    # ---- claims, conformed to one shape: (sub, cno, freq, orig, member, product, dos, paid, cpt, qty, allowed, fac, ref, tin)
    fac = []
    for r in rows(P("apcd_op_facility_claims_2024.csv")):
        fac.append(dict(sub=r["submitter_code"], cno=r["payer_claim_control_number"], freq=r["claim_frequency_code"],
                        orig=r["original_claim_control_number"], m=r["member_id"], prod=r["product_id"],
                        dos=d(r["service_from_date"]), paid=d(r["paid_date"]), cpt=r["procedure_code"],
                        qty=int(r["quantity"]), amt=float(r["allowed_amount"]), fac=r["service_facility_npi"],
                        ref=r["referring_provider_npi"], mod=r["procedure_modifier_1"]))
    for r in rows(P("apcd_op_facility_claims_2021_2023.csv")):
        fac.append(dict(sub=r["SUBMITTER_ID"], cno=r["CLAIM_ID"], freq={"O": "1", "R": "7", "V": "8"}[r["CLM_STATUS"]],
                        orig=r["ORIG_CLAIM_ID"], m=r["MEMBER_ID"], prod=r["PRODUCT_ID"], dos=d(r["DOS_FROM"]),
                        paid=d(r["PAID_DT"]), cpt=r["PROC_CD"], qty=int(r["UNITS"]), amt=float(r["ALLOWED_AMT"]),
                        fac=r["FAC_NPI"], ref=r["REF_NPI"], mod=r["MOD1"]))
    gone = {x["orig"] for x in fac if x["freq"] in ("7", "8")}
    fac = [x for x in fac if x["freq"] in ("1", "7") and x["cno"] not in gone]
    prof = rows(P("apcd_professional_claims_2024.csv"))
    gonep = {x["original_claim_control_number"] for x in prof if x["claim_frequency_code"] in ("7", "8")}
    prof = [x for x in prof if x["claim_frequency_code"] in ("1", "7") and x["payer_claim_control_number"] not in gonep]
    # ---- reference
    pr = rows(P("apcd_product_reference.csv"))
    commercial = {x["product_id"] for x in pr if x["line_of_business"] == "Commercial"}
    tiered = {x["product_id"] for x in pr if x["tiered_network"] == "Y"}
    carrier = {x["submitter_code"]: x["carrier_name"] for x in pr}
    place = {}
    for f in json.load(open(P("network_tier_placements_2020_2026.json")))["filings"]:
        for pl in f["hospital_system_placements"]:
            place[(f["product_id"], f["plan_year"], pl["hospital_system"])] = pl["tier"]
    tier = lambda prod, sysn, py: place[(prod, py, sysn)] if prod in tiered else 1
    sysof = {x["facility_npi"]: x["health_system"] for x in rows(P("facility_directory.csv"))}
    county_of_zip = {}
    text = " ".join(pg.extract_text() for pg in PdfReader(P("apcd_extract_data_dictionary.pdf")).pages)
    for county in ("Brown", "Calumet", "Fond du Lac", "Kewaunee", "Manitowoc", "Outagamie", "Sheboygan", "Winnebago"):
        m = re.search(re.escape(county) + r"\s+((?:\d{5}(?:,\s*)?)+)", text)
        for z in re.findall(r"\d{5}", m.group(1)):
            county_of_zip[z] = county
    elig = defaultdict(list)
    for x in rows(P("apcd_eligibility_spans.csv")):
        elig[x["member_id"]].append((d(x["coverage_start"]), d(x["coverage_end"]), x["product_id"],
                                     int(x["benefit_period_begin"][:4]), x["member_zip"]))

    def on(m, dt):
        for s, e, prod, py, z in elig[m]:
            if s <= dt <= e:
                return prod, py, z
        raise KeyError((m, dt))
    # ---- Exhibit C and the Medicare amounts
    mc = {x["hcpcs"]: float(x["cy2025_amount_wi_cbsa24580"]) for x in rows(P("cms_opps_clfs_2025_wisconsin.csv"))}
    wb = openpyxl.load_workbook(P("N25-014_exhibit_C_ledgestone_rates.xlsx"), data_only=True)
    frate, prate = {}, {}
    hdr = None
    for r in wb["Outpatient facility"].iter_rows(values_only=True):
        if r[0] == "CPT/HCPCS":
            hdr = r
        elif hdr and r[0]:
            for j in range(2, 6):
                frate[(hdr[j], str(r[0]))] = float(r[j])
    hdr = None
    for r in wb["Bayfield terms"].iter_rows(values_only=True):
        if r[0] == "Service category":
            hdr = r
        elif hdr and r[0]:
            for c in str(r[1]).split(", "):
                frate[("Bayfield Mutual Health", c)] = round(mc[c] * float(r[2]), 2)
    hdr = None
    for r in wb["Professional"].iter_rows(values_only=True):
        if r[0] == "CPT/HCPCS":
            hdr = r
        elif hdr and r[0]:
            for j in range(3, 8):
                prate[(hdr[j], str(r[0]), r[1] or "")] = float(r[j])
    # ---- billing spans, the register
    spans = defaultdict(list)
    for x in rows(P("npi_reassignment_history.csv")):
        spans[x["npi"]].append((x["billing_tin"], d(x["effective_from"]), d(x["effective_to"]) if x["effective_to"] else FAR))
    reg = rows(P("provider_ownership_register.csv"))
    links = defaultdict(list)
    for x in reg:
        q = x["relationship"].startswith(("owned", "merged into", "affiliated, controlled"))
        links[x["entity_tin"] or x["entity_name"]].append(
            (x["related_entity_name"], x["related_entity_tin"], q, d(x["effective_from"]),
             d(x["effective_to"]) if x["effective_to"] else FAR))
    SYSTEMS = ("Ledgestone Health", "Wolf River Health", "Kinnickinnic Health")

    def system(tin, dt, depth=0):
        for name, ptin, q, s, e in links.get(tin, ()):
            if q and s <= dt <= e:
                if name in SYSTEMS:
                    return name
                if depth < 6:
                    up = system(ptin or name, dt, depth + 1)
                    if up:
                        return up
        return None
    regdates = sorted({d(x["effective_from"]) for x in reg})
    notice = " ".join(pg.extract_text() for pg in PdfReader(P("N25-014_notice_of_material_change.pdf")).pages)
    bmg = re.search(r"Brightwater's number\s*\((\d{2}-\d{7})\)", notice).group(1)
    tins_on = lambda n, dt: {t for t, s, e in spans.get(n, ()) if s <= dt <= e}
    runout = date(2025, 6, 30)
    base = lambda x: date(2024, 1, 1) <= x["dos"] <= date(2024, 12, 31) and x["paid"] <= runout and x["prod"] in commercial

    # ---- professional part
    Pinc = 0.0
    for x in prof:
        if x["billing_provider_tin"] != bmg or not x["product_id"] in commercial:
            continue
        dos, paid = d(x["service_from_date"]), d(x["paid_date"])
        if not (date(2024, 1, 1) <= dos <= date(2024, 12, 31) and paid <= runout):
            continue
        key = (carrier[x["submitter_code"]], x["procedure_code"], x["procedure_modifier_1"])
        Pinc += prate[key] * int(x["quantity"]) - float(x["allowed_amount"])

    # ---- what each system offers (codes its sites bill in 2024)
    offers = defaultdict(set)
    for x in fac:
        if x["dos"].year == 2024 and sysof.get(x["fac"]) in SYSTEMS:
            offers[sysof[x["fac"]]].add(x["cpt"])

    # ---- acquisitions: physicians joining a system with their practice, 2021 to 2023
    def first_in(n, sysn):
        best = None
        for t, s, e in sorted(spans[n], key=lambda z: z[1]):
            for dt in [s] + [r for r in regdates if s < r <= e]:
                if system(t, dt) == sysn:
                    if best is None or dt < best[0]:
                        best = (dt, t)
                    break
        return best
    members_of = defaultdict(set)
    for n, lst in spans.items():
        for t, s, e in lst:
            members_of[t].add(n)

    def joined(sysn, phys_only):
        first = {n: first_in(n, sysn) for n in spans if phys_only(n)}
        first = {n: v for n, v in first.items() if v}
        starts = defaultdict(set)
        for x in reg:
            if x["entity_tin"] and x["relationship"].startswith(("owned", "merged into", "affiliated, controlled")):
                starts[x["entity_tin"]].add(d(x["effective_from"]))
        out = {}
        for n, (dt, t) in first.items():
            prev_day = dt - timedelta(days=1)
            if any(tt == t and s <= prev_day <= e for tt, s, e in spans[n]) and system(t, prev_day) != sysn:
                out[n] = (dt, t)
                continue
            for p in [tt for tt, s, e in spans[n] if e == prev_day or (s <= prev_day <= e and tt != t)]:
                if system(p, prev_day) == sysn:
                    continue
                if dt in starts[p] and system(p, dt) == sysn:
                    out[n] = (dt, p)
                    break
                mem = [m for m in members_of[p] if phys_only(m)]
                mv = [first[m][0] for m in mem if m in first]
                if mv and len(mv) == len(mem) and (max(mv) - min(mv)).days <= 90 and \
                        all(max(e for tt, s, e in spans[m] if tt == p) < first[m][0] for m in mem):
                    out[n] = (dt, p)
                    break
        return out
    tax = {}
    for x in rows(P("carrier_provider_file.csv")):
        tax[x["provider_npi"]] = x["primary_taxonomy"]
    phys = lambda n: tax.get(n, "")[:3] in ("207", "208")
    cand = {}
    for sysn in SYSTEMS:
        for n, (dt, p) in joined(sysn, phys).items():
            cand[n] = (dt, sysn, p)
    sides = defaultdict(set)
    for x in fac:
        if x["ref"] in cand and x["prod"] in commercial:
            sides[x["ref"]].add(x["dos"] >= cand[x["ref"]][0])
    acq = {n: v for n, v in cand.items() if sides[n] == {False, True}}
    hist = []
    for x in fac:
        if x["ref"] in acq and x["prod"] in commercial and x["dos"] <= date(2024, 12, 31):
            dt, sysn, p = acq[x["ref"]]
            if x["cpt"] not in offers[sysn]:
                continue
            prod, py, z = on(x["m"], x["dos"])
            hist.append((p, x["dos"] >= dt, int(sysof.get(x["fac"]) == sysn), tier(prod, sysn, py)))
    pre = defaultdict(lambda: [0, 0])
    for p, post, at, t in hist:
        if not post:
            pre[p][0] += at
            pre[p][1] += 1
    s0 = {p: a / b for p, (a, b) in pre.items()}
    num, den = defaultdict(float), defaultdict(float)
    for p, post, at, t in hist:
        if post:
            num[t] += at - s0[p]
            den[t] += 1 - s0[p]
    raw_cap = {t: num[t] / den[t] for t in num}
    cap = {t: round(v, 2) + 0.0 for t, v in raw_cap.items()}   # stated in whole per cent (4.05)

    # ---- Brightwater's referred services and the projection
    ldg = "Ledgestone Health"
    fam = defaultdict(float)
    moved_q = defaultdict(float)
    for x in fac:
        if not base(x) or x["ref"] not in spans or bmg not in tins_on(x["ref"], x["dos"]):
            continue
        prod, py, z = on(x["m"], x["dos"])
        if x["cpt"] not in offers[ldg] or sysof.get(x["fac"]) == ldg:
            continue
        c = cap[tier(prod, ldg, 2026)]
        newp = frate[(carrier[x["sub"]], x["cpt"])]
        fam[line_of(x["cpt"])] += c * (newp * x["qty"] - x["amt"])
        if line_of(x["cpt"]) in ("IMG", "ENDO", "ARTH"):
            moved_q[(county_of_zip[z], line_of(x["cpt"]))] += c * x["qty"]
    total = Pinc + sum(fam.values())

    # ---- Exhibit 1 (appendix A2): services by county of residence and line; a service two plans were billed
    # for is one service, so each member, date, code, modifier and facility counts the units one plan holds
    span_zip = defaultdict(list)
    for x in rows(P("apcd_eligibility_spans.csv")):
        span_zip[(x["member_id"], x["product_id"])].append((d(x["coverage_start"]), d(x["coverage_end"]), x["member_zip"]))
    per_plan = defaultdict(lambda: defaultdict(int))
    bmg_key = {}
    for x in fac:
        if x["dos"].year != 2024 or x["prod"] not in commercial or line_of(x["cpt"]) not in ("IMG", "ENDO", "ARTH"):
            continue
        z = next(zz for s_, e_, zz in span_zip[(x["m"], x["prod"])] if s_ <= x["dos"] <= e_)
        cty = county_of_zip.get(z)
        if cty not in ("Manitowoc", "Kewaunee"):
            continue
        k = (cty, line_of(x["cpt"]), x["m"], x["dos"], x["cpt"], x["mod"], x["fac"])
        per_plan[k][x["sub"]] += x["qty"]
        bmg_key[k] = bmg_key.get(k, False) or (x["ref"] in spans and bmg in tins_on(x["ref"], x["dos"]))
    tot1, b1 = defaultdict(int), defaultdict(int)
    for k, by in per_plan.items():
        n = max(by.values())
        tot1[k[:2]] += n
        if bmg_key[k]:
            b1[k[:2]] += n
    ex1 = {"%s|%s" % k: ["{:,}".format(tot1[k]), "%.1f" % (100.0 * b1[k] / tot1[k])] for k in tot1}

    # ---- Exhibit 2 (appendix A3): in-person office visits by the rendering physician's own specialty
    own_tax = defaultdict(set)
    for x in rows(P("carrier_provider_file.csv")):
        own_tax[x["provider_npi"]].add(x["primary_taxonomy"])
    assert all(len(v) == 1 for v in own_tax.values()), "one taxonomy per provider"
    spec_of = {"207Q00000X": "primary care", "207R00000X": "primary care", "208000000X": "primary care",
               "207RG0100X": "gastroenterology", "207X00000X": "orthopaedic surgery",
               "207RC0000X": "cardiovascular disease"}
    office = {str(c) for c in range(99202, 99216)}
    visits = defaultdict(lambda: defaultdict(int))
    who = {}
    for x in prof:
        if x["product_id"] not in commercial or x["procedure_code"] not in office:
            continue
        if x["place_of_service"] == "10" or x["procedure_modifier_2"] == "95":
            continue
        dos = d(x["service_from_date"])
        if dos.year != 2024 or county_of_zip.get(x["service_facility_zip"]) not in ("Manitowoc", "Kewaunee"):
            continue
        t = next(iter(own_tax[x["rendering_provider_npi"]]))
        if t not in spec_of:
            continue
        k = (spec_of[t], x["member_id"], dos, x["procedure_code"], x["rendering_provider_npi"])
        visits[k][x["submitter_code"]] += int(x["quantity"])
        who[k] = (x["billing_provider_tin"] == bmg, system(x["billing_provider_tin"], dos) == ldg)
    tot2, b2, l2 = defaultdict(int), defaultdict(int), defaultdict(int)
    for k, by in visits.items():
        n = max(by.values())
        tot2[k[0]] += n
        b2[k[0]] += n if who[k][0] else 0
        l2[k[0]] += n if who[k][1] else 0
    ex2 = {sp: ["%.1f" % (100.0 * b2[sp] / tot2[sp]), "%.1f" % (100.0 * l2[sp] / tot2[sp])] for sp in tot2}
    parts = {"P": int(round(Pinc / 1e4)) * 10000}
    parts.update({k: int(round(v / 1e4)) * 10000 for k, v in fam.items()})
    return {"call": "proceed" if total >= 2_000_000 else "close", "total_m": "%.1f" % (total / 1e6),
            "parts": parts, "ex1": ex1, "ex2": ex2,
            "raw": {"total": total, "P": Pinc, "capture": cap, "fitted": raw_cap}}


def compare(v, figs):
    assert v["call"] == figs["call"], (v["call"], figs["call"])
    assert v["total_m"] == figs["total_m"], (v["total_m"], figs["total_m"])
    assert v["parts"] == figs["parts"], (v["parts"], figs["parts"])
    assert v["ex1"] == {k: list(x) for k, x in figs["ex1"].items()}, (v["ex1"], figs["ex1"])
    assert v["ex2"] == {k: list(x) for k, x in figs["ex2"].items()}, (v["ex2"], figs["ex2"])
    return True


if __name__ == "__main__":
    v = run(sys.argv[1])
    print(json.dumps({k: v[k] for k in v if k != "raw"}, indent=1), v["raw"])
    if len(sys.argv) > 2:
        figs = json.load(open(sys.argv[2]))
        print("verifier agrees with the golden figures:", compare(v, figs))
