"""The pack's record files as each system exports them: the OSCE system's marks for the 2026 sitting, the station
sheet and examiner allocation for it, the case bank and its sitting history, the examiner register, the training
team's attendance record, the availability form's responses and the two operational files the pack carries. Each
writer returns its row count."""
import csv
import datetime as dt
import unicodedata
import zlib

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import common as K
import world as W


def _csv(path, header, rows, delim=","):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delim, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def _ascii(x):
    return unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode()


def _sheet(ws, header, rows, widths, date_cols=(), freeze=True):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DCE6F0")
        c.alignment = Alignment(vertical="top", wrap_text=True)
    for row in rows:
        ws.append(row)
    for i, w in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    for c in date_cols:
        for cell in ws[openpyxl.utils.get_column_letter(c + 1)][1:]:
            if isinstance(cell.value, (dt.date, dt.datetime)):
                cell.number_format = "dd/mm/yyyy"
    if freeze:
        ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


# ---------------------------------------------------------------------------------------------- the 2026 sitting
def schedule():
    """Each candidate's day, round and the slot (start and end) of each station in their rotation: eight minutes a
    station and two to change, a round of twelve candidates in two hours."""
    starts = {1: [(8, 30), (10, 45), (13, 30), (15, 45)], 2: [(8, 30), (10, 45), (13, 30)]}
    out, i = {}, 0
    for dno, rounds in K.ROUNDS26.items():
        dd = K.SIT26[dno - 1]
        for ri, rno in enumerate(rounds):
            h, m = starts[dno][ri]
            t0 = dt.datetime(dd.year, dd.month, dd.day, h, m)
            for j in range(12):
                for slot in range(12):
                    sno = (j + slot) % 12 + 1
                    beg = t0 + dt.timedelta(minutes=10 * slot)
                    out[(i, sno)] = (dno, rno, beg, beg + dt.timedelta(minutes=8))
                i += 1
    return out


def exam_no(i):
    return "FM26-%04d" % (i + 1)


def badge(sno, ro):
    return "S%02d-%s" % (sno, "L" if ro == 0 else "2")


def write_marks(path, w, alloc):
    """One row an item an examiner marked (and one for the global grade): day 1 as the OSCE system stored it before
    its overnight update (station number, examiner badge, the mark's label), day 2 after it (case code, staff number,
    the mark's code). Station 7's item 14 was on the day 1 forms only; an item a cue opens is N/A when it was not
    given."""
    rng = np.random.default_rng([w["seed"], 41])
    sch = schedule()
    code_of = {st[0]: st[1] for st in K.STATIONS26}
    rows = []
    order = sorted(sch.items(), key=lambda kv: (kv[1][2], kv[0][1], kv[0][0]))
    for (i, sno), (dno, rno, beg, end) in order:
        for ro in (0, 1):
            rec = w["rec"][(i, sno, ro)]
            stamp = end + dt.timedelta(seconds=int(rng.integers(15, 170)))
            n_items = [st[4] for st in K.STATIONS26 if st[0] == sno][0]
            for item in range(1, n_items + 1):
                if sno == K.WITHDRAWN[0] and item == K.WITHDRAWN[1]:
                    if dno == 2:
                        continue
                    v = w["withdrawn"][(i, ro)]
                elif item in rec["items"]:
                    v = rec["items"][item]
                else:
                    v = None                                          # not applicable: the cue was not given
                if dno == 1:
                    resp = K.LABELS_DAY1[v]
                    rows.append([exam_no(i), dno, rno, str(sno), badge(sno, ro), "Lead" if ro == 0 else "Second",
                                 str(item), resp, stamp.strftime("%Y-%m-%d %H:%M:%S")])
                else:
                    resp = "NA" if v is None else str(v)
                    rows.append([exam_no(i), dno, rno, code_of[sno], alloc[(sno, ro)]["staff"],
                                 "L" if ro == 0 else "S", str(item), resp, stamp.strftime("%Y-%m-%d %H:%M:%S")])
    return _csv(path, ["exam_no", "exam_day", "round", "station", "examiner", "role", "item", "response",
                       "recorded_at"], rows)


