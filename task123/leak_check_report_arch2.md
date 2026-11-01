# leak check, task123

**Verdict: REVIEW.** 22 files read, 40 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: standard, inside, account, calendar, northbank, interval, golden, decisive, sentence, method, meters, harbor, prompt, monthly, billed, months, indicator, activity, period, closed, day-proration, nothing, extracts, service, asserted

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `County_Energy_Data_Standard_Ed3_2025.pdf`: golden figure 2.4 appears: ...s on which meters were read or bills were issued. 2.4 Service period. The gas days a bill covers: from...
- **REVIEW** `County_Energy_Data_Standard_Ed3_2025.pdf`: carries 16 of 17 distinctive words of the committed call: 'Split the $18,640,000 Northern Heat Assistance Grant for 2026-27 as Brennock $2,380,000, Rennick $2,145,000, Pellow $1,9'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `County_Energy_Data_Standard_Ed3_2025.pdf`: 11 of 25 stump-paragraph terms appear (standard, account, calendar, northbank, meters, harbor); read whether the document names the move
- **REVIEW** `RHEF_data_notes_utility_extracts_2026-04.docx`: 15 of 25 stump-paragraph terms appear (account, calendar, northbank, interval, meters, harbor); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `NNG_READ_SCHEDULE_2026-27.csv`: 240 ISO dates after 2026-04-20, e.g. 2026-09-01, 2026-09-02, 2026-09-03, 2026-09-04, 2026-09-07

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Three isolated reads at medium effort, each on a fresh copy of prompt.txt and target/. After the third read, five counties' displayed names changed (Carrow to Sauvain, Dellmoor to Rennick, Evanshade to Ottercreek, Glenhollow to Wynnell, Lorrance to Pellow) and the thread lost its line naming the two extra files; no figure moved. The reads below quote the names as they then stood.

### First read (cut pack, before the stage-4 fixes)

#### 1.
No file or sentence names the decisive step. The nearest is the PDF standard, 2.3: "Calendar month. The gas days dated in the month. A month's use is the gas used on those gas days, whatever the dates on which meters were read or bills were issued." With 2.4: "Service period. The gas days a bill covers: from the gas day after the prior meter read through the gas day of the read." It states the definition, not a method. It does not say to prorate cycle bills, use the MDMS dailies, drop cancel/rebill pairs, handle register rollover, or add the Kestrel Valley share in Tillery. The docx notes (Northbank "service period runs from the gas day after PREV-READ-DT through CURR-READ-DT"; Pine Harbor "billed on calendar months from their daily reads") describe layouts and are not an instruction.

#### 2.
none. No shipped file ranks the counties or gives a county total. The manifest, the eml and the docx carry no county figures. service_points_northern_region only maps premises to counties. KVG_WCP_ENROLLMENTS has SERVICE_COUNTY per enrollment, which is raw rows, not a ranking.

#### 3.
none strictly. The docx "data notes" (compiled by RHEF research, 17 April) and export_manifest_2026-04-20.csv are helper-like, but a research team does keep field notes and a manifest, so they are plausible. The eml is a plausible planning thread.

#### 4.
The only figure in the folder that reads as an answer is the $18,640,000 total in the eml and the prompt, and that is given context. No county award, therm total or indicator count appears anywhere. The PDF Appendix C lists the twelve counties and their utilities, which is context.

