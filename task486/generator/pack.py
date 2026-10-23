"""The pack's source files, written from the world as each system exports them: the four Continuums' HMIS client,
enrollment, exit and services files (stacked by the Partnership's warehouse, each vendor's identifiers and date habits
kept), the coalition's comparable-database workbook, the clinic's encounter extract, the outreach app's contacts, the
linkage unit's pair file, the project register, and the 2026 point-in-time count and housing inventory."""
import collections
import csv
import datetime as dt
import json

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import sim as S
import world as W

FILES = {
    "client": "hmis_client_fy2025_fy2026.csv",
    "enrollment": "hmis_enrollment_fy2025_fy2026.csv",
    "exit": "hmis_exit_fy2025_fy2026.csv",
    "services": "hmis_services_fy2025_fy2026.csv",
    "dvc": "dvc_comparable_db_export.xlsx",
    "vsm": "wsh_hch_encounters_fy2025_fy2026.csv",
    "hot": "hot_field_app_contacts.jsonl",
    "pairs": "sdlu_linkage_pairs_run_20261008.csv",
    "note": "sdlu_record_linkage_method_note_v3.pdf",
    "policy": "regional_fund_policy_RF-2027.docx",
    "guide": "partnership_extract_guide.txt",
    "register": "partnership_project_register.xlsx",
    "pit": "pit_2026_counts_by_coc.csv",
    "hic": "hic_2026_inventory.xlsx",
    "inventory": "data_inventory.csv",
}
SITE_COC = {"WSH-01": "HAL", "WSH-02": "HAL", "WSH-05": "HAL", "WSH-03": "MEL", "WSH-04": "OND", "WSH-MP": "PYR"}
SITE_NAME = {"WSH-01": "Wayfarer Street Health, Fourth Street clinic", "WSH-02": "Wayfarer Street Health, "
             "Harbor Street clinic (in Harbor Street Family Shelter)", "WSH-05": "Wayfarer Street Health, Riverside "
             "clinic", "WSH-03": "Wayfarer Street Health, Melbray clinic", "WSH-04": "Wayfarer Street Health, Ondrava "
             "clinic", "WSH-MP": "Wayfarer Street Health, mobile clinic (Pyrenna County days)"}


def _iso(d):
    return d.isoformat() if d else ""


class Keys:
    """Every source's own record keys, drawn once and stable for the build."""
    def __init__(self, world):
        rng = np.random.default_rng(W.SEED * 101 + 3)
        self.rec = {}
        used = set()
        for r in sorted(world.records, key=lambda r: (r["src"], r["pid"])):
            s = r["src"]
            while True:
                if s == "HMIS-HAL":
                    k = str(int(rng.integers(100000, 999999)))
                elif s == "HMIS-MEL":
                    k = "M-%05d" % int(rng.integers(10000, 99999))
                elif s == "HMIS-OND":
                    k = "%08x" % int(rng.integers(0x10000000, 0xFFFFFFFF))
                elif s == "HMIS-PYR":
                    k = str(int(rng.integers(20000, 79999)))
                elif s == "DVC":
                    k = "DV-%05d" % int(rng.integers(10000, 99999))
                elif s == "WSH":
                    k = str(int(rng.integers(3000000, 9999999)))
                else:
                    k = "C-%05d" % int(rng.integers(10000, 99999))
                if (s, k) not in used:
                    used.add((s, k))
                    break
            self.rec[(s, r["pid"])] = k


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        n = 0
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
            n += 1
    return n


# ------------------------------------------------------------------------------------------------ HMIS
CLIENT_COLS = ["PersonalID", "SourceCoC", "YearOfBirth", "DOBDataQuality", "NameDataQuality", "SSNDataQuality",
               "Woman", "Man", "NonBinary", "CulturallySpecific", "Transgender", "Questioning", "DifferentIdentity",
               "GenderNone", "AmIndAKNative", "Asian", "BlackAfAmerican", "HispanicLatinaeo", "MidEastNAfrican",
               "NativeHIPacific", "White", "RaceNone", "VeteranStatus", "DateCreated", "DateUpdated", "UserID",
               "ExportID"]
ENR_COLS = ["EnrollmentID", "PersonalID", "SourceCoC", "ProjectID", "EntryDate", "HouseholdID", "RelationshipToHoH",
            "LivingSituation", "DisablingCondition", "MoveInDate", "DateCreated", "DateUpdated", "ExportID"]
