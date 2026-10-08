# RC21 — Which cause of the rise in active job-seekers gets the professional network's product bet, when the biggest cause is not the one a bet moves most

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Product Analytics · two-sided marketplace supply and demand |
| Mirrors | Product-bet sizing at job and professional platforms (LinkedIn, Indeed, Upwork), where the largest cause of a rise in active seekers is not the cause whose fix moves the most members, and the product change log already holds past launches of every kind of bet, readable as natural experiments |
| Decision shape | Which of N root causes gets the fix: the year's one product bet on the job-seeker side |
| Committed call | The cause the bet targets, and the members its fix would take out of active job-seeking over the coming year, in thousands |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E26 (change-log natural experiments: ten past launches, each read against members in comparable markets, measure what each kind of bet moves and whom it reaches), with E33 (the population a flag suggests: open-to-work flags against the dated active-seeker rule) at rung 1 and E19 (a latent attribution marker: dormant accounts reactivated) at rung 2 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #25 assumes an effect the log could measure · #5 takes the population a flag or filter suggests · #17 guesses an attribution the data can settle |
| Calibration form | Change-log natural experiments: ten past launches in the product change log (four outplacement partnerships, two returnship partnerships, two posting-incentive city pilots, an early-career tools launch and a career-move tools launch), each with members' timelines before and after, in its own market and in comparable ones |
| Driving force | Once the behavioural trace recovers why members are looking, returners are the biggest cause of the rise. The template funds the cause whose fix would take the most members out of active seeking next year, and fixing a cause is not removing it. The change log's ten launches, each read against members in comparable markets, show what each kind of bet moves: posting incentives lift every seeker's exit rate 6% in the markets they run, applicants or not; outplacement lifts only the laid-off members partners can enrol; returnships barely move returners, whose constraint is not search. Applied to next year's stock, posting incentives move 340,000 members, four times any other bet. |

## 1. Situation

A professional network's active job-seekers rose by 1.20 million members this year, from 4.8 million to 6.0 million. The recruiting-products team says
a layoff wave is under way; the returnship team says career-break members are flooding back; the chief product officer thinks graduates are. The
company will place one product bet on the job-seeker side: outplacement partnerships (A), employer posting incentives to lift hiring (B), early-career
tools (C), a returnship programme (D) or career-move tools for voluntary changers (E). The planning template says how the bet is chosen. The product
change log records every past launch of each kind of bet.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the open-to-work flags, the optional reasons, applications, logins, profile edits, the research
  definition of an active seeker and the change log's launches and timelines. The layoffs, the returners and the graduates are all real, and
  returners are the biggest cause of the rise. Nothing reported is overturned; the biggest cause and the bet that moves the most members are
  different questions.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice and the licensed basis. The trace still names returners, and the change log still reads as a list of
  past partnerships and pilots.
* **Instrument repair.** Suspect files: the optional reason field (21% of new seekers fill it) and the open-to-work flag (0.9M flags stale).
  Repaired so that every member carries the reason they are looking and no flag is stale, rung 0 and rung 1 both return the returners (D), as
  rung 2's trace already does, and none returns B. The answer still needs each bet's effect read against comparable markets and applied to the
  members it reaches; no reason field or flag holds either.
* **Lens swap.** The naive build measures this year's rise by cause; the answer measures the members each bet would move out of next year's
  stock, read from past launches: a different population at a different moment.

## 3. The driving force

A strong solver distrusts the open-to-work flag, because members forget to switch it off, and uses the research definition (applied in the last
30 days or switched on in the last 90). It sees that the optional reason field under-represents returners (5% of them fill it, against 55% of
laid-off members) and recovers reasons from behaviour: an account dormant for at least twelve months, reactivated, with a profile update and the
open-to-work switch within thirty days, and layoffs as clusters of colleagues ending positions at one employer in one fortnight. Returners are
then the biggest cause, 620,000 of the rise. But the template does not fund the biggest cause; it funds the cause whose fix would take the most
members out of active seeking over the coming year, and a fix is not a removal. The change log holds ten past launches of the five kinds of bet.
Read against members of the same groups in comparable markets over the same months, each kind gives a stable effect: outplacement lifts enrolled
laid-off members' exit rate 24%, but partners can enrol only 40% of them; returnships move returners 4%, because their constraint is childcare
and confidence, not search; posting incentives lift every seeker's exit rate 6% in the markets they run, applicants or not. Applied to next
year's stock, posting incentives take 340,000 members out of active seeking, outplacement 79,000.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Rise in open-to-work flags by stated reason, scaled to the whole rise | A, layoffs (595k) | The recruiting team's own view, from the profile's own field | The research definition: an active seeker applied in the last 30 days or switched on in the last 90, and 0.9M flags are stale |
| 1 | Rise in active seekers by the dated definition, by stated reason, scaled | C, graduates (410k) | The research team's own population, with stale flags gone | The change log's partner lists: stated reasons reproduce 31% of the members partners enrolled |
| 2 | The same rise with reasons recovered from behaviour (dormancy for returners, colleague clusters for layoffs) | D, returners (620k) | Every member assigned by what they did, every partner list reproduced; the biggest cause found | The change log: the two returnship launches moved their returners' exit rate 4%, against 24% for outplacement |
| 3 | **Decisive:** each bet's effect read from its past launches against comparable markets, applied to the members it reaches in next year's stock | **B, employer posting incentives (340k)** (5th of 5 on rung 0) | — | — |

