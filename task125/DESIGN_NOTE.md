# task125 design note (architecture 3, the Umzimela sulfate loads)

Architecture 1 (Wealdmoor County Council's digit filter) and architecture 2 (Merrowland Statistics' Household Labour
Survey) are spent and in the card's lineage; their measured deaths are in `## Tried and rejected`. Architecture 3 draws
a new domain, world and dataset.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task125.json`, architecture v3, registered 2026-10-31 after `guard.py
  recent`, `coverage`, `mechanisms --objective anomaly-detection` and `slots` on the mechanism's words (mixing, mixing
  zone, confluence, mass balance, plume) and the setting's (sulfate, sulphate, acid mine, dissolved oxygen, diurnal,
  grab sample, sonde, lightning, arrester, vegetation, trim cycle). `check` WARN only: `overuse.org_family`
  (government_agency is the honest kind for a catchment management agency) and `repeat.decision` against task181 v6
  (the call is which resource units are over their allocations, a designation by nature; the answer unit differs in
  kind, units of a river against consultants). The two older structural matches are differentiated on the card
  (task84, task257, task269).
- **Pairing:** Physical & Environmental Sciences, task type environmental-monitoring-exceedance, objective Anomaly
  Detection & Diagnostics: which resource units of a coal-mining catchment carried more sulfate past their boundaries
  in the 2025/26 dry season than their load allocations allow, the units whose mines the Governing Board directs in
  2027.
- **Shape:** other (a designation against filed allocations: each resource unit's dry-season load and verdict, with
  the asks' per-site, per-gauge and per-discharge grids supplying the rest of the criteria). Scorecard shape 10 is
  barred against task181 by the guard's two-build window, and the structure is honestly a designation with
  per-unit loads rather than a scorecard of indicators.
- **Strategy:** `composition_mix`. The water a boundary monitor samples a few kilometres below a mine stream's
  confluence is a different blend of the two inflows than the whole river carries past the boundary, so the point's
  concentration is the bank's mix, not the section's. Gate G `method_or_model_selection` (two ways to put a load on
  the boundary, the boundary sample times the boundary flow or the inflows' loads carried down, the right one forced
  by conservation in the record); gap objective then population; generators G2 (the point against the section), G5
  (the load is measured where each inflow is mixed, upstream), G3.
- **Data-native sentence:** the agency's boundary monitors stand at gauging weirs chosen for bridge access, two to
  four kilometres below the confluences of the mine streams, where a stream's water still runs along the bank it
  entered on, so on every run the near-bank monitor samples the mine stream's water and the far-bank monitor the
  main river's, while each inflow's own monitor upstream samples water that is already mixed.
- **Abstraction sentence** (what a reviewer holding this build and its nearest approved build would say is the same):
  none writable. The nearest drivers on file score 0.07 and under; task263 (a source's level recovered from blends
  of sources running together) is the inverse move, a blend's level recovered from sources, and task120 (a draw read
  as inflow less storage gained) closes a balance over a stock in time rather than over a river's inflows in space.
- **Sources:** synthetic throughout. The world (the Umzimela Catchment Management Agency, its rivers, gauges, monitors,
  mines and people) is fictional and modelled on how South African catchment agencies, the national gauging network
  and coal-mine water use licences work; personas from `guard.py names --locale zu_ZA --seed 125`.

## Tried and rejected


- The source note's decisive rung (Housing Support's cohort run off on the 2021 intake's 30-instalment term) as the decisive rung: the pilot's plain solver replays records at the finest grain and runs event studies on staggered cohorts, and the 2021 intake's full rise and run-off sits in the same flagged-cell series, so a strong solver constructs it; kept as rung 3.
- Re-pricing Adult Social Care's standing stream at a 2027/28 tariff filed in the council's budget (band 2 from 366 to 399 a week, out of cell 14): honestly labelled (time, A) or (time, G13), which the guard blocks inside the batch (task121 v1 lineage) and as spent in ten older builds, with G13 task122's decisive generator; a relabel to G11 or G6 would not name the move as a reviewer would. It also hangs on a stated rate one multiplication from the digit consequence.
- An upward entrant move with the cohort drop under about a sixth of the closed-year figure: the run-off (down) and the entrants (up) cancel near the closed-year carry-forward, which then lands inside 10 per cent of the answer (L4); the targets keep the drop near 30 per cent.
- Step-down hosts inside the flagged cell, paid the same 1,464 as long-term band 2 hosts and separable only by the turnover pattern in their payment histories (a downward decisive move): its honest label is G3 (record versus operation), task121's decisive generator, and the affected payments sit in the very cell the solver is already examining.
- A guest-level arrangements register in the pack: it turns the carers' composition into a schema-visible join from payee to guests, RC01 v2's death (a two-hop join found from the schema alone) and FC01 loop 2's (a dated attribute of an entity the chain already joins); not shipped.
- Landlord-consolidated remittances in the Tenancy Sustainment scheme (a landlord's monthly payment falling into cell 14 once one household remains): the forward entrants are a few per cent of the answer at any realistic landlord mix, too small for a decisive rung.
- A fourteenth four-weekly cycle in 2027/28 (a 366-day year with a payment date on 1 April 2027) or a 53-Thursday year as a rung: worth 2 to 8 per cent of one stream, a knife-edge hazard; the design picks cycles that add no plan-year date unless it prices the cell.
- A plan-year move from four-weekly to monthly payment, or to fortnightly payment runs: a stated change the solver applies at first order, and its amount consequence sits on the remittance grain a screen rung already validates.
- The filter's own examination holds merging held payments into the next run: a council's digit filter examines after payment, and the merge timing opens forks the judge would read as unpinned.
- The 2025/26 screen close-out as the context artifact (close_out_summary): blocked at registration by ban.artifact against task124, drafted in parallel; the same closed-year figures ship in the filter's 2025/26 run log (operations_log).
- One step-down rate with 70 dual carers on one combined amount (3,044): 910 payments a year land in Adult Social Care cell 30, which then flags itself on the 2025/26 screen (paper ratio about 1.4), so the closure moves payments from one flagged cell to another and the decisive rung is worth zero; three tiers and 60 carers keep every Shared Lives cell under 0.86 of threshold.
- Twins identical on every statement figure (payments tested and MAD as well as the cell-14 count): Housing Support would need about 50,000 payments a year in range, which a county's housing-related support service cannot carry; the twin is held on the run log's 2025/26 line only.
- A second plan-year monthly series for the department that moves most (the draw's criteria arithmetic): a denser split of the committed figure, twelve more criteria the cracker banks free; replaced by the two 2025/26 tables.
- Annotating the plan-year month furthest from the closed-year line: January, February and March 2028 tie at 476 routed payments, an ungradable part; the busiest month (December 2027, 638 by run month) is annotated instead.
- The 2027/28 payment-run calendar on the main path, with "four weeks ending on the run date" as the pin against a 12-run reading: unnecessary, since the 28-day cadence fixes 13 runs and a 12-run reading files the same hundred; kept for the monthly ask only, so the main path carries no file an ask device lives in.
- The spending file from April 2021 with every department's background (build): about 100 MB of CSV; the file starts April 2023 and the 2021 round's histories ship in the Housing Support case extract, which is where the term pin lives anyway.
- Waste & Environment cell 25 as the run log's extra cell (build): a cell-25 count near 500 under 0.86 of its threshold needs a Waste department of more than 22,000 payments a year; cell 11 reaches it with 11,000.
- The rung-1 lever at net cell 20 with Property & Facilities at 7,400 invoices (build): rung 1 landed 8,348, and the net basis with the run-off applied then filed 6,458, inside the answer's hundred; the gross cells 20 to 25 had no room for more bills, so the lever moved to net cell 15 and rung 1 to 8,992.
- Rung 4 (Shared Lives carers' combined amounts decomposed against the weekly rate schedule, step-down placements dropped) as the decisive rung, round 1: the plain solver landed 6,522, filed 6,500, by listing the carer amounts against the rates at its step 4 in its own words, "On each carer pay date, 102 payments are £1,464, and 22 + 20 + 18 more are £1,464 plus a step-down rate (£3,044, £3,272, £3,524). When Home First step-down closes on 31 March 2027 those 60 drop to £1,464". The noisy amount universe did not hide them: the three combined amounts are the only carer amounts equal to 1,464 plus a step-down rate, so the decomposition is one subtraction, not a construction.
- Harden loop 1 (opening line), rung 4 as the decisive rung measured by round 1 plain (proxy 80.2, call landed at path step 4): the solver read every "Shared Lives carer payments" row as one carer's whole fee, summed at the carer grain in its own words, "ASC total: 115 x 12 + 162 x 13 = 3,486", having climbed rungs 2 and 3 and stepped over the side cell by taking the 2025/26 cells; a louder pin, a second decoy or a noisier amount list would only lengthen the same subtraction, so the repair attacks the assumption the sentence holds fixed (one row is one carer's fee) rather than the decomposition itself.
- Rung 5 (joint households' half-fees at the household grain) as the decisive rung, round 2 plain (proxy 85.1, call landed at path step 4, filed 6,700): the solver never constructed the household grain; it decomposed each half against the rate card on its own, read the 2,274, 2,388 and 2,514 halves as two weeks of each rate, dropped the step-down weeks and got 1,484 per vendor, in its own words "2,274/2,388/2,514, which leave 1,484 (16). That gives 178 per run". The halves are linear in the household fee, so halving the rates gives the same result as re-summing the household and halving it again; the grain gap never moves a single vendor's post-closure amount, and the rung cannot change the answer (discriminator dominance failed, not silence).
- Harden loop 2 (opening line), rung 5 as the decisive rung measured by round 2 plain (proxy 85.1 after the --landed yes regrade, call landed at path step 4): the solver treated each joint half as two weeks of each weekly rate, in its own words "2,274/2,388/2,514, which leave 1,484 (16). That gives 178 per run", so a grain step whose arithmetic is linear in the fee (halve, then subtract the halved step-down rate) can never move a vendor's post-closure amount; the repair has to make the household grain change the result, which only a non-linear step at that grain (a household-level threshold, cap or rate that a half cannot see) can do.
- Centring the loop 2 answer at 6,902 by trimming a flat stream by one payment a month (Property & Facilities 81 to 80, or Highways cell 49 66 to 65): the 2025/26 batch returns are drawn per payment, so the trim reshuffled the examined counts and put both unused-volume charges 2 pence off a half-pound edge (1,604.48 and 603.52 or 655.04); loop 1's stream counts were kept, the answer is 6,914 (36 from its upper edge) and asks B1, B2 and C are unchanged.
- The whole build after harden loop 2 (rung 6, the joint-household one-guest payment rule, as the decisive rung; round 3 plain missed at 43.3): the determinism judge returned SEND_BACK on 2026-10-10 with the mechanism matching the note on every field, so the build was retired and not submitted.
- Architecture 1 as a whole (2026-10-12, at the re-root): spent by two in-house solves and a judge SEND_BACK; the
  author's no-retirement rule re-roots the slot to architecture 2 on a new pairing.
- Interviewer falsification in a victimisation survey (2026-10-12, at the draw, never registered): fabricated
  interviews are wrong records, so catching them is a planted defect under the three rules whatever the method.
- A sample boost entering all at wave 1 against rotation-group bias (2026-10-12, at the draw): the first-interview
  bias moves a regional rate by about 0.1 point at any realistic boost, too small to carry a call.
- A staggered web-first rollout read by event time (2026-10-12, at the draw): the arm comparison and the per-wave
  phasing are what a survey-literate solver does first, and every estimator choice opens a numeric fork.

- Architecture 2's first ladder (2026-10-20, at this re-root): the methods note's section 5 stated the procedure the
  decisive step executes ("applying the change to the last full quarter collected before it and re-running the
  estimation as in section 4"), so a blind Sonnet reader at medium effort, holding only a fresh unzip of target.zip,
  the prompt and the figure names, took 2 of 2 call figures and 38 of 53 ask figures and quoted that sentence as what
  told it the step. Under rule 3 that is rule application, not analysis. Not repairable by deleting the sentence
  alone, because the base quarter it pinned would then be an open knob (measured: up to 0.085 point of movement on a
  figure printed to 0.01); the re-root deletes the sentence, lets the call-record app's coverage settle the base
  quarter, and moves the cap's timeline so the decisive step carries the headline.
- Keeping the cap on one intake and removing section 5 only (2026-10-20, at the re-root, measured): with the cap
  issued for a single quarter before the released one, the wave-1 route and the golden give the same cap share of the
  April to June to July to September change, because only one of the two quarters has a capped wave 1. The decisive
  step then carries no graded figure of the headline, only the forward path, which is exactly the half the measured
  reader took last. Rejected for the field-year timeline, which puts a capped intake in both compared quarters and
  makes the wave-1 route file 0.00 of the 0.27-point rise.
- Grading the non-contact bias of the published rate instead of the six-visit counterfactual (2026-10-20, at the
  re-root): the level of the bias is genuinely unobserved (measured at +0.78 to +0.84 point of unemployment in every
  pre-cap quarter against the eligible population, and +0.99 under the cap), which would put an estimated quantity in
  the deciding position. Rejected on the determinacy screen: it needs the never-contacted households, whose outcomes
  are reached only by extrapolating a level-of-effort gradient past the sixth visit, and the geometric contact process
  behind the pack is a three-class mixture whose tail mass is identified only to within a wide band, so the estimator
  family would be open on a figure printed to 0.01.
- Making the wave structure something the solver infers from the sample's own composition rather than from the methods
  note's section 1 (2026-10-20, at the re-root): a methods note that does not document a rotating panel's rotation is
  not a methods note, and the person file carries a `wave` column besides, so the rotation is schema-visible whatever
  the documents say. Readability test 2 fires. The re-root leaves the rotation filed and moves the decisive step to
  the unit the change acts on instead.
- Identifying the capped-out households from the capped intakes rather than from a pre-cap quarter, so that the
  counterfactual is estimated rather than subset (2026-10-20, at the re-root): with the pre-cap call records removed
  the forward path is unidentified, because nothing then measures how the selected households' outcomes persist
  across the telephone waves; with them shipped the counterfactual is exactly recoverable by subsetting and the step
  is arithmetic. Same dial, both ends. Recorded as the architecture's structural ceiling: no stage-2 move puts an
  estimated quantity in the deciding position on this draw, and a third measured Gate F failure retires the number
  rather than hardening it.

- Architecture 2 as a whole (2026-10-31, at the batch audit, re-rooted rather than repaired): it shipped before the survivor-anatomy gates and falls short on all three of them. The actor is schema-visible (the person file's `wave` and `intake` columns, the visit number reaching the later waves through the household serial, a key that invites the join), so there is no actor without a column and no link without a key; and the field's method (re-running the calibrated estimator on the capped subset) is the golden rather than the bottom of the ladder, which its own "Not rule application" line conceded by calling the decisive step exact arithmetic on recorded fields, argued rather than measured. Architecture 3 draws a new domain and world.

