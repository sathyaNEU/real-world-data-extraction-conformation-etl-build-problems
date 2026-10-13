"""Write the pack under target/: the simulated world through the records layer, then the documents, the dictionary and
the manifest."""
import csv
import json
import os
import random
import shutil
from datetime import date, timedelta

import docs
import params as P
import records as R
import sim
import world as W

FILES = {
    "log": "ncp_elr_message_log_2022-10_2026-10.csv",
    "extract": "ncp_enteric_case_extract_2022-2026.csv",
    "incidents": "ncp_interface_incident_log_2022-2026.csv",
    "feeds": "ncp_feed_register.xlsx",
    "codes": "ncp_condition_codes_2025.csv",
    "register": "cc_investigation_register_2021-2026.xlsx",
    "followup": "cc_contact_followup_2021-2026.csv",
    "att_a": "cc_attendance_signin_export.csv",
    "att_b": "cc_attendance_daily_roll.xlsx",
    "att_c": "cc_attendance_portal_export.json",
    "bookings": "cc_room_bookings.csv",
    "standard": "CD-ST-07_laboratory_feed_sla_lateness.docx",
    "guideline": "GL-CD-11_enteric_ecec_response_guideline.pdf",
    "release": "ncp_4-2_release_notes_sla_alerts.pdf",
    "dictionary": "data_dictionary.xlsx",
    "turnaround": "lab_turnaround_returns_2025-26.csv",
    "services": "ecec_services_register.csv",
    "manifest": "export_manifest.csv",
}
DISTRACTORS = ["codes", "turnaround", "services"]


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


LOG_COLS = ["msg_control_id", "received_utc", "sending_facility", "msh_datetime", "accession_no", "patient_ref",
            "specimen_collected", "test_code", "result_status", "result_text", "authorised_at", "condition_code",
            "ncp_case_no"]


def code_rows():
    rows = []
    for k, (name, legacy, new, _n, _p, _m, group) in R.CONDITIONS.items():
        rows.append([name, legacy, new, {"RES": "Respiratory", "VPD": "Vaccine preventable", "STI": "Sexually transmissible"
                     " and blood-borne", "ENT": "Enteric", "ARB": "Vector-borne and zoonotic"}[group],
                     "Y" if k in R.URGENT else ""])
    rows.sort(key=lambda r: r[0])
    return ["condition", "code_to_2025_06_30", "code_from_2025_07_01", "group", "urgent_childcare_list"], rows


def turnaround_rows():
    r = random.Random("%d|turnaround" % P.REC_SEED)
    groups = [("Enteric PCR", 22, 0.25), ("Enteric culture", 54, 0.2), ("Respiratory PCR", 14, 0.3), ("Serology", 30, 0.25)]
    base = {"CRBH": 0.9, "LPG": 1.0, "HDN": 1.08, "KES": 1.15, "HPS": 1.12, "SERL": 1.6}
    vol = {"CRBH": 1.0, "LPG": 1.7, "HDN": 1.1, "KES": 0.45, "HPS": 0.5, "SERL": 0.1}
    rows = []
    for f in P.FEEDS:
        for q, label in enumerate(["2025-Q4", "2026-Q1", "2026-Q2", "2026-Q3"]):
            for g, med, sd in groups:
                if f == "SERL" and g in ("Respiratory PCR",):
                    continue
                n = int(r.gauss(3800, 500) * vol[f] * (1.6 if g == "Respiratory PCR" and q == 3 else 1.0))
                m = med * base[f] * (1 + r.gauss(0, 0.06))
                rows.append([W.FEED[f]["name"], label, g, n, "%.1f" % m, "%.1f" % (m * (1.9 + r.uniform(-0.15, 0.25)))])
    return ["laboratory", "quarter", "test_group", "specimens", "median_hours_collection_to_authorisation",
            "p90_hours_collection_to_authorisation"], rows


def service_rows(world):
    rows = []
    for c in sorted(world.centres, key=lambda x: x["sid"]):
        rooms = "; ".join("%s %d" % (rm["room"], rm["places"]) for rm in c["rooms"])
        rows.append([c["sid"], sum(rm["places"] for rm in c["rooms"]), rooms, "%s-%s" % (R.hhmm(c["opens"]), R.hhmm(c["closes"])),
                     "Monday to Friday"])
    return ["service_id", "approved_places", "rooms_and_places", "opening_hours", "days"], rows


def portal_json(data):
    exports = []
    for inv, recs in data:
        exports.append({
            "investigation": inv.iid, "service": inv.centre["sid"], "room": inv.room["room"],
            "from": inv.ex_from.isoformat(), "to": inv.ex_to.isoformat(),
            "records": [{"attendee_id": pid, "attendee_type": role, "signed_in": R.local_iso(d, a),
                         "signed_out": R.local_iso(d, b)} for d, pid, role, a, b in recs]})
    return {"export": "Room attendance for public health investigations", "requested_by": W.UNIT, "exports": exports}


