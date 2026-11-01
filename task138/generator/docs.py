"""The pack's PDF documents, each in its issuing body's own voice: the district's levee standard (the WHAT the call is
judged on), the State Water Survey's regional skew update, Table 4 of the 2019 hydraulic update, the district's
flood warning and closure procedure, and the 2025 inspection summary."""
import io_util as IO
import params as PR
import world as W


def sta_str(s):
    return "%d+%02d" % (s // 100, s % 100)


def standard(path):
    b = [
        ("t", "LS-02 Levee design and review standard"),
        ("s", "Orrinsford Levee and Drainage District. Revision 3, adopted by the Board of Trustees on 9 April 2018. "
              "Owner: district engineer. Supersedes revision 2 (March 2009)."),
        ("h", "1. Purpose"),
        ("p", "This standard sets the level of protection the Orrinsford levee is to provide and the review the "
              "district engineer carries out before each five-year capital plan, so that the Board knows whether "
              "the levee crown still meets that level and, where it does not, what crown raise would restore it."),
        ("h", "2. Design flood"),
        ("p", "The design flood is the peak discharge of the Tamsen River at the Orrinsford gauge (State Water Survey "
              "05433000) that has a 1 per cent chance of being exceeded in any year, for the river, its floodplain "
              "and its levees as they stand at the time of the review."),
        ("h", "3. Frequency analysis"),
        ("p", "The frequency curve is a log-Pearson Type III distribution fitted by the method of moments to the "
              "base-10 logarithms of one annual peak discharge for every water year since the Orrinsford gauge "
              "opened in water year 1962. The skew coefficient is the station skew weighted with the generalized "
              "skew of the State Water Survey's current regional skew study, each weighted by the inverse of its "
              "mean square error, the station skew's mean square error taken from that study."),
        ("h", "4. Design water surface"),
        ("p", "The design water surface at each cross-section is read from the water surface table of the district's "
              "current hydraulic study, interpolated linearly in discharge."),
        ("h", "5. Freeboard"),
        ("table", [["Location", "Freeboard above the design water surface"],
                   ["Levee generally", "3.0 ft"],
                   ["Within 100 ft of a bridge or closure structure", "4.0 ft"],
                   ["Upstream allowance (added to the above)", "0.5 ft at station 0+00, decreasing uniformly to "
                    "nothing at the downstream end, station 180+00"]]),
        ("h", "6. Crown check"),
        ("p", "The crown elevation at each cross-section is the elevation shown by the latest certification survey. "
              "The levee meets this standard when, at every cross-section of the hydraulic study, the crown is at "
              "or above the design water surface plus the freeboard."),
        ("h", "7. Crown raises"),
        ("p", "Where the levee does not meet this standard, the review states the uniform crown raise, in whole "
              "feet, that would restore it. Each raise considered is reported with the annual chance that the "
              "river exceeds the discharge the raised levee would hold with its freeboard."),
        ("h", "8. Records"),
        ("p", "Discharges are taken from the State Water Survey's published records; the district's loggers record "
              "stage for flood warning only. Elevations are in feet on NAVD 88 and stations on the levee stationing "
              "in use at the time of the review."),
    ]
    IO.write_pdf(path, "LS-02 Levee design and review standard", "Dennis Zhang",
                 "Orrinsford Levee and Drainage District", b,
                 "LS-02 rev 3 | Orrinsford Levee and Drainage District | uncontrolled when printed",
                 "D:20180409141000-05'00'", "D:20180409143800-05'00'")


def skew_study(path):
    b = [
        ("t", "Regional skew coefficients for annual peak discharges, 2016 update"),
        ("s", "State Water Survey, Surface Water Section. Technical Release SW-16-03, September 2016. Prepared by "
              "Eric Thornton, hydrologist."),
        ("h", "Summary"),
        ("p", "This release replaces the generalized skew map of 1992 with three skew regions fitted to the annual "
              "peak records of 74 long-record streamgauges with little regulation. The generalized skew of a site "
              "is the value for the region holding the county in which the site's streamgauge stands."),
        ("h", "Table 1. Regional skew"),
        ("table", [["Region", "Generalized skew", "Mean square error"],
                   ["1 Northern Till Plain", "-0.25", "0.12"],
                   ["2 Central Lowlands", "-0.08", "0.14"],
                   ["3 Southern Uplands", "0.05", "0.16"]]),
        ("h", "Table 2. Counties by region"),
        ("table", [["Region", "Counties"],
                   ["1 Northern Till Plain", "Ardell, Baines, Corwin, Dunmore, Essling, Hollis, Kerr"],
                   ["2 Central Lowlands", "Fairlee, Marrow, Ostrand, Pell, Quill, Tolliver, Vance, Wexley"],
                   ["3 Southern Uplands", "Garrow, Lisle, Norcross, Pryor, Sumner, Yates"]]),
        ("h", "Weighting a station skew"),
        ("p", "Where a site's own annual peak record gives a station skew G, the skew used for the site is "
              "Gw = (MSE_R x G + MSE_G x G_R) / (MSE_R + MSE_G), where G_R is the generalized skew and MSE_R its "
              "mean square error from Table 1, and MSE_G is the mean square error of the station skew from a record "
              "of N years: MSE_G = 10 ^ (A - B x log10(N / 10)), with A = -0.33 + 0.08 |G| when |G| is 0.90 or less "
              "and A = -0.52 + 0.30 |G| otherwise, and B = 0.94 - 0.26 |G| when |G| is 1.50 or less and B = 0.55 "
              "otherwise."),
        ("p", "The station skew is computed from the base-10 logarithms of the annual peaks as "
              "N x sum((x - mean)^3) / ((N - 1)(N - 2) s^3), with s the sample standard deviation."),
        ("h", "Limitations"),
        ("p", "The regional values describe unregulated peaks. Users should satisfy themselves that a record "
              "represents the conditions for which an estimate is wanted."),
    ]
    IO.write_pdf(path, "Regional skew coefficients for annual peak discharges, 2016 update", "Eric Thornton",
                 "State Water Survey", b, "SW-16-03 | State Water Survey | Surface Water Section",
                 "D:20160926103000-05'00'", "D:20160926104500-05'00'")


def table4(path, t4, pk):
    head = ["Station"] + ["{:,}".format(q) for q in PR.TABLE4_Q]
    rows = [head]
    lab = {6240: " *", 11870: " *"}
    for s in PR.TABLE4_STATIONS:
        rows.append([sta_str(s) + lab.get(s, "")] + ["%.2f" % t4.loc[s, q] for q in PR.TABLE4_Q])
    b = [
        ("t", "Orrinsford Levee Hydraulic Update, 2019"),
        ("s", "Prepared for the Orrinsford Levee and Drainage District by Hernandez Water Engineering, project "
              "HWE-1907. Final report, December 2019. Chapter 4, results."),
        ("h", "Table 4. Computed water surface elevations at levee cross-sections"),
        ("p", "Steady-flow water surface elevations, ft NAVD 88, along the Tamsen River side of the Orrinsford "
              "levee for discharges at the Orrinsford gauge from %s to %s cfs. Stations are on the levee stationing "
              "adopted with the 2019 north tie-in (0+00 at the north tie-in, 180+00 at the south tie-in). Elevations "
              "at the two bridge cross-sections are at the upstream face and include the bridge losses. Channel and "
              "overbank roughness were calibrated to the high water marks of the %s and %s floods."
              % (("{:,}".format(PR.TABLE4_Q[0]), "{:,}".format(PR.TABLE4_Q[-1])) + calib_floods(pk))),
        ("table", rows),
        ("s", "Discharge at the Orrinsford gauge, cfs, across the top of the table. * Bridge cross-section, upstream "
              "face: 62+40 Main Street bridge, 118+70 Prairie and Western Railroad bridge."),
    ]
    w = {11: [18 * 2.83465] + [15.7 * 2.83465] * 10}
    IO.write_pdf(path, "Orrinsford Levee Hydraulic Update 2019 - Table 4", "Jesus Hernandez",
                 "Hernandez Water Engineering", b, "HWE-1907 | Orrinsford Levee Hydraulic Update | Chapter 4",
                 "D:20191216090500-06'00'", "D:20191216091900-06'00'", widths=w)


def calib_floods(pk):
    """The two largest Orrinsford floods of the years before the 2019 study, by month and year."""
    rec = pk[(pk["wy"] >= 2005) & (pk["wy"] <= 2018)].sort_values("hal_q", ascending=False).head(2)
    rec = rec.sort_values("hal_time")
    return tuple(t.strftime("%B %Y") for t in rec["hal_time"])


def procedure(path):
    b = [
        ("t", "Flood warning and closure procedure"),
        ("s", "Orrinsford Levee and Drainage District. Operating procedure OP-04, issued 3 March 2014. Owner: "
              "district engineer."),
        ("h", "1. Watching the river"),
        ("p", "The district follows the Tamsen River at two State Water Survey streamgauges: Coyle Bridge "
              "(05432100), 28 river miles upstream, and Orrinsford (05433000) at the Main Street bridge. Both report "
              "hourly. Flood forecasts for Orrinsford come from the river forecast centre twice a day during a "
              "flood."),
        ("h", "2. Warning"),
        ("p", "When the river at Coyle Bridge reaches the warning level, elevation 661.00 ft NGVD 29 (21.0 ft on the "
              "gauge), and is still rising, the district engineer declares a flood warning, calls out the closure "
              "crews and notifies the city and the Prairie and Western Railroad."),
        ("h", "3. Closures"),
        ("table", [["Closure", "Type", "Install before the river reaches"],
                   ["Main Street", "Aluminium stoplogs, 4 bays", "the closure sill, %.2f ft NAVD 88" % PR.MAIN_ST_SILL],
                   ["Prairie and Western Railroad", "Swing gate", "622.50 ft NAVD 88"]]),
        ("p", "Installing the Main Street stoplogs closes the city's main crossing of the levee and takes a full "
              "crew about 18 hours, including traffic diversion. The railroad gate is closed by the railroad's "
              "own crew on the district's notice."),
        ("h", "4. Standing down"),
        ("p", "Closures are removed once the river at Orrinsford has fallen below the closure sill and the forecast "
              "shows no further rise."),
        ("h", "5. Records"),
        ("p", "The duty officer logs the warning, call-out and closure times. River levels are taken from the "
              "State Water Survey's gauges."),
    ]
    IO.write_pdf(path, "OP-04 Flood warning and closure procedure", "Dennis Zhang",
                 "Orrinsford Levee and Drainage District", b,
                 "OP-04 | Orrinsford Levee and Drainage District | uncontrolled when printed",
                 "D:20140303110000-06'00'", "D:20140303112500-06'00'")


def inspection(path):
    items = [["Item", "Station", "Rating", "Remark"],
             ["Crown: grade, cracking, rutting", "0+00 to 180+00", "Acceptable", "Rutting 29+00 to 33+50 regraded"],
             ["Riverside slope: vegetation", "24+00 to 41+00", "Minimally Acceptable", "Woody growth over 2 in."],
             ["Riverside slope: vegetation", "41+00 to 180+00", "Acceptable", ""],
             ["Landside slope: animal burrows", "133+50, 137+20", "Acceptable", "Backfilled 14 Aug"],
             ["Landside slope: sloughing", "0+00 to 180+00", "Acceptable", "None seen"],
             ["Seepage and sand boils", "0+00 to 180+00", "Acceptable", "None reported since 2024 high water"],
             ["Toe drain outlets", "96+50", "Minimally Acceptable", "Outlet partly silted"],
             ["Relief wells", "102+00 to 108+00", "Acceptable", "7 of 7 pumped"],
             ["Encroachment", "140+00", "Unacceptable", "Grain terminal fence 15 ft from toe"],
             ["Floodwall: joints and panels", "85+00 to 97+00", "Acceptable", "Joint sealant replaced 2023"],
             ["Main Street closure", "62+40", "Acceptable", "Stoplogs inventoried, 2 bays trial fit"],
             ["P&W Railroad closure", "118+70", "Acceptable", "Hinges greased, seal checked"],
             ["PS-1 gravity outlet flap gate", "18+30", "Minimally Acceptable", "Seal worn, part ordered"],
             ["PS-1 pumps", "18+30", "Acceptable", "Run 40 min under load"],
             ["PS-2 pumps", "161+20", "Acceptable", "Run 40 min under load"],
             ["Culverts and pipes through the levee", "various", "Acceptable", "CCTV 2024, no defects"],
             ["Staff gauges and markers", "62+40, 118+70", "Acceptable", "Repainted"],
             ["Overall segment rating", "", "Minimally Acceptable", ""]]
    b = [
        ("t", "Annual levee inspection report"),
        ("s", "Orrinsford Levee and Drainage District, levee segment TR-L-10 (stations 0+00 to 180+00). Inspected 12 "
              "and 13 August 2025 by the district engineer with the State Department of Natural Resources levee "
              "safety officer. Report dated 29 August 2025."),
        ("table", items),
        ("s", "Ratings: Acceptable, Minimally Acceptable, Unacceptable, per the DNR levee inspection checklist."),
    ]
    w = {4: [52 * 2.83465, 34 * 2.83465, 34 * 2.83465, 56 * 2.83465]}
    IO.write_pdf(path, "2025 annual levee inspection report", "Dennis Zhang", "Orrinsford Levee and Drainage District",
                 b, "2025 annual inspection | Orrinsford Levee and Drainage District | segment TR-L-10",
                 "D:20250829150000-05'00'", "D:20250829152200-05'00'", widths=w)
