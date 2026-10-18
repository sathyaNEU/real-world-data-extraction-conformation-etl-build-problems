# task200 design note

**Status: PAUSED at stage 1. No card has ever been written or registered, which is deliberate.**
Four Layer 2 mechanisms on the assigned ground were screened with measurements on 2026-10-18 and all
four are dead. The ground is `criminology-justice` / `crime-incidence-hotspot-analysis`, objective
Anomaly Detection & Diagnostics. The measurement harness is
`scratchpad/wave5/task200/screens.py` with its output in `screens_output.txt`; every number below
reproduces from it with `python3 -I screens.py`.

## What is being left behind

The 2026-10-18 pass was handed the ground `crime-incidence-hotspot-analysis` with the exposed or
ambient population denominator as its first candidate. That candidate and three others are now dead
with numbers rather than on paper, and the cell itself is closed for a structural reason recorded under
`## The cell, not just the candidates`. Earlier grounds already closed on this number, carried forward
from `pipeline.json`: environmental monitoring exceedance (a variance lever that could carry neither a
ranking nor a banded verdict, the golden tier taking both values over 40 seeds, eleven estimator forms
spread 0.52 mg/L against 0.04 permitted) and the first pass at crime incidence hotspot analysis (ten
candidates dead on paper screens, and its survivor, true incidence behind the reporting and recording
filter, failed identification outright: the profile over the reporting level is flat from 0.10 to 1.00
within 0.08 log-likelihood units, pinning true incidence only to 38.0 to 367.3 per 1,000 households,
about 8,200 times the printed precision).

**The ten rejection lines from that first pass were never written to a design note.** `pipeline.json`
pointed at `handoffs/oviya13ya.md` for them and that file predates this number's work and does not
carry them. This pass therefore spent itself re-deriving four of them. That is the single most
expensive defect in this slot's history and the reason this note exists even though no draw landed.

## The cell, not just the candidates

The cell offers exactly one family of decisive step that can be both forced and silent, and it is
already taken.

A hotspot call grades counts or cuts of a distribution of counts. For a decisive step to survive the
WHAT screen (`stumping` 1.2) the estimand has to be beyond argument while two or more methods of
estimating that one filed quantity still stand. On this ground that requires a count the records leave
as a **range** for a share of rows, with the share largest exactly for the rows the decision exists to
catch. A crime record has six dimensions and the family is exhausted across all six:

| Dimension of a crime record | Left as a range? | Verdict |
|---|---|---|
| when the offence happened | yes, an occurrence window | **taken by task184** (aoristic weight per event-hour) |
| where it happened | yes, an area or a snapped centroid | **banned**: "the place the event could have been in" is task184's driver in other nouns, so the abstraction test refuses it |
| the offence class | no, always coded; provisional codes are a vintage problem | spent (task194, two vintages measuring a coding lag) |
| who offended | yes, unknown for undetected offences | M4 below: the attribution basis is the estimand's own population |
| the target | only for communal and public-space offences | collapses into the spatial dimension, so banned with it |
| how many offences one row is | counting rules fix it; a course of conduct is free text | parsing, and harder parsing is banned as hardening |

Every other unobserved quantity the cell offers fails for a reason already measured in house: true
incidence behind the reporting filter is unidentifiable on a thinned record (this number's own
measurement, above), the underlying rate at a selected place is a shrinkage target where the opponent's
reflex is also the better estimator (task202 measured empirical Bayes beating the designed step by more
than three to one on accuracy, with James-Stein filing the golden verdict in 40 of 40 seeds), and the
causal effect of a scheme belongs to `intervention-policing-policy-evaluation`, which the client
taxonomy tags EC rather than AD.

The client's own five rigor patterns for this task type are each blocked, which is the same finding
reached from the client's side rather than ours:

| Client rigor pattern | What blocks it as the decisive step |
|---|---|
| 1 rates need the named exposure denominator | the client's own pin is "risk per a stated exposure": filed makes it rule application, unfiled forks the call (M1, measured) |
| 2 persistence is staying in the top tier across periods | the client's own pin is "a stated consecutive-period rule", so executing it is rule application and no residue is left |
| 3 recorded crime mixes incidence, reporting and detection | spent on this objective by task199 (filing intensity), and the dark figure is unidentifiable (measured flat, above) |
| 4 test clusters against a spatial null, multiplicity corrected | task191's driver (an extremum judged against a null extremum) with space in place of time: same latent structure, same default path, same correction |
| 5 smooth small-exposure rates (empirical Bayes, minimum exposure) | "shrink" is an enumerated opponent reflex, and a level at a selected unit is a shrinkage target by the house rule |

**Criminology & Justice offers no second anomaly-detection cell.** Its four subdomains are tagged
`crime-incidence-hotspot-analysis` AD, `recidivism-risk-assessment` F, `sentencing-bail-disparity-analysis`
RC and `intervention-policing-policy-evaluation` EC. So this number cannot be redrawn inside the client
domain on this objective; it needs another client domain's AD cell.

