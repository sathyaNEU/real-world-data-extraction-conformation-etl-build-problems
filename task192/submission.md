## Tags

**Domain:** Political Science & Public Policy, conflict and protest event data analysis.
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**17 per cent of the dispute episodes the register opened between 1 May and 30 October 2026 will have
recorded a confrontational action by the time they close, 108 of the 635 episodes.**
Not the 89 episodes, 14 per cent, that have recorded one by the 6 November extract, which counts every
open episode as one that never will. Not the 22 per cent, 141 episodes, among the episodes whose outcome
is known, which drops 234 open episodes of which the long quiet ones will never produce a confrontation.
Not the 28 per cent, 178 episodes, from a product-limit survival of the time to a confrontational action,
which carries the 312 quiet closures as observations that stopped and so leaves each of them at risk.

## 2. Critical Components

1. The period's cohort is **635 dispute episodes**
2. Episodes with a confrontational action already recorded at the extract: **89**
3. Episodes closed without one: **312**; episodes still open at the extract: **234**

## 3. Step-by-Step Solution

1. Read the accepted items of `registo_itens_imprensa.csv` with `relatos_rede_parceiros.csv` and
   `relatos_linha_publica.csv`, and resolved every `local_texto` to a settlement and its municipality
   through `gazeteiro_localidades.csv`, current and former names alike.
2. Collapsed the reports to the protocol's 2.1 action grain, one theme at one locality on one calendar
   day, so the three routes, the two Atlantic editions and the August reload in `registo_importacoes.csv`
   count once: 4,138 actions dated in the reporting period.
3. Built the register's dispute episodes on 3.1, one municipality and one theme, each closing when 21
   calendar days pass with no action: 635 episodes opened in the period on 3.2.
4. Classified each episode of the cohort at the 6 November extract: 89 with a confrontational action
   coded CF, RF or DP, 312 closed with none, 234 still open.
5. Estimated Indicator 3 over the whole life of the cohort's episodes with a quiet close treated as the
   other way an episode ends, so a closed episode leaves the episodes still at risk and an open one does
   not: 108 episodes, 17 per cent.
6. Reported the period's confrontation rate as 17 per cent, 108 of the 635 episodes.

## 4. Deliverable Answers

### boletim_vigilancia_2026S2.xlsx

1. Confrontation rate of the period: 17 per cent, 108 episodes.
2. Episodes opened in the period: 635; with a confrontational action already recorded: 89; closed
   without one: 312; still open at the extract: 234.
3. Per fortnight, actions recorded, municipalities touched and the share of those actions the partner
   network reported, 13 rows in the file's order, counts as whole numbers and shares to one decimal:
   - Q1, 1 to 14 May: 100 actions, 32 municipalities, 44.0 per cent
   - Q2, 15 to 28 May: 149 actions, 46 municipalities, 47.7 per cent
   - Q3, 29 May to 11 June: 167 actions, 53 municipalities, 39.5 per cent
   - Q4, 12 to 25 June: 184 actions, 64 municipalities, 50.0 per cent
   - Q5, 26 June to 9 July: 211 actions, 69 municipalities, 43.6 per cent
   - Q6, 10 to 23 July: 219 actions, 63 municipalities, 42.0 per cent
   - Q7, 24 July to 6 August: 300 actions, 84 municipalities, 46.3 per cent
   - Q8, 7 to 20 August: 305 actions, 88 municipalities, 43.0 per cent
   - Q9, 21 August to 3 September: 302 actions, 84 municipalities, 49.0 per cent
   - Q10, 4 to 17 September: 441 actions, 99 municipalities, 46.7 per cent
   - Q11, 18 September to 1 October: 500 actions, 100 municipalities, 46.4 per cent
   - Q12, 2 to 15 October: 582 actions, 109 municipalities, 45.5 per cent
   - Q13, 16 to 30 October: 678 actions, 115 municipalities, 46.5 per cent
4. Per access route, the reports received in the period, those the association could not place and the
   median minutes from the start of the action to the report, 3 rows, counts as whole numbers and
   minutes to one decimal:
   - Monitor de imprensa (IMP): 4,779 received, 149 not placed, 109.0 minutes
   - Rede de parceiros (PAR): 1,947 received, 60 not placed, 622.0 minutes
   - Linha de participacao publica (LIN): 1,295 received, 92 not placed, 98.0 minutes
5. Per partner organisation, the reports it filed, those filed after the period closed and the euros
   paid under its data agreement, 7 rows, counts as whole numbers and euros to the nearest euro:
   - P01: 223 filed, 1 after the close, 1,421 euros
   - P02: 677 filed, 2 after the close, 3,915 euros
   - P03: 348 filed, 0 after the close, 2,471 euros
   - P04: 196 filed, 1 after the close, 1,154 euros
   - P05: 109 filed, 1 after the close, 729 euros
   - P06: 78 filed, 0 after the close, 640 euros
   - P07: 262 filed, 1 after the close, 1,670 euros

### acoes_por_quinzena.png

6. One stacked bar per fortnight of the period, the actions recorded with the confrontational ones
   shaded, each bar labelled with the fortnight's total, in the fortnight order of the workbook.
7. Confrontational actions shaded, by fortnight: Q1 2, Q2 3, Q3 4, Q4 6, Q5 11, Q6 2, Q7 9, Q8 6,
   Q9 9, Q10 18, Q11 16, Q12 8, Q13 27.
