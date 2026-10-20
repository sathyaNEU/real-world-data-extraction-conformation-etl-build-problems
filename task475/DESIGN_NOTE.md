# task475 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 1, drawn 2026-10-20 from seed ET32.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task475.json` (architecture v1), registered 2026-10-20 after a pull. Guard
  WARN on `overuse.objective` only (ETL in 7 of the last 12 builds): the lane is ETL by assignment, so the objective is
  not a free axis here. Nearest driver on file task268 v1 at 0.10 (people present in small areas from a commuting
  table), which shares no latent structure with this one.
- **Redrawn at the draw, and why the replacements are the honester labels.** The sibling's re-registration of task474
  put `filed_standard` and `budget_or_appropriation` into the three-build window, and the first card's signature (gap
  population, G6, allocation) repeats five older builds. Gap moved to `objective`, which is the truer gap: the credit
  claims count in the IRS tables is correct and complete, and the allocation is scored on a different count, the claims
  with children. Gate G moved to `etl_conformance`: the decisive step derives the policy's field from fields the source
  does carry. The forcing event is the council's 2027 weatherization plan filed with the state (`statutory_or_regulatory_filing`),
  and the context artifact is the program's program year 2025 close-out summary the program director works from, which the asks
  build on. `government_agency` and `nonprofit_or_charity` are banned in the window, so the deciding body is a regional
  council of governments (`local_government`), which administers weatherization for its member counties.
