## Tags

**Domain:** Biomedical & Clinical Research, survival and time-to-event analysis (which of Brennick Valley Health's six hip constructs stay on its hip agreement from 1 July 2027, by each construct's cumulative percent revision ten years after the operation on the system's joint registry, estimated by Kaplan-Meier with the hips the registry entered after their operation counted at risk from the day it entered them).
**Analytical objective:** Descriptive & Distribution Analysis (how the time from operation to first revision is distributed for each construct's hips, cut at ten years).

## 1. Final Recommendation

**Keep Askvane/Quarvel, Holbrin/Pellvoro and Askvane/Pellvoro on the hip agreement renewed on 1 July 2027, and take Edvalt/Kelvarne, Edvalt/Pellvoro and Kalvoran/Morvenne off it.**
Askvane/Quarvel (3.7 per cent revised by ten years), Holbrin/Pellvoro (4.1) and Askvane/Pellvoro (3.5) meet the policy's 5.0 per cent bar; Edvalt/Kelvarne (7.0), Edvalt/Pellvoro (5.7) and Kalvoran/Morvenne (7.6) do not. Not five constructs with both Edvalt constructs kept at 3.1 and 3.2 per cent, which clocks every hip from its operation, because a hip replaced before 2018 is on the registry only if it was unrevised at its 2018 to 2021 enrolment visit, so its years before the visit enter the curve as revision-free. Not four with Edvalt/Pellvoro kept at 4.6, which starts those hips at the registry's start on 1 January 2018, because the registry entered each of them at its visit. Not all six, from the share of each construct's hips ever revised, which ignores how long each hip has been followed.

## 2. Critical Components

1. Edvalt/Kelvarne **7.0 per cent** and Edvalt/Pellvoro **5.7 per cent** revised by ten years, each hip replaced before 2018 at risk from its enrolment visit
2. Kalvoran/Morvenne **7.6 per cent**
3. Askvane/Quarvel **3.7 per cent**, Holbrin/Pellvoro **4.1 per cent** and Askvane/Pellvoro **3.5 per cent**

## 3. Step-by-Step Solution

1. Stacked bvjr_prospective_hips_2018-2026.csv and bvjr_legacy_enrolment_2018-2021.xlsx, one row per hip, and mapped each hip's stem and cup catalogue numbers to its construct through bvjr_component_crosswalk.xlsx, Thorvik's numbers from before 1 July 2020 included: every hip maps.
2. Took each hip's first revision from bvjr_revisions_to_2026-12-31.csv and ended its follow-up at the patient's death (death_index_linkage_2026-12-31.csv, a month-only date taken as the 15th), at the move out of Wisconsin (bvjr_followup_status_2026-12-31.csv) or at 31 December 2026, deaths and moves censored (Policy VA-07, 4.3).
3. Counted each hip at risk from the day the registry entered it: its operation for a hip captured from 2018, its Enrolled on visit for a hip replaced before 2018 (bvjr_data_dictionary.pdf), the clock running from the operation.
4. Estimated each construct's cumulative percent revision at ten years (3,652.5 days) by Kaplan-Meier on those risk sets: Edvalt/Kelvarne 7.0, Edvalt/Pellvoro 5.7, Kalvoran/Morvenne 7.6, Askvane/Quarvel 3.7, Holbrin/Pellvoro 4.1 and Askvane/Pellvoro 3.5 per cent.
5. Kept the constructs at 5.0 per cent or less (Policy VA-07, 4.2): Askvane/Quarvel, Holbrin/Pellvoro and Askvane/Pellvoro.
6. Counted the 2026 primary total hips in periop_implant_log_2026.csv as each side or_case_list_2026.xlsx says the case operated on with an implanted stem and shell (net of any explanted), mapped to its construct: 1,009 hips; implants recorded on the other side of a one-sided case are the patient's existing hip, not that day's operation.
7. Matched each of those hips to the prospective export's operations of 2026 on medical record number (the case's number or a number him_mrn_merges_2026.csv retired into it), side and operation date: 28 are not on the registry.

## 4. Deliverable Answers

### hip_construct_scorecard_2027.xlsx

1. Each construct's cumulative percent revision ten years after the operation, and whether it stays:
   - Edvalt/Kelvarne: 7.0 per cent, comes off
   - Edvalt/Pellvoro: 5.7 per cent, comes off
   - Askvane/Quarvel: 3.7 per cent, stays
   - Holbrin/Pellvoro: 4.1 per cent, stays
   - Askvane/Pellvoro: 3.5 per cent, stays
   - Kalvoran/Morvenne: 7.6 per cent, comes off
2. Primary total hips each construct went into in 2026 at Brennick Valley Medical Center, Tollefson Lake Hospital and Kittelstad Orthopaedic Hospital:
   - Edvalt/Kelvarne: 32, 29 and 14
   - Edvalt/Pellvoro: 18, 9 and 63
   - Askvane/Quarvel: 83, 48 and 34
   - Holbrin/Pellvoro: 89, 54 and 174
   - Askvane/Pellvoro: 85, 34 and 92
   - Kalvoran/Morvenne: 46, 34 and 71
3. Each construct's 2026 primary total hips missing from the registry:
   - Edvalt/Kelvarne: 1
   - Edvalt/Pellvoro: 2
   - Askvane/Quarvel: 7
   - Holbrin/Pellvoro: 4
   - Askvane/Pellvoro: 8
   - Kalvoran/Morvenne: 6
4. Each hospital's 2026 primary total hips missing from the registry:
   - Brennick Valley Medical Center: 12
   - Tollefson Lake Hospital: 5
   - Kittelstad Orthopaedic Hospital: 11

### construct_review_memo_2027.docx

1. The one-page memo to the Value Analysis Committee recommending the three constructs above, with a step chart of each construct's cumulative percent revision over the ten years after the operation and the 5.0 per cent bar marked as a dotted line.
