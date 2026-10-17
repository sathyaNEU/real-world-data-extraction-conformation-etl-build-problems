# Determinism verdict, task192

**Verdict:** NOT_DETERMINISTIC (main recommendation, and supplementary answers 3, 4, 5 each carry an open fork). Failure label: `competing_defensible_answer` (governing), with `underspecified_objective` on the fortnight and partner-scope readings.

**Disposition:** SEND_BACK. The committed 234 is one of at least eight values between 226 and 237 that the shipped files leave standing. Closing it changes what solvers see (the protocol text and/or the hand-coding design), so it needs a regenerate and a rerun. The three supplementary forks (fortnight length, P12 code, Azores clock) are fixable in the dictionary/protocol with no rerun of data, but the main fork is not.

Everything below was computed only from `target/` with scratch scripts in `scratch/`.

## Gates

| Gate | Result |
|---|---|
| A (correct) | PASS on arithmetic: every graded figure reproduces under the golden's conventions (table below). The conventions behind the golden are not all shipped (see C). |
| B (facts present) | FAIL, narrow. The UTC to local offset (UTC+1 until 25 Oct 01:00 UTC, UTC+0 after) is in no file; the P12 to P07 link is in no file. |
| C (uniquely forced) | FAIL. Main count: method not forced (226.1 to 236.9). Supp. 3: fortnight length open. Supp. 4: report timestamp and Azores clock open. Supp. 5: P12 and the scope of "filed" open. |
| D (analytical, not semantic) | Main call is analytical in kind (misclassification correction). Fortnight, P12 and clock forks are semantic. |
| E (prompt unambiguous) | FAIL for supp. 3 ("fortnight" undefined in days) and supp. 5 ("the reports it filed" has no window). Main ask is clear but asks for an exact integer of a quantity that can only be estimated, with no estimator named. |
| F (stump power) | Would stump on a lottery, not on analysis: a strong solver who corrects with both rates lands anywhere in 226 to 237 depending on estimator; only RG-pooled matches. Wrong-reason stump. |
| G | see below |
| H | see below |

**Gate G line.** `mechanism: method_or_model_selection` (measurement-error / misclassification correction from a validation sample), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The pack ships no ranked wrong number: 178, 126 and 336 appear nowhere in the 18 files (`boletins_anteriores_2026.pdf` carries only monthly action and municipality counts), so deleting every wrong number leaves the difficulty untouched, and the difficulty is the estimator, not a lens swap. Caveat: protocol 3.3 itself announces that the code count is not the answer ("O numero que o boletim fixa e o das acoes que foram de confronto e nao o dos codigos atribuidos"), so the flip away from 178 is signposted, and what is left to decide the call is the estimator, which the files do not force. Passes G in type, fails determinism on the method.

**Gate H line.** `domain: pass` (event-data measurement: correcting an automated coder's error against a double-coded sample is the field's own work; swap test "protest" for "invoice" would not read the same), `layers: pass` (Layer 1: UTC against local clocks, a reloaded August file, former locality names, three overlapping routes, a partner code change; Layer 2: estimating the true confrontational count from a validation sample with two error rates), `decisive_step: analytical` in kind. The easy route a strong analyst takes after reading everything correctly (corrected counts using precision/recall-of-the-marked, or the sample prevalence applied to 4,357) gives 229 or 226, not 234: a plausible, defensible wrong answer. That is the right shape for H3, but it is only a stump if one estimator is forced, and none is.

## Reproduction

