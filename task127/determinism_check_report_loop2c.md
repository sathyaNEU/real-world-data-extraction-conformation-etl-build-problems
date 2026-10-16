# determinism-check report, task127, 2026-10-16 (final cut, loop 2c)

Judge thread on the final cut: working-week waits redrawn, acute notes gained the sentence "A patient counts as delayed in a month when at least one of these nights is dated in that month". Packages unchanged (508/350/120/222/0); bed-days 6,816. Supersedes loop2 and loop2b for values and asks.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (no fix required)
**Stumping type:** mechanism: binding_constraint (thread: borderline with counterfactual selection; earlier passes said decomposition_attribution, same step), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Allocation note SF-2026-14 values a package at the nights by which it would have shortened the stay; the ICES notes say hospital-discharge equipment is needed from the day the patient goes home; orders carry required_by equal to the ready date; 195 of Ashby Vale's 361 covered patients left on the day their equipment arrived. Valuing from the later of ready date and delivery gives 6.39/5.82/5.35/4.01/3.14 (RM, WB, HI, CP, AV); caps 508/350/120/285/361, 1,200 packages, so 508/350/120/222/0. Only competing answer, nights after the ready date (AV and CP first, 10,507 bed-days), fails the note's own definition of a package.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Latest submission per spell | 65,524 rows to 64,976 spells | same | yes |
| Covered patients | 508/350/120/285/361 (1,624) | same (merged practices count, Severnside N83 excluded) | yes |
| Equipment join | 794 delivered | 822 patients, 794 delivered, 28 cancelled-only; no delivery after discharge | yes |
| Nights freed per patient | 6.39/5.82/5.35/4.01/3.14 | 6.392/5.820/5.350/4.007/3.141 | yes |
| Naive nights after ready | AV 10.81, CP 9.86; 10,507 | same | yes |
| Split and bed-days | 508/350/120/222/0; 3,247/2,037/642/890/0 = 6,816 | same (unrounded 889.56 at CP) | yes |
| Chart bed-days (ward at midnight) | total 24,295 | 24,295; every hospital-month bed-day and patient cell matches (e.g. Ashby 2,057/1,989/1,678 and 316/305/274; Marchford 2,010/1,966/1,729 and 412/432/397) | yes |
| Referrals <=7 days | Marchford 178/228/166, Ashby 57/55/53, Teme Valley 106/103/95 | same | yes |

## Competing answers that survived
1. Main call: the valuation sentence does not say "equipment"; the files force the join. A solver ignoring the join gets 10,507 and the wrong order (the intended trap, not a fork). Excluding the 28 cancelled-only patients is not licensed by the note.
2. Chart attribution: ward at the midnight (golden) vs discharging site_code (moves 643 of 24,295 nights; e.g. AV December 1,978 (302) vs 2,057 (316)). The thread calls the ward reading the natural one ("occupied bed-days lost" at a hospital, ward stays shipped).
3. First vs last spot service_start: pinned by the council notes (lines after the break carry the day care resumed); first is the filed reading (last would give Ashby January 53, Marchford January 226).
4. "Took" population: no effect (only referrals with a care start count).

## Optional prompt pin: declined
The thread's optional pin (state the hospital a delayed night counts at) is declined by the author. Reasons recorded: that attribution is Ask A's primary device A1 (the spell carries the discharging site while the ward stays carry where the patient was); every judge pass (loop2, 2b, 2c) has called the ward-at-midnight reading the natural one and none has found it to flip to a defensible alternative; pinning it in the prompt would hand the device over. The residual fork is therefore accepted and left open on purpose, as a device, with the shipped ward stays and the midnight-census note as the closing evidence. Reviewer note: this is a judgment on a stated device, not a gap I verified independently.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | >=10 / >=3 | 16 / 4 (csv, txt, xlsx, pdf) | yes |
| Large file | >=25,000 rows | 138,606 ward stays (metadata), 65,524 discharges | yes |
| Distractors | >=2 named in metadata, none in a file name | weekly return, bed census, reablement outcomes | yes |
| Distractor relevance | unused, weighs, ruled out by shipped fact | weekly return and census cannot rank hospitals on the call (trust level, all ages); weekly return carries the naive basis, ruled out by the package definition and delivery data | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg) | yes |
| Asks | multi-dimensional, unit and rounding | 9-cell grid, 15-cell two-measure chart, whole numbers stated | yes |
| Prompt shape / rubric >=25 | identifiable; >=25 | shape 05 in metadata; gradable figures far above 25 (inferred) | yes |
| Realism | none LLM-read | authentic Layer 1 mess, provenance log, no authoring leakage | yes |

## Gate G reconciliation
Thread: binding_constraint (borderline counterfactual selection) / analytical_non_defect / surface_read no / sole_data_defect no. Card (.claude/skills/fingerprint/cards/task127.json): stump_class analytical, analyst_test = value at nights after the ready date and fill AV and CP first, domain_test = counterfactual length of stay with one discharge dependency removed. Design note Decisive step: valuing a package at the later of ready date and equipment delivery to discharge; mechanism per earlier passes decomposition_attribution. The mechanism label differs between passes (binding_constraint vs decomposition_attribution) but the thread's decisive step, easy route and wrong answer are the same as the card and note; I treat this as a labelling variance, not a mismatch. The declared distractor (weekly return) supplies the naive figure but does not carry the task; the same figure comes from the discharges file. Thread's caveat: if live runs show failure only on the missing word "equipment", route to live testing as a single_conceptual_flip.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the card and the design note's Three rules.

## Stump power (Gate F)
Good. The easy route is the national-collection concept (nights after ready), shown in the extract notes and weekly return, and it flips the headline (Ashby Vale 0 to 361; 10,507 vs 6,816). Asks add a second trap (Closed referrals with spot-purchased care, first service_start, received-date month) and the attribution device A1.

## Findings, ranked
1. Residual chart-attribution fork (15-cell ask), accepted as device A1; pin declined.
2. Mechanism label variance across passes (see Gate G); no action.
3. Live-test watch: failure only on the missing word "equipment" would indicate a conceptual flip.

## Next action for the author
Ship the final cut on this verdict; no prompt change and no further judge pass.
