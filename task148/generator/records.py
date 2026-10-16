"""The exports, written from the world: the legacy ACD call detail and the i3 call log, the floor roster, the
call-handling system's location records for the north-east, the township boundary, the ESInet PSAP directory, the
callback desk's tasks, the CAD incident export and the administrative line's ACD export."""
from __future__ import annotations

import datetime as dt
import json

import numpy as np

import common as K
import geo as G

F_LEGACY = "acd_call_detail_legacy_2025-01-01_2025-05-16.csv"
F_I3 = "i3_call_log_2025-05-13_2026-09-30.jsonl"
F_ROSTER = "floor_roster_2025-01_2026-09.csv"
F_FORECAST = "tri_county_911_hourly_forecast_fy2027_fy2028.xlsx"
F_CHE = "che_location_records_fy2026_northeast.csv"
F_BOUNDARY = "halvorsen_township_boundary.geojson"
F_DIRECTORY = "esinet_psap_directory.csv"
F_CALLBACK = "callback_desk_tasks_2026-01_2026-06.csv"
F_CAD = "cad_incidents_fy2026_fri_sat_late.csv"
F_ADMIN = "admin_line_acd_fy2026.csv"
F_MANIFEST = "qa_extract_log.csv"

QUEUE_URI = "sip:911@acd.tavish911.example"
ESINET = "tricounty911.example"
URI = {
    "wexley": "sip:psap@ecc.wexley911.example", "wexley_alt": "sip:alt07@bkp.state911.example",
    "garrick": "sip:911@ecc.garrick911.example", "garrick_alt": "sip:alt03@bkp.state911.example",
    "patrol": "sip:d6@comms.statepatrol.example", "hollin": "sip:911@pd.hollincreek.example",
}
LEGACY_CODE = {"wexley": "WEXLEY", "wexley_alt": "WEX ALT", "garrick": "GARRICK", "garrick_alt": "GAR ALT",
               "patrol": "SP D6", "hollin": "HOLLIN CR"}
I3_SERVICE = {"wireless": "wireless", "voip": "voip", "residence": "fixed", "business": "fixed", "mlts": "mlts",
              "telematics": "telematics"}
LEGACY_TRUNKS = {"wireless": ("WRLS", 6), "voip": ("VOIP", 2), "residence": ("CAMA", 4), "business": ("CAMA", 4),
                 "mlts": ("CAMA", 4), "telematics": ("TLMX", 1)}


def call_ids(W):
    """i3 Call Identifiers, assigned by the ESInet's routing proxy, and legacy CALL_IDs (date and daily sequence)."""
    ids = [None] * W.N
    seqs = {}
    for i in range(W.N):
        if in_legacy(W, i):
            d = K.to_local(W.t[i]).date()
            seqs[d] = seqs.get(d, 0) + 1
            ids[i] = "%s%05d" % (d.strftime("%y%m%d"), seqs[d])
        else:
            ids[i] = "urn:emergency:uid:callid:%s:esrp.%s" % (K.token("callid", i, n=10), ESINET)
    W.call_id = ids
    W.legacy_seq = seqs
    return ids


def in_legacy(W, i):
    t = W.t[i]
    if t < K.CUT_WIRELESS.astimezone(K.UTC).timestamp():
        return True
    return W.kind[i] in ("residence", "business", "mlts") and t < K.CUT_WIRELINE.astimezone(K.UTC).timestamp()


def test_in_legacy(ts):
    return ts < K.CUT_WIRELESS.astimezone(K.UTC).timestamp()


def cb_token(caller):
    return K.token("cbn", caller, n=12)


def _xfer_key(dest, alt):
    return dest + ("_alt" if alt else "")


# ---------------------------------------------------------------------------------------------------- legacy CSV
LEGACY_COLS = ["CALL_ID", "SEIZE_TIME", "ANS_TIME", "REL_TIME", "RDY_TIME", "DISC_TIME", "CALL_STATUS",
               "POSITION", "TRUNK_GROUP", "CLASS_OF_SVC", "XFER_IN_FROM", "XFER_OUT_TO", "CBN_REF"]