DICT_FILES = [
    ("ncp_elr_message_log_2022-10_2026-10.csv", "Every message the Notifiable Conditions Platform accepted from the six "
     "laboratory feeds for a resident of the district, 1 October 2022 to 31 October 2026, all notifiable conditions except "
     "COVID-19 (which reaches the platform through the national results gateway). A message carries one laboratory report: "
     "one test's result on one specimen, as the laboratory authorised it."),
    ("ncp_enteric_case_extract_2022-2026.csv", "The enteric team's case extract: one row per case of an enteric condition "
     "the platform holds for the district, opened 1 October 2022 to 31 October 2026."),
    ("ncp_interface_incident_log_2022-2026.csv", "The NCP interface team's incident log for the district's feeds."),
    ("ncp_feed_register.xlsx", "The NCP feed register: the district's six laboratory feeds and their sending facility codes."),
    ("ncp_condition_codes_2025.csv", "The platform's condition codes before and after the 2025 code set."),
    ("cc_investigation_register_2021-2026.xlsx", "The unit's childcare investigation register: one row per childcare "
     "investigation opened since July 2021."),
    ("cc_contact_followup_2021-2026.csv", "The contact follow-up of every childcare investigation: one row per room contact."),
    ("cc_attendance_signin_export.csv", "Room attendance supplied by centres whose software exports a sign-in log, one "
     "export per investigation."),
    ("cc_attendance_daily_roll.xlsx", "Room attendance supplied by centres whose software exports a daily roll, one export "
     "per investigation."),
    ("cc_attendance_portal_export.json", "Room attendance supplied by centres on the provider portal, one export per "
     "investigation."),
    ("cc_room_bookings.csv", "The booked days and hours of every child, and the rostered days and shifts of every educator, "
     "in each investigated room, as the centre supplied them."),
    ("CD-ST-07_laboratory_feed_sla_lateness.docx", "The unit's standard for setting each feed's SLA lateness."),
    ("GL-CD-11_enteric_ecec_response_guideline.pdf", "The unit's guideline for enteric cases in early childhood education and care."),
    ("ncp_4-2_release_notes_sla_alerts.pdf", "NCP release 4.2 release notes on per-feed SLA alerts."),
    ("lab_turnaround_returns_2025-26.csv", "The laboratories' quarterly turnaround returns, October 2025 to September 2026."),
    ("ecec_services_register.csv", "The long day care services in the district with their approved places."),
    ("export_manifest.csv", "What each file is, where it came from and when it was extracted."),
]
DICT_FIELDS = [
    ("ncp_elr_message_log", "msg_control_id", "The message control id the sending system gave the message (MSH-10)."),
    ("ncp_elr_message_log", "received_utc", "When the platform accepted the message, UTC."),
    ("ncp_elr_message_log", "sending_facility", "The sending facility code (MSH-4). The feed register maps codes to feeds."),
    ("ncp_elr_message_log", "msh_datetime", "The message date and time as the sending system wrote it (MSH-7), "
     "YYYYMMDDHHMMSS with its UTC offset."),
    ("ncp_elr_message_log", "accession_no", "The laboratory's filler order number for the specimen (OBR-3), as received."),
    ("ncp_elr_message_log", "patient_ref", "The laboratory's patient identifier (PID-3). Each laboratory numbers its own "
     "patients."),
    ("ncp_elr_message_log", "specimen_collected", "The specimen collection date (SPM-17)."),
    ("ncp_elr_message_log", "test_code", "The laboratory's test code (OBX-3)."),
    ("ncp_elr_message_log", "result_status", "The report's status (OBR-25): P preliminary, F final, C corrected."),
    ("ncp_elr_message_log", "result_text", "The result as reported."),
    ("ncp_elr_message_log", "authorised_at", "The date and time the laboratory authorised the report (OBR-22), "
     "YYYYMMDDHHMMSS with its UTC offset."),
    ("ncp_elr_message_log", "condition_code", "The platform's condition code for the result, mapped on receipt with the code "
     "set in force at receipt (ncp_condition_codes_2025.csv)."),
    ("ncp_elr_message_log", "ncp_case_no", "The case the platform matched the report to."),
    ("ncp_enteric_case_extract", "ncp_case_no", "The platform's case number."),
    ("ncp_enteric_case_extract", "condition", "The notifiable condition."),
    ("ncp_enteric_case_extract", "case_status", "Confirmed, Probable, or Merged (the case was found to be a duplicate and "
     "merged into the case in merged_into)."),
    ("ncp_enteric_case_extract", "merged_into", "For a merged case, the case it was merged into."),
    ("ncp_enteric_case_extract", "onset_date", "Onset of symptoms, where known."),
    ("ncp_enteric_case_extract", "notified_date", "The date the case was opened on the platform, New South Wales time."),
    ("ncp_enteric_case_extract", "notifying_facility", "The sending facility of the report the case was opened from; blank "
     "for a case the unit entered."),
    ("ncp_enteric_case_extract", "age_group", "Age group at onset."),
    ("ncp_enteric_case_extract", "sex", "Sex as recorded."),
    ("ncp_enteric_case_extract", "setting", "Childcare attendee, childcare staff, food handler or health care worker, where "
     "the case is one."),
    ("ncp_interface_incident_log", "incident_ref", "The incident reference."),
    ("ncp_interface_incident_log", "sending_facility", "The feed's sending facility code; NCP for a platform-wide change."),
    ("ncp_interface_incident_log", "category", "Interface outage, disaster recovery failover, planned maintenance or change."),
    ("ncp_interface_incident_log", "raised_by", "Who raised the incident."),
    ("ncp_interface_incident_log", "opened_utc", "When the incident was opened, UTC."),
    ("ncp_interface_incident_log", "resolved_utc", "When the incident was resolved, UTC."),
    ("ncp_interface_incident_log", "summary", "The interface team's summary."),
    ("ncp_condition_codes_2025", "code_to_2025_06_30", "The condition's code before the 2025 code set."),
    ("ncp_condition_codes_2025", "code_from_2025_07_01", "The condition's code in the 2025 code set."),
    ("ncp_condition_codes_2025", "urgent_childcare_list", "Y for the conditions the unit acts on urgently in a childcare "
     "attendee or educator."),
    ("cc_investigation_register", "Investigation", "The investigation's reference."),
    ("cc_investigation_register", "NCP case", "The index case's platform case number."),
    ("cc_investigation_register", "Index person no.", "The index case's attendee or educator number in the centre's "
     "attendance export."),
    ("cc_investigation_register", "Infectious attendance from / to", "The first and last days the index case attended from "
     "onset to the exclusion."),
    ("cc_investigation_register", "Notifying laboratory", "The feed whose report opened the investigation."),
    ("cc_investigation_register", "Result authorised", "The laboratory's authorisation of that report, New South Wales time."),
    ("cc_investigation_register", "Notification received", "The platform's acceptance of that report, New South Wales time."),
    ("cc_investigation_register", "Exclusion call", "The duty officer's call to the family and the centre, New South Wales "
     "time."),
    ("cc_investigation_register", "Follow-up to", "The last day of the room's follow-up."),
    ("cc_investigation_register", "Status", "Open or Closed (follow-up complete and results in)."),
    ("cc_contact_followup", "investigation_id", "The investigation."),
    ("cc_contact_followup", "contact_person_no", "The contact's attendee or educator number in the centre's export."),
    ("cc_contact_followup", "contact_type", "Child or Educator."),
    ("cc_contact_followup", "ill", "Y if the contact had diarrhoea from 21 days before the index case's onset to the end of "
     "the follow-up."),
    ("cc_contact_followup", "onset_date", "The contact's onset date."),
    ("cc_contact_followup", "onset_approximate", "Y where the family could give the onset only approximately."),
    ("cc_contact_followup", "specimen_collected", "The date of the contact's positive specimen."),
    ("cc_contact_followup", "result", "Positive, or Not tested."),
    ("cc_contact_followup", "case_status", "Confirmed or Probable (GL-CD-11 section 2)."),
    ("cc_contact_followup", "ncp_case_no", "The contact's case on the platform."),
    ("cc_attendance_signin_export", "person_type", "C child, S staff."),
    ("cc_attendance_signin_export", "date / sign_in / sign_out", "Attendance date (DD-Mon-YYYY) and sign-in and sign-out "
     "times (24-hour)."),
    ("cc_attendance_daily_roll", "In / Out", "Sign-in and sign-out times (12-hour)."),
    ("cc_attendance_portal_export", "signed_in / signed_out", "Local date and time of sign-in and sign-out."),
    ("cc_room_bookings", "booked_days / booked_from / booked_to", "The weekdays and hours a child is booked, or an educator "
     "rostered, in the room."),
    ("all attendance exports", "person numbers", "Each centre's software numbers its own attendees and educators; a casual "
     "educator covering an absence appears under their own number."),
]
DICT_NOTES = [
    "The unit dates and times its own records in New South Wales time, and a date it reports is a New South Wales date.",
    "Platform times ending in Z are UTC. HL7 date-times (MSH-7, OBR-22) carry the sending system's UTC offset.",
    "The laboratories: Coast and Ranges Base Hospital Laboratory (public pathology), Larkspur Pathology, Halden Pathology, "
    "Kestrel Pathology (Queensland), Highfield Pathology Services (a Larkspur laboratory since 1 March 2024) and the State "
    "Enteric Reference Laboratory.",
    "Owner of this dictionary: %s, surveillance data officer." % W.PEOPLE["interface"],
]
MANIFEST = [
    ("log", "NCP message store, district ELR extract", "2026-11-13", W.PEOPLE["interface"]),
    ("extract", "NCP case management, enteric case extract", "2026-11-13", W.PEOPLE["interface"]),
    ("incidents", "NCP interface team incident log", "2026-11-12", "NCP interface team"),
    ("feeds", "NCP feed register", "2026-11-13", W.PEOPLE["interface"]),
    ("codes", "NCP condition code set 2025", "2025-06-20", "NCP platform services"),
    ("register", "Unit investigation register", "2026-11-13", W.PEOPLE["manager"]),
    ("followup", "Unit contact follow-up", "2026-11-13", W.PEOPLE["manager"]),
    ("att_a", "Centres' attendance exports (sign-in log)", "2026-11-13", W.PEOPLE["manager"]),
    ("att_b", "Centres' attendance exports (daily roll)", "2026-11-13", W.PEOPLE["manager"]),
    ("att_c", "Centres' attendance exports (provider portal)", "2026-11-13", W.PEOPLE["manager"]),
    ("bookings", "Centres' bookings and rosters as supplied", "2026-11-13", W.PEOPLE["manager"]),
    ("standard", "Unit standard CD-ST-07, version 1.0", "2026-11-06", W.PEOPLE["manager"]),
    ("guideline", "Unit guideline GL-CD-11, version 3.1", "2024-05-20", W.PEOPLE["manager"]),
    ("release", "NCP 4.2 release notes", "2026-10-14", "NCP platform services"),
    ("dictionary", "Data dictionary for these files", "2026-11-13", W.PEOPLE["interface"]),
    ("turnaround", "Laboratories' quarterly turnaround returns", "2026-10-28", W.PEOPLE["interface"]),
    ("services", "Early childhood education and care services in the district", "2026-07-01", W.PEOPLE["manager"]),
]


