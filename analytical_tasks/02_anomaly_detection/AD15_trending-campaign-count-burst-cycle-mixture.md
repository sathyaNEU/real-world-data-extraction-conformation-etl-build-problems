# AD15 — How many coordinated campaigns the integrity report refers to enforcement, when bot bursts run on timers and several timers hit the same article

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Product Analytics · content integrity and trust & safety |
| Mirrors | Counting coordinated operations rather than affected items, when several operations share targets (coordinated inauthentic behaviour takedowns at Meta, fake-engagement networks on Google and YouTube surfaces, review-farm enforcement in marketplaces) |
| Decision shape | One figure committed at a date: the number of coordinated campaigns in the Q3 integrity report to the trust and safety council, filed 15 October, each opening one enforcement investigation |
| Committed call | Coordinated campaigns that inflated trending-rail candidates in Q3, as a whole number, with each campaign's burst period |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · a mixture, not a constant (E31): the unique set of burst cycles under which every verified minute agrees, with finer controls separating constructions at the lower rung (E16) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #3 stops at a close but inexact match · #12 stops at the first control that passes · #2 counts file rows instead of the real unit |
| Calibration form | Gold-standard verification subsample: 50 article-days of the two closed quarters that the forensic team resolved minute by minute, with every inauthentic view attributed to its campaign from server-side fingerprints |
| Driving force | Each campaign fires a fixed burst at a fixed period and phase across its own list of articles, and twelve articles sit on two lists, so their minute series is the sum of two cycles. A single period per article reproduces every verified day's total and none of the verified minutes on those twelve; co-movement clustering chains campaigns that share an article into one. Only the decomposition into cycles, the unique set of periods and phases under which every verified minute agrees at zero tolerance, counts the operations, and it gives nine. |

## 1. Situation

A media app's trending rail draws on article views. The integrity team's composite flags article-days whose view spikes look inauthentic, and
each quarter its report to the trust and safety council states how many coordinated campaigns it found; enforcement opens one investigation
per campaign. The council's reporting standard defines a campaign as one coordinated operation, whatever the number of articles it targets.
The pack carries minute-level view counts for every candidate article by access method from January to September, the composite's
flags, the cross-language series, and the forensic team's verification subsample from the two quarters it has closed.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the minute counts, the composite's indicators and flags, and the forensic attributions. The
  integrity lead's flagged articles are genuinely inflated. Nothing reported is overturned; the difficulty is that the unit the report
  counts, an operation, is not an article and not a cluster of co-moving articles.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the composite's flags. The minute series still show bursts, and fitting one timer per inflated
  article, the natural reading, still yields 13.
* **Instrument repair.** Suspect file: the forensic subsample, 50 article-days of the two closed quarters. Filled, every article-day of Q1
  and Q2 resolved minute by minute, it pins the same cycle structure on more days and names none of Q3's operations, which began after the
  closed quarters' campaigns had stopped; rung 0 still counts 47, rung 1 13 and rung 2 6. Q3's minute counts are exact and complete, and the
  access-method split is a correct record of a different attribute. No Q3 row claims a campaign, so the decomposition into cycles is still
  needed for 9.
* **Lens swap.** The naive count is of articles or article clusters; the answer counts cycles, a population of operations each spanning
  several articles, with twelve articles belonging to two of them.

## 3. The driving force

