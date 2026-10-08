# DA45 — Which top-sites frame a measurement team adopts for a year of crawls, when list entries are aliases of the sites the crawler lands on

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · web measurement |
| Mirrors | Choosing a stable sampling frame when list entries are aliases of one underlying entity (regional app bundle IDs, seller storefront aliases on marketplaces, CDN hostnames for one service), so identifier churn is not churn in what is measured |
| Decision shape | A structure the body adopts: the crawl frame (provider, depth and unit of a list entry), scored on how little the set the crawler would actually visit changes from day to day |
| Committed call | The frame adopted, and its mean daily churn (one minus rank-biased overlap) to three decimals |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · an implicit join through a multi-hop chain (measured #18), with a normalisation validated on one band and applied to another at rung 2 (measured #13) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #18 joins only on the visible key · #13 validates on one population, applies to another · #3 stops at a close but inexact match |
| Calibration form | Gold-standard verification subsample: 2,000 top-10,000 domains whose landing site analysts verified by hand |
| Driving force | The crawler visits what a list entry lands on: it follows HTTP redirects and DNS aliases, up to five hops, to a landing site, as its documentation describes. Registrable domains look like the natural unit and match the gold standard 99.4% in the top band. Deeper in the lists, where the providers' own statistics show a third of entries redirecting, Dunlin's apparent churn is almost all alias rotation, and on landing sites it is the most stable provider. |

## 1. Situation

A security-measurement team crawls a top-sites list every week and wants results that change only when the web changes, not when the list
reshuffles. It will adopt one provider and depth for the year from four candidates. The pack holds 31 days of each provider's top 100,000,
the crawler's documentation and logs for every entry and day, the Public Suffix List snapshot, the providers' monthly statistics with
redirect shares by rank band, the team's protocol, and the gold-standard verification sample.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each list, each crawl log, each verified site, each provider statistic. Nobody ranks the providers
  on the decision's basis and nothing reported is overturned. The difficulty is what one entry is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the lab's report and both voices. Rank-biased overlap on registrable domains, checked against the gold
  standard at 99.4%, still adopts Corvid.
* **Instrument repair.** Suspect: the gold standard, which verifies only the top 10,000. Repaired by verifying every entry's landing
  site, rung 0 still adopts Avocet, rung 1 Bittern and rung 2 Corvid, since none uses a landing site; the full sample would only show
  rung 2's normalisation failing in the deep band. The lists and logs are complete and an alias is a correct entry, so the answer stays
  Dunlin and the overlap on collapsed landing sites is still needed.
* **Lens swap.** The naive frame compares domains across days; the answer compares landing sites, a different set of units in which many
  domains collapse into one.

## 3. The driving force

A strong solver discards Jaccard for rank-biased overlap, which weights the top, normalises entries to registrable domains, checks that
normalisation against the gold standard (1,988 of 2,000), and adopts Corvid. The gold standard covers only the top 10,000, though, and the
providers' own statistics say 2% of entries redirect there against 31% between ranks 10,000 and 100,000. Deep entries are often aliases:
rotating tracking domains, regional mirrors and parked names that redirect or alias to one landing site. The crawler visits the landing
site, and its logs record each chain. Collapsed to landing sites, Dunlin, whose list rotates aliases daily, churns 0.017 against Corvid's
0.027.

## 4. The ladder

| Rung | Frame | Adopts (mean daily churn) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Jaccard on raw domains, top 100,000 | Avocet (0.088, 1.27× Bittern) | The field's standard stability check | The protocol: findings are weighted by rank, and Jaccard treats rank 1 like rank 100,000 |
| 1 | Rank-biased overlap (p = 0.999) on raw domains | Bittern (0.041, 1.22× Avocet) | Top-weighted, as the protocol wants | The suffix list: subdomains and hosts of one registrable domain churn as separate entries |
| 2 | Rank-biased overlap on registrable domains, validated on the gold standard (1,988 of 2,000) | Corvid (0.030, 1.23× Bittern) | The normalisation passes the verified sample | The providers' statistics: 31% of entries below rank 10,000 redirect, against 2% in the verified band |
| 3 | **Decisive:** rank-biased overlap on landing sites, each entry followed through its redirect and alias chain in the crawl logs | **Dunlin (0.017, 1.59× Corvid)** (4th of 4 on rung 0) | — | — |

* **Position table.** Dunlin is 4th on rungs 0 and 1 (0.204 and 0.083) and 3rd on rung 2 (0.044), and leads only rung 3.
* **Discriminator dominance.** Corvid carries 1.47× into rung 3 (0.044 against 0.030). Landing sites cut Dunlin's churn to 0.39 of its
  rung-2 value and Corvid's to 0.90, an edge of 2.33×, against the 1.2 × 1.47 = 1.76 needed (1.32× headroom). The product, 2.33 / 1.47 =
  1.59, is the final margin.
* **Partial correction priced (L3).** A solver who follows HTTP redirects but not DNS aliases leaves Dunlin at 0.033 and adopts Corvid at
  1.22× better. One who resolves chains only for the verified top 10,000 leaves Dunlin at 0.039 and adopts Corvid at 1.44× better. No half
  adopts Dunlin.
* **Grid.** Similarity (Jaccard or overlap) × unit (domain, registrable domain, redirects only, full chain) = 8 cells. Seven adopt
  Avocet, Bittern or Corvid.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere as a frame rule.** The crawler documentation describes following chains to a landing site as an operational fact. The
   protocol says the frame is "the list the crawler visits". No document says to collapse entries before measuring stability.
2. **Pattern B, reproduction against the gold standard.** Chain resolution returns 2,000 of 2,000 verified sites; registrable domains 1,988
   and raw domains 1,912. The verified band barely separates them, so the decisive evidence is the providers' published redirect shares
   for the unverified depth. The chain is a construction: redirects and aliases followed hop by hop through the logs.
3. **No arithmetic symptom.** Lists have 100,000 entries every day, logs cover every entry, and overlap computations reconcile at every
   depth.
4. **Not a row predicate.** An entry's unit is the end of a chain of other entries' records, up to five hops away.
5. **The enumeration is arithmetic.** No list column names a landing site.
6. **No cutover date.** Alias rotation runs daily, with nothing stepping.
7. **Survives deletion.** With every voice removed, registrable domains still adopt Corvid.

## 6. The calibration corpus

* **Form.** The gold-standard sample: 2,000 domains from the four providers' top 10,000, each with its landing site verified by analysts.
* **What it certifies.** That registrable domains nearly always equal the site in the top band, which carries a solver to rung 2.
* **What it is blind to.** The deep band, where the gap opens (above).
* **Twin pair.** Bittern's and Dunlin's ranks 20,000 to 30,000 on days 11 to 12 match on domain-level churn (0.083), registrable-domain
  churn and entry count. Their landing-site churn is 0.040 and 0.020 (2.0×): two-thirds of Dunlin's changed entries are aliases of sites
  that stayed.
* **Resemblance points at the decoy.** On every list-level statistic, Dunlin resembles the providers the field calls noisy.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The protocol: one provider and depth for the year; the frame is the list the crawler visits; stability is rank-biased
  overlap at p = 0.999 over 30 consecutive day-pairs, extrapolated to depth 100,000.
* **Empirical pins.** The unit, from the crawl logs and the gold standard.
* **Voices.** The research lead: "Jaccard on the top 100,000 is the stability check everyone publishes." The infrastructure engineer:
  "Registrable domains are how everyone normalises."
* **Licensed wrong basis.** The protocol records that the partner lab reports provider stability by Jaccard and will present it at the
  methods review.

## 8. Determinism by construction

* **Chains.** Every chain ends within five hops, none cycles, and each day's crawl covers every entry of every provider.
* **Collapsed ranks.** A landing site takes the best rank among its entries that day, as the gold standard's site lists do.
* **Overlap.** Extrapolated overlap at depth 100,000 with p = 0.999; no provider's day-pair sits within 0.002 of another's at rung 3.
* **Suffixes.** One suffix-list snapshot for all 31 days.

## 9. Prompt sketch and deliverables

> We lock the crawl frame for next year on Friday, and the research lead would settle it the way the field always has. Tell me which frame
> we adopt, scored on how little what the crawler would actually visit changes from day to day, and its mean daily churn to three
> decimals, as the decision for the methods log. Send `frame_choice.xlsx`, a chart `churn_by_unit.png`, and a one-page `frame_note.pdf`.

* `frame_choice.xlsx` — churn for each provider under each unit, the resolution sheet (ask A), the liveness sheet (ask B) and the
  gold-standard table (ask C).
* `churn_by_unit.png` — each provider's mean daily churn as the unit moves from domain to registrable domain to landing site, one line per
  provider, with the redirect share by rank band inset and the adopted frame marked.
* `frame_note.pdf` — the adopted frame, its churn, and why the other frames fail.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each provider, the mean daily share of entries that resolve, and its lowest day. *Device:*
  the resolver log retries a server failure within ten minutes and records the retry's outcome, as its note says; counting the first
  failure understates resolution for three providers.
* **Ask B (device-carried).** For each provider, the share of entries whose landing page is live. *Device:* the crawler's classifier flags
  soft-404 pages that return status 200 with an error template; counting them live overstates every provider.
* **Ask C (validity).** Each provider's churn under each of the four units, and gold-standard matches for each normalisation.
* **Decoupling.** Clearing the chain resolution changes no figure in asks A or B.

## 11. Rubric arithmetic

4 providers × 2 (ask A) + 4 providers (ask B) + 4 × 4 churn figures and 3 match counts (ask C) + the adopted provider, unit, depth and its
churn + 5 named chart parts + 3 files ≈ 43 criteria.

## 12. World-building constraints

* Churn by rung: Avocet 0.088 / 0.050 / 0.049 / 0.045; Bittern 0.112 / 0.041 / 0.037 / 0.031; Corvid 0.131 / 0.058 / 0.030 / 0.027;
  Dunlin 0.204 / 0.083 / 0.044 / 0.017.
* Redirecting entries: 2% in the top 10,000, 31% from 10,000 to 100,000; Dunlin rotates aliases for 4,100 sites daily.
* Gold standard: chains 2,000, registrable domains 1,988, raw domains 1,912.
* Resolver retries and soft-404 flags never touch a chain or a rank.
