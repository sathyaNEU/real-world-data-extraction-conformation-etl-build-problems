# leak check, task188

**Verdict: REVIEW.** 12 files read, 11 golden figures and 9 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: westbrook, likelihood, positive, infected, protocol, prompt, method, decisive, minimum, county, prairie, population, riverside, gravid, species, estimate, maximum, passes, nothing, records, district, gravid-trap, results, second, domain

## 2 author vocabulary (REVIEW 2)
- **REVIEW** `RCVCD_surveillance_and_control_protocol_2026.pdf`: \btraps?\b x21, a field term declared in metadata.json: ...rial application. 3 Adult mosquito sampling 3.1 CO2-baited light traps (CDC miniature light traps baited with 2 kg of dry ice, light off) st...
- **REVIEW** `field_database_data_dictionary.txt`: \btraps?\b x14, a field term declared in metadata.json: ...e ISO (YYYY-MM-DD); times are Central time. Table sites: one row per trap site site_id site ID (RC-nnn), assigned at the 15 June 202...

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `Ostby_Aviation_aerial_ULV_agreement_2026.pdf`: golden figure 2.3 appears: ...; a block is not split across nights or aircraft. 2.3 If the flight cannot be made on Thursday night...
- **REVIEW** `RCPHL_arbovirus_report_2026-W32_RCVCD.pdf`: golden figure 186 appears: ...Culex tarsalis 7 Undet. Negative RCPHL-26-5422 RC-186 08/11/2026 Culex pipiens 3 Undet. Negative RCPHL-...
- **REVIEW** `RCVCD_surveillance_and_control_protocol_2026.pdf`: golden figure 2.3 appears: ...heet Zone sections) and mapped in the zones file. 2.3 Each zone is one block for aerial application....

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `Ostby_Aviation_aerial_ULV_agreement_2026.pdf`: 4 of 25 stump-paragraph terms appear (county, maximum, records, district); read whether the document names the move
- **REVIEW** `RCPHL_arbovirus_report_2026-W32_RCVCD.pdf`: 6 of 25 stump-paragraph terms appear (positive, method, county, species, district, results); read whether the document names the move
- **REVIEW** `RCVCD_surveillance_and_control_protocol_2026.pdf`: 11 of 25 stump-paragraph terms appear (westbrook, positive, protocol, county, prairie, riverside); read whether the document names the move
- **REVIEW** `field_database_data_dictionary.txt`: 6 of 25 stump-paragraph terms appear (county, gravid, species, records, district, results); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'All eight of our treatment zones returned West Nile-positive Culex pools in the week ending 15 August 2026; which one should get the single aerial adulticide application we can fly on Thursday 20 August, judged by the es'

## 6 ranking artifacts (REVIEW 5, INFO 1)
- **REVIEW** `RCVCD_site_register_2026.xlsx`: names 7 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `RCVCD_surveillance_and_control_protocol_2026.pdf`: names 8 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `RCVCD_zones_2026.geojson`: names 7 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `WNV_human_case_log_2026.xlsx`: names 8 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `rcvcd_surveillance_2024_2026.sqlite`: names 7 of 9 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `aerial_applications_2024_2026.csv`: names 6 of 9 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read, wave 8 audit of every shipped build (2026-10-20)

Run because this build shipped with no scored reader evidence. The reader held only a fresh unzip of
`target.zip` and `prompt.txt`, with the figure names (not values) from `generator/figures.json`, and was
scored key by key by `.claude/skills/leak-check/score_reader.py`.

### Gate F has failed on this build, measured, and this is the worst call result on the lane

| block | hit |
|---|---|
| main call | **18 of 18** |
| ask figures | **60 of 82** (73.2 per cent) |

Every call figure. It filed the zone, the flight date, the rate to four decimals and the flip point, and
it reconstructed the whole decisive route unprompted: infected females per CO2 trap-night, species by
species, with the maximum-likelihood rate for pools of unequal size. It then scored the two rungs against
it in its own words, reporting that adding gravid pools puts two other zones ahead and drops this one to
third, and that the minimum infection rate puts the runner-up first because its high-abundance pools of
up to 50 understate the rate. That is the ladder, read off the pack.

It named five protocol clauses as what sent it there, 3.1, 3.2, 3.6 and 4.1 among them, which is
readability screen test 1 four times over: the pack files the trap biology, the females-per-trap-night
definition and the pool ceilings, and the decisive construction follows from them by arithmetic. It also
found and keyed the week-32 county PDF, matched all 1,155 pools by accession with no mismatches, caught
the 206-row re-import, applied the failed-trap-night clause and re-derived every case zone from the 2026
sections. The Layer 1 mess was all handled; it was never what made this hard.

```
call figures   18 of 18 hit
ask figures    60 of 82 hit (73.2 per cent)

FAIL  the reader landed the call. Gate F has failed and the architecture is spent:
      a ladder is not repaired by hardening, and an ask is not repaired by re-wording.
```

The repair re-sites the ladder, not the wording: a call a blind reader lands at medium effort is a ladder
whose decisive rung is readable, and `supplemental-stumping` 1.1c puts the reader above the author's own
cracker sheet wherever the two disagree. The specific finding here is that the protocol's own clauses
compose into the method, so the pack teaches the construction it is meant to withhold.
