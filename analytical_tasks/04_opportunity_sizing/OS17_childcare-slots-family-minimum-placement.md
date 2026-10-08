# OS17 — How many children the ten grant-funded centres will place in their first year, when a family enrols only if every one of its young children gets a place

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · early childhood services |
| Mirrors | Sizing uptake when a household adopts only if every member's need is met (family plans at Apple, Google One and Spotify where every member needs a compatible device, Amazon household benefits, ride-pooling where every rider's leg must be covered), so seat-level capacity overstates households served |
| Decision shape | One figure committed at a date: first-year children in care at the funded centres, stated in the state child-care plan |
| Committed call | Children newly in certified enrolment at the ten funded centres in their first year, to the nearest ten |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · a minimum over sub-units (the family clears only when every child is placed), pinned by the close-out, over a saturated enrolment measure broken by the certification rule (#19) |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #4 never tests its reading against the control · #6 treats a mixed segment all one way |
| Calibration form | Prior-period close-out: last grant cycle's close-out for eight funded centres, with rosters, attendance, subsidy payments and the waitlists they opened with |
| Driving force | Waitlisted families take an offer only when every child under five can be placed at the centre. Infant rooms are the scarcest band, so a preschooler whose infant sibling cannot be placed never enrols, and preschool rooms the band totals call full stay partly empty. Placement is a family-by-family pass through each centre's waitlist in application order, reached through the waitlist's family numbers. The close-out reproduces only under that rule, and every rule built on band totals has a flat loss curve against it. |

## 1. Situation

A state has awarded start-up grants to ten new child-care centres, with 360 infant, 480 toddler and 960 preschool places between them,
opening in March. Its child-care plan amendment, due on 30 September, must state how many children the centres will have in certified
enrolment in their first year. Each centre holds a waitlist of children with their family numbers and application dates. Last cycle's
close-out reports eight funded centres' enrolment, with rosters, attendance and subsidy files. The certification standard defines
certified enrolment. The grants director says every funded place gets filled.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the places, the waitlists, the rosters, the attendance and subsidy files, and the close-out's
  certified counts. The rosters really are full. No stakeholder read is overturned. The difficulty is that a family is the unit that
  enrols, and its youngest child decides whether it can.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view. Places against waitlisted children by band, discounted by the certification ratio, still
  give a clean 1,355.
* **Instrument repair.** The suspect field is the roster count, which records children on the roster, a narrower thing than certified
  enrolment, and reads 100% everywhere. Replace it with certified counts: rung 0 still returns 1,800, rung 1 1,584 and rung 2 1,355, and the
  family pass is still needed. The waitlists carry every child with family number and application date.
* **Lens swap.** The naive read counts places and children by band; the answer counts families placed whole, a different unit.

## 3. The driving force

A strong solver knows funded places are not enrolled children. It sees the close-out rosters at 100%, finds the certification standard
takes the lowest of roster, attendance and subsidy counts, and applies the close-out's 88% certified ratio. It then caps each band at the
children waiting: infant and toddler rooms fill, preschool rooms are capped at 700 waiting preschoolers. That gives 1,355, and every
step reconciles. But 450 of those preschoolers have an infant brother or sister on the same list, and there are only 360 infant places,
half of which go to single-infant families in application order. A family whose infant cannot be placed does not enrol its preschooler.
Preschool rooms reach only 399 children, and the figure is 1,090.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Funded places | 1,800 (+65.1%) | The grant agreements' capacity, and the close-out rosters show every place filled | The certification standard: certified enrolment is the lowest of roster, attendance and subsidy counts, 88% of the rosters in the close-out |
| 1 | Funded places × 0.88 | 1,584 (+45.3%) | Saturation broken with the standard's own rule | The waitlists: only 700 preschoolers wait for 960 preschool places |
| 2 | Each band's places capped at its waitlisted children, × 0.88 | 1,355 (+24.3%) | Supply and demand matched band by band, every total reconciled | The close-out: band caps reproduce 9 of 24 certified band cells; families enrol only when every child is placed |
| 3 | **Decisive:** a pass through each centre's waitlist in application order, placing a family only when every child under five fits, × 0.88 | **1,090 children** | — | — |

* **Figure shape.** Every correction walks the figure down and the answer is the minimum cell; the decisive move removes 19.6% of the
  rung-2 figure.
* **Partial correction priced (L3).** A solver who places families whole but skips the certification ratio lands at 1,239 (+13.6%). One who
  lets a family enrol whichever children fit lands back on the band caps at 1,355. One who walks the lists in any order
  but application date reproduces none of the close-out's eight centres to the child.
* **Grid.** Certification (rosters, lowest count) × placement (places, band caps, whole families) gives 6 cells: 1,800, 1,584, 1,540,
  1,355, 1,239 and the answer. The nearest wrong cell is 1,239 at +13.6%, and it costs the certification rule the close-out applies.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The waitlist policy says places are offered in order of application. No document says a family declines an offer
   that leaves a child out.
2. **Reproduction, not a menu.** Whole-family placement in application order reproduces all 24 certified band cells of the close-out to
   the child. Band caps reproduce 9, and their misses all run high, so they fail on the total too. A fitted fill rate on places has a flat
   loss curve from 0.70 to 0.80 and pins nothing. The rule is a construction: families are formed from the waitlist's family numbers, and
   each centre's list is walked in order against its rooms.
3. **No arithmetic symptom.** Places tie to the grant agreements, waitlisted children to the centres' lists, and the certification ratio to
   the close-out.
4. **Not a row predicate.** Placement needs a group (the family), an order (application date) and a state (rooms remaining) carried through
   each centre's list.
5. **The enumeration is arithmetic.** No column says which children will enrol; the waitlist holds 2,300 children in 1,750 families.
6. **No cutover date.** Every centre opens in the same month, and no series steps.
7. **Survives deletion.** Removing the director's view leaves the band caps certified on the totals.

## 6. The calibration corpus

* **Form.** Last cycle's close-out: eight centres' certified enrolment by band, their rosters, attendance and subsidy files, and the
  waitlists they opened with.
* **What it pins.** Whole-family placement in application order, 24 of 24 cells; the certified-to-roster ratio of 0.88 at every centre and
  band.
* **Twin pair.** Elmwood and Fairview are identical on places (12 infant, 16 toddler, 32 preschool), waitlisted children by band (30, 24,
  40), tract type and opening month. Elmwood's preschoolers come from single-child families and it certified 28; 30 of Fairview's 40 have
  an infant sibling, only 6 such families got infant places, and it certified 14, 2.0× fewer. Only the family pass separates them.
* **Resemblance points at the decoy.** The new centres' place mix most resembles the close-out's centres with single-child waitlists,
  which filled their preschool rooms.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The plan template: the figure is children in certified enrolment at funded centres in their first year. The
  certification standard: certified enrolment is the lowest of the month's roster, attendance-verified and subsidy-paid counts. The
  waitlist policy: places are offered in order of application date. The grant agreements' places by band.
* **Empirical pins.** Whole-family placement and the 0.88 ratio, from the close-out.
* **Voices.** The grants director: "Every place we fund gets filled. Our centres open with waiting lists." The licensing manager: "Preschool
  rooms are the easy part. Infant rooms are where we're short."
* **Licensed wrong basis.** The plan template records that the federal regional office reviews plans on funded places and will compare the
  figure with the grant agreements' capacity.

## 8. Determinism by construction

* **Order.** Application dates are unique within each centre's list, so the walk has one order.
* **Acceptance.** In the close-out every family offered places for all its children accepted, and none accepted a partial offer, so no
  acceptance rate needs fitting.
* **Lists.** Each family waits at one funded centre only, so no family is counted twice across centres.
* **Ratio.** The certified-to-roster ratio is 0.88 in every band and centre of the close-out.
* **Rounding.** The walk places 1,239 children; × 0.88 gives 1,090.3, mid-bin at the nearest ten.

## 9. Prompt sketch and deliverables

> The child-care plan amendment is due on 30 September and has to say how many children our ten new grant-funded centres will have in
> certified enrolment in their first year, to the nearest ten. Our grants director is confident every funded place gets filled. Give me the
> figure as a sentence for the plan, with `placement_build.xlsx`, a chart `rooms_and_families.png`, and a one-page `plan_note.pdf`.

* `placement_build.xlsx` — places, waitlisted children and placed children by centre and band under each basis, the close-out back-test,
  the staffing sheet (ask A) and the inspection sheet (ask B).
* `rooms_and_families.png` — a script-rendered grouped bar chart per centre: places, waitlisted children and placed children by band, the
  preschool shortfall caused by unplaced infant siblings hatched, and the certified figure labelled per centre.
* `plan_note.pdf` — the committed figure and the bridge from funded places to it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each funded centre, the share of lead-teacher posts held by qualified staff on its opening day.
  *Device:* provisional credentials appear in the registry with an expiry date, and the licensing guide counts a provisional credential
  valid on the day as qualified. Treating every provisional entry as unqualified understates the share at four centres.
* **Ask B (device-carried).** For each of the 24 existing centres in the funded tracts, serious findings per inspection over three years.
  *Device:* a follow-up inspection after a serious finding is recorded as a new inspection carrying `follow_up_of`, and the inspection guide
  counts it as part of the original. Counting follow-ups as inspections halves the rate at the centres with most findings.
* **Ask C (validity).** The figure under each of the four rung bases, and close-out band cells reproduced (of 24) by band caps, partial
  family placement and whole-family placement.
* **Decoupling.** Placing children by band instead of by family changes no figure in asks A or B. The staff registry and inspection records
  touch neither the waitlists nor the close-out.

## 11. Rubric arithmetic

10 centres (ask A) + 24 centres (ask B) + 4 bases and 3 back-test counts (ask C) + the committed figure, placed children by band (3) and
families placed + 5 named chart parts + 3 files ≈ 58 criteria.

## 12. World-building constraints

* Places: 360 infant, 480 toddler, 960 preschool. Waitlisted: 900 infants (450 with a preschool sibling), 700 toddlers (100 with a preschool
  sibling), 700 preschoolers (150 from single-child families).
* In application order, 180 infant places go to sibling families and 69 toddler places to toddler-and-preschooler families; 399 preschoolers
  are placed.
* Rung figures 1,800 / 1,584 / 1,355 / 1,090; partial readings 1,239 and 1,355.
* Elmwood and Fairview match on every place, waitlist-band and tract column.
* Staff registry and inspection records never touch waitlists, rosters or the close-out.
