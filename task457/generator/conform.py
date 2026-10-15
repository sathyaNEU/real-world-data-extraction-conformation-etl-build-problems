"""The conformed data the docket stands on, read from the bundle alone: the register's remuneration and the
disclosures, each tied to a faculty member and an Open Payments manufacturer, by year.

Every reading is a switch, so the checks can run the golden method with any one convention mishandled:
    attribution   "profile" (the covered-recipient profile's NPI; a profile without one through the NPI-bearing profile
                  with the same name and address), "profile_npi" (profiles carrying an NPI only), "profile_name" (a
                  profile without an NPI through the same name alone), "matcher" (the office's column), "npi" (records
                  carrying an NPI only)
    personal      drop payments made to a third party (True) or keep them
    natures       "remun" (the policy's five) or "all"
    version       "latest" submitted version of each disclosure, "first", or "sum" of every version
    typed         "resolve" typed names and listed companies with no identifier through the register's names (present
                  and former), "present" (the list's present names only), "list" (list ids only)
    vintage       "jan" (the refresh) or "jun" (the June 2026 publication for 2025)
"""
import csv
import datetime as dt
import os
from collections import defaultdict

REMUN = [
    "Consulting Fee",
    "Compensation for services other than consulting, including serving as faculty or as a speaker at a venue other "
    "than a continuing education program",
    "Honoraria",
    "Compensation for serving as faculty or as a speaker for an accredited or certified continuing education program",
    "Compensation for serving as faculty or as a speaker for an unaccredited and non-certified continuing education "
    "program",
]
REMUN_TYPES = {"Consulting", "Speaking", "Advisory board", "Honoraria", "Other paid services",
               "Consulting or advisory board", "Speaking or teaching", "Expert testimony"}
FILES = {
    "register": "open_payments_general_2021-2025_jan2027_extract.csv",
    "register_june": "open_payments_general_py2025_jun2026_extract.csv",
    "profiles": "open_payments_covered_recipient_profiles.csv",
    "roster": "clinical_faculty_appointments.csv",
    "depts": "department_codes.csv",
    "entities": "coi_entity_list.csv",
    "export": "coi_disclosures_2021-2026_export.xlsx",
    "history": "coi_submission_history.csv",
}
_CACHE = {}


def _csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load(target):
    if target in _CACHE:
        return _CACHE[target]
    p = lambda k: os.path.join(target, FILES[k])
    from openpyxl import load_workbook
    wb = load_workbook(p("export"), read_only=True)

    def sheet(name):
        rows = list(wb[name].iter_rows(values_only=True))
        return [dict(zip(rows[0], row)) for row in rows[1:]]
    disc, items = sheet("Disclosures"), sheet("Items")
    data = {"register": _csv(p("register")), "june": _csv(p("register_june")), "profiles": _csv(p("profiles")),
            "roster": _csv(p("roster")), "depts": _csv(p("depts")), "entities": _csv(p("entities")),
            "disc": disc, "items": items, "history": _csv(p("history"))}
    _CACHE[target] = data
    return data


def faculty(data):
    """emp_id -> {npi, name, terms[(start, end, dept, division, primary)]}"""
    if "faculty" in data:
        return data["faculty"]
    out = {}
    for r in data["roster"]:
        f = out.setdefault(r["emp_id"], {"npi": r["npi"], "first": r["first_name"], "last": r["last_name"], "terms": []})
        f["terms"].append((dt.date.fromisoformat(r["term_start"]), dt.date.fromisoformat(r["term_end"]),
                           r["dept_code"], r["division_code"], r["appointment_type"] == "Primary"))
    data["faculty"] = out
    return out


def holds(f, day):
    return any(s <= day <= e for s, e, _, _, _ in f["terms"])


def dept_on(data, f, day):
    """The department of the primary appointment on the day, a retired code read through its successor."""
    succ = {r["formed_from"]: r["dept_code"] for r in data["depts"] if r["formed_from"]}
    for s, e, code, div, prim in f["terms"]:
        if prim and s <= day <= e:
            if code == "MED":
                return succ["MED/%s" % div]
            return code
    return None