#### 5.
Main figure. PDF 1.1: "Where a program's rules allocate funds in proportion to a county's residential natural gas use, the use is the series defined here." 2.3 "A month's use is the gas used on those gas days [dated in the month], whatever the dates on which meters were read or bills were issued." 3.1: "the residential series is the therms of residential use in the month at premises in the county, summed over every utility serving the county." 2.1 residential = Appendix A residential schedules (RS-1, R1, RES); GS/G1/G2/IS/SGS/LGS excluded, including master-metered multi-family. 2.6: county of the premise per the service-point records, not the mailing address. 2.5: therms as billed; CCF times the heating value applied on the bill. 2.4: service period runs from the day after the prior read through the read day. 3.3: allocation from unrounded values; rounding as the program directs; not adjusted to the total. eml: "split across the twelve counties in proportion to each county's residential natural gas use in January 2026."
Literal result: for each county, sum over the three utilities' residential premises located in the county (via service_points COUNTY), of the therms used on gas days 1 to 31 January 2026, as billed (Northbank CCF x bill HV, which is the read month's factor; Pine Harbor 1.034 per CCF for MDMS dailies). Bills spanning January are therefore apportioned to the gas days in January, not taken whole by bill date or read date. Cancelled and rebilled transactions count once, as the rebill. Kestrel Valley Tillery premises add to Pine Harbor's. Award = 18,640,000 x county / sum of all twelve, with the prompt's rounding (therms to nearest 10,000, awards to nearest $5,000). The standard does not say how to spread a bill across its days (equal per day is the natural literal reading), or how to treat estimated reads, or the 23/25-hour gas days.
Disconnections for nonpayment completed in January. Appendix B: "Residential services disconnected for nonpayment of a utility bill, completed in the month." 4.2: counted at the county of the premise, not rounded. The notes give the codes: KVG ORDER_TYPE OFF with REASON_CD NP and STATUS COMP ("CERR completed in error, reversed", "UNAB unable to complete", "CANC cancelled" are not completed); NNG ACT_CD DNP with RESULT_CD C ("COMPLETED_AT: date and time the crew closed the activity"); PHE work orders and HES valve events (VALVE_CLOSE with REASON_CD NP). Literal count: orders whose completion falls in 1 to 31 January 2026 (completion time, not keyed or scheduled date), residential only, nonpayment only, by premise county. The Northline xlsx is the contractor's record of KVG collections jobs 5 to 16 Jan, a second source for the same disconnections; the docs do not say whether to add it or dedupe it.
Accounts on a low-income plan on 31 January 2026. Appendix B: "Residential accounts enrolled in the utility's low-income payment plan (Appendix A) on the last day of the month. An enrollment counts from its effective date through its end date." Appendix A: KVG Winter Care Plan, NNG HHAP, PHE IBPP. Notes: WCP "EFFECTIVE_DT is the first day the plan applies; END_DT is blank while it continues"; "SERVICE_COUNTY is the county entered on the application" (2.6 says use the premise county instead); HHAP file is the premises at close of business 31 Jan, PROGRAM_STATUS A active; PHE PLAN_TYPE IBPP only (BUDGET and DPA are not income-based), STATUS ACTIVE or ENDED. Literal count: accounts with effective <= 31 Jan 2026 <= end (or blank), residential, counted at the premise's county; the count of accounts (not premises or enrollments).

#### 6.
- docx: "SERVICE_COUNTY is the county entered on the application." (signals it may differ from the premise county)
- docx: "Kestrel Valley also serves residential premises in the north-east of Tillery County."
- docx: "Service orders were pulled on 3 February 2026 for the January indicators: every order with an activity date from 1 December 2025 to the pull." (late January orders may be incomplete or keyed across month)
- docx: "Northline Utility Services worked Kestrel Valley's collections orders from 5 to 16 January 2026 under its field contract."
- docx: "A four-digit or five-digit register rolls over to zero, so CURR-RDG can be below PREV-RDG; CCF is the gas registered."
- docx: "Pine Harbor exchanged the meters ... between 6 and 24 October 2025. From the day after the exchange those premises are billed on calendar months from their daily reads; the other premises are still read on 20 monthly cycles."
- docx: "the gas day of 2 November 2025 ran 25 hours and that of 8 March 2026 ran 23."
- docx column notes: "A cancel and its rebill carry the number of the bill they correct."; "TXN_TYPE BILL original; CNCL cancels the original in full; RBIL the corrected bill."; "READ_TYPE E estimated read, trued up at the next actual read."; "STATUS ... CERR completed in error, reversed"; "READ-CD A actual, F final read at a move-out"; "vee_status E estimated by the MDMS"; "times in UTC" (head-end events).
- docx: "Account history: every R1 account at each premise with its start and end dates."
- PDF 2.6: "A mailing address does not determine the county." PDF 2.1: "including master-metered multi-family buildings."
- PDF 1.2: "Utility billing conventions differ; the definitions below govern the series whatever the utility's own conventions."
These are mostly layout/code descriptions that a real data dictionary would carry, but together they point at each special-handling population. The standard 1.2 and 2.3 sentences come closest to narrating the move (calendar-month use regardless of read/bill dates).

