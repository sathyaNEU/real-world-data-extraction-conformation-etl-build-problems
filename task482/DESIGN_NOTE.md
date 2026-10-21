# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 4, drawn 2026-10-21 after architectures 1
to 3 were spent at stage 4; nothing of their worlds or decisive steps is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v4, lineage v1 to v3 spent), registered
  2026-10-21 after a pull. Guard WARN only, answered here: `people.first` (Evelyn, a common first name; surname
  unused), `overuse.objective` (the lane), `overuse.gate_g`, `repeat.decision` and `repeat.question_form` (a
  designation set asked as "which"), `repeat.deliverables` (one workbook). Redrawn at the draw: context artifact
  register then published_series (bans against task478 and task486) to filed_standard; gap population to objective
  (the same-driver signature was spent in five builds); differentiation lines for task481, task470, task251, task479,
  task464 and task484. People from `guard.py names --geo ireland --seed 4824` and `--seed 4825`: Clare McEntee and
  Evelyn Clune.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: the residential property price register in two layouts, the valuation register's dwelling attributes
  and the address point file's small areas conformed into one sales table, and each area's residential property
  price change built from it.
- **The decision and the quantity:** the Minister for Housing designates as rapid price growth areas for 2027 the
  local authority areas whose residential property price index, as the Brannagh Statistics Office measures it, rose by
  more than 8 per cent from the year to September 2025 to the year to September 2026. Forward facing: the designation
  governs 2027.
- **Data-native sentence:** the homes that sold in each area are a different slice of its stock in each year, more of
  them in the cheaper or the dearer electoral divisions, larger or smaller, new or second-hand, and the electoral
  division of a sale sits only in the address point file.
- **Strategy:** `population_selection`; Gate G `method_or_model_selection`; gap `objective` (the median sale price is
  correct and is not what the designation is scored on); generators G6, G17; pattern none. Layer 2 family
  `estimand_identification`, pattern `own:an area's price change read from summaries of what sold when the sold
  homes are a shifting sample of the stock by location, size and newness`. Compound by design: the client's held
  tasks keep a dimension in another file, and here every partial correction (per square metre, by dwelling type
  against the census stock, a regression without location) files its own wrong set.

## Tried and rejected
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- Architecture 3, registration offices put on a timeliness plan from a quarter's median working days with part of the quarter still open at the extract (2026-10-21, spent at stage 4): both readers censored the open applications at their age, took the Kaplan-Meier median and landed the call, and dated payments by the batch terminal day (asks 28 of 28). An open caseload shipped beside a duration cohort, with a paper saying the open ones count, is read as right-censored by a strong reader; a settlement batch file carrying the terminal day is a seen device.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
