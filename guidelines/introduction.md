> ## 10/10 UPDATES (2026-10-10), OPERATIVE: three rules for how every task is built and reviewed
>
> From October 10, every task is built and reviewed against three rules. They exist for one reason:
> tasks are training data, and a task is only useful if getting it right teaches a model something real.
>
> **The three rules in one line each.** (1) Your task must actually use its assigned domain, not just
> borrow its vocabulary. (2) Every task has two layers: realistic messy data, and real analytical rigor
> that decides the answer. (3) Planted traps, data semantics and rule application can appear in a task,
> but none of them can be the decisive stump.
>
> **1. Your task must really use its domain.** Every task is assigned a domain and secondary domain. The
> task must do the kind of analysis that domain is about, close to one of its task types on the client's
> Domains page. The domain cannot just be the setting or backdrop for a generic question. Two example
> prompts for every task type are on the client's Example prompts page. A quick test: swap the nouns to
> another field ("hospital" for "school", "megawatt-hours" for "visits"). If the task reads exactly the
> same, the domain is only a backdrop.
>
> - Good. Quantitative Finance, alpha research: "Our researcher found a sentiment signal with a strong
>   backtest. Decide whether to allocate capital to it, using a cost-adjusted, factor-neutral Sharpe ratio
>   over 2015 to 2024, measured point in time." Validating a return signal is the core work of alpha research.
> - Bad. Energy Systems and Utilities, as a backdrop: "Which three substations get the upgrade grant,
>   ranked by the score in the grant rules?" The answer comes from applying a stated score. Swap in
>   "schools" and the task reads the same, so energy is only the setting.
> - Good. Biomedical and Clinical Research, survival analysis: "Decide whether the new maintenance regimen
>   lengthens time to relapse, measuring from randomization to relapse, with patients who leave the study
>   treated as censored." Time-to-event analysis with censoring is the core work of survival analysis.
> - Bad. Epidemiology and Public Health, as a backdrop: "Which clinics qualify for the outreach fund under
>   the eligibility criteria?" This is checking criteria against a list. No epidemiological analysis,
>   such as a risk, a rate comparison or an outbreak signal, decides the answer.
>
> A decision framing like "which clinics" is fine. What matters is whether the quantity that decides it
> is something the field would estimate, model or test.
>
> **2. Every task has two layers.** Layer 1, messy data: the data should be hard to use for the reasons
> real data is hard to use. It complicates the problem and can help stump the model, but it must be
> realistic, with no planted defects or decoys: files whose layout changes across years, or tables inside
> PDFs that must be extracted; joins across sources with imperfect keys, like codes in one file and names
> in another; a preliminary release and a revised release that overlap, so you must decide which to use;
> fiscal and calendar years mixed, local time and UTC mixed, or values in thousands in one file and units
> in another. Layer 2, analytical rigor decides the answer: the recommendation turns on doing the
> analysis correctly, the kind of choice an expert in the field would recognize, where a capable analyst
> taking the easy route gets the wrong answer: comparing against the right group (in a staggered rollout,
> comparing each wave against units not yet treated, not a simple before and after); handling the data's
> real structure (estimating time to an event while accounting for people who left the study early);
> judging the evidence (reading a guardrail metric with a confidence interval, not only "it was not
> significant"); validating a forecast properly (testing it only on data it was not built on).
>
> **3. Three kinds of stump are banned as the decisive stump.** These can appear in your task, because
> real tasks always involve some field reading and rule following, but none of them can be what decides
> the answer. Something genuinely analytical must still stand between the solver and the right answer. A
> task decided by one of these is sent back, even if it is deterministic and correct.
>
> - Planted defects, decoys and hidden rules: something inserted only so that catching it flips the
>   answer. A block of hourly readings secretly copied from the week before, so finding the copy is what
>   changes the ranking; a staff memo written to argue for the wrong answer, where rejecting the memo is
>   what decides the call.
> - Data semantics: the answer flips only on reading a field, code, unit or definition correctly. The
>   answer flips only once you notice the school capacity column also counts preschool seats; the answer
>   flips only once you read that a rainfall column holds multi-day totals, not daily values.
> - Rule application: the answer comes from applying stated rules correctly, however many steps there
>   are. Ranking programs by checking six listed eligibility criteria and applying a stated score;
>   working out which company held a license on a given date by following the transfer records.
>
> **The test.** Could a strong analyst who cleaned the data and read every rule correctly still get the
> answer wrong by doing the analysis the easy way? If yes, your stump is analytical and valid. If no, it
> is semantics or rule application. Choosing the right estimand or unit of analysis counts as analysis.
>
> Where this lives in the working standard: `../CLAUDE.md` (Current spec),
> `../.claude/skills/stumping/SKILL.md` Part 1 (the three rules) and
> `../.claude/skills/stumping/references/client/two-layer-task-design.md`, `../.claude/skills/guide-to-prompt/SKILL.md`
> Step 1 (the swap test), the judge's Gate H in `determinism_judge_system_prompt.md`, and the card fields
> `stump_class`, `analyst_test` and `domain_test` that `../.claude/skills/fingerprint/guard.py` requires.

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