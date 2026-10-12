"""Write the evidence pack's data files: the profile, the projection and the survey workbook (the call's inputs),
the register extracts and the query log, the code list, the case export and the laboratory results (the asks'
inputs), the stock return (a distractor) and the transmittal list."""
import csv
import datetime as dt
import os

import callsim as CS
import world as W

FILES = {
    "profile": "measles_immunity_profile_oriel_2027-05.csv",
    "projection": "population_projection_oriel_2028-01-01.csv",
    "survey": "nscs_2023_published_tables.xlsx",
    "options": "mmr_catch_up_options_autumn_2027.pdf",
    "standard": "ps07_measles_winter_planning_standard.pdf",
    "people": "register_people_active_born_1993-2017.csv",
    "events": "register_mmr_events_born_1993-2017.csv",
    "merges": "register_merges_born_1993-2017.csv",
    "queries": "gp_return_queries_mmr_2005-2027.csv",
    "lho": "lho_codes_national_2024-07.csv",
    "circular": "lho_revision_circular_2024-04.pdf",
    "notes": "register_extract_notes_2027-07.docx",
    "guidelines": "immunisation_guidelines_ch12_mmr_excerpt.pdf",
    "cases": "nds_measles_cases_oriel_2019-2027.csv",
    "lab": "nmrl_measles_results_2019-2027.csv",
    "fields": "nds_case_export_fields.txt",
    "uptake": "national_mmr_uptake_report_2027q1.pdf",
    "stock": "mmr_stock_return_2027-06-30.csv",
    "transmittal": "transmittal_list_2027-07-12.csv",
}
DISTRACTORS = ("uptake", "stock")
CALL_FILES = ("profile", "projection", "survey", "options", "standard")
ASK_FILES = ("people", "events", "merges", "queries", "lho", "circular", "notes", "guidelines", "cases", "lab", "fields")


def iso(d):
    return d.isoformat() if d else ""


def irl(d):
    return d.strftime("%d/%m/%Y") if d else ""


