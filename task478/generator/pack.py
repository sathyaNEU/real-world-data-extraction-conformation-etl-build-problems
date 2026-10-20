"""Write the records into the pack's tables, in each system's own layout: Kerbline's detections in district local
time, the telematics provider's traversals in UTC, the MMS work orders with US dates, the road inventory and its
crosswalk, the distractors."""
import csv
import datetime as dt
import io
import json

import world as W

FILES = {
    "detections": "kerbline_detections_2027-03.csv",
    "traversals": "fleet_camera_traversals_2027-03.csv",
    "review": "kerbline_qa_review_2027-03.xlsx",
    "register": "kerbline_unit_register.xlsx",
    "sessions": "kerbline_unit_sessions_2027-03.json",
    "inventory": "road_inventory_2026.csv",
    "crosswalk": "road_inventory_crosswalk_2025_2026.csv",
    "turnback": "route_turnback_notice_2027-03.pdf",
    "orders": "mms_cold_patch_orders_2027-03.csv",
    "program": "spring_patching_program_2027.pdf",
    "sow": "kerbline_pilot_scope_of_work.pdf",
    "dictionary": "tamsett_pilot_data_dictionary.pdf",
    "manifest": "export_manifest.csv",
    "pci": "pavement_condition_2026.csv",
    "winter": "winter_operations_2027-03.csv",
    "sections": "maintenance_sections.csv",
}
DISTRACTORS = ["pavement_condition_2026.csv", "winter_operations_2027-03.csv"]

FUNC = {"FWY": "Other Freeway/Expressway", "ART": "Principal Arterial", "SUB": "Minor Arterial",
        "RUR": "Major Collector"}
GROUP_NAME = {"PATROL": "Section patrol", "FSP": "Freeway service patrol", "SWEEPER": "Street sweeper",
              "CREW": "District crew"}


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    n = 0
    for row in rows:
        w.writerow(["" if v is None else v for v in row])
        n += 1
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())
    return n


