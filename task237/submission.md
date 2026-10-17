# task237 submission

## Tags

**Domain:** Psychology & Behavioral Science (psychometric measurement and scale validation: the release gate for a survey scale's new language versions, each judged on the share of its pilot score's variance due to the trait it measures).
**Analytical objective:** Data Quality Monitoring & Alerting (whether each translated version's pilot data measure connectedness reliably enough to field in wave 6).

## 1. Final Recommendation

**Release the Punjabi, Spanish and Persian versions of the BCS-12 for the wave 6 fieldwork, hold the Mandarin, Tagalog, Arabic and Korean versions for cognitive interviews and a second pilot, and send the Cantonese, Urdu and Vietnamese versions back for retranslation.**

In the Mandarin, Cantonese, Tagalog, Arabic, Vietnamese and Korean versions the six negatively worded items share a wording factor of their own, and with it separated the trait's share of the total score's variance is under 0.80 in all six and under 0.70 in the Cantonese and Vietnamese versions; the Urdu version is under 0.70 with no wording factor, and the Punjabi, Spanish and Persian versions are 0.80 or more. Not Cronbach's alpha, which at 0.85 to 0.87 would release the Mandarin, Tagalog, Arabic, Vietnamese and Korean versions and hold the Cantonese one, because it counts the wording factor's variance as connectedness. Not omega from a single factor, which files the same decisions. Not omega total from the model with the wording factor, which still counts that factor's variance. Not the positively worded items alone, which release the Mandarin, Tagalog and Vietnamese versions and hold the Punjabi one.

## 2. Critical Components

1. In the Mandarin, Cantonese, Tagalog, Arabic, Vietnamese and Korean versions the six negatively worded items share a **wording factor** besides connectedness; in the Punjabi, Spanish, Urdu and Persian versions they share none.
2. The trait's share of total-score variance with the wording factor separated: **0.80 or more** in the Punjabi, Spanish and Persian versions, **0.70 to under 0.80** in the Mandarin, Tagalog, Arabic and Korean versions, **under 0.70** in the Cantonese, Urdu and Vietnamese versions.

## 3. Step-by-Step Solution

1. Built each online version's valid completes from ncp_bcs12_pilot_export_wave6.csv under TAS-4 section 4 (translation_adaptation_standard_TAS-4.pdf): respondents 18 or older whose entry started within the version's pilot dates in bcs12_translation_register_wave6.xlsx in Eastern time, who reached the end of the BCS-12 module (no item blank, status complete or partial) still in the version, counted once per panel member at their first valid complete with the accounts ncp_incentive_ledger_bcs12_pilot.csv shows merged taken as one member: 3,253 valid completes across the six online versions.
2. Built each interviewer-administered version's valid completes from flr_bcs12_pilot_interviews_long.csv: interviews within the version's pilot dates that reached BCS12, less those flr_backcheck_log_bcs12_pilot.csv reports not confirmed for the interviewer whose interview was checked (a reissued case's later interview stays): 2,078 across the four versions.
3. Scored the items under section 5 (BCS02, BCS04, BCS06, BCS08, BCS10 and BCS12 reversed; 9, -8 and -9 unanswered; one or two unanswered items prorated) and took each version's mean total score, from 36.89 (Korean) to 41.76 (Punjabi).
4. Took the covariance of the twelve item scores over each version's valid completes who answered all twelve items (section 6), 395 to 557 respondents per version.
5. Fitted a single factor and a bifactor model (connectedness on all twelve items, a wording factor on the six negatively worded items) by maximum likelihood: the wording factor improves on the single factor in the Mandarin, Cantonese, Tagalog, Arabic, Vietnamese and Korean versions and adds nothing in the Punjabi, Spanish, Urdu and Persian versions.
6. Took the trait's share of the total score's variance from the bifactor model (omega hierarchical: connectedness's loadings summed and squared over the total score's model variance) and compared it unrounded with the bands at 0.80 and 0.70: Punjabi, Spanish and Persian at 0.80 or more, Mandarin, Tagalog, Arabic and Korean from 0.70 to under 0.80, Cantonese, Urdu and Vietnamese under 0.70.
7. Filed the decisions with each version's valid pilot completes and pilot mean score, and charted alpha and the trait's share for each version against the bands.

## 4. Deliverable Answers

### bcs12_wave6_release_decisions.csv

1. One row per version in the translation register's order, valid pilot completes whole, pilot mean score to two decimals:
   - Punjabi (pa): release, 542 valid pilot completes, pilot mean score 41.76
   - Chinese, Simplified (Mandarin) (zh-Hans): hold, 606 valid pilot completes, pilot mean score 39.18
   - Cantonese (yue): rework, 489 valid pilot completes, pilot mean score 38.29
   - Tagalog (tl): hold, 450 valid pilot completes, pilot mean score 38.36
   - Arabic (ar): hold, 569 valid pilot completes, pilot mean score 39.53
   - Spanish (es): release, 622 valid pilot completes, pilot mean score 41.47
   - Urdu (ur): rework, 478 valid pilot completes, pilot mean score 38.46
   - Vietnamese (vi): rework, 512 valid pilot completes, pilot mean score 39.04
   - Persian (Farsi) (fa): release, 490 valid pilot completes, pilot mean score 40.23
   - Korean (ko): hold, 573 valid pilot completes, pilot mean score 36.89

### bcs12_wave6_release_chart.png

2. Each version's reliability, the trait's share of its score variance, against the rework, hold and release bands at 0.70 and 0.80, coloured by decision.