def attribute(data, how="profile"):
    """Record_ID -> emp_id under the attribution reading."""
    key = ("attribute", how)
    if key in data:
        return data[key]
    fac = faculty(data)
    by_npi = {}
    for e, f in sorted(fac.items()):
        by_npi.setdefault(f["npi"], e)          # a faculty member whose number changed: the number their records began under
    prof = {r["Covered_Recipient_Profile_ID"]: r["Covered_Recipient_NPI"] for r in data["profiles"]}
    prof_raw = {r["Covered_Recipient_Profile_ID"]: r for r in data["profiles"]}
    if how in ("profile", "profile_name"):
        # a profile without an NPI belongs to the physician whose NPI-bearing profile has the same name and address
        # ("profile_name": the same name, whatever the address)
        pkey = lambda r: (r["Covered_Recipient_Profile_First_Name"].strip().lower(),
                          r["Covered_Recipient_Profile_Last_Name"].strip().lower()) + (() if how == "profile_name" else (
                          r["Covered_Recipient_Profile_Address_Line_1"].strip().lower(),
                          r["Covered_Recipient_Profile_Zipcode"].strip()))
        with_npi = {}
        for r in data["profiles"]:
            if r["Covered_Recipient_NPI"]:
                with_npi.setdefault(pkey(r), set()).add(r["Covered_Recipient_NPI"])
        for r in data["profiles"]:
            if not r["Covered_Recipient_NPI"]:
                hit = with_npi.get(pkey(r), set())
                if len(hit) == 1:
                    prof[r["Covered_Recipient_Profile_ID"]] = next(iter(hit))
    out = {}
    for r in data["register"]:
        if how == "matcher":
            e = r["ORICOI_Matched_Emp_ID"]
        elif how == "profile_npi":
            e = by_npi.get(prof_raw.get(r["Covered_Recipient_Profile_ID"], {}).get("Covered_Recipient_NPI", ""))
        elif how == "npi":
            e = by_npi.get(r["Covered_Recipient_NPI"]) if r["Covered_Recipient_NPI"] else None
        else:
            e = by_npi.get(prof.get(r["Covered_Recipient_Profile_ID"], ""))
        if e:
            out[r["Record_ID"]] = e
    data[key] = out
    return out


def published(data, attribution="profile", personal=True, natures="remun", vintage="jan", years=None):
    """(emp_id, manufacturer id, year) -> remuneration the register published."""
    att = attribute(data, attribution)
    rows = data["register"]
    if vintage == "jun":
        june = {r["Record_ID"]: r for r in data["june"]}
        att_j = dict(att)
        prof = {r["Covered_Recipient_Profile_ID"]: r["Covered_Recipient_NPI"] for r in data["profiles"]}
        by_npi = {f["npi"]: e for e, f in faculty(data).items()}
        for rid, r in june.items():
            if rid not in att_j:
                e = by_npi.get(prof.get(r["Covered_Recipient_Profile_ID"], ""))
                if e:
                    att_j[rid] = e
        rows = [r for r in rows if r["Program_Year"] != "2025"] + list(june.values())
        att = att_j
    out = defaultdict(float)
    for r in rows:
        e = att.get(r["Record_ID"])
        if not e:
            continue
        if natures == "remun" and r["Nature_of_Payment_or_Transfer_of_Value"] not in REMUN:
            continue
        if personal and r["Third_Party_Payment_Recipient_Indicator"] not in ("No Third Party Payment", ""):
            continue
        y = int(r["Program_Year"])
        if years and y not in years:
            continue
        out[(e, r["Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID"], y)] += float(r["Total_Amount_of_Payment_USDollars"])
    return dict(out)


def payments(data, attribution="profile", personal=True, natures="remun"):
    """(emp_id, manufacturer id, year) -> [(date of payment, amount)] of the register's remuneration records."""
    key = ("payments", attribution, personal, natures)
    if key in data:
        return data[key]
    att = attribute(data, attribution)
    out = defaultdict(list)
    for r in data["register"]:
        e = att.get(r["Record_ID"])
        if not e:
            continue
        if natures == "remun" and r["Nature_of_Payment_or_Transfer_of_Value"] not in REMUN:
            continue
        if personal and r["Third_Party_Payment_Recipient_Indicator"] not in ("No Third Party Payment", ""):
            continue
        day = dt.datetime.strptime(r["Date_of_Payment"], "%m/%d/%Y").date()
        out[(e, r["Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID"], int(r["Program_Year"]))].append(
            (day, float(r["Total_Amount_of_Payment_USDollars"])))
    data[key] = dict(out)
    return data[key]


