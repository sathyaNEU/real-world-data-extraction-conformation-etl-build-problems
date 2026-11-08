# task118 design note, architecture 6

The slot's sixth architecture: a city-region rail executive siting the one platform dispatch team its 2027 rail plan
funds, in a new client domain, world, dataset, generator and prompt shell. Architecture 5 (a city utility's demand
response, read on consecutive event days) is spent on its first portal round; its card entry moves to the lineage.
Earlier architectures' notes live in git history and in `## Tried and rejected` below. The author's five conditions of
2026-11-07 (task127 and task306) are met here: the field's method done carefully files the wrong call; no fit,
back-test or reconciliation picks the golden route (the one validation on file confirms the easy route); the asks ride
reconstructions across two systems no sentence states; the ladder keeps every cheap route off the call; the three rules
are written below.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task118.json`, architecture v6. **Pairing:** client domain
  urban-regional-science, task type `optimization` (serves OS: siting under a stated objective), objective
  opportunity-sizing-decision. The headline is a sized opportunity: from the dwell minutes each shortlisted station's
  trains run over their timetabled dwell (the pool) to the passenger lateness one dispatch team, removing three fifths
  of those minutes in its hours, would take off the network's weekday trains (the realisable), and the sized figures
  drive the pick.
- **Shape:** 01, a ranked list under a cap of one: each shortlisted station's weekday saving (6), the pick, the
  runner-up and the gap (3), and the asks (designed at stage 2: each station's overrun minutes by period, each line's
  passenger lateness at the city terminus by period, the units in passenger service by line at two clock times).
- **Strategy and labels:** `decomposition_attribution` (the network's passenger lateness is attributed to the dwell
  overruns that start it, through every train and unit it reaches), Gate G `decomposition_attribution`, gap objective
  then time (the local overrun minutes are right and are not what the plan prices; the lateness travels on in time),
  pattern none, generators G1 (the unit of value is network passenger lateness, not the station's train-minutes), G7
  (the turnround slack is the operating window that decides whether lateness passes on), G3 (the unit that actually
  worked each train, from the running record, not the planned diagram). Layer 2 `estimand_identification` (the right
  counterfactual), pattern `own:network-lateness-through-unit-turnrounds` (the urban optimization cards site on a
  stated objective; none carries delay through vehicles).
- **World:** Ravelstoke Rail, the rail executive of the Ravelstoke City Region Combined Authority (an invented city
  region in the north of England, GBP), which specifies and funds the suburban network that Cardale Railways Ltd runs
  under a concession. Three lines run into Ravelstoke Central: the Crossmoor line, the Ambrey line (to Ravelstoke
  Airport, with the morning park-and-ride extras from Ambrey Parkway) and the Holm Ferry line. The 2027 rail plan funds
  one platform dispatch team; the shortlist is Ostley Lane and Brathwick Road (Crossmoor line), Ambrey Parkway and
  Pellingham (Ambrey line), Holcroft Green and Saltgate (Holm Ferry line). A 2025 trial team ran at Quayside (Holm
  Ferry line) and Cardale closed it out.
- **Furniture, drawn and checked:** forum `minister_or_cabinet` (the Mayor adopts the 2027 Rail Plan), forcing
  `cutover_or_migration` (the team starts with the May 2027 timetable change), org `local_government`, role
  `capacity_planner`, artifact `filed_standard` (the rail executive's dispatch team brief files the WHAT), calibration
  `prior_period_close_out` (Cardale's close-out of the 2025 Quayside trial). Personas from
  `guard.py names --geo "United Kingdom" --seed 118`: Julia Clayton (head of rail performance, Ravelstoke Rail, signs
  the brief), Leon Ross (performance manager, Cardale Railways, signs the close-out).
- **Data-native sentence:** the Ambrey line keeps its morning frequency with ten units by turning each all-stations
  unit at Ravelstoke Central five minutes after it arrives, a minute more than the four-minute minimum turnround, into
  the outbound airport workings that carry the airport's early shifts, while the morning park-and-ride extras from
  Ambrey Parkway run into the sidings once their passengers are off; the running record carries each train's unit, so
  the lateness Pellingham's long dwells put on an inbound train reappears on a full outbound train that never calls
  there, and Ambrey Parkway's longer dwells mostly end in the sidings, but no field, code or sentence says either.
- **Abstraction sentence (stumping Part 6), against the nearest builds on file:** written for this build, "a delay
  removed at one point is worth what it removes from every later assignment of the vehicle that carried it, which only
  the vehicles' own sequences show". Against 303 (a unit's record carries a shared upstream loss found by same-minute
  coincidence across siblings), 120 (a draw rebuilt as inflow less storage), 162 (a device read only in the hours an
  upstream reading crosses a setting) and 307 (users re-routing in equilibrium shrink a local saving), no single
  sentence fits both builds of a pair: here nothing is shared upstream, nothing is stored, no threshold is replayed on
  an exogenous series and no user chooses a path; the saving grows past the local figure because a resource carries the
  lateness into later work. Against task472 (a job's completion released only inside a schedule's windows): there the
  job's own finish is quantised by windows outside it; here the saving lands on other trains, the unit's next workings,
  weighted by their passengers. Not approved, so the heart rule is about drivers, not shells.
- **Shell (redrawn with the world):** question form `which`, the second sentence opening on the workbook ("In ..."),
  the rounding sentence opening on "Passenger-minutes", deliverables `png+xlsx`; the dead shells (how-much, put, give,
  docx+xlsx; what, the note, megawatts, docx+csv) are in `lineage_shells`.
- **Sources, one line each.** The client's two-layer standard (the field's own analysis decides: a siting valued on
  the passenger lateness it removes). Rail performance practice in Great Britain: train running records against the
  working timetable, sectional running times and allowances, minimum turnround times in the timetable planning rules,
  primary and reactionary delay (public domain knowledge; no text copied). The world, every figure and every file are
  synthetic, generated by `generator/build.py` under seed 118.
- **Re-root:** architecture 5's call landed on its first portal round (a run-position covariate, a contract-regime
  split and season-out validation, each a named reflex). This session's screen of the untried ground and the harness
  iterations that shaped this draw are lines in `## Tried and rejected`.

## Survivor anatomy

Actor: the property that decides is where each delayed train's unit goes next and how much of its lateness the turnround leaves, and no file stores it; the running record lists each train's calls and its unit, the timetable lists each working's times, and the next working a train's lateness reaches is a relation between rows (the same unit's next train that day, in time order).
Link: the knock-on is read through the unit number shared by an inbound train's terminus arrival and the same unit's next departure, with the turnround slack (layover less the four-minute minimum) deciding what passes; the key is the unit and the day, and the deciding relation is the slack arithmetic across the turnround and the passengers on the next working, which no column, field or sentence invites.
Reflex: the field's methods for the deciding quantity sit at rungs 0 and 1 and file the wrong station: the dwell minutes a team removes at its station (the operator's delay minutes), the passenger minutes on board, the same-train passenger lateness net of allowances, and that figure scaled by a network, line or line-by-period reactionary ratio.
Back-test: the textbook route validates: Cardale's close-out of the 2025 Quayside trial measured the passenger lateness the team took off the trains calling there, and the same-train route reproduces it, because Quayside's units turn round with slack on the Holm Ferry line and pass on nothing.
Second use: every file the decisive step reads is in the pack for its own reason: the running record is every rung's data and carries the units for the fleet ask, the working timetable and its planning rules give every rung its scheduled times, allowances and dwells, the passenger census weights every rung, and the diagrams serve the fleet ask; deleting the decisive step drops no file.
Shock: the knock-on reads as ordinary lateness: outbound Ambrey line trains leaving Ravelstoke Central a minute or two late in the morning look like any other start-of-journey lateness, the line's averages sit inside the other lines' range, and no candidate stands out on any shipped statistic.
Pins: the dispatch team brief files the WHAT in the rail executive's own genre (the passenger lateness taken off the network's weekday trains, each passenger's minutes after the timetable at the station where they leave the train, valued on the autumn 2026 weekdays as they ran, the team removing three fifths of the time each train's dwell runs over its timetabled dwell at its station in its hours), and no filed sentence names turnrounds, knock-on, reactionary delay, the next working or a unit.

