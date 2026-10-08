# Shape 16 · Indicators into one score

> **Where the criteria come from:** each indicator as it enters the index.

You combine several indicators into one composite score, each with its own value, the range it is
scaled over, and its weight, behind an eligibility screen. The answer is the unit the score
selects. The many criteria come from each indicator as it enters the index.

**Canonical Axis 1 objective under our roster:** Descriptive & Distribution Analysis.

## Sizing it to 25

Seven indicators, each graded twice (the value as it enters, and the min-max range it was scaled
over), is fourteen criteria. Add the weight set, the selected unit's composite, the runner-up's
composite, the screened-out set, one direction pin (which indicators are inverted before
scaling), the population the choice serves, and the ranked composite bars.

**What makes it hard rather than long.** The **scaling range is the eligible set's own min and
max**, not the full population's, so the screen has to run before the scaling and a solver that
scales first gets every scaled score slightly wrong and can select a different unit. Direction is
the second trap: some indicators are worse when higher and have to be inverted before scaling, and
which ones is stated in the methodology, not the prompt. Keep the screen, the weights and the
direction pins in three different shipped documents, and make the top two composites close enough
that a single mis-scaled indicator flips the selection.

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
> not the metric, not a file name, not the wording of a single ask.

### Nonprofit & Grant-making · 2 files · ~27 criteria
*Next cash-transfer district by vulnerability index*

I lead cash transfers for an NGO country office and the 2027 cohort goes to the shortlisted
district scoring highest on the vulnerability index, screened and scaled exactly as the
methodology note says and against the coordination matrix. I need that one district named. Build
the index table showing how every district scored, vulnerability_index_2027.xlsx, one row per
shortlisted district with each indicator as it enters, the range it was scaled over, its scaled
score and its composite, dropped districts marked and why, plus the weight applied to each
indicator. Then one donor slide, a deck, the district we go to next with its composite score and
the indicator contributing most to it, and composite bars for every district still in contention,
highest first.

*Criteria:* 7 indicators x 2 (value as entered + eligible-set min/max scaling range) = 14 + the
weight set + selected composite + runner-up composite + the dropped set + one direction pin + the
caseload + 2 deliverables.

### Policy & Education · 2 files · ~27 criteria
*The school that gets the turnaround grant*

I run the state turnaround office and this cycle's grant funds one school, named off the
composite risk index in our published methodology, screened for schools already in another
intervention, and scaled over the eligible set exactly as written. Give me the index table the
review committee reads, a workbook, one row per eligible school with each indicator as it enters,
the range it was scaled over, its scaled score and composite, screened-out schools marked and
why, and the weight applied to each indicator. Then the slide for the commissioner,
selected_school.pptx, the school we select with its composite score and the indicator
contributing most to it, and composite bars for every school still eligible, highest first.

*Criteria:* 7 indicators x 2 (value as entered + eligible-set min/max scaling range) = 14 + the
weight set + selected composite + runner-up composite + the screened-out set + one direction pin
+ the enrollment served + 2 deliverables.

### Supply Chain & Logistics · 2 files · ~26 criteria
*The supplier site for the resilience investment*

I own supply resilience and this year's hardening budget covers one supplier site, chosen off our
composite risk index, screened for sites already dual-sourced, and scaled over the eligible set
exactly as the scoring standard states. I need that site named. Build the index table the sourcing
council reviews, supplier_risk_index.xlsx, one row per eligible site with each indicator as it
enters, the range it was scaled over, its scaled score and composite, screened-out sites marked
and why, plus the weight applied to each indicator. Then the decision slide for the VP, a deck,
the site we invest in with its composite score and the indicator contributing most to it, and
composite bars for every site still in contention, highest first.

*Criteria:* 7 indicators x 2 (value as entered + eligible-set min/max scaling range) = 14 + the
weight set + selected composite + runner-up composite + the screened-out set + one direction pin
+ the annual spend exposed + 2 deliverables.

### Demographic & Social Science · 2 files · ~27 criteria
*The tract for the heat-resilience center*

I plan climate resilience for the city and the capital line funds one cooling center, sited in the
tract chosen off our heat-vulnerability index, screened for tracts already within reach of a
center, and scaled over the eligible set exactly as the methodology reads. Give me the index table
the council staff reviews, a workbook, one row per eligible tract with each indicator as it
enters, the range it was scaled over, its scaled score and composite, screened-out tracts marked
and why, and the weight applied to each indicator. Then the recommendation slide for council,
site_recommendation.pptx, the tract we site the center in with its composite score and the
indicator contributing most to it, and composite bars for every tract still eligible, highest
first.

*Criteria:* 7 indicators x 2 (value as entered + eligible-set min/max scaling range) = 14 + the
weight set + selected composite + runner-up composite + the screened-out set + one direction pin
+ the residents served + 2 deliverables.
