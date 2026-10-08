# AD32 — Which practice group gets the quarter's coding audit, when the upcoding belongs to a billing service that uploads for several groups at once

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · health-system payment integrity |
| Mirrors | Tracing a quality anomaly to the upstream crew that serves many accounts rather than to the accounts it shows up in (outsourced moderation vendors whose decisions surface across many queues at Meta and Google, listing agencies acting for many sellers on Amazon, a contract manufacturer's line feeding several brands) |
| Decision shape | Which of N gets one scarce thing: the quarter's single forensic coding audit goes to one of eight flagged practice groups |
| Committed call | The practice group audited this quarter, and the overpayment the audit is expected to recover over the twelve-month audit period |
| Gap · Pattern | Gap 4 (rule: an assignment recovered at zero tolerance) over Gap 2 (population) · a mixture, not a constant: each group's coded levels mix an outside service's batches with its own, with finer controls separating peer constructions below it |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #17 guesses an attribution the data can settle · #12 stops at the first control that passes · #13 validates on one population, applies to another |
| Calibration form | Retry or revision log: the claim revision log of 14 closed coding audits (2022–2025), with every audited claim's billed and revised level |
| Driving force | Upcoding is not a property of a practice group. Part of each group's visits are coded by an outside billing service that uploads one batch for several groups at once, to the same second; the rest are coded in house. In the revision log all 649 audit downcodes fall on claims that went out in such shared batches, and none of 2,380 in-house claims was ever downcoded. So each group's error rate is a mixture whose weight is this year's share of shared-batch claims, and no per-group constant reproduces the audits. E sends 68% of its high-level visits through shared batches; C, the divergence leader, sends 12%. |

## 1. Situation

A health plan's payment integrity unit has one forensic coding audit this quarter: a team of certified coders reviewing a statistically
sampled set of one practice group's records and extrapolating the overpayment over the last twelve months of claims. Eight practice groups
were flagged by the evaluation-visit level screen. The unit's charter scores an audit on the overpayment it recovers. The unit holds the
visit claims with their clearinghouse submission timestamps, the statewide specialty mix table, its last two quarterly review lists, the
fee schedule and the claim revision log. The medical director believes oncology is where money leaks.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the level shares, the peer mixes, the published review lists, the revision log's audit results and
  the timestamps. The medical director is right that oncology codes high. Nothing is overturned; the difficulty is where the upcoding
  originates, which no field records.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view and the current screen. A peer-divergence build that reproduces every control still names
  C, and a per-group audit rate still names C or D.
* **Instrument repair.** Make every claim, timestamp and audit record perfect: they are. No better record of a group's coding changes the
  fact that a third party coded some of it.
* **Lens swap.** The naive basis is each group's coded levels against its peers; the answer is the subset of each group's claims coded in
  shared batches this year, a different population of claims at a different moment from the audits that taught the rate.

## 3. The driving force

A strong solver drops raw level-5 share, builds the memo's likelihood-ratio divergence against peers, chooses the peer construction that
reproduces the unit's published review lists rather than only the statewide table, and converts each group's excess high-level visits into
dollars. Every step is correct, and each assumes a group codes like itself. The revision log says otherwise. Read claim by claim, every
downcode in 14 audits sits on a claim whose submission timestamp is shared, to the second, with claims of at least two other practice
groups: one upload by an outside service that codes for several groups. In-house claims go out per account and were never downcoded.
Shared-batch shares move a lot from year to year (a group hands its overflow coding out, or takes it back), so a group's last audit rate is
a stale weight, and the twin audits of one group show the rate doubling as its share doubled. The recoverable overpayment is this year's
shared-batch high-level visits × the shared-batch downcode rate × the fee difference.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Level-5 share of established-patient visits: A 41%, B 33%, C 29%, D 27%, E 24% | A, an oncology group | The plan's long-standing screen | The statewide specialty mix: oncology's own peers bill level 5 at 39% |
| 1 | Divergence from peers (statewide specialty table, clinician included in its own peer pool) × fee difference: B $820k, C $640k, A $610k, E $430k, D $390k | B | Reproduces the statewide specialty mix exactly | The last two quarterly review lists: this peer construction misses 17 of their 80 published statistics |
| 2 | Divergence with the construction that reproduces all 80 published statistics (leave-one-out, specialty × place of service) × fee difference: C $760k, E $560k, B $520k | C | Passes the salient control and both finer controls | The revision log: all 649 audit downcodes sit on shared-batch claims, and C codes 88% of its high-level visits in house |
| 3 | **Decisive:** assign each claim to shared-batch or in-house by cross-group co-submission, then this year's shared-batch high-level visits × the revision log's shared-batch downcode rate (0.46) × fee difference: E $640k, B $350k, D $290k, C $210k, A $180k | **E** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (C leads it by 1.36×), and leads only rung 3. Rung leaders beat
  their runners-up by 1.24×, 1.28×, 1.36× and 1.83×.
* **Discriminator dominance.** C carries a 1.36× divergence advantage into rung 3. E's edge on the decisive axis is its shared-batch share of
  high-level visits, 0.68 against 0.12 (5.7×), so the net is 5.7 / 1.36 = 4.2×.
* **Partial correction priced (L3).** A solver who finds co-submission but weights each group by its three-year average shared-batch share
  names D, which handed 70% of its coding out in 2023 and took all but 20% back in 2025; that lands further from E than rung 2. A solver who
  carries each group's last audit rate forward names D as well.
* **Grid.** Measure (share or divergence) × peers (statewide or finer) × recovery (divergence, last audit rate, claim-level mixture) = 12
  cells. Share cells name A, divergence cells name B or C, last-audit cells name D, and only claim-level mixture cells name E.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** No document mentions an outside coder, a billing service or shared uploads. The revision log records claims,
   levels and reasons, and the timestamps sit in the clearinghouse fields of the claim file.
2. **The corpus pins a construction, not a menu (Pattern B).** The claim-level mixture reproduces the downcode count of all 14 audits
   exactly (every downcode on a co-submitted claim, none on an in-house one). The best rival, each group's prior audit rate carried forward,
   reproduces 3 of 14; divergence-based expectations reproduce 2. The assignment is a group-by on exact timestamps across accounts, and no
   lag threshold or weekday rule reproduces it (shared-batch lags run 2–9 days and in-house 1–12, on every weekday).
3. **No arithmetic symptom.** Claims, payments and audit samples reconcile; timestamps are valid; every claim sits under its own group's
   clearinghouse account.
4. **Not a row predicate.** A claim is shared-batch only because other groups' claims carry its exact submission second, so the assignment
   needs a self-join across accounts before any rate is applied.
5. **The enumeration is arithmetic.** Shared-batch membership is computed for 412,000 claims; no column carries it.
6. **No cutover date.** Groups hand coding out and take it back at different times, so no group's series steps on one date.
7. **Survives deletion.** Remove both voices and the screen: the divergence build is still the natural one and still names C.

## 6. The calibration corpus

* **Form.** The claim revision log for 14 coding audits closed in 2022–2025: every audited claim with its billed level, revised level,
  revision date and reason code, alongside the clearinghouse fields of the original claims.
* **What it pins.** Shared-batch claims: 649 of 1,410 audited were downcoded (0.46). In-house claims: 0 of 2,380. The split is absolute, so
  the mixture is the only rule that reproduces every audit's count; both rivals miss in one direction (they over-predict in-house-heavy
  groups), so they fail on the total as well.
