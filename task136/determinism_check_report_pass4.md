# determinism-check report, task136, 2026-11-02 (pass 4, ask rework: reverse-flow ask on the SCADA and check-meter files)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (control-group uplift estimator; etl_conformance/reconciliation for ask 6), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

target.zip md5 1bb928fd43a8a219e82f72aee9e5e1b6 (15 files, fresh unzip at /tmp/determinism-check-task136-r40528/target/). prompt.txt is current (not legacy). The judge thread was run once, in isolation, by the main session from my brief; its full verdict.md is reproduced under "Judge thread verdict" below and is the evidence base.

## Why
The main call and asks 1 to 5 reproduce from NPP-114 rev 3 and the bundle: YRB27 1.9 MW above spring 2029 hosting capacity, YRB24 runner-up at 1.7 MW, gap 0.2 MW, bulk-buys +1.7 MW (Bindarra Waters, YRB24) and +0.7 MW (Wattleview, YRB27). The estimator choices the text leaves open give 4.05 to 4.19 per hundred across every variant the judge ran and the same rounded figures. The new ask 6 has exactly one supported reading: the check meters fit the historian only with the per-bay factors (rmse 0.011 MW, max 0.06), the historian's start-labelled and the meter's end-labelled half hours align one way only (other alignments rmse 3.6 to 3.8 MW), and the month assignment by interval start or end gives identical totals because no reverse flow occurs at a midnight boundary. All 8 feeders x (3 monthly energies + 1 peak) reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| YRB27 connected capacity 31 Aug 2026 | 11,645 kW | 11,645 | yes |
| YRB24 connected capacity | 17,845 kW | 17,844.8 | yes |
| Trend YRB27 / YRB24 | 1,245 / 1,935 kW a year | 1,245.0 / 1,934.6 | yes |
| Base forecasts YRB27 / YRB24 | 15,380 / 23,648 kW | same | yes |
| Houses without PV at openings | 15,349 | 15,349 | yes |
| Campaign addition | 627.8 systems, 4.09 per hundred | 627.8, 4.09 | yes |
| Owner-occupied houses without PV 1 Sep 2026 | 4,537 / 1,857 | 4,537 / 1,857 | yes |
| Bulk-buy systems | 185.6 / 76.0 | 185.6 / 76.0 | yes |
| Average new inverter YRB24 / YRB27 | 9.15 / 9.35 kW | 9.149 / 9.348 | yes |
| Bulk-buy MW | 1.7 / 0.7 | 1.698 / 0.710 | yes |
| YRB27 excess (PV 16.1 MW) | 1.9 MW | 1.900 | yes |
| YRB24 excess | 1.7 MW | 1.696 | yes |
| Gap | 0.2 MW | 0.204 | yes |
| Bay factors | 1.25/1.6/1.2/1.5 (FDR21-24), 1.5/1.2/1.6/1.25 (FDR25-28) | fitted 1.2504/1.5996/1.1996/1.4997; 1.4987/1.2004/1.5998/1.2507 | yes |
| Ask 6 YRB21 | 1,030 / 980 / 1,140 MWh; 12.0 MW | 1027.6 / 978.7 / 1142.7; 11.965 | yes |
| Ask 6 YRB22 | 850 / 810 / 960; 10.8 | 853.4 / 808.0 / 958.4; 10.768 | yes |
| Ask 6 YRB23 | 280 / 280 / 340; 5.4 | 282.4 / 283.4 / 342.5; 5.381 | yes |
| Ask 6 YRB24 | 660 / 620 / 750; 9.2 | 662.6 / 618.0 / 752.4; 9.202 | yes |
| Ask 6 YRB25 | 870 / 820 / 980; 11.2 | 870.9 / 821.1 / 978.9; 11.217 | yes |
| Ask 6 YRB26 | 220 / 210 / 260; 4.5 | 217.0 / 213.0 / 262.0; 4.502 | yes |
| Ask 6 YRB27 | 130 / 150 / 190; 3.7 | 133.1 / 146.9 / 187.0; 3.678 | yes |
| Ask 6 YRB28 | 710 / 670 / 820; 9.0 | 711.0 / 673.0 / 818.7; 8.964 | yes |

