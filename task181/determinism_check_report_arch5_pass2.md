# determinism-check report (pass 2, re-judge after FIX_NOW), task181, 2026-10-31

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK (judge's call; main call and chart bars depend on an unpinned working-day share)
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Plan 4.3 counts cases "infected in that barangay"; no shipped file records a place of infection. The golden is an estimate (NNLS workplace fit, share of working day at work 0.5 to 1.0). The judge reproduced the golden at s = 0.5 and 1.0, but at an 8-hour working day (s = 0.33) San Roque falls under 40 (excess-only placement) or lands at 41 with six extra barangays in (all-working-age placement); at 0.2 San Roque is out. Nothing in the package fixes the lower bound. The design note's own Three rules lean on "Aedes feeds in daylight", a fact absent from the plan, the zone bulletin and the rest of the bundle (grep of both PDFs: no hit), so it does not exist for the reviewer. Taxonomy: underspecified_objective, with margin_or_boundary_fragility at the plausible 8-hour share. The FIX_NOW edits (NNLS step, 0.5 to 1.0 range, estimates wording, two-facility sentence) did not close this; they state the author's range instead of forcing it from a shipped fact.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Home-address set MW37-40 (line list) | 8 barangays at 40+, San Roque under | Tabing-Ilog 48, Silangan 58, Kanluran 53, Pulong Bayabas 54, Maligaya 66, Burol 54, Malinta 47, Bagumbayan 85; San Roque 14 | yes |
| Working-age excess | six estate-side barangays | 37 to 55 each; Maligaya, Bagumbayan about nil | yes |
| Placement at s = 0.5 / 1.0 | San Roque, Bagumbayan, Maligaya only | same | yes |
| Placement at s = 0.33 | not claimed | San Roque out (excess-only) or six extra barangays in (all working-age) | fork |
| House index | 12 values | 6 of 12 matched; 6 not parsed | partial |
| Hospital admissions, lab counts | per submission | not recomputed (single pass) | not verified |

## Competing answers that survived
- Share of day at work 0.33 (8 of 24 hours): San Roque out or marginal, Silangan, Burol, Pulong Bayabas, Kanluran in. No shipped rule closes it.
- Whole working-age count moved versus only the excess moved: different bar values for the chart.
- Closing sentence offered: none in the files; the design note's "daylight feeding" is not shipped.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 12 | yes |
| Formats | 3+ | 4 (csv, xlsx, pdf, json) | yes |
| Large file | 25,000+ rows | line list 26,205 lines | yes |
| Distractors | 2+ in metadata.json, none labelled in a file name | 3 (VCU log, rainfall, zone bulletin); names unlabelled | yes |
| Distractor usable but ruled out | weigh, unused | not tested by me; judge saw them as distractors | not checked |
| Deliverables | 1 to 3 | 2 (PDF, CSV), all in golden | yes |
| Asks multi-dimensional with unit and rounding | yes | 3 PDF asks and 5 CSV asks, units stated | yes |
| Rubric 25+ criteria | 25+ | not generated here | not checked |
| Reads as real work product | yes | judge saw realistic mess, no authoring language | yes |
| target.zip | current | md5 bddf17795bb6541bb3a37e6299d0e2ed (post-rebuild, as the coordinator stated) | yes |

## Gate G reconciliation
Thread: decomposition_attribution / analytical_non_defect / surface_read_dependency no / sole_data_defect no. Design note: estimand_identification, place of infection, same family. No mismatch on class. The declared distractors (VCU log, rainfall, zone bulletin) were not named as the surface read. The surface read the thread names is the home-address count, which is the intended trap, not a distractor.
Gate H: domain pass, layers pass, decisive_step analytical. This agrees with the card and note; the residual risk is determinism, not Gate H.

## Stump power (Gate F)
Home-address route (eight barangays, San Roque out) is attractive and wrong, so a strong model can fail it. But the stump partly reflects guessing the exposure share, not a forced answer. Because the answer moves with an unshipped assumption, a solver landing the call is arguably lucky, and a solver who lands it by a different method gets different chart bars.

## Findings, ranked
1. Working-day share is unpinned: s = 0.33 or lower changes the in/out set, so the main call and the bars are not forced.
2. The deciding fact (Aedes feeds in daylight, so exposure sits at the workplace) lives only in the design note; no shipped file states it.
3. Bar values depend on method (excess-only versus all working-age, NNLS versus share) and are not reproducible to one number per barangay.
4. Verification gaps: six house indices, hospital and lab figures not independently recomputed by the thread.

## Next action for the author
Re-root or repair in the generator so the margin holds at every licensed share down to 0.2 to 0.33, or ship a fact (e.g. in the plan or bulletin) that states the exposure basis as an estimand (where the case was infected: the working day's place for working-age residents) without filing the HOW; then rebuild and re-judge only if the author asks.
