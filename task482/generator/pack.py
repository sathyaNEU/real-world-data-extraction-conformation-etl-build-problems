"""Write task482's data files from world.py's truth, each in the layout of the system that produces it: the item
bank's assembly-pool export, the two forms' layouts, the old platform's wide attempt export, the new platform's
attempt and item-response exports, the score-routing log, the cutover crosswalk, the testing centres and the
distractors. docs.py writes the documents and the review log workbook."""
import csv
import datetime as dt

import numpy as np

import world as W

FILES = {
    "report": "qpi_technical_report_2027.pdf",
    "policy": "bpccs_mathematics_placement_policy_4-12.pdf",
    "dictionary": "qpi_data_dictionary_2027.pdf",
    "pool": "itemstore_assembly_pool_2027-02-03.csv",
    "map27": "qpi_form_27A_assembly.csv",
    "layout26": "qpi_forms_26A_26B_layout.csv",
    "kts": "kts_qpi_attempts_2026-03-01_to_2026-06-30.csv",
    "ng_att": "northgate_attempts_2026-07-01_to_2027-01-31.csv",
    "ng_resp": "northgate_item_responses_2026-07-01_to_2027-01-31.csv",
    "reports": "qpi_score_reports_2026-03-01_to_2027-01-31.csv",
    "review": "qpi_session_review_log_2026.xlsx",
    "xwalk": "kts_to_northgate_student_crosswalk.csv",
    "centres": "qpi_testing_centres.csv",
    "headcount": "bpccs_fall_2026_headcount_by_college.csv",
    "outcomes": "math_course_outcomes_fall_2026.xlsx",
}
KTS_LEVEL = {"CA": "131", "CCA": "131C", "DM": "091"}


def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        n = 0
        for r in rows:
            w.writerow(r)
            n += 1
    return n


def bu(logit):
    return "%.1f" % (W.BU0 + W.BU1 * logit)


def utc(t_local):
    return t_local + dt.timedelta(hours=W.central_offset(t_local.date()))


