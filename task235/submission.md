# task235 submission

## Tags

**Domain:** Product Analytics (metric definition and measurement science: a mobile game's purchase tracking, the analytics SDK's client events reconciled against the store-verified purchases build by build).
**Analytical objective:** Data Quality Monitoring & Alerting (which production builds of Kittiwake Cove get a purchase-tracking alert in the KC-DQ-04 run of Monday 9 November 2026).

## 1. Final Recommendation

**Alert Android 7.41.0 and iOS 7.42.0 in the run of Monday 9 November, and no other build.**

Judged against the next session of the phone that made each purchase, Android 7.41.0 loses 6.34 per cent of its purchase events with none still on a phone, and iOS 7.42.0 at least 3.10 per cent even if every event still on a phone arrives. Not Android 7.38.1 and iOS 7.38.2, 7.39.1 and 7.40.0, which a seven-day settle window alerts: their missing events sit on phones that have not opened the game since, and each would cross the line only if 33 per cent or more of those were lost, where of its events still on a phone when the game next opened at most 2 per cent never arrived. Not Android 7.42.0, which short windows and same-age comparisons alert: its new uploads leave events on the phone until the game next starts, and all 62 of its events still on a phone when the game next opened have arrived. Not the account's next session, which alerts iOS 7.38.2, 7.39.1 and 7.40.0, whose players open the game on another device while the one that bought still holds the event.

## 2. Critical Components

1. Android 7.41.0: **157** of its **2,477** purchases have a missing event though their phone has opened the game since, and none is still open: tracking loss **6.34** per cent
2. iOS 7.42.0: **10** such purchases of **323**, and **8** whose event is still on a phone that has not opened the game since: tracking loss at least **3.10** per cent, **5.57** if none of those arrives
3. No other build has more than **0.55** per cent of its purchases missing an event after their phone opened the game again (iOS 7.41.0, 8 of 1,447, none open)

## 3. Step-by-Step Solution

1. Took the purchases under KC-DQ-04 section 2 from purchase_service_validations_2026-10-05_to_2026-11-09.csv (transaction kind purchase, Production, standard, the Irish date of purchased_at from 12 October to 8 November) with their builds from build_register.xlsx: 15,705 purchases.
2. Matched each to its purchase_completed event in warehouse_purchase_completed_2026-10-05_to_2026-11-09.csv by store transaction id, the warehouse's several rows for one transaction being one event (section 3): 15,204 matched, 501 missing at the run.
3. Found each purchase's next session start of the same device in session_service_starts_2026-10-05_to_2026-11-09.csv; as the SDK uploads its queue when the game starts (tern_sdk_changelog.md, 4.6.0), a missing event whose phone has opened the game since will never arrive: 204 lost, 297 still on phones that have not opened the game since (section 4).
4. Android 7.41.0 has none open: 157 of 2,477 lost, 6.34 per cent, above the 2 per cent line (section 5); iOS 7.42.0 has 10 lost and 8 open of 323, 3.10 per cent even if all 8 arrive.
5. Every other build has at most 0.55 per cent lost (iOS 7.41.0) and crosses the line only if far more of its open purchases were lost than of its events still on a phone when the game next opened (at most 2 per cent of those never arrived on the old builds, none on Android 7.42.0): no alert.
6. Charted each build's tracking loss against the 2 per cent line, its open purchases counted lost at the share of its events still on a phone when the game next opened that never arrived.
7. Counted paying players (section 6) with accounts joined through account_service_links_2026-10-05_to_2026-11-09.csv, followed through any chain, and each guest account joined to the account its phone shows next, by time, across the validations and session_service_starts_2026-10-05_to_2026-11-09.csv, when that account is not a guest (section 6: the links are no register of every account): from 275 (iOS 7.42.0) to 1,538 (Android 7.41.3).
8. Converted each purchase's price_minor at its currency's minor unit (none for JPY and KRW) at the ECB rate in force on its Irish date in ecb_euro_reference_rates_2026-09-28_to_2026-11-06.csv, rounded to the cent line by line, and divided each build's total by its paying players (section 6): from 5.58 euro (iOS 7.42.0) to 11.73 (iOS 7.41.1) per paying player.

## 4. Deliverable Answers

### tracking_loss_alerts_2026-11-09.csv

1. One row per build in the file's order, gross bookings per paying player in euro to the cent:
   - iOS 7.38.2, build 4417: no alert, 377 paying players, gross bookings per paying player 9.93
   - iOS 7.39.1, build 4521: no alert, 294 paying players, gross bookings per paying player 10.39
   - iOS 7.40.0, build 4588: no alert, 855 paying players, gross bookings per paying player 8.23
   - iOS 7.41.0, build 4652: no alert, 890 paying players, gross bookings per paying player 8.08
   - iOS 7.41.1, build 4671: no alert, 1,362 paying players, gross bookings per paying player 11.73
   - iOS 7.42.0, build 4730: alert, 275 paying players, gross bookings per paying player 5.58
   - Android 7.38.1, build 7380100: no alert, 386 paying players, gross bookings per paying player 9.86
   - Android 7.39.0, build 7390000: no alert, 293 paying players, gross bookings per paying player 9.82
   - Android 7.40.2, build 7400200: no alert, 669 paying players, gross bookings per paying player 7.03
   - Android 7.41.0, build 7410000: alert, 1,392 paying players, gross bookings per paying player 8.99
   - Android 7.41.3, build 7410300: no alert, 1,538 paying players, gross bookings per paying player 9.91
   - Android 7.42.0, build 7420000: no alert, 320 paying players, gross bookings per paying player 5.58

### tracking_loss_by_build_2026-11-09.png

2. Horizontal bar chart of the twelve builds' tracking loss against the 2 per cent alert line, grouped by platform: Android 7.41.0 and iOS 7.42.0 in red above the line, every other bar below it.
