# task212 design note

**Status: PAUSED 2026-11-04 at stage 1 (draw), no card registered.** Wave 8, Anomaly Detection & Diagnostics,
seed AD35. The seed's world was screened as the brief asks and cannot carry an honest unbanned draw under the five
go/no-go screens; the next action is a re-root into another client domain, world and dataset under the same
objective and number (`CLAUDE.md`, A stuck build is unblocked). Nothing below is a draw; it is the screening record
the re-root starts from.

## Draw

- **Seed kept for screening:** a regional claims contractor for a public insurer; one prepayment medical review
  team for FY2027 (1 October 2026 to 30 September 2027); six hospital by DRG-family cells flagged by the contractor's
  two-way model of FY2026 payments; the call is which cell goes under 100 per cent prepayment review and the
  improper payment the review is expected to deny over the twelve months.
- **Pairing screened:** `healthcare-delivery-health-economics` / `payment-claims-health-plan-analytics` (serves ETL
  and AD), the AD cell holding no live card. `provider-quality-risk-adjustment` was read as the neighbouring cell
  (task181, task194 live; task190 architecture 7's enumeration of coding-intensity candidates).
- **Axis window read off `guard.py recent` on 2026-11-04 (last three: task401, task210, task211):** strategies
  `grain_or_unit`, `decomposition_attribution`, `causal_design`; forums `council_or_assembly`, `operations_desk`,
  `committee_or_panel`; forcing events `budget_or_appropriation`, `launch_or_rollout`,
  `purchase_order_or_contract`; org families `local_government`, `government_agency`,
  `hospital_or_health_provider`; shapes `01` and `other`; subdomains multilevel-classroom-school-research,
  safety-incident-error-analysis, safety-signal-detection. Re-read with `check` at the re-root; the window moves.
- **Sibling cards:** every `batch4-task*` branch card (210, 211, 401, 402, 403) was already merged in this tree at
  70d341d; none needed copying.
- **Screening harness (scratch, not shipped):** the clean-truth prototypes live in the session scratch folder
  `t212/proto/` (`world.py` and `analysis.py` with `multi.py` for the repeated-diagnosis candidate, `m1.py` with
  `m1multi.py` for the occupancy candidate); each run is 20 redraws, seeds 1 to 20, four workers.
- **Outcome:** no candidate in this world passed screens 2 and 4 together. The structural reason, measured twice in
  two different mechanisms: the deniable payment in a hospital by DRG-family cell is a latent share of its claims
  (the review decides it from the medical record), so every golden here is an estimate whose matched baseline or
  benchmark noise is of the order of the signal at realistic cell sizes, while the mechanism's own naive count
  rides the same volume as the golden. A records-fixed alternative exists only where a filed rule decides
  improperness (two-midnight benchmark, post-acute transfer policy, payment window, grouper severity tables), which
  is rule application.

## Tried and rejected

- 2026-11-04, the seed's title mechanism (the FY2027 final rule's severity tables remove the largest excess by
  themselves): regrouping FY2026 claims under the published rule is rule application; it can stand only as a lower
  rung (the literal replay), never decide the call.
- 2026-11-04, the severity-validation family (peer benchmark on the MCC-level share, risk adjustment on observable
  case mix, length-of-stay and in-hospital mortality validators, one patient coded by two providers): every plain
  improper practice is visible to one of the validators or to the benchmark, so a strong analyst's own validator
  reaches whatever cell carries plain upcoding; task190 architecture 7 already measured the two-provider and
  look-back members dead (filter-and-difference reaches the designed set 18 to 20 of 20; the attaining subset is
  the fully enrolled patients).
- 2026-11-04, diagnoses repeated onto same-hospital readmissions from the patient's previous stay there (a
  documentation carry-over present at every hospital at its own rate), read against the same kind of patient
  readmitted to a different hospital, where the earlier record cannot carry over. Seven parameter sets, 20 redraws
  each. Truth named the designed cell 20 of 20 every time. The mechanism's naive count (every repeated diagnosis
  that moves the DRG on a same-hospital readmission) named the golden cell 17, 17, 19, 11 and 12 of 20 in the first
  five sets, and the acute-only naive count 15, 18, 15 and 16 of 20; the golden family (family by prior-diagnosis
  matching, pooled, by family, by class) held 15 to 20 of 20. The sixth set added large genuine-recurrence cells
  (dialysis patients' N18.6 on every stay, acute-on-chronic respiratory failure recurring at 0.75): the naive
  counts then landed wrong (20 and 19 of 20) but the golden collapsed to 1 to 8 of 20, because the matched
  other-hospital recurrence cannot subtract a recurrence volume that large. Earlier single-seed versions measured
  the deniable contrast at 20 to 36 claims a cell against binomial noise of 5 to 14 claims. It also sits beside the
  client's own example of a planted copied block, which a judge reading Gate H may take it for.
- 2026-11-04, bed occupancy on the admission day setting the admission threshold (a crowded hospital admits only
  its sickest medical patients on its full weekdays, so its genuine severity excess reads as upcoding, and every
  benchmark, the hospital's annual occupancy as a covariate and both validators land on it). On one seed the ladder
  formed exactly (flagged payment A, FY2026 decomposition B, every benchmark and the annual-occupancy reader C,
  golden D). Over 20 redraws it fails: truth split 10, 8 and 2 across three cells, the golden named the academic
  sepsis cell 9 of 20, because the benchmark excess of a cell of about 5,500 claims carries binomial noise of about
  36 claims, about 0.36 million at that cell's payment step, against a designed signal near 0.2 million; making the
  golden cell's upcoding loud enough to clear that noise makes every benchmark reader name it too.
- 2026-11-04, forward behaviour as the decisive step (the sentinel effect under review, code substitution after a
  severity downgrade, a coding programme's ramp): each is a practice a governing document would have to file, and
  filed it is executed (the withheld-rule trap the brief records from task211's architecture 1).
- 2026-11-04, probe-sample and close-out extrapolation (a targeted probe weighted back to its stratum,
  probability-proportional-to-size draws): spent as drivers (task482's lineage on stratified audit weighting,
  task190 architecture 3 on PPS draws).

## Re-root

The next session draws at stage 1 in another client domain under Anomaly Detection & Diagnostics, with the measured
lesson above as its first filter: the golden must be a records-fixed count over a per-case state rebuilt across two
systems (no estimated baseline subtracted from a quantity of the same size), and the mechanism's own naive count must
ride a different quantity from the golden, not the same volume. Ground already screened in other slots and recorded
dead before this draw, so not to be re-screened: insulator pollution flashover on coastal lines (task121 via task211's
note), lightning damage read through a strike file (task179), common-point-of-purchase and shared-device sources
(task181), exposure placed where members spend the day (task181 v5), a transient after each member's own dated
change (task211's live driver).
