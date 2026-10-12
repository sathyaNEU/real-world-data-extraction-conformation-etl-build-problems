# solver round: round 2, skeptic

**Proxy score 47.5 / 100** (recommendation 3.6 of 35, instruction 7.0 of 7, asks 36.9 of 58). Main call missed. 5 of 9 ask items cracked (80 per cent of tokens).

## Main call

golden: Wire the 2027 peak paging alert to the Exposure rate gap check (expo_rate_gap_pp) at a setting of 3.5, live from 4 January to 28 March 2027.

solver: For the 4 Jan to 28 Mar 2027 peak, wire the paging alert to beacon_loss_z (pageview beacon loss) at |z| >= 3.4, not to events per exposed user. Replayed on 28-night runs, which is the only booking length the peak offers, beacon_loss_z at 3.4 pages 7 of the 166 sound 28-night audited experiments (4.2%, inside the 1-in-20 budget) and would have caught 22 of FY2026's 78 audited defects in time (28.2%). The other checks catch fewer: exposure rate gap at 3.5 pp catches 15/78, assignment ratio p<=0.003 catches 11/78, late events at 1.2 pp catches 7/78, and events per exposed user at 24% catches only 4/78 because its sound-test false pages climb on 28-night runs. The current alert, srm_assign_p at 0.001, catches 9/78.

