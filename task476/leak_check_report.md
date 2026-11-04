# leak check, task476

**Verdict: REVIEW.** 11 files read, 16 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: rating, emissions-inventory, measurements, method, relation, architecture, register, payment-claims, application, golden, nothing, family, window, station, controller, control, vapour, decisive, sentence, driver, session, converted, mechanism, screen, previous

## 3 answer figures in the pack (REVIEW 8)
- **REVIEW** `gauge/bp1_rating7_report_2023.pdf`: golden figure 142 appears: ...022-09-13 2.27 54.3 53.4 +1.8 2022-11-30 3.05 138 142.1 -2.9 2022-12-15 7.36 2,050 2127.0 -3.6 2023-01-...
- **REVIEW** `license/flow_monitoring_plan_2024.pdf`: golden figure 404 appears: ...403 and the monthly spring volumes under Article 404 in its annual flow report, filed by January 31 of...
- **REVIEW** `license/flow_monitoring_plan_2024.pdf`: golden figure 403 appears: ...d at BP-1. The setpoint is held above the Article 403 minimum by an operating margin. 4. Reporting The...
- **REVIEW** `license/license_order_excerpt_2019.pdf`: golden figure 404 appears: ...er issuing new license, excerpt: Articles 403 and 404 Article 403. Minimum flow in the bypassed reach....
- **REVIEW** `license/license_order_excerpt_2019.pdf`: golden figure 403 appears: ...ject Order issuing new license, excerpt: Articles 403 and 404 Article 403. Minimum flow in the bypassed...
- **REVIEW** `reports/2025_annual_flow_compliance_report.pdf`: golden figure 404 appears: ...June), both computed at BP-1 on Rating 7. Article 404 The bypassed reach passed 17,640 acre-feet in May...
- **REVIEW** `reports/2025_annual_flow_compliance_report.pdf`: golden figure 403 appears: ...Compliance Report, filed January 22, 2026 Article 403 The bypassed reach met its minimum flow on every...
- **REVIEW** `reports/2025_annual_flow_compliance_report.pdf`: carries 15 of 20 distinctive words of the committed call: 'The bypassed reach fell below its Article 403 minimum from 29 July to 13 September and from 21 September to 31 October 2'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `gauge/bp1_rating7_report_2023.pdf`: 5 of 25 stump-paragraph terms appear (rating, measurements, register, station, control); read whether the document names the move
- **REVIEW** `license/flow_monitoring_plan_2024.pdf`: 3 of 25 stump-paragraph terms appear (method, station, control); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-04 (general-purpose, sonnet, medium), architecture 5, on a fresh copy of prompt.txt and target/ (target.zip sha256 7e78020ac42e5e8e56a6054ec9b669778f853799c6f7d111687bf4ca24b85bf1). Sweep 4's lines and the answer-figure numbers were kept out of the brief and ruled in the main thread.

# Leak read, task 476 v5 (read and quote only; nothing solved)

1. Decisive step: no file announces it. Nearest is gauge/bp1_field_visits_2026.csv, 2026-07-29 remark: "Post-storm visit. Debris line at 6.7 ft on staff. Control riffle reworked by the 27 July flood. Orifice line clear." It states the cause of the measurement departing from the rating (a changed control) outright; see item d.
2. Ranking or scoring of candidates: none. No file ranks periods or causes. operations/bypass_release_log_2026.csv lists setpoints and events, not a verdict.
3. Files that exist only to help: none clearly. The nearest is bp1_station_register.xlsx "Rating history" and gauge/bp1_rating7_report_2023.pdf, which are ordinary rating documentation. bp1_water_temperature_2026.csv, powerhouse_precipitation_2026.csv and daily_generation_2026.csv look like context/distractors.
4. Figure or name reading as the answer: none. Closest are the 2025 report's "53.6 cfs" and "17,640 acre-feet ... 9,870 acre-feet", which are 2025 values (53.6 also equals the 2026-07-26 visit discharge, a coincidence in text only).
5. Filed sentence fixing the figure/population: license_order_excerpt_2019.pdf Art. 403, "Compliance is determined on the daily mean flow in the bypassed reach for each calendar day, local time. A day whose mean flow is below the minimum for that day is a deviation." Fixes: daily mean per local calendar day (the logger is PST all year per the register, so local PDT days must be formed), threshold 50 cfs Jul 1 to Sep 30 and 30 cfs from Oct 1. Art. 404: "pass at least 20,000 acre-feet ... report the volume passed in each month and the peak flow of the period, with its date and time" fixes May and June volumes and the May 1 to Jun 30 peak. Monitoring plan s.2, "Discharge is computed from the stage record by the standard methods of the U.S. Geological Survey for stage-discharge stations", leaves the method as the standard one (field measurements used to correct the rating).
6. What decides it: an analytical choice (checking the stage-discharge record against the field measurements and correcting the rating where the control changed, rather than applying Rating 7 blindly). Evidence is in field_visits (2026-07-29 45.7 cfs at 2.27 ft, 2026-08-25 45.8 cfs at 2.28 ft versus 53.6 cfs at 2.27 ft on 07-26) and the plan's "standard methods of the U.S. Geological Survey". The time-zone and daily-mean conventions are filed in Art. 403 and the register, so they read as Layer 1.

## Sweep items
a. harmless, because it is the licensee's own 2025 filing (dated January 22, 2026, signed by the Environmental Manager), reports 2025 values, and says nothing about 2026 methods; only "computed at BP-1 on Rating 7" is a mild nod, which reads as ordinary reporting.
b. harmless, because the values (equations, 17 measurements, differences within 3.3 percent) are ordinary rating-report content; nothing is an answer. Mild note: "Low and medium flows are controlled by the gravel and cobble riffle below the orifice" sets up the later riffle remark but is standard rating prose.
c. harmless, because both are plain license text and plan boilerplate; article numbers 403/404/405 are just the articles; no sentence names an answer.

d. Mostly ordinary hydrographer log (consistent columns, plausible remarks), but the 07-29 remark "Control riffle reworked by the 27 July flood" diagnoses the cause for the analyst; a real hydrographer might write something like it, but it is the one place that reads as telling the analyst what the measurement means. Also "Summer setpoint in effect since midnight" on 07-01 and "Fall pulse in progress. Unit offline on low inflow." on 09-16 echo the operations log (harmless cause cues). Leak (mild): the riffle sentence; consider softening to observed conditions only.
e. Reads as the station's own register (datum, orifice height, control, rating history, logger clock "Pacific Standard Time (UTC-08:00) all year"). No note points at a step; the PST line is ordinary station metadata.
f. No steering sentences. Rating report: "All 17 measurements plot within 5 per cent of Rating 7" and the riffle control sentence are ordinary. Plan: "The setpoint is held above the Article 403 minimum by an operating margin" and visits "at least every six weeks ... after high flows" are ordinary content, though the latter mildly signals that visits matter.

Realism: field_visits_2026.csv has mild tells of tidiness: every discharge measurement is exactly 40 minutes, start is always arrival plus 10 minutes, staff and logger gage heights agree to the hundredth on nearly every visit, and the remark "Staff and logger agree." repeats. The measured discharges vs rating look fairly clean (07-26 53.6 at 2.27 versus table 53.36). Rating report is uniformly tidy (all 17 differences within 3.3 percent, round-looking). Other files: none.
