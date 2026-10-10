"""The words of the constructed documents, kept apart from the writers so the single-statement and
vocabulary sweeps in checks.py can read them."""

REMIT_TITLE = "External review of deaths after delayed escalation to critical care, 2027-28"
REMIT = [
    ("meta", "Terms of reference. Board paper WRHB/26/097, approved at the meeting of 17 September 2026."),
    ("meta", "Sponsor: Andrea Davey, Head of Quality Surveillance. Chair: Norman Scott."),
    ("h", "1. Purpose"),
    ("p", "The Board will fund one twelve-month external review in one of the eight acute trusts it commissions. "
          "Thornleholm Clinical Review LLP has been appointed to carry it out, with Benjamin Davies as lead reviewer. "
          "Fieldwork opens on 1 April 2027 and the final report comes to the Board in May 2028."),
    ("h", "2. Scope"),
    ("p", "The review examines adult patients referred from a ward or an emergency department for a level 3 critical "
          "care bed who waited more than four hours from the decision to admit to the assignment of a bed, and who "
          "died within 30 days of the decision to admit."),
    ("p", "Patients transferred between hospitals are reviewed with the trust that referred them. Children, maternity "
          "referrals and patients referred from another critical care unit are outside the scope."),
    ("h", "3. How the engagement is judged"),
    ("p", "The Board will judge the engagement by the number of deaths its reviewers confirm as avoidable because of "
          "problems in the reviewed trust's own care."),
    ("h", "4. Methodology note"),
    ("p", "A trust's decisions about the use of its own beds and staff are part of its own care."),
    ("h", "5. Placement"),
    ("p", "The engagement is placed once, on the latest four complete quarters of the network's referral record. "
          "The placement is not revisited when later quarters close."),
    ("p", "The National Rapid Review Programme screens trusts on the number of referrals waiting more than four "
          "hours from receipt of the referral. Sharon Banks, the programme coordinator, will present the programme's "
          "screen at the November meeting, and members will have it in front of them when the placement is decided."),
    ("h", "6. Information and access"),
    ("p", "The Board's information team will give the reviewers the network referral record, the critical care unit "
          "feed, the daily bed returns, the unit register and linked hospital episode data for the reviewed trust. "
          "Case-note access is under the 2025 data sharing agreement between the Board and the eight trusts, schedule "
          "C. The reviewed trust names a single point of contact by 31 January 2027."),
    ("h", "7. Reporting"),
    ("p", "The reviewers report quarterly to the Quality and Safety Committee and once to the full Board. The reviewed "
          "trust sees the draft report fourteen days before it is tabled. The Board will tell the eight trusts which "
          "trust has been chosen in December 2026."),
    ("h", "8. Timetable"),
    ("table", [["Milestone", "Date"],
               ["Placement decided by the Board", "26 November 2026"],
               ["Trusts informed", "December 2026"],
               ["Point of contact named", "31 January 2027"],
               ["Fieldwork opens", "1 April 2027"],
               ["Interim report to committee", "October 2027"],
               ["Final report to the Board", "May 2028"]]),
    ("foot", "Wenmarsh Regional Health Board. Board papers are not for onward circulation until published."),
]

