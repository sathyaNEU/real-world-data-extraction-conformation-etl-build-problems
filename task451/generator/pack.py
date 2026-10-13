"""Write task451's evidence pack: the IATI Datastore extract, the two funds' activity files, the secretariat's member
register and exchange table, the IATI Registry's publisher list and codelists, the query note and two files the
council also has to hand (country health indicators, office running costs)."""
import csv
import datetime as dt
import io

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import world as W

FILES = {
    "datastore": "datastore_mnh_transactions_2026-10-05.csv",
    "gxml": "pelorus_fund_activities.xml",
    "sxml": "sahel_fund_activities.xml",
    "register": "member_register.xlsx",
    "registry": "iati_registry_publishers_2026-10.csv",
    "fx": "exchange_rates_daily.csv",
    "codelists": "iati_codelists.xlsx",
    "query": "datastore_query_2026-10-05.txt",
    "indicators": "mnh_country_indicators_2024.csv",
    "offices": "office_costs_2027.xlsx",
}
DISTRACTORS = ["indicators", "offices"]

COLS = ["iati_identifier", "reporting_org_ref", "reporting_org_type", "reporting_org_narrative", "title_narrative",
        "activity_status_code", "hierarchy", "related_activity_ref", "related_activity_type", "default_currency",
        "activity_date_start_actual", "activity_date_end_planned", "activity_date_end_actual", "recipient_country_code",
        "recipient_country_percentage", "sector_vocabulary", "sector_code", "sector_percentage", "participating_org_ref",
        "participating_org_role", "participating_org_type", "participating_org_narrative", "other_identifier_ref",
        "other_identifier_type", "transaction_ref", "transaction_transaction_type_code",
        "transaction_transaction_date_iso_date", "transaction_value", "transaction_value_currency",
        "transaction_value_value_date", "transaction_provider_org_ref", "transaction_provider_org_narrative",
        "transaction_provider_org_provider_activity_id", "transaction_receiver_org_ref",
        "transaction_receiver_org_narrative", "transaction_receiver_org_receiver_activity_id",
        "transaction_recipient_country_code", "transaction_description_narrative", "last_updated_datetime"]


def _d(d):
    return d.isoformat() if d else ""


def _num(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".") if abs(v - round(v)) > 1e-9 else "%d" % int(round(v))
    return s


def _orgtype(orgs, ref):
    return orgs.get(ref, {}).get("type", "")


def _orgname(orgs, ref):
    return orgs.get(ref, {}).get("name", "")


