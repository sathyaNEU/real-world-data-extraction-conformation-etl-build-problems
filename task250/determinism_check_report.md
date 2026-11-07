# determinism-check report, task250, 2026-11-07 (Domains Fit rework)

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE, no repair and no rerun
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no (borderline)
**Three rules:** domain: pass, layers: pass, decisive_step: analytical

Thread verdict: /tmp/determinism-check-task250-dfit/verdict.md (Sonnet, medium, isolated to the bundle), read on target.zip
d5630ad1. The pack shipped is bd959e1c: after the judge read it, the interval's basis (the 90 per cent level, each parcel
the hub handled an independent chance of a missed sort scan, read wholly above, across or wholly below the tolerance)
moved from the prompt's second sentence into october_scorecard_request.eml as the requester's convention for the
scorecard, and the workbook sentence was rewritten as a request; the ask and its meaning are unchanged, and freeze.py
passes with every graded figure where the judge reproduced it.

## Why
The thread rebuilt every graded figure from the bundle and each matches the golden: the six hubs' parcels, missed sort
scans and rates (Komorniki 0.48, Bielany Wroclawskie 0.79, Sosnowiec 1.34, Modlniczka 0.63, Strykow 1.55, Pruszkow
1.23), the 300 unloadings at every door gap from 1 to 29 minutes, each holding one hub's sorted parcels, the 24
two-trailer mornings (1,440 parcels off Strykow's trailers, 130 unsorted, against 205 from Pruszkow's own), the side of
the tolerance each hub's 90 per cent interval falls on under the Wilson, normal, Clopper-Pearson, Jeffreys and
Agresti-Coull intervals (three wholly above, three wholly below), and all 13 depots' events sent twice and parcels never
picked up. The alert set (Sosnowiec, Strykow, Pruszkow) follows once each parcel without a sort event is charged to the
hub whose trailer it came off.

## Gate G and Gate H
- Gate G: `mechanism: decomposition_attribution`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`,
  `sole_data_defect: no` (borderline: without the Strykow trailers the attribution step vanishes, but the rate with its
  interval stays a real estimation task). No shipped artifact reports a wrong hub figure; the sort plan is a planned
  assignment, not a reported result.
- Gate H: `domain: pass` (per-hub scan completeness against a tolerance with a binomial interval is a tracking-data
  quality team's own monitoring work), `layers: pass` (Layer 1: DST and UTC, the two handheld clocks, a replaced depot
  code, re-sent rows, piece labels, the marketplace key; Layer 2: attributing the never-sorted parcels to their hub and
  judging each rate by its interval), `decisive_step: analytical` (the easy route charges missing scans to the plan's
  hub and files Pruszkow 1.76, Strykow 0.49). The thread notes a borderline planted risk on the Strykow overflow and
  judges it a real attribution problem the data reveal, not a hidden rule.

## Residual fork, ruled settled
TDS-4 s.2.1 makes a hub's parcels the parcels it sorted and does not say how the hub of a parcel with no sort event is
known; a literal reader holding only the sort plan could charge the plan's hub. The thread rules it settled by the
unloading structure: every unloading carries one hub's sorted parcels, Strykow's parcels for the Warsaw depots arrive in
their own door runs, and the unloading is the only physical link shipped, so the golden is the one reading consistent
with every file; the sort events themselves contradict the plan for 1,310 parcels. This is the stump (design note SF11).
The smaller depot-line conventions (the minute-cut duplicate, the TC51 clock, piece labels, the 20-character
marketplace key) are the only patterns the data support and touch the asks only.

## Stump power
Good: the sort plan is a tempting, correct-looking depot-to-hub map, and charging by it fires Sosnowiec and Pruszkow
and drops Strykow; only the unloading structure fires all three.

## Hygiene
PASS: 11 files in five formats (the depot scans 91k rows, the courier parquet 280k), the distractors present and unused.

## Earlier passes
2026-10-31 (architecture 3, target.zip 1b8dcbc7): DETERMINISTIC, APPROVE, with an optional prompt pin on the courier
events' window, taken as SF23; the same alert set, Gate G decomposition_attribution analytical_non_defect, Gate H pass.
