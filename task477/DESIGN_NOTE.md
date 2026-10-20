# task477 design note: the Tallis Valley workforce board's 2027 sector-partnership slate

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task477.json` (architecture v1), registered 2026-10-20 with WARNs only
  (ETL in 6 of 12 is the lane; shape 01 in 4 of 12; Gate G method_or_model_selection after task471 and task476, the
  decisive step being how each industry's pay-date exposure is estimated among defensible methods; "which" after
  task471 and task476, the slate being a pick of four). The first draft's decisive generator G13 repeated task476's
  driver signature and was redrawn to G3 (the record counts pay when it is paid, the decision runs on the work it
  pays for), the honest label; csv+xlsx repeated task472's set and became csv+docx. Nearest driver task102 at 0.07.
- **Seed:** ET34 (a county's private-sector average weekly wage jump read from QCEW). Kept: the world (a county
  labor market's covered-wage record), the decision (which industries' pay per job really grew) and the quantity
  (pay per job by industry). Dropped: the seed's hierarchy, ownership and suppression mechanism, which is Layer 1
  mess here.
- **Pairing:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production / Data
  Extraction & Conformation (ETL). The board conforms the state's quarterly covered-wage files (wages counted in the
  quarter they are paid, several releases, two layouts) into an earned-basis wage series by industry, the pay for the
  work done in each calendar year, and ranks industries on it.
- **Shape:** 01, a ranked list under a cap: each industry's 2021 and 2025 earned pay per job and growth, the four
  funded, the runner-up and its gap, the files.
- **Strategy:** composition_mix. Each industry's payroll is a mix of pay schedules (weekly, every other Friday on
  one of two alternating weeks, twice a month, monthly), recorded nowhere; 2021 holds 53 Fridays and, for one
  alternating-Friday phase, 27 pay dates, so each industry's 2021 wages are inflated by its own unseen mix. Decisive
  generator G3, with G6 (the schedule mix) and G17 (the exposure estimated from quarterly pay-date counts).
- **World:** United States, a fictional multi-county labor market region in an unnamed state. The Tallis Valley
  Workforce Development Board files its 2027 to 2029 sector-partnership slate (four industries) with the state's
  sector-partnership fund; the slate is the four industries with the fastest growth in pay per job from 2021, the
  program's base year, to 2025. Personas from `guard.py names --geo "United States" --seed 477`: Beverly Ray (labor
  market analyst), Dalton Harding (executive director).

## Tried and rejected