def iso_z(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _ids(e):
    """Stable identifiers: old-platform attempt ids, new-platform attempt refs, session refs."""
    if "_ids" in e:
        return e["_ids"]
    rng = np.random.default_rng(W.SEED + 7)
    out = {}
    serial = {}
    refs = set()
    for a in e["attempts"]:
        if a["platform"] == "old":
            serial[a["site"]] = serial.get(a["site"], 0) + 1
            out[id(a)] = "KT%s-26%04d" % (a["site"], serial[a["site"]] + 1180)
        else:
            while True:
                r = "NG%08d" % int(rng.integers(10000000, 99999999))
                if r not in refs:
                    refs.add(r)
                    break
            out[id(a)] = r
    e["_ids"] = out
    return out


def session_ref(a):
    c, d, hm = a["session"]
    return "S%s-%s-%s" % (c[2:], d.strftime("%Y%m%d"), hm.replace(":", ""))


CALIB_FORM = {2023: "23A", 2024: "24A", 2025: "25A"}


def pool_rows(e):
    it = e["items"]
    status = {}
    for f in ("27A", "27B"):
        for i in e["forms"][f]:
            status[i] = "Form %s" % f
    rng = np.random.default_rng(W.SEED + 11)
    rows = []
    for k in sorted(it):
        r = it[k]
        if r["role"] == "anchor":
            rows.append([k, r["legacy"], r["strand"], "anchor", bu(r["bank"]), "%.1f" % (W.BU1 * r["se"]), r["n"],
                         "base calibration 2022", "2022-07-15", r["key"]])
        elif r["role"] == "pool":
            st = int(rng.integers(1, 9))
            when = {2023: "2023-07-21", 2024: "2024-07-19", 2025: "2025-07-18"}[r["ft_year"]]
            rows.append([k, r["legacy"], r["strand"], status.get(k, "ready"), bu(r["bank"]),
                         "%.1f" % (W.BU1 * r["se"]), r["n"], "field test %d, Form %s set %d" % (r["ft_year"],
                         CALIB_FORM[r["ft_year"]], st), when, r["key"]])
    return rows


POOL_COLS = ["item_id", "kts_item", "strand", "status", "difficulty_bu", "se_bu", "n_calibration", "calibration",
             "calibrated_on", "key"]


def map27_rows(e):
    it = e["items"]
    anc = sorted([i for i in it.values() if i["role"] == "anchor"], key=lambda r: r["anchor_pos"])
    rows = [["27A", "anchor", r["anchor_pos"], r["id"], r["legacy"], r["strand"], r["key"], str(r["anchor_pos"])]
            for r in anc]
    for k, iid in enumerate(e["forms"]["27A"]):
        r = it[iid]
        rows.append(["27A", "unique", k + 1, iid, r["legacy"], r["strand"], r["key"], "21-70, shuffled with the field-test set"])
    rng = np.random.default_rng(W.SEED + 13)
    serial = 900
    for st in range(1, 9):
        for k in range(10):
            serial += int(rng.integers(1, 4))
            s = W.STRANDS[(st + k) % 5]
            rows.append(["27A", "field test", "%d.%d" % (st, k + 1), "QPI-%s-%04d" % (s, serial), "", s,
                         "ABCD"[int(rng.integers(4))], "21-70, shuffled with the unique items"])
    return rows


MAP27_COLS = ["form", "section", "slot", "item_id", "kts_item", "strand", "key", "position"]


def layout26_rows(e):
    it = e["items"]
    rows = []
    for form in ("26A", "26B"):
        anc, uni = W.form_items(it, form)
        for k, iid in enumerate(anc):
            r = it[iid]
            rows.append([form, "anchor", k + 1, iid, r["legacy"], r["strand"], r["key"], k + 1, k + 1])
        for k, iid in enumerate(uni):
            r = it[iid]
            rows.append([form, "unique", k + 1, iid, r["legacy"], r["strand"], r["key"], 21 + k, 60 - k])
    for st in range(1, 9):
        for k, iid in enumerate(W.ft_set_items(it, st)):
            r = it[iid]
            rows.append(["FT26-%d" % st, "field test", k + 1, iid, r["legacy"], r["strand"], r["key"], 61 + k, 70 - k])
    return rows


LAYOUT_COLS = ["form", "section", "slot", "item_id", "kts_item", "strand", "key", "kts_position_version_A",
               "kts_position_version_B"]


def _person(e, a):
    return e["students"][a["student"] - 1]


def kts_rows(e):
    ids = _ids(e)
    it = e["items"]
    rows = []
    for a in e["attempts"]:
        if a["platform"] != "old":
            continue
        s = _person(e, a)
        # delivered order: positions 1..70
        order = sorted(range(70), key=lambda i: a["pos"][i])
        resp = "".join(a["letters"][i] or "*" for i in order)
        site = a["centre"][2:4] + ("M" if a["centre"].endswith("1") else "S")
        rows.append([ids[id(a)], a["site"], site, "%07d" % a["sid"], s["dob"].strftime("%m/%d/%Y"), s["sex"],
                     s["hs"], s["registered"].strftime("%m/%d/%Y"), a["form"], a["version"], a["ft_set"],
                     a["date"].strftime("%m/%d/%Y"), a["start"].strftime("%H:%M"), a["end"].strftime("%H:%M"),
                     resp, a["raw"], KTS_LEVEL[a["level"]]])
    return rows


KTS_COLS = ["attempt_id", "college", "site", "student_no", "birth_date", "sex", "hs_code", "registered", "form",
            "version", "ft_set", "test_date", "start", "end", "responses", "raw_score", "placement"]


def ng_att_rows(e):
    ids = _ids(e)
    rows = []
    for a in e["attempts"]:
        if a["platform"] != "new":
            continue
        s = _person(e, a)
        rows.append([ids[id(a)], "%09d" % a["sid"], s["dob"].isoformat(), s["sex"], s["hs"], s["registered"].isoformat(),
                     a["college_held"], a["centre"], session_ref(a), a["form"], a["ft_set"], iso_z(utc(a["start"])),
                     iso_z(utc(a["end"])), a["raw"], a["level"]])
    return rows


NG_ATT_COLS = ["attempt_ref", "student_id", "birth_date", "sex", "hs_code", "registered", "college", "centre",
               "session_ref", "form", "ft_set", "started_at", "submitted_at", "raw_score", "placement"]


def ng_resp_rows(e):
    ids = _ids(e)
    rng = np.random.default_rng(W.SEED + 17)
    for a in e["attempts"]:
        if a["platform"] != "new":
            continue
        order = sorted(range(70), key=lambda i: a["pos"][i])
        t = utc(a["start"]) + dt.timedelta(seconds=int(rng.integers(40, 90)))
        span = (a["end"] - a["start"]).total_seconds() - 120
        rts = rng.gamma(2.2, 1.0, 70)
        rts = rts / rts.sum() * span
        for j, i in enumerate(order):
            rt = max(4, int(rts[j]))
            yield [ids[id(a)], a["items"][i], a["pos"][i], a["letters"][i], a["y"][i], rt, iso_z(t)]
            t += dt.timedelta(seconds=rt)


NG_RESP_COLS = ["attempt_ref", "item_id", "seq", "response", "score", "rt_s", "served_at"]


def report_rows(e):
    ids = _ids(e)
    reps = sorted(e["reports"], key=lambda r: (r["sent"], ids[id(r["attempt"])], r["to"]))
    rows = []
    for k, r in enumerate(reps):
        rows.append(["R%07d" % (2604000 + k * 3 + 1), ids[id(r["attempt"])], r["to"],
                     "automatic" if r["kind"] == "automatic" else "on request", r["sent"].strftime("%Y-%m-%d %H:%M")])
    return rows


REPORT_COLS = ["report_id", "attempt", "sent_to", "report", "sent"]


def xwalk_rows(e):
    rows = []
    for s in e["students"]:
        for c, n in sorted(s["csn"].items()):
            rows.append([c, "%07d" % n, "%09d" % s["sysid"], "2026-07-01"])
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


XWALK_COLS = ["kts_college", "kts_student_no", "northgate_student_id", "migrated"]


def centre_rows(e):
    rows = []
    for c, code, kind in e["centres"]:
        nm = W.NAMES[code].replace(" Community College", "")
        rows.append([c, code, "%s %s testing centre" % (nm, "main campus" if kind == "main" else "satellite"),
                     "%s%s" % (code, "M" if kind == "main" else "S")])
    return rows


CENTRE_COLS = ["centre", "college", "centre_name", "kts_site"]


def headcount_rows(e):
    rng = np.random.default_rng(W.SEED + 19)
    rows = []
    for code, name, n, _, _ in W.COLLEGES:
        hc = int(n * rng.uniform(5.6, 7.4))
        rows.append([code, name, hc, int(hc * rng.uniform(0.52, 0.64)), int(n * rng.uniform(0.62, 0.78))])
    return rows


HEADCOUNT_COLS = ["college", "college_name", "headcount_fall_2026", "fte_fall_2026", "first_time_students_fall_2026"]
