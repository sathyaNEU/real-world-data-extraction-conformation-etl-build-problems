# task268 design note: Corcally's Roastery 2027 sampling, the rival brand whose buyer homes least often already buy the Roastery

Architecture 5, a re-root drawn 2026-10-31 in Descriptive & Distribution Analysis (the number's objective), client domain
Marketing & Consumer Research, task type segmentation-market-structure. Architectures 1 to 4 are in the card's lineage and in
`## Leak check

`leak.py --asof 2027-01-13` on the cut pack: REVIEW, no LEAK. Each REVIEW line, ruled in this thread:
- The brief carries four words of the committed call ("2027 Roastery sampling ... homes"): it is the brief that sets the
  decision and names no brand. Harmless.
- The merchant agreement carries "online, settlement, terminal" and the Rewards terms "online, member, members": the
  agreement's own schedule and settlement clauses and the scheme's own card clauses; neither names a home, a shared card
  or a match. Harmless.
- The deal log and the product master name the brands beside numbers (funding per multibuy, shelf prices): neither ranks
  the rivals on overlap. Harmless.
- The online export's `generated` stamp read as a generator's word: renamed `exported_at`.

## Duplicate check

`guard.py heart` on the cut pack: WARN (three_rules.strategy_risk, answered by `Analyst test:`; the older same-puzzle and
same-driver notes against task131 v1 and task264 differentiated on the card). `guard.py surface` promoted two pairs for
the author's adjudication: task267 (back to back: the gap label and a pick in common; its driver reweights a screened
population's checked members by their checking rate, nothing here does) and task264 (the same-driver signature, already
differentiated). Personas in the pack: Alix Fennell only, on the card.

## Tried and rejected`.

## Draw

- **Card.** `.claude/skills/fingerprint/cards/task268.json`, architecture v5, `guard.py check` WARN (three_rules.strategy_risk
  on grain_or_unit, answered by `Analyst test:`), differentiation filed against task131 v1, task126, task114, task179 and
  task264; nearest drivers 0.08 (task116) and under.
- **Pairing.** marketing-consumer-research / segmentation-market-structure / descriptive-distribution; marketing has carried
  no descriptive build. The market-structure measure is the duplication of purchase between brands' buyer bases: of the homes
  that bought a rival brand in 2026, the share that also bought Corcally's Roastery, the chain's own-label coffee.
- **Decision.** Corcally's (a family-owned grocery chain in a Midlands market town, Drumsallagh, and its hinterland) sends
  its 2027 Roastery sampling to the homes of one rival coffee brand, the rival whose 2026 buying homes least often also
  bought the Roastery. Retrospective by design: the brief reads the closed calendar year 2026, the last full year of
  purchases, and the sampling runs in 2027.
- **The quantity.** For each rival brand, the share of its 2026 buying homes that also bought the Roastery, a home counting as
  a buyer when any of its members bought the brand at Corcally's in 2026, in a store or online.
- **Data-native sentence.** Corcally's Rewards issues a card to each adult member and pools nothing, the online shop keeps its
  own accounts, and the only record that two cards, or a card and an online account, belong to one home is that they pay with
  the same bank card, which shows as a shared card token in the acquirer's settlement file; partners split the coffee
  aisle (one buys capsules, the other the Roastery), so card by card the capsule brand's buyers look untouched by the
  Roastery while home by home they mostly already buy it.
- **Abstraction sentence (nearest approved builds).** task126 and task114 rebuild a counting unit from records a second system
  groups (dockets into applications by a credit class; bookings into meetings by invitees and badges); this build rebuilds the
  buying unit from member records that share nothing but a payment instrument in a third system, and the decided quantity is
  a duplication of purchase between brands. A reviewer holding task131 v1 (card-randomised offers, household interference)
  would say both turn on cards in one household: task131 v1 had the membership on file as a key and an experiment to read;
  here there is no household key and no experiment.
- **Shape.** 14, cuts of a distribution per segment: for each rival its buying homes, those also buying the Roastery and
  the share (seven rivals, 21 figures), the call, its share, the runner-up and the gap (4), the deck's chart (5 named
  parts), the two files (2), and two asks off the call's rows: the loose coffee the Drumsallagh counter sold of each guest
  roaster by quarter (12) and the multibuy funding each supplier owes by quarter (24). 68 criteria before the rubric's
  own instruction lines.
- **Strategy.** grain_or_unit, gate method_or_model_selection, generators G10 (what is one real-world buying unit), G2, G6;
  gap population; Layer 2 estimand_identification.
- **Sources (one line each).** The client's segmentation-market-structure card 4 (switching judged against share-based
  expectation) is the field's method this build keeps at rung 1 and reads at the card; task131 v1 (household interference,
  landed on the portal because the membership key sat on file) is why this build ships no household key; task120 v1 (a
  solver union-found households through a dependents schedule one join away) is why the link here is a shared payment card
  in a file kept for card-acceptance reconciliation, never a household or member field.

## Default path

1. Read `coffee_till_lines_2026.csv`, map each PLU to its brand through `product_master_coffee.xlsx` (folding the three
   spellings of a brand into one), keep the 2026 lines of the eight brands' packs presented on a Rewards card, and drop
   the cards `rewards_cards_2026.csv` types as store cards.
2. Fold each replaced card into its successor through the register's `replaced_by`, so a member is one buyer.
3. Add the online shop's delivered orders from `online_orders_2026.json` (each order's final version, by delivery date)
   as each account's purchases.
4. Build the duplication of purchase table at the loyalty programme's customer unit, the field's method: for each rival,
   the members and accounts that bought it, those that also bought the Roastery, and the share.
5. Read the lowest share. Nordhavn's capsule buyers seldom buy the Roastery, which reads as the capsule format's
   partition from ground coffee, and the analyst files it.

