---
name: fingerprint
description: The anti-repeat system for task builds. Every build has a fingerprint card under cards/ (domain, subdomain, niche, objective, prompt shape, decision type, gap, pattern, generators, Gate G mechanism, calibration form, context artifact, stakeholder role, spine, world, deliverables, opening move, and a driver sentence with the domain nouns stripped), and guard.py checks a proposed draw against every card before the ladder is written, so the same kind of project is never drawn twice. Use at the start of every new build and every re-root (guard.py recent, coverage, suggest), when the draw is fixed and before any data is cut (guard.py check, then register), after the pack is cut (guard.py surface), and whenever the author asks whether a build repeats an earlier one. Mandatory, mechanical and free, it spawns nothing; the adjudicated /clone-check is author-triggered only.
---

# Fingerprint

> The cheapest place to stop a repeat is before the first file exists.

## Part 0. What this is for

Builds come out as the same kind of project for a mechanical reason, not a creative one. The
shipped ledger records outcomes, so it gets a row only when the portal result comes back, and every
build finished but not yet reported is invisible to it; it is also too large, with single rows of
20,000 characters, to read whole at draw time. So the standing bans in `stumping` Part 6.1 cannot be
checked against it.

A fingerprint card fixes both halves. It is one small structured record per build, in a controlled
vocabulary, so two builds that made the same choice collide on the same string. It is filed the
moment the draw is fixed, so a build in flight is visible to the next one. And `guard.py` reads
every card in under a second, so the check is run every time rather than remembered.

**A card records identity, never the outcome of the build it describes.** It says what kind of
project a build is and what drives its difficulty. Whether that build stumped on the portal belongs
to `stumping/references/shipped-ledger.md` and is written there once, when the author reports it.
That split is deliberate: the ledger's rule against pending rows exists because a row written before
the portal speaks records a guess as a fact, and a card makes no claim about its own build's portal
result at all. The one place a card carries a fate is `lineage`, and that is history rather than a
guess: why an earlier architecture was abandoned, kept because a driver the portal already solved
is the worst thing to draw again.

## Part 1. The card

One JSON file per build slot, `cards/taskNN.json`. Every enumerated field takes a key from
`vocab.json`, and `guard.py validate` refuses anything else.

| Field | What it records | Kind |
|---|---|---|
| `domain`, `subdomain` | one of the nine domains and one of its enumerated subdomains | enum |
| `niche` | the unusual sub-function inside the subdomain, in the build's own nouns | free, compared by similarity |
| `objective` | one of the eight Axis 1 objectives | enum |
| `shape` | the prompt shape the rubric's criteria come from (`01` to `18`, `single-figure`, `other`) | enum |
| `decision_type`, `answer_unit` | what kind of call, and in what unit | enum |
| `gap`, `pattern`, `generators` | the decisive gap, pattern and G-code, **decisive first** | enum lists |
| `gate_g` | the FINE-numbers mechanism that carries the stump | enum |
| `calibration_form`, `context_artifact` | the calibration organ, and the type of file the stakeholder works from | enum |
| `stakeholder_role`, `role_family` | the role as the prompt states it, and its family | free plus enum |
| `scoring_unit` | the unit the decision is scored or paid on | enum |
| `spine` | the spine file, its rows, what one row is, its grain, and its source dataset | mixed |
| `world` | geography, currency, organisation type, the proper nouns the build invented, and `people`, every persona the build names | mixed |
| `forum`, `forcing_event`, `org_family` | who receives or decides the call, what forces it now, and the kind of organisation it sits in | enum |
| `deliverables`, `opening_move` | the file names the prompt asks for, and the prompt's opening move | free plus enum |
| `driver` | **one sentence, the decisive move with every domain noun stripped** | free, compared by similarity |
| `driver_concrete`, `stump` | the same move in the build's own terms, and the wrong committed answer a competent solver files with the step that lands them there | free |
| `answer`, `answer_source` | the committed answer verbatim, and where it was copied from | free |
| `lineage` | every earlier architecture of the slot, with its fate and its driver | list |
| `differentiation` | `{taskNN: one line}` against a build the guard flagged as close | map |

