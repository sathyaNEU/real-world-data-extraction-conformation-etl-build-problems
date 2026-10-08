# FC34 — How many first-time employers start running payroll with us in 2027, when the cohort rates that match every closed quarter were fitted before three states opened one-stop filing portals

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · business formation and small-business markets |
| Mirrors | Sizing a small-business acquisition plan from formation data after the filing channel changes (payroll and accounting platforms planning on business-application statistics, payments and commerce platforms planning on new-merchant applications), where conversion rates fitted on closed cohorts predate the channel |
| Decision shape | One figure committed at a date: the first-time-employer customer count the 2027 sales plan is built on |
| Committed call | New first-time-employer payroll customers in the twelve core states in calendar 2027, to the nearest 100 |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · validated on one population, applied to another (measured #13), with an implicit join (measured #18) at rung 2 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #18 joins only on the visible key · #25 assumes an effect the log could measure |
| Calibration form | Change-log natural experiments: the research team's log of five earlier one-stop portal launches in other states, each with applications and eight-quarter formations before and after |
| Driving force | The published cohort rates turn applications into employer formations and reproduce every closed quarter in the core states exactly, because every closed cohort predates the portals. In three core states a one-stop portal now takes 61% of applications, and portal applicants who are going to hire do so in the first two quarters, just as before, while the rest never do. Each of the five earlier launches shows the same thing: the eight-quarter rate for portal applications falls to 0.35 of the pre-launch rate, with the whole shortfall in quarters three to eight. The core states' portal cohorts have only reached quarter two, so nothing observed yet shows it. |

## 1. Situation

A payroll software company sizes its 2027 sales plan on first-time employers in its twelve core states: businesses whose first-ever
payroll run falls in the year and runs with the company. The pack holds the published business-application and formation statistics by
state, with cohort formation rates for high-propensity and other applications; each state's registration statistics, which split filings
by channel; the company's 2025 customer list; a firmographic vendor's file of business identifiers; and the research team's change log of
state registration reforms. Applications in the core states rose 26% over the last six quarters. The plan is signed off on Friday.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: application counts, cohort rates, channel splits, the customer list, the vendor file and the change
  log. The cohort rates reproduce every closed quarter exactly, and the head of growth is right that applications surged. No reported
  number is overturned; the difficulty is that next year's formations come from cohorts unlike any the rates were fitted on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of growth's view and every voice. The lag convolution on the published rates still reproduces every
  closed quarter and still carries the surge into 2027 at full value.
* **Instrument repair.** Imagine formation statistics published by filing channel. The portal cohorts' quarters three to eight have still
  not happened, so their conversion still has to be measured from the earlier launches.
* **Lens swap.** The naive read and the answer convert different populations: pre-portal cohorts, on which the rates were fitted, against
  portal-era cohorts in three states, which the rates were never fitted on.

## 3. The driving force

A strong solver convolves the last eight quarters of applications with the published lag weights for each propensity class, reproduces
every closed quarter in the core states to the formation, then applies the company's win rate. It also catches the identifier problem:
some "new" customers are existing ones whose business converted its entity type and received a new identifier. Every step is correct, and
the result carries the application surge into 2027. The surge is a channel. Three core states opened one-stop portals in the last eighteen
months, and 61% of their applications now come through them. A portal applicant who means to hire does so within two quarters, exactly as
before; many portal applicants were never going to hire at all. The five earlier launches in the change log each show applications up a
third or more and eight-quarter formations up only 5–8%: the portal channel's eight-quarter rate is 0.35 of the pre-launch rate, and all of
the gap opens after quarter two. The core states' portal cohorts are at quarter one or two, where they convert normally.

## 4. The ladder

| Rung | Construction | Lands on (2027 customers) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Latest quarter's applications × the eight-quarter rate × four quarters × the 2025 win rate matched on identifier | 9,200 (+56%) | The quickest reading of the published rates | The published cohort rates spread formations over eight quarters, so next year's come mostly from applications filed one to six quarters ago |
| 1 | Lag convolution by propensity class on the published cohort rates, × the identifier-matched win rate (12.6%) | 7,740 (+31%) | Reproduces every closed core-state quarter exactly; the textbook method on the official statistics | The vendor file: 11% of 2025 "first-time" customers carry a predecessor identifier from a business that already ran payroll with the company |
| 2 | Win rate recalibrated through the predecessor link (11.2%) | 6,880 (+16.7%) | Every customer linked to its business across entity conversions; the calibration now counts only genuine first-time employers | The registration statistics: portals now take 61% of applications in three core states, and the cohort rates were fitted on cohorts that predate every portal |
| 3 | **Decisive:** portal-channel applications converted at the rate the change log measures (unchanged in quarters one and two, 0.35 of the pre-launch eight-quarter rate overall) | **5,900** | — | — |

* **Figure shape.** Every correction walks the figure down and the decisive rung is the largest step after rung 0, so the answer is the
  minimum cell and every partial build over-plans. Rungs 0–2 sit 56%, 31% and 16.7% above it.
* **Partial correction priced (L3).** A solver who suspects the portals but measures their effect from the core states' own portal
  cohorts sees no shortfall, because those cohorts have only reached quarter two, and stays at 6,880. One who treats portal applications
  like the "other" propensity class lands at 6,880 too: the portals pre-fill the hiring-intent question, so 70% of portal applications are
  classed high-propensity. One who applies the measured effect to non-high-propensity portal applications only lands at 6,680 (+13.2%), because the shortfall falls
  mostly on portal applications classed high-propensity.
* **Grid.** Conversion (single period, lag convolution) × win-rate link (identifier, predecessor) × channel (pooled, propensity proxy,
  measured portal effect) = 12 cells. Every wrong cell sits at least 12% above 5,900. The nearest is the measured portal effect with the
  identifier-matched win rate (6,640, +12.5%), which counts converted businesses as new employers.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The change log records launch dates and before-and-after counts. No document states a conversion rate for portal
   applications or says the published rates predate the portals.
2. **Corpus blind for the core states.** *In every closed core-state cohort the portal share is zero, because the first core-state portal
   opened in the second quarter of 2025, after the last cohort that has completed eight quarters;* and in every observed quarter of the
   portal-era cohorts, formations match the published rates, because those cohorts have only reached quarters one and two. Only the five
   earlier launches, run to eight quarters elsewhere, carry the effect.
3. **No arithmetic symptom.** Applications reconcile to the registration statistics, formations to the published cohorts, customers to
   the billing system, and every closed quarter ties.
4. **Not a row predicate.** The effect is a lag-specific conversion recovered from before-and-after cohorts across five launches, applied
   by channel to each state's open cohorts and convolved forward.
5. **The enumeration is arithmetic.** Which 2027 formations come from portal applications, and how many, is computed; no column marks a
   formation by channel.
6. **No cutover date in the decisive cause.** The launches are dated and step the application series, and that step is loud in the wrong
   direction: it reads as growth. The shortfall opens in each cohort's own third quarter, so no outcome series in the core states has
   stepped yet.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The change log of five earlier one-stop portal launches in non-core states (2019–2023): each state's quarterly applications by
  channel and propensity class, and their formations at every lag up to eight quarters, before and after launch.
* **What it certifies.** That launches raise applications (by 30–45% within two quarters) while formations in quarters one and two per
  application are unchanged, which is what the core states' early portal cohorts show.
* **What it pins.** The portal channel's eight-quarter rate at 0.33–0.37 of the pre-launch rate in all five launches, with the shortfall
  entirely in quarters three to eight; the same within each propensity class.
* **Twin pair.** Core states R4 and R9 (the plan's region codes) are identical on every published application and cohort-rate column for
  the last six quarters. Their forecast 2027 formations differ 1.9×, because 61% of R4's applications came through its new portal and none
  of R9's, which only the registry's channel split reveals.
* **Resemblance points at the decoy.** By application growth and propensity mix, the core states' surge most resembles the 2021 national
  boom, whose cohorts converted at the published rates.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The plan template: the plan is sized on businesses in the twelve core states whose first-ever payroll run falls in 2027
  and runs with the company. The planning convention holds future quarters' applications at the trailing four-quarter level, by state,
  class and channel. The published cohort rates are the official statistics.
* **Empirical pins.** The portal effect by lag, from the change log. The win rate (11.2%), from 2025 customers linked through predecessor
  identifiers.
* **Voices.** The head of growth: "This application surge is the best news we've had in years." The vendor's account manager: "Every
  customer identifier matches an application; the match is clean." The company economist: "The official cohort rates have matched every
  closed quarter. They're the gold standard."
* **Licensed wrong basis.** The plan template records that the board's growth committee sizes the market on published high-propensity
  applications at the published cohort rates and will review the plan on that basis.

## 8. Determinism by construction

* **Portal effect.** Across the five launches the eight-quarter ratio runs 0.33–0.37; using any of them moves the committed figure by less
  than 1%, inside its 100-customer bin.
* **Lag shape.** In every launch the first two quarters' conversion is unchanged to within 2%, so early-lag readings converge.
* **Future applications.** The planning convention pins 2027 applications; a solver who instead trends them lands within 40 customers.
* **Win rate.** The predecessor-linked win rate is 11.1–11.3% in each of 2023, 2024 and 2025, so the calibration year does not matter.
* **Rounding.** The figure sits mid-bin at the nearest 100.

## 9. Prompt sketch and deliverables

> The 2027 sales plan is built on how many first-time employers in our twelve core states start running payroll with us next year, and I
> sign it off on Friday. Our head of growth thinks the surge in business applications is the best news we've had in years. Give me that
> number to the nearest 100, in a line for the plan, and send `new_employer_plan.xlsx` with the build and the sheets below, a chart
> `formation_bridge.png`, and a one-page `plan_note.pdf`.

* `new_employer_plan.xlsx` — the forecast by state, channel and lag, the first-payroll sheet (ask A) and the retention sheet (ask B).
* `formation_bridge.png` — a waterfall from the single-period figure to the committed figure: lag convolution, predecessor link and portal
  conversion as labelled steps with their sizes, the three portal states' share of the last step shown as a split bar, and the committed
  figure annotated.
* `plan_note.pdf` — the committed figure and why the official rates do not carry the surge.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twelve states and each quarter of 2025, the median employees on a new customer's
  first full payroll. *Device:* a customer's first run is often a test or off-cycle bonus run, flagged in the run-type table, as the
  payroll guide documents; reading the first run understates headcount at every state. Headcount enters no part of the customer forecast.
* **Ask B (device-carried).** For each state, the share of 2025 new customers still running payroll twelve months on. *Device:* seasonal
  businesses pause payroll and are marked inactive, then reactivate, as the account guide documents; counting the pause as churn
  understates retention at the five states with tourism-heavy books.
* **Ask C (validity).** The 2027 figure under each of the four rung constructions, and how many closed core-state quarters each
  reproduces.
* **Decoupling.** Clearing the portal effect changes no figure in asks A or B.

## 11. Rubric arithmetic

12 states × 4 quarters (ask A) + 12 states (ask B) + 4 constructions × 2 (ask C) + the committed figure, 2027 formations and the win rate
+ 5 named chart parts + 3 files ≈ 79 criteria.

## 12. World-building constraints

* Three core states with portals (opened 2025Q2, 2025Q4, 2026Q1), now taking 61% of their applications; 70% of portal applications are
  classed high-propensity. Portal applications supply 22% of 2027 formations under rung 2's construction.
* Figures: 9,200 / 7,740 / 6,880 / 5,900; identifier-matched win rate with the portal effect 6,640; portal effect on non-high-propensity
  applications only 6,680.
* Win rates: 12.6% on identifier, 11.2% through the predecessor link; 11% of identifier-matched 2025 first-time customers are converted
  businesses.
* Change log: five launches, eight-quarter ratio 0.33–0.37, quarters one and two unchanged.
* The twin states are identical on every published column for six quarters.
* Test runs and seasonal pauses touch no customer counted as a 2025 first-time employer.
