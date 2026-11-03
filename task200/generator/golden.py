"""The two deliverables the prompt asks for: remedial_course_2027.xlsx and remedial_course_2027_note.docx."""
import os

import pandas as pd

import office as O

XLSX = "remedial_course_2027.xlsx"
DOCX = "remedial_course_2027_note.docx"
MONTHS = ["February", "March", "April", "May", "June", "July"]


def _pct(x):
    return int(round(100 * x))


def write(folder, A):
    os.makedirs(folder, exist_ok=True)
    order = A["order"]
    rows = []
    for m, t in zip(MONTHS, order):
        f = A["first"][t]
        a = A["all"][t]
        rows.append({"Course month (2027)": m, "Team": t,
                     "Images met for the first time": f["n"], "Found": f["hits"], "Found (%)": _pct(f["rate"]),
                     "All projections shown": a["n"], "Found, all projections": a["hits"],
                     "Found, all projections (%)": _pct(a["rate"])})
    order_df = pd.DataFrame(rows)
    teams = []
    for t in sorted(A["hours"]):
        teams.append({"Team": t, "Screen time 2026 (hours)": A["hours"][t], "Clear searches 2026": A["clear"][t],
                      "Certificates running out before 1 July 2027": A["certs"][t]})
    teams.append({"Team": "Airport", "Screen time 2026 (hours)": round(sum(A["hours_exact"].values()) + 1e-9, 1),
                  "Clear searches 2026": sum(A["clear"].values()),
                  "Certificates running out before 1 July 2027": sum(A["certs"].values())})
    teams_df = pd.DataFrame(teams)
    notes = {"Course order": [
        "Remedial image interpretation course 2027: order of teams",
        "Prepared 20 January 2027 from the TIP exports and the Pier B TIP log, teams as rostered on 31 December 2026 "
        "(SPS-04 section 3).",
        "Found on first meetings: projections of a threat image the screener had not been shown before, counted back to "
        "each library's load; cancelled projections left out.",
        "On images already met every team finds more, so the all-projections column is shown for reference only."],
        "Teams 2026": [
            "Screening teams, 2026: screen time, clear searches and certificates",
            "Screen time is logged-on time at an X-ray screen; clear searches are charged to the screener whose reject "
            "sent the tray; certificates run three years from the assessment that awarded them, read from the LMS and "
            "from the assessment centre's own certificate list (SPS-04 section 3)."]}
    O.xlsx(os.path.join(folder, XLSX), [("Course order", order_df), ("Teams 2026", teams_df)],
           author="Security Screening", created="2027-01-19T08:41:00Z", modified="2027-01-20T16:12:00Z",
           widths={"Course order": [19, 9, 14, 9, 10, 13, 13, 13], "Teams 2026": [10, 16, 13, 22]},
           notes_rows=notes, number_formats={"Teams 2026": {"Screen time 2026 (hours)": "#,##0.0",
                                                           "Clear searches 2026": "#,##0"},
                                             "Course order": {"Images met for the first time": "#,##0",
                                                              "Found": "#,##0", "All projections shown": "#,##0",
                                                              "Found, all projections": "#,##0"}})
    o = order
    f = A["first"]
    al = A["all"]
    blocks = [
        ("Heading1", "%s first on the 2027 remedial image interpretation course" % o[0]),
        (None, "To: Marian Taylor, Head of Security Screening. From: Security Screening, standards and training. "
               "Date: 20 January 2027. Subject: order of the 2027 remedial course (SPS-04 section 4)."),
        (None, "**The course should run %s, %s, %s, %s, %s, %s, one team a month from February.**" % tuple(o)),
        (None, "SPS-04 puts first the team whose X-ray operators are least likely to find a prohibited article in a "
               "passenger's bag. A real article is always new to the screener, so I read each team on the threat "
               "images its operators met for the first time in 2026. %s found %d per cent of those (%s of %s), the "
               "lowest at the airport; %s is next at %d per cent and %s highest at %d per cent." % (
                   o[0], _pct(f[o[0]]["rate"]), "{:,}".format(f[o[0]]["hits"]), "{:,}".format(f[o[0]]["n"]),
                   o[1], _pct(f[o[1]]["rate"]), o[-1], _pct(f[o[-1]]["rate"]))),
        (None, "On every projection the order looks different: %s finds %d per cent and %s %d per cent. The "
               "difference is the Pier B library. The Pier B screens draw their projections from a small set of "
               "images that %s's operators see again and again, so in 2026 %s of the team's %s projections were "
               "images its operators had met before, and on those they find %d per cent. The Central CT library is "
               "large and most Central projections are first meetings, so the overall score flatters %s far more than "
               "any other team." % (o[1], _pct(al[o[1]]["rate"]), o[0], _pct(al[o[0]]["rate"]), o[0],
                          "{:,}".format(A["met_n"][o[0]]), "{:,}".format(A["all"][o[0]]["n"]),
                          _pct(A["met_rate"][o[0]]), o[0])),
        (None, "Reading the teams on d-prime against their clear searches would put %s first, because %s sends "
               "the most trays to search that come back clear; that measures how well a team separates threats from "
               "clutter, not how often it finds a threat, which is what SPS-04 orders the course by." % (
                   A["dprime_first"], A["dprime_first"])),
        (None, "The workbook remedial_course_2027.xlsx carries the order with each team's first-meeting and overall "
               "figures, and for the cover plan each team's 2026 screen time, its clear searches and its screeners "
               "whose image interpretation certificate runs out before 1 July 2027, who can be recertified on the "
               "course."),
        ("TABLE", ([["Month", "Team", "Found, first meetings", "Found, all projections"]] +
                   [[m, t, "%d%%" % _pct(f[t]["rate"]), "%d%%" % _pct(al[t]["rate"])] for m, t in zip(MONTHS, o)],
                   [1500, 1500, 2600, 2600])),
        (None, "Source: CT TIP exports 2024 to 2026 and the Pier B TIP log, 2026 projections, teams as rostered on "
               "31 December 2026. Cancelled projections are left out, as SPS-04 section 3 has it."),
    ]
    O.docx(os.path.join(folder, DOCX), blocks, author="Security Screening", created="2027-01-19T15:02:00Z",
           modified="2027-01-20T16:30:00Z", revision=6, total_time=74)
