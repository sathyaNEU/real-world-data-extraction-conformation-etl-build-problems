"""Writes task483's evidence pack from world.py and asks.py: the board's designation standard, the outcomes release's
2024 and 2025 editions and their technical notes, the college's program inventory and its two completion extracts, the
grant's participant roster, the participants' wage records, the college's attendance export for the grant's
participants, its Direct Loan disbursements and its cost of attendance, and the two distractors (the documents are
docs.py's)."""
import csv
import datetime as dt
import os

import numpy as np

import asks as A
import docs as DOC
import world as W

D = dt.date
TD = dt.timedelta
FILES = {
    "standard": "workforce_value_designation_standard_2027-28.pdf",
    "release24": "postsecondary_earnings_outcomes_2024_edition.xlsx",
    "release25": "postsecondary_earnings_outcomes_2025_edition.csv",
    "notes": "earnings_outcomes_technical_notes_2025.pdf",
    "inventory": "larkspur_program_inventory_2025-26.xlsx",
    "older": "fennimore_ridgefield_completions_2024-25.xlsx",
    "newer": "copper_flats_antelope_springs_completions_2024-25.csv",
    "roster": "ctg_participant_roster_2023-2026.csv",
    "wages": "ctg_participant_wage_records_2022q3-2026q2.csv",
    "attendance": "larkspur_ctg_attendance_2023-2026.csv",
    "loans": "larkspur_direct_loan_disbursements_2019-2026.csv",
    "coa": "larkspur_cost_of_attendance_2024-25.pdf",
    "oews": "state_occupational_wage_estimates_may2025.xlsx",
    "demand": "in_demand_occupations_list_2026-27.pdf",
}
OLD, NEW = A.OLD_SIS, A.NEW_SIS
EXTRACTED = D(2026, 10, 9)          # the board's wage extract
OLD_CODE = {"RN": "NURS.AAS", "RAD": "RADT.AAS", "WLD": "WELD.AAS", "DSL": "DIES.AAS", "BUS": "BUSN.AAS",
            "ECE": "ECED.AAS", "MA": "MDAS.CT2", "IT": "INFT.AAS", "CJ": "CRJS.AAS", "AUT": "AUTO.AAS",
            "CUL": "CULA.AAS", "PAR": "PARA.CT2", "CDL": "CDLA.CC", "CNA": "NAST.CC", "PHL": "PHLB.CC",
            "PHT": "PHRT.CC", "EMT": "EMTB.CC", "WLF": "WLDF.CC", "MCD": "MCOD.CC", "ITS": "ITSP.CC", "HVC": "HVAC.CC",
            "WHS": "WHSL.CC", "FRK": "FORK.CC"}
NEW_ID = {"RN": 4410, "RAD": 4420, "WLD": 3310, "DSL": 3320, "BUS": 2210, "ECE": 2240, "MA": 4450, "IT": 2260,
          "CJ": 2280, "AUT": 3330, "CUL": 2290, "PAR": 2295, "CDL": 7101, "CNA": 7102, "PHL": 7103, "PHT": 7104,
          "EMT": 7105, "WLF": 7106, "MCD": 7107, "ITS": 7108, "HVC": 7109, "WHS": 7110, "FRK": 7111}
ETP = {"CDL": "ETP-20461", "CNA": "ETP-20477", "PHL": "ETP-20485", "PHT": "ETP-20493", "EMT": "ETP-20508",
       "WLF": "ETP-20514", "MCD": "ETP-20529", "ITS": "ETP-20533", "HVC": "ETP-20546", "WHS": "ETP-20552",
       "FRK": "ETP-20567"}
CREDITS = {"RN": 68, "RAD": 72, "WLD": 64, "DSL": 64, "BUS": 60, "ECE": 60, "MA": 34, "IT": 62, "CJ": 60, "AUT": 66,
           "CUL": 62, "PAR": 32}
UNIT = {"A": 284110, "B": 284121, "C": 284132, "D": 284143}
PROVIDER = ("TP-0417", W.SYSTEM)
OTHER_INST = [(284200, "Granite Bench College", ("Main campus",)), (284311, "Pinyon Mesa College", ("Main campus",)),
              (284422, "Coldwater Range Community College", ("North campus", "South campus")),
              (284533, "Badger Hollow Technical College", ("Main campus",)),
              (284644, "Owl Creek Community College", ("Main campus",)),
              (284755, "Juniper Gap College", ("Main campus", "Valley center"))]
