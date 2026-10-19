"""The data dictionary shipped with task249's folder: what each file and column is, never what it explains."""

TEXT = """# Data dictionary: integrity desk folder, 2029 season preparation

Medhavi Assessment Labs. Compiled by Ishwar Tella (platform data) for the integrity desk, 9 May 2029.
Platform files carry UTC; client-facing files carry IST (UTC plus 5 hours 30 minutes).

## {attempts}

Platform export of MAT-R attempts in the 2028 season, July 2028. One row per attempt.

| Column | Meaning |
|---|---|
| booking_ref | the booking reference the attempt ran under |
| attempt_no | 1 for the first attempt under the booking reference, 2 for a second |
| candidate_id | the candidate the booking was made for |
| college_code | the candidate's college, short code (college register) |
| started_utc, ended_utc | attempt start and end, UTC |
| attempt_status | completed or interrupted |
| items_shown | items administered in the attempt |
| theta_logit | final estimate, logits (completed attempts) |
| se_logit | standard error of the estimate, logits (completed attempts) |
| scale_score | client scale score, 50 plus 10 per logit, whole number |
| device | the device the attempt ran on |
| platform_release | platform release in service when the attempt started |

## {exposure}

Platform log of MAT-R item administrations, July 2028. One row per item shown in an attempt.

| Column | Meaning |
|---|---|
| booking_ref, attempt_no | the attempt (as in the attempts file) |
| position | order of the item in the attempt, 1 to 16 |
| item_id | MAT-R bank item |
| shown_utc | time the item was shown, UTC |

## {bank}

MAT-R item bank, one row per item: item_id, content_area (NUM, VER, ABS), difficulty_b and discrimination_a
(two-parameter logistic, logit scale), introduced (bank release date), status (operational, retired, or pretest for
the pool replacements are drawn from).

## {register}

The 2028 season candidate register, one row per registered candidate: candidate_id, college_code, registered_on.

## {shares}

Client results feed, 2028 season. One row per share event: a candidate's MAT-R result made available to a client
account.

| Column | Meaning |
|---|---|
| share_id | share event identifier |
| candidate_id | candidate whose result was shared |
| account_code | client account (client accounts register) |
| shared_at_ist | time of the share, IST, day/month/year |
| channel | campus drive or careers page |
| share_status | active, or withdrawn by the candidate |

## {shortlists}

Selection-day operations, 2028 season. One row per account and shortlisted candidate: account_code, candidate_id,
shortlist_rank (the account's rank on MAT-R), selection_day, venue, outcome (attended, no show, rescheduled, withdrew,
result voided).

## {cases}

Integrity desk case log, 2028 season, sheet "Case log". One row per decision recorded on a case: case_ref, opened,
account_code (the client account the case concerns), candidate_id, booking_ref, finding, decided.

## {study}

MAT-V equivalence study pairs (report EQ-2028-03). One row per volunteer: volunteer_id, college_code,
mat_r_started_ist, mat_r_logit, mat_r_se, mat_v_started_ist, mat_v_logit, mat_v_se. Volunteers who did not attend
MAT-V have no MAT-V values.

## {plans}

Client plans for the 2029 season (client services), sheet "2029 plans" one row per client account; sheet "Calendar"
for the 2029 season calendar.

## {accounts}

Client accounts register: account_code, client_name, sector, onboarded, status, note.

## {colleges}

College register: college_code (short code), aishe_code, tier (T1 to T4), state, test_week_2028 (Monday of the
college's 2028 MAT-R test week), study_partner (Y for the equivalence study's partner colleges).

## {venues}

Assessment centre venues offered for 2029 selection days: venue_code, city, seats_per_session, sessions_per_day,
available_from, available_to, step_free_access (Y or N).

## {feedback}

Post-sitting candidate survey, 2028 (a sample of candidates): candidate_id, overall_rating (1 to 5),
technical_problem, comment_theme.

## Documents

{standard}: the assessment integrity standard, issue 4. {manual}: the technical manual's chapter 4 (scoring,
precision, Table 4.3). {report}: the equivalence study report.
"""


def write(path, files):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(TEXT.format(**files))
