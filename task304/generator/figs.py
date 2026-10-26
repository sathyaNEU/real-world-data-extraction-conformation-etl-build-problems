"""Compute every figure the goldens and the write-up state, from the pack alone, and write figures.json."""
import json

import params as P
import solve as S


def ten(v):
    return int(round(v / 10.0) * 10)


def r100(v):
    return int(round(v / 100.0) * 100)


def compute(target):
    H, B = S.load(target)
    g = S.main_call(target, H, B)
    e = S.main_call(target, H, B, route="default")
    rates = g["rates"]
    av = g["avoided"]
    order = sorted(P.ORDER, key=lambda b: -av[b])
    facts = S.ext_facts(H, B)
    books = S.account_books(target)
    a = S.ask_a(target, books)
    _, aS = S.litigation_state(target, books)
    _, oS = S.hearing_orders(target, books)
    b, bS = S.losses(target, books)
    oo = P.ORDER[:3]
    fig = {
        "call": {"book": g["book"], "next_best": order[1],
                 "avoided": {P.SHORT[k]: round(av[k], 1) for k in P.ORDER},
                 "avoided_ten": {P.SHORT[k]: ten(av[k]) for k in P.ORDER},
                 "rate_pct": {P.SHORT[k]: round(100 * rates[k], 1) for k in P.ORDER}},
        "easy": {"book": e["book"], "avoided": {P.SHORT[k]: round(e["avoided"][k], 1) for k in P.ORDER},
                 "avoided_ten": {P.SHORT[k]: ten(e["avoided"][k]) for k in P.ORDER}},
        "ext": {"ftb_raised_2026": facts["ftb_raised_2026"], "ftb_on_book": facts["ftb_on_book"],
                "years_added_median": int(round(facts["years_added_median"])),
                "pay_rise_extended": int(round(facts["pay_rise_extended"])),
                "pay_rise_kept": int(round(facts["pay_rise_kept"])),
                "raised_2024": facts["raised_2024"], "behind_8m": facts["behind_8m"],
                "behind_by_asof": facts["behind_by_asof"]},
        "askA": {P.SHORT[k]: {"orders": a[k]["orders"], "suspended": a[k]["suspended"], "open": a[k]["open"]}
                 for k in oo},
        "askB": {P.SHORT[k]: {"sold": b[k]["sold"], "at_loss": b[k]["at_loss"], "avg_loss": r100(b[k]["avg_loss"])}
                 for k in oo},
        # the conventions the write-up states: the filed cut, the fit's cells and its smoothing, the dates
        "basis": {"effect_pct": int(round(100 * P.EFFECT)), "rise_bands_pct": [5, 20, 40],
                  "term_bands_months": [8, 15, 16], "smoothing_weight": 20, "as_of": "30 September 2026",
                  "forecast_year": 2027},
    }
    oS = oS.assign(date=oS.d.dt.strftime("%Y-%m-%d"))
    bS = bS.assign(completion_date=bS.d.dt.strftime("%Y-%m-%d"))
    detail = {"claims": aS.to_dict("records"),
              "orders": oS[oS.book.isin(oo)][["claim_number", "account_number", "book", "date", "action",
                                              "detail"]].sort_values(["book", "date", "claim_number"]).to_dict("records"),
              "sales": bS[bS.book.isin(oo)][["completion_date", "acct", "book", "debt", "sale_price", "selling_costs",
                                             "loss"]].sort_values(["book", "completion_date", "acct"]).to_dict("records")}
    return fig, detail


def write(fig, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
