# Freeze and device checks. Usage: python3 -I checks.py <v1 inputs> <built inputs>
import filecmp, io, os, runpy, subprocess, sys, zipfile, contextlib
import numpy as np, pandas as pd

V1, V2 = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
POS = "pos_offer_redemptions_2027.csv"
UPGRADE = {"BV110": "2027-10-26", "BV113": "2027-10-26", "BV114": "2027-10-26", "BV115": "2027-10-26",
           "BV118": "2027-11-02", "BV119": "2027-11-02", "BV101": "2027-11-09", "BV104": "2027-11-09",
           "BV106": "2027-11-09", "BV128": "2027-11-16", "BV129": "2027-11-16", "BV132": "2027-11-16",
           "BV138": "2027-11-16", "BV141": "2027-11-16"}
fails = []

def ok(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)

# 1. every file the call reads is byte-identical; the POS export moved, and the runbook gained one clause in 7.3
RUNBOOK = "messaging_operations_runbook_2027.docx"
names = sorted(os.listdir(V1))
ok(names == sorted(os.listdir(V2)), "same 23 files")
moved = [f for f in names if not filecmp.cmp(os.path.join(V1, f), os.path.join(V2, f), shallow=False)]
ok(moved == sorted([POS, RUNBOOK]), "only the POS export and the runbook differ (%s)" % ", ".join(moved))
za, zb = zipfile.ZipFile(os.path.join(V1, RUNBOOK)), zipfile.ZipFile(os.path.join(V2, RUNBOOK))
ia, ib = za.infolist(), zb.infolist()
ok([(i.filename, i.date_time) for i in ia] == [(i.filename, i.date_time) for i in ib], "the runbook keeps its parts and stamps")
same_parts = all(za.read(i.filename) == zb.read(i.filename) for i in ia if i.filename != "word/document.xml")
da, db = za.read("word/document.xml").decode("utf-8"), zb.read("word/document.xml").decode("utf-8")
ok(same_parts and db == da.replace("the till honours it accordingly.", "the till honours it accordingly, once for each member."),
   "the runbook's only change is 'once for each member' in 7.3")

# 2. the POS export keeps its rows and order; only the receipt total and, on Julbrevet O2 rows, the offer code move
a = [l.split(";") for l in open(os.path.join(V1, POS), encoding="ascii").read().split("\n")]
b = [l.split(";") for l in open(os.path.join(V2, POS), encoding="ascii").read().split("\n")]
ok(len(a) == len(b) and a[0] == b[0], "POS keeps its header and 38,006 rows")
ok(all(x[:2] + x[3:5] + x[6:] == y[:2] + y[3:5] + y[6:] for x, y in zip(a[1:], b[1:]) if len(x) > 1),
   "POS changes receipt_total_sek and offer_code only")
recoded = [(x[2], y[2]) for x, y in zip(a[1:], b[1:]) if len(x) > 1 and x[2] != y[2]]
ok(set(recoded) == {("BV27-13-O2", "BV27-13-O1")}, "the only code change is BV27-13-O2 written as BV27-13-O1 (%d rows)" % len(recoded))

# 3. the POS export still ties to the BI table on offers and discounts, and holds every receipt inside its month
pos = pd.read_csv(os.path.join(V2, POS), sep=";", decimal=",", dtype={"member_id": str, "store_code": str})
pos["month"] = pos.redeemed_at.str[:7]
up = pos.store_code.map(UPGRADE)
pos["gross"] = up.notna() & (pos.redeemed_at.str[:10] >= up.fillna("9999"))
pos["paid"] = pos.receipt_total_sek - np.where(pos.gross, pos.discount_sek, 0.0)
msm = pd.read_csv(os.path.join(V2, "member_store_month_2027.csv"), dtype={"member_id": str, "month": str, "store_code": str})
key = ["member_id", "month", "store_code"]
g = pos.groupby(key).agg(n=("paid", "size"), paid=("paid", "sum"), tot=("receipt_total_sek", "sum"),
                         disc=("discount_sek", "sum"), gross=("gross", "min"), any_gross=("gross", "max")).reset_index().merge(msm, on=key)