OTHER_PROV = [("TP-0122", "Granite Bench College"), ("TP-0186", "Pinyon Mesa College"),
              ("TP-0233", "Coldwater Range Community College"), ("TP-0309", "Badger Hollow Technical College"),
              ("TP-0352", "Ridgeline Commercial Driving Academy"), ("TP-0388", "Owl Creek Community College"),
              ("TP-0451", "High Desert Allied Health Institute")]
LEVEL = {"AAS": "Associate", "C2": "Certificate (1 to 2 years)"}
FILLER_CIP = [("51.3801", "Registered Nursing/Registered Nurse", "AAS", 62000), ("47.0604", "Automobile/Automotive "
              "Mechanics Technology/Technician", "AAS", 41000), ("52.0201", "Business Administration and Management, "
              "General", "AAS", 39000), ("48.0508", "Welding Technology/Welder", "AAS", 47000),
              ("51.0801", "Medical/Clinical Assistant", "C2", 33000), ("19.0709", "Child Care Provider/Assistant",
              "AAS", 27000), ("51.0904", "Emergency Medical Technology/Technician (EMT Paramedic)", "AAS", 52000),
              ("15.0303", "Electrical, Electronic, and Communications Engineering Technology/Technician", "AAS",
               56000), ("11.0901", "Computer Systems Networking and Telecommunications", "AAS", 51000),
              ("51.0602", "Dental Hygiene/Hygienist", "AAS", 68000), ("43.0104", "Criminal Justice/Safety Studies",
              "AAS", 33000), ("51.2601", "Medical Insurance Coding Specialist/Coder", "C2", 34000)]
TITLES = {"RN": "Registered Nursing/Registered Nurse", "RAD": "Radiologic Technology/Science - Radiographer",
          "WLD": "Welding Technology/Welder", "DSL": "Diesel Mechanics Technology/Technician",
          "BUS": "Business Administration and Management, General", "ECE": "Child Care Provider/Assistant",
          "MA": "Medical/Clinical Assistant", "IT": ("Information Technology",
                                                     "Computer Systems Networking and Telecommunications"),
          "CJ": ("Criminal Justice/Law Enforcement Administration", "Criminal Justice/Safety Studies"),
          "AUT": "Automobile/Automotive Mechanics Technology/Technician", "CUL": "Culinary Arts/Chef Training",
          "PAR": "Legal Assistant/Paralegal"}


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(head)
        n = 0
        for r in rows:
            w.writerow(r)
            n += 1
    return n


def _book():
    import openpyxl
    return openpyxl.Workbook()


def _style(ws, widths, fmt=None, header=1):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    for c in ws[header]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, wd in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ws.freeze_panes = ws.cell(row=header + 1, column=1).coordinate
    for col, f in (fmt or {}).items():
        for row in ws.iter_rows(min_row=header + 1):
            if len(row) > col:
                row[col].number_format = f


def title(code):
    t = TITLES[code]
    return t if isinstance(t, str) else t[1]


def program_name(code):
    return W.DEGREE[code][0] if code in W.DEGREE else W.SHORT[code][0]


# ---------------------------------------------------------------------------------------------------------------------
# the outcomes release
def other_cells(year_after, cohort, earn_year, r, edition):
    """the release's rows for every institution and every years-after measure other than Larkspur's three-year cells"""
    rows = []
    for unit, inst, camps in OTHER_INST:
        rr = np.random.default_rng([W.SEED, unit, edition, year_after])
        for k, (cip, ttl, award, level) in enumerate(FILLER_CIP):
            if rr.random() < 0.45:
                continue
            for camp in camps:
                if camp != camps[0] and rr.random() < 0.5:
                    continue
                n = int(rr.integers(4, 70))
                lv = level * {1: 0.74, 3: 1.0, 5: 1.12}[year_after] * (1.0 if earn_year == 2025 else 1 / W.CPI_2425)
                rows.append((unit, inst, camp, cip, ttl, award, cohort, year_after, earn_year, n, _pcts(rr, n, lv)))
    return rows