- **Seed:** ET32 (a state energy office splits a fixed weatherization fund across counties in proportion to tax returns
  claiming the earned income credit, capped at 12 per cent, from IRS ZIP-code tables taken to counties through the
  HUD crosswalk; the capital county's share jumped). Kept: the world (a public body, a fixed weatherization fund, the
  IRS ZIP-code tables, the ZIP-to-county relationship file, a seat county), the decision (the capped proportional split)
  and the quantity (earned income credit claims by county, narrowed to claims with qualifying children). The seed's
  mechanisms (the crosswalk's direction, its ratio type, the other-ZIP-codes line) are not the stump: the policy files
  the direction and the residential ratio, and each is Layer 1 the analyst executes.
- **Pairing:** Demographic & Social Science (house domain, income and poverty statistics from tax returns; card
  subdomain `income-poverty-inequality`) sitting in Survey Research & Official Statistics, task type
  `census-register-administrative-data-quality`, which serves ETL. The work is official statistics from an
  administrative source: the IRS ZIP-code tables for two tax years in two layouts, conformed through the residential
  ZIP-to-county file into the county table the council's allocation policy defines, with one field the source does
  not carry and has to be derived. Objective: Data Extraction & Conformation (ETL).
- **The decision and the quantity:** the council's allocation policy splits the 2027 weatherization fund across its
  fourteen member counties in proportion to each county's tax-year 2023 returns claiming the federal earned income
  credit with at least one qualifying child (the latest year the IRS has published at the plan date), filed from
  residential addresses in the county; no county receives more than 12 per cent, the excess shared in proportion among
  the rest. Forward facing: the 2027 program year has not opened and the plan is due to the state on 15 November
  2026, before the subgrantee contracts are signed.
- **Shape:** `05`, an allocation to a fixed total: fourteen counties times three figures (returns with qualifying
  children, share, allocation: 42), the cap decision and the largest county (2), a chart with its parts (4), the files
  (2), and two asks over the program's last closed year, program year 2025 (28): the criteria come from the
  structure, none stacked.
- **Strategy:** `decomposition_attribution`: the decisive move splits each county's credit claims in the lowest AGI
  class into childless workers and families by their paired credit amount. `composition_mix` names the shortcut's
  failure (the statewide mix applied everywhere) rather than the move, and it is banned in the current window; the
  move is the split, so the decomposition label is the honest one. Gate G `etl_conformance`; gap `objective`, then
  `population`; pattern none, generators G6 (composition shift: each county's own mix of families and childless
  workers), G2 (ZIP code against county), G19 (the policy's county table); Layer 2 family `estimation_fit`, pattern
  `own:mixture recovered from a count and its paired amount by known per-kind averages`.
- **Data-native sentence:** the earned income credit pays a childless worker at most about six hundred dollars and
  phases it out below about twenty-five thousand of income, while a family's credit runs to several thousand, so the
  lowest AGI class is the only one where both kinds claim, and a county's credit amount in that class divided by its
  claims is a weighted average of the two kinds' averages that fixes its own share of families; the seat county, with
  a university and the region's hospitals and many young single workers, has far more childless claimants than the
  state, so the statewide share overstates its families.
- **Sources, one line each:** seed ET32 (the world, the decision and the quantity, never its mechanisms); the client's
  census-register patterns (net against gross classification error, dual-system estimates) for the task type's
  register-quality ground, neither used; strategies F6 composition rows (the statewide mix applied to every unit is the
  shortcut); the slot search on mixtures and paired amounts (task124's main kinds, task198's allowed amounts at a rate
  plateau: a price level, not a composition), none of which recovers a composition from a count and its amount.
- **Same-puzzle test:** gap objective, decisive generator G6, decision allocation_to_total against the last twelve
  builds, lineage included: no match. Same-driver test (gap objective, G6, etl_conformance): no match.
- **Abstraction test:** the nearest drivers stripped of nouns (task268's people present carried by commuting flows,
  task190's space-time pairs, task253's voucher split by response rates) carry no count and paired amount fixing a
  composition; none maps onto this driver.

## Default path

A strong analyst with every field read correctly:

1. Reads the allocation policy: tax-year 2023 returns claiming the earned income credit with at least one qualifying
   child, filed from residential addresses in each member county; the 12 per cent cap with the excess shared in
   proportion among the rest until no county exceeds it.
2. Conforms the IRS ZIP-code table for tax year 2023 to counties through the ZIP-to-county relationship file's
   residential ratio (the policy's direction and ratio), drops the state total and other-ZIP-codes lines, sums the
   credit claims by county and AGI class.
3. Finds that no table at ZIP or county level splits the claims by qualifying children; takes the Department of
   Revenue's statewide table of claims by AGI class and number of qualifying children, and applies the statewide share
   of claims with children in each AGI class to every county's claims in that class (all but a handful of claims above
   the lowest class are families, so the share matters in the lowest class).
4. Shares the fund in proportion and applies the cap.

**Ends on:** Tallis County, the seat, at the 12 per cent cap ($2,400,000), its excess shared among the other thirteen
counties (Tallis 15.46 per cent of the families before the cap).

**Golden:** no county reaches the cap; Tallis County receives $2,292,000 (11.46 per cent), and every county's
allocation moves by $1,892 to $107,993 against the default path.

## Stump sentence

The default path applies the statewide share of claimants with children in each AGI class to every county's credit
claims and caps the seat county at 12 per cent, because it never asks what each county's own credit amounts say about
its mix of families and childless workers; Tallis County's claims in the lowest class average far less than the
state's, which only a childless share well above the state's can produce, so its families fall below the cap.

## Three rules

Task type: census-register-administrative-data-quality (Survey Research & Official Statistics, the client domain the house domain demographic-social-science maps to): county statistics built from an administrative register's ZIP-code aggregates, the ZIP-to-county relationship file and the Department of Revenue's statewide credit statistics, conformed to the council's county table, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each member county's number of working families with children claiming the earned income credit, which tax-policy and income statistics read from the credit's own schedule: a childless worker's credit tops out near six hundred dollars and ends below about twenty-five thousand of income, a family's runs to several thousand, so in the lowest AGI class a county's claims count and credit amount fix how many of its claimants are families, the estimator being the two-kind decomposition by the statewide average credit of each kind in the class.

Swap: "which hospital wards get the new beds, in proportion to the patients with private cover, from each ward's admissions and total charges" keeps a count and an amount but loses the mechanism: no schedule fixes what each kind of patient is charged, so a ward's charges say nothing reliable about its mix, and the decomposition the call turns on does not exist.

Layer 1: the IRS ZIP-code tables in two tax years with a changed column layout (written by the IRS's two releases), amounts in thousands of dollars, AGI classes coded 1 to 6, a state total line and an other-ZIP-codes line; the ZIP-to-county relationship file's four ratios with a county-to-ZIP file beside it (the State Geographic Information Office's two products); four P.O. Box ZIP codes with no residential addresses; the Department of Revenue's statewide statistics as tables inside its annual report PDF; each is the systems as they publish, nothing is placed to be caught, each is executed from a filed sentence or the source's own documentation, and checks.py R2a to R2f mishandle each and keep the call.

Layer 2: estimation_fit, a two-kind mixture recovered from a count and its paired amount: the policy's count of claims with children is never published below the state, and the choice that flips the call is estimating each county's families from its own claims and credit amount instead of carrying the state's share of families to every county.

Decisive step: recovering each county's claims with children in the lowest AGI class from the class's claims count and credit amount, by the statewide average credit of a childless claim and of a family claim in that class, so that a county whose average credit sits low has more childless claimants than the state, instead of applying the statewide share of families to every county's claims.

Not semantics: every field, unit and definition read correctly (the policy's "at least one qualifying child", amounts in thousands, the AGI class codes, the residential ratio, the state and other-ZIP lines, the Department's table by number of children) still leaves the easy route applying the statewide share of families in each class, because no field says that the county's amount carries its own mix; the step is an estimation the analyst chooses, not a reading.

Not rule application: the policy fixes the population, the tax year, the residence rule, the cap and its sharing, and no rule or procedure says how to obtain a county's claims with children from tables that never split them; executing every filed rule with the statewide share files Tallis County at the cap, so the step no rule performs is using each county's credit amount to fix its own mix.

Analyst test: a strong analyst who conforms the ZIP tables to counties correctly, reads the basis correctly and applies the Department's statewide share of claims with children in each AGI class caps Tallis County at 12 per cent ($2,400,000) and shares its excess (the default path's Ends on); the decomposition by each county's own credit amount leaves Tallis County below the cap and moves every allocation; checks.py will run both on the clean truth.

Estimand: the council's weatherization allocation policy (filed in the pack): the population (tax-year 2023 federal returns claiming the earned income credit with at least one qualifying child, filed from residential addresses in a member county), the outcome (each county's count of such returns), the unit (returns; allocations in dollars), the window (tax year 2023, the latest the IRS has published at the plan date) and the comparison (each county's share of the fourteen counties' total, capped at 12 per cent with the excess shared in proportion until no county exceeds it).

No decoy: nothing is planted: the IRS tables, the relationship files and the Department's statistics are the sources' own publications, and the policy states the basis without a method; no memo, earlier allocation, staff draft, briefing or stakeholder figure ranks the counties or carries a statewide-share estimate.

No certified replay: no certified or published county count of claims with children ships, so nothing is recovered by reproducing a number; the method comes from the credit's schedule and each county's own count and amount.

Lesson: when a published total of mixed kinds comes with its paired amount and the kinds carry known, very different average amounts, the area's own count and amount fix its mix, and a region-wide share discards exactly the local information the amount carries; no build on file recovers a composition from a count and its amount (task124 splits mains by kind from the era, task198 reads a price level from allowed amounts).

## Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| R0 all credit claims | the IRS table's claims count read as the policy's basis, the policy's "with at least one qualifying child" skipped | readable |
| Layer 1: the residential ratio, the P.O. Box fallback, the other-ZIP and state lines | the policy's residence sentence and the IRS file's own line descriptions | readable |
| R1 the statewide share of families in each AGI class | the Department of Revenue's statewide table by AGI class and number of qualifying children, the only table that splits claims by children | readable |
| R2 (decisive) each county's families recovered from its own lowest-class claims count and credit amount | nothing: no sentence says an amount carries a mix, the Department's report gives counts and amounts without comparing kinds, and the IRS dictionary describes the amount as the credit claimed | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "with at least one qualifying child" | returns claiming the credit for one or more children | every credit claim | Tallis capped (R0) | the policy's basis sentence names the children |
| SF2 | tax year | 2023, the latest the IRS has published at the plan date | 2022 (last year's file) | moves every share | the policy names the latest published tax year; the 2022 file's header says 2022 |
| SF3 | a ZIP code's returns to counties | the relationship file's residential ratio | total ratio; the county-to-ZIP file | small moves, same cap decision | the policy's residence sentence names residential addresses and the ZIP-to-county direction |
| SF4 | a ZIP code with no residential addresses | its total ratio | dropped | same call | the policy's fallback sentence |
| SF5 | the IRS other-ZIP-codes and state-total lines | not county returns | spread over counties | same call | the policy: returns the tables place in no ZIP code count for no county |
| SF6 | member counties | the fourteen named in the policy's schedule | every county a ZIP code touches | same call | the policy's schedule; shares are of the fourteen counties' total |
| SF7 | amounts | thousands of dollars in the IRS file and in the Department's tables | read as dollars | the split fails visibly (every county's first-class count negative) | the dictionary's field list and the report's own note |
| SF8 | AGI classes | IRS classes 1 to 6 as the dictionary lists them | none | same call | the dictionary's class list |
| SF9 | families in classes 2 to 6 | every claim there is a family's (the Department's table shows no childless claims above the first class) | the statewide share applied there too | same call (share is 1.000) | the Department's table |
| SF10 | the decomposition's grain | ZIP cell then county, or county then decomposition | either | same figures (every cell's share of returns with children between 0.263 and 0.971, none clipped) | records converge (asserted) |
| SF11 | averages for the decomposition | the first class's childless and family averages ($394.88 and $4,723.49) | the family average pooled over all classes | all 14 allocations move by $331 to $7,698, same cap decision | applied to the IRS state line, the class averages return the Department's 162,495 first-class returns with children and the pooled average 181,434 |
| SF12 | the cap | 12 per cent of the fund, the excess shared in proportion among the rest, repeated until none exceeds it | one pass | same call (no county reaches it in the golden) | the policy's cap sentence |
| SF13 | rounding | counts and shares carried unrounded, each allocation rounded to the nearest $100 | counts rounded to one decimal first; shares rounded to two decimals first | counts first: same allocations; shares first: 13 allocations move | the policy's rounding sentence |
| SF14 | the fund | $20,000,000, the 2027 program year, shared whole | net of administration | every allocation | the prompt's fund; the policy shares "the fund" with no deduction |

