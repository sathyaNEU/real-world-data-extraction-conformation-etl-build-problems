"""task464 architecture 12: the documents and small tables under target/.

The 2027 jobseeker email plan (the governing document, Word), the restart pilot's design brief (PDF), the CRM send
calendar and finance's sponsored revenue by sector (Excel), the CRM's mailbox domain groups and the June alerts
survey (CSV). Each is written in the voice of the team that owns it; none describes the data files.
"""
import csv
import datetime as dt
import os
import re

import numpy as np
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

PIN = ("Every email programme is judged on the sponsored clicks Quaywork takes with it against what it would have taken "
       "without it, counted as the click system records them for billing. For the restart series those clicks are "
       "counted over the 28 days from each pilot send, the six sends as they ran, and the 2027 series is sized at what "
       "one pilot send did on average, thirteen times. The series stays in the plan if it adds sponsored clicks.")
PLAN_NAME = "jobseeker_email_plan_2027.docx"
BRIEF_NAME = "restart_pilot_brief_2026.pdf"


def plan(tgt):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    t = d.add_paragraph()
    r = t.add_run("Jobseeker email plan 2027")
    r.bold = True
    r.font.size = Pt(16)
    d.add_paragraph("Jobseeker Engagement | draft for the leadership team, meeting of 7 December 2026 | "
                    "%s, 16 November 2026" % W.PEOPLE["head"])
    d.add_heading("1. What this plan covers", level=2)
    d.add_paragraph("The daily job alerts and the weekly digest Quaywork sends to jobseekers in 2027, and the restart "
                    "series piloted in 2026. Employer-facing email and the recruiter newsletter are in the sales plan. "
                    "Budgets are at 2026 prices; Postvane's contract runs to March 2028.")
    d.add_heading("2. Daily job alerts and the weekly digest", level=2)
    d.add_paragraph("A jobseeker gets one alert a day for each saved search, sent from 06:00, listing the new jobs that "
                    "match it; sponsored jobs are marked and sit with the others. The weekly digest goes on Sunday "
                    "mornings to everyone with an account and email consent. Alerts pause when a jobseeker has not "
                    "clicked a job on Quaywork for 90 days; a paused jobseeker can restart them from the site, the app "
                    "or a restart email, and a restart turns every paused saved search back on.")
    d.add_paragraph("No change is proposed to either in 2027 beyond the template refresh already scheduled for March.")
    d.add_heading("3. The restart series", level=2)
    d.add_paragraph("The restart email (\"Still looking? Restart your job alerts\") asks a paused jobseeker to turn "
                    "their alerts back on with one click, and links to the newest jobs near them in six sectors. We "
                    "piloted it in 2026 on the jobseekers whose alerts were paused on 1 April: a random tenth of them, chosen by "
                    "account, was held out and never sent it, and the rest were sent it every four weeks from 14 April "
                    "until they restarted, six sends in all. The design is in the pilot brief of 10 March 2026.")
    d.add_heading("4. The series in 2027", level=2)
    d.add_paragraph("If it stays, the series runs as a standing programme: the same email every four weeks from "
                    "12 January 2027, thirteen sends in the year, each to the jobseekers whose alerts are paused on "
                    "the day it goes, with no holdout. The send dates follow.")
    sd = [dt.date(2027, 1, 12) + dt.timedelta(days=28 * i) for i in range(13)]
    tb = d.add_table(rows=1, cols=4)
    tb.style = "Light Grid Accent 1"
    hdr = tb.rows[0].cells
    for c, h in zip(hdr, ["Send", "Date", "Send", "Date"]):
        c.text = h
    for i in range(7):
        row = tb.add_row().cells
        row[0].text = "RS-27%02d" % (i + 1)
        row[1].text = sd[i].strftime("%d %b %Y")
        if i + 7 < 13:
            row[2].text = "RS-27%02d" % (i + 8)
            row[3].text = sd[i + 7].strftime("%d %b %Y")
    d.add_heading("5. How the programmes are judged", level=2)
    d.add_paragraph(PIN)
    d.add_heading("6. Budget and decisions needed", level=2)
    d.add_paragraph("Postvane bills restart sends at the contract rate for marketing email; the creative and the "
                    "landing page exist. The leadership team is asked on 7 December 2026 whether the restart series "
                    "stays in the 2027 plan. If it does not, paused jobseekers keep the site and app routes to "
                    "restart, and the rest of this plan is unchanged.")
    d.add_heading("7. Owner", level=2)
    d.add_paragraph("%s (Head of Jobseeker Engagement). Analysis: %s (CRM Analyst). Finance: %s."
                    % (W.PEOPLE["head"], W.PEOPLE["analyst"], W.PEOPLE["cfo"]))
    cp = d.core_properties
    cp.author = W.PEOPLE["head"]
    cp.last_modified_by = W.PEOPLE["head"]
    cp.title = "Jobseeker email plan 2027"
    cp.created = dt.datetime(2026, 11, 16, 9, 12, 0)
    cp.modified = dt.datetime(2026, 11, 16, 16, 48, 0)
    cp.revision = 7
    d.save(os.path.join(tgt, PLAN_NAME))


