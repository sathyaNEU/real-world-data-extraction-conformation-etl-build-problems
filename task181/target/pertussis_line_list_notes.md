# Pertussis line list: field notes

Southern Inland Public Health Unit, surveillance. Maintained by Tiffany Peters. Last revised 01/09/2026.

The daily extract `pertussis_notifications_2019-2026.csv` comes from the state notifiable conditions system. It holds
every pertussis notification the system has attributed to the unit since 1 January 2019, one row per laboratory
notification, as at the time the extract runs. Rows are in order of `notification_id`.

| Field | Meaning |
|---|---|
| `notification_id` | State system notification number. Numbers are issued across all conditions and units, so they are not consecutive here. |
| `received_utc` | Date and time the state system received the notification, in UTC (ISO 8601, `Z`). |
| `condition` | Always `Pertussis` in this extract. |
| `person_id` | State system person identifier. A person keeps the same identifier on every notification. |
| `sex`, `dob` | As recorded on the laboratory request. |
| `postcode` | Residential postcode on the laboratory request or as corrected at interview. |
| `specimen_date` | Date the specimen was collected (local date). |
| `onset_date` | Date of cough onset given at interview. Blank where the case was not interviewed or could not say. |
| `notifying_lab` | Laboratory that sent the notification: `Wagga Wagga Hospital Laboratory` (the district's hospital pathology service) or `Inland Pathology` (private collection network). |
| `test` | `PCR`, `Culture` or `Serology (IgA)`. |
| `result` | Result text as notified. |
| `case_status` | `Confirmed` or `Probable`, as assigned when the notification was received. |
| `mrn` | Medical record number at a Southern Inland LHD facility, eight digits, recorded at follow-up. Blank where the person has none on file. |
| `school_or_childcare` | School, preschool or childcare service the case attends or works at, as written at interview. |
| `school_role` | `Student`, `Staff` or `Parent or carer`, as ticked at interview. |

`school_or_childcare` and `school_role` were added to the case interview form on 1 September 2026 and are blank on
earlier interviews.

Linked files used in follow-up:

- `respiratory_admissions_2019-2026.csv`: inpatient episodes with a principal respiratory diagnosis at the district's
  hospitals, from the patient administration system. `mrn` is the PAS medical record number (numeric). Dates are
  dd/mm/yyyy.
- `birth_records_2024-2026.csv`: births at the district's maternity units. `baby_mrn` is the infant's medical record
  number; `mother_medicare_no` is the mother's Medicare card number followed by her individual reference number.
- `antenatal_vaccinations_2019-2026.parquet`: vaccines recorded in pregnancy for women in the district, from the
  antenatal vaccination register. `medicare_card` and `irn` identify the mother; `antigen` is the vaccine's antigen
  group (`dTpa` is the pertussis-containing vaccine); `estimated_due_date` is the due date of the pregnancy the dose was
  given in.
- `school_rosters_term3_2026.xlsx`: enrolment rosters received from schools during follow-up this term, one sheet per
  school, names removed. The school's name at the top of each sheet is as the school writes it.
- `postcode_lga_concordance.xlsx`: the unit's postcode lookup and area populations.