def _pcts(r, n, level, full_share=0.78):
    if n < 10:
        return None
    x = W.earnings(r, n, level, full_share)
    return tuple(int(round(v / 100.0)) * 100 for v in np.percentile(x, W.PS))


def larkspur_cells(edition):
    """Larkspur's rows in one edition: the three-year cells from world.py and the one- and five-year cells"""
    year3 = {2024: "2020-21", 2025: "2021-22"}[edition]
    rows = []
    for code, (name, cip, cip10, award, cells, comp) in W.DEGREE.items():
        for (camp, coh, year, n, x, q) in W.degree_cells(code):
            if coh != year3:
                continue
            rows.append((UNIT[camp], camp, code, award, coh, 3, year, n, q))
        rr = np.random.default_rng([W.SEED, edition, sum(map(ord, code))])
        for ya, coh in ((1, {2024: "2022-23", 2025: "2023-24"}[edition]), (5, {2024: "2018-19", 2025: "2019-20"}[edition])):
            for camp, cell in cells.items():
                n = max(3, int(round(cell[0] * rr.uniform(0.8, 1.15))))
                lv = cell[2] * {1: 0.76, 5: 1.13}[ya] * (1.0 if edition == 2025 else 1 / W.CPI_2425)
                rows.append((UNIT[camp], camp, code, award, coh, ya, edition, n, _pcts(rr, n, lv, cell[3])))
    return rows


def release_cip(code, edition):
    name, cip, cip10, award, cells, comp = W.DEGREE[code]
    if edition == 2024:
        return cip10, TITLES[code] if isinstance(TITLES[code], str) else TITLES[code][0]
    return cip, title(code)


def write_release24(path):
    wb = _book()
    ws = wb.active
    ws.title = "Program earnings"
    ws.append(["%s: Postsecondary Earnings Outcomes, 2024 edition" % W.CENTER])
    ws.append(["Annual earnings of completers found in the state's unemployment insurance wage records, in earnings-year "
               "dollars, by campus, program and award year. S: suppressed (fewer than 10 completers with earnings). "
               "See the technical notes."])
    ws.append([])
    head = ["Institution ID", "Institution", "Campus", "CIP code", "Program", "Award level", "Award year",
            "Years after award", "Earnings year", "Completers with earnings", "10th percentile", "25th percentile",
            "Median", "75th percentile", "90th percentile"]
    ws.append(head)
    rows = []
    for unit, camp, code, award, coh, ya, year, n, q in larkspur_cells(2024):
        cip, ttl = release_cip(code, 2024)
        rows.append((unit, W.SYSTEM, W.CAMPUS[camp], cip, ttl, LEVEL[award], coh, ya, year, n, q))
    r = np.random.default_rng(W.SEED * 3 + 2024)
    for ya, coh in ((1, "2022-23"), (3, "2020-21"), (5, "2018-19")):
        for unit, inst, camp, cip, ttl, award, c, y, ey, n, q in other_cells(ya, coh, 2024, r, 2024):
            rows.append((unit, inst, camp, cip, ttl, LEVEL[award], c, y, ey, n, q))
    rows.sort(key=lambda t: (t[0], t[2], t[3], t[7]))
    for unit, inst, camp, cip, ttl, lvl, coh, ya, ey, n, q in rows:
        sup = q is None
        ws.append([unit, inst, camp, cip, ttl, lvl, coh, ya, ey, "S" if sup else n] + (["S"] * 5 if sup else list(q)))
    _style(ws, (11, 30, 18, 9, 44, 22, 10, 9, 9, 11, 10, 10, 10, 10, 10), {k: "#,##0" for k in range(10, 15)}, header=4)
    wb.save(path)
    return len(rows)


