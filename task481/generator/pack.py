"""task481 pack: the file names, the columns and the rows each shipped table carries."""
import csv
import datetime as dt
import io

import numpy as np

import asks as A
import bundle as B
import world as W

FILES = {
    "extract": "epd_nibrs_offense_extract_2024-10_to_2026-09.csv",
    "dictionary": "epd_nibrs_extract_dictionary.pdf",
    "ra_2021": "return_a_2021.xlsx",
    "ra_2022": "return_a_2022.xlsx",
    "ra_2023": "return_a_2023.xlsx",
    "ra_2024": "return_a_2024.xlsx",
    "dvu": "dvu_case_log_2021_2026.csv",
    "dvu_notes": "dvu_case_log_fields.txt",
    "method": "scorecard_crime_chapter_methods_2026.docx",
    "cert": "state_ucr_nibrs_certification_letter.pdf",
}

EXTRACT_COLS = ["incident_number", "report_datetime_utc", "incident_date", "incident_hour", "offense_seq",
                "offense_code", "attempt_complete", "location_code", "weapon_force_1", "victim_seq", "victim_type",
                "victim_age", "victim_sex", "injury_1", "relationship_1", "ucr_summary_class", "cleared_by",
                "clearance_date"]
DVU_COLS = ["case_no", "rms_incident", "report_date", "case_opened", "offense_category", "ucr_line", "nibrs_offense",
            "relationship", "victim_sex", "victim_age", "lethality_screen", "case_status"]


def write_csv(path, cols, rows, lineterminator="\r\n"):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=lineterminator)
    w.writerow(cols)
    n = 0
    for row in rows:
        w.writerow(["" if v is None else v for v in row])
        n += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return n


def utc_text(local_naive):
    return B.to_utc(local_naive).strftime("%Y-%m-%dT%H:%M:%SZ")


def in_extract(rep):
    return (dt.datetime(2024, 10, 1) <= rep <= dt.datetime(2026, 9, 30, 23, 59, 59))


def dual(rep):
    return dt.datetime(2024, 10, 1) <= rep < dt.datetime(2025, 1, 1)


def extract_rows(b):
    """One row per offense against each victim, incidents reported from 1 October 2024 to 30 September 2026 that
    the department has not deleted. The summary class is filled for the October to December 2024 reports."""
    r = np.random.default_rng(b.seed * 19 + 2)
    by_inc = {}
    for v in b.victims:
        by_inc.setdefault(v["iid"], []).append(v)
    out = []
    for iid, vs in by_inc.items():
        inc = b.inc[iid]
        rep = inc["reported"]
        if inc["unfounded"] or not in_extract(rep):
            continue
        codes = []
        for v in vs:
            if v["nibrs"] not in codes:
                codes.append(v["nibrs"])
        cleared = ""
        cdate = ""
        u = r.random()
        if u < 0.42:
            cleared = "A" if r.random() < 0.82 else "E"
            cd = rep + dt.timedelta(days=int(r.integers(0, 120)))
            if cd <= dt.datetime(2026, 10, 4):
                cdate = cd.strftime("%Y-%m-%d")
            else:
                cleared = ""
        for vseq, v in enumerate(vs, 1):
            if dual(rep):
                cls = "NS" if v["kind"] in ("rob_extra", "hom_extra") else v["line"]
            else:
                cls = ""
            out.append((rep, inc["number"], codes.index(v["nibrs"]) + 1, vseq, [
                inc["number"], utc_text(rep), inc["occurred"].strftime("%Y-%m-%d"), "%02d" % inc["occurred"].hour,
                codes.index(v["nibrs"]) + 1, v["nibrs"], "A" if (v["kind"] == "fire_miss" and r.random() < 0.2) else "C",
                inc["place"], v["weapon"], vseq, v["vtype"], v["age"] if v["vtype"] == "I" else "", v["sex"] if v["vtype"] == "I" else "",
                "" if v["nibrs"] in ("09A", "13C") else v["injury"], v["rel"] if v["vtype"] == "I" else "", cls,
                cleared, cdate]))
    for o in b.others:
        rep = o["reported"]
        if o["unfounded"] or not in_extract(rep):
            continue
        cls = (o["line"] or "P2") if dual(rep) else ""
        out.append((rep, o["number"], 1, 1, [
            o["number"], utc_text(rep), o["occurred"].strftime("%Y-%m-%d"), "%02d" % o["occurred"].hour, 1, o["code"],
            "C", o["place"], "", 1, o["vtype"], o["age"] if o["vtype"] == "I" else "", o["sex"], "", "", cls, "", ""]))
    out.sort(key=lambda t: (t[0], t[1], t[2], t[3]))
    return [t[4] for t in out]


