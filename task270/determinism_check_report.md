# determinism-check report, task270 architecture 6

## Round 1 (run 20261026143254, the first architecture 6 pack)

- **Verdict:** DETERMINISTIC (main call forced). Two unfiled conventions leave graded sub-figures (B share, lead) open to a one-decimal fork; see Evidence.
- **Disposition:** FIX_NOW. Pin in briefing clause 3.3/3.4 (or dicionario_dados) that seconds watched are summed across a member's records on the channel and that a rotation spot is read at the places where the bookings sold for that reference day aired. No change to the analytic surface; no rerun needed for the call.
- **Why:** Executing clauses 3.2 to 3.5 literally on the shipped files gives A 26.56, B 22.07, C 16.86 per cent reached 3+ times, so A leads B by 4.5 points and the call is not close under any reading tried (A wins by 4.4 to 4.6 points in every variant that follows the briefing). The rotation spots of B were sold for prime time but 1,521 of 4,545 aired in daytime, which the briefing's "probability of having passed there" lets a solver recover from the as-run log. Only the one-decimal B share and the lead depend on conventions the text does not close (taxonomy label if a reviewer insists: underspecified_objective, minor, supplementary asks 1 and 2 only).
- **Evidence (recomputed from target/):**

| Quantity | Golden | Recomputed | Source |
|---|---|---|---|
| Rotation prime bookings on VRT, LIT, PLS, PLSP | 4,545 | 4,545 | reservas (janela Horário nobre) joined to emissao on id_reserva |
| of which aired outside 20:00-00:30 | 1,521 (33.5%) | 1,521 | emissao hora_inicio |
| Panel 18-34 weight (universe) | 2,100 thousand | 2,100,002.8 (571 members, weight above 0) vs universo_2026 2,100,000 | individuos, universo |
| A, reach 3+ | 26.6 | 26.5635 | visionamentos live, members, 28-day weight, Lisbon clock |
| B, reach 3+ | 22.1 | 22.0658 (seconds summed across records) | same |
| C, reach 3+ | 16.9 | 16.8640 | same |
| Lead A over B | 4.5 | 4.4977 | |
| Portal baseline (documento_hash, first first-donation booking, age on booking date, Mon-Sun weeks 10 Mar to 6 Apr 2025) | 135.5 | 135.5 (123, 142, 132, 145) | marcacoes_portal_dador_2025.csv, notas_extracao |
| Campaign weeks minus baseline | 93.5, 100.5, 121.5, 107.5; 423.0 | same (229, 236, 257, 243) | same |
| Response per thousand | 0.77 | 0.7722 (423.0 / 547.8) | relatorio 2025, 3+ people 547.8 thousand |
| Expected bookings A, B, C | 430, 360, 270 | 430.7, 357.8, 273.5 (also 429.5, 356.8, 272.7 with 0.77) | share times 2,100 thousand times response |

Costs reproduce (A 227,710; B 229,600; C 229,460, all within 230,000 at the price tables). Place counts: every first-place and last-place spot resolves to exactly one as-run place.

Forks tested (the literal reading is silent):
1. Seconds across split records. Single-record overlap: B 22.047 (prints 22.0), A 26.563, C 16.864, lead 4.5. Summed across a member's records (literal "at least half the seconds"): B 22.066 (22.1). B's one-decimal share and the expected-bookings figure 360 are unaffected in the call but the printed B share flips 22.0 vs 22.1. The golden margin to the 22.05 rounding line is 0.016, thin. 3,931 consecutive same-channel records sit within 120 s of each other, so this is real.
2. Which bookings define "that reference day's" rotation bookings. Sold for the day (reservas dia_tv): B 22.066, lead 4.5. Aired on the day (emissao dia_tv; 924 rotation spots sold for day d aired on d+1): B 21.995 (22.0), lead 4.6. Expected bookings unchanged to the nearest ten (A 430, B 360, C 270).
3. Denominator: 2,100,002.8 against 2,100,000, no effect.
4. Strict greater-than half: A 26.40, B 21.90, C 16.86; same winner, lead 4.5.
5. Easy route that ignores the as-run (rotation spread over prime breaks): B 40.3 (all prime breaks) or 31.8 (prime-aired places only), A 26.6, so the surface read picks B.
Portal side: counting rows gives 181.5 baseline and 0.67; counting donor numbers gives 164.0 and 0.59; counting documento_hash gives the golden. The notas file files "cada pessoa conta uma vez", and the dictionary and notes say the portal go-live created second donor numbers, so documento_hash is the literal person key (closed).