#### Review lines
- PDF figure 2.4: harmless. It is the clause number "2.4 Service period", not a figure.
- PDF 16 of 17 distinctive words of the committed call: harmless in this copy. I found no "Split the", "2,380,000" or any county award in the PDF text (grep 0 hits); the words are scope vocabulary (grant, residential, natural gas, county, proportion) and the twelve county names in Appendix C.
- PDF 4 of 25 stump terms (account, calendar, standard, income): partially leaks. It does not name a move, but 2.3 defines the calendar-month use "whatever the dates on which meters were read or bills were issued", which is the governing definition of the decisive quantity. That is a stated rule in a real standard, so acceptable, though it tells the solver not to take cycle bills at face value.
- docx 6 of 25 terms (register, months, account, calendar, income, interval): harmless. The terms occur in layout descriptions (register rollover, "billed on calendar months from their daily reads"); it describes formats and does not say to prorate, dedupe or compute anything.
- prompt sentence with two or more stump terms: harmless. It lists the three requested outputs and the file name, naming the quantities asked for, not how to compute them.
- NNG_READ_SCHEDULE_2026-27.csv dates after 2026-04-20: harmless. A forward reading schedule for 2026-27 (240 rows, one per route/month) is plausible for a utility to send. It is an unused distractor, not a leak; the only oddity is that a future schedule sits in a January 2026 folder.

#### Realism
- service_points_northern_region_2026-04-15.csv has a clean PREMISE_TYPE/COUNTY schema covering all three utilities ("all three utilities" provided it, one merged file), which a real regulator-free folder would not usually have.
- The manifest lists exact row counts for each file, and the docx data notes are very tidy, with every field defined; both read as authored.
- Premise/account IDs are uniformly patterned (KV0100009, P0600009, PH-1000009) and the three utilities use inconsistent date formats on purpose (MM/DD/YYYY, ISO, CCYYMMDD); the mess looks designed in a regular way.
- NNG_READ_SCHEDULE sorts routes and read dates in neat sequence (route n read on the nth of the month), with a reader per block of routes.
- Eml: tone is on the nose in stating the exact grant rule and all files received; the forwarded thread has no signature, disclaimer or attachment line.
- NNG_FIELD_ACTIVITY (442 rows) and NNG_CREW_COMPLETIONS (442 rows) have identical counts and a clean 1:1 key.
- The Northline xlsx has only one tidy sheet, with the invoice number in the header and no stray formatting.

### Second read (after the HHAP fix)

#### 1.
No file or sentence names a method for a county's January use. The nearest is the standard's 2.3: "Calendar month. The gas days dated in the month. A month's use is the gas used on those gas days, whatever the dates on which meters were read or bills were issued." (County_Energy_Data_Standard_Ed3_2025.pdf), with 2.4 "Service period. The gas days a bill covers: from the gas day after the prior meter read through the gas day of the read." The docx says Pine Harbor's AMI premises are "billed on calendar months from their daily reads; the other premises are still read on 20 monthly cycles", and that Northbank reads "every second month, route by route". The cycle, read-to-read and bimonthly structure is visible, and 2.3 tells the solver to use gas days rather than bill dates. That is the closest thing to a decisive-step statement. It reads as a general definition, not as an instruction about this task.

#### 2.
None. No file ranks or scores the counties. The eml gives only the $18,640,000 total and "in proportion to each county's residential natural gas use in January 2026". The service points file lists counties but carries no use. KVG_WCP_ENROLLMENTS carries a SERVICE_COUNTY column but no count.

#### 3.
- export_manifest_2026-04-20.csv: it is a plausible real index, but it lists each file's "covers" and row counts, so it works as a guide.
- RHEF_data_notes_utility_extracts_2026-04.docx: a real research team could plausibly write it, but it works as a field guide. It explains column codes and the HV-FACTOR picture, and the service point note says the file was combined by the research team.
- County_Energy_Data_Standard_Ed3_2025.pdf: a plausible real standard (the governing document).
- Nothing else is obviously there only to help. The eml is a plausible thread, and its second message lists which files are in the folder.

