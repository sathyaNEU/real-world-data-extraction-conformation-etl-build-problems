# Determinism review, task199 (isolated judge)

File universe: fresh unzip at `/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task199_judge_pack` (17 members) plus the graded
blocks inlined in the judge brief. Nothing under the repo task folder was opened: no design note, no
generator, no pipeline.json, no earlier report, no skills or guidelines. No git command, no agent.
Every figure below was recomputed from the shipped files with pandas / pdftotext / openpyxl.

---

## Verdict

**NOT_DETERMINISTIC** on the committed set as a whole (the main recommendation and its printed rate are
forced; supplementary answer 6 is not, and supplementary answer 4 admits a second licensed reading).

**Disposition: FIX_NOW.** The repair is two clauses in `prompt.txt`: pin how a transcribed range is turned
into a participant count and at what grain it is rounded, and say that the delivered-versus-billed gap is to
be reported as the reconciling items that explain it. The register, the remission log, the invoice, the
protocol and the whole main-call surface stay byte-identical; only the grading of asks 4 and 6 has to be
redone, not the main call.

## Derivation, written before the graded blocks were read

Working the prompt and the bundle first, the answer the pack forces is **Tibu, 92.2 recorded collective
actions per 100,000 residents**, by this path:

1. Build one register across `rac_acciones_2024/2025/2026.csv`. Three layouts: 2024 one row per day of a
   prolonged action (suffixed ids `-1`, `-2`), 2025 renamed columns and day-first dates, 2026 one row per
   action with `dias` plus a `preliminar`/`definitivo` flag. `protocolo` 3.1/3.2 makes the definitive extract
   replace the preliminary one; all 320 `preliminar` rows are exact field-for-field twins of a `definitivo`
   row, so deduplication is clean. `manual_codificacion` 1.2 and 2.1 fix the unit: one concentration, one day,
   one place, a day repeated is a second action. So 2026 rows expand to one action-day per date.
2. Count action-days by date of occurrence (`protocolo` 4.2) for 1 Apr to 30 Sep 2026 inclusive and for the
   24 months ended 31 Dec 2025.
3. `protocolo` 4.1 is operative, not decorative: the designation refers to a rise in protest activity, and
   "los registros del Observatorio son la evidencia de esa actividad y no su medida". The register's volume is
   a function of what the monitored media remitted, so the comparison has to hold monitoring exposure level.
   The only topic-independent exposure volume in the pack is `items_entregados` in
   `envios_resena_andina.csv` ("cuenta cuanto remitio el servicio desde ese municipio, sea cual sea el tema").
   `items_retenidos` ("los que pueden describir una accion") and `citas_rac.csv` are endogenous to the
   activity being measured; citations per action are circular by construction (one item cites one entry).
