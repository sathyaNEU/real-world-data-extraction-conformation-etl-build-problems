# leak check, task181

**Verdict: REVIEW.** 15 files read, 24 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: traffic, tarvik, close-out, vertical, exposure, nothing, climbing, grendal, crossing, crossings, levels, architecture, control, hallin, forward, descending, method, interaction, reflex, readable, centre, brekka, review, decisive, season

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `HACC_summer2026_safety_closeout.pdf`: carries 11 of 11 distinctive words of the committed call: "Tarvik will run over the safety plan's tolerance in summer 2027, at about 72 ATM-related losses of separation per 100,00"
- **REVIEW** `HACC_unit_safety_plan_2026-2028.pdf`: carries 9 of 11 distinctive words of the committed call: "Tarvik will run over the safety plan's tolerance in summer 2027, at about 72 ATM-related losses of separation per 100,00"

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `HACC_OM_part3_ch4_sector_configuration.pdf`: 5 of 25 stump-paragraph terms appear (traffic, tarvik, grendal, control, hallin); read whether the document names the move
- **REVIEW** `HACC_summer2026_safety_closeout.pdf`: 8 of 25 stump-paragraph terms appear (traffic, tarvik, close-out, grendal, control, hallin); read whether the document names the move
- **REVIEW** `HACC_unit_safety_plan_2026-2028.pdf`: 6 of 25 stump-paragraph terms appear (traffic, close-out, control, centre, review, season); read whether the document names the move
- **REVIEW** `extract_notes_2026-10-12.md`: 3 of 25 stump-paragraph terms appear (traffic, levels, control); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `planning_traffic_summer2027_issue1.csv`: 617826 ISO dates after 2026-10-12, e.g. 2027-05-31, 2027-06-01, 2027-06-02, 2027-06-03, 2027-06-04

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read (pass 1, Sonnet, 2026-10-12)

Q1. none. Nearest context: the close-out's Hallin note ("the western arrival stream to Holmvik moved entirely onto
the Hallin descent with AIRAC 2603 ... Hallin's summer flight hours rose by 7 per cent and its ATM-related losses went
from one to two") and safety plan 4.2 ("forecast for every elementary sector from the unit's occurrence record since
the present eight-sector structure came into use on 1 January 2025, and from the planning traffic"); inputs, not a
method.

Q2. The close-out's Table 1 ranks the sectors on their summer 2026 rates against 40.0 ("No sector exceeded the unit
safety plan's tolerance of 40.0"): the prior season, labelled as such. Nothing ranks summer 2027.

Q3. none clear; the extract notes and the occurrence code list are plausible.

Q4. none; the summer 2026 rates (Mosby 32.0, Grendal 28.6, Hallin 28.6) and the 40.0 tolerance are context, and no
2027 figure appears anywhere.

Q5. Plan 3.5 (flight hours from sector entry to exit, over the planning traffic for a season to come), 3.2 (summer in
local time, the data in UTC), 3.3 and 3.4 (SMI with ATM contribution D or I), 3.1 (counted for the elementary sector),
4.1 and 4.3 (per 100,000 flight hours, per sector and season, not averaged), 4.2 (the record since 1 January 2025).
None fixes the forecast method.

REVIEW lines: all harmless (the close-out and the plan are the indicator's own documents and neither forecasts 2027;
the manual, close-out and notes carry sector names and operations vocabulary; the planning traffic's 2027 dates are
the season it plans).

Realism tells:
1. The register's revision 14 beside the manual's table revision 8 and the current table's revision 9.
2. The configuration table's export dated the extract's day.
3. One-page PDFs with identical footers and layout.
4. Close-out rates neat (Grendal and Hallin both 28.6).
5. Planning flight keys strictly sequential; one roster remark repeating on the 4th of each month.

