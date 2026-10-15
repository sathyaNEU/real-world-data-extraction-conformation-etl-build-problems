"""Rows for every CSV in the pack, in each source system's own layout."""
import csv
import datetime as dt
import math

import numpy as np

import basin as B
import production as PR
import world as W


def write_csv(path, cols, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(r)
    return len(rows)


def _iso(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- Talmora
PLUME_COLS = ["plume_id", "campaign", "flight_line", "image_time_utc", "plume_lat", "plume_lon", "emission_rate_kg_h",
              "rate_uncertainty_kg_h", "wind_speed_10m_m_s", "nearest_facility", "facility_distance_m", "processing_version"]


def facility_points(sites, mfac):
    """Every facility number Talmora's attribution knows, with a point: the producers' sites and the midstream."""
    pts = []
    for s in sites:
        for f in s["fac"]:
            pts.append((f, s["lat"], s["lon"]))
    for f in mfac:
        pts.append((f["fac"], f["lat"], f["lon"]))
    return pts


def plume_records(x):
    """All plumes, numbered by campaign in image order, with Talmora's nearest-facility attribution."""
    pts = facility_points(x["sites"], x["mfac"])
    fla = np.array([p[1] for p in pts])
    flo = np.array([p[2] for p in pts])
    allp = [dict(p) for p in x["plumes"]] + [dict(p) for p in x["mplumes"]]
    allp.sort(key=lambda p: (p["campaign"], p["time"], round(p["lat"], 6), round(p["lon"], 6)))
    rng = np.random.default_rng(W.SEED + 85)          # the reanalysis wind at each plume, about its line's mean
    for p in allp:
        p["wind"] = p["wind"] * float(np.exp(rng.normal(0, 0.08)))
    seq = {}
    for p in allp:
        c = p["campaign"]
        seq[c] = seq.get(c, 0) + 1
        p["pid"] = "TA-%s-%04d" % (c.replace("-", ""), seq[c])
        d = np.hypot((p["lat"] - fla) * B.M_PER_DEG_LAT, (p["lon"] - flo) * B.M_PER_DEG_LON)
        i = int(np.argmin(d))
        p["nf"], p["nd"] = (pts[i][0], float(d[i])) if d[i] <= W.ATTRIB_M else (None, None)
    return allp


def plume_rows(recs):
    out = []
    for p in recs:
        ver = "L2-v2.3" if p["campaign"] in ("TB-2511", "TB-2602") else "L2-v2.4"
        out.append([p["pid"], p["campaign"], "L%02d" % (p["line"] + 1), _iso(p["time"]), "%.6f" % p["lat"], "%.6f" % p["lon"],
                    "%.1f" % p["rate"], "%.1f" % p["sigma"], "%.1f" % p["wind"], p["nf"] or "",
                    "" if p["nd"] is None else "%d" % round(p["nd"]), ver])
    return out


COVER_COLS = ["campaign", "flight_line", "line_start_utc", "line_end_utc", "facility_number", "imaged", "note"]


def coverage_rows(x):
    by_line = {}
    for ps in x["passes"] + x["mpasses"]:
        by_line.setdefault((ps["campaign"], ps["line"]), []).append(ps)
    site = {s["site_id"]: s for s in x["sites"]}
    out = []
    for (c, ln), lst in sorted(by_line.items()):
        t0 = min(p["time"] for p in lst) - dt.timedelta(minutes=6)
        t1 = max(p["time"] for p in lst) + dt.timedelta(minutes=9)
        facs = set()
        imaged = lst[0]["imaged"]
        for p in lst:
            if "site" in p:
                for f in site[p["site"]]["fac"]:
                    facs.add(f)
            else:
                facs.add(p["fac"])
        for f in sorted(facs):
            out.append([c, "L%02d" % (ln + 1), _iso(t0), _iso(t1), f, "Y" if imaged else "N", "" if imaged else "line lost to cloud"])
    return out


# ---------------------------------------------------------------- Tarvane
SITE_COLS = ["site_id", "site_name", "site_type", "latitude", "longitude", "facility_numbers", "operator", "operator_since",
             "previous_operator", "field"]


def site_rows(register, wells, seed):
    rng = np.random.default_rng(seed + 81)
    field_of = {}
    for w in wells:
        field_of.setdefault(w["site"], {}).setdefault(w["field"], 0)
        field_of[w["site"]][w["field"]] += 1
    fields = {p[0]: p[5] for p in W.PRODUCERS}
    out = []
    for s in sorted(register, key=lambda z: z["site_id"]):
        fl = max(field_of[s["site_id"]].items(), key=lambda kv: kv[1])[0] if s["site_id"] in field_of else fields[s["producer"]][0][0]
        kind_word = {"well pad": "Pad", "tank battery": "Battery", "compressor station": "Compressor"}[s["kind"]]
        name = "%s %s %d-%d %s" % (s["producer"].split()[0], fl.split()[0], int(rng.integers(1, 36)), int(rng.integers(1, 9)), kind_word)
        cur = s["ops"][-1]
        since = cur[0] if len(s["ops"]) > 1 else dt.date(2014 + int(rng.integers(0, 10)), int(rng.integers(1, 13)), 1)
        prev = s["ops"][-2][1] if len(s["ops"]) > 1 else ""
        out.append([s["site_id"], name, s["kind"], "%.6f" % s["lat"], "%.6f" % s["lon"], "; ".join(s["fac"]), cur[1],
                     since.isoformat(), prev, fl])
    return out


# ---------------------------------------------------------------- the commission
PROD_COLS = ["api_number", "well_name", "operator_number", "field_name", "production_month", "gas_mcf", "oil_bbl", "water_bbl",
             "days_produced", "report_type", "received_date"]


def operator_number(name):
    for p in W.PRODUCERS:
        if p[0] == name:
            return p[1]
    for o in W.OTHER_OPERATORS:
        if o[0] == name:
            return o[1]
    raise KeyError(name)


def production_rows(rows):
    out = []
    for r in sorted(rows, key=lambda z: (z["api"], z["y"], z["m"], z["filed"])):
        out.append([r["api"], r["name"], operator_number(r["op"]), r["field"], "%04d-%02d" % (r["y"], r["m"]), r["gas"], r["oil"],
                    r["water"], r["days"], "ORIGINAL" if r["kind"] == "O" else "AMENDED", r["filed"].isoformat()])
    return out


OPER_COLS = ["operator_number", "operator_name", "status", "mailing_city"]
CITIES = ["Ransom Wells", "Tollaver", "Corrick", "Brannagh Junction", "Brennick", "Dunvarra Flats", "Tamblin Crossing", "Callowmere"]


def operator_rows(seed):
    rng = np.random.default_rng(seed + 82)
    rows = [[p[1], W.LEGAL[p[0]], "ACTIVE", CITIES[int(rng.integers(0, len(CITIES)))]] for p in W.PRODUCERS]
    for name, num, _ in W.OTHER_OPERATORS:
        rows.append([num, name, "ACTIVE", CITIES[int(rng.integers(0, len(CITIES)))]])
    return sorted(rows)


GAS_COLS = ["field_name", "composite_date", "laboratory", "methane_mol_pct", "ethane_mol_pct", "propane_mol_pct",
            "butanes_plus_mol_pct", "co2_mol_pct", "n2_mol_pct", "heating_value_btu_scf"]


def gas_rows(seed):
    rng = np.random.default_rng(seed + 83)
    out = []
    for f in sorted(B.FIELD_CH4):
        for year, ch4 in ((2024, B.FIELD_CH4[f] + float(rng.normal(0, 0.006))), (2026, B.FIELD_CH4[f])):
            c1 = ch4 * 100
            co2 = float(rng.uniform(0.4, 1.6))
            n2 = float(rng.uniform(0.6, 2.2))
            rest = 100 - c1 - co2 - n2
            c2 = rest * float(rng.uniform(0.55, 0.62))
            c3 = rest * float(rng.uniform(0.22, 0.27))
            c4 = rest - c2 - c3
            hv = 10.10 * c1 + 17.70 * c2 + 25.16 * c3 + 32.6 * c4
            day = dt.date(year, 3, int(rng.integers(3, 27)))
            out.append([f, day.isoformat(), ("Basin Analytical Labs" if year == 2024 else "Tressall Gas Laboratories"),
                        "%.2f" % c1, "%.2f" % c2, "%.2f" % c3, "%.2f" % c4, "%.2f" % co2, "%.2f" % n2, "%.1f" % hv])
    return out


FLARE_COLS = ["lease_number", "production_month", "disposition_code", "volume_mcf", "report_type", "received_date"]


def flaring_rows(fl):
    out = []
    for r in sorted(fl["reports"], key=lambda z: (z["lease"], z["y"], z["m"], z["code"], z["filed"])):
        out.append([r["lease"], "%04d-%02d" % (r["y"], r["m"]), r["code"], r["mcf"], "ORIGINAL" if r["kind"] == "O" else "AMENDED",
                    r["filed"].isoformat()])
    return out


LEASE_COLS = ["lease_number", "lease_name", "operator_number", "effective_date"]


def lease_rows(fl):
    out = []
    for L in sorted(fl["leases"], key=lambda z: z["lease"]):
        for eff, op in sorted(L["hist"]):
            out.append([L["lease"], L["name"], operator_number(op), eff.isoformat()])
    return out


BASIN_COLS = ["month", "basin", "flared_mcf", "vented_mcf", "leases_reporting"]


def basin_rows(summary):
    out = []
    for (y, m), a in sorted(summary.items()):
        out.append(["%04d-%02d" % (y, m), W.BASIN, a["flared"], a["vented"], len(a["n"])])
    return out


# ---------------------------------------------------------------- the plant
STATEMENT_COLS = ["statement_id", "statement_month", "revision", "line_no", "station_id", "shipper_code", "reference",
                  "volume_mcf", "energy_mmbtu"]


def statement_rows(pl):
    out = []
    groups = {}
    for ln in pl["lines"]:
        groups.setdefault((ln["sy"], ln["sm"], ln["rev"]), []).append(ln)
    for (y, m, rev), lst in sorted(groups.items()):
        sid = "TGP-%02d%02d-R%d" % (y % 100, m, rev)
        lst = sorted(lst, key=lambda z: (z["station"], z["kind"] != "alloc", z["py"], z["pm"]))
        for i, ln in enumerate(lst, 1):
            if ln["kind"] == "alloc":
                ref = "Alloc %04d-%02d" % (ln["py"], ln["pm"])
            else:
                ref = "PPA %04d-%02d %s %s" % (ln["py"], ln["pm"], ln["station"], ln["word"])
            vol = "" if ln["energy_only"] else "%.0f" % ln["mcf"]
            out.append([sid, "%04d-%02d" % (y, m), rev, i, ln["station"], ln["shipper"], ref, vol, "%.1f" % ln["mmbtu"]])
    return out


STATION_COLS = ["station_id", "station_name", "shipper_code", "operator_number", "in_service", "metering"]


def station_rows(pl, seed):
    rng = np.random.default_rng(seed + 84)
    out = []
    for s in pl["stations"]:
        met = "orifice EFM; ultrasonic energy meter from 2026-07" if s["station"] in pl["energy_only"] else "orifice EFM"
        out.append([s["station"], s["name"], s["shipper"], operator_number(s["op"]),
                    dt.date(2009 + int(rng.integers(0, 14)), int(rng.integers(1, 13)), 1).isoformat(), met])
    return out


HEAT_COLS = ["station_id", "month", "heating_value_btu_scf"]


def heating_rows(pl):
    out = []
    for (st, y, m), h in sorted(pl["hv"].items()):
        out.append([st, "%04d-%02d" % (y, m), "%.1f" % h])
    return out


# ---------------------------------------------------------------- distractors
GHGRP_COLS = ["reporting_year", "facility_id", "facility_name", "parent_company", "industry_segment", "basin",
              "emission_source", "ch4_metric_tons", "co2e_metric_tons"]


def ghgrp_rows(rows):
    out = []
    for r in sorted(rows, key=lambda z: (z["year"], z["fid"], z["source"])):
        out.append([r["year"], r["fid"], r["fname"], r["parent"], "Onshore petroleum and natural gas production", W.BASIN,
                    r["source"], "%.2f" % r["ch4"], "%.1f" % r["co2e"]])
    return out
