# task146 design note (architecture 2)

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task146.json`, architecture v2, registered 2026-11-01T00:42:44Z after a
  pull and a guard check (WARN only). Architecture 1 (the Unemployment Insurance Board's first weekly count of the
  quarter) moved to the card's lineage, retired by the batch 1 audit.
- **Pairing:** Banking, Credit & Financial Risk, task type `deposit-liquidity-behaviour`, objective Forecasting &
  Predictive Modeling (the stable balance one, two and three years on is a forecast of money the Society will still
  hold, a window not yet closed). Banking x forecasting carries three builds (task133, task177, task446), none on
  deposits.
- **Niche:** Trentmoor Building Society, a fictional mutual in the East Midlands, runs its instant-access savings on a
  run of issues (Easy Saver, a Loyalty Saver issue each spring, a cash ISA, a children's saver). Its asset and liability
  committee (ALCO) resets the structural hedge each January: receive-fixed swaps laid against the part of the
  instant-access balances the Society expects to keep, so the margin on that money does not swing with Bank Rate.
- **Quantity:** the stable balance of the instant-access savings held on 30 November 2026 at the first, second and
  third anniversaries, and from it the hedge ALCO sets in January 2027 and the change to the swaps held now.
- **Decision:** the hedge notional (a dial) and whether swaps are added, run off or left.
- **Shell:** question form how-much, the second sentence led by the committee's use, deliverables pdf+xlsx, the
  rounding sentence opened on the figures it governs; it differs from architecture 1's (how-many, put, docx+xlsx).
- **Strategy:** `decomposition_attribution` (each closing payment from an instant-access account is booked to where
  it went: into a new instant-access issue the same day, or out of the Society), gap population then time, decisive
  generator G4 (attribution at transition: who holds the money now), G13 the horizon.
- **Data-native sentence:** Trentmoor cannot convert an account from one issue to another, so a member who takes up
  each spring's Loyalty Saver closes the old account and opens the new one on the same day with the same amount, and
  the treasury's account-level extract carries no member key: the move shows only as a closing payment and an opening
  deposit that agree to the penny on one date.
- **Abstraction sentence (not writable against an approved build):** "the money a book keeps is followed across a
  container's closure into the same-day container it funded, rather than measured container by container". The
  nearest approved shapes read differently: 124 infers an unexamined unit's kind from its group's other members, 108
  removes a request made twice, 132 restarts a wear curve at a replacement, 72 (held after repair) books a transferred
  enrolment to its origin, which assigns a unit to an owner rather than keeping money in a stock.
- **Personas:** `guard.py names --geo uk --seed 146` (Hugh Clements, Liam Bowen, Jennifer Russell; Denis Law skipped as
  a real public figure, Allan Simpson for a surname shipped in task306).
- **Axes redrawn at the post-registration check.** The first registration (00:39:56Z) met `ban.forum`
  (committee_or_panel, task231 v2) and `ban.artifact` (monitoring_export, task145 v2), both filed minutes earlier.
  In a mutual of this size the Board approves the hedge each January on ALCO's recommendation, and the reset acts on
  the treasury's swap register, so board_of_directors and register are the honester labels, not merely the passing
  ones; the prompt names the Board and the paper became structural_hedge_reset_2027.pdf.
- **WARN answers.** `repeat.deliverables` pdf+xlsx and `repeat.gate_g` forecasting against task145 v2: a paper and a
  ladder workbook are what a treasury hands a board, and the mechanism is honestly a forecast. `people.first` Jennifer in task101: an older build, one first name. `repeat.gate_g` forecasting
  against task130: the honest mechanism, a forecast of money kept; task130's is a recorded rate under an incentive.
  `test.same_driver_older` against task464 v1: differentiated on the card (a response model's change point there, no
  model here).
- **Sources:** the client's rigor card deposit-prepayment-interest-rate-behavior 3 (estimate deposit decay on cohorts
  of accounts open at the start date, not on total balances) is the default path's method, rung 1, and its shortcut
  (decay fitted to the total balance) is rung 0; the field's practice for non-maturity deposits (behavioural core
  balance from vintage run-off, structural hedge laid to it). Every figure is synthetic; no real society, issue or
  member.
- **The slot's earlier deposit screen.** task170's note records a deposit cell screened on 2026-10-19 where every
  heterogeneity candidate, product migration among them, died on the composition ban of that round, not on a
  measurement. This draw is not a heterogeneity: no class of saver behaves differently; the step is the unit the
  money is followed at.

## Default path

1. Read the month-end extract and the ALM policy; take every instant-access account with a balance at each 30 November
   from 2021 whose anniversary has passed.
2. Run off each start cohort account by account, the field's method for non-maturity deposits (the client's card 3:
   cohorts of accounts open at the start date, not total balances): each account's lowest month-end balance to the
   anniversary, a closed account at zero.
3. Pool each product's kept balances over its start balances across the start dates; multiply by each product's
   30 November 2026 balance; sum.
4. Set the hedge at the first-anniversary total to the nearest GBP 1 million and size the new swap against the
   GBP 101.9 million left after the January maturity.

**Ends on:** a hedge of GBP 125 million and a new swap of GBP 23 million (the share kept a year on 57.0 per cent).
**Golden:** a hedge of GBP 165 million and a new swap of GBP 63 million (75.4 per cent kept a year on; GBP 130 million
two years on and GBP 104 million three years on).

## Stump sentence

A competent solver runs the book off on cohorts of accounts open at each 30 November and files a GBP 125 million hedge
(a GBP 23 million new swap), because a member who takes up a new Loyalty Saver issue closes one account and opens
another the same day for the same amount and the cohort books that money as gone; matching each closing payment to the
same-day opening it funded keeps it in instant-access savings and puts the hedge at GBP 165 million.

## Three rules

- Task type: deposit-liquidity-behaviour (banking-credit-financial-risk), which serves Forecasting.
- Domain test: the deciding quantity is the stable (core) balance of non-maturity deposits that sizes a structural
  hedge, estimated from the book's own run-off over each anniversary.
- Swap: "the Board sets the hedge at the stable balance a year on" read as a school's pupils kept a year on has no
  hedge, no notional and no money moving between savings issues; the quantity stops making sense.
- Layer 1: pounds against pence, month ends dated on the last business day, UTC event stamps against local dates, the
  2025 re-coding with ES02 reused, closed accounts carried at zero for a month; each comes from the core banking
  system's own extracts.
- Layer 2: estimand identification; the unit the run-off is measured at (the money, followed across a closure into the
  opening it funded, not the account) flips the hedge by GBP 40 million.
- Decisive step: following each instant-access closing payment into the same-day instant-access opening it funded, so
  a move between issues is kept rather than run off.
- Not semantics: every field, code, unit and date read correctly (pence converted, ES02 read by date, local dates)
  still leaves the account cohort at GBP 125 million; no field marks a move, and no definition is misread.
- Not rule application: FAILS the 2026-11-01 lines (commits 19c4263b, 273af233). The decisive step is an inclusion over a second source: the event log's same-day CLOSE and OPEN pairs decide which balances count as kept. Filed, it is a rule executed: policy 7.3 counts a balance as kept "to the extent the Society held it in instant-access savings at every month end", which names the money a member moves into a new issue, and the event log lists every such move, so linking it executes the estimand (task445 v2, Gate H3). Unfiled, the stable balance is an intent phrase, the literal reading files the account cohort, and the golden needs a withheld rule (task468 v5). The account-cohort route also contradicts 7.3 for any analyst who sees the moves, so it is not a route a strong analyst would file without contradicting a filed sentence. Once the money is followed nothing is left to estimate: the link is exact to the penny (4,312 of 4,312 switches recovered), and the run-off after it is arithmetic on the extract.
- Analyst test: the easy route, account cohorts, ends on a GBP 125 million hedge and a GBP 23 million new swap.
- Estimand: ALM Policy section 7.3 and 7.4 (trentmoor_alm_policy_structural_hedge_v4.pdf): products, the kept balance,
  the start dates taken together, the first to third anniversaries, the hedge to the nearest GBP 1 million.
- No decoy: nothing is planted; no memo, draft or figure argues the account-cohort answer; the Board minute states
  last year's hedge only.
- No certified replay: no certified or published figure is reproduced to recover the method.
- Lesson: a deposit book's stable balance is the money kept, and where the system cannot convert an account between
  issues the money crosses a closure; no build on file follows money across a container's closure into a stock.

## Survivor anatomy

- Actor: the member's move to a new issue has no column; it is a relation between a CLOSE row and an OPEN row of
  another account, same local day, same pence.
- Link: no key joins the two accounts (the extract carries no member number); only the amount and the local date do,
  a cross-row comparison the cohort method never asks for.
- Reflex: the field's named method, run-off on cohorts of accounts open at the start date, sits at rung 1 and files
  GBP 125 million.
- Back-test: the account cohort validates: its run-off from each earlier 30 November reproduces the accounts' own
  month-end balances and the book reconciles to survivors plus new accounts at every month end.
- Second use: the event log is the extract's own record of openings and closures and carries the closures that end
  every account in the cohort route; the balance extract is the spine every route reads.
- Shock: moves happen every April and May at about a quarter of eligible balances a year, ordinary movement; no
  product or month stands out.
- Pins: the WHAT is filed in the ALM policy section 7 (a policy in the Society's genre); no sentence names the link,
  the amount, the date or the account.

## Ladder

| Rung | Construction | Hedge (GBP m) | New swap | Dies to |
|---|---|---|---|---|
| R0 | total book a year on over the book (new money in) | 221 | 119 | the policy's kept balance (7.3) |
| R1 | account cohorts, the field's method | 125 | 23 | the same-day links |
| R2 | money followed into instant-access and bond openings | 170 | 68 | 7.2: bonds are not instant-access |
| R3 (decisive) | money followed into instant-access openings only | 165 | 63 | golden |

Separation: R1 to R3 GBP 40 million; R2 to R3 GBP 5 million; every graded figure at least 0.05 million off a rounding
edge (checks.py), pooled and averaged start dates agree on every graded figure (seed 146079, SF1).

## Tried and rejected

- The seed's mechanism (an employer-filed block of claims for idled workers that the attention signal cannot see,
  with a model-risk standard certifying the house method on 52 past nowcasts): a hidden bulk filing and a certified
  record built to bless the wrong method, both banned as the decisive step (10/10 rules 3, and the validated decoy).
- The seed's home domain (`economics-econometrics`, forecasting): banned against task145 (the pairing in the last three
  builds); the house alias `economics` would pass the guard by name only and was not used.
- Additive against multiplicative seasonality under a non-seasonal level rise (the seasonal swing fixed in claims while
  a shock lifts the level): rejected at the draw because the solvers' own defaults split both ways (statsmodels'
  `seasonal_decompose` and STL are additive, ratios and year-on-year growth multiplicative), so the stump would be a
  coin flip on a library default, not an analysis a capable analyst skips.
- An attention-signal nowcast fitted on pages chosen by in-sample correlation, validated out of sample: the client's
  own example, but `forecast_method_backtest` is task145's strategy (banned in the last three) and the decisive step
  would need a filed back-test organ two builds running.
- A Labor Day or Christmas holiday misalignment in 52-week ratios: rejected as a calendar reading (time semantics)
  that a capable analyst checks by reflex, and as task102's family.
- A benefit-year anniversary echo of last year's surge (claims filed again 52 weeks on): rejected as too near task134
  v2's driver (an inflow a pool sends a year after entry) and too small at realistic re-employment.
- The national figure at a US scale (about 220,000 a week) or at 40,000: prototyped on 2026-10-15; the golden's
  defensible variants (the estimation sample, the base week, the step's form) spread 2 to 3 per cent, wider than a
  thousand-claim bin; a country of about 9 million (about 12,000 claims a week, the first week about 16,000) keeps
  every variant inside one bin with the rivals two or more bins off (prototype, eight seeds).
- The world prototype's first settings (2026-10-15): a pandemic surge of 4.3 times and holiday weeks at 8.5 per cent a
  day lost biased the rate (0.070 against the world's 0.084) and spread the golden's constructions over 827 claims;
  the surge was softened to 2.35 times and the holiday effects to 3 per cent a day.
- High-ineligibility quarters placed mostly in the third quarter: they lifted the fourth-quarter intercept every rival
  carries and put the level-driven and ratio rivals in the 15,000 bin, one bin from the golden; spread across the year.
- The episodes of 2022 to 2026 as first set: the high pools all fed the April turns and the January turns with the
  largest calendar moves followed the low pools, so the post-2022 construction came out about 650 claims low in every
  world seed; rebalanced, and the January return and shutdown softened, after which it is noise around the others.
- An attention-signal ask (the seed's encyclopedia page views, or search-interest exports each scaled to its own peak):
  its index needs a filed construction a careful solver executes, and its UTC-hour and rename devices are found by
  the battery; dropped.
- An insured unemployment rate ask (continued weeks over covered employment): every device found (fortnightly
  certifications, provisional quarters, an office restructure) is adjudicated by the definition a careful solver
  executes, so none holds the cracker.
- A first-payments ask (payments reissued under fresh ids): the battery's claim-and-week dedupe repairs it.
- The industry classification as a full renumbering: a raw join then gives implausible changes that invite the check;
  kept as partial code reuse with every total tying.
- The refiling at one national rate as the decisive step (the design paused on 2026-10-15): under the strict reading of
  rule 3 the base-period definition, read against the quarter turn, lets a careful reader infer that refused claimants
  can file again, and once inferred the natural sizing (the national determinations at the rate past turns show) is the
  golden, so the decisive step leaned on reading a definition; deepened so the share differs by region and the national
  rate on the national pool files a bin low (2026-10-16).
- A refiling share by the month of refusal (claimants refused late in the quarter come back more): a duration-dependent
  pool too near task134 v2's hazard by time since entry, and three monthly pools too collinear to separate three shares
  from 50 turns.
- A refiling share by the reason for monetary ineligibility: which reasons a base-period move cures can be read off the
  reasons' definitions, the same semantics lean one level down.
- A quarter-end separation bump in every quarter's last claims week (tried so that no-intercept rates miss): it gave the
  October turn a negative step of its own that crude ratios ignore, which carried a crude last-four-turns rate onto the
  golden; replaced by the fiscal year's end in June alone and a summer shutdown spanning the first January week.
- The 2025 boom quarters at the usual regional mix: the last four turns' national rate then sat near the golden; in
  this world the boom regions refused few claimants through 2025 and early 2026, and the latest-period rates read low.
- The national refiling at a steeper level only (re-centring the golden by the rate): the national-pool rival rose with
  it; the golden was re-centred through the late-2026 level, which moves every construction alike.
- Ask A's first-layoff dates stored as UTC stamps of local midnight (the device drafted at the pause): the hygiene
  battery executes UTC conversions (measured in-house), so it would not hold the cracker; the portal's lodgement stamps
  stay in UTC as texture.
- Ask B's week labels against the quarter-of-the-Sunday rule as a device: a filed rule adjudicates it; kept only as the
  cube's label switch at its rebuild, which no sentence states.
- The portal going live on 1 June 2026: the register then held few notices with first layoffs in October to December,
  so the re-keying touched three cells; moved to 1 July 2026, the fiscal year's start.
- Random coverage of the regions' cross-region sites: two cells carried only in-region employers in one draw, so the
  cracker hit them; every region and period now carries a site of an employer registered elsewhere by construction.
- The legacy weekly file's weeks labelled by their Saturday (the drawn Layer 1 item): read at face value for the
  quarter, the label moves the 29 legacy turns a week early and the call from 15,994 to 12,491 on the world, so a mess
  item could flip the call; both claims-system layouts key the week by its Sunday, and the Saturday-to-Sunday switch
  stays only in the cube, as Ask B's ledgered device (2026-10-16).
- The refiled claims and the rest of the week stated to the nearest 500 (4,500 and 11,500): the ratio form puts the
  refiling at 4,889 and the mean of three weeks as base puts the rest at 11,784, so no rounding is shared by every
  construction; stated as 4,000 to 5,000 and 11,000 to 12,000, which every construction and a one-sigma move keep.
- The regional first-week shares stated in whole per cent (about 2 in the Capital, 21 to 27 in Western, Coastal and
  Island): one sigma moves the Capital's 2.1 across 1.3 to 2.9; stated in words (one in five, one in four, fewer than
  one in ten), which every construction and a one-sigma move keep.
- The program statistics published on the fifth working day (7 October), before the weekly release of the month's last
  claims week: the month would make that week public before its advance count; published with the Thursday release,
  the last week at its advance count.
- A bank desk holding Employer Services' register and case notes with no record of how: the desk's data log records
  them as released on its information request, beside where every other file came from.
- "Most of the rise" for construction and accommodation in the preview: they rose 15,963 against a total rise of
  12,604; the sentence now says more than the whole rise, nine of the other twelve groups lower (asserted).
- base-period refiling left to the definitions: data semantics, per the rule 3 audit
- The three tourism and building regions' refusals moving independently of one another (the stage 3 world): their part
  of the pool hardly varied across turns (standard deviation 0.051), so pooling cost the national fit nothing visible
  (leave-one-out 414 against 400) and the national rate sat one bin low; a common quarterly factor for the three regions
  now shows the misfit in the history (2026-10-16).
- Ask B's rounding floor raised to 0.27 of a bin: unreachable for the smallest group, whose change moves about half a
  bin with each claim; kept at the design's 0.23.
- regional sizing alone: both top responses land it once the refiling is filed, per the rule 3 re-audit
- A refusal's weight decaying over four weeks with month swings of 0.22 (the first strengthening world): the month
  model predicted past turns no better than each region's quarter taken whole (leave-one-out 322 against 319), the
  April 2020 turn's pandemic fall swamping the timing; a 2.5-week decay with larger month swings, common to the three
  regions, and timed episodes separates them (303 against 635).
- The September wave on the history as it stood (no late waves): the 2026 last-month refusals over the base week sat
  beyond every past turn and the multiplicative form overshot to about 17,600 (18,000); with late waves in the history
  and September's refused share at 0.55, the multiplicative form lands the golden's bin (17,225).
- Late layoff waves in the recent quarters (Western 2022, Coastal 2024): they lifted the timing-blind constructions on
  the recent windows to about 16,600, inside a bin of the golden; made early waves (2026-10-16).
- The first draw of the month swings' streams: the national step on the three regions' months and the rest's filed
  16,437 (16,000), 460 claims under the golden on a standard error of 220; among forty draws, the one kept holds every
  construction of the golden within 310 claims.
- The week ended 3 October at a round 11,800 (the late-claim share's first range): a round headline count reads as
  made up; the range moved to 0.0023-0.0095 (11,814), which also keeps Ask B's nearest change 0.281 of a bin from its edge.
- Architecture 1 (the Unemployment Insurance Board's first weekly count of the fourth quarter, sized from the refiling
  pool region by region), retired 2026-11-01 by the batch 1 audit before any portal result: it was designed before the
  survivor anatomy gate, its note carries no Actor, Link or Reflex line, and precut.py fails it (no `Measured by:` line
  naming the script that ran the cracker on the cut pack); the refiling share was the part that fell short, a sizing a
  careful reader takes once the base-period definition is read. Re-rooted rather than repaired so the portal sees one
  strong build.
- Re-root draw screens (2026-11-01), each rejected before a card: a vineyard's frost nights under inversions (dead in
  task170's notes, and a probabilistic transfer with the right residual variance lands the count without any regime);
  a reserving triangle's settlement-speed or inception-mix change (Berquist-Sherman is a named correction; task176's
  notes measured the cell); amount-weighted pensioner deaths and a lapse wave at a linked mortgage's fixed-rate end
  (task171's miners' trust died on persistence; the linked-contract clock is task176's driver); scaling laws under
  data repetition and a strategy's borrow costs (task171's screen; task306's participation curve); a delisted brand's
  demand read from stock-outs (a filter and a divide, task171's note); a health plan's default under inertia (the
  opponent's first move once the default is filed); a practice closure dispersed through households (task124's group
  members' records); reactive inspections inflating a fault rate (filing the scheduled programme names the population,
  task269 v4's law).
- Architecture 2 as a whole (2026-11-01, on paper at stage 2, before any reader or judge): spent by the rule
  application lines the skills took from the day's deaths (19c4263b: a filed estimand naming the members one
  source misses, shipped beside a source that lists them, makes linking it rule application; 273af233: an
  inclusion or exclusion over a second source has no safe filing). Following the money across a member's move
  between instant-access issues is exactly that inclusion: policy 7.3 files it and the event log lists every
  move, while dropping 7.3's wording leaves the account cohort as the literal reading. The world, generator and
  goldens stay green (target.zip 06b54fc7) as history; the slot re-roots into another world with the decisive
  step drawn as an estimate no shipped source lists.
