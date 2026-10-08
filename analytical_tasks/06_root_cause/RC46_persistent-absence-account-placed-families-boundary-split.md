# RC46 — The account of doubled persistent absence the department adopts, when the pupils living outside the city are two groups the census labels alike

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Policy & Education · school attendance policy |
| Mirrors | Threshold KPIs at large platforms that double when the whole distribution shifts, while a cohort that another team moved far from its service point sits inside a segment the dashboard labels alike (the share of requests over a latency SLO at Google Cloud or AWS when a capacity team pins some tenants to a distant region, the share of late deliveries at Amazon when a fulfilment team reassigns some customers to a far depot) |
| Decision shape | A structure the body adopts: the account of the rise in persistent absence (how many problems, where each sits and its share), scored at next year's close-out |
| Committed call | Two problems: a whole-population shift carrying 72% of the rise, and the 17,200 pupils whose families the housing authority placed outside the city carrying 28%, with the 43,000 cross-border pupils inside the shift |
| Gap · Pattern | Gap 2 (population) at the decisive rung, Gap 4 (rule) below it · a mixed segment split through a join (measured #6): residents outside the city, labelled alike in the census, are placed families or cross-border choices, told apart only by the housing authority's placement register; with the saturated tie of measured #19 at rungs 1 and 2 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #6 treats a mixed segment all one way · #19 breaks a big tie instead of questioning it · #13 validates on one population, applies to another |
| Calibration form | Prior-period close-out: the department's close-outs of its last three annual absence accounts, each adopted account set against the next year's persistent absence by school, phase and census group |
| Driving force | Shift a distribution past a 10% threshold and the share doubles, and school by school the shift explains almost all of the rise. But the framework states every share at the lowest value consistent with every file of record, and the pupil census holds tails at 140 schools that no shift produces. The tails sit on pupils the census records as living outside the city, and separating that group leaves a clean shift. The census labels them alike. The housing authority's placement register shows that 17,200 of them are in families it placed outside the city, and the housing code makes their travel its duty. The other 43,000 chose schools across the boundary, and their absence moved with everyone else's. Booked as one group they carry 35% of the rise; split, the placed families carry 28%. |

## 1. Situation

A city's education department reports that persistent absence, the share of pupils missing at least 10% of sessions, has doubled since
before the pandemic, from 10.3% to 20.6% of its 430,000 pupils. The minister wants an attendance case-worker for every persistently absent
pupil. The department's analysts say the whole distribution moved and the threshold amplified it. The attendance framework requires an
account of the rise: how many problems, where each sits and its share, with each problem assigned to the service that holds the duty to act
on it. Next year's close-out will score the account. Eighteen months ago the housing authority, short of rooms inside the city, began
placing homeless families in temporary accommodation outside it, and their children kept their school places.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the census's sessions and addresses, the published persistent-absence rates, the placement
  register and the close-outs. The analysts are right that the distribution moved, and the minister is right that some children have
  nearly stopped coming. No one's reading of their own figures is overturned. The question is which children belong to which problem.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the minister, the analysts and every voice. The threshold model still explains the rise school by school, the
  census still offers the resident-authority split that clears the tails, and nothing in either separates placed families.
* **Instrument repair.** No file is suspect. The census records sessions possible and missed for every pupil and each pupil's address at
  each termly census; its resident-authority flag is correct and records residence, a different attribute from placement. The placement
  register records every household the housing authority placed, with members, addresses and dates. The register's reason codes enter no
  rung, and even a perfect reason for every session leaves rung 0 at one distinct group, rung 1 at one shift (97%) and rung 2 at the city
  boundary (35%), because none of them reads reasons. The saturation at rung 1 sits in the framework's booking rule, not in a file. Telling
  placed families from cross-border choices is a join across complete records under the housing code's clause, and re-running the shift on
  everyone else is a construction no row records, so the decisive rung is still needed.
* **Lens swap.** The naive population of the second problem is every pupil living outside the city. The answer's is the pupils whose
  families the housing authority placed there, a different population, and the 43,000 others move into the shift.

## 3. The driving force

A strong solver does not read the doubling as a new group. Most newly persistent absentees missed between 10% and 15%, and every decile of
the distribution moved, so it fits each school's reference distribution, moves it to the school's current mean and recovers the threshold
amplification. At 410 schools the model predicts at least the actual rise, and the framework's booking rule sends those schools' whole rise
to the shift. The account reads as one problem. But the framework states every share at the lowest value consistent with every file of
record, and the pupil census holds tails at 140 schools, pupils missing more than a fifth of their sessions, that no shift of their
reference distribution produces. The tails sit on pupils living outside the city. Separating them leaves a clean shift, and the close-outs
certify the construction, including the year a neighbouring authority cut its school bus. That account books 35% of the rise to
cross-boundary travel. But the census labels two groups alike. The placement register shows that 17,200 of the 60,200 pupils living
outside the city are in families the housing authority placed there, and the housing code makes their children's travel its duty. The
other 43,000 chose schools across the boundary, and their absence moved exactly with the shift. Split by the register, placed families carry
28% of the rise and the shift 72%.

## 4. The ladder

| Rung | Construction | Names (the account) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Newly persistent absentees counted and broken down by census group | One problem: a distinct group of 44,300 newly persistent absentees, in every group (100%) | The minister's reading, and every count is published | The pupil census: 79% of the newly persistent absentees missed between 10% and 15%, and every decile of the distribution moved up |
| 1 | Each school's reference distribution moved to its current mean, a fully explained school's whole rise booked to the shift by the framework's rule | One problem: a whole-population shift (97%, residual 3%) | The textbook threshold amplification, and 410 of 610 schools tie at a fully explained rise | The pupil census: at 140 schools a tail of pupils missing over a fifth of sessions that no shift of the reference distribution produces |
| 2 | Hygiene of a saturated share: each school's explained share at the lowest value consistent with the school model and the census; the census group whose separation clears the tails (residents outside the city) booked with its whole change, the shift on the rest | Two problems: shift 65%, residents outside the city 35% | Every tail cleared, and the close-outs certify the construction, including the year a neighbouring authority's bus cut sent its cross-border pupils' absence up | The placement register: 17,200 of the 60,200 pupils living outside the city are in families the housing authority placed there |
| 3 | **Decisive:** the residents outside the city split through the placement register under the housing code's travel clause; placed families booked with their whole change, cross-border choices returned to the shift's population | **Two problems: whole-population shift 72%, families placed outside the city 28%** | — | — |

* **Structure shape.** Each rung names a different account: one distinct group, one shift, two problems with the second at the city
  boundary, then two problems with the second among placed families. Rung 2's second share sits 27% above the answer's.
* **Partial correction priced (L3).** A solver who splits the segment by the register but keeps the cross-border choices as their own problem
  adopts three problems (shift 65%, placed families 28%, cross-border travel 7%). One who separates every family in temporary
  accommodation, including the 19,350 pupils placed inside the city, books 31% to placements (12% from the answer). Neither half adopts the
  answer's account.
* **Grid.** Shares (capped, lowest value) × separated segment (none, residents outside the city, every placed family, families placed
  outside, families placed outside with cross-border choices kept apart) gives 10 cells. Every capped cell reads one problem. Lowest value
  with no separation leaves an unlocated 25%. Only families placed outside, with cross-border choices returned, adopts the answer, and the
  nearest wrong share is the every-placed-family cell at 31%.
* **Which guard binds.** This is a structure with shares and no ranking, so the separation floor binds: every other second share sits at
  least 11% from 28%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The housing code gives the housing authority the travel duty for families it places outside the city, the admissions
   code leaves a family that chooses a school across the boundary to arrange its own travel, and the framework assigns each problem to the
   service with the duty. No document splits the residents outside the city or names the placement register as the key.
2. **Corpus blind for a computable reason.** *In every closed account the residents outside the city held no placed family, because the
   housing authority placed every family inside the city until eighteen months ago, so booking that segment one way was exact.* The
   close-outs certify rung 2's construction in 3 of 3 years, including the bus-cut year.
3. **No arithmetic symptom.** Persistent absence by school, phase and census group reconciles to the published rates on every rung, and the
   rise is partitioned exactly on rungs 2 and 3.
4. **Not a row predicate.** Placement comes from joining each pupil's census address and date of birth to the register's members and
   placement addresses, and the shift is then refitted on everyone the split leaves.
5. **The enumeration is arithmetic.** No census field marks a pupil as placed. The 17,200 are counted from the join.
6. **No cutover date.** Families were placed one by one over eighteen months, so there is no step to align on.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The department's close-outs of its last three annual absence accounts. Each holds the adopted account, the next year's
  persistent absence by school, phase and census group, and the close-out's verdict on each problem's share.
* **What it certifies.** Rung 2's construction: lowest-value shares, the separated group booked with its whole change and the shift fitted
  on the rest reproduce every closed year's realised shares within one point. In the bus-cut year the cross-border pupils carried 9% of
  that year's rise and gave it back when the route returned, exactly as booked. The capped construction misses that year.
* **What it is blind to.** Placement (property 2).
* **Twin pair.** Calder Street Academy and Wharf Lane School are identical on every column of the school table: roll (1,120), reference rate
  (10.1%), current rate (26.8%), mean absence and the share of pupils living outside the city (18%). Placed families are 12% of Calder
  Street's roll and 6% of Wharf Lane's, so their placement components are 8.6 and 4.3 points (2.0×). The resident split puts them 1.6×
  apart; only the register gives the 2.0×.
* **Resemblance points at the decoy.** The jump among pupils living outside the city most resembles the bus-cut year, which the close-out
  confirmed as a cross-boundary travel problem.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The framework: "Each problem is assigned to the service that holds the duty to act on it, and a group separated as a
  problem is booked with its whole change." The framework's standard: "Every share is stated at the lowest value consistent with every
  file of record." The framework's booking rule: "A school whose predicted rise meets its actual rise is fully explained by the shift." The
  housing code: "Where the authority places a household outside its area, it arranges the children's travel to their existing schools."
  The admissions code: "A family that chooses a school outside its home authority arranges its own travel."
* **Empirical pins.** Each school's reference distribution comes from the reference-year census. The tails come from the current census.
* **Voices.** Minister: "A generation of children has stopped turning up, and each of them needs a case-worker." Chief analyst: "Push a
  distribution past a threshold and the share doubles; nothing distinct happened." Transport manager: "Children crossing the boundary have
  the longest journeys in the system." Housing duty manager: "We place families where we can find rooms, and no school has raised
  attendance with us."
* **Licensed wrong basis.** The framework records that the ministerial board reads the account on the census's resident-authority breakdown
  and will see this year's on that basis.

## 8. Determinism by construction

* **Shift.** Each school's reference distribution is moved proportionally to the current mean of the pupils it covers. An additive shift
  moves no share by more than a point.
* **Tails.** A tail is the pupils above the 95th percentile of the shifted distribution. Any cut from the 90th to the 98th percentile
  flags the same 140 schools.
* **Join.** Every placed child matches exactly one census row on address and date of birth. No placed family returned to the city before
  the spring census, so every placed child's census address is the placement address.
* **Booking.** The framework books a separated group's whole change from the reference rate. Booking only its excess over the shift gives
  25%, which the bus-cut close-out rejects.
* **Maturity.** Every register for the year closed before the extract, and the census is the final spring return.

## 9. Prompt sketch and deliverables

> Persistent absence has doubled to one pupil in five, and the minister wants a case-worker for every persistently absent child. I need the
> account the department adopts: how many separate problems sit behind the rise, where each sits and the share of the rise each carries,
> in whole percentages, with the number of pupils in each group, because next year's close-out will score it. Send `absence_account.xlsx`,
> a chart `threshold_bridge.png`, and a one-page `account_note.pdf`.

* `absence_account.xlsx` — the account on every construction, the home-education sheet (ask A), the meal-eligibility sheet (ask B) and the
  close-out back-test (ask C).
* `threshold_bridge.png` — the reference and current distributions around the 10% line with the shifted reference overlaid, the placed
  families' distribution as its own layer, a bridge from 10.3% to 20.6% by problem, and a title stating the account.
* `account_note.pdf` — the problems, their places and shares, and the service assigned to each.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 districts, the children electively home educated at the year's end. *Device:* the
  home-education register keeps a child's row with an end date when the child returns to school, as its guide states. Counting rows
  overstates the year-end figure by about a quarter. Home-educated children are on no school roll and never enter persistent absence.
* **Ask B (device-carried).** For each district, the share of pupils eligible for free school meals on census day. *Device:* transitional
  protection keeps a pupil eligible after the family's income rises, recorded as a separate protection row with its own dates. Counting
  only current-eligibility rows understates eligibility by about a tenth. Eligibility enters no rung.
* **Ask C (validity).** For each of the three close-outs and each phase, the realised persistent-absence rate beside the one your construction
  gives on that year's files.
* **Decoupling.** Clearing the placement split or the lowest-value shares changes no figure in asks A or B. Ask C holds no placed family, by
  property 2.

## 11. Rubric arithmetic

12 districts (ask A) + 12 districts (ask B) + 3 close-outs × 3 phases (ask C) + the number of problems, each problem's place and share, and
the placed and cross-border pupil counts + 5 named chart parts + 3 files ≈ 47 criteria.

## 12. World-building constraints

* 430,000 pupils in 610 schools and 12 districts. Persistent absence rises from 10.3% to 20.6%, 44,300 pupils.
* 17,200 pupils (4.0%) are in families placed outside the city, at 82% persistent absence. 19,350 (4.5%) are placed inside the city, and
  43,000 (10.0%) cross the boundary by choice; both, like everyone else, sit at the shift's rate of 18.0%.
* Accounts by rung: one group (100%); shift 97% with a 3% residual; shift 65% and residents outside the city 35%; shift 72% and placed
  families 28%. Partials: three problems at 65 / 28 / 7, and every placed family at 31%.
* 410 schools cap at a fully explained rise, of which 140 hold tails. Calder Street and Wharf Lane are identical on every school-table
  column, with placed families at 12% and 6% of their rolls.
* The three close-outs hold no placed family, and the bus-cut year's cross-border pupils carry 9% of that year's rise.
* Home-education rows and meal-eligibility rows never touch sessions, addresses or the placement register.