def brief(tgt):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13)
    h = ParagraphStyle("h", parent=ss["Heading3"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=3)
    tt = ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=15, alignment=0)
    doc = SimpleDocTemplate(os.path.join(tgt, BRIEF_NAME), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm, title="Restart pilot brief",
                            author=W.PEOPLE["analyst"], creator="Microsoft Word", subject="")
    s = [Paragraph("Restart pilot: design brief", tt),
         Paragraph("CRM team, Quaywork. %s, 10 March 2026. Approved by %s, 16 March 2026."
                   % (W.PEOPLE["analyst"], W.PEOPLE["head"]), body), Spacer(1, 6)]
    s.append(Paragraph("Why", h))
    s.append(Paragraph("Since alerts began pausing after 90 days without a click, paused jobseekers have only come back "
                       "by finding the restart button on the site or in the app. We want to know whether asking them "
                       "by email brings them back to the alerts, and whether it is worth running as a standing "
                       "programme.", body))
    s.append(Paragraph("Who", h))
    s.append(Paragraph("Every jobseeker whose alerts are paused at the start of 1 April 2026 and who has email consent. "
                       "Each is placed in an arm by the last digit of a hash of the account number: one digit in ten "
                       "goes to the holdout, which is never sent the restart email; the other nine are mailed. Nobody "
                       "joins the pool after 1 April, and nobody changes arm.", body))
    s.append(Paragraph("What they get", h))
    s.append(Paragraph("The restart email every four weeks, sent at 10:00 on the six dates below, until the jobseeker "
                       "restarts their alerts (by any route) or unsubscribes. A jobseeker whose alerts pause again "
                       "rejoins the mailing at the next send. The email carries one button, \"Restart my alerts\", "
                       "that restarts every paused saved search in one click with no login, links to the newest jobs "
                       "near them in six sectors (care, driving, warehouse, retail, admin, hospitality), and the usual "
                       "footer links (manage alerts, privacy, help, unsubscribe). Both arms can restart from the site "
                       "or the app at any time, as now.", body))
    rows = [["Send", "Code", "Date", "Time"]] + [["%d" % (k + 1), "RS-26%02d" % (4 + k), d.strftime("%a %d %b %Y"), "10:00"]
                                               for k, d in enumerate(W.SENDS)]
    tb = Table(rows, colWidths=[18 * mm, 28 * mm, 40 * mm, 18 * mm])
    tb.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 9), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
                            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke)]))
    s += [Spacer(1, 4), tb]
    s.append(Paragraph("What we will measure", h))
    s.append(Paragraph("Restarts from the alert system's log, and sponsored clicks from the warehouse, the same way "
                       "everyone else's are reported. Postvane reports each send as it does any campaign. Results go "
                       "to the leadership team with the 2027 email plan.", body))
    s.append(Paragraph("Risks", h))
    s.append(Paragraph("Some addresses will bounce on the first send; Postvane suppresses a hard bounce automatically. Some jobseekers will have found work and will "
                       "unsubscribe. Customer Support has the email and a short script.", body))
    doc.build(s)


