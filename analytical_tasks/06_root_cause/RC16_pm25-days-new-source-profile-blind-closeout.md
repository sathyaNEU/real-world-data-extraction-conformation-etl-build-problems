# RC16 — How the air district should classify this summer's eleven bad-air days, when last year's certified method has never met a dust source

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · air quality regulation and enforcement |
| Mirrors | Attributing an incident cluster between a known external shock and a new internal source (a site-wide latency spike from an upstream provider against a newly deployed service at Google or Meta, a sales drop from a market-wide event against one new store), when the attribution method was certified before the new source existed |
| Decision shape | A structure the body adopts: the classification of the summer's exceedance days that the district files, from which the referral follows |
| Committed call | The number of exceedance days in each class (smoke, local, mixed), and the referral that the local count triggers |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · L1 with S4 (the close-out certifies the shallow rungs and is blind to the decisive one: no closed summer had a crustal source), with E17 (validated on one population, applied to another) at rung 1 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #4 never tests its reading against the control · #15 follows the requester's hunch over the rule |
| Calibration form | Prior-period close-out: the federal agency's concurrence on last summer's exceptional-events demonstration, with the district's day-by-day mass-balance tables |
| Driving force | The district classifies each day by the source holding the majority of its fine-particle mass, from a chemical mass balance over source profiles. Last summer's certified profiles (smoke, secondary aerosol, traffic) reproduce every accepted day, because no crustal source then operated within 30 km. This summer's new quarry sends silica-rich dust downwind; with the certified profiles that mass falls into an unexplained residual and the days read as smoke or no-majority. The quarry's own source-test profile, in its permit file, turns five of them local. |

## 1. Situation

A county recorded eleven days above the 24-hour fine-particle standard this summer, against two last summer, after a large aggregate quarry opened
nearby. Residents have petitioned for enforcement; the quarry points to a severe wildfire season. The air district must file a classification of the
eleven days: smoke days go into its exceptional-events demonstration and are excluded from the county's attainment record, and three or more days
classed as local refer the quarry for an enforcement inspection. The district's procedure sets how a day is classed, and last summer's demonstration
was concurred with in full.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the monitors, the smoke-plume maps, the speciation analyses, last summer's certified profiles and mass
  balances, and the quarry's source test. The wildfire season was severe and the quarry's operator is right that smoke covered the state on
  most of these days. Nothing reported is overturned; the certified method meets a population it was never calibrated on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the petition, the operator's statement, the board chair's expectation and the licensed basis. The certified mass
  balance still files no local day.
* **Instrument repair.** Perfect speciation still measures the crustal mass, as it does now; the difficulty is the profile set the balance is
  solved against, which no better instrument supplies.
* **Lens swap.** The naive classes describe this summer's days as last summer's sources would explain them; the answer explains them with the
  source set this summer actually had, so the population of local days changes, not its label.

## 3. The driving force

A strong solver distrusts the plume map and the before-and-after comparison, applies the district's multi-line rule (smoke overhead, regional
uniformity, a fire or ratio line, a downwind gradient), and finds it reproduces every day accepted last summer. It goes further, because the
procedure classes a day by mass, not by evidence lines: it solves the chemical mass balance over the certified profiles, reproduces last summer's
accepted smoke shares exactly, and applies it to this summer. Smoke holds the majority on seven days and no source does on four; no day is local.
Every input is correct, and the method was certified on summers when no crustal source operated within 30 km. In every closed case the crustal
fraction on an exceedance day was under 3%, so the profile set never needed one. This summer silicon, aluminium and calcium appear on days the
wind blew from the quarry, and the certified balance parks them in the residual. The quarry's permit file holds its source-test profile. Added to
the balance, it takes the majority on five days and splits two more.

## 4. The ladder

