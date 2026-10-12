"""Row writers for the pack's CSV extracts: the connection register, the legacy inverter table, the network model,
the NMI-to-property cross-reference, the council's rates roll, the DER Register extract, the NMI re-allocation log,
the battery rebate approvals and the export manifest."""
from __future__ import annotations

import datetime as dt

import common as K

REGISTER_COLS = ["application_id", "nmi", "application_type", "received_date", "approved_date", "status",
                 "status_date", "connection_date", "removal_date", "inverter_kw_ac", "panel_kwp", "battery_kwh",
                 "export_limit_kw", "phases", "feeder_at_application", "installer_accreditation_no", "program_ref",
                 "legacy_application_no"]
LEGACY_COLS = ["legacy_application_no", "inverter_make_model", "inverter_kw_ac_each", "inverter_count", "migrated_on"]
NETWORK_COLS = ["nmi", "feeder", "zone_substation", "distribution_transformer", "tariff_class", "street_address",
                "locality", "postcode", "nmi_status", "first_energised"]
XREF_COLS = ["nmi", "property_no", "match_method", "last_verified"]
RATES_COLS = ["property_no", "lot_on_plan", "property_address", "locality", "postcode", "land_use_code",
              "land_use_description", "rating_category", "rating_category_description", "land_area_m2",
              "dwelling_year"]
DER_COLS = ["ac_connection_id", "nmi", "device_type", "manufacturer", "model", "rated_power_kw",
            "storage_capacity_kwh", "ac_connection_status", "status_date", "registered_date",
            "installer_accreditation_no", "feeder"]
REALLOC_COLS = ["old_nmi", "new_nmi", "effective_date", "reason"]
REBATE_COLS = ["approval_ref", "property_address", "locality", "postcode", "battery_make_model", "nominal_kwh",
               "approved_date", "rebate_aud", "approval_status"]
MANIFEST_COLS = ["file", "source_system", "extracted", "rows", "owner", "scope"]

LAND_USE = {"01": "Vacant urban land", "02": "Single unit dwelling", "08": "Building units (primary use only)",
            "09": "Group title (primary use only)", "11": "Shop - single", "17": "Restaurant/fast food outlet",
            "27": "Medical centre", "41": "Child care centre"}
RATING = {"R1": "Residential - owner occupied", "R2": "Residential - not owner occupied", "V1": "Vacant land",
          "C1": "Commercial and other"}


def feeder_on(n, d):
    if n["locality"] == "Yarrabin North" and d < K.TRANSFER_DATE:
        return "YRB23"
    return n["feeder"]


def status_date(a):
    if a["status"] == "Withdrawn":
        return a["withdrawn"]
    if a["status"] == "Removed":
        return a["removed"]
    if a["status"] == "Connected":
        return a["connected"]
    if a["status"] == "Approved":
        return a["approved"]
    return a["received"]


def register_rows(W):
    for a in W.apps:
        legacy = a.get("legacy_no")
        kw = "" if legacy else ("%.2f" % a["kw"] if a["kw"] is not None else "")
        kwp = "%.2f" % a["kwp"] if a["kwp"] is not None else ""
        batt = "%.1f" % a["battery"] if a["battery"] else ""
        connected = a["connected"]
        if a["status"] == "Removed":
            connected = a["connected"]
        elim, phases = "", ""
        if a["kw"] is not None:
            phases = "3" if a["kw"] > 10 else "1"
            if a["received"] >= dt.date(2019, 1, 1):
                elim = "%.1f" % (min(a["kw"], 5.0) if phases == "1" else min(a["kw"], 15.0))
        yield [a["app_id"], a["nmi"], a["type"], K.iso(a["received"]), K.iso(a.get("approved")), a["status"],
               K.iso(status_date(a)), K.iso(connected), K.iso(a.get("removed")), kw, kwp, batt, elim, phases,
               feeder_on(a["n"], a["received"]), a["installer"], a["program"] or "", legacy or ""]


def legacy_rows(W, legacy):
    r = K.rng("legacy-models")
    makes = ["SMA Sunny Boy", "Fronius IG Plus", "Power-One Aurora", "Sungrow SG", "Delta Solivia", "Kaco Powador",
             "Zeversolar Eversol", "Samil SolarRiver"]
    for no, kw, count in legacy:
        each = kw / count
        yield [no, "%s %s" % (makes[int(r.integers(0, len(makes)))], ("%.1fk" % each).replace(".0k", "k")),
               "%.2f" % each, count, "2019-06-29"]


def network_rows(W):
    for n in sorted(W.nmis, key=lambda x: (x["feeder"], x["nmi"])):
        yield [n["nmi"], n["feeder"], "Yarrabin ZS", n["transformer"], n["tariff"], n["address"], n["locality"],
               n["postcode"], n["status"], K.iso(n["energised"])]


def xref_rows(W):
    r = K.rng("xref")
    for n in sorted(W.nmis, key=lambda x: x["nmi"]):
        p = n["prop"]
        method = "Address" if r.random() < 0.83 else ("Spatial" if r.random() < 0.8 else "Manual")
        verified = K.add_days(dt.date(2024, 2, 1), int(r.integers(0, 900)))
        if verified > dt.date(2026, 8, 28):
            verified = dt.date(2026, 8, 28)
        yield [n["nmi"], p["property_no"], method, K.iso(verified)]


def rates_rows(W):
    for p in sorted(W.props, key=lambda x: x["property_no"]):
        dwell = "" if p["kind"] in ("vacant", "biz") or p["built"] is None else p["built"]
        yield [p["property_no"], p["lot"], p["address"], p["locality"].upper(), p["postcode"], p["land_use"],
               LAND_USE[p["land_use"]], p["rating"], RATING[p["rating"]], p["area"] if p["area"] else "", dwell]


def der_rows(W):
    for s in W.der_systems:
        for d in s["devices"]:
            yield [s["ac"], s["nmi"], d["type"], d["brand"], d["model"],
                   "%.2f" % d["rated"] if d["rated"] is not None else "",
                   "%.2f" % s["storage"] if d["type"] == "Battery" else "",
                   s["status"], K.iso(s["decom"] or s["registered"]), K.iso(s["registered"]), s["installer"],
                   s["feeder"]]


def realloc_rows(rows):
    for old, new, when, reason in rows:
        yield [old, new, K.iso(when), reason]


def rebate_rows(W):
    """The state home battery rebate's approvals for addresses in Merindah, FY2025-26 (approval does not mean a
    battery was installed; the scheme pays on installation)."""
    r = K.rng("rebate")
    houses = [p for p in W.props if p["kind"] in ("house_oo",) and p["handover"] < dt.date(2025, 1, 1)]
    out = []
    for i, p in enumerate([houses[int(j)] for j in r.choice(len(houses), size=612, replace=False)]):
        make = str(r.choice(["Tesla Powerwall 3", "Sigenergy SigenStor", "BYD Battery-Box HVS", "Alpha ESS SMILE-G3",
                             "Sungrow SBR", "GoodWe Lynx Home"]))
        kwh = float(r.choice([10.24, 13.5, 13.5, 16.0, 9.6, 12.8, 10.1]))
        appr = K.add_days(dt.date(2025, 7, 1), int(r.integers(0, 365)))
        status = str(r.choice(["Approved", "Approved", "Approved", "Paid", "Paid", "Expired"]))
        out.append(["QBR-%06d" % (310000 + i * 3 + int(r.integers(0, 3))), p["address"], p["locality"], p["postcode"],
                    make, "%.2f" % kwh, K.iso(appr), "%d" % int(min(kwh * 250, 3000)), status])
    out.sort(key=lambda x: x[6])
    return out