GUIDE_TITLE = "Wenmarsh Adult Critical Care Network: referral and unit data"
GUIDE_SUB = "Extract of 14 August 2026, prepared for the Board's external review placement. Field guide, issue 2, 28 September 2026."
GUIDE_BY = "Diana Smith, Information Manager, Wenmarsh Regional Health Board"
GUIDE_INTRO = [
    "This folder holds the network's referral record and unit data for decisions to admit from 1 July 2023 to "
    "30 June 2026, with the papers the Board asked for. The extract was taken on 14 August 2026.",
    "Times are as each system recorded them.",
    "Death registrations reach the regional data service within 14 days of a death.",
]
GUIDE_FIELDS = {
    "critical_care_referrals_202307_202606.csv": [
        ("referral_id", "Platform reference (R, year and month, sequence) or migrated CCRS reference (CC and seven digits)."),
        ("received_at", "Time the critical care outreach team received the referral."),
        ("referring_trust", "Trust code of the referring hospital."),
        ("referred_from", "Ward or department code at the referring hospital. ED is the emergency department and REC "
                          "theatre recovery. AMU (acute medical unit), SAU (surgical assessment unit), SDU (surgical "
                          "day unit) and CCU (coronary care unit) are wards, as is each W code."),
        ("patient_key", "Regional patient key."),
        ("dta_at", "Time of the decision to admit to critical care."),
        ("level_of_care", "Level of critical care on the referral, 2 or 3."),
        ("outcome", "Admitted, Stood down, or Died before admission."),
        ("outcome_at", "Time of the outcome. For an admission, the time the bed was assigned. Blank where the source "
                       "record holds no time."),
        ("admitting_unit", "Unit code the patient was admitted to, from the unit register."),
    ],
    "acc_unit_stays_202306_202606.parquet": [
        ("stay_id", "Row identifier in the unit feed."),
        ("unit_code", "Unit code, from the unit register."),
        ("referral_id", "Referral that led to the admission, where there was one. Admissions before 1 July 2023 "
                        "carry referral numbers from before this extract."),
        ("patient_key", "Regional patient key."),
        ("admitted_at", "The minute the bed was assigned to the patient."),
        ("discharged_at", "The minute the patient left the bed."),
        ("admission_type", "01 unplanned local admission; 02 unplanned transfer in; 03 planned transfer in; "
                           "04 planned local surgical admission; 05 planned local medical admission; 06 repatriation."),
        ("source_location", "01 theatre and recovery; 02 recovery only; 03 other intermediate care area; "
                            "04 emergency department; 05 imaging; 06 ward; 07 clinic; 08 home; 09 other."),
    ],
    "acc_bed_return_0800_202306_202606.csv": [
        ("unit_code", "Level 3 unit."),
        ("return_date", "Date of the return."),
        ("beds_open", "Staffed critical care beds open at 08:00."),
        ("beds_occupied_0800", "Beds occupied at 08:00."),
    ],
    "acc_unit_register.csv": [
        ("unit_code", "Unit code used across the network's data."),
        ("trust_code", "Trust that runs the unit."),
        ("care_level", "Highest level of care the unit is commissioned to provide."),
        ("commissioned_beds", "Commissioned beds."),
        ("valid_from, valid_to", "Each row applies from valid_from to valid_to inclusive. A blank valid_to marks the "
                                 "row in force today."),
    ],
    "interhospital_transfer_audit_202307_202606.csv": [
        ("transfer_ref", "Audit reference."),
        ("patient_key", "Regional patient key."),
        ("from_trust, from_site", "Sending trust and hospital."),
        ("to_unit", "Receiving critical care unit."),
        ("decision_at", "Time of the decision to admit at the sending hospital."),
        ("bed_confirmed_at", "Time the network bed bureau allocated the bed at the receiving unit."),
        ("departed_at, arrived_at", "Times recorded by the transfer team."),
    ],
}

LEGACY_TITLE = "CCRS export specification for platform migration"
LEGACY_SUB = "Version 2.3, 12 February 2024. CCRS application support, Wenmarsh network informatics."
LEGACY = [
    ("h", "1. Purpose"),
    ("p", "This specification describes the CCRS records exported for loading into the regional referral platform at "
          "switch-off, and the network bed-management rows exported with them. It covers referrals with a decision to "
          "admit from 1 July 2023 until the last CCRS day."),
    ("h", "2. Referral records (CCRS)"),
    ("p", "Referral numbers are CC followed by seven digits, issued in order of receipt."),
    ("p", "All CCRS timestamps are held in UTC."),
    ("p", "level_of_care holds the level of care requested by the referring team, as entered on the referral form. "
          "The critical care decision, and any later change, is held in the referral level entries."),
    ("p", "The referral record holds no admission time. Admissions are held in the bed-management feed."),
    ("h", "3. Referral level entries (CCRS)"),
    ("p", "One row for each entry made against a referral: REQUEST, REVISED REQUEST, DECISION and LEVEL CHANGE, each "
          "with the time recorded and the level entered."),
    ("h", "4. Bed-management feed"),
    ("p", "The network bed-management feed records local time. Until switch-off it held one row per bed episode, "
          "from the time the patient was placed in the bed to the time the patient left it: a patient moved to "
          "another bed starts a new row, which repeats the admission type and source location of the admission. "
          "The CCRS referral number is held on the first row of an admission."),
    ("h", "5. Field mapping"),
    ("table", [["Source field", "Platform field"],
               ["REF_NO", "referral_id"], ["RECV_DTTM", "received_at"], ["TRUST", "referring_trust"],
               ["WARD", "referred_from"], ["PAT_KEY", "patient_key"], ["DTA_DTTM", "dta_at"],
               ["LOC", "level_of_care"], ["OUTCOME", "outcome"], ["OUTCOME_DTTM", "outcome_at"],
               ["DEST_UNIT", "admitting_unit"], ["BED_FROM (bed-management)", "admitted_at"],
               ["BED_TO (bed-management)", "discharged_at"]]),
    ("p", "Sign-off: CCRS application support and the platform migration lead, 12 February 2024."),
]