def write_csv(path, header, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return len(rows)


# --- the call's inputs ------------------------------------------------------------------------------------------------
def write_profile(path):
    v, basis = W.profile_values()
    rows = []
    for y in range(2027, 1926, -1):
        label = "1927 and earlier" if y == 1927 else str(y)
        rows.append([label, "%.1f" % v[y], W.PROFILE_NOTE_BASIS[basis[y]]])
    return write_csv(path, ["year_of_birth", "per_cent_immune", "basis"], rows)


def write_projection(path, reg):
    rows = []
    for c in W.COUNTIES:
        for a in CS.AGES:
            age = "100 and over" if a == 100 else str(a)
            yob = "1927 and earlier" if a == 100 else str(2027 - a)
            rows.append([c, age, yob, int(reg[c][a])])
    return write_csv(path, ["county", "age_at_1_january_2028", "year_of_birth", "persons"], rows)


def write_survey(path, P, nat):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Notes"
    notes = [
        ("National Social Contact Survey 2023", True),
        ("Published tables, version 1.1, 8 March 2024", False),
        ("", False),
        ("Fieldwork ran from 16 January to 26 May 2023 on school days and weekends, outside the February mid-term and "
         "Easter breaks.", False),
        ("%s participants each recorded everyone they had contact with on one assigned day: a conversation of at least "
         "three words in each other's presence, or any skin-to-skin contact. Contacts were recorded with their age or an "
         "age range; a range was assigned to its midpoint." % format(sum(W.SURVEY_PARTICIPANTS), ","), False),
        ("Children under 10 were reported by a parent or guardian; participants aged 10 to 15 completed the diary with a "
         "parent's help.", False),
        ("Participants are weighted by age group, sex, region and day of the week to the population at 1 January 2023.", False),
        ("Table 2 gives the mean number of contacts per participant per day, by the participant's age group (rows) and the "
         "age group of the person contacted (columns), corrected for reciprocity: for every pair of age groups the total "
         "number of contacts is made the same in both directions, using the population in Table 1.", False),
        ("Contacts with the same person on the day are counted once.", False),
        ("", False),
        ("Survey team: National Social Contact Survey, 2023 round. Tables may be reproduced with acknowledgement.", False),
    ]
    for i, (t, b) in enumerate(notes, start=1):
        if t:
            ws.cell(row=i, column=1, value=t).font = Font(bold=b, size=12 if b else 11)
    ws.column_dimensions["A"].width = 120
    t1 = wb.create_sheet("Table 1")
    t1.append(["Table 1. Participants and population by age group"])
    t1["A1"].font = Font(bold=True)
    t1.append(["Age group", "Participants", "Participants, weighted (%)", "Population, 1 January 2023"])
    N = CS.to_groups(nat)
    wshare = N / N.sum() * 100
    for k, lab in enumerate(W.GROUP_LABELS):
        t1.append([lab, W.SURVEY_PARTICIPANTS[k], round(float(wshare[k]), 1), int(N[k])])
    t1.append(["All ages", sum(W.SURVEY_PARTICIPANTS), 100.0, int(N.sum())])
    for col, wdt in zip("ABCD", (14, 14, 26, 28)):
        t1.column_dimensions[col].width = wdt
    t2 = wb.create_sheet("Table 2")
    t2.append(["Table 2. Mean contacts per participant per day, by age group of participant (rows) and age group of "
               "contact (columns), all settings, corrected for reciprocity"])
    t2["A1"].font = Font(bold=True)
    t2.append(["Participant age group"] + W.GROUP_LABELS)
    for i, lab in enumerate(W.GROUP_LABELS):
        t2.append([lab] + [float("%.2f" % P[i, j]) for j in range(W.NG)])
        for j in range(W.NG):
            t2.cell(row=i + 3, column=j + 2).number_format = "0.00"
    t2.column_dimensions["A"].width = 22
    for r in t2.iter_rows(min_row=2, max_row=2):
        for c in r:
            c.font = Font(bold=True)
            c.alignment = Alignment(horizontal="center")
    wb.save(path)


# --- the asks' inputs ---------------------------------------------------------------------------------------------------
def write_people(path, people, active):
    rows = []
    for p in sorted((p for p in people if p.status in active), key=lambda p: p.pid):
        rows.append([p.pid, iso(p.dob), p.sex, p.lho, iso(p.lho_recorded), iso(p.registered), p.practice])
    return write_csv(path, ["person_number", "date_of_birth", "sex", "lho_code", "lho_recorded", "registered_on",
                            "gp_practice"], rows, crlf=True)


def write_events(path, events):
    rows = []
    for e in events:
        rows.append([e.eid, e.pid, "MMR", e.product, iso(e.date), e.given_by, e.source_ref, iso(e.loaded)])
    return write_csv(path, ["event_number", "person_number", "vaccine", "product", "date_given", "given_by",
                            "source_ref", "loaded_on"], rows, crlf=True)


def write_merges(path, merges):
    rows = [[m["retired"], m["surviving"], iso(m["merged_on"]), m["reason"]] for m in merges]
    return write_csv(path, ["retired_number", "surviving_number", "merged_on", "reason"], rows, crlf=True)


def write_queries(path, log):
    rows = [[r["query_ref"], r["line_ref"], r["practice"], iso(r["raised"]), r["reason"], r["outcome"] if r["closed"]
             else "Open", r["replaced_by"], iso(r["closed"])] for r in log]
    return write_csv(path, ["query_ref", "line_ref", "practice", "raised_on", "reason", "outcome", "replaced_by",
                            "closed_on"], rows)


def write_lho(path):
    rows = []
    for code in sorted(set(W.REGION_LHO_NEW) | set(W.OTHER_LHO)):
        if code in W.REGION_LHO_NEW:
            name, county = W.REGION_LHO_NEW[code]
            region = W.REGION
        else:
            name, county, region = W.OTHER_LHO[code]
        rows.append([code, name, county, region, "2024-07-01"])
    return write_csv(path, ["lho_code", "lho_name", "county", "health_region", "in_force_from"], rows)


def write_cases(path, cases):
    rows = []
    for c in cases:
        rows.append([c["case_id"], c["legacy_ref"], irl(c["notified"]), irl(c["onset_date"]), irl(c["date_of_birth"]),
                     c["sex"], c["county"], c["classification"], c["importation"], c["outbreak_ref"], c["epi_link"],
                     c["hospitalised"], c["mmr_doses_reported"], c["comments"]])
    return write_csv(path, ["case_id", "legacy_ref", "notified", "onset_date", "date_of_birth", "sex", "county",
                            "classification", "importation", "outbreak_ref", "epi_link", "hospitalised",
                            "mmr_doses_reported", "comments"], rows, crlf=True)


def write_lab(path, lab):
    rows = [[r["specimen_id"], r["case_id"], irl(r["specimen_date"]), r["specimen_type"], r["test"], r["result"],
             r["genotype"]] for r in lab]
    return write_csv(path, ["specimen_number", "case_id", "specimen_date", "specimen_type", "test", "result",
                            "genotype"], rows, crlf=True)


def write_stock(path, stock):
    rows = [[r["store"], r["product"], r["batch"], iso(r["expiry"]), r["doses_on_hand"], iso(r["counted_on"])]
            for r in stock]
    return write_csv(path, ["store", "product", "batch", "expiry", "doses_on_hand", "counted_on"], rows)


TRANSMITTAL = [
    ("profile", "Measles immunity profile by year of birth, Oriel Health Region, projected to 1 January 2028",
     "National immunisation programme", "2027-05-14"),
    ("projection", "Projected usual residents at 1 January 2028 by county and single year of age",
     "Department of Public Health, health intelligence", "2027-03-22"),
    ("survey", "National Social Contact Survey 2023, published tables (version 1.1)", "National Social Contact Survey",
     "2024-03-08"),
    ("options", "Autumn 2027 MMR catch-up: options paper", "Regional Immunisation Office", "2027-06-09"),
    ("standard", "PS-07 Measles winter planning standard (version 3.0)", "Department of Public Health", "2026-03-10"),
    ("people", "Register extract: people with an active registration, born 1993 to 2017", "Regional immunisation register",
     "2027-06-30"),
    ("events", "Register extract: MMR events for registrations born 1993 to 2017", "Regional immunisation register",
     "2027-06-30"),
    ("merges", "Register extract: merged duplicate registrations, born 1993 to 2017", "Regional immunisation register",
     "2027-06-30"),
    ("queries", "Query log for GP return lines with an MMR dose, from January 2005", "Regional Immunisation Office",
     "2027-07-03"),
    ("lho", "Local health office codes in force from 1 July 2024", "National health service planning unit", "2024-07-01"),
    ("circular", "Local health office areas: revision of 1 July 2024 (circular)", "National health service planning unit",
     "2024-04-12"),
    ("notes", "Register extract notes", "Regional immunisation register", "2027-07-05"),
    ("guidelines", "National immunisation guidelines, chapter 12 (MMR), sections 12.4 to 12.6",
     "National immunisation programme", "2025-11-24"),
    ("cases", "Notifiable disease system: measles cases resident in Oriel Health Region, notified from 2019",
     "Department of Public Health, surveillance", "2027-07-06"),
    ("lab", "National measles reference laboratory results for those cases", "National measles reference laboratory",
     "2027-07-06"),
    ("fields", "Case export field notes", "Department of Public Health, surveillance", "2025-03-03"),
    ("uptake", "MMR uptake at 24 months and 5 years, quarter 1 2027", "National immunisation programme", "2027-06-20"),
    ("stock", "MMR stock return at 30 June 2027", "Regional Immunisation Office", "2027-06-30"),
]


def write_transmittal(path, rows_by_key):
    rows = []
    for key, desc, source, asof in TRANSMITTAL:
        n = rows_by_key.get(key)
        rows.append([FILES[key], desc, source, asof, "" if n is None else n])
    return write_csv(path, ["file", "description", "source", "as_of", "rows"], rows)
