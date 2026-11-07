# determinism-check report, task482 (architecture 16), 2026-10-31

Target.zip sha256 433ff500dd8e84b789b2ac3f42cdb0060c6f1b351b9fce363f62eb7b8c81b6ed. One judge thread, one pass, scratch /tmp/determinism-check-task482-1793487403/ (verdict at verdict.md there). Earlier architectures' reports (determinism_check_report_arch14.md, determinism_check_report_arch15.md) are untouched.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE. No repair and no rerun. One optional, advisory prompt pin: state the precision of the emissions-per-tonne figures (for example "to two decimals"). It is not needed for the call.
**Stumping type:** mechanism: method_or_model_selection (disaggregation of a metered fuel by process activity, validated by fit), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The premium turns on which families are at or under 0.235 t CO2/t. Every defensible way of attributing the metered gas to the processes gives the same split: 6063 and LM25 ingot under the limit, 6082 and the castings over it. SCR-2 s.3 and s.4 give the attribution rule, the gas energy basis and the factor; the 15-minute meter file, the invoices (calorific value per period), the process logs and the lots file supply the data. The premium is EUR 38 x (7,200 + 1,800) t = EUR 342,000. The easy route (all gas shared by tonnes) gives 0.2215 for every family, all four qualify, 12,650 t, EUR 480,700. No gate A to E failure was found for the main call or the scrap asks. Only soft spot: the unrounded emissions figures (recorded residual below).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Gas kWh (UTC to Europe/London, hcf x 2.83 before the 14 Apr exchange, x 1.02264 x CV of invoice period) | per invoice PDF | within about 20 kWh in 11 of 13 invoices (1 to 22 kWh, rounding); first and last straddle year ends | Yes (meter csv, invoices pdf) |
| 2026 gas total | n/a | 55.65 GWh, 10,181 t CO2 | Yes |
| Production, last result PASS | 22,897 / 8,205 / 12,816 / 2,044 | 22,896.7 / 8,204.9 / 12,815.9 / 2,044.0 (39 re-inspected lots once each) | Yes (lots csv) |
| H1 hours, 6082 share | 47 per cent of hours on 26 per cent of billet | 2,538 of 5,354 h (47.4%) on 26.3%; 6082 loads 15.0 h, 6063 6.0 h | Yes (H1 csv) |
| Emissions t CO2/t, daily regression (R2 0.9985) | 0.21 / 0.26 / 0.17 / 0.50 | 0.2115 / 0.2628 / 0.1686 / 0.4999 (6063 / 6082 / LM25 / castings) | Yes to two decimals under the filed method |
| Call-offs | 7,200 / 3,000 / 1,800 / 650 t | 4,320 + 2,880 = 7,200; 3,000; 1,800; 650 | Yes (call-off xlsx) |
| Premium | EUR 342,000 | EUR 38 x 9,000 t | Yes |
| Scrap by grade and quarter (CST / EXT / TRN / UBC) | Q1-Q4 as golden | exact: CST 2,186 / 2,214 / 2,121 / 2,299; EXT 2,299 / 2,110 / 1,773 / 2,041; TRN 2,024 / 1,845 / 2,200 / 2,188; UBC 2,376 / 2,521 / 2,009 / 2,020 | Yes (goods-in, weighbridge) |
| Dross, Midland waste-out | 286 / 262 / 251 / 270 | 285.7 / 261.6 / 251.1 / 269.6 | Yes |

Method variants, none flips a decision: without HDD 0.211 / 0.264 / 0.166 / 0.520; by-alloy melt coefficients 0.211 / 0.263 / 0.169 / 0.501; 6-hourly regression 0.214 / 0.265 / 0.172 / 0.441; hourly regression 0.218 / 0.271 / 0.174 / 0.356; rated kW x hours from the asset register (distractor route) 0.199 / 0.280 / 0.138 / 0.769. Margins about 0.025 on both billet alloys.

Wrong routes: all gas by tonnes gives 0.2215 for every family (EUR 480,700). H1 gas shared by tonnes instead of hours gives 6063 0.2250 and 6082 0.2251, both qualify, EUR 387,600. The golden call needs the hours-based H1 attribution.

Scrap ticket join: tickets restart on 29 June; rank-matching and min-cost matching agree on all 846 two-grade drops, no ties; rejected and returned loads net about 0 kg. Dross weighing sequence data-confirmed (first less second weighing equals the declared returned-metal weight within about 110 kg).

