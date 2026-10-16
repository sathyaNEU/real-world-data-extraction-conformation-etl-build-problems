"""Write the data files of the pack under target/ from the simulation: the APCD extracts (two layouts),
eligibility, the product reference, the carriers' tier placements, the register, the reassignment
history, the carriers' provider file, the facility directory, the Medicare amounts, Ledgestone's rate
exhibit and the two neighbouring files. Documents (PDF) are written by docs.py.

Ask-path mess is applied here, only to rows outside the main call's population (Brightwater's 2024
professional and referral claims, the acquired practices' referral claims 2021 to 2024, and those
members' eligibility), and every device row is tagged in the returned ledger for the checks.
"""
import csv
import json
import os
from collections import defaultdict
from datetime import date, timedelta

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import orgs as O
import sim as S
import world as W

D = date
h01 = S.h01

RUNOUT = D(2025, 6, 30)
PULL = W.EXTRACT_PULL                     # 2025-09-15
MAIN_TAGS = ("bmg_ref", "bmg_prof", "hist_ref")

FILES = {
    "fac24": "apcd_op_facility_claims_2024.csv",
    "fachist": "apcd_op_facility_claims_2021_2023.csv",
    "prof24": "apcd_professional_claims_2024.csv",
    "elig": "apcd_eligibility_spans.csv",
    "prodref": "apcd_product_reference.csv",
    "tiers": "network_tier_placements_2020_2026.json",
    "register": "provider_ownership_register.csv",
    "reassign": "npi_reassignment_history.csv",
    "provfile": "carrier_provider_file.csv",
    "facdir": "facility_directory.csv",
    "medicare": "cms_opps_clfs_2025_wisconsin.csv",
    "exhibit": "N25-014_exhibit_C_ledgestone_rates.xlsx",
    "hcris": "hcris_hospital_outpatient_extract_fy2023.csv",
    "ma": "apcd_medicare_advantage_facility_claims_2024.csv",
    "manifest": "export_manifest.csv",
}

# ------------------------------------------------------------------ identifiers
FAC_NPI = {f[0]: W.npi_from("fac|" + f[0]) for f in W.FACILITIES}
FAC_TIN = {f[0]: W.tin_from("fac|" + f[0]) for f in W.FACILITIES}
SYS_TIN = {"LDG": W.tin_from("sys|LDG"), "WRH": W.tin_from("sys|WRH"), "KNK": W.tin_from("sys|KNK")}
GROUP_NPI = {p: W.npi_from("grp|" + p) for p in O.PRACTICES}


def billing_of(fkey):
    """Hospital outpatient departments bill under their hospital; Ledgestone's Manitowoc centre is an
    off-campus department of Ledgestone Medical Center."""
    if fkey == "LMN":
        return FAC_NPI["LMC"], SYS_TIN["LDG"]
    sysk = W.FAC[fkey][2]
    if sysk is not None:
        return FAC_NPI[fkey], SYS_TIN[sysk]
    return FAC_NPI[fkey], FAC_TIN[fkey]


