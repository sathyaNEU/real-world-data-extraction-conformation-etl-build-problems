# OS32 — Which county gets 300 asthma home-visit enrolments, when one enrolment is a home and the claims count children

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · health-system administration (Medicaid managed care) |
| Mirrors | Sizing an outreach programme whose slot serves a household while the data counts individuals (family-plan retention offers at telecoms, household device bundles where one purchase covers every member, team-level onboarding seats in B2B software) |
| Decision shape | Which of N gets one scarce thing, with the sizing graded: the 300-enrolment programme goes to one of six counties |
| Committed call | The county that gets the programme, and the preventable asthma stays it avoids in its first year |
| Gap · Pattern | Gap 2 (population) · E02 (the unit the programme funds is a dwelling, which no file stores), with E16 below it (two person-linkage constructions pass the county totals and only one passes the state's finer counts) |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #2 counts file rows instead of the real unit · #12 stops at the first control that passes · #5 takes the population a flag or filter suggests |
| Calibration form | Change-log natural experiments: the programme's change log of four county launches (2019–2024), each with enrolment IDs and enrolled homes' preventable stays in the twelve months before and after |
| Driving force | A home visit fixes a home: one enrolment covers every child living in the dwelling, and the programme log counts enrolments, not children. Eastvale has many homes where two or three asthmatic children live under different Medicaid cases (half-siblings, kinship care), so its 300 best homes carry 1,200 prior-year stays against 770 for its 300 best children. Building homes needs the state's person index to gather each child's stays across re-issued IDs, then the address history as of the start date. No file stores the unit. |

## 1. Situation

A Medicaid managed-care plan will fund its paediatric asthma home-visiting programme in one county next year. Two community health workers
can take 300 enrolments, each a series of four home visits that removes asthma triggers. The plan's quality committee judges the programme
on preventable asthma stays avoided in its first year. The programme ran in four other counties between 2019 and 2024, and its change log
records each launch. The medical director wants Arden, which has the most asthma admissions.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the claims, the eligibility file, the state's published counts, the person index and the change log.
  Arden really does have the most admissions. Nothing reported is overturned. The difficulty is what one enrolment buys, which depends on a
  unit the claims do not hold.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view and every voice. The claims still rank counties by children's stays, and nothing says an
  enrolment is a home.
* **Instrument repair.** Make every claim perfect and every ID permanent. Children are still the rows and homes are still the enrolments,
  so the unit still has to be built.
* **Lens swap.** The answer counts a different population, the siblings an enrolment reaches who were never the enrolled child.

## 3. The driving force

A strong solver applies the programme's eligibility at the start date, links each child's stays through the state's person index, ranks
children by stays and sizes 300 enrolments on the top 300. That is a careful build, verified against the state's published counts, and it
names Calder. But the programme enrols a dwelling. A visit removes the mould, the pests and the smoke from the home, and in every launch the
stays of the enrolled child's siblings fell with the child's. In Eastvale, 41% of top-ranked children share a home with another child with
preventable stays, often on a different Medicaid case. Gathering stays by home needs three steps: link stays to persons through the index,
attach each person's address as of the start date from the effective-dated address history, then group by dwelling. Only then do the 300
best enrolments appear.

## 4. The ladder

| Rung | Construction (prior-year preventable stays in the top 300 units) | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Top 300 children flagged active, by plan member ID | A, Arden, 900 (1.30× Brookfield) | The programme size applied to the plan's own active children | Scheduled end dates and birth dates in the eligibility file put a third of Arden's top children out of the programme before it starts |
| 1 | Children eligible at the start date (under 18, eligibility running) | B, Brookfield, 680 (1.17× Dunham) | The contract's eligibility, applied as of the right date | The state's published counts of distinct children with two or more stays are reproduced only when stays are linked through its person index |
| 2 | Stays linked to persons through the state index, top 300 children | C, Calder, 943 (1.22× Eastvale) | Reproduces the county totals and every finer count the state publishes | The change log: each launch's enrolment figures reproduce only when enrolments are built as dwellings |
| 3 | **Decisive:** enrolment = dwelling: linked stays, address as of the start date, top 300 homes | **E, Eastvale, 1,200 (1.24× Calder)** (4th of 6 on rung 0) | — | — |

* **The answer.** Eastvale. At the change log's effect (0.55 of an enrolled home's prior-year stays), 300 enrolments avoid 660 preventable
  stays in the first year.