def write_release25(path):
    rows = []
    for unit, camp, code, award, coh, ya, year, n, q in larkspur_cells(2025):
        cip, ttl = release_cip(code, 2025)
        rows.append((unit, W.SYSTEM, W.CAMPUS[camp], cip, ttl, LEVEL[award], coh, ya, year, n, q))
    r = np.random.default_rng(W.SEED * 3 + 2025)
    for ya, coh in ((1, "2023-24"), (3, "2021-22"), (5, "2019-20")):
        for unit, inst, camp, cip, ttl, award, c, y, ey, n, q in other_cells(ya, coh, 2025, r, 2025):
            rows.append((unit, inst, camp, cip, ttl, LEVEL[award], c, y, ey, n, q))
    rows.sort(key=lambda t: (t[0], t[2], t[3], t[7]))
    out = []
    for unit, inst, camp, cip, ttl, lvl, coh, ya, ey, n, q in rows:
        base = ["2025", unit, inst, camp, cip, ttl, lvl, coh, ya, ey]
        if q is None:
            out.append(base + ["completers_with_earnings", "", "S"])
            for m in ("p10", "p25", "p50", "p75", "p90"):
                out.append(base + [m, "", "S"])
            continue
        out.append(base + ["completers_with_earnings", n, ""])
        for m, v in zip(("p10", "p25", "p50", "p75", "p90"), q):
            out.append(base + [m, v, ""])
    return write_csv(path, ["edition", "unit_id", "institution", "campus", "cip_2020", "program_title", "award_level",
                            "award_year", "years_after_award", "earnings_year", "measure", "value", "suppression"], out)


# ---------------------------------------------------------------------------------------------------------------------
# the college's records
def write_inventory(path):
    wb = _book()
    ws = wb.active
    ws.title = "Programs"
    ws.append(["Program", "Award", "Length", "CIP 2020", "CIP before fall 2022", "Fennimore and Ridgefield code",
               "Copper Flats and Antelope Springs ID", "Campuses", "Career Training Grant program ID",
               "Tuition per participant", "Materials and testing fee per section"])
    n = 0
    for code, (name, cip, cip10, award, cells, comp) in W.DEGREE.items():
        camps = ", ".join(W.CAMPUS[c] for c in sorted(set(cells) | set(comp)))
        ws.append([name, {"AAS": "Associate of Applied Science", "C2": "Certificate of Achievement"}[award],
                   "%d credits" % CREDITS[code], cip, cip10 if cip10 != cip else None, OLD_CODE[code], NEW_ID[code],
                   camps, None, None, None])
        n += 1
    for code, (name, cip, hours, weeks, secs, p) in W.SHORT.items():
        camps = ", ".join(W.CAMPUS[c] for c in sorted({s[0] for s in secs}))
        ws.append([name, "Certificate of Completion", "%d clock hours, %d weeks" % (hours, weeks), cip, None,
                   OLD_CODE[code], NEW_ID[code], camps, ETP[code], A.TUITION[code][0], A.TUITION[code][1]])
        n += 1
    _style(ws, (36, 28, 22, 9, 11, 13, 13, 44, 14, 11, 12), {9: "#,##0", 10: "#,##0"})
    ns = wb.create_sheet("Notes")
    for line in [
            "Program inventory for the 2025-26 catalog year, Office of Academic Affairs.",
            "Information Technology and Criminal Justice were recoded in fall 2022 with their curriculum revisions; "
            "awards conferred before then carry the earlier CIP code.",
            "Short-term programs run in sections; a section's grant participants are billed to the State Workforce "
            "Development Board as of the section's census day.",
            "Fennimore and Ridgefield record students in the college's older student system, Copper Flats and Antelope "
            "Springs in the newer one; each system has its own student identifiers, and both carry the state student "
            "ID."]:
        ns.append([line])
    ns.column_dimensions["A"].width = 120
    wb.save(path)
    return n


def completions(P):
    """the 2024-25 completers as each campus's student system records them"""
    out = []
    for c in P["degree"]:
        out.append(dict(code=c["code"], campus=c["campus"], ssid=c["ssid"], sis=c["sis"], date=c["conferred"],
                        award=c["award"]))
    for p in P["participants"]:
        if p["kind"] == "window" and not p["left"]:
            out.append(dict(code=p["code"], campus=p["campus"], ssid=p["ssid"], sis=p["sis"], date=p["section"][1],
                            award="CC"))
    for c in P["short_extra"]:
        out.append(dict(code=c["code"], campus=c["campus"], ssid=c["ssid"], sis=c["sis"], date=c["section"][1],
                        award="CC"))
    return out


