---
name: fingerprint
description: The anti-repeat system for task builds. Every build has a fingerprint card under cards/ (domain, subdomain, niche, objective, prompt shape, decision type, gap, pattern, generators, Gate G mechanism, calibration form, context artifact, stakeholder role, spine, world, deliverables, opening move, and a driver sentence with the domain nouns stripped), and guard.py checks a proposed draw against every card before the ladder is written, so the same kind of project is never drawn twice. Use at the start of every new build and every re-root (guard.py recent, coverage, suggest), when the draw is fixed and before any data is cut (guard.py check, then register), after the pack is cut (guard.py surface), and whenever the author asks whether a build repeats an earlier one. Mandatory, mechanical and free, it spawns nothing; the adjudicated /clone-check is author-triggered only.
---

# Fingerprint

> The cheapest place to stop a repeat is before the first file exists.

## Part 0. What this is for

The ledger holds each build's status and portal result; a card, filed when the draw is fixed, holds identity
in one vocabulary, so the guard bans against builds in flight. **A card records identity, never outcome**
(status and outcomes go to `stumping/references/shipped-ledger.md`), except `lineage`, which keeps each dead
architecture's fate: a driver already solved is the worst redraw.

## Part 1. The card

`cards/taskNN.json`. Every enumerated field takes a key from `vocab.json`; `guard.py validate` refuses
anything else.

| Field | Records |
|---|---|
| `domain`, `subdomain`, `client_domain` | domain and subdomain; the client domain a house domain sits in |
| `niche` | the unusual sub-function, in the build's nouns (similarity) |
| `objective`, `shape` | one of the eight objectives; prompt shape `01` to `18`, `single-figure`, `other` |
| `decision_type`, `answer_unit`, `scoring_unit` | kind of call, its unit, the unit it is scored or paid on |
| `gap`, `pattern`, `generators` | decisive first |
| `gate_g` | the mechanism carrying the stump |
| `calibration_form`, `context_artifact` | calibration organ (`none` allowed); the stakeholder's file type |
| `stump_strategy` | the family of the decisive move, from the dataset's own analytic structure |
| `decisive_rule_filed`, `official_decoy` | booleans; `false` plus `true` is the withheld rule with an official decoy, whatever the strategy says |
| `validated_decoy` | the wrong method reproduces every certified figure and only a forward condition breaks it |
| `stump_class` | `analytical`, `planted`, `data_semantics` or `rule_application`; only `analytical` passes |
| `analyst_test` | the easy route a strong analyst takes after reading everything correctly, and its wrong answer |
| `domain_test` | the field's own analysis that decides, and why a noun swap breaks the task |
| `layer2_family`, `layer2_pattern` | family from `vocab.json`; pattern `<domain>/<task-type>/<n>` from `layer2-rigor-patterns.md`, or `own:<name>` |
| `layer1` | the Layer 1 techniques the pack carries |
| `stakeholder_role`, `role_family` | the role as stated, its family |
| `spine` | file, rows, row meaning, grain, source dataset |
| `world` | geography, currency, org type, invented nouns, `people` |
| `forum`, `forcing_event`, `org_family` | who decides, what forces it now, the kind of organisation; always declared |
| `deliverables`, `opening_move`, `question_form` | file names; `question-first`; how many, how much, which, whether, what, when, who, where |
| `driver` | **one sentence, the decisive move with every domain noun stripped** (similarity) |
| `driver_concrete`, `stump` | the move in the build's terms; the wrong committed answer and the step that lands it |
| `answer`, `answer_source` | the committed answer verbatim, its source |
| `lineage`, `differentiation` | earlier architectures with fate and driver; `{taskNN: one line}` against a flagged build |

**The driver catches the reskin.** Strip industry, organisation, metric names and figures; keep what
quantity decides, where it comes from and what it does to the naive answer, so one insight in two
industries yields near-identical sentences.

```
weak    The analysis has to account for an important constraint in the data.
strong  The decisive quantity is a per-unit floor recovered from a closed corpus of past
        determinations, and applying it removes the largest naive candidates from the total.
```

## Part 2. The procedure

**1. Before choosing the pairing:**

