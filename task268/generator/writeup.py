"""submission.md from the golden's own run: every figure it states is taken from R and recorded in figures.json."""
import datetime as dt

import common as K

ROUTES = ["Policyholder", "Third party", "Third-party insurer", "Solicitor practice", "Claims management company"]


def fmt(v, d=0):
    return format(v, ",.%df" % d)


def write(R, F):
    f, o = R["freq"]["route"], R["order"]
    G = R["_G"]
    cmc = {}
    for reg in ("Pennine", "Wessex"):
        v = {}
        for ay in list(K.CLOSED) + [K.OPEN_YEAR]:
            pos = G.position(ay)
            v[ay] = int(((pos.region == reg) & (pos.head_of_claim == "TPI") & (pos.route == "Claims management company")).sum())
        cmc[reg] = v
    lo = min(cmc["Pennine"][a] for a in K.CLOSED)
    hi = max(cmc["Pennine"][a] for a in K.CLOSED)
    bt = R["bt"]
    worst = lambda h: max(abs(x[2]) for x in bt[h].values())
    wreg = lambda h: max(K.REG, key=lambda r: abs(bt[h][r][2]))
    fac = R["factors_route"]
    nyn = {r: R["est"]["route"][r] - R["notified"][r] for r in K.REG}
    ult = R["est"]["route"]
    A = R["ask_a"]
    CV = ("COMP", "TPFT", "TPO")
    extras = {"cmc_tpi_21m": cmc, "cmc_closed_range": [lo, hi],
              "bt_route_worst": round(worst("route"), 2), "bt_cmc_rest_worst": round(worst("cmc_rest"), 2),
              "bt_pooled": round(bt["pooled"][wreg("pooled")][2], 2), "bt_head": round(bt["head"][wreg("head")][2], 2),
              "bt_notified_by": round(bt["notified_by"][wreg("notified_by")][2], 2),
              "bt_representative": round(bt["representative"][wreg("representative")][2], 2),
              "bt_region": round(bt["region"][wreg("region")][2], 2),
              "tolerance": K.TOLERANCE, "totals_a": [sum(A[(r, c)] for r in K.REG) for c in CV],
              "cars_by_region": {r: sum(A[(r, c)] for c in CV) for r in K.REG}, "cy_total": round(sum(R["cy"].values()), 2),
              "notified_total_2025": sum(R["notified"].values()), "per_car_years": 100,
              "standard_clauses": ["2.1", "2.2", "2.3", "3.1", "3.2", "3.3"]}
    pd_ = lambda h, r: "%.1f" % R["freq"][h][r]
    g1 = "%.1f" % (R["gap"] + 1e-12)
    cells_a = "; ".join("%s %s COMP, %s TPFT and %s TPO" % (r, fmt(A[(r, "COMP")]), fmt(A[(r, "TPFT")]), fmt(A[(r, "TPO")]))
                        for r in K.REG)
    L = []
    L += ["## Tags", "", "**Domain:** Actuarial Science & Insurance (claims frequency and severity).",
          "**Analytical objective:** Descriptive & Distribution Analysis.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Put the 2027 telematics pilot in %s and %s.**" % (o[0], o[1]),
          "Their private cars had the two highest claim frequencies in accident year 2025, %s and %s claims per 100 "
          "car-years, and %s, third at %s, is %s below %s. Not %s and %s, which the whole book's development gives "
          "pooled, by head of claim or by the notified-by field: each blends the claims-management companies that "
          "notify Pennine's 2025 injury claims late with faster notifiers, and each misses 2022 in Wessex by %s to %s "
          "per cent, outside the Reserving Standard's two."
          % (pd_("route", o[0]), pd_("route", o[1]), o[2], pd_("route", o[2]), g1, o[1], o[0], o[2],
             "%.1f" % abs(extras["bt_notified_by"]), "%.1f" % abs(extras["bt_pooled"])), ""]
    L += ["## 2. Critical Components", "",
          "1. Claim frequency, accident year 2025, per 100 car-years earned in 2025: " +
          "; ".join("%s **%s**" % (r, pd_("route", r)) for r in o) + "; gap from %s to %s **%s**." % (o[1], o[2], g1),
          "2. Car-years earned in 2025, private cars: " + "; ".join("%s **%s**" % (r, fmt(R["cy"][r], 2)) for r in o) + ".",
          "3. Claims from 2025 accidents notified by 30 September 2026: " +
          "; ".join("%s **%s**" % (r, fmt(R["notified"][r])) for r in o) + ".",
          "4. The development by notifying route reproduces accident year 2022 within **%.1f** per cent in every "
          "region, as the Standard's 3.3 requires." % worst("route"), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Summed the private-car rows of the 2025 sheet of earned_exposure_2019_2025.xlsx, the earned exposure "
          "telematics_pilot_terms_2027.pdf term 3 names: %s car-years in all." % fmt(sum(R["cy"].values()), 2),
          "2. Counted private-car claims in motor_claims_notified_2019_2026.csv by the Standard's 2.1, each in its "
          "region from postcode_district_sales_regions.csv and notified on its UK date: %s claims from 2025 accidents "
          "by 30 September 2026." % fmt(sum(R["notified"].values())),
          "3. Gave each claim its notifying route, the notified-by field with representatives split by the firm type in "
          "claimant_representatives.csv, and measured the whole book's factors from 21 months to final on the closed "
          "years 2019 to 2022 (Standard 3.1, 3.2): %.1f for claims-management companies against %.1f for solicitors."
          % (fac["Claims management company"], fac["Solicitor practice"]),
          "4. Re-ran each development on accident year 2022 from 30 September 2023 with 2019 to 2021 (Standard 3.3): "
          "the route development is within %.1f per cent in every region, while pooled, by head of claim and by "
          "notified-by field miss Wessex by %.1f to %.1f per cent."
          % (worst("route"), abs(extras["bt_notified_by"]), abs(extras["bt_pooled"])),
          "5. For cars on cover, applied the address and cover changes in policy_changes_2025_2026.csv effective from "
          "each term's start to 30 September 2026 to the private cars on cover that day in "
          "policy_vehicles_in_force_20260930.csv, whose rows carry the district and cover at the term's start: %s."
          % cells_a,
          "6. Applied the route factors to each region's 2025 notified claims and divided by its car-years: %s; %s and %s "
          "host the pilot." % ("; ".join("%s %s" % (r, pd_("route", r)) for r in o), o[0], o[1]), ""]
    L += ["## 4. Deliverable Answers", "", "### %s" % K.GOLDEN, "",
          "1. Pilot regions: %s and %s." % (o[0], o[1]),
          "2. Claim frequency, accident year 2025, per 100 car-years, one decimal:"]
    for r in o:
        L.append("   - %s: %s" % (r, pd_("route", r)))
    L.append("3. Gap between the second region and the third, %s to %s: %s" % (o[1], o[2], g1))
    L.append("4. Private cars on cover on 30 September 2026, by cover, whole cars:")
    for r in K.REG:
        L.append("   - %s: %s COMP, %s TPFT, %s TPO" % (r, fmt(A[(r, "COMP")]), fmt(A[(r, "TPFT")]), fmt(A[(r, "TPO")])))
    L += ["", "### %s" % K.DECK, "",
          "1. Slide 1 names %s and %s as the pilot regions, at %s and %s claims per 100 car-years." % (
              o[0], o[1], pd_("route", o[0]), pd_("route", o[1])),
          "2. Slide 2 charts the five regions' 2025 frequency as stacked columns, claims notified by 30 September 2026 "
          "and claims still to come, the two pilot regions named and the gap of %s stated." % g1,
          "3. Slide 3 sets each development's 2022 back-test beside the Pennine and Severn frequency it gives.",
          "4. Slide 4 carries the cars on cover by region and cover as in the workbook.", ""]
    return "\n".join(L), extras
