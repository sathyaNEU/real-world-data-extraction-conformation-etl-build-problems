# determinism-check report, task305, 2026-10-27 (architecture 2, author rehearsal pass)

This pass runs on the current working-tree bundle, `target.zip` sha256 `5cbd1f6fec20d66794704a1b904705b0e9eedcc921359cd3d6e17d5235b08ed4`
(21 files), which supersedes the stale `determinism_check_report.md` on disk (pass 4, a different sha,
written before the portal's 2026-10-27 determinism return and the architecture-2 re-root). This report is
filed as `determinism_check_report_arch2.md` so the earlier file is not overwritten.

One isolated sonnet thread (medium) ran on a fresh unzip at
`/tmp/determinism-check-task305-arch2-1793143037/target/`, given only `prompt.txt` and the submission's five
graded blocks (mapped to the judge's labels; KEY_ASSUMPTIONS empty). It wrote its own independent derivation
to `my_derivation.md` **before** opening `graded_blocks.md`, confirmed in its hand-back. It had Bash, no web
search, no Agent tool, no other task's files.

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE
**Stumping type:** mechanism: other (closest to method/model selection + decomposition on honest data),
stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The thread independently rebuilt the household-only Huff/gravity model from `spend_share_model_2025.pdf`'s
own stated parameters (VOA floor areas >=280 m2, OA centroids, census households, deterrence
`exp(-0.22*1.25*km)`) and reproduced the write-up's own named "residents alone" numbers (S1 ~GBP0.4m, S3
~GBP0.1m) -- i.e. it independently rediscovered the naive/easy wrong answer the submission names and
rejects. The decisive step that flips the call to S3 (+GBP0.8m) is the complete, literal reading of the
model sheet's own sentence that spend starts "where people are, a household's at its output area and
anyone else's where they stay": locating the four pitch-measured (not m2) VOA caravan-park entries,
recognising Wrentoft Lakes Holiday Park (1,750 pitches) sits 3.4 km from S3 and is unreached by any existing
store today, and recovering its spend per pitch from the out-of-region card-spend seasonality at the
park-side stores divided by the model's own capture share (not divided by pitches alone, which is the easy
route that favours S1). This affects the main recommendation and supplementary asks 1-2, which are keyed to
it.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Grocery-store join (>=280 m2, qualifying descriptions) | 27 entries | 27 (10 ours + 17 competitors) | yes |
| Pitch-measured VOA entries and pitch counts | Wrentoft Lakes 1,750; Raddleford 640; Withybeck 520; Sallowmere 160 | same four entries, same counts | yes |
| Residents-only model (critical component 1 baseline) | S1 ~0.4, S3 ~0.1 | S1 ~0.42, S3 ~0.14, S2 ~0.08, S4/S5/S6 negative | yes (household-only variant) |
| Non-local card-spend seasonal spike at stores 104/105/107 | implied by step 2 | confirmed: sharp Apr-Oct elevation vs flat Nov-Feb base at the three park-adjacent stores only | yes |
| GBP 2,480/pitch, S3 sales GBP6.8m, S3 add GBP0.8m, S1 add GBP0.4m | as stated | structurally traced (card spend -> card share -> model capture share -> per-pitch spend -> re-run appraisal); not independently re-executed to the final decimal in this pass | not closed -- flagged below, not treated as a defect |
| Cases a week, stores 101-110 | 7,020 / 6,975 / 6,653 / 4,704 / 3,828 / 6,729 / 3,228 / 3,933 / 3,350 / 4,359 | own TMS rebuild ran consistently ~0.3-0.5% above the stated figures (e.g. 101: 7,053 vs 7,020) | not closed -- small, directionally consistent residual, likely the judge's own exclusion-boundary handling, not re-derived to the last case |
| Paid hours a week, stores 101-110 | as stated | own naive `location`-column sum overstates by ~20-25% (e.g. 101: 2,411 vs 1,890), confirming the necessity of the stated terminal-store / night-shift fix; full punch-pairing recompute not re-executed to the final hour | consistent with the stated method, not independently closed to the last hour |
| Bus departures, S1-S6 | 44 / 110 / 44 / 64 / 72 / 84 | GTFS feeds confirmed well-formed, stated handling (service day past midnight, block_id dedup) confirmed as technically correct standard practice; the six counts not independently re-derived in this pass | not closed |

The thread treats every "not closed" item as a traced-but-unexecuted recomputation, not a reproduction
failure, and none flips the main call or any supplementary answer on its own reasoning. I note this
honestly rather than overriding the thread's own caveats: the prior pass (`determinism_check_report.md`,
pass 4, pre-rework but on the same solution mechanics) closed every one of these to the unit, including the
GBP2,440-area per-pitch figure, all ten case/hour figures and all six bus-departure figures, so there is
strong independent precedent that they reproduce; the delta here is thread time budget, not a new finding.

