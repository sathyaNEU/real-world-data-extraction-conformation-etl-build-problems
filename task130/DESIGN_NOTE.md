# task130: the 2027 large-holder designation of census sections (realises ET02, the 13F institutional ownership bridge, redesigned as a stump)

Source note: `analytical_tasks/07_data_extraction_conformation/ET02_sec-13f-institutional-ownership-bridge.md` (ET02). Stage 1, draw, 2026-10-10. This is the build's one design note. Every count and date below is a draw-stage plan that stage 2 sizes and the generator asserts; nothing here is a measured figure.

```
DRAW  (independent draws, checked with ../fingerprint/guard.py)
  Card filed with guard.py register before the ladder was written? registered 2026-10-10 by the coordinator
    after task129, the wave's last   Verdict: PASS against the filed corpus (no WARN; one NOTE,
    test.same_driver_older against task62, differentiated on the card)
  Card filed: pending registration
  Shape: 03 bridge between two totals   Gate G mechanism: etl_conformance
  Gap: time (decisive), then population   Pattern: A (past exceedance against forward yield)
  Domain: Demographic & Social Science   Subdomain (enumerated): housing   Objective: Data Extraction & Conformation (ETL)
  Pairing repeated from last build? no (registered last three: task119 policy-education x anomaly-detection,
    task121 product-analytics x root-cause, task122 product-analytics x experiment-causal)
  Stakeholder role: head of the regional housing observatory (statistical_office_head)
  Context-artifact type: filed_standard (the designation programme order)
  Calibration form: prior_period_close_out (the 2026 designation's close-out: every watch-list section's
    large-holder dwellings and share on 1 January 2026)   Decision type: designation_set
  Decisive mechanism: holdings on the programme year's first day, where the housing agency has taken over
    scheduled sale agreements under its first-offer right (recorded only in its budget commitments) and
    completes each purchase 120 days after committing, a clock only its settled purchases show
    (G4, G3, G13, G16, G19)
  Repeats from prior builds: none on a banned axis; the (time, A, etl_conformance) signature repeats
    task62's seat-billing architectures, differentiated on the card
As-of date: 2026-09-30
```

Fiction's calendar: the large holders' quarterly dwelling returns are due 30 days after each quarter end, so the latest on file are those for 30 June 2026 (lodged by 30 July, with corrections and supplementary returns since); the portal moved from building rows to dwelling rows for returns lodged from 1 April 2026; the land register's deed extract and the housing agency's budget ledger run to 30 September 2026; the observatory works the designation in October and the order goes to the housing minister by 13 November 2026 for publication in the regional gazette before the 2027 programme year opens on 1 January 2027. The 2026 designation, the first, was computed in autumn 2025 on the 30 June 2025 returns rolled to 1 January 2026, and the agency's first-offer right began with it.

**Similarity claim.** No prior build commits a designation on holdings at a future effective date where a third party has displaced scheduled transfers and completes them on its own administrative clock, a move evidenced only in that party's spending commitments and its settled cases; the nearest driver on file scores 0.06 (task105, task100 and task75 lineages), and the closest mechanisms (task100's forward roll, task117's re-timing, task62's lapsing exclusion) are differentiated on the card.

**Pairing and shape.** The work is ETL: two years of versioned quarterly dwelling returns (corrections that replace, supplementary returns that add, a unit change keyed to the lodgement date, option and reservation rows, cadastral references to repair), a deed extract and an agency ledger conformed into one holdings table per section on the effective date, with the designation falling out of that table. The call faces forward (holdings on 1 January 2027, a date after the extract); every transfer it counts is known at the extract, so nothing is estimated and the tag stays ETL. Shape 03 arithmetic: two section bridges (the sections either side of the line on 1 January), each about 8 reconciling items in dwellings, 16; 14 watch-list sections x (large-holder share on 1 January to one decimal, designated or not) = 28; the largest large-holder group in each designated section with its dwellings, about 6 x 2 = 12; furniture (the designated count, the nearest section on each side with its share and gap to the line, five named chart parts, three files) about 10; about 66 criteria.

**Planned deliverables.** `designation_annex_2027.csv` (the order's annex: every watch-list section, its dwellings, large-holder dwellings and share on 1 January 2027, designated or not, its largest large-holder group), `section_bridge_2027.png` (the two bridges read at a glance, the 25 per cent line drawn at each section's dwelling count), `designation_brief_2027.pdf` (the brief that commits the designation to the minister). Provisional until the prompt is written.

**World.** The Observatori del Parc Residencial and its sister public housing agency, the Ens Públic de Patrimoni Residencial, which runs the Programa Primera Oferta (Valencian Community, Spain, EUR); a large holder is a person or group of related companies holding ten or more dwellings in the region. Personas drawn with `guard.py names --geo "Spain, Valencian Community" --seed 130`: Aurora Roig (head of the observatory, the requester), Leandro Sacristán (the agency's head of acquisitions, owner of the budget ledger), Celestina Gallart (built the 2026 designation), Amaro Peláez (director general for housing, receives the brief).

**Gate G.** Litmus: no. The returns, the deeds, the agency ledger, the published 30 June section shares and the 2026 designation are all correct; no file or voice reads a correct number the wrong way, and the difficulty is constructing holdings on a date no instrument has observed yet. Mechanism etl_conformance, framed by pattern A. surface_read_dependency: no. stumping_family: analytical_non_defect. sole_data_defect: no. Clean-data test per suspect file, to be asserted in the generator: the 30 June returns are complete and correct for 30 June (nothing to repair); the deed extract and the ledger are complete to 30 September; the instrument repair has nothing to substitute, because holdings on 1 January 2027 cannot be observed before that day. Lens-swap test: the stop rung and the answer are holdings on the same date with different transfers (who completes each displaced sale, and on which day), not one figure read two ways. Pre-draw identity test: the share closes over holdings on 1 January that the pack does not ship, and the decisive input (which transfers complete by then, and to whom) is neither filed nor visibly forced.

## Stump sentence

A competent solver conforms the 30 June 2026 returns (corrections replace, supplementary returns add, pre-migration building rows become dwellings, option and reservation rows drop, cadastral references are repaired by their control letters), rolls every dwelling to 1 January 2027 with the deeds registered to 30 September and the scheduled sale agreements at their agreed buyers and deed dates, reproduces the 2026 designation exactly and files a designation that keeps two sections over the line and leaves a third under it; the step that lands it there is carrying each scheduled agreement to its agreed buyer and date, when the housing agency's budget ledger shows it took over several of those agreements under its first-offer right and signed every purchase it has completed 120 days after committing, so on 1 January the agency holds the dwellings it committed to by early September (the two sections fall under the line) and a seller still holds the dwellings committed later, among them a December sale to a private buyer that the agency now completes in January (the third section stays over it).

## Decisive rung

Measured trap: **#13 Validates on one population, applies to another**, decided 3 of the client's 64 measured tasks, 2 of them under 0.50. The roll-forward is validated on the 2026 designation, a period in which no scheduled agreement had ever been taken over because the first-offer right began with that designation, and is applied to a year in which the agency has taken over agreements and completes them on its own clock. The client's own instance of the move is the Halls and Meeting Places drawdown task (mean 0.34): a scheduled-date field that fits every closed record is stale for the pending items, whose timing runs from a later event recovered from the paid record. Behind it, **#11 Beats the headline trap, misses the quiet one** (4 of 64, 2 under 0.50): a solver who gets the amendment semantics, the unit change, the exposure rows, the references and the forward roll right treats the last step as routine.

The two layers of the rung, and where each lives:

- **Displacement.** The agency's budget ledger (a spending extract shipped with the agency's records, its first-offer lines a minority among rent-support, repair and acquisition lines, the cadastral reference inside a free-text concept) is the only record of which scheduled agreements the agency has taken over. The returns schedule each agreement with its agreed buyer and deed date, correctly as of 30 June; nothing in them, the deeds or the programme order says an agreement can change hands after notification.
- **Clock.** Every settled first-offer purchase (in the deed extract, buyer the agency) was signed exactly 120 days after its ledger commitment, and none on its agreed deed date. That regularity is the only pin of when a pending purchase completes; no document states it.

The move runs both ways, so no partial reading lands on the answer: a portfolio sale between large holders agreed for February 2027 but committed by the agency in July completes in November (the section falls under the line, which the roll at agreed dates and agreed buyers misses twice over), while a sale to a private buyer agreed for December but committed in late September completes in January (the seller still holds it on 1 January, so the section stays over the line, which every earlier rung puts under it).