| Figure | Claimed | Mine | Note |
|---|---|---|---|
| Actions in period (tema x gazetteer locality x occurrence day, 3 routes, August reload once) | 4,790 | 4,790 | reproduces |
| With monitor report / conf-coded | 4,357 / 153 | 4,357 / 153 | reproduces; monitor reports map 1:1 to actions (no two monitor reports share a key) |
| Filer-only / conf-coded | 433 / 25 | 433 / 25 | reproduces |
| Hand-coded cells | 59 / 61 / 30 / 2,450 | same | reproduces (2,600 rows, 1,100 R1 + 1,500 R2) |
| Register-code count | 178 | 178 | 2.6 rule; "any route" would give 217 |
| 126 / 336 | 126.4 / 336.2 | reproduces | 126 = 153 x 59/89 + 25; 336 = 153/(59/120) + 25 |
| **234** | 234 | **234.13** | = (153 - 0.012097 x 4357)/(0.49167 - 0.012097) + 25. Reproduces only as Rogan-Gladen |
| Fortnights Q1 to Q13: actions, municipalities, partner share | table | all 39 cells reproduce | 14-day blocks, Q13 = 16 to 30 Oct (15 days) |
| Conf-coded by fortnight | 11 9 4 10 10 6 9 9 6 22 25 25 32 | same, sum 178 | reproduces |
| Route received / not placed | 4,505/148, 1,298/60, 967/92 | same | `totais_por_via` sums; `excecoes` by local date |
| Median minutes IMP / PAR / LIN | 111.0 / 656.0 / 96.0 | 111.0 / 656.0 / 96.0 | IMP only under earliest item per report plus mainland DST offset; see 4 |
| Partners filed / after close / euros | table | all reproduce | only with P12 folded into P07 (P07 = 122 + 34 = 156); unrounded euros 928.00, 2481.15, 1566.00, 907.15, 497.15 (P06), 621.00, 992.00 |

## Probe 1: what 3.3 puts in the figure

Literal reading: the actions recorded 1 May to 30 Oct (3.2) at action grain (2.1: theme x locality x day, locality and municipality from the gazetteer, current or former name, 2.3), dated by occurrence (2.4), coded per 2.6, that "foram de confronto na acepcao de 2.2". 3.3 then says the figure is "o das acoes que foram de confronto e nao o dos codigos atribuidos". The sentence that decides against 178 is that one; a literal reader cannot land on 178, and 4.5 ("a codificacao manual e a referencia da associacao") fixes the hand code as truth. So the target is the true count, which is not observed for 1,757 of the 4,357 monitor actions. 3.3 does not say "estimate", "extrapolate" or name a correction; it only says the sample "mede" the classifier. Literal-only candidates that also respect 3.3: 209 (hand code where sampled, classifier code elsewhere: 120 + 64 + 25), which no sentence rules out.

## Probe 2: is the method forced? Values for the filed population (all + 25 filer-coded)

| Estimator | Value |
|---|---|
| Coded count as it stands | 178 |
| Wrongly marked removed only, via precision (153 x 59/89) | 126.4 |
| Wrongly marked removed only, via FPR (153 - 0.0121 x 4357) | 125.3 |
| Scaled by recall only (153 / 0.4917) | 336.2 |
| Hand code where sampled, classifier code elsewhere | 209.0 |
| Sample prevalence x 4,357 (120/2600) | 226.1 |
| Month-stratified sample prevalence (HT weights) | 225.9 |
| Predictive-value correction (153 x PPV + 4204 x 61/2511) | 228.6 |
| Predictive-value with +0.5 continuity | 229.1 |
| Month-stratified predictive-value | 229.1 |
| Theme-stratified predictive-value | 229.1 |
| Round-wise: R1 rates on actions to 19 Jul, R2 rates on the rest | 230.4 (cut 31 Jul: 232.1) |
| Rogan-Gladen with +0.5 continuity | 232.4 |
| **Rogan-Gladen pooled (the golden)** | **234.13** |
| Hybrid, 120 known + RG on 1,757 unsampled | 234.13 (identical to pooled) |
| Theme-stratified RG | 235.9 |
| Month-stratified RG, own rates | 236.9 |

Estimators span 125 to 337; among those that correct for both kinds of error the integers are 226, 229, 230, 232, 234, 236 and 237 (plus 209 for hand code where sampled). Nothing shipped separates them. No sentence rules out the PPV/NPV family: 4.5 says only that the sample "mede o classificador no conjunto dos relatos aceites do periodo", and that is equally true of precision and negative predictive value as of recall and FPR. The prompt does not mention error rates at all. The only argument for sensitivity/FPR over predictive values is the textbook one that they transport across prevalence; that argument needs the sample to be non-proportional with a prevalence shift, and here the true hand-coded prevalence is flat across months (5.2, 4.0, 4.5, 5.3, 5.2, 3.9 percent; homogeneity p = 0.81), so the data does not discriminate either. Rates by month: sensitivity homogeneity p = 0.31, FPR p = 0.71, so stratifying is not forced by the data either. The correction is "forced in one direction" (up from 178 to the 205 to 237 band, not 126 or 336), but not to one integer.

