# Judge verdict, task153 (Overton transport loads, September to November 2026)

**Verdict:** NOT_DETERMINISTIC (supplementary asks 4 and 5 only). The main recommendation (23 loads, $17,408) and supplementary items 1 to 3 are forced and reproduce. Items 4 (SMPM and Crossroads months) and 5 (dollars above rack) each hold only under a convention that no shipped file states.

**Disposition:** FIX_NOW. Pin the two undocumented conventions in the shipped files (or move the goldens to the literal file readings). The main call, the counts, the saving, the pack's analytic surface and the stump stay untouched. The main-call runs stay valid. Only asks 4 and 5 need regrading. If the author instead edits card or rack data values, treat it as SEND_BACK.

## Why
The main call is robust: 23 loads and $17,408 reproduce from the files under every reasonable window, scaling and tank-cap choice I tried. Gate C fails on the asks. (a) Ask 5 dollars: the golden equals the contract adder times net gallons plus extras. A literal reading of "billed above its posted rack", with the rack in effect at lifting taken from the date-only rack file, gives different dollars in five of six months. (b) Ask 4: the golden moves every SMPM and Crossroads fill stamped 22:00 or later to the previous day. No file says so, so the file dates give different May, June and July figures for both accounts. Taxonomy: underspecified_objective for (a), competing_defensible_answer for (b).

## Evidence

**Literal reading, main ask.**
- The prompt pins the population (all 157 active units), the window (14 September to 8 November, 40 working days, no listed holiday inside it), whole 8,000-gallon loads per yard, and the saving as each account's charge over the TriState average less the $0.019 adder.
- The prompt does not pin how to estimate "what the island will hand out", the tank reserve, or the historical window. A solver must infer these.
- The offer letter itself says "saves the card programme's charge over the average less our 1.9 cents". That closes the terminal and date spread question for the saving.

**Main-call recomputation (my own pipeline).**
- I used the device-serial to unit mapping, own-yard geofence Enter and Exit pairs, burn since the previous visit cut by driving time, `min(burn, cap x tank)` per visit, and scaling to 40 days.
- My yard draws for 29 June to 23 August, with the cap at tank less 10.2%, are: Memphis 21,183; Jackson 43,503; Nashville 68,072; Cookeville 12,858; Knoxville 37,452; Blountville 27,825.
- The golden's draws are Memphis 21,303; Jackson 44,695; Nashville 69,402; Cookeville 12,898; Knoxville 37,575; Blountville 27,835. All are within 3 percent of mine, and the load counts are identical.
- Counts of 2/5/8/1/4/3 = 23 come out for tank caps of 0.80 to 1.00, for windows ending 23 or 27 August, and for scaling of 40/39 or 40/40.
- They fall to 21 or 22 only if the cap is 0.75 or lower, or if a window is shortened to 3 weeks.
- One window (6 July to 27 August) puts Blountville at 24,160, a 160-gallon margin over the 3-load line. All other margins are 2,400 gallons or more.
- The FMS 2025 data corroborate the model. Island share of burn was 96.9 percent at Jackson and 89.7 percent at Knoxville, and the 2026 model gives 99 and 89.5 percent.
- Weekly visit structure confirmed: Nashville tractors 2.0 visits per week, Blountville tractors 1.0, Cookeville vans 1.0, Knoxville tractors 2.5, others about 5.
- No seasonality: 15 September to 9 November 2025 divided by the same-length summer window is 1.000 to 1.010 for every yard.
- Saving: Riverbend $0.119 less $0.019 = $0.100 x 8,000 = $800 for 7 loads (Memphis 2 plus Jackson 5) = $5,600. Crossroads $0.084 plus $0.015 less $0.019 = $0.080 x 8,000 = $640 for 9 loads (Nashville 8 plus Cookeville 1) = $5,760. SMPM $0.127 less $0.019 = $0.108 x 8,000 = $864 for 7 loads (Knoxville 4 plus Blountville 3) = $6,048. Total $17,408. Reproduced. 23 is under the 32-load cap.
- Competing counts (29 from card gallons, 26 from the 2025 island share, 19 from overnight-only runs) are each wrong for a stated structural reason. The data show Nashville's midweek reload, the Blountville four-night loops and the Cookeville lot-based vans.

**Ask 4, monthly diesel gallons.**

| Account | Month | Golden | Raw file dates | Reproduced by |
|---|---|---|---|---|
| Delta (Riverbend) | May / Jun / Jul | 33,472 / 36,732 / 37,170 | 33,644 / 36,567 / 37,335 | UTC to CDT (-5) |
| Keeble (Crossroads) | May / Jun / Jul | 46,569 / 54,781 / 52,821 | 46,942 / 54,520 / 53,081 | 22:00 rule |
| Holston (SMPM) | May / Jun / Jul | 46,391 / 51,215 / 53,258 | 47,037 / 50,778 / 53,695 (after dedupe) | 22:00 rule and dedupe |

- Delta: the golden reproduces only after treating `TRAN_DATE_TIME` as UTC (-5 in May to July). Matching timestamps to `vehicle_days` ignition windows gives 100 percent fit at -5 and 46 percent as-is. The UTC reading is therefore inferable, but no file states it.
- Crossroads and SMPM: the golden reproduces to the gallon only if fills stamped 22:00 to 23:59 are moved to the previous calendar day.
- That convention is verified against telematics. For fills at 22:00 or later, 100 percent fit the previous day's engine window and only 36 to 53 percent fit the stamped day. Fills at 21:00 or earlier fit the stamped day 100 percent.
- No file states it. I checked all PDFs, notes and workbook XML. The SMPM layout and both pricing schedules say only "date of purchase".
- A literal solver using the file dates gets different May, June and July figures for both accounts.
- SMPM also needs the resent week of 6 July removed (details duplicated, 114 diesel rows, about 13,245 gallons). That is a clean, inferable de-duplication and is not an issue.

