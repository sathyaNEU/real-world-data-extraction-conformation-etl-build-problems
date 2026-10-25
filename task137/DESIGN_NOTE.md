# task137 design note

Architecture 2, drawn 2026-10-25 (wave 2 slot, Forecasting lane, sathya8571), a re-root after portal round 1.
Architecture 1 (Kaimai Building Society's maturity calls booked in agent-hours with an outsourced contact centre, seed
FC08) was landed on its golden by a portal response: reading each deposit's retention-offer share by the class of the
money is a reflex for the portal's models. Its identity is in the card's lineage and its dead ends below. Nothing of the
seed's world or of architecture 1 is kept, and no banking: this draw is a care home group's emergency admissions for
adverse drug events in the year after a group-wide structured medication review.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task137.json`, architecture v2, registered 2026-10-25T22:29:02Z, v1's two
   rounds in its lineage. `guard.py check` on the registered card: WARN, `three_rules.strategy_risk` only (answered in
   `## Three rules`, `Not semantics:` and `Analyst test:`); the structural tests are NOTE, differentiated on the card
   against task142, task148 (v1) and task173 (v2).
2. Pairing: Healthcare Delivery & Health Economics (client domain) / `utilization-access-demand-forecasting` /
   Forecasting & Predictive Modeling. The deciding quantity is a care population's 2027 emergency admissions for adverse
   drug events, a utilisation forecast whose exposure is pharmacoepidemiology's own: the pairs of interacting medicines
   each resident holds at once.
3. Niche: Calderbrook Care, a care home group in the north of England (34 nursing and residential homes, about 2,400
   beds, six of them acquired in 2025 with their own pharmacy supplier and eMAR system). Between September and December
   2026 a clinical pharmacist team reviewed every resident's medicines (structured medication reviews); each medicine's
   outcome (continued, stopped, reduced, switched) is recorded and dated. The reviews worked from the high-risk
   combinations clinicians screen for in older people, so the medicines they stopped were stopped mostly in the residents
   who held them with an interacting partner.
4. Call and shape: how many emergency admissions for adverse drug events Calderbrook's residents will have in calendar
   2027 (residents during 2027, including the residents the homes will admit in 2027), a count (`quantity_figure`,
   question form how-many), the rounding fixed at stage 2 from the family spread. Shape `02` (forecast across periods):
   the call with its quarterly path and an ask layer counted in `## Ask sheet` at stage 2.
