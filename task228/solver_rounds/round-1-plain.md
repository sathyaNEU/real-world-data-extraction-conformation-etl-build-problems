# solver round: round 1, plain

**Proxy score 50.4 / 100** (recommendation 4.3 of 35, instruction 7.0 of 7, asks 39.1 of 58). Main call missed. 6 of 12 ask items cracked (80 per cent of tokens).

## Main call

golden: Wire the 2027 peak paging alert to the Pageview beacon loss check (beacon_loss_z) at a setting of 3.3, live from 4 January to 28 March 2027.

solver: From 4 January to 28 March 2027, wire the paging alert to evpu_dev_pct (Events per exposed user) at 12.0 % (it pages when |value| >= 12): on the FY2026 replay audit it pages 20 of 452 sound runs (4.4%, within the 5.0% budget) and catches 29 of 68 defects in time (42.6%). The runner-up is beacon_loss_z at z 3.3, which pages 15 of 452 (3.3%) and catches 19 of 68 (27.9%), so it catches 10 fewer. The current srm_assign_p at 0.001 would catch only 7 of 68.

tokens matched 6 of 7 (3.3, 4, 28, Wire, Pageview, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| peak_alert_config.json | 1 | 1 | 1 | 100% |
| peak_alert_config.json | 2 | 1 | 3 | 33% |
| peak_alert_config.json | 3 | 3 | 3 | 100% |
| peak_alert_config.json | 4 | 6 | 6 | 100% |
| alert_replay_fy2026.xlsx | 1 | 18 | 24 | 75% |
| alert_replay_fy2026.xlsx | 2 | 0 | 2 | 0% |
| alert_replay_fy2026.xlsx | 3 | 12 | 12 | 100% |
| alert_replay_fy2026.xlsx | 4 | 6 | 6 | 100% |
| peak_alert_tradeoff.png | 1 | 2 | 6 | 33% |
| peak_alert_tradeoff.png | 2 | 1 | 1 | 100% |
| peak_alert_tradeoff.png | 3 | 0 | 1 | 0% |
| peak_alert_tradeoff.png | 4 | 2 | 3 | 67% |

## Solver's path

1. Read prompt.md, DQ-07 rev3 (docx text), vigia_check_catalogue.json, vigia_export_fields.md, export_notes, and handbook s6. Rules taken from these: catch = page on the first bad night or within the 2 nights after it; budget = at most 1 in 20 sound experiments paged on any night of the run, read off the full audit year; setting = most sensitive catalogue setting within budget; check = most defects caught, with fewer sound pages as the tie-break.
2. Parsed replay_audit_FY2026.xlsx sheets FY26 Q1-Q4 (header row 4, 130 rows each). Result: 520 experiments, 452 sound and 68 defects (12/15/21/20, which matches each sheet's footer). First bad night parsed as dd/mm/yyyy.
3. Joined the audit's Exp key to experiment_bookings_fy2026.csv exp_key to get experiment_id. All 520 matched, with no mismatches in last night or booked nights. Every defect's first bad night falls between launch and last night - 2.
4. Concatenated both Vigia parquets (126,685 rows) and dropped the late-load re-run duplicates on (experiment_id, check_night, check). There were 2,995 duplicate keys and their values were identical, so nothing changed. Every audited experiment has a full row for each booked night. Units are consistent across catalogue_rev v3 and v4.
5. For each check and each catalogue setting, applied the firing rule (srm: value <= setting; the others: |value| >= setting). Counted sound experiments with any firing night, and defects firing on fbn..fbn+2. Budget cap: 22 of 452 (5%).
6. Most sensitive in-budget settings: srm 0.005 (13 sound, 9 caught); expo 3.5 (21, 3); evpu 12 (20, 29); beacon 3.3 (15, 19); late 0.9 (19, 8). evpu wins with 29, and beacon_loss_z is second with 19, a gap of 10. By defect class, evpu catches 22 of 22 impression-not-firing and 7 of 7 double-fire defects.
7. Current-alert record: took vigia-bot tickets from dq_tracker_legacy_export (night parsed from the summary) and source=vigia tickets from dq_incidents json (check_night). Dropped the 4 legacy tickets carried over via imported_from (DQ-3265/3267/3268/3270) so they are counted once, at their json outcome. Kept FY2026 nights (2025-10-01 to 2026-09-30) and bucketed by the quarter of the night, not the UTC created date. Result: 55 pages, 40 confirmed, 15 not a defect. All 55 page nights have srm_assign_p <= 0.001 in Vigia.
8. Peak bookings: from peak27_booking_queue.csv, ignored drafts and took each booking_ref's latest accepted/superseded/cancelled version. Kept the 43 whose latest version is accepted and dropped 4 cancelled. All launch 2027-01-04 to 2027-02-25, Mon-Thu, 28 nights. Mapped each to its owner via surface_owners.csv effective on the launch night (CHK goes to SQ-04 from 2026-12-01; REV goes to SQ-02 from 2027-02-01), then to squads.csv (SQ-05 is named hosts from 2026-11-16). Counts: search 9, listing 11, payments 8, hosts 3, guest-comms 6, apps 6.
9. Live window from handbook 6.2 and DQ-07 s7: 2027-01-04 to 2027-03-28. Percentages are rounded to 1 dp from the counts above.

confidence: high

notes: The replay applies DQ-07 s3's catch definition directly. If a false page before the first bad night kept a ticket open through the catch window (s6), evpu could lose up to 2 catches (SRC-0372, MSG-0525), which would leave it at 27 and still ahead of beacon_loss_z's 19. Four evpu values below -100% (impossible values, two of them on sound experiments) were kept as recorded; dropping them would not move the 12% setting. One tracker ticket, DQI-1118, is a confirmed defect even though its recorded first bad night falls after the night it paged; it is counted as the tracker records it.

### peak_alert_config.json (solver's answers)
- check: evpu_dev_pct (Events per exposed user, unit percent, pages when abs(value) >= setting)
- setting: 12.0 (percent)
- live window: first night 2027-01-04 to last night 2027-03-28 inclusive (Lisbon nights; fixed at the 14 Dec 2026 freeze)
- on-call channel per squad with peak tests: search SQ-01 #oncall-search; listing SQ-02 #oncall-listing; payments SQ-04 #oncall-payments; hosts SQ-05 #oncall-hosts (was host-tools until 2026-11-15); guest-comms SQ-06 #oncall-guest-comms; apps SQ-07 #oncall-apps. checkout SQ-03 has no peak tests because CHK passes to payments from 2026-12-01. Platform on-call also gets every page under DQ-07 s6.

### alert_replay_fy2026.xlsx (solver's answers)
- srm_assign_p: most sensitive in-budget setting p <= 0.005; sound runs paged 13 of 452 counted (2.9%); defects caught in time 9 of 68 (13.2%)
- expo_rate_gap_pp: setting 3.5 pp; sound paged 21 of 452 (4.6%); defects caught 3 of 68 (4.4%)
- evpu_dev_pct: setting 12.0 %; sound paged 20 of 452 (4.4%); defects caught 29 of 68 (42.6%) - chosen
- beacon_loss_z: setting z 3.3; sound paged 15 of 452 (3.3%); defects caught 19 of 68 (27.9%)
- late_share_gap_pp: setting 0.9 pp; sound paged 19 of 452 (4.2%); defects caught 8 of 68 (11.8%)
- budget: at most 1 in 20 sound runs paged = 5.0%, i.e. at most 22 of 452
- second check and gap: beacon_loss_z at 3.3 catches 19 of 68, which is 10 fewer defects than evpu_dev_pct (29)
- current alert FY2026 record by quarter of night paged (srm_assign_p at 0.001): FY26 Q1 (Oct-Dec 2025): 16 pages, 13 confirmed defects, 3 false alarms; FY26 Q2 (Jan-Mar 2026): 9 pages, 5 confirmed, 4 false; FY26 Q3 (Apr-Jun 2026): 15 pages, 11 confirmed, 4 false; FY26 Q4 (Jul-Sep 2026): 15 pages, 11 confirmed, 4 false; FY total 55 pages, 40 confirmed defects, 15 false alarms
- peak tests booked per squad (owner on launch night): search 9, listing 11 (9 LST + 2 REV launched on or after 2027-02-01), payments 8 (3 PAY + 5 CHK), hosts 3, guest-comms 6 (4 MSG + 2 REV launched before 2027-02-01), apps 6, checkout 0; total 43 standing bookings

### peak_alert_tradeoff.png (solver's answers)
- share of defects caught per check (%, 1 dp): srm_assign_p 13.2%; expo_rate_gap_pp 4.4%; evpu_dev_pct 42.6%; beacon_loss_z 27.9%; late_share_gap_pp 11.8%
- share of sound runs paged per check (%, 1 dp): srm_assign_p 2.9%; expo_rate_gap_pp 4.6%; evpu_dev_pct 4.4%; beacon_loss_z 3.3%; late_share_gap_pp 4.2%
- budget line: 5.0% of sound runs paged
- chosen check marked and title: evpu_dev_pct marked; title along the lines of 'Peak 2027: page on events per exposed user at 12% - catches 42.6% of defects (29/68) and pages 4.4% of sound runs, inside the 5.0% budget'
