"""task197: emits submission.md from figures.json, enriching it with the counts the write-up owes."""
import os, sys, json, csv, datetime as dt
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sim, core
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")

def rd(p):
    with open(os.path.join(TGT, p), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

def main():
    fp = os.path.join(HERE, "figures.json")
    F = json.load(open(fp))
    F["spans"] = {s["id"]: s["ramp_s"] for s in sim.SITES}
    F["obliged_pairs"] = sum(r["episodes"] for r in F["scorecard"])
    F["episodes_total"] = F["counts"].get("episodes_under") or F["obliged_pairs"]
    F["sites_outside_tolerance"] = sum(1 for r in F["scorecard"] if r["under"])
    F["constants"] = {"qualify_under_hz": 49.920, "qualify_over_hz": 50.080, "span_hz": 0.190,
                      "deadband_mhz": 10, "qualify_secs": 15, "tolerance_pct": 90.0,
                      "full_activation_mhz": 200}
    json.dump(F, open(fp, "w"), indent=1, sort_keys=True)
    sc = F["scorecard"]
    o = []
    w = o.append
    w("## Tags")
    w("")
    w("**Domain:** Energy systems and utilities (grid reliability and outage analysis).")
    w("**Analytical objective:** Anomaly detection and diagnostics.")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**%s (%s) comes out of the frequency containment reserve portfolio for the %s delivery month "
      "and takes the month's re-prequalification slot.** Its realised response gain is %.0f per cent of "
      "the gain its contract requires, %.0f percentage points below %s at %.0f per cent. Not %s, whose "
      "%.0f per cent on the undisturbed level before each episode is its own programme unwinding a "
      "morning discharge through the deviation. Not %s, which leads at %.0f per cent on the period "
      "setpoint because its programme traverse is still running at the second the response is read."
      % (F["call_name"], F["call_site"], F["delivery_month"], F["call_gain"], F["gap_pp"],
         F["runner_name"], F["runner_gain"], F["rung0_name"], F["rung0_pre"],
         [r["name"] for r in sc if r["site"] == F["ladder_names"]["sp"]][0],
         F["ladder"]["sp"][F["ladder_names"]["sp"]]))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. %s's realised response gain is **%.0f** per cent of contracted gain over **%d** qualifying "
      "under-frequency episodes" % (F["call_name"], F["call_gain"], F["call_episodes"]))
    w("2. The runner-up %s is **%.0f** per cent, a gap of **%.0f** percentage points"
      % (F["runner_name"], F["runner_gain"], F["gap_pp"]))
    w("3. Each site's programme traverse runs for a fixed span from the settlement period boundary, "
      "recovered from the boundaries where no qualifying episode ran: **%d** seconds at %s and **%d** "
      "seconds at %s" % (F["spans"][F["call_site"]], F["call_name"], F["spans"]["VKF-TRB"], "Terborgh"))
    w("4. **%d** sites sit below the standard's %.0f per cent tolerance"
      % (F["sites_outside_tolerance"], F["tolerance"]))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Took every qualifying under-frequency episode from the published one-second frequency in "
      "system_frequency_1s_extracts.csv, at or below 49.920 Hz for 15 or more consecutive seconds per "
      "clause 2 of the reserve performance standard.")
    w("2. Scoped each episode to the sites contracted for that settlement period in "
      "fcr_block_commitments.csv and dropped the block parts the control platform event log records as "
      "withdrawn from reserve, leaving %d obliged site-episode pairs." % F["obliged_pairs"])
    w("3. Recovered each site's programme traverse from vkf_highres_archive.sqlite at the settlement "
      "period boundaries holding no qualifying episode: the span from the boundary to the new setpoint "
      "in site_programme_15min.csv is a constant of the site's controller, %d seconds at %s."
      % (F["spans"][F["call_site"]], F["call_name"]))
    w("4. Took each site's delivered response at an episode's extreme second as its recorded power less "
      "its programme traverse at that second, over the deviation beyond the 10 mHz dead band and over "
      "its contracted gain, which is its contracted FCR capacity in asset_register.xlsx divided by "
      "0.190 Hz per clause 2 of the technical conditions.")
    w("5. Averaged the per-episode ratios with equal weight for each site: %s."
      % ", ".join("%s %.0f per cent" % (r["name"], r["gain_pct"]) for r in sc[:4]))
    w("6. Ran the same episodes against the undisturbed level before each episode, which puts %s at "
      "%.0f per cent and %s at %.0f, and against the period setpoint, which puts %s at %.0f: both "
      "bases credit each site with whatever its own programme did during the deviation."
      % (F["rung0_name"], F["rung0_pre"], F["call_name"], F["ladder"]["pre"][F["call_site"]],
         [r["name"] for r in sc if r["site"] == F["ladder_names"]["sp"]][0],
         F["ladder"]["sp"][F["ladder_names"]["sp"]]))
    w("7. Applied clause 3 of the standard: %d sites are outside the %.1f per cent tolerance and the "
      "single monthly test slot goes to the site furthest below contract."
      % (F["sites_outside_tolerance"], F["tolerance"]))
    w("8. Recommended withdrawing %s for the %s delivery month." % (F["call_name"], F["delivery_month"]))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### response_determination.md")
    w("")
    w("1. Site withdrawn for the %s delivery month: %s (%s)." % (F["delivery_month"], F["call_name"], F["call_site"]))
    w("2. Its realised response gain: %.0f per cent of contracted gain." % F["call_gain"])
    w("3. Runner-up: %s (%s) at %.0f per cent." % (F["runner_name"], F["runner_site"], F["runner_gain"]))
    w("4. Gap: %.0f percentage points." % F["gap_pp"])
    w("")
    w("### site_response_scorecard.xlsx")
    w("")
    w("1. Realised response gain, qualifying under-frequency episodes and tolerance verdict, nine sites "
      "in gain order, gains to the nearest whole per cent and counts whole:")
    for r in sc:
        w("   - %s (%s): %.0f per cent, %d episodes, under tolerance %s"
          % (r["name"], r["site"], r["gain_pct"], r["episodes"], "yes" if r["under"] else "no"))
    w("2. Realised response gain and episode count on the qualifying over-frequency episodes, nine sites "
      "in site order:")
    for d in F["down"]:
        if d["gain_pct"] is None:
            w("   - %s (%s): none, 0 episodes" % (d["name"], d["site"]))
        else:
            w("   - %s (%s): %.0f per cent, %d episodes" % (d["name"], d["site"], d["gain_pct"], d["episodes"]))
    w("3. Reserve capacity hours committed, held available and short, six delivery blocks, MWh to one "
      "decimal place:")
    for b in F["availability"]:
        w("   - Block %d (%s): committed %.1f, held available %.1f, shortfall %.1f"
          % (b["block"], b["hours"], b["committed"], b["available"], b["shortfall"]))
    w("   - Portfolio: committed %.1f, held available %.1f, shortfall %.1f"
      % (F["avail_committed_total"], F["avail_available_total"], F["avail_shortfall_total"]))
    w("4. Net metered volume for the window and the difference against the operator's settlement "
      "statements, nine sites in site order, MWh to one decimal place:")
    for r in F["reconciliation"]:
        w("   - %s (%s): metered %.1f, settled %.1f, difference %.1f"
          % (r["name"], r["site"], r["metered"], r["settled"], r["difference"]))
    w("   - Portfolio: metered %.1f, settled %.1f, difference %.1f"
      % (F["rec_metered_total"], F["rec_settled_total"], F["rec_difference_total"]))
    w("5. Bar chart of the under-frequency realised gains by site on the Scorecard sheet, one bar per "
      "site in gain order, with the tolerance line drawn across at %.0f per cent and the axis titled in "
      "per cent of contracted gain." % F["tolerance"])
    w("")
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write("\n".join(o))
    print("submission.md written, %d lines" % len(o))

if __name__ == "__main__":
    main()
