# task264 design note

Architecture 2, re-rooted 2026-10-17 (wave 3, Descriptive lane, sathay3012), after architecture 1's determinism SEND_BACK (`## Tried and rejected`). Seed DA14's world is spent with architecture 1; this draw takes a new world. The Daskbeck Valley Regional Park Authority, a statutory joint body funded by a levy on its nine member councils, sets its 2027-28 levy at its members' budget meeting in January 2027. By the members' resolution of July 2026 the levy is apportioned among the member councils in proportion to the number of each council's residents aged 16 and over who visited at least one of the Authority's six parks in the 2025-26 survey year (1 April 2025 to 31 March 2026), each resident counted once however often they came, as estimated from the Authority's visitor survey. Every file predates the build; the call (a levy for a year not yet begun) faces forward, and the quantity it rests on is the closed 2025-26 survey year because the resolution fixes that year.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task264.json`, architecture v2, registered 2026-10-17; architecture 1 is in its lineage with its fate. The Authority is a joint body of councils (`local_government`); its members decide the levy at the budget meeting (`committee_or_panel`, `budget_or_appropriation`); the requester is the Authority's head of finance (`finance_controller`); the context artifact is Appendix B of the levy papers, the 2026-27 levy as apportioned by population (`close_out_summary`), and the members' resolution is the governing document; no calibration organ. `guard.py check`: WARN only. `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection against task235 and task465, five of the last twelve): the label is shared, the mechanisms are not (task235 a tracking loss conditioned on a delivery chance, task465 a fused two-trait count; here a person count from a visit sample). `test.same_driver_older` is differentiated on the card against task131 v1 (a randomised lift read at the parent unit), and the card also differentiates task452 (design weights from strata drawn before a map revision) and task253 (a count as a sum of probabilities under shrinkage).
2. Pairing: Survey Research & Official Statistics (client domain) / sample-design-allocation-weighting / Descriptive & Distribution Analysis. The task type's own object, the estimator a probability sample's design implies, decides the call; the setting is a regional park authority's funding formula.
3. Niche: an on-site exit survey run by a contractor at the six parks on sampled days, stratified by park, season and weekday or weekend; at the survey point the interviewer approaches every eighth adult leaving (adults in a group each eligible, each answering for themselves); about four and a half thousand interviews; each records the respondent's home town or village, age band and how many times in the last 12 months, including that day, they visited any of the Authority's parks. The contractor's weights expand each interview to the adult visits it represents in its stratum. Residents of the three valley councils walk, run and take dogs into the parks every week or every day; residents of the six outer councils come a few times a year.
4. Call and shape: each member council's 2027-28 levy (`allocation_to_total`, question form how much). Shape 05 (allocation to a fixed total): nine councils, each with its estimated adult residents who visited and its levy, the valley councils' combined share, and the change from the 2026-27 population basis as context only.
5. Gate G `method_or_model_selection`, strategy key `population_selection` (the sample is selected in proportion to how often each person visits), decisive generator G10 (one person stands behind many sampled visits), then G14 (a respondent mix conditioned on being in the park on a sampled day).
6. Data-native sentence: an exit survey meets people as they leave, so a resident who walks the dog in Brathden Woods every morning passes the survey point about two hundred times a year and a resident of an outer council who comes twice passes it twice; the interviews, expanded by the survey's weights, are a sample of visits in which every adult appears in proportion to their own visit count, and the resolution counts people.
7. Sources, one line each:
   - The two-layer design reference's `estimation_fit` family (weighting and post-stratification; estimation that fits the data): the estimator of a person total from a sample of visits weights each interview by its design weight over the person's own visit count.
   - The Survey Research library's sample-design patterns (a base weight multiplies every stage's probability; realised cluster sizes break self-weighting; optimal allocation): this build's pattern is `own:visit-intercept-to-person-weights`, the inclusion probability made proportional to frequency by the intercept design itself.
   - task452 (stratified reference points after a map revision): weights by the strata the sample was drawn from; here the weight is set by each person's own visit count, which no stratum carries.
   - task253 (schools past a floor as a sum of probabilities) and task262 (a slope on long-run income from single-year readings) in this lane: noise in a measurement; here the selection itself is proportional to the quantity, and no reading is noisy.
8. People, drawn with `guard.py names --geo "united kingdom" --seed 264`: Claire Foster (the Authority's head of finance, author of the levy papers), Toby Houghton (the survey contractor's project manager, author of the fieldwork and weighting note). Invented names (the Authority, its parks, the nine councils and their settlements, the contractor, the app provider, the card acquirer, the payers and the suppliers) are screened in `checks.py` against the real United Kingdom place, NHS and park names within three edits of any of them (H21: none within two edits or by containment).

