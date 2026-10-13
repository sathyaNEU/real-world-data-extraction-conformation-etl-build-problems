"""Read task451's shipped files back into calc.py's transaction rows, the way a solver would: the Datastore extract and
the two funds' activity files in one shape, the member register, the publisher list and the exchange table."""
import csv
import datetime as dt
import os
import re
import xml.etree.ElementTree as ET

import openpyxl

import pack as P


def _date(s):
    return dt.date.fromisoformat(s) if s else None


def _stamp(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ") if s else None


def _split(s):
    return [x for x in s.split(";")] if s else []


def fx(target):
    out = {}
    with open(os.path.join(target, P.FILES["fx"]), newline="") as fh:
        rd = csv.reader(fh)
        hdr = next(rd)
        for c in hdr[1:]:
            out[c] = {}
        out["USD"] = {}
        for r in rd:
            d = _date(r[0])
            out["USD"][d] = 1.0
            for c, v in zip(hdr[1:], r[1:]):
                out[c][d] = float(v)
    return out


def datastore(target):
    rows = []
    with open(os.path.join(target, P.FILES["datastore"]), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            roles = _split(r["participating_org_role"])
            refs = _split(r["participating_org_ref"])
            codes = _split(r["recipient_country_code"])
            pcts = [float(x) for x in _split(r["recipient_country_percentage"])] if len(codes) > 1 else [100.0] * len(codes)
            rows.append(dict(
                aid=r["iati_identifier"], rep=r["reporting_org_ref"], hierarchy=r["hierarchy"] or None,
                parent=r["related_activity_ref"] or None, countries=list(zip(codes, pcts)),
                funding=[x for x, ro in zip(refs, roles) if ro == "1"],
                implementing=[x for x, ro in zip(refs, roles) if ro == "4"],
                dccy=r["default_currency"], other_ids=list(zip(_split(r["other_identifier_ref"]), _split(r["other_identifier_type"]))),
                title=r["title_narrative"], updated=_stamp(r["last_updated_datetime"]), status=r["activity_status_code"],
                ttype=r["transaction_transaction_type_code"], tdate=_date(r["transaction_transaction_date_iso_date"]),
                value=float(r["transaction_value"]), ccy=r["transaction_value_currency"] or None,
                vdate=_date(r["transaction_value_value_date"]), prov_ref=r["transaction_provider_org_ref"] or None,
                prov_name=r["transaction_provider_org_narrative"] or None,
                prov_act=r["transaction_provider_org_provider_activity_id"] or None,
                recv_ref=r["transaction_receiver_org_ref"] or None, recv_name=r["transaction_receiver_org_narrative"] or None,
                recv_act=r["transaction_receiver_org_receiver_activity_id"] or None,
                tcountry=r["transaction_recipient_country_code"] or None,
                desc=r["transaction_description_narrative"], source="datastore"))
    return rows


def fund_xml(target, key):
    rows = []
    root = ET.parse(os.path.join(target, P.FILES[key])).getroot()
    for a in root.findall("iati-activity"):
        aid = a.findtext("iati-identifier")
        rep = a.find("reporting-org").get("ref")
        funding = [p.get("ref") for p in a.findall("participating-org") if p.get("role") == "1"]
        impl = [p.get("ref") for p in a.findall("participating-org") if p.get("role") == "4"]
        countries = [(c.get("code"), float(c.get("percentage"))) for c in a.findall("recipient-country")]
        rel = a.find("related-activity")
        base = dict(aid=aid, rep=rep, hierarchy=a.get("hierarchy"), parent=rel.get("ref") if rel is not None else None,
                    countries=countries, funding=funding, implementing=impl, dccy=a.get("default-currency"),
                    other_ids=[], title=a.find("title").findtext("narrative"), updated=_stamp(a.get("last-updated-datetime")),
                    status=a.find("activity-status").get("code"))
        for t in a.findall("transaction"):
            v = t.find("value")
            pr, rc = t.find("provider-org"), t.find("receiver-org")
            r = dict(base)
            r.update(ttype=t.find("transaction-type").get("code"), tdate=_date(t.find("transaction-date").get("iso-date")),
                     value=float(v.text), ccy=v.get("currency"), vdate=_date(v.get("value-date")),
                     prov_ref=pr.get("ref") if pr is not None else None,
                     prov_name=pr.findtext("narrative") if pr is not None else None,
                     prov_act=pr.get("provider-activity-id") if pr is not None else None,
                     recv_ref=rc.get("ref") if rc is not None else None,
                     recv_name=rc.findtext("narrative") if rc is not None else None,
                     recv_act=rc.get("receiver-activity-id") if rc is not None else None,
                     tcountry=None, desc=(t.find("description").findtext("narrative") if t.find("description") is not None else ""),
                     source=key)
            rows.append(r)
    return rows


def register(target):
    ws = openpyxl.load_workbook(os.path.join(target, P.FILES["register"]), read_only=True)["Members"]
    out = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        prev = re.match(r"(\S+)", r[3]).group(1) if r[3] else None
        out.append(dict(name=r[0], ref=r[2], prev=prev))
    return out


def registry(target):
    out = []
    with open(os.path.join(target, P.FILES["registry"]), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out.append(dict(name=r["publisher_name"], ref=r["iati_organisation_identifier"], type=r["organisation_type"],
                            country=r["country"], other=[x.strip() for x in r["other_identifiers"].split(";") if x.strip()]))
    return out


def load(target):
    rows = datastore(target) + fund_xml(target, "gxml") + fund_xml(target, "sxml")
    return dict(rows=rows, fx=fx(target), register=register(target), registry=registry(target))
