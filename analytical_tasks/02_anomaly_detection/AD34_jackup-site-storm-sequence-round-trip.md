# AD34 — Which offshore site gets the winter jack-up, when the downtime is in storm sequences that no sea-state statistic counts

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · offshore construction marine operations |
| Mirrors | Placing one scarce recovery asset where disruptions arrive in back-to-back sequences faster than recovery takes (cloud capacity buffers where incidents chain faster than failover completes, fulfilment backup capacity at Amazon where carrier disruptions chain, airline spare aircraft where weather events come in bursts) |
| Decision shape | Which of N gets one scarce thing: the contractor's single jack-up installation vessel goes to one of five sites for the 120-day winter campaign |
| Committed call | The site that gets the jack-up, and the floating-vessel weather downtime it avoids over the campaign, in days |
| Gap · Pattern | Gap 2 (population: the disruption is a sequence, not a storm) over Gap 4 (rule) · every screen is right and the answer is what nothing flags (stand-down sequences whose calm gaps are shorter than the site's port round trip), with the flag-suggested event population below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #7 uses the ready-made measure · #5 takes the population a flag or filter suggests · #4 never tests its reading against the control |
| Calibration form | Counterparty acknowledgement file: the developer's acknowledgement of every day claimed in 12 past winter campaigns (weather standby, weather transit or working) |
| Driving force | A floating installation vessel loses time per sequence, not per storm. When two stand-downs are separated by a calm gap shorter than the round trip to the site's marshalling port plus remobilisation and a minimum working window, the gap is lost as well. S5's storms are moderate, but they arrive in pairs 45–51 hours apart and its port is 16 hours away, so almost every gap is lost. Seeing it means declustering stand-downs, joining each site's transit time from the port register and chaining gaps shorter than the round trip: a construction at a grain none of the five sea-state statistics expresses, and the only one that reproduces the developer's acknowledged downtime in all 12 past campaigns. |

## 1. Situation

An offshore wind contractor installs foundations at five sites this winter (1 November to 28 February). It has one jack-up vessel, which
stands on its legs through any storm in the record, and floating heavy-lift vessels for the other four sites, which shelter in their
marshalling port whenever a stand-down comes. The campaign plan puts the jack-up where it avoids the most floating-vessel weather
downtime. The planner's metocean monitor reports five statistics per site from eighteen winters of buoy data, each labelled as a statement
about past sea states. The contractor also holds the vessel register, the port register's transit times and the developer's
acknowledgement file from 12 past campaigns.

## 2. Gate G: why this is legal

* **Litmus.** Every statistic is correct and labelled for what it measures: return levels, storm counts, exceedance hours, longest storms
  and window availability. The planner is right that S1 has the roughest seas. Nothing is overturned; the difficulty is a population
  (stand-down sequences against port distance) the monitor's grain cannot express.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the planner's view and the monitor's export. A weather-window analysis built from the buoy data still names S3,
  and still misses S5.
* **Instrument repair.** Suspect file: the buoy series, whose documented missing codes leave hours blank. Fill them from the hindcast: no
  missing hour falls within 48 hours of a stand-down, so rung 0 still names S1, rung 1 S2 and rung 2 S3. Chaining stand-downs through gaps
  shorter than each site's round trip is still needed, since no wave record holds a vessel's transit; the vessel and port registers and the
  acknowledgement file are complete.
* **Lens swap.** The monitor's populations are storms and hours at a site; the answer's is chains of stand-downs and the gaps between them,
  weighed against a property of a different entity (the marshalling port). A different population, not one population under a new lens.

## 3. The driving force

A strong solver rejects the alert-level storms, rebuilds stand-downs at each vessel's crane limit for the site's depth, and runs the
industry's weather-window analysis: a day is lost when no 24-hour workable window is available. Every step is correct, and each treats a
calm gap of a day or more as usable. A floating vessel, though, is in port when the gap opens. It must sail out, remobilise, work at least a
shift and be clear before the next stand-down, so a gap counts only if it covers the round trip and remobilisation plus twelve hours of
work. That threshold is a property of the port, not the sea: 38 to 42 hours for four sites and 54 for S5, whose port is 16 hours away. S5's
stand-downs come in pairs 45 to 51 hours apart, usable at any other site and lost there. Chaining stand-downs through lost gaps, per site,
with each site's own round trip, is the construction.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Storms above the planner's alert level per winter × mean storm length (expected days lost): S1 31, S2 25, S3 22, S4 19, S5 15 | S1 | The planner's alert levels, set on eighteen winters | The vessel register: floating vessels stand down at a crane limit of 2.2–2.8 m for each site's depth, far below the alert level |
| 1 | Stand-downs at each vessel's limit for the site's depth, declustered, × mean duration: S2 41, S3 33, S1 30, S5 27, S4 24 | S2 | The right event population, joined through the vessel register | The acknowledgement file: event-duration totals reproduce 3 of 12 past campaigns |
| 2 | Weather-window analysis: a day is lost when no 24-hour workable window is available: S3 48, S5 39, S2 37, S4 34, S1 31 | S3 | The industry-standard downtime estimate, reproducing 5 of 12 campaigns | The port register: S5's vessels need 42 hours of round trip and remobilisation before they can work |
| 3 | **Decisive:** chain stand-downs through gaps shorter than each site's round trip plus 12 hours of work, count the chained span: S5 80, S3 49, S2 44, S4 38, S1 33 | **S5** (5th of 5 on rung 0) | — | — |

* **Position table.** S5 ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (S3 leads it by 1.23×), and leads only rung 3. Rung leaders
  beat their runners-up by 1.24×, 1.24×, 1.23× and 1.63×.
* **Discriminator dominance.** S3 carries a 1.23× window-analysis advantage into rung 3, so the required edge is 1.2 × 1.23 = 1.48×. S5's
  sequence uplift (80 against 39, 2.05×) against S3's (49 against 48, 1.02×) is an edge of 2.01×, 1.36× the requirement, and the net is 2.01
  / 1.23 = 1.63×.
* **Partial correction priced (L3).** A solver who lengthens the window to one round trip for every site (the fleet's typical 28 hours)
  names S3 again, 52 days against S5's 44 (1.18×). One who uses each site's own round trip but drops the 12-hour working minimum puts S5's
  threshold at 42 hours, below its 45- to 51-hour gaps, and also names S3, 53 against S5's 45 (1.18×). Both land on the rung-2 leader.
* **Grid.** Event population (alert storms or stand-downs) × gap rule (none, 24-hour window, uniform round trip, site round trip plus work
  minimum) = 8 cells. Alert-storm cells name S1; stand-down cells name S2, S3, S3 and S5 in that order, so only the site-specific chain
  names S5.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The operations manual says only that floating vessels shelter in their marshalling port during stand-downs. No
   document says when they return or that gaps can be lost.
2. **The corpus pins a construction, not a menu (Pattern B).** The site-specific chain reproduces the acknowledged weather downtime of all
   12 campaigns within one day. The best rival, the 24-hour window, reproduces 5; no single uniform gap length from 12 to 60 hours
   reproduces more than 7, because the threshold is different at every port. Every rival under-predicts far-port campaigns, so each misses
   the 12-campaign total by 15% or more.
3. **No arithmetic symptom.** Buoy records are complete after the documented missing codes, stand-downs tie to the vessel logs, and every
   monitor statistic reproduces from the hourly series.
4. **Not a row predicate.** It needs declustered stand-downs, the gaps between consecutive ones, a join from site to port to transit time,
   and a chain over gaps that fall short, per site, across eighteen winters.
5. **The enumeration is arithmetic.** Lost gaps are computed; no column marks a sequence.
6. **No cutover date.** Storm pairing is a property of each site's weather regime in every winter of the record; nothing steps.
7. **Survives deletion.** Remove both voices and the monitor export: the window analysis is still the natural build.

## 6. The calibration corpus

* **Form.** The developer's acknowledgement file for 12 winter campaigns (2019–2025) across the five sites: every day the contractor
  claimed, with its status and the developer representative's acknowledgement.
* **What it pins.** The chain rule and its 12-hour working minimum: every acknowledged return to site was preceded by a calm window of at
  least the round trip plus 12 hours, and every gap shorter than that was acknowledged as weather time.
* **Twin pair.** Campaigns S4-2021 and S5-2023 are identical on every monitor statistic (alert storms, stand-downs, exceedance hours, return
  level, 24-hour window availability). The developer acknowledged 21 and 43 weather days, 2.0× apart: S5-2023's stand-downs came in pairs
  with gaps shorter than S5's round trip, and S4-2021's did not.
* **Resemblance points at the decoy.** On every monitor statistic S5 resembles the three campaigns with the least acknowledged downtime.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The campaign plan: the jack-up goes where it avoids the most floating-vessel weather downtime over the 120-day campaign.
  The operations manual: floating vessels shelter in their marshalling port during stand-downs. The vessel register's crane limits by
  depth and the jack-up's limit above every recorded peak. The port register's transit times. One sentence each.
* **Empirical pins.** The 12-hour working minimum and the chain rule, from the acknowledgement file.
* **Voices.** The planner: "Fifteen years of buoy data say S1 is the worst sea on this coast." The marine coordinator: "Downtime is hours
  above the limit; everything else is noise."
* **Licensed wrong basis.** The campaign plan records that the developer's marine warranty surveyor ranks sites by the 1-year return level
  of storm peaks and will present that ranking to the project board.

## 8. Determinism by construction

* **Gap threshold.** No gap in the record falls within three hours of any site's round trip plus 12 hours, so transit-time rounding or a
  10- to 14-hour working minimum chains the same gaps.
* **Declustering.** Stand-downs separated by under six hours merge; 3- to 9-hour merge rules give the same chains.
* **Transit.** The port register's times include mean tidal waiting, by vessel class, and each site has one marshalling port.
* **Averaging.** Expected downtime is the mean over the eighteen winters of the record; medians name the same site and the committed figure
  is the mean, to the nearest day.

## 9. Prompt sketch and deliverables

> We have one jack-up for the winter campaign and five sites that want it. The planner's alerts say S1 has the worst sea on the coast. Tell
> me which site gets the jack-up and how many weather days it saves us over the 120 days, to the nearest day, in a line for the project
> board. Send `jackup_case.xlsx`, a chart `stand_down_chains.png`, and a one-page `allocation_memo.pdf`.

* `jackup_case.xlsx` — the five sites under each rung's construction with its campaign reproduction count (ask C), the fuel sheet (ask A)
  and the tidal-access sheet (ask B).
* `stand_down_chains.png` — one lane per site for a typical winter, stand-downs as bars, gaps coloured usable or lost against that site's
  round trip, each site's threshold labelled, and the expected downtime per site in the margin.
* `allocation_memo.pdf` — the committed site and figure, and why each other site falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six floating vessels, fuel burned per transit hour last winter from bunker records
  and tank soundings. *Device:* delivery notes give volume at 15°C and soundings give observed volume at tank temperature, and the fuel
  guide's correction table reconciles them; mixing them misstates four vessels. The allocation never uses fuel records.
* **Ask B (device-carried).** For each marshalling port, January hours per day with berth access for a 7.5-metre draft, and the longest
  daily window. *Device:* the tide table is referenced to chart datum and berth depths to the port's own datum, with the offset in the port
  register; comparing them raw misstates access at three ports. The transit table already includes tidal waiting, so the main call never
  uses the tide table.
* **Ask C (validity).** Each site's downtime under each of the four rung constructions, and each construction's count of reproduced
  campaigns.
* **Decoupling.** Clearing the chain rule and the stand-down population changes no figure in asks A or B.

## 11. Rubric arithmetic

6 vessels × 2 (ask A) + 5 ports × 2 (ask B) + 5 sites × 4 constructions (ask C) + the committed site, its downtime avoided, the runner-up
and the margin + 5 named chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* Rung figures as in the ladder; S5 is 5th, 4th, 2nd (1.23× behind S3) and 1st (1.63× ahead of S3). The two partial builds give S3 52
  and 53 against S5's 44 and 45.
* Round trips plus remobilisation: 26–30 hours for S1–S4 and 42 for S5, so chain thresholds of 38–42 and 54 hours. S5's within-pair gaps
  run 45–51 hours.
* The jack-up's limit exceeds every recorded peak at all five sites.
* S4-2021 and S5-2023 are identical on every monitor statistic.
* Fuel records and tide tables never touch the buoy series, stand-downs or the acknowledgement file.
* No missing buoy hour falls within 48 hours of a stand-down at any site.
