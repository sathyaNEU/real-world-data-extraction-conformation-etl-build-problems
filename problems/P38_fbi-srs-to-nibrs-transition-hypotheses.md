# P38 — "Aggravated assaults up 9%": crime trend, counting rule or reporting change across the FBI's NIBRS transition

| Field | Value |
|---|---|
| Domain | Public safety analytics / criminal-justice statistics / city performance reporting |
| Objective family | Root-Cause Analysis |
| Task shape | 18 · Hypotheses versus evidence |
| Core technique | Reconciling two counting systems (SRS hierarchy rule vs NIBRS all-offense, victim-based counts) at incident level; coverage (months reported) checks; definitional mapping; evidence grid scoring |
| Trap family (honest data) | Raw NIBRS counts compared with prior SRS counts; hierarchy rule ignored; incidents vs offenses vs victims conflated |
| Primary sources | FBI Crime Data Explorer: NIBRS state master files (relational CSV), SRS (Return A) agency data, agency participation data; city open crime-incident data |

## 1. The real-world project

A city's performance office publishes an annual public-safety scorecard. In 2021 the FBI moved to NIBRS-only collection.
The city's 2021 NIBRS aggravated assault count was 9% above its 2020 SRS count, and a council member announced an assault
surge. The police department's own incident system showed a much smaller change. The office must say what actually
explains the movement before the scorecard goes out.

## 2. The business decision (one deterministic recommendation)

**Which single cause explains most of the reported 2020→2021 change in the agency's aggravated assault count, and how
many percentage points of the movement does it explain?**

Hypotheses (rows): H1 real increase in assaults; H2 counting-rule change — NIBRS records an aggravated assault even when a
more serious offense (e.g. homicide, rape, robbery) occurs in the same incident, while SRS's hierarchy rule counted only the
most serious; H3 reporting coverage change (months reported/agency participation); H4 classification differences
(NIBRS offense definitions/weapon-injury coding vs SRS); H5 population/denominator change (rate vs count).

Evidence (columns): E1 months reported in each year; E2 NIBRS 2021 incidents where aggravated assault co-occurs with a
higher-hierarchy offense against the same victim; E3 2021 NIBRS counts converted with the hierarchy rule (computed from the
incident files per the FBI's documented conversion) vs 2020 SRS; E4 the city's own incident-system trend for comparable
offense codes; E5 neighbouring SRS→NIBRS agencies with full participation.

Rules (analysis protocol): mark each cell consistent / inconsistent with the stated figure; the adopted cause is the
hypothesis consistent with all evidence that explains the largest share of the movement, measured as (raw NIBRS − converted
NIBRS) ÷ SRS 2020 for H2, the coverage-adjusted difference for H3, etc. (formulas in the protocol).

## 3. Why this gets overlooked in real projects

* Year-over-year comparisons cross the system change silently: both series are called "aggravated assault".
* The hierarchy rule is a 1930s-era convention few analysts have applied by hand; NIBRS's multi-offense structure is spread
  across incident, offense and victim tables.
* Coverage is checked at the national level (big agencies missing in 2021) and assumed fine locally.
* "Offenses", "incidents" and "victims" are used interchangeably in dashboards.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `NIBRS_<state>_2021/NIBRS_incident.csv` | CSV | 0.3–1M | FBI Crime Data Explorer (NIBRS master, by state) | U.S. Gov public domain | Incidents |
| 2 | `NIBRS_<state>_2021/NIBRS_OFFENSE.csv` | CSV | 0.4–1.2M | FBI CDE | Public domain | Offenses per incident |
| 3 | `NIBRS_<state>_2021/NIBRS_VICTIM.csv`, `NIBRS_VICTIM_OFFENSE.csv` | CSV | 0.4–1M | FBI CDE | Public domain | Victim-offense links |
| 4 | `NIBRS_<state>_2021/NIBRS_WEAPON.csv`, `NIBRS_VICTIM_INJURY.csv` | CSV | 0.1–0.5M | FBI CDE | Public domain | Classification evidence |
| 5 | `NIBRS_<state>_2021/agencies.csv`, `NIBRS_month.csv` | CSV | ~1k / ~10k | FBI CDE | Public domain | Participation, months reported |
| 6 | `srs_return_a_<state>_2020.csv` | CSV | ~10k agency-months | FBI CDE (Summary data) | Public domain | 2020 SRS counts |
| 7 | `cde_agency_summarized_<ori>.json` | JSON | ~100 | FBI CDE API | Public domain | Published agency estimates |
| 8 | `city_crime_incidents_2019_2022.csv` | CSV | 50k–500k | City open data portal | City open-data licence (verify) | E4 |
| 9 | `nibrs_user_manual.pdf`, `srs_user_manual_hierarchy_rule.pdf` | PDF | — | FBI UCR | Public domain | Counting rules, conversion |
| 10 | `analysis_protocol.pdf` | PDF | — | Task author | — | Hypotheses, evidence formulas |

## 5. Deterministic solution path

1. Confirm 12/12 months reported in both years (E1) and stable participation.
2. From NIBRS tables, count victim-level aggravated assaults (raw) and apply the hierarchy rule per incident (converted).
3. Compare raw and converted 2021 with 2020 SRS; compute each hypothesis's explained movement.
4. Check classification evidence (E4/E5); fill the grid; adopt the cause per protocol; report points explained.

## 6. The traps

**Trap A — raw NIBRS vs SRS.** Reads the counting-rule artefact as a real increase (H1).

**Trap B — incident counts.** Counting incidents with any aggravated assault instead of victim-level offenses.

**Trap C — coverage assumed.** Or the opposite: blaming coverage without checking months reported (inconsistent with E1).

**Trap D — mis-applied hierarchy.** Applying it across victims or excluding arson incorrectly changes the converted count.

## 7. Why the data is honest

All counts are as reported by the agency to the FBI; the system change, counting rules and conversion are documented. The
work is reconciling the two systems.

## 8. Draft task prompt (prose)

> Before the scorecard goes out, I need to know what really explains our 2021 aggravated assault increase. Using the NIBRS
> and SRS files, the participation data and our city incident data in the folder, test each hypothesis in the analysis
> protocol against each line of evidence and tell me which cause we act on and how many points of the movement it
> explains. Deliver `hypothesis_grid.xlsx` with the hypothesis × evidence grid (consistent/inconsistent and the figure
> behind each cell) and the reconciliation from 2020 SRS to 2021 raw NIBRS, plus `assault_bridge.png`, a waterfall from
> the 2020 SRS count to the 2021 raw NIBRS count through the explained components. On the first sheet, state the adopted
> cause, its points of the movement, and the residual change we should actually report.

## 9. Deliverables

* `hypothesis_grid.xlsx`, `assault_bridge.png`.

## 10. Where 25+ rubric criteria come from

* 5 × 5 = 25 grid cells with figures; raw and converted counts; adopted cause; points explained; residual change.

## 11. Golden-output checklist

* Participation verified; victim-level counts; hierarchy conversion per FBI rules; grid filled; cause and residual stated.

## 12. Build notes (scope tuning)

* Choose a full-year NIBRS agency whose raw vs converted assault gap is large relative to its true change; verify with the
  incident files.
* Quote the hierarchy rule and NIBRS counting rules from the FBI manuals included, not from memory.
