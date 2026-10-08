# FC15 — Which new repository gets February's spotlight, when "outside the organisation" means outside it on the day of the star

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · developer platforms and content promotion |
| Mirrors | Promoting new items on early engagement when part of it came from the creator's own circle at the time (GitHub Explore and npm trending, App Store and Google Play featuring, YouTube and Instagram creator promotion where launch-week engagement includes the creator's own team) |
| Decision shape | Which of N gets one scarce thing: the newsletter's single February spotlight, with its sponsored CI year, among eight shortlisted repositories |
| Committed call | The spotlighted repository, with its expected 90-day external stars in thousands to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · the population a forecast counts is defined by membership on each star's date, through an effective-dated register, not by the current-membership flag, with a subgroup-validated decay below it |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #13 validates on one population, applies to another · #15 follows the requester's hunch over the rule |
| Calibration form | Pilot log: twelve months of spotlight decisions, each month's full shortlist with the model's predictions and every candidate's realised 90-day external stars |
| Driving force | The featuring rule counts only stars from accounts that were not members of the owning organisation when they starred. The stargazer export's member flag shows membership today. Repository B's launch was starred by 140 contractors whose temporary memberships expired three weeks later, so today's flag counts them as outsiders and B's first week looks like the strongest organic launch on the list. Against the membership register's join and end dates, 48% of B's "external" first week was internal. No column carries membership on the day of the star. |

## 1. Situation

A developer platform spotlights one new repository a month in its newsletter, with a year of sponsored CI. The featuring memo sends the
spotlight to the shortlisted repository with the most expected external stars in its first 90 days. It counts only stars from accounts
that were not members of the owning organisation when they starred, and it files the forecasting model: log 90-day external stars on log
first-week external stars, fitted on the 2023 cohort, with a smearing factor. The editors shortlisted eight repositories that went public
in early January.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: star events, the stargazer export and its flag, the membership register, the referral report and
  the pilot log. No one's claim about their own numbers is overturned. The difficulty is which stars the forecast counts, and on which
  date that is decided.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the partner's ranking. The filed model on flag-external stars, de-duplicated and
  subgroup-calibrated, still names B.
* **Instrument repair.** Make every star event and every flag perfect; they are. The flag answers "member now", and the rule asks
  "member then". A better flag of today still answers the wrong date.
* **Lens swap.** The naive read and the answer differ in population: stars from accounts that are outsiders today against stars from
  accounts that were outsiders on the day they starred.

## 3. The driving force

A strong solver applies the filed model to external first-week stars using the export's member flag, removes repeat stars, and sees in
the pilot log that social-burst launches decay faster than the model's 2023 cohort, so it calibrates that subgroup apart. Every step is
right, and the list then names B, a company launch with a large, steady first week. The rule's word is "when they starred". B's
organisation brought 140 contractors onto temporary memberships for its launch hackathon. They starred the repository that week, and
their memberships ended three weeks later. Today's flag sees outsiders. The membership register's effective dates show members. Removing
them halves B's external first week and cuts its expected 90-day stars from 5.0 to 2.9 thousand. Membership on the star date is a join
from each stargazer to the register, compared with the event's timestamp. Nothing on the shortlist hints at it.

## 4. The ladder

| Rung | Construction | Names (expected 90-day external stars, thousands) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The filed model on first-week stars from accounts the export flags as non-members | A (6.9 against 5.8) | The memo's model on the memo's population, as the export presents it | The memo's star definition: the first star per account and repository; A's launch giveaway produced 1,100 star-unstar-restar cycles |
| 1 | Hygiene: repeat stars removed | C (5.8 against 5.0) | Clean counts and the filed model | **E17 (validated on one population, applied to another):** the pilot log and the referral report show social-burst launches realising 58% of the model's prediction; the 2023 cohort was 90% steady launches |
| 2 | The model calibrated separately for social-burst launches (their own smearing factor from the pilot log) | B (5.0 against 4.1) | The forecast now fits every subgroup the pilot shows | The membership register's join and end dates: 140 of B's flag-external first-week stars came from accounts that were members when they starred |
| 3 | **Decisive:** external stars defined by membership on each star's date (stargazer joined to the register at the event timestamp), then the calibrated model | **D (4.1 against 3.4)** | — | — |

* **Position table.** D, a community-built data-pipeline tool, is 5th on rung 0, 4th on rung 1, 2nd on rung 2 (1.22× behind B), and
  leads only rung 3. Rung margins are 1.19×, 1.16×, 1.22× and 1.21×.
* **Discriminator dominance.** B carries a 1.22× lead into rung 3. D's edge on the decisive axis, the share of its flag-external first
  week that was external on the day, is 1.92× (100% against 52%), above the required 1.2 × 1.22 = 1.46.
* **Partial correction priced (L3).** Removing today's members as well as the flag's members does nothing, since that is the flag.
  Removing only stargazers whose accounts were created in launch week catches 30 of the 140 and leaves B ahead at 4.6.
* **Grid.** Repeat stars (kept, removed) × model (pooled, subgroup) × membership (today, star date) gives 8 cells, which name A, C, B or
  D. Only star-date membership with both lower corrections names D. The nearest wrong cell is star-date membership without the subgroup
  calibration, which names C at 5.8.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo says "when they starred", once. No document says that today's flag differs or that B ran a contractor
   hackathon, and the register ships to support an unrelated ask.
