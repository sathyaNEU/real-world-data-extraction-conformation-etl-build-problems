"""The institute's own documents: the examination regulations (the filed rules), the November 2026 Paper 2 question
paper, the minutes of the Examinations Committee's May results meeting, and two files kept for other purposes (the
accreditation results history and the 2027 venue holds)."""
import datetime as dt

import numpy as np

import params as P
from pack import normalise_zip, write_pdf, xlsx_props

ISSUER = "%s Examinations Office" % P.ORG_SHORT


def regulations(path):
    b = [
        ("title", "%s Regulations" % P.EXAM),
        ("small", "%s. Version 3, approved by the Council on 28 July 2026 and in force from 3 August 2026. Version 3 "
                  "moves entries, withdrawals and requests to the candidate portal; the examination rules are "
                  "otherwise unchanged from version 2. Owner: Manager, Examinations." % P.ORG),
        ("h", "1 Application"),
        ("p", "1.1 These regulations govern the %s, which the Institute holds twice a year, in May and November. The "
              "examination has two papers. Paper 1 (Legislation and Standards) is a multiple choice paper of 100 "
              "marks. Paper 2 (Building Assessment and Certification Practice) is a written paper of three hours "
              "offering eight questions of 20 marks each, of which the candidate answers five." % P.EXAM),
        ("p", "1.2 A candidate is accredited when they have passed both papers."),
        ("h", "2 Definitions"),
        ("p", "In these regulations: <i>sitting</i> means an examination held on a date published by the Institute; "
              "<i>the candidates who sat a paper</i> means every candidate marked present for that paper at the "
              "sitting; <i>result</i> means pass or fail on a paper; <i>Committee</i> means the Examinations "
              "Committee; <i>working day</i> means a day other than a Saturday, a Sunday or a public holiday in New "
              "South Wales."),
        ("h", "11 Marking"),
        ("p", "11.1 Each answer is marked against the marking guide by an examiner appointed by the Chief Examiner "
              "for the paper."),
        ("p", "11.2 The mark of record for a part of a question is the last mark entered for it on the marking "
              "system. After results are issued, a mark of record changes only on a review under regulation 19."),
        ("h", "12 Pass mark"),
        ("p", "A candidate passes Paper 2 with a total of 50 or more of the 100 marks available, counted after any "
              "moves under regulation 14."),
        ("h", "14 Optional questions"),
        ("p", "14.1 Where a paper offers a choice of questions, each optional question is moved by a whole number of "
              "marks, rounded to the nearest whole mark, equal to how much harder (marks added) or easier (marks "
              "taken away) the question proved than the average of the paper's optional questions, each counted "
              "once, for the candidates who sat the paper."),
        ("p", "14.2 A question's move is applied to the mark of record of every candidate who answered the question. "
              "A moved mark is not taken below zero or above the marks available for the question."),
        ("p", "14.3 The Committee approves the moves for a sitting with that sitting's results, and the moves it "
              "approves stand for the sitting."),
        ("h", "15 Borderline review"),
        ("p", "Before results are issued, the script of every candidate whose Paper 2 total after the moves is 48 or "
              "49 is re-marked in full by a senior examiner."),
        ("h", "16 Issue of results"),
        ("p", "Results are issued to candidates in writing on the date the Committee sets. A result is issued on the "
              "marks of record on that date."),
        ("h", "17 Withdrawal and absence"),
        ("p", "17.1 A candidate withdraws an entry for one paper or both by a request through the candidate portal. A "
              "withdrawal has effect from the time the request is received."),
        ("p", "17.2 A request to withdraw that is received on the day of the sitting or later does not withdraw the "
              "entry."),
        ("p", "17.3 A candidate who is entered for a paper, has not withdrawn before the day of the sitting and does "
              "not sit the paper is recorded absent."),
        ("p", "17.4 The entry fee for an entry withdrawn by the closing date for entries is refunded less an "
              "administration charge of 25 per cent. No refund is made for a later withdrawal or an absence."),
        ("h", "18 Centres"),
        ("p", "A candidate may move an entry to another centre by a request through the candidate portal up to 14 "
              "days before the sitting."),
        ("h", "19 Review of results"),
        ("p", "19.1 A candidate may request a review of a Paper 2 result within 15 working days of its issue: a "
              "clerical check of the whole script, or a re-mark of one or more named questions."),
        ("p", "19.2 A review is carried out by a senior examiner, whose marks become the marks of record. Marks may go "
              "down as well as up. A review does not change the moves approved for the sitting."),
        ("p", "19.3 A request received after the closing date for reviews is declined."),
        ("p", "19.4 The fee paid for a review is refunded where the review changes the candidate's result. The fee "
              "paid for a declined request is refunded."),
        ("h", "20 Time"),
        ("p", "Times and dates in these regulations are Sydney time."),
        ("h", "Schedule 1 Fees"),
        ("table", [["Service (GST inclusive, AUD)", "1 July 2025 to 30 June 2026", "From 1 July 2026"],
                   ["Paper 1 entry", "540.00", "565.00"],
                   ["Paper 2 entry", "690.00", "725.00"],
                   ["Late entry surcharge (per entry)", "95.00", "100.00"],
                   ["Re-mark, per question named", "138.00", "145.00"],
                   ["Clerical check, per script", "58.00", "62.00"]]),
        ("p", "The fee for an entry or a request is the fee in force on the day it is received. Member firms with an "
              "account agreement are invoiced at the rate in their agreement."),
    ]
    write_pdf(path, "CAE Regulations v3", ISSUER, b, stamp_date="D:20260728163000+10'00'")