APC_SPEC = """REGIONAL DATA SERVICE
Admitted patient care extract specification RDS-APC-07, issue 4
Extract for Wenmarsh Regional Health Board, run 14 August 2026

Scope
  All admitted patient care episodes from 1 April 2022 to 13 August 2026, at the eight Wenmarsh acute trusts,
  for patients with a referral in the network critical care referral record (1 July 2023 to 30 June 2026).

Fields (apc_episodes_referred_patients_2022-2026.parquet)
  episode_id              Episode identifier.
  spell_id                Hospital spell; one spell may hold several consultant episodes.
  patient_key             Regional patient key.
  provider_code           Trust code.
  admission_date          Start of the hospital spell.
  admission_method        11 elective waiting list, 12 elective booked, 21 emergency via A&E, 22 emergency via GP,
                          28 other emergency, 2B emergency transfer from another hospital, 81 transfer from
                          another hospital, not an emergency.
  episode_order           Order of the episode within the spell.
  episode_start           Start of the consultant episode.
  episode_end             End of the consultant episode (blank while the episode is open).
  main_specialty          Main specialty code of the consultant.
  discharge_date          End of the spell, on the spell's last episode.
  discharge_method        1 discharged on clinical advice, 2 self-discharged, 4 died.
  discharge_destination   19 usual place of residence, 49 another NHS hospital, 79 not applicable (patient died).
  date_of_death           Date of death from death registrations.

Linkage
  date_of_death is linked from death registrations through the verified NHS number and appears on every episode
  recorded under the patient's verified key. Episodes recorded while a patient was held under a temporary
  registration keep the temporary key and carry no date of death. pas_patient_key_links_2023-2026.csv gives the
  verified key for each temporary key.

Open episodes on the run date carry no end date and no discharge fields.

Companion extract RDS-THR-02, issue 1 (rds_theatre_cases_2023-2026.parquet)
  Scope: theatre cases from 1 June 2023 to 13 August 2026 at the eight trusts' hospitals for patients with a
  referral in the network critical care referral record or a stay in the network unit feed. Times are local, as
  recorded by the theatre management systems.
  case_id                 Theatre case identifier.
  patient_key             Regional patient key, as held by the theatre system on the day.
  provider_code           Trust code.
  site_name               Hospital where the operation took place.
  case_date               Date of the operation.
  urgency                 Elective, Expedited, Urgent or Immediate (NCEPOD classification).
  procedure_code          Main procedure, OPCS-4.
  into_theatre_at         Patient into the operating theatre.
  out_of_theatre_at       Patient out of the operating theatre.
  left_recovery_at        Patient left the recovery area.
  recovery_destination    Where the patient went from recovery: Critical care unit, Ward or Home.

Contact: regional data service, extracts desk.
"""

BOARD_PAPER_TITLE = "Level 3 critical care capacity: winter 2023-24 and from April 2024"
BOARD_PAPER_SUB = "Wenmarsh Adult Critical Care Network Board, 21 November 2023. Paper ACCN/23/41."
BOARD_PAPER_BY = "Maria Reynolds, Critical Care Network Manager"
BOARD_PAPER = [
    ("h", "Summary"),
    ("p", "The network board is asked to approve two changes to level 3 capacity agreed in principle with the trusts "
          "in October."),
    ("h", "1. Ellerdyke"),
    ("p", "Ellerdyke Hospitals NHS Trust has been unable to staff its eight level 3 beds safely since the summer. "
          "From 1 April 2024 the Ellerdyke unit will provide level 2 care only, with six beds. Ellerdyke patients "
          "who need level 3 care will be referred through the network to the other units. The unit keeps its code "
          "in the register."),
    ("h", "2. Pellowham winter beds"),
    ("p", "Pellowham Hospitals NHS Trust will open three level 3 beds alongside its high dependency unit from "
          "4 December 2023 to 31 March 2024, staffed by the winter bank. They will report as a separate unit."),
    ("h", "3. Network arrangements"),
    ("p", "Transfers between trusts will continue to be agreed through the network's bed bureau. The register and "
          "the daily bed returns will be updated from the dates above. The network will review both changes in "
          "summer 2024."),
    ("h", "Recommendation"),
    ("p", "The board approves both changes. Approved at the meeting on 21 November 2023."),
]

CAPACITY_NOTES = [
    "Wenmarsh Adult Critical Care Network: monthly capacity report",
    "Version 3.4. Refreshed 20 August 2026 from the daily bed returns and the referral platform.",
    "Owner: Maria Reynolds, Critical Care Network Manager. Distribution: network board, trust critical care leads, "
    "Wenmarsh Regional Health Board quality surveillance.",
    "Occupancy is the 08:00 daily bed return for the level 3 units.",
    "Referrals waiting over four hours are level 3 referrals not given a bed within four hours of receipt of the "
    "referral, the network's operational standard, counted by month of receipt. Referral waits are reported from "
    "April 2024.",
    "The report describes bed capacity and flow. It does not compare trusts' standards of care.",
]
