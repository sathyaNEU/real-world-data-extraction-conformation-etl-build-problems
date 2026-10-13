# Shipped ledger

What has been done: one row per build, one line per dead architecture, and the outcome lessons.
Identity (domain, gap, pattern, driver, lineage) is on the fingerprint card
(`../../fingerprint/cards/taskNN.json`), which `guard.py` bans against. How to find, harden and
protect a stump is in `strategies.md`. This file holds status and what the portal said.

**Keeping it current.** Rewrite a build's row when its status changes (drawn, built, shipped,
re-rooted, retired), and add the portal result with its date the day the author reports it. The
portal record below is the author's list from the portal: an APPROVED build is `SHIPPED & APPROVED
MM-DD`, a PENDING_REVIEW build is `SHIPPED, delivered MM-DD, pending review`, and a build missing
from the list is `FAILED_TO_STUMP: backlog <handle>`, back in its lane owner's backlog wave
(`.claude/authors/`). The parser ranks the three as approved, delivered and failed. When
an architecture dies, move it to Earlier architectures in the same edit: a row describing a dead
version misleads the clone screen. task1 to task24 predate the ledger and have cards only.

**Format (parsed).** `clone-check/fingerprint.py` (`parse_ledger`) reads every line starting with
`|` whose first cell starts with a task number and maps the first ten cells by position: task,
status, domain, objective, gap, pattern, mechanism, calibration, artifact, decision. Later cells
are for readers. `guard.py` reads each task's strongest status through it. Keep the task number
first, no pipe inside a cell, and status words from one class only:

| Means | Status words the parser keys on | Rank |
|---|---|---|
| shipped, or approved before the portal | `delivered`, `approved` | 3, the exclusion |
| in build, open, or built and parked | `built ` (with the space), `rebuilt`, `hardened`, `awaiting`, `drawing`, `contested` | 2 |
| abandoned | `retired`, `failed`, `exhausted` | 1, history |

**Reading a row.** Dates are 2026, written MM-DD. Objective: FC forecasting, RCA root cause, AD
anomaly detection, CEX experiment and causal, DESC descriptive, ETL extraction and conformation,
OPP opportunity sizing, DQ data quality monitoring, `-` a retired tag. Domain: PA product
analytics, SCL supply chain, ECON economics, NPO nonprofit, P&E policy and education, DSS
demographic and social science, BOA business operations, AAF accounting and audit, MCR marketing
and consumer research, BIO biology (retired), EPH epidemiology, ENR energy and utilities, BANK
banking and credit risk, QF quantitative finance, ACT actuarial, HDE health economics, PES
physical and environmental sciences, GSD general statistics, HFE human factors, CJ criminology.
Gap and pattern are the card's, decisive first; calibration and artifact are on the card (`-`).
"Listed" means on the author's refresh lists of 10-02 or 10-07, which state no status. Rows 41 to
43 follow the folders and cards. Author is the lane owner in the root `START_HERE.md`; builds
before the lanes record none (`-`).

## Portal record

The author's portal list, rewritten whole each time they report it. Tasks below 100 are not tracked here.

| Task | Portal id | Portal status | Date |
|---|---|---|---|
| task100 | c25e448d-6679-4580-9b46-5b0850304c3a | APPROVED | 10-06 |
| task101 | 1aa2aa53-5cbb-4103-862a-758cb725d502 | APPROVED | 10-08 |
| task102 | 5a798ae4-0ac3-4254-b895-028eeded4b10 | APPROVED | 10-08 |
| task103 | 079972d3-05c9-4c24-9546-7c87c4c940a8 | APPROVED | 10-05 |
| task104 | 75942cb4-cf82-41c4-865d-229ea22276ea | APPROVED | 10-08 |
| task105 | 0d663732-82bf-4fba-ad56-a67b5074f031 | APPROVED | 10-05 |
| task106 | 16c2111a-934c-4e8a-b1ca-ed2335c9a507 | APPROVED | 10-06 |
| task107 | 17d4e5d9-7fd9-4acf-a2ab-e82de71ae010 | APPROVED | 10-06 |
| task108 | 4d1e2903-6452-45b0-afec-ce7cf3b70e50 | APPROVED | 10-09 |
| task109 | 9d1851a5-99cc-4129-b838-806c7ada966d | APPROVED | 10-09 |
| task110 | 5a548639-10a4-49ba-93b3-3bd5d35b7894 | PENDING_REVIEW | - |
| task111 | 34355e43-f330-4812-91ff-c9e3f37e920a | APPROVED | 10-11 |
| task114 | d01e4abc-d188-424e-a322-c6fe043b29fd | PENDING_REVIEW | - |
| task115 | 6e962c38-379f-4c7a-97c7-7d38e6fed366 | APPROVED | 10-11 |
| task116 | db59e379-425e-474e-9876-f36d07e0f97d | PENDING_REVIEW | - |
| task117 | 261f5aed-b97e-417f-b02d-98f44bb3263c | PENDING_REVIEW | - |
| task119 | 8fee9bfd-50c0-45a8-8f2e-69966ee4d1d8 | PENDING_REVIEW | - |
| task126 | adeccacd-4719-4d23-90c4-a5293c695201 | PENDING_REVIEW | - |
| task132 | 4a42e005-f62d-469b-96cc-8a21e53b1953 | APPROVED | 10-11 |
| task500 | 0e7ed8a4-b426-4c9f-9268-f692031dc597 | PENDING_REVIEW | - |

## Current builds

| Task | Status | Domain | Obj | Gap | Pattern | Stump mechanism | Cal | Art | Decision | Portal result | Author |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | approved | P&E public admin | AD | objective | C | serviceable timeliness against a filed standard | - | - | where one team goes | stump and determinism cleared | - |
| 26 | contested | PA monetisation | - | objective | C | settlement-side witness on fee itemisation | - | - | which programme | none reported | - |
| 27 | approved | ECON public finance | FC | rule | B | recapture netting, gross against net, behind a join | - | - | which of five lapses | stump and determinism cleared | - |
| 28 | approved | ECON labour | AD | objective | C | excess sits in employer-site batch separations | - | - | which cell gets the team | stump and determinism cleared | - |
| 29 | approved | ECON trade | FC | rule | B | realisation slope interacts with the instrument | - | - | which of seven markets | stump and determinism cleared | - |
| 30 | approved | ECON prices | FC | rule population | B, E | conditioned yield on substitution behind a catalogue join | - | - | which item group | stump and determinism cleared | - |
| 31 | failed | SCL sourcing | FC | population | E | censored milestone completion | - | - | how much to resource | failed | - |
| 32 | failed | SCL sourcing | FC | objective | C | quarterly condition inside a residuals instrument | - | - | which volume tier | failed | - |
| 33 | approved | BIO epidemiology | AD | time | A | ongoing level shift against a resolved one | - | - | which signal gets the team | stump and determinism cleared | - |
| 34 | approved | DSS housing | DESC | population | D | weighted household grain against person rows | - | - | structural verdict | stump and determinism cleared | - |
| 35 | approved 08-21, determinism pass | ECON prices | FC | time rule | A, B | adjustment attaches to the endorsement year | - | - | one provision | stump and determinism cleared | - |
| 36 | exhausted 08-21: 7 solves, 4 architectures | SCL transport | RCA | population objective | E, D | supplier agreement answers the largest repair | - | - | which driver | solved 7 times | - |
| 37 | built 08-22, no round recorded | P&E apprenticeship | FC | time population | E | accrual turns on the sponsor's agreement to cohort end | - | - | 2,585 completions | none reported | - |
| 38 | rebuilt 08-21, awaiting round 18 | ECON money and credit | DESC | objective time | C, E, B | concentration removable inside the compliance window | - | - | which of six members | none reported | - |
| 39 | drawing | SCL port and border | ETL | objective rule | none, B | contract grain drops the codes that stop the clock | - | - | one accrual | none reported | - |
| 40 | rebuilt 08-22, awaiting round 3 | ECON regional accounts | ETL | rule population | B | unstated producer test with control-linked firms | - | - | 1,623 k FLN | none reported | - |
| 41 | built 08-22, awaiting round 1 | NPO grant portfolios | ETL | rule time | B | version history loaded as state | - | - | USD 11,279,958.13 | none reported | - |
| 42 | built 08-22, awaiting round 2 | NPO subawards | ETL | rule population | B | resolution rule for a fan-out the solver creates | - | - | USD 6,468,921.99 | none reported | - |
| 43 | built 08-22, re-rooted onto a cap | NPO coaching | CEX | objective population | none, E | bimodal moderator behind a join; mix inverted | - | - | USD 6,749,000 | none reported | - |
| 44 | built 08-24 (v2 cut 4) | SCL slotting | CEX | time population | E | moderator measured on the prior peak | - | - | 66 of 288 items | none reported | - |
| 45 | rebuilt 08-22, awaiting round 3 | SCL service parts | ETL | rule population | B | per-van reorder floor; corpus silent for a reason | - | - | 2,596 units | none reported | - |
| 46 | rebuilt 08-24, awaiting review | SCL chassis | FC | time population | A, E | register age is not service exposure | - | - | 10,000 orders | none reported | - |
| 47 | built 08-24, awaiting round 1 | SCL returns | FC | time population | A, D, B | returns generated per order; baskets doubled | - | - | one parcel volume | none reported | - |
| 48 | rebuilt 08-25 (v2), awaiting round 2 | PA trust and safety | AD | population objective | none | pair ring the category-grain monitor cannot see | - | - | which area | none reported | - |
| 49 | built 08-25, round 1 filed the golden | NPO grantee finance | ETL | population objective | D, C | unpaid cost floored per award, not netted | - | - | USD 6,925,000 | none reported | - |
| 50 (v4) | built 08-27 (listed) | SCL damage claims | RCA | objective time | none, B | true cause is not the fundable cause in the window | - | - | which programme | none reported | - |
| 51 (v5) | built 08-27, awaiting round 1 | ECON tax remittance | ETL | time rule | B | register self-corrects under an unstated review | - | - | $102,491.05 tranche | none reported | - |
| 52 | built 08-26, round 1 not run | PA onboarding | FC | population time | D, A, B | clock at the slowest coach, separate teaching days | - | - | go-live reviews | none reported | - |
| 53 (v2) | rebuilt 08-28 | PA usage billing | DESC | population rule | E, B, C | heavy tail above an adoption break | - | - | which of five categories | none reported | - |
| 54 | drawing 08-28 | SCL cold chain | AD | population time | none | loss per excursion, borne by every pack aboard | - | - | one pack count | none reported | - |
| 55 (v3) | rebuilt 08-28, review repaired 08-29 | SCL code dates | FC | rule time | B, A | shared vat: per-line offset is a mixture | - | - | USD 516,267 | none reported | - |
| 56 (v6) | delivered 08-29 (its notes say shipped) | PA usage billing | ETL | population | E | obeying the billing-grain pin hides a population | - | - | 1,618,907.85 | none reported | - |
| 57 (v23) | built 08-30 | NPO capacity grants | DESC | population objective | D | short-form extract renames fields; a third nulls | - | - | USD 1,470,000 | none reported | - |
| 58 (v15) | built 08-30 (listed) | SCL grain co-op | ETL | objective population | none | nil floor does not commute with the split | - | - | $9,450,518.62 | none reported | - |
| 59 (v2) | rebuilt 08-31 | ECON UI benefits | FC | objective population | B, D | unstated hold on benefit years arising inside | - | - | USD 22,847,893 | none reported | - |
| 60 (v8) | rebuilt 08-31 | P&E CTE credentials | FC | population time | D, B, A | student filed by both districts counted once | - | - | 13,203 | v7 graded 37 and 75 | - |
| 61 | retired 09-01: superseded by task64 | NPO funder collaborative | AD | objective time | G11 | lead recomputed for an unreported year | - | - | which of ~55 members | solved, about 90 to 100 | - |
| 62 (wave 16) | built (listed) | PA seat billing | ETL | time population | A, D | reseller term lapses; schedule reverts | - | - | 51,220 seats | none reported | - |
| 63 | built 08-31 | ECON oil and gas tax | ETL | rule population | B | divisor counts capable wells with no rows | - | - | 2,528,078 bbl | none reported | - |
| 64 (v17) | built (listed) | PA usage billing | FC | objective time | none, B | source quotas bind across the account partition | - | - | $3,111,552.25 | none reported | - |
| 65 (v3) | built (listed) | P&E air permits | DESC | objective population | none | sources built from units at their own parcels | - | - | $1,468,358 | rollout 09-04: valid stump | - |
| 66 | built 09-03 | DSS housing stock | ETL | population objective | B | a dwelling with no meter is served by the parcel's | - | - | 13,745 units | none reported | - |
| 67 (v3) | built (listed) | SCL delivery duties | FC | objective population | none, D | minutes per drop are shares of a sector-day loop | - | - | 31 duties | none reported | - |
| 68 | built (listed) | ECON export statistics | AD | population rule | none, B | matched panel walked through trader successions | - | - | HS chapter 22 | in-house round held 09-05 | - |
| 69 (v4) | built (listed) | PA marketplace | CEX | objective time | C, B | sub-additive slate: a stockout converts once | - | - | 8 of 20, 182 orders | none reported | - |
| 70 (v2) | built (listed) | SCL parcel surcharge | ETL | population objective | none, B, D | reserved trunk pushes acceptance a day | - | - | GBP 16,078.88 | none reported | - |
| 71 | built 09-05 (listed) | SCL DC storage | DESC | rule population | B, E | only some holds stop the clock | - | - | 35 days | none reported | - |
| 72 (v2) | built 09-06, awaiting round 3 | P&E career pathways | RCA | population | D | transferred service books to the origin subaward | - | - | LG-0426 | none reported | - |
| 73 (world 10) | built 09-11 | P&E SNAP recertification | DESC | objective time | none | certification period re-assigned by rule | - | - | which sites | none reported | - |
| 74 (v2) | built 09-06 (listed) | PA assortment metric | ETL | population objective | D, B | a choice certifies across its graded size scale | - | - | 9,928 choices | none reported | - |
| 75 (v2) | built 09-07 (listed) | NPO legal-access slots | FC | population time | C, D | reopened files complete the inflow | - | - | 2,200 slots | review 09-07: valid stump | - |
| 76 (v2) | built 09-07 | DSS victim navigator | AD | population time | E | a household that declined is never engaged again | - | - | 1,474 households | none reported | - |
| 77 (v2) | built 09-07 (listed) | P&E early-learning permits | FC | population time | D, A | count people, not determination rows | - | - | 3,811 permits | none reported | - |
| 78 | built 09-07 (listed) | SCL planned maintenance | FC | rule time | B, D | unfiled span recovered from the settlement | - | - | 3,642 visits | one response at 96 via a leak | - |
| 79 | built 09-08 (listed) | DSS survey release | FC | objective time | none, A | caseload cap makes completes non-linear | - | - | 48,500 addresses | none reported | - |
| 80 (v2) | built 09-08 (listed) | P&E entitlement | ETL | rule population | none | designation dated from the criterion event | - | - | 5,195 students | none reported | - |
| 81 (v3) | built (listed) | ECON employment incentive | DESC | population objective | D | firm identity across reopened register units | - | - | NZD 7,725,800 | none reported | - |
| 82 (v2) | built 09-10 (listed) | PA loyalty merge | ETL | population objective | none | anonymous credits tied back through a second ledger | - | - | 1,298 kits | none reported | - |
| 83 (2.1) | built (listed) | PA save offers | CEX | population objective | E | band effect split by programme history | - | - | 200 sends split | review 09-09: valid stump | - |
| 84 | built 09-10 (listed) | PA paid acquisition | RCA | objective population | none, B | live campaign copies bid against themselves | - | - | 50 pauses | none reported | - |
| 85 (v2.5) | built (listed) | PA bounty partners | AD | time population | B | each member's clock on own pay dates | - | - | none, the hold | v2 rubric 37 | - |
| 86 (v2) | built (listed) | DSS bedroom mix | ETL | time population | none, B | the building opening first takes the list | - | - | 15/20/16/54/19 | none reported | - |
| 87 (v9) | built (listed) | P&E credit recovery | ETL | time population | none | same-period shortfalls hold one place | - | - | 102 seniors | none reported | - |
| 88 | built 09-11 | ECON lodging tax | FC | objective time | none, B | blocks displace guests on compression nights | - | - | $50,900 | none reported | - |
| 89 (v12) | built 09-14 (listed) | NPO stabilisation fund | FC | time | A | self-funded gap rolled to first passage | - | - | USD 330,000 | none reported | - |
| 90 | built (listed) | SCL forklift hire | ETL | population objective | D, B | a Rental persists across unit exchanges | - | - | $275,061 | none reported | - |
| 91 (v2) | built 09-13, awaiting the portal | ECON banknotes | FC | population time | B, A | dormant residue counted by print vintage | - | - | one note order | none reported | - |
| 92 (v4) | built 09-14 (listed) | SCL container terminal | ETL | objective population | C | a place collects only on diary days | - | - | GBP 255,732 | none reported | - |
| 93 (v3) | hardened 10-02 (listed) | ECON wages | DESC | population objective | D, none | flat-rate members owe a per-fortnight shortfall | - | - | 4.7 per cent | none reported | - |
| 94 (v3) | built 10-03 (round 7 pack) (listed) | SCL bulk silo | FC | objective time | C, A | a load on top of two weeks' draw at peak | - | - | 9,669 t | r6: 49, 53, call missed, average over 50 | - |
| 95 | built 09-14 (card only) | ECON output | FC | time population | A | a regime the closed window never reached | - | - | 937,000 m3 | none reported | - |
| 96 | drawing 09-14, data not cut | PA discovery | FC | population time | E | pooled uptake is a mixture by studio overlap | - | - | one bookings count | none reported | - |
| 97 (v5) | built 10-02 (listed) | DSS hardship fund | FC | time population | E, D | renewal depends on the address's grant history | - | - | 60 caseworkers | none reported | - |
| 98 (v7) | hardened 10-04 (listed) | P&E social rental | FC | population time | none | sold renovation dwellings leave once | - | - | 112 short | none reported | - |
| 99 | built 08-17 (spare slot of task31) | SCL sourcing | FC | - | - | characteristic gate read as a category | - | - | which family | none reported | - |
| 100 (v2) | SHIPPED & APPROVED 10-06 | P&E schools equity | ETL | time population | none | census rolled across the year end | - | - | four schools | none reported | - |
| 101 | SHIPPED & APPROVED 10-08 | NPO cold-spot line | DESC | population rule | none, B | own top-ups sit in the baseline | - | - | 12.40 GBP a head | none reported | - |
| 102 | SHIPPED & APPROVED 10-08 | P&E special education | FC | time objective | none | weekend due dates slip a fiscal year | - | - | $50,300,000 | both missed the call, about 50 | - |
| 103 (v4) | SHIPPED & APPROVED 10-05 | NPO food reserve | AD | population time | D | one hamper per household per week | - | - | CAD 279,234 | v3: stumped, still 60+ on the asks | - |
| 104 | SHIPPED & APPROVED 10-08 | DQ alerting | AD | population rule | none, B | least sensitive threshold still paging | - | - | volwatch 3.25 | none reported | - |
| 105 (v5) | SHIPPED & APPROVED 10-05 | DSS lettings | OPP | objective time | C | homes sit on the nearest open branch | - | - | 150 tenancies | v2 stumped (250), asks all filed; v4 solved | - |
| 106 | SHIPPED & APPROVED 10-06 | SCL backhaul | OPP | objective population | none | one corridor's suppliers share return legs | - | - | EUR 370,900 | run 3: both missed, 41 and 70 | - |
| 107 (v4) | SHIPPED & APPROVED 10-06 | NPO power credit | FC | time population | A | intake moves to the experienced rate | - | - | $275,000 | 10-05: stumped, deterministic, about 50 | - |
| 108 | SHIPPED & APPROVED 10-09 | SCL co-pack | FC | rule population | D, B | each requirement counted once | - | - | 12,853 cases | none reported | - |
| 109 (v2) | SHIPPED & APPROVED 10-09 | BOA parcel claims | ETL | population rule | B | two unwritten compilation rules | - | - | promise days | none reported | - |
| 110 | SHIPPED, delivered, pending review | AAF fixed assets | ETL | population rule | B | enhancements ride the host's remaining life | - | - | $951,870 | none reported | - |
| 111 (v2) | SHIPPED & APPROVED 10-11 | BOA field service | RCA | time objective | none, A | which cause still operates forward | - | - | parts and van stock | none reported | - |
| 114 | SHIPPED, delivered, pending review | BOA facilities | DESC | time population | A, D | demand only when two parties share a site | - | - | dial | none reported | - |
| 115 | SHIPPED & APPROVED 10-11 | MCR pricing | FC | time population | D, E | second response only where it undercuts | - | - | which of N | none reported | - |
| 116 | SHIPPED, delivered, pending review | PA monetisation | OPP | population objective | C | value only from one-buyer groups | - | - | slate under cap | none reported | - |
| 117 | SHIPPED, delivered, pending review | SCL sourcing | FC | time population | E, A | draw caps via a dated join | - | - | 110 kW | none reported | - |
| 118 | SHIPPED, delivered 10-12, pending review | MCR media | OPP | objective rule | none, C, B | gain only on volume tests have not banked | - | - | Culture·national at 1,250,000 clicks | redesigned 10-12 (change log to realised holdback lift; asks rebuilt: readers, visits, median minutes; pair ceiling 27.5); judge DETERMINISTIC, two FIX_NOWs fixed | oviya1301 |
| 119 (v2) | SHIPPED, delivered, pending review | P&E mortality review | AD | objective population | C | beds held empty for planned work | - | - | Stennock | none reported | - |
| 120 (v3) | RESHIPPED 10-12 (10/10 rework: retagged OPP, write-up step 3 reworded), pending review | ENR generation capacity planning | OPP | objective | G5, G3 | a day's use is the wells' production less the water the four tanks gained between Eastern midnights, not the largest day of production (none against 184 gpm) | - | - | added firm well capacity, 184 gpm | none reported | sathay3012 |
| 121 (v3) | RETIRED 10-12: third architecture spent (judge SEND_BACK on the re-judge) | PES odor source attribution | RCA | time population | G14 | an odor event's wind set against the same hours on other days, not counted upwind events | - | - | the facility behind the surge | none reported | sathay3012 |
| 122 (v2) | FAILED_TO_STUMP: backlog perssathya | PA experimentation | CEX | time rule | none, B | log keeps only pre-close outcomes | - | - | HC-37 | not submitted | perssathya |
| 123 (v2) | RESHIPPED 10-12 after a portal determinism return (a straddling bill's estimator and Northbank's HHAP count read two ways), pending review | SROS gas calendarization | ETL | time population | none, G4 | a bill's therms split by the measured daily use inside its read interval, not by days | - | - | county grant split, Brennock $2,380,000 to Wynnell $875,000 | re-rooted 10-12; leak reader clean on three reads; judge DETERMINISTIC, one FIX_NOW fixed (HHAP enrolling account), pass 2 APPROVE; portal 10-12 determinism block (C, D, E, competing_defensible_answer), repaired with the utilities' own move-out reads (SF12) and Northbank's account-level enrollment end dates (SF13), no graded figure moved, pass 3 DETERMINISTIC with one write-up FIX_NOW fixed | oviya1301 |
| 124 (v4) | SHIPPED, delivered 10-12, pending review | ENR lead service lines | FC | population | none | verified share inflated by why lines were dug | - | - | zone finish years, last 2037 | none reported | sathya8571 |
| 125 (v2) | SHIPPED, delivered 10-12, pending review | SROS labour survey fieldwork | AD | time population | none | a first-interview visit cap filters employed-heavy households for five quarters | - | - | cap 0.22 of the 0.27 rise; gap 0.37/0.25/0.19/0.07 to Jul-Sep 2027 | none reported | oviya13ya |
| 126 | SHIPPED, delivered, pending review | P&E pendency | DESC | population rule | none, D | a carried file joins two units | - | - | 28.9 months | none reported | - |
| 127 (v2) | SHIPPED, delivered 10-12, pending review | HDHE discharge-to-assess packages | OPP | population objective | C | a package frees only the care wait's excess over the equipment wait running alongside it (Royal Marchford first and Ashby Vale none, 7,160 bed-days, against Ashby Vale first on nights after the ready date, 10,425) | - | - | 508, 350, 120, 222 and 0 packages | none reported | sathay3012 |
| 128 (v3) | SHIPPED, delivered 10-12, pending review | BCF collections overflow | OPP | population objective | none, G5 | a call's effect read only on the over-capacity days' same list, the dialler's skipped records kept with the reached, scaled to a dial and sized on the new team's 400 a day | - | - | no centre gets the 2027 early-stage team; London about 500 rolls a year, 200 short of CP-14's 694 (default path funds London at 2,315) | re-rooted 10-12; leak reader: nothing names the move or ranks the centres, realism fixes applied (field reference column, dated policy line, exact 700 quotient); judge DETERMINISTIC, APPROVE | oviya1301 |
| 129 | FAILED_TO_STUMP: backlog perssathya | BOA service SLA | RCA | population objective | E, D | co-switched causes split by groups | - | - | cause named | none reported | perssathya |
| 130 (v4) | SHIPPED, delivered 10-12, pending review | ACT professional liability pricing | FC | time population | G13, G14 | a claims-made trust's opening window catches only the quick, cheap claims, part-year windows less than pro rata | - | register | trust contribution, $784,000 | none reported | sathya8571 |
| 131 | FAILED_TO_STUMP: backlog perssathya | MCR loyalty | CEX | population objective | none | card lift nets out inside a household | - | - | CHF 972k | none reported | perssathya |
| 132 | SHIPPED & APPROVED 10-11 | ENR asset condition | FC | population time | none | a replacement restarts the wear curve | - | - | 13 lots | none reported | sathya8571 |
| 133 | FAILED_TO_STUMP: backlog sathya8571 | BANK credit loss | FC | time | none | condition the curve on survival to date | - | - | AUD 13,160,000 | r1: one stumped, one at 100 | sathya8571 |
| 134 (v2) | SHIPPED, delivered 10-12, pending review | HDE utilisation | FC | time population | none | inflow hazard peaks after a year | - | - | 760 to 790 residents | none reported | sathya8571 |
| 135 (v2) | SHIPPED, delivered 10-12, pending review | QF volatility | FC | time | none | noon fund prices carry the previous New York close | - | - | 60 per cent growth | none reported | sathya8571 |
| 136 | SHIPPED, delivered 10-12, pending review | ENR load forecasting | FC | population | none | a bulk-buy's installations carry to a new suburb per owner-occupied house still without PV, not per address letterboxed (240 systems in Bindarra Waters against 90) | - | capacity report | YRB24, 1.9 MW over hosting capacity (YRB22 1.5) | none reported (judge DETERMINISTIC, one FIX_NOW fixed, pass 2 APPROVE) | sathya8571 |
| 137 | SHIPPED, delivered 10-12, pending review | BANK deposit behaviour | FC | time population | E | a reached holder's conversation goes to the retention offer on the drop from the deposit's locked rate to the card it reinvests at, not the past campaigns' pooled or per-term share | - | planning thread | 5,500 agent-hours for the January to March 2027 list (1,500, 2,000 and 2,000 by maturity month) | none reported (judge DETERMINISTIC, one FIX_NOW fixed, pass 2 APPROVE) | sathya8571 |
| 138 | SHIPPED, delivered 10-12, pending review | PES irrigation water order | FC | time | none, G16 | every replayed season starts from the depletion each field carries at the end of 31 January (its last 2026 delivered set through the driest October to January on record), not from a full root zone (189,800 acre-feet), each past winter's own state or the replay rule run through 2026 | - | filed standard | the 2027 season order: 202,700 acre-feet, set by the 2012 replay | none reported (judge DETERMINISTIC, APPROVE) | sathya8571 |
| 139 | drawing 10-12: new, wave 2 (seed FC10) | ACT workers' compensation nurse case management | FC | population objective | none, G9 | a randomised pilot read per assigned intake (each arm's indemnity-claim rate times its verified severity) over the place-days an intake holds, not per verified indemnity claim, because the nurses kept part of the strain intakes from ever paying indemnity | gold standard subsample | close-out summary | teams per segment and the AY2027 run-rate saving | none reported | sathya8571 |
| 180 (v4) | SHIPPED, delivered 10-12, pending review | PES induced seismicity monitoring | AD | population time | none | a town network loses small daytime earthquakes to noise | - | - | Pfeilbrunn (Q1 and Q4 2027) | none reported | oviya13ya |
| 181 (v4) | SHIPPED, delivered 10-12, pending review | HFE air traffic control safety | AD | population time | D | losses follow vertical crossings, not flight hours | - | - | Tarvik | none reported | oviya13ya |
| 182 | FAILED_TO_STUMP: backlog oviya13ya | PES groundwater | AD | objective | none | each bore's own lagged driver response | - | - | 4 owners, 5 bores | none reported | oviya13ya |
| 183 | SHIPPED, delivered 10-12, reshipped 10-12 (determinism: the Sutter Park 5 loop's overload and its end filed), pending review | ENR distribution reliability | AD | time population | none | repeat failures concentrate in parts already failed twice | - | - | Quarry Hill 21 | none reported | oviya13ya |
| 184 | SHIPPED, delivered 10-12, pending review | SCL aviation screening operations | AD | objective time | none | host airports stand down their own lanes while the posted unit screens | pilot_log | monitoring_export | Halloran Bay | none reported | oviya13ya |
| 185 | SHIPPED, delivered 10-12, pending review | GSD distribution assessment (weather index pricing) | AD | rule population | none, G16 | a station's instrument change sized at each reading across two count triggers | parallel_run_overlap | filed_standard | $525 a hectare | none reported | oviya13ya |
| 186 | SHIPPED, delivered 10-13, pending review | SROS anomaly detection (fuel price monitoring) | AD | rule time | none, G2 | each unit's change across an event judged against its own changes when nothing happened, under shared local price cycles | - | operations_log | Tallis Petroleum | none reported | oviya13ya |
| 228 (v2) | FAILED_TO_STUMP: backlog perssathya | PES soil moisture | DQ | objective | none | shared input breaks triple collocation | - | - | 8 stations | none reported | perssathya |
| 229 (v2) | FAILED_TO_STUMP: backlog perssathya | GSD missing data | DQ | time population | none | checks record a state before fixing it | - | - | six sites | none reported | perssathya |
| 230 (v2) | SHIPPED, delivered 10-12, pending review | HFE reliability | DQ | time population | A | hit rate falls as targets get rarer | - | - | five streams | none reported | perssathya |
| 253 | SHIPPED, delivered 10-12, pending review | EDU student growth | DESC | population | G11, G17 | a count of schools past a floor is the sum of their probabilities, not a count of shrunken predictions (28 against 42) | - | - | 42 places | none reported | sathay3012 |
| 254 | SHIPPED, delivered 10-12, pending review | URS network analysis | DESC | objective population | G7, G16 | a departure's trip composed segment by segment at the period the shuttle reaches each one, not the sixteen segments summed at the departure period (7:15 against 7:05) | - | - | 7:05 a.m. departure | none reported | sathay3012 |
| 255 | SHIPPED, delivered 10-13, pending review | ACT claims frequency-severity (liability pool retention) | DESC | population | G12, G16 | ground-up severity fitted through the record's own observation process, each occurrence truncated at its deductible and censored at the retention, both at 2027 cost (keep $4.0 million, 0.74 above it), not the recorded costs fitted as complete ($2.0 million) or censored without the floor ($2.5 million) | - | - | keep the first $4,000,000 of each 2027 occurrence | leak reader twice, no decisive-step sentence, realism tells fixed; judge DETERMINISTIC, APPROVE | sathay3012 |
| 445 | SHIPPED, delivered 10-12, pending review | QF 13F ownership | ETL | time population | E | an index sponsor's slice moves with each name's own share count | - | - | 5 of 12 crowded | loop 0 r1 10-11: 52, determinism fail; loop 2 shipped 10-12 | oviya1301 |
| 446 (v2) | SHIPPED, delivered 10-11, kept as shipped by the author 10-12 | BANK watch list | ETL | time population | none | carry error rates, not yield | - | - | 133 groups | left off the portal list (not stumped); the author closed the rework 10-12, no redesign | oviya1301 |
| 447 | SHIPPED, delivered 10-12, pending review | HDE vertical integration | ETL | objective population | C | referral capture follows the patient's tier for the acquirer in the projection year | - | - | proceed at $2.2M | ask layer rebuilt 10-12 (two standing exhibits, pair ceiling 27.5); judge APPROVE | oviya1301 |
| 448 | RESHIPPED 10-12 after a portal determinism return (the recorder file read as complete), pending review | SROS administrative-data coverage | ETL | population | E | a register missing whole lenders completed from a recorder feed whose capture is set by recording route | - | - | recruit Corvane, Weyrauch, Halverd, Mennwell and Arkhaven first (310, 260, 230, 200, 180; Shunga Valley sixth at 150; default path files Shunga Valley fifth) | leak reader clean three times; judge FIX_NOW on Ask B's county basis, pinned, then DETERMINISTIC, APPROVE; portal 10-12 one judge of two NOT_DETERMINISTIC (competing_defensible_answer), repaired with the vendor's coverage sentence, pass 3 DETERMINISTIC | oviya1301 |
| 449 | SHIPPED, delivered 10-12, pending review | GSDS record linkage (complaint desk) | ETL | population | none | a share read through first-of-k account attachments diluted toward the portfolio rate and inverted | - | - | carry 35 dedicated analysts (950 new matters a week after 500 from the posting failure; default path files 40) | leak reader twice, no decisive-step leak, realism tells fixed; judge FIX_NOW on hygiene (an agency export dated after the pull), then DETERMINISTIC, APPROVE | oviya1301 |
| 450 | drawing 10-12 | PES emissions inventory (methane overflights) | ETL | population time | none | a site's yearly mass from intermittent releases read as its mean measured rate over scheduled overflights, not detections booked as releases of assumed length | - | - | which gathering systems to nominate for 2027 low-methane supply | none reported | oviya1301 |
| 500 (v3) | SHIPPED, delivered, pending review | ECON lodging tax | RCA | rule population | B | each change measured by the office's matched-reference method | - | - | long-stay exemption, $3,235k | v1, v2 solved 10-10, 10-11 | sathya8571 |
| 501 (v4) | SHIPPED, delivered 10-12, pending review | EPH measles catch-up | FC | population time | none | a structured population's threshold set by the next-generation matrix's dominant eigenvalue, where the 15-19-year-olds mix mostly with each other (0.8 by the average, 1.3 by the eigenvalue) | - | standard | option B, the catch-up for those born 2008-12 (0.9 against 1.3) | none reported (v2 landed by 2 of 2, 10-11) | sathya8571 |

## Earlier architectures

One line per dead architecture, or per group of them in one world, so the clone screen reads
them as history. Round-by-round detail is in each build's design note and card lineage.

| Task (architecture) | Fate | Domain | Obj | Gap | Pattern | Mechanism |
|---|---|---|---|---|---|---|
| 35 (v1) | retired 08-21: 3 solves | ECON | FC | objective | C | component below the floor pays nothing |
| 35 (election) | exhausted 08-21: 5 solves | ECON | FC | rule time | B, A | election over a filed schedule |
| 36 (v1) | retired 08-20 | SCL | RCA | rule | B | rebuilt available-to-promise clock |
| 37 (class, character) | exhausted 08-21; failed Gates C, G | ECON | DESC | objective population | G11, C | eligibility over post-stratification; commission floors |
| 37 (completions 1) | retired 08-22: 3 solvers on 1,347 | P&E | FC | time population | E | five filed predicates over every row |
| 38 (v1) | retired 08-20: 11 rounds solved | ECON | DESC | rule | B | estimator chosen by a reproduction test |
| 38 (v2) | retired 08-21: 4 solves | ECON | DESC | objective | G18 | corrections refused by a control total |
| 40 (cut 2) | retired 08-22: one-column scan solved it | ECON | ETL | rule population | B | producer test scannable on one column |
| 42 (v1) | failed determinism 08-22, Gate G | NPO | ETL | rule population | B | shipped dimension, rung refused it |
| 43 (pooled read) | retired 08-22: Gate C, Gate G split | NPO | CEX | objective population | E | refusing a pooled read the pack endorsed |
| 44 (v1, v2 cuts 1 to 3) | retired 08-24: solved 4 ways; Gate G | SCL | CEX | population time | E, B | line split by two equations; pilot transport |
| 45 (cuts 1, 2) | retired 08-22: solved on first passes | SCL | ETL | population objective | C | filed clause plus stated join route |
| 48 (v1) | retired 08-25: solved round 1 | PA | AD | rule population | none | five flags explained away, the hold |
| 50 (v1 to v3) | retired 08-27: 2 solves, Gate G | SCL | RCA | population time | none | queue replay; load per unit; slow clock |
| 51 (v3, v4) | retired: solved, Gate C, solved twice | ECON | RCA | - | - | receipts gap; tranche on a static register |
| 55 (v1) | retired 08-28: FEFO simulation solved it | SCL | FC | - | - | rung computed from six filed inputs |
| 56 (v5) | failed 08-29: out of scope, 0 per cent stumped | PA | ETL | population | E | booked-to-recoverable ratio untransportable |
| 56 (v4, v4.1) | retired 08-29: solved twice | NPO | ETL | rule population | B | close-outs reproduce only under settlement |
| 57 (v1) | retired: superseded, no outcome | NPO | ETL | objective population | none | pledge evaluated to payability |
| 57 (v17b to v19) | retired 08-30: v17b solved twice | DSS, P&E | FC | time objective | A, E | forward walk; held-out measure choice |
| 57 (v20 to v22) | retired 08-30: Gates C, D; 94 and 54 | NPO | DESC | objective population | G11 | sum of min(places, population) |
| 58 (v1, v5, v8) | retired 08-30: solved | SCL, P&E | ETL | objective | none | max flow; merged intervals; capped pro-rata |
| 58 (v2, v6) | retired 08-29: solved, replaced | - | ETL | rule | B | days-held rule summed; sub-area cap |
| 58 (v3, v4, v7) | failed determinism 08-29, Gate G | P&E | ETL | - | - | range-join exclusion; floor hinge |
| 58 (v9 to v14) | retired 08-30: solved or exhausted | SCL, DSS | ETL | population rule | B | back-test survivor; lot balance; hereditary scope |
| 59 (v1) | retired 08-31: a live solver filed it | ECON | FC | population | D | population rule absorbed by the rate |
| 60 (v1, v4) | retired 08-31: both solved | P&E | FC | rule | B | run length recovered from settled years |
| 62 (fertility, licence) | retired 09-04: graded rounds landed all four | DSS | AD | population time | B, D | exchange fold; tempo; two registers; hold |
| 62 (seat s.29, waves 14, 15) | retired 09-04: solved, asks collected | PA | ETL | time objective | A | confirm the base; exclusion tied to a term |
| 64 (v1 to v5) | retired 09-02: solved, v3 failed Gate A | PA | FC | objective population | B | shape menu; filed ceilings executed |
| 64 (v6 to v16) | retired 09-05: scored 29 to 93; Gate C; a live solve | PA | FC | population time | none | silent billing population; orthogonal ceiling |
| 65 (v1, v2) | retired 09-04: solved; 94 and 52 | P&E | DESC | objective population | none | rule filed in full; a sentence gave the rung |
| 67 (v1, v2) | retired 09-06: solved in R1, R2, R4, R5 | SCL | FC | population objective | none, B | fit only on unrationed periods |
| 69 (v1 to v3) | retired 09-06: solved; Gate G twice | DSS, PA | CEX | objective population | none, E | assignment rebuilt at intake; counting basis |
| 70 (v1) | retired 09-06: GBP 15,123.71 filed | SCL | ETL | population objective | D, B | date rebuilt from the next departure |
| 72 (v1) | retired 09-06: golden filed twice | P&E | RCA | population | D | dated site membership split |
| 73 (worlds 1 to 9) | retired 09-10: solved; Gate G (world 9) | P&E, PA | DESC | - | - | identities closed over shipped inputs |
| 74 (v1) | failed determinism 09-06, Gate G | PA | ETL | population objective | D, B | bridge from a reported count |
| 75 (v1) | retired 09-07: both landed 1,800 | NPO | FC | population time | D, C | stock from censored durations |
| 76 (v1) | retired 09-07: both filed GBP 130,130 | DSS | AD | - | - | arithmetic closed over shipped figures |
| 77 (v1) | retired 09-07: one response at 100 | P&E | FC | time objective | A | stock in flight times stage completion |
| 80 (v1) | retired 09-08: both landed 6,246 | P&E | ETL | population | - | status read off a returns signature |
| 81 (v1, v2, v3 cut 1) | retired 09-09: solved; Gate G | NPO, ECON | AD | objective time | none, D | examined share via a time ledger |
| 82 (v1) | retired 09-10: solved at 1,128 | PA | ETL | objective | - | gross of tender against net reads |
| 83 (v1, re-roots 1, 2) | retired 09-09: solved; Gate G | PA | RCA | population objective | C, E | model stopped selecting; holdout ranking |
| 85 (v1, v2) | retired 09-12: solved; Gate G | PA | AD | time population | B | narrated window; shipped screen |
| 86 (v1) | retired 09-12: Template vs task72 | SCL | ETL | population objective | D, B | continues as task90 |
| 86 (v2 cut 1) | retired 09-12: both filed the mix | DSS | ETL | population time | none, B | membership read through the head |
| 87 (v1 to v8) | retired 09-13: portal solves; Gates C, G | NPO, P&E | ETL | objective population | B, C | caps, rulings, counts, argmax |
| 89 (v1 to v7) | retired 09-13: out of scope; portal solves | P&E | AD | population objective | - | origin recovery; staffing gate |
| 89 (v8 to v11) | retired 09-14: portal solves; Gate G | NPO | AD | time | A | need in window; net burn; payee graded |
| 92 (v1 to v3) | retired 09-14: solved on the portal | SCL | ETL | objective population | C | threshold; tariff accrual; netted value |
| 93 (v1 to v3 cut 1) | retired 10-02: 3 portal solves | ECON | DESC | - | - | rate ladder; flat rate spelled out |
| 94 (v1, v2) | retired 10-03: solved on the portal | SCL | FC | objective population | C, A | annual rate; eight-week minimum |
| 97 (v1 to v4) | retired 10-02: 3 portal solves | PA, P&E | CEX | population objective | G11 | notice; deduction chain; per-occupation cap |
| 98 (v1 to v6) | retired 10-04: portal not stumped; Gate G (v5) | DSS, P&E | ETL | population time | D, B | residual; carry; kern; versioned register |
| 100 (v1) | retired 10-05: every response found it | P&E | ETL | time objective | none | census roll on filed sentences |
| 103 (v1, v2) | retired 10-04: solved on the portal | NPO | AD | population time | D | forms fan-out; banded weekly rate |
| 105 (v1) | retired 10-03: both filed Torquay 240 | DSS | FC | time objective | none | the natural basis was correct |
| 107 (v1 to v3) | retired 10-04: portal not stumped | ECON, P&E, NPO | DQ, CEX, ETL | population objective | E | replayed checks; comparison receipt; re-pointed pipeline |
| 109 (v1) | retired 10-07: solved in-house | BOA | ETL | population time | none | departure unit from a filed definition |
| 111 (v1) | retired 10-06: both filed it on the portal | BOA | RCA | objective population | none | rest after call-out via payroll |
| 124 (v1, v2) | retired 10-10: solved in-house | BOA | FC | population time | E | analogs' uncalled draw |
| 124 (v3) | retired 10-12: validated decoy, rungs stacked above solved steps | BOA | FC | population time | E | pre-cool hours against heat-matched uncalled days |
| 125 (v1) | spent 10-10: solved in-house twice, judge SEND_BACK on hygiene | AAF | AD | population time | none, A, B | a filed date ends a component class (digit-filter call-off) |
| 123 (v1) | retired 10-11: solved in-house four times (93.8, 80.2, 86.0, 91.7) after three hardening loops; re-rooted 10-12 | NPO | ETL | time rule population | B | trailing total over filed years only; scope from a term in force |
| 128 (v1, v2) | retired: v1 solved in-house 10-10; v2 spent at the wave-1 re-root 10-12 (rule application decisive; no client-domain task type) | BOA | OPP | objective rule | C | whole-host rebuild value; one change request per drain window |
| 130 (v1, v2) | failed on the portal 10-10, 10-11 | - | FC | - | - | designation; duty-date queue |
| 130 (v3) | retired 10-11: landed in house round 1 (the analog was the default construction) | ACT | FC | objective population | A | regression to the mean after selection |
| 133 (v1) | retired 10-11: one portal model at 100 | BANK | FC | time | none | survival to date, soft asks |
| 134 (v1) | retired 10-11: default was the golden | CJ | FC | population time | none | Kaplan-Meier, deaths as non-returners |
| 135 (v1) | retired 10-11: default was the golden | PES | FC | objective time | none | back-transformed median is not the mean |
| 180 (v1) | spent 10-11: solved in-house | ENR | AD | population | none | screen grain, metering system against supply number |
| 180 (v2) | spent 10-11: judge SEND_BACK, Gate C | ENR | AD | objective | none | main-tank acetylene attributed to a leaking compartment |
| 180 (v3) | spent 10-11: solved in-house, then rule application once filed | PHA | AD | population time | none | channelling against a self-controlled comparison |
| 181 (v1) | retired 10-11: solved in-house | BANK | AD | population | none | skimmed terminals behind a common point |
| 181 (v2) | failed portal determinism 10-11: PR-07 4.2 fork, landed once filed | EPH | AD | time population | none | nowcast each area on its own delay |
| 181 (v3) | failed at design 10-11: no filed back-test closes it | CJ | AD | population time | E, A | near-repeat runs against background |
| 228 (v1) | retired 10-11: collided with task129 | PA | DQ | population time | E, A | beacon calibration; reweighting |
| 229 (v1) | failed portal determinism 10-11 | ENR | DQ | population time | D | standard error of a build mean |
| 230 (v1) | retired 10-11: solved in-house twice | PA | DQ | population time | none | segment comparison pool |
| 254 (v1, v2) | retired 10-11 at stage 2: v1 the estimand named the overlay; v2 the literal annex read to the stump's month | PES, PHA | DESC | objective population | C | burned area by final perimeter; right-truncated onsets |
| 120 (v1, v2) | retired 10-09: v1 solved in-house (96.8), v2 drafted and blocked | ECON | DESC | population objective | none, B | unit formed by the claimant's roster; losses netted across spouses |
| 121 (v1, v2) | retired 10-10: v1 rejected at checkpoint A, v2 solved in-house twice (86.1, 89.5) | PA | RCA | population time | none, A | self-healing exposure; signed-out customers who own accounts (the identity join a schema read) |
| 121 (v3) | retired 10-12: judge FIX_NOW (an unfiled duplicate rule on an ask), then SEND_BACK on the re-judge: no filed basis for "behind the surge", and a pre-surge baseline names the rendering plant | PES | RCA | time population | G14 | an odor event's wind against the same clock hours on the season's other days |
| 127 (v1) | retired 10-10: judge SEND_BACK, a filed install sentence read in date order moves a co-op's slots | NPO | OPP | time objective population | none, C, E | a co-op crew's meter-set queue to year end |
| 446 (v1) | retired 10-11: rule application | BANK | ETL | population time | none | group fixed at the projection date |
| 500 (v1, v2) | solved on the portal 10-10, 10-11 | SCL, P&E | RCA | population | none | held blocks off late calls (shuttle, 15 of 28); a later start spilling onto siblings |
| 501 (v1, v2, v3) | v1 retired 10-11 on the rules; v2 solved on the portal 10-11; v3's buffer step replaced on paper 10-12; v3 retired 10-12 at stage 4 (judge: margin on an unfiled fit window, then the remaining funds' call-rate base unseparated) | QF | FC | time population rule | none, G6 | recycling term recovered from audited cells; filed walk-forward executed; filed path buffer readable; funds behind schedule draw their balance before their deadlines |

## Lessons the outcomes paid for

One line each, with the builds that paid for it. The techniques behind them are in `strategies.md`.

**What strong solvers always do**
- Apply a filed rule to an enumerated population: a computation no rung fixes (36, 37, 49, 61, 97 v3 to v4, 107 v3).
- Rank N filed candidates by a filed rule: the name comes back right however the rule changes (36, 7 solves).
- Align the outcome series to any dated cause; use a chronic condition or a gap with no series to align (36, 83 v1).
- Enumerate a finite menu a back-test selects over and read off the survivor; count the cells first (38, 45, 56 v4, 64 v1, 98 v4).
- Scan a rule recovered from stored labels as one parameter, and test it on every export to find a silent switch (40 cut 2, 98 v4).
- Read every governing document: composing two documents is a reading, not a construction (76 v1).
- Run the textbook default first: deduplication, merged intervals, max flow, pilot decomposition, Kaplan-Meier, explain-away and re-screen (44 v2, 58 v1, 58 v5, 134 v1, 181 v1, 446 v1).
- Reach a hold over flags each explained by a documented structure by meta-inference; a hold counts only when reaching it took work (48 v1).
- Find a population extreme on a rate at a small denominator through its count; sweep one- and two-column aggregates on the series the solver conditions on (48).

**What hands the answer over**
- A decisive rule filed at authority level 1 or narrated in policy wording is executed as written; run the delete-the-clause test (61, 85 v1, 89 v4, 93 v3 cut 1, 103 v1, 111 v1).
- A prompt or ask that requests the back-test, spells out the basis or presupposes the conclusion (49, 56 v4, 61, 77 v1, 98 v2).
- A shipped dimension or screen supporting the naive read is rung 0 with a filename and fails Gate G (42 v1, 74 v1, 85 v2).
- A device whose only defence is silence, once any note names it; sweep the social layer against the device list (65 v2, 76 v1, 78).
- A dictionary that explains public file layouts hands over the plumbing (57 v22).
- A governing identity closing over quantities the pack must ship is an execution exercise (73, 76 v1, 92 v2, 98 v1 to v2, 107 v3).
- A corpus reproducing every closed case without the decisive term is a counter-pin; one returning a single surviving cell is an answer key (45).
- A finer-grain working paper in the pack validated four rules at once (60).
- A natural basis that happens to be right on the graded rows (105 v1, 107 v3); a coarse band that absorbs the decisive move (103 v2).

**What holds**
- A corpus blind by construction (the regime opens after the closed period) confirmed a back-tester in the wrong rule (56 v5); that is the validated decoy the guard now blocks, so a control ties under every basis for a reason true now (`strategies.md` L1). Blindness by tuning or by excluding a class leaves a fingerprint (56 v6, 57 v23, 76 v2).
- A pin the solver reads, executes correctly and is harmed by, such as a billing-grain join that makes a population vanish (56 v6).
- A correct monitor blind by its configured grain, which cannot refer a population split across its cells (48 v2).
- A non-linear move: in a rate-times-exposure world every linear mechanism is absorbed when the rate is re-struck (56 v5, 59).
- Rivals made indeterminate (flat across a threshold band) rather than distant; a set-valued count decorrelated from the obvious count (52).
- A re-root that changes what one unit of the graded sum is; changing which rows enter it does not escape a closed identity (76 v1).
- Grading the quantity, not the name: a which-of-N graded on the payee absorbs the rate error (55 v3, 89 v11).
- Fewer rungs: removing one can buy separation adding one cannot; compute the packing floor and the subset sums first (45, 56 v6).
- Never one live degree of freedom: it cannot hold a ladder (49). A min(capacity, population) makes rungs outside the binding band inert (57 v23).

**The ask layer and the bar**
- A response stumped on the call still clears the bar when the asks are by-products of one forward pass (94 r6, 103 v3, 105 v2, 133 r1, 181 r1 at 52).
- Asks downstream of the construction pay only when nobody lands the call (58 v12.1 moved 38 of 49 there); with one response on it, decoupled asks cost the pair less while ask leakage is under a half (`supplemental-stumping` references A5), so asks stay decoupled.
- An ask whose rule sits beside it, or that is a dictionary line, is a reading exercise (61, 107 v2).
- N asks both top responses fail drag both down: 97/(2 x (87 + N)) is under 50 from N = 11 (60 v7).
- Redo the decorrelation count after any prompt repair; the ask mix moves (61).

**Determinism, scope and clones**
- An unforced construction (sample SD over root n) or a literal reading of a filed clause fails the portal's determinism QC (229 v1, 181 r2 on PR-07 4.2).
- A money answer asserts no amount on a half-cent boundary (58 v12). Assert the constraint binds in the data (64 v3, 0.59 of capacity).
- A confound that makes a reported figure misleading forces a refusal and fails Gate G; delete it, do not dress it (44 v2 cut 2).
- The artifacts decide the domain, not the tag: an accounting close is out of scope (56 v5), and so were call-centre operations (89 v7).
- A forward committed figure reads as Forecasting even when nothing is estimated (55).
- A request block can be a template at 1.5 per cent n-gram overlap; compare sentence shapes (63). A hardening loop can land on an earlier driver (130 v2 loop 1 against 73 world 10).
- Generators: `hash()` is salted per process (use blake2b); replacing a seeded draw shifts every later draw; assert key uniqueness across the file and every replayed quantity against the generator (48, 56, 58 v12).

**Unspent, so not mistaken for spent**
- The ledger's old row 41 (displacement under fixed assessment capacity, four outreach arms) was drawn and never built.