def build(target, world=None, plat=None):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    world = world or sim.World().run()
    inv = R.Investigations(world) if plat is None else plat.inv
    plat = plat or R.Platform(world, inv)
    p = lambda k: os.path.join(target, FILES[k])
    counts = {}
    counts["log"] = write_csv(p("log"), LOG_COLS, [[m[c] for c in LOG_COLS] for m in plat.msgs])
    counts["extract"] = write_csv(p("extract"), *plat.case_extract())
    counts["incidents"] = write_csv(p("incidents"), *plat.incident_log())
    docs.feed_register(p("feeds"))
    counts["codes"] = write_csv(p("codes"), *code_rows())
    reg = inv.register()
    docs.register(p("register"), reg)
    counts["register"] = len(reg)
    counts["followup"] = write_csv(p("followup"), *inv.followup())
    a_rows = []
    for i, recs in inv.attendance("A"):
        for d, pid, role, a, b in recs:
            a_rows.append([i.iid, i.centre["sid"], i.room["room"], pid, "S" if role == "educator" else "C", R.dmy(d),
                           R.hhmm(a), R.hhmm(b)])
    counts["att_a"] = write_csv(p("att_a"), ["investigation", "service_id", "room", "person_no", "person_type", "date",
                                             "sign_in", "sign_out"], a_rows)
    counts["att_b"] = docs.daily_roll(p("att_b"), inv.attendance("B"))
    data_c = inv.attendance("C")
    with open(p("att_c"), "w", encoding="utf-8") as fh:
        json.dump(portal_json(data_c), fh, indent=1)
        fh.write("\n")
    counts["att_c"] = sum(len(recs) for _i, recs in data_c)
    counts["bookings"] = write_csv(p("bookings"), *inv.bookings())
    docs.standard(p("standard"))
    docs.guideline(p("guideline"))
    docs.release_notes(p("release"))
    docs.dictionary(p("dictionary"), [list(x) for x in DICT_FILES], [list(x) for x in DICT_FIELDS], DICT_NOTES)
    counts["turnaround"] = write_csv(p("turnaround"), *turnaround_rows())
    counts["services"] = write_csv(p("services"), *service_rows(world))
    man = []
    for k, src, when, owner in MANIFEST:
        man.append([FILES[k], dict(DICT_FILES).get(FILES[k], "Field definitions and conventions for these files."), src,
                    when, counts.get(k, ""), owner])
    write_csv(p("manifest"), ["file", "contents", "source", "extracted_or_issued", "rows", "owner"], man)
    return world, plat, counts
