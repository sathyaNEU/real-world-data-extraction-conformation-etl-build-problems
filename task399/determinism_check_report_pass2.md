# determinism-check report, task399, pass 2, 2026-11-04

## Verdict
DETERMINISTIC, with SOLUTION_WRONG (wording only: solution steps 7 and 8)
**Disposition:** FIX_NOW (solution text and ask-layer conventions; no architecture touched)
**Stumping type:** mechanism: decomposition_attribution (etl_conformance layers on the asks), stumping_family: mixed, surface_read_dependency: yes (borderline), sole_data_defect: no

One judge thread, sonnet, medium. Scratch /tmp/determinism-check-task399-820589/ (judge_brief.md, derivation.md, verdict.md). target.zip sha256 5156aef8...b78fa, fresh unzip of all 15 files. **Order kept**: the graded blocks lived in graded_blocks.md, outside the brief; derivation.md was on disk before the thread opened it; the thread says it did not open, list or grep it earlier. Its derivation agreed with the submission on every graded value before it saw it; the only differences were wording and three unnamed conventions (F2 to F4 below). The pass-1 report was not shown to the thread.

## Why
Programme B (display renewal) is forced by the files: 76 wrong routes set onto an exit drawn 8.0 to 11.5 px from the required one (next-closest pair 49 px; the other 14 wrong routes 60 px or more) fail at the same rate per route request for first-two-years and other signallers (2.46 against 2.31 per 1,000 on the crowded pairs), so only the redraw would have prevented them. With the 10 display faults B reaches 8,985 minutes, against 6,517 at most for A restricted to the signallers it enrols, 7,331 for C and 6,642 for E counted overlap-generously. The recorded investigation causes alone make A lead (8,240), which the control-system records rule out. All 12 hours cells and all 24 ARS cells reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Crowded-exit wrong routes | 76 / 8,173 | 76 / 8,173 (register joined to layout routes and signal x,y) | yes |
| Display faults | 10 / 812 | 10 / 812 (category Workstation fault) | yes |
| Programme B minutes | 8,985 | 8,985 (8,173 without faults) | yes |
| B by workstation | W03 3,544; W05 1,487; W01 1,266; W06 1,230; W02 762; W04 696 | identical | yes |
| 360 routes cancelled within 20 s | 360 | 360 of 3,910 CN | yes |
| Hours, first-two-years / others (12 cells) | e.g. W04 3,947.5 / 4,812.5 | identical, from rosters + changes + sign-ons | yes |
| ARS sub-area hours off by quarter (24 cells) | e.g. W03 336.7, 279.5, 339.1, 291.5 | identical | yes |

