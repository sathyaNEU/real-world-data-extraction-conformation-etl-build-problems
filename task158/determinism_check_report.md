# Judge verdict, task158 (re-judge after repair, fresh read)

**Verdict:** DETERMINISTIC (main pool call and all supplementary answers reproduce; one rounding-level soft spot on the shortfall figure, below).

**Disposition:** APPROVE. Optional hardening: file the WHAT of the report-call cost basis (rates measured on unreused, one-call-per-session lc2 traffic) so a calibrate-to-the-early-access-tenant reader cannot land on 330. No change to the stump; a rerun is needed only if the pack changes.

**Why:** Docs is forced as the pool. Report calls costed in tokens at the cache-free lc2 rates (0.248 / 1.85 GPU-ms, fitted on batch-prod lc2 hours where requests = sessions_new) give a Docs W13 shortfall of 338.9, so 340, against Code at 299.4, so 300. The only route to Code first (Docs' 1.630 GPU-s per request, or Docs' own cache-inflated token fit) is separated by the shipped early-access report days: those rates predict the tenant's excess busy GPU-seconds within about 5 per cent, Docs' per-request rate predicts about a fifth. Main call and Q1 (shortfall) affected only at the 330/340 rounding edge described in Evidence.

## Evidence (recomputed from the bundle)

| Value | Result | Source |
|---|---|---|
| Rates 0.248 / 1.85 GPU-ms (batch-prod lc2, 4,998 hours, R2 0.9999, requests/sessions_new = 1.0) | reproduced (0.24801 / 1.84997) | fleet_rollup_hourly csv |
| Docs lc2 own fit 0.0403 / 2.348 (requests per session 4.95, cache-inflated) | reproduced; gives Docs 181, Code first | same |
| Close-out GPU-s/request (Docs 1.630 etc.) | reproduced from rollup Q3 (1.6297 etc.) | capacity_closeout PDF vs rollup |
| Report GPUs at W13 (11 signed contracts, go-live Mondays, proposals/early access excluded) | 249.4 (golden 250) | commitments xlsx, tiers |
| Docs W13: 1152.6k x 1.630 / 2520 = 745.5, + 249.4 - 656 | 338.9 -> 340, peak W13 | intake, plan, policy |
| Code W13: 4122k x 0.589 / 2520 - 664 | 299.4 -> 300 | |
| Others W13 | agents 151.5, voice 20.8 (rps x 3600), chat -77.6, batch -80.2 | |
| Early-access check: 295,368 report calls, 5 Oct to 4 Dec; rollup requests and sessions_new exceed app+api by about the call count; billed report tokens equal rollup token excess | reproduced; token-priced excess 2.187M vs observed 2.083M GPU-s (+5%); 1.630/call predicts 0.48M; Docs token fit about 1.17M | docs_usage csv vs rollup |
| Out of service Nov GPU-hours / longest (cordon-to-uncordon, fleetctl + console + by-hand completions, Amsterdam to UTC, month clip, pool at the time, no interval spans a pool move or a month end except clipped ones) | chat 3,630 / 57.4; code 1,110 / 33.7; agents 1,470 / 57.0; docs 1,260 / 57.1 (1,262); batch 810 / 56.0; voice 1,250 / 55.9. All reproduced | fleetctl jsonl, ops console csv, fleet_nodes csv, desk notes |
| Acceptance at 13:00 UTC 4 Dec (latest burn-in run per fitted serial, last fabric run before the review, Gbit/s / 8, 360 GB/s) | R11 48 (hold 2638), R12 40 (2653, 2654), R13 48 (2662), R14 64 (2645). All reproduced; the two 4 Dec re-runs (13:48, 13:55 UTC) fall after the review | nx7 burn-in, fabric, handover csvs, Schedule 3 PDF |

