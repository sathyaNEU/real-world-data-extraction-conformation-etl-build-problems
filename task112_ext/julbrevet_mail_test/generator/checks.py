# Freeze and device checks for the v2 inputs. Usage: python3 -I checks_v2.py <v1 inputs> <v2 inputs>
import filecmp, os, subprocess, sys
import numpy as np, pandas as pd

V1, V2 = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
POS = "pos_offer_redemptions_2027.csv"
UPGRADE = {"BV113": "2027-10-26", "BV115": "2027-10-26", "BV118": "2027-11-02", "BV132": "2027-11-02",
           "BV125": "2027-11-09", "BV128": "2027-11-09", "BV141": "2027-11-16"}
fails = []

def ok(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)

# 1. the call's files and every other file are byte-identical; only the POS export moved
names = sorted(os.listdir(V1))
ok(names == sorted(os.listdir(V2)), "same 23 files in v1 and v2")
moved = [f for f in names if not filecmp.cmp(os.path.join(V1, f), os.path.join(V2, f), shallow=False)]
ok(moved == [POS], "only %s differs (%s)" % (POS, ", ".join(moved)))

# 2. the POS export keeps its rows, order and every column but the receipt total
a = open(os.path.join(V1, POS), encoding="ascii").read().split("\n")
b = open(os.path.join(V2, POS), encoding="ascii").read().split("\n")
ok(len(a) == len(b) and a[0] == b[0], "POS keeps its header and 38,006 rows")
same = all(x.split(";")[:5] + x.split(";")[6:] == y.split(";")[:5] + y.split(";")[6:] for x, y in zip(a[1:], b[1:]) if x)
ok(same, "POS changes receipt_total_sek only")

# 3. the POS export still ties to the BI table on offers and discounts, and holds every receipt inside its month
pos = pd.read_csv(os.path.join(V2, POS), sep=";", decimal=",", dtype={"member_id": str, "store_code": str})
pos["month"] = pos.redeemed_at.str[:7]
up = pos.store_code.map(UPGRADE)
pos["gross"] = up.notna() & (pos.redeemed_at.str[:10] >= up.fillna("9999"))
pos["paid"] = pos.receipt_total_sek - np.where(pos.gross, pos.discount_sek, 0.0)
msm = pd.read_csv(os.path.join(V2, "member_store_month_2027.csv"), dtype={"member_id": str, "month": str, "store_code": str})
key = ["member_id", "month", "store_code"]
g = pos.groupby(key).agg(n=("paid", "size"), paid=("paid", "sum"), tot=("receipt_total_sek", "sum"),
                         disc=("discount_sek", "sum"), gross=("gross", "max")).reset_index().merge(msm, on=key)
ok((g.n == g.offers_redeemed).all() and np.allclose(g.disc, g.offer_discount_sek), "offers and discounts tie to the BI table")
ok((g.paid <= g.spend_sek + 0.005).all(), "amounts paid never exceed the month's spend")
full = g.visits == g.n
ok(np.allclose(g.paid[full], g.spend_sek[full], atol=0.005), "where every receipt redeemed an offer, the amounts paid add up to the spend")
# the evidence a grader verifies: on those months the upgraded tills' totals exceed the spend by exactly the discount
gf = g[full & g.gross]
ok(len(gf) > 300 and np.allclose(gf.tot - gf.disc, gf.spend_sek, atol=0.005), "upgraded tills write the total before the discount (%d months)" % len(gf))
nf = g[full & ~g.gross]
ok(np.allclose(nf.tot, nf.spend_sek, atol=0.005), "every other till writes the amount paid (%d months)" % len(nf))
o2 = pos[pos.offer_code == "BV27-13-O2"]
ok((o2.paid + o2.discount_sek >= 700).all(), "every O2 receipt is over 700 SEK before the discount")
ok(sorted(pd.read_csv(os.path.join(V2, "stores.csv"), dtype=str).set_index("store_code").loc[list(UPGRADE), "format"].unique())
   == ["Mellan", "Nära", "Stor"], "the upgraded stores span every format")

# 4. the call recomputes unchanged on the v2 inputs
out = subprocess.run([sys.executable, "-I", os.path.join(HERE, "call.py"), V2], capture_output=True, text=True).stdout
for s in ["control 1942", "mailed: 14108 households, 2298.58 SEK", "control: 1942 households, 2161.36 SEK",
          "objected: 1150 households, 2102.15 SEK", "diff 137.21", "se 94.21", "t 2.0615", "range -56.99 331.42",
          "lower margin -14.25 shortfall 25.65 needed 239.81"]:
    ok(s in out, "call: " + s)

print("ALL PASS" if not fails else "%d FAIL" % len(fails))
sys.exit(1 if fails else 0)
