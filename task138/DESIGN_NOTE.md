# task138: Orrinsford levee crown review for the 2027 capital plan (architecture 2)

Private, never ships. Re-rooted on 2026-11-01 at the Batch 3 queue reset: architecture 1 (the Kestrel Bend Irrigation
District's 2027 season order, shipped 2026-10-15 with no portal result) is closed with its world and kept in
`## Architecture 1 record`; its card identity is in the card's `lineage`. Seed FC09 numbered the slot; nothing of its
world, decision or quantity is used here beyond the objective.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task138.json`, architecture v2, registered 2026-11-01T17:20:03Z; `guard.py check` WARN only (repeat.gate_g, repeat.question_form; NOTEs differentiated against task104, task171 v5, task168); re-checked on the registered card as the draw's last act |
| Domain / task type | physical-environmental-sciences / hydrology-flood-frequency (client domain physical-environmental-sciences; the task type serves Forecasting): the 1 per cent annual chance flood at a gauged town, carried through the hydraulic model to a levee crown |
| Objective | Forecasting & Predictive Modeling: the flood the levee must hold in the years after the review, the 1 per cent annual chance peak at Orrinsford for the river as it now runs, a window not yet open |
| Shape | 04 (setting one dial): the uniform crown raise 0 to 4 ft, each setting with the discharge it holds and its annual chance (5 graded figures), the call (1) and the design discharge (1); asks A (crown settlement, eight reaches) and B (warning lead time, seven floods); the chart with named parts (frequency curve, record curve, five capacity lines, the 1 per cent line, about 5); the two files (2): about 27 criteria |
| Decision | `dial_setting`, answer unit `count` (whole feet of crown raise) |
| Mechanism | gap population then time (the flood population the record samples is not the river's present one, and the change is dated by the levee raises); pattern none; generators G16 then G6; Gate G `forecasting`; layer 2 family `field_method`, pattern `own:post-raise-two-gauge-record-extension`; strategy `other` |
| Furniture | forum `trustees_or_governors` (the district's Board of Trustees adopts the capital plan), forcing event `budget_or_appropriation` (the 2027 capital plan), org family `utility_or_infrastructure` (a levee and drainage district), role family `policy_adviser` (the district engineer reviews the levee against the district's standard), context artifact `published_series` (the State Water Survey's annual peak export), calibration none, question form `whether` |
| World | Orrinsford, a fictional Midwestern river town on the Tamsen River; the Orrinsford Levee and Drainage District (OLDD); the State Water Survey's gauges at Coyle Bridge (RM 41.0, 4,930 sq mi) and Orrinsford (RM 12.6, 6,480 sq mi); the State Department of Natural Resources' levee inventory; six agricultural levee districts on the 28 miles between the gauges, raised to the 1 per cent flood between 1996 and 2008 |
| Spine | `SWS_05432100_hourly_WY2017-2026.csv`, 87,635 hourly rows at Coyle Bridge (ask B); the main call's record is the annual peak export (280 rows, five gauges) |
| Deliverables | `levee_raise_review.xlsx` (raise options, the present-river series and fit, settlement by reach, closure lead times), `levee_raise_memo.pdf` (one page to the Board with the frequency chart) |
| People | `guard.py names --geo US --seed 138`: Dennis Zhang (district engineer, LS-02 and OP-04), Kristin Lucas (land surveyor, both crown surveys), Eric Thornton (State Water Survey hydrologist, the skew release), Jesus Hernandez (hydraulic engineer, the 2019 update); none appears in the prompt |
| As of | 9 November 2026 (the district engineer's review for the 2027 capital plan) |

**Candidates screened before this one** (each in `## Tried and rejected`): TV audience flow after a lead-in change
(spent, task115 and task174), hospital weekend discharges (spent, task127 and task170), a gauge rating drifting with
channel aggradation, rating hysteresis on the rising and falling limbs (spent at the abstraction test, task279), a
reservoir regulating the flood record, landfill airspace with waste settlement. `guard.py slots` on the chosen
mechanism's nouns (levee floodplain, attenuation storage) and its setting's (levee raise, flood frequency, Bulletin)
returned no slot.

**Data-native sentence.** Orrinsford's own annual peak record holds two rivers: until the last of six agricultural levees
between the gauges was raised (in force from water year 2009) the floodplain behind them filled in every flood above
about 46,000 cfs at Coyle Bridge and cut the town's peak, so the record's two great floods (1970 and 1973, Orrinsford at
0.71 and 0.80 of Coyle Bridge against 1.064 since 2009) are smaller than today's river would make them, while every smaller flood, most of the
record, is untouched; the change lives only in the upper tail the 1 per cent flood is read from, leaves no trend or
step, and shows only against a second gauge above the reach.

**Abstraction test.** Stripped of nouns: the deciding quantity is an upper quantile of a long record whose largest
members were produced under a regime that ended part way through, a regime that never touched the ordinary members,
and it is recovered by carrying a second, unaffected long record across at the relation the two show since the regime
ended. The nearest drivers on file (task104, task171 v5, task168) recover a level, a rate or a share, not a tail
quantile of a non-homogeneous record; differentiated on the card.

## Survivor anatomy

- Actor: the deciding property, whether a year's Orrinsford peak was cut by upstream floodplain storage that no longer exists, has no column anywhere: the peak export carries discharges, the inventory carries each segment's raise year, and the property is the relation between the two gauges' peaks in the years before and after those raises.
- Link: the comparison of Orrinsford's peaks against Coyle Bridge's by water year, split at the in-force year of the raises on the segments between the two gauges' river miles (inventory Segments and Gauges sheets), which LS-02's frequency method never asks for; no key, code or sentence ties the raise years to the peak record.
- Reflex: LS-02's own method (log-Pearson Type III by moments with the weighted skew) fitted to the Orrinsford record as published, which meets its window of one peak for every water year since 1962, is rung 0 and files no raise (95,430 cfs, 0 ft).
- Back-test: the textbook route validates: Mann-Kendall p 0.43 and Pettitt p 0.73 on the record, no Bulletin 17B low outlier, the agency's peak codes flag nothing at Orrinsford, and Fenwick downstream (100,192 cfs at site) agrees with the town.
- Second use: every file the decisive step reads is in the pack for its own reason: the peak export is the record LS-02 fits and carries the whole basin as the agency exports it; the inventory carries the town levee's crown at the model cross-sections and its bridge closures, which the crown check needs, beside every other segment.
- Shock: the movement reads as ordinary hydrology: big floods smaller downstream through floodplain storage is textbook, the town record has no trend, step or outlier, and the two low ratios sit among 65 years of ratios near 1.06; the golden's answer is not an interval of any sort of the gauges or years.
- Pins: LS-02 section 2 files the WHAT (the 1 per cent flood at the Orrinsford gauge "for the river, its floodplain and its levees as they stand at the time of the review") and section 3 its window (one annual peak for every water year since the gauge opened in 1962); no filed sentence names the upstream raises, the record's homogeneity, a second gauge or a relation, and the published record meets both sentences as they read, so the pins do not hand the step over.

## Default path

1. Read LS-02: the design flood is the 1 per cent annual chance peak at the Orrinsford gauge, fitted as log-Pearson Type III by moments with the station skew weighted with the SW-16-03 regional skew (region 2, -0.08, mean square error 0.14).
2. Take the 65 Orrinsford annual peaks from the State Water Survey export (one for every water year 1962 to 2026, the window LS-02 section 3 sets, the provisional 2026 included) and fit: mean of logs 4.4734, standard deviation 0.2089, station skew 0.281, weighted skew 0.133; the 1 per cent discharge is 95,430 cfs.
3. Check the record before trusting it: Mann-Kendall (p 0.43) and Pettitt (p 0.73) find no trend or change point; no low outlier.
4. Read Table 4 at that discharge (linear in discharge), add LS-02 freeboard (3.0 ft, 4.0 ft within 100 ft of a bridge, plus the upstream allowance) and compare with the 2024 crown at the 21 cross-sections: the worst, the railroad closure at 118+70, has 1.16 ft to spare.
5. File no raise; each raise's annual chance of exceeding what it holds is 0.7, 0.5, 0.4, 0.3 and 0.2 per cent.

Ends on: no raise (0 ft), design discharge 95,000 cfs.
Golden: raise 2 ft, design discharge 110,000 cfs.

## Stump sentence

The default path fits LS-02's frequency curve to Orrinsford's record as published and files no raise (0 ft, a 95,000 cfs
design flood) because it never asks whether the 1962 to 2008 peaks belong to the river as it now runs: the six levees
between Coyle Bridge and Orrinsford, all raised by October 2008, no longer let their floodplains take the top off a big
flood, which shows only when Coyle Bridge's record is set against the raise years; rebuilt for the present river the
design flood is 110,000 cfs and the crown needs 2 ft.

## Three rules

Task type: hydrology-flood-frequency, the 1 per cent annual chance flood estimated from a gauged annual peak record and carried to a design level, a task type that serves Forecasting.
Domain test: the deciding quantity is the 1 per cent annual chance peak discharge at the Orrinsford gauge, estimated the field's way with a log-Pearson Type III frequency curve (moments on logs, weighted skew, the Bulletin 17 family) and read through the hydraulic model's water surfaces to the crown with freeboard.
Swap: "Does the warehouse need a bigger dock to meet its standard against its 1 per cent busiest day, now that its suppliers' depots were enlarged?" stops making sense: there is no stage at which upstream storage starts to fill, no peak cut only above it, and no second meter above the reach whose relation changes when the storage is gone.
Layer 1: the agency's export lists each annual peak by date with no water year column (Oct to Dec peaks belong to the next water year), three significant figures, a provisional 2026 approval code, estimate codes and gaps on the other gauges; Table 4 sits in the consultant's PDF with station strings; the DNR inventory reports raises as the sponsors wrote them ("Oct 1998", "2003-11", "Sept 2005"); the asks' telemetry, surveys and benchmarks carry two vertical datums, a re-stationed levee, a gauge datum change and a logger clock change (ask devices, ledgered).
Layer 2: family field_method, record homogeneity: a flood frequency curve assumes its record is one population of floods under the conditions the estimate is for; upstream levee raises broke that for the large floods only, and the field's remedy (adjusting the record to present conditions through a long-record gauge above the change) has to be built from the two gauges.
Decisive step: recognising that the Orrinsford peaks before water year 2009 belong to a river whose upstream floodplain still held back big floods, so the published record is not homogeneous with the river as it now runs, and carrying Coyle Bridge's long record across at the relation the two gauges show since the last levee raise.
Not semantics: every field, code, unit and definition read correctly (water years, approval codes, three-figure peaks, Table 4, LS-02's freeboard and skew rules) still gives 0 ft on the published record; nothing in any field marks the attenuated years, and the agency's codes say nothing about them.
Not rule application: the filed rules fix the WHAT (s.2, the river as it stands; s.3, one peak for every water year since 1962) and the method, and the published record satisfies both as they read, so LS-02 executed word for word files 0 ft; no rule says the 1962 to 2008 peaks are not the present river's or how to rebuild them. The window rules out the shortcut that keeps only the 18 water years since the last raise, and it does not name the rebuild. The enumerated family (the at-site fit, post-raise years only, whole-record relation, Coyle Bridge unscaled, since 1994, drainage-area ratios at 0.5 to 1.0) spreads 93,473 to 136,398 cfs, 0 to 6 ft; the standing family once the raises are seen (13 constructions: six relation forms fitted over 2009 to 2026, the inverted regression, mean of ratios, three fitting windows, carrying only the pre-raise years, keeping larger observed peaks) spreads 109,813 to 110,527 cfs, every member 2 ft with the same five chances; the ruling-out is quiet, two ratios out of 65 visible only with both gauges side by side by water year.
Analyst test: a strong analyst who reads every rule, takes LS-02's window as given (one published peak for every water year since 1962) and fits its frequency curve to the Orrinsford record as published, after homogeneity tests that pass, files no raise (0 ft) with a 95,000 cfs design flood; the window is a WHAT (which years the record covers), and judging whether those years' peaks are the present river's is the decisive analysis it leaves open.
Estimand: LS-02 section 2 (`OLDD_LS-02_levee_standard_rev3.pdf`): the peak discharge at the Orrinsford gauge with a 1 per cent chance of being exceeded in any year, for the river, its floodplain and its levees as they stand at the time of the review, fitted (section 3) to one annual peak discharge for every water year since the gauge opened in water year 1962, discharges from the State Water Survey's records (section 8); the crown is the latest certification survey's (section 6) and a raise is uniform in whole feet (section 7). The window is part of the WHAT: it says which years the present-river record covers, never how a year's present-river peak is found.
No decoy: nothing is planted: no memo, prior review, published design flood or stakeholder figure ships; the hydraulic study gives water surfaces by discharge and no design discharge; the raise years are the sponsors' own inventory entries.
No certified replay: no certified design discharge, frequency curve or prior review ships, so the method is never recovered by matching published figures; LS-02 files the frequency method openly and the record's construction is the analysis.
Lesson: an at-site flood frequency curve is only as good as the homogeneity of its record, and upstream flood-control works change its upper tail without leaving a trend; the check is a second gauge set against the works' in-force dates; no build on file teaches record homogeneity broken by upstream floodplain storage (`guard.py slots` returns nothing on levee, floodplain or attenuation).

**Layer 1 inventory** (each asserted neutral in `checks.py`, L1 and SF rows):

| Item | System that writes it | File | Natural mishandling | Effect |
|---|---|---|---|---|
| Peaks by date, no water year column | SWS peak export | annual peaks CSV | label by calendar year | same call and bin (SF8) |
| Published peak times in local standard time | SWS peak export | annual peaks CSV | read as UTC | ask B only (the clock routes) |
| Provisional WY2026 | SWS approval workflow | annual peaks CSV | drop it | same call and bins (SF12) |
| Estimate codes, missing years | SWS records at Ashby, Gale Creek, Fenwick | annual peaks CSV | none on the main gauges | none (SF13) |
| Table 4 in a PDF, station strings | consultant's report | Table 4 PDF | parse error | asserted read (L1) |
| Raise dates in the sponsors' words | DNR inventory | inventory XLSX | read "Oct 2008" as WY2008 | same call and bin (SF14) |
| NGVD 29 survey and gauge datums | the 2016 surveyor, the ORF2 logger header | 2016 survey, ORF2 export | not converted | ask A and B only (ledgered) |
| Levee re-stationed in 2019 | the 2019 tie-in project | 2016 survey | join by station number | ask A only (device) |
| Coyle Bridge gauge datum lowered October 2019 | SWS field office | Coyle hourly, OP-04 | 21.0 ft throughout | ask B only (device) |
| The old ORF2 logger's records in CST, three days beside the new one | the old and new loggers | ORF2 export | read as UTC | ask B only (device) |

## Readability screen

| Rung | Column or one join | Field reflex | Named in a document | Helper narration | Largest anomaly | File read only by it | Verdict |
|---|---|---|---|---|---|---|---|
| Rung 0, LS-02 fit to the published record | the record is the column | yes, the reflex | LS-02 sections 2 and 3 | none | no | no | readable |
| Rung 1, homogeneity tests | one series | yes (Bulletin 17C advises it) | no | SW-16-03's generic limitation line | no | no | readable |
| Rung 2, post-raise years only | needs the raise years | no | no | none | no | no | silent |
| Rung 3, Coyle Bridge at the whole-record relation | one join by water year | partly (record extension) | no | none | no | no | silent |
| Decisive, the present river rebuilt from Coyle Bridge at the post-raise relation (decisive) | no column; two files joined by water year and split by in-force years from a third sheet | no | no | none | no (two ratios among 65) | no (the inventory and the Coyle Bridge rows each have their own use) | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | design flood | 1 per cent annual chance peak at Orrinsford for the river as it now runs, over one peak for every water year since 1962 | 1 per cent of the published record as it stands | 0 ft | LS-02 s.2 and s.3 file the estimand and its window; the published record is an easier method on the same estimand, not another reading |
| SF2 | annual chance per raise | exceedance of the discharge the raised levee holds with freeboard | exceedance of the discharge held to the crown | figures move | the prompt's "with its freeboard" and LS-02 s.7 |
| SF3 | crown | the 2024 certification survey (the inventory's crown sheet equals it at all 21 cross-sections) | the 2016 survey, or the 2024 crown less projected settlement | 2 ft either way | LS-02 s.6, "the latest certification survey"; asserted 2 ft with three more years of settlement |
| SF4 | where the crown is checked | the 21 cross-sections of Table 4 | every 50 ft survey shot | same raise and bins | asserted (same call) |
| SF5 | 4 ft freeboard | within 100 ft of a bridge or closure | only at the bridge stations | same call | no other cross-section within 100 ft (asserted) |
| SF6 | Table 4 interpolation | linear in discharge | log-linear | same raise and bins | LS-02 s.4; asserted same |
| SF7 | which stations are bridges | 62+40 and 118+70 | none | same call | inventory Structures and the Table 4 marks agree (asserted) |
| SF8 | annual peak year | water year | calendar year labels, or calendar-year maxima | same call and bin; maxima drop water years' peaks | asserted; LS-02 s.3 (one peak for every water year) |
| SF9 | raise | uniform, whole feet | fractional or local raises | not an option | LS-02 s.7 |
| SF10 | regional skew | region 2, -0.08 and 0.14 (Pell and Marrow counties) | another region | not licensed | SW-16-03 Tables 1 and 2 |
| SF11 | 1 per cent | annual exceedance probability 0.01 | none | same call | LS-02 s.2 |
| SF12 | provisional 2026 | included | dropped | same call and bins | asserted |
| SF13 | estimate codes | on other gauges only | dropping estimated years | same call | asserted (no code at Orrinsford or Coyle Bridge) |
| SF14 | first fully raised year | water year 2009 (raise reported Oct 2008) | 2008 | same call and bin | asserted |
| SF15 | skew used | weighted | station skew only | 4 ft | LS-02 s.3 files the weighting |
| SF16 | upstream allowance | 0.5 ft at 0+00 to nothing at 180+00 | none | figures move | LS-02 s.5 |
| SF17 | ask A points | crown shots matched by position (every 2016 shot on today's levee pairs one to one with a 2024 shot), structures in or out | structures included; median per reach; the difference of the two surveys' reach means | same bins | asserted |
| SF18 | ask B crossing time and rounding | interpolated within the hour, rounded | first hour at or above, last hour below, truncation | same whole hours (every lead's fraction 0.1 to 0.4) | asserted |
| SF19 | ask B floods | every rise of the Orrinsford stage through the Main Street sill since October 2016 | none | seven floods | asserted |
| SF20 | ask A datum | NAVD 88 = NGVD 29 + 0.27 at every district benchmark | averaging a subset | same | every pair gives 0.27 (asserted) |
| SF21 | which years | one annual peak for every water year 1962 to 2026 | only the 18 water years since the last raise (104,714 cfs, 1 ft) | 1 ft | LS-02 s.3, "every water year since the Orrinsford gauge opened in water year 1962" |
| SF22 | records | discharges from the State Water Survey's published records | every year's peak used as published | 0 ft | LS-02 s.8 names the source, not the years' values; s.2 sets the river they describe (asserted: no sentence says the peaks are the published ones) |

## Ladder

| Rung | Construction | Design discharge (cfs) | Raise | Annual chance by raise 0 to 4 ft (%) |
|---|---|---|---|---|
| 0 | LS-02 fit to the published Orrinsford record, 1962 to 2026 | 95,430 (95,000) | 0 ft | 0.71, 0.54, 0.41, 0.31, 0.24 |
| 1 | rung 0 after Mann-Kendall (p 0.43) and Pettitt (p 0.73) | 95,430 | 0 ft | as rung 0 |
| 2 | only the 18 water years since the last raise (outside LS-02 s.3's window) | 104,714 (105,000) | 1 ft | 1.13, 0.89, 0.70, 0.56, 0.45 |
| 3 | Coyle Bridge's record at the whole-record relation (0.969) | 100,546 (100,000) | 0 ft | 0.94, 0.75, 0.59, 0.47, 0.38 |
| golden | Orrinsford from 2009, Coyle Bridge x 1.064 (the 2009 to 2026 relation through the origin) before | 110,403 (110,000) | 2 ft | 1.40, 1.12, 0.90, 0.72, 0.58 |
| off | Coyle Bridge unscaled | 103,772 | 1 ft | |
| off | Orrinsford since 1994 | 93,473 | 0 ft | |
| off | drainage-area ratio at 0.5, 0.7, 1.0 | 118,971, 125,658, 136,398 | 3, 5, 6 ft | |

The relation's form, every one fitted over water years 2009 to 2026 and applied to 1962 to 2008 (asserted per form in
`checks.py`; tightest margin of any chance to its one-decimal edge, the design discharge's margin to 107,500 or
112,500):

| Form | Design discharge (cfs) | Chances by raise 0 to 4 ft (%) | Tightest chance margin | Discharge margin |
|---|---|---|---|---|
| through the origin (golden) | 110,403 | 1.401, 1.118, 0.896, 0.721, 0.583 | 0.029 | 2,097 |
| ratio of means | 110,477 | 1.405, 1.121, 0.899, 0.723, 0.585 | 0.027 | 2,023 |
| straight line (OLS) | 110,260 | 1.394, 1.112, 0.891, 0.717, 0.579 | 0.029 | 2,240 |
| straight line in logs | 110,359 | 1.399, 1.116, 0.895, 0.720, 0.582 | 0.030 | 2,141 |
| MOVE.1 in logs | 110,372 | 1.400, 1.117, 0.895, 0.720, 0.582 | 0.030 | 2,128 |
| every year from Coyle Bridge at the ratio | 110,445 | 1.403, 1.120, 0.898, 0.723, 0.584 | 0.028 | 2,055 |

Stress rows (mean of ratios, the inverted regression, fitting from 2008, 2010 or 2012, carrying only the pre-raise
years, keeping a larger observed peak) stay in every bin, tightest 0.019. Shortfall at 118+70 under the golden 1.50 ft
(the railroad closure governs every raise; Main Street 62+40 is next at 0.77 ft). Gate F count on the clean truth and
the pack: no cheap route files 2 ft (asserted).

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | the river as it now runs (LS-02 s.2, filed) over one peak for every water year since 1962 (s.3, filed); whether a year's published peak is the present river's is the analysis; every relation form converges (C1 over six forms and seven stress rows) |
| 2 | Unit of account | the annual peak at one gauge; the raise in whole feet (filed) |
| 3 | Attribution window | water year (C1: calendar labels give the same call and bin) |
| 4 | As-of dating | the review date; the record through water year 2026 (C1 with or without the provisional year) |
| 5 | Version basis | discharges from the State Water Survey's records (LS-02 s.8), the provisional 2026 included (C1); the latest certification survey (s.6) |
| 6 | Denominator | none in the main call; ask A averages matched shots per reach (C1 with structures) |
| 7 | Weighting | moments on logs, equal years (filed method) |
| 8 | Window length | every water year since the gauge opened in 1962 (LS-02 s.3, filed, which rules out the 18-year fit, SF21); the relation's fitting window converges 2008 to 2012 (C1) |
| 9 | Boundary inclusivity | the in-force year (Oct 2008 raise, WY2009); C1 with 2008 |
| 10 | Rounding path | figures computed unrounded, rounded once at the end (prompt) |
| 11 | Tie-break | none arises (asserted margins) |
| 12 | Maturity and censoring | no censored peaks; no low outlier (asserted) |
| 13 | Order of operations | fit, then quantile, then Table 4, then freeboard; commuting |
| 14 | Row order | none (sorted by water year; sums) |
| 15 | Duplicate resolution | one peak per gauge and water year (asserted unique) |
| 16 | Identity normalisation | site numbers; ask A structures matched by name across surveys (asserted one offset) |
| 17 | Netting against gross | none |
| 18 | Dimensional units | cfs, ft NAVD 88; ask datums converted by the benchmark pairs (C4 for the ask, asserted) |
| 19 | Code and status semantics | approval and estimate codes neutral (asserted) |
| 20 | Integerisation | the raise is the smallest whole foot clearing the shortfall (filed) |
| 21 | Clause scope | LS-02 freeboard rules scope to cross-sections (s.6) |
| 22 | Forward window contents | the design flood is a property of the present river; the record through 2026 is the driver, nothing past it is needed |

## Literal reader

Executed word for word, LS-02 sections 2 to 8 on the shipped files ask for the 1 per cent flood of the river as it
stands, fitted to one annual peak for every water year since 1962, with discharges from the State Water Survey's
records. The published record meets the window and the source as they read; whether its 1962 to 2008 peaks are the
present river's is the analysis no sentence performs. Read literally, s.3's window rules out the 18 water years since
the last raise (SF21), and s.8 no longer says the peaks are the published ones (SF22), so a rebuilt year breaks no
sentence. Every other term has a row above, each converging (asserted) or ruled out by a quotable sentence, and the
at-site fit is an easier method on the same estimand, not another reading of it.

## Oracles

None ships. Table 4 has no design discharge; no prior review, published frequency curve or certified figure ties to the
golden; Fenwick and Ashby agree with the published-record route (the back-test), not with the golden; the trend tests
pass; the asks' controls (benchmark pairs, structure shots) tie under every handling of the main call.

## Ask sheet

Two asks, both off the main call's rows: the main call reads the peak export (discharges), LS-02, SW-16-03, Table 4 and
the inventory; the asks read the two crown surveys, the benchmark list, both hourly gauge records and OP-04, and no
main-call file carries a datum, a stationing history, a clock or a survey (asserted).

- Ask A, crown settlement by reach (8 figures, 0.01 ft; maintenance program): 2016 shots against 2024 shots by
  position, every 2016 shot on today's levee paired one to one with a 2024 shot (both surveys every 100 ft), so the
  paired mean and the difference of the two surveys' reach means agree. Primary device (D7 keys): the 2016 survey is on
  the stationing used before the 2019 north tie-in moved the start 700 ft, found only from the four structures both
  surveys shot; joining by station number gives every reach 0.09 to 0.34 ft too much and every figure stays positive
  (silent). Hazard (D3): NGVD 29 against NAVD 88, +0.27 ft
  from the benchmark pairs (seen; unconverted settlement goes negative).
- Ask B, warning lead time per flood (7 figures, whole hours; closure planning): from the river reaching the Coyle
  Bridge warning level to the Orrinsford stage reaching the Main Street sill. Primary device (D2, a label stored before
  a silent switch): OP-04 (2014) files the warning level as elevation 661.00 ft NGVD 29, "21.0 ft on the gauge" on the
  gauge datum of the day; the Coyle Bridge export states today's 638.00 ft datum and its stage steps 2.00 ft against
  discharge on 22 October 2019, so the level is 23.00 ft on the gauge for every flood in the ask. Second device (D8
  clocks): the old ORF2 logger's records are CST under the export's UTC header; the two loggers ran together for three
  days in June 2021 and their records line up only at a 6 h shift, the published peak times (local standard time) sit
  on the old logger's yearly highs and 6 h before the new one's, and Coyle Bridge's hourly record tops out 6 h after
  every published Coyle Bridge time, so every route gives 6 h. Hazard (D3): the ORF2 gauge datum is on NGVD 29 and the
  sill on NAVD 88. Every lead's crossing fractions put it 0.1 to 0.4 h past the whole hour, so rounding, truncation and
  either whole-hour crossing convention agree.

| Ask | Golden | Cracker handling | Cracker figures | Cracker |
|---|---|---|---|---|
| A settlement R1 to R8 (ft) | 0.07, 0.12, 0.16, 0.21, 0.29, 0.24, 0.14, 0.09 | datum converted, joined by station number | 0.24, 0.29, 0.41, 0.30, 0.37, 0.58, 0.35, 0.28 | miss |
| B lead times, 2020 floods (h) | 37, 29, 38 | datums converted, the ORF2 clock moved 6 h, 21.0 ft as printed | 42, 33, 43 | miss |
| B lead times, 2024 to 2025 floods (h) | 38, 32, 35, 51 | same | 43, 35, 40, 58 | miss |

Mirror: off the call at rung 0, the same ask handling (nothing in the asks comes from the call): 0 of 15 ask criteria.
The re-stationer (re-stations the 2016 survey, prints 21.0 ft) keeps 8 of 15; the full includer 15 of 15 (stress
rows, not the gate). The ORF2 clock now shows in the battery (the stamps step back where the new logger starts), so
the cracker is priced as fixing it; the Coyle Bridge datum change before the 2020 floods keeps every lead off it.

Pair ceiling: 28.5 (cracker 45.0, mirror 12.0)
Mirror leakage: 0.0 per cent of the ask weight
Measured by: generator/ceiling.py on the cut pack

## Prompt

Question form `whether` (does the levee need a raise, and if so how many whole feet), second sentence opening on the
call's companions ("Alongside the call"), deliverables a workbook and a one-page memo carrying the chart; rounding in
the last sentence; no count the data hold, no persona; `voice-check.py` PASS at 993 characters.

## Leak review

`leak.py --asof 2026-11-09` on the final cut: REVIEW, no LEAK. Each REVIEW line:

- Table 4, "Main Street" beside decision words: the bridge footnote naming the two bridge cross-sections; no ranking.
- SW-16-03, 0.12, 0.14 and 0.16: the regional skews' mean square errors; they share digits with three settlement
  figures and nothing else. SW-16-03's 1.50 is the skew threshold in the mean-square-error formula, which shares digits
  with the railroad closure's shortfall.
- Table 4's discharge columns (65,000 to 155,000 by 10,000): the write-up states the rival discharges to the nearest
  100 cfs (95,400 and 104,700), so no column header repeats a stated figure.
- LS-02 carrying the call's words (raise, levee, crown, flood season): the governing standard's own subject; it states
  no figure and no direction.
- Design-note words in Table 4 (upstream, station, floods, section), LS-02 (record, published, method, nothing,
  upstream, station), OP-04 (record, upstream, gauges) and SW-16-03 (record, station, section): each document's
  ordinary vocabulary (an upstream face, the upstream freeboard allowance, the published peaks, station skew,
  calibration floods); none names the levee raises, a second gauge, a period or the record's homogeneity.
- The inventory naming three of the answer set's names beside numbers: the Structures sheet's pump stations and the
  Main Street closure with their stations; it ranks nothing on the decision question.

## Stage 4 round 1

- Judge (2026-11-01): NOT_DETERMINISTIC, SEND_BACK, the failing gates C and E; Gate G passes (nonstationary frequency,
  analytical, no surface-read dependency) and Gate H passes (domain, layers, an analytical decisive step). The brief
  carried the graded blocks inline, so the round broke derive-first and does not spend the one re-judge.
- Findings: (1) the 18 water years since the last raise met LS-02 s.2 and s.8 as written, a competing answer (1 ft);
  (2) extension forms ran 111.2k to 113.6k, the top over the bin edge; (3) the ORF2 clock offset was not forced (Coyle
  Bridge's hourly crests 3 to 5 h after the published times pointed at 4 h); (4) "whole hours" admitted truncation;
  (5) reach descriptors with no shipped source, and the surveys' reach means differing from the paired figure.
- Leak reader: question 6 read "mostly rule application, with one analytical judgement left (record homogeneity)";
  realism tells in Table 4's uniform fall, the smooth crown and the inspection summary.
- Repair (generator, one pass): LS-02 s.3 files the window ("one annual peak discharge for every water year since the
  Orrinsford gauge opened in water year 1962") and s.8 the source only ("Discharges are taken from the State Water
  Survey's published records; the district's loggers record stage for flood warning only"); the relation steadier and
  the design discharge centred (six forms 110,260 to 110,477, every chance 0.027 or more inside its bin); published
  peak times set from the agency's own hourly crests, the two ORF2 loggers overlapping three days, all three clock
  routes at 6 h; every lead's fraction 0.1 to 0.4 h; reach descriptors dropped, both surveys every 100 ft with a 700 ft
  realignment; Table 4 with reach slopes and cross-section effects, the crown with low spots, a tie-in step and a level
  floodwall top, the inspection a ratings report; the Coyle Bridge datum change moved to October 2019 and the sill to
  616.95 ft. The Three rules lines say why the window is a WHAT and the homogeneity judgement stays the decisive step.

## Build record

Round 1 repair green on 2026-11-01, every gate on the final cut (`target.zip` sha256 81bc1b755d580b192f921eeca93774a96b9c50081276155baa0c8a09fa54be99):

- Generator: `generator/build.py` builds twice from the fixed seeds, byte-identical over 17 files, and installs
  `target/`, `golden/`, `metadata.json`, `generator/figures.json` and `target.zip`; `generator/writeup.py` then emits
  `submission.md` from `figures.json`.
- `checks.py` 102 of 102 (the ladder and the Gate F count; each of the six relation forms and the seven stress rows in
  every graded bin; SF1 to SF22; R1 to R3c on the clean truth; Layer 1 neutrality; the three ORF2 clock routes at 6 h;
  rounding, truncation and both crossing conventions agreeing; one-to-one survey pairing; separation, input gates,
  realism sweep, distractor deletion); `verify.py` 30 of 30 on its own readers; `figures_check.py` 81 of 81;
  `precut.py` 61 checks, 0 FAIL, 0 WARN; `voice-check.py` PASS at 999 characters.
- Pack: 13 files in three formats (seven CSV, five PDF, one XLSX); the largest `SWS_05432100_hourly_WY2017-2026.csv`
  at 87,635 rows; distractors `coop_daily_precip_Orrinsford_Coyle.csv` and `OLDD_2025_annual_inspection_summary.pdf`.
- `leak.py --asof 2026-11-09` REVIEW, no LEAK (each line answered in `## Leak review`); `guard.py heart` WARN
  (repeat.gate_g, repeat.question_form), no BLOCK; `guard.py check` on the registered card WARN only; `guard.py
  surface` below.
- Ceiling (`generator/ceiling.py`): pair 28.5, mirror leakage 0.0 per cent.

## Architecture 1 record`; its card identity is in the card's `lineage`. Seed FC09 numbered the slot; nothing of its
world, decision or quantity is used here beyond the objective.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task138.json`, architecture v2, registered 2026-11-01T17:20:03Z; `guard.py check` WARN only (repeat.gate_g, repeat.question_form; NOTEs differentiated against task104, task171 v5, task168); re-checked on the registered card as the draw's last act |
| Domain / task type | physical-environmental-sciences / hydrology-flood-frequency (client domain physical-environmental-sciences; the task type serves Forecasting): the 1 per cent annual chance flood at a gauged town, carried through the hydraulic model to a levee crown |
| Objective | Forecasting & Predictive Modeling: the flood the levee must hold in the years after the review, the 1 per cent annual chance peak at Orrinsford for the river as it now runs, a window not yet open |
| Shape | 04 (setting one dial): the uniform crown raise 0 to 4 ft, each setting with the discharge it holds and its annual chance (5 graded figures), the call (1) and the design discharge (1); asks A (crown settlement, eight reaches) and B (warning lead time, seven floods); the chart with named parts (frequency curve, record curve, five capacity lines, the 1 per cent line, about 5); the two files (2): about 27 criteria |
| Decision | `dial_setting`, answer unit `count` (whole feet of crown raise) |
| Mechanism | gap population then time (the flood population the record samples is not the river's present one, and the change is dated by the levee raises); pattern none; generators G16 then G6; Gate G `forecasting`; layer 2 family `field_method`, pattern `own:post-raise-two-gauge-record-extension`; strategy `other` |
| Furniture | forum `trustees_or_governors` (the district's Board of Trustees adopts the capital plan), forcing event `budget_or_appropriation` (the 2027 capital plan), org family `utility_or_infrastructure` (a levee and drainage district), role family `policy_adviser` (the district engineer reviews the levee against the district's standard), context artifact `published_series` (the State Water Survey's annual peak export), calibration none, question form `whether` |
| World | Orrinsford, a fictional Midwestern river town on the Tamsen River; the Orrinsford Levee and Drainage District (OLDD); the State Water Survey's gauges at Coyle Bridge (RM 41.0, 4,930 sq mi) and Orrinsford (RM 12.6, 6,480 sq mi); the State Department of Natural Resources' levee inventory; six agricultural levee districts on the 28 miles between the gauges, raised to the 1 per cent flood between 1996 and 2008 |
| Spine | `SWS_05432100_hourly_WY2017-2026.csv`, 87,635 hourly rows at Coyle Bridge (ask B); the main call's record is the annual peak export (280 rows, five gauges) |
| Deliverables | `levee_raise_review.xlsx` (raise options, the present-river series and fit, settlement by reach, closure lead times), `levee_raise_memo.pdf` (one page to the Board with the frequency chart) |
| People | `guard.py names --geo US --seed 138`: Dennis Zhang (district engineer, LS-02 and OP-04), Kristin Lucas (land surveyor, both crown surveys), Eric Thornton (State Water Survey hydrologist, the skew release), Jesus Hernandez (hydraulic engineer, the 2019 update); none appears in the prompt |
| As of | 9 November 2026 (the district engineer's review for the 2027 capital plan) |

**Candidates screened before this one** (each in `## Tried and rejected`): TV audience flow after a lead-in change
(spent, task115 and task174), hospital weekend discharges (spent, task127 and task170), a gauge rating drifting with
channel aggradation, rating hysteresis on the rising and falling limbs (spent at the abstraction test, task279), a
reservoir regulating the flood record, landfill airspace with waste settlement. `guard.py slots` on the chosen
mechanism's nouns (levee floodplain, attenuation storage) and its setting's (levee raise, flood frequency, Bulletin)
returned no slot.

**Data-native sentence.** Orrinsford's own annual peak record holds two rivers: until the last of six agricultural levees
between the gauges was raised (in force from water year 2009) the floodplain behind them filled in every flood above
about 46,000 cfs at Coyle Bridge and cut the town's peak, so the record's two great floods (1970 and 1973, Orrinsford at
0.71 and 0.80 of Coyle Bridge against 1.064 since 2009) are smaller than today's river would make them, while every smaller flood, most of the
record, is untouched; the change lives only in the upper tail the 1 per cent flood is read from, leaves no trend or
step, and shows only against a second gauge above the reach.

**Abstraction test.** Stripped of nouns: the deciding quantity is an upper quantile of a long record whose largest
members were produced under a regime that ended part way through, a regime that never touched the ordinary members,
and it is recovered by carrying a second, unaffected long record across at the relation the two show since the regime
ended. The nearest drivers on file (task104, task171 v5, task168) recover a level, a rate or a share, not a tail
quantile of a non-homogeneous record; differentiated on the card.

## Survivor anatomy

- Actor: the deciding property, whether a year's Orrinsford peak was cut by upstream floodplain storage that no longer exists, has no column anywhere: the peak export carries discharges, the inventory carries each segment's raise year, and the property is the relation between the two gauges' peaks in the years before and after those raises.
- Link: the comparison of Orrinsford's peaks against Coyle Bridge's by water year, split at the in-force year of the raises on the segments between the two gauges' river miles (inventory Segments and Gauges sheets), which LS-02's frequency method never asks for; no key, code or sentence ties the raise years to the peak record.
- Reflex: LS-02's own method (log-Pearson Type III by moments with the weighted skew) fitted to the Orrinsford record as published, which meets its window of one peak for every water year since 1962, is rung 0 and files no raise (95,430 cfs, 0 ft).
- Back-test: the textbook route validates: Mann-Kendall p 0.43 and Pettitt p 0.73 on the record, no Bulletin 17B low outlier, the agency's peak codes flag nothing at Orrinsford, and Fenwick downstream (100,192 cfs at site) agrees with the town.
- Second use: every file the decisive step reads is in the pack for its own reason: the peak export is the record LS-02 fits and carries the whole basin as the agency exports it; the inventory carries the town levee's crown at the model cross-sections and its bridge closures, which the crown check needs, beside every other segment.
- Shock: the movement reads as ordinary hydrology: big floods smaller downstream through floodplain storage is textbook, the town record has no trend, step or outlier, and the two low ratios sit among 65 years of ratios near 1.06; the golden's answer is not an interval of any sort of the gauges or years.
- Pins: LS-02 section 2 files the WHAT (the 1 per cent flood at the Orrinsford gauge "for the river, its floodplain and its levees as they stand at the time of the review") and section 3 its window (one annual peak for every water year since the gauge opened in 1962); no filed sentence names the upstream raises, the record's homogeneity, a second gauge or a relation, and the published record meets both sentences as they read, so the pins do not hand the step over.

## Default path

1. Read LS-02: the design flood is the 1 per cent annual chance peak at the Orrinsford gauge, fitted as log-Pearson Type III by moments with the station skew weighted with the SW-16-03 regional skew (region 2, -0.08, mean square error 0.14).
2. Take the 65 Orrinsford annual peaks from the State Water Survey export (one for every water year 1962 to 2026, the window LS-02 section 3 sets, the provisional 2026 included) and fit: mean of logs 4.4734, standard deviation 0.2089, station skew 0.281, weighted skew 0.133; the 1 per cent discharge is 95,430 cfs.
3. Check the record before trusting it: Mann-Kendall (p 0.43) and Pettitt (p 0.73) find no trend or change point; no low outlier.
4. Read Table 4 at that discharge (linear in discharge), add LS-02 freeboard (3.0 ft, 4.0 ft within 100 ft of a bridge, plus the upstream allowance) and compare with the 2024 crown at the 21 cross-sections: the worst, the railroad closure at 118+70, has 1.16 ft to spare.
5. File no raise; each raise's annual chance of exceeding what it holds is 0.7, 0.5, 0.4, 0.3 and 0.2 per cent.

Ends on: no raise (0 ft), design discharge 95,000 cfs.
Golden: raise 2 ft, design discharge 110,000 cfs.

## Stump sentence

The default path fits LS-02's frequency curve to Orrinsford's record as published and files no raise (0 ft, a 95,000 cfs
design flood) because it never asks whether the 1962 to 2008 peaks belong to the river as it now runs: the six levees
between Coyle Bridge and Orrinsford, all raised by October 2008, no longer let their floodplains take the top off a big
flood, which shows only when Coyle Bridge's record is set against the raise years; rebuilt for the present river the
design flood is 110,000 cfs and the crown needs 2 ft.

## Three rules

Task type: hydrology-flood-frequency, the 1 per cent annual chance flood estimated from a gauged annual peak record and carried to a design level, a task type that serves Forecasting.
Domain test: the deciding quantity is the 1 per cent annual chance peak discharge at the Orrinsford gauge, estimated the field's way with a log-Pearson Type III frequency curve (moments on logs, weighted skew, the Bulletin 17 family) and read through the hydraulic model's water surfaces to the crown with freeboard.
Swap: "Does the warehouse need a bigger dock to meet its standard against its 1 per cent busiest day, now that its suppliers' depots were enlarged?" stops making sense: there is no stage at which upstream storage starts to fill, no peak cut only above it, and no second meter above the reach whose relation changes when the storage is gone.
Layer 1: the agency's export lists each annual peak by date with no water year column (Oct to Dec peaks belong to the next water year), three significant figures, a provisional 2026 approval code, estimate codes and gaps on the other gauges; Table 4 sits in the consultant's PDF with station strings; the DNR inventory reports raises as the sponsors wrote them ("Oct 1998", "2003-11", "Sept 2005"); the asks' telemetry, surveys and benchmarks carry two vertical datums, a re-stationed levee, a gauge datum change and a logger clock change (ask devices, ledgered).
Layer 2: family field_method, record homogeneity: a flood frequency curve assumes its record is one population of floods under the conditions the estimate is for; upstream levee raises broke that for the large floods only, and the field's remedy (adjusting the record to present conditions through a long-record gauge above the change) has to be built from the two gauges.
Decisive step: recognising that the Orrinsford peaks before water year 2009 belong to a river whose upstream floodplain still held back big floods, so the published record is not homogeneous with the river as it now runs, and carrying Coyle Bridge's long record across at the relation the two gauges show since the last levee raise.
Not semantics: every field, code, unit and definition read correctly (water years, approval codes, three-figure peaks, Table 4, LS-02's freeboard and skew rules) still gives 0 ft on the published record; nothing in any field marks the attenuated years, and the agency's codes say nothing about them.
Not rule application: the filed rules fix the WHAT (s.2, the river as it stands; s.3, one peak for every water year since 1962) and the method, and the published record satisfies both as they read, so LS-02 executed word for word files 0 ft; no rule says the 1962 to 2008 peaks are not the present river's or how to rebuild them. The window rules out the shortcut that keeps only the 18 water years since the last raise, and it does not name the rebuild. The enumerated family (the at-site fit, post-raise years only, whole-record relation, Coyle Bridge unscaled, since 1994, drainage-area ratios at 0.5 to 1.0) spreads 93,473 to 136,398 cfs, 0 to 6 ft; the standing family once the raises are seen (13 constructions: six relation forms fitted over 2009 to 2026, the inverted regression, mean of ratios, three fitting windows, carrying only the pre-raise years, keeping larger observed peaks) spreads 109,813 to 110,527 cfs, every member 2 ft with the same five chances; the ruling-out is quiet, two ratios out of 65 visible only with both gauges side by side by water year.
Analyst test: a strong analyst who reads every rule, takes LS-02's window as given (one published peak for every water year since 1962) and fits its frequency curve to the Orrinsford record as published, after homogeneity tests that pass, files no raise (0 ft) with a 95,000 cfs design flood; the window is a WHAT (which years the record covers), and judging whether those years' peaks are the present river's is the decisive analysis it leaves open.
Estimand: LS-02 section 2 (`OLDD_LS-02_levee_standard_rev3.pdf`): the peak discharge at the Orrinsford gauge with a 1 per cent chance of being exceeded in any year, for the river, its floodplain and its levees as they stand at the time of the review, fitted (section 3) to one annual peak discharge for every water year since the gauge opened in water year 1962, discharges from the State Water Survey's records (section 8); the crown is the latest certification survey's (section 6) and a raise is uniform in whole feet (section 7). The window is part of the WHAT: it says which years the present-river record covers, never how a year's present-river peak is found.
No decoy: nothing is planted: no memo, prior review, published design flood or stakeholder figure ships; the hydraulic study gives water surfaces by discharge and no design discharge; the raise years are the sponsors' own inventory entries.
No certified replay: no certified design discharge, frequency curve or prior review ships, so the method is never recovered by matching published figures; LS-02 files the frequency method openly and the record's construction is the analysis.
Lesson: an at-site flood frequency curve is only as good as the homogeneity of its record, and upstream flood-control works change its upper tail without leaving a trend; the check is a second gauge set against the works' in-force dates; no build on file teaches record homogeneity broken by upstream floodplain storage (`guard.py slots` returns nothing on levee, floodplain or attenuation).

**Layer 1 inventory** (each asserted neutral in `checks.py`, L1 and SF rows):

| Item | System that writes it | File | Natural mishandling | Effect |
|---|---|---|---|---|
| Peaks by date, no water year column | SWS peak export | annual peaks CSV | label by calendar year | same call and bin (SF8) |
| Published peak times in local standard time | SWS peak export | annual peaks CSV | read as UTC | ask B only (the clock routes) |
| Provisional WY2026 | SWS approval workflow | annual peaks CSV | drop it | same call and bins (SF12) |
| Estimate codes, missing years | SWS records at Ashby, Gale Creek, Fenwick | annual peaks CSV | none on the main gauges | none (SF13) |
| Table 4 in a PDF, station strings | consultant's report | Table 4 PDF | parse error | asserted read (L1) |
| Raise dates in the sponsors' words | DNR inventory | inventory XLSX | read "Oct 2008" as WY2008 | same call and bin (SF14) |
| NGVD 29 survey and gauge datums | the 2016 surveyor, the ORF2 logger header | 2016 survey, ORF2 export | not converted | ask A and B only (ledgered) |
| Levee re-stationed in 2019 | the 2019 tie-in project | 2016 survey | join by station number | ask A only (device) |
| Coyle Bridge gauge datum lowered October 2019 | SWS field office | Coyle hourly, OP-04 | 21.0 ft throughout | ask B only (device) |
| The old ORF2 logger's records in CST, three days beside the new one | the old and new loggers | ORF2 export | read as UTC | ask B only (device) |

## Readability screen

| Rung | Column or one join | Field reflex | Named in a document | Helper narration | Largest anomaly | File read only by it | Verdict |
|---|---|---|---|---|---|---|---|
| Rung 0, LS-02 fit to the published record | the record is the column | yes, the reflex | LS-02 sections 2 and 3 | none | no | no | readable |
| Rung 1, homogeneity tests | one series | yes (Bulletin 17C advises it) | no | SW-16-03's generic limitation line | no | no | readable |
| Rung 2, post-raise years only | needs the raise years | no | no | none | no | no | silent |
| Rung 3, Coyle Bridge at the whole-record relation | one join by water year | partly (record extension) | no | none | no | no | silent |
| Decisive, the present river rebuilt from Coyle Bridge at the post-raise relation (decisive) | no column; two files joined by water year and split by in-force years from a third sheet | no | no | none | no (two ratios among 65) | no (the inventory and the Coyle Bridge rows each have their own use) | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | design flood | 1 per cent annual chance peak at Orrinsford for the river as it now runs, over one peak for every water year since 1962 | 1 per cent of the published record as it stands | 0 ft | LS-02 s.2 and s.3 file the estimand and its window; the published record is an easier method on the same estimand, not another reading |
| SF2 | annual chance per raise | exceedance of the discharge the raised levee holds with freeboard | exceedance of the discharge held to the crown | figures move | the prompt's "with its freeboard" and LS-02 s.7 |
| SF3 | crown | the 2024 certification survey (the inventory's crown sheet equals it at all 21 cross-sections) | the 2016 survey, or the 2024 crown less projected settlement | 2 ft either way | LS-02 s.6, "the latest certification survey"; asserted 2 ft with three more years of settlement |
| SF4 | where the crown is checked | the 21 cross-sections of Table 4 | every 50 ft survey shot | same raise and bins | asserted (same call) |
| SF5 | 4 ft freeboard | within 100 ft of a bridge or closure | only at the bridge stations | same call | no other cross-section within 100 ft (asserted) |
| SF6 | Table 4 interpolation | linear in discharge | log-linear | same raise and bins | LS-02 s.4; asserted same |
| SF7 | which stations are bridges | 62+40 and 118+70 | none | same call | inventory Structures and the Table 4 marks agree (asserted) |
| SF8 | annual peak year | water year | calendar year labels, or calendar-year maxima | same call and bin; maxima drop water years' peaks | asserted; LS-02 s.3 (one peak for every water year) |
| SF9 | raise | uniform, whole feet | fractional or local raises | not an option | LS-02 s.7 |
| SF10 | regional skew | region 2, -0.08 and 0.14 (Pell and Marrow counties) | another region | not licensed | SW-16-03 Tables 1 and 2 |
| SF11 | 1 per cent | annual exceedance probability 0.01 | none | same call | LS-02 s.2 |
| SF12 | provisional 2026 | included | dropped | same call and bins | asserted |
| SF13 | estimate codes | on other gauges only | dropping estimated years | same call | asserted (no code at Orrinsford or Coyle Bridge) |
| SF14 | first fully raised year | water year 2009 (raise reported Oct 2008) | 2008 | same call and bin | asserted |
| SF15 | skew used | weighted | station skew only | 4 ft | LS-02 s.3 files the weighting |
| SF16 | upstream allowance | 0.5 ft at 0+00 to nothing at 180+00 | none | figures move | LS-02 s.5 |
| SF17 | ask A points | crown shots matched by position (every 2016 shot on today's levee pairs one to one with a 2024 shot), structures in or out | structures included; median per reach; the difference of the two surveys' reach means | same bins | asserted |
| SF18 | ask B crossing time and rounding | interpolated within the hour, rounded | first hour at or above, last hour below, truncation | same whole hours (every lead's fraction 0.1 to 0.4) | asserted |
| SF19 | ask B floods | every rise of the Orrinsford stage through the Main Street sill since October 2016 | none | seven floods | asserted |
| SF20 | ask A datum | NAVD 88 = NGVD 29 + 0.27 at every district benchmark | averaging a subset | same | every pair gives 0.27 (asserted) |
| SF21 | which years | one annual peak for every water year 1962 to 2026 | only the 18 water years since the last raise (104,714 cfs, 1 ft) | 1 ft | LS-02 s.3, "every water year since the Orrinsford gauge opened in water year 1962" |
| SF22 | records | discharges from the State Water Survey's published records | every year's peak used as published | 0 ft | LS-02 s.8 names the source, not the years' values; s.2 sets the river they describe (asserted: no sentence says the peaks are the published ones) |

## Ladder

| Rung | Construction | Design discharge (cfs) | Raise | Annual chance by raise 0 to 4 ft (%) |
|---|---|---|---|---|
| 0 | LS-02 fit to the published Orrinsford record, 1962 to 2026 | 95,430 (95,000) | 0 ft | 0.71, 0.54, 0.41, 0.31, 0.24 |
| 1 | rung 0 after Mann-Kendall (p 0.43) and Pettitt (p 0.73) | 95,430 | 0 ft | as rung 0 |
| 2 | only the 18 water years since the last raise (outside LS-02 s.3's window) | 104,714 (105,000) | 1 ft | 1.13, 0.89, 0.70, 0.56, 0.45 |
| 3 | Coyle Bridge's record at the whole-record relation (0.969) | 100,546 (100,000) | 0 ft | 0.94, 0.75, 0.59, 0.47, 0.38 |
| golden | Orrinsford from 2009, Coyle Bridge x 1.064 (the 2009 to 2026 relation through the origin) before | 110,403 (110,000) | 2 ft | 1.40, 1.12, 0.90, 0.72, 0.58 |
| off | Coyle Bridge unscaled | 103,772 | 1 ft | |
| off | Orrinsford since 1994 | 93,473 | 0 ft | |
| off | drainage-area ratio at 0.5, 0.7, 1.0 | 118,971, 125,658, 136,398 | 3, 5, 6 ft | |

The relation's form, every one fitted over water years 2009 to 2026 and applied to 1962 to 2008 (asserted per form in
`checks.py`; tightest margin of any chance to its one-decimal edge, the design discharge's margin to 107,500 or
112,500):

| Form | Design discharge (cfs) | Chances by raise 0 to 4 ft (%) | Tightest chance margin | Discharge margin |
|---|---|---|---|---|
| through the origin (golden) | 110,403 | 1.401, 1.118, 0.896, 0.721, 0.583 | 0.029 | 2,097 |
| ratio of means | 110,477 | 1.405, 1.121, 0.899, 0.723, 0.585 | 0.027 | 2,023 |
| straight line (OLS) | 110,260 | 1.394, 1.112, 0.891, 0.717, 0.579 | 0.029 | 2,240 |
| straight line in logs | 110,359 | 1.399, 1.116, 0.895, 0.720, 0.582 | 0.030 | 2,141 |
| MOVE.1 in logs | 110,372 | 1.400, 1.117, 0.895, 0.720, 0.582 | 0.030 | 2,128 |
| every year from Coyle Bridge at the ratio | 110,445 | 1.403, 1.120, 0.898, 0.723, 0.584 | 0.028 | 2,055 |

Stress rows (mean of ratios, the inverted regression, fitting from 2008, 2010 or 2012, carrying only the pre-raise
years, keeping a larger observed peak) stay in every bin, tightest 0.019. Shortfall at 118+70 under the golden 1.50 ft
(the railroad closure governs every raise; Main Street 62+40 is next at 0.77 ft). Gate F count on the clean truth and
the pack: no cheap route files 2 ft (asserted).

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | the river as it now runs (LS-02 s.2, filed) over one peak for every water year since 1962 (s.3, filed); whether a year's published peak is the present river's is the analysis; every relation form converges (C1 over six forms and seven stress rows) |
| 2 | Unit of account | the annual peak at one gauge; the raise in whole feet (filed) |
| 3 | Attribution window | water year (C1: calendar labels give the same call and bin) |
| 4 | As-of dating | the review date; the record through water year 2026 (C1 with or without the provisional year) |
| 5 | Version basis | discharges from the State Water Survey's records (LS-02 s.8), the provisional 2026 included (C1); the latest certification survey (s.6) |
| 6 | Denominator | none in the main call; ask A averages matched shots per reach (C1 with structures) |
| 7 | Weighting | moments on logs, equal years (filed method) |
| 8 | Window length | every water year since the gauge opened in 1962 (LS-02 s.3, filed, which rules out the 18-year fit, SF21); the relation's fitting window converges 2008 to 2012 (C1) |
| 9 | Boundary inclusivity | the in-force year (Oct 2008 raise, WY2009); C1 with 2008 |
| 10 | Rounding path | figures computed unrounded, rounded once at the end (prompt) |
| 11 | Tie-break | none arises (asserted margins) |
| 12 | Maturity and censoring | no censored peaks; no low outlier (asserted) |
| 13 | Order of operations | fit, then quantile, then Table 4, then freeboard; commuting |
| 14 | Row order | none (sorted by water year; sums) |
| 15 | Duplicate resolution | one peak per gauge and water year (asserted unique) |
| 16 | Identity normalisation | site numbers; ask A structures matched by name across surveys (asserted one offset) |
| 17 | Netting against gross | none |
| 18 | Dimensional units | cfs, ft NAVD 88; ask datums converted by the benchmark pairs (C4 for the ask, asserted) |
| 19 | Code and status semantics | approval and estimate codes neutral (asserted) |
| 20 | Integerisation | the raise is the smallest whole foot clearing the shortfall (filed) |
| 21 | Clause scope | LS-02 freeboard rules scope to cross-sections (s.6) |
| 22 | Forward window contents | the design flood is a property of the present river; the record through 2026 is the driver, nothing past it is needed |

## Literal reader

Executed word for word, LS-02 sections 2 to 8 on the shipped files ask for the 1 per cent flood of the river as it
stands, fitted to one annual peak for every water year since 1962, with discharges from the State Water Survey's
records. The published record meets the window and the source as they read; whether its 1962 to 2008 peaks are the
present river's is the analysis no sentence performs. Read literally, s.3's window rules out the 18 water years since
the last raise (SF21), and s.8 no longer says the peaks are the published ones (SF22), so a rebuilt year breaks no
sentence. Every other term has a row above, each converging (asserted) or ruled out by a quotable sentence, and the
at-site fit is an easier method on the same estimand, not another reading of it.

## Oracles

None ships. Table 4 has no design discharge; no prior review, published frequency curve or certified figure ties to the
golden; Fenwick and Ashby agree with the published-record route (the back-test), not with the golden; the trend tests
pass; the asks' controls (benchmark pairs, structure shots) tie under every handling of the main call.

## Ask sheet

Two asks, both off the main call's rows: the main call reads the peak export (discharges), LS-02, SW-16-03, Table 4 and
the inventory; the asks read the two crown surveys, the benchmark list, both hourly gauge records and OP-04, and no
main-call file carries a datum, a stationing history, a clock or a survey (asserted).

- Ask A, crown settlement by reach (8 figures, 0.01 ft; maintenance program): 2016 shots against 2024 shots by
  position, every 2016 shot on today's levee paired one to one with a 2024 shot (both surveys every 100 ft), so the
  paired mean and the difference of the two surveys' reach means agree. Primary device (D7 keys): the 2016 survey is on
  the stationing used before the 2019 north tie-in moved the start 700 ft, found only from the four structures both
  surveys shot; joining by station number gives every reach 0.09 to 0.34 ft too much and every figure stays positive
  (silent). Hazard (D3): NGVD 29 against NAVD 88, +0.27 ft
  from the benchmark pairs (seen; unconverted settlement goes negative).
- Ask B, warning lead time per flood (7 figures, whole hours; closure planning): from the river reaching the Coyle
  Bridge warning level to the Orrinsford stage reaching the Main Street sill. Primary device (D2, a label stored before
  a silent switch): OP-04 (2014) files the warning level as elevation 661.00 ft NGVD 29, "21.0 ft on the gauge" on the
  gauge datum of the day; the Coyle Bridge export states today's 638.00 ft datum and its stage steps 2.00 ft against
  discharge on 22 October 2019, so the level is 23.00 ft on the gauge for every flood in the ask. Second device (D8
  clocks): the old ORF2 logger's records are CST under the export's UTC header; the two loggers ran together for three
  days in June 2021 and their records line up only at a 6 h shift, the published peak times (local standard time) sit
  on the old logger's yearly highs and 6 h before the new one's, and Coyle Bridge's hourly record tops out 6 h after
  every published Coyle Bridge time, so every route gives 6 h. Hazard (D3): the ORF2 gauge datum is on NGVD 29 and the
  sill on NAVD 88. Every lead's crossing fractions put it 0.1 to 0.4 h past the whole hour, so rounding, truncation and
  either whole-hour crossing convention agree.

| Ask | Golden | Cracker handling | Cracker figures | Cracker |
|---|---|---|---|---|
| A settlement R1 to R8 (ft) | 0.07, 0.12, 0.16, 0.21, 0.29, 0.24, 0.14, 0.09 | datum converted, joined by station number | 0.24, 0.29, 0.41, 0.30, 0.37, 0.58, 0.35, 0.28 | miss |
| B lead times, 2020 floods (h) | 37, 29, 38 | datums converted, the ORF2 clock moved 6 h, 21.0 ft as printed | 42, 33, 43 | miss |
| B lead times, 2024 to 2025 floods (h) | 38, 32, 35, 51 | same | 43, 35, 40, 58 | miss |

Mirror: off the call at rung 0, the same ask handling (nothing in the asks comes from the call): 0 of 15 ask criteria.
The re-stationer (re-stations the 2016 survey, prints 21.0 ft) keeps 8 of 15; the full includer 15 of 15 (stress
rows, not the gate). The ORF2 clock now shows in the battery (the stamps step back where the new logger starts), so
the cracker is priced as fixing it; the Coyle Bridge datum change before the 2020 floods keeps every lead off it.

Pair ceiling: 28.5 (cracker 45.0, mirror 12.0)
Mirror leakage: 0.0 per cent of the ask weight
Measured by: generator/ceiling.py on the cut pack

## Prompt

Question form `whether` (does the levee need a raise, and if so how many whole feet), second sentence opening on the
call's companions ("Alongside the call"), deliverables a workbook and a one-page memo carrying the chart; rounding in
the last sentence; no count the data hold, no persona; `voice-check.py` PASS at 993 characters.

## Leak review

`leak.py --asof 2026-11-09` on the final cut: REVIEW, no LEAK. Each REVIEW line:

- Table 4, "Main Street" beside decision words: the bridge footnote naming the two bridge cross-sections; no ranking.
- SW-16-03, 0.12, 0.14 and 0.16: the regional skews' mean square errors; they share digits with three settlement
  figures and nothing else. SW-16-03's 1.50 is the skew threshold in the mean-square-error formula, which shares digits
  with the railroad closure's shortfall.
- Table 4's discharge columns (65,000 to 155,000 by 10,000): the write-up states the rival discharges to the nearest
  100 cfs (95,400 and 104,700), so no column header repeats a stated figure.
- LS-02 carrying the call's words (raise, levee, crown, flood season): the governing standard's own subject; it states
  no figure and no direction.
- Design-note words in Table 4 (upstream, station, floods, section), LS-02 (record, published, method, nothing,
  upstream, station), OP-04 (record, upstream, gauges) and SW-16-03 (record, station, section): each document's
  ordinary vocabulary (an upstream face, the upstream freeboard allowance, the published peaks, station skew,
  calibration floods); none names the levee raises, a second gauge, a period or the record's homogeneity.
- The inventory naming three of the answer set's names beside numbers: the Structures sheet's pump stations and the
  Main Street closure with their stations; it ranks nothing on the decision question.

## Stage 4 round 1

- Judge (2026-11-01): NOT_DETERMINISTIC, SEND_BACK, the failing gates C and E; Gate G passes (nonstationary frequency,
  analytical, no surface-read dependency) and Gate H passes (domain, layers, an analytical decisive step). The brief
  carried the graded blocks inline, so the round broke derive-first and does not spend the one re-judge.
- Findings: (1) the 18 water years since the last raise met LS-02 s.2 and s.8 as written, a competing answer (1 ft);
  (2) extension forms ran 111.2k to 113.6k, the top over the bin edge; (3) the ORF2 clock offset was not forced (Coyle
  Bridge's hourly crests 3 to 5 h after the published times pointed at 4 h); (4) "whole hours" admitted truncation;
  (5) reach descriptors with no shipped source, and the surveys' reach means differing from the paired figure.
- Leak reader: question 6 read "mostly rule application, with one analytical judgement left (record homogeneity)";
  realism tells in Table 4's uniform fall, the smooth crown and the inspection summary.
- Repair (generator, one pass): LS-02 s.3 files the window ("one annual peak discharge for every water year since the
  Orrinsford gauge opened in water year 1962") and s.8 the source only ("Discharges are taken from the State Water
  Survey's published records; the district's loggers record stage for flood warning only"); the relation steadier and
  the design discharge centred (six forms 110,260 to 110,477, every chance 0.027 or more inside its bin); published
  peak times set from the agency's own hourly crests, the two ORF2 loggers overlapping three days, all three clock
  routes at 6 h; every lead's fraction 0.1 to 0.4 h; reach descriptors dropped, both surveys every 100 ft with a 700 ft
  realignment; Table 4 with reach slopes and cross-section effects, the crown with low spots, a tie-in step and a level
  floodwall top, the inspection a ratings report; the Coyle Bridge datum change moved to October 2019 and the sill to
  616.95 ft. The Three rules lines say why the window is a WHAT and the homogeneity judgement stays the decisive step.

## Build record

Stage 3 green on 2026-11-01, every gate on the final cut (`target.zip` sha256 1ceb11827588fdf4f589d1e172de81bffee0faf53c815e0781a3d2d7a6a785f6):

- Generator: `generator/build.py` builds twice from the fixed seeds, byte-identical over 17 files, and installs
  `target/`, `golden/`, `metadata.json`, `generator/figures.json` and `target.zip`; `generator/writeup.py` then emits
  `submission.md` from `figures.json`.
- `checks.py` 88 of 88 (ladder and Gate F count, the golden family over 12 constructions and every graded bin, SF1 to
  SF20, R1 to R3c on the clean truth, Layer 1 neutrality, both asks' devices and conventions, separation, input gates,
  realism sweep, distractor deletion); `verify.py` 28 of 28 on its own readers (csv, zip and xml, its own PDF stream
  decoder, a gamma-based log-Pearson III); `figures_check.py` 80 of 80; `precut.py` 61 checks, 0 FAIL, 0 WARN;
  `voice-check.py` PASS at 999 characters.
- Pack: 13 files in three formats (seven CSV, five PDF, one XLSX); the largest `SWS_05432100_hourly_WY2017-2026.csv`
  at 87,635 rows; distractors `coop_daily_precip_Orrinsford_Coyle.csv` and `OLDD_2025_annual_inspection_summary.pdf`
  (deleting both leaves every graded figure, asserted).
- `leak.py --asof 2026-11-09` REVIEW, no LEAK (each line answered in `## Leak review`); `guard.py heart` WARN
  (repeat.gate_g, repeat.question_form; NOTEs differentiated against task104, task171 v5, task168), nearest driver
  0.07; `guard.py surface` exit 0, five pairs promoted for the author's adjudication (task136 and task139 on the
  consecutive-build surface percentile at 0.100, task171, task168 and task104 on the card axes the card already
  differentiates), personas in the pack all the card's; `guard.py check` on the registered card WARN only.
- Ceiling (`generator/ceiling.py`): pair 28.5, mirror leakage 0.0 per cent.

## Architecture 1 record (shipped 2026-10-15, re-rooted 2026-11-01)

- Draw: the Kestrel Bend Irrigation District's 2027 season order from the Tolan Valley Project (California),
  physical-environmental-sciences / hydrology-flood-frequency, shape 13, question form how-much; the order at the
  headgate requirement covered in 24 of 30 replayed weather seasons through a daily root-zone balance of each field.
- Round 3 golden: 212,000 acre-feet, each replay started from the root-zone state the 2026 record leaves at the
  efficiency the soil moisture network's season shows; default path 215,000 (the record run at Table 4's design
  efficiency). Rounds 1 and 2 are in the lines below (round 1 weak on the 10/10 audit, round 2 read as rule
  application).
- Build: shipped 2026-10-15 (19 files in `target.zip`, 2,541,365 bytes, sha256 50c887dc), determinism and leak reports
  kept with the `_arch1` suffix.
- Fate: no portal result; re-rooted 2026-11-01 at the Batch 3 queue reset (one architecture per world: the
  irrigation-district world is closed); its card identity is in the v2 card's `lineage`.

## Tried and rejected

- The seed's loss-per-refill mixture (fill per refill plus seepage per wetted day, recovered from the 270 closed lateral
  balances): the same driver as task67 (a fixed-plus-variable cost carried per unit onto a denser period), and its
  dry-out gap was a rule recovered from a closed corpus; dropped at the draw.
- Seed 1380202 for the world: the setting year was the same on every rung, so the setting year and its requirement
  carried nothing; moved to 1380206.
- Six-inch flashboards with the board height in the structures sheet: the bare-crest spill exceeded a lateral's whole
  measured loss, so the device announced itself; cut to 2-inch boards whose height is only in the riders' remarks.
- Planning tables with even last digits (root depths in whole feet, allowable depletion fractions of 0.50): replay days
  landed exactly on an allowable depletion in most weather years, so the irrigation test was settled by floating-point
  noise and several monthly figures moved between the two tie-breaks; Tables 2 and 3 re-cut so every allowable
  depletion is an odd number of hundred-thousandths of an inch (asserted), and the walnut June coefficient set at 1.11
  to keep the months clear of their rounding edges.
- One WOP 2.4 sentence stating that a replay starts from each field's depletion at the end of 31 January, carried from
  its last delivered 2026 set (the judge's optional hardening, 12 October): refused. It names the decisive rung and
  pins the method, turning R3 into rule application; the start stays forced by WOP 3.1 and 3.4 on the record (SF9).
- Every replacement meter at a near-zero register (the reader's random-looking registers): a solver who counts a new
  meter's first read from zero would recover 307 of the 500 acre-feet the 31 swaps hide, and bench-test registers
  summing to 0.8 acre-feet on Lateral 3's two would put its delivery back in the golden's bin; kept the shop's real
  mix instead, 14 new meters at 0.00 and 17 rebuilt with their carried registers, every Ask A figure off on that
  path (S2b).
- Round 1 shipped design: weak per the 10/10 audit (COMPLIANT_WEAK, 2026-10-14), because its stump (each replay started
  from the depletion each field carried on 31 January, from its last set taken as a refill, against a full start) was the
  same gap as the judge's one open fork (no filed sentence fixed the 1 February state, so the DETERMINISTIC verdict was
  conditional on it), the decisive step was visible (the 64,887-row orders file the one large non-distractor file the
  default path never read, Table 1's November to January coefficients, the weather run to 31 January 2027; the judge and
  the reader both found it unprompted), and Ask A's meter chaining was crackable through the shop log's registers with no
  second device on the figures it moved.
- Filing the start state (WOP 2.4) on round 1's world: the literal estimand made round 1's golden the default path with
  nothing left to decide (every field's last set had refilled it in that world); the growers were rebuilt so the drip,
  micro-sprinkler and sprinkler fields are held at a working deficit, which only the record's water shows.
- An unscoped sentence that an irrigation returns the root zone to field capacity (round 1's WOP 3.4): its literal
  execution on the 2026 sets is the default path (a filed sentence whose literal reading gives the easy answer, a
  main-call fork); scoped to the replays ("In a replay").
- Filing a field-capacity start on 1 February 2026, or the record run itself: names the method (rule application); left
  to the data (SF12, the run converges from any start before the wet winter).
- Grading the monthly schedule (WOP 5.1): R3's monthly shares matched the golden's from May to September, five of nine
  months free to the default path; dropped from the prompt.
- Grading the setting replay's requirement to the nearest 10 or 100 acre-feet: defensible constructions of the record
  run (SF13 to SF16, SF22, SF27) move it by up to 267 acre-feet, across those bins; dropped, and the order moved to whole
  thousands so every construction lands in one bin.
- Asking for the setting weather year: the default path and every near correction also land on 2012, a free criterion
  for the mirror; dropped.
- The Lateral 5 tail reach (05-045 to 05-058) re-served through a connector: replaced by the west spur (05-021 to
  05-034), every spur meter read on the change day and no water across it, so the as-of assignment converges.
- A heading logger cutover (a clock change in mid-season) as Ask 2's device: it moved only the days at the season's
  edges and announced itself in the daily series; replaced by the logger outages whose estimates sit in the operations
  log.
- Closing SF14 (the record's water within a day) by an evening convention: abandoned; the three orders of a day converge
  on the order and the year (asserted).
- `UNIT_SALT` 0 (the first draw of which replacements came new): a new meter's first read counted from zero landed
  Lateral 2's deliveries in the golden's bin (1.5 acre-feet off); redrawn (14), every lateral 18 acre-feet or more off.
- Cancelled sets placed after a field's last set and allowed to run past 31 October: two 2026 orders ended on 1
  November, a set the ordering system would not take after the canal's close; such a set is no longer placed.
- The asks' motive as round 1 worded it ("Our loss allowances will be set against what the laterals did in 2026"): it
  named a later decision with another owner (the Board's next allowances), the H18 defect; retied to the call as the
  audit trail of the allowance the order carries for each lateral.
- The record run started at field capacity on 1 February 2026 and the golden's note saying the winter had every root zone
  full then: four dry days after the 27 January rain left every field up to 0.17 inches short on 1 February, so the note
  was not true of the record (H6); the run now starts from the end of 27 January 2026, when every root zone was full
  from any November state (asserted), and files the same state on 31 January 2027.
- A WOP sentence crediting each field's 2026 delivered sets to its root zone, to answer the judge's round 2 residual:
  refused. It files the HOW, the decisive step's own estimator, and turns the record run into rule application; the
  residual is closed by the estimand and the data instead (SF34, asserted on the clean truth).
- Round 2 shipped design: decisive step read as rule application per the rule 3 audit (2026-10-15, VERDICT FAIL), because
  its start state was the procedure's daily balance (WOP 3.1 to 3.3) executed on the 2026 delivery record at Table 4's
  efficiency, which the table's note then defined as "the share of the water delivered to a field that its root zone
  receives", as WOP 2.4 pointed to; executed word for word on clean data it gave the golden (215,000) with no parameter
  fitted, no state uncertain and no candidate estimators separated by data. Kept the world, the order rule, the replay
  model and the estimand; the start is now an estimate (Table 4 scoped to WOP 3.5, the record's efficiency fitted on the
  soil moisture network), and 215,000 is the default path.
- The audit's proposed late-January probe snapshot on a random sample of fields of each method (prototype, 65 probed
  fields): the probed fields' mean share of total available water by method, an additive offset of the Table 4 run and
  a regression on the probes each landed in or next to the golden's bin (217,000 against 217,000 at an efficiency below
  Table 4; 212,000 and 213,000 against 212,000 above it), so the probe file's natural use was the answer and the file
  a signpost; replaced by a season-long station network whose 31 January readings cannot see the efficiency.
- A probe sample skewed by crop (no tubes in the shaken nut orchards) or by the last set (cooperators' later sets),
  prototype: the transfers' misses swung a bin either way with the efficiency and the draw, never a structural miss;
  replaced by stations in the early blocks, which the dry autumn takes to the bottom of their root zones under any
  efficiency, so the January snapshot is blind for a computable reason.
- The record's efficiency below Table 4 (systems short of design): the start saturates near total available water, the
  order flattens (216,100 to 216,400 across 0.88 to 0.94 times Table 4), the stations' January share lands the golden's
  bin, and the growers' orchards would have run far past allowable depletion all summer; replaced by an efficiency above
  Table 4 (a deficit set loses little below the root zone), 1.0425 times it give or take 0.004 field to field.
- Re-simulating the growers on the record's efficiency (each set sized to the true share): it moves every set, the
  meter book, the headings, the weirs and every ask figure; dropped: the growers keep sizing their sets on Table 4 (the
  2026 record unchanged byte for byte) and only the root zone as it is runs on the share that reaches it.
- Stations drawn without the January property (`STATION_SALT` 0 to 8 at 1.04 times Table 4): five to nine of the eleven
  stations blind, the rest still short of the bottom of their root zones on 31 January, so their January offsets showed
  the Table 4 run's excess and an offset correction moved to 214,000; redrawn (9): every station's 31 January state the
  same under Table 4 and under every efficiency up to its own (asserted), the order 212,000 with its 24th mid-bin.
- The grant's name ("water use efficiency") in the station export's title line: the stump's own word in a main-call
  file; the grant is named the state's on-farm water conservation grant.
- Fitting each station by golden section alone: on a small pasture root zone the misfit's floor is flat and bumpy (local
  minima 0.0005 apart), so the verifier's own search settled elsewhere and one replay crossed a 10 acre-foot line; the fit
  is now the best of a ten-thousandth grid, refined, and the verifier scans the same grid on its own code.
- The ranch names (a place or bird word plus Ranch, Farms, Vineyards: "Juniper Vineyards" on 11 request rows, 203 names
  over 688 rows) and the operations log's nine outage pairs in one frame ("Lateral N heading flume: ... No logger total;
  Water Master estimating ..."): generator tells under the wave 3 bar; replaced by grower accounts drawn the way an
  east-side district's accounts read (family farms, partnerships, trusts, a few road-named LLCs, account names unique) and
  outage entries in their writers' own words, every estimate and ask figure unchanged (asserted).
- A March station gap noted as the probe pulled for the grower's ripping, on an alfalfa block: ripping is an orchard and
  vineyard job; the note now says gophers chewed through the logger cable.
- The round 3 judge's optional prompt clause filing the start "from the root zone the District's 2026 deliveries and
  soil moisture readings put each field in on 31 January" (a WHAT, not the fit): declined at ship; it names the decisive
  step's evidence in the prompt, a single-purpose sentence the wave 3 bar bans, and the judge found the method forced by
  the data without it (SF48).
- Architecture 1 (Kestrel Bend Irrigation District, round 3, 212,000 acre-feet): shipped 2026-10-15 with no portal
  result and re-rooted 2026-11-01 at the Batch 3 queue reset; one architecture per world, so the irrigation-district
  world is closed and the slot redrawn as architecture 2 (`## Architecture 1 record`).
- Draw candidate, TV audience flow after a lead-in change (2026-11-01): spent at the slots screen (task115 and task174
  rejected the same inherited-against-loyal audience law); dropped before a card.
- Draw candidate, hospital weekend discharges and the Monday pile-up: spent (task127 loop 1 and task170); dropped.
- Draw candidate, a gauge's stage-discharge rating drifting with channel aggradation so the published discharges carry
  a level shift: removing an artefact from a published series is catching a defect (rule 3's planted-defect ban, the
  literal standard is the golden), and the field's correction is a reflex once seen; dropped at the draw.
- Draw candidate, rating hysteresis on the rising and falling limbs of a flood: spent at the abstraction test
  (task279's concentration-discharge hysteresis screen) and decided by a field reading of the loop; dropped.
- Draw candidate, a reservoir upstream regulating the flood record: the agency codes regulated peaks and Bulletin 17C
  names the remedy (the post-regulation period), so the step is read off a code and the reflex lands it; dropped.
- Draw candidate, landfill airspace with waste settlement: the field's settlement curve fitted to the survey record
  would itself be the golden (no precondition the data violate), the method-at-the-top shape 1.1b forbids; dropped.
- First card draft (2026-11-01): `ban.pattern` G5 (task125), `ban.artifact` register and `ban.forum`
  board_of_directors (task133); redrawn to G16 then G6, `published_series`, `trustees_or_governors`. A G13 decisive
  generator with gap time hit `test.same_driver` inside the batch, not clearable by differentiation; dropped.
- First personas from a hand list (James, Danielle, Richard, Jennifer, Matthew, Nicole): `people.first` WARNs; replaced
  by the seed-138 draw (Dennis Zhang, Kristin Lucas, Eric Thornton, Jesus Hernandez).
- Orrinsford's drainage area at 5,900 sq mi in the prototype: the drainage-area ratio at exponent 0.5 landed the golden's
  raise (a cheap route on the call, Gate F); set to 6,480 sq mi (ratio 1.314), the area routes now file 3 ft or more.
- Other world seeds in the draw-stage search (a scratch screen, not shipped): many put the at-site route or the
  post-raise-only route on the golden's raise, or made the trend tests significant; seed 1445 puts every rung on its
  own raise with trend tests at p 0.48 and 0.77 and the golden family inside one design-discharge bin (asserted in
  `checks.py` on the shipped pack).
- A crown built knot by knot from Table 4 margins (each cross-section's own shortfall, -1.50 to +0.41 ft): the 50 ft
  survey points between cross-sections near the railroad bridge, inside its 4 ft freeboard zone, came within 0.1 ft of
  2 ft of shortfall (a fork on where the crown is checked), and a 650 ft misaligned survey join produced negative
  settlement; the crown is now a smooth as-built grade, the bridges short only through their afflux and extra
  freeboard.
- Annual chances under the first hydraulics (WS_C 7.30, exponent 0.55, railroad afflux 1.45): the golden family's
  spread left the five settings at best about 0.009 percentage points inside their one-decimal bins (a scratch
  measurement on that pack); the hydraulic model
  re-cut (6.80, 0.58, 1.40) and the railroad crown placed about 1.48 ft short, every setting now 0.012 points or more
  inside under all twelve constructions (asserted).
- The 2016 stationing as a 2019 extension (old station plus 650 ft): a station-number join then gave settlement 0.16
  ft too small, negative in four reaches, so the device announced itself; the 2019 work is now a realignment that
  took the first 650 ft out of service, the join's error is positive everywhere (silent).
- The Main Street sill at 617.60 and then 617.90 ft: under the re-cut hydraulics the 2025 flood no longer reached it and
  water year 2022 sat within 0.33 ft; set to 617.45 ft (2025 reaches it by 0.35 ft, 2022 stays 0.68 ft below).
- Estimate codes on early Coyle Bridge and Orrinsford peaks: dropping the estimated years moved the design discharge to
  115,000 (a Layer 1 item moving a critical component, R2); the codes now sit on the Ashby, Gale Creek and Fenwick rows.
- A Notes sheet in the DNR inventory (what RM and "Crown raised" mean): a sheet describing the data
  (`dataset-generation` section 3); removed, each column's header carries its meaning.
- OP-04 (2014) listing the closures at 62+40 and 118+70: the present stationing dates from 2019, an anachronism and a
  second key to the ask A device; the closures are named only.
- LS-02 (April 2018) naming "the 2019 hydraulic update": a document citing a later one; it now names the district's
  current hydraulic study.
- Table 4's discharge grid at 60,000 to 150,000 cfs in 10,000 steps: its 110,000 column header is the golden design
  discharge to the nearest 5,000, a `leak.py` sweep 3 LEAK by coincidence; the grid now runs 65,000 to 155,000, and the
  crown was re-placed (1.485 ft short in the world, 1.48 ft on the survey) so every annual chance stays mid-bin.
- The town named Halbrook: one letter from real towns named Holbrook (`reduce-house-fixes` H21) and already used by
  five builds on file; renamed Orrinsford (district OLDD, logger ORF2, benchmarks OL-), no figure moved.
- The ORF2 logger export with battery voltage and enclosure temperature: the battery's charging hour profiles the clock
  in one file (a hygiene-battery item, so the cracker kept the three 2020 floods); the export now carries stage alone
  and the clock shows only against the published peak times or the Coyle Bridge travel time.
- OP-04's warning as "21.0 ft on the gauge (elevation 661.00 ft NGVD 29)" with the prompt asking for the warning
  stage: a literal reader could take the gauge figure as the trigger after the datum change (a fork on ask B); OP-04
  now files the warning level as the elevation with the gauge figure in brackets, and the prompt asks for the warning
  level.
- The Orrinsford gauge datum at 608.00 ft NAVD 88: low-flow stages read about -1 ft on the ORF2 logger, below any real
  gauge datum's floor; set to 600.00 ft (599.73 ft NGVD 29), the sill at 17.45 ft on the gauge, every crossing and
  lead time unchanged (both datums whole feet, so the hundredths round alike).
- LS-02 s.3 with no window and s.8 saying the annual peaks are "those published by the State Water Survey" (judge
  round 1, Gate C): the 18 water years since the last raise met s.2 and s.8 as written (1 ft), and s.8 read literally
  forbade any rebuilt year; s.3 now files the window (one peak for every water year since 1962) and s.8 the source
  only. The judge's wording ("the discharges the present river would carry in the years of the Coyle Bridge record")
  was refused: it names the move.
- The relation at about 2 per cent scatter (intervening share sd 0.018, noise 0.011) around 1.078: the judge's
  extension forms ran 111.2k to 113.6k, the top past the 112,500 edge; the intervening tributaries' share made steadier
  (they crest a day before the main stem reaches town: sd 0.009, noise 0.0055) and smaller (0.065), centring the
  design discharge at 110,403 with six forms at 110,260 to 110,477.
- Published peak times off the hourly records by 0 to 3 h (each crest pulled earlier by a falling baseflow), which
  pointed at a 4 h clock: the published times are now the hour the agency's own record tops out, each annual crest a
  single top hour in every shipped series (crest sharpness set per flood).
- The ORF2 logger swap as a 7 h gap: nothing inside the export fixed the old clock; the two loggers now run together
  for three days and line up only at 6 h.
- Lead times with fractions up to 0.86 h: truncation filed other whole hours (judge round 1); every lead now sits 0.1
  to 0.4 h past its whole hour.
- Reach descriptors ("north tie-in to Pump Station 1" and the rest) in the golden and the write-up with no shipped
  source: dropped; the reaches are their ids and station ranges from the 2024 survey.
- A 2024 survey every 50 ft against a 2016 survey every 100 ft with a 650 ft realignment: the 2016 shots paired with
  one 2024 shot in two, so the surveys' reach means differed from the paired figure (R1 0.06, R2 0.11, R8 0.10);
  both surveys every 100 ft and the realignment 700 ft, pairing one to one.
- Table 4 with one uniform fall and a crown falling smoothly at round steps (the leak reader read both as computed):
  reach slopes, cross-section effects and the bridges' afflux in Table 4; low spots, the 2019 tie-in step and the
  Cedar Street floodwall's level top in the crown, none within 400 ft of a bridge.
- The 2025 inspection summary with an overall-rating paragraph and a follow-up line: restyled as the DNR checklist's
  item, station, rating and remark table.
- The Coyle Bridge datum change in October 2021: with the ORF2 overlap now visible to the battery, a cracker fixing
  the clock would have kept the three 2020 floods; the change moved to 22 October 2019, before every flood in the ask.
- The Main Street sill at 617.45 ft under the repaired hydraulics: the 2025 flood crested below it; set to 616.95 ft
  (2025 over it by 0.42 ft, water year 2022 0.74 ft under).
