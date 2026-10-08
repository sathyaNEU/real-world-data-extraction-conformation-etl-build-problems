# AD01 — Which trust gets the region's one external mortality review, when the deaths it should find are counted at the hospitals patients were moved to

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · health-system administration (hospital quality oversight) |
| Mirrors | Crediting failures to the stage where they begin when every monitor counts them where they surface (incident ownership along microservice call chains at cloud platforms, order defects charged to the last-mile carrier instead of the origin warehouse in marketplace fulfilment, app crashes blamed on the last module on the stack at Apple and Google) |
| Decision shape | Which of N gets one scarce thing: the region's single twelve-month external mortality-review engagement |
| Committed call | The one acute trust whose non-elective adult medical care the review team examines next year |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · S7, every screen is right and the answer is what nothing flags, at transfer-chain grain, with Pattern B (the retry log pins the chain construction) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #14 coarsens the segment it was asked about · #1 reports a failed back-test, ships anyway · #18 joins only on the visible key |
| Calibration form | Retry or revision log: the rapid-review retry log, 34 closed reviews and 47 attempts over five years, with each review's confirmed avoidable deaths |
| Driving force | Every death is counted against the patient's last spell, so a trust that transfers deteriorating patients late exports its avoidable deaths to whichever hospitals receive them, a few to each, and its own figures look ordinary. Only chains of spells linked across trusts by patient key and a hand-over gap of hours, credited to the trust where the chain began and set against that first spell's risk, concentrate those deaths, and only that construction reproduces the retry log. |

## 1. Situation

A regional health board replaces its six-week rapid mortality reviews with one twelve-month external engagement, and it can fund one for
next year across the region's eight acute trusts. The board's quality monitor exports five flags per trust for the last 36 months, each a
correct measure: the overdispersion-adjusted SHMI funnel z, the weekend-admission mortality ratio, the palliative-coding share of deaths,
the 30-day emergency readmission ratio and the share of deaths occurring after discharge. Each flag is high somewhere, and each high flag
has a documented service reason. The committee chair wants the engagement sent to the trust in the funnel's alarm band.

## 2. Gate G: why this is legal

* **Litmus.** Every flag is computed correctly and is labelled in the export as a description of the last 36 months, not a referral
  ranking, and every high flag has a documented, legitimate cause. The chair's reading of the funnel is a correct reading of the funnel.
  Nothing reported is wrong and no stakeholder's read is overturned; the answer is a population the monitor's last-spell grain cannot
  express.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chair's preference and the monitor export. The episode records still credit each death to the last spell,
  and every trust-level analysis built from them still misses the trust where the chains begin.
* **Instrument repair.** Recompute every flag from perfect coding and a perfect case-mix model; they are already correct. A better
  trust-level instrument still counts a death where it happens, so it still cannot see a pathway that begins at one trust and ends at
  another.
* **Lens swap.** The naive read is spells grouped by the trust of the last spell. The answer is multi-trust chains grouped by their first
  trust: a different population, not the same spells under another lens.

## 3. The driving force

A strong solver distrusts the coarse SHMI, rebuilds the funnel on the remit's segment, removes palliative spells, runs a risk-adjusted
CUSUM for recency, and each step is competent. All of it is built on spells credited to the trust where the patient's last spell sat,
which is the indicator's documented convention and the natural grain of the episode file. Trust E, a district general hospital with no
level-3 critical care, transfers deteriorating patients late. They die at the regional centre and at three neighbours, a handful at each,
inside those trusts' noise, and E's own in-hospital mortality is unremarkable. The transfers carry no flag: the regional extract records
only the admission method, and a transfer arrives at the receiving trust as an emergency admission. Seeing it means linking spells across
trusts on the regional patient key, cutting the links at a gap of hours, crediting each chain's death to the trust where the chain began
and setting it against the risk the case-mix model gave that first spell. Nothing in the pack invites that self-join. The retry log is
reproduced by it and by no trust-level screen.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Overdispersion-adjusted funnel z on each trust's SHMI, all spells, 36 months | A, the regional cardiothoracic centre (z 3.3) | The published methodology, the monitor's own headline, and A sits outside the 99.8% limit | The board's remit confines the engagement to non-elective adult medical care, and 71% of A's excess is elective cardiothoracic surgery |
| 1 | The remit's segment: funnel z rebuilt on non-elective adult medical spells from the episode file, consultant episodes collapsed to spells | B, a trust with an inpatient hospice unit (z 2.9) | The segment the remit names, built at the grain the methodology defines, where the monitor only offers an all-spell table | The commissioning register lists B's 20-bed hospice unit, whose admissions hold all of B's segment excess; the retry log back-test reads 19 of 34 |
| 2 | Risk-adjusted CUSUM on the segment, palliative spells excluded, latest 12 months | C, the trust running the weekend hyperacute stroke service (peak 1.9 × the decision interval) | Recency-aware, palliative-clean and sequential: the monitoring textbook's answer to "is it still happening" | The ambulance service's diversion protocol routes every weekend stroke to C, and all of C's CUSUM signals are those spells; the retry log back-test reads 23 of 34 |
| 3 | **Decisive:** chains of spells linked across trusts (same patient key, next emergency admission within hours of a discharge elsewhere), each chain death credited to the chain's first trust, excess over the first spell's modelled risk, segment only, latest four quarters | **E, a district general hospital** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (z 1.2), 4th on rung 1 (z 1.4) and 3rd on rung 2 (1.2 × the interval), and leads only rung 3.
  Intermediate leaders beat their runners-up by 1.27×, 1.26× and 1.27×.