* **Every rule exercised.** One audit covers a group coded wholly in house (no downcodes) and one a group coded wholly in shared batches
  (downcodes at 0.46), so both arms of the mixture are identified.
* **Twin pair.** Group F's 2023 and 2025 audits are identical on every visible column: clinicians, specialties, place of service, divergence
  statistic within 1%, visit volume. They found 61 and 128 downcodes, 2.1× apart, because F's shared-batch share rose from 31% to 66%.
* **Resemblance points at the decoy.** By specialty and divergence, C most resembles the three closed audits with the largest recoveries.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The integrity charter: an audit is scored on the overpayment it recovers over the twelve months of claims before the
  audit, extrapolated under the unit's sampling standard. The fee schedule. The revision log as the unit's record of audit outcomes. One
  sentence each.
* **Empirical pins.** The peer construction, from the two published review lists; the claim assignment and the 0.46 rate, from the
  revision log.
* **Voices.** The medical director: "Oncology always codes high; that is where the money leaks." The special investigations manager:
  "Divergence from peers is the only basis that has ever survived an appeal."
* **Licensed wrong basis.** The charter records that the state's program-integrity contractor ranks practice groups on level-5 share and
  will bring its list to the audit committee.

## 8. Determinism by construction

* **Co-submission.** Every shared-batch upload carries claims of at least three groups at one second, and the clearinghouse queues in-house
  submissions per account, so no in-house claim shares a second with another group. Matching to the second or to the minute assigns the
  same claims.