```
python3 .claude/skills/fingerprint/guard.py recent      # last builds, one line each
python3 .claude/skills/fingerprint/guard.py coverage    # spent and never-drawn cells, axis use overall and last 12
python3 .claude/skills/fingerprint/guard.py suggest     # optional fresh draws, never breaking a ban
python3 .claude/skills/fingerprint/guard.py mechanisms --objective <o>   # every spent driver there, lineage included
```

`mechanisms` is the one read of the corpus a draw needs: one block per build on the objective (narrow it with
`--gate-g` or `--strategy`), so no card is opened by hand. Write one line on the insight each spends before
drawing. Everything here is mechanical and free; the people index and the clone screen keep working caches
under `.cache/` (never committed), seeded from the tracked baselines in `corpus/` and
`../clone-check/corpus/`.

**2. When the draw is fixed** (before the ladder; personas from `guard.py names --geo <geo> --seed <N>`):

```
python3 .claude/skills/fingerprint/guard.py new task98 > <scratch>/task98_card.json   # fill from ## Draw
python3 .claude/skills/fingerprint/guard.py check <scratch>/task98_card.json
python3 .claude/skills/fingerprint/guard.py register <scratch>/task98_card.json
```

The registered card is committed at once with `pipeline.json` and the design note (`DRAWN (taskNN)`), so every
other session's guard sees the draw.

Clear every BLOCK by redrawing its axis; answer each WARN in one design-note line. `register` refuses a
BLOCK; `--force` is the author's override, reason in `notes`.

**2b. The window moves under you, and your own registration moves it.** The axis bans (`ban.forum`,
`ban.forcing_event`, `ban.org_family`, `ban.strategy`, `ban.pairing`, `ban.subdomain`, `ban.pattern`,
`ban.role`, `ban.artifact`, `ban.spine`, `ban.shape`) run against the last three builds by filing time, and
`register` stamps that time afresh. So registering your own card pushes the slot's previous architecture
out of the window and pulls another build in, and a late re-registration anywhere reorders every live
build's window at once. A clear verdict therefore has a short shelf life. **Run `check` against the
registered card as the last act of stage 1**, not against the draft, and run it again before relying on a
clear verdict at stage 2. Three builds hit this in one day: one cleared `ban.forum` twice post-registration
before landing on a third value, and one cleared three axis BLOCKs at stage 2 that had not existed when its
draw was fixed. Redraw the axis rather than argue it, since differentiation never clears an axis ban, and
say in the note which values were redrawn and why the replacement is the honester label and not merely the
passing one.

**3. Re-root:** move the old identity into `lineage` with its fate, write the new draw, check and register.
The guard compares against the slot's own lineage too.

**4. After the pack is cut:** `guard.py surface task98` runs the `clone-check` hard-tell screen on the build
and re-reads persona names from the pack; a promoted pair is renamed or regenerated.

**4b. Duplicate check (stage 3, and `/approve`):** `guard.py heart taskNN` compares `driver`,
`driver_concrete` and `stump` with every driver, lineage driver, stump and shipped-ledger row, then runs
the full check; exit 1 on BLOCK. An empty `stump` is filled from the design note first.

**5. When the submission is final**, update `answer`, `answer_source`, `spine.rows`, `deliverables`,
`opening_move` and `question_form`. Part of delivery, because the next draw checks against it.

**6. The ledger row** is rewritten at each status change (drawn, built, shipped, re-rooted, retired) and
takes the portal result with its date the day the author reports it (`build-pipeline`, The ledger row);
the card is untouched.

## Part 3. What the guard decides

BLOCK if any rule blocks, else WARN, else PASS; exit 1 on BLOCK.