- **Ends on:** Nordhavn, the rival whose buying cards least often also bought the Roastery.
- **Golden:** Oro Rosso, the rival whose buying homes least often also bought the Roastery.

## Stump sentence

A competent analyst builds the duplication of purchase table on the Rewards card, the chain's customer unit, and names
Nordhavn, whose capsule buyers are mostly a home's second card while the home's other member buys the Roastery on their
own; assembled from the Rewards cards and online accounts that pay with one bank card in Faircourt's settlement file, a
match no key offers, homes put Oro Rosso lowest and Nordhavn mid-table.

## Three rules

- **Task type:** segmentation-market-structure (marketing-consumer-research), serving descriptive-distribution: the
  duplication of purchase between the brands' buyer bases is the market-structure table a segmentation analyst reads.
- **Domain test:** the deciding quantity is each rival's duplication with the Roastery at the household buying unit, the
  share of the rival's buying homes that also bought the Roastery, read the way the duplication of purchase law reads
  brand overlap in a household panel; the field's estimator is that table built on the unit that buys for one cupboard.
- **Swap:** "whose 2026 patient households least often also used the hospital's own clinic": a patient's visits are
  their own and nothing is split between members' cards, so the household unit changes nothing and the call no longer
  turns on how the buying unit is assembled; the swap breaks the task.
