## Tags

**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution (a hydro licensee's bypassed-reach flow record rebuilt from its stage logger, station register, rating memo and the hydrographer's discharge measurements).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**The bypassed reach fell below its Article 403 minimum from 29 July to 13 September and from 21 September to 31 October 2026, 88 days with a shortfall of 600 acre-feet, and Tallis Creek Paper Company must report both periods.**
The 27 July storm shifted gauge BP-1's stage-discharge control: the four measurements after it sit 13.8 to 18.0 per cent below Rating 7 while the four before range from 1.6 per cent below to 2.2 per cent above it, so on the measured relation the reach carried 46.1 cfs in August and 27.0 cfs in October. Not the record on Rating 7, which keeps every day at or above its minimum (lowest July to September day 53.8 cfs) only because the plant's controller held the rated flow on its targets.

## 2. Critical Components

1. The four 2026 measurements after the 27 July storm sit **13.8 to 18.0 per cent** below Rating 7 at their gage heights; the four before range from **1.6 per cent below to 2.2 per cent above** it.
2. The measured correction after the storm is a stage shift of **about 0.10 ft (fitted -0.0990 ft, the mean of the four post-storm measurements' shifts)**, applied from the storm's peak at 23:40 PDT on 27 July; on it the reach carried **46.1 cfs** in August and **27.0 cfs** in October.
3. **88** deviation days: 3 in July, 31 in August, 23 in September and 31 in October.
4. The shortfall below the minimum is **600 acre-feet** (graded within 100 acre-feet).

## 3. Step-by-Step Solution

1. Read `gauge/bp1_stage_2026.csv` (gage height every ten minutes on Pacific Standard Time) and moved each reading one hour later to local daylight time.
2. Built Rating 7 from `gauge/bp1_station_register.xlsx` (the expanded table from 1.00 to 4.00 ft, interpolated) and, above 4.00 ft, the high-water segment in `gauge/bp1_rating7_report_2023.pdf` (Q = 319.4 + 260 (GH - 4.00)^1.60).
3. Set each measurement in `gauge/bp1_field_visits_2026.csv` against Rating 7 at its mean gage height: the four after the storm sit 13.8 to 18.0 per cent below, stage shifts of -0.0971 to -0.1006 ft with a mean of -0.0990 ft (about 0.10 ft); the four before range from 1.6 per cent below to 2.2 per cent above, inside the rating's own scatter, and take no correction.
4. Converted every reading on Rating 7 up to the storm's peak in the stage record (22:40 PST, 23:40 PDT on 27 July) and on Rating 7 at the gage height plus the -0.0990 ft shift after it (the shift runs from the storm, since the 26 July measurement still sits on the rating), and averaged the flows by local calendar day.
5. Compared each day with Article 403's minimum (`license/license_order_excerpt_2019.pdf`, 50 cfs July to September and 30 cfs otherwise): 88 days below, in two runs, 29 July to 13 September and 21 September to 31 October, the fall pulse holding the reach above 50 cfs between them.
6. Summed each deviation day's deficit below its minimum at 1.98347 acre-feet per cfs-day: 600 acre-feet.
7. Summed the May and June daily means for Article 404: 18,800 and 9,000 acre-feet; the spring peak 10-minute flow was 575 cfs at 27 May 2026 20:30 PDT.

## 4. Deliverable Answers

### bypass_flow_record_2026.xlsx

1. 123 rows, 1 July to 31 October 2026, each local day's mean flow in whole cfs and whether it met the minimum; each daily mean is graded within 2 cfs of the value below with the shift running from the storm's peak, and 27, 28 and 29 July (the storm's two days and the day of the first measurement after it, whose means turn on the hour the correction starts) on met only:
   - 1 July: 54 cfs, met
   - 2 July: 54 cfs, met
   - 3 July: 54 cfs, met
   - 4 July: 54 cfs, met
   - 5 July: 54 cfs, met
   - 6 July: 54 cfs, met
   - 7 July: 54 cfs, met
   - 8 July: 54 cfs, met
   - 9 July: 54 cfs, met
   - 10 July: 54 cfs, met
   - 11 July: 54 cfs, met
   - 12 July: 54 cfs, met
   - 13 July: 54 cfs, met
   - 14 July: 54 cfs, met
   - 15 July: 54 cfs, met
   - 16 July: 54 cfs, met
   - 17 July: 54 cfs, met
   - 18 July: 54 cfs, met
   - 19 July: 54 cfs, met
   - 20 July: 54 cfs, met
   - 21 July: 54 cfs, met
   - 22 July: 54 cfs, met
   - 23 July: 54 cfs, met
   - 24 July: 54 cfs, met
   - 25 July: 54 cfs, met
   - 26 July: 54 cfs, met
   - 27 July: met (142 cfs)
   - 28 July: met (277 cfs)
   - 29 July: below (46 cfs)
   - 30 July: 46 cfs, below
   - 31 July: 46 cfs, below
   - 1 August: 46 cfs, below
   - 2 August: 46 cfs, below
   - 3 August: 46 cfs, below
   - 4 August: 46 cfs, below
   - 5 August: 46 cfs, below
   - 6 August: 46 cfs, below
   - 7 August: 46 cfs, below
   - 8 August: 46 cfs, below
   - 9 August: 46 cfs, below
   - 10 August: 46 cfs, below
   - 11 August: 46 cfs, below
   - 12 August: 46 cfs, below
   - 13 August: 46 cfs, below
   - 14 August: 46 cfs, below
   - 15 August: 46 cfs, below
   - 16 August: 46 cfs, below
   - 17 August: 46 cfs, below
   - 18 August: 46 cfs, below
   - 19 August: 46 cfs, below
   - 20 August: 46 cfs, below
   - 21 August: 46 cfs, below
   - 22 August: 46 cfs, below
   - 23 August: 46 cfs, below
   - 24 August: 46 cfs, below
   - 25 August: 46 cfs, below
   - 26 August: 46 cfs, below
   - 27 August: 46 cfs, below
   - 28 August: 46 cfs, below
   - 29 August: 46 cfs, below
   - 30 August: 46 cfs, below
   - 31 August: 46 cfs, below
   - 1 September: 46 cfs, below
   - 2 September: 46 cfs, below
   - 3 September: 46 cfs, below
   - 4 September: 46 cfs, below
   - 5 September: 46 cfs, below
   - 6 September: 46 cfs, below
   - 7 September: 46 cfs, below
   - 8 September: 46 cfs, below
   - 9 September: 46 cfs, below
   - 10 September: 46 cfs, below
   - 11 September: 46 cfs, below
   - 12 September: 46 cfs, below
   - 13 September: 46 cfs, below
   - 14 September: 55 cfs, met
   - 15 September: 55 cfs, met
   - 16 September: 55 cfs, met
   - 17 September: 55 cfs, met
   - 18 September: 55 cfs, met
   - 19 September: 55 cfs, met
   - 20 September: 55 cfs, met
   - 21 September: 46 cfs, below
   - 22 September: 46 cfs, below
   - 23 September: 46 cfs, below
   - 24 September: 46 cfs, below
   - 25 September: 46 cfs, below
   - 26 September: 46 cfs, below
   - 27 September: 46 cfs, below
   - 28 September: 46 cfs, below
   - 29 September: 46 cfs, below
   - 30 September: 46 cfs, below
   - 1 October: 27 cfs, below
   - 2 October: 27 cfs, below
   - 3 October: 27 cfs, below
   - 4 October: 27 cfs, below
   - 5 October: 27 cfs, below
   - 6 October: 27 cfs, below
   - 7 October: 27 cfs, below
   - 8 October: 27 cfs, below
   - 9 October: 27 cfs, below
   - 10 October: 27 cfs, below
   - 11 October: 27 cfs, below
   - 12 October: 27 cfs, below
   - 13 October: 27 cfs, below
   - 14 October: 27 cfs, below
   - 15 October: 27 cfs, below
   - 16 October: 27 cfs, below
   - 17 October: 27 cfs, below
   - 18 October: 27 cfs, below
   - 19 October: 27 cfs, below
   - 20 October: 27 cfs, below
   - 21 October: 27 cfs, below
   - 22 October: 27 cfs, below
   - 23 October: 27 cfs, below
   - 24 October: 27 cfs, below
   - 25 October: 27 cfs, below
   - 26 October: 27 cfs, below
   - 27 October: 27 cfs, below
   - 28 October: 27 cfs, below
   - 29 October: 27 cfs, below
   - 30 October: 27 cfs, below
   - 31 October: 27 cfs, below

### minimum_flow_deviation_report_2026.docx

1. Deviation periods: 29 July to 13 September 2026 and 21 September to 31 October 2026, 88 days.
2. Cause: the 27 July storm shifted gauge BP-1's stage-discharge control, so Rating 7 overstated every later flow while the plant's controller held the rated setpoint: the four measurements after the storm sit 13.8 to 18.0 per cent below Rating 7 at the held stages.
3. Total shortfall below the minimum: 600 acre-feet (graded within 100 acre-feet).
4. Article 404: 18,800 acre-feet in May and 9,000 acre-feet in June 2026; spring peak flow 575 cfs at 27 May 2026 20:30 PDT.
