# Product Analytics

**Axis 0 domain.** Canonical label, do not rename it. Every task sits in exactly one domain, and the one to pick is the one whose decision-maker would actually own the call.

- **Typical decisions:** Growth, activation, retention, monetization, experimentation calls at a digital product company
- **Typical data:** Event logs, funnels, experiment results, billing/usage tables

## Enumerated subdomains

Pick one and write it into `DATASET_NOTES.md` with the domain. These lists are a browsing aid rather than a closed set, but a subdomain you cannot map to one of these is a signal to change the trap, not to stretch the scope.

- **Acquisition & growth:** channels, campaigns, signups, referral loops; marketing attribution (CAC, LTV:CAC); organic and content growth (SEO, virality)
- **Onboarding & activation:** the "aha" moment, time-to-value, first-key-action completion; signup, checkout, and multi-step funnels
- **Engagement & retention:** Dn retention, stickiness (DAU/MAU), resurrection; feature adoption and depth; lifecycle messaging; search, ranking and recommendations; session quality
- **Monetization & subscriptions:** MRR/ARR, ARPU, net and gross revenue retention; pricing and packaging; usage-based billing; free-to-paid and PLG conversion
- **Retention risk:** voluntary and involuntary churn, leading indicators, cohort-level drivers
- **Trust, safety & support:** payment fraud and chargebacks; abuse, spam and content integrity; support and CX (deflection, CSAT/NPS)
- **Experimentation & measurement:** A/B testing (lift, guardrails, sample-ratio checks); metric diagnosis; metric definition and goaling; segmentation and personas; instrumentation and data quality
- **Other:** anything else that fits product analytics, as long as it stays in scope

## Example prompts

The worked example prompts live in `../shapes/`, filed by prompt shape. Read them as idea
seeds for what a task in this domain can be about. **Never copy one into a build**: not the
scenario, not the entity, not the metric,
not a file name, not the wording of an ask. The anti-clone draw in
`../../../stumping/SKILL.md` Part 6 is what turns a seed into a fresh build.