def iso_z(t):
    return t.astimezone(W.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def local_s(t):
    return W.local(t).strftime("%Y-%m-%d %H:%M:%S")


def us_local(t):
    return W.local(t).strftime("%m/%d/%Y %H:%M")


# ------------------------------------------------------------------------------------------------- tables
DET_COLS = ["detection_id", "defect_id", "unit_serial", "captured_local", "latitude", "longitude", "road_ref",
            "route", "road_mp", "defect_class", "severity", "confidence", "image_ref"]


def detection_rows(e):
    for x in e["detections"]:
        loc = W.local(x["t"])
        yield [x["det"], x["defect"], x["unit"], loc.strftime("%Y-%m-%d %H:%M:%S"), "%.6f" % x["lat"], "%.6f" % x["lon"],
               x["road_ref"], x["route"], None if x["road_mp"] is None else "%.3f" % x["road_mp"], x["cls"], x["sev"],
               "%.2f" % x["conf"],
               "kv/%s/%s/%s_%d.jpg" % (loc.strftime("%Y%m%d"), x["unit"][3:], loc.strftime("%H%M%S"), x["det"])]


TRAV_COLS = ["traversal_id", "vehicle_id", "segment_id", "direction", "enter_utc", "exit_utc"]


def traversal_rows(e):
    """The provider numbers traversals as it processes them (a few minutes after each leaves the segment); the
    12 to 13 March block it re-ran on 15 March took that day's numbers."""
    r = W.rng(40)
    items = []
    for t in e["trav"]:
        items.append((t["exit"] + dt.timedelta(seconds=int(r.integers(240, 1300))), t))
    base = dt.datetime(2027, 3, 15, 14, 2, tzinfo=W.UTC)
    for k, t in enumerate(sorted(e["replays"], key=lambda t: (t["enter"], t["veh"]))):
        items.append((base + dt.timedelta(seconds=k // 3), t))
    items.sort(key=lambda it: (it[0], it[1]["veh"], it[1]["enter"]))
    tid = 618004211
    rows = []
    for proc, t in items:
        tid += int(r.integers(1, 4))
        rows.append((t["veh"], t["enter"], tid, t))
    rows.sort(key=lambda x: (x[0], x[1], x[2]))
    for veh, enter, tid, t in rows:
        yield [tid, veh, t["seg"], t["dir"], iso_z(t["enter"]), iso_z(t["exit"])]


INV_COLS = ["segment_id", "route", "section", "begin_mp", "end_mp", "length_mi", "through_lanes", "functional_class",
            "jurisdiction"]


def inventory_rows(e):
    for s in sorted(e["segs"], key=lambda s: (s["route_num"], s["bmp"])):
        yield [s["seg"], s["route"], s["sec"], "%.3f" % s["bmp"], "%.3f" % s["emp"], "%.3f" % s["length"], s["lanes"],
               FUNC[s["cls"]], "STATE"]


XW_COLS = ["segment_id_2025", "route", "begin_mp_2025", "end_mp_2025", "segment_id_2026", "begin_mp_2026",
           "end_mp_2026", "change"]


def crosswalk_rows(e):
    out = []
    for x in e["seg25"]:
        if x["kind"] == "SAME":
            continue
        for ch, lo, hi in x["children"]:
            s = e["S"][ch]
            out.append([x["seg25"], x["route"], "%.3f" % x["bmp"], "%.3f" % x["emp"], ch, "%.3f" % s["bmp"],
                        "%.3f" % s["emp"], x["kind"]])
    out.sort(key=lambda row: (row[1], float(row[2])))
    return out


WO_COLS = ["wo_number", "task_line", "activity", "section", "route", "milepost", "ext_ref", "raised", "finished",
           "crew", "crew_size", "cold_mix_lb", "status"]


def order_rows(e):
    for x in e["wo_rows"]:
        yield ["WO-%d" % x["wo"], x["line"], "PCOLD", x["sec"], x["route"], "%.3f" % x["mp"], x["ref"], us_local(x["raised"]),
               None if x["finish"] is None else us_local(x["finish"]), x["crew"], x["crew_size"], x["lb"], x["status"]]


PCI_COLS = ["segment_id", "route", "begin_mp", "end_mp", "survey_date", "iri_in_per_mi", "rut_depth_in", "cracking_pct",
            "pci"]


def pci_rows(e):
    for x in sorted(e["pci"], key=lambda x: (x["route"], x["bmp"])):
        yield [x["seg"], x["route"], "%.3f" % x["bmp"], "%.3f" % x["emp"], x["date"].isoformat(), x["iri"],
               "%.2f" % x["rut"], "%.1f" % x["crack"], x["pci"]]


WINTER_COLS = ["section", "event_id", "start_date", "end_date", "plow_hours", "salt_tons", "brine_gallons",
               "freeze_thaw_cycles"]


def winter_rows(e):
    for x in e["winter"]:
        yield [x["sec"], x["event"], x["start"].isoformat(), x["end"].isoformat(), "%.1f" % x["plow_hrs"],
               "%.1f" % x["salt_t"], x["brine_gal"], x["ft_cycles"]]


YARDS = {401: ("Holloway Run", "Holloway Run yard, 2210 Mill Creek Rd"), 402: ("Fenwick Gap", "Fenwick Gap yard, 55 Depot St"),
         403: ("Carrow Point", "Carrow Point yard, 1180 Harbor Rd"), 404: ("Grisholt", "Grisholt yard, 47 Quarry Ln"),
         405: ("Marlpit", "Marlpit yard, 902 Kiln Rd"), 406: ("Kestrelton", "Kestrelton yard, 18 Station Rd"),
         407: ("Elmscourt", "Elmscourt yard, 3301 Foundry Ave"), 408: ("Halverton", "Halverton yard, 6 Ridge Rd"),
         409: ("Thistlebank", "Thistlebank yard, 740 Bank St"), 410: ("Oxbrae", "Oxbrae yard, 129 Ferry Rd"),
         411: ("Rushmead", "Rushmead yard, 2650 Canal St"), 412: ("Stonebeck", "Stonebeck yard, 311 Beck Rd"),
         413: ("Norvelle", "Norvelle yard, 88 Schoolhouse Rd"), 414: ("Pyke Hill", "Pyke Hill yard, 4415 Turnpike Rd")}


def section_rows(e):
    for no in sorted(YARDS):
        name, yard = YARDS[no]
        yield [no, name, yard, "Tamsett District"]


def sessions_json(e):
    units = []
    for v in sorted(e["veh"], key=lambda v: v["unit"]):
        ss = [s for s in e["sessions"] if s["unit"] == v["unit"] and not s.get("unclosed")]
        units.append({"unit_serial": v["unit"], "sessions": [
            {"session_id": "s-%d" % s["sid"], "start_utc": iso_z(s["start"]), "end_utc": iso_z(s["end"]),
             "frames": s["frames"], "upload_mb": s["mb"]} for s in ss]})
    doc = {"account": "Tamsett District pilot", "exported_utc": "2027-04-02T13:06:41Z",
           "range_utc": ["2027-02-15T00:00:00Z", "2027-04-02T00:00:00Z"], "units": units}
    return json.dumps(doc, indent=1, ensure_ascii=True) + "\n"


def review_rows(e):
    for x in e["review"]:
        yield [x["defect"], "pothole", x["route"], None if x["mp"] is None else round(x["mp"], 3),
               x["first"].astimezone(W.UTC).replace(tzinfo=None, microsecond=0), x["decision"], x["reason"] or None,
               x["reviewed"].astimezone(W.UTC).replace(tzinfo=None, microsecond=0), x["reviewer"]]


def register_rows(e):
    notes = {}
    for v in e["veh"]:
        if v["installed"] > dt.date(2027, 3, 1):
            notes[v["unit"]] = "Second delivery"
        if v["removed"] is not None:
            notes[v["unit"]] = "Removed for sweeper spring overhaul; returned to Kerbline"
    for v in sorted(e["veh"], key=lambda v: v["unit"]):
        yield [v["unit"], v["veh"], GROUP_NAME[v["group"]], v["desc"], v["home"], v["installed"], v["removed"],
               "Windshield, center", notes.get(v["unit"])]


def manifest_rows(n):
    return [
        [FILES["detections"], "Kerbline platform, detections export", "2027-04-02", "detections captured 1 to 31 March 2027",
         n["detections"], "captured_local is district local time"],
        [FILES["traversals"], "Fleet telematics provider, segment traversal export", "2027-04-02",
         "pilot vehicles, 28 February to 1 April 2027 (UTC)", n["traversals"], "state highway segments only"],
        [FILES["review"], "Kerbline platform, review module export", "2027-04-02", "pothole-class defects", n["review"], ""],
        [FILES["register"], "Kerbline install log", "2027-04-01", "pilot units", n["register"], ""],
        [FILES["sessions"], "Kerbline device API", "2027-04-02", "15 February to 1 April 2027 (UTC)", n["sessions"],
         "sessions"],
        [FILES["inventory"], "District road inventory", "2027-01-04", "state highway segments in the fourteen sections",
         n["inventory"], "2026 inventory release"],
        [FILES["crosswalk"], "District road inventory", "2027-01-04", "segments renumbered in the 2026 release",
         n["crosswalk"], ""],
        [FILES["orders"], "Maintenance management system", "2027-04-02", "activity PCOLD work orders raised in March 2027",
         n["orders"], ""],
        [FILES["pci"], "Pavement management section", "2026-11-30", "2026 condition survey", n["pci"], ""],
        [FILES["winter"], "Winter operations", "2027-04-01", "March 2027 storm events", n["winter"], ""],
        [FILES["sections"], "District Maintenance", "2027-01-04", "the district's maintenance sections", n["sections"], ""],
        [FILES["program"], "District Maintenance", "2027-04-06", "Spring Patching Program 2027", "", "document"],
        [FILES["sow"], "Kerbline Vision, Inc.", "2027-01-19", "pilot scope of work, purchase order 27-PO-0418", "",
         "document"],
        [FILES["turnback"], "City of Tamsett, Department of Public Works", "2027-03-01", "route turnback effective date",
         "", "document"],
        [FILES["dictionary"], "Maintenance Management Systems", "2027-04-03", "data notes for these extracts", "",
         "document"],
    ]
