"""submission.md, emitted from generator/figures.json: every figure in blocks 1 to 4 is read from the file the build
wrote, never typed."""
import json
import os

import analysis as A

QLAB = {"FQ1": "Jul-Sep 2025", "FQ2": "Oct-Dec 2025", "FQ3": "Jan-Mar 2026", "FQ4": "Apr-Jun 2026"}


def money(x):
    return "${:,}".format(int(x))


def write(task_dir):
    here = os.path.join(task_dir, "generator")
    f = json.load(open(os.path.join(here, "figures.json")))
    classes = [c for c in A.CLASS_ORDER]
    picks = {c: f["call." + c] for c in classes}

    def members_of(c):
        return sorted([k.split(".", 1)[1] for k in f if k.startswith("net.") and f.get("class." + k.split(".", 1)[1]) == c],
                      key=lambda b: f["net_exact." + b])

    def line_for(c):
        bs = members_of(c)
        return ", ".join("%s **%s**" % (b, money(f["net." + b])) for b in bs)

    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics.")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Prefer %s on the 2027 preferred drug list.** Each has its class's lowest fiscal 2026 net cost per 30-day "
             "supply once every manufacturer's remittances are traced to the products that earned them: Velantro %s "
             "against Liraquent %s, Glarvia %s against Deglutra %s and Bevoria %s against Vilaro %s. Not Liraquent, "
             "insulin glargine-qmrt or Saltiva, which lead their classes only when each manufacturer's remittances are "
             "spread over its products by ingredient cost, giving every product its manufacturer's average rebate."
             % (", ".join("%s (%s)" % (picks[c], c) for c in classes[:-1]) + " and %s (%s)" % (picks[classes[-1]],
                                                                                          classes[-1]),
                money(f["net.Velantro"]), money(f["net.Liraquent"]), money(f["net.Glarvia"]), money(f["net.Deglutra"]),
                money(f["net.Bevoria"]), money(f["net.Vilaro"])))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("Net cost per 30-day supply, fiscal 2026:")
    L.append("")
    comp = [["GLP-1 receptor agonists"], ["SGLT2 inhibitors"], ["Long-acting insulins"],
            ["Direct oral anticoagulants", "Inhaled corticosteroid and LABA combinations"], ["Adalimumab products"]]
    for i, grp in enumerate(comp, 1):
        L.append("%d. %s" % (i, "; ".join("%s: %s" % (c, line_for(c)) for c in grp)))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    steps = [
        "Conformed pbm_paid_claims_fy2026.csv: removed every paid claim that a reversal row names in reversal_of, read "
        "both NDC and date layouts, and mapped group codes %s, %s, %s and %s to the accounts' new codes." %
        tuple(f["group_codes"]),
        "Took each compared product's ingredient cost paid and its 30-day supplies (quantity over the 30-day quantity "
        "in clinical_review_2027_pdl.pdf) on its fiscal 2026 claims, per policy EB-RX-04.",
        "Read the five rebate_remittance statements and assigned every current quarter and prior period line to its "
        "quarter of service and plan account, leaving out the lines for fiscal 2025 service.",
        "For each manufacturer, fitted its fiscal 2026 remittances per account and quarter of service on the 30-day "
        "supplies of every product it supplies in the same account and quarter (least squares; the fit is exact to the "
        "cent), giving each product's rebate per 30-day supply and its fiscal 2026 rebates.",
        "Divided each product's ingredient cost less its rebates by its 30-day supplies, giving the net costs in block "
        "2.",
        "Counted fiscal 2026 brand claims (compound claims out) by quarter of service and by the pharmacy's network on "
        "the date of service per Exhibit C, a claim carrying the retail dispensing fee as retail (the three hospital "
        "outpatient pharmacies that pharmacy_network_202610.txt lists as specialty were retail until 1 May 2026), "
        "priced them at Exhibit C's rates and set them against every remittance line for that quarter's service."
        "Matched each claim before 1 January 2026 to member_roster_20261009.csv through the subscriber's "
        "legacy_cardholder_id and the member's birth date and gender, and counted the distinct members with a paid "
        "claim in each class under each account.",
        "Preferred the product with the lowest net cost per 30-day supply in each class, per the policy.",
    ]
    for i, s in enumerate(steps, 1):
        L.append("%d. %s" % (i, s))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### pdl_2027_net_cost.xlsx")
    L.append("")
    L.append("1. Net cost per 30-day supply, fiscal 2026, to the nearest ten dollars:")
    for c in classes:
        for b in members_of(c):
            L.append("   - %s: %s %s%s" % (c, b, money(f["net." + b]), ", preferred" if picks[c] == b else ""))
    L.append("2. Preferred product for 2027:")
    for c in classes:
        L.append("   - %s: %s" % (c, picks[c]))
    L.append("3. Rebate guarantee by fiscal 2026 quarter (brand claims by channel, guarantee, rebates remitted for the "
             "quarter's claims, shortfall):")
    for k in ["FQ1", "FQ2", "FQ3", "FQ4"]:
        sf = f["guar.%s.shortfall" % k]
        L.append("   - %s: retail under 84 days {:,} claims, retail 84 days or more {:,}, mail order {:,}, specialty {:,}; "
                 "guarantee %s; remitted %s; %s".format(f["guar.%s.RETAIL30" % k], f["guar.%s.RETAIL90" % k],
                                                         f["guar.%s.MAIL" % k], f["guar.%s.SPECIALTY" % k])
                 % (QLAB[k], money(f["guar.%s.guarantee" % k]), money(f["guar.%s.remitted" % k]),
                    "shortfall %s" % money(sf) if sf > 0 else "no shortfall"))
    L.append("4. Members with a paid claim in each reviewed class, by employer account:")
    for c in classes:
        L.append("   - %s: %s" % (c, ", ".join("%s %s" % (a, "{:,}".format(f["members.%s.%s" % (c, a)]))
                                             for a in A.ACC_ORDER)))
    L.append("")
    L.append("### pdl_2027_trustees.pptx")
    L.append("")
    L.append("1. Slide 1 names the preferred product in each class with its net cost per 30-day supply and the next "
             "lowest product.")
    L.append("2. Slide 2 charts every compared product's net cost per 30-day supply by class, the preferred product's "
             "bar in green, adalimumab products on their own scale.")
    L.append("")
    open(os.path.join(task_dir, "submission.md"), "w").write("\n".join(L))
