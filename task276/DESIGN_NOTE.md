# task276 design note

## Draw

Not yet drawn: the guard blocks the architecture below on `ban.strategy` (composition_mix, task179 v3 in the last three live builds) and warns `overuse.strategy` (3 of the last 12). It is drawn the day the window clears; relabelling it to pass the guard would be a lie on the card.

Seed DA26, kept as world, decision and quantity: a code-hosting platform's developer-relations team can staff one community's launch of pair-review sessions, and the slot goes to the community whose launch reaches the most developers. Pairing: `product-analytics` / `feature-adoption-diffusion-modeling` (DD).

Architecture prototyped (scratch prototype, 2026-10-23): the launch seeds 2,500 active members at random and counts the seeded developers plus every collaborator who accepts one of their invitations within 30 days, invitations going out together on activation. A pair-review invitation is worth accepting only when several team-mates already have the feature, so a developer's chance of accepting rises steeply with the number of seeded collaborators who invite them (prototype curve 0.05, 0.19, 0.36, 0.50, 0.58 for one to five invitations). Fourteen pilot seedings ran two designs: random members (almost every invitee invited once) and half of each enrolled team (invitees invited several times). The pilots' per-seed yield, or a per-invitation rate with overlap, carries the pilots' exposure mix onto a launch whose density invites most developers of a dense community several times; only the acceptance per number of invitations, pooled across communities where every community's observed counts agree, applied to each community's exposure distribution at launch density (each developer's collaborators among the active members, seeded at random), names the golden community. Prototype: linear yield and independent invitations name Embedded systems (4,701 and 4,264), the exposure-response route and the world name Infrastructure (5,687 against 4,996, truth 5,653). To meet the ladder's separation, Infrastructure's own pilots are the random-member design (its yield looks low on every easy route), and the margins are tuned to 1.2x before the draw.

## Tried and rejected

- Overlap and saturation alone (`binding_constraint`, G8): the first-order correction a careful analyst makes by reflex (collaborators already seeded cannot be invited) lands the call, and overlap among invitees is a second-order effect at launch densities that stay plausible.
- Acceptance delay completed community by community (`maturity_censoring`): the nowcast by unit-specific delay is task181's and task451's driver.
- A dated platform campaign inflating some pilots (`decomposition_attribution`): a cause with a cutover date is adjusted by reflex (the strategy record, F8).
- The pilots' evidence judged at the pilot rather than the invitation (`uncertainty_hold`): the client's record has interval stumps landing on the natural computation.
