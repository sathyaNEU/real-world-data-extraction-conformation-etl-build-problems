"""Writes the evidence pack under target/ from the simulated world."""
import csv, os, datetime as dt
import numpy as np
import openpyxl
from openpyxl.styles import Font, Alignment
from reportlab.platypus import Paragraph, Spacer
from world import *
import docs

MONTH_LABEL = ["2026-%02d" % m for m in range(1, 13)]


def abn(rng):
    """An Australian Business Number with a valid check (weights 10, 1, 3 ... 19 on the digits, the first less one,
    summing to a multiple of 89)."""
    wts = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    while True:
        body = [int(d) for d in rng.integers(0, 10, size=9)]
        for p in range(10, 100):
            if sum(a * b for a, b in zip(wts, [p // 10 - 1, p % 10] + body)) % 89 == 0:
                s = "%02d" % p + "".join(map(str, body))
                return "%s %s %s %s" % (s[:2], s[2:5], s[5:8], s[8:])


def statement_sa2_by_month(c, rng_sa2):
    """The statement SA2 a card carried each month: its address at selection, or a new one from the month it changed."""
    out = {}
    for m in range(1, 13):
        if c.sa2_change and m >= c.sa2_change[0]:
            out[m] = c.sa2_change[1]
        else:
            out[m] = c.sa2
    return out


def card_tokens(cards):
    """The scheme's de-identified card tokens: twelve hexadecimal characters, unique, unrelated to selection order."""
    rng = np.random.default_rng(SEED + 23)
    seen, out = set(), {}
    for c in cards:
        while True:
            t = "%012x" % int(rng.integers(16 ** 11, 16 ** 12))
            if t not in seen:
                seen.add(t); out[c.cid] = t
                break
    return out


def write_sample(T, cards, weight, rng, sa2s):
    tok = card_tokens(cards)
    rows = []
    for c in cards:
        sm = statement_sa2_by_month(c, None)
        for (r, m), v in c.rows.items():
            rows.append((tok[c.cid], r, m, sm[m], v[0], v[1], v[2]))
    rows.sort(key=lambda t: (t[2], t[0], t[1]))
    path = os.path.join(T, "apn_pos_research_extract_2026.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["card_id", "merchant_region", "month", "statement_sa2", "spend_aud", "transactions", "active_days"])
        for cid, r, m, sa2, s, t, d in rows:
            w.writerow([cid, r, MONTH_LABEL[m - 1], sa2, "%.2f" % s, t, d])
    # the card register: stratum and selection weight
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "cards"
    ws.append(["card_id", "selection_stratum", "selection_weight"])
    strata = list(CODES) + ["IS"]
    perm = [strata[i] for i in rng.permutation(len(strata))]
    label = {h: "ST%02d" % (i + 1) for i, h in enumerate(perm)}
    for c in sorted(cards, key=lambda c: tok[c.cid]):
        ws.append([tok[c.cid], label[c.stratum], round(weight[c.stratum], 4)])
    for col, wd in zip("ABC", (15, 12, 16)):
        ws.column_dimensions[col].width = wd
    docs.save_xlsx(wb, os.path.join(T, "apn_research_cards_2026.xlsx"), SCHEME, dt.datetime(2027, 1, 22, 2, 47, 11),
                   dt.datetime(2027, 1, 22, 2, 47, 11), SCHEME)
    return len(rows)


def write_erp(T, sa2s):
    with open(os.path.join(T, "erp_sa2_30jun2026_preliminary.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["sa2_code", "sa2_name", "sa3_code", "sa3_name", "erp_30jun2026"])
        for x in sa2s:
            w.writerow([x["sa2"], x["sa2_name"], x["sa3"], x["sa3_name"], x["erp26"]])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Table 1"
    ws.append(["Estimated resident population, statistical areas level 2"])
    ws.append(["30 June 2025, revised"])
    ws.append([])
    ws.append(["SA2 code", "SA2 name", "Persons"])
    for x in sa2s:
        ws.append([int(x["sa2"]), x["sa2_name"], x["erp25"]])
    ws.append([])
    ws.append(["Released with the 30 June 2026 preliminary estimates."])
    ws["A1"].font = Font(bold=True)
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 26
    docs.save_xlsx(wb, os.path.join(T, "erp_sa2_30jun2025_revised.xlsx"), "Statistics office",
                   dt.datetime(2026, 12, 16, 22, 40, 12), dt.datetime(2026, 12, 16, 23, 5, 3), "Statistics office")


def write_totals(T, cards, weight, rng):
    tot = {}
    for c in cards:
        w = weight[c.stratum]
        for (r, m), v in c.rows.items():
            k = (r, m)
            a = tot.setdefault(k, [0.0, 0.0])
            a[0] += w * v[0]; a[1] += w * v[1]
    overseas = {"JAB": 0.16, "SPX": 0.14, "LYR": 0.05, "WST": 0.06, "YAL": 0.07, "TNG": 0.04, "CAR": 0.05}
    with open(os.path.join(T, "apn_regional_totals_2026.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["merchant_region", "month", "issuer_location", "spend_aud", "transactions"])
        for r in CODES:
            for m in range(1, 13):
                s, t = tot.get((r, m), (0.0, 0.0))
                k = rng.uniform(1.07, 1.13)  # the totals carry commercial and prepaid cards the research sample leaves out
                w.writerow([r, MONTH_LABEL[m - 1], "Australia", "%.2f" % (s * k), int(round(t * k))])
                o = overseas.get(r, 0.02) * rng.uniform(0.7, 1.3)
                w.writerow([r, MONTH_LABEL[m - 1], "Overseas", "%.2f" % (s * o), int(round(t * o * 0.8))])


def guidelines(T, sa2s):
    path = os.path.join(T, "rvif_2027_round_guidelines.pdf")
    shared_rows = []

    def story():
        P = lambda t, s=docs.BODY: Paragraph(t, s)
        out = [P("Regional Visitor Infrastructure Fund", docs.H1),
               P("Guidelines for the 2027 round", docs.H2),
               P("%s. Approved by the Commission's board on 9 November 2026. Fund manager: %s." % (COMMISSION, PEOPLE["fund"]), docs.META),
               Spacer(1, 6),
               P("1. Purpose", docs.H2),
               P("Visitors use the toilets, car parks, waste services, lookouts and local roads that councils build and keep "
                 "up out of their rates. Where a region's visitors spend a great deal for each person who lives there, that "
                 "load falls on a small rate base. The Fund pays for visitor infrastructure in the regions where the load is "
                 "heaviest."),
               P("2. The 2027 round", docs.H2),
               P("The round funds five tourism regions. Its total is the Fund's 2027 appropriation of $12,000,000, adjusted "
                 "for the closure of the Regional Tourism Infrastructure Program as the Commission's decision of 21 October "
                 "2026 provides, and it is shared equally among the five regions. Each funded region's councils then apply "
                 "for projects under the grant conditions."),
               P("3. Eligible regions", docs.H2),
               P("The tourism regions in Schedule 1 other than Westhaven are eligible."),
               P("4. Which regions are funded", docs.H2),
               P("The Commission ranks the eligible regions on their visitor spending per resident in 2026 and funds the five "
                 "highest. Where two regions are level to the dollar, the region with the smaller population ranks higher."),
               P("A region's visitor spending per resident is its visitor spending in the 2026 calendar year divided by its "
                 "estimated resident population at 30 June 2026."),
               P("Visitor spending is what visitors spend in person at the region's merchants on cards issued in Australia. "
                 "A visitor has the meaning the International Recommendations for Tourism Statistics 2008 give it. The "
                 "Commission estimates visitor spending from the %s research sample for 2026, raising each sampled card "
                 "by its selection weight." % SCHEME),
               P("A region's estimated resident population is the statistics office's preliminary estimate for 30 June 2026 "
                 "summed over the region's statistical areas level 2 under Schedule 1. An area the schedule shares between two "
                 "regions counts towards each at its share."),
               P("5. Timetable", docs.H2),
               P("The Commission's board adopts the round on 18 February 2027. Funding agreements are signed by 30 April "
                 "2027 and the projects are finished by 30 June 2029."),
               P("Schedule 1. Tourism regions", docs.H2),
               P("Each region is made up of the statistical areas level 2 in the statistical areas level 3 listed against "
                 "it, except where the second column shares an area level 2 with another region.", docs.SMALL),
               Spacer(1, 4)]
        rows = [["Region", "Code", "Statistical areas level 3", "Shared areas level 2"]]
        sa3_by_reg = {}
        for x in sa2s:
            sa3_by_reg.setdefault(x["region"], [])
            if x["sa3_name"] not in sa3_by_reg[x["region"]]:
                sa3_by_reg[x["region"]].append(x["sa3_name"])
        for reg in CODES:
            sh = []
            for x in sa2s:
                if x["sa2_name"] in SHARED and reg in SHARED[x["sa2_name"]]:
                    sh.append("%s (%s): %d per cent" % (x["sa2_name"], x["sa2"], round(SHARED[x["sa2_name"]][reg] * 100)))
            rows.append([Paragraph(NAME[reg], docs.SMALL), reg, Paragraph(", ".join(sa3_by_reg.get(reg, [])) or "none", docs.SMALL),
                         Paragraph("; ".join(sh) if sh else "", docs.SMALL)])
        out.append(docs.table(rows, (36, 14, 70, 54)))
        return out
    docs.pdf(path, "Regional Visitor Infrastructure Fund: guidelines for the 2027 round", COMMISSION, story,
             "Tourism Commission  |  Regional Visitor Infrastructure Fund  |  Guidelines, 2027 round",
             dt.datetime(2026, 11, 9, 5, 26, 0))


def program_files(T, agreements, claims, payments, receipts, rng):
    abns = {c[0]: abn(rng) for c in COUNCILS}
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Agreements"
    ws.append(["Regional Tourism Infrastructure Program: agreements at 31 December 2026"])
    ws.append([])
    hdr = ["Agreement", "Round", "Council", "Region", "Project", "Approved ($)", "Signed", "Status",
           "Acquitted or withdrawn", "Final cost ($)", "Paid to 31 Dec 2025 ($)"]
    ws.append(hdr)
    for a in sorted(agreements, key=lambda a: (a["round"], a["agreement"])):
        ws.append([a["agreement"], a["round"], a["council"], NAME[a["region"]], a["project"], a["approved"], a["signed"],
                   a["status"], a["acquitted"], a["final_cost"], a["paid_before"]])
    for row in ws.iter_rows(min_row=4):
        for cell in row:
            if isinstance(cell.value, dt.date):
                cell.number_format = "dd/mm/yyyy"
            elif cell.column in (6,):
                cell.number_format = "#,##0"
            elif cell.column in (10, 11):
                cell.number_format = "#,##0.00"
    ws["A1"].font = Font(bold=True)
    for col, wd in zip("ABCDEFGHIJK", (15, 7, 32, 22, 38, 12, 11, 11, 13, 13, 16)):
        ws.column_dimensions[col].width = wd
    docs.save_xlsx(wb, os.path.join(T, "rtip_agreements_2026-12-31.xlsx"), "Grants management system",
                   dt.datetime(2027, 1, 4, 22, 31, 52), dt.datetime(2027, 1, 4, 22, 31, 52), COMMISSION)
    with open(os.path.join(T, "rtip_claims_2026.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["claim_no", "agreement", "council", "milestone", "claimed_aud", "approved_aud", "approved_on"])
        for c in sorted(claims, key=lambda c: (c["approved_on"], c["claim"])):
            w.writerow([c["claim"], c["agreement"], c["council"], c["milestone"], "%.2f" % c["claimed"], "%.2f" % c["approved_amt"],
                        c["approved_on"].strftime("%d/%m/%Y")])
    with open(os.path.join(T, "ap_payments_rtip_2026.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["payment_id", "payment_run", "paid_on", "payee", "payee_abn", "amount_aud", "agreement_ref"])
        for p_ in payments:
            w.writerow([p_["payment"], p_["run"], p_["paid_on"].isoformat(), p_["payee"], abns[p_["payee"]], "%.2f" % p_["amount"], p_["ref"]])
    styles = {}
    for name, reg, first in COUNCILS:
        short = name.replace("Council", "").replace("Shire of", "").replace("City of", "").replace("Regional", "RC").replace("Shire", "SC").replace("City", "CC").strip().upper()
        styles[name] = rng.choice(["%s RTIP REFUND", "REFUND RTIP %s", "%s GRANT REFUND", "RTIP RETURN %s"]) % short
    with open(os.path.join(T, "ar_receipts_rtip_2026.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["receipt_no", "receipted_on", "payer", "payer_abn", "amount_aud", "payer_reference"])
        for r in receipts:
            w.writerow([r["receipt"], r["on"].isoformat(), r["payer"], abns[r["payer"]], "%.2f" % r["amount"], styles[r["payer"]]])
    return abns


def closure(T):
    path = os.path.join(T, "rtip_closure_decision_2026.pdf")

    def story():
        P = lambda t, s=docs.BODY: Paragraph(t, s)
        return [P("Regional Tourism Infrastructure Program", docs.H1),
                P("Closure of the program", docs.H2),
                P("Decision of the board of the %s, 21 October 2026. Secretary to the board: %s." % (COMMISSION, PEOPLE["ceo"]), docs.META),
                Spacer(1, 6),
                P("The board decided:"),
                P("1. The Regional Tourism Infrastructure Program closes on 31 December 2026. No round opens after the 2025 round."),
                P("2. An agreement acquitted or withdrawn on or before 31 December 2026 ends with the program."),
                P("3. An agreement still open on 31 December 2026 passes to the Regional Visitor Infrastructure Fund, which pays "
                  "what remains of it out of the Fund's 2027 round as the agreement provides. What remains of an agreement is its "
                  "approved amount less what the program had paid on it by 31 December 2026."),
                P("4. Money a council returned to the program in 2026 because it did not spend it is added to the Fund's 2027 round."),
                P("5. The Fund's 2027 round is therefore its 2027 appropriation, plus the unspent money councils returned to the "
                  "program in 2026, less what remains of the agreements the Fund takes over."),
                P("6. Councils with open agreements are told of the transfer by 30 November 2026. Their claims continue to be "
                  "lodged in the grants management system, and finance continues to pay them each week until the transfer.")]
    docs.pdf(path, "Regional Tourism Infrastructure Program: closure", COMMISSION, story,
             "Tourism Commission  |  Board decision  |  21 October 2026", dt.datetime(2026, 10, 21, 5, 14, 0))
