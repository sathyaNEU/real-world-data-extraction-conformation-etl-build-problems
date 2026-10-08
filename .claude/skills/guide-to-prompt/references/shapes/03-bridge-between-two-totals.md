# Shape 03 · Bridge between two totals

> **Where the criteria come from:** each reconciling item along the walk, on both sides.

You walk one total across to another, one reconciling item at a time, until the two sides meet.
This can be two systems, two time periods, or plan against actual. The answer is the source or
figure you adopt, usually the item that moves the total the most. Each reconciling item along
the way is its own criterion.

**Canonical Axis 1 objective under our roster:** Data Extraction & Conformation (ETL). It is
Descriptive & Distribution Analysis instead when the two totals are two periods of the same
series and the walk is a growth decomposition rather than a system reconciliation.

## Sizing it to 25

Two candidate sources, each bridged item by item to the same audited figure, doubles the count
for free: five or six reconciling items per side is ten to twelve criteria. Add the gap for each
source in each of three periods (six more), the raw and audited totals at both ends, the flagged
rows where the two sources diverge beyond tolerance, the adopted source, and the single largest
item on the losing side.

**What makes it hard rather than long.** The adjudication rule has to bite. "Inside tolerance in
every period, ties broken on the smallest gap in the final period" forces the solver to compute
both bridges completely before it can name a source, and it punishes a solver that bridges only
the source it expected to win. The reconciling items themselves must be discoverable from the
pack rather than listed anywhere, and the tolerance lives in a shipped memo, never in the prompt.

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

### Product Analytics · 2 files · ~25 criteria
*Canonical daily orders source*

I run analytics engineering and I have to pick one canonical source for the daily orders table,
either the SDK event stream or the server table. After Finance's memo exclusions, adopt whichever
lands inside tolerance against the ledger in each of the last three months, and settle ties and
any misses on the smaller August gap. Produce daily_orders_conformed.csv, the daily table for
June through August from the source that wins, one row per day with orders after exclusions and
any day where the two sources differ by more than the flag threshold marked. Then the note the
CFO signs, a Word memo, giving the source we adopt and each source's gap to the ledger for all
three months, then the August bridge for each source, raw count down through one line per
reconciling item to the ledger.

*Criteria:* the SDK August bridge items + the server August bridge items + June/July/August gaps
for both sources + the raw and ledger totals + the flagged-day set + the adopted source and its
decisive gap + the largest losing item + 2 deliverables.

### Supply Chain & Logistics · 2 files · ~26 criteria
*System of record for on-hand stock*

I own inventory master data and I need one on-hand source of record named, WMS or ERP. After the
reconciliation memo's adjustments, take whichever sits inside tolerance against the physical
count in each of the last three counts, breaking ties on the smaller final-count variance. Build
the reconciled daily on-hand table from the system that wins, a CSV, one row per SKU-day with
the reconciled on-hand and any day the two systems differ beyond tolerance flagged. And the
reconciliation the controller signs off, inventory_bridge.docx: the system we adopt and each
system's variance to the physical count across the three counts, then the final-count bridge for
each system, system count down through one line per reconciling item to the physical count.

*Criteria:* the WMS final-count bridge items + the ERP final-count bridge items + all three
counts' variances for both systems + the raw and physical totals + the flagged-day set + the
adopted system and its decisive variance + the largest losing item + 2 deliverables.

### Policy & Education · 2 files · ~25 criteria
*Enrollment source for state funding*

I own enrollment reporting and the state needs one source named for the official count, either
the student information system or the state attendance portal. After the audit memo's
exclusions, whichever lands inside tolerance against the audited count in each of the last three
counts wins, ties going to the smaller October gap. I need the reconciled daily enrollment table
from the winning source, a CSV, one row per school-day with reconciled enrollment and any day
the two systems diverge beyond tolerance flagged. Then the reconciliation the business office
certifies, a memo, naming the source we adopt with each source's gap to the audited count across
the three counts, and the October bridge for each source running raw count down through one line
per reconciling item to the audited count.

*Criteria:* the SIS October bridge items + the portal October bridge items + all three counts'
gaps for both sources + the raw and audited totals + the flagged-day set + the adopted source and
its decisive gap + the largest losing item + 2 deliverables.

### Nonprofit & Grant-making · 2 files · ~26 criteria
*Revenue source for the annual report*

I manage our finance data and I have to name the canonical revenue source for the annual report
and the 990, the donor CRM or the processor export. After the finance memo's adjustments, adopt
whichever sits inside tolerance against bank deposits in each of the last three months, settling
ties on the smaller December gap. Give me donations_conformed.csv, the reconciled daily
gift-revenue table from the chosen system, one row per day with reconciled gift revenue and any
day the two systems differ beyond tolerance flagged. Then the reconciliation for the audit
committee, a PDF with the bridge laid out as a table, showing the source we adopt and each
system's gap to bank deposits across the three months, then the December bridge for each system
from raw total down through one line per reconciling item to deposits.

*Criteria:* the CRM December bridge items + the processor December bridge items + all three
months' gaps for both systems + the raw and deposit totals + the flagged-day set + the adopted
source and its decisive gap + the largest losing item + 2 deliverables.