* **Position table.** Eastvale ranks 4th on rung 0, 4th on rung 1 and 2nd on rung 2 (1.22× behind Calder), and leads only rung 3.
* **Discriminator dominance.** Calder carries a 1.22× lead into rung 3 (943 against 770). Grouping by home multiplies Eastvale's stays by
  1.56 and Calder's by 1.02, an edge of 1.52×, above 1.2 × 1.22 = 1.47.
* **Partial correction priced (L3).** A solver who builds households from Medicaid case numbers still names Calder: half-siblings and
  kinship placements sit on separate cases, so Eastvale reaches only 890. A solver who groups by the address on the plan's member file
  without the person index attaches no stays filed under old IDs and names Arden.
* **Grid.** Eligibility at start (off, on) × person linkage (plan ID, state index) × unit (child, home) = 8 cells. Every non-answer cell
  names Arden, Brookfield or Calder. The nearest is linkage and homes without the start-date eligibility, led by Arden at 1,400 to
  Eastvale's 1,215, because Arden's top homes hold children who age out.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The contract says "300 enrolments" and the log counts enrolments. No document says what an enrolment is or that
   siblings benefit.
2. **The corpus pins the unit by reproduction.** Dwelling enrolments reproduce all four launches' enrolment counts, enrolled children and
   before-and-after stays exactly (4 of 4). Case-number grouping misses every launch's enrolled children by 9–14%, and child-level grouping
   misses every launch's stays. The dwelling is a three-step construction (index link, as-of address, group), not one key a solver can
   sweep.
3. **No arithmetic symptom.** County totals of stays are identical under every unit, because every grouping partitions the same stays, and
   member counts reconcile to the eligibility file.
4. **Not a row predicate.** Each child's stays are gathered across IDs, placed at a dated address, and summed over the dwelling's children
   before any ranking.
5. **The enumeration is arithmetic.** No column holds a dwelling's stays, and no file lists homes.
6. **No cutover date.** Launch dates are in the log, but the decisive fact is a unit, and no series steps with it.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** Four launches, each with enrolment IDs, launch date and the enrolled homes' preventable stays in the twelve months before and
  after, plus the same counts for eligible homes the launch did not reach.
* **What it certifies.** The effect: enrolled homes fell to 0.45 of their prior-year stays net of unreached homes, between 0.43 and 0.47 in
  every launch. That confirms any solver who sizes 300 units at 0.55.
* **What it pins.** The unit (above), reproduced only by the dwelling construction.
* **Twin pair.** Launches Riverton and Saltmarsh are identical on every column of the log a lookup reaches: enrolments (300), launch
  season, county class, mean index-child age and stays per enrolment ID. Avoided stays differ 2.0× (155 against 310), because Saltmarsh's
  homes held twice as many siblings with stays. Only the dwelling build from claims separates them.
* **Resemblance points at the decoy.** Calder resembles the four launch counties on urban share, churn and housing age, so a solver
  transferring a launch's per-enrolment result by resemblance lands on Calder.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme contract funds 300 enrolments for members under 18 at the start date. The quality committee judges the
  programme on preventable asthma stays avoided in its first year. The state's technical note defines a preventable asthma stay and
  excludes transfers in.
* **Empirical pins.** The 0.55 effect and the dwelling unit come from the change log. Person links come from the state index, which the
  state's finer published counts confirm.
* **Voices.** The medical director: "Arden has the most asthma admissions, so that's where the need is." The programme lead: "We enrolled
  300 every time and every launch delivered." That is true.