Open for the design stage: whether the programme order names the first-offer programme at all (fairness needs the agency's purchases to be knowable from the ledger and the deeds; a sentence describing their mechanics would make the solver ask the decisive question), and whether the large-holder threshold is reassessed on 1 January (a group that sells to the agency below ten dwellings takes its remaining dwellings out of the count, a cliff that could serve as a lower rung or a hazard).

## Ladder sketch

Candidates are the designated sets of the 14 watch-list sections; P, Q and S name the three sections the top rungs turn on. Counts are plans.

| Rung | Construction | Candidate | Killed by |
|---|---|---|---|
| R0 | each holder's latest lodged 30 June return taken whole (a supplementary return read as the full return), every row a dwelling, option and reservation rows counted, malformed references dropped as orphans, no roll-forward | set A, about 5 sections | the return dictionary's version field: a correction replaces the return it corrects, a supplementary return adds to it |
| R1 | versions applied as filed | set B, about 7 sections | the cadastre: rows lodged before 1 April 2026 are buildings carrying several dwellings each, whatever quarter they report |
| R2 | building rows expanded to dwellings by lodgement date, option and reservation rows dropped, references repaired by their two control letters; reproduces the observatory's published 30 June shares for 14 of 14 sections | set C, about 8 sections (the 30 June snapshot) | the programme order: a section is designated on the dwellings large holders hold on 1 January of the programme year |
| R3 (the stop) | every dwelling rolled to 1 January 2027 with the deeds registered to 30 September and each scheduled agreement at its agreed buyer and deed date; reproduces the 2026 designation section for section | set D, about 7 sections, P and S in, Q out | the agency's budget ledger: it has taken over several scheduled agreements under its first-offer right |
| R4 | the takeovers applied at the agreed deed dates | set E, P in, S out, Q out | the settled first-offer purchases: every one signed 120 days after its commitment, none on its agreed date |
| R5 (decisive) | the takeovers completed on the agency's clock | the answer, P out, S out, Q in | none |

Why each stop is satisfying: R2 gives back every published 30 June share to the dwelling; R3 is the forward roll the programme order asks for and gives back the only closed designation exactly, with every control tying; R4 has found the agency and applied its purchases on the dates the parties agreed.

## Why it survives the solver

Against `pilot_lessons.md`: the solver reads every document and executes every stated rule, so the version semantics, the lodgement-date unit change, the exposure rows, the reference check and the 1 January basis are all lower rungs it is expected to clear, and none of them carries the stump; it reproduces published tables and treats a mismatch as a search signal, so both controls (the published 30 June shares and the 2026 designation) reproduce exactly at the stop, and they do so for a structural reason (no agreement could be taken over before the first-offer right began with the 2026 designation), leaving no mismatch to search from; it finds any join whose keys line up, so the decisive record carries no key column into the returns (the reference sits inside a budget line's free-text concept, in a spending extract the ownership question never opens) and the deeds of settled agency purchases read to the roll as ordinary deeds; it replays at the finest grain and checks against closed periods, so the dwelling-level forward roll is the stop rung rather than a place it fails; and it applies stated deadlines and scope, which the 1 January basis already is. What held in the pilot is reproduced on both counts: like FC01, the decisive fact is operational and lives in a record the solver has no reason to open for the question asked, and its timing is pinned only by the settled cases' regularity, never by a sentence; like OS01, the step is a judgment the files support but never state, that a commitment in the agency's ledger displaces a sale the returns schedule, where the natural reading (the agreement completes as agreed) is defensible and nothing in the pack contradicts it. Residual exposure, stated so the solver round can test it: task100's forward designation rolls were solved when every limb sat on a filed sentence, a labelled column or a findable prior snapshot, and a solver that audits every file for transfers could read the ledger's first-offer lines; the build keeps the ledger off every ask path and gives no file a sentence on first-offer mechanics.

## Nearest exemplars

- **Budget on the Halls and Meeting Places fund balance running out in 2029-30** (Nonprofit & Grant-making, Capital Grant Drawdown Forecasting, model mean 0.34): every paid certificate falls on its scheduled date and the closed years reproduce from the schedule, but the pending awards run on a clock that starts at a later event recovered from the paid record; the model dated the pending stages from the schedule. The same move as this build's clock layer, on a different object.
- **Block-contract 899 beds for residents aged 85 and over in 2032/33** (Demographic & Social Science, Adult Social Care Capacity Planning, model mean 0.62): a forward position read on a future date after dated changes recorded in a register (five deregistration notices); the model built the demand model and stopped before the register. The domain's nearest forward-position task, and the warning that a filed register of the changes gets read (the 0.62 is the cost of a visible register).

## Guard

`guard.py check` on the scratchpad card (`cards/task130.json`): PASS. One NOTE, `test.same_driver_older` (decisive gap time, pattern A and Gate G etl_conformance repeat task62's seat-billing architectures), cleared by the card's differentiation line: task62's forward base grows because an exclusion lapses with its instrument and its population enters, while here a third party displaces scheduled transfers and completes them on its own clock. Differentiation lines are also on the card for task100 (forward designation roll) and task117 (re-timing), which the guard did not flag. No WARN. Nearest drivers 0.06 (task105, task100 and task75 lineages, task85). Personas clear of the name index. Not registered: the coordinator registers the wave in task-number order, and the axis bans against task127 to task129 (forum minister_or_cabinet, forcing event statutory_or_regulatory_filing, organisation research_or_statistics_office, pattern A, context artifact filed_standard, calibration prior_period_close_out) are checked then. Fallbacks if one blocks: pattern none with G4 decisive; context artifact close_out_summary; forum executive_team.

## Changes from the source note

- Domain: capital-markets ownership analytics (out of scope for Economics, which excludes markets trading) moved to Demographic & Social Science, housing: large-holder ownership of dwellings by census section, decided by a regional housing observatory.
- Scenario kept as a structure: 13F filers become large holders' quarterly dwelling returns, issuers become census sections, shares outstanding become dwellings per section from the cadastre, the 80 per cent crowded flag becomes the 25 per cent designation line, the top holder by market value becomes the largest large-holder group by dwellings, and the bridge from the raw sum to the conformed total stays (two sections, either side of the line).
- The note's honest-data traps become the lower rungs: RESTATEMENT and NEW HOLDINGS become corrections and supplementary returns; the VALUE unit keyed to the filing date becomes building rows against dwelling rows keyed to the lodgement date; option rows become option and reservation rows; the CUSIP check digit becomes the cadastral reference's control letters.
- The note's methodology memo is dropped: no shipped sentence states a decisive rule.
- The call moves from a retrospective report-period flag to holdings on the programme year's first day, and a decisive rung the note does not have (the agency's first-offer takeovers on its own clock) sits above the note's traps.
- Deliverables re-cut from the note's CSV, PNG and DOCX to a CSV annex, a PNG bridge and a PDF brief; the real SEC hosts are replaced by a fully constructed pack with declared provenance (dataset-generation section 2).

## Stage 2: design (2026-10-10)

Every count, share and date below is a target the generator builds forward and asserts; nothing here is a measured figure. Section codes are INE census-section codes (province, municipality, district, section). The fourteen watch-list sections and the roles they play in the ladder:

| Code | Municipality, district | Role |
|---|---|---|
| 4625001005 | València, Ciutat Vella | A1, designated at every correct rung |
| 4625002007 | València, l'Eixample | A2, designated at every correct rung |
| 4625011004 | València, Poblats Marítims | A3, designated at every correct rung |
| 0301401008 | Alacant, district 1 | A4, designated at every correct rung |
| 4625001012 | València, Ciutat Vella | **P**: a portfolio sale between two large holders agreed for February 2027 that the agency committed to on 9 July 2026, completing 6 November 2026 |
| 4625011016 | València, Poblats Marítims | **S**: a sale between two large holders agreed for 19 November 2026 that the agency committed to on 5 August 2026, completing 3 December 2026 |
| 0301402014 | Alacant, district 2 | **Q**: a large holder's December 2026 unit sales to private buyers that the agency committed to between 15 and 24 September 2026, completing 13 to 22 January 2027 |
| 4625002019 | València, l'Eixample | **T**: over the line on 30 June, under it on 1 January through deeds registered July to September (an ordinary roll) |
| 4625012009 | València, Camins al Grau | **U**: under the line on 30 June, over it on 1 January through a building a large holder bought in August (an ordinary roll) |
| 4625005013 | València, la Saïdia | O1, never designated at a correct rung; an option-heavy holder lifts it over the line while option rows are counted |
| 4625013021 | València, Algirós | O2, never designated |
| 0301405003 | Alacant, district 5 | O3, never designated |
| 1204001006 | Castelló de la Plana, district 1 | O4, never designated |
| 1204003011 | Castelló de la Plana, district 3 | O5, never designated |

### What the design stage settled

1. **The agency's takeovers touch twelve of the fourteen sections, not three.** The draw had the first-offer move deciding P, S and Q only, which left eleven sections' 1 January figures identical under the stop rung and handed the mirror response 33 annex cells. The agency has now committed to 84 large-holder dwellings under scheduled agreements across twelve sections, in all seven combinations of agreed date (before or after 1 January), completion date (before or after) and agreed buyer (a large holder or not), including the three that change nothing (benign twins). The large-holder count on 1 January differs between the stop rung and the answer by at least 3 dwellings in each of the twelve, and the one-decimal share differs in each of the twelve. P, S and Q are the only sections where the move crosses the line.
2. **No large-holder agreement taken over has settled by 30 September, and none has an agreed date on or before it.** Every large-holder commitment is dated after 30 June (6 July to 29 September 2026), so the earliest completion is 3 November; every agreement the agency took over has an agreed date after 30 September. The back-test a solver can run (every scheduled agreement in any return with an agreed date on or before 30 September, checked against the deeds) finds every one completed on its agreed date to its agreed buyer, 100 per cent. Nothing on the stop rung's path fails, is late or is missing.
3. **The clock is pinned by small owners' sales.** The agency's settled first-offer purchases (23 of them, committed January to May 2026, deeds May to September) are of dwellings whose sellers are not on the register, so they touch no return and no large-holder count. Each was signed exactly 120 calendar days after its commitment, and each commitment's concept quotes the notified sale's planned date, which differs from the deed date in 23 of 23. That one record kills both the agreed-date reading and the commitment-date reading.
4. **The programme order says nothing about first offer.** The right comes from a decree that is not in the pack. The order defines a large holder (public administrations and their entities are not large holders), the 25 per cent line, the 1 January basis and the annex's contents. The ledger's word for the right (tempteig, with the programme code PPO) and the settled agency deeds are the only traces of the mechanism.
5. **The large-holder threshold never moves anything.** Every registered holder holds ten or more dwellings in the Community on 30 June 2026 and on 1 January 2027 under every rung, and no buyer off the register reaches ten. The cliff the draw left open is closed by convergence, not used as a rung.
6. **The 1 January basis and the deed date are pinned in the order**: a dwelling is held on 1 January by whoever holds it under deeds executed on or before that day. No deed, scheduled date or agency completion falls between 28 December 2026 and 4 January 2027, and no deed in the extract was executed in the last ten days of September without being registered by 30 September.
7. **The deliverables keep the draw's three names, and the annex drops the two columns every response gets free** (each section's dwelling count, which is the cadastre's, and the designated flag, which is the share against the line and would hand the mirror eleven cells). The annex carries the large-holder dwellings and share (the call's components), the largest group and its dwellings, and the large-holder dwellings with nobody on the municipal register (the two device-carried asks). The bridge walks month by month, which is determinate without naming a kind of transfer.
8. **Kept as drawn:** the pairing, shape 03, the gap and pattern, the calibration form, the context artifact, the forum, the forcing event, the personas, the calendar-first opening move and the as-of date of 30 September 2026.

### Gate G

- **Litmus.** No. The returns, the deeds, the cadastre, the agency's budget ledger, the observatory's 30 June bulletin and the 2026 annex are all correct, and no stakeholder states a figure the task overturns. Each scheduled agreement in a 30 June return is a true record of the agreement as it stood on 30 June. The task exists because the order counts holdings on a day that has not come, and what happens between 30 June and that day is recorded in a party's spending commitments rather than in any ownership record.
- **Primary mechanism:** `etl_conformance`, framed by `forecasting` (pattern A: a correctly measured past snapshot against a forward position).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Deletion test.** Delete Celestina's note, the 31 March bulletin, the deposit register and the income atlas. The bulletin still reproduces at R2 on 14 of 14 sections, the 2026 annex still reproduces at R3 on 14 of 14, the back-test still certifies every agreement completing as agreed, and R3 still files A1 to A4, P, S and U.
- **Clean-data test, three depths, asserted per suspect file.** The suspect files are the returns (versioned, delta-shaped through supplementary returns and the no-change rule), the deed extract (cut at 30 September) and the ledger (cut at 30 September). Fill: consolidate every holder's 30 June picture into one complete return; R2, R3 and the answer do not move. Semantics: every field means what its dictionary says, and a scheduled-sale row means an agreement in force on 30 June, which it was. Instrument: no instrument can observe holdings on 1 January 2027 before that day; the deeds and the ledger are complete to their own cut, nothing executed or committed by 30 September is missing, and extending either past 30 September would invent records that do not exist at the as-of date. The generator asserts answer(repaired) = answer(shipped), R3(repaired) = R3(shipped) and answer != R3 for the fill repair of the returns.
- **Lens swap.** R3 and the answer are holdings on the same day built from different transfers (who completes each displaced sale, and on which day). Not one population read two ways.
- **Pre-draw identity.** Share = large-holder dwellings on 1 January / cadastre dwellings. The numerator closes over transfers that complete between 30 June and 1 January, and the decisive input (which scheduled sales the agency completes instead, and when) is neither filed in any ownership record nor visibly forced: it needs the ledger's free-text reference joined to the returns' scheduled rows and the settled cases' interval recovered.
- **Corpus direction.** Under the naive path both controls reproduce: the bulletin at R2 (14 of 14 to the dwelling) and the 2026 annex at R3 (14 of 14 to the dwelling), and the agreement back-test certifies R3's completion rule at 100 per cent. None of them refutes R3, because no agreement could be taken over before the right began on 1 January 2026 and none taken over since has an agreed date inside the observed window.
- **No shipped artifact ranks the candidates on the 2027 question.** The bulletin reports 30 June shares (labelled in-file as holdings on that date from returns lodged by 31 August); the 2026 annex is the closed 2026 designation, labelled as such; the 31 March bulletin is a superseded quarter.

### Entity, unit of value and decision

- **Entity and unit.** The Observatori del Parc Residencial prepares the yearly order that designates census sections for the large-holder programme; it is scored per certified output (one designation set, one annex row per watch-list section).
- **Two quantities that both read as size.** A section's large-holder dwellings as the returns report them on 30 June (the bulletin's figure) against the dwellings large holders will hold on 1 January. And for a scheduled sale, the agreed buyer and date against the party that will actually complete it and the day it will. They rank the sections differently because the agency's commitments since 30 June move twelve sections' counts, three of them across the line, and the ordinary roll moves two more across it.
- **Decision.** Exactly one designation set from the 2^14 subsets of the watch list, for the 2027 programme year.

