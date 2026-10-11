# task229: read-health alert on the comms firmware builds before Wave 8

## Tags

**Domain:** Energy Systems & Utilities (smart-meter interval data delivery, a metering data provider's read performance).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Fire the read-health alert on EM3.10.9, EM3.12.1 and PX5.2.7, and hold EM3.12.0, PX5.3.0, EM3.11.4, EM3.12.2 and PX5.3.1 for Wave 8.**

The deciding margins are PX5.2.7 at 98.45% against its 98.99% limit and EM3.12.1 at 99.13% against 99.39%. PX5.2.7 fires although its week looks complete once the morning catch-up deliveries land, because only what the MDM held at the 06:00 cut-off counts. Not PX5.3.0: its 5-minute commercial installations carry most of its reads but count once each, and its average installation is 99.51% against 99.36%. Not EM3.12.0 or the PX5.3.1 pilot, which breach only on an error taken from the read count rather than from installation-to-installation spread. Not EM3.12.2, whose shortfall is Wave 7's upgrade nights on installations that did not run it all week.

## 2. Critical Components

1. PX5.2.7's read health is **98.45%** against a lower limit of **98.99%**
2. EM3.12.1's read health is **99.13%** against a lower limit of **99.39%**
3. PX5.3.0's read health is **99.51%** against a lower limit of **99.36%**
4. EM3.12.0's read health is **99.44%** against a lower limit of **99.38%**
5. EM3.10.9's read health is **98.55%** against a lower limit of **98.98%**

## 3. Step-by-Step Solution

1. In `mdm_interval_receipts_20261005_20261011.csv`, kept for each NMI, suffix and read date the latest delivery received before 06:00 AEST the next day (20:00 UTC on the read date), per MDS-STD-114 3.5; a register-day with no such delivery holds no actual reads.
2. Built each meter's running release from the commissioning and successful activation events in `hes_meter_firmware_history.json`, each event id once, images named through `fw_release_catalogue.csv` (3.6).
3. Kept the installations in `mp_installation_register_20261012.xlsx` whose one meter ran one release from 00:00 AEST 5 October to 24:00 AEST 11 October (3.7).
4. Took each installation's read health as its actual reads held at the cut-off over its expected interval reads, every data stream in the register's Data streams sheet for all seven days (3.3, 4.1).
5. Took each build's read health as the mean over its assessed installations and its lower limit as the 5.1 reference less three times their sample standard deviation over the square root of their number (4.2, 5.2, 7).
6. Wave 8: took the meters on both batch sheets of `wave8_schedule.xlsx` once each, serials padded to eight digits, and kept those still in service at their installation and not already on the target release (block 4).
7. Wave 7: took each WAVE7 activation once, dated it in market time, and summed the installation's expected reads that day less the actual reads held at the cut-off for it (block 4).
8. Recommendation: the alert fires where read health is below the lower limit, on EM3.10.9, EM3.12.1 and PX5.2.7; the other five builds hold.

## 4. Deliverable Answers

### wave8_read_health_alerts.json

1. Fire: PX5.2.7, EM3.10.9, EM3.12.1. Hold: EM3.12.0, PX5.3.0, EM3.11.4, EM3.12.2, PX5.3.1.
2. One record per build, furthest below its lower limit first (installations assessed, read health, lower limit, alert):
   - PX5.2.7: 728 installations, 98.45%, 98.99%, fire
   - EM3.10.9: 423 installations, 98.55%, 98.98%, fire
   - EM3.12.1: 695 installations, 99.13%, 99.39%, fire
   - EM3.12.0: 2,242 installations, 99.44%, 99.38%, hold
   - PX5.3.0: 789 installations, 99.51%, 99.36%, hold
   - EM3.11.4: 1,662 installations, 99.78%, 99.42%, hold
   - EM3.12.2: 153 installations, 99.85%, 99.39%, hold
   - PX5.3.1: 37 installations, 98.96%, 96.83%, hold
3. Wave 8 schedule, if it goes ahead: 1,274 installations onto EM3.12.2 and 109 onto PX5.3.1.
4. Wave 7 this week: onto EM3.12.2, 1,109 installations moved and 17,455 interval reads missing at the cut-off on their move day; onto PX5.3.1, 63 installations moved and 933 interval reads missing.

### read_health_by_build_wk41.png

1. Titled "Read-health alert fires on EM3.10.9, EM3.12.1 and PX5.2.7; the other five builds hold for Wave 8", one row per build in the payload's order labelled with its assessed installations, read health as a point, its lower limit as a tick beside it, and the reference drawn as a line labelled with its value.
