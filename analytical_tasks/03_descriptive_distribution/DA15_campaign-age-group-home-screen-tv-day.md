# DA15 — Which age group a streaming campaign targets, when its trailer plays once per TV per day and the heaviest viewers share their TV

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · media consumption measurement on a connected-TV platform |
| Mirrors | Choosing who a frequency-capped placement reaches from how much they use the screen, when the cap is per device and the heaviest users share theirs (connected-TV home-screen units at Roku-, Google TV- and Fire TV-style platforms, lock-screen and widget placements capped per device, console dashboard promotions on shared Xbox and PlayStation consoles) |
| Decision shape | Which of N gets one scarce thing: the spring brand campaign, for one of five age groups |
| Committed call | The age group, and its expected daily home-screen impressions per 100 persons in platform households |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · E07, two grains of viewing (minutes, and the TV-day whose first home-screen session the campaign buys), with E19 (the OS account signed in when each session starts, which credits Family-profile viewing) below it, pinned by Pattern B on the ledger's home-screen pilots |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #7 uses the ready-made measure · #10 notes a binding limit as a risk · #17 guesses an attribution the data can settle · #12 stops at the first control that passes |
| Calibration form | Settled-transaction ledger: 41 settled campaigns on the platform, each with guaranteed and partner-verified impressions by age group |
| Driving force | The campaign is a home-screen trailer, and the platform shows a home-screen campaign once per TV per day, on the first session of the day. Every measure of how much each age group watches, attribution fixed included, says 15- to 24-year-olds. But they watch on the family TV in the evening, after a parent or a younger child has switched it on that morning and used the day's impression. People aged 25 to 34 are the group most likely to have a TV to themselves, alone or in a flat-share with a set in each room, so they receive their TV's impression nearly every day. Counted by TV-day, they lead, and they were fourth on every minutes measure. |

## 1. Situation

A company that makes a TV operating system and runs a streaming service on it has one brand campaign for its spring slate. The brief
sends it to the age group the campaign would reach most often per person in platform households. The campaign is a home-screen trailer,
and the ad-operations guide caps home-screen campaigns at one impression per TV per day. The pack holds the streaming session log
(device, profile, start and end), the profile table (birth year where users set one), accounts with the holder's age, the household
rosters, the TV operating system's sign-in log and home-screen event log, the 41-campaign settled ledger, the measurement standard and
the ad-operations guide. The brief is due on 2 February.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: sessions, profiles, rosters, the sign-in and home-screen logs and the ledger. Crediting a
  Family-profile session to the account holder is the service's documented fallback, and the age group that watches most really is
  15–24. Nobody's reading of their own numbers is overturned. The difficulty is what the campaign buys.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of research's view, the brand director's view and the audience council's basis. Every viewing
  measure still ranks 15–24 or an older group first, and minutes are still the natural proxy for exposure.
* **Instrument repair.** Clean-data test. The suspect file is the session log, whose Family profile records the viewer as the
  household. Repair it at every depth (give each session its viewer's birth year, or replace the log with one that records who
  watched). Rung 0 still names 65+ and rung 1 35–49, because they credit the holder by construction; rung 2 becomes a direct read and
  names 15–24. The answer is unchanged, and the decisive construction, crediting each TV-day's one impression to whoever opened that TV
  first, is still needed. No other file is suspect: the home-screen log and the rosters are complete.
* **Lens swap.** The two reads count different things: all 1,260 million daily viewing minutes, against the 9.4 million TV-days a day
  whose first home-screen session receives the campaign.

## 3. The driving force

