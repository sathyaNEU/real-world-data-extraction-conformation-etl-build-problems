# FC20 — How many recordable injuries the twenty ergonomics-programme sites will have next year, when nine of them start shifts staffed by new hires

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · warehouse safety programmes |
| Mirrors | Forecasting injuries or incidents for a workforce whose newest members have not yet reached the tenure window where the harm surfaces (Amazon fulfilment safety programmes when a building adds a shift, UPS and FedEx hub staffing, Walmart distribution centres hiring a new cohort, content-moderation teams onboarding a new vendor cohort) |
| Decision shape | One figure committed at a date: the forecast the ergonomics vendor's contract is priced on |
| Committed call | Recordable injuries at the twenty programme sites next year, to the nearest 50 |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · maturity: next year's injuries on the new shifts crystallise as 6,000 new associates pass through the tenure months where strain injuries surface, computable only from the HR roster, with a suppressed benchmark cell bounded below |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Gold-standard verification subsample: an independent occupational-health audit of 1,200 recordable cases from the last three years, each verified against clinic records and linked to the injured associate's HR record |
| Driving force | Site rates times planned hours reproduce every closed year, because the operator always grew by rehiring returning seasonal associates and each site's rate carried the same small new-hire share. In January nine of the twenty programme sites start second shifts staffed by 6,000 associates hired in December, all new to warehouse work. Verified cases put strain injuries in tenure months four to nine at 2.6× the tenured rate, and this cohort will pass through that window inside next year. Its hours by tenure come only from the HR roster's production-start dates. |

## 1. Situation

A logistics operator runs an ergonomics programme (lift assists, job rotation, coaching) at twenty fulfilment sites next year, chosen
for their planned growth. The vendor prices the programme per forecast recordable injury, and the contract is signed on the 15th. The
safety analytics memo forecasts each site as planned hours times the expected recordable rate for those hours, shrunk empirically toward
the state injury survey's rate for the site's industry and size class. All twenty sites employ more than 1,000 people, and the survey
suppresses that size class's rate.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the sites' injury logs and annual hours, the state survey table, the labour plan, the HR roster
  and the audited cases. No one's claim about their own numbers is overturned. The difficulty is who will work next year's new hours,
  and where each of them will be in their first year.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the insurer's basis. Shrinkage toward the bounded benchmark times planned hours still says
  1,837, and every closed year still confirms the method.
* **Instrument repair.** Record every injury and hour perfectly. The second shifts have not worked a day, and their injuries depend on
  where each associate will be in tenure next year, which no record of the past holds.
* **Lens swap.** The naive read and the answer differ in population and moment: hours worked by a steady tenure mix against hours worked
  by a cohort moving through its first year.

## 3. The driving force

A strong solver follows the memo's shrinkage, bounds the suppressed size-class rate from the survey's published total and other classes,
and multiplies by planned hours. That reproduces every closed site-year within 3%, because every closed year had the same workforce
shape: new associates were 7–9% of hours, mostly returning seasonal associates in their first weeks. Next year is different in who
works the hours. Nine sites start second shifts on 5 January with 6,000 associates hired in December, all new to warehouse work and in
training at the extract. The audited cases, linked to HR tenure, show injury risk by tenure month: 1.6× the tenured rate in the first
three months, 2.6× in months four to nine, when strain injuries surface, and 1.3× to the end of the first year. The site rate prices
those hours as if they were worked by the usual mix. The cohort's hours by tenure band come from the roster's production-start dates and
HR's replacement rule, and nothing the forecast normally reads contains them.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each site's two-year recordable rate × next year's planned hours | 1,633, −24% | The operations team's own rates on the labour plan's hours | The memo: each site's rate is shrunk toward the state survey's rate for its industry and size class |
| 1 | Empirical-Bayes shrinkage, with the suppressed 1,000+ class read as unknown and the industry total (5.4) used instead | 1,664, −22% | The filed method, with the only published rate that fits | **E25 (a suppressed cell, bounded):** the survey publishes case counts and hours for the total and the other three classes, which fix the suppressed class at 6.45–6.55 |
| 2 | Shrinkage toward the bounded large-site rate (6.5) × planned hours | 1,837, −14% | Every published figure used, the hidden one bounded, every closed site-year reproduced within 3% | The HR roster: the second shifts' 6,000 associates were hired in December, new to warehouse work, and start production on 5 January |
| 3 | **Decisive:** existing hours at the shrunk site rate; second-shift hours split by tenure band (roster production-start dates and HR's replacement rule), each at the audited tenure hazard on the site's tenured rate | **2,138 → 2,150** | — | — |

* **Figure shape.** Every correction moves the figure up (−24%, −22%, −14%), and the answer is the largest cell of the grid, so a solver
  who stops anywhere short under-prices the programme.
* **Partial correction priced (L3).** Applying the network's historical new-hire multiplier (1.3×, from first-year associates who were
  mostly short-stay seasonals) to the second shifts gives 1,921 (−10.1%). Raising only their first three months (1.6×) gives 1,878
  (−12.1%), because most of the cohort's excess falls in months four to nine.
