## Tags

**Domain:** Political Science & Public Policy, conflict and protest event data analysis.
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**450 of the actions the register recorded between 1 May and 30 October 2026 were confrontational
actions, to the nearest fifty.**
Not 600, the count the audited reports' own confrontational shares give when they are carried onto the
record: those shares were measured on 1 May to 31 August, where the classifier marked 8.8 per cent of
press-reported actions, and the rest of the period marks 4.3 per cent. Not 300, the actions the
register carries under the confrontational codes. Not 400, the hand codes where the coding desk
audited with the classifier's code elsewhere. Not 600, the coded count scaled by the classifier's
recall, and not 250, the coded count with its false marks taken out.

## 2. Critical Components

1. Actions recorded in the reporting period: **4,656**
2. Actions with a press monitor report, which carry the classifier's code: **4,228**, of which **271**
   carry a confrontational code
3. Actions reaching the register only through a partner organisation or the public line: **428**, of
   which **49** carry a confrontational code
4. The coding desk's two rounds of hand coding: **1,064** reports drawn, **8** of them with no manual
   code because the desk could not fix one, leaving **1,056** comparisons that cover months **5**, **6**, **7** and **8** of the
   period only, with **77** agreed confrontational, **84** the classifier missed, **18** it marked
   wrongly and **877** agreed ordinary, a recall of **0.4783** and a false-mark rate of **0.0201**

## 3. Step-by-Step Solution

1. Read the accepted items of `registo_itens_imprensa.csv` with `relatos_rede_parceiros.csv` and
   `relatos_linha_publica.csv`, resolving every `local_texto` to a settlement, municipality and
   district through `gazeteiro_localidades.csv`, current and former names alike.
2. Collapsed the reports to the protocol's 2.1 action grain, one theme at one locality on one calendar
   day, so the three routes, the items of one press report and the August reload in
   `registo_importacoes.csv` count once: 4,656 actions dated in the reporting period.
3. Took each action's code on 2.6, the press monitor's where the monitor has a report and the filer's
   otherwise: 4,228 actions on the classifier's code with 271 confrontational, and 428 on a filer's
   with 49 confrontational.
4. Read `amostra_dupla_codificacao.csv`: the desk's two rounds closed on 20 June and 10 September and
   between them cover months 5 to 8 only, with 77, 84, 18 and 877 in the four cells of its 1,056
   comparisons.
5. Took from those cells the classifier's recall, 0.4783, and its false-mark rate, 0.0201, which are
   properties of the classifier and hold on the whole period, rather than the audited reports' own
   confrontational shares, which hold only where they were measured.
6. Rebuilt the confrontational actions among the 4,228 from both rates together, so the actions the
   classifier missed go in and the ordinary actions it marked come out, and added the 49 a filer
   coded.
7. Reported the period's confrontational actions to the nearest fifty: 450.

## 4. Deliverable Answers

### boletim_vigilancia_2026S2.xlsx

1. Confrontational actions in the period, to the nearest fifty: 450.
2. Per fortnight, actions recorded, municipalities touched and how many of those actions the partner
   network reported, 13 rows in the file's order, all three as whole numbers:
   - Q1, 1 to 14 May: 264 actions, 70 municipalities, 65 reported by the network
   - Q2, 15 to 28 May: 251 actions, 63 municipalities, 65 reported by the network
   - Q3, 29 May to 11 June: 240 actions, 68 municipalities, 52 reported by the network
   - Q4, 12 to 25 June: 263 actions, 68 municipalities, 50 reported by the network
   - Q5, 26 June to 9 July: 222 actions, 65 municipalities, 59 reported by the network
   - Q6, 10 to 23 July: 237 actions, 66 municipalities, 56 reported by the network
   - Q7, 24 July to 6 August: 252 actions, 66 municipalities, 68 reported by the network
   - Q8, 7 to 20 August: 260 actions, 66 municipalities, 67 reported by the network
   - Q9, 21 August to 3 September: 253 actions, 69 municipalities, 58 reported by the network
   - Q10, 4 to 17 September: 639 actions, 112 municipalities, 157 reported by the network
   - Q11, 18 September to 1 October: 589 actions, 112 municipalities, 155 reported by the network
   - Q12, 2 to 15 October: 588 actions, 111 municipalities, 156 reported by the network
   - Q13, 16 to 30 October: 598 actions, 111 municipalities, 157 reported by the network
3. Per access route, the reports received in the period, those the association could not place and the
   median minutes from the start of the action to the report, 3 rows, counts as whole numbers and
   minutes to one decimal:
   - Monitor de imprensa (IMP): 4,374 received, 147 not placed, 115.0 minutes
   - Rede de parceiros (PAR): 1,207 received, 58 not placed, 1385.0 minutes
   - Linha de participacao publica (LIN): 947 received, 93 not placed, 107.0 minutes
4. Per partner organisation, the reports it filed on actions in the period, those filed after the
   period closed and the euros its data agreement pays for the ones filed by the close, 7 rows,
   counts as whole numbers and euros to the nearest euro:
   - P01: 147 filed, 0 after the close, 926 euros
   - P02: 413 filed, 12 after the close, 2,386 euros
   - P03: 304 filed, 1 after the close, 2,212 euros
   - P04: 61 filed, 0 after the close, 370 euros
   - P05: 80 filed, 1 after the close, 545 euros
   - P06: 45 filed, 1 after the close, 354 euros
   - P07: 115 filed, 1 after the close, 701 euros

### boletim_confrontos_2026S2.pdf

5. The page leads with 450 confrontational actions in the period, over one bar for each fortnight of
   the actions recorded, 13 bars in the period's order at the heights of answer 2.