| Rung | Construction | Files | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Smoke-plume map: a day with medium or heavy smoke over the county is smoke, otherwise local | 9 smoke, 2 local | The federal plume product, applied day by day | The close-out: plume-only classes reproduce 8 of last summer's 14 accepted days |
| 1 | The district's multi-line rule, which reproduces all 14 accepted days | 6 smoke, 3 mixed, 2 local | Validated on every closed day the agency accepted | The procedure classes by mass contribution; the rule's lines are surrogates, and on this summer's days they disagree with the speciation on four |
| 2 | Chemical mass balance over the certified profiles, majority source above regional background | 7 smoke, 4 with no majority source, 0 local | The procedure's own measure, with the profiles the agency concurred with, reproducing last summer's shares exactly | The quarry's source-test profile: the four no-majority days and three smoke days carry its silica signature in the residual |
| 3 | **Decisive:** the same balance with the quarry's profile added | **4 smoke, 5 local, 2 mixed: referral** | — | — |

* **Structure table.** The answer's local class holds 2, 2 and 0 days on rungs 0–2 and 5 on rung 3; every partition sums to eleven days, and
  only the decisive one crosses the referral line of three.
* **Discriminator dominance.** Smoke carries a 1.75× lead into rung 3 (7 days against 4 with no majority, local at 0). The quarry profile
  takes 41% of the mass above background on downwind days and moves three smoke days and two no-majority days to local: local then leads smoke
  5 to 4 (1.25×) and clears the referral line of 3 by two days, so no single day's class decides the referral.
* **Partial correction priced (L3).** A solver who adds the quarry profile but solves the balance at the monitor nearest the quarry rather
  than at each day's maximum monitor, which the procedure classes, finds 2 local days, rung 1's count, and no referral. One who adds a generic
  crustal profile from the speciation guide instead of the quarry's source test splits the silica between road dust and the quarry and files
  3 smoke, 2 local and 6 mixed, again no referral.
* **Grid.** Classifier (plume, multi-line, mass balance) × profile set (certified, generic crustal, quarry source test) × monitor (nearest,
  daily maximum) gives seven feasible builds. Five file two local days or fewer; the quarry profile at the daily maximum files five.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The procedure says to class by majority mass from the speciation balance; the close-out lists the profiles used. No
   document says the profile set must change, and the quarry's source test sits in its permit file for an unrelated reason.
2. **Corpus blind for a computable reason.** *In every closed summer the crustal fraction on every exceedance day was under 3%, because no
   crustal source operated within 30 km, so the certified balance and a balance with any crustal profile return the same classes on every
   accepted day.* The close-out certifies the multi-line rule and the balance and cannot see the quarry.
3. **No arithmetic symptom.** The certified balance closes on this summer's days with a residual inside the range the close-out's own days
   showed, because the close-out's residuals were never tested against silica.
4. **Not a row predicate.** Each day's classes come from solving a mass balance across species against a source set, at the day's maximum
   monitor.
5. **The enumeration is arithmetic.** Which days are local is the output of eleven balances; no column flags dust.
6. **No cutover date.** The quarry's opening steps nothing that alignment can use: it fell in the same weeks the smoke season began, so the
   petition's before-and-after comparison credits the smoke to the quarry and is a decoy in the other direction (nine extra days).
7. **Survives deletion.** With every voice and the petition gone, the certified balance still files no local day.

## 6. The calibration corpus

* **Form.** The federal agency's concurrence on last summer's exceptional-events demonstration: the 14 exceedance days accepted, and for each
  the district's mass balance (species, profiles, contributions) and evidence lines.
* **What it certifies.** The multi-line rule (14 of 14), the certified profiles and the balance (every accepted day's smoke share reproduced
  within 0.5 µg/m³), and the majority rule for classing.
* **What it is blind to.** A crustal source (above).
* **Twin pair.** 14 July and 2 August had the same maximum (41 µg/m³), medium smoke overhead, uniformity 0.31, wind from the quarry's sector at
  the maximum monitor and the same fine-particle to nitrogen-dioxide ratio. Local mass was 17.2 and 8.4 µg/m³ (2.05×), and the days class as
  local and mixed: the quarry ran double shifts on 14 July. Only the balance with the quarry's profile separates them.
