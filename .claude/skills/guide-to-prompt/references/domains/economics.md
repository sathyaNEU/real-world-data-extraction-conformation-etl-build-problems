# Economics

**Axis 0 domain.** Canonical label, do not rename it. Every task sits in exactly one domain, and the one to pick is the one whose decision-maker would actually own the call.

- **Typical decisions:** Labor, price, output, or trade reads and forecasts
- **Typical data:** Payroll, CPI/PPI, GDP, trade, and monetary series

## Enumerated subdomains

Pick one and write it into `DATASET_NOTES.md` with the domain. These lists are a browsing aid rather than a closed set, but a subdomain you cannot map to one of these is a signal to change the trap, not to stretch the scope.

- **Labor markets:** payrolls, unemployment, participation, job openings; wages and occupational pay
- **Prices & inflation:** CPI, PPI, cost of living, inflation decomposition
- **Output & activity:** GDP by industry or state, industrial production, business dynamics
- **Trade & international economics:** trade balances and flows, terms of trade, external exposure
- **Public finance:** federal and state spending, tax statistics, deficits
- **Money & credit:** monetary and credit aggregates, forecasting an economic indicator
- **Other:** other macro, labor, trade, or fiscal reads

## Boundary

**In scope:** macro, labor, trade, and fiscal reads. **Out of scope:** corporate finance, markets trading, and lending underwriting.

## Objectives in scope

Economics carries the **eight** Axis 1 objectives, and only these eight:

1. Descriptive & Distribution Analysis
2. Anomaly Detection & Diagnostics
3. Root-Cause Analysis
4. Experiment & Causal Analysis
5. Forecasting & Predictive Modeling
6. Data Extraction & Conformation (ETL / Pipeline Build)
7. Opportunity Sizing & Decision Support
8. Data Quality Monitoring & Alerting

These are the same eight that apply to every domain. Nothing else is a valid tag.

## Example prompts

The worked example prompts live in `../shapes/`, filed by prompt shape. Read them as idea
seeds for what a task in this domain can be about. **Never copy one into a build**: not the
scenario, not the entity, not the metric,
not a file name, not the wording of an ask. The anti-clone draw in
`../../../stumping/SKILL.md` Part 6 is what turns a seed into a fresh build.