## Ladder

Built values from the cut pack (generator/checks.py L1 to L8). Tallis County is the seat.

| Rung | Route | Tallis share | Cap | Tallis allocation |
|---|---|---|---|---|
| R0 | all credit claims by county | 16.54 per cent | binds | $2,400,000 |
| R1 (default path) | statewide share of families in each AGI class | 15.46 per cent | binds | $2,400,000 |
| R1c | the first class's credit amount over the family average alone | 12.10 per cent | binds | $2,400,000 |
| R1b | the decomposition with the family average pooled over every class | 11.50 per cent | none | $2,299,700 |
| Golden | the decomposition by the first class's childless and family averages | 11.46 per cent | none | $2,292,000 |

- Dominance: the golden and R1 differ in every county's allocation by $1,892 to $107,993, Tallis by $107,993; R1b
  differs from the golden by $331 to $7,698 per county, outside every $100 bin; every wrong route misses all 14.
- The second-largest county sits between 9.48 and 9.68 per cent under every route, so the cap decision turns on Tallis
  alone.
- Separation: no rung prints a golden figure; R0, R1 and R1c cap Tallis; the golden leaves it 0.54 points under the
  cap; on the clean truth the true count of families puts Tallis at 10.59 per cent (R3a).

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | tax-year 2023 federal returns claiming the credit with at least one qualifying child, residents of the fourteen member counties | filed in the policy (SF1, SF6) |
| 2 | Unit of account | returns; allocations in dollars | filed |
| 3 | Attribution window | tax year 2023 | filed (SF2) |
| 4 | As-of dating | the IRS file as published; the relationship file of the fourth quarter of 2023 | filed in the policy |
| 5 | Version basis | the published tables; nothing is restated | C1 |
| 6 | Denominator | the fourteen counties' total of families | filed |
| 7 | Weighting | each county's estimated families | filed outcome; the estimate is the decisive step |
| 8 | Window length | one tax year | filed |
| 9 | Boundary inclusivity | AGI classes as the IRS defines them | dictionary |
| 10 | Rounding path | unrounded counts, allocations to $100 | filed (SF13) |
| 11 | Tie-break | none arises (no two counties share a figure) | C1, asserted |
| 12 | Maturity and censoring | none: the tax year is closed and published | C1 |
| 13 | Order of operations | residence shares, then classes, then the cap | filed; the decomposition commutes with the residence shares (SF10) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | one row per ZIP code and AGI class | C1 |
| 16 | Identity normalisation | ZIP codes as five-digit text, county FIPS codes | dictionary |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | thousands in the IRS file, dollars in the Department's table | headers (SF7) |
| 19 | Code and status semantics | AGI class codes, the other-ZIP and state lines, P.O. Box ZIP codes | dictionary and policy; never the stump |
| 20 | Integerisation | allocations to $100 | filed |
| 21 | Clause scope | the cap applies to every county including those taking shared excess | filed (SF12) |
| 22 | Forward window contents | the 2027 program year funded from the tax-year 2023 count | filed: the latest published year |