tokens matched 5 of 7 (3.5, 4, 28, Wire, Exposure, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| peak_alert_config.json | 1 | 0 | 1 | 0% |
| peak_alert_config.json | 2 | 0 | 2 | 0% |
| peak_alert_config.json | 3 | 3 | 3 | 100% |
| peak_alert_config.json | 4 | 6 | 6 | 100% |
| alert_replay_fy2026.xlsx | 1 | 9 | 10 | 90% |
| alert_replay_fy2026.xlsx | 2 | 12 | 12 | 100% |
| alert_replay_fy2026.xlsx | 3 | 5 | 5 | 100% |
| peak_alert_tradeoff.png | 1 | 2 | 4 | 50% |
| peak_alert_tradeoff.png | 2 | 1 | 3 | 33% |

## Solver's path

1. Read DQ-07 rev3. Catch = a page on the first bad night or either of the two nights after it, read on every audited defect. Budget = at most 1 in 20 sound experiments paged on any night of the run, over the season the setting is live, read off the full audit year. Setting = the most sensitive catalogue setting that keeps the budget. Wired check = the one with the most catches, with ties going to the check that pages fewer sound experiments.
2. Read the handbook: peak launches are 4 Jan to 1 Mar 2027, all book 28 nights (no two-week bookings), and the last night is 28 Mar. The peak budget is therefore read on 28-night runs.
3. Joined the two Vigia parquets, 133,900 rows. Dropped 3,280 re-run duplicate rows (the values were identical) and kept 26,780 experiment-night-check rows. The catalogue_rev v3/v4 value scales are consistent.
4. Parsed the four signed sheets of replay_audit_FY2026.xlsx (dd/mm/yyyy): 600 experiments, 522 sound and 78 defects (17/29/20/12, matching each sheet's footer). Joined them to experiment_bookings_fy2026.csv on exp_key. Last nights, booked nights, quarters and Vigia night coverage all match, and every first bad night falls inside its run.
5. Method test: replayed srm_assign_p <= 0.001 over all experiments with DQ-07's open-ticket suppression and confirmed-defect mute, using the actual close times. This reproduces 45 of the 46 tracker alert pages (legacy plus new tracker; the 3 legacy in-progress tickets imported as DQI-1018/1022/1026 were deduplicated). The one it misses, CHK-0513 on 2026-04-08, is a real firing night but was raised while the migrated 03-31 ticket was still open, so the suppression model does not reproduce it. A firings-only check covers all 46: every page falls on a firing night, and every experiment that fired was paged on its first firing night. Of the audited defects, 9 were paged in time, matching the tracker.
6. Replayed all 5 checks at every catalogue setting on the audit. Sound share used the 166 sound 28-night experiments from the full year. Catch counts used all 78 defects. Pre-window firings never removed a catch at the chosen settings, so ticket suppression does not affect the result.
7. Peak settings: srm 0.003 (0.01 gives 7.2%); expo 3.5 (3.0 gives 5.4%); evpu 24 (23 gives 6.0%); beacon 3.4 (3.3 gives 5.4%); late 1.2 (1.1 gives 5.4%). Most catches: beacon_loss_z with 22/78.
8. Built the alert record from the tracker alert tickets (vigia-bot / source=vigia) for check nights 1 Oct 2025 to 30 Sep 2026, bucketed by fire night into FY quarters: 43 pages, 30 confirmed, 13 not a defect.
9. peak27_booking_queue.csv: 43 accepted bookings, all 28-night Mon-Thu launches between 4 Jan and 1 Mar. BK27-103 and BK27-129 are the same LST test on the same night, so they count as one, giving 42. Owner = surface_owners on the launch night (CHK goes to SQ-04 from 2026-12-01; REV goes to SQ-02 from 2027-02-01). Channel = squads.csv valid at launch (SQ-05 is hosts #oncall-hosts from 2026-11-16).

confidence: medium-high. The call depends on reading the peak budget off 28-night sound runs. If the budget is read on all 522 sound experiments instead, evpu_dev_pct at 14 would win (28/78 caught, 26/522 paged).

notes: Two points stay open. First, BK27-103 and BK27-129 are both accepted bookings of the same LST test on 2027-01-04. If both count, listing has 7 tests and the total is 43. Second, the folder does not give a platform on-call channel for the config; #exp-platform is a questions channel.

### peak_alert_config.json (solver's answers)
- check: beacon_loss_z (Pageview beacon loss)
- setting: 3.4 (z; pages when abs(value) >= 3.4)
- live window: 2027-01-04 to 2027-03-28 inclusive (peak first night to last night; fixed at the 14 Dec 2026 freeze)
- on-call channel per squad with peak tests: SQ-01 search #oncall-search; SQ-02 listing #oncall-listing; SQ-04 payments #oncall-payments; SQ-05 hosts #oncall-hosts; SQ-06 guest-comms #oncall-guest-comms; SQ-07 apps #oncall-apps. SQ-03 checkout has no peak tests, because CHK moves to SQ-04 on 2026-12-01.

### alert_replay_fy2026.xlsx (solver's answers)
- sheet 1: each check at its peak setting, defects caught in time / total: srm_assign_p: 0.003, 11 of 78 caught, 3/166 sound 28-night tests paged (1.8%). expo_rate_gap_pp: 3.5 pp, 15 of 78 caught, 4/166 paged (2.4%). evpu_dev_pct: 24%, 4 of 78 caught, 8/166 paged (4.8%). beacon_loss_z: 3.4, 22 of 78 caught, 7/166 paged (4.2%). late_share_gap_pp: 1.2 pp, 7 of 78 caught, 8/166 paged (4.8%).
- current alert FY2026 record by quarter (pages, confirmed defects, false alarms): Q1 Oct-Dec 2025: 7 pages, 4 confirmed, 3 false. Q2 Jan-Mar 2026: 14 pages, 11 confirmed, 3 false. Q3 Apr-Jun 2026: 10 pages, 6 confirmed, 4 false. Q4 Jul-Sep 2026: 12 pages, 9 confirmed, 3 false. FY total: 43 pages, 30 confirmed, 13 false.
- peak tests per squad on-call: apps (SQ-07) 15; search (SQ-01) 7; payments (SQ-04) 7, which includes 4 CHK tests; listing (SQ-02) 6, which includes REV test BK27-208 and counts duplicate bookings BK27-103/BK27-129 once; guest-comms (SQ-06) 5; hosts (SQ-05) 2. Total 42 tests.

### peak_alert_tradeoff.png (solver's answers)
- title: beacon_loss_z (Pageview beacon loss) at 3.4
- bar per check: % of defects caught in time at peak setting (1 dp): beacon_loss_z 28.2%; expo_rate_gap_pp 19.2%; srm_assign_p 14.1%; late_share_gap_pp 9.0%; evpu_dev_pct 5.1%
