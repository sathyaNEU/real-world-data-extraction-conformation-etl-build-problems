# determinism-check report, task305, 2026-10-27

Stage: `/build` stage 4, architecture 2 loop 1 (redesign after the portal's FAILED_TO_STUMP on architecture 1 /
architecture 2's prior loop). target.zip sha256 `c91a09a227bb736541a8ca782fa0e7e28313ac3d13491d5609d5ceb8c3411b52`
(prefix matches the one cited at invocation). Fresh unzip used by the judge thread:
`/tmp/determinism-check-task305-loop1/target/`.

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE, with one non-blocking FIX_NOW note (re-verify the 15%/8%/17% recovery shares against
the generator; no rerun of model responses required, since the thread's independent recomputation left the
site pick and the rounded GBP 0.8 million unchanged under every operationalization it tried).
**Stumping type:** mechanism: `method_or_model_selection` (secondary: a vintage/grain-matching `binding_constraint`); stumping_family: `analytical_non_defect`; surface_read_dependency: `no`; sole_data_defect: `no`.

## Why
The main recommendation and ask 2 are forced by two filed facts the judge thread traced to specific VOA
rows: (1) `spend_share_model_2025.pdf` section 1 scopes the spend base to include "anyone else's [spend],
at the place where they are staying," which rules out the residents-only sub-total (S1 GBP 0.4m) as the naive,
incomplete reading, not an equally licensed alternative; (2) section 2 says the model shares spend among the
stores "trading when it is made, at their floor area then," which forces the FY2025/26 vintage (store 105 =
945.05 m², store 107 = 1,007.66 m², Raddleford Water = 480 pitches, Withybeck Lakes = 400 pitches) over
today's post-extension list, ruling out the GBP 0.5m inversion-on-today's-list reading. The one remaining free
choice in the prompt/files (what "the store's own November to February monthly level" means: average, min, or
max of the four months) moves the per-pitch rate from GBP 2,451 to GBP 2,645, but every one of the three
conventions rounds S3's addition to the committed GBP 0.8 million, so this fork does not disturb the main call.

## Recomputation ledger
(from the judge thread's independent recomputation against the fresh unzip; not re-run by this pass)

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Store 105 floor area, FY2025/26 | 945 m² | 945.05 m² (UARN 70511887) | Yes |
| Store 107 floor area, FY2025/26 | 1,008 m² | 1,007.66 m² (UARN 94436352) | Yes |
| Store 105/107 floor area, today's list | n/a (named as the wrong vintage) | 1,412.78 / 1,490.33 m² | Yes, confirms the trap is data-native |
| Raddleford Water pitches, FY2025/26 | 480 | 480 (current 1 Apr 2023 - 31 Mar 2026) | Yes |
| Withybeck Lakes pitches, FY2025/26 | 400 | 400 | Yes |
| Raddleford Water / Withybeck pitches, today | n/a (the wrong vintage) | 640 / 520 | Yes |
| Wrentoft Lakes pitches, today's list | 1,750 | 1,750 (vs 1,450 FY2025/26) | Yes |
| Qualifying grocery stores (>=280 m²) | 27 | 27, both periods | Yes |
| Out-of-region card spend seasonality | a season/baseline step | ~GBP 34k-88k Mar-Oct vs ~GBP 13.6k-14.9k Nov-Feb | Yes, forces the split |
| Per-pitch rate, GBP | 2,550 | 2,554 (avg Nov-Feb) / 2,645 (min) / 2,451 (max) | Average matches; all three round S3 to GBP 0.8m |
| S3 addition | GBP 0.8 million | GBP 0.8 million under all three Nov-Feb conventions | Yes |
| Recovery shares (Raddleford/Withybeck/Sallowmere) | 15% / 8% / 17% | 12.3% / 7.5% / 15.1% | **No** -- same ranking and order of magnitude, 1.5-2.7 pts low on two of three; source of gap not found within the review budget |
| Case-rejection threshold (ask 3 device) | a dwell-time cutoff | zero DEL stops within 2 minutes of the boundary | Yes, clean gap, not an arbitrary line |
| Cases/hours/bus totals for all 10 stores / 6 sites (asks 3-5) | ten+ten+six figures | not independently executed this pass (time-boxed) | Not verified |

## Competing answers that survived
None on the main call. The one genuinely live competitor the thread stress-tested is the residents-only
reading (S1 GBP 0.4m > S3 GBP 0.1m), which is the solution's own step-1 intermediate figure; it survives only
by ignoring section 1's explicit "anyone else's spend" scoping clause, so it is the designed naive route, not
a defensible fork. The Nov-Feb "monthly level" fork (average/min/max) produces three different per-pitch
rates but the same rounded GBP 0.8 million, so it does not survive as a competing *answer*.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | >=10 | 23 files | Pass |
| Format mix | >=3 formats | csv, txt, xlsx, pdf, zip (5 formats) | Pass |
| Large file | >=25,000 rows or large DB | `ta_punches_...csv` 108,741 rows; `wfm_paid_hours_...csv` 60,976 rows | Pass |
| Distractors named in metadata, not in filenames | >=2 | `dft_aadf_count_points_lq_2025.csv`, `customer_survey_store_scores_2025.csv` in `metadata.json.distractor_files`; neither filename says "distractor" | Pass |
| Distractors relevant but unused | each | AADF traffic counts (plausible footfall/accessibility confound against the bus-departure ask) and customer survey scores (plausible site-quality confound against the appraisal) are both grepped-absent from `generator/checks.py`'s `DISTRACTORS` read-check (`"aadf" not in src`, `"survey" not in src`) and are never referenced in `SOLUTION_STEPS` | Pass |
| A distractor reproduces arithmetically, ruled out by a shipped fact | at least one | Not demonstrated: neither AADF counts nor the survey scores arithmetically reproduce a graded ask value under any plausible misreading found in the design note or ladder; they read as classic unused-but-plausible confounds, not a reproduce-then-rule-out trap | **Weak / not evidenced** -- not blocking, see Findings |
| Deliverables | 1-3, all in golden, no required format family | `marrable_site_appraisal_2027.xlsx`, `new_store_case_2027.docx`, both present under `golden/` | Pass |
| Asks multi-dimensional, unit+rounding stated | yes | Cases (10 stores, reject-and-redeliver device, SF28), hours (10 stores, shift-pairing + night-shift-grain device, SF29), buses (6 sites, GTFS block_id dedup across a service day past midnight, SF30/SF24/SF25) -- each carries its own silent device, not a flat lookup; unit and rounding stated in the prompt's last sentence | Pass |
| Prompt shape identifiable, rubric >=25 criteria | yes | Main site pick + main dollar figure + 10 case figures + 10 hours figures + 6 bus figures = 28 separately gradable numeric items, before recommendation/critical-component criteria | Pass (by count; rubric file itself not inspected, out of scope for this pass) |
| Not LLM-generated; goldens read as real work product | yes | Judge thread: no LLM-authorship tells, no benchmark/authoring disclosures in any opened file; VOA/ONS/GTFS layouts carry real-world incidental mess (overlapping list-entry versions, forgotten punches, rejected-and-redelivered loads) | Pass |

## Gate G reconciliation
Design note's own `Strategy` line (Draw section) files Gate G as `decomposition_attribution`; the card
(`stump_class: analytical`) and the design note's `## Three rules` / `analyst_test` / `domain_test` describe the
decisive step as recovering a park's spend through the modelled share at the FY2025/26 vintage, versus the
easy route of inverting on today's list. The judge thread independently classified the mechanism as
`method_or_model_selection` with a secondary vintage/grain-matching `binding_constraint`, `stumping_family:
analytical_non_defect`, `surface_read_dependency: no`. These are different taxonomy labels for the same
non-banned shape: both agree there is no reported/surface figure the solver must catch as "wrong" and flip
away from (the naive path is an *omission* -- stopping at residents-only -- plus a *vintage mismatch*, not a
corrected defect in a stated number). The thread did not name either declared distractor (`aadf`, `survey`) as
carrying the surface read, and neither distractor is load-bearing in its stumping account. This is a
label mismatch, not a substantive one, and does not predict a send-back.

## Gate H reconciliation
Thread: `domain: pass`, `layers: pass`, `decisive_step: analytical` -- H1 the swap test fails to preserve the
task (no hospital/utility analogue has an origin whose demand is observed only as one rival's floor-area-and-
distance share of it); H2 names Layer 1 (VOA list versioning, mid-year floor-area extensions, forgotten TA
punches, GTFS services running past midnight) and Layer 2 (scoping the spend base to include visitor spend,
and vintage-matching the floor areas/pitch counts to the period the calibrating card spend was recorded) in
one line each; H3 names the easy route (stop at the residents-only gravity-model sub-total, filing S1) as the
wrong answer a strong analyst who read everything correctly could still reach, so decisive_step is analytical.
This matches the design note's `domain_test` and `analyst_test` almost verbatim (same easy route, same wrong
figure, same field-method mechanism), and matches the card's `stump_class: analytical`. No mismatch; this is
the strongest signal against a send-back on Gate H.

Per the instructions on a landable call: the thread classes the decisive step analytical because a capable
analyst applying the field's own standard spatial-interaction / share-recovery method, with no judgment call
the data had to settle beyond vintage-matching, still lands on the wrong figure the easy way. This is recorded
here, under stump power, as a textbook route a strong solver takes (`stumping` 1.3) rather than as a weakness;
the main thread should weigh it against the design note's ladder (R0-R7), which already shows the decisive
step is worth 6.6x on the per-pitch price and separates S3's margin from 0.238 to 0.801.

## Stump power (Gate F)
The judge thread estimates real stump power: a model must (a) include visitor/holiday-park spend rather than
stopping at residents-only (the R0-R3 rungs on the ladder, which all still name S1), and (b) vintage-match the
floor areas and pitch counts to the FY2025/26 state the card feed actually measured, rather than the current
list (R4, which still mispicks the dollar figure at GBP 0.5m rather than 0.8m). Both are genuine data/structure
traps native to the VOA list's own versioning, not planted decoys, consistent with the design note's ladder
and `No decoy:` line. The one unresolved item -- the thread's own gravity-model recomputation of the
15%/8%/17% shares came out 1.5-2.7 points low on two of three -- does not appear to threaten stump power or the
rounded headline figure (per the thread's sensitivity sweep), but is flagged below as a finding needing the
author's own generator re-check.

## Findings, ranked
1. **(Non-blocking, needs author verification) Recovery-share discrepancy.** The judge thread's independent
   gravity-model rebuild of the three recovery shares came out at 7.5% / 12.3% / 15.1% against the committed
   8% / 15% / 17% (CRITICAL_COMPONENTS item 2) -- same ranking, same order of magnitude, 1.5-2.7 points low on
   two of three. The thread could not find the source of the gap within its review budget (checked duplicate
   UARNs, road-factor variants, date-window logic) and did not fail the gate on it because the downstream
   per-pitch rate and the rounded GBP 0.8 million addition reproduce under every Nov-Feb-window convention it
   tried. **Fix location:** solution (re-run `generator/checks.py` / the share computation against the
   thread's method and confirm 15/8/17 is what the generator's own clean truth produces; regenerate the
   CRITICAL_COMPONENTS block only if a real discrepancy is found). No prompt or input-file change, no model
   rerun.
2. **(Informational) Asks 3-5 not independently executed this pass.** The thread traced the rules for cases
   (reject-and-redeliver detection, SF28), hours (shift-pairing by terminal not location, night-shift grain,
   SF29), and buses (GTFS block_id dedup across a service day past midnight, SF24/SF25/SF30) to specific
   shipped files and spot-checked the cases threshold (a clean gap, zero DEL stops within 2 minutes of the
   boundary), but did not compute the full ten-store/six-site totals end to end. **Fix location:** none
   required to ship on this pass's evidence; if the author wants full confirmation, it is a re-run of the
   same judge thread's Bash recomputation on these three asks specifically, not a design change.
3. **(Informational) Spec-gate "distractor reproduces arithmetically, ruled out by a fact" not evidenced.**
   Neither `dft_aadf_count_points_lq_2025.csv` nor `customer_survey_store_scores_2025.csv` was found, in the
   design note or ladder, to arithmetically reproduce any graded ask value under a plausible misreading before
   being ruled out; they read as ordinary unused-but-relevant confounds (traffic volume vs the bus-departure
   ask; survey satisfaction vs the site appraisal). This is weaker than the ideal spec-gate shape but is not a
   determinism or Gate G/H defect, and the input-gate's floor (>=2 relevant, unused, named distractors) is
   otherwise met. **Fix location:** none required; optional future hardening only if the author wants a
   reproduce-then-rule-out distractor specifically.

## Next action for the author
Re-run the generator's own gravity-model share computation for the three recovery shares (15% / 8% / 17%)
against the method in CRITICAL_COMPONENTS item 2 and confirm it matches; if it does not, regenerate that one
solution block (and only that block) before shipping -- everything else on this pass is APPROVE.
