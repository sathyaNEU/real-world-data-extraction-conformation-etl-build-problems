"""task146 architecture 2: submission.md, figures.json and metadata.json, every figure from the golden run."""
import json
import os

import golden as G
import pack as PK

SRC = {
    "balances": "synthetic: the core banking system's month-end balance extract for instant-access accounts",
    "events": "synthetic: the core banking system's account event log (openings and closures)",
    "products": "synthetic: the Society's product register kept by product governance",
    "swaps": "synthetic: the treasury's register of structural hedge swaps",
    "bonds": "synthetic: the bond ledger's openings of fixed-rate bonds",
    "rates": "synthetic: the Society's savings rate history beside Bank Rate",
    "isa_in": "synthetic: cash ISA transfers received from other providers in 2026",
    "policy": "synthetic: the Asset and Liability Management Policy, section 7",
    "minutes": "synthetic: the Board minute extract on the January 2026 reset",
    "email": "synthetic: the Treasurer's request for the January 2027 reset",
}
WHY = {"bonds": "fixed-rate bonds are not instant-access savings (policy 7.2), so a bond a closing payment funded is not kept",
       "rates": "the stable balance is measured on balances kept, not on rates; the rate history explains margins",
       "isa_in": "transfers in from other providers are new money, outside the balances held on 30 November"}


def m(x):
    return int(round(x / 1e6))


def figures(res):
    g = res["golden"]
    f = {"call": {"hedge_m": m(res["hedge"]), "new_swap_m": m(res["hedge"] - res["after_january"]),
                  "swaps_now_m": round(res["swaps_now"] / 1e6, 1), "after_january_m": round(res["after_january"] / 1e6, 1)},
         "book_m": m(g["book"]),
         "now_m": {k: m(v) for k, v in g["now"].items()},
         "stable_m": {str(k): {x: m(y) for x, y in g["stable"][k].items()} for k in G.HORIZONS},
         "share": {str(k): {x: round(y, 4) for x, y in g["share"][k].items()} for k in G.HORIZONS}}
    return f


def submission(res, path):
    g = res["golden"]
    D = res["D"]
    acc = G.stable(D, money=False)
    new = m(res["hedge"] - res["after_january"])
    L = ["## Tags", "",
         "**Domain:** Banking, Credit & Financial Risk (deposit and liquidity behaviour: a building society's "
         "structural hedge on its instant-access savings).",
         "**Analytical objective:** Forecasting & Predictive Modeling.", "",
         "## 1. Final Recommendation", "",
         "**Set the structural hedge at GBP %d million in January 2027 and replace the maturing GBP 51 million swap "
         "with a new three-year swap of GBP %d million: Trentmoor will still hold GBP %d million of the GBP %d million "
         "instant-access savings of 30 November 2026 a year on.**" % (m(res["hedge"]), new, m(g["stable"][12]["total"]),
                                                                       m(g["book"])),
         "Run-off measured account by account puts the stable balance at GBP %d million, because a member who takes "
         "up a new Loyalty Saver issue closes one account and opens another the same day with the same amount; that "
         "money is still held in instant-access savings." % m(acc["stable"][12]["total"]), "",
         "## 2. Critical Components", "",
         "1. Each closing payment from an instant-access account that funded an instant-access opening the same local "
         "day for the same amount is the same money: the share kept to the first anniversary is **%.1f per cent** "
         "across the products, against %.1f per cent account by account." % (
             100 * g["stable"][12]["total"] / g["book"], 100 * acc["stable"][12]["total"] / acc["book"]),
         "2. The Society's stable balance a year on is **GBP %d million**, two years on **GBP %d million** and three "
         "years on **GBP %d million**." % (m(g["stable"][12]["total"]), m(g["stable"][24]["total"]),
                                          m(g["stable"][36]["total"])),
         "3. The swaps outstanding after the January 2027 maturity are **GBP %.1f million**, so the new swap is "
         "**GBP %d million**." % (res["after_january"] / 1e6, new), "",
         "## 3. Step-by-Step Solution", "",
         "1. Month-end balances read on their calendar month (the extract dates them on the last business day); "
         "product codes mapped on the product register by date (ES02 is Easy Saver Online to 30 June 2025 and Young "
         "Saver from 1 July 2025).",
         "2. Account events converted from UTC to UK local time; each CLOSE matched to the instant-access OPEN on the "
         "same local day with the same amount in pence.",
         "3. For every account with a balance at each 30 November from 2021, the money followed through its matched "
         "openings and its lowest month-end balance taken to each anniversary (a closure with no matched opening "
         "ends it).",
         "4. Each product's share kept: the kept balances over the 30 November balances, the start dates taken "
         "together, for one, two and three years.",
         "5. Each product's 30 November 2026 balance times its share; summed for the Society.",
         "6. The hedge is the first-anniversary stable balance to the nearest GBP 1 million (policy 7.4); the new "
         "swap brings the GBP %.1f million outstanding after January to it." % (res["after_january"] / 1e6), "",
         "## 4. Deliverable Answers", "", "### " + "structural_hedge_reset_2027.pdf", "",
         "1. Hedge from January 2027: GBP %d million." % m(res["hedge"]),
         "2. Change to the swaps: the maturing GBP 51 million swap replaced by a new three-year swap of GBP %d "
         "million." % new,
         "3. Chart of the stable balance at each anniversary (GBP %d, %d and %d million) against the swaps "
         "outstanding at each after the reset." % (m(g["stable"][12]["total"]), m(g["stable"][24]["total"]),
                                                  m(g["stable"][36]["total"])), "",
         "### " + "stable_balance_ladder_2026-11.xlsx", "",
         "1. Balance on 30 November 2026, GBP million: " + ", ".join("%s %d" % (f, m(g["now"][f])) for f in G.FAMILIES)
         + "; total %d." % m(g["book"])]
    for i, k in enumerate(G.HORIZONS):
        L.append("%d. Stable balance %d year%s on, GBP million: " % (i + 2, k // 12, "" if k == 12 else "s") +
                 ", ".join("%s %d" % (f, m(g["stable"][k][f])) for f in G.FAMILIES) +
                 "; total %d." % m(g["stable"][k]["total"]))
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


def metadata(path):
    files = []
    for k, name in PK.FILES.items():
        files.append({"name": name, "role": "distractor" if k in PK.DISTRACTORS else "evidence", "source": SRC[k],
                      "date": "2026-12-03", "license": "CC0 1.0 (synthetic, authored for this task)"})
    meta = {"task": "task146", "architecture": 2, "setting": "2026-12-03",
            "files": sorted(files, key=lambda f: f["name"]),
            "distractors": [PK.FILES[k] for k in PK.DISTRACTORS],
            "distractor_reasons": {PK.FILES[k]: WHY[k] for k in PK.DISTRACTORS},
            "deliverables": ["structural_hedge_reset_2027.pdf", "stable_balance_ladder_2026-11.xlsx"]}
    json.dump(meta, open(path, "w"), indent=1)


def write(target, res, out_task):
    submission(res, os.path.join(out_task, "submission.md"))
    metadata(os.path.join(out_task, "metadata.json"))
    gen = os.path.join(out_task, "generator")
    os.makedirs(gen, exist_ok=True)
    json.dump(figures(res), open(os.path.join(gen, "figures.json"), "w"), indent=1, sort_keys=True)
