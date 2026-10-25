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

## Round 2 (2026-10-25, target.zip 34487572)

**Verdict:** DETERMINISTIC (the main call is forced; two figure-level forks are listed under Evidence).

**Disposition:** FIX_NOW. File the population of the main-ask statistics in one clause of the prompt, or in the data dictionary, so the sold parcels are counted at their own 2026 values among all 25,988 parcels, as Rule 18-7 2.1 already says. Add a one-line dictionary pin that a second hearing in a case replaces the first. The analytic surface is unchanged, so no model rerun is needed.

**Why:** Every sound route that corrects for the post-sale revaluation fails the roll. The only route that passes it is the uncorrected sales sample (0.95 and 8.0), and the data refutes that sample. The 1,742 parcels with a 2025 Q deed rose a median 14.9 percent from the 2025 roll to the 2026 roll, against 3.4 percent for the other parcels. The prompt does not say how the unsold parcels are valued or how the sold share is weighted. The median to two decimals and the COD to a whole number therefore depend on that construction (main ask, figures 1 and 2). The condominium and Board of Review answers reproduce exactly.

## Evidence (recomputed from target/)

| Item | Golden | Mine | Reproduced |
|---|---|---|---|
| R1 Q deeds on roll (deed parcel number without dashes plus 0) | 1,742 | 1,742 | yes |
| R1 sales set aside (permit finaled after deed) | 44 | 44, all from building_permits_2025.csv; no R1 split or combine hits a Q deed | yes |
| R1 study sales | 1,698 | 1,698 | yes |
| Sales-only R1 median ratio and COD | 0.95, 8.0 | 0.9519, 8.007 | yes |
| 2025 to 2026 change, parcels with a Q deed | 14.9% | 14.93% | yes |
| 2025 to 2026 change, other parcels | 3.4% | 3.40% | yes |
| Sold share of the 25,988 R1 parcels | 6.7% | 1,742 / 25,988 = 6.70% | yes |
| Weighted R1 level and COD (93.3% at 2025 value times neighbourhood median change among unsold parcels, to the nearest 100, over indexed price; 6.7% at the 2026 value) | 0.87, 18 | 0.8697, 17.99 | yes |
| Condominium sales | 129 | 129 | yes |
| Condominium median, aggregate, COD, PRD | 0.93, 0.932, 7.1, 0.997 | 0.9317, 0.9322, 7.09, 0.9969 | yes |
| Board of Review count and dollars, areas 1 to 6 | 132, 156, 171, 94, 166, 152 and 4,349,600 / 5,656,500 / 6,564,800 / 3,402,200 / 7,095,200 / 6,109,300 | identical in all six areas | yes |

Facts that do not change the figures:
- **Weights.** The R1 figures are the same with sold weight 1,698 / 25,988 or 1,742 / 25,943.
- **Neighbourhood factor.** A county-wide factor or a neighbourhood mean gives the same 0.87 and 18 within rounding.

Condominium reproduction needed three readings, each supported by the files:
- **Wexley Commons numbering.** Wexley Commons (book 218, page 12) was renumbered on 1 July 2025 (DECL-25-0117, 404 renumbered, 16 combined parcel rows). Deeds and permits dated before 1 July carry the old number and map through the change log. Deeds and permits from 1 July on carry the new number. I checked the mapping against the unit labels: 404 of 404 renumbered units match, and 24 of 24 permit unit labels match the 2026 situs. Mapping every Wexley deed through the log instead gives a post-July ratio spread of 0.32 to 3.44. The data separates the readings.
- **Combined units.** Only deeds signed before the combination are set aside (5 deeds, under rule 3.2). The two post-combination deeds (3 July and 3 November) stay in. This gives 154 less 5 less 20 permit set-asides, which is 129.
- **Permits.** The 20 permit set-asides (permit finaled after the deed) do not overlap the 5 combined-unit set-asides.

Condominium sold and unsold parcels moved the same median (5.3 percent), so the condominium class shows no post-sale revaluation and straight sales is right for it.

Forks and competing answers:
1. **Main ask, how the unsold parcels are valued and weighted (Gates C and E).**
   - Sold-only sample, which is the literal Rule 3.1 evidence: 0.95 and 8.0. This meets the rule, so decline the vendor. The data refutes it (14.9 versus 3.4 percent), and Rule 2.1 says "sold or not".
   - Unsold-parcel projection only, with the 6.7 percent sold share dropped: 0.86 and 19. The call is the same, but the median and COD differ from the golden at the asked precision.
   - Sold share weighted in at 6.7 percent (golden): 0.87 and 18. This is the only reading that counts every parcel, as 2.1 says, but the prompt does not say so.
   - No sales-chasing correction, with the 2025 roll level 0.90 carried forward by the index: 0.86 at Jan 2026 for the unsold. The call is again "fail".
   - The pass/fail call is unchanged across every correcting route. Only the two figures differ (0.86 or 0.87, 18 or 19).
