"""The PDFs in the pack: the cooperative's planning criteria, its 2027 operating plan, the 2025 pilot's test plan,
the July 2026 switching order and the wholesale supplier's delivery point schedule."""
import pandas as pd

import io_util as IO
import params as PR
import world as W

COOP = "Breckwater Electric Cooperative"


def criteria(path):
    b = [
        ("t", "Distribution Planning Criteria"),
        ("s", "%s. Revision 4, adopted by the Board of Directors on 27 February 2024 (resolution 2024-06). Owner: "
              "Manager of Engineering. Prepared by Julie Gibbs, P.E., System Planning Engineer. Supersedes revision "
              "3 (April 2019)." % COOP),
        ("h", "1. Purpose"),
        ("p", "These criteria set how the cooperative judges whether each distribution substation can serve its summer "
              "load with its largest transformer out of service, and how much load must be served from other "
              "substations when it cannot. They govern the capacity review that the system planning engineer "
              "prepares each autumn for the construction work plan and the next year's budget."),
        ("h", "2. Terms"),
        ("table", [["Term", "Meaning in these criteria"],
                   ["Summer", "1 June to 30 September."],
                   ["Substation load", "The sum of the loads of the substation's feeders, as hourly average MW from "
                                       "the SCADA historian."],
                   ["Firm rating", "The load the substation can carry with its largest transformer out of service "
                                   "(Table 1)."],
                   ["Design temperature", "The daily maximum temperature at the substation's weather station that "
                                          "the planning peak is set at (Table 1)."],
                   ["Operating plan", "The plan the Board approves each year for how the system is to be run in the "
                                      "following calendar year: feeder configuration, voltage settings, load control."],
                   ["Switching block", "0.5 MW, the smallest load the cooperative plans to move between substations "
                                       "through feeder ties."]]),
        ("h", "3. Planning peak"),
        ("p", "3.1 The planning peak of a substation for a summer is the highest hourly substation load expected on a "
              "day whose maximum temperature reaches the design temperature, with every feeder run as the operating "
              "plan for that summer sets it."),
        ("p", "3.2 The weather-normal peak is read from the five most recent complete summers, with the feeders as "
              "they ran in those summers. For each summer day take the highest hourly substation load and the day's "
              "maximum temperature at the substation's weather station, and fit a straight line by least squares to "
              "the days whose maximum temperature was 85 F or more. The weather-normal peak is the line's value at "
              "the design temperature. It stands for the middle summer of the five and is carried to a later summer "
              "at the substation's base case growth rate in the current load forecast, compounded yearly."),
        ("p", "3.3 Where the operating plan for a summer runs the feeders differently from the way they ran in the "
              "five summers of 3.2 (voltage settings, load control, feeder configuration), the planning peak is the "
              "weather-normal peak carried to that summer and adjusted by the change's effect on the substation load "
              "at the planning peak. Otherwise the planning peak is the weather-normal peak carried to that summer."),
        ("h", "4. Firm capacity"),
        ("p", "4.1 A substation's planning peak is not to exceed its firm rating. Where it does, the transfer "
              "requirement for that summer is the excess of the planning peak over the firm rating rounded up to "
              "whole switching blocks: the load that other substations must carry through feeder ties in that "
              "summer. A summer with no excess has no transfer requirement."),
        ("p", "4.2 The capacity review states, for every summer of the construction work plan, each substation's "
              "planning peak and transfer requirement. A transfer requirement that the feeder ties cannot meet is "
              "carried into the construction work plan as a substation project."),
        ("h", "Table 1. Firm ratings and design temperatures"),
        ("table", [["Substation", "Transformers", "Firm rating (MW)", "Weather station", "Design temperature"],
                   ["Carrow Creek", "2 x 30/40/50 MVA", "48.0", "Mossford Municipal Airport", "101 F"],
                   ["Dunraith", "2 x 75/100/125 MVA", "104.0", "Mossford Municipal Airport", "101 F"],
                   ["Lindell", "1 x 20/26.7 MVA, mobile backup", "22.5", "Harrow County Airport", "99 F"],
                   ["Ostby", "2 x 45/60/75 MVA", "63.0", "Mossford Municipal Airport", "101 F"],
                   ["Tessaly", "2 x 20/26.7/33.3 MVA", "30.5", "Harrow County Airport", "99 F"]]),
        ("h", "5. Records"),
        ("p", "Loads are taken from the SCADA historian and temperatures from the airport's routine and special "
              "observations. Where the historian holds no value for an hour, the hour is left out."),
    ]
    IO.write_pdf(path, "Distribution Planning Criteria, revision 4", "Julie Gibbs", COOP, b,
                 "Distribution Planning Criteria rev 4 | %s | uncontrolled when printed" % COOP,
                 "D:20240227101500-06'00'", "D:20240227104100-06'00'",
                 widths={5: [26 * 2.83465, 44 * 2.83465, 26 * 2.83465, 46 * 2.83465, 28 * 2.83465]})


