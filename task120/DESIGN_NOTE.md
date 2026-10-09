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
- First-moves test: the methodology's word "household" beside a shipped dependents schedule may send a strong solver straight to the attachment (Part 1, property 1). Run it on paper.
- The note's asks A and B (withholding by wage month, estimated payments by instalment) may fail the H18 fourth read as figures a person could act on with the schedule unmade; re-cut them to per-tier figures carrying the same devices. Ask C as written names the four constructions; the exemplar's form is the closest reading that does not stand. Without A and B the shape-14 core sits near 23 criteria.
- The requester heads the office that staffs the conference, so the world needs a reason the office does not hold the household construction.
- 3,412,000 synthetic return rows is heavy for one pack; settle the format or a scaled state at dataset-generation.

## Tried and rejected
