"""The pack's documents for task270: the 2027 proxy metric standard and the experimentation platform guide (PDF), the
scorecard export notes (TXT), the metric catalogue (YAML), the data dictionary (CSV) and the acquisition spend
workbook (XLSX)."""
from __future__ import annotations

import csv

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import cm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle      # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
INK, GREY, RULE = colors.HexColor("#1f2328"), colors.HexColor("#5b6470"), colors.HexColor("#c3c9d0")
GREEN = colors.HexColor("#0f6b4f")
SLATE = colors.HexColor("#33475b")


def styles(accent):
    body = ParagraphStyle("b", fontName="Sans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName="Sans-B", fontSize=14.0, leading=17.5, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName="Sans-B", fontSize=10.4, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName="Sans", fontSize=8.3, leading=11, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=7.9, leading=9.9, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=7.9, leading=9.9, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=26, firstLineIndent=-26))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.3)
        canvas.drawString(2.0 * cm, A4[1] - 1.25 * cm, left)
        canvas.drawRightString(A4[0] - 2.0 * cm, A4[1] - 1.25 * cm, right)
        canvas.drawRightString(A4[0] - 2.0 * cm, 1.1 * cm, "%d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.6),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


def _doc(path, title, author, left, right):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.0 * cm, rightMargin=2.0 * cm, topMargin=2.0 * cm,
                             bottomMargin=1.9 * cm, title=title, author=author, subject=title, creator=author,
                             producer=author), _frame(left, right)


# ----------------------------------------------------------------------------------------------------- the standard
def write_standard(path):
    S = styles(GREEN)
    doc, fr = _doc(path, "Proxy metric standard for onboarding experiments, 2027", K.HEAD_EXP,
                   "%s Growth" % K.ORG, "Proxy metric standard 2027")
    st = [Paragraph("Proxy metric standard for onboarding experiments, 2027", S["h1"]),
          Paragraph("%s Growth. Owner: %s, Head of Experimentation. Version 2027.1, approved by the growth leadership "
                    "team on 12 October 2026; replaces the 2026 reading guide for onboarding experiments." %
                    (K.ORG, K.HEAD_EXP), S["meta"]),
          Paragraph("1. Why a proxy", S["h2"]),
          _clause(S, "1.1", "We judge onboarding changes by how many of our new users are still with us six months "
                            "after they sign up. That read arrives half a year after a change ships, so from 1 January "
                            "2027 every onboarding experiment is read at two weeks on one proxy metric, and its "
                            "six-month read follows as the check."),
          _clause(S, "1.2", "The proxy is chosen once a year from the metrics the metric catalogue marks as "
                            "candidates for that year's review."),
          Paragraph("2. Choosing the proxy", S["h2"]),
          _clause(S, "2.1", "The proxy is the candidate whose movement in an experiment best tells us how the change "
                            "will move six-month retention across all our new users once it ships."),
          _clause(S, "2.2", "Each candidate is judged by the correlation, across our past onboarding changes, between "
                            "the change's effect on the candidate and the change's effect on six-month retention. The "
                            "candidate with the highest correlation is the proxy for the year."),
          _clause(S, "2.3", "A change's effect on a metric is the difference the change makes to the metric's mean "
                            "across all our new users. An experiment measures it on the users it enrols; the "
                            "correlation in 2.2 is between the changes' effects themselves."),
          _clause(S, "2.4", "The past changes are those tested in onboarding experiments that started on or after "
                            "1 January 2024 and whose six-month read had closed by the review's data cut, the "
                            "scorecard export of 23 October 2026. Each treatment arm tested against its "
                            "experiment's control is one change, and each change counts once. An experiment that "
                            "failed the sample-ratio check is not read; an experiment stopped before its planned end "
                            "is read on the users it enrolled."),
          _clause(S, "2.5", "Six-month retention is retained_m6, and every metric is as the metric catalogue defines "
                            "it."),
          Paragraph("3. Reading experiments in 2027", S["h2"]),
          _clause(S, "3.1", "A 2027 onboarding change ships when, at two weeks, the proxy rises at the 5 per cent level "
                            "in a two-sided test and neither guardrail (uninstalled_d14, support_contacts_d14) "
                            "worsens at that level."),
          _clause(S, "3.2", "The owning team sizes each experiment so that the smallest effect on the proxy it can "
                            "detect with 80 per cent power is no larger than the effect the team expects. Experiments "
                            "run in their layer for the dates on the onboarding calendar."),
          _clause(S, "3.3", "The six-month read of every 2027 change is reported to the growth leadership team when "
                            "it closes."),
          Paragraph("4. The review", S["h2"]),
          _clause(S, "4.1", "The proxy review gives each candidate's correlation and names the proxy. It goes to the "
                            "growth leadership team before the 2027 onboarding calendar opens on 4 January 2027."),
          _clause(S, "4.2", "The review is repeated each autumn on the changes whose six-month read closed in the "
                            "year.")]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------- the platform guide
def write_guide(path):
    S = styles(SLATE)
    doc, fr = _doc(path, "Experimentation platform: how onboarding experiments run", K.ENGINEER,
                   "%s Experimentation Platform" % K.ORG, "Platform guide, onboarding layers")
    st = [Paragraph("How onboarding experiments run on the experimentation platform", S["h1"]),
          Paragraph("%s Experimentation Platform. Maintained by %s, data engineering. Revised 5 October 2026 for "
                    "the 2027 holdout." % (K.ORG, K.ENGINEER), S["meta"]),
          Paragraph("Assignment", S["h2"]),
          _clause(S, "A1", "A new consumer user is assigned when they first open the app after signing up. Business "
                           "(seller) accounts are not assigned and are not part of any holdout."),
          _clause(S, "A2", "The global holdout is set aside first: a random 5 per cent of each year's new consumer "
                           "users in 2025 and 2026, and a random 3 per cent from 1 January 2027, about 430 new users "
                           "a week in the first quarter. A holdout user keeps "
                           "the onboarding as it stood on 1 January of their sign-up year and enters no onboarding "
                           "experiment."),
          _clause(S, "A3", "Every other new consumer user is assigned once in each of the three onboarding layers: "
                           "signup_flow, first_feed and notifications. Within a layer, experiments are mutually "
                           "exclusive: on each day, the layer's new users on each platform are split evenly among the "
                           "layer's experiments that are live that day on that platform."),
          _clause(S, "A4", "Within an experiment, users are split evenly among its arms. An experiment enrols from "
                           "the start of its start date to the end of its end date, Amsterdam time."),
          Paragraph("Scorecards", S["h2"]),
          _clause(S, "S1", "The platform computes a scorecard for each arm: the arm's users, and each metric's mean "
                           "and standard deviation over those users. Two-week metrics are computed the day after the "
                           "last enrolled user's fourteenth day, and retained_m6 when the experiment's six-month read "
                           "closes, 180 days after its last enrolment day."),
          _clause(S, "S2", "Each experiment's arm sizes are tested against an even split with a chi-squared test. An "
                           "experiment fails the sample-ratio check at p &lt; 0.001; the registry records the result."),
          _clause(S, "S3", "Metric keys were renamed on 3 March 2025 when the metric store moved; scorecards computed "
                           "before that date carry the former keys, which the metric catalogue lists."),
          Paragraph("Data kept", S["h2"]),
          _clause(S, "D1", "User-level experiment data is deleted once an experiment's six-month read closes; its "
                           "scorecards are kept. The global holdout's user table is kept until the year's holdout "
                           "review."),
          Paragraph("Layers in 2027", S["h2"]),
          _table(S, [["Layer", "What it changes", "Platforms"],
                     ["signup_flow", "Sign-up screens up to the first feed", "iOS and Android"],
                     ["first_feed", "The first feed and the first item pages", "iOS and Android"],
                     ["notifications", "Pushes and in-app messages in the first 14 days", "iOS and Android"]],
                 [3.2, 9.0, 4.0]),
          Paragraph("An experiment on the onboarding calendar may run on one platform only; its platforms are on the "
                    "calendar.", S["body"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------ the export notes
def write_export_notes(path, counts):
    text = """Kleerwissel experimentation platform: scorecard export
=========================================================
File:      experiment_scorecards_2024_2026.csv
Exported:  23 October 2026, 07:12 (Europe/Amsterdam)
By:        %s, data engineering
Scope:     every onboarding experiment started from 8 January 2024 whose two-week scorecards had
           been computed by the export ({experiments} experiments, {rows} rows)

Columns
-------
experiment_id   the experiment's id in the registry (onboarding_experiments_2024_2026.csv)
arm             the arm's label as the owning team named it; the registry gives each experiment's
                arms and its control arm
metric          the metric's key as stored when the scorecard was computed
users           users assigned to the arm and counted in its scorecard
mean            the metric's mean over those users
std_dev         the metric's standard deviation over those users (n - 1)
computed_at     the date the platform computed the scorecard

Rows
----
One row per experiment, arm, metric and computation. Two-week metrics (the five candidates and
the two guardrails) come from the computation the day after the last enrolled user's day 14;
retained_m6 comes from the computation when the six-month read closes, so experiments whose
six-month read is still open have no retained_m6 rows yet.

Experiments in the signup_flow and first_feed layers whose two-week scorecards were computed
between 1 July and 10 September 2025 were computed again on 15 September 2025, after iOS events
held back by an SDK fault were delivered. A scorecard computed again replaces the earlier
computation for every purpose; the export keeps both rows.

Keys were renamed on 3 March 2025 (metric store migration). See metric_catalogue.yaml for the
former key of each metric.

Numbers are written to six decimals. Questions to the data engineering channel.
""" % K.ENGINEER
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.format(**counts))


# ----------------------------------------------------------------------------------------------- the catalogue
CATALOGUE = [
    ("active_days_d1_14", "act_days_14", "Active days, days 1 to 14", "days", "count",
     "Days from day 1 to day 14 after sign-up on which the user opened the app. Day 1 is the sign-up day, "
     "Amsterdam time.", "candidate", "2021-04"),
    ("sessions_d1_14", "sess_count_14", "Sessions, days 1 to 14", "sessions", "count",
     "App sessions from day 1 to day 14 after sign-up. A session ends after 30 minutes without an event.",
     "candidate", "2021-04"),
    ("first_purchase_d14", "first_buy_14", "First purchase within 14 days", "share of users", "binary",
     "1 when the user completed a purchase (paid, not cancelled within 48 hours) within 14 days of sign-up, "
     "otherwise 0.", "candidate", "2022-02"),
    ("items_saved_d1_14", "fav_saves_14", "Items saved, days 1 to 14", "items", "count",
     "Items the user added to favourites from day 1 to day 14 after sign-up and had not removed by the end of day 14.",
     "candidate", "2022-09"),
    ("push_opens_d1_14", "push_open_14", "Push notifications opened, days 1 to 14", "opens", "count",
     "Push notifications the user opened from day 1 to day 14 after sign-up, one open per notification. Users "
     "without push permission count 0.", "candidate", "2023-03"),
    ("retained_m6", "ret_d180", "Retained at six months", "share of users", "binary",
     "1 when the user opened the app on at least one day from day 151 to day 180 after sign-up, otherwise 0.",
     "north star (onboarding)", "2021-04"),
    ("uninstalled_d14", "uninst_14", "Uninstalled within 14 days", "share of users", "binary",
     "1 when the app was uninstalled from the user's last active device within 14 days of sign-up.", "guardrail",
     "2023-06"),
    ("support_contacts_d14", "cs_contacts_14", "Support contacts, days 1 to 14", "contacts", "count",
     "Contacts the user opened with customer support from day 1 to day 14 after sign-up.", "guardrail", "2023-06"),
    ("gmv_d30", None, "Gross merchandise value, days 1 to 30", "EUR", "sum",
     "Value of the user's completed purchases in their first 30 days, excluding buyer protection fees and shipping.",
     "reporting", "2022-02"),
    ("listings_d30", None, "Items listed, days 1 to 30", "items", "count",
     "Items the user listed for sale in their first 30 days.", "reporting", "2022-02"),
]


def write_catalogue(path):
    out = ["# Kleerwissel metric catalogue: growth metrics",
           "# exported from the metric store on 2026-10-20",
           "# owner: growth analytics (%s)" % K.ANALYST,
           "# proxy_review_2027: the candidates for the 2027 proxy review are marked 'candidate'", "", "metrics:"]
    for key, old, name, unit, typ, defn, role, since in CATALOGUE:
        out.append("  - key: %s" % key)
        if old:
            out.append("    former_key: %s     # until 2025-03-03" % old)
        out.append("    name: \"%s\"" % name)
        out.append("    unit: %s" % unit)
        out.append("    type: %s" % typ)
        out.append("    definition: >-")
        words, line = defn.split(), "     "
        for wd in words:
            if len(line) + len(wd) + 1 > 100:
                out.append(line)
                line = "     "
            line += " " + wd
        out.append(line)
        if role == "candidate":
            out.append("    proxy_review_2027: candidate")
        else:
            out.append("    role: %s" % role)
        out.append("    in_scorecards: %s" % ("true" if old else "false"))
        out.append("    since: \"%s\"" % since)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


# --------------------------------------------------------------------------------------------- the dictionary
DICTIONARY = [
    ("onboarding_experiments_2024_2026.csv", "experiment_id", "Registry id of the experiment"),
    ("onboarding_experiments_2024_2026.csv", "layer", "Onboarding layer the experiment ran in"),
    ("onboarding_experiments_2024_2026.csv", "start_date", "First enrolment day"),
    ("onboarding_experiments_2024_2026.csv", "planned_end_date", "Last enrolment day as planned at launch"),
    ("onboarding_experiments_2024_2026.csv", "end_date", "Last enrolment day; blank while enrolling"),
    ("onboarding_experiments_2024_2026.csv", "arms", "Arm labels, separated by semicolons"),
    ("onboarding_experiments_2024_2026.csv", "control_arm", "Label of the control arm"),
    ("onboarding_experiments_2024_2026.csv", "status", "completed, stopped_early, analysing or running"),
    ("onboarding_experiments_2024_2026.csv", "srm_check", "Sample-ratio check result: pass or fail"),
    ("onboarding_experiments_2024_2026.csv", "decision", "The owning team's decision at the two-week read"),
    ("onboarding_experiments_2024_2026.csv", "shipped_on", "Date the shipped arm went to all new users"),
    ("onboarding_experiments_2024_2026.csv", "six_month_read_closes", "Date the six-month read closes"),
    ("global_holdout_users_2025.csv", "user_id", "Pseudonymous user id; one row per user in the 2025 global holdout"),
    ("global_holdout_users_2025.csv", "signed_up_on", "Sign-up date, Amsterdam time"),
    ("global_holdout_users_2025.csv", "platform", "Platform of the first app open"),
    ("global_holdout_users_2025.csv", "country", "Country of the account"),
    ("global_holdout_users_2025.csv", "active_days_d1_14 to retained_m6", "The user's value of each metric, as the metric catalogue defines it"),
    ("signup_cohorts_2025.csv", "signup_date", "Sign-up date, Amsterdam time"),
    ("signup_cohorts_2025.csv", "account_type", "The account's type at the table's refresh: consumer or business"),
    ("signup_cohorts_2025.csv", "signup_account_type", "The type the account signed up as: consumer or business"),
    ("signup_cohorts_2025.csv", "new_users", "Accounts that signed up on the day, platform and country"),
    ("signup_cohorts_2025.csv", "active_days_total to retained_m6_users", "Sums of the metrics over those accounts"),
    ("signup_cohorts_2025.csv", "refreshed_at", "Date the row was computed; a row refreshed later replaces the earlier one"),
    ("onboarding_calendar_2027q1.csv", "platforms", "all, ios or android"),
    ("onboarding_calendar_2027q1.csv", "start_date", "First enrolment day"),
    ("onboarding_calendar_2027q1.csv", "end_date", "Last enrolment day"),
    ("onboarding_calendar_2027q1.csv", "arms", "Number of arms, control included"),
    ("new_user_forecast_2027.csv", "date", "Calendar day"),
    ("new_user_forecast_2027.csv", "iso_week", "ISO week of the day"),
    ("new_user_forecast_2027.csv", "new_consumer_users_forecast", "The forecasting tool's new consumer user forecast for the platform"),
    ("app_store_ratings_2024_2026.csv", "week_starting", "Monday of the week"),
    ("app_store_ratings_2024_2026.csv", "average_rating", "Average of the week's new ratings, 1 to 5 stars"),
]


def write_dictionary(path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["file", "column", "description"])
        w.writerows(DICTIONARY)


# ---------------------------------------------------------------------------------------------- the spend book
def write_spend(path, rows):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    wb = Workbook()
    sh = wb.active
    sh.title = "Spend 2026"
    sh.append(["Month", "Channel", "Spend (EUR)", "Installs attributed", "Cost per install (EUR)"])
    for m, c, s, i in rows:
        sh.append([m, c, s, i, None])
        r = sh.max_row
        sh.cell(r, 5).value = "=C%d/D%d" % (r, r)
        sh.cell(r, 1).number_format = "mmm yyyy"
        sh.cell(r, 3).number_format = "#,##0.00"
        sh.cell(r, 4).number_format = "#,##0"
        sh.cell(r, 5).number_format = "0.00"
    for c in "ABCDE":
        sh.column_dimensions[c].width = {"A": 11, "B": 26, "C": 14, "D": 19, "E": 22}[c]
    for cell in sh[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="0F6B4F")
    sh.freeze_panes = "A2"
    n = wb.create_sheet("Notes")
    n.append(["Paid acquisition spend by channel, January to September 2026, from the marketing finance ledger."])
    n.append(["Installs attributed: the attribution partner's last-click installs; organic installs are not shown."])
    n.column_dimensions["A"].width = 100
    wb.save(path)
