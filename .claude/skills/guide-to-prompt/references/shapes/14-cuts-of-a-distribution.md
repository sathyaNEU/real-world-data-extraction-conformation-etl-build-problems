# Shape 14 · Cuts of a distribution

> **Where the criteria come from:** each cut of the distribution, in each segment.

You cut one weighted distribution at several percentiles across a few segments. The answer is the
set of nested band boundaries that hits the committed cumulative coverage shares under the stated
scaling and rounding rules. The many criteria come from each cut of the distribution in each
segment.

**Canonical Axis 1 objective under our roster:** Descriptive & Distribution Analysis.

## Sizing it to 25

Two percentiles across six segments is twelve distribution cuts. Add the share of each segment
qualifying at all (six more), the population each tier serves (three), the reference-size boundary
for each tier (three), the scaling or inflation factor, the base the shares are struck on, and the
exhibit with the boundaries drawn across the segments.

**What makes it hard rather than long.** Three things. The distribution is **weighted**, so the
percentile is not the row-order percentile and a solver that ignores the weight is wrong
everywhere at once. The boundaries are **solved backwards** from committed coverage shares rather
than read off the distribution, which is the inverse of the natural direction. And they are
**nested** across segments through an equivalence scale, so one reference-size boundary generates
the whole schedule under a rounding rule that lives in the shipped policy. Put the scaling factor
and the rounding rule in different files.

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

### Demographic & Social Science · 2 files · ~29 criteria
*Energy credit income ceilings by household size*

I own our 2027 credit-tariff filing, and the order commits us to cumulative shares of served
households at each tier. It is on me to turn that into one schedule of tier income ceilings at
the reference household size that clears every committed share. Draft the tariff filing the
commission signs, energy_credit_ceilings_2027.docx, with the full ceiling table: each tier's
ceiling at each household size in the order and the households receiving each tier's credit, then
the share of households of each size qualifying for any tier. And the distribution exhibit that
goes in the filing, a PNG, the lower-quartile and median 2027 income of served households at each
size labeled, with the tier ceilings drawn across household sizes.

*Criteria:* 2 percentiles x 6 household sizes = 12 distribution cuts + 6 qualifying shares + 3
tier-credit populations + 3 reference ceilings + the inflation adjustment factor + the
served-household base + 2 deliverables.

### Policy & Education · 2 files · ~28 criteria
*Need-based aid income bands by family size*

I am the fiscal analyst who owns the state grant's income schedule. The board committed to what
share of the applicant pool lands in each award tier, and I have to publish one set of award-tier
income ceilings at the reference family size that produces those shares. Build the published band
table campuses will key off, aid_income_bands_2027.xlsx, each award tier's income ceiling at each
family size in the resolution and the applicants receiving each tier's award, then the share of
applicants of each family size qualifying for any award. Then the distribution chart for the
board packet, a PNG, the lower-quartile and median adjusted income of applicants at each family
size labeled, with the tier ceilings drawn across family sizes.

*Criteria:* 2 percentiles x 6 family sizes = 12 distribution cuts + 6 qualifying shares + 3
award-tier populations + 3 reference ceilings + the income adjustment factor + the applicant base
+ 2 deliverables.

### Product Analytics · 2 files · ~27 criteria
*Usage thresholds for the new plan tiers*

I own monetization and we are repackaging into Free, Pro and Enterprise. Leadership committed to
what share of accounts sits in each tier, and I have to set the monthly usage thresholds at the
reference segment that land every committed account share in its tier. Give me the threshold
table the billing team implements, plan_thresholds.xlsx, each tier's usage threshold for each
account segment in the brief with the accounts falling in each tier, then the share of accounts
in each segment above the Free ceiling. And the usage distribution slide for the pricing review, a
PNG, the lower-quartile and median monthly usage of accounts in each segment labeled, with the
tier thresholds drawn across the segments.

*Criteria:* 2 percentiles x 5 segments = 10 distribution cuts + 5 above-ceiling shares + 3 tier
populations + 3 reference thresholds + the normalization factor + the active-account base + 2
deliverables.

### Nonprofit & Grant-making · 2 files · ~28 criteria
*Sliding-scale fee bands for the food program*

I direct our community food program. The board committed to what share of clients pays at each
fee level, and I need one set of fee-tier income bands at the reference household size that
produces those shares under our own rounding rule. Draft the fee schedule that goes in the
renewal packet, a Word doc, each fee tier's income band at each household size in the policy with
the clients paying at each tier, then the share of clients of each household size in the
reduced-fee tiers. Then the distribution exhibit the board reviews, income_bands_exhibit.png, the
lower-quartile and median adjusted income of clients at each household size labeled, with the
fee-tier bands drawn across household sizes.

*Criteria:* 2 percentiles x 6 household sizes = 12 distribution cuts + 6 reduced-fee shares + 3
fee-tier populations + 3 reference bands + the cost-of-living factor + the served-client base + 2
deliverables.
