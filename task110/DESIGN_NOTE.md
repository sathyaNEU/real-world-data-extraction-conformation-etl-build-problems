# task110 design note

## Axis tags

- Domain: Accounting, Audit & Forensic Analytics (author-declared new domain, 2026-10-06; added to
  `fingerprint/vocab.json` the same way the two 2026-10-03 domains were). The client roster on file
  lists six domains, so the tag risk sits with the author.
- Subdomain: fixed assets and leases.
- Objective: Data Extraction & Conformation (ETL). The deliverable is Yacaaba Radiology's conformed
  load file, and the committed figure is what the group ledger posts from that file.

## DRAW

| Axis | Draw |
|---|---|
| Niche | internal audit's re-performance of the last legacy fixed-asset register to migrate: Yacaaba Radiology (four NSW sites, a spreadsheet register kept by its external accountant) loads to the Quandong Imaging Group ledger at 1 January 2027; Bremer and Strzelecki went live at 1 July 2026 and Bremer's load is the precedent |
| Gap | population (an upgrade's depreciable horizon belongs to the system it is fitted to, not to its register row), then rule (Yacaaba's legacy practice is recovered from its own postings) |
| Pattern | B, with a reproduction clause as the gate |
| Generators | G16, G2, G19 |
| Gate G | etl_conformance |
| Calibration form | parallel_run_overlap (the legacy depreciation journals for July 2025 to September 2026 and both trial balance runs, which since harden loop 3 certify the five-year path as exactly as the answer) and a prior-period close-out (note 9's 2024 comparative in the FY2025 report, which only the answer reproduces) |
| Context artifact | register (Yacaaba's asset register workbook) |
| Role | the group's internal audit manager signing the migration off for the CFO's go/no-go (compliance_or_audit) |
| Forum, forcing event, org family | executive team (the CFO's go/no-go), cutover, hospital or health provider |
| Decision type, unit | conformed dataset, AUD |
| Shape | 03, bridge between two totals (each site's book value walked from 30 September through October to December to the load, then the January to June charge), with the class book values beside it |
| Deliverables | `fa_load_2027-01-01.csv`, `cutover_signoff.docx` |
| Opening move | other: a request for help ("I need your help signing off ..."), one paragraph, not in the vocab (rule-first until harden loop 1, when the replay clause left the prompt; situation-first until the portal sent the spec-voice prompt back) |
| World | Australia (NSW, Hunter region), AUD, June year end, as-of 13 October 2026 |
| People (guard.py names --geo Australia --seed 110) | Cynthia Rice (internal audit manager, the prompt's voice), Timothy Hill (CFO), Lorraine Wright (Yacaaba's former external accountant), Ronald Lawrence (finance systems lead), Donna Ramirez (practice manager) |

Guard: PASS on 2026-10-06 after one redraw; re-checked and re-registered after the re-scope with one
WARN, answered here: `repeat.gate_g` against task109, an ETL build in another author-declared
domain drawn the same day. Both carry `etl_conformance` because both objectives are ETL; the
decisive mechanisms differ (task109 has no Part 2 pattern and turns on a time and population gap in
a hotel's work sessions; this build is pattern B under a replay gate on a ledger).

## Gate G

- Litmus: no reported number or stakeholder conclusion is overturned. Every filed figure is correct:
  the register's categories, the rate card (which carries no rate for Equipment upgrades), the GL
  postings, both trial balance runs, the FY2025 notes, the capital approvals. The difficulty is
  constructing, for each upgrade, the horizon Yacaaba's ledger actually used, a property of another
  row (the system it was fitted to) reached through the capital approvals register. Since harden
  loop 3 the replay accepts the five-year path as well, so the horizon is pinned by the practice's
  own published 2024 depreciation (note 9's comparative), not by the replay.
- Primary mechanism: `etl_conformance`, with `method_or_model_selection` support (the horizon rule
  is the unique survivor of the replay).
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- Delete every wrong number from the pack: there are none to delete, and it is still hard.
- Clean-data test: the suspect file is the register, which records no system link and no horizon.
  Adding the link leaves the answer and the five-year path unchanged; only a register that recorded
  each upgrade's horizon would collapse the task, and no system records that (the accountant's
  workings are her firm's papers and were never handed over).
- Lens-swap test: the five-year path and the answer are not one population under two lenses. The
  answer needs a second entity per upgrade (its host), that entity's own schedule and a join
  through a third file.

## Entity, unit of value, decision

- Yacaaba's ledger depreciated every asset straight line from the month it was bought, rounded to
  the cent each month with the last month taking the remainder. Equipment upgrades (coil packages,
  detectors, software platforms, digital retrofits) were spread over the months their system had
  left. The register files them as their own rows under Equipment upgrades, a category with no rate
  on the card; stand-alone options and accessories carry 20 per cent.
- Two quantities that read as an upgrade's life: a single standard life (five years fits best) and
  the host's remaining months at the upgrade date. They disagree in both directions (an upgrade on
  an old system ends early, one on a young system runs long), and the upgrade invoices are set
  (`world.net_upgrades`) so the mix nets to the cent in every month and at every balance date the
  replay and the trial balances carry. The two readings part only in FY2024, when four upgrades
  started part-way through the year, which is the year note 9's comparative publishes.
- Decision: the January to June 2027 depreciation the group ledger will post on Yacaaba's register
  as loaded at 1 January 2027 (FIN-STD-014 section 6), committed for the reforecast and the go/no-go.

## The stump sentence

A competent solver cleans Yacaaba's register, recovers the ledger's conventions (full month in the
month bought, computer equipment moved to four years prospectively, the June 2025 impairment, the
Bremer Voluson's brought-forward depreciation), sweeps a single life for the unrated Equipment
upgrades and finds that five years (the rate the card gives options and accessories, and Bremer's
precedent) replays all 90 account-months and ties both trial balance runs to the cent, stops at the
first control that passes, and files a January to June 2027 charge of $1,133,471, 22 per cent high;
only note 9's 2024 comparative in the FY2025 report refuses five years, its imaging depreciation
$8,901 short, and only each upgrade on its system's remaining months reproduces it, which puts six
upgrades on systems that ran out between October and December 2026 at nil book value.

## The ladder (measured, `generator/build_report.txt`)

| Rung | Construction | Jan-Jun 2027 charge | vs answer | Killed by |
|---|---|---|---|---|
| R0 | the register as delivered: tracked items and repeated lines in, computer equipment on four years throughout, no impairment, the Bremer Voluson read as new, upgrades five years | $1,142,519 | +22.7% | cost does not tie to the trial balance |
| R1 | cleaned to the ledger's cost, rules unapplied | $1,140,748 | +22.5% | the computer and imaging accounts miss every month; accumulated misses by the Voluson's brought-forward $134,362 |
| R2 | plus the life change, the impairment and the brought-forward: the five-year path | $1,133,471 | +21.7% | replays every account-month and both trial balance runs to the cent; only note 9's 2024 imaging depreciation refuses it ($8,901 short); the stop |
| R3 | the five-year path, each upgrade stopped when its system's life ends | $993,555 | +6.7% | replays every cell too; refused by the same 2024 figure |
| R3b | five years unless the system runs out sooner (min of 60 months and the host's remaining months) | $981,803 | +5.4% | misses every imaging month |
| Answer | each upgrade over its system's remaining months | $931,458 | | replays all 90 account-months, both trial balance runs and both years of note 9 |

- Sign: every correction walks the figure down and the answer is the minimum of the grid (L5).
- R0 to R2 are hazards on the main figure (each under 1 per cent); they matter to the replay and the
  tie-outs, and the decisive move is worth 22 per cent.
- The grader accepts the main figure within plus or minus 1.5 per cent, so the two cells the replay
  certifies sit at +21.7 and +6.7 per cent (asserted at 5 or more). Four cells sit near the answer
  and are recorded rather than separated, all of them failing the replay: ten years for the upgrades
  at $950,220 (+2.0%), which misses the imaging account by $30,541.96 every month and its balance by
  $1,317,985; the host's whole remaining years rounded to nearest at $984,846 (+5.7%); and the right
  construction with a counting slip, the host's months without the upgrade month at $930,318 (-0.1%)
  and the host's remaining life cut to whole years at $936,168 (+0.5%), a cracker's near misses
  inside the tolerance.
- Why R2 is satisfying to stop at: every account-month and both trial balance runs reproduce to the
  cent, sixty months is the only single life that does, and it is the card's options and
  accessories rate and Bremer's precedent.

## Survival properties of the decisive rung

1. No shipped sentence states or invites it: the card has no upgrade rate, the FY2025 policy note
   lists rates for the other categories, and Bremer's precedent load carries its sub-numbered
   upgrades on their own five years (true of Bremer). Round 1 showed two sentences did invite it, the
   prompt restating the replay gate and an Existing Asset key on Upgrade rows defined as the equipment
   a request upgrades; since harden loop 1 the gate is stated only in FIN-STD-014 section 4, Existing
   Asset keys only retirements, and an upgrade's system is named only in its request text (system and
   site), which every text reading resolves to one in-service system (asserted both sides).
2. The replay and the trial balances nominate five years exactly (sixty months is the only single
   life that reproduces them, asserted) and are blind to the host horizon; only note 9's 2024
   comparative, one whole-dollar cell, refuses five years.
3. Arithmetic symptom: none on the replay or the balances. Five years ties every account-month and
   both trial balance runs to the cent (asserted, and re-derived by the verifier from the bundle).
   The only symptom is note 9's 2024 imaging depreciation, $8,901 short on the five-year path, in a
   published comparative the replay gate does not name. A solver whose first guess is the imaging
   category's 120 months misses by a constant $30,541.96 a month, and the single-life sweep then
   settles on sixty months exactly, which is the stop.
4. Not a per-row predicate: the horizon is a property of a different row reached through the
   approvals' Existing Asset field.
5. Enumeration is a construction from the host's own schedule.
6. No dated event drives it.
7. Survives the deletion.

## Determinism: the 22 axes

| # | Axis | Closure |
|---|---|---|
| 1 | Population | C1/C2: the register cleaned to the ledger's cost (Capitalised N items and repeated invoice lines out, the cost tie pins it), disposals out, nil-book-value assets not sighted written off (FIN-PRO-022 section 6); every write-off is already at nil on 30 September and charges nothing in October to December, so the site walk reads the same from what loads or from everything on site (asserted) |
| 2 | Unit of account | C2: one register row is one asset; an upgrade's horizon comes from its host, pinned by the replay and the trial balances together with note 9's 2024 comparative: the host horizon is the only member of the swept family (single lives of 24 to 120 months, five years stopped with the host, five years unless the host runs out sooner, the host's months less one, the host's full class life, the host's months in whole years either way) that reproduces all three, asserted in the generator and re-derived in the verifier |
| 3 | Attribution window | pinned: January to June 2027, a full month in January (FIN-STD-014 section 6) |
| 4 | As-of dating | the register as exported on 2 October 2026 (FIN-STD-014 section 2); balances of record are the last run before the September lock (section 5), the 9 October run |
| 5 | Version basis | the approved mapping (v2), the log marks v3 as issued for review |
| 6 | Divisor | remaining whole months (section 6) |
| 7 | Weighting | none |
| 8 | Measurement window | fixed by section 4 (July 2025 to September 2026); note 9 adds the 2024 and 2025 years as published figures, and no upgrade schedule starts or ends inside the replay on any of the three readings (asserted) |
| 9 | Boundary inclusivity | the cut-off is 5:00 pm local on 9 October; the last valid Friday scan is at 4:33 pm and the late scans run from 5:10 pm to 5:49 pm, so no reading of the cut-off's edge moves a scan |
| 10 | Rounding path | C2: per asset per month, half up, last month takes the remainder; whole dollars in the note from the cent figures, and every table foots (asserted) |
| 11 | Tie-break | none needed |
| 12 | Maturity | not applicable |
| 13 | Order of operations | impairment then re-spread; life change then re-spread; both pinned by the replay |
| 14 | Row order | invariant (asserted by the verifier's own construction) |
| 15 | Duplicate resolution | repeated invoice lines (same invoice, serial, cost, date, description) collapse to the lower number; the cost tie pins it |
| 16 | Identity normalisation | tags exact; serial where the tag is blank (FIN-PRO-022 section 2) |
| 17 | Netting | none |
| 18 | Dimensional units | AUD ex GST throughout |
| 19 | Code and status semantics | Capitalised Y/N and Status defined in the extract notes |
| 20 | Integerisation | months, whole |
| 21 | Scope of a clause | FIN-STD-014 section 3 governs migrated assets; FIN-POL-006 only assets bought after cutover |
| 22 | Forward window contents | pinned in the prompt and section 2: the register as loaded, nothing bought or sold after cutover |

Bins: every graded dollar figure sits at least three cents from the half-dollar and off any round
thousand, the tables foot and the write-up is rendered from the solution (asserted, 334 assertions in all, and the verifier re-derives every figure from the files).

## Ask sheet

Main call population: assets loading at 1 January 2027 with remaining life, their register rows,
the depreciation journal lines, the trial balances' cost and accumulated lines, the approvals links,
the rate card, the FY2025 notes. No device moves the main call (asserted for every device).

| Ask | Construction layer | Devices (measured moves) | How it enters the call |
|---|---|---|---|
| Per site: book value 30 Sep, Oct-Dec depreciation, book value loaded, Jan-Jun charge (16) | differs at every site on the five-year path (CHA, MAI, CES, RAY all hold upgrades) | site of record from the scans and the count sheet (left on the register site: CHA charge -$7,708, MAI +$28,318, CES -$15,810, RAY -$4,799); the DST cut-off read at a fixed +10 (MAI and CES book value loaded +$78,252 and -$79,901); the Raymond Terrace sheet ignored (CHA and RAY charges +/-$5,093) | a split of the committed figure and the walk of the load it is computed on |
| Per site: assets with nothing left to depreciate, count and original cost (8) | six upgrades at CHA and MAI are nil only on the host horizon | DST (CHA +2, MAI +2, CES +1 count); tag-only join (CHA -3, MAI -3 including the Maitland MRI at $2.0m of cost, CES -2); no count sheet (RAY -12); register site (CES +1, CHA +2, MAI -3) | the part of the load that posts nothing |
| Book value by group class (6) | imaging differs on the five-year path | mapping v3 (folds ultrasound into imaging and vehicles into furniture); the first trial balance run (joinery under furniture, about $20k); the Voluson read as new (clinical +$134k) | the class split of the load the call is computed on |

Pair arithmetic, on paper: a mirror on the five-year path loses all 16 site walk figures, the CHA and
MAI nil cells and the imaging class on construction, so it keeps at most the CES and RAY nil cells
and five class figures, and only by handling every device. A cracker who misses the site-of-record
rule loses every site figure. The solver rounds measure both.

## Criteria arithmetic

Main call 1 + per-site walk 16 + per-site nil 8 + class book values 6 = 31, plus the load file's row
count and column totals (2 to 5) and the chart (2 to 3): about 36.

## Stopping rule (written before the portal)

- Harden loop 3 is the last on this architecture. If a solver round or the portal puts a response
  on the call (within the grader's plus or minus 1.5 per cent), the world is at ceiling and the slot
  is re-rooted at stage 1, with this architecture moved into the card's lineage.
- No response on the call and the pair under 50: pass, nothing touched.
- Responses at $1,133,471 or $993,555: the false confirmation held; read the asks for which
  devices were handled.

## Leak read (leak.py, 13 October 2026 as-of): REVIEW lines answered

- `fa_migration_standard.pdf` shares six of nine words of the committed call: it is the standard
  that defines the group ledger's depreciation from cutover, and it carries no figure.
- Stump vocabulary in the FY2025 extract (upgrades, imaging): the class label "including upgrades,
  options and accessories"; no rate or horizon for upgrades is stated anywhere. Note 9's 2024
  comparative is a second table in the 2025 table's layout and names no rule, no horizon and no
  upgrade.
- Stump vocabulary in the extract notes (imaging, balance, Bremer, account): field definitions;
  Existing Asset is defined for retirements only, and nothing names the upgrade link or a life.
- Stump vocabulary in the verification procedure (window, licence, inside) and the standard (balance,
  residual, schedule): the documents' own section words.

## Ask layer, loop 2: the handheld export

Portal result on the harden-loop-1 pack (2026-10-07): top two 84 and 24. The 84 response failed only
criterion 1 (the committed sentence) and passed all 26 others, so it held the host-horizon
construction; read it as near 99 on a regrade. The main ladder is left as it is on purpose (three
solvers on two pack versions read the horizon), and the ask layer takes the weight instead. The
rubric's site criteria (16 to 21) each name all four sites, so one asset misplaced fails the
criterion, and criteria 2 to 4 turn only on which assets load.

Two devices in the scan export, answer-neutral (golden figures, both deliverables and the
submission byte-identical; 320 assertions; verifier recomputes both from the bundle):

| Device | Planted | Organ (documentary / structural) | Wrong reading and what it moves | Rubric cost |
|---|---|---|---|---|
| Label on the wrong unit (D7) | Laptop 1232 (moved CES to CHA) scanned once at CHA wearing laptop 1171's tag with its own plate keyed; 1171 sighted on its plate | FIN-PRO-022 s2 (tag or plate, and a plate scan sights the asset that carries it; the old "where the tag is missing" condition removed so a readable tag cannot govern) / the one scan whose tag and plate name different units | Tag before plate: 1232 unsighted, loads at CES; CHA and CES walk move ($1,243 Sep book value, $129 Oct-Dec, $1,114 load, $257 Jan-Jun) | 16-19, 21 points |
| HH-07 clock (D8, interior) | HH-07 ran on its factory clock on Thursday 8 Oct, so its Cessnock scans read 1 January 2025; filing compactus 1157 (moved CHA to CES) and reception chairs 1006 (nil) sighted only then; trial scans at MAI on 25 Sep include 1010 (nil, never sighted in the window) | FIN-PRO-022 s1, a sighting counts only inside the window, and the extract notes' scan_id, the handheld's own running number / the run sits between HH-07's Wednesday and Friday scans and includes an asset bought after the date the clock shows | No window start: 1010 loads (203 rows, MAI nil +1 / +$5,279). Window applied to the clock as written: 1006 written off and 1157 left at CHA (201 rows, cost and AD -$4,058, CES nil -1, CHA and CES walk -$4,592 Sep book value) | no start: 2, 3, 4, 20, 21, 30 points; clock as written: those plus 16-19, 51 points |

Pair sheets on the generated rubric (99 points), the strong response otherwise perfect: every
path but the fully right one loses at least 21, the habitual one (window applied, clock trusted)
loses 51 and files 48; with the second response at 24 the pair averages 36. A response that
never applies the window start leaves the clock device inert (the 2025 rows pass) and pays only
the trial device: 30 lost, files 69, pair 46.5, under the bar and short of the target. Separation: every
wrong reading leaves the Jan-Jun figure to the cent (asserted per reading); the devices move only
site attribution or the load status of assets at nil. Over-cleaning prices too: dropping all of
HH-07, or every scan whose tag and plate disagree, lands on a wrong stop.

## Harden log

- Loop 1 (2026-10-07), after round 1 (plain) landed $951,870 and every ask: the announcements of the
  decisive join were removed, answer-neutral (golden figures and both deliverables byte-identical,
  259 assertions, verifier clean). The prompt no longer states the replay gate (FIN-STD-014 section
  4 carries it alone), Existing Asset is blank on Upgrade rows and defined for retirements only, and
  submission step 3 cites the request text. Brief the round tests: a solver whose 120-month rebuild
  misses the imaging account has no key column to the host and has to build the link from text.
  Stopping rule: if round 2 (plain) lands $951,870 again, the architecture is at ceiling and is
  re-rooted, not hardened a second time.
- Loop 2 (2026-10-08), ask layer, after the portal's 84 and 24 on the loop-1 pack: the handheld
  export devices above. The main ladder untouched. Stopping rule: if a solver round's top response
  still passes criteria 2 to 4 and 16 to 21, the scan-export devices read as work orders and the
  ask layer moves to a different file family rather than a third device in this one.

- Loop 3 (2026-10-10), after the one-paragraph prompt's run put both responses on the call (one at
  $951,870.13, one at +0.07 per cent, inside the grader's 1.5 per cent tolerance): the replay is turned
  from an alarm into a false confirmation. The upgrade invoices are netted (`world.net_upgrades`, ten
  upgrades moved by up to about $90,000, the Maitland MRI moved from October to November 2016 so no
  host-horizon schedule ends inside the replay) so the five-year path replays all 90 account-months
  and ties both trial balance runs to the cent, and note 9 gains its 2024 comparative, the one shipped
  control that refuses five years. The answer moves to $931,458. The prompt is the author's "I want"
  request. Stopping rule above: this is the last loop on the architecture.

## Tried and rejected

- Indiana Transparency Portal state asset file (237,664 real asset rows with acquisition date and
  cost) as the spine: rejected, the Indiana Data Hub terms of use grant only a personal, news,
  nonprofit or academic licence and bar redistribution and derivative works, and the dataset
  carries no licence of its own.
- First card (gap rule, pattern B, Gate G method_or_model_selection): BLOCK on
  test.same_driver_older, that triple is spent in twelve earlier builds. Redrawn to gap population
  first (which is the honest decisive gap, the unit), Gate G etl_conformance, and the forum moved
  from committee_or_panel (27 uses) to executive_team.
- Three practices in scope at one cutover (Bremer, Gippsland and Hunter all loading at 1 January
  2027, graded on the group's January to June 2027 charge): rejected after the prototype, because
  the upgrades' higher rates and their earlier ends net out and the decisive move was worth 1 to 3
  per cent of the group charge (a 2.44m charge moving by 31k to 89k). Re-scoped to Hunter as the
  last practice to migrate, with Bremer and Gippsland already live from 1 July 2026 as the closed
  precedent.
- Hunter upgrades on their own ten-year imaging life as the natural path: it leaves a 1.65m gap on
  the 30 September 2026 accumulated depreciation balance, which a migration tie-out finds at once
  and which is sized like the upgrades' book value, so it is a work order rather than a stump.
- A four-year lure rate: upgrades started between August 2021 and October 2022 finish their
  four-year schedule inside the replay window, so the residual steps by 13k to 45k a month and
  points at the assets; five years keeps every lure schedule clear of the window.
- An upgrade starting inside the window (a stereotactic biopsy kit on the Charlestown mammography
  unit, January 2026): its residual step identifies its implied life (25 months), which equals its
  host's remaining months, so the step hands the rule over. No upgrade starts or ends inside the
  window.
- Short-horizon recent upgrades (tube replacements and software on old CTs and MRIs, 21 to 28
  months left): each adds 2k to 6k a month of residual that no realistic long-horizon mass can
  offset, so the five-year path could not tie the balances. Upgrades sit at 37 to 106 months.
- The Charlestown 3T MRI platform upgrade and the Charlestown X-ray room 2 retrofit in late 2021 or
  January 2022: their five-year schedules end in late 2026, so the five-year path charges nothing in
  2027 while the host horizon still does, which pulls the five-year path toward the answer.
- Shape 07 (grid of sites by measure): blocked on ban.shape after task109 registered shape 07 the
  same day; the criteria are re-homed on the balance-to-load walk by group class (shape 03), with
  the site table beside it.
- Sarah Hughes as the internal audit manager: first name used in task108; replaced by Cynthia Rice
  from the same seed-110 draw.
- A filed five-year rate for the upgrades ("Upgrades & options 20%" on the rate card and in the FY2025
  policy note, with the ledger depreciating installed upgrades over their host's remaining life):
  rejected before any file was cut, because a filed rate that misstates how the ledger treated the
  decisive rows is the judge's wrong-methodology-artifact refutation (Gate G, surface read). Installed
  upgrades now sit in their own register category, Equipment upgrades, with no rate on the card or in
  the note; stand-alone items are Options & accessories at 20 per cent. Five years is now the
  solver's own best constant-life fit to the replay, not a filed statement.
- Write-off candidates chosen by nil book value at 31 December: two of them (a Cessnock bed ending
  October 2026, a Charlestown laptop ending December 2026) still carried $68 and $71 at 30 September
  and charged it in October to December, which gave the per-site walk two readings (start from what
  loads, or from everything on site and deduct the write-offs). Write-off picks are now drawn from
  assets already at nil on 30 September, and the generator asserts it.

- The v1 pack as cut, solver round 1 (plain, 2026-10-07): landed $951,870 and every ask figure.
  Its own path sentence: "Upgrades run to the end of the parent asset's 120-month life, using
  Existing Asset in the capital approvals file." It never stood on the five-year stop: its first
  rebuild put the unrated upgrades on the imaging category's 120 months, the imaging account missed
  by a constant $34,180.36 a month while every other account tied, and the next call joined the
  register's Approval Ref to the approvals' Existing Asset and tested host, 60 and 120 against that
  residual at once. Announced by three sentences: the prompt's opening (the to-the-cent replay
  stated in the prompt), the approvals' Existing Asset key on Upgrade rows, and the extract notes
  defining that field as "the equipment the request replaces or upgrades".
- Harden loop 1 (announcements removed: no replay clause in the prompt, no Existing Asset key on
  Upgrade rows), solver round 2 (plain, 2026-10-07): landed $951,870 and every ask figure again.
  Its path sentence: "Equipment upgrades run to the end of the host system's 120-month life (hosts
  taken from the approvals text)." It fitted the imaging account's monthly totals as a target and
  typed the sixteen upgrade-to-host pairs by hand from the request text, so moving the key into
  prose cost it nothing. With FIN-STD-014's exact replay in the pack, the one unknown on the imaging
  account is solvable against a to-the-cent target whatever the link's form: the architecture is at
  ceiling, and the stopping rule in the harden log calls a re-root.
- The spec-voice prompt (portal, 2026-10-10, sent back on the prompt alone with the stump, rubric and
  determinism passing): each file arrived as a definition ("fa_load_2027-01-01.csv is the load, in
  cents, one row per asset that loads: ...") and the note as verbless fragments, with the role, the
  CFO and the go/no-go cut, so the reviewer read it as telling the model how to build the files
  rather than asking for help with them. Rewritten as a request, every graded element kept; "in
  cents" became "in dollars and cents", which is what the golden CSV carries.
- The harden-loop-2 pack's main ladder, re-run on the one-paragraph prompt (2026-10-10, two responses):
  both landed the call inside the grader's +/-1.5 per cent tolerance, one at $951,870.13 and one at
  $952,537.33 (+0.07 per cent), and both loaded 200 rows (the HH-07 clock device held on both). Five
  solves out of five on the host horizon: the five-year path's constant ~$375 a month miss on the
  imaging account is an alarm under section 4, and every solver chases it to the hosts. The
  tolerance also puts the near-miss cells (host months without the upgrade month at -0.09 per cent,
  whole host years at +0.6 per cent) on the call.
- The per-site nil ask worded "how many assets come across with nothing left to depreciate and what
  they originally cost" (prompt review, 2026-10-10, P2 FAIL): the cost clause presupposes a non-zero
  count, so the prompt states a fact about the register before a file is opened. Reworded to ask
  whether any do and, if so, how many and their original cost. The ask, its criteria and every golden
  figure are unchanged, because every site loads some (28, 24, 5 and 13) on the golden path and on
  every device reading in the ask sheet.
- The provenance file opening "Every file in this folder was constructed for this exercise ... are
  invented" (portal Input Asset Quality, 2026-10-10, authorship FAIL, authoring_tell): stepping
  outside the fiction breaks the premise of both deliverables. Rewritten in the generator as Finance
  Systems' own compile note (compiled 13 October 2026, CC BY 4.0, real names used descriptively). Only
  that file and target.zip changed; 334 assertions and the verifier green, the golden byte-identical.
  The world is constructed, and that is recorded here and in the card, never in target/.