A strong solver reads the brief as a question about who watches. It moves from minutes per viewer to minutes per person on the rosters,
credits personal profiles to their birth years, and resolves the shared Family profile through the operating system's sign-in log: a
session belongs to the OS account signed in when it starts. The ledger's in-stream campaigns verify that attribution, and it names 15- to
24-year-olds, who watch 84 minutes a day. But the campaign is not an in-stream ad. It is a home-screen trailer, capped at one impression
per TV per day, and the impression goes to the first session that opens the home screen. In a family the TV is switched on in the
morning by a parent for the news or a child for cartoons, and the teenager's evening binge comes long after the day's impression is
spent. A 28-year-old living alone, or with a TV in their own room of a flat-share, opens their own TV almost every day. Read by TV-day,
25–34 receives 49 impressions per 100 persons a day and 15–24 seven.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Average daily minutes per viewer, each session credited to the account holder's age | A, 65 and over (212 min, 1.26× 50–64) | The streaming service's standard engagement metric | The brief scores reach per person, and the rosters count everyone, viewers or not |
| 1 | Minutes per person (roster denominators), credited to the account holder | B, 35–49 (78 min, 1.22× 50–64) | The brief's population and the service's documented attribution | The ledger's age cells: holder credit reproduces 112 of 190 in-stream age cells and 2 of 15 home-screen cells |
| 2 | Minutes per person, personal profiles by birth year and Family sessions by the OS account signed in at session start (E19) | C, 15–24 (84 min, 1.40× 25–34) | Reproduces all 190 in-stream age cells, the ledger's salient check | The ledger's three home-screen pilots: crediting impressions in proportion to minutes reproduces 3 of their 15 age cells |
| 3 | **Decisive:** each TV-day's one impression credited to the person signed in at that TV's first home-screen session, per person on the rosters (E07) | **D, 25–34 (0.49 a day, 1.29× 65+)** (4th of 5 on rung 0) | — | — |

* **Position table.** 25–34 ranks 4th on rungs 0 and 1 and 2nd on rung 2 (1.40× behind 15–24), and leads only rung 3. Each rung's leader
  beats its runner-up by at least 1.22×.
* **Discriminator dominance.** 15–24 carries 1.40× (84 against 60 minutes) into rung 3. On the decisive axis, impressions received per
  minute watched, 25–34 converts 0.0082 and 15–24 0.00083, an edge of 9.8×. That is 5.8 times the required 1.2 × 1.40 = 1.68. The final
  margin over 15–24 is 0.49 against 0.07 a day.
