# FC25 — The desk's call on the advance GDP print, when the trade report that feeds three of its lines lands after the agency has frozen its inputs

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · national-accounts nowcasting |
| Mirrors | Forecasting a figure that a counterparty compiles from upstream feeds on its own unpublished cut-off (ad-platform daily reports that carry a partner's conversions forward when its batch misses the cut, marketplace sales dashboards that hold a seller feed's last day when it arrives late, warehouse stock snapshots that keep a site's last scan when its feed is delayed, consensus-beating earnings when one segment reports after the close) |
| Decision shape | One figure committed at a date: the desk's call on the advance print, sent to clients at 18:00 the business day before the release |
| Committed call | Real GDP growth in the agency's advance print, percent at an annual rate, to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B, the agency's compile rule recovered from the pilot log as a mixture: one report's three lines carried from month 2 whenever the report lands after a freeze four business days before the print; with a labour-input rate validated on quarters when goods and services hours moved together below it |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #8 papers over a failed reproduction · #13 validates on one population, applies to another · #3 stops at a close but inexact match |
| Calibration form | Pilot log: sixteen quarters of the desk's tracking pilot, each quarter's filed call with every line's monthly inputs as held at filing, beside the advance print line by line |
| Driving force | One upstream release, the trade agency's advance trade and inventories report, feeds three lines of the print: exports, imports and wholesale and retail inventories. The statistics agency freezes its inputs four business days before the print, and when the report lands later all three lines carry month 2 forward. So the pilot's misses on those lines are zero in twelve quarters and one third of each line's month-3 change in four, which no per-line constant reproduces. This quarter the report came out two business days before the print, after imports fell $500bn at an annual rate in month 3 and the inventory build stopped: the desk's data say 2.5%, and the print will say 1.0%. The freeze is in no document; only a four-day freeze with month-2 carry reproduces all 128 line contributions, with business days counted on the holiday calendar. |

## 1. Situation

A bank's research desk sends clients its call on the statistics agency's advance estimate of quarterly real GDP growth at 18:00 on the
business day before the release. The research memo files the desk's tracking: each expenditure line rebuilt from the monthly source the
agency's handbook lists for it, every source at its latest values at filing, consumer services extrapolated with total private hours. The
desk ran the tracking as a pilot for sixteen quarters and logged each filed call, with every line's inputs, beside the advance print line
by line. This quarter a systems outage delayed the trade agency's advance trade and inventories report, which came out two business days
before the print.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the source releases and their vintages, the release calendar, the hours file, the pilot log and the
  advance prints. No one's claim about their own numbers is overturned. The difficulty is which of this quarter's numbers the agency will
  have used.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the validation unit's basis. The tracking on service-providing hours, add-factored on the
  pilot, still says 2.7%.
* **Instrument repair.** No file is suspect. The advance prints are what the agency published, the release calendar and the source
  archive hold every release with its time stamp and every vintage, and the hours file is complete by supersector. The release time is a
  different attribute from what the agency held, so it is not a narrower record of it. Take the deepest repair anyway, a manifest of the
  sources the agency held at each freeze, this quarter's included: rung 0 still returns 2.1%, rung 1 2.5% and rung 2 2.7%, since none of
  them reads it, and the carry, the three lines grouped under one report and each line's month 2 still have to be built to turn "report not
  held" into 1.0%.
* **Lens swap.** The naive read and the answer differ in moment: the data the desk holds at filing, against the data the agency held when
  it froze its inputs four business days before the print.

## 3. The driving force

A strong solver implements the memo's tracking, reads the handbook's line that services follow "labour input in the industries that
provide them", and sees that this quarter the factories cut shifts: private service-providing hours grew 2.0% at an annual rate against
1.3% for all private hours. Services move to their own industries' hours and the call rises to 2.5%. It then back-tests the pilot and
finds the tracking exact on every line except three, which missed the print in four of sixteen quarters. The desk's standard repair is an
add-factor per line, and it lifts the call to 2.7%. The misses are not noise. Exports, imports and wholesale and retail inventories all
come from one release, the advance trade and inventories report, and the agency freezes its inputs four business days before the print.
When the report lands after the freeze, the agency carries each of its lines from month 2. In twelve pilot quarters the report was in
and the misses were zero; in four it was not, and each line missed by a third of its month-3 change, all three in the same quarters. This
quarter the report came out two business days before the print. Imports fell $500bn at an annual rate in month 3 after a front-loaded
month 2, and the inventory build stopped. The print will carry month 2 instead: imports $166.7bn higher, inventories $80bn higher and
exports $3.3bn lower, 1.5 points off the desk's 2.5%.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The memo's tracking: each line from its handbook source at its latest values at filing, the report's month 3 included, services extrapolated with total private hours | 2.1%, +1.1 pts | The filed method on the desk's own pipeline, with the desk's best record: zero misses in twelve pilot quarters | **E17 (validated on one population, applied to another):** the employment report: private service-providing hours grew 2.0% at an annual rate this quarter and all private hours 1.3%, as factories cut shifts; in every pilot quarter the two grew within 0.1 point of each other |
| 1 | Services extrapolated with private service-providing hours, as the handbook's "industries that provide them" reads | 2.5%, +1.5 pts | Every line follows its own source as the handbook lists it, and every line outside the report reproduces in every pilot quarter | The pilot log: the report's three lines missed the print in four of sixteen quarters, by up to 1.8 points on the headline |
| 2 | Each line's mean pilot miss added as an add-factor | 2.7%, +1.7 pts | The desk's standard bias correction, built on its own record, and it cuts the pilot's RMS miss from 0.59 to 0.56 points | The pilot log line by line: each report line's miss is zero in twelve quarters and one third of its month-3 change in the other four, all three lines in the same quarters, so no per-line constant reproduces any of them |
| 3 | **Decisive:** the report's three lines carried from month 2 whenever it lands fewer than four business days before the print, the freeze recovered by reproduction from the pilot log and the calendar | **1.0%** | — | — |

* **Figure shape.** Every lower correction raises the call (2.1%, 2.5%, 2.7%), and the decisive rung reverses them by 1.5 points: the
  print carries the report's three lines from month 2, so this quarter's month-3 fall in imports, net of the end of the inventory build,
  never reaches it.
* **Partial correction priced (L3).** A solver who finds the freeze but fills month 3 with the average of months 1 and 2 gets 0.6% (−0.4
  points), and with the month-1-to-2 trend 1.7% (+0.7). Carrying imports alone, with the report's inventories and exports as published,
  gives −0.3%. Keeping the add-factors on top of the freeze counts the pilot's misses twice: 1.2% (+0.2).
* **Grid.** Services indicator (all private hours, service-providing hours) × the report's lines (as published, add-factored, shrunk by the
  pilot's per-line regression, carried under the freeze) gives 8 cells: 2.1%, 2.3%, 1.4% and 0.6% on all private hours; 2.5%, 2.7%, 1.8%
  and the answer on service-providing hours. The nearest wrong cells are 1.4% (+0.36 points, two omissions) and 0.6% (−0.39 points, the
  services indicator alone); every other cell is at least 36% from the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The handbook lists each line's source and says the advance estimate rests on "source data that are incomplete or
   subject to revision". The calendar lists dates. No document says the agency freezes its inputs four business days before the print,
   that a report missing the freeze is replaced by its month 2, or that three lines move together.
2. **The reproduction numbers.** The four-business-day freeze, with the report's three lines carried from month 2, reproduces 128 of 128
   line contributions in the pilot to the published hundredth. A three-day freeze reproduces 122, a five-day freeze 122, the freeze with
   month 3 at the average of months 1 and 2 116, the release-date rule 116 and per-line add-factors 80. The rule is a construction:
   business days between two releases counted on the holiday calendar, lines grouped by the release that feeds them through the
   handbook's source table, and each line's month 2 from the archive. The freeze means nothing outside that grouping, and no per-line
   sweep reaches it.
3. **No arithmetic symptom.** Each filed line ties to its source release, the lines add to the filed call, and the print's lines add to
   its headline under every rung. The pilot's misses are forecast errors, not breaks in any total.
4. **Not a row predicate.** The carry replaces month 3 in three lines at once with each line's own month 2, and whether it applies depends
   on the business days between two releases. No row of this quarter's data marks it.
5. **The enumeration is arithmetic.** Which lines carry and by how much is computed from the source table and the archive: imports
   $166.7bn higher at an annual rate, inventories $80bn higher, exports $3.3bn lower. No column says "assumed".
6. **No cutover date.** The freeze applied in every quarter of the record, and the report landed anywhere from one to eight business days
   before the print; no series steps. The outage that delayed this quarter's report is a dated event and the decoy: it explains the date,
   not the print.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The pilot log: sixteen quarters of the desk's tracking pilot, each quarter's filed call and every line's monthly inputs as held
  at filing, beside the advance print line by line, with the release calendar and the source archive behind it.
* **What it pins (Pattern B).** The freeze, the carry from month 2 and the report's three lines, as above. Its headline record certifies
  the tracking at 0.59 points RMS with twelve exact quarters, which is why rungs 0–2 feel confirmed. Both services indicators reproduce the
  services contribution in all sixteen quarters, because goods-producing and service-providing hours never grew more than 0.1 point apart.
* **Free training instance (O3).** Construction spending for month 3 is never out at the print, and every print in the log carries
  structures from month 2, as the memo does. The carry is visible every quarter and harmless there.
* **Twin pair.** Pilot quarters 5 and 11 are identical on every column the log and the calendar carry: the same filed lines and filed call
  (1.2%), the same month-3 changes (imports +$300bn, inventories +$60bn, exports +$25bn at an annual rate), and the report published on a
  Wednesday six calendar days before a Tuesday print. The prints were 1.2% and 2.4% (2.0×), because quarter 11's six days held a Monday
  holiday: three business days, after the freeze. The release-date rule gives both 1.2%; only the freeze on business days reproduces both.
* **Resemblance points at the decoy.** This quarter's month-3 import fall most resembles pilot quarter 7's ($420bn after a front-loaded
  month 2), which the tracking hit exactly, because that report landed six business days before the print.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The research memo: each line rebuilt from the source the handbook lists for it, every source at its latest values at
  filing, consumer services extrapolated with total private hours plus 0.2% a quarter, structures' month 3 carried from month 2. The
  handbook: the source table; consumer services extrapolated with "labour input in the industries that provide them"; the advance estimate
  rests on "source data that are incomplete or subject to revision". The client-publication policy: one call at 18:00 on the business day
  before the print, at an annual rate, to one decimal.
* **Empirical pins.** The freeze, the carry and the report's three lines, from the pilot log, the calendar and the archive. The services
  productivity term, from the pilot log. Hours by supersector, from the employment report.
* **Voices.** The head of rates strategy: "Once the trade numbers are out, the print is arithmetic." The senior economist: "The fall in
  imports is the story of this print. The market will see a strong number."
* **Licensed wrong basis.** The memo records that the bank's model-validation unit scores the desk's calls against the agency's latest
  estimate of each quarter, not the advance print, and will present the desk's record on that basis.

## 8. Determinism by construction

* **Freeze.** This quarter's report landed two business days before the print, outside any freeze from three to eight days, and the log
  pins four: two reports at three days were out and two at four days were in.
* **Carry.** In each of the four late pilot quarters every report line's months 1 and 2 differ by at least $20bn at an annual rate and its
  month 3 differs from month 2 by at least $10bn, so the carry is the only fill that reproduces them. Each line's month 2 comes from the
  previous month's full trade release, out three weeks before the freeze, and nothing revises it before the print.
* **Business days.** Counted on the federal holiday calendar shipped with the release calendar, from the day after the report to the
  print day inclusive.
* **Services.** Private service-providing hours, the employment report's supersector series. The report is out three weeks before the
  print, and its next revision comes after it.
* **Structures.** Carried from month 2 under every rung and grid cell.
* **Rounding.** The call is 1.005 before rounding, 0.045 points from the nearer boundary.
* **Maturity.** An advance print never changes once published, and the archive holds every vintage of every source.

## 9. Prompt sketch and deliverables

> Clients get our call on the advance GDP print at six the evening before it comes out, and this quarter's goes out on Tuesday. I need one
> number: real growth at an annual rate, to one decimal. Our senior economist says the fall in imports is the story of this print. Send me
> `print_call.xlsx`, a chart `print_bridge.svg`, and a one-page `client_flash.docx` that commits to the figure.

* `print_call.xlsx` — the call by line under each construction, the short-time sheet (ask A) and the survey sheet (ask B).
* `print_bridge.svg` — a bridge from the desk's filing-day tracking to the call, one bar per line with the report's three carried lines
  picked out; an inset of the pilot's sixteen quarters, report-line misses against business days from the report to the print, with the
  freeze marked; this quarter's report placed on the inset; and the committed call labelled.
* `client_flash.docx` — the committed call, the three lines the print will carry from month 2, and the basis the validation unit uses.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month of the quarter, the manufacturing workers on approved short-time plans and the
  number of plans. *Device:* the state short-time file lists an employer plan once for every week it is active, under one plan ID with its
  enrolled workers repeated, as the file guide states. Summing rows counts each plan four or five times a month.
* **Ask B (device-carried).** For each pilot quarter, the market survey's median call for the advance print and the print's surprise
  against it. *Device:* the survey file keeps every submission with its time stamp, and the survey's rules take each forecaster's last
  submission before the close. A median over every row counts revisers twice and moves the median in five quarters.
* **Ask C (validity).** The call under each of the four rung constructions, with each one's reproduction count over the pilot's 128 line
  contributions.
* **Decoupling.** Replacing the freeze with the release-date rule changes no figure in asks A or B.

## 11. Rubric arithmetic

3 months × 2 (ask A) + 16 quarters × 2 (ask B) + 4 constructions × 2 (ask C) + the committed call, the report's position against the
freeze and the three carried lines + 5 named chart parts + 3 files ≈ 59 criteria.

## 12. World-building constraints

* Last quarter ($bn at an annual rate, fixed-base so lines add): consumer goods 5,500; services 12,800; equipment 1,600; structures
  1,700; government 4,100; inventories 60 (manufacturing 20, wholesale and retail 40); exports 1,800; imports 3,560; GDP 24,000.
* This quarter by month: consumer goods 5,545 / 5,555 / 5,565; equipment 1,620 / 1,625 / 1,630; government 4,110 / 4,114 / 4,118;
  manufacturing inventories 30 each month; structures 1,702 / 1,706 / carried; wholesale and retail inventories 0 / 240 / 0; exports
  1,815 / 1,825 / 1,835; imports 3,760 / 3,880 / 3,380. Services: last quarter × (1 + hours growth) × 1.002; service-providing hours
  +0.50% on the quarter, all private hours +0.32% (goods-producing −0.70%).
* Rungs 2.13 / 2.53 / 2.72 / 1.005. Grid cells on all private hours 2.33, 1.37 and 0.62; the regression cell on service-providing hours
  1.76. Partials 0.64 (average fill), 1.73 (trend fill), −0.28 (imports only), 1.20 (add-factors kept).
* Pilot: the report landed 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7 and 8 business days before the print in the twelve exact quarters, and 3, 3, 2
  and 1 in the four late ones. Late quarters' month-3 changes (imports, inventories, exports): +300/+60/+25, +420/+70/+30, −150/−30/−10,
  +180/+40/+15; headline misses +1.21, +1.81, −0.62, +0.70; add-factors −15.6, −2.9 and −1.25 ($bn). Per-line regression slopes 0.58,
  0.66 and 0.48.
* Quarters 5 and 11 are identical on every column of the log and the calendar; quarter 11's six calendar days hold a Monday holiday.
* Short-time plans and survey submissions never touch the source releases, the pilot log's lines or the calendar.
