"""The pack's documents: the readiness standard (PDF), the load test plan (DOCX), the endpoint register and the status
page's incident register (XLSX), the developer portal's changelog (HTML), the synthetic checks (YAML) and the pack's
contents."""
from __future__ import annotations

import datetime as dt
import html

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import letter                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import inch                                                # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import asks as A     # noqa: E402
import common as K   # noqa: E402
import world as W    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
INK, GREY, RULE = colors.HexColor("#1c2329"), colors.HexColor("#5a646d"), colors.HexColor("#b9c1c8")
NAVY = colors.HexColor("#203a5c")

TEAMS = {"payroll-core": "Payroll Core", "tax-forms": "Tax and Filings", "filings": "Tax and Filings",
         "reports": "Reporting", "employees": "Workforce", "time-entries": "Workforce", "pay-stubs": "Payroll Core",
         "deductions": "Payroll Core", "banking": "Money Movement", "companies": "Platform Services",
         "auth": "Platform Services", "search": "Platform Services", "documents": "Reporting",
         "webhooks": "Integrations", "accounting-sync": "Integrations", "state-local": "Tax and Filings"}


def styles():
    body = ParagraphStyle("b", fontName="Sans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName="Sans-B", fontSize=14.5, leading=18, textColor=NAVY, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName="Sans-B", fontSize=10.4, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName="Sans", fontSize=8.3, leading=11.2, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=8.2, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=8.2, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=26, firstLineIndent=-26))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.4)
        canvas.drawString(.8 * inch, letter[1] - .5 * inch, left)
        canvas.drawRightString(letter[0] - .8 * inch, letter[1] - .5 * inch, right)
        canvas.drawRightString(letter[0] - .8 * inch, .45 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


# ------------------------------------------------------------------------------------------------ the standard
def write_standard(path):
    S = styles()
    title = "Public API Year-End Readiness Standard"
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=.85 * inch, rightMargin=.85 * inch, topMargin=.8 * inch,
                            bottomMargin=.75 * inch, title=title, author=K.OWNER, subject="", creator="", producer="")
    st = [Paragraph(title, S["h1"]),
          Paragraph("%s &nbsp;|&nbsp; Platform Engineering &nbsp;|&nbsp; Owner: %s, Vice President, Platform "
                    "Engineering &nbsp;|&nbsp; Approved 8 September 2026 &nbsp;|&nbsp; Applies from the 2026 review"
                    % (K.COMPANY, K.OWNER), S["meta"]),
          Paragraph("1. Purpose and scope", S["h2"]),
          _clause(S, "1.1", "Every January the platform carries the heaviest load of its year. Employers run the last "
                            "payrolls of the old year and the first of the new, correct the year's records and send "
                            "their employees' wage statements, and the year's W-2 and 1099-NEC filings fall due on "
                            "31 January. This standard sets the response time every public API endpoint must deliver "
                            "at that peak and how its readiness is shown before the year's code freeze."),
          _clause(S, "1.2", "The public API's endpoints are those in the endpoint register. Its traffic comes from the "
                            "payroll integrations of about 5,000 employers and of the accounting firms that act for "
                            "them: thousands of clients, each working to its own schedule."),
          _clause(S, "1.3", "The review runs each November. Its outcome is the freeze list, the endpoints the platform "
                            "teams fix before the code freeze, which for the 2027 peak falls on 4 December 2026."),
          Paragraph("2. The response-time objective", S["h2"]),
          _clause(S, "2.1", "At its forecast peak-hour volume, at least 99 percent of the requests customers send an "
                            "endpoint receive their complete response within 800 milliseconds of reaching the edge."),
          _clause(S, "2.2", "A request's response time runs from the moment it reaches the edge to the moment the last "
                            "byte of its response leaves the edge, whatever the request meets on the way: the "
                            "service's own work, a wait for a connection or a database, or a pause of the service's "
                            "runtime."),
          _clause(S, "2.3", "An endpoint that does not meet 2.1 goes on the freeze list. The test is applied to the "
                            "unrounded figure."),
          Paragraph("3. Evidence", S["h2"]),
          _clause(S, "3.1", "Each endpoint is load tested in November in the performance cluster, which runs the "
                            "production build of every service with its production configuration: the same number of "
                            "pods, the same runtime, garbage collector and heap. Each endpoint's test runs at no less "
                            "than its provisional forecast peak-hour volume, one endpoint at a time, and every pod's "
                            "garbage-collection log is kept."),
          _clause(S, "3.2", "An endpoint's run of record is its last complete run of the campaign. A run's first three "
                            "minutes warm the services and do not count; the ten minutes after them are its "
                            "measurement. A run stopped before its measurement ended is not complete."),
          _clause(S, "3.3", "The run of record stands for the endpoint at its forecast peak hour. A run at or above "
                            "the forecast peak-hour volume is evidence for that volume: no allowance is made for the "
                            "difference between the two."),
          Paragraph("4. The forecast peak-hour volume", S["h2"]),
          _clause(S, "4.1", "An endpoint's forecast peak-hour volume for January of the coming year is the number of "
                            "requests the endpoint served customers in its busiest clock hour of January of the review "
                            "year, as the edge counted them, multiplied by its growth factor."),
          _clause(S, "4.2", "An endpoint's growth factor is the number of employers whose plan includes the endpoint on "
                            "1 November of the review year divided by the number on 1 January of the review year. An "
                            "employer counts on a day when its subscription covers that day. The endpoint register "
                            "lists the plans that include each endpoint."),
          _clause(S, "4.3", "The load tests are sized from the provisional forecast of the September planning round; "
                            "capacity planning recomputes every forecast for the review."),
          Paragraph("5. Service credits", S["h2"]),
          _clause(S, "5.1", "When an endpoint breaches its availability or response-time commitment, each customer "
                            "the incident affected earns a service credit under its plan's service schedule."),
          _clause(S, "5.2", "The readiness workbook shows, beside each endpoint's verdict, the service credits "
                            "customers were issued for the endpoint's breaches from 1 January to 31 October of the "
                            "review year, net of reversals."),
          Paragraph("6. The review", S["h2"]),
          _clause(S, "6.1", "Capacity planning prepares the readiness workbook: every endpoint's verdict under 2.1 with "
                            "its forecast peak-hour volume and its service credits, and the freeze list. The vice "
                            "president of platform engineering signs the workbook off before the code freeze."),
          _clause(S, "6.2", "The owning team fixes each endpoint on the freeze list before the freeze and shows the fix "
                            "with a new run in the performance cluster."),
          Paragraph("7. Terms", S["h2"])]
    rows = [["Term", "Meaning"],
            ["Customer", "An employer or an accounting firm that uses the public API under its plan."],
            ["Edge", "The API gateway at %s; in the performance cluster, %s." % (K.EDGE_HOST, K.PERF_EDGE)],
            ["Clock hour", "An hour that begins on the hour."],
            ["Endpoint register", "Platform Engineering's register of the public API's endpoints and the services that "
                                  "run them."],
            ["Code freeze", "The date after which no change reaches production before the peak except an emergency "
                            "fix."]]
    st.append(_table(S, rows, [1.5, 5.2]))
    st.append(Spacer(1, 8))
    st.append(Paragraph("Questions on this standard go to %s, Capacity Planning." % K.REQUESTER, S["meta"]))
    fr = _frame("%s | Platform Engineering" % K.COMPANY, "Public API Year-End Readiness Standard, 2026 edition")
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ the test plan
def write_plan(path, w):
    import docx
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, RGBColor

    d = docx.Document()
    normal = d.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)

    def para(text, bold_lead=None, size=None, after=6, color=None, italic=False):
        p = d.add_paragraph()
        if bold_lead:
            a = p.add_run(bold_lead + " ")
            a.bold = True
        r = p.add_run(text)
        r.italic = italic
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        p.paragraph_format.space_after = Pt(after)
        return p

    def heading(text):
        p = d.add_paragraph()
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(11.5)
        r.font.color.rgb = RGBColor.from_string("203A5C")
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)

    def table(rows, widths=None, right=()):
        tb = d.add_table(rows=len(rows), cols=len(rows[0]))
        tb.style = "Light List Accent 1"
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                cell = tb.cell(i, j)
                cell.text = str(v)
                for p in cell.paragraphs:
                    p.paragraph_format.space_after = Pt(0)
                    if j in right and i > 0:
                        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    for r in p.runs:
                        r.font.size = Pt(9)
                        if i == 0:
                            r.bold = True
        d.add_paragraph().paragraph_format.space_after = Pt(2)

    t = d.add_paragraph()
    r = t.add_run("Year-End Peak Load Test Plan, November 2026")
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor.from_string("203A5C")
    for k, v in (("Owner", "Performance Engineering"), ("Version", "1.4, campaign log added 19 November 2026"),
                 ("Build under test", K.BUILD), ("Environment", "Performance cluster, namespace perf"),
                 ("Results to", "%s, Capacity Planning" % K.REQUESTER)):
        p = d.add_paragraph()
        a = p.add_run(k + ": ")
        a.bold = True
        p.add_run(v)
        p.paragraph_format.space_after = Pt(0)
    d.add_paragraph()

    heading("1. Purpose")
    para("Each public API endpoint is load tested at no less than its provisional forecast peak-hour volume from the "
         "September planning round, on the production build in the performance cluster, as section 3 of the Public API "
         "Year-End Readiness Standard requires. Capacity Planning assesses each endpoint on its run of record and files "
         "the verdicts in the readiness workbook.")
    heading("2. Workload")
    para("Each endpoint's test is a closed workload with a fixed number of client threads (JMeter) or virtual users "
         "(k6). Each thread sends a request, waits for its response, sleeps for the endpoint's pacing time and then "
         "sends its next request. Table 1 gives each endpoint's threads and pacing, set in October so that every "
         "endpoint's throughput clears its provisional forecast.")
    rows = [["Code", "Route", "Tool", "Threads or VUs", "Pacing (ms)"]]
    for c in K.CODES:
        rows.append([c, K.PATH[c], "JMeter" if w["sched"][c]["tool"] == "jmeter" else "k6", w["eps"][c]["threads"],
                     int(round(w["eps"][c]["think"] * 1000.0))])
    para("Table 1. Threads and pacing", italic=True, after=2)
    table(rows, right=(3, 4))
    heading("3. Environment")
    para("The performance cluster runs each service with its production pod count, JVM options and garbage collector "
         "(the endpoint register's Services sheet). The load generators sit in the edge's own zone and call each "
         "endpoint through the performance edge, %s, which hands each new request to the service's next pod in turn and "
         "adds an X-Served-By header naming the pod that served it. Client timeout is 30 seconds. Test data is the perf "
         "tenant's 2,400 test employers." % K.PERF_EDGE)
    heading("4. Runs")
    para("A run lasts 13 minutes: 3 minutes of warm-up, then 10 minutes of measurement (readiness standard 3.2). "
         "Endpoints run one at a time, at least 15 minutes apart. A run stopped early is repeated the same day.")
    heading("5. Tools and schedule")
    para("Runs from 10 to 12 November use JMeter 5.6.3. The team moved its scripts to k6 0.54 on 13 November, and runs "
         "from 16 November use k6.")
    days = {}
    for c in K.CODES:
        s = w["sched"][c]
        days.setdefault(s["start"].date(), []).append((s.get("aborted_start", s["start"]), c, s["tool"]))
    rows = [["Day", "Tool", "Endpoints, in running order"]]
    for day in sorted(days):
        lst = sorted(days[day])
        rows.append([day.strftime("%a %d %b"), "JMeter" if lst[0][2] == "jmeter" else "k6",
                     ", ".join(c for _, c, _ in lst)])
    para("Table 2. Schedule (each day's first run from 14:00 UTC)", italic=True, after=2)
    table(rows)
    heading("6. Results and logs")
    para("JMeter writes a JTL results file, CSV with a header row: one row per sample, written when the sample "
         "completes. jmeter.properties sets sampleresult.timestamp.start=true, so timeStamp is the sample's start in "
         "epoch milliseconds; elapsed is its response time in milliseconds; label is the endpoint's code and route; "
         "threadName is the thread group and thread; servedBy is the X-Served-By header.", bold_lead="JMeter.")
    para("k6 writes its metrics to CSV. The campaign kept the http_req_duration metric only, one row per request, with "
         "K6_CSV_TIME_FORMAT=rfc3339_nano: timestamp is when the response completed (UTC) and metric_value is its "
         "response time in milliseconds; extra_tags carries the virtual user (vu), the pod that served the request "
         "(served_by) and the endpoint's code.", bold_lead="k6.")
    para("Every pod logs its collector's events with -Xlog:gc. The log platform's export covers each run and five "
         "minutes either side, and prefixes each line with the time the platform ingested it (UTC) and the pod's name. "
         "The JVM writes a pause's line when the pause ends, with its duration. Services on the 2026.11 base image "
         "decorate each line with wall-clock time (Eastern, UTC-05:00); tax-forms, banking and accounting-sync still "
         "run on the 2025.04 base image, whose lines carry the JVM's uptime in seconds instead.",
         bold_lead="Garbage-collection logs.")
    para("The cluster's events for the perf namespace, with each service's own start-up line, which gives how long its "
         "process had been running.", bold_lead="Pod events.")
    heading("7. Campaign log")
    pods = w["pods"]
    rows = [["When (UTC)", "What happened"],
            ["Mon 9 Nov 19:12", "Build %s deployed to the performance cluster, every service." % K.BUILD]]
    rows.append(["Fri 13 Nov 03:41", "Pod %s restarted (node maintenance)." % pods["tax-forms"][1]])
    rows.append(["Sat 14 Nov 22:05", "Pod %s restarted (node drain)." % pods["banking"][0]])
    for c in sorted(W.ABORTED, key=lambda x: w["sched"][x]["aborted_start"]):
        s = w["sched"][c]
        why = "a client host lost its connection" if c == "EP13" else "the performance edge rotated its certificate"
        sec = int(W.ABORTED[c])
        rows.append([s["aborted_start"].strftime("%a %d %b %H:%M"),
                     "%s first run stopped after %d min %02d s (%s); repeated at %s." % (
                         c, sec // 60, sec % 60, why, s["start"].strftime("%H:%M"))])
    rows.append(["Thu 19 Nov 16:20", "Campaign complete: every endpoint has a complete run."])
    table(rows)
    heading("8. Pass criterion")
    para("Readiness standard 2.1, assessed by Capacity Planning on each endpoint's run of record.")
    d.core_properties.author = "Performance Engineering"
    d.core_properties.title = "Year-End Peak Load Test Plan, November 2026"
    d.save(path)


# ------------------------------------------------------------------------------------------------ the register
def write_register(path, seed):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill

    import records as R
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Endpoints"
    head = ["Code", "Method", "Route", "Service", "Plans", "Owner team", "Status"]
    ws.append(head)
    for c in K.CODES:
        m, p = K.PATH[c].split(" ", 1)
        ws.append([c, m, p, K.SERVICE[c], ", ".join(A.ENDPOINT_PLANS[c]), TEAMS[K.SERVICE[c]], "Live"])
    ws2 = wb.create_sheet("Services")
    ws2.append(["Service", "Collector", "JVM options", "Pods (production)", "Pods (perf)", "Base image", "Runtime"])
    flag = {"parallel": "-XX:+UseParallelGC", "g1": "-XX:+UseG1GC", "zgc": "-XX:+UseZGC"}
    for svc, (gc, n) in K.SERVICES.items():
        mb = R.heap_mb(seed, svc)
        xmx = "-Xmx%dg" % (mb // 1024) if mb % 1024 == 0 else "-Xmx%dm" % mb
        old = svc in W.UPTIME_SERVICES
        logopt = "-Xlog:gc" if old else "-Xlog:gc:stdout:time,level,tags"
        if gc == "zgc":
            logopt = "-Xlog:gc,gc+phases:stdout:time,level,tags"
        ws2.append([svc, {"parallel": "Parallel", "g1": "G1", "zgc": "ZGC"}[gc],
                    "%s -Xms%s %s %s" % (flag[gc], xmx[5:], xmx, logopt), n, n, "2025.04" if old else "2026.11",
                    "Temurin 17.0.12" if old else "Temurin 21.0.5"])
    ws3 = wb.create_sheet("Plans")
    ws3.append(["Plan", "Public API", "Notes"])
    for pl, note in (("Starter", "Payroll runs, employees, pay stubs, direct deposits, tax forms, companies, "
                                 "authentication"),
                     ("Standard", "Starter, plus filings, approvals, time entries, deductions, local taxes"),
                     ("Professional", "Standard, plus reports, garnishments, search, documents, accounting sync, state "
                                      "filings"),
                     ("Enterprise", "Professional, plus webhooks")):
        ws3.append([pl, "Yes", note])
    for sh in (ws, ws2, ws3):
        for cell in sh[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="203A5C")
            cell.alignment = Alignment(vertical="center")
        sh.freeze_panes = "A2"
        for col in sh.columns:
            width = max(len(str(c.value)) if c.value is not None else 0 for c in col)
            sh.column_dimensions[col[0].column_letter].width = min(64, max(9, width + 2))
    wb.save(path)


# ------------------------------------------------------------------------------------------------ incidents
def write_incidents(path, inc):
    import openpyxl
    from openpyxl.styles import Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Incidents"
    ws.append(["Incident", "Started (UTC)", "Resolved (UTC)", "Severity", "Component", "Title"])
    what = {"latency": "Elevated response times on %s", "errors": "Errors on %s", "unavailable": "%s unavailable"}
    for x in inc:
        end = x["start"] + dt.timedelta(minutes=x["minutes"])
        ws.append([x["key"], x["start"], end, x["sev"], x["comp"], what[x["kind"]] % x["comp"]])
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="3B4F63")
    for row in ws.iter_rows(min_row=2):
        row[1].number_format = "yyyy-mm-dd hh:mm:ss"
        row[2].number_format = "yyyy-mm-dd hh:mm:ss"
    ws.freeze_panes = "A2"
    for col, wd in zip("ABCDEF", (16, 20, 20, 10, 34, 52)):
        ws.column_dimensions[col].width = wd
    ws.auto_filter.ref = "A1:F%d" % ws.max_row
    wb.save(path)


# ------------------------------------------------------------------------------------------------ changelog
CHANGES = [
    (dt.date(2026, 11, 2), "Year-end: W-2 preview fields",
     "GET /v2/tax-forms/w2 returns the preview fields boxes 12a to 12d and box 14 for forms not yet filed."),
    (dt.date(2026, 9, 15), "Webhooks: retry schedule",
     "Failed webhook deliveries are retried five times over 24 hours instead of three times over 6 hours."),
    (dt.date(2026, 6, 22), "Search: filter by document type",
     "GET /v2/search accepts type=w2, type=1099-nec and type=pay-stub."),
    (dt.date(2026, 4, 7), "Accounting sync: QuickBooks Online class mapping",
     "POST /v2/accounting-sync/exports accepts a class_map for QuickBooks Online exports."),
    (dt.date(2026, 3, 10), "Tax liability report: quarter totals",
     "GET /v2/reports/tax-liability adds quarter_totals to its response."),
    (dt.date(2026, 2, 3), "Garnishments: state-specific orders",
     "POST /v2/garnishments accepts order_state and the state's own order reference."),
    (dt.date(2026, 1, 21), "Search moves to v2",
     "GET /v1/search is now GET /v2/search, with the same parameters and cursor-based pagination. From 10:00 ET on "
     "21 January 2026 requests to /v1/search receive a permanent redirect (308) to /v2/search; the old path stops "
     "answering on 31 March 2026."),
    (dt.date(2026, 1, 19), "Employee list moves to v2",
     "GET /v1/employees is now GET /v2/employees, with the same response and cursor-based pagination. From 10:00 ET "
     "on 19 January 2026 requests to /v1/employees receive a permanent redirect (308) to /v2/employees; the old path "
     "stops answering on 31 March 2026."),
    (dt.date(2026, 1, 14), "Local tax rates: new path",
     "GET /v2/tax-rates/local is now GET /v2/local-taxes. From 10:00 ET on 14 January 2026 the old path answers with "
     "a permanent redirect (308) to the new one; it stops answering on 28 February 2026."),
    (dt.date(2026, 1, 5), "Rate limits for the year-end peak",
     "From 5 January to 13 February 2026 the per-client limit on GET /v2/tax-forms/w2 and GET /v2/tax-forms/1099-nec "
     "rises from 20 to 40 requests a second."),
]


def write_changelog(path):
    items = []
    for day, title, body in CHANGES:
        items.append('    <article class="entry" id="%s">\n      <time datetime="%s">%s</time>\n      <h2>%s</h2>\n'
                     '      <p>%s</p>\n    </article>' % (day.isoformat(), day.isoformat(),
                                                         day.strftime("%B %d, %Y").replace(" 0", " "),
                                                         html.escape(title), html.escape(body)))
    page = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>API changelog 2026 | Mirrendale Developer Portal</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; color: #1c2329; margin: 0; }
    header { background: #203a5c; color: #fff; padding: 18px 32px; }
    main { max-width: 820px; margin: 24px auto; padding: 0 24px; }
    .entry { border-bottom: 1px solid #d9dee3; padding: 14px 0; }
    time { color: #5a646d; font-size: 0.85em; }
    h2 { font-size: 1.1em; margin: 4px 0 6px; }
  </style>
</head>
<body>
  <header>Mirrendale Developer Portal &middot; Public API &middot; Changelog</header>
  <main>
    <h1>API changelog, 2026</h1>
%s
  </main>
</body>
</html>
""" % "\n".join(items)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(page)


# ------------------------------------------------------------------------------------------------ synthetic checks
def write_synthetic(path):
    """The monitoring repository's monitor definitions, as Site Reliability keeps them (keys equal to the defaults
    are left out)."""
    dflt_every, dflt_locs = 300, A.LOC2
    out = ["# Uptime monitors for the public API, run against the production edge (%s)." % K.EDGE_HOST,
           "# Owned by Site Reliability. Each run of a monitor sends its steps in order, once from each of its",
           "# locations, as the monitoring tenant's integration. Path parameters come from the previous step's response.",
           "version: 3", "defaults:", "  frequency_seconds: %d" % dflt_every,
           "  locations: [%s]" % ", ".join(dflt_locs), "  tenant: monitor-employer-0001", "  timeout_seconds: 10",
           "  retries: 0", "monitors:"]
    for name, every, locs, steps, created in A.SYNTH_CHECKS:
        out.append("  - name: %s" % name)
        out.append("    created: %s" % created.isoformat())
        if every != dflt_every:
            out.append("    frequency_seconds: %d" % every)
        if locs != dflt_locs:
            out.append("    locations: [%s]" % ", ".join(locs))
        out.append("    steps:")
        for c in steps:
            extra = ""
            if c == "EP01":
                extra = "  # dry_run=true"
            elif c == "EP16":
                extra = "  # validate_only=true"
            out.append("      - %s%s" % (K.PATH[c], extra))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")


# ------------------------------------------------------------------------------------------------ contents
def write_contents(path, items):
    out = ["%s, year-end readiness review 2027: contents of the review pack" % K.COMPANY,
           "Assembled %s by Capacity Planning." % K.ASSEMBLED.strftime("%d %B %Y").lstrip("0"), ""]
    for name, desc in items:
        out.append(name)
        out.append("    " + desc)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
