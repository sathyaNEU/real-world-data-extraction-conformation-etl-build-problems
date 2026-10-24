# Assembles Submission New Spec.md for v2 from the v1 file: blocks 3 and 5 and steps 1 to 8 are carried over byte for byte.
# Usage: python3 -I spec.py <v1 spec> <prompt_v2.txt> <figures.json> <out>
import json, re, sys
v1 = open(sys.argv[1], encoding="utf-8").read()
prompt = open(sys.argv[2], encoding="utf-8").read().rstrip("\n")
F = json.load(open(sys.argv[3], encoding="utf-8"))
blocks = v1.split("```")
assert len(blocks) == 13
head = blocks[0].replace("mail_test_2027.xlsx (workbook)", "julbrevet_2028_plan.xlsx (workbook)") \
               .replace("mail_test_chart.png (visual); visual: mail_test_chart.png",
                        "julbrevet_reach_2028.png (visual); visual: julbrevet_reach_2028.png")
steps_v1 = blocks[11].strip("\n").split("\n")
assert steps_v1[8].startswith("9. Deliver the three files")
n = lambda x: f"{x:,}"
k = lambda x: f"{x:,.1f}"
G, V = "Gävleborg", "Västernorrland"
supp = [
    "julbrevet_2028_plan.xlsx, sheet of the Julbrevet card offers (purchases paid on the receipts that redeemed the offer, 1 to 24 December 2027, thousand SEK):",
    f"1. BV27-13-O1 Julskinka 25 % billigare, Stor stores: {k(F['A|O1|Stor'])}",
    f"2. BV27-13-O1, Mellan stores: {k(F['A|O1|Mellan'])}",
    f"3. BV27-13-O1, Nära stores: {k(F['A|O1|Nära'])}",
    f"4. BV27-13-O2 50 kr rabatt vid köp över 700 kr, Stor stores: {k(F['A|O2|Stor'])}",
    f"5. BV27-13-O2, Mellan stores: {k(F['A|O2|Mellan'])}",
    f"6. BV27-13-O2, Nära stores: {k(F['A|O2|Nära'])}",
    "julbrevet_2028_plan.xlsx, sheet of the households mailed the Julbrevet in 2027 by county and by the channels that could still send them the 2028 Julbrevet:",
]
i = 7
for c in [G, V]:
    for g, label in [("email", "by email"), ("sms_push_only", "by SMS or app push but not by email"), ("none", "by none of the three")]:
        supp.append(f"{i}. {c}, {label}: {n(F[f'B|{c}|{g}'])} households")
        supp.append(f"{i + 1}. {c}, {label}: {k(F[f'C|{c}|{g}'])} thousand SEK paid on the receipts on which a card registered to those households redeemed a Julbrevet card offer")
        i += 2