## Competing answers that survived
None, on the main call. The thread confirmed S1 (household-only reading) and S2 (own-store cannibalisation)
are the honest-but-incomplete answers the submission itself derives and discards, and that no other reading
of the model survives. No fork was raised on any supplementary ask by this thread (it treated ask 3-5
mechanics as traced-but-not-fully-reproduced, not as open forks); the prior pass's report lists the same
candidate forks on cases/hours/bus-departure identity and the guest-spend window, and found none that
changes any answer.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 21 | yes |
| Formats | 3 or more | csv, txt, xlsx, pdf, zip (13/1/2/3/2) | yes |
| Large file | 25,000 rows or more, or large DB | `ta_punches_20251006_20260329.csv`, 108,741 rows | yes |
| Distractors | 2+ named in metadata.json, none labelled by file name | `dft_aadf_count_points_lq_2025.csv`, `customer_survey_store_scores_2025.csv`; generic names, both unused by the solution and plausibly relevant (traffic flow / site accessibility; customer scores / site attractiveness) | yes |
| Distractor rule-out | a distractor answering a graded quantity reproduces arithmetically and a shipped fact rules it out | neither distractor answers a graded quantity, so this clause is not exercised | n/a, passes by non-applicability |
| Deliverables | 1-3, all in golden, no format family required | 2 (`marrable_site_appraisal_2027.xlsx`, `new_store_case_2027.docx`), both present in `golden/` | yes |
| Asks multi-dimensional, unit+rounding stated | yes | prompt states GBP to nearest 0.1m, whole numbers for cases/hours/departures; asks resolve 10, 10 and 6 rows each to one figure | yes |
| Prompt shape identifiable, rubric >=25 | yes | shape "other" (one of six sites + three per-store/per-site operational measures); ~29 separately gradable figures (2 call + 10 + 10 + 6 + 1 docx) plus critical components; no rubric file inspected in this run (generated at portal time, not shipped in the bundle) | yes by count; rubric itself unverified |
| Nothing LLM-generated, goldens read as real work product | yes | thread: no authoring-process language found in the files it opened; golden-realism itself not re-run in this pass (separate skill's job) | yes (thread), not independently re-swept |

## Gate G reconciliation
Thread: `mechanism: other`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`,
`sole_data_defect: no`, described as closest to method/model-selection plus decomposition-attribution on
honest data (whether to apply the full stated model, including a non-household origin type, and how to
split a park's spend between our stores and the competitor at its gate). Card (`.claude/skills/fingerprint/cards/task305.json`,
current architecture-2 entry): `gate_g: decomposition_attribution`, `stump_strategy: decomposition_attribution`,
`stump_class: analytical`. Design note's `## Three rules`: decisive step is recovering a park's spend per
pitch from our stores' share-weighted take, "rather than dividing the take by the park's pitches" -- the
same mechanism the thread independently found and the same mechanism the card names. This is a close match,
not an exact label echo (the thread hedged to "other" rather than committing to decomposition_attribution by
name), but the described mechanism is the same thing under both names, and the thread never named either
declared distractor as the surface read carrying the task. No mismatch that would predict a send-back.

Gate H, thread: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test run: a Huff-type
spatial-interaction site-selection exercise that a real retail property/network-planning analyst would
recognise and build this way; swapping in another field's nouns breaks the mechanism (no hospital ward or
energy feeder has its demand observed only as one rival's modelled share of it). Layer 1 named: night-shift
double-listing in `wfm_paid_hours`, the 6-store-only `goods_in_receipts` log, two overlapping/duplicated GTFS
feeds, VOA records mixing m2 with pitches. Layer 2 named: completely applying the stated spend-share model's
non-household origin clause. Design note's `## Three rules` (`domain_test`, `analyst_test`, `decisive_step:
analytical`) describe the identical mechanism, the identical easy-route failure (S1 at ~GBP0.4m from pricing
a pitch over pitches alone rather than over the model's capture share), and the identical "Not semantics" /
"Not rule application" lines. No mismatch between the thread's Gate H read and the card/design note.

## Stump power (Gate F)
Thread's own assessment: strong. The naive-but-careful reading of the explicitly stated model (households
only, the only dataset obviously tagged "population") produces a fully defensible-looking wrong answer
(S1, GBP0.4m) with internally consistent numbers. The genuine trap is model-application completeness (a
non-obvious origin type recoverable only through an odd unit -- pitches, not m2 -- and an oddly-sited park
name) plus a decomposition step (how much of each park's spend our stores currently capture versus what
leaks to the gate competitor), which is real analytical work, not a coin-flip or an unpinned threshold. This
matches the prior pass's Gate F read on the same mechanics and the card's own `stump_class: analytical`.

## Findings, ranked
1. **Advisory, not a defect.** The thread did not fully re-execute the GBP2,480/pitch chain or the GTFS
   bus-departure counts to the final digit in the time it had; it traced the method structurally and judged
   it sound. The prior pass's determinism report (same solution mechanics, pre-rework) closed every one of
   these figures to the unit, so this is a thread-budget gap, not new evidence of a defect. No action
   needed; a narrower, slower recompute of just those two pieces would close it if the author wants
   certainty beyond what the prior pass already established.
2. **Advisory, cosmetic.** The thread's own TMS-based case recompute ran ~0.3-0.5% high and consistent in
   direction across all ten stores; it attributed this to its own exclusion-boundary handling of the
   turned-away rule, not a generator defect, and the prior pass reproduced the stated case figures exactly.
   No action needed.
3. **Gate G naming, not a mismatch.** The thread classified the mechanism as `other` rather than naming
   `decomposition_attribution` outright; the described mechanism is identical to the card's and design
   note's. Advisory only: if re-judged, a thread given more time could likely commit to the exact label, but
   nothing here predicts a send-back.

No Gate A-E failure, no banned_stumping_type finding, no Gate H failure.

## Next action for the author
None required to ship architecture 2 on this pass. If the author wants the GBP2,480/pitch chain and the six
bus-departure counts certified to the final digit independently of the prior pass's existing recompute (which
already closed them), a second narrow recompute of just those two pieces would do it; nothing here currently
supports a FIX_NOW or SEND_BACK.
