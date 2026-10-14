"""Write task137/submission.md from generator/figures.json: every figure in blocks 1 to 4 is emitted by the generator,
none typed."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import world as W  # noqa: E402

MONTHS = ("January", "February", "March")


def listing(items):
    return ", ".join(items[:-1]) + " and " + items[-1] if len(items) > 1 else items[0]


def render(f):
    call, comp, st, ru, b = f["call"], f["components"], f["steps"], f["rules"], f["ask_b"]
    hm = call["hours_by_month"]
    hu = st["hours_by_month_unrounded"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Banking, Credit & Financial Risk (deposit liquidity behaviour: term deposit retention at "
               "maturity).")
    out.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**We should book %s agent-hours with Harbourline for the %s term deposits on the %s "
               "maturity list: %s for the deposits maturing in January, %s for February and %s for March.**" % (
                   call["booking_hours"], st["listed_deposits"], call["quarter"], hm["January"], hm["February"],
                   hm["March"]))
    out.append("About %s per cent of the list's expected %s conversations will go to the %s-minute retention offer, "
               "against %s per cent across the seven closed campaigns, because %s of the deposits are money the "
               "%s-year special of %s won at %s per cent, and at its first maturity money a special won "
               "went to the retention offer in %s per cent of conversations, much the same at every drop it met. Not the "
               "past share at the same drop from the deposit's rate to the rate it reinvests at: at drops of %s to %s "
               "points, where the special's %s-point drop to the %s per cent %s-year rate falls, almost every past "
               "conversation was about other deposits, which went to the offer at %s per cent. Not the pooled share, the "
               "latest campaign's, a trend, the share by term or by locked rate: each carries other deposits' share onto "
               "a list that is mostly the special's money.\n" % (
                   comp["retention_share_pct"], comp["expected_conversations"], ru["minutes_retention"],
                   comp["past_pooled_share_pct"], comp["special_deposits"], comp["special_term_years"],
                   comp["special_opened"], comp["special_rate_pct"], comp["past_special_share_pct"],
                   st["band_from_points"],
                   st["band_to_points"], comp["drop_points"], comp["card_pct"], comp["special_term_years"],
                   comp["past_band_member_share_pct"]))
    out.append("## 2. Critical Components\n")
    out.append("1. **%s** of the %s listed deposits have no callable number once the holders' numbers are washed "
               "against the do-not-call register at the cut, and are not released." % (
                   comp["no_callable_number"], st["listed_deposits"]))
    out.append("2. **%s** deposits on the list are %s-year deposits opened at the **%s per cent** special in %s (the "
               "list's other %s-year deposits of that quarter from %s per cent); they reinvest at the **%s per cent** "
               "%s-year rate, a drop of **%s points**." % (
                   comp["special_deposits"], comp["special_term_years"], comp["special_rate_pct"], comp["special_opened"],
                   comp["special_term_years"], comp["cohort_lowest_rate_pct"], comp["card_pct"],
                   comp["special_term_years"], comp["drop_points"]))
    out.append("3. In the seven closed campaigns **%s per cent** of conversations about money a special won went to the "
               "retention offer, much the same at every drop it met." % comp["past_special_share_pct"])
    out.append("4. About **%s per cent** of the list's expected **%s** conversations go to the retention offer, "
               "against **%s per cent** of the seven campaigns' conversations.\n" % (
                   comp["retention_share_pct"], comp["expected_conversations"], comp["past_pooled_share_pct"]))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Normalised the numbers in %s to E.164 and dropped those on %s as it stood on 2 November 2026 (recorded by then "
        "and not withdrawn by then): %s of the %s deposits on %s have no callable number and, per the retention "
        "procedure, are not released." % (W.F_CONTACTS, W.F_DNC, comp["no_callable_number"], st["listed_deposits"],
                                          W.F_LIST_FWD),
        "Joined %s to %s and %s for every released case of the seven closed campaigns, averaged the dials that did not "
        "reach the holder (NOA, BSY, VML, DIS, WNG) and the chance of a conversation by the mix of the case's callable "
        "number types (how many mobile, home and work numbers), applied them to the list's mixes, and scaled them by "
        "the %s per cent of listed deposits with a callable number that the seven campaigns released (the rest had "
        "given instructions): about %s non-reaching dials and %s conversations." % (
            W.F_RELEASE, W.F_CLOSEOUT, W.F_DIALS, st["release_share_pct"], st["non_reaching_dials"],
            comp["expected_conversations"]),
        "Gave each past conversation its deposit's drop (the rate on its row in %s or %s less the reinvestment rate for "
        "its term in the quarter's campaign brief PDF) and its class: money a special won where the rate stood %s "
        "points or more above the lowest rate of the same list's deposits of its term opened in the same quarter (%s). "
        "Of %s conversations, the %s about special money went to the retention offer (RTK, RTW) at %s per cent, "
        "much the same at every drop they met; the rest far less often, rising with the drop." % (
            W.F_LISTS_2025, W.F_LISTS_2026, st["special_gap_points"], st["past_specials"],
            st["past_conversations"], st["past_special_conversations"], comp["past_special_share_pct"]),
        "Classed the list the same way and read its drops against %s (%s years %s per cent): %s deposits at %s per "
        "cent, against %s for the lowest of their term and quarter, meet a drop of %s points. Each deposit took its "
        "class's past share in its %s-point band of drop (special money at %s to %s points, %s per cent), so about %s "
        "per cent of the %s conversations go to the retention offer." % (
            W.brief_name(W.FWD), comp["special_term_years"], comp["card_pct"], comp["special_deposits"],
            comp["special_rate_pct"], comp["cohort_lowest_rate_pct"], comp["drop_points"], st["band_points"],
            st["band_from_points"], st["band_to_points"], comp["past_band_special_share_pct"],
            comp["retention_share_pct"], comp["expected_conversations"]),
        "Priced the list at schedule 2 of %s, %s minutes per dial that does not reach the holder, %s per conversation "
        "and %s per retention-offer conversation: %s agent-hours, %s for January maturities, %s for February and %s "
        "for March." % (W.F_SOW, ru["minutes_not_reached"], ru["minutes_conversation"], ru["minutes_retention"],
                        st["hours_unrounded"], hu["January"], hu["February"], hu["March"]),
        "For each listed deposit of the seven campaigns (account numbers without punctuation), took its principal when "
        "%s shows a REINVEST on its own account on its maturity date, or otherwise the amounts %s shows the maturity "
        "settlement account paying that day under the deposit's account number in the narrative into accounts the "
        "events extract shows opened that day; either counted only with no BREAK or CLOSE on the account in the %s "
        "days after maturity: the principal and the deposits it came from in block 4." % (
            W.F_EVENTS, W.F_TRANSFERS, ru["days_after_maturity"]),
        "Summed the principal in %s maturing in each month once per account, added the certificates in %s maturing in "
        "the month that are not in the core (not MIGRATED in %s, and matching no core certificate on issue date, "
        "maturity date, rate and term), and took the list's principal off the quarter's total: the amounts in block 4."
        % (W.F_HOLDINGS, W.F_KIP, W.F_BATCHES),
        "Rounded once, as the retention procedure books: %s agent-hours, %s for January, %s for February and %s for "
        "March." % (call["booking_hours"], hm["January"], hm["February"], hm["March"]),
    ]
    for i, s in enumerate(steps, 1):
        out.append("%d. %s" % (i, s))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### td_booking_q1_2027.xlsx\n")
    yr = call["quarter"][-4:]
    out.append("1. Agent-hours to book with Harbourline for the %s list: %s" % (call["quarter"], call["booking_hours"]))
    out.append("2. Agent-hours for the deposits maturing in each month:")
    for m in MONTHS:
        out.append("   - %s %s: %s" % (m, yr, hm[m]))
    out.append("3. Principal on each campaign's list still on term deposit with the Society 30 days after maturity, and "
               "the deposits it came from:")
    for q in W.PAST:
        a = f["ask_a"][q]
        out.append("   - %s: NZ$%s from %s deposits" % (a["campaign"], a["principal_nzd"], a["deposits"]))
    out.append("4. Principal on term deposits and investment certificates maturing across all members:")
    for m in MONTHS:
        out.append("   - %s %s: NZ$%s" % (m, yr, b["maturing_nzd"][m]))
    out.append("   - Not on the list, %s: NZ$%s" % (call["quarter"], b["quarter_not_on_list_nzd"]))
    out.append("")
    out.append("### td_booking_note_q1_2027.docx\n")
    out.append("1. Opens with the booking: %s agent-hours, %s for January maturities, %s for February and %s for "
               "March." % (call["booking_hours"], hm["January"], hm["February"], hm["March"]))
    out.append("2. Stacked bar chart of the agent-hours by maturity month, January, February and March %s, each bar "
               "labelled with its hours to book (%s, %s and %s) and split into dials that do not reach the holder, "
               "conversations and the retention offer's further minutes." % (yr, hm["January"], hm["February"],
                                                                              hm["March"]))
    return "\n".join(out) + "\n"


def main(figures_path=os.path.join(HERE, "figures.json"), out_path=os.path.join(TASK, "submission.md")):
    f = json.load(open(figures_path, encoding="utf-8"))
    text = render(f)
    assert "\u2014" not in text and "\u2013" not in text
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return text


if __name__ == "__main__":
    main()