def write_global(path, w, alloc):
    """The OSCE system's global grades table: one row an examiner an encounter, in each day's format (day 1 the
    grade's label, day 2 its code from 1, clear fail, to 5, excellent)."""
    rng = np.random.default_rng([w["seed"], 44])
    sch = schedule()
    code_of = {st[0]: st[1] for st in K.STATIONS26}
    rows = []
    order = sorted(sch.items(), key=lambda kv: (kv[1][2], kv[0][1], kv[0][0]))
    for (i, sno), (dno, rno, beg, end) in order:
        for ro in (0, 1):
            g = w["global"][(i, sno, ro)]
            stamp = (end + dt.timedelta(seconds=int(rng.integers(20, 190)))).strftime("%Y-%m-%d %H:%M:%S")
            if dno == 1:
                rows.append([exam_no(i), dno, str(sno), badge(sno, ro), K.GLOBAL[g], stamp])
            else:
                rows.append([exam_no(i), dno, code_of[sno], alloc[(sno, ro)]["staff"], str(g + 1), stamp])
    return _csv(path, ["exam_no", "exam_day", "station", "examiner", "global_grade", "recorded_at"], rows)


def allocation(e, seed):
    """The 2026 sitting's two examiners at each station, drawn from the register's eligible examiners as it stood
    in December 2025 (active, an eligible grade, training attended in the three years before)."""
    r = np.random.default_rng([seed, 42])
    ok = [p for p in e["people"] if p["status"] == "Active" and p["grade"] in W.ELIGIBLE_GRADES
          and p["base"] in ("Callowfield", "CUH", "General practice") and p["staff"] not in e["device"]
          and p["initial"] <= dt.date(2025, 11, 30)]
    ok.sort(key=lambda p: p["staff"])
    pick = [ok[j] for j in r.choice(len(ok), size=24, replace=False).tolist()]
    out = {}
    for k, st in enumerate(K.STATIONS26):
        for ro in (0, 1):
            p = pick[2 * k + ro]
            out[(st[0], ro)] = {"staff": p["staff"], "name": "%s %s" % (p["fore"], p["sur"]), "title": p["title"],
                                "grade": p["grade"]}
    return out


