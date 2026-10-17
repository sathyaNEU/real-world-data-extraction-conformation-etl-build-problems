# Verdict, task158

**Verdict:** DETERMINISTIC (one flagged convention fork, see Evidence).

**Disposition:** FIX_NOW. Pin in stopgap_assignment_policy section 3 the conversion basis for ordinary (non-report) traffic (the pool's Q3 busy GPU-seconds per completed request, as in the close-out Table 1) without saying anything about how report calls are costed. Policy text only, no data or ladder change; no model rerun needed unless the author judges the edit to change solver behaviour.

**Why:** The 340-GPU Docs shortfall in W13 and the 300-GPU Code figure reproduce from the shipped files. The call is forced because the policy fixes the report volume (signed contracts, contracted peak, tier calls and token limits), and the only cost model the data supports is the cold-prompt token fit (0.248 / 1.85 ms per token, from batch-prod lc2 hours where requests equal sessions_new). That model is validated on the early-access tenant's 295,368 report calls. The Docs pool's own per-request rate (1.630) does not apply to report calls, which put Code first at 300. Margin Docs 339 vs Code 299 is clean. One unpinned convention (the per-request rate for ordinary traffic) can narrow the margin to a tie at the reported rounding; see Evidence.

## Evidence (recomputed)

Main call, from q1_2027_capacity_intake.xlsx, fleet_plan_2027Q1.xlsx, report_service_commitments xlsx, capacity_closeout_2026Q3.pdf and the rollup:
- Q3 rates recomputed from the rollup: chat 0.4419, code 0.5889, agents 0.7335, docs 1.6297, batch 2.6095, voice 0.1203. Reproduced.
- Batch-prod lc2-2026.05 fit, 4,998 hours, R2 0.99986: 0.248 GPU-ms per prompt token and 1.850 per completion token. Reproduced. Docs-only fit gives 0.040 / 2.35 because of session reuse (requests per session 4.95). With the docs-own rates Docs is 181 and Code is first.
- Eleven signed contracts at tier limits and contracted peaks: 249.4 GPUs once all are live (W10 onward). The early-access row and the proposal are excluded. Reproduced.
- Weekly shortfalls in W13: docs 338.8 (rounds to 340), code 299.3 (300), agents 151.1, voice 21.5, chat -77.9, batch -80.1. Reproduced. Docs' W13 is also its peak (plan goes to 656 from W07).
- Early-access check: report-day excess busy GPU-seconds over non-report requests at 1.6297, versus the token model, ratio 0.98 in aggregate (daily values are noisy). The golden's "within 6 per cent" is consistent. Per-request pricing predicts 0.22 of the excess.
- Out-of-service table (fleetctl cordon/uncordon plus console cordon/uncordon plus the 31 hand-completed jobs, console times Europe/Amsterdam to UTC, double cordons counted once, pool at the time via the four nodes that moved agents to chat on 16 Nov, 8 GPUs per node): chat 3761.2 h / 57.40, code 920.7 / 22.90, agents 1100.4 / 55.60, docs 1339.4 / 55.51, batch 459.3 / 22.29, voice 500.7 / 15.21. All match the golden after rounding. Two stays straddle month ends (ams3-g1360, ams2-g0877) but neither is a pool's longest, so "stay" versus "November part" does not change any answer.
- Acceptance: R11 48 (hold 2638), R12 40 (2653, 2654), R13 48 (2662), R14 64 (2645). Reproduced using the last run per fitted serial and per node, with bus bandwidth from 1 Dec divided by 8. Closest nodes: 354.8, 355.2, 358.3 (held) against 366.7 and above (passed), so no knife edge.

Forks examined:
1. Rate for ordinary traffic (open, unpinned). Quarter-average rate (golden): Docs 340, Code 300. Rate of each pool's single Q3 busiest hour (policy says "that hour", the close-out lists the busiest hour): Code 344.5, Docs 341.8, a tie at nearest 10 and Code first as computed. All-time or Q4 or H2 average rates give Docs. The single-hour reading is noisy (top-50-hour rates give code 0.593, docs 1.629) and I do not think it is a strong reading, but the text does not exclude it. Hence the FIX_NOW pin.
2. Pricing at tier limits versus observed token use: the policy says limits, so literal. (Observed ratios of about 0.83 would flip it to Code, but that is against the text.)
3. Per-call, per-session, per-report, per-new-session costs from the early-access tenant: all under-price larger tiers (RM-8, RL-12 limits are 40k and 64k prompt tokens against 24k). Code first, but these are analytical errors, not interpretive forks. The per-session rate (8.07 GPU-s) happens to fit the early-access aggregate within about 7 per cent, so that check alone does not separate it from the token model; the tier limits do.
4. Early-access contract: status is not Signed and ends 18 Dec, so excluded; proposal excluded. Forced by the policy.

Unit risk (acceptance table only): nx7_fabric_results.csv has no unit column or note saying that runs from 1 Dec report Gbit/s. It is inferable (values are about 8 times larger, at 2,671 to 3,035, and consistent with 8 x 400 Gb/s ports), but nothing in the shipped files states it. A solver who misses it gets R12 56 or 64 and no holds from 1 Dec runs. This is layer 1 mess and affects supplementary 3 only, not the call.

## Files/Hygiene: PASS

19 files; formats pdf, csv, xlsx, jsonl, md, log (png is a deliverable, not an input). The rollup has 48,956 rows and the docs usage file 30,903. Row counts match the pull log. Distractors: serving_incidents_2026H2.csv and gpu_spec_register_2026-12.csv (unused). Dates are coherent with the 7 Dec 2026 setting (the early-access end on 18 Dec is a stated future date). No authoring or benchmark language found. Realistic mess is present: duplicate node rows after a pool move, mixed time zones, hand-completed jobs, mixed bandwidth units, replaced GPUs. The close-out states Docs and Batch both run lc2, which points to the right cohort for the fit; mild pre-disarming, not a defect. No exclusion-level finding.

## Stump power

Plausible: a strong model that prices report calls at Docs' 1.630 GPU-s per request (a figure printed in the close-out) or fits tokens on the Docs pool alone lands on Code at 300. Models that read the early-access data and fit the cold-prompt cost on batch-prod land on Docs. I expect a real share to fall for the easy route, but the policy giving tier token limits invites token costing, and the close-out's lc2 sentence points at batch, so the trap may be cleared often. If too easy, the lever is to remove that sentence from the close-out, not to add anything.

## Stumping type

mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no.
The reported 1.630 GPU-s per request is correct for the app and API traffic it measures; the difficulty is choosing the right cost model for a different workload (one-shot cold-prompt calls) and validating it on the early-access tenant, not rejecting a wrong number. Borderline note: a reader could say the close-out rate is "the misleading surface read", but the task would still stump on clean data since the cost model has to be built.

## Three rules

domain: pass, layers: pass, decisive_step: analytical.
Swap test: token-level GPU-time costing of serving traffic, KV/prefix reuse across sessions and a capacity requirement at 70 per cent busy are LLM-serving capacity work and do not survive a noun swap. Layer 1: Amsterdam against UTC, duplicate rows after a pool move, double cordons, hand-completed jobs, Gbit/s against GB/s. Layer 2: estimate the per-token cost of cold report calls from a no-reuse cohort and validate it. Easy route: price report volume at Docs' per-request rate (about 124 GPUs shortfall for Docs), giving Code at 300.

## Fix

solution/prompt-adjacent file edit (input_files: stopgap_assignment_policy_2026-11.pdf section 3): file the rate convention for ordinary traffic only. Optionally put a unit column or header note on nx7_fabric_results.csv so the Gbit/s switch is stated rather than inferred (a Layer 1 clarity pin that does not touch the stump).
