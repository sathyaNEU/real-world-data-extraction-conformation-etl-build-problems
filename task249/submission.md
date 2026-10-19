# task249 submission

## Tags

**Domain:** Product Analytics (metric definition and measurement science: a regional newspaper group's monthly unique browsers per local edition, counted by an analytics identifier that WebKit drops after seven days without a visit).
**Analytical objective:** Data Quality Monitoring & Alerting (which editions' published audience figure fails the 2029 policy's tolerance and carries the measurement note).

## 1. Final Recommendation

**Eight of the twelve editions carry the measurement note in the 2029 media kit: Rhenhagen Stadt, Kirchbrunn, Wiesbrück, Hollerfeld, Sonnweiler, Mühlenstedt, Grauheim and Lindenau; Altenhorst, Eichtal, Bergstetten and Falkenried print their figures without it.**

Each of the 8 reports more than 26 per cent above the browsers that read it in October to December 2028, the other four less than 23 per cent, against the policy's 25. Not the sign-in split (signed-in browsers from the register, signed-out identifiers on signed-out readers of other browsers), which leaves Grauheim, Lindenau, Sonnweiler and Wiesbrück under the line: the meter sits in the same capped storage, so on WebKit it restarts with the identifier and keeps weekly and occasional readers signed out who on other browsers met the wall and registered (signed-in WebKit devices carry fewer identifiers a month than the replay gives signed-in readers of other browsers, while print subscribers' WebKit devices carry as many as the replay gives their other browsers). Not the device-only replay, which drops Hollerfeld, Kirchbrunn and Mühlenstedt by pooling print subscribers, who read weekly on Apple devices. Not the signed-in identifiers per device, which are frequent readers' and drop Grauheim, Lindenau, Rhenhagen Stadt, Sonnweiler and Wiesbrück.

## 2. Critical Components

1. On other browsers an identifier is a browser; the seven-day rule replayed on their site-wide session histories, within edition, month and device class, gives the identifiers a WebKit browser carries.
2. Print subscribers are held apart and counted from the sign-in register: their access does not depend on the meter, and **61 per cent** of their signed-in devices are WebKit against **27 per cent** of other signed-in devices.
3. Every other reader is pooled whether signed in or not: registration is a consequence of the cap, so the comparison is matched only on what the cap cannot change.
4. The 8 noted editions overstate by more than **26 per cent**, the other four by less than **23 per cent**.

## 3. Step-by-Step Solution

1. Took the quarter's sessions from web_sessions_2028q4.parquet without is_bot rows, the newsroom's addresses and the re-sent duplicate rows, HKR read as HOL, months in Berlin time, and WebKit as every iOS browser and Safari on the Mac (analytics_tag_notes.pdf).
2. Reported figure: each edition's distinct client_ids per month averaged over October to December, the same as platform_users_by_month_2028.xlsx with HKR and HOL joined.
3. Print subscribers' browsers: client_ids in signin_device_register_2028q4.csv whose account's origin in reader_accounts.csv is print subscription, counted by device_id.
4. For each edition, month and device class: non-WebKit browsers as client_ids; WebKit print devices counted; WebKit non-print client_ids divided by the mean number of runs (a new run after more than seven days between one session's end and the next start, across all editions) that touch the edition and month among non-WebKit non-print client_ids; summed over device classes and averaged over the three months.
5. Overstatement: reported over estimated browsers less one; RHS, KBR, WBR, HOL, SOW, MST, GRH, LDN exceed 25 per cent (8 of 12).
6. Newsletter: status at 2028-12-31 23:00 UTC (midnight in Berlin) from newsletter_contacts_2029-01-15.csv with each contact's first status event after that moment in newsletter_activity_log.csv (a click is not a status event). Groups at that moment by undoing every change after it, newest first: the preference centre's changes in newsletter_group_changes.csv (the groups before) and the editions the newsletters' one-click links added, the clicked links to /newsletter/ausgabe-hinzufuegen in the activity log, which the preference centre's log does not hold (906 after midnight; the 458 clicked before it stand). Confirmed subscribers counted in each of their groups.
7. Sold copies: subscription numbers are issued in order as subscriptions are entered (DATA_DICTIONARY.md), so a start date later than that of a subscription numbered after it is not a first day of delivery: those 451 subscriptions, each shown starting between November and mid-December 2028 (the COMBI ones beside Digital Plus accesses that started years before), were delivered from before the quarter. Then for each publication day (Monday to Saturday less 3 October, 25 and 26 December, and 1 November in Rhineland-Palatinate) the DAILY and COMBI copies and SATURDAY copies on Saturdays, less pauses, plus e-paper accesses except the Digital Plus accesses (each the e-paper of a COMBI subscription, order_ref Kombi and its sub_no) and trials, plus delivered less returned single copies, averaged over the edition's publication days.
8. The 8 editions above carry the note in media_kit_2029_edition_figures.xlsx and measurement_note_2029.pdf.

## 4. Deliverable Answers

### media_kit_2029_edition_figures.xlsx and measurement_note_2029.pdf

1. Editions carrying the measurement note (8): RHS (Rhenhagen Stadt), KBR (Kirchbrunn), WBR (Wiesbrück), HOL (Hollerfeld), SOW (Sonnweiler), MST (Mühlenstedt), GRH (Grauheim), LDN (Lindenau).
2. Editions printed without the note (4): ALH (Altenhorst), EIT (Eichtal), BST (Bergstetten), FKR (Falkenried).
3. Average sold copies per publication day, fourth quarter 2028:
   - RHS: 7,288
   - KBR: 9,225
   - ALH: 3,154
   - WBR: 4,073
   - HOL: 5,044
   - SOW: 3,038
   - MST: 5,428
   - GRH: 2,328
   - EIT: 4,020
   - BST: 2,119
   - LDN: 2,616
   - FKR: 3,667
4. Newsletter subscribers at the end of 31 December 2028:
   - RHS: 3,434
   - KBR: 2,330
   - ALH: 1,233
   - WBR: 2,137
   - HOL: 1,467
   - SOW: 1,793
   - MST: 1,625
   - GRH: 1,220
   - EIT: 1,016
   - BST: 1,039
   - LDN: 1,582
   - FKR: 984
5. Chart on page 1 of measurement_note_2029.pdf: each edition's reported users against its estimated browsers, the 25 per cent line drawn and the noted editions marked.
