# task451 design note

Architecture 1 (drawn 2026-10-13, wave 2, oviya1301; the decisive step settled at design the same day, before any data was cut).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task451.json`, registered 2026-10-13 (guard PASS), revised at design 2026-10-13 and re-checked (WARN only: `driver.near` 0.18 against the slot's own draw-time card; every other driver at 0.05 or less).
- **Slot:** seed ET08 (analytical_tasks/07_data_extraction_conformation, header and Situation only): a consortium of donors and the organisations they fund publish to IATI, and the board opens three country coordination offices in the countries where the most of its money is spent. The world, the decision and the quantity are kept; the pitfall is re-found from the data under the 10/10 rules.
- **Pairing:** Survey Research & Official Statistics / census-register-administrative-data-quality / Data Extraction & Conformation (ETL). Aid statistics are compiled from administrative reports (the publishers' own IATI records), and the compilers' method for money that passes through pooled funds is the imputed flow: an intermediary's spending in a country credited to its funders in proportion to their part of the resources that paid for it. The ETL objective: several publishers' records in two layouts, currencies, value dates and the delivery chain's double reporting conformed into one table of the members' money by the country it was spent in.
- **Shape:** other: a register of the 13 candidate countries, each carrying three measures (the members' money spent there in 2025, the members' commitments there still unpaid at 30 June 2026, the organisations the members paid directly for work there in 2025), the call taken on the first. 39 country figures, the three countries, the two funds' member shares and the chart: about 47 criteria before the generated rubric selects.
- **Strategy:** decomposition_attribution. The money spent in a country is decomposed by whose money it was, each pooled fund's part at the mix of the money the fund held when it paid.
- **World:** a London-based donor collaborative of six foundations funding maternal and newborn health in East Africa, the Sahel and South Asia. Its members fund implementing organisations directly (project grants with a country) and through two pooled funds: a global maternal health fund, which collects its donors' contributions in the last quarter of each year and pays the collection out in full as annual grants the following year, and a regional fund for the Sahel, whose funders (the global fund, two members from 2025 and a regional facility) pay in each January and which pays the round out as one-year grants the same year. Non-member donors give to both funds. Every member, both funds and every organisation they fund publish to IATI. The members' council decides on 9 December 2026 where to open three country coordination offices; the host-country agreements and office leases are signed in the first quarter of 2027.
- **Forum and forcing event:** council_or_assembly (the members' council), purchase_order_or_contract (the host-country agreements and leases). Organisation foundation_or_funder, role research_desk (the secretariat's head of data and learning). Personas from `guard.py names --geo "United Kingdom" --seed 451`: Lesley Hunter, Lee Sykes, Gail Dobson, Kieran Patel.
- **Data-native sentence:** the global fund collects its contributions in the last quarter and pays the collection out the following year, so its 2025 grants were paid from its 2024 collection, of which the members gave 31.7 per cent; in its 2025 collection, which arrived after its last 2025 grant, a member's replenishment and a partner's withdrawal took the members' share to 75 per cent, and the Sahel fund, which pays out each January round the same year, carried the global fund's money into its 2025 grants at the 2024 mix.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`, decomposition (the quantity split by its true source): the country spending split by whose money it was; here the source of a fund's spending is fixed by what the fund held when it paid.
  - `stumping/references/strategies.md` F5 (the pooled rate does not fit this pool): the year's contribution mix is a correct rate for the contributions and the wrong one for the money spent, the mix rebuilt from each fund's dated receipts and payments, never read off a column.
  - `stumping/references/strategies.md` Part 6 (every reflex lands wrong): the year's share, the lifetime share, a lag on both funds and the receipts-before-payment share each file a named wrong three.
  - `dataset-generation/references/layer1-messiness.md` (layouts changing, currencies inherited, the same event reported twice): the Layer 1 here, none of it on the decisive step.