def calendar(tgt):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sends 2026"
    head = ["Campaign code", "Campaign", "Audience", "Send date", "Send time (UK)", "Subject line"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE7F0")
    ws.append(["JA-DAILY", "Job alerts", "jobseekers with alerts running", "daily", "06:00",
               "{n} new jobs for {search}"])
    ws.append(["JA-DIGEST", "Weekly digest", "all jobseekers with email consent", "Sundays", "08:00",
               "This week on Quaywork"])
    for k, d in enumerate(W.SENDS):
        ws.append(["RS-26%02d" % (4 + k), "Restart series pilot, send %d" % (k + 1),
                   "restart pilot, mailed arm, alerts paused", d, "10:00", "Still looking? Restart your job alerts"])
    ws.append(["SU-2611", "Salary survey invitation", "jobseekers active in the last 30 days", dt.date(2026, 11, 10),
               "11:00", "Tell us what you earn, see what others do"])
    for row in ws.iter_rows(min_row=2):
        if isinstance(row[3].value, dt.date):
            row[3].number_format = "dd/mm/yyyy"
    for col, w in zip("ABCDEF", [15, 32, 40, 13, 15, 44]):
        ws.column_dimensions[col].width = w
    wb.save(os.path.join(tgt, "crm_send_calendar_2026.xlsx"))


def domain_groups(tgt):
    from pack import WH_GROUP, SL_GROUP, PB_ISP
    rows = []
    for i, p in enumerate(W.PROVIDERS):
        for dom in W.DOMAINS[p]:
            rows.append([dom, WH_GROUP[i], SL_GROUP[i], PB_ISP[i]])
    rows.append(["(any other domain)", "other", "Other", "OTHER"])
    with open(os.path.join(tgt, "crm_mailbox_domain_groups.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["email_domain", "warehouse_group", "postvane_group", "inkrelay_isp"])
        w.writerows(rows)


SECTORS = ["Healthcare and nursing", "Warehouse and logistics", "Retail", "Hospitality and catering",
           "Construction and trades", "Teaching and education", "IT and software", "Accounting and finance",
           "Engineering", "Admin and office", "Customer service", "Social care", "Driving and transport", "Other"]


def revenue(tgt, h):
    """Finance's month-end view of sponsored clicks and revenue by job sector, January to October 2026."""
    rng = np.random.default_rng(W.SEED + 11)
    days, a, pool = h["days"], h["active"], h["pool"]
    c = pool["clicks"]
    pool_by_day = np.bincount(c["t"], minlength=len(days))
    monthly = {}
    for t, d in enumerate(days):
        if d.year != 2026 or d.month > 10:
            continue
        v = int(a["alert"][t].sum() + a["website"][t].sum() + a["app"][t].sum() + pool_by_day[t])
        monthly[d.month] = monthly.get(d.month, 0) + v
    share = rng.dirichlet(np.ones(len(SECTORS)) * 6)
    cpc = rng.uniform(0.32, 1.45, size=len(SECTORS))
    wb = Workbook()
    ws = wb.active
    ws.title = "Sponsored by sector"
    ws.append(["Quaywork Ltd: sponsored jobs, month-end view (Finance)", "", "", "", ""])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Month", "Sector", "Sponsored clicks", "Revenue (GBP)", "Average CPC (GBP)"])
    for cell in ws[2]:
        cell.font = Font(bold=True)
    for mth in sorted(monthly):
        tot = monthly[mth]
        alloc = np.floor(share * tot * rng.uniform(0.96, 1.04, size=len(SECTORS))).astype(int)
        alloc[-1] = tot - alloc[:-1].sum()
        for i, s in enumerate(SECTORS):
            rate = round(float(cpc[i] * rng.uniform(0.97, 1.03)), 2)
            ws.append([dt.date(2026, mth, 1), s, int(alloc[i]), round(alloc[i] * rate, 2), rate])
    for row in ws.iter_rows(min_row=3):
        row[0].number_format = "mmm yyyy"
        row[3].number_format = "#,##0.00"
    for col, wdt in zip("ABCDE", [12, 28, 17, 16, 18]):
        ws.column_dimensions[col].width = wdt
    wb.save(os.path.join(tgt, "sponsored_revenue_by_sector_2026.xlsx"))


REASONS = ["I found a job", "Too many emails", "The jobs were not relevant", "I moved area", "Taking a break",
           "Other"]
# the original fixed answers decide only which respondents left the comment box empty (the same draws as before)
COMMENTS = {
    "I found a job": ["a", "a", "a", "a", "a", ""],
    "Too many emails": ["a", "a", "a", "a", "a", ""],
    "The jobs were not relevant": ["a", "a", "a", "a", "a", ""],
    "I moved area": ["a", "a", "a", ""],
    "Taking a break": ["a", "a", "a", ""],
    "Other": ["a", "a", "a", "", "a"],
}
# What respondents wrote, in their own words. A comment is a short answer, an elaboration, or both; every
# elaboration is used at most twice and no comment repeats verbatim more than twice (checks.py asserts both).
HEADS = {
    "I found a job": [
        "got a job", "found a job", "Got a job!", "new job", "I have a job now", "I've got a job", "found work",
        "employed now", "back in work", "working now", "in work now", "got one", "job found", "got work",
        "Got a new job", "started a new job", "I'm working", "got a full time job", "found a job thank you",
        "no longer looking", "not looking any more", "got sorted", "all sorted thanks", "found something",
        "found employment", "Successful in finding work", "Have found a position", "got a permanent job",
        "Got the job I wanted", "I start next week", "start on monday", "started last week", "got offered a job",
        "accepted an offer", "got a contract", "Employed", "working full time now", "working again",
        "got back into work", "new role", "new position", "found a role", "have work now", "found a new job",
        "got lucky", "finally got a job", "got a job at last", "found work locally", "got a local job",
        "got a job yay", "In employment", "Job sorted", "I'm sorted for work now", "Found a job through you",
        "Got a job elsewhere", "I've been taken on", "Working at last", "Just started a job", "got a part time job",
        "employed again", "got a job, cheers", "doing well now", "got a job a few weeks ago", "new job since spring",
        "I got the job", "result!", "back on my feet with a job", "Have a job",
    ],
    "Too many emails": [
        "too many emails", "too many", "too much", "way too many", "far too many emails", "too many emails sorry",
        "Too frequent", "too often", "too many a day", "Overkill", "it was too much", "a bit much", "email overload",
        "was getting loads", "just too many", "Too many!!", "I was getting too many", "far too much email",
        "constant emails", "never ending", "every single day", "daily is too much", "they never stop", "got fed up",
        "annoying", "I get enough emails", "loads of emails", "they piled up", "overwhelmed", "bombarded",
        "I felt bombarded", "far too frequent", "relentless", "the amount of them", "more than I need",
        "Too many emails to keep up with", "it got a bit much", "excessive", "too regular", "sick of them",
        "Just too many of them", "the volume", "it was daily", "TOO MANY", "too many messages",
    ],
    "The jobs were not relevant": [
        "not relevant", "irrelevant", "wrong jobs", "not relevant to me", "jobs not suitable", "nothing suitable",
        "not what I was looking for", "the wrong kind of jobs", "unsuitable jobs", "jobs didn't match",
        "didn't match my search", "nothing relevant", "not my area", "not for me", "poor matches", "rubbish matches",
        "the matching is poor", "useless suggestions", "irrelevant jobs", "the jobs were rubbish",
        "nothing I could apply for", "nothing I was qualified for", "jobs too far away", "too far", "wrong location",
        "wrong area", "wrong sector", "wrong hours", "pay too low", "low pay", "badly paid jobs", "all agency jobs",
        "mostly agencies", "same old jobs", "not useful", "pointless", "not helpful", "never anything for me",
        "nothing in my field", "no good", "Not suitable", "Poor", "didn't suit",
    ],
    "I moved area": [
        "moved", "moved house", "moved away", "relocated", "new area", "I've moved", "moved area",
        "not local any more", "moving soon", "moved out of the area", "living elsewhere now", "changed address",
        "moved abroad", "emigrated", "moved back home", "House move",
    ],
    "Taking a break": [
        "taking a break", "on a break", "having a break", "not looking right now", "not looking at the moment",
        "on hold", "paused for now", "having time off", "not job hunting for now", "taking time out",
        "having a rest", "break from job hunting", "will come back later", "not ready yet", "need a break",
        "time out", "on leave", "busy with other things", "not for now", "maybe later", "Short break",
    ],
    "Other": [
        "other", "dont know", "not sure", "no reason", "can't remember", "no comment", "none", "n/a", "na",
        "nothing", "just because", "no idea", "personal reasons", "other reasons", "prefer not to say", "it's fine",
        "all good", "no complaints", "just didn't need them", "don't need them", "not needed", "didn't want them",
        "changed my mind", "no longer needed", "don't use them", "?", "Various",
    ],
}
TAILS = {
    "I found a job": [
        "started at the hospital in the laundry", "my cousin got me in where he works",
        "a mate put a word in for me at his place", "through an agency, temp to perm hopefully",
        "the agency found me something on nights", "care work, which is what I wanted",
        "I'm a carer now for the council", "back at my old job, they took me back",
        "my old boss rang and offered me my job back", "doing drops for a parcel firm",
        "driving for a builders merchant", "on the buses now", "got through the training and passed",
        "after about 30 applications", "took 4 months but got there", "after 6 interviews!!",
        "at a nursery 5 mins from home", "in a school kitchen, term time only which suits me",
        "teaching assistant at my son's school", "cleaning at the leisure centre, early mornings",
        "nights in a warehouse, not ideal but it pays", "seasonal at the garden centre for now",
        "at a hotel on reception", "in a care home in my village", "on a building site, labouring",
        "apprenticeship with a plumber", "with the council on the bins", "at the airport in baggage handling",
        "office job finally, admin", "part time in a bakery", "in a pharmacy as a counter assistant",
        "a dental practice took me on as a trainee nurse", "found it in the local paper funnily enough",
        "saw it in a shop window", "walked in and asked, old school", "from a jobs fair at the college",
        "through the job centre in the end", "the job centre put me forward for it", "my uni careers team helped",
        "a recruiter rang me out of the blue", "started 3 weeks ago and loving it",
        "it's only a 6 month contract so may be back", "fixed term till christmas",
        "zero hours but enough shifts for now", "permanent contract at last",
        "full time days, which is what I needed", "better money than my last place",
        "closer to home so no more buses", "can walk to work now", "work from home job, customer service",
        "warehouse picking, 4 on 4 off", "HGV class 2 job with a haulier",
        "forklift driver at a distribution centre", "bar work for now while I study",
        "kitchen porter, hoping to move up to chef", "commis chef in a hotel kitchen",
        "healthcare assistant on a ward", "staff nurse post at the hospital",
        "support worker with adults with learning disabilities", "domiciliary care, own car needed but fine",
        "retail, christmas temp that became permanent", "store supervisor, a step up for me",
        "assistant manager at a charity shop", "payroll job in an accountants",
        "bookkeeping for a small firm, 3 days a week", "trainee estate agent", "lab tech at a food factory",
        "machine operator on days", "packing at a food factory", "a joinery firm took me on",
        "painting and decorating with my uncle", "groundworks for a housebuilder",
        "electrician's mate till I qualify", "gardening for the council parks", "school caretaker",
        "porter at the hospital", "housekeeping at a hotel", "back in a salon doing hair",
        "mechanic at a garage near me", "call centre, it'll do for now", "self employed now doing odd jobs",
        "set up my own cleaning business", "two part time jobs that add up to full time",
        "my partner and I both found work", "got the job on my first interview",
        "they offered it to me on the spot", "offered after a trial shift", "it was one of your adverts actually",
        "applied through your site so thank you", "applied on a different site", "not through here unfortunately",
        "started in the spring", "starting in july", "since the end of april", "start date is the 1st",
        "just waiting on my DBS then I start", "references done, starting soon",
        "still on probation but going well", "passed my probation last week", "the hours suit the school run",
        "nights so I can be home in the day", "weekends only which works with uni",
        "it's minimum wage but it's a start", "pays well and good people", "same firm as before, different site",
        "at a hospice, really rewarding", "receptionist at a vets", "front desk at a solicitors office",
        "farm work for the summer", "with a removals firm", "taxi driving now",
        "bus driver training paid for by the company", "joined the army, basic training in september",
        "back into teaching after a break", "civil service admin job", "library assistant, love it",
        "postman, early starts", "cleaning a school, 3 hours a day", "my neighbour's firm needed a driver",
        "my sister's boss was hiring", "a local cafe, mornings only", "on the tills at a supermarket",
        "nights stacking shelves", "scaffolding with my brother", "making sandwiches at a factory",
        "admin at the hospital now", "with a cleaning company doing offices", "driving a van for a florist",
        "hospital catering", "an office near the station", "back with the company I left last year",
    ],
    "Too many emails": [
        "I only wanted one a week", "a weekly round up would be better", "I'd rather get them once a week",
        "the Sunday one is enough for me", "I already get the weekly one",
        "set up searches for two towns and got two lots every day", "every search sends its own email which is mad",
        "why does each search need a separate email", "should all come together in one",
        "could you put them all in one email", "had a search for driving and one for warehouse, so double",
        "I made too many searches when I signed up", "my fault for saving so many searches",
        "I didn't realise each search would email me", "half of them were the same jobs",
        "the same jobs kept coming up day after day", "same adverts over and over", "nothing new most days",
        "most days there was nothing new for me", "6am every morning is too early",
        "they woke me up at 6 in the morning", "my phone buzzing at 6am", "I could not keep on top of them",
        "couldn't keep up so ignored them", "ended up just deleting them", "I was deleting them without reading",
        "stopped reading them after a while", "they were drowning out my other emails",
        "my important emails got buried under them", "I'd like to choose how often", "let me pick the days",
        "would like them twice a week", "every other day would be fine",
        "only when something new and decent comes up", "only want to hear when there's a good match",
        "if there's nothing new don't send anything", "too many for the number of jobs round here",
        "small town, same handful of jobs every day", "plus the other job sites I'm on",
        "I'm signed up to 3 sites already", "on top of all the agency emails",
        "with the agencies emailing too it was too much", "I get texts from agencies as well",
        "my partner gets them as well, so we get double", "it felt like pressure every morning",
        "it was getting me down seeing them every day", "depressing seeing them when nothing fits",
        "too much when you're already stressed about money", "I'm not in a rush so don't need daily",
        "not urgently looking so daily is overkill", "I'm only casually looking",
        "just browsing really, don't need daily", "I prefer to look myself when I have time",
        "I'd rather search on the app when I want", "I check the site anyway",
        "I look on the site most days so the emails are pointless", "used to like them but it got too much",
        "fine at first then it got silly", "after a few weeks it was just noise", "felt like a lot of noise",
        "couldn't find how to change how often", "the settings are confusing",
        "tried to change to weekly but couldn't see how", "there's no option for less often",
        "please add a weekly option", "I'd have kept them if they were weekly", "less would be more",
        "you'd get more out of me with fewer emails", "I don't need one every day for one search",
        "one search, one email a day, still too much", "even one a day adds up",
        "seven a week is a lot from one site", "it's the daily thing, not the jobs",
        "the jobs were ok, just too often", "nothing wrong with the jobs, just the amount",
        "my emails are full of them", "I have too much going on to read them all",
        "I've got kids, no time to go through them", "on my phone it's a lot to scroll through",
        "too long, too many jobs in each one", "each email had 20 odd jobs in it",
        "they're long and I only read the first few", "the subject line was the same every time",
        "hard to tell them apart", "I couldn't tell which search each was for", "they all look the same",
        "can't you just send the best few", "with the digest on sunday too it never stopped",
        "I'll set them up again with just one search", "I set up one for my daughter too, too many",
        "monthly would suit me", "maybe once a fortnight", "it's a bit desperate daily",
        "I don't look at emails every day", "I'm at work all day and can't read them",
    ],
    "The jobs were not relevant": [
        "kept getting jobs 40 miles away", "I put 10 miles and got jobs in the next county",
        "the distance setting doesn't seem to work", "I don't drive so need jobs on a bus route",
        "half of them were in a different town", "searched for my town and got the whole region",
        "I wanted days and kept getting nights", "I need school hours and nothing fits",
        "part time searches still show full time", "I'm looking for part time only",
        "lots of zero hours contracts", "mostly agency adverts with no company named",
        "the same agency advert posted 10 times", "the pay was always minimum wage", "nothing over minimum wage",
        "the salary range I set seems to be ignored", "I'm a qualified accountant and got cleaning jobs",
        "searched for care work and got retail", "I wanted office work and got warehouse jobs",
        "I'm a chef and got bar jobs", "kept sending me driving jobs, I don't have a licence",
        "HGV jobs when I only have a car licence", "jobs needing experience I don't have",
        "everything wanted 2 years experience", "I'm 17 and most need you to be 18",
        "graduate here, all entry level stuff not in my field", "too senior for me, all manager roles",
        "too junior, I've got 15 years in the trade", "nursing jobs I'm not registered for",
        "jobs needing a DBS I don't have yet", "commission only sales jobs, no thanks",
        "lots of self employed courier roles, not real jobs", "the job titles didn't match what the job was",
        "it ignored my keywords", "I put warehouse and got everything", "seemed random to be honest",
        "like it picked jobs at random", "nothing new in my area for weeks",
        "rural area so there's hardly anything", "I'm in a small village, nothing nearby",
        "I need remote work and got office based jobs", "wanted work from home only",
        "night shifts when I said days", "weekend work when I can't do weekends",
        "jobs that closed before I saw them", "half were already filled", "expired adverts",
        "dodgy looking adverts", "lots of the same job from different agencies",
        "I'm looking for apprenticeships and got none", "nothing for apprenticeships",
        "I want hospitality and got construction", "I asked for admin and got sales",
        "care jobs are all I get and I've left care", "I've changed career and the old search kept going",
        "my old search was still running", "I couldn't edit the search properly",
        "every job was miles off what I asked for", "nothing matched my qualifications",
        "I have a degree and the jobs need GCSEs", "teaching jobs in primary, I'm secondary",
        "temp jobs only, I want permanent", "only ever temp work", "contract roles I don't want",
        "jobs paying less than I get now", "no part time at all",
        "I'm disabled and the jobs weren't accessible", "I need step free access and none said",
        "I need flexible hours, nothing was", "the hours were never listed",
        "pay never shown on half of them", "lots of jobs with no salary",
        "travel costs would eat the wage", "I'm a welder, got catering", "electrician jobs needing my own van",
        "everything was in the city centre and I can't get there", "retail jobs on sundays only",
        "jobs for students when I'm 50", "I wanted warehouse days, got office temp",
    ],
    "I moved area": [
        "now in Bristol", "moved up to Scotland", "back in Wales with family", "moved to be near my mum",
        "to Leeds for my partner's job", "moving to Spain in the autumn", "emigrating to Australia",
        "went back to Ireland", "living with my sister in Glasgow now", "moved from the city to the coast",
        "need to set up a new search for where I am now", "the alerts were for my old town",
        "my searches were all for the old area", "haven't got round to changing my location",
        "couldn't change the location easily", "will start a new search when settled",
        "moving for uni in september", "moved for a job my husband got",
        "a council house came up in another town", "rent was too high so moved out of town",
        "back home to Cornwall", "moved to Northern Ireland", "in the Highlands now, not much work",
        "moved down south", "moved up north for cheaper rent", "living in Norwich now", "I'm in Hull now",
        "my husband is in the forces so we moved again", "temporary move to look after my dad",
        "moved in with my partner in Derby",
    ],
    "Taking a break": [
        "maternity leave till next year", "just had a baby", "due in august", "looking after my newborn",
        "on paternity leave", "caring for my dad full time", "looking after my mum after her stroke",
        "my husband is ill so I'm at home", "carer for my son", "studying full time till the summer",
        "doing an access course", "doing my level 3", "college till june", "exams first then I'll look",
        "uni finishes in may", "doing my HGV licence first", "training course for a few months",
        "off sick with my back", "having an operation soon", "recovering from surgery", "mental health break",
        "need to sort my health out first", "travelling for the summer", "going travelling in asia",
        "backpacking till october", "summer off with the kids", "school holidays, can't work till september",
        "kids are off so on hold", "volunteering for a few months", "helping with a family business for now",
        "bereavement, not ready to look", "lost my dad, taking time", "moving house first then I'll look",
        "wedding to plan!", "taking the summer to think about what next", "deciding whether to retrain",
        "thinking about going back to uni", "waiting on my visa", "on sick pay still", "signed off for 6 weeks",
        "I'll turn them back on in the autumn", "back to it in the new year",
        "I'll be back when the baby is older", "caring for my grandad", "doing a course in september",
    ],
    "Other": [
        "can't remember signing up", "didn't know I'd signed up for these", "my daughter set it up for me",
        "my son did this for me", "my partner made the account", "using a different job site now",
        "I prefer a different app", "the app is easier than emails", "I just use the app now",
        "I look in the local paper", "I use the job centre now", "my work coach told me to use another site",
        "retired now", "retiring in the autumn", "self employed now", "started my own thing",
        "going back to education", "joined the army", "doing an apprenticeship through school",
        "it was for a friend", "was only looking for my son", "was looking for my partner",
        "I don't remember why", "too many sites, cutting down", "cutting down my emails generally",
        "having a clear out of everything I'm signed up to", "privacy, don't want my details out there",
        "worried about my data", "don't like the adverts", "your site is slow on my phone",
        "the site kept crashing", "I couldn't apply on my phone", "had a bad experience with an employer from here",
        "an employer never got back to me", "applied for loads, never heard anything",
        "no replies from any applications", "felt pointless, nobody replies", "I'm 64, nobody wants to hire me",
        "the survey is too long", "I prefer to apply in person", "my husband looks for me",
        "I'm on a course through the job centre", "my agency finds me work",
    ],
}
FORMS = {  # chance of a short answer alone, an elaboration alone; the rest write both
    "I found a job": (0.34, 0.26), "Too many emails": (0.30, 0.30), "The jobs were not relevant": (0.30, 0.34),
    "I moved area": (0.30, 0.38), "Taking a break": (0.30, 0.38), "Other": (0.32, 0.42),
}
JOINS = [", ", ", ", ", ", ". ", ". ", " ", " - ", "... ", ", "]
SHORTEN = [("I'm", "Im"), ("I've", "Ive"), ("don't", "dont"), ("didn't", "didnt"), ("can't", "cant"),
           ("couldn't", "couldnt"), ("it's", "its"), ("I'd", "Id"), ("doesn't", "doesnt"), ("there's", "theres"),
           ("you'd", "youd"), ("you're", "youre"), ("haven't", "havent"), ("weren't", "werent")]


def norm(s):
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", s.lower()).split())


def comment(reason, rng, st):
    """One answer in the respondent's own words: never more than twice the same, an elaboration at most twice."""
    heads, tails = HEADS[reason], TAILS[reason]
    p_head, p_tail = FORMS[reason]
    for _ in range(4000):
        u = rng.random()
        form = "h" if u < p_head else ("t" if u < p_head + p_tail else "ht")
        h = heads[int(rng.integers(0, len(heads)))] if "h" in form else None
        t = tails[int(rng.integers(0, len(tails)))] if "t" in form else None
        if h is not None and st["head"].get(h, 0) >= 4:
            continue
        if t is not None and st["tail"].get(t, 0) >= 2:
            continue
        if form == "h":
            s = h
        elif form == "t":
            s = t
        else:
            j = JOINS[int(rng.integers(0, len(JOINS)))]
            s = h.rstrip("!.") + j + (t[0].upper() + t[1:] if j == ". " else t)
        if rng.random() < 0.3:
            for a, b in SHORTEN:
                s = s.replace(a, b)
        v = rng.random()
        if v < 0.32:
            s = s[0].lower() + s[1:]
        elif v < 0.62:
            s = s[0].upper() + s[1:]
        elif v < 0.67:
            s = s.lower()
        if s[-1] not in ".!?":
            w = rng.random()
            if w < 0.24:
                s += "."
            elif w < 0.27:
                s += "!"
        key = norm(s)
        if st["seen"].get(key, 0) >= 2:
            continue
        st["seen"][key] = st["seen"].get(key, 0) + 1
        if h is not None:
            st["head"][h] = st["head"].get(h, 0) + 1
        if t is not None:
            st["tail"][t] = st["tail"].get(t, 0) + 1
        return s
    raise RuntimeError("survey: no fresh comment left for %r" % reason)


def survey(tgt):
    rng = np.random.default_rng(W.SEED + 12)
    crng = np.random.default_rng(W.SEED + 13)
    st = {"seen": {}, "head": {}, "tail": {}}
    rows = []
    n = 1287
    pr = np.array([0.31, 0.22, 0.2, 0.08, 0.09, 0.1])
    for i in range(n):
        d = dt.date(2026, 6, 8) + dt.timedelta(days=int(rng.integers(0, 17)))
        reason = REASONS[int(rng.choice(len(REASONS), p=pr))]
        status = "paused" if rng.random() < 0.7 else "unsubscribed"
        com = COMMENTS[reason][int(rng.integers(0, len(COMMENTS[reason])))]
        com = comment(reason, crng, st) if com else ""
        rows.append(["R%06d" % int(rng.integers(100000, 999999)), d.isoformat(), status, reason, com,
                     int(rng.integers(1, 6)) if rng.random() < 0.85 else ""])
    rows.sort(key=lambda r: (r[1], r[0]))
    with open(os.path.join(tgt, "alerts_feedback_survey_2026-06.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["response_id", "response_date", "alerts_status", "main_reason", "comment", "satisfaction_1_5"])
        w.writerows(rows)


def main(tgt, h):
    plan(tgt)
    brief(tgt)
    calendar(tgt)
    domain_groups(tgt)
    revenue(tgt, h)
    survey(tgt)