## Default path

1. Read the dispatch team brief: the team goes to one shortlisted station; it is worth the passenger lateness it takes
   off the network's weekday trains, valued on the autumn 2026 weekdays as they ran, the team removing three fifths of
   the time each train's dwell runs over its timetabled dwell at its station between 06:30 and 19:30.
2. From the running record, take each weekday train's arrival and departure at each shortlisted station against the
   working timetable, and the time its dwell ran over the timetabled dwell (net of time waiting for a timetabled
   departure).
3. Replay each train with three fifths of that overrun removed at the candidate station: the train runs each later
   section in its sectional running time and never leaves early, so the timetable's allowances recover part of its
   lateness; take each later station's arrival lateness times the census passengers alighting there.
4. Sum over the record's weekdays and divide by their number; rank the shortlist. A careful version scales each
   station's figure by a reactionary ratio (the network's, its line's, or its line's in that period) taken from the
   record's late starts.

Ends on: Saltgate, about 7,000 passenger-minutes a weekday (Ambrey Parkway next on the line-by-period scaling)
Golden: Pellingham, about 9,000 passenger-minutes a weekday (Saltgate runner-up at about 7,000)

## Stump sentence

The default path prices each shortlisted station's team at the overrun it removes there, carried down the same train
to each passenger's alighting station net of the timetable's allowances, and files Saltgate at about 7,000
passenger-minutes a weekday; the step that lands it there is stopping each train's lateness at Ravelstoke Central,
when the Ambrey line's all-stations units turn round there with a minute of slack and take their lateness straight
into the full outbound airport workings while the Ambrey Parkway extras go to the sidings, so Pellingham's team takes
the most lateness off the network, about 9,000.

## Three rules

Task type: optimization in urban-regional-science, which serves opportunity sizing: siting one team among shortlisted stations under a stated objective, sized from the overrun minutes each station's trains run (the pool) to the passenger lateness the team takes off the network (the realisable).

Domain test: the deciding quantity is each siting's passenger lateness avoided across the network's weekday trains, which rail performance analysis builds from train running records against the working timetable, the timetable's sectional running times and allowances, the minimum turnround in the planning rules, the units each working used and the passengers each train carries between stations.

Swap: "which ward should get the discharge team, valued at the patient waiting it takes off the hospital" keeps the sentence's shape and loses its substance: a ward has no timetable whose allowances absorb lateness, no passenger loading between stations and no vehicle whose late arrival starts a fixed-time, full working late, so the quantity and its construction stop making sense.

Layer 1: Cardale's running feed stamps calls at half-minute resolution against timing-point codes from the station register; the working timetable marks allowances in brackets and dwell as the gap between arrival and departure; the feed and the timetable switch from BST to GMT on Sunday 25 October 2026 with the rest of the country; a failed unit's diagram is worked by a spare on the day, so the record's unit can differ from the plan; the census counts each service's boarders and alighters on one autumn weekday. Nothing is placed to be caught, and none of it moves the call.

Layer 2: estimand identification: the counterfactual of a team at a station is the network as it would have run, so the methodological choice that flips the call is to replay each weekday through each unit's actual next workings, letting lateness beyond the turnround slack start the next working late, rather than pricing the overrun on the train that incurred it or scaling that figure by an average reactionary ratio.

Decisive step: follow each delayed train's unit at Ravelstoke Central into its next working, passing on the lateness beyond the layover less the four-minute minimum turnround, and weigh it by that working's passengers; on the Ambrey line's morning all-stations units this carries Pellingham's overruns onto the full outbound airport trains, while Ambrey Parkway's extras end in the sidings.

Not semantics: every field, code, unit and definition read correctly (the half-minute stamps, the bracketed allowances, the clock change, the unit swaps, waiting for a timetabled departure kept out of the overrun) still leaves the same-train route on Saltgate, because where a unit goes next and how much lateness its turnround passes on is not a reading of any field: it is a construction across rows of the running record that the analyst has to recognise the network figure needs.

Not rule application: no filed rule or procedure tells the analyst to carry lateness into a unit's next working, so executing the brief, the timetable and the planning rules correctly still files Saltgate when the saving is priced on the trains that call at the station. The enumerated family (train-minutes removed, passenger-minutes on board, the same-train replay with or without allowances, that replay scaled by the network's, the line's or the line-in-period reactionary ratio, the full replay through each unit's day, a one-hop replay) names Saltgate four times, Ambrey Parkway twice and Pellingham twice; the standing family once the replay follows the units (one hop, every hop, the planned or the actual unit, the minimum turnround as filed) is unanimous on Pellingham, with the figure inside one bin; what rules out the rest is loud on the running record's own late starts from Ravelstoke Central (each sits exactly four minutes after its unit's arrival) and silent on every station-level cut.

Analyst test: a strong analyst who reads every field and rule correctly replays each train with the team's three fifths of the overrun removed, carries the lateness to each passenger's alighting station net of the allowances, perhaps scales it by a reactionary ratio, and files Saltgate at about 7,000 passenger-minutes a weekday; the Ambrey line's all-stations units carry Pellingham's lateness into their full outbound workings, so Pellingham's about 9,000 is the call.

Estimand: the rail executive's dispatch team brief (`dispatch_team_brief_2027.docx`, section 3) files it: the team is worth the passenger lateness it takes off the network's weekday trains, each passenger's minutes after the timetabled arrival at the station where they leave the train (none for an early or on-time arrival), summed over every weekday train and averaged over the autumn 2026 weekdays as they ran, the team removing three fifths of the time each train's dwell runs over its timetabled dwell at its station between 06:30 and 19:30.

No decoy: nothing is planted to be caught: no memo, briefing, draft or stakeholder figure states a saving, a ranking or a preferred station; the close-out reports Quayside's own trial and is true of Quayside, and the operator's performance summary reports what it measures.

No certified replay: the method is not recovered by reproducing certified or published figures: the close-out's one measured saving is reproduced by every rung at Quayside and selects nothing among the shortlisted stations, and every golden figure is built from raw running rows.

Lesson: a delay removed at one point is worth what it removes from everything the vehicle carrying it does next, so a station's saving is read by following its trains' units through their turnrounds, not by pricing the minutes where they arise or scaling them by an average knock-on; no build on file carries a local saving through the vehicles' own sequences of work.

## Tried and rejected

