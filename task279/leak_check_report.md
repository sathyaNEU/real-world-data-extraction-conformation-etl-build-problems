# leak check, task279

**Verdict: REVIEW.** 16 files read, 41 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: material, inventory, subsidence, density, levels, method, oxidation, medium, drained, balance, points, decisive, surveyed, distribution, organic, repeat, register, component, compression, cannot, cumulative, slices, ranked, decision, measured

## 3 answer figures in the pack (REVIEW 16)
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 126 appears: ...7-0412-0071 VM-OL-1 28-02-1997 50 - 55 0,126 79,9 40,6 97-0412-0072 VM-OL-1 28-02-...
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 144 appears: ...7-0412-0264 VM-HW-2 17-03-1997 15 - 20 0,144 65,3 34,3 97-0412-0265 VM-HW-2 17-03-...
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 133 appears: ...7-0412-0033 VM-WK-2 26-02-1997 60 - 65 0,133 85,3 43,3 97-0412-0034 VM-WK-2 26-02-...
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 115 appears: ...7-0412-0037 VM-WK-2 26-02-1997 80 - 85 0,115 88,2 44,0 97-0412-0038 VM-WK-2 26-02-...
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 118 appears: ...7-0412-0078 VM-OL-1 28-02-1997 85 - 90 0,118 81,9 42,6 97-0412-0079 VM-OL-1 28-02-...
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 137 appears: ...7-0412-0008 VM-WK-1 26-02-1997 35 - 40 0,137 79,6 41,3 97-0412-0009 VM-WK-1 26-02-...
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 122 appears: ...7-0412-0098 VM-OL-2 28-02-1997 85 - 90 0,122 79,7 40,9 97-0412-0099 VM-OL-2 28-02-...
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 140 appears: ...7-0412-0069 VM-OL-1 28-02-1997 40 - 45 0,140 79,8 40,4 97-0412-0070 VM-OL-1 28-02-...
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 107 appears: ...7-0412-0018 VM-WK-1 26-02-1997 85 - 90 0,107 87,8 44,5 97-0412-0019 VM-WK-1 26-02-...
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 129 appears: ...7-0412-0096 VM-OL-2 28-02-1997 75 - 80 0,129 77,9 39,1 97-0412-0097 VM-OL-2 28-02-...
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 111 appears: ...7-0412-0039 VM-WK-2 26-02-1997 90 - 95 0,111 89,4 44,3 97-0412-0040 VM-WK-2 26-02-...
- **REVIEW** `veenkernen_1997_bodemlab_wageveld.txt`: golden figure 104 appears: ...7-0412-0129 VM-RL-1 06-03-1997 40 - 45 0,104 81,2 40,6 97-0412-0130 VM-RL-1 06-03-...
- **REVIEW** `veenmonitoring_protocol_2024.pdf`: golden figure 3.1 appears: ...7 and current code and both positions. 3. Coring 3.1 1997: one core a point to 1.00 m below the surfa...
- **REVIEW** `veenmonitoring_protocol_2024.pdf`: golden figure 4.1 appears: ...levelled on the day it is cored. 4. Laboratory 4.1 Each slice is analysed for dry bulk density (dri...
- **REVIEW** `veenmonitoring_protocol_2024.pdf`: golden figure 5.1 appears: ...heme in the year of analysis. 5. The carbon loss 5.1 A monitoring point's carbon loss is the carbon t...
- **REVIEW** `veenmonitoring_protocol_2024.pdf`: golden figure 6.2 appears: ...e other units follow in the order's later phases. 6.2 The order states for every unit its carbon loss...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `data_dictionary.txt`: 6 of 25 stump-paragraph terms appear (material, density, levels, method, repeat, register); read whether the document names the move
- **REVIEW** `hoogteonderzoek_lageveen_2024.pdf`: 6 of 25 stump-paragraph terms appear (levels, method, points, surveyed, repeat, register); read whether the document names the move
- **REVIEW** `veenmonitoring_protocol_2024.pdf`: 9 of 25 stump-paragraph terms appear (density, levels, method, drained, points, surveyed); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Two isolated scored readers (Sonnet, medium effort), each on its own fresh copy of prompt.txt and target/ unzipped from target.zip 977c37cc967376daafbd2eabfe28b6b6, 2026-10-24. Scored with score_reader.py --call-key call.first_raise.

**Reader A.** Call: Bovenmade, Zuidergeer, Ravenbroek (hit). Ask figures 35 of 48: every carbon loss but one (Oudelaak 3.0 against 3.1), every first-raise flag, every GLG; no surface lowering (it averaged every grid point levelled in both surveys, 413 of 441).
1. Decisive step: protocol 5.1, "the carbon that the peat which formed the top 1.00 m of the point's 1997 core has lost", with 3.2 and the two core lengths; "nothing states the method for locating that depth".
2. Ranking file: none. 3. Helper file: none. 4. Answer figure: none.
5. Literal sentence: 5.1 and 5.2 fix population, window, unit and mean, not how to find the peat in 2024; its own result with ash conservation is the golden three, the fixed-level reading gives Ruigeland, Hazelweer, Wedderkamp.
6. An analytical choice: identifying the same 1997 peat in the 2024 core (ash conservation against the surveyed lowering).
Sweep lines: all five harmless.

**Reader B.** Call: Bovenmade, Zuidergeer, Ravenbroek (hit). Ask figures 36 of 48: every carbon loss, every flag, every GLG; no surface lowering (the same 413 points).
1. Decisive step: protocol 5.1, the same sentence; the ash match inferred from 3.1 and 3.2.
2. Ranking file: none. 3. Helper files: the dictionary, the README and the point register (as maps, not answers). 4. Answer figure: none.
5. Literal sentence: 5.1 and 5.2; result the golden three; the method is not named.
6. An analytical choice: identifying the same peat in a thinner, compacted 2024 core; "the naive top-1-m comparison gives a wrong or negative answer".
Sweep lines: all five harmless.

**Verdict.** Gate F failed: both readers landed the call by the decisive step itself (the ash as the conserved component), from the estimand's own wording and the laboratories' loss on ignition, with no leak in any file. Ask B's renewed tube heights were read off the maintenance log by both (12 of 12 each): the device was on their path. Ask A's re-shot grid points held (0 of 12 each). Architecture 1 is spent.
