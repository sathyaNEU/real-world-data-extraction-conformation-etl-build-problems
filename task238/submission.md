# task238 submission

## Tags

**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement-error adjustment: the mode-mix monitor of a household wellbeing tracker moving to web-first collection, set from each headline index's mode effect read through a randomized contact strategy test).
**Analytical objective:** Data Quality Monitoring & Alerting (how far a quarter's web share may move before the tracker's published indexes are recalibrated).

## 1. Final Recommendation

**Run the Halvreth Wellbeing Tracker's mode-mix monitor at a band of 4 percentage points of web share from the fourth quarter of 2027.**

Heavy drinking binds: its mode effect, read through the CST-27 letters' random allocation, is more than 6 and at most 7.5 percentage points, which keeps a 4-point departure of the web share within its 0.30-point tolerance and takes a 5-point departure outside it; volunteering is next at 6 to under 7 points. Not 3 points, the band a comparison of web with telephone completes gives even with every recorded characteristic held fixed: households chose their mode on traits the questions also measure, so that comparison counts who answered online as an effect of answering online. Not 6 points, the band the letters' raw difference gives: it carries each index's mode effect only for the households a letter moved online.

## 2. Critical Components

1. Heavy drinking's mode effect, read through the letters, is **more than 6 and at most 7.5 percentage points**, so its widest band within tolerance is **4 to under 5 points**, the narrowest of the twelve indexes.
2. Volunteering is next, with a widest band of **6 to under 7 points**; every other index allows **8 points or more**.

## 3. Step-by-Step Solution

1. Built the test's completes from mwt_cst27_web_returns.csv and mwt_cst27_cati_interviews.csv under the CST-27 plan's section 5 (mwt_cst27_plan.pdf): web returns reaching section 6 by 23:59 Halvreth time on the quarter's last day (UTC+13 on 30 September), telephone interviews coded C, an address once at its first-submitted complete with the CATI clock read as Halvreth time, returns giving an age under 18 left out as not from the person the letters ask for, and the staff-entry returns of 9 to 12 August taken as the telephone interviews mwt_cst27_close_out.docx describes: 40,821 completes.
2. Joined each complete to its letter in mwt_cst27_issued_addresses.csv and scored the twelve headline indexes on valid answers as mwt_questionnaire_codebook_v9.xlsx (sheet Indexes) sets out.
3. Read each index's mode effect through the random letter allocation: its difference between the letter A and letter B completes divided by the letters' difference in the share of completes made online (two-stage least squares with the letter as the instrument sets the same band); heavy drinking's is more than 6 and at most 7.5 percentage points.
4. Divided each index's continuity tolerance (mso_ms14_tracker_continuity_standard.pdf, Table 2) by its mode effect: heavy drinking's widest band is 4 to under 5 points, volunteering's 6 to under 7 points, every other index's 8 points or more.
5. Took the widest whole-point band within every tolerance (MS-14 section 5): 4 points.
6. Took each letter's completes in each quarter over its eligible addresses (issued, less outcome codes 4.1 to 4.3, an address with a complete counted eligible whatever its code): response rates from 56.3 to 57.3 per cent.
7. Counted each index's completes giving its question a valid answer, online and by telephone.
8. Filed the band, the response rates and the valid answers in the workbook and charted each index's widest band against the band.

## 4. Deliverable Answers

### mwt_mode_mix_band_2027q4.xlsx

1. The band: 4 percentage points of web share, heavy drinking binding.
2. Response rate under each letter in each quarter, one decimal place:
   - second quarter 2027, letter A: 57.3 per cent
   - second quarter 2027, letter B: 56.4 per cent
   - third quarter 2027, letter A: 56.3 per cent
   - third quarter 2027, letter B: 56.8 per cent
3. Completes giving each index's question a valid answer, online and by telephone:
   - Life satisfaction (LS): 21,463 online, 19,144 by telephone
   - Worthwhile (WW): 21,434 online, 19,117 by telephone
   - Happiness yesterday (HY): 21,469 online, 19,171 by telephone
   - Anxiety yesterday (AX): 21,414 online, 19,120 by telephone
   - Loneliness (LN): 21,375 online, 19,109 by telephone
   - Trust in others (TR): 21,327 online, 18,823 by telephone
   - Safe after dark (SF): 21,349 online, 19,126 by telephone
   - Good health (GH): 21,445 online, 19,167 by telephone
   - Smoking (SM): 21,177 online, 19,165 by telephone
   - Heavy drinking (BD): 20,800 online, 18,980 by telephone
   - Volunteering (VL): 21,381 online, 19,188 by telephone
   - Financial strain (FS): 20,753 online, 18,830 by telephone

### mwt_mode_mix_band_2027q4.png

4. Each index's widest band within its continuity tolerance against the 4-point band, heavy drinking marked as binding.