### Stump sentence (re-solved)

A competent solver conforms the 30 June 2026 returns (a correction replaces the return it corrects, a supplementary return adds to it, a holder with no change since its last return is carried on that return, rows lodged before 1 April 2026 are expanded from buildings to dwellings, option and reservation rows are dropped, malformed cadastral references are repaired), reproduces the observatory's 30 June bulletin on all fourteen sections, rolls every dwelling to 1 January 2027 with the deeds registered to 30 September and every scheduled sale at its agreed buyer and date, reproduces the 2026 annex on all fourteen sections, and files seven sections (A1 to A4, P, S and U); the step that lands it there is carrying each scheduled sale to its agreed buyer and date, when the housing agency's budget ledger shows it committed to 84 of those dwellings in the watch list under its first-offer right after 30 June and its settled purchases were all signed 120 days after commitment, so P and S fall under the line (the agency holds the dwellings it committed to on 9 July and 5 August by November and December) and Q stays over it (the seller still holds the December sales the agency committed to in late September, which complete in January), and the order designates six sections: A1 to A4, Q and U.

### The answer

**The 2027 order designates six sections: 4625001005, 4625002007, 4625011004, 0301401008, 0301402014 and 4625012009.** Target shares on 1 January 2027 (one decimal; the generator tunes each count so the unrounded share sits at least 0.015 points inside its one-decimal bin and at least 0.5 points from 25.0):

| Section | Role | Cadastre dwellings (target) | Share 30 June (R2) | R3 | R4 (agreed dates) | **Answer (R5)** |
|---|---|---|---|---|---|---|
| 4625001005 | A1 | about 810 | 32.4 | 32.1 | 31.9 | **31.6** |
| 4625002007 | A2 | about 690 | 29.9 | 29.5 | 29.3 | **29.2** |
| 4625011004 | A3 | about 930 | 33.9 | 33.6 | 33.4 | **33.2** |
| 0301401008 | A4 | about 560 | 28.9 | 28.6 | 28.6 | **28.4** |
| 4625001012 | P | about 760 | 27.1 | 26.8 | 26.8 | **24.2** |
| 4625011016 | S | about 640 | 26.4 | 26.1 | 23.4 | **23.4** |
| 0301402014 | Q | about 600 | 27.4 | 23.3 | 23.3 | **25.7** |
| 4625002019 | T | about 720 | 25.9 | 23.2 | 23.0 | **22.8** |
| 4625012009 | U | about 540 | 23.5 | 26.7 | 26.6 | **26.5** |
| 4625005013 | O1 | about 880 | 21.4 | 21.2 | 21.1 | **20.9** |
| 4625013021 | O2 | about 750 | 20.1 | 19.9 | 19.9 | **19.6** |
| 0301405003 | O3 | about 610 | 18.7 | 18.5 | 18.4 | **18.2** |
| 1204001006 | O4 | about 690 | 22.6 | 22.3 | 22.3 | **22.1** |
| 1204003011 | O5 | about 520 | 17.8 | 17.6 | 17.6 | **17.4** |

- **The designated section closest to the line** is Q at about 25.7 (0.7 points over); the next designated section up is U at about 26.5, at least 0.3 points further.
- **The undesignated section closest to the line** is P at about 24.2 (0.8 points under); the next one down is S at about 23.4, at least 0.3 points further.
- **The bridge sections are therefore P and Q.** P's walk: the bulletin's 30 June figure, small July to September movements, about minus 20 in November (the agency's portfolio completion), small movements elsewhere. Q's walk: about minus 6 over July to September, about minus 4 in December (the sales the agency did not take over), and no movement for the fourteen deferred sales.
- **Margin.** A set decision has no runner-up ratio, so the guard that binds is the line clearance: every answer share sits at least 0.5 points from 25.0, and each of the three decisive sections crosses it by at least 1.3 points between R3 and R5 (P 2.6, S 2.7, Q 2.4).

### The ladder

| Rung | Construction | Set filed | Killed by (one shipped fact) | Why a good analyst stops here |
|---|---|---|---|---|
| R0 | each holder's latest-lodged 30 June return taken whole (a supplementary return read as the full return), holders with no 30 June lodgement left out, every row one dwelling, option and reservation rows counted, rows whose reference fails the cadastre join dropped as orphans, no roll | A1, A3, A4, P, O4 (5) | the return guidance's version field: a correction replaces, a supplementary adds, and a holder that lodged nothing for a quarter stands on its last return | it is the returns as lodged, summed per section against the cadastre, and every join that lands is clean |
| R1 | versions and the no-change rule applied as filed | A1 to A4, P, Q, O4 (7) | the portal's notice: returns lodged before 1 April 2026 carry one row per building, whatever quarter they report | the register's own rules are honoured line by line |
| R2 | building rows expanded to their cadastre dwellings by lodgement date, option and reservation rows dropped, references repaired by their control letters | A1 to A4, P, S, Q, T (8); the 30 June snapshot | the programme order: designation counts the dwellings held on 1 January of the programme year | it reproduces the bulletin's 30 June figures on 14 of 14 sections to the dwelling |
| R3 (the stop) | every dwelling rolled to 1 January 2027 with the deeds registered to 30 September and each scheduled sale at its agreed buyer and date | A1 to A4, P, S, U (7) | the agency's budget ledger: since 7 July it has committed to 84 watch-list dwellings under scheduled sales | it is the forward roll the order asks for, it reproduces the 2026 annex on 14 of 14 sections, and every agreement in the record with a passed date completed exactly as agreed |
| R4 | the agency's takeovers applied on the agreed dates | A1 to A4, P, U (6) | the settled first-offer purchases: 23 of 23 signed 120 days after commitment, none on the notified date | it has found the agency and applied its purchases on the dates the parties agreed |
| R4' (sibling) | the agency's takeovers applied from the commitment date | A1 to A4, U (5) | the same 23 settled cases: title passed at the deed, 120 days after commitment | a commitment of public funds reads as the moment the dwelling is spoken for |
| R5 (decisive) | the takeovers completed 120 days after commitment | **A1 to A4, Q, U (6)** | none | |

"A solver who does everything right up to R3 commits to seven sections: 4625001005, 4625002007, 4625011004, 0301401008, 4625001012, 4625011016 and 4625012009." Every rung files a different set and none equals the answer (asserted by name). Cleaning sits at R0 to R2, never at the decisive rung.

**The rung that carries the stump is R3 to R5, and it clears the seven survival properties.** (1) No shipped sentence describes first offer, displacement or the clock; the ledger's concept text is a budget line's description of what was bought. (2) No sweepable corpus nominates it: the 2026 annex and the agreement back-test are blind to it by construction (no takeover before 2026; no taken-over agreement inside the observed window), asserted case by case. (3) No arithmetic symptom: every agreement with a passed date completed as agreed, both controls tie, no join drops a row. (4) Not a per-row predicate: it needs the reference parsed out of a budget line's free text, joined to the scheduled rows of another file, and a constant recovered from a third population (small owners' settled deeds). (5) Its enumeration is arithmetic: which dwellings the agency completes before 1 January is commitment date plus a recovered interval, and the interval is visible only by joining settled commitments to deeds. (6) No cutover date steps any series: the takeovers run in three waves over July to September and no outcome series in the pack moves at a date. (7) It survives the deletion: with every wrong number and every belief deleted, R3 is still the natural forward roll and still reproduces both controls.

