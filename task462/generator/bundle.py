"""The shipped folder read back into plain records, as an analyst would load it: every estimator in methods.py and every
golden figure runs on these, never on the generator's own state."""
import csv
import datetime as dt
import json
import os

import world as W


def _rows(target, key):
    with open(os.path.join(target, W.FILES[key]), newline="") as f:
        return list(csv.DictReader(f))


def _ym(s):
    return int(s[:4]), int(s[5:7])


def _t(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def releases(target):
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(target, W.FILES["releases"]), read_only=True)["Releases"]
    it = ws.iter_rows(values_only=True)
    head = list(next(it))
    out = []
    for r in it:
        d = dict(zip(head, r))
        if d["release_id"] is None:
            continue
        out.append(dict(rid=d["release_id"], rate=float(d["metered_rate_kg_h"]), wind=float(d["wind_speed_10m_m_s"]),
                        detected=d["plume_detected"] == "Y",
                        est=None if d["quantified_rate_kg_h"] is None else float(d["quantified_rate_kg_h"])))
    return out


def operators(target):
    """Operator number to the producer's name as the site register writes it (the commission's list carries legal
    names; the register the short names they start with)."""
    out = {}
    for r in _rows(target, "operators"):
        short = [p for p in W.NAMES if r["operator_name"].startswith(p)]
        out[r["operator_number"]] = short[0] if short else r["operator_name"]
    return out


def sites(target):
    out = []
    for r in _rows(target, "sites"):
        ops = [(W.RATING_START, r["operator"])]
        if r["previous_operator"]:
            ops = [(W.RATING_START, r["previous_operator"]), (dt.date.fromisoformat(r["operator_since"]), r["operator"])]
        out.append(dict(site_id=r["site_id"], kind=r["site_type"], lat=float(r["latitude"]), lon=float(r["longitude"]),
                        fac=r["facility_numbers"].split("; "), ops=ops, field=r["field"]))
    return out


def passes(target, site_list):
    """Each register site's passes: a site is under a flight line where any of its facility numbers is."""
    by_fac = {}
    for s in site_list:
        for f in s["fac"]:
            by_fac.setdefault(f, []).append(s["site_id"])
    seen = {}
    for r in _rows(target, "coverage"):
        for sid in by_fac.get(r["facility_number"], []):
            key = (r["campaign"], r["flight_line"], sid)
            if key not in seen:
                seen[key] = dict(campaign=r["campaign"], line=r["flight_line"], time=_t(r["line_start_utc"]), site=sid,
                                 imaged=r["imaged"] == "Y")
    return list(seen.values())


def plumes(target):
    out = []
    for r in _rows(target, "plumes"):
        out.append(dict(n=r["plume_id"], pid=r["plume_id"], campaign=r["campaign"], line=r["flight_line"],
                        time=_t(r["image_time_utc"]), lat=float(r["plume_lat"]), lon=float(r["plume_lon"]),
                        rate=float(r["emission_rate_kg_h"]), sigma=float(r["rate_uncertainty_kg_h"]),
                        wind=float(r["wind_speed_10m_m_s"]), nf=r["nearest_facility"] or None,
                        nd=float(r["facility_distance_m"]) if r["facility_distance_m"] else None, raw=r))
    return out


def production(target):
    ops = operators(target)
    out = []
    for r in _rows(target, "production"):
        y, m = _ym(r["production_month"])
        out.append(dict(api=r["api_number"], y=y, m=m, op=ops[r["operator_number"]], field=r["field_name"],
                        gas=int(r["gas_mcf"]), kind=r["report_type"], filed=dt.date.fromisoformat(r["received_date"])))
    return out


def composites(target):
    """Each field's methane share (fraction) by composite year."""
    out = {}
    for r in _rows(target, "gas"):
        out.setdefault(r["field_name"], {})[int(r["composite_date"][:4])] = float(r["methane_mol_pct"]) / 100.0
    return out


def ghgrp(target):
    return [dict(year=int(r["reporting_year"]), parent=r["parent_company"], source=r["emission_source"],
                 ch4=float(r["ch4_metric_tons"])) for r in _rows(target, "ghgrp")]


def satellite(target):
    return json.load(open(os.path.join(target, W.FILES["satellite"])))


def statements(target):
    out = []
    for r in _rows(target, "statements"):
        ref = r["reference"].split()
        out.append(dict(sid=r["statement_id"], sy=_ym(r["statement_month"])[0], sm=_ym(r["statement_month"])[1],
                        rev=int(r["revision"]), station=r["station_id"], shipper=r["shipper_code"], ref=r["reference"],
                        kind="alloc" if ref[0] == "Alloc" else "ppa", py=_ym(ref[1])[0], pm=_ym(ref[1])[1],
                        mcf=float(r["volume_mcf"]) if r["volume_mcf"] else None, mmbtu=float(r["energy_mmbtu"])))
    return out


def stations(target):
    ops = operators(target)
    return {r["station_id"]: dict(op=ops[r["operator_number"]], shipper=r["shipper_code"], metering=r["metering"])
            for r in _rows(target, "stations")}


def heating(target):
    return {(r["station_id"],) + _ym(r["month"]): float(r["heating_value_btu_scf"]) for r in _rows(target, "heating")}


def flaring(target):
    out = []
    for r in _rows(target, "flaring"):
        y, m = _ym(r["production_month"])
        out.append(dict(lease=r["lease_number"], y=y, m=m, code=r["disposition_code"], mcf=int(r["volume_mcf"]),
                        kind=r["report_type"], filed=dt.date.fromisoformat(r["received_date"])))
    return out


def leases(target):
    ops = operators(target)
    out = {}
    for r in _rows(target, "leases"):
        out.setdefault(r["lease_number"], []).append((dt.date.fromisoformat(r["effective_date"]), ops[r["operator_number"]]))
    return {k: sorted(v) for k, v in out.items()}


def basin(target):
    return {_ym(r["month"]): dict(flared=int(r["flared_mcf"]), vented=int(r["vented_mcf"]), n=int(r["leases_reporting"]))
            for r in _rows(target, "basin")}


def load(target):
    st = sites(target)
    return dict(sites=st, passes=passes(target, st), plumes=plumes(target), releases=releases(target),
                production=production(target), composites=composites(target), ghgrp=ghgrp(target),
                satellite=satellite(target), statements=statements(target), stations=stations(target),
                heating=heating(target), flaring=flaring(target), leases=leases(target), basin=basin(target))
