# P10 — Trial-results compliance report card: submitted is not posted, and completion is not primary completion

| Field | Value |
|---|---|
| Domain | Pharma regulatory transparency / clinical-trial disclosure |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (five lowest-compliance sponsors named) |
| Core technique | Rule-based eligibility screen on a relational registry; deadline computation from the correct date field and date type; event-table reasoning (submission vs QC posting); lead-vs-collaborator role filtering |
| Trap family (honest data) | Posting date used instead of submission date; study completion instead of primary completion; anticipated dates treated as actual; collaborators counted |
| Primary sources | ClinicalTrials.gov via the AACT database (CTTI) |

## 1. The real-world project

A patient-advocacy group publishes an annual **results-reporting report card** under FDAAA 801 / 42 CFR Part 11:
sponsors of applicable clinical trials must submit summary results within one year of the primary completion date. The
group names the **five lead sponsors with the lowest on-time submission rate** among sponsors with at least 30 trials
due. Last year, two named sponsors disputed the list with evidence; both disputes were upheld.

## 2. The business decision (one deterministic recommendation)

**Which five sponsors are named on the report card for the snapshot dated in the folder, and which sponsor is sixth?**

Rules (report-card methodology):

* Applicable-trial screen: `study_type = Interventional`; phase not `Early Phase 1` or `Phase 1` (combined phases such as
  `Phase 1/Phase 2` are retained); at least one intervention of type Drug, Biological, Device, Combination Product or
  Genetic; at least one U.S. facility **or** `is_fda_regulated_drug`/`is_fda_regulated_device` true;
  `primary_completion_date_type = Actual`; primary completion on or after 2017-01-18.
* Due date = actual primary completion date + 365 days. Trials with a certification/extension request
  (`disposition_first_submitted_date`) submitted before the due date are not yet due and are excluded.
* Due set = due date ≤ snapshot date − 30 days.
* On time = `results_first_submitted_date` ≤ due date (submission, not public posting).
* Sponsor = `sponsors.name` where `lead_or_collaborator = lead`, exact string after trimming whitespace.
* Rank ascending by on-time rate (ties: more trials due ranks lower); sponsors with ≥ 30 due trials only.

## 3. Why this gets overlooked in real projects

* `results_first_posted_date` is the date the public sees results, and it is the date shown on study pages, so it feels
  like "when they reported". The legal obligation is submission; QC review can add months.
* `completion_date` and `primary_completion_date` sit side by side; the former is later, which quietly makes everyone
  look more compliant.
* Date *type* columns (`Actual`/`Anticipated`) are separate; filtering dates alone pulls in trials that have not finished.
* The `sponsors` table holds collaborators too; a join without the role filter assigns a trial to every collaborator.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `studies.txt` | pipe-delimited | ~500k | AACT flat-file snapshot (aact.ctti-clinicaltrials.org) | ClinicalTrials.gov public data (NLM terms); AACT by CTTI | Core study facts |
| 2 | `sponsors.txt` | pipe-delimited | ~800k | AACT | same | Lead/collaborator |
| 3 | `interventions.txt` | pipe-delimited | ~900k | AACT | same | Intervention types |
| 4 | `facilities.txt` | pipe-delimited | ~3M | AACT | same | U.S. sites |
| 5 | `calculated_values.txt` | pipe-delimited | ~500k | AACT | same | Cross-check only |
| 6 | `pending_results.txt` | pipe-delimited | ~50k | AACT | same | Submission / return events |
| 7 | `aact_data_dictionary.xlsx` | XLSX | — | AACT | same | Field definitions |
| 8 | `42cfr11_results_deadlines_extract.pdf` | PDF | — | eCFR (42 CFR Part 11) | Public domain | Legal deadline basis |
| 9 | `ctgov_data_element_definitions.pdf` | PDF | — | ClinicalTrials.gov | Public domain | Date field meanings |
| 10 | `report_card_methodology.pdf` | PDF | — | Task author | — | Rules in §2 |
| 11 | `snapshot_metadata.json` | JSON | 1 | Task author | — | Snapshot date |

## 5. Deterministic solution path

1. Apply the applicable-trial screen with the four tables; keep actual primary completion dates on/after 2017-01-18.
2. Compute due dates; drop trials with a timely certification/extension; apply the snapshot cut.
3. Flag on time by first submission date.
4. Attribute to lead sponsor; keep sponsors with ≥ 30 due trials; compute rates; rank ascending.
5. Name five; report sixth and the rate gap; quantify how the list changes under posting-date or completion-date variants.

## 6. The traps

**Trap A — posting date.** Sponsors with long QC cycles fall into the bottom five although they submitted on time.

**Trap B — completion date.** Deadlines move later; low-compliance sponsors climb out of the bottom five.

**Trap C — anticipated dates.** Trials not yet complete enter the due set, depressing sponsors with large active
pipelines.

**Trap D — collaborators.** Large companies collaborating on academic trials inherit those trials' late submissions.

**Trap E — over-broad phase exclusion.** Excluding `Phase 1/Phase 2` with a substring filter shrinks some sponsors below
the 30-trial floor.

## 7. Why the data is honest

AACT mirrors ClinicalTrials.gov exactly. Each date and its type are what the sponsor registered and what the registry
logged. The legal standard and field definitions are public; the challenge is applying them precisely.

## 8. Draft task prompt (prose)

> Our report card names the five lead sponsors with the lowest on-time results-submission rate among those with at least
> thirty applicable trials due, under the methodology in the folder. Using the AACT snapshot, tell me the five and who
> came sixth. Deliver `report_card.csv` with every qualifying sponsor's trials due, trials submitted on time, late, not
> yet submitted, on-time rate and rank, plus `report_card_chart.png`, a ranked bar chart of on-time rates for the twenty
> lowest sponsors with the named five highlighted and the count of trials due labelled on each bar. Close with
> `report_card_note.pdf`, a page leading with the five names, the gap between fifth and sixth, and which named sponsors
> would leave the list if posting dates had been used instead of submission dates.

## 9. Deliverables

* `report_card.csv`, `report_card_chart.png`, `report_card_note.pdf`.

## 10. Where 25+ rubric criteria come from

* Five named sponsors + sixth + gap; trials-due and on-time counts for those six; rates for 20 charted sponsors;
  posting-date variant differences; screen counts (applicable, due).

## 11. Golden-output checklist

* Screen applied with actual primary completion dates; certification exclusions; submission dates; lead sponsors only;
  list and gap stated.

## 12. Build notes (scope tuning)

* Run the method and each trap variant on the frozen snapshot; adjust the sponsor floor (25–40) so at least two traps
  change the named five.
* Record the AACT snapshot date; AACT refreshes daily.
