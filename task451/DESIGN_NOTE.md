# task451 design note

Architecture 1 (drawn 2026-10-13, wave 2, oviya1301).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task451.json`, registered 2026-10-13 (guard PASS).
- **Slot:** seed ET08 (analytical_tasks/07_data_extraction_conformation, header and Situation only): a consortium of donors and the organisations they fund publish to IATI, and the board opens three country coordination offices in the countries where the most of its money is spent. The world, the decision and the quantity are kept; the pitfall is re-found from the data under the 10/10 rules.
- **Pairing:** Survey Research & Official Statistics / census-register-administrative-data-quality / Data Extraction & Conformation (ETL). Aid statistics are compiled from administrative reports (the publishers' own IATI records), and the official compilers' method for money that passes through pooled funds is the imputed flow: an intermediary's spending in a country credited to its funders in proportion to what each gave it. The ETL objective: several publishers' activity files in two layouts, currencies, value dates and the delivery chain's double reporting conformed into one table of the members' money by the country it was spent in.
- **Shape:** 03, a bridge between totals: for each leading country, the bridge from the members' own recorded payments to the money of theirs spent there (the pooled funds' share, the implementers' pass-through, the payments counted twice), with the three countries the call.
- **Strategy:** decomposition_attribution. The money spent in a country is decomposed by whose money it was, through every layer of the funding network.
- **World:** a London-based donor collaborative of foundations and development agencies funding maternal and newborn health in East Africa, the Sahel and South Asia. Its members fund implementing NGOs directly (project grants with a country), and through two pooled funds run by an intermediary: a global maternal health fund and a regional fund for the Sahel that takes part of its money from the global fund. Non-member donors also give to both funds. Every member, both funds and the larger NGOs publish to IATI. The collaborative's council decides in December 2026 where to open three country coordination offices; the host-country agreements and office leases are signed in the first quarter of 2027.
- **Forum and forcing event:** council_or_assembly (the members' council), purchase_order_or_contract (the host-country agreements and leases). Organisation foundation_or_funder, role research_desk (the secretariat's head of data and learning). Personas from `guard.py names --geo "United Kingdom" --seed 451`: Lesley Hunter, Lee Sykes, Gail Dobson, Kieran Patel.
- **Data-native sentence:** the members put a large share of their money into the two pooled funds, whose contributions carry no country, and the regional fund draws part of its money from the global fund, so the countries where the members' money is spent only show once each fund's spending is credited back to its funders in proportion to what each gave, through both layers.
- **Sources, one line each:**
  - `stumping/references/client/two-layer-task-design.md`, decomposition (the quantity split by its true source): the country spending split by whose money it was.
  - `stumping/references/strategies.md` Part 6 (every reflex lands wrong): the members' own payments by country and the one-layer share each file a named wrong three.
  - `dataset-generation/references/layer1-messiness.md` (layouts changing, currencies inherited, the same event reported twice): the Layer 1 here, none of it on the decisive step.
- **Same-puzzle and abstraction:** the decisive generator G5 (provision elsewhere) and Gate G decomposition_attribution clear the window; the nearest drivers sit at 0.05 to 0.08 (task181 v1 lineage, task101, task57 lineage): none credits spending through layers of intermediaries to the original funders.

## Default path

1. Read the members' own 2025 transactions from their IATI activity files, convert each to US dollars at its value date with the collaborative's exchange table, and keep the disbursements and expenditures.
2. Total them by the recipient country recorded on the member's activity (multi-country activities by their percentages); contributions to the two pooled funds carry no country and drop out.
3. Rank the countries and take the top three.

Ends on: the wrong three countries (fixed at design).
Golden: the three countries where the most of the members' money was spent in 2025, each implementer's 2025 spending credited to the members by the members' share of the money it received, a pooled fund's share being pro rata of its contributions and a contribution from the other fund carrying that fund's own share (fixed at design).

## Stump sentence

The default path opens the offices in the wrong three countries because step 2 places the members' money where their own payment records put it, so their contributions to the two pooled funds, which carry no country, drop out and the countries the funds spend in are left short; followed to the organisations that spent it and credited back through both funds' layers, a different three lead (countries fixed at design).

## Three rules

Task type: Survey Research & Official Statistics / census-register-administrative-data-quality, serving the ETL objective (the publishers' IATI records in two layouts conformed into the members' money by country, the funding chain's double reporting resolved).
Domain test: the deciding quantity is the members' money spent in each country, which aid statistics compile as an imputed flow: each intermediary's spending credited to its funders by their share of its pooled contributions, carried through every layer of the delivery chain; with a retailer's nouns there are no pooled funds of commingled contributions, no delivery chain reported by each link and no imputed shares, so the task stops reading.
Swap: put a hospital system in ("which three regions get care coordinators, by where the system's money is spent") and there are no pooled multi-donor funds, no non-member co-funders and no chain of publishers each reporting the same money, so the call no longer reads.
Layer 1: the publishers' activity files in IATI XML and the Datastore's flattened CSV with differing layouts; transactions in several currencies, some inheriting the activity's default currency, converted at their value dates; the same payment reported by the payer and the receiver at different dates; commitments, payments, receipts and expenditures in one file; parent programmes reporting budgets over child projects that report transactions; multi-country activities with percentages; organisation identifiers under current and legacy prefixes, some receivers named without one. All of it is what IATI publishers' systems write; none is placed to be caught.
Layer 2: allocation_constraints (decomposition by source): the money spent in a country is counted where it is spent and credited to the members in proportion to their part of the money that paid for it, through both pooled funds.
Decisive step: crediting each implementer's 2025 country spending to the members through the funding chain, the pooled funds' shares solved pro rata through both layers; nothing filed names an imputed share, a pooled fund's member share or the chain.
Not semantics: every field read right (each currency converted at its value date, each transaction type kept or dropped correctly, each organisation identified) still leaves the members' money in the pooled funds without a country, and the members' own payment records or a one-layer share rank the wrong three.
Not rule application: the collaborative's methodology files the WHAT (the members' money spent in each country in 2025, in US dollars at the value date) and no rule says how money through a pooled fund is credited; executing every filed rule leaves the step open, and the default path executes every one of them.
Analyst test: a strong analyst who converts every currency at its value date, keeps payments and expenditures, removes the receipts that repeat a payment and sums the members' 2025 payments by recipient country, or credits each pooled fund's spending by the members' direct share of its contributions alone, opens the offices in the wrong three countries (fixed at design).
Estimand: the collaborative's methodology note: the members' money spent in a country in a year is the spending in that country, by the organisations that spent it, of money that came from the members, in US dollars at each transaction's value date; members' money is the members' own and the share of any pooled money the members provided.
No decoy: no document, dashboard extract or stakeholder carries a ranking of the countries; the members' annual reports state their own totals, which tie under every handling.
No certified replay: nothing published is reproduced; the members' annual reports total their own payments, not where the money was spent.
Lesson: money passed through pooled funds is spent where the funds spend it and belongs to their funders in proportion, through every layer; reading the donors' own records or one layer down misplaces it; no build on file teaches it.

## Tried and rejected
- 2026-10-13, draw: the draft's vote at the council (vote_or_meeting) and a ranked list under a cap (shape 01). Rejected: task255 holds the forcing event and task256 the shape in the window; the host-country agreements and leases force the decision (purchase_order_or_contract) and the answer is built as a bridge from the members' own records to the money spent (shape 03).
- 2026-10-13, draw: attribution at a transition (G4) as the decisive generator. Rejected: task450 v2 holds the pattern in the window; the members' money is provided elsewhere, through the funds (G5).