- **Layer 1:** four systems with four identifiers (the tills' Rewards card, the online shop's account, the register's
  member, Faircourt's card reference); settlement in UTC against Irish till time and settled one or two banking days on;
  a Lisgarvan terminal replaced in May; lost cards replaced under new numbers; store cards swiped for shoppers without
  one; brand names spelt three ways; online orders amended before cut-off and some cancelled; refunds on later receipts.
  None decides the call.
- **Layer 2:** estimand identification, the population a duplication table must count: the buying unit is the home,
  which the records hold only as Rewards cards and online accounts that settle on one bank card; the table on cards
  files Nordhavn, on homes Oro Rosso.
- **Decisive step:** recognising that the coffee repertoire belongs to the home and is split between its members'
  personal cards, and rebuilding each home as the cards and online accounts that pay with one bank card, which needs
  every till transaction matched to its settlement row on terminal, time and amount before the overlap is read.
- **Not semantics:** every field can be read correctly (the register types each card as a member's or a store's, the
  terms say a card is one member's, the card reference is a payment card) and the table built on members still files
  Nordhavn; the homes are in no field and appear only when card references are compared across two systems' rows.
- **Not rule application:** no filed rule assembles a home: the brief files the unit (a home, anyone in it) and the
  terms that a card is a member's, and the construction is the analyst's. Enumerated family (card, member, member and
  account, homes from store cards only, homes from cards and accounts; store cards kept or dropped; the settlement clock
  converted or not; a link on one, two or three shared payments): Nordhavn at 14.6 to 16.5, Westquay at 25.6 and Oro
  Rosso at 39.0 to 41.1 per cent on the cut pack, three calls. Standing family (every route that assembles homes from
  cards and accounts, drops the store cards and converts the clock or matches on the day): one call and identical
  figures, Oro Rosso 39.9, the thresholds converging (asserted).
  The ruling-out is quiet: the terms' personal-card clause and the brief's "anyone in it", neither naming a payment.
- **Analyst test:** with every file conformed and every rule read, the strong analyst builds the duplication of
  purchase table on Rewards members and online accounts as the customer unit and files Nordhavn as the least
  overlapped rival, when Nordhavn's capsule buyers are mostly the second card in a home whose other member buys the
  Roastery on their own card.
- **Estimand:** `roastery_sampling_brief_2027.docx`: for each rival, the share of the homes that bought it in 2026
  (anyone in the home buying a pack on a Corcally's Rewards card in one of the three stores or through the home's online
  shop account, an online order on its delivery date, 1 January to 31 December 2026) that also bought Corcally's
  Roastery packs in 2026, compared across the rivals.
- **No decoy:** nothing is planted to be caught: no memo, draft, briefing or stakeholder figure argues for Nordhavn or
  any rival; the brand tracker (a distractor) reports claimed brand use, never an overlap; the store cards and the
  replaced cards are the register's own records; no block is copied and no rule is hidden.
- **No certified replay:** no certified or published figure is reproduced to recover the method; nothing in the pack
  ties only under the golden.
- **Lesson:** a duplication table is only as good as its buying unit: loyalty cards are people while the cupboard is
  the home's, and where the scheme holds no household the home is rebuilt from evidence the business keeps for another
  reason, the payments it settles, before brands are compared; no build on file rebuilds a buying unit from a shared
  payment instrument through a settlement match.

## Survivor anatomy

- **Actor:** the deciding property is the home a card belongs to, and no file has a column for it: the register holds
  cards and members (no household, address or account link), the online shop holds accounts, Faircourt holds card
  references; the home is a relation between rows of three systems.
- **Link:** read through a match no key offers: a till transaction carries no settlement reference, so each is matched
  to its Faircourt row on terminal (through the merchant agreement's terminal schedule), time (UTC against Irish time)
  and amount, and cards sharing a card reference are one home; online orders join on their order number. No sentence
  invites it: the brief names homes, never payments.
- **Reflex:** the field's method, the duplication of purchase table, built on the programme's customer (the member, or
  member and account) files Nordhavn at rung 1, its low overlap reading as the capsule format's partition.
- **Back-test:** the textbook route validates: on members the table shows the pattern a category analyst expects (the
  rivals' overlaps with the Roastery close to one level, the capsule brand partitioned off), every member count ties
  to the register, and nothing in the pack contradicts a member being a buyer.
- **Second use:** every file the decisive step reads has its own reason: Faircourt's file carries the Drumsallagh
  counter's card payments, without which the counter ask cannot tell a sold label from a re-weighed one; the merchant
  agreement's terminal schedule places the counter's terminal; the till lines, online orders and register carry the
  call's purchases and the store and replaced cards.
- **Shock:** the movement reads as ordinary: on members Nordhavn's low overlap is the capsule partition and Oro Rosso
  sits mid-table; Oro Rosso is not the extreme of any shipped column or simple statistic (buyers, price, pack size,
  supplier funding, the tracker's claimed use), asserted.
- **Pins:** the WHAT is filed once, in the brief, in the Roastery team's own genre (homes, anyone in them, the three
  stores and the online shop, 2026 by delivery date); the terms file that a card is one member's; no filed sentence
  names a payment card, the settlement file, a match or a threshold, and deleting any one filed sentence leaves the home
  the unit (the terms alone make a card a person) without handing over how it is built.

## Readability screen

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | 7 Organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 baskets: share of the rival's transactions that also carry the Roastery | no | no | fires (a basket view) | no | no | no | no | readable |
| R1 members and accounts as buyers, the duplication table | no | fires (the card column) | fires (the field's method) | no | no | no | no | readable |
| R2 homes from store cards through the settlement match, online orders left out or accounts kept apart | no | no | no | no | no | no | no | silent |
| R3 (decisive) homes from cards and online accounts through the settlement match | no: the brief names homes, never payments | no: no key joins a till row to a settlement row | no: the field's table is built on its panel's or programme's unit | no: no control scores homes | no: no duplicate, clock or rescind repair builds a home | no | no: the settlement file carries the counter ask | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | home | the people living together, held as the cards and accounts that pay with one bank card | a Rewards card or member as the home | Nordhavn | the terms: "Each card is issued to one member"; the brief: a home buys when "anyone in it" bought |
| SF2 | bought a brand | a pack on any of the home's Rewards cards in a store, or on its online account | store-card or anonymous lines put to a home through the match | same call (asserted) | the brief: "on a Corcally's Rewards card ... or through the home's online shop account" |
| SF3 | the Roastery | Corcally's Roastery packs | the counter's loose coffee counted | same call | the counter sells guest roasters only (asserted) |
| SF4 | rival | the seven other brands in the product master, spellings folded | each spelling a brand | same call (asserted) | the master: the spellings share a supplier and range |
| SF5 | 2026 | Irish date on the tills; online orders by delivery date | UTC date; order date | same call and figures (asserted) | the brief's delivery-date clause |
| SF6 | online order | the delivered final version | every version; cancelled orders counted | same call and figures (asserted) | the export's status field |
| SF7 | store cards | dropped | kept as a member | same call, figures move (asserted) | the register's card type and the terms' member-prices clause |
| SF8 | replaced cards | folded into the successor | kept apart | same call and figures at the home (asserted) | the register's replaced_by; one member pays with one bank card |
| SF9 | a shared payment | one shared payment links | two or three needed | same call and identical figures (asserted) | convergence |
| SF10 | the settlement clock | UTC converted to Irish time | read as Irish time | same call, figures move (asserted) | the column name and the agreement: times are UTC |
| SF11 | terminal schedule | by its dates | the current terminal only | same call (asserted) | the schedule's installed and removed dates |
| SF12 | an online account no card shares | a home of its own | dropped | same call (asserted) | the brief: a home buying online is a home |
| SF13 | refunds | a refunded pack still bought | refunded packs removed | same call and figures (asserted) | convergence |
| SF14 | the share | the rival's buying homes as denominator | the Roastery's homes as denominator | Westquay | the prompt: "whose 2026 buying homes least often also bought" |
| SF15 | rounding | whole per cent from counts; gap from unrounded shares | rounding first | same figures (mid-bin asserted) | convergence |
| SF16 | tie-break | none needed | none | same call | margins of 1.15 or more asserted |

## Ladder

| Rung | Construction | Winner | Its share, next and margin (the cut pack, seed 263) |
|---|---|---|---|
| R0 | baskets: the rival's transactions also carrying the Roastery | Nordhavn | 0.8 against Westquay 1.0 per cent, a basket view nobody files |
| R1 | the duplication table on cards; on members | Nordhavn | 14.7 against Westquay 23.2, x1.57; 14.6 against 23.7, x1.62 |
| R1 (default path) | the duplication table on members and online accounts (the field's method) | Nordhavn | 16.5 against Westquay 23.7, x1.43 |
| R2 | homes from store cards through the match; online left out | Westquay | 25.6 against Oro Rosso 32.1, x1.25 |
| R2 | the same with online accounts kept apart | Westquay | 25.6 against Oro Rosso 33.9, x1.32 |
| R3 (decisive) | homes from cards and online accounts through the match | Oro Rosso | 39.9 against Nordhavn 48.7, x1.22; Halloran's third at 51.1 |
| hazards | store cards kept; the clock read as Irish time; unlinked accounts dropped; store-card and anonymous lines put to homes | Oro Rosso in every one | 40.0, 39.0, 39.7, 41.1: the call holds, the figures move only where a shipped sentence rules the reading out |

- **Position and dominance:** each rung names its own brand and dies to one shipped fact (R1 to the terms' personal
  cards; R2 to the brief's online clause); every correction walks one way (towards homes) and only R3 reverses
  Nordhavn; margins of 1.15 or more at every rung are asserted in `checks.py` on the cut pack, with Oro Rosso's share
  0.15 or more from its rounding edge.
- **Pricing sequence.** 1 Residue: how the buying unit is built from cards and accounts, a method, not a knob (the link
  thresholds converge). 2 The move: from the default path to R3 Nordhavn rises 32.2 points (16.5 to 48.7) and Oro Rosso
  10.4 (29.5 to 39.9), against a ceiling of every card in a home merging (the true homes, unseen by any file: Nordhavn 73.3, Oro Rosso 48.9, still the lowest). 3 The
  one-group-by route is R1 (group the lines by card or member), Nordhavn; nothing affine in a shipped column reaches
  Oro Rosso. 4 The standard error of Oro Rosso's share on 1,857 homes is 1.1 points; the gap of 8.8 points is eight of
  them. 5 The lever is structural (the unit), not a variance. 7 Subsets: online accounts alone name Kinvara Hills, heavy
  buyers' cards Nordhavn. 8 Reflex sweep as code: cards, members, members and accounts, heavy cards, online accounts
  alone, the reverse duplication (Westquay) and baskets, none Oro Rosso (asserted in `checks.py`).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | homes with a 2026 pack of a rival on a Rewards card or online account | WHAT in the brief |
| 2 Unit of account | the home (cards and accounts on one bank card) | WHAT in the brief; terms' personal cards |
| 3 Attribution window | a purchase in 2026 by Irish date, online by delivery date | WHAT in the brief; C1 asserted |
| 4 As-of dating | the register at the extract date, every 2026 card | C1: replacements fold either way |
| 5 Version basis | online orders' final delivered version | C1 asserted |
| 6 Denominator | the rival's buying homes | the prompt's wording |
| 7 Weighting | none: each home counts once | WHAT in the brief |
| 8 Window length | the calendar year | WHAT |
| 9 Boundary inclusivity | 1 January to 31 December inclusive | WHAT |
| 10 Rounding path | counts exact, share rounded once | C1 mid-bin asserted |
| 11 Tie-break | none needed | margins asserted |
| 12 Maturity and censoring | none: the year is closed | n/a, same call |
| 13 Order of operations | assemble homes, then read brands | C1: the reverse order is not defined |
| 14 Row order | none | same call |
| 15 Duplicate resolution | a line once; versions once | C1 asserted |
| 16 Identity normalisation | the three brand spellings folded | the master's supplier and range; asserted |
| 17 Netting against gross | refunds do not remove a purchase | C1 asserted |
| 18 Dimensional units | homes, a count; share in per cent | WHAT |
| 19 Code and status semantics | store cards out, cancelled orders out | the register's type; the export's status; C1 |
| 20 Integerisation | homes whole, shares whole per cent | the prompt |
| 21 Clause scope | the counter outside the brief | the brief; C1 (guest roasters only) |
| 22 Forward window contents | the 2027 sampling reads 2026 only | WHAT (retrospective by design) |

## Literal reader

Executed word for word (the brief's homes with anyone in them, on Rewards cards in the three stores and online
accounts, the terms' one-member cards, packs of the eight brands, 2026 by Irish date and delivery date), the only
executable home is the group of cards and accounts that settle on one bank card; a card as the home violates the
terms, dropping an online-only home or adding store-card lines violates the brief, and thresholds, replacement folding,
refunds, versions and cancellations converge (asserted in `checks.py`). Re-run on the cut pack (seed 263): every licensed
reading prints Oro Rosso at 40 and Nordhavn at 49; the readings that move a figure (the clock read as Irish time,
anonymous receipts put to homes) each violate a quoted sentence. Passes.

## Oracles

- The register's card counts tie to the member table on the wrong path and to the home table's cards on the right one:
  no oracle.
- The counter's card takings do not tie to the labels under any handling (accessories rung on the same terminal), and
  the counter lines on the tills are one label each: no control total arbitrates ask A.
- The deal log's funding per multibuy and the till's saving lines tie to nothing outside the pack: no supplier claim is
  shipped, so ask B has no control.
- The census households file and the brand tracker (distractors) confirm nothing on either path.

## Ask sheet

**Ask A.** The loose coffee the Drumsallagh counter sold of each guest roaster in each quarter of 2026, kilograms to one
decimal (three roasters by four quarters, 12 figures).
- H18 home: a qualifier on the call's reach: the counter runs outside Rewards, so the deck sizes, roaster by roaster,
  the coffee the brief's homes cannot see.
- Use: the Roastery team's view of the specialty coffee sold beside it.
- Primary 1 (D4, absence across systems): a label printed and re-weighed is binned, and only the second label is paid;
  a label is sold only if a counter card payment (Faircourt, the counter terminal, UTC) or a counter line on a till
  (cash) pays it, and the card payment also carries accessories keyed on the terminal, so it is matched as labels plus
  accessories from the counter's price board.
- Primary 2 (D8, a clock): scale 2's clock reset to 1 January after a power cut in April and ran from there until a
  service visit; its labels for those days carry January dates, out of step with their own label numbers, and only the
  payments date them.
- Hazards: scale 2 exports its weight in grams, scale 1 in kilograms; the settlement clock in UTC (shared with the call).
- Files and columns: `counter_scale_labels_2026.csv` (label, scale, printed, roaster, coffee, weight, price per kg,
  price), `faircourt_settlement_2026.parquet` (terminal, time, amount), `faircourt_merchant_agreement_2026.pdf` (the
  counter's terminal), `coffee_till_lines_2026.csv` (the counter PLU lines), `coffee_counter_price_board_2026.pdf`
  (accessory prices): five files, 14 columns.
- Stops: every label (re-weighs counted, all figures high); labels matched but the reset left in January (Q1 high, Q2
  low); the reset fixed but re-weighs kept; labels matched to card payments only, the cash half dropped (all low).
- Pin test: the asking sentence pins sold coffee, the roaster, the quarter and kilograms; the devices sit in which rows
  are sales and which date a sale carries, neither named.
- Realism: a weighed-goods counter with two scales of different firmware, a standalone card terminal and cash paid at
  the main tills is how a grocer's specialty counter runs.

**Ask B.** The multibuy funding each supplier owes Corcally's for each quarter of 2026, counting every multibuy a
customer got, by the quarter it was sold in, whole euros (six supplier accounts by four quarters, 24 figures).
- H18 home: a second measure per candidate: what each rival's supplier put into its 2026 multibuys at Corcally's.
- Use: the quarterly funding claims the buying team raises.
- Primary 1 (D7, the key elsewhere): on a deal's first days at one store the tills missed the multibuy; the service desk
  later refunded the saving as a multibuy adjustment line on another receipt whose note cites the original receipt, and
  the funding belongs to the deal and the quarter of that original sale.
- Primary 2 (D1, opposite meanings): a refund that breaks a multibuy rings a saving reversal with the same promotion
  code and the opposite sign, so a count of saving lines adds a multibuy that was taken back.
- Hazards: a deal revised mid-run with a new funding rate from its effective date (written in the deal log); the till
  ran one deal three days past its end at one store (outside the deal's dates, unfunded); Bellvale's deals were agreed
  with its distributor until 30 June and with Bellvale Foods from 1 July while the master names the current supplier.
- Files and columns: `multibuy_deals_2026.xlsx` (deal, supplier, brand, PLUs, mechanic, start, end, funding, version,
  effective from), `coffee_till_lines_2026.csv` (PLU, promotion code, value, note, date), `product_master_coffee.xlsx`
  (brand, supplier): three files, 13 columns.
- Stops: saving lines counted, adjustments ignored (all low where a miss happened); adjustments dated on their own
  receipt (quarter shifted); reversals counted as savings (high); the current supplier for Bellvale's first half.
- Pin test: the asking sentence pins every multibuy a customer got and the quarter it was sold in; the devices sit in
  which records are one multibuy and which date it carries.

**Separation.** Zero device or hazard rows in the call's row population (the eight brands' packs on Rewards cards and
online accounts): the counter labels, counter lines, accessory payments, adjustment and reversal lines sit outside it,
counted from the shipped rows in `checks.py`; the call is unchanged when every ask device is deleted.

| Cracker (lands the call, runs the battery, executes every filed rule, reads every helper) | Ask A | Ask B |
|---|---|---|
| The cracker: labels deduplicated, grams fixed, deal revisions and windows applied, reversals netted | miss | miss |
| The full includer: every device it can find handled, the silent one left | miss | miss |

| Measured on the cut pack (seed 263) | Ask A kept | Ask B kept |
|---|---|---|
| the cracker | 0 of 12 | 0 of 20 |
| the mirror (stops at R1; card payments matched, till lines left; adjustments on their own date) | 0 of 12 | 4 of 20 |
| the full includer (scale 2's block left where its clock put it; one multibuy per adjustment line) | 3 of 12 | 4 of 20 |

- **Mirror leakage:** 21.9 per cent of ask weight (the best response off the call keeps 7 of 32 ask figures).
- **Pair ceiling:** 34.5 (the cracker keeps 0 of 32 ask figures, the best miss 7 of 32).
- **Measured by:** `generator/ceiling.py` on the cut pack (seed 263), run by the build after every change.

## Tried and rejected

- The seed's own stump, residential density against daytime presence, rejected at the draw on 2026-10-18: with the estimand filed as the people present, choosing presence over residents is reading the estimand (data semantics); left unfiled, the call is not determinate.
- Network ride times against straight-line catchments (urban network analysis), rejected at the draw: a filed twenty-minute ride makes the street network the literal method, so the decisive step would be rule application.
- The plug-in bias of the weighted density from noisy survey counts per tract, rejected at the draw: the same insight as task253 (sampling noise counted as signal).
- Attendance conditioned on commute distance as a continuous covariate, rejected at the draw: the functional form opens forks on every graded figure; the county type of residence carries the same structure with nothing to choose.
- A mobile-device presence panel, rejected at the draw: a column holding the deciding quantity scaled, which R1 forbids and which reads the call off.
- Six distinct winners on six rungs, tried in the prototype on 2026-10-18: consecutive corrections move the cores too little to clear 1.15x margins at every rung; the ladder keeps three rungs with their own winners (every job present, the share by industry group, the share by industry group and county type) and the work-from-home reflex as a hazard landing on rung 0's metro.
- The draw's prototype shares (other services 0.80, 0.45, 0.20 against a survey mix of 0.45, 0.30, 0.25 in every industry), set aside at stage 2 on 2026-10-18: a quarter of every industry's workers living outside their workplace's metro is not the national pattern; with the survey's mix by industry (other services 0.48, 0.30, 0.22) and the realistic shares, two office cores cannot both clear 1.15, so Corrisford became a port and logistics core whose drivers and remote sales staff, living mostly outside the metro, are seldom on the premises.
- The draw's registration slot, set aside at the end of stage 2 on 2026-10-18: the draw-time `guard.py check` ran before the pull that brought in task165 (composition_mix, operations_director, registered at 14:10) and task167 v2 (population, E, method_or_model_selection, 06:59), so the card filed at 16:11 carries ban.strategy, ban.role and test.same_driver BLOCKs against them; three conditioning-transfer drivers in one batch is the template the bans exist for, and the composition stump is this seed's own pitfall, so the design is kept and the card re-registered once the batch has moved past them.
- Architecture 1 (the survey's share of weekdays on the premises carried onto each commuting flow within industry group and the type of county the worker lives in), spent at stage 4 on 2026-10-18: the isolated reader, working the cut pack cold at medium effort, carried the share by industry group and HOMEREL onto every flow as a matter of course and committed Tessavon at 28,805 against Corrisford's 21,709 (`score_reader.py` exit 1, the call 5 of 5, every core density); the decisive rung was readable through the schema, because the survey carries the residence relation as a column the codebook defines against the workplace's metropolitan area, which types every flow through the delineation file, and an analyst carrying a survey rate onto counts carries it on every classifier the two sources share, so the stratum the design called decisive is the careful analyst's reflex. The judge found the call forced and Gate H passing, and two ask forks (a workplace outside any metropolitan area is HOMEREL 4 in the codebook where the golden typed those flows 3; Ask B's partner-shop rule unfiled). In this world a stratification the survey's own columns invite cannot carry the stump; the re-root draws a decisive step no classifier the sources share can reach.
- The seed DA18's world itself, set aside at the re-root on 2026-10-18: every lever the weekday-presence measure offers is a rate carried within strata the survey and the counts share (residence relation, commute distance, shift times, firm size), which the careful analyst stratifies on by reflex, or a choice the board paper already files (residents, primary jobs, latest releases, the core's tracts).
- Length-biased sampling (a census-day stock of stays weighted by inverse length, a stop's random-arrival wait), set aside at the re-root draw: task264 in this lane already weights members sampled in proportion to their events, and a wait read with the inspection paradox is the transit field's standard excess-wait formula, a reflex for a strong solver.
- Measurement-error deconvolution of a distribution's tail, set aside at the re-root draw: task246 deconvolves measurers' error and task253 in this lane shrinks noisy unit averages.
- Values below varying detection limits, detection-corrected counts, dual-list capture and capacity-censored demand, set aside at the re-root draw: task189, task242 and task462, task196 and task448, task168 carry them.
- A return-wave nowcast for leavers whose window is open (the seed DA19's natural stump) and a nowcast conditioned on whether a leaver's post is held, set aside at the re-root draw: task157 carries the calendar-gated return wave, and the held-post nowcast is a composition shift (`composition_mix`), banned against task165 in the window and spent three times in this lane.
- The stage-2 contraction model (each cell's density proportional to its habitat quality to a power solved each year), set aside at stage 3 on 2026-10-18: a large power pulls the deep band's own cells apart, so the band does not hold together and the survey's plain mean sat within noise of the stratified mean (Halmorie Deep 39 to 47 per cent against Brettach Bank's 48 in the structural runs); replaced by band multipliers, the basin read by depth band, with Halmorie Deep enlarged to 80 cells so its deep band is a tenth of the area, which puts the plain mean 14 points under the stratified mean before any noise.
- Torn and weather-missed survey stations placed anywhere, set aside at stage 3 on 2026-10-18: on Halmorie Deep or Brettach Bank a balanced-panel or imputation reading moved a graded fall across its rounding edge in most seeds; the torn stations are on Vallaskie Hole (rough edges to the hole) and the missed one on Cullardy Patch, and the call, both falls and the gap are asserted unchanged under either reading.
- Seeds 1 to 200 searched on cut packs for the ladder's margins, every graded figure 0.12 or more from its rounding edge, the gap the same from unrounded and rounded falls, the convergent readings printing alike and every ask figure missed by the cracker and the over-cleaners: seeds 22, 40, 67, 69, 94 and 184 passed; 69 kept, the widest clearance (0.31 points) with every rung's margin 1.18 or more.
- Architecture 2 (the members' catch rates against the autumn survey's fixed stations, each depth band weighted by its share of the ground's stock area), spent at stage 4 on 2026-10-18: the isolated reader, cold at medium effort, went to the survey first and weighted the bands by area as a matter of course, reading plan 4.2's "weight of haddock on its stock area" with the manual's equal stations per band, and committed Halmorie Deep at 63 per cent against Brettach Bank's 52 with every fall (`score_reader.py` exit 1); it never weighed the logbooks. The judge found the call forced and Gates G and H passing. A survey whose design document describes its strata and allocation, under an estimand filed as a total over an area, makes the design-based estimator the careful analyst's default rather than a stump; the preferential-sampling rung below it is never reached by a reader who reads the plan first.
- Architecture 3's first draft (a motor mutual's 2027 telematics pilot region by January to September claims frequency, the claims not yet notified completed claim by claim on their own notification channel's development, pooled or regional development over-completing the region that moved to the app), dropped before registration on 2026-10-18: it is task181 v2's per-route delay completion, which a solver landed once the estimand was filed, with task451's handler-speed change on top; a channel column makes the per-channel development the careful analyst's reflex.
- Re-root screens on 2026-10-18 before this draw, each set aside with its record: values below detection limits (task189, task190, task183, task248, task246), Pareto interpolation within an income band (task264's own rejection: no decision rests on it), a concentration-discharge rating curve's retransformation (task135 v1 and task452 v1: the textbook construction was the default), anchor equating of two test forms (task450, task464), demand censored at capacity (task168, task147), dual-list capture (task248, task253), informative dropout in a growth curve (task257: multiple imputation lands without the insight), the dissimilarity index's small-unit bias and tempo-adjusted fertility (each estimand names its method), beta-binomial reach extrapolation (two collinear forms fit four insertions alike) and classification consistency at a cut score (classical and IRT estimators split the figures).
- The first informative-censoring prototype (the retirement hospital's patients diagnosed later, 2026-10-18): with a worse class mix at diagnosis its true survival sat so far below the urban hospital's that Kaplan-Meier found it too; its difference now lies in age (death rates 1.10 to 1.18 times and worsening 1.25 to 1.4 times the others') on a mix like theirs, and the cardiology group's departure ends follow-up for over half of Wrenhaven's patients, so the worst-case and complete-case routes fall on Wrenhaven, not Gullhaven.
- The stage-3 world with Gullhaven's moves high in every class (a north intercept of -5.2 to -5.5, a death multiplier of 1.22 to 1.25), set aside at stage 3 on 2026-10-18: a third or more of Gullhaven's patients moved north within two years, more than a retirement coast's return of the frail carries; the moves now concentrate on class IV visits (a quarter of them end in a move) with the death multiplier at 1.16, so 22 per cent move, 96 per cent of them in class III or IV.
- Seeds searched under the kept world on cut packs (2 to 81, 302 to 347, 502 to 547, 2026-10-18): every rung's pick and margin, every form of the decisive estimator printing the same whole percent for every hospital, the golden 0.1 or more from its edges and every ask figure missed by the cracker; 28 and 515 passed, 28 kept (515's truth separated Gullhaven from Fennick by 0.7 points only). Seeds 2 to 123 of the earlier world, searched alongside, were dropped with that world.
- Ask B's re-enrolments under the new record number as its primary device, set aside at stage 4 on 2026-10-19: every solver maps the record numbers through the crosswalk to link the Florida deaths, and with every number current the re-enrolments show as one patient enrolled twice; the round-1 reader left all 143 out and hit all ten figures. They stay as a hazard.
- The overwritten diagnosis dates at the 2025 year end (a November 2025 module update), set aside the same day: they took December 2025 diagnoses out of a count by the date shown while the re-enrolments put patients in, and on the registry as it stands the two cancelled on one of Fennick's figures; at the 2024 year end both move the count the same way.
- Brenmoor's first mix at diagnosis (34 per cent in class III or IV), set aside at stage 4: the default path's gap, Fennick to Brenmoor at 2.26, printed 2 like the golden's Gullhaven to Fennick at 2.08, so a Kaplan-Meier response stated the graded gap's number.
- The relocation recorded on the date of the visit where it was reported, set aside at stage 4 on 2026-10-19 (the round-2 judge's SEND_BACK, margin_or_boundary_fragility): an analyst who takes the class from the visits before the loss date drops that visit and carries a third of Gullhaven's movers from the milder class of the visit before, which put the landmark and fixed-class estimators at 66.9 to 67.3 against the golden's 64.9 and the gap at 2, 1 or 0. The registry now records a relocation when it processes that visit's note, one to four days later (manual 3.3), so the last visit precedes the loss date under every convention.
- A move allowed only after a quarter in the same class, tried the same day to close that convention instead: it made the move depend on the class history, so weights by the class at the visit no longer matched the moves and the projection fell 0.4 to 1.1 points below the weighting in every seed searched.
- The re-consent deadline of 1 April 2024, moved to 1 January 2025 the same day: 942 withdrawals with up to twenty months left carried Wrenhaven's figure from 71 to 73 across the estimators; with a year at most left it holds at 72 under every one, and leaving the withdrawn out still names Wrenhaven.
- The round-1 and round-2 world (Gullhaven's class-specific death rate 1.16 times the others', class IV improving 8 per cent a quarter, moves at 2.2 per cent of class III visits and 24 per cent of class IV), rejected after stage 4 round 2: the judge's class-adjusted estimators put Gullhaven between 64.9 and 67.3 per cent; pooled outcome models imported the other hospitals' death rate and the fixed-last-class and landmark models misread the movers' improvement, so the gap read 2, 1 or 0 by method.
- A seed search in that world with the relocation dated after the reporting visit (450 seeds), rejected: two seeds kept every by-hospital form in one bin, none with the pooled forms agreeing, and their leads were a point; luck in the seed was not a forced answer.
- Wrenhaven's re-consent on 1 January 2025 with three in four withdrawing, rejected in fix pass 2: its 2023 patients carried up to a year past the withdrawal spread the estimators 0.5 points on Wrenhaven; the deadline moved to 1 May 2025 with nine in ten withdrawing, the spread 0.3, the dropped and dead-counted readings still on Wrenhaven.
- A later deadline with Wrenhaven's mix unchanged (1 March or 1 May 2025), or 1 June with it sicker, rejected in fix pass 2: too few withdrawals for the dropped and the dead-counted readings to land on Wrenhaven rather than Gullhaven, and the complete-case route then lands Gullhaven within a point of the golden's figure.
- The discrete projection counting a death only within 91 days of a visit, corrected in fix pass 2: a visit kept late or missed dropped about one death in twelve, so the projection ran 0.2 to 0.5 points high on Gullhaven.
- Ask A asked as "the NT-proBNP tests its laboratory reported", replaced in fix pass 3: read literally every released row is a reported test, so counting a corrected specimen once rested on a supersession rule no file states (stage 4 round 3's judge); the unit is now the specimen, filed in the prompt, and no correction crosses the referral level.
- Portal round 1 (2026-10-28): both responses missed the call (rubric average 12.5); both determinism judges failed it as answer_contradicts_files, reading the charter's 3.2 ("Every patient ... counts, including patients the registry no longer follows") as the deaths on file over every patient, a lost patient counted alive (R0, Fennick). Not a redesign: closing the reading leaves the default path (Kaplan-Meier, Fennick) where it was. Repaired at the WHAT only: 3.2 now puts every patient in the share and says the registry does not learn of the deaths of the patients who left follow-up; SF13 asserted; the write-up's steps say why the deaths on file cannot stand for survival and why the class at the move carries a lost patient's chance of dying. No estimator filed.
- Determinism repair, round 1 of the portal (2026-10-28), sent back: with 3.2 reworded the re-judge (pass 5) accepted the crude reading as closed, then returned NOT_DETERMINISTIC, SEND_BACK. Gate C: plain Kaplan-Meier, every move as ordinary censoring, is a standard reading every filed rule allows and names Fennick (61.16 against Gullhaven 62.35), while carrying the lost from their class is filed nowhere; Gate G: the mechanic classed single_conceptual_flip, a standard statistic rejected as misleading. Two corrections of one graded quantity (determinism-check section 3): filing the class-carried estimator makes the decisive step rule application, filing Kaplan-Meier makes Fennick the answer, so the stump lives in the fork and no closure keeps it. Redesign of the decisive step at stage 2 (/build task268 from 2): keep the registry world if a split off the censoring treatment can be found, else re-root. Carry forward: 3.2's wording that closes the crude reading (every patient in the share as they were at two years; the lack of a death on the registry's files does not show a lost patient alive; a first wording, "whose deaths the registry does not learn of", was still read as alive by default), the deck's embedded-workbook stamps pinned, the Linux-only rebuild, and block 1's Wrenhaven count, 347, which did not reproduce (931 every CNR event, 336 those inside the two-year window).
- Architecture 4's first card labels, Gate G `forecasting` and strategy `composition_mix`, withdrawn on 2026-10-28 before any data was cut: the vocabulary defines forecasting as a forecast the correctly read past does not pin, and this design's closed years pin the development; composition_mix and the executive forum then met task270 v11's bans. Redrawn to method_or_model_selection, forecast_method_backtest and committee_or_panel, each the honest key.
- A notifying-channel column on the claims extract (Policyholder, solicitor, claims-management company and the rest as one field), rejected at stage 2 on 2026-10-28: with the Standard's back-test filed, every grouping the extract's own columns offer is an enumerable model class behind a shipped test, which the library records as an answer key (task38). The extract keeps the claims system's coarse notified-by field, and the firm type lives on the representatives table.
- Region-level development as the default, with no filed selection criterion, rejected at the draw: task127 v3 and this slot's architecture 3 died at the judge for leaving the method open. The Standard files the back-test in general terms and puts regional estimates on the whole book's factors (3.2), so each region's own development is against the text as well as failing 2022.
- A Severn own-damage rate at its first value and a Pennine wave of 0.55 per 100 car-years, measured on the prototype on 2026-10-28: the route split itself named Mersey and Severn (Pennine 8.03 against 8.25). The wave became 0.85 per 100 car-years and Severn's own-damage rate 7 per cent lower; seed 5 is the first of six where every route-based development prints the same five figures and the back-test separates at 1.1 against 6.8 per cent.
- Ask B (private-car claims notified on 2026 accidents by region, injury against the rest, the online notification journey's abandoned first records as its device), retired at stage 4 on 2026-10-28: the determinism judge's first pass found the call and Ask A uniquely forced and Ask B open, because no shipped file says the abandoned record is the phoned claim and the Standard's 2.1 ("every claim notified counts once, including claims closed without payment") reads literally for counting it. The device cannot be both determinate and silent: identity filed or carried on the row, the careful solver executes 2.1 and the cracker keeps the ask; left unfiled, it is a fork. The twins were taken out of the world (2026 rows only, no figure of the call moved) and the ask layer became the cars on cover by all three covers, the reconstruction the judge confirmed.
- Architecture 4 (a motor insurer's 2027 telematics pilot regions, the claims not yet notified developed by notifying route, the route built by joining each claim's representative to the representatives table), spent 2026-10-31 on the learning loop's paper screen: the route sits one join away (the notified-by field and the representatives table) and development by notification channel is the reserving field's own refinement, so the decisive rung was a reflex; the slot moves to marketing-consumer-research (segmentation-market-structure), a new world, dataset, generator and prompt shell.
- Marketing draws screened on paper before this one, 2026-10-31: excess duplication judged over shoppers whose stores stock both brands (task281's note: filing the co-availability population is rule application, leaving it unfiled forks the call); a receipt-scanning panel whose submissions rise in a brand's bonus weeks (the correction needs a submission model, so the estimator family is open); a sub-panel's cross-media duplication applied to the full panel (one consistency check of the sub-panel's TV reach against the full panel's lands it); an exposure crediting quirk in the as-run log (reading what a record means, data semantics); mystery-shopper audits inflated by detection (the calibration against the CCTV census is the natural data-fusion reflex and reaches the golden).
- The bank-card reference carried on the till lines themselves (a card alias beside the Rewards card on every row), set aside at stage 2 on 2026-10-31: a self-join on a column of the main file is the one line of code the survivor anatomy's Link test refuses, so the card reference lives only in Faircourt's settlement file, reached by a match on terminal, time and amount.
- A card acceptance cost by store and quarter as the settlement file's own ask, set aside at stage 2 on 2026-10-31: the cost belongs to another owner (finance) and the organisation already has it on Faircourt's monthly statements (H18); the settlement file's second use is the counter's card payments instead.
- The Roastery's own loose beans at the counter, set aside the same day: a home buying them would open a fork on what buying the Roastery means; the counter sells guest roasters only.
- A link standing on any single shared payment, measured on the prototype on 2026-10-31: with one in three couples' links resting on one or two shared payments, a reading that needs two or three moved Oro Rosso's share by six points and named Nordhavn at three; a home's shared card is now a habit (used three times or more by each card it links, the weaker uses falling back to the member's own card), so one, two and three shared payments build the same homes.
- Counter labels matched only to card payments, set aside the same day: the counter's card takings would tie to the sold labels (an oracle for both devices); cash customers pay at the main tills and the counter terminal also takes accessories, so no total ties.
- Seeds 1 to 81 and 101 to 266 screened on the in-memory world on 2026-10-31 for every rung's winner and margin (1.15, the decisive 1.2), the runner-up a point clear of third, every share off its rounding edge (the call and runner-up by 0.15), the gap rounding alike from unrounded and rounded shares, link thresholds identical, online accounts alone never naming the call, both asks' figures off their edges and the cracker missing every ask figure: seeds 263 and 276 passed; 263 kept (its one-line adjustment stop keeps 4 of 20 against 276's 11).
- The counter's card terminal as the only way to pay, and a scale clock reset in April, set aside in the stage 3 build on 2026-10-31: with no cash route the counter's takings tied to the sold labels, and a two-week April reset moved only three cells; cash labels now go to the main tills, the reset runs 22 June to 14 July across the second and third quarters, and the funding rates are odd cents so no quarter sits on a half euro.
- Multibuy deals whose cheapest pair cost less than the deal price, found in the stage 3 build: a pair of Cafetto Original 200g at 14.98 against a two-for-15.00 deal produced negative savings; every deal now lists packs of one price.