* **Partial correction priced (L3).** Every half-applied construction names a wrong group. Sharing each TV-day's impression among its
  sessions in proportion to minutes reproduces the minutes ranking and names 15–24 (1.40×). Taking the first session but crediting it to
  the account holder names 35–49 (0.61 against 0.49, 1.24×). Capping per household instead of per TV takes the flat-sharers' own sets
  away and names 65+ (0.38 against 50–64's 0.27, 1.41×).
* **Grid.** Denominator (viewers or persons) × attribution (holder, birth year with holder fallback, OS account) × exposure (minutes or
  first session per TV-day) gives 12 cells. They name 65+, 35–49, 50–64 or 15–24, and only persons, OS accounts and TV-days name 25–34.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The brief says "reach most often per person". The ad-operations guide says home-screen campaigns are capped at one
   impression per TV per day. No document says who receives the capped impression, or that the cap reverses the minutes ranking.
2. **Reproduction, and why it is a construction.** First-session credit with the OS viewer reproduces all 15 age cells of the three
   home-screen pilots. Minutes-proportional credit reproduces 3, holder first-session credit 5 and a per-household cap 4, and every rival
   overstates 15–24 and the older groups together, so none reconciles on the pilots' totals by age. The construction ranks each TV's
   home-screen events within the day and joins the first to the sign-in interval in force. No field or parameter reaches it.
3. **No arithmetic symptom.** Every construction partitions the same minutes or the same TV-days, rosters reconcile, and the in-stream
   cells verify under rung 2 exactly.
4. **Not a row predicate.** A session's role is set by its rank among the TV's home-screen events that day, a group-and-rank on device
   and date, and its viewer by another system's interval.
5. **The enumeration is arithmetic.** 9.4 million TV-days a day are ranked and credited; 6.7 million go to persons aged 15 and over.
6. **No cutover date.** The cap and households' morning habits are the same all year, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, minutes are still the obvious measure of exposure.

## 6. The calibration corpus

* **Form.** The settled ledger: 41 campaigns, each with guaranteed impressions by age group and the measurement partner's verified
  impressions by age group from its people-meter panel. 38 were in-stream campaigns on personal devices, and three were home-screen pilots
  on TVs.
* **What it certifies (E16 and Pattern B).** Every construction reproduces the 41 campaign totals. The 190 in-stream age cells pass only
  person-level attribution, and the 15 home-screen cells pass only first-session credit with the OS viewer.
* **Twin pair.** Households H-2207 and H-5513 are identical on every streaming column: a 47-year-old holder, a roster of 47, 45 and 19, one
  living-room TV and 312 Family minutes a day. In H-2207 the 19-year-old opens the TV first on most days, for morning games; in H-5513 the
  45-year-old does, for the news. Their 19-year-olds receive 0.62 and 0.31 impressions a day (2.0×). Every minutes rule credits both alike.
* **Resemblance points at the decoy.** By hour of day, the platform's TV viewing most resembles the partner's published profile for 15- to
  24-year-olds in the evening peak, where the in-stream campaigns delivered most.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The campaign brief: "The campaign goes to the age group it would reach most often per person in platform households."
  The ad-operations guide: "Home-screen campaigns are capped at one impression per TV per day." The measurement standard defines
  households by the roster and states the Family-profile fallback to the account holder.
* **Empirical pins.** Person-level attribution and first-session credit, from the ledger.
* **Voices.** The head of research: "Whoever watches most sees most; minutes have always been our proxy for reach." The brand director:
  "The young binge our shows. That's who we should be talking to."
* **Licensed wrong basis.** The standard records that the industry audience council credits connected-TV viewing to the account holder's
  age and will compare the campaign's targeting with that basis.

## 8. Determinism by construction

* **First session.** A TV-day runs midnight to midnight in the household's time zone, and its first session is the first home-screen
  event after the TV wakes. No TV wakes within a minute of midnight, so neither the day boundary nor a tie can move an impression.
* **Interval join.** Every home-screen event falls inside exactly one sign-in interval on its TV.
* **Rosters and days.** Ages are taken on 1 January 2027, and the 92 days of Q4 2026 are averaged with every roster member in the
  denominator for every day.
* **Margins.** Every rung's leader is at least 1.22× ahead of its runner-up, so no rounding convention reorders the groups.

## 9. Prompt sketch and deliverables

> We have one brand campaign for the spring slate and it goes to a single age group. Our head of research says whoever watches most sees
> most. Tell me which age group the campaign should target and how often it would reach them, in impressions per 100 persons a day, in a
> sentence for the brief, and send `audience_case.csv` with the age-group table, `reach_by_age.png`, and a short `targeting_memo.pdf`.

* `audience_case.csv` — five age groups × four rung constructions: minutes or impressions per person, the ledger's reproduction counts,
  and the churn and launch figures (asks A and B).
* `reach_by_age.png` — minutes per person and impressions per person by age group side by side, the share of each group's TV-days opened
  by someone else shaded, the chosen group marked, and the H-2207 and H-5513 twins annotated.
* `targeting_memo.pdf` — the committed group and its impressions, and why each other group falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Monthly churn of each of the four subscription plans from July to December 2026. *Device:* a plan
  change is logged as a cancellation of the old plan and a new subscription carrying a plan-change link, as the billing guide documents.
  Counting changes as churn overstates 17 of the 24 rates by 0.4 to 1.9 points.
* **Ask B (device-carried).** App launch-failure rate on each of the eight TV OS versions in Q4. *Device:* the OS retries a failed launch
  once within five seconds under the same launch token, as the crash-reporting guide states. Counting attempts doubles the failure rate on
  the three versions with the retry enabled.
* **Ask C (validity).** Minutes or impressions per person for each age group under each of the four rung constructions, and each
  construction's reproduction counts on the ledger's 190 in-stream and 15 home-screen age cells.
* **Decoupling.** Billing records and crash reports share no row with the session, sign-in or home-screen logs. Clearing the first-session
  credit changes no figure in asks A or B.

## 11. Rubric arithmetic

4 plans × 6 months (ask A) + 8 OS versions (ask B) + 5 groups × 4 constructions and 8 reproduction counts (ask C) + the committed group, its
impressions and its margin + 4 named chart parts + 3 files ≈ 70 criteria.

## 12. World-building constraints

* Persons in platform households (millions): 3.1 / 4.0 / 6.2 / 5.4 / 3.6 for 15–24 / 25–34 / 35–49 / 50–64 / 65+.
* Minutes per person: rung 1 12 / 49 / 78 / 64 / 55; rung 2 84 / 60 / 45 / 52 / 55. Per viewer at rung 0: 96 / 118 / 141 / 168 / 212.
* Impressions per person per day at rung 3: 0.07 / 0.49 / 0.24 / 0.31 / 0.38. Holder first-session credit: 0.02 / 0.49 / 0.61 / 0.47 /
  0.38. Per-household cap: 0.06 / 0.21 / 0.19 / 0.27 / 0.38.
* 9.4 million TV-days a day; 6.7 million first sessions belong to persons aged 15 and over, the rest to children.
* The three home-screen pilots reproduce only under first-session credit with the OS viewer; the 38 in-stream campaigns under person
  attribution.
* H-2207 and H-5513 are identical on every streaming column.
* Billing and crash data touch no session or home-screen event.
