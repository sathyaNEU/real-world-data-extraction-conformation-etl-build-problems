# Determinism verdict, task130 (Corvane professional liability trust 2027 contribution)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. Every committed answer recomputed from the shipped files; no rerun needed. Optional note below on a +/-1 day convention that moves the unrounded total by about $6k.

**Why:** The trust agreement (Art. 1.3, 2.1, 2.4, Sched. A/B) and funding policy (3.1 to 3.4) pin the estimand: cost at 2027 level of Claims first made by 31 Dec 2027 from incidents on or after each entity's Transition Date, with experience pooled within class, as recorded, with no development or tail factor. Read literally this forces the per-day lag-truncated calculation, and every reading I could build gives either that answer or one the policy text rules out (full-year cost per FTE-year, average cost times count, in-year share). The main call and all supplementary answers reproduce.

**Evidence (all recomputed from target/):**

| Item | Golden | Mine | Source |
|---|---|---|---|
| Experience claims (incidents 2017-2024, covered clinician in incident month, one per incident) | 328 | 328 | rm_claims_register + clinician_fte (both code sets) |
| Experience covered FTE-years | 6,188.6 | 6,188.57 | clinician_fte 2017-2024 |
| 2027 exposure FTE-years | 555.8 | 555.77 | clinician_staffing_plan_2027.xlsx from Transition Dates |
| Expected claims | 11.5 | 11.537 | per-day lag <= (31 Dec 2027 minus day) |
| Contribution | $784,000 | $783,667 | same |
| Naive FTE-year x cost per FTE-year | $4,854,000 | $4,853,804 | |
| By entity (claims / $) | TFH 2.9/227k, AMC 4.6/336k, CMG 3.9/214k, BCH 0.1/7k | 2.9/226,981; 4.6/336,314; 3.9/213,690; 0.1/6,682 | |
| By class | OB 2.0/148k, Surg 2.3/291k, EM 2.0/68k, Anes 0.5/65k, HMS 2.3/124k, PC 1.4/26k, APC 1.0/62k | all match (147,665; 291,389; 67,988; 64,587; 123,874; 25,976; 62,189) | |
| Missing open claims | AMC 2 / $178k; CMG 1 / $6k; TFH, BCH none | AMC IR-2026-00613 ($66k) and IR-2026-01269 ($112k); CMG IR-2026-00734 ($6k); matched via insured reference (RMN via notices, suits via prior_claim_no, Stoneleigh refs undashed); CONTRACT coverage lines excluded | register, notices, QMPL 9/30 xlsx, Stoneleigh csv |
| Sept 2026 covered FTE | 96.3 / 234.3 / 522.0 / 54.9 (907.5) | identical, one FTE per position, entity by cost centre directory | hcm pay lines, crosswalk, cost_centre_directory |

Checks on forks. Per-claim $2M limit never binds (max trended claim $1.75M). Class by first-named covered clinician: no change under any ordering variant tried (0 differences). Duplicate defendant rows across claim and suit numbers carry distinct payments, so summing is correct. Legacy emp_status L rows carry zero FTE. Home_entity would give different FTE (93.6/233.8/525.6/54.5) but the cost centre directory is the filed entity key; HCM dictionary defines home_entity as the worker's record, not the charged entity. The 30 Jun rev1 loss run and the premium history are unused (distractors).

Residual sensitivity (not a fail): shifting the day-count convention by one day (inclusive count) gives about $790k, minus one day $778k. The text "claim first made by 31 Dec" gives lag <= 31 Dec minus incident day exactly, so the golden convention is the literal one; flagged only because the figure is rounded to the nearest thousand.

**Files/Hygiene:** PASS. 16 files; formats csv, xlsx, pdf, md (four). One file over 25k rows (clinician_fte 114,499; also patient_safety 34,864). Carrier files in their own layouts (xlsx with subtotal rows, ref formats differing between carriers), extract log, dictionary. No synthetic/benchmark/solver wording found by grep; no hidden sheets. Distractors: patient_safety_events, premium history, 30 Jun loss run rev1. The data dictionary is descriptive and does not name the lag mechanism. No exclusion-level finding. Mild note: dictionary and premium history read slightly tidy, in-house fixable.

**Stump power:** Good. The trap is the claims-made window with a retroactive date: a strong analyst who cleaned everything correctly can still file $4.854M (cost per FTE-year x exposure), $1.784M (count at average cost), or $1.075M (calendar-year in-year share) and each is internally tidy; only truncating by reporting lag per exposure day, with class-level cost conditional on lag, gives $784k. The supplementary asks (loss-run matching, September FTE by cost centre) add several independent places to slip. Some risk that strong models do apply a lag truncation and land near $0.78 to 0.79M, which would be partial agreement at the rounding level.

**Stumping type:** `mechanism: forecasting` (reporting-lag censored exposure, with an element of method_selection pinned by the filed policy), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Reported numbers are fine; the difficulty is the right estimand and lag-conditioned expected cost, and it survives clean data.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Field's own analysis: expected claims-made cost with reporting-lag and retroactive date (actuarial funding of a new claims-made trust). Layer 1: two payroll systems and code sets, HCM crosswalk, three differently laid out carrier loss runs and reference formats, claim-to-suit chains. Layer 2: lag-truncated expected cost. Easy route: pooled cost per FTE-year times exposure, $4,854,000 (or average cost times count, $1,784,000).

**Fix:** none.

## Disposition

The verdict above is the isolated judge thread's verdict.md, verbatim (one pass at medium effort on a fresh unzip of target.zip, prompt.txt, the submission's graded blocks and the judge's system prompt).

APPROVE, ships with no re-judge. The judge's one optional note (a one-day shift in the day count moves the rounded contribution to $790,000 or $778,000) is closed in the record without moving a figure. The convention is filed on dates: trust agreement 1.3 (a Claim is made on the date it is first received), 1.7 and 2.4 (the Plan Year is the calendar year; a Claim first made after its end is not covered), 2.1 and 2.2 (incidents on or after the Retroactive Date; before the Transition Date, the occurrence policy), Schedule A's note (a policy period ends at 12:01 a.m. on its last date) and funding policy 3.3 (exposure from the Transition Date, earned evenly over the days of the month). checks.py now asserts that those dates give the golden to the cent and that each one-day variant contradicts a sentence read from the shipped PDFs: the days left counted with both ends ($790,000), the delay counted with both ends ($778,000), the Transition Date left out ($778,000), the day before it counted ($790,000); the design note's fork table carries it as SF19. The write-up's step 5 and the golden workbook's Notes line state the day count as the date rule. No document under target/ changed (all 16 files byte-identical to the judged pack); freeze.py check --mode determinism PASS.