ok((g.n == g.offers_redeemed).all() and np.allclose(g.disc, g.offer_discount_sek), "offers and discounts tie to the BI table")
ok((g.paid <= g.spend_sek + 0.005).all(), "amounts paid never exceed the month's spend")
full = g.visits == g.n
ok(np.allclose(g.paid[full], g.spend_sek[full], atol=0.005), "where every receipt redeemed an offer, the amounts paid add up to the spend")
gf = g[full & g.gross]
ok(len(gf) > 300 and np.allclose(gf.tot - gf.disc, gf.spend_sek, atol=0.005), "upgraded tills write the total before the discount (%d months)" % len(gf))
nf = g[full & ~g.any_gross]
ok(np.allclose(nf.tot, nf.spend_sek, atol=0.005), "every other till writes the amount paid (%d months)" % len(nf))
dec_full = g[full & (g.month == "2027-12")]
print("     December full months: %d before-discount, %d after" % ((dec_full.gross).sum(), (~dec_full.any_gross).sum()))

# 4. the offer-code device: what a grader verifies, and that it leaves no absence or marker behind
truth = pd.Series([x[2] for x in a[1:] if len(x) > 1])
o1 = pos.offer_code == "BV27-13-O1"
fifty = o1 & (pos.discount_sek == 50)
over = pos.paid + pos.discount_sek > 700
ok((pos[pos.offer_code == "BV27-13-O2"].pipe(lambda x: (x.discount_sek == 50) & (x.paid + 50 > 700))).all(), "every O2-coded redemption is 50 SEK off a basket over 700 SEK")
ok(((fifty & over) == (truth == "BV27-13-O2").values & o1).all(), "the O1 rows with 50 SEK off a basket over 700 SEK are exactly the O2 redemptions under O1 (%d)" % int((fifty & over).sum()))
ok(int((fifty & ~over).sum()) == 1, "one O1 row has 50 SEK off a basket under 700 SEK, a ham at 200 SEK")
ok(not (o1 & ~fifty & over & (pos.discount_sek == 50)).any(), "no other O1 row carries the O2 terms")
dup = pos[pos.duplicated(["member_id", "offer_code"], keep=False)]
ok(set(dup.offer_code) == {"BV27-13-O1"}, "accounts redeem an offer twice only under BV27-13-O1 (%d accounts)" % dup.member_id.nunique())
ok(not pd.Series([x[1] + x[2] for x in a[1:] if len(x) > 1]).duplicated().any(), "before the recode every member redeems each offer once, as runbook 7.3 says")
pairs = dup.assign(o2=(dup.discount_sek == 50) & (dup.paid + 50 > 700)).groupby("member_id").o2.agg(["sum", "size"])
ok((pairs["size"] == 2).all() and (pairs["sum"] == 1).all(), "each such account has one 50 SEK over-700 row and one ham row")
o2_true = truth.values == "BV27-13-O2"
by_store = pd.crosstab(pos.store_code[o2_true], pos.offer_code[o2_true])
ok((by_store > 0).all().all(), "every store has O2 redemptions under both codes, so no store is missing the offer")
print("     share under O1 by store: %.2f to %.2f" % ((by_store["BV27-13-O1"] / by_store.sum(axis=1)).min(), (by_store["BV27-13-O1"] / by_store.sum(axis=1)).max()))

# 5. each one-device route misses every graded figure
with contextlib.redirect_stdout(io.StringIO()):
    sys.argv = ["asks.py", V2]
    A = runpy.run_path(os.path.join(HERE, "asks.py"))
gold, variants = A["gold"], A["variants"]
graded = [k for k in gold if not k.startswith("C|")]
for name in ["the code read as the offer, the total as paid", "the code read as the offer, tills repaired",
             "O2 recovered from O1, the total as paid", "O2 recovered, the discount off at every till"]:
    fig = variants[name]
    miss = min(abs(fig[k] / gold[k] - 1) for k in graded if gold[k])
    ok(miss >= 0.2, "%s misses every graded figure (smallest miss %.0f%%)" % (name, 100 * miss))

# 6. the call recomputes unchanged
out = subprocess.run([sys.executable, "-I", os.path.join(HERE, "call.py"), V2], capture_output=True, text=True).stdout
for s in ["control 1942", "mailed: 14108 households, 2298.58 SEK", "control: 1942 households, 2161.36 SEK",
          "objected: 1150 households, 2102.15 SEK", "diff 137.21", "se 94.21", "t 2.0615", "range -56.99 331.42",
          "lower margin -14.25 shortfall 25.65 needed 239.81"]:
    ok(s in out, "call: " + s)

print("ALL PASS" if not fails else "%d FAIL" % len(fails))
sys.exit(1 if fails else 0)