def operating_plan(path):
    b = [
        ("t", "2027 Operating Plan"),
        ("s", "%s. Approved by the Board of Directors on 22 September 2026 (resolution 2026-31). Presented by "
              "Peter Roman, Manager of Operations." % COOP),
        ("h", "1. Scope"),
        ("p", "This plan sets how the cooperative's distribution system is to be run from 1 January to 31 December "
              "2027: the normal feeder configuration, voltage settings at the substations and on the feeders, and "
              "the reliability programs the operations department carries out."),
        ("h", "2. Feeder configuration"),
        ("p", "The normal configuration is the one in force after switching order SO-2026-114 (Dunraith, 30 June "
              "2026). No other change to normal open points is planned for 2027."),
        ("h", "3. Voltage"),
        ("p", "3.1 Conservation voltage reduction runs on every Dunraith feeder from 1 June 2027, at all hours, with "
              "the settings of the 2025 Dunraith pilot: feeder regulator bandcenter 119.2 V on a 120 V base "
              "(normal setting 123.5 V), bandwidth 2.0 V, line drop compensation off."),
        ("p", "3.2 AMI bellwether meters at the end of each Dunraith feeder are read every 15 minutes. If a "
              "bellwether meter reads below 114 V for 15 minutes the dispatcher returns that feeder to the normal "
              "setting and notifies the operations engineer."),
        ("p", "3.3 The other substations keep the normal setting through 2027."),
        ("h", "4. Reliability programs"),
        ("table", [["Program", "2027 scope"],
                   ["Right-of-way clearing", "Four-year cycle: Ostby and Lindell circuits, 412 miles"],
                   ["Pole inspection and treatment", "Ten-year cycle: about 3,900 poles, Carrow Creek and Tessaly"],
                   ["Regulator and recloser maintenance", "Annual: all substation regulators before 15 May"],
                   ["Underground cable replacement", "East Mossford subdivisions, phase 3, 2.6 miles"]]),
        ("h", "5. Reporting"),
        ("p", "Operations reports CVR suspensions and bellwether voltage exceptions to the Board each quarter."),
    ]
    IO.write_pdf(path, "2027 Operating Plan", "Peter Roman", COOP, b,
                 "2027 Operating Plan | %s | Board approved 22 September 2026" % COOP,
                 "D:20260923090500-05'00'", "D:20260923091800-05'00'")


def test_plan(path):
    weeks = [["Week starting (Monday 00:00)", "DUN-2, DUN-5, DUN-7"]]
    for t, act in W.pilot_schedule():
        weeks.append([t.strftime("%a %d %b %Y"), "CVR on" if act == "ON" else "normal"])
    b = [
        ("t", "Conservation voltage reduction pilot, Dunraith, summer 2025: test plan"),
        ("s", "%s, Operations. Prepared by Peter Roman, Manager of Operations, 16 May 2025. Reviewed by Julie "
              "Gibbs, System Planning Engineer." % COOP),
        ("h", "1. Purpose"),
        ("p", "To run conservation voltage reduction (CVR) on three Dunraith feeders through summer 2025 and record "
              "what it does to their load and to members' voltages, ahead of the Board's decision on CVR for every "
              "Dunraith feeder."),
        ("h", "2. Feeders"),
        ("p", "Pilot feeders: DUN-2, DUN-5 and DUN-7. Each has a three-phase feeder regulator bank at the "
              "substation and an AMI bellwether meter at its far end. DUN-1, DUN-3, DUN-4, DUN-6 and DUN-8 stay at "
              "the normal setting for the whole summer."),
        ("h", "3. Settings"),
        ("table", [["", "Normal", "CVR"],
                   ["Regulator bandcenter (120 V base)", "123.5 V", "119.2 V"],
                   ["Bandwidth", "2.0 V", "2.0 V"],
                   ["Time delay", "45 s", "45 s"],
                   ["Line drop compensation", "off", "off"]]),
        ("h", "4. Schedule"),
        ("p", "CVR is switched on and off by SCADA command to the pilot regulators at 00:00 each Monday, alternate "
              "weeks, from Monday 2 June 2025 until the pilot ends at 00:00 on Monday 29 September 2025. If a "
              "command fails, the dispatcher sends a line crew to make the change at the controller and logs the "
              "time."),
        ("table", weeks),
        ("h", "5. Voltage floor"),
        ("p", "If a pilot bellwether meter reads below 114 V for 15 minutes the dispatcher returns that feeder to "
              "the normal setting for the rest of the week."),
        ("h", "6. Records"),
        ("p", "SCADA historian: hourly average MW of every Dunraith feeder. Regulator controllers: event log of "
              "setting changes and commands. AMI: bellwether voltages (meter services)."),
    ]
    IO.write_pdf(path, "CVR pilot test plan, Dunraith 2025", "Peter Roman", COOP, b,
                 "CVR pilot test plan | %s Operations | 16 May 2025" % COOP,
                 "D:20250516142000-05'00'", "D:20250516150400-05'00'")


