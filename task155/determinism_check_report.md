# Verdict, task155 (re-judge, fresh)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair is needed and no rerun is required. Two optional notes are listed under Fix.

**Why:** The standard (WP-04 s.3-5) files the estimand literally. The crew goes to the store with the most paid hours of open Christmas shifts that call-ins would leave unfilled, forecast with the crew at no store. Crew hours are the paid hours of the placed store's open lines. I rebuilt the call-in module from kws_callin_module_notes.pdf over the published rosters, with an acceptance model fitted to the 156,070-offer history. Camberwell leads in every run, with about 605 unworked hours against about 391 for the next store. The leading alternative, Werribee, wins only if the offer-history structure is ignored. The tables for last year reproduce to the decimal. All five gates A-E pass.

## Evidence (recomputed from the bundle)

| Item | Result | Source |
|---|---|---|
| Open lines and paid hours at Christmas | Reproduced. Werribee 3,254.0 (golden 3,250), Box Hill 2,602.0, Altona 1,770.0, Camberwell 1,092.5 on 215 lines, Ballarat 876, Ringwood 1,140, Sunshine 1,378, Williamstown 641.5 | christmas_roster_2026_published.xlsx, status OPEN |
| Crew hours at Camberwell | 1,092.5, which is 1,090 to the nearest 10. The 25-person crew's 38-hour weekly cap (3,800 hours over four weeks) does not bind. | same file |
| Adjacent offers accepted at 32% against 4% | Reproduced. 2,241 adjacent offers, 31.8% accepted. The other 153,829 offers, 3.86%. This used both roster exports, the person-code to payroll mapping with previous numbers, vacated lines, and booked call-ins. | callin_offers, both roster files, kws_people, payroll_casual_register |
| Own-casual carry-on share of open shifts, after eligibility checks | Reproduced. Werribee 100%, Box Hill 95.6%, Altona 78.7%, Camberwell 0.0%. Ballarat 62%, Ringwood 71%, Sunshine 57%, Williamstown 75%. | christmas roster, kws_availability, module rules |
| Forecast unworked hours with the crew at none (my own 12-run simulation) | Camberwell about 605 (range 540-632). Next: Sunshine 391, Ringwood 350, Ballarat 328, Williamstown 324, Altona 322, Box Hill 319, Werribee 266. Camberwell is first in 12 of 12 runs. | simulation of the module rules plus a logit fitted on the offer history |
| Easy-route fork: drop the adjacency term | Werribee about 1,838 unworked hours, so Werribee wins. At half strength Werribee still wins (865 against 597). The flip point lies far from the fitted coefficient of 2.73 (SE 0.06). | same simulation |
| Table 1, last year's call-ins (28 Nov-24 Dec 2025), put out / covered / uncovered | All eight rows reproduce exactly, e.g. Altona 1,615.0 / 843.0 / 772.0 and Werribee 299.0 / 98.5 / 200.5. | see method below |
| Table 2, cross-store cover | All eight rows reproduce exactly. Cover into the store / out by the store's own casuals: Altona 44.0 / 4.0, Box Hill 33.5 / 90.0, Camberwell 65.5 / 54.0, Ringwood 83.0 / 38.0, Sunshine 34.5 / 32.0, Williamstown 24.0 / 39.0, Werribee 0.0 / 27.5, Ballarat 0.0 / 0.0. | same method, plus the payroll cost-centre history for each casual's home store on the shift date |

Method for Table 1:
- Put out = legacy VACANT lines (paid hours = Hrs less a 30-minute break over 5 hours) plus distinct ABS/LVE vacated lines.
- Re-raised shifts and the casual's give-back count once.
- Covered = fills backed by an ACCEPTED offer, minus the give-backs.
- Store-local shift dates.

### Literal reading, with the forks I tested

