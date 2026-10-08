# AD32 — Upcoding screens: high-level visits are normal for some specialties, and small panels swing

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Health-insurer special-investigation units and payment-integrity vendors; marketplace teams comparing a seller's price or category mix against true peers |
| Domain | Healthcare payment integrity |
| Task shape | 01 · Ranked list under a cap (40 clinicians for medical-record review) |
| Core method | Each clinician's distribution across established-patient office visit levels (99211–99215) against the specialty × state peer distribution; multinomial likelihood-ratio (G) statistic with a volume-aware p-value; direction check (shift toward higher levels); Benjamini–Hochberg control |
| Analytical stump | Ranking by share of level-5 visits flags specialties that legitimately see complex patients and low-volume clinicians whose shares swing. Peer-specific expected mixes and a statistic that accounts for volume separate unusual coding from case mix and noise |
| Primary sources | CMS "Medicare Physician & Other Practitioners — by Provider and Service" public use file |

## 1. The real-world situation

A payer's integrity unit can review records for **40** clinicians a quarter. The current screen ranks clinicians by the share of
established-patient visits billed at level 5 (99215). The list is dominated by oncologists and cardiologists and by clinicians with
a few dozen visits; reviewers found mostly appropriate coding.

## 2. The decision (one deterministic recommendation)

**The 40 clinicians selected for review, ranked by significance of an upward shift from their peer mix, and the 41st.**

Rules (integrity memo):

* Data: the 2022 provider-and-service file; HCPCS 99211–99215, place of service non-facility; services counted by `Tot_Srvcs`.
* Peers: same `Rndrng_Prvdr_Type` and state; peer distribution = pooled services excluding the clinician; peers with < 30 clinicians use
  the national specialty distribution.
* Eligibility: ≥ 200 services across the five codes.
* Statistic: G = 2 Σ O_k ln(O_k ÷ E_k), p-value from χ² with 4 df.
* Direction: mean level (1–5) above the peer mean by ≥ 0.25.
* BH at q = 0.01 across eligible clinicians; among discoveries with upward direction, rank by G ÷ total services (effect per visit),
  ties by G. Top 40; report #41.

## 3. Why capable analysts get it wrong

* Single-share thresholds ignore specialty and regional norms.
* With hundreds of thousands of clinicians, small p-values are common; multiple-testing control is needed.
* Ranking by G alone favours very high-volume clinicians with small deviations; the memo ranks by effect among discoveries.
* Including the clinician in the peer pool shrinks deviations in small specialties.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `MUP_PHY_R24_P05_V10_D22_Prov_Svc.csv` | CSV | ~9.8M | CMS data.cms.gov | U.S. Gov public domain | Provider × service rows |
| 2 | `MUP_PHY_R24_P05_V10_D22_Prov.csv` | CSV | ~1.2M | CMS | Public domain | Provider summary (context) |
| 3 | `methodology_prov_svc.pdf` | PDF | — | CMS | Public domain | Suppression (< 11 beneficiaries), definitions |
| 4 | `em_code_levels.json` | JSON | 5 | Task author | — | Code → level |
| 5 | `integrity_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `current_level5_share_list.xlsx` | XLSX | 40 | Task author | — | Current screen |
| 7 | `specialty_state_peer_counts.parquet` | Parquet | ~5k | Derived | Public domain | Peer sizes |
| 8 | `bh_procedure_citation.pdf` | PDF | — | Cite | Cite | FDR control |
| 9 | `nppes_taxonomy_lookup.csv` | CSV | ~900 | NUCC (public) | Public | Context |
| 10 | `review_capacity.json` | JSON | 1 | Task author | — | Cap |

## 5. Deterministic solution path

1. Filter codes and place of service; pivot to clinician × level counts.
2. Leave-one-out peer distributions with the fallback rule.
3. G statistics and p-values; direction; BH.
4. Effect-per-visit ranking; top 40 + #41; overlap with the current list.

## 6. Wrong paths (method errors, not misreadings)

**A — level-5 share.** Specialty mix dominates.

**B — no peer stratification.** Oncology flagged wholesale.

**C — raw p-values without FDR.** Thousands of "significant" clinicians.

**D — ranking by G only.** Volume dominates effect.

## 7. Why the stump is analytical, not semantic

Codes, peers and statistics are specified. The traps are case-mix comparison and multiple testing at scale.

## 8. Draft task prompt (prose)

> Build this quarter's 40-clinician review list using the peer-divergence screen in the integrity memo. Provide `review_list.csv` (clinician:
> specialty, state, services, level mix, peer mix, G, q-value, effect, rank), `mix_vs_peer.png` (the top five clinicians' level mixes beside their
> peers'), and a one-page `review_selection.pdf` including how many of the current list remain.

## 9. Deliverables

* `review_list.csv`, `mix_vs_peer.png`, `review_selection.pdf`.

## 10. Where 25+ rubric criteria come from

* 40 clinicians + #41; peer mixes for 3 specialties; G and effect for 6 clinicians; discoveries count; overlap.

## 11. Golden-output checklist

* Code filter; leave-one-out peers; fallback; G; BH; direction; ranking.

## 12. Build notes (scope tuning)

* Restrict to a subset of states if compute is heavy, keeping peer sizes adequate.
* Confirm that fewer than a quarter of the current list survives.
