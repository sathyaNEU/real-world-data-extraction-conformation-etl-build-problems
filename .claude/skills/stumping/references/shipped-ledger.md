# Shipped ledger

The builds the portal approved (the APPROVED_IN_PORTAL wave, STUMPED_IN_PORTAL_AND_READY_TO_LEARN) and the
lessons the portal paid for. Nothing else is kept here. Identity (domain, gap, pattern, driver, lineage, shell) is on the
fingerprint card (`../../fingerprint/cards/taskNN.json`), which `guard.py` bans against; how to find and
protect a stump is `../SKILL.md`, and the measured record behind every rule is `evidence.md`.

**Keeping it current.** A build gets a row here only when the author reports it approved in the portal:
its row goes into Approved builds and its portal status into the Portal record. Shipped builds awaiting a
result, returned builds and spent architectures have no row: their state is in each build's
`pipeline.json` and their identity and lineage on the card. Tasks below 100 are not tracked here.

**Format (parsed).** `clone-check/fingerprint.py` (`parse_ledger`) reads every line starting with `|`
whose first cell starts with a task number and maps the first ten cells by position: task, status,
domain, objective, gap, pattern, mechanism, calibration, artifact, decision. Later cells are for readers.
`guard.py` reads each task's strongest status through it and `status.py` reads the portal record. Keep
the task number first, no pipe inside a cell, and status words from one class only:

| Means | Status words the parser keys on | Rank |
|---|---|---|
| shipped, or approved | `delivered`, `approved` | 3, the exclusion |
| in build or open | `built ` (with the space), `rebuilt`, `hardened`, `awaiting`, `drawing`, `contested` | 2 |
| abandoned | `retired`, `failed`, `exhausted` | 1, history |

**Reading a row.** Dates are 2026, MM-DD. Objective: FC forecasting, RCA root cause, AD anomaly
detection, CEX experiment and causal, DESC descriptive, ETL extraction and conformation, OPP opportunity
sizing, DQ data quality monitoring. Domain abbreviations are the client's domains (PA product analytics,
SCL supply chain, ECON economics, NPO nonprofit, P&E policy and education, DSS demographic and social
science, BOA business operations, AAF accounting and audit, MCR marketing and consumer research, EPH
epidemiology, ENR energy and utilities, BANK banking and credit risk, QF quantitative finance, ACT
actuarial, HDE health economics, PES physical and environmental sciences, GSD general statistics, HFE
human factors, CJ criminology, BCR biomedical and clinical research, PHARM pharmacology). Gap and pattern
are the card's, decisive first; Cal and Art are the card's calibration organ and context artifact.

## Portal record

The author's portal list, rewritten whole each time they report it. Tasks below 100 are not tracked here.

| Task | Portal id | Portal status | Date |
|---|---|---|---|
| task100 | c25e448d-6679-4580-9b46-5b0850304c3a | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task101 | 1aa2aa53-5cbb-4103-862a-758cb725d502 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task102 | 5a798ae4-0ac3-4254-b895-028eeded4b10 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task103 | 079972d3-05c9-4c24-9546-7c87c4c940a8 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task104 | 75942cb4-cf82-41c4-865d-229ea22276ea | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task105 | 0d663732-82bf-4fba-ad56-a67b5074f031 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task106 | 16c2111a-934c-4e8a-b1ca-ed2335c9a507 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task107 | 17d4e5d9-7fd9-4acf-a2ab-e82de71ae010 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task108 | 4d1e2903-6452-45b0-afec-ce7cf3b70e50 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task109 | 9d1851a5-99cc-4129-b838-806c7ada966d | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task110 | 5a548639-10a4-49ba-93b3-3bd5d35b7894 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task111 | 34355e43-f330-4812-91ff-c9e3f37e920a | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task114 | d01e4abc-d188-424e-a322-c6fe043b29fd | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task115 | 6e962c38-379f-4c7a-97c7-7d38e6fed366 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task116 | db59e379-425e-474e-9876-f36d07e0f97d | PENDING_REVIEW | - |
| task117 | 261f5aed-b97e-417f-b02d-98f44bb3263c | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task119 | 8fee9bfd-50c0-45a8-8f2e-69966ee4d1d8 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task120 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task124 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task126 | adeccacd-4719-4d23-90c4-a5293c695201 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task128 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task132 | 4a42e005-f62d-469b-96cc-8a21e53b1953 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task135 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task141 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task151 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task162 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task169 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task175 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task179 | 2d6c30f6-8d7e-42ed-b73f-8630464142c7 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task182 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task196 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task236 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task253 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task258 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task275 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task303 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task309 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |
| task385 | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN | 10-30 |

