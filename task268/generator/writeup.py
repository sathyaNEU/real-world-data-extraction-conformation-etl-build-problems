"""submission.md, drafted from the figures the golden computed (figures.json): tags, the recommendation, the critical
components, the steps and the deliverable answers."""
import common as K

RN = K.BRAND_NAME


def _n(x):
    return "{:,}".format(int(x))


def write(R, F):
    ov = R["overlap"]
    call, runner = R["call"], R["runner"]
    rows = sorted(K.RIVALS, key=lambda b: ov[b][2])
    wes = "WES"
    L = []
    L += ["## Tags", "",
          "**Domain:** Marketing & Consumer Research (segmentation and market structure).",
          "**Analytical objective:** Descriptive & Distribution Analysis.", ""]
    L += ["## 1. Final Recommendation", "",
          "**The 2027 Roastery sampling goes to %s's homes.**" % RN[call],
          "",
          "Of the %s homes that bought %s in 2026, %s also bought Corcally's Roastery (%d%%), the lowest share of the "
          "rivals and %d points under %s (%d%%). Not %s, the least overlapped rival read card by card (%d%%), because "
          "its capsule buyers are mostly a home's second card while another member buys the Roastery. Not %s, whose "
          "homes buy their Roastery through the online shop (%d%%)." % (
              _n(ov[call][0]), RN[call], _n(ov[call][1]), F["call_share"], F["gap_points"], RN[runner],
              F["runner_share"], RN[R["default"][0]], F["default_share"], RN[wes], F["rivals"][RN[wes]]["share"]), ""]
    L += ["## 2. Critical Components", "",
          "1. %s: **%s** buying homes, **%s** of them also bought the Roastery, **%d%%**." % (
              RN[call], _n(ov[call][0]), _n(ov[call][1]), F["call_share"]),
          "2. Runner-up %s: **%s** buying homes, **%s** also bought the Roastery, **%d%%**." % (
              RN[runner], _n(ov[runner][0]), _n(ov[runner][1]), F["runner_share"]),
          "3. Gap between them: **%d points**." % F["gap_points"], ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Mapped each PLU in coffee_till_lines_2026.csv to its brand through product_master_coffee.xlsx (one "
          "brand per supplier and range, its spellings folded), kept the 2026 pack lines on Rewards cards, dropped the "
          "cards rewards_cards_2026.csv types STORE and folded each REPLACED card into its replaced_by card.",
          "2. Matched every card-paid receipt to its SALE row in faircourt_settlement_2026.parquet on terminal "
          "(faircourt_merchant_agreement_2026.pdf, Schedule 2, by installed and removed dates), amount and time "
          "(txn_time_utc converted to Irish time, the row up to two minutes before the receipt): %s receipts, one row "
          "each." % _n(F["receipts_matched"]),
          "3. Took each online order in online_orders_2026.json delivered in 2026, its last version's coffee lines, and "
          "its card_ref from the settlement row whose merchant_ref is the order number.",
          "4. Joined the Rewards cards and online accounts that share a card_ref into homes (%s homes bought coffee), "
          "and for each rival counted the homes that bought it and those that also bought Roastery packs: %s lowest at "
          "%d%%, %s next at %d%%." % (_n(F["homes_total"]), RN[call], F["call_share"], RN[runner], F["runner_share"]),
          "5. Counter: matched each label in counter_scale_labels_2026.csv to a SALE on terminal %s (labels printed in "
          "the 25 minutes before, plus accessories at coffee_counter_price_board_2026.pdf prices) or to a COUNTER "
          "COFFEE LOOSE till line of its price; scale 2's labels %s to %s, printed under January dates, re-dated by the "
          "offset that lines them up with those payments; S2 weights read as grams; unpaid labels left out." % (
              K.COUNTER_TID, F["clock_block"][0], F["clock_block"][1]),
          "6. Funding: each MULTIBUY SAVING line in a deal's dates at the multibuy_deals_2026.xlsx rate in force on the "
          "sale day, each reversal netted against the receipt its refund cites, and each MULTIBUY ADJ line added at the "
          "date of the receipt its note cites, one multibuy per missed pair on that receipt.",
          "7. The sampling goes to %s's homes." % RN[call], ""]
    L += ["## 4. Deliverable Answers", "", "### %s" % K.DECK, "",
          "1. The 2027 sampling goes to %s's homes." % RN[call],
          "2. Bar chart on slide 2 of every rival's share of buying homes that also bought the Roastery, lowest first, "
          "%s highlighted." % RN[call],
          "3. Runner-up %s at %d%%; gap %d points." % (RN[runner], F["runner_share"], F["gap_points"]),
          "4. Loose coffee the Drumsallagh counter sold, kilograms to one decimal:"]
    for rid, name, _ in K.ROASTERS:
        L.append("   - %s: Q1 %.1f, Q2 %.1f, Q3 %.1f, Q4 %.1f" % ((name,) + tuple(R["ask_a"][(name, q)] for q in (1, 2, 3, 4))))
    L.append("5. Multibuy funding owed by each supplier, whole euros:")
    for sp in sorted(set(k[0] for k in R["ask_b"])):
        L.append("   - %s: Q1 %s, Q2 %s, Q3 %s, Q4 %s" % ((sp,) + tuple(_n(round(R["ask_b"][(sp, q)])) for q in (1, 2, 3, 4))))
    L += ["", "### %s" % K.CSV_OUT, "", "1. One row per rival, lowest share first, whole numbers and whole per cents:"]
    for b in rows:
        L.append("   - %s: %s buying homes, %s also bought the Roastery, %d%%" % (
            RN[b], _n(ov[b][0]), _n(ov[b][1]), int(round(ov[b][2]))))
    L.append("")
    return "\n".join(L), {}