supp += [
    "julbrevet_mail_call.docx:",
    f"{i}. Opens with the call to drop addressed Julbrevet mail from the 2028 plan, with December purchases per household of 2,298.58 SEK mailed against 2,161.36 SEK control, 137.21 SEK of incremental purchases per piece with a 90 percent range of minus 56.99 to 331.42 SEK, and a lower-end margin of minus 14.25 SEK per piece against the 11.40 SEK piece cost; then a miss of 25.65 SEK per piece, 239.81 SEK per piece the test would have needed to show, and 1,942 control households.",
    f"{i + 1}. Mailed households none of the three channels could still send the 2028 Julbrevet to: {n(F['M|none|households'])}.",
    f"{i + 2}. What those households paid on their Julbrevet card offer receipts: {k(F['M|none|paid'])} thousand SEK.",
    "julbrevet_reach_2028.png:",
    f"{i + 3}. Bars of the mailed households for each county in the three groups: {G} {n(F[f'B|{G}|email'])} by email, {n(F[f'B|{G}|sms_push_only'])} by SMS or app push only, {n(F[f'B|{G}|none'])} by none; {V} {n(F[f'B|{V}|email'])}, {n(F[f'B|{V}|sms_push_only'])} and {n(F[f'B|{V}|none'])}.",
]
steps = steps_v1[:8] + [
    "9. Card offers. Take the BV27-13-O1 and BV27-13-O2 receipts of the POS export (all dated 1 to 24 December) and the format of the store where each was rung from stores.csv, on the BI warehouse's basis the prompt sets (spend_sek, the amount paid after offer discounts, the table the guidance takes purchases from). The POS receipt totals equal that basis at every store except BV113, BV115, BV118, BV125, BV128, BV132 and BV141, whose totals from late October 2027 on exceed it by exactly the discount on every member, store and month whose receipts all redeemed an offer (643 of 643 in December). The discount is taken off there, giving O1 "
    + f"{k(F['A|O1|Stor'])}, {k(F['A|O1|Mellan'])} and {k(F['A|O1|Nära'])} and O2 {k(F['A|O2|Stor'])}, {k(F['A|O2|Mellan'])} and {k(F['A|O2|Nära'])} thousand SEK paid for Stor, Mellan and Nära. [supplementary: card offers]",
    "10. Reach. Take the 14,108 BV27-13-D1 households by the county of their postcode area (postcode_areas.csv) and replay each channel's consent to 1 January 2028 00:00 Swedish time (31 December 23:00 UTC) on the accounts open at the end of 2027. Email leaves out the addresses on the email platform's suppression list, which keeps every address that ever hard-bounced (contact policy, section 7): the 238 members who hard-bounced in 2027, and the 252 whose addresses bounced before 2027, seen as the members who held email consent at one or more 2027 newsletter releases yet were sent no 2027 email (at every one of the 26 newsletters the consented open members not sent are exactly the earlier 2027 hard bounces and these members). The 11 members whose consent came after the last 2027 mailing stay in. SMS takes every consented account. App push needs a sign-in to the app and leaves out the 677 members whose last three notifications failed, whose tokens the January clean-up removes (runbook 5.2). "
    + f"Households by email, by SMS or app push only, and by none: {G} {n(F[f'B|{G}|email'])}, {n(F[f'B|{G}|sms_push_only'])} and {n(F[f'B|{G}|none'])}; {V} {n(F[f'B|{V}|email'])}, {n(F[f'B|{V}|sms_push_only'])} and {n(F[f'B|{V}|none'])}. [supplementary: households by group, chart]",
    "11. Purchases by group. Sum the amounts paid from step 9 on the Julbrevet offer receipts of every account registered to each group's households: "
    + f"{G} {k(F[f'C|{G}|email'])}, {k(F[f'C|{G}|sms_push_only'])} and {k(F[f'C|{G}|none'])}; {V} {k(F[f'C|{V}|email'])}, {k(F[f'C|{V}|sms_push_only'])} and {k(F[f'C|{V}|none'])} thousand SEK. The {n(F['M|none|households'])} households none of the three channels could send to paid {k(F['M|none|paid'])} thousand SEK. [supplementary: purchases by group, memo close]",
    "12. Deliver the three files: the workbook with the card offers sheet and the reach sheet, the short Word memo opening with the call and its figures and closing with the households no channel could send to and what they paid on Julbrevet offer receipts, and the PNG of the mailed households by county and group.",
]
blocks[1] = "\n" + prompt + "\n"
blocks[7] = "\n" + "\n".join(supp) + "\n"
blocks[11] = "\n" + "\n".join(steps) + "\n"
blocks[0] = head
tail = blocks[12].replace("mail_test_2027.xlsx, julbrevet_mail_call.docx, mail_test_chart.png",
                          "julbrevet_2028_plan.xlsx, julbrevet_mail_call.docx, julbrevet_reach_2028.png")
blocks[12] = tail
out = "```".join(blocks)
assert "\u2014" not in out and "\u2013" not in out
open(sys.argv[4], "w", encoding="utf-8").write(out)
# frozen blocks carried byte for byte
b1 = v1.split("```"); b2 = out.split("```")
assert b1[5] == b2[5] and b1[9] == b2[9] and b1[3] == b2[3], "recommendation, critical components and distractor carried over"
assert b2[11].strip("\n").split("\n")[:8] == steps_v1[:8]
assert b2[1].split("\n\n")[0].strip("\n") == b1[1].split("\n\n")[0].strip("\n")
print("spec written; frozen blocks identical")