def activity_rows(a, orgs):
    pref = a["funding"] + [r for r in a["implementing"] if r not in a["funding"]]
    roles = ["1"] * len(a["funding"]) + ["4"] * len([r for r in a["implementing"] if r not in a["funding"]])
    if a["reporting"] in (W.FUNDS["G"]["ref"], W.FUNDS["S"]["ref"]) and a.get("hierarchy") == "2":
        pref, roles = [a["reporting"]] + [r for r in a["implementing"]], ["1"] + ["4"] * len(a["implementing"])
    end_actual = a["end"] if a["status"] in ("4", "5") else None
    base = {
        "iati_identifier": a["id"], "reporting_org_ref": a["reporting"],
        "reporting_org_type": _orgtype(orgs, a["reporting"]), "reporting_org_narrative": _orgname(orgs, a["reporting"]),
        "title_narrative": a["title"], "activity_status_code": a["status"], "hierarchy": a.get("hierarchy") or "",
        "related_activity_ref": a.get("parent") or "", "related_activity_type": "1" if a.get("parent") else "",
        "default_currency": a["ccy"], "activity_date_start_actual": _d(a["start"]),
        "activity_date_end_planned": _d(a["end"]) if a["status"] != "5" else _d(a.get("planned_end") or a["end"]),
        "activity_date_end_actual": _d(end_actual),
        "recipient_country_code": ";".join(c for c, _ in a["countries"]),
        "recipient_country_percentage": ";".join(_num(p) for _, p in a["countries"]) if len(a["countries"]) > 1 else
        ("100" if a["countries"] else ""),
        "sector_vocabulary": "1", "sector_code": a["sector"], "sector_percentage": "100",
        "participating_org_ref": ";".join(pref), "participating_org_role": ";".join(roles),
        "participating_org_type": ";".join(_orgtype(orgs, r) for r in pref),
        "participating_org_narrative": ";".join(_orgname(orgs, r) for r in pref),
        "other_identifier_ref": ";".join(r for r, _ in a["other_ids"]),
        "other_identifier_type": ";".join(t for _, t in a["other_ids"]),
        "last_updated_datetime": a["updated"].strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    out = []
    for i, t in enumerate(a["tx"]):
        r = dict(base)
        r.update({
            "transaction_ref": t["ref"] or "",
            "transaction_transaction_type_code": t["type"],
            "transaction_transaction_date_iso_date": _d(t["date"]),
            "transaction_value": _num(t["value"]),
            "transaction_value_currency": "" if a.get("omit_ccy") else t["ccy"],
            "transaction_value_value_date": _d(t["value_date"]),
            "transaction_provider_org_ref": (t["provider"] or ("", "", ""))[0] or "",
            "transaction_provider_org_narrative": (t["provider"] or ("", "", ""))[1] or "",
            "transaction_provider_org_provider_activity_id": (t["provider"] or ("", "", ""))[2] or "",
            "transaction_receiver_org_ref": (t["receiver"] or ("", "", ""))[0] or "",
            "transaction_receiver_org_narrative": (t["receiver"] or ("", "", ""))[1] or "",
            "transaction_receiver_org_receiver_activity_id": (t["receiver"] or ("", "", ""))[2] or "",
            "transaction_recipient_country_code": t["country"] or "",
            "transaction_description_narrative": t["desc"],
        })
        out.append(r)
    return out


def write_datastore(w, path):
    """The Datastore's flattened transaction export: one row per transaction on every activity with a recipient
    country among the 13 and a maternal and newborn health sector, the pooled funds' own fund-level activities
    (which name no country) not among them."""
    rows = []
    for k in ("member_acts", "fund_acts", "old", "other_acts"):
        for a in w[k]:
            rows.extend(activity_rows(a, w["orgs"]))
    rows.sort(key=lambda r: (r["reporting_org_ref"], r["iati_identifier"], r["transaction_transaction_date_iso_date"],
                             r["transaction_transaction_type_code"], r["transaction_value"]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=COLS, lineterminator="\r\n")
        wr.writeheader()
        for r in rows:
            wr.writerow(r)
    return len(rows)


# ---------------------------------------------------------------------------------------------- IATI XML
def _esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def activity_xml(a, orgs, ind="  "):
    L = []
    attrs = 'default-currency="%s" last-updated-datetime="%s" xml:lang="en"' % (a["ccy"], a["updated"].strftime("%Y-%m-%dT%H:%M:%SZ"))
    if a.get("hierarchy"):
        attrs += ' hierarchy="%s"' % a["hierarchy"]
    L.append('%s<iati-activity %s>' % (ind, attrs))
    i2 = ind + "  "
    L.append('%s<iati-identifier>%s</iati-identifier>' % (i2, _esc(a["id"])))
    L.append('%s<reporting-org ref="%s" type="%s">' % (i2, a["reporting"], _orgtype(orgs, a["reporting"])))
    L.append('%s  <narrative>%s</narrative>' % (i2, _esc(_orgname(orgs, a["reporting"]))))
    L.append('%s</reporting-org>' % i2)
    L.append('%s<title><narrative>%s</narrative></title>' % (i2, _esc(a["title"])))
    if a.get("description"):
        L.append('%s<description type="1"><narrative>%s</narrative></description>' % (i2, _esc(a["description"])))
    roles = [(r, "1") for r in a["funding"]] + [(r, "4") for r in a["implementing"] if r not in a["funding"]]
    if a.get("hierarchy") == "2":
        roles = [(a["reporting"], "1")] + [(r, "4") for r in a["implementing"]]
    for r, role in roles:
        L.append('%s<participating-org ref="%s" role="%s" type="%s"><narrative>%s</narrative></participating-org>'
                 % (i2, r, role, _orgtype(orgs, r), _esc(_orgname(orgs, r))))
    L.append('%s<activity-status code="%s"/>' % (i2, a["status"]))
    L.append('%s<activity-date type="2" iso-date="%s"/>' % (i2, a["start"].isoformat()))
    L.append('%s<activity-date type="3" iso-date="%s"/>' % (i2, a["end"].isoformat()))
    if a["status"] in ("4", "5"):
        L.append('%s<activity-date type="4" iso-date="%s"/>' % (i2, a["end"].isoformat()))
    if a["countries"]:
        for c, p in a["countries"]:
            L.append('%s<recipient-country code="%s" percentage="%s"/>' % (i2, c, _num(p)))
    else:
        L.append('%s<recipient-region code="289" vocabulary="1" percentage="50"/>' % i2)
        L.append('%s<recipient-region code="798" vocabulary="1" percentage="50"/>' % i2)
    L.append('%s<sector code="%s" vocabulary="1" percentage="100"/>' % (i2, a["sector"]))
    if a.get("parent"):
        L.append('%s<related-activity ref="%s" type="1"/>' % (i2, a["parent"]))
    for t in a["tx"]:
        L.append('%s<transaction>' % i2)
        i3 = i2 + "  "
        L.append('%s<transaction-type code="%s"/>' % (i3, t["type"]))
        L.append('%s<transaction-date iso-date="%s"/>' % (i3, t["date"].isoformat()))
        vd = (' value-date="%s"' % t["value_date"].isoformat()) if t["value_date"] else ""
        L.append('%s<value currency="%s"%s>%s</value>' % (i3, t["ccy"], vd, _num(t["value"])))
        if t["desc"]:
            L.append('%s<description><narrative>%s</narrative></description>' % (i3, _esc(t["desc"])))
        if t["provider"]:
            ref, nm, act = t["provider"]
            pa = (' provider-activity-id="%s"' % act) if act else ""
            L.append('%s<provider-org ref="%s"%s><narrative>%s</narrative></provider-org>' % (i3, ref, pa, _esc(nm)))
        if t["receiver"]:
            ref, nm, act = t["receiver"]
            ra = (' receiver-activity-id="%s"' % act) if act else ""
            L.append('%s<receiver-org ref="%s"%s><narrative>%s</narrative></receiver-org>' % (i3, ref, ra, _esc(nm)))
        L.append('%s</transaction>' % i2)
    L.append('%s</iati-activity>' % ind)
    return L


def write_fund_xml(w, fund_key, path):
    pool = w["gfund"] if fund_key == "G" else w["sfund"]
    ref = W.FUNDS[fund_key]["ref"]
    acts = [pool] + [a for a in w["fund_acts"] if a["reporting"] == ref]
    stamp = max(a["updated"] for a in acts)
    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<iati-activities version="2.03" generated-datetime="%s">' % stamp.strftime("%Y-%m-%dT%H:%M:%SZ")]
    for a in acts:
        L.extend(activity_xml(a, w["orgs"]))
    L.append('</iati-activities>')
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    return len(acts)


# ---------------------------------------------------------------------------------------------- workbooks and tables
HEAD_FILL = PatternFill("solid", fgColor="DCE6F0")


def _sheet(ws, header, rows, widths, freeze="A2"):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
        c.alignment = Alignment(vertical="top", wrap_text=True)
    for r in rows:
        ws.append([None if v == "" else v for v in r])
    for i, wdt in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = wdt
    ws.freeze_panes = freeze


def write_register(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Members"
    pools = {"ASH": W.FUNDS["G"]["name"], "MER": W.FUNDS["G"]["name"], "TRE": W.FUNDS["G"]["name"],
             "FJE": W.FUNDS["S"]["name"], "ZIL": W.FUNDS["G"]["name"], "SEE": W.FUNDS["S"]["name"]}
    since = {"ASH": 2019, "MER": 2019, "TRE": 2020, "FJE": 2021, "ZIL": 2019, "SEE": 2022}
    rows = []
    for k in W.MEMBER_KEYS:
        m = W.M[k]
        prev = "%s (to 30 June 2024)" % m["prev"] if m["prev"] else ""
        rows.append([m["name"], m["country"], m["ref"], prev, since[k], pools[k]])
    _sheet(ws, ["Member", "Registered in", "IATI organisation identifier", "Previous IATI identifier", "Member since",
                "Pooled fund contributions"], rows, [30, 16, 30, 32, 14, 34])
    ws2 = wb.create_sheet("About")
    for line in ["Register of members of the %s, at %s." % (W.COLLAB, W.REGISTER_ASOF.strftime("%-d %B %Y")),
                 "Each member publishes its grants to IATI under the identifier shown.",
                 "Kept by the secretariat (%s)." % W.PEOPLE["data"][0]]:
        ws2.append([line])
    ws2.column_dimensions["A"].width = 100
    wb.save(path)


def write_registry(w, path):
    """The IATI Registry's publisher list for every publisher in the extract, one row per publisher account."""
    orgs = w["orgs"]
    rows = []
    reps = sorted({a["reporting"] for k in ("member_acts", "fund_acts", "old", "other_acts") for a in w[k]} |
                  {W.FUNDS["G"]["ref"], W.FUNDS["S"]["ref"]} | {p["ref"] for p in W.PARTNERS.values()} |
                  {W.REGIONAL["ref"]})
    other = {W.M["FJE"]["ref"]: W.M["FJE"]["prev"]}
    for d in W.DEVICE_ORGS:
        other[d[3]] = d[5]
    countries = {}
    for d in W.DEVICE_ORGS:
        countries[d[3]] = countries[d[5]] = W.ISO[d[1]]
    for n in W.NET_ORGS:
        countries[n[3]] = W.ISO[n[1][0]] if n[4] == "24" else {"GB": "GB", "US": "US", "NL": "NL"}[n[3][:2]]
    for k in W.MEMBER_KEYS:
        countries[W.M[k]["ref"]] = {"United States": "US", "United Kingdom": "GB", "Norway": "NO", "Netherlands": "NL",
                                    "Switzerland": "CH"}[W.M[k]["country"]]
    countries["XI-IATI-FJR"] = "NO"
    countries[W.FUNDS["G"]["ref"]] = "GB"
    countries[W.FUNDS["S"]["ref"]] = "SN"
    countries[W.PARTNERS["WEX"]["ref"]] = "US"
    countries[W.PARTNERS["KIY"]["ref"]] = "JP"
    countries[W.REGIONAL["ref"]] = "NE"
    for imp in w["impls"]:
        countries[imp["ref"]] = W.ISO[imp["country"]]
    for dn in w["donors"]:
        countries[dn["ref"]] = {"US": "US", "GB": "GB", "NL": "NL", "XI": "CH"}[dn["ref"][:2]]
    first = {}
    rng = np.random.default_rng(W.SEED + 71)
    for r in reps:
        y = 2013 + int(rng.integers(0, 10))
        first[r] = dt.date(y, int(rng.integers(1, 13)), int(rng.integers(1, 28)))
    for d in W.DEVICE_ORGS:
        first[d[3]] = d[6]
    first[W.M["FJE"]["ref"]] = W.NEW_ID_FROM
    first[W.FUNDS["G"]["ref"]] = dt.date(2023, 9, 18)
    first[W.FUNDS["S"]["ref"]] = dt.date(2024, 1, 3)
    upd = {}
    for k in ("member_acts", "fund_acts", "old", "other_acts"):
        for a in w[k]:
            upd[a["reporting"]] = max(upd.get(a["reporting"], a["updated"]), a["updated"])
    upd[W.FUNDS["G"]["ref"]] = w["gfund"]["updated"]
    upd[W.FUNDS["S"]["ref"]] = w["sfund"]["updated"]
    for r in reps:
        if r not in upd:
            upd[r] = dt.datetime(2026, 5, 11, 8, 0, 0) + dt.timedelta(hours=int(rng.integers(0, 2000)))
    for r in reps:
        rows.append([_orgname(orgs, r), r, _orgtype(orgs, r), countries.get(r, ""), other.get(r, ""),
                     first[r].isoformat(), upd[r].strftime("%Y-%m-%d")])
    rows.sort(key=lambda x: x[0].lower())
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(["publisher_name", "iati_organisation_identifier", "organisation_type", "country",
                     "other_identifiers", "publishing_since", "last_updated"])
        wr.writerows(rows)
    return len(rows)


def write_fx(fx, path):
    ccys = [c for c in W.CURRENCIES if c != "USD"]
    dates = sorted(fx["USD"])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(["date"] + ccys)
        for d in dates:
            wr.writerow([d.isoformat()] + [("%g" % fx[c][d]) for c in ccys])
    return len(dates)


CODELISTS = {
    "TransactionType": [("1", "Incoming Funds", "Funds received for use on the activity, from an external source."),
                        ("2", "Outgoing Commitment", "A firm, written obligation from the reporting organisation to provide resources of a specified amount."),
                        ("3", "Disbursement", "Outgoing funds placed at the disposal of a recipient government or organisation."),
                        ("4", "Expenditure", "Outgoing funds spent directly on goods and services for the activity."),
                        ("5", "Interest Payment", "The actual amount of interest paid on a loan or line of credit."),
                        ("6", "Loan Repayment", "The actual amount of principal repaid."),
                        ("7", "Reimbursement", "A type of disbursement that covers funds already spent by the recipient."),
                        ("8", "Purchase of Equity", "Outgoing funds used to buy equity."),
                        ("11", "Incoming Commitment", "A firm, written obligation from a donor or provider to provide funds to the activity."),
                        ("12", "Outgoing Pledge", "An indication of support that is not yet a commitment."),
                        ("13", "Incoming Pledge", "An indication of support from a provider that is not yet a commitment.")],
    "OrganisationRole": [("1", "Funding", "The government or organisation which provides funds to the activity."),
                         ("2", "Accountable", "An organisation responsible for oversight of the activity and its outcomes."),
                         ("3", "Extending", "An organisation that manages the budget and direction of an activity on behalf of the funding organisation."),
                         ("4", "Implementing", "The organisation that physically carries out the activity or intervention.")],
    "OrganisationType": [("10", "Government", ""), ("15", "Other Public Sector", ""), ("21", "International NGO", ""),
                         ("22", "National NGO", ""), ("23", "Regional NGO", ""), ("24", "Partner Country based NGO", ""),
                         ("40", "Multilateral", ""), ("60", "Foundation", ""), ("70", "Private Sector", ""),
                         ("80", "Academic, Training and Research", ""), ("90", "Other", "")],
    "ActivityStatus": [("1", "Pipeline/identification", ""), ("2", "Implementation", ""), ("3", "Finalisation", ""),
                       ("4", "Closed", ""), ("5", "Cancelled", ""), ("6", "Suspended", "")],
    "OtherIdentifierType": [("A1", "Reporting Organisation's internal activity identifier", ""),
                            ("A2", "CRS Activity identifier", ""), ("A3", "Previous Activity Identifier", ""),
                            ("A9", "Other Activity Identifier", ""), ("B1", "Previous Reporting Organisation Identifier", ""),
                            ("B9", "Other Organisation Identifier", "")],
    "Sector": [(c, n, "DAC 5-digit purpose code") for c, n in W.SECTORS],
    "Country": [(iso, nm, "") for nm, iso, _, _ in W.COUNTRIES],
    "Region": [("289", "South of Sahara, regional", ""), ("798", "Asia, regional", "")],
}


def write_codelists(path):
    wb = openpyxl.Workbook()
    first = True
    for name, rows in CODELISTS.items():
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = name
        _sheet(ws, ["code", "name", "description"], [list(r) for r in rows], [8, 44, 90])
    wb.save(path)


def write_query(path):
    text = (
        "IATI Datastore query\r\n"
        "Run: 2026-10-05 07:14 UTC by %s (%s)\r\n"
        "Activities: recipient country in KE, UG, TZ, ET, RW, NE, ML, BF, TD, SN, NP, BD, PK\r\n"
        "            and sector (vocabulary 1, DAC 5-digit) in 13020, 12220, 12281, 13030\r\n"
        "Transactions: every transaction on those activities dated 2023-01-01 to 2026-09-30\r\n"
        "Output: CSV, one row per transaction, activity fields repeated on each row; fields with several values\r\n"
        "        (participating organisations, recipient countries and their percentages, other identifiers) are\r\n"
        "        separated by semicolons in the same order\r\n"
        "Rows: %%d\r\n"
        "Activities that name no recipient country (the pooled funds' fund-level activities) are not returned by a\r\n"
        "country query; their files were downloaded from the funds' IATI Registry pages on the same day.\r\n"
        % (W.PEOPLE["finance"][0], W.SECRETARIAT))
    return text


def write_query_file(path, nrows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(write_query(path) % nrows)


INDICATORS = {  # live births (thousands), maternal deaths per 100,000 live births, newborn deaths per 1,000, skilled attendance %
    "Kenya": (1456, 530, 21, 70), "Uganda": (1663, 284, 19, 74), "Tanzania": (2187, 238, 20, 64),
    "Ethiopia": (3854, 267, 27, 50), "Rwanda": (382, 259, 18, 94), "Niger": (1132, 441, 24, 44),
    "Mali": (937, 440, 31, 67), "Burkina Faso": (768, 264, 24, 80), "Chad": (731, 1063, 32, 24),
    "Senegal": (548, 261, 21, 75), "Nepal": (546, 174, 16, 80), "Bangladesh": (2917, 123, 16, 59),
    "Pakistan": (6375, 154, 39, 68)}


def write_indicators(path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(["country", "iso2", "live_births_thousands", "maternal_mortality_ratio", "neonatal_mortality_rate",
                     "skilled_birth_attendance_pct", "note"])
        for c in W.NAMES:
            b, mmr, nmr, sba = INDICATORS[c]
            wr.writerow([c, W.ISO[c], b, mmr, nmr, sba, "secretariat compilation from national surveys, rounded"])


OFFICES = {"Kenya": ("Nairobi", 61200, 238000, 21500, 48000), "Uganda": ("Kampala", 47400, 211000, 19800, 41000),
           "Tanzania": ("Dar es Salaam", 52800, 219000, 17600, 43000), "Ethiopia": ("Addis Ababa", 58900, 205000, 26400, 52000),
           "Rwanda": ("Kigali", 39600, 197000, 12900, 37000), "Niger": ("Niamey", 33500, 226000, 48700, 61000),
           "Mali": ("Bamako", 36100, 231000, 51300, 58000), "Burkina Faso": ("Ouagadougou", 31800, 224000, 46900, 55000),
           "Chad": ("N'Djamena", 44700, 248000, 57200, 66000), "Senegal": ("Dakar", 55300, 233000, 18400, 45000),
           "Nepal": ("Kathmandu", 29400, 176000, 11800, 34000), "Bangladesh": ("Dhaka", 34600, 182000, 16300, 39000),
           "Pakistan": ("Islamabad", 37900, 191000, 29600, 47000)}


def write_offices(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Office costs 2027"
    rows = []
    for c in W.NAMES:
        city, rent, staff, sec, setup = OFFICES[c]
        rows.append([c, city, rent, staff, sec, rent + staff + sec, setup])
    _sheet(ws, ["Country", "City", "Rent and services (USD a year)", "Three posts (USD a year)", "Security (USD a year)",
                "Running cost (USD a year)", "Set-up (USD, once)"], rows, [16, 16, 16, 16, 16, 16, 14])
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=7):
        for c in row:
            c.number_format = "#,##0"
    ws2 = wb.create_sheet("Notes")
    ws2.append(["Estimates gathered by the secretariat from members' country staff and three facilities agents, August 2026."])
    ws2.append(["Running cost is rent and services, three posts and security for a full year."])
    ws2.column_dimensions["A"].width = 100
    wb.save(path)