## Literal reader

The policy executed word for word fixes the population, the tax year, the residence rule, the cap and the rounding;
it is silent on how to count a county's claims with children from tables that never split them, and the two methods
a literal reader can reach differ: the statewide share (R1) contradicts each county's published credit amount, and
the decomposition reproduces it, so the records rule R1 out; every other reading converges or violates a quoted
sentence (fork table). Re-run on the finished pack at stage 3.

## Oracles

- The IRS file's state-total line against the sum of its ZIP lines: ties under every handling (the other-ZIP line
  included), so it confirms the conformance and arbitrates nothing about families (O1).
- The Department's statewide table against the IRS state line: the same 414,067 credit returns and the same 304,367
  in the first class (O2); applied to the state line, the class averages return the Department's 162,495 first-class
  returns with children exactly, the pooled average 181,434 (SF11). It carries no county figure.
- Each county's published credit amount in the first AGI class: the only check the families estimate has, satisfied
  by the decomposition and contradicted by the statewide share, which implies first-class amounts 13.8 per cent
  under to 49.2 per cent over the counties' own (Tallis +49.2 per cent, O3).
- No control ties only under the golden on the asks: the close-out carries program-wide spending by category and
  fund and the agencies' intake (jobs opened, audits), which tie under every handling of the ask devices (B10).

