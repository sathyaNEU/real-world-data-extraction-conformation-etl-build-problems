# Assembles Submission New Spec.md from the v1 file: blocks 3 and 5 and steps 1 to 8 are carried over byte for byte.
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
FORMATS, WEEKS = ["Stor", "Mellan", "Nära"], [48, 49, 50, 51]
supp = ["julbrevet_2028_plan.xlsx, sheet 1 (BV27-13-O2 receipts of 1 to 24 December 2027 with a basket under 750 SEK before the 50 kr discount, amounts as the BI warehouse counts purchases):"]
i = 1
for f in FORMATS:
    supp.append(f"{i}. {f} stores: {n(F[f'F|{f}|receipts'])} receipts")
    supp.append(f"{i + 1}. {f} stores: {k(F[f'F|{f}|paid'])} thousand SEK paid on them")
    i += 2
supp.append("julbrevet_2028_plan.xlsx, sheet 2 (the same receipts by ISO week):")
for w in WEEKS:
    supp.append(f"{i}. Week {w}: {n(F[f'W|{w}|receipts'])} receipts")
    supp.append(f"{i + 1}. Week {w}: {k(F[f'W|{w}|paid'])} thousand SEK paid on them")
    i += 2
bars = "; ".join(f"week {w} {n(F[f'W|{w}|receipts'])} (" + ", ".join(f"{f} {n(F[f'C|{w}|{f}'])}" for f in FORMATS) + ")" for w in WEEKS)
supp += [
    "julbrevet_mail_call.docx:",
    f"{i}. Opens with the call to drop addressed Julbrevet mail from the 2028 plan.",
    f"{i + 1}. Closes with the total number of those receipts: {n(F['M|receipts'])}.",
    f"{i + 2}. Closes with the total paid on them: {k(F['M|paid'])} thousand SEK.",
    "julbrevet_reach_2028.png:",
    f"{i + 3}. Bars of the receipts in each ISO week split by store format: {bars}.",
]
steps = steps_v1[:8] + [
    "9. Workbook. Take every BV27-13-O2 redemption in the POS export (all dated 1 to 24 December, each 50 SEK off), the format of its store from stores.csv and the ISO week of redeemed_at, with amounts counted as the BI warehouse counts purchases (spend_sek, after offer discounts). 1,415 of the 2,841 O2 redemptions are written under BV27-13-O1: they are the O1 rows giving exactly 50 SEK off a basket over 700 SEK, the O2 terms, and each of the 219 accounts with two O1 rows, which the till's once-for-each-member rule (runbook 7.3) rules out, has one of them, while no other account redeems any offer twice. At BV101, BV104, BV106, BV110, BV113, BV114, BV115, BV118, BV119, BV128, BV129, BV132, BV138 and BV141 the POS receipt total is the amount before the discount: on every member, store and month whose receipts all redeemed an offer it exceeds spend_sek by exactly the discount (1,315 of 1,315 such months in December), while every other store's total equals spend_sek (671 of 671 in December). With both handled, the receipts with a basket under 750 SEK before the discount are "
    + ", ".join(f"{f} {n(F[f'F|{f}|receipts'])}" for f in FORMATS) + " (" + ", ".join(k(F[f'F|{f}|paid']) for f in FORMATS) + " thousand SEK paid) and weeks 48 to 51 "
    + ", ".join(n(F[f'W|{w}|receipts']) for w in WEEKS) + " (" + ", ".join(k(F[f'W|{w}|paid']) for w in WEEKS) + " thousand SEK). [supplementary: both sheets, memo, chart]",
    f"10. Deliver the workbook with the two sheets, the short Word memo opening with the call and closing with {n(F['M|receipts'])} receipts and {k(F['M|paid'])} thousand SEK, and the PNG of the receipts per ISO week split by store format.",
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
assert "\n\n" not in b2[1].strip("\n"), "the prompt is one paragraph"
print("spec written; frozen blocks identical")
