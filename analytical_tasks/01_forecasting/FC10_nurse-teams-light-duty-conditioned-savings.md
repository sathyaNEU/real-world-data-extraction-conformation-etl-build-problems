# FC10 — Where seventeen nurse case-management teams go next year, when the verified saving exists only at employers with light duty

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · workers' compensation insurance |
| Mirrors | Placing capped human-touch interventions where the measured lift was earned (cloud customer-success managers who move only accounts with an engaged admin, Amazon's return-to-work and accommodation programmes, outreach that converts only where a follow-on offer exists) |
| Decision shape | An allocation under a cap: 17 teams of 20 case slots across eight claim segments, at most three teams per segment |
| Committed call | Teams per segment for next accident year, and the ultimate indemnity they save, in $ thousands to the nearest 10, which goes into the loss-ratio pick |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern E (conditioned yield): the verified saving is a dollar amount at employers with light-duty capacity and nil elsewhere, a property of the employer behind a join |
| Gate G mechanism | decomposition_attribution, with binding_constraint support |
| Measured traps engaged | #13 validates on one population, applies to another · #17 guesses an attribution the data can settle · #6 treats a mixed segment all one way |
| Calibration form | Gold-standard verification subsample: 600 randomised pilot claims (300 managed, 300 control), each developed to ultimate and verified by an independent actuarial review |
| Driving force | The pilot's verified result, managed claims 18% cheaper at ultimate, is correct and applies to no segment. Nurse management saves $9,400 of indemnity on a claim whose employer has a record of bringing people back on light duty, and nothing on any other claim. That record is no field. It is an employer having paid temporary-partial benefits in the last three years, built from the payment history and joined through the policy. The pilot drew half its claims from such employers in every industry. Next year's segments run from 10% (construction) to 90% (public sector), so the costliest claims are the least savable. |

## 1. Situation

A workers' compensation insurer has funded seventeen nurse case-management teams for next accident year. Each team carries 20 lost-time
claims at a time, and claims are assigned within eight segments (industry × injury × region), at most three teams per segment. Last year an
independent actuarial review verified the pilot's randomised results at ultimate. The pricing committee will book the forecast saving in
next year's loss-ratio pick, so it needs the allocation and the saving it buys.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the verified subsample, the paid triangles, the claim file, the payment history and the policy
  file. No one's claim about their own numbers is overturned. The difficulty is which saving applies to which claims.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the reinsurer's basis. The verified 18% applied to developed severities still sends nine
  teams to construction and transport.
* **Instrument repair.** Verify every pilot claim perfectly, as the review already did. The 18% stays correct for the pilot's mix and
  stays wrong for next year's segments, whose employers differ.
* **Lens swap.** The naive read and the answer are different populations: the pilot's half-and-half mix of employers against each
  segment's forward mix.

## 3. The driving force

A strong solver assigns every claim to its true region, develops each segment's paid indemnity to ultimate with the paid triangles and
applies the verified 18% to it. That build is careful and it ranks construction backs first, because they are the costliest claims.
But the saving is not a share of indemnity. In the verified subsample it is a dollar amount: $9,400 at ultimate on a claim whose employer
has paid temporary-partial benefits within three years, and nil, within a few hundred dollars, on every other claim. A nurse can only
move a claimant back to work if a light-duty job exists. The pilot drew half its claims from such employers in every industry, injury
type and age band, so every split a solver can make on claim columns returns the pooled figure. The property belongs to the employer.
It is built from the payment history, joined through the policy, and it ranges from 10% of claims in construction to 90% in the public
sector.

## 4. The ladder

| Rung | Construction | Lands on (S1–S8 teams; saving) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | 18% × each segment's average paid-to-date indemnity, segments as stored | 3·3·0·3·0·3·2·3; $3,010k, +46% | The verified effect applied to the insurer's own claims, ranked by what each slot saves | **E19 (a latent attribution marker):** blank-region claims from the TPA feed default to Metro, and the claim-number prefix (the TPA office code) places every one exactly; only prefix regions reproduce last year's filed team caseloads |
| 1 | The same with regions from the prefix | 3·3·3·3·0·3·2·0; $2,990k, +45% | Every claim sits in its true segment, and last year's caseloads tie exactly | The paid triangles: the averages are paid-to-date on immature claims, while the verified 18% is a share of ultimate |
| 2 | 18% × each segment's indemnity developed to ultimate (volume-weighted chain ladder per segment) | 3·3·2·3·0·3·3·0; $3,520k, +70% | The verified effect on the basis it was verified on, the actuarial standard for the committee | The verified subsample joined to employers' payment history: $9,400 per managed claim where the employer paid temporary-partial benefits within three years, nil elsewhere |
| 3 | **Decisive:** $9,400 × each segment's share of forward claims at employers with that history, joined through the policy | **0·0·3·3·3·2·3·3; $2,068k → $2,070k** | — | — |

Segments: S1 construction back (North), S2 construction back (South), S3 manufacturing upper limb (North), S4 healthcare back (Metro), S5
retail lower limb (Metro), S6 transport multiple (South), S7 public-sector back (North), S8 hospitality upper limb (Metro).

* **Figure shape.** Every rung over-books the saving (+46%, +45%, +70%), and the decisive rung brings it down while moving all six
  construction teams elsewhere. Under the true saving, the rung 2 allocation would save $1,421k against the answer's $2,068k.
* **Partial correction priced (L3).** Keeping the percentage form but applying it only at light-duty employers (36% of their ultimate
  indemnity) gives the answer's allocation and a saving of $3,140k (+52%): the right teams, the wrong figure, because it prices the
  costliest claims highest. Conditioning on light duty but measuring shares on the stored regions books $1,814k (−12%).
* **Grid.** Region (stored, prefix) × severity (paid-to-date, developed) × saving (18% pooled, 36% at light duty, $9,400 at light duty)
  gives 12 cells and five distinct allocations. Only prefix regions with the dollar saving reach the answer, and they reach it under
  either severity, because the dollar saving does not scale with severity. The nearest other cell is stored regions with the dollar
  saving, at −12%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The review reports the pooled 18% and the claim-level results. No document mentions light duty, and the policy
   file has no return-to-work field.
2. **Corpus blind for a computable reason.** *In the verified subsample light-duty employers supply 50% of claims in every industry, injury
   type, age band and region, because the pilot drew its employers from the North safety council's return-to-work programme.* Every split
   on claim columns returns the pooled 18%, and only the employer join separates $9,400 from nil.
3. **No arithmetic symptom.** Claims tie to the policy file, payments to the ledger, ultimates to the triangles, and teams sum to 17 under
   every rung.
4. **Not a row predicate.** Light-duty capacity is a property of the employer: any temporary-partial payment on any of its claims in three
   years, built by grouping the payment history by employer and joined to claims through the policy.
5. **The enumeration is arithmetic.** Each segment's forward share of such claims is a count across two joins. No column holds it.
6. **No cutover date.** Employers' light-duty records accumulate over years, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The verified subsample: 600 randomised pilot claims with assignment, employer and policy IDs, injury, age band and verified
  ultimate indemnity.
* **The absolute split (O2).** Managed minus control at ultimate: $9,400 at employers with temporary-partial history and −$200 to +$300 at
  the rest, in every industry and injury cell. Pooled, it is $4,700, or 18% of ultimate indemnity.
* **Twin pair.** Pilot cells "healthcare back, age 40–49" in counties 12 and 31 are identical on every claim column: industry, injury,
  age and wage bands, region and verified severity. Their savings are $7,520 and $3,760 per managed claim (2.0×), at light-duty shares of
  80% and 40%. No claim-column rate reproduces both.
* **Resemblance points at the decoy.** Next year's construction segments resemble the pilot's construction cells on every claim column,
  and those cells saved the pooled 18%.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The claims plan: 17 teams of 20 slots, at most three per segment, claims assigned within segments first come first
  served. The committee charter: savings are booked as ultimate indemnity avoided in the accident year. The claim system's dictionary:
  a blank region defaults to Metro.
* **Empirical pins.** The saving and its condition, from the verified subsample. Development factors per segment, from the paid
  triangles. Regions, from the claim-number prefix, confirmed by last year's caseloads.
* **Voices.** The claims director: "Put the nurses on the expensive claims; that's where the money is." The reserving actuary: "Eighteen
  per cent was verified at ultimate. It's the most reliable number we have."
* **Licensed wrong basis.** The charter records that the reinsurer prices the programme credit on the pooled verified percentage applied
  to ultimate indemnity, and will see that basis in the treaty submission.

## 8. Determinism by construction

* **Light-duty window.** Every employer's temporary-partial history is either within the last 30 months or older than 48, so look-backs
  of three or four years return the same employers.
* **Forward shares.** Each segment's share is measured on its last two accident years of claims through the current policy file. The two
  years agree within two points in every segment.
* **Cut gaps.** Under every rung the segments at each team boundary are separated by at least $180 per slot, so no allocation turns on a
  rounding of severity or share.
* **Development.** Volume-weighted factors with no tail beyond lag 10, as the reserving standard states, and the decisive rung does not
  use severity.
* **Rounding.** The answer's $2,068k is reported to the nearest $10k.

## 9. Prompt sketch and deliverables

> We have seventeen nurse teams for next accident year, and the pricing committee will book whatever saving I put in front of it on the
> 20th. Our claims director wants the nurses on the most expensive claims. Tell me how many teams each segment gets and the indemnity
> they will save, to the nearest ten thousand dollars, and send `nurse_team_plan.xlsx`, a chart `savings_per_slot.png`, and a
> two-page `committee_paper.pdf`.

* `nurse_team_plan.xlsx` — the allocation build for all eight segments, the pharmacy sheet (ask A) and the nurse caseload sheet (ask B).
* `savings_per_slot.png` — saving per slot by segment under the 18% basis and the light-duty basis as paired bars, the seventeen-team
  cut line, each segment's light-duty share annotated, and an inset of the twin pilot cells.
* `committee_paper.pdf` — the committed allocation and saving, and the bases the reinsurer and the claims director will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each segment, last accident year's pharmacy spend per lost-time claim and the share of
  claims with an opioid prescription beyond 30 days. *Device:* the pharmacy benefit manager's reversals post as negative lines in a later
  monthly batch, carrying the original line's reference, as its file layout documents. Summing positive lines overstates spend in every
  segment and flags 40 claims whose long prescriptions were reversed.
* **Ask B (device-carried).** For each of the 14 nurses, last year's average caseload and median days from assignment to first contact.
  *Device:* a reassigned claim keeps its first nurse in the assignment history, with an end date. Crediting claims to the current
  assignee understates four nurses' caseloads and restarts their first-contact clocks.
* **Ask C (validity).** The allocation and booked saving under each of the four rung constructions, and each construction's prediction
  for the twin pilot cells.
* **Decoupling.** Replacing the light-duty condition with the pooled 18% changes no figure in asks A or B.

## 11. Rubric arithmetic

8 segments × 3 (ask A: spend, opioid share, claims) + 14 nurses × 2 (ask B) + 4 constructions × 2 (ask C) + the eight committed team
counts and the saving + 5 named chart parts + 3 files ≈ 77 criteria.

## 12. World-building constraints

* Developed severity ($k): S1 76.8, S2 69.6, S3 41.0, S4 51.7, S5 22.1, S6 48.3, S7 52.2, S8 21.0. Light-duty shares: 10, 12, 45, 85,
  60, 25, 90, 70%.
* Blank-region TPA claims inflate Metro's paid-to-date averages (S8 41 against 20) and deflate S3's (31 against 38).
* Allocations and savings by rung as in the ladder. Under the truth, rung 2's teams save $1,421k.
* In the subsample, light-duty share is 50% in every claim-column cell. The twin cells differ only in their employers.
* Pharmacy reversals and nurse reassignments never touch claims, payments that define light duty, or the triangles.
