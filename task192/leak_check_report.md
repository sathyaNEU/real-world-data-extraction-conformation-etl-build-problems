# leak check, task192

**Verdict: REVIEW.** 18 files read, 60 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: asserted, classifier, record, quoted, carries, coding, measured, audited, protocol, worksheet, sentence, change, decisive, nothing, monitor, dictionary, population, method, correction, window, changes, quantity, validation, sensitivity, district

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `boletins_anteriores_2026.pdf`: golden figure 119 appears: ...ulho 576 117 340 agosto 504 117 335 setembro 1174 119 482 Notas Uma acao e contada uma vez, qualquer qu...
- **REVIEW** `boletins_anteriores_2026.pdf`: golden figure 118 appears: ...s Municipios tocados Localidades tocadas maio 592 118 349 junho 528 117 333 julho 576 117 340 agosto 50...
- **REVIEW** `relatorios_mensais_parceiros_2026.pdf`: golden figure 103 appears: ...r avaria no portal agosto 46 setembro 117 outubro 103 novembro 31 Plataforma de Bairros da Margem Sul (...

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `manifesto_extracao.csv`: 1 ISO dates after 2026-11-06, e.g. 2026-11-25
- **REVIEW** `notificacoes_reuniao_publica.csv`: 107 ISO dates after 2026-11-06, e.g. 2026-11-07, 2026-11-08, 2026-11-09, 2026-11-10, 2026-11-11

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

## Solver's-eye read (loop 1)

# Reader answers, task192 (bundle only)

## Headline
Decisive step: correcting the press classifier's confrontational codes against the hand coding in `amostra_dupla_codificacao.csv`, and doing it in a way that survives the autumn drop in true prevalence (class-conditional error rates, not the sample's "share truly confrontational given the code"). Committed figure: about 453 confrontational actions, filed as **450**. Confidence about 60% in the 450 bucket, 85% that the answer is 400-500. Naive 332 files as 350. A positive-predictive-value correction files 600.

## 1. Which sentence or file tells you the decisive step
No sentence names the move. Four things point at it:
- protocolo_vigilancia_v4.pdf 3.3: "O codigo que o classificador do monitor de imprensa atribui e a leitura do classificador, que a mesa de codificacao mede contra a codificacao manual. O numero que o boletim fixa e o das acoes que foram de confronto e nao o dos codigos atribuidos." This says to count actions that were confrontational, not codes assigned, and that the desk measures the classifier against hand coding. It does not say how to correct.
- protocolo 4.5: "a codificacao manual e a referencia da associacao".
- The presence of `amostra_dupla_codificacao.csv` with `codigo_monitor` beside `codigo_manual`. Its PA rows are the hint: 211 PA codes, 48 of them truly CF/RF/DP.
- boletins_anteriores_2026.pdf note: September brings two new themes (ENE, FLO), and the monthly action counts jump from about 550 to 1,174. That is the hint that the mix, and so the true prevalence, differs between the sample window (May-Aug) and the autumn. The sample has no ENE/FLO rows.
- dicionario_dados.xlsx, `amostra_dupla_codificacao` sheet, `ronda`: "R2 fechada em 10 de setembro de 2026 sobre os relatos de 20 de junho a 31 de agosto". That shows the sample stops at 31 August.
- config_monitor.json `alteracoes_no_periodo: "nenhuma"` tells you the classifier is stable. That is why class-conditional error rates carry over to autumn.

## 2. Which file already ranks or scores the candidates
None. `indice_tensao_distrital.csv` and `notificacoes_reuniao_publica.csv` do not score confrontation.

## 3. Which file exists only to help the analyst
`amostra_dupla_codificacao.csv` (calibration), and the `convencoes` sheet of the dictionary. The convencoes sheet spells out median, fortnight, action, report, minutes, partner and delivery code, so it is the quasi-instruction file for the asks, not the main call.

## 4. Which figure or name reads as the answer
None directly. The monthly "Acoes registadas" in the boletins (592, 528, 576, 504, 1174) are context. The classifier's own count (CF 156, RF 96, DP 80 = 332 actions) is the tempting number and is wrong by design.

