# Determinism check, task269 (architecture 4)

The isolated judge thread (Sonnet, medium) saw a fresh unzip of target.zip and the submission's graded blocks only. Its verdicts follow as written, round by round.

## Round 1 (2026-10-25, target.zip e869069b)

**Verdict:** NOT_DETERMINISTIC (taxonomy: competing_defensible_answer; fix location: prompt, with a filed estimand)

**Disposition:** SEND_BACK. The class-level estimand for the single-family roll has to be filed in the prompt or Rule 18-7 (what stands for the 93.3% of parcels that did not sell, and how the sold parcels enter). That changes what solvers see, so a rerun is required.

**Why:** Read word for word, Rule 18-7 (2.1, 3.1, 3.2) gives single-family 0.95 and COD 8.0 on 1,698 sales. That meets the rule, so the county would decline the offer, and the rule says "Ratios are not otherwise trimmed". The golden (0.87, 18, fails, accept) comes from a method no shipped file states. It takes each sale's 2025 value times its neighbourhood's median change among unsold parcels, rounds to 100, and then weights that proxy set at 93.3% against the sales' actual 2026 ratios at 6.7%. The call direction survives every proxy variant I tried. The two graded single-family figures at the requested rounding do not (see Evidence). Affected: main recommendation (literal reading flips it) and the two single-family figures in reappraisal_recommendation.docx.

## Evidence (recomputed from target/)
| Item | Golden | Mine | Reproduced |
|---|---|---|---|
| R1 Q-deed sales matched to roll | 1,742 | 1,742 | yes |
| Set aside by permit finaled after deed | 44 | 44 | yes |
| Literal sales study (n, median, COD) | 1,698, 0.95, 8.0 | 1,698, 0.9519, 8.007 | yes |
| Sold-parcel 2025 to 2026 change, median | 14.9% | 14.93% | yes |
| Unsold-parcel change, median | 3.4% | 3.40% | yes |
| R1 parcels on 2026 roll | 25,988 | 25,988 (6.7% sold) | yes |
| Golden R1 median, COD | 0.87, 18 | 0.8697, 17.99 | yes, under the golden's own method |
| Condo n, median, COD, PRD | 149, 0.93, 7.3, 0.998 | 149, 0.9310, 7.277, 0.9981 | yes |
| Board of Review, market areas 1 to 6, parcels | 132/156/171/94/166/152 | same | yes |
| Board of Review, dollars, market areas 1 to 6 | 4,349,600 / 5,656,500 / 6,564,800 / 3,402,200 / 7,095,200 / 6,109,300 | same | yes |

**The fork on the single-family figures.** All variants below use the shipped data.
- Literal Rule 18-7 sales study: 0.95 and 8.0, meets, so decline. This is what a word-for-word executor files.
- Golden: weight 6.7% for the sold parcels at their actual 2026 ratios, 93.3% for the proxy ratios: 0.8697 and 17.99, so 0.87 and 18.
- Proxy ratios only, sold parcels' actual 2026 values given zero weight: 0.8569 and 18.65, so **0.86 and 19**. Nothing filed excludes it, and it is the simplest correction of the sales-chasing.
- Weight 5% on the sold parcels: 0.8662 and 18.17, so 0.87 and 18. Weight 10%: 0.8775 and 17.61, so 0.88 and 18.
- Neighbourhood mean, market-area, countywide or all-parcel factors: 0.867 to 0.871 and about 18.0.
- Naive 50/50 pooling of the two ratio sets: 0.92 and 13.4, which meets the rule (a wrong method, not a defensible one).

The pass/fail call holds in every proxy variant except naive pooling. The graded 0.87 and 18 flip to 0.86 and 19 on the zero-weight choice, and no filed rule or selection criterion separates the candidates. The shipped text also never signals that sold parcels were revalued after sale. Only the 14.9% against 3.4% contrast, which the solver has to find, shows it.

**Other committed answers.**
- Condominium: the 153 naive matches (0.94, 16.0, fails) fall to 149 once the 2025-07-01 Wexley Commons renumbering is resolved. Pre-effective-date deeds written at old numbers now point to different units, and 5 COMBINE deeds are set aside because the boundaries changed. This is unique and follows the rule, but it is data semantics. It is acceptable as an ask.
- Board of Review: hearings whose value_before equals the certified 2025 value, last hearing per case, reduction = before minus after. The 12 two-hearing cases are all REDUCED at the last hearing, and the second value is taken from the original value_before, so it is not cumulative. Counting every REDUCED row instead gives 158/95/155 in areas 2, 4 and 6, which is defeated by the "parcels reduced" wording. Acceptable.

## Files/Hygiene
PASS. 13 files (csv x6, xlsx x2, pdf x2, txt x1; the formats number four with the csv/xlsx/pdf/txt mix). The roll is 25,988 R1 rows, which meets the row floor. The distractors are homestead_credits_2026.csv and levy_and_rates_fy2026.xlsx, and the memo explicitly sets them aside. The 2025 xlsx export has the legacy report header and run stamp. Dates are coherent (a 14 September 2026 memo, an offer open to 30 October). I found no authoring leakage and no benchmark disclosure. Nothing is exclusion-level.

## Stump power (Gate F)
A strong solver who follows Rule 18-7 as written files 0.95 and 8.0, meets, decline. That is the wrong call. The easy route is the one the rule prescribes, and nothing in the files names sales-chasing, so the main trap is real and strong. A solver who spots the sales-chasing then splits on how to reconstruct the unsold population (the fork above). The Wexley identifier reuse and the 44 permit set-asides are Layer 1 and do not decide the call.

## Stumping type (Gate G)
`mechanism: statistical_rigor` (selection bias / sales-chasing), `stumping_family: analytical_non_defect` (borderline), `surface_read_dependency: no`, `sole_data_defect: no`.
The sales study is arithmetically correct and the difficulty is estimating the whole class from a non-representative sample. On clean data without the post-sale revaluation there would be no stump, because the rule's literal method would then give the right answer. The post-sale revaluation is an engineered feature of the data, so I call this borderline and route it to live testing.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
Domain: mass-appraisal ratio studies (median, COD, PRD, sales chasing) is the field's own work. Layer 1 is the legacy 2025 export, the parcel renumbering with reused identifiers, and the Board of Review re-hearings. Layer 2 is correcting the sale-selected sample for sales-chasing. The easy route computes the rule's sales ratios (0.95, 8.0), says it meets and declines the offer. The decisive step is analytical, but the estimand it must reach is not filed.

## Fix
- **prompt:** file the WHAT, not the HOW. For example, state the population: the level and COD are for the whole single-family class including parcels not sold, with sold parcels counted at their share of the class. Or add to Rule 18-7 a sentence on parcels revalued after sale.
- If the zero-weight variant is meant to be wrong, that has to follow from a filed sentence, not from method choice.
- Alternatively, grade the single-family median and COD with a stated tolerance (0.86 to 0.88, 18 to 19) and keep the accept call.
- Do not change the data. The condominium and Board of Review answers are fine.

**Disposition read against the gate table** (`determinism-check` section 6): Gates G and H pass and Gate F is strong; the failure is Gate C on the main call (the population left unfiled), so the build was repaired rather than re-rooted: rule 2.1 files the parcels that did not sell, the method stays open, and the one re-judge is owed.
