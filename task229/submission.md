# task229: read-health alert on the comms firmware builds before Wave 8

## Tags

**Domain:** Energy Systems & Utilities (smart-meter interval data delivery, a metering data provider's read performance).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Fire the read-health alert on PX5.2.7, EM3.12.1 and EM3.10.9, and hold PX5.3.0, EM3.11.4, EM3.12.0, PX5.3.1 and EM3.12.2 for Wave 8.**

The deciding margins are EM3.10.9 at 98.06% against its 98.40% limit and EM3.12.0 at 98.39% against 97.81%. Not EM3.12.2 or EM3.12.0: each falls short on nights when a collector missed its collection for most of the installations behind it at once, so their standard errors, built over the collectors those installations share, are 1.90 and 0.56 and both hold, where an error that treats every installation as independent fires both and stops Wave 8 onto EM3.12.2. Not PX5.3.0, whose average installation clears its limit although its 5-minute sites lose reads. PX5.2.7 fires although its week looks complete once the late deliveries land, because only reads the MDM held at the 06:00 cut-off count.

## 2. Critical Components

1. EM3.12.2's standard error is **1.90**, a lower limit of **93.79%** against read health of **97.92%**
2. EM3.12.0's standard error is **0.56**, a lower limit of **97.81%** against read health of **98.39%**
3. EM3.10.9's read health is **98.06%** against a lower limit of **98.40%**
4. EM3.12.1's read health is **98.92%** against a lower limit of **99.30%**
5. PX5.2.7's read health is **98.48%** against a lower limit of **98.99%**

## 3. Step-by-Step Solution

1. In `mdm_interval_receipts_20261005_20261011.csv`, kept for each NMI, suffix and read date the latest delivery received before 06:00 AEST the next day (20:00 UTC on the read date), per MDS-STD-114 3.5; a register-day with no such delivery holds no actual reads.
2. Built each meter's running release from the commissioning and successful activation events in `hes_meter_firmware_history.json`, each event id once, images named through `fw_release_catalogue.csv` (3.6).
3. Kept the installations in `mp_installation_register_20261012.xlsx` whose one meter ran one release from 00:00 AEST 5 October to 24:00 AEST 11 October (3.7).
4. Took each installation's read health as its actual reads held at the cut-off over every interval of every data stream in the register's Data streams sheet for all seven days (3.3, 4.1), and each build's read health as the mean over its assessed installations (4.2).
5. Grouped each build's installations by their meter's `comms_parent` (the collector or access point their reads come in through), because a node that misses a night's collection takes that day from most of the installations behind it at once, and outside those nights no node loses the day for more than a few.
6. Took each build's standard error over its nodes: the sample standard deviation of the nodes' summed deviations from the build's mean, times the square root of the node count, over the installation count (4.3, 7); lower limit is 99.50 less three standard errors (5.1, 5.2).
7. Wave 8: took the meters on both batch sheets of `wave8_schedule.xlsx` once each, serials padded to eight digits, kept those in service and not already on the target, none onto a build that fires (6.1); Wave 7: took each WAVE7 activation once, dated it in market time, and summed the installation's expected reads that day less the actual reads held at the cut-off.
8. Recommendation: the alert fires where read health is below the lower limit, on PX5.2.7, EM3.12.1 and EM3.10.9; the other five builds hold.

## 4. Deliverable Answers

### wave8_read_health_alerts.json

1. Fire: PX5.2.7, EM3.12.1, EM3.10.9. Hold: PX5.3.0, EM3.11.4, EM3.12.0, PX5.3.1, EM3.12.2.
2. One record per build, furthest below its lower limit first (read health, standard error, lower limit, alert):
   - PX5.2.7: 98.48%, standard error 0.17, lower limit 98.99%, fire
   - EM3.12.1: 98.92%, standard error 0.07, lower limit 99.30%, fire
   - EM3.10.9: 98.06%, standard error 0.37, lower limit 98.40%, fire
   - PX5.3.0: 99.49%, standard error 0.05, lower limit 99.36%, hold
   - EM3.11.4: 99.57%, standard error 0.15, lower limit 99.05%, hold
   - EM3.12.0: 98.39%, standard error 0.56, lower limit 97.81%, hold
   - PX5.3.1: 98.95%, standard error 1.11, lower limit 96.17%, hold
   - EM3.12.2: 97.92%, standard error 1.90, lower limit 93.79%, hold
3. Wave 8 under this call: 1,274 installations onto EM3.12.2 and 109 onto PX5.3.1.
4. Wave 7 this week: onto EM3.12.2, 1,109 installations moved and 16,907 interval reads missing at the cut-off on their move day; onto PX5.3.1, 63 installations moved and 1,101 interval reads missing.

### read_health_by_build_wk41.png

1. Titled "Read-health alert fires on PX5.2.7, EM3.12.1 and EM3.10.9; the other five builds hold for Wave 8", one row per build in the payload's order, read health as a point, its lower limit as a tick beside it, and the reference drawn as a line labelled with the standard's reference read health.
