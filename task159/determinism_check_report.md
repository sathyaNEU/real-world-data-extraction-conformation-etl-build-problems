# Verdict (task159 re-judge)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair is required and no model rerun is needed. The one advisory below (the local time zone is never named) is optional.

**Why:** Every committed answer reproduced from the shipped files, not only from the golden blocks.
- **Main call:** 26 shifts, split Mon 4, Tue 6, Wed 6, Thu 6, Fri 4. Under the crowding standard (peak above 85% of rated capacity), my independent train-capacity queue model posts exactly GAR-2, COR-2, ALB-6 and QUA-6 on all five days, and SAL-1S and SAL-4S on Tuesday to Thursday only. COR-5W is not posted, and no other platform is posted.
- **Supplementary figures:** All 14 escalator and elevator figures reproduced exactly.
- **Margins:** The decisive margins are robust (15% or more, and Sallow Park Mon/Fri holds even with alighting set to zero).
- **Stump:** It is analytical. The mid-week counts are backlog-censored by full trains, so scaling them by entries is the wrong route.

## Evidence

Literal-reading pass: the standard defines accumulation, the morning peak (the quarter-hour mean of trains arriving), the 85% threshold, rated capacity on the pick's first day, and what a weekday of the pick is. The forecast method is deliberately open. Options where the text is silent, and what each gives:
- **Seasonal ratio:** Spring-2026/autumn-2025 is about 1.02 for every complex, and 1.00 versus 1.02 changes no call.
- **Monday and Friday index:** Computed from the fare export for 06:00-10:00 local, 07:00-10:00 or all day, it is 0.80-0.82 (Mon) and 0.75-0.77 (Fri) for Sallow Park, in every window and in both autumn and spring.
- **Quarter-hour assignment:** Assigning a train to a quarter-hour by due time or by arrival time moves no call.
- **Capacity on 1 March 2027:** FER-4S reads 330, because the temporary 300 rating ended on 2027-02-12. FER-4S is far under the threshold either way.