**The driver sentence is the field that catches the reskin**, the clone with no surface overlap at
all, so write it with care. Strip the industry, the organisation, the metric names and the figures,
and keep the structure of the move: what quantity decides, where it comes from, and what it does to
the naive answer. Two builds that turn on the same insight in different industries should produce
near-identical sentences, and that is the point. A driver written vaguely to dodge the similarity
check defeats the only part of the system that sees mechanism, so the test of a good one is whether
the author, reading it cold, could name the move.

```
weak    The analysis has to account for an important constraint in the data.
strong  The decisive quantity is a per-unit floor recovered from a closed corpus of past
        determinations, and applying it removes the largest naive candidates from the total.
```

`lineage` carries every architecture the slot has been through, each with its own driver and its
fate. Retired drivers stay in the corpus on purpose: a driver the portal already solved is the
worst thing to draw again, in this slot or any other.

## Part 2. The procedure

**1. Before choosing the pairing** (`guide-to-prompt` steps 1 and 2):

```
python3 .claude/skills/fingerprint/guard.py recent      # the last builds, one line each
python3 .claude/skills/fingerprint/guard.py coverage    # what is spent and what has never been drawn
python3 .claude/skills/fingerprint/guard.py suggest     # optional: independent draws into fresh territory
```

`coverage` prints the domain by objective grid with the never-built cells, the never-drawn
subdomains, and the use of every other axis over the whole corpus and over the last twelve. Read
it before you choose, because the pairing is the cheapest thing in the build to change. `suggest`
samples each dimension independently, weighted toward what has been used least and never breaking
a standing ban; take it as a starting point, never as the decision.

**2. When the draw is fixed** (`stumping` Part 6.1, before the ladder is written):

```
python3 .claude/skills/fingerprint/guard.py new task98 > <scratchpad>/task98_card.json
#   fill it from the design note's DRAW block, including the driver and the stump sentence
python3 .claude/skills/fingerprint/guard.py check <scratchpad>/task98_card.json
python3 .claude/skills/fingerprint/guard.py register <scratchpad>/task98_card.json
```

Clear every BLOCK by redrawing the axis it names. Answer every WARN in one line in the design note,
because a WARN is a reviewer's eyebrow, not a pass. `register` runs the check again and refuses a
card that still carries a BLOCK; `--force` exists for the author's explicit override and needs the
reason in the card's `notes`. The card goes into `cards/` before the ladder exists, so the next
build drawn sees this one even while it is in flight.

**3. When a build is re-rooted**, move the old architecture's identity into `lineage` with its
fate, write the new draw into the main fields, and check and register again. The guard compares the
new draw with the slot's own lineage too, and blocks a re-root that lands back on the puzzle it was
meant to replace.

**4. After the pack is cut** (`dataset-generation` §13):

```
python3 .claude/skills/fingerprint/guard.py surface task98
```

This runs `clone-check/fingerprint.py`'s mechanical screen focused on the build: byte-identical
files, same-seed tables that survived a rename, identical column sets, shared invented names and
masked prompt wording, each ranked against how similar the corpus normally is. A promoted pair is a
rename or a regeneration before the bundle is called ready.

**4b. When the author types `/approve`**, `guard.py heart taskNN` compares the card's `driver`,
`driver_concrete` and `stump` text with every card's driver, every lineage driver, every card's
stump and every shipped-ledger row, then runs the full check. It is the cheap half of
`/clone-check` and exits 1 on BLOCK, so a template or duplicate is caught before a solver round is
paid for. A card with an empty `stump` cannot be checked and is filled from the design note first.

**5. When the submission is final**, update the card's `answer`, `answer_source`, `spine.rows`,
`deliverables` and `opening_move` so the corpus stays true. That is part of delivering the build,
not bookkeeping, because the next draw is checked against it.