2. **Board of Review parcels with two hearings (31 parcels).**
   - Golden: the last hearing in the case stands (value_before in the second hearing again equals the certified 2025 value, so it replaces the first).
   - "Any reduction counted": 136, 160, 175, 98, 170, 157 parcels and 4,394,600 / 5,826,400 / 6,641,800 / 3,511,700 / 7,143,000 / 6,177,000 dollars.
   - Example: parcel 105-10-013 is reduced at the first hearing and sustained at the second. The data dictionary says only that "a case heard a second time has a row for each hearing".
   - This fork is real but low-risk, and the pin is one dictionary line.
3. **Other forks.**
   - **Hearings before 2 June 2025.** These are appeals of the 2024 roll. All 198 have value_before different from the 2025 roll value, and all 1,559 later hearings (including the 115 withdrawn, which have no hearing date) have it equal. The cut is clean.
   - **Accept versus decline.** Accepting follows from a failing roll: the offer lapses 30 October, the Commission would order the reappraisal anyway at county cost, and the memo says no other vendor can start in time. If the Division's own study uses sold parcels only, the order may never come. The Rule 2.1 wording and the memo's question ("does the roll meet Rule 18-7") settle it for the golden.

Gate status:
- **Gate A:** pass. All figures reproduce.
- **Gate B:** pass. Every decisive fact is in the shipped files. The vendor's offer terms are in the memo, the standards in the rule PDF, and the index in the CSV.
- **Gate C:** the call holds. The figure-level fork above is a minor finding.
- **Gate D:** pass. The difficulty is in the analysis, not in what a word means.
- **Gate E:** the prompt pins the call and the formats. The weighting is unfiled.

## Files/Hygiene

- **Verdict:** PASS.
- **Files:** 13, of which 2 are distractors. Formats: csv (8), xlsx (2), pdf (2), txt (1).
- **Distractors:** homestead_credits_2026.csv and levy_and_rates_fy2026.xlsx. The memo itself says they are not part of the question, which pre-disarms them. This is not a stump-affecting issue.
- **Large file:** the 2026 roll has 27,680 rows, so the 25,000-row gate is met.
- **Realism:** the legacy xlsx has a report header ("Run 01/08/2026 ... CAMA-LEGACY RPT 114"). Parcel formats differ across the two systems. Deeds carry a mix of deed types. All read as county system exports.
- **Dates:** coherent. The roll was certified on 1 June 2026, the memo is dated 14 September 2026, the dictionary 18 September 2026, and the index runs to 2026-06. The rule's orders reproduce the memo's 2028 / 31 January 2027 dates.
- **Provenance:** no authoring or benchmark leakage seen in the shipped files. No public-data contamination concern.

## Stump power (Gate F)

- **Trap:** the easy route computes the sales ratios straight from the Q deeds, as Rule 3.1 reads on its face, and gets 0.95 and 8.0. That passes both tests, so it declines the vendor, which is the wrong call.
- **Why a strong model may fall for it:** the 14.9 versus 3.4 percent gap exists only on a 2025 roll to 2026 roll join that the prompt never mentions. Rule 2.1 ("sold or not") is a nudge, and some strong models will test for it.
- **Supporting stump power:** the condominium Wexley Commons renumbering and the Board of Review hearing logic add hard asks. Expect real stumps from the main call and the asks.
- **Too-easy signals:** the rule text says "sold or not" and the memo is clean, but neither states the mechanism.

## Stumping type (Gate G)

`mechanism: statistical_rigor` (selection bias in the sales sample, sales chasing), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.

No reported or stakeholder number is wrong. The solver derives the sales ratio from the rule's own evidence, and the difficulty is estimating the roll level for the whole class from a sample that the assessor revalued after sale. This is a FINE-numbers shape: the study shape and the rule are honest, and the unit of analysis (the whole class, not the sold sample) carries the call. The borderline is that the revaluation is generator-made; it is the real sales-chasing pattern, so I do not flag it as a planted defect. Not a banned scaffold.

## Three rules (Gate H)

`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- **Domain:** a property-tax ratio study (median ratio, COD, PRD, sales chasing). The swap test fails to substitute: another field's nouns change the meaning.
- **Layer 1:** a retired legacy system export against a new-system roll, parcel renumbering and combination, deed and permit numbering that changes by date, a price index to carry sales to the assessment date, and 2024-roll and 2025-roll hearings mixed together.
- **Layer 2:** estimating the level and COD of the whole class when the sold parcels were revalued after sale.
- **Easy route:** a strong analyst who cleaned the data and read every rule would take the sale ratios as the study and file 0.95 and 8.0, which passes the roll. That is the wrong answer. The correct estimand is the whole class.

## Fix

- **prompt:** file the population of the main-ask statistics, namely every one of the 25,988 parcels on the roll with sold parcels at their own 2026 value, without filing the method. Rule 18-7 2.1 already says "sold or not".
- **input_files:** a one-line data-dictionary pin that a later hearing in a case replaces an earlier one. Neither change alters the analytic surface.

**Outcome.** The call is forced and Gates G and H pass, but both round-2 scored readers landed the call, so the FIX_NOW is moot: the architecture is spent on Gate F.
