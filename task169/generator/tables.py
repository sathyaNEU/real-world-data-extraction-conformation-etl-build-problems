"""task169 tables: custody stays and facilities, the Department's capacity report, the Board's caseload extract,
the data dictionary and the export manifest."""
from __future__ import annotations

import datetime as dt
import hashlib

import common as C

CAPACITY = {"PRC": 1150, "SCI-KTR": 2350, "SCI-FNW": 1800, "SCI-DNM": 2600, "SCI-LKV": 1250, "SCI-BRW": 1700}
LONG_TERM = {"PRC": 0, "SCI-KTR": 1630, "SCI-FNW": 1210, "SCI-DNM": 1880, "SCI-LKV": 760, "SCI-BRW": 1140}


def facility_of(pid, ad):
    h = int(hashlib.sha256(("fac/%d/%s" % (pid, ad.isoformat())).encode()).hexdigest()[:8], 16)
    return C.FACILITIES[h % len(C.FACILITIES)]


def stays(book):
    """each admission with the date the person next left Department custody"""
    rels = {}
    for pid, rd, rtype, maxd, dist, rno in book.releases:
        rels.setdefault(pid, []).append(rd)
    deaths = {pid: d for pid, d in book.deaths}
    out = []
    for pid, ad, atype, otn, vid in book.admissions:
        nxt = min([r for r in rels.get(pid, []) if r > ad], default=None)
        end = nxt or deaths.get(pid) or dt.date(2099, 1, 1)
        out.append((pid, ad, atype, end))
    return out