* **Discriminator dominance.** C carries a 1.58× CUSUM advantage over E into rung 3 (1.9 against 1.2). On chain-origin excess E holds 38
  deaths to C's 2, an edge of 19×, far beyond 1.2 × 1.58 = 1.90. E's margin over the rung-3 runner-up G (17) is 2.24×.
* **Partial correction priced (L3).** A solver who builds the chains but counts chain deaths by first trust without setting them against
  the first spell's risk names G, the largest sender (66 chain deaths against E's 52, 1.27×), whose chains die at the expected rate. A
  solver who builds chains and credits each death to the trust that held the patient longest names A again, the rung-0 name, because
  critical-care stays are long. Both land further from E than rung 2 does.
* **Grid.** Segment (all spells or remit) × grain (last spell or chain) × chain measure (death count or excess over first-spell risk) gives
  six feasible cells. Last-spell cells name A or B; chain-count cells name G on both segments; chain excess on all spells names A, whose
  post-surgical step-down transfers carry elective deaths the remit excludes. Only chain excess on the remit's segment names E, and the
  nearest wrong cell (A) is reached only by ignoring the remit's segment clause.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The methodology states the last-spell attribution as a convention of the indicator. The remit says the engagement
   is judged by the avoidable deaths its reviewers confirm in the reviewed trust's care. No document mentions transfers, chains or where a
   pathway begins.
2. **The corpus pins a construction, not a menu.** Chain-origin excess reproduces 34 of 34 retry-log outcomes; the best rival, the segment
   CUSUM, reproduces 23 of 34, and every screen a solver sweeps at trust grain (the five flags, their composite, segment and palliative
   variants, the CUSUM) tops out there. The reproducing rule cannot be reached by sweeping columns, because its unit, the chain, exists in
   no file until a cross-trust self-join on patient key and hand-over gap builds it.
3. **No arithmetic symptom.** Episodes collapse cleanly to spells, spells reconcile to the monitor's denominators, deaths tie to the death
   register, and every death is counted exactly once under every rung.
4. **Not a row predicate.** It needs a self-join of spells across trusts, an ordering of each patient's spells in time, a gap cut, crediting
   to the first element of each chain, and a sum of modelled risk over chains.
5. **The enumeration is arithmetic.** Inter-trust gaps between one discharge and the next emergency admission are either under 4 hours
   (transfers) or 2 days and longer (readmissions), with nothing between, so every cut from 5 to 47 hours builds the same chains.
6. **No cutover date.** E's late transfers run at a steady rate through all 36 months; no series steps. The only dated event in the pack,
   the start of C's weekend diversion, sits under the decoy.
7. **Survives deletion.** With every voice and the monitor export removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The rapid-review retry log: 34 reviews closed from 2021 to 2025, each a trust-year, 47 attempts in all. Each of 13 reviews
  that confirmed nothing on the first attempt was retried with a doubled case-note sample, and none of the 13 retries confirmed anything.
  Each closed review carries its confirmed avoidable deaths (0 in 21 reviews, 9 to 31 in the other 13), and the episode records for the
  reviewed years ship with it.
* **What it pins.** Chain-origin excess reproduces all 34 outcomes: every confirmed count within ±2 deaths, and every unconfirmed review at a
  trust whose chain excess was 3 or fewer. Trust-of-death excess over-predicts the confirmed total by 74% (412 against 237), because it
  books the receivers' model shortfalls as deaths to find; the best rival's misses are all confirmed reviews it left below its alarm line.
* **Twin pair.** The 2022 review of Kellow Bridge and the 2023 review of Sandmere are identical on all five flags, the segment funnel z, the
  CUSUM peak, trust type, bed base and catchment. Kellow Bridge confirmed 24 avoidable deaths and Sandmere 11, matching their chain-origin
  excess (24 and 11); no trust-level field separates them.
* **Every rule exercised.** One confirmed review involves three-trust chains, so crediting the immediately preceding trust instead of the
  first misses it by 9 deaths. One unconfirmed review is at a trust with many chain deaths at expected risk, which refutes the chain count.
  One review's patients include readmissions three days after discharge, which are not chains and confirm nothing.