**Worth of each rung on the graded quantity** (the set, and the twelve touched sections' counts): R1 moves 2 sections' membership, R2 moves 3, R3 moves 3, R4 moves 2, R5 moves 3; on the counts, R3 to R5 moves at least 3 dwellings in each of twelve sections (the generator asserts the per-section delta). Sign: the conformance rungs raise the counts in most sections (versions, buildings and references add dwellings back; exposure rows remove a few), the ordinary roll lowers most, and the decisive rung moves both ways (minus in P, S and seven others, plus in Q and two others), so no single-signed partial correction lands on the answer.

### Position table (asserted set by set)

Distance is the number of sections whose membership differs from the answer (the symmetric difference).

| Rung | Set size | Distance from the answer | Sections wrong |
|---|---|---|---|
| R0 | 5 | 5 | P, O4 in; A2, Q, U out |
| R1 | 7 | 3 | P, O4 in; U out |
| R2 | 8 | 4 | P, S, T in; U out |
| R3 | 7 | 3 | P, S in; Q out |
| R4 | 6 | 2 | P in; Q out |
| R4' | 5 | 1 | Q out |
| R5 | 6 | 0 | |

R0's exact membership is tuned in the generator (the five above are the target); the assertion is that every rung's set is distinct from every other and from the answer, and that R2 and R3 each file at least seven sections.

### Separation and dominance

The decisive move has to beat what the decoy carries on the line, section by section. P carries 1.8 points of clearance over the line at R3 (26.8) and the agency's November completion removes 2.6; S carries 1.1 and loses 2.7; Q sits 1.7 under at R3 and regains 2.4. Each decisive move exceeds the clearance it overturns by at least 1.3 times (P 2.6 / 1.8 = 1.44, S 2.7 / 1.1 = 2.45, Q 2.4 / 1.7 = 1.41), asserted, and each lands at least 0.5 points past the line.

### The correction grid

Four conformance toggles (V versions with the no-change rule, B building rows, X option and reservation rows, K reference repair), each applied or not, crossed with six roll variants (none; deeds only; deeds plus scheduled sales as agreed, R3; takeovers on agreed dates, R4; takeovers from commitment, R4'; takeovers on the 120-day clock, R5): 16 x 6 = 96 cells. Plus seven partial cells on the decisive rung: the clock applied only to sales with a large-holder buyer; only to sales with a private buyer; only to agreements dated before 1 January; only to commitments before 1 September; the clock read as 4 calendar months; the clock read as 120 working days; and the takeovers applied only in the three sections that cross the line under R5 (which a solver cannot know, swept for completeness).

- Only the all-correct R5 cell files the answer set; each of the other 102 cells files a named wrong set, asserted cell by cell, and none files a set a solver could not defend (every cell is a set of sections; no cell produces a negative count or a share over 100).
- The 4-calendar-month reading and every day count from 110 to 132 return the answer set and the answer's counts on every section (C3 corridor, asserted), because no large-holder commitment falls between 22 August and 11 September and every commitment's completion under any reading in that range stays on the same side of 1 January. The 4-month reading is refused by the corpus (it misses at least 18 of the 23 settled deeds by at least one day), and 120 working days misses all 23 by more than 40 days.
- The deeds-only cell (no scheduled sales at all) files A1 to A4, P, S, Q and U (8), distinct from the answer.

### The calibration corpus

Three organs, each blind to the decisive rung by construction.

- **The observatory's 30 June 2026 bulletin** (context artifact and control): large-holder dwellings and share per watch-list section on 30 June, from returns lodged by 31 August. R2 reproduces 14 of 14 to the dwelling; R1 misses at least 8, R0 at least 11, each by at least 4 dwellings. Blind to everything after 30 June.
- **The 2026 annex** (prior-period close-out, the calibration form drawn): large-holder dwellings and share on 1 January 2026 per section, built in autumn 2025 from the 30 June 2025 returns. R3 run on the 2025 data reproduces 14 of 14 to the dwelling; the 30 June 2025 snapshot misses at least 9; the deeds-only roll misses at least 4 (the corpus scores the scheduled-sale rule). Structurally blind to first offer: the right began on 1 January 2026, the ledger has no line before 2026, and R3 and R5 run on the 2025 data return the same figures case for case (asserted twice, on the ledger being empty before 2026 and by re-running both).
- **The agreement back-test**: every scheduled sale in any return lodged from Q3 2024 to Q2 2026 with an agreed date on or before 30 September 2026 (target about 1,400 agreements) completes on its agreed date to its agreed buyer, 100 per cent, and none is a takeover. It certifies R3's completion rule over the window it can see and is blind to every takeover, asserted on the count of taken-over agreements with an agreed date on or before 30 September (zero).
- **The settled first-offer purchases** (the empirical pin of the clock): 23 commitments January to May 2026, 23 agency deeds May to September, deed date minus commitment date equal to 120 calendar days in 23 of 23, the notified planned date different from the deed date in 23 of 23, no seller on the register. Rivals and their misses: notified date 23 of 23 missed by at least 9 days; commitment date 23 of 23 missed by 120 days; 4 calendar months at least 18 of 23 missed by at least one day; 120 working days 23 of 23 missed by more than 40 days.
- **Twin pair.** Two of Q's December sales and two of T's December sales (T's not taken over) are identical on every column the returns carry (agreed month, private buyer, price band, building, door range, holder); Q's pair is still with the seller on 1 January and T's pair has left the large-holder count. Only the ledger separates them.
- **Resemblance.** Everything a lookup can see (the returns, the deeds, the 2026 annex) nominates R3's set: Q's December sales look exactly like every December sale that completed as agreed in 2024 and 2025.
- **Every rule the golden composes has a case that breaks if flipped**: versions (bulletin), no-change carry (bulletin, at least 9 carried holders with watch-list dwellings), building expansion (bulletin and 2026 annex), exposure rows (bulletin), reference repair (bulletin), the scheduled-sale roll (2026 annex and back-test), the takeover (no closed case can carry it; it is pinned by the ledger record itself), the clock (the 23 settled deeds), the deed-date basis (no deed is executed in one month and registered in the next across 31 December, and the order states the deed date).

### Pins and counter-pins

- **Filed pins.** The order (level 1): a large holder is a person or group of related companies holding ten or more dwellings in the Community, public administrations and their entities excluded; a section is designated if large holders hold 25 per cent or more of its dwellings on 1 January of the programme year; holdings follow deeds executed on or before that day; dwellings are counted from the cadastre; the annex lists each watch-list section's large-holder dwellings and share, its largest group as the register names it with that group's dwellings, and its large-holder dwellings with no resident on the latest delivery of the municipal register. The return guidance (level 4, field semantics): version types O, C and S, the no-change rule, the holding codes. The portal notice (level 5): building rows before 1 April 2026, dwelling rows from it. The register's dictionary (level 4): group membership is recorded by declarant with effective dates. The municipal register exchange note (level 5): each delivery replaces the previous one for the districts it contains; registrations past their renewal date have lapsed.
- **Empirical pins.** The 120-day clock (recoverable only as the unique interval reproducing the 23 settled deeds; any value from 110 to 132 gives the same answer). The scheduled-sale completion rule (the back-test, 100 per cent).
- **Counter-pins.** None. Celestina's note describes how she built 2026 (the 30 June 2025 returns rolled to 1 January with the deeds and the agreed sales) and says every agreed sale she had checked completed on time; both statements are true of 2025 and of every agreement the record can see, and the note states no rule for 2027.
- **What no file says.** That the agency can take over a notified sale, that a commitment displaces the agreed buyer, or how long the agency takes to complete.

### Fork grid: the 22-axis closure table (determinism-check A.5)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | every holder on the register on 1 January; the agency and other public bodies excluded | order pin; C1: no holder crosses ten in either direction, no off-register buyer reaches ten |
| 2 | Unit of account | the cadastre dwelling (reference plus door) | order and notice pins; C1: no co-owned dwelling in the fourteen sections |
| 3 | Attribution window | a transfer dates from deed execution | order pin; C1: no agreed date from 20 to 30 September, registration lag at most 10 days, no deed straddles a month end into the next quarter |
| 4 | As-of dating | holdings on 1 January 2027 | order pin; C1: nothing executed or completed from 28 December to 4 January |
| 5 | Version basis | O, then S replaces, C adds, in lodgement order; latest 30 June lodgement by 31 August | guidance pin; C2: the bulletin reproduces 14 of 14 |
| 6 | Denominator | cadastre dwellings per section | order pin; C1: no dwelling added or removed in the fourteen sections from 1 January 2025 to the as-of date |
| 7 | Weighting | none (a ratio of counts) | n/a, stated |
| 8 | Measurement window length | the roll runs 30 June to 1 January, fixed by the two dates | n/a; the settled-purchase corpus spans all 23 settled cases, no window choice |
| 9 | Boundary inclusivity | 25 per cent or more | order pin; C4: no share within 0.5 points of 25.0 at the answer, no deed on 1 January |
| 10 | Rounding path | share computed from integer counts, rounded once to one decimal; gap from the unrounded share | bin assertion: rounding the share first and then subtracting gives the same gap to one decimal for both nearest sections |
| 11 | Tie-break | largest group, nearest section on each side | C1: largest group leads the second by at least 3 dwellings in every section; nearest sections separated from the next by at least 0.3 points |
| 12 | Maturity and censoring | pending commitments completed on the clock | C2 (23 of 23) and C3 (corridor 110 to 132 days) |
| 13 | Order of operations | versions, then units, then exposure rows, then references, then the roll | C1: all 24 orders of the four conformance steps give the same 30 June picture (asserted) |
| 14 | Row order | irrelevant | C1: the answer recomputed on three shuffles |
| 15 | Duplicate resolution | a correction replaces the whole return; a supplementary never repeats a reference of its original | C1: no reference appears twice in any holder's conformed picture |
| 16 | Identity normalisation | references repaired by control letters to the one cadastre match; NIFs compared case-folded without separators | C2: the bulletin reproduces; C1: each malformed reference has exactly one cadastre candidate whose control letters validate |
| 17 | Netting against gross | section counts and bridge bars are net | prompt wording asks net change; C1: no month in either bridge has a gross in and out that a gross reading would separate within the same dwelling |
| 18 | Dimensional units | building rows against dwelling rows | notice pin keyed to the lodgement date; C4: the reporting-quarter reading misses the bulletin on at least 3 sections |
| 19 | Code and status semantics | holding codes PD counted, OP and RS not; budget phases D (commitment) and O (obligation at deed) | guidance pin; the ledger's own phase column; C2 on the settled cases |
| 20 | Integerisation | none needed | counts are integers by construction |
| 21 | Scope of a stated clause | the 1 January clause governs every annex column; the vacancy column reads the latest municipal delivery for each district | order pin and exchange-note pin |
| 22 | Forward window contents | deeds to 30 September, agreements not taken over as agreed, takeovers on the clock | C2 (back-test 100 per cent, settled cases 23 of 23) and C3 (corridor) |

### Deliverables and the criteria arithmetic

Shape 03, the bridge between two totals: each section's 30 June figure walked to its 1 January figure, with the two sections either side of the line drawn month by month.

1. `designation_brief_2027.pdf`, the brief Amaro Peláez reads: the designated set and its count; the designated section nearest the line and the undesignated section nearest it, each with its share and its gap to the line in points. About 8 criteria.
2. `designation_annex_2027.csv`, the order's annex, one row per watch-list section (14): large-holder dwellings on 1 January, share to one decimal, largest group as the register names it, that group's dwellings, large-holder dwellings with nobody on the municipal register. 14 x 5 = 70 cells; the generated rubric will compress them, target at least 28 criteria from the annex.
3. `section_bridge_2027.png`, rendered by the golden script: P and Q, each from the bulletin's 30 June figure through one bar per calendar month July to December (net change in dwellings) to the annex figure, the line drawn at 25 per cent of the section's dwellings with its value, a title carrying the designated count. 2 x (start, six months, end) = 16 values plus about 4 named parts.

Arithmetic: 8 + 28 (at least) + 20 + 3 files = about 59 criteria off the shape, against the 25 floor. Distinct findings: the designated set (the call), the forward walk for the two marginal sections (the bridge), the group concentration per section, the empty large-holder stock per section. Named-parts visual: yes. Breakdown at an explicit grain: one row per section. Robustness check: the bridge ties the bulletin's published figure to the annex figure, a cross-file reconciliation.

Script-generated: the CSV and the PNG come from the golden script; the PDF is typeset from the same figures.

### The ask ledger (supplemental-stumping)

**The main call's declared row population.** Return rows for references in the fourteen sections (columns: declarant NIF, return quarter, lodgement date, version type, replaced return, reference, door, holding code, agreed transfer date, agreed buyer NIF, agreed price), cadastre rows of the fourteen sections, deed rows for references in the fourteen sections (2025 and 2026), ledger rows of programme PPO whose concept carries a reference in the fourteen sections, the bulletin, the 2026 annex, the order, the guidance, the portal notice, the register's holder sheet (for who is a large holder). Asserted in the generator: **zero** device rows and zero hazard rows inside it. The device rows live in the register's group-link sheet, the group code table and the municipal register deliveries, which the main call never reads, and the one column of the returns an ask reads that the call does not (the group code stored at lodgement) carries no device by itself.

**Decoupling, asserted.** Recompute both asks under R3, R4, R4' and R5: every ask figure is identical across the four, because no agency-touched dwelling belongs to its section's largest group or the group second to it (sellers and agreed buyers in every takeover are small groups in that section), and every agency-touched dwelling is occupied on both municipal deliveries. The cracker and mirror sheets therefore differ only in the call's components.

**Ask B, the largest large-holder group per section and its dwellings (14 x 2).**
- Use: the order notifies each designated section's largest group, and the housing inspectorate addresses its first visits there; the annex carries it for every watch-list section so the notice list is ready whatever the minister changes.
- Primary device, a stored segment taken before a silent switch (D2, proven silent): each return carries the group code the declarant gave at lodgement. Four companies changed group between 1 July and 31 December 2026 (two acquisitions effective 1 October and 16 November, recorded in the register's link sheet in September with those effective dates; two exits effective 1 August and 14 December), and their 30 June returns carry the old code. The register's link sheet, in force on 1 January, is the record. Over-cleaning half: a fifth change is filed with an effective date of 1 March 2027 and must not be applied; reading the register's latest state applies it.
- Hazard HZ1, codes reissued to a different group (D7, proven silent): two group codes freed when their groups dissolved in early 2026 were reissued in May 2026 to new groups. Holders carried on returns lodged before the dissolution still bear the old code; joined to the code table they land on the new group's name with no orphan. The link sheet by declarant NIF is the record.
- Magnitudes (asserted): the primary alone moves the largest group or its count in at least 8 of 14 sections; HZ1 alone in at least 5; together in at least 11; every composed mishandling moves each moved figure by at least 3 dwellings, and no subset cancels back onto the golden.
- Stops: S1 the stored code mapped through the current code table (natural); S2 the link sheet used for the four switches but codes mapped through the current table; S3 the link sheet's latest state, the March 2027 change included (over-cleaned); S4 the right membership on the 30 June holdings (no roll); S5 the answer.
- Organs: the link sheet (structural) and the register dictionary's sentence that membership is recorded by declarant with its effective dates and that freed codes may be reissued (documentary, filed generally, in a different file from the returns).
- Path (8 files): returns, return guidance, portal notice, cadastre, deeds, register (holder and link sheets), group code table, order. Columns (12): declarant NIF, version type, replaced return, lodgement date, reference, door, holding code, stored group code, agreed buyer and date, link effective dates, code validity dates, group name.

**Ask C, large-holder dwellings with nobody on the municipal register (14).**
- Use: the agency's inspection unit plans the empty-dwelling notices the programme sends with the order; the count per section sizes the visits.
- Primary device, an absent reporter (D4, proven silent): the September 2026 municipal delivery is missing València districts 11 and 12 and Alacant district 2, whose last delivery is June 2026; a dwelling missing from the September file reads as empty. The exchange note's rule (each delivery replaces the previous one for the districts it contains) makes June the record for those districts. Over-cleaning half: genuinely empty dwellings in those districts appear in June with no resident, and some September districts have genuinely empty large-holder dwellings. Sections moved: A3, S and U (València districts 11 and 12) and Q (Alacant district 2), each by at least 6 dwellings (asserted).
- Hazard HZ2, lapsed registrations (code semantics by date, silent): non-EU residents whose registration passed its two-year renewal date without renewal are still listed with no status change; the exchange note states that such registrations have lapsed. Moves at least 9 of 14 sections by at least 2 dwellings.
- Hazard HZ3, units set per source (D3, proven silent): Castelló delivers one row per dwelling with a resident count (zeros included), València and Alacant one row per resident; counting rows reads every Castelló dwelling as occupied. Moves O4 and O5.
- Magnitudes: the primary moves at least 4 sections by at least 6 dwellings each; every section's figure sits under at least two devices; no subset of mishandlings cancels onto the golden in any section.
- Stops: S1 September file only, rows counted, missing read as empty (natural); S2 June fallback but lapsed residents counted; S3 every dwelling with any non-EU resident treated as empty (over-cleaned); S4 the right rule on the 30 June holdings; S5 the answer.
- Organs: the June delivery (structural, a second file) and the exchange note (documentary, a third).
- Path (10 files): returns, guidance, portal notice, cadastre, deeds, register holder sheet, order, municipal delivery September, municipal delivery June, exchange note. Columns (13).

**Referee.** The 2026 annex is byte-clean and never trapped; it arbitrates the scheduled-sale roll and nothing in the ask layer.

**Hazard table.**

| Hazard | Asks moved | Per-ask effect (target) |
|---|---|---|
| HZ1 reissued group codes | B | at least 5 sections' group or count |
| HZ2 lapsed registrations | C | at least 9 sections, at least 2 dwellings each |
| HZ3 per-source rows | C | O4 and O5, at least 5 dwellings each |

Two asks cannot carry hazards that cross several asks; each ask instead stacks a primary and at least one hazard on every graded figure (B's 28 figures under the primary or HZ1 in at least 11 sections; C's 14 under HZ2 everywhere it moves and the primary or HZ3 in six).

**Pair arithmetic, on paper.** Planning weights 38 / 7 / 55, with the annex's large-holder counts and shares, the brief and the bridge in the recommendation block (they are the call's components and its audit trail) and B and C as the asks. Mirror response (stops at R3): it keeps the large-holder counts and shares of the two untouched sections and a few chart parts, r about 4. Required: 55 x (Lc + Ls) <= 28 - 4 = 24, so Lc + Ls <= 0.44. Estimated leakage with the devices above and the battery applied: about 0.20 each (a top response that reads the register's link sheet by effective date and the exchange note's replacement rule clears the primaries; HZ1 to HZ3 then still hold most figures). Estimated pair: cracker 45 + 55 x 0.20 = 56, mirror 4 + 7 + 11 = 22, average 39. If the generated rubric files the annex's large-holder counts and shares as asks instead, the mirror keeps 4 of 28 of those cells and the cracker all of them, and the estimate moves to about 41; the Part 8 pair simulation reruns this with the real weights after stage 3.

**Separation.** Zero device rows and zero hazard rows in the main call's population, asserted with the counts in the generator; deleting every device from the pack leaves R3 and the answer unchanged (asserted).

### Assertion plan (generator and independent verifier: 26 groups, about 55 assertions)

1. Each rung's set by name (R0, R1, R2, R3, R4, R4', R5), all distinct, none but R5 equal to the answer.
2. The position table, row by row (set size and distance).
3. The 103-cell grid, cell by cell, with the set each cell files.
4. The corridor: every day count from 110 to 132 and the 4-calendar-month reading return the answer set and every annex count.
5. No large-holder commitment from 22 August to 11 September; every commitment Monday to Thursday; no completion on a Valencian public holiday or weekend.
6. The settled corpus: 23 of 23 at 120 calendar days; notified date different from deed date in 23 of 23; each rival's miss count and minimum miss.
7. The back-test: every scheduled sale with an agreed date on or before 30 September completed on that date to that buyer; zero taken-over agreements with an agreed date on or before 30 September; zero large-holder commitments dated on or before 30 June.
8. The bulletin reproduced by R2 on 14 of 14; R1 and R0 miss counts.
9. The 2026 annex reproduced by R3 on 2025 data on 14 of 14; R5 on 2025 data identical case for case; the ledger empty before 2026.
10. The R3 to R5 count delta at least 3 in each of twelve sections, and the one-decimal share different in each of them.
11. Line clearance: every answer share at least 0.5 points from 25.0; every share at least 0.015 points inside its one-decimal bin; both gap figures mid-bin and equal on both rounding paths.
12. Nearest-section separation at least 0.3 points on each side; the bridge sections are P and Q.
13. Dominance ratios for P, S and Q at least 1.3.
14. The twin pairs identical on every return column and split only by the ledger.
15. Threshold convergence: every holder at ten or more under every rung on both dates; no off-register buyer at ten or more.
16. No deed, scheduled date or completion from 28 December to 4 January; no co-owned dwelling in the fourteen sections; no cadastre change in the fourteen since 1 January 2025.
17. All 24 orders of the conformance steps give the same 30 June picture; three row shuffles give the same answer.
18. Each malformed reference has exactly one validating cadastre candidate; the reporting-quarter reading of the unit change misses the bulletin on at least 3 sections.
19. The clean-data fill repair: answer and R3 unchanged, answer different from R3.
20. Ask B: golden per section, each stop's figures, the primary's and HZ1's moved-section counts, composed-subset deltas, the largest group's lead of at least 3.
21. Ask C: golden per section, each stop, the primary's, HZ2's and HZ3's moved-section counts, composed-subset deltas.
22. Decoupling: both asks identical under R3, R4, R4' and R5.
23. Separation zero-counts inside the main call's population; deleting the devices moves neither R3 nor the answer.
24. Hygiene battery on each ask's wrong path comes back clean (no duplicate keys, no orphan joins, no fan-out).
25. Leak sweeps: no shipped sentence contains first offer, tempteig outside the ledger's concept column, displacement or a day count; the programme code PPO appears only in the ledger.
26. Input gates: at least 10 files, at least 4 formats, the returns file at least 25,000 rows, three distractors named in metadata.json; two consecutive builds byte-identical.

### Pack plan (stage 3 builds against it; names provisional, in the organisations' own idiom)

| File | Format | Role |
|---|---|---|
| `declaracions_grans_tenidors_2024T3_2026T2.csv` | CSV, about 68,000 rows | spine: every version of every holder's quarterly return, held, scheduled-sale, option and reservation rows |
| `guia_declaracio_trimestral.pdf` | PDF | return guidance: version types, the no-change rule, holding codes, field list |
| `avis_portal_canvi_format.eml` | EML | the portal's notice of the change from building to dwelling rows for returns lodged from 1 April 2026 |
| `registre_grans_tenidors.xlsx` | XLSX | the register: holders (NIF, name, registration), group links with effective dates, dictionary sheet |
| `codis_grup.csv` | CSV | group code table with validity dates and names |
| `cadastre_habitatges_extracte.csv` | CSV | every dwelling (reference, door) in the fourteen sections and every dwelling on any return, with its section |
| `escriptures_inscrites_2025-01_2026-09.csv` | CSV | deeds registered January 2025 to September 2026 for those dwellings: execution and registration dates, seller and buyer NIF, price |
| `EPPR_execucio_pressupost_2026.csv` | CSV, about 6,500 lines | the agency's budget execution January to September 2026, every programme, phases A, D, O and P, free-text concept |
| `butlleti_parc_residencial_2026T2.pdf` | PDF | the observatory's 30 June bulletin: watch list and per-section 30 June figures |
| `annex_designacio_2026.xlsx` | XLSX | the 2026 annex (the close-out) |
| `ordre_programa_grans_tenidors.pdf` | PDF | the programme order (governing document) |
| `padro_lliurament_2026-09.csv`, `padro_lliurament_2026-06.csv` | CSV | the two municipal register deliveries |
| `nota_intercanvi_padro.txt` | TXT | the exchange note |
| `notes_designacio_2026.docx` | DOCX | Celestina Gallart's working note on the 2026 build (social layer) |
| `fiances_lloguer_seccions_2025.csv` | CSV | distractor: rental deposit register by section |
| `atles_renda_seccions_2023.csv` | CSV | distractor: household income by census section |
| `butlleti_parc_residencial_2026T1.pdf` | PDF | distractor: the superseded 31 March bulletin |

18 files, 6 formats. Provenance: a fully constructed pack (dataset-generation section 2); the INE section codes, the municipality codes and the cadastral reference format with its control letters are real conventions.

### Realism debts

- **The agency's July to September commitments** (84 large-holder dwellings in the watch list and 16 elsewhere, plus 19 small owners', in three months) follow a mid-year credit increase that the ledger shows as a budget modification line in July; on a regional programme that is a plausible scale, stated here because it is concentrated.
- **The three-week gap with no large-holder commitment** (22 August to 11 September) is forced by the corridor; it sits in the August holiday and the budget cycle and is mirrored by a dip in every other programme's commitments in the same ledger.
- **Exactly 120 days, every time.** An administrative completion period fixed by the decree that is not shipped; the ledger shows the O phase on the deed date for every settled case, so the regularity reads as procedure rather than coincidence.

### Stopping rule (written before any round)

- One plain solver. If it files any set other than the six sections, the build goes to the determinism judge.
- If it files the six sections, the route is read: a solver that reached the ledger from the deeds' agency buyers gets a loop that moves the settled clock cases off the deed extract's buyer column (agency purchases registered under the agency's nominee company); a solver that reached it by auditing every file gets a loop that re-roots the ledger as a monthly commitments report keyed by expedient number with the reference in a second file. Three loops, then retire.

### Prompt

`prompt.md`, calendar-first, three files, 255 words at 25.5 words a sentence; voice-check clean (no calcified carrier, no shared six-word run, every ECONOMY gate under its flag). Written below the stump sentence's vocabulary: no input file named, no mention of first offer, the agency, deeds, returns or the 1 January basis, one stakeholder belief (Celestina sees no reason to change last year's method), and the bridge window carried as "every calendar month in between" so the prompt fixes no date.

## Build record

Stage 3a, the evidence pack, 2026-10-10. Generator: `generator/build.py` (modules `common`, `plan`, `world`, `history`, `nonwatch`, `returns`, `tables`, `ledger`, `padro`, `docs`, `distractors`, `writers`, `analysis`, `asserts`); independent verifier: `generator/verify.py` (pandas, its own parsing, conformance, roll and asks, reads only `target/` and, for the input gates alone, `metadata.json`); `generator/ship.py` runs the double build and the comparison. Seed 130. Every figure below is read off the generator's record or the verifier's report of the shipped files.

**Gate outcomes.**

- Generator green: 120 assertions (the 26 groups of the plan, plus the container audit and the referee checks).
- Two consecutive builds into the scratchpad byte-identical, file mtimes included (20 files: 19 in `target/` plus `metadata.json`); the task-folder build is byte-identical to both.
- Independent verifier green on the task folder; generator and verifier agree on 205 figures (the answer, 14 annex rows by 5 columns, 7 rungs by 14 sections, both nearest sections with share and gap, both bridges, the corpus counts, the 2026 close-out).
- Input gates: 19 files, 6 formats (csv, pdf, eml, xlsx, txt, docx); the returns file carries 45,746 rows; three distractors named in `metadata.json` (`fiances_lloguer_seccions_2025.csv`, `inspeccions_habitatge_buit_2025.csv`, `butlleti_parc_residencial_2026T1.pdf`) and nowhere in `target/`.
- Containers: `scrub_producer_metadata.py` audits `target/` clean (no writer signature, no timestamp outside 2024-01-01 to 2026-10-10); PDFs scrubbed in place at equal length, OOXML repacked with in-fiction authors and fixed entry times; mtimes set per file to in-fiction write times (the order 3 September 2025 through the file index 6 October 2026).

**The pack as built** (file names in the organisations' own idiom; the documents are in Valencian):

| File | Role | Size |
|---|---|---|
| `declaracions_grans_tenidors_2024T3_2026T2.csv` | spine: every version of every return, parcel rows before 1 April 2026, dwelling rows from it | 45,746 rows |
| `cadastre_habitatges_extracte_20260928.csv` | every unit of the 14 sections (shops and garages included, `us` column) and every dwelling on any return | 24,557 rows |
| `escriptures_inscrites_2024-07_2026-09.csv` | deeds executed July 2024 to September 2026, registered by 30 September | 2,001 rows |
| `EPPR_execucio_pressupost_2026_gen-set.csv` | the agency's budget execution, six programmes, phases A, D, O, P | 5,254 lines, 142 first-offer D lines |
| `registre_grans_tenidors_20261001.xlsx` | holders (143), group links (39) with effective and entry dates, dictionary | |
| `codis_grup.csv` | current group-code table (one row per code) | |
| `padro_lliurament_2026-06.csv`, `padro_lliurament_2026-09.csv` | municipal register deliveries for the 14 sections | 21,284 and 15,029 rows |
| `nota_intercanvi_padro_rev2.txt` | exchange protocol: replacement by district, the renewal rule, the per-dwelling format | |
| `ordre_designacio_seccions_grans_tenidors.pdf` | the order: definitions, 25 per cent on 1 January, deed execution date, annex contents | |
| `guia_presentacio_declaracio_trimestral_2024-01.pdf`, `avis_portal_canvi_format_2026-03.eml` | return guidance (O, C, S, no-change rule, codes) and the unit change by lodgement date | |
| `butlleti_parc_residencial_2026T2.pdf` | the 30 June bulletin (control, R2) | |
| `annex_designacio_2026.xlsx` | the 2026 close-out (calibration, R3 on 2025 data) | |
| `notes_annex_2026_CGallart.docx` | Celestina Gallart's method note (social layer) | |
| `index_expedient_designacio_2027.csv` | the file index (provenance record) | |
| distractors | deposit register 2025, inspection visits 2025, the 31 March bulletin | |

**The answer as built.** The order designates six sections: 0301401008 (A4, 28.0), 0301402014 (Q, 25.7), 4625001005 (A1, 31.4), 4625002007 (A2, 29.3), 4625011004 (A3, 33.3), 4625012009 (U, 26.2). Nearest designated Q at 25.7 (0.7 over, 155 of 603); nearest undesignated P at 24.2 (0.8 under, 183 of 757); the next ones are U at 26.2 and S at 23.4. Bridges: P 205 then July to December -1, 0, 0, -1, -20, 0 to 183; Q 165 then -2, -2, -2, 0, 0, -4 to 155.

| Section | Role | N | R0 | R1 | R2 | R3 | R4 | R4' | **R5** | share | largest group (dwellings) | empty |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0301401008 | A4 | 561 | 152 | 154 | 162 | 160 | 160 | 157 | **157** | 28.0 | Grup Cantonera (43) | 8 |
| 0301402014 | Q | 603 | 142 | 154 | 165 | 141 | 141 | 141 | **155** | 25.7 | Grup Barana (38) | 9 |
| 0301405003 | O3 | 612 | 92 | 98 | 114 | 113 | 109 | 109 | **109** | 17.8 | Grup Cantonera (28) | 5 |
| 1204001006 | O4 | 688 | 175 | 180 | 156 | 154 | 154 | 154 | **154** | 22.4 | Grup Porxo (40) | 9 |
| 1204003011 | O5 | 516 | 83 | 87 | 93 | 92 | 92 | 92 | **92** | 17.8 | Grup Arcada (25) | 6 |
| 4625001005 | A1 | 812 | 214 | 228 | 263 | 258 | 258 | 255 | **255** | 31.4 | Grup Barana (89) | 14 |
| 4625001012 | P | 757 | 200 | 201 | 205 | 203 | 203 | 183 | **183** | 24.2 | Grup Xamfrà (75) | 11 |
| 4625002007 | A2 | 689 | 146 | 179 | 205 | 199 | 199 | 198 | **202** | 29.3 | Grup Finestral (73) | 9 |
| 4625002019 | T | 722 | 126 | 132 | 187 | 166 | 163 | 163 | **163** | 22.6 | Grup Finestral (50) | 12 |
| 4625005013 | O1 | 879 | 164 | 172 | 188 | 186 | 186 | 183 | **183** | 20.8 | Grup Escaire (47) | 10 |
| 4625011004 | A3 | 931 | 255 | 272 | 316 | 313 | 308 | 308 | **310** | 33.3 | Grup Barana (108) | 17 |
| 4625011016 | S | 641 | 114 | 128 | 169 | 167 | 150 | 150 | **150** | 23.4 | Grup Mitgera (48) | 7 |
| 4625012009 | U | 538 | 105 | 110 | 126 | 144 | 144 | 141 | **141** | 26.2 | Grup Ràfec (54) | 13 |
| 4625013021 | O2 | 748 | 132 | 139 | 151 | 146 | 146 | 146 | **149** | 19.9 | Grup Andana (48) | 6 |

Rung sets, asserted by name: R0 A1, A3, A4, P, O4; R1 A1 to A4, P, Q, O4; R2 A1 to A4, P, Q, S, T; R3 A1 to A4, P, S, U; R4 A1 to A4, P, U; R4' A1 to A4, U; R5 A1 to A4, Q, U. The position table holds as designed (distances 5, 3, 4, 3, 2, 1, 0).

**Controls and the calibration corpus, as measured.** R2 reproduces the 30 June bulletin on 14 of 14; R1 and R0 miss it by 4 or more on 14 and 14 sections. R3 on the 2025 data reproduces the 2026 annex on 14 of 14 (designated A1 to A4, P, Q, S, T); the 30 June 2025 snapshot misses it on 13, the deeds-only roll on 8, and R5 on the 2025 data equals R3 case for case. The deeds to 31 December 2025 agree with the annex too, so the close-out is also the outcome. Back-test: 834 of 834 agreed sales with a date to 30 September completed on the agreed date to the agreed buyer. Settled first-offer purchases: 23 of 23 at 120 calendar days; the notified date misses all 23 by 10 to 82 days; four calendar months misses 18 of 23 (0 to 3 days); 120 working days misses all by 50 to 55 days. Corridor: every interval from 110 to 132 days and four calendar months give the answer's counts in all 14 sections. Dominance: P 2.64 against 1.82 points of clearance (1.45), S 2.65 against 1.05 (2.52), Q 2.32 against 1.62 (1.44).

**Grid.** 96 cells (four conformance toggles by six roll variants): only the all-correct R5 cell files the answer, the other 95 file wrong sets, each mapped to the shipped rule it violates. Partial cells: the clock applied only to large-holder buyers, only to private buyers, only to agreements dated before 1 January, or only to commitments before 1 September each file a wrong set; 120 working days files a wrong set; taking the commitments over only in P, S and Q files the answer set but misses the counts of nine sections.

**Asks as measured.** Ask B: the largest group leads by 3 or more everywhere; stored codes (the natural stop) move 13 sections; the switches alone (reissue handled) 9; the reissued codes alone 5; links else stored 8; the latest-state link sheet (over-cleaned) 1 (U); no roll 10; every moved figure moves by a name or by 3 dwellings or more. Ask C: golden 5 to 17 per section; the September file read alone puts every large-holder dwelling of A3, S, U and Q in the count (310, 150, 141, 155); lapsed registrations counted as residents move 12 sections by 2 or 3; per-dwelling rows counted as people zero O4 and O5; reading every non-EU resident as absent overstates all twelve per-person sections. Both asks are identical under R3, R4, R4' and R5, and deleting the link sheet, the code table and both deliveries moves neither R3 nor the answer.

**Departures from the stage 2 plan, all asserted.**

- The agency's commitments touch twelve sections with net R3 to R5 moves of 3 to 20 dwellings; O4 and O5 (Castelló) are untouched, so their figures match the stop rung. The plan's answer table had all fourteen moving; the stage 2 text (twelve) holds.
- 84 large-holder dwellings in the watch list are under first-offer commitments (the stump sentence said about 64), plus 16 elsewhere in the region; 142 first-offer D lines in all (with 23 settled and 19 pending small-owner purchases).
- The large-holder commitment gap runs 22 August to 13 September (the corridor's own arithmetic: 1 January minus 110 days is 13 September), not to 11 September.
- Shares differ from the plan's targets where the bins required: A1 31.4, A2 29.3, A3 33.3, A4 28.0, P 24.2, S 23.4, Q 25.7, T 22.6, U 26.2; every answer share sits 0.015 points or more inside its bin and 0.5 points or more from the line.
- The reporting-quarter fork on the unit change is closed by convergence rather than measured: every row's shape (parcel and units, or a 20-character reference) follows its lodgement date, asserted, so no reading of the notice can apply the wrong unit to a row. Returns for 2025T4 lodged after 1 April carry dwelling rows, asserted.
- The reference repair is made load-bearing at the answer: five malformed references sit in Q's 30 June picture (dropping them puts Q under the line), with Q's option rows raised to four so R1 keeps Q over it.
- To hold every ask B stop at a name or 3 dwellings, the leading group in eight sections buys 4 dwellings from a small holder between July and September (sales between large holders, count-neutral for every section and every rung).
- The 2026 annex's group column reads membership on 1 January 2026; no group whose code was later reissued leads any section, and the stored-code reading reproduces the column, so the referee arbitrates the roll and nothing in the ask layer.
- `DATASET_NOTES.md` is not written: this note carries the pairing, the ladder and the ask ledger, and a second note is banned in a task folder.

Stage 3b, the write-up and ship checks, 2026-10-10. `generator/golden.py` reads only `target/` (through the verifier's own parsing and conformance) and writes `golden/designation_brief_2027.pdf` (to Amaro Peláez from Aurora Roig, dated 30 October 2026, before the earliest agency completion it describes), `golden/designation_annex_2027.csv` (14 rows, the 2026 annex's column vocabulary) and `golden/section_bridge_2027.png`; it asserts the bulletin tie, both bridges closing, the 23 settled cases at 120 days and every count word in the brief from its own lists, scrubs the containers with the in-fiction producer and stamps the files 30 October 2026. Its figures equal the verifier's on every annex cell, both nearest sections and both bridges, and two runs are byte-identical. `submission.md` is in the five-block format; golden-realism and the reduce-house-fixes register ran after the figures froze and moved no figure. Two pack changes came out of the leak sweep and were made in the generator: the return guidance is now `guia_presentacio_declaracio_trimestral_2024-01.pdf` (the `_v3` suffix tripped the file-name sweep), and the order's watch list and both bulletins print each section as municipality, district, INE municipality code, district number and section number, with a sentence that the 10-digit code chains the last three (the verifier's bulletin parser rebuilt to match). Rebuilt with `ship.py`: 120 assertions green, two scratch builds and the task folder byte-identical, verifier green (15,031 checks), generator and verifier agreeing on 205 figures, goldens unchanged byte for byte. `leak.py --asof 2026-09-30`: REVIEW, answered below. `guard.py surface`: one promoted pair, task62, promoted on the card-level same-driver signature (gap time, pattern A, etl_conformance) already differentiated on the card at the draw, with surface similarity 0.069 at the corpus's 28th percentile, so there is no rename or regeneration to make; the three exchange-note and notice personas the pack names (Flor Segarra, Jose Nevado, Rosaura Rodrigo) are now on the card. `guard.py heart`: PASS (nearest 0.06; one NOTE, the task62 signature, differentiated). Card updated (stump, answer, deliverables, people) and `guard.py validate` clean.

## Leak review

`leak.py task130 --asof 2026-09-30`, verdict REVIEW, 82 lines, each class answered once with the files it covers.

- Section codes in `annex_designacio_2026.xlsx` (13 lines), `cadastre_habitatges_extracte_20260928.csv` (13), `padro_lliurament_2026-06.csv` (13), `padro_lliurament_2026-09.csv` (10): the watch-list sections are the row key of every per-section file; a code names a candidate and says nothing about which side of the line it falls on.
- Section codes in `fiances_lloguer_seccions_2025.csv` (13) and `inspeccions_habitatge_buit_2025.csv` (13): distractors keyed by section like the rest of the pack's registers; neither carries a large-holder share or a designation.
- `butlleti_parc_residencial_2026T2.pdf`, 205 and 165: the 30 June large-holder counts of 4625001012 and 0301402014, which the bridges start from by design (the bulletin is the control R2 reproduces).
- `butlleti_parc_residencial_2026T1.pdf`, 165: 0301401008's 31 March count, a coincidence with 0301402014's 30 June figure.
- `annex_designacio_2026.xlsx` as a ranking artifact: the closed 2026 designation, labelled as holdings on 1 January 2026; it designates eight sections and differs from the 2027 answer on four, so it ranks nothing on the 2027 question (the calibration form).
- `declaracions_grans_tenidors_2024T3_2026T2.csv`, 177 dates after 30 September: every one is `data_transmissio_prevista`, the deed date a signed sale contract schedules, forward by design.
- `index_expedient_designacio_2027.csv`, 5 dates after 30 September: the file dates of the extracts taken 1 to 5 October of records cut at 30 September.
- `registre_grans_tenidors_20261001.xlsx`, 5 dates after 30 September: group links annotated in September with effective dates of 1 October, 15 and 16 November, 13 December and 1 March 2027 (the ask B device), plus the extraction date of 1 October.

## Tried and rejected

- The blueprint's stated-memo architecture (a methodology memo fixing the holdings rows, the amendment semantics, the unit-by-filing-date rule, CUSIP repair and the denominator source): rejected because a strong solver implements every stated clause, so the bridge becomes a computation; its traps are kept only as lower rungs.
- Capital-markets ownership kept literally (13F holders, issuers, shares outstanding) under an accepted domain label (Accounting, Audit & Forensic, Business & Operations, a nonprofit investor coalition): rejected, markets trading is outside Economics and none of the nine owns a vendor's crowding flag without a relabel a reviewer would not accept.
- Confidentially omitted holdings recovered from another public disclosure as the decisive rung: rejected on the clean-data test, the public returns are a filtered file whose repair hands the natural pipeline the answer (sole_data_defect yes).
- Denominator timing (dwellings or shares outstanding taken at a later date than the holdings) as the decisive rung: rejected on the clean-data test (a stale file whose repair collapses the task) and as a single-fact flip.
- Holders whose returns are not yet due completed from the title register: rejected, the incomplete feed is a suspect file under the clean-data test, and the register-to-titles route is a schema-visible two-hop join a strong solver takes.
- Double reporting under a non-exclusive holding definition (a parent and its vehicle, a trustee and its beneficiary both returning the same dwellings): rejected, the regime text that makes both returns correct concedes the overlap, and dwelling-level returns are deduplicated by reference by default.
- Agent-filed returns and nominee title holders (the registrant is not the owner) as the decisive rung: rejected as a lens swap, registrant against owner of the same dwellings on the same date.
- Employer concentration with PEO look-through as the re-skin: rejected, it drops the ownership scenario and co-employment look-through is textbook, announced by the industry code.
- Passive holders re-derived at a forward date around an index change: rejected, out-of-scope domain and an index deletion's passive selling is textbook.
- The agency's takeovers evidenced by preventive annotations in the deed extract: rejected, the evidence would sit in the forward roll's own source, and a solver choosing which entry types to apply reads the annotation type.
- The first-offer move deciding only P, S and Q (the draw's sketch): rejected at design, eleven sections' 1 January figures were then identical under R3 and handed the mirror response 33 annex cells; the agency now touches twelve sections.
- Settled large-holder takeovers as the clock's evidence: rejected, a taken-over agreement scheduled in an earlier return and completed to the agency on another date is a back-test mismatch that sends the solver to the ledger; the clock is pinned by small owners' sales, which touch no return.
- The programme order naming the first-offer programme: rejected, a sentence in the document that defines the quantity sends every solver looking for exercises.
- A bridge from the raw lodged rows to the conformed total (the source note's bridge): rejected, every bar is a lower-rung conformance step both top responses execute, so it is free weight; the bridge now walks the 30 June bulletin figure to 1 January month by month.
- A bridge with one bar per kind of movement: rejected, the taxonomy of kinds is a Gate C fork two correct solvers split on; calendar months are determinate.
- The annex's dwelling-count and designated columns: dropped, the cadastre count is free to every response and the flag hands the mirror eleven cells.
- A region-wide large-holder total on 1 January as an ask, with the agency's effect netted to zero across the region: rejected, it is a figure for another population (H18) and the netting is a construction with no use behind it.
- Advocate notes from the agency's head of acquisitions: rejected, any voice from the agency about its purchases names the mechanism.
- Stage 3a: the reporting-quarter reading of the unit change as a measured fork (the plan's assertion that it misses the bulletin on 3 or more sections): dropped, every row's shape (parcel and units, or a 20-character reference) says which unit it carries, so the reading has no purchase on any row; closed by convergence instead, asserting that shape follows lodgement date.
- Stage 3a: malformed references sitting only in sections far from the line: skipping the repair still filed the answer set at R5, so the repair carried no weight on the call; five malformed references now sit in Q's 30 June picture.
- Stage 3a: the ask B no-roll stop built on the leading groups' single-dwelling sales: it moved the leading group's count by 1 in eight sections, inside any band a grader would grant; the leading group now buys 4 dwellings from a small holder in July to September, count-neutral for every rung.
- Stage 3a: the "takeovers only in P, S and Q" partial cell as a wrong-set cell: it files the answer set, because the other nine sections the agency touches never cross the line; it stays in the grid as a counts-only miss (nine sections' figures wrong).
- Stage 3a: a region total of large-holder dwellings in the bulletin: it landed on a round 2,500, a generation tell; the bulletin now states only the cadastre total of the fourteen sections.
- Stage 3b: the watch list printed as 10-digit section codes in the order and both bulletins: `leak.py` reads every code in the answer as a golden figure, so three filed documents came back LEAK although a code names a candidate and decides nothing; the printed lists now carry municipality code, district and section, with a sentence that the 10-digit code chains them, and the data files keep the 10-digit key.