## Ask sheet

- **Ask A, the dwellings the program weatherized in each county in program year 2025 (fourteen figures, whole
  dwellings).** H18 home: what each county delivered with the money the board is about to allocate again, set beside
  each allocation in the board paper (policy 6.1). Path: the job export (job, agency, county entered, dwelling tract,
  building type, units, funding, status, completion), the job status history (job, status, changed, user, note), the
  member and agency lists, the policy, the close-out, the dictionary.
  Primary device: D8, an anchor on the current record, not the first. Policy 6.1 counts each dwelling in the year its
  job was first completed; a job reopened for a callback is marked complete again when the callback closes, the
  export's COMPLETED_DATE is the latest, and the first completion is only in the status history (275 jobs completed
  twice or more; every county has jobs whose first and latest completions straddle the year, A9). Nothing in the
  export marks a re-completed job.
  Hazards: H1 the county entered (Tallis-Hesketh Community Action enters Tallis on its 253 Hesketh jobs, while the
  tract places the dwelling); H2 utility-only jobs kept in the same system (counted, all 14 move); multifamily units
  (jobs counted, all 14 move); deferred and cancelled jobs.
- **Ask B, the program's spending on dwellings in each county in program year 2025 (fourteen figures, whole
  dollars).** H18 home: the money each county's dwellings absorbed, the board's second figure beside each allocation.
  Path: the grants ledger (line, posted, agency, invoice, job number, account, fund, service date, amount), the job
  export, the status history's conversion notes, the close-out's convention (posted in the year, at the amount
  posted, lines charged to jobs), the dictionary.
  Primary device: D7, the true key elsewhere. The agencies invoiced 2025 under their previous system's job numbers;
  the January 2026 conversion loaded the old jobs in their old order under the WX system's numbers, so every 2025 line
  matches some job as written (none unmatched), the county totals stay plausible (0.71 to 1.66 times the true, B9),
  and only the line's agency and dates disagree with the job it lands on (5,729 of 7,302 lines); the old numbers live
  only in the history's MOVED conversion notes.
  Hazards: H1 (the county entered); the service date in place of the posting date (all 14 move); only lines on
  completed jobs (all 14 move); administration lines with no job.
- **The construction layer:** the call, the fourteen counts, shares and allocations, and the chart; the cracker has
  them.
- **Main population zero-counts (asserted):** the call reads no job, history, ledger or close-out file; with each of
  them removed the fourteen allocations are unchanged (S1), and the asks read no IRS, relationship or Department file
  (S2).
- **Hazard table (asserted):** A2 to A8 and B2 to B6 in checks.py; none moves the call.
- **Referee:** none; no file states a dwelling or spending total by county or by agency.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, dwellings weatherized by county | counts units of program jobs whose export completion date falls in the year, by the dwelling's tract; keeps 0 of 14 | miss |
| B, spending on dwellings by county | sums ledger lines posted in the year with a job number, joins the number to the export as written, by the job's tract; keeps 0 of 14 | miss |

