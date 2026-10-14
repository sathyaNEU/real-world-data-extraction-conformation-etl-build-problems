# Performance squad, quarter from 5 January 2027: Matchday

To: Margaret Good, Head of Web Platform  
From: Tasha Murillo, performance squad lead  
For the December planning, 8 December 2026

**Send the squad to Matchday.** The hero-image playbook would move 4.6 million of Matchday's page loads a month into the good LCP band (2,500 ms or less), the most of our six properties; Ledger is next at 3.3 million.

## What the playbook would do at each property

| Property | Page loads moved into the good band, a month | Hero-image egress on the image CDN, GB a month | At the contract rate, AUD a month | Live hero images to convert to AVIF |
|---|---:|---:|---:|---:|
| Matchday (squad) | 4.6 million | 1,208 | $86 | 4,210 |
| Ledger | 3.3 million | 1,056 | $75 | 2,044 |
| Hearth | 3.2 million | 2,102 | $149 | 2,777 |
| Tideline | 3.1 million | 1,971 | $140 | 6,362 |
| Pantry | 2.9 million | 653 | $46 | 3,543 |
| Trailhead | 1.8 million | 667 | $47 | 2,444 |

Page loads are November 2026's in Sydney time on our RUM, each beacon standing for 1 / the sampling rate in force when its page load started. Egress is costed on November's hero-image requests; the hero images are those live on the 2 December crawl. The chart is lcp_reach_q1_2027.png.

## How the counts were built

The playbook can only move a page load slower than 2,500 ms whose LCP element is the property's own hero image (charter 2.4). Each of those loads was rebuilt part by part the way the squad's 11 past engagements landed. Time to first byte stays as it is. The image's load time falls to 0.48 of what it was (AVIF at the slot size). The image's load delay goes to 240 ms, whatever it was before: on every engagement the after-window median sat between 232 and 247 ms, from before-window medians of a little over 100 ms to nearly 3,000 ms, because a preloaded hero waits only on the connection to the image CDN.

The rebuilt paint then comes no sooner than the page's own first contentful paint, which the playbook leaves where it is: the squad does no work on scripts, fonts or the render path (charter 3.2). At Brolga Kids (E06) and Fairway (E10) the render delay's median went from 377 and 462 ms to 2,321 and 2,245 ms once the hero arrived early, and the paint landed on the page's first paint, about three seconds after its first byte. On the other nine engagements the pages first painted soon after their first byte and the render delay held.

That floor decides the quarter. With the render delay held as it is today, Pantry comes first (6.8 million), because its hero images wait longest of all to start loading. But most of Pantry's slow loads are on its recipes, dinner, quick-meals and healthy pages, which first paint about three seconds after their first byte, and no faster image brings those under the line: Pantry moves 2.9 million. Most of Matchday's pages first paint soon after their first byte, so most of its gain stands.

Carried as a ratio of medians, or as a preload that removes the delay, the engagements put Ledger first (7.4 million and 8.4 million), because they shrink Ledger's already short delays further. On the image CDN those delays rise to the connection time, and Ledger moves 3.3 million.

Hearth has the most slow page loads on its own images (20.4 million), but its paint is held by time to first byte, which is the Hearth team's work, not the squad's.

## Notes

- Egress counts November's hero-slot requests answered with the image (revalidations answered 304 carry none) on each property's image host and image CDN path, and on the legacy aliases from the old media server's own log, at the mean AVIF size of the property's hero slot and AUD 0.071 per GB.
- Hero images are the DAM's hero assets on the 2 December crawl, counted once each (renditions together, and a migrated asset's library record together with its DAM record) under the property whose page carried it: the heroes of the three sections moved in March 2025 are their new property's own, though the DAM still files them under the collection they were uploaded to.
