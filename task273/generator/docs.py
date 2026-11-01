"""The two governing documents: the site's water supply security standard (the WHAT the call is judged on) and
the regional council's water permit (the take limits and the metering the permit asks for)."""
import io_util as IO


def standard(path):
    b = [
        ("t", "SWS-03 Site water supply security standard"),
        ("s", "Ruawaro Dairy Co-operative Ltd, Kaitanga site. Revision 4, approved by the site drought committee "
              "on 12 August 2025. Owner: site utilities engineer. Supersedes revision 3 (May 2021)."),
        ("h", "1. Purpose"),
        ("p", "The Kaitanga site draws all of its process and cleaning water from its own bore field. This standard "
              "sets the test a summer operating plan for the bore field must pass before the drought committee "
              "adopts it, so that the site can keep producing through a drought as severe as the worst on record "
              "without running a production bore's water level down to its pump."),
        ("h", "2. Scope"),
        ("p", "Every production bore listed in the Kaitanga bore register that the plan takes water from, "
              "including a bore entering supply under the plan. The test covers the months December to March."),
        ("h", "3. Terms"),
        ("table", [["Term", "Meaning"],
                   ["Pumping water level", "A production bore's daily mean water level as its level logger records "
                    "it, in metres below the bore's measuring point."],
                   ["Minimum operating level", "The level in the Kaitanga bore register below which a bore's pump "
                    "is not to run."],
                   ["Planned take", "The average daily take the summer operating plan gives a bore for a month."],
                   ["Design drought", "The groundwater levels Matarae Regional Council's monitoring bore MB1 "
                    "recorded from 1 December 2019 to 31 March 2020, the lowest summer in the MB1 record since the "
                    "bore field was built."]]),
        ("h", "4. The test"),
        ("p", "For each month from December to March, take every production bore at its planned take on every day "
              "of the month, with the aquifer at the level MB1 recorded on each day of the same month of the design "
              "drought. A plan passes when no production bore's pumping water level falls below its minimum "
              "operating level on any of those days."),
        ("p", "The plan put to the committee states, for each production bore and month, the lowest pumping water "
              "level expected under the test, and names any bore and month that fails it."),
        ("h", "5. When the test fails"),
        ("p", "The committee does not adopt a plan that fails the test. The utilities engineer brings back a revised "
              "plan, which may move take between bores, lower the site's take or bring in trucked or town supply "
              "under the contingency arrangements in SWS-05."),
        ("h", "6. Records"),
        ("p", "Daily take, pumping water level and pump run hours for each production bore are kept in the site "
              "SCADA historian and exported monthly. MB1 levels are taken from the regional council's environmental "
              "data portal."),
    ]
    IO.write_pdf(path, "SWS-03 Site water supply security standard", "Allan Morris", "Ruawaro Dairy Co-operative Ltd",
                 b, "SWS-03 rev 4 | Kaitanga site | uncontrolled when printed", "D:20250812031500+12'00'",
                 "D:20250812034200+12'00'")


def permit(path):
    rates = [["Bore", "Maximum rate (L/s)", "Permit meter"],
             ["Bore 1", "48", "WM-30455"], ["Bore 2", "42", "WM-30456"], ["Bore 3", "46", "WM-31690"],
             ["Bore 4", "45", "WM-31702"], ["Bore 5", "44", "WM-33119"], ["Bore 6", "38", "WM-33120"],
             ["Bore 7", "44", "WM-35873"], ["Bore 8", "44", "WM-35874"], ["Bore 9", "53", "to be advised"]]
    b = [
        ("t", "Water permit AUTH-117204"),
        ("s", "Matarae Regional Council. Granted under section 104 of the Resource Management Act 1991 to Ruawaro "
              "Dairy Co-operative Ltd on 3 April 2017; varied 19 October 2026 (addition of Bore 9). Expires 31 March "
              "2047."),
        ("h", "Activity"),
        ("p", "To take groundwater from the Kaitanga gravel aquifer through nine production bores at the Kaitanga "
              "dairy manufacturing site, Mangarewa Road, for milk processing, cleaning and associated uses."),
        ("h", "Conditions"),
        ("p", "1. The combined take from all bores shall not exceed 28,500 cubic metres in any day, and 7,450,000 "
              "cubic metres in any year beginning 1 July."),
        ("p", "2. The rate of take from each bore shall not exceed the rate in Schedule 1."),
        ("p", "3. Each bore shall be fitted with a water meter verified to within plus or minus 5 per cent, connected "
              "to a datalogger that sends the meter's cumulative reading to the Council at intervals of no more "
              "than 15 minutes. The permit holder shall advise the Council within 10 working days of replacing a "
              "meter."),
        ("p", "4. The permit holder shall, by 31 July each year, provide the Council with a report of the volume "
              "taken from each bore in the year ending 30 June."),
        ("p", "5. If the level in the Council's monitoring bore MB1 falls below 30.00 m (NZVD2016), the permit holder "
              "shall reduce the combined take to 26,000 cubic metres per day until the level has been above "
              "30.50 m for 14 consecutive days."),
        ("h", "Schedule 1"),
        ("table", rates),
        ("s", "Advice note: meters are identified by the serial number of the Council's datalogger installation. "
              "Readings are held in NZ Standard Time."),
    ]
    IO.write_pdf(path, "Water permit AUTH-117204", "Matarae Regional Council", "Matarae Regional Council", b,
                 "AUTH-117204 | Matarae Regional Council | consents@matarae.govt.nz", "D:20261019142800+13'00'",
                 "D:20261019143300+13'00'")