#### 4.
- The eml's "$18,640,000" and "twelve counties" are context from the prompt, not answers.
- Appendix C county list N01 to N12 (Ashwell ... Tillery, with Tillery served by "Pine Harbor Energy, Kestrel Valley Gas") reads as context. It flags that Tillery has two utilities.
- No figure reads as the answer. I saw no award, no ranking and no January county total.

#### 5.
Main figure. Sentences that fix it:
- Standard 1.1: "Where a program's rules allocate funds in proportion to a county's residential natural gas use, the use is the series defined here."
- 2.1: "Accounts billed on the residential rate schedules listed in Appendix A. Accounts on general service schedules are not residential, including master-metered multi-family buildings."
- 2.3: "A month's use is the gas used on those gas days, whatever the dates on which meters were read or bills were issued."
- 2.4: service period from the gas day after the prior read through the gas day of the read.
- 2.5: "Therms as billed by the utility. Where a utility meters in CCF, therms are the billed CCF times the heating value the utility applied to the bill."
- 2.6: "County ... as recorded in the utility's service-point records."
- 3.1: "summed over every utility serving the county."
- 3.3: allocations are "computed from unrounded county values" and "not adjusted to the program total."
- The docx adds how each utility's data is built: KVG bills have cancel and rebill transactions (BILL, CNCL, RBIL, with "THERMS ... negative on a cancel"); Northbank THERMS are "CCF times HV-FACTOR, the heating value of the month of the read" and the register rolls over; Pine Harbor uses "1.034 therms per CCF" and has local-time gas days.

Literal result for a county's January 2026 residential use: take only RS-1, R1 and RES premises. Assign each premise to its county by the service-point file, not by city or by the enrollment's county. For each premise and utility, count the therms used on gas days from 1 to 31 January 2026. Bills that cross month ends are split across the gas days of their service period. KVG cancels and rebills net to the corrected bill. NNG reads are spread over gas days from the day after the prior read through the current read date, using the therms billed. PHE AMI premises use daily CCF times 1.034 for the January gas days, and PHE cycle premises are split by service period. Add up across KVG, NNG and PHE (Tillery gets both KVG and PHE). The result is an unrounded county value. The award is $18,640,000 times the county value over the twelve-county total, rounded to $5,000, and therms are reported to 10,000. Whether to split by days or by a daily profile is not fixed except for "gas days". I read the days split as the literal execution.

Disconnections for nonpayment completed in January. Sentences:
- Appendix B: "Residential services disconnected for nonpayment of a utility bill, completed in the month."
- 4.2: "counted at the county of the premise (2.6) and are not rounded."
- docx KVG: "ORDER_TYPE OFF turn-off", "REASON_CD NP nonpayment", "STATUS COMP completed; UNAB unable to complete; CERR completed in error, reversed; CANC cancelled", "CREATED_TS, COMPLETED_TS: when the order was keyed; when the field work was completed".
- docx Northbank: "ACT_CD DNP disconnect for nonpayment", "RESULT_CD C completed; U unable; X cancelled", "COMPLETED_AT ... date and time the crew closed the activity".
- docx PHE: the work orders are residential, and the HES events carry "VALVE_CLOSE ... REASON_CD NP nonpayment" in UTC.
- The Northline job report is a contractor's list of the January KVG collections jobs ("Date", "Job Type DISCONNECT - NONPAY").

Literal count: each residential disconnection for nonpayment that actually completed with a completion date in January 2026, located by the premise's county, counted once per service. KVG: OFF, NP, status COMP (not UNAB, CERR or CANC) with COMPLETED_TS in January. NNG: DNP, result C, completed in January (completion file time, and ACT_DATE can differ). PHE: Collections Shutoff, status Completed, completedAt in January local time, matched with HES VALVE_CLOSE NP events (UTC converted to local) for AMI-V premises. Northline jobs are not a source by themselves.