A strong solver distrusts one-campaign-per-article, notices the bursts are periodic, finds each inflated article's dominant period, groups
articles by period and phase, and checks the forensic subsample: every verified article-day's inauthentic total reproduces within 1%. It
reports 13. Each step is competent. But an article on two campaigns' lists carries two cycles, a 23-minute and a 31-minute one, say, and
its dominant period is whichever burst is larger; the residue is a second "campaign" of its own or vanishes into noise. Thirteen is
nine true cycles plus four artefacts of mixed articles. Clustering articles by co-movement instead runs the other way: the twelve shared
articles chain campaigns together and the count falls to six. The subsample's minute-level attributions are the finer control. They are
reproduced at zero tolerance only by a decomposition in which every burst minute is the sum of the cycles scheduled on it, each cycle a
fixed period, phase and burst size across its own article list, and that decomposition is unique.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | One campaign per article the composite flags | 47, +422% | The composite is the team's own screen and every flagged article is inflated | The council's standard counts operations, whatever the number of articles, and flagged articles burst in step in groups |
| 1 | One period per inflated article (its dominant spectral peak), campaigns as distinct period-and-phase pairs | 13, +44.4% | Reproduces every verified article-day's inauthentic total within 1%, the subsample's headline control | The subsample's minute attributions: on the 12 verified days with two campaigns, single periods reproduce no minute |
| 2 | Co-movement clustering of inflated articles' excess series | 6, −33.3% | Groups articles the way coordination looks, no period assumed | The subsample: three of its verified campaigns share articles yet never burst in the same minute, so clusters linked through shared articles are not one operation |
| 3 | **Decisive:** burst minutes decomposed into cycles, each a fixed period, phase and burst size over its own articles, mixed articles carrying the sum, checked minute by minute against the subsample | **9** | — | — |

* **Figure shape.** The corrections walk the count down from 47 to 13 to 6, and the decisive move reverses them to 9. Per-rung offsets are
  +422%, +44.4% and −33.3%, and with the answer a small integer, every off-by-one lands at least 11% away.
* **Partial correction priced (L3).** A solver who decomposes mixtures but matches cycles on period alone, ignoring phase, merges the two
  pairs of campaigns that share a period and lands at 7 (−22.2%). A solver who decomposes each article but never takes the union across
  articles counts 31.
* **Grid.** Unit (article, single-period cycle, co-movement cluster, decomposed cycle) × phase (used or ignored) gives eight cells: 47, 13, 6
  and 9 with phase, 47, 11, 6 and 7 without. The nearest wrong cell is 7 or 11 (both 22% away), each one convention from the answer and each
  refuted by the subsample's minutes.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says a campaign is one operation. Nothing says operations run on timers, that articles can sit on two
   lists, or how to count them.
2. **The corpus pins a construction, not a menu.** The cycle decomposition reproduces all 50 verified article-days minute by minute; single
   periods reproduce 38 (all the single-campaign days) and clustering 31, and both rivals get the twelve mixed days wrong in the same
   direction for each. The decomposition is a construction: the cycles exist only after burst minutes across all articles are explained
   jointly, and no column holds a campaign.
3. **No arithmetic symptom.** Single-period fits reproduce every day's total, the decisive control everyone checks first; nothing fails
   until the minutes are compared.
4. **Not a row predicate.** It needs burst detection per article, a joint fit of periods and phases across articles, and a minute-level sum of
   cycles on mixed articles.
5. **The enumeration is arithmetic.** Each of the nine cycles is the unique period and phase consistent with every burst minute; every
   cycle repeats more than 300 times in the quarter, so no second solution fits at zero tolerance.
6. **No cutover date.** All nine campaigns run through the whole of Q3, and the closed quarters' campaigns had stopped before it began;
   no series steps inside the quarter.
7. **Survives deletion.** With every voice and the composite removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The forensic subsample: 50 article-days drawn from Q1 and Q2, the two quarters the forensic team has closed, each resolved
  minute by minute from server-side fingerprints, with every inauthentic view attributed to a campaign. Every campaign it verified was
  referred and had stopped by mid-June; Q3's nine cycles all began in the first days of July.
* **What it pins.** Campaigns are cycles of fixed period, phase and burst size; twelve verified days carry two campaigns, whose minute counts
  are exact sums; no verified day carries three.
* **Twin pair.** Verified days V-08 and V-33 are identical on every composite indicator (desktop-share change, hourly concentration,
  cross-language corroboration, automated co-movement) and on daily views and excess. V-08 carries one campaign and V-33 two (2×); only the
  minute decomposition separates them.
