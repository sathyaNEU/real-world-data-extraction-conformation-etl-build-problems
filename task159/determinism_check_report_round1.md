# Judge verdict, task159 (Vellmouth platform conductors, spring 2027)

**Verdict:** DETERMINISTIC (main call 26 shifts, Mon 4 / Tue 6 / Wed 6 / Thu 6 / Fri 4 reproduces; two small forks on the supplemental figures, below).

**Disposition:** FIX_NOW. Pin two supplemental conventions in the prompt wording only: escalator outages (FAULT time) do not reduce the rated flow, and "weekdays" of the autumn pick exclude the 26-27 November holiday-timetable days. The main call, the stump and the data are untouched, so no stump-power rerun is needed.

## Why
The shipped counts show that platform crowds do not scale with entries. Corran Junction 5W peaks ~1,000 on Tue-Thu but only 245-262 on the counted Monday and Friday, with entries down 16 and 25 per cent. The stump is a capacity-constrained loading model (cars x 150 max load, riders from upstream, alighters, queue carried to the next train), which separates the platforms that saturate (Sallow Park 1S and 4S, Corran 5W) from those that scale. Under it Sallow Park saturates Tue-Thu only, and Corran 5W clears with the spring eight-car trains. Every other posted platform (GAR-2, COR-2, ALB-6, QUA-6) clears the 85 per cent line on all five weekdays by a visible margin. The easy route (carry the counts to Mon/Fri and to eight cars by entries) files 35 shifts, not 26.

## Evidence (recomputed from the bundle)
| Item | Result | Source |
|---|---|---|
| Thresholds 0.85 x rating on 1 Mar 2027 | reproduce (SAL-1S 391, SAL-4S 425, COR-5W 400, GAR-2 323, COR-2 306, ALB-6 204, QUA-6 170); the only dated rating change (FER-4S 300 to 330 on 13 Feb) is not near the line | platform_capacity_register.csv |
| Counted peaks (max quarter-hour mean, 07:00-09:30) | SAL-1S 985/1008, SAL-4S 1253/1377, COR-5W 1030/932 (Tue-Thu), 262/245 (Mon/Fri); GAR-2 475/488 Tue-Thu, 398 Mon, 360 Fri; ALB-6 372 / 338 Tue-Wed, 270 Mon, 268 Fri; QUA-6 285-289, 287 Mon, 203 Fri; HES-3 ~300, ALB-3S ~300, all others far below | platform_counts_autumn_2026.xlsx |
| Own loading simulation (census flows scaled to the fare-entries index, timetable trips, 150 per car) | Autumn Tue-Thu peaks of the right order for SAL-1S/4S/COR-5W (the crude model reads low; per-car 143-145 fits the counts best). Spring: Monday SAL-1S 267, SAL-4S 291-354 (thresholds 391/425); Friday 244/266; COR-5W Monday 278 / Friday 248 (counted 262-272 / 245-257, so the model reproduces the hybrid-day counts); COR-5W Tue-Thu with 8 cars 329-338 (threshold 400); Sallow Tue-Thu 640-1,170, over the line | timetable, census, fleet register, fare parquet |
| Island and scaled platforms | forecast = count x spring index / count-day entries: GAR-2 Fri ~357-361 (>323), COR-2 Mon ~390 / Fri ~340-350 (>306), ALB-6 Fri 267 (>204), QUA-6 Fri ~205-214 (>170); HES-3 max ~300 (<357); every other platform at least 15 per cent under | counts, fare parquet |
| Posting set | GAR-2, COR-2, ALB-6, QUA-6 x 5 = 20; SAL-1S, SAL-4S x 3 = 6; total 26; Mon 4 / Tue-Thu 6 / Fri 4 | reproduces |
| Planning load 110 per car instead of 150 | gives backlogs of 2,400-3,300 at Sallow and Corran, nowhere near the counts, so the counts separate the two loads (fork closed by data) | fleet_register.csv, counts |
| Escalators (platform escalators, controller-log direction, controller speed 0.45 or 0.5 from the asset register, 72 weekdays 8 Sep-18 Dec less 26-27 Nov) | all 14 golden figures reproduce at the nominal configuration: GAR 72/144, SAL 216/72, HES 108/144, COR 232/96, FER 36/248, ALB 268/36, QUA 132/96. Direction is constant per unit over the window on every day (reversal at ~06:27), so the static inventory direction and the 0.5 inventory speed are the wrong readings | inventory, asset register, controller log, manual 5.3 |
| Elevator-hours (union of monitoring non-NORMAL intervals and work-order intervals, 07:00-09:45 local, same 72 days) | all 7 reproduce: 27.9, 53.3, 38.6, 18.0, 45.5, 37.3, 41.3. Monitoring only gives 21.0/49.1/35.6/16.7/38.5/33.6/36.9; work orders only 27.2/51.4/37.0/16.9/44.1/35.5/39.4 | monitoring, work orders, manual 5.4 |

