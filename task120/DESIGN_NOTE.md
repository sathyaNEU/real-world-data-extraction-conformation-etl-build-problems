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

Proven-in-production checks (stumping Part 6.1). Dead shapes (Part 4): no match; the nearest is a corpus built to refute the naive read, because the tables refute the return grain (3 of 69) and the federal-filing-unit grain (58 of 69, misses one-sided), which is the bet the measured catalogue's #1 and #3 take. Discriminators: the two units disagree in shape at the top and not only in level (the children's trust income carries 3,900 households past the top-1% mark); membership is computed through a join and never a column; the construction has no menu. L5 (the answer is the extreme cell of the grid) and L8 (every construction is a complete partition, so every total ties) are met. L1 is not (the corpus pins the decisive rung instead of being blind to it), and L3 only in part (the literature's partial, dropping dependent filers, lands at $657,000, -11.5 per cent, nearer than rung 2).

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
class's AGI and dependents' returns hold 2.00 per cent of resident AGI.

### Changes made at design (on top of "Changes from the source note")

6. **Scale.** TY2025 returns 852,947 (code 1 719,213, code 2 24,281, code 3 109,453), a quarter of the draw's
   3,412,000, because four tax years of returns and dependents schedules have to ship for the corpus to be rerunnable.
   Every count in the note is non-round; the source note's round thousands were a generation tell.
7. **Trust group.** Own AGI $520,000 to $742,000 (not $620,000 to $740,000) and $30,000 to $130,000 per return (not up
   to $90,000), so the group is 34 per cent of the household heads in its band instead of nearly all of them.
8. **Twin pair.** Kessler and Abington published at 301 against 287 (4.7 per cent apart) instead of 117 against 58,
   because a 2.02x pair makes the stop rung miss one county by 50 per cent, which contradicts the stump sentence's
   "every miss a few per cent short" and turns the corpus into a loud alarm.
9. **Rung figures from the model.** Rung 0 $520,000 and rung 1 $562,000 at the top floor (the source note's $504,000
   and $565,000), and the all-filer grid cells moved down because commuters now sit below the floors.
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
- Trust group: 2,350 of those returns carry $30,000 to $130,000 of trust and investment income (about $170M in all),
  claimed by 1,475 households whose own AGI is $520,000 to $742,000. Attached, 976 of them cross $742,000; with the 4,850
  households whose own AGI is already above it, exactly 5,826 (the top 1 per cent) sit at or above it. No household total
  reaches $1M.
- Conveyor (every year, published or not): N households cross each of $100K, $200K, $300K and $500K on their children's
  income (N = 23, 10, 30 and 30 for TY2022 to TY2025); in every class below $500K the attached income of households that
  stay in the class balances the boundary flows to the dollar, so the stop rung ties every class cell outside
  $500K to $1M. No household of $1M or more holds attached income. Other filing dependents sit in households under
  $100,000 and stay under it.
- Commuters (codes 2 and 3): AGI mostly $35,000 to $180,000 (median about $72,000), about 1 per cent above $500,000.
- Dependents schedule: about 420,000 rows (every claimed dependent, filer or not); 94,807 of the claimed TINs file.
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

**$214,000 / $318,000 / $742,000.** On the natural pipeline (rung 0, $168,000 / $243,000 / $520,000) the answer sits
27.4, 30.9 and 42.7 per cent higher, and it is the extreme (maximum) cell of the 12-cell grid at every floor (L5). Margin
over the nearest wrong cell: 11.5 per cent at the top floor (dropped dependents). At the 10 and 5 per cent floors the
dropped-dependent cell coincides by design (no published class from $100,000 to $500,000 separates the two), and the
nearest differing cell is the stop rung, 7.9 per cent below. **The guard that binds is the separation floor**, not the
1.20x rung margin: the answer is a figure graded to the nearest $1,000 and there is no ranking to change.

### Ladder

| Rung | Gap | Construction | Floors (10 / 5 / 1 per cent) | Cells reproduced | Killed by (one shipped fact) |
|---|---|---|---|---|---|
| 0 | objective | every return is a unit, all filers | $168,000 / $243,000 / $520,000 | 0 of 69 | the methodology's "full-year resident" with the codebook's residency codes |
| 1 | population (scope) | full-year residents, each return a unit | $179,000 / $265,000 / $562,000 | 3 of 69 | the published class cells: only the three totals tie |
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

**Worth of each move on the graded floors** (10 / 5 / 1 per cent): rung 0 to 1 +6.5 / +9.1 / +8.1 per cent; 1 to 2
+10.1 / +10.6 / +5.7; 2 to 3 +8.6 / +8.5 / +10.6; 3 to 4 0.0 / 0.0 / +12.9; 2 to 4 +8.6 / +8.5 / +24.9. **Sign
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
corpus, and lands; that solver is the one response the bar allows. The schedule's own shape works against it: about
420,000 listed dependents of whom 94,807 file, so it reads as a list of children rather than a list of returns.

### Position table (figure form)

| Rung | Floors | Distance from the answer (10 / 5 / 1) | Cells |
|---|---|---|---|
| 0 | $168,000 / $243,000 / $520,000 | -21.5 / -23.6 / -29.9 per cent | 0 |
| 1 | $179,000 / $265,000 / $562,000 | -16.4 / -16.7 / -24.3 | 3 |
| 2 | $197,000 / $293,000 / $594,000 | -7.9 / -7.9 / -19.9 | 58 |
| 3 | $214,000 / $318,000 / $657,000 | 0.0 / 0.0 / -11.5 | 55 |
| 4 | $214,000 / $318,000 / $742,000 | answer | 69 |

The answer leads no intermediate rung at the top floor; rung 3 coincides with it at the two lower floors (stated, and
priced by the gate). No rung sits within 6 per cent of the answer at a floor where it differs.

### Discriminator dominance (figure form)

The decisive move is worth +8.6 / +8.5 / +24.9 per cent on the graded floors against a separation floor of 6 per cent and
a quantile-convention spread under $100 (0.05 per cent at the top floor). The count effect (14.0 per cent fewer units)
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
| code 1 | return | attached | $195,000 / $287,000 / $620,000 | -16.4% | 3 | class cells (spouses split) |
| code 1 | return | dropped | $195,000 / $287,000 / $601,000 | -19.0% | 0 | totals and class cells |
| code 1 | return | separate | $179,000 / $265,000 / $562,000 | -24.3% | 3 | class cells |
| all | filing unit | attached | $195,000 / $286,000 / $589,000 | -20.6% | stage 3 | totals, class cells (residency) |
| all | filing unit | dropped | $195,000 / $286,000 / $580,000 | -21.8% | stage 3 | residency, totals |
| all | filing unit | separate | $182,000 / $266,000 / $550,000 | -25.9% | stage 3 | residency |
| all | return | attached | $179,000 / $260,000 / $556,000 | -25.1% | stage 3 | residency, spouses |
| all | return | dropped | $179,000 / $260,000 / $549,000 | -26.0% | stage 3 | residency, spouses, totals |
| all | return | separate | $168,000 / $243,000 / $520,000 | -29.9% | 0 | residency |

**Partial applications, swept separately:** dependents' income attached while their returns stay units (income counted
twice): $197,000 / $293,000 / $613,000 (-17.4 per cent), 66 of 69, refused by the three totals; attachment to the
claiming spouse's own return without recombining spouses is the (code 1, return, attached) cell. The all-filer cells
reproduce at most the 12 county cells (commuters carry an out-of-state county code); their exact counts are computed and
asserted at stage 3. Nearest wrong cell where it differs: 11.5 per cent at the top floor and 7.9 per cent at the two
lower floors.