Thin margins (thread): max half hour YRB21 11.965 (0.015 over the 11.95 boundary), YRB28 8.964 (0.014 over 8.95), YRB26 June 216.95 MWh (1.95 over 215). Safe against the 0.03 percent factor fit error; thin only if someone rounds a rounded factor.

## Competing answers that survived
- Fork 1 (residual, soft): gross program installs instead of an incremental effect. Program_ref systems (1,431) are 2.3 times the campaign effect (627.8). Gross, or a naive pre-rate scaling (5.94 per hundred), puts YRB24 on top; the summary's gross rate (about 4.8 percent installed per letterboxed home) gives YRB24 about 4.6 MW against YRB27 about 1.4 MW of uplift. NPP-114 4.1 ("impact on the feeder's connected capacity") and the prompt ("raise its feeder's PV") read as the net effect. Judged not a licensed alternative; it is the stump, flagged by the thread as the one soft spot.
- Ask 6, historian as recorded (factors of 1): Jun/Jul/Aug MWh and peak MW: YRB21 822/783/914, 9.6; YRB22 533/505/599, 6.7; YRB23 235/236/285, 4.5; YRB24 442/412/502, 6.1; YRB25 581/547/653, 7.5; YRB26 181/177/218, 3.8; YRB27 83/92/117, 2.3; YRB28 569/538/655, 7.2. The check meters are missed by 4.4 to 4.8 MW rmse (max 10 to 11 MW), so the recorded historian cannot be the true flow; no shipped sentence calls the meter authoritative, but the thread rules this a stump, not a fork.
- Ask 6, month by interval end: identical figures. Net monthly energy instead of reverse half hours: zero for every feeder, not licensed by "any energy it sent back". Average inverter over all connected applications (8.776 / 9.054 kW) would give 1.9 / 1.6 / 0.3 but NPP-114 4.3 says "first connected": closed. Withdrawn applications excluded by the filed "non-withdrawn": closed.
- Note for the main thread: the ask names no SCADA or meter file, so reaching the check-meter reconciliation is part of the analysis; the files give no other usable second reading.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, rows | 10+ files, 3+ formats, one 25,000+ rows | 15 files; csv, xlsx, pdf; rates roll 64,795 rows (metadata; thread counted 64,796 with header), applications 27,855, network model 62,991 | yes |
| Distractors | 2+ in metadata.json, none named in a file name | 4 named: feeder_peak_demand_forecast_2027-31.xlsx, home_battery_rebate_approvals_fy2025-26.csv, der_register_extract_yarrabin_20260901.csv, nmi_reallocations_2019-2026.csv; no file name labels one | yes |
| Distractor use | unused by the solution, relevant, ruled out by a shipped fact | the thread named three (battery, peak demand, DER register) and called the reallocation file Layer 1 key mess; metadata files it as a distractor. Thread found nothing answering a graded quantity from any of them | yes, see finding 3 |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | ask 6 is 8 feeders x 4 figures with nearest 10 MWh and one decimal MW in the prompt sentence | yes |
| Prompt shape, rubric 25+ criteria | identifiable, 25+ | shape "other", declared in metadata; rubric count not verifiable from the folder by me | not verified |
| Reads as real work product | no LLM tells | thread found no authoring or benchmark text in metadata; in-fiction authors; dates coherent with the 1 Sep 2026 snapshot | yes |