Accounts on a low-income payment plan on 31 January 2026. Sentences:
- Appendix A: Winter Care Plan (WCP), HHAP, IBPP.
- Appendix B: "Residential accounts enrolled in the utility's low-income payment plan (Appendix A) on the last day of the month. An enrollment counts from its effective date through its end date."
- 4.2: counted at the premise's county.
- docx: WCP "EFFECTIVE_DT is the first day the plan applies; END_DT is blank while it continues", "SERVICE_COUNTY is the county as recorded on the enrollment"; HHAP file is the snapshot "at close of business on 31 January 2026" with "ACCOUNT_NO" and "PROGRAM_STATUS A is active"; PHE "PLAN_TYPE IBPP ... STATUS ACTIVE, ENDED" (BUDGET and DPA are other plans).

Literal count: KVG WCP enrollments with EFFECTIVE_DT on or before 31 January 2026 and END_DT blank or on or after 31 January 2026, counted by the account's premise county, not SERVICE_COUNTY. NNG: HHAP premises as of 31 January 2026 (status A) with the enrolled account, counted once per account. PHE: IBPP arrangements, START_DATE on or before 31 Jan 2026 and END_DATE blank or on or after it (including ENDED ones whose end is later), but not BUDGET or DPA, counted at the account's premise county via the meter and account history.

#### 6.
- Standard 2.1: "Accounts on general service schedules are not residential, including master-metered multi-family buildings." This is a signal for GS files.
- Standard 2.3 and 2.4 (calendar month versus read dates, as quoted above).
- Standard Appendix B: "An enrollment counts from its effective date through its end date."
- docx KVG: "Kestrel Valley also serves residential premises in the north-east of Tillery County."
- docx: "TXN_TYPE BILL original bill; CNCL cancels the original in full; RBIL the corrected bill." and "A cancel and its rebill carry the number of the bill they correct."
- docx: "READ_TYPE ... E estimated read, trued up at the next actual read."
- docx: "THERMS are CCF times HV-FACTOR, the heating value of the month of the read", and "A four-digit or five-digit register rolls over to zero, so CURR-RDG can be below PREV-RDG; CCF is the gas registered."
- docx: "group A in odd months and group B in even months."
- docx: "the gas day of 2 November 2025 ran 25 hours and that of 8 March 2026 ran 23."
- docx: "exchanged the meters ... between 6 and 24 October 2025. From the day after the exchange those premises are billed on calendar months from their daily reads."
- docx: "times in UTC" for the head-end events.
- docx: "SERVICE_COUNTY is the county as recorded on the enrollment" and "CITY and ZIP are the postal address."
- docx: "STATUS ... CERR completed in error, reversed", "COMPLETED_TS: when the field work was completed" and Northbank "COMPLETED_AT" in a separate crew completions file.
- docx: the exports "pulled on 3 February" and the "current to 15 April 2026" notes.
These are mostly column definitions, as a real data dictionary would carry, though the combination narrates almost every device.

#### Review lines
- Standard PDF, "2.4 Service period": harmless. It is the section number 2.4 matching a figure by chance, not a golden figure.
- Standard PDF, 16 of 17 distinctive words of the committed call: leak (mild) if it really is the call text. I cannot see the call here. The sentence quoted ("Split the $18,640,000 ... Brennock $2,380,000, Dellmoor $2,145,000, Lorrance $...") does not appear in the PDF I read, which has no dollar award figures. I found only the words "grant", "allocate", "proportion", "county", "residential". So harmless in this copy (generic vocabulary, no awards).
- Standard PDF, 5 of 25 stump terms (account, standard, calendar, northbank, income): harmless. "Calendar month" is a definition (2.3) and defines gas-day assignment. It does not name a move or warn about the shortcut, though it does state the rule that bill dates do not matter. This is the nearest to a hint, and a careful reader gets "use gas days" from it. It reads as the standard's normal content.
- RHEF docx, 8 of 25 stump terms: harmless to mildly leaking. It is a field guide with column meanings. It does narrate that PHE premises are "billed on calendar months" versus cycles and that Northbank reads bimonthly, but it states no method or what to do.
- Prompt, two or more stump terms in one sentence: harmless. The sentence just names the three requested columns and the file; it names no method.
- NNG_READ_SCHEDULE_2026-27.csv, 240 ISO dates after 2026-04-20: harmless as to the answer, because it is a future reading schedule (a declared distractor). It is dated after the setting, which is natural for a schedule, though the manifest says extracted 2026-04-15, so a schedule for 2026-27 is plausible.

