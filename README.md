# Project Mark task builds

Each `taskNN/` folder is one deterministic analytical task built for Project Mark: a prompt, an evidence bundle,
the golden deliverables and the submission write-up. The aim is simple: unique, high-quality tasks that hold
on the portal, shipped one after another. `CLAUDE.md` is the working contract and every session loads it.

## Start a session

```
/build next                       # the next task in your backlog wave, built end to end
/build task136                    # a number you were handed
/build resume task134             # a paused build, from its pipeline.json
/fix-determinism task181 <finding>  # the portal's determinism block failed, the rubric was fine
/fix-rubric task445 <portal rows>   # the call held, the top two averaged 50 or more
python3 .claude/skills/build-pipeline/status.py          # every developer's waves, each task's status
```

`/build`, `/fix-determinism` and `/fix-rubric` run at max effort; `/approve`, `/leak-check`, `/clone-check` and
every spawned agent run at medium. There is no in-house solver round: the portal is the stump oracle.

## Lanes

Task numbers are fixed by objective in `START_HERE.md`. Each developer owns one lane and keeps two builds in
flight. Their `.claude/authors/<handle>.md` holds the status board link and the backlog: waves of six tasks to
ship, reworks of builds that failed to stump first.

| Lane | Tasks | Owner |
|---|---|---|
| Forecasting & Predictive Modeling | task132 to task179 | sathya8571 |
| Anomaly Detection & Diagnostics | task180 to task227 | oviya13ya |
| Data Quality Monitoring & Alerting | task228 to task252 | perssathya |
| Descriptive & Distribution Analysis | task253 to task300 | sathay3012 |
| Opportunity Sizing & Decision Support | task301 to task396 | unassigned |
| Root-Cause Analysis | task397 to task444 | unassigned |
| Data Extraction & Conformation (ETL) | task445 to task493 | oviya1301 |

## Git

One branch, `main`. Commit only at a status change (`DRAWN`, `SHIPPED`, `RESHIPPED`, `PAUSED`, `RETIRED`),
staging your own task folder, card and ledger row by name, then `git pull --rebase origin main` and push. Packs
and goldens are rebuilt by each generator; a shipped build tracks only `target.zip` and `golden/`. Raw downloads
and source caches never go in git.

## Layout

| Path | What it holds |
|---|---|
| `CLAUDE.md` | the contract: routing, commands, workflow, git, the current spec |
| `.claude/skills/` | the working standard, one skill per stage, scripts beside the skill that owns them |
| `.claude/commands/`, `.claude/agents/` | the six commands and the two isolated agents |
| `.claude/authors/` | one short file per developer: lane, email, status page |
| `START_HERE.md` | task numbers by lane, each linked to its seed |
| `analytical_tasks/` | the seed library (ideas, never designs) and its index |
| `guidelines/` | the client's spec and source libraries, behind the skills |
| `handoffs/` | where each paused build stopped |
| `taskNN/` | the builds from task110 on (the earlier corpus lives on as fingerprint cards and in the clone baseline) |

<!-- task-ids-by-domain:start -->
## Task ids by domain

Every build with a fingerprint card, grouped by its client domain (the build's `pipeline.json` where it has one, else its card); 304 tasks in 30 domains, as of 2026-10-28.

- **Accounting, Audit & Forensic Analytics:** task110, task184
- **Actuarial Science & Insurance:** task130, task139, task255, task309
- **Banking, Credit & Financial Risk:** task128, task133, task177, task196, task446
- **Biology, Biostatistics, Epidemiology & Bioinformatics:** task33
- **Biomedical & Clinical Research:** task122, task195, task260, task265, task267, task268
- **Business & Operations Analytics:** task109, task111, task114
- **Criminology & Justice:** task141, task169, task179
- **Data Quality Monitoring & Alerting:** task104
- **Demographic & Social Science:** task34, task66, task76, task79, task86, task97, task105, task272, task475
- **Economics:** task17, task27, task28, task29, task30, task35, task38, task40, task51, task59, task63, task68, task81, task88, task91, task93, task95, task500
- **Economics & Econometrics:** task118, task145, task154, task155, task163, task302
- **Education & Learning Sciences:** task253, task450, task464
- **Energy Systems & Utilities:** task120, task124, task129, task131, task132, task136, task152, task162, task164, task173, task183, task187, task197, task201, task303, task306, task308, task310
- **Epidemiology & Public Health:** task149, task188, task232, task234, task236, task242, task248, task301, task304, task501
- **General Statistics & Data Science:** task143, task147, task151, task153, task158, task172, task182, task185, task191, task202, task233, task246, task251, task280, task281, task449, task454, task456, task461, task465, task466, task469, task473
- **Healthcare Delivery & Health Economics:** task127, task137, task142, task160, task194, task198, task269, task447, task451, task458, task468, task479, task482
- **Human Factors & Ergonomics:** task121, task170, task181, task256
- **Marketing & Consumer Research:** task115
- **Nonprofit & Grant-making:** task41, task42, task43, task49, task57, task75, task89, task101, task103, task107, task167
- **Pharmacology, Pharmacoepidemiology & Safety:** task171, task193
- **Physical & Environmental Sciences:** task138, task180, task189, task204, task229, task241, task245, task247, task250, task252, task263, task279, task452, task459, task460, task462, task470, task474, task476, task478, task480, task484, task487
- **Policy & Education:** task25, task37, task60, task65, task72, task73, task77, task80, task87, task98, task100, task102, task119, task126
- **Political Science & Public Policy:** task157, task192, task199
- **Product Analytics:** task1, task2, task3, task4, task5, task6, task7, task8, task9, task10, task11, task12, task13, task14, task15, task19, task22, task23, task24, task26, task48, task52, task53, task56, task62, task64, task69, task74, task82, task83, task84, task85, task116, task144, task156, task166, task228, task235, task258, task305
- **Psychology & Behavioral Science:** task237, task239, task249, task257, task270
- **Quantitative Finance:** task135, task178, task271, task445
- **Sociology & Demography:** task150, task176, task262, task266
- **Supply Chain & Logistics:** task16, task18, task20, task21, task31, task32, task36, task39, task44, task45, task46, task47, task50, task54, task55, task58, task67, task70, task71, task78, task90, task92, task94, task99, task106, task108, task117, task140, task161, task168, task472
- **Survey Research & Official Statistics:** task123, task125, task146, task186, task190, task230, task231, task238, task240, task243, task244, task259, task261, task264, task274, task275, task311, task448, task453, task455, task457, task463, task467, task471, task477, task481, task483, task485, task486
- **Urban & Regional Science:** task134, task148, task159, task165, task175, task254, task273, task307
<!-- task-ids-by-domain:end -->
