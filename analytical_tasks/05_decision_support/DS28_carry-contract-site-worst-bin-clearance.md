# DS28 — Which storage site fills the co-op's one May carry contract, when a site delivers only if every one of its bins holds

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · grain storage and merchandising |
| Mirrors | Choosing the stock that fills one committed order when acceptance is decided by the worst sub-unit (single-origin produce programmes at grocery chains, semiconductor lots accepted only if every wafer passes, marketplace inbound shipments refused when any carton fails receiving checks) |
| Decision shape | Which of N gets one scarce thing: the co-op's single May carry contract, filled from one storage site |
| Committed call | The site that fills the contract, and its expected net carry in thousands of dollars |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · Pattern B with a minimum over sub-units (E30: a site delivers only if every bin holds), with finer controls (E16) killing rung 2 |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #12 stops at the first control that passes · #1 reports a failed back-test, ships anyway · #2 counts file rows instead of the real unit |
| Calibration form | Change-log natural experiments: the storage log of six seasons, 60 site-seasons stored to May, with intake tickets, bin fill logs and May outcomes |
| Driving force | The plant grades every load and the contract takes one origin, so a site fills it only if every bin holds condition to May. A bin's moisture is the bushel-weighted blend of the loads that went into it, and no file stores it: tickets carry timestamps, the fill log carries each bin's fill intervals. The site whose intake was driest on average hides one late-filled bin at 15.8%. The answer's intake ran wetter, and was spread evenly. |

## 1. Situation

A grain co-operative has signed one May carry contract with an ethanol plant: 300,000 bushels of corn from a single origin site, at a fixed
delivered price. Six member storage sites (A–F) have the room, and harvest is complete and binned. The co-op's marketing policy sends the
contract to the site where it earns the most. The merchandiser believes the river sites have always carried best. The co-op's lender
wants any storage case made on paired crop years, net of interest. The board names the site on Friday.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: cash bids, carrying costs, intake tickets, the bin fill log, the storage log and the co-op's annual
  delivered share. No stakeholder read is overturned. The river sites did carry best on average, and paired years net of interest are the
  right price history. The difficulty is which unit decides whether a site can deliver at all.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the merchandiser's view, the lender's request and the annual report. The contract margin net of carrying cost,
  adjusted by each site's intake moisture, still names C.
* **Instrument repair.** Put a moisture probe in every bin and log it daily. The probes would read what the blend already implies; the
  answer still turns on taking the worst bin rather than the site. The difficulty is the unit, not the measurement.
* **Lens swap.** The naive read scores each site's intake as one pool. The answer scores the bins inside it: a different population, and
  a minimum rather than a mean.

## 3. The driving force

A strong solver sets each site's contract margin against today's harvest bid, nets storage, interest and shrink, and adjusts for the
chance a site cannot deliver. The natural adjustment fits delivery on each site's average intake moisture, and that fit reproduces the
co-op's six-season delivered share to within 0.3 points. But the contract takes one origin and the plant grades every load, so a site
delivers in full only if every bin holds condition to May. Moisture blends inside a bin, not across a site: a load at 16% blended into a
dry bin is harmless, while a run of late wet loads filling one bin is not. Bin moisture is a construction. Each ticket is placed in the bin
whose fill interval contains its timestamp, and the bin's loads are blended by bushels. Site C's average intake was the driest of the six,
but its last bin filled at 15.8%. Site E's intake ran wetter, and every bin finished at or under 14.7%.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Average May bid minus average October bid at each site's local elevator, 15 crop years (the newsletter's spread) | A, a river site (47¢ against B's 39¢) | The co-op's own history at each site's market, and the river sites lead | The carrying-cost schedule: storage by site, interest at prime + 1% on harvest value, shrink 0.5% |
| 1 | Paired per-year net carry: each crop year's May bid less its own October bid and its carrying cost, averaged | B, a rail site (18.0¢ against C's 14.8¢) | The lender's own method, paired and netted | The contract: the May price is fixed, so the case is the margin over today's harvest bid, not a historical spread |
| 2 | Contract margin over today's bid net of carrying cost × 300,000, times a delivery rate fitted on site-average intake moisture | C, the inland terminal ($63.0k against E's $50.0k) | Forward-looking, priced on the contract, and its delivery fit reproduces the co-op's 91.4% six-season delivered share | The storage log's site-season rows: the site-average fit misses 19 of 60 outcomes |
| 3 | **Decisive:** tickets placed in bins by the fill log's intervals and blended by bushels; a site qualifies only if its worst bin is at or under 15.0%; the best qualifying margin | **E, the north elevator, $57.6k** (5th of six on rung 0) | — | — |

