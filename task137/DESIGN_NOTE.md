# task137: Kaimai Building Society, the agent-hours to book with Harbourline for the January to March 2027 term deposit maturity calls (architecture 1)

Private, never ships. A new build (wave 2), numbered from seed FC08: the seed's world, decision and quantity are kept (a
deposit-taker's maturity calls made by an outsourced contact centre booked in agent-hours, take-or-pay, a quarter ahead,
on a list fixed at the booking deadline); its architecture (dialling rules withheld from the contract and recovered from
the vendor's acknowledgements, with the callable-number count as the decisive unit) is not used. The dialling rules are
filed and the callable-number wash is depth; the pitfall is re-found from how the deposits on the list reprice.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task137.json`, architecture v1, registered 2026-10-12; `guard.py check` WARN on one finding (`repeat.gate_g`, answered below); `guard.py validate` clean |
| Domain / task type | banking-credit-financial-risk / deposit-liquidity-behaviour (a client domain): how term deposit holders behave at maturity when their deposit reprices onto the posted card is the deciding quantity |
| Objective | Forecasting & Predictive Modeling: the agent-hours the January to March 2027 list will use, a campaign not yet begun, forecast from the seven closed campaigns |
| Shape | other: the call and its components (the hours, the hours for each maturity month, the dials that will not reach a holder, the conversations), the note's chart and three asks on rows the call never reads; about 30 criteria, arithmetic in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (agent-hours, to the nearest 100) |
| Mechanism | gap time (decisive: the evidence is about past repricings on past cards, the bet is on a list repricing onto a much lower card), then population; pattern E (a conditioned yield, no column naming the conditioning quantity); generators G14 (the share of conversations that go to the retention offer, conditioned on the drop from the locked rate to the card) then G6 (the coming list's mix on that drop sits far from every past list's within each term); Gate G `forecasting`; strategy `composition_mix` |
| Layer 2 family / pattern | `field_method` (deposit behaviour's repricing-gap retention model); `own:repricing-gap-conditioned-retention-at-maturity` (banking has no library patterns; the family is the client's "the field's own method done right") |
| Furniture | forum `line_manager_or_team` (the head of deposits signs the block order), forcing event `purchase_order_or_contract` (the quarterly take-or-pay block order is due on Friday 20 November 2026), organisation family `cooperative_or_member_body` (a building society), role family `product_manager` (the term deposits product manager owns the campaign budget), context artifact `planning_thread` (Harbourline's request for the block order and the society's reply), calibration `none` (the past campaigns are the history the yields are estimated from, not an organ), opening `question-first`, question form `how-many` |
| Spine | `harbourline_dial_log_2025q1-2026q3.csv`, the contact centre's dial records: one row per dial on a released case, January 2025 to September 2026; constructed |
| Deliverables | `td_booking_q1_2027.xlsx` (the booking, its components and the three asks), `td_booking_note_q1_2027.docx` (a one-page note for the head of deposits opening with the block and charting it by maturity month) |
| People | drawn with `guard.py names --geo "New Zealand" --seed 137 --n 30`, keeping only names the guard clears: Hazel Johnstone (term deposits product manager, the requester), Stuart Waller (head of deposits, signs the block order), Suzanne Wallis (Harbourline account manager), Joseph Herd (customer data steward, keeps the do-not-call register), Sienna Stewart (treasury pricing analyst, prepares the quarterly card for ALCO), Ashton Findlay (Harbourline workforce planner); none appears in the prompt |

**Guard.** `guard.py check` on the scratch card: WARN, one finding. `repeat.gate_g` (`forecasting` in one of the last two
builds, task130): the key is honest, because the decisive step is how the forward share of long conversations is
forecast, conditioned on each deposit's repricing gap, and task130's mechanism (a claims-made window costed by report
lag) shares nothing with it. Bans run against the last three builds and the builds live beside this one (task128,
task136): a first draft blocked on `ban.org_family` (`financial_institution`, task128) and `ban.artifact`
(`operations_log`, task128; then `register`, task130), so the world moved to a building society and the context
artifact to the planning thread that frames the booking. A first gap draft (population, E) blocked on `test.same_driver`
against task124's lineage and on `test.same_puzzle_older`; gap time is the honest decisive gap (the stumping skill's
"a lapsing term": the quantity moves with where on the rate path each deposit locked and where it matures), and the
four older carriers of time, E and a quantity are differentiated on the card.

**Same-puzzle and same-driver tests.** Gap time, pattern E, decision `quantity_figure`, Gate G `forecasting`: no build in
the last twelve carries the four (task125 carries gap time with a composition mix on a G6 pattern; task130 gap time with
pattern none). Older carriers: task117 (draw caps of another entity through a dated join, follow-on operations re-timed
behind the one ahead), task37 v2 (a coupling to a linked entity's authorisation recovered from a closed roll), task44 v2
(a pilot's pooled gain mixing opposite effects split by a moderator), task97 v5 (the cumulative history of the place a
unit occupies). None conditions a share on the unit's own price change at a repricing; the card carries the four lines.

**Abstraction test.** Stripped of nouns, the driver is: a unit's chance of needing the long, costly form of a service at
a one-off repricing is set by the gap between the price it locked in and the schedule it rolls onto; the share is
stable across past rounds only per unit of that gap, and the coming round's dominant cohort meets a gap only a small
slice of past units met. The three nearest drivers (`guard.py nearest`: task97 v5 0.06, the place's cumulative history;
task254 v2 0.05, a cut of a time-to-event distribution seen only through events already happened; task98 v3 0.05, a
per-unit threshold on groups formed by chaining) share no latent structure, default path or correction with it.
task136, drawn beside this one, carries a campaign's yield to new sites per member still able to respond (a
denominator); here the population is fixed and nobody's eligibility moves, the share of the conversations that go
long is conditioned on a price change, and no denominator is rebuilt.

**Data-native sentence.** The society's term deposits reprice only at maturity, onto the posted card for their term,
so each holder Harbourline reaches meets in one step the whole gap between the rate they locked in and the card they
will roll onto, and that gap decides whether the conversation goes to the 21-minute retention offer; the seven past
campaigns spread their gaps across terms and vintages as the rate cycle turned, while January to March 2027 brings the
2024 three-year special at 5.75 per cent onto a 3.25 per cent card, a gap only a small slice of past deposits met.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (47 builds): hazards by time since entry
(134), selection on the outcome (124), the maturity of a claims window (130), a recycling term and a deadline-driven
draw (501), corpus-recovered conversion rates (27, 29, 30, 78), censored delays (31, 99), a slowest sub-unit (52), a
two-class mix recovered by differencing dated events (95), a campaign's yield carried per untapped member (136): none
conditions a behavioural share on the unit's own repricing gap. `stumping/references/client/two-layer-task-design.md`:
banking has no library patterns, so the pitfall comes from the `field_method` family (the field's own method done
right), here deposit behaviour's retention-at-maturity model on the repricing gap. `stumping/references/client/
measured-drivers.md`: the held tasks are a construction outside the solver's hypothesis space, upstream of every graded
figure; the drop is built across two files (the list's locked rate and the card in each quarter's campaign brief) that
no reflex joins. `guide-to-prompt/references/exemplars.md`: the 0.20 to 0.40 band misses on a window, a lag or a base;
this build's miss is the base the share is carried on. The seed's header (FC08) for the world only.

**World.** Kaimai Building Society is a mutual deposit-taker headquartered in Tauranga with about NZ$6.4 billion of
deposits, two thirds of them on term deposit (one- to five-year terms). At maturity a term deposit reinvests for the
same term at the posted rate in force on its maturity date unless the holder has given other instructions (the Term
Deposit Terms, clause 9.2). The society's Asset and Liability Committee sets the posted card each quarter, effective
on the first day of the quarter and published three weeks before it, and runs short new-money specials beside it
(the two-year special at 6.40 per cent in October to December 2023, the three-year special at 5.75 per cent in January
to March 2024, the one-year special at 6.35 per cent in July to September 2024). Since January 2025 Harbourline Contact
Services, a Palmerston North contact centre, has made the society's maturity calls under a statement of work
(HCS-KBS-2025-01): each quarter the society lists the term deposits of NZ$25,000 or more maturing in it with no maturity
instruction on file at the list cut, releases each to Harbourline 21 days before its maturity date unless the holder
has instructed in the meantime, and Harbourline works the case under the SOW's dialling rules until a conversation with
the holder, exhaustion of every callable number, withdrawal or maturity. Harbourline bills agent time at fixed minutes
per event (1.5 for each dial that does not reach the holder, 8 for each conversation, 21 for each conversation that
goes to the retention offer because the holder says they mean to withdraw or move the funds) against a quarterly
take-or-pay block the society books by the 20th of the second month before the quarter, hours beyond the block billed
at the block rate plus 35 per cent. The society's retention procedure (version 4) books the hours the quarter's list is
forecast to need, to the nearest 100.

As-of dates: the January to March 2027 list was cut on 2 November 2026 (18,400 term deposits, about two fifths of them
three-year deposits opened at the 5.75 per cent special); ALCO approved the January to March 2027 card (three years
3.25 per cent) on 27 October 2026 and it sits in the draft campaign brief; Harbourline's last close-out (July to
September 2026) arrived on 21 October 2026; the request is made on 4 November 2026; the block order is due on Friday
20 November 2026.

## Default path

1. Read the SOW (the minutes billed per event, the dialling rules, the take-or-pay block) and the retention procedure
   (the list, the release 21 days before maturity, the booking of the hours the list is forecast to need).
2. Take the 18,400 deposits on the January to March 2027 list, normalise their holders' phone numbers and wash them
   against the do-not-call register: each case's callable numbers by type (mobile, home, work), and the cases left with
   none.
3. From the seven closed campaigns (the release files, the dial log and the close-outs), price dialling per callable
   configuration: the dials that do not reach the holder and the chance of a conversation per released case, and the
   share of listed deposits that are released.
4. Take the share of the past conversations that went to the retention offer (pooled, about 29 per cent; the latest
   campaign's, about 27; or each term's own) and price each expected conversation at 8 minutes plus 13 times that share.
5. Sum over the list and round to the nearest 100.

Ends on: about 4,400 agent-hours (4,300 to 4,450 across the pooled, latest-campaign, per-term and locked-rate shares).
Golden: about 5,000 agent-hours (the share of conversations that go to the retention offer conditioned on each deposit's
drop from its locked rate to the January to March 2027 card for its term).

## Stump sentence

A competent solver washes the numbers against the do-not-call register, prices dialling per callable configuration from
the seven closed campaigns, carries the past share of conversations that went to the retention offer (pooled, the
latest campaign's or each term's) and books about 4,400 agent-hours (Ends on); the step that lands it there is not
conditioning that share on each deposit's drop from its locked rate to the card it reinvests at, which leaves the 2024
three-year special, meeting a 2.5-point drop on a list two fifths made of it, at the share of deposits that met small
or negative drops: the golden is about 5,000.

## Three rules

- **Domain test:** the deciding quantity is the share of maturing term deposits whose holders, once reached, will want
  to move their money, which deposit-behaviour analysis models on the repricing gap between each deposit's locked rate
  and the posted rate it reinvests at on maturity; with another field's nouns there is no fixed-term repricing, posted
  card, rate cycle or locked rate for the share to hang on, so the task stops making sense.
- **Analyst test:** a strong analyst who reads the SOW's billing and dialling rules and the procedure right, washes
  every number against the do-not-call register, prices dialling per callable configuration and scales by the released
  share still carries the past campaigns' retention-offer share (pooled, the latest campaign's, trended, by term or by
  the deposit's locked rate) and books 4,300 to 4,450 agent-hours, about an eighth short.
- **Layer 1:** realistic mess across the pack, none of it deciding the call: past lists in two extract layouts (rate in
  per cent with dashed account numbers through 2025, a decimal rate and unpunctuated account numbers after the January
  2026 core banking upgrade); the dial log in UTC with the contact centre's own disposition codes and case reference
  format; release files listing each case's callable numbers by type; phone numbers in mixed New Zealand formats
  normalised before the do-not-call wash; a register with added and removed dates; the posted card inside each
  quarter's campaign brief (PDF tables whose layout changes in 2026); the ask paths' own mess (an account event extract
  where an instructed reinvestment opens a new account, a whole-book maturity extract listing joint deposits once per
  holder).
- **Layer 2:** the field's method for retention at maturity: the shortcut a capable analyst takes is the share of
  conversations that went to the retention offer carried pooled, from the latest campaign, trended or by term; an
  expert in deposit behaviour rejects it because the share is a function of the repricing gap, which the coming list
  carries far from every past list's mix within each term; conditioning on the gap is the only method consistent with
  all seven closed campaigns.
- **Stump class:** analytical. The decisive step is choosing what the forward share is conditioned on; no plant, no
  field read and no filed rule decides, and every rule in the pack (the billing minutes, the dialling rules, the
  release, the do-not-call wash, the reinvestment default, the booking) is executed the same way on the default path
  and the golden.

## Tried and rejected

- The seed's architecture (FC08): the vendor's standard dialling rules withheld from the contract and recovered from its
  acknowledgements, with the callable-number count behind two number-level joins as the decisive unit. Rejected at the
  draw: a rule recovered from settled records is banned as the decisive step, and with the rules filed the callable
  count is rule application; the wash stays as depth on the default path.
- A first card in the seed's world as a bank (`financial_institution`, context artifact `operations_log`): blocked by
  the guard against task128, live beside this build (a Canadian bank's collections centres); the deposit-taker became a
  New Zealand building society and the context artifact the block-order thread.