* **Licensed wrong basis.** The contract records that the state's care-management reviewers size outreach on children with two or more
  stays and will review the placement on that basis.

## 8. Determinism by construction

* **Address date.** No top-300 home in any county gains or loses a child through a move in the 60 days before the start date, so the as-of
  convention cannot move the answer.
* **Index links.** Every link in the state index is one-to-one, with no probable matches left open.
* **Ties at the cut.** Homes tied at the 300th place carry equal stays, so the top-300 sum is unique whichever tied home is taken.
* **Effect window.** Twelve-month and launch-year windows give the same effect to two decimals in every launch, and the four launches
  pool to 0.55.
* **Maturity.** The prior year has nine months of claims run-out, and no inpatient claim posted after month four.

## 9. Prompt sketch and deliverables

> We can fund the asthma home-visiting programme in one county next year, 300 enrolments, and our medical director wants it in Arden
> because Arden has the most admissions. Tell me which county gets it and how many preventable asthma stays it should avoid in its first
> year, to the nearest 10, in a sentence for the quality committee. Send `asthma_programme_case.xlsx`, a chart `county_reach.png`, and a
> one-page `committee_note.pdf`.

* `asthma_programme_case.xlsx`: the six counties under the four rung bases, the specialist sheet (ask A) and the medication sheet (ask B).
* `county_reach.png`: for each county, the cumulative prior-year stays reached by the first 1 to 300 units, as two lines (children and
  homes), with the 300 cut marked, Eastvale highlighted and the sibling share printed beside each county.
* `committee_note.pdf`: the committed county, the stays avoided, and why Arden and Calder are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each county, in-network paediatric asthma specialist appointment hours a week per 1,000
  child members, and the share of them in evening clinics. *Device:* the provider directory repeats a specialist once per practice
  location, and the scheduling file splits each specialist's weekly hours across locations. Counting directory rows triples capacity for
  the 17 specialists who work at three sites.
* **Ask B (device-carried).** For each county, the share of children with persistent asthma covered by controller medication on at least
  75% of last year's days, and the median coverage. *Device:* a reversed pharmacy claim posts as a negative row carrying the original claim
  number, and 90-day fills post once. Counting rows as fills inflates coverage at the two counties with mail-order pharmacies.
* **Ask C (validity).** Each county's top-300 stays under each of the four rung bases, and the change-log reproduction under dwelling, case
  and child units (4, 0 and 0 of 4).
* **Decoupling.** Clearing the dwelling construction changes no figure in asks A or B.

## 11. Rubric arithmetic

6 counties × 2 (ask A) + 6 × 2 (ask B) + 6 × 4 bases + 3 reproduction counts (ask C) + the committed county, the stays avoided, its margin,
and the homes and children it reaches + 5 named chart parts + 3 files ≈ 64 criteria.

## 12. World-building constraints

* Top-300 prior-year stays by rung (children flagged active / eligible at start / index-linked / homes): Arden 900 / 560 / 575 / 874,
  Brookfield 690 / 680 / 700 / 760, Calder 520 / 510 / 943 / 966, Dunham 610 / 580 / 600 / 650, Eastvale 560 / 550 / 770 / 1,200, Fenwick
  480 / 470 / 485 / 533.
* Off-ladder cells: homes without start-date eligibility give Arden 1,400 and Eastvale 1,215 (index-linked) and Arden 1,370 (plan IDs).
  Homes without the index give Arden 851 and Eastvale 610. Index-linked children without start-date eligibility give Calder 960.
* Enrolled homes fall to 0.43–0.47 of prior-year stays net of unreached homes in all four launches (an effect of 0.55 ± 0.02).
  Riverton and Saltmarsh are identical on every log column.
* In Eastvale 41% of top-ranked children share a home with another child with stays, and 72% of those siblings sit on a different case.
* Directory repeats and pharmacy reversals never touch inpatient stays, the index or the address history.
