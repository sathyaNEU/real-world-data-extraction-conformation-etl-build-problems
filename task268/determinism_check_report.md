# determinism-check report, task268, 2026-11-07

(Written as pass2: `determinism_check_report.md` already exists on disk, dated 2026-10-31, and carries
content from a prior architecture, architecture 5, Oro Rosso / coffee-counter task. That file is stale
against the current architecture 6 (Rotalinha reliability) submission and is left untouched per the
never-overwrite-a-pass rule. This report is the first determinism-check pass against architecture 6.)

## Verdict
DETERMINISTIC. No SOLUTION_WRONG.
**Disposition:** APPROVE. Every committed figure (main call, both deliverables' asks) reproduces exactly
from the shipped files under the one estimator the data's own structure forces; no repair needed.
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect,
surface_read_dependency: no, sole_data_defect: no

Thread verdict: /tmp/determinism-check-task268-20261107184129/verdict.md (one pass, one thread, fresh
unzip of target.zip sha256 fd413384...f03639f).

## Why
Five services (journey-search, places, seat-map, partner-gateway, notifications) breach their 2026
latency error budget, forced by `trace_spans_2026-12.parquet`'s own structure: exactly 6 of the 10
services ever appear as a trace root (blank `parent_span_id`); the other 4, including partner-gateway,
never control their own sampling, so PR-SLO-3's literal population definition (every request counts
"whether or not the tracing store kept a span for it") forces reweighting each kept span by the inverse
keep rate of whichever edge service started its trace, per hour. The thread reproduced the golden's 2.9%
for partner-gateway under this method, and independently reproduced both of the explicitly-named wrong
constructions the golden's own text rejects (self-weighting on partner-gateway's own hourly count, 1.44%,
rounds to the stated 1.4%; raw unweighted kept-span share, 0.84%/0.69%/0.71%/0.74%, matches the stated
0.8%/0.7%/0.7%/0.7%), confirming the fork is real and only the golden's reading survives. Releases,
rollbacks and cost-by-half reproduced exactly for all 10 services. Incident minutes for partner-gateway
(27, 152) only reproduced once the status page's Lisbon-local (DST-observing) timestamps were converted to
UTC before subtracting against the incident tool's UTC timestamps; the naive same-clock read gives
272 minutes, not 152, confirming this is a forced Layer-1 reconciliation and not a method artifact.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| SLI, all 10 services (edge/root-hour reweighted) | 1.3/0.6/1.5/1.5/0.4/0.3/0.6/0.7/2.9/1.6 | same to 1 decimal | yes |
| Competing construction: self-weight on own hourly count | partner-gateway 1.4 (named, rejected) | 1.44 → 1.4 | yes (and correctly rejected) |
| Competing construction: raw kept-span share | journey-search/places/seat-map/partner-gateway 0.7/0.7/0.7/0.8 (named, rejected) | 0.69/0.71/0.74/0.84 → same roundings | yes (and correctly rejected) |
| Releases/rollbacks, all 10 services | as filed (e.g. partner-gateway 42/9) | same, by replaying production_deployments then cluster_rollout_history | yes |
| Cost by half, all 10 services | as filed (e.g. partner-gateway EUR 32,454 / 37,711) | same, via cloud_resources replacement chain + invoice FX | yes |
| Incident minutes, partner-gateway | 27 / 152 | 27.25 → 27; 93.1 + 58.8 = 151.9 → 152 | yes, only under Lisbon-DST-to-UTC conversion |

## Competing answers that survived
None. The thread names and rejects the two defensible-looking alternative estimators (self-weighting,
raw kept-span share) exactly as the golden's own text does, and both reproduce arithmetically to the
golden's named rejected figures, which closes the fork rather than leaving it open. No file states a
keep rate, a weighting rule, or an SLI directly; the thread found zero hits for "sampl", "keep", "tracing
store" outside PR-SLO-3 itself, so the edge-weighting discovery is unaided, not a hidden rule recovered
from a planted document.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 6 (csv, xlsx, docx, json, md, parquet) | yes |
| Large file | 25,000 rows or more | trace_spans_2026-12.parquet 379,119; lb_target_group_requests H1/H2 43,440 / 44,160 | yes |
| Distractors | 2 or more, in metadata, no file name labels one | capacity_review_2026-Q4.md, app_store_reviews_2026-H2.xlsx, lb_target_group_requests_2026-H1.csv in metadata.json; names do not label them | yes |
| Distractors unused yet weighable; one reproduces a graded quantity and a shipped fact rules it out | required | Design note states the capacity review and app reviews are "context the solution never reads"; confirmed unused by the thread's file-grep. Whether lb_target_group_requests_2026-H1.csv tempts a wrong-window SLI (full year or H1 instead of December) and is closed by PR-SLO-3's December-only scope was not independently stress-tested by me or the thread | partial |
| Deliverables | 1 to 3, all in golden | 2 (reliability_review_2026.docx, service_sli_2026.csv), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | prompt's last sentence states per cent to one decimal, whole minutes, whole euros; asks are 10-service rows across 8+ fields each | yes |
| Prompt shape and rubric 25 or more criteria | identifiable; 25 or more | Shape is a per-service, per-half grid (10 services x SLI/budget/over-or-under/releases/rollbacks/2 incident-minute halves/2 cost halves, plus the main call and the chart). Cardinality alone clears 25; the rubric itself was not opened (generated downstream, outside the judge's and my allow-list) | likely pass, not directly computed |
| Reads as real work product | required | Thread found no LLM-authorship tells, no benchmark/authoring disclosures, no provenance leakage in any file it opened; fictional company Rotalinha, no public-data contamination concern | yes |

## Gate G reconciliation
The thread's classification: mechanism `statistical_rigor` (unequal-probability / cluster-sampling
reweighting on honest data), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`,
`sole_data_defect: no`. It names no distractor as the surface read; the two things it names and rejects
(self-weighted SLI, raw kept-span share) are alternative *estimators*, not a misleading reported number,
so the distractors are not too load-bearing and nothing here resembles surface-read-rejection.

The design note's `## Three rules` section (read only after the thread returned) agrees point for point:
- **Domain test / swap test:** the note's own swap ("wards" for "services", "infection budget" for
  "latency error budget") breaks the sentence, because a ward has no trace store, no balancer count and no
  downstream unit riding another unit's sampling decision. Matches the thread's H1 pass.