5. Mechanism keys: gap population first (the record's unit is the dispensed medicine line; the harm's unit is the
   interacting pair a resident holds), then time; pattern none, generators G2 (the pair within a regimen against the
   medicine) then G6 (the reviews move the pair mix far from every closed quarter's); Gate G `forecasting`; strategy
   `grain_or_unit`.
6. Layer 2: `estimation_fit`, pattern `own:adverse-events-from-interacting-pairs-in-a-regimen`. The utilisation task
   type's client cards (capped demand, age-specific rates, floating catchments, overdispersed quantiles) leave the
   exposure unit untouched; the field's method for drug harm is exposure to interacting combinations, not to medicines.
7. Furniture: forum `executive_team` (Calderbrook's executive team signs the 2027 contract); forcing event
   `purchase_order_or_contract` (the 2027 enhanced health in care homes contract with the integrated care board, whose
   gain-share pays against an admissions baseline the group proposes for 2027); organisation family
   `hospital_or_health_provider` (a nursing and residential care provider); role family `operations_director` (the
   director of clinical services, who prepares the forecast); context artifact `register` (the residents' medicines
   register: the review outcomes by resident and medicine); calibration `none`.
8. Spine: `dispensing_lines_2023_2026.csv`, one dispensed medicine line for one resident in one 28-day cycle, from the
   two pharmacy suppliers' feeds (dm+d product codes on Fellside Pharmacy Services' feed, BNF sections on the acquired
   homes' supplier's). The forcing file is the review outcomes register. Other files at stage 3: admissions extracts
   from the two acute trusts (ICD-10 with the adverse-event Y-codes in secondary positions), the residents' register
   (admissions to and discharges from the homes, deaths), the acquired homes' eMAR export, distractors.
9. Deliverables: `ade_admissions_forecast_2027.xlsx` and `review_impact_note.docx`, fixed at stage 2 (the set is checked
   against the last three builds then; `guard.py check` raised no repeat on it).
10. People, drawn with `guard.py names --geo "United Kingdom" --seed 137`: Katherine Storey, Hugh Metcalfe, Charlene
    Dale (roles at stage 3; no persona in the prompt). Rachel and Patricia were dropped on `people.first`.

**Data-native sentence.** In the record an adverse drug event admission is almost never the work of one medicine: a
gastrointestinal bleed comes from an anticoagulant taken with an NSAID or an SSRI, an acute kidney injury from the ACE
inhibitor, diuretic and NSAID triple, a fall or respiratory depression from an opioid with a gabapentinoid or a
benzodiazepine, hyperkalaemia from trimethoprim with an ACE inhibitor; a resident holding either medicine alone carries
little of that risk, and the 2026 reviews removed the paired medicine from the residents who held the pairs.

## Three rules

Task type: utilization-access-demand-forecasting (healthcare delivery), which serves Forecasting in the taxonomy: a
care population's emergency admissions in a coming year.
Domain test: the expected count of adverse drug event admissions read from the interacting combinations each resident
holds at once, pharmacoepidemiology's exposure for drug harm (the combinations prescribing screens in older people are
built on), estimated as each combination's excess admission risk on the 2023 to 2026 record and summed over the 2027
residents' post-review regimens.
Swap: "admissions follow the interacting pairs of medicines a resident still holds" with machines for medicines and
breakdowns for admissions reads as nothing: there is no interaction table, and no reason a breakdown should need two
machines in one owner.
Layer 1: two pharmacy suppliers' feeds coded differently (dm+d against BNF sections), an acquired group of homes on its
own eMAR with its own resident numbers, admissions from two trusts with the adverse-event codes in secondary diagnosis
positions, as-required medicines dispensed but not taken daily, hospital stays and deaths interrupting regimens, NHS
numbers on one feed only: each is what these systems produce, none is placed to be caught.
Layer 2: estimation that fits the data (`estimation_fit`): the risk model's unit is the combination, so a per-medicine
model that back-tests cleanly on every closed quarter misprices the one forward period whose combinations the reviews
broke apart.
Decisive step: reading each resident's 2027 risk off the interacting pairs and triples it still holds after the review,
with each combination's excess risk estimated on the residents who held it, rather than off each medicine's average
effect.
Not semantics: reading every field, code and outcome correctly (every admission's adverse-event code, every review
outcome, every regimen) still leaves the per-medicine model on the wrong answer, because nothing in any field says the
risk sits in combinations; the record has to be modelled that way.
Not rule application: no filed rule or procedure sets how admissions are forecast; the reviews' screening criteria say
which combinations to stop, not how admissions follow. Measured on the prototype (`ddi1.py`, three seeds, 2,400
residents a quarter for 16 closed quarters, the review plan replayed on four forward quarters): the enumerated family
(per-medicine logistic, the historical rate, the pair model) spreads from +9.5 to +27.5 per cent around the truth; the
standing family (models whose combination terms the record supports) sits at -3.3 to +0.9 per cent; the ruling-out is
quiet, since the per-medicine model back-tests within noise on every closed quarter (the record's combinations
co-occurred at steady rates). The spread and the rounding are re-measured at stage 2 on the tuned generator.
Analyst test: a strong analyst who links the two feeds to residents, codes every admission correctly and fits each
medicine's own effect on the 2023 to 2026 admissions, then replays it on the post-review regimens, files a 2027 count
about a tenth above the golden (+9.5 to +13.1 per cent on the prototype), because each stopped NSAID, gabapentinoid and
benzodiazepine carries only its average effect across all its holders rather than the pair harm it carried in the
residents who lost it.
Estimand: emergency admissions with an adverse-drug-event code among Calderbrook's residents in calendar 2027, residents
being everyone living in its 34 homes at any time in 2027 (including residents not yet admitted), against the record of
2023 to 2026; filed in the contract schedule the prompt names at stage 2.
No decoy: nothing is planted to be caught; no memo, draft, briefing or stakeholder figure carries the per-medicine
answer.
No certified replay: no certified or published figure blesses either model; the method is open and the record decides
it.
Lesson: drug harm in a population is a property of the combinations its members hold, so a medicines programme that
targets combinations moves admissions further than its count of stopped medicines says; no build on file reads an
outcome off pairs of exposures held inside one member.

## Default path

The reflex: link the two feeds, build each resident's quarterly regimen, fit a logistic (or Poisson) model of an
adverse-drug-event admission on each medicine class (with age, sex and home type), check it on the closed quarters (it
fits every one), replay it on the post-review regimens and the expected 2027 intake. Ends on: a 2027 count about a tenth
above the golden (prototype: +9.5, +12.3 and +13.1 per cent on three seeds; the unchanged historical rate +27 per cent).
Rungs to measure at stage 2: the historical rate carried; the per-medicine model; the per-medicine model with the
review's stopped counts only; the pair model; the pair model with the combinations discovered from the record against
named from the screening list.

## Stump sentence

A competent solver fits each medicine's own effect on Calderbrook's 2023 to 2026 adverse-drug-event admissions,
replays it on the regimens the autumn 2026 reviews left and files a 2027 count about a tenth too high; the step that
lands it there is reading the harm per medicine rather than per interacting combination, so the medicines the reviews
stopped carry their average effect instead of the combination harm they carried in the residents who lost them.

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