(The thread's hygiene line miscounts formats: the bundle has 10 csv, 2 xlsx, 3 pdf. No consequence.)

## Gate G reconciliation
Thread: mechanism method_or_model_selection plus etl_conformance/reconciliation, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Layer 2 is estimand_identification (staggered adoption, not-yet-treated comparison), decisive step the control-adjusted bulk-buy uplift, 4.09 per 100 against 9.32 installed (gross) and 5.68 on the suburb's own before and after; the shortcut files YRB24. Match: the thread found the same trap, the same easy-route wrong answer (YRB24) and the same sole-defect verdict. No declared distractor was named as carrying the task; the DER register extract and re-allocation log play no part in any figure. Ask 6 is a Layer 1 ETL reconciliation (design note lists the start/end labelling and per-bay scale as Layer 1 on the ask path) and the asks are free of the three rules, so the thread's calling it a stump on the ask side is consistent with the note.

## Gate H
Thread: domain pass, layers pass, decisive_step analytical. Design note `## Three rules` (Domain test, Layer 2 estimand_identification, No decoy, Not semantics, Not rule application) consistent. The metadata gives no stump_class, analyst_test or domain_test (card not located in the task folder); the design note's analyst test (strong analyst reaches YRB24 at 3.7 to 5.0 MW or 2.4 to 2.6) matches the thread's easy route (YRB24 with 3.9 MW or more of uplift). Match.

## Stump power (Gate F)
Thread: good, two independent traps. (a) Gross program installs or naive scaling puts YRB24 on top; only the control-adjusted difference-in-differences gives YRB27, by a thin 0.2 MW. (b) A solver on the raw historian misses every ask 6 figure. The decisive step is not the field's standard textbook route landing by itself: the thread did not class it analytical merely because the method is standard. The thin 0.2 MW gap is itself the pressure on a solver who gets the uplift nearly right. The main thread weighs this against the ladder; the estimate stays within 4.05 to 4.19 per hundred for every defensible variant, so the gap is determinate and not a coin flip.

## Findings, ranked
1. Soft spot, not a block: fork 1, the gross-versus-net reading of "raise its feeder's PV". The thread recommends against a pin ("incremental to the underlying trend") because it would hand over the stump; I concur, since filing it names the HOW.
2. Ask 6 margins are thin at three values (YRB21 peak 11.965, YRB28 peak 8.964, YRB26 June 216.95), safe under the fitted factors and under the round factors; no action.
3. Metadata lists nmi_reallocations_2019-2026.csv as a distractor while the design note's Layer 1 and the thread treat it as key mess; the rubric of what makes it a distractor (unused by the solution, ruled out by a shipped fact) held in the thread's recomputation. Confirm the fiction intent only if the author wants consistency.
4. Rubric criteria count not verified by this pass.

## Next action for the author
None required for determinism: ship (or proceed to the remaining stage 4 gates). Optionally confirm the rubric reaches 25 or more criteria.

## Judge thread verdict (verbatim, /tmp/determinism-check-task136-r40528/verdict.md)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. Every graded figure reproduced from the shipped files, with no repair needed and no model rerun. One residual exposure is on the bulk-buy estimand (see Evidence, fork 1).

**Why:** The main call and asks 1-5 follow from NPP-114 rev 3 (connected capacity, three-year trend less program systems, programs confirmed in writing, spring-2029 hosting capacity, largest excess wins). Everything the filed text leaves open (the bulk-buy uplift estimator, the control set) lands on the same rounded figures across every difference-in-differences variant I ran (4.05 to 4.19 per hundred). The new reverse-flow ask (ask 6) has exactly one reading that the files support. The check meters fit the historian only with the per-bay factors, and the month and half-hour boundaries change nothing.

**Evidence (recomputed from target/ only; all reproduced):**
- Connected capacity at 31 Aug 2026, by the network-model feeder, latest connected configuration per NMI, legacy kW taken from legacy_inverter_equipment.csv, removals excluded:
  - YRB27 11,645 kW and YRB24 17,845 kW (17,844.8) match.
  - Others: YRB21 18,706; YRB22 18,531; YRB23 11,954; YRB25 21,255; YRB26 11,808; YRB28 16,554.
- Trend (FY24-26 average increase less program systems first connected in the year): YRB27 1,245.0 and YRB24 1,934.6 match. Base forecasts 15,380 and 23,648 match.
- Excess over the 2029 spring hosting capacity before the bulk-buys:

| Feeder | Excess (MW) |
|---|---|
| YRB22 | 1.395 |
| YRB27 | 1.190 |
| YRB25 | 0.971 |
| YRB21 | 0.859 |
| YRB28 | 0.716 |
| YRB23 | 0.435 |
| YRB24 | -0.001 |
| YRB26 | -0.656 |

- Campaign uplift:
  - Houses without PV at opening sum to exactly 15,349 across the 7 campaigns.
  - Control set: the later-campaign suburbs plus the never-campaigned suburbs; ratio form (campaign pre-rate times the control post/pre ratio). This gives 627.8 added systems, 4.09 per hundred.
  - Houses without PV at 1 Sep 2026: Bindarra Waters 7,065 less 2,528 = 4,537; Wattleview 2,828 less 971 = 1,857.
  - Average first-connected inverter, FY25-26: YRB24 9.149 kW, YRB27 9.348 kW.
  - Result: Bindarra Waters +185.6 systems = 1.698 MW; Wattleview +76.0 = 0.710 MW.
  - Final excess: YRB27 1.900 MW, YRB24 1.696 MW, gap 0.204, then YRB22 1.395. This gives 1.9 / 1.7 / 0.2 and bulk-buy adds 1.7 / 0.7, with YRB27 PV 16.1 MW.
- Estimator robustness:
  - Across control sets (later-campaign only, plus never-campaigned, never-campaigned only) and across ratio, difference and control-rate forms, the rate is 4.05 to 4.19 per hundred. At 4.05 the figures are 1.893 / 1.680; at 4.15 they are 1.910 / 1.721. Rounded figures and the gap of 0.2 are unchanged in every case.
  - YRB24 and YRB27 tie only at about 4.94 per hundred. YRB22 overtakes YRB27 only below about 1.2 per hundred.
- Forks considered (the first is residual; the rest are closed):
  1. Gross program count instead of an incremental effect. The program_ref systems (1,431) are 2.3 times the campaign effect (627.8). Non-program first applications in campaign suburbs fall below their pre-year pace, so gross overstates the effect. Gross, or a naive pre-rate scaling (5.94 per hundred), gives YRB24 on top. A gross rate from the summary (installed per letterboxed home, about 4.8 percent) applied to 10,477 and 3,117 addresses puts YRB24 about 4.6 MW against YRB27 about 1.4 MW of uplift. NPP-114 4.1 ("impact on the feeder's connected capacity") and the prompt ("raise its feeder's PV") read as the net effect. The trend is not rule-bound to be net of displacement, but "raise" is the literal estimand. Judged not a licensed alternative; flagged as the one soft spot.
  2. Average inverter over all connected applications including alterations: 8.776 and 9.054 kW. This would give 1.9 / 1.6 / 0.3, but NPP-114 4.3 says "first connected", and New-only gives 9.149 and 9.348. Closed.
  3. Withdrawn applications are excluded by the filed term "non-withdrawn". Closed.
- **Ask 6 (reverse flow).** Sign: negative historian value = feeder back into the 22 kV bus (the fitted coefficients are positive against meter import less export). The two buses are fitted on the meter side with a 30-minute offset: the historian is labelled interval_start_aest, and the meter is labelled interval_end_aest, closing the half hour that starts 30 minutes earlier.
  - With that alignment the meter equals the sum of the four historian values times a per-bay factor to rmse 0.011 MW (max 0.06). The fitted factors are 1.2504 / 1.5996 / 1.1996 / 1.4997 for FDR21-24 and 1.4987 / 1.2004 / 1.5998 / 1.2507 for FDR25-28, in effect 1.25 / 1.6 / 1.2 / 1.5 / 1.5 / 1.2 / 1.6 / 1.25. Aligned the other two ways (start to start shifted one way, or the other), rmse is 3.6-3.8 MW, so the boundary reading is unique.
  - With every factor at 1 (the historian as recorded), the check meters are missed by an rmse of 4.8 and 4.4 MW (max 10-11 MW). The recorded historian cannot be the true flow.
  - Feeder-head reverse energy is sum(max(-value x factor, 0) x 0.5) by month, with the month taken from the interval start. The same totals come out if the month is taken from the interval end, because no reverse flow occurs at any midnight boundary (solar hours only). Aug 31 23:30 and Sep 1 00:00 carry none, so Sep is 0. All figures are on AEST labels with no DST gap.

| Feeder | Jun / Jul / Aug (MWh, exact factors) | Rounded to 10 | Max half hour (MW) | Golden | Matches |
|---|---|---|---|---|---|
| YRB21 | 1027.6 / 978.7 / 1142.7 | 1030, 980, 1140 | 11.965 → 12.0 | 12.0 | yes |
| YRB22 | 853.4 / 808.0 / 958.4 | 850, 810, 960 | 10.768 → 10.8 | 10.8 | yes |
| YRB23 | 282.4 / 283.4 / 342.5 | 280, 280, 340 | 5.381 → 5.4 | 5.4 | yes |
| YRB24 | 662.6 / 618.0 / 752.4 | 660, 620, 750 | 9.202 → 9.2 | 9.2 | yes |
| YRB25 | 870.9 / 821.1 / 978.9 | 870, 820, 980 | 11.217 → 11.2 | 11.2 | yes |
| YRB26 | 217.0 / 213.0 / 262.0 | 220, 210, 260 | 4.502 → 4.5 | 4.5 | yes |
| YRB27 | 133.1 / 146.9 / 187.0 | 130, 150, 190 | 3.678 → 3.7 | 3.7 | yes |
| YRB28 | 711.0 / 673.0 / 818.7 | 710, 670, 820 | 8.964 → 9.0 | 9.0 | yes |

  - Using the least-squares fitted factors instead of the round ones gives the same rounded figures. The closest margins are max half hour YRB21 11.965 (0.015 over a 11.95 boundary), YRB28 8.964 (0.014 over 8.95) and YRB26 216.95 MWh (1.95 over 215). These are safe against the 0.03 percent factor fit error, but they are thin if someone rounds a rounded factor.
  - **Second readings the files support:**
    - The historian as recorded, if the solver never reconciles to the meters, gives:

| Feeder | Jun / Jul / Aug (MWh) | Max (MW) |
|---|---|---|
| YRB21 | 822 / 783 / 914 | 9.6 |
| YRB22 | 533 / 505 / 599 | 6.7 |
| YRB23 | 235 / 236 / 285 | 4.5 |
| YRB24 | 442 / 412 / 502 | 6.1 |
| YRB25 | 581 / 547 / 653 | 7.5 |
| YRB26 | 181 / 177 / 218 | 3.8 |
| YRB27 | 83 / 92 / 117 | 2.3 |
| YRB28 | 569 / 538 / 655 | 7.2 |

      No shipped sentence says the check meter is authoritative, but its own name and the unit-factor misfit of 10 MW exclude this reading for an expert. It is a stump, not a fork.
    - Month by interval end instead of start: identical figures (shown above).
    - Net monthly energy instead of the sum of reverse half hours: zero for every feeder, since the filed wording is "any energy it sent back"; not licensed.
    - The ask names no SCADA or meter file, so reaching the check-meter reconciliation is part of the analysis. The files give no other usable second reading.
- Both bay-factor and boundary readings are therefore single.

**Files/Hygiene:** PASS. Fifteen files in three formats: 11 csv, 2 xlsx and 3 pdf (note: the program and demand-forecast spreadsheets are the two xlsx; the NPP, hosting-capacity and council letter are the pdf). The largest files are eg_connection_applications (27,855 rows), the rates roll (64,796) and the network model (62,991). Distractors: home_battery_rebate_approvals, feeder_peak_demand_forecast (thermal rating/MVA, unused by the solution), der_register_extract (a second register not needed). Metadata authors are named in-fiction (Fletcher, Cochran, Buchanan), with no authoring or benchmark text. Dates are coherent with the 1 Sep 2026 snapshot. No exclusion-level finding. The 43 removed applications on NMIs absent from the model are uncounted and harmless. The reallocation file is a Layer-1 key mess.

**Stump power:** Good, from two independent traps. (a) Gross program installs or a naive scaling of the pre-year rate puts YRB24 on top (4.6 MW against 1.4 MW of uplift, or a 5.94 per hundred rate), while only a control-adjusted difference-in-differences gives YRB27 by 0.2 MW. (b) The reverse-flow ask turns on the historian scaling that only the check-meter reconciliation reveals; a solver on the raw historian misses every figure. A strong model that computes the incremental uplift correctly still has a thin 0.2 MW gap to hold.

**Stumping type:** mechanism: method_or_model_selection (causal uplift estimator with a control group; plus etl_conformance/reconciliation for ask 6); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. The summary's installed-systems counts are accurate but are not the effect; the difficulty is choosing the right estimand on honest data, and it would persist on perfectly clean data.

**Three rules:** domain: pass, layers: pass, decisive_step: analytical. Layer 1: legacy-system migration, NMI reallocations, financial-year trend, interval-start versus interval-end timestamps, historian-to-meter scaling. Layer 2: NPP-114 distribution planning, with the program impact estimated against a comparison group. The easy route (counting the program's installed systems, or scaling the pre-campaign pace) gives YRB24 as the call, with 3.9 MW or more of uplift instead of 1.7 MW.

**Fix:** none. Optional hygiene: none. (A one-line prompt pin of "incremental to the underlying trend" would close fork 1, but it would hand over the stump; not recommended.)