Facts located in files: rule for a "view" and place reading (briefing 3.2 to 3.5), clock (audimetria_nota_metodologica s.2), code change PLS to PLSP on 16 March (canais_codigos.csv), response rule (notas_extracao_portal_dador.txt), 3+ people reached in 2025 (relatorio 2025). No external fact needed.
- **Files/Hygiene:** PASS. 18 files; formats csv, pdf, xlsx, txt (four). One file of 441,227 rows (visionamentos) plus 20,545 and 19,980 row logs. Distractors available and unused: dadores_novos_2025.csv, plano_digital_2027.csv, audiencias_programas_semanais_2026-03.csv, tabelas_precos_2T2027.pdf (prices only pin schedule cost), grelha_programacao. Files read as system exports (UTC stamps, code lists with validity dates, hashed documents). Dates coherent (briefing 28 Oct 2026, drafts 17 Nov 2026, April 2027 campaign). No authoring or benchmark language seen. Not exclusion-level. Note: the briefing is dated 28 October 2026 and the xlsx says 17 November 2026, which matches the stated calendar.
- **Stump power:** Good. The trap that does the work is placing B's rotation spots where the channels actually aired them (a third in daytime breaks); the easy read that rotation sits in the sold prime window gives B 31.8 to 40.3 against A 26.6 and picks the wrong schedule. The second layer (documento_hash person dedup) cuts the response from 0.67 to 0.77, which moves the expected bookings and weekly asks. A strong model that fails to join the as-run log files a wrong call.
- **Stumping type:** `mechanism: method_or_model_selection` (exposure reconstruction from as-run placement), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported inputs (price tables, briefing rules) are fine; the difficulty is estimating where unplaced spots would have aired; it still stumps on clean data. Borderline note: part of the placement step is executing clause 3.4 on a join.
- **Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: panel clock UTC against legal time with the 29 March change, PLS to PLSP code change, a TV day running to 26:00, split viewing records, duplicate donor numbers after the portal go-live. Layer 2: reach and frequency (3+) of a media plan estimated from audience measurement with the placement uncertainty of rotation spots, then response per thousand reached applied to expected bookings; swap test fails the backdrop reading (reach-frequency modelling is the media-planning core). Easy route: take rotation spots as sitting in the sold prime window, giving B 31.8 to 40.3 per cent and a B purchase. Caveat: because clause 3.4 states the place-probability rule, a reviewer could class the join as rule application; I class it analytical because the clause does not say how to estimate the probabilities and the sold window is the plausible wrong estimate.
- **Fix:** input_files/prompt (non-decisive, in-house): add one sentence to clause 3.3 that seconds are summed over all of a member's live records on the channel, and one to clause 3.4 that a rotation spot's places are those where the bookings sold for the reference day aired; consider moving B's printed share off the 22.05 rounding line only if the author prefers more margin. Main call stays frozen.

## Repair after round 1 (2026-10-26)