4. Ratio of action-days per delivered item, semester against comparison period: Tibu 2.435, next eligible
   city San Calixto 1.342. Sardinata 0.453, El Tarra 0.477, Convencion 0.438: their register rise is
   monitoring, not activity (from April 2026 their delivered items roughly triple and three new source
   desks start reporting, while Tibu's fall).
5. `protocolo` 4.3: at least 70 actions in the semester. Only Hacari (56) fails, and it leads nothing.
6. `protocolo` 4.5: publish the designated city's registered-action rate per 100,000 on the population
   projection in force for 2026. 137 / 148,590 x 100,000 = 92.1999 -> **92.2**.

### Options enumerated where the shipped text is silent or could be read twice

Denominator, every population figure and vintage in the pack (Tibu):

| population figure | source | rate it gives |
|---|---|---|
| 148,590 | `proyecciones_poblacion.xlsx`, "Proyeccion 2026 unidades" | **92.2** (forced by 4.5, "vigente para 2026") |
| 148.59 thousand | same workbook, "Proyeccion 2026 miles" | 92.2 (identical quantity; 0.1 if misread as thousands) |
| 147,341 | "Serie 2018-2024", pre-census series, 2024 value | 93.0 (excluded: pre-census and no 2026 value) |

Unit the numerator counts (Tibu, semester):

| reading | n | rate |
|---|---|---|
| action-days, 2026 expanded by `dias` onto its own dates (forced: manual 1.2/2.1, diccionario) | **137** | **92.2** |
| register entries, a 2026 row counted once | 108 | 72.7 |
| rows as shipped, `preliminar` not dropped | 122 | 82.1 |
| rows as shipped x `dias` | 153 | 103.0 |
| all `dias` attributed to the action's start date | 138 | 92.9 |
| by `fecha_registro` instead of occurrence | 128 | 86.1 |

Window:

| reading | n | rate |
|---|---|---|
| 1 Apr to 30 Sep 2026, both days included (4.2) | **137** | **92.2** |
| whole months April through September (same span) | 137 | 92.2 |
| 30 Sep excluded | 135 | 90.9 |
| preliminary vintage instead of definitive | 137 | 92.2 (contents identical) |
| comparison period: 24 months / 4 | 226 / 4 | designation unchanged |
| comparison period: mean of the two Apr-Sep halves (seasonal) | 113 | Tibu 2.452, still first |
| exposure window on `periodo_publicacion` instead of `fecha_envio` | - | Tibu 2.440, still first |

The one live fork on the unit is "all days at the start date" (138, 92.9). It is closed by manual 1.2: the
second day of the 30 Sep 2026 Tibu action is its own action, dated 1 October, outside the semester. The
designation does not move under it (2.453), only the printed rate and the chart's 2.44.

Normalising one measured volume by another: the shipped text does **not** name the denominator volume.
`protocolo` 4.1 forces that the register not be used as the measure, and the data dictionary's own wording
separates the topic-independent volume from the filter's retained items, which is what closes the choice.
What each candidate denominator computes to (eligible cities, semester vs comparison):

| denominator | winner | value | runner-up |
|---|---|---|---|
| none, raw counts vs 24 months / 4 | Sardinata | 3.175 | Convencion 2.779 |
| `items_entregados` (exposure, topic-independent) | **Tibu** | **2.435** | San Calixto 1.342 |
| `items_retenidos` (filter output, endogenous) | Tibu | 1.658 | Teorama 1.455 |
| citations per action (`citas_rac.csv`, circular) | Teorama | 1.748 | Ocana 1.125 |

Both defensible exposure measures pick Tibu; only the raw path (Sardinata) and the circular path (Teorama)
diverge, and each is excluded by shipped text. The margin, 2.44 against 1.34, is wide and falls out of the
data the same way for every solver, so this is a thin-free, definitive gap.

## Gate table

| Gate | Result |
|---|---|
| A, solution correct on the shipped files | **Fail in part.** The main call, all four critical components, the whole eleven-city table, and asks 2, 3, 4 and 5 reproduce exactly. Ask 6 reproduces only under an unlicensed convention (below). One solution-block wording defect: step 5 says the retained-items and citations denominators "rank Teorama first", but retained items rank Tibu first (1.658) and only citations rank Teorama first (1.748). |
| B, every decisive fact in the shipped files | **Pass.** Panel (`protocolo` 2.1), window and comparison (4.2), 70-action floor and panel-tenure limb (4.3, all eleven have 24 months of register and remission coverage), published rate basis (4.5), the evidence-not-measure clause (4.1), unit (manual 1.2, 2.1), extract precedence (3.1, 3.2), population (`proyecciones_poblacion.xlsx`), exposure semantics (`diccionario_datos.md`, `envios_resena_andina.csv`). Action vocabulary ("mision de verificacion", "designacion", "nota de vigilancia") is the protocol's own. |
| C, uniquely forced | **Fail on supplementary answers.** Main designation and rate forced. Ask 6 is not (see below); ask 4's "a line for each difference" also carries the per-quarter arithmetic deltas -56, +68, -49, +126 instead of the three reconciling items 82, 125 and 7. |
| D, difficulty analytical, not semantic | **Pass on the main call.** The split between Tibu and Sardinata is an exposure confound, not a word. |
| E, prompt unambiguous on the decision | **Fail in part.** Main ask pinned to one city and one rate. Ask 4 is bundled and under-specified; ask 6 leaves the participant reconstruction and its rounding grain open, and the prompt's own "participants and every rate to one decimal" contradicts the whole-participant totals the block prints. The chart ask is internally inconsistent: bars "of gathering-days per 1,000 items received, the half year against the comparison period" with "a line at 1.00 for no change" (the 1.00 line belongs to the ratio, not to a per-1,000 level, which for Tibu is 42.5 against 17.5). |
| F, stump power | Moderate to good. See below. |
| G, stumping type | Pass. See the Gate G line. |
| H, the three rules | Pass. See the Gate H line. |
| Hygiene and integrity | **Pass.** 17 files, 4 formats (9 csv, 4 pdf, 2 xlsx, 1 md), largest file 51,173 rows. Every row count in `manifiesto_exportacion.csv` matches the file it names. No README or how-generated artifact, no "synthetic/generated/benchmark" string, no tool banner, no solver-facing language; grep for those terms returns nothing. Temporally coherent: protocol v4 of 12 Feb 2026, manual ed. 7 of Jan 2026, dictionary ed. 9 and manifest extract date 5 Nov 2026, register through 30 Sep 2026, remissions through 30 Sep 2026, invoice issued 19 Jan 2026. Artifacts read as operational (day-first dates in one export, renamed columns, mesa-sede roll-up, a credit note in the invoice's footer, an invoice whose tables live inside the PDF). No public-data contamination: the fiction is a Colombian corridor register with no canonical published analysis. Nothing exclusion-level. |

## Figures I could not reproduce, with what I got instead

**Supplementary answer 6, participants by actor sector (2025, the twelve municipalities outside the panel).**
In all 182 ranged rows `participantes_est` equals the **low end** of the range transcribed in
`nota_registro`, not the central estimate `manual_codificacion` 2.2 promises, so the central estimate has to
be rebuilt from the note. Taking the midpoint, excluding the zero/blank rows the dictionary declares
unreported, and counting by action date across the register (which pulls in the 1 Jan 2025 Curumani
Transportadores row that sits in the 2024 export, note "165 a 267", midpoint 216), the committed figures
reproduce **only if every row's midpoint is floored to a whole participant first**. Nothing in the pack
licenses that. Carrying the half and rounding at the end moves seven of eight totals and four of eight means:

| sector | committed | floor each midpoint (mine) | carry the half (mine) |
|---|---|---|---|
| Campesinado | 275.6 / 34,444 | 275.6 / 34,444 | 275.6 / 34,450 |
| Comerciantes | 378.3 / 8,702 | 378.3 / 8,702 | 378.4 / 8,704 |
| Docentes | 302.9 / 29,379 | 302.9 / 29,379 | 302.9 / 29,383 |
| Juntas comunales | 289.5 / 16,501 | 289.5 / 16,501 | 289.6 / 16,508 |
| Juventudes | 162.5 / 4,388 | 162.5 / 4,388 | 162.5 / 4,388 (4,388.5) |
| Mineria artesanal | 330.9 / 66,170 | 330.9 / 66,170 | 330.9 / 66,184 |
| Mujeres organizadas | 355.9 / 5,695 | 355.9 / 5,695 | 356.0 / 5,696 |
| Transportadores | 275.1 / 61,902 | 275.1 / 61,902 | 275.2 / 61,912 |

Using `participantes_est` as shipped (no reconstruction at all) gives a third set: Campesinado 256.8 /
32,105, Transportadores 266.9 / 59,787, and so on. Three sets of graded numbers, no shipped sentence
choosing between them.

**Everything else reproduced.** Semester and comparison action-days for all eleven panel cities (137/226,
80/216, 169/564, 100/358, 81/292, 56/215, 334/1326, 86/383, 175/252, 177/223, 107/154); all eleven rates;
Hacari alone failing 4.3; Tibu items 3,220 and 12,935, Sardinata 22,211 and 12,670; population 148,590;
the 2025 non-panel delivered grid by quarter and outlet type (T1 3,090/1,555/995/1,711/7,351 through T4
3,162/1,472/918/1,808/7,360, mapping `RSA-` codes back to the 2025 numbering via `panel_fuentes.xlsx`); the
invoice's 7,407/7,531/7,598/7,234 items and 16,545.0/16,812.7/16,980.5/16,174.0 thousands, summed from the
72 PDF rows; the three reconciling items (82 items published Dec 2024 delivered Jan 2025; 125 published Dec
2025 delivered Jan 2026; the 11 Aug 2025 lote of the Rio de Oro desk, 5 items for Rio de Oro plus 2 for
Gonzalez, which the desk also serves, = 7, and publication-basis T3 7,605 less 7 = the billed 7,598); and
all twelve register lines with months holding none (Abrego 146/0 through San Martin 89/0).

Checked and found sound, not a defect: `boletin_2026T1.pdf` disagrees with the definitive extract in two
cells (Convencion 2025 T3 16 against 17, 2026 T1 Planton 106 against 103). The bulletin states on its face
that its figures are revised when later accounts arrive, it covers no part of the evaluated semester, and it
declines to compare municipalities or anticipate the designation, so no shipped artifact ranks the
candidates on the decision question. `resumen_mensual_rac_2025.csv` is a genuine wrong-grain decoy for ask 5
(Abrego 173 against 146, Curumani 251 against 120, and zero for six municipalities whose mesa reports under
another sede) and the dictionary documents why it cannot be used.

## Distance from the printed bin edge, every graded figure

Rounding unit 0.1 unless stated; 0.3 of the unit is 0.03, and anything inside that is flagged.

| figure | exact | printed | distance to edge |
|---|---|---|---|
| rates per 100,000, all eleven cities | 92.1999, 76.4017, 84.3998, 102.7004, 49.7000, 63.4999, 66.0996, 75.9050, 98.5003, 121.3999, 88.9000 | 92.2 ... 88.9 | 0.047 to 0.050 each, none flagged |
| Tibu designation ratio (chart title) | 2.43513 | 2.44 | **0.00013** (unit 0.01, threshold 0.003) **FLAG** |
| Ocana ratio | 1.15466 | 1.15 | **0.00034 FLAG** |
| Teorama ratio (step 5) | 1.14359 | 1.14 | **0.00141 FLAG** |
| El Tarra / Sardinata / Convencion ratios | 0.47712 / 0.45277 / 0.43798 | 0.48 / 0.45 / 0.44 | **0.00212 / 0.00223 / 0.00298 FLAG** |
| San Calixto ratio (quoted as 1.34) | 1.34165 | 1.34 | 0.00335 |
| participants per action, Mineria artesanal | 330.85000 | 330.9 | **0.0000 FLAG**, exactly on the tie; half-up gives 330.9, half-even gives 330.8 |
| participants per action, Campesinado | 275.55200 | 275.6 | **0.0020 FLAG** |
| participants per action, Comerciantes | 378.34783 | 378.3 | **0.0022 FLAG** |
| participants per action, Mujeres organizadas | 355.93750 | 355.9 | **0.0125 FLAG** |
| participants per action, Docentes | 302.87629 | 302.9 | **0.0263 FLAG** |
| participants per action, Transportadores | 275.12000 | 275.1 | 0.0300, on the threshold |
| participants per action, Juventudes | 162.51852 | 162.5 | 0.0315 |
| participants per action, Juntas comunales | 289.49123 | 289.5 | 0.0412 |
| invoice items and thousands, delivered grid, register lines, action-day counts | integers / exact tenths from the PDF | as printed | not at risk |

The ratio figures are only quoted, not graded as the call; the designation they produce is nowhere near a
boundary. The flagged participant means are graded, and three of them (330.85, 275.552, 378.348) sit so
close to the tie that the row-level rounding convention alone decides what prints.

## Stump power (Gate F)

The trap that does the work: `protocolo` 4.2 reads as an instruction to compare the semester with the
register's own 24-month base, and executing it literally files **Sardinata** at 3.18 with a printed rate of
**121.4**, with El Tarra (2.78) and Convencion (2.78) behind it, because from 1 April 2026 the press service
roughly triples what it remits from those three municipalities and three new desks start reporting. A strong
model that counts correctly, cleans all three templates correctly and reads every field correctly still files
the wrong city unless it treats the register as evidence of activity rather than its measure and divides by
the monitoring volume. That is a genuine analytical failure mode and it should defeat a good share of strong
runs. Against it: `protocolo` 4.1 and the bulletin's own methodological note ("un registro construido a
partir de prensa depende de lo que las fuentes remitan y ... su cobertura no es uniforme entre municipios")
state the principle fairly loudly, so a careful reader is steered in. They do not hand out the correction
(neither names a normaliser, neither distinguishes delivered from retained items, neither names a city), so I
would call stump power moderate to good rather than high. If it needs hardening without touching
determinism, thin the bulletin's note to one neutral sentence; do not touch 4.1, which is what closes the
fork.

## Gate G line

`mechanism: decomposition_attribution`, `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`.

Every reported figure in the pack is fine: the register's action-days are correct, the bulletin's published
counts are correct for the vintage it declares, the delivered and billed item volumes are correct, and there
is no stakeholder conclusion or published ranking the solver must catch as wrong (the bulletin expressly
declines to compare municipalities or anticipate the designation). The difficulty is attributing a
correctly-reported movement to the right driver, register entries rising because monitored press volume rose
rather than because protest activity rose, and choosing the estimand that holds exposure level, which is the
description-bias correction that media-based protest event analysis is built on. Borderline note, recorded
honestly: one could argue for `single_conceptual_flip`, since a single lens change moves the winner. It
fails the litmus, because there is no misleading reported read in the pack to flip away from; the naive
ranking is one the solver constructs, and the governing protocol clause tells it not to.

## Gate H line

`domain: pass`, `layers: pass`, `decisive_step: analytical`.

The quantity that decides the call is a coverage-adjusted collective-action rate, the thing a protest-event
observatory actually estimates, and the swap test holds (replace actions with hospital visits and the
media-exposure denominator stops making sense, because the mechanism is the register's dependence on what
monitored sources remit). Layer 1: three register layouts across 2024, 2025 and 2026 (one row per day
against `dias`, renamed columns, day-first dates), a preliminary and a definitive extract overlapping, three
DIVIPOLA codes reissued in July 2025, the press service renumbering its desks to an `RSA-` prefix in 2026,
remission date against publication month, invoice tables inside a PDF, and a monthly summary rolled up by
desk sede rather than municipality. Layer 2: holding monitoring exposure level before comparing register
volumes across periods. The easy route a strong analyst who cleaned everything and read every field and rule
correctly would still take is executing clause 4.2's comparison on raw counts, which files Sardinata and
prints 121.4 instead of Tibu and 92.2.

## Fix

**prompt.** Two clauses, nothing else:

1. In the participants ask, pin the reconstruction and its grain: "where the note transcribes a range, take
   its midpoint as the central estimate, rounded to the nearest whole participant before any total, and
   ignore rows the source did not report". That makes one of the three candidate sets the literal answer.
   While there, reconcile the ask's rounding with the prompt's closing sentence, which currently says
   participants to one decimal while the committed totals are whole.
2. In the delivered-against-billed ask, replace "with a line for each difference" with "with a line for each
   item that reconciles the gap between them", so the three reconciling items are the forced reading rather
   than the four per-quarter arithmetic deltas.

Also worth correcting, outside the determinism finding: the chart ask should say the bars carry each city's
ratio of action-days per delivered item (semester against comparison period), since a 1.00 no-change line
does not belong on a per-1,000-item level; and step 5 of the solution should say that citations per action
rank Teorama first while retained items still rank Tibu first.