* **Position table.** B ranks 5th on rungs 0, 1 and 2 (no member states a hiring freeze as their reason) and leads only rung 3. Rung leaders
  beat their runners-up by 2.02×, 1.24×, 2.70× and 4.31×.
* **Discriminator dominance.** Returners carry a 31× lead over B into rung 3 (620k against 20k). The launch reads multiply B's figure by 17.0
  and returners' by 0.10, an edge of 167×, 4.5 times the required 1.2 × 31 = 37.2; the net margin is 5.4×.
* **Partial correction priced (L3).** Every half-read log leaves another bet in front. Reading each launch before and after, without
  comparable markets, credits outplacement with the spring hiring seasons its four launches fell in and posting incentives with nothing, since
  both city pilots ran in the downturn: A 174k against D's 119k (1.47×), B 30k. Reading against comparable markets but applying every effect only
  to members a bet enrols or who apply to its postings (15% of seekers for incentives) gives A 79k against D's 63k (1.25×), B 51k. Sizing each
  bet by its cause's share of the rise, the assumed effect, gives D.
* **Grid.** Cause-share builds name A, C or D under every population, reason source and decomposition; flows with stated reasons give A 426k
  against C's 332k, with the outflow component at 190k. Bet-effect builds name A when launches are read before and after or when effects are
  confined to enrolled members, and B only when comparable-market effects are applied to every member each bet reaches. The nearest wrong cell
  is the enrolled-only build, 1.55× short of B.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The change log records each launch's market, dates and partner; no document states an effect, says how a launch
   should be read, or says that posting incentives move seekers who never apply to an incentivised posting.
2. **The corpus pins a construction, not a menu.** Read against comparable markets, each kind of bet's launches agree within a point
   (outplacement 23–25%, posting incentives 5.8–6.2%, returnships 3.9–4.3%); read before and after, the same ten launches scatter from 0% to
   80%, and no common window brings them into line. The comparison is a construction (matched groups, markets and months), not a parameter, and
   the reach of each effect comes out of the same reads.
3. **No arithmetic symptom.** Flows reconcile to the 1.20M under every assignment; launches, members and timelines tie.
4. **Not a row predicate.** An effect is a difference between groups of members in different markets over months, and a bet's reach depends on
   which members its effect lands on, applicants or not.
5. **The enumeration is arithmetic.** No column holds a bet's effect or the members it would move; 340,000 is built from ten launches'
   timelines and next year's stock.
6. **No cutover date.** The effects come from launches spread over four years; the dated events in this year (two large layoff announcements
   in the spring) are the recruiting team's decoy.
7. **Survives deletion.** With every voice gone, the trace still names returners as the biggest cause.

## 6. The calibration corpus

* **Form.** Ten launches in the product change log over four years: four outplacement partnerships, two returnship partnerships, two
  posting-incentive pilots in single cities, an early-career tools launch and a career-move tools launch, each with its dates and market, the
  partner's enrolment list where there was one, and every member's platform timeline before and after, in the launch market and in the rest.
* **What it pins.** Each kind of bet's effect on its members' exit rate and the members it reaches (above); the partner lists also pin rung 2's
  traces, which reproduce every enrolled member's reason.
* **Twin pair.** Pilots P1 and P2 had identical incentive budgets, incentivised postings and applications to them. Members taken out of active
  seeking against comparable cities were 9,000 and 4,400 (2.05×), because P1's city held twice the seekers and the extra postings lifted every
  seeker's exit rate, not only the applicants'. Only an effect applied to every seeker reached reproduces both.