| Item | Recomputed from the bundle | Reproduced? |
|---|---|---|
| Escalators, down/up per complex (controller log direction, register set speed 0.45 m/s, step width in mm, rated flow from manual 5.3, 72 weekday-timetable days from 8 Sep to 18 Dec less 26 and 27 Nov) | Garnett 72/144, Sallow 216/72, Hesper 108/144, Corran 232/96, Ferrier 36/248, Albrecht 268/36, Quarry 132/96 | All 7 exact |
| Elevator-hours, 07:00-09:45 local on those days (union of non-NORMAL monitoring intervals and work orders, per manual 5.4) | Garnett 27.91, Sallow 53.34, Hesper 38.61, Corran 17.97, Ferrier 45.51, Albrecht 37.26, Quarry 41.34 | All 7 exact to one decimal (Corran 17.97 gives 18.0) |
| Escalator direction in 07:00-09:30 | Stable on all 72 days for all 67 units. Where the log disagrees with the inventory's "direction" (e.g. 255-E4, 226-E4), the controller log governs. | Yes |
| Weekday index, autumn 2026, 06:00-10:00 local | Mon about 0.82, Fri about 0.76 of Tue-Thu | Yes (the dashboard's average weekday is a diluted mix, not usable for this) |
| Observed counted peaks (counts file) | SAL-1S about 985-1008, SAL-4S about 1253-1377, COR-5W Wed/Thu 670-752, COR-5W Mon/Fri 260/240 | Yes |

My own queue model (the census gives arrivals and alightings per quarter-hour per platform and passage, scaled by entries; trains carry cars x 150, take only their room after upstream riders and alighters, and the rest wait) gave these results:
- **Validation on autumn counts:** It reproduces the Sallow Park Wed/Thu build-up in timing and shape, with a peak 15-25% under the observed one. It reproduces COR-5W Mon/Fri almost exactly (260 versus 260, 229 versus 240). It gives about 590 at COR-5W mid-week on six cars, against 670-750 observed.
- **Spring 2027 forecasts**

| Platform and day | Forecast peak | Threshold | Margin |
|---|---|---|---|
| SAL-1S, Tue-Thu | 741 | 391 | well over |
| SAL-4S, Tue-Thu | 1161 | 425 | well over |
| SAL-1S, Monday | 267 | 391 | well under |
| SAL-4S, Monday | 291 | 425 | well under |
| SAL-1S, Friday | 248 | 391 | well under |
| SAL-4S, Friday | 270 | 425 | well under |
| COR-5W, all days (eight cars) | 249-334 | 399.5 | under, about 16% at the highest |

- **Sallow Park Mon/Fri:** The maximum train load on a Monday is 718-770 of 900, and still below 900 with alighting set to zero. The backlog cliff sits at a demand index of about 0.9 to 0.95, against a measured Monday index of 0.80-0.82. The call is therefore not knife-edge.
- **COR-5W:** On eight cars the maximum load is 988 of 1200, so there is no backlog and the peak is pure arrivals (334). On six cars the same demand backs up (about 640-670 peak).
- **Counts-scaled forecasts for the other platforms** (observed qh peak x spring entries / counted-day entries, compared with 85% of rated capacity). Posted: GAR-2 1.17-1.49, COR-2 about 1.14 on Friday and about 1.5 mid-week, ALB-6 1.32-1.82, QUA-6 1.25-1.78. Not posted: HES-3 0.66-0.84, ALB-3S about 0.79, ALB-3N 0.68-0.82, HES-1S 0.56-0.58, GAR-3S 0.65-0.70, QUA-1S 0.66-0.69, FER platforms 0.21-0.57, SAL-1N 0.17.
- **Totals:** GAR-2, COR-2, ALB-6 and QUA-6 give 4 x 5 = 20 shifts. SAL-1S and SAL-4S give 2 x 3 = 6. The total is 26, split Mon 4, Tue-Thu 6 each, Fri 4. This agrees with every block.

Competing answers tested:
- **Count-by-entries route** (carries mid-week counts to Mon/Fri and to eight cars): posts SAL-1S and SAL-4S Mon-Fri and COR-5W Mon-Fri, giving 20 + 10 + 5 = 35 shifts (wrong).
- **One-headway-arrivals route:** misses the Sallow Park backlog (gives 20 shifts).
- **Dashboard average-weekday scaling:** diluted by Mon/Fri (about 0.92 of Tue-Thu), which flips SAL-1S to not posted. This is a decoy-like reading, but a defensible analyst reading the export's own note ("weekdays Mon-Fri") would not use it for a Tue-Thu build-up.
- **Using the 300 temporary FER-4S rating:** no effect.

Open items I could not close:
- The golden xlsx and png were not available to me, so the deliverable files themselves are unchecked. Only the figures in the graded blocks were reproduced.
- The cross-batch fingerprint check against delivered tasks is outside the brief's readable scope. No near-duplicate was visible from the bundle.

## Files/Hygiene
- **Result:** PASS.
- **Files:** 20 input files in 4 formats (csv, pdf, xlsx, parquet).
- **Size:** The parquet has 761,594 rows and the legacy reads csv has 216,013 rows.
- **Provenance:** No authoring or benchmark language. The data dictionary is a plausible in-fiction document. Dates are coherent: counts delivered 4 Dec 2026, spring plan issued 14 Dec 2026, "as of 11 Jan 2027".
- **Realism:** The capacity register mixes legacy-style codes on non-watch-list platforms, and the elements inventory carries in/mm and design-versus-set-speed noise, which reads as real system output.
- **Layer 1 mess found:** UTC to local with a DST shift on 1 Nov, hybrid Mon/Fri days, a preliminary dashboard and a legacy fare system, a merged complex (Kennet and Albrecht), a temporary rating that ends on 12 Feb 2027, the controller log against the inventory direction, speeds and step widths in different units, and work orders against monitoring for elevators.
- **Advisory, not blocking:** The local time zone or UTC offset is never named in the package. It is derivable and forced by the data: first trains and the first escalator RUN UP occur at about 05:00 local, which is UTC-4 before 1 Nov and UTC-5 after, matching US DST. A wrong offset would flip escalator directions on the autumn days before 1 Nov, so a one-line offset in the data dictionary would remove the only inferential step. This is optional.
- **Exclusion-level findings:** None.

## Stump power
Adequate, and for an analytical reason. A strong model that cleans everything and reads every rule can still scale the mid-week counts by entries. That posts Sallow Park on Mon/Fri and Corran Junction's Line 5 on every weekday, and files 35 shifts. The counts file itself shows the nonlinearity (COR-5W 260 and 240 on Mon/Fri against 670-750 mid-week on 18-24% less entries), so a careful model can notice it. Sallow Park has no Mon/Fri counts, so the Monday and Friday call needs an actual train-capacity queue model. The 14 supplementary figures carry their own device traps (controller log against inventory direction, set against design speed, the union of work-order and monitoring intervals, and DST). A forecast not validated against the counts fails.

## Stumping type
`mechanism: binding_constraint (train-capacity-limited accumulation, forecast under a changed fleet; counts are backlog-censored)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`

The reported counts and entries are all correct. The difficulty is the queue dynamics: the observed accumulation is a function of train room, not of demand alone. Clean data would still stump a model that scales by proportion. Not a banned scaffold.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`

- **Domain:** Transit station planning forecasts platform accumulation under train-capacity limits against a crowding standard. Swapping the nouns (hospital waiting room, megawatt-hours) breaks the quantity. The deciding number is a station-planning model output, not a stated score.
- **Layer 1:** The mess listed under Files/Hygiene (time zones and DST, hybrid days, legacy and merged keys, units, work orders against monitoring).
- **Layer 2:** A load-constrained boarding and backlog model, validated against the autumn counts.
- **Easy route:** Scale the counted mid-week peaks by the entries ratio to Monday and Friday and to eight cars. This gives 35 shifts instead of 26.
- **Semantics and rules:** The deciding step is not field reading or rule execution. The 85% rule and the definitions are fully stated.

## Fix
none. Optional, in input_files: add the local UTC offset to `vtc_data_dictionary.xlsx`. This only fixes what the convention is and does not change any figure or the stump.
