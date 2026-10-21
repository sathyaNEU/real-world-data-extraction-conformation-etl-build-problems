# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 1, drawn 2026-10-21.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v1), registered 2026-10-21 after a pull.
  Guard WARN only, answered here: `overuse.org_family` (a state board is a government agency), `overuse.objective`
  (the lane), `repeat.question_form` (a capped slate is asked as "which"). Redrawn at the draw: calibration form,
  context artifact and strategy (bans against task479 and task272), then gap population with G2 (same driver as
  task486) to G5, Gate G `etl_conformance`, strategy `composition_mix`, artifact `published_series`. People from
  `guard.py names --geo us --seed 482`: Jeremy Cortez and John Huang.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: the federal finance and 12-month enrollment returns of a state's public four-year campuses conformed with
  the state's credit hour file, the consolidated returns of four parent campuses apportioned to the campuses inside
  them.
- **The decision and the quantity:** the coordinating board's 2027-28 instructional investment grant goes to the five
  reporting units with the lowest fiscal 2026 instruction expense per FTE student. Retrospective by statute: the grant
  formula reads the latest closed fiscal year, so the window is fiscal 2026 (July 2025 to June 2026), and nothing is
  forecast.
- **Data-native sentence:** six branch campuses report enrollment and credit hours of their own but have their
  finances inside their parents' returns, and they teach mostly freshman and sophomore credit hours, which the sixteen
  campuses that report alone show cost about a third of a graduate hour.
- **Strategy:** `composition_mix`; Gate G `etl_conformance`; gap `population`; generators G5, G2. Layer 2 family
  `estimation_fit`, pattern `own:a combined return split among the units inside it by a cost model fitted on the units
  that report alone, not by their head counts`.

## Default path

To be written at stage 2 from the generator's clean truth.

## Tried and rejected