- **Same-puzzle and abstraction:** the decisive generator G6 (the pool's mix shifted under the rate) with Gate G decomposition_attribution clears the window; the nearest drivers sit at 0.05 (task111 v1 lineage, task101, task89 v12, task93 v3): none credits an intermediary's spending to its sources at the mix of what it held when it paid.

## Default path

1. Read the implementers' 2025 expenditure from the Datastore extract, convert each transaction to US dollars at the exchange table's rate for its value date, and place it in its recipient country (multi-country activities by their percentages).
2. Take each spending activity's funder from its participating organisations: a member, the global fund, the Sahel fund or another donor.
3. Credit member-funded spending in full and fund-funded spending by the members' share of the fund's 2025 contributions (the year's imputed share), the global fund's contribution to the Sahel fund carrying the global fund's share.
4. Total by country, rank, and take the top three.

Ends on: Rwanda, Uganda and Mali.
Golden: Rwanda, Kenya and Mali, each fund's spending credited by the members' share of the money the fund held when it paid (the global fund's 2024 collection, 31.7 per cent; the Sahel fund's January 2025 round, 34.4 per cent with the global fund's part carried at 31.7; design values, the generator fixes the figures).

## Stump sentence

The default path opens the offices in Rwanda, Uganda and Mali because step 3 credits each pooled fund's 2025 spending by the members' share of the contributions paid into it in 2025, while the global fund paid its 2025 grants out of the 2024 collection it held, when the members' share was 31.7 per cent, not the 75 per cent of the 2025 collection that arrived after its last 2025 grant; credited by the money each fund held when it paid, Kenya replaces Uganda.

## Three rules

Task type: Survey Research & Official Statistics / census-register-administrative-data-quality, serving the ETL objective (the publishers' IATI records in two layouts conformed into the members' money by country, each fund's spending traced to the resources that paid for it).
Domain test: the deciding quantity is the members' money spent in each country, which aid statistics compile as an imputed flow, each intermediary's country spending credited to its funders by their share of the resources that financed it, carried through every layer of the delivery chain; the compilers' same-year contribution share stands in for that only while a fund's donor mix is steady, and an expert matches a fund that collects in arrears to the year of money it spent. With a retailer's nouns there are no pooled funds of commingled donor money, no contribution cycle and no delivery chain, so the task stops reading.
Swap: put a hospital system in ("which three regions get care coordinators, by where the system's money was spent") and there are no pooled multi-donor funds paying out last year's collection, no non-member co-funders and no chain of publishers each reporting the same money, so the call no longer reads.
Layer 1: the funds' activity files in IATI XML and the Datastore's flattened transaction CSV with differing layouts, the funds' grant activities present in both; transactions in several currencies, some leaving the currency to the activity default, converted at their value dates; the same payment reported by the payer (disbursement) and the receiver (incoming funds) at different dates and in different currencies; commitments, payments, receipts and expenditures in one file; multi-country activities with recipient-country percentages; organisation identifiers under registry and IATI-assigned schemes, and one member's previous identifier. All of it is what IATI publishers' systems and the Datastore write; none is placed to be caught, and no item mishandled moves the call (asserted per item).
Layer 2: allocation_constraints (decomposition by source): the money spent in a country credited to the members in proportion to their part of the money that paid for it, each fund's part being the mix of what the fund held when it paid, carried through the fund that pays into the other.
Decisive step: matching each pooled fund's 2025 spending to the money it held when it paid (the global fund's 2024 collection, paid out over 2025; the Sahel fund's January 2025 round, paid out the same year) and crediting the members by that mix, the global fund's part of the Sahel fund carried at the global fund's; no document names a fund's balance, its cash cycle or which year of money a grant used.
Not semantics: every field read right (each currency converted at its value date, each transaction type kept or dropped correctly, each funder identified, each fund's receipts and payments dated) still leaves the members' share of a fund to be worked out, and the year's contribution share, the lifetime share and the share of contributions received before each payment, all built from correctly read fields, rank wrong threes.
Not rule application: the methodology note files the WHAT (the members' money spent in each country in 2025, directly or through one or more pooled funds, in US dollars at the value date) and no rule says which contributions paid for a fund's spending; executing every filed rule leaves the share open, and the default path executes every one of them.
Analyst test: a strong analyst who converts every currency at its value date, keeps the implementers' 2025 expenditure, identifies each activity's funder and credits each pooled fund's spending by the members' share of its 2025 contributions (the year's imputed share), the global fund's money in the Sahel fund carrying the global fund's share, opens the offices in Rwanda, Uganda and Mali; with the share of every contribution the funds have received, in Rwanda, Kenya and Uganda.
Estimand: the collaborative's methodology note (member_funds_methodology_2026.pdf, section 2): the members' money spent in a country in a year is the expenditure in that country in that year, by the organisations that spent it, of money that came from the members, whether the members paid it to those organisations directly or through one or more pooled funds, in US dollars at the exchange table's rate for each transaction's value date.
No decoy: no document, extract or stakeholder ranks the countries or states a fund's member share; the funds' files carry their own receipts and payments, which tie under every handling, and nothing is planted to be caught.
No certified replay: nothing published is reproduced; no figure in the pack is matched to recover a method.
Lesson: a pooled fund's spending belongs to its funders in the proportions of the money it held when it paid, so a fund that collects in arrears spends last year's mix and the same-year contribution share misplaces the money once the donor mix moves; no build on file teaches it.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the year's imputed share through both funds (default) | the methodology note's "directly or through one or more pooled funds" sends the solver into both funds | the funds' receipts and payments carry provider and receiver identifiers, so the chain is a join | yes (the compilers' same-year contribution share) | no | no | no | readable |
| R1 the share of every contribution the funds have received | no | the funds' full receipt histories sit in their files | yes (smooth a volatile one-year share) | no | no | no | readable |
| R2 the share of contributions received before each payment | no | the receipt and payment dates are on every row | partly (a dated cut on the receipts) | no | no | no | readable |
| R3 (decisive) the money each fund held when it paid | no: no document names a fund's balance, its cash cycle or which year of money a grant used | no column: the funds report receipts and payments, never balances; the global fund's 2023 collection being paid out in 2024 shows only by setting its 2024 payments against its 2023 receipts | no: the reflexes (the year's share, the lifetime share, a lag) each land elsewhere | no: no figure states a fund's member share or the members' money spent anywhere | the battery does not find it | no: a stock and flow per fund, then carried through the second fund | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the members | the six organisations on the member register | past members; the funds' other donors | same call: the register lists no departure, and no other donor is a member (asserted) | the member register |
| SF2 | money spent in a country | expenditure reported by the organisation that spent it, in its recipient country | the funders' disbursements by the grant's country | for the funds' money, same call and the same figures (each fund's grants are spent within the year paid, asserted); for the members' direct grants, Rwanda, Nepal and Kenya | the methodology note: "A payment from one organisation to another is not spending." |
| SF3 | in 2025 | transaction date in 2025 | value date in 2025 | same call and figures: no 2025 expenditure has a value date in another year (asserted) | the methodology note's dating rule |
| SF4 | money that came from the members | the members' own money, paid directly or through one or more pooled funds, credited in proportion to the members' part of what paid for it | the members' own payments only (donor view); one fund deep (the global fund's money in the Sahel fund counted as not the members'); the funds' money counted as the members' in full | Rwanda, Nepal and Kenya; Rwanda, Kenya and Tanzania; Rwanda, Mali and Uganda | the methodology note's "directly or through one or more pooled funds" and "money that came from the members" (the partners' and the regional facility's money did not) |
| SF5 | a pooled fund's spending, whose money it was (a convention of HOW, forced by the records) | the members' share of the money the fund held when it paid: the global fund's 2024 collection, the Sahel fund's January 2025 round with the global fund's part at the global fund's share | the 2025 contributions' share (R0); the share of every contribution received (R1); the share of contributions received before each payment (R2) | R0 Rwanda, Uganda and Mali; R1 Rwanda, Kenya and Uganda; R2 Rwanda, Kenya and Tanzania | the records: the global fund received its 2025 collection after its last 2025 grant, and its 2023 collection and the Sahel fund's 2024 round were paid out in full before 2025 (each fund's dated receipts and payments); first in first out, last in first out and pro rata of the balance all give the golden shares (C1, asserted) |
| SF6 | US dollars | the exchange table's rate for the transaction's value date, the transaction date where it carries none | the transaction date's rate; the year's average rate | same call (asserted) | the methodology note's conversion rule |
| SF7 | a transaction's country | its own recipient country where it names one, otherwise its activity's, split by the activity's percentages | the whole activity to its first country | same call (asserted) | the methodology note's country rule |
| SF8 | the three countries | the three highest totals | none | the third leads the fourth by 1.25x (design) | not applicable |
| SF9 | the global fund's transfer to the Sahel fund | counted once, where the Sahel fund's grantees spend it | also counted as the global fund's own spending | same call: the transfer carries no country (asserted) | the methodology note: a payment between organisations is not spending |
| SF10 | spending with no country | none in the network's 2025 expenditure | not applicable | same call (asserted: every 2025 expenditure carries a country) | the records |
| SF11 | organisations that do not publish | none: every organisation the members and the funds paid publishes its spending | not applicable | same call (asserted) | the council paper: the members and both funds require their grantees to publish |
| SF12 | the members' own spending | none: no member spends directly | not applicable | same call (asserted) | the records |

## Ladder

Design arithmetic (scratch LP at `t451/lp3.py`, margins 1.25 / 1.12 / 1.10); `generator/checks.py` asserts every rung by name on the built pack.

| Rung | Method | Global fund share | Sahel fund share | Three | Third over fourth | Dies to |
|---|---|---|---|---|---|---|
| R0 (default) | the year's imputed share, through both funds | 75.0 | 60.0 | Rwanda, Uganda and Mali | 1.26 | the global fund's 2025 collection arrived after its last 2025 grant |
| R1 | the share of every contribution received | 47.6 | 27.7 | Rwanda, Kenya and Uganda | 1.14 | the 2023 collection and the 2024 round were paid out in 2024, and the 2025 collection after the last 2025 grant |
| R2 | the share of contributions received before each payment | 30.5 | 20.5 | Rwanda, Kenya and Tanzania | 1.13 | money already paid out before 2025 funded none of the 2025 grants |
| R3 (golden) | the money each fund held when it paid | 31.7 | 34.4 | Rwanda, Kenya and Mali | 1.25 | none |

- **Off the ladder, each a named wrong three:** the donor view (the members' 2025 payments by country), Rwanda, Nepal and Kenya; the members' direct spending alone, Rwanda, Kenya and Tanzania; one fund deep at the right mix, Rwanda, Kenya and Tanzania; a lag applied to both funds (the previous year's share), Rwanda, Kenya and Tanzania; the mean of the annual shares, Rwanda, Kenya and Uganda; the funds' money counted as the members' in full, Rwanda, Mali and Uganda; the global fund's money in the Sahel fund counted in full, Rwanda, Mali and Niger.
- **Grid.** Two fund depths (one fund deep, through both) by five share bases (the year's, every contribution, before each payment, the previous year's, held when paid): ten cells, the golden three in one (asserted).
- **Separation.** Each rung names a different three; the golden's third (Mali) leads the fourth by 1.25x; every other reading misses the golden three by at least 1.12x on its nearest swap (design).
- **Walk.** R0 to R2 lower both shares (the global fund's from 75.0 to 30.5, the Sahel fund's from 60.0 to 20.5); the decisive move takes the Sahel fund's back up to 34.4, the one reversal.
- **Position.** On the default path Kenya is fourth and Uganda third; on R2 Mali falls below Tanzania.
- **Dominance.** The decisive move shifts the Sahel countries by 0.14 of the Sahel fund's spending and the global fund's countries by 0.43 of its spending against R0; Uganda's carried advantage on R0 (its global fund money at 75.0) is gone at 31.7.
- **Worth.** The decisive move changes one office of three on R0 (Uganda for Kenya) and one on R2 (Tanzania for Mali); every graded country figure with pooled money moves with it.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the members' money: the six members on the register; spending by every organisation that spent money from them | SF1, SF4; the register |
| 2 | Unit of account | one expenditure transaction, credited by its activity's funder's member share | SF2, SF5 |
| 3 | Attribution window | calendar 2025 by transaction date | SF3; the methodology note |
| 4 | As-of dating | the Datastore extract pulled on 5 October 2026 | every publisher's 2025 reporting complete by the pull (asserted: each last update after 31 March 2026) |
| 5 | Version basis | each activity as last published; one member's superseded dataset holds no 2025 transaction | asserted: the old copies stop in June 2024 |
| 6 | Denominator | each fund's money held when it paid | SF5, C1 |
| 7 | Weighting | the members' share of each fund's money, by amount | SF5 |
| 8 | Window length | one year | not applicable |
| 9 | Boundary inclusivity | 1 January to 31 December 2025, inclusive | C1: no expenditure dated on a boundary moves the call (asserted) |
| 10 | Rounding path | transactions converted and summed unrounded, totals reported to one decimal | figures checked mid-bin by the generator |
| 11 | Tie-break | none needed | the third leads the fourth by 1.25x |
| 12 | Maturity and censoring | the 2025 year closed and fully reported by the pull | axis 4 |
| 13 | Order of operations | convert each transaction, credit it, sum by country | C1: crediting before or after conversion gives the same totals (asserted) |
| 14 | Row order | none | not applicable |
| 15 | Duplicate resolution | the funds' grant activities in both the XML files and the Datastore counted once; a payment and its receipt are not spending | SF2, SF9; asserted |
| 16 | Identity normalisation | funders by IATI identifier through the member register; every spending activity names its funder by the funder's current identifier | asserted |
| 17 | Netting against gross | expenditure gross; no refunds in 2025 | asserted |
| 18 | Dimensional units | nine currencies to US dollars through the exchange table | SF6 |
| 19 | Code and status semantics | IATI transaction types: 1 incoming funds, 2 commitment, 3 disbursement, 4 expenditure; only 4 is spending | the codelists; the methodology note |
| 20 | Integerisation | none on the call | not applicable |
| 21 | Clause scope | the methodology note governs "money spent"; the council paper sets the call; each ask's wording governs its figure | stated once each |
| 22 | Forward window contents | the call opens offices for 2027 on the closed 2025 year | retrospective reason: the council paper takes the latest complete year of spending, the members' 2027 grants not yet being made |

## Literal reader

Executed word for word, the methodology note fixes one quantity per country: the 2025 expenditure there by the organisations that spent it, of money that came from the members directly or through one or more pooled funds, in US dollars at the value date. For spending a pooled fund paid for, "money that came from the members" is their part of the money the fund paid out; each fund's dated receipts and payments show what it held when it paid (the global fund's 2024 collection, the Sahel fund's January 2025 round, the global fund's part of that round carrying the global fund's mix), and every attribution of a commingled fund's payments (first in first out, last in first out, pro rata of the balance) gives the same shares. Every literal reading gives Rwanda, Kenya and Mali; the wrong threes come from easy methods on the same literal quantity (the year's contribution share, the share of every contribution, the receipts before each payment), never from another reading.

## Oracles

None. No shipped figure states a fund's member share, a fund's balance or the members' money spent in any country: the member register carries no amounts, the council paper names no country, the funds' files carry only their own receipts and payments (which tie under every handling), and the two distractors (country health indicators, office running costs) are on other bases.

## Ask sheet

**Ask A: the members' money spent in each country in 2025 (construction).** Figures: 13, millions of US dollars to one decimal. H18 home: the evidence the call is read from, every candidate. Use: the council sees every country's figure beside the three. Construction: the golden's, so the cracker keeps it and the mirror keeps only Kenya (no pooled money there). Device: none; Layer 1 hazards (a currency left to the activity default at two implementers off the boundary, multi-country percentages) move only these figures (asserted per item). Path: the Datastore extract, both funds' files, the exchange table, the member register, the methodology note.

**Ask B: commitments not yet paid at 30 June 2026.** Figures: for each country, the money the members had committed to activities there but not yet paid at 30 June 2026, at that day's exchange rates (13, millions of US dollars to one decimal). H18 home: a measure every candidate carries that the call does not turn on (the money still to reach each country). Use: the council paper asks for the pipeline beside the spending. Primary device: D2, a superseded publication that looks final: in 2024 one member moved its IATI identifier from the IATI-assigned one to its national registry number and republished every activity under new identifiers, and its old dataset was never withdrawn, so the Datastore still holds the old copies (last updated 14 June 2024) with their 2023 commitments and their disbursements to June 2024; the member works in all 13 countries, so in every country the old copy adds its unpaid commitment again. Split evidence: the member register gives both identifiers; each new activity carries its old identifier as an other-identifier (previous activity identifier); the old copies stop in June 2024. Silent: different activity identifiers and titles, so the battery's key, exact-duplicate and join checks pass. Hazards: multi-country activities' percentages (seen); a cancelled activity whose commitment is reversed by a negative commitment (seen); commitments and payments in different currencies, all at 30 June 2026 rates; transactions dated after 30 June 2026 in the extract (seen). Path: the Datastore extract, the member register, the exchange table, the codelists (four files, about eleven columns). Stops: the old copies counted (every figure high), the golden. Realism: publishers that change identifier republish under the new one and often leave the old dataset registered, and the Datastore keeps whatever is registered.

**Ask C: organisations the members paid directly in 2025.** Figures: for each country, how many organisations the members paid directly for work there in 2025 (13 whole numbers). H18 home: a measure every candidate carries (the organisations an office would coordinate). Use: the council paper asks for each country's partner count. Primary device: D1, the same records under two key schemes: one member cites the organisations it pays by their national registry numbers and another by the identifiers the organisations publish under, and the organisations' registered names differ from their published names, so in every country at least one organisation paid by two members appears under two identifiers and two names; only the IATI Registry's publisher list, which gives each publisher's other identifiers, joins them. Hazards: the same organisation paid by two members under one identifier (seen); names differing in case and spacing (seen); an organisation paid for a two-country activity counted in each (by the ask's "for work there"). Path: the Datastore extract, the registry publisher list, the member register (three files, about eight columns). Stops: identifiers counted (every figure high), the golden. Realism: funders record a grantee by whichever identifier their grants system holds, and IATI's own guidance lets an organisation publish under one identifier and list others.

Main population zero-counts (asserted): the main call reads the implementers' 2025 expenditure and the two funds' receipts and payments; it reads no commitment, no member payment, no old-copy activity and no receiver identifier. Deleting the old copies and putting every receiver under one identifier moves no main figure; the two device asks share no device file.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| B, 13 figures | counts the old copies' commitments beside the new ones: every country's figure high by the old copy's unpaid commitment | miss |
| C, 13 counts | counts distinct receiver identifiers: every country high by the organisations paid under two identifiers | miss |

Mirror leakage: 2.6 per cent (the mirror, stopping at R0 or R1, keeps Ask A's Kenya figure, the one country with no pooled money, and makes the cracker's errors on B and C).

Pair ceiling: 38.4 (planning weights 38 / 7 / 55 with r = 5; the cracker keeps the main block and Ask A, 13 of 39 ask figures: 38 + 7 + 55 x 13/39 = 63.3; the mirror keeps r, instruction-following and Kenya: 5 + 7 + 55 x 1/39 = 13.4; (63.3 + 13.4) / 2 = 38.4).

Criteria: the call (three countries), the two funds' member shares (critical components), 13 Ask A figures, 13 Ask B figures, 13 Ask C counts, about three chart criteria and two files, about 47 before the generated rubric selects.

## Tried and rejected
- 2026-10-13, draw: the draft's vote at the council (vote_or_meeting) and a ranked list under a cap (shape 01). Rejected: task255 holds the forcing event and task256 the shape in the window; the host-country agreements and leases force the decision (purchase_order_or_contract) and the answer is built as a bridge from the members' own records to the money spent (shape 03).
- 2026-10-13, draw: attribution at a transition (G4) as the decisive generator. Rejected: task450 v2 holds the pattern in the window; the members' money is provided elsewhere, through the funds (G5).
- 2026-10-13, design: the second fund layer (the global fund's money inside the Sahel fund) as the decisive step. Rejected: the transfer is a provider-receiver join the solver already holds the key to (screen test 2), and the estimand's "one or more pooled funds" files it, so a careful solver lands it; the prototype also moved the three only at fifth place. It stays on the default path, and the decisive step moved to the money each fund held when it paid (G6).
- 2026-10-13, design: shape 03 (a bridge between totals). Rejected: a bridge from the members' payments to the money spent walks the solver through the funds' timing and hands over the decisive step; the answer is a register of 13 countries with three measures (shape other).
- 2026-10-13, design: a payer-and-receiver reconciliation ask keyed on year-end receipt dates. Rejected: an ask about money crossing the year end points at the funds' timing; the asks carry identity and version devices instead.
- 2026-10-13, design: a shared decisive pool for both funds (one share window for both). Rejected: a single window lets a lag heuristic land; the global fund pays out a year late and the Sahel fund the same year, so only the money each fund held when it paid lands both.
