# leak check, task192

**Verdict: REVIEW.** 18 files read, 52 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: asserted, classifier, record, quoted, carries, sentence, coding, worksheet, measured, audited, protocol, decisive, change, nothing, monitor, dictionary, population, method, correction, window, shares, changes, instrument, validation, different

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `boletins_anteriores_2026.pdf`: golden figure 118 appears: ...s Municipios tocados Localidades tocadas maio 592 118 349 junho 528 117 333 julho 576 117 340 agosto 50...
- **REVIEW** `boletins_anteriores_2026.pdf`: golden figure 119 appears: ...ulho 576 117 340 agosto 504 117 335 setembro 1174 119 482 Notas Uma acao e contada uma vez, qualquer qu...
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

## Solver's-eye read (loop 2)

# Reader answers, task192 (loop2)

Committed number: **450** confrontational actions (point estimate about 440, range across defensible methods 394 to 442; the naive registry count is 332, which files as 350). Confidence about 55 to 60 percent that 450 is the graded bucket, about 25 percent for 400, about 15 percent for 350.

## 1. Which sentence or file tells you the decisive step
No sentence names the move. Three passages point at it without naming it.
- protocolo_vigilancia_v4.pdf 3.3: "O codigo que o classificador do monitor de imprensa atribui e a leitura do classificador, que a mesa de codificacao mede contra a codificacao manual. O numero que o boletim fixa e o das acoes que foram de confronto e nao o dos codigos atribuidos." This says the count is of true confrontation, not of codes, and that a manual reference exists. It names no correction method.
- protocolo 4.5 and dicionario_dados.xlsx (sheet amostra_dupla_codificacao): "A codificacao manual e a referencia da associacao." The sheet states the rounds' cuts (R1 to 19 Jun, R2 to 31 Aug). The file's presence and its stated coverage hand over the hint that a classifier-versus-manual confusion can be measured, and that it covers only May to August.
- boletins_anteriores_2026.pdf notes: September "registou a entrada de dois temas ... energia e redes e florestas e fogos". Together with config_monitor.json ("treinado_em 2026-03-18", "alteracoes_no_periodo: nenhuma") this is the only hint that the classifier's behaviour in September and October is unmeasured by the sample. Nothing says to treat it as drift.
Also the 50-action rounding in 3.3 and the Indicator 2 wording tell you an error-corrected estimate is expected.

## 2. Which file ranks or scores the candidates on the prompt's question
None. indice_tensao_distrital.csv and notificacoes_reuniao_publica.csv do not touch confrontation. amostra_dupla_codificacao.csv gives no per-period count.

## 3. Which file exists only to help the analyst
- amostra_dupla_codificacao.csv (the calibration sample).
- manifesto_extracao.csv (row counts) and totais_por_via.csv / registo_importacoes.csv (reconciliation helpers).
- boletins_anteriores_2026.pdf (monthly action counts: I reproduced 592, 528, 576, 504, 1174 exactly with the dedupe, so it validates the action definition).
- dicionario_dados.xlsx sheet convencoes: it also settles the quinzena, median, "relatada por uma via" and "codigos de entrega" conventions.
Distractor-looking files: cobertura_meios.csv, indice_tensao_distrital.csv, notificacoes_reuniao_publica.csv.

## 4. Which figure or name reads as the answer
Nothing states the count. Mild tells: the sample's PA row (48 of 218 PA-coded relatos are manually CF, RF or DP) reads as "the finding"; the 50-action rounding. In config, "alteracoes_no_periodo: nenhuma" reads as a pre-emptive denial of drift.

## 5. Which filed sentence fixes the main figure
- protocolo 3.3: "o numero das acoes registadas no periodo de relato que foram acoes de confronto na acepcao de 2.2, ao mais proximo de cinquenta acoes", read with 2.2 (CF, RF, DP), 2.1 (action = theme + locality + local calendar day), 2.3 (locality via gazetteer, current or former name), 2.4 (local date), 2.5 (unplaced gives no action), 3.2 (1 May to 30 Oct inclusive).
- Literal result of what the registry stores (2.6: IMP code where the monitor has the action, else PAR or LIN code): 4,627 actions in the period, of which 332 are coded CF, RF or DP, which rounds to 350. The literal text "foram acoes de confronto ... e nao o dos codigos atribuidos" excludes this reading. So the literal execution of 3.3 is the true class, which is not in any file and has to be estimated. The documents do not say how.