#### Realism
- The data notes docx is a very complete data dictionary and covers nearly every trap. It is unusually helpful, and it reads as written for the task.
- The standard's Appendix C lists a county-by-utility table with the exact utilities, and Tillery's two utilities are noted.
- The standard sets out exact definitions for the same concepts the task turns on (2.3, 2.4), which reads a bit tailored.
- Three utilities each use different column names, formats and dates (MM/DD/YYYY, ISO, fixed width). That is plausible, but all three are uniformly tidy.
- Account and premise numbering patterns are very regular (sequential prefixes like P06xxxxxx, KV01xxxxx, PH-1xxxxxx), and the premise IDs step by 17 in the service-point file (KV0100009, 0100026, 0100043).
- The bill numbers and account numbers look synthetic (NNG 8-digit starting 406).
- Round times in the Northline report and uniform crews (NUS-2, NUS-4) look generated.
- Fixed-width header "HNNGCIS R1 BIMONTHLY READS..." is a believable mainframe style, but trailer and counts are perfectly consistent.
- Manifest row counts all agree with the file contents. A real manifest is rarely so clean.
- The eml has a plausible header, but the quoted reply describes every file in the folder, which reads as exposition.
- The date of the eml (20 April 2026) and the manifest ("extracted 2026-04-17" for the docx) align very tidily.
- The Northline xlsx has no extra sheets or formulas. It is a clean single-sheet export with a title block.

### Third read (after the realism fixes)

#### 1.
No filed sentence names the decisive step. The closest is the standard's definition, County_Energy_Data_Standard_Ed3_2025.pdf 2.3: "Calendar month. The gas days dated in the month. A month's use is the gas used on those gas days, whatever the dates on which meters were read or bills were issued." This states the estimand (gas days dated in January), which makes the apportioning of cycle-billed use to calendar days the implied method. It also says 2.4 "Service period. The gas days a bill covers: from the gas day after the prior meter read through the gas day of the read." The docx adds "The service period runs from the gas day after PREV-READ-DT through CURR-READ-DT" and "From the day after the exchange those premises are billed on calendar months from their daily reads; the other premises are still read on 20 monthly cycles." The prompt itself says nothing about method.

#### 2.
None. No file ranks or scores the counties on awards or January use. The inputs are raw transactions: bills, reads, orders, enrollments. The eml only restates the $18,640,000 and the proportional rule. The county names in Appendix C of the PDF are a list, not a ranking.

#### 3.
- export_manifest_2026-04-20.csv: a row-count and coverage index; it is plausible for a shared folder but is mostly a convenience. It also gives useful row counts for reconciliation.
- RHEF_data_notes_utility_extracts_2026-04.docx: the layout, status-code and field glossary for every extract. It is arguably natural as a research-team note, but it exists to help the analyst read the files.
- Otherwise none. The remaining files read as native utility exports. The distractors (KVG_GS_BILLING_EXTRACT, NNG_READ_SCHEDULE_2026-27.csv, and the Northline xlsx and PHE work orders and HES events, which duplicate other disconnection records) are plausible folder clutter.

#### 4.
None reads as the answer. The only prominent figure is "$18,640,000" (prompt and eml), which is context. The eml's "twelve counties" and "proportion to each county's residential natural gas use in January 2026" are the question restated, not the answer. The PDF Appendix C lists which utilities serve each county (Tillery is served by Pine Harbor and Kestrel Valley); it frames the sum across utilities and is context.