EXIT_COLS = ["ExitID", "EnrollmentID", "PersonalID", "SourceCoC", "ExitDate", "Destination", "DateCreated",
             "DateUpdated", "ExportID"]
SERV_COLS = ["ServicesID", "EnrollmentID", "PersonalID", "SourceCoC", "DateProvided", "RecordType", "TypeProvided",
             "DateCreated", "ExportID"]
EXPORT = {"HAL": "HAL-20261005-01", "MEL": "MEL-20261005-02", "OND": "OND-20261006-01", "PYR": "PYR-20261005-01"}


EXPORTED = {"HAL": dt.datetime(2026, 10, 5, 5, 40), "MEL": dt.datetime(2026, 10, 5, 6, 10),
            "OND": dt.datetime(2026, 10, 6, 5, 55), "PYR": dt.datetime(2026, 10, 5, 6, 25)}


def _ts(d, rng, lag=(0, 6), coc=None):
    """A record's created or updated stamp, never later than its Continuum's export."""
    t = dt.datetime(d.year, d.month, d.day, 8, 0) + dt.timedelta(days=int(rng.integers(*lag)),
                                                                 minutes=int(rng.integers(0, 600)))
    if coc in EXPORTED and t > EXPORTED[coc]:
        t = EXPORTED[coc] - dt.timedelta(hours=7, minutes=(t.minute * 7 + t.hour * 13) % 600)
        t = max(t, dt.datetime(d.year, d.month, d.day, 7, 0))
    return t.strftime("%m/%d/%Y %H:%M") if coc == "MEL" else t.strftime("%Y-%m-%d %H:%M:%S")


def _stamps(created_day, updated_day, rng, lag_c, lag_u, coc):
    """DateCreated and DateUpdated, the update never before the creation."""
    c, u = _ts(created_day, rng, lag_c, coc), _ts(updated_day, rng, lag_u, coc)
    fmt = "%m/%d/%Y %H:%M" if coc == "MEL" else "%Y-%m-%d %H:%M:%S"
    if dt.datetime.strptime(u, fmt) < dt.datetime.strptime(c, fmt):
        u = c
    return c, u


def _dd(d, coc):
    """A date as the Continuum's HMIS vendor exports it: Melbray's writes month/day/year, the others ISO."""
    if d is None:
        return ""
    return "%d/%d/%d" % (d.month, d.day, d.year) if coc == "MEL" else d.isoformat()


# Ondrava's vendor still exports the FY2022 destination list; the others the FY2024 list
DEST_FY2022 = {410: 10, 435: 20, 422: 22, 302: 2, 116: 16, 101: 1, 99: 99}


def client_rows(world, keys):
    rng = np.random.default_rng(W.SEED * 7 + 1)
    race = {}
    for p in world.people:
        race[p["pid"]] = "HispanicLatinaeo" if p["hisp"] else str(rng.choice(
            ["White", "BlackAfAmerican", "AmIndAKNative", "Asian", "NativeHIPacific"], p=[0.58, 0.27, 0.07, 0.05,
                                                                                         0.03]))
    first_entry = {}
    for e in world.enrollments:
        k = ("HMIS-" + e["coc"], e["pid"])
        first_entry[k] = min(first_entry.get(k, e["entry"]), e["entry"])
    vet = {p["pid"]: (p["role"] != "child" and rng.random() < 0.08) for p in world.people}
    out = []
    for r in sorted(world.records, key=lambda r: (r["src"], keys.rec[(r["src"], r["pid"])])):
        if not r["src"].startswith("HMIS"):
            continue
        p = world.people[r["pid"]]
        coc = r["src"][5:]
        created = first_entry[(r["src"], r["pid"])]
        ssnq = (1 if rng.random() < 0.7 else 2) if r["ssn"] is not None else int(rng.choice([8, 9, 99],
                                                                                           p=[0.3, 0.2, 0.5]))
        g = [1 if p["sex"] == "F" else 0, 1 if p["sex"] == "M" else 0, 0, 0, 0, 0, 0, ""]
        rc = [1 if race[r["pid"]] == c else 0 for c in ("AmIndAKNative", "Asian", "BlackAfAmerican",
                                                        "HispanicLatinaeo", "MidEastNAfrican", "NativeHIPacific",
                                                        "White")] + [""]
        veteran = 99 if p["role"] == "child" else (1 if vet[r["pid"]] else 0)
        out.append([keys.rec[(r["src"], r["pid"])], coc, r["by"], 1 if r["full"] else 2,
                    1 if r["fn"] == p["fn"] else 2, ssnq] + g + rc + [veteran] +
                   list(_stamps(created, created, rng, (0, 6), (0, 200), coc)) +
                   ["U%03d" % int(rng.integers(1, 80)), EXPORT[coc]])
    return out


