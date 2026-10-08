---
name: determinism-check
description: "Force one answer while the build is being designed, assert it while the generator is written, and check the finished build against the judge's gates (A to E determinism, F stump power, G stumping type). Direct rules only; the evidence behind them is in references/forcing-the-answer.md (the 22-axis convention inventory, the four closure moves, the bin arithmetic, the eight ways determinism is lost). Also carries the judge rehearsal, spawned only when the author asks or when the /build pipeline reaches stage 6. Invoke three times per build: at the ladder, at the generator, at the end; and again when a build comes back NOT_DETERMINISTIC or SEND_BACK."
---

# Determinism

> Builds here do not fail determinism on arithmetic. They fail because a competent solver did the
> analysis correctly and landed somewhere else, on a choice the author never noticed was a choice:
> 31 `underspecified_objective` findings across 18 builds against 2 `solution_incorrect`. Every one
> of those builds had a verifier. A verifier asserts the forks somebody enumerated, so the work is
> the enumeration, and it happens before the data is cut.

The judge's own system prompt is `guidelines/determinism_judge_system_prompt.md` (v3); read it when
a verdict is contested. `references/forcing-the-answer.md` is the evidence for every rule below.

## A. While the ladder is designed

1. **Answer the litmus in writing, first.** *Is the reported number or conclusion the task overturns
   actually wrong, and is catching that the main thing that defeats the model?* Yes to both is
   banned (surface-read rejection, at any depth). The reported figures stay correct and the
   difficulty lives elsewhere.
2. **Name the primary mechanism** from the pass list: `forecasting`, `method_or_model_selection`,
   `binding_constraint`, `decomposition_attribution`, `signal_vs_noise_or_hold`,
   `confirm_surface_read`, `etl_conformance`. Never `planted_defect_flip` or
   `single_conceptual_flip`. `statistical_rigor` only paired with one of the seven.
3. **Write the three flags into the design note**: `surface_read_dependency: no`,
   `stumping_family: analytical_non_defect` (or `mixed` with the independent layer named),
   `sole_data_defect: no`. Flags are claims; section B asserts them.
4. **Ship no artifact that ranks the candidates on the decision question and gets it wrong.** A
   past-quantity ranking is legal only if it is correct about the past and labelled in-file for the
   question it answers. The one exception to the rule is the declared distractor (`dataset-generation` §8.3): wrong on a basis a shipped fact rules out, named in `metadata.json`, and never the stump. Assert that its answer is neither the correct answer nor the decoy.
5. **Walk the 22 axes** in `forcing-the-answer.md` Part 1 and write one line per axis in the design
   note: the reading chosen and which closure move closed it.
   - **C1 converge**: build the records so every reasonable reading selects the same rows and the
     same figure (the strongest close; assert on the figure and on the row and entity counts).
   - **C2 corpus recovery**: the rule is the unique survivor of a back-test over a closed corpus;
     state the family size, N of N, and every rival's worst miss.
   - **C3 corridor**: the parameter is unrecoverable and irrelevant, with the answer identical across
     its whole admissible range.
   - **C4 grid separation**: every cell of the fork grid computed, each mapped to the shipped rule
     it violates, and the nearest wrong cell at least 6 per cent from the answer (under that, the
     two-opposite-violations argument).
   An axis that cannot move the answer today still gets a line; it becomes load-bearing when
   another parameter moves.
6. **Centre every graded figure in its rounding bin, never on the round value.** State the flip
   condition as a number. A figure tuned to land at 24.8000 is a receipt: task100's in-house solver
   wrote "the composites land within 0.001 of round one-decimal values, which points to the intended
   method". Tune to a non-round position inside the bin (24.8371) with the same margin to the edges.
7. **Pin conventions in a filed document, once, stated as a rule and never argued.** A convention a
   competent analyst could reverse is a fork; the write-up pins nothing.
8. **Decision pinned, method not.** One committed call for the main ask, one determinate answer per
   supplementary figure, no bundled asks, unit and rounding inside the sentence. A hold is a call.
9. **No decision metric asserted in the prompt's own voice that a shipped file contradicts**; demote
   it to an attributed claim so the filed policy governs.
10. **Write the stump sentence**: the wrong committed answer a competent solver files and the step
    that lands them there. No sentence, no stump, no build.

## B. While the generator is written

Assert, do not state. Each of these is an assertion in the generator and a check in an independent
verifier that reads only the shipped bytes on a code path sharing nothing with the generator.

