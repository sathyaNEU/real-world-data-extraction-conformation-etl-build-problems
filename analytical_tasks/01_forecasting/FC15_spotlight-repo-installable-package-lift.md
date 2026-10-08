# FC15 — Which new repository gets February's spotlight, when the spotlight's extra stars go only to projects readers can install in one step

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · developer platforms and content promotion |
| Mirrors | Promoting new items where the promotion's lift lands only on items the audience can act on at once (GitHub Explore and npm trending for tools with an installable package, App Store featuring for apps with a free tier, YouTube and Instagram promotion of creators with something to follow) |
| Decision shape | Which of N gets one scarce thing: the newsletter's single February spotlight, with its sponsored CI year, among eight shortlisted repositories |
| Committed call | The spotlighted repository, with its expected 90-day external stars, spotlight included, in thousands to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern E (conditioned yield): the pilot's spotlight lift is an absolute 4,500 stars on repositories with an installable package and nil elsewhere, a property reached through the package registry, with a subgroup-validated decay below it |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #13 validates on one population, applies to another · #6 treats a mixed segment all one way · #15 follows the requester's hunch over the rule |
| Calibration form | Pilot log: twelve months of spotlight decisions, each month's full shortlist with the model's predictions and every candidate's realised 90-day external stars |
| Driving force | The pilot log's average spotlight lift is real and applies to no candidate. A spotlighted repository with a package on its language's registry gained 4,500 external stars over its forecast in 90 days, and one without gained 200, because readers star what they can try in one command. The pilot spotlighted large launches, so as a ratio the lift looks larger on the small packageless repositories, which points the wrong way. Packaging is no shortlist column; it comes from the registry's package records, each naming its source repository. |

## 1. Situation

A developer platform spotlights one new repository a month in its newsletter, with a year of sponsored CI. The featuring memo sends the
spotlight to the shortlisted repository with the most expected external stars in its first 90 days public, the spotlight's own effect
included, measured on the pilot log. It counts an account's first star only, and files the forecasting model: log 90-day external stars
on log first-week external stars, fitted on the 2023 cohort, with a smearing factor. The editors shortlisted eight repositories that went
public in early January.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: star events, the shortlist, the pilot log, the referral report and the package registry. No one's
  claim about their own numbers is overturned. The difficulty is which candidates the measured spotlight effect applies to.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the CI partner's ranking. The filed model on de-duplicated stars, calibrated by launch type
  and lifted by the pilot's average, still names B.
* **Instrument repair.** Suspect: the star-event file, a delta log in which A's launch giveaway left 1,100 star-unstar-restar cycles.
  Reduce it to each account's first star: rung 0 then names C (8.4 against 7.2), as rung 1 does, and rung 2 still names B. No file
  claims packaging: the shortlist has no such column, and the registry records every package with its source repository. The conditioned
  lift is still needed for D.
* **Lens swap.** The naive read and the answer differ in population: the pilot's spotlights averaged together, against the candidates
  that can take the spotlight's effect.

## 3. The driving force

A strong solver removes repeat stars, sees that social-burst launches decay faster than the model's 2023 cohort, calibrates them apart,
and adds the spotlight's effect from the pilot log: spotlighted repositories realised 1.36× their forecast. That multiplies every
candidate alike and names B, a steady company launch with the largest calibrated forecast. The pilot's twelve spotlights split cleanly.
The eight with a package published on their language's registry gained 4,200 to 4,800 stars over forecast, whatever their size. The four
without gained 100 to 300. A reader who can install a tool in one command tries it and stars it; a reader who has to build it rarely
does. The pilot spotlighted large launches with packages, so their ratio was only 1.20, while the small packageless ones reached 1.67, and
the ratio points the wrong way. Among this month's candidates D, a community data-pipeline tool, and E have packages. Packaging appears on
no shortlist column. It comes from joining each candidate's repository to the registry, whose package records name their source
repository.

## 4. The ladder