- The note's own decisive rung, shrunk lift times platform-drawn clicks (pattern C, gap objective, decomposition_attribution): blocked at the draw by ban.pattern C against task116, test.same_puzzle_older against six builds and test.same_driver_older against task38 v3, and its driver (a reachable share of each candidate's magnitude certified by closed interventions) is task38 v3's and task28 v2's, so it can sit at rung 3 but cannot carry the stump.
- A G7 operating-window rung (a winner earns only on platform clicks after its fixed test window closes, invisible to the evergreen app-exclusive embeddings): blocked by test.same_puzzle (time, G7, pick_one_of_n) against task105 v1, a timing driver the portal already solved, and an in-window same_puzzle takes no differentiation.
- Grading every desk's four chain stages as requested figures (the draw's 24 chain criteria): the rung-3 mirror keeps the platform-clicks and lift stages (12 of 24) and the cracker all 24, so the one-cracker pair sits near 50 before any device ask; only the terminal stage is requested.
- The note's ask B, newsletter click-to-open with privacy-proxy opens: fails H18, because a person could act on it with the squad call unmade; its export ships as a distractor.
- The note's ask C as written, each desk's clicks under each of the four rung bases: names the ladder in the prompt and hands the mirror the shallow cells; only its back-test count survives.
- A workload ask (headlines a week the squad would test) and extra clicks per article: the workload puts each desk's article count beside its test count and nudges toward the netting; a per-article figure at whole-click precision inherits up to 1% of admissible shrinkage spread and cannot be binned.
- The committed figure to the nearest 10,000, the note's rounding: method of moments and maximum likelihood move Culture's figure by up to about 12,500 clicks, more than half a 10,000 bin; every click figure goes to 50,000.
- Matched squad-run and desk-run tests to close what the squad adds on a desk-tested headline: a closed embedding at a self-testing desk would let the change log see the netting and break its blindness, and squad loan tests at a shortlisted desk would blur who ran the tests; closed by construction instead.
- The advertising value of the extra clicks as a both-layer ask: at publisher yields the best desk's gain is worth tens of thousands of dollars against a six-person squad, which raises whether the squad should exist at all.
- A Culture·metro desk inside the Culture vertical to keep the dashboard-plus-netting cell off Culture: read as lift alone, the editor-in-chief's basis then names Local·metro; Politics·metro's raw lift at 8.3% keeps both readings of that basis on Politics·national and clears the cell.
- Method of moments as the golden prior: Sport·metro's and Politics·metro's tiny packages (about 120 clicks) bias the unweighted moments (mean -0.82% against -1.04% by maximum likelihood), Culture's figure moved 3.2% (out of its bin margin) and maximum likelihood failed the back-test 0 of 7; the golden became maximum likelihood, with DerSimonian-Laird convergent and method of moments refuted on the corpus.
- Raising the two small metro desks to about 350 clicks per package so the moment fits agree: the raw-lift netting cell then needs Sport·metro's rung-4 figure near 300,000, which the remaining spread between estimators cannot hold mid-bin, and rung 1 needs a 130M-click Sport·metro.
- Shipping the leader with no gate on the Brisbane instance: Local·metro ships 79% of its tests, its won-only share of platform clicks reaches 0.58 and the won-only netting cell names Culture at 1.07x; the Brisbane gate is 80 per cent (z above 0.84).
- Culture at 2,900 clicks per package (factor 0.70, raw 2.6%) with the gated Brisbane instance: the dashboard-plus-netting cell named Culture at 1.10x; Culture's tests lengthened (factor 0.80) and Politics·metro given 210 shorter tests.
- The design's lifts under one true-lift distribution: Sport·metro at 11% raw cannot keep a 3.08% shrunk lift, and the squad's raw lifts of 3.0% to 7.9% are out of reach through a 95% gate; built at 10.8% / 0.39% and 2.7% to 3.7%, with every ladder margin held through the solved planned clicks.
- The ask layer as designed (S1, S2, HZ1 to HZ4): with the export notes' and the standards policy's rules executed per document, the national desks' correction counts, rates and medians were all right and the pair simulated at 53.6; HZ5 (the migration's carried documents) brings the same reading to 38.0.
- Panel section codes reissued in alphabetical order: the careless join moved readers but left extra per reader in its bin at most desks; codes re-cut so the careless months read a section of very different size.
- Test sizes drawn independently of article size: 561 tests carried more clicks than their article's first-two-hours platform pageviews; tested-article sizes compressed and given an earlier platform profile, and the squad's in-window tests placed on enlarged lead items.
- The ask layer as shipped at stage 3 (S1, S2, HZ1 to HZ5, R1, HZ2, HZ3), round 1 plain solver: it missed the call at rung 3 exactly as the stump sentence says (Local·metro 2,800,000, runner-up Business·national) but scored 46.0 because it kept every device figure, readers, headline corrections, rate per 1,000 and median minutes at all six desks plus the back-test, by executing the filed rules per document in its own words: "merged documents recreated by the 14 Nov 2025 Brisbane restore into their originals. Dropped the 1,704 documents migrated from the old CMS", "a headline correction is a revision that adds a new correction note and changes headline_sha1, following standards s7.4. Notes copied forward to later revisions ... were not counted again", "Mapped section codes to desks through the Section history sheet ... using R26-07B's restated April to June 2026"; every primary and hazard falls to a field or a filed rule the solver reads, so device leakage is near 1.0 against the 0.10 the pair arithmetic needs. It also named rung 4 and declined it ("I also did not net off the testing the web desks already do themselves"), so the rung is visible though not taken.
- Hardening loop 1, the principle under the stage-3 ask layer: every primary and hazard adjudicated by a field or a filed rule on the ask's own path (the copied-note line, s7.4 with `headline_sha1`, `restored_from_doc`, `migrated_from`, `doc_type`, the section history's dates, the R26-07B release note), with two free confirmations beside them, the spine's per-desk article counts and the bulletin's March figures. A solver that reads every field executes each rule per document and then checks itself twice, in its own words "Story and live-blog counts match the article counts in the pageview data exactly" and "March 2026 (AEST) has 12 headline and 31 text corrections, matching the April standards bulletin exactly", so those devices stay only as hazards and the primaries move to constructions no field names: which revision published the headline, when a scheduled article went live, an entry's headline corrected under its live blog's note, and which section list a history release was issued on.
- Hardening loop 1's ask layer (primaries moved to which revision published the headline, scheduled go-live, live-blog entry headlines under the blog's note, and the section list a release was issued on), round 1 re-run as "round 2, plain" (38.0, main call missed at rung 3 on Local·metro 2,800,000 against Business·national 1,750,000): the round passes, but on the rung-3 extra-clicks tokens alone, because the solver again kept readers, headline corrections, rate per 1,000 and median minutes at all six desks plus the back-test, executing every new primary in its own words ("Go-live = first live save, or publish_at for a schedule that fired", "For live blogs, a note added to the blog in the same minute as a post headline change also counts", "Section codes are mapped by the taxonomy of the release ... including R26-04H") and confirming against the bulletin's March figures; device leakage stays near 1.0, so a solver that takes rung 4 keeps the whole xlsx row and the ask layer cannot hold the pair at round 2. It joined `owner_staff_id` to the staff list and saw every web test was desk-run, then declined the netting ("The files do not say whether a squad embedding adds to or replaces a desk's own testing"), so rung 4 is seen and refused, not silent.
- Round 3 (plain and skeptic together) on the hardening-loop ask layer: both missed the call at rung 3 on Local·metro (plain 2,800,000, skeptic 2,400,000 after re-applying the squad's 95% ship rule to every desk, runner-up Business·national 1,750,000 in both), proxies 46.5 and 36.8, average 41.65 with neither under 25, so the round does not pass. Neither path mentions `owner_staff_id` or the staff list this time, so rung 4 was silent and held. The asks did not: both kept readers at all six desks by catching R-back ("mapped section codes by release taxonomy ... 2026 codes for R26-04 onward, including the history release"), the skeptic kept every headline correction count and rate by catching K-auto, K-entry and M1 together ("Built the published sequence ... scheduled revisions at publish_at only if no later save came first ... plus live-blog entry notes matched to a post headline change in the same minute (16)"), the plain solver all but Local·metro's, and both kept the 7 of 7 back-test; only the medians held (timed from the entry going live rather than the blog), and the plain solver's notes list five of the six golden medians as its alternative. Device leakage stays near 1.0 for the second consecutive round, which under the Stopping rule re-roots the ask layer rather than adding a fifth primary.
- Hardening loop 2, the principle under hardening loop 1's ask layer: primaries that were constructions no field names (which revision published the headline, scheduled go-live, an entry's headline fixed under its blog's note in the same minute, the section list a history release was issued on), each still adjudicated by a sentence on the ask's own path that names its own construction (the status line, policy 7.4 and 7.5, the `publish_at` and `doc_type` lines, the R26-04H note "rerun on the 2026 content taxonomy"). A solver that reads every field note writes the construction from the sentence, in round 3's own words "Built the published sequence (live saves at saved_at; scheduled revisions at publish_at only if no later save came first ...) ... plus live-blog entry notes matched to a post headline change in the same minute (16)" and "mapped section codes by release taxonomy (old 2024 codes only for the R25-11 Oct 2025 release; 2026 codes for R26-04 onward, including the history release)", then confirms itself on the bulletin's March figures and the spine's article counts, so readers, counts and rates leaked at 5 or 6 of 6 for the second round running; the medians held only because both solvers timed an entry's fix from the entry going live rather than the blog, a reading choice and not a device. What dies is the organ that states its construction; what the round shows untouched is every assumption the solvers' own path makes and never checks: that a note and the headline fix it records arrive on one save (or one minute), and that the latest release per period is the record for every section in it.
- Update notices in the note field (a developing story's "This story has been updated ..." line saved with a headline change, excluded by 7.2): rejected on paper at hardening loop 2, because the notices form a visible family in any scan of the note texts and 7.2 already names updates, so a solver who lists note openings executes the exclusion; the note that follows its fix was taken instead, whose rows read like every other correction.
- A backdated `publish_at` for the medians (a scheduled revision saved after its own publish time): rejected on paper at hardening loop 2, because whether the CMS publishes at the save, at its next run or not at all needs a filed rule, and a filed rule on the field-notes path is executed.
- Readers devices that need a new sentence in the panel workbook (unique browsers on the Brisbane site, three-month rolling regional estimates, units set by agreement, an experimental release that does not replace the standard series): each needs a conversion nothing pins or a note the solver reads and executes; only a structure the release rows carry themselves (which sections a supplementary release reruns or restates) survived.
- The first lag sub-seeds left round 3's path on the golden median at Local·metro and Culture·national, and two partial readings on Culture's: a median moves only if the fix-then-note corrections sit around the median article, so each desk's lag stream was searched until all eleven readings miss every median (Local·metro's nearest by 15 minutes and Culture·national's by 19; the thinnest misses are Business·national's 88 against 89 and Sport·national's 45 against 47).
- R-part as the readers primary (supplementary releases carrying only the sections they rerun or restate), round 5 plain and skeptic: both solvers kept the latest release per period and section and reproduced all six readers, in the plain solver's words "kept the latest release for each period and desk (R26-04H for Nov 2025 to Feb 2026 BLN; R26-07B for Apr to Jun 2026 BLB)", because a per-section latest-release rule is what a careful solver writes by default and the partial release does not punish it; with the readers block leaking at 6 of 6 in every round since stage 3, the plain solver keeps enough ask weight to sit at 43.9 and no response reaches 25.
- K-lag as the corrections primary (a headline note on the save after the fix it records, and an entry's fix with its blog's note minutes later), round 5 plain and skeptic: both solvers paired a note with the headline published just before it, in the plain solver's words "A note counts as a headline correction if the live headline changes on the revision that publishes it, or if it is a headline-worded note whose headline changed live up to 10 minutes earlier. For a live-blog entry, it counts if the entry's headline changed live within 10 minutes" and the skeptic's "Also counted: notes that name the headline and follow a just-published headline change by 0 to 9 minutes, and live-blog notes paired with an entry whose headline changed", because a note that names the headline on a save that leaves the headline alone sends a careful reader to the save before it; the counts then sat 0 to 3 off the golden for the plain solver (Sport·metro's 18, 7.3 and 55 kept whole) and 1 to 7 off for the skeptic, so the block held on older hazards by a few corrections a desk, not on the primary, and K-lag is spent as a primary.
- Readers devices weighed on paper at hardening loop 3 and dropped: a desk's section split into content groups with a deduplicated total the audience team never mapped, because a mapping of the parts without the whole reads as planted and two or three rows a desk a month is a symptom the hygiene battery finds.
- A January rerun issued on the 2026 list with no taxonomy note: it fails only solvers who map codes by month (round 5's plain solver mapped by release), and the national sections a misread swaps differ in size by 25 to 180 per cent, a spike any monthly look shows.
- A supplementary release coded after the first month it replaces, so that code order and publication order disagree: the release notes say what each release replaces, and round 5's solvers applied the notes rather than a sort.
- An unlisted parallel-run delivery left in the panel export: setting it aside needs a sentence that names it, which a careful solver executes, and without one the record leaves its status undetermined; the July file's repeat of figures a filed restatement replaced was taken instead, decided by the release log's months and by the repeated figures themselves.
- The July file's repeat with the restatement as an overcount (a 4.5 per cent duplication fault, the first figures high): round 1's readers path cancelled back onto Culture·national's golden (the history release's lower 2024-basis figures against the repeat's higher ones) and per month and code fell inside half a per cent there; with an undercount every readers mishandling at Politics·national and Culture·national errs low, and every naive readers stop moves all six desks.
- Taking a per-reader figure from the cracker through the July file: a silent repeat (a 7 per cent undercount over three months) moves readers under 2 per cent and no one-decimal per-reader figure with it, and moving one needs readers 3 per cent low at Local·metro or 4.3 per cent high at Culture·national, a plateau any monthly look shows; tuning a golden readers figure toward its bin edge so the repeat could take one was rejected as moving a graded answer for the device's sake, so the one-cracker pair sits at the layer's floor, 40.6.
- Corrections devices weighed at hardening loop 3 and dropped: a longer gap between a fix and its note (10 to 45 minutes), which lives in the population round 5's solvers already examined and fails only a window choice; and a correction logged on a corrections page, which needs a filed rule naming the page that a careful solver executes.
- The first note-first and put-back sub-seeds: Local·metro's round-5 reading netted back to the golden count (two notes before their fix against two put back) and Culture·national drew no note-first case, so each desk's sub-seeds were searched until every partial reading missed every count and median (Business·national's at the 48th note-first seed).
- The loop-3 ask layer (R-echo for readers, note-first and put-back sub-seeds for corrections), round 7 plain and skeptic: both kept readers at 6 of 6 by reading the release log's scope per period (the skeptic: "each period took only the release the release log lists for it ... I ignored R26-08's stale reload of Apr to Jun"), and both kept counts and rates at 6 of 6 by pairing a new note with a headline change within 10 or 15 minutes either side and checking it on the bulletin's March figures; the skeptic kept all six medians ("Minutes to first headline correction run from go-live to the live save that published the corrected headline", with the live blog as the article), so R-echo and the note-first and put-back sub-seeds are spent as primaries and the medians are the only device left that a reading choice decides.
- Stage 6 fix cycle 1, closing the judge's residual entry-pairing fork (a live blog's note paired with an entry headline changed 21, 22 and 59 minutes after it under a symmetric 30 to 60 minute window, Sport·national 43 and Politics·national 48) by widening the generator's entry guard to the hour after every blog note: it would flip three ordinary entry updates in the CMS export, which is regenerating measurement data (a SEND_BACK-class change under judge v3 that the solver rounds' supplementary results would not survive), so the fork is closed instead by one line in the CMS field notes, a data-dictionary pin that only fixes what the correct count is and also rules out pairing a note with a headline change hours away.
- Stage 6 fix cycle 2, restating critical components 1 and 4 at a coarser rounding (1.8% and 70,000,000) so admissible variants cannot move them: a prior on the web engine's packages only, which the change log cannot refute (7 of 7, worst 1.90%), puts Culture·national's lift at 1.7746% (1.77%), and the in-window corridor variants put its untested platform clicks at 70,138,602 (pre-window articles left out) or 69,790,626 (7-day-and-older clicks left out). Rejected: every graded ask figure, the call and the back-test count converge under all three, every solver round fitted its prior on all 10,111 packages and kept the base whole, the judge reproduced 1.78% and 70,300,000 twice, and coarsening breaks the golden paper's reproducible line (70,300,000 at 1.78% is 1,250,000); pinning the prior's population in a filed document instead would put the estimator on a main-path file, which the method must not have. Recorded in the fork grid and the 22-axis table instead.
- Stage 6 fix cycle 2, the verifier's first read of the stored-headline surfaces checked the `canonical_headline` row but still took its platform classes from a fixed list, so its figures did not depend on the row: run on the unpinned fix-cycle-1 pack it failed only the row check and reproduced the call. The classes now come from the row itself (a source code carries the stored headline when the row names its surface), and the same control fails the call figure, the runner-up and every desk's extra clicks.
- Stage 6 fix cycle 3, redrawing the staff list's 201 non-persona names with `guard.py names --geo Australia --seed 118` as the judge's third report suggests: the installed Faker carries no en_AU person provider, so the en_AU locale falls back to en_US's pools and the draw reproduces the very skew the judge flagged (33 of its 201 surnames sit in Faker's es_ES or es_MX pools and in none of its British, Irish or New Zealand ones: Carrillo, Molina, Hernandez, Garza, Figueroa, Garcia and on; lowercase Mcdonald, Mcdowell and Mccarty; US first names such as Caleb, Bryan, Kelsey and Zachary), and `suggest_people` also refuses any surname used in any build and any surname repeated within the list, which a 207-row newsroom list should not look like. The six personas stay as drawn for the card; the staff rows are drawn instead from Faker's own en_NZ, en_GB and en_IE pools with romanized zh_CN, de-accented vi_VN, en_IN and de_DE surnames mixed in, seeded, with Mc, Mac and O' recased. it_IT was in the first mix and was dropped: its surname list is drawn from notable Italians (the first draw gave "Viridiana Berlusconi"). The second draw still gave "Peter Murdoch" in a news publisher's staff list, so Murdoch, Packer, Fairfax and Stokes are filtered as media-dynasty surnames, with en_IE's misspelt "O'Loughlinn".
- Stage 6 fix cycle 3, loosening the change log's fit, which the judge's third report reads as fitted (realised clicks within 1.2% of shrunk lift x planned clicks in all seven years), by widening the realised noise toward the 2% bound: the admissible fits already spread to 1.90% on the worst embedding (the web-engine prior, which the corpus cannot refute) against the golden's 1.16%, so the margin that keeps every admissible fit on 7 of 7 is 0.10 point, and any widening spends it and turns the graded back-test count into a fork between two admissible priors; it would also recut calibration data every solver round read. The tight fit stays, because the 2% back-test needs it; the judge's own report says as much.
- The change log as planned and realised clicks (wave-1 redesign): every closed embedding sat at an app desk where the platform share and the untested share are both 1.000, so rung 3's construction reproduced all seven realised gains and only the forward desks broke it, the validated decoy the guard now blocks; the log records the realised holdback lift instead, which selects the estimator and says nothing about the click base.
- The brief's line that the editor-in-chief's office reviews placement on the dashboard's average winning lift by vertical (wave-1 redesign): a filed basis whose literal reading gives another answer, an official decoy; cut, with the dashboard export kept as the declared wrong-basis distractor.
- The thread's four beliefs (readers, "a winner is a winner", Business like Puzzles, the dashboard view) (wave-1 redesign): a roll call handing a solver one rung to refute per voice; only the head of audience's belief stays.
- The per-desk extra clicks, the chart walk and the back-test count as asks (wave-1 redesign): the call's construction, which a response on the call keeps whole (12 of 42 criteria free); the chain stays in the golden, unrequested.
- Extra clicks per reader as an ask (wave-1 redesign): no silent readers shift moves a one-decimal per-reader figure (Local·metro's would need readers 3 per cent low), so a response on the call kept all six whatever the readers device did, and the figure tied the readers device to the call.
- The headline-correction count and rate as asks (wave-1 redesign): every corrections device is adjudicated by a filed line (policy 7.4 and 7.5, the field notes' ten-minute pairing and put-back lines), so a response that executes the filed rules keeps all twelve figures.
- The July file's repeat with the release log's months shipped (R-echo as built at hardening loop 3): round 6's solver set the rows aside from the months column ("the release log scopes R26-08 to Jul only"); the column is gone, so only the restatement's note and the repeated figures find the rows.
- `publish_at` in UTC beside a field-notes line naming its clock (M1 as built at hardening loop 1): a filed scheduling rule every solve executed; `publish_at` now carries the editor's Brisbane wall-clock time with no zone line, and only the record's own inconsistency on the saves' clock finds it.
- Sport·metro's lag draw 50 and Business·national's note-first draw 47 (the loop-3 draws, wave-1 redesign): with `publish_at` read on UTC, the round-3 path and the lag-blind reading landed back on Sport·metro's golden median and the note-first-blind reading on Business·national's; redrawn to 218 and 102, where every corrections reading on either clock misses every median and every structural assertion holds (Sport·metro's draw 53 passed the medians but put half its own fixes on a lagged note and left one note-first fix).
- Realised holdback lifts to two decimals of a per cent (wave-1 redesign): the smallest realised lift (0.70%) carried a rounding error near 0.7 per cent, which pushed the convergent web-engine prior to 5 of 7 (worst 2.50%); three decimals restore 7 of 7.
- Visits left wherever the draw put them (wave-1 redesign): Culture·national's average sat 67 visits from its rounding edge; the September release, which nothing restates, now absorbs each section's remainder so every average sits at least 150 inside its thousand.
- The brief's counting phrase "counted at the owning desk on every click an article earns from publication, the hours its headline is under test included" (wave-1 redesign, stage 4): the isolated reader executed "every click" as an all-sources click base for the lift, a main-call fork against the field reference's stored-headline surfaces; the brief now says "counted at the owning desk from each article's publication, the hours its headline is under test included", which pins the period and names no click base.
- Related links classed as Bightline surfaces only by their absence from the `canonical_headline` list (wave-1 redesign, judge pass 2): read the other way the call figure is 1,050,000 with the same desks; the `related_links` row now says the links show each linked article's current headline.
- Architecture 1, the headlines each desk's own editors already test netted out of the squad's gain (2026-10-27, portal
  FAILED_TO_STUMP): both responses kept the clicks from Bightline's own surfaces, dropped the articles a desk had already
  tested and filed Culture·national at 1,250,000; the netting reads as a filter anyone applies (a tested headline cannot be
  tested again), and the shrinkage that the change log selects moved the figure, never the desk. The resume line had
  already measured it: own surfaces plus the drop plus distrust of Sport·metro's small-test mean reaches Culture·national
  with no shrinkage at all. Re-rooted onto what share of a shipped headline's clicks is new to the site.
- The corrections ask with every rule filed in the corrections standard (going live, the ten-minute pairing, a note put back, entries, restored copies) and no silent device (architecture 2, 2026-10-27): a response executing the filed rules kept all 18 cuts and the pair measured 60.5 on the readers device alone; an autosave of a live article's working copy now carries the article's status, live, typed `autosave`, so reading the status column alone moves 15 of the 18 cuts.
- Quartiles of minutes to the first correction (the draw's shape line, architecture 2): the 25th and 75th percentiles of 13 to 43 values differ by several minutes between inclusive, exclusive and nearest-rank methods, a percentile-method fork; counts within the hour and after more than three hours carry the same cuts determinately.
- A six-hour mark for the second count (architecture 2): 0 to 3 a desk, two desks at 0 and two at 1, so a constant response files a third of them; the mark moved to three hours (2 to 7 a desk), and every first correction sits at least three minutes clear of 60 and 180.
- Readers and visits per desk as graded figures (architecture 2's first cut, 2026-10-27): the July file's April to June rows repeat replaced figures byte for byte, which the battery's duplicate sweep finds unprompted (supplemental-stumping 1.1e), and with the release log silent on R26-08 the house judge's pass on that cut marked the reading open; the log's months, restored for determinism, make the readers block Layer 1 work every careful response lands, as it has 6 of 6 in every round since stage 3, and a cracker keeping it fails precut. No readers device both silent and forced by the record was found, so readers and visits leave the graded asks and the panel files ship as declared distractors.
- The autosave status as the corrections primary (architecture 2's final cut, determinism pass 6, 2026-10-27): NOT_DETERMINISTIC on the workbook asks alone, because no shipped file said what an autosave is and the status column on those saves reads live, so counting them as published versions was a defensible reading that moved three desks' cuts. Filed in the corrections standard 7.3 ("An autosave of an editor's working copy publishes nothing"), which makes the autosaves a hazard every careful response executes; the primary moved to a schedule set back to draft before its time, which the status column decides by itself (a draft at the time first set, a draft saved after it, no document ever set back to draft once live) and which the round-3 skeptic's own rule, a scheduled time only if no later save came first, already handles.
- The method left to the change log alone (architecture 2 as shipped, portal determinism return 2026-10-27): one judge passed it as analytical, the other read it as replay, the lift estimator and the share of a won click new to Bightline stated in no file and recoverable only by matching the seven embeddings, and filed the portal's off-call response as a competing answer, each desk's raw mean winning lift scaled by one factor fitted on the change log (0.3209), Sport·metro at 900,000 with Culture·national runner-up. Closed with a filed selection criterion at authority, not the method: the brief's sign-off (a working run unchanged on each closed embedding within 2 per cent of the lift and the extra clicks it realised against its holdback), which that route fails on both halves (0 of 7, 1 of 7) and which every passing working on the filed netting meets with the golden call, figure, runner-up and gap. The fork was not the stump: rungs 4 and 5 still end on Culture·national, and the sign-off says a working must pass, never what passes.
- The ask layer as shipped at that return (18 figures on one silent primary; the on-call response at 87, the pair at 65.5): the median and the two counts move only when a mishandled article crosses the middle or a mark, so a response that mishandles a few stories away from them keeps the figure, and a response that repairs the set-back schedules by reading the status at each scheduled time keeps every figure. The total minutes a desk's wrong headlines stood went beside the median, because every mishandled article moves it, and a second silent primary (a schedule moved to a later time and saved again, still scheduled, after the time first set) went under that repair. Neither moves a golden ask figure.
- Architecture 2 as reshipped with Experimentation's sign-off (portal 2026-10-27, FAILED_TO_STUMP): both responses filed Business·national at 500,000, runner-up Local·metro, 100,000 behind. The sign-off, filed to close the second judge's replay finding, told every reader that a working must reproduce each closed embedding, which rules out the one average shortfall and sends the reader to what differs between the embeddings: the desks' page mixes and each page's click-through. The closure and the stump were one dial: without a filed criterion the method is recoverable only from the change log (a replay and a competing answer), with it the decisive step is a work order. Architecture 2 is spent; re-root.
- Architecture 3, first prototype (2026-10-27, scratch t118v3/proto.py, never built): the excess fall risk by time on the drug estimated from the board's own 2023 to 2026 records, the extract's start diluting the early band. Six networks avoided only 6 to 14 admissions each, the truth ranking nearly tied (A 11, C 10), and the hazard estimate's own noise reordered it across seeds: the bin narrower than the estimator, a fitted rate per band besides (stumping 1.1j). Replaced by a filed standard (the board's medicines safety policy gives the fall rate ratio by months on the drug) and a short extract (April to September 2026), so the decisive step is each user's start, rebuilt through the repeat-template re-authorisation chain, a reconstruction with one answer.
- Architecture 3 with a three-band schedule (first 3 months 4.0, 3 to 12 months 2.2, then 1.05) and the reviews on 1
  January (2026-10-27, scratch t118v3/proto2.py): with every current user started by 30 September 2026, no one is in the
  first band in 2027 and the second band reaches only the starts after January 2026, almost all of them visible in the
  extract, so treating the users present at its opening as long-term reproduced the golden ranking: a cheap route
  landing the call. The raised band now runs to 24 months and patients come off from 1 April 2027, so the year before
  the extract (1,485 of Selbourne Coast's users) carries the excess and that route names Wychcombe or Harrowden Central.
- Primary care networks of 1,600 to 3,400 current users (the draw's first sizing): a real network has a few hundred,
  and at a base of 4 per 100 the figures fell to about 10 admissions with a gap of 2; the decision moved to six
  localities of 3,200 to 6,800 users, where the figure is 19 and the gap 4.
- A base rate of 7 per 100 a year (the draw's first parameter): about three times the national rate of emergency
  admissions for a fall at 65 and over; set at 4.0, a frail population's rate.
- Thornbury Rise's whole locality moving clinical system in July 2026 (2026-10-27, first full build): read off the
  current system, every one of its 4,583 users started on the move's date and Thornbury Rise led at 49.9, so a Layer 1
  item carried a rung (dataset-generation 7.1 R2); one practice (Mill Road Group Practice, 266 users) moves instead,
  and mishandled it leaves Thornbury Rise at 13.2, under Wychcombe's 15.3, the call, runner-up and gap unchanged. The
  second-smallest practice left Thornbury Rise 0.05 behind Wychcombe and was not taken.
- The asks' stays joined on the receiving hospital's codes, with transfers coded consistently (the first SUS cut): a
  careful join kept 13 to 24 of the 24 figures; the receiving codes now vary as hospitals record them (a move coded as a
  fresh A&E admission or from home), hip fractures at district sites go to the trauma unit mostly the same day, and the
  natural joins keep 0 to 2.
- The extract's first-item route measured against the template route in a prototype where the extract began in April
  2023: a patient on the drug since before 2023 is long past 24 months either way, so the extract's dating moved nothing
  and there was no stump; the extract was cut to the platform's first six months.
- The localities and hospital sites as first named (stage 3, reduce-house-fixes H21): Harrowden and Thornbury are real
  places (Thornbury has a real community hospital), and Selbourne and Wychcombe sit one and two letters from Selborne and
  Wycombe; renamed Corvenham Central (CC), Saltreach Coast (SC), Quenford Rise (QR) and Hethermoss (HM), with their
  hospital sites, every figure unchanged (asserted on figures.json across the rename). Lines above this one keep the
  names they were written with.
- Architecture 3 as shipped (portal 2026-10-27, FAILED_TO_STUMP): both responses filed the golden, Saltreach Coast at 19
  (one at 19.2) with Hethermoss runner-up 4 fewer (one at 15.3 and 3.9). The policy's "months since the patient first
  started" sends every reader to ask when each patient started, the extract's April pile-up answers that it cannot
  say, and the template chains are a file any reader opens: the quiet step was loud once the filed risk model named its
  quantity. Architecture 3 is spent; re-root to architecture 4 in another client domain.

- Architecture 4 at a GBP 3 million envelope: cider's cut took 89 per cent of its duty, so the straight-line welfare
  formula moved cider 0.04 above the exact integral and the gap's family straddled 0.95; at GBP 1.5 million every cut is
  a smaller share of its duty and spirits, cider and the gap each sit 0.015 or more inside a bin.
- Architecture 4 with the release layout changing in 2020: the 2020 to 2026 file alone fits spirits at 1.3 against the
  full series' 0.9, so a reader who dropped the back series moved a graded figure (Layer 1 carrying a figure); the
  change moved to 2012, where the newer file alone files 0.9 and 0.4.
- Architecture 4's first ask device, a premises renumbered at a change of keeper (removals declared to the old
  approval number): with CE14 filing the rule by premises it is executed by any reader who checks the premises, and by
  approval number it is no device; replaced by the declaration's duty repeated on every item row.
- Architecture 4's first declarations draft: duty_gbp was each line's own duty, so every CE14 handling was a filed rule
  the cracker executes (20 of 20 kept); and declaration numbers from a nine-digit hash collided once in 26,752 lines
  (two declarations merged), replaced by a multiplier prime to ten.
- Architecture 4's furniture as drawn (a Treasury research desk taking the envelope to the Council of Ministers in the
  Budget round): BLOCKed by `heart` on role, forum, forcing event and organisation against task310, drawn the same day
  and delivered after this draw; redrawn to the Assembly's scrutiny panel and its adviser, the analysis unchanged.
- Architecture 4's first invented names: Castelmere sits two letters from a real Rochdale district, and Granary Wharf,
  Westfield, a saint's name and two retail brands in the shop quotes were real or distinctive; renamed (Eskerholm,
  Ardvane, Ropewalk, Moorside) with every figure unchanged.
- Architecture 4's ask primary as first built, each declaration's duty repeated on every item row: the battery's
  repeated-total reflex sees it, and a careful solver prices every item as litres times the rate, which reaches the
  golden without ever reading the repeated total (the coordinator's review; every careful path would have kept 20 of
  20 and the pair sat near 83.5, not 28.5). Demoted to a hazard; replaced by corrections lodged as new declarations
  naming the one they correct, chained across quarter ends, which acts on which rows are releases and in which
  quarter rather than on the price.
- The first chain draft spread stock-count corrections evenly over the quarter ends: the one-hop error in a quarter is
  its inflow from the quarter before less its outflow to the next, and in one cell they cancelled to GBP 151; with the
  year-end count fullest and the half-year next every careful path misses every cell by GBP 3,600 or more.

- Architecture 4 as shipped (portal, 2026-10-28 to 10-31): the call landed three times and the determinism block
  failed twice; the golden was the field's own welfare method (the existing wedge plus the cut's triangle on the
  year's partial-adjustment quantity), which the responses applied by reflex. Spent; re-rooted to architecture 5 in
  another client domain, world, dataset and prompt shell.
- Architecture 5's handed-out cell, pharmacology benefit-risk with a pharmacist medication review whose harms avoided
  depend on whether two interacting drugs come from one prescriber or two (2026-10-31, screened on paper): the
  realisable share carried from a pilot within the prescriber-split stratum is approved 124's abstraction (a share that
  holds only within the stratum, carried to the population); dropped.
- The same cell's other mechanisms, each screened and dropped before any harness: pharmacy-counter interaction alerts
  already resolving part of the pool (the netting architecture 1 spent); generic substitution resetting exposure (task302
  and architecture 2's ground); discharge supplies misdating treatment start (architecture 3's ground); the review's lag
  against harm onset (task105 v1, solved); a self-controlled case series as the golden (the field's reflex); OTC aspirin
  co-exposure (a reflex, and purchase is not use, an open determinism fork); 90-day conversion with manufacturer
  switching (a behavioural model with no forced form); long-term-care mandatory reviews (netting again); prescribing
  cascades (task193's sequence symmetry). The cell could not carry an honest unbanned stump, so the build moved to
  energy-systems-utilities, which the brief allows (not epidemiology, criminology or marketing).
- An operating-theatre instrument-tray draw in healthcare delivery (screened on paper): the decisive quantity rode on
  how surgeons book, a behavioural fork the WHAT cannot file without filing the step; dropped.
- The demand-response draw labelled gap time with pattern E (first probe, 2026-10-31): structural BLOCKs against nine
  older builds; the honest labels are gap objective first (the measured average is right and is not what the plan
  prices) with G13, G7 and G14, which clear every structural test.
- A water-pumping shift as the fourth programme (draw, 2026-10-31): its reservoir drawn down across a heat wave sits on
  approved 120's setting (tank drawdown behind a peak), a reviewer's setting match; replaced by Peak Time Rewards.
- The first calendar with every non-event day just under the trigger (harness dgp3, 2026-10-31): the three days' heat
  before an event proxied its run day so closely that a weather model with heat build-up named the batteries at 1.22,
  a cheap route landing the call; hot weekends (uncalled under OP-7's weekday rule) now precede several fresh Mondays,
  and the heat build-up route files Cool Credit at 1.24.
- A hot weekend whose Monday sat the day before a four-day run (harness dgp4): the Monday made it a five-day run and
  the record's fourth day moved; the weekend moved two weeks.
- A Friday event followed by a Monday event after an uncalled hot weekend (harness dgp4): whether the Monday is a run's
  second day or a fresh first day is a construction fork (calendar days against the log's order); every Friday before
  a hot weekend now falls just under the trigger, and the record holds no Friday-and-Monday pair (SF10, asserted).
- A flat battery record (harness dgp5): the tenth percentile of each programme's event reductions named the batteries
  at 1.03, a reading of "firm" that lands the call for the wrong reason; Brightwell's communications drops (four
  events in 2025 and 2026 at about two thirds of the fleet) are the record's own texture and put the batteries'
  tenth percentile under Cool Credit's.
- Peak Time Rewards and Business Demand Partners within 1.07 of each other on the fourth day (harness dgp4): the
  runner-up was not determinate; the commercial sites' fourth-day reduction deepened to about three tenths of a first
  day's, which also puts every programme's figure mid-bin at whole megawatts.
- A commercial settlement audit as an ask (each 2026 event's delivered kW against the nomination, with the baseline's
  excluded days as the device): it computes a depleting programme's reduction event by event and so shows it falling
  on consecutive event days, which hands the main call's decisive pattern to any solver doing the ask; replaced by the
  nominated kW in CBMU's territory.
- A battery energisation-date ask (register upload against the inspector's pass date): the governing sentence that
  makes it determinate names the pass date, so the device is executed by every reader of that sentence; dropped.
- Megawatts to one decimal place: the standing family spreads Cool Credit 0.1 MW and the rebate programme 0.2 MW at
  the fourth day, and the thermostat panel's sampling interval is about 0.5 MW, so one-decimal figures fork; graded to
  the whole megawatt with every figure mid-bin.
- IDLE's change of meaning as an ask A device (no field dated the switch): judge pass 9 found the ask open, since no
  file said what IDLE meant or whether a retired thermostat counts; OP-7 section 6 now files both, the ask keeps the
  address link, and the same section files Business Demand Partners' meters.
- Architecture 5, each demand-response programme read on the record's fourth consecutive event days (2026-11-07, spent
  on its first portal round): both responses filed the golden (Home Battery Network 6 MW, runner-up Peak Time Rewards
  4 MW, every programme's MW) because a frontier analyst puts a consecutive-call streak in the event regression by
  reflex once the design hour's place in its heat spell is visible, splits the batteries' contract regimes on the
  amendment, and validates season-out; a named covariate the field already models (fatigue, streak, regime) is executed,
  so the energy demand-response world and the run-position driver are spent.
- Architecture 6 draw screen (2026-11-07), a theatre productivity team placed with one specialty, sized by the extra
  patients its lists can operate on once recovered late-start and turnaround minutes are packed list by list against
  the waiting cases (healthcare-delivery x OS, patient-flow): task301's note already measured the per-list replay as
  both call-only probes' first construction, so the step is a reflex; dropped before a card.
- Architecture 6 draw screen (2026-11-07), a highway authority's preventive surfacing placed in one district, its
  defects split by whether they fall inside a recent utility reinstatement's footprint (urban x OS, municipal
  service): whether surfacing prevents failures of existing reinstatements turns on old against new openings and a
  failure-lag model, and the only sentence that closes it names reinstatements, so the fork is the stump; dropped
  before a harness.
- Architecture 6 draw screen (2026-11-07), a pressure ulcer prevention bundle placed on one of four wards, each
  ward's recorded ulcers split by whether the damage began on an ED trolley before arrival (healthcare-delivery x OS,
  patient-flow): on the harness (scratch harness_pu.py, three seeds) the textbook count files the medical admissions
  ward and the trolley-exposure attribution files the orthogeriatric ward, but the 72-hour inherited convention, a
  tissue-viability reflex, files the golden too, and short attribution windows flip the standing family (10 to 12 of
  32 grid cells); dropped.
- Architecture 6 paper screens (2026-11-07), each dead before a harness: step-free station lifts valued by journeys
  made possible (the end-to-end step-free journey is the field's own method; the interchange-path version forks on
  route choice); added GP appointments credited only with ED attendances after the practice's slots ran out (the
  condition has to be filed, so the step is rule application); TB contact tracing placed by genomic cluster (the
  field's own method is the golden); a 3T scanner's throughput capped by each patient's implant conditionality
  (task117's chain form, and the effect is small); agency shifts matched to same-shift redeployments and sickness (the
  step is a three-file reconciliation, Layer 1); household secondary cases credited to the vaccinated group (the
  counterfactual forks unless the estimand files the method); dialysis admissions after the long interdialytic gap
  (readable: days since the last session is one join and one subtraction, and the gap is a named clinical
  covariate); GP list inflation against the outreach pool (population_selection is banned against task268, and the
  register-against-resident step leans on reading the register); a low-traffic neighbourhood or bus lane valued on
  through-traffic or mid-block delay (the scheme's own specification names the mechanism, readability test 1); once
  binding_constraint and causal_design reopened, freed capacity credited only in saturated periods (task162's
  hour-by-hour threshold form), a pilot hospital's ED fall net of displacement to its neighbour (v2's displacement
  abstraction, this slot's own lineage), the on-call rota as an instrument (a named judge design on eight clusters)
  and a fast-track priority netted through queueing conservation (a replay of a filed priority rule, task301's kill).
- Architecture 6 draw screen (2026-11-07, the second session), each candidate killed on a named test before a card:
  vacancy chains from new homes (task174 and task137 slot notes: the housing literature's own construct, a lever of a
  few per cent); an intervention whose effect falls with an exogenous intensity (flood depth for property resilience,
  gust for roofs: task309's driver); claims-handling capacity shortfalls as a natural experiment (task128's driver);
  claims at sibling policies in one event (task303's driver); securities-lending supply overlap between a fund's
  mandates (architecture 2's displacement lineage) and its holding spells (a lag per spell too small to reorder the
  mandates); smoker misrepresentation found only at death (honestly population_selection, banned in the window);
  aggregate-deductible leverage on a fleet's insurer layer (a per-year replay reaches the golden); gully cleansing on
  each gully's silt fill rate (the grouping dichotomy, and silt-based cleansing is the field's own method); a
  two-phase validation sample read by its flag strata (one group-by); bus-lane savings on section loads (the field's
  method); stale bond marks, cash drag, an internal crossing network and tax lots (an execution task type that serves
  descriptive work only, or a filed rule); advice-and-guidance conversion windows (the window is the WHAT); emergency
  department arrivals hidden behind the ambulance queue (loud, and patient flow is this slot's most measured cell).
- The rail draw's first harness (scratch t118v6/harness_rail.py, one day per world): two minutes of allowance before
  the terminus absorbed every overrun and the knock-on was zero; the Ambrey line was then given a minute of turnround
  slack in the morning, a strong reverse flow and half a minute of allowance before Ravelstoke Central.
- Two Ambrey line candidates whose overruns sat on the same morning trains (harness3 and harness4): the turnround term
  max(0, lateness less slack) is convex, so their joint saving was subadditive and the best pair flipped between
  redraws; the plan funds one team, so the call is one station.
- Early-morning overruns (before 07:00) reached the terminus too rarely to carry a knock-on (harness4); the knock-on
  candidate's overruns sit on the 07:00 to 09:30 all-stations trains.
- Candidates whose same-train figures sat within 1.15 of the cheap winners (redraw5, 20 jittered redraws at 20 per
  cent): the same-train route and the network, line and line-by-period reactionary scalings landed the knock-on
  candidate in 2 of 20 redraws; the generator holds Pellingham's same-train figure at least 1.3 times under Saltgate's
  and Ambrey Parkway's, so every scaled route stays off it.
- A three-minute minimum turnround (stab5): two minutes of slack absorbed Pellingham's lateness and Ambrey Parkway
  filed first; the minimum is a planning value every timetable carries, so the planning rules file four minutes and
  every late start in the running record sits exactly four minutes after its unit's arrival.
- The name "Airport line" for the line to Ravelstoke Airport: `guard.py check` BLOCKed tell.names against task467;
  the lines are named for their outer ends (Crossmoor, Ambrey, Holm Ferry).