Sampling uncertainty of the graded figure (parametric bootstrap on the four cells): RG 236 +/- 28 (95% interval 185 to 297); predictive-value 229 +/- 15 (200 to 258). The ask demands a whole-number count: a claimed precision of 0.2 percent against a real standard error of about 12 percent.

## Probe 3: does the sample measure the population being corrected?

Sampled from: accepted monitor reports (4.5), two simple random draws, R1 closed 20 Jul (rows dated 1 May to 19 Jul), R2 closed 3 Nov (dated 1 May to 30 Oct). Corrected: the 4,357 actions that have a monitor report and dated in the period. Same set at the unit level (reports map 1:1 to actions; all 2,600 sampled ids are in-period accepted monitor reports). Not the same set in inclusion probability: sampling fraction by occurrence month is 92, 89, 69, 49, 49 and 44.5 percent (May to Oct), because R1 only drew from the first 11 weeks. 4.5 says "amostra aleatoria simples" and "mede o classificador no conjunto dos relatos aceites do periodo", but the files show the pooled sample is not simple random over the period. Effect on the figure: the non-uniform fraction is harmless to RG if rates are time-stable (they are, p above) and moves the predictive-value family by about 0.5. Figures by choice: pooled 234.1 or 228.6; round-weighted 230.4; month-stratified 236.9 or 229.1. Filer-coded 433: sample has "Nao ha linhas de outras vias" and 4.3 says the filers' codes are "revistos pela mesa", so taking the 25 at face value is supported; RG applied to them would give 250 and is ruled out by that dictionary sentence only weakly (not by a statement that filer codes are error-free).

## Probe 4: the three conventions

- **Fortnights (3.4): OPEN.** The only text is "contam-se a partir de 1 de maio e a ultima quinzena do periodo termina com o periodo" (also in `convencoes`). No file gives the length in days. The period is 183 days. Readings: (a) 14-day blocks, the 183rd day absorbed into Q13 (golden, 13 rows, Q13 = 683 actions, 25.0 percent); (b) 14-day blocks with a 14th one-day row for 30 Oct (14 rows; Q13 = 647 actions, 117 municipalities, 24.4 percent; Q14 = 36 actions, 33 municipalities, 36.1 percent, 3 conf-coded; Q13 conf 29); (c) 15-day blocks, "quinzena" in Portuguese (13 rows; Q1 = 268 actions, 105, 21.6 percent; Q13 = 28 to 30 Oct, 130, 77, 24.6 percent). The golden's absorption rule is not written anywhere. Affects supp. 3 and 7 and the PDF.
- **Median of an even set: CLOSED.** `convencoes`: "a media dos dois valores centrais". PAR set is even (1,246): 655 and 657, 656.0. IMP (4,357) and LIN (875) are odd. A lower/upper-median reader gives 655 or 657, ruled out by that sentence.
- **Partner payment (6.1, 6.2, adenda): mostly closed, two open points.** Rate in force on delivery day, UTC timestamp, P04 6.20 from 1 Aug: no PAR delivery falls within two hours of the 31 Jul/1 Aug midnight, so the clock does not matter. 6.2 plus 3.2 close "after the close" as delivered after 30 Oct. Open: (i) the file carries delivery code **P12** (40 reports, first on 10 Sep, in `relatos_rede_parceiros.csv`) that appears in no agreement table and no PDF. The golden folds it into P07 (P07 156 filed, 992 euros). Only reconciliation to `relatorios_mensais_parceiros_2026.pdf` supports it (P07 September 38 = 20 + 18, October 41 = 24 + 17, November 6 = 1 + 5, by occurrence month) and it is inferred; no sentence links the codes. If P12 is unmapped: P07 122 filed, 0 after close, 780.80 euros, and P12 34 filed, 1 after, 0 euros. (ii) "the reports it filed" has no window: 1,246 in-period actions (golden: P02 419) against all 1,317 rows in the file (P02 449, 32 after close; euros unchanged). Also the reload (`C20260802`, same ids, same delivery stamps) is paid once in the golden; the dictionary says the same report appears twice, which supports it.

