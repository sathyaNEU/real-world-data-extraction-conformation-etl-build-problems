# task258 design note

## Draw

- **Card:** `cards/task258.json`, registered 2026-10-13. Product Analytics, task type
  metric-definition-measurement-science, objective Descriptive & Distribution Analysis; shape 14 (each property's
  page loads cut at 2,500 ms, now and after the playbook); decision pick_one_of_n; gap population; pattern C; G8 then
  G16; Gate G method_or_model_selection; strategy population_selection (the loads one intervention can reach, built
  load by load from the parts of each load's paint).
- **World:** Brolga Media, a fictional Australian digital media group with six properties: Courier (news), Matchday
  (sport), Hearth (home), Ledger (personal finance), Trailhead (travel) and Pantry (food). Its web platform team has
  one performance squad, sent each quarter by the squad's charter to the property where the squad's hero-image
  playbook will move the most page loads a month into the good Largest Contentful Paint band (2,500 ms or less), as
  the group's own RUM measures them on the latest complete month. The playbook moves a property's hero images to
  the group image CDN (AVIF, sized to the slot), preloads them at high priority and never lazy-loads them. The next
  engagement starts on 5 January 2027 and is fixed at the December planning (forcing event other: the quarter's
  assignment); the head of web platform assigns the squad (forum line_manager_or_team).
- **People** (guard.py names --geo Australia --seed 258; the first three drawn, Andrea Koch, Justin Fernandez and
  Christina Singleton, skipped for first names used in older builds): Margaret Good, head of web platform (role
  family product_manager); Tasha Murillo, performance squad lead; Doris Rhodes, site reliability lead who keeps the
  domains runbook and the CDN host list.
- **Data-native sentence:** every RUM beacon carries its own paint broken into time to first byte, the image's load
  delay and load time, and render delay, and the playbook moves a property's hero images to the group image CDN
  with a preload, so after it the image request waits on that CDN's connection rather than on the page finding the
  image: the delay settles at one level whatever it was before, rising on pages that already found their image
  early, which no ratio of before over after reproduces.
- **Guard:** PASS with WARNs. repeat.gate_g and overuse.gate_g (method_or_model_selection after task255 and task256):
  the decisive step is which model of the playbook's effect the past engagements bear out, the honest key; the
  strategy (population_selection) differs from task255's maturity_censoring and task256's composition_mix.
  repeat.decision (pick_one_of_n after task256): one squad, one property, the seed's decision by construction. The
  question leads with where (the squad is sent somewhere), not which, after task256.
- **Order:** drawn ahead of task257. DA07's world (a parcel carrier's van tiers by duty-cycle fuel economy) turns on
  the duty-cycle mix, composition_mix, which ban.strategy bars against task256 for any build drawn the same day with
  a lower number; task257 is drawn on a later day.
- **Pairing and shape:** the field's own analysis decides (how many page loads a month a change to two of the paint's
  four parts brings under the Core Web Vitals line, estimated from RUM attribution and the measured effect of past
  engagements), the objective is where a distribution sits against a cut, and each property's distribution is cut
  at 2,500 ms before and after (shape 14). Criteria: six properties, each with the page loads a month the playbook
  moves (6), the share of its page loads whose paint element is an image it serves itself (6) and its page loads a
  month in the good band now (6); the call, the runner-up and the gap (3); the chart's named parts (5); two files
  (2). 28 before the asks are weighed.
- **Sources, one line each.** `guard.py mechanisms --strategy population_selection`: task25 and task28 (the share of
  a flagged excess one intervention can reach, behind a join) are this pattern's precedent, here the reach is built
  from each load's own parts and the playbook's effect, not a source attribute; task124 (a rate from units examined
  because they showed signs), task132 (a failed item restarts its wear curve) and task116 (a group offer) spend other
  selections. task129 (another lane: a publisher's slowdown split between two changes by first loads against cached
  reloads) shares the setting, not the move: it attributes a loss, this build counts the loads an intervention can
  move. `layer2-rigor-patterns.md` (metric-definition-measurement-science: metrics validated on known interventions,
  ratio of sums, mix shift) has no counterfactual over a metric's parts; the family is estimand identification (the
  right counterfactual, `two-layer-task-design.md`). The seed DA08 gave the world, the decision and the quantity; its
  own hint (fixes only moved loads whose paint element was the property's own image) stays a lower rung.
- **Forward facing:** the call sends the squad for the quarter from 5 January 2027, a window not yet open; the
  deciding quantity is counted on November 2026's page loads because the charter measures it on the latest complete
  month.

## Tried and rejected

- DA07 for this slot's turn (a parcel carrier's 2027 van tiers by duty-cycle fuel-economy demonstration): every
  honest decisive step found in that world normalises each van's fuel use to its duty cycle (composition_mix),
  barred today against task256; the other candidates (ledger posting lag, telematics fuel bias, protected cold days
  for electric vans) were a near copy of task181's completion by channel, a planted-defect flip or the same mix by
  temperature. task258 drawn first; task257 waits for a later draw day.
