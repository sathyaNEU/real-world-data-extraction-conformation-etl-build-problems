# Verdict, task150 (classroom placement, Sorrel Creek RE-6)

**Verdict:** NOT_DETERMINISTIC, on supplementary answer 2 only. The main recommendation is forced (Gates A, B, C pass for it). Ask 2 fails Gate E: "homeroom classes meeting that day" has no filed unit.

**Disposition:** FIX_NOW. Pin the unit of a class in one clause of the prompt, for example "counting each room and session once", or in sis_export_notes.txt. The main call, the pack and the other figures stay byte-identical. Only ask 2 needs regrading, and no re-run of the main call is needed.

**Why:**
- Ask 2 asks for "each school's homeroom classes meeting that day". No shipped file says what one class is.
- The golden counts distinct (room, session) pairs among homeroom sections with at least one active pupil. A combined 1/2 class in one room with one teacher counts once. A second teacher's 3 to 5 pupil section in the same room counts once. A kindergarten AM and PM pair counts twice. The zero-pupil T00000/TBD placeholder and sections ended before Oct 1 are dropped.
- sis_export_notes.txt says each row is a "section" that "meets" in a room and session. A literal solver reading "classes" as sections gets different numbers (table below).
- Taxonomy label: prompt_ambiguity (Gate E), and underspecified_objective for the unit.

## Evidence

Main call (reproduced from the shipped files):

| Item | Reproduced? | Source |
|---|---|---|
| Pupil linkage: 76,597 rows on 14 count days, no duplicate pupil-year, 16 legacy numbers unconverted | Yes | membership_oct2013-oct2018.txt, october_membership_2019-2026.csv, student_number_crosswalk_2019.csv, school_codes.csv (105 = Kessler) |
| 2026 October K-5 counts 778, 804, 733, 845, 949, 726, 566 | Yes, and they match meal_eligibility_2026-10.csv | membership files |
| K-new / births five years earlier is about 1.0 at most schools (Ortega about 0.69) | Yes | membership files, brandt_county_births_by_attendance_area_2008-2025.csv |
| Rated capacities 667, 640, 703, 710, 833, 651, 577 | Yes | facilities_capacity_report_2026-09.xlsx |
| Flow model (repeats per grade, exits and moves per K-4 pupil of the school left, average arrival count per grade, new K per birth, 13 transitions, 2026 and 2027 births at the 2023-25 average): excess over capacity 5-year avg 2028-32 = 109, 131, -92, 89, 152, 60, 10 for Fifth, Lincoln, Ortega, Bluestem, Prairie Rose, Kessler, North Fork | Yes, exactly | membership files, births file, FEA-R2 PDF 2(b) to 2(e) |
| Need 5, 6, 0, 4, 7, 3, 1 (26 in all); placement Prairie Rose 7, Lincoln 6, Fifth 5, Bluestem 4, Kessler 2, North Fork 0, Ortega 0 | Yes | FEA-R2 section 3 |
| Preschool: 88 and 4 rooms (Fifth), 94 and 4 (Ortega), 51 and 3 (Kessler), 35 and 3 (North Fork) | Yes | preschool_enrollments_2026-27.csv (active on Oct 1, one record per state ID) plus ecse_roster_2026-10-01.xlsx (ECSE and inclusive classroom children not already in the file, itinerant excluded) |
| Homeroom classes 17/17, 19/15, 19/13, 15/20, 21/20, 15/17, 13/13 | Yes, but only under the room-and-session rule above | sections_fall2026.csv, section_enrollment_fall2026.csv |

Main-call robustness (flow family):
- Windows of 3 to 13 transitions, per-school against pooled repeat rates, births for 2026 and 2027 (last year, 3-year average, 5-year average, plus 1.5 per cent on provisional 2025) all give need 5, 6, 0, 4, 7, 3, 1 and the same placement.
- Excess ranges: Bluestem 80 to 92 (band 73 to 96), Fifth 102 to 114 (band 97 to 120), Prairie Rose 149 to 159 (band 145 to 168), Lincoln 129 to 135 (band 121 to 144).
- The margins to a band edge are only about 7 to 12 pupils. They hold across every defensible variant I ran, so this is thin-but-clean and not contested.

Competing methods on the same files (none reaches the golden):

