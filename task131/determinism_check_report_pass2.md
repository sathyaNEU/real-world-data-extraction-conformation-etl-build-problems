# determinism-check report, task131, pass 2, 2026-10-13

## Verdict
DETERMINISTIC (main call and every graded figure reproduce; residual softness in xlsx ask 1 and the GST basis of ask 2)
**Disposition:** FIX_NOW (one clarifying clause in prompt.txt; no data or graded figure changes)
**Stumping type:** mechanism: other (heterogeneous treatment effect at design-day heat, aggregated to the system peak), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
At the 44.6 C design-day heat, estimated on the 7 workdays at 43.7 to 45.3 C, Design C lowers the 214.6 MW 2027-28 50% POE maximum by 11 MW, A raises it by 5 MW and B by 20 MW. The plan's section 6 fixes intention-to-treat, the forecast's Method sheet fixes the design day, the Customers sheet gives 41,860 customers. The pass 1 survey-denominator finding is closed: ask 3 now reproduces at 60.3 / 41.5 / 58.8 (n 257 / 241 / 250). Open items are graded-figure forks only.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Hot workdays | 7 (19-23 Jan, 10-11 Feb) | same 7, IDCJAC0010 | yes |
| B effect 8 pm / A effect 9 pm | 0.7 / 0.6 kW | 0.732 / 0.635 | yes |
| Home Plan max | 214.6 MW | 214.6 (forecast Design day sheet) | yes |
| Change C / A / B | -11 / +5 / +20 | -10.99 / +5.10 / +20.04 (all estimators same whole-MW bins) | yes |
| Ask 1 billed on design / own request / left | A 370;22;7 B 361;29;9 C 374;18;6 | same | yes (see fork 1) |
| Ask 2 charged more; mean | 123,-19.64; 45,-42.86; 52,-31.61 | same | yes (GST-inclusive, all 400 households) |
| Ask 3 share to stay | 60.3 / 41.5 / 58.8 | same | yes |

## Competing answers that survived
Main call: none. Graded-figure forks, low severity:
1. Four households asked to return to the Home Plan and then left before 28 Feb (A1, B2, C1): golden counts them as no longer customers; an unanchored reading of "back on the Home Plan at their own request" gives 23/31/19. Close with a status-on-28-February clause.
2. Four life-support returns (A1, B1, C2) fall in none of the three categories (rows sum to 399/399/398); the history marks them INELIGIBLE - LIFE SUPPORT, not a request.
3. GST: plan design prices exclude GST, the gazetted schedule includes it; golden uses inclusive. Means would be 1/1.1 of golden ex-GST. Counts unaffected. Close with "including GST".

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 18 / csv, xlsx, pdf | yes |
| Large file | 25,000+ rows | four NEM12 files, ~336k day records | yes |
| Distractors | 2+, named in metadata, not in file names | 3 named (zone_substation_loads, rooftop_pv_connections, generation_availability); none labelled in names | yes |
| Distractor weighs, unused, ruled out | yes | substation loads show the summer without ranking designs or reproducing a figure (design note); judge found no ranking artifact | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | prompt states MW whole, dollars to the cent, percentages to 1 dp | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | per-design x many figures (about 22 asks figures plus call and components); rubric count not generated here, not verified | not verified |
| Prompt | under 1,000 chars | 992 | yes |
| Reads as LLM generated / golden realism | no | judge saw none; golden-realism not re-read here | yes (judge) |

## Gate G reconciliation
Judge: no artifact ranks the designs on the decision question wrongly; the three declared distractors carry nothing; surface_read_dependency no, sole_data_defect no. Matches the card (stump_class analytical). One mismatch of detail: the design note and card name the wrong default as Design B (about 15 MW lower, window cut on an average day) or A (average whole profile); the judge's measured pooled-workday route gives A -13, B -3, C -10 and so picks A. Both are the same average-day family and neither is a shipped artifact, so not a send-back, but the note's "B by about 15 MW" does not match the judge's pooled figure; the author should check the Ends on figure. Judge mechanism wording differs from the card (heterogeneous effect at design-day heat versus the card's deferred-cooling rebound) but names the same step.

## Stump power (Gate F)
Moderate. Pooling picks A; a linear temperature fit gives A 0, B +14, C -12; naive survey coding gives 49.4/44.0/50.4. A careful model that conditions on design-day heat and finds the shifted evening peak lands on C.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the card's analyst_test and domain_test (the intention-to-treat rule is stated but heat conditioning decides).

## Findings, ranked
1. xlsx ask 1 status partition ambiguity (fork 1), plus life-support returns in no category (fork 2).
2. GST basis of the dollar means (fork 3).
3. Design note easy-route figure (B about 15 MW) versus judge's pooled route (A); reconcile.
4. Rubric criterion count not verified here.
Fingerprint cross-batch check not run by the thread (out of its readable directory).

## Next action for the author
Add one clause to prompt.txt (it has 8 characters of room, so tighten elsewhere): the three counts are each household's status on 28 February 2026, each household counted once, and dollars include GST; then rebuild and re-confirm byte-identical figures. Run /fix-determinism if the single re-judge allows; otherwise ship after the pin.
