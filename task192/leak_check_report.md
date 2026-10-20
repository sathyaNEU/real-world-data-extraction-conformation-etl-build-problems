# leak check, task192

**Verdict: REVIEW.** 18 files read, 38 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: asserted, record, classifier, quoted, carries, coding, worksheet, measured, audited, protocol, sentence, monitor, change, decisive, nothing, shares, dictionary, population, method, correction, window, different, default, changes, quantity

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `protocolo_vigilancia_v4.pdf`: golden figure 4.3 appears: ...cam no registo de itens com o motivo da rejeicao. 4.3 Cada parceiro entrega relatos ao abrigo do seu ac...

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `manifesto_extracao.csv`: 1 ISO dates after 2026-11-06, e.g. 2026-11-25
- **REVIEW** `notificacoes_reuniao_publica.csv`: 109 ISO dates after 2026-11-06, e.g. 2026-11-07, 2026-11-08, 2026-11-09, 2026-11-10, 2026-11-11

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


## Solver's-eye read, wave 8 audit of every shipped build (2026-10-20)

The reader held only a fresh unzip of `target.zip` and `prompt.txt`, with the figure names (not values)
from `generator/figures.json`, and was scored by `.claude/skills/leak-check/score_reader.py`.

### Gate F has failed on this build, measured

| block | hit |
|---|---|
| main call | **1 of 1** |
| ask figures | **98 of 106** (92.5 per cent) |

It filed the call and took almost the whole ask layer. It built the decisive construction correctly, a Rogan-Gladen correction using recall and the false-mark rate, and it chose that form for the right reason, stating that the audit sample covers only part of the window and that prevalence changed across it, so recall alone or the audit's positive predictive value would not carry over. It also found that partner and public-line codes agree completely with the manual code, so only press-only actions need correcting, and calibrated on press-only rows.

**The readability screen holds here.** Asked what sent it there, it said **nothing in the files said to correct this way**, that three protocol clauses point to the manual reference and the classifier's weakness, and that it inferred the correction from the data. So the pack does not teach the method; the gap was crossable anyway.