def in_force_day(data, version="latest"):
    """(emp_id, year) -> the Eastern date the disclosure's version in force (or its first version) was submitted."""
    key = ("in_force_day", version)
    if key in data:
        return data[key]
    out = {}
    if version == "latest":
        for d in data["disc"]:
            v = d["last_submitted_utc"]
            t = v if isinstance(v, dt.datetime) else dt.datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            out[(d["emp_id"], int(d["disclosure_year"]))] = (t - dt.timedelta(hours=5)).date()
    else:
        did = {d["disclosure_id"]: (d["emp_id"], int(d["disclosure_year"])) for d in data["disc"]}
        for ev in data["history"]:
            if ev["event"] == "Submitted" and ev["disclosure_id"] in did:
                t = dt.datetime.strptime(ev["event_time_utc"], "%Y-%m-%dT%H:%M:%SZ")
                out[did[ev["disclosure_id"]]] = (t - dt.timedelta(hours=5)).date()
    data[key] = out
    return out


def name_to_op(data):
    """Present names from the entity list, former names from the register's earlier years, each to its ID."""
    m = {}
    for r in data["register"]:
        m.setdefault(r["Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name"].strip().lower(),
                     r["Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID"])
    for e in data["entities"]:
        if e["open_payments_id"]:
            m[e["entity_name"].strip().lower()] = e["open_payments_id"]
    return m


def entity_names(data):
    """entity_id -> every name the list has shown for it: its present name and the names on earlier items."""
    if "entity_names" in data:
        return data["entity_names"]
    out = defaultdict(set)
    for e in data["entities"]:
        out[e["entity_id"]].add(e["entity_name"].strip().lower())
    for it in data["items"]:
        if it["entity_id"]:
            out[it["entity_id"]].add(it["entity_name"].strip().lower())
    data["entity_names"] = dict(out)
    return data["entity_names"]


def listed_op(data, entity_id, listed="resolve"):
    """A listed company's Open Payments ID: the list's own, else (resolve) any name the list has shown for it that the
    register carries, else (present) its present name in the register, else (list) none."""
    ent = data.setdefault("_ent", {e["entity_id"]: e for e in data["entities"]})[entity_id]
    if ent["open_payments_id"] or listed == "list":
        return ent["open_payments_id"]
    n2op = name_to_op(data)
    if listed == "present":
        return n2op.get(ent["entity_name"].strip().lower(), "")
    for nm in sorted(entity_names(data).get(entity_id, ())):
        if nm in n2op:
            return n2op[nm]
    return ""


def disclosed(data, version="latest", typed="resolve", reporting_only=True, listed="resolve"):
    """(emp_id, manufacturer id or company name, year) -> remuneration disclosed. Keys for companies outside Open
    Payments are ('', name) pairs folded into the second element as 'NR:<name>'."""
    ent = {e["entity_id"]: e for e in data["entities"]}
    present = {e["entity_name"].strip().lower(): e["open_payments_id"] for e in data["entities"] if e["open_payments_id"]}
    n2op = name_to_op(data) if typed == "resolve" else (present if typed == "present" else {})
    cur = {d["disclosure_id"]: d for d in data["disc"]}
    first = {}
    for it in data["items"]:
        first.setdefault(it["disclosure_id"], it["version"])
        first[it["disclosure_id"]] = min(first[it["disclosure_id"]], it["version"])
    out = defaultdict(float)
    for it in data["items"]:
        d = cur[it["disclosure_id"]]
        if version == "latest" and it["version"] != d["current_version"]:
            continue
        if version == "first" and it["version"] != first[it["disclosure_id"]]:
            continue
        if it["relationship_type"] not in REMUN_TYPES:
            continue
        if it["entity_id"]:
            op = listed_op(data, it["entity_id"], listed if typed == "resolve" else "list")
        else:
            nm = it["entity_name"].strip().lower()
            op = n2op.get(nm)
        key = op if op else "NR:" + it["entity_name"].strip()
        if reporting_only and not op:
            continue
        out[(d["emp_id"], key, int(d["disclosure_year"]))] += float(it["amount_usd"] or 0)
    return dict(out)


def owed_filed(data, year=2026):
    """Faculty who owed the year's disclosure (an appointment on 31 December) and the first submission time of each
    faculty member's disclosure for the year (UTC)."""
    fac = faculty(data)
    owed = {e for e, f in fac.items() if holds(f, dt.date(year, 12, 31))}
    did = {d["disclosure_id"]: d["emp_id"] for d in data["disc"] if int(d["disclosure_year"]) == year}
    first = {}
    for ev in data["history"]:
        if ev["disclosure_id"] in did and ev["event"] == "Submitted":
            t = dt.datetime.strptime(ev["event_time_utc"], "%Y-%m-%dT%H:%M:%SZ")
            e = did[ev["disclosure_id"]]
            first[e] = min(first.get(e, t), t)
    return owed, first, fac
