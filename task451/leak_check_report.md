# leak check, task451

**Verdict: REVIEW.** 11 files read, 33 golden figures and 16 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: decisive, member, months, development, process, triangle, window, asserted, ladder, method, roster, latest, agreement, history, version, design, paid-date, rejected, changed, attributed, service, received-date, administrator, received, adjudication

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `accountable_care_partner_agreement_schedule_b.pdf`: golden figure 2.0 appears: ...exceeds its Target PMPM in Exhibit 1 by more than 2.0 per cent, the Partner pays the Fund a shared-los...
- **REVIEW** `accountable_care_partner_agreement_schedule_b.pdf`: carries 19 of 20 distinctive words of the committed call: 'Four of the twelve partners owe the Fund a shared-loss payment for 2026: Stonecrest Internal Medicine, Bellmont Clinic N'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `accountable_care_partner_agreement_schedule_b.pdf`: 8 of 25 stump-paragraph terms appear (member, months, process, roster, agreement, attributed); read whether the document names the move
- **REVIEW** `corvane_claims_file_layout_v4.pdf`: 3 of 25 stump-paragraph terms appear (member, version, adjudication); read whether the document names the move
- **REVIEW** `keswold_extract_dictionary_2027-02-01.txt`: 6 of 25 stump-paragraph terms appear (member, process, latest, version, service, received); read whether the document names the move
- **REVIEW** `laurelford_data_notes_2027-02.docx`: 5 of 25 stump-paragraph terms appear (member, months, roster, version, administrator); read whether the document names the move

## 6 ranking artifacts (REVIEW 3)
- **REVIEW** `accountable_care_partner_agreement_schedule_b.pdf`: names 16 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `partner_clinician_roster_2027-01-01.xlsx`: names 16 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `partner_quality_scorecard_2026.xlsx`: names 16 of 16 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

Reader pass 1, 2026-10-13 (isolated, Sonnet, medium, fresh copies of prompt.txt and target/ only).

## Solver's-eye read

### 1. Sentence naming the decisive step
Nothing names the step outright. The nearest is B.3.1 of accountable_care_partner_agreement_schedule_b.pdf: "The Fund estimates the claims incurred in the Performance Year and not yet paid from its claims data." It tells me an estimate of unpaid (incurred-but-not-reported) claims is part of the reconciliation, but it gives no method, no completion factor, and no instruction on how to apply it to the settlement. B.1.4 ("... with a first date of service in the Performance Year ... whenever the claims are paid") sets the incurred basis. Together they point at claims run-out but do not say to complete the January-paid figures, how, or that the call would flip. The prompt's "now that claims paid through January are in" is a hint at the lag but not the step. Verdict: no sentence announces the decisive step.

### 2. File that ranks or scores the twelve partners on the question
None. The agreement lists Target PMPMs only. The clinician roster and quality scorecard list partners beside non-cost numbers (tenure, quality scores). The quality score only matters to the savings side (B.2.2), not to who owes a shared loss. No file gives TCOC, PMPM against target, or an owes/does-not-owe flag.

### 3. Helper file the organisation would not really have produced
None. Every file is plausible as the Fund's or a vendor's own: Keswold extract dictionary, Corvane layout, Laurelford data notes, clinician roster, quality scorecard, stop-loss policy summary, attribution roster, eligibility spans, claims. The data notes are the most explanatory but read as a normal Fund Office note about member ids, spans and the roster, and they do not touch the cost computation.

### 4. Figure or name reading as the answer
None. No TCOC PMPM, shared-loss amount, or owes flag appears anywhere. Exhibit 1 Target PMPMs, the 2.0 per cent threshold, the 40 per cent share and the 4 per cent cap are contract terms, not results. The quality scores in the scorecard are marked "Preliminary".