| Method | Need (Fifth, Lincoln, Ortega, Bluestem, Prairie Rose, Kessler, North Fork) | Placed | Back-test from 2019, miss at 2026 |
|---|---|---|---|
| Cohort progression ratios, 5-year window | 5, 6, 0, 7, 9, 4, 1 | 3, 6, 0, 7, 8, 0, 0 | Fifth -8.0 per cent, Prairie Rose +8.5 per cent, Bluestem +3.9 per cent |
| Same, 3-year window | 5, 6, 0, 6, 8, 4, 1 | 4, 6, 0, 6, 8, 0, 0 | Fifth -9.9 per cent, Prairie Rose +8.8 per cent |
| Additive net-migration cohort | Bluestem 6 or 7, Prairie Rose 8 | Kessler 0 | Fifth -7 to -10 per cent |
| Pupil-level flow model | 5, 6, 0, 4, 7, 3, 1 | 5, 6, 0, 4, 7, 2, 0 | all within 1 to 2 per cent except Ortega 5.1 per cent |

- The golden's stated 8.2 per cent low at Fifth and 8.3 per cent high at Prairie Rose reproduces to within 0.3 points.
- The data therefore separates the candidates by out-of-sample test. Fifth's arrivals are a steady 66 to 89 a year while its K-4 pupils fall from 741 to 639. Prairie Rose's K-4 pupils rise from 532 to 752 with 61 to 81 arrivals a year. Ortega sends Bluestem 58 to 93 pupils a year.

Open fork on ask 2 (class unit), for example North Fork grades 3 to 5 and Fifth Street:

| Reading of "class" | North Fork 3-5 | Fifth Street K-2 / 3-5 |
|---|---|---|
| Golden: distinct room and session | 13 | 17 / 17 |
| Sections with active pupils | 15 | 18 / 19 |
| Sections meeting by dates, including the T00000/TBD placeholder | 16 | 18 / 19 |
| Distinct teacher of record (the AM/PM kindergarten pair becomes one) | differs again | differs again |

The same ambiguity runs through all 14 figures.

Preschool forks (accepted, noted):
- Counting preschool_enrollments_2026-27.csv alone, or leaving the ECSE roster out, gives 77/32/29/79 children. That is the intended completeness device and the roster is in the pack.
- Itinerant children are in no class, so excluding them is the natural reading.

## Files/Hygiene

PASS.
- 16 files: pdf, xlsx (3), csv (8), txt (3).
- Row counts in export_manifest_2026-10-09.csv match the files (44,314, 32,283, 5,505, 290, 229).
- Large file well over 25,000 rows.
- Distractors that weigh but are unused: facility_condition_assessment_2025.xlsx, meal_eligibility_2026-10.csv, the portables note.
- Artifacts read as district operational exports with real mess:
  - legacy and current systems with different codes and date formats;
  - the Southeast to Kessler rename;
  - duplicate and transfer preschool registrations;
  - mid-year section teacher swaps;
  - a placeholder section.
- No authoring or benchmark language found, and timelines are coherent (pulls 10/08/2026, policy adopted 3/12/2026). Nothing exclusion-level.

## Stump power

Good. The easy route is cohort progression ratios, the standard enrollment-projection method, which a capable analyst files. Even after perfect cleaning it gives Prairie Rose 8, Bluestem 7, Fifth 3, Lincoln 6 and Kessler 0, against the golden Prairie Rose 7, Lincoln 6, Fifth 5, Bluestem 4, Kessler 2. Every progression-ratio window lands on a different wrong vector, so the main call stumps many strong runs. The three tables are an independent source of ask-weight difficulty. Confirm with live runs that stumps are analytical (CSR) and not caused by the ask-2 fork.

## Stumping type

`mechanism: method_or_model_selection` (forecasting on honest data, with etl_conformance for the tables), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`

All reported counts are correct. The difficulty is choosing the arrival and transfer-aware flow projection over progression ratios, settled by an out-of-sample back-test the pupil-level data allows. Clean data still stumps, so Gate G passes.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`

- **Domain (H1):** enrollment projection and classroom need against rated capacity is the work of school facilities planning. The swap test fails to transpose it.
- **Layer 1:** the conversion of student systems in 2019 with a partial crosswalk, the school rename, two file layouts, provisional 2025 births, duplicate preschool records and ECSE rosters, and split sections.
- **Layer 2:** pupil-flow cohort projection validated against progression ratios by back-test.
- **Decisive step (H3):** the projection method. A strong analyst who cleaned everything and read FEA-R2 correctly would still file the progression-ratio answer above.

## Fix

Location: prompt, with an optional alternative in input_files (sis_export_notes.txt).
- Add one clause fixing the unit for ask 2, for example "counting each room and session once". Alternatively add a notes line that a class is the group of pupils meeting with a teacher in a room and session, and that sections are rows.
- Check the clause does not reveal the combination and co-teaching device beyond what is needed, and keep the prompt under 1,000 characters.
- Optionally pin in the prompt or notes that itinerant ECSE children are not enrolled in classes.
- Leave the main call, goldens for the placement and preschool tables, and the bundle otherwise untouched.
