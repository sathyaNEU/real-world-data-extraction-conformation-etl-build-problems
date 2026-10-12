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


def render(f):
    call, comp, st, ru = f["call"], f["components"], f["steps"], f["rules"]
    hm = call["hours_by_month"]
    hu = st["hours_by_month_unrounded"]
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Banking, Credit & Financial Risk (deposit liquidity behaviour: term deposit retention at "
               "maturity).")
    out.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**We should book %s agent-hours with Harbourline for the %s term deposits on the January to March 2027 "
               "maturity list: %s for the deposits maturing in January, %s for February and %s for March.**" % (
                   call["booking_hours"], st["listed_deposits"], hm["January"], hm["February"], hm["March"]))
    out.append("About %s per cent of the list's expected %s conversations will go to the %s-minute retention offer, "
               "against %s per cent across the seven closed campaigns, because %s of the deposits are four-year "
               "deposits at %s per cent reinvesting at the %s per cent four-year card, a drop of %s points. Not the "
               "hours from the past share of conversations that went to the retention offer, pooled, from the latest "
               "campaign or by term, which is the share of deposits that met smaller drops (the past four-year "
               "deposits had locked in low rates). Not the share by each deposit's locked rate, which past deposits at "
               "that rate earned on smaller drops.\n" % (
                   comp["retention_share_pct"], comp["expected_conversations"], ru["minutes_retention"],
                   comp["past_pooled_share_pct"], comp["deposits_at_5_65_four_year"], comp["locked_rate_pct"],
                   comp["card_four_year_pct"], comp["drop_points"]))
    out.append("## 2. Critical Components\n")
    out.append("1. **%s** of the %s listed deposits have no callable number once the holders' numbers are washed "
               "against the do-not-call register at the cut, and are not released." % (
                   comp["no_callable_number"], st["listed_deposits"]))
    out.append("2. **%s** deposits on the list are four-year deposits at **%s per cent** that reinvest at the **%s per "
               "cent** four-year card for January to March 2027, a drop of **%s points**; in the seven closed "
               "campaigns **%s per cent** of conversations at drops of %s points or more went to the retention offer."
               % (comp["deposits_at_5_65_four_year"], comp["locked_rate_pct"], comp["card_four_year_pct"],
                  comp["drop_points"], comp["past_share_at_2_5_or_more_pct"], st["drop_threshold_points"]))
    out.append("3. About **%s per cent** of the list's expected **%s** conversations go to the retention offer, "
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
        "Took each past conversation's drop, the rate on its deposit's row in %s or %s less the reinvestment rate for "
        "its term in the quarter's campaign brief PDF: the share that went to the retention offer (RTK, RTW) rises "
        "with the drop in every campaign and every term, from %s per cent where the rate rose to %s per cent at drops "
        "of %s points or more, %s per cent overall." % (
            W.F_LISTS_2025, W.F_LISTS_2026, st["past_share_negative_drop_pct"],
            comp["past_share_at_2_5_or_more_pct"], st["drop_threshold_points"], comp["past_pooled_share_pct"]),
        "Read each listed deposit's drop against the rates in %s (four years %s per cent) and gave it the past share "
        "of conversations in its %s-point band of drop: %s deposits at %s per cent meet a drop of %s points, and about "
        "%s per cent of the %s conversations go to the retention offer." % (
            W.brief_name(W.FWD), comp["card_four_year_pct"], st["band_points"], comp["deposits_at_5_65_four_year"],
            comp["locked_rate_pct"], comp["drop_points"], comp["retention_share_pct"], comp["expected_conversations"]),
        "Priced the list at schedule 2 of %s, %s minutes per dial that does not reach the holder, %s per conversation "
        "and %s per retention-offer conversation: %s agent-hours, %s for January maturities, %s for February and %s "
        "for March." % (W.F_SOW, ru["minutes_not_reached"], ru["minutes_conversation"], ru["minutes_retention"],
                        st["hours_unrounded"], hu["January"], hu["February"], hu["March"]),
        "Counted each listed deposit of the seven campaigns (account numbers without punctuation) as still on term "
        "deposit when %s shows a REINVEST on its own account on its maturity date, or %s shows its maturity proceeds "
        "paid that day into an account the events extract shows opened that day, with no BREAK or CLOSE on that "
        "account in the %s days after maturity, taking its principal or the amount transferred: the counts and "
        "principal in block 4." % (W.F_EVENTS, W.F_TRANSFERS, ru["days_after_maturity"]),
        "Summed the principal in %s maturing in each month once per account, added the certificates in %s maturing in "
        "the month that %s does not show as MIGRATED, and took off the list's principal for the month: the amounts in "
        "block 4." % (W.F_HOLDINGS, W.F_KIP, W.F_BATCHES),
        "Rounded once, as the retention procedure books: %s agent-hours, %s for January, %s for February and %s for "
        "March." % (call["booking_hours"], hm["January"], hm["February"], hm["March"]),
    ]
    for i, s in enumerate(steps, 1):
        out.append("%d. %s" % (i, s))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### td_booking_q1_2027.xlsx\n")
    out.append("1. Agent-hours to book with Harbourline for the January to March 2027 list: %s" % call["booking_hours"])
    out.append("2. Agent-hours for the deposits maturing in each month:")
    for m in MONTHS:
        out.append("   - %s 2027: %s" % (m, hm[m]))
    out.append("3. Deposits on each campaign's list still on term deposit with the Society 30 days after maturity, and "
               "their principal:")
    for q in W.PAST:
        a = f["ask_a"][q]
        out.append("   - %s: %s deposits, NZ$%s" % (a["campaign"], a["deposits"], a["principal_nzd"]))
    out.append("4. Principal on term deposits and investment certificates maturing across all members, and the part "
               "not on the list:")
    for m in MONTHS:
        b = f["ask_b"][m]
        out.append("   - %s 2027: maturing NZ$%s, not on the list NZ$%s" % (m, b["maturing_nzd"], b["not_on_list_nzd"]))
    out.append("")
    out.append("### td_booking_note_q1_2027.docx\n")
    out.append("1. Opens with the booking: %s agent-hours, %s for January maturities, %s for February and %s for "
               "March." % (call["booking_hours"], hm["January"], hm["February"], hm["March"]))
    out.append("2. Stacked bar chart of the agent-hours by maturity month, January, February and March 2027, each bar "
               "labelled with its hours to book (%s, %s and %s) and split into dials that do not reach the holder, "
               "conversations and the retention offer's further minutes." % (hm["January"], hm["February"],
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
