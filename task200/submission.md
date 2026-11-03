## Tags

**Domain:** Human Factors & Ergonomics (safety incident and error analysis).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Run the 2027 remedial image interpretation course in the order Fell, Brook, Dene, Esk, Arden, Cleve, with Fell first.**
On the threat images its operators met for the first time in 2026 Fell found 63 per cent (707 of 1,125), against 69 per cent for Brook, the next lowest. Not Brook first on the overall projection score (71 per cent against Fell's 80), because most of Fell's Pier B projections were images its operators had already met. Not Esk first on d-prime against its clear searches, which measures how well a team separates threats from clutter, not how often it finds one.

## 2. Critical Components

1. Fell's operators found **63%** of the threat images they met for the first time in 2026 (707 of 1,125), the lowest of the teams.
2. **4,104 of Fell's 5,229** projections in 2026 showed an image its operators had already met, against about one in eight for the Central teams, and on those images Fell found **84%**.
3. On first meetings Brook is next at **69%**, then Dene 74%, Esk 77%, Arden 81% and Cleve 85%.

## 3. Step-by-Step Solution

1. Read ct_tip_events_2024.csv to ct_tip_events_2026.csv (each first-of-month repeat row dropped) and pierb_tip_log_2023-09_2026-12.csv, mapped every CT login and Pier B TIP operator to its staff number and team through screening_roster_2026-12-31.xlsx, and left out cancelled projections (SPS-04 section 3).
2. Put each screener's projections in time order from the start of each export and marked one a first meeting where that screener had not been shown that image before.
3. On 2026 projections each team's share found on first meetings is Fell 63%, Brook 69%, Dene 74%, Esk 77%, Arden 81%, Cleve 85%.
4. On all 2026 projections Brook finds 71% and Fell 80%, the gap being Fell's 4,104 projections of images already met, found 84% of the time.
5. Screen time: merged each CT login's overlapping rows in ct_workstation_sessions_2026.csv into one span, and ended each Pier B log-on in pierb_screen_events_2026.csv at the operator's own log-off, the next log-on at that screen or the screen's shutdown, whichever came first, each badge read to its holder on the day through id_centre_badge_register.csv.
6. Clear searches: split search_log_2026.csv records that carry two trays, matched each tray to its latest reject before the search was taken (ct_tray_rejects_2026.csv, or the Pier B REJECT events) and charged it to the screener logged on at that screen then.
7. Certificates: took each rostered screener's latest certification, from the passed IIC rows in the LMS export and from every certificate in assessment_centre_certificates.csv by candidate staff number on its assessment date (an EXT-IIC row in the LMS carries the date it was keyed, and the centre's list also holds certificates not yet keyed), and counted three-year expiries before 1 July 2027.
8. Ordered the teams from least to most likely to find a prohibited article (SPS-04 4.2): Fell, Brook, Dene, Esk, Arden, Cleve.

## 4. Deliverable Answers

### remedial_course_2027.xlsx

1. Course order:
   - 1. Fell
   - 2. Brook
   - 3. Dene
   - 4. Esk
   - 5. Arden
   - 6. Cleve
2. Screen time in 2026, hours:
   - Arden: 5,168.8
   - Brook: 4,750.9
   - Cleve: 5,545.6
   - Dene: 4,593.7
   - Esk: 5,297.1
   - Fell: 4,603.7
3. Clear searches in 2026:
   - Arden: 6,608
   - Brook: 4,399
   - Cleve: 6,737
   - Dene: 6,429
   - Esk: 11,915
   - Fell: 5,683
4. Screeners whose image interpretation certificate runs out before 1 July 2027:
   - Arden: 4
   - Brook: 2
   - Cleve: 3
   - Dene: 2
   - Esk: 5
   - Fell: 3

### remedial_course_2027_note.docx

1. One page giving the order with Fell first and Brook second, the first-meeting figures it rests on, and why the overall projection score and d-prime would put another team first.
