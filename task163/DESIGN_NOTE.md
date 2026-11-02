# task163 design note

Architecture 2, drawn 2026-11-02 (wave 6, Forecasting lane), a re-root of architecture 1 (seed FC34's payroll company,
spent on its ask layer; its record is below and its full note is in git history). New client domain, world, dataset,
generator and shell. The two ask records and their mechanics were chosen and screened as code before the call was
fixed (the brief's ask-first rule), and the call was then drawn in the same world.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task163.json`, architecture v2, registered 2026-11-02; `guard.py check` on
   the registered card PASS (two NOTEs, differentiated; item 11).
2. Pairing: Human Factors & Ergonomics (client domain) / `human-reliability-assessment` (F) / Forecasting & Predictive
   Modeling. The deciding quantity is an unrecovered human error rate: a picking error's own probability per
   opportunity times the probability that the downstream check fails to recover it, the form human reliability
   assessment gives a task with a check. The house domain a warehouse would sit in (supply-chain-logistics) maps to
   urban-regional-science and general-statistics-data-science, neither of which carries a human error estimate.
3. World: Lathmor, a third-party logistics company, picks the online orders of Aubrine (a UK cosmetics and fragrance
   brand) at its Uphall fulfilment centre in West Lothian, from about 1,800 pick faces in four zones (A, carton flow
   for the fastest lines; B, C and D, static shelving). Every parcel is check-weighed at the pack benches against the
   item master's unit weights and the carton's tare, with a fixed tolerance; a parcel outside it is held and re-checked,
   so a mis-pick reaches a customer only when it passes. Aubrine's customer service logs the claims; the contract's
   order-accuracy KPI caps validated mis-pick claims per 10,000 order lines in a contract year. The slotting
   consultant's plan re-slots zones B to D by product family over the Christmas shutdown, live in January 2027, to cut
   pick travel. People (`guard.py names --geo GB --seed 163`): Kathryn Tomlinson, Lathmor's head of quality at Uphall
   (the stakeholder, never named in the prompt); Brian Cook, Lathmor's account director for Aubrine; Hazel Collins,
   Aubrine's head of e-commerce operations; Kayleigh Ward, the returns bench team leader. Invented names: Lathmor,
   Aubrine, Corsley (the staffing agency), Ravelrig (the repack partner).
4. The call: how many validated mis-pick claims Aubrine's customers will lodge on the order lines Lathmor picks in
   calendar 2027 under the re-slot plan, the claims per 10,000 lines against the KPI, and so whether the plan can go
   live as drawn (`quantity_figure`, count, how-many). Forward facing: the window opens in January.
   **Lesson 10, the fork-is-the-stump test on the WHAT, run now.** The filed WHAT names the claims (validated, on lines
   picked in 2027), the lines (the plan's forecast), the year and the KPI's ratio. The forks a judge would raise (claims
   lodged in 2027 against claims on 2027's lines; validated against lodged; the plan's lines against grown 2026 lines)
   close with sentences about claims, lines and dates. None names a weight, a tolerance, a neighbour or the check-weigh,
   which is what the decisive step recognises, so filing the WHAT hands over nothing.
   **Lesson 11.** No shipped document states a rate, factor, benchmark or design value the easy route can apply to the
   2027 claims: no accuracy benchmark, no "expected impact" line in the plan (it states travel only), no contract
   assumption of a claims rate. The KPI cap is a threshold the forecast is read against, not a rate it is built from.
   The easy route's rate is the analyst's own fit (claims per line), and the data's own fit refutes it (item 6).
5. Default path, in one line (written in full at stage 2): carry the twelve months' validated claims per 10,000 lines
   picked onto the plan's 2027 lines, about 140 claims and 1.2 per 10,000, inside the 2.5 KPI. Golden, design target
   about 340 and 2.8 per 10,000, over it. Rung 1, the look-alike reflex (human reliability assessment's performance
   shaping factor for similar items side by side), fitted on the same claims beside same-line or same-family
   neighbours: about 100 or 180, both inside. Toy screen of the ladder: scratchpad `task163_a2/task163_screen_main.py`
   (rung 0 140.1, same-line multiplier 97.8, same-family multiplier 175.8, golden 344.1 at 2.82 per 10,000; the
   plan lifts the weight-alike share of picks from 0.166 to 0.408 while the error rate per pick is held).
6. Stump sentence (draft): carrying the twelve months' claims per 10,000 lines onto the plan's 2027 lines files about
   140 claims, inside the KPI; the step that lands it there is treating claims as a fixed share of picking, when they are
   only the mis-picks the check-weigh lets through, which happen only where the item beside the ordered one weighs
   within the tolerance of it, so the re-slot that puts each line's shades side by side raises claims with no change in
   how often pickers err; only the claims per weight-alike neighbouring pick, carried onto the plan's faces and lines,
   gives about 340. Data-native sentence: the claims are the residue of a physical filter (a scale against a tolerance)
   applied to errors whose form a shelf layout fixes, so a count kept per line is stationary only while the layout is.
7. Shape and deliverables: shape `other`: the call (claims under the plan, per 10,000 lines, the verdict against the
   KPI), its comparison (the current layout's 2027 claims) and its zone split, then two decoupled ask tables. Tentative
   files: a workbook and a chart (`reslot_claims_2027.xlsx`, `reslot_claims_2027.png`); the shell is drawn with the
   prompt at stage 2 and must differ from architecture 1's (how-many, put, docx+xlsx).
8. **The ask records, chosen first, each with the domain mechanic that forces its reading, screened as code against
   the honest cracker before any data is cut** (scratchpad `task163_a2/task163_screen_asks.py`, toy data):
   - **Ask A, Corsley's weekly agency invoices** (scheduling and pricing). Each weekly invoice bills every agency
     worker's hours by day at the base charge rate; the night and Sunday uplifts are settled on one unlabelled
     "premium reconciliation" line on the first invoice after each of Corsley's four-week pay periods closes, the
     periods running Monday to Sunday and crossing month ends. The ask: what an agency hour worked cost in each month
     of the twelve (the rate the plan's travel saving is valued at). Only one alignment makes the lines an identity
     with two constant uplifts: the 28 days ending the Sunday a week before the invoice (worst residual GBP 0.00,
     against 504.07 for the 28 days to the Sunday before and 1,462.17 for the previous calendar month). The cracker
     that books each line by its date misses 12 of 12 months to the penny; the cracker that reads the line as last
     month's arrears (the reflex repair, the over-cleaning half) misses 12 of 12; the full includer hits 12 of 12.
     Told reader: told the premiums are periodic, it still has to find the period by fitting two unknown uplifts over
     candidate windows; no join, sort or uniqueness test performs it. Mass to widen at stage 2 (toy smallest gap 1.9p).
     Family: a catch-up half settled in a later period's line (the 151 family), on a pay-period grain no label states.
   - **Ask B, the returns bench's grading log with Ravelrig's monthly repack bills** (pricing). The bench grades every
     returned unit 1, 2 or 3; the handheld app that replaced the paper sheets on 8 June 2026 kept the codes but swapped
     the meanings of 2 and 3 (paper: 2 repack, 3 scrap; app: 2 scrap, 3 repack), and the bench's procedure on file
     carries the app's legend only. Ravelrig bills each month's repacks as one amount at constant contract rates by
     pack size (no unit counts, no rates on file). The ask: the share of returned units repacked and scrapped and the
     stock value scrapped, by product family (what each claim's wrong item costs when it comes back). Only the old
     legend before 8 June fits the bills to the penny at constant rates (worst monthly residual GBP 0.00; the filed
     legend all year 7.54, the old legend to 30 June 5.32 in the toy, both to widen at stage 2). The filed-legend
     cracker misses 13 of 20 toy figures; the resell share does not move under the swap, so the ask drops it and keeps
     the repack share, the scrap share and the scrapped value (15 figures, each moved). Over-cleaning half: a solver who
     swaps the codes to the end of June, or for the whole year, misses (11 and 13 of 20). Told reader: told the codes
     changed, it still has to find which codes and from which day by fitting the partner's unknown rates.
     Family: a label stored before a silent switch (D2), read through a partner's bills.
   - Both sit outside the main population: the call never reads an invoice, a return or a repack bill. The two
     families are disjoint and neither is on the brief's list (checked one by one: no person under two keys, no lent
     device, no re-keyed asset, no refiling, no scale per source, no capacity cardinality, no reference basis, no
     physical repair on every row, no visit placed by a purchase, no blank status read through a counter, no gauge
     rise, no silent meter, no blanket charge placed by hours, no bypassed meter, no pack size against fill weights, no
     subset-sum credit, no duct temperature). Suspicion test: the asks' nouns are an hour's cost and a returned unit's
     fate; neither invites a pay-period grain or a code switch.
9. Mechanism keys: gap population (the claims file is not the errors and the lines are not the exposure: the claims
   are the errors that survive the check, and their exposure is the picks whose neighbour the check cannot tell
   apart); decisive generator G9 (downstream survival against upstream acquisition), then G14 (the escape yield
   conditioned on the neighbour's weight gap) and G6 (the plan shifts the neighbour mix); Gate G `forecasting`;
   strategy `forecast_method_backtest` (stumping F6: a rate stationary only in a constructed exposure, the per-line
   rate back-testing clean on the stable layout and failing forward); Layer 2 `estimation_fit` (survivorship: the
   observed errors are the ones a filter passed), pattern `own:unrecovered-error-rate-per-check-passable-neighbour-opportunity`;
   calibration `physical_verification` (the check-weigh's own exception log, which counts the errors it caught and so
   pins the error rate per pick independently of the claims); context artifact `register` (Aubrine's claims register).
10. Lesson 7, the golden's assumptions, each asserted in checks.py on the shipped rows: the error rate per pick does
   not move with what sits beside a face (caught mis-picks per non-alike opportunity equal beside same-line,
   same-family and other neighbours; claims per alike opportunity equal across them); a mis-pick takes the left or right
   face of the same shelf run with equal chance and never a face above, below or across the aisle; no neighbour pair
   sits within a few grams of the tolerance, so scale and tare variation cannot move a pair across it; the reporting
   share of escaped mis-picks does not move with price, family or zone; no contamination cluster (a wrong item put away
   in a face) and no trend in the error rate across the twelve months; the tolerance and the pack benches unchanged in
   2027; every 2027 face in the plan holds an SKU with a 2026 history or a forecast on the plan's own sheet.
11. Guard: PASS on the registered card. NOTE test.same_puzzle_older and test.same_driver_older against task156's first
   architecture (a closed pool's leaving rate by tenure) and task452 v2 (design-weighted reference observations),
   differentiated on the card. Axes redrawn at the draw: context artifact `register` (monitoring_export met task458's
   ban), forcing event `cutover_or_migration` (launch_or_rollout met task458's), generators led by G9 (G14 first met five
   older same-signature builds; G6 first met task453's pattern ban and this slot's own lineage), validated_decoy false
   (no certified record blesses the per-line route; two_layer.validated_decoy refuses one). WARNs answered: Russell
   (first name in task460) replaced by Brian Cook; the pdf+xlsx deliverable set (task453 v3) moved to xlsx+png.
   Nearest drivers 0.05 (task149, task251 v4, task455 v1, task173 v3, task446 v2). `slots` on the driver's and the
   setting's nouns: task194's rejected candidate (a unit's own defect rate seen through a downstream check whose catch
   moves with its load, killed because caught plus escaped makes the rate unlatent and the escapes too thin to rank) and
   task107 v1 (the share of past failures a new check could have stopped, by delivery kind) are the nearest screens;
   here the check is fixed, the error rate is pinned by the caught log on purpose, and the forward count turns on the
   forms a new layout puts within the check's blind band, which neither screened. task44 (a fulfilment campus's
   carton-flow faces) and task229's Thornacre lineage (pick-face record accuracy) share the setting, not the mechanism.

## Architecture 1 record (spent 2026-11-02)

Economics & Econometrics / forecasting-forecast-evaluation: Kilbourne Payroll's 2027 first-time employers across twelve
states after three states put the employer-number application inside their formation filing; the call 2,500 (the
added applications' yield read against the nine other states before and after), the default 2,800. The call held
through three determinism rounds (DETERMINISTIC, APPROVE). The ask layer measured spent under the honest cracker
(29 of 29 kept, pair 83.5) and no re-site or full replacement passed both device tests, so the slot re-roots with a new
world, dataset, generator and shell. The full architecture 1 note, generator and pack are in git history (commit
7ea9cab and before); its card identity, fate and shell are in the card's lineage.

## Tried and rejected

- Completing the surge cohorts' formations from their own early formations at the closed cohorts' development pattern (a chain ladder on the formation triangle): rejected at the draw, the same latent structure as task157 (a cohort's size from its leading edge at a timing ratio earlier cohorts kept).
- A first-payroll hazard by months since registration applied to a pool the surge filled: rejected at the draw, task134 round 1's driver.
- A formation lag that lengthened after the reforms, so the closed cohorts' four-quarter rate reads a delay as a loss: rejected at the draw, the development-speed change task451 spent.
- The high-propensity flag as a screen whose yield moves with the base rate of genuine employers: rejected at the draw, task446's driver.
- A one-time formalisation wave at each launch that will not recur in 2027: rejected at the draw, a dated cause whose effect steps a series is found by an event study.
- A timely calendar formation series in the pack (state new-employer registrations or the company's 2026 first-timers): rejected at the draw, carrying the latest twelve months forward lands within a bin of the golden.
- Two more states opening the integrated filing inside 2027 as the forward change: rejected at the draw, the formation effect of a launch inside its first year is under a bin of the call.
- The round-1 world (go-lives in 2024, a common rise from mid-2023 to mid-2024, the line at 2,300): retired at stage 4 round 1, the formation-only routes (lines through the closed formations, annual totals, the rate per application from July 2023, 2025 grown by formation or application growth) landed on the golden, because the closed cohorts already carried the common rise at nearly the twelve months' slope.
- The audit's shared autumn 2025 rise (9 to 12 per cent) added to that world with its 2023 to 2024 rise kept: rejected, 12 to 22 of 62 bypass routes stayed within a bin (formation lines from 2023, the rate per application on a line, the nine states' application growth carried).
- The earlier common rise moved to calendar 2022 beside the autumn wave: rejected, the reform states' own pre-go-live level then held the rise, so the before-and-after split (0.15 bins) and a formations-on-applications regression with month terms (0.11 bins) landed within a bin.
- A larger added yield (0.30 of the ordinary rate) with go-lives from August 2023 and slow take-up: rejected, 21 of 62 routes within a bin (the formation lines and the before-and-after split within 0.12 bins), since a larger yield closes the gap between the blend and the split.
- A voluntary take-up of 0.35 to 0.50 before the older routes closed: rejected, the rate per application on a line from January 2023 lands within 0.3 bins (the voluntary plateau sets the closed rate's trend near the twelve months' mix).
- Go-lives from July 2023 to January 2024 at a low take-up (0.25), and go-lives from April 2023 on an extract from January 2022: rejected, the counterfactual rested on too few months before go-live and the bootstrap's 95 per cent interval spilled out of the bin (sigma 22 to 29); the extract from January 2021 and go-lives from January 2023 give 24 to 30 months before go-live.
- Counterfactual and ordinary-rate bases fixed at 2022 to 2023 for every state once go-lives moved into 2023: rejected, the base then held post-go-live months and widened the family past an edge; every base now ends the month before the state's own go-live.
- A per-state joint regression of formations on ordinary and added applications as a seventh estimator: dropped, the two move together inside a state after go-live, so its coefficients are not separately identified and its spread (2,506 to 2,545 in the sweep) is the collinearity, not a reading.
- Later retirements of the older routes (December 2025 to April 2026): rejected, at take-up 0.35 or more four to nine routes fell within a bin, and at 0.30 the nine states' application carry sat at 1.02 bins, too close to hold on another seed.
- Calibrating the company's size to the family's midpoint: rejected, the line sat low in its bin and the bootstrap interval's margin was 1.5; the rule now targets the line at the bin's centre (2,500.5), written before the outcome.
- A calibration stop within 1.5 of the target: rejected, one business added or dropped at the margin moves the line about 3.6, so the rescaling oscillated between 2,499.0 and 2,502.6 without settling; the stop is 2.0.
- EINs drawn at random per business: rejected, two businesses drew the same EIN and the share tab no longer tied to the export; EINs are issued unique.
- Added applications more than doubling the reform states' applications once the older routes closed (full take-up above one added application for every ordinary one, routes closing from October 2025): rejected at stage 4 round 2 on the judge's realism read, since a one-stop filing that more than doubles a state's business applications reads as engineered; full take-up now adds about seven for every ten ordinary applications, the routes close January to March 2026 and the added share of the twelve months is about a third.
- Added applications set apart from the ordinary on the published flags (lower high-propensity and planned-wage shares, so a flag route priced them): rejected at stage 4 round 2 as an engineered tell; the added applications carry the ordinary high-propensity and planned-wage shares, and the flag routes miss on their own (2,800 on the latest four closed quarters, 3,000 on every closed cohort).
- Pushing the two-way fixed-effects panel of formations on applications and the post-go-live regression with month terms a bin off the golden: rejected at stage 4 round 2 after about 45 harness worlds and four seeds, both land within 0.6 bins in every world because state effects learn the slope from the voluntary step at go-live; they read the comparison in regression form, so they sit in the construction family, asserted inside the golden's bin.
- An added share of 0.40 to 0.45 in the twelve months to clear the growth carries and the own before-and-after: rejected at stage 4 round 2, it needs full take-up above one added application per ordinary one (the doubling) or the older routes closing in autumn 2025, which drags the twelve-state carry back in; at a third the own before-and-after, the regression through every closed month and the nine-state January-to-September carry sit 0.6 to 0.7 bins off and round to 2,400.
- The liability record, tax filing only and the legacy code as the asks' silent primaries once the judge's pins filed them: rejected at stage 4 round 2, the pins hand all three to the cracker (its pair measured 48.5); the silent primaries are now the migration load's client-since date in first_pay_date, which only the wage files contradict, and the legacy re-key of a mistyped EIN.
- The legacy re-key with the state registering the corrected EIN afresh for any business: rejected at stage 4 round 2, a business that had employed before is on the state's books under its correct EIN, and re-registering it let the re-key add about as many accounts to a territory's 2024 count as the client-since date took out, so the cracker's Indiana-Kentucky count landed on the golden by offset (207 against 207); a fresh registration is now limited to businesses first employing through us, and the two devices pull every territory's count the same way.
- A third silent count device so that a response cracking both count primaries stays under 45 (47.7 measured, group 00 moving only the wages): not built at stage 4 round 2, since no further mess the company's systems write moves the counts apart from the first payroll and the business's identity, and a contrived one would read as planted; the pair table records it beside the both-on-call floor of 48.3.
- Rounding the share tab's stored shares to four decimals for a finance workbook's look: rejected at stage 4 round 3, the standard prices each state at its share in the plan workbook, so stored rounded shares would move the exact line from 2,499.6 to 2,500.4 and figures.json with it; the shares are now formulas over the tab's own counts and bases, shown to two decimals of a per cent with the results Excel stores.
- Moving the early 2026 rise off the three closings (a rise from October 2025 to January 2026): rejected in the round 2 harness and left at stage 4 round 3, the twelve-state growth carries came within 0.62 bins of the golden and the own before-and-after within 0.46; the rise ramps January to April 2026 with every closing inside the ramp, recorded as the residual in the pre-ship check.
- The pack's field guide (plan_pack_field_guide.xlsx, every data file's fields and codes) and manifest (pack_manifest.csv, each file's owner, source, date and cover), shipped to 18 October: retired on 1 November under the new leak gate, since no shipped file describes the data. Provenance moved to metadata.json; the legacy wage report's cents into its own column (gross_wages_cents); the closed cohorts, the series codes and the migration quarter's split left to the release's and the wage files' own rows (asserted); and the one ask rule the guide carried, a migrated account's channel from its legacy referral code where the load had given CPA, BP, TEL and APX the default web sign-up, closed by convergence in the data: the load now maps every code, so the export's channel is the golden's (SF15, asserted). No call or ask figure moved.
- The ceiling recorded on the reship cut was a narrowed cracker's (2026-11-01, honest-cracker audit): the careful solver, every field read by its plain meaning, every filed rule executed and the hygiene battery run, keeps 29 of 29 against the recorded 0 of 29, SPENT on Asks A, B and C, pair 57.7 (83.5 with the mirror on the honest route); the reason in one line: the anti-join on first_pay_date's quarter against the wage rows (179 migrated accounts), the counting notes' 'whatever its account or EIN' linking the re-keyed businesses, pay group 00 equal to 01 plus 02. The ask layer is owed a /fix-rubric pass before delivery; the leak repair stands.
- Re-siting the spent asks inside the files they read (2026-11-02, the /fix-rubric pass, each screened as code on the generator's own world before any cut): reciprocity home-state withholding registrations moving a business's first-employed state (a geography and tax-law link: a resident of a reciprocity partner has the home state's tax withheld, with no UI account there) die twice, since the home-state row ties the work-state row on the first payroll's date and the address-state tie-break a careful solver reaches for misplaces 1 of the 113 cohort businesses carrying one (file order 50), and the same law runs in the 2025 cohort, where the earliest-registration reading moves the share tab's counts by state (IN +30, KY +19, OH -23, PA -16), so the call's own input would be the device's oracle; a new company's first payrolls under its owner's legacy client, split out at the migration (a child under its parent's client number), is unforced, since the state dates the child's first wages under its own EIN and nothing shows they ran with us rather than elsewhere; a quarter-to-date balance load in the migration quarter is the battery's carried-over record across two systems (each such client's pay dates would overrun its frequency's quarter).
- The full replacement on new ask-only records (2026-11-02, step 4b), built as a prototype outside the pack and measured: the payroll tax team's new-hire report log, asking how many people each territory's 2024 first-time employers took on in 2025 (in whole people), the WHAT drafted for the counting notes ("A person a business took on in a year is someone who started working for it that year, counted each time they started."), the device the reports a successor's or a returning account files for the staff it carried on (a new FEIN requires them), the over-cleaning half the rehires; forced (the notes make the re-formed business the same business, and each carried person's earlier report is the predecessor's), and every natural careful route misses 6 of 6 (every report, distinct people, the first report only), but the told reader lands 6 of 6 with a person repeat and a date match on the new account's first pay date, the battery's re-keyed-record match applied to employees, and South and Plains carries one device row: spent. Screened and not built: fees on a billing export with an affiliate billed on its parent's invoice (the child's payroll with no invoice is an anti-join orphan and the parent's lines name it), fees billed in arrears (an invoice after an account's cancellation is a row after a system's close), the partners' payouts by channel priced at a share of the client's fees (one client under a partner's key priced on the account's fees, task447's family), commissions on multi-entity deals (the plan's per-business bonus, a reconciliation to a filed schedule), SUI rate notices with an inherited rate (the counting notes file status by the liability date, so the literal rule and the rate disagree, and the 2025 cohort carries the same mechanism into the share tab), 2025 W-2s across a re-formation (the carried staff are not in the per-EIN totals, unrecoverable), a legacy run archive dated by processing for a monthly phasing (forced only at quarter ends), employment on 12 December from the UI reports (the plain read is right). Cutting the spent asks leaves 7 criteria (the call, its four components, the two files), under 25. Owed: the author's call, a new ask layer on records this world would hold, designed at stage 2 and screened as code against the careful-solver cracker before any data is cut, or a re-root of the asks; the leak repair and the determinism record of the reship stand.
- 2026-11-02, architecture 1 re-rooted: its call held and its ask layer measured spent (the careful solver keeps 29 of
  29, pair 83.5), no re-site or full replacement passing both device tests; the world, the dataset, the generator and the
  prompt shell all move (architecture 2: Human Factors / human reliability assessment, a 3PL's mis-pick claims under a
  re-slot), the ask records chosen first.
- The world search for architecture 2 (2026-11-02), each candidate killed on paper before any harness: a pension
  scheme's payroll (a spouse's pension equal to half the deceased member's, the guarantee lump sum equal to the
  instalments left; strong ask links) had no main call that was not a reflex or a composition (commutation take-up
  against the factor, the payroll's run-off, deaths with a notification lag); consumer and motor lending (interest that
  dates a payment's value day, an instalment that reveals an unrecorded term change) had only reflex calls (roll rates,
  equity-driven hand-backs, refix shock); a district heat network's return temperature and a bus network's timed
  transfers had fresh calls but ask records in the banned meter and presence families.
- Ask devices screened in this world and rejected at the draw: a returns label reused for a later claim (the return
  booked under an old order; a join on customer, SKU and date performs the link, so a told reader lands it); a carrier's
  late-billed tariff increase (the same catch-up family as Ask A, and a filed rate card's reconciliation finds it); the
  grade switch read through waste transfer weights (a recorded attribute contradicted by a weight, the banned family);
  the repack partner's bills with unit counts (a count pairing performs it, so the bills carry amounts only); re-sends
  sent by another carrier and absent from the main carrier's invoices (an anti-join performs it); an agency worker's
  12-week parity (the charge rate states the tenure); a carton read from the carrier's dimensional weight and two orders
  in one parcel read from a weight sum (banned families: a measured weight against a master, a subset sum).
- The look-alike multiplier as the golden (human reliability assessment's performance shaping factor for similar items
  side by side, fitted on claims beside same-line or same-family faces): rejected at the draw as the field's reflex; it
  sits at rung 1 and files about 100 or 180 against about 340, because the current layout's same-line neighbours are a
  line's sizes (never weight-alike) while the plan's are its shades, and the caught exceptions show no rise in the
  error rate beside look-alikes.