- every C1 convergence as an equality on the figure and on the row and entity counts
- the C2 back-test: survivor N of N, family size, every rival's miss count and worst miss
- the C3 corridor's bounds and the answer's constancy across it
- every C4 grid cell, its violated rule, and the nearest cell's distance
- every graded figure's distance to its bin boundary
- **the clean-data test, once per suspect file** (incomplete, stale, superseded, delta-shaped or
  filtered): repair the file in the generator and assert `answer(repaired) == answer(shipped)`,
  `naive(repaired) == naive(shipped)`, `answer != naive`. Failing either equality makes
  `sole_data_defect` yes whatever the note says.
- **the lens-swap test, separately**: the naive read and the answer are not the same population at
  the same moment under two lenses; if they are, the mechanism is `single_conceptual_flip`.
- file grain honoured wherever a rate, average or roll-up runs (a delta feed is reconstructed into a
  panel before any rate)
- the input gates: 10 or more files, 3 or more formats, a file of 25,000 or more rows in any format, or a large database file, at
  least one distractor (no more than 20 per cent of files) named in `metadata.json`, 1 to 3
  deliverables, every ask with unit and rounding
- two consecutive builds byte-identical

## C. When the build is finished

Run the gates in this order; each is one question.

| Gate | The question | Fails as |
|---|---|---|
| G | Does the difficulty survive deleting every wrong number from the pack, and is it not a lens swap? | SEND_BACK, rebuild |
| A | Does every figure (call, components, steps, every supplementary answer) recompute from the shipped files alone, at the file's own grain, attributed to the right party and period? | `solution_incorrect` |
| B | Is every decisive fact in a shipped file, and does every distinctive term in the recommendation occur in some input (grep every format, tables included)? Never repair by adding vocabulary to an input afterwards. | missing input |
| C | Does any answer flip under a reasonable definition, threshold, scope, inclusion rule, window or rounding path the pack does not pin? Enumerate the rivals and defeat each. A thin margin is fine when clean; thin and contested is not. | `underspecified_objective` |
| D | Would rigorous solvers disagree because they read a term differently rather than analysed differently? | `semantic_fork` |
| E | Is the decision pinned, the method open, every ask single and precise? | hedge, bundled ask |
| F | Can the stump sentence be written, and is the ask layer holding both top responses to about a fifth of the ask weight (`supplemental-stumping` Part 0)? The bar is the top two averaging under 50 with one genuinely stumped; build to 40. | too easy |

Then the spec gates (section B's list), `leak-check`, and `golden-realism` after the figures are
frozen.

## D. The judge rehearsal

An isolated thread that sees the prompt, the unzipped bundle and the submission's graded blocks,
and nothing else: not the design note, the generator or any verifier. It recomputes every
load-bearing figure and returns a verdict (DETERMINISTIC or NOT_DETERMINISTIC), a disposition
(APPROVE, FIX_NOW, SEND_BACK) and the Gate G line.

**It runs when the author asks in their own words, or when `/build` reaches stage 6.** Nothing
else licenses it: not a finished build, not a patch that seems to want validation.

1. Resolve the task to an absolute folder; if none is named, ask and stop.
2. Spawn the `determinism-judge` agent once, `subagent_type: determinism-judge`, stating that the
   author asked through this skill (or that `/build` stage 6 reached it) and giving the path. If a
   `determinism_check_report.md` exists, name the pass number so the new report is numbered.
3. Relay the verdict, the disposition, the Gate G line and the report path. Do not fix, soften or
   re-run. Run it again only after a change that moves a graded number.

## Checklist

- [ ] Litmus answered in writing; mechanism from the pass list; three flags in the design note
- [ ] No shipped artifact ranks the candidates on the decision question, the declared distractor excepted
- [ ] 22 axes walked, one closure move per axis, in the design note
- [ ] Every convergence, back-test, corridor, grid cell and bin distance asserted in the generator and checked in the independent verifier
- [ ] Clean-data test and lens-swap test asserted, once per suspect file
- [ ] Every figure in the submission recomputes from `target/`, supplementary answers included
- [ ] Every distinctive term of the recommendation grepped in every input format, with hits
- [ ] Rivals enumerated and defeated for the main ask and every supplementary figure
- [ ] Stump sentence written; ask layer sized to the pair ceiling
- [ ] Spec gates green; `leak.py` not LEAK; goldens through `golden-realism` after figures froze
