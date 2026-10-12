# Determinism verdict, task501b

- **Verdict:** NOT_DETERMINISTIC (main recommendation and the dependent fee asks 2 and 3; the distributions asks are DETERMINISTIC and reproduce).
- **Disposition:** SEND_BACK. The expected-calls model has to be pinned by the shipped files (or the margin widened), which changes what solvers see; a rerun is required.
- **Why:** CHF 225 million is the answer only if expected 2027 calls fall in a band of about 318 to 341 million (about 3.5 per cent either side of the golden 329). Nothing in RL-PM-05 or the prompt fixes the forecast model (section 5.2 says only "the programme's own records ... over the programme's whole history"), and the data does not separate the competing models. Gates C/E fail. Taxonomy: margin_or_boundary_fragility (also underspecified_objective on the plan basis).

## Evidence: recomputation ledger
| Item | Reproduced | Source |
|---|---|---|
| Reference rates 31.12.2026 USD 0.7906, EUR 0.9339 | yes | fx_referenzkurse_tagesende.csv |
| 2026 calls carried forward CHF 310.0 m (issued lines, value date, plan-date rates) | yes, 310.04 | kapitalabrufe csv |
| 27 funds with investment period ended: drawn 92.2 to 93.3 per cent at period end, mean 92.6 | yes (92.22 to 93.26, 92.65) | csv + fondsregister |
| Age-band call rates on unfunded (12-month bands from first call, pooled since 2015) give CHF 236.1 m, four funds CHF 79.7 m | yes, 236.12 / 79.67 | csv + register |
| Golden model (ten funds complete to 92.6 per cent by period end, band rate elsewhere) CHF 329.3 m, four funds 170.1 m | approx. 329.0 / 169.9 (timing within the year not specified); 92.2 to 93.3 target gives 325.1 to 333.6 | same |
| Requirement 329.3 x 1.1 - 150 = 212.2; menu step 225 | yes arithmetically; 225 is right for calls 318.2 to 340.9 only | term sheet, RL-PM-05 s4 |
| Fees 225: 0.30% = 675,000, 0.15% = 337,500, total 1,012,500; 200: 600,000 + 300,000 = 900,000 | yes | term sheet |
| Covenants (NAV at least 900 m; 225 at most 25% of NAV) | satisfied, NAV about 1.23 to 1.42 bn | nav_register_quartal.csv |
| Ledger cumulative calls equal audited contributions at FY2025 for all 48 funds | yes (no hidden gap) | kapitalkonten xlsx |
| Distributions 2026 by strategy and quarter (match credits by Transaktionsreferenz else keyed notice number in Referenz; cash lines only; rate of Valuta) | yes, all 20 cells and quarter totals 92,183 / 62,803 / 70,260 / 86,537; Buyout 91,926 leads (Infrastructure 87,524) | programmkonto csv + ledger + fx |

All 353 credits match a notice; 52 credits carry a Referenz pointing to a Q4 2025 keyed twin of the same distribution, which is why Transaktionsreferenz is used. Implied CHF/notice rates deviate from the reference rate only 0 to 0.35 per cent, so the matching is robust.

## Competing answers (Gate C), all built from the shipped files
| Model for expected 2027 calls | Calls CHF m | Requirement | Facility |
|---|---|---|---|
| Age-band rate on commitment (pooled, whole history) | 219 | 91 | 100 |
| Age-band rate on unfunded (golden's "wrong" path) | 236 | 110 | 125 |
| Rate on unfunded by time-to-period-end band | 253 | 128 | 150 |
| 2026 calls carried forward | 310 | 191 | 200 |
| Golden: completion to 92.6% for the ten, band-on-unfunded for the rest | 329 | 212 | **225** |
| Same completion step, but the other funds on age-band rate on commitment | 349 | 234 | **250** |
| Same completion step, other funds on time-to-period-end band | 332 | 215 | 225 |

The fork that matters: once the period-end completion for the ten funds is accepted, the choice of base for the remaining ~38 funds (rate on unfunded vs rate on commitment) moves the total by about 20 m, across the 341 m line, and the answer becomes CHF 250 m. Back-tests do not choose between them: rate on unfunded errs +15.7, +20.6, +4.6, +0.9 per cent (plan dates 2022 to 2025), rate on commitment errs +43.8, +25.3, -0.4, -2.1 per cent (2023 to 2026 outcomes: better in the two latest years, worse in the two earlier). The golden's own step 3 justification ("the basis RL-PM-05 sets") overstates the directive, which names neither unfunded nor commitment as the base. The expected-calls margin is 3.5 per cent while the filed back-test errors are 1 to 20 per cent: thin and contested, not thin and clean. The selection of "pooled since 2015 on unfunded" is not forced by anything shipped.

The period-end completion insight itself (27 funds at 92.2 to 93.3 per cent, five at 50 to 70 per cent a year before) is well supported by the data and is a genuine analytical finding; the weakness is that the rest of the forecast is left to an unforced choice that is as large as the margin.

## Files/Hygiene
PASS, no exclusion-level finding. 13 shipped files, formats: csv (5), xlsx (2), docx, pdf (3), txt, json, md. Business-realistic, consistent dates (extract produced 5 Jan 2027, mail 6 Jan 2027), no authoring disclosures seen, no public-dataset contamination. Both the directive and the cover mail are tidy but plausible. Distractors (look_through_bestaende, kapitalkonten, halbjahresbericht, nav_register) are relevant and unused. Minor: the half-year report is for a period before the setting and harmless.

## Stump power (Gate F)
The completion-to-92.6-per-cent-at-period-end step against the "age-band rate" path is a real trap a capable analyst would fall into (125 or 200), so the main stump would plausibly work. The difficulty is not clean however: runs that find the period-end effect but model the rest differently land on 225 or 250, a model-choice split rather than an error.

## Stumping type (Gate G)
`mechanism: forecasting` / method_or_model_selection, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Honest data, forecast the trailing figures do not pin; passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Commitment pacing and drawdown forecasting for a liquidity facility is the field's own estimation work; the easy route (age-band call rate, or last year's calls) gives 125 or 200. Layer 1 (cancelled/reissued notices, mixed currency case, twin DN/PM notices, FX-day conversion) is realistic mess; Layer 2 is the period-end completion pattern. The distribution asks lean on data semantics and matching, acceptable as asks.

## Fix
Location: input_files and prompt. Pin the expected-calls basis so one model is literal (for example state in RL-PM-05 s5.2 the base and banding, or file a selection criterion with a back-test that actually separates the candidates, covering the non-ten funds), or move the golden so the requirement is not within 20 m of a menu step under the defensible variants (the 349 and 253 variants must land on the same menu step as the golden). Distributions asks and fee mechanics need no change.
