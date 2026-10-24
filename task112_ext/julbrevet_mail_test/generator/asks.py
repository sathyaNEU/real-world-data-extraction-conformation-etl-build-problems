# The supplemental asks of the build, computed from the patched inputs, with the routes the two devices are aimed
# against. Usage: python3 -I asks.py <inputs dir> [figures.json]
import json, sys
import numpy as np, pandas as pd

D = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else None
UPGRADE = {"BV110": "2027-10-26", "BV113": "2027-10-26", "BV114": "2027-10-26", "BV115": "2027-10-26",
           "BV118": "2027-11-02", "BV119": "2027-11-02", "BV101": "2027-11-09", "BV104": "2027-11-09",
           "BV106": "2027-11-09", "BV128": "2027-11-16", "BV129": "2027-11-16", "BV132": "2027-11-16",
           "BV138": "2027-11-16", "BV141": "2027-11-16"}
FORMATS, WEEKS = ["Stor", "Mellan", "Nära"], [48, 49, 50, 51]

pos = pd.read_csv(f"{D}/pos_offer_redemptions_2027.csv", sep=";", decimal=",",
                  dtype={"receipt_id": str, "member_id": str, "offer_code": str, "store_code": str})
stores = pd.read_csv(f"{D}/stores.csv", dtype=str).set_index("store_code")
jul = pos[pos.offer_code.isin(["BV27-13-O1", "BV27-13-O2"])].copy()
assert jul.redeemed_at.str[:10].between("2027-12-01", "2027-12-24").all()
up = jul.store_code.map(UPGRADE)
jul["gross_till"] = up.notna() & (jul.redeemed_at.str[:10] >= up.fillna("9999"))
jul["paid"] = jul.receipt_total_sek - np.where(jul.gross_till, jul.discount_sek, 0.0)   # the BI warehouse's basis
jul["format"] = jul.store_code.map(stores.format)
jul["week"] = pd.to_datetime(jul.redeemed_at).dt.isocalendar().week.astype(int)
coded = jul.offer_code == "BV27-13-O2"
fifty = (jul.offer_code == "BV27-13-O1") & (jul.discount_sek == 50)
# an O1-coded redemption with exactly 50 SEK off a basket over 700 SEK is the O2 offer under the campaign's first code
o2 = coded | (fifty & (jul.paid + jul.discount_sek > 700))
assert set(jul.week[o2]) == set(WEEKS) and (jul.discount_sek[o2] == 50).all()

def figures(sel, paid):
    band = sel & (paid + 50 < 750)                     # basket before the 50 kr discount under 750 SEK
    out = {}
    for f in FORMATS:
        x = band & (jul.format == f)
        out[f"F|{f}|receipts"] = int(x.sum())
        out[f"F|{f}|paid"] = round(float(paid[x].sum()) / 1000, 1)
    for w in WEEKS:
        x = band & (jul.week == w)
        out[f"W|{w}|receipts"] = int(x.sum())
        out[f"W|{w}|paid"] = round(float(paid[x].sum()) / 1000, 1)
    out["M|receipts"] = int(band.sum())
    out["M|paid"] = round(float(paid[band].sum()) / 1000, 1)
    for f in FORMATS:
        for w in WEEKS:
            out[f"C|{w}|{f}"] = int((band & (jul.format == f) & (jul.week == w)).sum())
    return out

gold = figures(o2, jul.paid)
tot = jul.receipt_total_sek
variants = {
    "the code read as the offer, the total as paid": figures(coded, tot),
    "the code read as the offer, tills repaired": figures(coded, jul.paid),
    "O2 recovered from O1, the total as paid": figures(coded | (fifty & (tot + 50 > 700)), tot),
    "O2 recovered, the discount off at every till": figures(coded | (fifty & (tot > 700)), tot - jul.discount_sek),
    "every 50 SEK O1 row taken as O2, tills repaired": figures(coded | fifty, jul.paid),
}
print("Julbrevet O2 redemptions", int(o2.sum()), "of which under O1", int((o2 & ~coded).sum()),
      "on before-discount tills", int((o2 & jul.gross_till).sum()))
for k, v in gold.items():
    if not k.startswith("C|"):
        print(f"{k:16s} {v}")
graded = [k for k in gold if not k.startswith("C|")]
for name, fig in variants.items():
    keep = [k for k in graded if abs(fig[k] - gold[k]) < 1e-9]
    miss = min(abs(fig[k] / gold[k] - 1) for k in graded if gold[k])
    print(f"{name:50s} keeps {len(keep)} of {len(graded)}; smallest miss {miss:.0%}; total {fig['M|receipts']}")
if OUT:
    json.dump(gold, open(OUT, "w"), ensure_ascii=False, indent=1)
