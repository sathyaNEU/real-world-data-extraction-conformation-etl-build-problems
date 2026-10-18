## Tags

**Domain:** Energy systems and utilities (grid reliability and outage analysis).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**The remediation slot goes to the fused medium-voltage spurs, SN-odgalezienie, in rejon Borowa Puszcza
of the Grabownik branch, which carry 7,152 customer-interruptions in that rejon.**
Zanowiec leads on the interrupted customer-hours the dispatch record states and loses because 95 per
cent of its interruptions are timed by a line device while only 9 per cent of Grabownik's are. Pustrzyca
leads once one pooled pre-notification interval of 101.8 minutes is added to every untimed interruption,
and loses because the station sections carrying its untimed interruptions stand at 17.0 minutes.
Nierzyca leads on the pack as it stands and loses to procedure PR-07 section 3, which excludes planned
switching.

## 2. Critical Components

1. Unplanned interruptions in the window with a recorded restoration: **6,005**, of which **1,065** were
   timed by a line device and **4,940** only from the first customer notification
2. Mean interval from loss of supply to the first customer notification, measured on the interruptions a
   device timed: **8.6 minutes** on SN-magistrala, **17.0** on SN/nN-stacja, **164.6** on nN-obwod and
   **242.5** on SN-odgalezienie
3. Interrupted customer-hours by branch on that basis: Grabownik **270.8 thousand**, Zanowiec **206.9**,
   Pustrzyca **182.5**, Nierzyca **148.7**
4. Grabownik's lead over Zanowiec at level one: **1.31x**

## 3. Step-by-Step Solution

1. Concatenated the two dispatch exports and kept one row per interruption id, the seven-day overlap
   between them counted once: 7,423 export rows reduce to 6,448 interruptions.
2. Normalised the device identifier to the register's zero-padded form, which the data dictionary states
   arrived with the 2024 upgrade, and joined rejestr_urzadzen_sn_nn.xlsx for the customers behind the
   device that operated, its branch, its rejon and its section class; the raw string join drops 2,823
   export rows.
3. Applied PR-07 section 3: unplanned only, restoration recorded on or before the extract, start inside
   the window, leaving 6,005 interruptions.
4. Split those by whether a line device timed them, using the register's telemetry flag and the station
   breakers on SN-magistrala, and converted telemetria_operacje_lacznikow_utc.csv from UTC to local
   time: 1,065 timed, 4,940 timed only from the first customer notification.
5. On the 1,065 timed interruptions, took the interval between the device operation and the first
   notification in zgloszenia_klientow_2026.csv, by section class: 8.6, 17.0, 164.6 and 242.5 minutes.
6. Added that class interval to each untimed interruption's span and recomputed interrupted
   customer-hours: Grabownik 270.8 thousand against Zanowiec 206.9, Pustrzyca 182.5 and Nierzyca 148.7.
7. Walked PR-07 section 4 on those hours: Grabownik, then rejon Borowa Puszcza, then SN-odgalezienie.
8. The slot goes to the SN-odgalezienie spurs of rejon Borowa Puszcza in Grabownik, carrying 7,152
   customer-interruptions in that rejon.

## 4. Deliverable Answers

### plan_remediacji_2026.docx

1. Branch: **Grabownik (GRB)**. Rejon: **Borowa Puszcza**. Section class: **SN-odgalezienie**.
2. Customer-interruptions the named class carries in its rejon: **7,152**
3. Runner-up branch: **Zanowiec (ZAN)**
4. Level one, every branch, unplanned interruptions and customer-interruptions:
   - Grabownik: 4,694 interruptions, 53,268 customer-interruptions
   - Zanowiec: 301 interruptions, 224,017 customer-interruptions
   - Pustrzyca: 560 interruptions, 139,433 customer-interruptions
   - Nierzyca: 450 interruptions, 125,948 customer-interruptions
5. Level two, every rejon of Grabownik:
   - Borowa Puszcza: 1,136 interruptions, 11,148 customer-interruptions
   - Mokrzyce: 1,846 interruptions, 18,690 customer-interruptions
   - Zalesie Stare: 1,066 interruptions, 11,435 customer-interruptions
   - Grabownik: 646 interruptions, 11,995 customer-interruptions
6. Level three, every section class of rejon Borowa Puszcza:
   - SN-odgalezienie: 926 interruptions, 7,152 customer-interruptions
   - nN-obwod: 201 interruptions, 2,551 customer-interruptions
   - SN/nN-stacja: 7 interruptions, 387 customer-interruptions
   - SN-magistrala: 2 interruptions, 1,058 customer-interruptions
7. Planned jobs in the window that ran past their published window: **85**, by **58.0 hours** in total
8. Customer-hours those jobs account for, per branch:
   - Zanowiec: 6,669.0
   - Pustrzyca: 11,465.3
   - Grabownik: 2,251.1
   - Nierzyca: 15,275.2
9. Notifications matching no interruption record, by branch and channel:
   - Zanowiec: telefon 432, IVR 381, aplikacja 409
   - Pustrzyca: telefon 268, IVR 222, aplikacja 261
   - Grabownik: telefon 261, IVR 212, aplikacja 294
   - Nierzyca: telefon 249, IVR 180, aplikacja 231
   - Total: 3,400
10. Customers behind the devices those notifications name, per branch:
   - Zanowiec: 216,840
   - Pustrzyca: 99,527
   - Grabownik: 30,657
   - Nierzyca: 53,061
11. October 2026 correction to reported unplanned interruption minutes: SN **+0.6 minutes**, **+15.7 per
    cent**; nN **+0.3 minutes**, **+11.0 per cent**

### drzewo_udzialow_2026.png

12. Three-level tree, one box per branch at level one, per rejon of Grabownik at level two and per
    section class of rejon Borowa Puszcza at level three, each box carrying its customer-interruptions,
    with the path Grabownik to Borowa Puszcza to SN-odgalezienie picked out and the slot stated beneath.