def claim_number(carrier, d, seq):
    if carrier == "C1":
        return "CB%s%06d" % (d.strftime("%y%j"), seq % 1000000)
    if carrier == "C2":
        return "1%04d%07d" % (d.year % 10000 // 1, seq % 10000000)
    if carrier == "C3":
        return "NB-%02d%08d" % (d.year % 100, seq % 100000000)
    if carrier == "C4":
        return "LF%s-%05d" % (d.strftime("%y%m%d"), seq % 100000)
    return "H%02d%09d" % (d.year % 100, seq % 1000000000)


class Numberer:
    def __init__(self):
        self.seq = defaultdict(lambda: 0)
        self.used = set()

    def next(self, carrier, d, salt):
        base = int(h01("cn", carrier, salt) * 900000) + 100000
        while True:
            self.seq[carrier] += 1
            n = claim_number(carrier, d, base * 37 + self.seq[carrier] * 7919)
            if n not in self.used:
                self.used.add(n)
                return n


# ------------------------------------------------------------------ cost sharing
def member_share(product, fac_tier, kind, key):
    ptype = W.PRODUCTS[product][2]
    if kind == "prof":
        base = 0.09 if ptype == "HMO" else 0.15
    elif W.PRODUCTS[product][3]:
        base = 0.12 if fac_tier == 1 else 0.36
    else:
        base = 0.08 if ptype == "HMO" else 0.17
    return round(base + 0.04 * (h01("ms", key) - 0.5), 4)


def money(x):
    return "%.2f" % x


# the second plan submits most, not all, of the services it receives after the first carrier pays
SECOND_SUBMITTED = 0.86
# billing offices that report their group's taxonomy in the rendering provider loop
GROUP_TAXONOMY = {"KPN": "207Q00000X"}

FAMILY_REV = {"IMG": "0320", "ECHO": "0483", "ENDO": "0750", "ARTH": "0360", "LAB": "0300", "SLEEP": "0740",
              "NUC": "0341"}
REV_BY_CPT = {"70551": "0610", "72148": "0610", "73721": "0610", "74177": "0350", "71250": "0350",
              "76700": "0402", "77067": "0403"}
INDEP_POS = {"IDTF": "11", "ASC": "24", "LAB": "81"}


def lag_days(carrier, key):
    lo, hi = {"C1": (9, 41), "C2": (14, 52), "C3": (11, 46), "C4": (18, 75), "C5": (12, 44)}[carrier]
    return lo + int(h01("lag", key) * (hi - lo))


# ------------------------------------------------------------------ claims
def build_claims(mem, people, lines):
    """Turn the simulated service lines into claim lines with the 2024 devices. Returns
    (facility rows by year, professional rows, device ledger)."""
    num = Numberer()
    fac_rows, prof_rows = [], []
    second = []                           # lines a spouse's plan may also have been billed for
    ledger = defaultdict(list)            # device -> list of claim numbers touched
    for i, l in enumerate(lines):
        key = l.get("key", ("ln", i))
        d = l["date"]
        car = l["carrier"]
        prod = l["product"]
        py = mem.plan_year(l["member"], d)
        paid = d + timedelta(days=lag_days(car, key))
        late = False
        # two self-funded groups administered by Lakefront: fourth-quarter 2024 claims held in the plans'
        # stop-loss review and paid in July and August 2025
        if l["tag"] not in MAIN_TAGS and mem.info[l["member"]]["group"] in ("KCSD", "TRWC") and d >= D(2024, 10, 1):
            paid = D(2025, 7, 8) + timedelta(days=int(h01("late", key) * 50))
            late = True
        if l["kind"] == "fac":
            f = l["fac"]
            sysk = W.FAC[f][2]
            ftier = 1 if sysk is None else W.tier_for(prod, sysk, py)
            unit_price = S.rate(f, car, l["cpt"], d.year)
            qty = l["units"]
            fam = W.CPT[l["cpt"]][1]
            bill_npi, bill_tin = billing_of(f)
            hosp = sysk is not None
            mod = ""
            # bilateral knee films and the occasional bilateral knee arthroscopy: two lines, RT and LT, on one claim
            bilateral = (l["tag"] in ("lake_ref", "other_ref") and
                         ((l["cpt"] == "73562" and h01("bilat", key) < 0.18) or
                          (l["cpt"] == "29881" and h01("bilat_a", key) < 0.05)))
            base = dict(year=d.year, tag=l["tag"], practice=l["practice"], member=l["member"], product=prod,
                        carrier=car, dos=d, paid=paid, fac=f, cpt=l["cpt"], ref_npi=l["ref_npi"],
                        bill_npi=bill_npi, bill_tin=bill_tin, fac_npi=FAC_NPI[f], fac_zip=W.FAC[f][4],
                        form="UB04" if hosp else "CMS1500",
                        tob="0131" if hosp else "", pos="" if hosp else INDEP_POS[W.FAC[f][3]],
                        rev=REV_BY_CPT.get(l["cpt"], FAMILY_REV[fam]) if hosp else "",
                        freq="1", orig="", late=late, device=[])
            if late:
                base["device"].append("late_paid")
                ledger["late_paid"].append(i)
            cno = num.next(car, d, key)
            claim_lines = []
            if bilateral:
                base["device"].append("bilateral_lines")
                ledger["bilateral_lines"].append(i)
                for ln, m in ((1, "RT"), (2, "LT")):
                    claim_lines.append((ln, m, 1))
            else:
                claim_lines.append((1, mod, qty))
            originals = []
            for ln, m, q in claim_lines:
                allowed = round(unit_price * q, 2)
                ms = member_share(prod, ftier, "fac", key + (ln,))
                liab = round(allowed * ms, 2)
                originals.append(dict(base, cno=cno, line=ln, mod=m, qty=q, allowed=allowed, liab=liab,
                                      plan=round(allowed - liab, 2)))
            fac_rows.extend(originals)
            versioned = False
            # replacements and voids on Kinnickinnic's own referrals to its Manitowoc hospital
            if l["tag"] == "lake_ref" and l["practice"] == "KPN" and f == "KLH" and d.year == 2024:
                u = h01("ver", key)
                if u < 0.095:
                    versioned = True
                if u < 0.07:
                    # replaced: corrected charge lines resubmitted under a new number
                    rno = num.next(car, d, key + ("r",))
                    adj = 0.94 + 0.12 * h01("adj", key)
                    rpaid = paid + timedelta(days=21 + int(h01("rp", key) * 40))
                    for ln, m, q in claim_lines:
                        allowed = round(unit_price * q * adj, 2)
                        ms = member_share(prod, ftier, "fac", key + (ln, "r"))
                        liab = round(allowed * ms, 2)
                        fac_rows.append(dict(base, cno=rno, line=ln, mod=m, qty=q, allowed=allowed, liab=liab,
                                             plan=round(allowed - liab, 2), freq="7", orig=cno, paid=rpaid,
                                             device=base["device"] + ["replaced"]))
                    ledger["replaced"].append(i)
                elif u < 0.095:
                    # voided in error, then billed again as a new original
                    vpaid = paid + timedelta(days=15 + int(h01("vp", key) * 30))
                    for row in originals:
                        fac_rows.append(dict(row, freq="8", orig=cno, paid=vpaid, qty=-row["qty"],
                                             allowed=-row["allowed"], liab=-row["liab"], plan=-row["plan"],
                                             device=row["device"] + ["voided"]))
                    nno = num.next(car, d, key + ("n",))
                    npaid = vpaid + timedelta(days=9 + int(h01("np", key) * 20))
                    for ln, m, q in claim_lines:
                        allowed = round(unit_price * q, 2)
                        ms = member_share(prod, ftier, "fac", key + (ln, "n"))
                        liab = round(allowed * ms, 2)
                        fac_rows.append(dict(base, cno=nno, line=ln, mod=m, qty=q, allowed=allowed, liab=liab,
                                             plan=round(allowed - liab, 2), paid=npaid,
                                             device=base["device"] + ["rebilled"]))
                    ledger["voided"].append(i)
            if not versioned and l["tag"] not in MAIN_TAGS and l["practice"] != "MFP" and sysk != "LDG":
                second.append((i, "fac", originals))
        else:
            code = l["code"]
            cpt = code.split("-")[0]
            mod1 = "26" if code.endswith("-26") else ""
            mod2 = ""
            pos = l["pos"]
            if l["tele"] == "10":
                pos = "10"
            elif l["tele"] == "95":
                mod2 = "95"
            bp = l["practice"]
            if bp == "BMG":
                price = S.bmg_prof_rate(car, code)
            elif bp == "LMG":
                price = S.ldg_prof_rate(car, code)
            else:
                price = S.other_prof_rate(bp, car, code)
            allowed = round(price, 2)
            ms = member_share(prod, 1, "prof", key)
            liab = round(allowed * ms, 2)
            tin = O.tin_of(bp)
            if bp == "LMG":
                tin = O.tin_of("LMG")
            # Kinnickinnic's business office reports the network's own taxonomy for every rendering provider
            taxonomy = GROUP_TAXONOMY.get(bp, people[l["rnd_npi"]]["taxonomy"])
            row = dict(year=2024, tag=l["tag"], practice=bp, member=l["member"], product=prod, carrier=car, dos=d,
                       paid=paid, cno=num.next(car, d, key), line=1, freq="1", orig="", pos=pos, cpt=cpt,
                       mod1=mod1, mod2=mod2, qty=1, allowed=allowed, liab=liab, plan=round(allowed - liab, 2),
                       bill_npi=GROUP_NPI[bp], bill_tin=tin, bill_zip=O.BILLING_ZIP.get(bp, O.PRACTICES[bp][2][0]),
                       rnd_npi=l["rnd_npi"], taxonomy=taxonomy, site_zip=l["site_zip"],
                       late=late, device=["late_paid"] if late else [])
            if taxonomy != people[l["rnd_npi"]]["taxonomy"]:
                row["device"] = row["device"] + ["group_taxonomy"]
                ledger["group_taxonomy"].append(i)
            prof_rows.append(row)
            if l["tag"] not in MAIN_TAGS and bp != "MFP":
                second.append((i, "prof", [row]))
    # the spouse's plan: the same services submitted again by the second carrier after the first paid, priced on
    # what the first left the member to pay (numbered after every first-carrier claim)
    for i, kind, rows in second:
        l = lines[i]
        k2 = l.get("key", i)
        p2 = mem.second_on(l["member"], l["date"])
        if p2 is None or h01("cob_sub", k2) >= SECOND_SUBMITTED:
            continue
        car2 = W.PRODUCTS[p2][0]
        cno2 = num.next(car2, l["date"], ("ln2", k2))
        paid2 = rows[0]["paid"] + timedelta(days=24 + int(h01("cob_lag", k2) * 46))
        for r in rows:
            a2 = r["liab"]
            pl2 = round(a2 * (0.72 + 0.26 * h01("cob_pay", k2, r["line"])), 2)
            out = dict(r, carrier=car2, product=p2, cno=cno2, freq="1", orig="", paid=paid2, allowed=a2, plan=pl2,
                       liab=round(a2 - pl2, 2), device=r["device"] + ["second_plan"])
            (fac_rows if kind == "fac" else prof_rows).append(out)
        ledger["second_plan"].append(i)
    return fac_rows, prof_rows, ledger


FAC24_COLS = ["submitter_code", "payer_claim_control_number", "line_counter", "claim_frequency_code",
              "original_claim_control_number", "form_type", "member_id", "product_id", "service_from_date",
              "paid_date", "type_of_bill", "place_of_service", "revenue_code", "procedure_code",
              "procedure_modifier_1", "quantity", "allowed_amount", "plan_paid_amount", "member_liability_amount",
              "billing_provider_npi", "billing_provider_tin", "service_facility_npi", "service_facility_zip",
              "referring_provider_npi"]
FACV2_COLS = ["SUBMITTER_ID", "CLAIM_ID", "LINE_NO", "CLM_STATUS", "ORIG_CLAIM_ID", "FORM", "MEMBER_ID",
              "PRODUCT_ID", "DOS_FROM", "PAID_DT", "TOB", "POS", "REV_CD", "PROC_CD", "MOD1", "UNITS",
              "ALLOWED_AMT", "PLAN_PAID_AMT", "MBR_RESP_AMT", "BILL_NPI", "BILL_TIN", "FAC_NPI", "REF_NPI"]
PROF_COLS = ["submitter_code", "payer_claim_control_number", "line_counter", "claim_frequency_code",
             "original_claim_control_number", "member_id", "product_id", "service_from_date", "paid_date",
             "place_of_service", "procedure_code", "procedure_modifier_1", "procedure_modifier_2", "quantity",
             "allowed_amount", "plan_paid_amount", "member_liability_amount", "billing_provider_npi",
             "billing_provider_tin", "billing_provider_zip", "rendering_provider_npi", "rendering_provider_taxonomy",
             "service_facility_zip"]


def sort_key(r):
    return (r["paid"], r["cno"], r["line"], r["freq"])


def write_fac24(rows, path):
    rows = sorted((r for r in rows if r["year"] == 2024 and r["paid"] <= PULL - timedelta(days=15)), key=sort_key)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(FAC24_COLS)
        for r in rows:
            w.writerow([W.CARRIERS[r["carrier"]]["submitter"], r["cno"], r["line"], r["freq"], r["orig"], r["form"],
                        r["member"], r["product"], r["dos"].isoformat(), r["paid"].isoformat(), r["tob"], r["pos"],
                        r["rev"], r["cpt"], r["mod"], r["qty"], money(r["allowed"]), money(r["plan"]),
                        money(r["liab"]), r["bill_npi"], r["bill_tin"], r["fac_npi"], r["fac_zip"], r["ref_npi"]])
    return rows


def write_fachist(rows, path):
    rows = sorted((r for r in rows if r["year"] < 2024), key=sort_key)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(FACV2_COLS)
        for r in rows:
            w.writerow([W.CARRIERS[r["carrier"]]["submitter"], r["cno"], r["line"], "O", "", r["form"][:2],
                        r["member"], r["product"], r["dos"].strftime("%Y%m%d"), r["paid"].strftime("%Y%m%d"),
                        r["tob"][1:] if r["tob"] else "", r["pos"], r["rev"], r["cpt"], r["mod"], r["qty"],
                        "%.2f" % r["allowed"], "%.2f" % r["plan"], "%.2f" % r["liab"], r["bill_npi"],
                        r["bill_tin"].replace("-", ""), r["fac_npi"], r["ref_npi"]])
    return rows


def write_prof24(rows, path):
    rows = sorted((r for r in rows if r["paid"] <= PULL - timedelta(days=15)), key=sort_key)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(PROF_COLS)
        for r in rows:
            w.writerow([W.CARRIERS[r["carrier"]]["submitter"], r["cno"], r["line"], r["freq"], r["orig"], r["member"],
                        r["product"], r["dos"].isoformat(), r["paid"].isoformat(), r["pos"], r["cpt"], r["mod1"],
                        r["mod2"], r["qty"], money(r["allowed"]), money(r["plan"]), money(r["liab"]), r["bill_npi"],
                        r["bill_tin"], r["bill_zip"], r["rnd_npi"], r["taxonomy"], r["site_zip"]])
    return rows


# ------------------------------------------------------------------ eligibility
ELIG_COLS = ["member_id", "submitter_code", "product_id", "coverage_start", "coverage_end", "benefit_period_begin",
             "relationship_code", "birth_year", "sex", "member_zip"]


def elig_rows(mem, used):
    out = []
    for mid in sorted(mem.info):
        if mid not in used:
            continue
        inf = mem.info[mid]
        rel = "18" if h01("rel", mid) < 0.55 else ("01" if h01("rel2", mid) < 0.5 else "19")
        cuts = set()
        for p, s, e in inf["spans"]:
            cuts.add(s)
            cuts.add(e + timedelta(days=1))
        for z, s, e in inf["zips"]:
            cuts.add(s)
            cuts.add(e + timedelta(days=1))
        first = min(s for _, s, _ in inf["spans"])
        last = max(e for _, _, e in inf["spans"])
        y = first.year - 1
        while True:
            rd = D(y, inf["renew"], 1)
            if rd > last:
                break
            if rd > first:
                cuts.add(rd)
            y += 1
        cuts = sorted(c for c in cuts if first <= c <= last + timedelta(days=1))
        for a, b in zip(cuts, cuts[1:]):
            e = b - timedelta(days=1)
            prod = mem.product_on(mid, a)
            py = W.plan_year_of(a, inf["renew"])
            bpb = D(py, inf["renew"], 1)
            out.append([mid, W.CARRIERS[W.PRODUCTS[prod][0]]["submitter"], prod, a.isoformat(), e.isoformat(),
                        bpb.isoformat(), rel, inf["birth"], inf["sex"], mem.zip_on(mid, a)])
        sc = inf.get("second")
        if sc:
            p2, s2, e2, rn2 = sc
            rel2 = "01" if h01("rel_s", mid) < 0.8 else "19"
            cuts2 = {s2, e2 + timedelta(days=1)}
            for z, s, e in inf["zips"]:
                cuts2.add(s)
                cuts2.add(e + timedelta(days=1))
            y = s2.year - 1
            while D(y, rn2, 1) <= e2:
                if D(y, rn2, 1) > s2:
                    cuts2.add(D(y, rn2, 1))
                y += 1
            cuts2 = sorted(c for c in cuts2 if s2 <= c <= e2 + timedelta(days=1))
            for a, b in zip(cuts2, cuts2[1:]):
                py = W.plan_year_of(a, rn2)
                out.append([mid, W.CARRIERS[W.PRODUCTS[p2][0]]["submitter"], p2, a.isoformat(),
                            (b - timedelta(days=1)).isoformat(), D(py, rn2, 1).isoformat(), rel2, inf["birth"],
                            inf["sex"], mem.zip_on(mid, a)])
    return out


# ------------------------------------------------------------------ reference files
def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(r)


SEGMENT = {"CBH-PPO1": "Large group", "CBH-TPO2": "Large group", "CBH-HMO1": "Small group", "BMH-PPO1": "Large group",
           "BMH-VTP3": "Large group", "BMH-HMO2": "Individual", "NBH-PPO1": "Large group", "NBH-TEP4": "Small group",
           "LBA-PPO7": "Self-funded (ASO)", "LBA-TPO9": "Self-funded (ASO)", "HCH-PPO1": "Small group"}
FUNDING = {"C1": "Fully insured", "C2": "Fully insured", "C3": "Fully insured", "C4": "Self-funded",
           "C5": "Fully insured"}
MA_PRODUCTS = {"CBH-MA01": ("C1", "Cedarbrook Medicare Advantage HMO", "HMO"),
               "BMH-MA05": ("C2", "Bayfield Medicare Advantage PPO", "PPO"),
               "NBH-MA03": ("C3", "Norbridge Medicare Advantage HMO-POS", "HMO-POS")}


def product_reference():
    rows = []
    for pid in sorted(W.PRODUCTS):
        car, name, ptype, tiered = W.PRODUCTS[pid]
        rows.append([pid, W.CARRIERS[car]["submitter"], W.CARRIERS[car]["name"], name, ptype, "Commercial",
                     SEGMENT[pid], FUNDING[car], "Y" if tiered else "N", "2019-01-01", ""])
    for pid in sorted(MA_PRODUCTS):
        car, name, ptype = MA_PRODUCTS[pid]
        rows.append([pid, W.CARRIERS[car]["submitter"], W.CARRIERS[car]["name"], name, ptype, "Medicare Advantage",
                     "Medicare Advantage", "Fully insured", "N", "2019-01-01", ""])
    return (["product_id", "submitter_code", "carrier_name", "product_name", "product_type", "line_of_business",
             "market_segment", "funding_type", "tiered_network", "product_effective_date", "product_end_date"], rows)


TIER_LABELS = {"CBH-TPO2": ("Choice", "Standard"), "BMH-VTP3": ("Value", "Standard"),
               "NBH-TEP4": ("Tier 1", "Tier 2"), "LBA-TPO9": ("Preferred", "Standard")}
FILING_PREFIX = {"C1": "CDBK", "C2": "BAYF", "C3": "NORB", "C4": "LKBA"}


def tier_filings():
    out = []
    for pid in sorted(W.TIER_PLACEMENTS):
        car = W.PRODUCTS[pid][0]
        lab1, lab2 = TIER_LABELS[pid]
        for py in range(W.FIRST_PLAN_YEAR, W.LAST_PLAN_YEAR + 1):
            appr = D(py - 1, 6 + int(h01("appr", pid, py) * 3), 3 + int(h01("apd", pid, py) * 24))
            placements = []
            for sysk in ("LDG", "WRH", "KNK"):
                t = W.tier_for(pid, sysk, py)
                placements.append({"hospital_system": W.SYSTEMS[sysk],
                                   "facilities": [FAC_NPI[f[0]] for f in W.FACILITIES if f[2] == sysk],
                                   "tier": t, "tier_label": lab1 if t == 1 else lab2})
            out.append({"carrier": W.CARRIERS[car]["name"], "submitter_code": W.CARRIERS[car]["submitter"],
                        "product_id": pid, "product_name": W.PRODUCTS[pid][1], "plan_year": py,
                        "form_filing_number": "%s-%d%07d" % (FILING_PREFIX[car], py - 1, int(h01("ff", pid, py) * 1e7)),
                        "approved": appr.isoformat(),
                        "tier_labels": {"1": lab1, "2": lab2},
                        "hospital_system_placements": placements,
                        "freestanding_facilities_tier": 1})
    return {"maintained_by": "Office of Health Care Cost Review, market oversight unit",
            "purpose": "standing reference on the tier placements carriers have filed for tiered-network products",
            "source": "network tier exhibits from carrier form filings approved by the Office of the Commissioner of Insurance",
            "updated": "2025-09-26 (plan year 2026 filings added)",
            "note": "One record per tiered product and plan year. A plan year is named by the calendar year in which it begins; a group renewing on 1 July holds the plan year that began on 1 July of the year before until 30 June. Products without tiers place every in-network facility on one level of cost sharing and are not listed.",
            "filings": out}


def register_rows():
    name = {k: v[0] for k, v in O.PRACTICES.items()}
    name.update(W.SYSTEMS)
    rows = []
    for i, (child, parent, rel, start, end, src) in enumerate(O.REGISTER):
        rid = "R-%04d" % (1000 + i * 7 + int(h01("rid", child, parent) * 5))
        rows.append([rid, name[child], O.tin_of(child) if child in O.PRACTICES else "", name[parent],
                     O.tin_of(parent) if parent in O.PRACTICES else SYS_TIN[parent], rel, start.isoformat(),
                     end.isoformat() if end else "", src])
    # standing registrations of the three systems and their hospitals (context rows)
    for sysk in ("LDG", "WRH", "KNK"):
        for f in W.FACILITIES:
            if f[2] == sysk and f[0] != "LMN":
                rows.append(["R-%04d" % (2000 + int(h01("hr", f[0]) * 900)), f[1], SYS_TIN[sysk], W.SYSTEMS[sysk],
                             SYS_TIN[sysk], "owned", "2012-01-01", "", "annual registration 2016"])
    rows.sort(key=lambda r: (r[6], r[0]))
    return (["register_id", "entity_name", "entity_tin", "related_entity_name", "related_entity_tin", "relationship",
             "effective_from", "effective_to", "source"], rows)


def reassignment_rows(people, assign):
    rows = []
    for npi, prac, s, e in assign:
        tin = O.tin_of(prac)
        src = "PECOS reassignment" if h01("src", npi, prac) < 0.7 else "carrier credentialing roster"
        rows.append([npi, tin, s.isoformat(), e.isoformat() if e else "", src])
    rows.sort(key=lambda r: (r[0], r[2]))
    return (["npi", "billing_tin", "effective_from", "effective_to", "record_source"], rows)


def provider_file_rows(people, assign):
    rows = []
    span = defaultdict(list)
    for npi, prac, s, e in assign:
        span[npi].append((prac, s, e))
    cars = sorted(W.CARRIERS)
    for npi in sorted(span):
        p = people[npi]
        for car in cars:
            if h01("inet", npi, car) < 0.15:
                continue
            for prac, s, e in span[npi]:
                if e is not None and e < D(2019, 1, 1):
                    continue
                last, first = p["last"], p["first"]
                v = h01("var", npi, car)
                if v < 0.18:
                    last = last.upper()
                    first = first.upper()
                elif v < 0.28:
                    first = first[0] + "."
                mi = chr(65 + int(h01("mi", npi) * 26)) if h01("hasmi", npi, car) < 0.6 else ""
                pname = O.PRACTICES[prac][0]
                if h01("pv", npi, car, prac) < 0.3:
                    pname = pname.upper().replace(" AND ", " & ")
                elif h01("pv2", npi, car, prac) < 0.2:
                    pname = pname + ", S.C." if "Group" not in pname else pname.replace("Group", "Grp")
                cred = p["cred"]
                if cred in ("MD", "DO") and h01("cr", npi, car) < 0.12:
                    cred = cred[0] + "." + cred[1] + "."
                eff = max(s, D(2016, 1, 1)) + timedelta(days=int(h01("lagc", npi, car, prac) * 40))
                rows.append([W.CARRIERS[car]["submitter"], npi, last, first, mi, cred, p["taxonomy"], pname,
                             O.BILLING_ZIP.get(prac, O.PRACTICES[prac][2][0]), O.tin_of(prac), "In network",
                             eff.isoformat(), e.isoformat() if e else ""])
    rows.sort(key=lambda r: (r[0], r[1], r[11]))
    return (["submitter_code", "provider_npi", "last_name", "first_name", "middle_initial", "credential",
             "primary_taxonomy", "practice_name", "practice_zip", "billing_tin", "network_status",
             "network_effective_date", "network_termination_date"], rows)


FAC_TYPE_NAME = {"HOPD": "Hospital outpatient department", "IDTF": "Independent diagnostic testing facility",
                 "ASC": "Ambulatory surgery center", "LAB": "Independent clinical laboratory"}


def facility_rows():
    rows = []
    for f in W.FACILITIES:
        key, name, sysk, ftype, z, ccn, svc = f
        dept_of = "Ledgestone Medical Center (CCN 520147)" if key == "LMN" else ""
        rows.append([FAC_NPI[key], ccn, name, W.SYSTEMS.get(sysk, "") if sysk else "Independent",
                     FAC_TYPE_NAME[ftype], W.ZIP_CITY[z], z, W.ZIP_COUNTY[z], dept_of])
    rows.sort(key=lambda r: r[2])
    return (["facility_npi", "ccn", "facility_name", "health_system", "facility_type", "city", "zip", "county",
             "department_of"], rows)


APC = {"70551": ("5523", "Q3"), "72148": ("5523", "Q3"), "73721": ("5523", "Q3"), "74177": ("5572", "Q3"),
       "71250": ("5522", "Q3"), "71046": ("5521", "Q1"), "73562": ("5521", "Q1"), "76700": ("5522", "Q3"),
       "77067": ("", "A"), "93306": ("5524", "S"), "45378": ("5312", "T"), "45380": ("5312", "T"),
       "43239": ("5302", "T"), "29881": ("5113", "J1")}


def medicare_rows():
    rows = []
    for cpt in sorted(S.MEDICARE):
        desc = W.CPT[cpt][0]
        if W.CPT[cpt][1] == "LAB":
            rows.append([cpt, desc, "CLFS", "", "A", money(S.MEDICARE[cpt])])
        else:
            apc, si = APC[cpt]
            rows.append([cpt, desc, "OPPS" if apc else "MPFS (mammography)", apc, si, money(S.MEDICARE[cpt])])
    return (["hcpcs", "short_descriptor", "payment_system", "apc", "status_indicator", "cy2025_amount_wi_cbsa24580"],
            rows)


# ------------------------------------------------------------------ Ledgestone's rate exhibit
LDG_CPTS = sorted({c for f in W.FACILITIES if f[2] == "LDG" for c in f[6]})
PROF_CODES = sorted(W.PROF)


def exhibit_c(path):
    wb = openpyxl.Workbook()
    hfont = Font(bold=True)
    fill = PatternFill("solid", fgColor="DDE5F0")
    ws = wb.active
    ws.title = "Outpatient facility"
    ws.append(["Ledgestone Health - outpatient facility rates in force from 1 January 2025 (all sites, one chargemaster)"])
    ws.append(["Cedarbrook, Norbridge, Lakefront and Heartland agreements: allowed amount per unit. Bayfield: see sheet Bayfield terms."])
    ws.append([])
    hdr = ["CPT/HCPCS", "Description", "Cedarbrook Health Plan", "Norbridge Health Insurance",
           "Lakefront Benefit Administrators", "Heartland Cooperative Health"]
    ws.append(hdr)
    for c in ws[4]:
        c.font = hfont
        c.fill = fill
    for cpt in LDG_CPTS:
        ws.append([cpt, W.CPT[cpt][0]] + [S.ldg_facility_rate(car, cpt, 2025) for car in ("C1", "C3", "C4", "C5")])
    for row in ws.iter_rows(min_row=5, min_col=3, max_col=6):
        for c in row:
            c.number_format = "#,##0.00"
    for i, wdt in enumerate([12, 46, 20, 24, 30, 26], start=1):
        ws.column_dimensions[get_column_letter(i)].width = wdt
    ws2 = wb.create_sheet("Bayfield terms")
    ws2.append(["Bayfield Mutual Health - Ledgestone Health hospital agreement, amendment 4, effective 1 January 2025"])
    ws2.append(["Outpatient services are paid at the percentage below of the Medicare amount for the service in the "
                "calendar year of service (OPPS for outpatient procedures and imaging, CLFS for laboratory), "
                "Wisconsin wage-adjusted, CBSA 24580."])
    ws2.append([])
    ws2.append(["Service category", "CPT/HCPCS in the category (Ledgestone services)", "Percent of Medicare"])
    for c in ws2[4]:
        c.font = hfont
        c.fill = fill
    cats = [("IMG", "Diagnostic imaging"), ("ECHO", "Echocardiography"), ("ENDO", "Gastrointestinal endoscopy"),
            ("ARTH", "Arthroscopy"), ("LAB", "Clinical laboratory")]
    for fam, label in cats:
        codes = [c for c in LDG_CPTS if W.CPT[c][1] == fam]
        ws2.append([label, ", ".join(codes), W.LDG_C2_PCT_2025[fam]])
        ws2.cell(row=ws2.max_row, column=3).number_format = "0%"
    ws2.column_dimensions["A"].width = 30
    ws2.column_dimensions["B"].width = 70
    ws2.column_dimensions["C"].width = 20
    ws3 = wb.create_sheet("Professional")
    ws3.append(["Ledgestone Medical Group - professional fee schedule by carrier, in force from 1 January 2025"])
    ws3.append(["Allowed amount per service. Procedure codes are the professional component where the service is "
                "performed in a facility."])
    ws3.append([])
    ws3.append(["CPT/HCPCS", "Modifier", "Description"] + [W.CARRIERS[c]["name"] for c in sorted(W.CARRIERS)])
    for c in ws3[4]:
        c.font = hfont
        c.fill = fill
    for code in PROF_CODES:
        cpt = code.split("-")[0]
        mod = "26" if code.endswith("-26") else ""
        ws3.append([cpt, mod, W.PROF[code][0]] + [S.ldg_prof_rate(car, code) for car in sorted(W.CARRIERS)])
    for row in ws3.iter_rows(min_row=5, min_col=4, max_col=8):
        for c in row:
            c.number_format = "#,##0.00"
    for i, wdt in enumerate([12, 9, 44, 20, 20, 24, 30, 26], start=1):
        ws3.column_dimensions[get_column_letter(i)].width = wdt
    for wsx in (ws, ws2, ws3):
        wsx["A1"].font = Font(bold=True, size=12)
        wsx.sheet_view.showGridLines = True
    wb.properties.creator = "Jacob Murillo"
    wb.properties.lastModifiedBy = "Jacob Murillo"
    wb.properties.title = "Exhibit C to notice N25-014"
    import datetime as _dt
    wb.properties.created = _dt.datetime(2025, 10, 6, 15, 12, 0)
    wb.properties.modified = _dt.datetime(2025, 10, 7, 9, 41, 0)
    wb.save(path)
    normalize_xlsx(path, "2025-10-07T09:41:00Z")


def normalize_xlsx(path, modified):
    """Repack the workbook reproducibly: fixed entry stamps (as Excel writes them) and a fixed
    last-saved time in the core properties."""
    import re
    import zipfile
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(path, "w") as z:
        for name, data in items:
            if name == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              lambda m: m.group(1) + modified.encode() + m.group(2), data)
            if name == "docProps/app.xml":
                data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", data)
                data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 0
            z.writestr(zi, data)


