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

A strong analyst with every field read correctly:

1. Reads the paper: a regional register goes to re-validation when the share of its 30 April 2026 records in error
   exceeds 4 per cent, the evidence the summer audit.
2. Joins the audit outcomes to the register through the old region codes, reads FAIL and the codes 1 to 4 as errors,
   and takes each region's error rate as the share of its audited records in error.
3. Compares with 4 per cent.

**Ends on:** AR01, AR02, AR04, AR05, AR06, AR07, AR08, AR10, AR11, AR12 and AR13 chosen

On that path the audited shares run 7.8 to 12.9 per cent in the eleven and 2.7 to 3.4 per cent in AR03, AR09 and
AR14.

**Golden:** AR01, AR05, AR08, AR11 and AR12 chosen; each audited record carried to its stratum (referred by the May
screen or not) on the 30 April register puts AR02, AR04, AR06, AR07, AR10 and AR13 at 2.1 to 3.3 per cent and the five
at 4.7 to 6.7 per cent.

## Stump sentence

The default path takes each region's share of its audited records in error and files AR01, AR02, AR04, AR05, AR06, AR07, AR08, AR10, AR11, AR12 and AR13 chosen, because it never asks how the audit drew its records: it took close to a quarter of the records the May risk screen referred and one in twenty-five of the rest, the referred records are in error far more often, and a region's register error rate is its strata's audited rates carried to the records each stratum holds.

## Three rules

Task type: census-register-administrative-data-quality (Survey Research & Official Statistics): the business register extract, the risk screen's referral list, the summer quality audit and the region code crosswalk conformed by record and region, and each regional register's error rate estimated from the audit, a conformation serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each regional register's share of records in error, worked the way official statistics estimates a register's accuracy from a quality audit drawn with unequal probabilities: the audit's strata (referred by the risk screen or not) each estimated from their audited records and carried to the records they hold on the register (stratified, inverse-probability estimation), the sampling fractions read from the counts audited against the counts on the register.

Swap: "which hospitals' share of misfiled charts exceeds 4 per cent, from a chart audit" keeps an audited share and would need the same weighting only if its audit were drawn by a screen; the step's ground is the register's quality audit drawn on its own automated referral list, which a chart audit with simple random draws does not have.

Layer 1: the register extract with UTC creation times against a register kept in local time, the audit system's pre-2025 region codes and their crosswalk, the audit's two outcome schemes either side of 1 July, records registered after the audit's frame, a company struck off and restored inside the quarter (the asks); each is how the producing system writes, nothing is placed to be caught, and checks.py asserts the call under them (SF4 to SF7, L1 whole_extract).

Layer 2: estimand_identification, the population an audit sample speaks for: the choice that flips the call is carrying each stratum's audited error rate to the register records it stands for, instead of reading the audited share as the register's.

Decisive step: estimating each region's register error rate as its referred and unreferred strata's audited error rates weighted by the records each stratum holds on the 30 April register (the referral list giving the stratum), which takes AR02, AR04, AR06, AR07, AR10 and AR13 under 4 per cent.

Not semantics: every field, code and definition read correctly (the two outcome schemes, the old region codes, the UTC times, the referral flag) still leaves the easy route reading the audited share, because no field says how the audit drew its records; the step is the inference that the audit over-represents the referred records, which the counts audited against the counts on the register show and no sentence says.

Not rule application: the paper fixes the population (the 30 April register), the outcome (a certified field wrong), the unit (the share of records) and the comparison (over 4 per cent), and names the audit as the evidence; no rule says how the audit's outcomes are carried to the register, and executing every filed rule on the audited share files the default eleven.

Analyst test: a strong analyst who conforms every file and reads every rule, taking each region's audited share as its error rate, files AR01, AR02, AR04, AR05, AR06, AR07, AR08, AR10, AR11, AR12 and AR13 chosen (the default path's Ends on); one who keeps only the unreferred records files AR01 and AR08; only carrying each stratum's audited rate to its records files the golden five; checks.py runs them on the clean truth (R3a, R3b).

Estimand: the quality board paper (sar_quality_board_paper_register_revalidation_2027.pdf, sections 2 and 3): the population (each region's records on the register on 30 April 2026, active and since dissolved), the outcome (a certified field wrong against source documents), the window (the register at the audit's draw), the unit (the share of records) and the comparison (exceeding 4 per cent), the evidence the summer 2026 quality audit.

No decoy: nothing is planted: the register, the referral list, the audit and the gazette are the producing systems' records, the paper states the basis without a method, and no earlier exercise, published accuracy figure or region ranking ships; the costs, survey and returns files rank nothing on accuracy.

No certified replay: no certified or published error rate, sampling design or weight ships; the method is not recovered by reproducing any figure.

Lesson: an audit's share speaks for the records it was drawn from in the proportion it drew them, and an audit drawn on a screen's referrals has to be carried back to the register stratum by stratum; no build on file estimates a register's rate from an audit drawn unequally by its own screen.

## Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| R0 the unreferred records only | the referral list read as records to set aside | readable |
| Layer 1: old codes, outcome schemes, UTC times | the dictionary and the crosswalk | readable |
| R1 (default path) the audited share | the paper and the audit file | readable |
| R2 (decisive) each stratum's audited rate carried to its records | nothing: no sentence describes how the audit drew its sample, names a sampling fraction or a weight; the referral list is listed in the manifest as the screen's run | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the population | the 30 April register, active and since dissolved | the 30 September extract | same call (asserted, whole_extract) | paper section 2 |
| SF2 | records registered after 30 April | out | in | same call (asserted) | paper section 2 |
| SF3 | exceeds | strictly over | at or over | same call (no region within half a point, C2) | paper section 2 |
| SF4 | the outcome codes | FAIL and 1 to 4 are errors | 0 to 4 counted | not filed alternatives | the dictionary; paper section 3 |
| SF5 | region codes | old to new by the crosswalk | another mapping | same call (asserted) | the crosswalk |
| SF6 | an audited record's region | the register's | the audit's old code | same call (they agree, asserted) | SF6 |
| SF7 | repeated audits | one outcome per record | several | same call (asserted) | SF7 |
| SF8 | the evidence | the audit alone | other checks | not filed alternatives | paper section 3 |

## Ladder

Built values from the cut pack (generator/checks.py L1 to L3, C2, C3), register error rate, per cent.

| Rung | Route | Chosen | AR02, AR06, AR13 / AR12 |
|---|---|---|---|
| R0 | the unreferred records only | AR01, AR08 | 0.0, 1.3, 0.7 / 3.8 |
| R1 (default path) | the audited share | eleven regions | 9.8, 9.8, 9.6 / 7.8 |
| Golden | each stratum carried to its records | AR01, AR05, AR08, AR11, AR12 | 2.6, 3.3, 2.9 / 4.7 |

- Dominance: under the golden, its design-weight and ratio forms and the whole extract, every region sits half a point
  or more from 4 per cent (C2), and every estimate lies within two points of the register's true rate (C3).
- The data separates the readings: the audit holds about 24 per cent of the referred records and 4 per cent of the rest in
  every region, and the referred records' audited error rate runs several times the rest's.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | each region's 30 April records | filed (SF1) |
| 2 | Unit of account | the share of records | filed |
| 3 | Attribution window | the register at the draw | filed |
| 4 | As-of dating | the extracts of September and October 2026 | manifest |
| 5 | Version basis | one outcome per audited record | SF7 |
| 6 | Denominator | the region's 30 April records | filed (SF1) |
| 7 | Weighting | each stratum by its records | L1 forms |
| 8 | Window length | one audit season | filed |
| 9 | Boundary inclusivity | strictly over 4 per cent | SF3 |
| 10 | Rounding path | unrounded against the line | prompt |
| 11 | Tie-break | none | C2 |
| 12 | Maturity and censoring | the audit complete by August | manifest |
| 13 | Order of operations | conform, stratify, carry, compare | commutes |
| 14 | Row order | none | commutes |
| 15 | Duplicate resolution | none on the call's files | SF7 |
| 16 | Identity normalisation | old region codes | SF5 |
| 17 | Netting against gross | none | commutes |
| 18 | Dimensional units | UTC against local time | the dictionary |
| 19 | Code and status semantics | outcome codes | SF4; never the stump |
| 20 | Integerisation | none | commutes |
| 21 | Clause scope | every region | filed |
| 22 | Forward window contents | none (the register at the draw) | filed |

## Literal reader

The paper executed word for word asks for each region's share of its 30 April records in error, with the audit as the
evidence; the literal question is what the audit says about the register's records, which the audited records answer
only stratum by stratum in proportion to the records each stratum holds. A literal reader who takes the audited share
has assumed the audit drew every record alike, which the counts audited against the counts on the register contradict;
every other reading converges or violates a quoted sentence (fork table). Re-run on the finished pack.

## Oracles

- No shipped file carries a register error rate, a sampling design, a weight or a ranking of the regions.
- The cost estimates, the user survey and the returns compliance are distractors (metadata.json).
- No control ties only under the golden on the asks.

## Ask sheet

- **Ask A, each region's new registrations in the third quarter of 2026 (fourteen figures).** H18 home: the register's
  intake beside its accuracy (paper section 4). Path: the register extract's creation times. Primary device: D8, a
  clock against a filed cutoff: the extract writes creation times in UTC while the register's quarter keeps Ardmuir
  local time, an hour ahead in summer, so registrations filed online in the first hour of 1 July read as 30 June.
- **Ask B, each region's companies struck off and dissolved in the quarter and still dissolved at its end (fourteen
  figures).** H18 home: as ask A. Path: the gazette's notices, the register for the region. Primary device: D2, the
  record is the latest accepted: some companies struck off in July or August were restored to the register before the
  quarter ended, so counting struck-off notices overstates. Hazards: first notices of a proposal to strike off.
- **The construction layer:** the call, the fourteen decisions and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads the register's region and creation date, the referral
  list and the audit; the asks read creation times across the quarter's edge and the gazette (X1).
- **Hazard table (asserted):** A1, A2, B1, B2 in checks.py; none moves the call.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, third-quarter registrations | the creation time as written; keeps 0 of 14 | miss |
| B, dissolutions still standing | every struck-off company; keeps 0 of 14 | miss |

- Mirror leakage: 0.0 per cent of ask weight on the cut pack (0 of 28).
- Pair ceiling: 34.0 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call and instructions, 45.0; the
  mirror at the default path misses the set and keeps 8 of 14 decisions, 23.0). Re-measured by the stage 4 readers.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

READERS_LINE

JUDGE_LINE

## Tried and rejected
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