* **Resemblance points at the decoy.** This year's surge in open-to-work switches matches the 2020 layoff wave in the change log, when the first
  two outplacement partnerships launched, on timing, sectors and stated reasons.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The planning template: the bet targets the cause whose fix would take the most members out of active job-seeking over the
  coming year. The research data dictionary's dated definition of an active seeker.
* **Empirical pins.** Each bet's effect and reach, from the launches read against comparable markets; the stock by cause, from the traces.
* **Voices.** The head of recruiting products: "Look at the open-to-work spikes; this is a layoff wave." The head of the returnship team: "Half
  the rise is people coming back from career breaks. Build for them."
* **Licensed wrong basis.** The template records that the public-policy team reads the rise through the government's displaced-worker series
  and will present it as layoffs.

## 8. Determinism by construction

* **Effects.** A launch's effect is the change in its members' monthly exit rate in the six months after launch, against the same group,
  tenure band and months in markets without the launch; every kind of bet's launches agree within one point.
* **Reach.** Posting incentives act on every seeker in the market, outplacement on enrolled members (partners' capacity takes 40% of laid-off
  seekers), the other bets on their whole group; members taken out are next year's stock × effect / (1 + effect).
* **Stock.** Next year starts from this year-end's 6.0M active seekers, grouped by the traces; dormancy is at least twelve months without a login
  (no reactivated seeker falls between 7 and 12), and a layoff cluster is twenty or more colleagues in one fortnight.
* **Horizon.** The coming twelve months, at this year's group sizes; the template fixes it.
* **Rounding.** Thousands of members; the committed figure sits mid-bin.

## 9. Prompt sketch and deliverables

> Active job-seekers on the platform are up 1.2 million this year and we get one product bet on the seeker side. Our CPO is convinced graduates
> are flooding in. Tell me which cause we build for and how many members the bet would take out of active job-seeking over the coming year, in
> thousands, as one line for the planning review. Send `seeker_rise_case.xlsx` and a chart `bet_effects.png`.

* `seeker_rise_case.xlsx` — the five causes under each construction, the postings sheet (ask A), the subscriptions sheet (ask B) and the launch
  reads (ask C).
* `bet_effects.png` — for each bet, members it would move next year under before-and-after reads and under comparable-market reads as linked
  dots, each bet's reach as a bar beneath, the rise by cause as a reference strip, and the chosen bet labelled with its figure.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month and each of four employer size bands, new job postings. *Device:* an employer refreshing
  a posting creates a new id with a refresh-of pointer, as the posting schema documents; counting ids overstates postings for the two largest
  bands, which refresh weekly.
* **Ask B (device-carried).** For each month and plan, new premium subscriptions on the seeker side. *Device:* annual plans billed monthly
  write a charge row each month with a plan-term field, as the billing schema documents; counting charges as new subscriptions inflates the
  annual plan twelvefold.
* **Ask C (validity).** For each of the ten launches, its effect read before and after and against comparable markets; and each cause or bet
  under each rung construction.
* **Decoupling.** Clearing the comparable-market reads changes no figure in asks A or B; posting counts and subscriptions enter no exit rate.

## 11. Rubric arithmetic

12 months × 4 bands (ask A) + 12 months × 3 plans (ask B) + 10 launches × 2 reads + 5 causes × 4 constructions (ask C) + the chosen cause, its
figure and the runner-up's + 5 named chart parts + 2 files ≈ 135 criteria.

## 12. World-building constraints

* Rise of 1.20M by trace: inflows A 0.21M, C 0.15M, D 0.57M, E 0.08M, lower job-finding 0.19M; as a stock view (rung 2) D 620k, A 230k,
  C 170k, E 90k, B 20k, other 70k.
* Reason fill rates: layoffs 55%, graduates 60%, voluntary 50%, returners 5%, 21% of new seekers overall. Rung figures (A / B / C / D / E):
  595 / 10 / 295 / 103 / 197; 330 / 20 / 410 / 170 / 270; 230 / 20 / 170 / 620 / 90; 79 / 340 / 58 / 63 / 31. Flows with stated reasons:
  426 / 190 / 332 / 105 / 147.
* Effects against comparable markets: outplacement +24% on enrolled members (40% of laid-off seekers), posting incentives +6% on every seeker in
  the market, early-career tools +9%, returnships +4.1%, career-move tools +4%. Before and after: outplacement +60%, posting incentives +0.5%,
  returnships +8%. Year-end stock 6.0M (laid-off 0.90M, graduates 0.70M, returners 1.60M, voluntary 0.80M).
* P1 and P2 identical on budget, incentivised postings and applications; their cities' seekers stand 2:1.
* Posting refreshes and billing rows touch no seeker's activity log, launch read or exit rate.