* **Resemblance points at the decoy.** Every one of this summer's eleven days matches an accepted smoke day of last summer on plume density,
  fire activity and uniformity.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The district's procedure: each exceedance day is classed by the source holding the majority of its fine-particle mass above
  regional background at the day's maximum monitor, from the speciation balance; a day with no majority source is mixed. The referral rule:
  three or more local days refer the source for inspection.
* **Empirical pins.** The balance and the certified profiles, from the close-out; the quarry's profile, from its source test.
* **Voices.** The quarry's environmental manager: "It was smoke. The whole state was under it for six weeks." The district's monitoring lead:
  "Our rule got every single day right last year."
* **Licensed wrong basis.** The procedure records that the quarry's consultant classes days by the smoke-plume map and will present that
  classification at the hearing.

## 8. Determinism by construction

* **Background.** Regional background is the five-day median at the upwind rural monitor, as the procedure fixes.
* **Balance.** Effective-variance solution over the filed species; every day's balance converges under every profile set.
* **Majority.** No day has a leading source within three points of 50% under the decisive balance.
* **Days.** The eleven days are fixed by the standard; every monitor reports at least 18 valid hours on each.
* **Rounding.** Day counts are whole; contributions to 0.1 µg/m³.

## 9. Prompt sketch and deliverables

> The district has to file how it classifies this summer's eleven bad-air days, and whatever we file decides whether the quarry is referred.
> The board chair expects the answer to be smoke. Tell me how many of the eleven days we class as smoke, local and mixed, and whether that refers
> the quarry, as the paragraph for the hearing brief. Send `exceedance_days.csv`, a chart `source_mass_by_day.png` and `hearing_brief.docx`.

* `exceedance_days.csv` — one row per day: evidence lines, species, the balance under each profile set, and the class.
* `source_mass_by_day.png` — stacked bars of each day's mass above background by source under the certified and the decisive balance, side by
  side, with the 50% majority line, the referral count annotated and 14 July and 2 August marked.
* `hearing_brief.docx` — the classification, the referral, and what the plume map and last year's rule miss.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the four ozone monitors, the summer's fourth-highest daily maximum 8-hour average.
  *Device:* 8-hour averages are labelled by their starting hour and the daily maximum takes only windows starting 07:00 to 23:00, as the
  data-handling appendix documents; labelling by ending hour or using all 24 windows moves the fourth-highest value at two monitors.
* **Ask B (device-carried).** For each month of operation, the quarry's reported production and operating hours. *Device:* its quarterly
  reports switch from short tons to metric tonnes in the second quarter, with a units field, as the permit's reporting form documents; summing
  across the switch overstates June by about 10%.
* **Ask C (validity).** For each of last summer's 14 accepted days, the class and smoke share each of the four constructions returns; and this
  summer's eleven classes under each construction.
* **Decoupling.** Clearing the quarry profile changes no figure in asks A or B.

## 11. Rubric arithmetic

4 monitors (ask A) + 4 months × 2 figures (ask B) + 14 days × 4 constructions + 11 days × 4 constructions (ask C) + the three class counts, the
referral and the quarry's share on the five local days + 5 named chart parts + 3 files ≈ 135 criteria.

## 12. World-building constraints

* Classes by rung: 9/0/2; 6/3/2; 7/4/0 (smoke / mixed or no majority / local); 4/2/5 at the decisive rung.
* Closed summers: crustal fraction under 3% on every exceedance day; the multi-line rule and the certified balance both reproduce 14 of 14.
* The quarry's profile takes 41% of the mass above background on downwind days; silicon, aluminium and calcium appear only on days with wind
  from its sector.
* 14 July and 2 August identical on every evidence-line column.
* Ozone windows and the quarry's tonnage units touch no fine-particle day or balance.
