"""task273 architecture 5: submission.md, every figure taken from generator/figures.json."""
import os

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def _and(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def call_sentence(F):
    return ("Designate %s of Tallowbark Networks' sixteen zone substations for spring 2027: %s."
            % ({7: "seven"}.get(F["call"]["count"], str(F["call"]["count"])), _and(F["call"]["designated_names"])))


def write(F):
    ps = F["per_substation"]
    by_name = sorted(ps, key=lambda c: ps[c]["name"])
    des = [c for c in by_name if ps[c]["designated"]]
    clr = [c for c in by_name if not ps[c]["designated"]]
    flip = [ps[c]["name"] for c in F["call"]["reach_flips"]]
    cur = [ps[c]["curtail_mw"] for c in des]
    h = F["heaters"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Energy Systems & Utilities (load forecasting).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**%s**" % F["call"]["sentence"])
    L.append("Their forecast lowest demand between 10.00 am and 3.00 pm on the 2027 reference Sunday falls %.1f to "
             "%.1f MW below threshold once the solar soak is placed on the %s controlled-load heaters whose meters "
             "switch on the network's signal. Not the four of the forecast that moves every heater into the window, "
             "which adds the %s heaters on internal time switches that keep heating overnight and so clears %s. Not "
             "the eleven of a forecast with no soak load, which leaves out the heaters the new signal times do move."
             % (min(cur), max(cur), format(h["reached"], ","), format(h["time_switch"], ","), _and(flip)))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. The reference day is Sunday 25 October 2026, network demand **%.1f MW** at its lowest half-hour "
             "between 10.00 am and 3.00 pm." % F["ref_network_min_mw"])
    L.append("2. The new switch-on signals reach **%s** of the %s controlled-load heaters (meters with an integral "
             "audio-frequency receiver); **%s** are on meters with an internal time switch."
             % (format(h["reached"], ","), format(h["total"], ","), format(h["time_switch"], ",")))
    L.append("3. Forecast lowest demand at the designated substations: %s."
             % "; ".join("%s **%.1f MW** against %.1f MW" % (ps[c]["name"], ps[c]["forecast_min_mw"],
                                                            ps[c]["threshold_mw"]) for c in des))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Converted zss_net_demand_spring2026.csv from UTC interval ends to local time (AEDT from 4 October "
             "2026; TIBB is Tibbarin) and took the Sunday with the lowest network half-hour between 10.00 am and "
             "3.00 pm (framework 2.2): 25 October 2026, %.1f MW." % F["ref_network_min_mw"])
    L.append("2. Subtracted each substation's forecast inverter capacity in solar_connections_outlook_2027.xlsx at "
             "that day's output per kW in rooftop_pv_monitoring_spring2026.json (framework 3.1a).")
    L.append("3. Took each heater's daily energy as its controlled-load register kWh (register named in "
             "approved_meter_models.xlsx) over the days read, all its meters, in cl_customer_reads_spring2026.csv "
             "(framework 3.2).")
    L.append("4. Read each heater's current meter in metering_installations_2026-12-11.csv against "
             "approved_meter_models.xlsx: %s heaters have a contactor driven by an integral audio-frequency "
             "receiver and take network_notice_NN-2027-02.pdf's new signals; %s run from an internal time switch "
             "and keep heating overnight." % (format(h["reached"], ","), format(h["time_switch"], ",")))
    L.append("5. Placed each reached heater at its element rating from its group's switch-on "
             "(load_control_register_2026-12-10.csv, the notice) until its daily energy was taken, summed by the "
             "metering register's zone substation, and took each substation's lowest half-hour: %d below their "
             "framework section 4 thresholds." % F["call"]["count"])
    L.append("6. Curtailment is the threshold less the forecast lowest demand; further capacity is the smallest, "
             "over the ten half-hours, of forecast demand less the threshold divided by output per kW.")
    L.append("7. For solar in service on 25 October 2026, chained der_applications_2026-12-08.xlsx through "
             "prior_application, took the latest application commissioned by that day, kept NMIs with a meter in "
             "service that day in the metering register and located them by it: %.2f MW; the backstop share takes "
             "the commissioning of the first application carrying the inverter serial in service, on or after 1 "
             "July 2025 (framework 5.2): %.2f MW." % (F["totals"]["cap_mw"], F["totals"]["backstop_mw"]))
    L.append("8. Designated the %d substations whose forecast lowest demand falls below threshold." % F["call"]["count"])
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### minimum_load_spring_2027.xlsx")
    L.append("")
    L.append("1. Forecast lowest half-hour demand between 10.00 am and 3.00 pm on the reference Sunday, MW to one "
             "decimal:")
    for c in by_name:
        L.append("   - %s: %.1f (threshold %.1f, %s)" % (ps[c]["name"], ps[c]["forecast_min_mw"], ps[c]["threshold_mw"],
                                                       "designated" if ps[c]["designated"] else "clears"))
    L.append("2. Solar a designated substation would have to curtail at its lowest half-hour, MW to one decimal:")
    for c in des:
        L.append("   - %s: %.1f" % (ps[c]["name"], ps[c]["curtail_mw"]))
    L.append("3. Further inverter capacity a cleared substation could take before any half-hour from 10.00 am to "
             "3.00 pm fell below its threshold, MW to one decimal:")
    for c in clr:
        L.append("   - %s: %.1f" % (ps[c]["name"], ps[c]["headroom_mw"]))
    L.append("4. Rooftop solar inverter capacity in service behind each substation on 25 October 2026, and the part "
             "the emergency backstop can curtail, MW to two decimals:")
    for c in by_name:
        L.append("   - %s: %.2f in service, %.2f curtailable" % (ps[c]["name"], ps[c]["in_service_mw"],
                                                                ps[c]["backstop_mw"]))
    L.append("")
    L.append("### minimum_load_briefing_2027.docx")
    L.append("")
    L.append("1. One-page briefing to the Minister recommending the %d designations, with a bar chart of each "
             "substation's forecast lowest demand against its threshold, designated substations in amber."
             % F["call"]["count"])
    L.append("")
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(L))