## Default path

1. Read the members' resolution: the 2027-28 levy is apportioned in proportion to each member council's residents aged 16 and over who visited at least one of the parks in the 2025-26 survey year, each counted once.
2. Stack the survey's two deliveries; code each respondent's 12-month visit count with the codebook; place each home town or village in a council through the Authority's settlement gazetteer; keep the residents of the nine member councils.
3. Join the contractor's expansion weights and sum them by council: the adult visits each council's residents made in the survey year.
4. Turn each council's visits into residents by dividing them by its respondents' average 12-month visit count (the expansion-weighted mean).
5. Apportion the levy in proportion to those residents.

Ends on: the three valley councils pay 24.9 per cent of the levy between them.
Golden: the three valley councils pay 50.6 per cent of the levy between them.

## Stump sentence

The default path charges the three valley councils 24.9 per cent of the levy instead of 50.6 because it turns each council's expanded visits into residents with its respondents' average 12-month visit count, and in an exit survey that average is visit-weighted (a resident who comes two hundred times is two hundred times as likely to be interviewed), so it overstates how often the valley councils' residents come and undercounts them most; the survey's weight over each respondent's own visit count counts each resident once and gives the golden split.

## Three rules

Task type: sample-design-allocation-weighting (Survey Research & Official Statistics), which serves Descriptive & Distribution Analysis in the taxonomy; the setting is a regional park authority's funding formula.
Domain test: the deciding quantity is a population total, each member council's adult residents who visited at least once in 2025-26, estimated from a probability sample of visits by the design-based estimator that weights every interview by the inverse of its person's inclusion probability, which an exit survey makes proportional to that person's visits; replacing it with the visit total, or with visits over a visit-weighted average frequency, moves every council's levy.
Swap: "how should a hospital trust's patient-experience budget be split among its nine clinics by the patients each saw" keeps an exit survey and a split, but loses the intercept design that draws each adult in proportion to how often they come, the expansion strata of park, season and day type and the 12-month visit count that set each person's chance of selection, so the estimator the call turns on has nothing to attach to and the task no longer reads the same.
Layer 1: the survey in two contractor deliveries (a spring and summer workbook and an autumn and winter CSV from the contractor's new tablet system) with renamed columns, parks as names in one and site codes in the other, dates as Excel dates and as DD/MM/YYYY text, recoded age bands and interview numbers written three ways (DV25-1-0001, DV25/2/0001 and the weights file's 1-0001); the contractor's expansion weights in a separate file; home areas coded by the contractor, with NK where no home was given or it could not be placed; 12-month visit counts heaped at round numbers as people give them; and, off the main path, pay-machine payments and counter hours stamped in UTC across British Summer Time, the parking app's statements by month and tariff, and the finance system's cash book carrying both its posting date and the bank's value date. All of it is how the contractor's and the Authority's systems hold their records, and nothing is placed to be caught.
Layer 2: the estimation_fit family; a person total estimated from a sample of visits needs each sampled person weighted by the inverse of their own inclusion probability (the design weight over their visit count), because the exit survey's selection is proportional to how often each person comes.
Decisive step: weighting each interview by its expansion weight divided by the respondent's own 12-month visit count, so each resident counts once, instead of apportioning by expanded visits or dividing each council's visits by its respondents' average visit count.
Not semantics: every field and document read correctly (the resolution's residents counted once, the weights' adult visits, the visit-count question, the gazetteer) still leaves the analyst choosing how to turn visits into residents, and the natural conversion, visits over the respondents' average visits, is a size-biased average; no field, code or definition says how a sample of visits becomes a count of people.
Not rule application: the resolution fixes what is counted (residents aged 16 and over of each member council who visited at least once in the survey year, each once) and the contractor's note fixes how interviews were drawn and weighted; no filed rule says how to estimate a count of people from them, so executing every stated rule still files the default path's split.
Analyst test: a strong analyst who codes every answer, places every respondent, reads the resolution correctly and expands the interviews by the contractor's weights divides each council's visits by its respondents' average visit count and charges the valley councils 24.9 per cent (Ends on: the three valley councils pay 24.9 per cent of the levy between them); weighting each interview by its weight over its own visit count charges them 50.6.
Estimand: the members' resolution of July 2026 (in the Authority's levy papers) fixes the population (residents aged 16 and over of each of the nine member councils who visited at least one of the Authority's six parks between 1 April 2025 and 31 March 2026, whether or not the survey met them), the outcome (the number of such residents, each counted once), the unit (the member council) and the comparison (each council's levy in proportion to its number).
No decoy: nothing is planted; no memo, draft, briefing or stakeholder figure argues a split, the old population basis is the 2026-27 levy as invoiced, and the survey is the Authority's routine visitor survey.
No certified replay: the method is not recovered by reproducing published or certified figures; no file publishes a resident count, a share or a split on the new basis.
Lesson: an on-site intercept survey samples visits, so each person's chance of selection rises with how often they come, and a count of people weights each respondent by the inverse of their own visit count; the respondents' average visit count is a visit-weighted average that overstates frequency, so dividing visits by it undercounts the most frequent visitors; no build on file teaches frequency-proportional selection.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 respondents read as residents (interviews counted by home council) | the resolution's "each resident counted once" and the note's "weights expand each interview" kill it | the home-area column | counting rows is the first move | none | none | none | readable |
| R1 the survey's weights summed by council (adult visits) | the resolution counts residents, not visits | the weight column | expanding by the survey's weights | none | none | none | readable |
| R2 each council's visits over its respondents' average visit count (the default path) | no sentence names a conversion; the resolution's "however often they visited" asks for one | the visit-count column | dividing a total by an average per head | none | none | one ratio per council | readable |
| R3 each interview's inverse visit count, unweighted | the note says each interview's weight is its stratum's adult visits over its stratum's interviews | the weights file | weighting by the survey's weights | none | none | none | readable |
| (decisive) each interview's expansion weight over its own visit count | none: the note describes how visits were drawn and weighted; no document speaks of how often a person comes or of counting people from visits | the visit count is one of sixteen survey columns and is what the default path averages | expand, average and reweight land R1, R2 or R3 | no published resident count or share | keys unique, joins one to one, nothing for the battery to find | a weighted sum of ratios, no ratio of reported figures | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | member councils | the nine councils in the levy papers' schedule | every council a respondent names | other councils' residents counted | the resolution's "member councils" and the schedule's nine |
| SF2 | residents | residents aged 16 and over, the survey's own population | residents of all ages (children in parties) | counts not estimable from the survey | the resolution's "aged 16 and over" |
| SF3 | visited | at least one visit to any of the six parks in the survey year | the number of visits | the R1 split | the resolution's "each resident counted once however many times they visited" |
| SF4 | survey year | 1 April 2025 to 31 March 2026 | calendar 2025 | other interviews | the resolution's paragraph 3 |
| SF5 | however many parks | one person across the six parks | one person per park | parks' counts summed, people counted twice | the resolution's "however many parks they visited" and Q9's "any of the Authority's parks" |
| SF6 | as estimated from the survey | the contractor's expansion weights as delivered | weights rebuilt from the counters | a different estimate | the resolution's "as estimated from the Authority's visitor survey" and the note's statement that the delivered weights are the survey's |
| SF7 | a respondent's visits | Q9, visits to any of the parks in the 12 months to the interview, that day included | visits in the survey year | not recorded | same call: Q9 is the survey's only measure (asserted: no other visit field) |
| SF8 | home not placed (NK) | not counted | shared out pro rata | same call | same call: pro rata keeps every share (asserted) |
| SF9 | residents outside the member councils (OUT) | not counted | counted in a tenth share | the levy spread over a non-payer | the resolution's paragraph 6 |
| SF10 | the levy requirement | 7,416,300 pounds | the 2026-27 levy | every amount moves | the levy papers' budget table |
| SF11 | rounding path | each council's levy rounded to the pound from its unrounded share | shares rounded first | pounds move | the resolution's paragraph 5 |
| SF12 | one person interviewed twice | each interview counted as drawn | interviews merged by guesswork | no identifier links interviews | same call: the note's selection rule and no person identifier (asserted: interview numbers unique) |
| SF13 | adults in a group | each interview is one adult answering for themselves | weighting by party size | counts move | the note: every adult in a group eligible, each answering for themselves |

