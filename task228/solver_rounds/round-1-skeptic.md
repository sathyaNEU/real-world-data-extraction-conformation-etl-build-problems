# solver round: round 1, skeptic

**Proxy score 97.6 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 55.6 of 58). Main call LANDED. 11 of 12 ask items cracked (80 per cent of tokens).

## Main call

golden: Wire the 2027 peak paging alert to the Pageview beacon loss check (beacon_loss_z) at a setting of 3.3, live from 4 January to 28 March 2027.

solver: Through the 2027 winter peak (live 4 Jan to 28 Mar 2027), the paging alert should page on beacon_loss_z (Pageview beacon loss) at |z| >= 3.3. In the FY2026 replay it would have paged 6 of 123 sound 28-night runs (4.9%, inside the 1-in-20 budget) and caught 19 of 68 audited defects in time (27.9%). That is 7 more than the runner-up, evpu_dev_pct (Events per exposed user), which at its tightest in-budget setting of 18% catches 12 of 68 (17.6%). So not the events-per-user check Isabela expects: on 28-night runs evpu at 12% would page 9 of 123 sound runs (7.3%) and break the budget.

tokens matched 4 of 7 (3.3, 4, 28, Wire, Pageview, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| peak_alert_config.json | 1 | 1 | 1 | 100% |
| peak_alert_config.json | 2 | 3 | 3 | 100% |
| peak_alert_config.json | 3 | 3 | 3 | 100% |
| peak_alert_config.json | 4 | 6 | 6 | 100% |
| alert_replay_fy2026.xlsx | 1 | 24 | 24 | 100% |
| alert_replay_fy2026.xlsx | 2 | 1 | 2 | 50% |
| alert_replay_fy2026.xlsx | 3 | 12 | 12 | 100% |
| alert_replay_fy2026.xlsx | 4 | 6 | 6 | 100% |
| peak_alert_tradeoff.png | 1 | 6 | 6 | 100% |
| peak_alert_tradeoff.png | 2 | 1 | 1 | 100% |
| peak_alert_tradeoff.png | 3 | 1 | 1 | 100% |
| peak_alert_tradeoff.png | 4 | 3 | 3 | 100% |

## Solver's path

1. Read prompt.md, DQ-07 rev 3 (docx text), vigia_check_catalogue.json, vigia_export_fields.md, export_notes, handbook s6, squads.csv and surface_owners.csv. The rules applied: audit verdicts govern; a defect is caught if the check fires on its first bad night or either of the next two nights; budget is at most 1 in 20 sound experiments paged on any night of their run, over the season the setting is live, read off the full audit year; most sensitive catalogue setting within budget; most defects caught wins, ties go to fewer sound pages.
2. Concatenated the two Vigia parquets (65,100 + 61,585 rows). Dropped 2,995 duplicate rows from re-runs after late warehouse loads, keyed on experiment, night and check; re-run values were identical. That left 123,690 rows, all inside each experiment's booked run.
3. Joined to experiment_bookings_fy2026.csv on experiment_id. Every one of the 1,378 bookings has complete nightly coverage.
4. Parsed the replay_audit_FY2026.xlsx quarter sheets (dd/mm/yyyy dates): 520 experiments, 452 sound and 68 defect. Per-quarter defect counts 12, 15, 21 and 20 match the sheet footers. Last night and booked nights match the bookings file for all 520. All first bad nights fall between launch and last night minus 2. All 30 first bad nights that also appear in the trackers agree with the audit.
5. Method test: replayed srm_assign_p <= 0.001 over all experiments, applying DQ-07 s6. A page is skipped while a prior ticket is still open at the 06:15 Lisbon run, and an experiment is muted after a confirmed defect (actual closed_at times used). This reproduced exactly the 58 vigia-bot tickets across the legacy CSV and the new JSON, with none missing and none extra. The 4 legacy in-progress tickets were de-duplicated against their imported_from copies.
6. FY2026 current-alert record: kept the 55 vigia tickets whose check night falls between 2025-10-01 and 2026-09-30. Legacy nights were parsed from the summary text; the 3 September 2025 tickets are excluded. Grouped by fiscal quarter of the check night, not of the UTC created date, which would move 7 tickets across quarters: 16/13/3, 9/5/4, 15/11/4 and 15/11/4.
7. Peak runs are all 28 nights (handbook 6.2), and the budget applies over the season the setting is live. So sound runs were counted on the 123 sound 28-night audit experiments from all four quarters, giving a cap of 6. Defects were counted on all 68 per DQ-07 s3.
8. For each check, walked the catalogue settings from most to least sensitive and stopped at the first within budget: srm 0.01 (6/123, 10/68), expo 3.25 (6/123, 4/68), evpu 18 (6/123, 12/68), beacon 3.3 (6/123, 19/68), late 0.9 (6/123, 8/68). Beacon wins by 7 over evpu. Requiring no earlier page before the first bad night changes none of these figures.
9. Contrast check: counting all 452 sound runs (14- and 28-night) would pick evpu at 12% (20/452 sound, 29/68 caught). But evpu at 12% pages 9 of 123 sound 28-night runs (7.3%), over budget for peak-length runs, so that reading was rejected.
10. Peak bookings: from peak27_booking_queue.csv (67 versions, 47 refs), took each booking at its latest accepted version, ignoring later drafts and dropping refs whose latest version is cancelled (BK27-103, 208, 211, 220). That leaves 43 tests, all 28 nights, launching Monday to Thursday between 2027-01-04 and 2027-02-25. Mapped each surface to its owner on the launch night (CHK goes to SQ-04 from 2026-12-01; REV goes to SQ-02 from 2027-02-01) and each squad to its name and channel valid then (SQ-05 is hosts / #oncall-hosts from 2026-11-16). Result: search 9, listing 11, payments 8, hosts 3, guest-comms 6, apps 6.

confidence: Medium-high. The data handling is verified by the exact 58/58 ticket reproduction and the audit footers. The main judgement is counting the budget on 28-night sound runs, to match the all-28-night peak. Counting all 452 sound runs would instead pick evpu_dev_pct at 12%.

notes: Neither DQ-07 nor the handbook says outright whether the page budget for the peak setting should be measured on 28-night runs only; I read 'over the season a setting is live' plus the 28-night peak booking rule as requiring it. The platform on-call channel is not given in the files; guardrail_watchlist and site_status_events were not needed.

### peak_alert_config.json (solver's answers)
- check: beacon_loss_z (Pageview beacon loss), pages when abs(value) >= setting
- setting: 3.3 (z)
- live window: 2027-01-04 to 2027-03-28 (peak first night to last night, inclusive; fixed at the 14 Dec 2026 change freeze)
- on-call channel per squad with peak tests (43 standing bookings): SQ-01 search #oncall-search (9 tests); SQ-02 listing #oncall-listing (11); SQ-04 payments #oncall-payments (8); SQ-05 hosts #oncall-hosts (3); SQ-06 guest-comms #oncall-guest-comms (6); SQ-07 apps #oncall-apps (6). SQ-03 checkout has no peak tests (CHK moves to SQ-04 from 2026-12-01). Platform on-call is also paged under DQ-07 s6, but its channel is not listed.

### alert_replay_fy2026.xlsx (solver's answers)
- per-check most sensitive in-budget setting, sound paged, defects caught: srm_assign_p 0.01 (p): sound paged 6 of 123 (4.9%), defects caught 10 of 68 (14.7%); expo_rate_gap_pp 3.25 pp: 6 of 123 (4.9%), 4 of 68 (5.9%); evpu_dev_pct 18.0%: 6 of 123 (4.9%), 12 of 68 (17.6%); beacon_loss_z 3.3 z: 6 of 123 (4.9%), 19 of 68 (27.9%); late_share_gap_pp 0.9 pp: 6 of 123 (4.9%), 8 of 68 (11.8%). Budget: at most 1 in 20, i.e. at most 6 of 123 (5.0%).
- second check and shortfall: evpu_dev_pct at 18.0% is second with 12 of 68 caught, 7 fewer defects than beacon_loss_z (19 of 68)
- current alert (srm_assign_p at 0.001) FY2026 record by quarter of the night paged for: Q1 (Oct-Dec 2025): 16 pages, 13 confirmed defects, 3 false alarms; Q2 (Jan-Mar 2026): 9 pages, 5 confirmed, 4 false; Q3 (Apr-Jun 2026): 15 pages, 11 confirmed, 4 false; Q4 (Jul-Sep 2026): 15 pages, 11 confirmed, 4 false; FY2026 total: 55 pages, 40 confirmed, 15 false alarms
- peak tests booked per squad (owner of the surface on launch night): search 9; listing 11; payments 8; hosts 3; guest-comms 6; apps 6; checkout 0; total 43

### peak_alert_tradeoff.png (solver's answers)
- share of defects caught per check (%, 1 dp): srm_assign_p 14.7%; expo_rate_gap_pp 5.9%; evpu_dev_pct 17.6%; beacon_loss_z 27.9%; late_share_gap_pp 11.8%
- share of sound runs paged per check (%, 1 dp): 4.9% for all five checks (6 of 123)
- budget line: 5.0%
- chosen check marked: beacon_loss_z at 3.3
- title: Peak 2027 alert: page on pageview beacon loss at |z| >= 3.3, which catches 27.9% of defects vs 17.6% for events per user, within the 5.0% page budget
