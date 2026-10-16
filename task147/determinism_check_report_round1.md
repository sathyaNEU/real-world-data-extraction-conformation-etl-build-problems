# determinism-check report, task147, 2026-10-16, round 1

The judge ran at stage 4, isolated, at medium effort, on a fresh unzip of the stage 3 cut (commit cd5abab, target.zip
sha256 5c3be492ee795008), before the stage 4 repairs. Its FIX_NOW (78 guest-count amendments dated after the extract) was
repaired in the generator at c06e15f, together with the rule 3 audit's findings; the call did not move (the closing week
about 400, the concert week next at about 200). This verdict is history; the shipped cut's verdict is
`determinism_check_report.md`. Verbatim:

# Verdict (task147), judged from the shipped bundle only

**Verdict:** DETERMINISTIC

**Disposition:** FIX_NOW. The one hygiene defect is 78 ADULTS rows in `pms_amendment_log_2027-07-01.csv` dated after the extract (2 Jul to 19 Dec 2027). Clamp or drop them. They touch no stay dates, so the analytic surface is unchanged and no model rerun is needed. Otherwise the package is ship-ready.

**Why:**
- The main call is forced by a stay-level availability constraint that the pickup history cannot show. On the 06:12 book, Fri 13 and Sat 14 Aug 2027 are full (480 each). A stay needs a room on every night, so no later stay can touch either night.
- Once those stays are removed, the closing week forecasts at about 417 room-nights above 380 and the concert week at about 215. Both reproduce the golden's 400 and 200.
- Methods that ignore the constraint put the concert week first. Every one I ran does:
  - additive pickup capped at 480: 560
  - ratio pickup: 506
  - past actuals from the night audit: about 503
- No file ranks the weeks wrongly, and no file states the constraint.
- One residual fork is flagged under Evidence (partial recovery of displaced stays). It is not a defect on the shipped text.
- Taxonomy: none.

## Evidence

**Method.** I rebuilt the book from `pms_reservations_extract_2027-07-01.csv`, excluding day-use and reservations cancelled by the cut. Dates were reverted to "as then stood" by undoing later changes in `pms_amendment_log_2027-07-01.csv`. The cut for each of 2022 to 2026 was the Thursday five weeks before that year's opening night, at 05:12 UTC (06:12 local). Past nights were aligned by offset from the festival's first Friday (`festival_programme_dates.json`).

**Checks on the inputs.**
- The amendment-log chain is continuous. Its last value equals the extract's current date on all 12,512 date fields.
- PMS stayed-room totals tie exactly to `night_audit_statistics_2022-2027.xlsx` for 2022, 2023, 2024 and 2026 (max difference 0). I did not run 2025, and I recomputed the 2024 and 2026 totals against sheets with the other header layout.

**Main call and critical components.**

| Item | Golden | My recompute | Result |
|---|---|---|---|
| Fri 13 and Sat 14 Aug 2027 on the book at the cut | 480, 480 | 480, 480 | reproduced |
| Later-stay room-nights on the concert week's other five nights, past stays touching Fri or Sat, 5-season mean | about 420 | 423 (2022 to 2026: 458, 440, 372, 458, 389) | reproduced |
| Concert week above 380 | about 200 | 215 (195 with full nights at 470; 186 with the EVT no-show rate of about 3 percent) | reproduced |
| Closing week above 380 | about 400 | 417 | reproduced |
| Opening week | below the concert week | 60 | reproduced |
| Week after the concerts | below the concert week | 139 | reproduced |

The concert week is second under every variant. Subsets of 3 or 4 seasons give 220 to 222. Pickup as a share of headroom gives 236. The closing week stays at 407 to 417.

**Easy route.** Per-night pickup without the stay constraint gives the concert week 560 against 417 for the closing week.

**Residual fork, not a defect on the shipped text.** The golden loses displaced stays entirely.
- If a guest turned away from Fri or Sat instead books a shorter stay and the hotel recovers roughly half or more of the 423 room-nights on the other nights, the concert week reaches about 430 and ties or passes the closing week.
- Neither the past seasons nor the 2027 book shows any such recovery, and no past night was full to test it. A literal executor therefore removes the stays outright.
- The golden's own sentence ("a stay is sold only if every night of it has a room") states the intent, but only in the golden, not in the files.
- This is a moderate fragility that a strong solver could argue. It is not an input-noise near-tie: the gap is about 200 on about 415.

**Supplementary tables.** All recomputed from the files and all reproduce.
- Task counts, as in the golden, in every roster week and column:
  - 27 Jul: crew 920 / 1,100, Brennock 184 / 206
  - 3 Aug: crew 796 / 986, Brennock 113 / 166
  - 10 Aug: crew 788 / 1,336, Brennock 341 / 577
  - 17 Aug: crew 929 / 1,460, Brennock 145 / 249
  - 24 Aug: crew 962 / 1,574, Brennock 187 / 276