def switching_order(path):
    b = [
        ("t", "Switching order SO-2026-114"),
        ("s", "%s. Dunraith feeder rebalancing. Written by Julie Gibbs, 18 June 2026. Approved by Peter Roman, "
              "22 June 2026. Dispatcher: Luis Ortega. Crew: Line Crew 3." % COOP),
        ("h", "Purpose"),
        ("p", "Move three line sections between Dunraith feeders to even out feeder loading. The moved sections "
              "become part of their new feeders' normal configuration."),
        ("h", "Steps (30 June 2026)"),
        ("table", [["Step", "Time", "Device", "Operation", "Result"],
                   ["1", "23:22", "TS-2236 (DUN-4 / DUN-8 tie)", "Close", "DUN-4 and DUN-8 paralleled"],
                   ["2", "23:27", "S-4471 (DUN-4)", "Open", "Section beyond S-4471 fed from DUN-8"],
                   ["3", "23:35", "TS-2252 (DUN-6 / DUN-2 tie)", "Close", "DUN-6 and DUN-2 paralleled"],
                   ["4", "23:39", "S-6120 (DUN-6)", "Open", "Section beyond S-6120 fed from DUN-2"],
                   ["5", "23:47", "TS-2219 (DUN-1 / DUN-3 tie)", "Close", "DUN-1 and DUN-3 paralleled"],
                   ["6", "23:52", "S-1302 (DUN-1)", "Open", "Section beyond S-1302 fed from DUN-3"],
                   ["7", "23:58", "", "Order complete, reported to dispatcher", ""]]),
        ("h", "Closeout"),
        ("p", "Order completed 30 June 2026 23:58 without outage. Normal open points now S-4471, S-6120 and S-1302; "
              "TS-2236, TS-2252 and TS-2219 normally closed."),
    ]
    IO.write_pdf(path, "SO-2026-114 Dunraith feeder rebalancing", "Julie Gibbs", COOP, b,
                 "SO-2026-114 | %s dispatch | completed 30 Jun 2026" % COOP,
                 "D:20260618103000-05'00'", "D:20260701001500-05'00'")


def delivery_points(path):
    b = [
        ("t", "Exhibit A: Delivery points and metering"),
        ("s", "Wholesale Power Contract between Westmarch Generation and Transmission Cooperative and %s. Exhibit A, "
              "revision 2024-1, effective 1 January 2024." % COOP),
        ("p", "Power is delivered to the Member at the delivery points below and measured at the metering points "
              "shown. Delivery point demand is the sum of the demands at its metering points in the same 15-minute "
              "interval. Metering points are read by Westmarch."),
        ("table", [["Delivery point", "Metering point (recorder)", "Location and voltage", "Notes"],
                   ["DP-0412 Carrow Creek", "41-1980", "Carrow Creek T1, 24.9 kV", ""],
                   ["DP-0412 Carrow Creek", "41-1981", "Carrow Creek T2, 24.9 kV", ""],
                   ["DP-0417 Dunraith", "41-2207", "Dunraith T1, 24.9 kV low side", ""],
                   ["DP-0417 Dunraith", "41-2208", "Dunraith T2, 24.9 kV low side", ""],
                   ["DP-0417 Dunraith", "41-2391", "Dunraith 69 kV, line terminal L3", "Rider LL-1"],
                   ["DP-0421 Ostby", "41-2455", "Ostby T1, 24.9 kV", ""],
                   ["DP-0421 Ostby", "41-2456", "Ostby T2, 24.9 kV", ""],
                   ["DP-0430 Lindell", "41-2610", "Lindell T1, 12.47 kV", "Mobile substation metered at 41-2611 "
                                                                         "when in service"],
                   ["DP-0433 Tessaly", "41-2702", "Tessaly T1, 24.9 kV", ""],
                   ["DP-0433 Tessaly", "41-2703", "Tessaly T2, 24.9 kV", ""]]),
        ("p", "Metering point changes are made by written notice and take effect on the first day of the following "
              "billing month."),
    ]
    IO.write_pdf(path, "WPC Exhibit A delivery points", "Westmarch Contracts", "Westmarch Generation and "
                 "Transmission Cooperative", b,
                 "Exhibit A rev 2024-1 | Westmarch G&T | Member: %s" % COOP,
                 "D:20231205110000-06'00'", "D:20231205113000-06'00'",
                 widths={4: [32 * 2.83465, 34 * 2.83465, 58 * 2.83465, 46 * 2.83465]})
