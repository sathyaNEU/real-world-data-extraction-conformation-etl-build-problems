# solver round: round 2, plain

**Proxy score 48.9 / 100** (recommendation 5.0 of 35, instruction 7.0 of 7, asks 36.9 of 58). Main call missed. 4 of 9 ask items cracked (80 per cent of tokens).

## Main call

golden: Wire the 2027 peak paging alert to the Exposure rate gap check (expo_rate_gap_pp) at a setting of 3.5, live from 4 January to 28 March 2027.

solver: For the 4 January to 28 March 2027 peak, wire the paging alert to beacon_loss_z (Pageview beacon loss) at |z| >= 3.4 instead of the current srm_assign_p at 0.001. When the page budget is read on 28-night sound runs (166 audited sound experiments, at most 8 may be paged), this setting pages 7 of 166 (4.2%). It catches 22 of the 78 FY2026 audited defects in time (28.2%), more than exposure rate gap at 3.5 pp (15/78, 19.2%), assignment ratio at p<=0.003 (11/78, 14.1%), late events at 1.2 pp (7/78, 9.0%) and the desk's preferred events per exposed user, which has to be set at 24% to stay in budget and then catches only 4/78 (5.1%).

tokens matched 7 of 7 (3.5, 4, 28, Wire, Exposure, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| peak_alert_config.json | 1 | 0 | 1 | 0% |
| peak_alert_config.json | 2 | 0 | 2 | 0% |
| peak_alert_config.json | 3 | 2 | 3 | 67% |
| peak_alert_config.json | 4 | 6 | 6 | 100% |
| alert_replay_fy2026.xlsx | 1 | 9 | 10 | 90% |
| alert_replay_fy2026.xlsx | 2 | 12 | 12 | 100% |
| alert_replay_fy2026.xlsx | 3 | 5 | 5 | 100% |
| peak_alert_tradeoff.png | 1 | 2 | 4 | 50% |
| peak_alert_tradeoff.png | 2 | 2 | 3 | 67% |

## Solver's path

1. Read prompt.md, DQ-07 rev3 docx (catch = page on first bad night or the 2 nights after, read on every audited defect; budget = at most 1 sound experiment in 20 paged on any night of its run over the live season, read off a full audit year; most sensitive accepted setting per check; pick the check with most catches, ties to fewer sound pages), handbook s6 (peak launches book 28 nights; runs not cut short), vigia_check_catalogue.json (5 checks, accepted settings, firing directions), and the field notes and export notes.
2. Loaded both Vigia parquets (133,900 rows). Removed 3,280 duplicate re-run rows: each is the same experiment, night and check under a later job_run with an identical value. Checked that units are consistent across catalogue_rev v3 and v4.
3. Parsed replay_audit_FY2026.xlsx, 4 quarter sheets of 150 rows each: 600 experiments, 522 sound and 78 defects (17, 29, 20 and 12 by quarter, matching the sheet footers). Joined to experiment_bookings_fy2026.csv on exp_key with 600/600 matches. Last night and booked nights all agree, every first bad night falls inside its run, and Vigia covers every booked night.
4. Replayed every check at every catalogue setting. Paged sound means any run night fires; caught means a fire on a night from the first bad night to first bad night +2. No caught defect had an earlier page that could have held a ticket open.
5. Peak runs are 28 nights, so I read the page budget on the 166 sound audited experiments that ran 28 nights, across all four quarters (budget at most 8). Catches are counted on all 78 defects. Result: srm 0.003 (3 paged, 11 caught), expo 3.5 (4, 15), evpu 24.0 (8, 4), beacon 3.4 (7, 22), late 1.2 (8, 7). Beacon at 3.4 wins. Contrast: reading the budget on all 522 sound runs, which are mostly 14-night, lets evpu sit at 14.0 with 28 catches (26/522 paged). That understates the false pages evpu raises over 28 nights: at 14.0 it pages 14/166.
6. Current alert record: took vigia-bot tickets from the legacy tracker CSV (pre-migration) and source=vigia tickets from the JSON. Removed 3 migration imports (DQ-3245/3246/3252 = DQI-1018/1022/1026) and kept the closed outcomes from the new tracker. Excluded manual and duplicate tickets. Put each page in a quarter by the night it fired on (legacy night parsed from the summary), not the ticket date, and kept nights from 2025-10-01 to 2026-09-30, which drops 3 September 2025 pages. Result: 43 pages, 30 confirmed and 13 false; every page's srm value checks out at <=0.001 in Vigia.
7. Peak coverage: peak27_booking_queue.csv, accepted only (43 of 47; 4 cancelled). All launches fall from 2027-01-04 to 2027-03-01, all Mon-Thu, all 28 nights. The owning squad comes from surface_owners.csv as of each launch night: 4 CHK tests go to SQ-04 rather than booker SQ-03, and REV-0208 (launching 2027-02-15) goes to SQ-02. Channels come from squads.csv in force over the peak (SQ-05 is hosts, #oncall-hosts, from 2026-11-16). Counts: 7/7/7/2/5/15.

confidence: Medium-high. The figures are exact under the stated reading. The main judgment call is reading the peak page budget on 28-night sound runs. Under an all-runs reading the answer would flip to evpu_dev_pct at 14.0 (28/78), but that reading understates false pages over the 28-night peak bookings.

notes: BK27-129 and BK27-103 are both accepted LST 'calendar opens on first free week' bookings launching 2027-01-04; I counted both, so listing has 7 tests and the total is 43 (42 and 6 if one is a double booking). DQI-1093 (APP-0685) was closed as a confirmed defect on 2026-06-14 for a page fired on 2026-06-12, but its first bad night is 2026-06-18 in both the ticket and the audit; I kept it as confirmed as the tracker recorded it, and it would move one Q3 page to the false alarms if reclassified.

### peak_alert_config.json (solver's answers)
- check: beacon_loss_z (Pageview beacon loss); pages when abs(value) >= setting
- setting: 3.4 (z, a catalogue setting)
- live window: 2027-01-04 to 2027-03-28, both nights inclusive (Lisbon nights); setting fixed at the 14 Dec 2026 change freeze
- on-call channel per squad with peak tests: SQ-01 search #oncall-search; SQ-02 listing #oncall-listing; SQ-04 payments #oncall-payments; SQ-05 hosts #oncall-hosts; SQ-06 guest-comms #oncall-guest-comms; SQ-07 apps #oncall-apps (6 squads; SQ-03 checkout has no peak tests because CHK passes to SQ-04 from 2026-12-01). Platform on-call also receives every page.

### alert_replay_fy2026.xlsx (solver's answers)
- Sheet 1: each check at its most sensitive in-budget peak setting, defects caught in time / total: srm_assign_p p<=0.003: 11/78 caught (14.1%), 3/166 sound 28-night runs paged; expo_rate_gap_pp 3.5 pp: 15/78 (19.2%), 4/166 paged; evpu_dev_pct 24.0%: 4/78 (5.1%), 8/166 paged; beacon_loss_z 3.4: 22/78 (28.2%), 7/166 paged; late_share_gap_pp 1.2 pp: 7/78 (9.0%), 8/166 paged. Budget is at most 1 in 20 sound runs, so at most 8 of 166.
- Current alert (srm_assign_p 0.001) FY2026 record by quarter, counted on the night each page fired: Q1 (Oct-Dec 2025): 7 pages, 4 confirmed defects, 3 false alarms; Q2 (Jan-Mar 2026): 14 pages, 11 confirmed, 3 false; Q3 (Apr-Jun 2026): 10 pages, 6 confirmed, 4 false; Q4 (Jul-Sep 2026): 12 pages, 9 confirmed, 3 false; FY2026 total: 43 pages, 30 confirmed defects, 13 false alarms
- Peak tests each squad's on-call will cover (accepted bookings, owner on launch night): search SQ-01: 7; listing SQ-02: 7; payments SQ-04: 7; hosts SQ-05: 2; guest-comms SQ-06: 5; apps SQ-07: 15; total 43 tests

### peak_alert_tradeoff.png (solver's answers)
- title: Peak 2027 alert: Pageview beacon loss (beacon_loss_z) at |z| >= 3.4
- bars: share of FY2026 defects caught in time at each check's peak setting (%, 1 dp): beacon_loss_z @3.4: 28.2%; expo_rate_gap_pp @3.5: 19.2%; srm_assign_p @0.003: 14.1%; late_share_gap_pp @1.2: 9.0%; evpu_dev_pct @24.0: 5.1%
