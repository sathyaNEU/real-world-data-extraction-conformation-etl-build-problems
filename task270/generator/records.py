"""The pack's record files: the dispensing extract, the two practice systems' year-end lists, the pseudonym
crosswalk, the practice-to-network list and the statin product list."""
from __future__ import annotations

import datetime as dt
import os

import openpyxl
from openpyxl.styles import Font

from common import (EXTRACT_START, NETWORK_MOVE, NETWORK_NAME, REKEY, TARGET, YEAR_END, rng, write_csv)
from world import BRAND, PRODUCTS

F_DISP = "community_pharmacy_statin_dispensing_2025-12-01_to_2026-12-31.csv"
FIRST_ITEM = 4826113000                  # the data service's item number on the extract's first row
F_QUARVIS = "quarvis_practices_lipid_cohort_2026-12-31.csv"
F_SYNARIS = "synaris_practices_lipid_cohort_2026-12-31.xlsx"
F_XWALK = "pseudonym_crosswalk_2026-07-01.csv"
F_PRACTICES = "practice_network_membership_2026.csv"
F_PRODUCTS = "statin_products_dmd_2026-12.csv"


def dispensing(pts):
    rows = []
    for pt in pts:
        for d, ods, prod, qty, ptype in pt["items"]:
            if d < EXTRACT_START or d > YEAR_END:
                continue
            key = pt["old_key"] if d < REKEY else pt["new_key"]
            rows.append((d, ods, key, pt, prod, qty, ptype))
    rows.sort(key=lambda x: (x[0], x[1], x[2], x[4]))
    out = []
    for i, (d, ods, key, pt, prod, qty, ptype) in enumerate(rows):
        out.append(dict(dispense_id=str(FIRST_ITEM + i), dispensed_date=d.isoformat(), dispenser_ods=ods,
                        patient_pseudonym=key, prescriber_practice=pt["practice"], product_description=prod,
                        quantity=qty, quantity_unit="tablet", dosage_instructions=dosage(pt),
                        prescription_type=ptype))
    return out


ONE = ["ONE TABLET AT NIGHT", "One tablet at night", "ONE TO BE TAKEN EACH DAY", "TAKE ONE TABLET DAILY", "1 OD",
       "ONE AT NIGHT", "TAKE ONE ONCE A DAY", "ONE TABLET ONCE DAILY AT NIGHT", "1 TABLET AT NIGHT", "TAKE ONE AT NIGHT",
       "Take ONE tablet at night", "1 ON", "ONE DAILY", "TAKE 1 AT NIGHT", "ONE TO BE TAKEN AT NIGHT", "1 NOCTE",
       "take one each evening", "ONE TABLET TO BE TAKEN EACH EVENING", "1 at night", "ONE TABLET DAILY AT BEDTIME"]
TWO = ["TWO TABLETS AT NIGHT", "TAKE TWO DAILY", "2 AT NIGHT", "TWO TO BE TAKEN AT NIGHT", "Take TWO tablets at night",
       "2 ON", "TAKE 2 AT NIGHT", "two tablets each evening"]
DIRECTED = ["AS DIRECTED", "As directed", "USE AS DIRECTED"]


def dosage(pt):
    """The dosage as the patient's prescriber typed it: the same text on every item of the patient's prescription."""
    r = rng("dosage", pt["pid"])
    pool = DIRECTED if pt["dose_text"] == "AS DIRECTED" else (TWO if pt["tpd"] == 2 else ONE)
    return pool[int(r.integers(0, len(pool)))]


def quarvis(pts):
    out = []
    for pt in pts:
        if pt["system"] != "Q" or pt["left"]:
            continue
        out.append(dict(nhs_pseudo=pt["new_key"], practice_ods=pt["practice"], yob=pt["yob"], sex=pt["sex"],
                        care_home_since=pt["care_home_date"].strftime("%d/%m/%Y") if pt["care_home_date"] else "",
                        mds_since=pt["aid_code_date"].strftime("%d/%m/%Y") if pt["coded_aid"] else ""))
    out.sort(key=lambda x: (x["practice_ods"], x["nhs_pseudo"]))
    return out


