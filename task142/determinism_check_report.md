# Determinism check, task142 (stage 4)

The isolated judge's verdict, verbatim, then the disposition. The judge saw a fresh unzip of `target.zip`, the prompt
and the submission's graded blocks; it ran at medium effort.

---

# Verdict, task142 (Bellbird overflow block, Jan-Mar 2027)

**Verdict:** NOT_DETERMINISTIC (one supplementary cell only; the main recommendation and 14 of 15 payment cells, all referral shares and all weekly counts are forced and reproduce).

**Disposition:** FIX_NOW. Pin the duplicate-survivor rule in data_dictionary.xlsx (or move the one record's start time off the 18:00 line). The main call, the stump and every other graded figure stay byte-identical, so no model rerun is needed for the main call. If the author edits the visit record instead of pinning, treat it as SEND_BACK-lite (the record is solver-visible).

**Why:** Bellbird's visit file holds 29 near-duplicate pairs (same patient_ref, nurse and visit type, starts 2 to 13 minutes apart, overlapping times, one record posted late). No filed text says which record of a pair is the visit. For 28 pairs the choice does not change any figure. For Kingsdale's CLN visit for C4478/322795 on 16 Sept (BV6111873 start 18:08 Melbourne, BV6112106 start 17:58 Melbourne) it decides whether the 25 per cent evening loading applies. Keep first posted, latest start or first recorded_at gives Kingsdale September **$8,787** (the golden). Keep earliest start, last posted or last recorded_at gives **$8,755**. Both are reasonable, so Gate C fails on supplementary answer 2 (Kingsdale, September), taxonomy label `competing_defensible_answer`. Schedule 3.7 says Bellbird's records are the basis of the invoice and gives no tie rule.

## Evidence (recomputed from the bundle)

Literal reading first. The prompt and Schedule 2 (clauses 2.3 to 2.7) fix the estimand: nurse visits received by admitted patients on 1 Jan to 31 Mar 2027, patients admitted earlier included for their days in the quarter, expected value equal to the plan's Jan to Mar visits, lots of 25 over in-house capacity, booked in the 2.2 order until 850 is used. The method is left open.

| Item | Golden | My value | Source and note |
|---|---|---|---|
| Stays by stream | n/a | reproduced | episodes csv, 7,703 rows; completed, admitted to 30 Jun 2026 (the 47 open episodes were all admitted Aug to Sep 2026, so no censoring bias); AB/WC/AC/HF mapped through the crosswalk (AB by the 3-character diagnosis); census nurse_visits equals the stated schedule exactly (wound care every second day, heart failure 2,2,1...) |
| Daily admissions | Poisson | var/mean 0.95 to 0.99 by member | episodes csv |
| Model mean vs plan Jan-Mar visits | 2,143 / 1,905 / 1,570 / 1,209 / 1,064 | 2,142.9 / 1,905.5 / 1,568.7 / 1,209.7 / 1,064.8 | operating plans xlsx; exact compound Poisson (daily arrival rate = plan admissions / days in month, Oct to Mar, BJI at Northgate and Westmere from Alliance H04 stays) |
| P90 requirement | 2,400 / 2,150 / 1,800 / 1,400 / 1,250 | 2,397 / 2,148 / 1,798 / 1,403 / 1,247 | reproduces. Normal approximation gives 2,394 / 2,145 / 1,794 / 1,401 / 1,245, same rounded values |
| In-house visits | 2,112 / 1,911 / 1,589 / 1,246 / 1,086 | same | capacity xlsx (net shifts times visits per shift checked) |
| Lots | 12 / 10 / 9 / 3 (of 7) / 0 | 12 / 10 / 9 / 7 needed (3 left) / 0 | booking 300 / 250 / 225 / 75 / none reproduces |
| Plan-plus-Poisson-on-visits | 250 total | P90 2,202 / 1,961 / 1,621 / 1,254 / 1,106, a 250-visit booking | the easy wrong route, as stated |
| Historical weekly or monthly spread | wrong | weekly-spread P90 puts Northgate at 5 lots, monthly at 6 | confirms the data separates the candidates |

Robustness of the booking: I varied the stay source (per member, post-July-2025 only, all completed to Sept 2026, mode 1 only). Rounded requirements stay in the same 50-visit bins and the booking stays 300 / 250 / 225 / 75 / 0 in every variant when centred on the plan as clause 2.5 requires. The one thin spot is Westmere's 9 lots, which needs a P90 above 1,789 (mine 1,794 to 1,799). Without centring on the plan (a per-member-stay run using the model's own mean) Northgate falls to 11 lots and Kingsdale would take 100. Clause 2.5 files the centring, so this is closed.

