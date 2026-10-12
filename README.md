# Project Mark task builds

Each `taskNN/` folder is one deterministic analytical task built for Project Mark: a prompt, an evidence bundle,
the golden deliverables and the submission write-up. The aim is simple: unique, high-quality tasks that hold
on the portal, shipped one after another. `CLAUDE.md` is the working contract and every session loads it.

## Start a session

```
/build next                       # the next open number in your lane, built end to end
/build task136                    # a number you were handed
/build resume task134             # a paused build, from its pipeline.json
/fix-determinism task181 <finding>  # the portal's determinism block failed, the rubric was fine
/fix-rubric task445 <portal rows>   # the call held, the top two averaged 50 or more
python3 .claude/skills/build-pipeline/status.py          # the board, read from every pipeline.json
```

`/build`, `/fix-determinism` and `/fix-rubric` run at max effort; `/approve`, `/leak-check`, `/clone-check` and
every spawned agent run at medium. There is no in-house solver round: the portal is the stump oracle.

## Lanes

Task numbers are fixed by objective in `START_HERE.md`. Each developer owns one lane, set in
`.claude/authors/<handle>.md`, and keeps two builds in flight.

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