# ------------------------------------------------------------------ the neighbouring files
def hcris_rows():
    rows = []
    for f in W.FACILITIES:
        if f[2] is None or f[0] == "LMN":
            continue
        key = f[0]
        opch = 180e6 + 420e6 * h01("opch", key)
        ccr = 0.21 + 0.12 * h01("ccr", key)
        rows.append([f[5], f[1], "2023-12-31" if h01("fye", key) < 0.6 else "2023-06-30",
                     "%.0f" % opch, "%.0f" % (opch * ccr), "%.4f" % ccr,
                     "%d" % (4000 + int(h01("dis", key) * 16000)), "%d" % (60 + int(h01("beds", key) * 240))])
    return (["provider_ccn", "hospital_name", "fiscal_year_end", "outpatient_charges", "outpatient_costs",
             "outpatient_cost_to_charge_ratio", "total_discharges", "licensed_beds"], rows)


def ma_rows(mem, people, roster):
    """Medicare Advantage facility claims referred by the lakeshore groups' physicians in 2024."""
    rows = []
    num = Numberer()
    refs = []
    for p in ("BMG", "KPN", "RRF", "AFH", "KAC", "MDC", "SOA", "MFP"):
        refs += [(p, n) for n in roster[p]]
    for i in range(5200):
        p, npi = refs[int(h01("ma_ref", i) * len(refs))]
        spec = people[npi]["spec"]
        mix = S.REF_MIX[spec]
        cpts = sorted(mix)
        cpt = S.weighted_pick({c: mix[c] for c in cpts}, h01("ma_cpt", i))
        fam = W.CPT[cpt][1]
        opts = [f for f, s in S.OUTSIDE["lakeshore"][fam] if S.site_offers(f, cpt)] or ["KLH"]
        f = opts[int(h01("ma_f", i) * len(opts))]
        pid = sorted(MA_PRODUCTS)[int(h01("ma_p", i) * 3)]
        car = MA_PRODUCTS[pid][0]
        d = S.day_in(2024, 1 + int(h01("ma_m", i) * 12), h01("ma_d", i))
        allowed = round(S.MEDICARE.get(cpt, W.CPT[cpt][2] * 0.6) * (1.0 + 0.04 * h01("ma_a", i)), 2)
        liab = round(allowed * 0.11, 2)
        bill_npi, bill_tin = billing_of(f)
        mid = "WM" + ("%010X" % int(h01("ma_m_id", i // 3) * 16 ** 10))
        rows.append([W.CARRIERS[car]["submitter"], num.next(car, d, ("ma", i)), 1, "1", "",
                     "UB04" if W.FAC[f][2] else "CMS1500", mid, pid, d.isoformat(),
                     (d + timedelta(days=lag_days(car, ("ma", i)))).isoformat(), "0131" if W.FAC[f][2] else "",
                     "" if W.FAC[f][2] else INDEP_POS[W.FAC[f][3]],
                     REV_BY_CPT.get(cpt, FAMILY_REV[fam]) if W.FAC[f][2] else "", cpt, "", 1, money(allowed),
                     money(allowed - liab), money(liab), bill_npi, bill_tin, FAC_NPI[f], W.FAC[f][4], npi])
    rows.sort(key=lambda r: (r[9], r[1]))
    return FAC24_COLS, rows


# ------------------------------------------------------------------ everything
def write_all(wd, target):
    os.makedirs(target, exist_ok=True)
    mem, people, assign, roster, lines = wd["mem"], wd["people"], wd["assign"], wd["roster"], wd["lines"]
    fac_rows, prof_rows, ledger = build_claims(mem, people, lines)
    f24 = write_fac24(fac_rows, os.path.join(target, FILES["fac24"]))
    fh = write_fachist(fac_rows, os.path.join(target, FILES["fachist"]))
    p24 = write_prof24(prof_rows, os.path.join(target, FILES["prof24"]))
    used = {r["member"] for r in f24} | {r["member"] for r in fh} | {r["member"] for r in p24}
    er = elig_rows(mem, used)
    write_csv(os.path.join(target, FILES["elig"]), ELIG_COLS, er)
    cols, rows = product_reference()
    write_csv(os.path.join(target, FILES["prodref"]), cols, rows)
    with open(os.path.join(target, FILES["tiers"]), "w", encoding="utf-8") as fhd:
        json.dump(tier_filings(), fhd, indent=1)
        fhd.write("\n")
    cols, rows = register_rows()
    write_csv(os.path.join(target, FILES["register"]), cols, rows)
    cols, rows = reassignment_rows(people, assign)
    write_csv(os.path.join(target, FILES["reassign"]), cols, rows)
    cols, rows = provider_file_rows(people, assign)
    write_csv(os.path.join(target, FILES["provfile"]), cols, rows)
    cols, rows = facility_rows()
    write_csv(os.path.join(target, FILES["facdir"]), cols, rows)
    cols, rows = medicare_rows()
    write_csv(os.path.join(target, FILES["medicare"]), cols, rows)
    exhibit_c(os.path.join(target, FILES["exhibit"]))
    cols, rows = hcris_rows()
    write_csv(os.path.join(target, FILES["hcris"]), cols, rows)
    cols, rows = ma_rows(mem, people, roster)
    write_csv(os.path.join(target, FILES["ma"]), cols, rows)
    return {"fac_rows": fac_rows, "prof_rows": prof_rows, "ledger": ledger, "f24": f24, "fh": fh, "p24": p24,
            "elig": er}