def enrollment_rows(world, keys):
    rng = np.random.default_rng(W.SEED * 7 + 2)
    out, exits, servs = [], [], []
    eid_key = {}
    for e in sorted(world.enrollments, key=lambda e: (e["coc"], e["entry"], e["eid"])):
        coc = e["coc"]
        pk = keys.rec[("HMIS-" + coc, e["pid"])]
        if coc == "MEL":
            ek = "E-%07d" % e["eid"]
        elif coc == "OND":
            ek = "%08x" % ((e["eid"] * 2654435761) % 0xFFFFFFFF)
        else:
            ek = str(e["eid"])
        eid_key[e["eid"]] = ek
        mi = e["move_in"] if e["rel"] == 1 else world.member_move_in.get(e["eid"])
        living = int(rng.choice([116, 101, 118, 215, 435, 302], p=[0.42, 0.24, 0.14, 0.08, 0.06, 0.06]))
        dis = 1 if rng.random() < 0.38 else 0
        out.append([ek, pk, coc, e["project"], _dd(e["entry"], coc), e["hh_id"], e["rel"], living, dis, _dd(mi, coc)] +
                   list(_stamps(e["entry"], e["exit"] or e["entry"], rng, (0, 6), (0, 12), coc)) + [EXPORT[coc]])
        if e["exit"] is not None:
            dest = int(rng.choice([410, 435, 422, 302, 116, 101, 99], p=[0.2, 0.16, 0.12, 0.1, 0.14, 0.12, 0.16]))
            if coc == "OND":
                dest = DEST_FY2022[dest]
            exits.append(["X%07d" % (e["eid"] % 10000000), ek, pk, coc, _dd(e["exit"], coc), dest] +
                         list(_stamps(e["exit"], e["exit"], rng, (0, 6), (0, 9), coc)) + [EXPORT[coc]])
    sid = 7000000
    for n in sorted(world.bed_nights, key=lambda n: (n["date"], n["eid"])):
        sid += 1 + int(rng.integers(0, 3))
        servs.append(["S%08d" % sid, eid_key[n["eid"]], keys.rec[("HMIS-" + n["coc"], n["pid"])], n["coc"],
                      _dd(n["date"], n["coc"]), 200, 200, _ts(n["date"], rng, (0, 2), coc=n["coc"]), EXPORT[n["coc"]]])
    return out, exits, servs


# ------------------------------------------------------------------------------------------------ other sources
def dvc_workbook(path, world, keys):
    rng = np.random.default_rng(W.SEED * 7 + 3)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Clients"
    ws.append(["ClientKey", "BirthYear", "Gender", "RaceCode", "Veteran", "CreatedOn"])
    first = {}
    for s in world.dv_stays:
        first[s["pid"]] = min(first.get(s["pid"], s["start"]), s["start"])
    for r in sorted((r for r in world.records if r["src"] == "DVC"), key=lambda r: keys.rec[("DVC", r["pid"])]):
        p = world.people[r["pid"]]
        ws.append([keys.rec[("DVC", r["pid"])], r["by"], {"F": "Female", "M": "Male"}[p["sex"]],
                   "H" if p["hisp"] else str(rng.choice(["W", "B", "I", "A", "P"], p=[0.6, 0.25, 0.08, 0.05, 0.02])),
                   None if p["role"] == "child" else ("N" if rng.random() < 0.96 else "Y"),
                   dt.datetime.combine(first[r["pid"]], dt.time(10, int(rng.integers(0, 59))))])
    st = wb.create_sheet("Stays")
    st.append(["StayID", "ClientKey", "Program", "StayStart", "StayEnd"])
    progs = ["Hearthstone Emergency Shelter", "Haven House", "Bridges Transitional Program"]
    for k, s in enumerate(sorted(world.dv_stays, key=lambda s: (s["start"], s["pid"]))):
        end = s["end"] if s["end"] <= W.PULL - dt.timedelta(days=10) else None
        st.append(["ST-%05d" % (20000 + 3 * k), keys.rec[("DVC", s["pid"])], progs[s["pid"] % 3], s["start"], end])
    for w_ in (ws, st):
        for c in w_[1]:
            c.font = Font(bold=True)
        w_.freeze_panes = "A2"
    for row in st.iter_rows(min_row=2):
        for c in row[3:5]:
            c.number_format = "m/d/yyyy"
    for row in ws.iter_rows(min_row=2):
        row[5].number_format = "m/d/yyyy h:mm"
    wb.save(path)
    return ws.max_row - 1 + st.max_row - 1


