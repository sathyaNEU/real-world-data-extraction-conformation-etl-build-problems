## Tags

**Domain:** Political Science & Public Policy, conflict and protest event data analysis.
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**450 of the actions the register recorded between 1 May and 30 October 2026 were confrontational
actions, to the nearest fifty.**
Not 600, the count the audited reports' own confrontational shares give when they are carried onto the
record: those shares were measured on 1 May to 31 August, where the classifier marked 9.7 per cent of
press-reported actions, and the rest of the period marks 4.9 per cent. Not 350, the actions the
register carries under the confrontational codes. Not 400, the hand codes where the coding desk
audited with the classifier's code elsewhere. Not 650, the coded count scaled by the classifier's
recall, and not 250, the coded count with its false marks taken out.

## 2. Critical Components

1. Actions recorded in the reporting period: **4,627**
2. Actions with a press monitor report, which carry the classifier's code: **4,200**, of which **302**
   carry a confrontational code
3. Actions reaching the register only through a partner organisation or the public line: **427**, of
   which **30** carry a confrontational code
4. The coding desk's two rounds of hand coding: **1,000** reports, covering months **5**, **6**, **7**
   and **8** of the period only, with **74** agreed confrontational, **76** the classifier missed,
   **21** it marked wrongly and **829** agreed ordinary, a recall of **0.4933** and a false-mark rate
   of **0.0247**

## 3. Step-by-Step Solution

1. Read the accepted items of `registo_itens_imprensa.csv` with `relatos_rede_parceiros.csv` and
   `relatos_linha_publica.csv`, resolving every `local_texto` to a settlement, municipality and
   district through `gazeteiro_localidades.csv`, current and former names alike.
2. Collapsed the reports to the protocol's 2.1 action grain, one theme at one locality on one calendar
   day, so the three routes, the items of one press report and the August reload in
   `registo_importacoes.csv` count once: 4,627 actions dated in the reporting period.
3. Took each action's code on 2.6, the press monitor's where the monitor has a report and the filer's
   otherwise: 4,200 actions on the classifier's code with 302 confrontational, and 427 on a filer's
   with 30 confrontational.
4. Read `amostra_dupla_codificacao.csv`: the desk's two rounds closed on 20 June and 10 September and
   between them cover months 5 to 8 only, with 74, 76, 21 and 829 in the four cells.
5. Took from those cells the classifier's recall, 0.4933, and its false-mark rate, 0.0247, which are
   properties of the classifier and hold on the whole period, rather than the audited reports' own
   confrontational shares, which hold only where they were measured.
6. Rebuilt the confrontational actions among the 4,200 from both rates together, so the actions the
   classifier missed go in and the ordinary actions it marked come out, and added the 30 a filer
   coded.
7. Reported the period's confrontational actions to the nearest fifty: 450.

## 4. Deliverable Answers

### boletim_vigilancia_2026S2.xlsx

1. Confrontational actions in the period, to the nearest fifty: 450.
2. Actions recorded in the period: 4,627; with a press monitor report: 4,200; only from a filer: 427;
   carrying a confrontational code under the classifier: 302; under a filer: 30; reports hand coded:
   1,000.
3. Per fortnight, actions recorded, municipalities touched and how many of those actions the partner
   network reported, 13 rows in the file's order, all three as whole numbers:
   - Q1, 1 to 14 May: 289 actions, 111 municipalities, 69 reported by the network
   - Q2, 15 to 28 May: 257 actions, 110 municipalities, 68 reported by the network
   - Q3, 29 May to 11 June: 234 actions, 100 municipalities, 49 reported by the network
   - Q4, 12 to 25 June: 257 actions, 103 municipalities, 52 reported by the network
   - Q5, 26 June to 9 July: 265 actions, 104 municipalities, 67 reported by the network
   - Q6, 10 to 23 July: 259 actions, 103 municipalities, 61 reported by the network
   - Q7, 24 July to 6 August: 230 actions, 100 municipalities, 64 reported by the network
   - Q8, 7 to 20 August: 231 actions, 105 municipalities, 59 reported by the network
   - Q9, 21 August to 3 September: 248 actions, 111 municipalities, 58 reported by the network
   - Q10, 4 to 17 September: 581 actions, 116 municipalities, 144 reported by the network
   - Q11, 18 September to 1 October: 565 actions, 118 municipalities, 150 reported by the network
   - Q12, 2 to 15 October: 554 actions, 119 municipalities, 146 reported by the network
   - Q13, 16 to 30 October: 657 actions, 119 municipalities, 167 reported by the network
4. Per access route, the reports received in the period, those the association could not place and the
   median minutes from the start of the action to the report, 3 rows, counts as whole numbers and
   minutes to one decimal:
   - Monitor de imprensa (IMP): 4,346 received, 148 not placed, 115.0 minutes
   - Rede de parceiros (PAR): 1,204 received, 61 not placed, 1,327.0 minutes
   - Linha de participacao publica (LIN): 945 received, 94 not placed, 98.0 minutes
5. Per partner organisation, the reports it filed on actions in the period, those filed after the
   period closed and the euros its data agreement pays for the ones filed by the close, 7 rows,
   counts as whole numbers and euros to the nearest euro:
   - P01: 134 filed, 0 after the close, 851 euros
   - P02: 421 filed, 2 after the close, 2,493 euros
   - P03: 216 filed, 1 after the close, 1,548 euros
   - P04: 127 filed, 3 after the close, 742 euros
   - P05: 84 filed, 3 after the close, 559 euros
   - P06: 52 filed, 1 after the close, 413 euros
   - P07: 120 filed, 1 after the close, 726 euros

### boletim_confrontos_2026S2.pdf

6. The page leads with 450 confrontational actions of the 4,627 recorded in the period, over one
   stacked bar for each fortnight of the actions recorded with the actions carrying a confrontational
   code shaded, and repeats the fortnightly table of the workbook.
7. Actions carrying a confrontational code, shaded by fortnight: Q1 38, Q2 30, Q3 24, Q4 22, Q5 26,
   Q6 23, Q7 16, Q8 26, Q9 22, Q10 37, Q11 20, Q12 24, Q13 24.