def month_ends(year, months):
    out = []
    for m in months:
        d = dt.date(year + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
        out.append(d)
    return out


def capacity_rows(book, transfer_lag):
    """population at each 2026 month end by institution: people with a stay in the record placed at the institution
    their classification sent them to, plus the population admitted before the record opens"""
    st = stays(book)
    rows = []
    for me in month_ends(2026, range(1, 10)):
        pop = {f: LONG_TERM[f] for f in CAPACITY}
        pv = {f: 0 for f in CAPACITY}
        for pid, ad, atype, end in st:
            if ad <= me < end:
                lag = transfer_lag.get((pid, ad))
                f = "PRC" if (lag is None or me < C.add(ad, lag)) else facility_of(pid, ad)
                pop[f] += 1
                if atype != "NC":
                    pv[f] += 1
        for f in CAPACITY:
            rows.append((me, f, CAPACITY[f], pop[f], pv[f]))
    return rows


def write_capacity(path, rows):
    import xlsxwriter
    wb = xlsxwriter.Workbook(path)
    hf = wb.add_format({"bold": True, "bg_color": "#E2EFDA", "border": 1, "text_wrap": True})
    df = wb.add_format({"num_format": "mmm d, yyyy"})
    nf = wb.add_format({"num_format": "#,##0"})
    pf = wb.add_format({"num_format": "0.0%"})
    ws = wb.add_worksheet("Month-end population")
    ws.write(0, 0, "Department of Corrections: population and operating capacity at month end, January to September 2026")
    ws.write(1, 0, "Counts at 23:59 on the last day of the month. Parole violators are people whose current admission "
                   "is a Board recommitment. Refreshed 6 October 2026, Bureau of Planning, Research and Statistics.")
    head = ["Month end", "Institution", "Operating capacity", "Population", "Of whom parole violators", "Occupancy"]
    for j, h in enumerate(head):
        ws.write(3, j, h, hf)
    for i, (me, f, cap, pop, pv) in enumerate(rows, start=4):
        ws.write_datetime(i, 0, dt.datetime(me.year, me.month, me.day), df)
        ws.write(i, 1, f)
        ws.write_number(i, 2, cap, nf)
        ws.write_number(i, 3, pop, nf)
        ws.write_number(i, 4, pv, nf)
        ws.write_formula(i, 5, "=D%d/C%d" % (i + 1, i + 1), pf, pop / cap)
    for j, w in enumerate([12, 12, 11, 11, 13, 10]):
        ws.set_column(j, j, w)
    ws.freeze_panes(4, 0)
    wb.close()
    return len(rows)


def caseload_rows(book, ident):
    """parolees under the Board's supervision at each month end, by district office, with the compact cases the
    office supervises for other states and its own parolees supervised elsewhere"""
    rng = C.stream("pack/caseload")
    st = stays(book)
    custody = {}
    for pid, ad, atype, end in st:
        custody.setdefault(pid, []).append((ad, end))
    deaths = {pid: d for pid, d in book.deaths}
    spells = []
    for pid, rd, rtype, maxd, dist, rno in book.releases:
        if rtype == "EXPIRATION" or maxd is None:
            continue
        spells.append((pid, rd, maxd, dist))
    rows = []
    comp_in = {d: int(rng.integers(140, 260)) for d in C.DISTRICTS}
    comp_out = {d: int(rng.integers(90, 190)) for d in C.DISTRICTS}
    for me in month_ends(2025, range(1, 13)) + month_ends(2026, range(1, 10)):
        n = {d: 0 for d in C.DISTRICTS}
        for pid, rd, maxd, dist in spells:
            if rd <= me < maxd and not any(a <= me < e for a, e in custody.get(pid, [])):
                if pid in deaths and deaths[pid] <= me:
                    continue
                n[dist] += 1
        for d in C.DISTRICTS:
            comp_in[d] += int(rng.integers(-6, 7))
            comp_out[d] += int(rng.integers(-5, 6))
            rows.append((me.isoformat(), C.OFFICE[d], d, n[d], comp_in[d], comp_out[d]))
    return rows


def write_caseload(path, rows):
    head = ("month_end", "office", "district", "pembroke_parolees_supervised", "compact_cases_received",
            "pembroke_parolees_supervised_elsewhere")
    return C.write_csv(path, head, rows)


DICT = {
    C.F_REL: ("Department of Corrections, offender management system: release movements out of Department custody, "
              "1 January 2019 to 30 September 2026. One row per release movement.", [
        ("doc_number", "text", "Department number. A person keeps one number across commitments."),
        ("release_date", "date MM/DD/YYYY", "Date of the release movement."),
        ("movement_code", "text", "Release movement. From 14 March 2022: PAR parole, RPR reparole after a Board "
                                  "recommitment, EXP expiration of the maximum sentence (no supervision follows). Before "
                                  "that date the same movements were written PAROLE, REPAROLE and MAX EXP."),
        ("facility", "text", "Institution or community corrections centre released from."),
        ("county_of_commitment", "text", "County of the governing commitment."),
        ("birth_date", "date MM/DD/YYYY", "Date of birth."),
        ("sex", "text", "M or F as recorded at reception."),
        ("governing_offense", "text", "Offence category of the governing commitment."),
        ("prior_commitments", "integer", "Earlier commitments to the Department on a court sentence before this release."),
        ("prat_total", "integer 0-24", "Pembroke Release Assessment Tool total at the last assessment before release."),
        ("prat_date", "date MM/DD/YYYY", "Date of that assessment."),
        ("max_expiration_date", "date MM/DD/YYYY", "Maximum expiration date of the sentence at release; parole "
                                                    "supervision ends on this date. Blank for EXP."),
    ]),
    C.F_ADM: ("Department of Corrections, offender management system: inbound and internal movements, 1 January 2019 "
              "to 30 September 2026, for people released since 1 January 2019. One row per movement.", [
        ("doc_number", "text", "Department number."),
        ("movement_datetime", "local date and time", "Date and time of the movement."),
        ("movement_type", "text", "ADM admission to Department custody; TRN transfer between institutions; WRO out on a "
                                  "court writ; WRI back from a court writ."),
        ("movement_reason", "text", "For ADM: NEW COMMITMENT (a court sentence) or PAROLE VIOLATOR (a Board "
                                    "recommitment)."),
        ("location", "text", "Institution receiving the person (PRC is the reception centre)."),
        ("county_of_commitment", "text", "County of the governing commitment."),
    ]),
    C.F_ARR: ("State Bureau of Identification, criminal history repository: fingerprint-supported arrests of people "
              "released from Department custody since 1 January 2019, arrests from 1 January 2019 to 30 September "
              "2026. One row per arrest event.", [
        ("sbi_no", "text", "State identification number, seven digits and a check letter."),
        ("otn", "text", "Offence tracking number assigned at arrest; the courts carry it on the case."),
        ("arrest_date", "date", "Date of arrest."),
        ("arresting_ori", "text", "Arresting agency identifier (PBSP: State Police)."),
        ("top_charge_grade", "text", "Grade of the most serious charge at arrest: FA to FE felonies, M1 to M3 "
                                     "misdemeanours."),
        ("top_charge", "text", "Description of that charge."),
    ]),
    C.F_AOC: ("Administrative Office of the Courts, case management system: criminal cases carrying an offence "
              "tracking number in the Bureau's extract, as at 30 September 2026. One row per docket entry of a "
              "disposition; an amended disposition is a later row on the same docket.", [
        ("docket_no", "text", "Court docket number."),
        ("otn", "text", "Offence tracking number."),
        ("county", "text", "County of the court."),
        ("charge_grade", "text", "Grade of the lead charge as filed."),
        ("filed_date", "date YYYY-MM-DD", "Date the case was filed."),
        ("disposition", "text", "GP guilty plea, GT guilty at trial, AQ acquitted, DM dismissed, NP nolle prosequi, "
                                "OPEN no disposition yet."),
        ("disposition_date", "date YYYY-MM-DD", "Date of the disposition."),
        ("sentence_type", "text", "DOC total confinement in a State correctional institution, CJ county jail, PROB "
                                  "probation."),
        ("sentence_date", "date YYYY-MM-DD", "Date of sentence."),
        ("sentence_days", "integer", "Sentence length in days (maximum term for DOC)."),
        ("entry_date", "date YYYY-MM-DD", "Date the row was entered."),
    ]),
    C.F_XW: ("State Bureau of Identification: state identification numbers matched to Department numbers.", [
        ("sbi", "text", "State identification number written with a hyphen before the check letter."),
        ("doc_number", "text", "Department number."),
    ]),
    C.F_BLEG: ("Board of Parole, legacy case system: violation actions on reports filed to 2 January 2026, one sheet "
               "per calendar year of the report. One row per action.", [
        ("case_no", "text", "Legacy violation case number."),
        ("doc_number", "text", "Department number."),
        ("office", "text", "District office that filed the violation report (D1 Garrison, D2 Ridgway, D3 Linwood, D4 "
                           "Corliss)."),
        ("report_date", "date", "Date of the violation report."),
        ("conditions", "text", "Conditions of parole cited, by code: 01 obey all laws, 03 report as directed, 04 "
                               "approved residence, 05 travel, 07 controlled substances, 09 curfew, 11 programme."),
        ("arrest_otn", "text", "Offence tracking number of the arrest reported, where the report is of an arrest."),
        ("hold_lodged", "date", "Date the Board's detainer was lodged with a county jail."),
        ("hold_lifted", "date", "Date the Board lifted the detainer."),
        ("hold_facility", "text", "County jail holding the detainer."),
        ("action_date", "date", "Date of the action."),
        ("action", "text", "REVOKE parole revoked and the parolee recommitted, CONTINUE parole continued, POSTPONE "
                           "hearing postponed, RESCIND an earlier revocation rescinded on reconsideration."),
        ("term_days", "integer", "Recommitment term set by the Board."),
        ("hearing_officer", "text", "Hearing officer code."),
    ]),
    C.F_BNEW: ("Board of Parole, case system in use from 5 January 2026: violation cases, including the cases open in "
               "the legacy system at its close on 2 January 2026. One row per case.", [
        ("case_id", "text", "Case identifier."),
        ("doc_number", "text", "Department number."),
        ("office", "text", "District office that filed the violation report."),
        ("opened_in", "text", "LEGACY for a case opened in the legacy system and carried over, NEW otherwise."),
        ("report_date", "date YYYY-MM-DD", "Date of the violation report."),
        ("arrest_otn", "text", "Offence tracking number of the arrest reported, where the report is of an arrest."),
        ("conditions_cited", "text", "Conditions of parole cited."),
        ("hold_facility", "text", "County jail holding the Board's detainer."),
        ("hold_start", "date YYYY-MM-DD", "Date the detainer was lodged."),
        ("hold_end", "date YYYY-MM-DD", "Date the person left the county jail on the detainer."),
        ("decision", "text", "REVOKED or CONTINUED; blank while the case is open."),
        ("decision_ts", "date and time with offset", "When the decision was recorded."),
        ("revocation_term_days", "integer", "Recommitment term set by the Board."),
        ("rescinded_date", "date YYYY-MM-DD", "Date a revocation was rescinded on reconsideration."),
        ("hearing_officer", "text", "Hearing officer code."),
    ]),
    C.F_PROJ: ("Department of Corrections: people in custody on 9 October 2026 with a projected release date in "
               "calendar 2027, from sentence computation. One row per person.", [
        ("doc_number", "text", "Department number."),
        ("projected_release_date", "date YYYY-MM-DD", "Projected release date."),
        ("projected_movement", "text", "PAR parole or RPR reparole."),
        ("birth_date", "date MM/DD/YYYY", "Date of birth."),
        ("sex", "text", "M or F."),
        ("county_of_commitment", "text", "County of the governing commitment."),
        ("governing_offense", "text", "Offence category of the governing commitment."),
        ("prior_commitments", "integer", "Earlier commitments to the Department on a court sentence."),
        ("prat_total", "integer 0-24", "PRAT total at the latest assessment."),
        ("max_expiration_date", "date YYYY-MM-DD", "Maximum expiration date of the sentence."),
    ]),
    C.F_DEATH: ("Department of Health, vital records: deaths matched to people released from Department custody, "
                "1 January 2019 to 30 September 2026. One row per matched death.", [
        ("sbi_no", "text", "State identification number."),
        ("doc_number", "text", "Department number."),
        ("date_of_death", "date YYYY-MM-DD", "Date of death."),
        ("birth_date", "date MM/DD/YYYY", "Date of birth on the death record."),
        ("county_of_death", "text", "County of death."),
        ("match_score", "integer", "Probabilistic match score, 80 to 99; the Department accepts 80 and above."),
    ]),
    C.F_CASE: ("Board of Parole: parolees under supervision at each month end, by district office, January 2025 to "
               "September 2026.", [
        ("month_end", "date YYYY-MM-DD", "Last day of the month."),
        ("office", "text", "District office."),
        ("district", "text", "Parole district."),
        ("pembroke_parolees_supervised", "integer", "Pembroke parolees supervised by the office at month end."),
        ("compact_cases_received", "integer", "Parolees of other states supervised by the office under the interstate "
                                              "compact."),
        ("pembroke_parolees_supervised_elsewhere", "integer", "The office's parolees supervised in other states."),
    ]),
}


def write_dictionary(path):
    import xlsxwriter
    wb = xlsxwriter.Workbook(path)
    hf = wb.add_format({"bold": True, "bg_color": "#DDEBF7", "border": 1})
    wf = wb.add_format({"text_wrap": True, "valign": "top"})
    ws = wb.add_worksheet("Files")
    ws.write_row(0, 0, ["File", "Contents"], hf)
    ws.set_column(0, 0, 46)
    ws.set_column(1, 1, 110, wf)
    for i, (f, (desc, _)) in enumerate(DICT.items(), start=1):
        ws.write(i, 0, f)
        ws.write(i, 1, desc, wf)
    for f, (desc, fields) in DICT.items():
        name = f.split(".")[0][:31]
        sh = wb.add_worksheet(name)
        sh.write_row(0, 0, ["Field", "Type", "Description"], hf)
        sh.set_column(0, 0, 30)
        sh.set_column(1, 1, 24)
        sh.set_column(2, 2, 100, wf)
        for i, (a, b, c) in enumerate(fields, start=1):
            sh.write_row(i, 0, [a, b, c])
        sh.freeze_panes(1, 0)
    wb.close()


MANIFEST = [
    (C.F_REL, "DOC offender management system", "2026-10-06", "releases 2019-01-01 to 2026-09-30"),
    (C.F_ADM, "DOC offender management system", "2026-10-06", "movements 2019-01-01 to 2026-09-30, people released since 2019"),
    (C.F_PROJ, "DOC sentence computation", "2026-10-09", "people in custody with a projected 2027 release"),
    (C.F_ARR, "SBI criminal history repository", "2026-10-07", "arrests 2019-01-01 to 2026-09-30 of people released since 2019"),
    (C.F_XW, "SBI criminal history repository", "2026-10-07", "identifiers of people in the arrest extract"),
    (C.F_AOC, "AOC case management system", "2026-10-08", "cases carrying an OTN in the SBI extract, as at 2026-09-30"),
    (C.F_BLEG, "Board legacy case system (read-only archive)", "2026-10-05", "violation actions, reports filed to 2026-01-02"),
    (C.F_BNEW, "Board case system", "2026-10-05", "violation cases open on or opened from 2026-01-05, to 2026-09-30"),
    (C.F_DEATH, "Department of Health vital records match", "2026-10-02", "deaths 2019-01-01 to 2026-09-30"),
    (C.F_CAP, "DOC Bureau of Planning, Research and Statistics", "2026-10-06", "month ends January to September 2026"),
    (C.F_CASE, "Board of Parole statistics", "2026-10-05", "month ends January 2025 to September 2026"),
    (C.F_ACT, "Legislative Reference Bureau", "2026-07-02", "enrolled act"),
    (C.F_METH, "Commission Research and Projections Unit", "2026-10-14", "projection definitions"),
    (C.F_PRAT, "DOC Bureau of Planning, Research and Statistics", "2023-06-21", "validation study, 2019 and 2020 releases"),
    (C.F_DICT, "Commission Research and Projections Unit", "2026-10-14", "field definitions for the extracts"),
]


def write_manifest(path, counts):
    rows = []
    for f, sysname, d, cover in MANIFEST:
        rows.append((f, sysname, d, cover, counts.get(f, "")))
    return C.write_csv(path, ("file", "source_system", "extract_or_issue_date", "covers", "rows"), rows)
