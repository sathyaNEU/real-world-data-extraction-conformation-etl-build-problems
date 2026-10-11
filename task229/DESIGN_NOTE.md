# task229 design note

Seed DQ02 (whether the release-health alert fires on this week's build, when the metric is the
average user's rate). The seed's pairing was product-analytics; task228 is being built the same day
in the same objective inside the product-analytics experiment-platform world, so this build keeps the
seed's Layer 2 pitfall and objective and moves the world to a smart-meter metering data provider,
where the object under analysis (interval data delivery) is the health of the data itself.

## DRAW

| Axis | Value |
|---|---|
| Domain / subdomain | Energy Systems & Utilities / other (smart-meter interval data delivery quality, the metering data provider's read performance; the client list carries no energy task type that serves Data Quality Monitoring) |
| Objective | Data Quality Monitoring & Alerting |
| Niche | a smart-meter data provider's read-health gate on the communications-module firmware builds live in its fleet, deciding which builds the read-health alert fires on before the next rollout wave |
| Shape | 10 scorecard against thresholds: eight builds, each with its assessed installations, read health, lower limit and fire or hold, plus the wave's exposure and the week's upgrade-night cost |
| Decision type / unit | designation_set (which builds the alert fires on) / set_of_items |
| Gap / pattern / generators | population (decisive: the unit the standard scores is the installation that ran the build all week, the file grain is the register-day delivery), time (the delivery cut-off as of which a read counts); pattern D (two grains, both flawless); G2 grain mismatch, G7 operating window, G17 statistical rigor |
| Gate G mechanism | signal_vs_noise_or_hold (which builds sit below the reference by more than their own noise; five of eight hold) |
| Stump strategy | grain_or_unit; decisive rule filed (the read-health standard defines the measure and its limit); no official decoy; no validated decoy; no calibration organ |
| Layer 2 | estimation_fit, `product-analytics/metric-definition-measurement-science/2` (ratio of sums is not mean of ratios; the limit follows the unit), made this build's own: the heavy unit is a 5-minute, three-register installation that files eighteen times a 30-minute single-register household's reads, and the build's error has to come from installation-to-installation spread |
| Layer 1 | interval reads with quality codes at mixed 5, 15 and 30 minute resolution; register-days re-delivered when a later retrieval completes them; receipts in UTC, market time in AEST, field times in AEDT, against a filed cut-off; firmware build codes spelled three ways across the head-end, the rollout schedule and the MDM; effective-dated meter-to-installation assignments with mid-week exchanges; head-end events replayed after a failover and failed activations rolled back |
| Calibration form | none, because the strategy is a stated rule whose construction is the work; no closed corpus is needed or shipped |
| Context artifact | monitoring_export (the MDM interval receipt extract) |
| Stakeholder | metering data services lead, who owns the read-health alert the rollout desk gates each wave on |
| Forum / forcing event / org family | operations_desk (the rollout desk holds the wave for any build the alert fires on) / cutover_or_migration (Wave 8 of the firmware migration goes out on Tuesday night) / utility_or_infrastructure |
| World | Wattle Grid Metering, an accredited metering provider and metering data provider in the National Electricity Market, New South Wales, AUD; personas drawn with `guard.py names --locale en_AU --seed 229` |
| Deliverables | `wave8_read_health_alerts.json` (the alert payload the routing system ingests: commits), `read_health_by_build_wk41.png` (reads at a glance) |
| Guard | PASS (WARN repeat.deliverables cleared by moving to json plus png, a set the batch has not used); NOTE same_puzzle_older against task98 v3, differentiated on the card; nearest driver 0.06 (task87 v3) |

**Coordination with task228.** Drawn the same day in the same objective. task228 holds the
product-analytics experiment-platform guardrail world; this build differs in domain (energy
utilities), organisation (a metering data provider), forum (the rollout desk), forcing event (a
firmware migration wave), geography (New South Wales), personas (en_AU draw), data structure
(register-day deliveries of interval counts by quality flag, with an activation history) and
stump strategy (grain_or_unit with a limit that follows the unit).

**Data-native sentence.** A metering data provider's fleet mixes 30-minute single-register
household meters with 5-minute three-register installations (solar export and controlled load, or
small commercial sites) that file up to eighteen times as many interval reads a day, and its
communications firmware fails in ways that hit one profile and not the other; so on this fleet the
pooled share of interval reads and the average installation's share are different measures of the
same week, and the record-count error a pooled share invites is a fraction of the installation-level
noise, which is exactly the shortcut a capable analyst takes on interval data.

**Why every element is real.** NEM metering data providers deliver interval data with quality flags
(actual, substituted, estimated) by register (data stream suffix) and day, re-deliver a day when a
later retrieval recovers the reads, work in market time (AEST, no daylight saving) while field crews
and the head-end log local or UTC time, and roll communications firmware out in waves with a
go/no-go per build.

## Stump sentence

A competent solver builds each firmware build's read health from the MDM receipts as the share of
all expected interval reads that were actual, with the binomial error on those reads, and fires the
alert on EM3.12.0, EM3.12.2, PX5.3.0, PX5.3.1 and EM3.10.9 while holding PX5.2.7 and EM3.12.1; the
step that lands it there is pooling interval reads, which the 5-minute three-register installations
dominate, with a read-count error, instead of averaging the installations that ran the build all week
on the reads held at the delivery cut-off with the error taken from installation-to-installation
spread; done that way the alert fires on PX5.2.7, EM3.12.1 and EM3.10.9 and holds the other five.

(The build list is the design target; the generator asserts it and this sentence is restated from
the generator's output once the pack is cut.)

## Tried and rejected

- Keeping the seed's product-analytics crash-rate world: a per-user crash rate is a product health
  metric, not the health of data or of a pipeline, so the build would retag as Anomaly Detection
  without changing a word; and task228 holds product-analytics in this objective on the same day,
  so the pairing would block on `ban.pairing` at the heart check.
