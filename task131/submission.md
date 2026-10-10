# task131: the 2027 member card offer

## Tags

**Domain:** Marketing & Consumer Research (CRM, loyalty and retention).
**Analytical objective:** Experiment & Causal Analysis (a card-randomised offer test read at the unit the rollout acts on).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Put the Frischbonus (fresh bonus) on every member card in 2027; its 2027 programme value is CHF 966 thousand.**

It adds CHF 0.49 of net margin per active card-week against CHF 0.34 for the Wochenauswahl, the runner-up. Not the Wochenauswahl, which leads only when cards are compared one by one and its lead is baskets moved between cards of the same membership. Not the Monatsziel, which moved the most spend but pays for it in vouchers. Not the Dreifachpunkte, whose lift fades after launch.

## 2. Critical Components

1. Frischbonus net margin per active card-week, memberships whose cards all drew one cell: **CHF 0.49**
2. Wochenauswahl net margin per active card-week on the same basis: **CHF 0.34**
3. Active cards in the 2027 programme plan: **37,720**

## 3. Step-by-Step Solution

1. Built every allocated card's net margin per card-week (gross margin less reward cost) over the baseline weeks 2026-W15 to W22 and the run-rate weeks W29 to W34, weeks without a row counting as zero, per MP-3 sections 2 to 4.
2. Joined `st26_offer_allocation.csv` to `member_cards.csv`: the engine allocated cards, so the cards of one membership often carry different cells, and a card with an offer gains baskets its sibling cards lose, which disappears once every card carries the offer.
3. Kept memberships whose cards all drew the same cell and took each offer's mean run-rate change against the control cell: Frischbonus CHF 0.49, Wochenauswahl CHF 0.34, Dreifachpunkte CHF 0.26, Monatsziel CHF 0.16 per active card-week.
4. Multiplied by 52 and the 37,720 active cards in `programme_plan_2027.xlsx` (MP-3 section 5): CHF 966, 666, 516 and 316 thousand.
5. Placed each membership's home branch in the 1 July 2026 network from `network_changes_2026-07-01.docx` (Degersheim members to Herisau, Egnach members to Arbon, Rorschach Hafen, Goldach and Thal into St. Gallen Stadt) and repeated step 3 by region.
6. Recommendation: the Frischbonus on every card in 2027, CHF 966 thousand.

## 4. Deliverable Answers

### programme_offer_2027.docx

1. First line: the Frischbonus on every member card in 2027, 2027 programme value CHF 966 thousand.
2. All four offers ranked, net margin per active card-week and 2027 programme value:
   - Frischbonus: CHF 0.49, CHF 966 thousand
   - Wochenauswahl: CHF 0.34, CHF 666 thousand
   - Dreifachpunkte: CHF 0.26, CHF 516 thousand
   - Monatsziel: CHF 0.16, CHF 316 thousand
3. Runner-up: the Wochenauswahl, CHF 0.15 per card-week behind the Frischbonus.
4. Net margin per active card-week by region and offer:
   - St. Gallen Stadt: Frischbonus CHF 0.55, Dreifachpunkte CHF 0.30, Monatsziel CHF 0.21, Wochenauswahl CHF 0.40
   - Fürstenland: Frischbonus CHF 0.42, Dreifachpunkte CHF 0.20, Monatsziel CHF 0.08, Wochenauswahl CHF 0.25
   - Rheintal: Frischbonus CHF 0.41, Dreifachpunkte CHF 0.19, Monatsziel CHF 0.09, Wochenauswahl CHF 0.28
   - Thurgau Ost: Frischbonus CHF 0.47, Dreifachpunkte CHF 0.24, Monatsziel CHF 0.15, Wochenauswahl CHF 0.30
   - Toggenburg: Frischbonus CHF 0.45, Dreifachpunkte CHF 0.27, Monatsziel CHF 0.13, Wochenauswahl CHF 0.32
   - Appenzellerland: Frischbonus CHF 0.58, Dreifachpunkte CHF 0.33, Monatsziel CHF 0.24, Wochenauswahl CHF 0.41

### offer_grid_2027.png

1. Heatmap with the six regions down the side and the four offers across, a chain-wide row on top (Frischbonus CHF 0.49, Dreifachpunkte CHF 0.26, Monatsziel CHF 0.16, Wochenauswahl CHF 0.34), every cell labelled with the values above, the Frischbonus column outlined and the Wochenauswahl marked as runner-up.
2. Title: put the Frischbonus on every card in 2027, CHF 0.49 net margin per active card-week, ahead of the Wochenauswahl at CHF 0.34.