def write_older(path, P):
    wb = _book()
    ws = wb.active
    ws.title = "Completions 2024-25"
    ws.append(["Campus", "Student ID", "SSID", "Program Code", "Program Title", "CIP", "Award", "Conferred",
               "Award Year"])
    rows = [c for c in completions(P) if c["campus"] in OLD]
    rows.sort(key=lambda c: (c["campus"], c["date"], OLD_CODE[c["code"]], c["sis"]))
    for c in rows:
        code = c["code"]
        cip = W.DEGREE[code][1] if code in W.DEGREE else W.SHORT[code][1]
        aw = {"AAS": "AAS", "C2": "CA", "CC": "CC"}[c["award"]]
        ws.append([W.CAMPUS[c["campus"]].upper(), c["sis"], c["ssid"], OLD_CODE[code], program_name(code).upper(), cip,
                   aw, c["date"], "2024-25"])
    _style(ws, (13, 10, 12, 11, 40, 8, 6, 11, 9), {7: "mm/dd/yyyy"})
    wb.save(path)
    return len(rows)


def write_newer(path, P):
    rows = [c for c in completions(P) if c["campus"] in NEW]
    rows.sort(key=lambda c: (c["campus"], c["date"], NEW_ID[c["code"]], c["sis"]))
    out = []
    for c in rows:
        code = c["code"]
        cip = W.DEGREE[code][1] if code in W.DEGREE else W.SHORT[code][1]
        cred = {"AAS": "Associate of Applied Science", "C2": "Certificate of Achievement",
                "CC": "Certificate of Completion"}[c["award"]]
        s = c["ssid"]
        out.append([W.CAMPUS[c["campus"]], c["sis"], "%s-%s-%s" % (s[:3], s[3:6], s[6:]), NEW_ID[code],
                    program_name(code), cip, cred, c["date"].isoformat()])
    return write_csv(path, ["campus_name", "student_number", "state_student_id", "program_id", "program_name",
                            "cip_2020", "credential", "completion_date"], out)


def exit_reason(p, r):
    if not p["left"]:
        return "Completed", "Y"
    return ["Withdrew - personal", "Withdrew - employment", "Withdrew - other"][int(r.choice(3, p=[.55, .25, .20]))], "N"


def write_roster(path, P):
    r = np.random.default_rng(W.SEED * 5 + 1)
    rows = []
    for p in sorted(P["participants"], key=lambda p: (p["section"][0], p["code"], p["campus"], p["pid"])):
        s, e = p["section"]
        why, cred = exit_reason(p, r)
        enrolled = s - TD(days=int(r.integers(6, 35)))
        rows.append([p["pid"], p["ssid"], PROVIDER[0], PROVIDER[1], ETP[p["code"]], W.SHORT[p["code"]][0],
                     W.CAMPUS[p["campus"]], p["section_id"], s.isoformat(), e.isoformat(),
                     (p["late"] or enrolled).isoformat(), p["exit_day"].isoformat(), why, cred])
    return write_csv(path, ["participant_id", "state_student_id", "provider_id", "provider_name", "etp_program_id",
                            "program_name", "campus", "section_id", "section_start", "section_end", "enrolled_on",
                            "exit_date", "exit_reason", "credential_earned"], rows)


# ---------------------------------------------------------------------------------------------------------------------
# wage records
NAICS = {"CDL": "484121", "CNA": "623110", "PHL": "621511", "PHT": "446110", "EMT": "621910", "WLF": "332312",
         "MCD": "622110", "ITS": "541512", "HVC": "238220", "WHS": "493110", "FRK": "423830"}
OTHER_NAICS = ["722511", "445110", "452319", "561320", "236118", "811111", "621111", "531110", "811122", "541611"]


def ui_account(r_map, key):
    if key not in r_map["acct"]:
        while True:
            v = "%07d" % int(r_map["rng"].integers(1000000, 9999999))
            if v not in r_map["used"]:
                r_map["used"].add(v)
                r_map["acct"][key] = v
                break
    return r_map["acct"][key]


def q_index(q):
    return q.year * 4 + (q.month - 1) // 3


