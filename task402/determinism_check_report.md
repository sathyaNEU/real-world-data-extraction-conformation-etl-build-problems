# determinism-check report, task402, 2026-11-04

## Pass 1 (target.zip f2a3c845, judge thread run by the coordinator)

**Verdict:** DETERMINISTIC. **Disposition:** FIX_NOW (SOLUTION_WRONG, minor: step 2's frost clause executed on the
trip's own day dropped one record, 8,433 against the stated 8,700). Closed in one generator pass (the clause removed,
the world changed so every pairing operationalisation gives 8,714), with the leak reader's realism and ask findings.

### The thread's verdict, verbatim

- **Verdict:** DETERMINISTIC, SOLUTION_WRONG (minor: SOLUTION_STEPS step 2 does not reproduce the SO-7 figure it states).
- **Disposition:** FIX_NOW. Rewrite step 2 and critical component 1 so the SO-7 selection is "section overload records starting within 10 minutes of that section's restoration from an interruption of 60 minutes or more" (no -3 C clause), or restate the figure; the pack and prompt are untouched, so no model rerun. Also fix the prompt wording noted under Gate E (optional, wording only).
- **Why:** Own derivation before opening the blocks reached the heat-pump waiver (1,520) as the largest change and missed SO-7. After opening the blocks I checked the SO-7 claim against the files and it holds. From 1 Dec 2025, 39 of the 44 section-level OVLD records (CI 8,700 of 9,920) begin 0.2 to 3.8 minutes after the same section's restoration from a 75-minute or longer outage, while the other 5 sit thousands of minutes from any restoration. In the FY2025 and earlier data, 0 of 357 cold-day restorations of 60 minutes or more are followed by such a re-trip, against 39 of 141 after SO-7 (restoration_steps shows multi-step restoration falling from about 37 percent to 13 percent of winter events). So the data force SO-7 (about 8,700) ahead of the waiver (about 1,500), animal guards (about 700), risers (about 700) and Brekke (about 100). Gates A to E pass for the call, with the exceptions listed below.
- **Evidence (recomputed):**
  - MED threshold 15.51 min; FY2026 MED is 10 Apr 2026 only (133 events, 19,274 CI); base 203,412 CI, SAIFI 1.563, ties to the review.
  - SO-7: the paired set is 8,700 CI exactly. Applying the step's own "day averaging -3 C or colder" test (Chicago local dates) drops the 18 Mar 2026 record (day mean -2.44 C, 267 CI) and gives 8,433, which rounds to 8,400 and a gap of 6,900. The -3 C figure appears in no shipped file and does no work (every other record is far colder), so the step and its figure disagree.
  - Waiver: 174 OVLD records on waived-HP service transformers after connection, 1,520 CI (about 1,509 net of a 12-CI baseline), rounds to 1,500. Studied-HP transformers show 0 in FY2026.
  - Animal: 8 FY2026 events at 2026-list structures, 1,697 CI, but 5 fall before the January fitting window, leaving 702 CI. Risers: 5 events after the Oct to Nov replacement window, 671 CI. Brekke: 15 XFMR events, 118 CI, about 100 excess. All three round to the golden figures.
  - Ask 1: reproduces exactly (to 2 dp) with five-minute bursts per device, lockout bursts dropped, breaker events given to the sections on that feeder at the time (the 10 sections moved on 1 Jun 2026 sit on their earlier feeder, visible via XFER records), and one event per section per five minutes across devices.
  - Ask 2: reproduces to the hour and dollar (OUTAGE orders, approved, latest entry per employee and order, rows under 15 minutes apart merged, work-order date, Article 14 and 18 pay).
  - Forks:
    - Main figure. A solver who sizes SO-7 as all post-SO-7 section OVLD records gets about 9,900 (or 9,300 net of baseline). The call is unchanged, but the graded figures 8,700 and gap 7,200 depend on pairing with restorations.
    - Ask 1. A device-sum (no merge across the breaker and recloser overlap) gives Lakes 1.45/1.88/3.01/3.53 and North 2.29/1.54/2.94/3.90, against the golden's Lakes 1.34/1.72/2.75/3.34 and North 2.12/1.42/2.61/3.51. The IEEE customer-event reading supports the golden; no file states the merge.
    - Ask 2. "Callout hours" as worked span, 4,979.5 for the year (golden), against paid hours with the 2-hour minimum, 6,171. Article 14.2 defines a callout as a span and supports the golden, but the prompt does not say which hours.