Clock for supp. 4: `config_monitor.json` ("o carimbo_recepcao ... vem no relogio UTC ... o inicio_acao vem na hora local do local da acao") gives no offset. Golden applies Portuguese mainland summer time with the change on 25 Oct 01:00 UTC to every locality; those are real-world facts absent from the bundle. Values: IMP raw UTC 57.0; fixed +60 min 117.0; DST-aware (golden) 111.0; DST-aware with the three Azorean municipalities one hour behind (Angra do Heroismo, Ponta Delgada, Praia da Vitoria are all in `gazeteiro_localidades.csv` under distrito "Ilhas" with Madeira) 110.0. PAR raw 599.0, fixed +60 659.0, golden 656.0, Azores-aware 654.5. Which item is the monitor report's receipt time is also unstated (4.2 merges items into one report): earliest item gives 111.0, latest item 131.0, per item 127.0.

## Answers to the two extra questions

**1. Forced or only smooth?** Not forced, and not an artifact of smooth data. Unrounded: sample prevalence 226.09, predictive-value 228.56, month-stratified PV 229.07, round-wise 230.41, RG continuity 232.40, **RG pooled 234.13**, theme RG 235.92, month RG 236.92: a spread of 10.8 (4.6 percent of 234), wider than the integer rounding. Dispersion of the record: daily action counts before the 4 Sep surge chi-square/df 1.15 (mean 17.8, variance 20.5); post-surge 1.17; `totais_por_via` daily pre-surge IMP 1.18, LIN 0.90, PAR 0.98; daily conf-coded actions 1.10; fortnight action counts Q1 to Q9 0.51 (df 8, lower-tail p about 0.15) and fortnight conf counts 0.66 (p about 0.27). These are near 1 at the daily grain and mildly low at the fortnight grain with a p that does not indicate a manufactured record. The honest spread on a plausible-noise record is wider, not narrower: across 20,000 resamples of the four hand-coding cells the RG minus predictive-value gap has mean +7 and SD 24, and RG itself has SD 28. The 8-unit gap observed is a typical draw. So the estimators disagree by more than the rounding on this very file; no stated rounding is hiding it. The one place rounding does the work is the main count: "whole numbers" asks for a unit of resolution on a quantity whose estimator-choice spread is 11 and whose sampling SD is 15 to 28.

**2. Rounding edges.** All 24 rounded graded figures (13 shares, 3 medians, 7 euro amounts, 1 count) clear their edges; the claim of 0.0022 on a share is right. Exact values: Q12 27.4478 (171/623, 0.0022 pp from 27.45), Q3 28.3525 (74/261, 0.0025 from 28.35), Q7 22.7468 (53/233, 0.0032 from 22.75), Q2 23.7548 (0.0048 from 23.75). Every other share is 0.013 pp or more away. Medians are x.0 (even-set average of two integers is x.0 or x.5, no one-decimal edge). Euros are x.00 or x.15, 0.35 from an edge. The count 234.134 is 0.37 from 234.5. These four shares sit near an edge only in the sense that a solver who rounds 171/623 to a three-digit proportion first (0.274) or half-up on 27.45 could flip; since they are exact ratios of integers, the real sensitivity is that one action more or less in a numerator shifts a share by about 0.4 pp (four rounding units), so every share is only as determinate as the 4,790 action reconstruction.

## Hygiene

PASS. 18 files; formats csv, pdf, xlsx, json; `registo_itens_imprensa.csv` has 25,545 rows; distractors (`notificacoes_reuniao_publica.csv`, `indice_tensao_distrital.csv`, `cobertura_meios.csv`, `boletins_anteriores_2026.pdf`) are plausible and unused. No authoring language seen. Temporal: `notificacoes_reuniao_publica.csv` runs to 25 Nov against a 6 Nov extraction (scheduled meetings, acceptable). Not exclusion-level.

## Fix

- Main call (SEND_BACK, regenerate): make the estimand's population filed and then force one estimator by the data, not by narration. Either file the sampling frame (each round an SRS of the accepted reports on record at its close, with its stratum) and make true prevalence shift between strata enough that predictive-value and sample-prevalence estimators are decisively biased against sensitivity/FPR (and then judge only the file), or enlarge the validation sample so the sampling SD falls below the estimator gap. As built, a one-unit answer from a 2,600-row sample with SD 28 cannot be forced by shipped sentences. Do not file the HOW (per project rule); file the WHAT (the stratum structure) and let the data separate.
- Fortnight: add a sentence of days per fortnight and what the 183rd day does, or move the period end so it divides (no rerun of data).
- P12: ship a one-line mapping (agreement addendum or dictionary) or drop the code.
- "Filed": add the window to the ask or dictionary.
- Clock: ship the offset rule, including whether Azores differ, or move the receipt stamps into local time.