| Rung | Construction | Names (expected 90-day external stars with the spotlight, thousands) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The filed model on every first-week star event, × the pilot's average spotlight ratio (1.36) | A (12.8 against 8.4) | The memo's model and the pilot's measured effect | The memo's star definition: an account's first star only; A's launch giveaway produced 1,100 star-unstar-restar cycles |
| 1 | Hygiene: repeat stars removed | C (8.4 against 7.2) | Clean counts, the filed model and the measured effect | **E17 (validated on one population, applied to another):** the pilot log and the referral report show social-burst launches realising half the model's prediction; the 2023 cohort was 90% steady launches |
| 2 | Social-burst launches calibrated apart (their own smearing factor from the pilot log) | B (6.8 against 5.2) | The forecast now fits every launch type the pilot shows, and the effect is the pilot's own | The registry joined to the pilot's spotlights: +4,500 stars on the eight with a package, +200 on the four without |
| 3 | **Decisive:** the calibrated forecast plus the spotlight's lift conditioned on an installable package, found by joining each repository to the registry's package records | **D (8.3 against 7.2)** | — | — |

* **Position table.** D is 5th on rung 0 (5.2), 4th on rung 1 (5.2), 2nd on rung 2 (1.32× behind B), and leads only rung 3. Rung margins
  are 1.52×, 1.17×, 1.32× and 1.16×.
* **Discriminator dominance.** B carries a 1.32× lead into rung 3 (6.8 against 5.2). D's edge on the decisive axis is 2.10× (D rises
  1.61× to 8.3 while B falls to 0.77× of itself, 5.2), against the required 1.2 × 1.32 = 1.58, a headroom of 1.33.
* **Partial correction priced (L3).** Adding the pilot's average lift as stars (+3,070) to every candidate names B (8.1 against D's 6.9,
  1.17×). Conditioning on packaging but keeping the lift as a ratio (1.20 with a package, 1.67 without) names B by more (8.4 against 5.3,
  1.56×). Conditioning correctly without the launch-type calibration names E (9.8 against 8.3, 1.18×); without removing repeat stars, A
  (9.6 against 8.3, 1.16×).
* **Grid.** Repeat stars (kept, removed) × baseline (pooled, calibrated by launch type) × spotlight effect (average ratio, average stars,
  ratio by packaging, stars by packaging) gives 16 cells. A, B, C or E leads every cell but the answer's.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo says the effect is to be measured on the pilot log. No document says the effect depends on packaging or
   comes in stars rather than proportion, and the registry ships in the editors' standard data pack.
2. **Corpus blind for a computable reason.** *In the pilot, packaging was uncorrelated with every shortlist column (language, owner type,
   launch source, first-week size band), because the editors shortlist on launches and the registry is a separate service.* Every split of
   the pilot on shortlist columns returns the average effect; only the registry join separates 4,500 from 200.
3. **No arithmetic symptom.** Star counts tie to events, predictions to the filed model, and every pilot month's realised stars to the
   events, under every rung.
4. **Not a row predicate.** No star or candidate is filtered. The effect is a quantity measured per spotlight, split by a property of the
   repository held in another service, then added to each candidate's own calibrated forecast.
5. **The enumeration is arithmetic.** Which candidates have a package is found by matching registry records to repositories. No column
   says so.
6. **No cutover date.** Packages were published at different dates across the pilot year, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The pilot log: twelve monthly shortlists (96 repositories), each with first-week stars, the model's prediction, the spotlight
  decision and every candidate's realised 90-day external stars.
* **What it certifies.** The filed model on steady launches that were not spotlighted (within 5% in 58 of 60), the social-burst subgroup's
  half realisation, and the spotlight effect by packaging: 4,200 to 4,800 stars on predictions from 4,000 to 40,000 with a package, 100 to
  300 without.
* **The absolute split (O2).** As stars the effect is flat within each group; as a ratio it runs from 1.11 to 2.05 with a package and is
  highest on the smallest packageless repositories, so the cross-section by ratio points the wrong way.
* **Twin pair.** Spotlights P-0611 and P-0907 are identical on every shortlist column: 812 first-week external stars, language, launch
  source and owner type, both predicted at 4,300. They realised 8,800 and 4,500 (2.0×), because P-0611 had a package on its registry. The
  average ratio gives both 5,800; only the conditioned lift reproduces both.
* **Resemblance points at the decoy.** B resembles the pilot's best-realising spotlights on every shortlist column: a steady, organic
  first week from a well-known owner.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The featuring memo: the spotlight goes to the shortlisted repository with the most expected external stars in its first
  90 days public, the spotlight's effect included and measured on the pilot log; a star counts only if it is an account's first on the
  repository; the model is log–log OLS on the 2023 cohort with Duan smearing.
