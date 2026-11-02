## Tags

**Domain:** Product Analytics (metric definition and measurement science).  
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**The scorecard service should hold experiments on the gap-sessions check from January 2027, at a hold line of 0.28 percentage points for a standard experiment.**

Tested at the install, the unit the platform assigns to arms, gap sessions would have held 10 of the 18 experiments of 2026 with a confirmed data incident and 0 of the 64 without one. Not late sessions, which holds 5 and leads only when every session is treated as an independent draw, a test that understates the variance of the gap-session share and pushes that check over the allowance. Not duplicate sessions or the treatment share, 3 each. Not events per install, which would have held 3 experiments without an incident against an allowance of 1.

## 2. Critical Components

1. Gap sessions would have held **10** of the 18 experiments with a confirmed data incident and **0** of the 64 without one.
2. Late sessions, the next best check within the allowance, would have held **5** of 18.
3. Events per install would have held **3** experiments without a confirmed incident, over the allowance of **1** in 64.
4. The hold line for a standard experiment (10,000 installs in each arm, 14 days) is **0.28** percentage points.

## 3. Step-by-Step Solution

1. Labelled the 82 experiments of 2026 from the incident register's confirmed experiment entries, matched to the registry by title: 18 with a confirmed data incident, 64 without one (withdrawn suspicions count as none).
2. Stacked install_summary_2026q1.csv, install_summary_2026q2.parquet and install_summary_2026q3.parquet, mapping service 1's columns and its arms A (control) and B (treatment) onto service 2's.
3. Compared each experiment's arms on its full run at the two-sided 1 per cent level in each check's hold direction (DH-3 section 4): each session share with its variance taken over installs, the unit DH-3 section 2 assigns to arms (delta method on per-install sums of the check's sessions and all sessions); events per install with Welch's t test; the treatment share against the registry's design share.
4. Counted each check's holds over the 82 experiments: gap sessions 10 and 0, late sessions 5 and 0, duplicate sessions 3 and 0, treatment share 3 and 0, events per install 0 and 3 (with a confirmed incident and without one).
5. Applied DH-3 section 5: at most 2 per cent of 64, so at most 1, rules out events per install; of the rest, gap sessions holds the most experiments with a confirmed incident.
6. Took the per-install variance of the gap-session share over both arms of the 64 experiments without an incident and set the line at 2.576 standard errors of the difference for 10,000 installs an arm: 0.28 percentage points.
7. SDK 9.4.1 installs: from collector_client_summary_2026-08.parquet took the iOS and Android client IDs with a 9.4.1 batch on a day from 3 to 6 August, joined each client ID first seen on 9.4.2 to the earlier client ID whose last sequence number it continues by one (the update issued it a new client ID), and counted, at each day's end, Copenhagen time, the installs with no 9.4.2 batch yet.

## 4. Deliverable Answers

### auto_hold_check_scorecard_2027.xlsx

1. The check and its line: Gap sessions, hold line 0.28 percentage points for a standard experiment.
2. Experiments with a confirmed data incident each check would have held, of 18:
   - Gap sessions: 10
   - Duplicate sessions: 3
   - Late sessions: 5
   - Events per install: 0
   - Treatment share: 3
3. Installs that sent events from SDK 9.4.1 from 3 to 6 August still on it at the end of each day, Copenhagen time (iOS; Android):
   - 6 August: 39,523; 32,798
   - 7 August: 36,149; 28,101
   - 8 August: 32,148; 22,422
   - 9 August: 27,664; 16,246
   - 10 August: 22,967; 9,821
   - 11 August: 18,207; 6,318
   - 12 August: 13,146; 4,314
   - 13 August: 8,216; 3,049
   - 14 August: 5,436; 2,268
   - 15 August: 3,777; 1,715
   - 16 August: 2,727; 1,363
   - 17 August: 2,047; 1,093
   - 18 August: 1,571; 905
   - 19 August: 1,232; 731
