# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 2, drawn 2026-10-21 after architecture 1 was
spent at stage 4; nothing of its world or decisive step is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v2, lineage v1 spent), registered 2026-10-21
  after a pull. Guard WARN only, answered here: `overuse.objective` (the lane), `repeat.decision` and
  `repeat.question_form` (a designation set asked as "which", as task479), `people.first`. Redrawn at the draw: Gate G
  statistical_rigor (supporting only) to etl_conformance, shape 10 then 15 (bans against task272 and task479) to other,
  pattern G17 (same puzzle as task471) to G14 with differentiation lines for task233, task458 and task473. People from
  `guard.py names --geo gb --seed 4822`: Sally Phillips and Sophie Williams.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: a national statistics office's business register extract in two layouts, its summer 2026 quality audit
  and the register's risk screen output conformed by region and record, and each region's register error rate
  estimated from the audit.
- **The decision and the quantity:** the office's quality board sends to a 2027 re-validation exercise the regional
  registers whose share of records in error exceeds 4 per cent. Current state by design: the exercise is chosen on the
  register as it stands at the audit, so nothing is forecast.
- **Data-native sentence:** the audit drew the records the register's automated risk screen flagged at sixty in a
  hundred and the rest at two in a hundred, and flagged records are in error far more often, so a region's audited
  share is mostly its flagged records' error rate, whatever share of its register they are.
- **Strategy:** `population_selection`; Gate G `etl_conformance`; gap `population`; generators G14, G5. Layer 2 family
  `estimand_identification`, pattern `own:an audited share read as the register's rate when the audit drew records by a
  screen at very different rates`.

## Default path

To be written at stage 2 from the generator's clean truth.

## Tried and rejected
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
