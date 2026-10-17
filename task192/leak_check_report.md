# leak check, task192

**Verdict: REVIEW.** 18 files read, 58 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: asserted, sample, classifier, record, carries, quoted, nothing, decisive, correction, double-coding, sentence, protocol, measured, population, method, monitor, shipped, changes, change, reporting, instrument, sensitivity, specificity, reaches, recall

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `boletins_anteriores_2026.pdf`: golden figure 119 appears: ...os Localidades tocadas maio 552 117 333 junho 560 119 341 julho 533 119 337 agosto 553 119 335 setembro...
- **REVIEW** `boletins_anteriores_2026.pdf`: golden figure 117 appears: ...s Municipios tocados Localidades tocadas maio 552 117 333 junho 560 119 341 julho 533 119 337 agosto 55...

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `manifesto_extracao.csv`: 1 ISO dates after 2026-11-06, e.g. 2026-11-25
- **REVIEW** `notificacoes_reuniao_publica.csv`: 95 ISO dates after 2026-11-06, e.g. 2026-11-07, 2026-11-08, 2026-11-09, 2026-11-10, 2026-11-11

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 4 design-note vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

# Reader answers, task192 (isolated read of prompt.txt and bundle/ only)

## Committed number
232 confrontational actions, 1 May to 30 Oct 2026. The raw registry code count is 178 (153 from the press monitor, 25 from partner/line-only actions). Defensible range 227 to 234.

## 1. Which sentence tells the decisive step
Yes, protocol text names it. `protocolo_vigilancia_v4.pdf`, 3.3: "O codigo que o classificador do monitor de imprensa atribui e a leitura do classificador, que a amostra de dupla codificacao da associacao mede contra a codificacao manual. O numero que o boletim fixa e o das acoes que foram de confronto e nao o dos codigos atribuidos."
That is the move in other words: correct the classifier's codes using the double-coding sample. Also 4.5: "A amostra do periodo e o conjunto das duas rondas e mede o classificador no conjunto dos relatos aceites do periodo." The presence of `amostra_dupla_codificacao.csv` (codigo_monitor next to codigo_manual) is a second hint. The 3.3 sentence does not give the HOW (stratified rate, Rogan-Gladen, known-truth substitution), only the WHAT.

## 2. Which file ranks or scores the candidates
None. `indice_tensao_distrital.csv` and `notificacoes_reuniao_publica.csv` are context (not opened as a ranking). `boletins_anteriores_2026.pdf` gives monthly action counts, not confrontation.

## 3. Which file exists only to help the analyst
`amostra_dupla_codificacao.csv` (the correction instrument), `dicionario_dados.xlsx` (sheet `convencoes`: median of even set is the mean of the two middle values; fortnight rule), `manifesto_extracao.csv`, `registo_importacoes.csv` (explains the C20260802 reload). The distractors look like `indice_tensao_distrital.csv`, `notificacoes_reuniao_publica.csv`, `cobertura_meios.csv`, `config_monitor.json` (peso_de_circulacao).

## 4. Which figure or name reads as the answer
- 3.3's "nao o dos codigos atribuidos" reads as the answer's direction (do not count codes).
- `amostra_dupla_codificacao.csv` itself is the answer's instrument (confusion table). Monitor codes CF/RF/DP have manual-conf rates 0.57/0.75/0.65, while the other five codes have 1.8 to 4.1% manual-conf, so the false-negative mass (about 60 of 120 sample true-conf) is visible at once.
- The P12 code, an undocumented partner code (see 9).

## 5. Which filed sentence fixes the figure literally
3.3: "o numero das acoes registadas no periodo de relato que foram acoes de confronto na acepcao de 2.2, em numero inteiro". Read literally: the number of actions in 1 May to 30 Oct (2.1 action = tema x localidade x day, 2.3 gazetteer incl. former names, 2.4 local calendar day, 3.2 period) that WERE confrontational by CF/RF/DP truth. Literal result is the true count, which is not observable; the nearest executable readings:
- codes as filed: 178 (not literal, 3.3 excludes it)
- literal-with-sample: my 232.3 (below). Population = 4,790 actions in the period (4,357 press-covered + 298 partner-only + 135 line-only after dedup of cross-via keys). The rounding to a whole number is filed; the estimator is not.

