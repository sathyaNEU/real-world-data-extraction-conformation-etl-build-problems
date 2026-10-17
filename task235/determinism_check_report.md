# determinism-check report, task235 (architecture 2), 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The single judge thread (sonnet, medium, scratch /tmp/determinism-check-task235-a2-218315) recomputed every load-bearing value from the fresh unzip. Everything reproduced. The main call follows from KC-DQ-04 s.4 ("lost only if it never will") plus the SDK notes (the queue stays on the phone until the game starts). Only Android 7.41.0 (6.34, none open) and iOS 7.42.0 (3.10 floor, 5.57 ceiling) can exceed 2 per cent. Every other build is either capped at or under 2 per cent with all missing events lost, or would need 24 to 33+ per cent of its open events lost against at most 2 per cent of resolved gaps. The settle-window and account-next-session readings are closed by shipped facts (lag data; device-held queue, e.g. iOS 7.40.0 54 of 76 open events show a later session on another device).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Purchases in scope | 15,705 | 15,705 | yes |
| Matched / missing / lost / open | 15,204 / 501 / 204 / 297 | same | yes |
| Android 7.41.0 lost | 157 of 2,477, 6.34 | same, 0 open | yes |
| iOS 7.42.0 | 10 lost, 8 open of 323, 3.10 floor, 5.57 ceiling | same | yes |
| iOS 7.41.0 | 8 of 1,447, 0.55 | same | yes |
| Paying players (12 builds) | 377, 294, 855, 890, 1,362, 275, 386, 293, 669, 1,392, 1,538, 320 | identical (union-find over links + guest accounts joined by session file) | yes |
| Gross bookings per paying player (12) | 9.93, 10.39, 8.23, 8.08, 11.73, 5.58, 9.86, 9.82, 7.03, 8.99, 9.91, 5.58 | identical; half-up, half-even and unrounded lines give the same cent (nearest boundary 0.0015, iOS 7.40.0) | yes |
| Android 7.42.0 resolved gaps | 62, none stayed missing | 74 under the judge's wider definition (late-or-missing with later session), 0 stayed missing | count differs by definition only; conclusion identical |

## Competing answers that survived
None. Forks examined and closed: settle window (lag data, SDK notes), same-age comparison (Android 7.42.0 alert, closed by session-resolved gaps), account vs device next session (SDK notes), links-only player count (1,412 or 1,406 vs 1,392 for Android 7.41.0; closed by catalogue s.6, dictionary "not a register of every account", session file), half-up/even rounding (no cell moves), JPY/KRW minor units and ECB weekend rate (filed).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 13 | yes |
| Formats | 3+ | 4 (csv, md, xlsx, pdf) | yes |
| Large file | 25,000+ rows | session_service_starts 325,515 rows | yes |
| Distractors | 2+ in metadata.json, none named by file | 3 (crash_free_sessions_by_build, store_ratings_by_version, push_campaigns_2026-10); file names do not label them | yes |
| Distractors unused yet weighable | yes | none answers a graded quantity (judge found none carrying the call); not independently arithmetic-checked by me | yes (judge) |
| Deliverables | 1 to 3, all in golden | 2 (CSV, PNG), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per build: alert, paying players, euro per paying player to the cent; prompt states euro and nearest cent | yes |
| Prompt shape, 25+ criteria | identifiable, 25+ | shape 10 scorecard; 12 builds x 3 fields + chart + call gives well over 25 (rubric itself not in the folder, not verified) | yes (inferred) |
| Not LLM-looking; goldens real | yes | judge found README and DATA_DICTIONARY clean; golden realism not separately reviewed by me | yes (judge) |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: strategy maturity_censoring (G12 decisive), stump class analytical, no planted decoy, nothing in the pack states a loss or alert. Match. Declared distractors (crash-free sessions, ratings, push campaigns) were not named by the thread as the surface read carrying the task. Gate G holds: no shipped artifact ranks the builds wrongly. The thread's stated easy route (settle window or same-age rate) agrees with the note's ladder rungs 0 to 2; the note's default path ends 5 of 12 wrong (iOS 7.42.0 missed), the thread's wording lists the alerted old builds plus the 7.42.0 pair; same family, no conflict.

## Stump power (Gate F)
Decisive trap is right-censoring of open events. Settle-window, pooled-curve, same-age and account-next-session routes each land on a wrong set. Risk flagged by the thread: catalogue s.4 and SDK notes partly pre-disarm the trap, so a strong model may clear the main call and the asks (players union through the session file, per-line euro rounding) would then carry the difficulty. Optional lever, would need a rerun: shorten the s.4 hint. Not a determinism issue.

## Gate H
domain: pass | layers: pass | decisive_step: analytical. Layer 1: Irish date vs UTC, duplicates and restores, sandbox/test/renewals, JPY/KRW units, ECB weekend rates, guest accounts. Layer 2: loss on a right-censored population of pending events. Matches the note's Three rules (No decoy, Not semantics, Not rule application) and the card.

## Findings, ranked
1. Low: the submission says Android 7.42.0 has 62 resolved gaps; the judge's wider definition counts 74 (the note's margin says 22 per cent of 34 open, judge says 24 per cent, 8 of 34). Both are zero stayed missing and the margin is wide. Optionally state the "resolved gap" definition in the submission or align the number; no graded figure moves.
2. Info: cross-batch fingerprint not run by the thread (no other tasks in scope).
3. Info: stump-power lever above.

## Next action for the author
None required for determinism; proceed to ship after the leak reader's findings. Optionally align the "62" resolved-gap wording in submission.md section 1 and the note.