PAPER_TEXT = [
    ["A two-storey building is to contain a ground-floor pharmacy and a first-floor medical practice with "
     "consulting rooms.",
     "Classify each part of the building under the NCC and explain your reasoning.",
     "The applicant proposes a Performance Solution for the stair serving the first floor. Describe the steps you "
     "would require before relying on it.",
     "Identify the Deemed-to-Satisfy provisions most likely to apply to the medical practice's sanitary facilities."],
    ["A three-storey residential flat building is framed in steel with precast concrete floors.",
     "State the documents you would require from the structural engineer before issuing a construction certificate.",
     "Explain the limits on a certifier's reliance on an engineer's certificate.",
     "During construction the builder substitutes a lighter steel section. Set out your response.",
     "List the inspections you would carry out on the structural elements and when."],
    ["A Class 5 office fit-out on the fourth floor of an existing building includes new lighting and air "
     "conditioning.",
     "Explain how Section J applies to the fit-out and which parts you would assess.",
     "The designer relies on a JV3 verification. Describe what you would check in the modelling report.",
     "Identify the provisions that apply to the new lighting and its controls.",
     "Describe the evidence you would require at completion."],
    ["A dwelling has a first-floor bathroom over a habitable room and a timber-framed balcony.",
     "State the waterproofing standard and the extent of membrane required in the bathroom.",
     "Describe the inspection you would carry out before the bathroom is tiled.",
     "The balcony has a step-down of 20 mm at the door. Comment on compliance.",
     "Water stains appear on the ceiling below the bathroom six months after occupation. Outline your obligations."],
    ["A new two-storey community centre is proposed with a public hall on the upper floor.",
     "Identify the access requirements for the entrance and the path of travel to the hall.",
     "The applicant seeks to rely on unjustifiable hardship for a lift. Explain the process and your role.",
     "List the documents you would require to show compliance with the accessible sanitary facilities.",
     "State the requirements for hearing augmentation in the hall."],
    ["A six-storey office building relies on a fire engineered Performance Solution to extend the travel distance "
     "to the exits on each floor.",
     "Describe the content you would expect in the fire engineering brief and who should be consulted.",
     "Explain how you would assess the fire engineering report against the Performance Requirements.",
     "Identify the conditions of the Performance Solution you would record on the certificate.",
     "Describe your obligations at the final inspection for the essential fire safety measures."],
    ["During construction of a dwelling you find the slab poured without the required inspection.",
     "Explain which mandatory inspection was missed and the consequences under the legislation.",
     "Describe the options open to you before certifying further work.",
     "Draft the key elements of the notice you would issue to the builder.",
     "Explain when you must notify the regulator."],
    ["A development consent for a mixed-use building contains forty conditions, several requiring matters to be "
     "satisfied before a construction certificate is issued.",
     "Explain how you determine which conditions must be satisfied before the construction certificate.",
     "The plans lodged for the construction certificate differ from the approved plans. Explain the test you apply.",
     "List the matters you must be satisfied of before issuing the construction certificate.",
     "The developer has not paid a contribution the consent requires before the certificate. Set out your response."],
]


def question_paper(path):
    b = [
        ("title", "%s, %s" % (P.EXAM, P.PAPER2)),
        ("small", "%s. November 2026 sitting, Saturday 7 November 2026. Time allowed: three hours, plus ten minutes "
                  "reading time." % P.ORG),
        ("p", "<b>Instructions to candidates.</b> Answer any FIVE questions. Each question carries 20 marks; the marks "
              "for each part are shown in brackets. Start each question on a new page of the answer booklet and "
              "write the question number at the top of the page. References are to the National Construction Code "
              "2022 and the legislation in force in your state or territory."),
    ]
    for j, (title, mx) in enumerate(P.NOV_QUESTIONS):
        txt = PAPER_TEXT[j]
        b.append(("h", "Question %d. %s" % (j + 1, title)))
        b.append(("p", txt[0]))
        for k, m in enumerate(mx):
            b.append(("p", "(%s) %s [%d marks]" % ("abcd"[k], txt[k + 1], m)))
    b.append(("small", "End of paper. CAE2 November 2026."))
    write_pdf(path, "CAE Paper 2 November 2026", ISSUER, b, stamp_date="D:20260918110000+10'00'")