Competing answers stress-tested:
- Cost per request at 1.630: Docs 124.5, Code 300 first. Rejected by the file: the policy fixes report volume in tier token limits, and the early-access days contradict a per-request cost by a factor of about five.
- Docs token fit or per-new-session cost: Docs about 181, Code first. Rejected by the early-access reconciliation (predicts about 56 per cent or less of observed).
- Early-access tenant's measured 7.05 GPU-s per call applied to every call: Docs 241, Code first. Rejected: tenant is RS-6 only, tiers RM-8 (40k) and RL-12 (64k) prompts are 1.7 to 2.7 times larger, and 7.05 is a tier-specific average.
- lc1 rates: Docs 454, Docs still first (shortfall figure differs). lc1 is the wrong build for a lc2 pool; rollup labels the model per hour.
- **Residual fork (graded figure only):** rescale the fitted rates by the early-access ratio 0.952 and Docs W13 = 327, which rounds to 330 not 340. Pool and rank unchanged (Docs 327 vs Code 299). The daily ratio is very noisy (std 0.64 across 43 days), so a rescale is not a well-defined route and the unscaled fitted rates are the better-supported figure; I judge 340 the forced answer but record this as a soft spot.
- Review-time fork: reading 14:00 as 14:00 UTC would accept R11 and R13 two more nodes of 56. Rollup and provider files are labelled UTC, December Amsterdam is UTC+1, so 13:00 UTC is forced.

Gate A through E: pass. Gate B: every decisive fact is in a shipped file (tier limits in commitments Tiers sheet, policy rules in the policy PDF, review time in Schedule 3, unit and pool facts in the notes and fleet_nodes). Cost basis for report calls is not stated anywhere and is recovered by estimation, which is the stump (method open, data separates the candidates).

## Files/Hygiene
PASS. 19 files, formats pdf, md, log, csv, jsonl, xlsx (six). 25,000-plus-row files present (rollup 48,956 rows; usage 30,903 rows). Distractors: serving_incidents, gpu_spec_register, stopgap_lease_terms (fees, service credits), Q3 table beyond the used columns. Files read as system exports and operational documents with incidental mess (mixed units and harness versions, Amsterdam vs UTC, by-hand job completions, a pool move on 16 Nov, a rollup sessions_new that counts every report call). No authoring or benchmark language in any file; capdesk log and desk notes read as a real pull. No temporal incoherence (pull on 7 Dec after the 4 Dec review). Cross-batch fingerprint check was not run (other task folders are out of bounds for this review).

## Stump power
The stump is the cost basis for report calls: the visible Docs 1.630 GPU-s per request (and Docs' own token fit) is correct for app/API traffic but wrong for reports, where every call is a fresh session on lc2 and the whole prompt is computed. A strong model that prices reports per request or from Docs' own rollup fit files Code at 300 (about 45 points banked on the call is lost); one that reads the policy's token limits, finds the cache-free rate in batch-prod and validates on the early-access days files Docs. Plausible to fail: yes, the easy routes are natural and nothing flags them. Not too easy: the rollup, billing and policy each look sufficient on their own. The ETL asks (out-of-service intervals from three sources, rack acceptance with unit and time-zone traps) are laborious, with exact figures, which keeps the asks demanding.

## Stumping type
`mechanism: method_or_model_selection` (cost model transferred from a cache-free source, validated out of sample), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported numbers (1.630 per request, billing counts, Q3 close-out) are all correct; the difficulty is choosing the right cost basis for a different traffic type and validating it on the early-access days, not catching a wrong number. Clean data would still stump a model that prices reports per request. Passes Gate G; the ETL tables are etl_conformance.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
Domain: capacity planning and fleet utilisation modelling for GPU serving (peak-hour requirement at target busy, per-token cost model by model build, shortfall against allocation); swap test with another field's nouns fails, the quantity deciding the call is one capacity planners estimate. Layer 1: Amsterdam vs UTC, Gbit/s vs GB/s harness versions, by-hand job completions, pool move mid-month, rollup vs billing session semantics, preliminary and superseded fleet plan v3. Layer 2: a service-time cost model transferred from a cache-free source and validated against observed report days. Easy route: price report calls at Docs' 1.630 GPU-s per request (or Docs' token fit), giving Code (300 GPUs) instead of Docs (340).

## Fix
none (solution blocks and files are consistent). Optional, input_files-neutral: in the prompt or policy file the WHAT of the cost basis only (rates measured on calls that reuse no earlier context), not the method, to close the 330/340 soft spot; otherwise accept 340 as the golden and keep the grader tolerant of the nearest-10 edge.