## Ladder

Built from the shipped pack (asserted in `checks.py`, recomputed by `verify.py`). The levy requirement is 7,416,300 pounds; shares are each council's estimate over the nine councils' total.

| Rung | Construction | Valley share | What kills it |
|---|---|---|---|
| R0 | interviews counted by home council | 86.3 | the resolution counts residents once; the note says interviews are drawn from visits and weighted |
| R1 | the survey's weights summed by council (adult visits) | 85.1 | the resolution counts residents, not visits |
| R2 (default) | each council's weighted visits over its respondents' weighted average visit count | 24.9 | the respondents' average is visit-weighted: an exit survey draws each person in proportion to their visits, so it overstates every council's frequency, most where frequent and occasional visitors mix |
| R3 | each interview's inverse visit count, without the weights | 53.4 | the weights: interviews per visit run 2.4 times higher in the quiet strata, where the valley's regulars walk |
| Golden | each interview's expansion weight over its own visit count, summed by council | 50.6 | none |

Position and separation: every rung names a different split; the nearest wrong rung (R3) differs from the golden by 9,287 pounds or more for every council (Ferncote the closest), the default path by 484,137 pounds or more for each valley council. Dominance: the default path's error (25.7 points of valley share) is nine times the nearest wrong rung's (2.8). The decisive move reverses the over-correction: R1 to R2 swings the valley share from 85 to 25 and the golden sits between, so no half-applied correction lands on it (R3 is the only rung within ten points, and it needs the weights dropped).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | residents 16+ of the nine councils who visited at least once in the survey year, met by the survey or not | filed: the resolution, paragraph 2 |
| 2 Unit of account | the resident, each once | filed: the resolution |
| 3 Attribution window | the survey year | filed; C1: every interview inside it, none on an edge |
| 4 As-of dating | home as given at the interview, coded by the contractor | filed: the wave notes and the codebook |
| 5 Version basis | the contractor's two deliveries as delivered | C1: one version of each, no superseded file |
| 6 Denominator | the nine councils' estimates summed | filed: the resolution's "in proportion" |
| 7 Weighting | the survey's expansion weight times each interview's inverse visit count | the design forces it (the decisive step); C4 against R1, R2, R3 |
| 8 Window length | Q9's 12 months | same call: the survey's only measure |
| 9 Boundary inclusivity | 31 March 2026 inclusive | C1: no interview on 31 March or 1 April |
| 10 Rounding path | unrounded shares, each levy rounded to the pound | filed: the resolution, paragraph 5 |
| 11 Tie-break | none arises | C1: no two councils' estimates tie (asserted) |
| 12 Maturity and censoring | the survey year is closed; Q9 complete for every interview | C1 |
| 13 Order of operations | weight times inverse visits per interview, summed by council | C1: the sum commutes (asserted over shuffled rows) |
| 14 Row order | none | C1: asserted over permutations |
| 15 Duplicate resolution | interview numbers unique in each wave and in the weights | C1: asserted |
| 16 Identity normalisation | three interview-number formats, one mapping | C4: every interview joins one to one (asserted) |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | weights in adult visits, Q9 in visits | C1: one unit each |
| 19 Code and status semantics | the area codes (nine councils, OUT, NK) | dictionary: the codebook |
| 20 Integerisation | the levy in whole pounds | filed: the resolution; the rounded amounts' total stated beside the requirement |
| 21 Clause scope | the resolution from 2027-28 | filed: paragraph 1 |
| 22 Forward window contents | the 2027-28 levy on the closed 2025-26 survey year | filed: paragraph 3 |