* **Grid.** Benchmark (none, industry total, bounded cell) × second-shift rate (site rate, historical new-hire multiplier, first-three-
  months uplift, tenure path) gives 12 cells, all below the answer. The nearest is the tenure path on the industry-total benchmark, 1,937
  (−9.4%), which has the decisive insight and misses the bound.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo says "the expected rate for those hours" and files the shrinkage. No document says new hires carry a
   different rate, when strain injuries surface, or that the second shifts are new to the work; the roster ships for the hours ask.
2. **Corpus blind for a computable reason.** *In every closed year new associates worked 7–9% of each site's hours, mostly returning
   seasonal associates in their first weeks, because the operator staffed growth through peak-season rehiring.* Every site's rate carried
   the same new-hire share, so planned hours times site rate reproduce every closed site-year within 3%.
3. **No arithmetic symptom.** Cases tie to the logs, hours to the annual summaries, and the bounded cell to the survey's totals. Next
   year's hours tie to the labour plan under every rung.
4. **Not a row predicate.** No case or site is filtered. The second shifts' hours are spread over tenure bands by each associate's
   production-start date and the replacement rule, and priced through a hazard estimated on verified cases joined to HR records.
5. **The enumeration is arithmetic.** Which hours fall in months four to nine of tenure next year is computed from dates. No column holds
   it.
6. **No cutover date.** The hiring is dated, but no outcome series has stepped: the cohort has worked no production hours, and its
   injuries exist only in the forward year.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The audit: 1,200 recordable cases from the last three years, each verified against clinic records for recordability, onset
  and diagnosis, and linked to the associate's HR record (production-start date, prior warehouse tenure, path and shift).
* **What it certifies.** The site logs' recordable counts (98% of cases confirmed), and, with HR hours by tenure, the hazard by tenure
  band: 1.6×, 2.6× and 1.3× the tenured rate in months one to three, four to nine and ten to twelve. A back-tester is confirmed at rung 2.
* **What it cannot show.** A site-year with a large cohort of new permanent hires (above).
* **Twin pair.** At site S-118 in the audit's second year, 410 pack associates hired that spring as permanent staff and 410 tenured pack
  associates on the same shift are identical on every column the site log carries: site, path, shift, hours and age band. Their verified
  recordables over the year were 52 and 26 (2.0×). The site rate gives both 26; only tenure from the HR join reproduces both.
* **Resemblance points at the decoy.** The nine second-shift sites resemble the sites that added hours by peak-season rehiring in past
  years, whose injuries rose exactly in proportion to hours.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme charter: the vendor's fee is priced per forecast recordable injury at the twenty sites next year. The
  memo: planned hours times the expected recordable rate for those hours, with Poisson–gamma shrinkage toward the state survey's rate for
  the site's industry and size class. The labour plan: next year's hours by site and shift. HR's staffing rule: a second-shift leaver is
  replaced within the week by a new hire.
* **Empirical pins.** The tenure hazard, from the audit. The cohort's tenure bands, from the roster. The suppressed rate's bound, from the
  survey's published counts and hours.
