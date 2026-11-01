# leak check, task281

**Verdict: REVIEW.** 16 files read, 29 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: device, camera, validation, architecture, relief, capture, reflex, analysis, method, distribution, golden, carries, register, decisive, pooled, family, window, closed, network, corpus, screened, nothing, history, service, budget

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `clinical_ai_governance_standard_v3.pdf`: 6 of 25 stump-paragraph terms appear (camera, validation, capture, network, screened, service); read whether the document names the move
- **REVIEW** `pellam_reading_agreement_2027.pdf`: 3 of 25 stump-paragraph terms appear (closed, network, service); read whether the document names the move
- **REVIEW** `validation_study_protocol_2025.pdf`: 4 of 25 stump-paragraph terms appear (validation, analysis, network, service); read whether the document names the move

## 6 ranking artifacts (REVIEW 4, INFO 2)
- **REVIEW** `biomed_asset_register_2026-09-30.xlsx`: names 4 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `biomed_service_tickets_2025-26.csv`: names 4 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `retinacheck_site_configuration_2026-10-01.json`: names 4 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `retinacheck_site_dashboard_2026q3.xlsx`: names 4 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `clinic_directory.csv`: names 4 of 4 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `retina_ai_results_2025-10_2026-09.csv`: names 4 of 4 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (the isolated leak reader, three rounds)

Every REVIEW line above is ruled harmless by the reader in each round; no round found a decisive-step sentence, a ranking file, a helper file or a figure that reads as the answer, and every round answered question 6 with an analytical choice.

### Leak reader, round 1 (2026-11-01, isolated, Sonnet at medium effort, on target.zip 11435654)

1. Decisive step: no sentence announces one; the nearest pointer is the validation protocol's site table (three pilot clinics), a fact, not an instruction.
2. No file ranks or scores operating points (the dashboard reports referable and ungradable shares at Standard only).
3. clinic_directory.csv (the key crosswalk) and retinacheck_operating_points.pdf (vendor thresholds the prompt needs): realistic, not suspicious.
4. Nothing reads as the answer: the configuration JSON shows every site at Standard (the current state); the agreement's 7,200 is the prompt's named capacity.
5. Standard s.3.1: the least sensitive vendor point whose sensitivity among the clinic's reference-year screenings is at least 85 per cent, the point estimate against the floor; s.2.1 (reference year by local capture date), s.2.2 (clinic of capture), s.2.4 (Ungradable counts as a referral), s.3.2 (referrals against capacity). These fix the estimand (WHAT); none says how to estimate sensitivity at the nine clinics outside the study.
6. An analytical choice decides it: how to estimate each clinic's sensitivity when only three clinics carry reference-standard data; nothing planted.
Sweep flags: all seven harmless (the standard files the estimand only; the vendor sheet is a tool fact; the protocol's site table is study design; the register, tickets, configuration and dashboard rank nothing).
Realism: none (mixed date formats, system-specific column names, clinic names differing across systems); a small note that every site shares one operatingPointSince date and one software version, plausible for a single rollout.

### Leak reader, round 2 (2026-11-01, isolated, Sonnet at medium effort, on target.zip 0837f761)

1. Decisive step: no file names it; the closest is the validation protocol's site table (three pilot clinics), which never says what to do for the others; CAI-03 3.1 asks only for sensitivity "among that clinic's reference-year screenings".
2. Nothing ranks or scores the operating points (the dashboard reports shares at the configured point; the configuration has every site at Standard).
3. No helper file outright (the clinic directory is an ordinary key crosswalk; the operating-points sheet's "the result ... at any other operating point can be read from its score" restates product behaviour).
4. Nothing reads as the answer (no point recommended anywhere; 7,500 is a stated limit).
5. CAI-03 3.1 (the least sensitive point whose point estimate among the clinic's reference-year screenings is at least 85 per cent), 2.4 (Ungradable counts as a referral), 2.1 and 2.2 (reference year by local capture date, clinic of capture), 3.2 (referrals against 7,500), Pellam 2.1 (a referral counts once), 3.3 (no qualifying point suspends autonomous screening). The method for clinics outside the three pilot sites is left open.
6. An analytical choice decides it (how to estimate or transport sensitivity to the other clinics; "the data separate the candidate methods"); rule execution weighs moderately.
Sweep flags: all eight harmless (the standard states what to compute, not the estimation method; the agreement, the operating-points sheet and the protocol are definitions, product documentation and study design; the register, tickets, configuration and dashboard rank nothing).
Realism: none from what was sampled.

### Leak reader, round 3 (2026-11-01, isolated, Sonnet at medium effort, on target.zip 314f3a3b, after the forum redraw)

1. Decisive step: none stated; the protocol's derive-from-score sentence describes how the study data were made and does not say how to estimate sensitivity at the nine clinics outside the pilot.
2. Nothing ranks or scores the operating points (the dashboard reports Standard-point volume and rates only).
3. No helper file (the vendor's thresholds and derive-from-score note read as context).
4. Nothing reads as the answer (the configuration JSON's Standard at every site is the current state).
5. CAI-03 3.1 (the least sensitive point whose point estimate among the clinic's reference-year screenings is at least 85 per cent, no confidence bounds; precision reported to the Chief Medical Officer separately), 3.2 with the agreement's 7,500, 3.3, definitions 2.1 to 2.4: the WHAT; the estimation method is left open.
6. An analytical choice decides it (how to estimate sensitivity from selected, partly verified data); no sentence names it.
Sweep flags: all seven harmless.
Realism: no file clearly reads as generated; two neat points: one operatingPointSince, software version and ungradable handling for every site in the configuration JSON (plausible for a single rollout; the result rows' earlier 4.2.1 against the export's 4.3.0 reads as an upgrade during the year), and short, tidy policy PDFs.
