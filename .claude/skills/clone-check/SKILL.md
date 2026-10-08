---
name: clone-check
description: Decide whether a finished build is a clone of one already shipped, the way the final_verdict reviewer decides it. Carries the discrimination the check turns on (reusing a proven component is legitimate, reusing the thing that drives the stump is not, and the prompt shape is a component), the two tracks a finding can land in and why they carry different severity, the tier ladder, and the ways the check itself gives a wrong answer. Use when asked for a clone check, a template check or a duplicate check, when a batch is about to be submitted, and as a pre-flight on a build whose draw is fixed but whose data is not yet cut.
---

# Clone check

> Two builds are not the same task because they share a device. They are the same task
> when the thing a solver has to see is the same thing.

## Part 0. What this is for

A reviewer at final_verdict fingerprints a package against everything already delivered and
excludes it on a hit, and the client has already said in writing that these builds were reading
as templated. So the question this skill answers is not whether two tasks look alike. It is
whether a reviewer holding both of them would say the second one taught them nothing the first
one had not already taught them, and that is a question about the driving force, not about the
surface.

The check runs against the corpus of previous builds and reports what a reviewer would find, at
the severity a reviewer would attach. It never repairs anything. A clone finding is answered by
redrawing, and the redraw belongs to the author.

## Part 1. The discrimination the whole check turns on

**Reusing a component is legitimate. Reusing the driver is not.** A trap device that has proven
it works is an asset and it is meant to be spent again, so a build that carries a device already
seen in three prior builds is not thereby a clone. What cannot repeat is the thing the stump
actually rides on, the single insight a solver has to reach and keeps failing to reach, because
that is the only part of a build a reviewer remembers and the only part a solver can be primed
against.

So a path that runs through familiar moves in an unfamiliar order, with an unfamiliar move
carrying the decisive step, is a new task. A path that runs through unfamiliar moves in an
unfamiliar order but arrives at the same decisive insight is the old task in new clothes, and it
is the second one that gets excluded. This is why the check cannot be a similarity score. A
similarity score ranks the first case above the second, and it has the answer exactly backwards.

**The prompt shape is a component, not a driver.** The client's example library is organized by
prompt shape (a ranked list under a cap, a bridge between two totals, a grid of cells, a forecast
across many periods, `guide-to-prompt/references/shapes/`), and the shape is where the generated
rubric's 25 criteria come from. It is therefore going to repeat across a
batch, and that repetition is legitimate on its own: two builds can both be a ranked list under a
cap the way two builds can both carry a duplicate-key device. What cannot repeat is the **driver**,
the insight the ranking, the bridge or the grid is hiding. Score a shared shape as a Track A
surface finding, and only escalate when the shared shape carries the same decisive rung in both.

The reason to say this out loud is that the shape is unusually visible: it shows in the prompt's
own wording and in the deliverable structure, so a reviewer reads it immediately, and a batch that
draws the same shape four times reads as templated even when every driver is different. Vary the
shape across a batch for the same reason you vary the domain, and check it in the pre-flight while
the draw is still cheap to change.

**Read the position, not the inventory.** When two builds share moves, ask where each shared move
sits. A device that carried the decisive rung in one build and sits at rung 1 in the other has
been demoted, and demotion is real work, so that is reuse rather than cloning. A device that
carried the decisive rung in both is spent twice, and no amount of surface distance repairs it.

## Part 2. Two tracks, because the repairs are different

A finding lands in one of two places and the two are not comparable, so they are never merged
into one score.

**Track A is what a reviewer can see.** Prompt wording and sentence construction, target file
names, schemas, row counts, the values themselves, invented names and dated windows, the
deliverable species, and the phrasing of the write-up. These are what the cross-batch check
actually fingerprints, and a Track A hit against a delivered task is exclusion level on its own,
whatever the mechanism underneath is doing. The repair is cosmetic in the sense that it does not
touch the ladder, but it is not optional.

> **Run `../guide-to-prompt/references/voice-check.py` bare before adjudicating Track A on a
> batch.** It measures the surface this track is about: opening moves, calcified carrier phrases,
> unlisted repeated word runs, prompt length, file count and format mix. The division of labour is
> that the script **measures** the surface and this skill **adjudicates** whether a repeat is a
> clone, and the two need each other, because a monoculture spread thinly across a batch is
> invisible pair by pair and obvious in the counts. The client's note on voice landed exactly
> there: no two prompts were clones of each other, and all eighteen shared one skeleton.
> `../guide-to-prompt/references/prompt-voice.md` carries what to do about a finding.

