> ## BAR UPDATE (2026-09-05), OPERATIVE, supersedes the 2026-08-27 block below and the criteria under it
>
> **The bar is the top two responses averaging under 70 per cent, with at least one model genuinely
> stumped.** The threshold moved from 50 to 70; the **top-two structure never went away**, and the
> two conditions are conjunctive. The *all-models* stump of the original criteria stays retired, but
> one genuine stump is back as a pass condition in its own right.
>
> **Build to 60, not to 70.** The client's own reason: the on-platform verifiers are not perfectly
> accurate and the task is **regraded more accurately after submission**, so a build measuring 68 can
> regrade past the bar after work has stopped.
>
> **The golden deliverables must look business-realistic.** This is now a stated send-back cause: a
> golden that reads as overly LLM-generated is returned even when every figure is correct. Using an
> LLM to help is fine, shipping its first draft is not. See `../.claude/skills/golden-realism/`.
>
> **Deliverables are one to three, and three is the ceiling.** The 2026-08-27 floor of three
> reversed: a four-file build is now a spec failure. No format family is assigned. Pick the files
> a real analyst would actually produce for this decision, and prioritize a visual wherever it
> makes the call read at a glance. A table can live inside a memo rather than take a slot.
>
> **The asks are uncapped and untargeted, and each has to be multi-dimensional and hard.** The
> three-asks-per-file floor is retired. One ask can span many rows, periods or cuts and still
> resolve to one defensible answer.
>
> **The prompt is prose, first person**, the way you would write to a colleague, not a bulleted
> spec. The bracketed deliverable headers and bulleted asks are retired.
>
> **The rubric is still generated for you and still must reach 25 or more criteria**, but it now
> gets there through the **prompt shape**, the structure of the answer, rather than through a long
> list of asks (`rubric.md`, `prompt_guide.md`). Weights moved to 30 to 40 per cent recommendation,
> 5 to 10 instruction-following, about 55 on the asks.
>
> **The input gates are unchanged**: 10 or more files, 3 or more distinct formats, at least one
> file over 10,000 rows, real license-clean data with source, date and license recorded, nothing
> LLM generated. The six domains and six objectives are unchanged.

> ## BAR UPDATE (2026-08-27), SUPERSEDED by the 2026-09-05 block above, retained for reference
>
> Three of the criteria below changed. **The stump bar is retired**: a task now passes when the
> top two of twelve model responses average under 50 percent against the generated rubric, and
> the bottom ten are submitted without checking. **The rubric is generated for you** from the
> prompt, the golden and the requested files, you no longer write or edit it, and it must reach
> 25 or more criteria before the task can advance (`rubric.md`). **The input gates are the
> 2026-08-20 ones, not the ones below**: 10 or more files, 3 or more distinct formats, at least
> one file over 10,000 rows, real license-clean data with source, date and license recorded,
> nothing LLM generated. Deliverables are three or more, across the two format families assigned
> per task, each carrying at least three asks (`prompt_guide.md`). Everything else below stands.

Welcome to project mark
As a fellow, you'll craft tough, open-ended analytical challenges built on messy, multi-file datasets. Each task should push models through the full reasoning loop, exploring, hypothesizing, analyzing, and synthesizing, until they land on a single, pre-verified recommendation you can score cleanly with a weighted binary rubric.

Approval criteria
How your task gets approved
Every submission is reviewed within 24 hours. To be approved, it has to clear all of the following.
It stumps the models
At the very end, at least 2 of Responses 1 to 4 and at least 1 of Responses 5 to 8 must land on a meaningfully different answer.
The solution is deterministic
One unambiguous conclusion that domain experts would independently agree on.
The stump is analytical, not semantic
The model must fail on methodology and analytical reasoning, never on vague wording or a trick definition.
The golden solution is correct
Every number and step must be reproducible from the prompt and the shipped input files.
The input files clear the bar
6 or more files, a variety of formats, and nothing LLM generated.
The prompt is original
It cannot closely resemble another fellow's task or one you have already submitted.

Goal
What you're building
Generate a prompt-and-dataset pair that, in essence, is an ambiguous prompt paired with messy data. The data conceals "secrets" that point to a single, correct answer, one that only surfaces when a skilled data analyst or domain expert cleans, manipulates, and runs complex calculations on it. The answer must be deterministic and hard enough to stump frontier models.
Specifically, the pair should have these properties:
Ambiguous prompt
The ask isn't obvious on the surface and requires interpretation.
Messy data
The dataset hides the path to the answer, so it must be cleaned, transformed, and analyzed to be usable.
Single deterministic answer
There is exactly one correct result, reachable only through careful analysis, and reproducible every time.
Hard enough to stump frontier models
A strong LLM should fail it without genuine analytical skill and domain expertise. The bar: at the very end, at least 2 of Responses 1 to 4 and at least 1 of Responses 5 to 8 get a meaningfully different answer.