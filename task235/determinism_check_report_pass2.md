# determinism-check report, task235, 2026-10-31 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (right-censoring of the loss rate), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One judge thread (sonnet, medium, scratch /tmp/determinism-check-task235-r2/, fresh unzip of target.zip sha256 prefix 526ac9335f1fb56b) recomputed every load-bearing value from the bundle. The main call follows from the catalogue (KC-DQ-04 s.4: an event not arrived by the run is lost only if it never will) and the SDK changelog 4.6.0 (queue held on the device, uploaded when the game starts). Only Android 7.41.0 (6.34 per cent, none open) and iOS 7.42.0 (3.10 floor, 5.57 ceiling) can reach the 2 per cent line. Every other build crosses it only if about 33 per cent or more of its open events were lost, against at most about 2 per cent of its events still on a phone when the game next opened. Both asks reproduce to the cent for all 12 builds.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Purchases in scope (Production, standard, purchase, Irish date 12 Oct to 8 Nov) | 15,705 | 15,705 | yes |
| Matched / missing at the run | 15,204 / 501 | 15,204 / 501 | yes |
| Missing with a later session on the device / still open | 204 / 297 | 204 / 297 | yes |
| Android 7.41.0 loss | 157 of 2,477, 6.34% | same | yes |
| iOS 7.42.0 loss | 10 lost + 8 open of 323, 3.10% floor, 5.57% ceiling | same | yes |
| Highest other build | iOS 7.41.0, 8 of 1,447, 0.55% | same | yes |
| Android 7.42.0 | 0 lost, 62 of 62 resolved arrived | same | yes |
| Paying players, 12 builds | 275 to 1,538 | exact | yes |
| Gross bookings per paying player, 12 builds | 5.58 to 11.73 | exact (half-up and half-even agree) | yes |

## Competing answers that survived
None. Tested and closed by shipped facts: seven-day settle window (alerts Android 7.41.0 plus Android 7.38.1 and iOS 7.38.2, 7.39.1, 7.40.0; drops iOS 7.42.0; 32 of 93 Android 7.38.1 late arrivals came after day 7); short window and same-age comparison (alerts Android 7.42.0, which has 0 lost against 62 late arrivals); the account's next session (changelog 4.6.0 puts the queue on the device); all unresolved counted lost (contradicts s.4); lower bound only (same list as the golden).
Residual soft spot, no graded figure moves on it: the guest-join phrase "the account its phone shows next" read as the very next session of any account gives different counts (Android 7.41.0: 1,406 against 1,392); catalogue s.6 ("the account it signs in to") closes it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | 4 (csv, md, pdf, xlsx) | yes |
| Large file | 25,000 rows | session_service_starts 325,515 rows | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | 3 (crash_free_sessions_by_build, store_ratings_by_version, push_campaigns_2026-10); none counts a purchase or event; names are neutral | yes |
| Distractor weighs but is unused | yes | judge found none used; they are build-level quality context, ruled out because none counts purchases or events | yes |
| Deliverables | 1 to 3, all in golden | 2 (csv, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 12 builds x (players, bookings per paying player to the cent) | yes |
| Prompt shape and rubric | shape identifiable, 25+ criteria | shape 10 (scorecard against a threshold); 12 builds x 3 fields plus the chart gives well over 25 | yes |
| Prompt | one paragraph, under 1,000 characters | 521 characters, question first | yes |
| Reads as real work product | yes | judge: system-export mess, no authoring language | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (stump sentence, Layer 2 line, item 5 of the pre-ship list) and card: censoring and estimation_fit, analytical, no surface read; card gate_g is labelled method_or_model_selection, a different label for the same analytical family, not a mismatch. The thread did not name the declared distractors as the surface read, and none carries the task.

## Gate H
domain: pass; layers: pass; decisive_step: analytical (judge each missing event against the next session of the phone that made the purchase, and complete the few still open at the build's own resolved share). Matches the note's Three rules (No decoy, Not semantics, Not rule application) and the card (stump_class analytical, analyst_test, domain_test). The note's analyst test (settle window files 5 of 12 builds wrong) agrees with the thread's reproduced counts.

## Stump power (Gate F)
Moderate. The catalogue's "never will" sentence and the changelog's start-time upload let a strong solver reach the censoring; that route is a landable call, so the asks carry the bar, as the design note already says. The easy routes (seven-day window, account's next session) each file a wrong list and are closed by shipped data, not by a withheld rule. The main thread should weigh this against the note's ladder.

## Findings, ranked
1. No blocking finding.
2. Low: DESIGN_NOTE.md item 7 says 13 files; the bundle and metadata.json hold 11 (all gates still pass). Correct the note.
3. Low, optional: pin in submission step 7 that a guest joins the first later non-guest session on its device, and in step 6 that open events are counted at the rate among events still on a phone at next open. No rerun needed.
4. Info: the chart's bar heights for builds with open events depend on that rate; above or below the line does not.

## Next action for the author
Fix the file count in DESIGN_NOTE.md (13 to 11) and proceed to ship; the optional pins in finding 3 are the only text edits worth considering.