## 6. What decides the main answer
An analytical choice: correcting the classifier's misclassification (a measurement-error or prevalence-shift problem). Not field reading (the dedupe, gazetteer join and 2.6 rule are stated and reproduce the published monthly counts). Not planted: the drift is in the data, not signposted beyond the passages in Q1. A cleaned, rule-following analyst who takes the 332 registry count (350), or who applies the sample's precision by code to all months (about 531, which files as 550), files a wrong answer.

## 7. The work
Steps.
1. Relatos: IMP items collapsed to one relato per id_relato (4,507, all items agree on code, theme, locality, date); PAR deduped on id_relato (1,376 rows to 1,250, the 126 August reposts are byte-identical copies); LIN 894. All local_texto join the gazetteer exactly (14 former names included). Actions = distinct (theme, locality code, data_ocorrencia) in 1 May to 30 Oct: **4,627** (monthly 592, 528, 576, 504, 1,174, 1,253). Each via has at most one relato per action.
2. Truth for actions with a PAR or LIN relato (1,803 actions, 160 confrontational) is taken from that code. 2,824 actions are IMP only; the true class must be estimated.
3. Sample confusion (1,000 double-coded relatos): the classifier's sensitivity for confrontation is 0.493 and specificity 0.975. Many true CF, RF, DP are coded PA (23 CF, 12 DP, 13 RF of 218 PA), and CF/RF/DP-coded relatos are 72 to 88 percent right.
4. The sample stops at 31 Aug. In the IMP-vs-PAR/LIN overlap (assuming partner and line codes are the truth) the P(truth is confrontation | IMP code PA) is 22 percent for May to Aug (matches the sample's 22.7 percent) but 6 percent in Sep to Oct; P(confrontation | IMP coded CF) falls from 68 percent to 29 percent. The confrontation base rate in partner and line only actions falls from about 13 percent to about 3 percent. So the sample's precision by code (P(truth | code)) does not transfer to autumn, because prevalence fell with ENE and FLO entering, while the error profile given truth looks closer to stable (sample PA|CF 0.34, overlap early 0.36; but the late overlap sensitivity of 0.28 on only 32 true cases is lower).
5. Estimates for the 2,824 IMP-only actions plus 160 known:
   - invert the sample's code-given-truth matrix period by period (May to Aug, Sep to Oct): 197.6 + 82.2 + 160 = **439.8**.
   - Rogan-Gladen with sample sensitivity and specificity, by period: 199.3 + 82.9 + 160 = **442.2**.
   - sample precision for May to Aug, overlap precision for Sep to Oct: 428.8.
   - overlap-derived matrix for both periods: 426 (precision) or 394 (matrix inversion).
   - sample precision across all months, no drift adjustment: 530.6.
   - registry codes only: 332 (or 362 if the 160 known partner-line truths replace nothing and the IMP-only codes are counted raw).
   Buckets: 440 and 442 and 429 and 426 give 450; 394 gives 400; 531 gives 550; 332 gives 350.
   Committed: 450.

Choices the documents did not make: (a) whether the partner and line codes are truth for overlap actions (assumed yes); (b) whether to calibrate with P(truth | code) or P(code | truth), the first giving 531 or 429, the second about 440; (c) whether the autumn behaves like the sample (nothing says so); (d) a single pool or per-period or per-theme calibration; (e) whether IMP-only actions are a random subset (overlap rates are about 30 to 36 percent for every code, so yes); (f) the handling of the sample's mesa decisions (manual code is post-decision, used as filed).
Routes I considered but did not compute: a per-theme calibration (cells too small, 12 themes by 8 codes on 1,000 rows), and the confidence interval (the 394 to 442 spread and a sampling standard error of roughly 30 to 40 actions on the corrected part are my guess, not computed).

## Hygiene battery
Dedupe of IMP items, of PAR reposts, of cross-via action matches, former-name joins, UTC/local conversion, 30 Oct cut on local date: none moves the confrontation count by more than a few actions as long as the dedupe to 4,627 actions is right (published bulletin counts confirm it). Counting relatos instead of actions would change it a lot (1,5xx CF/RF/DP relatos). No classifier-code-based path is changed by cleaning; the answer 350 survives all cleaning and is wrong.

## 8. Realism
Reads as generated in several places, but the pack is mostly plausible.
Generated tells.
- amostra_dupla_codificacao.csv is exactly about 50 percent of relatos in every month (May 52.0, Jun 47.7, Jul 48.2, Aug 52.0) and exactly 50.0 percent in each round (420 of 842, 580 of 1,159). A coding desk's own sample would be a round number or a fraction that varies. The sheet is sorted by id_relato, with data_codificacao monotone in id, so the desk worked through the relatos in id order. A real desk's worksheet would be in the order they were pulled. Daily loads are repeated values (6, 7, 10, 11, 12, 15, 18, 19, 21, 24, 26, 32, 40 per day), like batch sizes from a formula. R1 spans 17 May to 20 June, R2 7 Aug to 9 Sep, with no codings between 21 June and 6 Aug, though R2's lot includes relatos from 20 June. Coders are tied to weekdays (RC only Mon, Wed, Thu, Sat; MM never Wed, Fri-light). The weekend days are few: Sat 38, Sun 18, which fits "dias de recuperacao". The reviewer is never the coder (0 of 77), reviewed 7.7 percent. Notes appear on 47 rows, and none of the 10 rows with the note "codigo alterado depois de rever o texto completo" has a reviewer or a decision, which is self-contradictory. Of 18 "alterado" decisions, 11 end with manual equal to the monitor code, i.e. the desk's alteration puts the code back where the classifier had it, which is possible but 61 percent is odd. Coder agreement with the classifier is the same across all four coders (74 to 79 percent), which is too uniform. A real worksheet would have an open column of coding time, a mix of statuses, blanks, uncoded rows, corrections, and a non-id order.
- The classifier reads as a noisy relabeller rather than an instrument: errors are a symmetric confusion with a hand-set structure (the true CF, RF, DP are shifted toward PA, OC, BL; true non-confrontation rarely gets a confrontation code); each code has about 80 to 90 percent diagonal. Real classifier errors would depend on text features, such as organ, theme and day, and I could see none except prevalence and theme drift.
- Start times: 82 percent fall on minutes divisible by 5, the rest are uniform; hard floor at 07:00 and cap at 21:55 for all three vias, nothing earlier or later (real actions, blockades and vigils would sometimes start at 05:00 or 23:00). Hour profile is the same shape in IMP, LIN and PAR (mean 14.0 to 14.2, sd 3.6).
- Day of week: Mon to Fri roughly equal, Saturday about 60 percent and Sunday about 35 percent of weekdays, smooth.
- Lags: IMP median 115 min (min 12, p99 491), LIN 98 (min 10), no negative lag after the district time zone conversion (so the clock design is clean), PAR median 1,331 min with min 12. Partner delivery times are 07:00 to 19:59 UTC only, nothing overnight or at weekends in any month, another hard cutoff.
- Reconciliation: totais_por_via equals files plus exceptions plus the repost exactly: IMP 4,507 + 151 = 4,658; LIN 894 + 94 = 988; PAR 1,250 + 63 + 126 = 1,439. A real counter would rarely reconcile to the unit; the repost rows keep their original delivery timestamps (carga C20260802 carries the same stamps as C20260801), while the counter registered them on 14 Sep (PAR 135 that day). A real reposted batch would carry new delivery stamps.
- Names and numbers: gazetteer names like "Santa Marta (Arcos de Valdevez)", "Ribeira Brava (Chaves)" and "Monte Redondo (Cantanhede)" are generated: Ribeira Brava is a Madeira name used in Chaves. indice_tensao_distrital.csv is random (index 18 to 74, trend labels unrelated to the next value).
- Reads as recorded: ids with gaps (rejected relatos removed), IMP rejection reasons, item duplicates per action, the 14 former names, monthly counts that match the published bulletin, the Azores clock shift on 25 Oct, the manifest.

## 9. Supplementary asks
Fortnights (13: 1 May to 30 Oct, 14 days each, the last 15 days).
Actions and municipalities (forced given 2.1, 2.3, 2.4, 3.4):

| fortnight | actions | municipalities | PAR-reported actions (any delivery date) | PAR delivered by 30 Oct |
|---|---|---|---|---|
| 1 | 289 | 111 | 69 | 69 |
| 2 | 257 | 110 | 68 | 68 |
| 3 | 234 | 100 | 49 | 49 |
| 4 | 257 | 103 | 52 | 52 |
| 5 | 265 | 104 | 67 | 67 |
| 6 | 259 | 103 | 61 | 61 |
| 7 | 230 | 100 | 64 | 64 |
| 8 | 231 | 105 | 59 | 59 |
| 9 | 248 | 111 | 58 | 58 |
| 10 | 581 | 116 | 144 | 144 |
| 11 | 565 | 118 | 150 | 150 |
| 12 | 554 | 119 | 146 | 146 |
| 13 | 657 | 119 | 167 | 156 |

Third column ways of computing it: (a) actions with a PAR relato, counted once, whatever the delivery date (convencoes "acao relatada por uma via"; 1,154 in total); my filing. (b) Only those delivered by 30 Oct (1,143; differs in fortnight 13 only, 167 vs 156). (c) PAR relatos instead of actions (1,250 unique; 1,376 with reposts). (d) Actions reported only by PAR (excluding those other vias also saw). (e) By fortnight of delivery instead of action date. The dictionary convention picks (a), so I treat it as forced except for the late-delivery wording in the prompt ("how many of those actions the partner network reported", no cutoff), which is a residual ambiguity (b). Municipalities touched per fortnight: forced (gazetteer municipio; 119 over the whole period).

The count per route (reports received, unplaced, median minutes):
- Received by arrival day (Lisbon time) in 1 May to 30 Oct: IMP 4,198 placed, 148 unplaced; LIN 851 placed, 94 unplaced; PAR 1,143 placed, 61 unplaced (reposts counted once). By action date instead: IMP 4,200, LIN 851, PAR 1,154 placed (exceptions carry no action date, so they only work on arrival date). The prompt does not say received-by-arrival vs on-actions-in-period, so this is **not fully forced**: IMP 4,346 vs 4,351 and PAR 1,204 vs 1,215 and so on. Totals including reposts (totais_por_via) would be wrong.
- Median minutes (placed relatos, action start converted to the district's clock, Lisbon stamps for LIN converted to UTC, IMP uses the first item stamp): IMP 115.0, LIN 98.0, PAR 1,327.0 by arrival date, 1,331.0 by action date. IMP and LIN forced; PAR differs by 4 min between bases. Without the clock conversion the medians are IMP 59.0 / LIN 44.0 / PAR 1,274.0, and with Lisbon clock against UTC stamps 116.0 / 100.0 / 1,331.0.
- Using the first item for IMP is stated in the dictionary. Using the later item would change IMP.

Partner organisations (reports on actions dated in the period, deduped; filed after the period closed on 30 Oct; euros for those filed by the close):
P01 134 / 0 / 851 EUR; P02 421 / 2 / 2,493; P03 216 / 1 / 1,548; P04 127 / 3 / 742; P05 84 / 3 / 559; P06 52 / 1 / 413; P07 with P12 120 / 1 / 726 (P12 started 11 Sep, the 8 Sep addendum merges the codes). Euros are the sum over relatos filed by 31 Oct 00:00 UTC of the table in force on the delivery day; P04 uses 5.45 before 1 Aug and 6.30 from 1 Aug by delivery date (46 pre, 81 post; by action date 47 pre, so the choice matters by about 1 relato, 0.85 EUR, no rounding impact seen). Clause 6.2 is not consulted for the period total. Not forced: repost handling (counting reposted relatos twice would add the 126 repost rows, but the relato is "accepted" once and the repost keeps the same delivery stamp, so once is the defensible reading); the "filed by the close" boundary (30 Oct local vs UTC, no relatos fall in the gap); counting codes P07 and P12 separately would split the figure. Delivery codes: P01 to P07 and P12 only; no other codes, no blank codes.
Clock conversion: forced by config_monitor.json fusos_horarios and the Azores distinct from Madeira, with the DST end at 25 Oct 01:00 UTC; the gazetteer distrito decides. Without it the lags are off by 1 hour for most actions, 0 for Azores before 25 Oct.
Reposted load: forced by id_relato (PAR-2026-000407 and 126 more appear in C20260801 and C20260802 with identical fields).
Addenda: P04 rate change from 1 Aug (forced by the table and the delivery stamp) and P07 to P12 on 10 Sep (forced).
