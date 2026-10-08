# DA40 — How local are people's friendships? A connectedness index needs destination weights

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Social platforms describing the geography of friendships for local features (marketplace radius, events, local news); any normalised pairwise index that must be re-weighted to answer a share question |
| Domain | Social networks / local products |
| Task shape | 14 · Cuts of a distribution (share of each county's friendship links within 50, 100, 200 and 500 miles for 10 metro counties; the county where a local-marketplace pilot is launched) |
| Core method | Social Connectedness Index (SCI) is proportional to friendship links ÷ (users_i × users_j); estimated links ∝ SCI_ij × pop_j (destination population as user proxy, per memo); distance-band shares = Σ_j in band SCI_ij pop_j ÷ Σ_j SCI_ij pop_j |
| Analytical stump | Averaging SCI over destinations within a radius (unweighted) answers "how connected is a typical county pair", not "what share of a person's friends live nearby". Large destinations hold most friends; the index must be converted back to link shares by multiplying by destination size |
| Primary sources | Meta Data for Good — Social Connectedness Index (US county–county); Census county population estimates and centroids |

## 1. The real-world situation

A local-marketplace team will pilot a 100-mile "nearby" radius in one metro county where the largest share of users' friends live within 100
miles. An analyst computed the mean SCI of counties within 100 miles divided by the mean SCI of all counties and picked a county with many
small, highly connected neighbours. The team asked for the share of friendships within the radius.

## 2. The decision (one deterministic recommendation)

**The pilot county (highest share of friendship links within 100 miles among 10 candidate metro counties), with 50/100/200/500-mile shares for
all ten.**

Rules (growth memo):

* Data: SCI county-county file (release in memo); county populations (same year); county population-weighted centroids.
* Distance: great-circle between population-weighted centroids; own county distance = 0.
* Link share within d miles for county i = Σ_{j: dist ≤ d} SCI_ij × pop_j ÷ Σ_j SCI_ij × pop_j (including j = i).
* Candidates: 10 metro counties in `candidates.csv`.
* Pilot: highest 100-mile share; ties → larger population.

## 3. Why capable analysts get it wrong

* SCI is a relative index; its unweighted average is not a share.
* Friends are concentrated in populous destinations.
* Own-county links are the largest single component and must be included.
* Geographic centroids misstate distances for large counties.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `county_county.tsv` | TSV | ~10.3M pairs | Meta Data for Good SCI | CC BY 4.0 (per Data for Good terms; verify) | SCI values |
| 2 | `sci_methodology.pdf` | PDF | — | Bailey et al., JEP 2018 (cite) | Cite | Index definition |
| 3 | `co-est<yyyy>-alldata.csv` | CSV | ~3.2k | Census Bureau | Public domain | Populations |
| 4 | `CenPop2020_Mean_CO.txt` | Text | ~3.2k | Census Bureau | Public domain | Population-weighted centroids |
| 5 | `candidates.csv` | CSV | 10 | Task author | — | Candidate counties |
| 6 | `growth_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `analyst_mean_sci_ratio.xlsx` | XLSX | 10 | Task author | — | Naive ranking |
| 8 | `distance_matrix_candidates.parquet` | Parquet | ~32k | Derived | Public domain | Distances |

## 5. Deterministic solution path

1. Load SCI rows for candidate origins; join populations and centroids.
2. Distances; weighted shares by band.
3. Choose pilot; contrast with mean-SCI ratio ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — unweighted mean SCI.** Not a share.

**B — excluding own county.** Shares understated.

**C — geographic centroids.** Distances distorted.

**D — weighting by origin population.** Wrong side of the pair.

## 7. Why the stump is analytical, not semantic

The index definition and weighting are specified. The trap is interpreting a normalised index as a share without re-weighting.

## 8. Draft task prompt (prose)

> Where should we pilot the 100-mile marketplace radius? Convert SCI to friendship shares by distance band as the growth memo specifies.
> Provide `distance_band_shares.csv` (county: shares within 50/100/200/500 miles), `share_curves.png`, and a one-page `pilot_county.pdf`.

## 9. Deliverables

* `distance_band_shares.csv`, `share_curves.png`, `pilot_county.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 counties × 4 bands = 40 shares (sampled); pilot; contrast.

## 11. Golden-output checklist

* Destination weighting; own-county inclusion; centroids; bands; choice.

## 12. Build notes (scope tuning)

* Confirm the naive ranking's top county is not the weighted-share leader.
