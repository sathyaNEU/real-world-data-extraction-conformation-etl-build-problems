# Verdict, task145

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair is needed. Two optional wording pins are listed under Fix; neither changes what solvers see on the main call.

## Why
The main call is forced by the literal text. BRK-STD-03 4.3 says the forecast is made on "the plan's shipments for the gateway and the plan's planning assumptions". Assumption 7 of network_plan_2027.xlsx gives the 2027 planning rates (USD 1.3400, EUR 1.6800, GBP 1.8750, CNY 0.18800, JPY 0.0092500). CLR-OPS-11 3.1 routes a shipment as formal when its value for duty exceeds CAD 3,300, or when its goods are under an OGD program. Executed word for word, this gives Dorval 2, Calgary 1, 3 held. Every committed figure reproduced from the shipped files.

## Literal reading and recomputation
Each row gives the figure, the file and field it came from, and whether it reproduced.

| Item | Source | Recomputed | Reproduced |
|---|---|---|---|
| Stacked extract rows | the four highvalue_check files (2025Q4 layout dd/mm/yyyy, no OGD value = none) | 246,908 rows; 14 amended rows (AMEND=Y) re-extract earlier waybills; keeping the later row gives 246,894 shipments, 2025-10-01 to 2026-09-30 | yes |
| Routing replication | route vs (value_for_duty_cad > 3300 or OGD flag) | 100% match on all 246,894 rows, FORMAL 176,809 and CLVS 70,085. So the routing rule, the blank-means-none OGD reading and the CAD rows are confirmed by the data itself | yes |
| Formal entries at plan rates | invoice value x plan rate > 3,300 or OGD | YYZ 43,058, YUL 41,853, YVR 35,134, YYC 28,835, YWG 17,610 | yes |
| Base inbound shipments, Oct 2025 to Sep 2026 | gateway_activity_2024-10_2026-09.csv | 1,384,986 / 775,015 / 891,209 / 403,450 / 501,262; agrees with the plan's Base column | yes |
| Scale to plan shipments, divide by 12 | plan Inbound volumes sheet: 1,421.2 / 801.3 / 933.9 / 411.1 / 515.8 thousand | YYZ 3,682 (3,700), YUL 3,606 (3,600), YVR 3,068 (3,050), YYC 2,448.5 (2,450), YWG 1,510 (1,500) | yes |
| Placement | App. A posts 7/5/6/4/3, 560 line, one at a time | YUL at 721, YYC at 612, YUL at 601; then the highest load is YYZ at 526, under 560, so 3 are held. Loads after placement: YYZ 526, YUL 515, YVR 511, YYC 490, YWG 503 | yes |
| Per-post figures to nearest 5 | computed from unrounded forecasts | 525 / 515 / 510 / 490 / 505 | yes |
| Overtime hours by desk and quarter | ta_legacy and ta_export files, hr_assignment_changes, hr_brokerage_staff | See the rules below. Total 2,664.07, and all 20 cells match the golden after rounding | yes |
| Brandmoor net before tax | ap_invoice_register (Net CAD), finance_cost_centres, portal JSON | See the rules below. Total 220,798.10, and all 20 cells match the golden after rounding | yes |

Overtime rules that gave the match:
- Overtime lines and call-backs are included.
- Call-backs are counted at their punch time, not the 3.00 paid minimum.
- The 153 MIGRATED lines duplicate the legacy 27 to 31 October lines (153 of 153 match on employee, date, code and hours), so they are counted once.
- The desk is the one in force on the work date from hr_assignment_changes.
- The fiscal quarter is cut at April.

Brandmoor rules that gave the match:
- A statement bills the month before its date. All 10,577 portal lines have the statement month one month after the transmission month.
- The March 2026 transmissions come from the 1 April 2026 statements in the AP register, which the portal does not hold.
- Mississauga's February 2026 transmissions use the re-issue BCS-2026-25336-R1 (3,288.40). The original (3,704.40) is reversed by credit memo BCM-2026-00118. Rate schedule note 4 supports this.
- The cost centre maps to the desk through the finance file. The mapping agrees with the client code on all 59 invoices.