## Tried and rejected

- The exposed or ambient population denominator, a crime rate per ambient person or per opportunity
  rather than per resident (2026-10-18, stage 1, measured): dead three ways over 40 neighbourhoods and
  a top-8 funded band. Ten ambient-population forms a competent analyst would use produce **5 distinct
  designation sets and 4 distinct rank-1 neighbourhoods**, and the graded rate for one fixed
  neighbourhood runs 116.81 to 373.42 per 1,000, a spread of **256.61 against 0.04 permitted** at a
  printed unit of 0.1, over by a factor of about 6,400. So the family is not closed and cannot be
  closed by discretising the answer, because the spread crosses the band boundary. The WHAT screen
  kills it independently: the denominator **is** the estimand's unit, so naming it ("per 1,000 ambient
  person-hours on 24/9/3 weights") makes the decisive step the execution of a filed clause, and leaving
  it unnamed ("relative to the population at risk") forks the main recommendation across those 5 sets,
  with no third position. And the swap test fails outright: "the rate per ambient person present at the
  hours the offences happen" reads identically as an infection rate per ambient person or as faults per
  machine-hour, so per-exposure rather than per-head is the most general move in quantitative science
  and the generating process has dropped out.
- The baseline fitted on a window that already contains the intervention, with the field's method an
  interrupted series fitted on a clean period and projected (2026-10-18, stage 1, measured): dead on
  the 1.2b pincer. A council files its own rollout dates in the committee report that authorised the
  spend, so excluding the implementation period follows from reading one shipped sentence, which is
  rule application. Unfiled, the record does not measure its own rollout window: profiling the
  implementation start over plus or minus 10 periods with level, trend and shift free leaves a set **3
  periods wide** within 2 log-likelihood units, so recovering it is an unstated rule (banned) or case
  three. Worth recording that the reflex sweep did **not** kill this one: 0 of 6 reflexes landed within
  2.0 of the true shift of -14.00 (the all-pre-period baseline filed -7.78, a last-12-months baseline
  +0.44, pre mean against post mean -0.96), so the mechanism had real separation and died purely on the
  pincer. Any future attempt on this shape needs an implementation window no document states and that
  the record measures about itself exactly, which this ground does not supply.
- Displacement and diffusion between adjacent units, with the field's method a net effect over a buffer
  ring rather than a per-unit count (2026-10-18, stage 1, measured): dead four ways. A single citywide
  displacement fraction gives net = gross x (1 - df), a positive monotone rescaling of every candidate,
  so **the ranking cannot change at any value of df** and the mechanism is worth nothing on the graded
  object. A per-scheme fraction is needed instead, and from a closed roster of 24 past schemes the
  fraction estimates at 0.436 with a standard error of 0.109 against a truth of 0.32, while the
  per-scheme spread is 0.522 against the **0.109 difference needed to reorder the leading two
  candidates**, so the lever is 4.8 times the estimator's own noise and the call is seed hostage. The
  WHAT screen kills it again, because "the net change across the whole city" against "the change in the
  funded area" is the estimand's comparison population. And the objective is wrong: a funding pick on a
  causal effect is served by `intervention-policing-policy-evaluation`, tagged EC, so the
  `Task type:` line would not pass `precut.py`.
- Journey-to-crime attribution, the count the decision defines being offences committed by residents of
  each neighbourhood rather than offences occurring in it, apportioned by the distance decay the
  detected offence-offender pairs measure (2026-10-18, stage 1, measured): dead on the WHAT screen,
  which is the shape that killed task190, task192 and task193 at stage 4 with every figure reproducing.
  The two bases are not two methods for one quantity, they are two different populations, and the
  measured designation sets share only **2 of 8 members** with rank 1 moving between them. Filing the
  basis makes the offender join follow from the clause; leaving it unfiled forks the call. This is the
  strongest candidate the cell has on the swap test (no other field has an offender choosing a target a
  short distance from home) and it still cannot be drawn, which is the clearest single statement of why
  the cell is closed rather than merely picked over.

## Resume

Do not re-screen the five mechanisms in the table above or the four in `## Tried and rejected`: all
nine are measured, not argued. The next pass on this number takes it to **another client domain's
anomaly-detection cell**, because Criminology & Justice has no second one. The nine axes reserved for
this slot in wave 5 were never spent and return to the pool unused: `shape` 14,
`stump_strategy` `population_selection`, `calibration_form` `realised_outcome_roster`, `role_family`
`field_unit_lead`, `gate_g` `decomposition_attribution`, `gap` `population`, `forum`
`council_or_assembly`, `forcing_event` `budget_or_appropriation`, `org_family` `local_government`.