def wage_rows(P):
    """(participant, account, naics, year, quarter, wages, report, received) for every participant, Larkspur's and the
    other providers', with an amended report for some employer-quarters"""
    accounts = dict(rng=np.random.default_rng(W.SEED * 7 + 3), acct={}, used=set())
    r = np.random.default_rng(W.SEED * 7 + 5)
    lo, hi = q_index(D(2022, 7, 1)), q_index(D(2026, 4, 1))
    out = []

    def add(pid, key, naics, q, amt, protect):
        if not lo <= q_index(q) <= hi:
            return
        acct = ui_account(accounts, key)
        y, k = W.qlabel(q)
        recv = W.qend(q) + TD(days=int(r.integers(25, 45)))
        out.append([pid, acct, naics, y, k, "%.2f" % amt, "Original", recv.isoformat()])
        if not protect and r.random() < 0.04:
            v = amt * (1 + r.uniform(-0.07, 0.07)) if r.random() < 0.7 else amt
            arrived = recv + TD(days=int(r.integers(40, 260)))
            if arrived <= EXTRACTED:                 # an amendment received after the extract is not in it
                out.append([pid, acct, naics, y, k, "%.2f" % v, "Amended", arrived.isoformat()])
    for p in P["participants"]:
        guard = set()
        if p["kind"] == "window" and not p["left"]:
            q = W.qstart(p["completed"] + TD(days=W.DAY))
            for k in range(-2, 3):
                qq = q
                for _ in range(abs(k)):
                    qq = W.qnext(qq) if k > 0 else W.qprev(qq)
                guard.add(qq)
        for (e, q), amt in sorted(p["rec"].items()):
            naics = NAICS[p["code"]] if int(e[-2:]) <= 20 else OTHER_NAICS[int(e[-2:]) % len(OTHER_NAICS)]
            add(p["pid"], e, naics, q, amt, q in guard)
        # a job before the program, ending a month or more before the section began
        if r.random() < 0.45:
            end = p["section"][0] - TD(days=int(r.integers(30, 240)))
            st = end - TD(days=int(r.integers(120, 900)))
            wage = float(np.exp(r.normal(np.log(560), 0.25)))
            job = ("PRE%s%s" % (p["pid"][-6:], p["code"]), st, end, round(wage, 2), int(r.choice([1, 2])))
            for (e, q), amt in sorted(W.quarterly(r, [job]).items()):
                add(p["pid"], e, OTHER_NAICS[int(p["pid"][-1]) % len(OTHER_NAICS)], q, amt, False)
    ids = A.Ids(W.SEED * 7 + 9)
    ids.seen |= {p["pid"] for p in P["participants"]}
    for i in range(1700):                       # the other providers' participants
        pid = ids.participant()
        start = D(2023, 7, 1) + TD(days=int(r.integers(0, 900)))
        jobs = []
        if r.random() < 0.5:
            st = start - TD(days=int(r.integers(100, 700)))
            jobs.append(("OP%s-0" % pid, st, start - TD(days=int(r.integers(10, 90))),
                         round(float(np.exp(r.normal(np.log(600), 0.3))), 2), 1))
        if r.random() < 0.8:
            st = start + TD(days=int(r.integers(20, 200)))
            jobs.append(("OP%s-1" % pid, st, st + TD(days=int(r.exponential(500)) + 60),
                         round(float(np.exp(r.normal(np.log(820), 0.3))), 2), int(r.choice([1, 2]))))
        for (e, q), amt in sorted(W.quarterly(r, jobs).items()):
            add(pid, e, OTHER_NAICS[int(pid[-2:]) % len(OTHER_NAICS)], q, amt, False)
    out.sort(key=lambda x: (x[3], x[4], x[0], x[1], x[6] == "Amended"))
    return out


# ---------------------------------------------------------------------------------------------------------------------
# the college's attendance export
def attendance_rows(rows):
    """one row per session a grant participant attended, in date order; the week the export carries twice is appended
    again at its end"""
    rows = sorted(rows, key=lambda x: (x["date"], x["crn"], x["pid"]))
    out = [[x["pid"], x["crn"], x["date"].isoformat(), A.hmm(x["minutes"])] for x in rows]
    out += [[x["pid"], x["crn"], x["date"].isoformat(), A.hmm(x["minutes"])] for x in rows
            if A.RESENT[0] <= x["date"] <= A.RESENT[1]]
    return out


def loan_rows(rows):
    out = []
    for x in rows:
        new = x["ay"] >= "2024-25"
        typ = {"Sub": "DL Sub", "Unsub": "DL Unsub", "PLUS": "DL PLUS Parent"}[x["type"]] if new else \
            {"Sub": "SUB", "Unsub": "UNSUB", "PLUS": "PLUS"}[x["type"]]
        out.append([x["ssid"], x["ay"], typ, x["loan_id"], x["no"], x["date"].isoformat(), "%.2f" % x["amount"],
                    x["status"]])
    return out