## 5. Which filed sentence, read literally, fixes the main figure
- Protocolo 3.3 plus 2.2, 2.1 and 3.2: "o numero das acoes registadas no periodo de relato que foram acoes de confronto na acepcao de 2.2, ao mais proximo de cinquenta acoes". Confrontational means true code CF, RF or DP. The codes given by the classifier are a reading, and the count is of actions that were confrontational.
- Protocolo 2.6 sets which code an action carries: the press report's code when the monitor covers the action, else the partner or line code.
- Literal result, with no correction: 4,627 actions in the period, of which 332 carry a CF/RF/DP code (302 press, 15 partner, 15 line), so 350 to the nearest 50. A literal reading of "foram acoes de confronto" needs the hand coding, which gives about 453, so 450.

## 6. What decides the main answer
An analytical choice: how to correct a classifier's confrontational codes using the hand-coded sample when the true prevalence shifts between the sample window and the rest of the period. It is not a field or unit reading and not a stated procedure. No planted decoy. The data cleaning (dedupe across vias, gazeteiro old names) gets you to 4,627 actions and 332 coded, and does not decide it.

## 7. Do the work
Steps:
1. Union the three vias, map `local_texto` to `codigo_localidade` through the gazeteiro (names are unique, old names resolve), and key actions on tema, localidade and `data_ocorrencia`. This gives 4,627 actions from 6,205 reports in the period (IMP 4,200 relatos from 6,155 items, PAR 1,154 unique, LIN 851). Code priority is press, then partner, then line.
2. 4,200 actions are press-covered, 427 not. Of the 427, 30 carry a confrontational code from coders, and I take them as is.
3. The sample is 1,000 press relatos: 150 truly confrontational, 95 coded so by the classifier, 74 in both. Sensitivity is 74/150 = 0.493 and false-positive rate is 21/850 = 0.0247. The positive predictive value is 0.78, and a non-confrontational code is truly confrontational 8.4% of the time (PA 22.7%).
4. The sample window, May-Aug, holds 2,001 press actions, of which 194 carry a confrontational code (9.7%). 1,000 of these relatos are hand-coded (150 confrontational). For the 1,001 unsampled with 99 confrontational codes: (99/1001 - 0.0247)/(0.4933-0.0247) = 15.8% so 158. Together 308.
5. Sep-Oct holds 2,199 press actions, of which 108 carry a confrontational code (4.9%). Prevalence is not the sample's. Rogan-Gladen gives (0.0491-0.0247)/0.4687 = 5.2%, so 114.5. An 8x8 matrix inversion gives 113. A theme-stratified version gives 115.
6. Total 308 + 114.5 + 30 = 453, filed **450**.

Alternatives and their values:
- Naive classifier count: 332, 350.
- Positive-predictive-value correction (apply P(true|code) from the sample to all 4,200): about 598, files 600. Wrong, because the autumn share of confrontational codes halves (9.7% to 4.9%) while the classifier is unchanged, and a cross-via check confirms: press CF/RF/DP codes agree with the independent partner or line code 75% of the time in May-Aug and 26% in Sep-Oct (35 pairs).
- Pooled sample rate 15% applied to everything: about 660, files 650.
- Stratified but with sensitivity at its confidence limits (0.42 to 0.57): 440 to 470, still 450.
- Press only (dropping the 30 non-press confrontational actions): about 423, files 400 (not run as a separate figure, arithmetic from the above).

Choices the documents did not make: the correction method; whether the 30 non-press confrontational codes are right (taken as correct); whether sample strata should be by code or by theme (no theme dependence found); the treatment of ENE/FLO (not in sample, classifier unchanged, I assume the same error rates). Nothing I could not compute. Unclear boundaries: 453 sits 28 above the 425 edge. A different sample estimator could tip it to 400.

## Hygiene battery and whether it changes the answer
- Dedupe actions across vias: 6,205 reports to 4,627 actions. Changes the denominators, not the confrontational answer much. I did not compute a report-level count.
- Reposted partner load (C20260802 repeats C20260801 for August; 126 ids duplicated, same timestamp): dedupe by `id_relato`. Dedupe matters for euros and counts, not for the main call.
- Rejected items (19,900 of 26,055) carry no relato.
- Old gazeteiro names: all 6,651 relatos match a name.
- Period: 1 May to 30 Oct. Reports with `data_ocorrencia` 31 Oct to 6 Nov are out (6,651 minus 6,205 = 446 reports); I did not compute what including them would add.
- Clock: `data_ocorrencia` is the local day already, nothing to convert for the date. Only the minutes need time zones.
- Net: cleaning moves the naive count only between 332 and about 340; it does not produce 450.