Repair (2026-10-12), in the stage 4 pass with the judge's FIX_NOW: the plan, close-out and manual rebuilt to their
genres (the plan with its indicators table, sections 6 and 7 and edition history; the close-out with a memo head,
three tables and actions; the manual in its own house style), the configuration table's export dated 9 October, the
planning flight keys issued out of order and the roster remarks varied. Kept: the revisions (a manual edition printed
before a table amendment is the record the hours ask reads) and the two 28.6 rates (2 on 6,983 and 4 on 14,008 hours).
No graded figure moved. A second read follows because the documents changed.

## Solver's-eye read (pass 2, Sonnet, 2026-10-12)

Q1. none. Closest context: plan 4.2 (the occurrence record since 1 January 2025 and the planning traffic) and the
close-out's section 4 (the summer 2027 forecast to be presented on the planning traffic Network and Capacity Planning
issues); both name inputs, not how to model them.

Q2. none ranks summer 2027. The close-out's Table 1 ranks the summer 2026 rates against 40.0 (Mosby 32.0 highest): the
prior season's standing.

Q3. none; every file reads as something the unit would hold. Weakest: the met activity summary and the controller
roster (the notes say they were sent as asked), both plausible requests.

Q4. none; 40.0, Mosby 32.0 and the Hallin note (7 per cent more flight hours after AIRAC 2603) are context and state no
2027 conclusion.

Q5. Plan 3.5 (flight hours summed entry to exit over the planning traffic's flights, per elementary sector), 3.1
(counted for the elementary sector, not the combined position), 3.2 (1 June to 31 August local time, the planning file
in UTC), 3.3 and 3.4 (SMI, contribution D or I), 4.1 and 4.3 (shall not exceed 40.0 per 100,000 flight hours, per
sector and season, not averaged), 4.2 (the whole record since 1 January 2025 with the planning traffic), the notes (one
row per planned flight per traffic volume, UTC). Not fixed: the model form.

REVIEW lines: all harmless (the close-out gives 2026 rates, not a 2027 forecast; the plan is the filed tolerance and
definitions; the manual, close-out, plan and notes carry sector names and generic words; the planning dates from
2027-05-31 22:00 UTC are 1 June local).

Realism tells (minor): Table 1's coinciding 28.6 rates (checked correct); flight keys interleaved and repeated across
traffic-volume rows (plausible for a multi-volume join); the planning CSV's terse column names and single issue
number; tidy PDFs without logos or stamps; the manual's revision 8 against the register's revision 14 valid from
19 March 2026. No strong machine tells. Nothing to repair.


## Solver's-eye read, wave 8 audit of every shipped build (2026-10-20)

Run because this build shipped with no scored reader evidence. The reader held only a fresh unzip of
`target.zip` and `prompt.txt`, with the figure names (not values) from `generator/figures.json`, and was
scored key by key by `.claude/skills/leak-check/score_reader.py`.

### Gate F has failed on this build, measured

| block | hit |
|---|---|
| main call | **1 of 1** |
| ask figures | **86 of 141** (61.0 per cent) |

It filed the right sector as the only one over tolerance and reconstructed the decisive step whole: that
the occurrences are a climbing or descending flight crossing a level flight's cruise level, so the
exposure is level crossings rather than flight hours, and that this sector's crossings jump about
fourfold on a flight-hour rise of a tenth, which a flight-hour projection hides. It also reported the
sector's flight-hour record rate as the lowest of the eight, which is the trap stated from the inside.

**The one encouraging detail, and it is not enough.** Asked what told it to take the step, it said
plainly that **nothing in the files states crossings as a method and that it inferred it from the data**.
So this build's readability screen holds where four of the others' do not: the pack does not teach the
construction. It was landed anyway, which says the gap between the easy route and the decisive one was
too small to stop a careful reader rather than that the route was signposted. That is a magnitude
failure, not a leak, and it is repaired by widening the separation at stage 2.

```
call figures   1 of 1 hit
ask figures    86 of 141 hit (61.0 per cent)

FAIL  the reader landed the call. Gate F has failed and the architecture is spent:
      a ladder is not repaired by hardening, and an ask is not repaired by re-wording.
```