* **Empirical pins.** The social-burst subgroup's smearing and the spotlight effect by packaging, from the pilot log. Each candidate's
  packaging, from the registry.
* **Voices.** The newsletter editor: "Big launches with company backing always do best in the spotlight." The developer-relations lead:
  "The spotlight adds about a third to anyone; pick the biggest and you get the most."
* **Licensed wrong basis.** The memo records that the sponsoring CI partner ranks candidates by first-week stars as shown on the repository
  page and will present that ranking at the editorial meeting.

## 8. Determinism by construction

* **Packaging date.** D and E published their packages weeks before the decision, and no other candidate has a registry record, so the
  property does not depend on the cut-off chosen.
* **Effect form.** Within each group the pilot's effect is flat in stars across a tenfold range of predictions, so the absolute form is
  pinned, and no group straddles the 4,500 and 200 levels.
* **Subgroup assignment.** Launch source comes from the referral report, and every candidate's first-week share from social referrers is
  either above 60% or below 15%.
* **Smearing.** Duan's factor is computed on each subgroup's 2023 residuals, as the memo's method states, and the pilot reproduces both.
* **Ties.** No two candidates are within 1.15× of each other at the top of any rung.

## 9. Prompt sketch and deliverables

> The February spotlight goes to one of the eight repositories on the shortlist, and I announce it on Monday. Our editor is convinced the
> company-backed launches will do best. Tell me which repository gets it and how many external stars you expect it to reach in its first
> 90 days, and send `spotlight_case.xlsx`, a chart `spotlight_effect.png`, and a short `spotlight_decision.pdf`.

* `spotlight_case.xlsx` — the eight candidates under each construction, the fork sheet (ask A) and the issue sheet (ask B).
* `spotlight_effect.png` — the pilot's twelve spotlights as points (forecast against realised, packaged and packageless marked), the two
  flat effect levels as lines, the eight candidates' calibrated forecasts as bars with their expected effect stacked, and the choice
  marked.
* `spotlight_decision.pdf` — the committed repository, its expected stars, and why each other candidate falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each candidate, first-month forks and the share from accounts under 30 days old. *Device:* a
  fork deleted and recreated posts two fork events and one delete event, and the platform's fork count is net of deletions, as the event
  documentation says. Counting fork events overstates three candidates' forks.
* **Ask B (device-carried).** For each candidate, open issues at day 30 and the median hours to a maintainer's first response. *Device:*
  an issue transferred between repositories closes at the origin and reopens at the destination with a transfer link. Counting the close
  as a resolution understates two candidates' open issues and shortens their response times.
* **Ask C (validity).** Each candidate's expected stars under each of the four rung constructions, and each construction's fit to the
  pilot's twelve spotlights.
* **Decoupling.** Replacing the conditioned effect with the average ratio changes no figure in asks A or B.

## 11. Rubric arithmetic

8 candidates × 2 (ask A) + 8 candidates × 2 (ask B) + 8 candidates × 4 constructions (ask C) + the committed repository, its expected
stars, the runner-up and the margin + 5 named chart parts + 3 files ≈ 76 criteria.

## 12. World-building constraints

* Calibrated forecasts without the spotlight (thousands): A 3.2 (9.4 with repeat stars), B 5.0, C 3.1 (6.2 before launch-type
  calibration), D 3.8, E 2.65 (5.3 before calibration), F 3.0, G 2.8, H 2.2. Packages: D and E only.
* Expected stars with the spotlight by rung: A 12.8/4.3/4.3/3.4, B 6.8/6.8/6.8/5.2, C 8.4/8.4/4.2/3.3, D 5.2/5.2/5.2/8.3, E
  7.2/7.2/3.6/7.2.
* Pilot effect: +4,500 (4,200–4,800) on eight packaged spotlights averaging 22,000 predicted; +200 (100–300) on four packageless ones
  averaging 300 predicted; average ratio 1.36, average stars +3,070.
* P-0611 and P-0907 are identical on every shortlist column. Recreated forks and transferred issues never touch stars or the registry.