- **Analyst test:** the note's stated easy route is "post-stratify each service's kept spans by hour on
  its own balancer count," landing journey-search, places, seat-map and notifications with
  partner-gateway at 1.4 against 2.0. This is exactly the thread's reproduced "self-weighting" competing
  construction (1.44% → 1.4%), reproduced independently and rejected the same way.
- **Not semantics / not rule application:** the note states no filed rule weights kept spans and the
  estimator family spans 0.84 to 2.90 depending on which unit's keep share is used, closed only by
  recognizing the sampling unit is the trace, not the service. This matches the thread's framing that no
  reported number anywhere is false, and the difficulty is building the correct Horvitz-Thompson-style
  estimator, not catching a wrong one.
- **Layer 1 / Layer 2:** the note's Layer 1 (balancer export format changes across halves, re-sent trace
  batches, health probes, nanosecond clocks, Lisbon-vs-UTC clocks on the asks, USD invoice lines, team-tag
  retags, deployment-pipeline staging) lines up with the thread's H2 Layer 1 list (14-April deployment
  migration, mid-year LB rename, USD/EUR billing, Lisbon-DST-vs-UTC). The note's Layer 2
  (`estimation_fit`, a population share from unequal-inclusion-probability sampling where the sampling
  unit is the trace) matches the thread's Layer 2 and its `statistical_rigor` mechanism.

No mismatch. The card carries no literal `stump_class`/`analyst_test`/`domain_test` JSON fields (the
`## Three rules` section in DESIGN_NOTE.md carries the labelled lines instead, with `Not semantics:` and
`Not rule application:` each on its own line as the standing-rule format requires), and its content is the
thread's content in substance.

Gate H line: domain pass, layers pass, decisive_step analytical. This is a genuine Layer-2 analytical
construction (an inverse-probability-weighted estimator over a sample whose sampling unit is the trace,
not the service), not the field's single standard off-the-shelf method applied by rote: recognizing which
unit's keep share applies is the judgment the data has to settle, so this does not fall under the
landable-call carve-out for a textbook method applied with no judgment required.

## Stump power (Gate F)
Credible. The decisive trap (4 of 10 services never originate a trace, so their inclusion probability must
be borrowed from whichever of the 6 edge services started each of their traces, reweighted by that edge's
own hourly keep rate) is undocumented anywhere in the pack; the thread confirmed zero hits for "sampl",
"keep", or "tracing store" outside PR-SLO-3. Both named easy routes are concrete, reproduce to specific
wrong breach lists (self-weighting clears partner-gateway; raw kept-span share clears journey-search,
places, seat-map and partner-gateway all at once), and are plausible failure modes a strong but
insufficiently careful analyst would commit to. The Lisbon-DST incident-minute reconciliation is a
secondary, Layer-1-only difficulty on a supplementary figure, not the main call.

## Findings, ranked
1. (Minor, informational) The input-gate distractor requirement that "one [distractor] that answers a
   graded quantity reproduces arithmetically and a shipped fact rules it out" was not independently
   stress-tested against `lb_target_group_requests_2026-H1.csv` by either the thread or me. The design
   note states the other two distractors (capacity review, app reviews) are never read by the solution at
   all, which satisfies "unused... relevant enough to weigh" but does not itself supply the stronger
   arithmetic-reproduction-and-rule-out case. This does not affect the verdict or disposition; it is a
   spec-gate completeness note only. No fix required unless a future portal review raises it.

## Next action for the author
None. Ship as-is. If the author wants the distractor gate fully closed on paper, name in the design note
which specific graded quantity `lb_target_group_requests_2026-H1.csv` would tempt an analyst to compute
(e.g., an SLI averaged over the full year or over H1 instead of December) and the PR-SLO-3 sentence that
rules it out; this is paperwork, not a rebuild, since the thread already confirmed the file is unused by
the actual solution path.