```
== call figures ==
HIT  call_actions                       golden 450                        reader 450

== ask figures ==
HIT  actions_in_period                  golden 4656                       reader 4656
miss actions_with_a_filer_report        golden 428                        reader 1165
miss audit_months                       golden [5, 6, 7, 8]               reader 4
miss audit_prevalence_share             golden 0.1525                     reader 15.2
HIT  candidates.naive                   golden 320.0                      reader 320
HIT  classifier_false_mark_rate         golden 0.0201                     reader 0.0201
miss classifier_recall                  golden 0.4783                     reader 0.478
HIT  fortnight_rows                     golden 13                         reader 13
HIT  fortnights.Q1.actions              golden 264                        reader 264
HIT  fortnights.Q1.marked_actions       golden 28                         reader 28
HIT  fortnights.Q1.municipalities       golden 70                         reader 70
HIT  fortnights.Q1.partner_actions      golden 65                         reader 65
HIT  fortnights.Q10.actions             golden 639                        reader 639
HIT  fortnights.Q10.marked_actions      golden 39                         reader 39
HIT  fortnights.Q10.municipalities      golden 112                        reader 112
HIT  fortnights.Q10.partner_actions     golden 157                        reader 157
HIT  fortnights.Q11.actions             golden 589                        reader 589
HIT  fortnights.Q11.marked_actions      golden 30                         reader 30
HIT  fortnights.Q11.municipalities      golden 112                        reader 112
HIT  fortnights.Q11.partner_actions     golden 155                        reader 155
HIT  fortnights.Q12.actions             golden 588                        reader 588
HIT  fortnights.Q12.marked_actions      golden 23                         reader 23
HIT  fortnights.Q12.municipalities      golden 111                        reader 111
HIT  fortnights.Q12.partner_actions     golden 156                        reader 156
HIT  fortnights.Q13.actions             golden 598                        reader 598
HIT  fortnights.Q13.marked_actions      golden 25                         reader 25
HIT  fortnights.Q13.municipalities      golden 111                        reader 111
HIT  fortnights.Q13.partner_actions     golden 157                        reader 157
HIT  fortnights.Q2.actions              golden 251                        reader 251
HIT  fortnights.Q2.marked_actions       golden 21                         reader 21
HIT  fortnights.Q2.municipalities       golden 63                         reader 63
HIT  fortnights.Q2.partner_actions      golden 65                         reader 65
HIT  fortnights.Q3.actions              golden 240                        reader 240
HIT  fortnights.Q3.marked_actions       golden 26                         reader 26
HIT  fortnights.Q3.municipalities       golden 68                         reader 68
HIT  fortnights.Q3.partner_actions      golden 52                         reader 52
HIT  fortnights.Q4.actions              golden 263                        reader 263
HIT  fortnights.Q4.marked_actions       golden 24                         reader 24
HIT  fortnights.Q4.municipalities       golden 68                         reader 68
HIT  fortnights.Q4.partner_actions      golden 50                         reader 50
HIT  fortnights.Q5.actions              golden 222                        reader 222
HIT  fortnights.Q5.marked_actions       golden 17                         reader 17
HIT  fortnights.Q5.municipalities       golden 65                         reader 65
HIT  fortnights.Q5.partner_actions      golden 59                         reader 59
HIT  fortnights.Q6.actions              golden 237                        reader 237
HIT  fortnights.Q6.marked_actions       golden 23                         reader 23
HIT  fortnights.Q6.municipalities       golden 66                         reader 66
HIT  fortnights.Q6.partner_actions      golden 56                         reader 56
HIT  fortnights.Q7.actions              golden 252                        reader 252
HIT  fortnights.Q7.marked_actions       golden 28                         reader 28
HIT  fortnights.Q7.municipalities       golden 66                         reader 66
HIT  fortnights.Q7.partner_actions      golden 68                         reader 68
HIT  fortnights.Q8.actions              golden 260                        reader 260
HIT  fortnights.Q8.marked_actions       golden 17                         reader 17
HIT  fortnights.Q8.municipalities       golden 66                         reader 66
HIT  fortnights.Q8.partner_actions      golden 67                         reader 67
HIT  fortnights.Q9.actions              golden 253                        reader 253
HIT  fortnights.Q9.marked_actions       golden 19                         reader 19
HIT  fortnights.Q9.municipalities       golden 69                         reader 69
HIT  fortnights.Q9.partner_actions      golden 58                         reader 58
miss grain                              golden 50                         reader "action"
miss hand_coded_confrontational         golden 49                         reader 161
HIT  marked_rate_inside_the_audited_window_pct golden 8.8                        reader 8.8
HIT  marked_rate_outside_it_pct         golden 4.3                        reader 4.3
HIT  partner_rows                       golden 7                          reader 7
HIT  partners.P01.after_close           golden 0                          reader 0
HIT  partners.P01.euros                 golden 926                        reader 926
HIT  partners.P01.filed                 golden 147                        reader 147
HIT  partners.P02.after_close           golden 12                         reader 12
HIT  partners.P02.euros                 golden 2386                       reader 2386
HIT  partners.P02.filed                 golden 413                        reader 413
HIT  partners.P03.after_close           golden 1                          reader 1
HIT  partners.P03.euros                 golden 2212                       reader 2212
HIT  partners.P03.filed                 golden 304                        reader 304
HIT  partners.P04.after_close           golden 0                          reader 0
HIT  partners.P04.euros                 golden 370                        reader 370
HIT  partners.P04.filed                 golden 61                         reader 61
HIT  partners.P05.after_close           golden 1                          reader 1
HIT  partners.P05.euros                 golden 545                        reader 545
HIT  partners.P05.filed                 golden 80                         reader 80
HIT  partners.P06.after_close           golden 1                          reader 1
HIT  partners.P06.euros                 golden 354                        reader 354
HIT  partners.P06.filed                 golden 45                         reader 45
HIT  partners.P07.after_close           golden 1                          reader 1
HIT  partners.P07.euros                 golden 701                        reader 701
HIT  partners.P07.filed                 golden 115                        reader 115
HIT  press_marked_confrontational       golden 271                        reader 271
miss press_only_actions                 golden 4228                       reader 2842
miss raw_total                          golden 454.91                     reader 320
HIT  route_rows                         golden 3                          reader 3
HIT  routes.IMP.median_minutes          golden 115.0                      reader 115.0
HIT  routes.IMP.received                golden 4374                       reader 4374
HIT  routes.IMP.unplaceable             golden 147                        reader 147
HIT  routes.LIN.median_minutes          golden 107.0                      reader 107.0
HIT  routes.LIN.received                golden 947                        reader 947
HIT  routes.LIN.unplaceable             golden 93                         reader 93
HIT  routes.PAR.median_minutes          golden 1385.0                     reader 1385.0
HIT  routes.PAR.received                golden 1207                       reader 1207
HIT  routes.PAR.unplaceable             golden 58                         reader 58
HIT  sample_comparisons                 golden 1056                       reader 1056
HIT  sample_fn                          golden 84                         reader 84
HIT  sample_fp                          golden 18                         reader 18
HIT  sample_rows                        golden 1064                       reader 1064
HIT  sample_rows_without_a_manual_code  golden 8                          reader 8
HIT  sample_tn                          golden 877                        reader 877
HIT  sample_tp                          golden 77                         reader 77

READ AS A COUNT, so these misses are not sound: the reader answered the size of a set where
the golden holds its members, and the size is right. Read the reader's prose before scoring
the call, and rename the key or ask for the members next time.
     audit_months                       golden [5, 6, 7, 8]                   reader 4

call figures   1 of 1 hit
ask figures    98 of 106 hit (92.5 per cent)

FAIL  the reader landed the call. Gate F has failed and the architecture is spent:
      a ladder is not repaired by hardening, and an ask is not repaired by re-wording.
```