def dvu_rows(b):
    """One row a domestic victim the unit received, January 2021 to September 2026."""
    r = np.random.default_rng(b.seed * 23 + 9)
    out = []
    n = {}
    for d in b.dvu:
        inc = d["inc"]
        rep = inc["reported"]
        if rep.year < 2021 or rep > dt.datetime(2026, 9, 30, 23, 59, 59):
            continue
        n[rep.year] = n.get(rep.year, 0) + 1
        opened = rep + dt.timedelta(days=int(r.integers(1, 11)))
        number = inc["number"]
        if inc.get("old_number"):
            number = inc["old_number"]
        new = rep >= dt.datetime(2024, 10, 1)
        if d["v"] is not None:
            v = d["v"]
            line = v["line"] if rep < dt.datetime(2025, 1, 1) else ""
            if v["kind"] == "dv_threat":
                cat = "Threats or stalking"
            elif line in ("4A", "4B", "4C", "4D") or (new and v["nibrs"] == "13A"):
                cat = "Assault - aggravated"
            else:
                cat = "Assault"
            rel = B.DVU_REL[v["rel"]]
            sex, age = v["sex"], v["age"]
            nibrs = v["nibrs"] if new else ""
        else:
            cat = {"90Z": "Protective order violation", "290": "Property damage", "220": "Burglary"}[d["kind"]]
            line = ("5A" if d["kind"] == "220" else "") if rep < dt.datetime(2025, 1, 1) else ""
            nibrs = d["kind"] if new else ""
            rel = B.DVU_REL[inc["rel"]]
            sex, age = inc["sex"], inc["age"]
        ipv = rel.startswith("Intimate")
        status = "UNFOUNDED" if inc["unfounded"] else (
            "OPEN" if rep > dt.datetime(2026, 7, 1) and r.random() < 0.6 else
            ("REFERRED TO PROSECUTOR" if r.random() < 0.35 else "CLOSED"))
        # a case the unit had not opened by the export carries no opening date
        opened_s = opened.strftime("%Y-%m-%d") if opened <= dt.datetime(2026, 10, 2, 23, 59) else ""
        out.append([("DVU-%d-%05d" % (rep.year, n[rep.year])), number, rep.strftime("%Y-%m-%d"), opened_s,
                    cat, line, nibrs, rel, sex, age, ("Y" if r.random() < 0.86 else "N") if ipv else "", status])
    return out


FILES.update({
    "state_table": "crime_in_the_state_2025_table8.pdf",
    "state_repo": "state_repository_download_ellsmere_13A_2025.csv",
    "gvr": "gvr_shooting_log_2023_2026.csv",
    "me": "medical_examiner_homicide_list_2023_2026.csv",
    "population": "census_population_estimates_ellsmere.csv",
    "cad": "epd_cad_assault_calls_2024_2025.csv",
})
STATE_COLS = ["state_record_id", "ori", "incident_number", "incident_date", "victim_seq", "offense_code", "victim_age",
              "victim_sex", "first_accepted_utc"]
GVR_COLS = ["gvr_id", "rms_number", "shot_datetime", "block", "inside_city", "victim_age", "victim_sex",
            "circumstance", "outcome", "entered", "analyst"]
ME_COLS = ["me_case", "date_of_injury", "injury_location", "date_of_death", "age", "sex", "cause", "manner"]
POP_COLS = ["vintage", "reference_date", "geography", "population"]
CAD_COLS = ["event_no", "created_utc", "call_type", "priority", "source", "disposition", "master_event"]


def state_rows(sf):
    out = []
    for k, (inc, seq, v, number, accepted) in enumerate(sf.snapshot, 1):
        out.append(["R%09d" % (418_200_000 + 37 * k), "XX0110100", number, inc["occurred"].strftime("%Y-%m-%d"), seq,
                    "13A", v["age"] if v["vtype"] == "I" else "", v["sex"],
                    B.to_utc(accepted).strftime("%Y-%m-%dT%H:%M:%SZ")])
    return out


