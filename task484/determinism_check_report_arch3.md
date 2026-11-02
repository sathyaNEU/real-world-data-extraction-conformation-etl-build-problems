# determinism-check report, task484, 2026-10-24

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (carries to the shipped pack 87a0101c91c1a4ef for the main call and every graded figure; see Pack-identity note for the one ask-B caveat)
**Stumping type:** mechanism: other (current-season activity nowcast by difference-in-differences against an unaffected control group), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Pack-identity note
The judge thread read target.zip d51a7c26815e683b (unzipped at /tmp/determinism-check-task484-484-1792865040/target/). The shipped target.zip is 87a0101c91c1a4ef (21 files in both). I diffed the two by md5. Three things differ:
1. assessor_housing_units_2010_block_groups.csv is renamed assessor_housing_units_by_block_group_2025.csv. Content is byte-identical (md5 e01f28dd82a3ae9c).
2. burn_zone_parcels_2025.csv: the commercial parcels at 5198 QUARTZ RD (East Bench) and 7438 SAGE HEN TRL (West Bench) get parcel ids of their own. Geocodes are now unique across all 19,769 rows.
3. wapiti_propane_accounts.csv: account 51284 (5198 Quartz Rd, Commercial) carries its new id.

Neither the parcel nor the account change touches a residential home, a zone or the commercial-propane category's membership, and the generator's figures are unchanged.

**Does the APPROVE carry?** Yes for the main call, the critical components, the zone CSV and ask A. Changes 2 and 3 are id hygiene on commercial rows, and the thread's recomputed figures depend on residential joins and on category/zone membership. For ask B (the outside-the-area sheet) the carry is conditional: the thread's own derivation cites "the 2010 assessor file" and "assessor 2010 BG outside share", so its vintage reading may have come from the old file name. I therefore tested the renamed pack myself.