**Ask 5, 2025 programmes.**
- Net gallons reproduce as BOL net gallons by delivery month, counting each split-drop BOL once. Jackson: 31,911 / 24,004 / 7,986. Knoxville: 23,977 / 24,021 / 8,021.
- Credit memos CM09072 and CM09074 reverse the July invoices and are rebilled by 260505 and 260509. Netting them is sensible.
- The golden dollars equal contract adder x net gallons plus split-drop, wait-time and freight charges after credits and rebills ($0.024 at Jackson, $0.016 at Knoxville). The golden values are $891, $811, $254, $446, $542 and $191.
- Invoice unit prices equal a posted rack plus the exact adder for all 15 loads. For evening lifts at 18:00 or later the rack used is the next day's posting; at 17:48 or earlier it is the lifting day's. This is how Overton actually billed, and it is not documented.
- The rack file carries only an effective date, so a literal "rack in effect at the time of lifting" by date gives different dollars. Contract-adder reading versus alternatives:

| Month | Golden | Lifting-date rack | Delivery-date rack |
|---|---|---|---|
| Jackson March | 891 | 750 | 765 |
| Jackson April | 811 | 938 | 913 |
| Jackson May | 254 | 257 | 254 |
| Knoxville June | 446 | 412 | 640 |
| Knoxville July | 542 | 620 | 607 |
| Knoxville August | 191 | 191 | 252 |

- Five of six months differ under the literal date reading. Both readings are defensible.
- It is also unclear whether the "billed above rack" figure should be the billing-error view or the contract-adder view. The golden took the contract-adder view.

**Other items.**
- "Last eight weeks" is not pinned in the prompt. The golden uses 29 June to 23 August, the last complete SMPM week. This is inferable, since the three accounts share data only to 23 August. It affects the chart's card-gallon bars and not the counts.
- The draw gallons in the chart vary about 3 percent between defensible methods. The prompt asks for gallons to the nearest gallon, but the draw is not itself a numbered ask.

## Files and hygiene: PASS
- 22 files. Formats: PDF (6), CSV (8), XLSX (4), fixed-width TXT (1), MD (2).
- One file of 78,789 rows (`vehicle_days`) and two of about 21,000 and 33,000 rows.
- Real-looking operational artifacts: resent SMPM batch, device swaps with serial-named telematics rows, split drops, credit memos and rebills, UTC portal stamps.
- Distractors that are not used by the solution: tank wagon prices, IFTA returns, tank register detail (calibration dates, dips), the spare M2s and the DEF lines.
- No authoring or benchmark disclosure, no hidden sheets or comments, no temporal incoherence. The telematics start 3 March and SMPM ends 23 August, consistent with the 28 August pull.
- No public-data contamination and no exclusion-level finding.
- Cross-batch check: not run (other tasks are out of bounds). I saw no duplicate within the package.

## Stump power (Gate F)
- The main call needs a structural draw model: visit-by-visit `min(fuel burned since the previous yard visit, tankful above the reserve)`. It needs the geofence visits, the telematics burn, a reserve fitted from the 2025 FMS fills, and the Nashville midweek reload.
- Easy routes land on 29 (card gallons), 26 (2025 island share) or 19 (overnight-only). A strong model that does only the card-gallon or the share route is stumped for an analytical reason.
- Once the visit model is built the count is robust, so the stump is real but not knife-edge.
- The package does not rank the candidates or hand over the draw. The yard notes describe routes, not method.
- Moderate to high stump power. No too-easy signal.

## Stumping type (Gate G)
`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
- The reported card-gallon series is correct. The stump is estimating what the island can hand out from visit structure and tank limits, on a clean-data basis. On perfectly clean data it would still stump.
- Passes Gate G.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: bulk fuel contracting and fleet fuel logistics. The deciding quantity is dispensable island volume from vehicle visits and tank capacity, which the field itself would model. Swapping "fuel loads" for generic units breaks it, so the domain is not a backdrop.
- Layer 1: UTC portal stamps, device-serial renames, a resent SMPM batch, split drops, credit memos and rebills, fixed-width records, DST.
- Layer 2: the visit-bounded draw model with a tank-reserve cap.
- The easy route a strong analyst takes after correct cleaning is the card-gallon fill (29 loads) or the 2025 island share (26 loads), both wrong.
- The hidden rules in asks 4 and 5 are semantics and rule application. They sit in the asks, not in the main call, so they do not decide the call.

## Fix
Location: input_files and solution. The main call, prompt, counts and saving are unchanged.
1. Ask 5: state when Overton's posted rack takes effect in `overton_rack_postings_2024-09_2026-08.csv` (a header note, evening postings effective the prior day at 18:00), or state in the prompt that the dollars are the amounts Overton billed over the rack it priced each load on, net of credit memos and rebills.
2. Ask 4: document in the SMPM layout and the Crossroads pricing addendum that the card processors date a transaction after 22:00 to the next day, and that Riverbend portal stamps are UTC. Alternatively move the goldens for SMPM and Crossroads to the file dates, leaving UTC conversion as the single inferable fix.
3. Keep every graded figure of the main call frozen.