- **"Unworked":** defined in s.4 as unfilled open shifts. Absolute hours (Camberwell) and share of open hours (Camberwell about 55%) give the same store. Vacated shifts are excluded by s.4.
- **Hours:** paid hours per the EA (unpaid 30-minute meal break on shifts over 5 hours). The legacy export's Hrs is shift length, which the module notes document. Using it would give wrong 2025 figures but not a wrong main call.
- **Register mess:** 601 FILLED rows have no ACCEPTED offer and duplicate another fill (same casual, same close time). ABS duplicates are documented. The OPN duplicates are not, but they are derivable: the roster VACANT line count and the accepted offers agree. A literal reader who counts register rows gets the Table 1 covered hours wrong. This is Layer 1 mess, recoverable from the shipped files.
- **Home store for Table 2:** the transmittal says people.home is only the extraction-date home, so the payroll cost-centre history is needed. 24 casuals moved. This is documented.
- **Availability for Dec 2026:** the current open-ended profile applies. Last year's student profile switched on 26 Dec, after the term ended, so the data supports the literal reading.
- **Margin:** thick and clean (605 against 391). No gate C fragility.

### Competing answers
- Werribee (most open hours; best on a naive fill rate): survives only if adjacency is ignored. The data refutes it (32% against 4%, 2,241 offers).
- Box Hill or Altona (evening uplift): their carry-on shares are 96% and 79%, so their unworked hours are low in the simulation.
- Ballarat (highest uncovered hours in 2025, 1,297.5): it has only 876 open hours this year, and its rate is not special.

## Files/Hygiene

PASS.
- **Count and formats:** 15 files in 5 formats: csv ×7, xlsx ×2, pdf ×3, json, txt. The largest file has 156k rows.
- **Distractors:** the trading plan and the school-terms calendar are relevant but unused by the solution.
- **Realism:** the files read as KWS and payroll exports, with mixed date formats and a legacy export. The register carries duplicates.
- **Provenance:** I saw no authoring leakage.
- **Dates:** the standard is dated 9 Oct, the extraction is 12 Nov, and the data ends at 12 Nov 05:00Z. Coherent.
- **Metadata:** the xlsx and pdf metadata names fictional authors, with no toolchain banner.
- **Contamination:** none. No exclusion-level finding.

## Stump power (Gate F)

Strong.
- **Easy route 1:** rank by open hours, which gives Werribee.
- **Easy route 2:** last year's fill rates. Camberwell fills best (74%) and Werribee worst (33%), so Werribee again.
- **Easy route 3:** model acceptance without the continuation-of-own-shift effect. The simulation puts Werribee at 1,838 unworked hours.
- **Why it works:** the continuation effect is not narrated anywhere. It must be found in 156k offers joined to rosters. The Christmas Camberwell uplift (9:00-15:00 weekday online picking) has no adjacent rostered casual, which flips the store from best filler to worst.
- **Judged:** the past is correct, the forecast is not pinned by the trailing figure, and a strong model that extrapolates fails.

## Stumping type (Gate G)

mechanism: forecasting (with an acceptance-model selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no.

No reported figure is wrong. The trailing fill rates are correct and the forecast diverges for a data-supported structural reason. Run on clean data it would still stump. Passes.

## Three rules (Gate H)

domain: pass, layers: pass, decisive_step: analytical.

- **Domain:** the workforce-planning task is the field's own work. A call-in fill forecast from offer acceptance and availability, over a roster, decides the placement. Swapping in another field's nouns would not preserve it.
- **Layer 1:** a legacy against KWS roster layout; UTC against store time; payroll number and cost-centre changes; duplicated register rows; Hrs against paid hours.
- **Layer 2:** modelling acceptance at the offer level with the own-shift continuation, then forecasting the unfilled hours of new shifts with the module's eligibility rules.
- **Easy route:** a strong analyst who cleaned everything and read every rule would still rank on historical fill rates, or fit acceptance without the adjacency term, and file Werribee.

## Fix

none required (disposition APPROVE).

Optional notes:
1. The OPN duplicate fills are not mentioned in kws_callin_module_notes.pdf, while the ABS duplicates are. They are resolvable from the data, so this is not a defect.
2. The roster xlsx was created at 10:05, five minutes after its stated 10:00 publication time. Cosmetic.
