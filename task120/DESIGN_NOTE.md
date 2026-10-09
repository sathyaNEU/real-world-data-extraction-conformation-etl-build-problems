# task120: the TY2025 household-income tier floors a state revenue estimating conference adopts (realises analytical_tasks note DA01)

Source note: `analytical_tasks/03_descriptive_distribution/DA01_revenue-tiers-household-unit-dependent-returns.md`. This build is its first realisation. The note keeps the decision, the mechanism and the world; every change the guard forced is under Changes.

## DRAW

```
DRAW  (independent draws, checked with .claude/skills/fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? yes, registered 2026-10-09 after checkpoint A (go)   Verdict: PASS (no WARN)
  Shape: 14 cuts of a distribution   Gate G mechanism: method_or_model_selection
  Gap: population (decisive), objective   Pattern: none of A to E carries the decisive rung (the note's S1, a G2 unit construction), gated by B
  Domain: Economics   Subdomain (enumerated): public-finance   Objective: Descriptive & Distribution Analysis
  Pairing repeated from last build? no (task116 is Product Analytics x Opportunity Sizing; Economics x Descriptive was last drawn as task93)
  Stakeholder role: director of the state's nonpartisan revenue research office, which staffs the Revenue Estimating Conference (statistical_office_head)
  Context-artifact type: published_series (the Department of Revenue's Returns Processed by AGI Class, all filers, correct about returns)
  Calibration form: certified_matrix (the conference's Household Income Tables for TY2022 to TY2024, 69 cells, under the methodology's reproduction clause)
  Decision type: dial_setting (three AGI floors for the top 10, 5 and 1 per cent of household units, each to the nearest $1,000)
  Decisive mechanism: household units built by attaching each dependent's own return to its claimant through the claimant's
                      dependents schedule (G2), over federal filing units recombined on the federal primary TIN (G10), the
                      construction selected by the published tables (G16, Pattern B as the gate)
  Repeats from prior builds: none on a banned axis after the redraws under Guard; the reproduction gate is a device reused from
                      task109, differentiated on the driver
  Generators: G2, G10, G16   Answer unit: currency (USD)
  Forum: minister_or_cabinet (the state finance secretary adopts the re-based floors on the office recommendation; the conference certifies its estimate on them and does not vote on the floors)
  Forcing event: statutory_or_regulatory_filing (the conference certifies the income-tax estimate under statute, and the estimate runs on the re-based tiers)
  Organisation family: research_or_statistics_office
  Spine: TY2025 processed-return file, 3,412,000 rows planned, one processed state individual income tax return per row, return grain,
         synthetic (return microdata is confidential; shape calibrated to public IRS SOI state AGI-class aggregates)
  World: United States, a fictional state with invented counties (Kessler, Abington); USD
  People (guard.py names --geo "United States" --seed 120):
         Stephanie Reid, the requester, director of the revenue research office
         Manuel Stevenson, the office's chief economist (the belief that every return is a taxpayer)
         Brittany Shepard, the Department of Revenue's statistics chief (her all-filer table ties to the file)
         Jeffrey King, the legislative fiscal office (the licensed federal-filing-unit basis)
  Deliverables: tier_schedule.xlsx, tier_floors.png   Opening move: evidence-first
  Prompt shape arithmetic: three floors under each of four constructions with each one's published-cell hit count (16), the
         household-unit and twin-county counts (3), 24 wage-month and 12 instalment cells on the device-carried asks (36), four
         named chart parts and two files (6): 61 distinct criteria (the note's s.11 counts 64, its committed floors counted twice)
  As-of date: 2026-11-09
```

**Similarity claim.** No prior build is a tier schedule drawn on a unit that exists only through a link recorded on the claiming record: task109 shares the reproduction-gated percentile architecture but is stumped by two compilation conventions that each reproduce fewer controls alone than neither, while here the published cells respond monotonically (3, then 58, then 69 of 69) and the stump is a dependent's own return that joins its household only through the claimant's schedule.

## Stump sentence

A competent solver filters to full-year residents, recombines separately filed state returns into federal filing units through the federal primary TIN (the textbook tax unit), sees that construction reproduce 58 of the 69 published cells with every miss a few per cent short in one class, and files the schedule $197,000 / $293,000 / $594,000 against $214,000 / $318,000 / $742,000, because the dependents' own returns join their claimants only through the claimant's dependents schedule, a link no column on the dependent's return invites.

## Decisive rung

Measured trap #2, counts file rows instead of the real unit: decided 11 of the client's 64 tasks, 7 of them under 0.50 (established). The decisive step takes the form of #18, joins only on the visible key (2 of 64, 1 under 0.50, emerging): the federal primary TIN is the visible key, and the dependents' link is a two-hop chain through the claimant's schedule. Behind it, #3 stops at a close but inexact match (8 of 64, 5 under 0.50) and #1 reports a failed back-test, ships anyway (11 of 64, 9 under 0.50) hold a solver at the federal-filing-unit rung; #14 coarsens the segment (3 of 64, 1 under 0.50) sits under rung 1 as the Department's all-filer table.