## Competing answers that survived
- F1 minutes 8,985 against 8,173 (faults out): clause 2.3 and the catalogue (VDS-3 removed from every workstation) rule the faults in; programme and start workstation do not move. Low.
- F2 second-anniversary day counted outside the first two years (3 shifts: 474844 17 Dec 2025 W01, 461744 9 Apr 2026 W01, 905596 14 May 2026 W04): W01 moves 24 h, W04 12 h (4 of 42 supplementary cells). No shipped sentence closes it. Low.
- F3 elapsed against nominal hours on the clock-change nights (13 h on 25 Oct 2025, 11 h on 28 Mar 2026): W04 cells move 1.0 h (3,946.5 / 4,813.5). Step 7 as written ("on the clock") points the wrong way. Low.
- F4 FAIL rows counted or not: 33 workstation-wide FAIL rows, 8 to 20 h per workstation. The rows state OFF at workstation level and are ended by per-sub-area ONs, so the literal reading counts them. Closed by the literal text; record the convention in the solution.
- F5 sign-on records against roster + changes for who worked: "who worked" is factual and sign-ons are the direct evidence; the rostered figures survive for 4 cells only. Low.
- Reading 1 and 2: A as recorded (8,240) is ruled out by shipped data (equal per-request slip rates; A's scope), not by a quoted sentence; weak survivor only.
- Clock readings (ARS): B as UTC moves W01 and W03 by 35 h and 55 h; A-only drops outage-day events. The submission's Central European reading is the one the mirror's copies force.
- Rounding: smallest distance of any ARS cell to a rounding line is 0.034 h (W02 Q2, 233.084). Main margin: B 8,985 against A as recorded 8,240 (745, 9 percent), against C 654 (overlap-generous), against A in scope 2,468.

## Spec gates (checked by me on the unzipped bundle)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, docx, json) | yes |
| Large file | 25,000 rows or more | actions log 357,103 rows (25 MB); ARS log 14,894 | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | workload assessment 2025 (pdf, Hatherby high-load story pointing at E) and railhead adhesion reports (csv); both in `reference/`, neither labelled | yes |
| Distractors unused yet weighing | | peak-hour error rates reproduce arithmetically and point to E; shipped per-request rates ruled it out (the workload one answers no graded quantity) | yes |
| Deliverables | 1 to 3, all in the golden | 2 (pptx, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | | workstation x experience band; workstation x sub-area x quarter; "whole minutes", "one decimal" in the prompt | yes |
| Prompt | one paragraph, question first, under 1,000 chars, no count the data hold | 845 chars, question first, no counts | yes |
| Shape and 25 or more criteria | identifiable shape, rubric 25 or more | shape 12 (drill-down); rubric is generated and not in the package; the cells alone (6 workstations x 2 bands, 24 ARS cells, 6 splits, call, minutes, start) exceed 25 | yes (by count of gradable cells) |
| Reads as real, not LLM generated | | judge found no authoring language; minor templating in the 2025-26 register summaries ("Other moves being dealt with." 78 times) and an all-OCF `resp` column, undefined ARS reason codes; not exclusion-level | yes (minor) |

## Gate G reconciliation
CLAUDE.md Gate G: no shipped artifact ranks the candidates on the decision question and gets it wrong; the difficulty survives deleting every wrong number. Design note and card against the thread:

| Item | Thread | Design note / card | Match |
|---|---|---|---|
| mechanism | decomposition_attribution | gate_g decomposition_attribution | yes |
| stumping_family | mixed | stump_class analytical, strategy classification_error (field_method layer 2) | partial; see below |
| surface_read_dependency | yes (borderline) | the surface read is the sum by recorded cause (A at 8,240) | consistent |
| sole_data_defect | no | no decoy, no planted value | yes |

- **Is the register's cause a ranking artifact?** No. Per the design note and the thread, the recorded underlying causes are per-incident investigator findings that a solver must total; no shipped file ranks, prices or recommends a programme (the ToR states clause 2.3 only; the catalogue lists programmes). The sum 8,240 for A exists only if the solver makes it. The one document that ranks anything, the 2025 workload assessment, is the declared distractor (Hatherby highest) and the shipped per-request rates rule it out. So the Gate G exception for a declared distractor is met and it is not the stump.
- **Does the difficulty survive deleting the wrong numbers?** Per the pass-1 finding the coordinator relays (I did not re-judge it), the call still stumps if the register's cause labels are blank. This is consistent with the note: B is reached from the layout's pixel geometry, the route join, and the per-request slip rates by experience, which live in the layout export and action logs, not in the register's labels.
- **Is the decisive step rejecting a wrong number?** The banned shape would be spotting a wrong figure and flipping it. Here no figure is wrong: the investigators' findings are honest records. The decisive step is building the exposure-normalised counterfactual (routes by drawn exit separation x request counts x signaller experience, clause 2.3 but-for) from two systems. Rejecting A's 8,240 is a consequence of that, not the work. The thread's residual doubt, that a reviewer may read the rejection of the recorded cause as the whole difficulty, is carried as the finding below. The two-pass family drift (pass 1 analytical_non_defect, surface_read no borderline; pass 2 mixed, yes borderline) is the same borderline read stated twice by independent threads; it does not move any gate.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the card (stump_class analytical, domain_test: error mode by performance shaping factor, field_method) and the note's Three rules. The thread's own analyst route (total by recorded cause, fund A at 8,240, or E) is the one the card names; it did not class the step analytical merely because the method is standard. Nothing here is a landable call by the easy route.

## Stump power (Gate F)
High on the main call: the recorded findings make A the visible leader, and the rate by experience (the textbook reflex) agrees with it; reaching B takes the layout join plus a per-request rate. The asks carry independent hard layers (Central-European mirror log, workstation-wide FAIL rows, 12 sign-on-only substitutions, relief desks, partial covers, a 13-hour night), each silently moving cells. No landable-by-textbook flag.

## Findings, ranked
1. Solution step 7 says "counted hours on the clock"; the figures are elapsed hours (13 h on 25 Oct 2025, 11 h on 28 Mar 2026). A grader could accept the nominal-hour W04 cells. Wording repair.
2. Solution step 8 states server B's copies "sit one hour behind in winter and two in summer"; they sit 1 h (winter) and 2 h (summer) ahead. Wording repair.
3. Second-anniversary day (3 shifts, W01 24 h, W04 12 h) is an unstated convention. File it in the solution (the day itself is outside the first two years), or optionally one prompt clause on the window (a WHAT).
4. FAIL-row convention and sign-ons over roster + changes not stated in the solution.
5. Residual Gate G risk: a reviewer who reads the rejection of the recorded cause as the whole difficulty. Not a determinism failure; routed to the author.
6. Minor realism: templated register summaries, all-OCF `resp`, undefined ARS reason codes.

## Next action for the author
**Gates failing: none of G or H; the FIX_NOW is the solution text and ask conventions only.** The failing items are the determinism-wording items (steps 7 and 8) and the unstated conventions F2 to F4 on 4 to 30 supplementary cells; no input file, the main call, the stump or the ladder moves. Spec gates all pass. This was the architecture's one re-judge; the repairs are ask-layer and wording repairs that spend no architecture and need no further judge rerun. Reword step 7 (elapsed hours, 13 h on 25 Oct 2025 and 11 h on 28 Mar 2026) and step 8 (B's stamps run one hour ahead of A in winter, two in summer), add the anniversary-day, FAIL-row and sign-on conventions to the solution or rubric notes, rebuild if any golden text moves, and re-run only the free gates. If the author instead files the anniversary day as a prompt clause, that edits prompt.txt, so run voice-check and figures_check but not the judge again.