- Mirror leakage: 0.0 per cent of ask weight on the cut pack (generator/ceiling.py: the mirror builds both asks the
  cracker's way and keeps none of 28).
- Pair ceiling: 31.0 on the cut pack (weights 38 / 7 / 55: the cracker keeps the main block and instructions, 45.0;
  the best mirror off the call keeps the cap decision through the pooled average and instructions, 17.0); re-measured
  by the stage 4 readers and from the generated rubric at ship.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

- **The 10/10 rules re-read against the built pack.** Domain: the deciding quantity is each member county's count of
  credit returns with qualifying children, recovered in the lowest AGI class from the class's claims and credit
  amount by the credit schedule's two very different average credits (childless $394.88, families $4,723.49 statewide);
  a noun swap leaves no schedule and nothing for the amount to say. Layers: the mess (two IRS layouts, thousands, the
  state and small-ZIP lines, the P.O. Box ZIP codes, the relationship file's ratios and its reverse twin, the
  Department's tables inside a PDF) is the publishers' own and keeps the call when mishandled (R2a to R2f). Three
  rules: no decoy, memo, ranking or county figure ships (R3c); no field reading decides (every field read correctly,
  the statewide share still caps Tallis, R3a); no filed rule says how to count a county's returns with children.
- **Free gates (2026-10-20):** checks.py 0 failed (input gates, dates, pins, SF1 to SF14, L1 to L8, O1 to O3, R1 to
  R3c, S1 and S2, A1 to A12, B1 to B10, E1 to E4, F1 to F6), verify.py 71 of 71 independently, two builds
  byte-identical, target.zip cut from the final build (14 files), figures_check.py 130 of 130, precut.py 51 checks
  clean, voice-check PASS, guard.py heart WARN on objective overuse only (nearest driver 0.06), surface no personas,
  containers clean, generator/ceiling.py pair ceiling 31.0 with mirror leakage 0.0.
- **leak.py REVIEW lines, each harmless:** 131, 114, 129, 135 and 200 appear only inside larger numbers (dollar
  amounts in the close-out and the Department's tables, an income class bound in the dictionary); the policy and the
  dictionary carry the call's words because they define the allocation and the files it is made from; the policy,
  the close-out and the dictionary use the plain words amount, residential, published, agency and close-out in their
  own sense, and none names the decomposition, the conversion's renumbering or the callbacks' effect on the
  completion date.

## Tried and rejected

- The seed's own mechanisms as the decisive step (2026-10-20, screened at the draw): the crosswalk's direction, its
  ratio type and the other-ZIP-codes line each flip only on reading a file or a field correctly, so each is data
  semantics; all three stay in the pack as Layer 1 under filed sentences.
- Apportioning split ZIP codes by a better weight than residential addresses (2026-10-20, screened): a crossing
  partition split by an indicator whose ratio to the target differs within the coarse unit, which task474's first
  architecture spent at stage 4 (a reader landed it) and task476's first architecture carried to a SEND_BACK.
- Suppressed small cells recovered against the state total (2026-10-20, screened): task465 recorded the same stump
  sitting in Layer 1, and task201 found disclosure bounds reduce to interval arithmetic with no estimation choice.
- Late-filed returns completed from processing-year files, and two administrative lists for the families' true count
  (2026-10-20, screened): maturity and capture strategies, both banned in the current window and spent in this lane.
- A LEGACY_JOB_NO column in the job export as ask B's antidote (2026-10-20, stage 3, before any reader): a pack that
  names the renumbering hands the join to every careful solver (proven-in-production, 76 v1); the old numbers moved
  into the conversion notes of the status history.
- The close-out's jobs and spending by agency (2026-10-20, stage 3): agency totals tie only under the right join and
  the right completion date, a control tying only under the golden; the close-out now reports program-wide spending by
  category and fund and the agencies' intake, which tie under every handling.
- Agency-blocked renumbering at the conversion (2026-10-20, stage 3): the raw join piled the year's spending into the
  last two agencies' counties (one county at 2.4 times its true figure), loud enough to send any solver looking; the
  conversion now loads the old jobs in their old order.
- Program years from July to June (2026-10-20, stage 3): the asked year had not closed at the pull; program years are
  calendar years and the asks read the last closed one, 2025.