### 5. Filed sentences that fix the computation or population, and their literal consequence
- B.1.2/B.1.3 "Attributed Member Month means a month in which a Member is eligible for the Fund's medical benefits and appears on the Fund's attribution roster for the Partner for that month. The roster is run on the first day of each month..." Consequence: the denominator counts member-months that are both eligible (from the eligibility spans, using latest versions, so retroactive terminations and reinstatements matter) and on that month's roster; the roster is not rerun for later eligibility changes (data notes), so the intersection must be taken.
- B.1.4 "Total Cost of Care means the Fund's paid amount for covered medical services (professional services and outpatient and inpatient facility services) with a first date of service in the Performance Year, for Members attributed to the Partner in the month of that first date of service, whenever the claims are paid. Outpatient prescription drugs ... are excluded." Consequence: incurred basis by service_from_date in 2026, attributed by the month of the first service date, so claims paid after January 2027 are in scope in principle (hence the need for completion); pharmacy excluded; use the paid_amount of each claim's latest version (extract dictionary).
- B.1.5 "Where a Member's amount under B.1.4 for the Performance Year exceeds $200,000, the amount above $200,000 is excluded. For a Member attributed to more than one partner group during the year, the excluded amount is shared in proportion..." Consequence: a $200,000 per-member cap, not the $175,000 stop-loss deductible; applied to the member's year total, with the excess split pro rata across partners.
- B.1.6 "TCOC PMPM means the Partner's Total Cost of Care ... after B.1.5, divided by its Attributed Member Months for the year."
- B.2.1 "exceeds its Target PMPM in Exhibit 1 by more than 2.0 per cent ... 40 per cent of the amount by which its TCOC PMPM exceeds its Target PMPM, multiplied by its Attributed Member Months, but not more than 4 per cent of its Target PMPM multiplied by its Attributed Member Months." Consequence: owes only if PMPM is more than 102 per cent of target; payment is 40 per cent of the excess, capped. Owing is the yes/no that matters.
- B.2.3 "The comparisons ... are made on unrounded figures."
- B.3.1 "claims its claims administrator has paid through the last business day of January following the year. The Fund estimates the claims incurred in the Performance Year and not yet paid from its claims data." Consequence: the reconciliation uses claims paid through the end of January plus an estimate for unpaid incurred claims; the estimate method is left open. (This is the literal text a judge must read as requiring completion.)
- B.4.1(a) pharmacy: "the Fund's net payments to its pharmacy benefit manager for prescriptions filled in the Performance Year in the Members' Attributed Member Months with the Partner". Consequence: plan_paid net of reversals (B2), fill-date in 2026 and Attributed Member Month of the fill; person_code/cardholder id must be mapped to member ids.
- B.4.1(b) "the share of the Fund's paid amount for the professional services in its Total Cost of Care, before B.1.5 and as paid through the reconciliation date, that was for services rendered by clinicians who were not with the Partner group when the service was given." Consequence: professional claims only, paid through January (no completion), before the cap, by rendering clinician status on the service date.
- Keswold dictionary: "The claim's value is the paid_amount of its latest version." Consequence: de-duplicate to the latest version, with frequency code sets differing by platform (O/A/V versus 1/7/8).

### 6. What decides the main answer
An analytical choice. Mechanical steps are heavy but readable from the documents: versions, member id mapping, attribution join, the cap, thresholds. After doing all of these literally on the paid-through-January data I could still reach a wrong owes/does-not-owe list, because late-2026 service months are incompletely paid and the agreement requires estimating claims incurred and not yet paid. The easy route (take the paid-through-January totals) would understate PMPM for partners near the 2.0 per cent line. The quantity to estimate (completion from the paid-date lag in the claims data) is a real actuarial method, and the text names the need but not the method. It is not a single field or code reading and not a planted defect; B.3.1 is the only sentence pointing at it. The prompt's reference to claims paid through January is the only other pointer, and it does not say that the figure must be completed. The stop-loss policy ($175,000, 12/15 basis) is a near-miss distractor against the $200,000 cap in B.1.5; the $200,000 cap is stated outright, so it is rule application and not the decision.

### 7. Realism
None that reads as constructed. The layouts, version/frequency codes (Tallis versus legacy), release notes, names and roles read like real vendor documents. Minor observations only: the quality scorecard and clinician roster are tidy single-sheet workbooks with a title and note row, and the data notes are unusually clear about the roster not being rerun, but both are plausible for a small Fund Office. Metadata authors on the workbooks are the named Fund staff (Ariel Hogan, George Khan), consistent with the documents. No hidden sheets.

