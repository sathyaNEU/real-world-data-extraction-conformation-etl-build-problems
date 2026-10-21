# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 3, drawn 2026-10-21 after architectures 1
and 2 were spent at stage 4; nothing of their worlds or decisive steps is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v3, lineage v1 and v2 spent), registered
  2026-10-21 after a pull. Guard WARN only, answered here: `overuse.objective` (the lane), `repeat.decision` and
  `repeat.question_form` (a designation set asked as "which"), `people.first`. Redrawn at the draw: role family and
  organisation family (bans against task480), differentiation lines for task231, task234, task445 and task469. People
  from `guard.py names --geo ie --seed 4823`: Eunan Reid and Jennifer Dyer.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: a business registry's registration log in two systems' layouts, its open caseload snapshot and its
  holiday calendar conformed by office and application, and each office's third-quarter timeliness measured.
- **The decision and the quantity:** the registry's management board places on a timeliness improvement plan the
  regional offices whose median working days from a complete application to registration, for applications received
  from 1 July to 30 September 2026, exceed 20. Forward facing in its data: at the 9 October extract the quarter's
  applications are still being registered.
- **Data-native sentence:** at the extract a share of each office's third-quarter applications is still open, listed
  only as counts by office and receipt day in the open caseload snapshot, and the open ones are the slow ones.
- **Strategy:** `maturity_censoring`; Gate G `etl_conformance`; gap `time`; generators G12, G9. Layer 2 family
  `estimand_identification`, pattern `own:a cohort's median duration read from its finished members alone when the
  unfinished are the slow ones`.

## Default path

To be written at stage 2 from the generator's clean truth.

## Tried and rejected
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
