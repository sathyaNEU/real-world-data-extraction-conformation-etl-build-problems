# Determinism check, task470 (Domains Fit and metadata repair, 2026-11-07)

Judge thread: one isolated read on Sonnet at medium effort, from `/tmp/determinism-check-task470-dfit/judge_brief.md`
on target.zip bc4fe60e (the bundle unzipped at `/tmp/determinism-check-task470-dfit/target/`, 14 files). The thread saw
only the bundle and the submission's graded blocks; its verdict is `/tmp/determinism-check-task470-dfit/verdict.md`.

## Verdict

**DETERMINISTIC, SOLUTION_WRONG (minor).** The main call is forced: the counted dwellings (8,020), the vacant (396),
the ten shares and the qualifying five (Tverrvika 5802, Hesteby 5803, Solmoen 5805, Ørnevik 5807, Fjordeid 5809)
reproduce at every threshold of a household's day from 0.2 to 1.0 kWh and every window variant the thread tried,
because the per-dwelling largest rise is bimodal with nothing between 0.3 and 0.8 kWh. The ten Clopper-Pearson 90 per
cent intervals, table A (13,599 persons, all 30 cells) and table B (all ten) reproduce exactly. One critical component
did not: 557 lived-in dwellings with nobody registered, which the thread made 556.

## Disposition

**FIX_NOW**, in the solution only; no input file moves.

## Gate G

`mechanism: etl_conformance` (method selection of the occupancy signal), `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`. The register's occupancy is set aside by Section 4, so no
reported number is overturned; the difficulty survives on clean data.

## Gate H

`domain: pass`, `layers: pass`, `decisive_step: analytical`. Register-plus-smart-meter occupancy estimation of the kind
a statistics office does; Layer 1 is the municipality split, meter changes, replaced deliveries, the clock, the block
renumberings and the title names; Layer 2 is the choice of occupancy indicator. The parts close to data semantics sit in
the two ministry tables only.

## Competing readings the thread tested

- The register's empty dwellings: all ten qualify; ruled out by Section 4.
- A consumption floor: none qualify from 1 to 14 kWh a day, four at 15; empty dwellings are heated, so a floor is not a
  defensible reading of nobody living there.
- A waking-hours mean over the night mean: three, six or ten by threshold, no gap; not a defensible indicator.
- Vacant on fewer than half of days: eight qualify; contradicts Section 4's "on any day".
- Qualification by the whole interval above the line: Tverrvika, Hesteby and Ørnevik only; closed by Section 6, rated a
  mild fork in the prompt's wording.
- The population register: the renumberings read as moves give 13,494 persons, no roll-back 13,520, a filter on
  bosatt_fra 12,847; the block renumbering is a clean one-floor shift inferable from the data, so 13,599 is forced.

## Stump power

Two natural easy routes give wrong answers on correct, cleaned data (the register: all ten; a consumption floor: none).
The golden needs an occupancy indicator built from each dwelling's daily shape against its own night-time baseline.
Risk of being too easy is low; the clean gap keeps the method from being a coin-flip.

## Hygiene

PASS: 14 files, CSV, parquet (2.72 million hourly rows), PDF, EML and XLSX; distractors present and unused; nothing
exclusion-level. Minor: the shareholder register is dated 2025 against ownership wanted on 1 November 2026, the only one
shipped.

## Fixes made after the read

1. **Critical component 3, 557 to 556.** In Haugveien 6 (5805), renumbered on 24 November, person 7123550 emigrated on
   14 November from old unit H0302. Nobody still held H0302 on the renumbering day, so the golden's relabelling, built
   only from the residents renumbered that day, had no entry for it and left the person in the new H0302, a different
   flat. The world renumbers every flat of a picked block one floor up (generator/sim.py), so the person's dwelling on
   1 November is the new H0402. The roll-back now applies a renumbered block's rule to every old number written before
   its day (methods.block_relabels and relabelled; verify.py the same rule in its own code). The persons-registered
   column moves for two dwellings (Haugveien 6 H0302 from 3 to 2, H0402 from 0 to 1), lived in with nobody registered is
   556, vacant with a registered resident stays 118, and the municipal totals and table A do not move. Step 6 says the
   golden's rule. checks.py asserts every counted dwelling's persons against the world's (0 differ) and component 3
   against the world's counts; verify.py recomputes both counts independently.
2. **The interval fork in the prompt.** The question now reads "judged on the estimated share of each municipality's
   housing standing vacant, from the register and meter data, with that share's 90 per cent interval beside it", so the
   designation rests on the share and the interval is reported (fork table SF25, asserted: the whole-interval rule gives
   5802, 5803 and 5807). 997 characters, voice-check PASS.

freeze.py (rubric mode against the shipped snapshot) moves only the corrected component 3 and the reworded call
sentence; no other main-call figure, the stump and the ladder do not move. The pack (target.zip bc4fe60e) is unchanged
by both fixes.

## Round 1 of this repair

The determinism judge on architecture 2's original ship (target.zip 52fc465d, 2026-10-31) returned DETERMINISTIC,
APPROVE, with SF19 closing its one low note (the deed's date against the registration date).