## Competing answers that survived
None that change a graded figure or the call. Recorded residual, non-flipping:
- **Emissions precision (recorded residual).** The prompt rounds tonnes and premium only, so the emissions per tonne are unrounded. The castings figure moves with the regression design (0.36 to 0.52, always over 0.235); 6063 sits at 0.21 to 0.22 and 6082 at 0.26 to 0.27, so the two-decimal values are method-dependent at the second decimal. The call is unaffected. Optional pin: "to two decimals" in the prompt.
- Log time zone is not stated anywhere; inferable (gas pattern correlates better with logs on a local clock; SCR-2 s.6 says local). Non-flipping.
- Toll-return sows are excluded as "not bought in"; the golden's four grades follow the prompt wording. Non-flipping.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats | 10+ files, 3+ formats | 15 files; csv 10, xlsx 3, pdf 2, eml 1 (4 formats) | Yes |
| Large file | 25,000+ rows | meter file 35,040 rows | Yes |
| Distractors | 2+ in metadata.json, none named in a file name | 3 in metadata.json (electricity half-hourly, plant asset register, shift roster); the judge also names the despatch weighings and the asset register's electrical sheet as unused material; none labelled in a file name | Yes |
| Distractors unused yet weighable | rule-out by a shipped fact | asset register rated kW x hours is a plausible wrong route (0.199 / 0.280 / 0.138 / 0.769, same split as the call) and does not answer the graded quantity | Yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, csv), both in golden/ | Yes |
| Asks | multi-dimensional, unit and rounding stated | scrap 4 grades x 4 quarters plus dross by quarter; tonnes and euro rounding in the prompt | Yes (precision of emissions per tonne not stated; residual above) |
| Rubric 25+ criteria | prompt shape identifiable | not checked in this pass (rubric is generated; shape is a per-family, per-quarter, per-grade grid, 36+ gradable figures) | Not verified here |
| Reads as real | no LLM tells, goldens real | judge found no authoring or benchmark language; real-export mess present | Yes |

## Gate G reconciliation
Thread's line: mechanism method_or_model_selection; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. Gate H line as the thread gives it: **domain: pass, layers: pass, decisive_step: analytical.**
Card (task482.json): stump_class analytical, analyst_test and domain_test present; the design note's Three rules lines and Stump sentence name the same decisive step (the homogenizing furnace's gas by loads' firing hours, 6082 at 47 per cent of hours on 26 per cent of billet). Match. The declared distractors (electricity, asset register, roster) are not named by the thread as the surface read carrying the task; the thread's surface-read answer is the tonnes-share route, so no "distractor too load-bearing" finding. One numeric difference to note, not a mismatch of type: the card and the design note state the default path at EUR 456,000 (billet alloys level at 0.225); the thread's recomputations give EUR 480,700 for all-gas-by-tonnes and EUR 387,600 for H1-by-tonnes with the rest regressed. The design note's EUR 456,000 was not reproduced by the thread under either route, so the stated default-path premium should be re-derived before it is quoted anywhere. It does not touch the golden.

## Stump power (Gate F)
Moderate to high. The trap is the attribution step: SCR-2 s.3 attributes each process the fuel it burned, but there is no sub-metering, so the single gas meter must be disaggregated by regression on process activity. The tonnes-share route files the wrong qualifiers; so does H1 by tonnes. The ETL layer (UTC to local, hcf to m3, CV per invoice period, de-duplicating heats, last-result production) adds ways to be quietly wrong. Nothing in the package pre-answers the trap. The thread did not class the decisive step analytical merely because regression is standard; it reached the golden by choosing hours for the soak furnace, which the data separate (R2 0.9985). The main thread weighs the standard-method note (library methods are textbook routes a strong solver takes, stumping 1.3) against the design note's ladder.

## Findings, ranked
1. Residual, advisory: emissions per tonne are unrounded and method-dependent at the second decimal (castings 0.36 to 0.52). Does not flip any family. Optional prompt pin.
2. Note and card quote EUR 456,000 as the default-path premium; the thread could not reproduce it (480,700 and 387,600 are the recomputed wrong routes). Documentation only.
3. Log time zone inferred, not stated. Non-flipping.
4. Rubric criteria count not verified in this pass.

## Next action for the author
None required for the call. Optionally add "to two decimals" for the emissions-per-tonne figures to the prompt (a prompt change would reopen voice-check and the byte-identical rebuild) and re-derive the EUR 456,000 default-path figure in the note and card.
