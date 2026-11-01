"""Every owed figure, computed once from target/ by solve.py and carried, as stated, into the goldens, the write-up
and figures.json."""
import solve as S

WARDS = ["Abbots Hollow", "Brindley Moor", "Calder Bank", "Dunmore", "Eastholme", "Fennick", "Gorsey Hill",
         "Hollin Edge", "Kestrel Rise", "Moss Brow", "Pellbury", "Wexley"]


def r1(x):
    return round(float(x) + 1e-12, 1)


def compute(target):
    G = S.golden(target)
    D = S.solve(target, drop_works=False)
    ch = {w: r1(G["change"][w]) for w in WARDS}
    every = {w: r1(D["change"][w]) for w in WARDS}
    press = G["pressured"]
    default_press = S.pressured(D["change"])
    homes = {w: int(G["homes"].get(w, 0)) for w in WARDS}
    sh = {w: int(G["shares"].get(w, 0)) for w in WARDS}
    tot_d = sum(homes[w] for w in default_press)
    default_sh = {w: int(round(S.POT * homes[w] / tot_d)) if w in default_press else 0 for w in WARDS}
    n_pairs = sum(1 for k, a, b in D["pairs"] if b["date"].year == 2026 and D["ward_of"].get(S.norm_pc(b["postcode"])) == "Pellbury")
    n_clean = sum(1 for k, a, b in G["S"]["pairs"] if b["date"].year == 2026 and G["S"]["ward_of"].get(S.norm_pc(b["postcode"])) == "Pellbury")
    fig = {
        "call": {"pressured": press, "shares": {w: sh[w] for w in press},
                 "shares_text": {w: "GBP {:,}".format(sh[w]) for w in press},
                 "homes": {w: homes[w] for w in press}, "homes_total": sum(homes[w] for w in press),
                 "pot": S.POT, "pot_text": "GBP 12,000,000", "line": S.LINE},
        "change": ch,
        "change_3dp": {w: round(float(G["change"][w]), 3) for w in WARDS},
        "pellbury": {"golden": ch["Pellbury"], "every_pair": every["Pellbury"],
                     "pairs_2026_every": n_pairs, "pairs_2026_kept": n_clean},
        "default": {"pressured": default_press, "change": every, "shares": default_sh},
        "homes": homes,
        "ask_a": {w: int(G["supply"].get(w, 0)) for w in WARDS},
        "ask_b_count": {w: int(G["company_n"].get(w, 0)) for w in WARDS},
        "ask_b_money": {w: int(G["company_money"].get(w, 0)) for w in WARDS},
        "ask_b_money_text": {w: "GBP {:,}".format(int(G["company_money"].get(w, 0))) for w in WARDS},
        "ask_c": {w: int(G["starts"].get(w, 0)) for w in WARDS},
    }
    fig["window"] = {"from": 2025, "to": 2026, "programme_year": "2027-28", "chart_page": 1}
    fig["ask_a_total"] = sum(fig["ask_a"].values())
    fig["ask_b_count_total"] = sum(fig["ask_b_count"].values())
    fig["ask_b_money_total"] = sum(fig["ask_b_money"].values())
    fig["ask_c_total"] = sum(fig["ask_c"].values())
    return fig


if __name__ == "__main__":
    import json
    import sys
    print(json.dumps(compute(sys.argv[1] if len(sys.argv) > 1 else S.TARGET), indent=1))