* **Voices.** The safety director: "Injury rates follow the building, not who works in it." The operations vice-president: "We add hours
  every year and the rate never moves."
* **Licensed wrong basis.** The charter records that the operator's insurer prices its programme credit on the survey's industry rate
  times planned hours, and will present that figure at renewal.

## 8. Determinism by construction

* **Bound.** The survey publishes case counts to the nearest 10 and hours to the nearest 0.1 million, so the suppressed class sits at
  6.45–6.55, and every value in that range gives a forecast that rounds to 2,150.
* **Tenure.** The audit measures tenure from production start, excluding training weeks, as the roster does. With HR's replacement rule
  and retention curve, the second shifts' hours fall 27% in months one to three, 48% in months four to nine and 25% in months ten to
  twelve.
* **Tenured rate.** Each site's shrunk rate carries the closed years' 9% new-hire share at the historical 1.3× multiplier, and the tenured
  rate is that rate divided by 1.027.
* **Shrinkage.** The memo's prior variance comes from the network's sites by method of moments, and the twenty sites' weights average
  one half; no other convention is filed.
* **Maturity.** Every audited case is closed, and every closed year's log is complete.

## 9. Prompt sketch and deliverables

> Our ergonomics vendor prices next year's programme at the twenty sites per forecast recordable injury, and I sign the contract on the
> 15th. Our safety director says injury rates follow the building, not who works in it. Give me the forecast to the nearest fifty, and
> send `programme_forecast.xlsx`, a chart `site_injury_build.png`, and a one-page `contract_basis.pdf`.

* `programme_forecast.xlsx` — the forecast by site and shift under each construction, the case-status sheet (ask A) and the hours sheet
  (ask B).
* `site_injury_build.png` — the twenty sites' forecast injuries as stacked bars (existing hours, second-shift hours by tenure band), the
  planned-hours forecast as a marker on each bar, an inset of the tenure hazard, and an inset of the survey's size classes with the
  suppressed rate's bound shaded.
* `contract_basis.pdf` — the committed forecast, the second shifts' share of it, and the insurer's basis.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the twenty sites, last year's cases with days away, restriction or transfer, and
  their rate per 200,000 hours. *Device:* a case that moves from restricted duty to days away keeps one case number and gains a second
  status row in the case system, and the recordkeeping rule counts it once, as days away. Counting status rows double-counts eleven such
  cases across six sites.
* **Ask B (device-carried).** For each of the nine second-shift sites, last year's average weekly hours per associate and the overtime
  share. *Device:* a timecard corrected after payroll close posts as a reversal and a replacement row carrying the original timecard ID.
  Summing every row double-counts corrected hours at three sites. The forecast's hours come from the annual summaries and the labour plan,
  never from timecards.
* **Ask C (validity).** The forecast under each of the four rung constructions, with each one's fit to the audited cases by tenure band.
* **Decoupling.** Replacing the tenure path with the site rate changes no figure in asks A or B.

## 11. Rubric arithmetic

20 sites × 2 (ask A) + 9 sites × 2 (ask B) + 4 constructions × 2 (ask C) + the committed forecast, the second shifts' injuries and the
bounded rate + 5 named chart parts + 3 files ≈ 77 criteria.

## 12. World-building constraints

* Next year's hours: 52.0 million existing and 10.8 million on the second shifts (6,000 positions). Raw two-year rate 5.2; industry
  total 5.4; suppressed 1,000+ class 6.5 (published classes 3.9, 4.9 and 5.4 on 30, 80 and 110 million hours; the class itself 80
  million hours).
* Forecasts: 1,633 / 1,664 / 1,837 / 2,138; partial cells 1,921 and 1,878; the nearest grid cell 1,937. Every cell sits below the answer.
* Tenure hazard 1.6× / 2.6× / 1.3× in months 1–3 / 4–9 / 10–12; the cohort's hours 27% / 48% / 25%; historical new-hire multiplier 1.3×.
* S-118's two groups are identical on every site-log column. Closed site-years reproduce within 3% under rung 2.
* Status changes and corrected timecards never touch the annual summaries, the roster or the audited cases.