## Open forks (low severity, supplemental asks only)
1. **Escalator outages.** Time-weighting the 0.3 per cent FAULT minutes gives Sallow down 215, Quarry down 131, Ferrier up 247, Hesper up 143 against golden 216, 132, 248, 144. The prompt says "at their rated flows", which supports the golden, but a careful analyst can reasonably deduct faults. Four of 14 figures move by 1.
2. **Weekdays of the autumn pick.** Including 26-27 November (holiday timetable) moves Garnett Street elevator-hours from 27.9 to 31.8 (the other six unchanged). The standard's own definition ("weekday on which the weekday timetable runs") and the service plan support exclusion, but the supplemental sentence does not cite it.
3. Main call margins: GAR-2 Friday leads its line by ~11 per cent, COR-2 Fri by ~11-14 per cent; SAL-4S Monday is under its line by 17-30 per cent but flips if the per-car load is pushed to ~135. The counts on COR-5W and the 150 max load keep it on the golden side. No fork found.

## Files/Hygiene
PASS. 20 files; formats csv, xlsx, pdf, parquet (4). Largest: fare parquet 761,596 rows and legacy register 216,012 rows. The legacy register, the rounded and preliminary dashboard, the withdrawn rev 3 and the 2019 FER-4S rating are the distractors (unused by the solution). Layer 1 mess present: UTC against local, inches against mm, Kennet Street merge, estimated counts marked E, preliminary month. No authoring or benchmark language in any file, PDF and xlsx metadata name in-fiction authors, dates are coherent with the fiction (counts delivered 4 Dec 2026, spring plan 14 Dec 2026, data to 10 Jan 2027). No public-data contamination found. Nothing exclusion-level. Minor: the fare file name ends 2027-01-10 while the last hour is 2027-01-11 05:00 UTC (local midnight), harmless.

## Stump power
Good. The tempting routes all file wrong totals: scaling counts by entries to Mon/Fri and to eight cars gives about 35 shifts (Sallow posted Mon-Fri, Corran 5W all week); ignoring the eight-car change gives 29; a one-headway static count (no backlog) gives about 20. A strong model must build and validate the loading model against the counts. The supplemental asks add several cheap-to-miss devices (controller speed and reversal against the static inventory, union of two outage sources, DST, inch widths).

## Stumping type
`mechanism: forecasting` (capacity-constrained flow model, validated out of sample against the Mon/Fri counts), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The counts are correct; the difficulty is that they do not extrapolate proportionally once trains saturate. On clean data the task still stumps. Passes Gate G.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Domain: platform accumulation against rated capacity under a train-loading model is transit station planning work (swap test fails: "megawatt-hours" or "visits" would not give the same task). Layer 1: UTC and DST, inch and mm, merged complex id, estimated counts, preliminary month. Layer 2: loading-model forecast with queue carry-over, validated against the hybrid-day counts. Easy route a careful analyst takes (counts scaled by entries, spring plan read as same-fleet): 35 shifts against the golden 26.

## Fix
prompt (small). Add "escalator outages ignored" and "weekdays with the weekday timetable" (or name 26-27 November as excluded) in the supplemental sentence, or rely on the rubric to accept 215/216, 131/132, 247/248, 143/144 and 27.9/31.8. Cross-batch fingerprint not checked: no other task folder is readable under the isolation rules.