def legacy_rows(W):
    rows = []
    for i in range(W.N):
        if not in_legacy(W, i):
            continue
        kd = W.kind[i]
        r = K.rng("legacy", i)
        tg, n_tg = LEGACY_TRUNKS[kd]
        cls = {"wireless": "WPH2" if r.random() < 0.86 else "WPH1", "voip": "VOIP", "residence": "RESD",
               "business": "BUSN", "mlts": "PBXB", "telematics": "TLMA"}[kd]
        row = {"CALL_ID": W.call_id[i], "SEIZE_TIME": K.local_str(W.t[i]), "TRUNK_GROUP": "%s-%d" % (tg, r.integers(1, n_tg + 1)),
               "CLASS_OF_SVC": cls, "CBN_REF": cb_token(int(W.caller[i])).upper()}
        if W.xin[i]:
            row["XFER_IN_FROM"] = LEGACY_CODE[W.xin[i]]
        if W.ab[i]:
            row["CALL_STATUS"] = "ABN"
            row["DISC_TIME"] = K.local_str(W.hang_t[i])
        else:
            row["CALL_STATUS"] = "ANS"
            row["ANS_TIME"] = K.local_str(W.ans_t[i])
            row["REL_TIME"] = K.local_str(W.rel_t[i])
            row["RDY_TIME"] = K.local_str(W.ready_t[i])
            row["POSITION"] = W.position[i].replace("CT", "POS")
            if W.xout[i]:
                row["XFER_OUT_TO"] = LEGACY_CODE[_xfer_key(W.xout[i], W.xout_alt[i])]
        rows.append((W.t[i], row))
    tseq = {}
    for ts, dur, tid in W.tests:
        if not test_in_legacy(ts):
            continue
        d = K.to_local(ts).date()
        tseq[d] = tseq.get(d, 0) + 1
        rows.append((ts, {"CALL_ID": "%sT%02d" % (d.strftime("%y%m%d"), tseq[d]), "SEIZE_TIME": K.local_str(ts),
                          "ANS_TIME": K.local_str(ts + 1.0), "DISC_TIME": K.local_str(ts + dur),
                          "CALL_STATUS": "TST", "POSITION": "TEST", "TRUNK_GROUP": "CAMA-%d" % (1 + tid % 4),
                          "CLASS_OF_SVC": "TEST", "CBN_REF": ""}))
    rows.sort(key=lambda x: x[0])
    return [r for _, r in rows]


# ---------------------------------------------------------------------------------------------------- i3 JSON Lines
def i3_lines(W):
    out = []
    for i in range(W.N):
        if in_legacy(W, i):
            continue
        o = {"callId": W.call_id[i], "queue": QUEUE_URI, "presented": K.iso_utc_ms(W.t[i]),
             "serviceType": I3_SERVICE[W.kind[i]]}
        if W.xin[i]:
            o["referredBy"] = URI[W.xin[i]]
        if W.ab[i]:
            o["disposition"] = "abandoned"
            o["ended"] = K.iso_utc_ms(W.hang_t[i])
        else:
            o["disposition"] = "answered"
            o["answered"] = K.iso_utc_ms(W.ans_t[i])
            if W.xout[i]:
                o["transferTo"] = URI[_xfer_key(W.xout[i], W.xout_alt[i])]
                o["transferAt"] = K.iso_utc_ms(W.xout_t[i])
            o["released"] = K.iso_utc_ms(W.rel_t[i])
            o["ready"] = K.iso_utc_ms(W.ready_t[i])
            o["position"] = W.position[i]
        o["callbackRef"] = "cb-" + cb_token(int(W.caller[i]))
        out.append((W.t[i], json.dumps(o, separators=(",", ":"))))
    for ts, dur, tid in W.tests:
        if test_in_legacy(ts):
            continue
        o = {"callId": "urn:emergency:uid:callid:%s:esrp.%s" % (K.token("testcall", tid, n=10), ESINET),
             "queue": QUEUE_URI, "presented": K.iso_utc_ms(ts), "serviceType": "test",
             "disposition": "test-responder", "answered": K.iso_utc_ms(ts + 0.4), "ended": K.iso_utc_ms(ts + dur),
             "callbackRef": "cb-" + K.token("testcbn", tid % 3, n=12)}
        out.append((ts, json.dumps(o, separators=(",", ":"))))
    out.sort(key=lambda x: x[0])
    return [s for _, s in out]