Competing answers tested:
- **Volume-only scaling.** This carries the base-year formal ratio from the gateway report (YYZ 4,160, YUL 3,209, YVR 3,511, YYC 2,581, YWG 1,742 a month) onto plan volumes. It gives one post at each gateway and 1 held. It is not licensed, because 4.3 says "planning assumptions" and assumption 7 supplies the rates. The plan's Assumption 2 (goods "and the prices those goods are invoiced at, as in the base") is in invoice currency, so it does not conflict. A competing-answer risk remains: a reader who thinks "as in the base" freezes the formal share. I rate it low, but it is the main fork.
- **Customs-rate-of-the-day routing.** This is the same as volume-only scaling.
- **Desk from home cost centre.** The home cost centre is overwritten to the final desk: 196 of 2,054 overtime lines disagree with the assignment history, for seven transferred employees. Home-cc totals differ materially, for example Mississauga Q3 228 against 273. The prompt says "worked at", so the assignment reading holds.
- **Call-back paid hours.** Using the paid 3.00 gives 2,830 hours against 2,664. The prompt says "worked" and the extract note says HOURS is "the hours the line pays", so punch time holds.
- **Statement-month label.** Using the PDF's "Statement month: April 2025" label instead of the billed month shifts every quarter. The portal contradicts the label on every line, so the billed month holds.
- **Portal fees.** All portal lines carry the 1 February 2026 rates (19.10 / 28.65 / 6.50), so repricing from the portal would be wrong. The statement net in the AP register governs.
- **HR staff headcount.** It agrees with Appendix A (7/5/6/4/3) once the terminated broker is excluded. The licence-granted trainees do not change posts.
- **Rounded inputs.** If per-post figures are computed from the already rounded monthly figures, Mississauga gives 530 and Winnipeg 500 instead of 525 and 505. Computing from rounded inputs is not what the prompt says: it rounds the outputs. The placement is unchanged in every variant I ran.

Margins: Dorval's second post is placed at 601 against 560. The next candidate, Mississauga, is at 526, which is 6% under. These are definitive calculations from shipped data with no estimation freedom, so the gaps are thin-but-clean at worst.

## Files/Hygiene
PASS. 22 files; formats are csv, xlsx, pdf, docx, json and txt. The four high-value-check CSVs are about 60k rows each, and the portal JSON has 10,577 lines.

- **Distractors.** network_plan_2026_issued_2025-09.xlsx (older rates), gateway_activity_2021-01_2024-09.xlsx (lagged B3 counting), export_declarations_monthly, the HR staff file and the portal fees are relevant but unused.
- **Authoring leakage.** None found; I grepped for synthetic, benchmark, generated, trap and decoy.
- **Dates.** The dates cohere with the fiction: the extracts were pulled 6 and 7 October 2026, the plan was issued 18 September 2026, and Appendix A was updated 18 September 2026.
- **Realism.** Mixed date formats, a French-language statement block, an amended-row layout change and legacy and ERP cost-centre schemes read as system-made.
- **Not checked.** The golden xlsx and pptx are not in the package, so I could not review how they look.
- **Exclusion-level findings.** None.

## Stump power
Moderate. The trap that does the work is the plan's FX assumption. A strong analyst can clean everything correctly, take the published gateway-report formal counts and scale by the plan's growth. That gives the one-post-at-each-gateway call with 1 held, which is wrong. About half of strong runs will do this. The supplementary asks add independent traps:
- the migrated duplicate lines,
- home cost centre against assignment history,
- call-back punch time against paid time,
- the billed-month shift,
- the re-issued Mississauga statement,
- the March 2026 transmissions that appear only in the AP register.

## Stumping type
`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.

The reported base-year formal counts are correct. The difficulty is that a forecast of a threshold-driven count under a changed exchange-rate regime is not pinned by the trailing figure. The task would still stump on perfectly clean data. This is a FINE-numbers forecasting shape and passes Gate G.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical` (borderline against rule_application; see below).

- **Domain.** Customs brokerage workforce planning: forecasting the formal-entry workload from invoice-level valuation under planning FX, against a staffing standard.
- **Swap test.** Substituting "hospital visits" or "megawatt-hours" breaks the invoice-currency threshold reclassification, so the domain is not a backdrop.
- **Layer 1.** Layout change mid-year (dd/mm against ISO, a renamed OGD flag), amended-row re-extracts, local date against UTC release time, a legacy against an ERP cost-centre scheme, a time-and-attendance system migration with an overlapping window, a fiscal year from April, and a bilingual statement.
- **Layer 2.** Re-forecast the count of shipments over the CAD 3,300 line at the planned exchange rates, then apply the staffing standard's one-at-a-time placement.
- **Decisive step and easy route.** The easy route is to scale the published base-year formal-entry ratio, which is a correct figure, by plan growth. That gives YYZ 4,160, YUL 3,209, YVR 3,511, YYC 2,581 and YWG 1,742 a month, so one post at each gateway and 1 held, against the golden of Dorval 2, Calgary 1 and 3 held.
- **Borderline.** Part of the decisive step is applying a stated assumption (assumption 7) through a stated routing rule. A client reviewer could read that as rule_application. I class it as analytical because the model must see that the correct trailing figure mispredicts the forward count, and the standard's "planning assumptions" wording does not name the exchange rate.
- **Supplementary asks.** They lean on data semantics and rule application, which is permitted outside the main call.

## Fix
none, with two optional pins:
1. **Prompt or answer file.** Add "computed from the unrounded forecast" to the per-post rounding instruction, or state in the workbook that per-post uses unrounded monthly figures, so the Mississauga 525 against 530 and Winnipeg 505 against 500 rounding fork cannot occur.
2. **Prompt.** Optionally say "worked" means punch time for call-backs. This is already supported by "worked" and by the extract note.

Neither pin changes the analytic surface.