- I counted Completed Departure and Stayover tasks only. DND, Refused and Re-clean rows are excluded.
- Brennock credit goes to:
  - the six regular-temp logins; the three now shown as crew (`adreszer`, `dcosta`, `gmocanu`) are on Brennock's timesheet every day they have tasks
  - the `block01` to `block10` logins
  - supervisor-login tasks whose note names a Brennock temp
- Tasks under supervisor "tablet down" notes go to crew.
- All completed-task closing times fall on the service date.
- Crew overtime by date worked in `reference`, from `payroll_overtime_lines_2026-P14-P19.csv`: 17.25, 20.75, 15.25, 11.25, 14.25. The weekly sums reproduce.
- Billable hours:
  - I joined the eight block temps to their day badges in `reception_day_badge_log_2026-08.csv`.
  - I took first entry and last exit from `staff_access_events_2026-08.csv`, with LB-02 shifted +1 h from UTC.
  - Framework clauses 4.1 to 4.3 gave 59.25, 59.50, 55.75, 59.25, 59.75, 59.75, 59.75 (Mon 10 Aug to Sun 16 Aug 2026).
  - Marina Alves on 12 Aug is the 4.00 h floor (sent home at 10:00).
  - At EUR 22.56, Sunday at 1.25 times, the week's charge is EUR 9,654.27. Each day's amount is exact to the cent, so there is no rounding fork.
- The invoice's EUR 9,813.60 is a distractor.

**Clock convention, not stated in any file.** Nothing says LB-02 runs on UTC.
- The offset is derivable from the data. Final exits are 170 at LB-02 in the 15:xx hour against 795 at SE-02 in the 16:xx hour.
- Per-badge IN/OUT alternation breaks 16 times with LB-02 +1 h and 30 times unshifted.
- With the shift, the billable total is 9,654.27. Unshifted it is 9,293.31.
- This is data-derivable, but it is the only unstated convention in the supplements. It is an "ask" and is free of rule 3.

## Files/Hygiene
**PASS**, with one FIX_NOW item (the late amendment rows below).
- 20 files in 5 formats: pdf (3), xlsx (6), csv (9), json (1), txt (1).
- `pms_reservations_extract_2027-07-01.csv` has 361,527 rows (34.5 MB), so the large-file gate is met.
- Distractors are present: the invoice, the compset rate shop, the tourism survey and the HR list.
- Provenance is clean. There is no authoring language, the docProps carry in-fiction authors, and I found no hidden sheets (grep of workbook.xml for hidden or veryHidden state returned nothing).
- Temporal coherence has one flaw. `pms_amendment_log_2027-07-01.csv` has 78 ADULTS changes with `changed_utc` after the extract (2027-07-02 to 2027-12-19), all outside the 06:12 cut. They do not affect any decisive figure, so this is a non-stump hygiene fix.
- The `hk_task_log` temp note forms ("Brennock - X", "agency - X", "X (Brennock)", "Brennock temp X") repeat in a templated way. This is minor.
- Nothing is exclusion-level.
- I could not run the cross-batch fingerprint check from this directory.

## Stump power
Good, and I expect a strong solver to fall to the concert week.
- The decisive, non-obvious step is to see that stays through the sold-out Fri and Sat cannot be sold, and to remove that pickup.
- The nightly pickup average, the ratio pickup and the same-weeks-last-year actuals all put the concert week first. That is where most runs will land.
- The package does not document the correction. HK-04 gives only the capacity and "forecast".
- The supplementary asks add independent difficulty, each with its own unstated device:
  - the three logins held as crew
  - re-cleans, DND and refused rooms
  - the UTC reader
  - the day-badge join
  - the 4 h floor
  - the Sunday rate
- Too-easy signals: none.

## Stumping type
`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`

Reported numbers are fine: the book, the night audit and the past seasons are internally consistent. The difficulty is a forecast the correctly read past does not pin (a length-of-stay inventory constraint on a new demand event). On clean data it would still stump. Gate G passes.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`

- **Domain.** Hotel booking-pace and pickup forecasting under length-of-stay availability is the field's own estimate; the swap test fails for any other nouns. Housekeeping labour is sized on forecast occupied rooms above crew capacity.
- **Layer 1.** UTC and local clocks, amendment-log "as it stood" dates, retired channel codes, seasons aligned by first Friday, and attribution of tasks across the app, HR, timesheet and note sources.
- **Layer 2.** A pickup forecast under the length-of-stay constraint, ranking five weeks against capacity.
- **Easy route.** A strong analyst who read everything correctly files the unconstrained nightly pickup, which gives the concert week at about 560 to 600 first, against the golden's closing week.

## Fix
- **Where:** input_files.
- **What:** clamp or remove the 78 post-extract amendment rows (all ADULTS) from `pms_amendment_log_2027-07-01.csv`.
- **Optional:** state in the filed text that stays touching a sold-out night cannot be sold and are not recovered as shorter stays. This closes the partial-recovery fork without giving away the method.
- **Optional:** one ranking fact or a one-line note on the clock of LB-02 in the access export would remove the only unstated supplementary convention.
- **Not needed:** model rerun for the first item.