def minutes(path, w):
    may = w.may_entries
    n_entries = sum(1 for e in may if "2" in e["papers"])
    n_wd = sum(1 for e in may if "2" in e["papers"] and e["withdrawn"])
    n_marked = w.may_sat_committee
    mv = ["%+d" % v if v else "0" for v in w.may_moves]
    b = [
        ("title", "Examinations Committee: minutes of meeting"),
        ("small", "%s. Thursday 18 June 2026, 10.00 am, Sussex Street boardroom and online. Minutes "
                  "(draft for confirmation, circulated to members on 22 June 2026)." % P.ORG),
        ("p", "<b>Present:</b> %s (Chair); %s (Chief Examiner, Paper 2); the Chief Examiner, Paper 1; two Council "
              "nominees. <b>In attendance:</b> %s (Assessment Analyst, Examinations Office); the Manager, "
              "Examinations." % (P.PEOPLE["chair"], P.PEOPLE["chief"], P.PEOPLE["analyst"])),
        ("h", "1. Apologies and declarations"),
        ("p", "None. No member declared an interest in a candidate at the sitting."),
        ("h", "2. Minutes of the previous meeting"),
        ("p", "The minutes of the meeting of 10 December 2025 were confirmed."),
        ("h", "3. May 2026 sitting, Paper 2"),
        ("p", "There were %d entries for Paper 2, of which %d were withdrawn before the sitting. The scripts of %d "
              "candidates have been marked. One script from the Melbourne centre has not yet been received from the "
              "courier; the candidate's result will be issued when it has been marked." % (n_entries, n_wd, n_marked)),
        ("p", "The Committee considered the moves for the paper's optional questions under regulation 14 and approved "
              "them as follows."),
        ("table", [["Question"] + ["Q%d" % (j + 1) for j in range(8)], ["Move (marks)"] + mv]),
        ("p", "With these moves, %d of the %d candidates whose scripts have been marked reach 50 marks. The Committee "
              "approved the Paper 2 results on that basis, subject to the borderline review under regulation 15." %
              (w.may_pass_committee, n_marked)),
        ("h", "4. Paper 1"),
        ("p", "The Chief Examiner, Paper 1 reported on the multiple choice paper. The Committee approved the Paper 1 "
              "results."),
        ("h", "5. Issue of results and reviews"),
        ("p", "Results will be issued on Tuesday 30 June 2026. The closing date for reviews under regulation 19 is "
              "Tuesday 21 July 2026."),
        ("h", "6. November 2026 sitting"),
        ("p", "The November sitting will be held on Saturday 7 November 2026. Entries open on 3 August and close on 25 "
              "September through the new candidate portal, with late entries to 9 October. The Parramatta centre "
              "will be known as Western Sydney from 1 August."),
        ("p", "The meeting closed at 11.40 am. Next meeting: Thursday 10 December 2026."),
    ]
    write_pdf(path, "Examinations Committee minutes 18 June 2026", ISSUER, b, stamp_date="D:20260622153000+10'00'")


def history_rows():
    rng = np.random.default_rng(P.SEED_PEOPLE + 31)
    rows = []
    for y in range(2019, 2027):
        for s in ("May", "Nov"):
            if y == 2026 and s == "Nov":
                continue
            if y == 2020 and s == "May":
                continue
            ex = int(rng.integers(420, 690))
            rate = float(rng.uniform(0.47, 0.61))
            acc = int(round(ex * rate))
            rows.append(["%s %d" % (s, y), ex, acc, "%.1f" % (100.0 * acc / ex)])
    return rows


def venue_holds(path, rng):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "2027 holds"
    ws.append(["Centre", "Venue", "Sitting", "Date", "Seats held", "Hire AUD (GST incl.)", "Hold expires",
               "Booking ref"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for code, name, _blk, share, venue, _st in P.CENTRES:
        for sitting, day in (("May 2027", dt.date(2027, 5, 15)), ("Nov 2027", dt.date(2027, 11, 6))):
            seats = int(round(share * 900 / 10.0)) * 10 + int(rng.integers(0, 3)) * 10
            hire = round(float(seats) * float(rng.uniform(21.0, 34.0)), 2)
            ws.append([name, venue, sitting, day.strftime("%d/%m/%Y"), seats, hire,
                       (day - dt.timedelta(days=int(rng.integers(60, 120)))).strftime("%d/%m/%Y"),
                       "VH-%s-%d" % (code, int(rng.integers(1000, 9999)))])
    for col, wd in zip("ABCDEFGH", (15, 42, 10, 11, 10, 18, 12, 14)):
        ws.column_dimensions[col].width = wd
    xlsx_props(wb, "Examinations Office", "Venue holds 2027", dt.datetime(2026, 10, 14, 9, 25))
    wb.save(path)
    normalise_zip(path, when="2026-10-13T22:25:00Z")