# ---------------------------------------------------------------------------------------------------- roster
ROSTER_COLS = ["date", "block", "call_takers_on_911", "note"]


def roster_rows(W):
    rows = []
    for (d, blk), (c, note) in sorted(W.roster.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        if blk == K.LATE_BLOCK and d < K.HIST_START.date() - dt.timedelta(days=1):
            continue
        if d < K.HIST_START.date() and blk != K.LATE_BLOCK:
            continue
        rows.append({"date": d.isoformat(), "block": blk, "call_takers_on_911": c, "note": note})
    return rows


# ---------------------------------------------------------------------------------------------------- CHE locations
CHE_COLS = ["call_id", "seq", "received_utc", "method", "latitude", "longitude", "radius_m", "confidence_pct",
            "cell_sector"]
FY26 = (dt.datetime(2025, 7, 1, tzinfo=K.TZ).astimezone(K.UTC).timestamp(),
        dt.datetime(2026, 7, 1, tzinfo=K.TZ).astimezone(K.UTC).timestamp())


def che_rows(W):
    rows = []
    for i, (sid, recs) in sorted(W.locrecs.items(), key=lambda kv: W.t[kv[0]]):
        if not (FY26[0] <= W.t[i] < FY26[1]) or in_legacy(W, i):
            continue
        for s, (method, when, x, y, rad, conf) in enumerate(recs, start=1):
            lat, lon = G.to_latlon(x, y)
            rows.append({"call_id": W.call_id[i], "seq": s, "received_utc": K.iso_utc_ms(when), "method": method,
                         "latitude": "%.6f" % lat, "longitude": "%.6f" % lon, "radius_m": int(round(rad)),
                         "confidence_pct": conf, "cell_sector": sid if method == "cell" else ""})
    return rows


# ---------------------------------------------------------------------------------------------------- boundary
def boundary_geojson():
    main = G.MAIN if G.signed_area(G.MAIN) > 0 else G.MAIN[::-1]
    hole = G.HOLE if G.signed_area(G.HOLE) < 0 else G.HOLE[::-1]
    det = G.DETACHED if G.signed_area(G.DETACHED) > 0 else G.DETACHED[::-1]
    feat = {"type": "Feature",
            "properties": {"NAME": "Halvorsen Township", "TYPE": "civil township", "COUNTY": "Tavish",
                           "GEOID_LOCAL": "TC-TWP-14", "SOURCE": "Tavish County GIS, municipal boundaries",
                           "EFFECTIVE": "2024-03-01", "ECRF_LAYER": "PSAP boundary for the Halvorsen move, in service from 1 July 2027"},
            "geometry": {"type": "MultiPolygon",
                         "coordinates": [[G.ring_lonlat(main), G.ring_lonlat(hole)], [G.ring_lonlat(det)]]}}
    fc = {"type": "FeatureCollection", "name": "halvorsen_township_boundary",
          "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}, "features": [feat]}
    return json.dumps(fc, indent=1) + "\n"


# ---------------------------------------------------------------------------------------------------- directory
DIRECTORY_COLS = ["agency", "psap", "role", "uri", "county_or_area"]


def directory_rows():
    return [
        {"agency": K.AGENCY, "psap": "Tavish County 911", "role": "primary", "uri": QUEUE_URI, "county_or_area": "Tavish"},
        {"agency": K.AGENCY, "psap": "Tavish County 911, backup centre", "role": "alternate",
         "uri": "sip:911-b@backup.tavish911.example", "county_or_area": "Tavish"},
        {"agency": K.NEIGHBOUR, "psap": "Wexley County 911", "role": "primary", "uri": URI["wexley"], "county_or_area": "Wexley"},
        {"agency": K.NEIGHBOUR, "psap": "Wexley County 911, state backup centre position group 7", "role": "alternate",
         "uri": URI["wexley_alt"], "county_or_area": "Wexley"},
        {"agency": "Garrick County Emergency Communications", "psap": "Garrick County 911", "role": "primary",
         "uri": URI["garrick"], "county_or_area": "Garrick"},
        {"agency": "Garrick County Emergency Communications", "psap": "Garrick County 911, state backup centre position group 3",
         "role": "alternate", "uri": URI["garrick_alt"], "county_or_area": "Garrick"},
        {"agency": "Hollin Creek Police Department", "psap": "Hollin Creek PD Communications", "role": "secondary",
         "uri": URI["hollin"], "county_or_area": "City of Hollin Creek"},
        {"agency": "State Patrol, District 6", "psap": "District 6 Communications", "role": "primary",
         "uri": URI["patrol"], "county_or_area": "District 6 highways"},
    ]


# ---------------------------------------------------------------------------------------------------- callback desk
CALLBACK_COLS = ["task_id", "line", "created", "call_ref", "callback_number", "first_dial", "dial_attempts", "result",
                 "closed"]


def callback_rows(W):
    rows = []
    for n, task in enumerate(sorted(W.cb_tasks, key=lambda t: t["created"]), start=1):
        if task["line"] == "911":
            i = task["opener"]
            ref = W.call_id[i]
            num = cb_token(int(W.caller[i])).upper()
        else:
            a = W.admin[task["opener"]]
            ref = W.admin_id[task["opener"]]
            num = K.token("admincbn", a[4], n=12).upper()
        rows.append({"task_id": "CB26-%06d" % n, "line": task["line"],
                     "created": K.local_str(task["created"], "%Y-%m-%d %H:%M:%S"), "call_ref": ref,
                     "callback_number": num,
                     "first_dial": K.local_str(task["first_dial"], "%Y-%m-%d %H:%M:%S") if task["first_dial"] else "",
                     "dial_attempts": task["attempts"], "result": task["result"],
                     "closed": K.local_str(task["closed"], "%Y-%m-%d %H:%M:%S")})
    return rows


# ---------------------------------------------------------------------------------------------------- admin line
ADMIN_COLS = ["call_id", "presented", "answered", "ended", "disposition", "position", "caller_ref"]


def admin_ids(W):
    ids, seq = [], {}
    for a in W.admin:
        d = K.to_local(a[0]).date()
        seq[d] = seq.get(d, 0) + 1
        ids.append("ADM-%s-%04d" % (d.strftime("%y%m%d"), seq[d]))
    W.admin_id = ids


def admin_rows(W):
    rows = []
    for j, a in enumerate(W.admin):
        ts, w, ab, serv, num = a
        if not (FY26[0] <= ts < FY26[1]):
            continue
        r = {"call_id": W.admin_id[j], "presented": K.local_str(ts, "%Y-%m-%d %H:%M:%S"),
             "caller_ref": K.token("admincbn", num, n=12).upper()}
        if ab:
            r["disposition"] = "abandoned"
            r["ended"] = K.local_str(ts + w, "%Y-%m-%d %H:%M:%S")
        else:
            r["disposition"] = "answered"
            r["answered"] = K.local_str(ts + w, "%Y-%m-%d %H:%M:%S")
            r["ended"] = K.local_str(ts + w + serv, "%Y-%m-%d %H:%M:%S")
            r["position"] = "ADM%d" % (1 + num % 2)
        rows.append(r)
    return rows


# ---------------------------------------------------------------------------------------------------- CAD
CAD_COLS = ["incident_no", "call_ref", "incident_type", "priority", "created", "first_unit_dispatched", "units"]


def cad_rows(W):
    rows = []
    for n, (i, typ, pri, created, disp, units) in enumerate(sorted(W.cad, key=lambda x: x[3]), start=1):
        rows.append({"incident_no": "TC%s-%05d" % (K.to_local(created).strftime("%y"), n), "call_ref": W.call_id[i],
                     "incident_type": typ, "priority": pri,
                     "created": K.local_str(created, "%Y-%m-%d %H:%M:%S"),
                     "first_unit_dispatched": K.local_str(disp, "%Y-%m-%d %H:%M:%S"), "units": units})
    return rows