def synaris(pts, path):
    r = rng("synaris residence")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Lipid cohort"
    head = ["Patient Ref", "Registered Practice", "Year of Birth", "Gender", "Residence", "Residence Recorded"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
    rows = []
    for pt in pts:
        if pt["system"] != "T" or pt["left"]:
            continue
        if pt["kind"] == "ch":
            res = "Care home (nursing)" if r.random() < 0.45 else "Care home (residential)"
            rec = pt["care_home_date"]
        else:
            u = r.random()
            res = "Own home" if u < 0.86 else ("Sheltered housing" if u < 0.94 else "Not recorded")
            rec = None if res == "Not recorded" else dt.date(int(r.integers(2012, 2026)), int(r.integers(1, 13)), 1)
        rows.append([pt["new_key"], pt["practice"], pt["yob"], "Female" if pt["sex"] == "F" else "Male", res, rec])
    rows.sort(key=lambda x: (x[1], x[0]))
    for row in rows:
        ws.append(row)
    for row in ws.iter_rows(min_row=2, min_col=6, max_col=6):
        for c in row:
            c.number_format = "dd/mm/yyyy"
    for col, w in zip("ABCDEF", (16, 20, 14, 10, 24, 18)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    wb.save(path)
    return len(rows)


def crosswalk(pts):
    out = [dict(old_pseudonym=pt["old_key"], new_pseudonym=pt["new_key"]) for pt in pts if pt["in_crosswalk"]]
    out.sort(key=lambda x: x["old_pseudonym"])
    return out


def practice_list(pracs):
    """The two practices that moved network on 1 April 2026 carry a row for each network; every other one row."""
    out = []
    for p in pracs:
        before = p["network_before"]
        if before != p["network"]:
            out.append(dict(practice_ods=p["code"], practice_name=p["name"], clinical_system=_sys(p),
                            network=NETWORK_NAME[before] + " PCN", member_from="2019-07-01",
                            member_to=(NETWORK_MOVE - dt.timedelta(days=1)).isoformat()))
            out.append(dict(practice_ods=p["code"], practice_name=p["name"], clinical_system=_sys(p),
                            network=NETWORK_NAME[p["network"]] + " PCN", member_from=NETWORK_MOVE.isoformat(),
                            member_to=""))
        else:
            out.append(dict(practice_ods=p["code"], practice_name=p["name"], clinical_system=_sys(p),
                            network=NETWORK_NAME[p["network"]] + " PCN", member_from="2019-07-01", member_to=""))
    out.sort(key=lambda x: (x["network"], x["practice_ods"], x["member_from"]))
    return out


def _sys(p):
    return "Quarvis" if p["system"] == "Q" else "Synaris"


def products():
    out = []
    pack = {"Fluvastatin 80mg modified-release tablets": 28}
    for name, ing, mg, _w in PRODUCTS:
        out.append(dict(product_description=name, vmp=name, ingredient=ing, strength_mg=mg,
                        form="modified-release tablet" if "modified" in name else "tablet", brand="N",
                        pack_size=pack.get(name, 28)))
    for gen, br in BRAND.items():
        ing = gen.split()[0].lower()
        mg = int(gen.split()[1].replace("mg", ""))
        out.append(dict(product_description=br, vmp=gen, ingredient=ing, strength_mg=mg, form="tablet", brand="Y",
                        pack_size=28))
    out.sort(key=lambda x: (x["ingredient"], x["strength_mg"], x["brand"]))
    return out


def write_all(pracs, pharms, pts):
    os.makedirs(TARGET, exist_ok=True)
    n = {}
    D = dispensing(pts)
    n[F_DISP] = write_csv(os.path.join(TARGET, F_DISP), list(D[0].keys()), D)
    Q = quarvis(pts)
    n[F_QUARVIS] = write_csv(os.path.join(TARGET, F_QUARVIS), list(Q[0].keys()), Q)
    n[F_SYNARIS] = synaris(pts, os.path.join(TARGET, F_SYNARIS))
    X = crosswalk(pts)
    n[F_XWALK] = write_csv(os.path.join(TARGET, F_XWALK), ["old_pseudonym", "new_pseudonym"], X)
    P = practice_list(pracs)
    n[F_PRACTICES] = write_csv(os.path.join(TARGET, F_PRACTICES), list(P[0].keys()), P)
    PR = products()
    n[F_PRODUCTS] = write_csv(os.path.join(TARGET, F_PRODUCTS), list(PR[0].keys()), PR)
    return n
