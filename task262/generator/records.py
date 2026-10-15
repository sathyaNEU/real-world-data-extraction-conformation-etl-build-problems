"""Writers for the pack's records: the data centre's census-linked extract (the cohort, the children's earnings by
year, the parents' income history for the families that filed in every year, the region recode, the price index)
and the foundation's Bridges records (the case-management export, the program ledger, the office list)."""
from __future__ import annotations

import csv

import numpy as np

import bridges as BR
import common as K


def _writer(path):
    fh = open(path, "w", newline="", encoding="utf-8")
    return fh, csv.writer(fh, lineterminator="\n")


def identify(regions):
    """Child and family numbers as the data centre assigns them (scrambled, fixed per build)."""
    r = K.rng("ids")
    nfam = sum(R["nfam"] for R in regions)
    nch = sum(len(R["fam_of"]) for R in regions)
    fam_ids = r.choice(np.arange(1000000, 9999999), nfam, replace=False)
    ch_ids = r.choice(np.arange(10000000, 99999999), nch, replace=False)
    fo = co = 0
    for R in regions:
        R["fam_id"] = ["H%07d" % v for v in fam_ids[fo:fo + R["nfam"]]]
        R["child_id"] = ["K%08d" % v for v in ch_ids[co:co + len(R["fam_of"])]]
        fo += R["nfam"]
        co += len(R["fam_of"])
    return regions


def census_income(R):
    """Parents' total income in 2000 as the census recorded it, in 2000 dollars: the family's long-run level, the
    year's swing, a few families at or below zero (self-employment losses)."""
    r = K.rng("census-income", R["code"])
    v = np.exp(R["xp"] + R["u_census"]) * K.CPI[K.CENSUS_YEAR] / 100.0
    v = np.round(v).astype(np.int64)
    low = r.random(R["nfam"]) < 0.004
    v = np.where(low, -np.round(r.uniform(0, 9000, R["nfam"])).astype(np.int64), v)
    R["census_income"] = v
    return v


def write_cohort(path, regions):
    rows = []
    for R in regions:
        inc = census_income(R)
        for i, f in enumerate(R["fam_of"]):
            rows.append((R["child_id"][i], R["fam_id"][f], int(R["birth"][i]), R["sex"][i], R["code"],
                         int(R["parents"][f]), int(inc[f])))
    rows.sort()
    fh, w = _writer(path)
    w.writerow(["child_id", "family_id", "birth_year", "sex", "census_region_2001", "parents_in_household",
                "parents_total_income_2000"])
    w.writerows(rows)
    fh.close()
    return len(rows)


def write_earnings(path, regions):
    rows = []
    for R in regions:
        for i in range(len(R["fam_of"])):
            for j, y in enumerate(K.EARN_YEARS):
                nominal = R["real"][i, j] * K.CPI[y] / 100.0
                rows.append((R["child_id"][i], y, int(round(nominal))))
    rows.sort()
    fh, w = _writer(path)
    w.writerow(["child_id", "tax_year", "earnings"])
    w.writerows(rows)
    fh.close()
    return len(rows)


def write_history(path, regions):
    rows = []
    for R in regions:
        for f in np.flatnonzero(R["files"]):
            for t, y in enumerate(K.TAX_YEARS):
                rows.append((R["fam_id"][f], y, int(round(np.exp(R["xp"][f] + R["u_tax"][f, t])))))
    rows.sort()
    fh, w = _writer(path)
    w.writerow(["family_id", "tax_year", "family_total_income_2005_dollars"])
    w.writerows(rows)
    fh.close()
    return len(rows)


def write_recode(path):
    fh, w = _writer(path)
    w.writerow(["census_region_2001", "region_2021", "change"])
    notes = {"4710": "boundary unchanged", "4720": "boundary unchanged", "4730": "renamed from Kestry-Inlet",
             "4740": "renamed from Selvane-Mills", "4750": "boundary unchanged", "4760": "boundary unchanged",
             "4770": "renamed from Ostler-Prairie", "4780": "boundary unchanged"}
    for code, name in zip(K.CODES, K.NAMES):
        w.writerow([code, name, notes[code]])
    fh.close()
    return len(K.CODES)


def write_cpi(path):
    fh, w = _writer(path)
    w.writerow(["year", "cpi_2005_100"])
    for y in sorted(K.CPI):
        w.writerow([y, "%.1f" % K.CPI[y]])
    fh.close()
    return len(K.CPI)


# ---------------------------------------------------------------------------------------------- Bridges
def write_participants(path, rows):
    fh, w = _writer(path)
    w.writerow(["participant_ref", "source_system", "office", "intake_date", "date_of_birth", "referral_source", "status",
                "exit_date", "transfer_from"])
    for x in sorted(rows, key=lambda x: (x["system"], x["ref"])):
        w.writerow([x["ref"], x["system"], x["office"], x["intake"].isoformat(), x["dob"].isoformat(), x["referral"],
                    x["status"], x["exit"].isoformat() if x["exit"] else "", x["transfer_from"]])
    fh.close()
    return len(rows)


def write_ledger(path, lines):
    fh, w = _writer(path)
    w.writerow(["posting_date", "cost_centre", "account", "amount", "journal", "description"])
    for d, cc, acct, amt, jn, desc in lines:
        w.writerow([d.isoformat(), cc, acct, "%.2f" % amt, jn, desc])
    fh.close()
    return len(lines)


def write_offices(path):
    fh, w = _writer(path)
    w.writerow(["office", "town", "region", "cost_centre"])
    for code, region, town in BR.OFFICES:
        w.writerow([code, town, region, code])
    w.writerow(["CEN", "Torvale (head office)", "", "CEN"])
    fh.close()
    return len(BR.OFFICES) + 1
