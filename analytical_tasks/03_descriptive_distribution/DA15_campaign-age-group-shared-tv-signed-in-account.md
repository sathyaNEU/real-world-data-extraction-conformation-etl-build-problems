# DA15 — Which age group a streaming campaign targets, when the family TV's viewing is credited to whoever holds the account

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · media consumption measurement on a connected-TV platform |
| Mirrors | Crediting viewing on shared screens to the person actually watching (connected-TV measurement at YouTube, Netflix and Roku-style platforms, console play time on shared Xbox and PlayStation devices, family tablets in Apple and Amazon household accounts) |
| Decision shape | Which of N gets one scarce thing: the spring brand campaign, for one of five age groups |
| Committed call | The age group, and its average daily TV viewing minutes per person in platform households |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E19, a latent attribution marker (the operating-system account signed into the TV when a session starts), with E16 (the settled ledger's age cells, finer than its totals) below it, pinned by Pattern B on the ledger's TV pilots |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #17 guesses an attribution the data can settle · #12 stops at the first control that passes · #1 reports a failed back-test, ships anyway · #15 follows the requester's hunch over the rule |
| Calibration form | Settled-transaction ledger: 41 settled ad campaigns on the platform's ad tier, each with guaranteed and partner-verified impressions by age group |
| Driving force | Half of all TV viewing runs on households' shared "Family" profiles, which carry no birth year, so every credit rule falls back to the account holder: a parent aged 35 to 64. The platform's own TV operating system logs which household member's OS account was signed in, switch by switch, and every session starts inside exactly one such interval. Read through that log, evening Family-profile viewing belongs to the household's 15- to 24-year-olds. Per person they watch more TV than any other group, and they were fifth under every other rule. |

## 1. Situation

A company that makes a TV operating system and runs a streaming service on it has one brand campaign for its spring slate. The brief
sends it to the age group with the most average daily TV viewing minutes per person in platform households. The pack holds the streaming
service's TV session log (device, streaming profile, start and end), the profile table (birth year where users set one), accounts with the
holder's age, the household rosters with every member's age, the TV operating system's account-switch log, the 41-campaign settled ad
ledger and the measurement standard. The brief is due on 2 February.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: sessions, profiles, account ages, rosters, the switch log and the ledger's verified impressions.
  Crediting a Family-profile session to the account holder is the streaming service's documented fallback, and nobody's reading of their
  own numbers is overturned. The difficulty is who was watching.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of research's view and the industry council's licensed basis. Family-profile sessions still have no
  birth year, and the account holder is still the only age on the session's own records.
* **Instrument repair.** Perfect the streaming logs and the Family profile is still one profile shared by a household, because that is
  how households set up their TVs. The person is recorded by a different system, the OS log, which the session never references.
* **Lens swap.** The two reads credit different people: 410 million Family-profile minutes a day go to account holders aged 35 to 64,
  or to the household members signed into the TV, 140 million of them aged 15 to 24.

## 3. The driving force

A strong solver moves from minutes per viewer to minutes per person on the household rosters. It credits sessions on personal profiles to
the profile's birth year, and back-tests that against the settled ledger, whose verified age cells match on all 38 personal-device
campaigns. That names the 50-to-64 group, which fits the belief that TV is where older viewers live. But half the TV minutes run on
Family profiles, which have no birth year, and every rule so far falls back to the account holder. The TV operating system records
which household member's OS account was signed in, and it always has exactly one, from sign-in to switch. A session inherits the account
signed in when it starts, through an interval join on device and time that nothing in the streaming data points to. In the evenings that
account belongs to the household's teenager or young adult. The ledger's three TV pilot campaigns verify only under that attribution.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Average daily minutes per viewer, each session credited to the account holder's age | A, 65 and over (212 min, 1.26× 50–64) | The streaming service's standard engagement metric | The brief scores minutes per person, and the household rosters count everyone, viewers or not |
| 1 | Minutes per person (roster denominators), credited to the account holder | B, 35–49 (78 min, 1.22× 50–64) | The brief's population, the service's documented attribution | The ledger's age cells: account-holder credit reproduces 112 of 190 personal-device cells |
| 2 | Personal profiles credited to their birth year, Family profiles to the account holder (E16) | C, 50–64 (72 min, 1.26× 35–49) | Reproduces all 41 campaign totals and all 190 personal-device age cells | The ledger's TV pilots: profile credit reproduces 4 of their 15 age cells |
| 3 | **Decisive:** Family-profile sessions credited to the OS account signed into the TV at session start (E19) | **D, 15–24 (78 min, 1.32× 25–34)** (5th of 5 on rung 0) | — | — |

* **Position table.** 15–24 ranks 5th on rungs 0, 1 and 2 and leads only rung 3. Each rung's leader beats its runner-up by at least 1.22×.
* **Discriminator dominance.** 50–64 carries 2.18× (72 against 33 minutes) into rung 3. On the decisive axis, minutes kept once the TV log
  credits the viewer, 15–24 rises 2.36-fold and 50–64 keeps 0.78, an edge of 3.03×. That clears 1.2 × 2.18 = 2.62. The final margin over
  50–64 is 78 against 56 (1.39×).
* **Partial correction priced (L3).** A solver who sees that Family profiles are shared and splits their minutes equally among the
  household's members (the guessed attribution) names 50–64 (61 against 58): the heuristic lands on the decoy.
* **Grid.** Denominator (viewers or persons) × personal-profile credit (holder or birth year) × Family credit (holder, equal split or OS
  account) gives 12 cells. They name 65+, 35–49 or 50–64, and only persons, birth years and the OS account name 15–24.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The measurement standard says Family-profile sessions "fall back to the account holder". The OS log is documented
   as a device-security record. No document links a session to it.
2. **Reproduction, and why it is a construction.** OS-account credit reproduces all 15 age cells of the three TV pilot campaigns. Profile
   credit reproduces 4, holder credit 2, and an equal split 6. The rivals' misses run one way (too old), so none nets out on the pilots'
   totals by age. The rule is an interval join of each session's start to the device's sign-in intervals, with no field or parameter to
   scan.
3. **No arithmetic symptom.** Every attribution is a complete partition of the same 1,260 million daily minutes. Campaign totals, roster
   counts and session counts tie under every rung.
4. **Not a row predicate.** The viewer is the OS account whose interval on that device contains the session's start, a property of
   another system's record reached through device and time.
5. **The enumeration is arithmetic.** 410 million Family minutes a day are credited by the join, not by any field.
6. **No cutover date.** Households sign into their TVs the same way all year, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the Family profile still falls back to the holder.

## 6. The calibration corpus

* **Form.** The settled ledger of the platform's ad tier: 41 campaigns, each with guaranteed impressions by age group and the measurement
  partner's verified impressions by age group (from its people-meter panel), with make-goods settled. 38 ran on personal-device inventory
  and three were TV pilots.
* **What it certifies (E16).** Every attribution reproduces the 41 campaign totals, the salient control. The 190 personal-device age cells
  pass only birth-year credit, and the 15 TV-pilot age cells pass only OS-account credit.
* **Twin pair.** Households H-2207 and H-5513 are identical on every streaming-visible column: a 47-year-old holder, a roster of 47, 45 and
  19, the same devices and profiles, and 312 Family minutes a day. Their 19-year-olds are credited with 126 and 63 minutes a day (2.0×)
  by the OS log. Every other rule credits both with none.
* **Resemblance points at the decoy.** By hour of day, the platform's TV viewing most resembles the measurement partner's published
  profile for viewers aged 50 to 64.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The campaign brief: "The campaign targets the age group with the most average daily TV viewing minutes per person in
  platform households." The measurement standard defines a household by the roster and a person by its member record. The standard
  states the Family-profile fallback to the account holder.
* **Empirical pins.** Birth-year credit for personal profiles and OS-account credit for Family sessions, from the ledger.
* **Voices.** The head of research: "We credit viewing to account holders; it's always been close enough to sell on." The brand director:
  "TV is where our older viewers live. The young are on their phones."
* **Licensed wrong basis.** The standard records that the industry audience council credits connected-TV viewing to the account holder's
  age and will compare the campaign's targeting with that basis.

## 8. Determinism by construction

* **Interval join.** Every session starts inside exactly one sign-in interval on its device. No switch falls within a session's first
  minute, so start-time and majority-time credit agree.
* **Rosters.** Ages are taken on 1 January 2027, and no member crosses an age band during the measured quarter.
* **Days.** Minutes are averaged over the 92 days of Q4 2026 with every roster member in the denominator for every day.
* **Margins.** No rung's leader is within 15% of its runner-up, so rounding conventions cannot reorder groups.

## 9. Prompt sketch and deliverables

> We have one brand campaign for the spring slate and it goes to a single age group. Our head of research is comfortable crediting
> viewing to account holders, as we always have. Tell me which age group the campaign should target and its average daily TV viewing
> minutes per person, in a sentence for the brief, and send `audience_case.csv` with the age-group table, `minutes_by_age.png`, and a
> short `attribution_memo.pdf`.

* `audience_case.csv` — five age groups × four rung constructions: minutes per person, the ledger's reproduction counts, and the churn and
  launch figures (asks A and B).
* `minutes_by_age.png` — minutes per person by age group under holder, birth-year and OS-account credit as grouped bars, the Family-profile
  share hatched, the chosen group marked, and the H-2207 and H-5513 twins annotated.
* `attribution_memo.pdf` — the committed group and minutes, and why each other group falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Monthly churn of each of the four subscription plans from July to December 2026. *Device:* a plan
  change is logged as a cancellation of the old plan and a new subscription carrying a plan-change link, as the billing guide documents.
  Counting changes as churn overstates 17 of the 24 rates by 0.4 to 1.9 points.
* **Ask B (device-carried).** App launch-failure rate on each of the eight TV OS versions in Q4. *Device:* the OS retries a failed launch
  once within five seconds under the same launch token, as the crash-reporting guide states. Counting attempts doubles the failure rate on
  the three versions with the retry enabled.
* **Ask C (validity).** Minutes per person for each age group under each of the four rung constructions, and each construction's
  reproduction counts on the ledger's 190 personal-device and 15 TV-pilot age cells.
* **Decoupling.** Billing records and crash reports share no row with the session log or the OS sign-in log. Clearing the OS-account
  credit changes no figure in asks A or B.

## 11. Rubric arithmetic

4 plans × 6 months (ask A) + 8 OS versions (ask B) + 5 groups × 4 constructions and 8 reproduction counts (ask C) + the committed group, its
minutes and its margin + 4 named chart parts + 3 files ≈ 70 criteria.

## 12. World-building constraints

* Persons in platform households (millions): 3.1 / 4.0 / 6.2 / 5.4 / 3.6 for 15–24 / 25–34 / 35–49 / 50–64 / 65+. Daily minutes total 1,260
  million under every attribution.
* Minutes per person by rung: rung 1: 12 / 49 / 78 / 64 / 55; rung 2: 33 / 54 / 57 / 72 / 55; rung 3: 78 / 59 / 45 / 56 / 55. Per viewer at
  rung 0: 96 / 118 / 141 / 168 / 212. The equal split gives 55 / 58 / 53 / 61 / 55.
* Family profiles carry 410 million minutes a day, and 140 million of them belong to 15- to 24-year-olds by the OS log.
* The 38 personal-device campaigns reproduce under birth-year credit and the 3 TV pilots only under OS-account credit.
* H-2207 and H-5513 are identical on every streaming column.
* Billing and crash data touch no session.
