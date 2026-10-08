# Shape 01 · Ranked list under a cap

> **Where the criteria come from:** every candidate's score, the in-or-out call on each, and the first one left below the line.

You rank every candidate on one score and fill the list from the top until a cap runs out.
The answer is the set that makes the cut. The many rubric criteria fall out naturally: each
candidate's score, who is in and who is out, and the first one left just below the line.

**Canonical Axis 1 objective under our roster:** Descriptive & Distribution Analysis. It
becomes Forecasting & Predictive Modeling when the score being ranked is itself a predicted
value the supplied history pins down.

## Sizing it to 25

Ten to twelve candidates carries the shape on its own, because each candidate's score is a
criterion and the in-or-out verdict on each is a second. The rest comes from the first
candidate below the cutline (its identity, its score and its shortfall), the candidates whose
award the cap trimmed rather than granted in full, the screened-out set with its reasons, and
the cutline drawn on the chart. Do not stretch the candidate list to make the count; a
shortlist of five with a cap that bites hard beats twenty near-identical rows.

**What makes it hard rather than long.** The score has to be built, not read. Push the
eligibility screen and the cap into different files, make the guideline award a computed
figure rather than a stated one, and let the cap run out mid-list so the trimming rule
matters. If the candidates arrive pre-scored and the cap is a plain sum, the shape is a
spreadsheet exercise and every response gets it.

---

## Four worked prompts


> **Before you draft, read [`../prompt-voice.md`](../prompt-voice.md).** The four prompts below are
> the client's. Across the eighteen shape files these examples open on the rule, the constraint,
> the deliverable, the question, the symptom, the number and the person, so **none of them is the
> template and the four below are not a menu of four.** Read four in a row and you will write the
> fifth in whichever voice you just read, which is how eighteen consecutive builds came to open
> with "I run". Pick the move from what forces your decision, then check it against the last three
> builds with `../voice-check.py`.

> **Idea seeds only.** Nothing below transfers into a build: not the scenario, not the entity,
> not the metric, not a file name, not the wording of a single ask. What transfers is the
> shape. Draw your own nouns through the anti-clone draw in `../../../stumping/SKILL.md` Part 6.

### Nonprofit & Grant-making · 2 files · ~28 criteria
*Youth Workforce Fund 2026 award slate*

I run our community foundation's Youth Workforce Fund, and the board votes next week off one
funded slate. Fill the pot in strict protocol-score order, full guideline awards only, skip any
organization the money left cannot cover, and keep going until nothing more fits. Give me the
ranked read as award_slate_2026.xlsx: every eligible applicant in score order with its protocol
score, its request, its award, and whether it was funded, then a second tab listing the
applicants we ruled ineligible and why. And write the note the board reads before the vote, a
short memo, naming the organizations we fund with each award and what is left in the pot, then
the first applicant we could not cover and how far short we fell.

*Criteria:* 12 funded scores + the first-left-out score and identity + its shortfall + the 3
guideline-capped awards + 4 ineligible reasons + the funded set + the ineligible set + 2
deliverables.

### Product Analytics · 2 files · ~26 criteria
*Which experiments the platform funds*

I lead growth, and I need to lock which experiments get platform slots this quarter. Fill in
priority-score order, each experiment gets its full requested run-length or nothing, and skip
anything that will not fit the test-weeks still open. Start with the ranked read of the whole
queue, a spreadsheet, every eligible proposal in score order with its priority score, requested
weeks, allotted weeks, and whether it was funded, plus a tab of the proposals we screened out
and why. Then a one-pager for the quarterly planning review, experiment_readout.pdf: the funded
set and the platform weeks left over, the first proposal below the cutline and how many weeks
short it landed, and a ranked bar chart of the scores with the cutline drawn across it.

*Criteria:* the funded scores down the queue + the first proposal below the cutline and its
shortfall + the capacity-trimmed allotments + the screened-out set + the funded set + the
cutline chart + 2 deliverables.

### Supply Chain & Logistics · 2 files · ~27 criteria
*Reefer container load for Friday*

The refrigerated container leaves Friday and I load it in margin-per-cube score order, full
case-lots only, skipping any lot that will not fit the cube still open. I need the committed set
of SKU lots that make it on. Build load_plan.xlsx as the ranked pick list the dock crew works
to, each eligible lot in score order with its margin-per-cube score, its cube, and whether it
loaded, and a tab for the lots the cold-chain screen threw out with the reason. Then a fill
chart for the shift huddle, a PNG, plotting cumulative cube down the ranked list against the
container line, with the first lot that did not fit called out and how much cube it came up
short.

*Criteria:* the committed scores down the ranked lots + the first lot left off and its cube
shortfall + the cube-trimmed partial + the excluded set + the loaded set + the cumulative-fill
chart + 2 deliverables.

### Policy & Education · 2 files · ~26 criteria
*Teacher residency stipend cohort*

I run the teacher residency program and I need the cohort of residents who get stipends this
cycle. Work down in rubric-score order, the full guideline stipend or nothing, skip any
candidate the remaining budget cannot cover, and stop once the money runs out. Give me a ranked
award workbook for the program file, each eligible candidate in score order with rubric score,
stipend, and whether awarded, plus a tab of the ones ruled ineligible and why. Then write
award_brief.docx for the program office: the residents funded and the budget remaining, the
first candidate left unfunded and by how much, and a table of the awards broken out by region.

*Criteria:* the scores down the funded cohort + the first candidate left out and the shortfall +
the budget-trimmed award + the ineligible reasons + the funded cohort set + the by-region table
+ 2 deliverables.