| Rule | Level | Against |
|---|---|---|
| `legal.domain`, `legal.objective`, `legal.gate_g` | BLOCK | the taxonomy; surface-read rejection or `statistical_rigor` alone |
| `ban.pairing`, `ban.subdomain`, `ban.pattern`, `ban.calibration`, `ban.role`, `ban.artifact`, `ban.spine`, `ban.strategy` | BLOCK | last three builds |
| `ban.source` | BLOCK, else WARN | the same real source dataset in the last three, else anywhere |
| `ban.shape` | BLOCK | last two |
| `ban.forum`, `ban.forcing_event`, `ban.org_family` | BLOCK | last three; `overuse.*` WARN when spent across the corpus |
| `template.withheld_rule_decoy`, `template.cap` | BLOCK | in any of the last three, or already two in the last twelve; `template.flagged` WARN on every carrier |
| `template.validated_decoy`, `template.validated_cap` | BLOCK | in the last build, or already three in the last twelve |
| `overuse.strategy` | WARN | one strategy in three of the last twelve |
| `three_rules.class`, `.analyst_test`, `.domain_test` | BLOCK | a card from 2026-10-10 missing them or not `analytical` |
| `three_rules.strategy_risk` | WARN | `time_semantics`, `grain_or_unit`, `identity_resolution`, `stated_rule_hard_construction`, `withheld_rule_corpus_fit` |
| `test.same_puzzle` | BLOCK | gap, pattern and decision type equal, last twelve, lineage included (older: unless differentiated) |
| `test.same_driver` | BLOCK | gap, pattern and Gate G equal, last twelve, lineage included (older: unless differentiated) |
| `test.own_lineage` | BLOCK unless differentiated | the slot's earlier architectures |
| `driver.text` / `driver.near` | BLOCK unless differentiated / WARN | driver similarity 0.30 and up / 0.12 to 0.30, every driver on file |
| `tell.names` | BLOCK | a shared multi-word invented name |
| `people.full`, `people.inside` | BLOCK | a full name reused anywhere; two personas in one build sharing a first name or surname |
| `people.first` / `people.last` | BLOCK, else WARN | first name in 3+ builds or the last twelve / surname in 2+ or the last twelve; else one older build |
| `overuse.*`, `repeat.*` | WARN | domain, objective, shape, Gate G, decision type, deliverable set, PDF share, opening move, question form, geography, niche |

- **Three and twelve:** the neighbours a reviewer holds, and one sitting.
- **Two structural tests:** the Template clone on record (task86 v1, task72 v2) differed only in decision
  type, so `test.same_puzzle` alone passed it.
- **Differentiation** clears only similarity rules, never axis bans. A line that cannot be written is the
  finding.
- **Drawn, never typed:** personas (one first name stood in 23 builds), furniture (committees and boards
  decided 49 prompts, regulators none), and pack file names in the organisation's idiom.

**Look up a strategy's ban window before spending design time on the direction.** `ban.strategy` is an
axis ban, so differentiation does not clear it and no argument will: a direction is either available or
it is not, and that is a fact to read off `coverage` and `recent` in the same breath as `mechanisms`,
before the design exists. task194 drew a sound architecture on `maturity_censoring` and could not
register it, because the immediately preceding build in the corpus carried the same label. Two costs
follow from checking late. The design waits for a window to lapse rather than being drawn into a free
cell, and the builder is put in front of a choice between relabelling the mechanism to pass the guard,
which is a lie in the card, and handing the block back. The right answer to that choice is to hand it
back; the better outcome is never to face it.

## Part 4. How this goes wrong

- **A PASS read as "not a clone"**: the design note still answers the similarity test.
- **A card written to pass**: if two keys fit, use the reviewer's. **A vague driver**: no quantity, no source.
- **A stale card** after a re-root: bans run against the dead architecture and pass.
- **Vocabulary drift:** a new `vocab.json` value only when none is honest (reason in `notes`); `other`
  exists so no untrue key is forced.
- **A family offered on its label:** a mechanism `coverage` shows as never drawn may have died in lineage
  (confirm_surface_read: zero main uses, four lineage architectures, all solved). Read the fates first.
- **Not registering.** An unfiled card protects nobody.

## Part 5. Maintenance

`guard.py validate` after editing a card or `vocab.json`; cards are edited in place. `register` stamps
`registered` with the filing time, and builds drawn the same day order by it (cards filed before the stamp keep
task-number order and come first), so a draw's bans reach the builds actually filed before it. Driver thresholds:
cross-slot 99.9th percentile under 0.10, a byte-identical rebuild 0.88, AUC about 0.6 for mechanism (hence
the structural tests); recalibrate with `guard.py nearest`. Cards to task36 carry fitted labels; builds
with no design note or ledger row carry `mechanism_source: submission_only`.
