# leak check, task482

**Verdict: REVIEW.** 16 files read, 123 golden figures and 59 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, population, student, plausible, reader, decisive, reflex, report, family, students, readers, screened, selection, assessment, register, points, method, window, counted, standing, driver, contract, benchmark, record, missed

## 3 answer figures in the pack (REVIEW 15)
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 1000.00 appears: ...27-06-30,"Lumenfold subscription 2026-27, annual",1000.00,0.00,1000.00,Open, INV-261626,C-205108,Havwinmont...
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 875.00 appears: ...07-31,Lumenfold subscription seat true-up 2025-26,875.00,875.00,0.00,Paid,2026-09-29 INV-262582,C-206193,L...
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 262145 appears: ...ster 2 instalment",6887.50,0.00,6887.50,Open, INV-262145,C-204758,Delrowfield Local SD,2026-11-16,2026-12-...
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 261475 appears: ...nnual",16800.00,16800.00,0.00,Paid,2026-09-22 INV-261475,C-204520,Garterfield SD RE-2,2026-07-01,2026-08-1...
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 262013 appears: ...ster 2 instalment",4275.00,0.00,4275.00,Open, INV-262013,C-204184,Balrickwood City Schools,2026-11-16,2026...
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 262226 appears: ...ster 2 instalment",7200.00,0.00,7200.00,Open, INV-262226,C-204254,Corlinbury Local SD,2026-11-16,2026-12-3...
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 261830 appears: ...ster 2 instalment",4812.50,0.00,4812.50,Open, INV-261830,C-205626,Havdenstead Local SD,2026-11-16,2026-12-...
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 261702 appears: ...nnual",18525.00,18525.00,0.00,Paid,2026-08-04 INV-261702,C-205976,Merleywick SD 9,2026-07-01,2026-08-15,20...
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 262295 appears: ...ster 2 instalment",3675.00,0.00,3675.00,Open, INV-262295,C-204632,Kelnorfield ESD,2026-11-16,2026-12-31,20...
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 261203 appears: ...2026-27, annual",21600.00,0.00,21600.00,Open, INV-261203,C-204646,Lorleyford SD 8,2026-07-01,2026-08-15,20...
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 261645 appears: ...ster 2 instalment",5625.00,0.00,5625.00,Open, INV-261645,C-205108,Havwinmont City SD,2026-11-16,2026-12-31...
- **REVIEW** `billing_invoices_2026_27.csv`: golden figure 261680 appears: ...ster 2 instalment",7425.00,0.00,7425.00,Open, INV-261680,C-204905,Merganwick SSD,2026-11-16,2026-12-31,202...
- **REVIEW** `billing_invoices_2026_27.csv`: and 6 more golden figures
- **REVIEW** `caldrith_lsoa_technical_report_2026.pdf`: golden figure 17.5 appears: ...te Ohio -6.0 State Georgia -15.2 State Tennessee -17.5 State Colorado -2.7 State Arizona -11.4 Prior sta...
- **REVIEW** `caldrith_lsoa_technical_report_2026.pdf`: golden figure 21.5 appears: ....9 499.4 Georgia 4,703 24.7 492.8 Tennessee 3,374 21.5 487.7 Colorado 5,265 34.9 504.3 Arizona 3,775 21....

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `caldrith_lsoa_technical_report_2026.pdf`: 8 of 25 stump-paragraph terms appear (population, student, plausible, report, students, assessment); read whether the document names the move
- **REVIEW** `lumenfold_msa_v4_2025.docx`: 8 of 25 stump-paragraph terms appear (student, report, students, assessment, counted, contract); read whether the document names the move

## 6 ranking artifacts (REVIEW 4)
- **REVIEW** `billing_invoices_2026_27.csv`: names 19 of 59 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `order_forms_2025_26.xlsx`: names 58 of 59 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `pd_sessions_2025_26.csv`: names 20 of 59 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `renewal_forecast_2026_27.xlsx`: names 58 of 59 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `billing_invoices_2026_27.csv`: 109 ISO dates after 2026-11-24, e.g. 2026-12-31, 2027-06-30, 2027-07-31

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Round 1 (zip 632eeb37), two isolated readers (sonnet, medium, fresh copies), the six questions sent after each had
solved the task and been scored.

- Reader A: 1. MSA 9.2 and 9.3 define the test; the report's section 4 says how its own results are computed from the
  plausible values. 2. none. 3. the import layout and the crosswalk. 4. none (Table 8's 28.7 is national context).
  5. MSA 9.2 with 9.1, and the report's "Each result in Table 8 is computed five times ... averaged", which it carried
  to the districts: 19 districts. 6. an analytical choice, with a stated procedure doing part of the work. Sweep items
  a, b, c harmless.
- Reader B: 1. none ("No file says which step decides which districts are owed"). 2. none. 3. the technical report
  and the item parameters. 4. none. 5. the same two sentences, noting that the report "describes its own Table 8 and
  not the guarantee": 19 districts. 6. an analytical choice, with a partial overlap with a stated rule. Sweep items a,
  b, c harmless.

Ruling: no sentence names the decisive step and no file ranks the districts. Question 5's sentence is the report's
account of its own Table 8, scoped to it in the fix after the round 1 judge read; the readers carried it to the
districts by analogy, which is the default path, not a filed instruction. The REVIEW lines above (invoice numbers and
amounts the memo file applies credits to, two report figures that equal golden hours by coincidence, common vocabulary,
rows naming districts, forward due dates) are harmless.

## Round 2 readers (zip ce5456c3)

Reader D filed the default 19 districts (USD 32,045.00) and read the PD hours field as hours and minutes, keeping 98.2 per cent of ask weight. Reader C refitted the 2PL latent regression from the item responses with district in the conditioning model, checked the fit against the contractor's Table 6, and filed the golden 16 districts and USD 25,493.75; it kept 58 of 58 hours, 20 of 20 shortfall credits and 36 of 36 memo rows (score_reader exit 1). Architecture 11 is spent on the call.