* **Peers.** Only one construction reproduces all 80 published statistics; the statewide table alone admits three.
* **Fee difference.** The fee schedule is fixed for the audit period, and every downcode is by exactly one level, so the dollar conversion
  has no fork.
* **Rounding.** The committed recovery is given to the nearest $10,000, and E's $640k sits mid-bin.

## 9. Prompt sketch and deliverables

> The coding audit team can take one practice group this quarter, and the screen flagged eight. Our medical director is certain oncology is
> where the money leaks. Name the group we audit and the overpayment we should expect to recover, to the nearest $10,000, in a line for the
> audit committee. Send `audit_case.xlsx`, a chart `coding_sources.png`, and a one-page `audit_memo.pdf`.

* `audit_case.xlsx` — the eight groups under each rung's basis (ask C), the attribution sheet (ask A) and the authorisation sheet (ask B).
* `coding_sources.png` — for each group, high-level visits split into shared-batch and in-house bars, the expected recovery as a marker on a
  second axis, the 0.46 shared-batch rate in the subtitle, and the audited group highlighted.
* `audit_memo.pdf` — the committed group, the expected recovery and why each other group falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each group, attributed members at 30 June and twelve-month attribution churn. *Device:*
  attribution changes are effective-dated, and a retroactive correction row with an earlier effective date supersedes the row it corrects,
  as the attribution guide says. Counting current rows misstates five groups. The audit build never uses attribution.
* **Ask B (device-carried).** For each group, prior-authorisation requests in the last twelve months and the share denied. *Device:* a
  withdrawn and resubmitted request keeps its number with a sequence suffix, and the authorisation guide counts one request per number.
  Counting rows overstates requests and shifts denial shares in four groups.
* **Ask C (validity).** Each group's figure under each of the four rung bases.
* **Decoupling.** Clearing the shared-batch assignment and the peer construction changes no figure in asks A or B.

## 11. Rubric arithmetic

8 groups × 2 (ask A) + 8 × 2 (ask B) + 8 × 4 bases (ask C) + the committed group, its expected recovery, the runner-up and the margin + 5
named chart parts + 3 files ≈ 76 criteria.

## 12. World-building constraints

* Rung leaders A, B, C, E with the margins above; E is 5th, 4th, 2nd (1.36× behind C) and 1st.
* Shared-batch shares of high-level visits this year: E 0.68, C 0.12, D 0.20 (0.70 in 2023), B 0.41. Shared-batch lags 2–9 days, in-house
  1–12, both on every weekday.
* The revision log: 1,410 shared-batch audited claims (649 downcoded) and 2,380 in-house (none).
* F's 2023 and 2025 audits are identical on every visible column.
* Attribution records and authorisation requests never touch claims, timestamps or the revision log.