**Assessor vintage, current pack (I confirm the coordinator's measurement).**
- The assessor file has 56 rows over 48 block_group codes (Inside plus blank rows; the same code set as the ACS files).
- For all 48 codes, assessor housing units equal the relationship file's HU_20_OVERLAP summed by GEOID_BG_10. There are 0 mismatches and the ratio's standard deviation is 0.
- Summed by GEOID_BG_20 they differ in 34 codes, and the ratio's standard deviation is 0.447.
- So the 2010 vintage is recoverable from data alone, with no file name or header needed. Step 7 of the submission names the handling.
- The tool documentation (section 3) says only "the county assessor's housing unit counts" and gives no vintage. The code sets of the two vintages coincide, so a reader gets the vintage only by testing against the relationship file.
- The old file name stated it outright. The renamed pack makes it a data check instead, which is a modest tightening, and it is not a second defensible answer: the alternative (skipping the crosswalk) gives 3,350 households and 221.9 t, against 240.0 t, and fails the exact-sum test.
- Residual risk is confined to ask B (12 criteria) and none touches the call. I make no repair recommendation.

## Why
The thread's verdict was DETERMINISTIC, with one residual risk on the main call that it does not count against the verdict. The estimand is filed: the PM2.5 from wood burned in the 2025-26 season, at the 2023 factors, against Table 4-2. The pack separates the candidate methods. In every zone the propane homes with a heating appliance in use in both seasons took 26 to 32 per cent less propane (season ratio 0.68 to 0.74). The homes without one were flat at 0.996 to 1.002. The two seasons' heating degree days are identical (7,393.5 against 7,394.5). Each home has one heating device, so the displaced wood has no efficiency or device ambiguity.

That puts East Bench and West Bench over their allotments and Valley Floor North and Upper Valley under. Valley Floor South is over either way, and 465,000 / 3 = USD 155,000 each. Every enumerated variant (no pooling, unweighted pooling, removed devices counted, a pooled control ratio) leaves the same set. The thread's sensitivity: displaced wood needs to be about 59 per cent (East Bench) and 63 per cent (West Bench) of the golden estimate to hold the call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Devices in use (registry Active, installed before 1 Oct 2025, not removed) | 12,100 | 12,100 | yes |
| Survey carry-forward tons (East Bench / West Bench) | 78 / 68 | 77.9 / 68.2 | yes |
| Survey carry-forward tons (Valley Floor North / South / Upper Valley) | not stated in the golden | 57.5 / 56.3 / 47.3 | n/a |
| Propane-displaced wood PM2.5 tons (VFN / VFS / EB / WB / UV) | 2 / 3 / 20 / 15 / 7 | 1.66 / 2.64 / 20.22 / 14.77 / 6.81 | yes |
| Zone PM2.5 tons (VFN / VFS / EB / WB / UV) | 59 / 59 / 98 / 83 / 54 | 59.2 / 58.96 / 98.1 / 83.0 / 54.2 | yes |
| Fund shares | 155,000 each to VFS, EB, WB | 465,000 / 3 | yes |
| Commercial propane gallons | 515,500 / 437,300 / 323,000 / 253,000 / 276,900 | same | yes |
| Commercial NOx tons | 3.35 / 2.84 / 2.10 / 1.64 / 1.80 | same | yes |
| Outside the area appliances | 2,753 / 2,999 / 652 / 1,333 / 3,347 / 507 | same | yes |
| Outside the area PM2.5 tons | 118.6 / 50.4 / 9.9 / 4.0 / 16.1 / 41.0 | same | yes |
| Main-heat households outside the area | 3,622 | 3,622.3 | yes |

The thread read the old pack. Ask B's vintage handling was independently re-verified by me on the shipped pack (the Pack-identity note). The other rows were not re-run on 87a0101c91c1a4ef, but the diff shows no input to them changed.

## Competing answers that survived
None failing. One recorded fork:
- Survey carried forward unchanged gives Valley Floor South only (fund 465,000). This is the declared default-path error, and the shipped data contradict it (the 26 to 32 per cent shortfall against the flat control).
- Secondary, asks only: the Coldwater ticket-reference date is not in the record layout, and TRANS-DT instead gives 484,700 / 419,300 / 309,000 / 235,200 / 260,900 gallons. The ticket reference equals TRANS-DT for every residential row and is recoverable from the data.
- Ask B: skipping the crosswalk gives 221.9 t against 240.0 t. It is closed by the exact-sum test above.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 21 | yes |
| Formats | 3 or more | 4 (csv, txt, xlsx, pdf) | yes |
| Large file | 25,000 rows or more | Coldwater 64,123 lines; Wapiti tickets 43,811 | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | burn_curtailment_calls_2023_2026.csv, forest_firewood_permits_2019_2025.csv | yes |
| Distractors relevant but unused | each weighable and unused, ruled out by a shipped fact | thread found both relevant and unused, and neither carries the call (the temperature file is neutral by design) | yes |
| Deliverables | 1 to 3, all in the golden | 2, both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | zone PM2.5 nearest ton, gallons nearest hundred, NOx two decimals, county appliances whole and PM2.5 one decimal | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | shape 07, 45 criteria per the design note | yes |
| Not LLM-reading, realistic goldens | | The xlsx has five sheets (RWC inventory, Propane comparison, Commercial propane, Outside the area, Notes). Nothing in the pack or goldens reads as generated. | yes |

## Gate G reconciliation
- Thread: mechanism "other" (a difference-in-differences nowcast of the open season), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
- Card and design note: stump_strategy causal_design, gate_g decomposition_attribution, stump_class analytical, layer2_family estimand_identification. The thread's reading is the same mechanism in different words.
- Declared distractors (curtailment calls, firewood permits): the thread names neither as the surface read carrying the task. No finding.
- Gate G line: no shipped artifact ranks the zones on the decision and gets it wrong. The survey-carry-forward figures exist only as the solver's own error path and nothing ships them. The difficulty survives deleting every wrong number from the pack.
- Minor: the card's analyst_test text is garbled against the design note and golden. It says the "valley floor zones" are over and the "benches" under, whereas the note says Valley Floor South alone is over on the default path and the benches go over on the golden. This is a card-text fix for the author and not a determinism finding.

## Gate H line
domain: pass; layers: pass; decisive_step: analytical.
- Layer 1 is the three distributor layouts, the Coldwater posting date against the delivery date, the 2010 against 2020 block groups, and mixed survey units.
- Layer 2 is estimating the open season's wood burned by comparing appliance homes with appliance-free propane homes in the same zone, season and weather.
- This matches the design note's `## Three rules`: No decoy, Not semantics, Not rule application. The thread reached the golden by recognising the switch, which the note also states as the decisive step. No judgment was left that the data did not settle.

## Stump power (Gate F)
Good, per the thread. A strong analyst who cleans the data and reads every rule correctly still plausibly files the survey carry-forward (Valley Floor South only, 465,000). Two cautions for the main thread to weigh with the scored readers' result:
- Nothing in the prompt points at the residential propane accounts, so a failure may be partly discovery. That is the intended analysis, not a hidden rule.
- The design note concedes that the cheapest method (each home's 2024-25 gallons less its 2025-26 gallons, no control) already files the golden set. Once the switch is recognised, the method is not a second hurdle, so stump power rests on recognition.

## Findings, ranked
1. Pack mismatch: the judge read d51a7c26815e683b and the shipped pack is 87a0101c91c1a4ef. The differences are harmless to the call and the graded figures (see the Pack-identity note).
2. The file rename moves the assessor vintage from the name to the data. I confirmed it is recoverable (exact-sum test, 0 mismatches). The thread cited the vintage, perhaps from the old name, so ask B on the shipped pack rests on my check and not on the thread's. This is low severity.
3. The Coldwater ticket reference date is undescribed in the layout but recoverable. Asks only.
4. The registry is stamped 2026-05-15 but shows no installs or removals after 2025-09-28, and Coldwater holds 63 postings dated 2026-07-01. Both are explained and neither affects the stump.
5. The card's analyst_test text conflicts with the design note.

## Next action for the author
Proceed to ship on 87a0101c91c1a4ef. Correct the card's analyst_test to match the design note, and do not re-judge unless the scored readers' result calls for it.
