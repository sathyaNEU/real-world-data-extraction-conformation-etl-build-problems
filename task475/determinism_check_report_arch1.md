# determinism-check report, task475, 2026-10-20

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: etl_conformance (method_or_model_selection on the main estimand), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed figure reproduced from the shipped bundle. Policy rev 4 (3.1, 4.1, 4.2, 5.1 to 5.3) fixes the population, tax year, crosswalk (2023Q4 ZIP-to-county, residential ratio, total ratio for four P.O. Box ZIPs) and the exclusion of the 00000 and 99999 lines. Tallis leads at 11.46 per cent, under the 12 per cent cap. Asks A and B are closed by policy 6.1 and the close-out notes, with the data separating the readings. Judge thread: one pass, sonnet, medium, isolated to /tmp/determinism-check-task475-6066/ (verdict.md retained there).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Tallis returns with children | 6,270.1 | 6,270.08 | yes |
| Fourteen-county total | 54,712.6 | 54,712.62 | yes |
| Tallis share / allocation | 11.46 / $2,292,000 | same | yes |
| All 14 counts, shares, allocations | per submission | match exactly | yes |
| First-class averages $394.88 / $4,723.49 | DOR Table 2 | match | yes |
| Ask A dwellings (14 counties) | Tallis 352 ... Ravell 51 | all match (989 jobs, first COMPLETED in 2025) | yes |
| Ask B spending (14 counties) | Tallis $1,653,025 ... Ravell $308,925 | all match (7,578 lines, $10,892,452.88 ties close-out Table 1) | yes |
| CSV families file | item 2 | consistent | yes |

## Competing answers that survived
- Main figures, low to moderate: the estimation method is not filed. Using the all-class with-children average ($4,271.65) instead of the first-class average moves Tallis to 11.50 per cent and the counts by 160 to 460 returns per county (allocations up to about $7,700). The cap call is unchanged. The first-class average is the only one consistent with Table 2 (credits fall in higher classes), so the data separates the candidates. The graded one-decimal counts depend on that choice. Per house rules this is left unfiled (filing it would file the HOW); the main thread should weigh it.
- Statewide share (Tallis 15.46 per cent, capped) and all credit returns (16.54 per cent) are shown wrong by the ZIP-level amounts; not defensible alternatives.
- Ask A: export COMPLETED_DATE (Tallis 349), agency-entered county (465), excluding mixed UTIL-LIW jobs (322) are each closed by policy 6.1 and the close-out definitions.
- Ask B: literal ledger job numbers fail (21 per cent agency match, 99.9 per cent service before opening); the MOVED mapping gives 100 per cent. The mapping is not stated in words but the data forces it (a Layer-1 key mess in a supplementary ask). Service-year basis (Tallis $1,485,067) is closed by the close-out's posting-year note.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | 4 (csv, xlsx, pdf, txt) | yes |
| Large file | 25,000+ rows | status history 29,231 | yes |
| Distractors | 2+ in metadata.json, none named in a file name | TY2022 extract, county-to-ZIP relationship file; names do not label them | yes |
| Distractor weight | unused by solution, rules out by a shipped fact | both reproduce a wrong basis; policy 3.1 and 4.1 rule them out | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 14-county grids; units and rounding in the prompt | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | per-county grids for counts, shares, allocations, dwellings, spending (70+ gradable figures) | yes |
| Reads as real, not LLM generated | clean | judge found no authoring language; data dictionary is mildly over-explanatory | yes |

## Gate G reconciliation
Thread: mechanism etl_conformance, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card/design note: stump_class analytical; the stump is applying the statewide child share (Tallis 15.46 per cent, capped) against recovering each county's own mix from credit count and amount. Match. The declared distractors (TY2022 extract, reverse crosswalk) are not the surface read carrying the task; the thread names the statewide-share estimate, which no shipped artifact computes or ranks. No finding.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical (credit-amount decomposition into childless and family claims, an ecological estimate, with the cap call flipping on it). Matches the card's analyst_test and domain_test.

## Stump power (Gate F)
Good. The wrong route flips the cap call, and the ZIP-level decomposition is rarer. Asks B (old-number mapping) and A (first completion versus export date) add independent traps. The two-kind decomposition by statewide average credit is the textbook route for this data, so a strong solver may land it; the scored readers decide. The 11.46 versus 12 margin is clean.

## Findings, ranked
1. Low-moderate: the one-decimal counts depend on the unfiled choice of first-class averages (see forks). Cap call unaffected. No fix required.
2. Info: data dictionary is unusually explanatory; it does not disarm any trap.

## Next action for the author
None required; proceed to ship. Optionally, hold the first-class-average choice open, as the design intends.
