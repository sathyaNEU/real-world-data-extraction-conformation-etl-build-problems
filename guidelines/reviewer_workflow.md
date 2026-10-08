Reviewer checklist
This page is for reviewers. It assumes you already know general Project Mark principles and focuses on how to run a review: what to reproduce, what to compare, and how to write feedback that names a repair location. Each task moves through two verdicts: a prelim_verdict and a final_verdict.

Review flow
Step 1
Four quality checks
Determinism
Solution correctness
Difficulty
Duplicate
→
Step 2
prelim_verdict
A first-pass review found the task deterministic, correctly solved, hard enough, and not a duplicate. This is a provisional pass: the task is nearly approved, but it still needs the final review before it can be paid.
→
Step 3
final_verdict
A more comprehensive review confirms the task meets the desired difficulty level and is not a duplicate. 98% of tasks that pass prelim_verdict also pass final_verdict, so this should not be a major concern.
→
Step 4
Approved & paid
Once a task shows "Approved and Paid" in final_verdict, the amount appears in the author's Payments dashboard. Base pay appears first; incentives and bonuses are paid later.
↶
If a task fails a check
Write feedback in the gold sheet naming the file, the mistake, how it moves the answer, and where to repair it. "Task is ambiguous" or "model got it wrong" is not usable feedback.
Review 1 rules
Rules checked at Review 1

A task ships with at least six input files.
Blocking
at least 6 files
At least four of the shipped files are independently necessary: remove any one of them and the solution can no longer be reached.
Blocking
at least 4 files
At least two of the inputs are substantial rather than token: long, dense files that take real work to read and reconcile.
Blocking
at least 2 files
Optional distractor files are allowed and encouraged, but they never count toward the four independently necessary files.
Blocking
AI may be used to locate data or to write transformation scripts, but it may never create the empirical source evidence itself.
Blocking
Scenario documents and derived files carry explicit provenance stating what they are and how they were produced.
Blocking
Reviewer flow
Work through the task in this order. Each step is an action you take, not a definition to recall.

1. Verify scope

Confirm the task sits in one accepted domain and has one primary analytical objective.
Confirm domain, analytical objective, and reasoning phase match the actual task, not just the populated fields.
For biology-related tasks, confirm the subject matter stays inside the allowed biology scope in Task types. If it falls into a banned subdomain (pathogen enhancement or design, delivery and dissemination, toxins and harmful agents, high-risk pathogen and biodefense areas, targeting and population effects, acquisition and evasion), treat the task as out of scope regardless of analytical quality.
2. Reproduce the golden

Independently reproduce every load-bearing number in the golden from the submitted files: joins, filters, denominators, cohort or population definitions, cleaning, transformations, normalization, QC, statistical calculations, predictive validation, thresholds, and decision rules.
For predictive tasks, test target definition, absence of leakage, train/validation/test design, time-aware validation, forecast horizon, model comparison fairness, metric choice, and calibration where decision-relevant.
For biology, biostatistics, epidemiology, and bioinformatics tasks, test cohort inclusion/exclusion, assay or sequencing QC, normalization, variant filtering, batch handling, exposure and outcome definitions, confounding, and multiple testing. Keep the review analytical, not clinical, and inside the allowed biology scope.
Compare Final Recommendation, Critical Components, Step-by-Step Solution, Justification, and Determinism against each other; flag stale numbers, copied blocks, and contradictions.
If a model response follows a reproducible path better supported by the shipped files than the golden, classify it as a golden-solution defect, not a response error. Repair the task at the source.
3. Test determinism

Test whether competent domain experts working from the same prompt, workspace, and standard domain knowledge converge on the same recommendation.
Fail determinism if a materially different answer stays defensible because of an unpinned definition, threshold, scope, population, time window, metric, or decision criterion.
Test robustness: the winner should survive reasonable expert variation (confidence intervals, validation variability, model specification, forecast uncertainty, or an alternate defensible metric). No single robustness test is required.
4. Inspect the trap

Identify whether a plausible wrong analytical path exists and whether taking it produces a meaningful error in an intermediate result, ranking, interpretation, prediction, or the final recommendation.
Reject difficulty that comes from missing information, arbitrary thresholds, unclear wording, unresolved definitions, unreconcilable files, external facts not supplied, or file volume with no analytical purpose. See Invalid stumps for the full patterns and how to name them in feedback.
Check the workspace: multiple files must be substantively necessary, versions and identifiers must reconcile, and source material must be real, traceable, and licensed for use.
5. Analyze rollout divergence

When a model response differs from the golden, classify why before writing feedback:

Classification	Meaning	Counts as difficulty?
Valid analytical stump	The response misses decisive evidence, uses a provably wrong method, mishandles data, stops at a misleading artifact, or applies invalid cleaning/filtering/QC/statistical logic	Yes
Semantic fork	The response analyzes correctly but resolves an unpinned objective or convention differently	No, it is a determinism defect in the task
Golden wrong	The response follows a reproducible path better supported by the files than the golden	No, it is a solution defect, repair the golden
Judge the rollout as a whole: strong model responses should be making real analytical errors, not stylistic ones.
Reject tasks that are too easy even when deterministic and correct: the prompt explains the methodology, a document states the planted trap outright, the decisive rule is a lookup, or the complexity never changes the answer.
6. Approve or return with repair location

Every failure has to name the file, the mistake, how it moves the answer, and where the task gets repaired:

Prompt: pin the objective, scope, or decision term.
Input files: add the missing evidence, remove the unresolvable contradiction, strengthen the live trap, or repair workspace coherence.
Solution: correct or regenerate the stale or wrong golden content.
Never use the rubric to paper over a broken task, and never approve overly templated or duplicate tasks, these are caught at the final_verdict stage.