2. **Corpus blind for a computable reason.** *In every pilot month the spotlighted repository was community-owned, because the pilot kept
   organisation-owned repositories out of the spotlight.* The model's calibration on spotlight outcomes never met an insider star, and the
   flag and the register agree for 96% of all stargazers.
3. **No arithmetic symptom.** Star counts tie to events, flags to the export, and the shortlist to the editors' file. Nothing fails under
   the flag.
4. **Not a row predicate.** Membership on a date is a property of a different entity (the person) at a time set by another table (the
   star event), reached through an effective-dated join, then aggregated per repository.
5. **The enumeration is arithmetic.** Which stars were internal is computed by interval comparison. No column says so.
6. **No cutover date.** Memberships start and end continuously, and nothing steps in any series the solver would align.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The pilot log: twelve monthly shortlists (96 repositories), each with first-week stars, the model's prediction, the spotlight
  decision and every candidate's realised 90-day external stars.
* **What it certifies.** The filed model on steady community launches (realised within 5% of predicted in 58 of 60), and the social-burst
  subgroup's lower realisation (58%) that rung 2 calibrates. A back-tester is confirmed at rung 2.
* **What it is blind to.** Insider stars among spotlights (above).
* **Twin pair.** Shortlisted repositories P-0611 and P-0907, both organisation-owned and never spotlighted, are identical on every
  shortlist column: flag-external first-week stars (812), language, launch source and owner type. They realised 2,140 and 1,050 external
  stars (2.0×), because 50% of P-0907's flag-external first week were members on the day. Only star-date membership reproduces both.
* **Resemblance points at the decoy.** B resembles the pilot's best-realising spotlights on every shortlist column: a steady, organic-
  looking first week from a well-known owner.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The featuring memo: the spotlight goes to the shortlisted repository with the most expected external stars in its first
  90 days public; a star counts only if it is an account's first star on the repository and the account was not a member of the owning
  organisation when it starred; the model is log–log OLS on the 2023 cohort with Duan smearing.
* **Empirical pins.** The social-burst subgroup's smearing, from the pilot log. Membership on each star's date, from the register.
* **Voices.** The newsletter editor: "Big launches with company backing always do best in the spotlight." The developer-relations lead:
  "Stars are stars; we've never needed to look behind them."
* **Licensed wrong basis.** The memo records that the sponsoring CI partner ranks candidates by first-week stars as shown on the
  repository page and will present that ranking at the editorial meeting.

## 8. Determinism by construction

* **Membership timing.** No contested star falls within a day of a membership start or end, so inclusive and exclusive interval rules
  agree.
* **Subgroup assignment.** Launch source comes from the referral report, and every candidate's first-week share from social referrers is
  either above 60% or below 15%, so the subgroup line cannot move a candidate.
* **Day 0.** Every shortlisted repository was created public, so day 0 is unambiguous.
* **Smearing.** Duan's factor is computed on each subgroup's 2023 residuals, as the memo's method states, and the pilot reproduces both
  factors.
* **Ties.** No two candidates are within 1.15× of each other at the top of any rung.

## 9. Prompt sketch and deliverables

> The February spotlight goes to one of the eight repositories on the shortlist, and I announce it on Monday. Our editor is convinced the
> company-backed launches will do best. Tell me which repository gets it and how many external stars you expect it to reach in its first
> 90 days, and send `spotlight_case.xlsx`, a chart `first_week_external.png`, and a short `spotlight_decision.pdf`.

* `spotlight_case.xlsx` — the eight candidates under each construction, the fork sheet (ask A) and the issue sheet (ask B).
* `first_week_external.png` — the eight candidates' first-week stars as stacked bars (external on the day, members then but not now,
  members now), the expected 90-day stars as dots on a second axis, and the spotlight choice marked.
* `spotlight_decision.pdf` — the committed repository, its expected stars, and why each other candidate falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each candidate, first-month forks and the share from accounts under 30 days old. *Device:* a
  fork deleted and recreated posts two fork events and one delete event, and the platform's fork count is net of deletions, as the event
  documentation says. Counting fork events overstates three candidates' forks.
* **Ask B (device-carried).** For each candidate, open issues at day 30 and the median hours to a maintainer's first response. *Device:*
  an issue transferred between repositories closes at the origin and reopens at the destination with a transfer link. Counting the close
  as a resolution understates two candidates' open issues and shortens their response times.
* **Ask C (validity).** Each candidate's expected 90-day stars under each of the four rung constructions, and each construction's fit to
  the pilot log's 96 realised outcomes.
* **Decoupling.** Replacing star-date membership with today's flag changes no figure in asks A or B.

## 11. Rubric arithmetic

8 candidates × 2 (ask A) + 8 candidates × 2 (ask B) + 8 candidates × 4 constructions (ask C) + the committed repository, its expected
stars, the runner-up and the margin + 5 named chart parts + 3 files ≈ 76 criteria.

## 12. World-building constraints

* Expected 90-day external stars (thousands) by rung: A 6.9/3.2/3.2/3.2; B 5.0/5.0/5.0/2.9; C 5.8/5.8/3.4/3.4; D 4.1 throughout; E 4.4/4.4/3.0/3.0;
  F 3.2; G 2.9; H 2.2.
* B's first week: 290 flag-external stars, 140 of them from contractors whose memberships ended three weeks after launch.
* The flag and the register agree for 96% of stargazers overall. P-0611 and P-0907 are identical on every shortlist column.
* Recreated forks and transferred issues never touch stars, flags or the register.
