"""The pack's documents: the network's Performance Standard (Exhibit B to each payer agreement), the board's July 2026
resolution on the 2027 two-sided track, the three payers' 2025 settlement statements on their own contract terms, and
the network's field guide to the payers' feeds."""
import datetime as dt

import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

reportlab.rl_config.invariant = 1
STY = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=STY["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=6)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10)
H = ParagraphStyle("h", parent=STY["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
T = ParagraphStyle("t", parent=STY["Title"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=10)
HEAD = ParagraphStyle("hd", parent=STY["BodyText"], fontName="Helvetica-Bold", fontSize=7, leading=8.5, alignment=2)
HEADL = ParagraphStyle("hdl", parent=HEAD, alignment=0)
STAMPS = {"standard": b"D:20251216143000-06'00'", "resolution": b"D:20260724101500-05'00'",
          "statements": b"D:20260612090000-05'00'"}


def _pdf(path, title, story, author, org):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch, topMargin=0.7 * inch,
                            bottomMargin=0.7 * inch, title=title, author=author, creator=author, subject=title,
                            producer=org)

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(0.8 * inch, 0.45 * inch, org + "  |  " + title)
        c.drawRightString(letter[0] - 0.8 * inch, 0.45 * inch, "Page %d" % d.page)
        c.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def _table(rows, widths=None, size=8):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def P(text, style=BODY):
    return Paragraph(text, style)


def standard_pdf(path):
    payers = "%s, %s and %s" % tuple(W.PAYER_NAMES[p] for p in W.PAYERS)
    rates = "; ".join("%s USD %.2f" % (W.PAYER_NAMES[p], W.CCF_RATE[p]) for p in W.PAYERS)
    s = [P("Performance Standard for Commercial Members", T),
         P(W.NETWORK + ". Adopted by the Board of Directors on 11 December 2025 and attached as Exhibit B to the network's "
           "2026 value-based agreements with " + payers + ". Effective for performance year 2026.", SMALL),
         P("1. Purpose", H),
         P("This standard sets the one measure the network uses for each member practice's cost performance across its "
           "commercial payers: the network measure. Each agreement's own settlement of shared savings with its payer is "
           "governed by that agreement's Schedule A and is not changed by this standard."),
         P("2. Attribution", H),
         P("2.1 Each payer attributes its own commercial members on its own claims. A member is attributed for a performance "
           "year to the member practice whose primary care clinicians furnished the most days of qualifying primary care "
           "services to the member in that year; where practices tie, to the practice that furnished the latest such day. "
           "A qualifying primary care service is a service with a code in Appendix A furnished by a clinician on the network's "
           "primary care roster for that practice on the date of service."),
         P("2.2 A member with no qualifying primary care service from a network clinician in the year is not attributed for "
           "that year. A member attributed for a year is attributed for every month of the year in which the member was "
           "covered by the payer, including the months before the member's first qualifying service."),
         P("2.3 Each payer runs attribution monthly from March of the performance year (an interim run), on qualifying "
           "services incurred through the end of the second month before the run and paid by the end of the month before it. "
           "The final run for a performance year is the payer's April run in the following year, on all qualifying services "
           "incurred in the performance year and paid by 31 March."),
         P("3. The network measure", H),
         P("3.1 A member's total cost of care for a year is the allowed amount, at its current version, of every claim for "
           "covered medical and pharmacy services incurred in the year and first paid by 31 March of the following year, "
           "capped at USD 250,000 for the member's year. A claim is incurred on its first date of service (a pharmacy "
           "claim on its fill date)."),
         P("3.2 A member month is a calendar month in which the member's coverage with the payer was in force."),
         P("3.3 A practice's network measure for a year is the total cost of care of the members attributed to it on the "
           "final runs of the three payers, summed across the payers, divided by those members' member months in the year, "
           "summed across the payers."),
         P("3.4 A practice's benchmark for 2026 is its network measure for 2025, rounded to the cent, times the "
           "agreements' 2026 trend factor of 1.052, rounded to the cent."),
         P("4. Interim reports", H),
         P("4.1 After each interim run the network reports each practice's interim measure: the allowed amounts of the "
           "claims incurred from 1 January through the month of the run's service cut and paid by the date of the payer's "
           "feed, divided for each payer and month incurred by that payer's completion factor for the month (Appendix C), "
           "for the members on the interim run, each member's year to date capped at USD 250,000, divided by those members' "
           "member months from January through the month of the service cut."),
         P("4.2 Interim reports are management information and are not used to settle shared savings."),
         P("5. Care coordination fees", H),
         P("5.1 Each payer pays the network a care coordination fee for each attributed member for each month of the "
           "performance year the member is covered by the payer: " + rates + " a member month in 2026."),
         P("5.2 Fees are paid on each interim run: for the month of the run, for each member on the run covered that month, "
           "and, for a member on the payer's run for the first time in the year, for each earlier month of the year in which "
           "the member was covered. Fees are paid to the network for the practice to which the run attributes the member."),
         P("Appendix A. Qualifying primary care services", H),
         P("The codes are listed in qualifying_primary_care_services.csv, issued with this standard."),
         P("Appendix B. The payers' feeds", H),
         P("Each payer sends the network, monthly, its claims and coverage for the members on its latest interim run and, "
           "for the prior performance year, for the members on its final run, with its attribution runs and its fee "
           "remittances. The layouts are set out in the network's field guide."),
         P("Appendix C. Completion factors", H),
         P("Each payer issues, with its September-paid feed, the share of a month's allowed amounts it has paid by 30 "
           "September for each month incurred from January, from its lag study of the prior year.")]
    _pdf(path, "Performance Standard for Commercial Members", s, W.PEOPLE["analytics"], W.NETWORK)


def resolution_pdf(path):
    s = [P("Resolution 2026-11: Two-sided risk track for 2027", T),
         P(W.NETWORK + ", Board of Directors. Adopted at the meeting of 23 July 2026.", SMALL),
         P("Whereas each of the network's 2026 agreements with its commercial payers offers member practices, from 1 January "
           "2027, a two-sided track that pays a larger share of savings and recovers a share of losses; and whereas a "
           "practice should take on losses only where its cost performance is already clear of its benchmark;"),
         P("<b>Resolved</b>, that the network enters a member practice in the two-sided track for 2027 only where the "
           "practice's network measure for 2026 under the Performance Standard, on the payers' final 2026 attribution, comes "
           "in at least 2 per cent below the practice's 2026 benchmark;"),
         P("<b>Resolved further</b>, that because the payers' elections close before the final 2026 runs, the president "
           "presents to the Board at its October meeting the network's projection of each practice's 2026 network measure on "
           "that basis, and the Board elects on it;"),
         P("<b>Resolved further</b>, that the elections be filed with each payer by 30 October 2026, and that a practice not "
           "entered remains in the one-sided track for 2027."),
         Spacer(1, 10),
         P("Attest: " + W.PEOPLE["president"] + ", President.", SMALL)]
    _pdf(path, "Board Resolution 2026-11", s, W.PEOPLE["president"], W.NETWORK)


STATEMENT_TERMS = {
    "B": dict(cap=150000.0, rx=True, msr=0.02, share=0.50, note="Schedule A: medical and pharmacy allowed, each member's "
              "year capped at USD 150,000; savings shared at 50 per cent where the practice's savings reach 2 per cent of its "
              "benchmark, times the practice's quality multiplier."),
    "M": dict(cap=100000.0, rx=False, msr=0.0, share=0.45, note="Schedule A: medical allowed only (pharmacy is settled "
              "under the pharmacy benefit agreement), each member's year capped at USD 100,000; savings shared at 45 per cent, "
              "times the practice's quality multiplier."),
    "T": dict(cap=200000.0, rx=True, msr=0.03, share=0.50, note="Schedule A: medical and pharmacy allowed, each member's "
              "year capped at USD 200,000; savings shared at 50 per cent where the practice's savings reach 3 per cent of its "
              "benchmark, times the practice's quality multiplier."),
}


def statement_rows(w):
    """Each payer's 2025 settlement by practice on its own Schedule A terms, from the world's 2025 claims."""
    col, att, ppl = w["claims"], w["att"], {q.pid: q for q in w["people"]}
    quality = W.quality_multipliers()
    out = {}
    for payer in W.PAYERS:
        terms = STATEMENT_TERMS[payer]
        fin = att[("final", payer, 2025)]
        tot = {}
        for i in range(len(col["pid"])):
            if col["payer"][i] != payer or col["year"][i] != 2025 or col["paid"][i] > W.FINAL_PAID[2025]:
                continue
            if col["pid"][i] not in fin or (col["ctype"][i] == "RX" and not terms["rx"]):
                continue
            tot[col["pid"][i]] = tot.get(col["pid"][i], 0.0) + col["allowed"][i]
        g = W.rng(51, W.PAYERS.index(payer))
        rows = []
        for c in W.CODES:
            mem = [pid for pid, v in fin.items() if v[0] == c]
            mm = sum(W.enrolled_months(ppl[pid], 2025) for pid in mem)
            tc = sum(min(terms["cap"], tot.get(pid, 0.0)) for pid in mem)
            pmpm = tc / mm
            bench = round(pmpm * float(g.uniform(0.965, 1.075)), 2)
            sav = (bench - pmpm) * mm
            earned = sav if sav >= terms["msr"] * bench * mm and sav > 0 else 0.0
            qm = quality[(payer, c)]
            pay = round(earned * terms["share"] * qm, 2)
            rows.append(dict(practice=c, members=len(mem), mm=mm, tcoc=round(tc, 2), pmpm=round(pmpm, 2), bench=bench,
                             savings=round(sav, 2), quality=qm, payment=pay))
        out[payer] = rows
    return out


def statements_pdf(path, w):
    rows = statement_rows(w)
    s = []
    for n, payer in enumerate(W.PAYERS):
        if n:
            s.append(PageBreak())
        s.append(P(W.PAYER_NAMES[payer] + ": Performance Year 2025 Shared Savings Statement", T))
        s.append(P("Prepared for " + W.NETWORK + ". Final attribution run of April 2026; claims incurred in 2025 and paid "
                   "through 31 March 2026. Issued 12 June 2026." + (" Signed for the plan: " + W.PEOPLE["payer"] + ", Manager, "
                   "Provider Performance." if payer == "B" else ""), SMALL))
        s.append(P(STATEMENT_TERMS[payer]["note"], SMALL))
        hdr = [P("Practice", HEADL)] + [P(x, HEAD) for x in ("Members", "Member months", "Total cost (USD)", "PMPM",
                                                             "Benchmark PMPM", "Savings (USD)", "Quality", "Payment (USD)")]
        body = [[W.PRACTICE_NAMES[r["practice"]], "{:,}".format(r["members"]), "{:,}".format(r["mm"]), "{:,.2f}".format(r["tcoc"]),
                 "%.2f" % r["pmpm"], "%.2f" % r["bench"], "{:,.2f}".format(r["savings"]), "%.2f" % r["quality"],
                 "{:,.2f}".format(r["payment"])] for r in rows[payer]]
        tot = ["Network", "{:,}".format(sum(r["members"] for r in rows[payer])), "{:,}".format(sum(r["mm"] for r in rows[payer])),
               "{:,.2f}".format(sum(r["tcoc"] for r in rows[payer])), "", "", "{:,.2f}".format(sum(r["savings"] for r in rows[payer])),
               "", "{:,.2f}".format(sum(r["payment"] for r in rows[payer]))]
        s.append(_table([hdr] + body + [tot], widths=[1.6 * inch, 0.62 * inch, 0.66 * inch, 0.84 * inch, 0.5 * inch,
                                                       0.72 * inch, 0.76 * inch, 0.52 * inch, 0.78 * inch], size=7))
        s.append(Spacer(1, 6))
        s.append(P("Savings are the benchmark PMPM less the PMPM, times member months; a negative figure is a loss and is not "
                   "recovered under the one-sided track. The quality multiplier is 1.00 where every measure scored for the "
                   "practice meets its target, 0.95 where three quarters or more do, 0.90 where half or more do, and 0.85 "
                   "otherwise.", SMALL))
    _pdf(path, "Performance Year 2025 Shared Savings Statements", s, W.PEOPLE["payer"],
         "Payer statements as received by " + W.NETWORK)


def guide_txt(path):
    text = """LARROWBROOK PHYSICIAN NETWORK - FIELD GUIDE TO THE PAYERS' VALUE-BASED FEEDS
Maintained by Payer Performance Analytics (Joel Brewer, Director). Revised 13 October 2026.

The payers send claims and coverage for the members on their latest interim attribution run and, for the
prior performance year, for the members on their final run (Performance Standard, Appendix B). Each payer's
files keep that payer's own layout. A member's identifier is the payer's; the master patient index carries
one network patient identifier across payers.

MERRINLAKE HEALTH PLAN (MLH)
  mlh_tcoc_claims_2025-01_2026-09.csv     one row per claim; comma separated; dates YYYY-MM-DD
    CLM_ID           claim number; a reprocessed claim is voided and replaced under new numbers
    MBR_ID           Merrinlake member identifier
    CLM_TYP          PROF professional, OUTP outpatient facility, INPT inpatient facility, PHRM pharmacy
    SVC_FROM_DT      first date of service (fill date for pharmacy)
    SVC_THRU_DT      last date of service
    PD_DT            date paid
    PROC_CD          CPT or HCPCS code (professional claims)
    PROC_MOD         procedure modifier, where billed
    POS_CD           place of service (professional claims)
    REV_CD           revenue code (facility claims)
    NDC_11           national drug code (pharmacy claims)
    REND_NPI         rendering provider NPI (professional claims)
    ALLOWED_AMT      allowed amount, USD
    DAYS_SUPPLY      days supply (pharmacy claims)
    ADJ_TYP          blank for an original claim; VOID for a reversal of it; REPL for its replacement
    ORIG_CLM_ID      on VOID and REPL rows, the claim they reverse or replace
  mlh_eligibility_2025_2026.csv           one row per coverage span; COV_TERM_DT 9999-12-31 while open
  mlh_attribution_runs_py2025_py2026.csv  the final 2025 run (PY2025-F) and the October 2026 interim run (PY2026-10)
  mlh_care_coordination_remittance_2026.csv  fees paid on each 2026 interim run; COV_MO is the month the fee covers;
                                          LINE_TYP CUR for the run's month, RETRO for an earlier month

KESSELCREST BENEFIT PARTNERS (KBP)
  KBP_CLAIMS_LPN_20261009.txt             pipe delimited; dates MM/DD/YYYY
    CLAIM_NO, LINE_NO, MEMBER_NO          claim, line and member; a reprocessed claim takes a suffix -01
    CLAIM_FORM                            1500 professional, UB04 facility, NCPDP pharmacy
    FIRST_DOS, LAST_DOS, PAID_DATE        dates of service and payment
    PROCEDURE, MODIFIER, PLACE_OF_SVC, REVENUE, NDC, RENDERING_PROV_NPI
    ALLOWED_CENTS                         allowed amount in cents
    CLAIM_STATUS                          P paid and current; A adjusted (superseded by a reprocessed claim)
  KBP_ELIG_LPN_20261009.txt               coverage spans; blank TERM_DATE while open; REL_CD 18 self, 19 child
  KBP_ATTRIBUTION_PY2025F_PY2026R10.xlsx  one sheet per run; the header row is the fourth row
  KBP_CCF_REMIT_2026.xlsx                 care coordination remittances to the network's TINs in 2026; Service Period is
                                          the month the fee covers

PEMBERGLEN MUTUAL HEALTH (PMH)
  pmh_partner_claims_2026-10-12.json      {"records": [...]}; one object per claim version
    claimId, memberId, type               type professional, institutional_outpatient, institutional_inpatient, pharmacy
    serviceStart, serviceEnd, adjudicated dates of service and of adjudication
    cpt, modifier, pos, renderingNpi      professional claims (modifier where billed)
    revenueCode                           facility claims
    ndc, daysSupply                       pharmacy claims
    allowed                               allowed amount, USD
    version                               1 for the first adjudication; a reprocessed claim's later version replaces it
  pmh_members_2026-10-12.csv              coverage; blank coverageEnd while open
  pmh_attribution_py2025_py2026.csv       FINAL (2025) and INTERIM-10 (2026) runs
  pmh_ccf_payments_2026.csv               care coordination payments on each 2026 interim run

NETWORK FILES
  lpn_primary_care_roster_2026-10.xlsx    the network's primary care clinicians by practice with effective dates
  lpn_master_patient_index.csv            network patient identifier for each payer member identifier
  payer_completion_factors_2026-09.csv    Appendix C of the Performance Standard
  qualifying_primary_care_services.csv    Appendix A of the Performance Standard
  payer_em_fee_schedules_2026.xlsx        each payer's 2026 evaluation and management rates for network clinicians
"""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def write_all(t, w, ids, cf):
    standard_pdf(t("standard"))
    resolution_pdf(t("resolution"))
    statements_pdf(t("statements"), w)
    guide_txt(t("guide"))
