# determinism-check report, task286, 2026-11-07

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (two small golden text corrections ride with the builder's layout rebuild; neither moves a figure)
**Stumping type:** mechanism: signal_vs_noise_or_hold, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet thread on a fresh unzip of target.zip (sha256 216a2882...b058e) at /tmp/determinism-check-task286-194223/. It reports it kept the order (derivation.md before graded_blocks.md). Its derivation matched every graded figure.

## Why
The prompt's "homes that nobody used" is closed by terms of reference 4.3 ("a week counts as a week of use if anybody lived in, stayed at or used the home on any day of it, for however short a time"), 4.2 (home = self-contained dwelling on the gazetteer, however taxed, rated or let) and 4.1 (the window). Read literally, a running cistern is not anybody using the home. The meter data is bimodal: zero, trickle (2 to 39 L a day), human days (100 L and up, varying) and flat constant flow, with no weekly range between 30 and 60 L. Orrimouth 203, Ellingsea 159, gap 44 is forced. Council tax and rates asks close on the Taxbase definition, the Teversby migration link, and the gazetteer parent/child structure. No margin reading changes a count.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Homes, one meter each | 5,730 | 5,730 (113 UPRN-less matched by address, 8 flats by postcode+flat) | yes |
| Unused 26+ weeks Orr/Ell/Tar/Kit/Bra/Que/Wen/Cra | 203/159/119/113/104/55/51/49 | identical | yes |
| Chart bands, all 8 areas | e.g. Orr 15/108/80 | identical | yes |
| Long-term empty (Bra, Wen, Que, Tar, Orr, Cra, Ell, Kit) | 30, 10, 17, 14, 20, 15, 39, 6 | identical | yes |
| Self-catering homes | Bra 13, Cra 7, Ell 23, Kit 27, Orr 9, Que 6, Tar 51, Wen 10 (146) | identical (103 entries, 55 child homes via shells) | yes |
| Gap | 44 | 44 | yes |

## Competing answers that survived
None on the main call or the asks. Readings tested and how they stand:
- Any water above 0 names Ellingsea (148). Any 40 L+ day names Ellingsea (155). Weekly volume lines of 50 to 700 L name Ellingsea (149 to 181). These are ruled out by 4.3 ("anybody lived in, stayed at or used") plus the data's gap: a steady flat flow is not a person. They do not survive as defensible answers, but see the Gate B weighing below.
- Flat-flow detectors with run length 3/4/5/7 name Orrimouth every time (205/204/203/203 vs Ellingsea 163/159/159/159). The winner never changes.
- Estimated-day weeks counted as used: Brackwater 104 to 103 only, non-decisive.
- Long-term empty: spell lengths have a dead zone of 173 to 203 days around the 184-day boundary. Chain-gap variants are identical.
- Easy routes that fail: new Teversby system alone gives 0 for Teversby; Swanholt current account alone gives 66 not 80.
- Week boundaries: READ_DATE_UTC is a date, so no sub-day local-time shift exists, and no count depends on it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 13 | yes |
| Formats | 3+ | 4 (csv, pdf, parquet, xlsx) | yes |
| Large file | 25,000+ rows | 2,286,365-row parquet | yes |
| metadata distractors | 2+ named, no file name labels one | 3 files (census table, its OA lookup, HNA summary), which is two sources; wrong_basis_distractor declared on the HNA; names plain | yes |
| Distractor behaviour | unused, weighable, ruled out by a shipped fact | census/HNA rank Tarnhithe and Kittlesea; ruled out by TOR 4.1 and 4.3 (one census day five years earlier, not 52 weeks of use) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both present | yes |
| Asks | multi-dimensional, unit and rounding stated | three per-area columns over 8 areas plus 3 chart bands; "Every count is in whole homes" | yes |
| Prompt shape / rubric | identifiable, 25+ | shape 01, about 33 criteria by the design note (8 + 3 + 16 + about 4 + 2) | yes |
| Reads as real, not LLM | | prompt 780 characters, one paragraph; golden chart and workbook read as an agency product; two defects below | yes with fixes |

## Gate G reconciliation
Thread: mechanism signal_vs_noise_or_hold, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and note: Gate G `decomposition_attribution`, strategy `population_selection`, Layer 2 `estimation_fit`. These are consistent: a correctly reported volume split into steady flow and use, with no wrong shipped number. No shipped artifact ranks the areas on the decision question wrongly. The declared distractor (HNA census table) is named in metadata, ruled out by TOR 4.1 and 4.3, and is not the surface read carrying the task: the thread's easy route is the void or volume read, not the census. No finding on distractor load.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Card: `stump_class: analytical`, with `analyst_test` (void weeks file Ellingsea) and `domain_test` (void-read precondition broken by a leak). The note's Three rules agree on all three points. The note's decoy line (nothing names a leak or volume rule) is confirmed by the thread. One qualification: the note says no file names how use shows in the meter, so the decisive step rests on the data's own signature, which is Gate B territory, below.

## Gate B weighing (week-of-use reading)
Does it hold as the literal reading forced by filed text plus data? Yes, with one caveat.
- The filed text (TOR 4.3) files the WHAT: anybody lived in, stayed at or used the home. The prompt repeats it as "nobody used". A cistern that runs every day is not a person using the home, so "any metered water is use" is not a literal execution of 4.3. It substitutes "water registered" for "anybody used".
- The data separates the readings: no weekly range between 30 and 60 L, and the margin from 30 to 75 L gives the same counts. The thread reached the golden from the data alone, without the submission's rule, and its detector variants (run lengths 3 to 7) never changed the winner.
- The caveat: "for however short a time" can be read as pushing toward a low-volume line (a few litres of use is still use). That does not contradict the golden. Trickle weeks of a few litres a day are flat and are not anybody using the home. A volume line is the reading that 4.3 plus the data refute.
- A strict grader could still say that knowing a leak is flat is knowledge outside the files. I do not think so. The standard is whether the filed words and the shipped data settle the reading, and they do: "nobody used" plus a bimodal gap. The model must notice that litres are not occupancy, which is the analysis, not a semantic field reading.
- Closure: none needed. Any closure that names a leak, a steady flow, a variation test or a margin would file the thing the decisive step recognises, which is the fork-is-the-stump case and would turn the call into rule application. Do not add one. Keep TOR 4.3 as filed.
- Risk to carry: moderate. If the portal's reader reports "volume reading defensible", the design note's rung table and this ledger are the evidence that the flat-flow reading is the one the files force.

## Stump power (Gate F)
Good, per the thread. The easy route (any water, or a volume line at any threshold from 1 to 1,000 L) names Ellingsea, a defensible-looking wrong area. The note's analyst test says a strong analyst who cleaned every file and read every rule correctly still files Ellingsea 161 vs Orrimouth 85 by the void read. The thread did not class the decisive step analytical because it was a standard method: the water industry's void read is the textbook route, and it is the wrong one here. Two ask traps (Teversby migration reset, shell-parent homes) are real joins. Low too-easy risk. Low fragility, since any reasonable flat-flow detector lands on Orrimouth.

## Findings, ranked
1. Realism, layout (leak reader, confirmed by rendering): terms of reference PDF page 2, the risks table mitigation text overruns its cell border and the document-control change text runs into the By column. Layout only. Builder wraps the cells.
2. Golden text, homes_in_use_pilot_2027.xlsx Recommendation sheet (golden.py line 116): cites "Terms of reference 3.1 to 3.3", but the section is 4.1 to 4.3 in the shipped PDF. Correct it to 4.1 to 4.3.
3. Golden text, xlsx Notes row 4 (golden.py line 172): says the count is the same "for any margin between about 20 and 70 litres", while submission.md and checks.py SF11 say 30 to 75. Make the two agree (30 to 75, the asserted range), per the rule that a figure shared by two deliverables agrees.
4. Gate B watch item above: no fix, carry as a note for the portal.

## Next action for the author
Wrap the two PDF cells and correct findings 2 and 3 in golden.py in the same generator pass, rebuild, then re-run the free gates on the final cut (generator checks, verify, two byte-identical builds, figures_check, precut, leak, heart, surface). The PDF change alters target.zip's hash, so ship the hash from the final rebuild. Finding 1 does not move any graded figure or any file's content the judge read for the decisive step, so the APPROVE stands without a re-judge. Do not file a rule about leaks or flat flow.