#### 5.
Main figure. Sentences: PDF 2.3 "A month's use is the gas used on those gas days, whatever the dates on which meters were read or bills were issued." PDF 3.1 "For each county and calendar month, the residential series is the therms of residential use in the month at premises in the county, summed over every utility serving the county." PDF 3.3 "Allocations made in proportion to the series are computed from unrounded county values." PDF 2.1 "Accounts billed on the residential rate schedules listed in Appendix A. Accounts on general service schedules are not residential." PDF 2.6 "The county in which the premise served is located, as recorded in the utility's service-point records." PDF 2.5 "Therms as billed by the utility."
Literal result: for each county, sum the therms used on the gas days dated 1 to 31 January 2026 (the billed therms of each bill spread over the gas days of its service period, then the January days counted), at premises located in the county per the service-point file, on residential rate schedules only (RS-1, R1, RES; exclude GS-1, GS-2, G1, G2, IS, SGS, LGS), across the three utilities, using the utility's billed therms and heating value. Sum unrounded, then award = $18,640,000 x county share, rounded to the nearest $5,000. The literal reader does not simply take bills with a read date in January. The text does not say how billed therms are spread over the service days (even per-day vs MDMS daily shape), how cancel/rebill pairs are handled, or how estimated reads are trued up. The docx lets a reader infer them (CNCL cancels the original in full, RBIL replaces it; E estimated, trued up at the next actual read; MDMS daily CCF x 1.034 for the converted Pine Harbor premises).
Indicator 1, disconnections for nonpayment completed in January: PDF Appendix B "Residential services disconnected for nonpayment of a utility bill, completed in the month", counted at the premise county (4.2), not rounded. Literal result: count residential services whose nonpayment disconnection was completed (finished by a crew, not merely scheduled or created) in 1 to 31 January 2026, per county. Open on the literal text: which file/status code counts as completed, and use of completion date vs status date. The docx defines STATUS COMP, "COMPLETED_TS", RESULT_CD C with COMPLETED_AT, and reason NP.
Indicator 2, accounts on a low-income payment plan on 31 January 2026: Appendix B "Residential accounts enrolled in the utility's low-income payment plan (Appendix A) on the last day of the month. An enrollment counts from its effective date through its end date." Literal result: count accounts, per county, whose plan (WCP, HHAP, IBPP) has an effective/start date on or before 31 January 2026 and a blank end date or an end date on or after 31 January 2026 (inclusive), at the premise county (4.2), not rounded. Only the IBPP plan type of Pine Harbor counts (not BUDGET or DPA, per Appendix A). The docx says SERVICE_COUNTY on WCP is "the county as recorded on the enrollment", which conflicts with 2.6/4.2 premise county; the standard governs.

#### 6.
- docx: "Pine Harbor exchanged the meters at part of its residential premises for AMI meters with service valves between 6 and 24 October 2025. From the day after the exchange those premises are billed on calendar months from their daily reads; the other premises are still read on 20 monthly cycles."
- docx: "the gas day of 2 November 2025 ran 25 hours and that of 8 March 2026 ran 23."
- docx: "Residential (RS-1) premises are read on 21 cycles a month, cycle 01 early in the month and cycle 21 at the end."
- docx: "R1 premises are read every second month, route by route: group A in odd months and group B in even months." and "THERMS are CCF times HV-FACTOR, the heating value of the month of the read".
- docx table: "A Cancel and its rebill carry the number of the bill they correct", "CNCL cancels the original in full", "E estimated read, trued up at the next actual read", "DIALS register digits (4 or 5); the register rolls over to zero", "READ-CD F final read at a move-out".
- docx: "Service orders were pulled on 3 February 2026 for the January indicators: every order with an activity date from 1 December 2025 to the pull." and "Northline ... worked Kestrel Valley's collections orders from 5 to 16 January 2026 ... Their job report ... came with their February invoice." Statuses "UNAB unable to complete (no access)", "CERR completed in error, reversed", "CANC cancelled"; "RESULT_CD C completed; U unable to complete; X cancelled before a crew was sent"; "Crew completion file: date and time the crew closed the activity."
- docx: "SERVICE_COUNTY is the county as recorded on the enrollment. EFFECTIVE_DT is the first day the plan applies; END_DT is blank while it continues." and "PROGRAM_STATUS A is active", "PLAN_TYPE IBPP ... BUDGET budget billing; DPA deferred payment arrangement".
- docx: "times in UTC" for head-end events; "Gas days run midnight to midnight Eastern time"; "Combined by the research team ... CITY and ZIP are the postal address."
- eml: "Kestrel Valley's order extract is the one they pulled on 3 February for the monthly table" and "I've left both in the folder" for the GS extract and read schedule (flags those as unused).
- PDF 2.3 "whatever the dates on which meters were read or bills were issued", PDF 1.2 "Utility billing conventions differ; the definitions below govern the series whatever the utility's own conventions."
These read as a mix of ordinary layout notes and a lightly narrated map of the devices (calendar vs cycle, cancel/rebill, estimates, county on enrollment vs premise, disconnect completion). The docx is the densest.

