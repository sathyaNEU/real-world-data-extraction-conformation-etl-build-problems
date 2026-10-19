"""Loaders that read the shipped pack (never the world): policy years with their mid-term adjustments, the region
map, the claims of both systems in pounds and UK dates, the glass partner's job lines and the salvage statements.
Exposure is cut into pieces of constant district and cover, split at the region map's change dates."""
import csv
import datetime as dt
import os

import openpyxl

import common as K

BST = {2022: (dt.date(2022, 3, 27), dt.date(2022, 10, 30)), 2023: (dt.date(2023, 3, 26), dt.date(2023, 10, 29)),
       2024: (dt.date(2024, 3, 31), dt.date(2024, 10, 27)), 2025: (dt.date(2025, 3, 30), dt.date(2025, 10, 26)),
       2026: (dt.date(2026, 3, 29), dt.date(2026, 10, 25))}
COVER = {"COMP": "COMP", "TPFT": "TPFT", "Comprehensive": "COMP", "Third party, fire and theft": "TPFT"}
TYPE = {"ACC": "ACC", "WSC": "WSC", "THF": "THF", "FIR": "FIR", "Accident": "ACC", "Windscreen": "WSC", "Theft": "THF",
        "Fire": "FIR"}
LIAB = {"F": "F", "S": "S", "N": "N", "P": "P", "": "", "At fault": "F", "Split": "S", "Not at fault": "N",
        "Pending": "P"}


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def dmy(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date() if s else None


def iso(s):
    return dt.date.fromisoformat(s) if s else None


def local_date(stamp):
    t = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
    a, b = BST[t.year]
    lt = t + dt.timedelta(hours=1)
    return lt.date() if a <= lt.date() < b else t.date()


def district_of(postcode):
    return postcode.split(" ")[0] if postcode else postcode


class RegionMap:
    def __init__(self, path):
        self.by = {}
        for r in rows(path):
            self.by.setdefault(r["postcode_district"], []).append(
                (iso(r["effective_from"]), iso(r["effective_to"]) or dt.date(2099, 12, 31), r["rating_region_code"]))
        self.changes = sorted({iso(r["effective_from"]) for r in rows(path)} - {dt.date(2019, 1, 1)})

    def region(self, district, day):
        for a, b, code in self.by[district]:
            if a <= day <= b:
                return code
        raise KeyError((district, day))


def load(target):
    F = {k: os.path.join(target, v) for k, v in K.FILES.items()}
    rmap = RegionMap(F["regions"])
    terms = []
    for r in rows(F["pol_legacy"]):
        end = expiry = dmy(r["EXPIRY_DATE"]) + dt.timedelta(days=1)
        if r["CANCELLATION_DATE"]:
            end = min(end, dmy(r["CANCELLATION_DATE"]) + dt.timedelta(days=1))
        terms.append(dict(sys="L", ref=r["POLICY_NO"], seq=int(r["TERM_NO"]), start=dmy(r["INCEPTION_DATE"]), end=end,
                          expiry=expiry,
                          district=r["GARAGING_DISTRICT"], step=int(r["NCD_STEP"]), prot=r["STEP_PROTECTION"] == "Y",
                          cover=COVER[r["COVER"]], reg=r["VEHICLE_REG"], mtas=[]))
    for r in rows(F["pol_platform"]):
        end = expiry = iso(r["term_end"])
        if r["cancellation_date"]:
            end = min(end, iso(r["cancellation_date"]))
        terms.append(dict(sys="P", ref=r["policy_number"], seq=int(r["term_number"]), start=iso(r["term_start"]),
                          end=end, expiry=expiry, district=district_of(r["garaging_postcode"]), step=int(r["ncd_step"]),
                          prot=r["step_protection"] == "true", cover=COVER[r["cover_type"]],
                          reg=r["vehicle_registration"], mtas=[]))
    key = {(t["ref"], t["seq"]): t for t in terms}
    for r in rows(F["mta"]):
        t = key[(r["policy_number"], int(r["term_number"]))]
        t["mtas"].append(dict(day=iso(r["effective_date"]), kind=r["adjustment_type"],
                              district=district_of(r["new_garaging"]) if r["new_garaging"] else None,
                              cover=COVER[r["new_cover"]] if r["new_cover"] else None,
                              reg=r["new_vehicle_reg"] or None))
    for t in terms:
        t["mtas"].sort(key=lambda m: m["day"])
    by_ref = {}
    for t in terms:
        by_ref.setdefault(t["ref"], []).append(t)
    for v in by_ref.values():
        v.sort(key=lambda t: t["start"])
    xw = {}
    for r in rows(F["crosswalk"]):
        xw[r["platform_policy_number"]] = r["legacy_policy_no"]
        xw[r["legacy_policy_no"]] = r["platform_policy_number"]
    claims = []
    for r in rows(F["clm_legacy"]):
        claims.append(dict(sys="L", no=r["CLAIM_NO"], ref=r["POLICY_NO"], loss=dmy(r["LOSS_DATE"]),
                           notified=dmy(r["NOTIFIED_DATE"]), type=TYPE[r["CLAIM_TYPE"]], section=r["SECTION"],
                           liab=LIAB[r["FAULT"]], status=r["STATUS"], paid=int(r["PAID_AMT"]) / 100.0,
                           os=int(r["OS_AMT"]) / 100.0, rec=int(r["RECOV_AMT"]) / 100.0,
                           police=r["POLICE_REF"].replace("/", ""), supplier=r["SUPPLIER"], sref=r["SUPPLIER_REF"]))
    for r in rows(F["clm_platform"]):
        claims.append(dict(sys="P", no=r["claim_number"], ref=r["policy_number"], loss=iso(r["loss_date"]),
                           notified=local_date(r["notified_at"]), type=TYPE[r["claim_type"]], section=r["section"],
                           liab=LIAB[r["liability"]], status=r["status"], paid=float(r["paid_gbp"]),
                           os=float(r["outstanding_gbp"]), rec=float(r["recovered_gbp"]),
                           police=r["police_reference"], supplier=r["supplier"], sref=r["supplier_reference"]))
    for c in claims:
        c["incurred"] = round(c["paid"] + c["os"], 2)
    glass = []
    for r in rows(F["glass"]):
        glass.append(dict(job=r["job_ref"], line=int(r["line_no"]),
                          booked=dt.datetime.strptime(r["booked"], "%d/%m/%Y %H:%M").date(),
                          fitted=dmy(r["fitted_date"]), ref=r["insurer_policy_ref"], reg=r["vehicle_reg"],
                          where=r["fitting_postcode_district"], desc=r["description"], billed=r["billed_to"],
                          net=float(r["net_amount"]), vat=float(r["vat_amount"])))
    salvage = []
    wb = openpyxl.load_workbook(F["salvage"], read_only=True)
    for ws in wb.worksheets:
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0 or row[0] is None:
                continue
            salvage.append(dict(lot=row[0], sold=row[1].date() if hasattr(row[1], "date") else row[1], claim=row[2],
                                reg=row[3], cat=row[4], hammer=float(row[5]), fees=float(row[6]), net=float(row[7])))
    return dict(rmap=rmap, terms=terms, by_ref=by_ref, xw=xw, claims=claims, glass=glass, salvage=salvage)


def term_for(P, ref, day):
    """The policy year covering a day under the number a record carries, through the crosswalk when the record
    carries the other system's number."""
    for r in (ref, P["xw"].get(ref)):
        for t in P["by_ref"].get(r, []):
            if t["start"] <= day < t["end"]:
                return t
    return None


def state_on(t, day):
    d, c = t["district"], t["cover"]
    for m in t["mtas"]:
        if m["day"] > day:
            break
        if m["district"]:
            d = m["district"]
        if m["cover"]:
            c = m["cover"]
    return d, c


def pieces(P, t):
    """(start, end, district, cover) pieces of a policy year, cut at adjustments and at the region map's changes."""
    cuts = sorted({t["start"], t["end"]} | {m["day"] for m in t["mtas"] if t["start"] < m["day"] < t["end"]}
                  | {d for d in P["rmap"].changes if t["start"] < d < t["end"]})
    out = []
    for a, b in zip(cuts, cuts[1:]):
        d, c = state_on(t, a)
        out.append((a, b, d, c))
    return out


def exposure(P, years, by=("region",), cover=None):
    """Vehicle-years (days over 365) within the given calendar years, keyed by region and optionally step and
    protection."""
    E = {}
    lo, hi = dt.date(min(years), 1, 1), dt.date(max(years) + 1, 1, 1)
    for t in P["terms"]:
        if t["end"] <= lo or t["start"] >= hi:
            continue
        for a, b, d, c in pieces(P, t):
            if cover and c != cover:
                continue
            a2, b2 = max(a, lo), min(b, hi)
            if b2 <= a2:
                continue
            reg = P["rmap"].region(d, a2)
            k = tuple(reg if f == "region" else t["step"] if f == "step" else t["prot"] for f in by)
            E[k] = E.get(k, 0.0) + (b2 - a2).days / 365.0
    return E