**Track B is the mechanism.** The gap, the pattern, the decisive rung, the calibration form, the
decision family. These are the author's draw discipline, and a Track B hit means the draw did not
do its job. The repair is a redraw, and a redraw usually invalidates the data, so a Track B
finding is far more expensive to answer and far more important to catch early.

A pair can hit one track and not the other, and the interesting pairs usually do. A build with a
fully reskinned surface and a repeated driver scores near zero on every mechanical axis, which is
why the mechanism axes are checked on their own and never gated behind a surface threshold. That
pair is the worst case and the check has to reach it.

## Part 3. The tiers, and what each one costs

Ordered by what the finding costs to answer, not by how much text the two builds share.

**Exact.** The artifacts are the same artifacts. Nothing to discuss.

**Same seed.** The surface has been renamed and reskinned but the underlying values are the
generated output of the same run, which is visible in row counts, column sets and the numeric
content of the tables surviving a rename. A reviewer who compares two packages closely finds this
one, and it reads as worse than a template because it looks like an attempt to hide.

**Dataset.** The spine dataset, or its schema, carries both builds. Part 6.1 already bans this
between consecutive builds, and the ban exists because the data is where most of the build cost
sits, so reusing it is the temptation the draw is meant to defeat.

**Template.** The driver is the same. The gap, the pattern and the decisive rung line up, whatever
the domain and the names are doing. This is the tier the client's feedback was about and it is the
one this skill exists to catch, and it is also the only tier that survives an author rewriting
every noun in the package.

**Shape echo.** The mechanism differs but the build is recognisable from its outline, so the ask
sentence is built the same way, the deliverable pair is the same species, the decision has the
same shape and the calibration form is the same organ. No single one of these is a finding.
Several of them together are the thing Part 6.1 means by a task recognisable from its shape, and
that is a soft flag rather than an exclusion.

**Idiom.** The author's habits, visible across the whole corpus rather than in any pair, so a file
role that appears in most builds under the same name, a construction the ask sentence keeps
reaching for, a deliverable pairing that never varies. A reviewer holding one package cannot see
this and a reviewer holding a batch sees nothing else, which is why it is checked corpus wide and
reported separately from the pairs.

**Clean, shares components by design.** This is a verdict and not an absence of one. Say it
explicitly when two builds share devices and the drivers differ, because an author who is told
only about hits learns to read every shared device as a problem, and then stops reusing what
works.

## Part 4. Evidence that is not there

Half of any corpus predates whatever vocabulary the check is written in, and older builds carry no
private design note, so the mechanism is genuinely unavailable for them rather than merely
undiscovered. Where the labels were fitted after the fact they are accurate about what the build
did and approximate about what it was called, so two builds sharing a back-fitted label share a
guess, not a mechanism.

**Read the fingerprint cards first** (`../fingerprint/cards/`). Every build on disk has one, in
a controlled vocabulary, with the driver written as one sentence with the domain nouns stripped,
and a card with `mechanism_source: submission_only` is the honest marker of a build whose
mechanism was never recorded. The mechanical screen scores Track B from the cards wherever both
builds have them.

State the gap and stop. A label inferred from a prompt, or a driver reconstructed from a
submission, is a fabrication with a confident tone, and a fabricated Track B collision is worse
than a missing one because it sends the author to redraw a build that was fine. Where the
mechanism cannot be read, the honest report says the pair was checked on Track A only.

## Part 5. How this check gives a wrong answer

**It flags legitimate reuse.** Most common by far, because shared surface is easy to measure and
shared drivers are not, so the check drifts toward reporting proximity. Proximity is not a
finding. If the write up cannot name the shared decisive move in one sentence, there is no
Template finding, and saying so is the correct output.

**It misses the reskin.** The case the check exists for is the one with no surface signal at all,
and any design that reaches the mechanism only after a surface threshold has already failed. The
mechanism axes get their own independent route to adjudication or the check is decorative.

**It scores instead of deciding.** A number is triage. It says which pairs are worth a person's
attention and it never says what they are. The verdict comes from reading both builds and naming
what they share, and a verdict quoted as a similarity figure has skipped the only step that
mattered.

**It treats the corpus as flat.** A collision against an approved and delivered build is the
exclusion. A collision against a build that failed, or was retired, or is one of several rows for
a single task number, is a different thing entirely, and the last of those is not a finding at all
because a build cannot clone its own ancestor.

## Part 6. What a finding has to carry

A finding that does not name the shared driver in one sentence is not a finding, it is an
observation about two files. Every reported hit carries the tier, the track, the two builds, the
specific thing they share stated as a mechanism rather than as a score, the delivery status of
both sides, and the one axis the author should redraw to clear it. Where the finding is Track A
only, say so, because the repair is a rename and not a rebuild, and telling an author to redraw a
ladder over a shared file name burns a week for nothing.
