## Tags

**Domain:** Psychology and behavioural science (decision-making and computational behavioural modelling).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**Budget about TNK 11,500,000 for the employer's match on Vindeholm County Hospitals' 2027 intake in FY2027, with about 1,600 of the intake contributing on the December 2027 payroll.**
Every hire holds the three per cent default until making a choice, and the opt-in record shows that 90 per cent have chosen by their twelfth payroll while 43 per cent of those who choose join. Not the income protection cover's cancellations carried as the plan's opt-outs (about TNK 14,500,000).

## 2. Critical Components

1. Share of hires who join when joining is their own choice (the join curve's five-year level): **43 per cent**.
2. Share of hires who have made a choice by their twelfth payroll (the join curve over that level): **90 per cent**.

## 3. Step-by-Step Solution

1. Took every spell starting from January 2019 in hr_employment_history_2019_2026.csv as a hire, followed to the October 2026 payroll or the month it ended.
2. Placed each membership in ledstrand_member_register_2026-10.xlsx on its spell through either employee number and the month of its first contribution, and built the share of hires joined by each payroll month of service, leavers censored (Kaplan-Meier); its five-year level is 43 per cent.
3. Read the share who have made a choice by each month as the join curve over its five-year level (90 per cent by the twelfth payroll); the income protection cancellations in tarnmark_ipc_bordereau_2019_2026.csv, over their own five-year level, run on the same clock.
4. Built the share of hires still on the payroll by month of service from the same spells, and the average match on joiners' rates at join under the rules' formula.
5. For each requisition in vch_hiring_plan_2027.xlsx, paid at the 2027 scale for its grade and FTE from its planned start, summed over its 2027 payrolls: still employed times pay times (not yet chosen at three per cent plus joined at their own rates' match).
6. The 2026 match: ERM lines on the January to October 2026 payrolls of every run, each employee's line counted once per payroll and run, by cost centre.
7. Members: Ledstrand's Active memberships opened before 1 January 2019, less those whose HR contract ended on 31 October 2026, by the cost centre of their October 2026 payroll.
8. The FY2027 match on the 2027 intake is about TNK 11,500,000.

## 4. Deliverable Answers

### vindeholm_match_forecast_2027.xlsx

1. Employer match on the 2027 intake, FY2027, group (to the nearest half million TNK): 11,500,000
2. By hospital (to the nearest hundred thousand TNK):
   - Vindeholm Central Hospital: 3,800,000
   - Rendholm Hospital: 2,300,000
   - Askvik Hospital: 1,700,000
   - Ostervall Hospital: 1,400,000
   - Brannby Hospital: 1,200,000
   - Lidmark Hospital: 1,000,000
3. Intake contributing on the December 2027 payroll (to the nearest hundred): 1,600
4. Employer match paid on the January to October 2026 payrolls (to the nearest thousand TNK):
   - Vindeholm Central Hospital: 27,990,000
   - Rendholm Hospital: 14,628,000
   - Askvik Hospital: 11,882,000
   - Ostervall Hospital: 9,827,000
   - Brannby Hospital: 8,466,000
   - Lidmark Hospital: 7,134,000
5. Members since before 2019 still active on 1 November 2026:
   - Vindeholm Central Hospital: 728
   - Rendholm Hospital: 354
   - Askvik Hospital: 302
   - Ostervall Hospital: 238
   - Brannby Hospital: 199
   - Lidmark Hospital: 187

### match_forecast_note_2027.docx

1. A one-page note to the employment committee stating the FY2027 line (TNK 11,500,000) and each hospital's figure.
