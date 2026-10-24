# How the self-service relabel draw (SEED in patch.py) was picked: each one-device route has to miss every graded
# ask figure, and the threshold band has to be recoded at about the rate of all O2 redemptions. The script lists the
# draws within half a point of that rate with their smallest one-device miss; 150 was taken from that list
# (smallest miss 43 percent). Runs on the built inputs. Usage: python3 -I seed_search.py <inputs dir>
import sys
import numpy as np, pandas as pd
D = sys.argv[1]
UP = {"BV110": "2027-10-26", "BV113": "2027-10-26", "BV114": "2027-10-26", "BV115": "2027-10-26",
      "BV118": "2027-11-02", "BV119": "2027-11-02", "BV101": "2027-11-09", "BV104": "2027-11-09",
      "BV106": "2027-11-09", "BV128": "2027-11-16", "BV129": "2027-11-16", "BV132": "2027-11-16",
      "BV138": "2027-11-16", "BV141": "2027-11-16"}
SHARE = {"Stor": 0.55, "Mellan": 0.45, "Nära": 0.40}
FORMATS, WEEKS = ["Stor", "Mellan", "Nära"], [48, 49, 50, 51]
pos = pd.read_csv(f"{D}/pos_offer_redemptions_2027.csv", sep=";", decimal=",", dtype={"receipt_id": str, "member_id": str, "offer_code": str, "store_code": str})
st = pd.read_csv(f"{D}/stores.csv", dtype=str).set_index("store_code")
up = pos.store_code.map(UP)
gross = up.notna() & (pos.redeemed_at.str[:10] >= up.fillna("9999"))
paidA = pos.receipt_total_sek - np.where(gross, pos.discount_sek, 0.0)
fmt = pos.store_code.map(st.format)
week = pd.to_datetime(pos.redeemed_at).dt.isocalendar().week.astype(int)
# the true offer of every row: an O1 row with 50 SEK off a basket over 700 SEK is a recoded O2 redemption
true_o2 = (pos.offer_code == "BV27-13-O2") | ((pos.offer_code == "BV27-13-O1") & (pos.discount_sek == 50) & (paidA + 50 > 700))
isO2 = true_o2
isO1 = (pos.offer_code == "BV27-13-O1") & ~true_o2

def relabel(seed):
    rng = np.random.default_rng(seed)
    share = {s: SHARE[st.format[s]] + rng.uniform(-0.06, 0.06) for s in sorted(st.index)}
    u = rng.random(len(pos))
    return isO2 & (u < pos.store_code.map(share).values)

def figs(sel, paid):
    band = sel & (paid + 50 < 750)
    out = {}
    for f in FORMATS:
        x = band & (fmt == f); out[f"F|{f}|receipts"] = int(x.sum()); out[f"F|{f}|paid"] = round(float(paid[x].sum()) / 1000, 1)
    for w in WEEKS:
        x = band & (week == w); out[f"W|{w}|receipts"] = int(x.sum()); out[f"W|{w}|paid"] = round(float(paid[x].sum()) / 1000, 1)
    out["M|receipts"] = int(band.sum()); out["M|paid"] = round(float(paid[band].sum()) / 1000, 1)
    return out

gold = figs(isO2, paidA)          # the truth: every O2 redemption, on the BI basis
best = []
for seed in range(1, 400):
    rl = relabel(seed)
    o2c = isO2 & ~rl                       # still coded O2 after the relabel
    o1c = isO1 | rl
    fifty = o1c & (pos.discount_sek == 50)
    routes = {
        "easy": figs(o2c, pos.receipt_total_sek),
        "A only": figs(o2c, paidA),
        "B only": figs(o2c | (fifty & (pos.receipt_total_sek + 50 > 700)), pos.receipt_total_sek),
    }
    # the golden handling must recover the truth exactly
    rec = figs(o2c | (fifty & (paidA + 50 > 700)), paidA)
    assert rec == gold, seed
    worst = min(abs(r[k] / gold[k] - 1) for r in routes.values() for k in gold if gold[k])
    best.append((worst, seed, int(rl.sum())))
band = isO2 & (paidA + 50 < 750)
pick = []
for w, s, n in best:
    rl = relabel(s)
    gap = abs((rl & band).sum() / band.sum() - rl.sum() / isO2.sum())
    if gap <= 0.005 and w >= 0.35:
        pick.append((w, s, n, gap))
pick.sort(reverse=True)
print("gold", gold)
for w, s, n, gap in pick:
    print(f"seed {s}: smallest one-device miss {w:.0%}, recoded {n}, band share gap {gap:.4f}")
s = 150
rl = relabel(s); o2c = isO2 & ~rl; o1c = isO1 | rl; fifty = o1c & (pos.discount_sek == 50)
for name, r in {"easy": figs(o2c, pos.receipt_total_sek), "A only": figs(o2c, paidA),
                "B only": figs(o2c | (fifty & (pos.receipt_total_sek + 50 > 700)), pos.receipt_total_sek)}.items():
    print(name, {k: (r[k], gold[k]) for k in gold})