* **Every rule exercised.** Two campaigns share a period (29 minutes) at different phases, so phase is tested; one campaign targets a single
  article, so a one-article cycle counts.
* **Resemblance points at the decoy.** By composite profile, the quarter's most-flagged article most resembles the single-campaign verified
  days.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The council's reporting standard: a campaign is one coordinated operation, whatever the number of articles it targets; a
  campaign counts in the quarter if it inflated any rail candidate in it. The pageview guide: minute counts are exact and complete.
* **Empirical pins.** The cycle structure and the burst threshold, from the subsample.
* **Voices.** The integrity lead: "Every article that breaks the composite is its own operation until proven otherwise." The team's data
  scientist: "Bots run on timers; one timer per article is plenty."
* **Licensed wrong basis.** The standard records that enforcement's triage desk logs one case per flagged article and will read the referral
  on that basis.

## 8. Determinism by construction

* **Bursts.** Every burst exceeds the minute's smooth baseline by at least 40 views and genuine minute noise never exceeds 12, so any burst
  threshold from 13 to 39 finds the same minutes.
* **Periods.** The nine periods are distinct whole minutes from 17 to 53, except the shared 29, and each repeats over 300 times, so the
  decomposition is unique.
* **Baseline.** A 60-minute rolling median or a same-hour-of-week median gives the same burst minutes.
* **Quarter.** All nine cycles fire in every week of Q3, so the activity rule cannot split them.

## 9. Prompt sketch and deliverables

> The Q3 integrity report goes to the trust and safety council on 15 October, and it has to say how many coordinated campaigns we are
> sending to enforcement, since they open one investigation each. Our integrity lead counts every article that breaks the composite as its
> own operation. Give me the number, with each campaign's burst period, in two sentences for the report, plus `campaign_count.xlsx` holding
> the sheets below, the chart `burst_cycles.svg`, and a short `council_brief.pptx`.

* `campaign_count.xlsx` — the cycle decomposition with every article's cycles, the impressions sheet (ask A), the reports sheet (ask B) and
  the subsample back-test (ask C).
* `burst_cycles.svg` — a minute-by-article raster of Q3's bursts coloured by cycle, the twelve mixed articles outlined, the twin days V-08 and
  V-33 shown as inset minute series, and the nine periods listed in the legend.
* `council_brief.pptx` — the committed count and why 47, 13 and 6 are not it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 content categories, Q3 rail impressions and click-through rate. *Device:* a rail
  that re-renders after an app refresh logs a second impression carrying a refresh flag, as the analytics guide documents. Counting every
  impression understates click-through in the four categories read most on mobile. The campaign build never reads the impression log.
* **Ask B (device-carried).** For each month of Q3, user reports of suspicious trending items and the share actioned. *Device:* a report
  against an item already actioned is auto-closed with a "duplicate of action" reference, per the reporting guide. Counting auto-closed
  reports as unactioned understates the share in every month.
* **Ask C (validity).** For each of the four rung constructions, the verified article-days it reproduces minute by minute out of 50, and its
  error on the subsample's daily totals.
* **Decoupling.** Clearing the cycle decomposition changes no figure in asks A or B.

## 11. Rubric arithmetic

12 categories × 2 (ask A) + 3 months × 2 (ask B) + 4 constructions × 2 (ask C) + the committed count, the twelve mixed articles and the nine
periods + 5 named chart parts + 3 files ≈ 57 criteria.

## 12. World-building constraints

* Nine cycles with periods from 17 to 53 minutes (two at 29, different phases); twelve articles on two lists; 47 articles flagged.
* Rung figures are 47 / 13 / 6 / 9; period-only matching gives 7 and per-article counts without union 31.
* Single-period fits reproduce every verified day's total within 1% and no minute on the twelve mixed days.
* The subsample holds 50 days from Q1 and Q2, 12 with two campaigns, and none of its campaigns fired after mid-June; V-08 and V-33 are
  identical on every composite column.
* Refresh impressions and auto-closed reports never touch the minute view counts.