## 6. What decides the main answer
An analytical choice: whether to count filed codes (178) or correct the classifier's misclassification against the manual sample (about 230). Not semantics (the CF/RF/DP list is stated in 2.2), not rule application (the rules produce 178), not planted. A strong analyst who cleaned the data and read every rule could still file 178, but 3.3 tells them not to. So the decisive step is named by 3.3, though the correction method is left open.

## 7. Do the work
Steps:
1. Dedupe: partner file 1463 rows to 1317 ids (C20260802 reload duplicates 146 rows exactly). Press accepted items 6305 to 4635 reports. Map `local_texto` to gazetteer (all 6,859 map; 14 former names resolve). Drop unplaced (excecoes, 308).
2. Key = tema|localidade|data_ocorrencia (local). Period filter on data_ocorrencia: 4,357 press + 1,246 partner + 875 line rows; 4,790 actions. Press reports never collide with each other.
3. Code per 2.6: press code if the press has the action, else the partner/line code (298+135 actions; 25 confrontational).
4. Cross-source check: for actions that both press and PAR/LIN reported, press code equals the other code only 20.5% (PAR) and 19.6% (LIN); PAR and LIN agree with each other 100% (238), and the manual sample code equals the PAR/LIN code 100% (889 of 889). So the partner/line codes are reliable and usable as extra reference truth for press actions.
5. Estimates of the true count:
   - Class-conditional rates from the 2,600 sample (rate by monitor code), applied to all 4,357 press: 202.4 + 25 = 227.4.
   - Same, sample known exactly (120 true-conf) and the 1,757 unsampled estimated (82.4): 227.4.
   - Two-class rates (flagged 66.3%, unflagged 2.43%): 228.6.
   - Rogan-Gladen with sample sens 0.492 / spec 0.988: 234.1.
   - Known-truth route (sample manual code, else the PAR/LIN code on the same action: 3,161 press actions known, 154 confrontational; 1,196 unknown estimated at 53.3 using non-overlap sample rates; plus 25): 232.3. I file 232.
   - Round-by-round: R1 gives 233.4, R2 224.8 (sampling noise; the two rounds have similar rates 4.6%).
6. Confidence: 55% that the golden is 232 +/- 2, about 90% that it is within 225 to 235. A grader keyed on 228 or 227 is the main risk.
Open choices and their values: raw codes 178; naive sample prevalence (4.6% x 4,357) + 25 = 226.1; class-conditional 227.4; two-class 228.6; Rogan-Gladen 234.1; with partner truth 232.3; including the 308 unplaced or the notificacoes would move nothing (not actions). If the dedup key ignored tema, counts fall; if actions were not deduplicated across vias (6,478 rows) the base inflates (4,790 vs 6,478).

## 8. Realism
Reads as largely generated, with good Layer 1 mess. Good: the P12 code, UTC against local (press lag goes to -10 min for 659 reports if UTC is not converted, and 50 min minimum when Lisbon DST is applied, a clean confirmation); C20260802 reload; adenda rate change; old and new gazetteer names; `totais_por_via` reconciles exactly (IMP 4786 = 4635 + 151, LIN 1013 = 919 + 94, PAR 1380 = 1317 + 63), a bit too exact but it is plausible for a counter table.
Tells (generated):
- `inicio_acao` in all three files: 100% of minutes are multiples of 5, hours exist only 08-11 and 14-19 (zero starts at 12:00-13:59, none before 08 or after 19:59). Real action starts include lunch hour and evenings.
- Press `carimbo_recepcao` minute is not mod 5 (20%), partner delivery hours are flat over 24 h (about 60 per hour, no diurnal shape) while the line file is a bell between 08 and 21.
- Daily counts have no weekday/weekend effect: IMP weekday means 15.8-18.2, weekend 16.8-17.6; PAR and LIN the same. LIN/PAR variance equals mean (Poisson). The September step up (about 550 to 1,248 actions per month, partner monthly reports 2.4x) is a step, not a ramp.
- Classifier: monitor vs manual agree 21.8% overall against 19.8% expected by chance. The five non-confrontation codes are noise; no real classifier is this bad, and agreement is the same across coders (0.189-0.236) and themes (0.20-0.25). Disagreement is independent of coder.
- Lag distributions: LIN min 42, max 206 minutes, bounded and flat-ish; PAR min 276 minutes. Sharp bounds.
- Monthly partner PDF totals are not exactly the file counts, which is realistic.
Double-coding file, directly: no, a real desk would not have produced it in this shape. It is 2,600 hand-coded reports (59.7% of the 4,357 accepted in the period) in two 9-day bursts (R1 12-20 Jul about 130/day, R2 26 Oct-3 Nov about 165/day), including both weekend days at the same rate, four coders each at 30-45 per day with near-equal shares (JB 675, RC 663, MM 640, LS 622), a sample "twice per period" that is about 60% of the population, not a sample. File order is shuffled, ids are the whole press sequence (1 to 4356), codings never precede the action, R1 only holds occurrences to 19 Jul (coherent). It carries exactly the columns the correction needs (both codes, the round) and nothing a desk would add (no confidence, no notes, no second-coder id, no time spent, no disagreement adjudication). It reads as built to be read by an analyst. A desk's own file would be 200 to 500 reports per round with a visible adjudication field.