## Literal reader

Executed word for word, the resolution counts each member council's residents aged 16 and over who visited at least once in the survey year, whether or not the survey met them, as estimated from the visitor survey; the contractor's note says each interview was drawn from the adults leaving on a sampled day and weighted to its stratum's adult visits; the one estimate of a count of people those files support weights each interview by its expansion weight over the respondent's own visit count, which gives the golden, and every other reading violates a quoted sentence (R1 the resolution's "each resident counted once", R2 the same sentence executed on a sample whose draw the note states, R3 the note's weights) or converges (SF7, SF8, SF12).

## Oracles

- The contractor's stratum estimates of adult visits tie to the expanded visits under every handling (they are the weights' numerators) and say nothing about people: no oracle.
- The 2026-27 levy schedule in the levy papers is on the old population basis, a different basis filed as superseded by the resolution; it ranks nothing on the new basis.
- No file states a resident count, a share or a split on the new basis.
- Ask referees (each arbitrates its own device and ties under every handling elsewhere): the parking tariff table (Ask A, the app statements' VAT basis), the councils' remittance advices (Ask B, the shared service's transfers), the pay-machine transactions (Ask C, the moved counter's site before October).

## Ask sheet

Asks are decoupled from the call: none reads the survey, the weights or the resolution, and the main population (the 4,470 interviews, their weights and the resolution) carries zero device rows (asserted: the call computes from the three survey files with every ask file deleted).

**Ask A. What parkers paid at each charging park's car parks for 2025-26 parking, through the pay machines and the parking app, net of VAT (four figures).**
- H18 home: the car-park income line that offsets the levy requirement in the budget (the levy papers' car parking charges), reconciled to the parking systems.
- Use: the levy report's car parks section.
- Path: pay-machine transactions (machine, ticket number, paid at, tariff code, amount, method), the asset register (machine to car park), the app provider's statement lines (month, location code, tariff, sessions, parking income, commission, net payable), the tariff table (charge by car park and season, and its notes): four files, fifteen columns.
- Primary device D3, units set per source: the app statement's parking income is stated net of VAT (sessions times charge over 1.2 on every line) while the machines record what was paid; the tariff notes say charges include VAT, so the natural read takes VAT off both and every park comes out low by its app income over six. Hazards: D1, three machines (Gorthfield, Water Park, Thruscote) re-sent four to six days' tickets with a later night's upload under fresh transaction numbers, machine and ticket number kept, so no row is an exact duplicate; D2, PM-2103 stood in Gorthfield's main car park until it replaced PM-2203 at the Water Park on 1 September 2025, and the register holds its current site, so its spring and summer takings, at Gorthfield's charges, follow it.
- Stops (built): natural read (VAT off the app income too, every row, register sites) misses all four by 31,934 to 59,983 pounds; VAT off the app income with the replays dropped misses all four; the app as stated, every row, register sites misses three (Gorthfield 21,821 low, Water Park 23,478 high, Thruscote 1,197 high); the app as stated with the replays dropped misses two (Gorthfield and the Water Park by 22,391); the answer.
- Realism: app providers state parking income net of VAT; machines re-send stored tickets after a back-office restore; machines move between car parks and asset registers hold the current site.

**Ask B. Each member council's payments toward its 2025-26 levy by 31 March 2026 and what it still owed that day (eighteen figures).**
- H18 home: the collection position of the levy the call replaces, the audit trail the report carries.
- Use: the levy report's collection section.
- Path: the 2025-26 levy invoices (four instalments each, the fourth due 31 March 2026), the cash book export of the bank receipts (date, value date, type, payer, reference, amount), the remittance advices held (the shared finance service's and Larkstead's): three files, fourteen columns.
- Primary device D8, a clock against a filed cutoff: the finance system posts each credit from the next morning's bank statement, so every receipt's date column is the working day after its value date; the fourth instalments, all paid on their due date, 31 March 2026, were credited that day and posted on 1 April, so the date column puts all nine outside the year; the export manifest says what each date is (the posting from the morning's statement, the bank's credit) and nothing says which one answers "paid by". Hazards: D7, Hornmere and Wendstow's shared finance service paid both councils' second, third and fourth instalments in single transfers quoting Hornmere's invoice, divided only by its remittance advices; D5, six councils' 2024-25 fourth instalments, credited 31 March 2025, sit at the export's start under invoices the 2025-26 list does not hold. Chaldale's third instalment, paid at its 2024-25 amount, is a genuine arrear of 3,455 pounds, not a device.
- Stops (built): natural read (date column, reference match) misses all eighteen; the date column with the shared transfers split by the advices misses all eighteen; value dates with the shared transfers credited to the invoice quoted misses four (Hornmere paid 1,580,812 and owed minus 616,024, Wendstow paid 205,341 and owed 616,024); value dates with the shared transfers halved misses four (53,784 each way); the answer.
- Realism: finance systems post the morning's bank statement with the bank's value dates; councils pay a year-end instalment on its due date; shared services pay for their partner councils in one run and send the advice; a payment run left at the previous year's instalment.

**Ask C. How many vehicles entered each charging park's car parks in 2025-26 (four figures).**
- H18 home: the car-park counts the survey's stratum estimates of adult visits rest on (the field note), the audit trail of the weights' frame.
- Use: the levy report's car parks section.
- Path: the hourly car-park counts (counter, hour in UTC, vehicles) and the asset register (counter to car park, model, installed and removed dates), with the pay-machine transactions as the cross-check: three files, ten columns.
- Devices, one per park: D6 at the Water Park, the BX-2 loop installed 18 August 2025 counts every pass, in and out (its counts per paying vehicle run at twice its predecessor's); D1 at Gorthfield, the old lakeside logger C-05 kept reading the entrance's loop beside its replacement C-10 from 3 to 24 February 2026, the same count hour by hour; D2 at Lockshaw Moor and Thruscote Hall, C-07 counted at Thruscote Hall until it moved to Lockshaw's valley car park on 14 October 2025 (the day C-08 there was removed and C-11 installed at Thruscote), and the register shows its current site.
- Stops (built): natural read (register sites, every row, counts as reported) misses all four (Gorthfield 2,564 high, Water Park 74,246 high, Lockshaw 80,078 high, Thruscote 80,078 low); the BX-2 counts halved misses three; halved and one counter per car park and hour misses Thruscote; halved with C-07 placed misses Gorthfield; the answer.
- Realism: replacement counters with another detection mode, an old logger left on the loop while its replacement is commissioned, a counter moved and re-registered in place.

Main population zero-counts: device rows in the interviews, the weights, the gazetteer and the levy papers: 0 (asserted: the call computes from the survey files alone with every ask file deleted, and no survey or weights column names a machine, counter, invoice or bank field).

| Hazard | Asks moved | Per-ask delta (built) |
|---|---|---|
| D3 app VAT basis | A | every park low by its app income over six (32,368 to 55,412 pounds) |
| D1 machine replays | A | Gorthfield 570, Water Park 1,087 and Thruscote 1,197 pounds high |
| D2 machine moved | A | Gorthfield 22,391 low, Water Park 22,391 high |
| D8 posting date | B | every council's fourth instalment, all eighteen figures |
| D7 shared transfers | B | Hornmere 616,024 high in payments, Wendstow 616,024 low |
| D5 prior-year receipts | B | only under a payer-name match: six councils high by their 2024-25 fourth instalment |
| D6 passes counted | C | Water Park 74,246 high |
| D1 parallel loggers | C | Gorthfield 2,564 high |
| D2 moved counter | C | Lockshaw 80,078 high, Thruscote 80,078 low |

Referee: each ask's own (the tariff table and the app lines' sessions for A, the remittance advices for B, the machine payments for C); none ties only under the golden.

| Ask figure | Cracker (lands the call, runs the battery, executes the tariff note) |
|---|---|
| A, each of four parks | miss |
| B, paid by each of nine councils | miss |
| B, owed by each of nine councils | miss |
| C, each of four parks | miss |

Mirror leakage: 0 per cent of ask weight (the mirror stops at R2 on the call and takes the same natural reads on the asks; `checks.py` asserts the cracker's path hits no ask figure).
Pair ceiling: 29.0 (cracker 45 on the call and instruction-following plus 0 of 55 on the asks, mirror 5 plus 7 plus 0; to be rerun on the generated rubric).

## Build record

- **World.** About 419,000 adults visited in the survey year: the three valley councils' residents split between regulars (dog walkers, runners and daily walkers, 12 to 400 visits) and occasional visitors, the outer councils' and outside visitors' a few visits each, each person's visits spread over parks, seasons and day types by their own favourites (world.py). The exit survey draws every interview from the stratum's visits with equal chance, on 29 sampled days a park, each shift completing what the flow and the interviewer allow; the contractor's stratum estimates of adult visits carry three per cent of frame error and are rounded to ten.
- **Pack.** 19 files in three formats: the two survey deliveries (2,349 and 2,121 interviews), the weights, the codebook, the gazetteer, the field note and the levy papers on the main path; the pay-machine transactions (246,404 rows), the app statements, the tariffs, the asset register, the hourly counts (53,063 rows), the levy invoices, the cash book, the remittance advices on the asks' paths; three distractors (annual permits, county population estimates, supplier payment runs) and the export manifest.
- **Gates.** checks.py 105 assertions (the three rules on the clean truth, the ladder and its separation, every SF row, the closure moves, the golden against the truth, the asks' devices and stops, the cracker sheet, separation, the distractors' deletion test, input gates, realism, H21, the containers); verify.py PASS on its own code path (csv and openpyxl, no pandas), finding the BX-2 loop, the moved counter and the moved machine from the data; two builds byte-identical; figures_check 78 of 78; precut 49 of 49; voice-check PASS; leak.py REVIEW (no LEAK, the levy requirement declared a stated input); producer metadata clean; guard heart WARN (repeat and overuse of the Gate G label, answered at the draw); guard surface promotes task136 at 0.102 on card axes alone (population_selection, method_or_model_selection, a council), differentiated on the card, no shared names or text.
- **Leak REVIEW lines, each harmless.** Sweep 3: the levy papers carry the nine councils' names and "2027-28 levy" because they are the levy papers, with no split on the new basis. Sweep 4: the field note describes the survey and its weights and the resolution states the estimand; neither says how visits become people. Sweep 6: the register, the wave 1 workbook, the field note, the invoices and the population estimates name councils or parks beside numbers, and Appendix B ranks the councils on the 2026-27 population basis the resolution replaces; none ranks them on the 2027-28 question. Sweep 9: the permits' valid-until dates run a year past issue, a validity window.
- **Stage 4, judge r1.** DETERMINISTIC, FIX_NOW (Gate G statistical_rigor, analytical_non_defect; Gate H domain pass, layers pass, decisive step analytical): the call, every residents figure and levy, the parking income and the vehicles reproduced to the pound and the vehicle; its one real fork, the cut-off basis of "paid by 31 March 2026" (value date against posting date, every council's figures flipping), is closed in the records by the manifest's definition of the cash book's two dates rather than in the prompt, so the device stays a reading of the data; its optional pins taken in the files (the tariff notes' VAT rate, the resolution's apportionment arithmetic on each council's number) and the write-up reworded (the 24.9 per cent rival's weighted average named, the moved machine and counter and the in-and-out loop stated as found from the takings and counts, both asserted); the residents' totals left out of the graded blocks, the goldens noting that totals come from the unrounded estimates. No graded figure moved.
- **Stage 4, reader 1.** Q1 none (the resolution states the estimand, the note the weights; no file says how to turn visits into people), Q2 none, Q4 none, Q6 an analytical choice; its realism notes fixed in one pass (`## Tried and rejected`): per-park interview totals, the names' spelling pattern, the remittance senders, the field note's weight-range table. Reader 2 on the fixed pack: Q1 none (the conversion is not announced), Q2 none, Q4 none, Q6 an analytical choice; its notes: the permits' single price (now three permit types), the manifest and the shared service's advices read as tidy but plausible (kept).

## Pre-ship check

- **Rule 1, the domain, on the built pack.** The call is decided by a design-based estimate of a population total: each member council's adult residents who visited, from a probability sample of visits in which each person's inclusion probability is in proportion to their own visits, so each interview is weighted by its design weight over its visit count. No shipped column holds a resident count, a person weight or a share (asserted, R1). With another field's nouns the intercept design, the strata and the 12-month visit count that set each person's chance of selection are gone and the call no longer reads the same.
- **Rule 2, two layers.** Layer 1 on the call's path is how the contractor's and the Authority's systems hold the survey: two deliveries in two layouts, three interview-number formats, a separate weights file, NK and OUT codes, heaped visit counts; each mishandled leaves every levy where it was or fails loudly (asserted, R2). Layer 2 is the estimator: on the clean truth (true visit counts, true stratum visits) the default path files 24.9 per cent for the valley councils against a true 50.4, and the golden estimator 50.6 (R3a, R3b).
- **Rule 3, the decisive step.** No shipped sentence says how a sample of visits becomes a count of people (asserted: the resolution states the estimand, the note the draw and the weights); executing the resolution and the note with the natural conversion (visits over the respondents' average visit count) files 24.9 per cent; nothing planted, copied or withheld carries the answer (R3c).
- **Determinism.** The estimate is exact given the shipped weights (six decimals, agreeing with adult visits over interviews to a fraction of a penny); every council's residents sit at least 7 from a hundred's edge and every levy at least 4 pence inside its pound; the rounded levies add to the requirement; NK pro rata and the shuffled rows change nothing; every ask figure reproduces in the verifier on its own path.

## Tried and rejected

- The seed's reliability as a matched-pair minimum (every pair of weeks sharing a set share of spending): filed literally it is a rule's execution, and left vague it is a fork; dropped at the draw.
- Reliability as the sampling error of each format's index (stores or chains resampled): the decisive move would be the resampling unit, the lesson task260 and task261 already teach in this lane; dropped at the draw.
- Each format's change on items pooled across chains as the decisive step: binary, and its insight (read the change within each seller) is task259's lower rung; kept only as rung 0 and rung 1.
- Linking relaunched packs (a smaller pack under a new code) to price shrinkflation: the link reads an item master's attributes, an identity resolution the record says never held; dropped at the draw.
- Promotions drawn at random by line and week: the four-week ends carried about two points of promotional noise in every category and format, swamping the designed gaps; replaced by each chain's weekly catalogue, one line a category a week in a sixteen-week rotation (a second, eight-week rotation for heavier programmes), so the window's first and last four weeks carry the same specials.
- The promotion calendar started at the window's first week: that week carried a quarter of the usual specials and every change fell by about a point; the calendar now starts twenty weeks before the window.
- Four chains repeating the store's weekly total on each of six to eight department rows: an eightfold over-count shows in any per-store sanity check; they now report two department groups, beside two chains reporting the same groups as a true split.
- First-draft banner and firm names (Pellwick, Penhallow, Varnley, Corbel, Tovell, Hollin, Dunstar, Wenlow, Tallen, Marrin and others) sat within two edits of Australian places; renamed after the H21 screen, figures unchanged.
- Random streams keyed to store codes: giving the July chain a refit re-numbered every later code and reshuffled the world; streams are now keyed by chain, site and segment, and the ladder was refitted once.
- Gaps asked as distances ("how far its change sits from that"): a literal reader could give them unsigned; the ask now says above or below.
- A delivery-log note on the convenience chain's till release beside its first TPR week: the first reader took it for a planted hint; the code list's in-use dates carry the record instead.
- The PC rows before 2 August 2026 left to inference from the data's pattern: the first judge read the code list literally (PC never a special, every share 0.2 to 0.6 points lower); the in-use dates now force the reading.
- The gap ask's rounding path and the continuity ask's window left to the prompt's grammar: the first judge found both open (rounded changes subtracted; each store's own panel weeks); the methodology now files the rounding path and the prompt names the chain's weeks.
- The store sales file described as takings by department: a literal reader sums the four chains' repeated rows; the dictionary now describes the rows as the chain's export lays them out, and the repetition to the cent decides it.
- Architecture 1 (2026-10-17, a grocery scanner price index's 2027 sub-index structure, each line followed at the chain that prices it): spent at stage 4. The first judge found the call deterministic (FIX_NOW on four ask forks); the one re-judge returned SEND_BACK (competing_defensible_answer) because the methodology never said what a product is, so a literal reader priced each line store by store (7 categories) and the golden's line at its chain (10) held only under an unfiled product definition; filing it would have made the decisive step rule application. The world's index-construction choices are all definitional, so the slot re-roots to a new world.
- Architecture 2 draw, partial verification of a laboratory's urine screen-out cut-off (culture only above the cut-off plus a random quality-assurance pull of screened-out specimens): the verified subsample is a gold-standard subsample, the calibration form task465 used in the last three builds (`ban.calibration`); dropped at the draw.
- Architecture 2 draw, a duration distribution read from a stock sample (people in emergency accommodation on a census night, stays weighted by the inverse of their length): the delayed-entry lesson task133 teaches and the truncation family task255 spends in this lane; dropped at the draw.
- Architecture 2 draw, competing exits treated as censoring (a cumulative incidence against one minus Kaplan-Meier): needs right censoring to tempt the survival route, so honestly `maturity_censoring`, banned against task235 in the last three; dropped at the draw.
- Architecture 2 draw, top income shares from tax tabulations by Pareto interpolation inside the band holding the 99th percentile: analytically clean, but no natural decision rests on a top share computed from tabulations by the body that sets it, and the subdomain repeats task262 in this lane; dropped at the draw.
- Architecture 2 draw, respondent-driven sampling weighted by the inverse of each recruit's network size: the design's name hands over its estimator and RDS-I, RDS-II and the successive-sampling estimator compete; dropped at the draw.
- Ask B with every council paid in full by 31 March: all nine owed figures zero, eighteen figures a guess could fill; Chaldale's third instalment, paid at its 2024-25 amount, now leaves a genuine arrear.
- Ask B with Grinbury's first instalment paid twice and the duplicate refunded through accounts payable: with Grinbury's fourth instalment posted on 1 April the duplicate and the missing instalment cancelled to within four pounds under the natural read, so the hazard composed back inside the bin; dropped.
- Ask B with a remittance advice for every payment: the advices alone answered the ask; only the shared finance service's and Larkstead's are held.
- Ask B with only the late-day credits posted next morning: seven of nine councils carried the device and the cracker hit the other two; the cash book now posts every credit from the next morning's statement, one mechanism all year.
- Ask A at the first car-park stream: Lockshaw Moor's income landed exactly on a half pound when the app income is recomputed from sessions; the stream was rekeyed so every park sits a quarter pound or more inside its pound (the survey and the call do not read it).
- Ask A's replays as one re-sent day each: Thruscote's came to 219 pounds, inside a tolerant grader's band; each is now four to six days.
- The app provider and the card acquirer first named Tarnwick and Velbrook, within two edits of Alnwick, Warwick and Kelbrook; renamed after the H21 screen, figures unchanged.
- The first survey world had every shift reach its 30-interview ceiling, so three parks showed 870 interviews and the rest 847 to 857, which the leak reader read as constructed; each shift's completed interviews now vary (mean 25.4, 14 to 32), every park's total differs (732 to 768), and the setting was chosen where the rounded levies add to the requirement and every council's levy sits at least 4 pence inside its pound.
- Expansion weights shipped to four decimals: a solver computing them as adult visits over interviews would have moved two councils' levies across a half pound; the weights now ship to six decimals and agree with that route to a fraction of a penny.
- First-draft names (Kesvham, Tarvstead, Jeskley, Lorvborne, Glevby, Varvcote, Teskfield, Erskden, Cresvley, Corvgarth, Lesvley, Thorvcote, Fenvstead and the villages) shared one spelling pattern the leak reader read as generated; renamed to a varied set screened against the UK reference, each council's random streams keeping its first key so the people did not change.
- A remittance file holding only the shared finance service's and Larkstead's advices read as built for the ask; Grinbury, Ferncote and Ravenwick now send advices with some of their payments, as councils do.
- The field note's table of each park's smallest and largest weight read as an author's aid; it now gives each park's survey days, interviews and estimated adult visits.
- The first judge read "paid by 31 March 2026" two ways (the bank's value date, the cash book's posting date) with nothing in the pack saying what either column was; the manifest now defines both, in the records, while the prompt keeps the plain words so the device is still a reading of the data.
- Residents' totals in the graded blocks: the nine rounded figures add to 271,800 against the unrounded total's 271,900; the totals left the submission and the goldens say how they are formed.
