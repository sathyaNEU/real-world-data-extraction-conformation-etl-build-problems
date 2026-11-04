"""submission.md, emitted from figures.json so that no figure is typed."""
import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def day(s):
    d = dt.date.fromisoformat(s)
    return "%d %s" % (d.day, d.strftime("%B"))


def n(x):
    return "{:,}".format(x)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    c, r = F["call_group"], F["ru_group"]
    st = F["stretch"]
    zone_to = st["to"][0]
    zone_pole = st["to_poles"][0]
    meds = " and ".join(day(d) for d in F["meds"])
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Energy Systems & Utilities, grid reliability and outage analysis (finding the component "
             "breaking down on a distribution feeder from its protective devices' fault records).  ")
    L.append("**Analytical objective:** Anomaly Detection & Diagnostics.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Send the overhead line patrol crew to %s for the week of 9 November 2026, walking the main line from "
             "the Millrace feeder breaker %s to recloser %s at pole %s and the taps fused off it.** Its breaker has "
             "recorded %d momentary faults on phase %s at %s to %s A on separate mornings since %s, one place on the "
             "line failing again and again, against %d at one current behind the second choice %s's recloser %s. Not "
             "NYD-3, whose rise in non-storm momentary events per overhead mile is squirrels scattered along the "
             "feeder; not NYD-2, whose damp-morning blinks are wet limbs on overgrown taps; not BLV-3, whose phase B "
             "concentration is the phase of its taps."
             % (F["call"], c["device"], zone_to, zone_pole, c["n"], c["phase"], n(c["lo"]), n(c["hi"]), day(c["first"]),
                r["n"], F["runner_up"], r["device"]))
    L.append("\n## 2. Critical Components\n")
    L.append("1. %s's breaker %s recorded **%d** momentary faults on phase %s at **%s to %s A**, each a single trip "
             "cleared on the first reclose, on separate mornings from %s to %s 2026."
             % (F["call"], c["device"], c["n"], c["phase"], n(c["lo"]), n(c["hi"]), day(c["first"]), day(c["last"])))
    L.append("2. %s's recloser %s recorded **%d** on phase %s at **%s to %s A** from %s; no other feeder carries more "
             "than **%d** at one phase and one current since 1 August."
             % (F["runner_up"], r["device"], r["n"], r["phase"], n(r["lo"]), n(r["hi"]), day(r["first"]), F["others_max"]))
    L.append("3. The faults sit in the breaker's zone, so a failure there locks out the feeder and its **%s** customers, "
             "against **%s** behind %s." % (n(c["behind"]), n(r["behind"]), r["device"]))
    L.append("\n## 3. Step-by-Step Solution\n")
    L.append("1. Read every momentary interruption event from soe_breakers_reclosers_2025_2026.csv (feeder breakers) and "
             "recloser_control_events_2025_2026.csv (operations within five minutes of the first, DRP-04 2.5), and "
             "took each one's first trip from feeder_relay_events_2025_2026.csv or the control's TRIP row (terminals "
             "to phases through protective_device_register.csv): its faulted phase and recorded current.")
    L.append("2. Grouped each device's momentary faults since 1 August 2026 by faulted phase and current within 2 per "
             "cent, counted on separate days: %s's breaker %d on phase %s at %s to %s A, %s's recloser %d, no other "
             "feeder above %d." % (F["call"], c["n"], c["phase"], n(c["lo"]), n(c["hi"]), F["runner_up"], r["n"],
                                   F["others_max"]))
    L.append("3. Took the stretch as the recording device's zone (DRP-04 5.4) from protective_device_register.csv: "
             "%s to recloser %s at %s, %s customers behind the breaker against %s behind %s."
             % (c["device"], zone_to, zone_pole, n(c["behind"]), n(r["behind"]), r["device"]))
    L.append("4. Found the 2026 major event days under DRP-04 4 (daily system SAIDI over %s minutes on %s customers): "
             "%s." % (F["tmed"], n(F["nsys"]), meds))
    L.append("5. Built every sustained interruption from oms_outage_history_2025_2026.xlsx (legacy child tickets timed "
             "from their parent's Out, incidents with their restoration steps) and the openings over five minutes "
             "that soe_breakers_reclosers_2025_2026.csv holds with no ticket, each reaching the service points below "
             "its device on the day through the register's dated rows and service_points_2026-10-31.csv; customers "
             "already without supply are not interrupted again, and a service ticket opened at the minute the device "
             "above closed is the same interruption carrying on: SAIDI by feeder.")
    L.append("6. Counted each customer's momentary interruption events under DRP-04 2.5: a device event reaches the "
             "customers below it, less those already out and those whose fuse or transformer fuse blew in the event's "
             "minute, and a customer's events within five minutes of the first are one: MAIFI-E by feeder.")
    L.append("7. Counted the service points each feeder supplies on 31 October with more than two of those sustained "
             "interruptions: CEMI-2 by feeder.")
    L.append("8. Sent the crew to %s's breaker zone for the week of 9 November, %s next." % (F["call"], F["runner_up"]))
    L.append("\n## 4. Deliverable Answers\n")
    L.append("### line_patrol_2026-11-09.xlsx\n")
    L.append("1. Patrol feeder: %s; stretch to walk: the main line from the feeder breaker %s to recloser %s at pole "
             "%s, with the taps fused off it." % (F["call"], c["device"], zone_to, zone_pole))
    L.append("2. Second choice: %s (recloser %s, %d momentary faults on phase %s at %s to %s A since %s)."
             % (F["runner_up"], r["device"], r["n"], r["phase"], n(r["lo"]), n(r["hi"]), day(r["first"])))
    L.append("3. What keeps it second: %d repeat faults against %d, %s's beginning %s against %s, and a failure on %s "
             "locks out the feeder breaker and %s customers against %s's %s."
             % (c["n"], r["n"], F["call"], day(c["first"]), day(r["first"]), F["call"], n(c["behind"]), r["device"],
                n(r["behind"])))
    fs = sorted(F["feeders"])
    L.append("4. Minutes of interruption per customer served, January to October 2026, major event days (%s) left "
             "out, one decimal:" % meds)
    for f in fs:
        L.append("   - %s: %.1f" % (f, F["feeders"][f]["saidi"]))
    L.append("5. Momentary interruption events per customer served, same window, two decimals:")
    for f in fs:
        L.append("   - %s: %.2f" % (f, F["feeders"][f]["maifi"]))
    L.append("6. Customers with more than two sustained interruptions, same window:")
    for f in fs:
        L.append("   - %s: %s" % (f, n(F["feeders"][f]["cemi"])))
    L.append("\n### reliability_2026.svg\n")
    L.append("7. Scatter of each feeder's minutes of interruption per customer served against its momentary "
             "interruption events per customer served, %s labelled as the feeder the crew walks." % F["call"])
    text = "\n".join(L) + "\n"
    assert "\u2014" not in text and "\u2013" not in text
    open(os.path.join(TASK, "submission.md"), "w").write(text)
    print("submission.md: %d characters" % len(text))


if __name__ == "__main__":
    main()