### Sweep verdicts
- schedule_b.pdf "2.0 per cent": harmless. It is a contract threshold the solver needs, and a number from the contract, not a result.
- schedule_b.pdf vocabulary overlap with a sentence naming the twelve partners and the shared-loss payment: harmless. It is the governing agreement for shared-loss payments between the Fund and the twelve partners and must use those words; the sentence naming the question is not the decisive step.
- Shared vocabulary of schedule_b.pdf, corvane_claims_file_layout_v4.pdf, keswold_extract_dictionary_2027-02-01.txt, laurelford_data_notes_2027-02.docx with the design notes: none names the decisive step. The nearest is B.3.1's one sentence about estimating unpaid claims, which states that the Fund estimates but not how or what it changes; I would keep it, since the contract needs it to be a coherent reconciliation, and the decisive method (completion) stays unfiled. The other three describe layouts, codes, ids and the roster, which are cleaning topics.
- Three files naming every partner beside numbers (schedule_b.pdf, partner_clinician_roster_2027-01-01.xlsx, partner_quality_scorecard_2026.xlsx): harmless. None ranks partners on cost against target or on the owes question. Targets are inputs; roster tenure and quality scores are unrelated to who owes.

Reader pass 2, 2026-10-13, after the release note's backlog sentence, the roster's scope sentence and B.4.1's pins (same isolation; question 8 added on Ask B's reading).

### Pass 2

### 1. Sentence or file giving the decisive step
No file names the decisive step as a method. The nearest pointer is Schedule B B.3.1: "The Fund estimates the claims incurred in the Performance Year and not yet paid from its claims data." It says an estimate is made, but not how, and the prompt's "now that claims paid through January are in" points the same way. The claims extract itself shows the shortfall: paid 2026 service months fall from about 4.5M (June) to 2.6M (December). Nothing says "complete the claims" or "use completion factors".

### 2. Files that rank or score partners
None on the shared-loss question. partner_quality_scorecard_2026.xlsx scores the partners (quality points) but is relevant only to the shared-savings side (B.2.2, 70 points), not to who owes. It is a plausible distractor. Exhibit 1 gives targets but no performance.

### 3. Helper files the organisation would not really have produced
None. The Keswold dictionary, Corvane layout, Laurelford data notes, stop-loss summary, clinician roster and scorecard each read as something the named organisation would hold. The data notes docx is short and slightly tutorial ("The roster is not rerun when eligibility changes later"; "The partners' clinician roster is the network file the partners update by notice"). Those lines are plausible for a fund office note, but they come close to flagging the two traps (attribution against eligibility, and the roster being stale).

### 4. Figure or name that reads as the answer
None. There are no partner-level totals, no PMPMs and no owes flags anywhere. Targets in Exhibit 1 are inputs. The $200,000 truncation (B.1.5) and the stop-loss $175,000 deductible are distinct, and the stop-loss is a distractor for the TCOC cap.

### 5. Filed sentences that fix the computation
- B.1.3: "Attributed Member Month means a month in which a Member is eligible ... and appears on the Fund's attribution roster for the Partner for that month." Consequence: a member-month counts only if it is in both eligibility_spans and that month's roster row. The roster is not filtered for later eligibility changes (data notes), so the intersection is required. Final span versions apply.
- B.1.4: TCOC is the Fund's paid amount for professional and facility services with first date of service in 2026, for members attributed to the partner in the month of that first date of service, "whenever the claims are paid"; pharmacy is excluded. Consequence: incurred basis by service_from_date, with the attribution month taken from the service date, so claims paid after January count. This is the literal reason the January-paid data is incomplete.
- B.1.5: the amount above $200,000 per member is excluded, shared in proportion for multi-partner members. Consequence: member-level cap before the partner sum.
- B.1.6: PMPM is TCOC after the cap divided by Attributed Member Months.
- B.2.1: owes only if PMPM exceeds target by more than 2.0 percent. Payment is 40 percent of the excess times member months, capped at 4 percent of target times member months. B.2.3: unrounded comparison. Consequence: threshold test on unrounded PMPM.
- B.3.1: claims paid through the last business day of January, and "The Fund estimates the claims incurred in the Performance Year and not yet paid from its claims data." Consequence: the claims not yet paid must be estimated and added. The method is open.
- Keswold dictionary: "The claim's value is the paid_amount of its latest version." Voids carry zero. Consequence: take the latest version per claim_number, and the frequency codes are mixed (O/A/V vs 1/7/8, even numeric versus text).
- B.4.1(a): pharmacy is the Fund's net payments to the PBM, "reversals included whenever processed", for prescriptions filled in the Attributed Member Months with the partner. Consequence: use net B1/B2/B3 by adjudication, filtered by fill date in the member-months. Corvane ids are cardholder plus person_code, which must be mapped to member ids (the suffix mapping is by enrollment order, not person_code or relationship code).
- B.4.1(b): the share of the paid amount for professional services in TCOC "before B.1.5 and as paid through the reconciliation date" for services "rendered by clinicians who were not with the Partner group when the service was given". Consequence: paid as of January, no completion and no cap, professional claims only, determined by service date. The test is the rendering clinician against the partner at the service date.

