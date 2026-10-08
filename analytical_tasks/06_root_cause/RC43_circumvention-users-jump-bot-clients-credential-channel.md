# RC43 — How many people the election really sent to the circumvention service, when bots fill the dashboard and the real arrivals use a channel it never counts

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Demographic & Social Science · internet censorship and circumvention measurement |
| Mirrors | Active-user metrics at platforms where automated clients inflate one channel while real users arrive through another the dashboard does not count (Telegram and Signal proxy channels during app-store removals, Meta sign-ups in blocked markets, Google products when users move from a blocked app to the web) |
| Decision shape | One figure committed at a date (a component): the daily users the election added in the country, published in the annual report |
| Committed call | The election added 62,000 daily users in the country, 24,000 through the app and 38,000 through credentials from the messaging bot, beside 126,000 automated clients that are not users |
| Gap · Pattern | Gap 2 (population) at the decisive rung · S1 through an implicit join (measured #18): people reached through bot-issued credentials, linked credential → account in the issuance log and absent from the dashboard's client IDs, with the latent marker of measured #17 at rung 1 (automated clients by their missing heartbeat) |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #18 joins only on the visible key · #17 guesses an attribution the data can settle · #11 beats the headline trap, misses the quiet one |
| Calibration form | Retry or revision log: the NGO's revision log for its past annual reports, nine published user figures, each revised up to twice as late proxy logs arrived |
| Driving force | The dashboard's fivefold jump is mostly a botnet: 126,000 clients that never send the app's heartbeat. Take them out with the failed handshakes, and the app shows 24,000 new people, which reads as a modest real rise. But the censor blocked the app store two days after the election, and from then on new users in the country came through the NGO's messaging bot, which issues each person a proxy credential. Their connections sit in the credential endpoint's log under the credential, and only the bot's issuance log ties each credential to the account that asked for it. Joined, 38,000 more people connected each day, and the election added 62,000 users. |

## 1. Situation

A digital-rights NGO runs a free circumvention service: an app, and a messaging bot that hands out proxy credentials for any standard
client. In one country the service dashboard's daily active clients rose from 40,000 to 200,000 within a week of a contested election. The
NGO's annual report must state how many people the election sent to the service, and its donors will read that figure. The draft says
160,000, the whole jump. A reviewer warns that past jumps like this were botnets using the service for command-and-control.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the dashboard's client counts, the telemetry heartbeats, the app-endpoint and
  credential-endpoint logs, the bot's issuance log and the revision log. The reviewer is right that most of the jump is automated, and the
  draft is right that people came. No one's reading of their own figures is overturned. The task quantifies the people.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the draft, the reviewer and every voice. The dashboard still counts 160,000 new clients, and removing the bots
  still leaves 24,000 app users.
* **Instrument repair.** Suspect: the dashboard's daily active count includes clients whose only contact was a failed handshake, a broader
  meaning than a connection. Repair: count connections only, and give every client a perfect automated-or-human flag. Rung 0 then returns
  +150,000 (or +24,000 with the flag), rung 1 +24,000 and rung 2 +24,000; none reaches +62,000. The endpoint logs and the issuance log are
  complete. A person reached through a bot credential appears only as a credential in one log and an account in another, and joining them
  is a construction no row records, so it is still needed.
* **Lens swap.** The naive population is the app's client IDs. The answer's is people who connected by either channel, most of the new ones
  through a channel the dashboard never reads.

## 3. The driving force

A strong solver does not publish the dashboard's jump. It reads the reviewer's warning, checks the telemetry spec, and finds that 126,000 of
the new clients never send the app's foreground heartbeat and connect only on the hour and the half hour, which no person does. The
revision log shows the same signature in the NGO's 2021 correction for another country. It also drops clients whose only contact was a
failed handshake. That leaves 24,000 new people on the app, a real but modest rise, and the reviewer looks mostly right. But the app store
was blocked two days after the election. From then on, a person who could not install the app asked the messaging bot for a credential and
put it into any standard client. Those connections reach the credential endpoint, which logs the credential, not a client ID, so the
dashboard never counts them. The issuance log ties every credential to one phone-verified account. Joined, 38,000 more people connected on
an average day after the election than before it.

## 4. The ladder

| Rung | Construction | Lands on (daily users added, thousands) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The dashboard's daily active clients, 28 days after against 28 days before | +160 (+158%) | The NGO's own dashboard and the draft's figure | The telemetry spec: every app session sends a foreground heartbeat, and 126,000 of the new clients never sent one |
| 1 | Latent marker: clients with no heartbeat that connect only on the hour and half hour removed as automated | +34 (−45%) | The reviewer's concern answered with a signal the 2021 correction confirms | The handshake status field: 10,000 of the remaining new clients only ever failed a handshake |
| 2 | Hygiene of activity: clients with no completed connection removed | +24 (−61%) | Every counted client is a person who connected, and the dashboard reconciles | The messaging bot's operations guide: since the store block, new users in the country take a credential from the bot and connect through the credential endpoint |
| 3 | **Decisive:** people reached through bot credentials added, each credential's connections joined to the account it was issued to | **+62** | — | — |

* **Figure shape.** The corrections walk the figure down from +160 to +24, and the decisive move reverses them to +62. Offsets from the
  answer are +98, −28 and −38.
* **Partial correction priced (L3).** Rung 2 sits 38 from the answer. A solver who counts credentials with traffic instead of the accounts
  behind them double-counts every re-issued credential and lands at +108. One who counts accounts that asked the bot for a credential, whether
  or not it ever connected, lands at +119. Both are further away than rung 2.
* **Grid.** Bots (in, out) × failed handshakes (in, out) × credential channel (none, credentials, requesting accounts, connecting accounts)
  gives 16 cells. The nearest wrong cell keeps the failed handshakes in and lands at +72 (16%). Every other cell is at least 45% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The bot's guide describes how credentials are issued. No document says the dashboard omits the credential endpoint,
   or that credential users belong in the report's figure.
2. **Corpus blind for a computable reason.** *In every figure in the revision log the bot had issued no credential in that country, because
   the bot serves only countries where the app store is blocked, and none of them was blocked in those years.* The log certifies rung 2's
   construction 9 of 9.
3. **No arithmetic symptom.** The dashboard reconciles exactly to the app endpoint's log, and the credential endpoint reconciles to the
   issuance log.
4. **Not a row predicate.** A credential user is a person built by joining each credential's connections to the account that received it,
   then counting distinct accounts per day.
5. **The enumeration is arithmetic.** No field marks a connection as a new user. People are counted from the join.
6. **No cutover date.** The bot channel grew through the window as people discovered it. The figure is a difference of four-week means, not
   a step.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The NGO's revision log: nine published user figures from three countries over three years, each with its data vintage and up to
  two revisions as partner servers' late logs arrived.
* **What it certifies.** Rung 2's construction, bots removed by the heartbeat marker and failed handshakes dropped, reproduces every
  revision from its vintage exactly. The 2021 correction is the settled case for the marker: it moved a published 90,000 to 21,000, and only
  the heartbeat signature reproduces it.
* **What it is blind to.** The credential channel (property 2).
* **Twin pair.** Talvar and Ostrel provinces are identical on new dashboard clients, bot clients, failed handshakes and new app users
  (2,000 each). The credential join adds 7,000 people in Talvar and 2,500 in Ostrel, so they gained 9,000 and 4,500 users (2.0×), because
  Talvar's mobile networks also blocked the site the app is sideloaded from.
* **Resemblance points at the decoy.** The jump most resembles the 2021 jump in the revision log, which the NGO first published as demand and
  then corrected to a botnet.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The report's style guide: "A user is a person who connected to the service on the day; automated clients are not users."
  The telemetry spec: "Every app session sends a foreground heartbeat every five minutes." The bot's guide: "The bot issues one credential
  at a time to a phone-verified account, and only in countries where the app store is blocked."
* **Empirical pins.** The heartbeat marker comes from the 2021 correction. The 28-day windows come from the revision log's practice.
* **Voices.** Draft author: "People in their hundreds of thousands turned to us." Reviewer: "We have seen this before; it is a botnet."
  Security engineer: "The bots never bother with the app's heartbeat." Bot channel manager: "The bot is a small side channel; it has never
  mattered for the numbers."
* **Licensed wrong basis.** The style guide records that the NGO's donors read user figures from the service dashboard and will see this
  report on that basis.

## 8. Determinism by construction

* **Windows.** The before window is the 28 days ending the day before the election, and the after window the 28 days starting the day after
  the store block. Days are local calendar days.
* **Marker.** Every automated client lacked the heartbeat on every day it appeared, and no human client went a whole day without one, so the
  marker is exact.
* **Join.** Every credential was issued to exactly one account and never reassigned, and every account is one phone number, so distinct
  accounts per day are unambiguous. Re-issued credentials stay with their account.
* **Activity.** The handshake status field is filled on every attempt, and a client counts as connected if any attempt completed.
* **Maturity.** Partner servers' logs arrive within 21 days, and the extract is 45 days after the after window closed.

## 9. Prompt sketch and deliverables

> Our draft annual report says 160,000 people in the country turned to the service after the election, and a reviewer thinks it was a
> botnet. I need the number of daily users the election actually added there, in thousands, to the nearest thousand, in a sentence the report
> can carry. Send `user_figure.xlsx`, a chart `user_jump_bridge.png`, and a one-page `report_wording.pdf`.

* `user_figure.xlsx` — the figure on every construction, the bandwidth sheet (ask A), the crash sheet (ask B) and the revision-log back-test
  (ask C).
* `user_jump_bridge.png` — a bridge from the dashboard's +160,000 to the committed figure with bots out, failed handshakes out and credential
  users in, an inset of daily people by channel through the election, and a title stating the figure.
* `report_wording.pdf` — the figure, its two channels and the automated clients set beside it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month of the report year, terabytes served to the country. *Device:* the endpoint logs
  record bytes in both directions per session, and the metrics guide counts only bytes leaving the service's servers. Summing both directions
  overstates bandwidth by about 15%, and by far more in the bot months, because the bots upload heavily. Bytes never enter a user count.
* **Ask B (device-carried).** For each of the six app versions in use and each quarter, crashes per thousand sessions. *Device:* the
  telemetry spec deduplicates crash reports by device, signature and day, and two versions loop on the same crash. Counting raw reports
  overstates their rates about threefold.
* **Ask C (validity).** For each of the nine figures in the revision log, the final revised figure beside what your construction gives on that
  figure's vintage.
* **Decoupling.** Clearing the credential join changes no figure in asks A or B. Ask C contains no credential user, by property 2.

## 11. Rubric arithmetic

12 months (ask A) + 6 versions × 4 quarters (ask B) + 9 figures (ask C) + the committed figure, its app and credential parts, the automated
clients and the failed handshakes + 5 named chart parts + 3 files ≈ 58 criteria.

## 12. World-building constraints

* Daily averages, after against before: dashboard clients +160,000, of which automated +126,000, failed-handshake-only +10,000 and new app
  users +24,000. Credential-channel people +38,000, holding 84,000 credentials, with 95,000 accounts having asked for one.
* The 2021 correction moved a published 90,000 to 21,000 on the heartbeat marker.
* Talvar and Ostrel are identical on every dashboard and telemetry column, with credential people of 7,000 and 2,500.
* Every revision-log figure has zero credential users. Every grid cell other than the answer sits at least 16% from 62,000.
* Byte counts and crash reports never touch client IDs, credentials or accounts.