## 8. Realism
Reads as largely generated, with good surface texture.

Pointing to real:
- Press funnel with rejection reasons (fora_do_ambito 8,770, sem_acao_coletiva 5,390, duplicado_de_item 1,780), item IDs and timestamps in order, daily weekday/weekend profile (IMP Sat 19.0, Sun 13.0 against about 28 weekdays), lag lognormal-like with long tail (IMP 5-95%: 44-302 min, max 1,016), partner deliveries 07-20 UTC with weekday weighting, a P04 rate step and the P07/P12 code merge, monthly partner PDFs that match file counts by delivery month (P01 = 143, P02 = 454, P07+P12 = 129), `totais_por_via` reconciling with rows.

Pointing to generated:
- `totais_por_via.csv` reconciles exactly: IMP 4,658 = 4,507 relatos + 151 exceptions; LIN 988 = 894 + 94; PAR 1,439 = 1,376 rows + 63. A real counter would drift (reposts, rejected, late rows). A perfect match is a tell.
- `amostra_dupla_codificacao.csv`:
  - 1,000 rows is 50.0% of all accepted press relatos for the window (R1 420 of 842, R2 580 of 1,159, monthly 48-52%). No desk hand-codes half the record. A real worksheet would be a few percent, and unrepresentative.
  - Rows sorted by id and `data_codificacao` monotonic non-decreasing across all 1,000 rows (the whole of R1 then the whole of R2). Real sheets are in coding order with jumbled ids, with gaps and re-dos.
  - R2 coded 7 Aug to 9 Sep for relatos from 20 June; the first R2 coding day is seven weeks after the R1 close, while R1 was coded 17 May to 20 June. Five-day weekly pattern with some weekend days (38 Sat, 18 Sun), 56 coding days.
  - Coder loads: RC 360, MM 218, LS 212, JB 210; four coders with exactly four-letter-initial style, every coder works through both rounds.
  - Only 77 rows (7.7%) have a second coding; the 18 "alterado" decisions have no nota, while the notes ("codigo alterado depois de rever o texto completo", 10) sit on rows with no reviewer or decision. Reviewer never equals the coder (0 of 77), which is tidy.
  - `codigo_manual` is the code after the desk's decision, so the first coding is lost, which is what a worksheet would never do. A real worksheet would keep both codings and the decision, free-text notes in varied wording.
  - The 8 notes types are all from a closed list.
- Classifier: disagreements (236 of 1,000, 23.6%) are asymmetric around two confusions (PA to CF 23, DP 12, RF 13) and otherwise a flat spray; BL, CO, MA, OC errors go to all other classes about evenly. A real classifier confuses neighbours (BL with OC, CO with MA). This reads as a relabeller that mixes a planted PA-to-confrontation leak with random noise. Agreement is a constant 75-79% by month, round, coder and theme, which is too stable.
- Action start times: 82% on a multiple of 5 minutes, 889 of the :00 minutes dominate. Hour profile bimodal at 10 and 15. Fine for a register that rounds but a bit neat. 
- Daily volumes: weekday 765-790, Sat 505, Sun 321, with the autumn doubling in Sept 1,174 (new themes). Smooth.
- Partner delivery lag median 1,312 min (about 22h), 5-95% 353-3,943; LIN 98, IMP 115. Reasonable. Delivery by day-of-week is skewed to Monday (Mon 15.4 against 7-9 later), which fits batching.
- `data_ocorrencia` always equals the date of `inicio_acao`, zero exceptions, 6,651 rows. No missing dates and no overnight-start effects.
- Gazeteiro: 560 rows, 14 old names; place names repeat across municipalities in the generated pattern ("Santa Marta (Arcos de Valdevez)").

