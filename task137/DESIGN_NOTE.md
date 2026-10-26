# task137 design note

Architecture 3, drawn and registered 2026-10-26 (wave 2 slot, Forecasting lane, sathya8571), the number's third and last
architecture. Architecture 1 (Kaimai Building Society's maturity campaign booked in agent-hours, banking) was landed on
the portal; architecture 2 (Calderbrook Care's 2027 adverse-drug-event admissions, the care world) lost every decisive
step it held to isolated probes before a pack shipped. Both identities are in the card's lineage and their dead ends in
`## Tried and rejected`; nothing of either world is kept. This draw is Harrowdown Police's forecast of the first-year
detentions at its new city-centre custody hub.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task137.json`, architecture v3, registered 2026-10-26T05:10:19Z on main
   437a0102. `guard.py check` on the filed card: PASS, with NOTEs only (`test.same_puzzle_older` differentiated against
   task133 and task196, `test.same_driver_older` against task133 and task180, `driver.near` 0.25 against this slot's
   never-registered architecture 3 candidate 2).
2. Pairing: Urban & Regional Science (client domain) / `municipal-service-demand-resource-allocation` / Forecasting &
   Predictive Modeling. The deciding quantity is a public service's demand at a new site, the detentions a custody suite
   books in its first year, forecast from the service's demand model over the site's catchment and used to size the
   site's cells and staff.
3. Niche: Harrowdown Police, a metropolitan county force in England (124 wards in five districts, four custody suites:
   Northgate and Eastmoor in Harrowdown city, Southfields and Wendle Cross in the county). The Tanner Street custody hub
   opens on 1 April 2027 and takes the six city centre wards from Northgate and Eastmoor; the fit-out contract signed on
   9 December 2026 fixes its cells and detention officer posts from its planning figure for 2027-28.
4. Call and shape: the hub's 2027-28 detentions to the nearest 250 (`quantity_figure`, how-many); shape `other`: the
   call with its two components (the force's own arrests by the model, British Transport Police's arrests at the hub's
   two stations) and the note's chart, plus asks on the four existing suites' 2025-26 operations for the custody
   healthcare tender, counted in `## Ask sheet` at stage 2.
5. Mechanism keys: gap population (the force's arrest records are not everyone its suites book); pattern none,
   generators G12 (the records' silence about BTP's arrests read as nobody there), G5 (the railway is policed by another
   force, whose custody the territorial force provides), G3 (the records count the force's arrests, the suite books every
   detainee from its wards); strategy `population_selection`; Gate G `forecasting`, not `method_or_model_selection`,
   because the graded object is a forward projection whose history is read correctly and the step is the new site's
   intake rather than a choice between fitted models (task305's judges read its origin set as model selection because
   its call was a site pick).
6. Layer 2: `field_method`, pattern `own:custody-demand-counts-every-arresting-agency-not-the-force-records-alone`.
7. Furniture: forum `executive_team` (the chief officer team signs the fit-out contract); forcing event
   `purchase_order_or_contract`; organisation family `local_government` (a territorial force under a locally elected
   commissioner; `government_agency` is spent against task121); role family `capacity_planner` (Custody Services
   Planning); context artifact `filed_model` (the custody demand model note); calibration `existing_book_actuals` (the
   four suites' arrest records against the model). `committee_or_panel` is spent against task121 as well.
8. Spine: the force's arrest records, April 2021 to September 2026 (about 135,000 rows), one row per arrest by a
   Harrowdown officer. The forcing file is data.police.uk's street-level crime for the force area as the community safety
   partnership downloads it, which carries British Transport Police's crime at the stations; the custody fact sits in
   the custody service's suite allocation notes (stage 2). The asks' files are fixed at stage 2.
9. Deliverables: `tanner_street_planning_figure_2027-28.xlsx` and `hub_planning_note.docx`.
10. People, drawn with `guard.py names --geo GB --seed 137`: Charlene Dale, Hugh Metcalfe, Emma Roberts (Patricia,
    Rachel, Duncan, Rebecca and Richard repeat older builds' first names). None appears in the prompt.

**Spent mechanisms on the ground** (`guard.py mechanisms --objective forecasting --strategy population_selection`, seven
builds): task22 a declining segment masked by inflations of its own base; task132 a wear curve restarted by
replacements; task136 an intervention enrolling units about to take up anyway; task141 outcomes recorded only for the
units a decision-maker let through; task150 arrivals from outside at a steady count beside transfers from siblings;
task168 capped units completed from slow-season builds; task137 v2 short-stay occupants booked through another
organisation's system. None prices a second agency's caseload booked into the operator's own facility.

**Slot screens.** `guard.py slots` on the driver's words returns task117, task179, task134, task182, task190, task194,
task198 and task229, none an outside agency's intake; on the setting's words (custody, police, detention, station,
arrest) it returns task141 (a county detention centre's bed-days, defendants boarded out), task169 (arrests per day out
of custody under a revocation change), task473 (blood draws under a sheriff's agency number) and task273, none a
suite's intake from another force's arrests.

**Probes before the draw.** The candidate was probed before registration on a six-file pack (`t137_a3/probe7` in the
session scratchpad: the planning brief, the model note, the arrest records, the street-level extract, the allocation and
the LSOA lookup; generator `p7lib.py`, seed 7216), call plus the over-24-hour share, by two isolated Opus probes.
- p137i filed 4,500 (4,515.7). It ran model v2 ward by ward, reproduced the published validation exactly (5,904, 3,093,
  7,883 and 7,435), checked pooled growth, a flat level, the last twelve months and a seasonal Poisson, and wrote that the
  street crime file and the LSOA lookup were not needed: the file includes British Transport Police records, and BTP
  detainees are not in the force arrest file and are not counted. Ask 14.8.
- p137j filed 4,500 (4,516). It ran the same model and six alternatives and wrote that the street file has 1,740 of its
  2,022 BTP crimes in the hub wards around the station, that BTP detainees are not in the force's arrest register, and
  that if BTP books into Tanner Street the hub will see extra detentions not captured here; it left that as a caveat.
  Ask 14.8.
Both saw the outside body and dismissed it, the survivor pattern (task305's out-of-region cardholders, task306's
imports). The golden on that pack was 4,750 (4,779.0); two of two missed. Their realism notes are fixed at stage 3: a
possible duplicate pair (two people arrested together, now an ordinary co-arrest pattern); about 750 arrests booked away
from their ward's suite (overflow, kept); demand flat for five years (year-to-year movement, the 2021-22 COVID tail and
ward shifts with their causes); custody references running one to N with no gaps, which p137j read as a complete
booking register (the arrest records are keyed by the force's arrest reference instead); `detention_hours` stopping at
charge (p137i), which ask A turns on.

**The Gate B fact.** p137j's own words, "if BTP books into Tanner Street", are the judge's question, so the fact that a
detainee is booked at the suite serving the ward of arrest, whatever force or agency arrested them, is filed in the files
as the ordinary custody-service fact it is, in the custody service's suite allocation notes among that document's other
operating notes; never in the brief's estimand sentence, never as a pointer, and tested at stage 2 by the single-use and
deletion rules. If filing it turns the probes' caveat into a landing, that is a Gate F failure for stage 4 to catch.

**Data-native sentence.** British Transport Police polices Harrowdown and Kingsway stations, inside two of the six
wards, and with no cells of its own books the people its officers arrest there into the force suite serving the ward;
their arrests are BTP's, so the force's arrest records, on which the custody demand model is built and validated, hold
none of them, and their only trace in the pack is BTP's recorded crime at the stations in the partnership's
data.police.uk extract, about one per cent of the force area's recorded crime and one crime in sixteen in the six wards.

## Three rules

Task type: municipal-service-demand-resource-allocation (Urban & Regional Science), which serves Forecasting in the taxonomy: a public service's demand at a new site from its demand model over the site's catchment, sized to set the site's cells and staff.
Domain test: The deciding quantity is the hub's first-year detentions worked the way custody planning works a suite's demand, every detainee the suite books counted by the agency that arrested them and carried forward from the catchment's record; the hub's catchment holds two railway stations policed by British Transport Police, which has no cells of its own and books its arrests into the territorial force's suite for the ward, so the demand is the force's own arrests by its model plus BTP's arrests sized from BTP's recorded crime at the force's own arrests per crime by offence type, which moves the planning figure from 4,500 to 4,750.
Swap: "the hub books another police force's arrests at the stations in its wards" put into a hospital's admissions or a utility's megawatt-hours loses its mechanism: no second health service admits patients with no beds of its own and hands them to the nearest hospital by ward, no utility's load is metered by another company that books it into the first's substations, and neither converts another body's recorded incidents into its own intake at an incident type's arrest rate.
Layer 1: the arrest records' UTC clock against UK-time financial years, arrests booked away from their ward's suite when a suite is full or closed, co-arrests booked minutes apart, data.police.uk's anonymised map points and LSOAs rather than wards with two reporting forces in one file, a best-fit LSOA to ward lookup, arrest offence groups against data.police.uk's crime types with a warrant, recall or breach group that has no crime type; each is what these systems produce, and none carries the call.
Layer 2: field_method: the demand model's population is every detainee booked into the suite, so the force's own arrests, modelled and validated on four suites, are completed by BTP's arrests at the hub's two stations, sized from BTP's recorded crime there at the force's own arrests per recorded crime by offence type.
Decisive step: carrying British Transport Police's arrests at Harrowdown and Kingsway stations as the second population of the hub's demand, each crime BTP recorded there in 2025-26 at the force's own arrests per recorded crime of its type, rather than taking the force's arrest records as everyone the hub will book.
Not semantics: every field reads as what it is: the arrest records hold the force's officers' arrests, the street-level file names the force that recorded each crime, and the allocation notes say a detainee goes to the ward's suite whoever arrests them; no field, code or definition says that BTP's arrests are missing from the model or how many there are, and the analyst who reads all of it correctly still counts the force's arrests, as both probes did.
Not rule application: the model note files the WHAT (a suite's demand is the people arrested in the wards it serves) and the HOW for the force's own records (each ward's latest year carried at its capped three-year change), and no rule says which arrests the records omit or how to size them, so executing every filed rule over the arrest records files 4,500. Family measured on the probe pack: the enumerated own-arrest family (nine constructions: the model with and without its cap, Holt-Winters, the latest year, the three- and two-year means, a five-year trend, the last twelve months, the latest year at the force's change) spreads 4,418 to 4,516, every member printing 4,500; the standing family that carries BTP (twenty constructions: five own-arrest bases by four sizings, per-type rates with and without the warrant share, the force's overall rate and the hub wards' overall rate) spreads 4,688 to 4,806, every member printing 4,750; what rules the frame out is no filed clause but the record, BTP's 1,740 crimes at the two stations in the street-level file read with the allocation notes' routing by ward of arrest, and nothing names it.
Analyst test: A strong analyst who reads every file correctly runs the custody demand model over the six wards' arrest records, confirms it on the four open suites (each forecast within 3 per cent), cross-checks a trend, Holt-Winters and the latest year and files 4,500, where the golden is 4,750; checks.py runs both on the generator's clean truth and on the pack.
Estimand: the detentions the Tanner Street hub will book from 1 April 2027 to 31 March 2028 (the brief), a suite's demand being the people arrested in the wards it serves (the model note, 2.1), each detainee booked at the suite serving the ward of arrest whichever force or agency arrests them (the allocation notes).
No decoy: nothing is planted: the arrest records are the force's own, the street-level file is data.police.uk's, the allocation is the custody service's; no memo, draft or figure argues for a count, no file states a figure for the hub, and no stakeholder figure is set up to be overturned.
No certified replay: no certified or published figure sits in the pack to be reproduced; the model's validation table is its own back-test on the arrest records, and the sizing of BTP's arrests is recovered from no figure.
Lesson: a custody suite's demand is every detainee booked into it, while a territorial force's arrest records hold only its own officers' arrests; where another force works inside the catchment with no cells of its own, as the railway police do at a city's stations, its arrests are demand the force's model never sees, and its own recorded crime read at the host force's arrests per crime is what prices it; no build on file prices a second agency's caseload booked into the operator's own facility.

## Default path

1. Read the brief and the allocation: the six city centre wards move to Tanner Street on 1 April 2027.
2. Count each of the six wards' arrests in the force's records by UK-time financial year, converting `arrested_utc`.
3. Run the custody demand model as filed: each ward's 2025-26 arrests carried two years at its three-year average
   change, capped at 10 per cent a year, summed over the six wards.
4. Re-run the model's validation from 2024-25 and reproduce its table; cross-check Holt-Winters, the latest year, a trend
   and the last twelve months, all in the same printed cell.
5. Read the street-level file as context: BTP's rows are BTP's crimes and its detainees are not in the force's records,
   so they are left out.

Ends on: 4,500 (4,515.7 on the probe pack)
Golden: 4,750 (4,779.0 on the probe pack)

## Stump sentence

A competent analyst runs the force's validated custody demand model over the six wards' arrest records and files 4,500,
where the golden is 4,750; the step that lands it there is taking the force's arrest records as everyone the hub will
book, when British Transport Police officers policing Harrowdown and Kingsway stations, inside the hub's wards, have no
cells of their own and book their detainees into the force suite serving the ward, about 260 a year from the 1,740
crimes they record there, which sit in data.police.uk's street-level file and in none of the force's records.

## Tried and rejected

- The seed's architecture (FC08): the vendor's standard dialling rules withheld from the contract and recovered from its
  acknowledgements, with the callable-number count behind two number-level joins as the decisive unit. Rejected at the
  draw: a rule recovered from settled records is banned as the decisive step, and with the rules filed the callable
  count is rule application; the wash stays as depth on the default path.
- A first card in the seed's world as a bank (`financial_institution`, context artifact `operations_log`): blocked by
  the guard against task128, live beside this build (a Canadian bank's collections centres); the deposit-taker became a
  New Zealand building society and the context artifact the block-order thread.
- The coming list's special as the 2024 three-year special (5.65 per cent onto a 3.00 per cent card): the latest
  campaign's share by term and the share by locked rate within term landed 2 to 3 per cent under the golden, because the
  2026 campaigns' three-year deposits, opened at the 2023 peak, met the same drop. Moved to a 2023 four-year special,
  whose past four-year peers all locked in the 2021 and 2022 lows; every term-based rival now lands 19 to 28 per cent
  short.
- Hours to the nearest 100: with the list's drops on thin past support (0.25, 0.55, 1.50 points) the estimator corridor
  (bands of 0.2 to 0.5 at offsets, logistic, isotonic) spread 110 to 230 hours. The 2027 card was set so the list's
  drops sit on dense past drops (0.45, 1.35, 2.00, 2.30, 2.50), and the block moved to multiples of 250 (SOW 2.2,
  procedure 6.1).
- Hours to the nearest 500: the locked-rate and trend rivals landed all three months, and rounding each month to 500
  stopped the months adding to the block.
- Extract notes that said the certificates in the holdings view were moved to the core and what MIGRATED means: they
  narrated Ask B's overlap; the notes now describe the files' fields only.
- Forum `line_manager_or_team` (the head of deposits signing the block order alone): task136 moved its forum to the same
  key after this card was registered, and `ban.forum` blocked; the Deposits Committee now approves the block.
- Write-up figures rounded coarser than they read: the list's retention-offer share to the nearest 5 per cent (60,
  against 62.1) and its non-reaching dials to the nearest 500 (67,500, against 67,354.8); the judge read both as wrong.
  Now whole per cent and nearest 100 (62, 67,400), with freeze.py allowing the two keys
  (`components.retention_share_pct`, `steps.non_reaching_dials`); the Final Recommendation and Critical Components move
  only by that 60 to 62.
- The judge's wording for the Ask A clause (a deposit counts if any of its maturity proceeds were in a society term
  deposit, its principal the amount in term deposit then): "maturity proceeds" is the transfer extract's narrative and
  points at Ask A's device, and "the amount on term deposit then" reads as the new deposit's whole balance, new money
  included (the whole-principal stop). Filed as: counting a deposit if any of its principal was, and only the part that
  was.
- Round 1 shipped design: weak per the 10/10 audit (COMPLIANT_WEAK), because its decisive step, the share of
  conversations going to the retention offer conditioned on each deposit's drop from its locked rate to the card, was
  the strong model's reflex and the field's textbook model: a logistic of the retention outcome on term with a separate
  locked-rate slope per term booked about 5,496 hours, inside the golden's 5,500 bin, without reading any card; the
  share by locked rate sat one bin under; Ask B's migration batches file announced the overlap and an account-level
  dedup against it cracked the ask; Ask A's clause (a deposit counted if any of its principal was kept, and only that
  part) signalled the partial-move device; and the swap test passed only narrowly (insurance renewals priced off a rate
  card read almost the same). Round 2 keeps the world, the call and the asks' populations and moves the decisive step
  to the class of the money, a reason only deposit repricing behaviour has.
- A market-gap stump for round 2 (each deposit's locked rate against a published market rate for its term and opening
  month, the deposits far above the market leaving): the market table made the premium a visible column and the step
  one join (readability tests 2 and 6); the class is rebuilt from each list's own cohorts instead, with no table naming
  it.
- Other round-2 candidates for the decisive step, dropped at the draw: the term structure of the card alone (still the
  drop, read term by term, the reflex the audit measured); the best card across terms as the rate a deposit is compared
  with (a second reading of the rate it reinvests at, a fork and never a stump); money above the Depositor Compensation
  Scheme's per-depositor cover leaving at maturity (a filed limit executed on a visible principal column, rule
  application read off the schema).
- Round 2's first prototype kept round 1's January to March 2027 card (four years 3.15 per cent, so the special's drop
  was 2.50 points): past special money dominated the 2.50 band, so the share by drop alone booked near the golden, and
  the locked-rate-by-term logit carried the special's deposits at about 0.8. The 2027 card was turned up (four years
  4.00, a drop of 1.65), a band in which past conversations are 89 per cent member money.
- The card's gap reordered to population first: `guard.py check` blocked on `test.same_driver` (population, E,
  forecasting against task124's lineage) and `test.same_puzzle_older`; the gap stays time then population, the honest
  order for a premium that lapses at first maturity.
- January's share of the 2023 four-year special's sales at 0.242: January's hours sat near a rounding edge and the drop
  and term logistic landed January's bin (1,250); the sales by month are now 0.184, 0.408 and 0.408, January's golden
  1,206.9 and that rival's January 1,000.
- Ask B at six figures (each month's maturing principal on and off the list): with Ask B the most obvious device, the
  cracker's pair ceiling rose to 41; cut to four figures (the three months and the quarter's part not on the list),
  39.0.
- Ask A's device as a posting date (D8, maturity proceeds posted on the next business day): the hygiene battery's
  unmatched-join count found it at once; moved to the payments system's settlement account with the matured deposit
  named only in the narrative (D7).
- The write-up's past share for member money (15 per cent, 14.57 unrounded) and all past conversations' share in the
  special's band (35 per cent, 34.55): both within 0.07 of a rounding edge; dropped from figures.json, the write-up, the
  note and the workbook, the band given by class instead (88 and 28 per cent, 0.24 and 0.18 from an edge).
- The note's chart title "Seven in ten hours are conversations, most of them retention offers": under the round-2
  shares January's conversations go to the offer 45 per cent of the time and the retention offer's minutes are under
  half the talk in January and March; retitled to the measured two-thirds (0.665 to 0.693, asserted).
- Band shares as a Critical Component (88 against 28 per cent at drops of 1.50 to 1.75): a corridor member (special
  money pooled, a logistic within each class) never computes them; the component keeps the class's 87 per cent and the
  bands stay in the steps.
- Portal round 1 (2026-10-25): response 1 landed the call exactly, 5,250 agent-hours (1,250, 2,000 and 2,000 by maturity month), so reading each reached holder's retention-offer share by the class of the money (the 2023 four-year special's block at 5.65 per cent against its cohort's 5.15) is a reflex for the portal's model, as the drop was for the audit's; with both the drop and the class spent, the world's deposit behaviour layer has no decisive step left, and the one structural step it still holds (a reached holder's conversation settling the holder's later deposits on the list, so hours follow holders, not deposits) reads the same with a clinic's reminder calls, a backdrop by the swap test.
- Re-root to architecture 2 (2026-10-25): architecture 1 spent on portal round 1 (above); the slot moves to a new
  cell, healthcare-delivery-health-economics / utilization-access-demand-forecasting, with nothing of the seed's world kept.
- Architecture 2 draw, coastal high-water flood days in 2027 from the window's astronomical tide plus skew surge
  (climate-weather-extremes): dead on the slots screen, it is task178's architecture 1, spent at Gate F when a scored
  reader conditioned on the 2027 tide table; the prototype (`tide.py`) had shown 2027's tide-only exceedances 15 to 25
  per cent under 2026's at a semidiurnal port.
- Architecture 2 draw, candidates killed on the lane's dead lists before code: bike-share pairs and pupil yield by
  estate age (task170's ninth cell), event prediction and illness-death states (task171, task174), the disposition
  effect in listings and notification habituation (task177's rate-by-state screens), vacancy chains (too close to
  task166's live junior-on-senior driver), OR-list overruns and clinic slot cascades (task170's replay law).
- Architecture 2 draw, a liability book's back-loaded accident year (`res1.py`, two seeds): the accident-year chain
  ladder missed by -36 to -42 per cent but Bornhuetter-Ferguson and frequency-severity on earned exposure landed within
  5 to 14 per cent: the textbook fallback for an immature year is the golden, so dead.
- Architecture 2 draw, warranty claims on a months-in-service clock a new retail channel delays (`war1.py`, two seeds):
  the shipment-clock default missed by only -2 to -5 per cent; dead on lever.

- Interacting pairs as the decisive step (the registered card's, 2026-10-25, restarted thread): a strong enumerator's own
  pick, so on the enumerable chain. On the generator's world a logistic with the canonical pairs wins out of sample
  (log-likelihood -1,629.7 against -1,741.2 per medicine and -1,641.8 for every two-way pair, 2023 to mid-2025 fitted,
  the next nine months scored), and replayed on the regimens the reviews left it files 191 admissions against the
  golden's 343; the pairs stay as a rung any solver climbs, and the decisive step moves to the stopped medicines'
  restarts.
- The dead thread's restart world with the programme counting as each resident's annual review: the 2027 annual reviews
  then all fall in October to December 2027, and leaving them out filed 9 per cent high, a fork between two readings of
  the procedure; the programme is now additional to the annual review, which continues in its usual month, so an
  implicit stop hazard over every month and explicit 2027 reviews agree within 1 per cent (345.4 against 343.0).
- Start hazards scaled by frailty: the pooled restart clock then sat 3 to 6 per cent under the truth, so a frailty-
  stratified estimator would have crossed a bin; the start and restart hazards are frailty-free and the record's clock
  recovers the truth within 1 per cent.
- Pair partners stopped only where the pair is held, with small main effects for NSAIDs and benzodiazepines: the per-
  medicine model with a pooled start hazard landed within 1 per cent of the golden (two errors of opposite sign); the
  criteria now stop NSAIDs and benzodiazepines in every regular user, their own effects carry most of their harm, and
  that route sits at 329 (4 per cent under).

- The restart clock as the decisive step (the stopped medicines restarted on the record's clock from each earlier
  stop), probed 2026-10-26 on a six-file pack (golden 343.0, nearest 25 = 350; frozen 191 to 220, pooled Markov 295):
  two isolated Opus call-only probes landed it, p137a at 350 (355.4) and p137b at 350 (361.9), each with a monthly
  Poisson rate on the month's medicines and their combinations, frailty and care type, validated on October to December
  2026, every medicine switched month by month with recent stoppers restarting faster and about three in ten stopped at
  an annual review, a leaving hazard and a microsimulation, back-tested on the 2024 and 2025 year-start cohorts within 2
  to 5 per cent. Any transition the record shows as a rate gets measured; dead. Their realism catches carried forward:
  the programme stopped 93 per cent of the NSAIDs and benzodiazepines it reviewed against 31 per cent at annual reviews
  under criteria the schedule called the same; no annual reviews after 26 October 2026; 24 admissions overlapping the
  person's previous stay; discharge dates after the pull.
- The blanket-programme restart curve (the programme's stops restarting like Ferncliffe's 2025 blanket programme rather
  than like selective annual-review stops), prototyped 2026-10-26 before a probe: the pooled clock landed 9 to 17 per cent
  under it and the per-medicine model with the pooled clock within one bin (two errors of opposite sign); set aside
  unprobed for the coordinator's evidence from five probe deaths: every dead step put the decisive attribute on the frame's
  own units, where a thorough modeller joins it and measures it, and the survivors (task305, task306) carry a body the
  frame does not hold; re-registered on the step-down guests.

- The step-down guests as the decisive step (re-registered 2026-10-26, d1f3551d), probed on a six-file pack (probe3):
  Opus probe p137c took the step, filing 500 (502.4) as 407.4 for the long-term residents plus 95.0 for the step-down
  guests (37 drug-event readmissions over 23,576 occupied bed-days, 180 beds at 92.1 per cent occupancy), because Annex A
  split each home's beds into long-term and step-down. No honest rebuild hides them: the golden is determinate only if a
  file states the 2027 step-down beds (an annex, a bed plan, a purchase order or a registration variation), and the
  probe cross-matched every file by NHS number (it found the 81 guests who became long-term residents, none on the
  register); if the trusts' returns carry the guests, they are an unmatched block, and if they do not, the guests' rate
  has no determinate source (an analogue choice is a fork). Dead in this world.
- The households other councils placed in Hartmoor's hotels and hostels as the decisive step (architecture 3's first
  candidate, a borough council's 2027 Part 7 assessments; probe pack probe5, golden 1,400 against the frame's 1,200, never
  registered): Opus probe p137f landed it exactly, 1,400 (1,383) and both asks. The block bookings showed as 655 s208
  notices in Q4 2026 against about 20 a quarter, and normalised addresses linked 151 of the 324 earlier placed households
  to later cases (47 per cent, about 27 per cent within a year), a direct analogue in the same files, carried to the 2027
  window by a Kaplan-Meier curve. Every landing so far had an anomaly that invites a look plus an analogue a join can
  measure; the next candidate keeps the outside body steady and quiet, applies a validated model to a situation the
  record's units never had, ties the body to the quantity by an indirect domain link, and forces its size and rate from
  ordinary data with other uses.
- The serving personnel beside a new urgent treatment centre as the decisive step (architecture 3's second candidate,
  Harrowdown ICB's Wexley UTC, 2027 attendances; probe pack probe6, golden 12,500 against the model's 11,000, never
  registered): Opus probe p137h landed it, 12,500 (12,456.7) and the ask. It ran the model as filed (10,846), then
  calibrated the open centres' other attendances as 0.98 per cent of ICB attendances plus 0.99 times the model's demand
  for the census defence population, a fit that matched all three centres and explained Tolland's higher share by the
  RAF station; it knew the personnel are registered with Defence Medical Services, and it excluded the prison and the
  halls students correctly. Defence was the communal establishment table's largest category, and the open centres
  carried enough of it to calibrate the rate. The next candidate's outside body is small wherever the solver can
  measure it, absent from the open units, concentrated on the new one, and sized from data the model does not use.

- Re-root to architecture 3 (2026-10-26): architecture 2, the care world, is spent on probes (the pairs, the restarts and
  the step-down guests above), so the number moves to urban-regional-science / municipal-service-demand-resource-allocation
  with nothing of Calderbrook kept; architecture 3's first two candidates (above) died at the probe gate before
  registration, and the third, Harrowdown Police's Tanner Street custody hub, was missed by both probes (`## Draw`).