Proven-in-production checks (stumping Part 6.1). Dead shapes (Part 4): no match; the nearest is a corpus built to refute the naive read, because the tables refute the return grain (3 of 69) and the federal-filing-unit grain (58 of 69, misses one-sided), which is the bet the measured catalogue's #1 and #3 take. Discriminators: the two units disagree in shape at the top and not only in level (the children's trust income carries 3,900 households past the top-1% mark at the draw's scale, 976 at the build's); membership is computed through a join and never a column; the construction has no menu. L5 (the answer is the extreme cell of the grid) and L8 (every construction is a complete partition, so every total ties) are met. L1 is not (the corpus pins the decisive rung instead of being blind to it), and L3 only in part (the literature's partial, dropping dependent filers, lands at $657,000, -11.5 per cent, nearer than rung 2).

## Nearest exemplars

- **0.13**, Supply Chain & Logistics, Replenishment Cover Standards: *Adopt the arrival-based 2026 cover schedule with GMR at 50,670 minutes at p90* (runs 0.21, 0.21, 0.00, 0.21). Nearest on shape and gate: a percentile schedule adopted only on the compilation that reproduces all 24 published means; the order-line grain returns 19 of 24 and the model adopted it anyway.
- **0.17**, Nonprofit & Grant-making, Means-Tested Grant Eligibility Estimation: *Estimate 2,591,394 applicant units eligible for the Winter Relief Grant at 185 percent of the poverty guideline* (runs 0.16, 0.18, 0.18, 0.18). Nearest on the unit: the applicant unit is built from person records (householder, spouse or partner, own children, each subfamily), and the housing-record grain reproduces one of six November shares and no allocation.

Same-domain neighbour, for voice: 0.21, Economics, Retail Market Activity Measurement (stalls joined from neighbouring lettings, pinned by last year's seventeen printed figures).

## Guard

PASS against the existing corpus (last three task114, task115, task116; window of twelve from task105), no WARN, nearest driver task109 at 0.09.

BLOCKs on the note-faithful draft, and how each was cleared:
- `ban.role` (research_desk, task115): the requester redrawn as the director of the office that staffs the conference (statistical_office_head).
- `ban.forcing_event` (vote_or_meeting, task115): the call forced by the statutory certification of the income-tax estimate (statutory_or_regulatory_filing).
- `test.same_driver` and `test.same_puzzle` (population, B, method_or_model_selection and dial_setting, inside the window against task109), and `test.same_driver_older` (task66, task67 v1 and v2 lineage, task86 v2 lineage): the decisive rung recorded under its generator with B as its gate, which is the note's own pattern line ("S1 ... gated by Pattern B"); a differentiation line against task109 is on the card.

WARN answered: `overuse.org_family` (government_agency, 21 builds) on the draft, answered by setting the build in a research and statistics office, the family no build has used. No WARN remains. At batch registration the last three become the pilot siblings, so the furniture bans run again then.

## Changes from the source note

1. **Requester.** The note's staff analyst (research_desk) is now the director of the revenue research office that staffs the conference (statistical_office_head), because ban.role blocks research_desk against task115.
2. **Forcing event.** The note's "the conference sits on 14 November" (vote_or_meeting) is now the conference's statutory certification of the income-tax estimate, which runs on the re-based tiers (statutory_or_regulatory_filing), because ban.forcing_event blocks vote_or_meeting against task115. The finance secretary, not the conference, now adopts the schedule (see change 5).
3. **Organisation family.** A nonpartisan legislative revenue research office (research_or_statistics_office), the same institution as the note's conference staff, recorded in its own family rather than as a generic agency, which 21 builds already use.
4. **Decisive pattern on the card.** Recorded as the note's S1 (a G2 unit construction) with Pattern B as its gate, not B as the decisive pattern, because B first repeats task109 inside the twelve-build window on both structural tests, which no differentiation clears. No rung, figure, file or ask changes.

Added where the note was silent: the personas (drawn with guard.py names), the geography (a fictional state, to keep the note's invented counties), the spine as synthetic, and the as-of date.
5. **Forum and opening (batch registration).** The forum moves from committee_or_panel to minister_or_cabinet, because ban.forum blocked committee_or_panel against task118 in this batch and line_manager_or_team against task116: the state finance secretary adopts the re-based floors on the revenue research office recommendation, and the conference certifies its estimate on them. The planned opening moves from calendar-first to evidence-first, because calendar-first repeats task117.

## Open items for the design stage

- The corpus-direction test (stumping Part 1) treats a corpus that refutes the naive path as an alarm; these tables refute the federal-filing-unit path with every miss in one class and one direction. Write the corpus-direction line and decide it against the measured #1 and #3 record before the ladder is fixed.
  **Settled at design: kept, with four asserted conditions.** See "Calibration corpus", the corpus-direction line.
- First-moves test: the methodology's word "household" beside a shipped dependents schedule may send a strong solver straight to the attachment (Part 1, property 1). Run it on paper.
  **Settled at design.** Run under "Ladder", the first-moves test. No first move lands on the answer; the residual risk is named there.
- The note's asks A and B (withholding by wage month, estimated payments by instalment) may fail the H18 fourth read as figures a person could act on with the schedule unmade; re-cut them to per-tier figures carrying the same devices. Ask C as written names the four constructions; the exemplar's form is the closest reading that does not stand. Without A and B the shape-14 core sits near 23 criteria.
  **Settled at design.** A and B retired as asks (both fail H18: a figure for other periods, actionable with the schedule unmade). Their devices move onto per-tier figures (ask A1 carries the instalment device and the prior-year credit device; the employer deposit ledger stays as inert context and a distractor). Ask C no longer names any construction; the closest-reading form was also rejected (see Tried and rejected), and the validity check is the reproduction disclosure. The shape now reaches 38 criteria (see "Deliverables").
- The requester heads the office that staffs the conference, so the world needs a reason the office does not hold the household construction.
  **Settled at design.** The TY2022 to TY2024 Household Income Tables were compiled for the conference by the state university's fiscal research center under an interagency data agreement that ended with the TY2024 tables; the center's programs stayed with the center under the agreement's data-use terms. TY2025 is the first year the office compiles the tables and the schedule itself. One line in the methodology's revision history carries it; the prompt does not.
- 3,412,000 synthetic return rows is heavy for one pack; settle the format or a scaled state at dataset-generation.
  **Settled at design: a scaled state**, because the corpus has to be rerunnable from shipped records, so four tax years of returns and dependents schedules ship, not one. TY2025 carries 852,947 returns; every count below is at that scale. The card's spine row count and the counts in its driver_concrete are refreshed at stage 3's `guard.py surface` step.

## Design (stage 2)

The world below is a scaled state (TY2025: 852,947 returns). Counts are targets the generator tunes toward and then
asserts as realised; rounded floors and hit counts are asserted exactly. A design-stage feasibility model (scratchpad,
not shipped) confirmed the structure: with the stop rung pinned at $197,100 / $293,100 / $594,200 and the household
tail at $214,100 / $318,100, 1,475 trust households lift the top floor to $741,819 with 972 crossers against the 976
the target needs, the dropped-dependent cell lands at $657,500, the trust income is 3.55 per cent of the $500,000 to $1M
class's AGI and dependents' returns hold 2.00 per cent of resident AGI. Those are the model's figures; the built pack's
are in the Build record (floor units $214,063 / $318,081 / $742,043, 976 crossers, the dropped-dependent floor unit
$657,057, dependents' returns 2.019 per cent of resident AGI).

### Changes made at design (on top of "Changes from the source note")

6. **Scale.** TY2025 returns 852,947 (code 1 719,213, code 2 24,281, code 3 109,453), a quarter of the draw's
   3,412,000, because four tax years of returns and dependents schedules have to ship for the corpus to be rerunnable.
   Every count in the note is non-round; the source note's round thousands were a generation tell.
7. **Trust group.** Own AGI $520,000 to $742,000 (not $620,000 to $740,000) and $30,000 to $130,000 per return (not up
   to $90,000; realised at build as $30,804 to $99,500, see the Build record), so the group is 34 per cent of the household heads in its band instead of nearly all of them.
8. **Twin pair.** Kessler and Abington published at 301 against 287 (4.7 per cent apart) instead of 117 against 58,
   because a 2.02x pair makes the stop rung miss one county by 50 per cent, which contradicts the stump sentence's
   "every miss a few per cent short" and turns the corpus into a loud alarm.
9. **Rung figures from the model.** Rung 0 $520,000 and rung 1 $562,000 at the top floor (the source note's $504,000
   and $565,000; realised at build as $531,000 and $551,000), and the all-filer grid cells moved down because commuters now sit below the floors.
10. **Ladder** extended to five rungs (the dropped-dependent partial is rung 3). **Asks** re-cut to per-tier figures
    (H18). **Chart** re-cut: no rival-construction series; each tier's band carries its capital-gain share of AGI.
11. **Published classes fixed:** $100K to $200K, $200K to $300K, $300K to $500K, $500K to $1M, $1M to $1.5M, $1.5M to
    $2M, $2M to $5M, $5M to $10M, $10M or more.

### The world, TY2025 targets

- 41,862 resident couples file separate state returns (83,724 returns), 29,722 of them (71 per cent) among the top two
  deciles of federal filing units. Each separate return carries the federal primary TIN, giving 677,351 federal filing
  units.
- 94,807 resident returns are filed by people another resident return claims (2.0 per cent of resident AGI), each TIN
  on exactly one schedule, every one a child of its claimant. Attached, they stop being units: 582,544 household units.
- Trust group: 2,350 of those returns carry $30,804 to $99,500 of trust and investment income ($171,703,020 in all),
  claimed by 1,475 households whose own AGI is $520,000 to $742,000. Attached, 976 of them cross $742,000; with the 4,850
  households whose own AGI is already above it, exactly 5,826 (the top 1 per cent) sit at or above it. No household total
  reaches $1M.
- Conveyor (every year, published or not): N households cross each of $100K, $200K, $300K and $500K on their children's
  income (N = 23, 10, 30 and 30 for TY2022 to TY2025); in every class below $500K the attached income of households that
  stay in the class balances the boundary flows to the dollar, so the stop rung ties every class cell outside
  $500K to $1M. No household of $1M or more holds attached income. Other filing dependents sit in households under
  $100,000 and stay under it.
- Commuters (codes 2 and 3): 133,734 returns, median AGI $69,185 realised, 899 of them (0.67 per cent) at $500,000 or
  more.
- Dependents schedule: 466,638 rows realised (every claimed dependent, filer or not); 94,807 of the claimed TINs file.
- Ranks: households k = 58,255 / 29,128 / 5,826; federal filing units k = 67,736 / 33,868 / 6,774.

### Gate G

**Gate G line.** method_or_model_selection; surface_read_dependency no; stumping_family analytical_non_defect;
sole_data_defect no; no shipped artifact computes a TY2025 schedule or ranks one; the difficulty survives deleting every
voice and the licensed basis.

- **Litmus.** No. Every figure in the pack is correct: the return files, the dependents schedules, the Department's
  all-filer table and the conference's published tables, and no stakeholder's reading of their own figures is
  overturned. The Department's table is right about returns and says so in its header; the fiscal office's basis is
  right about filing units. Nobody in the pack reports a TY2025 schedule at all, so the task corrects no read: the
  difficulty is constructing the unit the published tables count, which no file stores. The framing limb holds too:
  the chief economist's view is a belief about the unit, never a reading of a reported number.
- **Primary mechanism:** method_or_model_selection (the construction is selected by exact reproduction of the
  published cells), on a G2 grain construction with G10 underneath.
- **Flags:** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
- **Deletion test.** Delete the chief economist's belief, the statistics chief's remark and the fiscal office's
  licensed basis. The return file still ties to the Department's table to the row and the dollar, the filing unit still
  reproduces 58 of 69 published cells, and the household still has to be built through a link no column on the
  dependent's return carries. Still hard.
- **Clean-data test, three depths.** Fill: no file has a gap, a sentinel or a missing record. Correct the semantics:
  every field means what the codebook says, including the schedule's description as the exemption-credit list.
  Replace the instrument: a return-processing system records households nowhere by law; a household exists only
  through claiming relationships, which the law records on the claimant's schedule, so the "better instrument" is the
  construction itself. Generator assertion on the one repairable gap: give every dependent's own return a claimant
  field, recompute, and assert answer(repaired) = answer(shipped), naive(repaired) = naive(shipped), answer != naive.
- **Lens-swap test.** The naive population (719,213 resident returns) and the answer's (582,544 household units)
  differ in membership; no relabelling of rows maps one onto the other. Asserted on the counts.
- **Pre-draw identity.** floor_p = Q_p over households of the sum of member AGI. The partition into households is
  neither shipped nor filed (the methodology names it and never defines it); it is forced only by the corpus.

### Entity and unit of value

The state's nonpartisan revenue research office re-bases the income-tax tiers the Revenue Estimating Conference's
forecast carries. A schedule is scored on whether its construction reproduces every published cell of the conference's
last three Household Income Tables (the methodology's gate); the floors are then what the certified estimate runs on.
Two counts both read as the size of the population: **returns** (the file's rows, the Department's all-filer table)
and **household units** (the conference's tables, which no file stores). They place the floors differently because 13.2
per cent of resident returns are dependents' own returns that are not units, separately filed spouses are one unit,
and the income on a dependent's return belongs to the claimant's household.

### Decision

Exactly one schedule of three floors (top 10, 5 and 1 per cent of full-year resident household units, household AGI,
each to the nearest $1,000) for TY2025, adopted by the finance secretary on the office's recommendation, with the
conference certifying its income-tax estimate on it. Shape: a structure the body adopts (Part 2), as a dial setting.
**Why the quantity is retrospective:** the methodology re-bases the tiers on the latest processed year, so the floors
measure TY2025; the decision they drive (which tiers the certified estimate runs on for the coming forecast) is forward,
no forecast is graded, and the objective stays Descriptive & Distribution Analysis.

### Answer

**$214,000 / $318,000 / $742,000.** On the natural pipeline (rung 0, $166,000 / $243,000 / $531,000) the answer sits
28.9, 30.9 and 39.7 per cent higher, and it is the extreme (maximum) cell of the 12-cell grid at every floor (L5). Margin
over the nearest wrong cell: 11.5 per cent at the top floor (dropped dependents). At the 10 and 5 per cent floors the
dropped-dependent cell coincides by design (no published class from $100,000 to $500,000 separates the two), and the
nearest differing cell is the stop rung, 7.9 per cent below. **The guard that binds is the separation floor**, not the
1.20x rung margin: the answer is a figure graded to the nearest $1,000 and there is no ranking to change.

### Ladder

| Rung | Gap | Construction | Floors (10 / 5 / 1 per cent) | Cells reproduced | Killed by (one shipped fact) |
|---|---|---|---|---|---|
| 0 | objective | every return is a unit, all filers | $166,000 / $243,000 / $531,000 | 0 of 69 | the methodology's "full-year resident" with the codebook's residency codes |
| 1 | population (scope) | full-year residents, each return a unit | $179,000 / $262,000 / $551,000 | 3 of 69 | the published class cells: only the three totals tie |
| 2 | population (unit, G10) | federal filing units: separate returns recombined on the federal primary TIN | $197,000 / $293,000 / $594,000 | 58 of 69 | the dependents schedule: only attaching the dependents' own returns reproduces the 11 missed cells |
| 3 | population (partial) | filing units with dependents' own returns dropped | $214,000 / $318,000 / $657,000 | 55 of 69 | the three published total-AGI cells, which every complete partition ties and this one misses by 2.0 per cent |
| 4 | decisive (G2, selected by G16) | households: each filing unit plus the own returns of the dependents its schedule claims | **$214,000 / $318,000 / $742,000** | 69 of 69 | (none) |

**Why each rung is a place to stop.**
- Rung 0: the file ties to the Department's all-filer table to the row and the dollar; it is the file's own grain.
- Rung 1: the methodology's population on the authoritative code list, and it reproduces all three published totals
  exactly, which reads as confirmation.
- Rung 2: the literature's tax unit, built through the only key the return carries for it; 58 of 69 cells, every miss
  one-sided, under 5 per cent and inside the $500,000-and-over region, totals tied. A careful analyst reads the residue
  as a classification quirk in one class and files.
- Rung 3: a solver who has accepted rung 2's fit and then meets the dependents' returns in the file applies the
  top-income literature's convention (tax units net of dependent filers) without re-running the gate; the unit count
  falls to the households' and two of the three floors are already right.

"A solver who does everything right up to rung 2 commits to $197,000 / $293,000 / $594,000." The stump rung is rung 2;
the decisive move is rung 4. Rung 3 is the priced partial (L3): the first step toward the dependents is punished by the
gate (55 against 58).

**Worth of each move on the graded floors** (10 / 5 / 1 per cent): rung 0 to 1 +7.8 / +7.8 / +3.8 per cent; 1 to 2
+10.1 / +11.8 / +7.8; 2 to 3 +8.6 / +8.5 / +10.6; 3 to 4 0.0 / 0.0 / +12.9; 2 to 4 +8.6 / +8.5 / +24.9. **Sign
direction:** every correction raises every floor or leaves it; the answer is the extreme cell, so no partial application
can overshoot or cancel onto it.

**The seven survival properties, rung 4.** (1) Written nowhere: the methodology says "full-year resident household
units" once and never says what a household holds; no document uses the word beside the schedule. The word does raise
the question, and its natural answer is the filing unit, which the corpus nearly confirms; that is the concession this
build makes. (2) Corpus: **not met by design**, the corpus pins rung 4 (settled in the corpus-direction line).
(3) No arithmetic symptom: every construction is a complete partition of the same resident returns, so totals tie, row
counts reconcile and no key repeats. (4) Not a row predicate: membership is a property of another return, reached
through a two-hop join and resolved into components; no column on the dependent's return flags it. (5) The enumeration
is arithmetic: 94,807 memberships are computed, none is flagged, and the construction has no menu. (6) No cutover date:
separate filing and dependents' returns run unchanged through all four years. (7) Survives deletion (above).

**First-moves test, on paper.** Move 1, residents by return: 3 of 69. Move 2, the natural operationalisation of
"household" in a tax file, spouses joined on the federal primary TIN: 58 of 69. Move 3, the corpus back-test on it:
misses one-sided and small. Move 4, the literature's treatment of dependent filers, dropping them: 55 of 69, worse.
No first move lands on the answer. The residual risk is a solver who reads "household" the way distributional
analysts do (all income of the people the unit supports), joins the schedule's TINs to filers before running the
corpus, and lands; that solver is the one response the bar allows. The schedule's own shape works against it:
466,638 listed dependents of whom 94,807 file, so it reads as a list of children rather than a list of returns.

### Position table (figure form)

| Rung | Floors | Distance from the answer (10 / 5 / 1) | Cells |
|---|---|---|---|
| 0 | $166,000 / $243,000 / $531,000 | -22.4 / -23.6 / -28.4 per cent | 0 |
| 1 | $179,000 / $262,000 / $551,000 | -16.4 / -17.6 / -25.7 | 3 |
| 2 | $197,000 / $293,000 / $594,000 | -7.9 / -7.9 / -19.9 | 58 |
| 3 | $214,000 / $318,000 / $657,000 | 0.0 / 0.0 / -11.5 | 55 |
| 4 | $214,000 / $318,000 / $742,000 | answer | 69 |

The answer leads no intermediate rung at the top floor; rung 3 coincides with it at the two lower floors (stated, and
priced by the gate). No rung sits within 6 per cent of the answer at a floor where it differs.

### Discriminator dominance (figure form)

The decisive move is worth +8.6 / +8.5 / +24.9 per cent on the graded floors against a separation floor of 6 per cent and
a quantile-convention spread of at most $129 at the answer's floors ($125 / $129 / $117, 0.02 per cent at the top
floor). The count effect (14.0 per cent fewer units)
carries all three floors; the shape effect (976 households crossing on their children's income) carries the top
floor's extra 12.9 per cent over the dropped-dependent cell. The stop rung's only carried advantage is its fit (58 of 69,
84 per cent of cells), and the gate converts any fit short of 69 into a refusal, so nothing it carries can outweigh
the move.

### Correction grid

Residency (code 1, all filers) x unit (return, federal filing unit) x dependents' returns (separate units, dropped,
attached): 12 cells. Floors rounded; distance at the top floor; cells reproduced.

| Residency | Unit | Dependents | Floors | Top floor | Cells | Violates |
|---|---|---|---|---|---|---|
| code 1 | filing unit | attached | $214,000 / $318,000 / $742,000 | answer | 69 | |
| code 1 | filing unit | dropped | $214,000 / $318,000 / $657,000 | -11.5% | 55 | total cells |
| code 1 | filing unit | separate | $197,000 / $293,000 / $594,000 | -19.9% | 58 | $500K to $1M and county cells |
| code 1 | return | attached | $196,000 / $283,000 / $618,000 | -16.7% | 3 | class cells (spouses split) |
| code 1 | return | dropped | $195,000 / $282,000 / $592,000 | -20.2% | 0 | totals and class cells |
| code 1 | return | separate | $179,000 / $262,000 / $551,000 | -25.7% | 3 | class cells |
| all | filing unit | attached | $194,000 / $289,000 / $640,000 | -13.7% | 0 | totals, class cells, county cells (residency) |
| all | filing unit | dropped | $194,000 / $289,000 / $600,000 | -19.1% | 0 | residency, totals |
| all | filing unit | separate | $180,000 / $268,000 / $565,000 | -23.9% | 0 | residency |
| all | return | attached | $179,000 / $259,000 / $573,000 | -22.8% | 0 | residency, spouses |
| all | return | dropped | $179,000 / $259,000 / $560,000 | -24.5% | 0 | residency, spouses, totals |
| all | return | separate | $166,000 / $243,000 / $531,000 | -28.4% | 0 | residency |

**Partial applications, swept separately:** dependents' income attached while their returns stay units (income counted
twice): $197,000 / $293,000 / $639,000 (-13.9 per cent), 66 of 69, refused by the three totals; attachment to the
claiming spouse's own return without recombining spouses is the (code 1, return, attached) cell. The all-filer cells
reproduce none of the 69 (realised at build: each appendix county holds a part-year resident at $500,000 or more, so
no all-filer construction ties a county cell). Nearest wrong cell where it differs: 11.5 per cent at the top floor and 7.9 per cent at the two
lower floors.

### Calibration corpus

- **Form.** The conference's Household Income Tables for TY2022 to TY2024: for the nine classes from $100,000 up,
  household units and AGI ($ thousands), plus total AGI, 19 cells a year, 57 in all; the TY2024 table's appendix gives
  household units at $500,000 or more in the twelve largest counties. 69 cells.
- **Back-test.** Households reproduce 69 of 69 exactly at the published precision (rebuilt from whole dollars, so no
  rounding path splits). Rivals: income attached with units kept 66, filing units 58, dropped dependents 55, residents
  by return 3, attached to a return 3, every all-filer construction 0. Charitable scoring: the smallest rival miss is
  1 unit on a county cell (the all-filer households, whose part-year residents add one to each appendix county and
  whose totals run 17.5 to 17.7 per cent over), 2 units on a county cell for the stop rung, 2.0 per cent on a
  total-AGI cell (the two partials) or 3.1 per cent on a class AGI cell, all outside anything the published rounding
  (whole counts, $ thousands) excuses.
- **Stop rung's misses, exactly 11.** $500,000 to $1M household units short by 23, 10 and 30 (TY2022 to TY2024, all
  under 0.5 per cent); that class's AGI short by 3.4, 3.1 and 3.6 per cent; five county cells short (Kessler 14 of
  301, 4.7 per cent; four others 2 to 4 each, under 1 per cent). Every class cell outside $500,000 to $1M ties to the
  dollar.
- **Twin pair.** Kessler and Abington hold 287 federal filing units at $500,000 or more each and the same count of
  resident returns at $500,000 or more, with dependents' own returns within 2 per cent of each other (3,031 and 3,001);
  published household units at $500,000 or more are 301 against 287. Kessler's 14 are households just under $500,000 whose children's custodial-account
  income carries them over; Abington's comparable dependents are claimed lower down. The pair's job here is to show
  that the extra count lives in who claims whom, which no county aggregate carries; its gap is sized to the stump
  sentence, not to the 2x lookup-killing form (no candidate is transferred by resemblance in this build).
- **Every rule the golden composes has a cell that breaks if it flips:** residency (the totals), spouse recombination
  (every class cell), attaching rather than dropping (the totals), attaching income rather than counting it twice (the
  totals), the claimant's county (the appendix), membership by claim (the twin).
- **Blind to:** the count of household units. No published cell covers units under $100,000 and there is no total-units
  cell, so the largest effect on the floors (14.0 per cent fewer units) shows only through the construction the cells
  pin.
- **Resemblance points at the decoy:** TY2025's class shares sit nearest TY2023's, the year the stop rung comes closest
  (10 units short).
- **Corpus-direction line.** Under the stop rung the corpus returns 58 of 69, every miss one-sided: the device
  accumulates rather than nets, so the corpus refutes the stop rung, which Part 1 treats as an alarm. **Decided: kept**,
  on the only record of this exact architecture: the client's measured #1 (failed back-test shipped anyway) and #3
  (close but inexact match accepted) decided 19 of 64 accepted tasks, 14 of them under 0.50, every one a corpus
  refuting the obvious construction on a minority of its cells (19 of 24, 10 of 14, 24 of 32 published figures). The two
  in-house deaths behind the alarm differ on the property that matters: task92 v2's corpus missed the naive read by
  18.45 per cent on the graded quantity itself, and task89 v5's workbook measured the same quantity the answer is.
  Here the refuted cells are class counts, class AGI and county counts, never floors. Four conditions, each asserted:
  (1) no stop-rung miss exceeds 5 per cent on any cell; (2) the first step toward the dependents (dropping them)
  reproduces fewer cells than the stop rung, 55 against 58; (3) the refuted cells are not the graded quantity, so a
  solver at the stop rung learns it is a few per cent short in one class, never that its top floor is 20 per cent low;
  (4) every total ties under every complete partition, so the refutation never shows as a missing return.

### Pins and counter-pins

- **Filed pins, the methodology (authority 1), each stated once:** P1 "Tiers are drawn on full-year resident household
  units at the 10, 5 and 1 per cent marks of household AGI; every such unit counts in the base whatever its AGI, and each
  floor is stated to the nearest $1,000." P2 "A tier schedule is adopted only on a construction that reproduces every
  published cell of the three most recent Household Income Tables." P3 tier bands: tier 1 at or above the 1 per cent
  floor, tier 2 from the 5 per cent floor up to the 1 per cent floor, tier 3 from the 10 per cent floor up to the 5 per
  cent floor, membership by the adopted floor. Ask organs: receipts are cash received toward the tax year, and an
  overpayment credited from a prior year's return is not a receipt of the year it is credited to; withholding is
  measured on employers' wage statements; capital gain is the amount entering AGI. Licensed wrong basis: the
  legislative fiscal office draws its own tiers on federal filing units and will put its schedule beside the office's at
  the certification. Revision history: TY2025 is the first year the office compiles the tables itself.
- **Codebook (authority 4, field semantics only):** federal_agi is federal adjusted gross income as reported on the state return and the only AGI the extract carries (state taxable income is a separate, plainly named column); residency codes 1 to 3; the federal primary TIN field (equal to the
  filer's own TIN except on a spouse's separate state return); the schedule as "dependents claimed for the exemption
  credit"; ledger timestamps in UTC; instalment due dates with the weekend and holiday rule; the Schedule D extract as
  the latest version received; the TIN register (TIN match cases); the two wage-statement channels.
- **Empirical pin:** the household construction, the unique survivor at 69 of 69.
- **Counter-pins: none.** The Department's table header ("Returns processed, all filers") names a different
  population correctly; the fiscal office's basis is attributed, never endorsed; every voice holds a belief. Sweep: the
  word "household" appears only in P1, the table titles and the fiscal-office line; "filing unit" only in the
  fiscal-office line.
- **Voices (beliefs, never figures):** Manuel Stevenson, chief economist: every return is a taxpayer, so build the tiers
  off this year's returns. Brittany Shepard, the Department's statistics chief: her table ties to the processed file to
  the dollar and that is the file she would trust. Jeffrey King, legislative fiscal office: the federal return is the
  tax unit and his office tiers on it. No voice supports the household construction.

### Fork grid: the 22-axis closure table (determinism-check A.5)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | full-year residents (code 1) | filed P1; C2, the totals refuse codes 2 and 3 under every unit |
| 2 | Unit of account | filing unit plus the own returns of the dependents its schedule claims | C2, 69 of 69 against 66, 58, 55, 3, 0 |
| 3 | Attribution window | tax year 2025 on every record; A1 instalments by state-time receipt under the filed due-date rule | C1 on the main path (every record carries its tax year, no other year in the file); filed rule for A1, whose clock is its device |
| 4 | As-of dating | residency and claims as filed for TY2025; A2's schedule of record as of the extract date | C1: no filing unit changes residency, each claimed TIN on one schedule, no TIN changes on a return; filed version rule for A2 |
| 5 | Version basis | returns as of record (accepted amendments already in AGI); A2 latest accepted version | C1 on the main path (one row per filer per year, no amendment rows); filed for A2 |
| 6 | Divisor and denominator | every household unit counts in the base, zero and negative AGI included; shares over the tier's household AGI | filed P1; C2, dropping negative-AGI units misses the totals |
| 7 | Weighting | none, each unit once | C1, no weight column ships |
| 8 | Window length | one tax year | filed |
| 9 | Boundary inclusivity | membership at or above the adopted floor | filed P3; C1, the rank-k unit sits in [F, F + $250) and rank k + 1 in [F - $250, F), so the rounded floor selects exactly the top k; each boundary household carries no estimated payment, capital gain or wage statement, so the asks are identical under rank membership |
| 10 | Rounding path | floors rounded once from the floor unit's exact AGI; ask sums from whole-dollar records; shares rounded once from unrounded sums | filed; C1, whole-dollar records, every share at least 0.02 points from a .x5 edge |
| 11 | Tie-break | ties at a floor rank | C1, no two households share an AGI among ranks k - 2 to k + 2 at any floor |
| 12 | Maturity | TY2025 processing complete at the extract (after the 15 October extension deadline) | C1, no TY2025 return or payment after the extract date |
| 13 | Order of operations | residency filter before or after building households | C1, no filing unit mixes codes and every dependent of a code-1 claimant files code 1, so both orders give the same 582,544 units |
| 14 | Row order | irrelevant | C1, asserted under six row orders |
| 15 | Duplicate resolution | one return per filer per year, one schedule row per claimed TIN | C1, zero duplicates asserted on both keys |
| 16 | Identity normalisation | one TIN token scheme across returns and schedules; ask files keep TINs as reported | C1 on the main path; filed register plus hazard H4 on the ask paths |
| 17 | Netting against gross | AGI net by definition; receipts net of dishonoured items | filed |
| 18 | Dimensional units | dollars; published AGI in $ thousands per each table's header | filed; rebuilt AGI compared at the published unit |
| 19 | Code semantics | residency, filing status, relationship, payment kind, disposition, register status | filed codebook; C1, every filing dependent is a child, so an "attach only children" reading selects the same units |
| 20 | Integerisation | counts integral, floors from integer AGI | not applicable, stated |
| 21 | Scope of a clause | "three most recent tables" = TY2022 to TY2024 with the appendix inside "every published cell" | filed; C1, the appendix sits in the TY2024 table file |
| 22 | Forward window | the forecast is not graded; the graded call is the TY2025 schedule | not applicable, stated under Decision |

**Quantile convention (axes 9 to 11 together):** nearest rank at k, k - 1 and k + 1, Hyndman-Fan types 1 to 9 and the
midpoint all round to the same three floors, for the answer and for the stop rung, asserted. The flip condition: a floor
moves only if a unit within two ranks of k lands outside [F - $250, F + $250), which the generator forbids.

### Deliverables and criteria arithmetic

Prompt shape 14, cuts of a distribution, the segment being the tier. Two files, both fixed by the draw.

1. **tier_schedule.xlsx** (Data): the schedule (three floors, the household-unit count, the construction) with the
   2022 to 2024 published cells beside their rebuild in the published units and the count matched; the tier base, one row per tier: 2025
   estimated-tax receipts at each of four instalments, 2025 withholding, 2025 net capital gain and its share of the
   tier's AGI.
2. **tier_floors.png** (Visual): the count of units at or above each AGI from $100,000 up on log scales, the three floors
   as vertical lines carrying their values, each tier's band labelled with its capital-gain share (one decimal, as in the workbook), the schedule in the
   title.

Script-generated: both. Unit and rounding: the floors to the nearest $1,000 in the call sentence; the rebuild in the
published units (counts, AGI in $ thousands); whole dollars scoped to the tier list; the share pinned to one decimal
place, and the chart's band labels carry the same share at the same rounding.

**Prompt** (`prompt.md`): evidence-first opening (the processed year landing is what forces the re-base), the role as
a short sentence of its own, one belief clause (the chief economist's), the call as one quotable sentence closing the
context, then the workbook and the chart, each paragraph opening on the schedule. voice-check 120: 233 words, 25.9
words a sentence, context 41.2 per cent, a sentence under eight words, two rounding tags, no "because", no flag.
Nothing in it fixes the unit, the population, the basis or the window; no input file, method or trap word; the tiers
are never called "the top 10 per cent tier", so the prompt cannot counter-pin P3's bands.

**Arithmetic:** the three floors 3 + the construction, the unit count and the reproduction count 3 + estimated-tax
receipts 3 tiers x 4 instalments 12 + withholding 3 + capital gain and share 3 x 2 6 + the reproduction table 1 + chart
parts (distribution on log scales 1, three floor lines with values 3, three share labels 3, title 1) 8 + two files 2 =
**38 criteria.** Distinct findings: the schedule (a cut of a distribution), the tier base (receipts timing, withholding,
gains), the validity check (the reproduction). Named-parts visual yes; breakdown at an explicit grain yes (tier x
instalment); robustness check yes (the reproduction). The ask set does not over-determine any constant: no ask carries
a unit count, a dependent count or a floor under another construction.

**Each ask fails under a wrong analytical path:** on the stop rung every per-tier figure is computed on a different set
of units (every cell wrong at once); on the right units each figure still crosses at least two silent devices (ledger
below).

### Ask ledger (supplemental-stumping Part 9)

Every ask carries both layers: the construction (tier membership on the household construction and the adopted floors;
a household's records are those of its filer, its separately filing spouse and its dependents) and at least two devices
on files the main call never reads. Root-cause fictions (law 9): the Department's 2024 move to a hosted payments and
information-returns platform (it stamps times in UTC, keeps TINs as reported, and left paper wage statements with the
keying vendor) feeds D8, D4 and H4; the amended-return backlog feeds D2; credit elections and dishonoured items are
ordinary revenue accounting.

| Ask | Figures | Primary device | Hazards | Use (who acts) | H18 line |
|---|---|---|---|---|---|
| A1 estimated-tax receipts by tier and instalment | 12, whole dollars | D8 clock: received times in UTC, instalments due 11:59:59 pm state time (Central), a weekend or holiday due date rolling to the next business day (15 June 2025 is a Sunday) | H1, H2, H4 | the estimating staff spread each tier's estimated tax over the four instalment months from the 2025 pattern | component: the tier base the certified estimate runs on; not computable with the schedule unmade |
| A2 net capital gain by tier, and its share of tier AGI | 6 (whole dollars; percentage to one decimal) | D2 version of record: the Schedule D extract is the latest version received; the version of record is the latest accepted, dispositions and figures in the amended-return log | H3 | the capital-gains assumption is applied tier by tier to each tier's 2025 gains; the share sets each tier's exposure | component |
| A3 withholding by tier | 3, whole dollars | D4 absent channel: paper wage statements keyed by the capture vendor sit in their own file and layout; the e-file extract carries no sign of them | H4 | the withholding forecast grows each tier's 2025 withholding with wages | component |
| Reproduction table | 1 | none (audit trail) | | the secretary's assurance the schedule meets the gate | audit trail |

**Per-ask stops** (targets as distance from the golden, asserted per figure):

| Ask | S1 natural path | S2 half-handled | S3 over-cleaned | S4 right rules, filing-unit tiers | Lazy delta |
|---|---|---|---|---|---|
| A1 | UTC dates, every ES and transfer row, no returned items, no register: April +6 to +18%, other cells -4 to +6% and never within 1% | clock handled, the rest natural | every transfer row and every returned item dropped: -1 to -4% | every cell wrong by the tier shift | at least 1% in every cell |
| A2 | extract as is, net gain-or-loss column: -5 to -12% per tier | versions handled, loss limit missed: -1 to -4% | original schedule for every amended return: 2 to 5% off | every tier wrong | at least 4% per tier, share at least 0.3 points |
| A3 | e-file statements only, no register: -4 to -8% per tier | paper added, register missed: -1 to -2% | paper statements from employers that also e-filed dropped: -0.5 to -2% | every tier wrong | at least 3% per tier |

**Hazard table.**

| Hazard | Family | Moves | Delta when mishandled |
|---|---|---|---|
| H1 transfers: credits elected on TY2024 returns posted late January to May 2025 as transfer rows citing the TY2024 return are not receipts; transfer rows citing a payment misapplied to another year are cash, dated by the original payment | D5 with D7 linkage | A1 | April cells +8 to +15% if credits counted; every cell -1 to -3% if all transfers dropped |
| H2 dishonoured items: the ledger records payments as received and the returned-items file reverses them; items re-presented and paid stay | D4 | A1 | every cell +1.5 to +3%; -0.3 to -1% if re-presented items are dropped too |
| H3 loss limitation: the extract carries net gain or loss and the amount entering AGI ($3,000 limit, $1,500 on a separate return) | D3 | A2 and the chart's share labels | -1 to -4% per tier |
| H4 TIN resolution: wage statements and payments keep the TIN as reported; the register links a reported number to its filer (resolved rows only) | D7 | A1, A3 | A1 -1 to -2.5% per cell; A3 -1 to -2% per tier |

- **Organ pairs (law 2), split across files:** clock, the codebook's timestamp sentence plus the due-date rule (two
  sentences, one file) against the timestamps themselves; transfers, the methodology's receipts rule against the
  transfer rows' source reference and the TY2024 return's credit-elect line; dishonours, the codebook's ledger sentence
  against the returned-items file; register, the codebook sentence against the register; versions, the extract's own
  description and the codebook's version rule against the amended-return log; loss limit, the methodology's capital-gain
  sentence against the two Schedule D columns; paper channel, the codebook's channel list against the paper file.
- **Spans** (counted on roles, so they hold however stage 3 groups the prior-year files): A1 crosses the TY2025
  returns and schedule, the prior-year returns and schedules, the published tables, the methodology, the codebook, the
  ledger, the returned-items file and the register (at least 9 files, about 15 columns); A2 the construction files, the
  methodology, the codebook, the Schedule D extract and the amended-return log (at least 8 files, 12 columns); A3 the
  construction files, the methodology, the codebook, both wage-statement files, the register and the referee (at least
  10 files, 12 columns). Necessity verified by the matrix at stage 3.
- **Referee (exactly one):** the employers' annual reconciliation summary (statewide state withholding on all wage
  statements, by filing channel). It arbitrates the e-file against paper disagreement at state level and hands over no
  tier figure.
- **Main call's declared row population:** returns TY2022 to TY2025 (return_id, tax_year, residency_code, filer_tin,
  federal_primary_tin, county_code, federal_agi), dependents schedules TY2022 to TY2025 (claimant_return_id,
  dependent_tin, relationship_code), the 69 published cells, P1 to P3 and the licensed-basis line, the codebook's return
  and schedule sections. **Device rows inside it: 0. Hazard rows inside it: 0.** Every device and hazard lives in a file
  the main call never opens; asserted by deleting every ask-path file and recomputing the schedule and all rung hit
  counts unchanged. The TY2024 credit-elect column is a read-only antidote in an off-path column and carries no device.
- **Independence:** three primaries from three families (D8, D2, D4), no family repeated; every graded figure sits under
  at least two devices; composed deltas asserted for every subset of mishandlings (all 15 on every A1 cell, the
  transfers-alone subset leaving September and January untouched as built; 3 on each A2 and A3 figure), none within 1
  per cent of the golden (192 assertions at build, nearest 1.39 per cent).
- **Pair arithmetic (Part 0).** Rubric plan: recommendation block 38 (the floors and their three components), instruction
  following 7 (files, sheets, format), asks 55 over 30 criteria (A1 12, A2 6, A3 3, chart share labels 3, all
  device-carried; reproduction table 1 and chart floor lines and title 4, construction-only; log-scale plot 1, format).
  r, the recommendation criteria a wrong call keeps, about 3. Cracker sheet: catch rates assumed 0.55 for each silent
  device and hazard and 0.65 for the loss-limit hazard (two plainly named columns) and for the paper channel (the
  referee points at it); a figure survives only when every device on it is handled, so A1 0.15 (April 0.09, three
  devices elsewhere), A2 0.36, A3 0.36, share labels 0.36, giving q = 0.25 on the 24 device-carried criteria;
  Lc = (5 + 1 + 0.25 x 24) / 30 = 0.40. Mirror sheet (stop rung): every per-tier figure wrong, Ls = 1 / 30 = 0.03.
  55 x (0.40 + 0.03) = 24.0 against 28 - r = 25: **pair about 39.5**, under 40 with a thin margin. With no top
  response on the call the pair sits near 12. Lever if a round shows leakage: the denominator (Part 3) before any ladder
  work. Note on the pair simulation: because every ask carries the construction layer, ask answers move between the
  cracker and mirror sheets by design; the sheets are read on their totals.
- **Distractors (two, named in metadata.json at stage 3):** the Department's Returns Processed by AGI Class (TY2025, all
  filers), and the employer withholding-deposit ledger dated by receipt (the retired ask A's file, inert).

### Assertion plan (52)

Main call: (1) TY2025 counts: 852,947 returns, 719,213 resident, 677,351 filing units, 582,544 households. (2) Answer
floors round to $214,000 / $318,000 / $742,000. (3) Units at or above each adopted floor equal k (58,255 / 29,128 /
5,826). (4) Rank-k and rank-(k+1) units inside [F, F + $250) and [F - $250, F) at all six answer and stop-rung floors.
(5) Quantile-convention convergence across nearest rank (k - 1, k, k + 1), Hyndman-Fan 1 to 9 and the midpoint.
(6) Stop rung $197,000 / $293,000 / $594,000. (7) Rung 3 $214,000 / $318,000 / $657,000. (8) Rungs 0 and 1 realised,
recorded here at stage 3, each at least 15 per cent below the answer at every floor. (9) Floors non-decreasing rung by
rung at every floor, strictly increasing at the top floor. (10) Hit counts 0, 3, 58, 55, 69. (11) Partials: 66 hits at
$197,000 / $293,000 / $639,000; 3 hits at $196,000 / $283,000 / $618,000. (12) All 12 grid cells computed; the answer is
the maximum at every floor. (13) Every losing cell mapped to the shipped rule it violates. (14) Trust group: 1,475
households, 2,350 returns, own AGI in [$520,000, $742,000), 976 crossing, no total at $1M. (15) Dependents' returns hold
2.0 to 2.1 per cent of resident AGI; rung 3 misses each total by -1.9 to -2.2 per cent. (16) Households reproduce 69 of
69, rebuilt from exact dollars. (17) Stop rung misses exactly the 11 named cells, each one-sided and under 5 per cent.
(18) Every class cell outside $500,000 to $1M ties under the stop rung to the dollar, every published year (the
conveyor). (19) No attached income in any household at $1M or more. (20) Twin: 287 and 287 filing units, published 301
and 287, households reproduce both, a county-symmetric allocation fails one. (21) TY2025 class shares nearest TY2023's;
stop-rung miss smallest in TY2023. (22) No published cell below $100,000 and no total-units cell. (23) No filing unit
mixes residency codes; every dependent of a code-1 claimant files code 1. (24) Each claimed TIN on one schedule; one
return per filer per year. (25) Every filing dependent is a child; no chains; no married dependent; no dependent is a
separately filing spouse. (26) Filter order gives the same 582,544 units. (27) Six row orders give the same floors and
counts. (28) Zero and negative AGI units present and in the base; dropping negative-AGI units misses the totals.
(29) Clean-data test on the claimant-field repair (three equalities). (30) Lens-swap counts differ. (31) No shipped file
carries any floor of any construction (grep for every figure in the grid). (32) Single statement: P1, P2 and P3 each in
exactly one file; "household" and "filing unit" only where the pins section allows. (33) Generation tells: no published
total on a round boundary, no share an exact round figure.

Ask layer: (34) Golden A1 12, A2 6, A3 3; chart labels equal A2's shares to the same rounding. (35) Every stop S1 to S4 per figure and its
distance (at least 1 per cent; A2 shares at least 0.3 points). (36) Composed-subset deltas per figure. (37) Separation:
ask-path files deleted, schedule and hit counts unchanged. (38) Necessity matrix: each device alone moves only its asks,
by its stated range. (39) Hygiene battery on each wrong path comes back clean. (40) Over-cleaner per device lands on S3.
(41) Fairness per device: unique handling, golden reproduced from the bytes. (42) Boundary households carry no estimated
payment, gain or wage statement; asks identical under rank membership. (43) Shares at least 0.02 points from a .x5
edge. (44) Referee equals e-file plus paper statewide withholding exactly. (45) No marker (batch id, channel flag, load
stamp) isolates device rows. (46) Oracle sweep: no shipped figure equals a tier-level golden. (47) Device-vocabulary
grep: each device's organ sentence appears once and no file narrates a device.

Pack: (48) 10 or more files, 3 or more formats, a file of 25,000 or more rows, two distractors in metadata.json.
(49) Independent verifier recomputes every graded figure from the bundle. (50) Two consecutive builds byte-identical.
(51) The Department's table ties to the TY2025 file (all filers) to the row and dollar. (52) The deposit ledger touches
no graded figure.

### Realism debts (stated)

1. **Filing dependents outside the designed groups sit in households under $100,000**; a real state would have some in
   every class. Forced because the stump sentence needs the stop rung to tie every published cell outside $500,000 to
   $1M, and any dependent income in another published class moves that class's AGI cell. Mitigation: visible only
   after the two-hop join, so only to a solver who already holds the answer; stated cause, working students from
   lower-income families filing to recover withholding.
2. **Income shifting is concentrated:** 34 per cent of household heads with own AGI $520,000 to $742,000 claim children
   with $30,804 to $99,500 of their own trust and investment income, and 976 households (17 per cent of the top 1 per
   cent) cross the mark on it. Forced by the top floor's 12.9 per cent shape effect over the dropped-dependent cell.
   Mitigation: the state taxes each return on its own brackets with no child-income rule, the same cause that drives
   separate filing; invisible before the join.
3. **No attached income in households of $1M or more.** Forced by the one-class miss pattern; invisible.
4. **Dependent filers are 13.2 per cent of resident returns,** about twice a national share. Forced by the count effect
   the two lower floors need (7.9 per cent). Mitigation: a low dependent filing threshold with withholding on teenage
   wages.
5. Separately filing couples are 6.2 per cent of filing units, plausible for a state that allows separate returns on
   one schedule. Two counties equal at 287 filing units above $500,000 is a coincidence of one count.
6. **Returned items are 3.5 per cent of estimated payments** (11,148 of 320,087; 2.6 per cent not paid), above a
   typical dishonour rate. Forced by the ask layer: the hazard has to move every A1 cell by more than its 1 per cent
   floor alone and in every composed subset (the nearest, with the clock, is 1.39 per cent). Added at build.

### Stopping rule (written before any round)

- **At ceiling:** two consecutive measured rounds (solver round or portal) in which a top response files $214,000 /
  $318,000 / $742,000 by attaching dependents' returns through the schedule. The household architecture is then
  measured out and the next move re-roots the graded quantity, not another rung.
- **One more repair:** a round in which every top response stops at or below the stop rung but the strongest keeps more
  than a fifth of the ask weight (repair at the device layer only); or a round in which a response lands the call by a
  route other than the two-hop link (close that route).
- **Not a trigger:** a response at rung 3 files two right floors by design.

### Portal log

(none yet)

### Determinism check

Invoked while the ladder was designed (section A walked: litmus, mechanism, flags, no ranking artifact, the 22 axes,
bins centred off the round value with the flip condition stated, pins filed once, one committed call, no planted
metric in the prompt's voice, stump sentence). Section B at stage 3, asserted in the generator (2,158 assertions):
every C1 convergence on the figure and on the row and unit counts, the C2 back-test (69 of 69 against 66, 58, 55, 3,
3 and 0), the quantile-convention corridor, every grid cell with the rule it violates and the nearest cell (7.9 and
11.5 per cent), every graded figure's distance from its rounding edge and every share's distance from its round
value, the clean-data test on the claimant-field repair, the lens-swap counts and the input gates. The independent
verifier (99 checks, 0 failed) recomputes from the shipped bytes every construction's reproduction count and floors,
the quantile conventions, the stop rung's misses and every graded figure; two builds came out byte-identical. Judge
rehearsal pending stage 6.

## Build record

Stage 3, 2026-10-09. The generator is `task120/generator/` (seed 120, every random stream keyed by name): `build.py`
writes `task120/target/` and `task120/metadata.json` and runs every assertion; `verify_pack.py` is the independent
verifier, DuckDB SQL over the shipped bytes with no generator import. From the repo root:
`python3 task120/generator/build.py` (about five minutes), then `python3 task120/generator/verify_pack.py task120/target`.
The design figures above now carry the realised values where the build moved them (listed under Changes made at build).

- **Assertions: 2,158, all holding.** m01 to m33 the main call (1,200 of them the sweep that no shipped file carries any
  floor of any construction), a34 to a47 the asks, p48, p51 and p52 the pack, h1, h9 and h16 the container, intake and
  date sweeps, with the six row-order replays. Plan items (49) and (50) are the verifier and the double build.
- **Independent verifier: 99 checks, 0 failed** on `task120/target/`: every construction's reproduction count and exact
  floors, the quantile conventions, the stop rung's 11 misses, the unit counts and the units at each floor, every A1,
  A2 and A3 figure, each share's bin, every stop off its golden, the referee, the Department's table, both antidotes,
  and no reported TIN on a listed dependent who does not file.
- **Byte-identical:** two full builds from nothing into separate scratch directories gave equal sha256 on all 25 files
  and `metadata.json`, and equal build records; the build into the task folder matches them. File times are set to
  2026-11-06 08:30.
- **Input gates:** 25 files in five formats (csv, parquet, pdf, txt, xlsx); the largest is
  `wage_statements_efile_ty2025.parquet` at 1,083,466 rows (the TY2025 return file holds 852,947); 102.4 MB in all. The
  two distractors are named in `metadata.json` and nowhere under `target/`: `returns_processed_by_agi_class_ty2025.xlsx`
  and `withholding_deposits_2025.csv`.
- **Leak preview** (leak.py on a scratch copy, so no report sits in the task folder yet): REVIEW, no LEAK; the four
  REVIEW lines are design vocabulary in the methodology, the thread, the record layouts and the prompt's opening
  sentence, for the reader's pass at the leak-check stage.

**Main call, TY2025.** 852,947 returns, 719,213 resident, 677,351 federal filing units, 582,544 household units; ranks
k = 58,255 / 29,128 / 5,826 (households) and 67,736 / 33,868 / 6,774 (filing units).

| Residency | Unit | Dependents' returns | Floor unit's AGI | Floors | Distance from the answer (10 / 5 / 1) | Cells |
|---|---|---|---|---|---|---|
| code 1 | filing unit | attached | $214,063 / $318,081 / $742,043 | $214,000 / $318,000 / $742,000 | answer | 69 |
| code 1 | filing unit | dropped | $214,063 / $318,081 / $657,057 | $214,000 / $318,000 / $657,000 | +0.0 / +0.0 / -11.5 | 55 |
| code 1 | filing unit | separate | $197,042 / $293,068 / $594,090 | $197,000 / $293,000 / $594,000 | -7.9 / -7.9 / -19.9 | 58 |
| code 1 | return | attached | $195,594 / $283,211 / $618,397 | $196,000 / $283,000 / $618,000 | -8.4 / -11.0 / -16.7 | 3 |
| code 1 | return | dropped | $195,388 / $282,266 / $592,013 | $195,000 / $282,000 / $592,000 | -8.9 / -11.3 / -20.2 | 0 |
| code 1 | return | separate | $179,405 / $261,583 / $551,318 | $179,000 / $262,000 / $551,000 | -16.4 / -17.6 / -25.7 | 3 |
| all | filing unit | attached | $194,429 / $288,579 / $640,396 | $194,000 / $289,000 / $640,000 | -9.3 / -9.1 / -13.7 | 0 |
| all | filing unit | dropped | $194,429 / $288,579 / $600,218 | $194,000 / $289,000 / $600,000 | -9.3 / -9.1 / -19.1 | 0 |
| all | filing unit | separate | $179,741 / $268,213 / $565,112 | $180,000 / $268,000 / $565,000 | -15.9 / -15.7 / -23.9 | 0 |
| all | return | attached | $178,907 / $259,351 / $573,175 | $179,000 / $259,000 / $573,000 | -16.4 / -18.6 / -22.8 | 0 |
| all | return | dropped | $178,756 / $258,646 / $559,725 | $179,000 / $259,000 / $560,000 | -16.4 / -18.6 / -24.5 | 0 |
| all | return | separate | $166,425 / $242,863 / $531,325 | $166,000 / $243,000 / $531,000 | -22.4 / -23.6 / -28.4 | 0 |
| code 1 | filing unit | income attached, returns kept | $197,042 / $293,068 / $639,318 | $197,000 / $293,000 / $639,000 | -7.9 / -7.9 / -13.9 | 66 |

- **Answer** $214,000 / $318,000 / $742,000 (rung 4); stop rung (rung 2) $197,000 / $293,000 / $594,000; rung 3
  $214,000 / $318,000 / $657,000; rung 1 $179,000 / $262,000 / $551,000; rung 0 $166,000 / $243,000 / $531,000.
- **Quantile conventions:** nearest rank at k - 1, k and k + 1, Hyndman-Fan types 1 to 9 and the midpoint round to the
  same floors under the answer and the stop rung; the spread across them is $125 / $129 / $117 at the answer and
  $138 / $155 / $176 at the stop rung, inside the $250 window on each side of every floor.
- **Nearest wrong cell:** 7.9 per cent at the 10 and 5 per cent floors (the stop rung and the double-counting partial,
  both $197,000 / $293,000) and 11.5 per cent at the top floor (dependents' returns dropped). The answer is the maximum
  cell at every floor.
- **Corpus:** households 69 of 69; the double-counting partial 66; filing units 58; dropped dependents 55; resident
  returns 3; resident returns with dependents attached 3; every other cell 0. The stop rung's 11 misses, every one short:
  $500,000 to $1M units by 23, 10 and 30 (TY2022 to TY2024), that class's AGI by 3.41, 3.11 and 3.59 per cent, and the
  county cells of Marston (071) by 4, Corwin (089) by 3, Fenwick (113) by 3, Hollowell (097) by 2 and Kessler (061) by
  14 of 301. Twin pair: 287 and 287 filing units at $500,000 or more, published 301 and 287, dependents' own returns
  3,031 and 3,001. TY2025's class shares sit nearest TY2023's table, the year of the smallest stop-rung miss.
- **World:** dependents' own returns 94,807, holding 2.019 per cent of resident AGI; trust group 1,475 households and
  2,350 returns of $30,804 to $99,500 ($171,703,020 in all), 976 households crossing $742,000, the largest household
  total $960,808; conveyor 23, 10, 30 and 30 households a year; 41,862 couples filing separate state returns;
  commuters 133,734 returns, median AGI $69,185, 899 at $500,000 or more.
- **Separation (37):** zeroing the two off-path return columns (state taxable income and the credit election) and
  reading no ask file leaves 582,544 households and the same floors; device rows and hazard rows on the main call's row
  population: 0 and 0, since every device lives in an ask file.

**Asks, golden (whole dollars).**

| Tier | Instalment 1 | Instalment 2 | Instalment 3 | Instalment 4 |
|---|---|---|---|---|
| 1 | $57,100,430 | $60,982,470 | $59,690,330 | $62,279,690 |
| 2 | $27,130,950 | $28,344,190 | $28,273,480 | $29,413,200 |
| 3 | $12,597,420 | $13,026,520 | $13,083,940 | $13,625,350 |

| Tier | Household AGI | Net capital gain | Share of AGI, exact | Share, graded | Withholding |
|---|---|---|---|---|---|
| 1 | $10,356,865,342 | $3,147,270,635 | 30.3883 | 30.4 | $135,364,253 |
| 2 | $9,837,059,854 | $995,783,766 | 10.1228 | 10.1 | $229,035,640 |
| 3 | $7,492,715,926 | $339,052,645 | 4.5251 | 4.5 | $184,720,391 |

**Stops, per cent from the golden (A2 shares in brackets).**

| Ask | S1 natural path | S2 half-handled | S3 over-cleaned | S4 filing-unit tiers |
|---|---|---|---|---|
| A1 | April +8.1 to +9.2, June -13.6 to -15.0, September +21.1 to +22.3, January +6.5 to +6.7 | April +13.5 to +13.9, June +5.9, September and January +1.6 to +1.7 | -3.3 to -3.4 every cell | tier 1 +3.0 to +3.1, tier 2 +2.4 to +3.0, tier 3 -8.9 to -9.5 |
| A2 | -8.2 / -8.7 / -10.7 (27.9 / 9.2 / 4.0) | -2.6 / -2.9 / -4.4 (29.6 / 9.8 / 4.3) | -3.2 / -3.2 / -3.4 (29.4 / 9.8 / 4.4) | +2.5 / -6.0 / -9.2 (29.7 / 8.8 / 3.9) |
| A3 | -7.5 / -7.6 / -7.9 | -1.6 / -1.6 / -1.6 | -2.3 / -2.3 / -2.3 | +10.1 / +9.3 / +7.1 |

- **Each device alone:** clock -4.57 to -5.38 (April), -19.01 to -20.68 (June), +19.07 to +20.45 (September), +4.72 to
  +4.95 (January); transfers +11.90 to +12.13 (April) and +4.24 to +4.29 (June), nothing elsewhere; returned items
  +3.21 to +3.39 every cell; register -1.58 to -1.60 every A1 cell and -1.56 to -1.57 every A3 tier; versions -5.60 /
  -5.80 / -6.30; loss limit -2.60 / -2.90 / -4.42; paper channel -5.99 / -6.11 / -6.45.
- **Composed subsets:** the nearest any mishandled figure comes to its golden is 1.39 per cent on A1 (clock and returned
  items, tier 1 April), 2.60 per cent on A2 (the loss limit alone, tier 1) and 1.56 per cent on A3 (the register alone,
  tier 3); every A2 share under every subset rounds off the golden share.
- **Device sizes:** 11,148 returned items on 320,087 estimated payments (8,330 not paid); 25,771 TIN match cases (21,493
  resolved, 4,278 open; 20,876 on wage statements, 4,895 on payments); 13,035 transfers citing a TY2024 return and 11,022
  citing a payment; 73,102 paper statements carrying 6.29 per cent of withholding beside 1,083,466 e-filed; a Schedule D
  extract of 159,450 rows and an amended-return log of 57,896 rows on 27,664 returns.

**Changes made at build** (each also has its line under Tried and rejected where an approach died).

12. **Rung and grid figures realised:** rung 0 $166,000 / $243,000 / $531,000 and rung 1 $179,000 / $262,000 / $551,000
    (designed $168,000 / $243,000 / $520,000 and $179,000 / $265,000 / $562,000); the double-counting partial $639,000
    at the top floor (designed $613,000); no all-filer construction reproduces any of the 69 cells, because every
    appendix county holds a part-year resident at $500,000 or more.
13. **Trust children's returns run $30,804 to $99,500** (designed up to $130,000), so under filing units a trust
    child's own return never enters a published class and every class outside $500,000 to $1M still ties.
14. **The dependents schedule ships every claimed dependent:** 466,638 rows in TY2025 (designed about 420,000).
15. **Commuters** median $69,185 with 0.67 per cent at $500,000 or more (designed about $72,000 and 1 per cent).
16. **The appendix counties** are the twelve with the most full-year resident returns in TY2024, at least 15 per cent
    clear of the thirteenth (asserted), so the appendix's "twelve largest counties" reads one way.
17. **The TIN register ships as `tin_match_cases.csv`.**
18. **Stops against the ask sheet:** A1's natural path moves June by -13.6 to -15.0 and September by +21.1 to +22.3 per
    cent (the sheet expected cells other than April within -4 to +6), because 15 June 2025 is a Sunday and receipts on
    the rolled due date fall to September under a calendar-date reading; returned items run +3.2 to +3.4 per cent a cell
    (sheet +1.5 to +3), A3's over-cleaner -2.3 (sheet -0.5 to -2) and A2's loss limit -4.4 on tier 3 (sheet -1 to -4).
    Every stop clears its floor: 1 per cent a figure, 4 per cent and 0.3 share points on A2's natural path, 3 per cent on
    A3's.
19. **Realism debt 6 added** (returned items at 3.5 per cent of estimated payments, under Realism debts).

## Write-up and ship checks (stage 3)

- **Golden.** `task120/generator/golden.py` reads only `target/` (DuckDB over the shipped bytes) and writes
  `task120/golden/tier_schedule.xlsx` (sheets Schedule, Reproduction, Tier base 2025, Notes) and
  `task120/golden/tier_floors.png`; run from the repo root as `python3 task120/generator/golden.py` (about a minute). It
  asserts every graded figure against the Build record and reads the workbook's graded cells back after writing. Printed:
  floors $214,000 / $318,000 / $742,000 (k-th household AGI $214,063 / $318,081 / $742,043), 582,544 household units,
  69 of 69 cells, and the tier base exactly as in the Build record's asks tables.
- **Submission.** `task120/submission.md`, five blocks. Block 2's counts (41,862 couples recombined, 94,807 dependents'
  returns attached) recompute from the TY2025 return and schedule files; block 1's rival clauses were checked on the
  bytes (resident returns match only the three totals; filing units miss the $500,000 to $1M class all three years and
  five counties; dropping dependents' returns misses all three totals).
- **golden-realism**, run after the figures froze: chart floor labels moved above the plot (the 10 and 5 per cent
  labels collided), band labels shortened with a key in the subtitle (tier 3's band is too narrow for a three-line
  label), the subtitle's unit count taken from the data; workbook header alignment by column type, Basis labels
  top-aligned, column A widened, every sheet fitted to one page wide (Reproduction and Notes had split across pages).
  Both files rendered and read. Figures unchanged on the re-run.
- **reduce-house-fixes register.** H1: golden container carries the Office of Revenue Research and 9 November 2026
  (the as-of date), no writer signature; the scrub audit is clean on `golden/` (band 2026-10-23 to 2026-11-09) and on
  `target/`. H2 and H3: every figure in the submission is printed or asserted by `golden.py` or `verify_pack.py`; the
  workbook's and chart's prose is built from the same variables as their figures. Thinnest margin on file: the
  quantile-convention spread of $129 at the 5 per cent floor against the $250 window either side of it. H4: `golden/`
  holds exactly the two files the prompt names (sha256 prefixes: tier_floors.png dfec0216b3411fb6,
  tier_schedule.xlsx a28fd97fca202b7f). H6: the golden's stated rules back-test on the record with zero mispredictions:
  tier membership by adopted floor (units at or above each floor equal k), the household's county as its primary
  filer's (all twelve appendix counties reproduce), the version of record (0 accepted-version AGI mismatches), the
  credit-election transfer rule (0 transfers off their TY2024 election). H7: two builds of the golden byte-identical.
  H8: every citation resolves (methodology s.2, s.3, s.4; record layouts s.3; every file name is in the pack). H11: one
  `submission.md`, one `prompt.md` in the tree. H16: no date in either golden after 9 November 2026. `verify_pack.py`
  after the pass: 99 checks, 0 failed.
- **Surface** (`guard.py surface task120`): 0 promoted pairs; nearest neighbour task72 at 0.101 (97th percentile),
  proximity only.
- **Heart** (`guard.py heart task120`): WARN, no BLOCK. Nearest heart text 0.06 (task109's driver, differentiated on
  the card). WARN `repeat.gate_g` against task123 (method_or_model_selection in one of the last two builds): answered,
  the mechanism is the same label on a different move (here a unit built through a roster link, selected by exact
  reproduction), and the batch's other furniture differs; the card's driver_concrete was refreshed to build scale and
  its answer, answer_source, spine and deliverables filled.
- **Stage 3 re-run, 2026-10-09 (after harden loop 1).** The pack was not rebuilt: harden loop 1 found no repair
  inside the driver, so `generator/` (other than `golden.py`), `target/` and `metadata.json` are as they passed stage 3
  and solver round 1's landing applies to this pack unchanged. `golden.py` now also asserts against the record and
  prints the two counts block 2 owes beyond the schedule (41,862 couples recombined on the federal primary TIN, 94,807
  dependents' returns attached); the outputs are byte-identical to the first stage 3 (tier_floors.png dfec0216b3411fb6,
  tier_schedule.xlsx a28fd97fca202b7f), so the golden-realism pass stands and both files were re-read (chart labels
  clear, workbook sheets Schedule, Reproduction, Tier base 2025, Notes as filed). `submission.md` is unchanged: every
  figure in it is printed by `golden.py`. `verify_pack.py`: 99 checks, 0 failed. Metadata audit clean on `golden/` (band
  2026-10-23 to 2026-11-09) and on `target/` (no signature; its in-fiction dates are the tables' and the methodology's
  publication dates). One `submission.md` and one `prompt.md` in the tree, no em dash in any written file. leak.py:
  REVIEW, no LEAK, the same nine REVIEW lines answered under Leak review. Surface: 0 promoted pairs, nearest task72 at
  0.101 (97th percentile), proximity only. Heart: **PASS** (nearest heart text 0.05, task109; the earlier
  `repeat.gate_g` WARN no longer fires); card fields (answer, answer_source, spine.rows 852,947, deliverables,
  opening_move) already match the submission and the pack; `guard.py validate` 119 cards, 0 invalid.

## Leak review

leak.py, as of 2026-11-09: REVIEW, no LEAK. One line per REVIEW line.
- `household_income_tables_ty2022.xlsx`, 500,000: a published class boundary ($500,000 under $1,000,000), not an answer; it reaches the sweep only through block 1's rival clause.
- `household_income_tables_ty2023.xlsx`, 500,000: the same class boundary.
- `household_income_tables_ty2024.xlsx`, 500,000: the same class boundary, plus the Appendix A threshold the tables publish.
- `returns_processed_by_agi_class_ty2025.xlsx`, 500,000: the Department's own class boundary on the distractor table; it carries no floor.
- `income_tax_tier_methodology.pdf`, 8 of 9 words of the committed call: that is pin P1 (full-year resident household units, the 10, 5 and 1 per cent marks, the nearest $1,000), stated once as determinism requires; it carries no floor and does not say what a household holds.
- `income_tax_tier_methodology.pdf`, 11 stump terms: the pins' own vocabulary (household, federal, filing, construction); the filing-unit basis is attributed to the Legislative Fiscal Office and the dependents' link is not named.
- `re_ty2025_tier_rebase.txt`, 4 stump terms: the delivery note lists the files it delivers (returns, the dependents schedule); no sentence points at attaching them.
- `research_extract_record_layouts.txt`, 12 stump terms: field semantics only; the schedule is described as dependents claimed for the exemption credit and the dependent's return carries no claimant field, which is the design.
- `prompt.md`, opening sentence with two stump terms ("returns", "income-tax"): the evidence-first opening names the processed-return year, the forcing fact; it fixes no unit, population or basis.
- Re-run at the stage 3 re-run (2026-10-09, as of 2026-11-09): REVIEW, no LEAK, the same nine lines on unchanged files, each answered above.

## Harden loop 1

Solver round 1 (plain, proxy 96.8, 2026-10-09; graded output in `task120/solver_rounds/round-1-plain.md`)
landed the call at its step 2 and kept every ask item but one chart label. The loop was worked on paper against
the registered driver before any generator change, as the hardening loop directs: a rung after which the solver's
step still completes and still returns a wrong answer, from the measured catalogue first, and never a louder pin,
a planted defect or a second decoy.

**Diagnosis.** The corpus-direction line kept a corpus that refutes the stop rung (58 of 69, every miss short in
one class) on the record of measured traps #1 and #3. Those traps stump when the construction that reproduces
every control is one the solver fails to find. Here it is the household's other link, the dependents schedule,
so the refutation tells the solver where to look and the look is one join. The registered driver is that
structure, and stumping Part 4 lists it as dead (a corpus built to refute the naive read is quoted back as the
evidence for the rung it hides).

**Every repair the skills direct, worked against this driver** (one line each under Tried and rejected):
1. A corpus blind to the attachment, so the filing unit reproduces every cell and returns the wrong floors.
   Buildable, since every attachment into a household of $100,000 or more in the closed years is a designed one,
   but the household then rests on a sentence that is either missing (Gate C) or executed (Part 4, a filed
   formula).
2. Households as the confirmed stop rung, with a decisive move only TY2025 carries. No TY2025-only structure in
   this world is at once silent on the battery, unfiled, and a construction rather than an instrument repair.
3. A harder household behind the same refuting corpus. Every extra membership rule is a filter or a join over
   shipped columns, inside the search the refutation starts.

The escalation list (stumping Part 10) adds nothing here: the discriminator already sits behind a join, there is
no filed pin to split, an advocate for the runner-up is a second decoy to a solver that test-benches, and the
corpus is the leak rather than too weak.

**Ask layer.** Every device was cleared because its rule sat in the ask's own layout or governing section, or a
control total confirmed it. The fresh-device redesign is not built: while the call is landed, two responses bank
about 45 each before any ask, and no ask layer brings that pair under 40.

**Disposition: re-root recommended, no rebuild.** Nothing in the generator, `target/`, `golden/` or
`submission.md` changed, and the build stands as it passed stage 3. The stopping rule asks for a second
consecutive landing through the schedule before the household architecture is called measured out; that round
is not run, because no repair exists to put in front of it and the unchanged pack falls to the same step. The
next move is the stopping rule's own: re-root the graded quantity at stage 1, a new draw through checkpoint A,
with this architecture moved into the card's lineage. The re-draw can carry the world and its tables, whose
class-by-class balance can certify households outright (the L1 form) if the new call puts its decisive move
where the tables cannot see, and the ask-layer finding above.

## Re-root v2: DRAW

Drawn 2026-10-09 at stage 1, after solver round 1 (plain, 96.8) and harden loop 1, which closed every repair inside the
v1 driver. The v1 sections above stay as the record of the architecture that died; the card moves it into `lineage`.
Nothing in the generator, `target/`, `golden/` or `submission.md` changes at this stage, and no ladder is designed
until the author answers at checkpoint A.

```
DRAW  (re-root v2, independent draws, checked with .claude/skills/fingerprint/guard.py)
  Card filed: pending re-registration (candidate card checked in the scratchpad, not registered; the author registers after checkpoint A)
  Verdict: BLOCK on one rule (test.same_driver inside the window, see Guard); no WARN
  Shape: 14 cuts of a distribution   Gate G mechanism: binding_constraint
  Gap: objective (decisive), time   Pattern: none of A to E; G11 (a per-return loss limit that does not commute with the
       joint return) over G13 (the TY2026 regime no closed year reached)
  Domain: Economics   Subdomain (enumerated): public-finance   Objective: Descriptive & Distribution Analysis
  Pairing repeated from the last three builds? no (task119 Policy & Education x Anomaly Detection, task121 Product
       Analytics x Root-Cause, task122 Product Analytics x Experiment & Causal)
  Stakeholder role: director of the state's nonpartisan revenue research office, which staffs the Revenue Estimating
       Conference (statistical_office_head), kept from v1
  Context-artifact type: published_series (the Department's Returns Processed by AGI Class), kept
  Calibration form: certified_matrix (the Household Income Tables for TY2022 to TY2024, 69 cells), kept as the organ and
       turned round: it now certifies the stop rung instead of refuting it
  Decision type: dial_setting (three AGI floors for the top 10, 5 and 1 per cent of full-year resident household units on
       the TY2026 current-law base, each to the nearest $1,000)
  Decisive mechanism: the 2026 session's flat-rate restructuring repeals the married-filing-separately state return from
       TY2026, so a couple filing a joint federal return files one joint state return starting from that return's federal
       AGI, and the conference strikes its TY2026 estimate on TY2025 returns as that law computes them; on a TY2025
       separate return a spouse's net capital loss counted only to $1,500 and a passive loss only against that spouse's own
       passive income, so a couple whose separate returns held such a loss beside the other spouse's gains carries less AGI
       on the joint return than the sum of its filed returns, a class no column marks
  Generators: G11, G13   Answer unit: currency (USD)
  Forum: minister_or_cabinet (the state finance secretary adopts the re-based floors on the office recommendation), kept
  Forcing event: statutory_or_regulatory_filing (the conference certifies the TY2026 income-tax estimate under statute), kept
  Organisation family: research_or_statistics_office, kept
  Spine: TY2025 processed-return file, return grain, synthetic, 852,947 rows at the v1 scale (set at build)
  World: United States, a fictional state with invented counties (Kessler, Abington); USD; kept
  People (guard.py names --geo "United States" --seed 120 still draws all four): Stephanie Reid (requester), Manuel
       Stevenson, Brittany Shepard, Jeffrey King, kept; their lines are rewritten at design
  Deliverables: ty2026_tier_schedule.xlsx, ty2026_tier_floors.png   Opening move: calendar-first
  Prompt shape arithmetic: the three committed floors (3), household units and AGI in each tier (6), households above the
       top floor in each of the twelve appendix counties (12), four named chart parts and two files (6): about 27 before
       the ask sheet, which supplemental-stumping sizes
  As-of date: 2026-11-09
```

**Similarity claim.** No build on file cuts a distribution on a forward law's base where a limit that sat on each
member's record stops applying when two records become one. task58 v15 applies a floor at the sub-unit grain after a
split (the opposite direction), task64 v4 lets a filed capacity bind for the first time against a forward book, and
task114 (inside the window) merges two sites so that demand appears; here the merger removes AGI through the grain of
a loss limit, and where the parties are plays no part.

**Stump sentence.** A competent solver builds household units (all 69 published cells reproduce), reads the TY2026
repeal of the separate state return as the pairing of spouses its households already perform, and files the summed
TY2025 household floors as the TY2026 current-law schedule (in the v1 pack, $214,000 / $318,000 / $742,000), because the
joint return nets a loss one spouse's separate return could only limit or suspend (capital or passive) against the other
spouse's income of the same kind before one limit applies, so the couples holding such a loss carry less AGI under the
law the estimate is struck on and the top floors fall.

**Litmus and Gate G line.** No number in the pack is wrong and no reading is overturned: the filed returns, the
published tables and the Department's table are right about what they record, and the summed household AGI is the
correct TY2025 figure. The difficulty is a limit whose grain the forward law changes. surface_read_dependency: no;
stumping_family: analytical_non_defect; sole_data_defect: no (no file is incomplete, and no instrument could have recorded the
joint return the answer needs, because TY2025 had none). Lens-swap test: the naive read is the households' AGI under the regime
their returns were filed under, the answer the same households under the regime the estimate is struck on, and the two
differ only where a per-return limit bound; this is the line Gate G will test hardest (see Concerns).

**Decisive rung.** Measured trap #13, validates on one population, applies to another: decided 3 of the client's 64
tasks, 2 of them under 0.50 (established). The summed household AGI is validated on every closed separate-return year
(69 of 69) and applied to the joint-return base. Behind it, #7 uses the ready-made measure (5 of 64, 2 under 0.50): each
separate return's reported federal AGI, summed, in place of the AGI the joint return defines. Corpus direction: the
tables reproduce under the naive path, because every published cell was struck on filed returns. L1 sentence: in every
published cell the joint netting is absent, because no couple's separate returns were ever combined before TY2026; the
compulsory joint return first combines them in the year the estimate is struck on.

**Ladder sketch.**
- Rung 0, every return a unit: ties the Department's all-filer table; killed by the residency code list and the tables.
- Rung 1, full-year residents with each return a unit: the methodology's population; the tables refute it (3 of 69).
- Rung 2, federal filing units: the textbook tax unit; the tables refute it (short in one class).
- Rung 3, household units (filing units plus the dependents' own returns): 69 of 69, the construction the tables
  certify, given away on purpose (L1).
- Rung 4, the stop: households on the TY2026 base with AGI summed from the filed returns; the repeal reads as the
  pairing households already perform and 69 of 69 confirms it. Killed only by the per-return limits in the Schedule D
  and passive-loss detail, which net on the joint return.
- Rung 5, the partial: capital losses re-netted under the joint limit, passive losses left on their returns; lands
  between the stop rung and the answer, so it is priced as a wrong cell rather than a farther one.
- Rung 6, decisive: every per-return-limited loss netted across the couple under one limit. The answer is the lowest
  cell of the grid (L5).

**Nearest exemplars.**
- **0.34**, Nonprofit & Grant-making, Capital Grant Drawdown Forecasting: every one of 1,632 paid certificates falls on
  its scheduled date, and the schedule is stale for the unpaid stages the forecast runs on (#13: the closed record
  certifies a basis the forward set breaks).
- **0.39**, Nonprofit & Grant-making, CDFI Award Compliance: the single-family posting lag that fits the ledger, applied
  to commercial draws (#13).

Same-domain neighbour, for voice: 0.41, Economics, Treasury Cash Flow Forecasting (#7, the ready-made QA scorecard
over the certified loss).

**Guard.** BLOCK on one rule against the existing corpus (last three task119, task121, task122; window of twelve from
task111), nearest driver at 0.05.
- `test.same_driver` inside the window: (objective, G11, binding_constraint) against task122's v1 lineage, a draft drawn
  2026-10-08, redrawn at checkpoint A and never registered (a pick under filed conditions with a library fallback). It
  is not differentiable inside the window, and no honest relabel exists: every cap build on file records its gap
  objective-first under G11, and the decisive miss here is the limit, not the date. Registering needs the author's
  `--force` with that reason, or a redraw.
- `test.same_driver_older` and `test.same_puzzle_older`: the signature is the non-commuting-cap family in 13 older
  builds (task32, task36, task37, task43, task50, task57, task58, task64, task73, task76, task79, task87, task106); each
  carries a differentiation line on the card, and task114 carries one although the guard did not ask for it. Reusing
  the device is legitimate; the driver differs from each.
- No WARN. The split-residency variant (the out-of-state spouse the joint return brings in, time over population, G4)
  passes clean and is rejected under Tried and rejected.

**What changes from v1.**
1. Graded quantity: the TY2025 floors become the floors on the TY2026 current-law base.
2. The household construction falls from the decisive rung to a shallow rung the tables certify, so the reproduction
   clause becomes a certification and the corpus confirms the stop rung; round 1's search signal is gone.
3. Decisive move: per-return loss limits that the joint return nets across spouses (objective over time, G11 and G13,
   binding_constraint), where v1's was the household unit (population, G2 gated by B, method_or_model_selection).
4. Kept: world, people, forum, forcing event, organisation family, role, context artifact, calibration organ, shape 14.
5. Deliverables renamed for TY2026; opening move calendar-first (v1's was evidence-first).
6. Ask layer rebuilt at design so that no device's rule sits in the ask's own layout or governing section and no
   control total confirms it (the harden-loop finding).

**What changes from the source note.** The note's decision (the conference's top-tier floors) and its world stay. Its
decisive rung (S1 gated by Pattern B) becomes a certified shallow rung, its committed call moves from the TY2025
schedule to the TY2026 current-law schedule, and the repeal of the separate state return is added: the note's
"two-earner couples file separate state returns" is the practice the repeal ends. The reproduction clause turns from a
gate the stop rung fails into a certification it passes.

**Concerns for checkpoint A.**
- The household-tier world is close to exhausted for a Descriptive call under the four standing rules. Harden loop 1
  closed every TY2025 move, the forward-population and completeness moves are on the dead list, and the joint-return
  base is the one place the tables cannot see; its honest signature is the non-commuting-cap family.
- Stump power: a tax-literate solver that builds each joint return from its items, rather than summing the filed AGIs,
  lands the answer. Determinism needs the layouts to say that a separate return's AGI is figured as on a federal
  married-filing-separately return, and that sentence is the question the stump depends on nobody asking.
- Separation: at realistic shares of couples holding a limited or suspended loss beside the other spouse's gains, the
  top floor moves a few per cent; a wider gap needs a stranded-loss class large enough to be realism debt.
- Gate G: the answer recomputes the same households under the forward law, close to the lens-swap line.
- Every Descriptive exemplar under 0.25 is the reproduction-gated hidden unit, which the rule against a refuting corpus
  removes, so a world redraw carries the same constraint. The realistic alternatives are a world whose L1 corpus covers
  only segments without the decisive property (task71's form), or a Forecasting retag of this decision; either needs
  the author's word.

## Retired

The author retired this build on 2026-10-09 after solver round 1 (plain, 96.8, landed at step 2) and a re-root draw that could not carry a strong stump under the standing rules. It is not submitted. The v1 pack, goldens and submission stay as the record of what was built and solved.

## Tried and rejected
- Twin pair at 117 against 58 (2.02x, the source note's form): dropped because the stop rung would miss Kessler by 50 per cent, which breaks "every miss a few per cent short" and makes the corpus a loud alarm; there is no lookup transfer to kill in this build, so the pair only needs a nonzero gap in an exact count.
- Trust group with own AGI $620,000 to $740,000 and $30,000 to $90,000 a return (the source note's figures): the feasibility model needs about 976 crossers into the top 1 per cent, which would be about 98 per cent of the household heads in that band; widened to $520,000 to $742,000 and up to $130,000 a return (34 per cent).
- Asks A and B as written (24 withholding wage-months, 12 instalment cells for TY2022 to TY2024): both fail H18, figures for other periods a person could act on with the schedule unmade.
- Ask C as written (three floors under each of four named constructions): names the rungs, which hands the ladder over.
- "The closest reading that does not stand" as an ask (the exemplar's form): not determinate here, because by cells reproduced the closest rival is the double-counting partial (income attached with dependents kept as units, 66 of 69), not the filing-unit stop rung (58).
- A per-instalment count of paying households beside the receipts: the unit of the count forks (payers against household units), and naming the unit in the prompt would fix the population.
- The full-scale state (3,412,000 returns a year): with four years of returns and schedules shipping for the corpus, the pack would run to several hundred megabytes; scaled to 852,947.
- Publishing AGI cells only for the top classes so dependents could sit realistically in the middle classes: it changes the 69-cell corpus the stump sentence is written on; the middle-class concentration is carried as realism debt 1 instead.
- Commuter incomes spread to $400,000 (median about $105,000): the all-filer household cell's 10 per cent floor landed 0.3 per cent from the answer's; commuters moved below the floors (median about $72,000).
- Trust group drawn by random tuning of households and children (build): the search reached 885 crossers of $742,000 against the 976 the top floor needs; replaced by an allocation that picks the 976 crossers first and gives the other 499 households children that leave them under the mark.
- Trust children's returns up to $130,000 (the design's range): under filing units a child's own return of $100,000 or more is a unit in the $100,000 to $200,000 class, which breaks the stop rung's tie on every class outside $500,000 to $1M; capped at $99,500.
- Abington's comparable dependents claimed by households anywhere under $500,000: the attached income could carry a claimant to the class top (the generator stopped on it), which would hand Abington a crosser the twin pair does not allow; the claimants sit under $440,000.
- Filing dependents drawn from the first household composition (fewer, younger children): only 77,314 of the 91,281 needed in a year could be placed; child ages now run 0 to 26 on a smooth profile with a Poisson(0.9) child count, child and head-of-household rates are higher at low incomes, and each year has its own target.
- Twin pair equalised by moving one separately filing couple between Kessler and Abington: after the year factors were retuned no couple fitted and the build stopped ("no couple to adjust"); the equaliser now has four moves, in both directions.
- Commuter AGI with a long tail: the all-filer household cell sat 6.7 / 7.8 / 6.9 per cent below the answer, nearer than the designed nearest cell at the top floor (11.5 per cent); with the tail cut to 0.68 per cent of commuters (Pareto shape 3.4) and the median at $69,000 it sits 9.3 / 9.1 / 13.7 per cent below.
- Prior-year trust groups at the first planned sizes (1,391, 1,342 and 1,436 households): the own-AGI band seated only 1,262, 1,224 and 1,317 in the lower-income prior years, and the group size is what sets the stop rung's $500,000 to $1M AGI miss; resized to 1,066, 1,163 and 1,552 so the misses land at 3.41, 3.11 and 3.59 per cent.
- Prior-year tables left to coincidence: some return-grain constructions tied a published class or county cell by chance (separate spouses moving in and out of a class netting to zero), which moved their hit counts off 3 and 0; such ties are broken by moving one couple's split share (return-grain cells only), and every appendix county holds a part-year resident at $500,000 or more so no all-filer construction ties a county cell.
- Rival cells' floors left where they fell: six grid cells' floors sat within $53 of a half-thousand rounding edge (two of them $3 away), so quantile conventions could round them two ways; unit AGIs within $70 of such an edge are moved out of the window, and every cell's floor is asserted at least $70 from an edge under every convention.
- First prior-year income factors (0.952, 0.981 and 1.043): TY2025's class shares sat nearest TY2024's table, the year of the largest stop-rung miss, instead of TY2023's; retuned to 0.948, 0.992 and 1.061.
- Ask devices drawn as one share of all rows: the transfers alone moved April by 56 to 57 per cent and the loss limit moved tier 3 by 34 per cent, while composed mishandlings cancelled to within 0.24 to 0.58 per cent of a golden cell; every device, the credit elections included, is now drawn per tier and instalment cell to its own target, and the worst composed subset is 1.39 per cent.
- The first estimated-payment participation curve: under filing-unit tiers (stop S4) tier 2's receipts came within 0.4 to 1.6 per cent of the golden; the curve now rises through 0.25 at $200,000, 0.33 at $260,000 and 0.47 at $300,000, and S4 moves tier 2 by 2.4 to 3.0 per cent.
- A paper channel carrying about 1 per cent of withholding: A3's natural path (e-file only, no register) landed 2.3 to 2.5 per cent from the golden, under the ask sheet's 3 per cent floor; the channel was enlarged to 6.29 per cent of withholding and the natural path now lands 7.5 to 7.9 per cent off.
- Realism defects in the first full build, each fixed: TY2025 original returns received in December 2025 (e-filing now opens 21 January 2026), capital losses piled at exactly -$600 (random floors now), register cases opened before the payment they cite, deposits dated on weekends, TY2024 ledger rows dated in December 2024 (outside the ledger's stated window), accepted amendment dispositions after the extract (all now by 15 August 2026), and the reconciliation summary's all-channel employer count summed across channels (now distinct employers).
- Parquet with byte_stream_split on integer columns (to shrink the return files): DuckDB refuses it ("BYTE_STREAM_SPLIT encoding is only supported for FLOAT or DOUBLE data"), so a solver's likeliest engine could not read the spine; dropped, the bundle is 102.4 MB, and the build asserts that DuckDB and pyarrow agree on every Parquet file's row count.
- The TIN register named tin_resolution_register.csv: leak.py read "solution" inside "resolution" as author vocabulary (LEAK); renamed tin_match_cases.csv, with the record layouts, the thread and the verifier following.
- Tier 2's capital-gain share of AGI at 10.10005 per cent (within 0.0001 points of the round one-decimal value, the receipt determinism-check A.6 names): tier 2's gains carry a 1.0023 tilt in the generator (share 10.1228), and every share is asserted at least 0.01 points from its round value and 0.02 points from its rounding edge.
- Misreported TINs drawn clear of TY2025 filers and spouses only: 10 landed on dependents listed on a schedule who do not file (3 e-filed statements kept such a dependent as their owner after the register), so attaching records through the schedule would have moved A3 off the filer-and-spouse resolution; a misreported TIN now avoids every TIN in the files, asserted in the generator and the verifier.
- Stop rung at federal filing units (rung 2) held by its 58-of-69 fit, as built (solver round 1, plain, 96.8, main call landed, 8 of 9 asks): the solver used the reproduction clause as a test bench, saw the federal unit fall short ("federal units (filer_tin grouped with federal_primary_tin) matched 17/19") and went straight to "Federal units plus each dependent's own return, joined through dependents_schedule dependent_tin = filer_tin (union-find), matched 19/19 in every year", so the corpus that refutes the stop rung (the alarm the corpus-direction line kept) works as a search signal and the dependents schedule is the next table on the bench; rung 3 was never visited, and every ask device (Sunday roll to 16 June, returned items, misapplied transfers, TY2024 credits, latest accepted amendment, paper W-2s) was cleared.
- Harden loop 1, diagnosis of round 1 (the corpus-direction line's decision to keep a corpus that refutes the stop rung, on the record of measured traps #1 and #3): those recipes stump only when the reproducing construction is one the solver fails to find, and here it is the household's own second link, so the refutation is a search signal with a one-step search, in the solver's words "federal units (filer_tin grouped with federal_primary_tin) matched 17/19. Federal units plus each dependent's own return, joined through dependents_schedule dependent_tin = filer_tin (union-find), matched 19/19 in every year"; that is the shape stumping Part 4 lists as dead (a corpus built to refute the naive read is quoted back as the evidence for the rung it hides), and the registered driver ("grouping on the visible key alone reproduces most cells ... only the full grouping reproduces all of them") is that shape, so no magnitude, threshold or wording change inside the driver repairs it.
- Harden loop 1, repair on paper, the corpus made blind to the attachment so federal filing units reproduce every published cell and still return $197,000 / $293,000 / $594,000 (the brief's form, and stumping L1's): buildable, because every attachment into a household of $100,000 or more in TY2022 to TY2024 comes from the designed groups (1,915, 1,544 and 2,690 households, crossings exactly the conveyor's 23, 10 and 30 a boundary), so dropping the prior-year trust groups and the conveyor's crossings ties all 69 cells under both units; but then two constructions reproduce 69 of 69 and the methodology already reads "The Legislative Fiscal Office draws its household tiers on federal filing units", which licenses the filing unit as a household reading, so households need an added sentence (a claimed dependent is a member of the claimant's household); unstated the floors are underspecified (Gate C), stated it defines the graded quantity's unit in the layouts or the methodology, which round 1's solver read at its step 1, and it is stumping Part 4's dead shape (a committed figure that is the output of a filed formula: unstated fails Gate C, stated hands it over). Dead.
- Harden loop 1, repair on paper, households kept as the corpus-confirmed stop rung with a decisive move above them that only TY2025 carries (a corpus blind to the decisive move for a structural reason): every structure this world can hold in TY2025 alone either surfaces on the habitual battery or as a year-on-year step (a dependent TIN on two schedules under a split credit, against the layouts' "The Department accepts one claim for a dependent TIN in a tax year"; households mixing residency codes, which the solver checked in its own words, "no unit mixes residencies"; a narrower TY2025 schedule or new code values; separate returns reporting the couple's joint AGI), or has to be filed and is then executed (a dependent-income threshold for membership, a co-residence rule for code 05 parents), or is a completeness or identifier repair the judge's instrument test bans (returns held in process at the extract, a second schedule channel, an ITIN converted to an SSN, non-filing households counted in the base). Dead.
- Harden loop 1, repair on paper, a harder household behind the same refuting corpus (attach-all scoring below the filing unit, with membership by relationship code, by the dependent's county against the claimant's, or a subfamily split needed for 69 of 69): each added rule is a filter or a join over columns the schedule and the return already carry, which is the next search a solver runs on a refutation, so the corpus stays the search signal round 1 used. Dead.
- Harden loop 1, diagnosis of the ask layer (D8 clock, D2 version of record, D4 paper channel, hazards H1 to H4): every device's rule sat in the ask's own record layout or governing section, or a control total confirmed it, and the solver executed each in its own words: "Both channels tie to the employer reconciliations ($1,394,690,352 + $93,587,882)" (the referee confirmed the paper channel the layouts' section 8 names instead of arbitrating a disagreement), "UTC was converted to Central time and compared against due dates of 2025-04-15, 2025-06-16 (June 15 is a Sunday)" (layouts section 3), "the latest ACCEPTED amended version's AGI equals the processed AGI on all 27,664 amended returns. Capital gain uses amount_in_agi from the version of record" (layouts sections 6 and 7, methodology s.4), "I excluded the 13,035 overpayment-credit transfers ... I removed 11,148 returned items unless they were re-presented PAID" (methodology s.4, layouts section 4), "plus RESOLVED WAGE_STATEMENT TIN cases" (layouts section 5). Dead at this layer: a device whose rule sits in the ask's own layout or governing section, a channel with its own control total, and a hazard resolved by a register the layouts describe; and no ask layer rescues the pair while the call is landed, since two responses on the call bank about 45 each before any ask.
- Re-root at stage 1, the v1 architecture retired (household units as the decisive rung, gated by the 69-cell reproduction clause): solver round 1 (plain, 96.8) landed it at its step 2 by reproducing the published tables, in its words "federal units (filer_tin grouped with federal_primary_tin) matched 17/19. Federal units plus each dependent's own return, joined through dependents_schedule dependent_tin = filer_tin (union-find), matched 19/19 in every year"; a corpus that refutes the stop rung is a search signal and the reproducing construction sat one join away, so the architecture moves to the card's lineage and v2 keeps households only as a certified shallow rung.
- Re-root candidate, the out-of-state spouse the TY2026 joint return brings into a resident household (split-residency couples) as the decisive rung: guard-clean (time over population, G4), but the class is one group-by on federal_primary_tin and residency_code, which round 1's solver already ran ("no unit mixes residencies"), and the joint-return clause names the move.
- Re-root candidate, a forward roll of the TY2025 households into the TY2026 population (2026 departures, 2025 part-year arrivals, dependents ageing out): stumping Part 4's dead "forward population named by a filed clause" (task100 v1), with every limb on a register, a residency code or a birth year.
- Re-root candidate, completing an earlier TY2025 extract for the returns still to come (extension filers, top-heavy): the judge's instrument repair, and Part 4's "recovery of what an instrument could not observe".
- Re-root candidate, floors for the top 10, 5 and 1 per cent of residents rather than of household units (person-weighted): a lens swap on the same households at the same moment (single_conceptual_flip).
- Re-root candidate, holding the TY2024 schedule while the TY2025 floors sit inside a revision band: a figure computed to see which side of a line it falls (stumping Part 2's exhausted shape), with its rule filed and so executed.
- Re-root label, the joint-return netting recorded time-first (time, G13) to clear the in-window collision with task122's v1 draft: a relabel, because every cap build on file is recorded objective-first under G11 and the decisive miss is the limit.
- 2026-10-09, re-root v2 (TY2026 current-law floors, joint-return loss netting across spouses) drafted and not built: test.same_driver blocked it on (objective, G11, binding_constraint), a tax-literate solver who rebuilds the joint return from its items lands it, and the effect on the top floor is a few per cent. The author retired DA01 rather than force it; DA11 takes the Descriptive slot in a later wave.