def gvr_rows(sh, seed):
    r = np.random.default_rng(seed * 37 + 1)
    analysts = ("KMB", "DJT", "RPA", "LCS")
    out = []
    for row in sh.log:
        p = row["p"]
        if row["entered"].date() > dt.date(2026, 10, 1):      # entered after the export
            continue
        # the old database marked a shooting inside the city by the patrol beat, and the beats take in the township the
        # department patrols under contract; the records system the log moved into on 1 October 2024 marks it from the
        # address, names the municipality, and stores every time in UTC
        new = row["entered"] >= A.MIGRATION
        beat = p["township"] and not new
        inside = p["inside"] or beat
        shot = B.to_utc(p["at"]) if new else p["at"]
        out.append([row["gvr"], row["number"], shot.strftime("%Y-%m-%d %H:%M"),
                    p["block"] if inside else "%s (%s)" % (p["block"], p["town"]),
                    "Y" if inside else "N", p["age"], p["sex"], p["circ"], row["outcome"],
                    row["entered"].strftime("%Y-%m-%d"), analysts[int(r.integers(0, len(analysts)))]])
    return out


def me_rows(sh):
    out = []
    seq = {}
    for row in sh.me:
        p = row["p"]
        if p["death"].date() > dt.date(2026, 10, 6):          # after the list was drawn
            continue
        y = p["death"].year
        seq[y] = seq.get(y, 0) + 1
        if p.get("block") and p.get("inside", True):
            place = p["block"] + ", ELLSMERE"
        elif p.get("block"):
            place = p["block"] + ", " + p["town"]
        else:
            place = (p["town"] if not p.get("inside") else "ELLSMERE")
        out.append(["ME-%d-%04d" % (y, seq[y]), p["at"].strftime("%Y-%m-%d"), place, p["death"].strftime("%Y-%m-%d"),
                    p["age"], p["sex"], row["cause"], "HOMICIDE"])
    return out


def population_rows():
    out = []
    for vint, vals in (("V2024", (641_822, 643_105, 645_960, 649_214, 653_480)),
                       ("V2025", (641_822, 643_590, 647_012, 651_377, 656_942, 660_118))):
        for i, v in enumerate(vals):
            out.append([vint, "%d-07-01" % (2020 + i), "Ellsmere city", v])
    return out


def cad_rows(b):
    """Assault-related calls for service, 2024 and 2025: each assault incident brought one or more calls, and many
    calls found no offense."""
    r = np.random.default_rng(b.seed * 41 + 13)
    events = []
    for i in b.incidents:
        if i["kind"] not in ("assault", "assault_dv") or not (2024 <= i["reported"].year <= 2025):
            continue
        typ = "DOM" if i["kind"] == "assault_dv" else ("ASLT" if r.random() < 0.8 else "FIGHT")
        n = 1 + (r.random() < 0.18)
        for k in range(n):
            t = i["reported"] - dt.timedelta(minutes=int(r.integers(1, 25))) + dt.timedelta(minutes=2 * k)
            events.append((t, typ, "911" if r.random() < 0.86 else "ADMIN", "RPT" if k == 0 else "DUP", k))
    for y in (2024, 2025):
        for m in range(1, 13):
            for _ in range(int(r.poisson(560 * W.STREET[m - 1] ** 0.6))):
                t = dt.datetime(y, m, int(r.integers(1, 29)), int(r.integers(0, 24)), int(r.integers(0, 60)))
                events.append((t, ("FIGHT", "ASLT", "DOM", "DISTURB")[int(r.integers(0, 4))],
                               "911" if r.random() < 0.8 else ("OFFICER" if r.random() < 0.5 else "ADMIN"),
                               ("NRPT", "GOA", "UNF")[int(r.integers(0, 3))], 0))
    events.sort(key=lambda e: e[0])
    out, last = [], {}
    seq = {}
    for t, typ, src, disp, k in events:
        y = t.year
        seq[y] = seq.get(y, 0) + 1
        no = "%d%07d" % (y % 100, seq[y])
        master = last.get(typ, "") if disp == "DUP" else ""
        if disp != "DUP":
            last[typ] = no
        out.append([no, B.to_utc(t).strftime("%Y-%m-%dT%H:%M:%SZ"), typ, "1" if typ in ("ASLT", "DOM") else "2", src,
                    disp, master])
    return out