#### Review lines
- PDF "2.4" golden figure: harmless. It is the clause number "2.4 Service period", not a figure.
- PDF 16 of 17 words of the committed call: leak-ish only if the line truly matches; as sampled, the quoted text 'Split the $18,640,000 Northern Heat Assistance Grant for 2026-27 as Brennock $2,380,000, Dellmoor $2,145,000, Lorrance $...' does NOT appear in the PDF I read (I found no such sentence, no county dollar awards anywhere in target/). Harmless as far as I can verify; the mechanical match appears to be a false positive from shared vocabulary (county names, grant words), though if the checker's call text is a different string, re-check. I found no county award figures.
- PDF 5 of 25 stump terms (account, standard, calendar, northbank, income): harmless. The words occur as definitions and table entries; however 2.3 "calendar month ... gas days dated in the month ... whatever the dates on which meters were read or bills were issued" states the estimand but does not name the move (how to apportion bills across days). Mild: it effectively tells the solver the January series is by gas day, not read date. That is the filed estimand, not a leak.
- docx 8 of 25 stump terms (register, account, months, calendar, northbank, income...): harmless to mild. It names the file mechanics (cycle vs calendar billing, register rollover, cancel/rebill, estimates trued up), which are layer 1 field descriptions and do not say what to do for the decisive step; "billed on calendar months from their daily reads; the other premises are still read on 20 monthly cycles" narrates the split, but not the method.
- prompt sentence with two or more stump terms: harmless. It names the three requested quantities and the file/format; it says "residential" and "January 2026" and does not describe a method. The prompt states the estimand only.
- NNG_READ_SCHEDULE_2026-27.csv 240 dates after 2026-04-20: harmless. It is a next-winter read schedule (2026-27), a declared distractor, dated after the setting only because it is a forward schedule; it is plausible as a real Northbank file (eml: "Northbank their reading schedule for next winter"). It cannot affect January 2026.

#### Realism
- NNG_R1_READS_BIMONTHLY_20260415.txt header "HNNGCIS  R1 BIMONTHLY READS ..." and the trailer fields look plausibly mainframe; no tell.
- export_manifest_2026-04-20.csv: a tidy manifest with exact row counts for every file, plus "covers" descriptions that closely paraphrase the docx; reads as constructed.
- The docx data notes explain every status code and layout in clean prose, and its tables show codes with consistent one-line definitions; a research team note this complete and uniform across three utilities reads authored.
- Date conventions: all three utilities have identical date-range extracts (reads from 1 Oct 2025 to 14 Apr 2026) and common pull date 15 Apr 2026; very uniform.
- Order/activity ID files are perfectly clean (blank REMARKS, regular IDs); the Northline xlsx has a neat 8-column layout with a heading block and an invoice number.
- The eml is short and every sentence supplies a fact the solver needs (who sent what, which files are left unused); it reads as a plot-explaining email, and it flags the GS extract and read schedule as the unused extras.
- The PDF standard is thin (two pages) for an "Edition 3" with a replaced "Edition 2 (March 2022)"; no legal references or revision notes beyond one line.
- Heading-case and sequential names (Brennock, Dellmoor, Lorrance...) with alphabetic initials A-L, N01 to N12 in alphabetical order by utility group; invented fantasy-style county names ("Ashwell, Brennock, Carrow ... Tillery" run alphabetically A to M-T), a generated feel.

### After the portal determinism repair (2026-10-12)

leak.py re-run above: REVIEW, no LEAK, the same lines as the third read (section numbers and the counties' names in the standard, ordinary words in the standard and the notes, the 2026-27 reading schedule's future dates). The repair changed one document: the data notes' account-history line now names the account's HHAP enrollment columns, beside the Ask 2 device and away from the decisive step, so no reader was re-run (/fix-determinism). Nothing on the main path changed.