# ---------------------------------------------------------------------------------------------------------------------
# the distractor workbook
OCCUPATIONS = [("29-1141", "Registered Nurses", 84210), ("29-2034", "Radiologic Technologists and Technicians", 70120),
               ("51-4121", "Welders, Cutters, Solderers, and Brazers", 50980),
               ("49-3031", "Bus and Truck Mechanics and Diesel Engine Specialists", 58740),
               ("43-6014", "Secretaries and Administrative Assistants", 41630), ("39-9011", "Childcare Workers", 29650),
               ("31-9092", "Medical Assistants", 40310), ("15-1231", "Computer Network Support Specialists", 66420),
               ("33-3051", "Police and Sheriff's Patrol Officers", 67980),
               ("49-3023", "Automotive Service Technicians and Mechanics", 49870), ("35-1011", "Chefs and Head Cooks",
               52440), ("23-2011", "Paralegals and Legal Assistants", 55870),
               ("53-3032", "Heavy and Tractor-Trailer Truck Drivers", 56430), ("31-1131", "Nursing Assistants", 37820),
               ("31-9097", "Phlebotomists", 40210), ("29-2052", "Pharmacy Technicians", 41380),
               ("29-2042", "Emergency Medical Technicians", 40170), ("29-2072", "Medical Records Specialists", 47960),
               ("15-1232", "Computer User Support Specialists", 54020),
               ("49-9021", "Heating, Air Conditioning, and Refrigeration Mechanics and Installers", 55610),
               ("53-7065", "Stockers and Order Fillers", 36780), ("53-7051", "Industrial Truck and Tractor Operators",
               42150)]


def write_oews(path):
    r = np.random.default_rng(W.SEED * 13 + 1)
    wb = _book()
    ws = wb.active
    ws.title = "Statewide"
    ws.append(["Occupational Employment and Wage Statistics, May 2025: statewide estimates"])
    ws.append([])
    ws.append(["SOC code", "Occupation", "Employment", "Mean hourly wage", "Annual 10th percentile",
               "Annual 25th percentile", "Annual median", "Annual 75th percentile", "Annual 90th percentile"])
    for soc, name, med in OCCUPATIONS:
        emp = int(round(r.uniform(400, 9000), -1))
        ps = [med * f for f in (0.68, 0.82, 1.0, 1.2, 1.42)]
        ws.append([soc, name, emp, round(med * 1.04 / 2080, 2)] + [int(round(v, -1)) for v in ps])
    _style(ws, (9, 58, 11, 10, 11, 11, 11, 11, 11), {k: "#,##0" for k in (2, 4, 5, 6, 7, 8)}, header=3)
    wb.save(path)
    return len(OCCUPATIONS)


def build_pack(out):
    f = lambda k: os.path.join(out, FILES[k])
    P = A.people()
    att = A.attendance(P)
    loans = A.loans(P)
    n = {}
    n["release24"] = write_release24(f("release24"))
    n["release25"] = write_release25(f("release25"))
    n["inventory"] = write_inventory(f("inventory"))
    n["older"] = write_older(f("older"), P)
    n["newer"] = write_newer(f("newer"), P)
    n["roster"] = write_roster(f("roster"), P)
    n["wages"] = write_csv(f("wages"), ["participant_id", "ui_account", "naics", "year", "quarter", "wages",
                                        "report_type", "received_date"], wage_rows(P))
    n["attendance"] = write_csv(f("attendance"), ["participant_id", "crn", "session_date", "hours"],
                                attendance_rows(att))
    n["loans"] = write_csv(f("loans"), ["SSID", "AWARD_YEAR", "LOAN_TYPE", "LOAN_ID", "DISB_NO", "DISB_DATE",
                                        "GROSS_AMT", "DISB_STATUS"], loan_rows(loans))
    n["oews"] = write_oews(f("oews"))
    DOC.write_standard(f("standard"))
    DOC.write_notes(f("notes"))
    DOC.write_coa(f("coa"))
    DOC.write_demand(f("demand"))
    for k in ("standard", "notes", "coa", "demand"):
        n[k] = 1
    return n