def vsm_rows(world, keys):
    rng = np.random.default_rng(W.SEED * 7 + 4)
    out = []
    n = 4100000
    visit = ["Medical", "Medical", "Medical", "Behavioral health", "Dental", "Enabling services"]
    for e in sorted(world.encounters, key=lambda e: (e["date"], e["pid"])):
        n += 1 + int(rng.integers(0, 4))
        p = world.people[e["pid"]]
        out.append(["V%08d" % n, keys.rec[("WSH", e["pid"])], e["date"].strftime("%m/%d/%Y"), e["site"], e["status"],
                    visit[int(rng.integers(len(visit)))], p["by"], p["sex"]])
    return out


def _pacific_offset(t):
    """Pacific time: daylight time from 2:00 on the second Sunday of March to 2:00 on the first Sunday of
    November."""
    y = t.year
    mar = dt.date(y, 3, 1)
    start = dt.datetime.combine(mar + dt.timedelta(days=(6 - mar.weekday()) % 7 + 7), dt.time(2, 0))
    nov = dt.date(y, 11, 1)
    end = dt.datetime.combine(nov + dt.timedelta(days=(6 - nov.weekday()) % 7), dt.time(2, 0))
    return "-07:00" if start <= t < end else "-08:00"


def hot_lines(world, keys):
    rng = np.random.default_rng(W.SEED * 7 + 5)
    rec = {r["pid"]: r for r in world.records if r["src"] == "HOT"}
    lines = []
    for k, c in enumerate(sorted(world.contacts, key=lambda c: (c["date"], c["minute"], c["pid"]))):
        p = world.people[c["pid"]]
        t = dt.datetime.combine(c["date"], dt.time(c["minute"] // 60, c["minute"] % 60))
        age = c["date"].year - p["by"] - (1 if (c["date"].month, c["date"].day) < (p["bm"], p["bd"]) else 0)
        r = rec[c["pid"]]
        line = {"contact_id": "HC-%06d" % (310000 + 7 * k), "client_key": keys.rec[("HOT", c["pid"])],
                "contact_time": t.strftime("%Y-%m-%dT%H:%M:00") + _pacific_offset(t),
                "zone": "Z%02d" % (1 + (c["pid"] * 7 + k) % 14),
                "engagement": str(rng.choice(["engaged", "engaged", "declined", "not found"])),
                "reported_age": int(age), "birth_year": r["by"], "dob_on_file": bool(r["full"])}
        lines.append(line)
    return lines


def pair_rows(world, keys):
    out = []
    n = 0
    for i, j, sc, codes in world.pairs:
        if sc < 4.0:
            continue
        a, b = world.records[i], world.records[j]
        if (W.SOURCES.index(a["src"]), keys.rec[(a["src"], a["pid"])]) > (W.SOURCES.index(b["src"]),
                                                                          keys.rec[(b["src"], b["pid"])]):
            a, b = b, a
        out.append([a["src"], keys.rec[(a["src"], a["pid"])], b["src"], keys.rec[(b["src"], b["pid"])], codes["fn"],
                    codes["ln"], codes["by"], codes["bm"], codes["bd"], codes["sex"], codes["ssn"], "%.1f" % sc,
                    "LINK" if sc >= W.THRESHOLD else "NONLINK"])
    out.sort(key=lambda r: (W.SOURCES.index(r[0]), r[1], W.SOURCES.index(r[2]), r[3]))
    rows = []
    for k, r in enumerate(out):
        rows.append(["P%07d" % (k + 1), "SDLU-20261008-CV"] + r)
    return rows


PAIR_COLS = ["pair_id", "run_id", "source_a", "record_a", "source_b", "record_b", "agr_first_name", "agr_surname",
             "agr_birth_year", "agr_birth_month", "agr_birth_day", "agr_sex", "agr_ssn4", "score", "finding"]
VSM_COLS = ["EncounterID", "PatientKey", "EncounterDate", "Site", "HousingStatus", "VisitType", "PatientBirthYear",
            "PatientSex"]