- **Files/Hygiene:** PASS. 16 files in 5 formats (csv x6, xlsx x5, docx x3, pdf, parquet). Heat-pump terms, rebates, IVR calls, wholesale bills and HQ temperature are distractors, with temperature used only for the unneeded frost clause. No authoring or provenance leakage seen, dates sit inside the 30 Sep 2026 setting, and the operational mess is realistic (legacy hours vs minutes, crosswalk ids, UTC vs local, corrections and rejected entries, feeder transfers). No exclusion-level finding.
- **Stump power:** Strong. The tempting routes are to take SO-7 as harmless (it only shortens restoration, so it costs about 0), which names the waiver at about 1,500, or to cost the animal programme at 1,697 (all FY2026 events at list structures, ignoring that 5 precede fitting), which also beats the waiver. The real trap is the cold-load-pickup re-trips that only a restoration-paired look at the overload spike exposes. Moderate residual risk is that models land on 9,900 instead of 8,700 while still making the call.
- **Stumping type:** `mechanism: decomposition_attribution (counterfactual change costing)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The review's wording ("to shorten restoration times") is a stated intent, not a wrong number the solver must reject, and the data stay honest and still stump when clean.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1 is the legacy hours vs minutes daily file, old and new section ids, UTC vs local, correction and rejected time entries, and the 1 Jun feeder transfers. Layer 2 is counterfactual attribution of each change's interruptions, in which cold-load-pickup re-trips caused by a switching change must be paired to restorations; the easy route (cost each change on its own named population) files the waiver at about 1,500, or animal guards at 1,697 if timing is ignored.
- **Fix:** solution. Correct step 2 and critical component 1 as above (remove the -3 C clause, or switch to 8,400 and 6,900 if kept). Optional prompt wording fix: "on the work plan policy's terms in reliability_fix_2027.docx" reads as if the policy is the output file; name the deliverable and the policy separately. State in the Ask 2 sentence that hours are worked hours (callout span) to close the paid-hours fork.

## Pass 2 (target.zip af10a74f, the one re-judge, judge thread run by the coordinator)

**Verdict:** DETERMINISTIC. **Disposition:** APPROVE, no fix. Gate G: decomposition_attribution, analytical_non_defect,
no surface-read dependency, no sole data defect. Gate H: domain pass, layers pass, decisive step analytical. Order kept
(derivation written before the graded blocks and the round 1 findings were opened).

### The thread's verdict, verbatim

# Determinism judge report

Order kept: yes. derivation.md was written from prompt.txt and target/ alone before graded_blocks.md and round1_findings.md were opened. Two honest caveats: my blind derivation picked the heat-pump waiver as the largest cost and missed the SO-7 re-trip mechanism (I read the 37 section-device OVLD records as cold-snap load); and my blind Ask A figures carried two coding slips (lone restoration CLOSE rows counted as events, the 4-TRIP/4-CLOSE glitch sequences treated as momentary). Both were re-derived from the files after seeing the blocks; the corrected results are below.

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE (no repair needed; optional wording hardening below, no rerun).
- **Why:** The call is forced by the files. 32 OVLD records on section devices (FUSE/SECT/RCLR) start 0 to 4 minutes after the same section's restoration from an interruption of 133 to 661 minutes, all after 1 Dec 2025, and they total 8,714 customer interruptions. Nothing else comes near, and the heat-pump runner-up (1,520) is separated from every other change by a wide margin. The easy route, bucketing the whole OVLD category onto the heat-pump waiver (about 11,450), is refuted by the files themselves: the rebate terms say the load study covers only the service transformer and its secondary, and the section-device overloads show no enrichment in sections with waived connections (8 of 37 against 114 of 558 sections).

## Evidence (recomputed)
| Item | Golden | Mine | Reproduces |
|---|---|---|---|
| MED threshold (FY2021-25 daily SAIDI, legacy hours x60 + OMS minutes, 2.5 beta) | 16.1 min | 16.09 / 16.12 (ddof 0 / 1); FY2026 MED day 2026-04-10 only | yes |
| FY2026 unplanned non-MED customer interruptions | n/a | 203,428 = SAIFI 1.569 x 129,630 (matches review) | yes |
| SO-7 re-trips (step 2, executed literally, gap 10 min, prior outage 60+ min) | 8,700 | 32 records, 8,714 | yes |
| Same selection before 1 Dec 2025 (Oct 2024 on) | none | none (only FY2026 OVLD has any pair) | yes |
| Heat pump: OVLD on transformers after first waived connection | 1,500 | 174 records, 1,520 (10 other OVLD transformer records are baseline) | yes |
| Animal guards: 2026-list structures from 1 Jan 2026 | 700 | 3 records, 702 (5 earlier records, 1,149, are before the fitting window) | yes |
| Risers: 2025-list structures | 700 | 5 records, 671 | yes |
| Supplier (Brekke units after fitting) | 100 | 134 all causes / 118 XFMR cause | yes (nearest 100) |
| Gap | 7,200 | 8,714 - 1,520 = 7,194 | yes |
| Ask B, 12 months hours and pay | listed | identical to the dollar and hour in all 12 months (4,958 h, 505,766) | yes |
| Ask A, 16 cells | listed | identical to 2 decimals in all 16 cells after the fix noted above | yes |

Step-by-step: steps 1 to 4 and 7 reproduce the stated figures. Step 5 reproduces Ask A once "ending in lockout" is read as the last operation being a TRIP (this matters: ten recloser sequences carry a stray CLOSE that balances the trip and close counts but end in a TRIP, and the lone CLOSE rows after a lockout are restorations, not events). Step 6 reproduces Ask B exactly (APPROVED entries only, latest per employee and order, date from the work order, 15-minute chain, 2 hour minimum per callout, 2x on 15 holiday callouts, none under 2 h and none crossing midnight).

Forks tested:
- SO-7 selection thresholds: gaps are 0 to 4 min, prior outages 133 to 661 min, the 5 unmatched OVLD records sit 20,000+ min after a prior record. Any window from 5 to 30 minutes and any minimum from 30 to 120 minutes gives the same set.
- Cold versus SO-7: pre-1-Dec restorations in the same files include 108 long restorations (FY2022 to FY2025) at -20 C or colder with zero re-trips, against 32 re-trips after SO-7 (restoration steps also fall from about 25 percent multi-step to about 10 percent). Cold alone does not produce the trips, so the counterfactual is forced.
- Heat-pump-takes-all: wins only if section-device overloads are attributed to a waiver whose terms exclude them and whose sections show no enrichment. Not defensible.
- Runner-up: heat pump (1,520) against 700 for the next two, forced. Guard (702) against riser (671) for third place is thin and both print 700; the golden chart and list order them at a tie, nothing graded depends on it.
- Ask A denominator: only the register's year-end district members exist at district grain (the review pins 130,325 at 30 Sep 2026). A solver who rescales to average members would shift cells by about 0.5 percent (up to 0.01); minor.

## Files/Hygiene
PASS. 16 files; formats csv (6), xlsx (5), docx (3), pdf, parquet. Largest files 52,584 rows (temperature), 30,191 (IVR), 10,815 outage records, 14,669 transformer rows. Distractors present and unused by the solution: wholesale_power_bills, ivr_calls (flicker calls against momentary), hq_substation_temperature (cold-snap lure). No provenance or authoring leakage found in the docs. Layer 1 mess is realistic and present in the data (legacy hours sheet, old section ids and crosswalk, 1 Jun 2026 feeder transfers marked by XFER records, UTC SCADA with DST against local logs, corrected and rejected timesheet entries, SCADA stray CLOSE rows). No file states the SO-7 mechanism. Nothing exclusion-level.

## Stump power (Gate F)
Strong. The surface read is that the OVLD jump (12 to 221 records) belongs to the heat-pump waiver, with the rebate terms doc standing right next to it, and the review presents SO-7 as a benign "shorten restoration times" change; a solver who buckets by cause code files heat pumps at about 11,450 and is wrong (my own blind pass fell into it). Reaching the call needs linking each overload to the same section's earlier restoration and separating it from the cold winter. Asks A and B are hard stand-alone layers.

## Stumping type (Gate G)
mechanism: decomposition_attribution (counterfactual attribution of a category on correct data); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no.
No reported figure is wrong (cause codes and counts are accurate); the work is attributing a correctly recorded movement to the right driver with the right comparison period. On clean data the task still stumps. Borderline note: the heat-pump story is a natural decoy, but it is a true smaller effect, not a planted artifact.

## Three rules (Gate H)
domain: pass, layers: pass, decisive_step: analytical.
Field analysis: costing operating changes counterfactually in sustained interruptions under IEEE 1366 conventions, including cold-load-pickup re-trips after whole-section restoration. Swap test fails to reproduce the task with other nouns. Layer 1: mixed units, id crosswalk, feeder transfers, UTC and DST, timesheet corrections. Layer 2: the attribution above. Easy route: assign all OVLD records to the heat-pump waiver (about 11,450, heat pumps wrongly fixed), or count whole cause buckets or all FY2026 events at list sites for the other changes; the guard list alone gives 1,851 against a correct 702.

## Fix
none. Optional, no rerun needed: say in the design note that the guard and riser costs both print 700 and the chart order between them is a tie by design.