## 9. Supplementary asks
Fortnight table (13 fortnights, last one is 15 days): actions 289, 257, 234, 257, 265, 259, 230, 231, 248, 581, 565, 554, 657 (sum 4,627). Municipalities touched 111, 110, 100, 103, 104, 103, 100, 105, 111, 116, 118, 119, 119. Partner-reported share % 23.9, 26.5, 20.9, 20.2, 25.3, 23.6, 27.8, 25.5, 23.4, 24.8, 26.5, 26.4, 25.4.
- Actions: forced (protocolo 2.1, 3.4).
- Municipalities: forced (gazeteiro `municipio`, old names resolve).
- Partner share: mostly forced; the share counts actions with a partner report, once per action. An alternative is to count only partner deliveries inside the period, or to include late deliveries (11 deliveries past 30 Oct). Slightly changes a few shares by under 0.5 pt.
- Confrontational count: not forced, as above (450 vs 350 vs 600).

Per route (period):
- Reports received: placed reports by action date in period IMP 4,200, LIN 851, PAR 1,154 (unique). Not placed (excecoes, receipt date in period): IMP 148, LIN 94, PAR 61. Alternatives: by receipt date (IMP 4,198, LIN 851, PAR 1,143), total including excecoes, the counter file (counts reposts: PAR 1,439), and a PAR row count (reposts twice) of 1,376. The definition of "received" is not forced by one sentence; the convencoes sheet says a report counts once per route regardless of loads, which settles reposts. Unplaced counts whether to include 3 exceptions dated 31 Oct to 4 Nov: 151 / 94 / 63 if all.
- Median minutes (action to report): IMP 115.0, LIN 98.0, PAR 1,331.0 for period actions (all actions: 115 / 98 / 1,312). Forced once the clock rules are applied: IMP carimbo in UTC, LIN carimbo in Lisbon local (UTC+1 until 25 Oct 02:00 local), PAR in UTC, action start in district-local time (mainland and Madeira +1 to +0, Azores 0 to -1) from `config_monitor.json`. The conversion check is the naive version: without conversion medians are IMP 59, LIN 44, PAR 1,274. After conversion no negative lags and the minimum is 10 to 12 minutes, which is a self-validating check. IMP relato time is the earliest item carimbo (dictionary says so). Even-count median averages the two middle values (convencoes).
- Clock conversion: forced by config and dictionary. Fall-back hour on 25 Oct is ambiguous for local times in the repeated hour; the effect is negligible.

Per partner (reports on actions in period; late; euros; P07+P12 merged, deduped by id):
- P01 134, 0 late, 850.90; P02 421, 2 late, 2,504.95; P03 216, 1, 1,555.20; P04 127, 3, 761.00; P05 84, 3, 579.60; P06 52, 1, 421.20; P07 (with P12) 120, 1, 738.00. Total 1,154, 11 late, 7,410.85 euros.
- Rounded euros: 851, 2,505, 1,555, 761, 580, 421, 738.
- Reposted load: dedupe by id (126 ids repeated with identical timestamps), pay once. Forced by "relato aceite" and the dictionary note.
- P12 addendum: P12 deliveries from 11 Sep (31 rows) belong to P07, forced by the 8 September addendum and the convencoes sheet. A reader who misses it would drop 31 reports from P07.
- P04 addendum: 6.30 from 1 August by delivery date (clause 6.1). Forced, with a boundary case: PAR-2026-000406 delivered 1 Aug 11:29 for an action of 31 July, so delivery date and not action date decides (price 6.30). The UTC/Lisbon difference does not move any delivery across 1 Aug.
- Late deliveries: not forced for euros. Clause 6.2 says late reports are paid with the period in which they were delivered, which can be read as excluding the 11 late reports from this period's euros: P02 2,493.05, P03 1,548.00, P04 742.10, P05 558.90, P06 413.10, P07 731.85, total 7,337.90. The ask says "euros paid under its data agreement" in the same row as the reports on period actions, so I filed all of them, but this is a second defensible reading and moves 73 euros in total.
- "After the period closed" is delivery after 30 Oct, UTC date equals Lisbon date at those hours (after the 25 Oct clock change), so not ambiguous.
- Delivery codes found: P01 to P07, and P12 only; no other.
- Monthly PDF note for P02 ("entrega semanal interrompida de 13 a 19 de julho") and the P06 note do not alter anything, and the PDF totals match deduped file counts by delivery month.
