# task229: read-health alert on the comms firmware builds before Wave 8

## Tags

**Domain:** Energy Systems & Utilities (smart-meter interval data delivery, a metering data provider's read performance).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Fire the read-health alert on EM3.12.1, EM3.10.9 and PX5.2.7, and hold PX5.3.0, EM3.12.0, EM3.11.4, PX5.3.1 and EM3.12.2 for Wave 8.**

The deciding margins are PX5.2.7 at 98.73% against its 98.96% limit and EM3.12.0 at 98.21% against 97.80%. Not EM3.12.2 or EM3.12.0: their installations sit behind collectors that missed a night's collection for most of the meters behind them at once, so their standard errors, built over the collectors those installations share, are 1.83 and 0.57 and both hold, where an error that treats every installation as independent fires both and stops Wave 8 onto EM3.12.2. Not PX5.3.0, whose average installation clears its limit although its 5-minute sites lose reads. PX5.2.7 fires although its week looks complete once the late deliveries land, because only reads the MDM held at the 06:00 cut-off count.

## 2. Critical Components

1. EM3.12.2's standard error is **1.83**, a lower limit of **94.01%** against read health of **97.87%**
2. EM3.12.0's standard error is **0.57**, a lower limit of **97.80%** against read health of **98.21%**
3. PX5.2.7's read health is **98.73%** against a lower limit of **98.96%**
4. EM3.10.9's read health is **98.06%** against a lower limit of **98.40%**
5. EM3.12.1's read health is **98.92%** against a lower limit of **99.30%**

## 3. Step-by-Step Solution

1. In `mdm_interval_receipts_20261005_20261011.csv`, kept for each NMI, suffix and read date the latest delivery received before 06:00 AEST the next day (20:00 UTC on the read date), per MDS-STD-114 3.5; a register-day with no such delivery holds no actual reads.
2. Built each meter's running release from the commissioning and successful activation events in `hes_meter_firmware_history.json`, each event id once, images named through `fw_release_catalogue.csv` (3.6).
3. Kept the installations in `mp_installation_register_20261012.xlsx` whose one meter ran one release from 00:00 AEST 5 October to 24:00 AEST 11 October (3.7).
4. Took each installation's read health as its actual reads held at the cut-off over every interval of every data stream in the register's Data streams sheet for all seven days (3.3, 4.1), and each build's read health as the mean over its assessed installations (4.2).
5. Grouped each build's installations by their meter's `comms_parent` (the collector or access point their reads come in through), because a node that misses a night's collection takes that day from most of the installations behind it at once, and outside those nights no node loses the day for more than a few.
6. Took each build's standard error over its nodes: the sample standard deviation of the nodes' summed deviations from the build's mean, times the square root of the node count, over the installation count (4.3, 7); lower limit is the reference less three standard errors (5.1, 5.2), and the distance is read health less the limit.
7. Wave 8: took the meters on both batch sheets of `wave8_schedule.xlsx` once each, serials padded to eight digits, kept those in service and not already on the target, none onto a build that fires (6.1); the substitution load is every installation whose in-service meter runs a build that fires (6.1, 3.6).
8. Recommendation: the alert fires where read health is below the lower limit, on EM3.12.1, EM3.10.9 and PX5.2.7; the other five builds hold.

## 4. Deliverable Answers

### wave8_read_health_alerts.json

1. Fire: EM3.12.1, EM3.10.9, PX5.2.7. Hold: PX5.3.0, EM3.12.0, EM3.11.4, PX5.3.1, EM3.12.2. One record per build, furthest below its lower limit first (read health, standard error, lower limit, distance from the limit, alert):
   - EM3.12.1: 98.92%, standard error 0.07, lower limit 99.30%, 0.38 below the limit, fire
   - EM3.10.9: 98.06%, standard error 0.37, lower limit 98.40%, 0.34 below the limit, fire
   - PX5.2.7: 98.73%, standard error 0.18, lower limit 98.96%, 0.23 below the limit, fire
   - PX5.3.0: 99.49%, standard error 0.05, lower limit 99.36%, 0.13 above the limit, hold
   - EM3.12.0: 98.21%, standard error 0.57, lower limit 97.80%, 0.41 above the limit, hold
   - EM3.11.4: 99.57%, standard error 0.15, lower limit 99.05%, 0.52 above the limit, hold
   - PX5.3.1: 98.98%, standard error 1.05, lower limit 96.35%, 2.63 above the limit, hold
   - EM3.12.2: 97.87%, standard error 1.83, lower limit 94.01%, 3.86 above the limit, hold
2. Wave 8 under this call: 1,274 installations onto EM3.12.2 and 109 onto PX5.3.1.
3. Substitution load: 1,846 installations run a build the alert fires on.

### read_health_by_build_wk41.png

1. Titled "Read-health alert fires on EM3.12.1, EM3.10.9 and PX5.2.7; the other five builds hold for Wave 8", one row per build in the payload's order, read health as a point, its lower limit as a tick beside it, and the reference drawn as a line labelled with the standard's reference read health.
