## Tags

**Domain:** Economics & Econometrics (elasticity, welfare and policy impact estimation).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Fund measure A, the Prestación Infancia Directa: it brings 3,700 children above the poverty line in 2027 (Valmesura 1,100, Las Cuencas 1,400, Sierra del Alba 1,200).**
Not C, the Complemento's higher limit, which leads only if its newly entitled families were paid all year; not B or D, new payments families must claim; not E, which tops up families mostly far below the line.

## 2. Critical Components

1. Measure A brings **3,700** children above the line in 2027: Valmesura **1,100**, Las Cuencas **1,400**, Sierra del Alba **1,200**.
2. Measure C would bring **18,400** children above the line if every family it covers were paid all of 2027, but its payments received in 2027 bring fewer than **3,000**.
3. Measures B and D also stay under **3,000** in 2027, and E brings **300**.

## 3. Step-by-Step Solution

1. Built each household from ecvv2026_households.csv and ecvv2026_persons.csv: children born 2009 or later, equivalent adults from birth years, 2027 income as 2025 disposable income times 1.061, and computable income per equivalent adult as the appraisal guidance defines it.
2. Gave each measure's households their payments from child_poverty_proposals_2027.pdf and counted, with the household weights, the children moved from below €11,550 to at or above it: with a full year, C 18,400 and A 3,700.
3. Paid A and E for all of 2027 (automatic from January); B, C and D pay a family only once it has claimed, from the month after its claim is decided (appraisal guidance 3.9 with complemento_familiar_rules_2026.pdf, payment).
4. From cfv_register_extract_20261102.csv (both date layouts) took the granted initial claims of the families the April 2024 rise brought in, claimed from that month with computable income from €7,200 to under €8,400, month by month as a share of the survey's households with children in that band (27.9 per cent by the twelfth month) as C's claims, the claims before the rise under €7,200 over the households under it (62.0 per cent) as B and D's, and the months from claim to first payment.
5. Took each household's chance of crossing the line over claim month and decision lag: A 3,700, B, C and D each under 3,000, E 300, so A is funded.
6. Counted each family once in the last month of each quarter of 2025 from resolutions decided by 31 December 2025, keeping awards whose status now reads REVOKED because their revocation is dated 2026, in the province of its municipality (territorial_codes.csv) with the moves in cfv_incidents_2025.xlsx taking effect the month after: the families in the annex.
7. Took each reissue in ecvv2026_fieldwork_cases.csv as the dwelling of the case it reissues (reissue_of, which also joins the reissues whose census section was renumbered from April 2026), each dwelling once at its last issue, in the province of its municipality, with eligibility, complete interviews and the response rate as ecvv2026_main_results.pdf defines them: the fieldwork figures in the annex.

## 4. Deliverable Answers

### cabinet_note_child_poverty_2027.pdf

1. Recommends measure A, the Prestación Infancia Directa: 3,700 children above the poverty line in 2027, Valmesura 1,100, Las Cuencas 1,400, Sierra del Alba 1,200.
2. Bar chart on page 1 comparing the measures' children above the line with a full year of payments and with the payments received in 2027, A highest in 2027.

### appraisal_annex_2027.xlsx

1. Families the Complemento Familiar was paying, as its decisions stood at 31 December 2025, by the province each family lived in that month (families):
   - March 2025: Valmesura 5,408; Las Cuencas 4,949; Sierra del Alba 3,651
   - June 2025: Valmesura 5,697; Las Cuencas 5,154; Sierra del Alba 3,867
   - September 2025: Valmesura 5,866; Las Cuencas 5,289; Sierra del Alba 4,041
   - December 2025: Valmesura 5,934; Las Cuencas 5,374; Sierra del Alba 4,117
2. ECVV 2026 eligible sample dwellings, complete interviews and response rate (per cent) by province:
   - Valmesura: 7,132; 5,172; 72.5
   - Las Cuencas: 5,317; 3,961; 74.5
   - Sierra del Alba: 3,672; 2,834; 77.2
