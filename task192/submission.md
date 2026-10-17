## Tags

**Domain:** Political Science & Public Policy, conflict and protest event data analysis.
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**234 of the actions the register recorded between 1 May and 30 October 2026 were confrontational
actions.**
Not the 178 actions the register carries under the confrontational codes, which counts the labels the
press classifier assigned on 4,357 of the period's actions. Not 126, the same count with the
classifier's false marks taken out, which drops the ordinary actions it marked and leaves the ones it
missed out. Not 336, the count scaled by the classifier's recall, which puts the missed actions back and
leaves its false marks in.

## 2. Critical Components

1. Actions recorded in the reporting period: **4,790**
2. Actions with a press monitor report, which carry the classifier's code: **4,357**, of which **153**
   carry a confrontational code
3. Actions reaching the register only through a partner organisation or the public line: **433**, of
   which **25** carry a confrontational code
4. The coding desk's hand-coding sample: **2,600** reports, with **59** agreed confrontational, **61**
   the classifier missed, **30** it marked wrongly and **2,450** agreed ordinary

## 3. Step-by-Step Solution

1. Read the accepted items of `registo_itens_imprensa.csv` with `relatos_rede_parceiros.csv` and
   `relatos_linha_publica.csv`, and resolved every `local_texto` to a settlement and its municipality
   through `gazeteiro_localidades.csv`, current and former names alike.
2. Collapsed the reports to the protocol's 2.1 action grain, one theme at one locality on one calendar
   day, so the three routes, the items of one press report and the August reload in
   `registo_importacoes.csv` count once: 4,790 actions dated in the reporting period.
3. Took each action's code on 2.6, the press monitor's where the monitor has a report and the filer's
   otherwise: 4,357 actions on the classifier's code with 153 confrontational, and 433 on a filer's with
   25 confrontational.
4. Read the classifier's two error rates off `amostra_dupla_codificacao.csv`, where the coding desk's
   2,600 hand-coded reports give 59, 61, 30 and 2,450 in the four cells.
5. Rebuilt the confrontational actions among the 4,357 from both rates together, so the actions the
   classifier missed go in and the ordinary actions it marked come out, and added the 25 a filer coded:
   234 confrontational actions.
6. Reported the period's confrontational actions as 234.

## 4. Deliverable Answers

### boletim_vigilancia_2026S2.xlsx

1. Confrontational actions in the period: 234.
2. Actions recorded in the period: 4,790; with a press monitor report: 4,357; only from a filer: 433;
   carrying a confrontational code under the classifier: 153; under a filer: 25; reports hand coded:
   2,600.
3. Per fortnight, actions recorded, municipalities touched and the share of those actions the partner
   network reported, 13 rows in the file's order, counts as whole numbers and shares to one decimal:
   - Q1, 1 to 14 May: 247 actions, 102 municipalities, 22.7 per cent
   - Q2, 15 to 28 May: 261 actions, 106 municipalities, 23.8 per cent
   - Q3, 29 May to 11 June: 261 actions, 109 municipalities, 28.4 per cent
   - Q4, 12 to 25 June: 264 actions, 102 municipalities, 25.4 per cent
   - Q5, 26 June to 9 July: 237 actions, 104 municipalities, 23.6 per cent
   - Q6, 10 to 23 July: 256 actions, 105 municipalities, 29.3 per cent
   - Q7, 24 July to 6 August: 233 actions, 108 municipalities, 22.7 per cent
   - Q8, 7 to 20 August: 243 actions, 105 municipalities, 25.1 per cent
   - Q9, 21 August to 3 September: 245 actions, 104 municipalities, 31.8 per cent
   - Q10, 4 to 17 September: 589 actions, 117 municipalities, 24.6 per cent
   - Q11, 18 September to 1 October: 648 actions, 118 municipalities, 27.3 per cent
   - Q12, 2 to 15 October: 623 actions, 119 municipalities, 27.4 per cent
   - Q13, 16 to 30 October: 683 actions, 118 municipalities, 25.0 per cent
4. Per access route, the reports received in the period, those the association could not place and the
   median minutes from the start of the action to the report, 3 rows, counts as whole numbers and
   minutes to one decimal:
   - Monitor de imprensa (IMP): 4,505 received, 148 not placed, 111.0 minutes
   - Rede de parceiros (PAR): 1,298 received, 60 not placed, 656.0 minutes
   - Linha de participacao publica (LIN): 967 received, 92 not placed, 96.0 minutes
5. Per partner organisation, the reports it filed, those filed after the period closed and the euros
   paid under its data agreement, 7 rows, counts as whole numbers and euros to the nearest euro:
   - P01: 146 filed, 1 after the close, 928 euros
   - P02: 419 filed, 2 after the close, 2,481 euros
   - P03: 218 filed, 2 after the close, 1,566 euros
   - P04: 153 filed, 1 after the close, 907 euros
   - P05: 93 filed, 1 after the close, 621 euros
   - P06: 61 filed, 0 after the close, 497 euros
   - P07: 156 filed, 1 after the close, 992 euros

### boletim_confrontos_2026S2.pdf

6. The page leads with 234 confrontational actions of the 4,790 recorded in the period, over one stacked
   bar for each fortnight of the actions recorded with the actions carrying a confrontational code
   shaded, and repeats the fortnightly table of the workbook.
7. Actions carrying a confrontational code, shaded by fortnight: Q1 11, Q2 9, Q3 4, Q4 10, Q5 10, Q6 6,
   Q7 9, Q8 9, Q9 6, Q10 22, Q11 25, Q12 25, Q13 32.