### Calibration corpus

- **Form.** The conference's Household Income Tables for TY2022 to TY2024: for the nine classes from $100,000 up,
  household units and AGI ($ thousands), plus total AGI, 19 cells a year, 57 in all; the TY2024 table's appendix gives
  household units above $500,000 in the 12 largest counties. 69 cells.
- **Back-test.** Households reproduce 69 of 69 exactly at the published precision (rebuilt from whole dollars, so no
  rounding path splits). Rivals: income attached with units kept 66, filing units 58, dropped dependents 55, residents
  by return 3, attached to a return 3, all filers by return 0. Charitable scoring: the smallest rival miss is 2 units on
  a county cell, 2.0 per cent on a total-AGI cell (the two partials) or 3.1 per cent on a class AGI cell, all outside
  anything the published rounding (whole counts, $ thousands) excuses.
- **Stop rung's misses, exactly 11.** $500,000 to $1M household units short by 23, 10 and 30 (TY2022 to TY2024, all
  under 0.5 per cent); that class's AGI short by 3.4, 3.1 and 3.6 per cent; five county cells short (Kessler 14 of
  301, 4.7 per cent; four others 2 to 4 each, under 1 per cent). Every class cell outside $500,000 to $1M ties to the
  dollar.
- **Twin pair.** Kessler and Abington hold 287 federal filing units above $500,000 each and the same count of resident
  returns above $500,000, with dependents' own returns within 2 per cent of each other; published household units above
  $500,000 are 301 against 287. Kessler's 14 are households just under $500,000 whose children's custodial-account
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
  the latest version received; the TIN-resolution register; the two wage-statement channels.
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
| H1 transfers: credits elected on TY2024 returns posted Feb to May 2025 as transfer rows citing the TY2024 return are not receipts; transfer rows citing a payment misapplied to another year are cash, dated by the original payment | D5 with D7 linkage | A1 | April cells +8 to +15% if credits counted; every cell -1 to -3% if all transfers dropped |
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
  at least two devices; composed deltas asserted for every subset of mishandlings (15 subsets on April cells, 7 on the
  other A1 cells, 3 on each A2 and A3 figure), none within 1 per cent of the golden.
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
$197,000 / $293,000 / $613,000; 3 hits at $195,000 / $287,000 / $620,000. (12) All 12 grid cells computed; the answer is
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
   with $30,000 to $130,000 of their own trust and investment income, and 976 households (17 per cent of the top 1 per
   cent) cross the mark on it. Forced by the top floor's 12.9 per cent shape effect over the dropped-dependent cell.
   Mitigation: the state taxes each return on its own brackets with no child-income rule, the same cause that drives
   separate filing; invisible before the join.
3. **No attached income in households of $1M or more.** Forced by the one-class miss pattern; invisible.
4. **Dependent filers are 13.2 per cent of resident returns,** about twice a national share. Forced by the count effect
   the two lower floors need (7.9 per cent). Mitigation: a low dependent filing threshold with withholding on teenage
   wages.
5. Separately filing couples are 6.2 per cent of filing units, plausible for a state that allows separate returns on
   one schedule. Two counties equal at 287 filing units above $500,000 is a coincidence of one count.

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
metric in the prompt's voice, stump sentence). Verdict: pending stage 3 (generator assertions) and stage 6 (judge
rehearsal).

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