* **Position table.** E is 5th on rung 0 (31¢), 4th on rung 1 (11.5¢) and 2nd on rung 2, 1.26× behind C, the only rung where it is
  second. It leads only rung 3. Rung margins: A over B 1.21×, B over C 1.22×, C over E 1.26×, E over F 1.75×.
* **Discriminator dominance.** C carries a 1.26× value advantage into rung 3. Its worst bin (15.8%) fails the line and its value falls to
  −$21.4k; E's worst (14.7%) clears it, and E stands 1.75× the next qualifying site (F, $33.0k). The rung needs 1.2 × 1.26 = 1.51.
* **Partial correction priced (L3).** A solver who takes the minimum over loads rather than bins (no site with any load above 15%) rules out
  E too, because E received loads at up to 15.6% that blended down, and names F: a different wrong name. A solver who blends at site level
  is at rung 2.
* **Grid.** Price basis (average spread, paired carry, contract margin) × delivery rule (none, site average, any load, worst bin) = 12
  cells. The cells name A, B, C or F; only contract margin with the worst bin names E. The nearest wrong cell is contract margin with the
  any-load rule (F), reached by one wrong unit.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The contract grades loads and takes one origin. The storage guide says to keep grain cool and dry. No document says
   a site is only as good as its worst bin, or how a bin's moisture is formed.
2. **The reproducing rule is a construction, and the corpus pins it.** The worst-bin rule reproduces 60 of 60 site-season outcomes. The
   best rival, no load above 15%, reproduces 44 of 60. The site-average fit reproduces 41 of 60, and its loss curve is flat from 13.9% to
   14.9%, so no threshold rescues it. Bin moisture exists in no file and has to be built from the interval join and the blend, so there is
   no menu to sweep.
3. **No arithmetic symptom.** Tickets reconcile to site intake, intake to bin capacity, and May shipments to contract records. Site-level
   fits pass the co-op's delivered-share total.
4. **Not a row predicate.** It needs an interval join from tickets to bins, a bushel-weighted blend per bin and a maximum per site.
5. **The enumeration is arithmetic.** Which sites qualify is computed. No column holds bin moisture or a qualification flag.
6. **No cutover date.** The bins filled over one harvest, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the site-average fit still names C.

## 6. The calibration corpus

* **Form.** The co-op's storage log: six seasons, 60 site-seasons stored to May, each with its intake tickets (timestamp, bushels,
  moisture at the bin leg), its bin fill log and its May outcome (delivered in full, or the bushels short and sold out of condition).
* **What it pins.** The worst-bin rule, 60 of 60 against 44 and 41 (above). Worst bins of the 42 full deliveries sit at or under 14.8%,
  those of the 18 shortfalls at or above 15.5%, and nothing lies between.
* **The salient control (E16).** The annual reports' six-season delivered share, 91.4% of stored bushels. The site-average fit matches it to
  within 0.3 points because its misses run both ways. Only the site-season rows separate the rules.
* **Twin pair.** Site D in 2021 and site B in 2023 are identical on every site-level column: average intake moisture 14.2%, 612,000
  bushels, eight bins, the same fill window and temperature zone, and the same October bid. Their realised net carry was 29¢ and 13¢ a
  bushel (2.2×). B's 2023 run had one bin at 15.6% that went out of condition in March; D's worst bin in 2021 was 14.6%.
* **Resemblance points at the decoy.** By average moisture, intake size and zone, site C's current season most resembles eleven site-seasons
  that delivered in full.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The contract: 300,000 bushels, one origin site, delivered in May at a fixed price; every load graded at the plant;
  rejected loads become shortfall, bought in at the plant's posted price plus $0.35 a bushel. The marketing policy: the contract goes to
  the site where it earns the co-op most. The carrying-cost schedule: storage per bushel-month by site, interest at prime + 1% on harvest
  value, shrink 0.5%.