Supplementary tables:
- **Payments** (Melbourne = UTC+10 for all of Jul to Sep; Sat 40, Sun 60, 25 Sep public holiday 100, weekday before 7 or from 18:00 25 per cent; attempted $68.40 flat; cancelled nil; C3920 mapped to Westmere; C4466 visits mapped to the member through the intake log). Mine: Northgate 3,819 / 14,501 / 8,112; Riverbend 5,856 / 4,174 / 13,349; Westmere 4,474 / 6,436 / 6,143; Kingsdale 7,059 / 5,351 / 8,755 or 8,787; Hillcrest 2,652 / 6,641 / 7,163. All match the golden except the Kingsdale September fork above.
- **Payable visits per member** (completed or attempted, after dedup): 161 / 140 / 106 / 130 / 103, matching the golden. The survivor choice does not move any visit across a pay-week boundary. The PNG itself is not in the bundle, so the chart was not inspected.
- **Referrals.** Counts need the 9 telephone referrals from the intake log during the portal outage (10 to 13 Aug) added to the 212 portal rows: 56 / 43 / 40 / 45 / 37 reproduces. Accepted within two hours over all referrals (Melbourne time, portal response is UTC): 75.0 / 81.4 / 82.5 / 73.3 / 75.7 reproduces. First visit within 24 hours of acceptance (completed or attempted, first attendance after acceptance; phoned patients linked through the IL26 log number): 94.1 / 82.1 / 94.4 / 84.6 / 90.6 reproduces. Nearest boundary cases are 23.70 to 23.83 hours, so a wrong time-zone handling would flip them, but the zone is filed in the data dictionary and Schedule 4.
- **Reading forks I checked and closed:** "accepted within two hours" literally means accepted (not accepted or declined), and the golden follows it; the "responded within two hours" reading (82.1 / 88.4 / 92.5 / 84.4 / 86.5) is the SLA wording of clause 4.2 but is not what the prompt asks. Portal-only counting (212 referrals) is ruled out by clause 4.1 (a referral is any request) and the register entries "Portal down, referral by phone". No exact 2.0 hour or 24.0 hour ties exist.

## Files/Hygiene

**PASS.** 20 files, five formats (csv x7, xlsx x5, pdf x4, jsonl, docx); one file over 25,000 rows (census, 32,517). Distractors present (patient experience survey, 2025-26 declined referrals, 2025-26 service report with platform-reported shares). Office and PDF metadata read as real authors and companies; no README, no authoring or benchmark language, no tool banners. Dates are coherent (agreement 2 Oct, plans 14 Oct, capacity v1.1 19 Oct, register extract 30 Oct, dictionary 2 Nov). One mild oddity: the visit extract ends at 30 Sep 12:29 Melbourne (only 4 visits on 30 Sep), which looks like a cut, not a defect that moves any figure. Cross-batch fingerprinting against other tasks was not done (other task folders are out of bounds).

## Stump power

Moderate to strong. The tempting route is plan visits plus a Poisson or historical-spread margin, which books 250 of 850 (Northgate 100, Riverbend 50, Westmere 50, Kingsdale 25, Hillcrest 25) and misses that BJI and wound-care stays carry visits across the quarter. A strong model that builds the admission-by-stay model and centres it on the plan gets the call. The asks add many separately gradable cells (duplicates, UTC conversion, the C4466 account, Altona Park account, phoned referrals, app status vocabulary change) so the top two responses should lose much of the ask weight. No contrasting model runs were supplied, so the empirical GPT bar is not assessed.

## Stumping type