### 6. What decides the main answer
It is an analytical choice: the 2026 TCOC from claims paid through January is incomplete for the late months, as the monthly paid totals in the extract show. The decisive step is judging the incurred but not yet paid claims with a completion estimate drawn from the claims' own lag pattern (paid_date minus service_from_date, with claim versions), and then testing each partner's PMPM against target with that uncertainty. The agreement states the estimate happens but not how, and the data separates the methods. The easy route (paid-through-January TCOC over member months) is natural and lands wrong for the partners near the 2 percent line. Nothing announces this beyond B.3.1 and the prompt's "claims paid through January". Several data steps sit beside it as Layer 1 work: latest-version resolution, mixed frequency codes, eligibility crossed with attribution, ID mapping and the cap. None of them is a planted decoy. Rule application is heavy (B.1 to B.2), but the call turns on the completion estimate. I could not verify whether the rule steps alone settle the partners; I did not build the full model, so I can't say whether the margin is narrow enough that the completion matters.

### 7. Realism
None clearly. The documents are well-formed, with signed-off lines, versioned release notes and job ids. Minor tells: the clinician roster is a clean 182-row file with exactly 12 partners; the Corvane NDCs look synthetic (unique per claim: 72,415 distinct NDCs over 75,896 claims, which is not what a real pharmacy file would show); and the dates shown in the file names (2027-02, 2027-01-01) are after "today" while the prompt speaks of January data. The mixed int/text frequency codes in the extract read as an authentic mess.

### 8. Professional-services ask: deciding whether a clinician was with the partner
Files and fields that decide it:
- medical_claims_extract: claim_form CMS1500, rendering_npi, billing_npi, service_from_date, latest version's paid_amount.
- Exhibit 1 (Schedule B): the partner group NPIs. A professional claim billed under the partner's group billing_npi means the clinician was with the group at that date.
- partner_clinician_roster_2027-01-01.xlsx: NPI, partner code, "With partner since". The roster is a 1 January 2027 snapshot: "A clinician who leaves a group is removed when the partner gives notice."
Findings from the data:
- Twelve rendering NPIs (one per partner) are absent from the roster but billed under the partner's group NPI from 2025-01 until mid-2026 (about 1,700 claims). They are clinicians who left. A roster-only reading, "on roster = with partner", would call them outside the group for the whole period, wrongly. The group-NPI billing shows they were with the partner then.
- Four roster clinicians joined in 2026 (since dates 2026-03 to 2026-06). Before the since date, all 361 of their claims were billed under their own NPI (none under a group NPI), and from the since date all of their claims are billed under the group NPI. So billing_npi and "With partner since" agree for joiners.
- No group-billed claim precedes a since date, and the group-billed rendering clinician never maps to a different partner than the billing group.
The reading the files support: with the partner on the service date means billing_npi equals the partner's group NPI (the rendering clinician's own-NPI claims after joining do not occur), cross-checked by the roster's since date for joiners. A reading that uses the 1 January 2027 roster alone gives a different answer (it misclassifies the leavers); a reading that uses the roster's partner code for current members matches the group-NPI reading for those members. One residual doubt: a clinician who is on the roster and bills under their own NPI would be "not with the partner", and the files show no such post-join case, so the two readings give the same classification for the roster clinicians.
