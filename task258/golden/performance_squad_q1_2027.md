# Performance squad, quarter from 5 January 2027: Trailhead

To: Margaret Good, Head of Web Platform  
From: Tasha Murillo, performance squad lead  
For the web platform steering group's December planning, 8 December 2026

**Send the squad to Trailhead.** The hero-image playbook would move 4.9 million of Trailhead's page loads a month into the good LCP band (2,500 ms or less), the most of our six properties; Matchday is next at 3.4 million.

## What the playbook would do at each property

| Property | Page loads moved into the good band, a month | Hero-image egress on the image CDN, GB a month | At the contract rate, AUD a month | Live hero images to convert to AVIF |
|---|---:|---:|---:|---:|
| Trailhead (squad) | 4.9 million | 1,259 | $89 | 2,444 |
| Matchday | 3.4 million | 1,217 | $86 | 4,478 |
| Pantry | 3.3 million | 770 | $55 | 3,742 |
| Hearth | 3.2 million | 2,102 | $149 | 2,777 |
| Ledger | 3.0 million | 1,056 | $75 | 2,168 |
| Tideline | 2.6 million | 1,997 | $142 | 6,741 |

Page loads are November 2026's in Sydney time on our RUM, each beacon standing for 1 / the sampling rate in force when its page load started. Egress is costed on November's hero-image requests; the hero images are those the DAM shows in use on 2 December. The chart is lcp_reach_q1_2027.png.

## How the counts were built

The playbook can only move a page load slower than 2,500 ms whose LCP element is the property's own hero image (charter 2.4). Each of those loads was rebuilt part by part the way the squad's eleven past engagements landed. Time to first byte stays as it is. The image's load time falls to 0.48 of what it was (AVIF at the slot size). Where the hero is preloaded, its load delay goes to 240 ms whatever it was before: on every engagement the after-window median sat between 232 and 247 ms, from before-window medians of a little over 100 ms to nearly 3,000 ms, because a preloaded hero waits only on the connection to the image CDN.

The preload is written into the page's document head (step 3 on the Playbook sheet), so it can only name a hero the page's own HTML carries. Every engaged site served its hero in the article's HTML. Ours do not everywhere: on the 2 December crawl, the pages of Tideline's /live/, Matchday's /live/, Ledger's /markets/ and Pantry's /planner/ carry no hero at all, only the site logo, because those sections are apps that put their hero on the page after the app's own code has run. The squad does no work on scripts or the render path (charter 3.2), so on those pages the hero's request starts when it starts today, and their first byte and load delay alone already run past 2,500 ms: AVIF or not, none of those loads moves. That is 2.9 million of Matchday's slow page loads on its own heroes. Preloaded everywhere, Matchday would come first (6.3 million); it moves 3.4 million.

The rebuilt paint also comes no sooner than the page's own first contentful paint, which the playbook leaves where it is. At Brolga Kids (E06) and Fairway (E10) the render delay's median went from 377 and 462 ms to 2,321 and 2,245 ms once the hero arrived early, and the paint landed on the page's first paint, about three seconds after its first byte. On the other nine engagements the pages first painted soon after their first byte and the render delay held. With the render delay held as it is today, Pantry would come first (8.0 million), because its hero images wait longest to start loading; most of its slow loads are on pages that first paint about three seconds after their first byte, and it moves 3.3 million.

Trailhead has none of those app sections and few pages held from painting, so nearly all of its gain stands. Carried as a ratio of medians, or as a preload that removes the delay, the engagements would put Ledger first (8.8 million and 9.7 million) by shrinking its already short delays further; on the image CDN those delays rise to the connection time, and Ledger moves 3.0 million. Hearth has the most slow page loads on its own images (20.4 million), but its paint is held by time to first byte, which is the Hearth team's work, not the squad's.

## Notes

- Egress counts November's hero-slot requests answered with the image (revalidations answered 304 carry none) on each property's image host and image CDN path, and on the legacy aliases from the old media server's own log, at the mean AVIF size of the property's hero slot and AUD 0.071 per GB.
- Hero images are the DAM's hero assets in use on 2 December, counted once each (renditions together, and a migrated asset's library record together with its DAM record) under the property whose page carried it: the heroes of the three sections moved in March 2025 are their new property's own, though the DAM still files them under the collection they were uploaded to.