## 9. Supplementary asks
Fortnight table (14 fortnights from 1 May; the last is the single day 30 Oct; municipalities counted as unique codigo_municipio; "reported by network" = share of the fortnight's actions with at least one PAR report):
| fn | actions | municipios | partner share % |
|---|---|---|---|
| 1 | 247 | 102 | 22.7 |
| 2 | 261 | 106 | 23.8 |
| 3 | 261 | 109 | 28.4 |
| 4 | 264 | 102 | 25.4 |
| 5 | 237 | 104 | 23.6 |
| 6 | 256 | 105 | 29.3 |
| 7 | 233 | 108 | 22.7 |
| 8 | 243 | 105 | 25.1 |
| 9 | 245 | 104 | 31.8 |
| 10 | 589 | 117 | 24.6 |
| 11 | 648 | 118 | 27.3 |
| 12 | 623 | 119 | 27.4 |
| 13 | 647 | 117 | 24.4 |
| 14 | 36 | 33 | 36.1 |
Total 4,790 actions. The records force one answer for actions and municipalities (2.1, 2.3, 2.4, 3.4). Open: whether the share means "any PAR report" (my reading) or the share of PAR reports in all reports; which `ronda` of dedupe the fortnight uses is not a choice.

Per route (reception day within 1 May-30 Oct local; `totais_por_via.csv`, `excecoes_geocodificacao.csv`, lag = local reception minus `inicio_acao`, DST window 29 Mar 01:00 to 25 Oct 01:00 UTC applied to UTC stamps):
| route | received | unplaced | median minutes |
|---|---|---|---|
| press (IMP) | 4,505 | 148 | 111.0 |
| partner (PAR) | 1,298 | 60 | 656.0 |
| line (LIN) | 967 | 92 | 96.0 |
Forced: received and unplaced (the two files). Open: IMP median from the first item (111.0) vs every item (127.0) vs last item (131.0), as press reports hold 1 to 4 items; `carimbo_recepcao` UTC unconverted gives 57.0 (PAR 599.0) which is wrong because of `nota_de_relogio`; the period filter by occurrence day gives the same medians. Decided by `registo_itens_imprensa.csv` carimbo_recepcao vs id_relato grouping.

Per partner (dedup of reload; P12 folded into P07; period by occurrence date; late = delivered local on or after 31 Oct; euros per accepted report at the delivery-day table, P04 6.20 from 1 Aug, late reports paid with the later period per clause 6.2):
| partner | filed | late | euros (excl. late) | euros (incl. late) |
|---|---|---|---|---|
| P01 | 146 | 1 | 928 | 934 |
| P02 | 419 | 2 | 2,481 | 2,493 |
| P03 | 218 | 2 | 1,566 | 1,581 (1,580.50) |
| P04 | 153 | 1 | 907 | 913 |
| P05 | 93 | 1 | 621 | 628 |
| P06 | 61 | 0 | 497 | 497 |
| P07 | 156 | 1 | 992 | 998 |
Open and decided by file: (a) `relatos_rede_parceiros.csv` codigo_parceiro P12 (34 reports from 10 Sep, Norte-only, absent from `acordos_dados_parceiros.pdf`); only `relatorios_mensais_parceiros_2026.pdf` supports folding it into P07 (P07 Sep 38 = 20 + 18, Oct 41 = 24 + 17), nothing states it. Without the fold P07 is 122 filed, 0 late, 781 euros and P12 has 34. (b) late reports in or out of the euros (6.2 says paid with the later period: 7,992 vs 8,045 total). (c) unplaced partner reports carry no partner code (excecoes), so they cannot be attributed. (d) Rate day by UTC vs local: no difference for P04 in these data; the 31 Oct late boundary no difference either (all 8 late reports are 30 Oct actions delivered after midnight, UTC and local agree).