def write_station_sheet(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Stations"
    rows = [[st[0], st[1], st[2], st[3], st[4], st[5], "8 minutes"] for st in K.STATIONS26]
    _sheet(ws, ["Station", "Case code", "Case title", "Blueprint domain", "Checklist items", "Resources",
                "Station time"], rows, [8, 11, 40, 20, 14, 20, 12])
    ws2 = wb.create_sheet("Marking")
    notes = [["Each checklist item is marked 0 (not done), 1 (partly done) or 2 (done well), or N/A where the item "
              "depends on a cue the simulated patient gives and the cue was not given."],
             ["The station mark is the points scored over the points the station's available items carry, out of 20 "
              "(assessment policy 3.2)."],
             ["Each examiner also gives a global grade: clear fail, borderline, clear pass, good or excellent."],
             ["Both examiners at a station mark every candidate independently; the candidate's station mark is the "
              "mean of the two."]]
    for n in notes:
        ws2.append(n)
    ws2.column_dimensions["A"].width = 120
    wb.save(path)
    return len(rows)


def write_allocation(path, alloc):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Examiners"
    rows = []
    for st in K.STATIONS26:
        for ro in (0, 1):
            a = alloc[(st[0], ro)]
            rows.append([st[0], st[1], "Lead examiner" if ro == 0 else "Second examiner", badge(st[0], ro),
                         a["staff"], "%s %s" % (a["title"], a["name"]), a["grade"]])
    _sheet(ws, ["Station", "Case code", "Role", "Badge", "Staff no.", "Examiner", "Grade"], rows,
           [8, 11, 16, 9, 10, 30, 22])
    wb.save(path)
    return len(rows)


# ---------------------------------------------------------------------------------------------- the case bank
def _bank_date(d):
    """The bank keeps a review date entered in the old system as the text it was typed in, day first; a date
    entered since the migration is a date."""
    if d < K.BANK_MIGRATION:
        return d.strftime("%d/%m/%Y")
    return d


def write_bank(path, b):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cases"
    rows = []
    for c in sorted(b["cases"], key=lambda c: (K.DOMAINS.index(c["domain"]), c["code"])):
        rows.append([c["code"], c["title"], c["domain"], c["specialty"], c["resources"], c["version"], c["status"],
                     _bank_date(c["reviewed"])])
    _sheet(ws, ["Case code", "Title", "Blueprint domain", "Specialty", "Resources", "Version", "Status",
                "Last reviewed"], rows, [12, 46, 20, 24, 20, 9, 22, 14], date_cols=(7,))
    ws2 = wb.create_sheet("Fields")
    for line in [["Field", "Meaning"],
                 ["Case code", "The case's code in the bank"],
                 ["Resources", "What the station needs: SP (a simulated patient), Manikin, Task trainer, SP and task "
                               "trainer, Video, Paper case"],
                 ["Version", "The case's current version; a case written in the Assessment Item Bank starts at 1"],
                 ["Status", "Active; Active - edits pending (usable as it stands); Under review (not usable until the "
                            "assessment group signs it off); Retired"],
                 ["Last reviewed", "The date the OSCE assessment group last reviewed the case"]]:
        ws2.append(line)
    ws2.column_dimensions["A"].width = 16
    ws2.column_dimensions["B"].width = 110
    wb.save(path)
    return len(rows)


def write_usage(path, b):
    rows = [[u["sitting"], u["date"].isoformat(), u["station"], u["code"], u["title"]] for u in b["usage"]]
    return _csv(path, ["sitting", "sitting_date", "station", "case_code", "title_as_set"], rows)


# ---------------------------------------------------------------------------------------------- examiners
def write_register(path, e):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Register"
    rows = []
    for p in sorted(e["people"], key=lambda p: (p["sur"], p["fore"])):
        rows.append([p["staff"], p["title"], p["fore"], p["sur"], p["grade"], p["base"], p["email"], p["initial"],
                     p["last_refresher"], p["status"]])
    _sheet(ws, ["Staff no.", "Title", "Forename", "Surname", "Grade", "Base", "Email", "Examiner training",
                "Last refresher", "Status"], rows, [10, 7, 14, 22, 22, 18, 40, 17, 15, 11], date_cols=(7, 8))
    wb.save(path)
    return len(rows)


def _signed(title, fore, sur, venue):
    """A name as each venue's sign-in sheet carries it: the training team's own sheet from the register, the
    hospital's and Fennabeg's typed from the sheet with the title and without the accents."""
    if venue == W.VENUES[0]:
        return "%s %s" % (fore, sur)
    return "%s %s %s" % (title, _ascii(fore), _ascii(sur))


def write_training(path, e):
    """The training team's record of every session since 2021: its own sessions from the booking system by
    university staff number, and the sessions the hospital's postgraduate centre and Fennabeg run, from their
    sign-in sheets, by their own staff numbers for their own staff."""
    by_staff = {p["staff"]: p for p in e["people"]}
    rows = []
    for a in e["attendance"]:
        p = by_staff[a["staff"]]
        v = a["session"]["venue"]
        no = p["alt"][0] if "alt" in p and p["alt"][1] == v else p["staff"]
        rows.append([a["session"]["id"], a["session"]["date"].isoformat(), a["session"]["type"], v, no,
                     _signed(p["title"], p["fore"], p["sur"], v), a["att"]])
    for t in e["trainees"]:
        v = t["session"]["venue"]
        rows.append([t["session"]["id"], t["session"]["date"].isoformat(), t["session"]["type"], v, t["no"],
                     _signed("Dr", t["name"][0], t["name"][1], v), t["att"]])
    rows.sort(key=lambda x: (x[1], x[0], x[4]))
    return _csv(path, ["session_id", "session_date", "session_type", "venue", "staff_no", "examiner", "outcome"], rows)


PERSONAL = ["gmail.com", "hotmail.com", "outlook.com", "icloud.com", "eircom.net", "yahoo.ie"]


def write_availability(path, e):
    """The form's export: one row a submission, the time it was submitted, the email it came from and the name
    typed, the site and a Yes for each session offered. About one examiner in ten answered from a personal address
    and typed their name without its accents; about one in ten submitted again later, changing their sessions or
    site (the form says the latest response stands); a few who are not on the register answered too."""
    r = np.random.default_rng([e["seed"], 43])
    rp = np.random.default_rng([e["seed"], 44])      # how each personal address is made up
    by_staff = {p["staff"]: p for p in e["people"]}
    t0 = K.FORM_OPENED
    subs = []
    for x in sorted(e["responses"], key=lambda x: x["staff"]):
        p = by_staff[x["staff"]]
        personal = r.random() < 0.10
        if personal:
            fo, su = _ascii(p["fore"]).lower(), _ascii(p["sur"]).lower().replace(" ", "").replace("'", "")
            digits = int(r.integers(1, 99))
            shape = int(rp.integers(0, 5))
            local = [fo + su + str(digits), fo + "." + su, fo[0] + su, fo + "_" + su + str(digits % 10),
                     su + "." + fo][shape]
            email = "%s@%s" % (local, str(r.choice(PERSONAL)))
            name = "%s %s" % (_ascii(p["fore"]), _ascii(p["sur"]))
            if r.random() < 0.5:
                name = name.replace("O ", "O'", 1) if " O " in " %s " % name else name
        else:
            email = p["email"]
            name = "%s %s" % (p["fore"], p["sur"])
        if r.random() < 0.25:
            name = "Dr %s" % name
        final = dict(x["ticks"]), x["site"]
        when = t0 + dt.timedelta(minutes=int(r.integers(0, 39 * 24 * 60)))
        if r.random() < 0.10 and x["staff"] not in e["device"]:
            # an earlier submission that the later one replaced: other sessions or another site
            first_ticks = dict(x["ticks"])
            flip = [k for k in first_ticks]
            k = flip[int(r.integers(0, 4))]
            first_ticks[k] = not first_ticks[k]
            if not any(first_ticks.values()):
                first_ticks[flip[0]] = True
            first_site = x["site"]
            if r.random() < 0.3:
                first_site = [s[0] for s in K.SITES27 if s[0] != x["site"]][int(r.integers(0, 2))]
            gap = dt.timedelta(minutes=int(r.integers(600, 9000)))
            early = when - gap
            if early < t0 + dt.timedelta(minutes=40):
                # the first answer came in during the form's first days and the change followed it
                early = t0 + dt.timedelta(minutes=40 + gap.seconds // 60 % 2400)
                when = max(when, early + gap)
            subs.append((early, email, name, first_site, first_ticks))
        subs.append((when, email, name, final[1], final[0]))
    for fore, sur in e["extra"][:4]:
        ticks = {s[0]: bool(r.random() < 0.6) for s in K.SESSIONS}
        if not any(ticks.values()):
            ticks["d1_am"] = True
        subs.append((t0 + dt.timedelta(minutes=int(r.integers(0, 39 * 24 * 60))),
                     "%s.%s@callowfield.ie" % (_ascii(fore).lower(), _ascii(sur).lower().replace(" ", "")),
                     "%s %s" % (fore, sur), K.SITES27[int(r.integers(0, 3))][0], ticks))
    subs.sort(key=lambda s: s[0])
    site_label = {s[0]: s[1] for s in K.SITES27}
    # what a few examiners typed in the form's last box: logistics only, about the site they chose and nothing
    # about other sites or sessions; no note used more than twice
    notes = {"CSC": ["Is there parking at the Clinical Skills Centre?", "Which entrance for the Clinical Skills Centre?"],
             "CUH": ["Parking permit for CUH please", "Where do examiners meet at the Simulation Suite?"],
             "FCS": ["First time examining at Fennabeg, directions would help",
                     "Is there a car park at the Clinical Skills Unit?"],
             None: ["Please send the station briefing by email", "Vegetarian lunch please",
                    "Can a medical student observe my station?", "Please use this address for anything about the OSCE",
                    "Could I have a ground-floor room? Knee surgery in March", "Thanks",
                    "Happy to help with the briefing if needed", "Gluten-free lunch if possible"]}
    used = {}
    rc = np.random.default_rng([e["seed"], 45])
    rows = []
    for when, email, name, site, ticks in subs:
        when = when + dt.timedelta(seconds=zlib.crc32(("%s|%s" % (email, when)).encode()) % 60)
        assert K.FORM_OPENED < when <= K.FORM_CLOSED
        note = ""
        if rc.random() < 0.07:
            pool = [x for x in notes[site] + notes[None] if used.get(x, 0) < 2]
            note = pool[int(rc.integers(0, len(pool)))]
            used[note] = used.get(note, 0) + 1
        rows.append([when.strftime("%d/%m/%Y %H:%M:%S"), email, name, site_label[site]] +
                    ["Yes" if ticks[s[0]] else "" for s in K.SESSIONS] + [note])
    return _csv(path, ["Timestamp", "Email address", "Your name", "Which site can you examine at?"] +
                ["Sessions you can examine [%s]" % s[1] for s in K.SESSIONS] + ["Anything we should know?"], rows)