* **Empirical pins.** The 15.0% line and the bin unit, from the storage log.
* **Voices.** The merchandiser: "The carry has always paid best at the river sites." The quality manager: "Average moisture tells you the
  site; we dried whatever came in wet." The lender's credit officer: "Show me paired years and the interest, and I'll sign."
* **Licensed wrong basis.** The marketing policy records that the board's finance committee compares sites on the newsletter's average
  harvest-to-May spread and will see that table.

## 8. Determinism by construction

* **Interval join.** Every ticket timestamp falls inside exactly one bin's fill interval; intervals never overlap, and gaps between them
  run at least ten minutes.
* **The line.** In the corpus nothing falls between 14.8% and 15.5%. This season's worst bins are A 15.7%, B 16.1%, C 15.8%, D 15.6%, E 14.7%,
  F 14.4%, so any cut inside the gap returns the same qualifiers.
* **Blending.** Bushel-weighted and dry-matter-weighted blends agree for every bin, because none sits within 0.2 points of the line.
* **Prices.** The contract price, today's bids, freight per site and the prime rate are all filed, so the margin has no window choice.

## 9. Prompt sketch and deliverables

> We have to name the site that fills the ethanol plant's May contract by Friday, and six of our sites have the room. Our merchandiser is
> sure the river sites carry best. Tell me which site gets it and what it should net the co-op, in one sentence for the board, with the net
> in thousands of dollars. Send `carry_site_choice.xlsx`, a chart `site_bins.png`, and a one-page `contract_assignment.pdf`.

* `carry_site_choice.xlsx` — the six sites under the four rung bases (ask C), the propane sheet (ask A) and the basis sheet (ask B).
* `site_bins.png` — for each site, its bins as dots of fill moisture sized by bushels, the 15.0% line labelled, each site's average intake
  as a tick, C's late-filled bin annotated, and the chosen site highlighted.
* `contract_assignment.pdf` — the committed site and its net, and why the driest site on average is ruled out.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the six sites, last season's propane per bushel dried and its cost per point of
  moisture removed. *Device:* dryer propane meters are cumulative, and two sites had a meter replaced mid-season, recorded in the
  maintenance log with the new meter's opening reading. Differencing across the swap produces one large negative and one inflated period.
* **Ask B (device-carried).** For each site's local elevator, the average basis (cash bid less the nearby corn futures) in each quarter of
  the last marketing year. *Device:* bids are quoted against a nearby contract that rolls on the date the market-news report description
  gives, not at month end. Basis against a calendar-month nearby misprices two to three weeks around each roll.
* **Ask C (validity).** Each site's expected value under each of the four rung bases, and the hit count out of 60 for each of the three
  delivery rules.
* **Decoupling.** Clearing the worst-bin rule changes no figure in asks A or B. Propane meters and futures rolls touch no ticket, bin or
  contract record.

## 11. Rubric arithmetic

6 sites × 2 (ask A) + 6 sites × 4 quarters (ask B) + 6 sites × 4 bases + 3 hit counts (ask C) + the committed site, its net, its margin
over F and C's worst bin + 5 named chart parts + 3 files ≈ 75 criteria.

## 12. World-building constraints

* Rung 0 spreads: A 47¢, B 39¢, D 36¢, C 34¢, E 31¢, F 27¢. Rung 1: B 18.0¢, C 14.8¢, A 12.1¢, E 11.5¢, D 9.0¢, F 7.2¢. Rung 2: C $63.0k, E
  $50.0k, B $44k, D $41k, A $37k, F $30k. Rung 3: E $57.6k, F $33.0k; A, B, C and D below zero (C −$21.4k).
* Average intake moisture: C is the driest site, E the wettest of the qualifying two. E received loads up to 15.6% that blended into bins no
  wetter than 14.7%.
* Storage log: 60 site-seasons, 42 full and 18 short, with the gap from 14.8% to 15.5% empty. D-2021 and B-2023 are identical on every
  site-level column.
* Rung leaders A, B, C, E. Propane meters and futures rolls are independent of every main-call record.