`mechanism: method_or_model_selection` (forecasting of a stay-driven requirement), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Plans, census and stays are all correct; the difficulty is modelling the requirement as arrivals times stay structure and validating that visits are not independent. On clean data it would still stump. Gate G passes.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`. Swap test: "megawatt-hours" or "school places" would not carry a stay-length convolution against a roster, so the domain is used (demand and surge capacity for hospital-in-the-home). Layer 1: program codes to streams crosswalk, campus reissue, UTC against Melbourne time, app status vocabulary change at v5.0, portal outage with phoned referrals, late-posted duplicates. Layer 2: P90 of a compound arrival-and-stay quarter total, centred on the plan, against in-house capacity and the booking order. Easy route a strong analyst takes after correct cleaning and rule reading: plan plus a Poisson margin on visits (or historical spread), giving the 250-visit booking instead of 775 plus 75.

## Fix

**data_dictionary.xlsx (input_files, no effect on the main call):** add under bellbird_visits a line such as "Where the app posts one visit twice (same patient, nurse and visit type, overlapping times), the record with the lower visit_no is the visit." That gives $8,787 as in the golden. Alternatively shift one of the two Kingsdale records (BV6111873 or BV6112106) so both start on the same side of 18:00. Keep the golden as is. Regenerate the solution blocks only if the golden rule is changed.

---

## Disposition

**NOT_DETERMINISTIC on one cell, FIX_NOW, applied in one generator pass; the single re-judge is next.** The main call,
the stump, the ladder and every graded figure are unchanged: `freeze.py check task142 --mode determinism` exits 0
(Kingsdale September stays $8,787; `generator/figures.json` is byte-identical, and the 98 figures of blocks 1 to 4 all in it). The call sentence of the prompt is
unchanged; its chart sentence changed (below). Each finding:

| Finding | Ruling | Where it is closed | Asserted |
|---|---|---|---|
| Which record of a re-posted pair is the visit (Kingsdale CLN, C4478/322795, 16 September: BV6111873 at 6.08 pm, BV6112106 at 5.58 pm; $8,787 or $8,755) | fixed, in the data | The generator draws a re-keyed record on the first record's side of every line its figures turn on: the Melbourne day (weekend, public holiday, month, pay week, quarter), 7.00 am and 6.00 pm, the referral's acceptance and 24 hours after it. Only the one crossing draw is redrawn (from the record's own stream), so BV6112106 now starts at 6.12 pm and ends at 6.39 pm; the other 29 pairs, every visit number and every other record are unchanged. No survivor rule is filed: a filed rule would adjudicate Ask A's device and name it. | `checks.py`: all 30 pairs on one side of every line, on one Melbourne day at one fee; keeping the first or last posted, the lowest or highest visit number, or the earliest or latest start removes the 30 re-posts and gives all 15 amounts to the cent, every Member's count in all 14 pay weeks and every referral count and share. `verify.py`: the same under four rules on its own code path |
| Leak reader: the referral share's basis (accepted within two hours over referrals made, against clause 4.2's responded within two hours) | fixed, by the WHAT | Schedule 4 clause 4.5 now reads: the Alliance reviews, for each Member, "the share of the referrals the Member made in the quarter that Bellbird accepted within two hours of the Member making them, and the share of the Member's accepted referrals that Bellbird first visited within 24 hours of accepting them", the prompt's own words | the responded reading (82.1, 88.4, 92.5, 84.4, 86.5) and acceptances over accepted referrals (82.4, 89.7, 91.7, 84.6, 87.5) each miss every Member's golden share (75.0, 81.4, 82.5, 73.3, 75.7) |
| Leak reader: the chart's weeks (the finance calendar's Monday to Sunday weeks; weeks straddling 1 July or 30 September) | fixed, by the WHAT, and shown not to arise | The prompt asks "by pay week"; the dictionary's calendar rows say pay weeks run Monday to Sunday and the new week_commencing row that the year's first pay week commences Monday 29 June 2026. The export holds visits on 1 July to 30 September only (Melbourne dates), so the part weeks commencing 29 June and 28 September carry only the quarter's days however a straddling week is read | every export record on a quarter day; the 14 pay weeks hold every payable visit; the graded totals (161, 140, 106, 130, 103) are the quarter's payable visits under any weeks |
| Leak reader: payable visits as a count | fixed, by the WHAT | The prompt asks for "the number of" payable visits; clauses 3.4 and 3.5 make completed and attempted visits payable and cancelled visits not | completed visits alone miss every Member's total |
| Leak reader, realism: the manifest without sizes for some files; the H04 plan rows' October ramp then flat level | manifest fixed; plan rows kept | `export_manifest.csv` gives rows, sheets or pages for every file. The H04 rows are left: their October to March months feed the call's expected visits and percentile, so no change there is figure-neutral | every manifest size recounted from the file |

**Changed under `target/`:** `bellbird_agreement_schedules3-4_fees_and_service_levels.pdf` (clause 4.5, still one
page), `bellbird_visits_2026-07-01_to_2026-09-30.jsonl` (BV6112106's start and end only),
`data_dictionary.xlsx` (the week_commencing row) and `export_manifest.csv` (rows_or_pages). Every other file is
byte-identical to the judged pack. `prompt.txt` changed in the chart sentence only ("the number of Bellbird's payable
visits by pay week and member"; 838 characters, `voice-check.py` PASS).

**Cost to the asks.** None to the devices: the cracker profiles are unchanged (no device 2, intake files alone 0,
re-posts alone 10, telephoned referrals alone 12, telephoned referrals and intake files 15, re-posts with either other
20, all three 35), the pair ceiling stays 39.5. Clause 4.5 removes a reading the design never counted on; the
telephoned referrals, the intake files and the UTC response times still carry Ask B.

**Gates on the final rebuild:** `build.py` green (490 assertions), `verify.py` agrees, two builds byte-identical,
`target.zip` cut; `freeze.py --mode determinism` PASS; `figures_check.py` PASS (98 figures); `precut.py` 49 checks, 0
FAIL; `leak.py --asof 2026-11-03` REVIEW, no LEAK; `guard.py surface` 0 promoted, `heart` WARN (`repeat.gate_g`, as
drawn), `validate` clean; the container audit clean on `target/` and `golden/`.