**6. When the author reports the portal result**, write the ledger row (the ledger's own "Adding a
row" section). The card is not touched, because it never recorded an outcome.

## Part 3. What the guard decides, and where each rule comes from

The verdict is **BLOCK** if any rule blocks, **WARN** if any warns, otherwise **PASS**. Exit status
is 1 on BLOCK, so the check can sit in a script.

| Rule | Level | Against | Source |
|---|---|---|---|
| `legal.domain`, `legal.objective` | BLOCK | the nine domains and the eight objectives | the spec |
| `legal.gate_g` | BLOCK | surface-read rejection, or `statistical_rigor` alone | Gate G v3 |
| `ban.pairing` | BLOCK | domain plus objective, last three builds | Part 6.1 |
| `ban.subdomain` | BLOCK | domain and subdomain both, last three | Part 6.1 draw table |
| `ban.pattern` | BLOCK | the decisive pattern (or decisive G-code), last three | Part 6.1 |
| `ban.calibration` | BLOCK | calibration form, last three | Part 6.1 |
| `ban.role`, `ban.artifact` | BLOCK | role family, context-artifact type, last three | Part 6.1 |
| `ban.spine` | BLOCK | spine entity and grain, last three | Part 6.1, `dataset-generation` §13 |
| `ban.source` | BLOCK, else WARN | the same real source dataset, last three, else anywhere | `dataset-generation` §13 |
| `ban.shape` | BLOCK | prompt shape, last two | `clone-check` Part 1 |
| `test.same_puzzle` | BLOCK | gap, pattern and decision type all equal, last twelve, lineage included | Part 6.1 similarity test |
| `test.same_puzzle_older` | BLOCK unless differentiated | the same, older than twelve | Part 6.1 similarity test |
| `test.same_driver` | BLOCK | gap, pattern and Gate G mechanism all equal, last twelve, lineage included | `clone-check` Template tier |
| `test.same_driver_older` | BLOCK unless differentiated | the same, older than twelve | `clone-check` Template tier |
| `test.own_lineage` | BLOCK unless differentiated | the slot's own earlier architectures | re-roots |
| `driver.text` | BLOCK unless differentiated | driver similarity at or above 0.30, every driver on file | `clone-check` Track B |
| `driver.near` | WARN | driver similarity 0.12 to 0.30 | `clone-check` Part 5 |
| `tell.names` | BLOCK | a shared multi-word invented name | `clone-check` hard tells |
| `people.full` | BLOCK | a persona's full name used in any other build | the name audit, Part 3b |
| `people.first` | BLOCK, else WARN | a first name in 3 or more builds or any of the last twelve, else in one older build | the name audit, Part 3b |
| `people.last` | BLOCK, else WARN | a surname in 2 or more builds or any of the last twelve, else in one older build | the name audit, Part 3b |
| `people.inside` | BLOCK | two personas in one build sharing a first name or a surname | the name audit, Part 3b |
| `ban.forum`, `ban.forcing_event`, `ban.org_family` | BLOCK | the same forum, forcing event or organisation family as any of the last three | the business-furniture audit, Part 3b |
| `overuse.forum`, `overuse.forcing_event`, `overuse.org_family` | WARN | a forum, event or organisation family already spent across the corpus | the business-furniture audit, Part 3b |
| `overuse.*`, `repeat.*` | WARN | domain, objective, shape, Gate G, decision type, deliverable set, PDF share, opening move, geography, niche | the client's voice note, Part 6.1 |

**Why the bans reach three builds and not one.** Part 6.1 writes them against "your last build",
and builds here are routinely drawn two or three at a time, so the last build is not the only one a
reviewer reads beside this one. Three is the batch a reviewer holds as neighbours; twelve is the
batch they read in one sitting, which is where `voice-check.py` measures too.

**Why there are two structural tests.** Part 6.1's similarity test reads gap, pattern and decision
type. The one Template clone on record (task86 v1 against task72 v2) shared the gap, the pattern and
the Gate G mechanism and differed only in how the decision was cut, a quantity against a pick, so
that test let it through. `test.same_driver` reads gap, pattern and Gate G mechanism and blocks it.
Across the corpus each test collides on under 4 per cent of card pairs, and `suggest` never
proposes a signature either test would block. When a signature is spent in many earlier builds the
guard says so, because redrawing the gap or the pattern is cheaper than a page of differentiation.

**Why a differentiation can clear some blocks and not others.** The axis bans are cheap to honour
at draw time, so they never take an override. The similarity rules compare free text and a
structural signature, and two builds can share both and still turn on different insights, which
`clone-check` Part 1 is explicit about. There the guard asks for the one line that names the
difference, and a line that cannot be written is the finding.

## Part 3b. People and business furniture

**Personas are drawn, never typed.** One first name stood in 23 builds (one full name in 13),
because a model asked to invent a colleague reaches for the same few names. So every persona
comes from `guard.py names --geo <the build's geography> --seed <task number>`, which draws from that
locale's own Faker name pool and skips anything the check would block. The rule is ordinary names
that are not recycled, not rare ones: a first name may recur across the corpus as names do in real
offices, but never in a recent build, never in three builds, and never as the same full name. The
names go in `world.people` at the draw, and `guard.py surface` re-reads the cut pack afterwards,
because a generator writes names the card never planned.

**The furniture around the decision repeats as badly as the mechanism did.** A committee or panel
decided the call in 28 prompts and a board in 21, while a regulator, a minister, a funder, a line
manager and an operations desk never decided one. Government agencies and retailers are the
organisation in 37 builds. So `forum`, `forcing_event` and `org_family` are drawn like any other
axis, banned against the last three builds and warned on when spent across the corpus. Where a
card does not declare them, the guard reads them off the build's prompt with phrase rules, which is
approximate, so every card declares all three and the bans rely on the declared fields.

**The pack's file names are furniture too.** `data_dictionary.md` sits in 62 builds and
`export_manifest.csv` in 34. The dictionary and the provenance record are required content; their
file names are not, so name them the way the organisation in the build would.

## Part 4. How this goes wrong

**A PASS read as "not a clone".** The guard is necessary and not sufficient. It sees what the card
says, and the similarity test in Part 6.1 still has to be answered in writing in the design note.

**A card written to pass.** Choosing the vocabulary key that dodges a ban while the build is the
same build is the failure the whole system exists to stop, and it fools nobody but the script. If
two keys fit, use the one a reviewer would use.

**A vague driver.** See Part 1. A driver that names no quantity and no source is a driver nobody can
compare, including the guard.

**A stale card.** A card that still describes a retired architecture is worse than a missing one,
because the bans run against it and pass. Re-root means rewrite the card in the same edit.

**Vocabulary drift.** A new value added to `vocab.json` because nothing seemed to fit splits one
choice across two strings and the collision disappears. Add a value only when no existing one is
honest, and say why in the card's `notes`. The opposite failure is a forced key: a value that is not
true makes a collision that is not real. `calibration_forms` and `context_artifacts` carry an `other`
for that case, which never counts as a collision, and the card's notes name what it actually is.

**A mechanism family offered on its label.** A Gate G mechanism or generator that `coverage` lists as never drawn
can still have been tried, and solved, in lineage. When `check` names the architectures a candidate collides with, read
their fates in the cards before offering that family to the author: confirm_surface_read showed zero main-field uses
while four lineage architectures had tried it and all four were solved (task107's screen, Tried and rejected).

**Forgetting to register.** An unfiled card protects nobody. `register` is the step that makes the
build visible.

## Part 5. Maintenance

`guard.py validate` checks every card against `vocab.json` and exits non-zero on any error; run it
after editing a card or the vocabulary. Cards are plain JSON and are edited in place, and like
everything else in this repo they are never versioned or backed up inside the repo.

The driver thresholds are calibrated on the corpus. Across pairs of
drivers from different slots the 99.9th percentile sat under 0.10, the highest pair that was not
the same build sat under 0.20, and the one byte-identical rebuild on disk (task90, built as task86
v1) scored 0.88 against its original. Text similarity separates same-mechanism pairs from unrelated
ones only weakly (an AUC of about 0.6), which is why it is a near-duplicate catcher and the
mechanism check is the structural signature in `test.same_puzzle`. Recalibrate with
`guard.py nearest taskNN` across a few known pairs if the corpus or the way drivers are written
changes.

**How this relates to the other records.** `clone-check` adjudicates whether two builds are the
same task and is author-triggered, because it spends real tokens; its mechanical screen is what
`guard.py surface` runs, and its adjudicators read the cards first because they carry the mechanism
layer in one vocabulary. The shipped ledger records outcomes and the lessons each build paid for.
The design note records the build's own reasoning and its `## Tried and rejected` section. The card
is the one record that exists for every build on disk, in one vocabulary, from the moment the draw
is fixed.

**Backfilled cards.** A card not filed at draw time is extracted from the build folder's prompt,
submission, design note and target, and reconciled against the shipped ledger. For builds up to
task36 the gap and pattern labels were fitted after the fact (accurate about the
mechanism, approximate about the label), and builds with no design note and no ledger row carry an
empty gap and pattern with `mechanism_source: submission_only`, because a mechanism inferred from a
prompt is a guess.