## Approved builds

The portal's word on 2026-10-30: STUMPED_IN_PORTAL_AND_READY_TO_LEARN. One row per task, the approved
architecture only; the architectures a task spent before it are on its card's lineage. task179's approved
version is architecture 3 (the portal returned it as a Duplicate of task175 and approved both); its folder
holds architecture 5, not yet on the portal, and the row describes the folder.

| Task | Status | Domain | Obj | Gap | Pattern | Stump mechanism | Cal | Art | Decision | Portal result |
|---|---|---|---|---|---|---|---|---|---|---|
| 100 (v2) | SHIPPED & APPROVED 10-30 | P&E schools equity | ETL | time population | none | census rolled across the year end | - | - | four schools | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 101 | SHIPPED & APPROVED 10-30 | NPO cold-spot line | DESC | population rule | none, B | own top-ups sit in the baseline | - | - | 12.40 GBP a head | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 102 | SHIPPED & APPROVED 10-30 | P&E special education | FC | time objective | none | weekend due dates slip a fiscal year | - | - | $48,300,000 FY2029 supplemental appropriation (FY2029 SFS projected at $339,414,875 to the dollar against the FY2028 certified $387,664,450.77, shortfall $48,249,576) | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 103 (v4) | SHIPPED & APPROVED 10-30 | NPO food reserve | AD | population time | D | one hamper per household per week | - | - | CAD 279,234 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 104 | SHIPPED & APPROVED 10-30 | DQ alerting | AD | population rule | none, B | least sensitive threshold still paging | - | - | volwatch 3.25 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 105 (v5) | SHIPPED & APPROVED 10-30 | DSS lettings | OPP | objective time | C | homes sit on the nearest open branch | - | - | 150 tenancies | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 106 | SHIPPED & APPROVED 10-30 | SCL backhaul | OPP | objective population | none | one corridor's suppliers share return legs | - | - | EUR 370,900 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 107 (v4) | SHIPPED & APPROVED 10-30 | NPO power credit | FC | time population | A | intake moves to the experienced rate | - | - | $275,000 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 108 | SHIPPED & APPROVED 10-30 | SCL co-pack | FC | rule population | D, B | each requirement counted once | - | - | 12,853 cases | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 109 (v2) | SHIPPED & APPROVED 10-30 | BOA parcel claims | ETL | population rule | B | two unwritten compilation rules | - | - | promise days | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 110 | SHIPPED & APPROVED 10-30 | AAF fixed assets | ETL | population rule | B | enhancements ride the host's remaining life | - | - | $951,870 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 111 (v2) | SHIPPED & APPROVED 10-30 | BOA field service | RCA | time objective | none, A | which cause still operates forward | - | - | parts and van stock | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 114 | SHIPPED & APPROVED 10-30 | BOA facilities | DESC | time population | A, D | demand only when two parties share a site | - | - | dial | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 115 | SHIPPED & APPROVED 10-30 | MCR pricing | FC | time population | D, E | second response only where it undercuts | - | - | which of N | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 117 | SHIPPED & APPROVED 10-30 | SCL sourcing | FC | time population | E, A | draw caps via a dated join | - | - | 110 kW | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 119 (v2) | SHIPPED & APPROVED 10-30 | P&E mortality review | AD | objective population | C | beds held empty for planned work | - | - | Stennock | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 120 (v3) | SHIPPED & APPROVED 10-30 | ENR generation capacity planning | OPP | objective | G5, G3 | a day's use is the wells' production less the water the four tanks gained between Eastern midnights, not the largest day of production (none against 184 gpm) | - | - | added firm well capacity, 184 gpm | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 1 earlier return or reship |
| 124 (v6, round 3) | SHIPPED & APPROVED 10-30 | ENR lead service lines | FC | population | none, G6 | every verification route and the surviving cards sit on lead or galvanized mains far more than the unknown lines do, so the share holds only within the kind of main and era (99.2, 95.0 and 60.6 per cent on lead or galvanized mains, a few in a thousand and then none on copper ones) carried to the ... | - | - | zone finish years, last RZ-06 Wexley 2037 ($267 million | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 3 earlier returns or reships |
| 126 | SHIPPED & APPROVED 10-30 | P&E pendency | DESC | population rule | none, D | a carried file joins two units | - | - | 28.9 months | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 128 (v3) | SHIPPED & APPROVED 10-30 | BCF collections overflow | OPP | population objective | none, G5 | a call's effect read only on the over-capacity days' same list, the dialler's skipped records kept with the reached, scaled to a dial and sized on the new team's 400 a day | - | - | no centre gets the 2027 early-stage team | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 1 earlier return or reship |
| 132 | SHIPPED & APPROVED 10-30 | ENR asset condition | FC | population time | none | a replacement restarts the wear curve | - | - | 13 lots | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 135 (v2) | SHIPPED & APPROVED 10-30 | QF volatility | FC | time | none | noon fund prices carry the previous New York close, taken into the twelve-month variance through the daily cross-day covariances | - | - | 60 per cent growth | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 1 earlier return or reship |
| 141 | SHIPPED & APPROVED 10-30 | CJ recidivism risk assessment | FC | population time | none, G11, G13 | the capped terms' end-of-term petitions carried at the rate of the record's terms already at their offense class's maximum (38.7 per cent of their last-120-day windows draw a petition, 36 to 42 in every class, against 6.0 per cent of terms with room, 53.5 per cent of which are extended), not at the ... | - | capacity_report | 7 violator pods (projection 1,424, within seven pods' 1,261 to 1,470 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 2 earlier returns or reships |
| 151 | SHIPPED & APPROVED 10-30 | GSDS resampling and simulation | FC | population time | none, G1 | each bonus line priced at the share of the 1,440 seasons of the 2021-2026 winter-planned non-catcher regulars whose starts, read at the signing's 2027 lineup slot's plate appearances per start, reach its threshold, the basis FIN-14 4.4's look-back (working paper CF-14.4) over 748 hitter-seasons ... | - | register | accrue $4,250,000 (4,221,715 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 6 earlier returns or reships |
| 162 | SHIPPED & APPROVED 10-30 | EN&U asset condition, water network leakage | FC | time population | none, G7, G13 | each valve lowers its district's pressure only in the hours its inlet runs above the setting, and the paper mill's weekday draw on the trunk main takes the far inlets below the settings through the working day, so the 2027-28 leakage comes from replaying each day's hourly pressures through the ... | none | close_out_summary | whether the phase meets its contracted 0.48 Ml/d, and the find-and-fix gang-years | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 1 earlier return or reship |
| 169 | SHIPPED & APPROVED 10-30 | CJ recidivism-risk-assessment, client domain Criminology & Justice | FC | time population | none, G3, G13 | the Board's revocations in lieu of prosecution re-routed through the courts: arrests per day out of custody by time since release, times the courts' DOC-sentence share by charge grade read off the arrests the Board left to them, timed by the arrest-to-admission lag | none | capacity_report | 20 per cent of the 2027 parole releases return within two years (20.40 | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 9 earlier returns or reships |
| 175 | SHIPPED & APPROVED 10-30 | URS land use and spatial development modeling, client domain Urban & Regional Science | FC | population, time | none, G6, G14 | each vacant lot's permit chance read at the homes standing on the street it faces, the earlier extension areas having been served when their streets were built | none | register | 300 permits, the three areas' total at the nearest 50 (the default first-year analog 500) | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 2 earlier returns or reships |
| 179 | SHIPPED & APPROVED 10-30 | C&J recidivism risk assessment | FC | time population | none | each supervisee's 2027 booking chance from the caseload's own risk model plus the lift of being recorded by the city police as the victim of a violent incident, linked by surname, first given name and date of birth (30.7 against 4.4 per cent next-year bookings on the 2018 to 2025 year ends), with ... | none | forecast memo and GPS order workbook | 500 people booked on a new Category V charge in 2027 while supervised, to the nearest 100 (495.0) | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 4 earlier returns or reships |
| 182 | SHIPPED & APPROVED 10-30 | PES groundwater | AD | objective | none | each bore's own lagged driver response | - | - | 4 owners, 5 bores | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 196 | SHIPPED & APPROVED 10-30 | BANK fraud and AML detection | AD | population time | none | how many scam cases a member firm really held, recovered from the overlap of two capture channels where the second is largely produced by the firm chasing the first, so treating every register match as an independent sighting understates the count and a date rule cannot separate a sighting the firm ... | none | filed standard | the indemnity year index a mutual sets for a member firm, 31 scam cases per million payments sent | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 236 | SHIPPED & APPROVED 10-30 | EPH disease surveillance and outbreak anomaly detection | DQ | population | G16, G6, G14 | each region's change in the share of its influenza infections notified, read against the sentinel general practice network's influenza-like-illness rate times its protocol swabs' influenza positivity, which no regional testing change reaches | none | filed_standard | flag Far North, Metropolitan South, Metropolitan West and South Coast and no other region | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 253 | SHIPPED & APPROVED 10-30 | EDU student growth | DESC | population | G11, G17 | a count of schools past a floor is the sum of their probabilities, not a count of shrunken predictions (28 against 42) | - | - | 42 places | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 258 | SHIPPED & APPROVED 10-30 | PA web performance, LCP counterfactual (a media group's performance squad) | DESC | population, time | G8, G11 | each slow own-image page load rebuilt part by part as the engagements show the playbook lands (the delay at 240 ms, the load time at 0.48, each paint no sooner than its own first contentful paint) but only where the preload can reach the hero: the preload sits in the page's server-rendered head ... | - | - | send the squad to Trailhead, 4.9 million page loads a month into the good LCP band | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 275 | SHIPPED & APPROVED 10-30 | SROS nonresponse, calibration and measurement-error adjustment | DESC | population | G3, G12, G6 | each segment's discards as its observed trips' discards plus, on the unobserved trips, the unwanted catch per hour fished that observed trips show on each ground times the unobserved hours there, less the BMS the unobserved trips declared | gold_standard_subsample | operations_log | designate four: TR1, TR2, NEP and BT (12 to 14 per cent | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 4 earlier returns or reships |
| 303 | SHIPPED & APPROVED 10-30 | ESU asset-condition-maintenance | OPP | population | G8, G3 | each candidate's figure as nine in ten of its backbone's vegetation, wind and wildlife customer-minutes outside the accepted major event days over seven, after taking out the breaker tickets every feeder at the substation opened in the same minute (losses of the substation's supply the conversion ... | none | operations_log | F-205 (Sorrel Hill), 237,600 customer-minutes a year, USD 499,000 a year (the default path F-112, 455,400) | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; 2 earlier returns or reships |
| 309 | SHIPPED & APPROVED 10-30 | INS actuarial-science-insurance catastrophe-exposure-accumulation | OPP | objective | G14 | the roof's cut read class by class of peak gust from the insurer's own claims (about 0.59 under 130 mph, 0.06 above), which passes MG-04's storm-by-storm reproduction test, carried event by event through the vendor's 2027 set | none | register | Cypress Ridge, about USD 3 million a year removed (2.84), Marlin Shoals next at 2.08 (the default path Marlin Shoals at 1.07) | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30; approved on the first ship |
| 385 | SHIPPED & APPROVED 10-30 | (no card, folder or row on file; the portal record and a seed line in START_HERE.md are the only record) | - | - | - | - | - | - | - | STUMPED_IN_PORTAL_AND_READY_TO_LEARN 10-30 |

## Lessons the portal paid for

One line each, with the builds that paid for it; the measurements are in `evidence.md` and the rules in the
skills. Nothing here comes from a solver, a scored reader or a probe.

**What the portal's models do**
- Execute the field's named method for the deciding quantity by reflex, quoting the textbook; in none of the eighteen recorded landings did a response take the design's default path (139, 166 v1 and v2, 156, 137, 133, 255, 273 v2 and v4, 464 v2).
- Follow a filed sentence or a helper document to the quantity it names (118 v2's sign-off, 118 v3's policy, 144's field notes and manifest, 130 v1's bulletin, 141's review sentence, 124 loop 0's verification account).
- Read a column one join away as a column (117 round 1, 119 rounds 1 to 3, 120 v1, 124 loop 0); every approved stump moved off the column.
- Validate the easy route on whatever the pack offers and stop when it validates (179 v5, 135, 132); a record that refutes the stop rung is a search signal (120 v1).
- Handle every ask device whose handling is written anywhere: a filed rule (236 at 79, 114 at 62, 187), the asking sentence's own pin (196, 169 at 74), the frozen main files (151 at 84), a visible pairing (151 and 464 at 72).

**What held**
- A property with no column, read as a relation between rows or across files that nothing invites (117, 119, 114, 124, 128, 236, 275, 141, 303, 258).
- Identity resolved across different entities with no key (179 v3 class pairs; 175 the hundred-block; 196 the payment reference; 179 v5 surname, given name and birth date).
- The field's method at rung 0 or 1 filing a wrong answer, with the decisive step the precondition this dataset violates (every approved build; 1.1b).
- A back-test that confirms the textbook route (179, 135, 132) and a second source that agrees on the wrong reading too (126, 275, 196).
- Ask devices that are a reconstruction across two systems or grains no sentence states (151's catch-up half, 275's undated terminal chain, 119's arrival-dated transfers, 135's payment lag and lot lines, 268's re-accessioned specimens).
- Fast builds: draw commit to ship commit ran 42 minutes to 8.5 hours on the approved set (258 loop 2, 236, 162 v2, 303 v2, 275, 309, 128, 132, 253); the calendar time was the portal's.

**What was sent back**
- The field's named method as the golden (45 and more architectures in house, every portal landing); a filed estimand sentence naming what the correction adjusts for (193, 199, 273 v4, 269 v4, 270 v3 and v5).
- The fork is the stump: a decisive step that settles population, unit, window or comparison, dead whether filed or not (190, 192, 193, 269, 306, 305 v1, 483, 464 v3 and v9).
- A pin naming the clock, window, grouping or test the stump rides on (141 SF33, 179 v3 section 6, 181 v2, 118 v2, 124 loop 0), each landing the call the next round.
- A method whose deciding configuration is out of sample (162 v1: three passes, three new models) and a graded figure finer than the honest family's spread (141 pass 4, 309 pass 1, 157).
- A rubric at or over 70 on devices executable from written text (236, 151, 169, 464) and the unfiled convention under a holding device as a determinism return (119, 275, 281, 151 round 4).
- A shell repeated across worlds: the one Duplicate finding named the prompt's roles, the side table, the chart and the rounding, not the nouns (179 v3 against 175); 118, 305 and 273 kept one shell across every re-root.

**Repairs that worked, and the ones that never did**
- Worked: a WHAT pin in a governing document naming no method (169, 135, 151, 162); the world rebuilt so every sound route taking the step converges (169, 124, 196); the graded unit set to the decision or a band (175, 124, 141, 309, 196); asks re-sited onto what systems do to records (236, 151, 196, 175); the decisive step moved after a landed call (124, 258, 141, 162); a pointing sentence or file deleted (196, 141, 124, 258).
- Never worked: a rung stacked above the solved step (124 loop 1, 258 loop 1, 305 v2, 445 loop 2); a filed forecast test on a record lacking the deciding configuration (162); re-siting asks inside files the frozen call pins (151, twice); renaming a device's file without removing its control (196); decoys hiding an estimation sample (124 loop 1); hardening the asks alone after a landed call (none approved).
- A return inferred from absence is not a return: task182 (eight architectures, approved as shipped) and thirteen numbers filed failed from in-house reads until 10-25.
- A skipped gate predicts the return: every portal round on a build shipped at `precut: exit null` was a convention the gate asks for (448, three rounds).
