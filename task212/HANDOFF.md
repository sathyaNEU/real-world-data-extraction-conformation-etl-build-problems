# task212 handoff: paused by the author

**Status: PAUSED (2026-11-08), on the author's word. No session is working on it, and nothing resumes without the author.**
Wave 8, Anomaly Detection & Diagnostics. Architecture 2, stage 2 (design). No generator exists yet. Batch branch
`claude/jolly-hypatia-06c61h`. The detailed plan is `pipeline.json` (`resume` and `resume_stage2_plan`). The design is in
`DESIGN_NOTE.md`, and every dead approach is in its `## Tried and rejected`.

## Where it stands

### Architecture 1: spent at stage 4

- **The world:** Brujula Paqueteria, a fictional Spanish parcel carrier with six sortation hubs. One sorter-engineering
  survey goes out before the 2026 peak.
- **Domain:** General Statistics & Data Science, exploratory-data-analysis-distribution-assessment.
- **The call:** Ribarroja del Turia, about 800 damaged parcels a week.
- **Decisive step:** each parcel's crush load, rebuilt from the cage build log's load order and the weight scanner.
- **Round 1:** NOT_DETERMINISTIC on two asks (an unfiled flat-rate claim grain; a drifting safety-system clock). Fixed.
- **Round 2:** DETERMINISTIC with FIX_NOW (a work-order timing fork; "60 kg is the lowest BIC" did not reproduce). Fixed.
- **Round 3:** SEND_BACK on the weekly figure.
  - The programme filed "the estimate with the lowest BIC" over a family no document lists.
  - Adding the cage's total weight wins on BIC and gives about 600 a week, against the golden's 800.
  - Listing the family would have named the load, so the fork was the stump.
  - The hub was forced in every round, every ask reproduced exactly, and every judge filed Zaragoza blind. The stump was
    strong; the forward figure was not determinate.
- **Records:** `determinism_check_report_arch1.md` and `pipeline.json` `lineage_v1`. Architecture 1's generator is in git
  history (last at commit 26d4f91, `task212/generator/`).

### Architecture 2: current, stage 2

- **Domain:** Biomedical & Clinical Research, genomics-gwas-high-dimensional-association.
- **The world:** the Silverbirch Health Cohort (fictional, Ontario). Its 2026 genotyping release covers 47,800 buffy-coat
  aliquots from seven assessment centres. The biorepository director sends one handling audit before the February 2027
  ISO 20387 surveillance visit and the March 2027 collection restart.
- **The call (provisional):** the audit goes to Barrie.
- **The default path:** risk-adjusting each centre's genotyping failures on storage time, the LIMS freeze-thaw counter,
  the processing codes, sex and age sends it to Kingston.
- **Decisive step:** rebuild, from the custody log against the freezer map, how many trolley pulls each aliquot's rack
  took before the aliquot's own pick.
  - Every pick pulls the whole rack onto a trolley.
  - The multi-omics study swept Kingston's racks first, so Kingston's excess is storage warming.
  - Barrie fails DNA at about 1.8 times the others' rate from its own handling.
  - Every rack is pulled equally often, so only the order separates the centres.
- **Done:**
  - Card v2 is registered (guard WARN only), DRAWN at 40c09f8.
  - The design note is complete except the measured ask sheet.
  - `prompt.txt` is drafted (voice-check PASS).
- **Screens on the clean truth:** prototype `generator/prototype/h1.py`, 20 redraws on seeds 200 to 219, output in
  `generator/prototype/h1_out_200_20.json`.
  - The golden names Barrie 20 of 20 (lead 1.37 or more), and every golden variant does too.
  - The first look, every careful reader (a) to (e) and the literal execution of the filed WHAT name Kingston 20 of 20.
  - Fit parity: the easy route's AUC is 0.596 to 0.622 against the golden's 0.674 to 0.695.
- **precut:** exits 1, only because ceiling.py and checks.py do not exist yet.

## What needs to be done going forward

1. **Settle the rack-pull schedule before any generator code.**
   - The sweep schedule in `resume_stage2_plan` makes each middle centre's exposure a step in pick date. A table of
     failures by centre and pick week would show that.
   - Either build the prototype's local structure (each centre's multi-omics walk through the same participant order
     at a centre-specific lead or lag, drawn per rack, independent of pick date) and bring the card's `driver_concrete`
     and the note's world paragraph into line, or add a centre-by-pick-week reader and rerun the screens.
2. **Fix the rack size.** The prototype's unit holds about 27 released aliquots. A rack of 81 participants gives about
   590 release racks; 162 gives about 295. Then rerun every screen at 20 redraws on the generator's own world.
3. **Cite the effect level honestly.** Odds of about 4 after four to eight trolley sessions is at the top of the
   freeze-thaw record; cite it honestly or bring it into range.
4. **Re-price the asks.** On paper first, then with ceiling.py on the cut pack. The cracker and the full includer each
   keep at most 6 of the 16 ask figures.
   - Ask B needs both primaries re-sited. As filed, D6 is performed by the receiving SOP's own WHAT; D8 is still open.
   - Ask A's D4 (a walk back through the location history) is replaced, because careful solvers run that check
     unprompted.
   - D7 holds only if:
     - the 2025 holders of re-issued identifiers carry no aliquots;
     - each identifier's issue date is filed in the LIMS's and the registry's own form;
     - enough re-keyed participants differ in consent or centre that every figure in its block moves by several.
   - At least one ask holds both primaries against the full includer.
   - Ask B reads draw times from the manifest, never the LIMS inventory the call reads.
5. **Build:** the generator, checks.py, verify.py and ceiling.py (sharing no code), precut exit 0, then the stage-3
   gates. Stage 4 is the leak reader and the determinism judge together, on Sonnet at medium effort, each on an isolated
   copy.
6. **Before every guard run,** merge `claude/jolly-hypatia-06c61h` and copy any batch4 card your tree lacks into the
   cards folder, untracked.

## Binding lessons (from this build and its siblings)

- A graded figure built on a model-dependent estimate must land its bin under every defensible model, including each
  single covariate a careful analyst adds. A filed "lowest BIC" over an unlisted family is not a selection criterion.
  Never round an intermediate the filed text does not round.
- A governing document may file the estimand (what, who, when, the unit) but never the procedure. If a careful replay of
  every filed sentence reaches the golden, the decisive step is rule application (task214 architecture 1 died on Gate H).
- A golden handling that only consistency in the data reveals is unfiled: file the WHAT in the producing system's own
  voice, or change the world so every defensible handling gives one figure.
- PDFs are Word documents exported by LibreOffice Writer (`officepdf.py`, as in task482 on main): Producer
  LibreOffice, Creator Writer, a real Subject, the organisation as author, and no round-hour issue times.
- The prompt asks one question first, with at most one templating signal (files up front, steps, stacked questions, a
  closing list of documents, a dictated method, lists, UK spelling).
- **Risk:** the structure (exposure from other records' handling in a shared storage unit) is close to architecture 1's
  crush load. Keep the card's differentiation lines current and make the swap test read as this domain's own.