* **Resemblance points at the decoy.** By flag profile E most resembles six district-general reviews that confirmed nothing; C's
  weekend-heavy profile resembles the confirmed 2021 review of Fenwold.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The remit: the engagement examines non-elective adult medical care and is judged by the deaths its reviewers confirm as
  avoidable in the reviewed trust's care. The remit's annex lists the 38 diagnosis groups that make up the segment. The data dictionary:
  the patient key is the regional pseudonymised identifier, the same at every trust.
* **Empirical pins.** The hand-over gap (from the absolute split), crediting to the first trust and the first-spell risk basis (from the
  retry log).
* **Voices.** The committee chair: "The funnel is what every region uses; I won't argue with an alarm." The regional clinical lead: "Weekends
  are where we lose people, and C's weekends worry me."
* **Licensed wrong basis.** The remit records that the national quality regulator ranks trusts on the overdispersion-adjusted SHMI funnel
  and will present its alarm list at the planning meeting.

## 8. Determinism by construction

* **Linkage gap.** No inter-trust gap falls between 4 hours and 2 days, so every cut in that range builds the same 3,906 chains.
* **Risk basis.** Setting chain deaths against the first spell's risk or against the risk summed over the chain's spells gives the same
  order in every corpus year and the live year (E first by at least 1.9×).
* **Window.** The latest four or eight quarters give the same leader, because E's practice is steady.
* **Maturity.** The extract is taken 45 days after the last discharge in the window and death registration lags at most 14 days, so every
  30-day post-discharge death in the window is present.
* **Spell grain.** Episodes carry a spell ID, so collapsing to spells is a key group-by with no convention. Overdispersion and winsorising
  follow the shipped methodology, which every rung uses identically.

## 9. Prompt sketch and deliverables

> Next year's external mortality review can go to one trust only, and our committee chair would send it to whichever trust sits in the
> funnel's alarm band. Tell me the trust, in one sentence I can read into the board minutes. Send `review_allocation.xlsx` with the sheets
> below, a chart `pathway_deaths.png`, and a two-page `allocation_note.docx` that names the trust and says why each of the other seven is
> not it.

* `review_allocation.xlsx` — the allocation build, the critical-care sheet (ask A), the handover sheet (ask B) and the screen back-test
  (ask C).
* `pathway_deaths.png` — a first-trust × trust-of-death matrix of chain deaths for the eight trusts, shaded by excess over first-spell risk,
  with the named trust's row outlined, each trust's own in-hospital excess as a side bar, and an inset histogram of hand-over gaps marking
  the empty band between 4 and 47 hours.
* `allocation_note.docx` — the committed trust and why each of the other seven falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight trusts, occupied level-2 and level-3 critical-care bed-days over the last
  four quarters. *Device:* the critical-care dataset splits a period of care into one record per level, and the data manual records the
  day of a step-down in both records. Summing record days double-counts every change day and overstates bed-days at the two trusts with
  the most step-downs. The episode file and the chains never use this dataset.
* **Ask B (device-carried).** For each trust, ambulance arrivals whose handover took longer than 60 minutes over the last twelve months, and
  the median handover time. *Device:* the handover protocol makes the cohort-nurse acceptance time the handover time wherever a trust runs
  a cohorting area, while the crew's terminal button is pressed later. Reading the button time overstates delays at the two cohorting
  trusts.
* **Ask C (validity).** For each of the four rung constructions, the retry-log outcomes it reproduces out of 34 and its error on the 237
  confirmed deaths.
* **Decoupling.** Clearing the chain construction and the linkage changes no figure in asks A or B.

## 11. Rubric arithmetic

8 trusts × 2 levels (ask A) + 8 trusts × 2 figures (ask B) + 4 constructions × 2 (ask C) + the committed trust, its chain-origin excess and
the margin over the runner-up + 5 named chart parts + 3 files ≈ 51 criteria.

## 12. World-building constraints

* Each of the five flags is high in at least one trust for a documented reason: specialist elective case mix (A), a hospice unit (B), the
  weekend stroke diversion (C), a frailty virtual ward that readmits by design (D) and a coastal retirement catchment (F).
* E's late transfers run steadily and go to A, C, D and G; no receiver gains more than 13 attributed deaths a year from them. E's chain
  excess is 38 deaths in the latest four quarters; G's is 17 and every other trust's 9 or fewer. G sends the most chains (66 deaths to
  E's 52) at expected risk.
* Inter-trust gaps are under 4 hours or at least 2 days. The regional extract carries admission method but no admission source or
  discharge destination.
* Rung leaders are A, B, C, E with margins of 1.27×, 1.26× and 1.27×; E is 5th, 4th and 3rd across rungs 0–2.
* The retry log holds 34 reviews (13 confirmed, 237 confirmed deaths) and 13 failed retries; Kellow Bridge and Sandmere are identical on
  every trust-level field.
* Critical-care step-downs and ambulance cohorting never touch the episode file or the chains.