- Clause 3.3 now sums all of a member's live statements on the channel inside a place ("somados todos os seus registos nesse canal").
- The channels' traffic places a sold-out window's excess only in the same day's daytime breaks, so every rotation booking airs on the TV day it was sold for and the bookings sold for a reference day and the bookings aired that day are one set (SF7 in `generator/checks.py`, 0 of 10,443 off their day).
- The prime-time oversell rose from 1.45 to 1.6 and the traffic draw was re-seeded: the golden is A 26.6, B 20.9, C 16.9, lead 5.7 (margin 1.27), with B's share 0.028 and the lead 0.035 from their rounding edges.
- The asks were re-sited onto the donor record read on the extraction day (see the design note's ask sheet); the 2025 report's three-plus reach is 26.0 per cent (543.7 thousand), response 0.82, expected bookings A 460, B 360, C 290.

## Round 2 (run 20261026T154020, target.zip 34fd25351da2421267902c552cb1f377)

- **Verdict:** DETERMINISTIC
- **Disposition:** SEND_BACK. The Gate G and Gate H findings below (the decisive step is catching that Schedule B's nominal prime-time rotation lands in daytime) are repaired only by rebuilding the decisive step, so a rerun is required. The determinism gates themselves need no change.

- **Why:** Executed word for word, briefing clauses 3.2 to 3.5 and the portal extraction note give one answer. Schedule A reaches 26.6 per cent three or more times, B 20.9 and C 16.9, a 5.7 point lead for A over B. All three reproduced from the shipped files. Every variant I could license puts A first, except trusting the rotation window by the clock, which gives B 31.8. The call and the supplementary answers are forced. The governing taxonomy label for the disposition is banned_stumping_type, not a determinism failure.

## Evidence (recomputed from target/)
| Value | Golden | Mine | Source |
|---|---|---|---|
| Prime-window rotation bookings on Vértice, Litoral and Pulsar+ | 4,943 | 4,943 | reservas_publicidade_2026-03.csv (colocacao ROTAÇÃO, janela Horário nobre) |
| Of those, aired outside prime time | 1,854 (37.5%) | 1,752 aired between 07:00 and 16:59, plus 276 in the 00:00 hour, of which about 102 are after 00:30. Consistent with 1,854, but I did not derive 1,854 exactly. | join to emissao_publicitaria_2026-03.csv on id_reserva; all 4,943 match once |
| Reach of three or more, A | 26.6 | 26.56 | esquemas xlsx, visionamentos, individuos, emissao |
| Reach of three or more, B | 20.9 | 20.88 | same |
| Reach of three or more, C | 16.9 | 16.86 | same |
| Lead of A over B | 5.7 | 5.68 | |
| Baseline average and the four campaign weeks above it | 136.0; 85.0, 118.0, 99.0, 144.0; 446.0 total | 136.25; 84.75, 117.75, 98.75, 143.75; 445. Reproduces exactly (136.0, 85, 118, 99, 144, 446) only when the person's age is read at their first first-donation booking. | marcacoes_portal_dador_2025.csv |
| Response per thousand reached three or more times | 0.82 | 0.8203 or 0.8185, both 0.82 | 543.7 from relatorio_campanha_jovens_2025.pdf |
| Expected bookings A / B / C | 460 / 360 / 290 | 457.6 / 359.5 / 290.4, which round to 460 / 360 / 290 under either response | |

The method I ran:
- Panel members of 18 to 34 with 28-day weight above zero, live viewing only.
- UTC converted to local time with the 29 March clock change.
- Pulsar and Pulsar+ merged.
- A seen place needs half its seconds watched live, summed over all records on the channel.
- First and last places taken from the as-run log.
- Rotation spots spread over the places where that day's prime-window rotation bookings on the channel actually aired.
- Independent spots, a Poisson-binomial for three or more, weights over the 2.1 million universe. The weights sum to the 2,100,003 universe, so there is no denominator fork.

Forks tested, with the answers they give:
1. Rotation place distribution (clause 3.4 is silent on which bookings define "the probability of having passed there"):
   - Same-day prime-window bookings, as filed in the golden: B 20.9, lead 5.7.
   - All rotation spots that day: B 18.5, lead 8.1.
   - Prime bookings pooled by weekday: B 21.1, lead 5.5.
   - Prime bookings pooled over all days: B 21.1, lead 5.5.
   - Rotation read by nominal clock 20:00 to 00:30, or only the prime-window bookings that aired in prime: B 31.8, so B would win. This is the designed easy route, and it is excluded by the filed clause 3.4 (probability of having passed there), not by a stated rule.
   - Result: the call A is robust to every evidence-based variant. The graded B share and the lead (5.7 against 5.5) depend on the unstated choice of same-day, same-window bookings. That is the natural reading, because the spot is a "Rotação horário nobre" booking and the clause 3.2 day mapping applies, but it is not written in the briefing. This is a residual minor fork on graded figures, not on the call.
2. Age edge in the booking baseline. One person (F7B7B70223C1EB71) is 17 at their first first-donation booking on 3 March and 18 at their second booking on 27 March.
   - Age read at the person's first booking, which is what the extraction note's "Cada pessoa conta uma vez, na data da primeira marcação ... idade no dia da marcação" literally gives: baseline 136.0, weeks 85.0, 118.0, 99.0, 144.0, total 446.0.
   - Age filtered per booking: baseline 136.3, weeks 84.8, 117.8, 98.8, 143.8, total 445.0.
   - Both give response 0.82 and the same bookings to the nearest ten. The golden is the literal reading, but the fork on the one-decimal weekly figures is real, from a one-person edge.
3. Person identity and first-donation test. Persons are identified by documento_hash. Using tipo_dadiva or the single id_dador gives a baseline of 42.75 or 146.75 and a response of 0.13 or 0.74, both wrong. The earliest data_primeira_dadiva across a person's numbers (314 people hold two numbers) is forced by notas_extracao_portal_dador.txt. Booking date against first donation date makes no difference at the single same-day case.
4. No expected-bookings fork: both response roundings give the same tens.

Hygiene on the supporting facts:
- The 29 March change-over and the PLS to PLSP rename are documented in the nota metodologica and canais_codigos.csv.
- No place was missing for the 30 + 50 first-place and last-place spots.
- Within a channel there are no overlapping viewing records per person, so summing records is unambiguous.

## Files/Hygiene: PASS
18 files: csv x12, pdf x4 (briefing, nota metodologica, 2025 report, price tables), xlsx x1, txt x1 (plus the pptx and xlsx deliverables are outputs, not inputs). The largest is the 441k-row viewing file. Distractors usable: plano_digital_2027.csv, audiencias_programas_semanais, dadores_novos_2025.csv, tabelas_precos_2T2027.pdf. They read as system exports, with no authoring or benchmark language, no README and no temporal incoherence (briefing of 28 October 2026, drafts of 17 November 2026, extract of 2 July 2025). No exclusion-level finding. Real-looking fictional entities only.

## Stump power
Two trap layers. The first is on the rotation: a strong model reading the rate card and Schedule B's name takes the rotation as prime-time-by-clock and reports B at about 31.8 against A at 26.6, buying B. Catching it needs the join of reservations to the as-run log, where 37.5 per cent of the "prime" rotation bookings landed in daytime. A model that skims the briefing and does not join the files will fall for it, so the stump is plausible. The second layer is the portal identity and first-donation test, which is a plain wrong-answer trap for ask 3 (a person against a donor number, 0.13 or 0.74 against 0.82). Both are heavily specified by the shipped text, so a careful reader may clear both.

## Stumping type (Gate G)
`mechanism: planted_defect_flip`, `stumping_family: surface_read_rejection`, `surface_read_dependency: yes`, `sole_data_defect: yes`.

Banned scaffold: the primary stumping strategy is catching that Schedule B's nominal prime-time rotation (the rate card and schedule label) is misleading, and flipping away from it. The clean-data test collapses the task. If rotation had aired in its window, B at about 31.8 would simply beat A, so the task only works because the rotation placement is damaged. Rebuild the difficulty where the reported reads are fine, for example a frequency-response or saturation question on honest delivery, or a binding constraint or a validated forecast of the reach-to-bookings response. If the author disagrees on the call, this item is borderline and should go to live testing.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: planted`.

- Domain: media planning (reach and frequency, cover at three or more, delivery of rotation spots, a response-per-reach estimate) passes the swap test.
- Layer 1: the 29 March clock change in UTC viewing, the Pulsar to Pulsar+ rename, the one person holding two donor numbers, and the preliminary baseline on an extract of mixed dates.
- Layer 2: reading each spot where it would have passed, and a response estimated from a clean baseline.
- Decisive step: the solver must find that the "prime-time" rotation bookings were placed in daytime breaks (1,854 of 4,943). That is a defect inserted so that catching it flips B to second place, with the rest of the pipeline being the executed rules of clauses 3.2 to 3.5. Easy route: read the rotation as sitting in the 20:00 to 00:30 window, which gives B 31.8 against A 26.6, and buy B. A strong analyst who cleaned the data and read every clause correctly could still take it. So H3 fails as planted, and arguably as rule application.
- Fork: asks 3 and 4 are data semantics and rule application, which are allowed in the asks.

## Fix
Where: input_files and prompt, a rebuild of the decisive step (rerun required). Make the decisive quantity a field-native estimate on honest data. For example, keep the rotation honestly delivered and let the choice turn on a saturation or a frequency response validated out of sample, or on a binding budget constraint. If the build is kept as is, pin the one fork sentence in clause 3.4: "the probability is the share of that day's rotation bookings sold for the same window on that channel that aired at each place". Pin the age fork in notas_extracao_portal_dador.txt: "age is read at the person's first first-donation booking".

Outcome: architecture 6 spent at this round (SEND_BACK on Gate G and Gate H, and both stage 4 readers landed the call); the gate reconciliation against the design note was not run.
