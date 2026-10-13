# task255 design note

## Draw

- **Card:** `cards/task255.json`, registered 2026-10-13. Actuarial Science & Insurance, task type
  claims-frequency-severity, objective Descriptive & Distribution Analysis; shape 04 (setting one dial: each quoted
  attachment); decision dial_setting; gap population; G12 then G16; Gate G method_or_model_selection; strategy
  maturity_censoring (here limit censoring at the pool's retention with deductible truncation, no maturity element).
- **World:** Fallowmere Intergovernmental Risk Pool, a Washington pool of 62 cities and special districts. The pool
  shares its members' liability occurrences above each member's deductible ($10,000, $25,000, $50,000 or $100,000,
  elected yearly) up to its per-occurrence retention, inclusive of the deductible ($250,000 for occurrences in 2014
  to 2017, $500,000 from 2018); its excess insurer pays above the retention, outside the pool's claims system. For
  1 January 2027 the broker gathered indications at seven attachments from $1.0 million to $5.0 million, and the
  trustees' risk financing policy keeps every layer the pool expects to be reached more than once a year. The
  trustees set the 2027 retention at their meeting of 18 November 2026 (forcing event vote_or_meeting).
- **People** (guard.py names --geo US --seed 255): Laura Williams, finance director; Larry Hodge, consulting actuary;
  Matthew Klein, the broker's account executive; Caleb Payne, claims manager.
- **Data-native sentence:** a pool's claims record is a window on its members' losses: an occurrence enters it only
  once its member has paid the deductible in force that year, and stops at the pool's retention, beyond which the
  excess insurer pays and the pool records nothing; both thresholds were fixed in each year's dollars, so at 2027
  cost every occurrence carries its own floor and its own ceiling.
- **Guard:** WARN repeat.gate_g and overuse.gate_g (method_or_model_selection after task450 and task501): the
  mechanism here is a loss model's observation process, deductible truncation and retention censoring in the
  likelihood, against task450's emissions grain and task501's transmission model; the vocabulary's nearest honest key.
  Question form how-much: the attachment is the amount of each occurrence the pool keeps.

## Tried and rejected

- DA05's seed world (a hospital trust's weekend day-surgery team and 52-week waits): no Descriptive task type in the
  client taxonomy fits that world's decision, so the number was redrawn inside Descriptive with a new world.
- A competing-risk design (time to resolution with withdrawals as non-returners): task134 v1 spent Kaplan-Meier with
  competing exits as the golden; rejected at the draw.
- High member deductibles across the board: the complete-sample fit and the truncated fit cancelled toward one
  attachment; rejected in the feasibility search.
